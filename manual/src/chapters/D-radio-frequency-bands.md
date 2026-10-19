---
title: Radio-Frequency Bands and Spectrum
abstract: A quick reference to the radio spectrum as used in space — the ITU and IEEE band names, the frequencies allocated to telemetry and command, deep-space, Earth observation, satellite communication and navigation services, the bands used by radars and radiometers, how the atmosphere and rain attenuate each band, free-space path loss from LEO to the outer planets, optical-communication wavelengths, and the international rules that govern who may transmit where.
---

Every satellite depends on the radio spectrum — to be commanded, to send its data home, to navigate, or to sense the Earth. Spectrum is a finite natural resource shared by all nations, managed through the International Telecommunication Union (ITU) and its Radio Regulations. This appendix gathers the frequencies and rules referred to in Chapters 7, 13, 15, 16, 17, 18 and 24. Band edges are approximate and simplified; the exact allocation for any service depends on the ITU Region (Region 1: Europe, Africa, the Middle East and northern Asia; Region 2: the Americas; Region 3: the rest of Asia and Oceania) and on national rules.

## Band Names

Two naming systems are in use. The ITU names bands by decade of frequency (@tbl:apxitubands); the radar "letter bands" standardised by the IEEE (@tbl:apxieeebands) are what satellite engineers use day to day. The letters began as wartime secrecy codes, which is why they follow no logical order.

::: small
| ITU band no. | Name | Frequency | Wavelength | Typical space uses |
|---|---|---|---|---|
| 4 | VLF (very low) | 3–30 kHz | 100–10 km | Whistlers and plasma waves measured by science payloads |
| 5 | LF (low) | 30–300 kHz | 10–1 km | Ground navigation (Loran), not used for space links |
| 6 | MF (medium) | 0.3–3 MHz | 1 000–100 m | Reflected by the ionosphere; radio astronomy impossible from the ground |
| 7 | HF (high) | 3–30 MHz | 100–10 m | Ionospheric sounding; amateur satellites (rare) |
| 8 | VHF (very high) | 30–300 MHz | 10–1 m | CubeSat and amateur links (145 MHz), weather APT (137 MHz), AIS (162 MHz) |
| 9 | UHF (ultra high) | 300 MHz–3 GHz | 1 m–10 cm | CubeSat TT&C (435–438 MHz), military narrowband satcom, GNSS, mobile satcom, S-band TT&C |
| 10 | SHF (super high) | 3–30 GHz | 10–1 cm | C, X, Ku and Ka bands: most satellite communication, SAR, EO downlinks |
| 11 | EHF (extremely high) | 30–300 GHz | 10–1 mm | Ka, Q/V and E bands; protected military satcom (44 GHz); radiometry |
| 12 | THF (tremendously high) | 0.3–3 THz | 1–0.1 mm | Sub-millimetre astronomy and limb sounders |

: ITU frequency band designations. {#tbl:apxitubands}
:::

::: small
| Letter band | Frequency (GHz) | Wavelength | Typical space uses |
|---|---|---|---|
| L | 1–2 | 30–15 cm | GNSS, mobile satcom (Inmarsat, Iridium), L-band SAR, weather-satellite direct broadcast |
| S | 2–4 | 15–7.5 cm | TT&C, deep space (legacy), mobile satcom, S-band SAR |
| C | 4–8 | 7.5–3.75 cm | Fixed satellite service (TV distribution), C-band SAR (Sentinel-1) |
| X | 8–12 | 3.75–2.5 cm | Deep space, EO data downlinks, military satcom, X-band SAR |
| Ku | 12–18 | 2.5–1.67 cm | Direct-to-home TV, broadband (Starlink user links), altimeters, ISS Ku-band |
| K | 18–27 | 1.67–1.11 cm | Ka-band downlinks (17.7–21.2 GHz), EESS data downlink (25.5–27 GHz) |
| Ka | 27–40 | 11.1–7.5 mm | Uplinks of high-throughput satellites, deep-space Ka-band, SWOT radar interferometer |
| V | 40–75 | 7.5–4 mm | Q/V-band feeder links, oxygen-band temperature sounding (50–60 GHz) |
| W | 75–110 | 4–2.7 mm | E-band feeder links (71–86 GHz), cloud radars (94 GHz) |

: IEEE radar letter bands (IEEE Std 521) and their main space uses. Note that the satellite industry often calls 17.7–21.2 GHz "Ka-band downlink" although it lies in the IEEE K band. {#tbl:apxieeebands}
:::

@fig:apxbandmap places the main space services on a single logarithmic frequency axis.

![The radio spectrum used in space, from VHF to E-band. Coloured bars show approximate allocations for the main satellite services; the triangles mark the centre frequencies of the radar bands used by imaging radars, and the dots mark some of the passive bands that radiometers use and that are protected from transmissions.](figures/out/apxD_bandmap.svg){#fig:apxbandmap width=98%}

## Telemetry, Command and Deep-Space Frequencies

Telemetry, tracking and command (TT&C) and science downlinks use bands allocated to the *space operation*, *space research* and *Earth exploration-satellite* (EESS) services. The ITU distinguishes *Category A* missions, within 2 million km of Earth, from *Category B* deep-space missions beyond that distance, which use separate, specially protected sub-bands because their signals arrive extremely weak (@tbl:apxttc).

::: small
| Use | Earth-to-space (uplink) | Space-to-Earth (downlink) | Examples |
|---|---|---|---|
| Amateur-satellite and CubeSats | 144–146 MHz; 435–438 MHz | same bands | University CubeSats, AMSAT |
| Near-Earth S-band TT&C | 2 025–2 110 MHz | 2 200–2 290 MHz | Almost all LEO and GEO satellites, ISS, launchers |
| Near-Earth X-band | 7 190–7 235 MHz | 8 450–8 500 MHz | Lunar and L1/L2 missions |
| EESS X-band data downlink | — | 8 025–8 400 MHz | Landsat, Sentinel, commercial EO |
| EESS / space research Ka-band | 22.55–23.15 GHz | 25.5–27.0 GHz | JPSS, NISAR, SWOT, Euclid, Roman, TDRS |
| Deep space S-band (Cat. B) | 2 110–2 120 MHz | 2 290–2 300 MHz | Legacy missions, Voyager (S/X) |
| Deep space X-band (Cat. B) | 7 145–7 190 MHz | 8 400–8 450 MHz | Workhorse band of the DSN, ESTRACK and CDSN |
| Deep space Ka-band (Cat. B) | 34.2–34.7 GHz | 31.8–32.3 GHz | Kepler; MRO demonstration; radio science on Cassini, Juno and BepiColombo |
| Mars and lunar proximity links | 435–450 MHz (to surface) | 390–405 MHz (from surface) | Electra relay radios on Mars orbiters, rovers and landers |

: Frequencies for telemetry, command and science data (simplified). {#tbl:apxttc}
:::

## Communication and Broadcasting Satellites

::: small
| Band | Downlink | Uplink | Services and users |
|---|---|---|---|
| UHF (military) | 240–270 MHz; MUOS 360–380 MHz | 290–320 MHz; MUOS 300–320 MHz | Narrowband tactical satcom (UFO legacy channels, MUOS) |
| L (mobile) | 1 518–1 559 MHz | 1 626.5–1 660.5 MHz | Inmarsat, Ligado/Viasat, Thuraya |
| L (Iridium) | 1 616–1 626.5 MHz | same (time-division) | Iridium voice, data and Certus |
| L/S (Globalstar) | 2 483.5–2 500 MHz | 1 610–1 618.725 MHz | Globalstar; Apple emergency SOS |
| S (2 GHz MSS) | 2 170–2 200 MHz | 1 980–2 010 MHz | EchoStar, EU 2 GHz MSS; spectrum SpaceX agreed to buy in 2025 for direct-to-device |
| Cellular (direct-to-device) | 600 MHz – 2.7 GHz | same | Terrestrial mobile bands reused from space: T-Mobile/Starlink, AST SpaceMobile |
| C | 3.7–4.2 GHz | 5.925–6.425 GHz | TV distribution, maritime, trunking; US 3.7–3.98 GHz cleared for 5G in 2020–23 |
| X (military) | 7.25–7.75 GHz | 7.9–8.4 GHz | WGS, Skynet, Syracuse, SATCOMBw |
| Ku | 10.7–12.75 GHz | 12.75–13.25, 13.75–14.5 GHz | Direct-to-home TV, VSAT, Starlink and OneWeb user links, aero and maritime |
| Ka (commercial) | 17.7–20.2 GHz | 27.5–30.0 GHz | High-throughput satellites (ViaSat-3, Jupiter), gateways, ESIM |
| Ka (government) | 20.2–21.2 GHz | 30.0–31.0 GHz | WGS, military high-throughput payloads |
| Q/V | 37.5–42.5 GHz | 47.2–50.2, 50.4–51.4 GHz | Gateway (feeder) links for new constellations |
| EHF (protected) | 20.2–21.2 GHz | 43.5–45.5 GHz | AEHF and its successor ESS — anti-jam, nuclear-survivable |
| E | 71–76 GHz | 81–86 GHz | Experimental gateway links |

: Main satellite communication bands (simplified). {#tbl:apxcommbands}
:::

## Navigation Signals

Global navigation satellite systems share three frequency regions: 1 164–1 215 MHz (lower L-band), 1 215–1 300 MHz, and 1 559–1 610 MHz (upper L-band). Systems deliberately share centre frequencies (1 575.42 MHz and 1 176.45 MHz) so that one antenna and receiver front end can use satellites from several constellations (Chapter 18).

::: small
| System | Signal | Centre frequency (MHz) | Notes |
|---|---|---|---|
| GPS | L1 C/A, L1C | 1 575.42 | 1.023 Mchip/s C/A code, used by every receiver |
| | L2C, P(Y) | 1 227.60 | Second civil frequency for ionospheric correction |
| | L5 | 1 176.45 | Safety-of-life signal, 10.23 Mchip/s |
| Galileo | E1 | 1 575.42 | Open Service; OSNMA authentication |
| | E5a / E5b | 1 176.45 / 1 207.14 | Wideband AltBOC signal |
| | E6 | 1 278.75 | High Accuracy Service (≈ 20 cm) |
| GLONASS | L1OF / L2OF | 1 602 + 0.5625 *k* / 1 246 + 0.437 5 *k* | FDMA: channel *k* from −7 to +6 |
| | L3OC | 1 202.025 | New CDMA signal |
| BeiDou | B1I / B1C | 1 561.098 / 1 575.42 | |
| | B2a / B2b | 1 176.45 / 1 207.14 | B2b carries PPP corrections |
| | B3I | 1 268.52 | |
| QZSS | L1, L2, L5, L6 | as GPS; L6 1 278.75 | Centimetre-level augmentation (CLAS) on L6 |
| NavIC | L5, S | 1 176.45 / 2 492.028 | L1 added on second-generation satellites |
| SBAS | L1, L5 | 1 575.42 / 1 176.45 | WAAS, EGNOS, MSAS, GAGAN, SouthPAN |

: GNSS signals. GPS signals arrive at the ground with a minimum power of about −158.5 dBW — far below the noise. {#tbl:apxgnss}
:::

## Remote-Sensing Frequencies

### Active Sensors

Radar imagers and altimeters choose their band by trading resolution and antenna size against penetration of vegetation, soil and rain (Chapter 15). Longer wavelengths penetrate further into forest canopies and dry soil; shorter wavelengths give finer detail with smaller antennas.

::: small
| Band | Centre frequency | Wavelength | What it sees | Missions |
|---|---|---|---|---|
| P | 435 MHz | 69 cm | Penetrates forest canopy to trunks and branches | ESA BIOMASS (launched April 2025) |
| L | 1.26 GHz | 24 cm | Forests, soil moisture, ground deformation, ice | ALOS-2/ALOS-4, SAOCOM, NISAR (L) |
| S | 3.2 GHz | 9.4 cm | Crops, snow, sea ice | NISAR (S), NovaSAR-1 |
| C | 5.405 GHz | 5.5 cm | All-round monitoring, sea ice, winds, floods | Sentinel-1, RADARSAT Constellation, Gaofen-3 |
| X | 9.65 GHz | 3.1 cm | High-resolution imaging, change detection | TerraSAR-X/TanDEM-X, COSMO-SkyMed, ICEYE, Capella, Umbra |
| Ku | 13.575 GHz | 2.2 cm | Sea-surface height, winds, rain | Sentinel-3 and Sentinel-6 altimeters, GPM (13.6 GHz) |
| Ka | 35.75 GHz | 8.4 mm | Water-surface topography, snow, light rain | SWOT KaRIn, SARAL/AltiKa, GPM (35.5 GHz) |
| W | 94.05 GHz | 3.2 mm | Cloud droplets and ice | CloudSat, EarthCARE |

: Radar bands used by imaging radars, altimeters and cloud and rain radars. {#tbl:apxsarbands}
:::

### Passive Sensors

Microwave radiometers measure the natural thermal emission of the Earth's surface and atmosphere. They rely on frequencies set by physics — the oxygen absorption complex near 50–60 GHz for temperature profiles, the 22.235 GHz and 183.31 GHz water-vapour lines for humidity, the 1.4 GHz "window" for soil moisture and ocean salinity. Because those frequencies cannot be moved, the Radio Regulations protect them: in bands such as 1 400–1 427 MHz, 23.6–24.0 GHz and 50.2–50.4 GHz *all emissions are prohibited*. Unwanted emissions from neighbouring services remain a concern: the decision at the 2019 World Radiocommunication Conference on 5G emissions next to the 23.8 GHz water-vapour band was criticised by meteorologists as too permissive.

## Propagation Through the Atmosphere

The atmosphere is nearly transparent to radio below about 10 GHz, but above that gases and rain absorb increasingly (@fig:apxatten). Clear-sky absorption peaks at the oxygen lines (60 GHz and 118.75 GHz) and the water-vapour lines (22.2 GHz and 183.3 GHz); between them lie *windows* near 35, 94 and 140 GHz used by radars and radiometers. Rain is usually the larger problem for satellite links: at Ku-band a heavy shower (25 mm/h) attenuates about 1 dB per kilometre of rain path, at Ka-band (30 GHz) about 5 dB/km. Link designers therefore add a *rain margin* chosen from the statistics of rain at each ground station — for example, enough to keep the link closed for 99.9 % of an average year — and use adaptive coding and modulation, site diversity and uplink power control to ride out the worst storms. The ionosphere affects lower frequencies instead: it delays GNSS signals by up to tens of metres, rotates the polarisation of VHF and UHF signals (Faraday rotation) and causes scintillation near the equator and the poles (Chapter 23).

![Atmospheric attenuation of radio waves. Left: clear-sky attenuation by oxygen and water vapour for a path looking straight up from sea level, computed with the ITU-R P.676 line-by-line model. Right: specific attenuation by rain for three rain rates, from ITU-R P.838; the total rain loss is this value multiplied by the length of the path through rain, typically a few kilometres.](figures/out/apxD_atten.svg){#fig:apxatten width=100%}

## Free-Space Path Loss

Most of the loss in any space link is simply geometric spreading. The *free-space path loss* between isotropic antennas is

$$ L_\mathrm{fs}\,(\mathrm{dB}) = 92.45 + 20\log_{10} f_\mathrm{GHz} + 20\log_{10} d_\mathrm{km} $$

so every doubling of distance or frequency costs 6 dB. (The frequency dependence is offset by the higher gain of an antenna of a given size at higher frequency, which is why deep-space links moved from S- to X- to Ka-band.) @tbl:apxfspl gives typical values.

::: small
| Link | Distance | 437 MHz | 2.2 GHz | 8.4 GHz | 20 GHz | 32 GHz |
|---|---|---|---|---|---|---|
| LEO, overhead | 550 km | 140.1 | 154.1 | 165.7 | 173.3 | 177.4 |
| LEO, low elevation | 2 000 km | 151.3 | 165.3 | 177.0 | 184.5 | 188.6 |
| GEO | 38 000 km | 176.9 | 190.9 | 202.5 | 210.1 | 214.1 |
| Moon | 384 400 km | 197.0 | 211.0 | 222.6 | 230.2 | 234.2 |
| Sun–Earth L2 | 1.5 million km | 208.8 | 222.8 | 234.5 | 242.0 | 246.1 |
| Mars, closest | 0.37 au | 240.2 | 254.2 | 265.9 | 273.4 | 277.5 |
| Mars, farthest | 2.67 au | 257.3 | 271.3 | 283.0 | 290.5 | 294.6 |
| Jupiter | 6.2 au | 264.6 | 278.6 | 290.3 | 297.8 | 301.9 |
| Voyager 1 (2026) | ≈ 170 au | 293.4 | 307.4 | 319.0 | 326.6 | 330.7 |

: Free-space path loss (dB) for typical space links. {#tbl:apxfspl}
:::

## Optical Communication Wavelengths

Laser links avoid spectrum licensing for the beam itself and offer far higher data rates from small terminals (Chapters 7 and 17). Most terminals work at the telecommunication wavelength of 1 550 nm, where fibre-optic components such as erbium-doped amplifiers are mature; some use 1 064 nm (Nd:YAG lasers). Examples include NASA's LCRD relay (1.2 Gbit/s, 2021), the TBIRD CubeSat (200 Gbit/s bursts, 2022–23), the DSOC experiment on Psyche (267 Mbit/s from 33 million km in 2023, and links from beyond the distance of Mars until 2025), the European Data Relay System (1.8 Gbit/s at 1 064 nm), the inter-satellite lasers of Starlink, and the optical terminals specified by the US Space Development Agency for its Proliferated Warfighter Space Architecture. Clouds block optical links, so ground networks use several geographically separated stations.

## Who Decides: Spectrum Regulation

**The ITU Radio Regulations** are an international treaty, revised every three to four years by a World Radiocommunication Conference (WRC). They allocate each band to one or more *services* (fixed-satellite, mobile-satellite, broadcasting-satellite, radionavigation-satellite, Earth exploration-satellite, space research, space operation, radio astronomy and others) with primary or secondary status. WRC-23 (Dubai, 2023) opened Ka-band to earth stations in motion communicating with non-geostationary satellites and placed direct-to-device satellite connectivity in mobile bands and lunar-surface communications on the agenda of WRC-27, due in late 2027.

**Filing and coordination.** Before a satellite network can use a frequency, its national administration files it with the ITU Radiocommunication Bureau — first an advance publication or coordination request, then a notification for recording in the Master International Frequency Register. Coordination with earlier filings is negotiated between administrations; date priority ("first come, first served") governs most bands, while some broadcasting and fixed-satellite bands are governed by *plans* that guarantee each country access.

**Non-geostationary constellations.** Article 22 of the Radio Regulations sets *equivalent power flux-density* (EPFD) limits that protect geostationary networks from interference by non-geostationary constellations in shared Ku- and Ka-bands. Since WRC-19, a constellation must bring 10 % of its filed satellites into use within two years of the end of its seven-year regulatory period, 50 % within five years and 100 % within seven years, or its filing is reduced — a rule that discourages "paper satellites" (Chapter 17).

**National licensing.** Operators also need licences from their own regulator — in the United States the Federal Communications Commission (FCC) for commercial systems and the NTIA for federal ones; in the United Kingdom Ofcom — and landing rights in each country they serve.

::: key
**Key takeaways**

- Satellite engineers name bands by IEEE letters: L, S, C, X, Ku, K, Ka, V, W. The ITU allocates spectrum by service and Region.
- TT&C lives in S-band; deep space in X- and Ka-band sub-bands reserved for distances beyond 2 million km.
- GNSS signals cluster at 1 176, 1 207–1 278 and 1 575 MHz; shared centre frequencies enable multi-constellation receivers.
- Above 10 GHz rain fade dominates link margins; gas absorption peaks at 22, 60, 118 and 183 GHz.
- Free-space loss rises 6 dB per doubling of distance or frequency — from about 154 dB for LEO S-band to over 280 dB for Mars X-band.
- Spectrum is a treaty-governed shared resource: filings, coordination, EPFD limits and milestones shape every constellation.
:::
