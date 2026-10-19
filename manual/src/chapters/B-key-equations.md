---
title: Key Equations
abstract: The essential equations of space engineering gathered in one place — orbital mechanics and manoeuvres, rocket propulsion, atmospheric flight and entry, power, thermal and attitude control, communication links, remote sensing and radar, the space environment and astronomy — each with its symbols defined and a pointer to the chapter where it is derived and used.
---

This appendix is a formula sheet. Each table gives the equation, defines its symbols briefly and names the chapter where it is explained. SI units are assumed throughout unless stated: metres, kilograms, seconds, kelvin, watts and radians. μ = *GM* is the gravitational parameter of the central body (Appendix C), *r* a distance from its centre, *g*₀ = 9.806 65 m/s², σ the Stefan–Boltzmann constant and *k* the Boltzmann constant (Appendix A).

## Orbital Mechanics

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Vis-viva (speed anywhere on an orbit) | $v^2 = \mu\left(\dfrac{2}{r} - \dfrac{1}{a}\right)$ | *a* semi-major axis; Chapter 3 |
| Circular and escape speed | $v_c = \sqrt{\mu/r}$, $\;v_{esc} = \sqrt{2\mu/r}$ | |
| Orbital period | $T = 2\pi\sqrt{a^3/\mu}$ | Kepler's third law |
| Specific orbital energy | $\varepsilon = \dfrac{v^2}{2} - \dfrac{\mu}{r} = -\dfrac{\mu}{2a}$ | negative for bound orbits |
| Specific angular momentum | $h = r v \cos\gamma = \sqrt{\mu a (1-e^2)}$ | γ flight-path angle |
| Orbit equation (conic) | $r = \dfrac{a(1-e^2)}{1 + e\cos\nu}$ | *e* eccentricity, ν true anomaly |
| Periapsis and apoapsis | $r_p = a(1-e)$, $\;r_a = a(1+e)$ | |
| Kepler's equation | $M = E - e\sin E$, $\;M = n(t - t_p)$, $\;n = \sqrt{\mu/a^3}$ | *E* eccentric anomaly, *n* mean motion |
| True from eccentric anomaly | $\tan\dfrac{\nu}{2} = \sqrt{\dfrac{1+e}{1-e}}\tan\dfrac{E}{2}$ | |
| Hohmann transfer Δ*v* | $\Delta v_1 = \sqrt{\dfrac{\mu}{r_1}}\left(\sqrt{\dfrac{2r_2}{r_1+r_2}} - 1\right)$, $\;\Delta v_2 = \sqrt{\dfrac{\mu}{r_2}}\left(1 - \sqrt{\dfrac{2r_1}{r_1+r_2}}\right)$ | circular, coplanar orbits |
| Hohmann transfer time | $t_H = \pi\sqrt{(r_1+r_2)^3/(8\mu)}$ | half the transfer-orbit period |
| Pure plane change | $\Delta v = 2v\sin(\Delta i/2)$ | cheapest at low speed (apoapsis) |
| Combined manoeuvre | $\Delta v^2 = v_1^2 + v_2^2 - 2v_1v_2\cos\Delta i$ | GTO-to-GEO insertion |
| Nodal regression (*J*₂) | $\dot\Omega = -\dfrac{3}{2}\, n J_2 \left(\dfrac{R}{p}\right)^2 \cos i$, $\;p = a(1-e^2)$ | Earth *J*₂ = 1.0826 × 10⁻³ |
| Sun-synchronous condition | $\dot\Omega = 360°/365.2422\ \mathrm{d} = 0.9856°/\mathrm{day}$ | gives *i* ≈ 97–99° in LEO |
| Apsidal precession (*J*₂) | $\dot\omega = \dfrac{3}{4}\, n J_2 \left(\dfrac{R}{p}\right)^2 (5\cos^2 i - 1)$ | zero at *i* = 63.4° (Molniya) |
| Ground-track shift per orbit | $\Delta\lambda \approx T\,(\omega_\oplus - \dot\Omega)$ | westward, in radians |
| Sphere of influence | $r_{SOI} = a_p (m_p/M_\odot)^{2/5}$ | patched conics; Chapter 24 |
| Hyperbolic excess and C3 | $v_\infty^2 = C_3 = v^2 - \dfrac{2\mu}{r}$ | departure energy |
| Δ*v* to depart from a circular orbit | $\Delta v = \sqrt{v_\infty^2 + 2\mu/r} - \sqrt{\mu/r}$ | Oberth effect: burn deep in the well |
| Gravity-assist turn angle | $\sin\dfrac{\delta}{2} = \dfrac{1}{1 + r_p v_\infty^2/\mu}$ | velocity change $2v_\infty\sin(\delta/2)$ |
| Clohessy–Wiltshire (relative motion) | $\ddot x - 3n^2x - 2n\dot y = 0$, $\;\ddot y + 2n\dot x = 0$, $\;\ddot z + n^2 z = 0$ | *x* radial, *y* along-track; Chapters 21 and 40 |
| Synodic period | $\dfrac{1}{T_{syn}} = \left|\dfrac{1}{T_1} - \dfrac{1}{T_2}\right|$ | interval between launch windows |

: Orbital mechanics. {#tbl:apxeqorbit}

## Rocket Propulsion

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Rocket equation (Tsiolkovsky) | $\Delta v = v_e \ln\dfrac{m_0}{m_f} = I_{sp}\, g_0 \ln\dfrac{m_0}{m_f}$ | *m*₀ initial, *m*~f~ final mass; Chapter 35 |
| Propellant for a given Δ*v* | $m_p = m_f\left(e^{\Delta v/v_e} - 1\right)$ | |
| Thrust | $F = \dot m v_e + (p_e - p_a)A_e$ | *p*~e~ exit, *p*~a~ ambient pressure, *A*~e~ exit area |
| Specific impulse | $I_{sp} = \dfrac{F}{\dot m g_0}$ | seconds |
| Characteristic velocity | $c^* = \dfrac{p_c A_t}{\dot m}$ | combustion efficiency; *A*~t~ throat area |
| Thrust coefficient | $C_F = \dfrac{F}{p_c A_t}$, $\;F = C_F\, p_c A_t$ | nozzle efficiency; 1.4–2.0 |
| Ideal exhaust velocity | $v_e = \sqrt{\dfrac{2\gamma}{\gamma - 1}\dfrac{R_u T_c}{\mathcal M}\left[1 - \left(\dfrac{p_e}{p_c}\right)^{(\gamma-1)/\gamma}\right]}$ | γ ratio of specific heats, $\mathcal M$ molar mass, *T*~c~ chamber temperature |
| Nozzle area ratio | $\dfrac{A_e}{A_t} = \dfrac{1}{M_e}\left[\dfrac{2}{\gamma+1}\left(1 + \dfrac{\gamma-1}{2}M_e^2\right)\right]^{\frac{\gamma+1}{2(\gamma-1)}}$ | *M*~e~ exit Mach number |
| Staged rocket Δ*v* | $\Delta v = \sum_i v_{e,i}\ln\dfrac{m_{0,i}}{m_{f,i}}$ | Chapter 34 |
| Losses in ascent | $\Delta v_{total} = \Delta v_{orbit} + \Delta v_{gravity} + \Delta v_{drag} + \Delta v_{steering}$ | ≈ 9.3–9.6 km/s to LEO |
| Electric thruster power | $P_{jet} = \dfrac{F v_e}{2} = \dfrac{\dot m v_e^2}{2}$, $\;F = \dfrac{2\eta P}{v_e}$ | η thruster efficiency; Chapters 6 and 42 |
| Burn time at constant thrust | $t_b = \dfrac{m_p v_e}{F}$ | |

: Rocket propulsion. {#tbl:apxeqprop}

## Atmospheric Flight, Drag and Entry

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Exponential atmosphere | $\rho = \rho_0\, e^{-h/H}$, $\;H = \dfrac{R_u T}{\mathcal M g}$ | *H* scale height (8.5 km on Earth); Chapter 2 |
| Dynamic pressure | $q = \tfrac{1}{2}\rho v^2$ | "max-Q" during ascent |
| Drag force | $D = \tfrac{1}{2}\rho v^2 C_D A$ | *C*~D~ ≈ 2.2 for satellites in free-molecular flow |
| Ballistic coefficient | $\beta = \dfrac{m}{C_D A}$ | kg/m²; higher β → longer orbital life |
| Decay of a circular orbit | $\dfrac{da}{dt} = -\dfrac{\sqrt{\mu a}\,\rho}{\beta}$ | per orbit Δ*a* = −2π ρ *a*²/β; Chapter 21 |
| Peak deceleration (ballistic entry, Allen–Eggers) | $a_{max} = \dfrac{v_E^2 \sin\gamma_E}{2eH}$ | *v*~E~, γ~E~ entry speed and angle; *e* = 2.718; Chapter 10 |
| Stagnation-point heat flux (Sutton–Graves) | $\dot q = k\sqrt{\rho/r_n}\, v^3$ | *k* ≈ 1.74 × 10⁻⁴ (Earth), 1.90 × 10⁻⁴ (Mars) in SI; *r*~n~ nose radius |
| Terminal velocity | $v_t = \sqrt{\dfrac{2 m g}{\rho C_D A}}$ | parachute sizing; Chapter 27 |
| Lift-to-drag ratio and cross-range | $L/D$; cross-range grows roughly with $(L/D)^2$ | capsule ≈ 0.3, Shuttle ≈ 1–4.5 |
| Mach number | $M = v/a$, $\;a = \sqrt{\gamma R_u T/\mathcal M}$ | 340 m/s at sea level |

: Atmospheric flight and entry. {#tbl:apxeqentry}

## Power, Thermal and Attitude Control

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Solar array power | $P = S\,\eta\, A \cos\theta \cdot L_d$ | *S* ≈ 1 361 W/m² at 1 au (∝ 1/*d*²); η cell efficiency; *L*~d~ degradation; Chapter 5 |
| Array sizing with eclipses | $P_{sa} = \dfrac{\dfrac{P_e T_e}{X_e} + \dfrac{P_d T_d}{X_d}}{T_d}$ | *e* eclipse, *d* daylight; *X* path efficiencies |
| Battery capacity | $C = \dfrac{P_e T_e}{\mathrm{DoD}\cdot n\cdot \eta_b}$ | DoD depth of discharge |
| Radiated power | $P = \varepsilon \sigma A T^4$ | ε emissivity |
| Equilibrium temperature of a plate | $T = \left(\dfrac{\alpha S + Q_{int}/A}{\varepsilon\sigma}\right)^{1/4}$ | α solar absorptance; one side lit, one radiating |
| Planetary equilibrium temperature | $T_{eq} = \left(\dfrac{S(1-A_B)}{4\sigma}\right)^{1/4}$ | *A*~B~ Bond albedo; Earth 255 K |
| Conduction | $Q = \dfrac{kA}{L}\Delta T$ | *k* conductivity |
| Euler's equations | $I_x\dot\omega_x + (I_z - I_y)\omega_y\omega_z = T_x$ (cyclic) | principal axes; Chapter 6 |
| Gravity-gradient torque | $T_{gg} = \dfrac{3\mu}{2r^3}\,\lvert I_z - I_y\rvert \sin 2\theta$ | θ deviation from local vertical |
| Solar radiation pressure torque | $T_{srp} = \dfrac{S}{c} A_s (1+q)\cos\phi\,(c_{ps} - c_g)$ | *q* reflectance |
| Aerodynamic torque | $T_a = \tfrac{1}{2}\rho v^2 C_D A_s (c_{pa} - c_g)$ | dominant below ≈ 500 km |
| Magnetic torque | $T_m = D B$, $\;B \approx B_0 (R/r)^3\sqrt{1 + 3\sin^2\lambda}$ | *D* residual dipole (A m²) |
| Wheel momentum to store | $H = T_d \cdot \dfrac{T_{orbit}}{4}\cdot 0.707$ | cyclic disturbance estimate |
| Slew time (bang-bang) | $t = 2\sqrt{\theta I / T}$ | θ slew angle, *T* torque |

: Power, thermal and attitude control. {#tbl:apxeqsubsys}

## Communication Links

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Free-space path loss | $L_{fs} = \left(\dfrac{4\pi d}{\lambda}\right)^2$; in dB: $92.45 + 20\log f_{GHz} + 20\log d_{km}$ | Chapter 7, Appendix D |
| Antenna gain | $G = \eta\left(\dfrac{\pi D}{\lambda}\right)^2$ | η ≈ 0.55–0.70 for dishes |
| Half-power beamwidth | $\theta_{3dB} \approx 70\,\dfrac{\lambda}{D}$ degrees | |
| Effective isotropic radiated power | $\mathrm{EIRP} = P_t G_t / L_t$ | dBW |
| Received carrier-to-noise density | $\dfrac{C}{N_0} = \mathrm{EIRP} - L_{fs} - L_a + \dfrac{G}{T} - 10\log k$ | in dB; −10 log *k* = +228.6 |
| Energy per bit to noise density | $\dfrac{E_b}{N_0} = \dfrac{C}{N_0} - 10\log R_b$ | *R*~b~ bit rate |
| Link margin | $M = \left(\dfrac{E_b}{N_0}\right)_{received} - \left(\dfrac{E_b}{N_0}\right)_{required}$ | typically ≥ 3 dB |
| System noise temperature | $T_{sys} = T_{ant} + (L - 1)T_0 + L\,T_{rx}$ | *T*₀ = 290 K |
| Shannon capacity | $C = B\log_2(1 + S/N)$ | upper limit on bit rate |
| Doppler shift | $\Delta f = f\,\dfrac{v_r}{c}$ | ± 50 kHz at 2.2 GHz from LEO |
| Slant range to a satellite | $d = \sqrt{(R+h)^2 - R^2\cos^2\varepsilon} - R\sin\varepsilon$ | ε elevation angle |

: Communication links. {#tbl:apxeqlink}

## Remote Sensing, Optics and Radar

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Planck's law | $B_\lambda(T) = \dfrac{2hc^2}{\lambda^5}\,\dfrac{1}{e^{hc/(\lambda k T)} - 1}$ | spectral radiance; Chapter 13 |
| Wien's law | $\lambda_{max} = 2898\ \mu\mathrm{m\,K}/T$ | Sun 0.50 µm, Earth 10 µm |
| Stefan–Boltzmann law | $M = \varepsilon\sigma T^4$ | |
| Diffraction limit (Rayleigh) | $\theta = 1.22\,\lambda/D$ | Chapters 14 and 38 |
| Ground sample distance | $\mathrm{GSD} = \dfrac{H\,p}{f}$ | *p* pixel pitch, *f* focal length, *H* altitude |
| Swath width (nadir) | $W \approx 2H\tan(\mathrm{FOV}/2)$ | |
| Signal-to-noise ratio of a detector | $\mathrm{SNR} = \dfrac{S}{\sqrt{S + n_{pix}(B + D t + R^2)}}$ | *S* signal electrons, *B* background, *D* dark current, *R* read noise |
| NDVI | $\mathrm{NDVI} = \dfrac{\rho_{NIR} - \rho_{red}}{\rho_{NIR} + \rho_{red}}$ | vegetation index |
| Radar range resolution | $\delta_r = \dfrac{c}{2B}$ (slant), ground: $\delta_r/\sin\theta_i$ | *B* chirp bandwidth; Chapter 15 |
| SAR azimuth resolution (stripmap) | $\delta_a \approx L_a/2$ | *L*~a~ antenna length |
| Radar equation | $P_r = \dfrac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4}$ | σ radar cross-section |
| Altimeter range | $R = \dfrac{c\,\Delta t}{2}$ | Δ*t* echo delay |

: Remote sensing, optics and radar. {#tbl:apxeqrs}

## Space Environment and Astronomy

| Quantity | Equation | Symbols and notes |
|---|---|---|
| Dipole magnetic field | $B = B_0\left(\dfrac{R_E}{r}\right)^3\sqrt{1 + 3\sin^2\lambda}$ | *B*₀ ≈ 30 µT at Earth's equator; Chapter 23 |
| Dipole field line (L-shell) | $r = L R_E \cos^2\lambda$ | λ magnetic latitude |
| Gyrofrequency | $f_g = \dfrac{qB}{2\pi m}$ | electrons: 28 GHz per tesla |
| Plasma frequency | $f_p \approx 8.98\sqrt{n_e}$ Hz | *n*~e~ in m⁻³; sets ionospheric reflection |
| Ionospheric group delay | $\Delta\rho = \dfrac{40.3}{f^2}\,\mathrm{TEC}$ | metres, TEC in electrons/m²; Chapter 18 |
| Dynamic pressure of the solar wind | $p = \rho_{sw}v_{sw}^2 = n m_p v^2$ | ≈ 1–2 nPa, sets magnetopause distance |
| Magnetopause stand-off | $\dfrac{r_{mp}}{R_E} \approx \left(\dfrac{2B_0^2}{\mu_0\, n m_p v^2}\right)^{1/6}$ | ≈ 10 *R*~E~ |
| Apparent magnitude | $m_1 - m_2 = -2.5\log_{10}\dfrac{F_1}{F_2}$ | 5 magnitudes = factor 100 |
| Distance modulus | $m - M = 5\log_{10}\dfrac{d}{10\ \mathrm{pc}}$ | |
| Transit depth | $\delta = \left(R_p/R_\star\right)^2$ | Earth–Sun: 84 ppm; Chapter 39 |
| Hubble–Lemaître law | $v = H_0 d$ | *H*₀ ≈ 67–73 km/s/Mpc |
| Redshift | $1 + z = \dfrac{\lambda_{obs}}{\lambda_{emit}}$ | |
| Radiation dose | $D = E/m$ (gray), $\;H = w_R D$ (sievert) | Chapter 30 |

: Space environment and astronomy. {#tbl:apxeqenv}

::: note
**Using these equations safely**

Every equation here rests on assumptions — two bodies and point masses for the conic equations, ideal gas and frozen chemistry for the nozzle equations, an exponential atmosphere for the entry formulas, isotropic antennas for path loss. Use them to size, estimate and check; use validated tools (high-fidelity propagators, chemical-equilibrium codes, ray-tracing and finite-element models) for design decisions, and always check that an answer has the right units and order of magnitude.
:::
