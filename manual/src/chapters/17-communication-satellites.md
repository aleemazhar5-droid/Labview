---
title: Communication Satellites
hero: ch17
abstract: Communication satellites carry television to hundreds of millions of homes, connect ships, aircraft and remote communities to the internet, relay data from other spacecraft, and now connect ordinary smartphones directly from space. This chapter traces their evolution from passive balloons to geostationary "high-throughput" satellites delivering a terabit per second and to constellations of thousands of satellites in low orbit linked by lasers. It explains the engineering choices that shape every system — orbit, frequency band, propagation, link budget, payload architecture, frequency reuse and terminals — and the regulatory framework that shares the radio spectrum and orbits among nations. It closes with the current state of the industry in 2026: Starlink, OneWeb, Amazon Leo and the Chinese constellations, direct-to-device services, optical communications and data relay.
---

## From Science Fiction to Global Infrastructure

In October 1945 the engineer and writer Arthur C. Clarke proposed in *Wireless World* that three satellites in a 24-hour orbit above the equator could relay radio signals around the whole world. Fifteen years later the idea began to come true. NASA's **Echo 1** (1960), a 30 m aluminised balloon, reflected radio signals passively between ground stations (@fig:echo). AT&T's **Telstar 1** (1962), the first active communication satellite, relayed the first live television pictures across the Atlantic, but its low elliptical orbit meant it was visible from both continents for only minutes at a time. In 1963 Hughes' **Syncom 2** reached the first geosynchronous orbit, and in 1964 **Syncom 3** — in a true geostationary orbit — broadcast the Tokyo Olympic Games to the USA. In 1965 **Intelsat I** ("Early Bird") began commercial transatlantic telephone and television service with 240 voice circuits. The Soviet Union, whose territory lies at high latitudes, chose highly elliptical **Molniya** orbits for its own system from 1965 (@fig:commhistory).

::: figrow
![Inflation test of an Echo balloon satellite in 1958. Echo 1, launched in 1960, was a 30 m passive reflector — the first communication satellite experiment to relay voice between continents.](figures/photos/ch17_echo.jpg){#fig:echo}

![A Syncom IV communication satellite after deployment from the Space Shuttle Discovery in 1984. The Syncom name dates back to the first geosynchronous satellites of 1963–64.](figures/photos/ch17_syncom.jpg){#fig:syncom}
:::

![Milestones in satellite communications.](figures/out/ch17_history.svg){#fig:commhistory width=100%}

For half a century, communication satellites were dominated by a few hundred large geostationary satellites operated by international organisations (Intelsat, Inmarsat, Eutelsat — later privatised) and national and commercial operators. They carried international telephone trunks (until undersea fibre took over from the 1990s), distributed television to cable head-ends and directly to homes, and provided mobile communications to ships and aircraft. In the 2010s two revolutions transformed the industry: **high-throughput satellites (HTS)** in GEO, which multiplied capacity a hundredfold using many small spot beams; and **low-Earth-orbit broadband constellations** of hundreds to thousands of mass-produced satellites. In 2026 satellite communications remain the largest commercial space market, generating more than $100 billion a year in services and equipment.

![The Space Shuttle crew of STS-49 captured the stranded Intelsat VI satellite in 1992 during the first three-person spacewalk, attached a new perigee motor and sent it on to geostationary orbit. Communication satellites were among the Shuttle's main commercial payloads.](figures/photos/ch17_intelsat.jpg){#fig:intelsatrescue width=70%}

## Services and Markets

Satellite communications serve several distinct markets, each defined in the ITU Radio Regulations as a "service" with its own frequency allocations (@tbl:commservices).

| Service | Typical users | Main bands | Example systems |
|---|---|---|---|
| Fixed Satellite Service (FSS): trunking, backhaul, enterprise networks, video contribution | Telecom operators, broadcasters, businesses | C, Ku, Ka | SES, Intelsat, Eutelsat, APT, Telesat |
| Broadcasting Satellite Service (BSS): direct-to-home TV and radio | Households | Ku (TV), S/L (radio) | SES Astra, DirecTV, Dish, Sky, SiriusXM |
| Satellite broadband | Homes, businesses, communities, governments | Ku, Ka, Q/V, E | Starlink, OneWeb, Amazon Leo, Viasat, Hughes |
| Mobility: maritime and aeronautical connectivity | Ships, oil rigs, airlines, business jets | L, Ku, Ka | Inmarsat (Viasat), Panasonic, Starlink, OneWeb |
| Mobile Satellite Service (MSS): handheld voice and data, IoT | Remote workers, emergency services, militaries | L, S | Iridium, Globalstar, Inmarsat, Thuraya |
| Direct-to-device (D2D) | Ordinary smartphones | Terrestrial cellular bands, S, L | Starlink Direct to Cell, AST SpaceMobile, Lynk, Apple–Globalstar |
| Government and military satellite communications | Armed forces, civil protection | UHF, X, Ka, EHF | WGS, AEHF/ESS, Skynet, Syracuse (Chapter 19) |
| Data relay | Other spacecraft (ISS, EO satellites) | S, Ku, Ka, optical | TDRS, EDRS, Tianlian, Luch |

: Satellite communication services. {#tbl:commservices}

Broadcasting was long the most profitable segment, but linear satellite TV is declining as viewers move to internet streaming, while satellite broadband — especially LEO broadband — is growing rapidly. Starlink alone reported about 12 million customers in more than 160 countries by June 2026.

## Choosing an Orbit

The orbit determines coverage, latency, the number of satellites needed and the cost of terminals (Chapter 11).

- **Geostationary orbit (GEO)** allows a satellite to cover about a third of the Earth continuously, and simple fixed dishes to point at it. Three satellites cover the world except the polar regions. The penalty is distance: radio signals take about a quarter of a second to travel up and down, so a round trip through a GEO satellite (user → satellite → gateway → satellite → user) takes at least 477 ms, plus processing — noticeable in conversations and online gaming. The large distance also requires big antennas and high power.
- **Medium Earth orbit (MEO)** offers a compromise. SES's **O3b** and **O3b mPOWER** satellites, in an 8 062 km equatorial orbit, provide fibre-like links with round-trip latency of about 110–150 ms to cruise ships, mobile operators and governments.
- **Low Earth orbit (LEO)** at 500–1 200 km gives latencies comparable with terrestrial networks (@fig:latency) and allows smaller terminals, but each satellite is visible from a given place for only a few minutes, so hundreds to thousands of satellites, steerable user antennas and handovers between satellites are required.
- **Highly elliptical orbits (HEO)** such as Molniya and Tundra serve high latitudes. Space Norway's two Arctic Satellite Broadband Mission satellites (2024), carrying military and commercial payloads, use such orbits to provide continuous coverage of the Arctic.

![Minimum round-trip propagation time through a bent-pipe satellite versus altitude. LEO systems approach the latency of terrestrial fibre.](figures/out/ch17_latency.svg){#fig:latency width=86%}

## Frequencies, Propagation and Spectrum Sharing

### Frequency Bands

Satellite communications use bands from VHF to millimetre waves and, increasingly, optical wavelengths (Chapter 7). Lower bands (L, S) propagate well, penetrate foliage and work with small, non-directional antennas — ideal for mobile services — but offer little bandwidth. Higher bands (Ku, Ka, Q/V, E) offer gigahertz of bandwidth and allow small, high-gain antennas, but suffer from rain. The industry has migrated steadily upwards: C-band for early trunking, Ku-band for television from the 1980s, Ka-band for broadband from the 2000s, and Q/V- and E-band for gateway links in the newest systems.

### Rain Fade

Above about 10 GHz, raindrops absorb and scatter radio waves. The **specific attenuation** (dB/km) grows rapidly with frequency and rain rate (@fig:rain). A heavy tropical downpour of 100 mm/h can attenuate a Ka-band signal by 30–50 dB — enough to break any link — while the same rain costs only a few dB at Ku-band and almost nothing at C-band. Because heavy rain is rare and localised, systems are designed for a specified **availability** (for example 99.7 % of the average year, about 26 hours of outage) using statistical rain models from ITU-R Recommendations, and they combat fades with:

- **adaptive coding and modulation (ACM)**, which switches to more robust waveforms when the link degrades (standardised in DVB-S2 and DVB-S2X);
- **uplink power control**, which raises the transmitted power during a fade;
- **site diversity**, using two gateways several tens of kilometres apart, since intense rain cells rarely cover both.

![Rain attenuation versus frequency for different rain rates. Attenuation increases dramatically above about 10 GHz.](figures/out/ch17_rain.svg){#fig:rain width=86%}

### Sharing the Spectrum and the Orbits

Radio spectrum and orbital positions are limited natural resources shared by all nations. The **International Telecommunication Union (ITU)**, a United Nations agency, maintains the **Radio Regulations** — an international treaty that allocates frequency bands to services — and the **Master International Frequency Register**. A satellite operator, through its national administration, must file its planned network with the ITU, **coordinate** it with earlier networks that might suffer interference, and bring it into use within seven years. Geostationary positions are typically spaced 2–3° apart, and coordination between neighbouring operators is a complex negotiation. Every three to four years a **World Radiocommunication Conference** (WRC-23 in Dubai; WRC-27 next) revises the Regulations — for example to allocate spectrum for direct-to-device services or to set rules for lunar communications.

Non-geostationary constellations must protect GEO networks. ITU **equivalent power-flux-density (EPFD)** limits cap the interference that their combined satellites may cause to GEO terminals, which in practice means that a LEO system must not transmit along the line of sight between a ground terminal and the geostationary arc (@fig:gsoarc). Large constellations must also meet **milestones**: since 2019, ITU rules require 10 % of a constellation to be deployed within two years of the end of the seven-year bring-into-use period, 50 % within five years and 100 % within seven years. National licences add their own conditions. In the USA, for example, the FCC required Amazon's constellation to have half of its satellites (about 1 600) in orbit by July 2026; with roughly 300–400 in orbit, Amazon obtained a conditional waiver in 2026.

![A ground terminal's view of the sky. To protect geostationary networks, LEO systems avoid using satellites that appear near the geostationary arc (illustrative exclusion zone).](figures/out/ch17_gsoarc.svg){#fig:gsoarc width=86%}

## Link Budgets and Terminals

The link-budget method of Chapter 7 determines whether a link closes. @fig:satwaterfall shows the budget of a typical Ku-band direct-to-home television downlink as a "waterfall": a satellite EIRP of 52 dBW is attenuated by a free-space loss of about 206 dB over 38 000 km; a 60 cm dish with a low-noise block converter recovers about 36 dB of gain against a system noise temperature of about 120 K; and in a 27 MHz channel the resulting carrier-to-noise ratio is about 15 dB — enough for the DVB-S2 8PSK rate-3/4 waveform with a margin of more than 6 dB for rain.

![Link budget of a Ku-band direct-to-home television downlink, shown as a waterfall of gains and losses.](figures/out/ch17_waterfall.svg){#fig:satwaterfall width=96%}

Modern systems adapt their waveforms continuously. The **DVB-S2X** standard offers more than 100 combinations of modulation (from QPSK to 256APSK) and coding, achieving spectral efficiencies from below 0.5 to more than 5 bit/s/Hz, within about 1 dB of the Shannon limit. Since 2022 the 3GPP mobile standards (Release 17 onward) have included **non-terrestrial networks (NTN)**, allowing satellites to be integrated into 5G — the basis for direct-to-device services.

### User Terminals

Terminals have changed as much as satellites (@fig:terminals). The 60 cm dish for satellite TV, fixed to a wall and pointed at a GEO satellite, costs a few tens of dollars. A LEO broadband system needs an antenna that follows satellites across the sky and switches between them every few minutes. The breakthrough was the low-cost **electronically steered phased array**: Starlink's flat terminal contains about a thousand or more antenna elements whose signals are phase-shifted by custom chips to form and steer beams with no moving parts, at a cost that fell from thousands of dollars to a few hundred through mass production. Aircraft and ships use larger flat-panel or mechanically steered terminals.

![Antenna gain of typical terminals. Direct-to-device service must close the link with a smartphone's near-isotropic antenna, so the satellite antenna must be enormous.](figures/out/ch17_terminals.svg){#fig:terminals width=90%}

## The Communication Payload

### Transponders: Bent Pipe and Regenerative

The heart of a classic communication satellite is the **transponder** (@fig:payload). In a **bent-pipe** (transparent) design, the receive antenna collects the uplink signals; a low-noise amplifier boosts them; filters and frequency converters shift them from the uplink to the downlink band (for example from 14 GHz to 12 GHz at Ku-band); an **input multiplexer** divides the band into channels, typically 36–72 MHz wide; each channel is amplified by a **travelling-wave-tube amplifier (TWTA)** or a solid-state amplifier; and an **output multiplexer** recombines the channels for the transmit antenna. A bent pipe does not care what signals it carries, which makes it flexible and long-lived — a satellite launched for analogue television can carry digital broadband 15 years later.

A **regenerative** payload demodulates and decodes the uplink signals, switches or routes the data, and re-modulates it for the downlink. Regeneration improves link quality (uplink and downlink noise no longer add), enables on-board routing between beams and inter-satellite links, and is essential for networks such as Iridium and Starlink. **Digital transparent processors** sit between the two: they digitise the band and route and filter channels flexibly without decoding them.

![Architecture of bent-pipe and regenerative communication payloads.](figures/out/ch17_payload.svg){#fig:payload width=96%}

TWTAs remain the workhorse high-power amplifiers in space because of their efficiency (60–70 %) and power (tens to hundreds of watts per tube); gallium-nitride solid-state amplifiers are increasingly used, especially in phased arrays where many small amplifiers are distributed over the antenna.

### Antennas, Spot Beams and Frequency Reuse

Early satellites used a single **global beam** or a few regional beams. Capacity is limited by bandwidth, so the key to more capacity is to **reuse** the same frequencies many times. **Multi-beam antennas** — large reflectors fed by clusters of horns, or phased arrays — form tens to hundreds of narrow **spot beams**, each a few hundred kilometres wide. Adjacent beams use different frequency sub-bands or polarisations; beams that are far enough apart reuse the same ones. In the classic **four-colour** scheme (@fig:reuse), the available spectrum is split into two sub-bands and two polarisations, so each beam uses half the spectrum and the whole band is reused about a quarter as many times as there are beams. A satellite with 100 beams thus reuses its spectrum about 25 times. Smaller beams also have higher antenna gain, so users can have smaller terminals and higher data rates.

![Four-colour frequency reuse with spot beams. Neighbouring cells always use different sub-band and polarisation combinations.](figures/out/ch17_reuse.svg){#fig:reuse width=90%}

### High-Throughput Satellites

Applying this principle at Ka-band produced **high-throughput satellites (HTS)**. Eutelsat's KA-SAT (2010) had 82 spot beams and 90 Gbit/s of capacity; Viasat's ViaSat-1 (2011) offered 140 Gbit/s — more than all other satellites over North America combined at the time. Capacity per satellite has grown roughly a hundred-thousand-fold since Early Bird (@fig:capacity). Hughes' Jupiter 3 (EchoStar XXIV, 2023) provides about 500 Gbit/s. Viasat's **ViaSat-3** class was designed for more than 1 Tbit/s per satellite, but the first satellite's huge deployable reflector failed to deploy fully in 2023, sharply reducing its capacity — a reminder of the risks of large deployable structures (Chapter 5). The second ViaSat-3 was launched in late 2025.

![Throughput per satellite from Early Bird (1965) to modern HTS in GEO and to individual LEO broadband satellites.](figures/out/ch17_capacity.svg){#fig:capacity width=88%}

### Software-Defined Satellites

A GEO satellite must serve markets for 15 years that cannot be predicted when it is ordered. **Software-defined** or **flexible** satellites, such as Eutelsat Quantum (2021), Airbus OneSat, Thales Alenia Space's Space Inspire and Boeing's 702X, use digital processors and active phased-array antennas so that coverage, beam shapes, frequencies and power can be reconfigured in orbit to follow demand, or even to follow a moving ship or aircraft. Standardised designs also shorten manufacturing times from about three years to about 18 months. At the other end of the scale, start-ups such as **Astranis** build small (about 400 kg) "MicroGEO" satellites that serve a single customer or country with a dedicated software-defined payload.

### The Geostationary Industry in Transition

The rise of LEO constellations has put pressure on traditional GEO operators. Orders for large commercial GEO satellites fell from 20–25 per year in the 2000s and early 2010s to around ten or fewer in the 2020s, and operators have consolidated: Eutelsat merged with OneWeb (2023), Viasat acquired Inmarsat (2023), and SES completed its acquisition of Intelsat in July 2025. Most GEO operators now offer "multi-orbit" services combining their GEO capacity with LEO or MEO partners.

## LEO Broadband Constellations

### Earlier Attempts

LEO communication constellations are not new. Iridium (66 satellites, 1998), Globalstar (48 satellites, 1999) and Orbcomm (1990s) were built for mobile telephony and messaging, and Teledesic planned a constellation of 840 broadband satellites in the 1990s. Iridium and Globalstar went bankrupt shortly after entering service — undercut by cheaper terrestrial mobile networks — although both later recovered and replaced their constellations. What changed in the 2010s was the cost of building and launching satellites, the availability of cheap phased arrays, and soaring demand for broadband.

### Starlink

SpaceX's **Starlink** has become by far the largest satellite system ever built (@fig:commconst, @fig:starlinkgrowth). Its first 60 production-type satellites were launched in May 2019; by mid-October 2026 about 11 000 were in orbit, launched mostly by SpaceX's own reusable Falcon 9 rockets in batches of 20–30 satellites. Key features of its design include:

- **Flat-panel satellites** stacked in the fairing and released together, each with phased-array antennas for user beams (Ku-band), parabolic or phased-array antennas for gateways (Ka- and E-band), a single large solar array and **Hall-effect thrusters** using krypton or argon for orbit raising, station-keeping and de-orbiting.
- **Low altitudes** — mostly 480–560 km, in "shells" at inclinations of 43°, 53°, 70° and 97.6° (@fig:commshells). At these altitudes, failed satellites re-enter within about five years by atmospheric drag, which limits long-term debris; in 2026 SpaceX began lowering many satellites towards about 480 km.
- **Laser inter-satellite links** on all recent satellites, forming an optical mesh network that carries traffic across oceans and to places without nearby gateways (@fig:lasermesh).
- **Rapid iteration**: successive versions (v0.9, v1.0, v1.5, V2 Mini) have increased capacity per satellite. The much larger **V3** satellites, designed for about 1 Tbit/s of downlink capacity each, require the Starship launch vehicle; the first V3 satellites were deployed on Starship's fourteenth flight in September 2026.
- **Direct to Cell** satellites with large antennas that connect to ordinary phones (see below).

![Active satellites in the main broadband and mobile communication constellations in October 2026 (logarithmic scale).](figures/out/ch17_constellations.svg){#fig:commconst width=90%}

![Starlink satellites launched per year and cumulatively, 2019 to mid-October 2026.](figures/out/ch17_starlink.svg){#fig:starlinkgrowth width=84%}

![Orbital shells of the main LEO communication constellations, plotted from the October 2026 satellite catalogue. Each constellation uses a few distinct combinations of altitude and inclination.](figures/out/ch17_shells.svg){#fig:commshells width=90%}

![Laser inter-satellite links create an optical mesh network in space, routing traffic between distant users and gateways.](figures/out/ch17_lasermesh.svg){#fig:lasermesh width=94%}

### Other Constellations

- **OneWeb** (Eutelsat): about 650 satellites at 1 200 km in near-polar orbits (87.9°), built with Airbus. Rather than selling directly to consumers, OneWeb serves telecom operators, governments, enterprises and mobility providers. A second generation is being procured.
- **Amazon Leo** (formerly Project Kuiper): authorised for 3 236 satellites in shells at 590–630 km. Amazon began full-scale launches in April 2025, using Atlas V, Falcon 9, Vulcan and other rockets, and renamed the system in November 2025. About 400 satellites were in orbit by October 2026; launch-vehicle shortages, including the loss of a New Glenn rocket in a pad explosion in May 2026, slowed deployment.
- **China's Guowang** (China Satellite Network Group, about 13 000 satellites planned) and **Qianfan** (Spacesail, about 14 000 planned) began deploying in 2024; each had more than 200 satellites in orbit by October 2026.
- **Telesat Lightspeed** (Canada): about 200 satellites built by MDA in polar and inclined orbits at about 1 000–1 300 km, serving enterprise and government customers, with launches from 2026.
- **IRIS²** (EU): a multi-orbit secure-connectivity constellation of roughly 300 satellites in LEO and MEO for governmental and commercial services, with first launches expected around 2029–2030.
- **Rassvet** (Bureau 1440, Russia) began launching in 2025.

| System | Operator | Satellites (planned / active Oct 2026) | Altitude | Frequency bands | Market |
|---|---|---|---|---|---|
| Starlink | SpaceX (USA) | ≈ 12 000 authorised (Gen 1), up to ≈ 30 000 Gen 2 proposed / ≈ 11 000 | 340–570 km | Ku, Ka, E; PCS/AWS for D2C | Consumer, enterprise, mobility, government, D2C |
| OneWeb | Eutelsat (France/UK) | 648 Gen 1 / ≈ 650 | 1 200 km | Ku, Ka | Wholesale, enterprise, government |
| Amazon Leo | Amazon (USA) | 3 236 / ≈ 400 | 590–630 km | Ka | Consumer, enterprise, government |
| Guowang | China SatNet | ≈ 13 000 / ≈ 230 | 500–1 150 km | Ku, Ka, Q/V | National broadband |
| Qianfan (Spacesail) | Shanghai SSST | ≈ 14 000 / ≈ 260 | ≈ 800–1 100 km | Ku, Ka | National and international broadband |
| Lightspeed | Telesat (Canada) | 198 / first launches 2026 | ≈ 1 000–1 300 km | Ka | Enterprise, government |
| Iridium NEXT | Iridium (USA) | 66 + spares / ≈ 80 | 780 km | L, Ka | Mobile voice, IoT, safety |
| O3b mPOWER | SES (Luxembourg) | 13 / 13 | 8 062 km (MEO) | Ka | Enterprise, cruise, government |
| IRIS² | EU | ≈ 300 (LEO + MEO) / — | LEO and MEO | Ka and others | Government and commercial |

: Major non-geostationary communication constellations (approximate). {#tbl:commconst}

### Challenges

Mega-constellations raise new problems. Their satellites are visible in astronomical images as streaks and their radio emissions can interfere with radio telescopes; operators have darkened satellites, adjusted orientations and coordinated with observatories, but the effect on wide-field astronomy is significant (Chapter 38). The sheer number of satellites makes **collision avoidance** a continuous activity — Starlink satellites perform tens of thousands of automated avoidance manoeuvres per year — and raises concerns about the long-term sustainability of LEO (Chapter 21). The re-entry of thousands of satellites per year is also adding aluminium oxide to the upper atmosphere, a possible environmental effect now being studied.

### The Economics of a Constellation

A LEO broadband system is a capital-intensive bet. Building, launching and operating several thousand satellites, plus gateways and user terminals, costs on the order of $10–30 billion before the system covers its costs, and satellites must be replaced every five to seven years. Three factors dominate the economics:

1. **Cost per satellite and per launch.** Mass production on assembly lines (Starlink, OneWeb and Amazon all built factories producing several satellites per day) has reduced satellite costs to a few hundred thousand to a few million dollars each, and reusable launchers have cut launch costs per kilogram by a factor of five to ten (Chapter 34).
2. **Capacity per satellite.** Because most of the fleet flies over oceans and empty land at any moment, revenue comes only from the fraction over paying customers. Larger satellites with more capacity improve this ratio dramatically, which is why SpaceX's V3 satellites depend on Starship.
3. **Terminal cost.** A phased-array terminal that costs more to make than the customer pays for it must be subsidised. Driving terminal costs down from thousands to a few hundred dollars was essential to reaching consumers.

Vertical integration — one company building the satellites, the rockets, the terminals and the network — gave SpaceX a decisive cost advantage, and governments increasingly view sovereign broadband constellations (China's Guowang and Qianfan, the EU's IRIS²) as strategic infrastructure, not just commercial ventures.

### Satellite IoT and Machine-to-Machine Services

A separate class of constellations serves the **Internet of Things (IoT)**: tracking containers, livestock, wildlife, pipelines, ships and environmental sensors in remote areas with very small, low-power devices. Systems include Orbcomm, Iridium's short-burst data, Kinéis (France, 25 nanosatellites launched in 2024, continuing the Argos system used for wildlife tracking since 1978), Astrocast, Myriota and Swarm (acquired by SpaceX). Some use standard LoRa or NB-IoT protocols so that cheap terrestrial chips can talk to satellites. Data rates are tiny — bytes to kilobytes per day — but the number of devices could reach tens of millions.


## Mobile Satellite Services and Direct-to-Device

### Classic Mobile Satellite Systems

Mobile satellite services use L- and S-band frequencies, which suit small, non-directional antennas. **Inmarsat** (founded in 1979 for maritime safety, now part of Viasat) provides voice, data and safety services to ships and aircraft from GEO, including the Global Maritime Distress and Safety System. **Iridium**'s 66 cross-linked LEO satellites at 780 km in six near-polar planes cover the entire Earth, including the poles, for handheld phones, IoT devices and aircraft tracking; the second-generation **Iridium NEXT** constellation was completed in 2019. **Globalstar** uses bent-pipe LEO satellites and, since 2022, provides emergency messaging for Apple iPhones.

### Direct-to-Device

The newest frontier is connecting **unmodified smartphones** directly to satellites, using the phones' own cellular frequencies. The challenge is the link budget (@fig:terminals): a phone has an antenna gain of about 0 dBi and transmits only about 0.2 W, compared with a broadband terminal's 30–40 dBi. The missing gain must be provided by the satellite — with very large antennas — and by modest data rates.

- **SpaceX** launched its first Direct to Cell satellites in January 2024; by 2025 several hundred were in orbit, and T-Mobile's **T-Satellite** text and data service launched commercially in the USA in July 2025, followed by partners in Canada, Japan, Australia, Switzerland, Latin America and elsewhere. In 2025 SpaceX agreed to acquire mobile-satellite spectrum from EchoStar to expand the service.
- **AST SpaceMobile** builds satellites with enormous phased-array antennas — about 64 m² on its first five BlueBirds (2024) and about 223 m² on the second-generation BlueBirds, the largest commercial communication arrays ever flown — designed to deliver broadband speeds of up to about 120 Mbit/s per cell to ordinary phones, in partnership with AT&T, Verizon, Vodafone and others. Thirteen BlueBirds had been launched by August 2026.
- **Lynk Global**, **Skylo** (using existing GEO satellites for messaging) and Chinese providers (Tiantong) offer other approaches, and the 3GPP standards now include satellite access, so future phones and networks will treat satellites as just another cell.

## Gateways, Teleports and Networks

Satellites are only part of a communication system. **Gateways** (also called teleports or ground stations) connect the satellite network to the terrestrial internet and telephone networks. A GEO HTS may need 10–50 gateways spread over its coverage area, each with 7–9 m Ka-band antennas and fibre connections, located far enough apart that rain fades are uncorrelated. A LEO constellation needs many more — Starlink operates well over a hundred gateway sites worldwide, each with several tracking antennas — although laser links reduce the need for gateways in remote areas. Network operations centres control the satellites, allocate capacity, manage subscribers and monitor quality of service, and increasingly the whole system is managed as software, with virtualised network functions running in commercial clouds.

Satellite networks are also integrating with terrestrial networks. Mobile operators use satellite **backhaul** to connect cell towers in remote areas; airlines and shipping companies combine LEO, GEO and cellular links on the same terminal; and the 5G non-terrestrial-network standards allow a satellite to act as part of a mobile operator's radio-access network. The long-term vision is a seamless network in which users neither know nor care whether their data travel through fibre, a cell tower or a satellite.

| Satellite (operator) | Launch | Orbit | Throughput | Notes |
|---|---|---|---|---|
| KA-SAT (Eutelsat) | 2010 | GEO 9° E | ≈ 90 Gbit/s | 82 Ka-band spot beams over Europe |
| ViaSat-1 (Viasat) | 2011 | GEO | ≈ 140 Gbit/s | First HTS above 100 Gbit/s |
| Intelsat EpicNG series | 2016– | GEO | 25–60 Gbit/s each | Ku/Ka multi-spot, open architecture |
| ViaSat-2 (Viasat) | 2017 | GEO | ≈ 260 Gbit/s | Antenna deployment problem reduced capacity |
| Jupiter 3 / EchoStar XXIV (Hughes) | 2023 | GEO 95° W | ≈ 500 Gbit/s | One of the heaviest commercial GEO satellites (≈ 9 t) |
| ViaSat-3 F1, F2 (Viasat) | 2023, 2025 | GEO | designed > 1 Tbit/s each | F1 reflector partially deployed |
| O3b mPOWER (SES) | 2022– | MEO | multi-Tbit/s system | Up to ≈ 5 000 beams per satellite |

: Selected high-throughput satellites (approximate design capacities). {#tbl:hts}


## Optical Communications and Data Relay

### Laser Links

Optical communications offer far higher data rates than radio with much smaller antennas and no spectrum licensing (Chapter 7). Inter-satellite laser links are now routine in LEO constellations: Starlink operates thousands of laser terminals carrying up to about 100 Gbit/s per link. The **European Data Relay System (EDRS)** has relayed Sentinel data from LEO to Europe via GEO at 1.8 Gbit/s since 2016. NASA's **Laser Communications Relay Demonstration (LCRD)** (2021) and the **ILLUMA-T** terminal on the ISS (2023) demonstrated an end-to-end laser relay from the space station through GEO to the ground, and the TBIRD CubeSat (2022) downlinked at 200 Gbit/s. The main limitation of space-to-ground laser links is cloud cover, which is overcome with networks of optical ground stations in dry locations.

![NASA's optical communications demonstrations: the Lunar Laser Communications Demonstration (2013), Deep Space Optical Communications on Psyche (2023), ILLUMA-T on the ISS, LCRD in geostationary orbit, TBIRD and the Orion Artemis II optical system.](figures/photos/ch17_illumat.jpg){#fig:optdemos width=82%}

### Data Relay Satellites

Low-orbiting spacecraft see a given ground station for only about 10 minutes per pass. **Data relay satellites** in GEO provide near-continuous contact. NASA's **Tracking and Data Relay Satellite System (TDRSS)**, operating since 1983, has supported the Space Shuttle, the ISS, the Hubble Space Telescope and many science missions; TDRS-M, launched in 2017 (the chapter's opening image), was the last of the series. NASA plans to retire TDRS in the 2030s and buy relay services from commercial providers instead, and in 2022 it awarded development agreements to several companies for this purpose. China operates the Tianlian relay satellites and Russia the Luch series; ESA's EDRS uses laser links.

::: example
**Example: how many satellites does a LEO broadband system need?**

*Coverage.* A satellite at 550 km serving users at elevations above 25° covers a circle of Earth-central half-angle

$$\lambda = \arccos\!\left(\frac{R_E\cos\varepsilon}{R_E+h}\right)-\varepsilon = \arccos\!\left(\frac{6371\cos 25^\circ}{6921}\right) - 25^\circ \approx 8.4^\circ$$

so each footprint covers about 2.8 million km² — about 0.54 % of the Earth's surface. Continuous single coverage of the whole Earth therefore needs at least about 190 satellites, and in practice, with overlap and uneven distribution, 300–600.

*Capacity.* Suppose 10 million subscribers in the busiest regions each need an average of 3 Mbit/s at the evening peak, after statistical multiplexing: a total demand of 30 Tbit/s. Only satellites above populated areas carry this traffic, perhaps 10–15 % of the fleet at any moment. With 100 Gbit/s per satellite, about 300 satellites must be over the busy regions — implying a fleet of 2 000–3 000 satellites. Doubling the subscriber base or the demand per user doubles the fleet unless capacity per satellite grows.

This is why broadband constellations are sized by **capacity**, not coverage, and why capacity per satellite (and the launch vehicle needed to carry larger satellites) is the key to their economics.
:::

::: ai
**AI in satellite communications**

Modern satellite networks are too complex to manage by hand. Machine learning predicts traffic demand and rain fades, allocates beams, frequencies and power dynamically on software-defined satellites, routes traffic through laser meshes, detects interference and jamming, and plans collision-avoidance manoeuvres for thousands of satellites. Chapter 45 discusses AI for satellite operations and networks.
:::

::: key
**Key takeaways**

- Communication satellites evolved from passive balloons (Echo, 1960) through GEO trunking and broadcasting to high-throughput GEO satellites and LEO broadband constellations.
- Orbit choice trades coverage and simplicity (GEO) against latency and terminal size (LEO); MEO and HEO fill specific niches.
- Higher frequencies give more bandwidth but suffer rain fade; systems use adaptive coding and modulation, power control and site diversity.
- The ITU allocates spectrum and coordinates orbital positions; EPFD limits protect GEO from LEO interference; milestone rules require constellations to be deployed on time.
- Capacity comes from frequency reuse with many spot beams; HTS increased GEO capacity per satellite to 0.5–1 Tbit/s.
- Starlink (about 11 000 satellites in October 2026 and about 12 million customers) has transformed the market; OneWeb, Amazon Leo, Guowang, Qianfan and others follow.
- Direct-to-device services connect ordinary phones by using very large antennas in orbit and 3GPP non-terrestrial-network standards.
- Laser links are now routine between satellites; data-relay satellites keep low-orbit spacecraft in near-continuous contact.
:::
