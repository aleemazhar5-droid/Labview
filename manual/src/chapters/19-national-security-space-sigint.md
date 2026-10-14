---
title: National Security Space and Signals Intelligence
hero: ch19
abstract: Space was a military and intelligence domain from the very beginning: the first reconnaissance satellites returned film from orbit in 1960, and today armed forces depend on space for intelligence, warning, navigation, communications and weather. This chapter describes, from public sources, the mission areas of national-security space and the organisations that conduct them; the principles of imagery and signals intelligence (SIGINT, ELINT and COMINT) from orbit, including the physics of intercepting and geolocating radio emitters; protected military satellite communications; the shift from a few exquisite satellites to proliferated constellations; the growing role of commercial space in conflict; and the counterspace threats — from anti-satellite missiles to jamming and cyber attacks — that have made space a contested domain, together with the legal and diplomatic efforts to limit them.
---

## Space as a National Security Domain

### Mission Areas

Military and intelligence organisations use space for the same reasons as civilians — global coverage, a vantage point above any territory, and the ability to relay signals over the horizon — but with demands for resilience, security and timeliness that civil systems rarely face. National-security space is usually divided into the mission areas shown in @fig:nssfunctions:

- **Intelligence, surveillance and reconnaissance (ISR)**: imagery (IMINT), signals intelligence (SIGINT), and measurement and signature intelligence (MASINT).
- **Missile warning and tracking**: infrared satellites that detect missile launches and nuclear detonations (Chapter 20).
- **Positioning, navigation and timing**: GPS and its military signals (Chapter 18).
- **Satellite communications (SATCOM)**: protected, wideband and narrowband links to forces worldwide.
- **Environmental monitoring**: military weather satellites.
- **Space domain awareness**: tracking and characterising objects and activities in space (Chapter 21).
- **Space control**: protecting one's own space systems and, if necessary, denying an adversary's use of space.
- **Launch and ranges**: assured access to space.

![Mission areas of national-security space.](figures/out/ch19_functions.svg){#fig:nssfunctions width=90%}

### History

The first US reconnaissance satellites flew within three years of Sputnik (@fig:nsshistory). The Naval Research Laboratory's **GRAB** satellite, launched in June 1960 under cover of a scientific mission, intercepted Soviet air-defence radar signals — the world's first SIGINT satellite. Two months later, the **Corona** programme achieved the first recovery of exposed film from orbit, dropped in a capsule and caught in mid-air by an aircraft. A single early Corona mission photographed more of the Soviet Union than all previous U-2 flights combined, settling the debate about the "missile gap". Corona flew from 1960 to 1972, its resolution improving from about 12 m to under 2 m; its more than 800 000 images were declassified in 1995 and remain a valuable record of mid-20th-century landscapes. The Soviet Union's **Zenit** satellites, derived from the Vostok crewed spacecraft, followed from 1962.

Film-return systems gave way to electro-optical imaging satellites, which transmit images digitally, in the mid-1970s. The **Vela** satellites (from 1963) watched for nuclear tests in space and the atmosphere, and the **Defense Support Program** (from 1970) for ballistic-missile launches. The 1991 Gulf War, in which GPS, satellite communications, missile warning and reconnaissance supported coalition forces on an unprecedented scale, is often called the first "space war". The very existence of the US **National Reconnaissance Office (NRO)**, founded in 1961, was declassified only in 1992.

![Milestones in national-security space.](figures/out/ch19_history.svg){#fig:nsshistory width=100%}

### Organisations

Many countries have reorganised their armed forces to treat space as a domain of operations alongside land, sea, air and cyberspace (@tbl:nssorgs). NATO recognised space as an operational domain in 2019.

| Country | Military space organisation | Intelligence / other agencies | Notes |
|---|---|---|---|
| USA | US Space Force (2019); US Space Command (re-established 2019); Space Development Agency (2019) | National Reconnaissance Office; National Geospatial-Intelligence Agency | Largest military space budget; extensive use of commercial services |
| China | PLA Aerospace Force (2024, formed from the Strategic Support Force) | — | Yaogan, Gaofen, Shijian and TJS series; rapid growth |
| Russia | Aerospace Forces (VKS), Space Forces | GRU and others | Persona, Bars-M, Lotos-S/Liana, Tundra |
| France | Space Command (CDE, 2019) | DGSE, DRM | CSO imaging satellites; CERES SIGINT trio |
| United Kingdom | UK Space Command (2021) | — | Skynet SATCOM; partnerships and commercial data |
| Germany, Italy, Spain | National space commands | — | SARah, COSMO-SkyMed, PAZ radar satellites |
| Japan | Air and Space Self-Defense Force (renamed) | Cabinet Satellite Intelligence Center | Information Gathering Satellites (IGS) |
| India | Defence Space Agency (2019) | — | RISAT, EMISAT (ELINT), dedicated GSAT |
| Israel | Israeli Air Force / Ministry of Defence | — | Ofek imaging satellites |

: Selected military space organisations (public information). {#tbl:nssorgs}

## Imagery Intelligence from Space

Military imaging satellites use the same physics as civil Earth observation (Chapters 13–15): high-resolution optical and infrared telescopes, and synthetic aperture radars for all-weather, day-and-night coverage. The most capable systems are believed to use mirrors of about 2.4 m — the same size as the Hubble Space Telescope — giving resolutions of roughly 10–15 cm from low orbit (Chapter 14, @fig:optics). Governments seldom publish the specifications of such systems. What distinguishes military imaging is less the sensor than the **system**: priority tasking, rapid processing, secure dissemination and the fusion of many sources into intelligence products.

### Revisit and Constellation Design

For many military purposes the critical parameter is not resolution but **revisit** — how often a target can be observed. A single agile imaging satellite in a sun-synchronous orbit can view a mid-latitude target only about once every two to three days in daylight; doubling the number of satellites roughly halves the wait (@fig:isrrevisit). Radar satellites, which can image at night as well, have about twice as many opportunities. To watch a target several times per day, a constellation of a dozen or more satellites — or satellites in mid-inclination orbits, which pass over mid-latitudes more often and at varying local times — is needed. This is why both governments and commercial operators have moved towards larger constellations of smaller satellites.

![Simulated mean time between looks at a target at 35° N as a function of the number of agile imaging satellites.](figures/out/ch19_revisit.svg){#fig:isrrevisit width=84%}

| Country | System (public name) | Type | Notes |
|---|---|---|---|
| USA | NRO electro-optical and radar satellites | Optical, SAR | Specifications classified; large-aperture optical systems since 1976 |
| USA | NRO proliferated architecture | Optical and other sensors | Launched from 2024 with SpaceX and Northrop Grumman |
| France | CSO (Composante Spatiale Optique) | Optical | Three satellites (2018, 2020, 2025); shared with partners |
| Germany | SAR-Lupe, SARah | SAR | SARah constellation launched 2022–2023 |
| Italy | COSMO-SkyMed (1st and 2nd generation) | SAR | Dual-use military and civil |
| Japan | Information Gathering Satellites (IGS) | Optical, SAR | Programme started after the 1998 North Korean missile overflight |
| Israel | Ofek, TecSAR | Optical, SAR | Launched westward from Israel on Shavit rockets |
| China | Yaogan, Gaofen series | Optical, SAR, ELINT | About 170 Yaogan satellites in orbit; some in triplets |
| Russia | Persona, Bars-M, Kondor | Optical, SAR | Smaller fleet than the USA or China |
| India | Cartosat, RISAT, EMISAT | Optical, SAR, ELINT | Dual-use national programmes |

: Selected government imaging and reconnaissance systems (public information). {#tbl:imint}


### The Intelligence Cycle

Intelligence agencies describe their work as a cycle: **planning and direction** (what do decision-makers need to know?), **collection** (tasking satellites and other sensors), **processing and exploitation** (turning raw data into information — locating, identifying and measuring objects), **analysis and production** (combining sources into assessments) and **dissemination**. Satellites contribute mainly to collection, but the bottlenecks have increasingly moved to processing and analysis: modern constellations generate far more images than human analysts can examine, which is why AI-based object detection and change detection have become essential (Part XIII).

### Commercial Imagery in National Security

Commercial imagery now complements government systems on a large scale. The USA buys imagery under the NRO's Electro-Optical Commercial Layer contracts and from commercial SAR providers, and many smaller nations rely entirely on commercial or allied data. During the war in Ukraine, commercial optical and radar imagery from companies such as Vantor (formerly Maxar), Planet, Airbus, ICEYE, Capella and BlackSky has been widely used by governments and published by the media, transforming public understanding of military events. Commercial data are unclassified and shareable with allies and the public, which has given them diplomatic as well as operational value.

## Signals Intelligence from Space

### Disciplines

**Signals intelligence (SIGINT)** is the collection and analysis of electromagnetic signals emitted by an adversary's systems (@tbl:sigint). It is traditionally divided into:

| Discipline | Target | Typical frequencies | Information obtained |
|---|---|---|---|
| ELINT (electronic intelligence) | Radars and other non-communication emitters | ≈ 0.1–40 GHz | Location, type and operating mode of radars; air-defence order of battle |
| COMINT (communications intelligence) | Voice, data and messaging | HF to Ka-band | Content (if decrypted), traffic patterns, location of communicators |
| FISINT (foreign instrumentation signals intelligence) | Telemetry from missiles, aircraft and spacecraft | VHF to S-band | Performance of weapons under test |
| Commercial RF geolocation | Ships with AIS switched off, satellite phones, push-to-talk radios, GNSS jammers | VHF to Ku-band | Location and track of emitters for maritime and security customers |

: Signals intelligence disciplines. {#tbl:sigint}

### Intercept Physics

A SIGINT satellite is a sensitive radio receiver with a large antenna. Intercepting radar signals is relatively easy because radars are powerful — often hundreds of kilowatts to megawatts of peak power — and even their side lobes are strong. Intercepting low-power communications from space is harder. The link budget (Chapter 7) shows that a 5 W VHF handheld radio received at 600 km arrives at about −95 dBm — easily detectable — but at geostationary distance it arrives about 36 dB weaker, requiring a significant receiving antenna.

The bigger challenge is to **separate and locate** emitters. A receiving antenna's beamwidth is about $70\lambda/D$ degrees, so at low frequencies even large antennas have broad beams (@fig:sigintfootprint). From geostationary orbit, a 10 m antenna at 1 GHz has a beam about 1 300 km wide, and at VHF a beam narrow enough to isolate a single city would need an antenna several hundred metres across. Public reports describe very large deployable reflectors on some geostationary SIGINT satellites, and complementary geolocation techniques are used.

![Ground footprint of a receiving antenna beam as a function of antenna diameter, for four frequencies, from geostationary and low orbit. Isolating emitters by beam alone requires very large antennas, especially at low frequencies.](figures/out/ch19_footprint.svg){#fig:sigintfootprint width=86%}

### Geolocation Techniques

Emitters are located by measuring how their signals arrive at one or more receivers:

- **Angle of arrival (AOA)**: an interferometer measures the phase difference of a signal between two or more antennas separated by a baseline $d$; the phase difference $2\pi d\sin\theta/\lambda$ gives the arrival direction $\theta$ (@fig:aoa). Long baselines give precise but ambiguous angles; combinations of baselines resolve the ambiguity.
- **Time difference of arrival (TDOA)**: two satellites receive the same signal at slightly different times; each measured time difference places the emitter on a hyperbolic curve on the Earth's surface (@fig:tdoa). Three satellites give two independent TDOAs whose curves intersect at the emitter.
- **Frequency difference of arrival (FDOA)**: because the satellites move, they receive slightly different Doppler shifts; the frequency difference defines another family of curves that cross the TDOA curves, so a pair of satellites measuring both can fix an emitter.
- **Single-satellite Doppler**: like the old Transit system in reverse, one satellite can locate a continuously transmitting emitter from the Doppler curve observed during a pass.

![Emitter geolocation from a pair of satellites. Lines of constant time difference of arrival (left) are hyperbolas on the ground; lines of constant frequency difference (right) cross them, so the two measurements together fix the emitter.](figures/out/ch19_tdoa.svg){#fig:tdoa width=98%}

![Angle-of-arrival measurement with a two-element interferometer.](figures/out/ch19_aoa.svg){#fig:aoa width=88%}

These principles explain the distinctive configurations of SIGINT satellites reported in public sources. Ocean-surveillance systems such as the historic US "White Cloud"/NOSS series and China's Yaogan triplets fly **clusters** of two or three satellites tens of kilometres apart to measure TDOA from ship radars and communications. France's **CERES** system (three satellites launched in 2021) and its ELISA demonstrators locate radars for the French armed forces. Russia's Lotos-S/Liana system and India's EMISAT perform similar roles.

### Commercial RF Geolocation

Since 2018, commercial companies have brought these techniques to an open market. **HawkEye 360** (USA) flies clusters of three microsatellites that detect and geolocate signals from marine VHF radios, AIS transponders, satellite phones, radars and GNSS jammers; by 2026 it had about 40 satellites in orbit. France's **Unseenlabs** locates ships from their radio emissions using single satellites, and Luxembourg's **Kleos Space** and others offer similar services. Their customers include coast guards fighting illegal fishing and smuggling — finding "dark" vessels that switch off their AIS transponders — and defence agencies.

### MASINT

**Measurement and signature intelligence (MASINT)** uses the physical signatures of objects and events: infrared signatures of missile plumes and industrial activity, spectral signatures of materials (hyperspectral imaging), radar signatures, and the light flash, X-rays and electromagnetic pulse of nuclear detonations. Nuclear-detonation detection sensors have flown on GPS satellites since the 1980s as part of the US Nuclear Detonation Detection System, continuing the role of the Vela satellites in verifying the Limited Test Ban Treaty.

## Military Satellite Communications

Military forces need communications that are global, secure and resistant to jamming and interception. Military SATCOM is usually divided into three tiers (@tbl:milsatcom):

| Tier | Purpose | Bands | Example systems |
|---|---|---|---|
| Protected / strategic | Survivable, jam-resistant, low-probability-of-intercept links for nuclear command and control and critical operations | EHF (44 GHz uplink / 20 GHz downlink) | US AEHF (six satellites, 2010–2020) and planned ESS; Milstar (legacy) |
| Wideband | High-capacity links for headquarters, ships, aircraft and drones | X, Ka | US WGS; UK Skynet 5/6; France Syracuse 4; Italy Sicral 2; Spain SpainSat NG |
| Narrowband / tactical | Voice and data to small mobile terminals | UHF | US MUOS (five satellites, 2012–2016); UHF Follow-On |
| Commercial and hybrid | Additional capacity, resilience and Arctic coverage | Ku, Ka, L | Commercial GEO and LEO services, Starshield, Space Norway ASBM |

: Military satellite communication tiers. {#tbl:milsatcom}

**Jam resistance** is achieved mainly by spreading signals over very wide bandwidths — by direct-sequence spreading or rapid **frequency hopping** — so that a jammer must spread its power across the whole band. The protection, called **processing gain**, is $10\log(W/R)$, where $W$ is the spread bandwidth and $R$ the data rate (@fig:antijam). EHF systems hop over about 2 GHz, giving more than 60 dB of protection to low-rate strategic messages. Other techniques include **nulling antennas** that steer deep nulls towards jammers, on-board processing that demodulates signals and rejects interference, and narrow spot beams. **Low probability of intercept and detection (LPI/LPD)** waveforms hide transmissions below the noise.

![Processing gain of spread-spectrum military links versus user data rate. High data rates leave little margin against jamming.](figures/out/ch19_antijam.svg){#fig:antijam width=86%}

The war in Ukraine demonstrated the value — and vulnerability — of commercial communications in conflict. Thousands of Starlink terminals provided resilient connectivity to Ukrainian forces and civil infrastructure, while a cyber attack on the ground network of Viasat's KA-SAT system on 24 February 2022, the first day of the invasion, disabled tens of thousands of terminals across Europe.

## Military Weather, Launch and the Wider Enterprise

### Military Weather

Weather affects every military operation — cloud cover over a target, winds for parachute drops, sea state for landings, and space weather for communications and GPS. The US Defense Meteorological Satellite Program (DMSP), operating since the 1960s, pioneered night-time visible imaging and microwave sounding; its last satellites are reaching the end of their lives. Its replacements include the **Weather System Follow-on – Microwave (WSF-M)**, the first of which was launched in April 2024 to measure ocean-surface winds and tropical-cyclone structure, and small electro-optical/infrared weather satellites for cloud imagery over regions where geostationary coverage is poor. Military users also rely heavily on civil systems such as Metop and JPSS (Chapter 16).

### National Security Launch

Assured access to space is a national-security requirement in itself. The USA certifies launch providers for national-security payloads under the **National Security Space Launch (NSSL)** programme; in the 2020s, launches were shared between SpaceX (Falcon 9 and Falcon Heavy), United Launch Alliance (Vulcan Centaur, which replaced Atlas V and Delta IV) and, from Phase 3 (2025 onward), Blue Origin's New Glenn, with a separate "lane" for new entrants on lower-risk missions. **Tactically responsive space** demonstrations, such as Victus Nox in 2023 — in which a satellite was launched 27 hours after the order was given — aim to show that satellites can be replaced quickly in a crisis. China, Russia, India and Europe maintain their own launchers for sovereign access (Chapter 36).

### Who Operates Military Satellites?

@fig:milregimes summarises the publicly catalogued military satellites of the main space powers by orbit. The USA operates the largest number — boosted by proliferated LEO constellations — followed by China, whose Yaogan series alone counts about 170 satellites, and Russia. Many military satellites operate in LEO for imaging and SIGINT; communications, missile-warning and some SIGINT satellites are in GEO and highly elliptical orbits; and navigation satellites are in MEO.

![Active military satellites of selected series by orbit regime in October 2026 (public catalogue).](figures/out/ch19_regimes.svg){#fig:milregimes width=90%}

### Allies and Commercial Partners

No country can afford all space capabilities alone. The **Combined Space Operations (CSpO)** initiative brings together the space commands of Australia, Canada, France, Germany, Italy, Japan, New Zealand, Norway, the UK and the USA to coordinate operations and share data. NATO adopted its first space policy in 2019 and established a Space Centre at its air command in Germany. Commercial companies increasingly act as partners: providing imagery, RF geolocation, communications, launch and space-tracking data, and in some cases building dedicated government constellations. This raises new questions — such as whether commercial satellites supporting military operations become legitimate targets, and how governments protect companies that operate in conflict zones.


## From Exquisite to Proliferated Architectures

For most of the space age, national-security satellites were few, large, expensive and long-lived — "exquisite" systems that took a decade to develop and cost billions of dollars each. Such systems are extremely capable but also tempting targets: losing one can remove a capability for years. Since about 2019, the USA and other countries have shifted towards **resilience** through:

- **Proliferation**: many cheaper satellites, so that losing a few does not matter;
- **Disaggregation**: separating functions (for example strategic and tactical missile warning) onto different satellites;
- **Diversification**: using several orbits, frequencies and providers, including commercial ones;
- **Rapid replenishment**: replacing satellites every few years in "tranches" that incorporate new technology.

The US **Space Development Agency (SDA)**, founded in 2019, is building the **Proliferated Warfighter Space Architecture (PWSA)** in low Earth orbit at about 1 000 km (@fig:pwsa). Its **Transport Layer** forms a mesh network of optical inter-satellite links and radio links (including the Link 16 tactical data link) to deliver targeting data directly to forces, and its **Tracking Layer** carries infrared sensors to detect and track missiles, including hypersonic glide vehicles (Chapter 20). After about two dozen Tranche 0 demonstration satellites launched in 2023, the first operational Tranche 1 satellites launched in September 2025; Tranche 1 comprises 154 satellites (126 transport and 28 tracking), with further tranches planned every two years. Separately, the NRO has been deploying a proliferated constellation of imaging satellites, built with SpaceX and Northrop Grumman, since 2024.

![The Proliferated Warfighter Space Architecture: a transport layer of laser-linked satellites delivers data from a tracking layer of infrared sensors to forces and missile-defence systems.](figures/out/ch19_pwsa.svg){#fig:pwsa width=94%}

In 2025 the US government launched **Golden Dome**, an ambitious homeland missile-defence initiative that includes space-based sensors and, controversially, **space-based interceptors**. In April 2026 the Space Force awarded prototype agreements worth up to $3.2 billion to twelve companies to demonstrate space-based interceptors by 2028; independent analysts have questioned the technical feasibility and cost of the overall programme, which official estimates put at about $175–185 billion.

Other powers are following similar paths: China has launched large numbers of Yaogan and other military satellites and is building proliferated LEO constellations, and Europe's IRIS² constellation will include secure governmental communications.

### Spaceplanes and Experimental Platforms

The US Space Force's **X-37B** Orbital Test Vehicle, a small reusable uncrewed spaceplane built by Boeing (Chapter 10), has flown eight missions since 2010, some lasting more than two years. Its seventh mission (2023–2025) demonstrated aerobraking from a highly elliptical orbit, and its eighth was launched in August 2025. China has flown a comparable reusable experimental spacecraft several times since 2020. Such platforms test new technologies and allow sensors to be returned to Earth for inspection.

## Counterspace: A Contested Domain

### Categories of Threat

As military dependence on space grew, so did interest in denying an adversary's use of it. Public assessments by organisations such as the Secure World Foundation and the Center for Strategic and International Studies group counterspace capabilities into four categories (@fig:counterspace):

- **Kinetic physical**: direct-ascent anti-satellite (DA-ASAT) missiles that destroy a satellite by collision; co-orbital weapons that approach and attack a target; attacks on ground stations.
- **Non-kinetic physical**: lasers that dazzle or damage optical sensors, high-power microwaves and — most dangerously — nuclear detonations in space, whose radiation would damage large numbers of satellites indiscriminately.
- **Electronic**: jamming of uplinks and downlinks and spoofing of GNSS and other signals — the most widely used and most easily reversible form of counterspace.
- **Cyber**: attacks on the data, ground systems or satellites themselves.

![Categories of counterspace capability.](figures/out/ch19_counterspace.svg){#fig:counterspace width=96%}

### Anti-Satellite Tests and Debris

Five destructive anti-satellite tests have created long-lived debris (@fig:asat; @tbl:asattests). The worst, China's January 2007 destruction of its Fengyun-1C weather satellite at about 865 km, produced more than 3 500 catalogued fragments — the largest debris-generating event in history — and more than 2 300 were still in orbit in October 2026, threatening satellites in sun-synchronous orbits for decades. Russia's November 2021 test against the defunct Cosmos 1408 at about 480 km produced about 1 800 catalogued fragments and forced the ISS crew to shelter in their spacecraft; most have since re-entered. Tests at lower altitudes, such as the US destruction of the failing USA-193 satellite in 2008 at about 247 km and India's "Mission Shakti" in 2019 at about 283 km, created debris that decayed within months to a few years.

| Year | Country | Target | Intercept altitude | Catalogued debris | Still in orbit (Oct 2026) |
|---|---|---|---|---|---|
| 1985 | USA | Solwind P78-1 (air-launched ASM-135) | ≈ 525 km | 286 | 0 |
| 2007 | China | Fengyun-1C (SC-19 missile) | ≈ 865 km | 3 534 | 2 314 |
| 2008 | USA | USA-193 (SM-3 from a ship) | ≈ 247 km | 174 | 0 |
| 2019 | India | Microsat-R (PDV Mk-II) | ≈ 283 km | 129 | 0 |
| 2021 | Russia | Cosmos 1408 (Nudol) | ≈ 480 km | 1 806 | 4 |

: Destructive direct-ascent anti-satellite tests (debris counts from the CelesTrak SATCAT). {#tbl:asattests}

![Tracked debris from destructive anti-satellite tests. Debris from the high-altitude 2007 test remains in orbit; debris from lower-altitude tests has re-entered.](figures/out/ch19_asat.svg){#fig:asat width=90%}

In April 2022 the USA announced a unilateral commitment not to conduct destructive direct-ascent ASAT missile tests, and in December 2022 the UN General Assembly adopted a resolution calling on all states to make the same commitment; dozens of countries have since joined the pledge.

### Rendezvous and Proximity Operations

Satellites that can approach other satellites — for inspection, servicing or, potentially, attack — are a growing concern because the same technology serves peaceful and hostile purposes. The USA operates the Geosynchronous Space Situational Awareness Program (GSSAP) satellites to inspect objects in GEO; Russian satellites such as Cosmos 2542, which released a sub-satellite that manoeuvred near a US reconnaissance satellite in 2020, and Luch/Olymp, which has parked near Western communication satellites, have caused public concern; and China's Shijian-21 towed a dead BeiDou satellite to a graveyard orbit in 2022, demonstrating capture technology. Orbital mechanics shapes these operations: an inspector at a slightly different orbit can perform a natural circumnavigation of its target once per orbit without using propellant (@fig:rpo).

![Relative motion of an inspector satellite around a target in geostationary orbit (Clohessy–Wiltshire equations). A suitably offset orbit produces a daily 2:1 ellipse around the target.](figures/out/ch19_rpo.svg){#fig:rpo width=86%}

### Jamming, Spoofing and Cyber Attacks

Electronic and cyber attacks are now routine in conflicts. GNSS jamming and spoofing affect aviation and shipping across large regions (Chapter 18); satellite television and communications are jammed; and the 2022 KA-SAT attack showed how a cyber attack on a satellite operator's ground network can have international effects. Because these attacks are reversible, hard to attribute and often below the threshold of armed conflict, they are difficult to deter.

### Nuclear Weapons in Space

The 1962 US Starfish Prime test, a 1.4-megaton nuclear explosion at 400 km, created artificial radiation belts that damaged or destroyed about a third of the satellites then in orbit (Chapter 22). The Outer Space Treaty (1967) prohibits placing nuclear weapons or other weapons of mass destruction in orbit. In 2024 US officials publicly expressed concern that Russia was developing a nuclear anti-satellite capability; a UN Security Council resolution reaffirming the prohibition was vetoed by Russia in April 2024.

## Law, Norms and Stability

International law applies in space. The **Outer Space Treaty** declares space the province of all humankind, prohibits national appropriation and weapons of mass destruction in orbit, and requires states to authorise and supervise their nationals' space activities; the UN Charter, including the right of self-defence, and the law of armed conflict also apply. However, there is no treaty banning conventional weapons in space or ground-based anti-satellite weapons. Diplomatic efforts include:

- Russian–Chinese proposals for a treaty on the Prevention of the Placement of Weapons in Outer Space (PPWT), criticised by Western states for lacking verification and ignoring ground-based ASATs;
- the UK-led UN Open-Ended Working Group on **reducing space threats through norms, rules and principles of responsible behaviour** (2022–23);
- the destructive DA-ASAT test moratorium;
- expert efforts to clarify how existing law applies, such as the Woomera Manual and the MILAMOS project.

Transparency measures — announcing manoeuvres, sharing space-tracking data, and establishing communication channels between space commands — aim to reduce the risk of misunderstanding in a crowded orbital environment where an accidental collision could be mistaken for an attack.

::: example
**Example: geolocating a ship radar with two satellites**

Two SIGINT satellites fly 80 km apart at 600 km altitude. A ship's navigation radar transmits pulses at 9.4 GHz.

1. The satellites time-tag each received pulse with GNSS-disciplined clocks. A time difference of 100 µs means the ship is about 30 km farther from one satellite than the other; the ship lies on a hyperbola-like curve on the sea surface (@fig:tdoa, left).
2. A timing precision of 50 ns corresponds to a range-difference precision of 15 m; geometry stretches the position error along the curve, typically to a few hundred metres.
3. The satellites also measure the Doppler shift of the pulses: their slightly different velocity vectors give a frequency difference of a few kilohertz that places the ship on a second family of curves (@fig:tdoa, right).
4. The intersection gives the ship's position. Repeating the measurement on successive pulses, or on the next pass, gives its course and speed — even if it has switched off its AIS transponder.
:::

::: ai
**AI in national-security space**

AI is used to detect objects and changes in imagery, classify radio emitters from their signal characteristics, fuse data from many sensors, detect anomalous satellite behaviour, plan collections across large constellations and support battle management. These uses raise questions about reliability, adversarial manipulation and human control, discussed in Chapters 46 and 47.
:::

::: key
**Key takeaways**

- National-security space includes ISR, missile warning, PNT, SATCOM, weather, space domain awareness, space control and launch.
- Reconnaissance satellites date from 1960 (Corona film return, GRAB SIGINT); imagery is now digital and complemented by large commercial constellations.
- SIGINT satellites intercept radar (ELINT), communications (COMINT) and telemetry (FISINT); emitters are located by angle of arrival, TDOA and FDOA, often with satellite clusters. Commercial RF geolocation now serves maritime security.
- Military SATCOM uses wide spreading and frequency hopping for jam resistance; commercial services have become important but are also targets.
- Architectures are shifting from a few exquisite satellites to proliferated, frequently replenished constellations (SDA PWSA) for resilience.
- Five destructive ASAT tests have created thousands of debris fragments; the 2007 Chinese test left debris that will persist for decades. Jamming, spoofing and cyber attacks are now routine in conflicts.
- International law applies in space, but there is no ban on conventional space weapons; norms such as the DA-ASAT test moratorium aim to improve stability.
:::
