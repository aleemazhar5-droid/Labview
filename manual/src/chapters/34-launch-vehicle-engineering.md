---
title: Launch Vehicle Engineering
hero: ch34
abstract: A launch vehicle must accelerate its payload to nearly 8 km/s in under ten minutes while carrying all of its own propellant and surviving aerodynamic loads, noise, vibration and heat — reliably and cheaply. This chapter explains how engineers meet that challenge. It builds the velocity budget and shows how launch latitude changes it, derives the rocket equation and the logic of staging, follows a simulated two-stage kerosene vehicle from the pad to orbit, and describes tanks, pressurisation, guidance and flight termination. It then turns to the environments a payload must survive, the payload penalty of landing a booster, the economics of launch, and what seventy years of launch statistics reveal about reliability.
---

A rocket standing on the pad is mostly propellant. A Falcon 9 weighs about 549 t at lift-off, almost 490 t of it liquid oxygen and kerosene; the satellites on top make up only 3–4 % of the total. Within about eight minutes it must lift its payload above the atmosphere and accelerate it to 7.8 km/s. Launch is the shortest phase of most missions and the most violent: the payload meets its highest loads, loudest noise and strongest vibration in its first minutes of flight.

To keep the numbers concrete, this chapter follows a **reference vehicle**: a planar trajectory simulation of a two-stage kerosene rocket with Falcon 9-class masses and engines, flown from Cape Canaveral to a 200 km orbit (@fig:lvascent). The engines themselves are the subject of Chapter 35, the world's launch vehicles of Chapter 36, and launch sites and ground systems of Chapter 37; the orbital mechanics used here is developed in Chapter 3.

## Getting to Orbit

### The Velocity Budget

A satellite in a circular orbit 200 km above Earth moves at 7.78 km/s. Each kilogram carries about 30 MJ of kinetic energy and almost 2 MJ of potential energy. The launch vehicle supplies it by throwing propellant backwards, and the measure of what it can do is the **velocity change** Δv it can give itself (@fig:lvdvbudget).

::: formula
**The rocket equation**

A rocket of mass $m$ ejects propellant at speed $v_e$ relative to itself. When it expels a small mass $-dm$, conservation of momentum gives $m\,dv = -v_e\,dm$. Integrating from the initial mass $m_0$ to the final mass $m_f$:

$$\Delta v = v_e \ln\frac{m_0}{m_f} = I_{sp}\, g_0 \ln\frac{m_0}{m_f}$$

where $I_{sp}$ is the specific impulse (Chapter 35) and $g_0$ = 9.806 65 m/s². The ratio $m_0/m_f$ is the **mass ratio**. The equation, published by Konstantin Tsiolkovsky in 1903, gives the velocity change in empty space, with no gravity or air.
:::

![Left: Δv budget of the simulated reference ascent to a 200 km circular orbit from Cape Canaveral. Earth's rotation reduces the requirement by 0.41 km/s; gravity and steering losses add about 1.5 km/s. Right: how launch-site latitude changes the eastward surface speed and the Δv a satellite needs to turn a geostationary transfer orbit into a geostationary one.](figures/out/ch34_dvbudget.svg){#fig:lvdvbudget width=98%}

Four **losses** separate this ideal Δv from the final orbital speed:

- **Gravity loss**, $\int g \sin\gamma \, dt$, where γ is the flight-path angle above the horizontal: while the rocket climbs, part of its thrust only holds it up. A rocket that hovered would burn all its propellant and gain nothing.
- **Drag loss**, $\int D/m \, dt$, the momentum given to the air.
- **Steering loss**, $\int (T/m)(1-\cos\alpha)\,dt$, when the thrust $T$ points at an angle α away from the velocity.
- **Back-pressure loss**: a nozzle produces less thrust in the atmosphere than in a vacuum (Chapter 35).

Earth's rotation helps, because the pad already moves east:

$$\Delta v_{ideal} = v_{orbit} - v_{rotation} + \Delta v_{gravity} + \Delta v_{drag} + \Delta v_{steering} + \Delta v_{pressure}$$

@fig:lvdvbudget shows the terms for the reference vehicle, integrated along its simulated trajectory: it needs an ideal Δv of 9.00 km/s. Gravity loss (0.92 km/s) is the largest. Steering loss (0.62 km/s) is almost as large, because the second stage, whose thrust is less than its weight at ignition, must point its nose above the flight path to avoid falling back while it gains speed — trading gravity loss for steering loss. Drag costs only 0.02 km/s, because a large, dense vehicle has so much mass per unit of frontal area; small launchers lose more, often 0.1–0.2 km/s. Without the 0.41 km/s gift of Earth's rotation the reference vehicle would need 9.4 km/s, consistent with the usual rule of thumb of 9.3–9.6 km/s to low Earth orbit (LEO).


### Latitude and Inclination

The ground at latitude φ moves east at 465 m/s × cos φ. A rocket launched on azimuth *Az* (measured from north) into an orbit of inclination *i* must satisfy sin *Az* = cos *i* / cos φ, and the useful part of the rotation it inherits works out to 465 m/s × cos *i* — it depends only on the orbit, not the site. A launch due east gives the lowest inclination reachable directly, *i* = φ. A launch to the International Space Station (51.6°) gains 289 m/s; a polar orbit gains nothing; a sun-synchronous orbit, inclined about 97–98°, is slightly retrograde and costs about 60 m/s extra.

Reaching an inclination *lower* than the site latitude needs a **dog-leg** (steering sideways during ascent) or a plane change in orbit, both expensive: at orbital speed each degree costs 2*v* sin 0.5° ≈ 136 m/s. Latitude therefore matters most for geostationary missions (@tbl:lvsites). A satellite released into a geostationary transfer orbit (GTO) inclined at the site latitude must remove that inclination at apogee, where it moves slowly and plane changes are cheapest, while circularising. From Kourou (5.2° N) this costs 1.49 km/s; from Cape Canaveral (28.5° N), 1.84 km/s; from Baikonur (45.9° N), 2.27 km/s. For a satellite with a 320 s apogee engine, the 0.35 km/s difference between Kourou and the Cape raises the propellant share of its mass from 38 % to 44 %. Alternatives are a "supersynchronous" transfer, whose higher apogee makes the plane change cheaper, or direct injection into geostationary orbit by the upper stage.

| Launch site | Latitude | Eastward surface speed | GTO → GEO Δv |
|---|---|---|---|
| Kourou (Guiana Space Centre) | 5.2° N | 463 m/s | 1.49 km/s |
| Sriharikota (India) | 13.7° N | 452 m/s | 1.57 km/s |
| Wenchang (China) | 19.6° N | 438 m/s | 1.66 km/s |
| Cape Canaveral / Kennedy | 28.5° N | 409 m/s | 1.84 km/s |
| Mahia (New Zealand) | 39.3° S | 360 m/s | 2.10 km/s |
| Baikonur (Kazakhstan) | 45.9° N | 324 m/s | 2.27 km/s |
| Plesetsk (Russia) | 62.9° N | 212 m/s | 2.74 km/s |

: Latitude effects at selected launch sites. GTO → GEO Δv assumes a 200 km perigee and an inclination equal to the site latitude. {#tbl:lvsites}

::: example
**Example: the Δv budget to a 500 km, 53° orbit from Cape Canaveral**

1. Launch azimuth: sin *Az* = cos 53° / cos 28.5° = 0.602 / 0.879 = 0.685, so *Az* = 43° — the vehicle flies north-east along the US coast.
2. Earth-rotation gain: 465 × cos 53° = 280 m/s, instead of 409 m/s for a due-east launch.
3. Insertion into a 200 km parking orbit (7 784 m/s), then a Hohmann transfer to 500 km: 86 m/s to raise apogee plus 85 m/s to circularise (Chapter 3).
4. Ascent losses from @fig:lvdvbudget: 0.92 + 0.62 + 0.02 + 0.06 = 1.62 km/s.
5. Ideal Δv = 7 784 − 280 + 1 620 + 172 ≈ 9 300 m/s, 0.30 km/s more than the due-east 200 km orbit — about 2.3 t of droneship payload in the model of @fig:lvperf. This is one reason constellations are often deployed low and raise their own orbits with electric propulsion.
:::

## Staging

### Why One Stage Is Not Enough

Every stage carries structure — tanks, engines, plumbing, avionics — that becomes dead weight once its propellant is gone. It is described by the **structural ratio** ε = $m_s/(m_s + m_p)$, the structure's share of a loaded stage; good modern stages achieve ε ≈ 0.05–0.10. A single stage with an average specific impulse of 330 s that must deliver 9.3 km/s needs a mass ratio of $e^{9300/3236}$ = 17.7: only 5.6 % of the lift-off mass may remain at burnout. If structure alone takes 8 %, the rocket cannot reach orbit even empty. This is the fundamental difficulty of **single-stage-to-orbit** vehicles, studied for decades but never flown to orbit (Chapter 10).

### The Rocket Equation for Several Stages

Staging throws structure away as soon as it is empty. Each stage *k* contributes $\Delta v_k = v_{e,k} \ln(m_{0,k}/m_{f,k})$, where the "payload" of stage *k* is everything above it, and the contributions add. For *n* identical stages the optimum is an equal split of Δv, and the overall payload fraction is

$$\frac{m_{payload}}{m_0} = \left(\frac{e^{-\Delta v/(n v_e)} - \varepsilon}{1-\varepsilon}\right)^{n}$$

@fig:lvstaging evaluates this formula. Going from one stage to two turns an impossible vehicle into one that delivers 3 % of its lift-off mass; a third stage adds about a fifth more; beyond that the gains are small, while every extra stage adds engines, a separation event, an in-flight ignition and cost. Most modern launchers therefore have two stages. Real stages are not identical: hydrogen upper stages (Isp near 450 s) take a larger share of the Δv, and a reusable first stage is given a *smaller* share so that it separates slowly and close to the launch site.

![Left: payload fraction for a 9.3 km/s mission as a function of the number of identical stages and their structural ratio. Right: payload fraction versus total Δv for one, two and three stages with ε = 0.08; a single stage runs out of capability just above 8 km/s.](figures/out/ch34_staging.svg){#fig:lvstaging width=96%}

::: example
**Example: two stages versus one**

Take Isp = 330 s ($v_e$ = 3 236 m/s), Δv = 9.3 km/s and a lift-off mass of 550 t.

1. One stage, ε = 0.08: the final-to-initial mass ratio is $e^{-9300/3236}$ = 0.0565, less than ε, so no payload is possible. Even with an exceptionally light structure (ε = 0.05) the payload fraction is (0.0565 − 0.05)/0.95 = 0.7 %, or 3.8 t.
2. Two equal stages, ε = 0.08: each provides 4.65 km/s, so $e^{-4650/3236}$ = 0.238; each stage's payload ratio is (0.238 − 0.08)/0.92 = 0.171, and the overall fraction is 0.171² = 2.9 %, or **16 t**.
3. With ε = 0.06 this rises to 3.6 % (19.6 t); with ε = 0.10 it falls to 2.3 % (12.9 t). Each percentage point of structural ratio is worth about 1.7 t of payload, a tenth of the total, which is why engineers fight for every kilogram of tank wall.
:::

### Serial, Parallel and Cross-Feed

In **serial** staging the stages sit on top of one another and fire in sequence, as in the Saturn V (@fig:siistack) and Falcon 9. In **parallel** staging, boosters strapped around a core ignite on the ground and drop away first: the R-7 of 1957, ancestor of today's Soyuz, uses four; Ariane 6 uses two or four solid boosters; the Space Launch System (SLS) two; Falcon Heavy two Falcon 9 first stages. Parallel staging avoids lighting engines in flight, but the core must carry side loads. The Space Shuttle's orbiter engines burned propellant from an external tank that was discarded just short of orbit (@fig:etseparation). **Cross-feed** — pumping propellant from the boosters into the core so that its tanks are still full when they separate — would give serial-staging performance with parallel hardware; it was proposed for Falcon Heavy but has not flown.

::: figrow
![The second stage (S-II) of the Saturn V for Apollo 6 being lowered onto the first stage in the Vehicle Assembly Building in 1967. Serial staging stacks each stage on top of the previous one.](figures/photos/ch34_sii.jpg){#fig:siistack}

![The Space Shuttle's external tank falling away after separation in March 1989 (STS-29), photographed from Discovery. The tank fed the orbiter's main engines and was discarded just short of orbit.](figures/photos/ch34_etsep.jpg){#fig:etseparation}
:::

## The Ascent Trajectory

### Lift-Off, Pitch-Over and the Gravity Turn

A liquid-fuelled vehicle ignites its engines a few seconds before release and is held down while its computers confirm that every engine is running normally; if not, it shuts down safely on the pad. At release its thrust-to-weight ratio is typically 1.2–1.5 (1.44 for the reference vehicle). It rises vertically to clear the tower, rolls to its launch azimuth, then makes a small **pitch-over** — 4.8° between 8 and 18 s in the simulation. In a **gravity turn** the vehicle keeps its nose along the airflow, at nearly zero **angle of attack** α, and gravity gradually bends the path towards the horizontal, which keeps the aerodynamic side force and the bending of the long, thin structure small. The pitch-over sets the whole first-stage trajectory: too small and the rocket climbs too steeply; too large and it stays too long in thick air. The simulation chooses it to maximise payload.

**Dynamic pressure**, $q = \tfrac{1}{2}\rho v^2$, rises as the vehicle accelerates and falls as the air thins; its peak, **max-Q**, is typically 25–40 kPa. In the simulation it reaches 34 kPa at T+53 s, 8 km up, just after Mach 1; the Falcon 9 user's guide lists max-Q at T+67–74 s. The engines are throttled through a **throttle bucket** (75 % in the simulation) to limit it. What matters most for the structure is the product **qα**: a gust or **wind shear** at high dynamic pressure forces a non-zero angle of attack and bends the vehicle. Balloons and wind profilers measure the upper winds before each launch, and the trajectory is "wind-biased" and the loads recomputed to confirm that they stay within limits.

![Simulated ascent of the reference vehicle to a 200 km orbit with a droneship booster recovery. Altitude climbs steeply while speed builds slowly; max-Q is limited by throttling the first stage; the sensed acceleration rises as propellant burns off, is capped at 4.5 g, and drops to zero during the coast between staging and second-stage ignition.](figures/out/ch34_ascent.svg){#fig:lvascent width=100%}

As propellant burns off, acceleration grows (@fig:lvascent) from 1.4 g towards 4–5 g, where vehicles cap it by throttling or shutting down engines.

### Staging, Fairing Jettison and the Upper Stage

At **main-engine cut-off** (MECO), 147 s after lift-off, the reference first stage is 65 km up and moving at 2.5 km/s relative to the air. Pneumatic pushers separate the stages, and the second stage coasts briefly while its propellant settles before igniting. The **payload fairing** is jettisoned once the aerodynamic heating it would let through is negligible: Falcon releases it when the **free-molecular heating** rate, ½ρv³, falls below 1 135 W/m², which in the simulation happens at T+199 s and about 109 km.

The upper stage then flies above the atmosphere under closed-loop guidance. Its thrust-to-weight ratio is only 0.85 at ignition, so it pitches up to hold altitude while it accelerates; by **second-engine cut-off** (SECO) at T+477 s its acceleration has climbed above 4 g. For higher orbits the stage usually stops in a low **parking orbit**, coasts, and restarts to raise the apogee (@tbl:f9timeline). Restarting after a long coast requires settling the propellant with small thrusters and keeping engine and propellants within temperature limits. Afterwards a responsible stage performs a **deorbit burn** or vents its propellant and pressurant to "passivate" itself, so that it cannot explode and add to the debris population (Chapter 21).

| Event | LEO mission | GTO mission |
|---|---|---|
| Lift-off | T+0 | T+0 |
| Maximum dynamic pressure | T+67 s | T+74 s |
| First-stage main-engine cut-off | T+145 s | T+147 s |
| Stage separation | T+148 s | T+151 s |
| Second-stage ignition (1) | T+156 s | T+158 s |
| Fairing separation | T+195 s | T+222 s |
| Second-stage cut-off (1) | T+514 s | T+484 s |
| Second-stage ignition (2) | T+3 086 s | T+1 636 s |
| Second-stage cut-off (2) | T+3 090 s | T+1 696 s |
| Spacecraft separation | T+3 390 s | T+1 996 s |

: Sample Falcon 9 flight timelines from the Falcon User's Guide (May 2025). Every mission's profile is different. {#tbl:f9timeline}

## Structures and Materials

### Tanks, Domes and Stiffeners

A launch vehicle is essentially a stack of thin-walled pressure vessels with engines at one end and a payload at the other (@fig:lvanatomy). A first stage 3.7 m across has tank walls only a few millimetres thick, and structure is typically 5–8 % of its loaded mass.

![Anatomy of a two-stage kerosene launch vehicle. The first stage carries its oxygen tank above its fuel tank, with a common dome between them and a feed line running through the fuel tank; the composite interstage houses the second stage's vacuum engine; the fairing, lined with acoustic blankets, encloses the payload on its adapter.](figures/out/ch34_anatomy.svg){#fig:lvanatomy width=100%}

**Aluminium alloys** have been the standard since the 1950s (@tbl:tankmaterials). The Saturn V's first stage, the original Shuttle external tank and the SLS core stage use alloy 2219, which welds well and stays tough at cryogenic temperatures. **Aluminium–lithium** alloys are lighter and stiffer: the Shuttle's Super Lightweight Tank, first flown on STS-91 in June 1998, used alloy 2195, about 30 % stronger and 5 % less dense than 2219, and weighed 3 400 kg less than its predecessor. Falcon 9's tanks are aluminium–lithium joined by **friction-stir welding**, in which a rotating tool stirs the metal together below its melting point. Al–Li is harder to weld and less tolerant of flaws, and SLS returned to 2219.

**Stainless steel**, used in the balloon tanks of Atlas and Centaur, has returned in SpaceX's Starship. It is heavier but cheap, easy to weld, stronger when cold, and keeps its strength at several hundred degrees Celsius — an advantage for a stage that must survive re-entry. **Carbon-fibre composites** promise the lightest tanks; Rocket Lab's Electron uses them throughout, and its larger Neutron is built around composite tanks, although voids found in a composite tank dome helped push Neutron's first launch into 2027. Composite tanks must resist micro-cracking, leakage and, for oxygen, ignition.

| Material | Density (g/cm³) | Typical strength (MPa) | Strength / density vs 2219 | Examples |
|---|---|---|---|---|
| Aluminium 2219 | 2.84 | 420–460 | 1.0 | Saturn V S-IC, SLS core stage |
| Aluminium–lithium (e.g. 2195) | 2.71 | 550–600 | ≈ 1.4 | Shuttle SLWT (2195), Falcon 9 |
| Stainless steel (300 series) | 7.9 | 500–600 (more when cold) | ≈ 0.5 | Atlas, Centaur, Starship |
| Carbon-fibre/epoxy laminate | 1.55–1.6 | 600–1 000 | ≈ 3 | Electron, Neutron, interstages |

: Tank and structure materials. Strengths are typical room-temperature tensile values; the metals are stronger at cryogenic temperature, and composite values depend strongly on the lay-up. {#tbl:tankmaterials}

A **common bulkhead** — a single dome separating the two propellants — saves the length and mass of a second dome. Falcon 9 uses one, as did both upper stages of the Saturn V, where the S-II's bulkhead had to be insulated to stop −183 °C oxygen freezing against −253 °C hydrogen. Walls in compression must resist **buckling**, so they are stiffened: by stringers attached to a thin skin (**skin-and-stringer**, as in Falcon 9's fuel tank), or by ribs machined out of thick plate in a triangular **isogrid** or rectangular **orthogrid** pattern (@fig:orthogridbarrel), which removes most of the metal but leaves a light, damage-tolerant structure without fasteners.

::: figrow
![A completed liquid-hydrogen tank barrel for the SLS core stage lifted off the Vertical Weld Center at NASA's Michoud Assembly Facility in February 2025. The orthogrid stiffening machined into the inner surface is visible.](figures/photos/ch34_barrel2.jpg){#fig:orthogridbarrel}

![The SLS liquid-hydrogen tank structural test article being placed in a test stand at NASA Marshall in January 2019. In December 2019 this test article was loaded to more than 260 % of its expected flight loads before it buckled and ruptured.](figures/photos/ch34_lh2tank.jpg){#fig:lh2testarticle}
:::

### Pressurisation

Tanks are pressurised to push propellant into the turbopumps without cavitation and to stiffen the walls, so that internal pressure carries part of the compressive and bending loads. **Balloon tanks** such as those of Atlas had no stiffeners at all and had to stay pressurised even on the ground. The pressurant is usually helium, stored at very high pressure in **composite-overwrapped pressure vessels** (COPVs), often submerged in the cold liquid oxygen where the gas is denser; Falcon heats the helium before it enters the tanks so that less is needed. Failures of these systems destroyed two Falcon 9s (@tbl:lvfailures). **Autogenous** pressurisation avoids helium altogether by feeding warmed propellant gas back into the tanks, as Starship does with methane and oxygen.

### Loads, Vibration and POGO

**Axial compression** peaks at the highest acceleration, just before first-stage cut-off; **bending** peaks around max-qα and in ground winds on the pad; internal pressure sizes the tank walls; and **acoustic** loads shake panels and equipment. A dangerous coupling is **POGO**, named after the pogo stick: a longitudinal vibration changes the pressure at the pump inlets, which changes the thrust, which reinforces the vibration. On Apollo 13 in April 1970, POGO oscillations shut down the centre engine of the Saturn V's second stage about two minutes early. The cure is to detune the feed system with gas-filled **accumulators** in the propellant lines; baffles damp propellant **slosh**.

Structures are designed with **factors of safety**, typically 1.1 on yield and 1.25–1.4 on ultimate strength, and proven by test, sometimes to destruction (@fig:lh2testarticle). Wind tunnels still provide the aerodynamic loads; in 2025 NASA's Ames Research Center tested a 1.2 % scale model of the Super Heavy Version 3 booster to measure the forces on it during its return through the atmosphere (@fig:superheavymodel).

### Fairings and Adapters

The **payload fairing** is a two-piece shell, usually carbon-fibre composite, lined with acoustic blankets; Falcon's is 5.2 m in diameter and 13.2 m tall. Some fairings are split by pyrotechnic **frangible joints**, which fracture a grooved structural seam (@fig:fairingseptest); Falcon's standard fairing releases mechanical latches and pushes the halves apart pneumatically, a system that can be tested before flight and produces little shock or debris. Below the payload, a **payload adapter** carries loads into the upper stage and holds the **separation system** — typically a **clamp band** of standard diameter (937, 1 194 or 1 666 mm on Falcon), released by cutting its bolts, with springs to push the spacecraft away.

::: figrow
![An Ariane 5 payload fairing in NASA's Space Power Facility at Plum Brook, Ohio, in 2012, before a full-scale test of a new horizontal pyrotechnic separation system that blew the two halves apart.](figures/photos/ch34_fairingtest.jpg){#fig:fairingseptest}

![A 1.2 % scale model of the Super Heavy Version 3 booster in a wind tunnel at NASA's Ames Research Center in 2025, used to measure the aerodynamic forces during re-entry.](figures/photos/ch34_windtunnel.jpg){#fig:superheavymodel}
:::

## Avionics, Guidance, Navigation and Control

### Navigation and Guidance

**Navigation** rests on an **inertial measurement unit** (IMU): gyroscopes, typically ring-laser or fibre-optic, measure rotation, and accelerometers measure specific force; integrating them gives attitude, velocity and position without outside help. Its errors grow with time, so it is blended with satellite navigation (Chapter 18) in a **Kalman filter**.

**Guidance** decides where to steer. In the dense atmosphere most vehicles fly a pre-computed, **open-loop** pitch programme that keeps α near zero. Above it, **closed-loop** guidance recomputes, many times a second, the steering needed to reach the target orbit from the current state. The Saturn V's Iterative Guidance Mode and the Shuttle's **Powered Explicit Guidance** both rest on the result that the fuel-optimal steering law in uniform gravity is the **linear-tangent law**, in which the tangent of the pitch angle varies linearly with time. The reference simulation uses this law for its second stage, solving for the two coefficients that place it on a 200 km circular orbit.

### Control and Redundancy

Liquid engines are mounted on **gimbals** and swivelled by a few degrees for **thrust vector control** (TVC). Actuators are hydraulic or, increasingly, electromechanical: Falcon's first-stage actuators use high-pressure kerosene from the engine as hydraulic fluid, removing a separate hydraulic system, while the solid first stage of Vega-C and Starship's Raptors use electric actuators. Single-engine stages control roll with small thrusters, such as Falcon's nitrogen cold-gas jets. Most rockets are aerodynamically unstable — their centre of pressure lies ahead of the centre of gravity — so the control loop must actively hold them straight without reacting to structural vibration or propellant slosh. Returning boosters steer with **grid fins**, lattice-like surfaces that work at hypersonic speed and fold flat during ascent.

Avionics are **fault tolerant**: Falcon uses a three-string architecture that votes between triplicated computers and sensors. Several engines give propulsion redundancy — Falcon 9 can shut down a misbehaving first-stage engine and burn the others longer (Chapter 35). A study by The Aerospace Corporation, cited in the Falcon user's guide, found that 91 % of launch failures in the two decades before 2001 were caused by engines, avionics or stage separation, the areas where redundancy and simplicity pay off most.

### Range Safety and Flight Termination

A rocket that strays threatens people on the ground. Ranges compute its **instantaneous impact point** — where it would land if thrust stopped — in real time, and every vehicle carries a **flight termination system** whose charges cut open the tanks to disperse the propellant before it can reach populated areas. For decades a range safety officer watched radar and telemetry and sent the destruct command by radio. An **autonomous flight safety system** runs the same rules on board, using the vehicle's own GNSS and inertial navigation; its first operational use was on Falcon 9's CRS-10 launch on 19 February 2017. It removes tracking radars and ground crews and allows launches in quick succession. In the United States the Federal Aviation Administration licenses commercial launches under 14 CFR Part 450, which caps the collective risk to the public at an expected 1 × 10⁻⁴ casualties per launch.

## The Payload's Ride

### Environments

The **launch vehicle user's guide** defines the environments a satellite must survive and the interfaces it must meet. @fig:lvenvironment and @tbl:f9environment summarise those of Falcon 9, taken from SpaceX's guide.

- **Quasi-static loads** combine steady acceleration and low-frequency vibration into load factors: up to +6 g axially and ±2 g sideways for satellites heavier than 1 800 kg, more for lighter ones.
- **Sine vibration** (5–100 Hz) comes from engine transients and structural modes; to avoid coupling, Falcon asks for payload fundamental frequencies above 25 Hz axially and 10 Hz laterally.
- **Acoustic** noise inside the fairing, from engine exhaust at lift-off and turbulent airflow in transonic flight, reaches 131 dB overall with acoustic blankets and 138 dB without. Solar arrays and antennas suffer most.
- **Random vibration** through the adapter (5.1 grms) matters mainly for small components, and **shock** from fairing and spacecraft separation, up to 1 000 g at kilohertz frequencies, can break crystals, relays and solder joints near the source.
- The payload must also tolerate heating, rapid depressurisation and contamination; it is processed in clean rooms (ISO class 8 on Falcon) and encapsulated before transport to the pad (@fig:paceencap).

![Payload environments of Falcon 9, from the Falcon User's Guide (May 2025): quasi-static limit-load envelopes for three payload-mass classes; acoustic spectra inside the fairing with and without blankets; random vibration at the payload adapter compared with NASA's generalised component test level; and shock response spectra for fairing and spacecraft separation.](figures/out/ch34_environment.svg){#fig:lvenvironment width=96%}

| Environment | Falcon 9 maximum predicted value | Typical verification test |
|---|---|---|
| Axial quasi-static load (> 1 800 kg) | +6.0 g compression, −2.0 g tension | Static load or sine burst, 1.25 × limit |
| Lateral quasi-static load (> 1 800 kg) | ±2.0 g | As above |
| Sine vibration | 0.5–1.0 g, 5–100 Hz | Sine sweep, 1.25 × limit |
| Acoustic (with blankets) | 131.4 dB overall | Reverberant chamber, MPE + 3 dB |
| Random vibration at adapter | 5.13 grms, 20–2 000 Hz | Shaker, MPE + 3 dB |
| Separation shock (clamp band) | up to 1 000 g, 1–10 kHz | Separation or pyroshock test |
| Fairing jettison | heating < 1 135 W/m² | Thermal analysis |

: Falcon 9 payload environments and the corresponding qualification tests (Falcon User's Guide, May 2025). MPE = maximum predicted environment. {#tbl:f9environment}

Satellites are verified against these environments with margin. A **qualification** test, on a unit that will not fly, exceeds the predicted loads by 25 % or the acoustic and vibration levels by 3 dB; an **acceptance** test applies the predicted levels to flight hardware to reveal workmanship defects; and many programmes use **protoflight** testing, at qualification levels for a shorter time on the flight unit (Chapter 4). Late in development the launch provider runs a **coupled loads analysis**, combining finite-element models of rocket and satellite to predict the loads at every interface.

::: figrow
![NASA's PACE Earth-observation satellite being encapsulated in a Falcon 9 fairing in January 2024. The work is done in a clean room to protect the instruments from contamination.](figures/photos/ch34_encap.jpg){#fig:paceencap width=74%}

![The Orion capsule that flew around the Moon on Artemis I, now an environmental test article, during vibro-acoustic testing at NASA's Armstrong Test Facility, Ohio, in 2024.](figures/photos/ch34_acoustic.jpg){#fig:orionacoustic width=74%}
:::

### Reading a Performance Curve

The other key part of a user's guide is the **performance curve** — payload against target orbit. @fig:lvperf shows the reference vehicle's, from a rocket-equation model calibrated to the trajectory simulation. For orbits reaching far from Earth the natural measure is the **characteristic energy** $C_3 = v_\infty^2$ (Chapter 24): negative for bound orbits (−60.6 km²/s² for a 200 km circular orbit, −16.4 km²/s² for GTO), zero for escape, and about 10 km²/s² for a typical trip to Mars. For low orbits, payload falls gently with altitude and with inclination. The model reproduces Falcon 9's published expendable capabilities well: 23.2 t to a 200 km orbit (published 22.8 t) and 8.4 t to GTO (8.3 t).

![Left: payload of the reference vehicle versus orbital energy for three booster-recovery modes, compared with published Falcon 9 values (crosses) and the full trajectory simulation (circles). Right: payload to circular orbits of different altitude and inclination with droneship recovery.](figures/out/ch34_perf.svg){#fig:lvperf width=98%}

## Reusability

### Landing a Booster

For most of the space age every stage was thrown away. The Space Shuttle (Chapter 10) recovered its orbiter and boosters but needed months of refurbishment. The modern approach, pioneered by SpaceX's first Falcon 9 landing in December 2015 and first re-flight in 2017, flies the booster back under its own power to a vertical landing on legs. It must keep propellant for up to three burns: a **boostback** burn to reverse its course; an **entry burn** to slow down before the dense atmosphere, limiting heating and loads; and a **landing burn**, timed so that velocity reaches zero just as the legs touch down, because even at minimum throttle one engine lifts more than the empty stage weighs. In a **return to launch site** (RTLS) the booster cancels its downrange velocity and flies back to a landing zone near the pad; in a **droneship** landing it continues on its ballistic arc to an autonomous barge hundreds of kilometres downrange, usually without a boostback burn.

@fig:lvrecovery shows both for the reference vehicle. Every kilogram kept in the booster is a kilogram not used to accelerate the upper stage, so the first stage cuts off earlier and slower. In the simulation a droneship landing keeps 22 t of propellant and costs 18 % of the LEO payload; RTLS keeps 45 t and costs 33 %. GTO missions need a faster staging speed and so more braking: the penalties grow to 26 % and 46 %. Falcon 9's published figures show larger penalties (22.8 and 17.5 t to LEO; 8.3, 5.5 and 3.5 t to GTO), partly because the model ignores the legs, grid fins and performance reserves.

![Left: simulated booster return trajectories for a droneship landing about 680 km downrange and for a return to the launch site, with the boostback (orange), entry (red) and landing (green) burns highlighted. Right: payload delivered to LEO and GTO in each recovery mode.](figures/out/ch34_recovery.svg){#fig:lvrecovery width=100%}

::: example
**Example: the propellant bill for landing**

The reference booster has a dry mass of 25.6 t, plus 1.5 t of unusable residual propellant. Its exhaust speed is 3.06 km/s in vacuum and 2.78 km/s at sea level. Work backwards from touchdown with $m_{before} = m_{after}\, e^{\Delta v/v_e}$:

1. **Droneship.** Landing burn, 0.44 km/s at sea level: 27.1 t × $e^{0.44/2.78}$ = 31.8 t. Entry burn, 1.23 km/s: 31.8 × $e^{1.23/3.06}$ = 47.5 t. Propellant kept at MECO: 47.5 − 25.6 = **21.9 t** (simulation: 22.0 t).
2. **RTLS.** At MECO the stage is moving downrange at 1.87 km/s. Landing burn 0.38 km/s: 27.1 × $e^{0.38/2.78}$ = 31.1 t; entry burn 0.21 km/s: 33.3 t; boostback burn 2.32 km/s: 33.3 × $e^{2.32/3.06}$ = 71.0 t. Propellant kept: **45.4 t**, more than twice as much.
3. Payload: in the simulation each tonne kept in the booster costs about 0.17–0.19 t of LEO payload, roughly one tonne for every five to six held back, because the upper stage still provides most of the Δv. RTLS suits light payloads, where saving the time and cost of a droneship voyage matters more than the lost mass.
:::

### Records, Catches and Refurbishment

Falcon has turned landing into routine. SpaceX made its 600th Falcon booster landing on 19 April 2026, and the fleet leader, B1067, flew for the 37th time on 25 August 2026. By February 2025 SpaceX had also re-flown fairing halves, recovered from the sea, on 307 missions. Between flights engines, heat shielding, grid fins and legs are inspected and a few parts replaced; Falcon Heavy's side boosters routinely land side by side (@fig:fhdualland).

Others are following. Blue Origin's New Glenn landed its first booster in November 2025 and re-flew it in April 2026. China recovered its first orbital booster on 10 July 2026, when the first stage of the new **Long March 10B** was caught at sea on its maiden flight by hooks that snagged cables tensioned over a net on the ship *Linghangzhe*; in August 2026 LandSpace's stainless-steel **Zhuque-3** landed on legs at a desert site in Gansu province, although a fire broke out after touchdown. SpaceX's Super Heavy booster is caught by the launch tower's mechanical "chopstick" arms instead of landing on legs: the first catch came on Starship Flight 5 on 13 October 2024 and was repeated on Flights 7 and 8 in 2025, and a caught booster re-flew on Flight 9. On 28 September 2026 Starship reached orbit for the first time on Flight 14; catching the ship, needed to make the whole vehicle reusable, was planned for a later flight.

![Falcon Heavy's two side boosters returning to Landing Zones 1 and 2 at Cape Canaveral after launching the GOES-U weather satellite in June 2024.](figures/photos/ch34_fhland2.jpg){#fig:fhdualland width=38%}

### The Economics of Launch

Reuse matters because hardware dominates launch cost: flying a first stage ten or thirty times spreads the cost of most of a vehicle's engines and structure. It pays only at a high flight rate, because factories, recovery ships and launch teams are fixed costs. Falcon 9 flew 165 times in 2025, half of all orbital launch attempts worldwide, and Starlink satellites made up 3 169 of the 4 511 payloads launched that year — an in-house customer that keeps the fleet busy.

@tbl:launchcostkg compares launch prices per kilogram; list prices are not costs, and rockets rarely fly full. A 2018 NASA analysis found that vehicles introduced between 1970 and 2000 averaged about $18 500 per kilogram to LEO (2018 dollars), the Space Shuttle $61 700, and Falcon 9 at its advertised price $2 700 — less than a twentieth of the Shuttle's figure. Prices have since risen with inflation and demand: in 2026 SpaceX listed a dedicated Falcon 9 at $74 million and rideshare at $350 000 for 50 kg to sun-synchronous orbit. Cheaper access has transformed demand: the mass launched to orbit grew from about 400 t in 2015 to about 3 500 t in 2025.

| Vehicle | First flight | Price per launch | Payload to LEO | Price per kg |
|---|---|---|---|---|
| Vanguard | 1957 | — | very small | ≈ $895 000 (2018 $) |
| Saturn V | 1967 | $728 M (2018 $) | 140 t | $5 200 (2018 $) |
| Space Shuttle | 1981 | $1 697 M (2018 $) | 27.5 t | $61 700 (2018 $) |
| Ariane 5 G | 1996 | — | — | $13 100 (2018 $) |
| Falcon 9 (2018 list) | 2010 | $62 M | 22.8 t | $2 700 |
| Falcon Heavy (2018 list) | 2018 | $90 M | 63.8 t | $1 400 |
| Falcon 9 (2026 list, booster landed) | 2010 | $74 M | ≈ 17.5 t | ≈ $4 200 |
| Falcon 9 rideshare (2026) | — | $350 000 per 50 kg | — | $7 000 |

: Launch prices per kilogram to low Earth orbit. Historical values from Jones (NASA, 2018); 2026 values from SpaceX's published prices in current dollars; per-kilogram values assume a full vehicle. {#tbl:launchcostkg}

## Reliability and Testing

### How Often Do Rockets Fail?

Of 330 orbital launch attempts in 2025, 11 failed — 3.3 %. @fig:lvreliability puts this in context using Jonathan McDowell's General Catalog of Artificial Space Objects (GCAT). In the late 1950s a third or more of all launches failed; the five-year average fell below 10 % in the early 1970s and has stayed at roughly 3–8 % since the mid-1970s, even as the launch rate tripled after 2020. The right-hand panel shows that **reliability is learned**. Across the 100 vehicle families first flown since 1980, 38 % of maiden flights failed, 23 % of second flights and 15 % of third flights; from the 21st to the 50th flight the rate was 4 %, and beyond the 50th, 0.7 %. New vehicles meet combinations of conditions that no ground test fully reproduces. Mature vehicles are very reliable: by October 2026 Falcon 9 had made 695 orbital attempts with 2 failures (99.7 %), and Soyuz more than 1 180 with 97.4 % success (Appendix E).

![Left: orbital launch attempts per year since 1957, split into successes and failures, with the five-year running failure rate. Right: the share of flights that failed as a function of flight number within each vehicle family, for families first flown before and after 1980.](figures/out/ch34_reliability.svg){#fig:lvreliability width=90%}

A few flights say little about a new vehicle. With *k* failures in *n* flights a reasonable estimate of failure probability is (*k* + ½)/(*n* + 1), the mean of the Jeffreys distribution used for the error bars of @fig:lvreliability. A rocket with ten successes in ten flights thus has an estimated failure probability of about 5 %, and the upper end of its 90 % interval lies near 17 %; only a hundred clean flights bring it below 2 %.

### Why Rockets Fail

Propulsion causes the largest share of failures; Chapter 35 describes the engine failures that shaped design practice. @tbl:lvfailures lists failures elsewhere in the vehicle — software, sensors, structures, separation and weather — and their lessons.

| Event | What failed | Lesson |
|---|---|---|
| Atlas-Centaur AC-67, Mar 1987 | Launched into cloud; lightning altered guidance-computer memory | Stricter weather launch-commit criteria |
| Ariane 5 flight 501, Jun 1996 | Reused Ariane 4 inertial-reference software overflowed | Re-validate reused software for the new flight |
| Taurus XL, Feb 2009 and Mar 2011 | Fairing did not separate; traced to falsified tests of aluminium parts | Verify the supply chain |
| Proton-M, Jul 2013 | Angular-rate sensors installed upside down | Error-proof mounting; inspection |
| Falcon 9 CRS-7, Jun 2015 | Strut holding a helium COPV in the upper-stage oxygen tank broke | Test critical small parts individually |
| Falcon 9 AMOS-6, Sep 2016 | Oxygen trapped in a COPV overwrap ignited during fuelling on the pad | Understand cryogenic loading; change procedures |
| H3 flight 8, Dec 2025 | Bonded composite payload adapter, delaminated in manufacture, failed under fairing-separation shock; satellite lost | Shock exposes hidden flaws; bolted adapter adopted |

: Launch failures outside the main engines and their lessons. {#tbl:lvfailures}

### Investigations and Testing

After a failure the operator leads a **mishap investigation** — in the United States under FAA oversight — and the vehicle is grounded until the cause is understood and the fix accepted. The evidence is mainly telemetry, analysed with fault trees that work through every possible cause. Falcon 9's Starlink 9-3 failure of 11 July 2024 shows the process at its fastest. An oxygen leak was traced to a pressure-sensor line cracked by vibration fatigue and a loose clamp; it chilled the engine's ignition system and caused a hard start at relight (Chapter 35). SpaceX removed the line, inspected clamps across the fleet, and the FAA cleared the vehicle on 25 July. Investigations take longer when the cause is less obvious. On New Glenn's third flight, in April 2026, one upper-stage engine fell short of full thrust, stranding its satellite in too low an orbit; five weeks later the FAA accepted Blue Origin's finding that a cryogenic leak had frozen a hydraulic line. Japan's H3 needed six months: its December 2025 failure was traced to a manufacturing flaw in its bonded carbon-fibre payload adapter that grew under the shock of fairing separation. With a bolted adapter, H3 flew successfully again in June and August 2026.

The guiding rule of testing is **test like you fly**: components are qualified on test stands, stages are fired whole (Chapter 35), complete vehicles perform a **static fire** on the pad, and structures are tested to failure to learn their true margins. Two philosophies coexist. The traditional approach spends years on analysis and ground testing to make the first flight as safe as possible. The **iterative**, hardware-rich approach builds cheaper test articles, flies early and expects to lose some — SpaceX's approach with Starship, which lost several upper stages in 2025 before reaching orbit in 2026. Both converge on the lesson of @fig:lvreliability: reliability is demonstrated by flying.

::: ai
**AI in launch-vehicle engineering**

Convex optimisation already flies: the G-FOLD algorithm, developed at NASA's Jet Propulsion Laboratory, computes fuel-optimal landing trajectories in milliseconds with guaranteed convergence, and SpaceX has described landing Falcon 9 boosters with automatically generated convex-optimisation code. Machine learning is being added around such algorithms: anomaly detectors scan thousands of telemetry channels for patterns that precede failures, and learned surrogates of loads and engine behaviour speed up design optimisation. Flight-critical software still rests on verifiable algorithms (Chapters 52 and 53).
:::

::: key
**Key takeaways**

- Reaching a 200 km orbit takes about 9.0–9.6 km/s of ideal Δv: 7.8 km/s of orbital speed plus about 1.5–2 km/s of gravity, steering, drag and back-pressure losses, minus up to 0.46 km/s from Earth's rotation (465 m/s × cos *i*).
- Launch latitude matters most for geostationary missions: removing a 28.5° inclination at apogee costs 0.35 km/s more than removing 5°.
- With realistic structures one stage cannot reach orbit with useful payload; two stages capture most of the benefit of staging.
- A gravity turn keeps the angle of attack near zero; engines throttle through max-Q (typically 25–40 kPa) and acceleration is capped at about 4–5 g.
- Tanks are thin pressurised shells of aluminium–lithium, stainless steel or composite; payloads must survive 130–140 dB of noise and loads of several g.
- Landing a booster costs payload — about a fifth for a droneship landing and a third for a return to the launch site — but enables dozens of re-flights.
- About 40 % of maiden flights fail; reliability grows with flight experience to 99 % or better for mature vehicles.
:::

::: questions
**Review questions**

1. List the four losses in a launch Δv budget and explain why steering loss can rival gravity loss for a vehicle with a low-thrust upper stage.
2. Show that the Earth-rotation gain for a launch into an orbit of inclination *i* is 465 m/s × cos *i*, whatever the site latitude. What is it for a 97.5° sun-synchronous orbit?
3. A 4 000 kg geostationary satellite with a 320 s apogee engine is launched from Kourou or from Cape Canaveral. Estimate the difference in the propellant it needs.
4. For stages with Isp 340 s and ε = 0.07, compute the payload fraction of one, two and three identical stages for Δv = 9.4 km/s.
5. Why do launch vehicles fly a gravity turn? What is max-qα, and how is it managed on launch day?
6. Explain the purpose of a throttle bucket and why acceleration rises during each stage's burn.
7. Compare aluminium–lithium, stainless steel and composite tanks. Why might a reusable stage use steel?
8. What is POGO, and how is it suppressed?
9. A satellite's lowest lateral natural frequency is 8 Hz. Why might the launch provider object, and what analysis would settle the question?
10. Estimate the propellant a 25 t booster must keep for a 3 km/s return-to-launch-site profile with Isp 300 s, and explain why the payload penalty is much smaller than the propellant kept.
:::
