---
title: "Spacecraft Subsystems I: Structures, Thermal Control, Power and Mechanisms"
hero: ch05
abstract: Every spacecraft, whatever its mission, needs a skeleton to carry it through launch, a way to keep its parts at safe temperatures, a source of electrical power, and mechanisms that release, deploy and point. This chapter explains how structures are designed and built, how thermal control works with insulation, radiators, heat pipes and heaters, how solar arrays, batteries and radioisotope generators produce and store power, and how mechanisms are made reliable in vacuum.
---

## The Spacecraft Bus

A spacecraft consists of a **payload**, which performs the mission, and a **bus** (or **platform**), which supports the payload. The bus is divided into **subsystems** (@tbl:subsystems). This chapter covers the "physical" subsystems — structures and mechanisms, thermal control, and electrical power. Chapter 6 covers attitude control, propulsion, data handling and flight software, and Chapter 7 covers communications.

Table: The subsystems of a spacecraft bus and their main functions. {#tbl:subsystems}

| Subsystem | Main functions | Key components |
|---|---|---|
| Structure and mechanisms | Carry loads, provide mounting, maintain alignment; release, deploy and point | Primary/secondary structure, adapters, hinges, release devices, drive mechanisms |
| Thermal control (TCS) | Keep every unit within its allowed temperature range | MLI blankets, coatings, radiators, heat pipes, heaters, louvres, thermostats |
| Electrical power (EPS) | Generate, store, regulate and distribute power | Solar arrays or RTGs, batteries, regulators, power distribution |
| Attitude determination and control (ADCS / GNC) | Know and control orientation (and position) | Sensors (star trackers, gyros, Sun sensors), actuators (wheels, thrusters, magnetorquers) |
| Propulsion | Change orbit, maintain orbit, control attitude, de-orbit | Thrusters, tanks, valves, feed system, electric thrusters |
| Command and data handling (C&DH / OBDH) | Process commands, run software, collect and store data | Onboard computer, mass memory, data buses, remote interface units |
| Telemetry, tracking and command (TT&C) and payload data | Link to ground for control and data | Transponders, antennas, high-rate transmitters, optical terminals |
| Flight software (FSW) | Autonomy, control laws, fault protection, payload operations | Operating system, application software, FDIR |

## Structures

### Functions and Requirements

The structure carries all the spacecraft's equipment through launch, holds instruments in precise alignment in orbit, and often contributes to thermal control and radiation shielding. The **primary structure** carries the main loads from the launch-vehicle interface; **secondary structures** (brackets, panels, booms) carry individual units; **tertiary structures** include cable trays and small supports.

Structural design is driven by:

- **Strength** — the structure must not yield or break under launch loads multiplied by **factors of safety** (typically 1.1–1.25 against yield and 1.25–1.4 against ultimate for flight hardware that is tested; higher for untested designs or pressure vessels).
- **Stiffness** — the fundamental natural frequencies must exceed launcher requirements (e.g., > 20 Hz axial and > 10 Hz lateral for many launchers) to avoid dynamic coupling. Stiffness, not strength, usually sizes the structure.
- **Stability** — dimensional stability under temperature changes and moisture release, which is critical for telescopes and antennas (alignment tolerances of micrometres).
- **Mass** — every kilogram costs launch capacity; structures are typically 15–25 % of dry mass.
- **Interfaces** — standard launch-vehicle adapters (e.g., 937 mm, 1 194 mm, 1 666 mm clamp-band diameters) and CubeSat deployer rails.

### Configurations

@fig:structures shows the three most common configurations. Large GEO platforms use a **central thrust cylinder** (often carbon-fibre) that carries the propellant tanks and transfers loads to the adapter, with honeycomb **shear panels** and equipment panels. Small and medium satellites use **box structures** of bolted honeycomb panels. Stations and very large antennas use **trusses**. Mega-constellation satellites such as Starlink use flat-packed designs that stack dozens of satellites inside a fairing, with the stack itself carrying launch loads.

![Common spacecraft structural configurations: central cylinder with shear panels, box/panel structure, and truss.](figures/out/ch05_structures.svg){#fig:structures width=92%}

![The primary structure of NASA's MAVEN Mars orbiter during assembly at Lockheed Martin. The central core carries the propellant tanks and transmits launch loads to the launch-vehicle adapter.](figures/photos/ch05_maven.jpg){#fig:maven width=58%}

### Materials

Aluminium alloys remain the workhorse of spacecraft structures — cheap, easy to machine and well characterised. Titanium is used for highly loaded fittings and for its low thermal conductivity; carbon-fibre reinforced polymers (CFRP) give the highest stiffness per unit mass and near-zero thermal expansion, ideal for optical benches and antenna reflectors; beryllium offers extreme stiffness for lightweight mirrors (JWST); Invar and Super-Invar give dimensional stability (@fig:materials). Additive manufacturing (3-D printing) of titanium, aluminium and polymer parts is now routine, allowing topology-optimised brackets that are 30–60 % lighter than machined parts (Chapter 52).

![Specific stiffness and specific strength of common spacecraft structural materials. Composites and beryllium dominate where stiffness per kilogram matters most.](figures/out/ch05_materials.svg){#fig:materials width=88%}

### Sandwich Panels

The most common structural element is the **honeycomb sandwich panel** (@fig:sandwich): two thin face sheets bonded to a lightweight honeycomb core. Like an I-beam, the faces carry bending stresses while the core keeps them apart and carries shear. Equipment is attached with **potted inserts**. Embedded heat pipes can be bonded inside panels to spread heat.

![Construction of a honeycomb sandwich panel. Separating the face sheets with a light core increases bending stiffness roughly with the square of the core thickness.](figures/out/ch05_sandwich.svg){#fig:sandwich width=86%}

### Structural Analysis

Structures are analysed with the **finite-element method (FEM)**, using codes such as NASTRAN, Abaqus or ANSYS. The main analyses are:

1. **Modal analysis** — natural frequencies and mode shapes.
2. **Coupled loads analysis (CLA)** — the launcher provider combines the spacecraft model with the launcher model and simulates flight events (lift-off, transonic buffet, engine cut-off, stage separation) to predict the real loads at each interface.
3. **Stress analysis** — margins of safety for every part:

$$MS = \frac{\text{allowable stress}}{\text{FS} \times \text{applied stress}} - 1 \geq 0$$

4. **Thermo-elastic analysis** — distortion caused by temperature changes, critical for pointing and optical alignment.
5. **Fracture control** — for pressure vessels and fracture-critical parts, demonstration that a crack of detectable size will not grow to failure within four lifetimes.

## Thermal Control

### Why Temperature Matters

Each component has an **operational temperature range** and a wider **survival range** (@tbl:temps). The thermal control subsystem (TCS) must keep every unit within these limits during all mission phases — launch, eclipse, hot and cold attitudes, safe mode, and end of life — despite the large external variations described in Chapter 2.

Table: Typical allowed temperature ranges of spacecraft components. {#tbl:temps}

| Component | Operating range (°C) | Notes |
|---|---|---|
| Li-ion batteries | 0 to +30 (charging), −20 to +40 (discharge) | Narrow range; usually the TCS design driver |
| General electronics | −20 to +50 | Reliability falls ≈ 2× per 10 °C rise |
| Solar arrays | −150 to +110 | Efficiency falls as temperature rises |
| Hydrazine propellant and lines | +7 to +50 | Must not freeze (+2 °C) |
| Reaction wheels / bearings | −10 to +40 | Lubricant viscosity |
| Infrared detectors (HgCdTe) | −233 to −173 (40–100 K) | Cryocoolers or passive radiators |
| Optical structures | ± 0.1–1 °C stability | Thermal distortion budget |
| CCD/CMOS visible detectors | −40 to +20 | Cooler = lower dark current |

### Passive Thermal Control

Most thermal control is **passive** — it uses no moving parts or power:

- **Surface finishes** set the balance between absorbed sunlight and emitted infrared (the α/ε ratio, Chapter 2): white paints and optical solar reflectors (OSRs — silvered quartz tiles, α ≈ 0.08, ε ≈ 0.8) on radiators; low-emittance gold or aluminium surfaces where heat must be retained.
- **Multi-layer insulation (MLI)** blankets (@fig:mli) are the "thermos flask" of spacecraft: many thin layers of aluminised polymer film separated by netting, each layer radiating only to its neighbours. MLI reduces radiative heat flow by a factor of 30–100 compared with a bare surface. The gold-coloured "foil" seen on most spacecraft is the outer Kapton layer of MLI.
- **Radiators** — surfaces with high ε and low α, oriented away from the Sun (and often Earth), that reject waste heat to space (@fig:radiator). The required area is $A = Q / (\varepsilon\sigma(T^4 - T_{sink}^4))$.
- **Conductive paths** — doublers, thermal straps, interface fillers and isolators control where heat flows.
- **Heat pipes** (@fig:heatpipe) — sealed tubes containing a working fluid (usually ammonia) that evaporates at the hot end and condenses at the cold end, with capillary wicks or grooves returning the liquid. They transport hundreds of watts across a spacecraft with only a few degrees of temperature drop. **Loop heat pipes** extend this over metres with flexible lines; **variable-conductance heat pipes** regulate temperature automatically using a non-condensable gas reservoir.

![Construction of a multi-layer insulation blanket. Effective emittances of 0.01–0.05 are typical for real installations, limited by seams, penetrations and compression.](figures/out/ch05_mli.svg){#fig:mli width=92%}

![Principle of a heat pipe. Vapour carries heat from the evaporator to the condenser; capillary forces in the wick return the liquid without pumps.](figures/out/ch05_heatpipe.svg){#fig:heatpipe width=92%}

![Heat rejected per square metre by a radiator with ε = 0.85 as a function of its temperature, for three effective sink temperatures. Warmer radiators are smaller, which is why electronics are allowed to run warm when possible.](figures/out/ch05_radiator.svg){#fig:radiator width=82%}

::: figrow
![Radiator panels of the ISS P6 truss photographed during STS-114 in 2005. The station's external active thermal control system pumps ammonia through radiators totalling more than 1 000 m².](figures/photos/ch05_radiator.jpg){#fig:issradiator}

![Damage to a multi-layer insulation blanket on the exterior of the ISS Zarya module, photographed during an Expedition 15 spacewalk in 2007. MLI is lightweight but fragile; outer layers are chosen to resist ultraviolet light, atomic oxygen and handling.](figures/photos/ch05_mli.jpg){#fig:mlidamage}
:::

### Active Thermal Control

Where passive methods are not enough, **active** methods add control:

- **Electric heaters** (Kapton film heaters with thermostats or software control) keep batteries, propellant lines and electronics above minimum temperatures during eclipses and cold attitudes. Heater power is a significant item in the power budget, particularly in safe mode.
- **Louvres** — blinds driven by bimetallic springs that open over radiators when the spacecraft is hot and close when cold (used on Rosetta and many science missions).
- **Mechanically pumped fluid loops** — pumps circulate a coolant (e.g., ammonia, Freon, water in pressurised modules) to carry large heat loads to radiators. The ISS rejects up to 70 kW; Mars rovers use fluid loops to carry heat from their RTG.
- **Cryocoolers** — Stirling, pulse-tube, Joule–Thomson or turbo-Brayton coolers that cool infrared detectors to 4–150 K. JWST's MIRI instrument uses a pulse-tube/Joule–Thomson cryocooler to reach 6.7 K.
- **Thermoelectric coolers** (Peltier devices) for small detectors.

### Thermal Analysis

The TCS is designed with a **thermal mathematical model**: the spacecraft is divided into hundreds or thousands of "nodes" connected by conductive and radiative couplings. Tools such as ESATAN-TMS, Thermal Desktop/SINDA and Systema compute the radiative view factors and orbital heat inputs, then solve the energy balance

$$m_i c_i \frac{dT_i}{dt} = Q_{ext,i} + Q_{int,i} + \sum_j G_{ij}(T_j - T_i) + \sum_j \sigma R_{ij}(T_j^4 - T_i^4)$$

for each node $i$, over hot-case and cold-case scenarios (combinations of end-of-life coatings, maximum dissipation, solstice/equinox, attitudes). Predictions carry **uncertainty margins** (typically ±10–15 °C before thermal balance test correlation, ±5 °C after) so that the hardware is qualified beyond the predicted extremes.

## Electrical Power

### Power System Architecture

The electrical power subsystem (EPS) generates, stores, conditions and distributes power (@fig:powerarch). A typical small satellite needs 50–500 W; a large Earth-observation satellite 2–5 kW; a modern high-throughput GEO communications satellite 15–25 kW; the ISS about 120 kW (after the iROSA upgrade, up to 215 kW of array capacity).

![Architecture of a spacecraft electrical power system. Solar array power is regulated onto a main bus that charges the battery and supplies the loads through a protected distribution unit and point-of-load converters.](figures/out/ch05_power_arch.svg){#fig:powerarch width=96%}

Two families of regulation exist:

- **Direct energy transfer (DET)** — the array is connected directly (through shunt regulators) to the bus. Simple, efficient and common on GEO platforms (sequential switching shunt regulators, S3R) with regulated 50 V or 100 V buses.
- **Peak power tracking (MPPT)** — a DC/DC converter continuously adjusts the array operating point to its maximum power point (@fig:iv). This extracts 10–25 % more power when the array is cold or illuminated at varying angles — common in LEO and on CubeSats.

Buses may be **regulated** (fixed voltage) or **unregulated** (voltage follows battery state of charge, typically 22–36 V). Larger spacecraft use higher voltages (100 V on GEO platforms, 120–160 V on the ISS) to reduce current and harness mass; the Lunar Gateway's Power and Propulsion Element was designed for 120 V to feed 50 kW-class Hall thrusters.

### Solar Arrays

Photovoltaic **solar cells** convert sunlight into electricity. Early satellites used silicon cells of about 10 % efficiency; modern space cells are **multi-junction** gallium-arsenide-based devices stacking three or four semiconductor layers, each absorbing a different part of the spectrum, reaching **30–33 %** efficiency at beginning of life under the space (AM0) spectrum (@fig:solareff). Cost-sensitive mega-constellations often use silicon or other lower-cost cells instead.

![Evolution of the efficiency of flight-qualified space solar cells. Multi-junction III–V cells now exceed 30 %.](figures/out/ch05_solar_eff.svg){#fig:solareff width=86%}

![Current–voltage characteristics of a triple-junction cell at three temperatures. The maximum power point lies at the "knee" of the curve; heating reduces the voltage and the power.](figures/out/ch05_iv.svg){#fig:iv width=82%}

Array output at end of life (EOL) is estimated as

$$P_{EOL} = S\,\eta_{cell}\,A_{cells}\,\cos\theta\;\cdot\;F_{packing}\,F_{temp}\,F_{assembly}\,(1 - d)^{L}$$

where $\theta$ is the Sun incidence angle, $F$ terms account for packing factor (≈ 0.85–0.9), temperature and assembly losses, and $d$ is the annual degradation from radiation, UV and micrometeoroids (typically 1–3 % per year in LEO; more in MEO). Arrays are sized for EOL conditions at the worst season (aphelion in July: 1 316 W/m²).

**Array types:**

- **Body-mounted** cells on the spacecraft surface — simple, used on spinning and very small satellites.
- **Rigid deployable panels** — honeycomb panels hinged together, rotated to track the Sun by a **solar array drive assembly (SADA)**.
- **Flexible / roll-out arrays** — thin blankets on booms. The **Roll-Out Solar Array (ROSA)** and its ISS version **iROSA** (≈ 20 kW each, six installed 2021–2023, more delivered later) are lighter and more compact than rigid panels.
- **Concentrator arrays** — lenses or mirrors focus sunlight on fewer cells (e.g., Deep Space 1).

![Spacewalkers install an ISS Roll-Out Solar Array (iROSA) in December 2022. Each iROSA unrolls from a compact canister into a 6 × 19 m flexible wing over the station's original arrays.](figures/photos/ch05_irosa.jpg){#fig:irosa width=86%}

Solar power falls with the square of the distance from the Sun (@fig:solardist). NASA's Juno is the farthest solar-powered spacecraft (Jupiter, 5.2 AU), using three 9-metre wings that produce about 14 kW at Earth but only about 500 W at Jupiter. ESA's JUICE and NASA's Europa Clipper are also solar-powered at Jupiter, with arrays of 85 m² and about 100 m² respectively. Lucy uses two 7.3 m circular "UltraFlex" arrays to reach Jupiter's Trojan asteroids.

![Solar irradiance versus distance from the Sun. At Jupiter sunlight is 27 times weaker than at Earth; at Saturn about 90 times.](figures/out/ch05_solar_distance.svg){#fig:solardist width=84%}

### Batteries

Batteries supply power during eclipses, launch, peak loads and emergencies. **Lithium-ion** cells have replaced older nickel-cadmium (Ni-Cd) and nickel-hydrogen (Ni-H₂) technologies since the early 2000s because of their two to four times higher specific energy (@fig:batteries). Battery packs are built from many small commercial-format cells (e.g., 18650 cylindrical cells) or larger prismatic cells, arranged in series strings (for voltage) and parallel strings (for capacity and redundancy).

![Specific energy and energy density of space battery chemistries. Li-ion cells made rechargeable storage several times lighter than nickel-based batteries.](figures/out/ch05_batteries.svg){#fig:batteries width=86%}

Battery life depends strongly on the **depth of discharge (DoD)** in each cycle (@fig:dod). A LEO satellite cycles about 5 500 times per year, so its batteries are typically limited to 15–30 % DoD; a GEO satellite cycles only 90 times per year (during two eclipse seasons) and can use 60–80 % DoD. Battery capacity is sized as

$$C = \frac{P_{eclipse}\;t_{eclipse}}{\text{DoD}\;\eta_{discharge}\;N_{strings,\,usable}/N_{strings}}$$

![Illustrative cycle life of Li-ion cells versus depth of discharge. Low-orbit satellites use shallow discharges because they cycle many thousands of times.](figures/out/ch05_dod.svg){#fig:dod width=82%}

![Power generation, load and battery state of charge over two orbits for a LEO satellite. The battery charges in sunlight and supplies the load in eclipse; the array must be sized to recharge it within the sunlit part of each orbit.](figures/out/ch05_orbit_power.svg){#fig:orbitpower width=88%}

::: example
**Worked example — sizing a LEO power system**

A satellite in a 600 km orbit (period 96.7 min, maximum eclipse 35.5 min) needs 400 W continuously.

*Battery:* energy in eclipse = 400 W × 35.5/60 h = 237 Wh. With 25 % DoD and 95 % discharge efficiency, plus one failed string out of five: $C = 237/(0.25\times0.95\times0.8) = 1\,250$ Wh — about 7 kg of Li-ion cells at 180 Wh/kg cell level.

*Array:* in sunlight (61.2 min) the array must supply the load and recharge 237 Wh / (charge efficiency 0.9) = 263 Wh, so it needs $400 + 263/(61.2/60) = 658$ W at EOL. With 30 % cells, a packing factor of 0.88, 0.85 for temperature and other losses, 10 % degradation over 7 years and an average cosine loss of 0.9, each square metre gives $1\,361\times0.30\times0.88\times0.85\times0.9\times0.9 = 247$ W, so about **2.7 m²** of array is needed, plus margin.
:::

### Radioisotope Power

Beyond Jupiter, in permanent shadow, or on planetary surfaces with long nights and dust, spacecraft use **radioisotope power systems (RPS)**. A **radioisotope thermoelectric generator (RTG)** converts the heat of plutonium-238 decay into electricity using thermocouples (@fig:rtg). Pu-238 is used because it emits mainly alpha particles (easily shielded) and has an 87.7-year half-life. RTGs have powered Pioneer 10/11, Voyager 1/2 (still operating after 49 years, though at reduced power), Galileo, Cassini, New Horizons, Curiosity and Perseverance; NASA's Dragonfly rotorcraft (launch 2028) will use one on Titan.

![Schematic of a Multi-Mission RTG. Heat from plutonium dioxide fuel flows through thermoelectric couples to radiator fins; about 6 % of it becomes electricity.](figures/out/ch05_rtg.svg){#fig:rtg width=86%}

![The Multi-Mission Radioisotope Thermoelectric Generator (MMRTG) for the Mars 2020 Perseverance rover during testing at Idaho National Laboratory.](figures/photos/ch05_mmrtg.jpg){#fig:mmrtgphoto width=50%}

Smaller **radioisotope heater units (RHUs)**, each producing about 1 W of heat from 2.7 g of PuO₂, keep components warm on many missions (e.g., Mars rovers Sojourner–Opportunity, Chang'e 3/4 landers, which used Chinese-made RHUs). Russia and China use Pu-238 and Po-210 heaters. Future systems aim at higher efficiency: Stirling convertors (≈ 25–30 %), the next-generation RTG with skutterudite couples, and americium-241 RTGs under development in Europe. For high power, **fission reactors** — such as NASA's Kilopower/KRUSTY demonstration (2018) and the Fission Surface Power project targeting a lunar reactor of at least 40 kW (and, under 2025 direction, 100 kW-class) by about 2030 — are being developed for lunar bases and nuclear electric propulsion (Chapter 42).

### Power Distribution and Protection

The **power distribution unit (PDU)** switches power to each load through **latching current limiters (LCLs)** or fuses, so that a short circuit in one unit cannot collapse the main bus. Harnesses are designed with derated wire gauges, twisted pairs and shielding for electromagnetic compatibility, and separated from RF and pyrotechnic lines. **Point-of-load converters** provide the low voltages (3.3 V, 1.8 V, 1.0 V core) that modern processors need. Fault protection includes undervoltage load shedding: when the battery falls below a threshold, non-essential loads are switched off and the spacecraft enters a power-safe mode.

## Mechanisms

Mechanisms are among the most failure-prone items on spacecraft because they must work after launch vibration, in vacuum and over temperature extremes, often after years of storage — and many can be tested only a few times on the ground. The main families are summarised in @fig:mechanisms.

![Families of spacecraft mechanisms and typical examples.](figures/out/ch05_mechanisms.svg){#fig:mechanisms width=98%}

- **Hold-down and release mechanisms (HDRMs)** lock deployables during launch and release them in orbit. Pyrotechnic devices (bolt cutters, separation nuts) are fast and reliable but produce shock; non-explosive actuators (NEA split-spool devices, Frangibolt shape-memory-alloy actuators, thermal knives that cut Dyneema cords on CubeSats) produce little shock.
- **Hinges and deployment devices** — spring-driven hinges with dampers or latches; booms such as coilable lattice masts, STEM/bi-STEM tubes and telescopic masts for magnetometers, antennas and solar sails.
- **Rotating mechanisms** — solar array drives, antenna pointing mechanisms, scan mirrors, reaction wheel bearings; they need space-qualified lubricants and transfer power and signals across rotating joints through slip rings or flexible cables.
- **Separation systems** — clamp bands, motorised Lightband rings and CubeSat deployers (e.g., the standard 3U/6U/12U deployers) separate the spacecraft from the launcher.
- **Precision mechanisms** — hexapods, focus and filter mechanisms, mirror actuators (JWST has 132 actuators to align its 18 primary mirror segments to tens of nanometres).

Design rules for reliable mechanisms include: a **torque margin** of at least 2× (ECSS-E-ST-33-01C requires the motorisation torque to exceed twice the sum of resistive torques plus inertia terms, with higher factors early in design), redundant springs or motor windings, avoidance of cold welding by dissimilar materials and coatings, life testing to several times the required number of cycles, and careful "test as you fly" deployment testing with gravity compensation.

::: warning
**Failure lesson — Galileo's high-gain antenna (1991)**

NASA's Galileo Jupiter probe carried a 4.8 m umbrella-like high-gain antenna. When commanded to open in April 1991, three of its 18 ribs stuck, probably because the lubricant on the rib restraint pins had been lost during repeated truck transports while the launch was delayed after the Challenger accident. Engineers could never free it. Through heroic software and ground-station upgrades — new data compression and coding, arraying of DSN antennas — the mission still returned about 70 % of its science objectives using the low-gain antenna at about 160 bit/s instead of 134 kbit/s. Lessons include lubricant life, the effect of ground handling, and the value of in-flight reprogrammability.
:::

## Integrated Design: Example Bus

To see how these subsystems combine, @tbl:busexample lists the main characteristics of a representative 500 kg-class Earth-observation bus.

Table: Representative characteristics of a 500 kg-class LEO Earth-observation satellite bus (illustrative). {#tbl:busexample}

| Parameter | Value |
|---|---|
| Launch mass / payload mass | 500 kg / 150 kg |
| Structure | Aluminium honeycomb box, CFRP payload bench, 1 194 mm interface ring |
| Orbit | 600 km sun-synchronous, 10:30 local time |
| Power | Two deployable GaAs triple-junction wings, 1.2 kW BOL / 0.95 kW EOL; 28 V unregulated bus; 60 Ah Li-ion battery |
| Thermal | MLI, white-paint and OSR radiators, heat pipes on payload panel, 120 W of thermostatic heaters |
| ADCS | 3-axis stabilised, 4 reaction wheels, 3 magnetorquers, 2 star trackers, fibre-optic gyro, GNSS receiver; pointing accuracy 0.02° |
| Propulsion | Hydrazine monopropellant, 4 × 1 N thrusters, 40 kg propellant (or Hall thruster, 15 kg xenon/krypton) |
| Data handling | Radiation-tolerant processor, 4 Tbit mass memory, SpaceWire payload interface |
| Communications | S-band TT&C (2 kbit/s up, 64 kbit/s down); X-band payload downlink 800 Mbit/s; optional optical terminal |
| Design life | 7 years |

::: key
**Key takeaways**

- Structures are usually sized by stiffness, not strength; honeycomb sandwich panels, aluminium, titanium and CFRP dominate; FEM and coupled-loads analysis predict the real launch loads.
- Thermal control is mostly passive (coatings, MLI, radiators, heat pipes), supplemented by heaters, louvres, pumped loops and cryocoolers; models are correlated in thermal-balance tests.
- Multi-junction solar cells reach 30–33 % efficiency; arrays are sized for end-of-life, worst-case conditions; Li-ion batteries are sized by eclipse energy and allowable depth of discharge.
- Beyond Jupiter or on dark, dusty surfaces, RTGs (≈ 6 % efficient) provide power for decades; fission power is being developed for the Moon.
- Mechanisms are high-risk items: use torque margins, redundancy, proper lubrication and realistic deployment testing.
:::

::: questions
**Review questions**

1. Why are spacecraft structures usually sized by stiffness rather than strength? Why do launch vehicles specify minimum fundamental frequencies?
2. Explain why honeycomb sandwich panels are so widely used in spacecraft structures.
3. A radiator with emittance 0.85 views deep space and must reject 500 W at 290 K. Estimate its area, ignoring absorbed environmental heat.
4. Describe four passive and two active thermal control techniques, and give a typical application of each.
5. A LEO spacecraft needs 800 W during a 35-minute eclipse. Size the battery capacity for a 30 % depth of discharge, ignoring losses.
6. Why are solar arrays sized for end-of-life conditions? List three factors that reduce array output during a mission.
7. Why do missions beyond Jupiter use radioisotope power, and what are its main drawbacks?
8. Why are mechanisms considered high-risk items, and how is that risk reduced?
:::
