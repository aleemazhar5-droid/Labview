---
title: The Space Environment
hero: ch02
abstract: A spacecraft must survive two very different environments - the short, violent environment of launch and the long, quiet but hostile environment of space. This chapter explains each hazard in turn - the upper atmosphere and drag, vacuum, the thermal environment, atomic oxygen, plasma and charging, ionising radiation, micrometeoroids and debris, and the mechanical loads of launch - shows how each one varies with orbit, and gives the design rules engineers use to cope with them.
---

## Why the Environment Drives Design

A spacecraft engineer's first question about any mission is *where* the spacecraft will fly, because the environment determines most design decisions: the thickness of shielding, the type of electronic parts, the thermal coatings, the solar array degradation margin, the propellant needed to fight drag, and even the shape of the vehicle. Many famous failures — from the early Telstar 1 satellite, killed in 1962 by radiation from a high-altitude nuclear test, to the loss of 38 newly launched Starlink satellites to a minor geomagnetic storm in February 2022 — were environmental failures.

The space environment can be divided into the following components, each discussed in this chapter:

1. **The neutral atmosphere** — drag, atomic oxygen, and their dependence on solar activity.
2. **Vacuum** — outgassing, contamination, cold welding, discharges.
3. **The thermal environment** — sunlight, Earth albedo and infrared, eclipses, deep-space cold.
4. **Plasma** — charged particles that charge spacecraft surfaces and cause discharges.
5. **Ionising radiation** — trapped belts, solar particle events and galactic cosmic rays.
6. **Micrometeoroids and orbital debris (MMOD)** — hypervelocity impacts.
7. **Mechanical environments** — launch loads, vibration, acoustics, shock, and microgravity.

![Relative severity of the main environmental hazards in different orbital regimes. No orbit is benign: low orbits suffer drag, atomic oxygen and debris; medium and high orbits suffer radiation and charging; deep space adds cosmic rays and solar particle events with no magnetospheric protection.](figures/out/ch02_env_matrix.svg){#fig:envmatrix width=92%}

## The Neutral Atmosphere

### Structure of the Atmosphere

The atmosphere is divided into layers by the way temperature changes with height (@fig:tprofile). In the **troposphere** temperature falls about 6.5 K per kilometre. In the **stratosphere** it rises again because ozone absorbs ultraviolet sunlight. It falls through the **mesosphere** to the coldest point on Earth, the **mesopause** at 85–90 km (about −90 °C), where noctilucent clouds form and meteors burn up. Above that, in the **thermosphere**, the very thin gas absorbs extreme-ultraviolet (EUV) radiation from the Sun and is heated to 700–1 400 K or more. Above about 500 km lies the **exosphere**, where atoms are so sparse that they follow ballistic trajectories and can escape to space.

![Temperature profile of the atmosphere. Below 86 km the US Standard Atmosphere 1976 is shown; above, the thermosphere approaches an "exospheric temperature" T∞ that depends strongly on solar EUV output.](figures/out/ch02_temperature.svg){#fig:tprofile width=88%}

The composition also changes. Below about 100 km the atmosphere is well mixed (78 % N₂, 21 % O₂). Above, gases separate by molecular weight, and solar ultraviolet splits O₂ into **atomic oxygen (O)**, which becomes the dominant species between about 200 and 600 km. Higher still, helium and then hydrogen dominate.

### Density and the Scale Height

In a column of gas in hydrostatic equilibrium, the pressure falls exponentially with altitude:

$$\rho(h) = \rho_0 \exp\left(-\frac{h-h_0}{H}\right), \qquad H = \frac{k_B T}{m g}$$

where $H$ is the **scale height** — the height over which density falls by a factor of $e \approx 2.72$. Near the ground $H \approx 8.5$ km; at 400 km, where the gas is hot and light, $H$ is about 50–60 km. Because $H$ depends on temperature, and thermospheric temperature depends on the Sun, **density at a given LEO altitude can change by a factor of ten or more** between solar minimum and solar maximum, and by a factor of two to five within hours during a geomagnetic storm (@fig:density).

![Neutral density of the upper atmosphere for low and high solar activity. At typical LEO altitudes, the density — and therefore the drag on a satellite — varies by about an order of magnitude over the 11-year solar cycle.](figures/out/ch02_density.svg){#fig:density width=88%}

Solar activity is tracked by two indices that drive the atmospheric models (NRLMSIS 2.0, JB2008, DTM-2020): the **F10.7 index**, the solar radio flux at 10.7 cm wavelength (a proxy for EUV output; typically 70 at solar minimum and 150–250 at maximum), and the geomagnetic **Ap / Kp indices**, which measure the heating of the upper atmosphere by the solar wind (Chapter 22).

### Atmospheric Drag

A satellite moving at velocity $v$ through gas of density $\rho$ experiences a drag force

$$F_D = \tfrac{1}{2}\,\rho\, v^2\, C_D\, A$$

where $A$ is the cross-sectional area and $C_D$ is the drag coefficient (typically 2.0–2.4 for satellites in free-molecular flow). The ratio $B = m/(C_D A)$ is the **ballistic coefficient**: a dense, compact satellite (large $B$) decays slowly; a satellite with large solar arrays (small $B$) decays quickly. For a circular orbit of radius $a$, drag reduces the orbit radius at the rate

$$\frac{da}{dt} = -\frac{\rho\,\sqrt{\mu\, a}}{B}$$

Counter-intuitively, drag makes a satellite *speed up*: as it loses energy it sinks to a lower orbit, where the orbital speed is higher. The decay accelerates as the satellite descends into denser air, so most of a satellite's orbital life is spent at the higher altitudes and the final descent from 200 km takes only days. @fig:lifetime shows typical orbital lifetimes.

![Approximate orbital lifetime versus initial altitude for three ballistic coefficients. A satellite at 400 km with m/(C_D A) = 100 kg/m² lasts about one to three years; at 600 km it lasts decades; at 800 km it lasts more than a century. The 5-year line marks the US FCC post-mission disposal rule (2022) for LEO satellites.](figures/out/ch02_lifetime.svg){#fig:lifetime width=90%}

::: example
**Worked example — how fast does the ISS lose height?**

Take $a = 6\,778$ km (400 km altitude), $\rho = 3\times10^{-12}$ kg/m³ (moderate activity), mass 420 t, effective $C_D A \approx 2.2 \times 1\,900$ m² ≈ 4 200 m², so $B \approx 100$ kg/m².

$$\frac{da}{dt} = -\frac{3\times10^{-12}\times\sqrt{3.986\times10^{14}\times 6.778\times10^{6}}}{100} \approx -1.6\times10^{-3}\ \text{m/s}$$

That is about 140 m per day, or 4 km per month. The real ISS loses 1–5 km per month depending on solar activity and attitude, and is periodically re-boosted by the engines of Progress or Cygnus cargo vehicles. Without re-boosts it would re-enter within one to two years.
:::

::: warning
**Failure lesson — the February 2022 Starlink loss**

On 3 February 2022, 49 Starlink satellites were released into a low 210 × 340 km parking orbit, a deliberately low orbit that ensures failed satellites re-enter quickly. A moderate geomagnetic storm the next day increased atmospheric density at that altitude by up to 50 %. The satellites, placed in a low-drag "knife-edge" attitude, could not climb out against the extra drag, and 38 re-entered. The lesson: in very low orbits, space-weather forecasts are as important as weather forecasts are for aircraft.
:::

### Very Low Earth Orbit (VLEO)

Orbits below about 350 km are attracting interest for high-resolution imaging (resolution improves in proportion to distance), lower latency and natural debris removal. Satellites such as ESA's GOCE (operated at 255 km from 2009 to 2013 using an ion engine to cancel drag), Japan's SLATS/Tsubame (as low as 167 km, 2017–2019) and a new generation of commercial VLEO imagers use streamlined shapes, electric propulsion and atmosphere-resistant materials. Some concepts even scoop up atmospheric gas to feed an electric thruster ("air-breathing electric propulsion").

## Vacuum

At 400 km the pressure is about $10^{-6}$ Pa, and in GEO about $10^{-11}$ Pa — far better vacuum than most laboratory chambers. Vacuum causes several problems:

- **Outgassing.** Polymers, adhesives, paints and composites release trapped water and volatile compounds. The vapour can condense on cold optics, star trackers and solar cells, reducing their performance. Materials are screened with the ASTM E595 test: total mass loss (TML) below 1.0 % and collected volatile condensable material (CVCM) below 0.1 %. Sensitive instruments use "bake-out" before launch, contamination budgets and heated covers.
- **Cold welding and friction.** Clean metal surfaces in contact can bond (cold weld) in vacuum because there is no oxide layer or adsorbed gas to separate them. Mechanisms use dissimilar materials, dry lubricants (MoS₂, lead), or space-qualified oils with very low vapour pressure (perfluoropolyethers, multiply-alkylated cyclopentanes).
- **Sublimation.** Some materials (cadmium, zinc, uncoated magnesium) sublimate at elevated temperatures; tin whiskers grow on pure-tin finishes. Space-grade parts forbid pure tin, cadmium and zinc plating.
- **Electrical discharge.** Between about 1 and 1 000 Pa — the pressure inside a spacecraft just after launch — the breakdown voltage of a gap reaches a minimum (Paschen's law). High-voltage equipment must be vented or switched off during ascent. In RF equipment, high-power signals can cause **multipaction**, a resonant electron avalanche between surfaces in vacuum.
- **No convection.** Heat moves only by conduction and radiation, so electronics cannot be cooled by fans and air (except inside pressurised modules).

## The Thermal Environment

### Heat Sources

A spacecraft in Earth orbit receives heat from three external sources and loses heat only by radiation (@fig:solarearthspec):

1. **Direct sunlight.** The **solar constant** at 1 AU is about $S = 1\,361$ W/m² (it varies ±3.4 % between January perihelion and July aphelion, and only ±0.1 % over the solar cycle). The spectrum peaks in the visible.
2. **Albedo.** The Earth reflects on average about 30 % of incident sunlight (0.25–0.40 depending on clouds, ice and ocean).
3. **Earth infrared.** The Earth radiates about 240 W/m² at its effective temperature of 255 K, with a peak wavelength near 10 µm.

In addition, internal electronics dissipate heat. Deep space appears as a sink at 2.7 K.

![Spectra of sunlight and of Earth's thermal emission. Because the two hardly overlap, a surface can be designed to absorb little sunlight (low α) while radiating strongly in the infrared (high ε) — the principle behind white paints and mirrors used on radiators.](figures/out/ch02_spectrum.svg){#fig:solarearthspec width=90%}

### Radiative Equilibrium

The temperature of a surface is set by the balance between absorbed and emitted power. For a flat plate facing the Sun with an insulated back:

$$\alpha\, S\, A = \varepsilon\, \sigma\, A\, T^4 \quad\Rightarrow\quad T = \left(\frac{\alpha}{\varepsilon}\,\frac{S}{\sigma}\right)^{1/4}$$

where $\alpha$ is the **solar absorptance**, $\varepsilon$ the **infrared emittance** and $\sigma = 5.67\times10^{-8}$ W m⁻² K⁻⁴ the Stefan–Boltzmann constant. The ratio $\alpha/\varepsilon$ controls temperature. For an isolated sphere (absorbing on its cross-section $\pi r^2$, radiating from its surface $4\pi r^2$) the result is $T = (\alpha S / 4\varepsilon\sigma)^{1/4}$. @fig:alphaeps shows how surface coatings span a range of more than 300 °C in equilibrium temperature.

![Absorptance–emittance map of common spacecraft surface finishes with lines of equal equilibrium temperature. Radiators use low-α/high-ε finishes (white paint, optical solar reflectors); blankets use low-ε outer layers to isolate; black paint maximises heat exchange inside instruments.](figures/out/ch02_alpha_eps.svg){#fig:alphaeps width=88%}

::: example
**Worked example — temperature of a CubeSat in sunlight and eclipse**

A 1U CubeSat (10 cm cube) is covered in solar cells (α = 0.91, ε = 0.85). In a 500 km orbit it absorbs sunlight on (on average) about 1.5 faces, plus albedo and Earth IR on the Earth-facing side. A simple estimate of absorbed power in sunlight is

$P_{in} \approx \alpha S A_{sun} + \alpha a S F A_{earth} + \varepsilon\, q_{IR} F A_{earth} + P_{int}$
$\approx 0.91\times1361\times0.015 + 0.91\times0.3\times1361\times0.5\times0.01 + 0.85\times240\times0.5\times 0.01 + 1 \approx 18.6+1.9+1.0+1 \approx 22.5$ W

The satellite radiates from 0.06 m², so $T = \left(22.5/(0.85\times5.67\times10^{-8}\times0.06)\right)^{1/4} \approx 290$ K (17 °C). In eclipse (35 minutes of a 95-minute orbit) only Earth IR and internal power remain (≈2 W), and the equilibrium would be about 150 K; thermal mass slows the cooling so that the real minimum is typically −10 to −30 °C. Batteries (operating range typically 0–40 °C for charging) usually need heaters or careful placement.
:::

### Eclipses and Thermal Cycling

A LEO satellite passes through Earth's shadow on most orbits — up to about 36 minutes of a 92-minute orbit at 400 km. It therefore experiences about 15–16 thermal cycles per day, or more than 50 000 cycles in ten years. These cycles fatigue solder joints, composite bonds and solar-array interconnects. Sun-synchronous dawn–dusk orbits avoid most eclipses. GEO satellites experience eclipses only during two **eclipse seasons** of about 45 days around the equinoxes, with a maximum eclipse of 72 minutes per day.

The thermal control techniques — insulation blankets, radiators, heat pipes, louvres and heaters — are described in Chapter 5.

## Atomic Oxygen

Between about 200 and 700 km, atomic oxygen (AO) is the most abundant gas. A satellite moving at 7.7 km/s hits AO atoms with an energy of about 5 eV, enough to break chemical bonds. AO **erodes** organic materials such as Kapton, Mylar and carbon-fibre epoxy, oxidises silver, and degrades some paints. Erosion is characterised by the **erosion yield** — the volume of material removed per incident atom:

$$\Delta x = E_y\,\Phi$$

where $\Phi$ is the fluence (atoms/cm²). Kapton H has $E_y \approx 3.0\times10^{-24}$ cm³/atom. At 400 km during solar maximum, the ram-facing fluence can exceed $10^{22}$ atoms/cm² per year, removing about 0.3 mm of Kapton per year — enough to destroy an unprotected 25 µm film in weeks. Protective measures include silicon-dioxide or aluminium-oxide coatings, AO-resistant polymers (e.g., polysiloxane-based coatings, "CP1"), silicone-based paints and metal foils. NASA's Materials International Space Station Experiment (MISSE) series has exposed thousands of material samples on the ISS exterior since 2001 to measure these effects.

![The first Materials International Space Station Experiment (MISSE-1) mounted on the outside of the ISS airlock in 2001, backdropped by an orbital sunrise. Each suitcase-like carrier exposed hundreds of material samples to atomic oxygen, ultraviolet light, radiation and thermal cycling for about 18 months before being returned to Earth for analysis.](figures/photos/ch02_misse.jpg){#fig:misse width=78%}

AO also produces a faint orange **"spacecraft glow"** on ram-facing surfaces and can affect the calibration of sensitive optical instruments.

## Plasma and Spacecraft Charging

Space is filled with **plasma** — ionised gas containing free electrons and ions. In LEO the plasma is cold (≈0.1 eV) and dense ($10^{10}$–$10^{12}$ m⁻³) — this is the ionosphere (Chapter 23). In GEO it is hot (keV energies) and tenuous. A spacecraft floating in plasma collects charge until the currents of electrons and ions to its surface balance, which sets its **floating potential**.

**Surface charging** is most severe in GEO and in high-inclination LEO orbits during geomagnetic substorms, when hot electrons (1–50 keV) are injected from the magnetotail. A sunlit surface emits photoelectrons and stays near zero potential, but shadowed dielectric surfaces may charge to thousands of volts negative. If neighbouring surfaces reach different potentials, an **electrostatic discharge (ESD)** can occur, injecting current pulses into cables, causing anomalies ("phantom commands"), or damaging solar arrays. Mitigations include conductive coatings (indium-tin oxide, Germanium-coated Kapton, carbon-loaded black Kapton), grounding all conductive parts, and limiting the voltage between adjacent solar cells.

**Internal (deep-dielectric) charging** occurs when energetic electrons (above about 0.5 MeV) penetrate shielding and accumulate inside cable insulation and circuit boards, eventually discharging. It is the dominant anomaly mechanism in GEO and MEO during periods of high outer-belt electron flux — for example after high-speed solar-wind streams. Guidelines (NASA-HDBK-4002B, ECSS-E-ST-20-06C) limit floating metal and require bleed paths for charge.

**High-voltage solar arrays** in LEO (above about 100 V) can arc into the surrounding plasma. The ISS uses 160 V arrays and a **plasma contactor unit** that emits xenon plasma to keep the structure near plasma potential, protecting astronauts during spacewalks.

## Ionising Radiation

### Sources

Three populations of energetic particles reach spacecraft:

1. **Trapped radiation (Van Allen belts).** Earth's magnetic field traps electrons and protons in two toroidal belts (@fig:belts). The **inner belt** (1.2–2.5 Earth radii, $R_E$) contains protons of tens to hundreds of MeV, produced mainly by cosmic-ray neutron decay; it is very stable. The **outer belt** (3–7 $R_E$) contains electrons of 0.1–10 MeV; it varies dramatically with solar-wind conditions. Between them lies the **slot region**. GNSS satellites (≈4.2 $R_E$) fly in the heart of the outer belt; GEO satellites (6.6 $R_E$) on its outer edge.
2. **Solar particle events (SPEs).** Large solar flares and coronal mass ejections accelerate protons (and heavier ions) to tens or hundreds of MeV. Events last hours to days and can increase radiation doses by orders of magnitude. They are the dominant hazard for astronauts beyond LEO (Chapter 30). The largest events of the space age include August 1972 (between Apollo 16 and 17) and October 1989.
3. **Galactic cosmic rays (GCRs).** Fully ionised nuclei (87 % protons, 12 % helium, 1 % heavier ions up to iron and beyond) arriving from outside the Solar System with energies up to $10^{20}$ eV. Their flux is low but they are nearly impossible to shield, and heavy ions cause single-event effects in electronics. GCR flux is about 2–3 times higher at solar minimum, when the weaker solar wind lets more of them in.

![Cross-section of Earth's magnetic field and radiation belts. Low Earth orbit lies below the belts except over the South Atlantic Anomaly; navigation satellites fly through the outer electron belt; geostationary satellites sit at its outer edge.](figures/out/ch02_belts.svg){#fig:belts width=96%}

Because Earth's magnetic axis is offset and tilted relative to its rotation axis, the inner belt comes closest to the surface over South America and the South Atlantic — the **South Atlantic Anomaly (SAA)**. LEO satellites, including the ISS and Hubble, receive most of their trapped-proton dose during SAA passes, and many instruments switch off or flag their data there (@fig:saa). In polar orbits, satellites also cross the "horns" of the outer belt at high latitudes and are exposed to solar particles, which reach low altitudes near the magnetic poles.

![Schematic map of the regions where LEO satellites receive most of their radiation: the South Atlantic Anomaly and the high-latitude auroral zones, with one day of International Space Station ground track overlaid.](figures/out/ch02_saa.png){#fig:saa width=96%}

### Radiation Effects on Electronics and Materials

Radiation affects spacecraft in three main ways:

- **Total ionising dose (TID).** Energy deposited by ionisation accumulates over the mission, trapping charge in oxides of transistors and shifting their threshold voltages and leakage currents until circuits fail. Dose is measured in gray (Gy = 1 J/kg) or, traditionally, **rad** (1 rad = 0.01 Gy), quoted for silicon as krad(Si).
- **Displacement damage dose (DDD).** Protons and neutrons knock atoms out of the crystal lattice, degrading solar cells, optocouplers, CCD and CMOS image sensors (more "hot pixels", worse charge-transfer efficiency) and bipolar transistors.
- **Single-event effects (SEEs).** A single heavy ion or energetic proton deposits a dense track of charge that can flip a memory bit (**single-event upset, SEU**), disturb an analogue output (**single-event transient, SET**), latch a CMOS circuit into a high-current state that can burn it out (**single-event latch-up, SEL**), or destroy power MOSFETs (**single-event burnout, SEB; single-event gate rupture, SEGR**).

@tbl:radeffects summarises effects and mitigations.

Table: Radiation effects, typical causes and mitigations. {#tbl:radeffects}

| Effect | Main cause | Typical consequence | Mitigations |
|---|---|---|---|
| Total ionising dose (TID) | Trapped electrons and protons, SPE protons | Parameter drift, increased power, eventual failure | Shielding, rad-hard parts, derating, spot shielding, part screening (lot acceptance testing) |
| Displacement damage (DDD) | Protons, neutrons | Solar array power loss, detector dark current, CCD charge transfer loss | Cover glass, annealing, operating detectors cold, design margins (typically 15–30 % end-of-life array margin) |
| Single-event upset (SEU) | Heavy ions (GCR, SPE), protons in SAA | Bit flips in memories and registers | Error detection and correction (EDAC), triple modular redundancy (TMR), memory scrubbing, watchdogs |
| Single-event latch-up (SEL) | Heavy ions, protons | High current; destructive if not cleared | Latch-up-immune technologies (SOI), current limiters with automatic power cycling |
| Single-event burnout / gate rupture | Heavy ions | Permanent destruction of power devices | Voltage derating (e.g., operate at < 50–75 % of rated V_DS), rad-hard MOSFETs |
| Single-event functional interrupt (SEFI) | Heavy ions | Processor or FPGA hangs | Watchdog timers, reset logic, configuration scrubbing |

Electronic parts are classified by their tolerance. Commercial off-the-shelf (COTS) parts often survive 5–30 krad(Si) and can be susceptible to latch-up; **radiation-tolerant** parts are characterised to 30–100 krad; **radiation-hardened** parts are designed for 100 krad to more than 1 Mrad and are latch-up immune. Rad-hard parts are expensive and lag commercial technology by one to two decades in performance — a major reason why AI processors in space are a challenge (Chapter 43).

![Illustrative annual total ionising dose behind spherical aluminium shielding for four orbits. MEO is the harshest common orbit; LEO at ISS altitude is comparatively benign. Shielding is effective against electrons (MEO, GEO) but less effective against high-energy protons.](figures/out/ch02_dose_depth.svg){#fig:dosedepth width=88%}

### Estimating Upset Rates

The susceptibility of a device to single-event effects is measured in particle accelerators. The result is a curve of **cross-section** $\sigma$ (the effective sensitive area per bit or per device) versus **linear energy transfer (LET)**, the energy deposited per unit path length, usually given in MeV·cm²/mg (@fig:weibull). A device with a threshold LET above about 37 MeV·cm²/mg is considered effectively immune to heavy-ion upsets in most environments, because heavier, more ionising particles are very rare. The upset rate is found by folding the cross-section curve with the LET spectrum of the orbit (tools: CREME96, OMERE, SPENVIS).

![Single-event upset cross-section versus LET for three classes of memory, fitted with Weibull functions. Hardening raises the threshold LET and lowers the saturated cross-section, reducing upset rates by orders of magnitude.](figures/out/ch02_weibull.svg){#fig:weibull width=82%}

::: note
**Engineering note — radiation design margin**

Agencies require a **radiation design margin (RDM)** — the ratio of a part's tested capability to the predicted mission dose at its location. NASA and ESA practice is typically RDM ≥ 2 for TID (with lot-specific test data), rising for parts with large lot-to-lot variability. Dose predictions use standard models: AE8/AP8 or the newer **AE9/AP9-IRENE** for trapped particles, ESP/PSYCHIC or SAPPHIRE for solar protons, and ISO 15390 or Badhwar–O'Neill for cosmic rays, combined with ray-tracing through a 3-D model of the spacecraft (sector analysis) to find the shielding at each part.
:::

## Micrometeoroids and Orbital Debris

### The Particle Population

Two kinds of small particles strike spacecraft at hypervelocity:

- **Micrometeoroids** — natural dust from comets and asteroids. They arrive from all directions at 11–72 km/s (average about 20 km/s), with annual showers such as the Perseids and Leonids adding short peaks. About 30–40 tonnes of meteoroid material enter Earth's atmosphere every day.
- **Orbital debris** — artificial objects: fragments from explosions and collisions, paint flakes, solid-rocket-motor slag and aluminium-oxide dust, and dead satellites. In LEO, debris impacts occur at an average of about 10 km/s, mainly from directions near the velocity vector.

For particles smaller than about 0.1 mm, meteoroids dominate; for larger particles in LEO, debris dominates. Objects larger than about 10 cm in LEO (1 m in GEO) are tracked and catalogued (Chapter 21); the roughly one million objects between 1 and 10 cm are not tracked and cannot be avoided, yet they carry enough energy to destroy a satellite. A 1 cm aluminium sphere at 10 km/s has a kinetic energy of about 70 kJ — similar to a small car at 50 km/h.

![Illustrative cumulative flux of meteoroids and orbital debris at ISS altitude. The steep size dependence means that small impacts are frequent but survivable, while the rare large impacts are catastrophic.](figures/out/ch02_mmod_flux.svg){#fig:mmodflux width=88%}

### Shielding

The standard protection is the **Whipple shield**, invented by astronomer Fred Whipple in 1947 (@fig:whipple). A thin sacrificial **bumper** placed some distance in front of the main wall shatters the incoming particle into a cloud of fragments and vapour, which spreads out and is stopped by the rear wall. A Whipple shield is far more mass-efficient than a single thick wall. Variants include the **stuffed Whipple shield** (with layers of Nextel ceramic fabric and Kevlar between bumper and wall, used on the ISS) and **multi-shock shields**. The ISS has more than 100 types of shield and is the most heavily protected spacecraft ever flown; the Bigelow-built BEAM and future inflatable habitats use multiple layers of fabric.

![Principle of the Whipple shield. The bumper breaks up and partly vaporises the projectile; the resulting cloud spreads its momentum over a large area of the rear wall.](figures/out/ch02_whipple.svg){#fig:whipple width=88%}

![The Long Duration Exposure Facility (LDEF), a 9.7-tonne bus-sized cylinder carrying 57 experiments, being retrieved by Space Shuttle Columbia in January 1990 after almost six years in orbit. LDEF's surfaces recorded more than 30 000 impact craters visible to the naked eye and remain a cornerstone data set for meteoroid, debris and atomic-oxygen models.](figures/photos/ch02_ldef.jpg){#fig:ldef width=78%}

Shield performance is described by **ballistic limit equations** (BLEs) — empirical fits to hypervelocity gun tests (light-gas guns reach about 7 km/s) and hydrocode simulations that give the critical particle diameter $d_c$ that just perforates the rear wall as a function of velocity, impact angle, particle density and shield geometry. Combining the BLE with the flux model gives the **probability of no penetration (PNP)** over the mission, typically required to be above 0.95–0.99 for critical elements. Tools include NASA's BUMPER and ESA's ESABASE2/Debris.

::: data
**Data box — MMOD on the ISS and Hubble**

- The ISS has been struck by many thousands of small particles; impact pits are regularly found on windows (the Cupola windows have external shutters for protection), radiators and handrails.
- In 2021 an untracked object punched a 5 mm hole through the thermal blanket of the Canadarm2 boom — the arm continued to work.
- Solar arrays returned from Hubble servicing missions (1993, 2002) showed thousands of impact features, used to calibrate debris models.
- The ISS performs a debris-avoidance manoeuvre when a tracked object's collision probability exceeds about 1 in 10 000 (or about 1 in 100 000 if the manoeuvre is easy); it has manoeuvred more than 40 times since 1999.
:::

## Mechanical Environments: Launch and Microgravity

### Launch Loads

The most mechanically severe minutes of a spacecraft's life are during launch. Loads arise from:

- **Quasi-static acceleration.** Steady thrust produces axial accelerations of 3–6 g at burnout (Falcon 9 ≈ 4–5 g, Ariane 6 ≈ 4.5 g, Soyuz ≈ 4.3 g); low-frequency dynamic transients add lateral accelerations of 1–2 g.
- **Sine vibration.** Low-frequency (5–100 Hz) oscillations from engine ignition, pogo, wind gusts and staging. Spacecraft must have their primary structural natural frequencies above values specified by the launcher (typically > 20–25 Hz axial and > 10–15 Hz lateral) to avoid dynamic coupling.
- **Random vibration.** Broadband vibration (20–2 000 Hz) transmitted through the structure from engines and aerodynamic turbulence. Components are tested to spectra such as NASA's General Environmental Verification Standard (GEVS) shown in @fig:gevs.
- **Acoustic noise.** Sound pressure levels inside the fairing reach 135–145 dB overall at lift-off and in the transonic region, exciting light, large-area structures such as solar panels and antennas.
- **Shock.** Pyrotechnic separation events (fairing jettison, stage and spacecraft separation) produce short, high-frequency accelerations of thousands of g, characterised by a **shock response spectrum (SRS)**. Shock attenuates rapidly with distance, so sensitive units are placed away from separation interfaces.

![Random-vibration qualification and acceptance spectra from NASA's GEVS for small components. The plateau from 50 to 800 Hz at 0.16 g²/Hz corresponds to an overall level of 14.1 g rms.](figures/out/ch02_gevs.svg){#fig:gevs width=82%}

### Microgravity

Once in orbit, the spacecraft and everything in it are in free fall. Residual accelerations of $10^{-6}$ to $10^{-3}$ g arise from drag, gravity gradient, rotation, crew motion and machinery. Microgravity matters for fluid management (propellant does not settle at the bottom of a tank; see Chapter 6), for heat transfer (no buoyant convection, so boiling and combustion behave differently), for deployable structures (which must be tested on the ground with gravity-offloading rigs), and for the human body (Chapter 30). It is also a resource: in-space manufacturing (Chapter 40) exploits it to make materials impossible to make on Earth.

## Environments Beyond Earth Orbit

Deep-space missions face additional environments. @tbl:planetenv and @fig:planettemps summarise some of the most demanding.

Table: Representative environmental challenges for planetary missions. {#tbl:planetenv}

| Destination | Key environmental challenges | Engineering responses (examples) |
|---|---|---|
| Moon | Surface −170 °C to +120 °C at the equator; 14-day nights; permanently shadowed craters near 25–40 K; abrasive, electrostatically charged dust; no magnetic field or atmosphere | Radioisotope heater units, lunar-night survival modes, dust-tolerant seals and connectors, radiation shielding for crews |
| Mars | Thin CO₂ atmosphere (≈0.6 % of Earth's pressure); dust storms reducing sunlight; −125 °C to +20 °C; perchlorate-laden dust; no global magnetic field | Entry heat shields and parachutes (Chapter 27), RTG or dust-tolerant solar power, heaters, dust-clearing strategies |
| Venus | Surface 465 °C and 92 bar, sulfuric-acid clouds; super-rotating winds | Pressure vessels and insulation (Venera landers survived up to 127 minutes); silicon-carbide electronics research |
| Mercury / near-Sun | Solar flux up to 11 times Earth's (Mercury) or ≈500 times (Parker Solar Probe at closest approach); intense heating from planet's surface | Heat shields (Parker's 11.4 cm carbon-composite shield), high-temperature solar arrays, sunshades, special orbit design |
| Jupiter system | The most intense radiation belts in the Solar System — Europa Clipper receives ≈2.8 Mrad behind 0.1 inch of aluminium | Radiation vaults (Juno's 1 cm titanium vault, Clipper's aluminium-zinc vault), orbits that minimise belt passages |
| Outer Solar System | Sunlight 1/100 to 1/1000 of Earth's; temperatures 40–100 K; light-hour communication delays | RTGs, low-temperature materials, high-autonomy operations |
| Interplanetary cruise | Solar particle events, GCRs, micrometeoroid streams near comets | Shielding, fault protection, safe modes, trajectory selection |

![Temperature ranges at the surfaces (or local environments) of selected Solar System bodies. Thermal design must cover both extremes — and, for landers, the transition from cruise vacuum to surface conditions.](figures/out/ch02_planet_temps.svg){#fig:planettemps width=88%}

## Designing for the Environment: Standards and Tools

Engineers capture the environment in a project **environmental specification**, derived from standards such as **ECSS-E-ST-10-04C** (space environment), **NASA-STD-7009**/**NASA-HDBK-1001** (terrestrial and natural space environments), **ISO 15390** (cosmic rays), the **AE9/AP9** models, **ORDEM 3.2** and **MASTER-8** (debris), **MEM 3** (meteoroids) and **NRLMSIS 2.0** (atmosphere). ESA's online **SPENVIS** system and NASA's **Space Environments and Effects (SEE)** program provide integrated tools.

![NASA's Juno spacecraft emerging from thermal-vacuum testing at Lockheed Martin in 2011. In the chamber the spacecraft was cycled between the hot and cold extremes predicted for its mission while operating, verifying both the thermal design and the electronics.](figures/photos/ch02_tvac.jpg){#fig:tvac width=78%}

The environmental specification feeds the verification programme: thermal-vacuum and thermal-balance tests, vibration, acoustic and shock tests, EMC tests, radiation tests of parts, and material screening (Chapter 4). The general principle is **"test as you fly, fly as you test"**: every environment the spacecraft will meet in flight should, as far as practical, be reproduced or bounded on the ground.

::: key
**Key takeaways**

- Atmospheric density at a given LEO altitude varies by ~10× over the solar cycle; drag sets satellite lifetime (about 1–3 years at 400 km, decades at 600 km, centuries at 800 km).
- Vacuum causes outgassing, cold welding and discharges; the thermal environment is governed by radiation balance and the α/ε ratio of surfaces.
- Atomic oxygen erodes polymers in LEO; plasma causes surface and internal charging, most severely in GEO and MEO.
- Radiation causes total dose, displacement damage and single-event effects; MEO is the harshest common orbit, and Jupiter the harshest planetary environment.
- Micrometeoroids and debris strike at 10–20 km/s; Whipple shields defeat particles up to about 1 cm, and larger objects must be tracked and avoided.
- Launch imposes quasi-static, sine, random, acoustic and shock loads that often size the structure; environmental testing reproduces these on the ground.
:::

::: questions
**Review questions**

1. Why does atmospheric density at 400 km change by about a factor of ten over a solar cycle, and what does this mean for satellite lifetime?
2. With a scale height of 60 km, by what factor does density fall between 400 km and 450 km altitude?
3. A plate at 1 au faces the Sun with α = 0.2 and ε = 0.8 on its sunlit face and loses heat only from that face. Estimate its equilibrium temperature.
4. What is atomic oxygen, at which altitudes does it matter most, and how are exposed materials protected?
5. Distinguish surface charging from internal (deep dielectric) charging. In which orbits is each most severe?
6. Explain the differences between total ionising dose, displacement damage and single-event effects, and give one mitigation for each.
7. How does a Whipple shield work, and why must objects larger than about 1 cm be tracked and avoided instead?
8. List the main mechanical loads during launch and explain why they, rather than the space environment, often size a spacecraft's structure.
:::
