---
title: Global Navigation Satellite Systems
hero: ch18
abstract: Global navigation satellite systems (GNSS) — GPS, GLONASS, Galileo and BeiDou, with regional systems in Japan and India — broadcast precisely timed radio signals from atomic clocks in orbit, allowing billions of receivers to determine their position, velocity and time anywhere on Earth. This chapter explains how satellite navigation works: one-way ranging, pseudoranges and the navigation solution; spread-spectrum signals and receivers; atomic clocks and relativity; the error budget and satellite geometry; and the augmentation techniques that improve accuracy from metres to centimetres. It describes the four global systems as they stand in 2026, the enormous range of applications that depend on them — including the timing of telecom networks, power grids and financial markets — and their vulnerability to interference, jamming and spoofing, which has grown into a serious problem. It ends with the next generation of satellites and with navigation in low Earth orbit and on the Moon.
---

## Positioning, Navigation and Timing

Satellite navigation is one of the most pervasive technologies ever created. In 2026 there are roughly seven billion GNSS receivers in use — in phones, vehicles, aircraft, ships, tractors, drones, watches, survey instruments and the timing equipment of telecommunications networks, power grids and stock exchanges. Most users think of GNSS as a way to find their position, but its three outputs — **positioning, navigation and timing (PNT)** — are equally important. Precise time from GNSS synchronises mobile-phone base stations, time-stamps financial transactions and aligns measurements across electricity grids; a study for the US government estimated that GPS alone generated about $1.4 trillion in economic benefits in the USA between its opening to civil use in the 1980s and 2017.

### A Short History

The idea grew from the space race. When Sputnik was launched in 1957, scientists at the Johns Hopkins Applied Physics Laboratory found that they could determine its orbit from the Doppler shift of its radio signal — and realised that, conversely, a receiver could determine its own position from the Doppler shift of a satellite in a known orbit. The resulting US Navy **Transit** system (first satellite 1960, operational 1964) allowed submarines to fix their position every hour or so. Experiments with atomic clocks in orbit (Timation) and the Air Force's 621B programme led in 1973 to the decision to build the **NAVSTAR Global Positioning System**. The first GPS satellite was launched in 1978 and the system was declared fully operational in 1995. The Soviet Union developed the similar **GLONASS** from 1982.

GPS was opened to civil users in the 1980s, but its civil signal was deliberately degraded by "Selective Availability" to about 100 m accuracy until it was switched off in May 2000, instantly improving accuracy tenfold and unleashing the consumer navigation industry. Other powers then built their own systems for strategic independence: China's **BeiDou** (regional from 2012, global in 2020), Europe's civilian **Galileo** (initial services in 2016), Japan's regional **QZSS** and India's regional **NavIC** (@fig:gnsshistory).

![Milestones in satellite navigation.](figures/out/ch18_history.svg){#fig:gnsshistory width=100%}

## How Satellite Navigation Works

### One-Way Ranging and Pseudoranges

Each GNSS satellite carries atomic clocks and continuously broadcasts radio signals that contain its precise time and its position (ephemeris). A receiver measures when each signal arrives; the difference between the time of reception and the time of transmission, multiplied by the speed of light, is the distance (range) to the satellite. With ranges to three satellites at known positions, the receiver's position could be found by **trilateration** — the intersection of three spheres (@fig:trilat).

The difficulty is that the receiver's own clock — a cheap quartz oscillator — is not synchronised with the satellites' atomic clocks. An error of just one microsecond would cause a range error of 300 m. The measured ranges, which include this unknown clock offset, are therefore called **pseudoranges**:

$$\rho_i = \sqrt{(x_i - x)^2 + (y_i - y)^2 + (z_i - z)^2} + c\,\delta t + \varepsilon_i$$

where $(x_i, y_i, z_i)$ is the position of satellite $i$, $(x, y, z)$ the receiver position, $\delta t$ the receiver clock offset and $\varepsilon_i$ the remaining errors. Because the clock offset is common to all measurements, it can be solved as a fourth unknown: **four satellites** are needed to determine three position coordinates and time. In practice receivers track 10–40 satellites from several constellations and solve the over-determined system by iterative least squares or, for continuous navigation, by a Kalman filter. As a by-product, every GNSS receiver becomes a clock synchronised to the system time within tens of nanoseconds. Velocity is found in a similar way from the Doppler shifts of the signals.

![Trilateration. With perfect clocks, ranges from three satellites intersect at the user's position (left). A receiver clock error changes all ranges by the same amount, so the circles no longer meet (right) — the error is solved for using a fourth satellite.](figures/out/ch18_trilat.svg){#fig:trilat width=94%}

### Spread-Spectrum Signals

GNSS signals are extraordinarily weak. A GPS L1 signal arrives at the Earth's surface with a minimum power of about −128.5 dBm (1.4 × 10⁻¹⁶ W) — roughly the brightness of a 25 W light bulb seen from 20 000 km, and well **below** the thermal noise in the receiver's bandwidth. Receivers can nevertheless detect them because the signals use **direct-sequence spread spectrum**: the navigation data are multiplied by a fast **pseudo-random noise (PRN) code** that spreads the signal over a wide bandwidth. The receiver generates a replica of each satellite's code and correlates it with the incoming signal; only when the replica is aligned with the received code does a strong correlation peak appear (@fig:correlation). Correlating over 1–20 ms or more provides a **processing gain** of 30–45 dB that lifts the signal out of the noise.

Each satellite uses a different code chosen to have low **cross-correlation** with the others, so all satellites can transmit on the same frequency without interfering — **code division multiple access (CDMA)**. The GPS **coarse/acquisition (C/A) code**, for example, is a Gold code of 1 023 chips transmitted at 1.023 million chips per second, repeating every millisecond. The timing of the correlation peak, refined by tracking loops to a small fraction of a chip, gives the pseudorange; the phase of the carrier wave (wavelength 19 cm at L1) can be measured even more precisely, to about a millimetre.

![Correlation properties of the GPS C/A code, computed from the generators in the GPS interface specification. The autocorrelation has a single sharp peak of 1 023 at zero offset; sidelobes and cross-correlations with other satellites' codes take only the values −65, −1 and +63.](figures/out/ch18_correlation.svg){#fig:correlation width=98%}

### Receivers

A GNSS receiver consists of an antenna (typically right-hand circularly polarised), a radio-frequency front end that amplifies, filters and down-converts the signals and digitises them, and a baseband processor with many **correlator channels**. **Acquisition** searches over all possible code delays and Doppler shifts for each satellite — a two-dimensional search that modern receivers perform in parallel using FFTs, taking from about a second (with assistance data from the mobile network) to a minute (cold start). **Tracking** then follows each signal with a delay-locked loop for the code and a phase- or frequency-locked loop for the carrier, while the navigation message is decoded. A smartphone GNSS chip, which tracks four constellations on two frequencies, costs about a dollar and consumes tens of milliwatts.

### Signals of the Four Global Systems

All four global systems now broadcast multiple civil signals in the radio-navigation bands around 1.2 and 1.575 GHz, which are protected for aeronautical safety use (@fig:gnsssignals). Newer signals share common centre frequencies — 1575.42 MHz (GPS L1C, Galileo E1, BeiDou B1C) and 1176.45 MHz (GPS L5, Galileo E5a, BeiDou B2a) — so that a single dual-frequency receiver can use all of them. Some use **binary offset carrier (BOC)** modulation, which splits the signal's power away from the band centre, improving tracking precision and reducing interference with older signals.

![Simplified frequency plan of the four global navigation systems.](figures/out/ch18_signals.svg){#fig:gnsssignals width=100%}

| System | Signal | Centre frequency (MHz) | Modulation | Use |
|---|---|---|---|---|
| GPS | L1 C/A | 1575.42 | BPSK(1) | Legacy civil signal, used by almost every receiver |
| GPS | L1C | 1575.42 | TMBOC(6,1,1/11) | Modern civil, interoperable with Galileo E1 and BeiDou B1C (GPS III) |
| GPS | L2C | 1227.60 | BPSK(1) time-multiplexed | Second civil frequency (since 2005) |
| GPS | L5 | 1176.45 | BPSK(10) | Safety-of-life civil signal (since 2010) |
| GPS | P(Y), M-code | 1575.42, 1227.60 | BPSK(10), BOC(10,5) | Military, encrypted |
| Galileo | E1 OS | 1575.42 | CBOC(6,1,1/11) | Open service; carries OSNMA authentication |
| Galileo | E5a, E5b | 1176.45, 1207.14 | AltBOC(15,10) combined | Open service; E5b also for integrity |
| Galileo | E6 | 1278.75 | BPSK(5) | High-Accuracy Service; Public Regulated Service (encrypted) |
| BeiDou | B1I, B1C | 1561.098, 1575.42 | BPSK(2), MBOC | Open service |
| BeiDou | B2a, B2b | 1176.45, 1207.14 | QPSK(10) | Open service; B2b carries PPP corrections |
| BeiDou | B3I | 1268.52 | BPSK(10) | Open and authorised services |
| GLONASS | L1OF, L2OF | 1602 + k·0.5625, 1246 + k·0.4375 | FDMA, BPSK(0.511) | Legacy open signals, one frequency channel per satellite pair |
| GLONASS | L3OC | 1202.025 | CDMA | New CDMA signal (GLONASS-K) |

: Principal signals of the global navigation satellite systems (simplified). {#tbl:gnsssignals}

## The Systems in 2026

### Space Segments

| System | Operator | Nominal constellation | MEO orbit | Other orbits | Clocks | Status (Oct 2026) |
|---|---|---|---|---|---|---|
| GPS (USA) | US Space Force | 24 slots (≈ 31 operational) | 20 180 km, 55°, 6 planes | — | Rubidium, caesium | Operational since 1995; ten GPS III launched 2018–2026; GPS IIIF from ≈ 2027 |
| GLONASS (Russia) | Roscosmos / Ministry of Defence | 24 | 19 100 km, 64.8°, 3 planes | — | Caesium, rubidium | Operational; transition to GLONASS-K/K2 with CDMA signals |
| Galileo (EU) | EU / EUSPA, ESA | 24 + spares | 23 222 km, 56°, 3 planes | — | Passive hydrogen maser, rubidium | Initial services since 2016; ≈ 30 satellites usable after the December 2025 launch; second generation from 2026–27 |
| BeiDou-3 (China) | China Satellite Navigation Office | 24 MEO + 3 IGSO + 3 GEO | 21 528 km, 55°, 3 planes | GEO and inclined GEO over Asia | Rubidium, hydrogen maser | Global service since 2020; legacy BeiDou-2 satellites still in use |
| QZSS (Japan) | Cabinet Office | 7 (growing to 11) | — | Quasi-zenith (inclined, elliptical GEO) and GEO | Rubidium | Six satellites by October 2026 |
| NavIC (India) | ISRO | 7 | — | GEO and IGSO over India | Rubidium | Several clock failures; NVS-series replacements, one (NVS-02) stranded in transfer orbit in 2025 |

: The world's satellite navigation systems in 2026. {#tbl:gnsssystems}

The global systems use medium Earth orbits at 19 000–23 000 km (@fig:gnssorbits), a compromise between coverage (each satellite sees about 38 % of the Earth) and the number of satellites needed: about 24 satellites give at least four visible everywhere at all times. GLONASS uses a higher inclination (64.8°) for better coverage of Russia's northern latitudes. BeiDou and the regional systems add satellites in geostationary and **inclined geosynchronous (IGSO)** orbits, which trace figure-of-eight ground tracks and remain over their service regions; Japan's quasi-zenith satellites are designed to stay at high elevation over Japan, so that their signals are not blocked by tall buildings and mountains.

![Altitude and inclination of active navigation satellites in October 2026. Each global system occupies a distinct MEO shell; BeiDou, QZSS and NavIC also use geostationary and inclined geosynchronous orbits.](figures/out/ch18_orbits.svg){#fig:gnssorbits width=88%}

![A Delta II rocket ready to launch the 19th NAVSTAR GPS satellite from Cape Canaveral in 1993. Delta II rockets launched most GPS satellites from 1989 to 2009.](figures/photos/ch18_navstar.jpg){#fig:navstarlaunch width=42%}

### Atomic Clocks and Time

The precision of GNSS rests on atomic clocks. GPS satellites carry rubidium and caesium frequency standards; Galileo satellites carry two rubidium clocks and two **passive hydrogen masers**, the most stable clocks flying in navigation satellites, with a stability of better than one part in 10¹⁴ over a day; BeiDou-3 also carries hydrogen masers. A clock error of 1 ns produces a range error of 30 cm, so the clocks must be extremely stable between updates from the ground. Each system maintains its own **system time** (GPS Time, Galileo System Time, BeiDou Time, GLONASS Time), steered to Coordinated Universal Time (UTC) and broadcast with the offsets between them, so that receivers can combine all systems. NASA's **Deep Space Atomic Clock** (the opening image of this chapter), a mercury-ion clock flown in 2019–2021, demonstrated stability good enough for spacecraft to navigate autonomously in deep space.

### Relativity in Daily Life

GNSS is the most familiar practical application of Einstein's theories of relativity (@fig:relativity). A clock in a GPS orbit runs **faster** than a clock on the ground by about 45.7 µs per day because it sits higher in the Earth's gravitational field (general relativity), and **slower** by about 7.2 µs per day because of its orbital speed (special relativity). The net effect is +38.5 µs per day — which, left uncorrected, would cause range errors growing by about 11 km per day. GPS satellite clocks are therefore deliberately set to run slow by 4.465 parts in 10¹⁰ before launch, and receivers apply a further small correction for orbital eccentricity.

![Relativistic clock-rate offsets of orbiting clocks relative to a clock on the ground. Above about 3 000 km the gravitational effect dominates and orbiting clocks gain time.](figures/out/ch18_relativity.svg){#fig:relativity width=86%}

### Control Segments

Each system has a control segment of monitor stations around the world that track the satellites, master control stations that compute orbit and clock predictions, and uplink antennas that upload them to the satellites for broadcast. The GPS master control station at Schriever Space Force Base in Colorado updates each satellite's navigation message at least daily. The modernised GPS ground system, **OCX**, needed to exploit the new civil and military signals fully, suffered years of delays and cost growth; Galileo's ground segment includes control centres in Germany and Italy and a worldwide network of sensor stations.

## Accuracy

### The Error Budget

The accuracy of a GNSS position depends on the errors in each pseudorange — summarised as the **user equivalent range error (UERE)** — and on the geometry of the satellites. The main error sources are (@fig:gnsserrors):

- **Satellite clock and orbit errors**: the broadcast predictions are not perfect. The GPS signal-in-space range error has improved to about 0.5 m (RMS) in recent years, and Galileo's to about 0.2 m.
- **Ionospheric delay**: free electrons in the ionosphere (50–1 000 km) delay the signal by an amount proportional to the **total electron content (TEC)** along the path and inversely proportional to the square of the frequency (@fig:iono) — typically 2–15 m at L1, and much more during solar maxima and geomagnetic storms (Chapter 22). Single-frequency receivers remove only about half of it using a broadcast model; **dual-frequency** receivers eliminate the first-order effect almost completely, which is the main reason for the new civil signals.
- **Tropospheric delay**: the neutral atmosphere delays signals by about 2.4 m at the zenith (more at low elevations); models remove most of it, leaving errors of decimetres.
- **Multipath**: reflections from buildings, the ground and vehicles distort the correlation peak — the dominant error in cities.
- **Receiver noise**, typically decimetres for code measurements and millimetres for carrier phase.

![Typical pseudorange error budget for single- and dual-frequency receivers. Dual-frequency operation removes the ionospheric error, the largest error source for single-frequency users.](figures/out/ch18_errors.svg){#fig:gnsserrors width=86%}

![Ionospheric delay versus frequency for different total electron contents. The delay at L1 can exceed 30 m in a strongly ionised ionosphere.](figures/out/ch18_iono.svg){#fig:iono width=86%}

### Satellite Geometry and DOP

The same range errors produce larger position errors when the satellites are poorly spread across the sky (@fig:dopgeom). This amplification is expressed by the **dilution of precision (DOP)**, computed from the geometry matrix of the least-squares solution: position error ≈ PDOP × UERE (with HDOP and VDOP for horizontal and vertical components, and TDOP for time). Vertical errors are typically 1.5–2 times larger than horizontal errors because all satellites are above the horizon.

![Satellite sky plots illustrating good and poor geometry. Clustered satellites give a large dilution of precision.](figures/out/ch18_dopgeom.svg){#fig:dopgeom width=80%}

Using several constellations together dramatically improves geometry and availability (@fig:dop): a multi-GNSS receiver typically sees 30–40 satellites rather than 8–12, and PDOP falls from about 2 to about 1. This matters most where much of the sky is blocked — in city "urban canyons", forests and mountains.

![Simulated number of visible satellites and PDOP over 24 hours for GPS alone and for four global constellations together.](figures/out/ch18_dop.svg){#fig:dop width=90%}

A typical smartphone achieves 3–5 m accuracy in open sky (dual-frequency phones, introduced in 2018, do better) and worse in cities; a single-frequency GPS receiver meets the official GPS performance standard of a few metres; a dual-frequency, multi-constellation receiver achieves about 1–2 m.

## Augmentation: From Metres to Centimetres

Many applications need more accuracy or guaranteed **integrity** — assurance that the position is not wrong without warning. **Augmentation** systems provide corrections and integrity information (@fig:accuracy).

![Typical accuracy versus time to reach it for different GNSS positioning techniques.](figures/out/ch18_accuracy.svg){#fig:accuracy width=86%}

- **Differential GNSS (DGNSS)**: a reference station at a known position computes the errors in each pseudorange and broadcasts corrections; nearby users, who experience nearly the same errors, apply them to obtain sub-metre accuracy.
- **Satellite-based augmentation systems (SBAS)** use networks of reference stations across a continent to compute corrections for satellite orbits, clocks and the ionosphere, plus integrity messages, and broadcast them from geostationary satellites on the GPS L1 frequency (@fig:sbas). The US **WAAS** (2003), Europe's **EGNOS** (2009–2011), Japan's MSAS, India's GAGAN and others allow aircraft to fly precision approaches with vertical guidance (LPV) to thousands of airports without ground-based landing systems. The next generation, **dual-frequency multi-constellation (DFMC) SBAS**, will use L1/L5 and Galileo signals.
- **Ground-based augmentation systems (GBAS)** provide corrections and integrity within about 40 km of an airport for Category I (and in future Category II/III) landings.
- **Real-time kinematic (RTK)** positioning uses carrier-phase measurements from a nearby base station (@fig:rtk). Once the integer number of carrier cycles (the **ambiguity**) has been resolved, the rover's position is known to 1–2 cm within seconds. Networks of continuously operating reference stations (CORS) provide RTK corrections across whole countries for surveying, construction and precision agriculture.
- **Precise point positioning (PPP)** uses precise satellite orbit and clock products computed from global networks (such as those of the International GNSS Service) to achieve centimetre accuracy with a single receiver anywhere, after a convergence time of 10–30 minutes. **PPP-RTK** adds regional atmospheric corrections to shorten convergence. Satellite systems now broadcast PPP corrections free of charge: Galileo's **High Accuracy Service (HAS)** since 2023, QZSS's CLAS and MADOCA, and BeiDou's PPP-B2b.

![Approximate service regions of satellite-based augmentation systems.](figures/out/ch18_sbas.svg){#fig:sbas width=96%}

![Real-time kinematic positioning. A base station at a known position sends its carrier-phase measurements to the rover, which can then resolve the carrier-cycle ambiguities and position itself to about a centimetre.](figures/out/ch18_rtk.svg){#fig:rtk width=90%}

## Applications

| Sector | Applications | Typical requirement |
|---|---|---|
| Consumer and location-based services | Smartphones, maps, ride-hailing, fitness, games | 3–5 m, low power, fast fix |
| Road transport | Navigation, fleet management, emergency call (eCall), tolling, connected and automated vehicles | 1–5 m; lane-level 0.5 m for automation, with integrity |
| Aviation | Performance-based navigation, precision approaches (SBAS, GBAS), ADS-B surveillance | Certified accuracy and integrity |
| Maritime | Navigation, port approaches, AIS, dynamic positioning of drilling ships | 1–10 m; decimetres for dynamic positioning |
| Rail | Train location, signalling (ERTMS), asset management | Safety-critical integrity |
| Agriculture | Auto-steering, variable-rate application, yield mapping | 2 cm (RTK) |
| Surveying, construction, mapping | Cadastral surveys, machine control, GIS, mobile mapping | mm–cm |
| Timing and synchronisation | Telecom networks (5G needs ±1.5 µs), power-grid phasor measurements, financial time-stamping, data centres, broadcasting | 10 ns–1 µs |
| Drones and robotics | Autonomous flight, delivery, inspection | cm–m, high integrity |
| Search and rescue | Cospas-Sarsat MEOSAR distress beacons; Galileo Return Link Service confirms receipt | < 100 m, minutes |
| Science | Geodesy and plate tectonics (mm/year), sea level and ice, seismology, ionospheric and atmospheric sounding, reflectometry | mm, ns |
| Space | Orbit determination of LEO satellites, launch-vehicle tracking, GEO and lunar navigation | cm–m |
| Defence | Navigation, weapon guidance, timing of military networks | Encrypted, jam-resistant signals |

: Major applications of GNSS. {#tbl:gnssapps}

Scientific uses are remarkable. Networks of thousands of geodetic GNSS stations measure the motion of tectonic plates at millimetres per year, the elastic rebound of the crust as ice sheets melt, and the ground deformation of earthquakes in real time, which can improve tsunami warnings. The same signals measure the atmosphere: water vapour from tropospheric delay, electron content from ionospheric delay (@fig:tongatec) and temperature profiles from radio occultation (Chapter 16).

![Ionospheric total electron content measured in real time by NASA's Global Differential GPS network after the eruption of the Hunga Tonga–Hunga Ha'apai volcano on 15 January 2022. Waves travelling outward from the eruption appear as diagonal stripes, measured simultaneously with GPS, GLONASS, Galileo and BeiDou signals.](figures/photos/ch18_tonga.jpg){#fig:tongatec width=74%}

## Vulnerabilities: Interference, Jamming and Spoofing

The weakness of GNSS signals makes them easy to disrupt. **Jamming** — transmitting noise in the GNSS bands — can deny service over large areas with modest power (@fig:jamming): a 1 W jammer can prevent a typical receiver from tracking GPS C/A signals at line-of-sight distances of more than 10 km, and military jammers of hundreds of watts affect aircraft hundreds of kilometres away. Cheap illegal "privacy jammers" in vehicles regularly disrupt airports and port operations. **Spoofing** — transmitting counterfeit GNSS signals — is more insidious: a spoofed receiver reports a false position or time without any warning.

![Jamming-to-signal ratio versus distance from jammers of different power. Even very low-power jammers disrupt receivers at kilometres; high-power military jammers reach the radio horizon.](figures/out/ch18_jamming.svg){#fig:jamming width=86%}

Since 2017, interference has grown into a serious international problem. Ships in the Black Sea reported spoofed positions placing them at inland airports; aircraft over the Middle East, the Baltic region and elsewhere routinely encounter jamming and spoofing linked to military conflicts. In Lithuania alone, more than 1 000 aircraft per month reported interference in the first half of 2025, and the number of spoofing incidents in the region rose to several thousand per month in mid-2025, with transmitters located in the Kaliningrad region. Aviation authorities (ICAO, EASA, the FAA) have issued safety bulletins, and airlines have had to return to traditional radio navigation aids.

Countermeasures operate at several levels:

- **Robust receivers**: multi-frequency, multi-constellation tracking; interference detection and filtering; controlled-reception-pattern antennas (CRPAs) that steer nulls towards jammers; integration with inertial sensors that bridge outages.
- **Signal authentication**: Galileo's **Open Service Navigation Message Authentication (OSNMA)**, operational since 2025, digitally signs the navigation data so that receivers can detect forged messages; GPS plans similar protection (CHIMERA), and encrypted military signals (GPS M-code, Galileo PRS) resist spoofing.
- **Complementary PNT**: terrestrial systems (eLoran, mobile-network timing, fibre time distribution), signals from LEO satellites, and new technologies such as quantum inertial sensors and magnetic-anomaly navigation, so that critical infrastructure does not depend on GNSS alone. US Executive Order 13905 (2020) requires critical-infrastructure operators to manage their PNT risks.

## Future Systems

### Modernisation

All the global systems are modernising. The final GPS III satellite (SV10) was launched in April 2026, and the next generation, **GPS IIIF**, from about 2027, will add a regional high-power military signal, laser retroreflectors for precise orbit determination, and search-and-rescue payloads. Europe's **second-generation Galileo** satellites, built by Airbus and Thales Alenia Space, introduce electric propulsion, fully digital reconfigurable payloads, improved clocks and inter-satellite links, with first launches expected in 2026–27. China plans a next-generation BeiDou around 2035 with LEO augmentation; GLONASS is moving to CDMA signals with GLONASS-K2; Japan is expanding QZSS to seven and later eleven satellites; and India is replacing NavIC satellites with the NVS series, which carry indigenous atomic clocks and an L1 signal for wider receiver compatibility.

### LEO PNT

Satellites in low Earth orbit are about 20 times closer than MEO navigation satellites, so their signals arrive about 30 dB stronger — much harder to jam — and their faster motion across the sky allows rapid convergence of precise solutions. **Iridium**'s Satellite Time and Location service already provides timing and positioning that works indoors. Start-ups such as **Xona Space Systems** (which launched its first production-class Pulsar satellite in 2025) are building dedicated LEO PNT constellations; ESA's **LEO-PNT** in-orbit demonstrators (Celeste) are testing the concept; and researchers have shown that even signals from broadband constellations such as Starlink can be used opportunistically for navigation. LEO PNT is expected to complement rather than replace MEO GNSS.

### Navigation Beyond the Earth

GNSS signals are increasingly used above the constellations. In geostationary and high orbits, receivers use the weak signals that spill past the Earth's limb and the antenna side lobes — the **space service volume**. In March 2025 the **Lunar GNSS Receiver Experiment (LuGRE)**, an Italian–NASA receiver on Firefly's Blue Ghost lander, became the first to track GPS and Galileo signals on the Moon's surface and compute a navigation fix, some 380 000 km from Earth (@fig:spacevol). For the coming era of lunar exploration, NASA, ESA (Moonlight), JAXA and others are developing **LunaNet**, a framework for lunar communications and navigation with dedicated lunar navigation satellites and a lunar time standard.

![GNSS signals beyond the constellations. Users in high orbits and at the Moon receive signals that spill past the Earth's limb.](figures/out/ch18_spacevolume.svg){#fig:spacevol width=90%}

::: figrow
![Firefly's Blue Ghost Mission 1 lander was launched on 15 January 2025 on a Falcon 9 rocket. It carried LuGRE, which made the first GNSS navigation fix on the Moon in March 2025.](figures/photos/ch18_blueghost.jpg){#fig:blueghost}

![The Gravity Probe B spacecraft, launched in 2004 on a Delta II, confirmed predictions of general relativity — the same physics that every GNSS satellite clock must account for.](figures/photos/ch18_delta.jpg){#fig:gpb}
:::

::: example
**Example: what accuracy do GNSS clocks and orbits need?**

1. *Clock stability.* To keep the satellite clock contribution to the range error below 0.3 m (1 ns) for 12 hours between uploads, the clock must keep time to 1 ns in 43 200 s — a fractional frequency stability of about $1 \times 10^{-9}/43\,200 \approx 2\times10^{-14}$. Only hydrogen masers and the best rubidium clocks achieve this; the ground segment also estimates and broadcasts each clock's drift.
2. *Orbit accuracy.* An orbit error mainly affects the range along the line of sight. To contribute less than 0.3 m, the broadcast orbit must be known to about 0.3 m radially — even though the satellite moves at 3.9 km/s.
3. *Position accuracy.* With UERE = 1.0 m (dual-frequency) and PDOP = 1.5 (multi-GNSS), the 1-σ position error is about 1.5 m; with RTK (UERE ≈ 1 cm for carrier phase after ambiguity resolution) it falls to about 1.5 cm.
4. *Timing.* A static receiver at a known position needs only one satellite to solve for time; averaging many satellites gives timing accuracy of 10–20 ns relative to UTC — sufficient for 5G networks.
:::

::: ai
**AI in satellite navigation**

Machine learning helps receivers detect and classify interference and spoofing, mitigate multipath in cities by learning which signals are reflected, fuse GNSS with cameras, lidar and inertial sensors in autonomous vehicles, and forecast ionospheric conditions. On the ground, AI models improve orbit and clock predictions and monitor the health of the constellation. Chapters 44 and 46 discuss these applications.
:::

::: key
**Key takeaways**

- GNSS provides positioning, navigation and timing worldwide; about seven billion receivers depend on it, and so do telecom, power and financial networks.
- Receivers measure pseudoranges to at least four satellites and solve for position and receiver clock offset; carrier phase allows centimetre precision.
- Signals are weaker than thermal noise but are recovered through spread-spectrum correlation; codes such as the GPS C/A Gold code allow all satellites to share frequencies.
- GPS, GLONASS, Galileo and BeiDou each operate about 24–30 MEO satellites with atomic clocks; QZSS and NavIC serve regions. Relativity changes GPS clock rates by +38.5 µs per day.
- Accuracy depends on the error budget (ionosphere, clocks, orbits, troposphere, multipath) and satellite geometry (DOP); dual-frequency, multi-GNSS receivers achieve 1–2 m.
- SBAS, GBAS, RTK and PPP improve accuracy to centimetres and provide integrity for aviation and other safety-critical uses.
- Jamming and spoofing have become widespread; authentication (Galileo OSNMA), robust receivers and complementary PNT (including LEO PNT) are the responses.
- GNSS is now used at the Moon: LuGRE made the first lunar GNSS fix in 2025.
:::
