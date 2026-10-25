---
title: Spacecraft Systems Engineering
hero: ch04
abstract: A spacecraft is a system of systems that must work first time, in an environment it was never fully tested in, for many years without repair. Systems engineering is the discipline that makes this possible. This chapter explains the project life cycle and its reviews, requirements and architecture, technical budgets and margins, technology readiness, reliability and redundancy, risk management, model-based systems engineering, the verification and test campaign, product assurance, cost and schedule estimation, and the standards that codify decades of hard-won lessons.
---

## What Systems Engineering Does

The International Council on Systems Engineering (INCOSE) defines systems engineering as "a transdisciplinary and integrative approach to enable the successful realisation, use and retirement of engineered systems." In plainer words: the systems engineer makes sure that the right system is built, that all its parts work together, and that it is shown to work before it is launched.

In a space project the systems engineering team is responsible for:

- **Defining the problem.** Understanding stakeholder needs and turning them into a concept of operations (ConOps) and verifiable requirements.
- **Designing the architecture.** Choosing the orbit, the segments, the spacecraft configuration and the split of functions between subsystems, hardware and software, space and ground.
- **Managing interfaces.** Every mechanical, electrical, thermal, data and RF interface between subsystems and segments is documented and controlled (interface control documents, ICDs).
- **Allocating and tracking budgets.** Mass, power, propellant, pointing, data, link and cost budgets, each with margins.
- **Managing technical risk.** Identifying what could go wrong and reducing likelihood or consequence.
- **Planning and closing verification.** Proving, by test, analysis, inspection or demonstration, that every requirement is met.
- **Making trade-offs.** Comparing alternatives using clear criteria (performance, cost, risk, schedule).

::: key
**Key concept — optimise the whole, not the parts**

A subsystem engineer naturally wants the best solar array, the lightest structure or the fastest computer. The systems engineer asks a different question: what combination of choices gives the best *mission* within cost, schedule and risk? A slightly heavier structure that simplifies the thermal design and the test campaign may be the better system choice.
:::

## The Project Life Cycle

Large space projects follow a phased life cycle with formal reviews and decision points. NASA's version (NPR 7120.5 and NPR 7123.1) is shown in @fig:lifecycle; ESA's ECSS-M-ST-10C uses equivalent phases 0, A, B, C, D, E and F.

![NASA's project life cycle. Formulation (Pre-Phase A to Phase B) defines and plans the mission; Implementation (Phases C to F) builds, launches, operates and closes it out. Key Decision Points (KDPs) are management gates; technical reviews assess maturity before each gate.](figures/out/ch04_lifecycle.svg){#fig:lifecycle width=100%}

Table: Phases of a space project and their main products. {#tbl:phases}

| Phase | Purpose | Typical products | Exit review |
|---|---|---|---|
| Pre-Phase A — Concept studies | Explore the mission idea, identify needs and alternative concepts | Mission concept, feasibility study, rough cost | Mission Concept Review (MCR) |
| A — Concept and technology development | Define the system baseline, mature critical technologies | ConOps, system requirements, technology development plan, preliminary budgets | System Requirements Review (SRR), Mission/System Definition Review (MDR/SDR) |
| B — Preliminary design | Complete the preliminary design of all elements; establish cost and schedule baseline | Subsystem specifications, ICDs, preliminary design, verification plan, risk list | Preliminary Design Review (PDR) |
| C — Final design and fabrication | Complete the detailed design; build and test engineering and qualification models; start flight hardware | Build-to drawings, software code, qualification test results | Critical Design Review (CDR), System Integration Review (SIR) |
| D — System assembly, integration, test and launch | Integrate and verify the flight system; prepare operations; launch; commission | Verified flight system, operations procedures, trained team | Operational Readiness Review (ORR), Flight Readiness Review (FRR), Launch Readiness Review (LRR), Post-Launch Assessment Review (PLAR) |
| E — Operations and sustainment | Conduct the mission | Science and service data, operations reports | Critical events reviews, Decommissioning Review (DR) |
| F — Closeout | Dispose of the spacecraft and close the project | Disposal manoeuvres, data archiving, lessons learned | Disposal readiness |

Commercial and "New Space" projects compress these phases dramatically, often merging reviews and replacing paper documents with continuously updated models and agile software practices. A Starlink satellite design iterates in weeks; a flagship science mission such as Europa Clipper took about a decade from Phase A to launch. The principles — know what you need, design to it, prove it works — remain the same.

### Why Early Decisions Matter

Most of a project's life-cycle cost is *committed* by decisions made early, long before most of the money is *spent* (@fig:costcommit). Choosing the orbit, launch vehicle, propulsion type or instrument technology in Phase A fixes most of what follows. A change that costs a meeting in Phase A may cost a redesign in Phase C and a mission failure if discovered in orbit. This is why systems engineering effort should be heaviest at the start of a project.

![Cumulative life-cycle cost committed by design decisions versus cost actually spent. By the end of the preliminary design phase, roughly three-quarters of the eventual cost is already determined.](figures/out/ch04_cost_committed.svg){#fig:costcommit width=86%}

## Requirements Engineering

### Good Requirements

A requirement states what the system *shall* do or be. Requirements form a hierarchy (@fig:reqtree): Level 1 mission requirements (owned by the sponsor), Level 2 system requirements, Level 3 segment and subsystem requirements, and Level 4 component requirements. Every lower-level requirement should trace to a parent; requirements with no parent are "gold plating", and parents with no children are gaps.

![The requirements hierarchy, from mission objectives through system and segment requirements to subsystem specifications. Each requirement carries a verification method and a trace to its parent.](figures/out/ch04_req_tree.svg){#fig:reqtree width=94%}

A good requirement is:

- **Necessary** — traceable to a real need;
- **Unambiguous** — only one interpretation ("the spacecraft shall be lightweight" fails; "the spacecraft wet mass shall not exceed 450 kg" passes);
- **Verifiable** — there is a test, analysis, inspection or demonstration that proves it;
- **Achievable** — technically feasible within the budget;
- **Singular** — one requirement per statement;
- **Solution-independent** where possible — states *what*, not *how*.

::: example
**Worked example — from a mission objective to a subsystem requirement**

*Mission objective:* "Map crop health across Europe every five days."

*System requirement:* "The system shall acquire multispectral imagery of all land between 35° N and 72° N. The revisit time shall be no more than 5 days, and the ground sampling distance shall be 10 m or better in the red, green, blue and near-infrared bands."

*Derived requirements:* the constellation shall consist of two satellites in a 786 km sun-synchronous orbit phased 180° apart (orbit analysis). The instrument swath shall be ≥ 290 km (coverage analysis), and the instrument focal length and detector pitch shall give 10 m GSD (optics design). The data-handling subsystem shall store ≥ 2.4 Tbit and the X-band downlink shall transmit ≥ 520 Mbit/s (data budget). These numbers are, in fact, those of ESA's Sentinel-2 mission (Chapter 14).
:::

### Concept of Operations

A **concept of operations (ConOps)** describes how the system will be used from the user's viewpoint. It covers the mission phases (launch, early orbit, commissioning, nominal operations, contingencies, disposal) and what the spacecraft does on a typical day. It also covers who commands it and how often, how data flows to users, and how anomalies are handled. Writing the ConOps early exposes missing requirements — for example, a need for autonomy because ground contacts are only a few minutes per orbit.

## Architecture and Trade Studies

The **architecture** is the high-level structure of the system: what elements exist and how functions are allocated among them. Typical architectural decisions for an Earth-observation mission include:

- One large satellite or a constellation of small ones?
- Optical or radar payload, or both?
- Onboard processing or raw-data downlink?
- Own ground stations, a commercial ground network or optical relay through GEO?
- Chemical, electric or no propulsion?

Alternatives are compared in **trade studies**. A transparent method is to define weighted criteria (e.g., performance 30 %, cost 25 %, risk 20 %, schedule 15 %, growth potential 10 %). The method then scores each option and tests how sensitive the result is to the weights. A trade study is only as good as its assumptions, so the assumptions must be documented.

## Technical Budgets and Margins

### The Main Budgets

The systems engineer maintains a set of **budgets** — tables that allocate a limited resource among subsystems and track the current best estimate against the allocation:

| Budget | Resource tracked | Typical drivers |
|---|---|---|
| Mass | kg, including propellant | Launch vehicle capability, structure, propellant for Δv |
| Power | W (average and peak), Wh per orbit | Payload duty cycle, eclipse length, heaters, end-of-life degradation |
| Propellant / Δv | m/s and kg | Orbit raising, station-keeping, attitude control, disposal |
| Data | bits generated, stored, downlinked per day | Payload data rate, compression, ground contact time |
| Link | dB of margin | Distance, antenna gains, transmitter power, rain fade |
| Pointing | arcseconds of error and stability | Payload field of view, jitter, alignment, thermal distortion |
| Thermal | °C ranges for each unit | Dissipation, radiator area, orbit environment |
| Cost and schedule | money and time | All of the above |

@fig:masspie shows how the launch mass of two typical spacecraft is divided.

![Typical distribution of launch mass for a LEO Earth-observation satellite and a GEO communications satellite. The GEO satellite carries a large propellant fraction for orbit raising and 15 years of station-keeping.](figures/out/ch04_mass_pie.svg){#fig:masspie width=100%}

### Margins and Contingency

Early in a project the estimates are uncertain, and history shows that mass and power almost always *grow* as the design matures. Projects therefore hold **contingency** and **margin**. Contingency is an allowance for growth in the estimate of each item, larger for new designs than for heritage hardware. Margin is a system-level reserve between the total estimate and the hard limit. @fig:margins shows typical guidance.

![Typical recommended margins as a function of project phase. Margins are largest when uncertainty is largest and are progressively released as the design matures.](figures/out/ch04_margins.svg){#fig:margins width=86%}

::: warning
**Failure lesson — running out of margin**

The James Webb Space Telescope grew in cost from an initial estimate of about US$1–3.5 billion to about US$10 billion, and its launch slipped from 2007 to 2021. This was in part because the technical complexity of the deployable sunshield and mirror had been underestimated, and early reserves were too small. The telescope ultimately performed better than its requirements. But the experience led NASA to require cost and schedule reserves for major projects to be budgeted at the 70 % confidence level ("joint confidence level", JCL).
:::

## Technology Readiness

**Technology Readiness Levels (TRLs)** — invented at NASA in the 1970s and now an international standard (ISO 16290) — measure how mature a technology is (@fig:trl). Most agencies require all critical technologies to reach **TRL 6** (prototype demonstrated in a relevant environment) by PDR. Technologies at TRL 3–5 cross the "valley of death", where research funding ends but projects are not yet willing to adopt them. Related scales include Manufacturing Readiness Levels (MRL) and Software/AI readiness frameworks (Chapter 53).

![The nine Technology Readiness Levels. Projects typically require TRL 6 for critical technologies by the Preliminary Design Review.](figures/out/ch04_trl.svg){#fig:trl width=92%}

## Reliability and Redundancy

### Reliability Basics

**Reliability** $R(t)$ is the probability that an item performs its function for time $t$ under stated conditions. During the useful-life period of electronics, failures occur at a roughly constant rate $\lambda$, so

$$R(t) = e^{-\lambda t}, \qquad \text{MTTF} = 1/\lambda$$

Failure rates are often given in **FITs** (failures in $10^9$ device-hours). Before and after this period, the "bathtub curve" rises (@fig:reliability). Early *infant mortality* failures are weeded out by burn-in, screening and environmental testing. At the end, *wear-out* (battery capacity fade, bearing wear, propellant depletion, solar cell degradation) limits life.

For components in series (all must work), reliabilities multiply: $R_{sys} = \prod R_i$. For parallel redundancy (any one suffices), unreliabilities multiply: $R_{sys} = 1 - \prod(1 - R_i)$.

![Left: the bathtub curve of failure rate over life. Right: reliability over a 20-year mission for a single unit and for three redundancy schemes, assuming an MTTF of 30 years per unit.](figures/out/ch04_reliability.svg){#fig:reliability width=100%}

### Redundancy Strategies

- **Hot (active) redundancy** — two units operate together; either can carry the load.
- **Cold (standby) redundancy** — the backup is switched on only when the primary fails; it suffers less wear but needs reliable failure detection and switching.
- **Cross-strapping** — each of two redundant units of subsystem A can work with either unit of subsystem B, avoiding a single failure taking out a whole chain.
- **Voting (k-out-of-n)** — three computers compare outputs and outvote a faulty one (triple modular redundancy); used for launch vehicle avionics and safety-critical systems.
- **Functional redundancy** — a different method achieves the same function (e.g., attitude from star trackers or from Sun sensors and magnetometers).
- **Constellation-level redundancy** — spare satellites in orbit or on the ground, or graceful degradation by design (common in mega-constellations).

Single points of failure (SPFs) are identified by **failure modes, effects and criticality analysis (FMECA)** and either removed or justified. Typical SPFs that are accepted include primary structure, propellant tanks and some deployment mechanisms, which are designed with large margins instead.

Table: Extract of a failure modes, effects and criticality analysis (FMECA) for a small-satellite power subsystem (illustrative). {#tbl:fmeca}

| Item | Failure mode | Cause | Local effect | System effect | Severity | Detection | Mitigation |
|---|---|---|---|---|---|---|---|
| Solar array string | Open circuit | Interconnect fatigue, MMOD impact | Loss of one string (≈ 4 % power) | Reduced power margin | 3 (minor) | String current telemetry | 15 % end-of-life array margin; string-level blocking diodes |
| Battery cell | Internal short | Manufacturing defect, dendrite growth | Cell voltage drop, heating | Loss of battery module if not isolated | 2 (major) | Cell voltage and temperature monitoring | Cell screening, cell bypass, n+1 strings |
| Battery charge regulator | Fails "on" | Transistor short | Overcharge | Battery damage, possible thermal runaway | 1 (catastrophic) | Hardware over-voltage detector | Independent hardware cut-off, redundant regulator |
| Power distribution switch | Fails open | Latch-up, wear | Load unpowered | Loss of unit until switched to redundant | 2 | Current telemetry, watchdog | Cross-strapped redundant switches |
| Main bus | Short circuit | Harness chafing, debris | Bus voltage collapse | Loss of mission | 1 | Undervoltage monitor | Fault-current limiters, harness protection, design reviews |

## Risk Management

A **risk** is a potential future event that would harm the project, characterised by its **likelihood** and **consequence**. Risks are recorded in a risk register, scored on a **5 × 5 matrix** (@fig:riskmatrix) and assigned an owner. Each is handled by one of four strategies: *mitigate* (reduce likelihood or consequence), *accept*, *transfer* (e.g., insurance or contract terms), or *avoid* (change the design). Mitigation plans include "burn-down" steps tied to milestones, so that progress is visible.

![A 5 × 5 risk matrix. Each risk (R1–R5) is plotted by likelihood and consequence; mitigation actions aim to move risks out of the red zone before key reviews.](figures/out/ch04_risk_matrix.svg){#fig:riskmatrix width=72%}

Programmes also distinguish **risk classes**. NASA's NPR 8705.4 defines Class A to Class D, plus a "do no harm" category for very low-cost CubeSats. Class A has the highest priority and lowest risk tolerance (e.g., JWST, crewed systems). Class D accepts higher risk for lower cost (many small science missions). The class determines parts quality, redundancy, review depth and test requirements. ESA and other agencies use similar tailoring.

## Model-Based Systems Engineering

Traditionally, the system design lived in hundreds of documents, spreadsheets and drawings, with inconsistencies discovered late. **Model-based systems engineering (MBSE)** replaces documents with a single, connected digital model of requirements, structure, behaviour and parameters (@fig:mbse). The standard language is **SysML** (Systems Modeling Language); **SysML v2**, formally adopted by the Object Management Group in 2025, adds a precise textual notation and an API that lets engineering tools exchange data automatically. MBSE tools link to CAD, finite-element, thermal, orbit and cost models, so that a change in one place propagates everywhere — the foundation of the "digital thread" and **digital twin** concepts (Chapter 52).

![Model-based systems engineering links requirements, operations, structure, behaviour and parametric analyses in one authoritative system model, connected to specialist engineering tools.](figures/out/ch04_mbse.svg){#fig:mbse width=90%}

::: ai
**AI in practice — assistants for systems engineers**

Large language models are increasingly used to check requirement quality (ambiguity, missing "shall", non-verifiable wording), to trace requirements to design elements, to search lessons-learned databases and to draft SysML models from text. Agencies including NASA and ESA are evaluating such tools under strict data-security rules. Chapter 52 discusses how AI outputs must themselves be verified before they enter a controlled baseline.
:::

## Verification and Validation

**Verification** asks "did we build the system right?" — does it meet its requirements? **Validation** asks "did we build the right system?" — does it meet the stakeholders' needs in its real environment? The V-model (@fig:vmodel) shows how each level of design on the left is matched by a level of verification on the right.

![The systems engineering "V". Requirements are decomposed down the left side, the system is built at the bottom, and verification proceeds up the right side, each level verified against the requirements defined at the same level.](figures/out/ch04_vmodel.svg){#fig:vmodel width=96%}

### Verification Methods

Every requirement is assigned one or more verification methods:

- **Test** — measurement under controlled conditions (e.g., thermal-vacuum test of the battery).
- **Analysis** — calculation or simulation, used when testing is impossible or too costly (e.g., MMOD survival probability, 15-year radiation dose).
- **Inspection** — visual or dimensional check (e.g., connector labelling, workmanship).
- **Demonstration** — operation showing a function without detailed measurement (e.g., deploying an antenna with gravity offloading).

The **verification matrix** lists every requirement, its method, the verification event and the closure evidence. Closing it is a condition of flight readiness.

### Model Philosophy

Projects choose how many physical models to build (@fig:models). A classic approach builds a **structural-thermal model (STM)** to verify mechanical and thermal design, and an **engineering model (EM)** to verify functions and interfaces. It also builds a **qualification model (QM)** tested to qualification levels (typically flight levels plus 3–6 dB for vibration and ±10 °C beyond predicted temperatures). Finally, it builds a **flight model (FM)** tested to acceptance levels. The cheaper **protoflight** approach tests the single flight model to qualification levels for acceptance durations, accepting a slightly higher risk of fatigue damage.

![Model philosophies. Classic approaches qualify a dedicated model before building the flight unit; protoflight approaches qualify and accept the flight unit itself.](figures/out/ch04_models.svg){#fig:models width=94%}

### The Integration and Test Campaign

Assembly, integration and test (AIT) — called I&T in the US — brings the spacecraft together and exposes it to every environment it will see (@fig:aitflow). Key tests include:

- **Functional and performance tests** at unit, subsystem and system levels, repeated after each environmental test (comprehensive performance tests, CPTs, and shorter "aliveness" tests).
- **Mechanical tests**: sine vibration, random vibration (for smaller spacecraft), acoustic (for large spacecraft with light panels), shock and separation tests, modal surveys, and static load tests on structural models.
- **Thermal tests**: thermal balance (to validate the thermal model) and thermal-vacuum cycling (to show the hardware works at the hot and cold extremes; typically 4–8 cycles for units).
- **Electromagnetic compatibility (EMC)**: conducted and radiated emissions and susceptibility (e.g., MIL-STD-461), plus RF compatibility with ground stations and the launcher.
- **Deployment tests** with gravity off-loading (zero-g rigs, balloons, air-bearing tables).
- **End-to-end tests** with the real ground segment and mission operations team, and **mission simulations** that rehearse launch and early operations.
- **Mass properties** (mass, centre of gravity, moments of inertia) and **alignment** measurements.

![A typical spacecraft assembly, integration and test (AIT) flow. Environmental tests are separated by functional tests that check for damage; the sequence is arranged so that the most severe mechanical tests precede the final thermal and functional verification.](figures/out/ch04_ait_flow.svg){#fig:aitflow width=100%}

::: figrow
![The High Bay 1 cleanroom at NASA's Jet Propulsion Laboratory during assembly of the Mars 2020 Perseverance rover and its cruise stage. Cleanrooms control particulate and molecular contamination and, for Mars missions, biological contamination.](figures/photos/ch04_highbay.jpg){#fig:highbay}

![Europa Clipper in JPL's High Bay 1 after installation of its 3 m high-gain antenna in August 2023. The spacecraft was launched in October 2024 and will arrive at Jupiter in 2030.](figures/photos/ch04_clipper.jpg){#fig:clipper}
:::

![A technician inside Sierra Space's Dream Chaser spaceplane preparing for vibration testing at NASA's Neil Armstrong Test Facility in Ohio, home to the world's most powerful spacecraft shaker system and a large vacuum chamber.](figures/photos/ch04_shake.jpg){#fig:shake width=80%}

::: warning
**Failure lesson — test as you fly**

In 1999 NASA's Mars Polar Lander was probably lost because its software interpreted vibrations from the deployment of its landing legs as touchdown, shutting off the descent engines about 40 m above the surface. The fault could have been found by a system-level test of the leg deployment with the flight software — a test that was planned but, after a wiring error was corrected, not repeated. The same year, Mars Climate Orbiter was lost because one team used pound-force seconds and another newton-seconds for thruster impulse data. Both losses led to stricter end-to-end testing and interface verification across NASA.
:::

## Product Assurance and Safety

**Product assurance (PA)** — called mission assurance in the US — ensures that the hardware and software are built as designed and are reliable. It includes:

- **Quality assurance**: configuration management, nonconformance reporting, material review boards, inspections, workmanship standards (e.g., soldering to ECSS-Q-ST-70-08 or NASA-STD-8739).
- **Electrical, electronic and electromechanical (EEE) parts**: selection from approved lists, screening (burn-in, X-ray), radiation testing, counterfeit avoidance, derating (operating parts well below their maximum ratings).
- **Materials and processes**: outgassing, flammability, stress corrosion, atomic-oxygen resistance.
- **Software product assurance**: coding standards, independent verification and validation (IV&V), software criticality classes (e.g., NASA Class A–E; ECSS criticality A–D).
- **Safety**: hazard analyses for launch-site operations (pressurised systems, pyrotechnics, batteries, propellants), launch-range safety, crew safety for human-rated systems, and re-entry casualty risk. The probability of injuring someone on the ground from re-entering debris must normally be below 1 in 10 000.

## Cost and Schedule

### Estimating Cost

Space projects are estimated by three methods: **analogy** (scaling from a similar past project), **parametric** and **engineering build-up** (summing labour and materials for every work-package). The parametric method uses cost-estimating relationships (CERs) that relate cost to mass, power, complexity and heritage. Examples are NASA's Project Cost Estimating Capability (PCEC), the USAF Unmanned Space Vehicle Cost Model and the Aerospace Corporation's Small Satellite Cost Model. Mature projects use all three and reconcile the results.

Typical cost elements for a science mission are the spacecraft bus (25–35 %), instruments (20–35 %) and project management/systems engineering/mission assurance (10–15 %). The others are integration and test (5–10 %), launch (10–25 %), and operations and data analysis (10–20 %). Reserves of 25–50 % are typical before PDR.

### Schedule

Space schedules are dominated by long-lead items (detectors, star trackers, reaction wheels, radiation-hardened processors, propellant tanks). They are also dominated by integration and test, which cannot be easily parallelised, and by launch windows. For planetary missions, launch windows occur only every one to two years. A slip of a few weeks in delivering a Mars mission can delay launch by 26 months. This happened to ESA's ExoMars rover, delayed from 2020 to 2022 and then to 2028 after cooperation with Russia ended.

## Standards and Bodies of Knowledge

Systems engineering practice is codified in standards that capture lessons from decades of successes and failures:

Table: Key standards and handbooks for space systems engineering. {#tbl:standards}

| Standard / handbook | Publisher | Scope |
|---|---|---|
| NASA Systems Engineering Handbook (SP-2016-6105 Rev 2) | NASA | Processes, life cycle, technical management |
| NPR 7120.5 / NPR 7123.1 | NASA | Programme/project management and systems engineering requirements |
| ECSS-E-ST-10C, ECSS-M-ST-10C, ECSS-Q-ST series | European Cooperation for Space Standardization | Systems engineering, project phasing, product assurance |
| ISO/IEC/IEEE 15288 | ISO / IEEE | System life-cycle processes (all industries) |
| ISO 24113 | ISO | Space debris mitigation requirements |
| GSFC-STD-7000 (GEVS) | NASA Goddard | Environmental verification requirements for payloads and spacecraft |
| SMC-S-016 / SMC-S-010 | US Space Force | Test requirements for launch, upper-stage and space vehicles; systems engineering |
| AIAA S-120A | AIAA | Mass properties control and growth allowance |
| CCSDS Blue Books | Consultative Committee for Space Data Systems | Communication and data-system standards (Chapter 7) |
| *Space Mission Engineering: The New SMAD* (Wertz, Everett & Puschell, 2011) | Microcosm Press | Classic engineering reference for mission design |
| INCOSE Systems Engineering Handbook (5th ed., 2023) | INCOSE | General systems engineering body of knowledge |

::: key
**Key takeaways**

- Systems engineering optimises the whole mission across segments, subsystems, cost, schedule and risk; most cost is committed in early phases.
- Life cycles move from concept (Pre-A, A) through design (B, C) to integration, launch and operations (D, E) and closeout (F), gated by reviews such as SRR, PDR and CDR.
- Good requirements are necessary, unambiguous, verifiable and traceable; budgets track mass, power, Δv, data, links and pointing with phase-dependent margins.
- Reliability is improved by part quality, derating, redundancy and testing; FMECA identifies single points of failure; risks are managed on a likelihood–consequence matrix.
- MBSE (SysML v2) connects requirements, design and analysis in a single model; verification closes every requirement by test, analysis, inspection or demonstration.
- "Test as you fly": many famous failures (Mars Polar Lander, Mars Climate Orbiter) were interface or end-to-end test gaps, not exotic physics.
:::

::: questions
**Review questions**

1. Why is most of a project's life-cycle cost committed during the early phases, even though little money has been spent by then?
2. Outline the project phases from Pre-A to F and name the major reviews that close Phase B and Phase C.
3. Rewrite the requirement "The satellite shall have a good camera" so that it is necessary, unambiguous and verifiable.
4. Why do mass and power budgets carry larger margins early in a project? How do the margins change as the design matures?
5. Two identical units are flown in active parallel redundancy, each with a reliability of 0.90 over the mission. What is the reliability of the pair? What assumption does this answer rely on?
6. What is a technology readiness level? Why is TRL 6 normally expected by the preliminary design review?
7. Distinguish verification from validation and list the four verification methods, with an example of each.
8. Explain the principle "test as you fly" using one of the mission failures discussed in this chapter.
:::
