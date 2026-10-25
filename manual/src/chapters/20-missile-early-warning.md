---
title: Missile Early Warning Satellites
hero: ch20
abstract: The fiery exhaust of a rocket is one of the brightest infrared sources on Earth. Since 1970, satellites watching for that signature have given the first warning of ballistic-missile launches anywhere in the world, underpinning nuclear deterrence and, increasingly, missile defence. This chapter explains, from public sources, how early-warning satellites work: the infrared physics of rocket plumes and the atmosphere, scanning and staring sensors, orbits that cover the globe and the poles, the processing that separates launches from sunlight and clouds, and the timelines of ballistic-missile flight. It traces the history from MIDAS and the Defense Support Program to SBIRS and Next-Generation OPIR, describes Russian, Chinese and European systems, and explains why hypersonic glide vehicles are driving a shift to proliferated low-orbit tracking constellations.
---

## Why Warning from Space?

A ballistic missile launched from one continent can reach another in about 30 minutes; a missile launched from a submarine near the coast can arrive in 10–15 minutes. Ground-based radars, limited by the curvature of the Earth, can see such missiles only after they rise above the horizon — typically several minutes into flight and thousands of kilometres from the launch point. A satellite high above the Earth, by contrast, can see a launch almost anywhere within seconds, because the rocket's exhaust plume is an intense source of infrared radiation.

Early-warning satellites therefore serve four purposes:

1. **Strategic warning**: detecting missile attacks on a nation's territory and confirming that an attack is real, a cornerstone of nuclear deterrence and crisis stability.
2. **Missile defence**: providing the earliest possible track of a missile to cue radars and interceptors, and increasingly providing tracks precise enough to guide interceptors directly.
3. **Battlespace awareness**: detecting and characterising other infrared events — tactical missile launches, explosions, aircraft afterburners, large fires.
4. **Technical intelligence**: measuring the performance of foreign missiles during tests.

The same satellites, together with sensors on GPS satellites, also detect nuclear detonations.

![The Defense Support Program satellite DSP Flight 16 on its Inertial Upper Stage in the payload bay of Space Shuttle Atlantis before deployment in November 1991. DSP satellites provided US missile warning for almost five decades.](figures/photos/ch20_dspbay.jpg){#fig:dspbay width=60%}

## History

The US **MIDAS** (Missile Defense Alarm System) programme launched twelve experimental satellites between 1960 and 1966 (@fig:ewhistory). Many failed, and early sensors were overwhelmed by false alarms from sunlight reflected by clouds, but MIDAS proved that rocket launches could be detected from orbit. Its successor, the **Defense Support Program (DSP)**, launched its first satellite in 1970; 23 DSP satellites were launched until 2007, and some operated for more than 20 years. DSP gained public fame in the 1991 Gulf War, when it detected Iraqi Scud launches and warned Coalition forces and Israel.

The Soviet Union developed the **Oko** system from the 1970s, using satellites in highly elliptical Molniya orbits. These viewed US missile fields obliquely, against the dark background of space near the Earth's limb, to avoid confusion with sunlit clouds. On 26 September 1983 an Oko satellite falsely reported the launch of several US missiles — sunlight reflected off high-altitude clouds had triggered the alarm. The duty officer, Lieutenant Colonel Stanislav Petrov, judged it to be a false alarm and did not pass it up the chain of command. This episode is often cited as an example of the dangers of automated warning systems and the importance of human judgement.

The US **Space-Based Infrared System (SBIRS)** replaced DSP: sensors hosted on classified satellites in highly elliptical orbits from 2006–2008, and six SBIRS GEO satellites launched between 2011 and 2022. Russia replaced Oko with the **EKS (Tundra/Kupol)** system from 2015, and China, France and others have developed their own capabilities.

![Milestones in space-based missile warning.](figures/out/ch20_history.svg){#fig:ewhistory width=100%}

## The Physics of Seeing Rockets

### Plume Emission

A rocket plume consists of hot combustion gases — mainly water vapour, carbon dioxide, carbon monoxide and, for solid-propellant motors, aluminium oxide particles — at temperatures of 1 500–3 000 K. Hot gases emit strongly in the vibrational bands of their molecules, especially near **2.7 µm** (H₂O and CO₂) and **4.3 µm** (CO₂), while hot particles emit a continuum like a grey body (@fig:plume). Where the plume mixes with the atmosphere, unburned fuel continues to burn ("afterburning"), increasing its size and brightness. A large booster plume radiates megawatts per steradian in the infrared.

![Schematic emission of a rocket plume compared with the transmission of the atmosphere. The strongest plume emission falls in molecular bands where the lower atmosphere is opaque.](figures/out/ch20_plume.svg){#fig:plume width=88%}

### The Atmosphere as a Filter

The atmosphere is opaque in the same bands where the plume is brightest, because the same molecules — water vapour and carbon dioxide — absorb there. This is the key to early-warning sensor design. Suppose a sensor looks at the Earth in a strong absorption band such as 2.7 µm. The radiation from the ground, clouds and sunlit surfaces is then absorbed before it reaches space, so the Earth appears dark and uniform. A rocket plume is invisible while it is low in the atmosphere. The absorbing layer extends a few kilometres up for the water-vapour band, and higher in the more strongly absorbing parts of the CO₂ band. Once the plume climbs above this layer, it suddenly appears as a bright point against a dark background (@fig:visibility). This **"above-the-horizon of absorption"** approach suppresses clutter from clouds and sun glints; sensors working in more transparent bands see launches earlier but must cope with a bright, structured background.

![Fraction of plume radiation escaping to space as a function of the plume's altitude in different spectral bands. In strongly absorbing bands, a plume becomes visible only after it climbs above the absorbing layer, but the background below is suppressed.](figures/out/ch20_visibility.svg){#fig:visibility width=82%}

### How Far Can Sensors See?

The irradiance at the sensor falls with the square of the distance (@fig:irdetect). A bright ICBM booster seen from geostationary orbit, 36 000–40 000 km away, delivers an irradiance far above the sensitivity of modern infrared sensors. Dimmer targets include short-range missiles, the hot bodies of re-entry vehicles after burnout, and hypersonic glide vehicles. These are much harder to see from GEO, and they favour sensors in lower orbits, which are 30–40 times closer.

![Irradiance from infrared sources of different intensity as a function of range, compared with an illustrative sensitivity range for space infrared sensors.](figures/out/ch20_detect.svg){#fig:irdetect width=86%}

## Sensors and Satellites

### Scanning and Staring

Two basic sensor architectures are used (@fig:scanstare):

- **Scanning sensors**, as on DSP, sweep a linear array of detectors across the scene. DSP satellites rotated about six times per minute. A telescope tilted slightly off the spin axis swept a line of several thousand lead-sulphide (and later also mercury-cadmium-telluride) detectors around the Earth's disc. Each point was revisited about every 10 seconds. Scanning is efficient with small detector arrays but cannot follow a fast event continuously.
- **Staring sensors**, made possible by large two-dimensional infrared focal-plane arrays, watch an area continuously, measuring the brightness of every pixel many times per second. They detect dimmer and shorter events and measure the time history of a plume precisely. SBIRS GEO combined a **scanning sensor** covering the whole Earth with a **staring sensor** that could be pointed at areas of interest; Next-Gen OPIR uses large staring arrays.

![Scanning (DSP) and staring (SBIRS, Next-Gen OPIR) sensor architectures.](figures/out/ch20_scanstare.svg){#fig:scanstare width=92%}

![A DSP satellite being prepared at Cape Canaveral in 1991 for launch on the Space Shuttle. The large telescope tube housing the infrared sensor projects from the spacecraft; the satellite spun around its axis to scan the Earth.](figures/photos/ch20_dsp.jpg){#fig:dsp width=44%}

### Detection and Clutter Rejection

Turning detector signals into reliable warnings is a demanding signal-processing problem. The background — sunlight reflected by clouds and water (sun glint), hot surfaces, fires, volcanoes, lightning and even high-altitude aircraft — produces vastly more "events" than missile launches. On-board and ground processing:

- estimate and subtract the slowly varying background in each pixel;
- detect pixels whose brightness rises above a threshold (constant-false-alarm-rate detection);
- associate detections in successive frames into **tracks** with consistent motion (@fig:clutter);
- compare the track's intensity history and multi-band "colour" with the signatures expected from missiles;
- fuse data from two or more satellites to compute the three-dimensional trajectory by stereo triangulation, estimate the launch point and predict the impact area.

Within a minute or two of launch, a missile-warning centre (for the USA, at Buckley Space Force Base in Colorado) can report the launch, the missile type and its predicted impact region.

![Simulated detection of a faint moving infrared source: invisible in a single frame against structured clutter, it emerges after background subtraction and is confirmed by tracking it over successive frames.](figures/out/ch20_clutter.png){#fig:clutter width=96%}

### Infrared Detectors

The heart of every early-warning sensor is its infrared **focal-plane array**: a two-dimensional array of photodetectors bonded to a silicon read-out integrated circuit that amplifies and digitises each pixel's signal. Detector materials are chosen for the spectral band (@fig:irdetectors):

- **Lead sulphide (PbS)**, used on early DSP sensors, responds to the 2.7 µm band at moderate cooling.
- **Indium antimonide (InSb)** covers 1–5.5 µm and must be cooled to about 77 K.
- **Mercury cadmium telluride (HgCdTe, "MCT")** can be tuned by its composition to cut off anywhere from about 1.7 to 14 µm; it is the workhorse for space infrared sensors, from SBIRS to astronomical telescopes.
- **Type-II strained-layer superlattices** and **nBn barrier detectors** are newer III–V semiconductor technologies that can operate at higher temperatures with lower dark current, easing cooling requirements.

Cooling is provided by passive radiators or mechanical cryocoolers (Chapter 5). Arrays with millions of pixels, read out hundreds of times per second, are now available — enabling wide-field staring sensors that were impossible in the DSP era. Radiation hardening is essential: energetic particles striking the array create false "spikes" that processing must reject, especially in highly elliptical orbits that pass through the radiation belts.

![Approximate spectral ranges and operating temperatures of infrared detector technologies.](figures/out/ch20_detectors.svg){#fig:irdetectors width=86%}

| Material | Spectral range | Operating temperature | Use in missile warning |
|---|---|---|---|
| PbS | 1–3 µm | ≈ 190–240 K | Early DSP sensors (2.7 µm band) |
| InSb | 1–5.5 µm | ≈ 77 K | MWIR sensors |
| HgCdTe | 1–14 µm (tunable) | ≈ 60–200 K | SBIRS, Next-Gen OPIR, LEO tracking sensors |
| Type-II superlattice / nBn | 3–12 µm | ≈ 80–160 K | Newer MWIR and LWIR sensors; higher operating temperature |
| QWIP | 7–11 µm | ≈ 40–70 K | LWIR (e.g. Landsat TIRS) — not typical for warning |

: Infrared detector materials. {#tbl:irdetectors}

### From Detection to Decision

Missile-warning data flow from the satellites through relay and ground stations to mission-control centres. There, data from several satellites are fused into tracks with estimated launch points and impact areas. The data then flow to warning and command centres (in North America, the North American Aerospace Defense Command, NORAD) and to missile-defence systems and allied forces (@fig:ewflow). The whole chain must be fast, highly reliable and protected against cyber attack and jamming. It is tested continuously with real launches, including the world's routine space launches, which look exactly like missile launches during boost.

![The missile-warning data chain from satellites to decision-makers.](figures/out/ch20_groundflow.svg){#fig:ewflow width=94%}

### Orbits

Geostationary satellites are the backbone of missile warning: three or four can watch almost the whole Earth between about 70° N and 70° S continuously. They see poorly at very high latitudes, however — exactly where the shortest routes for ICBMs between North America and Eurasia and many submarine patrol areas lie. Sensors in **highly elliptical orbits** (Molniya- or Tundra-type), which spend many hours near apogee over the Arctic, fill this gap (@fig:arctic). Russia's Oko and EKS systems rely mainly on such orbits; the USA has used sensors hosted on satellites in highly elliptical orbits since 2006 and plans dedicated Next-Gen OPIR Polar satellites.

![Coverage of the Arctic from geostationary orbit and from the apogee of a highly elliptical orbit (schematic).](figures/out/ch20_arctic.svg){#fig:arctic width=90%}

## Missile Flight and Warning Timelines

### Phases of Ballistic-Missile Flight

A ballistic missile's flight has three phases (@fig:bmtrajectories):

- **Boost**: the rocket engines burn for about 1–5 minutes, accelerating the payload to about 7 km/s for an intercontinental missile. This is when the plume is brightest and space-based infrared sensors see it best.
- **Midcourse**: after burnout, the warhead and any decoys coast above the atmosphere on an elliptical arc. For a minimum-energy ICBM trajectory over 10 000 km, they reach an apogee of about 1 000–1 300 km and take 20–25 minutes. Without a plume, the objects are cold and dim; they are tracked mainly by radars and by sensitive sensors observing their thermal emission against cold space.
- **Terminal**: re-entry vehicles plunge back through the atmosphere in the final minute or so.

Submarine-launched missiles can fly **depressed trajectories** — lower and faster — reducing warning time to about 10 minutes. These timelines (@fig:ewtimeline) leave national leaders only minutes to assess an attack, which is why fast, reliable warning from space is so important for crisis stability.

![Computed trajectories of an intercontinental ballistic missile and a depressed-trajectory submarine-launched missile, with a schematic hypersonic glide vehicle for comparison. The inset expands the first 2 500 km.](figures/out/ch20_trajectories.svg){#fig:bmtrajectories width=96%}

![Illustrative timeline of a ballistic-missile attack and its detection. Space-based infrared sensors provide the first warning within minutes, long before the missile rises above the radar horizon.](figures/out/ch20_warning.svg){#fig:ewtimeline width=96%}

| Phase | Duration (ICBM) | Main observables | Primary sensors |
|---|---|---|---|
| Boost | 1–5 min | Bright plume (2.7, 4.3 µm bands) | GEO and HEO infrared satellites; LEO tracking satellites |
| Post-boost / midcourse | 20–25 min | Warm warhead, decoys, debris against cold space | Ground- and sea-based radars; LEO infrared tracking with discrimination |
| Terminal | ≈ 1 min | Re-entry heating, radar signature | Terminal-defence radars |

: Phases of ballistic-missile flight and the sensors that observe them. {#tbl:ewphases}

### From Warning to Defence

Early-warning satellites provide the first **cue** to a missile-defence system. Their tracks tell ground-based radars, such as the US Upgraded Early Warning Radars and the Long Range Discrimination Radar in Alaska, where to look, and they initiate the engagement planning for interceptors. Modern missile-defence architectures increasingly aim for **fire-control-quality** tracks from space — precise enough to launch and guide an interceptor before ground radars can see the target — and for **discrimination** between warheads and decoys.

## Hypersonic Glide Vehicles and the Tracking Layer

**Hypersonic glide vehicles (HGVs)**, now deployed by Russia (Avangard) and China (DF-17), are boosted by rockets. They then glide through the upper atmosphere at 30–60 km altitude and speeds above Mach 5, manoeuvring over thousands of kilometres (@fig:bmtrajectories). They challenge existing warning systems in three ways. First, their low altitude keeps them below the horizon of ground radars until late. Second, their glide phase is much dimmer than a rocket plume, although the vehicle is heated by atmospheric friction. Third, their manoeuvres make their target uncertain.

Tracking HGVs requires sensors that are closer and that can follow dim, hot objects against the Earth background through their whole flight. This is the motivation for **proliferated low-Earth-orbit tracking constellations** (@fig:ewlayers):

- The US Space Development Agency's **Tracking Layer** (Chapter 19) carries wide-field-of-view infrared sensors on satellites at about 1 000 km; Tranche 1 includes 28 tracking satellites, with more in later tranches.
- The Missile Defense Agency's **Hypersonic and Ballistic Tracking Space Sensor (HBTSS)** — two prototypes launched in February 2024 — demonstrates medium-field-of-view sensors that can produce fire-control-quality tracks.
- The US Space Force is also deploying missile-warning and tracking satellites in **medium Earth orbit** ("Epoch 1"), for a layered architecture that is harder to defeat.

![The layered missile-warning and tracking architecture being built by the USA: geostationary and polar satellites for strategic warning, plus medium- and low-orbit constellations for resilience and tracking.](figures/out/ch20_layers.svg){#fig:ewlayers width=84%}

## Systems in Operation

| Country | System | Orbit | Status (2026) |
|---|---|---|---|
| USA | Defense Support Program (DSP) | GEO | 23 launched 1970–2007; last satellites retired or in reserve |
| USA | SBIRS GEO-1 to GEO-6 | GEO | Operational; launched 2011–2022 |
| USA | SBIRS HEO payloads | HEO (hosted) | Operational since 2006–2008; replacement payloads added |
| USA | Next-Gen OPIR GEO (2 satellites) | GEO | First satellite awaiting launch in late 2026 after delays |
| USA | Next-Gen OPIR Polar (2 satellites) | HEO | Planned ≈ 2028 |
| USA | SDA Tracking Layer; MDA HBTSS | LEO | Prototypes 2023–2024; Tranche 1 deploying from 2025–26 |
| USA | Resilient MW/MT ("Epoch 1") | MEO | First satellites planned from about 2026–27 |
| Russia | EKS "Kupol" (Tundra satellites) | HEO (Tundra) | About six satellites launched 2015–2022 |
| China | Early-warning satellites (TJS/Huoyan series, reported) | GEO | Operational (limited public information) |
| France / Europe | SPIRALE (demonstrators, 2009); TWISTER and ODIN'S EYE studies | LEO, GEO | European system under study |

: Space-based missile-warning systems (public information). {#tbl:ewsystems}

### SBIRS and Next-Gen OPIR

Each **SBIRS GEO** satellite, built by Lockheed Martin around the A2100 bus, weighs about 4 500 kg at launch. It carries a scanning sensor that covers a wide area continuously and a staring sensor that can be pointed at regions of interest. Both operate in several short- and mid-wave infrared bands. The ground segment processes data from SBIRS, the remaining DSP satellites and hosted sensors together.

The **Next-Generation Overhead Persistent Infrared (Next-Gen OPIR)** programme replaces SBIRS with two GEO satellites (Lockheed Martin, with sensor payloads from RTX and a Northrop Grumman–Ball team) and two polar satellites (Northrop Grumman). Its sensors are designed to be more sensitive to dimmer targets and more resistant to jamming and attack. Like many large defence programmes, it has suffered delays: the first GEO launch, originally planned for 2025, slipped into late 2026.

### Other Nations

Russia's **EKS** (Integrated Space System) uses Tundra satellites in highly elliptical orbits with a "Kupol" (dome) sensor, reportedly able to detect not only ICBM launches but also smaller missiles, and to relay combat commands. China is reported to operate early-warning satellites in GEO and has cooperated with Russia on missile-warning systems. France flew the two **SPIRALE** microsatellites in 2009 to measure infrared backgrounds for a future system. The European Union is funding studies (ODIN'S EYE) and the PESCO **TWISTER** project for a European space-based early-warning capability linked to interceptors.

## Beyond Missiles: Other Infrared Events

The same sensors see many other events. US officials have stated that space-based infrared sensors detected the missile that destroyed Malaysia Airlines flight MH17 over Ukraine in 2014. They have also stated that the sensors gave advance warning to troops in Iraq of the Iranian ballistic-missile attack in January 2020, allowing them to shelter. Large ballistic-missile attacks on Israel in 2024 and on Ukraine throughout the war were detected and tracked from space, cueing the defences. Researchers have also used declassified infrared data to study bolides — small asteroids exploding in the atmosphere — such as the Chelyabinsk event of 2013. US government sensors report such events publicly to NASA's Center for Near-Earth Object Studies.

![The plume of Starship's sixth flight test seen from the International Space Station on 19 November 2024. Rocket plumes are among the brightest infrared sources on Earth.](figures/photos/ch20_starship6.jpg){#fig:starship6 width=70%}

### Nuclear Detonation Detection

Nuclear explosions in the atmosphere or space produce a characteristic double-peaked flash of light, bursts of X-rays, gamma rays and neutrons, and an electromagnetic pulse. The **Vela** satellites (1963–1984) carried detectors for these signatures to verify the 1963 Limited Test Ban Treaty. Their successor, the **US Nuclear Detonation Detection System**, uses optical "bhangmeters", X-ray, gamma-ray, neutron and electromagnetic-pulse sensors carried on GPS and DSP/SBIRS satellites. Because GPS satellites are distributed around the Earth, at least four always see any point, allowing a detonation to be located by timing.

## Stability and Arms Control

Reliable early warning is stabilising. If leaders know they will receive unambiguous warning of an attack, they need not adopt hair-trigger postures. They are also less likely to mistake an accident or a space launch for an attack. Conversely, attacks on early-warning satellites could be extremely escalatory, since they might be interpreted as the prelude to a nuclear strike. The **Ballistic Missile Launch Notification Agreement** (1988) between the USA and the Soviet Union, and later agreements, require advance notice of certain launches. Plans for a joint US–Russian data-exchange centre, agreed in 1998, were never implemented. The growing use of the same satellites for both strategic warning and conventional missile defence — "entanglement" — is a subject of concern among arms-control experts.

::: example
**Example: warning time for an ICBM attack**

Using the computed trajectory of @fig:bmtrajectories (burnout at 7.0 km/s and 17° flight-path angle at 200 km altitude):

1. *Boost*: about 3 minutes; the plume becomes visible to a 2.7 µm sensor once it climbs above about 8–10 km, about 40–60 s after launch.
2. *Detection and assessment*: two or more satellites confirm the launch and compute an initial trajectory within about 1–2 minutes of the plume becoming visible.
3. *Flight*: the warhead coasts for about 29 minutes after burnout, reaching an apogee of about 1 040 km and impacting about 10 000 km from the launch site, 32 minutes after launch.
4. *Warning*: subtracting about 3 minutes for detection and reporting leaves roughly 25–28 minutes of warning. A ground-based radar 4 000 km from the target, by contrast, would see the warhead rise above its horizon only about halfway through its flight — giving about half as much warning.
:::

![The exhaust plumes of a Falcon 9 rocket illuminated by sunlight before dawn during the launch of the CRS-35 cargo mission on 13 October 2026, seen from Florida. Twilight launches show the vast extent of rocket plumes at high altitude.](figures/photos/ch20_crs35.jpg){#fig:crs35 width=62%}

::: ai
**AI in missile warning**

Machine learning helps reject clutter and false alarms, classify infrared events from their spectral and temporal signatures, fuse data from many satellites and radars into tracks, and discriminate warheads from decoys. Because errors could have grave consequences, these uses demand rigorous verification and human oversight (Chapters 50 and 53).
:::

::: key
**Key takeaways**

- Space-based infrared sensors detect ballistic-missile launches within about a minute, providing strategic warning and cueing missile defences.
- Rocket plumes emit strongly at 2.7 and 4.3 µm; sensors operating in these atmospheric absorption bands see a dark Earth background and a bright plume once it climbs above the absorbing layer.
- Scanning sensors (DSP) gave way to staring arrays (SBIRS, Next-Gen OPIR); processing rejects clutter from clouds, sun glint and fires and builds three-dimensional tracks from several satellites.
- GEO satellites provide global coverage to about 70° latitude; highly elliptical orbits cover the Arctic.
- ICBMs fly for about 30 minutes, submarine-launched missiles on depressed trajectories for about 10; space-based warning roughly doubles the warning time compared with ground radars alone.
- Hypersonic glide vehicles are driving a shift to proliferated LEO and MEO tracking constellations.
- Early-warning satellites also detect nuclear detonations, bolides and other infrared events; their reliability is central to strategic stability.
:::

::: questions
**Review questions**

1. Why do missile-warning sensors observe in the 2.7 µm and 4.3 µm absorption bands rather than in atmospheric windows?
2. What angle does the Earth subtend from geostationary orbit? How many 10 µrad pixels would a staring sensor need across that angle?
3. Compare scanning and staring infrared sensors for missile warning.
4. Describe three sources of clutter and how processing rejects them.
5. Why do early-warning constellations combine geostationary satellites with highly elliptical orbits?
6. Outline the phases of an ICBM's flight and how much warning space-based sensors provide in each case for land-based and submarine-launched missiles.
7. Why do hypersonic glide vehicles require a new tracking layer in LEO or MEO?
8. Why is the reliability of early-warning satellites important for strategic stability?
:::
