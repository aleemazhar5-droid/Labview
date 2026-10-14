---
title: "Spacecraft Subsystems II: Attitude Control, Propulsion, Data Handling and Flight Software"
hero: ch06
abstract: A spacecraft must know which way it is pointing and turn when needed, change its orbit, and think for itself between ground contacts. This chapter explains attitude determination and control - sensors, actuators, disturbance torques and control laws; spacecraft propulsion - cold gas, monopropellant, bipropellant and electric thrusters, feed systems and propellant management; command and data handling - onboard computers, memories, buses and radiation-tolerant electronics; and flight software, autonomy and fault protection.
---

## Attitude Determination and Control

### What the ADCS Does

**Attitude** is the orientation of the spacecraft in space. Almost every mission needs attitude control: cameras must point at their targets, antennas at the Earth, solar arrays at the Sun, radiators away from it, and thrusters along the desired Δv direction. The **attitude determination and control subsystem (ADCS)** — often combined with orbit control as **guidance, navigation and control (GNC)** — measures the attitude with sensors, compares it with the desired attitude, and applies torques with actuators in a feedback loop (@fig:adcsloop).

![The attitude control loop. Sensors feed an estimator (usually a Kalman filter); the controller compares estimated and commanded attitude and commands actuators to produce torques that act, together with disturbances, on the spacecraft dynamics.](figures/out/ch06_adcs_loop.svg){#fig:adcsloop width=96%}

Pointing requirements range enormously:

- **Coarse**: Sun-pointing for power, ±5–10° (safe modes, simple CubeSats).
- **Moderate**: Earth-pointing communications satellites, ±0.05–0.1°.
- **Fine**: Earth-observation imagers, 0.01–0.02° (tens of arcseconds) with stability of a few µrad/s during imaging.
- **Very fine**: space telescopes — Hubble holds its pointing to 0.007 arcsec (7 milliarcseconds) for hours; JWST about the same with a fine-steering mirror.

Requirements distinguish **accuracy** (how close to the target direction), **knowledge** (how well the attitude is known after the fact), **stability** or **jitter** (how much it moves over a short time), and **agility** (how fast it can slew from target to target).

### Stabilisation Methods

- **Spin stabilisation** — the spacecraft spins (typically 5–60 rpm) and behaves like a gyroscope, keeping its spin axis fixed in inertial space. Simple and robust; used by early satellites, many sounding rockets, the Juno spacecraft (spinning at 2–5 rpm) and some upper stages. **Dual-spin** satellites combine a spinning rotor with a de-spun platform for antennas.
- **Gravity-gradient stabilisation** — an elongated spacecraft tends to align its long axis with the local vertical because the near end feels slightly more gravity than the far end. Accuracy is a few degrees; used on early navigation satellites and some small satellites with deployable booms.
- **Passive magnetic stabilisation** — permanent magnets align a CubeSat with Earth's field, with hysteresis rods for damping.
- **Three-axis stabilisation** — active control of all three axes with wheels or thrusters. This is the standard for modern spacecraft.

### Rigid-Body Dynamics

The rotational motion of a rigid spacecraft is governed by **Euler's equation**:

$$\mathbf{I}\,\dot{\boldsymbol\omega} + \boldsymbol\omega \times (\mathbf{I}\,\boldsymbol\omega) = \mathbf{T}_{control} + \mathbf{T}_{disturbance} - \dot{\mathbf{h}}_{wheels} - \boldsymbol\omega\times\mathbf{h}_{wheels}$$

where $\mathbf I$ is the inertia tensor, $\boldsymbol\omega$ the angular velocity, $\mathbf T$ the external torques and $\mathbf h$ the angular momentum stored in internal wheels. Attitude itself is represented with **direction-cosine matrices**, **Euler angles** (intuitive but singular at certain angles — "gimbal lock"), or **quaternions** (four parameters, no singularities, the standard in flight software).

### Disturbance Torques

Small external torques continually push the spacecraft away from its desired attitude (@fig:disturb):

- **Gravity gradient** — $T = \frac{3\mu}{2r^3}|I_z - I_y|\sin 2\theta$, important for large, elongated spacecraft in LEO.
- **Aerodynamic** — drag acting at a centre of pressure offset from the centre of mass; dominant below about 500 km.
- **Solar radiation pressure** — the same offset effect for sunlight; dominant in high orbits and deep space.
- **Magnetic** — interaction of residual magnetic dipoles (from currents and magnetised materials) with Earth's field.
- **Internal** — propellant slosh, moving mechanisms, flexible appendages, outgassing and thruster misalignment.

![Order-of-magnitude disturbance torques on a 1 000 kg spacecraft as a function of altitude. Aerodynamic torque dominates in low orbits; gravity-gradient and magnetic torques in mid-LEO; solar pressure in high orbits.](figures/out/ch06_disturbances.svg){#fig:disturb width=84%}

Because these torques act continuously in one direction, momentum accumulates in the reaction wheels until they approach their maximum speed; it must periodically be "dumped" using magnetorquers or thrusters (**momentum management**).

### Attitude Sensors

Table: Common attitude sensors. {#tbl:sensors}

| Sensor | Measures | Typical accuracy | Notes |
|---|---|---|---|
| Coarse Sun sensor | Sun direction (photodiode currents) | 1–5° | Cheap, robust; used for safe mode |
| Fine (digital) Sun sensor | Sun direction (slit or pinhole on detector array) | 0.01–0.1° | Field of view up to ±64° |
| Earth (horizon) sensor | Direction of Earth's IR limb (14–16 µm CO₂ band) | 0.03–0.3° | Classic for GEO and LEO Earth-pointing |
| Magnetometer | Local magnetic field vector | 0.5–5° (after comparison with field model) | Also used for magnetorquer control |
| Star tracker | Full 3-axis attitude by matching stars to a catalogue | 1–10 arcsec (cross-boresight); ≈ 5–40 arcsec (roll) | The precision sensor of modern spacecraft; blinded by Sun/Moon/Earth |
| Gyroscope / IMU | Angular rate (integrates to attitude change) | Drift from 0.001°/h (HRG, FOG) to 10°/h (MEMS) | Bridges star-tracker outages; ring-laser, fibre-optic, hemispherical resonator, MEMS |
| GNSS receiver | Position, velocity, time (and attitude with several antennas) | Position 1–10 m real-time | Standard in LEO; works up to GEO and beyond with weak-signal receivers |
| Fine guidance sensor | Offset of a guide star in the science telescope focal plane | Milliarcseconds | Hubble FGS, JWST FGS, Roman |

![Typical accuracy ranges of attitude sensors on a logarithmic scale. Star trackers improved attitude knowledge by two to three orders of magnitude over Sun and Earth sensors.](figures/out/ch06_sensor_accuracy.svg){#fig:sensoracc width=90%}

A **star tracker** is a small digital camera with a wide-angle lens (field of view 10–25°) and an onboard catalogue of thousands of stars. A "lost-in-space" algorithm identifies star patterns (triangles or pyramids of stars) without prior knowledge; once locked, it tracks the stars at 1–10 Hz. Modern trackers for small satellites weigh under 300 g; high-end units (e.g., Leonardo's AA-STR, Sodern's Hydra, Ball's CT-2020) serve large missions. Measurements from all sensors are fused by an **extended Kalman filter** (usually a multiplicative quaternion formulation) that also estimates gyro biases.

![Engineers install the star-tracker camera heads on NASA's Europa Clipper before launch (image released by JPL in 2025, when the trackers returned their first in-flight star-field images). Star trackers are the primary attitude sensors of almost every modern three-axis-stabilised spacecraft.](figures/photos/ch06_startrackers.jpg){#fig:startrackers width=78%}

### Attitude Actuators

- **Reaction wheels** — flywheels driven by brushless motors; accelerating a wheel in one direction rotates the spacecraft in the other. They give smooth, precise, propellant-free control. Typical wheels provide 0.01–0.3 N·m of torque and store 0.01 N·m·s (CubeSat wheels) to 200 N·m·s. Four wheels in a skewed pyramid (@fig:wheels) provide full control with one redundant wheel.
- **Momentum wheels** — biased wheels spinning at constant high speed for gyroscopic stiffness about one axis (classic GEO "momentum-bias" designs).
- **Control moment gyroscopes (CMGs)** — constantly spinning wheels whose spin axis is tilted by a gimbal motor. The gyroscopic reaction produces torques hundreds of times larger than a reaction wheel of similar mass, enabling very agile spacecraft (WorldView, Pléiades Neo) and the attitude control of the ISS (four 4 760 N·m·s double-gimbal CMGs).
- **Magnetorquers** — electromagnetic coils or rods that interact with Earth's field ($\mathbf T = \mathbf m \times \mathbf B$); used for momentum dumping and for CubeSat attitude control. They can only produce torque perpendicular to the local field.
- **Thrusters** — produce large torques for slews, momentum dumping and control during orbit manoeuvres; necessary beyond Earth's magnetic field.

![Four reaction wheels in a pyramid arrangement. The configuration tolerates the failure of any one wheel.](figures/out/ch06_wheels.svg){#fig:wheels width=72%}

::: figrow
![The four reaction wheels of Europa Clipper installed on the spacecraft's propulsion module in 2022.](figures/photos/ch06_wheels.jpg){#fig:clipperwheels}

![Astronauts Mike Massimino and James Newman replace a reaction wheel assembly on the Hubble Space Telescope during Servicing Mission 3B in March 2002.](figures/photos/ch06_wheel_eva.jpg){#fig:wheeleva}
:::

::: warning
**Failure lesson — when reaction wheels fail**

Reaction wheels are a classic life-limiting item. NASA's Kepler planet-hunting telescope lost its second of four wheels in 2013 and could no longer point precisely; engineers invented the "K2" mission, balancing the spacecraft against solar radiation pressure, which continued to discover exoplanets for five more years. The Dawn asteroid mission lost two wheels and completed its mission using hydrazine thrusters and careful propellant management. Hubble has had several gyro failures and since 2024 operates in a one-gyro mode to preserve its remaining gyros. Lessons include bearing lubrication, cage instability, conservative speed limits, and designing control modes that work with fewer actuators.
:::

### Control Laws and Modes

Most attitude controllers are variants of **proportional–integral–derivative (PID)** control around each axis, designed with classical frequency-domain margins (typically ≥ 6 dB gain margin and ≥ 30° phase margin) and with filters to avoid exciting flexible modes of solar arrays and antennas. More advanced methods include **linear-quadratic regulators (LQR)**, **model predictive control (MPC)** for constrained slews, and **eigen-axis slews** that rotate about a single axis for time-optimal reorientation.

A spacecraft has several **ADCS modes**: rate damping after separation (often magnetic "B-dot" control on small satellites), Sun acquisition, safe mode, nominal pointing (nadir, target or inertial), slew, orbit-control (thrusting) mode, and momentum-dumping mode. Mode transitions are managed by the flight software and by the fault-protection system.

## Spacecraft Propulsion

### Why Spacecraft Need Propulsion

On-board propulsion provides:

- **Orbit insertion and transfer** — e.g., GTO→GEO, lunar or planetary orbit insertion.
- **Orbit maintenance** — compensating drag in LEO, station-keeping in GEO, constellation phasing.
- **Attitude control and momentum dumping**.
- **Rendezvous, proximity operations and docking**.
- **Collision avoidance**.
- **End-of-life disposal** — de-orbiting within regulatory limits or raising to a graveyard orbit.

Every propulsion system is characterised by two numbers: **thrust** $F$ (newtons) and **specific impulse** $I_{sp}$ (seconds), which measures propellant efficiency:

$$I_{sp} = \frac{F}{\dot m\, g_0} = \frac{v_e}{g_0}$$

where $v_e$ is the effective exhaust velocity. Through the rocket equation, $I_{sp}$ determines how much propellant a given Δv requires (@fig:rocketeq). The landscape of thruster technologies spans eight orders of magnitude in thrust and two in specific impulse (@fig:ispthrust).

![Propellant required as a fraction of initial mass versus Δv for different propulsion technologies. High-Isp electric propulsion makes large Δv missions possible with modest propellant mass, at the cost of very long thrusting times.](figures/out/ch06_rocket_eq.svg){#fig:rocketeq width=84%}

![Operating ranges of in-space propulsion technologies in thrust and specific impulse.](figures/out/ch06_isp_thrust.svg){#fig:ispthrust width=92%}

### Chemical Propulsion

**Cold gas** thrusters simply release compressed gas (nitrogen, xenon, butane) through a nozzle. Isp is only 50–75 s, but they are simple, clean and produce precise small impulses — used on CubeSats and for fine control (Gaia used cold gas micro-thrusters).

**Monopropellant hydrazine** (N₂H₄) has been the standard for satellite attitude and orbit control since the 1970s. Hydrazine decomposes exothermically when it passes over a heated iridium-on-alumina catalyst bed, producing hot ammonia, nitrogen and hydrogen (@fig:monoprop). Thrusters range from 0.5 N to several hundred newtons (Isp 220–235 s). Hydrazine is toxic and carcinogenic, so handling requires protective suits (SCAPE suits) and is expensive. **"Green" monopropellants** — AF-M315E (ASCENT, flown on NASA's Green Propellant Infusion Mission, 2019) and LMP-103S (ammonium dinitramide-based, flown on PRISMA and Skybox/SkySat) — offer higher density-Isp and much safer handling.

![A hydrazine monopropellant thruster system. Propellant flows from a blowdown tank through filters and valves to a catalyst bed where it decomposes; the hot gases expand through a nozzle.](figures/out/ch06_monoprop.svg){#fig:monoprop width=92%}

**Bipropellant** systems burn a fuel (monomethylhydrazine, MMH, or hydrazine) with an oxidiser (nitrogen tetroxide, NTO, or mixed oxides of nitrogen, MON) that ignite spontaneously on contact (**hypergolic**). Isp is 300–330 s. A typical GEO satellite has a 400–500 N **liquid apogee engine** for orbit raising and 10–22 N thrusters for attitude and station-keeping, fed from regulated tanks (@fig:biprop). Planetary orbiters use biprop engines for orbit insertion (e.g., Juno's 645 N Leros-1b). **Dual-mode** systems use hydrazine both as monopropellant for small thrusters and as fuel for a biprop engine.

![A pressure-regulated bipropellant system. Helium from a high-pressure tank is regulated to constant pressure and pushes fuel and oxidiser to the engines.](figures/out/ch06_biprop.svg){#fig:biprop width=92%}

**Solid rocket motors** provide a single, large impulse — historically used as apogee kick motors and for planetary orbit insertion, and still common in upper stages.

### Feed Systems and Propellant Management

Propellant can be fed by **blowdown** (pressurant in the same tank; pressure and thrust fall as the tank empties — simple, typical of LEO satellites) or **pressure regulation** (constant pressure from a separate high-pressure tank — needed for biprop engines with tight mixture-ratio control). Large launch-vehicle stages use pumps (Chapter 35).

In microgravity, liquid does not settle at the tank outlet. **Propellant management devices (PMDs)** — surface-tension vanes, sponges, galleries and screens — or **elastomeric diaphragms and bladders** keep gas-free liquid at the outlet. Alternatively, a small "ullage" burn settles the propellant before a main burn. **Propellant gauging** is difficult in weightlessness and uses bookkeeping (counting thruster pulses), pressure–volume–temperature methods, or the thermal response of the tank to heating.

### Electric Propulsion

**Electric propulsion (EP)** uses electrical energy to accelerate propellant to much higher exhaust speeds than chemical reactions allow — 15–50 km/s instead of 3–4.5 km/s. Thrust is tiny (millinewtons to a few newtons) because it is limited by available power:

$$F = \frac{2\,\eta\,P}{v_e} = \frac{2\eta P}{g_0 I_{sp}}$$

so a 5 kW Hall thruster at 60 % efficiency and 1 800 s produces about 0.34 N. The main types (@fig:ionhall) are:

- **Electrothermal** — resistojets and arcjets heat propellant electrically (Isp 300–800 s); used for GEO station-keeping in the 1990s.
- **Gridded ion engines** — xenon is ionised in a discharge chamber and accelerated through electrically charged grids; a neutraliser emits electrons to keep the spacecraft neutral. Isp 2 500–4 500 s. Flown on Deep Space 1, Hayabusa 1 and 2, Dawn (three NSTAR engines, total Δv ≈ 11 km/s — a record), BepiColombo (four T6 engines), DART (NEXT-C) and Boeing 702 GEO satellites (XIPS).
- **Hall-effect thrusters** — a radial magnetic field traps electrons in an annular channel, creating an axial electric field that accelerates ions. Isp 1 200–2 800 s, higher thrust per kW than ion engines. They are by far the most widely flown EP technology: Starlink uses krypton and (V2 Mini onwards) argon Hall thrusters on every satellite; the 6 kW-class units power Psyche (SPT-140) and all-electric GEO satellites; 12 kW AEPS thrusters were developed for the Gateway Power and Propulsion Element.
- **Electrospray and field-emission (FEEP)** thrusters accelerate ions or charged droplets from liquid metals or ionic liquids, giving micronewton thrust for precise control (LISA Pathfinder) and compact CubeSat propulsion.
- **Pulsed plasma thrusters** ablate a Teflon block with an electric arc — simple, used on small satellites.
- **Advanced concepts** (VASIMR, magnetoplasmadynamic thrusters, nuclear electric propulsion) are covered in Chapter 42.

![Principles of gridded ion and Hall-effect thrusters. Both ionise a noble gas and accelerate the ions electrostatically; a cathode neutralises the beam.](figures/out/ch06_ion_hall.svg){#fig:ionhall width=96%}

::: data
**Data box — propellants for electric propulsion**

- **Xenon**: heavy, easily ionised, inert, stores densely at high pressure (≈ 1.5 g/cm³ at 80–150 bar). Expensive (US$ 3 000–20 000/kg depending on market; prices spiked in 2022).
- **Krypton**: about 10× cheaper than xenon, slightly lower thrust efficiency; used by Starlink V1.
- **Argon**: cheaper still; adopted by Starlink V2 Mini thrusters (≈ 2.4× more thrust and 1.5× more Isp than the earlier krypton thrusters, according to SpaceX).
- **Iodine**: stored as a solid at low pressure — no high-pressure tanks; first flown by ThrustMe on Beihangkongshi-1 in 2020.
- **Water** and other condensables for electrothermal and microwave thrusters on small satellites.
:::

### Choosing a Propulsion System

The choice depends on the Δv required, the time available, the power available, cost and safety. Rules of thumb: small LEO satellites needing < 100 m/s use cold gas, green monopropellant or electric propulsion; GEO satellites increasingly use all-electric or hybrid architectures; deep-space missions with large Δv use ion or Hall thrusters if solar power is sufficient; planetary orbit insertion and landing need chemical thrust. Mega-constellations have made Hall thrusters a mass-produced commodity: SpaceX alone has built more electric thrusters than the rest of the world combined.

## Command and Data Handling

### Functions and Architecture

The **command and data handling (C&DH)** subsystem — **on-board data handling (OBDH)** in European terminology — is the spacecraft's nervous system. It receives and validates commands, distributes them to subsystems, runs the flight software, keeps time, collects housekeeping telemetry and payload data, stores data in mass memory, formats it for downlink, and supervises the health of the spacecraft (@fig:cdh).

![A typical C&DH architecture: a redundant onboard computer connected through a platform bus to remote interface units and GNC equipment, a high-rate network to the payload and mass memory, and a link to the TT&C transponders.](figures/out/ch06_cdh.svg){#fig:cdh width=96%}

Architectures may be **centralised** (one computer does everything — common on small satellites), **federated** (separate computers for GNC, payload and platform), or **distributed/integrated modular avionics** (partitioned software on shared processors connected by deterministic networks, now common on human spacecraft and large platforms).

### Data Buses and Networks

Table: Common spacecraft data bus and network standards. {#tbl:databuses}

| Standard | Data rate | Typical use |
|---|---|---|
| MIL-STD-1553B | 1 Mbit/s, dual-redundant, command/response | Military and NASA platforms, ISS, Orion |
| CAN (and CANopen / CubeSat Space Protocol) | up to 1 Mbit/s | Small satellites, ESA platforms (ECSS-E-ST-50-15C) |
| RS-422 / RS-485, I²C, SPI | kbit/s–tens of Mbit/s | Simple point-to-point and board-level links |
| SpaceWire (ECSS-E-ST-50-12C) | 2–400 Mbit/s, packet-switched | Instrument and mass-memory networks (JWST, Gaia, many ESA/NASA/JAXA missions) |
| SpaceFibre | 2.5–6.25 Gbit/s per lane, multi-lane | High-rate payloads (SAR, hyperspectral) |
| Time-Triggered Ethernet / TSN | 100 Mbit/s–10 Gbit/s, deterministic | Orion, Gateway, launch vehicles, next-generation platforms |
| SpaceVPX / VITA standards | Backplane | Modular payload processors |

### Processors and Memory

Spacecraft computers lag their terrestrial counterparts by 10–20 years in performance because they must tolerate radiation (Chapter 2) and are qualified slowly (@fig:processors). The **BAE Systems RAD750**, a radiation-hardened PowerPC first flown in 2005, has powered more than 150 missions including Curiosity, Perseverance, JWST and Juno, at about 200–260 MIPS. European missions use **LEON** SPARC processors (GR712RC dual-core, GR740 quad-core). NASA's **High-Performance Spaceflight Computing (HPSC)** project with Microchip is producing a radiation-hardened multicore RISC-V processor (PIC64-HPSC) with roughly 100 times the performance of the RAD750, available to missions from about 2025–2026.

![Approximate integer performance of spaceflight processors over time. Commercial processors with radiation mitigation (e.g., the Snapdragon on the Ingenuity Mars helicopter) offer orders-of-magnitude more performance than rad-hard parts but less proven reliability.](figures/out/ch06_processors.svg){#fig:processors width=90%}

A widening alternative is to fly **commercial (COTS)** processors, FPGAs and GPUs with **mitigation**: screening and radiation testing, triple modular redundancy in FPGA logic, watchdogs, error-correcting memory, current-limited power with automatic latch-up recovery, and frequent memory scrubbing. Short-duration LEO missions, mega-constellations and technology demonstrations increasingly use this approach — the Ingenuity helicopter on Mars ran on a Qualcomm Snapdragon 801 smartphone processor for nearly three years. Reconfigurable **FPGAs** (e.g., AMD/Xilinx Kintex UltraScale and Versal space-grade parts, Microchip RTG4 and RT PolarFire) process high-rate payload data and run neural networks (Chapter 43).

**Memory** must cope with single-event upsets. Program memory is often in radiation-tolerant PROM, MRAM or protected Flash; working memory in SDRAM with **error detection and correction (EDAC)** that corrects single-bit errors and detects double-bit errors, continuously **scrubbed** in the background. Mass memories use NAND Flash with file systems (CCSDS File Delivery Protocol for ground transfer) and capacities from gigabits on CubeSats to tens of terabits on Earth-observation satellites.

### Time

The C&DH maintains **onboard time**, synchronised to UTC or GPS time via GNSS or ground correlation, to time-tag telemetry and to execute **time-tagged commands** stored in an onboard schedule. Earth-observation and science missions need time knowledge to microseconds; navigation satellites carry atomic clocks with nanosecond precision (Chapter 18).

## Flight Software

### Architecture

Flight software (FSW) has grown from a few kilobytes on early spacecraft to millions of lines of code (Orion ≈ 2 million; the F-35 fighter about 8 million; Starlink satellites run Linux). Good FSW is layered (@fig:fswlayers): a hardware abstraction layer and drivers; a **real-time operating system** (RTEMS, VxWorks, FreeRTOS, or Linux with real-time extensions); a reusable framework — such as NASA's **core Flight System (cFS)**, JPL's **F Prime** (used on Ingenuity and many CubeSats) or ESA's component-based frameworks — providing a software bus, time, event logging and table services; and mission applications on top.

![Layered flight-software architecture. A framework such as NASA's cFS or JPL's F Prime separates mission applications from the operating system and hardware.](figures/out/ch06_fsw_layers.svg){#fig:fswlayers width=94%}

### Development and Assurance

Because flight software controls the whole spacecraft and can be the cause of mission loss, it is developed under strict processes: coding standards (e.g., MISRA C, JPL's "Power of Ten" rules: no recursion, no dynamic memory allocation after initialisation, bounded loops, assertions), static analysis, unit and integration tests, hardware-in-the-loop testing on flight-like testbeds ("flatsats"), and **independent verification and validation (IV&V)** for high-criticality software. Most modern spacecraft can be **reprogrammed in flight** — a capability that has rescued many missions.

::: warning
**Failure lesson — software can end a mission in seconds**

On its maiden flight in 1996, Ariane 5 broke up 37 seconds after lift-off because inertial-reference software reused from Ariane 4 converted a 64-bit floating-point horizontal velocity into a 16-bit integer, causing an overflow that shut down both (identical) inertial units. In 2016 the Japanese X-ray observatory Hitomi was destroyed when an incorrect parameter uploaded to its attitude-control software, combined with a star-tracker anomaly, caused it to spin up until it broke apart. In 2023 the ispace HAKUTO-R lander crashed on the Moon after its software rejected valid altimeter data as faulty while passing over a crater rim. Each case shows the importance of verifying software against realistic, end-to-end scenarios — including "off-nominal" ones.
:::

### Autonomy and Fault Protection

Spacecraft are out of contact much of the time — a LEO satellite sees a given ground station for only about 10 minutes per pass, and a Mars rover's commands take 5–22 minutes to arrive. They therefore need **autonomy**: the ability to execute plans, react to events and protect themselves.

**Fault detection, isolation and recovery (FDIR)** — called fault protection at NASA — is organised hierarchically (@fig:fdir). Faults are handled at the lowest level possible: a memory bit-flip is corrected by EDAC, a failed unit is replaced by its redundant twin, a subsystem anomaly triggers a mode change, and if all else fails the spacecraft enters **safe mode** — pointing its solar arrays at the Sun, switching off non-essential loads, and waiting for instructions from the ground. Safe modes must be simple, robust, and independent of the failed hardware (many spacecraft have a separate "survival" computer or hardware-implemented safe mode).

![The hierarchy of fault detection, isolation and recovery. Fast local responses handle simple faults; system-level safe mode and ground intervention handle complex ones.](figures/out/ch06_fdir.svg){#fig:fdir width=82%}

Higher levels of autonomy — onboard planning and scheduling, autonomous navigation, opportunistic science and model-based diagnosis — are increasingly implemented with artificial intelligence techniques, discussed in depth in Chapter 45.

::: key
**Key takeaways**

- The ADCS determines and controls attitude with sensors (star trackers, gyros, Sun sensors, magnetometers, GNSS) and actuators (reaction wheels, CMGs, magnetorquers, thrusters) in a Kalman-filter-based feedback loop; momentum must be managed against persistent disturbance torques.
- Propulsion is characterised by thrust and Isp: chemical systems (cold gas 70 s, hydrazine 225 s, biprop 320 s) give high thrust; electric propulsion (Hall 1 200–2 800 s, ion 2 500–4 500 s) gives high efficiency at low thrust and is now standard on constellations and many GEO and deep-space missions.
- Microgravity requires propellant management devices; feed systems are blowdown or pressure-regulated.
- C&DH uses radiation-hardened or mitigated commercial processors, EDAC-protected memory and deterministic buses (1553, CAN, SpaceWire, TSN); rad-hard processors lag commercial ones by a decade or more.
- Flight software is layered (RTOS + framework + applications), rigorously verified and reprogrammable; hierarchical FDIR and safe modes protect the spacecraft between ground contacts.
:::
