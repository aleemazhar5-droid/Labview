---
title: Sounding Rockets and Suborbital Vehicles
hero: ch09
abstract: A suborbital flight goes up into space and comes straight back down, without reaching orbital speed. Sounding rockets have used such flights since the 1940s to measure the upper atmosphere, observe the Sun and stars, test spacecraft technology and provide minutes of high-quality weightlessness. Since 2021, commercial vehicles have carried paying passengers on similar trajectories. This chapter explains suborbital trajectories, sounding-rocket design and operations, the science and technology they enable, microgravity research platforms, crewed suborbital vehicles, hypersonic test flights and the infrastructure and regulation that support them.
---

## What "Suborbital" Means

A **suborbital** trajectory is one whose path intersects the Earth's surface: the vehicle does not have enough horizontal speed to stay in orbit. A suborbital flight may still go very high — sounding rockets have reached more than 1 500 km — and spend many minutes above the atmosphere. Suborbital flights include:

- **Sounding rockets** — unguided or minimally guided research rockets that carry instruments on a nearly vertical trajectory;
- **Crewed suborbital spacecraft** — vehicles such as Blue Origin's New Shepard and Virgin Galactic's SpaceShipTwo, carrying tourists and researchers;
- **Rocket-powered research aircraft and spaceplanes** — the X-15 of the 1960s, SpaceShipOne in 2004, and future hypersonic vehicles (Chapter 10);
- **Test flights** of orbital vehicles (for example Starship's early flights and launch-abort tests) and **hypersonic test vehicles**;
- **Ballistic missiles**, which follow suborbital trajectories (discussed only as context in Chapter 20).

The energy needed is much smaller than for orbit. Rising vertically to 100 km requires a burnout speed of about 1.4 km/s (ignoring drag and the height gained during the burn); reaching 300 km requires about 2.4 km/s; 1 000 km about 4 km/s — compared with roughly 9.4 km/s, including losses, to reach low Earth orbit.

::: key
**Key concept — suborbital flight is a vertical cannon shot**

After the motor burns out, a sounding rocket coasts upward like a stone thrown in the air, slowing under gravity until it stops at apogee and falls back. Above about 80–100 km, air drag is negligible, so everything aboard — instruments, fluids, passengers — falls together and is weightless. The weightless time grows roughly with the square root of the height above the atmosphere: about 3 minutes for a 105 km apogee, 6 minutes for 260 km and 13 minutes for 700 km (@fig:microtime).
:::

## Suborbital Trajectories

### Ballistic Flight

Neglecting drag above the atmosphere, a vertically launched rocket with burnout speed $v_b$ at altitude $h_b$ reaches an apogee given by energy conservation:

$$\frac{v_b^2}{2} - \frac{\mu}{R + h_b} = -\frac{\mu}{R + h_{apo}} \quad\Rightarrow\quad h_{apo} = \frac{R + h_b}{1 - \dfrac{v_b^2 (R + h_b)}{2\mu}} - R$$

For low apogees this reduces to the flat-Earth result $h_{apo} \approx h_b + v_b^2/2g$. Sounding rockets are not launched exactly vertically — typically at 80–88° elevation — so that spent stages and the payload fall into a designated impact area downrange (@fig:trajectories); the launch elevation and azimuth are adjusted for winds before each launch (**wind weighting**), because unguided rockets weathercock into the wind while their fins are effective at low speed.

![Computed altitude–time and altitude–downrange profiles for five representative sounding rockets after motor burnout. Higher apogees mean longer flights and longer impact ranges.](figures/out/ch09_trajectories.svg){#fig:trajectories width=100%}

### Microgravity Time

The time spent above a given altitude depends only on the apogee (@fig:microtime). Because drag is negligible above about 100 km, a sounding rocket provides residual accelerations of only $10^{-5}$–$10^{-6}$ g once its attitude control system has stopped firing — better than the International Space Station, where crew motion, pumps and fans create disturbances.

![Time spent above 100 km and above 80 km as a function of apogee for a vertical ballistic flight, with typical quoted weightless times for several vehicles.](figures/out/ch09_micro_time.svg){#fig:microtime width=86%}

### Re-entry

On the way down, the payload re-enters at roughly the speed it had at burnout. For a 300 km apogee this is about 2.3 km/s — enough to produce significant aerodynamic heating and decelerations of 20–50 g, but far milder than orbital re-entry. Payloads that are to be recovered carry a parachute system, deployed at about 5 km altitude after the payload has slowed to subsonic speed; recovery is by helicopter over land (White Sands, Esrange) or by ship at sea (Wallops, Andøya).

## Sounding Rockets

### History

The first scientific rockets were captured German V-2 missiles, launched from White Sands, New Mexico, from 1946. They carried cosmic-ray counters, spectrographs and cameras, and in October 1946 returned the first photographs of Earth from above 100 km. Purpose-built sounding rockets followed: the US Aerobee (from 1947), Viking and Nike-based vehicles; the British Skylark (1957–2005, 441 launches); the Canadian Black Brant (from 1961); and many others in France, Japan, India, the USSR and China.

Sounding rockets made fundamental discoveries:

- **X-ray astronomy** was born on 18 June 1962, when an Aerobee rocket launched by Riccardo Giacconi's team detected the first X-ray source outside the Solar System, Scorpius X-1 — work recognised with the 2002 Nobel Prize in Physics.
- The **solar extreme-ultraviolet and X-ray spectrum** was first measured from rockets in the late 1940s and 1950s.
- Rocket measurements mapped the **ionosphere**, the **mesosphere** and the **thermosphere**, and discovered phenomena such as the airglow layers and the auroral electrojet.
- India's space programme began with a Nike-Apache launched from a church at **Thumba** in November 1963.

### Anatomy of a Sounding Rocket

A typical modern sounding rocket (@fig:anatomy) has one to four solid-propellant motor stages, fins for aerodynamic stability, and a payload made of modular cylindrical sections:

- **Motors.** Military-surplus motors (Terrier, Talos, Nike) and purpose-built motors (Black Brant, Nihka, Oriole, Brazil's S-30/S-31, Germany's improved Orion and ESA/DLR's Rheinmetall-built motors) give total burn times of 30–90 seconds.
- **Ignition and despin module.** Rockets are spun at a few revolutions per second during powered flight for stability (by canted fins and spin motors), then despun with **yo-yo weights** — masses on cables that unwind and carry away angular momentum.
- **Telemetry and power.** S-band transmitters send data at up to tens of Mbit/s; batteries provide power for 10–20 minutes.
- **Attitude control system (ACS).** Cold-gas thrusters and gyros, often with a Sun sensor or star tracker, point instruments to arcseconds (for solar and astronomical payloads) or hold the payload still (for microgravity).
- **Experiment modules.** The scientific instruments, often with vacuum doors that open above the atmosphere.
- **Recovery system.** A parachute and, for sea recovery, flotation and beacons.
- **Nose cone.** Protects the payload during ascent and is ejected in space.

![Anatomy of a two-stage sounding rocket, based on the NASA Black Brant IX configuration.](figures/out/ch09_anatomy.svg){#fig:anatomy width=100%}

### Vehicles Around the World

NASA's **Sounding Rocket Program**, managed from Wallops Flight Facility and operated with contractors, flies about 20 missions a year using a family of vehicles assembled from a small set of motors (@fig:nasafamily, @tbl:sounders). Magellan Aerospace's Black Brant has flown more than 1 000 times, with a reported success rate of 99.4 % over its last 500 launches.

![Approximate payload–apogee performance of NASA sounding-rocket vehicles.](figures/out/ch09_nasa_family.svg){#fig:nasafamily width=86%}

Table: Selected sounding rockets in current or recent use. {#tbl:sounders}

| Vehicle | Country / operator | Stages | Typical payload | Typical apogee | Notes |
|---|---|---|---|---|---|
| Terrier-Improved Orion | USA (NASA) | 2 | 50–400 kg | 70–200 km | Student and technology flights (RockSat-X, RockOn) |
| Terrier-Improved Malemute | USA (NASA) | 2 | 50–300 kg | 250–650 km | Atmospheric and technology missions |
| Black Brant IX | USA / Canada | 2 (Terrier–BB) | 150–700 kg | 200–420 km | Workhorse for solar and astrophysics |
| Black Brant X, XI, XII | USA / Canada | 3–4 | 100–800 kg | 380–1 500 km | Long-duration ionospheric and auroral missions |
| Terrier-Oriole | USA | 2 | 150–650 kg | 190–450 km | Higher-performance option |
| VSB-30 | Brazil (DCTA/IAE) with DLR | 2 | ≈ 400 kg | ≈ 260 km | Used for TEXUS and MAPHEUS microgravity missions |
| VS-30 / VS-31 | Brazil | 1–2 | 260–300 kg | ≈ 120–160 km | Atmospheric and hypersonic research |
| MAXUS | ESA / Sweden / Germany | 1 (Castor 4B) | ≈ 800 kg | ≈ 700 km | 12–13 minutes of microgravity |
| Improved Orion, REXUS | DLR / SSC | 1–2 | 30–100 kg | 80–100 km | European student programme REXUS/BEXUS |
| S-310, S-520, SS-520 | Japan (JAXA) | 1–3 | 50–150 kg | 150–800 km | SS-520-5 orbited a CubeSat in 2018 (smallest orbital rocket) |
| RH-200, RH-300, RH-560 | India (ISRO) | 1–2 | 10–100 kg | 70–500 km | Rohini series since 1967 |
| Various solid rockets | China (CAS, CASIC) | 1–2 | varied | 100–200+ km | Atmospheric research, technology and tourism demonstrators |

### Launch Ranges

Sounding rockets need ranges with large unpopulated impact areas, tracking radars and telemetry stations, and safety infrastructure (@fig:ranges). Major ranges include NASA's **Wallops Flight Facility** (Virginia), **White Sands Missile Range** (New Mexico), **Poker Flat Research Range** (Alaska, operated by the University of Alaska Fairbanks for auroral science), the **Andøya Space** range and **SvalRak** (Norway), **Esrange** (Sweden), **Woomera** (Australia), **Kwajalein** (Marshall Islands, for equatorial ionosphere studies), **Alcântara** and **Barreira do Inferno** (Brazil), **Thumba** (India), **Uchinoura** (Japan) and **El Arenosillo** (Spain). High-latitude ranges let rockets fly directly into the aurora.

![Selected sounding-rocket and suborbital launch sites.](figures/out/ch09_ranges.png){#fig:ranges width=96%}

::: figrow
![A NASA rocket launches from Poker Flat Research Range in Alaska into the aurora during the M-TeX and MIST campaign. Long-exposure photographs record the rocket trails.](figures/photos/ch09_mtex.jpg){#fig:mtex}

![Red vapour tracer released by the EVEX mission over Kwajalein Atoll (2013) to measure winds in the equatorial ionosphere.](figures/photos/ch09_evex.jpg){#fig:evex}
:::

### Scientific Uses

Sounding rockets remain irreplaceable for several kinds of science:

- **In-situ measurement of the mesosphere and lower thermosphere (50–150 km)** — the "ignorosphere", too high for balloons and too low for satellites. Rockets carry neutral and ion mass spectrometers, Langmuir probes, electric-field booms and particle detectors directly through the region. They also release **chemical tracers** — trimethylaluminium, barium, sodium, lithium — that glow or scatter sunlight so that ground cameras can measure winds and electric fields (@fig:vapor).
- **Auroral and ionospheric physics** — rockets fly through auroral arcs to measure the particles and fields that create them; multi-rocket campaigns (e.g., NASA's Grand Challenge Initiative – Cusp, 2019) and rocket–satellite conjunctions resolve spatial and temporal structure.
- **Solar physics** — high-resolution ultraviolet and X-ray instruments that test concepts for future satellites (Hi-C, CLASP, FOXSI, MaGIXS) observe the Sun for about 5 minutes per flight.
- **Astrophysics** — ultraviolet and X-ray spectroscopy of hot gas, galaxies and the diffuse background (e.g., CIBER, FIRE, the Micro-X microcalorimeter).
- **Planetary science** — rockets observed Comet Halley, Comet Hale-Bopp and planetary atmospheres in the ultraviolet.
- **Calibration** — under-flights of satellites with calibrated instruments (e.g., SDO's EVE instrument, calibrated by rocket flights).

![Artificial clouds formed by vapour tracers released from a NASA sounding rocket over the US East Coast. Ground cameras track their motion to measure upper-atmosphere winds.](figures/photos/ch09_clouds.jpg){#fig:vapor width=82%}


### Anatomy of a Mission: From Proposal to Flight

A NASA sounding-rocket mission typically takes two to three years from selection to launch — fast by space standards. A principal investigator proposes an experiment through NASA's Research Opportunities in Space and Earth Sciences (ROSES); once selected, the Wallops team assigns a mission manager and works with the scientists through a requirements definition meeting, design review and mission readiness review. Payload integration and testing at Wallops (vibration, spin balance, bend tests, mass properties, horizontal and vertical sequence tests with the real telemetry and attitude systems) takes a few weeks. The payload is then shipped to the range, where a launch window of one to three weeks is held for the right geophysical or astronomical conditions: an active aurora overhead, a solar target at the right elevation, or dark skies for an astronomical observation.

@fig:sequence shows the sequence of events for a typical Black Brant IX solar or astronomy mission.

![Sequence of events for a typical Black Brant IX science mission, from rail launch to parachute landing about 15 minutes later.](figures/out/ch09_sequence.svg){#fig:sequence width=100%}

Table: A simplified sequence of events for a Black Brant IX solar mission (representative timings). {#tbl:soe}

| Time | Event | Notes |
|---|---|---|
| T−6 h to T−30 min | Final payload checks, ACS gas loading, vacuum pump-down of instruments | Science team monitors detector temperatures |
| T−15 min | Wind measurement and launcher setting | Elevation ≈ 85–87°, azimuth adjusted for wind weighting |
| T+0 | Lift-off from the rail launcher; Terrier first stage burns ≈ 6 s | Spin-up by canted fins |
| T+12 s | Black Brant second-stage ignition after coast | Burn ≈ 32 s |
| T+44 s | Burnout at ≈ 2.3 km/s, ≈ 80 km altitude | Accelerations up to ≈ 12 g |
| T+60 s | Nose cone ejection, despin with yo-yos, motor separation | Payload rates < 1°/s |
| T+70–90 s | ACS acquires the Sun; shutter doors open above ≈ 100 km | Pointing accuracy ≈ 1 arcsec with fine Sun sensor |
| T+90–470 s | Science observations | Data telemetered live at up to ≈ 20–40 Mbit/s; images also stored onboard |
| T+280 s | Apogee ≈ 320 km | |
| T+470 s | Doors close, payload put in re-entry attitude | |
| T+720 s | Main parachute deploys at ≈ 5 km | Payload descends at ≈ 8 m/s |
| ≈ T+15 min | Landing ≈ 80 km downrange | Helicopter recovery; reflight of instrument possible |

### Solar and Astrophysics Instruments on Rockets

Because a rocket flight lasts only minutes, instruments are designed to make one measurement extremely well. Recent examples include:

- **Hi-C (High-resolution Coronal Imager)** — an extreme-ultraviolet telescope that imaged the solar corona at about 0.3 arcsec resolution (five times better than SDO's AIA), revealing fine magnetic "braids" (flights in 2012, 2018 and 2024).
- **CLASP / CLASP2** — a Japan–US–Europe ultraviolet spectropolarimeter that measured magnetic fields in the solar chromosphere for the first time using the Hanle effect (2015, 2019, 2021).
- **FOXSI** — a focusing hard X-ray telescope that observes faint solar flares and nanoflares (flights 2012–2024), a pathfinder for future satellites.
- **MaGIXS** — a soft X-ray spectrometer that measures plasma composition in active regions.
- **Micro-X** — the first X-ray microcalorimeter flown with a transition-edge-sensor array, observing supernova remnants.
- **CIBER and CIBER-2** — measurements of the near-infrared extragalactic background light.

Many of these instruments are recovered and reflown, and their technologies feed into satellite missions such as Solar Orbiter, MUSE (Multi-slit Solar Explorer) and future X-ray observatories.

### Technology Demonstration and Training

Sounding rockets also serve as cheap, fast test beds — "a space mission in a year" — for new technologies before they fly on satellites: star trackers, detectors, deployable booms, atmospheric re-entry experiments, telemetry systems and attitude-control software. NASA's **Flight Opportunities** programme buys flights on commercial suborbital vehicles for the same purpose. Equally important, sounding rockets train scientists and engineers: a graduate student can design, build, launch and analyse an instrument within a PhD. Student programmes include NASA's RockOn and RockSat-X, ESA/DLR/SNSA's REXUS/BEXUS, and many university rocketry teams.

## Microgravity Research Platforms

Gravity affects many processes in subtle ways: it drives buoyant convection in fluids, sedimentation, hydrostatic pressure, and the structure of flames. Removing it lets researchers study fundamental physics (fluid dynamics, combustion, crystal growth, soft matter), biology (cell behaviour, plant growth, physiology) and materials processing. Several platforms provide reduced gravity, trading duration against quality and cost (@fig:microgplatforms, @tbl:microgravity).

![Duration and quality of reduced gravity provided by different research platforms.](figures/out/ch09_platforms.svg){#fig:microgplatforms width=86%}

Table: Microgravity research platforms. {#tbl:microgravity}

| Platform | Duration | Residual acceleration | Typical cost per experiment | Examples |
|---|---|---|---|---|
| Drop towers and tubes | 2–10 s | 10⁻⁶ g | Low (thousands of €) | ZARM Bremen (146 m tower, 4.7 s; 9.3 s with catapult); NASA Glenn Zero Gravity Research Facility (5.2 s); Beijing NMLC |
| Parabolic flights | ≈ 20–25 s × 30+ parabolas | 10⁻² g | Moderate | Novespace Airbus A310 Zero-G (France); Zero Gravity Corporation (US); national programmes in Russia, China |
| Sounding rockets | 3–15 min | 10⁻⁵–10⁻⁶ g | Moderate–high | TEXUS, MAPHEUS, MASER (≈ 6 min), MAXUS (≈ 12.5 min), Black Brant |
| Crewed suborbital vehicles | 3–4 min | 10⁻²–10⁻³ g (vibration, crew) | Moderate | New Shepard (paused 2026), SpaceShipTwo/Delta |
| Orbital free-flyers and capsules | days–months | 10⁻⁶ g | High | Chinese SJ-10, Varda W-series, Photon/Bion (Russia), Space Rider (planned) |
| Space stations | months–years | 10⁻⁶–10⁻⁴ g | High | ISS (US, Europe, Japan, Russia), Tiangong |

::: example
**Worked example — how long a microgravity experiment for an apogee of 260 km?**

The TEXUS missions launched on VSB-30 rockets from Esrange reach about 260 km. Using the vertical-flight formula with an average gravity $g \approx 9.3$ m/s² between 100 and 260 km, the time above 100 km is $2\sqrt{2\times160\,000/9.3} \approx 371$ s ≈ 6.2 min. After motor separation, despin and settling of residual rates, about 6 minutes of high-quality microgravity are available — enough for experiments on crystal growth, solidification of metal alloys, and biological processes. The payload then re-enters, deploys its parachute at about 5 km and lands about 70 km downrange, where helicopters recover it within an hour.
:::

## Crewed Suborbital Spaceflight

### From the X-15 to SpaceShipOne

The first humans to make suborbital spaceflights were the Mercury astronauts **Alan Shepard** (Freedom 7, 5 May 1961, 187 km apogee) and **Gus Grissom** (Liberty Bell 7), launched on Redstone rockets. Between 1959 and 1968 the **North American X-15** rocket plane, air-launched from a B-52 at about 13.7 km, made 199 flights, reaching Mach 6.7 and, on 13 flights, altitudes above 80 km; two flights by Joe Walker in 1963 exceeded 100 km (maximum 107.8 km). The X-15 programme provided much of the knowledge of hypersonic flight, reaction controls and pressure suits used later in the Space Shuttle.

In 2004 **SpaceShipOne**, built by Scaled Composites with funding from Paul Allen, became the first privately developed crewed vehicle to reach space, winning the US$10 million **Ansari X Prize** with two flights above 100 km within two weeks. Its innovations — a hybrid rocket motor (rubber fuel with nitrous oxide oxidiser) and a "feathering" wing that folds upward to stabilise re-entry like a shuttlecock — were carried into Virgin Galactic's SpaceShipTwo.

### Blue Origin New Shepard

**New Shepard** is a fully reusable, vertically launched suborbital system named after Alan Shepard (@fig:profiles). A single-stage booster powered by one BE-3PM liquid-hydrogen/liquid-oxygen engine (≈ 490 kN) lifts a pressurised capsule with six large windows and six seats. After main engine cut-off at about 55–60 km, the capsule separates and coasts to an apogee of about 105–107 km, giving 3–4 minutes of weightlessness. The booster returns and lands vertically on a pad near the launch site using its engine and drag brakes; the capsule descends under three main parachutes, firing a retro-thrust system just before touchdown in the West Texas desert. The capsule has a launch escape motor that can pull it away from a failing booster — used successfully in an uncrewed in-flight test in 2016 and in the NS-23 booster failure in September 2022.

New Shepard began crewed flights on 20 July 2021 with Jeff Bezos aboard. By January 2026 it had flown 38 times, carried 98 people above the Kármán line and more than 200 research payloads. On 30 January 2026 Blue Origin announced that it would **pause New Shepard flights for at least two years** to redirect resources to its lunar lander programme.

### Virgin Galactic SpaceShipTwo and the Delta Class

Virgin Galactic's **SpaceShipTwo** is air-launched from the carrier aircraft **VMS Eve** at about 14 km. Its hybrid rocket motor fires for about 60 seconds, accelerating the spaceplane to about Mach 3 and an apogee of about 85–90 km — above the US 80 km astronaut boundary but below the Kármán line. The twin tail booms then feather upward for a stable, self-correcting re-entry, after which the vehicle glides to a runway landing at Spaceport America, New Mexico. The programme suffered a fatal accident in 2014, when the first vehicle (VSS Enterprise) broke up after its feather was unlocked prematurely during a powered test flight, killing co-pilot Michael Alsbury. Its successor, **VSS Unity**, flew commercial missions from June 2023 (Galactic 01) to June 2024 (Galactic 07) and was then retired. Virgin Galactic is building a new **Delta-class** fleet designed to fly twice a week with six passengers each; as of mid-2026 the company planned flight tests of the first Delta ship in the third quarter of 2026 and rocket-powered spaceflight in the fourth quarter, with commercial service ramping up in 2027.

![Comparison of the New Shepard vertical-launch profile and the SpaceShipTwo air-launched profile.](figures/out/ch09_suborbital_profiles.svg){#fig:profiles width=98%}

Table: Crewed suborbital vehicles. {#tbl:crewedsub}

| Vehicle | Operator | Launch mode | Propulsion | Apogee | Passengers | Status (Oct 2026) |
|---|---|---|---|---|---|---|
| Mercury-Redstone | NASA | Vertical, expendable | Alcohol/LOX | 187–190 km | 1 | 2 flights (1961) |
| X-15 | NASA / USAF | Air launch from B-52 | XLR99 (NH₃/LOX) | up to 107.8 km | 1 pilot | 199 flights (1959–68) |
| SpaceShipOne | Scaled Composites | Air launch from White Knight | Hybrid (HTPB/N₂O) | 112 km | 1 pilot (+ ballast) | 3 spaceflights (2004) |
| New Shepard | Blue Origin | Vertical, reusable booster and capsule | BE-3PM (LH₂/LOX) | ≈ 105–107 km | 6 | 38 flights, 98 people; paused 2026 |
| SpaceShipTwo (VSS Unity) | Virgin Galactic | Air launch from VMS Eve | Hybrid (HTPB/N₂O) | ≈ 85–90 km | 2 pilots + 4 | Retired 2024 after 11 spaceflights |
| Delta class | Virgin Galactic | Air launch | Hybrid | ≈ 85–90 km | 2 pilots + 6 | First spaceflight planned late 2026 |
| Chinese suborbital tourism vehicles | CAS Space, Deep Blue Aerospace and others | Vertical | Liquid | > 100 km planned | 6–7 planned | In development (first flights targeted for late 2020s) |


### Engineering of Crewed Suborbital Vehicles

**Hybrid propulsion.** SpaceShipOne and SpaceShipTwo use **hybrid rocket motors**, which combine a liquid or gaseous oxidiser with a solid fuel (@fig:hybrid). Because the fuel and oxidiser are stored separately and only mix in the combustion port, a hybrid cannot detonate like a mixed solid propellant and can be shut down by closing the oxidiser valve. Nitrous oxide is attractive because it is self-pressurising (its vapour pressure is about 50 bar at room temperature), avoiding pumps; HTPB rubber or polyamide fuels are cheap and inert. Hybrids have lower regression rates (the speed at which the fuel surface burns back) and lower Isp (≈ 250 s) than liquid engines, and their combustion can be rough; paraffin-based fuels, which form a liquid layer that sheds droplets into the flow, burn three to four times faster.

![Principle of a hybrid rocket motor as used on SpaceShipOne and SpaceShipTwo.](figures/out/ch09_hybrid.svg){#fig:hybrid width=88%}

**Liquid-hydrogen propulsion and reusability.** New Shepard's BE-3PM engine burns liquid hydrogen and liquid oxygen at high efficiency and can be deeply throttled (to about 20 % of full thrust) for the vertical landing. The booster uses a ring fin and wedge fins for aerodynamic stability on descent, drag brakes to slow down, and the engine for a final landing burn — an approach later scaled up for orbital boosters (Chapter 34).

**Escape systems.** A crew capsule escape system must pull the crew away from a failing booster at any point in flight, faster than an explosion can propagate. New Shepard's solid escape motor in the capsule base delivers a short, high-acceleration impulse (about 10 g). SpaceShipTwo, being a winged vehicle released from a carrier aircraft, has no escape system; its safety relies on the reliability of the hybrid motor and on the feather mechanism, which was redesigned with an inhibit after the 2014 accident.

**Cabin and environment.** Suborbital cabins are pressurised to about sea-level conditions, with oxygen masks for emergencies (SpaceShipTwo pilots wear pressure suits; New Shepard passengers do not). Seats are designed for re-entry decelerations of 5–6 g in the "eyeballs-in" direction, which healthy adults tolerate well. Medical screening is lighter than for orbital flight: people in their 80s and 90s have flown, including Wally Funk (82) in 2021 and William Shatner (90) in 2021.

### Passenger Experience and Safety

A suborbital passenger experiences 3–4 g during ascent (New Shepard) or up to about 3.5 g along the axis and 6 g during the pull-out on re-entry (SpaceShipTwo), 3–4 minutes of weightlessness, and a view of the Earth's curvature against a black sky. Training takes one to a few days. In the United States, the **Commercial Space Launch Amendments Act of 2004** established an "informed consent" regime: passengers ("spaceflight participants") must be told the risks, and the FAA regulates public safety rather than occupant safety; a "learning period" moratorium on occupant-safety regulation has been extended repeatedly by Congress. Suborbital flights are therefore not certified like airliners.

::: data
**Data box — who counts as an astronaut?**

- **FAI (international records body):** 100 km (Kármán line).
- **US Air Force, NASA, FAA:** 50 statute miles (80.5 km).
- **FAA Commercial Space Astronaut Wings:** awarded 2004–2021 to crew (not passengers) who reached 50 miles; the programme ended in January 2022, after which names of all who reach the altitude are listed on the FAA website.
- **Virgin Galactic flights** (≈ 86–89 km) cross the US boundary but not the FAI boundary; **New Shepard flights** cross both.
:::

## Hypersonic and Re-entry Test Flights

Suborbital trajectories are ideal for testing vehicles and materials at hypersonic speeds (above Mach 5):

- **Re-entry experiments** — heat-shield materials and capsule shapes, e.g., NASA's IRVE inflatable re-entry experiments on Black Brant rockets (2009–2012), ESA's EXPERT and the Intermediate eXperimental Vehicle (IXV, 2015, launched on Vega to 412 km).
- **Air-breathing hypersonic propulsion** — NASA's X-43A scramjet (2004, Mach 9.6, launched on a Pegasus booster from a B-52) and the USAF/DARPA X-51A Waverider (2013, Mach 5.1 for 210 s), Australia's HIFiRE programme (sounding rockets from Woomera), and many more recent national programmes.
- **Commercial hypersonic test services** — Rocket Lab's **HASTE** (a suborbital variant of Electron, flying from Wallops since 2023) and several start-ups provide flights for defence hypersonic testing, reflecting a large increase in US Department of Defense test cadence.

![NASA's B-52B carrier aircraft takes off from Edwards Air Force Base in 2004 carrying the third X-43A scramjet research vehicle mounted on a Pegasus booster. The X-43A reached Mach 9.6 — the fastest flight of an air-breathing vehicle.](figures/photos/ch09_x43.jpg){#fig:x43 width=80%}


## New Suborbital Vehicles and Reusable Sounding Rockets

A new generation of reusable suborbital vehicles aims to reduce cost and increase flight rates for research, testing and training:

- **Dawn Aerospace Mk-II Aurora** (New Zealand) — a small rocket-powered spaceplane that takes off from a runway, intended to fly to 100 km several times per day. It became the first civil aircraft to fly supersonic since Concorde when it exceeded Mach 1 in November 2024, using a liquid bipropellant engine.
- **PLD Space MIURA 1** (Spain) — a liquid-propellant suborbital rocket that flew in October 2023 from El Arenosillo as a pathfinder for the orbital MIURA 5.
- **Chinese suborbital vehicles** — several companies (CAS Space, Deep Blue Aerospace and others) are developing vertical-takeoff, vertical-landing suborbital rockets and capsules for tourism and research, with first crewed flights targeted for the late 2020s.
- **Reusable sounding rockets** — concepts in Europe and Japan (e.g., JAXA's RV-X demonstrator for reusable rocket technology) test throttleable engines, landing guidance and rapid turnaround.
- **Hypersonic test beds** — Rocket Lab's HASTE, Stratolaunch's Talon-A reusable hypersonic vehicle (first powered hypersonic flight in December 2024, launched from the Roc aircraft) and others serve the growing demand for hypersonic testing.

## Milestones of Suborbital Flight

Table: Milestones of suborbital and sounding-rocket flight. {#tbl:submilestones}

| Year | Milestone |
|---|---|
| 1944 | A German V-2 test rocket (MW 18014) becomes the first human-made object to cross 100 km |
| 1946 | First scientific V-2 flights from White Sands; first photograph of Earth from above 100 km |
| 1947 | First animals (fruit flies) launched to space on a V-2 and recovered alive |
| 1949 | Bumper-WAC two-stage rocket reaches 393 km |
| 1957 | First British Skylark launch (Woomera) |
| 1961 | Alan Shepard's Freedom 7 — first American in space (suborbital) |
| 1962 | Aerobee rocket discovers Scorpius X-1, founding X-ray astronomy |
| 1963 | X-15 exceeds 100 km (Joe Walker); India's first sounding rocket from Thumba |
| 1980s | TEXUS (1977–) and MASER microgravity programmes establish European microgravity research |
| 1992 | First MAXUS flight (12+ minutes of microgravity) |
| 2004 | SpaceShipOne wins the Ansari X Prize |
| 2015 | New Shepard becomes the first booster to fly to space and land vertically |
| 2018 | Japan's SS-520-5, a modified sounding rocket, orbits a 3U CubeSat |
| 2021 | First commercial crewed suborbital flights: VSS Unity (Branson, 11 July) and New Shepard (Bezos, 20 July) |
| 2023 | Virgin Galactic begins commercial service; Rocket Lab's HASTE first flight |
| 2026 | New Shepard paused after 38 flights; Virgin Galactic prepares Delta-class flights |

## Suborbital Point-to-Point Transport

Rocket-powered point-to-point travel — reaching anywhere on Earth in under an hour on a suborbital trajectory — has been proposed for passengers (SpaceX's "Earth to Earth" Starship concept) and for rapid military cargo delivery (the US Air Force/Space Force "Rocket Cargo" Vanguard programme, studying delivery of up to 100 t anywhere in about 90 minutes). A flight from New York to Shanghai would require a burnout speed of roughly 6–7 km/s, accelerations of about 3–4 g, and a re-entry comparable to an orbital vehicle. The challenges are cost per flight, noise and sonic booms near cities, safety certification, and the need for spaceports at sea or far from populated areas.

## Operations, Safety and Regulation

A sounding-rocket or suborbital launch is planned against strict **range safety** criteria. Analysts compute the impact dispersion of each stage and payload from Monte Carlo simulations including motor performance, winds and misalignments; launch is allowed only if the expected casualty risk to the public ($E_c$) is below limits such as $10^{-4}$ per mission (US FAA Part 450 and range commanders' standards). Unguided vehicles may carry a thrust termination or flight termination system. Winds are measured with balloons shortly before launch to set the launcher elevation and azimuth. Aircraft and shipping are kept clear of hazard areas by NOTAMs (notices to air missions) and navigational warnings.

Commercial suborbital vehicles in the United States are licensed by the FAA Office of Commercial Space Transportation under **14 CFR Part 450** (streamlined launch and re-entry licensing, fully in force since 2021). In Europe, national laws (France, the UK, Norway, Sweden) govern sounding-rocket ranges, and EASA is developing a framework for suborbital vehicles that take off and land like aircraft.

::: warning
**Failure lesson — NS-23 (September 2022)**

On its 23rd flight, an uncrewed New Shepard mission carrying research payloads, the booster suffered a thermal-structural failure of its engine nozzle about one minute after lift-off. The capsule's escape system fired automatically and carried it safely to a parachute landing; the booster was destroyed on impact. The investigation led to a redesign of the nozzle and operating changes, and flights resumed in December 2023. The event demonstrated the value of a capsule escape system — the same principle protects crews on Soyuz, Crew Dragon, Orion and Shenzhou.
:::

::: key
**Key takeaways**

- Suborbital flights reach space without orbital speed; weightless time scales roughly with the square root of the height above 100 km (≈ 3 min at 105 km, ≈ 6 min at 260 km, ≈ 13 min at 700 km).
- Sounding rockets, flown since 1946, remain unique for in-situ study of the 50–150 km region, auroral physics, solar and astrophysical observations, technology tests and training; NASA flies about 20 per year.
- Microgravity platforms range from drop towers (seconds) to sounding rockets (minutes) to orbital stations (months), each trading duration, quality and cost.
- Commercial crewed suborbital flights began in 2021; New Shepard flew 98 people before pausing in 2026, and Virgin Galactic plans to resume with its Delta class in late 2026–2027.
- Suborbital trajectories are also used for hypersonic and re-entry testing; range safety, wind weighting and impact-dispersion analysis are central to all operations.
:::
