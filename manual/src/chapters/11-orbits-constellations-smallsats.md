---
title: Earth Orbits, Constellations and Small Satellites
hero: ch11
abstract: A satellite's orbit decides what it can see, how often, with what delay and at what cost. This chapter turns the orbital mechanics of Chapter 3 into practical mission design - choosing an orbit, calculating coverage and revisit, and designing constellations of many satellites. It then surveys the crowded reality of Earth orbit in 2026, the mega-constellations that dominate it, the geostationary belt, the small-satellite and CubeSat revolution, rideshare and in-orbit deployment, formation flying, and the sustainability questions raised by tens of thousands of satellites.
---

## Choosing an Orbit

Orbit selection is usually the first and most important decision in mission design, because it sets the environment (Chapter 2), the launch cost, the communication geometry and the performance of the payload. The main drivers are:

- **What must be seen or served** — the whole globe, high latitudes, a specific region, or a point in deep space.
- **How often** — continuously (communications, early warning), several times a day (weather, maritime), daily (crop monitoring), or occasionally (mapping).
- **How closely** — resolution improves in proportion to distance for optical and radar sensors, and link budgets improve with the square of distance.
- **Lighting** — optical imagers want consistent Sun angles; thermal and power design prefer predictable eclipses.
- **Latency** — interactive services (voice, gaming, finance) want short round-trip delays.
- **Environment and lifetime** — drag, radiation, debris density and disposal rules.
- **Launch and cost** — higher-energy orbits need bigger rockets or longer transfers.

@tbl:orbitchoice gives typical choices.

Table: Typical orbit choices by mission type. {#tbl:orbitchoice}

| Mission | Typical orbit | Reason |
|---|---|---|
| High-resolution optical imaging | 400–700 km sun-synchronous (10:00–10:30 LTDN), increasingly VLEO 250–400 km | Short range for resolution; constant lighting |
| Radar imaging (SAR) | 500–700 km dawn–dusk sun-synchronous | Near-continuous sunlight for power; radar works day/night |
| Global weather (polar) | 800–850 km sun-synchronous, morning and afternoon planes | Full global coverage twice daily |
| Weather (regional, continuous) | GEO | Images every 30 s–10 min over a hemisphere |
| Ocean altimetry | 1 336 km, 66° (Jason, Sentinel-6); 890 km, 77.6° (SWOT) | Avoid sun-synchronous tidal aliasing; long-lived repeat tracks |
| Gravity mapping | 450–500 km polar, low-low formation (GRACE-FO) | Sensitivity to gravity anomalies |
| Broadband internet | 340–1 200 km LEO (constellations); GEO; MEO (O3b) | Low latency (LEO) or wide coverage per satellite (GEO) |
| Direct-to-device mobile | 500–700 km LEO; GEO for narrowband | Short range to tiny phone antennas |
| Navigation | 19 000–23 300 km MEO, GEO/IGSO for regional | Many satellites visible at once; stable orbits |
| Missile warning | GEO and HEO (Molniya-type), increasingly LEO/MEO layers | Continuous view of launch regions; polar coverage |
| Space science (astronomy) | LEO (Hubble), HEO (Chandra), Sun–Earth L2 (JWST, Euclid, Roman) | Cold, stable, unobstructed sky |
| Solar wind monitoring | Sun–Earth L1 | Upstream of Earth, ≈ 1 hour warning |
| Technology demos, education | 400–600 km (rideshare or ISS deployment) | Cheap launch, natural decay |

## Coverage Geometry

### Footprint and Elevation

What a satellite can see from altitude $h$ is described by four angles (@fig:geometry): the **elevation angle** $\varepsilon$ of the satellite above the local horizon of a ground point, the **nadir angle** $\eta$ at the satellite between the nadir and the ground point, the **Earth central angle** $\lambda$, and the slant range $\rho$. They are linked by

$$\sin\eta = \frac{R_\oplus}{R_\oplus + h}\cos\varepsilon, \qquad \lambda = 90° - \eta - \varepsilon, \qquad \rho = R_\oplus\frac{\sin\lambda}{\sin\eta}$$

and the area of the coverage circle is $A = 2\pi R_\oplus^2(1 - \cos\lambda)$.

![Coverage geometry of a satellite. The minimum elevation angle at which a terminal can use the satellite — limited by terrain, buildings, atmosphere and antenna design — sets the coverage radius.](figures/out/ch11_geometry.svg){#fig:geometry width=84%}

The **minimum elevation angle** is a key design parameter: 5–10° for ground stations with clear horizons; 25–40° for broadband user terminals (to avoid blockage and long atmospheric paths and to share spectrum with GEO systems); 10–20° for navigation. A higher minimum elevation shrinks the footprint, so more satellites are needed (@fig:footprint).

![Left: coverage radius on the ground versus altitude for four minimum elevation angles. Right: maximum duration of an overhead pass. LEO satellites are visible for minutes, MEO for hours, GEO continuously.](figures/out/ch11_footprint.svg){#fig:footprint width=100%}

::: example
**Worked example — how many minutes can a ground station talk to a 550 km satellite?**

For $h$ = 550 km and $\varepsilon$ = 10°: $\sin\eta = (6\,378/6\,928)\cos 10° = 0.9066$, so $\eta = 65.0°$ and $\lambda = 90 - 65.0 - 10 = 15.0°$. The coverage radius is $6\,378 \times 0.262 = 1\,670$ km. The satellite's angular rate is its mean motion, $n = 360°/95.6$ min = 3.77°/min, so an overhead pass lasts at most $2\times15.0/3.77 \approx 8.0$ minutes; passes that do not go directly overhead are shorter. A station sees such a satellite on 4–6 passes a day at mid-latitudes, but on almost every orbit from Svalbard if the orbit is polar.
:::

### Swath, Revisit and Repeat

For an Earth-observation satellite, the relevant footprint is the **swath** — the width of ground imaged as the satellite moves, set by the instrument field of view or, for agile satellites, by how far off-nadir it can point. Two different time measures are used:

- **Revisit time** — how often a given place *can* be observed (possibly at different angles). Agile pointing and constellations reduce revisit to hours or less.
- **Repeat cycle** — how long until the satellite passes over exactly the same ground track (Chapter 3), giving identical viewing geometry. Landsat 8 and 9 each repeat every 16 days; together they give 8-day coverage.

For a single sun-synchronous imager with swath $W$ at the equator, global coverage takes about $2\pi R_\oplus / (W \times N_{orbits/day})$ days: a 290 km swath (Sentinel-2) with 14.3 orbits per day covers the equator in about 10 days; two satellites halve this to 5 days. Revisit improves at higher latitudes, where ground tracks converge.

## Constellation Design

When one satellite is not enough — for continuous coverage, frequent revisit, more capacity or redundancy — engineers design **constellations**.

### Walker Constellations

The most widely used patterns were described by J. G. Walker in 1970–1984. A **Walker delta** constellation is written **i: T/P/F** — inclination, total number of satellites $T$, number of equally spaced orbital planes $P$ (with RAAN spaced 360°/P), and a phasing parameter $F$ (0 to P−1) that sets the relative position of satellites in adjacent planes (in units of 360°/T). GPS's original design is close to a 55°: 24/6/1 Walker; Galileo is a 56°: 24/3/1 Walker (plus spares). A **Walker star** (or polar, "street-of-coverage") constellation places planes over 180° of RAAN with near-polar inclination, so that adjacent planes overlap like streets; Iridium uses 66 active satellites in six planes at 86.4° (@fig:constellations).

![Two classic constellation geometries: a Walker delta MEO constellation like GPS, and a near-polar "street-of-coverage" constellation like Iridium.](figures/out/ch11_constellations.svg){#fig:constellations width=96%}

Other families include **Flower constellations** (satellites on identical repeating ground tracks), **elliptical constellations** that concentrate coverage over high latitudes (Molniya, Ellipso), and hybrid multi-orbit systems combining LEO, MEO and GEO (e.g., Eutelsat OneWeb with Eutelsat's GEO fleet; SES with O3b mPOWER and GEO; IRIS²).

### How Many Satellites?

The number of satellites needed for continuous global coverage falls rapidly with altitude because each satellite sees more of the Earth (@fig:satscov). Three GEO satellites cover everything except the polar caps; about 24 MEO satellites give global navigation (which needs at least four in view everywhere); 66 satellites at 780 km give Iridium global voice coverage. Broadband mega-constellations use far more satellites than coverage alone requires — thousands — because what limits them is **capacity**: each satellite can serve only so many users with its spectrum and beams, and users want high elevation angles and low latency.

![Approximate number of satellites needed for continuous single global coverage versus altitude, compared with real systems. Broadband constellations exceed the coverage requirement many times over to provide capacity.](figures/out/ch11_sats_coverage.svg){#fig:satscov width=88%}

The main constellation trade-offs are:

| Choice | Lower altitude | Higher altitude |
|---|---|---|
| Number of satellites | More | Fewer |
| Latency (round trip, user–satellite–gateway) | ≈ 20–40 ms in LEO | ≈ 125 ms in MEO, ≈ 500+ ms in GEO |
| Link budget, user terminal size | Better / smaller | Worse / larger |
| Satellite lifetime vs drag | Shorter (natural disposal) | Longer (must actively dispose) |
| Radiation | Lower | Higher (especially MEO) |
| Handover and tracking | Frequent (minutes) | Rare or none |
| Launch cost per satellite | Lower | Higher |
| Debris risk if satellites fail | Self-cleaning below ≈ 550 km | Persistent above ≈ 600 km |


### Deploying a Constellation: Plane Phasing

Placing satellites in many orbital planes is expensive if each plane needs its own launch. Constellation operators therefore exploit **differential nodal precession** (Chapter 3): because the J₂ precession rate depends on altitude, satellites from a single launch can wait at different "parking" altitudes, where their planes drift apart in RAAN at different rates, before raising themselves to the operational shell at the right moment (@fig:raanspread). A satellite parked 100 km below a 550 km shell drifts about 0.18° per day relative to it, so three months of waiting separates planes by about 15°. The cost is time rather than propellant — a trade that suits electric propulsion and mass-produced satellites.

![Relative RAAN drift between satellites parked below a 550 km, 53° shell and satellites already in it. Waiting at lower altitudes spreads orbital planes using Earth's oblateness instead of propellant.](figures/out/ch11_raan_spread.svg){#fig:raanspread width=84%}

Table: Key parameters of major satellite constellations (October 2026). {#tbl:constellations}

| Constellation | Operator | Service | Altitude / inclination | Satellites (in orbit / planned) | Mass per satellite | Notable features |
|---|---|---|---|---|---|---|
| Starlink | SpaceX (USA) | Broadband, D2C, government | ≈ 480–570 km; 33°–97.6° | ≈ 10 650 / 12 000 (Gen1) + Gen2 | ≈ 300 kg (V1.5), ≈ 800 kg (V2 Mini), ≈ 2 t (V3) | Laser mesh, argon Hall thrusters, Starship-launched V3 |
| Eutelsat OneWeb | Eutelsat (France/UK) | Enterprise broadband | 1 200 km, 87.9° | ≈ 650 / 648 + Gen2 | ≈ 150 kg | Bent-pipe Ku/Ka; GEO + LEO offering |
| Amazon Leo | Amazon (USA) | Broadband | 590–630 km, 33°–52° | ≈ 400 / 3 232 | ≈ 600 kg | Launches on five vehicle types |
| Qianfan | SSST (China) | Broadband | ≈ 800–1 000 km (first shells) | ≈ 220–240 / > 14 000 | ≈ 250–300 kg | Launched in batches of 18 on Long March 6A |
| Guowang | China SatNet | Broadband, government | ≈ 500–1 145 km | ≈ 200 / ≈ 13 000 | various | State-owned |
| Iridium NEXT | Iridium (USA) | Voice, data, IoT, PNT | 780 km, 86.4° | 66 active + spares | 860 kg | Cross-links; hosted ADS-B (Aireon) |
| Globalstar | Globalstar (USA) | Voice, data, Apple emergency SOS | 1 414 km, 52° | ≈ 25 active + new generation | ≈ 700 kg | Bent-pipe; new satellites from MDA |
| O3b mPOWER | SES (Luxembourg) | High-throughput MEO | 8 062 km, 0° | 13 | ≈ 1 700 kg | Thousands of steerable beams |
| AST SpaceMobile | AST (USA) | Direct-to-device | ≈ 520–700 km | 13 / ≈ 45 (2027) | ≈ 1.5–6 t | Giant phased arrays |
| SDA PWSA | US Space Development Agency | Military data transport, missile tracking | ≈ 1 000 km | 42 / ≈ 1 000 (all tranches) | ≈ 500–1 000 kg | Optical crosslinks, Link 16 |
| Planet (Dove/Pelican) | Planet Labs (USA) | Earth observation | ≈ 475–525 km SSO | ≈ 200 | 5 kg (Dove), ≈ 100–200 kg (Pelican) | Daily global imaging |
| Spire | Spire Global (USA) | RF data (AIS, ADS-B, GNSS-RO) | ≈ 400–600 km | ≈ 80–100 | ≈ 5 kg (3U) | GNSS radio occultation for weather |
| ICEYE | ICEYE (Finland) | SAR imaging | ≈ 550 km SSO | ≈ 50 | ≈ 90–130 kg | Largest SAR constellation |

## The Population of Earth Orbit

The orbital population in 2026 is dominated by a few altitude bands (@fig:althist). CelesTrak's public catalogue lists about **35 000 objects** in Earth orbit — 20 100 payloads (of which about 17 200 are operational), 12 500 debris fragments and 2 300 rocket bodies. More than half of all objects now lie between 450 and 600 km, where Starlink operates; a second, older concentration between 750 and 1 000 km contains sun-synchronous Earth-observation satellites, Iridium, and the long-lived debris from the 2007 Fengyun-1C test and the 2009 Iridium–Cosmos collision.

![Distribution of catalogued objects in Earth orbit by mean altitude, October 2026. Operational payloads (blue) cluster in constellation shells; debris (grey) dominates the 700–1 000 km region.](figures/out/ch11_alt_hist.svg){#fig:althist width=92%}

## Mega-Constellations

### Starlink

SpaceX's **Starlink** is the largest satellite system ever built. Its first operational satellites launched in May 2019; by October 2026 more than 10 600 were in orbit, serving more than 8 million subscribers in over 140 countries and territories with broadband, maritime, aviation and mobile ("Direct to Cell") services. Key engineering features include:

- **Mass production** — satellites are built at rates of several per day in Redmond, Washington, and launched in batches of 21–29 (V2 Mini) on Falcon 9 or, from September 2026, in larger batches of the much bigger **V3** satellites on Starship.
- **Flat-pack design** — satellites stack in the fairing without a dispenser; a single solar array per satellite on V1/V1.5, two on V2 Mini.
- **Electric propulsion** — krypton (V1) and argon (V2 Mini) Hall thrusters for orbit raising, station-keeping, collision avoidance and de-orbit.
- **Phased-array antennas** for Ku- and Ka-band user and gateway links and E-band backhaul; **laser inter-satellite links** (three or more per satellite) forming a mesh network that routes traffic across oceans and polar regions.
- **Autonomous collision avoidance** — satellites manoeuvre automatically using conjunction data; SpaceX reports tens of thousands of avoidance manoeuvres per half-year (Chapter 21).
- **Low orbits** for natural disposal: SpaceX began lowering about 4 400 satellites from about 550 km to about 480 km during 2026, citing lower debris density and much faster decay of failed satellites.

The US government uses a derivative, **Starshield**, for national-security applications, including a proliferated reconnaissance constellation for the National Reconnaissance Office.

### Other Broadband Constellations

- **Eutelsat OneWeb** — about 650 satellites at 1 200 km in 12 near-polar planes, serving enterprise, government, aviation and maritime customers through partners; second-generation satellites are being procured.
- **Amazon Leo** (formerly Project Kuiper) — authorised for 3 232 satellites in three shells at 590–630 km; about 400 were in orbit by mid-2026 after launches on Atlas V, Falcon 9, Vulcan, Ariane 6 and New Glenn; beta service was planned for autumn 2026. The FCC waived its July 2026 half-constellation milestone.
- **Qianfan / "Thousand Sails"** (Shanghai Spacecom Satellite Technology) — planned to exceed 14 000 satellites; about 220–240 launched by mid/late 2026.
- **Guowang** (China Satellite Network Group, "SatNet") — a state constellation of about 13 000 satellites; about 200 launched by September 2026.
- **Telesat Lightspeed** — 198 advanced satellites with optical links planned for enterprise and government service from the late 2020s.
- **IRIS²** — the EU's secure multi-orbit constellation (SpaceRISE consortium of SES, Eutelsat and Hispasat): under an August 2026 agreement, 330 LEO and 18 MEO satellites plus 66 dedicated government satellites, with first launches planned for 2029.
- **AST SpaceMobile** — very large (up to ≈ 220 m² phased-array) "BlueBird" satellites that connect directly to unmodified phones; 13 in orbit by August 2026, with about 45 targeted by early 2027 (Chapter 17).

![Mega-constellations: satellites in orbit (coloured) compared with first-generation plans or authorisations (grey), October 2026.](figures/out/ch11_mega.svg){#fig:mega width=94%}

![Altitudes and inclinations of representative constellation shells. Shells at different inclinations concentrate capacity where most users live (mid-latitudes) while polar shells cover high latitudes.](figures/out/ch11_shells.svg){#fig:shells width=86%}

### Military Proliferated Constellations

The US **Space Development Agency (SDA)** is deploying the **Proliferated Warfighter Space Architecture** — hundreds of relatively low-cost satellites in LEO in successive "tranches" every two years: a **Transport Layer** of data-relay satellites with optical crosslinks and Link 16 tactical radios, and a **Tracking Layer** of infrared satellites that detect and track missiles (Chapter 20). Tranche 1 launches began in September 2025. China, Europe and others are pursuing similar concepts, reflecting a shift from a few exquisite satellites to resilient proliferated architectures.

## The Geostationary Orbit

### A Unique Resource

A satellite at 35 786 km altitude above the equator, moving eastward with a period of one sidereal day, appears fixed in the sky. Antennas on the ground need not track it, and three satellites cover most of the populated Earth. The **geostationary arc** is therefore a limited natural resource, shared through ITU coordination: satellites are assigned **orbital slots** (longitudes), typically spaced 2–3° for the same frequency bands, and must stay within a **station-keeping box** of about ±0.05–0.1° in longitude and latitude. About 1 340 payloads are in GEO-type orbits, of which roughly 600–650 are operational.

Natural forces push GEO satellites out of their boxes: the Sun and Moon tilt the orbit by about 0.8° per year (north–south drift), the ellipticity of Earth's equator causes east–west drift towards stable points near 75° E and 105° W, and solar radiation pressure changes the eccentricity. Station-keeping requires about 50 m/s per year (Chapter 3). At end of life, operators must raise their satellites at least 235 km plus a margin depending on area-to-mass ratio above GEO into a **graveyard orbit** (IADC guideline). Some operators extend life by allowing inclination to grow ("inclined-orbit operation") or by using life-extension servicers (Chapter 40).

### Eclipses and Sun Interference

GEO satellites experience eclipses only around the equinoxes (up to 72 minutes per day for about 45 days in each season). Around the equinoxes, the Sun also passes directly behind satellites as seen from ground antennas, causing **Sun outages** of a few minutes per day due to solar noise.

### Trends in GEO

GEO remains the workhorse for broadcasting and many government services but faces competition from LEO broadband. Trends include **software-defined, reconfigurable payloads** that can change coverage and frequency plans in orbit (Airbus OneSat, Thales Inspire, Boeing 702X), **all-electric propulsion**, **smaller GEO satellites** (Astranis MicroGEO, about 400 kg), and **in-orbit servicing** to extend life.

## Small Satellites and the CubeSat Revolution

### Why Small?

"Small satellites" (below about 500 kg) have transformed the industry by trading individual capability for speed, cost and numbers. Their enablers were: commercial electronics (processors, cameras, radios) that became small, capable and cheap; standardised interfaces and deployers; inexpensive rideshare launch; and a culture of rapid iteration ("fail fast"). @fig:massclasses shows how launches have shifted over the past 15 years — first towards very small satellites, then towards mass-produced constellation satellites in the 100–2 500 kg range.

![Payloads launched per year by launch mass, 2010–2025 (GCAT). The explosion after 2019 is driven by mass-produced constellation satellites; CubeSats (< 10 kg) continue at several hundred per year.](figures/out/ch11_mass_classes.svg){#fig:massclasses width=92%}

### The CubeSat Standard

The **CubeSat** was proposed in 1999 by Jordi Puig-Suari (California Polytechnic State University) and Bob Twiggs (Stanford) as a standard for student satellites: a 10 cm cube ("1U") of up to about 2 kg, launched from a standard spring-loaded box deployer (the P-POD and its successors) that protects the launch vehicle and primary payload. Larger formats stack units: 3U, 6U, 12U and 16U are now the most common (@fig:cubesats). The standard's genius is that it decouples the satellite from the launcher: any CubeSat fits any compatible deployer on any rocket or on the ISS.

![Common CubeSat form factors and approximate maximum masses.](figures/out/ch11_cubesats.svg){#fig:cubesats width=96%}

A thriving commercial supply chain now sells CubeSat buses and components "off the shelf": structures, solar panels, batteries and power units, reaction wheels and star trackers, flight computers running Linux or FreeRTOS, S- and X-band radios, and even electric thrusters. A 6U Earth-observation CubeSat can be built and launched for a few million dollars in under two years.

### What Small Satellites Do

- **Earth observation** — Planet's fleet of about 200 "Dove" and "SuperDove" 3U CubeSats images the entire land surface daily at 3–5 m resolution; larger SkySats and Pelican satellites offer 50 cm imaging.
- **Radio-frequency data** — Spire's Lemur CubeSats collect GNSS radio-occultation weather data, ship AIS and aircraft ADS-B signals; HawkEye 360 geolocates RF emitters (Chapter 19).
- **Radar** — ICEYE, Capella and Umbra fly 50–150 kg SAR microsatellites (Chapter 15).
- **Science** — NASA's TROPICS CubeSats measure tropical-cyclone microwave signatures every hour; GRACE-like and space-weather missions use CubeSat swarms.
- **Deep space** — NASA's twin **MarCO** CubeSats relayed InSight's landing data from Mars in 2018 — the first CubeSats beyond Earth orbit; ten CubeSats rode on Artemis I to the Moon (2022), and CAPSTONE pioneered the Gateway's NRHO.
- **Technology demonstration and education** — thousands of students worldwide have built CubeSats; the ISS deploys many of them.

::: figrow
![JPL engineers with one of the twin MarCO 6U CubeSats, which flew alongside InSight to Mars in 2018 and relayed its landing data in real time.](figures/photos/ch11_marco.jpg){#fig:marco}

![NASA astronaut Frank Rubio installs a NanoRacks CubeSat Deployer in the ISS Kibo airlock (2023). Deployers are passed outside through the airlock and the station's robotic arm releases the CubeSats.](figures/photos/ch11_nanoracks.jpg){#fig:nanoracks}
:::

### Reliability of Small Satellites

Early CubeSats had high failure rates — studies of missions launched up to the mid-2010s found that roughly 20–40 % failed early in their missions, often due to power, communications or deployment failures, with university "first missions" faring worst. Reliability has improved greatly with commercial heritage hardware, more thorough testing ("flatsat" functional testing, thermal-vacuum and vibration) and better operations. Commercial constellations accept some individual failures because the system degrades gracefully; science and defence small satellites adopt selected high-reliability practices ("Class D" risk posture, Chapter 4).


## Launch and Early Operations

The first days after launch — the **launch and early orbit phase (LEOP)** — are the riskiest of a satellite's life. A typical LEO satellite's LEOP sequence is:

1. **Separation** from the launch vehicle; the spacecraft wakes on a separation switch, powers essential units and starts timers.
2. **Detumbling** — rates from separation (up to a few degrees per second) are damped using magnetorquers ("B-dot" control) or thrusters.
3. **Sun acquisition** — solar arrays are deployed (if folded) and pointed at the Sun to make the spacecraft power-positive.
4. **First contact** — ground stations around the world, often including commercial network stations, search for the beacon. Orbit determination from the launcher's injection data and early ranging refines the orbit; for rideshare launches, operators must first identify which of dozens of newly catalogued objects is theirs.
5. **Deployments** — antennas, booms, radiator covers and instrument doors are released.
6. **Commissioning** — each subsystem and the payload are switched on and verified; propulsion is tested with small burns; the satellite is manoeuvred to its operational orbit.
7. **Calibration and validation** of the payload, typically lasting weeks (communications) to months (science instruments), before the satellite enters routine operations.

## Orbit Maintenance

Satellites in LEO must counter drag to stay in their slots; constellations must also maintain their relative phasing. The velocity lost to drag each year is the integral of the drag deceleration over the year:

$$\Delta v_{year} = \int_{1\,\text{yr}} \frac{\rho\,v^2}{2B}\,dt \;\approx\; \frac{\rho\,v^2}{2B}\times 3.16\times10^{7}\ \text{s}$$

At 550 km with moderate solar activity ($\rho \approx 5\times10^{-13}$ kg/m³, $v$ = 7.6 km/s) and $B$ = 50 kg/m², the drag deceleration is $5\times10^{-13}\times(7\,600)^2/100 \approx 2.9\times10^{-7}$ m/s², or about **9 m/s per year**; at 400 km and solar maximum it can exceed 100 m/s per year.

## A Worked Small-Satellite Design

To see how the material of Part I comes together, consider the preliminary design of a 12U CubeSat for agricultural monitoring.

**Requirements.** Multispectral images (blue, green, red, red-edge, near-infrared) at 5 m ground sampling distance (GSD) over Europe, revisit ≤ 5 days with a constellation, 3-year life, launch on a rideshare to SSO.

**Orbit.** 525 km sun-synchronous (97.5°), 10:30 local time. Lifetime analysis (Chapter 2) gives 6–15 years for a 12U CubeSat with deployed panels, so a small thruster for collision avoidance and end-of-life lowering is advisable to meet the 5-year disposal rule with margin.

**Payload optics.** GSD = altitude × pixel pitch / focal length. With 5.5 µm pixels: $f = 525\,000 \times 5.5\times10^{-6} / 5 = 0.58$ m. A 9 cm-aperture compact catadioptric telescope with a 580 mm focal length fits in about 4U; at f/6.4 the diffraction limit at 800 nm ($2.44\lambda N \approx 12.5$ µm spot diameter) is acceptable for 5 m GSD with some MTF loss. A 4 096-pixel line array gives a 20 km swath.

**Data budget.** Imaging Europe's croplands ≈ 2 million km² per 5 days per satellite with 5 bands × 12 bits at 5 m: $2\times10^{6}\,\text{km}^2 / 5\ \text{days} \times (10^6/25)\ \text{pixels/km}^2 \times 60\ \text{bits} \approx 1\times10^{12}$ bits/day ≈ 1 Tbit/day before compression. With 3:1 compression and onboard cloud screening (Chapter 45) removing about half, the downlink requirement is ≈ 170 Gbit/day. An X-band transmitter at 200 Mbit/s needs about 14 minutes of contact per day — two or three passes over a high-latitude station.

**Power budget.**

| Mode | Power (W) | Duty / orbit | Energy per orbit (Wh) |
|---|---|---|---|
| Platform (OBC, ADCS, receivers, heaters) | 12 | 100 % | 19.1 |
| Imaging (payload + ADCS fine pointing) | 25 | 10 % | 4.0 |
| X-band downlink | 30 | 7 % | 3.3 |
| Total | — | — | ≈ 26.4 per 95.3-min orbit |

Deployable panels with triple-junction cells (≈ 80 W peak, ≈ 45 W orbit-average after pointing losses) give a positive balance with 30 % margin; a 90 Wh Li-ion battery supports eclipse at < 20 % depth of discharge.

**Mass budget.**

| Item | Mass (kg) |
|---|---|
| Structure and deployers | 3.2 |
| Payload telescope and focal-plane electronics | 5.5 |
| Power (panels, battery, EPS) | 3.0 |
| ADCS (3 wheels, star tracker, magnetorquers, sensors) | 1.6 |
| OBC and payload processor (with AI accelerator) | 0.6 |
| S-band TT&C and X-band transmitter with patch array | 0.9 |
| Propulsion (electrospray or cold gas) | 1.2 |
| Harness, thermal hardware | 0.8 |
| **Subtotal** | **16.8** |
| Margin (25 %) | 4.2 |
| **Total (12U limit ≈ 24 kg)** | **21.0** |

**Constellation.** With a 20 km swath, one satellite cannot meet a 5-day revisit over Europe by nadir imaging alone; ±20° off-nadir pointing gives an accessible swath of about 400 km, so a constellation of four to six satellites in one or two planes meets the requirement. This example illustrates how requirements cascade through optics, data, power, mass and constellation size — the essence of systems engineering (Chapter 4).

## Getting Small Satellites to Orbit

### Rideshare

Most small satellites fly as **secondary payloads** sharing a launch with others. SpaceX's **Transporter** (sun-synchronous) and **Bandwagon** (mid-inclination) missions carry 50–120 satellites per flight from many customers; ISRO's PSLV, Rocket Lab's Electron, Arianespace's Vega-C (SSMS dispenser) and China's Long March and commercial rockets offer similar services. Rideshare is cheap (≈ US$6 000–7 000 per kg on Transporter in 2025) but the customer does not choose the orbit or the date. **Dedicated small launchers** (Electron, Firefly Alpha, Kinetica-1, Ceres-1, Zhuque-2, Vega-C, PSLV, SSLV) provide orbit and schedule control at higher cost per kilogram (Chapter 36).

### Orbital Transfer Vehicles

**Orbital transfer vehicles (OTVs)** or "space tugs" bridge the gap: they ride a rideshare launch, then carry their satellite passengers to individual orbits or planes. Examples include D-Orbit's ION Satellite Carrier (more than 15 missions since 2020), Exotrail's spacevan, Momentus' Vigoride, Impulse Space's Mira, Rocket Lab's Photon and Firefly's Elytra. Some OTVs also host experiments and are evolving into servicing vehicles.

### Deployment from the ISS

The ISS has deployed hundreds of CubeSats through the Japanese **J-SSOD** and commercial NanoRacks deployers in the Kibo module airlock. ISS-deployed satellites start at about 410 km and decay within one to three years — an advantage for debris mitigation.

## Formation Flying and Swarms

Some missions require two or more satellites to fly in a controlled geometry:

- **GRACE and GRACE-FO** (US–Germany) — two satellites 220 km apart in the same orbit measure their separation to micrometres (GRACE-FO adds a laser ranging interferometer at nanometre precision) to map changes in Earth's gravity from melting ice, groundwater and ocean mass.
- **TanDEM-X** (Germany) — two radar satellites flying in a close "helix" formation a few hundred metres apart acted as a single-pass interferometer to produce a global digital elevation model (Chapter 15).
- **PROBA-3** (ESA, launched December 2024) — two satellites flying about 150 m apart in a highly elliptical orbit, one acting as an occulting disc for the other's coronagraph to create artificial solar eclipses, with millimetre-level relative positioning; it produced its first artificial-eclipse images of the solar corona in 2025.
- **MMS** (NASA) — four spacecraft in a tetrahedral formation measuring magnetic reconnection (Chapter 23).
- **Starling** (NASA, 2023) — four CubeSats demonstrating autonomous swarm manoeuvre planning and relative navigation.

![Illustration of NASA's Starling mission: four CubeSats flying as an autonomous swarm in low Earth orbit (2023–2024).](figures/photos/ch11_starling.jpg){#fig:starling width=72%}

Formation flying requires precise relative navigation (carrier-phase differential GNSS, inter-satellite radio or optical ranging, vision sensors) and control using small thrusters or differential drag. Future concepts include distributed-aperture telescopes and interferometers, synthetic-aperture radar clusters, and gravitational-wave observatories (LISA, Chapter 39).

## Operating Large Constellations

Operating thousands of satellites is impossible with traditional mission control, where a team watches each spacecraft. Constellation operators rely on:

- **Automation** — automated planning and scheduling of ground contacts, autonomous orbit maintenance and collision avoidance, automated anomaly detection and recovery; humans manage by exception.
- **Fleet management** — configuration management of thousands of identical vehicles, software updates over the air, health trending with machine learning (Chapter 49).
- **Ground networks** — hundreds of gateways (Starlink operates more than 150 gateway sites) and cloud-based processing.
- **Replenishment** — continuous launches to replace satellites that reach end of life (typically after five years in LEO) and to upgrade technology.
- **Space traffic coordination** — sharing ephemerides and manoeuvre plans with other operators and with space-surveillance organisations (Chapter 21).

## Sustainability, Regulation and the Night Sky

The rapid growth of constellations raises four sustainability issues:

1. **Orbital debris and collision risk.** Large numbers of satellites increase conjunctions. Mitigation measures include low operating altitudes, reliable propulsion, prompt disposal (the US FCC requires LEO satellites ending their missions to deorbit within **5 years**, adopted in 2022, replacing the older 25-year guideline), high post-mission disposal reliability (> 90–99 %) and design for demise (Chapter 21).
2. **Spectrum.** The ITU requires non-geostationary systems to deploy **10 % of their filed satellites within 2 years**, **50 % within 5 years** and **100 % within 7 years** after the end of the regulatory period (rules adopted at WRC-19) to keep their priority — driving the "race" to launch. Interference with GEO systems is limited by equivalent power-flux-density (EPFD) rules.
3. **Astronomy.** Sunlit satellites appear as moving streaks in telescope images, particularly in twilight and in wide-field surveys such as the Vera C. Rubin Observatory's Legacy Survey of Space and Time. Operators have reduced brightness with dark coatings, visors and attitude changes, and the International Astronomical Union's Centre for the Protection of the Dark and Quiet Sky coordinates mitigation. Unintended radio emissions from satellite electronics also affect radio astronomy.
4. **Atmosphere.** Re-entering satellites (several per day from large constellations) deposit aluminium oxide and other materials in the upper atmosphere, with possible effects on ozone chemistry that are under study.

::: key
**Key takeaways**

- Orbit choice sets coverage, revisit, resolution, latency, environment and cost; coverage geometry links altitude, minimum elevation and footprint.
- Walker delta and polar "street-of-coverage" constellations are the classic designs; broadband constellations need thousands of satellites for capacity, not just coverage.
- In October 2026 about 35 000 objects were catalogued in Earth orbit (≈ 17 200 operational payloads); more than half of all objects orbit between 450 and 600 km, dominated by Starlink (> 10 600 satellites).
- Mega-constellations (Starlink, OneWeb, Amazon Leo, Qianfan, Guowang, IRIS², SDA layers) are reshaping the industry and the orbital environment.
- GEO is a limited resource managed through ITU slots and station-keeping boxes, now evolving towards software-defined and smaller satellites.
- CubeSats and small satellites, rideshare launches and orbital transfer vehicles made space accessible to universities, start-ups and new nations; sustainability rules (5-year disposal, ITU milestones, brightness mitigation) are evolving with them.
:::

::: questions
**Review questions**

1. List six mission characteristics that depend on the choice of orbit.
2. A satellite at 550 km altitude serves users down to 25° elevation. Calculate the Earth central angle and the ground radius of its coverage circle.
3. Explain Walker delta notation *i*: *T*/*P*/*F*, using a GNSS constellation as an example.
4. Why do broadband constellations need thousands of satellites when a few dozen could cover the whole Earth?
5. How are satellites launched into one plane redistributed into several planes without large plane-change manoeuvres?
6. When do geostationary satellites experience eclipses, and how long can an eclipse last?
7. What features of the CubeSat standard made small satellites affordable? What are the main reliability concerns?
8. Describe three rules or practices that aim to keep low Earth orbit sustainable and limit the effect of constellations on astronomy.
:::
