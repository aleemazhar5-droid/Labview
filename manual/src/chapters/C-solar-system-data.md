---
title: Solar System Data
abstract: Reference data for mission design and planetary science — physical and orbital properties of the Sun, the planets, the Moon and Pluto; gravitational parameters, spheres of influence and idealised transfer requirements from Earth; the major moons; the small bodies visited by spacecraft; Lagrange points; and the US Standard Atmosphere. Values follow the NASA Planetary Fact Sheets, JPL Solar System Dynamics and IAU working-group data, rounded for engineering use.
---

The tables in this appendix give the values used in the chapters on orbital mechanics (Chapter 3), deep-space mission design (Chapter 24) and planetary exploration (Chapters 25–29). Masses and radii are known far more precisely than shown here; the values are rounded so that the tables stay readable. When designing a real trajectory, use the gravitational parameters and ephemerides distributed by JPL (the DE440 series) through the SPICE toolkit.

## The Planets

| Body | Mass (10²⁴ kg) | Equatorial radius (km) | Mean density (kg/m³) | Surface gravity (m/s²) | Escape speed (km/s) | Sidereal rotation (h) | Obliquity (°) |
|---|---|---|---|---|---|---|---|
| Mercury | 0.330 | 2 440 | 5 429 | 3.7 | 4.3 | 1 407.6 | 0.03 |
| Venus | 4.87 | 6 052 | 5 243 | 8.9 | 10.4 | −5 832.5 | 177.4 |
| Earth | 5.97 | 6 378 | 5 514 | 9.8 | 11.2 | 23.93 | 23.4 |
| Moon | 0.073 | 1 738 | 3 344 | 1.6 | 2.4 | 655.7 | 6.7 |
| Mars | 0.642 | 3 396 | 3 934 | 3.7 | 5.0 | 24.62 | 25.2 |
| Jupiter | 1 898 | 71 492 | 1 326 | 23.1 | 59.5 | 9.93 | 3.1 |
| Saturn | 568 | 60 268 | 687 | 9.0 | 35.5 | 10.66 | 26.7 |
| Uranus | 86.8 | 25 559 | 1 270 | 8.7 | 21.3 | −17.24 | 97.8 |
| Neptune | 102 | 24 764 | 1 638 | 11.0 | 23.5 | 16.11 | 28.3 |
| Pluto | 0.013 0 | 1 188 | 1 854 | 0.62 | 1.2 | −153.3 | 122.5 |

: Physical properties of the planets, the Moon and Pluto. A negative rotation period means retrograde rotation. Gravity and escape speed are at the equator of the 1-bar level for the giant planets. Source: NASA Planetary Fact Sheet. {#tbl:apxplanetphys}

| Body | Semi-major axis (au) | Eccentricity | Inclination to ecliptic (°) | Orbital period | Mean surface temperature | Surface pressure | Known moons (2026) |
|---|---|---|---|---|---|---|---|
| Mercury | 0.387 | 0.206 | 7.0 | 88.0 d | 167 °C (−180 to 430) | ≈ 0 | 0 |
| Venus | 0.723 | 0.007 | 3.4 | 224.7 d | 464 °C | 92 bar | 0 |
| Earth | 1.000 | 0.017 | 0.0 | 365.26 d | 15 °C | 1.014 bar | 1 |
| Mars | 1.524 | 0.093 | 1.8 | 687.0 d | −65 °C | 0.006 bar | 2 |
| Jupiter | 5.203 | 0.048 | 1.3 | 11.86 yr | −110 °C (1 bar) | — | 101 |
| Saturn | 9.555 | 0.054 | 2.5 | 29.45 yr | −140 °C (1 bar) | — | 285 |
| Uranus | 19.22 | 0.047 | 0.8 | 84.0 yr | −195 °C (1 bar) | — | 29 |
| Neptune | 30.11 | 0.009 | 1.8 | 164.8 yr | −200 °C (1 bar) | — | 16 |
| Pluto | 39.48 | 0.249 | 17.2 | 248 yr | −225 °C | ≈ 10 µbar | 5 |

: Orbital properties of the planets and Pluto (epoch J2000). Moon counts change as surveys find more small irregular moons; the 2026 values include the Jupiter and Saturn moons announced by the Minor Planet Center in March 2026. {#tbl:apxplanetorb}

The giant planets have no solid surface; their "surface" values refer to the level where the pressure is 1 bar. Saturn's mean density is lower than that of water. Venus and Uranus rotate backwards; Uranus is tipped on its side, so each pole faces the Sun for 42 years at a time.

## Gravitational Parameters and Mission Design Data

@tbl:apxgm gives the gravitational parameter μ = *GM* of each body, its *J*₂ oblateness coefficient, and the radius of its *sphere of influence* — the region inside which the planet's gravity, rather than the Sun's, is the better reference for a patched-conic trajectory (Chapter 24). The sphere-of-influence radius is *r*~SOI~ = *a* (*m*/*M*~☉~)^2/5^, where *a* is the planet's orbital radius.

| Body | μ = *GM* (km³/s²) | *J*₂ (× 10⁻⁶) | Sphere of influence (10³ km) | in planet radii |
|---|---|---|---|---|
| Sun | 132 712 440 041 | 0.2 | — | — |
| Mercury | 22 032 | 50 | 112 | 46 |
| Venus | 324 859 | 4.5 | 616 | 102 |
| Earth | 398 600 | 1 082.6 | 925 | 145 |
| Moon | 4 902.8 | 203 | 66 (about Earth) | 38 |
| Mars | 42 828 | 1 960 | 577 | 170 |
| Jupiter | 126 686 534 | 14 736 | 48 200 | 674 |
| Saturn | 37 931 187 | 16 298 | 54 600 | 907 |
| Uranus | 5 793 939 | 3 343 | 51 800 | 2 028 |
| Neptune | 6 836 529 | 3 411 | 86 800 | 3 504 |
| Pluto | 869.6 | — | 3 150 | 2 648 |

: Gravitational parameters, oblateness and spheres of influence. Computed from JPL values; the Moon's sphere of influence is with respect to the Earth. {#tbl:apxgm}

@tbl:apxhohmann gives the idealised *Hohmann transfer* from Earth to each planet, assuming circular, coplanar orbits. Real launch opportunities differ — Mars needs a C3 of 8–16 km²/s² depending on the year, and missions to the outer planets use gravity assists to cut both C3 and flight time (Chapter 24) — but the table shows the scale of each journey. *C3* is the square of the hyperbolic excess speed at departure; *v*~∞~ at arrival is the speed relative to the planet before its gravity accelerates the spacecraft.

| Destination | Departure C3 (km²/s²) | Δ*v* from 400 km LEO (km/s) | Arrival *v*~∞~ (km/s) | Transfer time | Synodic period (days) |
|---|---|---|---|---|---|
| Mercury | 56.7 | 5.54 | 9.61 | 105 d | 116 |
| Venus | 6.2 | 3.46 | 2.71 | 146 d | 584 |
| Mars | 8.7 | 3.57 | 2.65 | 259 d | 780 |
| Jupiter | 77.3 | 6.29 | 5.64 | 2.73 yr | 399 |
| Saturn | 105.9 | 7.28 | 5.44 | 6.06 yr | 378 |
| Uranus | 127.3 | 7.98 | 4.66 | 16.1 yr | 370 |
| Neptune | 135.8 | 8.25 | 4.05 | 30.7 yr | 367 |
| Pluto | 139.6 | 8.37 | 3.69 | 45.5 yr | 367 |

: Idealised Hohmann transfers from Earth (circular coplanar orbits; Pluto at its mean distance). The synodic period is the interval between successive launch opportunities. {#tbl:apxhohmann}

## Major Moons

| Moon | Planet | Mean radius (km) | μ (km³/s²) | Orbit radius (10³ km) | Period (days) | Notes |
|---|---|---|---|---|---|---|
| Moon | Earth | 1 737.4 | 4 902.8 | 384.4 | 27.32 | Synchronous rotation; polar ice in shadowed craters |
| Phobos | Mars | 11.1 | 7.1 × 10⁻⁴ | 9.38 | 0.319 | Target of JAXA's MMX sample return |
| Deimos | Mars | 6.2 | 1.0 × 10⁻⁴ | 23.46 | 1.263 | |
| Io | Jupiter | 1 821.6 | 5 959.9 | 421.8 | 1.769 | Most volcanically active body known |
| Europa | Jupiter | 1 560.8 | 3 202.7 | 671.1 | 3.551 | Subsurface ocean; Europa Clipper arrives 2030 |
| Ganymede | Jupiter | 2 631.2 | 9 887.8 | 1 070.4 | 7.155 | Largest moon; own magnetic field; JUICE target |
| Callisto | Jupiter | 2 410.3 | 7 179.3 | 1 882.7 | 16.69 | Heavily cratered |
| Mimas | Saturn | 198.2 | 2.50 | 185.5 | 0.942 | Possible young internal ocean |
| Enceladus | Saturn | 252.1 | 7.21 | 238.0 | 1.370 | South-polar water plumes |
| Tethys | Saturn | 531.1 | 41.2 | 294.7 | 1.888 | |
| Dione | Saturn | 561.4 | 73.1 | 377.4 | 2.737 | |
| Rhea | Saturn | 763.8 | 153.9 | 527.1 | 4.518 | |
| Titan | Saturn | 2 574.7 | 8 978.1 | 1 221.9 | 15.945 | 1.5 bar N₂ atmosphere; methane lakes; Dragonfly target |
| Iapetus | Saturn | 734.5 | 120.5 | 3 560.8 | 79.33 | Two-toned surface |
| Miranda | Uranus | 235.8 | 4.3 | 129.9 | 1.413 | Extreme cliffs |
| Ariel | Uranus | 578.9 | 83.5 | 190.9 | 2.520 | |
| Umbriel | Uranus | 584.7 | 85.1 | 266.0 | 4.144 | |
| Titania | Uranus | 788.4 | 228.2 | 436.3 | 8.706 | Largest moon of Uranus |
| Oberon | Uranus | 761.4 | 192.4 | 583.5 | 13.46 | |
| Triton | Neptune | 1 353.4 | 1 427.6 | 354.8 | 5.877 (retrograde) | Captured Kuiper-belt object; nitrogen geysers |
| Charon | Pluto | 606 | 106.1 | 19.6 | 6.387 | Mutually locked with Pluto |

: Properties of the major moons. Source: JPL Solar System Dynamics planetary satellite physical and mean orbital parameters. {#tbl:apxmoons}

## Small Bodies Visited by Spacecraft

| Body | Type | Size | Orbit | Spacecraft (year of visit) |
|---|---|---|---|---|
| 1 Ceres | Dwarf planet (C-type) | 939 km diameter | 2.77 au, 4.6 yr | Dawn orbiter (2015–18) |
| 4 Vesta | Differentiated asteroid | 525 km | 2.36 au, 3.6 yr | Dawn orbiter (2011–12) |
| 433 Eros | S-type NEA | 34 × 11 × 11 km | 1.46 au, 1.76 yr | NEAR Shoemaker; landed 2001 |
| 25143 Itokawa | S-type NEA | 535 × 294 × 209 m | 1.32 au | Hayabusa sample return (2005, returned 2010) |
| 162173 Ryugu | C-type NEA | 0.9 km | 1.19 au | Hayabusa2 sample return (2018–19, returned 2020) |
| 101955 Bennu | B-type NEA | 0.49 km | 1.13 au | OSIRIS-REx sample return (2018–21, returned 2023) |
| 65803 Didymos / Dimorphos | S-type binary NEA | 0.78 km / 0.15 km | 1.64 au | DART impact (2022); Hera (arrives November 2026) |
| 152830 Dinkinesh | S-type main-belt | 0.79 km, with contact-binary moon | 2.19 au | Lucy flyby (2023) |
| 52246 Donaldjohanson | C-type main-belt | ≈ 8 km elongated | 2.38 au | Lucy flyby (April 2025) |
| 16 Psyche | M-type (metal-rich) | ≈ 220 km | 2.92 au | Psyche orbiter (arrival 2029) |
| 67P/Churyumov–Gerasimenko | Jupiter-family comet | 4.1 × 3.3 × 1.8 km (two lobes) | 3.46 au, 6.4 yr | Rosetta and Philae (2014–16) |
| 1P/Halley | Halley-type comet | 15 × 8 km | 17.8 au, 76 yr | Giotto, Vega 1/2, Suisei, Sakigake (1986) |
| 486958 Arrokoth | Cold classical KBO | 36 km contact binary | 44.6 au | New Horizons flyby (2019) |
| 99942 Apophis | S-type NEA | ≈ 340 m | 0.92 au | OSIRIS-APEX (arrives 2029, after the 13 April 2029 Earth flyby at ≈ 32 000 km altitude) |

: Small bodies visited, or soon to be visited, by spacecraft (Chapters 25–29). {#tbl:apxsmallbodies}

## Lagrange Points

In the three-body problem a small spacecraft can stay fixed relative to two large bodies at five *Lagrange points* (Chapter 3). L1, L2 and L3 lie on the line through the two bodies and are unstable — a spacecraft must make small station-keeping burns, typically a few metres per second per year — while L4 and L5 lead and trail the smaller body by 60° and are stable.

| System | L1 (from smaller body) | L2 (from smaller body) | L3 | L4 / L5 | Spacecraft |
|---|---|---|---|---|---|
| Sun–Earth | 1.498 million km sunward | 1.508 million km anti-sunward | opposite side of the Sun | 60° ahead / behind Earth | L1: SOHO, ACE, DSCOVR, Aditya-L1, SWFO-L1, IMAP; L2: JWST, Gaia, Euclid, Roman |
| Earth–Moon | 58 000 km Earth-side of the Moon (326 400 km from Earth) | 64 500 km beyond the Moon (448 900 km from Earth) | 381 700 km from Earth, opposite the Moon | at lunar distance, 60° ahead / behind | L2: Queqiao-1 and -2 halo orbits; the Gateway's NRHO is related to the L1/L2 halo family |

: Lagrange-point locations computed from the circular restricted three-body problem. {#tbl:apxlagrange}

## The US Standard Atmosphere 1976

The *US Standard Atmosphere 1976* is an idealised, steady-state model of the Earth's atmosphere for moderate solar activity. Below 86 km it is identical to the ICAO standard atmosphere used in aviation. Above about 150 km the real density can be ten times higher or lower than shown, depending on solar and geomagnetic activity (Chapters 2 and 22) — use an empirical model such as NRLMSIS 2.1 or JB2008 for drag and lifetime work.

| Altitude (km) | Temperature (K) | Pressure (Pa) | Density (kg/m³) | Layer |
|---|---|---|---|---|
| 0 | 288.15 | 101 325 | 1.225 | Troposphere |
| 5 | 255.68 | 54 048 | 0.736 | |
| 11 | 216.77 | 22 700 | 0.365 | Tropopause |
| 20 | 216.65 | 5 529 | 0.088 9 | Stratosphere |
| 32 | 228.49 | 889.1 | 0.013 6 | |
| 47 | 269.68 | 115.9 | 1.50 × 10⁻³ | Stratopause region |
| 51 | 270.65 | 70.46 | 9.07 × 10⁻⁴ | Mesosphere |
| 71 | 216.82 | 4.480 | 7.20 × 10⁻⁵ | |
| 86 | 186.87 | 0.373 4 | 6.96 × 10⁻⁶ | Mesopause |
| 100 | 195.08 | 3.20 × 10⁻² | 5.60 × 10⁻⁷ | Kármán line, thermosphere |
| 150 | 634.39 | 4.54 × 10⁻⁴ | 2.08 × 10⁻⁹ | |
| 200 | 854.56 | 8.47 × 10⁻⁵ | 2.54 × 10⁻¹⁰ | |
| 300 | 976.01 | 8.77 × 10⁻⁶ | 1.92 × 10⁻¹¹ | |
| 400 | 995.83 | 1.45 × 10⁻⁶ | 2.80 × 10⁻¹² | ISS altitude |
| 500 | 999.24 | 3.02 × 10⁻⁷ | 5.22 × 10⁻¹³ | |
| 600 | 999.85 | 8.21 × 10⁻⁸ | 1.14 × 10⁻¹³ | |
| 800 | 999.99 | 1.70 × 10⁻⁸ | 1.14 × 10⁻¹⁴ | |
| 1 000 | 1 000.00 | 7.51 × 10⁻⁹ | 3.56 × 10⁻¹⁵ | Exosphere |

: US Standard Atmosphere 1976 (geometric altitude). {#tbl:apxstdatm}

| Planet / moon | Main gases | Surface pressure | Scale height (km) | Notes for entry and flight |
|---|---|---|---|---|
| Venus | 96.5 % CO₂, 3.5 % N₂ | 92 bar | 15.9 | Surface 464 °C; sulphuric-acid clouds 48–70 km |
| Earth | 78 % N₂, 21 % O₂ | 1.014 bar | 8.5 | |
| Mars | 95 % CO₂, 2.6 % N₂, 1.9 % Ar | ≈ 6 mbar (varies with season and height) | 11.1 | Thin: parachutes alone cannot land heavy payloads |
| Jupiter | 90 % H₂, 10 % He | — | 27 | Galileo probe entered at 47.4 km/s (1995) |
| Titan | ≈ 95 % N₂, ≈ 5 % CH₄ | 1.5 bar | ≈ 20–40 | Dense and cold (94 K): ideal for flight — Dragonfly |

: Atmospheres relevant to entry, descent and aerial vehicles (Chapters 27 and 28). {#tbl:apxatmospheres}

::: key
**Key takeaways**

- Use μ = *GM* from JPL ephemerides for trajectory work; the tables here are rounded for estimates.
- The Hohmann table gives the scale of each journey: Mars and Venus need about 3.5 km/s from LEO, the outer planets 6–8 km/s, and Neptune more than 30 years without gravity assists.
- Launch opportunities repeat at the synodic period — every 26 months for Mars, every 19 months for Venus, about every 13 months for the outer planets.
- Atmospheric density above 150 km varies by a factor of ten with solar activity; standard atmospheres are only a starting point.
:::
