"""Figures for Chapter 34 — Launch Vehicle Engineering.

Most figures are computed: a 2-D ascent simulation of a Falcon 9-class two-stage kerosene vehicle
(planar, inertial polar coordinates, rotating spherical Earth, US 1976 atmosphere, Mach-dependent drag),
booster-return simulations, staging theory, a calibrated payload-performance model, GCAT launch statistics,
and payload environments from the Falcon User's Guide (May 2025).
"""
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from figlib import *  # noqa: F401,F403   (plt, np, palette, helpers)
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyBboxPatch, Wedge  # noqa: F401

import math
from scipy.optimize import brentq, fsolve

# ----------------------------------------------------------------------------------------------------------
# Constants and vehicle model (Falcon 9-class; approximate public values, see chapter text)
# ----------------------------------------------------------------------------------------------------------
MU = 3.986004418e14
RE = 6378.137e3
G0 = 9.80665
OMEGA = 7.2921159e-5
LAT = 28.5                         # Cape Canaveral
V_ROT = OMEGA * RE * math.cos(math.radians(LAT))   # 408 m/s eastward

S1 = dict(dry=25_600.0, prop=395_700.0, Fsl=7_607e3, Fvac=8_227e3, Ivac=312.0)
S2 = dict(dry=3_900.0, prop=92_670.0, Fvac=981e3, Ivac=348.0, resid=900.0)
FAIRING = 1_900.0
AREF = math.pi * (3.66 / 2) ** 2   # 10.5 m^2
FMH_LIMIT = 1_135.0                # W/m^2, fairing jettison criterion (Falcon User's Guide)

# US Standard Atmosphere 1976 (geopotential layers to 84.852 km) + tabulated density above
_LAYERS = [(0.0, 288.15, -6.5e-3), (11e3, 216.65, 0.0), (20e3, 216.65, 1.0e-3), (32e3, 228.65, 2.8e-3),
           (47e3, 270.65, 0.0), (51e3, 270.65, -2.8e-3), (71e3, 214.65, -2.0e-3), (84.852e3, 186.946, 0.0)]
_P = [101325.0]
for _i in range(len(_LAYERS) - 1):
    _hb, _Tb, _L = _LAYERS[_i]
    _h1 = _LAYERS[_i + 1][0]
    if _L == 0:
        _P.append(_P[-1] * math.exp(-G0 * 0.0289644 / (8.31446 * _Tb) * (_h1 - _hb)))
    else:
        _P.append(_P[-1] * (_Tb / (_Tb + _L * (_h1 - _hb))) ** (G0 * 0.0289644 / (8.31446 * _L)))
_HI = np.array([86, 90, 100, 110, 120, 130, 150, 200, 300, 500, 1000]) * 1e3
_RHOHI = np.log(np.array([6.958e-6, 3.416e-6, 5.604e-7, 9.708e-8, 2.222e-8, 8.152e-9, 2.076e-9, 2.541e-10,
                          1.916e-11, 5.215e-13, 3.561e-15]))


def atmos(h):
    """Return (pressure Pa, density kg/m3, speed of sound m/s) at geometric altitude h (m)."""
    if h < 0:
        h = 0.0
    if h < 86e3:
        z = RE * h / (RE + h)
        i = 0
        while i < len(_LAYERS) - 1 and z >= _LAYERS[i + 1][0]:
            i += 1
        hb, Tb, L = _LAYERS[i]
        T = Tb + L * (z - hb)
        if L == 0:
            p = _P[i] * math.exp(-G0 * 0.0289644 / (8.31446 * Tb) * (z - hb))
        else:
            p = _P[i] * (Tb / T) ** (G0 * 0.0289644 / (8.31446 * L))
        rho = p * 0.0289644 / (8.31446 * T)
        return p, rho, math.sqrt(1.4 * 287.053 * T)
    rho = math.exp(np.interp(h, _HI, _RHOHI))
    return rho * 287.053 * 200.0, rho, 280.0


_MACH = [0.0, 0.6, 0.85, 1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]
_CD = [0.27, 0.27, 0.34, 0.48, 0.50, 0.45, 0.38, 0.31, 0.26, 0.24]


def cd_body(m):
    return float(np.interp(m, _MACH, _CD))


# ----------------------------------------------------------------------------------------------------------
# Ascent simulation
# ----------------------------------------------------------------------------------------------------------
def s1_throttle(t):
    """Throttle bucket around max-Q (fraction of full thrust)."""
    if t < 45:
        return 1.0
    if t < 55:
        return 1.0 - 0.25 * (t - 45) / 10
    if t < 75:
        return 0.75
    if t < 85:
        return 0.75 + 0.25 * (t - 75) / 10
    return 1.0


def _deriv(t, s, F, mdot, aim, area, cd_scale=1.0):
    """s = [r, th, vr, vt, m]; aim(t, s, vrel) -> unit thrust vector (ur, ut)."""
    r, th, vr, vt, m = s
    h = r - RE
    p, rho, a = atmos(h)
    vrr, vrt = vr, vt - OMEGA * math.cos(math.radians(LAT)) * r
    vrel = math.hypot(vrr, vrt)
    q = 0.5 * rho * vrel * vrel
    D = q * area * cd_body(vrel / a) * cd_scale
    ar = at = 0.0
    if vrel > 1e-6:
        ar -= D / m * vrr / vrel
        at -= D / m * vrt / vrel
    T = F(t, p, s) if F else 0.0
    ur = ut = 0.0
    if T > 0:
        ur, ut = aim(t, s, (vrr, vrt))
        ar += T / m * ur
        at += T / m * ut
    md = mdot(t, p, s) if mdot else 0.0
    return (np.array([vr, vt / r, vt * vt / r - MU / r ** 2 + ar, -vr * vt / r + at, -md]),
            (q, D, T, vrel, rho, p, ur, ut))


def rk4(f, t, s, dt):
    k1, _ = f(t, s)
    k2, _ = f(t + dt / 2, s + dt / 2 * k1)
    k3, _ = f(t + dt / 2, s + dt / 2 * k2)
    k4, _ = f(t + dt, s + dt * k3)
    return s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


KICK_T0, KICK_T1, KICK_DEG = 8.0, 18.0, 3.4


def stage1(payload, reserve=0.0, amax=None, record=None, dt=0.5, kick=None):
    """Fly stage 1 from lift-off to MECO. Returns state at MECO and time."""
    kick = KICK_DEG if kick is None else kick
    m_upper = S2["dry"] + S2["prop"] + FAIRING + payload
    m0 = S1["dry"] + S1["prop"] + m_upper
    m_meco = S1["dry"] + reserve + m_upper
    ve = S1["Ivac"] * G0
    mdot_full = S1["Fvac"] / ve

    def thr(t, s):
        k = s1_throttle(t)
        if amax:
            p, rho, a = atmos(s[0] - RE)
            Tfull = S1["Fvac"] - (S1["Fvac"] - S1["Fsl"]) * p / 101325.0
            k = min(k, max(0.57, amax * G0 * s[4] / Tfull))
        return k

    def F(t, p, s):
        return thr(t, s) * (S1["Fvac"] - (S1["Fvac"] - S1["Fsl"]) * p / 101325.0)

    def mdot(t, p, s):
        return thr(t, s) * mdot_full

    def aim(t, s, vrel):
        if t < KICK_T0:
            return 1.0, 0.0
        if t < KICK_T1:
            ang = math.radians(kick) * (t - KICK_T0) / (KICK_T1 - KICK_T0)
            return math.cos(ang), math.sin(ang)
        v = math.hypot(*vrel)
        # gravity turn: thrust along the air-relative velocity, never steeper than the kick attitude
        return vrel[0] / v, vrel[1] / v

    f = lambda t, s: _deriv(t, s, F, mdot, aim, AREF)  # noqa: E731
    s = np.array([RE, 0.0, 0.0, OMEGA * math.cos(math.radians(LAT)) * RE, m0])
    t = 0.0
    while s[4] > m_meco:
        step = dt
        md = mdot_full * thr(t, s)
        if s[4] - md * step < m_meco:
            step = (s[4] - m_meco) / md
        if record is not None:
            _, (q, D, T, vrel, rho, p, ur, ut) = f(t, s)
            record.append(dict(t=t, s=s.copy(), q=q, D=D, T=T, Tvac=thr(t, s) * S1["Fvac"], ur=ur, ut=ut,
                               stage=1, thr=thr(t, s)))
        s = rk4(f, t, s, step)
        t += step
        if step < dt:
            break
    return t, s


def stage2(t0, s0, payload, tan0, cslope, leftover_dv=0.0, record=None, dt=1.0, coast=11.0, h_target=200e3):
    """Coast `coast` s after MECO (separation), then fly stage 2 with linear-tangent steering until the
    orbital energy of a circular orbit at h_target is reached. Returns (t, state, propellant left)."""
    ve = S2["Ivac"] * G0
    mdot = S2["Fvac"] / ve
    r_t = RE + h_target
    e_target = -MU / (2 * r_t)
    # remove first stage
    s = s0.copy()
    s[4] = S2["dry"] + S2["prop"] + FAIRING + payload
    t = t0
    f0 = lambda t, s: _deriv(t, s, None, None, None, AREF)  # noqa: E731
    while t < t0 + coast:
        if record is not None:
            _, (q, D, T, vrel, rho, p, ur, ut) = f0(t, s)
            record.append(dict(t=t, s=s.copy(), q=q, D=D, T=0.0, Tvac=0.0, ur=0.0, ut=0.0, stage=0, thr=0.0))
        s = rk4(f0, t, s, 1.0)
        t += 1.0
    t_ign = t
    fairing_on = True
    m_burn_end = S2["dry"] + S2["resid"] + payload

    def aim(tt, ss, vrel):
        ang = math.atan(tan0 - cslope * (tt - t_ign))   # pitch above local horizontal
        return math.sin(ang), math.cos(ang)

    F = lambda tt, p, ss: S2["Fvac"]  # noqa: E731
    md = lambda tt, p, ss: mdot  # noqa: E731
    f = lambda tt, ss: _deriv(tt, ss, F, md, aim, AREF)  # noqa: E731
    t_fair = None
    while True:
        r, th, vr, vt, m = s
        energy = 0.5 * (vr * vr + vt * vt) - MU / r
        if energy >= e_target:
            break
        if fairing_on:
            _, rho, _ = atmos(r - RE)
            vrel = math.hypot(vr, vt - OMEGA * math.cos(math.radians(LAT)) * r)
            if 0.5 * rho * vrel ** 3 < FMH_LIMIT:
                s[4] -= FAIRING
                fairing_on = False
                t_fair = t
        if s[4] <= m_burn_end + (0 if fairing_on else 0):
            break
        if record is not None:
            _, (q, D, T, vrel, rho, p, ur, ut) = f(t, s)
            record.append(dict(t=t, s=s.copy(), q=q, D=D, T=T, Tvac=T, ur=ur, ut=ut, stage=2, thr=1.0))
        # refine last step so energy target is not overshot by much
        step = dt
        if energy > e_target - 5e5:
            step = 0.1
        if energy > e_target - 5e4:
            step = 0.02
        s = rk4(f, t, s, step)
        t += step
    prop_left = s[4] - (S2["dry"] + S2["resid"] + payload) - (FAIRING if fairing_on else 0)
    if leftover_dv > 0:
        m_end = S2["dry"] + S2["resid"] + payload
        need = (m_end + prop_left) - (m_end + prop_left) * math.exp(-leftover_dv / ve)
        prop_left -= need
    return t, s, prop_left, t_fair, t_ign


def solve_stage2(t0, s0, payload, guess=(0.6, 0.004), leftover_dv=0.0, h_target=200e3):
    def resid(x):
        t, s, pl, _, _ = stage2(t0, s0, payload, x[0], x[1], leftover_dv=leftover_dv, h_target=h_target)
        return [(s[0] - RE - h_target) / 1e4, s[2] / 50.0]
    best = None
    for g in (guess, (0.6, 0.004), (0.3, 0.002), (0.9, 0.006), (0.1, 0.001)):
        sol, info, ier, msg = fsolve(resid, g, full_output=True, xtol=1e-6)
        t, s, pl, tf, ti = stage2(t0, s0, payload, sol[0], sol[1], leftover_dv=leftover_dv, h_target=h_target)
        ok = abs(s[0] - RE - h_target) < 500 and abs(s[2]) < 5
        if ok:
            return sol, pl, True
        best = (sol, pl)
    return best[0], -1e5, False


def max_payload(reserve=0.0, leftover_dv=0.0, h_target=200e3, kick=None, lo=500, hi=30_000):
    """Largest payload (kg) for which stage 2 reaches the target with zero spare propellant."""
    cache = {"g": (0.6, 0.004)}

    def g(P):
        t1, s1 = stage1(P, reserve, amax=4.5, kick=kick)
        sol, pl, ok = solve_stage2(t1, s1, P, cache["g"], leftover_dv=leftover_dv, h_target=h_target)
        if ok:
            cache["g"] = tuple(sol)
        return pl
    return brentq(g, lo, hi, xtol=30)


def best_payload(reserve=0.0, leftover_dv=0.0, h_target=200e3, kicks=(3.6, 4.0, 4.5, 5.0)):
    """Maximise payload over the pitch-kick angle (a one-parameter first-stage trajectory optimisation)."""
    res = []
    for k in kicks:
        try:
            res.append((max_payload(reserve, leftover_dv, h_target, kick=k), k))
        except Exception:
            pass
    return max(res)


# ----------------------------------------------------------------------------------------------------------
# Booster return (after MECO): boostback, coast, entry burn, landing burn
# ----------------------------------------------------------------------------------------------------------
ENG_VAC, ENG_SL, ISP_SL = S1["Fvac"] / 9, S1["Fsl"] / 9, 283.0
MDOT_ENG = ENG_VAC / (S1["Ivac"] * G0)
OM_EFF = OMEGA * math.cos(math.radians(LAT))
V_ENTRY = 1_300.0      # entry burn ends at this Earth-relative speed
H_ENTRY = 65e3         # entry burn starts below this altitude (descending)
CD_BOOST = 2.0         # booster falls engines-first with grid fins: drag coefficient scale vs nose-first table


def downrange(s, t):
    return RE * (s[1] - OM_EFF * t)


def booster_return(t0, s0, reserve, mode="asds", x_aim=0.0, record=None, dt=0.5):
    """Simulate the first stage after MECO. Returns dict with propellant used per burn and landing point."""
    s = s0.copy()
    s[4] = S1["dry"] + reserve
    t = t0
    used = {"boostback": 0.0, "entry": 0.0, "landing": 0.0}
    dv = {"boostback": 0.0, "entry": 0.0, "landing": 0.0}
    phase = "coast0"
    t_flip = t0 + 10.0

    def make_f(n_eng, direction):
        F = (lambda tt, p, ss: n_eng * (ENG_VAC - (ENG_VAC - ENG_SL) * p / 101325.0)) if n_eng else None
        md = (lambda tt, p, ss: n_eng * MDOT_ENG) if n_eng else None
        return lambda tt, ss: _deriv(tt, ss, F, md, direction, AREF, CD_BOOST)

    def retro(tt, ss, vrel):
        v = math.hypot(*vrel)
        return -vrel[0] / v, -vrel[1] / v

    def back(tt, ss, vrel):          # boostback: thrust back towards the launch site, 15 deg above horizontal
        a = math.radians(15)
        return math.sin(a), -math.cos(a)

    coast = make_f(0, None)
    bb = make_f(3, back)
    eb = make_f(3, retro)
    while True:
        r, th, vr, vt, m = s
        h = r - RE
        x = downrange(s, t)
        u = vt - OM_EFF * r                     # Earth-relative horizontal speed
        if record is not None:
            record.append((t, x, h, phase))
        if phase == "coast0" and t >= t_flip:
            phase = "boostback" if mode == "rtls" else "coast1"
        if phase == "boostback":
            gl = MU / r ** 2
            tf = (vr + math.sqrt(max(vr * vr + 2 * gl * h, 0))) / gl
            if x + u * tf <= x_aim:
                phase = "coast1"
        if phase == "coast1" and vr < 0 and h < H_ENTRY and math.hypot(vr, u) > V_ENTRY:
            phase = "entry"
        if phase == "entry" and math.hypot(vr, u) <= V_ENTRY:
            phase = "coast2"
        if phase in ("coast1", "coast2") and vr < 0 and h < 15e3:
            # landing burn: single engine near sea level, constant thrust ~ 75 % (stop at ground)
            v = math.hypot(vr, u)
            dt_l = 0.05
            while True:
                _, rho, a = atmos(h)
                if h <= 0 or v <= 0:
                    break
                acc_t = 0.75 * ENG_SL / m
                D = 0.5 * rho * v * v * AREF * cd_body(v / a) * CD_BOOST
                # stopping distance under thrust + drag - gravity
                dec = acc_t + D / m - G0
                if v * v / (2 * dec) >= h * 0.98:
                    break
                h -= v * dt_l
                v += (G0 - D / m) * dt_l
                if record is not None:
                    record.append((t, x, h, "coast2"))
                t += dt_l
            # burn from (h, v) to rest; integrate
            mdot = 0.75 * ENG_SL / (ISP_SL * G0)
            m_l = m
            dvl = 0.0
            while v > 0 and h > -50:
                _, rho, a = atmos(max(h, 0))
                D = 0.5 * rho * v * v * AREF * cd_body(v / a) * CD_BOOST
                acc_t = 0.75 * ENG_SL / m_l
                v -= (acc_t + D / m_l - G0) * dt_l
                h -= max(v, 0) * dt_l
                m_l -= mdot * dt_l
                dvl += acc_t * dt_l
                if record is not None:
                    record.append((t, x, max(h, 0), "landing"))
                t += dt_l
            used["landing"] = m - m_l
            dv["landing"] = dvl
            s[4] = m_l
            break
        f = {"coast0": coast, "coast1": coast, "coast2": coast, "boostback": bb, "entry": eb}[phase]
        step = dt if phase.startswith("coast") else 0.1
        s_new = rk4(f, t, s, step)
        if phase in ("boostback", "entry"):
            dm = s[4] - s_new[4]
            used[phase] += dm
            dv[phase] += S1["Ivac"] * G0 * math.log(s[4] / s_new[4])
        s = s_new
        t += step
        if s[4] < S1["dry"]:
            used["fail"] = True
            break
    return dict(used=used, dv=dv, x_land=downrange(s, t), t_land=t, total=sum(used.values()))


# ----------------------------------------------------------------------------------------------------------
# Cached model results shared by several figures
# ----------------------------------------------------------------------------------------------------------
KICK = 4.5
DV_GTO = 2_455.0   # 200 km circular parking orbit (28.5 deg) -> 200 x 35 786 km GTO perigee burn


# Results of the (slow) trajectory optimisation, regenerated with `python3 ch34.py --recompute`.
CACHE = {
    "exp_leo": {"R": 0.0, "P": 23195.2, "kick": 4.626, "x_aim": 0.0},
    "exp_gto": {"R": 0.0, "P": 8418.3, "kick": 6.488, "x_aim": 0.0},
    "asds_leo": {"R": 21957.1, "P": 19098.2, "kick": 4.849, "x_aim": 0.0},
    "asds_gto": {"R": 24725.9, "P": 6196.7, "kick": 6.469, "x_aim": 0.0},
    "rtls_leo": {"R": 45402.9, "P": 15622.9, "kick": 4.963, "x_aim": 3042.8},
    "rtls_gto": {"R": 49436.2, "P": 4525.0, "kick": 6.333, "x_aim": 4134.1},
}
if "--recompute" in sys.argv:
    CACHE = {}


def _reserve(mode, P, kick, R, x_aim, leftover_dv):
    for _ in range(4):
        t1, s1 = stage1(P, R, amax=4.5, kick=kick)
        out = booster_return(t1, s1, R, mode, x_aim=x_aim)
        if mode == "rtls":
            x_aim -= out["x_land"]
        R = out["total"] + 1_500.0          # + unusable residuals / landing margin
    return R, x_aim, out


def _optimise(mode, leftover_dv):
    from scipy.optimize import minimize_scalar
    kick = 4.5 if leftover_dv == 0 else 6.5
    R = 0.0 if mode == "exp" else (22e3 if mode == "asds" else 45e3)
    P = 15e3 if leftover_dv == 0 else 5e3
    x_aim = 0.0
    for _ in range(2):
        if mode != "exp":
            R, x_aim, _ = _reserve(mode, P, kick, R, x_aim, leftover_dv)
        res = minimize_scalar(lambda k: -max_payload(R, leftover_dv, kick=k), bounds=(kick - 1.5, kick + 1.5),
                              method="bounded", options=dict(xatol=0.05))
        kick, P = float(res.x), float(-res.fun)
    if mode != "exp":
        R, x_aim, _ = _reserve(mode, P, kick, R, x_aim, leftover_dv)
        P = max_payload(R, leftover_dv, kick=kick)
    return dict(R=round(R, 1), P=round(P, 1), kick=round(kick, 3), x_aim=round(x_aim, 1))


def recovery_case(mode, leftover_dv=0.0):
    """Self-consistent stage-1 propellant reserve, pitch kick and maximum payload for one recovery mode."""
    key = "%s_%s" % (mode, "gto" if leftover_dv else "leo")
    if key not in CACHE:
        CACHE[key] = _optimise(mode, leftover_dv)
    return CACHE[key]


@lru_cache(maxsize=None)
def ascent_record(mode="asds"):
    c = recovery_case(mode)
    rec = []
    t1, s1 = stage1(c["P"], c["R"], amax=4.5, kick=c["kick"], record=rec)
    sol, pl, ok = solve_stage2(t1, s1, c["P"])
    t2, s2, pl, t_fair, t_ign = stage2(t1, s1, c["P"], sol[0], sol[1], record=rec)
    return rec, dict(t_meco=t1, s_meco=s1, t_seco=t2, s_seco=s2, t_fair=t_fair, t_ign=t_ign, P=c["P"], R=c["R"])


def losses(rec):
    """Integrate gravity, drag, steering and back-pressure losses along a recorded ascent."""
    out = dict(gravity=0.0, drag=0.0, steering=0.0, pressure=0.0, ideal=0.0)
    for a, b in zip(rec[:-1], rec[1:]):
        dt = b["t"] - a["t"]
        r, th, vr, vt, m = a["s"]
        v = math.hypot(vr, vt)
        sing = vr / v
        out["gravity"] += MU / r ** 2 * sing * dt
        out["drag"] += a["D"] / m * dt
        if a["T"] > 0:
            cosal = (a["ur"] * vr + a["ut"] * vt) / v
            out["steering"] += a["T"] / m * (1 - cosal) * dt
            out["pressure"] += (a["Tvac"] - a["T"]) / m * dt
            out["ideal"] += a["Tvac"] / m * dt
    return out


# ----------------------------------------------------------------------------------------------------------
# Figure 1: ascent simulation
# ----------------------------------------------------------------------------------------------------------
def ascent():
    rec, ev = ascent_record("asds")
    t = np.array([e["t"] for e in rec])
    S = np.array([e["s"] for e in rec])
    h = (S[:, 0] - RE) / 1e3
    x = RE * (S[:, 1] - OM_EFF * t) / 1e3
    vin = np.hypot(S[:, 2], S[:, 3]) / 1e3
    vrel = np.hypot(S[:, 2], S[:, 3] - OM_EFF * S[:, 0]) / 1e3
    q = np.array([e["q"] for e in rec]) / 1e3
    acc = np.array([(e["T"] - e["D"]) / e["s"][4] / G0 for e in rec])
    thr = np.array([e["thr"] for e in rec])
    imq = int(np.argmax(q))
    events = [(t[imq], "max-Q"), (ev["t_meco"], "MECO"), (ev["t_ign"], "SES"), (ev["t_fair"], "fairing"),
              (ev["t_seco"], "SECO")]

    fig, axs = plt.subplots(2, 2, figsize=(7.0, 5.0))
    ax = axs[0, 0]
    ax.plot(t, h, color=NAVY)
    ax.set_ylabel("Altitude (km)")
    ax2 = ax.twinx()
    ax2.plot(t, x, color=ORANGE, ls="--", lw=1.3)
    ax2.set_ylabel("Downrange (km)", color=ORANGE)
    ax2.tick_params(axis="y", colors=ORANGE)
    ax2.spines["right"].set_visible(True)
    ax2.grid(False)
    ax.set_title("Altitude and downrange distance", fontsize=8.6)
    ax.text(0.03, 0.93, "altitude", transform=ax.transAxes, color=NAVY, fontsize=7.2, va="top")
    ax.text(0.40, 0.30, "downrange", transform=ax.transAxes, color=ORANGE, fontsize=7.2)

    ax = axs[0, 1]
    ax.plot(t, vin, color=NAVY, label="inertial")
    ax.plot(t, vrel, color=SKY, ls="--", label="relative to air")
    ax.axhline(7.784, color=GREY, lw=0.8, ls=":")
    ax.text(10, 7.92, "circular speed at 200 km: 7.78 km/s", fontsize=6.6, color=GREY, va="bottom")
    ax.set_ylabel("Speed (km/s)")
    ax.set_ylim(0, 8.6)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), fontsize=7)
    ax.set_title("Speed", fontsize=8.6)

    ax = axs[1, 0]
    m = t < 185
    ax.plot(t[m], q[m], color=RED)
    ax.set_ylabel("Dynamic pressure (kPa)", color=RED)
    ax.set_xlim(0, 185)
    ax.annotate("max-Q %.0f kPa\nat T+%.0f s" % (q[imq], t[imq]), (t[imq], q[imq]), xytext=(t[imq] + 40, q[imq] * 0.88),
                fontsize=6.8, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax3 = ax.twinx()
    m1 = t <= ev["t_meco"] + 0.01
    ax3.plot(t[m1], thr[m1] * 100, color=GREEN, lw=1.2)
    ax3.set_ylabel("Stage 1 throttle (%)", color=GREEN)
    ax3.set_ylim(0, 110)
    ax3.tick_params(axis="y", colors=GREEN)
    ax3.spines["right"].set_visible(True)
    ax3.grid(False)
    ax.set_title("Dynamic pressure and throttle bucket", fontsize=8.6)
    ax.set_xlabel("Time after lift-off (s)")

    ax = axs[1, 1]
    ax.plot(t, acc, color=VIOLET)
    ax.set_ylabel("Sensed axial acceleration (g)")
    ax.set_ylim(-0.3, 5.2)
    ax.set_title("Acceleration felt by the payload", fontsize=8.6)
    ax.set_xlabel("Time after lift-off (s)")
    for a in (axs[0, 0], axs[0, 1], axs[1, 1]):
        a.set_xlim(0, t[-1] + 10)
    for a in axs.flat:
        lo, hi = a.get_xlim()
        for te, name in events:
            if lo <= te <= hi:
                a.axvline(te, color=GREY, lw=0.6, ls=":", zorder=0)
    ytop = 5.05
    for te, name in events:
        if name != "SES":
            axs[1, 1].text(te + 4 if name != "SECO" else te - 4, ytop, name if name != "MECO" else "MECO / SES",
                           fontsize=6.0, color=GREY, rotation=90, va="top", ha="left" if name != "SECO" else "right")
    fig.text(0.99, 0.005, "Planar simulation, Falcon 9-class vehicle (stage 1: 25.6 t dry, 395.7 t propellant, 7.6–8.2 MN, Isp 283–312 s; "
             "stage 2: 3.9 t dry, 92.7 t, 981 kN, 348 s; fairing 1.9 t),\n"
             "%.1f t payload to a 200 km circular orbit from 28.5° N with %.0f t of first-stage propellant kept for a droneship landing; "
             "US 1976 atmosphere, rotating Earth, 4.5 g limit." % (ev["P"] / 1e3, ev["R"] / 1e3),
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch34_ascent")


# ----------------------------------------------------------------------------------------------------------
# Figure 2: delta-v budget and launch-site effects
# ----------------------------------------------------------------------------------------------------------
def dvbudget():
    rec, ev = ascent_record("asds")
    L = losses(rec)
    v_orb = math.hypot(ev["s_seco"][2], ev["s_seco"][3])
    v0 = OM_EFF * RE
    items = [("Orbital\nspeed", v_orb, NAVY), ("Earth\nrotation", -v0, GREEN),
             ("Gravity", L["gravity"], ORANGE), ("Drag", L["drag"], RED),
             ("Steering", L["steering"], GOLD), ("Back-\npressure", L["pressure"], VIOLET)]
    total = sum(v for _, v, _ in items)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.2, 1]))
    cum = 0.0
    for i, (name, v, c) in enumerate(items):
        lo = cum if v >= 0 else cum + v
        ax.bar(i, max(abs(v), 15) / 1e3, bottom=lo / 1e3, color=c, width=0.72)
        if i == 0:
            ax.text(i, v / 1e3 + 0.1, "%.2f" % (v / 1e3), ha="center", va="bottom", fontsize=6.8)
        elif v < 0:
            ax.text(i, (cum + v) / 1e3 - 0.1, "%+.2f" % (v / 1e3), ha="center", va="top", fontsize=6.8)
        else:
            ax.text(i, (cum + v) / 1e3 + 0.1, "%+.2f" % (v / 1e3), ha="center", va="bottom", fontsize=6.8)
        cum += v
    ax.bar(len(items), total / 1e3, color=SKY, width=0.72)
    ax.text(len(items), total / 1e3 + 0.1, "%.2f" % (total / 1e3), ha="center", va="bottom", fontsize=7, weight="bold")
    ax.set_xticks(range(len(items) + 1))
    ax.set_xticklabels([n for n, _, _ in items] + ["Ideal Δv\nneeded"], fontsize=6.6)
    ax.text(3.5, 4.2, "losses", ha="center", fontsize=7, color=GREY)
    ax.annotate("", xy=(2.0, 3.9), xytext=(5.0, 3.9), arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_ylabel("Δv (km/s)")
    ax.set_ylim(0, 10.2)
    ax.set_title("Δv budget of the simulated ascent", fontsize=8.6)
    ax.grid(axis="x", visible=False)

    lat = np.linspace(0, 66, 200)
    rot = OMEGA * RE * np.cos(np.radians(lat))
    rp, ra = RE + 200e3, 42_164e3
    a = (rp + ra) / 2
    va = math.sqrt(MU * (2 / ra - 1 / a))
    vg = math.sqrt(MU / ra)
    dvg = np.sqrt(va ** 2 + vg ** 2 - 2 * va * vg * np.cos(np.radians(lat)))
    bx.plot(lat, dvg / 1e3, color=NAVY)
    bx.set_ylabel("GTO → GEO Δv at apogee (km/s)", color=NAVY)
    bx.set_xlabel("Launch-site latitude (°)")
    bx.set_ylim(1.35, 2.9)
    bx.set_xlim(0, 66)
    b2 = bx.twinx()
    b2.plot(lat, rot, color=GREEN, ls="--")
    b2.set_ylabel("Earth's eastward surface speed (m/s)", color=GREEN)
    b2.set_ylim(-300, 480)
    b2.set_yticks([200, 300, 400])
    b2.tick_params(axis="y", colors=GREEN)
    bx.tick_params(axis="y", colors=NAVY)
    b2.spines["right"].set_visible(True)
    b2.grid(False)
    sites = [("Kourou", 5.2, (1.5, -0.04)), ("Sriharikota", 13.7, (1.5, -0.04)), ("Wenchang", 19.6, (1.5, -0.04)),
             ("Cape Canaveral", 28.5, (1.5, -0.04)), ("Jiuquan", 41.0, (1.5, -0.04)), ("Baikonur", 45.9, (1.5, -0.04)),
             ("Vostochny", 51.9, (1.5, -0.10)), ("Plesetsk", 62.9, (-1.5, 0.03))]
    for nm, la, (dx, dy) in sites:
        y = float(np.interp(la, lat, dvg)) / 1e3
        bx.plot(la, y, "o", color=NAVY, ms=3.2, zorder=4)
        bx.text(la + dx, y + dy, nm, fontsize=6.0, va="top" if dy < 0 else "bottom", ha="left" if dx > 0 else "right")
    bx.text(47, 1.6, "GTO → GEO Δv", color=NAVY, fontsize=6.8)
    bx.text(3, 2.68, "eastward surface speed", color=GREEN, fontsize=6.8)
    bx.set_title("Why launch latitude matters", fontsize=8.6)
    fig.text(0.99, 0.005, "Left: losses integrated along the simulated ascent of the 4-panel ascent figure (ideal Δv = Σ vₑ ln(m₀/m_f), "
             "vacuum Isp).\nRight: GTO perigee 200 km, inclination = site latitude; the apogee burn circularises and removes the "
             "inclination. Surface speed = 465 m/s × cos(latitude).", ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch34_dvbudget")
    return L, total


# ----------------------------------------------------------------------------------------------------------
# Figure 3: staging theory
# ----------------------------------------------------------------------------------------------------------
def payload_fraction(dv, n, eps, ve):
    """Overall payload fraction of n identical stages (equal Isp and structural ratio: optimal split)."""
    x = np.exp(-dv / (n * ve))
    pi = (x - eps) / (1 - eps)
    return np.where(pi > 0, pi ** n, np.nan)


def staging():
    ve = 330 * G0
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.1))
    N = np.arange(1, 7)
    for eps, c in zip((0.06, 0.08, 0.10, 0.12), (GREEN, BLUE, ORANGE, RED)):
        pf = [float(payload_fraction(9_300.0, n, eps, ve)) * 100 for n in N]
        ax.plot(N, pf, "o-", color=c, ms=3.5, label="ε = %.2f" % eps)
    ax.set_xlabel("Number of stages")
    ax.set_ylabel("Payload / lift-off mass (%)")
    ax.set_title("Payload fraction for Δv = 9.3 km/s", fontsize=8.6)
    ax.legend(title="structural ratio", title_fontsize=7, fontsize=7, loc="lower right")
    ax.set_ylim(0, 4.8)
    ax.set_xlim(0.6, 6.4)
    ax.annotate("one stage:\nno payload", xy=(1, 0.05), xytext=(1.25, 0.9), fontsize=6.6, color=GREY,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))

    dv = np.linspace(2_000, 14_000, 400)
    for n, c in zip((1, 2, 3), (RED, BLUE, GREEN)):
        ax_ = payload_fraction(dv, n, 0.08, ve) * 100
        bx.semilogy(dv / 1e3, ax_, color=c, label="%d stage%s" % (n, "s" if n > 1 else ""))
    bx.axvline(9.3, color=GREY, ls=":", lw=0.9)
    bx.text(9.4, 40, "LEO", fontsize=7, color=GREY)
    bx.axvline(12.4, color=GREY, ls=":", lw=0.9)
    bx.text(12.5, 40, "escape", fontsize=7, color=GREY)
    bx.set_ylim(0.1, 100)
    bx.set_xlim(2, 14)
    bx.set_xlabel("Ideal Δv (km/s)")
    bx.set_ylabel("Payload / lift-off mass (%)")
    bx.set_title("Why staging pays off (ε = 0.08)", fontsize=8.6)
    bx.legend(fontsize=7, loc="lower left")
    fig.text(0.99, 0.005, "Tsiolkovsky equation for identical stages (Isp = 330 s for every stage; structural ratio ε = "
             "structure /(structure + propellant)); equal Δv split, which is optimal for identical stages.",
             ha="right", va="bottom", fontsize=5.9, color=GREY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "ch34_staging")


# ----------------------------------------------------------------------------------------------------------
# Figure 4: payload versus orbit (calibrated rocket-equation model)
# ----------------------------------------------------------------------------------------------------------
def dv_capability(P, R=0.0, f_fair=0.12):
    ve1, ve2 = S1["Ivac"] * G0, S2["Ivac"] * G0
    m2 = S2["dry"] + S2["prop"] + FAIRING + P
    m0 = S1["dry"] + S1["prop"] + m2
    dv1 = ve1 * math.log(m0 / (m0 - (S1["prop"] - R)))
    ma = m2
    mb = ma - f_fair * S2["prop"]
    mf = S2["dry"] + S2["resid"] + P
    dv2 = ve2 * (math.log(ma / mb) + math.log((mb - FAIRING) / mf))
    return dv1 + dv2


def payload_for(dv_req, R):
    f = lambda P: dv_capability(P, R) - dv_req  # noqa: E731
    if f(0.0) < 0:
        return 0.0
    return brentq(f, 0.0, 60_000.0)


@lru_cache(maxsize=None)
def calib():
    """LEO (200 km, 28.5 deg) ideal-delta-v requirement per mode, calibrated to the trajectory simulation."""
    out = {}
    for mode in ("exp", "asds", "rtls"):
        c = recovery_case(mode)
        out[mode] = (dv_capability(c["P"], c["R"]), c["R"], c["P"])
    return out


def dv_c3(c3):
    rp = RE + 200e3
    return math.sqrt(c3 * 1e6 + 2 * MU / rp) - math.sqrt(MU / rp)


def i_sso(h):
    a = RE + h
    J2 = 1.08263e-3
    rate = 2 * math.pi / (365.2422 * 86400)
    return math.degrees(math.acos(-rate * 2 * a ** 3.5 / (3 * J2 * RE ** 2 * math.sqrt(MU))))


def perf():
    cal = calib()
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.3))
    c3 = np.linspace(-60.6, 40, 300)
    cols = {"exp": NAVY, "asds": BLUE, "rtls": ORANGE}
    names = {"exp": "expendable", "asds": "droneship landing", "rtls": "return to launch site"}
    for mode in ("exp", "asds", "rtls"):
        dvl, R, P0 = cal[mode]
        P = [payload_for(dvl + dv_c3(c), R) / 1e3 for c in c3]
        ax.plot(c3, P, color=cols[mode], label=names[mode])
        g = recovery_case(mode, DV_GTO)
        ax.plot(-MU / ((2 * RE + 200e3 + 35_786e3) / 2) / 1e6, g["P"] / 1e3, "o", color=cols[mode], ms=4, mfc="white")
    for xx, nm, yy in ((-60.6, "LEO 200 km", 0.6), (-16.4, "GTO", 23.6), (-2.0, "Moon", 23.6), (10.0, "Mars", 23.6)):
        ax.axvline(xx, color=GREY, lw=0.6, ls=":")
        ax.text(xx + 1.0, yy, nm, fontsize=6.4, color=GREY, va="top" if yy > 5 else "bottom")
    pub = [(-60.6, 22.8, NAVY), (-60.6, 17.5, BLUE), (-16.4, 8.3, NAVY), (-16.4, 5.5, BLUE), (-16.4, 3.5, ORANGE)]
    for x_, y_, c in pub:
        ax.plot(x_, y_, marker="x", color=c, ms=5, mew=1.2, ls="none")
    ax.plot([], [], "x", color=GREY, label="published Falcon 9")
    ax.plot([], [], "o", color=GREY, mfc="white", label="full simulation (GTO)")
    ax.set_xlabel("Characteristic energy C₃ (km²/s²)")
    ax.set_ylabel("Payload (t)")
    ax.set_ylim(0, 24)
    ax.set_xlim(-64, 40)
    ax.legend(fontsize=6.2, loc="upper right", bbox_to_anchor=(1.0, 0.86))
    ax.set_title("Payload versus orbital energy", fontsize=8.6)

    hs = np.linspace(200e3, 1_500e3, 60)
    dvl, R, P0 = cal["exp"]
    dvl_a, R_a, _ = cal["asds"]

    def hohmann(h):
        r1, r2 = RE + 200e3, RE + h
        at = (r1 + r2) / 2
        return (math.sqrt(MU * (2 / r1 - 1 / at)) - math.sqrt(MU / r1)) + (math.sqrt(MU / r2) - math.sqrt(MU * (2 / r2 - 1 / at)))

    def rotloss(i):
        return OMEGA * RE * (math.cos(math.radians(LAT)) - math.cos(math.radians(i)))

    for lab, inc, c, ls in (("28.5° (Cape, due east)", lambda h: 28.5, NAVY, "-"), ("51.6° (ISS)", lambda h: 51.6, GREEN, "-"),
                           ("sun-synchronous (≈97–100°)", i_sso, RED, "-")):
        P = [payload_for(dvl_a + hohmann(h) + rotloss(inc(h)), R_a) / 1e3 for h in hs]
        bx.plot(hs / 1e3, P, color=c, ls=ls, label=lab)
    bx.set_xlabel("Circular-orbit altitude (km)")
    bx.set_ylabel("Payload (t), droneship recovery")
    bx.set_ylim(0, 21)
    bx.set_title("Payload versus altitude and inclination", fontsize=8.6)
    bx.legend(fontsize=6.5, loc="lower left")
    fig.text(0.99, 0.005, "Rocket-equation model of the simulated vehicle; LEO requirement calibrated to the trajectory simulation "
             "(expendable %.1f t, droneship %.1f t, RTLS %.1f t to 200 km);\nhigher orbits add impulsive Δv from a 200 km parking "
             "orbit; inclination changes the Earth-rotation gain (465 m/s × cos i), no dog-legs; booster reserves held at their LEO values."
             % (cal["exp"][2] / 1e3, cal["asds"][2] / 1e3, cal["rtls"][2] / 1e3), ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch34_perf")


# ----------------------------------------------------------------------------------------------------------
# Figure 5: booster recovery trajectories and payload penalty
# ----------------------------------------------------------------------------------------------------------
PHASE_COL = {"coast0": GREY, "coast1": GREY, "coast2": GREY, "boostback": ORANGE, "entry": RED, "landing": GREEN}


def recovery():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.4), gridspec_kw=dict(width_ratios=[1.55, 1]))
    for mode, ls in (("asds", "-"), ("rtls", "-")):
        c = recovery_case(mode)
        rec = []
        t1, s1 = stage1(c["P"], c["R"], amax=4.5, kick=c["kick"], record=rec)
        tt = np.array([e["t"] for e in rec])
        SS = np.array([e["s"] for e in rec])
        ax.plot(RE * (SS[:, 1] - OM_EFF * tt) / 1e3, (SS[:, 0] - RE) / 1e3, color=NAVY if mode == "asds" else SKY,
                lw=1.4, ls="-" if mode == "asds" else "--")
        br = []
        booster_return(t1, s1, c["R"], mode, x_aim=c["x_aim"], record=br)
        xs = np.array([b[1] for b in br]) / 1e3
        hs = np.array([b[2] for b in br]) / 1e3
        ph = [b[3] for b in br]
        start = 0
        for k in range(1, len(br) + 1):
            if k == len(br) or ph[k] != ph[start]:
                col = PHASE_COL[ph[start]]
                ax.plot(xs[start:k + 1], hs[start:k + 1], color=col, lw=2.4 if col != GREY else 1.0,
                        ls="-" if col != GREY else (":" if mode == "rtls" else "-"))
                start = k
        if mode == "asds":
            ax.plot(xs[-1], 0, marker="s", color=NAVY, ms=5)
            ax.text(xs[-1] - 12, 8, "droneship\n%.0f km" % xs[-1], ha="right", fontsize=6.4)
        else:
            ax.plot(0, 0, marker="^", color=NAVY, ms=6)
            ax.text(22, 6, "landing zone", ha="left", fontsize=6.4)
        # MECO marker
        xm = RE * (s1[1] - OM_EFF * t1) / 1e3
        hm = (s1[0] - RE) / 1e3
        ax.plot(xm, hm, "o", color=NAVY, ms=3.5)
        ax.annotate("MECO (%s)" % ("droneship" if mode == "asds" else "RTLS"), xy=(xm, hm),
                    xytext=(150, 50 if mode == "asds" else 34), fontsize=6.2, va="center",
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    rec2, ev2 = ascent_record("asds")
    t2 = np.array([e["t"] for e in rec2])
    S2_ = np.array([e["s"] for e in rec2])
    x2 = RE * (S2_[:, 1] - OM_EFF * t2) / 1e3
    h2 = (S2_[:, 0] - RE) / 1e3
    m2 = (t2 >= ev2["t_meco"]) & (x2 < 800)
    ax.plot(x2[m2], h2[m2], color=NAVY, lw=1.0, ls=(0, (4, 2)))
    ax.text(430, 197, "second stage to orbit", fontsize=6.4, color=NAVY, ha="center")
    for nm, col, y in (("boostback burn", ORANGE, 0.68), ("entry burn", RED, 0.62), ("landing burn", GREEN, 0.56)):
        ax.text(0.99, y, nm, color=col, transform=ax.transAxes, ha="right", fontsize=6.8, weight="bold")
    ax.set_xlabel("Downrange distance (km)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("Booster return trajectories", fontsize=8.6)
    ax.set_xlim(-40, 800)
    ax.set_ylim(0, 215)

    modes = ("exp", "asds", "rtls")
    leo = [recovery_case(m)["P"] / 1e3 for m in modes]
    gto = [recovery_case(m, DV_GTO)["P"] / 1e3 for m in modes]
    res = [recovery_case(m)["R"] / 1e3 for m in modes]
    x = np.arange(3)
    bx.bar(x - 0.2, leo, 0.38, color=NAVY, label="LEO 200 km")
    bx.bar(x + 0.2, gto, 0.38, color=ORANGE, label="GTO")
    for i in range(3):
        bx.text(i - 0.2, leo[i] + 0.3, "%.1f" % leo[i], ha="center", fontsize=6.6)
        bx.text(i + 0.2, gto[i] + 0.3, "%.1f" % gto[i], ha="center", fontsize=6.6)
        if i:
            bx.text(i - 0.2, leo[i] / 2, "−%.0f%%" % (100 * (1 - leo[i] / leo[0])), ha="center", fontsize=6.0,
                    color="white", rotation=90, va="center")
            bx.text(i + 0.2, gto[i] / 2, "−%.0f%%" % (100 * (1 - gto[i] / gto[0])), ha="center", fontsize=6.0,
                    color="white", rotation=90, va="center")
    bx.set_xticks(x)
    bx.set_xticklabels(["expendable", "droneship\n(%.0f t kept)" % res[1], "RTLS\n(%.0f t kept)" % res[2]], fontsize=6.8)
    bx.set_ylabel("Payload (t)")
    bx.set_ylim(0, 26)
    bx.legend(fontsize=6.8, loc="upper right")
    bx.set_title("Payload cost of recovery", fontsize=8.6)
    bx.grid(axis="x", visible=False)
    fig.text(0.99, 0.005, "Same model as the ascent figure. Booster: 25.6 t dry, 3 engines for boostback (15° above horizontal) and "
             "entry burns (below 65 km, to 1.3 km/s), one engine at 75 % for landing;\nkept propellant = burns + 1.5 t "
             "residuals, iterated to consistency; payload re-optimised for each case. GTO = 200 × 35 786 km.",
             ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "ch34_recovery")


# ----------------------------------------------------------------------------------------------------------
# Figure 6: payload environments (Falcon User's Guide, May 2025) and GEVS
# ----------------------------------------------------------------------------------------------------------
QSL = {  # axial, lateral polygon vertices (g)
    "> 1 800 kg": [(6.0, 0.5), (4.0, 0.5), (3.5, 2.0), (-1.5, 2.0), (-1.5, 0.5), (-2.0, 0.5), (-2.0, -0.5), (-1.5, -0.5),
                   (-1.5, -2.0), (3.5, -2.0), (4.0, -0.5), (6.0, -0.5)],
    "1 000–1 800 kg": [(8.5, 2.0), (4.0, 2.0), (4.0, 3.0), (-1.5, 3.0), (-1.5, 2.0), (-4.0, 2.0), (-4.0, -2.0), (-1.5, -2.0),
                       (-1.5, -3.0), (4.0, -3.0), (4.0, -2.0), (8.5, -2.0)],
    "< 1 000 kg": [(11.0, 4.0), (5.0, 4.0), (5.0, 7.5), (-2.0, 7.5), (-2.0, 4.0), (-6.0, 4.0), (-6.0, -4.0), (-2.0, -4.0),
                   (-2.0, -7.5), (5.0, -7.5), (5.0, -4.0), (11.0, -4.0)],
}
F3 = [31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000,
      5000, 6300, 8000, 10000]
SPL_BLK = [118.0, 119.5, 120.0, 120.0, 119.8, 120.5, 121.5, 122.0, 121.5, 120.5, 119.0, 117.0, 115.0, 113.0, 111.0, 109.5,
           108.0, 107.0, 106.0, 105.0, 104.0, 103.0, 102.0, 101.0, 100.0, 99.0]
SPL_NOB = [118.0, 119.5, 120.0, 120.0, 121.0, 123.3, 127.7, 129.3, 129.8, 129.5, 128.0, 126.0, 124.0, 122.0, 119.5, 117.8,
           116.4, 114.5, 113.0, 111.3, 110.2, 109.0, 107.5, 106.0, 104.0, 102.0]


def oaspl(levels):
    return 10 * math.log10(sum(10 ** (L / 10) for L in levels))


def psd_grms(f, a):
    """grms of a piecewise log-log PSD."""
    tot = 0.0
    for (f1, a1), (f2, a2) in zip(zip(f[:-1], a[:-1]), zip(f[1:], a[1:])):
        n = math.log(a2 / a1) / math.log(f2 / f1)
        if abs(n + 1) < 1e-9:
            tot += a1 * f1 * math.log(f2 / f1)
        else:
            tot += a1 * f1 / (n + 1) * ((f2 / f1) ** (n + 1) - 1)
    return math.sqrt(tot)


def environment():
    fig, axs = plt.subplots(2, 2, figsize=(7.0, 5.2))
    ax = axs[0, 0]
    for (nm, poly), c in zip(QSL.items(), (NAVY, BLUE, SKY)):
        P = np.array(poly + [poly[0]])
        ax.fill(P[:, 1], P[:, 0], color=c, alpha=0.12)
        ax.plot(P[:, 1], P[:, 0], color=c, lw=1.3, label=nm)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.set_xlabel("Lateral load factor (g)")
    ax.set_ylabel("Axial load factor (g)\n(+ = compression)")
    ax.set_title("Quasi-static limit loads", fontsize=8.6)
    ax.legend(fontsize=6.4, loc="upper left", title="payload mass", title_fontsize=6.4)
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-7, 12)

    ax = axs[0, 1]
    ax.semilogx(F3, SPL_NOB, color=RED, marker="o", ms=2.2, label="no blankets (OASPL %.1f dB)" % oaspl(SPL_NOB))
    ax.semilogx(F3, SPL_BLK, color=GREEN, marker="o", ms=2.2, label="with blankets (OASPL %.1f dB)" % oaspl(SPL_BLK))
    ax.set_xlabel("One-third-octave band centre frequency (Hz)")
    ax.set_ylabel("Sound pressure level (dB re 20 µPa)")
    ax.set_title("Acoustics inside the fairing", fontsize=8.6)
    ax.legend(fontsize=6.4, loc="lower left")
    ax.set_ylim(95, 135)

    ax = axs[1, 0]
    fF = [20, 100, 300, 700, 800, 925, 2000]
    aF = [0.0044, 0.0044, 0.01, 0.01, 0.03, 0.03, 0.00644]
    fG = [20, 50, 800, 2000]
    aG = [0.026, 0.16, 0.16, 0.026]
    ax.loglog(fF, aF, color=NAVY, label="Falcon MPE at adapter (%.1f grms)" % psd_grms(fF, aF))
    ax.loglog(fG, aG, color=ORANGE, label="GEVS component qual. (%.1f grms)" % psd_grms(fG, aG))
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Acceleration PSD (g²/Hz)")
    ax.set_title("Random vibration", fontsize=8.6)
    ax.legend(fontsize=6.4, loc="lower center")
    ax.set_ylim(1e-3, 0.5)
    ax.set_xlim(15, 2500)

    ax = axs[1, 1]
    ax.loglog([100, 500, 10000], [30, 300, 300], color=NAVY, label="fairing separation (at payload interface)")
    ax.loglog([100, 1000, 10000], [30, 1000, 1000], color=RED, label="clamp-band release (spacecraft separation)")
    ax.set_xlabel("Natural frequency (Hz)")
    ax.set_ylabel("Shock response (g)")
    ax.set_title("Pyroshock response spectra", fontsize=8.6)
    ax.legend(fontsize=6.4, loc="lower right")
    ax.set_ylim(10, 3000)
    fig.text(0.99, 0.005, "Data: SpaceX Falcon User's Guide (May 2025) — limit loads, P95/50 acoustic MPE for the standard fairing "
             "(Eastern Range, 60 % fill), random-vibration MPE at the top of the payload adapter, shock\nresponse spectra; "
             "GEVS = NASA GSFC-STD-7000B generalised qualification level for components up to 22.7 kg. Qualification adds 25 % "
             "(loads) or 3 dB (acoustics, vibration).", ha="right", va="bottom", fontsize=5.8, color=GREY)
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, "ch34_environment")


# ----------------------------------------------------------------------------------------------------------
# Figure 7: launch reliability (GCAT)
# ----------------------------------------------------------------------------------------------------------
# Failures by flight number within each vehicle family, from GCAT launch.tsv (13 Oct 2026); families grouped as in
# tools/gcat_stats.py with Long March split by number. (bin label, attempts, failures)
LEARN_OLD = [("1", 43, 17), ("2", 40, 16), ("3", 35, 14), ("4–5", 62, 18), ("6–10", 122, 33), ("11–20", 182, 39),
             ("21–50", 478, 44), (">50", 4317, 186)]
LEARN_NEW = [("1", 100, 38), ("2", 75, 17), ("3", 66, 10), ("4–5", 108, 12), ("6–10", 202, 26), ("11–20", 252, 16),
             ("21–50", 357, 14), (">50", 983, 7)]


def jeffreys(k, n, conf=0.90):
    from scipy.stats import beta
    lo = beta.ppf((1 - conf) / 2, k + 0.5, n - k + 0.5) if k > 0 else 0.0
    hi = beta.ppf(1 - (1 - conf) / 2, k + 0.5, n - k + 0.5) if k < n else 1.0
    return lo, hi


def reliability():
    import json
    d = json.loads((Path(__file__).resolve().parents[2] / "data" / "gcat_stats.json").read_text())
    years = sorted(int(y) for y in d["launches_by_year"])
    att = np.array([d["launches_by_year"][str(y)]["_all"] for y in years])
    fl = np.array([d["failures_by_year"].get(str(y), 0) for y in years])
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw=dict(width_ratios=[1.2, 1]))
    yrs = np.array(years)
    ax.bar(yrs, att - fl, color=SKY, width=0.85, label="successes")
    ax.bar(yrs, fl, bottom=att - fl, color=RED, width=0.85, label="failures")
    ax.set_ylabel("Orbital launch attempts per year")
    ax.set_xlim(1956, 2027.5)
    a2 = ax.twinx()
    rate = np.where(att > 0, fl / np.maximum(att, 1) * 100, np.nan)
    # 5-year running failure rate
    k = 5
    rr = np.array([fl[max(0, i - k + 1):i + 1].sum() / att[max(0, i - k + 1):i + 1].sum() * 100 for i in range(len(yrs))])
    a2.plot(yrs, rr, color=NAVY, lw=1.4)
    a2.set_ylabel("Failure rate, 5-yr running (%)", color=NAVY)
    a2.set_ylim(0, 75)
    a2.tick_params(axis="y", colors=NAVY)
    a2.spines["right"].set_visible(True)
    a2.grid(False)
    ax.legend(fontsize=6.8, loc="upper left", bbox_to_anchor=(0.02, 0.98))
    ax.set_title("Orbital launches, 1957–2026", fontsize=8.6)
    ax.annotate("2026 to\n13 Oct", xy=(2026, att[-1]), xytext=(2011, 300), fontsize=5.8, ha="center",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))

    for data, c, off, lab in ((LEARN_OLD, GREY, -0.2, "families first flown 1957–79"),
                              (LEARN_NEW, NAVY, 0.2, "families first flown 1980–2026")):
        x = np.arange(len(data))
        p = np.array([f / n * 100 for _, n, f in data])
        ci = np.array([jeffreys(f, n) for _, n, f in data]) * 100
        bx.bar(x + off, p, 0.38, color=c, label=lab)
        bx.errorbar(x + off, p, yerr=[p - ci[:, 0], ci[:, 1] - p], fmt="none", ecolor=INK, elinewidth=0.6, capsize=1.5)
    bx.set_xticks(np.arange(len(LEARN_NEW)))
    bx.set_xticklabels([b for b, _, _ in LEARN_NEW], fontsize=6.0)
    bx.set_xlabel("Flight number within the vehicle family")
    bx.set_ylabel("Share of flights that failed (%)")
    bx.set_title("The learning curve", fontsize=8.6)
    bx.legend(fontsize=6.4, loc="upper right")
    bx.set_ylim(0, 55)
    fig.text(0.99, 0.005, "Data: GCAT (J. McDowell, launch list to 13 Oct 2026); partial failures counted as failures. Right: "
             "143 vehicle families; error bars are 90 % Jeffreys intervals.", ha="right", va="bottom", fontsize=5.9,
             color=GREY)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "ch34_reliability")


# ----------------------------------------------------------------------------------------------------------
# Figure 8: anatomy of a two-stage kerosene launch vehicle (schematic)
# ----------------------------------------------------------------------------------------------------------
def anatomy():
    fig, ax = canvas(7.0, 3.05, xlim=(0, 150), ylim=(-2, 64))
    cy, R = 31, 5.5
    STEEL, TANKF, LOXC, RPC = "#D9DEE4", "#F4F6F8", "#CFE3F5", "#F6E3C8"
    # stage 1 tanks
    ax.add_patch(Rectangle((12, cy - R), 36, 2 * R, fc=RPC, ec="#555", lw=0.8, zorder=2))      # RP-1
    ax.add_patch(Rectangle((48, cy - R), 32, 2 * R, fc=LOXC, ec="#555", lw=0.8, zorder=2))     # LOX
    # common dome between them
    th = np.linspace(-np.pi / 2, np.pi / 2, 50)
    ax.plot(48 - 3.0 * np.cos(th) * 0 + 3.2 * np.cos(th) - 3.2, cy + R * np.sin(th), color=NAVY, lw=1.4, zorder=4)
    # LOX transfer tube through RP-1 tank
    ax.add_patch(Rectangle((10, cy - 0.7), 36, 1.4, fc=LOXC, ec=NAVY, lw=0.7, zorder=3))
    # stringers on RP-1 tank
    for yy in (cy - 3.5, cy - 1.8, cy + 1.8, cy + 3.5):
        ax.plot([13, 47], [yy, yy], color="#B9A27F", lw=0.5, zorder=2.5)
    # COPVs in LOX tank
    for xx, yy in ((74, cy + 2.6), (74, cy - 2.6), (77.5, cy)):
        ax.add_patch(Circle((xx, yy), 1.5, fc="#8E9AA6", ec="#444", lw=0.6, zorder=4))
    # engine section (octaweb) and engines
    ax.add_patch(Rectangle((6, cy - R), 6, 2 * R, fc=STEEL, ec="#555", lw=0.8, zorder=2))
    for yy in (cy - 3.6, cy, cy + 3.6):
        ax.add_patch(Polygon([(6, yy - 0.9), (6, yy + 0.9), (1.2, yy + 1.9), (1.2, yy - 1.9)], fc="#6E7781", ec="#333",
                             lw=0.6, zorder=3))
    # landing legs folded
    for sgn in (1, -1):
        ax.add_patch(Polygon([(7, cy + sgn * R), (27, cy + sgn * (R + 0.2)), (27, cy + sgn * (R + 1.1)),
                              (7, cy + sgn * (R + 1.2))], fc="#3F4A55", ec="#222", lw=0.5, zorder=3))
    # interstage with MVac nozzle inside
    ax.add_patch(Rectangle((80, cy - R), 13, 2 * R, fc="#3B3F45", ec="#222", lw=0.8, zorder=2))
    ax.add_patch(Polygon([(93, cy - 1.0), (93, cy + 1.0), (82, cy + 4.3), (82, cy - 4.3)], fc="#9AA3AD", ec="#DDD",
                         lw=0.6, zorder=3))
    # grid fins
    for sgn in (1, -1):
        ax.add_patch(Rectangle((88, cy + sgn * R + (0 if sgn > 0 else -1.6)), 2.4, 1.6, fc="#6E7781", ec="#222", lw=0.5,
                               zorder=3, hatch="++++"))
    # stage 2 tanks
    ax.add_patch(Rectangle((93, cy - R), 11, 2 * R, fc=RPC, ec="#555", lw=0.8, zorder=2))
    ax.add_patch(Rectangle((104, cy - R), 12, 2 * R, fc=LOXC, ec="#555", lw=0.8, zorder=2))
    ax.plot(104 + 2.2 * np.cos(th) - 2.2, cy + R * np.sin(th), color=NAVY, lw=1.4, zorder=4)
    ax.add_patch(Circle((113.5, cy + 2.6), 1.2, fc="#8E9AA6", ec="#444", lw=0.6, zorder=4))
    # avionics / adapter
    ax.add_patch(Rectangle((116, cy - R), 3, 2 * R, fc=STEEL, ec="#555", lw=0.8, zorder=2))
    ax.add_patch(Polygon([(119, cy - R), (119, cy + R), (122, cy + 3), (122, cy - 3)], fc="#B8C1CA", ec="#555", lw=0.7,
                         zorder=2))
    # fairing
    fx0, fx1, FR = 116, 147, 7.8
    xs = np.linspace(0, 1, 60)
    top = [(fx0 + 0, cy + FR)] + [(fx0 + 17 + 14 * u, cy + FR * math.sqrt(max(1 - u ** 1.6, 0))) for u in xs]
    bot = [(x, 2 * cy - y) for x, y in top[::-1]]
    ax.add_patch(Polygon([(fx0, cy - FR)] + [(fx0, cy + FR)] + top + bot, fc="white", ec=NAVY, lw=1.0, zorder=1.5,
                         alpha=1.0))
    ax.plot([fx0, fx1 - 0.2], [cy, cy], color=NAVY, lw=0.5, ls=(0, (3, 2)), zorder=1.6)
    # acoustic blankets
    inner = [(fx0 + 1, cy + FR - 0.9)] + [(fx0 + 17 + 13 * u, cy + (FR - 0.9) * math.sqrt(max(1 - u ** 1.6, 0))) for u in xs]
    ax.plot([p[0] for p in inner], [p[1] for p in inner], color=GOLD, lw=1.6, zorder=1.7)
    ax.plot([p[0] for p in inner], [2 * cy - p[1] for p in inner], color=GOLD, lw=1.6, zorder=1.7)
    # payload
    ax.add_patch(Rectangle((123, cy - 4.2), 9, 8.4, fc="#E8C766", ec="#7A6320", lw=0.7, zorder=3))
    ax.add_patch(Rectangle((125, cy + 4.2), 5, 1.4, fc="#2A4E8A", ec="#1b2d4f", lw=0.4, zorder=3))
    ax.add_patch(Rectangle((125, cy - 5.6), 5, 1.4, fc="#2A4E8A", ec="#1b2d4f", lw=0.4, zorder=3))
    # stage brackets
    for x0, x1, nm in ((1, 93, "first stage (booster)"), (93, 119, "second stage"), (116, 147, "payload fairing")):
        y = 61 if nm != "payload fairing" else 55
        ax.plot([x0, x0, x1, x1], [y - 1.2, y, y, y - 1.2], color=NAVY, lw=0.8)
        ax.text((x0 + x1) / 2, y + 0.6, nm, ha="center", va="bottom", fontsize=7.4, weight="bold", color=NAVY)
    lab = [  # (text, xy, xytext, ha)
        ("9 gimballed\nengines", (4, cy + 3.6), (0.5, 50), "left"),
        ("fuel tank (RP-1):\nskin and stringers", (30, cy + 3.5), (32, 50), "center"),
        ("common dome", (45, cy + 4.0), (49, 43.5), "center"),
        ("oxidiser tank (LOX):\nAl–Li monocoque", (63, cy + 3.5), (64, 50), "center"),
        ("grid fins", (89, cy + R + 1.4), (84, 43.5), "center"),
        ("interstage\n(composite)", (91, cy + R - 1), (95, 50), "center"),
        ("avionics, batteries,\ncold-gas thrusters", (117.5, cy + 4.5), (117, 50), "center"),
        ("acoustic\nblankets", (139, cy + 4.8), (143, 49), "center"),
        ("folded landing legs", (17, cy - R - 1.0), (14, 14), "center"),
        ("LOX feed line through fuel tank", (34, cy - 0.5), (36, 7), "center"),
        ("helium COPVs", (75, cy - 3.5), (66, 14), "center"),
        ("vacuum engine\n(fixed nozzle)", (87, cy - 2.5), (82, 7), "center"),
        ("stage-2 tanks with\ncommon dome", (104, cy - 4.0), (101, 14), "center"),
        ("payload adapter +\nseparation system", (120.5, cy - 3.5), (120, 7), "center"),
        ("payload", (128, cy - 3.0), (138, 14), "center"),
    ]
    for text, xy, xyt, ha in lab:
        ax.annotate(text, xy=xy, xytext=xyt, fontsize=6.2, ha=ha, va="center", color=INK,
                    arrowprops=dict(arrowstyle="-", color="#5B6670", lw=0.6, shrinkA=1, shrinkB=0), zorder=6)
    ax.text(149, -1.5, "Schematic of a generic two-stage kerosene vehicle, loosely based on Falcon 9 (diameter exaggerated "
            "about ×1.5; length ≈ 70 m).", ha="right", va="bottom", fontsize=5.9, color=GREY)
    save(fig, "ch34_anatomy")


if __name__ == "__main__" and "--recompute" in sys.argv:
    for m in ("exp", "asds", "rtls"):
        for lv in (0.0, DV_GTO):
            recovery_case(m, lv)
            print(m, lv, CACHE, flush=True)
    print("CACHE =", CACHE)
    sys.exit()

if __name__ == "__main__":
    fns = [ascent, dvbudget, staging, perf, recovery, environment, reliability, anatomy]
    sel = sys.argv[1:]
    for fn in fns:
        if not sel or fn.__name__ in sel:
            fn()
    print("ok")
