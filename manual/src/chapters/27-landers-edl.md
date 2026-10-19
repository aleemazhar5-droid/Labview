---
title: Landers and Entry, Descent & Landing
hero: ch27
abstract: Landing is the most dangerous minute of any planetary mission. A lander must shed kilometres per second of speed, find a safe spot it has never seen, and touch down gently enough to survive — all on its own, minutes or hours of light-time from Earth. This chapter explains how this is done on airless worlds like the Moon, on Mars with its treacherously thin atmosphere, in the crushing heat of Venus, under the haze of Titan and in the feeble gravity of comets and asteroids. It describes powered descent, heat shields, parachutes, airbags and sky cranes, terrain-relative navigation and hazard avoidance, the record of lunar landings from Luna 9 to the commercial landers of 2024–25, and what landers have discovered on the surface.
---

**Entry, descent and landing (EDL)** is the sequence of events that takes a spacecraft from its approach trajectory or orbit to a safe rest on a planetary surface. It is the phase in which most planetary missions have failed: of the 34 robotic attempts to land softly on the Moon up to 2025, 12 crashed and 4 more landed damaged or on their sides, and only a little over half of all attempts to land on Mars have succeeded. This chapter covers stationary **landers**; rovers, helicopters and balloons are described in Chapter 28, and the return of samples to Earth in Chapter 29.

## Why Land?

Orbiters map whole worlds, but some measurements can only be made by touching the surface (@tbl:landerscience). A lander can analyse the chemistry and mineralogy of rocks and soil in contact, listen for quakes with a seismometer, measure the flow of heat from the interior, record the weather day after day, search for organic molecules and signs of life, and collect samples for return to Earth. Landers also prove technologies needed for later crewed missions and for building permanent bases.

| Measurement | Instrument | Examples |
|---|---|---|
| Interior structure | Seismometer | Apollo passive seismic experiments (Moon, 1969–77); InSight SEIS (Mars, 2018–22) |
| Heat flow from the interior | Heat-flow probe | Apollo 15 and 17; InSight HP³; Blue Ghost LISTER (2025) |
| Surface chemistry and mineralogy | X-ray, gamma-ray and laser spectrometers, microscopes | Venera 13 (Venus); Phoenix and Perseverance (Mars); Chandrayaan-3 (Moon) |
| Volatiles and organics | Gas chromatograph–mass spectrometer, ovens | Viking (Mars); Phoenix; Philae (comet 67P) |
| Atmosphere and weather | Pressure, temperature, wind and dust sensors | Viking, InSight, Huygens (Titan) |
| Ground truth for orbital data | Cameras, spectrometers | Every lander |

: Science that requires a lander. {#tbl:landerscience}

## The Landing Problem

A spacecraft arriving at a planet carries an enormous amount of kinetic energy per kilogram. Coming down from a low lunar orbit at 1.7 km/s, each kilogram carries 1.4 MJ — as much as 30 g of TNT. Entering the Martian atmosphere at 5.4 km/s, it carries 15 MJ; returning to Earth from the Moon at 11 km/s, 60 MJ. All of this energy must be removed before touchdown, together with the potential energy of the altitude. There are only three ways to do it:

- **Aerodynamic drag** — heat shields and parachutes convert kinetic energy into heat in the atmosphere. This is free in terms of propellant but requires an atmosphere and protection from heating.
- **Propulsion** — rocket engines fired against the direction of motion. This works anywhere but is expensive: every metre per second costs propellant, and slowing down against gravity adds **gravity losses**.
- **Impact attenuation** — airbags, crushable structures or shock-absorbing legs absorb the last few metres per second at touchdown.

Every lander combines these in proportions set by its destination (@tbl:destinations).

| Destination | Surface gravity | Atmosphere | How landers slow down |
|---|---|---|---|
| Moon, Mercury | 1.6 / 3.7 m/s² | None | Entirely propulsive, from orbital speed |
| Mars | 3.7 m/s² | Thin (≈ 0.6 % of Earth's surface pressure) | Heat shield removes ≈ 90 % of speed; parachute; propulsion or airbags for the last 80–100 m/s |
| Venus | 8.9 m/s² | Very dense (92 bar at the surface) | Heat shield, parachute high up, then free fall: the dense air limits the landing speed to a few metres per second |
| Titan | 1.35 m/s² | Dense and extended (1.5 bar) | Heat shield and parachutes all the way to the surface |
| Asteroids, comets | 10⁻⁵–10⁻³ m/s² | None | Small thrusters; the challenge is to avoid bouncing off |

: Landing on different worlds. {#tbl:destinations}

## Landing on the Moon

### Powered Descent

With no atmosphere, a lunar lander must cancel its entire orbital velocity with its engines. The Apollo Lunar Module (LM) set the pattern still used today. It first lowered its orbit to a periapsis of about 15 km, 480 km before the landing site. At **powered descent initiation**, its throttleable descent engine fired against the direction of motion. During the **braking phase**, lasting about eight minutes, the engine removed most of the 1 690 m/s orbital speed while the lander gradually lost height. At the **pitch-over**, about 2 km up, the LM rotated to a more upright attitude so the crew — or, today, the cameras — could see the landing site. In the **approach phase** the site was checked and, if necessary, changed; and in the **terminal descent** the lander came straight down at a metre per second or so (@fig:lunardescent).

![Lunar powered descent. (a) A simulated Apollo-class descent from 15 km altitude. (b) Descent Δv versus the peak thrust-to-weight ratio: a weak engine must fight gravity for longer and wastes more propellant.](figures/out/ch27_lunardescent.svg){#fig:lunardescent width=98%}

If the lander could stop instantly, it would need a Δv equal to its orbital speed. In reality it must also hold itself up against gravity during the descent, and the total Δv is 1.8–2.1 km/s, including margins for hovering and diverting to a safer site. The higher the thrust-to-weight ratio, the shorter the burn and the smaller these **gravity losses** — but bigger engines are heavier and must be throttled deeply to hover.

::: example
**Example: propellant for a lunar descent**

An Apollo-class lander of 15 100 kg begins powered descent at 15 km. Its engine has a specific impulse of 311 s ($v_e$ = 3 050 m/s).

1. The guided descent of @fig:lunardescent needs Δv = 1 844 m/s to reach 150 m above the site. Adding about 200 m/s for the final descent, hovering and redesignation margin gives about 2 040 m/s.
2. Rocket equation: $m_p = m_0\,(1 - e^{-\Delta v / v_e})$ = 15 100 × (1 − e^{−2 040/3 050}) = 7 360 kg.
3. Nearly half the lander's mass is descent propellant. The real LM descent stage carried about 8 200 kg, the rest being reserve. Apollo 11 touched down with less than a minute of usable propellant left before the abort limit, after Neil Armstrong flew beyond a boulder field.
:::

### Navigation and Hazard Avoidance

A lander must know its altitude and velocity precisely. Apollo used a **landing radar** that measured altitude and, by the Doppler shift of four beams, velocity. Modern landers add **laser rangefinders** and **Doppler lidar** — NASA's Navigation Doppler Lidar measures velocity to a few centimetres per second — and cameras for **terrain-relative navigation (TRN)**, which matches images of craters and other landmarks with an onboard map to determine position to tens of metres.

The final hazard is the landing site itself: a boulder or a slope of more than 10–15° can tip a lander over. **Hazard detection and avoidance** systems image the terrain below with lidar or cameras during the last few hundred metres, build a map of slopes and rocks, and steer to a safe spot. China's Chang'e 3 lander hovered 100 m above the Moon in 2013 to choose its landing point, and every Chang'e lander since has done the same. Japan's **SLIM** (Smart Lander for Investigating Moon) demonstrated vision-based "pinpoint" landing in January 2024, touching down about 55 m from its target, within its 100 m goal — even though one of its two main engines lost a nozzle about 50 m above the surface and the lander came to rest on its nose.

### Touchdown

Landing legs must absorb the remaining vertical speed, typically 1–3 m/s, and keep the lander upright on slopes and rocks. Apollo's legs contained **crushable aluminium honeycomb** cartridges that absorbed energy by deforming permanently (@fig:aldrin). A lander tips over when its centre of gravity (CG) passes outside the line joining its downhill feet. On level ground, the static limit is the angle whose tangent is the footprint radius divided by the CG height; but a sideways velocity at touchdown makes the lander rotate about its downhill feet, and a tall, narrow lander can be tipped by less than 1 m/s of lateral speed on a modest slope (@fig:tipover). Both Intuitive Machines landers to date (2024 and 2025) — tall vehicles 4.3 m high — ended on their sides.

![Apollo 11's Buzz Aldrin beside a leg of the Lunar Module Eagle in July 1969. The footpad and the crushable struts above it absorbed the landing shock.](figures/photos/ch27_aldrin.jpg){#fig:aldrin width=56%}

![Tip-over stability. (a) A low, wide lander tolerates much steeper slopes than a tall, narrow one. (b) The lateral speed at touchdown that would tip each lander over, as a function of slope.](figures/out/ch27_tipover.svg){#fig:tipover width=96%}

The engine exhaust also interacts with the surface. Plumes blast away dust and rocks at high speed, erode shallow craters and can damage nearby hardware: when Apollo 12 landed about 160 m from the robotic Surveyor 3 lander in 1969, the astronauts found Surveyor's surfaces sandblasted by the LM's plume (@fig:surveyor). Plume–surface interaction is a major concern for the large Artemis landers and for future lunar bases.

![Apollo 12's Pete Conrad inspects Surveyor 3, which had landed 31 months earlier; the Lunar Module Intrepid stands on the horizon. Parts brought back to Earth showed sandblasting by the LM's plume.](figures/photos/ch27_surveyor.jpg){#fig:surveyor width=60%}

### Sixty Years of Lunar Landings

The Soviet **Luna 9** made the first soft landing on another world in February 1966, using an inflated airbag-like ball ejected just before impact; NASA's **Surveyor 1** followed four months later with a fully propulsive landing. Between 1966 and 1976, five of seven Surveyors and seven Soviet Luna landers succeeded, including three sample-return missions and two Lunokhod rovers, and six Apollo crews landed. Then, for 37 years, no spacecraft landed on the Moon — until China's **Chang'e 3** in 2013 (@fig:lunarattempts).

![Robotic lunar soft-landing attempts by year and outcome.](figures/out/ch27_lunarattempts.svg){#fig:lunarattempts width=100%}

The 2010s and 2020s opened the Moon to new nations and to private companies. China has landed four times without failure, including the first landings on the far side (Chang'e 4, 2019) and the first far-side sample return (Chang'e 6, 2024). India's **Chandrayaan-3** became the first lander near the south pole region, at 69° S, in August 2023. Through NASA's **Commercial Lunar Payload Services (CLPS)**, companies now deliver NASA instruments under fixed-price contracts; Firefly's **Blue Ghost Mission 1** became the first fully successful commercial landing on 2 March 2025 in Mare Crisium, operating for a full lunar day of 14 Earth days.

The failures are equally instructive (@tbl:lunarfailures). Most were caused not by hardware breaking but by **navigation and software**: sensors that were not enabled, data rejected as faulty, or unexpected terrain that confused altitude estimates.

| Mission | Date | What happened | Lesson |
|---|---|---|---|
| Beresheet (SpaceIL) | Apr 2019 | An inertial measurement unit fault led to a computer reset that shut down the main engine during descent | Fault responses must not remove thrust during descent |
| Vikram (ISRO) | Sep 2019 | Higher-than-expected thrust in the braking phase; the guidance could not recover | Robust guidance margins; Chandrayaan-3 widened them and succeeded |
| Hakuto-R M1 (ispace) | Apr 2023 | Passing over a crater rim, the altitude estimate jumped; software rejected correct radar data, and the lander ran out of propellant 5 km up | Test navigation with realistic terrain |
| Luna 25 (Roscosmos) | Aug 2023 | An orbit-lowering burn lasted 127 s instead of 84 s; the lander crashed | Independent burn-cutoff protection |
| SLIM (JAXA) | Jan 2024 | Nozzle lost 50 m up; landed on its nose but operated | Precision landing works; design for off-nominal touchdown |
| IM-1 Odysseus (Intuitive Machines) | Feb 2024 | Laser rangefinders unusable because a safety switch was not enabled before launch; the team switched to a NASA lidar experiment; a leg caught at touchdown and the lander tipped | Pre-launch checks; end-to-end sensor testing |
| IM-2 Athena (Intuitive Machines) | Mar 2025 | Altimeter data degraded over dark polar terrain; landed on its side in a crater | Sensors for low-Sun polar lighting |
| Resilience (ispace) | Jun 2025 | Laser rangefinder measurements came late; the lander could not slow down in time | Sensor qualification for the descent environment |

: Lessons from recent lunar landing failures and anomalies. {#tbl:lunarfailures}

In 2026, no lunar landing had been attempted by October: Astrobotic's Griffin-1 was due to launch no earlier than November, while Blue Origin's Blue Moon MK1, Intuitive Machines' IM-3, Firefly's far-side Blue Ghost Mission 2 and China's Chang'e 7 (which missed its August 2026 launch window) were all expected in 2027.

## Entry, Descent and Landing at Mars

### The Thin-Atmosphere Problem

Mars is the hardest place to land in the inner Solar System. Its atmosphere is thick enough to heat an entering spacecraft to well over 1 000 °C, but so thin — less than 1 % of Earth's surface pressure — that a heat shield and parachute alone cannot slow a spacecraft to a safe landing speed. Under the same parachute, a spacecraft descends about five times faster on Mars than it would on Earth, and the parachute must open at supersonic speed. Each Mars lander therefore uses a chain of devices, each taking over when the previous one has done all it can: the famous **"seven minutes of terror"** (@fig:marsedl).

![Entry, descent and landing at Mars, simulated for a Perseverance-class spacecraft. (a) Altitude and speed with the main events. (b) Deceleration: the heat shield removes about 90 % of the speed in the first two minutes.](figures/out/ch27_marsedl.svg){#fig:marsedl width=98%}

### The EDL Sequence

The sequence flown by NASA's Perseverance rover on 18 February 2021 illustrates the state of the art:

1. **Cruise-stage separation and entry.** Ten minutes before entry, the cruise stage that carried the spacecraft from Earth is jettisoned. The 4.5 m aeroshell enters the atmosphere at about 125 km altitude at 5.4 km/s.
2. **Guided entry.** The capsule flies at an angle of attack that gives it a little lift (lift-to-drag ratio about 0.24). By rolling to point this lift up, down or sideways with small thrusters, the onboard guidance corrects for variations in the atmosphere and steers towards the target, like the Apollo capsules returning to Earth. Peak heating and a deceleration of about 10 *g* occur about 80 seconds after entry; the heat shield's surface reaches about 1 300 °C.
3. **Parachute.** About four minutes after entry, at 9–11 km altitude and close to Mach 1.7, a 21.5 m disk-gap-band parachute is fired out by a mortar. Perseverance used a **range trigger**, opening the parachute when its position estimate showed it was the right distance from the target, rather than at a fixed speed.
4. **Heat-shield separation.** Twenty seconds later the heat shield is released, exposing the radar and cameras.
5. **Terrain-relative navigation.** From about 4 km altitude, Perseverance's **Lander Vision System** photographed the ground, matched the images with an onboard map made from orbital images, and computed its position to within about 40 m. It then chose the safest reachable spot from a pre-loaded hazard map.
6. **Back-shell separation and powered descent.** At about 2.1 km altitude and 90 m/s, the descent stage with the rover beneath it drops away from the back shell and parachute, and eight throttleable engines take over (@fig:pdv).
7. **Sky crane.** About 20 m above the surface, the descent stage lowers the rover on three nylon bridles 6.4 m long. When the rover's wheels touch down at 0.75 m/s, the bridles are cut and the descent stage flies away to crash at a safe distance (@fig:skycrane).

The whole sequence is autonomous: with 11 minutes of light-time, the landing was already over when the first signal of entry reached Earth.

![Perseverance's powered descent vehicle (descent stage, top, with the rover beneath) being stacked at Kennedy Space Center in 2020.](figures/photos/ch27_pdv.jpg){#fig:pdv width=80%}

::: figrow
![Perseverance under its parachute, photographed from orbit by MRO's HiRISE camera during the descent on 18 February 2021.](figures/photos/ch27_hirisedesc.jpg){#fig:hirisedesc}

![The sky crane manoeuvre, seen from the descent stage: Perseverance hangs on its bridles a few metres above the surface.](figures/photos/ch27_skycrane.jpg){#fig:skycrane}
:::

::: example
**Example: why a Mars parachute is not enough**

A 3 000 kg spacecraft hangs under a 21.5 m parachute with drag coefficient 0.6 (drag area $C_D A$ = 218 m²). At terminal velocity, drag equals weight: $v_t = \sqrt{2 m g / (\rho C_D A)}$.

- **Mars**, 2 km above the surface: ρ ≈ 0.017 kg/m³, $g$ = 3.71 m/s²: $v_t = \sqrt{2 × 3\,000 × 3.71 / (0.017 × 218)}$ ≈ **78 m/s** (280 km/h).
- **Earth**, at the same altitude: ρ ≈ 1.0 kg/m³, $g$ = 9.81 m/s²: $v_t$ ≈ **16 m/s**.

Even a parachute of 50 m diameter would leave the spacecraft falling at about 30 m/s on Mars. The final 80–100 m/s must be removed by rockets — or the impact must be absorbed by airbags, as Mars Pathfinder and the Mars Exploration Rovers did, bouncing up to 15 m high before rolling to a stop.
:::

### Landing Architectures

| Mission | Year | Final landing system | Notes |
|---|---|---|---|
| Viking 1 and 2 (USA) | 1976 | Throttled rockets and three legs | Biology experiments; operated until 1980 and 1982 |
| Mars Pathfinder (USA) | 1997 | Airbags | Carried the first Mars rover, Sojourner |
| Spirit and Opportunity (USA) | 2004 | Airbags | Opportunity operated for 14 years |
| Phoenix (USA) | 2008 | Pulsed rockets and legs | Arctic plains, 68° N; dug into ground ice |
| Curiosity (USA) | 2012 | Sky crane | First guided lifting entry at Mars; 899 kg rover |
| Schiaparelli (ESA) | 2016 | Crushable structure | Failed: navigation error, see below |
| InSight (USA) | 2018 | Pulsed rockets and legs | Seismometer and heat-flow probe |
| Perseverance (USA) | 2021 | Sky crane | First terrain-relative navigation at Mars; 1 025 kg rover |
| Tianwen-1 / Zhurong (China) | 2021 | Rockets and legs, with hover and hazard avoidance | First successful landing on Mars at the first attempt by a new nation |

: Successful and attempted Mars landing systems (selected). {#tbl:marslanders}

Airbags are simple and tolerant of rocks and slopes but limited to landed masses of a few hundred kilograms. Legged landers, as on Phoenix and InSight, can carry heavier instruments but need flat, rock-free sites. The **sky crane**, introduced for the 899 kg Curiosity, keeps the rocket engines high above the surface, avoiding dust and craters, and puts the rover directly on its wheels, ready to drive. Landing heavier payloads — such as the tonnes of cargo needed for human missions — will require new techniques, such as inflatable heat shields and **supersonic retropropulsion**, in which rocket engines are fired into the oncoming supersonic flow; SpaceX's Falcon 9 first stages use this technique when returning through Earth's upper atmosphere, and Starship is designed to land on Mars the same way.

### Shrinking the Landing Ellipse

Because the atmosphere and the spacecraft's approach are never known exactly, a lander can only be targeted to land somewhere within a **landing ellipse**, and every point inside it must be safe. Better approach navigation, guided entry, the range trigger and terrain-relative navigation have shrunk Mars landing ellipses about 400 times in area in 25 years (@fig:ellipses), opening scientifically rich but rugged sites such as Perseverance's Jezero crater, an ancient river delta.

![Mars landing ellipses. Smaller ellipses allow landings in complex, scientifically interesting terrain.](figures/out/ch27_ellipses.svg){#fig:ellipses width=96%}

### Failures at Mars

The Soviet **Mars 3** made the first soft landing on Mars in December 1971 but fell silent after about 20 seconds, possibly because of a dust storm. NASA's **Mars Polar Lander** was lost in 1999, almost certainly because the jolt of its legs deploying was misread by software as touchdown, shutting off the engines 40 m above the ground. Britain's **Beagle 2** landed in 2003 but was not heard from; in 2015 HiRISE images showed it on the surface with its solar panels only partly unfolded, blocking its antenna. ESA's **Schiaparelli** test lander crashed in October 2016 when its inertial measurement unit briefly saturated during parachute descent; the navigation software then calculated a negative altitude, released the parachute and fired the braking thrusters for only three seconds while the lander was still 3.7 km up.

### What Mars Landers Found

The two **Viking** landers of 1976 returned the first images from the surface (@fig:viking) and ran three biology experiments whose results — chemically active soil but no organic molecules — are still debated; the later discovery of perchlorates in the soil by **Phoenix** suggests that heating during the analysis destroyed any organics. Phoenix scraped through the soil at 68° N and found water ice a few centimetres down (@fig:phoenixice).

![The first photograph taken by Viking Lander 2 at Utopia Planitia in September 1976, showing rocks and part of the lander's footpad (lower right).](figures/photos/ch27_viking.jpg){#fig:viking width=96%}

![Phoenix's "Dodo-Goldilocks" trench in June 2008. Lumps of bright material in the lower left (top image) had vanished four days later (bottom), proving that they were water ice that sublimated.](figures/photos/ch27_phoenix.jpg){#fig:phoenixice width=34%}

NASA's **InSight** (2018–2022) placed a seismometer on the Martian surface with its robotic arm (@fig:seis) and recorded 1 319 marsquakes, including one of magnitude 4.7 in May 2022 and the shaking from meteorite impacts whose fresh craters were then found by orbiters. Seismic waves passing through the planet revealed its internal structure (@fig:marsinterior): a crust 24–72 km thick, a large liquid iron-rich core surrounded by a layer of molten rock and, according to a study published in 2025, possibly a solid inner core. InSight's heat-flow probe, a self-hammering "mole", could not penetrate the unexpectedly cohesive soil. Dust slowly covered the solar panels (see the chapter-opening image) and the mission ended in December 2022.

![InSight's robotic arm placing the SEIS seismometer on the surface of Mars in December 2018.](figures/photos/ch27_seis.jpg){#fig:seis width=50%}

![The interior of Mars revealed by InSight's seismometer.](figures/out/ch27_marsinterior.svg){#fig:marsinterior width=86%}

## Venus, Titan and Small Bodies

### Venus: Landing in an Oven

The surface of Venus is at 465 °C and 92 bar — the pressure 900 m deep in Earth's oceans — under clouds of sulphuric acid. The Soviet Union nevertheless landed ten spacecraft there between 1970 and 1985. **Venera 7** (1970) transmitted for 23 minutes from the surface, the first data ever received from the surface of another planet; **Venera 9** (1975) returned the first pictures; and **Venera 13** (1982) returned colour panoramas, drilled a sample and analysed it with an X-ray fluorescence spectrometer, surviving for 127 minutes.

Venus landers are built like deep-sea submersibles: a spherical titanium pressure vessel, thick insulation, and a heat sink of lithium nitrate or similar phase-change material, with the electronics pre-chilled before entry. They are doomed from the moment they land, and the race is to return data before the interior overheats. Because the atmosphere is so dense, the parachute is released at about 50 km altitude and the lander falls the rest of the way with only a drag plate, reaching the surface at about 8 m/s. New electronics based on silicon carbide, which NASA operated for 60 days in a Venus simulation chamber in 2021, may one day allow long-lived Venus landers.

### Titan: Huygens

ESA's **Huygens** probe, carried to Saturn by Cassini, entered Titan's atmosphere on 14 January 2005. Titan's dense, extended atmosphere and low gravity made the landing gentle: Huygens descended under parachutes for 2 hours 27 minutes, imaging river channels and shorelines below, and landed at about 4.5 m/s on damp ground strewn with rounded pebbles of water ice (@fig:huygens). It recorded a surface temperature of −179 °C and a pressure of 1.5 bar, and transmitted from the surface for 72 minutes until Cassini set below the horizon — still the most distant landing ever made. NASA's Dragonfly rotorcraft will return to Titan in 2034 (Chapter 28).

![The surface of Titan photographed by Huygens after landing in 2005. The "pebbles" in the foreground, 10–15 cm across, are made of water ice.](figures/photos/ch27_huygens.jpg){#fig:huygens width=38%}

### Comets and Asteroids: Avoiding the Bounce

Landing on a small body is the opposite problem: gravity is so weak — the escape speed from the 900 m asteroid Ryugu is about 0.37 m/s, a slow walking pace — that a lander risks bouncing back into space. NASA's **NEAR Shoemaker** orbiter, not designed as a lander, touched down on Eros at the end of its mission in 2001 and kept operating for two weeks. ESA's **Philae** landed on comet 67P/Churyumov–Gerasimenko on 12 November 2014, but its harpoons failed to fire and its hold-down thruster did not work; it bounced about a kilometre high and came to rest two hours later in the shadow of a cliff, where it operated on its batteries for about 64 hours before falling silent. JAXA's Hayabusa2 deployed the first hopping rovers, **MINERVA-II-1A and 1B**, and the German–French **MASCOT** lander on Ryugu in 2018; sample-collecting "touch-and-go" landings are described in Chapter 29.

::: example
**Example: how slowly must you land on a comet?**

Comet 67P has a mass of about 1.0 × 10¹³ kg and an effective radius of about 2 km.

1. Escape speed: $v_{esc} = \sqrt{2GM/r} = \sqrt{2 × 6.67 × 10^{-11} × 10^{13} / 2\,000}$ = 0.82 m/s.
2. Philae touched down at about 1 m/s. Without anchoring, any rebound faster than 0.82 m/s would have escaped the comet entirely; Philae's damping legs absorbed most of the energy, and it rebounded at about 0.4 m/s — slow enough to fall back, but only after a two-hour flight.
3. Surface gravity is about $GM/r^2$ = 1.7 × 10⁻⁴ m/s², so the 100 kg Philae weighed only about 0.02 N — the weight of a 2 g object on Earth. This is why it carried harpoons, ice screws and a thruster to press it down: without them, almost any disturbance could launch it back into space.
:::

## Surviving on the Surface

Landing is only the beginning. A lander must then survive the local environment:

- **Night and cold.** A lunar night lasts 14 Earth days, and the surface cools to about −170 °C. Solar-powered landers usually die at sunset unless they carry radioisotope heater units, as China's Chang'e 3 and 4 landers do; SLIM, not designed to survive, revived after three lunar nights before failing in 2024. Martian nights reach −90 °C, and winter is the end of most solar-powered polar landers, as it was for Phoenix.
- **Dust.** Lunar dust is sharp and electrostatically charged, sticking to radiators, seals and optics; Martian dust settles on solar panels, steadily reducing power, as it ended InSight's mission.
- **Communications.** A lander on the Moon's near side can talk directly to Earth, but one on the far side, which never faces Earth, needs a relay satellite such as China's Queqiao and Queqiao-2. Mars landers relay most of their data through orbiters (Chapter 25).

::: ai
**AI and autonomy for landing**

Landing is the most autonomous phase of any mission, and modern landers rely on computer vision. Terrain-relative navigation systems detect craters or match image patches with onboard maps; hazard-detection systems turn lidar or stereo images into maps of slope and roughness and select a safe spot within seconds; and SLIM's vision-based navigation demonstrated 100 m landing accuracy. On the ground, deep-learning models trained on orbital images detect boulders and craters to map hazards at candidate landing sites — for the Artemis south-pole sites, they have catalogued millions of boulders from LRO images. Future landers will combine these into fully autonomous "land anywhere" systems (Chapters 45 and 46).
:::

::: key
**Key takeaways**

- Landing removes huge kinetic energy — 1.4 MJ/kg from lunar orbit, 15 MJ/kg at Mars entry — using drag, propulsion and impact attenuation in proportions set by the destination.
- Airless bodies require fully propulsive descent; gravity losses add 10–20 % to the Δv, and the final phase depends on accurate altimetry, terrain-relative navigation and hazard avoidance.
- Tall, narrow landers are vulnerable to tipping over; most recent lunar failures and anomalies were caused by navigation sensors and software rather than hardware breakdowns.
- Mars's thin atmosphere requires a chain of heat shield, supersonic parachute and propulsive or airbag landing; guided entry and terrain-relative navigation have shrunk landing ellipses 400-fold.
- Venus landers survive for hours at 465 °C and 92 bar; Huygens landed on Titan under parachutes; small-body landers must avoid bouncing off in micro-gravity.
- Landers have revealed Mars's interior, water ice at its high latitudes and the surfaces of Venus and Titan; in 2026 a new wave of commercial and national lunar landers was preparing for 2027.
:::

::: questions
**Review questions**

1. Calculate the specific kinetic energy that must be removed when landing from lunar orbit (1.68 km/s) and at Mars entry (5.5 km/s).
2. A lunar lander needs a Δv of 2.0 km/s with engines of 320 s specific impulse. What fraction of its initial mass must be propellant?
3. Why do airless bodies require fully propulsive descent, and why do gravity losses add 10–20 % to the Δv?
4. Why have recent commercial lunar landers tipped over? What design and navigation lessons follow?
5. Describe the Mars EDL sequence from entry to touchdown for a sky-crane landing.
6. How have guided entry and terrain-relative navigation reduced the size of Mars landing ellipses?
7. How did the Venera landers survive on the surface of Venus, and for how long?
8. Why is landing on a comet or small asteroid difficult? What happened to Philae?
:::
