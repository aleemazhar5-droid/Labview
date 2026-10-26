---
title: AI for Autonomy, Navigation and Robotics
hero: ch48
abstract: A spacecraft that waits for instructions from Earth cannot land on Mars, dodge debris every few minutes or grab a tumbling satellite. It must sense, decide and act on its own. This chapter explains how. It starts with why autonomy is needed and the ECSS autonomy levels, then looks inside an autonomous spacecraft: executives, fault protection, model-based diagnosis and onboard planners. It covers navigation by stars, craters and terrain maps, pose estimation for rendezvous, convex guidance and reinforcement learning, docking, rovers, robot arms, free-flyers, swarms and constellations. Small optimisation and learning experiments, run from scratch, show what each method does well and where it fails. Status is given as of October 2026.
---

Every spacecraft is a robot. Most of the time it follows a script written on the ground. But some decisions cannot wait for the ground. A Mars lander has about seven minutes from the top of the atmosphere to the surface, while a radio signal takes up to 22 minutes to arrive. A rover that stops after every metre to ask for advice will never get anywhere. A fleet of ten thousand satellites meets debris many times an hour. In each case the spacecraft must sense its situation, decide what to do and act — on its own.

This chapter is about the software that makes those decisions. Much of it is not machine learning. Planners search through possible schedules, filters fuse sensor data, and optimisers compute fuel-optimal trajectories with mathematical guarantees. Learning enters where hand-written rules struggle: recognising craters, finding a satellite's corners in a camera image, or choosing a path across rough ground. The hero image above shows the idea. It is a replay of telemetry from Perseverance's first self-driving (AutoNav) drive: the rover's own three-dimensional map of the ground ahead and the path it chose.

Background is covered elsewhere: control and estimation in Chapter 6, deep-space navigation in Chapter 24, landing in Chapter 27, rovers in Chapter 28 and servicing in Chapter 40. Machine-learning basics are in Chapters 43 and 44, and onboard computers in Chapter 45.

## Why Spacecraft Need Autonomy

The key idea is simple. A spacecraft needs autonomy whenever the ground cannot respond fast enough, often enough or cheaply enough. Four things set the limit: light-time, gaps in contact, the number of spacecraft and the speed of events.

### Light-Time, Gaps and Scale

**Light-time** is the time a radio signal takes to travel one way. It is 0.12 s to geostationary orbit and 1.3 s to the Moon. To Mars it ranges from about 3 to 22 minutes, and to Jupiter from 33 to 53 minutes. Voyager 1 will be one light-day from Earth in November 2026. A question and its answer take twice as long.

**Contact gaps** often matter more. A low-orbit satellite passes over a ground station for about ten minutes at a time, a few times a day. A Mars rover talks to Earth mostly through orbiters that fly over a few times per sol (a Martian day of 24 h 39 min). Deep-space missions share NASA's Deep Space Network with dozens of others and may get a few hours of contact a day.

**Scale** is the newest driver. Over ten thousand Starlink satellites are in orbit, and other constellations are following (Chapter 17). No team of people can plan every pointing change, data dump and collision-avoidance manoeuvre for such a fleet by hand.

**Speed of events** sets the final limit. A failed thruster valve, a boulder in a landing zone or a closing piece of debris must be dealt with in seconds to hours. Autonomy also saves money, because fewer people are needed to watch routine operations.

### Levels of Autonomy

The European standard on space segment operability, ECSS-E-ST-70-11C (2008, revised in October 2025), defines levels on three separate scales (@tbl:ecsslevels). The **E** scale covers the execution of nominal operations. The **D** scale covers onboard storage of mission data, and the **F** scale covers what the spacecraft does after a failure. A mission states a level on each scale. A typical Earth-observation satellite might be E2, D2 and F1; a Mars rover is E3 or E4 for driving, with F2 for many faults.

| Level | The spacecraft can… | Typical example |
|---|---|---|
| E1 | Execute commands from the ground in real time, plus time-tagged commands for safety | Early satellites; ground-controlled tests |
| E2 | Execute a pre-planned, ground-written timeline stored on board | Most Earth-observation and communication satellites |
| E3 | React to events with onboard rules and procedures | Rover hazard avoidance; autonomous collision avoidance |
| E4 | Re-plan on board from goals | EO-1 Autonomous Sciencecraft; Perseverance onboard planner |
| D1 | Store essential data on board during a ground outage or failure | Event logs kept until the next pass |
| D2 | Store all mission data, independent of the ground | Mass memory sized for the longest gap |
| F1 | Detect a failure, isolate it and go to a safe state | Safe mode with Sun pointing and a call for help |
| F2 | Recover and resume nominal operations after a failure | Deep-space probes switching to redundant units and continuing |

: Autonomy levels of ECSS-E-ST-70-11C for execution (E), data management (D) and failure management (F). The standard defines two data levels and two failure levels, not four. {#tbl:ecsslevels}

### How Much Autonomy Is Enough?

A simple model shows where each level is needed. Suppose an event happens on board. The ground learns of it, decides and replies. The time this takes is

$$ T_\mathrm{ground} = 2\tau + 2W + T_\mathrm{decide}, \qquad W = \tfrac{1}{2}(1-f)^2 P , $$

where $\tau$ is the one-way light-time and $T_\mathrm{decide}$ the time the team needs to decide. $W$ is the mean wait for a contact window, for a spacecraft in contact a fraction $f$ of a cycle of length $P$. The factor $(1-f)^2$ appears because an event falls outside contact with probability $1-f$ and then waits, on average, half the gap.

The model is applied in @fig:autonneed with a 30-minute decision time. A geostationary satellite or the space station gets an answer in about half an hour. A low-orbit imager with two polar ground stations waits about 1.9 hours, mostly for the next pass. A Mars rover waits about 23 hours, and Voyager 1 about 61 hours. Where the ground is more than about ten times too slow, the spacecraft must re-plan for itself (E4). Equipment faults need at least a safe mode (F1) everywhere. Far from Earth, or during landing, they need full recovery on board (F2).

![How much autonomy different missions need, from a simple model. (a) Time for the ground to respond to an event on board: round-trip light-time, waiting for contact windows and a 30-minute decision. (b) The autonomy level implied when that time is compared with how fast typical events unfold. Grey cells are events that do not apply.](figures/out/ch48_autonomy.svg){#fig:autonneed width=100%}

## Inside an Autonomous Spacecraft

An autonomous spacecraft is not one clever program. It is a stack of simple, well-tested parts, each working on its own time scale. Learning is usually confined to the parts that interpret sensor data.

### Sense, Plan, Act

Most designs follow a **three-layer architecture** (@fig:autonarch). The **functional layer** runs fast control loops: attitude control, engine firing, camera exposure, and the perception software that turns images into estimates of position or hazards. The **executive layer** runs the plan. It starts activities, checks that resources and timing stay within limits, and switches modes. The **deliberative layer** thinks ahead. A planner turns goals into a timeline, science software decides what is worth observing, and navigation software chooses paths and manoeuvres.

Two functions cut across the stack. **Fault detection, isolation and recovery (FDIR)** watches for anything that goes wrong. A **runtime monitor** checks commands against simple safety rules before they reach the hardware. The ground does not disappear. It sends goals, models and rules instead of individual commands, and receives summaries and selected data instead of everything.

![Block diagram of an autonomous spacecraft. Faster layers sit lower in the stack; the ground sends goals and rules rather than commands. Gold dots mark where learned models are used or tested today: event detection and perception.](figures/out/ch48_arch.svg){#fig:autonarch width=96%}

### Executives, Behaviour Trees and Fault Protection

The **executive** turns a plan into action. Classic flight executives are timeline sequencers: time-tagged commands plus rules such as "if the battery falls below 30 %, stop the payload". **Behaviour trees**, taken from computer games and ground robotics, organise behaviours as a tree. Each node is "ticked" in turn and reports success, failure or running. A *sequence* node runs its children in order until one fails; a *fallback* node tries alternatives until one succeeds. Trees are easy to read and test, which is why they are increasingly proposed for space robots.

**FDIR** is the oldest form of autonomy. Monitors compare telemetry with limits. When a limit is crossed, a recovery action switches to a redundant unit or puts the spacecraft in **safe mode**: Sun-pointing, power-positive, listening for the ground. That is level F1. Level F2 goes further and resumes the mission, as deep-space probes must.

Fault protection can also cause failures, when the rules meet a situation nobody imagined. In October 2016 ESA's Schiaparelli lander saw its inertial unit saturate for about a second under the parachute. The navigation software then computed a negative altitude, released the parachute and fired the thrusters for only a few seconds. The lander fell from about 3.7 km. In April 2023 ispace's Hakuto-R lander crossed a crater rim during descent. The sudden jump in measured altitude made its software reject the good altimeter data as faulty. The lander kept descending slowly from about 5 km until its fuel ran out. Both lessons are the same: autonomy must be tested against the real terrain and sensors, not only the expected ones.

### Model-Based Diagnosis

Rules say "if symptom A, then do B". They become unmanageable when faults combine. **Model-based diagnosis** takes another approach. Engineers write a model of each component and its possible modes — a valve can be *open*, *closed*, *stuck open* or *stuck closed* — and how the modes connect. The software then searches for the most probable set of modes that explains what the sensors see:

$$ \hat{m} = \arg\max_{m}\; P(m \mid \text{observations}) \;\propto\; P(\text{observations} \mid m)\, P(m). $$

Faults are rare, so the prior $P(m)$ favours explanations with few failed parts. NASA's **Livingstone** engine, built at Ames Research Center in the 1990s, did this with logical models and fast search. It then planned the reconfiguration needed to work around the fault. Learned anomaly detectors on the ground (Chapter 49) now complement such models.

::: history
**Remote Agent: an AI in charge of a spacecraft (Deep Space 1, May 1999)**

NASA's Deep Space 1 tested twelve new technologies. One was the **Remote Agent**, the first AI software to control a spacecraft without ground commanding. It had three parts: a constraint-based planner and scheduler, a multi-threaded "Smart Executive", and Livingstone for diagnosis and recovery. The experiment ran during 17–21 May 1999, for about 35 hours in all.

A 2-day scenario started at 11:04 PDT on 17 May. Remote Agent planned and ran ion-engine thrusting and imaging. It handled an injected camera-switch failure by re-planning. On the morning of 18 May it failed to stop the ion engine as planned. The cause was a race condition between two executive threads that had never appeared in thousands of ground tests. About 70 % of the objectives had been met. The team wrote a new 6-hour scenario overnight. The project chose not to uplink the software fix, judging it insufficiently tested. On 21 May the new scenario completed the remaining objectives, so the experiment met 100 % of them. Its deadlock became a classic argument for formal verification of flight software.
:::

### Twenty-Five Years of Flight Experience

Landmark flights of onboard autonomy are listed in @tbl:autonomyflights. Three patterns stand out. Autonomy has grown from one-off experiments into everyday operations. Most of it is search, estimation and optimisation, not learning. And learned components have entered mainly through perception and science, such as EO-1's classifiers and rover targeting; the first learned flight controller flew only in 2025.

| Year | Mission | Autonomous function | Status | Result |
|---|---|---|---|---|
| 1999 | Deep Space 1 | Remote Agent planning, execution, diagnosis | Flight experiment | 100 % of objectives |
| 1999–2001 | Deep Space 1 | AutoNav optical navigation | Flight demonstration | Comet Borrelly flyby, 2001 |
| 2004–17 | EO-1 | Onboard planning and event detection (ASE) | Operational | Over $1 M a year saved |
| 2016– | Curiosity, Perseverance | AEGIS science targeting | Operational | 889 targets to May 2026 |
| 2020 | OSIRIS-REx | Natural Feature Tracking to sample site | Operational | Within about 1 m |
| 2021 | Perseverance | Lander Vision System | Operational | Touchdown 5 m from aim |
| 2021– | Perseverance | Enhanced AutoNav | Operational | > 90 % of 45 km |
| 2022 | DART | SMART Nav terminal guidance | Operational | Hit 160 m Dimorphos |
| 2023– | Perseverance | Onboard planner (from 5 Oct 2023) | Operational | Hundreds of plans |
| 2024 | SLIM | Crater-matching pinpoint landing | Flight demonstration | Under 10 m before final avoidance |
| 2019– | Starlink | Autonomous collision avoidance | Operational | 207 152 manoeuvres in 6 months |
| 2025 | InnoCube | Learned attitude controller (LeLaR) | Flight experiment | First full manoeuvre 30 Oct 2025 |

: Landmark flights of onboard autonomy, from experiments to daily operations. "Operational" means used in normal mission operations. {#tbl:autonomyflights}

## Onboard Planning and Scheduling

A planner decides *what* to do; a scheduler decides *when*. In space the two are usually combined. The key idea is that a plan is a set of activities that must satisfy hard constraints — time windows, power, data volume and instrument states — while earning as much value as possible.

### Plans, Constraints and Search

Written as mathematics, choosing observations is an integer programme. Each candidate observation $i$ has a value $v_i$, and $x_i$ is 1 if it is chosen and 0 if not.

$$ \max_{x}\; \sum_i v_i x_i \quad \text{subject to} \quad A x \le b, \qquad x_i \in \{0, 1\}. $$

Each row of $A x \le b$ is one constraint. Two observations that overlap in time cannot both be chosen. The energy used in an orbit must stay within the battery budget, and data taken between downlinks must fit in memory. Such problems are **NP-hard**: no known algorithm solves every case quickly, and the worst-case effort grows exponentially with size. Flight planners therefore use three families of methods.

- **Greedy heuristics** sort candidates by a rule, such as value per unit of resource, and add each one that still fits. They are fast and predictable but can miss better combinations.
- **Local search** starts from a plan and keeps making small changes — add an observation, remove a clashing one — accepting changes that help, and sometimes ones that do not, to escape dead ends. JPL's **CASPER** planner uses a related idea called *iterative repair*: when reality departs from the plan, it fixes only the parts that conflict.
- **Exact optimisation**, such as mixed-integer linear programming (MILP) or constraint programming, proves that a plan is the best possible. It needs more computing and its run time is harder to bound.

### A Toy Scheduling Problem

@fig:obssched compares the three on a synthetic day for an imaging satellite. There are 45 targets, each visible one to three times, with values from 1 to 10. The satellite has one instrument with 2-minute slews, an energy budget per 96-minute orbit and a memory emptied at four downlink passes. A typical day has about 90 opportunities and just over 100 constraints.

Over 40 random days, the greedy rule reached 94.4 % of the optimal value on average and 89 % in the worst case, in under a millisecond on a laptop. Local search by **simulated annealing** reached 99.2 % on average in about a tenth of a second, and found the exact optimum on 15 of the 40 days. The exact MILP solver also took about a tenth of a second. As problems grew to about 570 opportunities, MILP took over a second and the greedy rule's shortfall stayed near 9 %. Flight computers are a hundred to a thousand times slower than a laptop. Flight planners therefore pair a fast heuristic, which always yields a safe plan, with improvement when time allows.

![Scheduling one day of observations for a synthetic imaging satellite. (a) Part of one day: all opportunities (top) and the plans chosen by a greedy rule, local search and an exact mixed-integer solver, with values. (b) Value achieved relative to the optimum over 40 random days. (c) Run time against problem size on a laptop.](figures/out/ch48_sched.svg){#fig:obssched width=100%}

::: history
**The Autonomous Sciencecraft on EO-1 (2004–2017)**

NASA's Earth Observing-1 satellite, launched in 2000 to test new imagers, became the longest-running test of an onboard planner. From January 2004 its **Autonomous Sciencecraft Experiment** (ASE) ran full-time. It had three parts. Onboard classifiers analysed Hyperion images for events such as eruptions, floods, fires and ice break-up. The CASPER planner re-planned observations around new goals. A robust executive ran the result.

The computer was modest: a 12 MHz Mongoose V processor of about 8 million instructions per second with 256 MB of memory, separate from the main flight computer for safety. CASPER's model was kept small so that it could build a plan in tens of minutes. By 2007 ASE had made over 11 000 autonomous data acquisitions and over 1 500 closed-loop re-tasks. Alerts from other satellites, such as volcano warnings, could trigger Hyperion images through ground "sensorwebs". JPL reported that operations costs fell by more than $1 million a year, and science events captured per megabyte of downlink rose over a hundredfold. ASE remained the primary planning system until the end of the mission in 2017, after more than 60 000 autonomous observations.
:::

### Planners in Flight Today

The most visible planner today runs on Perseverance. Its **onboard planner** (also called Simple Planner) was developed from 2016 and verified from October 2021, and entered operations on 5 October 2023. It is a priority-first, non-backtracking scheduler: it places activities in priority order and never undoes a placement, which keeps its run time bounded. It re-schedules when an activity ends early or late, or when energy differs from predictions, so the rover can use margin that ground planners had to hold back. In its first two years it ran hundreds of plans with very few anomalies.

Europe has tested autonomy mainly through small missions. ESA's OPS-SAT CubeSat (2019–2024) was an open flying laboratory for experiments in onboard planning and machine learning, among others. France's space agency CNES flew autonomous orbit control on the DEMETER microsatellite from 2005 and an autonomous guidance kit on PICARD in 2014. Its ASTERIA orbit-control software was later demonstrated on OPS-SAT. These steps matter because operators accept autonomy gradually, function by function, once each one has proved itself.

## Navigation Without the Ground

Navigation means knowing where you are and how fast you are moving. Most spacecraft are navigated from the ground by radio tracking (Chapter 24), which is accurate but slow. The key idea of autonomous navigation is to measure position against something the spacecraft can see — stars, asteroids, craters or terrain — and fuse those measurements in an onboard filter.

### Optical Navigation in Deep Space

A camera measures a direction. If it sees a known asteroid against background stars, it measures the unit vector $\hat{u} = (\mathbf{r}_a - \mathbf{r})/\lVert \mathbf{r}_a - \mathbf{r} \rVert$ from the spacecraft at $\mathbf{r}$ to the asteroid at $\mathbf{r}_a$. A Kalman filter (Chapter 6) combines such directions, taken over days, with the equations of motion to fix the orbit.

Deep Space 1's **AutoNav** was the first system to do this on its own, in 1999. It also steered the spacecraft through its flyby of comet Borrelly in September 2001. The same software kept Stardust's camera locked on comet Wild 2 during its 2004 flyby. In July 2005 it flew Deep Impact's impactor into comet Tempel 1, making the final targeting manoeuvres in the last two hours. DART's **SMART Nav** went further in September 2022. It took over about four hours before impact, picked out the 160 m moonlet Dimorphos from its larger partner only about an hour before impact, and steered into it at about 6 km/s. None of these systems used machine learning: they relied on image centroiding, geometry and filtering.

### Terrain-Relative Navigation

Near a surface, the spacecraft can compare what it sees with a map. This is **terrain-relative navigation (TRN)**. It solves a problem that radio tracking cannot: an inertial unit alone may drift by kilometres during entry, while the safe spots in a rugged landing area may be only tens of metres across.

Perseverance's **Lander Vision System** (LVS) set the standard in February 2021, after tests on a rocket-powered lander (@fig:lvsxombie). Its maps came from HiRISE orbital images, resampled to 12 m pixels for a coarse search and 6 m for a fine one. During descent, LVS first matched 15 landmarks across three images, correlating 128 × 128-pixel patches against large map windows in the frequency domain. It then matched up to 150 small landmarks per image and fused them with inertial data. This cut the position error from up to 3.2 km to the required 40 m or less. LVS then chose the safest reachable spot from an onboard hazard map. Perseverance touched down within 5 m of the point LVS aimed for.

![A prototype of the Mars 2020 Lander Vision System flying on Masten's Xombie rocket at Mojave, California, on 9 December 2014. The same vehicle had flown JPL's G-FOLD guidance tests in 2012–13.](figures/photos/ch48_lvstest.jpg){#fig:lvsxombie width=34%}

The matching step uses **normalised cross-correlation**. For a template $t$ from the descent image and a map patch $m$ at offset $(i, j)$,

$$ \rho(i,j) = \frac{\sum_{k} (t_k - \bar t)(m_{k+ij} - \bar m_{ij})}{N\, \sigma_t\, \sigma_{m,ij}}, $$

where the sums run over the $N$ pixels of the template. The offset with the highest $\rho$ is the match. Because $\rho$ removes the mean and scales by the spread, it tolerates changes in brightness and contrast. It does not tolerate changes in shadow direction, because shadows move when the Sun moves.

@fig:trnmatch tests this on synthetic terrain. With the Sun in the same place for the map and the descent image, 32 × 32-pixel templates matched a 6 m map well. The median error was 0.7 m, about a tenth of a pixel. When the Sun had moved 60° in azimuth, the median grew to 2.1 m. At 90° a third of matches failed outright. Real systems therefore plan landing times to match the lighting of the map, and reject outliers. Panel (c) shows the bigger lesson: with many landmarks, the matching error is not the limit. Errors in tying the map to the inertial frame, and in knowing the camera's attitude, dominate the final fix.

![Terrain-relative navigation on synthetic terrain. (a) A 6 m map with a 32 × 32-pixel descent template and its search window. (b) Error of single landmark matches as the Sun's azimuth changes between map and descent; dashed lines show the 90th percentile. (c) A position-fix error budget against altitude: the map tie and attitude knowledge dominate.](figures/out/ch48_trn.svg){#fig:trnmatch width=100%}

::: example
**Example: how accurate can terrain-relative navigation be?**

A lander carries a 6 m-pixel map tied to the inertial frame with 3 m (1σ) error. Its attitude is known to 0.03°. At 4 km altitude it matches $N$ = 15 landmarks, each with the median error of @fig:trnmatch for a modest lighting change: 0.86 m, or 0.14 pixel.

1. **Landmarks.** Averaging $N$ independent matches gives $0.86/\sqrt{15}$ = **0.22 m**.
2. **Attitude.** A pointing error $\delta\theta$ shifts the projected position by $h\,\delta\theta$ = 4 000 m × 5.2 × 10⁻⁴ rad = **2.09 m**.
3. **Map tie.** The map itself may sit 3 m from where the navigation frame thinks it is: **3.0 m**.
4. **Total.** Independent errors add in root-sum-square: $\sqrt{0.22^2 + 2.09^2 + 3.0^2}$ = **3.7 m**.

The answer is about ten times better than the 40 m requirement LVS had to meet, and matches its 5 m touchdown. Doubling the number of landmarks hardly helps. Halving the map-tie error helps most. With a 10 m map tie and 0.1° attitude knowledge, the same matcher gives 12 m.
:::

Other landers use similar ideas. China's Chang'e landers have hovered about 100 m above the Moon since 2013 to choose a safe spot with lidar and cameras (Chapter 27). Japan's SLIM matched craters in its descent images with an onboard crater map in January 2024. All 14 of its image-matching fixes were judged accurate, and its position error before the final hazard avoidance was under 10 m. NASA's **SPLICE** project packages TRN, hazard-detection lidar, a Navigation Doppler Lidar and a descent computer for commercial landers. On Intuitive Machines' IM-1 in February 2024, a safety switch left the lander's own laser rangefinders disabled. A software patch to use NASA's Doppler lidar instead reportedly failed for want of a data flag, and Odysseus landed on its side. In June 2025 ispace's second lander crashed after its laser rangefinder reported late. Sensors, not clever algorithms, cause most landing failures.

### Crater Detection with Learning

Craters are the natural landmarks of airless worlds. A crater-based navigator detects craters in the descent image, matches the pattern with a crater catalogue and solves for position. Classical detectors look for the bright-and-dark pair that a bowl makes in low sunlight, or correlate the image with crater templates. Learned detectors instead train a network on many labelled examples (Chapter 44). The best-known example, **DeepMoon** (2019), trained a U-Net on lunar elevation maps. It recovered 92 % of the craters in a human-made catalogue, roughly doubled the number of detections, and had an estimated 11 % false-positive rate among new finds.

@fig:craterdetect compares the two approaches on synthetic scenes. The template matcher was given an ideal crater rendered at the *true* Sun angle. The learned detector was a small numpy neural network with about 16 500 weights, trained in seconds on 29 689 patches from ten other scenes under random lighting. At a low Sun of 10°, both found craters equally well: average precision (the area under the precision–recall curve) was 0.56 and 0.62. As the Sun rose, shadows shrank and eroded craters faded. At 25° the template matcher dropped to 0.28, and at 45° to 0.09, while the network kept 0.57 and 0.34. At 65° both failed.

What matters for navigation is the **position fix**. Matching the 40 best detections to the catalogue with RANSAC gave errors of 0.2–0.8 m with templates at 10°. The network's fixes were slightly less precise, 0.5–1.7 m, because its sliding window is coarser. Template-based fixes locked onto wrong matches, more than 100 m off, in one of three scenes at 25° and in all scenes from 45° upwards. The network's fixes stayed within 3 m to 45° and mostly within 10 m at 65°. The learned detector was not more accurate, but it was more *robust*, because it had seen many lighting conditions. Synthetic tests flatter both methods; real images add blur and craters missing from the catalogue.

![Crater detection on synthetic lunar scenes with 5 m pixels. (a) The 100 highest-scoring detections of a small neural network at 25° Sun elevation; green circles match a catalogued crater. (b) Precision–recall curves for the network (solid) and template matching at the true Sun angle (dashed). (c) Average precision against Sun elevation. (d) Error of the position fix obtained by matching detections to the crater catalogue; the shaded band marks wrong matches.](figures/out/ch48_crater.svg){#fig:craterdetect width=100%}

### Small Bodies

Asteroids and comets are hard targets. Their gravity is weak and irregular, and maps must be built on arrival. **OSIRIS-REx** navigated to the Nightingale site on Bennu in October 2020 with **Natural Feature Tracking**. The spacecraft rendered the expected terrain from an onboard shape model and correlated it with its camera images. It touched down within about 1 m of its target. Japan's **Hayabusa2** dropped reflective target markers on Ryugu and homed in on them. Its second touchdown, in July 2019, was 60 cm from the aim point. ESA's Hera, due at Didymos in November 2026, relies on an autonomous "self-driving" navigation system around the pair.

@tbl:navsystems summarises the main onboard navigation systems.

| System | Mission | Sensor | Method | Reported accuracy |
|---|---|---|---|---|
| AutoNav | DS1, Stardust, Deep Impact | Camera | Asteroid and comet directions, filter | Comet impact, 2005 |
| SMART Nav | DART, 2022 | DRACO camera | Target centroiding, onboard guidance | Hit 160 m moonlet |
| Natural Feature Tracking | OSIRIS-REx, 2020 | Navigation camera | Rendered-template correlation | About 1 m |
| Target markers | Hayabusa2, 2019 | Camera, flash, rangefinder | Marker tracking | 60 cm |
| Lander Vision System | Perseverance, 2021 | Camera, inertial unit | Landmark correlation with maps | Within 5 m of aim |
| Hover and avoid | Chang'e 3–6, 2013–24 | Lidar, cameras | Hazard map at about 100 m | Safe landings |
| Crater matching | SLIM, 2024 | Camera | Crater detection and catalogue match | Under 10 m before avoidance |

: Onboard navigation systems that have flown. None used machine learning in its flight loop. {#tbl:navsystems}

## Pose Estimation for Rendezvous and Servicing

To dock with, inspect or capture another spacecraft, a chaser must know the target's **pose**: its position and its attitude relative to the camera (Chapter 40). A cooperative target carries markers, reflectors or radio beacons. A non-cooperative one — a dead satellite or a rocket stage — does not. Its pose must be estimated from images and the known shape alone, under harsh lighting that changes every few minutes.

### Keypoints and Perspective-n-Point

The most successful learned approach splits the task in two. First, a convolutional network finds the target in the image and predicts the pixel positions of a few **keypoints** — corners, antenna tips, nozzle centres — whose 3-D positions on the target are known. Second, a geometric solver recovers the pose. A point $\mathbf{X}_i$ on the target appears in the image at

$$ \mathbf{u}_i = \pi\big(K(R\,\mathbf{X}_i + \mathbf{t})\big), $$

where $R$ and $\mathbf{t}$ are the rotation and translation, $K$ holds the camera's focal length and centre, and $\pi$ divides by depth. The **Perspective-n-Point (PnP)** solver finds the $R$ and $\mathbf{t}$ that minimise the squared reprojection error $\sum_i \lVert \mathbf{u}_i - \hat{\mathbf{u}}_i \rVert^2$. **RANSAC** (random sample consensus) protects it from wrong keypoints. It fits poses to many small random subsets, keeps the pose that most points agree with, and refits on those "inliers". This split is popular because the network does what networks are good at — recognising image patterns — and the geometry stays exact and checkable.

Keypoint errors become pose errors as shown in @fig:pnpnoise, for a camera like the one used in the Stanford–ESA challenges and an 11-keypoint target. At 15 m range, keypoint noise of 1 pixel gave a median attitude error of 0.35° and a position error of 0.2 % of range. At 8 pixels the attitude error grew to about 3°. Doubling the range roughly doubled the error, because the target covers fewer pixels. Two badly misplaced keypoints out of 11 ruined a plain least-squares fit, giving a pose score of about 0.4. RANSAC restored almost the full accuracy.

![Pose from keypoints by Perspective-n-Point. (a) True and noisy keypoints on a satellite-like target, with one outlier. (b) Median attitude error against keypoint noise at three ranges. (c) Mean pose score at 15 m, with and without two outliers and with RANSAC; dotted lines mark the winning scores of the 2019 and 2021 challenges.](figures/out/ch48_pnp.svg){#fig:pnpnoise width=100%}

### The ESA–Stanford Challenges and the Domain Gap

Two open competitions shaped this field. In the **Satellite Pose Estimation Challenge** of 2019, run by ESA's Advanced Concepts Team and Stanford's Space Rendezvous Laboratory, 48 teams estimated the pose of the PRISMA mission's Tango satellite. The data set held about 15 000 rendered images and 305 laboratory photographs of a mock-up. The score adds the attitude error in radians to the position error divided by range. The winner, from the University of Adelaide, used keypoints and PnP. It scored 0.0094 on rendered test images, about 0.4° and 3 cm. On real photographs its score was 0.375, forty times worse.

That jump is the **domain gap**: networks trained only on rendered images meet real images with different noise, reflections and lighting (Chapter 45). The 2021 challenge attacked it directly. Teams trained on 59 960 rendered images and were tested on 9 531 hardware-in-the-loop images taken with two kinds of lighting: a "lightbox" imitating Earth glow and a "sunlamp" imitating direct sunlight. With heavy data augmentation, style randomisation and adaptation methods, the winning scores fell to about 0.06–0.07. By @fig:pnpnoise, such scores correspond to several pixels of keypoint noise, against well under a pixel on rendered images.

### Lidar and Sensor Fusion

Cameras fail in darkness and glare. **Lidar** measures range directly by timing laser pulses. Its point cloud is matched to the target's 3-D model, often with the **iterative closest point** algorithm, which pairs each measured point with the nearest model point and solves for the best rigid motion. Lidar works at any Sun angle but has fewer pixels and costs more power. Crew Dragon, ATV and the commercial servicers combine laser sensors with cameras.

## Guidance and Control: Optimisation or Learning?

Guidance decides the path; control makes the vehicle follow it. The key message of this section is that the most impressive autonomous guidance in flight today is **optimisation**, not learning. Learning is promising but much harder to verify.

### Convex Guidance

A powered landing must reach a target with zero velocity, using as little propellant as possible, without exceeding thrust limits or flying into the ground. The thrust magnitude has a lower bound as well as an upper one, because rocket engines cannot be throttled to zero. That lower bound makes the problem non-convex — it can have many local optima — and hard to solve reliably on board.

In 2007 Behçet Açıkmeşe and Scott Ploen at JPL showed a way out, called **lossless convexification**. They introduced a slack variable $\sigma$ for the thrust acceleration magnitude and wrote the constraints as

$$ \lVert \mathbf{u}(t) \rVert \le \sigma(t), \qquad \rho_{\min} \le \sigma(t) \le \rho_{\max}, \qquad \min \int_0^{t_f} \sigma(t)\, dt . $$

This relaxed problem is convex, so a solver finds its global optimum reliably and quickly. They proved that at the optimum $\lVert \mathbf{u} \rVert = \sigma$, so the relaxation loses nothing. The resulting **G-FOLD** algorithm (guidance for fuel-optimal large diverts) was flown on Masten's Xombie rocket in 2012–13. In July 2013 it diverted 750 m sideways at about 25 m/s. Its custom solver could compute a trajectory in about 100 ms on a 1.4 GHz processor. SpaceX engineers have described using convex optimisation to land Falcon 9 boosters. This is not machine learning: nothing is learned from data, and every answer can be checked against the constraints.

A 2-D version for a Mars landing can be solved by linear programming, approximating the circle $\lVert \mathbf{u} \rVert \le \sigma$ by a 16-sided polygon (@fig:gfoldlp). From 1 500 m altitude and 75 m/s descent, the convex method could reach targets from 2.5 km behind to 3.5 km ahead. A classical polynomial guidance law, with acceleration linear in time, could reach only from 250 m behind to 1.5 km ahead. Where both worked, the polynomial law used 5–8 % more Δv. The optimal thrust profile is "max–min–max": brake hard, coast at minimum thrust, then brake hard again.

![Fuel-optimal powered descent solved by linear programming (lossless convexification) compared with polynomial guidance. (a) Trajectories to targets at different distances; dashed lines show polynomial guidance where it is feasible. (b) Δv against target shift: convex guidance reaches a three times wider span of targets. (c) The optimal thrust profile for the largest shift.](figures/out/ch48_gfold.svg){#fig:gfoldlp width=100%}

### Reinforcement Learning

**Reinforcement learning (RL)** learns a control **policy** $\pi(a \mid s)$ — what action $a$ to take in state $s$ — by trial and error in a simulator. Each trial earns rewards $r_t$, and learning maximises the expected **return**

$$ J(\pi) = \mathbb{E}\Big[\sum_{t=0}^{T} \gamma^t\, r_t\Big], $$

where $\gamma \le 1$ discounts distant rewards. Policy-gradient methods nudge the policy's parameters in the direction that raises $J$. Simpler **policy-search** methods such as the cross-entropy method try many random parameter sets, keep the best few and sample around them. RL's appeal is that it needs no explicit model of the optimal solution, only a simulator and a reward.

In @fig:rllanding a small neural-network policy, with 12 hidden units and 49 weights, learns to land on the Moon in one dimension. Training used the cross-entropy method: 60 generations, 64 candidate policies each and 24 simulated landings per candidate — 92 160 landings in about 7 seconds. From generation 8 every landing in a validation set was soft (below 1.5 m/s). The policy then kept improving its fuel use, from 58 m/s of Δv to 31 m/s. A simple proportional–derivative (PD) controller that tracks a speed profile used 48 m/s. The learned policy had discovered a near-optimal "suicide burn": fall fast, then brake at full thrust at the last moment.

That efficiency is also its weakness. With 20 % less thrust than expected and faster starting speeds, the PD controller still landed softly 92 % of the time. The learned policy never did: its late braking left no margin. Research on landing, docking and attitude control shows the same pattern. RL policies match or beat classical controllers inside their training conditions but can fail abruptly outside them.

Real flights are beginning. In October 2025 the University of Würzburg's **InnoCube** CubeSat performed a full attitude manoeuvre with a controller trained by deep RL in simulation. Its team reported this LeLaR experiment as the first in-orbit demonstration of an AI-based attitude controller. On the ISS in February 2025, Stanford researchers used a neural network to give the Astrobee robot's trajectory optimiser a starting guess. Solver iterations fell by 50–60 %, and the optimiser still enforced every constraint. Learning that speeds up an optimiser, rather than replacing it, is the most likely route into flight.

### Verifying Learned Controllers

Classical controllers come with proofs such as stability margins and worst-case bounds. A neural-network policy has none by default. It may exploit flaws in the simulator and behave strangely in states it never saw. Testing can show the presence of failures but not their absence.

**Runtime assurance** offers a practical answer. In the *simplex* architecture, an untrusted high-performance controller runs inside a "safety envelope". A simple monitor checks every command. If the state approaches the edge of the envelope, a verified backup controller takes over. In @fig:rllanding the monitor computes the stopping distance at 70 % of rated thrust and orders full braking when it approaches the height. With this **shield**, the learned policy landed softly 92 % of the time in the shifted test, as often as the PD controller. The price was fuel: the shield acted in every landing, raising the nominal Δv from 31 to 42 m/s. Assurance methods, from formal verification of networks to simplex designs, are covered in Chapter 53.

![Learning to land, in one dimension on the Moon. (a) Return of a neural-network policy trained by the cross-entropy method, with a PD controller for comparison. (b) Height against speed for four landings; in the shaded region a runtime monitor would order full braking. (c) Soft landings in nominal conditions and with a weaker engine and faster starts, for the PD controller, the learned policy and the learned policy with a shield.](figures/out/ch48_rl.svg){#fig:rllanding width=100%}

@tbl:controlcompare compares the three approaches.

| Approach | How it decides | Guarantees | Flight status (2026) | Main risk |
|---|---|---|---|---|
| Classical (PD, LQR) | Fixed feedback law | Stability margins | Universal | Wastes fuel and envelope |
| Convex optimisation | Solves an optimisation on board | Global optimum; checkable | Rocket landing; G-FOLD tests | Solver time; model errors |
| Learned policy (RL) | Network trained in simulation | Statistical testing only | First flight tests (2025) | Fails outside training |
| Learned + runtime assurance | Network inside a monitored envelope | From verified monitor and backup | Research | Conservative envelope |
| Learned warm start | Network guesses, optimiser solves | Optimiser's guarantees kept | ISS test (2025) | A bad guess slows the solver |

: Ways to compute guidance and control on board, from fixed laws to learned policies. {#tbl:controlcompare}

## Rendezvous, Docking and Proximity Operations

Automated docking is the oldest everyday autonomy in human spaceflight. The key idea is a strict sequence of hold points and approach corridors (Chapter 40), with the chaser flying itself and humans or the ground able to stop it at any time.

Soviet spacecraft have docked automatically since 1967, with the Igla system and, from 1986, the Kurs radio system still used by Soyuz and Progress. Europe's five **Automated Transfer Vehicles** (2008–2014) docked with the ISS using relative GPS, then laser rangefinders and a camera-based "videometer" reading retroreflectors (@fig:atvjulesverne). **Crew Dragon** docked itself for the first time in March 2019, using lidar and visible and thermal cameras. China has made automated rendezvous fast. Tianzhou-5 docked with the Tiangong station 2 hours 7 minutes after launch in November 2022, a world record. Shenzhou-21 brought its crew in about 3.5 hours in 2025.

::: figrow
![ESA's first Automated Transfer Vehicle, Jules Verne, approaching the ISS during a rehearsal of its automated approach on 31 March 2008.](figures/photos/ch48_atvjv.jpg){#fig:atvjulesverne}

![Crew Dragon on its first crewed approach to the ISS on 31 May 2020, nose cone open to show the docking mechanism.](figures/photos/ch48_dm2.jpg){#fig:dm2approach}
:::

Servicing adds non-cooperative targets. DARPA's Orbital Express captured its partner autonomously in 2007, and Northrop Grumman's MEV-1 docked with Intelsat 901 in 2020. Astroscale's ADRAS-J approached a spent rocket stage to about 15 m in 2024. Learned pose estimation is the main entry point for AI here. The systems are compared in @tbl:rpoautonomy.

| Vehicle | First automated docking | Relative sensors | Who decides | Typical time to dock |
|---|---|---|---|---|
| Soyuz, Progress | 1967 (Igla); Kurs from 1986 | Radio (Kurs) | Onboard; crew backup (TORU) | 3 h – 2 days |
| ATV | 2008 | Relative GPS, laser, videometer | Onboard; ground can abort | About 10 days (ATV-4) |
| Crew Dragon | 2019 | Lidar, visible and thermal cameras | Onboard; crew monitors | About 1 day |
| Shenzhou, Tianzhou | 2011 | Radar, laser, cameras | Onboard; manual backup | 2 h 7 min to 6.5 h |
| MEV-1, MEV-2 | 2020 | Cameras, infrared, lidar | Onboard; ground go/no-go | Days to weeks |
| ADRAS-J | 2024 (approach only) | Cameras, lidar | Onboard; ground holds | Months |

: Automated rendezvous and docking systems. Most combine onboard control with human go/no-go decisions at hold points. {#tbl:rpoautonomy}

## Robots and Swarms

Robots are where autonomy is most visible. The key idea is that a robot's usefulness grows with the distance it can safely go, or the work it can safely do, between two contacts with its operators.

### Rover Autonomy

A Mars rover drives in three ways (Chapter 28). In a **blind drive**, operators plan a path through terrain they have seen in stereo images, and the rover follows it with **visual odometry** — tracking features between images to measure its true motion. In **AutoNav**, the rover builds its own 3-D map, scores each patch for slope, rocks and steps, and chooses paths towards a goal. Perseverance's **Enhanced AutoNav** adds "thinking while driving". A dedicated vision processor makes the maps while the wheels turn. An algorithm called Approximate Clearance Evaluation checks whether the rover's body can clear the rocks along each candidate path.

The benefit is large (@fig:roverdist). Spirit and Opportunity used their early AutoNav for about 5 % of their driving, and Curiosity for about 6 %. Perseverance used AutoNav for more than 90 %. On 11 October 2026 it passed Opportunity's off-world driving record, reaching 45.22 km in about five and a half years. Opportunity needed nearly fifteen years for the same distance. Perseverance can cover up to 412 m in a sol.

![Why rovers drive themselves. (a) Modelled distance per sol against one-way light-time for teleoperation with a continuous link, a single ground-planned drive per sol, and two kinds of onboard autonomy. (b) Share of distance driven autonomously by NASA's Mars rovers.](figures/out/ch48_rover.svg){#fig:roverdist width=96%}

::: example
**Example: how much autonomy does a Mars rover need?**

Assume a one-way light-time of 20 minutes and one uplink of commands per sol. The rover can drive for 3.5 hours a day at a top speed of 4.2 cm/s.

1. **Teleoperation.** Even with a continuous link, each 10 m step takes 238 s of driving and 2 400 s of round-trip light-time. Add a minute to decide, and a step takes 2 698 s. In 3.5 hours that is 4.7 steps, or **47 m**.
2. **Ground planning.** With one uplink per sol, operators can plan only as far as their images show, about **40 m** of blind driving.
3. **Onboard autonomy.** At an average of 110 m/h while thinking while driving, the rest of the window adds about 356 m, giving about **400 m** per sol.
4. **Decisions.** If AutoNav assesses the terrain about once per metre, a 400 m drive needs about 400 hazard decisions. The ground can make one set of decisions per sol.
5. **Faults.** If a fault happens just after the morning uplink, the team may not hear of it for several hours, until the next relay pass. The rover must make itself safe (F1) and often continue (F2).

So driving needs event-driven autonomy (E3), resource-aware re-planning helps (E4), and fault handling must be F1–F2. To cross 10 km, ground planning alone would need about 250 driving sols; autonomy needs about 25.
:::

Autonomy also chooses what to study. **AEGIS** (Autonomous Exploration for Gathering Increased Science) finds rocks in navigation-camera images after a drive and points a laser spectrometer at the best one, without waiting for the ground (@fig:aegisrock). On Curiosity from 2016 it selected the scientists' preferred kind of target over 93 % of the time, against about 24 % expected without it. By May 2026 it had picked 596 targets on Curiosity and 293 on Perseverance.

![A rock targeted by AEGIS on Perseverance on 18 May 2022, one of the first two chosen by the software for SuperCam without input from Earth. The red marks show the laser spots.](figures/photos/ch48_aegis.jpg){#fig:aegisrock width=50%}

The newest step moves AI into route planning on the ground. On 8 and 10 December 2025, Perseverance drove 210 m and 246 m along waypoints chosen by generative vision-language models from orbital images. Before upload, engineers checked the commands in JPL's digital twin of the rover, covering more than 500 000 telemetry variables. Onboard AutoNav stayed in charge of safety.

### Arms, Free-Flyers and Humanoids

Robot arms in space are mostly supervised rather than autonomous. **Canadarm2** (2001) and **Dextre** (2008) on the ISS are driven by ground controllers or crew. Ground teams run pre-planned, automatic motion sequences for routine jobs, while astronauts usually fly the capture of cargo ships. Canada's **Canadarm3** was designed for the Gateway station. After NASA paused Gateway in March 2026, its builder MDA Space continued under its Canadian Space Agency contract, refocused on lunar-surface logistics, with launch no earlier than 2029.

Inside the ISS, three cube-shaped **Astrobee** free-flyers have operated since 2019. They navigate by matching camera images to a map of the station, move with electric fans and serve as a test bed for autonomy research (@fig:astrobeefly). **Robonaut 2**, the first humanoid robot in space, worked on the ISS from 2011 to 2018. It was mostly teleoperated, testing whether a dexterous robot could use tools and switches made for people (@fig:robonautlab). The Japanese start-up **GITAI** tested an arm inside the commercial Bishop airlock in 2021. In March 2024 it mounted a second arm outside and performed assembly and servicing tasks, reaching technology readiness level 7.

::: figrow
![An Astrobee free-flying robot during a Zero Robotics student programming demonstration on the ISS on 1 May 2024.](figures/photos/ch48_astrobee.jpg){#fig:astrobeefly}

![Robonaut 2 in the ISS Destiny laboratory on 2 January 2013, operating valves on a task board under remote command from the ground.](figures/photos/ch48_robonaut.jpg){#fig:robonautlab}
:::

### Swarms, Formations and Constellations

Spacecraft working together must know where the others are and agree on who does what. The Swedish-led **PRISMA** mission (2010) demonstrated autonomous formation flying with two satellites, Mango and Tango — the Tango of the 2019 pose challenge. ESA's **Proba-3**, launched in December 2024, flies two satellites about 150 m apart. One casts a precise shadow on the other's coronagraph to create artificial solar eclipses. Holding the formation to about a millimetre needs onboard control, using GPS, star trackers, lasers and radio links. Its first eclipse images were taken in May 2025, and it was commissioned for autonomous formation flying in June 2025.

NASA's **Starling** mission (July 2023) flew four CubeSats to test swarm autonomy. Its Distributed Spacecraft Autonomy software let the satellites share observations of the ionosphere over crosslinks and plan follow-up measurements together. Its StarFOX experiment tracked swarm members and other objects with commercial star trackers. On the Moon, the **CADRE** project will land three suitcase-sized rovers that explore and map as a team without moment-to-moment commands (@fig:cadreyard). It is due to fly on Intuitive Machines' IM-3, no earlier than early 2027.

![A development model of a CADRE rover on its first autonomous drive in JPL's Mars Yard in June 2023. Three such rovers are to map the Moon together as a team.](figures/photos/ch48_cadre.jpg){#fig:cadreyard width=56%}

At constellation scale, autonomy is already routine. Starlink satellites receive conjunction warnings and plan and execute avoidance manoeuvres themselves.

::: data
**Starlink's autonomous collision avoidance in numbers**

- **Volume.** From 1 December 2025 to 31 May 2026, Starlink satellites made 207 152 propulsive collision-avoidance manoeuvres: 65 137 by first-generation and 142 015 by second-generation satellites. The previous six months saw 148 696.
- **Rate.** That is about 36 manoeuvres per satellite per year for the first generation and 46 for the second.
- **Threshold.** SpaceX manoeuvres when the probability of collision exceeds 3 in 10 million (3 × 10⁻⁷), plus miss-distance criteria. The common industry threshold is 1 in 10 000.
- **Misses.** The onboard system ran without system-wide outages. In 22 individual cases the targeted risk was not reduced, mostly because predictions of the other object were poor or arrived too late. Newly launched satellites not yet tracked and short Space-Track.org outages were among the causes.
- **New sensing.** In January 2026 SpaceX announced Stargaze, which uses about 30 000 Starlink star trackers to spot nearby objects. It aims to screen conjunctions in minutes rather than hours.

Source: SpaceX semi-annual report to the US Federal Communications Commission, mid-2026; SpaceX announcements.
:::

::: example
**Example: collision-avoidance decisions for a 10 000-satellite constellation**

Assume Starlink's second-generation rate of 46 manoeuvres per satellite per year.

1. **Per year.** 10 000 × 46 = **460 000** manoeuvres.
2. **Per day and hour.** 460 000 / 365.25 = 1 259 a day, or 52 an hour — one every **69 s**, day and night.
3. **Human review.** If each decision took an analyst 10 minutes, that would be 210 person-hours a day. At about 1 800 working hours per person per year, it would need about **43 full-time analysts** for this task alone.

This is why the decision is automated: humans set the thresholds and handle the exceptions, while the satellites plan and execute routine manoeuvres. The weak point moves from deciding to *knowing*: most failures come from poor tracking data about the other object (Chapter 50).
:::

@tbl:robotstatus gives the status of the robotic systems discussed.

| System | Type | Autonomy | Status, October 2026 |
|---|---|---|---|
| Perseverance | Mars rover | Enhanced AutoNav, onboard planner, AEGIS | Operating; record 45.22 km; extended to about 2028 |
| Canadarm2, Dextre | ISS arms | Supervised; automated routine motions | Operating |
| Canadarm3 | Lunar arm system | Planned supervised autonomy | Refocused on lunar surface; NET 2029 |
| Astrobee | ISS free-flyers | Map-based navigation; research autonomy | Operating since 2019 |
| GITAI S2 | Arm on Bishop airlock | Autonomous and teleoperated tasks | Demonstrated 2024 |
| Starling | 4-CubeSat swarm | Distributed planning, star-tracker navigation | Extended mission to end of 2025 |
| CADRE | 3 lunar rovers | Cooperative mapping | Awaiting IM-3, NET early 2027 |
| Proba-3 | 2-satellite formation | Millimetre formation control | Operating since 2025 |

: Robots, swarms and formations with onboard autonomy. NET means no earlier than. {#tbl:robotstatus}

::: note
**Practice: designing and verifying an autonomy function with a runtime monitor**

1. **State the decision.** Write down what the function decides, how often, and what a wrong decision costs. Example: "choose a safe landing point within 10 s, with at most one hazardous choice in 10 000 landings".
2. **Define the operating domain.** List the conditions it must handle — Sun angles, terrain, sensor noise, speeds — and which of them the training data cover.
3. **Build the simplest baseline.** Start with a classical method, such as a template, a PD law or a greedy rule. A learned method must beat it by a measured margin.
4. **Design the safety envelope.** Write simple, checkable rules the system must never break, such as stopping distance or keep-out zones, and a backup that always keeps it inside them.
5. **Add the monitor.** Make it independent of the learned component, and simple enough to verify exhaustively or formally.
6. **Test in layers.** Run millions of randomised simulations, then hardware-in-the-loop tests. Report failure rates with confidence intervals, and test outside the domain too.
7. **Measure the cost of safety.** Record how often the monitor intervenes and what that costs. Frequent interventions mean the learned part or the envelope needs work.
8. **Fly in shadow mode first.** Run the function on board without letting it act, compare its choices with the existing system, then give it authority step by step.
:::

::: key
**Key takeaways**

- Spacecraft need autonomy when the ground cannot respond fast enough, often enough or cheaply enough. Light-time, contact gaps, fleet size and event speed set the level; ECSS defines E1–E4 for execution, D1–D2 for data and F1–F2 for failures.
- Most autonomy in flight is search, estimation and optimisation, not learning: executives, fault protection, diagnosis, planners, optical navigation and convex guidance.
- Learning has entered through perception and science: crater detection, keypoint networks for pose and rover science targeting. Learned detectors are often more robust to lighting than templates, but not more precise.
- Terrain-relative navigation can reach metre-level accuracy. Map registration and attitude knowledge, not image matching, usually limit it, and sensors cause most landing failures.
- Reinforcement learning can find efficient policies but may fail abruptly outside its training conditions. Runtime monitors with verified backups, and learning that speeds up an optimiser, are the practical routes to flight.
- Autonomy is now routine at scale: Perseverance drives itself for over 90 % of its distance, and Starlink satellites made over 200 000 autonomous avoidance manoeuvres in six months.
:::

::: questions
**Review questions**

1. Using $T_\mathrm{ground} = 2\tau + 2W + T_\mathrm{decide}$, estimate the ground response time for a Jupiter orbiter with 43 minutes of one-way light-time and 8 hours of contact a day. Which ECSS execution level does a 2-hour science event require?
2. Explain the difference between levels F1 and F2. Give one mission for which F1 is enough and one that needs F2, with reasons.
3. Describe the three layers of an autonomous spacecraft and their time scales. Where are learned models most often used, and why?
4. How does model-based diagnosis choose between explanations of a fault? Why does the prior probability favour explanations with few failed components?
5. In @fig:obssched, why does a greedy rule fall short of the optimum, and why might a flight planner still use one? What property of Perseverance's onboard planner keeps its run time bounded?
6. Why does normalised cross-correlation tolerate changes in brightness but not in Sun direction? Give two ways a landing system can cope.
7. Repeat the terrain-relative navigation example for a 12 m map, 150 landmarks, a 5 m map tie and 0.05° attitude knowledge at 3 km. Which term dominates?
8. In the 2019 pose-estimation challenge, the winning score was forty times worse on real images than on rendered ones. What is this gap called, and what methods narrowed it in 2021?
9. Why is G-FOLD not machine learning? What does lossless convexification achieve?
10. In @fig:rllanding, why did the learned policy fail with a weaker engine, and how did a runtime monitor restore safety? What did the monitor cost?
:::
