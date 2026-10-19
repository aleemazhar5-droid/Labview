---
title: Space Communications and the Ground Segment
hero: ch07
abstract: Without communications a spacecraft is useless - it cannot be controlled, and its data cannot be used. This chapter explains how radio and laser links work, from frequency bands and antennas to the link budget that decides whether a signal can be received; how modulation and error-correcting codes approach the theoretical limits of communication; the ground stations, networks and mission control centres that make up the ground segment; deep-space communications; and the international standards that let spacecraft and ground systems from different organisations work together.
---

## The Role of Communications

Every spacecraft has at least one radio link. Communications serve four purposes:

1. **Telecommand (TC)** — instructions from the ground to the spacecraft (uplink), typically at a few kbit/s with strong error protection and authentication.
2. **Telemetry (TM)** — health and status data from the spacecraft (housekeeping), typically kbit/s to tens of kbit/s.
3. **Tracking** — measuring range, range-rate and angles to determine the orbit (Chapter 3).
4. **Payload (mission) data** — the product of the mission: images, radar data, science measurements, or, for communications satellites, the user traffic itself. Rates range from bits per second (deep space) to tens of gigabits per second (laser crosslinks).

The first three are grouped as **TT&C** (telemetry, tracking and command). Payload data usually uses a separate, higher-frequency, higher-rate link.

## Frequency Bands and Spectrum

### The Radio Spectrum for Space

Radio frequencies are a limited, shared natural resource. The **International Telecommunication Union (ITU)** allocates frequency bands to services (e.g., Earth exploration-satellite, space research, fixed-satellite, mobile-satellite, radionavigation-satellite) in its **Radio Regulations**, revised at World Radiocommunication Conferences every three to four years. Satellite operators must file their networks with the ITU through national administrations and coordinate with others to avoid interference — a process that can take years and is a central part of any commercial constellation business plan.

Space engineers use the IEEE radar letter designations for bands (@fig:bands, @tbl:bands).

![Microwave frequency bands used for space communications, with their approximate frequency ranges in GHz. Optical communication uses frequencies about 2 000 times higher than Ka-band.](figures/out/ch07_bands.svg){#fig:bands width=96%}

Table: Principal frequency bands for space communications and their uses. {#tbl:bands}

| Band | Frequency range | Typical space uses | Notes |
|---|---|---|---|
| VHF / UHF | 30–300 MHz / 300 MHz–1 GHz | Amateur and CubeSat TT&C, military UHF SATCOM (MUOS), AIS ship tracking, IoT | Low gain, crowded, ionospheric effects |
| L-band | 1–2 GHz | GNSS (1 164–1 610 MHz), Iridium, Inmarsat, Globalstar uplink, direct-to-device | Penetrates foliage and rain; small antennas |
| S-band | 2–4 GHz | TT&C (2 025–2 110 MHz up, 2 200–2 290 MHz down), Globalstar, some EO, radar | The classic TT&C band |
| C-band | 4–8 GHz | GEO TV distribution, rain-robust trunking, SAR (Sentinel-1, RADARSAT) | Little rain fade; large ground dishes |
| X-band | 8–12 GHz | EO payload downlinks (8 025–8 400 MHz), deep space (7.1–7.2 GHz up, 8.4–8.45 GHz down), military SATCOM, SAR | Workhorse for science downlinks |
| Ku-band | 12–18 GHz | Direct-to-home TV, VSAT, Starlink/OneWeb user links, data relay | Rain fade becomes significant |
| K / Ka-band | 18–40 GHz | High-throughput satellites, gateways, deep-space Ka (31.8–32.3 GHz), EO high-rate (25.5–27 GHz) | Wide bandwidths, strong rain fade |
| Q / V-band | 33–75 GHz | Feeder links for next-generation HTS and constellations | Experimental-to-early operational |
| W-band | 75–110 GHz | Experimental links and radiometry | Research |
| Optical | ≈ 200 THz (1 064 / 1 550 nm) | Laser crosslinks, data relay, deep-space optical | Unregulated by ITU (so far); blocked by cloud |

### Why Higher Frequencies?

Higher frequencies offer more **bandwidth** (and therefore higher data rates) and allow small antennas to form narrow, high-gain beams. Their disadvantages are greater attenuation by rain and atmospheric gases (@fig:atten), the need for more precise antenna pointing, and more expensive components. The trend over 60 years has been steadily upward: from VHF and S-band to X and Ka for downlinks, and now to optical.

![Approximate atmospheric attenuation through the whole atmosphere as a function of frequency: gaseous absorption at zenith and rain attenuation exceeded 0.1 % of the time at 30° elevation in a temperate climate. Above 10 GHz, rain fade dominates link design.](figures/out/ch07_atten.svg){#fig:atten width=86%}

## Antennas

An antenna converts electrical signals into electromagnetic waves and focuses them in a direction. Its key property is **gain** $G$ — how much it concentrates power compared with an isotropic radiator, expressed in dBi. For a parabolic dish of diameter $D$ at wavelength $\lambda$ and aperture efficiency $\eta$ (typically 0.55–0.70):

$$G = \eta\left(\frac{\pi D}{\lambda}\right)^2, \qquad \theta_{3dB} \approx 70\,\frac{\lambda}{D}\ \text{degrees}$$

Gain rises with the square of frequency for a fixed size, while beamwidth shrinks (@fig:antgain). A 34 m Deep Space Network antenna has a gain of about 68 dBi at X-band and 80 dBi at Ka-band, with a Ka beam only 0.017° wide — so pointing must be accurate to a few millidegrees.

![Gain of parabolic antennas as a function of diameter for four frequency bands.](figures/out/ch07_antenna_gain.svg){#fig:antgain width=84%}

Spacecraft use several antenna types (@fig:anttypes):

- **Low-gain antennas (LGAs)** — monopoles, patches, helices with almost hemispherical coverage, used for TT&C in any attitude and in safe mode.
- **Medium-gain antennas** — horns, helices and small arrays with tens of degrees of beamwidth.
- **High-gain antennas (HGAs)** — fixed or steerable parabolic reflectors; deployable mesh reflectors up to 22 m (e.g., on mobile-satellite GEO spacecraft such as TerreStar and AST SpaceMobile's large phased arrays in LEO).
- **Phased arrays** — many small elements whose signals are shifted in phase to steer the beam electronically, with no moving parts. They are now standard on LEO broadband satellites and user terminals (the Starlink user terminal is a phased array of more than a thousand elements) and on SAR satellites.

![Common antenna types used on spacecraft and ground terminals.](figures/out/ch07_antenna_types.svg){#fig:anttypes width=96%}

## The Link Budget

### The Link Equation

The **link budget** is the accounting that shows whether a link closes — whether the received signal is strong enough compared with noise to deliver the required data rate at the required error rate. In decibels, the received carrier power is:

$$C = P_t + G_t - L_t - L_{fs} - L_a - L_{pol} - L_{point} + G_r - L_r \quad [\text{dBW}]$$

where $P_t$ is transmitter power, $G_t$ and $G_r$ are antenna gains, $L_t$ and $L_r$ line losses, $L_a$ atmospheric losses, and $L_{fs}$ is the **free-space path loss**, which describes how power spreads over the surface of an ever-larger sphere:

$$L_{fs} = \left(\frac{4\pi d f}{c}\right)^2 \quad\Rightarrow\quad L_{fs}[\text{dB}] = 92.45 + 20\log_{10} d[\text{km}] + 20\log_{10} f[\text{GHz}]$$

The product $P_t + G_t - L_t$ is the **effective isotropic radiated power (EIRP)**. Path loss grows enormously with distance (@fig:fspl): about 177 dB for a 2 000 km LEO link at X-band, 205 dB to GEO at Ku-band, and about 280 dB to Mars at X-band.

![Free-space path loss versus distance for four frequency bands. Each tenfold increase in distance costs 20 dB.](figures/out/ch07_fspl.svg){#fig:fspl width=86%}

The noise that competes with the signal is characterised by the **noise power spectral density** $N_0 = kT_{sys}$, where $k = 1.38\times10^{-23}$ J/K (−228.6 dBW/K/Hz) is Boltzmann's constant and $T_{sys}$ is the system noise temperature (antenna, sky, receiver). A receiving system's quality is summarised by its **figure of merit** $G/T$ in dB/K. The ratio that matters is

$$\frac{C}{N_0} = \text{EIRP} - L + \frac{G}{T} + 228.6 \quad[\text{dB-Hz}], \qquad \frac{E_b}{N_0} = \frac{C}{N_0} - 10\log_{10} R_b$$

where $R_b$ is the bit rate and $E_b/N_0$ the energy per bit relative to noise density. The link **margin** is the difference between the achieved and the required $E_b/N_0$; designs typically require 3 dB of margin, more for rain-affected links.

::: example
**Worked example — an X-band Earth-observation downlink**

A LEO satellite transmits 10 W (10 dBW) through 1.5 dB of losses into a 6 dBi patch antenna (EIRP = 14.5 dBW) at 8.2 GHz. At 5° elevation from a 600 km orbit, the slant range is about 2 000 km, so $L_{fs}$ = 176.7 dB; atmosphere and rain cost 1.5 dB, pointing and polarisation 1 dB. The ground station has a 5.4 m dish (51 dBi) and $T_{sys}$ = 150 K, so $G/T = 51 - 21.8 = 29.2$ dB/K. Then (@fig:waterfall)

- $C = 14.5 - 176.7 - 2.5 + 51 = -113.7$ dBW
- $C/N_0 = -113.7 - 10\log(1.38\times10^{-23}\times150) = -113.7 + 206.8 = 93.1$ dB-Hz
- For $R_b$ = 500 Mbit/s (87.0 dB-Hz): $E_b/N_0 = 6.1$ dB.

With LDPC-coded QPSK requiring about 3 dB, the margin is about 3 dB — adequate. At higher elevations the range shrinks to 600 km and the margin rises by 10 dB, which modern systems exploit with **variable coding and modulation (VCM)**, increasing the data rate during the pass.
:::

![Signal level through the example X-band downlink: free-space loss dominates, and is recovered mainly by the gain of the ground antenna.](figures/out/ch07_link_waterfall.svg){#fig:waterfall width=92%}

## Modulation and Coding

### Modulation

**Modulation** imprints digital data on the carrier wave by changing its phase, amplitude or frequency. Phase-shift keying is dominant in space (@fig:constel):

- **BPSK** — two phases, 1 bit per symbol, very robust; used for TT&C and deep space.
- **QPSK / OQPSK** — four phases, 2 bits per symbol, same power efficiency as BPSK with twice the spectral efficiency; the workhorse of EO downlinks.
- **8PSK, 16APSK, 32APSK** — more bits per symbol at the cost of needing more $E_b/N_0$; amplitude-phase shift keying (APSK) arranges points on concentric rings to tolerate the non-linear power amplifiers (travelling-wave tube amplifiers, TWTAs) used in space. DVB-S2/S2X and CCSDS 131.2 support them with adaptive switching.
- **GMSK and filtered modulations** — constant-envelope, spectrally compact schemes.

Ranging signals (tones or pseudo-noise codes) can share the carrier with data to measure distance.

![Constellation diagrams of common modulation schemes with noise. Denser constellations carry more bits per symbol but need a stronger signal to separate the points.](figures/out/ch07_constellations.svg){#fig:constel width=96%}

### Error-Correcting Codes

Claude Shannon showed in 1948 that the maximum error-free data rate (capacity) of a channel of bandwidth $B$ is

$$C = B\log_2\left(1 + \frac{S}{N}\right)$$

and that, for any rate below capacity, a code exists that makes errors arbitrarily rare. The ultimate limit is $E_b/N_0 = -1.59$ dB. **Forward error correction (FEC)** codes add redundant bits that let the receiver correct errors; the improvement is called the **coding gain** (@fig:ber). Space communications have driven coding theory for 60 years:

- **Reed–Muller codes** on Mariner 6/7/9 (1969–1971).
- **Convolutional codes with Viterbi decoding** (rate 1/2, constraint length 7) — the standard from Voyager onwards.
- **Concatenated Reed–Solomon + convolutional codes** — Voyager at Uranus and Neptune, Galileo, and many EO missions.
- **Turbo codes** (invented 1993; CCSDS standard 1999) — within 1 dB of the Shannon limit; used on MRO, New Horizons, MESSENGER and many deep-space missions.
- **Low-density parity-check (LDPC) codes** — near-Shannon performance with efficient parallel decoding; standardised in CCSDS 131.0 (AR4JA codes for deep space, rate 7/8 for near-Earth) and DVB-S2 for commercial satellite broadband.

![Bit error rate versus Eb/N0 for uncoded and coded transmission. Modern turbo and LDPC codes operate within about 1–2 dB of the Shannon limit, a gain of roughly 9 dB over uncoded transmission — equivalent to an eightfold increase in transmitter power or antenna area.](figures/out/ch07_ber.svg){#fig:ber width=86%}

Data is also **compressed** before transmission. CCSDS standards include lossless compression (CCSDS 121.0, based on Rice coding), image compression (CCSDS 122.0, wavelet-based) and multispectral/hyperspectral compression (CCSDS 123.0). Onboard AI that discards cloudy images or extracts only events of interest is an increasingly powerful form of "compression" (Chapter 44).

## Optical (Laser) Communications

**Free-space optical communications** use lasers at near-infrared wavelengths (1 064 or 1 550 nm). Because the wavelength is about 10 000 times shorter than X-band, a 10 cm telescope produces a beam about 10 µrad wide — far narrower than any radio beam — concentrating the power on the receiver. Optical links offer data rates of gigabits to hundreds of gigabits per second, use spectrum that is not (yet) regulated, and are very hard to intercept or jam. Their challenges are clouds (which block the beam entirely), precise pointing, acquisition and tracking (to microradians while both terminals move), and atmospheric turbulence.

Milestones include:

- **LLCD** (NASA, 2013) — 622 Mbit/s from lunar orbit on LADEE.
- **EDRS** (ESA/Airbus "SpaceDataHighway", 2016 onwards) — GEO relay nodes receiving 1.8 Gbit/s laser links from Sentinel-1 and Sentinel-2 satellites and relaying the data to Europe in near-real time.
- **LCRD** (NASA, 2021) — a GEO laser relay, linked with the **ILLUMA-T** terminal on the ISS in 2023.
- **TBIRD** (NASA/MIT Lincoln Laboratory, 2022) — a CubeSat terminal that downlinked at 200 Gbit/s.
- **DSOC** (NASA/JPL, on the Psyche mission, 2023–2025) — the first deep-space laser link, achieving 267 Mbit/s from 33 million km and continuing to link from beyond Mars' distance, with a superconducting nanowire photon-counting detector at Palomar Observatory.
- **Optical inter-satellite links in mega-constellations** — Starlink satellites carry three or more laser terminals, forming a mesh network in space carrying many petabytes per day; the US Space Development Agency's Transport Layer also uses optical crosslinks; China's constellations are adopting them.
- **Artemis II's O2O terminal** (2026) — a laser link returning high-definition video from Orion during the crewed lunar flight.

![The Deep Space Optical Communications (DSOC) flight laser transceiver before integration with NASA's Psyche spacecraft. Its 22 cm telescope sent the first high-rate laser signals from deep space.](figures/photos/ch07_dsoc_ftl.jpg){#fig:dsoc width=70%}

![Artist's illustration of the ILLUMA-T terminal on the International Space Station relaying data by laser through the LCRD relay satellite in geostationary orbit.](figures/photos/ch07_illumat.jpg){#fig:illumat width=80%}

@fig:datarates shows how the best achievable data rates have grown by more than ten orders of magnitude since the first planetary missions.

![Representative space communication data rates since 1965. Laser links have pushed rates into the tens and hundreds of gigabits per second.](figures/out/ch07_data_rates.svg){#fig:datarates width=90%}

## The Ground Segment

### Architecture

The **ground segment** comprises all the ground facilities needed to operate the spacecraft and exploit its data (@fig:groundarch):

- **Ground stations** with antennas, RF equipment (low-noise amplifiers, high-power amplifiers, up/down-converters), modems/baseband units, timing, and network connections.
- **Mission operations centre (MOC)** — the control room where flight controllers monitor telemetry, send commands, and respond to anomalies, using a **mission control system** (e.g., ESA's SCOS-2000 and its successor EGS-CC, NASA's ITOS and AMMOS, or open-source frameworks such as Yamcs and OpenMCT).
- **Flight dynamics** — orbit determination, manoeuvre planning, attitude reconstruction, collision avoidance, and product generation (ephemerides, pointing predictions).
- **Mission planning and scheduling** — turning user requests into conflict-free activity timelines that respect power, thermal, data-volume and visibility constraints (Chapter 45 discusses AI planners).
- **Payload data ground segment (PDGS)** — receiving, processing, calibrating, archiving and distributing payload data. Processing levels follow a standard ladder: Level 0 (raw, time-ordered), Level 1 (calibrated, geolocated), Level 2 (geophysical variables), Level 3 (gridded, composited), Level 4 (model output) (Chapter 13).
- **Security** — encryption and authentication of telecommands (e.g., CCSDS Space Data Link Security), network segmentation, intrusion detection, and protection of ground systems, which are the most frequently attacked part of space systems.

![Elements of a typical ground segment and their data flows.](figures/out/ch07_ground_arch.svg){#fig:groundarch width=96%}

### Ground Station Networks

A LEO satellite is visible from a given station for only 5–15 minutes per pass, and from a mid-latitude station for only a few passes a day. Polar-orbiting satellites, however, pass over the poles on every orbit, so stations at high latitudes see every orbit (@fig:contact). This is why **Svalbard** (78° N, KSAT's SvalSat with more than 100 antennas), **Inuvik**, **Kiruna**, **Fairbanks** and Antarctic stations such as **Troll** (72° S) and **McMurdo** host so many antennas.

![Daily contact time between a 600 km sun-synchronous satellite and a ground station, as a function of station latitude, computed for this manual. A polar station sees the satellite for several times longer than an equatorial one.](figures/out/ch07_contact_time.svg){#fig:contact width=86%}

Operators increasingly buy **ground-station-as-a-service**, paying per pass or per minute on shared networks: KSAT, SSC (Swedish Space Corporation), AWS Ground Station, Microsoft Azure Orbital (partnered networks), Leaf Space, Atlas Space Operations, RBC Signals and others. Electronically steered **phased-array ground stations** and software-defined radios allow one site to track several satellites at once. Data relay satellites in GEO — NASA's **TDRS** constellation, ESA's **EDRS**, China's **Tianlian**, Russia's **Luch** — provide nearly continuous contact for the ISS, Hubble, Tiangong and Earth-observation satellites.

### Deep Space Communications

Deep-space missions require the largest antennas, the most sensitive receivers and the most powerful transmitters on Earth. NASA's **Deep Space Network (DSN)** has three complexes spaced about 120° apart in longitude — **Goldstone** (California), **Madrid** (Spain) and **Canberra** (Australia) — so that any spacecraft beyond a few thousand kilometres is always visible from at least one (@fig:dsnmap). Each complex has a 70 m antenna and several 34 m beam-waveguide antennas; new 34 m antennas were added under the DSN Aperture Enhancement Project (DSS-53 in Madrid in 2022, DSS-56 and others). Antennas can be **arrayed** to combine their signals, as at Madrid in 2024, where six antennas were arrayed together for the first time to receive Voyager-class signals.

![Locations of the three Deep Space Network complexes.](figures/out/ch07_dsn_map.png){#fig:dsnmap width=94%}

::: figrow
![Six DSN antennas at the Madrid complex arrayed for the first time in April 2024 to receive a single spacecraft's signal.](figures/photos/ch07_madrid.jpg){#fig:madrid}

![The 34 m beam-waveguide antenna DSS-53, added to the Madrid complex in 2022.](figures/photos/ch07_dss53.jpg){#fig:dss53}
:::

Other agencies operate complementary networks: ESA's **ESTRACK** with 35 m deep-space antennas at New Norcia (Australia), Cebreros (Spain) and Malargüe (Argentina); China's deep-space network with 35 m and 66 m antennas at Kashgar, Jiamusi and Zapala (Argentina); India's IDSN at Byalalu; JAXA's 54 m Misasa antenna; and Russia's network. **Cross-support** agreements using CCSDS standards let agencies track each other's missions.

The DSN is heavily oversubscribed: in the late 2020s it supports more than 40 missions, and demand from lunar missions (Artemis, CLPS landers, international orbiters) is growing. NASA is complementing it with commercial lunar communication services and with optical ground stations.

::: data
**Data box — talking to Voyager 1**

- Distance (October 2026): about 171 AU, or 25.6 billion km; one-way light time ≈ 23.7 hours (it reaches one light-day from Earth in late 2026).
- Transmitter: about 22 W at 8.4 GHz through a 3.7 m dish (gain ≈ 48 dBi, EIRP ≈ 61 dBW).
- Free-space loss ≈ 319 dB; received power at a 70 m DSN antenna ≈ 4 × 10⁻¹⁹ W (−184 dBW).
- Downlink rate: 160 bit/s (science), reduced over the years as power and distance changed.
- Commands are sent with transmitters of 20 kW or more; a round-trip command-and-response takes almost two days.
:::

### Delay- and Disruption-Tolerant Networking

The Internet assumes continuous end-to-end connectivity and round-trip times of milliseconds. In space, links are intermittent and delays can be minutes or hours. **Delay/Disruption-Tolerant Networking (DTN)** uses the **Bundle Protocol** to store data at each node until the next link is available ("store-and-forward"), forming an interplanetary internet. NASA has used DTN on the ISS since 2016 and in the PACE Earth-observation mission (2024); it is a core element of **LunaNet**, the planned interoperable network of lunar relays and services, and of ESA's **Moonlight** initiative.

## Space Data Standards: CCSDS

The **Consultative Committee for Space Data Systems (CCSDS)**, founded in 1982 by the major space agencies, develops open standards ("Blue Books") for space communications and data handling. Using CCSDS standards lets spacecraft use any compliant ground station and lets agencies share hardware and software. @fig:ccsds shows the main layers.

![The CCSDS protocol stack used by most civil spacecraft, from physical-layer modulation up to file delivery and mission operations services.](figures/out/ch07_ccsds.svg){#fig:ccsds width=94%}

Key CCSDS standards include Space Packets (133.0), TM/TC/AOS frames (132.0/232.0/732.0), the Unified Space Data Link Protocol (USLP, 732.1), channel coding (131.0, 231.0), the CCSDS File Delivery Protocol (CFDP, 727.0), Space Data Link Security (355.0), the Bundle Protocol (734.2) and optical communications (141.0, 142.0). Commercial communications satellites use the DVB-S2/S2X family; LEO broadband constellations use proprietary protocols; and **3GPP non-terrestrial network (NTN)** standards (from Release 17 onwards) integrate satellites into 5G mobile networks (Chapter 17).

::: key
**Key takeaways**

- TT&C links control the spacecraft; payload links deliver its product. Frequencies are allocated by the ITU; higher bands give more bandwidth but suffer rain fade.
- The link budget — EIRP minus losses plus G/T — determines C/N₀ and Eb/N₀; free-space loss grows 20 dB per decade of distance.
- Modern LDPC and turbo codes operate within 1–2 dB of the Shannon limit; adaptive coding and modulation use every available dB.
- Laser links deliver gigabit-to-hundreds-of-gigabit rates and now connect satellites in constellations, relays in GEO and even deep-space probes.
- The ground segment includes stations, mission control, flight dynamics, planning and payload data processing; polar stations and relay satellites maximise contact time; the DSN's three complexes provide continuous deep-space coverage.
- CCSDS standards enable interoperability; DTN extends the Internet to intermittent space links.
:::

::: questions
**Review questions**

1. Distinguish TT&C links from payload data links and give typical frequency bands for each.
2. Calculate the gain of a 3.7 m ground antenna with 60 % efficiency at 8.2 GHz.
3. Calculate the free-space path loss at 2.2 GHz over a slant range of 2 000 km.
4. Write the link equation for *C*/*N*₀ and explain each term. Why does −228.6 dBW/(K Hz) appear?
5. Why do modern links use LDPC or turbo codes? What does "within 1–2 dB of the Shannon limit" mean?
6. Give two advantages and two disadvantages of laser communication compared with radio.
7. Why are many ground stations for polar-orbiting satellites located at high latitudes?
8. Why does deep-space communication need very large antennas and three stations spaced around the world?
9. What problem does delay- and disruption-tolerant networking solve, and how?
:::
