---
title: Spaceplanes, Atmospheric Re-entry and Reusable Vehicles
hero: ch10
abstract: Coming back from orbit is as hard as getting there. A returning spacecraft must shed the enormous kinetic energy it gained during launch - about 30 megajoules for every kilogram - as heat in the upper atmosphere, without burning up or crushing its crew. This chapter explains the physics of atmospheric entry and heating, the design of heat shields and thermal protection systems, capsules versus winged spaceplanes, the history and lessons of the Space Shuttle, Buran and the X-37B, today's reusable spaceplanes and lifting bodies, hypersonic air-breathing concepts, and the economics of reusability.
---

## The Re-entry Problem

### Energy to Dissipate

A satellite in low Earth orbit moves at about 7.8 km/s. Its kinetic energy per kilogram is

$$\frac{v^2}{2} = \frac{(7\,800)^2}{2} \approx 3.0\times10^7\ \text{J/kg} = 30\ \text{MJ/kg}$$

— about seven times the chemical energy in a kilogram of TNT, and enough to vaporise the spacecraft several times over if it were all absorbed. A vehicle returning from the Moon arrives at about 11 km/s (60 MJ/kg); a Mars sample capsule at 12–13 km/s; the Stardust comet-sample capsule entered at 12.9 km/s, the fastest human-made re-entry to date.

Re-entry works because almost all this energy goes into heating the *air*, not the vehicle. A strong **bow shock wave** forms ahead of the vehicle; the air passing through it is compressed and heated to temperatures of 6 000–11 000 K (hotter than the surface of the Sun), dissociated into atoms and partly ionised into a plasma. Most of this hot gas flows around the vehicle and is left behind. Only about 1–5 % of the energy reaches the vehicle surface — and the job of the **thermal protection system (TPS)** is to deal with that fraction.

### The Blunt-Body Insight

In 1951, H. Julian Allen and Alfred Eggers at NACA Ames made a counter-intuitive discovery: a re-entry vehicle should be **blunt**, not sharp (@fig:blunt). A blunt body creates a detached shock that stands off from the surface, so that most of the heat stays in the shock layer; a sharp body has an attached shock close to its nose and receives far more heating. The convective heat flux at the stagnation point scales approximately as

$$\dot q_{s} \approx k\,\sqrt{\frac{\rho}{r_n}}\;V^3 \qquad\text{(Sutton–Graves; } k \approx 1.74\times10^{-4}\ \text{for Earth's atmosphere in SI units)}$$

where $r_n$ is the nose radius. Larger nose radii mean lower heat flux. This insight shaped every capsule since Mercury and the rounded noses of ICBM warheads and the Space Shuttle.

![Sharp and blunt bodies at hypersonic speed. A blunt nose pushes the bow shock away from the surface so that most of the heat remains in the air.](figures/out/ch10_blunt.svg){#fig:blunt width=88%}

At speeds above about 10 km/s, the hot shock layer also emits strong **radiative heating** (from excited nitrogen and oxygen atoms and molecules), which, unlike convective heating, increases with nose radius. Lunar-return capsules such as Orion and Apollo experience significant radiative heating, and Mars-return or outer-planet probes even more.

### The Entry Corridor

A returning vehicle must enter within a narrow range of **flight-path angles** — the **entry corridor** (@fig:corridor). If it enters too shallowly, it may skip back out of the atmosphere (for a lifting vehicle) or spend too long in the heating region; if too steeply, deceleration and peak heating become excessive. For a ballistic capsule, Allen and Eggers showed that the peak deceleration depends only on the entry speed $V_E$ and angle $\gamma_E$:

$$n_{max} = \frac{V_E^2\,\sin|\gamma_E|}{2\,e\,H\,g_0}$$

where $H$ ≈ 7.2 km is the atmospheric scale height (@fig:allen). Returning from LEO at 7.8 km/s, a ballistic capsule entering at −2° experiences about 8–9 g; at −6° it would experience over 20 g. Lunar returns must be precisely targeted — Apollo's corridor was only about 2° wide.

![The entry corridor. A returning vehicle must enter steeply enough not to skip out or overheat over a long path, but shallowly enough to keep deceleration and peak heating within limits.](figures/out/ch10_corridor.svg){#fig:corridor width=86%}

![Peak deceleration of a ballistic entry vehicle as a function of entry angle and speed (Allen–Eggers result). Crews can tolerate about 8 g in the eyeballs-in direction for short periods; lifting entries reduce the load dramatically.](figures/out/ch10_allen_eggers.svg){#fig:allen width=86%}

### Lift Changes Everything

A purely ballistic entry is simple but harsh. Generating even a small amount of **lift** — by flying a capsule at an angle of attack with its centre of mass offset from the centreline — lets the vehicle stay higher where the air is thinner, spreading deceleration over a longer time. A lift-to-drag ratio of only 0.3 (Gemini, Apollo, Soyuz, Shenzhou, Crew Dragon, Orion) reduces peak deceleration from LEO from about 8 g to 3–4 g and allows the vehicle to steer by rolling its lift vector ("bank-angle modulation"), giving landing accuracy of a few kilometres. Winged vehicles with L/D ≈ 1–1.5 at hypersonic speeds (the Space Shuttle, Buran, X-37B, Dream Chaser) can keep decelerations below 1.5–2 g and glide thousands of kilometres, with cross-range capability of hundreds to 2 000 km.

@fig:entryprof compares simulated entries for four classes of vehicle.

![Simulated entries (computed for this manual) for a ballistic capsule, a lifting capsule, a winged orbiter and a lunar-return capsule: altitude–velocity profiles, deceleration and stagnation-point heat flux versus time. Lift reduces peak deceleration and heating rate but lengthens the heating pulse.](figures/out/ch10_entry_profiles.svg){#fig:entryprof width=100%}

::: example
**Worked example — reading the simulated entries**

The simulation in @fig:entryprof gives: a ballistic capsule from LEO entering at −2.0° peaks at about 9 g and 140 W/cm²; a lifting capsule (L/D = 0.3) at −1.5° peaks at about 2.6 g and 60 W/cm²; a winged orbiter flying a bank-modulated equilibrium glide peaks at about 1.3 g and 80 W/cm² but travels some 6 000 km during entry; a lunar-return capsule at 11 km/s entering at −6.2° peaks at about 6 g and 180 W/cm² (convective only — real lunar returns add radiative heating). These numbers are close to flight experience: Soyuz ballistic (backup) entries reach 8–9 g, nominal lifting entries about 4 g; Shuttle entries stayed below 1.5 g; Apollo returns peaked at 6–7 g.
:::

### Communications Blackout

The plasma around an entering vehicle reflects and absorbs radio waves, causing a **communications blackout** of several minutes (about 4 minutes for Apollo, 6 minutes for Orion on Artemis II). The Space Shuttle avoided blackout from about 1988 by transmitting upward through the plasma "wake" to TDRS relay satellites; Crew Dragon and Starship similarly maintain contact through relay links (Starship uses Starlink) for much of entry. Research continues on techniques such as magnetic "windows" in the plasma and higher frequencies.


### Beyond the Basics: Real-Gas Aerothermodynamics

At entry speeds the air behind the shock does not behave as an ideal gas. Oxygen molecules begin to dissociate above about 2 500 K and nitrogen above about 4 000 K; above about 9 000 K the gas ionises. These **real-gas effects** lower the temperature behind the shock (energy goes into breaking bonds rather than raising temperature) and change the shock stand-off distance and pressure distribution — which, for example, caused the Shuttle's body-flap deflection on its first flight to be twice the predicted value because the pitching moment had been underestimated. Because the flow moves so fast, chemical reactions may not have time to reach equilibrium (**thermochemical non-equilibrium**), and whether atoms recombine at the vehicle surface depends on the surface material's **catalytic efficiency**: non-catalytic coatings (like the Shuttle's black glass) can reduce heating substantially compared with catalytic metals.

Other important phenomena include:

- **Boundary-layer transition** — at lower altitudes the boundary layer becomes turbulent, increasing heating by a factor of 3–5. Transition is triggered by surface roughness: protruding gap fillers between Shuttle tiles were a concern after Columbia, and on STS-114 (2005) astronaut Steve Robinson pulled out two protruding fillers during an unprecedented spacewalk under the orbiter.
- **Shock–shock and shock–boundary-layer interactions** — where one shock impinges on another surface (e.g., a wing leading edge behind the bow shock), local heating can be many times higher. The X-15 suffered severe burn-through on a pylon during a 1967 Mach 6.7 flight with a dummy ramjet because of such interactions.
- **Heat load versus heat rate** — two quantities size a heat shield. The *peak heat flux* (W/cm²) determines which material can survive; the *integrated heat load* (J/cm², the heat flux integrated over time) determines how thick the insulation or ablator must be. Lifting entries reduce the peak but lengthen the pulse, so they may increase the total load.

### Entry Guidance

A lifting vehicle steers by **rolling its lift vector**: flying with lift "up" keeps it high and extends range; rolling the lift "down" or sideways makes it descend faster and turn. Entry guidance algorithms compute the bank angle needed to reach the landing site within the allowed deceleration and heating:

- **Apollo guidance** predicted the remaining range from the current state and commanded bank angles, including a "skip" phase for long-range returns.
- **Shuttle entry guidance** followed a reference **drag-acceleration-versus-velocity profile** designed to respect heating and load limits; deviations were corrected by bank angle, and periodic **roll reversals** kept the cross-range error within bounds as the orbiter weaved left and right across its ground track. The **Terminal Area Energy Management (TAEM)** phase then managed energy below Mach 2.5 to align with the runway using a "heading alignment cone".
- **Orion skip-entry guidance** can dip into the atmosphere, climb out, and re-enter to extend range to more than 8 000 km, so that a lunar return can always reach a landing zone off California; for Artemis II NASA used a less aggressive profile.
- **Mars entry guidance** (MSL, Mars 2020) used Apollo-derived bank control to reduce the landing ellipse from about 100 km to 20 km × 7 km, enabling landing in Gale and Jezero craters (Chapter 27).

Modern research applies numerical predictor–corrector guidance and convex optimisation, increasingly with onboard computing power that would have been unthinkable in the Apollo era (Chapter 45).

### Descent and Landing

After hypersonic deceleration, vehicles need a final descent and landing system (@fig:landing). Capsules deploy **drogue parachutes** at about 7–10 km (often with reefing lines that limit initial inflation to reduce opening shock) and **main parachutes** at 2–3 km; Orion's three 35 m main parachutes slow it to about 7.6 m/s at splashdown. Soyuz fires **soft-landing solid motors** about 0.7 m above the ground triggered by a gamma-ray altimeter, reducing touchdown speed from about 6 to 1.5 m/s. Boeing's Starliner lands on land using **airbags**. Winged vehicles glide to **runway** landings, and rocket stages and some landers land **propulsively**.

![Families of landing systems used by returning spacecraft.](figures/out/ch10_landing.svg){#fig:landing width=98%}

## Thermal Protection Systems

The TPS keeps the vehicle structure (typically aluminium or composite, limited to about 175 °C, or titanium to about 400 °C) cool enough during entry. There are two fundamentally different approaches: **ablative** and **reusable (insulating or radiative)**. @fig:tpsmat compares materials.

![Approximate maximum surface temperature and density of thermal protection materials. Reusable insulators such as silica tiles are extremely light; ablators tolerate far more severe conditions by sacrificing material.](figures/out/ch10_tps_materials.svg){#fig:tpsmat width=90%}

### Ablative Heat Shields

An **ablator** is a material that absorbs heat by decomposing (pyrolysing), charring and eroding. Pyrolysis gases flow out through the char and form a cooler boundary layer that blocks some of the incoming heat ("blowing"), while the char surface radiates heat away at temperatures of 2 000–3 000 °C. Ablators can handle very high heat fluxes but are consumed and are normally used once. Important ablators include:

- **Avcoat** — an epoxy-novolac resin in a fibreglass-phenolic honeycomb, used on Apollo and, in moulded block form, on Orion.
- **PICA (Phenolic-Impregnated Carbon Ablator)** — very light (≈ 0.27 g/cm³) and efficient; used on Stardust (1999–2006), Mars Science Laboratory and Mars 2020 heat shields. SpaceX's **PICA-X** (and later versions) protects Crew and Cargo Dragon; its shield can be reused a limited number of times with refurbishment.
- **SLA-561V** — a cork-silicone ablator used on Viking and many Mars landers.
- **Carbon-phenolic** — dense and robust; used for ICBM warheads and the Galileo Jupiter probe, which entered at 47.4 km/s and lost about half its heat-shield mass.
- **HEEET (Heatshield for Extreme Entry Environment Technology)** — a 3-D woven carbon/phenolic system developed by NASA for Venus, Saturn and high-speed entries.
- **Cork- and silicone-based ablators** used by ESA (Norcoat Liège on ARD, IXV, Huygens) and in Chinese capsules.

![The Artemis I Orion heat shield after its 2022 lunar-return entry. Engineers found unexpected loss of charred Avcoat material in many locations; the investigation led NASA to fly Artemis II on a modified, shallower-skip entry trajectory rather than change the heat shield.](figures/photos/ch10_orionhs.jpg){#fig:orionhs width=78%}

::: warning
**Lesson — Artemis I heat-shield char loss**

After the uncrewed Artemis I flight in 2022, engineers found that pieces of charred Avcoat had broken away from Orion's heat shield in more than 100 places, unlike Apollo-era experience. Investigators traced the cause to gases generated inside the Avcoat during the "skip" entry — in which Orion dipped into the atmosphere, climbed back out and re-entered — that could not escape because the material was not permeable enough, building pressure that cracked the char. For Artemis II (April 2026) NASA kept the existing heat shield but flew a modified entry trajectory that reduced the time spent in the conditions that caused the problem; the crew returned safely, and later Orion heat shields use a more permeable Avcoat formulation.
:::

![Arc-jet testing of Orion's Avcoat heat-shield material at NASA Ames Research Center during the investigation. Arc jets heat air to plasma temperatures with an electric arc and accelerate it over material samples for minutes, reproducing entry heating on the ground.](figures/photos/ch10_arcjet.jpg){#fig:arcjet width=78%}

### Reusable Thermal Protection

A **reusable** TPS must survive many flights without degradation. Approaches include:

- **Insulating ceramic tiles** — the Space Shuttle's tiles were made of 90 % empty space: very pure silica fibres sintered into blocks (LI-900 at 0.14 g/cm³) coated with a black, high-emittance borosilicate glass (on the hot underside) or white coating (upper surfaces). A tile can be held by its edges seconds after being removed from a 1 260 °C oven, because it conducts heat so poorly. Stronger toughened tiles (FRCI, AETB, TUFROC) followed.
- **Reinforced carbon-carbon (RCC)** — carbon fibres in a carbon matrix, protected from oxidation by a silicon-carbide coating; used on the Shuttle's nose cap and wing leading edges, where temperatures exceeded 1 260 °C.
- **Flexible blankets** — quilted silica-fabric blankets (AFRSI) and felt (FRSI) for cooler areas.
- **Metallic TPS** — superalloy or titanium shingles over insulation; studied for X-33 and other vehicles.
- **Hot structures** — load-bearing structures made of materials that can operate hot (carbon-silicon carbide, titanium aluminides), avoiding a separate TPS; used on X-37B control surfaces and hypersonic vehicles.
- **Transpiration and active cooling** — pumping a coolant through a porous surface (studied for Starship's leeward side early in development) or circulating fuel through panels (scramjets).

**Starship** uses about 18 000 hexagonal ceramic tiles attached to its stainless-steel windward side by pins, with the steel itself tolerating higher temperatures than aluminium on the leeward side. Its flight tests since 2023 have been as much about maturing a fully reusable TPS as about the vehicle itself.

### Designing and Testing a Heat Shield

Heat-shield design couples **computational fluid dynamics** (CFD with thermochemical non-equilibrium models), **material response** codes that compute pyrolysis, char and recession (e.g., NASA's FIAT and PATO), and margins for uncertainty — typically 30–50 % on heating for new designs. Ground testing uses **arc-jet** facilities (NASA Ames, NASA Johnson, CIRA Scirocco in Italy, DLR) that expose samples to supersonic plasma for minutes, **shock tunnels** and **expansion tubes** that reproduce flow conditions for milliseconds, and **ballistic ranges**. Because no ground facility reproduces all flight conditions simultaneously, flight tests and instrumented flights (e.g., MEDLI sensors on Mars landers) remain essential.

## Capsules

Most crewed and cargo vehicles that return from orbit are **capsules** — blunt, axisymmetric bodies with an ablative heat shield on the base, descending finally under parachutes to land or water (Chapter 31). Their advantages are robustness, simplicity, light weight and good packaging; their disadvantages are modest cross-range, limited reusability and relatively high landing loads. Recent trends include **propulsive landing** (Crew Dragon was designed for it but uses parachutes; the Chinese Mengzhou and Russia's planned vehicles use retro-rockets and airbags), **reusable capsules** (Dragon capsules have flown up to six or more times), and **small sample-return and manufacturing capsules** (e.g., Varda Space's W-series capsules returning materials made in orbit; Chapter 40).

## Winged Spaceplanes and Lifting Bodies

### Why Wings?

Wings and lifting-body shapes provide high L/D, giving gentle decelerations, large cross-range (the ability to land at a site far from the orbital ground track), runway landings and — in principle — rapid reuse. The costs are mass (wings, landing gear and large TPS areas) and complexity. A winged orbital vehicle typically has 2–3 times the dry mass of a capsule carrying the same crew or cargo.

### The X-15 and Early Spaceplanes

The X-15 (Chapter 9) explored hypersonic flight to Mach 6.7 and the edge of space. The US Air Force's **X-20 Dyna-Soar** (1957–1963), a small delta-winged orbital spaceplane, was cancelled before flight, but its research informed the Shuttle. Lifting-body research aircraft such as the M2-F2, HL-10 and X-24 (1960s–1970s) demonstrated that wingless shapes could glide to runway landings; the HL-10 shape later became the basis of Dream Chaser.

### The Space Shuttle (1981–2011)

The **Space Transportation System** was the world's first reusable orbital spacecraft. The winged **orbiter** (37 m long, 24 m span, about 78 t dry) launched vertically with three reusable RS-25 main engines fed from an expendable external tank and boosted by two recoverable solid rocket boosters. It carried up to seven crew and 24 t of payload to LEO, deployed and retrieved satellites, serviced Hubble five times and assembled most of the ISS. Five orbiters flew 135 missions, carrying 355 different people.

![STS-1: Space Shuttle Columbia lifts off on the first Shuttle flight, 12 April 1981 — the first time a crewed vehicle flew to orbit on its first launch.](figures/photos/ch10_sts1.jpg){#fig:sts1 width=54%}

The orbiter's thermal protection system (@fig:shuttletps) was one of its most innovative and most troublesome elements: tens of thousands of individually shaped tiles, each different, which had to be inspected and many repaired or replaced between flights.

![Schematic of the orbiter's thermal protection zones: reinforced carbon-carbon on the hottest areas, black high-temperature tiles on the underside, white low-temperature tiles and blankets on upper surfaces.](figures/out/ch10_shuttle_tps.svg){#fig:shuttletps width=86%}

![A technician installs a thermal protection tile on the underside of Space Shuttle Atlantis in the Orbiter Processing Facility at Kennedy Space Center (2003). Turnaround between flights required months of inspection and repair.](figures/photos/ch10_tiles.jpg){#fig:tiles width=66%}

::: warning
**Failure lessons — Challenger (1986) and Columbia (2003)**

On 28 January 1986, Challenger broke apart 73 seconds after launch when hot gas escaped past an O-ring seal in a solid rocket booster joint that had been weakened by cold weather, killing seven astronauts. On 1 February 2003, Columbia broke up during re-entry, killing seven, because a piece of foam insulation from the external tank had struck and breached the RCC panels of the left wing's leading edge during launch, letting superheated plasma enter the wing. Both accidents had been preceded by earlier incidents that had been rationalised as acceptable — what sociologist Diane Vaughan called the **normalisation of deviance**. The investigations (Rogers Commission; Columbia Accident Investigation Board) led to safety-culture reforms across NASA and influenced the decision to retire the Shuttle and to design the next crewed vehicles as capsules placed on top of their rockets, with launch escape systems.
:::

The Shuttle demonstrated reusable spaceflight but not cheap spaceflight: each flight cost on the order of US$450 million in marginal cost and roughly US$1.5 billion when programme costs are included, because refurbishment was labour-intensive and flight rates (at most 9 per year) were far below the 50 per year originally envisioned. @fig:reuseecon shows why refurbishment cost determines whether reuse pays.

![A simple model of average cost per flight versus number of reuses for different refurbishment costs. Reuse saves money only when refurbishment and operations are a small fraction of the cost of building a new vehicle.](figures/out/ch10_reuse_econ.svg){#fig:reuseecon width=86%}

### Buran

The Soviet **Buran** orbiter, outwardly similar to the Shuttle but launched by the powerful Energia rocket (whose core stage carried the main engines, so Buran itself had only orbital manoeuvring engines), made a single **fully automatic uncrewed orbital flight** on 15 November 1988, completing two orbits and landing autonomously on a runway at Baikonur in a crosswind of 17 m/s — a remarkable achievement in autonomous flight control. The programme was cancelled in 1993 for lack of funds; the flown vehicle was destroyed in 2002 when its hangar roof collapsed.

### Today's Spaceplanes

**Boeing X-37B Orbital Test Vehicle (USA).** A 9 m-long, 5 t uncrewed spaceplane operated by the US Space Force that launches inside a fairing and lands on a runway. Two vehicles have flown eight missions since 2010, testing technologies in orbit for up to 908 days (OTV-6, 2020–2022). OTV-7 (December 2023 – March 2025) flew in a highly elliptical orbit and demonstrated **aerobraking** to lower its orbit before landing. OTV-8, launched in August 2025 on a Falcon 9, is testing laser communications and a quantum inertial sensor for navigation without GPS.

**China's reusable experimental spacecraft.** China has flown an uncrewed reusable spacecraft on three missions (2020, 2022–2023, and a third from December 2023 to September 2024), launched on Long March 2F rockets from Jiuquan and landing on a runway; few details have been released.

**Sierra Space Dream Chaser (USA).** A 9 m lifting-body spaceplane derived from NASA's HL-20, designed to carry 5 t of cargo to the ISS and land on a runway with gentle (< 1.5 g) loads suitable for delicate experiments. A crewed version is planned. After years of delays, NASA and Sierra Space modified the cargo contract in September 2025: the first flight became a **free-flying demonstration** without ISS docking, targeted for late 2026 on a ULA Vulcan rocket, after which NASA may order cargo missions.

![The Dream Chaser engineering test article arriving at NASA's Armstrong Flight Research Center in 2017 for approach-and-landing tests, in which it was dropped from a helicopter and glided to a runway landing.](figures/photos/ch10_dreamchaser.jpg){#fig:dreamchaser width=74%}

**ESA Space Rider (Europe).** An uncrewed reusable lifting-body spacecraft, derived from the IXV demonstrator that flew in 2015, designed to carry 600 kg of experiments for two months in orbit and land under a steerable parafoil. It will be launched by Vega-C; its first flight has slipped to no earlier than 2028.

**ISRO RLV (India).** India's Reusable Launch Vehicle Technology Demonstrator flew a hypersonic test in 2016 (splashing down at sea), and the "Pushpak" vehicle completed three autonomous landing experiments (RLV-LEX) in 2023–2024 after being dropped from a helicopter, landing on a runway at Chitradurga. An orbital re-entry experiment is planned.

![Space Shuttle Discovery lands at Edwards Air Force Base with its drag chute deployed at the end of STS-53 (December 1992). The Shuttle landed like a heavy glider with no engine power, at about 340 km/h.](figures/photos/ch10_sts53.jpg){#fig:sts53 width=80%}

![Timeline of winged and lifting-body spaceplane programmes.](figures/out/ch10_timeline.svg){#fig:spaceplanetimeline width=94%}

Table: Orbital spaceplanes and lifting bodies. {#tbl:spaceplanes}

| Vehicle | Country | Length / mass | Crew | Launch | Landing | Flights / status (Oct 2026) |
|---|---|---|---|---|---|---|
| Space Shuttle orbiter | USA | 37 m / ≈ 100 t at landing | 2–8 | Vertical (own engines + SRBs + ET) | Runway | 135 flights 1981–2011 (retired) |
| Buran | USSR | 36 m / ≈ 80 t | 0 (designed for 2–10) | Energia | Runway (automatic) | 1 flight 1988 (cancelled) |
| X-37B OTV | USA | 8.9 m / ≈ 5 t | 0 | Atlas V, Falcon 9, Falcon Heavy | Runway | 8 missions (OTV-8 in orbit since Aug 2025) |
| Chinese reusable experimental spacecraft | China | not disclosed | 0 | Long March 2F | Runway | 3 missions 2020–2024 |
| Dream Chaser (Tenacity) | USA | 9 m / ≈ 9 t | 0 (crewed version planned) | Vulcan | Runway | First flight (free flyer) planned late 2026 |
| Space Rider | ESA | ≈ 4.6 m / ≈ 2.4 t | 0 | Vega-C | Parafoil on runway/ground | First flight NET 2028 |
| IXV | ESA | 5 m / ≈ 2 t | 0 | Vega | Parachute at sea | 1 suborbital flight 2015 |
| RLV-TD / Pushpak | India | 6.5 m / 1.75 t | 0 | Rohini booster / helicopter drops | Sea / runway | Hypersonic test 2016; landing tests 2023–24 |


## Entry at Other Worlds

Atmospheric entry is not unique to Earth. Planetary missions enter atmospheres with very different compositions and speeds (@fig:entryspeeds): Mars' thin CO₂ atmosphere provides little drag, so landers must also use parachutes and rockets (Chapter 27); Venus' dense CO₂ atmosphere and high entry speed produce severe heating; Titan's thick, cold nitrogen atmosphere allowed Huygens a gentle 2.5-hour parachute descent; and the Galileo probe's entry into Jupiter at 47.4 km/s remains the most extreme ever survived, consuming about half of its carbon-phenolic heat shield. **Aerocapture** — using a single pass through a planet's atmosphere to brake into orbit instead of a propulsive burn — and **aerobraking** (many shallow passes to gradually lower an orbit, used by Magellan, Mars Global Surveyor, MRO, TGO and X-37B) exploit atmospheres to save propellant.

![Entry speeds of representative missions relative to the atmosphere they entered. The Galileo probe's Jupiter entry was nearly four times faster than any Earth return.](figures/out/ch10_entry_speeds.svg){#fig:entryspeeds width=86%}

## Uncontrolled Re-entries and Design for Demise

Not every re-entry is planned. Thousands of satellites, rocket stages and fragments re-enter each year; most burn up, but dense or high-melting-point components (titanium and stainless-steel tanks, optical benches, reaction-wheel hubs, carbon-fibre-overwrapped pressure vessels) can survive to the ground. About 10–40 % of the mass of large objects may survive.

- **Skylab** (77 t) re-entered over Western Australia in 1979, scattering debris over the town of Esperance.
- **Tiangong-1** (2018) and **Long March 5B core stages** (≈ 21 t, re-entering uncontrolled in 2020–2022) drew international criticism.
- In March 2024 a 0.7 kg fragment from a pallet of old ISS batteries, jettisoned in 2021, crashed through the roof of a house in Florida — prompting legal claims against NASA under the Liability Convention principles.
- Fragments of SpaceX Dragon trunks have been found on farms in Australia (2022) and North Carolina (2024), and debris from a Falcon 9 upper stage fell in western Poland (2025).

International guidelines require that the **casualty risk** from an uncontrolled re-entry be below **1 in 10 000** (NASA-STD-8719.14, ISO 27875 and many national laws); otherwise the object must perform a **controlled re-entry** over the South Pacific Ocean Uninhabited Area ("Point Nemo"), as done for cargo vehicles, the Mir station (2001) and planned for the ISS (≈ 2030, using the SpaceX-built US Deorbit Vehicle). Engineers increasingly practise **design for demise** — choosing materials and configurations (aluminium rather than titanium tanks, components that separate early) so that nothing survives re-entry — tools such as NASA's DAS and ORSAT and ESA's DRAMA predict surviving fragments. Re-entry is also a growing environmental question: aluminium oxide particles from thousands of burning satellites each year may affect stratospheric chemistry, an active research topic.

## Hypersonic Air-Breathing Flight and Single-Stage-to-Orbit

A long-standing dream is a vehicle that takes off from a runway, breathes air for much of its ascent (avoiding the need to carry oxidiser), and flies to orbit in a single stage. Air-breathing engines offer specific impulses of 1 000–4 000 s compared with about 450 s for the best rockets, but their thrust-to-weight ratio is low and they work only within the atmosphere up to about Mach 5 (turbojets, ramjets) or Mach 10–15 (scramjets, in theory).

- **Scramjets** (supersonic-combustion ramjets) burn fuel in a supersonic airstream. NASA's X-43A reached Mach 9.6 for about 10 seconds in 2004; the X-51A sustained Mach 5.1 for 210 seconds in 2013. Many countries now fly scramjet-powered hypersonic missiles.
- **Combined-cycle engines** switch between modes. The British **SABRE** (Synergetic Air-Breathing Rocket Engine) concept used a pre-cooler to chill incoming air from 1 000 °C to −150 °C in milliseconds, allowing an engine to run as an air-breathing rocket up to Mach 5.5 and then switch to pure rocket mode, for the proposed **Skylon** single-stage-to-orbit spaceplane. Its developer, Reaction Engines, demonstrated the pre-cooler at Mach 5 conditions in 2019 but entered administration in October 2024.
- **Single-stage-to-orbit (SSTO)** remains elusive: the required propellant fraction leaves almost no mass for structure, TPS, engines and payload with current technology. The US NASP/X-30 (1986–1993), the X-33/VentureStar (cancelled 2001) and others were abandoned. Two-stage, partially or fully reusable rockets (Falcon 9, New Glenn, Starship) have instead become the route to cheap access (Chapter 34).

## Reusability Beyond Spaceplanes

The reusability revolution of the 2010s came not from spaceplanes but from **vertically landing rocket stages** and **reusable capsules**. Falcon 9 first stages land on drone ships or landing pads and have flown more than 30 times each; New Glenn's booster landed on its second flight (November 2025); China's commercial and state rockets have begun landing tests; and Starship's Super Heavy boosters are caught by the launch tower's mechanical arms. These are discussed in Chapter 34 and Chapter 36. The lessons of the Shuttle — design for rapid inspection and minimal refurbishment, and fly often — have been central to their success.

::: key
**Key takeaways**

- Returning from LEO means dissipating ≈ 30 MJ/kg (≈ 60 MJ/kg from the Moon); a blunt shape puts most of the heat into the air through a detached bow shock.
- Peak deceleration for a ballistic entry depends only on speed and angle; lift (even L/D ≈ 0.3) cuts loads from ≈ 8–9 g to 3–4 g and allows steering; winged vehicles keep loads near 1.5 g with large cross-range.
- Ablative heat shields (Avcoat, PICA, carbon-phenolic) handle the most severe entries; reusable TPS (silica tiles, RCC, ceramic hex tiles) must survive many flights with minimal refurbishment.
- The Shuttle proved reusable spaceflight but was expensive because of refurbishment; Columbia and Challenger taught lasting safety lessons.
- Today's spaceplanes are uncrewed or cargo vehicles (X-37B, Chinese spaceplane, Dream Chaser, Space Rider, ISRO RLV); air-breathing SSTO remains a research goal, while reusable rocket stages dominate in practice.
:::

::: questions
**Review questions**

1. Calculate the kinetic energy per kilogram of a vehicle entering at 7.8 km/s and at 11 km/s. Why does only a small fraction of this energy reach the vehicle as heat?
2. Explain the "blunt-body insight" of Allen and Eggers. Why are re-entry capsules blunt rather than pointed?
3. Use the Allen–Eggers result to estimate the peak deceleration of a ballistic entry at 7.8 km/s with a 3° entry angle, taking a scale height of 7 km. How does a lift-to-drag ratio of 0.3 change the result?
4. What is the entry corridor? What happens if the entry angle is too shallow or too steep?
5. Why does communications blackout occur during re-entry, and how has it been overcome for some vehicles?
6. Compare ablative and reusable thermal protection systems, giving two examples of each and the missions they suit.
7. What made the Space Shuttle expensive to operate, and what safety lessons did the Challenger and Columbia accidents teach?
8. What is "design for demise"? Why does it matter for satellites that re-enter uncontrolled?
:::
