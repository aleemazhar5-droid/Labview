---
title: Space Probes and Flyby Missions
hero: ch26
abstract: A flyby gives a few hours of close-up science after years of travel, yet flybys revealed most of the Solar System to us — the volcanoes of Io, the rings of Uranus, the geysers of Triton, the nitrogen glaciers of Pluto. This chapter explains the different kinds of space probes — flyby spacecraft, atmospheric entry probes, impactors and interstellar travellers — and the engineering behind them, from encounter navigation and imaging at 14 km/s to radioisotope power and data links across 25 billion kilometres. It follows the Pioneers, Voyagers and New Horizons to the edge of the heliosphere, describes how DART moved an asteroid, and reviews the probes active in 2026.
---

A **space probe** is an uncrewed spacecraft that leaves Earth orbit to explore the Solar System. In a broad sense every planetary mission is a probe, but this chapter concentrates on missions that do not stay in orbit or land — spacecraft that **fly past** their targets, **plunge into** atmospheres, **crash into** surfaces on purpose, or travel **out of the Solar System**. Orbiters are described in Chapter 25, landers in Chapter 27, rovers in Chapter 28 and sample-return missions in Chapter 29.

## Kinds of Probes

| Type | What it does | Advantages | Limitations | Examples |
|---|---|---|---|---|
| Flyby | Passes a target once, observing for hours to days | Cheapest way to reach a new world; can visit several targets | Brief, one-sided view; high speed blurs images | Mariner 4, Voyager 1 and 2, New Horizons, Lucy |
| Atmospheric entry probe | Enters an atmosphere, measuring it during descent | Direct measurement of composition, temperature, winds | Short life (minutes to hours); extreme entry heating | Pioneer Venus, Galileo probe, Huygens |
| Impactor | Strikes a surface deliberately | Excavates subsurface material; tests asteroid deflection | Single event; must be observed by another spacecraft or telescope | Deep Impact, LCROSS, DART |
| Heliospheric and interstellar | Travels outward to sample the solar wind and interstellar medium | The only direct measurements of the Sun's outer boundary | Power and communications limits; decades-long missions | Pioneer 10 and 11, Voyager 1 and 2 |
| Close-solar | Dives towards the Sun | In-situ measurements of the corona | Intense heat; needs many gravity assists | Helios, Parker Solar Probe, Solar Orbiter (Chapter 22) |

: The main kinds of probes discussed in this chapter. {#tbl:probetypes}

Flybys are the natural first step in exploring a world. A flyby needs no braking propellant and can be combined with gravity assists to reach several targets in one mission (Chapter 24). They are followed, where budgets allow, by orbiters for global mapping and landers for surface measurements. For the most distant worlds — Uranus, Neptune, Pluto and the Kuiper Belt — flybys remain our only close-up views.

## Sixty Years of Flybys

The first spacecraft to escape Earth was the Soviet **Luna 1** in January 1959. It missed the Moon by about 6 000 km and became the first artificial object in orbit around the Sun. The same year **Luna 3** photographed the Moon's far side. The planetary era began with NASA's **Mariner 2**, which flew past Venus in December 1962 and showed that its surface was hot enough to melt lead. **Mariner 4** returned the first close-up pictures of another planet — 21 images of a cratered, Moon-like Mars — in July 1965 (@fig:probehistory).

![Milestones in flyby and probe exploration, 1959–2033.](figures/out/ch26_history.svg){#fig:probehistory width=100%}

**Mariner 10** (1973–75) was the first spacecraft to use a gravity assist: a Venus flyby bent its path towards Mercury, which it passed three times. **Pioneer 10** became the first spacecraft to cross the asteroid belt and fly past Jupiter (December 1973); **Pioneer 11** followed it past Jupiter and then made the first Saturn flyby in 1979. In 1986 an international fleet — the **Halley Armada** of ESA's Giotto, the Soviet Vega 1 and 2, and Japan's Suisei and Sakigake — met Halley's Comet; Giotto passed 596 km from the nucleus and returned the first images of a comet's core.

| Year | Spacecraft | Achievement |
|---|---|---|
| 1959 | Luna 1 (USSR) | First spacecraft to escape Earth and orbit the Sun |
| 1959 | Luna 3 (USSR) | First images of the Moon's far side |
| 1962 | Mariner 2 (USA) | First successful planetary flyby (Venus) |
| 1965 | Mariner 4 (USA) | First close-up images of Mars |
| 1967 | Venera 4 (USSR) | First data from inside another planet's atmosphere (Venus) |
| 1973 | Pioneer 10 (USA) | First crossing of the asteroid belt; first Jupiter flyby |
| 1974 | Mariner 10 (USA) | First gravity assist; first Mercury flyby |
| 1979 | Pioneer 11 (USA) | First Saturn flyby |
| 1985 | ICE (USA) | First comet encounter (Giacobini–Zinner) |
| 1986 | Giotto (ESA) | First close images of a comet nucleus (Halley) |
| 1986, 1989 | Voyager 2 (USA) | Only flybys of Uranus and Neptune |
| 1991, 1993 | Galileo (USA) | First asteroid flybys (Gaspra, Ida) and first asteroid moon (Dactyl) |
| 1995 | Galileo probe (USA) | First entry probe into a giant planet |
| 2005 | Deep Impact (USA) | First impact experiment on a comet |
| 2012 | Voyager 1 (USA) | First spacecraft in interstellar space |
| 2015 | New Horizons (USA) | First Pluto flyby |
| 2019 | New Horizons (USA) | Most distant object explored (Arrokoth, 6.6 billion km) |
| 2022 | DART (USA) | First change of an asteroid's orbit by a human-made object |

: Firsts in flyby and probe exploration. {#tbl:probefirsts}

## The Grand Tour: Pioneer and Voyager

### Pioneer 10 and 11

The two Pioneers were simple, spin-stabilised spacecraft of about 260 kg, powered by four SNAP-19 radioisotope generators and communicating through a 2.74 m dish (@fig:pioneer). Their main task was to find out whether a spacecraft could survive the asteroid belt and Jupiter's radiation belts. They could — just: Pioneer 10's instruments recorded radiation doses close to their limits. Both spacecraft carry a gold-anodised plaque showing a man and a woman and the Sun's location relative to 14 pulsars. Pioneer 11 fell silent in 1995 and Pioneer 10 in 2003, at a distance of 80 AU.

![Pioneer 10 being prepared for launch in 1972. The 2.74 m antenna dominates the spacecraft; the radioisotope generators are on booms to keep their radiation away from the instruments.](figures/photos/ch26_pioneer.jpg){#fig:pioneer width=62%}

### Voyager 1 and 2

In the late 1970s the four giant planets lined up so that a single spacecraft could visit all of them, using each one's gravity to reach the next — an alignment that occurs about once every 175 years. NASA's two **Voyagers**, launched in August and September 1977, made use of it (@fig:grandtour). Voyager 1 flew past Jupiter (March 1979) and Saturn (November 1980); it was then deliberately sent close to Saturn's moon Titan, which bent its path northward out of the ecliptic. Voyager 2 visited Jupiter (July 1979), Saturn (August 1981), Uranus (January 1986) and Neptune (August 1989) — still the only spacecraft to have seen the two ice giants close up.

![The trajectories of the five spacecraft that are leaving the Solar System, computed from the planets' positions on the actual encounter dates.](figures/out/ch26_grandtour.svg){#fig:grandtour width=86%}

Each Voyager weighed 825 kg at launch and carried ten science instruments, a 3.66 m high-gain antenna, three radioisotope generators producing 470 W, and a scan platform that pointed the cameras and spectrometers without turning the whole spacecraft (@fig:voyagerart). Their three onboard computers had a combined memory of about 69 kilobytes, and data were recorded on an eight-track digital tape recorder.

![Artist's concept of a Voyager spacecraft. The 3.66 m antenna points to Earth; the magnetometer boom (13 m) and the RTG boom extend to the sides.](figures/photos/ch26_voyager.jpg){#fig:voyagerart width=70%}

The Voyagers transformed planetary science:

- **Jupiter:** active volcanoes on Io — the first seen beyond Earth — a thin ring, and the cracked, icy surface of Europa, hinting at an ocean beneath.
- **Saturn:** thousands of ringlets and the "spokes" in the rings, shepherd moons that confine narrow rings, and a thick nitrogen atmosphere on Titan.
- **Uranus:** a magnetic field tilted by 59° to the rotation axis, ten new moons and the bizarre, patchwork surface of Miranda.
- **Neptune:** the Great Dark Spot, the fastest winds in the Solar System (about 2 000 km/h), and nitrogen geysers on its large moon Triton, which orbits backwards and is probably a captured Kuiper Belt object (@fig:neptune).

![Neptune imaged by Voyager 2 in August 1989, showing the Great Dark Spot (centre) and bright methane-ice clouds.](figures/photos/ch26_neptune.jpg){#fig:neptune width=46%}

On 14 February 1990, at a distance of 6 billion km, Voyager 1 turned its cameras back towards the Sun and photographed the planets for a "family portrait". In one frame Earth appears as a pale blue dot less than a pixel across (@fig:paleblue). The cameras were then switched off to save power and memory; they have not been used since.

![The "Pale Blue Dot": Earth (in the band of scattered sunlight, right of centre) seen by Voyager 1 from 6 billion km in 1990, reprocessed in 2020.](figures/photos/ch26_paleblue.jpg){#fig:paleblue width=48%}

Each Voyager carries a **Golden Record** — a gold-plated copper disc with sounds and images of Earth, greetings in 55 languages and 90 minutes of music — in case either spacecraft is ever found by another civilisation.

## Engineering a Flyby

### Arriving at the Right Place at the Right Time

A flyby is aimed in the **B-plane**, the plane through the target's centre perpendicular to the incoming asymptote of the hyperbolic trajectory (Chapter 24). The aim point in this plane determines the closest-approach distance and the bending of the trajectory; the arrival time determines which side of the target is lit and which moons can be observed. Errors grow as the spacecraft approaches: a small velocity error made weeks before encounter can move the aim point by thousands of kilometres. Navigators therefore combine radio tracking (Doppler, ranging and delta-DOR) with **optical navigation** — images of the target against the stars taken by the spacecraft's own cameras — and make a series of trajectory correction manoeuvres in the final weeks. For the Pluto flyby, the uncertainty in Pluto's own position, known only from 85 years of telescopic observations, was larger than that of the spacecraft; optical navigation reduced it to a few hundred kilometres before the encounter. New Horizons arrived within about 90 seconds of the planned time.

### Sequences and Fault Protection

The most important hours of a flyby must run without help from the ground: at Pluto, a radio signal took 4.5 hours each way. The encounter is therefore executed by a **command sequence** loaded days in advance, which points the spacecraft and instruments, sets exposure times and records the data. **Fault protection** software monitors the spacecraft and, if a problem occurs, puts it into a safe state — but during an encounter, entering safe mode could mean losing the unrepeatable observations. Flyby sequences therefore include special "critical sequence" fault protection that keeps the observations going through most faults. Ten days before the Pluto flyby, on 4 July 2015, New Horizons went into safe mode when its main computer was overloaded while compressing data and loading the encounter sequence at the same time; the team recovered the spacecraft in three days and lost only minor science.

### Imaging at High Speed

A flyby spacecraft sees its target grow from a dot to a world in a few days, and then sweep past in hours. The resolution — the size of a camera pixel projected on the target — improves in proportion to the distance, but the target's angular rate rises sharply near closest approach (@fig:nhflyby). New Horizons passed Pluto at 13.78 km/s; at closest approach, 12 500 km above the surface, Pluto's centre moved across the sky at 0.058° per second, and a feature would cross one pixel of the LORRI telescopic camera in about 5 milliseconds. Exposures had to be short, or the spacecraft had to turn to follow the target, which it did with its thrusters.

![New Horizons at Pluto. (a) The resolution of the LORRI camera and the colour imager improved from kilometres to about 70 m per pixel at closest approach. (b) Pluto's angular rate rose more than ten-thousandfold in the last two days.](figures/out/ch26_nhflyby.svg){#fig:nhflyby width=96%}

Voyager mounted its cameras on a **scan platform** that could point independently of the spacecraft, so the high-gain antenna could stay pointed at Earth. New Horizons, to save mass and complexity, had no scan platform: the whole spacecraft turned to point its instruments, so it could not transmit while observing. It recorded about 6.25 gigabytes during the Pluto encounter on two solid-state recorders and then spent 15 months sending it to Earth at 1–4 kilobits per second.

::: example
**Example: image smear during a flyby**

At closest approach to Pluto, New Horizons was 13 690 km from Pluto's centre, moving at 13.78 km/s.

1. Angular rate of the target as seen from the spacecraft: $\omega = v/d$ = 13.78 / 13 690 = 1.0 × 10⁻³ rad/s (0.058°/s).
2. LORRI's pixels subtend 4.96 µrad. The time for the image to move by one pixel is 4.96 × 10⁻⁶ / 1.0 × 10⁻³ ≈ 5 ms.
3. Sunlight at 33 AU is 1/1 100 as bright as at Earth, so long exposures are tempting; but an exposure of 50 ms would smear the image over 10 pixels unless the spacecraft rotated to track the target.
4. A day earlier, at 1.2 million km, Pluto was almost straight ahead: its angular rate, $v\,b/r^2$ with $b$ = 13 690 km, was only about 10⁻⁷ rad/s and smear was negligible — but each pixel covered 6 km.

The design of a flyby encounter is therefore a trade between distance (resolution), speed of tracking (smear) and the time needed to observe each target.
:::

### Pluto and Arrokoth: New Horizons

**New Horizons** was launched on 19 January 2006 on an Atlas V with an additional solid-fuel upper stage, leaving Earth faster than any spacecraft before it (about 16.3 km/s relative to Earth). A Jupiter flyby in February 2007 shortened its journey by three years. Most of the 9.5-year cruise was spent in hibernation, with the spacecraft spinning slowly and sending a weekly beacon tone.

At Pluto on 14 July 2015, it found a geologically active world: **Sputnik Planitia**, a 1 000 km plain of nitrogen ice slowly convecting in cells tens of kilometres across; mountains of water ice several kilometres high; a blue, layered haze; and evidence of a possible ocean beneath the ice. Its large moon **Charon** has a vast canyon system and a reddish polar cap made of material from Pluto's escaping atmosphere (@fig:charon).

![Charon in enhanced colour from New Horizons. The reddish polar region (top) is coloured by organic material formed from methane that escaped from Pluto.](figures/photos/ch26_charon.jpg){#fig:charon width=46%}

On 1 January 2019, New Horizons flew 3 500 km past **Arrokoth**, a 36 km Kuiper Belt object 6.6 billion km from the Sun — the most distant object ever explored. Arrokoth turned out to be a "contact binary" of two flattened lobes that merged gently at walking speed, supporting the theory that planetesimals formed by the gentle collapse of clouds of pebbles. New Horizons continues to study the Kuiper Belt, the heliosphere and the faint cosmic optical background, which can only be measured from far beyond the zodiacal dust of the inner Solar System.

## Power and Communications Far from the Sun

### Radioisotope Power

Sunlight weakens with the square of the distance: at Jupiter it is 1/27 as strong as at Earth, at Saturn 1/90 and at Pluto about 1/1 100. Solar arrays work as far as Jupiter — Juno, JUICE, Europa Clipper and Lucy all use very large arrays — but beyond that every probe has relied on **radioisotope thermoelectric generators** (RTGs), which convert heat from the decay of plutonium-238 into electricity (Chapter 5).

| Generator | Electrical power at launch | Mass | Missions |
|---|---|---|---|
| SNAP-19 | ≈ 40 W | 14 kg | Pioneer 10 and 11 (four each), Viking landers |
| MHW-RTG | ≈ 158 W | 38 kg | Voyager 1 and 2 (three each), LES-8 and 9 |
| GPHS-RTG | ≈ 290 W | 56 kg | Ulysses, Galileo, Cassini, New Horizons |
| MMRTG | ≈ 110 W | 45 kg | Curiosity, Perseverance, Dragonfly |
| Next-Generation RTG | ≈ 250 W (design) | — | In development for missions of the 2030s |

: Radioisotope thermoelectric generators used on US deep-space probes. {#tbl:rtgs}

An RTG's output declines for two reasons: the plutonium decays with a half-life of 87.7 years, and the thermocouples degrade as they age. For the Voyagers, the combined effect is a loss of about 4 W per year (@fig:voyagerpower). From 470 W at launch, each Voyager had about 220 W in 2026. To keep operating, engineers have switched off the cameras (1990), the scan platforms, heaters and, one by one, the science instruments: Voyager 1's cosmic ray instrument in February 2025 and its low-energy charged particle instrument in April 2026, and Voyager 2's low-energy charged particle instrument in March 2025. In 2026 Voyager 1 retained only its magnetometer and plasma wave instruments. The team plans to keep at least one instrument running on each spacecraft into the 2030s.

![Electrical power available on each Voyager. Ageing thermocouples make the decline faster than plutonium decay alone; instruments are switched off as power falls.](figures/out/ch26_power.svg){#fig:voyagerpower width=92%}

Keeping 49-year-old spacecraft alive has required remarkable engineering. In November 2023, Voyager 1 began sending meaningless data; engineers traced the fault to one failed memory chip in its flight data system and, in April 2024, moved the affected code to other parts of the memory — a software patch sent across 24 billion km. In 2025 they revived Voyager 1's primary roll thrusters, which had been considered dead since 2004, as a backup to its degrading secondary thrusters, whose fuel lines are slowly clogging with silicon dioxide.

### Talking across the Solar System

Radio signals weaken with the square of the distance as well, so a probe's data rate falls as it travels outward (@fig:downlink). At Jupiter in 1979, each Voyager returned up to 115 kilobits per second; at Neptune, ten years later, it achieved 21.6 kbit/s only because NASA had enlarged its 64 m antennas to 70 m and combined them electronically with other radio telescopes, including the Very Large Array and Australia's Parkes dish. In 2026, Voyager 1 transmits at 160 bits per second; its signal, from a 21 W transmitter, delivers only about 3 × 10⁻¹⁹ W to a 70 m antenna on Earth.

![Data rate versus distance for a Voyager-class X-band link. The orange points are rates actually achieved.](figures/out/ch26_downlink.svg){#fig:downlink width=90%}

Because Voyager 2 is heading south, far below the ecliptic, it can be seen only from the southern hemisphere, and only the 70 m antenna at Canberra (DSS-43) has an S-band transmitter able to command it. When that antenna was upgraded between March and October 2020, Voyager 2 could receive no commands. In August 2023 an incorrect command turned Voyager 2's antenna 2° away from Earth; the team regained contact by "shouting" — transmitting at high power from Canberra in the hope that some of the signal would reach the spacecraft, which it did.

::: example
**Example: Voyager 1's link budget in 2026**

Voyager 1 is 172 AU (2.57 × 10¹³ m) from Earth, transmitting 21.3 W at 8.415 GHz (wavelength 3.56 cm) through a 3.66 m antenna to a 70 m Deep Space Network antenna.

1. Transmit power: 10 log₁₀ 21.3 = 13.3 dBW.
2. Antenna gains $G = \eta (\pi D/\lambda)^2$: transmit (η = 0.55) 47.6 dBi; receive (η = 0.60) 73.6 dBi.
3. Free-space loss $(4\pi d/\lambda)^2$ = 319.2 dB.
4. Received power: 13.3 + 47.6 + 73.6 − 319.2 = −184.7 dBW, or 3.4 × 10⁻¹⁹ W.
5. Noise density for a 22 K receiving system: $kT$ = −228.6 + 13.4 = −215.2 dBW/Hz. Carrier-to-noise density: 30.5 dB-Hz.
6. At 160 bit/s (22.0 dB-Hz), the energy per bit relative to noise is $E_b/N_0$ = 8.5 dB. Voyager's concatenated coding needs about 2.5 dB, leaving about 6 dB of margin for pointing losses, weather and the noise of the sky.
7. The one-way light time is 23.8 hours: a command sent on Monday morning is answered on Wednesday morning. On 18 November 2026, Voyager 1 becomes the first spacecraft one light-day from Earth.
:::

## Atmospheric Entry Probes

An entry probe is released from a carrier spacecraft weeks before arrival, coasts to the planet and enters its atmosphere at high speed, protected by a heat shield. Once it has slowed, it deploys a parachute and descends, measuring temperature, pressure, composition, clouds and winds and relaying its data to the carrier spacecraft overhead.

The Soviet **Venera 4** returned the first data from inside the atmosphere of Venus in 1967 before being crushed by the pressure. NASA's **Pioneer Venus Multiprobe** dropped one large and three small probes into Venus in December 1978; one of them survived impact and transmitted from the surface for 67 minutes. In 1985 the Soviet–French **Vega** missions placed two balloons in the Venus atmosphere at 54 km altitude, where they floated for two days, tracked by radio telescopes around the world.

**The Galileo probe** remains the only probe to have entered a giant planet. Released five months before arrival, it entered Jupiter's atmosphere on 7 December 1995 at 47.4 km/s — the fastest atmospheric entry ever — and decelerated at up to 228 *g*. Its carbon-phenolic heat shield, 152 kg of the probe's 339 kg, lost about 80 kg to ablation. The probe transmitted for 58 minutes and descended about 150 km below the cloud tops, to a pressure of 22 bar. It found less water than expected — it had entered a dry "hot spot" — winds of over 600 km/h, and heavy noble gases more enriched than models predicted, which changed theories of how Jupiter formed. ESA's **Huygens** probe, which descended through Titan's atmosphere and landed on its surface in 2005, is described in Chapter 27.

![Entry physics. (a) Peak deceleration depends only on entry speed, flight-path angle and the atmosphere's scale height; the Galileo probe's measured 228 g matches this simple model. (b) The Galileo probe entered at four times the speed of a lunar return capsule.](figures/out/ch26_entry.svg){#fig:entry width=98%}

The heating rate at the stagnation point of an entry vehicle rises roughly as $\rho^{1/2} v^3$, so the Galileo probe's entry was far more severe than any Earth return, and much of its heating came as radiation from the extremely hot gas of the shock layer. For entries into Earth's atmosphere, see Chapters 31 and 29.

::: example
**Example: the Galileo probe's deceleration**

For a ballistic entry at speed $v_e$ and flight-path angle γ into an exponential atmosphere of scale height $H$, the peak deceleration (Allen and Eggers, 1958) is

$$a_{\max} = \frac{v_e^2 \sin\gamma}{2\,e\,H}.$$

For the Galileo probe, $v_e$ = 47.4 km/s, γ = 8.5° and $H$ ≈ 27 km in Jupiter's upper atmosphere:

$a_{\max}$ = (47 400)² × 0.148 / (2 × 2.718 × 27 000) = 2 260 m/s² ≈ 230 *g*,

within 1 % of the measured 228 *g*. Steeper entries give higher decelerations but shorter, less intense heat pulses; shallower entries risk skipping out of the atmosphere. Probe designers choose γ to keep both deceleration and total heat load within limits.
:::

New entry probes are planned but not yet secure. NASA's **DAVINCI** would descend through the atmosphere of Venus in the 2030s, and the US planetary science decadal survey (2022) chose a **Uranus Orbiter and Probe** as the highest-priority new flagship mission. In 2026, budget pressures left the timing of both uncertain.

## Impactors and Planetary Defence

### Deep Impact

Some questions can be answered only by hitting a target. NASA's **Deep Impact** released a 372 kg copper-rich impactor into the path of comet Tempel 1, which struck the nucleus at 10.2 km/s on 4 July 2005 (@fig:tempel). In its final two hours the impactor steered itself using **AutoNav**, an autonomous navigation system that tracked the brightest part of the nucleus. The flyby spacecraft, 500 km away, observed the plume of ejecta, which revealed that the nucleus is covered in fine dust as loose as talcum powder. In 2011, NASA's Stardust-NExT spacecraft flew past Tempel 1 and imaged the 150 m crater.

![The flash and ejecta of Deep Impact's collision with comet Tempel 1 on 4 July 2005, imaged by the flyby spacecraft 67 seconds after impact.](figures/photos/ch26_tempel.jpg){#fig:tempel width=46%}

### DART: Moving an Asteroid

Asteroid impacts are rare but potentially catastrophic: an object 140 m across, striking land, could devastate a whole metropolitan region, and the 10 km asteroid that ended the age of the dinosaurs released billions of times the energy of the Hiroshima bomb. The simplest way to deflect an asteroid that is discovered years before impact is a **kinetic impactor** — a spacecraft that strikes it to change its velocity slightly, so that years later it misses Earth.

NASA's **Double Asteroid Redirection Test (DART)** tested this idea on **Dimorphos**, a 150 m moon of the asteroid Didymos (@fig:dart, @fig:dartart). A binary asteroid was chosen because a change in the moon's 12-hour orbit around its primary could be measured from Earth within weeks, whereas a change in an asteroid's orbit around the Sun would take years to detect. DART struck Dimorphos at 6.1 km/s on 26 September 2022, steering itself during the last four hours with an autonomous navigation system (SMART Nav) that identified Dimorphos only an hour before impact. The Italian cubesat **LICIACube**, released 15 days earlier, flew past three minutes after the impact and imaged the ejecta plume.

![DART's impact on Dimorphos. (a) The Didymos system. (b) The orbit period shortened by 33 minutes, far more than DART's momentum alone could explain.](figures/out/ch26_dart.svg){#fig:dart width=98%}

![Artist's illustration of DART approaching the binary asteroid Didymos (left) and its moon Dimorphos.](figures/photos/ch26_dart.jpg){#fig:dartart width=72%}

Telescope observations showed that Dimorphos's orbital period had shortened by 33.0 ± 1.0 minutes, from 11 h 55 min — more than 25 times the mission's minimum success criterion of 73 seconds. More than a million kilograms of rock were thrown off, forming a tail thousands of kilometres long; the recoil from this ejecta pushed Dimorphos several times harder than the spacecraft did. The ratio of the total momentum change to the momentum DART delivered, the **momentum enhancement factor β**, is about 3.6 (between 2.2 and 4.9, depending on Dimorphos's unknown density). In 2026, stellar occultation and radar measurements showed that the impact had also changed the orbit of the whole Didymos system around the Sun, by about 12 micrometres per second.

::: example
**Example: how hard did DART push?**

Dimorphos orbits 1.19 km from the centre of Didymos with a period $T$ = 11.92 h, so its orbital speed is $v$ = 2π × 1 190 m / 42 900 s = 0.174 m/s.

1. For a nearly circular orbit, a small along-track velocity change Δ*v* changes the period by $\Delta T / T ≈ 3\,\Delta v / v$.
2. The measured Δ*T* = −33 min gives Δ*T*/*T* = −0.046, so Δ*v* ≈ 0.046 × 0.174 / 3 = 2.7 mm/s.
3. Dimorphos has a volume of about 1.8 × 10⁶ m³. For a density of 2 400 kg/m³, its mass is 4.3 × 10⁹ kg. DART's momentum (580 kg × 6 145 m/s) could change its velocity by at most 3.6 × 10⁶ / 4.3 × 10⁹ = 0.83 mm/s.
4. The observed 2.7 mm/s is more than three times larger: the ejecta, thrown backwards out of the crater, provided most of the push.

Because the result depends on Dimorphos's mass, ESA's Hera mission (arriving in November 2026) will measure it, along with the shape of the crater, so that future deflection missions can be designed with confidence.
:::

### Finding the Threats First

A deflection mission needs years of warning, so planetary defence begins with discovering near-Earth objects (NEOs). US law set the goal of finding 90 % of NEOs larger than 140 m; by 2026 well under half of them had been found. Ground surveys such as Catalina, Pan-STARRS, ATLAS and the Vera C. Rubin Observatory, which began its survey in 2025, will be joined by NASA's **NEO Surveyor**, an infrared telescope to be stationed at the Sun–Earth L1 point, with launch targeted for September 2027. The value of these surveys was shown by asteroid **2024 YR4**, about 60 m across, discovered in December 2024: in February 2025 its calculated chance of striking Earth in 2032 briefly reached 3 %, the highest ever recorded for an object of its size, before further observations ruled out an Earth impact (a small chance of hitting the Moon remains).

On 13 April 2029, the 340 m asteroid **Apophis** will pass about 32 000 km above Earth's surface — closer than geostationary satellites — and be visible to the naked eye. It will be studied by NASA's OSIRIS-APEX (the extended OSIRIS-REx spacecraft, Chapter 29) and by ESA's **Ramses**, approved in 2025 for launch in April 2028 on a Japanese H3 rocket, which will observe how Earth's gravity shakes and reshapes the asteroid. China plans its own impactor-and-observer test later in the decade.

## Comets, Asteroids and Interstellar Visitors

Flybys of small bodies have revealed their bewildering variety. Galileo's flyby of **Ida** in 1993 discovered **Dactyl**, the first known asteroid moon. **Deep Space 1** (1998–2001) tested ion propulsion and autonomous navigation and flew past comet Borrelly; **Stardust** collected dust from comet Wild 2 (Chapter 29); and Rosetta flew past the asteroids Šteins and Lutetia on its way to its comet.

NASA's **Lucy**, launched in October 2021, is touring the **Trojan asteroids** — primitive bodies sharing Jupiter's orbit at its L4 and L5 Lagrange points (Chapter 3). On its way it flew past the main-belt asteroid **Dinkinesh** in November 2023, discovering that it has a moon, Selam, which is itself a contact binary, and past **Donaldjohanson** in April 2025. Lucy will fly past the Trojans Eurybates and its moon Queta (August 2027), Polymele (September 2027), Leucus (April 2028) and Orus (November 2028), and finally the binary pair Patroclus–Menoetius in March 2033.

Three objects from outside the Solar System have been discovered passing through it: **ʻOumuamua** (2017), an elongated body that accelerated slightly as it left; the comet **2I/Borisov** (2019); and **3I/ATLAS**, discovered on 1 July 2025, which passed perihelion at 1.36 AU at the end of October 2025, moving at about 58 km/s relative to the Sun. When 3I/ATLAS was hidden behind the Sun as seen from Earth, spacecraft across the Solar System observed it: Mars orbiters as it passed Mars in early October 2025, the solar observatories SOHO and STEREO near perihelion, and later ESA's JUICE and NASA's SPHEREx, which found a coma rich in carbon dioxide and a strong increase in water after perihelion. ESA's **Comet Interceptor**, to be launched in 2028 or 2029, will wait at the Sun–Earth L2 point for a newly discovered comet — or interstellar object — and then intercept it with three spacecraft.

## Into Interstellar Space

The Sun blows a supersonic wind of charged particles, the solar wind, that carves a bubble in the interstellar medium — the **heliosphere** (Chapter 22). About 90 AU from the Sun the wind passes through a **termination shock**, where it slows abruptly; beyond it, in the **heliosheath**, the slowed, heated wind is deflected towards a long tail. The **heliopause** is the boundary where the solar wind meets the interstellar plasma (@fig:heliosphere).

![The heliosphere and the Voyagers' crossings of its boundaries (schematic, not to scale).](figures/out/ch26_heliosphere.svg){#fig:heliosphere width=94%}

Voyager 1 crossed the termination shock in December 2004 at 94 AU and the heliopause on 25 August 2012 at 121.6 AU, becoming the first human-made object in interstellar space. Voyager 2 followed in November 2018 at 119 AU. The crossings were identified by a sudden fall in solar-wind particles, a jump in galactic cosmic rays and — because Voyager 1's plasma instrument had failed decades earlier — by its plasma wave instrument, which detected the plasma's natural oscillation frequency and revealed a density about 40 times higher than in the heliosheath. Surprisingly, the direction of the magnetic field barely changed across the heliopause. The Voyagers now measure the interstellar medium directly, including the faint "hum" of plasma waves, and show that the Sun's influence extends well beyond the heliopause.

The **Pioneer anomaly** — a tiny unexplained sunward acceleration of Pioneers 10 and 11, about 8.7 × 10⁻¹⁰ m/s² — was once proposed as evidence of new physics. A careful analysis of recovered tracking data and a thermal model of the spacecraft showed in 2012 that it was caused by the uneven emission of heat from the RTGs and electronics, which acts as a minute thrust.

No spacecraft is yet on its way to explore the interstellar medium deliberately. Concept studies of an **Interstellar Probe**, launched in the 2030s with a super-heavy launcher and a close gravity assist from Jupiter, aim at speeds of about 7 AU per year — twice the Voyagers' — to reach several hundred AU within a working lifetime. Light-sail concepts that could reach other stars are discussed in Chapter 42.

## Probes in 2026

| Spacecraft | Status in October 2026 |
|---|---|
| Voyager 1 | 172 AU; one light-day from Earth on 18 November 2026; magnetometer and plasma wave instruments operating |
| Voyager 2 | About 144 AU, heading south; magnetometer, plasma wave and cosmic ray instruments operating early in 2026 |
| New Horizons | About 66 AU; Kuiper Belt and heliosphere observations; extended mission until it leaves the Kuiper Belt (≈ 2028–29) |
| Lucy | Cruising to the L4 Trojans; Eurybates flyby August 2027 |
| Psyche | Mars flyby May 2026; arrival at asteroid Psyche August 2029 |
| Europa Clipper | Earth flyby December 2026; Jupiter arrival April 2030 |
| JUICE | Earth flyby on 28 September 2026 added 3.5 km/s; one more Earth flyby (January 2029); Jupiter in July 2031 |
| Hera | Final approach; arrival at Didymos in November 2026 |
| BepiColombo | Mercury orbit insertion November 2026 (Chapter 25) |
| Parker Solar Probe | Closest solar passes at 6.1 million km and 192 km/s (Chapter 22) |
| In development | NEO Surveyor (2027), Ramses (2028), Comet Interceptor (2028–29), Dragonfly (2028, Chapter 28), Tianwen-4 to Jupiter and Uranus (≈ 2029–30) |

: Probes and flyby missions in 2026. {#tbl:probes2026}

::: ai
**Autonomy and AI on flyby missions**

Flybys and impacts happen too fast and too far away for ground control, so they were among the first uses of onboard autonomy. **AutoNav**, developed for Deep Space 1 (1999–2001), navigated by images of asteroids against the stars and steered Deep Impact's impactor into Tempel 1. DART's **SMART Nav** found Dimorphos in its camera images an hour before impact and guided the spacecraft into the centre of the 150 m target. Lucy uses an autonomous **terminal tracking** system that keeps an asteroid centred in its instruments' fields of view during the fastest part of each flyby. Machine-learning tools are now used on the ground to plan encounter sequences, to detect new moons, rings and plumes in flyby images, and to search survey data for near-Earth asteroids and interstellar objects (Chapter 46).
:::

::: key
**Key takeaways**

- Probes include flyby spacecraft, atmospheric entry probes, impactors and heliospheric explorers. Flybys are the cheapest way to reach a new world and remain our only close-up views of Uranus, Neptune, Pluto and the Kuiper Belt.
- Flyby engineering requires precise targeting in the B-plane, autonomous encounter sequences protected against faults, and imaging strategies that trade resolution against smear.
- Beyond Jupiter, probes rely on RTGs, whose output declines by a few watts each year; data rates fall with the square of distance, and Voyager 1 now returns 160 bit/s from 172 AU.
- Entry probes face extreme heating and deceleration — up to 228 g for the Galileo probe at Jupiter — that can be estimated from simple physics.
- DART showed that a kinetic impactor can change an asteroid's orbit: Dimorphos's period shortened by 33 minutes, with ejecta multiplying the push about 3.6 times. Hera arrives in November 2026 to measure the result.
- The Voyagers crossed the heliopause in 2012 and 2018 and are now sampling interstellar space; Voyager 1 reaches one light-day from Earth in November 2026.
:::
