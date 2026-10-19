---
title: Constants, Units and Time Systems
abstract: The physical and astronomical constants used throughout this manual, the SI units and prefixes, conversion factors for the non-SI units still common in aerospace, decibel conventions used in link budgets, and the time scales and epochs used to timestamp orbits, telemetry and observations. Values follow the 2019 SI, CODATA 2022 recommended values, the IAU 2012 and 2015 resolutions, and the WGS 84 Earth model.
---

This appendix collects the numbers an engineer reaches for most often. Exact values (by definition) are marked **exact**; other values are given to the precision useful in engineering work, with the last digits uncertain as in the source. Where two sources differ slightly — for example the Earth's gravitational parameter in WGS 84 and in the latest geodetic models — the value used throughout this manual is given, and the difference is far smaller than any engineering margin.

## The SI and Its Defining Constants

Since 20 May 2019 all seven SI base units are defined by fixing the numerical values of seven constants of nature (@tbl:apxsidefining). The kilogram is no longer a metal cylinder in Paris; it is defined through the Planck constant. For practical engineering nothing changed, but every unit can now in principle be realised anywhere — including in orbit.

| Defining constant | Symbol | Value (exact) | Unit it defines |
|---|---|---|---|
| Caesium hyperfine transition frequency | Δν~Cs~ | 9 192 631 770 Hz | second |
| Speed of light in vacuum | *c* | 299 792 458 m/s | metre |
| Planck constant | *h* | 6.626 070 15 × 10⁻³⁴ J s | kilogram |
| Elementary charge | *e* | 1.602 176 634 × 10⁻¹⁹ C | ampere |
| Boltzmann constant | *k* | 1.380 649 × 10⁻²³ J/K | kelvin |
| Avogadro constant | *N*~A~ | 6.022 140 76 × 10²³ mol⁻¹ | mole |
| Luminous efficacy of 540 THz light | *K*~cd~ | 683 lm/W | candela |

: The seven defining constants of the SI (2019). {#tbl:apxsidefining}

| Factor | Prefix | Symbol | Factor | Prefix | Symbol |
|---|---|---|---|---|---|
| 10³⁰ | quetta | Q | 10⁻¹ | deci | d |
| 10²⁷ | ronna | R | 10⁻² | centi | c |
| 10²⁴ | yotta | Y | 10⁻³ | milli | m |
| 10²¹ | zetta | Z | 10⁻⁶ | micro | µ |
| 10¹⁸ | exa | E | 10⁻⁹ | nano | n |
| 10¹⁵ | peta | P | 10⁻¹² | pico | p |
| 10¹² | tera | T | 10⁻¹⁵ | femto | f |
| 10⁹ | giga | G | 10⁻¹⁸ | atto | a |
| 10⁶ | mega | M | 10⁻²¹ | zepto | z |
| 10³ | kilo | k | 10⁻²⁴ | yocto | y |
| 10² | hecto | h | 10⁻²⁷ | ronto | r |
| 10¹ | deca | da | 10⁻³⁰ | quecto | q |

: SI prefixes. Ronna, quetta, ronto and quecto were added in 2022 — partly so that data volumes and planetary masses could be written compactly (the Earth's mass is about 6 Rg). {#tbl:apxprefixes}

For data storage the binary prefixes are also standardised (IEC 80000-13): 1 KiB (kibibyte) = 1 024 bytes, 1 MiB = 1 048 576 bytes, 1 GiB = 2³⁰ bytes, 1 TiB = 2⁴⁰ bytes. Space-mission documents usually quote downlink rates in decimal units (1 Mbit/s = 10⁶ bit/s) and on-board memory in binary units, so a "256 GB" recorder may hold 256 GiB = 275 × 10⁹ bytes. Always check which convention a specification uses.

## Physical Constants

@tbl:apxphysconst lists the physical constants used in this manual. The gravitational constant *G* is known only to about 22 parts per million, which is why orbital mechanics always uses the product *GM* (the *gravitational parameter* μ) — it can be measured from spacecraft tracking about a million times more precisely than *G* or *M* separately.

| Constant | Symbol | Value | Notes |
|---|---|---|---|
| Newtonian constant of gravitation | *G* | 6.674 30 × 10⁻¹¹ m³ kg⁻¹ s⁻² | ± 0.000 15 |
| Stefan–Boltzmann constant | σ | 5.670 374 419 × 10⁻⁸ W m⁻² K⁻⁴ | exact (derived) |
| Wien displacement constant | *b* | 2.897 771 955 × 10⁻³ m K | λ~peak~ = *b*/*T* |
| Molar gas constant | *R* | 8.314 462 618 J mol⁻¹ K⁻¹ | exact (derived) |
| Vacuum permittivity | ε₀ | 8.854 187 8188 × 10⁻¹² F/m | |
| Vacuum permeability | μ₀ | 1.256 637 061 27 × 10⁻⁶ N/A² | ≈ 4π × 10⁻⁷ |
| Impedance of free space | *Z*₀ | 376.730 Ω | μ₀*c* |
| Electron mass | *m*~e~ | 9.109 383 7139 × 10⁻³¹ kg | 0.511 MeV/c² |
| Proton mass | *m*~p~ | 1.672 621 925 95 × 10⁻²⁷ kg | 938.272 MeV/c² |
| Atomic mass constant | *m*~u~ | 1.660 539 068 92 × 10⁻²⁷ kg | 1 Da |
| Electronvolt | eV | 1.602 176 634 × 10⁻¹⁹ J | exact |
| Standard acceleration of gravity | *g*₀ | 9.806 65 m/s² | exact; used for *I*~sp~ |
| Standard atmosphere | atm | 101 325 Pa | exact |
| Boltzmann constant in decibels | 10 log *k* | −228.6 dBW K⁻¹ Hz⁻¹ | link budgets |

: Physical constants (CODATA 2022 recommended values). {#tbl:apxphysconst}

## Astronomical and Earth Constants

| Quantity | Value | Source / note |
|---|---|---|
| Astronomical unit (au) | 149 597 870 700 m | exact (IAU 2012) |
| Light-time for 1 au | 499.005 s (8 min 19 s) | |
| Light-year (Julian year × *c*) | 9.460 730 × 10¹⁵ m = 63 241 au | exact |
| Parsec | 3.085 678 × 10¹⁶ m = 3.262 ly = 206 265 au | exact via au |
| Sun, *GM*~☉~ | 1.327 124 400 41 × 10²⁰ m³/s² | planetary ephemerides |
| Sun, mass | 1.988 4 × 10³⁰ kg | *GM*/*G* |
| Sun, nominal radius | 695 700 km | IAU 2015 |
| Sun, nominal luminosity | 3.828 × 10²⁶ W | IAU 2015 |
| Sun, effective temperature | 5 772 K | IAU 2015 |
| Total solar irradiance at 1 au | ≈ 1 361 W/m² | varies ± 0.1 % with the cycle |
| Earth, *GM*~⊕~ | 3.986 004 418 × 10¹⁴ m³/s² | WGS 84 |
| Earth, mass | 5.972 2 × 10²⁴ kg | |
| Earth, equatorial radius *a* | 6 378 137 m | WGS 84 |
| Earth, flattening *f* | 1/298.257 223 563 | WGS 84 |
| Earth, polar radius *b* | 6 356 752.3 m | WGS 84 |
| Earth, mean radius | 6 371.0 km | |
| Earth, *J*₂ zonal harmonic | 1.082 63 × 10⁻³ | drives nodal regression |
| Earth, rotation rate ω~⊕~ | 7.292 115 × 10⁻⁵ rad/s | |
| Sidereal day | 86 164.091 s (23 h 56 min 4.09 s) | |
| Mean solar day | 86 400 s | |
| Tropical year | 365.242 19 days | seasons |
| Sidereal year | 365.256 36 days | |
| Obliquity of the ecliptic (J2000) | 23.439° | |
| Moon, *GM* | 4 902.800 km³/s² | |
| Moon, mean distance | 384 400 km (light-time 1.28 s) | varies 356 400–406 700 km |
| Moon, mean radius | 1 737.4 km | |

: Astronomical and Earth constants. {#tbl:apxastroconst}

::: formula
**Useful orbital numbers for Earth**

| Altitude | Period | Circular speed | Distance to horizon | Typical use |
|---|---|---|---|---|
| 200 km | 88.5 min | 7.78 km/s | 1 610 km | Lowest practical orbit, parking orbits |
| 400 km | 92.6 min | 7.67 km/s | 2 290 km | ISS, Tiangong |
| 550 km | 95.6 min | 7.59 km/s | 2 710 km | Starlink shells, EO satellites |
| 800 km | 100.9 min | 7.45 km/s | 3 290 km | Sun-synchronous weather and EO |
| 1 200 km | 109.4 min | 7.25 km/s | 4 090 km | OneWeb, Jason/Sentinel-6 |
| 20 200 km | 11 h 58 min | 3.87 km/s | 25 800 km | GPS (half a sidereal day) |
| 35 786 km | 23 h 56 min | 3.07 km/s | 41 680 km | Geostationary orbit (radius 42 164 km) |

: Circular-orbit period, speed and horizon distance (spherical Earth, *GM* from WGS 84). One degree of longitude along the geostationary arc is 736 km. {#tbl:apxleoquick}

Escape speed from the Earth's surface is 11.19 km/s; from a 400 km orbit it is 10.85 km/s, only 3.18 km/s more than circular speed.
:::

## Conversion Factors

Aerospace still mixes SI with US customary units — rocket thrust in pounds-force, altitude in feet, pressures in psi, antenna gain in decibels. @tbl:apxconv lists the conversions used most often; all are exact except where three or fewer significant figures are shown as a rounded value.

| Quantity | Unit | SI value |
|---|---|---|
| Length | inch / foot | 0.025 4 m / 0.304 8 m (exact) |
| | statute mile / nautical mile | 1 609.344 m / 1 852 m (exact) |
| Mass | pound (lb) | 0.453 592 37 kg (exact) |
| | slug | 14.593 9 kg |
| | metric tonne (t) | 1 000 kg |
| Force | pound-force (lbf) | 4.448 222 N |
| | kilogram-force (kgf) | 9.806 65 N (exact) |
| Pressure | psi (lbf/in²) | 6 894.757 Pa |
| | bar / atm / torr | 10⁵ Pa / 101 325 Pa / 133.322 Pa |
| Energy | kilowatt-hour | 3.6 MJ (exact) |
| | British thermal unit (BTU) | 1 055.06 J |
| | thermochemical calorie | 4.184 J (exact) |
| | kilotonne of TNT | 4.184 × 10¹² J |
| Power | horsepower (mechanical) | 745.700 W |
| Speed | knot / mile per hour | 0.514 444 m/s / 0.447 04 m/s |
| | Mach 1 at sea level (15 °C) | 340.3 m/s |
| Angle | degree / arcminute / arcsecond | 17.453 3 mrad / 290.888 µrad / 4.848 14 µrad |
| | milliarcsecond (mas) | 4.848 14 nrad |
| | steradian (sphere = 4π sr) | 1 sr = 3 282.8 deg² |
| Temperature | °C / °F / °R | *T*~K~ = *T*~°C~ + 273.15; *T*~°F~ = 1.8 *T*~°C~ + 32; *T*~°R~ = 1.8 *T*~K~ |
| Radiation dose | rad / rem | 0.01 Gy / 0.01 Sv |
| Magnetic flux density | gauss (G) / gamma (γ) | 10⁻⁴ T / 1 nT |
| Specific impulse | second (s) | effective exhaust speed *v*~e~ = *I*~sp~ × *g*₀ (300 s ≈ 2.94 km/s) |
| Thrust-specific fuel consumption | lb/(lbf h) | 28.33 mg/(N s) |
| Data rate | bit/s (decimal) | 1 Gbit/s = 10⁹ bit/s |

: Conversion factors. {#tbl:apxconv}

## Decibels

Radio engineers express ratios that span many orders of magnitude in decibels: a power ratio *P*₂/*P*₁ is 10 log₁₀(*P*₂/*P*₁) dB. A factor of two is 3.01 dB, ten is 10 dB, a thousand is 30 dB, and a million is 60 dB. Multiplications in a link budget become additions. A suffix tells you the reference (@tbl:apxdb).

| Unit | Reference | Example |
|---|---|---|
| dBW | 1 W | 20 W transmitter = 13.0 dBW |
| dBm | 1 mW | 1 W = 30 dBm; GPS signal at the ground ≈ −128.5 dBm |
| dBi | isotropic antenna | 1 m dish at 8.4 GHz with 60 % efficiency ≈ 36.7 dBi |
| dBic | isotropic, circular polarisation | common for GNSS and S-band patch antennas |
| dBK | 1 kelvin | 290 K system noise temperature = 24.6 dBK |
| dB/K | gain-to-noise temperature ratio *G*/*T* | ground station 35 dB/K |
| dBHz | 1 Hz | 1 MHz bandwidth = 60 dBHz; *C*/*N*₀ in dBHz |
| dBW/m² | flux density | saturated flux density of a GEO transponder |
| dBsm | 1 m² (radar cross-section) | a 1U CubeSat ≈ −20 dBsm at high frequency |
| dBc | carrier power | spurious emission 60 dBc below the carrier |

: Decibel conventions used in link budgets (Chapter 6). {#tbl:apxdb}

## Time Scales and Epochs

A spacecraft clock, a ground station log and a planetary ephemeris may each use a different time scale. Mixing them up produces errors of a minute or more — enough to put a planetary encounter or a collision-avoidance manoeuvre in the wrong place. @tbl:apxtimescales summarises the scales in use.

| Time scale | What it is | Relation (2026) |
|---|---|---|
| TAI (International Atomic Time) | Weighted average of about 450 atomic clocks worldwide | Reference |
| UTC (Coordinated Universal Time) | Civil time; stays within 0.9 s of Earth rotation by inserting leap seconds | UTC = TAI − 37 s (since 1 January 2017) |
| UT1 | Time defined by the Earth's actual rotation angle | UT1 − UTC within ± 0.9 s, published by the IERS |
| GPS time | Continuous atomic time of the GPS system, started 6 January 1980 | GPS = TAI − 19 s = UTC + 18 s |
| Galileo System Time / BeiDou Time | Continuous GNSS time scales | GST = GPS time; BDT = UTC + 4 s |
| TT (Terrestrial Time) | Ideal time on the geoid, used for ephemerides | TT = TAI + 32.184 s = UTC + 69.184 s |
| TDB (Barycentric Dynamical Time) | Time at the Solar System barycentre, used by planetary ephemerides | TDB − TT within ± 1.7 ms (periodic) |
| Spacecraft clock (SCLK) | On-board counter; drifts | Correlated to UTC by the ground (SPICE kernels) |

: Time scales used in space operations. {#tbl:apxtimescales}

**Leap seconds.** Because the Earth's rotation is irregular, 27 leap seconds were added to UTC between 1972 and 2016. None has been needed since, because the Earth has recently been spinning slightly faster. In 2022 the General Conference on Weights and Measures decided that the tolerance between UTC and UT1 will be relaxed by 2035, effectively ending leap seconds. Software that assumes every minute has 60 seconds, or that GPS time equals UTC, has caused real outages.

**Julian Date.** Astronomers count days continuously from noon on 1 January 4713 BC (Julian calendar). The Julian Date (JD) at 00:00 UTC on 1 January 2026 is 2 461 041.5. The Modified Julian Date is MJD = JD − 2 400 000.5, so a day starts at midnight and the numbers are shorter (MJD 61 041 for the same instant). The standard epoch **J2000.0** is JD 2 451 545.0 TT — 12:00 TT on 1 January 2000 (11:58:55.816 UTC). Orbital elements in two-line element sets use a two-digit year and day-of-year with fraction.

**GNSS weeks.** GPS broadcasts a week number that originally rolled over every 1 024 weeks (19.6 years); rollovers on 21 August 1999 and 6 April 2019 broke unprepared receivers. Modernised GPS messages use a 13-bit week number that will not roll over until 2137.

**Relativity matters.** A GPS satellite clock runs fast by about 38 µs per day compared with a clock on the ground — about +45.9 µs from the weaker gravity at 20 200 km and −7.2 µs from its orbital speed. Uncorrected, this would cause ranging errors growing by about 11 km per day; the clocks are deliberately set slightly slow before launch. A clock on the Moon runs fast by about 56 µs per day relative to Earth. In 2024 the US government asked NASA to establish a Coordinated Lunar Time, and the International Astronomical Union adopted resolutions calling for a lunar reference system and time scale, so that lunar navigation systems such as LunaNet and ESA's Moonlight can share a common clock.

**Mars time.** A Martian solar day (*sol*) lasts 24 h 39 min 35.244 s (88 775.244 s). Mars rover teams work on "Mars time" for the first weeks of a mission, shifting their working day by about 40 minutes every Earth day. A Mars year lasts 668.6 sols (687.0 Earth days).

::: key
**Key takeaways**

- Seven constants now define the SI exactly; *c*, *h*, *e* and *k* have no uncertainty.
- Use the gravitational parameter μ = *GM*, not *G* and *M* separately — it is known far more precisely.
- *g*₀ = 9.806 65 m/s² exactly converts specific impulse in seconds to exhaust speed.
- In link budgets, add decibels; −228.6 dBW/(K Hz) is Boltzmann's constant.
- UTC = TAI − 37 s, GPS = UTC + 18 s, TT = TAI + 32.184 s in 2026 — always state which time scale a timestamp uses.
:::
