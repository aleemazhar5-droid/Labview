---
title: Crewed Spacecraft
hero: ch31
abstract: A crewed spacecraft is a small, self-contained world that must keep people alive, carry them away from an exploding rocket within seconds, and bring them home through a fireball at up to 11 km/s. This chapter traces the vehicles that have carried people since 1961 — from Vostok and Mercury through Apollo, Soyuz and the Space Shuttle to Shenzhou, Crew Dragon, Starliner and Orion, which carried four astronauts around the Moon in April 2026 — and the vehicles now being built in India and China and for lunar landings. It explains how they are engineered: pressure vessels, windows, seats and acceleration limits, avionics, propulsion, docking systems, launch abort, entry and parachutes, and how their safety is estimated, demonstrated and certified.
---

A **crewed spacecraft** carries people into space and back. Unlike a robotic spacecraft, its payload cannot be replaced and tolerates only a narrow range of pressure, temperature, acceleration and air composition. Three requirements set it apart: it must keep its crew alive (life support, Chapter 30), it must be able to escape from a failing launch vehicle at any moment of the ascent, and it must bring its crew back to Earth gently enough for them to walk away.

Since Yuri Gagarin's flight in April 1961, fewer than twenty types of vehicle have carried people into space, and only four were in service in October 2026: Russia's Soyuz, China's Shenzhou, SpaceX's Crew Dragon and NASA's Orion. Boeing's Starliner was grounded after its troubled first crewed flight, and India's Gaganyaan and China's Mengzhou were preparing for their first orbital flights. This chapter describes these vehicles and the engineering behind them; space stations are covered in Chapter 32, spacesuits in Chapter 33 and launch vehicles in Chapters 34 and 36.

## Sixty-Five Years of Crewed Spacecraft

@fig:crewtimeline shows every orbital crewed spacecraft and how long it served, and @tbl:crewvehicles compares them. Two waves stand out: the 1960s race to the Moon, and a second wave from 2020 driven by commercial contracts and by China.

![Crewed spacecraft from 1961 to 2026 and those planned for the late 2020s. The numbers give the crewed launches of each type. Soyuz has flown for almost sixty years; the Space Shuttle flew 135 times in 30 years.](figures/out/ch31_timeline.svg){#fig:crewtimeline width=98%}

### The First Generation: Vostok, Mercury, Voskhod and Gemini

The Soviet **Vostok** was a 2.3 m sphere, which needed no attitude control during its ballistic 8–9 g entry. It landed too hard for safety, so the cosmonaut ejected at about 7 km and came down under a separate parachute. Six Vostoks flew in 1961–63, carrying Gagarin and Valentina Tereshkova, the first woman in space.

NASA's **Mercury** capsule weighed only about 1.4 t so that it could ride the Redstone and Atlas missiles of the day. It set the pattern of every American capsule since: a cone with a broad, blunt heat shield at the base (Chapter 10), and a crew lying on contoured couches facing it. Mercury flew twice suborbitally in 1961, starting with Alan Shepard on 5 May, and four times in orbit from John Glenn's flight on 20 February 1962.

**Voskhod**, a Vostok without its ejection seat — and so without any means of escape early in the ascent — carried three cosmonauts in 1964 and two in 1965, when Alexei Leonov made the first spacewalk. **Gemini** carried two astronauts and was the first spacecraft built to be *flown*: thrusters, an onboard computer and radar let it change orbit, rendezvous and dock. Between March 1965 and November 1966 ten Gemini crews demonstrated the techniques Apollo needed — rendezvous (@fig:geminirdv), docking, spacewalks, fuel-cell power, guided lifting entry and flights of up to 14 days.

![Gemini 7 photographed from Gemini 6A during the first space rendezvous, 15 December 1965, with the two spacecraft about 11 m apart. The white section is the adapter module carrying propellant, fuel cells and radiators.](figures/photos/ch31_gemini.jpg){#fig:geminirdv width=42%}

### Apollo: The Command, Service and Lunar Modules

Apollo divided a lunar mission between three modules. The **command module (CM)**, a 3.9 m cone of 5.6 t, carried three astronauts and alone returned. The **service module** carried fuel cells, oxygen tanks, radiators and a single 91 kN engine, which had to work to bring the crew home from lunar orbit and was therefore pressure-fed, with redundant valves. The **Lunar Module (LM)**, the first spacecraft designed to fly only in vacuum, had a descent stage with a throttleable engine and an ascent stage that carried two astronauts back to the CM in lunar orbit (@fig:lmascent; landing is described in Chapter 27).

![The ascent stage of Apollo 11's Lunar Module Eagle returns from the surface to rendezvous with the command module Columbia in lunar orbit, July 1969.](figures/photos/ch31_lmA.jpg){#fig:lmascent width=46%}

The command and service module flew 15 crewed missions: 11 Apollo flights from 1968 to 1972, three Skylab crews and the Apollo–Soyuz Test Project of 1975. When an oxygen tank in Apollo 13's service module exploded in April 1970, the crew survived for almost four days in the Lunar Module, using it as a lifeboat.

### Soyuz and the Space Shuttle

**Soyuz**, first flown with a crew in April 1967, is the longest-serving crewed spacecraft. A spherical **orbital module** serves as living space and airlock, the crew launch and land in the bell-shaped **descent module**, and an unpressurised **service module** carries the engine, solar arrays and radiators. Only the 2.2 m descent module returns, which keeps the whole spacecraft to about 7 t. Two early accidents (Soyuz 1 and Soyuz 11, @tbl:crewaccidents) killed four cosmonauts. Upgraded through the T, TM, TMA and MS versions, Soyuz had made about 155 crewed launches by October 2026, the latest, Soyuz MS-29, on 14 July 2026.

The **Space Shuttle** (1981–2011) was a reusable winged orbiter carrying up to eight people and a 24 t payload and landing on a runway. Its two-deck crew module had a pressurised volume of about 66 m³, six times that of the Apollo command module. The Shuttle flew 135 times, assembled most of the International Space Station (ISS) and serviced Hubble five times, but two orbiters and 14 astronauts were lost (Chapter 10).

### Shenzhou and China's Programme

China's **Shenzhou** follows the Soyuz layout but is larger, with a 2.5 m descent module, and on its early flights the orbital module stayed in orbit as a satellite after the crew returned. Yang Liwei made China's first spaceflight on Shenzhou 5 on 15 October 2003, and since 2021 Shenzhou has ferried crews of three to the Tiangong space station, usually for six months.

Shenzhou also showed why a station needs a spare lifeboat. In November 2025, shortly before its crew was due home, a crack — probably from the impact of a debris particle smaller than a millimetre — was found in a window of Shenzhou-20. The crew returned in the newer Shenzhou-21 instead, so China launched an uncrewed **Shenzhou-22** from its standby rocket on 25 November to give the Shenzhou-21 crew a ride home; they landed in it on 29 May 2026 after a Chinese-record 210 days. Russia had met the same problem in December 2022, when a coolant leak attributed to a micrometeoroid emptied the radiator loop of Soyuz MS-22 and an uncrewed Soyuz MS-23 was sent as a replacement.

### The Commercial Era: Crew Dragon and Starliner

After the Shuttle retired, the United States relied on Soyuz for nine years while NASA's **Commercial Crew Program** paid two companies to develop vehicles that they own and operate under fixed-price contracts. SpaceX's **Crew Dragon** launched Doug Hurley and Bob Behnken to the ISS on 30 May 2020. By October 2026 Dragon had flown 21 crewed missions — the Demo-2 test flight, 13 NASA crew rotations, four private Axiom missions to the ISS and three free-flying private missions, including Polaris Dawn's spacewalk in 2024 and Fram2's polar orbit in 2025 — and in January 2026 it made the first medical evacuation from the ISS, bringing the Crew-11 astronauts home early. Five capsules are in service; Endeavour has flown six times.

Boeing's **CST-100 Starliner** has struggled. Its first uncrewed test in 2019 failed to reach the ISS because of software errors, and the second succeeded in 2022. On the **Crew Flight Test**, launched on 5 June 2024 with Butch Wilmore and Suni Williams, five of the 28 small thrusters on the service module failed during the approach to the ISS and helium leaks appeared in the propulsion system (@fig:starlinercft). The thrusters, packed in enclosed "doghouse" pods, had overheated during repeated firings, deforming the Teflon seals in their valves. NASA brought Starliner home uncrewed in September 2024 — it landed safely — and returned its crew on a Crew Dragon in March 2025, after 286 days in space instead of eight. In February 2026 NASA reclassified the flight as a Type A mishap, its most serious category. As of October 2026, an uncrewed cargo flight, **Starliner-1**, with new thruster valves and seals was planned for December 2026–January 2027, and the first crew rotation flight for 2028.

![Boeing's Starliner approaching the ISS on 6 June 2024 during the Crew Flight Test, with Butch Wilmore and Suni Williams aboard. Thruster failures during this approach led NASA to return the spacecraft without its crew.](figures/photos/ch31_starliner.jpg){#fig:starlinercft width=52%}

### Orion and Artemis II

NASA's **Orion** is the first new deep-space crew vehicle since Apollo. Its 5.0 m crew module, built by Lockheed Martin, carries four astronauts for up to 21 days; the **European Service Module**, built by Airbus for ESA, provides propulsion, about 11 kW from four solar wings and life-support consumables. After the uncrewed Artemis I flight around the Moon in 2022, **Artemis II** was launched on 1 April 2026 by the Space Launch System. Reid Wiseman, Victor Glover, Christina Koch and the Canadian Jeremy Hansen flew Orion *Integrity* on a free-return trajectory around the Moon (@fig:orionselfie), passing about 6 500 km above the far side and reaching 406 771 km from Earth — farther than any humans before them — before splashing down off San Diego on 10 April after an entry at about 11 km/s. Problems were minor, such as a frozen urine vent line.

![Orion photographed itself with a camera on a solar array wing on the second day of Artemis II, 3 April 2026. The crew module, with its windows, sits on the European Service Module.](figures/photos/ch31_orionselfie.jpg){#fig:orionselfie width=50%}

### Coming Next: Gaganyaan, Mengzhou and the Lunar Landers

India's **Gaganyaan** is a three-person spacecraft of about 8 t (crew module plus service module), launched by the human-rated LVM3, for flights of up to seven days at about 400 km. As of October 2026 the first uncrewed orbital flight, G1, carrying the humanoid robot Vyommitra, had not flown; ISRO aimed for the end of 2026, though mid-2026 reports pointed to 2027, and a crewed flight was not expected before 2027–28.

China's **Mengzhou** is a reusable successor to Shenzhou for Earth orbit (up to seven crew) and the Moon (three crew). After abort tests in 2025 and 2026, its first uncrewed orbital flight is expected around 2027. For lunar missions, one Long March 10 will launch Mengzhou and another the **Lanyue** lander, which completed a landing and take-off test in August 2025 while suspended from a tower rig that simulated lunar gravity; China's goal is a crewed landing by 2030.

The Artemis lunar landers are the largest crewed spacecraft yet designed. SpaceX's **Starship HLS**, a version of the 50 m Starship upper stage with a crew cabin near the top reached by an elevator, must be refuelled in orbit by a series of tanker flights — not yet demonstrated when Starship first reached orbit in September 2026. Blue Origin's **Blue Moon MK2** is a 16 m, 45 t-class lander burning liquid hydrogen and oxygen. In 2026 NASA turned Artemis III into a crewed test in Earth orbit, no earlier than late 2027, in which Orion is to dock with one or both landers; the first landing moved to Artemis IV, no earlier than 2028.

| Vehicle | Crew | Mass (t) | Pressurised volume (m³) | Launcher | Landing | First crewed flight; status |
|------------------|-----|----------|----------|------------|------------|----------------|
| Vostok (USSR) | 1 | 4.7 | — | Vostok | Land; crew ejects | 1961; retired 1963 |
| Mercury (USA) | 1 | 1.4 | 2.8 | Redstone, Atlas | Water | 1961; retired 1963 |
| Gemini (USA) | 2 | 3.2–3.8 | ≈ 2.3 | Titan II | Water | 1965; retired 1966 |
| Apollo CSM (USA) | 3 | 28.8 (CM 5.6) | 10.4 | Saturn IB, V | Water | 1968; retired 1975 |
| Apollo LM (USA) | 2 | 15–16 | 6.7 | Saturn V | Moon | 1969; retired 1972 |
| Soyuz MS (Russia) | 3 | 7.1 | 8.5 (two modules) | Soyuz-2.1a | Land, retro-rockets | 1967; flying |
| Space Shuttle (USA) | 7–8 | ≈ 110 (orbiter) | 66 | Shuttle stack | Runway | 1981; retired 2011 |
| Shenzhou (China) | 3 | 7.8 | 14 (two modules) | Long March 2F | Land, retro-rockets | 2003; flying |
| Crew Dragon (USA) | 4 | ≈ 12.5 | 9.3 | Falcon 9 | Water | 2020; flying |
| Starliner (USA) | 4 | ≈ 13 | 11 | Atlas V | Land, airbags | 2024; grounded |
| Orion (USA, Europe) | 4 | 26.5 (with ESM) | 19.6 | SLS | Water | 2026; next flight 2027 |
| Gaganyaan (India) | 3 | ≈ 8.2 | — | LVM3 | Water | Uncrewed G1 pending |
| Mengzhou (China) | 3–7 | 14 (LEO), 21.6 (Moon) | 13 | Long March 10A, 10 | Land, airbags | Uncrewed flight ≈ 2027 |

: Crewed spacecraft compared (status in October 2026). Masses at launch without escape systems; free, habitable volume is roughly half the pressurised volume (5.9 m³ in the Apollo CM, 8.9 m³ in Orion). {#tbl:crewvehicles}

## Anatomy of a Crewed Spacecraft

Most crewed spacecraft are **capsules** with a three-part layout (@fig:capsuleanatomy). The **crew module**, the only part that returns, is a pressure vessel wrapped in a heat shield and thermal protection, containing the crew, the controls and the parachutes. The **service module** carries everything not needed for entry — main engine and most of the propellant, solar arrays, radiators and consumables — and burns up in the atmosphere. The **launch abort system** sits on top for the first minutes of flight.

![Anatomy of a capsule stack, based on Orion's layout. Only the crew module returns to Earth; the service module provides propulsion, power and heat rejection during the mission, and the abort system protects the crew during ascent.](figures/out/ch31_anatomy.svg){#fig:capsuleanatomy width=88%}

### Pressure Vessel and Atmosphere

The heart of the crew module is the **pressure vessel**, usually welded from aluminium or aluminium–lithium alloy. At sea-level pressure (101 kPa) every square metre of wall carries about 10 t, so the vessel is built from cones, cylinders and domes that carry pressure efficiently as tension (Chapter 5). It is designed for 1.5–2 times its operating pressure, proof-tested, and shielded from debris by the heat shield and backshell around it.

The cabin atmosphere has large consequences. Mercury, Gemini and Apollo flew pure oxygen at about 34–38 kPa, which kept the structure light. But on 27 January 1967 a fire in the Apollo 1 command module, filled with pure oxygen above sea-level pressure for a ground test, killed its three astronauts, whose inward-opening hatch could not be opened against the cabin pressure. Apollo was redesigned with a quick-opening hatch, non-flammable materials and a nitrogen–oxygen mixture on the pad. Soyuz, the Shuttle, Shenzhou, Dragon and Orion all fly an Earth-like nitrogen–oxygen atmosphere at about 101 kPa, maintained by the systems described in Chapter 30.

### Windows

Windows are weak points in the pressure shell, but crews need them for docking and for seeing the horizon. They are typically stacked as three panes: an outer pane of fused silica that takes entry heating and debris impacts, and two inner pressure panes, either of which can hold cabin pressure on its own. Because glass fails by the slow growth of tiny flaws, windows have large safety factors. The crack in Shenzhou-20's window ran right through the outer, protective pane, but the two pressure panes behind it held — exactly what the redundancy is for.

### Seats and Acceleration Limits

Capsule crews sit in contoured seats facing the heat shield, because the body tolerates acceleration very differently along its three axes (@fig:gtolerance). In the **eyeballs-in** direction (+Gx, chest to back) heart and brain are at the same level, so trained crews can withstand 15 g for several seconds and 4–5 g for many minutes. In the **eyeballs-down** direction (+Gz, head to foot) blood drains from the brain and, without protection, vision greys out at about 4 g. NASA's human-system standard, NASA-STD-3001, sets limits for each axis and duration, lower for crews deconditioned by months in weightlessness and higher for aborts and emergency entries.

In @fig:gtolerance (b), a lifting entry from low Earth orbit (LEO) stays inside the nominal return limit, while a ballistic backup entry, at almost 10 g, crosses it but stays within the emergency limit — which is why Soyuz and Shenzhou use ballistic entry only as a backup.

Seats spread the load over as much of the body as possible. Soyuz cosmonauts lie in individually moulded seat liners on seats that stroke on shock absorbers at touchdown; Dragon's four carbon-fibre seats sit side by side beneath the display panel (@fig:dragonseats).

![Human tolerance of sustained acceleration. (a) NASA-STD-3001 limits for four directions: eyeballs-in is by far the most tolerable. (b) Eyeballs-in limits compared with the time spent above each acceleration level in the simulated entries of @fig:capsuleentry, and with the 1983 Soyuz T-10-1 pad abort.](figures/out/ch31_gtol.svg){#fig:gtolerance width=96%}

![The NASA SpaceX Crew-10 astronauts in their seats inside a Dragon capsule during a pre-flight equipment test at Kennedy Space Center, February 2025. The commander and pilot take the two central seats, facing the touchscreen display panel (out of view).](figures/photos/ch31_ceit2.jpg){#fig:dragonseats width=48%}

### Displays and Avionics

**Avionics** — the guidance, navigation and control computers, sensors and displays — show the largest generational change. The Apollo Guidance Computer had 2 048 words of erasable memory and was operated through a numeric keypad. The Shuttle had five computers, four running identical software and a fifth independently written backup software. Dragon's crew fly with three large touchscreens and a row of physical buttons for critical actions such as an emergency deorbit, parachute deployment or fire suppression, and the vehicle normally rendezvouses and docks on its own. Orion uses airliner-derived flight computers with independent backup flight software, and its crew demonstrated manual piloting on Artemis II.

The governing principle is **fault tolerance**: no single failure — and for many functions no two — may cause loss of the crew. It is achieved with redundant, physically separated strings of equipment, voting computers that outvote a faulty member, dissimilar backups that cannot share a software error, and manual control of critical functions.

### Propulsion, Power and Thermal Control

Crewed spacecraft carry a **main engine** for large manoeuvres (Orion's service module uses a refurbished 27 kN Space Shuttle orbital manoeuvring engine), **reaction-control thrusters** for attitude control and docking and, in pusher designs, **abort engines**. Almost all burn storable **hypergolic** propellants, which ignite on contact and can wait for months in orbit (Chapter 35). Dragon has 16 Draco thrusters of 400 N and 8 SuperDraco abort engines of about 71 kN, all fed from the same tanks. Thrusters are a recurring source of trouble: on Gemini 8 in 1966 a stuck thruster spun the spacecraft at about one revolution per second until Neil Armstrong regained control, and Starliner's 2024 failures came from heat building up during long series of pulses — so qualification tests must reproduce realistic firing sequences.

Gemini and Apollo introduced **fuel cells**, which combine hydrogen and oxygen to make electricity — on Apollo and the Shuttle also the crew's drinking water. Today's vehicles use **solar arrays** with batteries for eclipses and entry. Crew and electronics produce hundreds of watts to several kilowatts of heat, carried by pumped fluid loops to **radiators** on the service module or, on Dragon, the trunk (Chapter 5). The Soyuz MS-22 leak showed how exposed these external loops are.

### Docking Systems

Docking joins two spacecraft so that crews can move between them through a pressurised tunnel. Early systems used a **probe** on the active vehicle and a cone-shaped **drogue** on the passive one, as Soyuz and the Russian ISS segment still do. **Androgynous** systems, with identical rings on both sides, let any two vehicles dock and leave the passage clear without removing a probe, and the International Docking System Standard (IDSS) of 2010 defines a common interface for vehicles of different agencies and companies (@tbl:dockingsys). Modern systems first make a **soft capture**, with latches on a compliant, actuator-controlled ring absorbing the contact energy at closing speeds of about 0.1 m/s or less, then a **hard capture**, in which hooks pull the structures together and seal them.

| System | Type | Used by | Notes |
|---|---|---|---|
| Apollo probe and drogue | Probe on CSM, drogue on LM | Apollo, Skylab | Removed to open the tunnel |
| SSVP | Probe and drogue | Soyuz, Progress, Russian ISS modules | In use since 1971; 0.8 m hatch |
| APAS-75 / -89 / -95 | Androgynous, peripheral | Apollo–Soyuz, Mir, Shuttle | Shuttle docked to Mir and ISS |
| Chinese mechanism | APAS-derived | Shenzhou, Tianzhou, Tiangong | Automated 2011, manual 2012 |
| IDSS (NDS, SpaceX system) | Androgynous, low-impact | Dragon, Starliner, Orion; ISS adapters | Common standard; 0.8 m passage |

: Docking systems for crewed spacecraft. {#tbl:dockingsys}

## Launch Abort

### Why Crews Need to Escape

A launch vehicle is a controlled explosion of hundreds of tonnes of propellant. If it fails, the crew may have only seconds before blast overpressure, a fireball, flying fragments or, at altitude, aerodynamic forces reach them. The **launch abort system** must detect the failure, carry the crew module far enough away fast enough, stabilise it and hand it over to the normal parachute landing.

Vostok and Gemini used **ejection seats**, which work only at low altitude and speed. When Gemini 6A's engines shut down 1.2 s after ignition on 12 December 1965, Wally Schirra judged that the rocket had not lifted off and chose not to eject — saving the mission and avoiding a risky ejection from a pure-oxygen cabin. Apollo and almost every crewed vehicle since — the Space Shuttle being the main exception — instead remove the whole crew module from the rocket.

### Towers and Pushers

There are two ways to do this (@fig:abortsystems). A **tower**, or tractor, system mounts solid rocket motors above the capsule, with nozzles canted outwards so that the plumes clear it; it *pulls* the capsule away with a short, violent burn and is jettisoned once the rocket is high enough. Mercury, Apollo, Soyuz, Shenzhou, Orion, Gaganyaan and Mengzhou use towers. A **pusher** system builds liquid-propellant engines into the capsule or service module, like Dragon's SuperDracos and Starliner's four 178 kN RS-88 engines, and *pushes* it away.

![Launch escape systems. (a) A tower pulls the capsule away; (b) a pusher uses engines built into the capsule or service module. (c) Typical trade-offs between them.](figures/out/ch31_abort.svg){#fig:abortsystems width=94%}

Towers give very high thrust for their mass from simple solid motors, but they are dead weight after jettison and are discarded on every flight. Pushers are available all the way to orbit, and their propellant can be used for manoeuvring, but they carry tonnes of toxic propellant next to the crew for the whole mission and give a slower escape.

### Abort Modes

The abort method changes as the rocket climbs. On the pad, the escape motor must lift the capsule high enough to open its parachutes; through **maximum dynamic pressure** (max-Q) it must also overcome drag. After the tower is jettisoned, two to three minutes after launch, the capsule separates with its own engines (on Soyuz, with motors on the payload fairing) and makes a ballistic or lifting entry downrange. Close to orbital speed, it may be better to continue to a lower orbit (**abort to orbit**).

### Aborts in Flight

@tbl:crewaborts lists the aborts that occurred during crewed launches or, for Soyuz T-10-1, with the crew aboard on the pad; every crew survived. (The Shuttle also had five engine shutdowns on the pad, which needed no escape.) The two Soyuz in-flight aborts showed that the backup motors and ballistic entry worked — at the cost of high accelerations.

| Flight | Date | Phase | What happened | Outcome |
|--------|-------|--------|------------------------|-------------|
| Soyuz 18a | 5 Apr 1975 | Staging | Stages failed to separate; steep entry from 192 km at about 21 g | Crew injured; landed in the Altai mountains |
| Soyuz T-10-1 | 26 Sep 1983 | On the pad | Booster fire; tower fired seconds before the explosion; 14–17 g for 5 s | Crew unhurt; landed 4 km away |
| STS-51F | 29 Jul 1985 | Ascent, 5 min 45 s | Main engine shut down by faulty sensors | Abort to orbit; mission completed |
| Soyuz MS-10 | 11 Oct 2018 | Booster separation, ≈ 2 min | Strap-on struck the core (sensor pin deformed in assembly); fairing motors pulled the spacecraft clear; ballistic entry at 6–7 g | Crew landed 19 min 41 s after launch |

: Launch aborts with crews aboard. {#tbl:crewaborts}

### Abort Tests and Abort Sizing

Abort systems are proven with uncrewed test flights. Orion's Pad Abort-1 in May 2010 accelerated a test capsule to about 200 m/s (445 mph) in three seconds, and Ascent Abort-2 in July 2019 fired the abort motor at about 9.5 km and Mach 1.1 (@fig:aa2launch). SpaceX tested Dragon from the pad in 2015 and, in January 2020, near max-Q from a Falcon 9 whose engines were shut down at the abort command. Starliner's pad abort test in November 2019 succeeded although one of three main parachutes failed because of an improperly connected link (@fig:starlinerpat). India tested Gaganyaan's system in flight in 2023, and China tested Mengzhou in 2025 and 2026.

::: figrow
![Orion's Ascent Abort-2 test lifts off from Cape Canaveral on 2 July 2019. Less than a minute later the abort motor fired at about 9.5 km altitude, pulling the test crew module off the booster.](figures/photos/ch31_aa2D.jpg){#fig:aa2launch width=72%}

![Starliner's pad abort test at White Sands, 4 November 2019: four abort engines and several manoeuvring thrusters push the spacecraft off the stand with a combined thrust of about 710 kN.](figures/photos/ch31_spaA.jpg){#fig:starlinerpat}
:::

How much thrust is needed? That depends on how far the crew module must get from the booster, and how quickly; @fig:abortsep simulates both types of system.

![Simulated separation after an abort. (a) Distance from the booster for a tower and a pusher, from the pad and at maximum dynamic pressure. If the booster keeps thrusting, even a tower struggles to escape. (b) The acceleration the crew feels: at max-Q, drag first reduces the net push and then decelerates the capsule once the motor burns out.](figures/out/ch31_abortsim.svg){#fig:abortsep width=98%}

::: example
**Example: sizing an abort motor**

Suppose the crew module must be 300 m from the booster within 3 s of the abort command, and the abort vehicle (crew module plus tower) has a mass of 16 t.

1. Required relative acceleration: $a_{rel} = 2s/t^2 = 2 × 300 / 3^2$ = 66.7 m/s² (6.8 g).
2. **Pad abort.** The booster stands still and the capsule climbs against gravity: $T/W = (a_{rel} + g)/g$ = **7.8**, a thrust of 1.22 MN.
3. **Max-Q, booster shut down.** At 420 m/s and 11 km (ρ = 0.356 kg/m³), $q = \tfrac12\rho v^2$ = 31 kPa. With $C_D A$ = 0.8 × 19.6 = 15.7 m², the drag is 0.49 MN (3.1 g). Gravity acts equally on capsule and booster and cancels in their relative motion: $T = m\,a_{rel} + D$ = 1.07 + 0.49 = 1.55 MN, **T/W = 9.9**.
4. **Max-Q, booster still thrusting** at 1.5 g: $T = m(a_{rel} + 1.5g) + D$ = 1.79 MN, **T/W = 11.4** — close to the 1.8 MN (400 000 lbf) of Orion's abort motor.
5. A Dragon-class pusher (8 × 71 kN on 12.5 t, T/W = 4.6) needs about 4.1 s to open 300 m from the pad and 5.3 s at max-Q (@fig:abortsep), so pushers depend on shutting the booster's engines down the instant an abort begins. A solid booster cannot be shut down, which favours towers on rockets with solid first stages.
:::

## Coming Home: Entry, Descent and Landing

### Capsule Shapes and Lift

A capsule returning from orbit must dissipate about 30 MJ of kinetic energy per kilogram, and from the Moon about 60 MJ (Chapter 10). Placing the centre of mass slightly off the axis makes the capsule fly at an angle of attack of 15–25° and produce a **lift-to-drag ratio** (L/D) of 0.25–0.4 — about 0.37 for Apollo and 0.25–0.3 for Soyuz, Shenzhou and Orion. By rolling to point this lift up, down or sideways (**bank-angle modulation**), the guidance controls both deceleration and landing point; Artemis II splashed down 0.95 km from its predicted point. A broad cone like Orion's has a low **ballistic coefficient** $\beta = m/(C_D A)$, so it decelerates high in thin air, but it must stay stable from hypersonic to subsonic speeds and carries uprighting bags in case it floats apex-down.

### Ballistic, Lifting and Skip Entries

@fig:capsuleentry compares four ways of coming home. A **lifting entry from LEO** (Soyuz-like, at 7.6 km/s and −1.35°) peaks at 3.8 g. The **ballistic backup** of the same capsule — flown when the guidance fails, the capsule spinning slowly to cancel its lift — peaks near 10 g in the model, compared with the roughly 8 g reported on the ballistic Soyuz entries of 2007 and 2008. Returning from the Moon at 11 km/s, a capsule must enter more steeply (about −6°) so as not to skip out; with lift and guidance the model peaks at 4.5 g. A **skip entry** dips into the atmosphere, climbs back to about 100 km and enters again, roughly doubling the downrange distance so that the capsule can reach a fixed landing zone from a wider range of return trajectories.

![Simulated capsule entries. (a) Trajectories; (b) deceleration; (c) convective heat flux at the stagnation point; (d) total heat absorbed per unit area. Lift cuts the peak load from about 10 g to about 4 g; a lunar return raises the peak heating, and a skip entry splits it into two pulses and increases the total heat load.](figures/out/ch31_entry.svg){#fig:capsuleentry width=98%}

::: example
**Example: why lunar return needs lift**

The Allen–Eggers formula (Chapter 10) gives the peak deceleration of a ballistic body entering on a straight path at speed $V_E$ and angle $\gamma_E$, with scale height $H$ = 7.2 km:

$$n_{max} = \frac{V_E^2 \sin|\gamma_E|}{2\,e\,H\,g_0}$$

1. **LEO return**, 7.6 km/s at −1.35°: $n_{max}$ = 7 600² × 0.0236 / (2 × 2.718 × 7 200 × 9.81) = **3.5 g**.
2. **Lunar return**, 11.0 km/s at −6.0°: $n_{max}$ = 11 000² × 0.105 / 383 900 = **33 g** — a factor (11.0/7.6)² = 2.1 from speed and 4.4 from the steeper angle.
3. **Simulation** (@fig:capsuleentry). The LEO ballistic case actually peaks at 9.9 g: on such a shallow path gravity bends the trajectory down, steepening it to about −5.5° by the time of peak deceleration. The lunar ballistic case at −6.0° peaks at 9.7 g, because above orbital speed the curving path lifts the capsule — but entering just 0.5° steeper raises it to 15.5 g.
4. **Lesson.** The formula shows the scaling — deceleration grows with the square of speed and the steepness of entry — but real entries must be integrated numerically. A lunar-return capsule is so sensitive to its entry angle that it needs lift and closed-loop guidance; with L/D = 0.27 the simulated peak falls to 4.5 g.
:::

### Heat Shields

A crewed heat shield cannot be tested at full scale before flight. Nearly all capsules use **ablators**, which char and erode, carrying heat away in the gases they release (Chapter 10). Apollo's **Avcoat**, an epoxy-novolac resin with silica fibres filling a fibreglass honeycomb, was revived for Orion, whose 5 m shield is made of 186 bonded blocks. Dragon uses SpaceX's **PICA-X**, a low-density carbon–phenolic ablator derived from NASA's PICA. Soyuz and Shenzhou jettison their heat shields shortly before landing.

After **Artemis I**, engineers found that charred Avcoat had broken away from more than a hundred places on Orion's heat shield. NASA traced the cause to the skip entry: as the heating fell between the two pulses — the dip in @fig:capsuleentry (c) — the Avcoat kept generating gas inside but formed permeable char too slowly to let it escape, so pressure built up and cracked off pieces of char. Rather than replace the Artemis II shield, NASA flew a modified entry with a shorter maximum downrange distance, reducing the time spent in the troublesome heating regime. Artemis II's shield, whose surface exceeded 2 200 °C, showed only nine spots of char loss against 103, and the Artemis III shield uses Avcoat of more uniform permeability.

### Parachutes

Below about 10 km a capsule falls at 100–200 m/s, and parachutes take over in stages that keep opening loads within the strength of the structure and the tolerance of the crew. Pilot parachutes or mortars deploy **drogues**, which stabilise the capsule and slow it to 50–90 m/s; the drogues then pull out the **mains**, whose **reefing** lines hold each canopy partly closed until pyrotechnic cutters release them a few seconds later (@fig:parachutesizing b). Redundancy is essential: Apollo 15 landed safely in 1971 although one of its three mains collapsed, and modern systems are designed to land safely with one main failed. Soyuz has a single large main parachute and a complete reserve.

![Parachute design. (a) Sea-level descent speed versus main-canopy diameter for a 9.3 t capsule with one to four mains; Orion's three 35 m mains give about 8 m/s, and about 10 m/s with one failed. (b) A simulated descent: drogues at 7 km, reefed mains at 2.6 km, full mains below 1.5 km.](figures/out/ch31_chutes.svg){#fig:parachutesizing width=98%}

At terminal velocity, drag equals weight, so the descent speed is $v = \sqrt{2mg/(\rho C_D S)}$ for total canopy area $S$: halving the landing speed needs four times as much parachute.

::: example
**Example: sizing the main parachutes**

A 9.3 t crew module must splash down at no more than 10 m/s at sea level (ρ = 1.225 kg/m³) even if one of its three mains fails. Ringsail canopies have $C_D$ ≈ 0.80 on their nominal area, and two canopies in a cluster lose about 5 % of their drag through interference.

1. Drag area needed: $S = 2mg/(\rho v^2 C_D)$ = 2 × 9 300 × 9.81 / (1.225 × 10² × 0.80) = 1 860 m².
2. Two working canopies: each needs 1 860 / (2 × 0.95) = 980 m², a nominal diameter $D_0 = \sqrt{4 × 980/\pi}$ = **35.3 m** — the size of Orion's mains.
3. With all three open (cluster efficiency 0.92), $v$ = **8.3 m/s** (19 mph), and the capsule meets the water with about 320 kJ of kinetic energy.
4. **Why reef?** The mains open at 2.6 km (ρ = 0.94 kg/m³) and about 57 m/s, where $q$ = 1.55 kPa. Opened fully at once, three canopies would decelerate the capsule at about 36 g; reefed to 6 % of their area, about 2 g. The peak in the simulated sequence is 3.9 g.
:::

### Water or Land?

Water landings are gentle but need ships and divers, and seawater makes reuse harder. American capsules from Mercury to Orion have splashed down (@fig:a2chutes); since mid-2025 Dragon has usually returned to the Pacific off California, where its trunk, jettisoned after the deorbit burn, falls into the ocean.

![Orion Integrity descends under its three main parachutes before splashdown in the Pacific off San Diego on 10 April 2026, ending Artemis II.](figures/photos/ch31_a2splash.jpg){#fig:a2chutes width=36%}

Landing on land makes recovery and reuse easier but needs a soft touchdown. Soyuz and Shenzhou fire **soft-landing rockets**, six small solid motors triggered by a gamma-ray altimeter about a metre above the ground, which cut the speed from about 7 m/s to about 1.5 m/s (@fig:soyuzlanding). Starliner inflates six **airbags** beneath its jettisoned heat shield and lands at White Sands, New Mexico; Mengzhou will also use airbags (@tbl:landingsystems).

![Soyuz MS-08 lands near Zhezkazgan, Kazakhstan, on 4 October 2018. The flash beneath the descent module is the soft-landing rockets firing just before touchdown.](figures/photos/ch31_soyuzC.jpg){#fig:soyuzlanding width=44%}

| Vehicle | Drogues | Mains | Speed under mains | Final attenuation |
|---|---|---|---|---|
| Apollo CM | 2 × 5.0 m | 3 × 25.5 m ringsail | ≈ 10 m/s (22 mph) | Water |
| Soyuz | 1 (≈ 24 m²) after pilots | 1 × ≈ 1 000 m², plus reserve | ≈ 7 m/s | Soft-landing rockets → ≈ 1.5 m/s |
| Crew Dragon | 2, at ≈ 5.5 km | 4, at ≈ 1.8 km | ≈ 7 m/s (15–16 mph) | Water |
| Starliner | 2 | 3 | — | Six airbags, on land |
| Orion | 2 × 7 m | 3 × 35 m ringsail | < 9 m/s (< 20 mph) | Water |

: Descent and landing systems of capsules. {#tbl:landingsystems}

At sea, Dragon's recovery ship lifts the capsule onto its deck within about an hour, and the crew are helped out while their balance readjusts to gravity (@fig:dragonrecovery); the Artemis II crew instead stepped onto a raft and were flown to their ship by helicopter. The winged alternative — the Shuttle's runway landing after a gliding entry with up to 2 000 km of cross-range — gave the gentlest deceleration of all, at the cost of carrying wings, landing gear and a fragile thermal protection system to orbit and back (Chapter 10).

![The recovery team opens the hatch of Dragon Endeavour on the SpaceX recovery ship after the Crew-11 splashdown off California on 15 January 2026. The discolouration is from entry heating.](figures/photos/ch31_dsplash.jpg){#fig:dragonrecovery width=48%}

## Reliability and Safety

### What Has Gone Wrong

Four accidents in flight have killed 18 people in orbital spacecraft, and the Apollo 1 fire killed three on the ground (@tbl:crewaccidents). Each occurred where the crew could not escape: during entry and landing (Soyuz 1, Soyuz 11, Columbia), or during ascent in a vehicle without an escape system (Challenger).

| Accident | Date | Phase | Cause | Main changes afterwards |
|----------|-------|------|-------------------|--------------|
| Apollo 1 | 27 Jan 1967 | Ground test | Fire in pure oxygen; inward-opening hatch; 3 killed | N₂–O₂ on the pad, new hatch, materials control |
| Soyuz 1 | 24 Apr 1967 | Landing | Main parachute failed, reserve tangled; 1 killed | Redesigned parachutes |
| Soyuz 11 | 30 Jun 1971 | Entry | Valve opened at module separation; cabin depressurised; 3 killed | Pressure suits for launch and landing |
| Challenger (STS-51L) | 28 Jan 1986 | Ascent | Booster joint seal failed in cold weather; 7 killed | Booster redesign, bail-out system |
| Columbia (STS-107) | 1 Feb 2003 | Entry | Wing holed by foam at launch; 7 killed | In-orbit inspection; Shuttle retirement |

: Fatal accidents in orbital crewed spacecraft. {#tbl:crewaccidents}

### Estimating Risk

How safe is a spacecraft? The best answer comes from **probabilistic risk assessment (PRA)**: a model of the vehicle built from fault trees and event sequences, using failure rates from tests and experience, that estimates the probability of **loss of crew (LOC)** per flight. Investigating the Challenger accident in 1986, the physicist Richard Feynman found that NASA managers believed the chance of losing a Shuttle was about 1 in 100 000, while engineers estimated about 1 in 100. A 2011 NASA study recomputed the risk as it really was through the programme (@fig:crewsafety a): about 1 in 12 on the first flight, 1 in 10 at the time of Challenger, improving to about 1 in 90 by the end as hazards were found and fixed. The actual record — 2 losses in 135 flights, or 1 in 68 — agreed with this retrospective estimate, not with the managers' belief.

@fig:crewsafety (b) shows why flight experience alone cannot prove a vehicle safe. After $n$ flights without loss, a vehicle whose true risk is $p$ per flight would show that record with probability $(1-p)^n$; claiming with confidence $C$ that the risk is no worse than $p$ requires $n = \ln(1-C)/\ln(1-p)$ successful flights. Showing 1 in 270 at 80 % confidence needs 434 flights — more than any crewed vehicle has made. Safety must be built in by design, analysis and test.

![Measuring safety. (a) Retrospective estimates of the Space Shuttle's loss-of-crew risk at selected flights, compared with the actual loss rate. (b) The number of consecutive successful flights needed to demonstrate a risk target with a given statistical confidence.](figures/out/ch31_safety.svg){#fig:crewsafety width=98%}

### Human-Rating

NASA certifies a spacecraft for crews (**human-rating**) under NPR 8705.2, *Human-Rating Requirements for Space Systems*, together with the technical standards of NASA-STD-3001. Among other things, the system must:

- tolerate failures, so that no single failure — and for many functions no combination of two — causes a catastrophic event;
- provide abort and crew survival capability in every phase where it is feasible;
- give the crew insight into, and manual control of, critical functions, within human limits for acceleration, noise, vibration, atmosphere and workload;
- be verified by test and analysis, including flight tests of the integrated system before crews fly.

For Commercial Crew, NASA required a loss-of-crew risk no worse than **1 in 270** over a 210-day ISS mission, with no more than 1 in 500 from ascent and entry — three to five times safer than the Shuttle at its best; in 2019 the US Government Accountability Office found that debris strikes during the long docked period dominated the risk. Starliner showed the limits of certification: thruster failures had also occurred on its 2022 uncrewed flight, but their cause was not fully understood before a crew flew.

::: ai
**AI in crewed spacecraft**

Crewed vehicles already rely on autonomy: Soviet and Russian spacecraft have docked automatically using radio systems since 1967 (Igla, then Kurs from 1986), and Crew Dragon flies its whole rendezvous and docking on its own with lidar, thermal and visible cameras while the crew monitors. Machine learning is being added cautiously, where it can be verified: vision-based pose estimation for docking and inspection; anomaly detection that compares thousands of telemetry channels with learned normal behaviour and could flag slow degradations such as Starliner's thruster heating; and crew assistants, such as the voice assistant demonstrated on Artemis I. On Mars missions, light-time delays will make onboard fault diagnosis essential. Chapters 45 and 46 discuss these applications and how they can be qualified for human spaceflight.
:::

::: key
**Key takeaways**

- In October 2026 Soyuz, Shenzhou, Crew Dragon and Orion were in service, Starliner was grounded, and Gaganyaan and Mengzhou were preparing for uncrewed test flights.
- A capsule stack has a crew module (pressure vessel, heat shield, parachutes), a service module and a launch abort system; only the crew module returns.
- Crews tolerate acceleration best eyeballs-in: about 15 g for seconds and 4–5 g for minutes. Lift (L/D ≈ 0.3) cuts entry loads from about 10 g to about 4 g and lets capsules steer to a precise landing.
- Abort systems must open hundreds of metres of separation within seconds: towers give T/W ≈ 7–13; pushers (T/W ≈ 4–6) work all the way to orbit but rely on shutting the booster down.
- Lunar return doubles the energy per kilogram and demands a precise entry angle, guided lift and robust heat shields.
- Parachute descent speed falls only with the square root of canopy area; systems are designed to land safely with one main parachute failed.
- Flight experience alone cannot demonstrate safety: the Shuttle's 1-in-68 record matched retrospective risk models, not its managers' 1-in-100 000 belief.
:::

::: questions
**Review questions**

1. Why do capsule crews lie facing the heat shield? Use @fig:gtolerance to compare +Gx and +Gz limits for 60 s.
2. List the three elements of a capsule stack and their functions. Which are reused on Crew Dragon?
3. Compare tower and pusher abort systems. Why might a rocket with a solid-fuel first stage favour a tower?
4. An abort vehicle of 10 t must open 200 m of separation from a stationary booster within 2.5 s. What thrust is required?
5. Use the Allen–Eggers formula to estimate the peak deceleration of a ballistic capsule entering at 11 km/s and −6.5°. Why is the real value lower, and why do lunar-return capsules still need lift?
6. How does a skip entry differ from a direct entry, and how did the skip lead to char loss on Orion's Artemis I heat shield?
7. A 6 t capsule must splash down at no more than 9 m/s with one of its two mains failed. What nominal canopy diameter is needed ($C_D$ = 0.8)?
8. Why do Soyuz and Shenzhou need soft-landing rockets, while Dragon and Orion do not?
9. What do the Shenzhou-20 window damage (2025) and the Soyuz MS-22 leak (2022) teach about lifeboats for space stations?
10. Why can flight experience alone not prove a crewed vehicle safe? How many successful flights would show a risk of 1 in 500 with 90 % confidence?
:::
