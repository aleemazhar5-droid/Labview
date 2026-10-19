---
title: Satellite Buses and Payload Instruments
hero: ch12
abstract: Every satellite is a payload carried by a bus. This chapter surveys the commercial and government satellite platforms on which payloads fly - from standard geostationary buses to mass-produced constellation platforms and CubeSat kits - and the interfaces between bus and payload. It then introduces the families of payload instruments that later chapters apply: optical and infrared imagers and spectrometers, microwave radiometers, radars, lidars, particle and field instruments and service payloads, with the physics of detectors, telescopes, scanning methods, calibration and the payload data chain.
---

## The Bus as a Product

### From Custom Spacecraft to Product Lines

Early satellites were built one at a time around their payloads. Today most satellites use a **standard bus** (platform) from a manufacturer's product line, adapted to the payload — much as a truck chassis carries different bodies. Product lines lower cost and risk through heritage (flight-proven designs), reuse of qualification data, and streamlined production. @tbl:buses lists representative product lines.

Table: Representative satellite bus product lines (2026). {#tbl:buses}

| Class | Bus | Manufacturer | Typical mass / power | Typical missions |
|---|---|---|---|---|
| Large GEO | Eurostar Neo; OneSat (software-defined) | Airbus (Europe) | 3–6.5 t / up to 25 kW | Broadband and broadcast comsats |
| Large GEO | Spacebus Neo; Inspire | Thales Alenia Space (Europe) | 3–6 t / up to 20 kW | Comsats, Galileo second generation (with Airbus) |
| Large GEO | 702 family (702SP, 702X) | Boeing (USA) | 2–6 t / 3–25 kW | Comsats, WGS, O3b mPOWER (MEO) |
| Large GEO | LM 2100 / LM 400 | Lockheed Martin (USA) | 2–6 t | GOES-R, GPS III (A2100-derived), SBIRS, comsats |
| Large GEO | 1300 series | Maxar Space Systems (USA) | 3–7 t / up to 25 kW | Comsats, Psyche (derived bus) |
| Large GEO | DFH-4 / DFH-4E / DFH-5 | CAST (China) | 5–9 t / up to 28 kW | Chinese comsats, Tianlian relays |
| Large GEO | I-3K / I-4K / I-6K | ISRO (India) | 2–6 t | GSAT, INSAT |
| Small GEO | MicroGEO | Astranis (USA) | ≈ 400 kg | Regional broadband |
| LEO / MEO medium | Eurostar / AstroBus / Arrow | Airbus | 0.3–2 t | Sentinel, EO, OneWeb (Arrow) |
| LEO medium | SSTL-150 / -300 / -S1 | Surrey Satellite Technology (UK) | 100–500 kg | EO, Galileo FOC payloads, technology |
| LEO medium | LM 400 / LM 50 | Lockheed Martin | 50–2 000 kg | SDA, military |
| LEO productised | Aries / Nova / Comet | Apex (USA) | 100–500 kg | Rapid-delivery buses for many customers |
| LEO productised | X-Bus, MicroSat | York Space / Blue Canyon (RTX) | 50–500 kg | SDA Transport Layer, NASA science (TROPICS) |
| Constellation-specific | Starlink V2 Mini / V3 | SpaceX | 0.8–2 t | Vertical integration, in-house only |
| CubeSat kits | 3U–16U buses | Blue Canyon, EnduroSat, GomSpace, NanoAvionics, AAC Clyde, Open Cosmos | 4–30 kg | EO, IoT, science, education |

Three major trends are reshaping bus design:

1. **Productisation and speed.** Companies such as Apex and York aim to deliver standard buses in months rather than years, with large factories building dozens per year. Governments (e.g., the US Space Development Agency) buy satellites in "tranches" of tens to hundreds.
2. **Software-defined platforms and payloads.** Digital processors and flexible antennas let a satellite's coverage, frequency plan and power allocation be changed in orbit — and let the bus's own behaviour be updated like a phone's operating system.
3. **Vertical integration.** The largest constellation operators build their own buses, payloads, ground terminals and launches, optimising the whole system rather than buying components.

### What the Bus Provides

From the payload's point of view, the bus is a service provider. It must deliver:

- **A place to live**: mechanical mounting with the required alignment and stiffness, protection during launch.
- **Power**: average and peak power at the right voltage, with protected switching.
- **Thermal environment**: heat removal for electronics, stable temperatures for optics, cooling for detectors.
- **Pointing**: accuracy, knowledge, stability (jitter), agility and keep-out zones (e.g., never point a sensitive telescope near the Sun).
- **Data handling**: command distribution, data collection, storage and downlink capacity.
- **Time and position**: precise time (often a GNSS-derived pulse per second) and orbit/attitude data for geolocation.
- **A clean environment**: low contamination, low electromagnetic interference and low microvibration.

These services are defined in a **payload–bus interface control document** (@fig:interfaces). Mismatches at interfaces — a payload drawing more peak power than expected, or a bus reaction wheel exciting a resonance of the telescope — are among the commonest causes of problems in integration.

![The payload–bus interfaces that must be specified and verified for every mission.](figures/out/ch12_interfaces.svg){#fig:interfaces width=94%}

### Hosted Payloads

A **hosted payload** is an instrument or transponder that flies on someone else's satellite, using spare mass, power and data capacity — typically on a commercial GEO communications satellite. Hosting can cut costs by a factor of several and speed access to orbit. Examples include NASA's GOLD ultraviolet imager (on SES-14, 2018) and TEMPO air-quality spectrometer (on Intelsat 40e, 2023), the Aireon ADS-B receivers on all 66 Iridium NEXT satellites (giving global air-traffic surveillance), and several US and European government payloads on commercial satellites. The challenges are aligning schedules, defining interfaces and ensuring that the host's operations do not compromise the hosted mission.

## A Taxonomy of Payload Instruments

Payloads can be grouped in four families (@fig:taxonomy):

- **Passive remote sensing** — instruments that measure radiation emitted or reflected by the target: cameras, imagers, spectrometers, radiometers, polarimeters, and receivers of GNSS signals (radio occultation and reflectometry).
- **Active remote sensing** — instruments that transmit their own signal and measure its echo: radars (synthetic aperture radar, altimeters, scatterometers, precipitation and cloud radars) and lidars.
- **In-situ instruments** — instruments that measure their immediate environment: magnetometers, plasma and particle detectors, electric-field and wave instruments, dust detectors, mass spectrometers and accelerometers.
- **Service payloads** — communications transponders, navigation payloads (clocks and signal generators), data relay terminals, search-and-rescue repeaters.

![A taxonomy of satellite payloads.](figures/out/ch12_taxonomy.svg){#fig:taxonomy width=96%}

Each part of the electromagnetic spectrum carries different information and needs different technology (@fig:spectrum). Short wavelengths (X-rays, gamma rays) reveal high-energy processes; ultraviolet senses ozone, the upper atmosphere and hot plasmas; visible and near-infrared light shows surface reflectance (vegetation, minerals, water); thermal infrared shows temperature and composition; microwaves penetrate clouds and sense moisture, temperature profiles and surface roughness; and radio wavelengths are used for radar, navigation and communications.

![The electromagnetic spectrum and the wavelength ranges used by different classes of space instruments.](figures/out/ch12_spectrum.svg){#fig:spectrum width=96%}

Not all wavelengths reach the ground from space: the atmosphere absorbs strongly in certain bands (@fig:windows). Imagers that want to see the surface use **atmospheric windows**; **sounders** deliberately use absorption bands — at different distances from the centre of a CO₂ or O₂ band, the radiation comes from different heights — to retrieve vertical profiles of temperature and humidity (Chapter 16).

![Schematic atmospheric transmission from 0.2 to 20 µm. Windows are used for surface imaging; absorption bands of water vapour, carbon dioxide and ozone are used for atmospheric sounding.](figures/out/ch12_windows.svg){#fig:windows width=92%}

## Optical and Infrared Instruments

### Telescopes

An optical instrument collects light with a **telescope** and focuses it onto a detector. The main designs (@fig:telescopes) are:

- **Refractors** — lenses; simple but heavy and limited in aperture; used in star trackers, small cameras and wide-field instruments.
- **Cassegrain-type reflectors** — a concave primary and convex secondary mirror; the **Ritchey–Chrétien** variant (Hubble, many Earth-imaging telescopes) corrects coma for a wider field.
- **Three-mirror anastigmats (TMA)** — three curved mirrors, often off-axis, give wide, well-corrected fields with no central obstruction; used in pushbroom imagers (Landsat OLI, Sentinel-2 MSI, WorldView) and JWST.
- **Segmented and deployable primaries** — large telescopes that fold for launch (JWST's 6.5 m, 18-segment mirror; Chapter 38).
- **Catadioptric** designs combining lenses and mirrors, compact enough for small satellites.

![Telescope configurations used in space instruments.](figures/out/ch12_telescopes.svg){#fig:telescopes width=98%}

The angular resolution of a telescope is limited by diffraction:

$$\theta \approx 1.22\,\frac{\lambda}{D}$$

For a 1.1 m telescope (WorldView-3) at 0.5 µm, $\theta$ = 0.55 µrad, so from 617 km it can resolve about 34 cm on the ground. Real resolution also depends on the detector pixel size, optical aberrations, satellite motion and jitter, and the atmosphere — summarised in the **modulation transfer function (MTF)** (Chapter 13).

### Detectors

**Detectors** convert photons into electrical signals. Visible and near-infrared imagers use **silicon** detectors — CCDs (charge-coupled devices) and, increasingly, CMOS image sensors, which integrate readout electronics on the chip, consume less power and are more tolerant of radiation. **Time-delay integration (TDI)** sensors shift charge along columns in step with the image motion, adding up the signal from tens of rows to increase sensitivity for fast-moving LEO imagers.

Infrared detectors use semiconductors with smaller band gaps: **InGaAs** (short-wave IR to 1.7 µm, usable at near room temperature), **InSb** (to 5.5 µm, cooled to about 80 K), **HgCdTe** ("MCT", tunable from 1 to more than 14 µm by changing its composition — the workhorse of space IR instruments including JWST's NIRCam and NIRSpec), and newer **type-II superlattice** (T2SL) and **barrier** detectors. **Microbolometers** detect the heating of tiny suspended membranes and need no cooling, making thermal cameras possible on small satellites, although with lower sensitivity (@fig:qe).

![Schematic quantum efficiency or relative response of common detector materials. Each material covers a spectral range set by its band gap; infrared detectors must be cooled to suppress dark current.](figures/out/ch12_detector_qe.svg){#fig:qe width=92%}

Because the dark current of a detector grows exponentially with temperature and inversely with band gap, long-wave infrared detectors must be cooled — to 40–80 K for HgCdTe and InSb, and to below 10 K for some astronomical detectors — by **passive radiators** (for missions with cold views, such as polar orbiters and L2 telescopes) or **cryocoolers** (Chapter 5).

### Imaging Architectures

Imagers build a 2-D picture of the ground in three ways (@fig:scanmodes):

- **Whiskbroom** scanners use a rotating or oscillating mirror to sweep a few detectors across the swath, building the image line by line as the satellite moves (Landsat 1–7 MSS/TM/ETM+, AVHRR, MODIS). They need few detectors but have short dwell times and moving parts.
- **Pushbroom** imagers use long linear arrays (thousands to tens of thousands of pixels) perpendicular to the ground track; the satellite's motion sweeps the array along. They have long dwell time, no scanning mirror and excellent geometry — the standard for modern EO (Landsat 8/9 OLI, Sentinel-2 MSI, WorldView, Pléiades).
- **Framing** (staring) cameras use 2-D arrays to capture whole scenes at once, like a normal camera; used on SkySat, Planet Doves, many GEO imagers in step-stare mode, and astronomical telescopes. **Video** from orbit is possible with framing cameras on agile satellites.

![The three basic imaging architectures.](figures/out/ch12_scan_modes.svg){#fig:scanmodes width=98%}

### Spectrometers

A **spectrometer** splits light into its component wavelengths to measure composition. Main types:

- **Dispersive** spectrometers use a **prism** or **diffraction grating**; an imaging spectrometer forms a 2-D detector image with one axis spatial and one axis spectral (hyperspectral pushbroom imagers such as EMIT, PRISMA and EnMAP; Chapter 14).
- **Fourier-transform spectrometers (FTS)** measure an interferogram with a moving mirror (Michelson interferometer) and transform it into a spectrum with high spectral resolution; used by infrared sounders (IASI, CrIS) and greenhouse-gas instruments (GOSAT).
- **Filter-based** spectral imagers use fixed or tunable filters (multispectral imagers; Fabry–Pérot and acousto-optic tunable filters).
- **Spatial heterodyne** and **grating-based high-resolution** spectrometers for specific gases (OCO-2/3 measure CO₂ with three grating spectrometers at 0.76, 1.61 and 2.06 µm).

## Microwave Instruments

### Passive Microwave Radiometers

Every object emits microwave radiation in proportion to its temperature and **emissivity**. In the microwave region the Rayleigh–Jeans approximation holds, so the measured radiance is expressed as a **brightness temperature** $T_B = \varepsilon\,T_{physical}$. Radiometers measure $T_B$ at several frequencies and polarisations to retrieve:

- **Sea-surface temperature and wind speed** (6–37 GHz; AMSR2, GMI);
- **Soil moisture and ocean salinity** at L-band (1.4 GHz; SMOS, SMAP), where emissivity depends strongly on water content;
- **Sea ice, snow and rain** (10–89 GHz);
- **Atmospheric temperature profiles** using the 50–60 GHz oxygen band and **humidity profiles** using the 183 GHz water-vapour line (ATMS, AMSU, MWS on MetOp-SG); see Chapter 16.

Because microwave wavelengths are long, antennas must be large for fine resolution: at 1.4 GHz a 6 m reflector (SMAP) gives about 40 km resolution, and SMOS used a 2-D **interferometric** array of 69 small antennas to synthesise a large aperture. Radiometers are calibrated on every scan by viewing a warm blackbody target and cold space.

### Radars

Active microwave instruments transmit pulses and analyse the echoes:

- **Synthetic aperture radar (SAR)** — high-resolution imaging day and night through cloud, using the satellite's motion to synthesise a long antenna (Chapter 15).
- **Radar altimeters** — measure the height of the ocean, ice or land surface to centimetre precision from the round-trip time of nadir pulses (Jason, Sentinel-3, Sentinel-6 Michael Freilich); **SWOT** (2022) uses Ka-band radar interferometry to map water heights in 2-D swaths.
- **Scatterometers** — measure backscatter from the ocean surface from several directions to infer wind speed and direction (ASCAT on MetOp, HY-2 series).
- **Precipitation radars** (Ku/Ka-band; GPM's Dual-frequency Precipitation Radar) and **cloud radars** (94 GHz; CloudSat, EarthCARE's Doppler cloud profiling radar).
- **Sounding radars** — low-frequency radars that penetrate ice and dry ground (MARSIS and SHARAD at Mars, RIME on JUICE, REASON on Europa Clipper).

### GNSS Remote Sensing

Navigation signals are a free, global source of microwave illumination. In **radio occultation (RO)**, a LEO receiver tracks a GNSS signal as it sets behind the Earth's atmosphere; the bending of the signal gives profiles of refractivity, hence temperature and humidity, with high vertical resolution and no calibration drift — among the most valuable inputs to weather forecasting (COSMIC-2, MetOp GRAS, Spire, PlanetiQ). In **GNSS reflectometry (GNSS-R)**, receivers measure signals reflected from the ocean or land to infer wind speed, soil moisture and flooding (CYGNSS, 2016).

## Lidar Instruments

A **lidar** (light detection and ranging) fires laser pulses and measures the return. Space lidars include:

- **Altimetry lidars** — ICESat (2003–2009) and **ICESat-2** (2018–), whose ATLAS instrument fires 10 000 pulses per second split into six beams and counts individual returning photons to measure ice-sheet and sea-ice elevation to centimetres; **GEDI** on the ISS measures forest canopy height.
- **Backscatter lidars** — CALIPSO (2006–2023) and EarthCARE's ATLID (2024) profile aerosols and clouds, separating particle types by depolarisation.
- **Doppler wind lidar** — ESA's **Aeolus** (2018–2023) measured wind profiles globally for the first time from the Doppler shift of molecular and aerosol backscatter at 355 nm, improving weather forecasts.
- **Differential absorption lidar (DIAL)** — measures gases such as methane (France–Germany's planned MERLIN) by comparing absorption at two nearby wavelengths.
- **Planetary lidars** — the Mars Orbiter Laser Altimeter (MOLA) and Lunar Orbiter Laser Altimeter (LOLA) mapped topography; lidars guide landers (Chapter 27).

Space lidars need powerful, efficient, long-life lasers (diode-pumped Nd:YAG at 1 064 nm and its harmonics at 532 and 355 nm; fibre lasers at 1.5–2 µm), large receiving telescopes, and sensitive detectors (photomultipliers, avalanche photodiodes, single-photon counters). Laser-induced damage of optics in vacuum and laser lifetime were major challenges for Aeolus.

## In-Situ Instruments: Fields and Particles

Space-physics missions (Part VII) and planetary missions carry instruments that sample their surroundings directly:

- **Magnetometers** — **fluxgate** vector magnetometers (accurate to ≈ 0.01–0.1 nT) and **scalar** magnetometers (optically pumped helium, Overhauser) that measure field magnitude absolutely. They are mounted on long booms (5–10 m) to escape the spacecraft's own magnetic field, and missions follow strict **magnetic cleanliness** programmes. The ESA **Swarm** constellation maps Earth's field; Juno's magnetometers revealed Jupiter's complex dynamo.
- **Plasma analysers** — electrostatic analysers that measure the energy, direction and (with time-of-flight sections) mass of ions and electrons of eV–tens of keV.
- **Energetic particle detectors** — solid-state silicon telescopes and scintillators for MeV particles in radiation belts and solar events.
- **Electric-field and plasma-wave instruments** — long wire booms (tens of metres) and search-coil magnetometers.
- **Langmuir probes** — measure plasma density and temperature.
- **Dust detectors and mass spectrometers** — analyse cometary dust, planetary atmospheres and exospheres (e.g., Rosetta's COSIMA and ROSINA, Europa Clipper's SUDA and MASPEX).
- **Accelerometers** — measure non-gravitational accelerations for gravity missions (GOCE, GRACE-FO) and atmospheric density.

::: figrow
![The Parker Solar Probe magnetometer boom being tested for deployment before launch (2018). Booms separate sensitive magnetometers from the spacecraft's own magnetic fields.](figures/photos/ch12_psp_mag.jpg){#fig:pspmag}

![Europa Clipper's 8.5 m magnetometer boom, a coilable lattice mast, during deployment testing at JPL (2021).](figures/photos/ch12_clippermag.jpg){#fig:clippermag}
:::

## Service Payloads

**Communications payloads** — transponders that receive, amplify, frequency-convert and retransmit signals, and modern regenerative payloads with digital processors and beam-forming networks — are described in Chapter 17. **Navigation payloads** — atomic clocks, signal generators and high-stability transmitters — are described in Chapter 18. Other service payloads include **search-and-rescue repeaters** (Cospas-Sarsat MEOSAR on GPS, Galileo, GLONASS and BeiDou satellites, which relay 406 MHz distress beacons and, on Galileo, send a "return link" acknowledgement), **AIS and ADS-B receivers** for ship and aircraft tracking, **data collection systems** (Argos for animal tracking and buoys), and **laser communication terminals**.

## Performance, Calibration and Data

### Key Performance Measures

Instrument performance is captured by a small set of figures of merit:

| Measure | Meaning | Typical use |
|---|---|---|
| Ground sampling distance (GSD) / spatial resolution | Size of a pixel on the ground; ability to separate nearby objects | Imaging (0.3 m–1 km) |
| Modulation transfer function (MTF) | Contrast preserved at a given spatial frequency (sharpness) | Optical imagers (MTF at Nyquist ≈ 0.1–0.3) |
| Signal-to-noise ratio (SNR) | Signal relative to noise at a reference radiance | Optical/IR imagers (100–500) |
| Noise-equivalent temperature difference (NEΔT) | Smallest detectable temperature change | Thermal IR (0.05–0.3 K) |
| Noise-equivalent differential reflectance | Smallest detectable change in reflectance | Ocean colour, hyperspectral |
| Spectral resolution / sampling | Width of spectral channels | Hyperspectral (5–10 nm), sounders (< 0.5 cm⁻¹) |
| Radiometric accuracy and stability | Agreement with SI-traceable truth over time | Climate records (≤ 1–3 %; ≤ 0.1 K) |
| Geolocation accuracy | Error in where a pixel is placed on Earth | EO (≤ 1 pixel; < 5 m for high-res) |
| Revisit / temporal resolution | Time between observations | EO, weather |

### Calibration

A measurement is only useful if it is accurate and comparable over time and between instruments. Calibration (@fig:calib) starts with **pre-launch laboratory calibration** against standards traceable to national metrology institutes (NIST, NPL, PTB), continues with **onboard references** — sunlight scattered from diffuser panels, internal lamps, blackbodies at known temperatures, views of cold space — and uses natural targets: the **Moon** (whose reflectance is extremely stable and is modelled by the ROLO and LIME models), stable desert and ice sites (**vicarious calibration**, e.g., the RadCalNet network), and **inter-calibration** against reference instruments during simultaneous observations (the WMO **Global Space-based Inter-Calibration System, GSICS**). Future "climate benchmark" missions such as NASA's CLARREO Pathfinder and ESA's TRUTHS aim to fly SI-traceable references in orbit with uncertainties ten times smaller than today's instruments.

![The calibration chain for Earth-observation instruments, from laboratory standards to in-orbit inter-calibration.](figures/out/ch12_calibration.svg){#fig:calib width=98%}

### The Payload Data Chain

Inside the instrument, photons or radio signals become information through a chain of steps: detector → analogue signal conditioning → **analogue-to-digital conversion** (typically 12–16 bits for imagers) → **non-uniformity correction** and binning → **compression** (lossless or near-lossless, CCSDS 121/122/123) → formatting into packets with time and attitude tags → **mass memory** → downlink. Increasingly, an onboard processor or AI accelerator analyses the data before downlink — detecting clouds, ships, fires or scientific events — and sends only what matters (Chapters 43–44). On the ground, processing turns raw data (Level 0) into calibrated, geolocated products (Level 1) and geophysical variables (Level 2 and above), described in Chapter 13.


## Designing an Optical Payload: Radiometry and SNR

### How Much Light Reaches a Pixel?

The signal in an Earth-imaging detector can be estimated from the scene radiance $L$ (W m⁻² sr⁻¹ µm⁻¹), the telescope aperture diameter $D$ and focal length $f$, the optical transmission $\tau$, the spectral bandwidth $\Delta\lambda$, the detector pixel pitch $p$, the quantum efficiency $\eta$ and the integration time $t_{int}$. The number of photoelectrons collected is

$$N_e = \frac{\pi}{4}\,\frac{L\,\tau\,\eta\,\Delta\lambda\,p^2\,t_{int}}{F^2}\,\frac{\lambda}{hc}, \qquad F = f/D$$

where $F$ is the focal ratio (f-number). The noise has contributions from **photon shot noise** ($\sqrt{N_e}$), **dark current**, **read noise** and **quantisation**, so

$$\text{SNR} = \frac{N_e}{\sqrt{N_e + N_{dark} + \sigma_{read}^2 + \sigma_{quant}^2}}$$

For a pushbroom imager, the integration time is limited by the time the ground image takes to move one pixel: $t_{int} = \text{GSD}/v_{ground}$, about 1 ms for a 7 m GSD at a ground speed of 7 km/s and only about 50 µs for a 30 cm GSD. This is why very-high-resolution imagers need large apertures, **time-delay integration** with dozens of stages, or satellite "slow-down" manoeuvres that rotate the spacecraft to slow the apparent ground motion.

::: example
**Worked example — SNR of a 10 m multispectral band**

Consider a red band (centre 665 nm, $\Delta\lambda$ = 30 nm) viewing vegetation of radiance $L$ = 50 W m⁻² sr⁻¹ µm⁻¹ from 786 km with a 15 cm aperture, f/6.5 telescope ($\tau$ = 0.8), 7.5 µm pixels ($\eta$ = 0.8), and $t_{int}$ = 1.5 ms (10 m pixel at 6.7 km/s ground speed).

$N_e = (\pi/4)\times50\times0.8\times0.8\times0.030\times(7.5\times10^{-6})^2\times1.5\times10^{-3}/6.5^2 \times (0.665\times10^{-6}/(6.63\times10^{-34}\times3\times10^8))$

$= 0.785\times50\times0.64\times0.030\times5.6\times10^{-11}\times1.5\times10^{-3}/42.3 \times 3.34\times10^{18} \approx 2.6\times10^{5}$ electrons.

With shot noise dominating, SNR ≈ $\sqrt{2.6\times10^5}$ ≈ 500 (before other noise sources), comfortably above typical requirements of 100–200. Real designs check SNR at a dark reference radiance (e.g., over water) where the margin is much smaller — the reason ocean-colour sensors use large apertures and wider bands.
:::

### Pointing, Jitter and Microvibration

A high-resolution imager magnifies every tiny motion of the spacecraft. If the line of sight moves by more than a fraction of a pixel during integration, the image blurs. For a 30 cm GSD at 600 km, one pixel subtends 0.5 µrad (0.1 arcsec) — so **jitter** during the 50–100 µs line time must be held to a fraction of that. Sources include reaction-wheel imbalance (at the wheel spin frequency and harmonics), cryocooler compressors, solar-array drive steps and thermal "snaps". Mitigations include isolating wheels on vibration-damping mounts, balancing wheels to very tight tolerances, using control-moment gyroscopes with high rotor speeds above structural modes, quiet (counter-balanced) cryocoolers, **fine-steering mirrors** in the optical path, and line-of-sight stabilisation. JWST and Hubble use dedicated fine guidance sensors; high-resolution EO satellites use extremely stiff, thermally stable optical benches made of silicon carbide, Zerodur or carbon-fibre composites.

### Field-of-View and Keep-Out Analysis

Every instrument has a field of view that must not be blocked by solar arrays, antennas or thruster plumes, and keep-out zones that must avoid the Sun (to prevent detector damage or stray light), the Earth limb or the Moon. Accommodation studies use 3-D models to compute fields of view, stray-light paths (with tools such as FRED or ASAP), thruster-plume impingement, and contamination deposition. Thrusters are placed so that plumes do not reach cold optics, and sensitive instruments carry covers that open only after outgassing has subsided in orbit.

## Instrument Case Studies

Table: Representative modern instruments and their key parameters. {#tbl:instruments}

| Instrument (mission, launch) | Type | Key parameters | What it measures |
|---|---|---|---|
| OLI-2 (Landsat 9, 2021) | Pushbroom multispectral imager, 4-mirror anastigmat | 9 bands 0.43–2.29 µm; 15 m pan, 30 m multispectral; 185 km swath; 14-bit | Land cover, agriculture, water quality, long-term record since 1972 |
| TIRS-2 (Landsat 9) | Pushbroom thermal imager, QWIP detectors at ≈ 40 K | 2 bands 10.9 and 12.0 µm; 100 m | Land-surface temperature, evapotranspiration |
| MSI (Sentinel-2A/B/C, 2015–2024) | Pushbroom TMA imager | 13 bands 0.44–2.19 µm; 10/20/60 m; 290 km swath | Vegetation, coastal and inland waters |
| ABI (GOES-R series, 2016–2024) | Scanning GEO imager | 16 bands 0.47–13.3 µm; 0.5–2 km; full disk every 10 min, mesoscale every 30–60 s | Weather, fire, volcanic ash, cloud properties |
| VIIRS (Suomi NPP, NOAA-20/21) | Whiskbroom scanning radiometer | 22 bands 0.41–12.5 µm; 375 m / 750 m; day–night band | Weather, fires, night lights, ocean colour, aerosols |
| IASI-NG (MetOp-SG A, 2025) | Fourier-transform IR sounder | 3.62–15.5 µm, 16 921 channels, 0.25 cm⁻¹ | Temperature, humidity and trace-gas profiles |
| ATMS (JPSS) | Microwave sounder | 22 channels 23–183 GHz | All-weather temperature and humidity profiles |
| SMAP radiometer (2015) | L-band radiometer, 6 m rotating mesh antenna | 1.41 GHz, ≈ 40 km, 1 000 km swath | Soil moisture, freeze/thaw |
| ATLAS (ICESat-2, 2018) | Photon-counting lidar | 532 nm, 10 kHz, 6 beams, ≈ 0.7 m along-track sampling | Ice-sheet, sea-ice and vegetation height |
| C-SAR (Sentinel-1, 2014–2025) | C-band SAR, active phased array 12.3 × 0.8 m | 5.405 GHz; 5 × 20 m (IW mode), 250 km swath | Deformation, floods, ice, ships |
| TROPOMI (Sentinel-5P, 2017) | UV–SWIR imaging spectrometer | 270–2 385 nm; 5.5 × 3.5 km; 2 600 km swath | NO₂, O₃, SO₂, CO, CH₄, aerosols |
| MAG (Swarm, 2013) | Vector fluxgate + absolute scalar magnetometers on boom | 0.1 nT resolution | Geomagnetic field and its variations |

These instruments illustrate recurring design patterns: pushbroom imagers with TMA optics for land imaging; scanning imagers in GEO for weather; FTS and grating spectrometers for atmospheric composition; large deployable antennas for long-wavelength microwave measurements; and booms for magnetic measurements.

## Large Communications Platforms: Power as the Measure

For communications satellites, available power largely determines capacity. Over six decades GEO communications satellites grew from the 40 W *Early Bird* (1965) to platforms of 20–30 kW (@fig:geopower), enabled by multi-junction solar cells, lithium-ion batteries, deployable radiators with loop heat pipes, and electric propulsion that frees mass for payload. Very-high-throughput satellites such as **ViaSat-3** (each about 6.4 t and about 30 kW, deploying a very large reflector) push the limits of what a single platform can do — while the deployment of ViaSat-3 F1's reflector partially failed in 2023, showing that large deployables remain a risk.

![Approximate power of representative geostationary communications satellites since 1965.](figures/out/ch12_geo_power.svg){#fig:geopower width=82%}

![A GOES-R series full-disk image of the Western Hemisphere from the Advanced Baseline Imager in geostationary orbit — the kind of product made possible by a capable payload carried on a stable bus.](figures/photos/ch12_goesfull.jpg){#fig:goesfull width=60%}

::: key
**Key takeaways**

- Most satellites use standard buses from product lines; trends are productisation, software-defined platforms and vertical integration; hosted payloads share buses to reduce cost.
- Payload–bus interfaces (mechanical, power, thermal, data, time, pointing, contamination/EMC) must be specified and verified carefully.
- Payloads are passive or active remote-sensing instruments, in-situ field and particle instruments, or service payloads; each spectral region reveals different physics, and atmospheric windows and absorption bands are both useful.
- Optical systems combine telescopes (refractors, Ritchey–Chrétien, TMA, segmented mirrors) with detectors chosen for wavelength (Si, InGaAs, InSb, HgCdTe, microbolometers) and cooled as needed; pushbroom imaging dominates modern EO.
- Microwave radiometers, radars, GNSS radio occultation and lidars measure the atmosphere and surface in all weather; magnetometers and particle instruments sample space plasmas.
- Performance is described by GSD, MTF, SNR, NEΔT, spectral resolution, radiometric accuracy and geolocation; calibration from the laboratory to the Moon and vicarious sites makes measurements trustworthy.
:::

::: questions
**Review questions**

1. Why have most satellite manufacturers moved to standard bus product lines? What are hosted payloads?
2. List the interfaces between a payload and its bus that must be specified and verified.
3. Which detector materials are used for visible, short-wave infrared and thermal-infrared imaging, and which require cooling?
4. Compare framing, whisk-broom and push-broom imaging architectures.
5. A push-broom imager at 500 km altitude has 8 µm pixels and a 4 m focal length. What is its ground sample distance at nadir? What aperture is needed for its diffraction-limited resolution at 0.6 µm to match that GSD?
6. How does GNSS radio occultation measure atmospheric temperature and humidity profiles?
7. Explain why calibration is needed before launch, in orbit and with vicarious sites, and give an example of each.
8. Why is a communication satellite's payload capability usually described by its power?
:::
