---
title: Planetary Rovers and Aerial Explorers
hero: ch28
abstract: A lander sees one spot; a rover can follow the clues. Since Lunokhod 1 rolled onto the Moon in 1970, rovers have crossed tens of kilometres of the Moon and Mars, climbed mountains, drilled rocks, cached samples for return to Earth and found the strongest evidence yet that Mars was once habitable. In 2021 a 1.8 kg helicopter made the first powered flight on another planet, and a nuclear-powered rotorcraft is being built to fly through the dense air of Titan. This chapter explains how rovers move over soft ground, stay warm and powered, navigate by themselves, and carry laboratories across other worlds; it reviews every rover mission to date and those planned for the next decade.
---

A **rover** is a mobile laboratory. Mobility lets one mission visit many sites, follow geological layers like the pages of a book, and reach targets first spotted from orbit. The price is complexity: a rover must cross unknown terrain, mostly on its own, with its power, temperature and communications all depending on where it stops. This chapter describes robotic rovers on the Moon and Mars, the vehicles that carried Apollo astronauts, and the newest class of explorer — aircraft that fly in other worlds' atmospheres.

## Sixty Years of Rovers

### The First Rovers: Lunokhod and the Apollo Lunar Roving Vehicle

The first rover on another world was the Soviet **Lunokhod 1**, landed by Luna 17 on 17 November 1970. The 756 kg, eight-wheeled vehicle was driven from Earth by a five-person crew who watched slow-scan television pictures arriving with a delay of several seconds; a polonium-210 heater kept it alive through the lunar nights. It operated for 11 lunar days and drove 10.5 km. **Lunokhod 2** (1973) drove 39 km in four months — the distance record for 41 years. Their landing sites have been photographed by NASA's Lunar Reconnaissance Orbiter (@fig:lunokhod).

![The Lunokhod 2 rover (arrow), as seen by NASA's Lunar Reconnaissance Orbiter, at the end of its tracks in the crater Le Monnier, where it stopped in 1973.](figures/photos/ch28_lunokhod.jpg){#fig:lunokhod width=50%}

The last three Apollo missions (1971–72) carried the **Lunar Roving Vehicle (LRV)**, a 210 kg, battery-powered, four-wheel-drive car that folded into the side of the Lunar Module. With wire-mesh wheels and a top speed of about 13 km/h, the LRVs carried astronauts and their samples a combined 90 km and let them explore up to 7.6 km from the lander (@fig:lrv).

![Apollo 15's Jim Irwin with the first Lunar Roving Vehicle at Hadley–Apennine in July 1971. Mount Hadley rises in the background.](figures/photos/ch28_lrv.jpg){#fig:lrv width=60%}

### Mars Rovers

NASA's rovers have grown with each generation (@fig:rovers3):

- **Sojourner** (1997), a 10.6 kg, solar-powered microrover carried by Mars Pathfinder, explored the rocks around the lander for 83 sols (Martian days) and travelled about 100 m.
- **Spirit and Opportunity** (2004), 185 kg each, were designed for 90 sols and 600 m of driving. Opportunity found layered rocks and spherules of hematite ("blueberries") formed in acidic groundwater, and operated for 14 years until a planet-wide dust storm in 2018 cut its power; its 45.16 km is still the record for distance driven on another world. Spirit found almost pure silica deposited by ancient hot springs before it became stuck in soft soil in 2009.
- **Curiosity** (2012), 899 kg and powered by a radioisotope generator, landed in Gale crater and showed that it once held a long-lived lake whose water could have supported microbes. It has found organic molecules preserved in mudstones and seasonal changes in atmospheric methane, and has climbed more than 1.3 km up the layered Mount Sharp, driving more than 37 km by 2026.
- **Perseverance** (2021), 1 025 kg, explores Jezero crater, which contained a lake fed by a river delta 3.5 billion years ago. It is the first rover to **collect and seal samples for return to Earth**; by early 2026 it had filled 33 of its 43 sample tubes, left ten of them in a depot on the crater floor in 2022–23, climbed out over the crater rim and driven more than 42 km. Its MOXIE experiment made 122 g of oxygen from the Martian carbon dioxide atmosphere.

![Three generations of NASA Mars rovers at JPL: a flight spare of Sojourner (front), a Mars Exploration Rover test vehicle (left) and a Curiosity test rover (right).](figures/photos/ch28_rovers3.jpg){#fig:rovers3 width=70%}

China's **Zhurong** rover (240 kg), landed by Tianwen-1 in May 2021 in Utopia Planitia, drove 1.9 km and found evidence of water-altered minerals and buried layers with its ground-penetrating radar before it entered hibernation in May 2022 under a coating of dust and did not wake.

### Rovers on the Moon Since 2013

China's **Yutu** (2013) drove 114 m before its mobility failed. **Yutu-2**, landed by Chang'e 4 on the far side in January 2019, became the longest-lived lunar rover; its ground-penetrating radar mapped layers of debris tens of metres deep, and it was still active, though nearly immobile, in 2025 after driving about 1.6 km. India's 26 kg **Pragyan**, carried by Chandrayaan-3 (2023), confirmed sulphur in the south polar regolith with its laser-induced breakdown spectrometer before going to sleep at the end of the lunar day. Japan's SLIM carried two tiny rovers in 2024: LEV-1, a hopping rover, and LEV-2 (SORA-Q), a 250 g sphere that unfolded into a two-wheeled rover and photographed SLIM lying on its nose. The UAE's first rover, **Rashid**, was lost when the Hakuto-R lander crashed in 2023.

| Rover | Operator | Body | Years | Mass | Power | Distance |
|---|---|---|---|---|---|---|
| Lunokhod 1, 2 | USSR | Moon | 1970–71, 1973 | 756 kg, 836 kg | Solar; Po-210 heater | 10.5 km, 39 km |
| Lunar Roving Vehicle (×3) | NASA | Moon | 1971–72 | 210 kg | Batteries | 90 km in total |
| Sojourner | NASA | Mars | 1997 | 10.6 kg | Solar | ≈ 0.1 km |
| Spirit, Opportunity | NASA | Mars | 2004–10, 2004–18 | 185 kg | Solar | 7.7 km, 45.2 km |
| Curiosity | NASA | Mars | 2012– | 899 kg | MMRTG | > 37 km |
| Yutu, Yutu-2 | CNSA | Moon | 2013–16, 2019– | 140 kg | Solar, radioisotope heaters | 0.1 km, 1.6 km |
| Perseverance | NASA | Mars | 2021– | 1 025 kg | MMRTG | > 42 km |
| Zhurong | CNSA | Mars | 2021–22 | 240 kg | Solar | 1.9 km |
| Pragyan | ISRO | Moon | 2023 | 26 kg | Solar | ≈ 0.1 km |

: Planetary rovers to 2026. {#tbl:rovers}

![The distances driven by rovers on the Moon and Mars.](figures/out/ch28_distances.svg){#fig:distances width=92%}

## Engineering a Rover

### Mobility

All NASA Mars rovers since Sojourner have used the **rocker-bogie** suspension (@fig:rocker). Each side has a large "rocker" link carrying the rear wheel (or front, depending on direction) and a smaller "bogie" carrying the other two wheels; the two rockers are connected through a differential so the body pitches only half as much as either side. The system has no springs: all six wheels stay in contact with the ground, sharing the load and providing traction, and the rover can climb obstacles almost as high as the wheel diameter. Each wheel has its own drive motor, and the four corner wheels can be steered so the rover can turn in place.

![The rocker-bogie suspension used on NASA's Mars rovers.](figures/out/ch28_rocker.svg){#fig:rocker width=88%}

The greatest mobility hazard is soft ground. A wheel sinks until the soil beneath it can support its load, and must then bulldoze and compact soil in front of it — the **compaction resistance** — while its grousers (tread cleats) shear the soil to generate thrust. The science of this, **terramechanics**, developed by M. G. Bekker and J. Y. Wong for military vehicles, predicts the net force available to pull the rover forward, the **drawbar pull**, as a function of wheel slip (@fig:terra). On loose sand, even a well-designed rover can climb only about 20–25°; Spirit and Opportunity both became trapped in sand, Opportunity escaping after five weeks of careful driving in 2005, Spirit never.

![Wheel–soil interaction. (a) Drawbar pull rises with slip; the same rover on Earth sinks deeper, which is why engineers test Mars rovers with lightened copies. (b) Wider wheels and lighter loads let a rover climb steeper sandy slopes.](figures/out/ch28_terra.svg){#fig:terra width=98%}

::: example
**Example: testing a Mars rover on Earth**

Curiosity has a mass of 899 kg. On Mars each of its six wheels carries 899 × 3.71 / 6 = 556 N; on Earth, 899 × 9.81 / 6 = 1 470 N.

1. With the soil model of @fig:terra, the wheels sink about 23 mm on Mars but 44 mm on Earth, and the compaction resistance rises from 16 % to 22 % of the wheel load.
2. A rover tested at full mass on Earth would therefore perform worse than on Mars — misleading the engineers.
3. JPL instead tests mobility with a lightened rover, nicknamed "Scarecrow", that has the same wheels and suspension but weighs on Earth what Curiosity weighs on Mars (about 340 kg mass), with no computer or cameras on board.
:::

Wheels must also survive rocks. Curiosity's 0.5 m aluminium wheels, with skins only 0.75 mm thick, were punctured and torn by sharp, wind-carved rocks from 2013 (@fig:wheel). The team responded by planning routes over softer ground and, in 2017, uploading a **traction-control** algorithm that adjusts each wheel's speed to reduce the forces on it; Perseverance's wheels were made thicker and narrower, with more grousers.

![Damage to one of Curiosity's aluminium wheels after about 4.8 km of driving, in December 2013.](figures/photos/ch28_wheel.jpg){#fig:wheel width=56%}

### Power and Temperature

A rover must keep its electronics and batteries above about −40 °C through nights that, on Mars, reach −90 °C. Solar-powered rovers house their electronics in an insulated **warm electronics box** heated by electric heaters and radioisotope heater units (RHUs); Spirit and Opportunity carried eight RHUs each. Dust gradually covers solar arrays, reducing power by a fraction of a per cent per sol; Opportunity's arrays were repeatedly cleaned by gusts of wind and dust devils, which is why it lasted 14 years, while Zhurong's power was not restored. Curiosity and Perseverance use **multi-mission radioisotope thermoelectric generators** (MMRTGs), which provide about 110 W of electricity at launch — around 2.5 kWh per sol, day and night — and whose waste heat warms the rover through a pumped fluid loop. Batteries supply the peaks when the rover drives, drills or runs its laboratories.

### Communications and Operations

Rovers can talk directly to Earth through high-gain X-band antennas, but most of their data — hundreds of megabits per sol — is relayed by orbiters passing overhead (Chapter 25). Lunar far-side rovers depend on relay satellites such as Queqiao. Because of the light-time (4–24 minutes each way at Mars) and the limited contact windows, rovers cannot be joysticked. Instead, the operations team plans each sol's activities — drives, images, arm placements, drilling — and uplinks them as a command sequence in the Martian morning; the rover executes them and sends back the results by the afternoon relay pass, and the team plans the next sol. A rover team works on "Mars time" during the first months of a mission, with its working day shifting 40 minutes later each Earth day.

### Autonomous Navigation

To drive further than the operators can see, rovers navigate themselves (@fig:autonav). Stereo cameras build a three-dimensional map of the terrain ahead; software assesses each patch for slope, rocks and steps relative to the rover's dimensions; it chooses the path that makes most progress towards the goal set by the team; and **visual odometry** — tracking features between successive images — measures how far the rover has really moved, correcting for wheel slip. Opportunity's patterned tracks record this process (@fig:opptracks). Spirit and Opportunity had to stop to think after each short step; Perseverance's faster computer and dedicated vision processor let it plan "while driving", and it can cover more than 100 m per hour across favourable terrain — several times faster than Curiosity.

![The autonomous navigation loop of a Mars rover.](figures/out/ch28_autonav.svg){#fig:autonav width=94%}

![Opportunity's tracks on Meridiani Planum in 2011. The pattern of short arcs records the rover stopping to check for hazards autonomously.](figures/photos/ch28_opptracks.jpg){#fig:opptracks width=100%}

### A Laboratory on Wheels

Rover science payloads combine remote-sensing instruments on the mast, contact instruments on a robotic arm, and laboratories inside the body (@tbl:roverpayload).

| Location | Instrument type | Curiosity | Perseverance |
|---|---|---|---|
| Mast | Colour stereo cameras with zoom | Mastcam | Mastcam-Z |
| Mast | Laser-induced breakdown spectroscopy (zaps rocks from up to 7 m) | ChemCam | SuperCam (also Raman and infrared spectroscopy, microphone) |
| Arm | Hand lens imager | MAHLI | WATSON |
| Arm | X-ray spectrometer for chemistry | APXS | PIXL (maps elements at 0.1 mm scale) |
| Arm | Ultraviolet Raman and fluorescence for organics | — | SHERLOC |
| Arm | Rock drill | Powder drill | Coring drill producing intact cores |
| Body | Mineralogy by X-ray diffraction | CheMin | — |
| Body | Organic and isotope analysis by gas chromatography–mass spectrometry | SAM | — |
| Body | Sample sealing and caching | — | 43 tubes |
| Body or deck | Weather, radiation, ground-penetrating radar, oxygen production | REMS, RAD, DAN | MEDA, RIMFAX, MOXIE |

: Science instruments of Curiosity and Perseverance. {#tbl:roverpayload}

## What Rovers Have Found

The Mars rovers have turned the question "was Mars ever habitable?" into a resounding "yes". Opportunity found that Meridiani Planum was once soaked in acidic, salty groundwater; Spirit found the deposits of hot springs; Curiosity found that Gale crater held fresh, neutral water for long periods, with all the chemical ingredients needed by microbes. Perseverance has studied the ancient delta and the volcanic rocks of Jezero's floor. In July 2024, it drilled a rock nicknamed **Cheyava Falls** with millimetre-sized "leopard spots" — pale patches with dark rims rich in iron phosphate and iron sulphide minerals (@fig:leopard). On Earth, such reactions are often driven by microbes. In September 2025 the team reported in *Nature* that the sample, named Sapphire Canyon, contains a **potential biosignature** — a feature that might have a biological origin but could also have formed without life. Only analysis in laboratories on Earth can settle the question.

![The "leopard spots" in the Cheyava Falls rock, imaged by Perseverance's WATSON camera in July 2024. The sample drilled here may preserve a potential biosignature.](figures/photos/ch28_leopard.jpg){#fig:leopard width=62%}

That question is now tied to the fate of **Mars Sample Return**. The NASA–ESA plan to collect Perseverance's tubes with a lander, a small rocket and an Earth-return orbiter grew to an estimated cost of about US$11 billion with return no earlier than 2040. In 2025–26 the US Congress provided no money for the existing programme, leaving the samples on Mars with no retrieval plan, while China's **Tianwen-3** prepares to launch in 2028 and return samples from a different site by 2031 (Chapter 29).

## Aerial Explorers

### Ingenuity: First Flight on Another World

On 19 April 2021, NASA's **Ingenuity** helicopter, carried to Mars beneath Perseverance, rose 3 m above Jezero crater, hovered and landed in a flight lasting 39 seconds — the first powered, controlled flight of an aircraft on another planet (@fig:ingenuity). Flying on Mars is hard: the atmosphere has 1.4 % of the density of Earth's at sea level. Ingenuity, with a mass of 1.8 kg, had two counter-rotating rotors 1.2 m across spinning at about 2 500 rpm — five times faster than a terrestrial helicopter's rotor — limited by the need to keep the blade tips below the speed of sound, which is lower on Mars than on Earth (@fig:flight).

![Perseverance's selfie with Ingenuity in April 2021, shortly before the helicopter's first flight.](figures/photos/ch28_ingenuity.jpg){#fig:ingenuity width=64%}

![The physics of flying on other worlds. (a) Hover power per kilogram for the same rotor loading. (b) Rotor tip Mach number: Mars's lower speed of sound limits rotor speed.](figures/out/ch28_flight.svg){#fig:flight width=98%}

Planned as a five-flight technology demonstration, Ingenuity flew 72 times over nearly three years, covering about 17 km in a total of 129 minutes, reaching altitudes of 24 m and speeds of 10 m/s, and scouting routes for Perseverance. It navigated by tracking features on the ground with a downward-looking camera. On its 72nd flight, on 18 January 2024, over featureless sand ripples, the navigation system lost track of the ground and the helicopter landed hard, breaking its rotor blades (@fig:blade). It remains on Mars as a weather station.

![Ingenuity's own navigation camera reveals the shadow of a rotor blade with its tip missing after its final flight in January 2024.](figures/photos/ch28_blade.jpg){#fig:blade width=50%}

::: example
**Example: hovering on Mars**

Ingenuity weighs $T = 1.8 × 3.71$ = 6.7 N on Mars. Its rotor disk area is $A = \pi × 0.605^2$ = 1.15 m², and the air density at Jezero is about 0.017 kg/m³.

1. Momentum theory gives the ideal hover power $P = T^{3/2} / \sqrt{2\rho A}$ = 6.7^1.5 / √(2 × 0.017 × 1.15) = 17.3 / 0.198 ≈ **88 W**.
2. The same helicopter on Earth would weigh 17.7 N and need only $17.7^{1.5}/\sqrt{2 × 1.225 × 1.15}$ = 74.5 / 1.68 ≈ 44 W: half the power, because the dense air makes the rotor far more effective.
3. Real rotors have a figure of merit (ideal/actual power) of about 0.5–0.6, and the coaxial rotors interfere with each other; Ingenuity drew about 350 W in flight from six lithium-ion cells, so each flight was limited to about 2–3 minutes.
:::

### Balloons

The only balloons flown on another planet were the two **Vega** balloons of 1985, released into the atmosphere of Venus at about 54 km altitude, where they drifted for two days, tracked by a worldwide network of radio telescopes that measured the winds. Venus's cloud layer, where temperature and pressure are similar to Earth's surface, is attractive for long-lived balloons; NASA and others have tested variable-altitude "aerobot" prototypes that could rise and sink through the clouds.

### Dragonfly: Flying on Titan

Titan is the easiest place in the Solar System to fly: its atmosphere is four times denser than Earth's and its gravity one-seventh, so hovering takes about 40 times less power per kilogram than on Earth (@fig:flight). NASA's **Dragonfly**, a car-sized rotorcraft lander with eight rotors and an MMRTG, is scheduled for launch on a Falcon Heavy in July 2028 and arrival in 2034. Landing first in the Shangri-La dune fields, it will fly from site to site — eventually more than 175 km in total — towards the 80 km Selk impact crater, where liquid water and organic molecules may once have mixed. Its mass spectrometer and drill will analyse the surface for prebiotic chemistry. Dragonfly will recharge its batteries from the MMRTG between flights, making flights of several kilometres at a time, roughly once per Titan day (16 Earth days).

## Rovers at the Lunar Poles

The next generation of lunar rovers is heading for the south pole, where water ice is thought to be trapped in **permanently shadowed regions** — crater floors that have not seen sunlight for billions of years and stay below −200 °C. Because the Moon's spin axis is tilted only 1.54° to the plane of its orbit around the Sun, the Sun near the poles never rises more than a few degrees above the horizon; it circles the sky once a month, casting shadows tens of times longer than the objects that cast them (@fig:polar). This creates unique engineering problems:

- **Power and thermal.** Solar arrays must be vertical, and they must turn to follow the Sun around the horizon. A rover that drives into a shadow loses its power and starts to freeze within hours; NASA's VIPER was planned to travel between "safe havens" of sunlight, entering shadowed craters for short excursions only.
- **Navigation.** Low sun angles hide rocks and holes in long shadows and dazzle cameras pointed towards the Sun. Polar rovers carry their own headlights, and stereo vision and lidar must work in near-total darkness.
- **Communications.** Earth, too, hangs low on the horizon and is often hidden by terrain, so rovers need relay satellites or carefully planned routes to stay in contact.

![Lighting at the lunar south pole. (a) Sun elevation over one lunar day–night cycle at two latitudes. (b) Shadow length of a 1 m boulder at low Sun angles.](figures/out/ch28_polar.svg){#fig:polar width=98%}

::: example
**Example: how long are the shadows at the pole?**

At 89.5° S during southern summer, the Sun stays about 2° above a flat horizon.

1. A boulder of height $h$ casts a shadow of length $h / \tan e$, where $e$ is the Sun's elevation: for $e$ = 2°, a 1 m boulder casts a shadow 29 m long.
2. A crater only 10 m deep, with walls rising 5° from its floor, is entirely in shadow when the Sun is lower than 5° — which, at this latitude, is always.
3. On polar summits a few kilometres high, the Sun may be visible for 80–90 % of the year — the reason these "peaks of near-eternal light" are favoured sites for future lunar bases and their solar power stations.
:::

## The Next Generation

| Mission | Body | Planned | Features |
|---|---|---|---|
| VIPER (NASA) | Moon, south pole | Late 2027, on Blue Origin Blue Moon MK1 | Cancelled in 2024 and revived in 2025; prospects for water ice with a 1 m drill and a neutron spectrometer; can raise and lower each wheel to free itself |
| CADRE (NASA) | Moon | 2027, on IM-3 | Three suitcase-sized rovers that explore cooperatively as a team |
| Chang'e 7 (CNSA) | Moon, south pole | 2027 | Rover and a hopping probe to search shadowed craters for ice |
| Lunar Terrain Vehicle (NASA) | Moon | From about 2028 | Unpressurised rover for Artemis crews, also driven remotely between missions; competitors Astrolab, Lunar Outpost and Intuitive Machines |
| Lunar Cruiser (JAXA/Toyota) | Moon | Early 2030s | Pressurised rover in which two astronauts can live and drive for weeks |
| IDEFIX (CNES/DLR) on MMX (JAXA) | Phobos | Launch Oct 2026; landing 2029 | 25 kg rover, first on a Martian moon |
| Rosalind Franklin (ESA) | Mars, Oxia Planum | Launch 2028; landing 2030 | Drill to 2 m depth to reach organics shielded from radiation; NASA provides radioisotope heaters and landing engines |
| Dragonfly (NASA) | Titan | Launch 2028; arrival 2034 | Rotorcraft lander |

: Rovers and aerial explorers in development in 2026. {#tbl:nextrovers}

![A mobility test model of NASA's VIPER lunar rover on a tilting bed of simulated regolith at NASA Glenn Research Center.](figures/photos/ch28_viper.jpg){#fig:viper width=72%}

::: ai
**AI on rovers**

Rovers are among the most autonomous robots ever built. Besides autonomous navigation, Curiosity and Perseverance use **AEGIS**, software that selects rocks in navigation-camera images and aims the laser spectrometer at them without waiting for the ground; Perseverance's PIXL uses **adaptive sampling**, deciding on board where to dwell longer on interesting mineral grains, and an onboard scheduler rearranges activities when tasks run faster or slower than planned. On the ground, machine-learning classifiers of terrain type (sand, bedrock, sharp rocks) trained on orbital and rover images help plan routes that spare the wheels. Future rovers will combine these into "science autonomy" — recognising what is scientifically interesting and acting on it (Chapters 45 and 46).
:::

::: key
**Key takeaways**

- Rovers have explored the Moon since 1970 and Mars since 1997; Opportunity holds the distance record (45.2 km), with Perseverance (> 42 km) and Curiosity (> 37 km) still driving in 2026.
- Rocker-bogie suspensions, terramechanics, wheel design and traction control determine where rovers can go; soft sand and sharp rocks are the main hazards.
- Solar rovers are limited by dust and night-time cold; MMRTG-powered rovers have steady power day and night.
- Light-time forces sol-by-sol planning and growing autonomy: hazard-avoiding navigation, visual odometry, autonomous targeting.
- Rovers established that Mars was once habitable; Perseverance has cached samples, one with a potential biosignature, whose return to Earth is uncertain.
- Ingenuity proved that aircraft can fly on Mars; Dragonfly will fly on Titan, where flight is easiest of all.
:::
