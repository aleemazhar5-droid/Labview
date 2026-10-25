---
title: In-Space Servicing, Assembly and Manufacturing
hero: ch40
abstract: Almost every satellite ever launched has been used once and thrown away, retired with working instruments because its propellant ran out or a single part failed. In-space servicing, assembly and manufacturing (ISAM) aims to change that by inspecting, refuelling, repairing, upgrading, moving and disposing of spacecraft in orbit, building structures too large for any rocket fairing, and making products that can only be made in weightlessness. This chapter traces servicing from the Skylab and Hubble spacewalks to the commercial robots docking with communication satellites in 2020–26, explains the engineering of rendezvous, capture and refuelling, and estimates the economics of life extension, debris removal and orbital propellant depots, with the state of every major programme as of October 2026.
---

A geostationary communication satellite costs several hundred million dollars to build, launch and insure, and is designed to work for about 15 years. When it retires, its transponders usually still work: what it has run out of is the few hundred kilograms of propellant needed to stay in its slot. A science observatory can be crippled by one failed gyroscope; a broken solar-array hinge can end a mission worth billions. On Earth, no one would scrap a car because its fuel tank was empty or a tyre was flat. In orbit, until recently, there was no alternative.

**In-space servicing, assembly and manufacturing (ISAM)** is the set of technologies that treat spacecraft as maintainable, upgradeable and buildable in place. The term was adopted in the United States' *ISAM National Strategy* of April 2022; NASA previously used **OSAM** (on-orbit servicing, assembly and manufacturing), and European documents speak of **in-orbit servicing (IOS)**. The idea is old — astronauts repaired Skylab in 1973 — but for forty years it depended on the Space Shuttle and its crews. What changed after 2019 is that robotic servicers began to dock with commercial satellites as a paid service, that China demonstrated similar capabilities in geostationary orbit, and that refuelling became central to plans for returning people to the Moon.

This chapter follows the three strands of ISAM in turn. Servicing extends and repairs existing spacecraft; assembly builds structures larger than any launcher can carry; manufacturing makes things — parts, fibres, crystals, tissues — in orbit. Rendezvous and proximity operations, the common foundation of all three, are treated in detail; the orbital mechanics of relative motion is introduced in Chapter 3, and the security implications of satellites that approach other satellites in Chapter 19.

## What ISAM Means and Why It Matters

@tbl:isamactivities lists the main ISAM activities, from the simplest — looking at another spacecraft from close range — to the most ambitious. They share a ladder of difficulty. **Inspection** needs only safe proximity operations. **Relocation** and **life extension** need a physical connection that can carry thrust loads. **Refuelling** adds leak-tight fluid connections; **repair and upgrade** add dexterous robotics; **assembly** and **manufacturing** require all of these to be repeatable, hundreds of times, without people present.

| Activity | What it does | Typical client | Status (Oct 2026) |
|---|---|---|---|
| Inspection | Close-range imaging of a satellite or debris object | Any; damaged or unknown objects | Operational (commercial and military) |
| Relocation and disposal | Tow to a new slot, graveyard orbit or re-entry | Dead or retiring satellites; debris | Demonstrated in GEO (2020, 2022) |
| Life extension | Attach a vehicle or pod that takes over attitude and orbit control | GEO satellites short of propellant | Commercial since 2020 |
| Refuelling | Transfer propellant through a valve | Prepared clients (port); later unprepared | Demonstrated 2007; commercial demos 2026–27 |
| Repair and upgrade | Replace units, free stuck mechanisms, add payloads | Prepared or high-value clients | Crewed (Hubble); robotic in development |
| Assembly | Join modules, trusses or mirror segments | Stations, antennas, telescopes | Crewed (ISS); robotic demos planned |
| Manufacturing | Print, draw, crystallise or grow material in orbit | Parts, fibres, drugs, semiconductors | Demonstrations on ISS and free-flyers |

: The main ISAM activities, in rough order of increasing difficulty. {#tbl:isamactivities}

The arguments for ISAM are economic, scientific and environmental:

- **Life extension.** A satellite that keeps earning for five more years defers the cost of a replacement worth hundreds of millions of dollars.
- **Repair and upgrade.** Hubble was launched with a flawed mirror and 1980s electronics; five servicing missions turned it into one of the most productive scientific instruments ever built (Chapter 38).
- **Debris removal.** The objects that threaten long-term sustainability in low Earth orbit are a few thousand large derelicts (Chapter 21); only something that can rendezvous with and grip them can remove them.
- **Size.** A rocket fairing limits a monolithic structure to about 5 m (or 9 m for Starship). Larger telescopes, antennas and solar power stations must be folded or built in orbit.
- **New products.** Weightlessness suppresses convection and sedimentation, enabling purer glasses and crystals; and refuelling in orbit multiplies what one rocket can send beyond it.

## Sixty Years of Servicing

The history of servicing has two halves: four decades in which astronauts did the work, and a commercial robotic era that began in 2020 (@fig:isamtimeline).

![Milestones of in-space servicing, assembly and manufacturing. (a) Until 2012 nearly all servicing was done by astronauts working from the Space Shuttle. (b) Since 2014 the field has shifted to commercial robotic servicers, debris-removal demonstrators and manufacturing experiments.](figures/out/ch40_timeline.svg){#fig:isamtimeline width=100%}

### Astronauts as Servicers

The first repair was improvised. When Skylab reached orbit in May 1973 with its micrometeoroid shield torn away and a solar wing jammed, its first crew deployed a sunshade through a small airlock and cut the wing free on a spacewalk (Chapter 33). The Space Shuttle then made servicing a planned activity. The **Solar Maximum Mission** satellite had lost its fine pointing in 1980 when fuses in its attitude-control system failed; it was built with a grapple fixture and replaceable modules precisely so that the Shuttle could fix it. In April 1984 George Nelson flew to it with the Manned Manoeuvring Unit (@fig:solarmaxmmu) to attach a docking device to a pin on its side. The device failed to latch — an unexpected small fitting was in the way — and Nelson's attempt to steady the satellite by hand set it tumbling. Controllers at NASA Goddard stabilised it overnight, Challenger's robotic arm grappled it, and Nelson and James van Hoften replaced the attitude-control module and repaired an instrument's electronics. Solar Max returned to work until it re-entered in 1989.

::: figrow
![George Nelson, flying the Manned Manoeuvring Unit, approaches the ailing Solar Maximum Mission satellite during STS-41C in April 1984. His attempt to dock by hand failed; the Shuttle's arm captured the satellite instead.](figures/photos/ch40_solarmax.jpg){#fig:solarmaxmmu}

![Richard Hieb, Thomas Akers and Pierre Thuot hold the 4.5-tonne Intelsat VI (603) satellite above Endeavour's payload bay on 13 May 1992, minutes after the only three-person capture by hand.](figures/photos/ch40_intelsat.jpg){#fig:intelsat603}
:::

Later in 1984, the crew of STS-51A retrieved two communication satellites, Palapa B2 and Westar 6, stranded in useless orbits by failed kick motors, and brought them back to Earth; both were refurbished and launched again. The most dramatic rescue came in 1992. Intelsat 603 had been left in low orbit when its Titan III upper stage failed to separate in 1990. On Endeavour's first flight, STS-49, two attempts to attach a capture bar failed because the satellite rotated away at the slightest touch; on the third spacewalk three astronauts simply grabbed it by hand (@fig:intelsat603), the only three-person spacewalk ever made. They fitted a new perigee motor, and the satellite reached geostationary orbit and served for many years.

**Hubble** was designed for servicing from the start, with handrails, standard bolts and drawer-like **orbital replacement units**. Five Shuttle missions between 1993 and 2009 (Chapter 38) replaced every instrument, gyroscope set and battery and corrected the flawed optics; each began with the Shuttle's arm grasping one of two grapple fixtures on the telescope and berthing it in the payload bay (@fig:hubblegrapple). The **International Space Station** was the culmination: assembled from 1998 to 2011 by Shuttle and Russian launches, it remains a servicing laboratory in which crews and the Canadarm2 and Dextre robots replace pumps, batteries and solar arrays (Chapter 32).

![Hubble held by Atlantis's robotic arm on 13 May 2009 at the start of the fifth and final servicing mission, STS-125. The grapple fixture and handrails were designed in from the start.](figures/photos/ch40_hstgrapple.jpg){#fig:hubblegrapple width=64%}

The lesson of the Shuttle era is mixed. Servicing worked spectacularly on clients designed for it — Solar Max and Hubble — and was heroic but risky on clients that were not. And it was expensive: each Hubble mission required a Shuttle flight costing well over a billion dollars at full cost, so it was never economical for commercial satellites.

### Robotic Pioneers

Robotic servicing began with fuel. In January 1978 the uncrewed **Progress 1** docked with the Salyut 6 station and pumped propellant into its tanks — the first transfer of propellant between spacecraft — and Progress and China's Tianzhou freighters still refuel the ISS and Tiangong. Japan's **ETS-VII** (1997–99) made the first autonomous docking between two uncrewed satellites and tested a robotic arm in orbit. NASA's **DART** demonstrator of 2005 (not the later asteroid impactor) showed the dangers: errors in its navigation software made it collide gently with its target. In 2007 DARPA's **Orbital Express** — the Boeing-built ASTRO servicer and Ball's NextSat client — demonstrated nearly everything a servicer needs: autonomous rendezvous, capture with a robotic arm, transfer of hydrazine in both directions, and the exchange of a battery and a flight computer.

NASA then tackled a harder problem: refuelling a satellite never designed for it, whose fill-and-drain valves are covered by caps, lock wire and thermal blankets meant to be closed once, on the ground. The **Robotic Refuelling Mission (RRM)**, carried to the ISS on the last Shuttle flight in 2011 (@fig:rrmfossum), gave Dextre a set of specialised tools that cut lock wire, unscrewed caps and, in 2013, transferred liquid ethanol through a standard valve. RRM3 (2018–19) aimed to store and transfer liquid methane, a cryogenic propellant, but a failed cryocooler forced its methane to be vented.

::: figrow
![Astronaut Mike Fossum, riding Canadarm2, carries the Robotic Refuelling Mission module during the final Shuttle mission in July 2011. Dextre later used its tools to open and refuel simulated satellite valves.](figures/photos/ch40_rrm.jpg){#fig:rrmfossum}

![The hose management assembly built for NASA's Restore-L (later OSAM-1) refuelling servicer, in electromagnetic testing at Kennedy Space Center in 2020. It extended and retracted the propellant hose like a tape measure.](figures/photos/ch40_restorel.jpg){#fig:restorelhose}
:::

RRM led to **Restore-L**, renamed **OSAM-1**: a servicer that would grasp the Landsat 7 satellite, refuel it, and use a separate arm called SPIDER to assemble a 3 m antenna and manufacture a 10 m beam (@fig:restorelhose). Its cost estimate grew from about $650–750 million to more than $2 billion, and in March 2024 NASA cancelled it, citing "continued technical, cost, and schedule challenges" and "a broader community evolution away from refueling unprepared spacecraft". About $1.5 billion had been appropriated. A companion mission to 3D-print beams in orbit, OSAM-2 (Archinaut One), had been closed out in 2023 before flight.

### Commercial Life Extension

The first commercial servicer avoided refuelling altogether. Northrop Grumman's **Mission Extension Vehicle (MEV)** — about 2.3 t at launch, built for a 15-year life — docks with a client, then provides all of the combined vehicle's attitude and orbit control with its own electric thrusters. It needs nothing special on the client: it inserts a probe into the satellite's liquid apogee engine (the large rocket motor used once to reach geostationary orbit), expands a tip inside the nozzle, and pulls itself in until stanchions press against the launch-adapter ring (see @fig:captureinterfaces).

**MEV-1** docked with Intelsat 901, which had been parked in the graveyard orbit about 300 km above GEO, on 25 February 2020 — the first docking of two commercial satellites — and returned it to service in April 2020. After about five years it moved Intelsat 901 back to the graveyard orbit, undocked on 9 April 2025 and went on to an Optus satellite. **MEV-2** docked with Intelsat 10-02 directly in its operational slot in April 2021, for a planned stay of about five years. Intelsat reportedly paid about $13 million per year for the service.

Northrop's second generation launched on a Falcon 9 on 21 July 2026: the **Mission Robotic Vehicle (MRV)**, carrying the robotic arms and tools of DARPA's Robotic Servicing of Geosynchronous Satellites (RSGS) programme, together with three **Mission Extension Pods (MEPs)**. Each MEP is a small propulsion module that the MRV will attach to a client's launch-adapter ring; the pod then keeps the satellite on station for up to about eight years while the MRV moves on. The MRV needs about a year to raise itself to geostationary orbit with electric propulsion; early customers include Optus and SES (which absorbed Intelsat in 2025). After checkout, RSGS operations are to pass to the US Space Force.

### China's Geostationary Servicers

China has developed comparable capabilities, with less publicity. **Shijian-21**, launched in October 2021, docked with the dead BeiDou-2 G2 navigation satellite in December 2021 and in January 2022 towed it about 3 000 km above the geostationary belt — far higher than the usual 300 km graveyard — before returning to GEO. **Shijian-25**, launched in January 2025, approached Shijian-21 and the two appeared merged in commercial optical tracking from about 2 July 2025, separating again by late November. The pairing was widely reported as the first refuelling in geostationary orbit, but China has not described what was transferred. Because the same rendezvous, grappling and towing capabilities could disable another nation's satellite, these missions are watched closely (Chapter 19).

### Debris Removal and Inspection

Removing debris is harder than servicing a satellite: the target was never meant to be approached, may be tumbling, has no lights, reflectors or radio, and nobody pays it to cooperate. Japan's **Astroscale** has worked up to it step by step (@tbl:servicingmissions). **ELSA-d** (launched March 2021) released and recaptured its own small client with a magnet in August 2021, but thruster failures in 2022 ended its more ambitious tests. **ADRAS-J**, launched on an Electron rocket in February 2024 under a JAXA contract, made the first close inspection of a large piece of real debris: an 11 m, 3 t H-IIA upper stage left in orbit in 2009. It flew around the stage at 50 m in mid-2024 — once aborting automatically when the target's attitude did not match predictions — and in late November 2024 closed to about 15 m from the planned capture point. **ADRAS-J2**, under a JAXA contract worth about ¥12 billion (about $80 million), is to capture the same stage with a robotic arm and lower it for re-entry; a launch on Isar Aerospace's Spectrum rocket in Japan's fiscal year 2027 (up to April 2028) was contracted in September 2026.

| Mission | Operator | Launch | Client | Result (as of Oct 2026) |
|---|---|---|---|---|
| Orbital Express | DARPA (Boeing, Ball) | 2007 | Own client (NextSat) | Capture, hydrazine transfer, battery and computer swap |
| MEV-1 | Northrop Grumman | 2019 | Intelsat 901 (GEO) | Docked 2020; 5 years' extension; moved on 2025 |
| MEV-2 | Northrop Grumman | 2020 | Intelsat 10-02 (GEO) | Docked in slot 2021 |
| ELSA-d | Astroscale | 2021 | Own client (17 kg) | Magnetic capture 2021; ended 2024 |
| Shijian-21 | China | 2021 | Dead BeiDou-2 G2 | Towed 3 000 km above GEO, 2022 |
| ADRAS-J | Astroscale / JAXA | 2024 | H-IIA upper stage | Inspected down to 15 m |
| Shijian-25 | China | 2025 | Shijian-21 | Docked 2025; refuelling reported, unconfirmed |
| Katalyst LINK | Katalyst / NASA | 2026 | Swift observatory | Lost attitude control; reboost abandoned |
| MRV + 3 MEPs | Northrop Grumman | 2026 | GEO comsats | Raising orbit to GEO |
| Otter | Starfish Space | 2026 | Defunct US satellites | Commissioning; inspection for NASA |
| ADRAS-J2 | Astroscale / JAXA | FY2027 | H-IIA upper stage | Capture and de-orbit planned |
| ClearSpace-1 | ESA (OHB, ClearSpace) | ≈ 2029 | PROBA-1 (95 kg) | Capture with four arms planned |

: Robotic servicing and debris-removal missions (selected). {#tbl:servicingmissions}

Europe's **ClearSpace-1**, led by OHB with the Swiss company ClearSpace, will capture ESA's 95 kg PROBA-1 satellite, launched in 2001, with four arms and de-orbit it; ESA lists the launch for 2029. In the USA, **Starfish Space** launched its first full-size Otter servicer on a SpaceX rideshare at the start of October 2026 to inspect defunct US satellites for NASA, ahead of planned life-extension work for Intelsat in GEO and de-orbit services for the Space Development Agency; its smaller Otter Pup 2 demonstrator, in orbit since June 2025, had not yet docked with a client.

A reminder of how unforgiving the field is came in 2026. NASA's Swift gamma-ray observatory, launched in 2004, was decaying towards re-entry, and in September 2025 NASA gave the start-up **Katalyst Space** a $30 million contract to boost it — a first attempt to reboost a satellite not designed for servicing, on a schedule of months rather than years. Its 425 kg LINK spacecraft reached orbit on the final Pegasus XL launch on 3 July 2026, but three weeks later it lost attitude control and two of its three reaction wheels failed. It came within 12–15 km of Swift before the reboost was abandoned in August; LINK re-entered on 25 September, and Swift is expected to re-enter around the end of 2026.

## Rendezvous, Proximity Operations and Capture

Every ISAM activity starts with **rendezvous and proximity operations (RPO)**: bringing two spacecraft from hundreds of kilometres apart to contact, safely. The far-range phases — launch into a slightly lower or higher orbit, phasing, and orbit matching — use the methods of Chapter 3. Within a few kilometres the relative motion is described by the Clohessy–Wiltshire equations in the target's local frame, with *x* radial (the **R-bar**, pointing away from Earth) and *y* along the target's velocity (the **V-bar**). Their solutions are counter-intuitive: a forward push raises a spacecraft and makes it drift backwards, and a spacecraft below the target drifts forwards.

### Approach Strategies

Operators approach along one of two straight lines through the target (@fig:isamapproach). On the **V-bar** a chaser can rest at any distance ahead of or behind the target, because it then shares the target's orbit; this makes the V-bar ideal for **hold points**, where the approach pauses while controllers check sensors and give the go-ahead. The chaser moves between hold points by **radial hops**: a small burn towards Earth makes it dip below the target's orbit, travel forwards and return to the V-bar half an orbit later, where an equal and opposite burn stops it. The ISS's European ATV and Japanese HTV, and today's Cygnus and Dragon, all use variants of these patterns.

![Approach strategies computed from the Clohessy–Wiltshire equations for a target in a 420 km orbit. (a) A V-bar approach: two radial hops carry the chaser from 3 km to a hold point 200 m behind the target, followed by a slow straight-line approach. (b) An approach up the R-bar from below: if thrust is lost, orbital mechanics makes the chaser fall away. (c) If thrusters fail during a V-bar approach from 100 m, a slow chaser stops short of the target while a fast one sweeps past it — the basis of "passively safe" approach speeds.](figures/out/ch40_approach.svg){#fig:isamapproach width=100%}

The **R-bar** approach climbs towards the target from directly below (or descends from above). Here orbital mechanics provides **natural braking**: a chaser below the target is in a lower orbit, so the tidal term in the equations pulls it down and away; to hold position on the R-bar it must thrust continuously towards the target, and if the thrust stops it falls away and drifts ahead, as in panel (b). The Shuttle approached the ISS this way, and so do servicers wanting to reach a client's underside. The final metres are flown along a narrow **approach corridor** at a few centimetres per second, with the docking interface pointing at the chaser.

The key design rule is **passive safety**: at every point, if the chaser's thrusters stopped working, its free drift must not hit the target. Panel (c) shows why approach speeds must be low. A chaser closing at 0.1 m/s from 100 m behind on the V-bar, with its thrusters suddenly dead, coasts forward only 42 m before orbital mechanics lifts it and carries it back; at 0.3 m/s it sweeps over the target within 34 m. Approach paths are surrounded by **keep-out spheres** that the chaser may enter only after explicit approval.

::: example
**Example: hopping along the V-bar**

A servicer must move from a hold point 1 km behind a client in a 420 km orbit to a point just behind it. The mean motion is $n = \sqrt{\mu/r^3}$ = 1.126 × 10⁻³ rad/s, so the orbital period is 93.0 min.

1. **Radial hop.** For a radial burn $\Delta v$, the Clohessy–Wiltshire solution gives $x = -(\Delta v/n)\sin nt$ and $y = (2\Delta v/n)(1-\cos nt)$. After half an orbit the chaser is back on the V-bar, $4\Delta v/n$ further forward. For a 1 000 m hop, $\Delta v = nL/4$ = 1.126 × 10⁻³ × 1 000 / 4 = **0.28 m/s**; an equal burn stops it, so the hop costs 0.56 m/s and takes 46.5 min. The path dips 250 m below the V-bar.
2. **Straight-line approach.** Flying the same 1 000 m straight along the V-bar requires continuous radial thrust to cancel the Coriolis term, $a_x = 2n\,\dot y$. Integrated over the approach this costs $2nL$ = **2.25 m/s** whatever the speed — four times the hop's cost, which is why straight lines are kept for the last few hundred metres.
3. **Passive safety.** A chaser drifting forward at speed $v$ along the V-bar travels at most 0.478 $v/n$ before reversing. In LEO at 0.1 m/s that is 42 m. In GEO, where $n$ = 7.29 × 10⁻⁵ rad/s, the same speed would carry it 655 m: to stop short of a client 100 m away, a GEO servicer must approach at less than 1.5 cm/s. Hops are cheap there (0.036 m/s per kilometre) but each one takes 12 hours.
:::

### Sensors and Navigation

A servicer measures the client's relative position and attitude — its **pose** — with a sequence of sensors that hand over as the range shrinks: relative GNSS or ground tracking at tens of kilometres, visible and infrared cameras that see the client as a point and then as a shape, and lidar or time-of-flight cameras below a few hundred metres that measure range and three-dimensional shape directly. Cooperative clients such as the ISS carry retroreflectors and radio beacons; unprepared clients do not, so the servicer must estimate pose from images alone, under harsh lighting that changes every few minutes, using the client's known geometry. Thermal infrared cameras help in eclipse and against glinting surfaces. The guidance software, running on board because ground loops are too slow and too intermittent, must recognise when measurements stop making sense and abort — as ADRAS-J did when the rocket stage's attitude departed from predictions.

### Capturing a Client

How a servicer grips its client depends on whether the client was **prepared** — fitted before launch with a grapple fixture, docking plate or refuelling port — or **unprepared**. @fig:captureinterfaces compares the main options. Prepared interfaces are simple and reliable: the Shuttle's and ISS's arms snare a grapple pin with three wires, and Astroscale's clients carry a ferromagnetic plate. Most satellites in orbit, though, were never prepared, so the commercial servicers have learned to grip features that almost every satellite has anyway: the **launch-adapter ring** and its bolt holes, by which the satellite was clamped to its rocket, and the nozzle of the **liquid apogee engine** that raised it to GEO. Both are strong enough to carry towing loads and are located on the satellite's axis.

![Six ways for a servicer to grip a client. The top row and the magnetic plate are proven in orbit; prepared interfaces (grapple fixture, magnetic plate, refuelling port) need equipment fitted before launch, while the apogee-engine probe and ring grasp work on most satellites already in orbit. Nets and harpoons can catch tumbling debris but give poor control afterwards.](figures/out/ch40_interfaces.svg){#fig:captureinterfaces width=94%}

**Tumbling** is the main obstacle to capturing debris. Without attitude control, objects are spun up over years by solar radiation pressure, gravity-gradient torques and eddy currents induced by Earth's magnetic field. Envisat, the 8.2 t ESA satellite that failed in 2012, was measured by laser ranging spinning once every 135 s in 2013 — about 2.7° per second. A grasp point 5 m from the spin axis of such an object moves at about 24 cm/s (@fig:tumblecapture), far too fast to seize gently, so a servicer must either fly in synchrony with the rotation, matching the spin while hovering, or slow the target down first, for example by eddy-current braking, plume impingement or repeated gentle contacts. After capture, the stack's angular momentum must be absorbed. An H-IIA upper stage (moment of inertia about 3.3 × 10⁴ kg·m²) tumbling at 1° per second carries about 580 N·m·s, more than ten times what a large reaction wheel can store, so servicers use thrusters to detumble the combined vehicle.

![Capturing a tumbling object. (a) The speed of a grasp point grows with tumble rate and with its distance from the spin axis; only slowly rotating targets can be seized directly. (b) The angular momentum of large debris objects at typical tumble rates exceeds the storage of reaction wheels, so thrusters must stop the rotation after capture.](figures/out/ch40_capture.svg){#fig:tumblecapture width=96%}

### Robotic Arms and Tools

Servicing robots descend from the Shuttle's arm and from the ISS's **Canadarm2** and **Dextre** (Chapter 32), but must work without astronauts nearby and often with a time delay of a quarter of a second or more through geostationary relays. The arms that FREND and RSGS developed for GEO servicing have seven joints, like a human arm, so that they can reach around obstacles, and carry force–torque sensors at the wrist. Their controllers use **compliance** (also called impedance control): instead of driving the hand rigidly to a position, they make it behave like a spring and damper, so that contact forces stay small even if the client is not exactly where the cameras think it is. Free-flying arms also disturb their own base: every arm motion rotates the servicer slightly in the opposite direction, and the control system must account for this coupling.

Tools turn arms into technicians. NASA's RRM tools — a wire cutter, a multifunction tool that unscrews caps, a nozzle tool that mates with standard fill-and-drain valves, and a camera tool for looking inside blanketed areas — showed that even lock-wired valves could be opened robotically. Teleoperation from the ground remains normal for complex tasks, with operators watching stereo video and a simulation that predicts the arm's motion through the time delay; routine motions are increasingly automated.

### Refuelling Interfaces and Standards

Refuelling an unprepared satellite is possible but slow, because the robot must reproduce work done by hand on the ground. The industry is therefore converging on **refuelling ports** fitted before launch (@tbl:refuelinterfaces), which open, seal and verify the connection in one robotic operation, together with standard **grapple fixtures** for capture. Agreeing on such interfaces — and on how close servicers may approach other operators' satellites — is the work of industry groups such as **CONFERS** (Consortium for Execution of Rendezvous and Servicing Operations), founded with DARPA support in 2018, whose principles fed into the international standard ISO 24330:2022 on rendezvous, proximity operations and on-orbit servicing.

| Interface | Developer | Type | Notes |
|---|---|---|---|
| Standard fill-and-drain valve | Satellite industry | Unprepared | Opened robotically by RRM tools; slow, multi-step |
| Probe and ring docking | Northrop Grumman (MEV, MEP) | Unprepared | No fluid transfer; servicer takes over propulsion |
| RAFTI port | Orbit Fab | Prepared | Accepted by the US Space Force (2024) as a refuelling interface |
| GRIP | Orbit Fab | Servicer side | Docks with RAFTI-equipped clients; flight-qualified 2025 |
| ASSIST | GMV / ESA | Prepared | Docking and refuelling; servicer tool plus passive client fixture |
| Magnetic docking plate | Astroscale | Prepared | For capture and de-orbit at end of life |
| ISO 24330:2022 | ISO (CONFERS input) | Standard | Programmatic principles and practices for RPO and servicing |

: Capture and refuelling interfaces and standards. {#tbl:refuelinterfaces}

Refuelling demonstrations on prepared clients were scheduled for 2026–27: Astroscale US's 300 kg APS-R servicer is to transfer hydrazine to one of the Space Force's Tetra-5 satellites in GEO, and Orbit Fab planned to fly its GRIP system to service the same satellites. As of October 2026, neither had been reported as launched.

### Safety, Law and Trust

Servicing raises questions that ordinary satellites do not. Under the Outer Space Treaty, a state keeps **jurisdiction and control** over an object it registered — including debris — indefinitely, so removing another nation's dead satellite or rocket stage needs that state's consent. Liability for damage in orbit depends on proving fault, which is hard when two spacecraft touch on purpose. Servicers must convince their clients' insurers and regulators that they will not turn a working satellite into a tumbling wreck; the MEVs first rehearsed their docking on Intelsat 901 in the graveyard orbit, where an accident would not have endangered the GEO belt. And because the same technology can inspect, disable or move another country's satellite, transparency about intentions and approaches — what CONFERS calls being a "responsible actor" — matters as much as engineering (Chapter 19).

## The Economics of Life Extension and Debris Removal

### What a Satellite-Year Is Worth

A geostationary satellite drifts north–south under lunar and solar gravity and east–west under Earth's slightly elliptical equator, and needs about 50 m/s of Δv per year to stay in its slot. With chemical thrusters of 290 s specific impulse, a 2 500 kg satellite therefore burns about 44 kg of propellant a year, and must keep about 10 kg in reserve to raise itself to the graveyard orbit at the end (@fig:lifeextvalue). With 100 kg of usable propellant left, it has about two years to live — and because propellant gauging is uncertain, operators often retire satellites with a margin that a servicer could have used.

![Economics of life extension. (a) Remaining life of a GEO satellite as a function of its usable propellant. (b) Net present value to an operator of extending a satellite's life at the reported MEV price of about $13 million a year: worthwhile if the satellite still earns well, or if extension defers an expensive replacement.](figures/out/ch40_lifeext.svg){#fig:lifeextvalue width=96%}

Whether extension pays depends on what the satellite still earns. A satellite with 40 transponders leased at about $1 million each per year earns $40 million a year; paying $13 million a year for five more years gives the operator a present value of about $108 million at an 8 % discount rate. Even if the satellite would otherwise be replaced immediately, deferring a $300 million replacement by five years is worth about $96 million in present value, $44 million more than the fees. Conversely, a satellite earning less than its servicing fee is not worth extending. The market is limited by the number of high-value satellites approaching the end of their propellant at any time — some tens per year — and by competition from cheaper new satellites and from LEO constellations.

::: example
**Example: a tug in geostationary orbit**

A servicer of 2 330 kg (MEV class) docks with a 2 500 kg satellite whose tanks are empty. The combined mass is 4 830 kg.

1. **Disposal.** Raising the stack 300 km above GEO (r = 42 164 km, v = 3.075 km/s) by a Hohmann transfer takes two burns of 5.44 m/s, 10.9 m/s in total. With chemical thrusters (Isp 300 s, $v_e$ = 2 942 m/s) this uses $m_p = m_0(1-e^{-\Delta v/v_e})$ = 4 830 × (1 − e^{−10.9/2 942}) = **17.8 kg**; with Hall-effect thrusters of Isp 1 700 s, only **3.2 kg**.
2. **Station keeping.** Keeping the stack in its slot for five years needs 5 × 50 = 250 m/s: **72 kg** of xenon at 1 700 s, but **393 kg** of chemical propellant at 300 s — almost the entire life-extension budget. This is why servicers use electric propulsion.
3. **Relocation.** To drift along the GEO arc at 1° per day, the orbit's semi-major axis must change by $\Delta a = \tfrac{2}{3}\,(\dot\lambda/n)\,a$ = 78 km, costing 2.8 m/s to start and 2.8 m/s to stop. Moving 90° to a new client takes three months and about 6 m/s. A single 15-year servicer can therefore serve several clients in turn, as MEV-1 has done.
:::

### Paying to Remove Debris

Debris removal has a harder business case: nobody earns revenue from a dead rocket stage. The Δv to dispose of an object grows with altitude (@fig:adrpropellant). A controlled re-entry — lowering the perigee to about 50 km so that the object falls into an empty ocean area — needs about 177 m/s from 600 km and 240 m/s from 840 km. For a tug of 800 kg, de-orbiting the 3 t H-IIA stage needs about 235 kg of propellant, and a 9 t Soviet-era SL-16 stage about 830 kg, before any margin for a second attempt. One tug can therefore remove one large object, or perhaps a few small satellites — which is why proposals for multi-target removal favour attaching cheap de-orbit kits to several objects in the same orbital plane.

![Disposing of debris. (a) Δv to lower the perigee of an object from a circular orbit, for a controlled re-entry or to accelerate natural decay. (b) Propellant needed by an 800 kg tug to de-orbit four candidate objects with a controlled re-entry.](figures/out/ch40_adr.svg){#fig:adrpropellant width=96%}

Current removal missions are demonstrations funded by space agencies (@tbl:isamcosts): ADRAS-J2 costs about ¥12 billion for one object, and ESA's 2020 contract for ClearSpace-1 was worth €86 million. Studies suggest that removing five to ten of the most dangerous large objects per year would stabilise the LEO population (Chapter 21), which at today's prices means several hundred million dollars a year. Possible funding models include government procurement as a public good, removal fees built into launch licences, and a requirement that new satellites carry a docking plate so that a cheap commercial tug can remove them if they fail.

| Mission or service | Customer | Value | Notes |
|---|---|---|---|
| MEV life extension | Intelsat | ≈ $13 M per year (reported) | Five-year term per client |
| OSAM-1 (cancelled 2024) | NASA | ≈ $1.5 B appropriated; > $2 B estimate | Refuelling and assembly demonstration |
| ADRAS-J2 | JAXA | ≈ ¥12 B (≈ $80 M) | Capture and de-orbit one rocket stage |
| ClearSpace-1 | ESA | €86 M (2020 contract) | Capture and de-orbit PROBA-1 |
| Swift reboost (LINK) | NASA | $30 M | Abandoned 2026 |
| Otter inspection (SSPICY) | NASA | $15 M | Several defunct US satellites |
| Otter de-orbit services | Space Development Agency | $52.5 M | Proliferated LEO constellation |

: Prices and budgets of selected servicing and debris-removal missions. {#tbl:isamcosts}

## Assembling Large Structures in Orbit

### Lessons from the ISS

The ISS is the largest structure ever assembled in space: about 420 t, with a 109 m truss carrying eight pairs of solar wings, built from components launched on more than 40 flights between 1998 and 2011. The Shuttle's arm lifted truss segments out of the payload bay and handed them to Canadarm2, which positioned them for bolting; spacewalkers then connected the power, data and coolant lines that robots could not (@fig:s1truss). Hundreds of hours of spacewalks went into assembly (Chapter 33). The station's design shows what makes assembly possible: standard mechanical interfaces (the segment-to-segment attach system and the common berthing mechanism), structures tested together on the ground before launch wherever possible, and connectors designed for gloved hands or robot end-effectors.

![The Starboard One (S1) truss segment newly installed on the ISS in October 2002, during the STS-112 assembly mission; Canadarm2 is visible at left. Each truss segment was berthed by robotic arms and connected by spacewalkers.](figures/photos/ch40_s1truss.jpg){#fig:s1truss width=56%}

### Beyond the Fairing

Every launch vehicle limits the size of what it carries to the diameter of its fairing — about 5 m for most large rockets, 7 m for New Glenn and 9 m for Starship. Designers escape this limit in three ways (@fig:aperturescale). A **monolithic** mirror must fit inside the fairing: Hubble's and Roman's are 2.4 m. **Folding** gains a factor of one to six: JWST's 6.5 m segmented mirror was folded into a 5.4 m fairing, and the gold-plated mesh reflectors of mobile communication satellites such as TerreStar-1 (18 m) and SkyTerra-1 (22 m), and NISAR's 12 m radar antenna, unfurl like umbrellas. Beyond that, structures must be **assembled**, as the ISS was.

![Aperture size versus launcher. (a) Monolithic, folded and mesh structures stay within a few fairing diameters; only assembly escapes the limit. (b) Equivalent aperture of a telescope assembled from hexagonal segments, versus number of launches, for illustrative packing assumptions.](figures/out/ch40_aperture.svg){#fig:aperturescale width=96%}

Assembly trades launch volume for complexity. In the illustrative case of panel (b), a 20 m telescope needs about four launches of segments in 5 m fairings, or one launch in a 9 m fairing. The challenges lie in precision: mirror segments must be aligned to a few nanometres, so they need actuators and wavefront sensing like JWST's (Chapter 38), and the supporting truss must be stiff and thermally stable. Robotic assembly has been demonstrated on Earth and in small experiments; NASA's in-orbit demonstrations — OSAM-1's SPIDER antenna assembly and OSAM-2's printed beams — were cancelled before flight. NASA's study of the Habitable Worlds Observatory includes standard interfaces and an orbit reachable by servicers, so that instruments could be replaced as Hubble's were. Modular spacecraft with standard mechanical, electrical and data interfaces between their blocks — sometimes called "Lego-like" — are a related idea: a damaged module could be swapped and a new payload added without replacing the whole satellite.

### Space-Based Solar Power

The most ambitious assembly concept is a **space solar power station**, collecting sunlight continuously in GEO and beaming it to Earth as microwaves. The physics sets its scale: to deliver 1 GW with about 10 % end-to-end efficiency from sunlight at 1.36 kW/m² requires a collecting area of about 7 km², and a structure of thousands of tonnes even at 1 kg/m² — far beyond any foldable spacecraft. Caltech's **SSPD-1** demonstrator, launched in January 2023, showed the first steps: its MAPLE experiment, a lightweight array of microwave transmitters steered electronically, beamed power to receivers in orbit and sent a detectable beam to a receiver on the roof of a laboratory at Caltech. Commercial viability would require launch costs, mass per unit area and robotic assembly far beyond today's.

## Manufacturing in Space

### Why Make Things in Orbit?

Manufacturing in orbit offers three things that are hard to obtain on Earth: **weightlessness**, which suppresses buoyant convection and the settling of heavier components, so that crystals grow more evenly and mixtures do not separate; **containerless processing**, in which a liquid can solidify without touching walls that would contaminate or seed it; and an unlimited **high vacuum**. Against these stand the costs of launch and return, a few cubic metres of space on a station, and the need to automate almost everything. In-space manufacturing therefore targets two niches: products so valuable per kilogram that they justify the round trip (@tbl:spacemanufacturing), and parts made in space for use in space, which save the cost of launching spares.

| Product | Why microgravity helps | Status (2026) | Example |
|---|---|---|---|
| Spare parts (polymer) | Print on demand instead of stocking spares | ISS printers since 2014 | Made In Space (Redwire) printers |
| Metal parts | Strong tools and parts for long missions | First metal print 2024 | ESA/Airbus printer in Columbus |
| ZBLAN optical fibre | Less crystallisation, so lower optical loss | > 11 km drawn on ISS (2024) | Flawless Photonics |
| Protein and drug crystals | Larger, more uniform crystals | Routine ISS research; capsule returns | Merck, Varda (ritonavir) |
| Bioprinted tissue | Soft tissue holds shape without scaffolds | Meniscus printed 2023 | Redwire BioFabrication Facility |
| Semiconductor crystals | Purer crystals grown from gas or melt | Furnace operated in orbit 2025 | Space Forge ForgeStar-1 |
| Large structures | Unlimited length; no launch loads | Studies; demos cancelled | OSAM-2 beam printing |

: Candidate products for in-space manufacturing. {#tbl:spacemanufacturing}

### Printing in Orbit

The first 3D printer in space, built by Made In Space for NASA, reached the ISS in 2014 and printed its first part — a faceplate for its own extruder — in November (@fig:zerogprinter). Its test coupons, compared with identical ones printed on the ground, showed that extrusion works normally in weightlessness. Later in 2014 it printed a ratchet wrench from a file sent up from the ground. A commercial printer followed in 2016, and the company, now part of Redwire, printed hundreds of parts. Metal is harder: molten metal must be controlled without gravity, and powder beds cannot be used because loose powder floats. ESA and Airbus's printer, installed in the Columbus module in 2024 (@fig:metalprinter), melts stainless-steel wire with a laser and produced its first part that summer; samples were returned to Earth for testing against parts printed on the ground.

::: figrow
![Barry Wilmore holds a test coupon made by the first 3D printer in space, aboard the ISS in December 2014. Comparing such coupons with identical ones made on the ground showed that printing works in weightlessness.](figures/photos/ch40_printer.jpg){#fig:zerogprinter}

![Jeanette Epps configures the ESA metal 3D printer in the Columbus module in August 2024. It melts stainless-steel wire with a laser inside a sealed chamber.](figures/photos/ch40_metal.jpg){#fig:metalprinter}
:::

### Fibres, Crystals and Tissue

**ZBLAN** is a fluoride glass (named after its zirconium, barium, lanthanum, aluminium and sodium components) that transmits infrared light far better than silica in theory, but on Earth tiny crystals form as it is drawn into fibre, scattering light. In weightlessness, without convection and sedimentation, fewer crystals form. In 2024 the start-up Flawless Photonics drew more than 11 km of ZBLAN fibre on the ISS, the longest run yet; whether its quality justifies the cost of production in orbit is still being assessed.

**Protein crystals** grown in weightlessness are often larger and more regular, which helps determine molecular structures by X-ray diffraction and can improve drug formulation; experiments on the ISS helped Merck develop a more uniform crystalline suspension of its cancer drug pembrolizumab. **Bioprinting** benefits because soft tissues printed from cells and gels do not collapse under their own weight; Redwire's BioFabrication Facility on the ISS printed a human knee meniscus in 2023, a first step towards printing tissues for transplantation.

### Free-Flying Factories

Stations offer crew help but little throughput. **Varda Space Industries** builds small free-flying factories: a satellite bus carries a process module and a re-entry capsule, which returns its product at almost orbital speed and lands under a parachute. W-1 grew crystals of the HIV drug ritonavir and, after months waiting for permission to land, came down in Utah in February 2024 — the first commercial capsule licensed under the US FAA's re-entry rules. Its successors land at the Koonibba Test Range in South Australia: W-2 in February 2025, W-3 in May 2025, W-5 in January 2026 with the first heat shield made entirely of Varda's own carbon ablator, and W-6 in May 2026. Each capsule is also a **hypersonic test bed**, measuring re-entry conditions for the US Air Force and NASA — today a more reliable source of revenue than pharmaceuticals. In the UK, **Space Forge**'s ForgeStar-1, launched in June 2025, ignited a plasma at about 1 000 °C in its miniature furnace in December 2025, a step towards growing semiconductor crystals in orbit and returning them on later missions.

The economics of all these products depends on the price of the round trip. At a rideshare price of a few thousand dollars per kilogram to orbit, plus a capsule and recovery, only products worth hundreds of thousands of dollars per kilogram — drug crystals, seed crystals and specialised fibre — are plausible candidates. Lower launch costs and reusable capsules would widen the range.

## Refuelling for Exploration

Refuelling in orbit matters most for exploration. A rocket that arrives in low Earth orbit has used most of its propellant; if it can be refilled there, it can carry far more payload to the Moon or Mars than its launch vehicle alone could send. Both Artemis landers depend on this: SpaceX's Starship HLS is filled in LEO from a depot ship loaded by a series of tanker launches, and Blue Origin's Blue Moon Mk2 is to be refuelled by a separate transporter vehicle.

Cryogenic propellants make this hard. Liquid oxygen boils at −183 °C and methane at −162 °C, so heat leaking into a tank boils them away continuously — **boil-off** — unless the tank is shaded, insulated or actively cooled. In weightlessness the liquid floats as blobs and does not sit over the outlet, so transfer requires a small settling acceleration or capillary devices; transfer lines must first be chilled, wasting some propellant as gas; and the amount in a tank is hard to measure without gravity. RRM3's methane experiment failed before it could test these effects. In March 2024, on Starship's third flight, SpaceX transferred liquid oxygen between tanks inside one ship. The first ship-to-ship transfer, between two Starships docked in orbit, was planned for no earlier than late 2026; Starship first reached orbit on 28 September 2026. NASA restructured Artemis in 2026 so that Artemis III, in 2027, will rehearse rendezvous and docking with the landers in Earth orbit, with the first landing on Artemis IV.

How many tanker flights a landing needs depends on assumptions that SpaceX has not published in detail. Public estimates range from about 10 (SpaceX) to the "high teens" (NASA officials). @fig:tankerflights shows how the number depends on how much each tanker delivers and how fast the depot loses propellant.

![Propellant transfer for a lunar lander. (a) Tanker flights needed to load the lander, versus propellant delivered per tanker, for different depot boil-off rates. (b) Propellant in the depot during a campaign with one tanker every 6 or 12 days: slower launch rates lose more to boil-off.](figures/out/ch40_tankers.svg){#fig:tankerflights width=96%}

::: example
**Example: how many tankers for a lunar landing?**

Assume (these are not SpaceX figures) a lander of 120 t dry mass carrying 15 t, with Raptor engines of Isp 375 s ($v_e$ = 3 677 m/s). After leaving LEO it needs about 3.6 km/s to reach near-rectilinear halo orbit (NRHO), 2.65 km/s to land and 2.65 km/s to return to NRHO: 8.9 km/s in total.

1. Mass ratio: $e^{8\,900/3\,677}$ = 11.25, so the lander must leave LEO with 135 × 11.25 = 1 518 t, of which **1 383 t** is propellant.
2. If each tanker delivers 100 t, and each transfer (tanker to depot, depot to lander) loses 3 %, the lander needs 1 383 / (0.97 × 0.97 × 100) = 14.7, so **15 tanker flights** with no boil-off.
3. With boil-off of 0.2 % per day in the depot and one tanker every 6 days, the campaign takes **17 flights over 96 days**; at one every 12 days, 18 flights over 204 days. Add the depot and the lander themselves, and a single landing needs about 19–20 launches.
4. If each tanker could deliver 150 t, the count falls to about **11**. The answer is most sensitive to tanker payload and launch rate — which is why rapid reuse is central to the plan.
:::

::: ai
**AI and autonomy for servicing**

Servicing is one of the most demanding applications of space autonomy. Approaching an unprepared, tumbling object requires the servicer to estimate its pose from camera images in real time; convolutional neural networks trained on synthetic images, tested in international satellite pose-estimation competitions run by ESA and Stanford, now estimate pose from a single image, though the gap between rendered training images and real lighting remains the main difficulty. Onboard guidance must decide when to abort — ADRAS-J's autonomous abort in 2024 is an example — and learning-based planners are being studied for grasping tumbling targets and for scheduling multi-client missions. On the ground, machine-learning models monitor the health of the servicer and client and flag anomalies such as unexpected attitude behaviour (Chapters 45 and 46).
:::

::: key
**Key takeaways**

- ISAM spans inspection, relocation, life extension, refuelling, repair, assembly and manufacturing; each step up the ladder adds harder requirements for capture, fluid transfer and dexterity.
- Astronauts serviced Solar Max, Intelsat 603 and Hubble and assembled the ISS; since 2020 commercial robots have docked with satellites as a paid service (MEV-1, MEV-2; MRV and MEPs launched July 2026), and China has towed and probably refuelled satellites in GEO.
- Rendezvous uses V-bar hops and R-bar approaches designed to be passively safe; final approaches are slow — centimetres per second, slower still in GEO — and capture of unprepared or tumbling clients relies on launch-adapter rings, engine nozzles and careful detumbling.
- Life extension pays when a satellite earns more than the roughly $13 million per year fee or when it defers a replacement; debris removal remains a government-funded demonstration market costing about $80–100 million per object.
- Assembly escapes the fairing limit that caps monolithic and folded structures at a few fairing diameters; NASA's robotic assembly demonstrations were cancelled, but the ISS proves the principle.
- Manufacturing in orbit has moved from ISS printers to free-flying factories with return capsules; refuelling in orbit, still undemonstrated between two vehicles, is the key to Artemis landers that need 10–20 tanker flights each.
:::

::: questions
**Review questions**

1. List the main ISAM activities in order of difficulty and explain what each additional step requires of the servicer and the client.
2. Why did servicing Solar Max and Hubble succeed while the first attempts to capture Intelsat 603 failed? What does this imply for designing future satellites?
3. How does the Mission Extension Vehicle attach to a client that was never designed for servicing, and why does it use electric propulsion?
4. Using the Clohessy–Wiltshire equations, calculate the Δv for a 2 km radial hop along the V-bar in a 500 km orbit, and the time it takes.
5. Explain "passive safety" in rendezvous. Why must approaches in GEO be slower than in LEO?
6. A dead satellite with a moment of inertia of 5 × 10⁴ kg·m² tumbles at 2° per second. What is its angular momentum, and how could a servicer remove it after capture?
7. A GEO satellite of 3 000 kg has 80 kg of usable propellant. Estimate its remaining life with chemical thrusters of 290 s, keeping 11 m/s for disposal.
8. Why do debris-removal missions struggle to find a business case, and what funding models have been proposed?
9. Explain why folding structures cannot grow beyond a few fairing diameters, and outline the engineering challenges of assembling a 20 m telescope in orbit.
10. Explain the difficulties of transferring cryogenic propellants in orbit and estimate how the number of tanker flights for a lunar landing changes if each tanker delivers 150 t instead of 100 t.
:::
