---
title: The Space Ecosystem: An Overview
hero: ch01
abstract: Space is not one place or one industry. It is a layered environment that begins a few tens of kilometres above our heads and stretches to interstellar space, and an interconnected ecosystem of vehicles, ground systems, users, companies, governments and rules. This chapter maps that ecosystem, defines the regimes in which space systems operate, describes the segments of every space system, and summarises the history, economics, statistics and governance that shape it today.
---

## Where Does Space Begin?

There is no physical surface where the atmosphere stops and space starts. Air simply becomes thinner with height: at 5.5 km half of the atmosphere's mass is below you, at 16 km about 90 %, and at 50 km more than 99.9 %. Engineers therefore use *functional* boundaries — heights at which the physics that governs a vehicle changes.

The best-known boundary is the **Kármán line** at **100 km**. It is named after Theodore von Kármán, who noticed that an aircraft trying to fly at about this height would need to travel so fast to generate enough lift that it would already be close to orbital speed. Above it, wings are useless; a vehicle must either follow a ballistic path or be in orbit. The Fédération Aéronautique Internationale (FAI) uses 100 km for astronautics records. The United States Air Force, NASA and the US Federal Aviation Administration award astronaut wings above **50 miles (80.5 km)**, and some scientists argue that 80 km is physically better justified, because satellites with very low perigees can briefly dip to about 80–90 km without immediately re-entering.

Neither number is a legal border. International law has never defined where national airspace ends and outer space begins. In practice, no satellite can stay in orbit for long below about 160 km, because atmospheric drag removes its energy within days.

![The regimes of near-Earth and cislunar space shown on a logarithmic distance scale. Each order of magnitude in altitude corresponds to a different class of vehicle and a different engineering problem: aerodynamics and buoyancy below 50 km, ballistic flight up to a few hundred kilometres, orbital mechanics beyond, and interplanetary trajectories past the Moon.](figures/out/ch01_regimes.svg){#fig:regimes width=96%}

@fig:regimes and @tbl:regimes summarise the regimes used throughout this manual. Moving outward, each regime adds new challenges: lower air density first removes lift and cooling, then oxygen for air-breathing engines, then protection from radiation and debris; finally distance itself becomes the problem, delaying radio signals by seconds, minutes or hours.

Table: Altitude regimes and the vehicles that operate in them. {#tbl:regimes}

| Regime | Typical altitude or distance | Main vehicles | Dominant physics / engineering problem |
|---|---|---|---|
| Troposphere | 0–12 km (0–18 km at the equator) | Aircraft, drones, weather balloons | Weather, lift, air-breathing propulsion |
| Stratosphere | 12–50 km | HAPS (solar aircraft, airships), stratospheric balloons, U-2/ER-2 | Low density, extreme cold (−56 °C), ozone, UV, long endurance |
| Mesosphere / lower thermosphere ("near space" / "ignorosphere") | 50–100 km | Sounding rockets, suborbital vehicles, re-entering spacecraft | Too thin for aircraft, too dense for satellites; meteors burn up here |
| Suborbital | apogee 80–1 500 km | New Shepard, sounding rockets, ballistic missiles, test vehicles | Ballistic flight, minutes of microgravity, re-entry heating |
| Low Earth orbit (LEO) | 160–2 000 km | ISS, Tiangong, Starlink, Earth observation | Drag, atomic oxygen, debris, short ground contacts |
| Medium Earth orbit (MEO) | 2 000–35 786 km | GPS, Galileo, GLONASS, BeiDou, O3b mPOWER | Van Allen radiation belts, longer links |
| Geosynchronous orbit (GEO) | 35 786 km altitude (42 164 km radius) | Communications, weather, missile warning | Station-keeping, 0.24 s round-trip delay, crowded arc |
| Highly elliptical orbit (HEO) | perigee ~500 km, apogee ~40 000 km | Molniya/Tundra comms, early warning | Repeated belt crossings, high-latitude coverage |
| Cislunar space | to 384 400 km (Moon) and Earth–Moon L1/L2 | Orion, lunar orbiters, landers, CAPSTONE | Three-body dynamics, deep-space communications |
| Sun–Earth Lagrange points | 1.5 million km | SOHO, DSCOVR, JWST, Euclid, Roman | Halo orbits, thermal stability, station-keeping |
| Interplanetary / deep space | 0.4–100+ AU | Planetary probes, orbiters, landers, Voyager | Light-time delay, power far from the Sun, autonomy |

::: key
**Key concept — space is about speed, not height**

Reaching 100 km altitude needs only about 1.4 km/s of velocity change if you go straight up and come straight down. Staying in space at 400 km needs a horizontal speed of about **7.7 km/s** — roughly 28 000 km/h. Getting to orbit is therefore mostly a problem of going *sideways fast enough* that the ground curves away beneath you as quickly as you fall towards it. This is why an orbital rocket is roughly ten to twenty times larger than a suborbital rocket carrying the same payload.
:::

## The Segments of a Space System

Every space mission, whether a CubeSat built by students or a constellation of thousands of broadband satellites, can be described as a set of cooperating **segments** (@fig:segments).

![The four segments of a space system and the links that join them. The space segment is usually the most visible, but the ground and user segments often cost as much over a mission's life.](figures/out/ch01_segments.svg){#fig:segments width=88%}

**Space segment.** The spacecraft themselves: satellites, probes, stations and their payloads. A spacecraft is normally divided into a **payload** (the part that performs the mission — a camera, a transponder, a telescope) and a **bus** or **platform** (the part that keeps the payload alive — power, thermal control, attitude control, propulsion, computing and communications). Part I explains the bus in detail; the application Parts explain the payloads.

**Ground segment.** Everything on the ground that controls the spacecraft and handles its data: mission control centres, ground stations with antennas, networks, flight dynamics software, payload data processing, archives and distribution systems. Large ground networks — NASA's Deep Space Network, ESA's ESTRACK, commercial "ground-station-as-a-service" networks such as KSAT, AWS Ground Station and Leaf Space — are shared by many missions.

**Launch segment.** The launch vehicle, the spaceport, the range that tracks the rocket and protects the public, and the facilities that integrate the payload into the fairing. For a single satellite the launch is a one-time event, but its cost and risk shape the entire mission design.

**User segment.** The people and equipment that use the service: a GPS receiver in a phone, a satellite TV dish, a farmer's crop-monitoring app, a forecaster using satellite data in a weather model, or a scientist analysing telescope images. For commercial systems the user segment is where revenue is earned; for navigation and broadband systems the user equipment is produced in hundreds of millions of units.

The **link segment** — radio-frequency (RF) and, increasingly, optical (laser) links — joins all of them. Links include telemetry, tracking and command (TT&C) for spacecraft control, high-rate payload data downlinks, user service links, and inter-satellite links that relay data through space. Chapter 7 explains how links are designed.

::: note
**Engineering note — think in segments early**

A frequent cause of mission failure or cost overrun is a space segment designed in isolation. Examples include satellites that produce more data than the ground stations can download, spacecraft whose radio frequencies were never coordinated with regulators, and payloads whose data products nobody was funded to process. Systems engineering (Chapter 4) exists largely to prevent these interface failures.
:::

## A Map of the Space Ecosystem

The word *ecosystem* is used deliberately: space activities depend on each other like species in an environment. Cheap launch enables mega-constellations; mega-constellations create demand for ground terminals, spectrum and collision avoidance; collision avoidance needs space situational awareness; and all of them depend on scientific understanding of space weather. @fig:ecosystem maps the major domains covered in this manual.

![The space ecosystem as eight interlocking domains, each covered by one or more Parts of this manual, supported by common enablers such as systems engineering, ground infrastructure, spectrum management, artificial intelligence and law.](figures/out/ch01_ecosystem_map.svg){#fig:ecosystem width=92%}

### Classification by Mission Purpose

Spacecraft are commonly grouped by what they do. The classification below follows the structure of this manual.

- **Near-space and suborbital platforms** — stratospheric balloons, high-altitude platform stations (HAPS), sounding rockets, suborbital crewed vehicles and spaceplanes (Part II).
- **Earth observation (EO) and remote sensing** — optical, infrared, radar, atmospheric and oceanographic satellites (Part IV).
- **Communications** — fixed and mobile satellite services, broadcasting, broadband, data relay, direct-to-device (Part V).
- **Positioning, navigation and timing (PNT)** — GPS, GLONASS, Galileo, BeiDou and regional systems (Part V).
- **National security** — intelligence, surveillance and reconnaissance (ISR), signals intelligence, missile warning, military communications (Part VI).
- **Space safety** — space situational awareness, debris tracking and removal (Part VI).
- **Space science** — heliophysics, magnetospheric physics, astronomy and astrophysics (Parts VII and XI).
- **Exploration** — robotic orbiters, probes, landers, rovers and sample-return missions; human spaceflight (Parts VIII and IX).
- **Technology and in-space economy** — servicing, assembly, manufacturing, resource extraction, propulsion demonstrations (Part XII).

### Classification by Size

Satellites range from a few grams to more than 400 tonnes (the International Space Station). The industry uses an informal mass scale (@tbl:massclass). The boundaries vary slightly between organisations, but the categories are widely understood.

Table: Informal spacecraft mass classes and examples. {#tbl:massclass}

| Class | Wet mass | Typical examples | Typical cost range (spacecraft only) |
|---|---|---|---|
| Femto/chip satellite | < 100 g | KickSat "Sprites", ChipSats | < US$1 000 each |
| Picosatellite | 0.1–1 kg | PocketQube, 1U CubeSat (≈1.3 kg is borderline) | US$10k–100k |
| Nanosatellite | 1–10 kg | 1U–6U CubeSats, Planet "Dove" (≈5 kg) | US$50k–2M |
| Microsatellite | 10–100 kg | 12U/16U CubeSats, ICEYE SAR (≈90 kg), Spire | US$1M–20M |
| Minisatellite / small satellite | 100–500 kg | OneWeb (≈150 kg), Starlink V1.5 (≈300 kg), NovaSAR-1 (≈450 kg) | US$5M–100M |
| Medium satellite | 500–2 500 kg | Starlink V2 Mini (≈800 kg), Iridium NEXT (≈860 kg), Sentinel-2 (≈1.1 t) | US$50M–500M |
| Large satellite | > 2 500 kg | Landsat 9 (≈2.7 t), GPS III (≈3.9 t), GEO communications satellites (3–7 t), JWST (6.2 t) | US$150M–10B |
| Space station | > 50 t | Tiangong (≈100 t), ISS (≈450 t) | US$10B–150B |

The CubeSat standard (Chapter 11) deserves special mention: by defining a standard 10 cm cube "unit" (1U) and a standard deployer, it made space accessible to universities and start-ups. More than 2 500 CubeSats have been launched since 2003.

## A Short History of Spaceflight

The modern space age began on 4 October 1957, when the Soviet Union launched **Sputnik 1**, an 84 kg sphere with four antennas that transmitted a simple beep. Within twelve years humans had orbited the Earth (Yuri Gagarin, 12 April 1961), walked in space (Alexei Leonov, 1965), and walked on the Moon (Neil Armstrong and Buzz Aldrin, 20 July 1969). @fig:timeline marks major milestones.

![Selected milestones of the space age, 1957–2026. The pace of "firsts" was highest in the 1960s; since 2015 a second wave has been driven by reusable rockets, small satellites and new national programmes.](figures/out/ch01_timeline.svg){#fig:timeline width=100%}

The history can be divided into five broad eras:

1. **The Space Race (1957–1975).** A competition between the USA and the USSR produced the first satellites, human flights, planetary probes, weather and communications satellites, reconnaissance satellites (CORONA, Zenit), and the Apollo lunar landings. Launch rates peaked at about 140 orbital attempts in 1967.
2. **Stations and shuttles (1971–2000).** The USSR operated Salyut stations and Mir; the USA flew Skylab and the reusable Space Shuttle. Satellite applications matured: Landsat (1972), GPS (first launch 1978, fully operational 1995), INTELSAT global communications, and the great observatories (Hubble 1990, Compton 1991, Chandra 1999).
3. **International cooperation and globalisation (1998–2010).** Assembly of the International Space Station began in 1998, permanently crewed since November 2000. China flew its first astronaut (Yang Liwei, 2003). Europe, Japan and India developed independent launch and exploration capabilities. Mars exploration intensified with orbiters and rovers.
4. **"New Space" (2010–2019).** Private capital entered the industry. SpaceX's Falcon 9 began flying in 2010, delivered cargo to the ISS in 2012 and landed an orbital-class booster in December 2015. CubeSats and small-satellite constellations (Planet, Spire) appeared. China landed on the far side of the Moon (Chang'e 4, 2019) and the first Starlink satellites launched in 2019.
5. **The industrial space age (2020–present).** Commercial crew transport (Crew Dragon, 2020), mega-constellations with thousands of satellites, routine booster reuse, China's Tiangong station (2021–2022), the James Webb Space Telescope (2021), the first far-side sample return (Chang'e 6, 2024), the first catch of a returning booster by its launch tower (Starship, October 2024), the first crewed flight around the Moon since 1972 (Artemis II, April 2026) and the launch of the Nancy Grace Roman Space Telescope (August 2026).

::: history
**History — the second space race is commercial and multipolar**

In 1967, two nations conducted nearly all space launches. In 2025, rockets from more than ten countries reached orbit, private companies launched most of the payloads, and the busiest single launch provider (SpaceX) flew more often than the whole world had in any year before 2021.
:::

## Space Activity in Numbers

### Launch Rate

@fig:launchyear shows every orbital launch attempt since 1957, grouped by the nationality of the launching organisation. After the Cold War peak, launch rates fell for two decades as satellites became longer-lived and the Soviet programme contracted. Since 2016 the rate has risen steeply, driven first by reusable Falcon 9 boosters and Chinese commercial and government launches.

![Orbital launch attempts per year, 1957–2025, by country of the launch provider. The 2025 total of 330 attempts (counts vary slightly between sources, from 323 to 330, depending on how test flights are treated) is the highest in history. "United States" includes Rocket Lab launches from New Zealand.](figures/out/ch01_launches_year.svg){#fig:launchyear width=100%}

Table: Orbital launch attempts by country of launch provider, 2025 and 2026 to mid-October (GCAT). {#tbl:launch2025}

| Country / region | 2025 attempts | Share 2025 | 2026 (to 13 Oct) | Main vehicles |
|---|---|---|---|---|
| United States | 198 | 60 % | 146 | Falcon 9, Falcon Heavy, Electron, Starship, Atlas V, Vulcan, New Glenn |
| China | 93 | 28 % | 71 | Long March family, Zhuque, Kinetica-1, Ceres-1, Kuaizhou, Jielong, Gravity-1 |
| Russia | 17 | 5 % | 13 | Soyuz-2, Angara, Proton |
| Europe | 8 | 2 % | 7 | Ariane 6, Vega-C |
| India | 5 | 2 % | 3 | PSLV, GSLV, LVM3 |
| Japan | 4 | 1 % | 3 | H3, H-IIA (retired 2025) |
| Others (Iran, North Korea, South Korea, …) | 5 | 2 % | 1 | Simorgh, Qaem-100, Nuri |
| **World** | **330** | 100 % | **244** | |

![Orbital launch attempts in 2025 by launch-vehicle family. A single vehicle family, Falcon 9, accounted for half of all orbital launches worldwide.](figures/out/ch01_families_2025.svg){#fig:families width=86%}

### Satellites in Orbit

The number of satellites has grown even faster than the number of launches, because one launch can now deploy dozens or hundreds of satellites. In 2025 alone about **4 500 payloads** were placed in orbit — more than in the first fifty years of spaceflight combined (@fig:payloads). Most of the growth comes from broadband constellations, especially SpaceX's Starlink, which had more than 10 600 satellites in orbit by October 2026, followed by Eutelsat OneWeb (≈650), China's Guowang and Qianfan constellations, and Amazon Leo (formerly Project Kuiper, about 400 satellites by mid-2026).

![Payloads launched per year, 1990–2025, separating Starlink from all other payloads. The step change after 2019 is the arrival of mega-constellations.](figures/out/ch01_payloads_year.svg){#fig:payloads width=96%}

![Left: the ~33 800 catalogued objects in Earth orbit by type. Right: payloads in orbit by orbital regime. Low Earth orbit dominates in numbers; GEO dominates in value per satellite.](figures/out/ch01_in_orbit.svg){#fig:inorbit width=100%}

::: data
**Data box — Earth orbit population, October 2026 (GCAT)**

- Catalogued objects in orbit: **≈33 800**, of which payloads ≈19 200, debris fragments ≈11 300, rocket bodies ≈2 000, other mission objects ≈1 300.
- Payloads believed to be operating: **≈16 000–17 000** (GCAT estimate ≈16 000; CelesTrak lists ≈17 200 as operational; definitions of "active" differ).
- Starlink satellites in orbit: **≈10 650**.
- Payloads by regime: LEO ≈17 100, GEO ≈1 340, MEO ≈460, highly elliptical ≈240.
- Estimated objects too small to track (1–10 cm): **about one million**; objects 1 mm–1 cm: over 100 million (ESA debris model).
:::

### The Space Economy

The **space economy** is the total of all revenues and budgets generated by space activities. Estimates differ in what they include (for example, whether satellite TV subscriptions or GNSS-enabled phones count), but the Space Foundation's series is widely quoted: the global space economy reached about **US$686 billion in 2025**, up 12 % from US$613 billion in 2024 (@fig:economy). About 79 % was commercial; government space budgets totalled about US$141 billion, of which the United States accounted for 57 %.

![Left: growth of the global space economy, 2019–2025. Right: split between commercial activity and government budgets in 2025.](figures/out/ch01_economy.svg){#fig:economy width=100%}

Three observations help interpret these numbers:

1. **Most money is made on the ground.** Satellite communications services, user terminals, GNSS chipsets and downstream data products earn far more than rockets or satellites themselves. The "upstream" manufacturing and launch sector is only roughly a tenth of the total.
2. **Governments remain the anchor customers.** Even in commercial markets, government contracts (for example NASA's Commercial Crew and Cargo programmes, the US Space Development Agency's constellation, or ESA's Galileo) fund the first systems and reduce investor risk.
3. **Defence spending is rising fastest.** Since 2022, military and intelligence space budgets have grown more quickly than civil budgets in the United States, Europe, Japan and elsewhere, reflecting the role of satellites in modern conflicts.

![Estimated government space spending by country in 2024 (civil and defence combined). The United States spends roughly four times more than China and more than all other governments together.](figures/out/ch01_gov_budgets.svg){#fig:govbudgets width=92%}

Table: Major space agencies and organisations (selected). {#tbl:agencies}

| Organisation | Country / members | Founded | Notable capabilities (2026) |
|---|---|---|---|
| NASA | USA | 1958 | Artemis (SLS/Orion), ISS, deep-space science, JWST, Roman, Deep Space Network |
| US Space Force / NRO / SDA | USA | 2019 / 1961 / 2019 | GPS, missile warning, military comms, reconnaissance, proliferated LEO architecture |
| NOAA (NESDIS) | USA | 1970 | GOES, JPSS weather satellites, space weather (SWFO-L1), commercial remote-sensing licensing |
| Roscosmos | Russia | 1992 (successor to Soviet programme) | Soyuz crew and cargo, GLONASS, Angara, ISS Russian segment |
| CNSA / CMSA | China | 1993 / 1992 | Tiangong station, Chang'e lunar, Tianwen planetary, BeiDou, Long March |
| ESA | 23 member states | 1975 | Ariane 6, Vega-C, Copernicus (with EU), Galileo (with EU), science missions |
| EUSPA / European Commission | EU-27 | 2021 | Galileo, EGNOS, Copernicus programme management, IRIS² secure connectivity |
| JAXA | Japan | 2003 (merger) | H3, Hayabusa missions, SLIM lunar lander, MMX, HTV-X cargo |
| ISRO | India | 1969 | PSLV, LVM3, Chandrayaan-3, Aditya-L1, NavIC, Gaganyaan |
| CNES / DLR / ASI / UKSA | France / Germany / Italy / UK | 1961 / 1969 (as DFVLR) / 1988 / 2010 | National programmes and major ESA contributors |
| CSA | Canada | 1989 | Canadarm robotics, RADARSAT, Artemis II astronaut |
| KASA | South Korea | 2024 | Nuri launcher, Danuri lunar orbiter |
| UAE Space Agency / MBRSC | United Arab Emirates | 2014 / 2006 | Hope Mars orbiter, astronaut programme, Gateway airlock (planned) |

## Why Space Is Hard

Space engineering combines three difficulties that are rarely found together in other industries.

**1. The energy problem.** To reach low Earth orbit a vehicle must gain about 9.3–9.6 km/s of velocity once gravity and drag losses are included. The rocket equation (Chapter 34) shows that this requires a vehicle that is typically 85–95 % propellant at lift-off; only 2–4 % of the lift-off mass reaches orbit as payload. Every kilogram of spacecraft therefore costs many kilograms of rocket.

**2. The environment problem.** In orbit, a spacecraft must survive vacuum, temperature swings of more than 200 °C, radiation that damages electronics and solar cells, atomic oxygen, micrometeoroids and debris travelling at 10 km/s, and launch vibrations and shocks of tens of g (Chapter 2).

**3. The no-repair problem.** With very few exceptions (Hubble servicing, the ISS, the new generation of servicing vehicles), a spacecraft cannot be repaired after launch. It must work first time and keep working for 5–15 years. This drives redundancy, extensive testing, conservative design margins and long development schedules.

These difficulties explain why spacecraft traditionally cost tens of thousands of dollars per kilogram. Two trends are now lowering the cost: reusable launch vehicles, and mass-produced small satellites that accept higher individual failure rates because the constellation as a whole is resilient. @fig:costkg shows how much the price of reaching orbit has fallen.

![Approximate cost per kilogram to low Earth orbit for representative launch vehicles, in inflation-adjusted dollars. Reusable boosters reduced commercial launch prices by about an order of magnitude; fully reusable vehicles aim for another order of magnitude.](figures/out/ch01_cost_per_kg.svg){#fig:costkg width=94%}

::: example
**Worked example — how much does it cost to put a 6U CubeSat in orbit?**

A 6U CubeSat has a mass of about 10 kg. On a rideshare mission (for example SpaceX's Transporter series), the list price in 2025 was about US$6 500 per kilogram with a minimum of about US$325 000 for 50 kg to sun-synchronous orbit, so a single 6U satellite would typically be launched through an integrator for roughly US$150 000–300 000 including the deployer. A dedicated small launcher (e.g., Rocket Lab Electron, about US$8.5 million per launch) is far more expensive per kilogram but lets the customer choose the orbit and the launch date. The choice between *rideshare* and *dedicated* launch is one of the first trade-offs in a small-satellite mission (Chapter 11).
:::

## Governance: The Rules of Space

Space activities are regulated by a combination of international treaties, UN guidelines, international technical bodies and national laws.

Table: The core instruments of international space law. {#tbl:spacelaw}

| Instrument | Year | Key provisions |
|---|---|---|
| Outer Space Treaty | 1967 | Space free for exploration by all states; no national appropriation of celestial bodies; no weapons of mass destruction in orbit; states responsible for national activities, including private ones ("authorisation and continuing supervision"); liability for damage |
| Rescue Agreement | 1968 | Assistance to astronauts in distress; return of space objects |
| Liability Convention | 1972 | Absolute liability for damage on Earth's surface or to aircraft; fault-based liability in space |
| Registration Convention | 1975 | States register launched objects with the UN (UNOOSA register) |
| Moon Agreement | 1979 | Moon resources as "common heritage of mankind" — ratified by few states, not by major space powers |
| ITU Constitution and Radio Regulations | updated at each World Radiocommunication Conference (latest WRC-23; next WRC-27) | Allocation of radio frequencies; coordination and registration of satellite networks and orbital positions |
| UN COPUOS Space Debris Mitigation Guidelines | 2007 | Limit debris release, avoid break-ups, post-mission disposal |
| UN Long-Term Sustainability Guidelines | 2019 | 21 voluntary guidelines on safety, SSA, debris, regulation |
| Artemis Accords | 2020 | Non-binding principles for civil lunar exploration: transparency, interoperability, emergency assistance, registration, release of scientific data, preserving heritage sites, deconfliction "safety zones", space-resource use consistent with the OST. 76 signatories by late September 2026 |

National regulators turn these principles into licences. In the United States, for example, the FAA licenses launches and re-entries, the Federal Communications Commission (FCC) licenses spectrum and imposes debris rules (including a five-year post-mission disposal rule for LEO satellites adopted in 2022), and NOAA licenses commercial remote-sensing systems. Other countries, including the UK (Space Industry Act 2018), France (French Space Operations Act 2008), Japan (Space Activities Act 2016), New Zealand, Luxembourg and the UAE, have comparable laws. China's International Lunar Research Station (ILRS) programme forms a second international lunar partnership alongside the Artemis Accords.

::: warning
**Lesson — debris is a shared risk**

In 2007 China destroyed its Fengyun-1C weather satellite with a ground-launched missile, creating more than 3 500 trackable fragments, many still in orbit. In 2009 the active Iridium 33 and the defunct Kosmos 2251 collided at 11.7 km/s, creating about 2 300 more. In November 2021 a Russian anti-satellite test destroyed Kosmos 1408 and forced the ISS crew to shelter. Because debris does not respect national boundaries, debris mitigation and space traffic coordination (Chapter 21) have become central policy issues.
:::

## The Engineering Disciplines of the Space Ecosystem

A space programme employs almost every branch of engineering and science. @tbl:disciplines lists the main disciplines and where they appear in this manual.

Table: Engineering and science disciplines in the space ecosystem. {#tbl:disciplines}

| Discipline | What it does in space programmes | Main chapters |
|---|---|---|
| Systems engineering | Requirements, architecture, interfaces, budgets, verification, risk | 4, 11, 24 |
| Astrodynamics / flight dynamics | Orbit design, manoeuvres, navigation, orbit determination | 3, 11, 21, 24 |
| Structural and mechanical engineering | Primary structure, mechanisms, deployables, launch loads | 5, 34 |
| Thermal engineering | Radiators, heaters, insulation, heat pipes, cryogenics | 5, 38 |
| Electrical power engineering | Solar arrays, batteries, power conditioning, RTGs | 5, 24 |
| Guidance, navigation and control (GNC) | Attitude determination and control, autonomous navigation, landing | 6, 27, 45 |
| Propulsion engineering | Rocket engines, electric thrusters, propellant systems | 6, 35, 42 |
| Avionics and embedded software | Flight computers, data handling, fault protection, flight software | 6, 45 |
| RF and optical communications | Antennas, transponders, link budgets, lasercom | 7, 17 |
| Payload and instrument engineering | Optics, detectors, radars, spectrometers, particle instruments | 12–16, 38–39 |
| Aerothermodynamics | Re-entry heating, heat shields, atmospheric entry | 10, 27 |
| Human factors and life sciences | Life support, radiation protection, ergonomics, medicine | 30–33 |
| Ground systems and operations | Mission control, scheduling, data processing | 7, 45 |
| Data science and artificial intelligence | Onboard processing, analytics, autonomy, forecasting | 43–47 |
| Product assurance and safety | Reliability, quality, parts, materials, safety analysis | 4 |
| Law, policy and economics | Licensing, spectrum, insurance, finance, export control | 1, 21, 41 |

## How This Manual Is Organised

The remaining chapters follow a logical sequence. Part I builds the foundations: the environment (Chapter 2), orbits (Chapter 3), systems engineering (Chapter 4), spacecraft subsystems (Chapters 5 and 6) and communications (Chapter 7). Each later Part applies these foundations to a family of systems. Part XIII then shows how artificial intelligence — from onboard image classification to AI weather models and autonomous rovers — is changing every one of these domains, and Part XIV collects the reference data an engineer needs at hand.

::: key
**Key takeaways**

- Space has no physical boundary; 100 km (Kármán line) and 80 km are conventional limits. Orbit requires horizontal speed (≈7.8 km/s), not just height.
- Every mission consists of space, ground, launch and user segments joined by links; interfaces between segments are where many problems occur.
- In 2025 the world made a record 330 orbital launch attempts and placed about 4 500 payloads in orbit; about 16 000 satellites were operating in late 2026, two-thirds of them Starlink.
- The space economy was about US$686 billion in 2025, roughly four-fifths commercial; government budgets (≈US$141 billion) remain the anchor of the industry.
- Space is hard because of the energy needed to reach orbit, the hostile environment, and the near-impossibility of repair; reusability and mass production are changing the economics.
- International treaties set principles, while national licences, ITU spectrum rules and debris guidelines govern day-to-day activities.
:::
