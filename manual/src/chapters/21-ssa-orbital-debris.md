---
title: Space Surveillance, Orbital Debris and Space Situational Awareness
hero: ch21
abstract: Some 35 000 catalogued objects — working satellites, dead satellites, spent rocket stages and fragments — orbit the Earth, together with an estimated million pieces of debris too small to track but large enough to destroy a satellite. Space situational awareness (SSA) is the knowledge of where these objects are, where they are going and what they are doing. This chapter uses the public satellite catalogue to show how the orbital population has grown and where it is concentrated, explains the hazards of hypervelocity impacts and the threat of a collisional cascade, and describes the radars, telescopes and analytical methods used to track objects, predict close approaches and decide when to manoeuvre. It then covers debris mitigation rules — from the 25-year guideline to the new five-year rule — active debris removal, re-entry risks and the emerging governance of space traffic.
---

## A Crowded Environment

### Space Situational Awareness and Space Domain Awareness

**Space situational awareness (SSA)** is the knowledge of the population of objects in space and of the space environment needed to operate safely. It covers where each object is, how its orbit is changing, what it is, and whether it threatens another. Military organisations increasingly use the broader term **space domain awareness (SDA)**, which adds understanding of the capabilities and intentions of other actors (Chapter 19). SSA has three main components:

- **Space surveillance and tracking (SST)** of objects in orbit;
- **Space weather** monitoring (Chapters 22 and 23);
- **Near-Earth object** monitoring — asteroids and comets that could hit the Earth (Chapter 41).

This chapter concentrates on the first: the population of artificial objects and the debris problem.

### The Numbers

In October 2026 the publicly available catalogue maintained by the US Space Force and redistributed by CelesTrak contained about **35 000** objects in Earth orbit. These were some 20 000 payloads (about 17 000 of them active), 12 500 catalogued debris fragments and 2 300 rocket bodies (@fig:population). The total had more than doubled in a decade, driven mostly by the growth of large constellations. Surveillance networks track many more objects than are published — ESA estimates about 40 000 tracked objects — and statistical models estimate far larger populations of smaller debris (@tbl:debrissizes).

![Catalogued objects in Earth orbit by type, 1957–2026, computed from the public satellite catalogue. Two destructive events (2007 and 2009) caused sudden jumps; since 2019 large constellations have dominated growth.](figures/out/ch21_population.svg){#fig:population width=96%}

| Size | Estimated number | Can it be tracked? | Effect of impact on a satellite |
|---|---|---|---|
| > 10 cm | > 50 000 | Yes (most, in LEO) | Catastrophic break-up; satellites manoeuvre to avoid |
| 1–10 cm | ≈ 1.2 million | Mostly not | Can destroy a satellite; cannot be avoided or shielded against easily |
| 1 mm – 1 cm | ≈ 130 million | No | Damage to sensitive surfaces; penetration of unshielded components |
| < 1 mm | Many billions | No | Erosion, pitting of windows and solar cells |

: Estimated population of debris by size (ESA Space Environment Report 2025, model estimates). {#tbl:debrissizes}

### Where the Objects Are

Objects are not evenly distributed (@fig:debrisdensity). The spatial density in LEO peaks sharply at 450–570 km, where most Starlink satellites fly. It also shows a broader band of old debris and rocket bodies at 700–1 000 km. This is the region of the 2007 Chinese ASAT test, the 2009 Iridium–Cosmos collision and many older break-ups. Debris at these higher altitudes will remain for decades to centuries because the atmosphere is too thin to remove it quickly. Other concentrations are found in the geostationary ring, where about 1 000 objects, active and dead, crowd a narrow belt, and in the MEO navigation orbits.

![Spatial density of catalogued objects in low Earth orbit by altitude and type (October 2026).](figures/out/ch21_density.svg){#fig:debrisdensity width=94%}

Plotting every object by altitude and inclination (@fig:altinc) reveals the structure of the population. It shows vertical streaks of satellites in the same orbital planes, the dense band of sun-synchronous orbits at 97–99°, and the shells of Starlink and OneWeb. It also shows clouds of debris spread in altitude around the orbits of the satellites and stages that broke up.

![Altitude and inclination of every catalogued object below 2 100 km in October 2026.](figures/out/ch21_altinc.png){#fig:altinc width=96%}

Responsibility for the population is concentrated (@fig:owners). Objects attributed to the USA — including Starlink — are the most numerous, followed by Russia and China. Russia and China account for most of the catalogued debris, through old explosions, the 2007 and 2021 ASAT tests and recent upper-stage break-ups. Under the Outer Space Treaty and the Liability Convention, the launching state remains responsible for its objects, including debris, indefinitely.

![Catalogued objects in orbit by owner and type (October 2026).](figures/out/ch21_owners.svg){#fig:owners width=88%}

## Sources of Debris

### Fragmentations

Most catalogued debris comes from a few hundred **fragmentation events** (@fig:fragmentations):

- **Explosions** of rocket upper stages and satellites, caused by residual propellant, pressurised tanks or batteries — the most common cause historically. Stages that remain in orbit with leftover propellant can explode decades later, which is why "passivation" (venting propellant and discharging batteries) is now required.
- **Deliberate destruction**, above all the anti-satellite tests of 2007 (Fengyun-1C) and 2021 (Cosmos 1408) (Chapter 19).
- **Collisions**. On 10 February 2009 the active Iridium 33 communications satellite collided with the defunct Russian Cosmos 2251 at about 790 km and a relative speed of 11.7 km/s. It was the first accidental collision between two intact satellites, and it produced more than 2 300 catalogued fragments. Smaller collisions have occurred before and since; in 2021, for example, the Chinese satellite Yunhai 1-02 broke up after being struck by a fragment of debris from a 1996 launch.
- **Anomalous events**: the sudden break-up of old weather satellites (NOAA-16, NOAA-17, DMSP) and, in 2022 and 2024, of Long March 6A upper stages, each producing hundreds of fragments.

![The largest fragmentation events in the public catalogue: total catalogued fragments and those still in orbit in October 2026.](figures/out/ch21_fragmentations.svg){#fig:fragmentations width=94%}

### Other Sources

Smaller debris also comes from **mission-related objects** (lens covers, bolts, adapters released during deployment) and from **solid-rocket-motor** slag and aluminium-oxide dust. Other sources are **paint flakes** and degraded insulation shed by ageing spacecraft (@fig:mlishield). There are also droplets of sodium–potassium coolant leaked by Soviet nuclear-powered radar satellites of the 1980s. Natural **micrometeoroids** — dust from comets and asteroids — add a background flux that dominates for sizes below about 0.1 mm.

![Damage to a multi-layer insulation blanket on the Zarya module of the International Space Station, photographed during a spacewalk in 2007. Long-term exposure to micrometeoroids, debris and atomic oxygen degrades exterior materials.](figures/photos/ch21_mli.jpg){#fig:mlishield width=62%}

## Why Debris Is Dangerous

### Hypervelocity Impacts

Objects in LEO collide at an average relative speed of about 10 km/s — ten times faster than a rifle bullet. At such speeds, even small particles carry enormous energy (@fig:impactenergy). A 1 cm aluminium sphere at 10 km/s has a kinetic energy of about 70 kJ, comparable to a small car crash. Both projectile and target are partly vaporised. In practice:

- particles smaller than about 1 mm cause pitting and erosion; windows of the Space Shuttle were replaced after almost every flight because of tiny impacts;
- particles of 1 mm to 1 cm can penetrate unshielded walls, tanks and cables, but **shielding** works against them;
- objects of 1–10 cm are too small to track reliably but too large to shield against — they represent the greatest unmanaged risk;
- objects larger than about 10 cm are tracked, and spacecraft can manoeuvre to avoid them.

![Kinetic energy of an aluminium sphere at 10 km/s as a function of its diameter, with the effects of impacts in each size range.](figures/out/ch21_energy.svg){#fig:impactenergy width=86%}

### Shielding

In 1947, the astronomer Fred Whipple proposed protecting spacecraft from meteoroids with a thin outer "bumper" separated from the main wall. A projectile striking a **Whipple shield** shatters and partly vaporises on the bumper. The resulting cloud of fragments spreads out over the gap and strikes the main wall over a wide area, where it can be stopped. **Stuffed Whipple shields**, with intermediate layers of Kevlar and Nextel ceramic fabric, protect the crewed modules of the ISS against particles up to about 1 cm. Shields are designed and tested with light-gas guns that fire small projectiles at up to about 7–8 km/s (@fig:hvi), complemented by computer simulations. Recovered hardware, such as Hubble's Wide Field and Planetary Camera 2 returned in 2009 (@fig:wfpc2), provides real data on the impact environment.

::: figrow
![A target plate after a hypervelocity impact test at 6.8 km/s at NASA's White Sands Test Facility, during tests of materials for the Orion spacecraft.](figures/photos/ch21_hvi.jpg){#fig:hvi}

![Engineers of NASA's Orbital Debris Program Office and Hypervelocity Impact Technology team examine impact craters on Hubble's Wide Field and Planetary Camera 2 after its return in 2009, after 16 years in orbit.](figures/photos/ch21_sts125.jpg){#fig:wfpc2}
:::

### The Kessler Syndrome

In 1978 Donald Kessler and Burton Cour-Palais of NASA predicted what would happen as the number of objects in orbit grew. Collisions between them would eventually produce debris faster than the atmosphere removes it. This would lead to a self-sustaining **collisional cascade** — now called the **Kessler syndrome**. Long-term models of the debris environment include NASA's LEGEND, ESA's DELTA and the studies of the Inter-Agency Space Debris Coordination Committee. They agree that some LEO altitude bands, especially around 700–1 000 km, may already be above this critical density. Even with no further launches, collisions would slowly increase the number of fragments. The models also show that the outcome depends strongly on behaviour (@fig:cascade). If spacecraft are reliably removed from orbit at the end of their missions, growth can be held in check. Removing a few large derelict objects per year can also stabilise the environment.

![Schematic of the qualitative conclusions of long-term debris-environment models under different mitigation scenarios.](figures/out/ch21_cascade.svg){#fig:cascade width=86%}

## Tracking Objects in Space

### Sensors

Objects in orbit are observed by networks of radars, optical telescopes and, increasingly, sensors in space (@fig:ssasensors; @tbl:ssasensors).

- **Radars** dominate in LEO because they work day and night in all weather and measure range and range-rate directly. Large phased-array radars include the US PAVE PAWS and Upgraded Early Warning Radars (originally built for missile warning, Chapter 20). Others are Cobra Dane in Alaska and the S-band **Space Fence** on Kwajalein Atoll (operational since 2020). Such radars can detect objects down to about 5–10 cm in LEO and track thousands of objects per hour. Tracking and imaging radars such as Germany's TIRA can produce radar images of satellites.
- **Optical telescopes** observe sunlit objects against a dark sky and are best for high orbits, where radar echoes are extremely weak. This is because the radar signal falls as the fourth power of range, but reflected sunlight only as the square (@fig:detectability). The US Ground-based Electro-Optical Deep Space Surveillance (GEODSS) telescopes, commercial networks and European and Russian systems such as ISON monitor the geostationary belt, detecting objects of about 0.5–1 m at GEO.
- **Space-based sensors** avoid weather and day–night limitations. The US Space-Based Space Surveillance satellite (since 2010) observes GEO from LEO. The Geosynchronous Space Situational Awareness Program (GSSAP) satellites — six launched in 2014–2022 and two more in 2026 — patrol near the GEO belt to inspect objects.
- **Commercial providers** now operate their own networks. These include LeoLabs' phased-array radars in several countries and optical networks such as those of ExoAnalytic Solutions and Slingshot Aerospace. Some companies also fly cameras on satellites to observe other objects.

![Selected ground-based space-surveillance sensors around the world (public information).](figures/out/ch21_sensors.svg){#fig:ssasensors width=96%}

![Approximate smallest detectable object size as a function of range for radars and optical telescopes. Radars excel in LEO; telescopes are needed for GEO.](figures/out/ch21_detectability.svg){#fig:detectability width=86%}

| Sensor | Operator | Type | Main role |
|---|---|---|---|
| Space Fence (Kwajalein) | US Space Force | S-band phased-array radar | Uncued detection of small LEO objects |
| Cobra Dane, PAVE PAWS/UEWR | US Space Force | UHF/L-band phased-array radars | Missile warning and LEO surveillance |
| GEODSS (Socorro, Maui, Diego Garcia) | US Space Force | 1 m optical telescopes | Deep-space (GEO) surveillance |
| GSSAP, SBSS | US Space Force | Space-based optical | GEO inspection and surveillance |
| GRAVES, TIRA, EU SST network | France, Germany, EU | Bistatic radar, tracking/imaging radar, optical | European surveillance and tracking |
| LeoLabs network | LeoLabs (commercial) | UHF/S-band phased-array radars | Commercial LEO tracking and conjunction services |
| ISON | Russian Academy of Sciences | Optical network | GEO and HEO objects |
| Okno, Krona | Russia | Optical and radar complexes | Military space surveillance |

: Selected space-surveillance sensors. {#tbl:ssasensors}

### The Catalogue

The observations are combined into a **catalogue** of orbits. The US Space Force (through its space defence squadrons) maintains the most complete catalogue, publishing data on most unclassified objects through the Space-Track website, where each object has a NORAD catalogue number. Orbits are published as **two-line element sets (TLEs)**, compatible with the SGP4 analytical propagator (Chapter 3). For precise applications, the military also maintains a "special perturbations" catalogue, computed by numerical integration with detailed force models. In addition, operators exchange precise ephemerides. Keeping the catalogue current requires associating every new observation with the right object. This is difficult after break-ups or when many satellites are deployed together. It also requires modelling atmospheric drag, which changes with solar activity and is the largest source of prediction error in LEO (Chapter 22).

**Characterisation** goes beyond orbits. Brightness variations (**light curves**) reveal whether an object is tumbling and how fast, and radar cross-sections and radar images reveal its size and shape. Spectroscopy can identify surface materials, and observing manoeuvres reveals whether a satellite is active.

## Conjunction Assessment and Collision Avoidance

### Predicting Close Approaches

Every day, screening software compares the predicted trajectories of all catalogued objects to find **conjunctions** — close approaches — within the next several days. For each, the screening centre issues a **conjunction data message (CDM)** to the operators involved, giving the predicted time of closest approach, the miss distance and the uncertainty (covariance) of both objects' positions. Large constellations receive thousands of such messages per week.

The key quantity is the **probability of collision** ($P_c$), computed in the **encounter plane** perpendicular to the relative velocity (@fig:encounter). LEO encounters last only a fraction of a second at 10–15 km/s, so relative motion can be treated as a straight line. $P_c$ is then the integral of the two-dimensional probability density of the miss vector over a circle. The circle's radius is the combined size of the two objects (@fig:pc). Counter-intuitively, very uncertain predictions give *low* probabilities, because the probability is spread over a large area ("dilution"); good tracking data are needed to recognise a real threat.

![Geometry of a conjunction in the encounter plane.](figures/out/ch21_encounter.svg){#fig:encounter width=90%}

![Probability of collision versus predicted miss distance for different levels of position uncertainty.](figures/out/ch21_pc.svg){#fig:pc width=86%}

### Deciding to Manoeuvre

Operators typically plan an avoidance manoeuvre when $P_c$ exceeds about 1 in 10 000 (NASA's threshold for robotic missions), sometimes using more conservative values for crewed vehicles. Each manoeuvre costs propellant, interrupts the mission and may create new conjunctions, so operators weigh the risk carefully; the decision is often made only one or two days before the encounter, when uncertainties have shrunk. The ISS has performed dozens of debris-avoidance manoeuvres since 1999, and its crew has occasionally sheltered in their return vehicles when a threat was detected too late to manoeuvre. Large constellations automate the process: Starlink satellites perform tens of thousands of autonomous avoidance manoeuvres per year using screening data, and share their ephemerides publicly. When both objects can manoeuvre, operators must coordinate so that they do not both move the wrong way.

## Debris Mitigation

### Guidelines and Rules

International efforts to limit debris began in the 1990s. The **Inter-Agency Space Debris Coordination Committee (IADC)** was founded in 1993 by the major space agencies. It issued mitigation guidelines in 2002, which were endorsed by the UN Committee on the Peaceful Uses of Outer Space (COPUOS) in 2007. The UN adopted wider **Guidelines for the Long-term Sustainability of Outer Space Activities** in 2019 (@tbl:mitigation). The main principles are:

1. **Limit debris released** during normal operations.
2. **Minimise the potential for break-ups**: passivate spacecraft and stages at the end of life by venting propellant and pressurants and discharging batteries.
3. **Post-mission disposal**: remove spacecraft and stages from the protected LEO region within a limited time — traditionally **25 years**. Do this by lowering their orbits so that drag brings them down, by controlled re-entry, or by boosting them to a disposal orbit. Move GEO satellites at least about 235 km above the geostationary ring (plus a term depending on their area-to-mass ratio) into a "graveyard" orbit.
4. **Prevent on-orbit collisions** through conjunction assessment and manoeuvre capability.

| Instrument | Body | Year | Key provisions |
|---|---|---|---|
| IADC Space Debris Mitigation Guidelines | IADC | 2002 (updated) | Passivation, 25-year LEO disposal, GEO graveyard |
| Space Debris Mitigation Guidelines | UN COPUOS | 2007 | Endorsed IADC principles for all states |
| ISO 24113 | International Organization for Standardization | 2010 (updated) | Engineering requirements for debris mitigation |
| LTS Guidelines | UN COPUOS | 2019 | 21 guidelines on safety, sustainability and cooperation |
| Five-year rule | US FCC | adopted 2022, in force 2024 | LEO satellites below 2 000 km must be disposed of within 5 years of mission end |
| Zero Debris approach / Charter | ESA and partners | 2023 | Aim to stop generating debris by 2030; ≥ 99 % disposal success |
| French Space Operations Act | France | 2008 | Legally binding technical regulations, including disposal |

: Selected debris-mitigation guidelines and rules. {#tbl:mitigation}

The 25-year guideline was set when LEO held a few thousand objects; with tens of thousands of satellites, it is now widely considered too lax. The US Federal Communications Commission's **five-year rule**, in force since 2024 for satellites it licenses, reflects the tightening of expectations. So does ESA's **Zero Debris** approach, which aims to stop creating debris by 2030. @fig:debrislifetime shows why altitude matters. Satellites below about 500 km re-enter naturally within a few years. Those above about 700 km may stay up for a century or more unless they carry propulsion to lower their orbits.

![Approximate orbital lifetime versus initial altitude for different ballistic coefficients and solar activity levels.](figures/out/ch21_lifetime.svg){#fig:debrislifetime width=86%}

### Compliance

Compliance with disposal guidelines has improved but remains imperfect. ESA's annual space-environment reports show that most new LEO payloads now comply, largely because so many fly in low orbits that decay quickly. However, many rocket bodies are still abandoned in long-lived orbits, and a few percent of large-constellation satellites fail before they can de-orbit themselves. A failure rate of even 1–2 % in a constellation of 10 000 satellites leaves 100–200 uncontrolled objects.

## Active Debris Removal and Remediation

The most dangerous objects for the long term are the few thousand large, intact derelicts — especially rocket bodies of 1–9 tonnes in crowded orbits. So **active debris removal (ADR)** focuses on capturing them and de-orbiting them. The challenges are considerable: the targets were not designed to be captured, may be tumbling, and have no docking fixtures, and someone must pay for the service.

- Japan's **Astroscale** demonstrated magnetic capture of a cooperative target with **ELSA-d** (2021). With **ADRAS-J** (2024), it approached a discarded H-IIA upper stage to about 15 m and inspected it in detail — the first close approach to a real piece of debris. Its follow-on, **ADRAS-J2**, planned for launch around 2027–28, is designed to capture and remove such a stage.
- ESA's **ClearSpace-1** mission, now planned for around 2028–29, will capture and de-orbit the PROBA-1 satellite (launched in 2001).
- Other concepts include nets, harpoons, robotic arms, drag sails and tethers, ground- or space-based lasers that nudge small debris, and life-extension servicing that keeps valuable satellites working (Chapter 40).

Studies suggest that removing about five to ten of the most dangerous large objects per year, combined with high compliance with disposal rules, could stabilise the LEO environment.

## Re-entries

What goes up comes down. About 2 000 catalogued objects now re-enter each year (@fig:reentries), most of them small objects and constellation satellites that burn up completely. Larger objects pose a risk to people on the ground: dense components such as titanium tanks, steel parts and optics can survive re-entry. Guidelines limit the casualty risk of an uncontrolled re-entry to 1 in 10 000. Larger spacecraft and stages must perform a **controlled re-entry** into a remote ocean area — the South Pacific "spacecraft cemetery" near Point Nemo — or be designed to **demise** completely. Notable uncontrolled re-entries include Skylab (1979), whose debris fell on Western Australia, and several 20-tonne Long March 5B core stages (2020–2022). Another was a fragment of an ISS battery pallet that struck a house in Florida in March 2024, prompting claims for damages under the Liability Convention. Scientists are also studying whether the aluminium oxide produced by thousands of burning satellites each year could affect the upper atmosphere and ozone layer.

![Catalogued objects re-entering the atmosphere each year by type. Re-entries have increased sharply with large constellations and the decay of debris from the 2021 ASAT test.](figures/out/ch21_reentries.svg){#fig:reentries width=88%}

## Space Traffic Coordination

There is no international space traffic management system comparable to air traffic control. Each country licenses its own operators, and coordination relies on the sharing of data and good practice. Steps toward more organised **space traffic coordination** include:

- the US Office of Space Commerce's **Traffic Coordination System for Space (TraCSS)**, which is taking over civil conjunction services from the military. It was in pre-production with operators in 2026, though its funding has been contested;
- the **EU Space Surveillance and Tracking** partnership, which provides collision-avoidance services to hundreds of European and international satellites;
- industry initiatives such as the **Space Data Association** and the **Space Sustainability Rating**, which scores missions on their debris-mitigation and data-sharing practices;
- research on automated, interoperable coordination between operators — increasingly using AI (Part XIII).

::: example
**Example: should we manoeuvre?**

A conjunction data message predicts that an Earth-observation satellite will pass a defunct rocket body at a miss distance of 400 m in 36 hours. The combined hard-body radius is 8 m, and the position uncertainty in the encounter plane is about σ = 300 m in each direction.

1. Using the circular-uncertainty approximation, $P_c \approx \dfrac{R^2}{2\sigma^2} \exp\!\left(-\dfrac{d^2}{2\sigma^2}\right) = \dfrac{64}{180\,000} \exp(-0.89) \approx 1.5 \times 10^{-4}$.
2. This exceeds the 1 × 10⁻⁴ threshold, so the operator plans a manoeuvre but waits for the next update.
3. Twelve hours later, new tracking reduces σ to 100 m and the predicted miss distance to 150 m: $P_c \approx \dfrac{64}{20\,000}\exp(-1.13) \approx 1.0 \times 10^{-3}$ — a real threat.
4. A small along-track burn of a few centimetres per second, executed half an orbit before the encounter, changes the timing of arrival and increases the miss distance to about 2 km, reducing $P_c$ below 10⁻⁷. The operator confirms with the screening service that the new orbit creates no new conjunctions.
:::

::: ai
**AI for space situational awareness**

Machine learning is used to associate observations with catalogue objects, detect manoeuvres and break-ups, characterise objects from light curves and radar data, improve drag and orbit predictions, prioritise conjunction alerts and recommend avoidance manoeuvres. As constellations grow, automated and AI-assisted coordination between operators will become essential (Chapter 50).
:::

::: key
**Key takeaways**

- About 35 000 objects are catalogued in Earth orbit (October 2026), of which about 17 000 are active payloads; models estimate more than a million debris objects larger than 1 cm.
- Debris comes mainly from explosions, deliberate destruction and collisions; the 2007 Chinese ASAT test and the 2009 Iridium–Cosmos collision are the largest sources still in orbit.
- At 10 km/s, a 1 cm fragment carries the energy of a small car crash; objects of 1–10 cm can neither be tracked reliably nor shielded against.
- Some LEO altitude bands may already exceed the critical density for a collisional cascade (Kessler syndrome); reliable post-mission disposal and removal of large derelicts can stabilise the environment.
- Radars track LEO objects down to about 5–10 cm; telescopes monitor GEO; catalogues are maintained by military, civil and commercial organisations.
- Conjunction assessment uses the probability of collision in the encounter plane; operators typically manoeuvre above about 1 in 10 000.
- Mitigation rules are tightening — from the 25-year guideline to the FCC five-year rule and ESA's Zero Debris approach; active removal missions such as ADRAS-J2 and ClearSpace-1 are preparing to remove debris.
:::

::: questions
**Review questions**

1. How many objects are catalogued in Earth orbit in 2026, how many are active payloads, and how many debris objects larger than 1 cm are estimated to exist?
2. Calculate the kinetic energy of a 1 cm aluminium sphere (density 2 700 kg/m³) at 10 km/s, and compare it with a 1-tonne car at 12 m/s.
3. Which events created the largest amounts of debris still in orbit?
4. Why are objects of 1–10 cm in LEO the most dangerous class for operational satellites?
5. What is the Kessler syndrome? Why do studies conclude that removing large derelict objects is more effective than removing small fragments?
6. How is the probability of collision for a conjunction calculated, and what thresholds do operators use to decide on a manoeuvre?
7. Compare the 25-year guideline, the FCC five-year rule and ESA's Zero Debris approach.
8. Describe two active debris-removal techniques and the missions planned to demonstrate them.
:::
