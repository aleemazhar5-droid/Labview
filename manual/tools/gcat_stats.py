#!/usr/bin/env python3
"""Derive summary statistics from Jonathan McDowell's GCAT (planet4589.org/space/gcat, CC-BY)
into data/gcat_stats.json, used by figure scripts. Raw TSVs live in data/raw (not committed)."""
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"


def load(name):
    with open(RAW / name, encoding="utf-8", errors="replace") as f:
        hdr = f.readline().lstrip("#").rstrip("\n").split("\t")
        rows = []
        for r in csv.reader(f, delimiter="\t"):
            if not r or r[0].startswith("#"):
                continue
            rows.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(hdr)})
    return rows


GROUPS = {"US": "United States", "SU": "USSR / Russia", "RU": "USSR / Russia", "CN": "China", "F": "Europe",
          "I-ESA": "Europe", "I-ARIANE": "Europe", "J": "Japan", "IN": "India", "NZ": "United States",
          "KZ": "USSR / Russia"}


def main():
    orgs = {o["Code"]: o for o in load("orgs.tsv")}
    sites = {s["Site"]: s for s in load("sites.tsv")}
    launches = load("launch.tsv")
    out = {"updated": "2026-10-13"}

    def site_state(code):
        s = sites.get(code)
        return s["StateCode"] if s else "?"

    def agency_state(code):
        code = code.split("/")[0]
        o = orgs.get(code)
        return o["StateCode"] if o else "?"

    by_year = collections.defaultdict(lambda: collections.Counter())
    fam_2025 = collections.Counter()
    fam_2026 = collections.Counter()
    mass_year = collections.Counter()
    fails = collections.Counter()
    for L in launches:
        code = L["LaunchCode"]
        if not code or code[0] not in "OD":
            continue
        y = L["Launch_Date"][:4]
        if not y.isdigit():
            continue
        st = agency_state(L["Agency"])
        # Rocket Lab (NZ site, US company) counts as US; Arianespace/ESA as Europe
        grp = GROUPS.get(st, None)
        if grp is None:
            if st.startswith("I-") or st in ("F", "D", "I", "UK", "GB", "E", "S", "N"):
                grp = "Europe"
            else:
                grp = "Other"
        if L["Agency"].startswith("RLAB"):
            grp = "United States"
        by_year[y][grp] += 1
        by_year[y]["_all"] += 1
        if len(code) > 1 and code[1] == "F":
            fails[y] += 1
        lv = L["LV_Type"]
        fam = family(lv)
        if y == "2025":
            fam_2025[fam] += 1
        if y == "2026":
            fam_2026[fam] += 1
        try:
            mass_year[y] += float(L["OrbPay"] or 0)
        except ValueError:
            pass
    out["launches_by_year"] = {y: dict(c) for y, c in sorted(by_year.items())}
    out["failures_by_year"] = dict(sorted(fails.items()))
    out["families_2025"] = fam_2025.most_common(25)
    out["families_2026_ytd"] = fam_2026.most_common(25)
    out["payload_mass_t_by_year"] = {y: round(v, 1) for y, v in sorted(mass_year.items())}

    # ---- satellite catalogue ----
    sat = load("satcat.tsv")
    psat = {p["JCAT"]: p for p in load("psatcat.tsv")}
    in_orbit = [s for s in sat if s["Status"] in ("O", "AO", "OX", "N") or s["Status"].startswith("O")]
    out["status_codes"] = collections.Counter(s["Status"] for s in sat).most_common(20)
    types = collections.Counter()
    regimes = collections.Counter()
    pay_regimes = collections.Counter()
    owners = collections.Counter()
    alt_hist = collections.Counter()
    starlink = 0
    active = 0
    for s in in_orbit:
        t = s["Type"][:1]
        types[t] += 1
        reg = regime(s["OpOrbit"])
        regimes[reg] += 1
        if t == "P":
            pay_regimes[reg] += 1
            st = s["State"]
            owners[st] += 1
            if "Starlink" in s["Name"]:
                starlink += 1
            p = psat.get(s["JCAT"])
            if p and p.get("TF", "-") in ("-", "") and p.get("TDate", "-") in ("-", "", "*"):
                active += 1
        try:
            per = float(s["Perigee"]); apo = float(s["Apogee"])
            if 0 < apo < 2500:
                alt_hist[int((per + apo) / 2 // 25 * 25)] += 1
        except ValueError:
            pass
    out["in_orbit_by_type"] = dict(types)
    out["in_orbit_by_regime"] = dict(regimes)
    out["payloads_in_orbit_by_regime"] = dict(pay_regimes)
    out["payloads_in_orbit_by_state"] = owners.most_common(20)
    out["starlink_in_orbit"] = starlink
    out["payloads_active_est"] = active
    out["mean_alt_hist_25km"] = dict(sorted(alt_hist.items()))
    # payloads launched per year (all, and Starlink)
    pl_year = collections.Counter()
    sl_year = collections.Counter()
    for s in sat:
        if s["Type"][:1] != "P":
            continue
        y = s["LDate"][:4]
        if y.isdigit():
            pl_year[y] += 1
            if "Starlink" in s["Name"]:
                sl_year[y] += 1
    out["payloads_launched_by_year"] = dict(sorted(pl_year.items()))
    out["starlink_launched_by_year"] = dict(sorted(sl_year.items()))
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/gcat_stats.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("in_orbit_by_type", "payloads_in_orbit_by_regime", "starlink_in_orbit",
                                           "payloads_active_est", "status_codes")}, indent=0))
    print("2025:", out["launches_by_year"].get("2025"), "2026:", out["launches_by_year"].get("2026"))
    print(out["families_2025"][:15])


def regime(op):
    op = op.upper()
    if op.startswith("GEO") or op.startswith("GSO"):
        return "GEO"
    if op.startswith("MEO"):
        return "MEO"
    if op.startswith("HEO") or op.startswith("GTO") or op.startswith("VHEO"):
        return "HEO/GTO"
    if op.startswith("LLEO") or op.startswith("LEO"):
        return "LEO"
    if op.startswith("DSO") or op.startswith("CLO") or op.startswith("EEO") or op.startswith("SO"):
        return "Deep space"
    return "Other"


def family(lv):
    lv = lv.strip()
    for pat, name in [(r"^Falcon 9", "Falcon 9"), (r"^Falcon Heavy", "Falcon Heavy"), (r"^Starship", "Starship"),
                      (r"^Chang Zheng|^CZ-", "Long March"), (r"^Soyuz|^Soyuz-2", "Soyuz"), (r"^Electron", "Electron"),
                      (r"^Kuaizhou", "Kuaizhou"), (r"^Ceres", "Ceres-1"), (r"^Zhuque", "Zhuque"),
                      (r"^Lijian|^Kinetica", "Kinetica-1 (Lijian)"), (r"^Jielong|^Smart Dragon", "Jielong"),
                      (r"^Gushenxing", "Ceres-1"), (r"^Yinli", "Gravity-1"), (r"^Ariane 6", "Ariane 6"), (r"^Vega", "Vega"),
                      (r"^H-?3", "H3"), (r"^H-IIA|^H-2A", "H-IIA"), (r"^PSLV", "PSLV"), (r"^GSLV", "GSLV/LVM3"),
                      (r"^LVM3|^GSLV Mk ?III", "GSLV/LVM3"), (r"^Vulcan", "Vulcan"), (r"^Atlas", "Atlas V"),
                      (r"^New Glenn", "New Glenn"), (r"^Angara", "Angara"), (r"^Proton", "Proton"),
                      (r"^Minotaur", "Minotaur"), (r"^Antares", "Antares"), (r"^Firefly|^Alpha", "Firefly Alpha"),
                      (r"^Tianlong", "Tianlong"), (r"^Hyperbola", "Hyperbola"), (r"^SSLV", "SSLV"),
                      (r"^Nuri", "Nuri"), (r"^Qaem|^Simorgh|^Qased", "Iran"), (r"^Chollima", "Chollima"),
                      (r"^Spectrum", "Spectrum"), (r"^Delta", "Delta IV")]:
        if re.search(pat, lv):
            return name
    return lv


if __name__ == "__main__":
    main()
