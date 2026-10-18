---
title: Space Stations and Habitats
hero: ch32
abstract: A space station is a spacecraft that people live in for months or years, supplied from Earth and maintained in orbit. This chapter traces stations from Salyut 1 and Skylab through Mir to the International Space Station and China's Tiangong, then takes the ISS apart system by system — power, thermal control, attitude control, reboost, communications and robotics — and explains the engineering that every station must solve: choosing an orbit against drag, sizing arrays and radiators, shielding against micrometeoroids and debris, providing enough habitable volume, and keeping cargo flowing. It covers expandable habitats and artificial gravity, the plan to deorbit the ISS around 2030, and the commercial and national stations competing to replace it as of October 2026.
---

A satellite can be designed once and left alone. A space station cannot: it is a house, a laboratory, a port and a factory in one, occupied by people who must be kept healthy and brought home safely. It must be supplied with tonnes of food, water, gas and spare parts every year, boosted against atmospheric drag, repaired when things break, and protected against impacts from particles moving at ten times the speed of a rifle bullet. In return it offers something nothing else can — months of continuous human presence in weightlessness, for research, technology testing and preparation for journeys to the Moon and Mars.

People have lived aboard the **International Space Station (ISS)** without a break since November 2000, and Chinese crews have occupied the **Tiangong** station continuously since mid-2022. This chapter explains how stations work and how they are designed; the human body and life support are covered in Chapter 30, crewed spacecraft and docking systems in Chapter 31, and spacewalks in Chapter 33.

## Fifty-Five Years of Space Stations

Each station since 1971 has taught how to keep people in orbit longer, with less help from the ground (@fig:stntimeline, @tbl:stationhistory).

![Space stations from Salyut 1 to the stations planned for the late 2020s. Each bar runs from launch to re-entry; hatched bars are planned, with uncertain dates.](figures/out/ch32_timeline.svg){#fig:stntimeline width=96%}

### Salyut and Skylab

The Soviet Union launched the first station, **Salyut 1**, on 19 April 1971: a single 18-tonne cylinder with about 100 m³ of pressurised volume. Its first crew, on Soyuz 10, docked but could not enter. The second, aboard Soyuz 11, spent more than three weeks on board, but on 30 June 1971 Georgy Dobrovolsky, Vladislav Volkov and Viktor Patsayev died during their return when a pressure-equalisation valve was jolted open as the descent module separated, venting its air to space. They are the only people to have died above the atmosphere, and since then Soyuz crews have worn pressure suits for launch and re-entry.

The United States converted a Saturn V third stage into **Skylab**, launched on 14 May 1973 — a 77-tonne station with 361 m³ of volume, still the most spacious station ever launched in one piece (@fig:skylabphoto). Sixty-three seconds into the launch its micrometeoroid shield tore away; one solar wing was lost and debris jammed the other. The first crew, Pete Conrad, Joe Kerwin and Paul Weitz, put up a parasol sunshade to cool the overheating workshop and cut free the jammed wing during a spacewalk — the first major in-orbit repair. Three crews spent 28, 59 and 84 days on board, operating the Apollo Telescope Mount solar observatory. High solar activity then expanded the upper atmosphere, and Skylab re-entered on 11 July 1979 over the Indian Ocean and Western Australia, before the Space Shuttle could boost it.

**Salyut 6** (1977–82) and **Salyut 7** (1982–91) introduced the feature that made long stays possible: a second docking port. Uncrewed **Progress** freighters, first flown in January 1978, could deliver food, water and propellant while a crew was on board, and short "visiting" crews could exchange the Soyuz lifeboat. Stays grew to 237 days in 1984. In 1985 Vladimir Dzhanibekov and Viktor Savinykh docked manually with a dead, frozen Salyut 7 and brought it back to life — a demonstration that crews can repair what automation cannot.

### Mir

**Mir** grew from a core module launched on 19 February 1986 into a 130-tonne complex of seven modules by 1996 (@fig:mirphoto), the first station assembled in orbit. It was occupied for 4 592 days, including almost ten years without a break (1989–99), and in 1994–95 the physician Valeri Polyakov stayed 437 days, still the record for a single spaceflight. Between 1995 and 1998 nine Space Shuttle missions docked with Mir, and seven NASA astronauts lived on board — the rehearsal for the ISS. Mir also taught hard lessons: in February 1997 a burning oxygen-generating canister filled it with smoke, and in June 1997 a remotely piloted Progress struck and punctured the Spektr module, which the crew had to seal off, losing much of the station's power. Mir was deliberately de-orbited into the South Pacific on 23 March 2001.

| Station | Operator | In orbit | Mass (t) | Pressurised volume (m³) | Notable for |
|---|---|---|---|---|---|
| Salyut 1 | USSR | 1971 | 18.4 | ≈ 100 | First station |
| Skylab | USA | 1973–79 | 77 | 361 | Largest module |
| Salyut 6, 7 | USSR | 1977–91 | 19–20 | ≈ 90 | Progress resupply |
| Mir | USSR, Russia | 1986–2001 | ≈ 130 | ≈ 350 | First modular station |
| ISS | 5 agencies | 1998– | ≈ 420 | 1 005 | Crewed since 2000 |
| Tiangong-1, -2 | China | 2011–19 | 8.5 | ≈ 15 | Docking, refuelling tests |
| Tiangong | China | 2021– | ≈ 70 | ≈ 340 | Crewed since 2022 |

: Space stations that have been crewed. Masses exclude visiting vehicles. {#tbl:stationhistory}

::: figrow
![Skylab photographed by the departing Skylab 4 crew in February 1974. The gold twin-pole sunshade, erected by the second crew over the first crew's parasol, covers the workshop, which lost one of its two large solar wings during launch; the windmill-shaped arrays belong to the Apollo Telescope Mount.](figures/photos/ch32_skylab.jpg){#fig:skylabphoto}

![Mir photographed from the approaching Space Shuttle Atlantis on 29 June 1995, during the first Shuttle–Mir docking mission. The modules radiate from the docking node at the front of the core.](figures/photos/ch32_mir.jpg){#fig:mirphoto}
:::

### The International Space Station

The ISS combined the American Freedom station design with the planned Mir-2. Five agencies — NASA, Roscosmos, the European Space Agency (ESA), the Japan Aerospace Exploration Agency (JAXA) and the Canadian Space Agency (CSA) — representing 15 countries are partners. The Russian-built, US-funded Zarya module was launched on 20 November 1998 and the US Unity node two weeks later; the first resident crew, Expedition 1, arrived on 2 November 2000. Assembly took 42 flights — 37 Space Shuttle missions and five Russian launches — and the last major Russian module, the Prichal docking node, arrived in November 2021. On 2 November 2025 the station marked 25 years of continuous occupation, with more than 290 people from 26 countries having visited.

![The ISS seen from Crew Dragon Endeavour after undocking in November 2021: the pressurised modules run down the centre from the 109 m truss and its solar-array wings to the Russian segment.](figures/photos/ch32_iss2021.jpg){#fig:issflyaround width=44%}

### China's Tiangong

China followed a step-by-step path. **Tiangong-1** (2011), an 8.5-tonne laboratory, received the uncrewed Shenzhou 8 and two crews in 2012 and 2013, then re-entered uncontrolled in April 2018. **Tiangong-2** (2016) hosted a 30-day mission and tested in-orbit refuelling by the Tianzhou-1 freighter in 2017. The modular **Tiangong** station began with the 22.5-tonne Tianhe core module on 29 April 2021; the Wentian and Mengtian laboratory modules (July and October 2022) completed a T-shaped station of about 70 tonnes — roughly 90–100 tonnes with docked spacecraft — with about 340 m³ of pressurised volume. It orbits at about 390 km and 41.5° inclination, normally carries three astronauts (six during crew handovers), and was the first crewed station to use **Hall-effect electric thrusters** for reboost. In November 2025, when the Shenzhou-20 return capsule was found to have a cracked window, China launched the uncrewed Shenzhou-22 as a replacement lifeboat within weeks.

## The International Space Station in Detail

The ISS is 109 m from end to end, has a mass of about 420 tonnes and offers 1 005 m³ of pressurised volume — about as much as a Boeing 747 — of which 388 m³ is habitable. It circles Earth every 93 minutes, about 15.5 times a day, at about 415–420 km altitude and 51.6° inclination, passing over more than 90 % of the world's population.

### Modules and Segments

The station has two halves (@fig:isslayout). The **Russian Orbital Segment** includes the Zvezda service module, which provides propulsion, crew quarters and life support for the Russian crew; Zarya, which was the first element; the docking and research modules Poisk, Rassvet, Nauka and Prichal; and ports for Soyuz and Progress. The **US Orbital Segment** includes the nodes Unity, Harmony and Tranquility; the US Destiny laboratory, ESA's Columbus and JAXA's Kibo laboratories; the Quest and commercial Bishop airlocks; the Leonardo storage module; the seven-window Cupola; and the expandable BEAM. Modules connect through standard ports: Russian probe-and-drogue docking ports, **Common Berthing Mechanisms (CBMs)** with 1.27 m square hatches wide enough to pass equipment racks, and **International Docking Adapters (IDAs)** for Crew and Cargo Dragon and Starliner.

### Power

Electrical power comes from eight **solar-array wings**, each about 35 m long, mounted in pairs on rotating joints at the ends of the truss so that they can track the Sun. Their silicon cells, designed for 15 years, have degraded; by about 2020 the arrays generated roughly 160 kW in sunlight. Since 2021 NASA has installed **ISS Roll-Out Solar Arrays (iROSAs)** — flexible blankets that unroll from a compact canister, each producing more than 20 kW — in front of the old wings, partly shading them (@fig:irosaeva). Six iROSAs installed by 2023 raised the output to about 215 kW, and the final pair arrived in October 2026 aboard the CRS-35 Cargo Dragon for installation by spacewalk. Part of the power charges 24 lithium-ion batteries (which replaced 48 nickel–hydrogen batteries in 2017–21) for the eclipse, so the power available to the station's systems and experiments over a whole orbit is much lower than the sunlit output; NASA's fact sheet quotes 75–90 kW. The US segment distributes power at 160 V direct current, converted to 124 V for users; the Russian segment uses 28 V.

![Schematic connection diagram of the ISS pressurised modules and the ports used by visiting vehicles in 2026.](figures/out/ch32_isslayout.svg){#fig:isslayout width=98%}

### Thermal Control

Every watt the station uses ends up as heat that must be radiated to space. Inside the US segment, two water loops — a low-temperature loop at about 4 °C and a moderate-temperature loop at about 17 °C — collect heat from cold plates and air heat exchangers. Water is safe in the cabin but would freeze outside, so heat exchangers pass the heat to the **External Active Thermal Control System**, two independent loops of liquid ammonia that circulate through six radiator assemblies on the truss — three on each side, each of eight panels and each rejecting about 11.7 kW, 70 kW in all. The radiators rotate to keep edge-on to the Sun. Separate radiators cool the power electronics at the array roots. Ammonia leaks and pump failures have required several repair spacewalks.

### Attitude Control and Reboost

The station normally flies with one axis along its velocity and another pointing at Earth, turning once per orbit. Small torques from gravity gradient, drag and venting would slowly twist it out of this attitude, so four **control moment gyroscopes (CMGs)** on the Z1 truss absorb them. Each is a 100 kg wheel spinning at 6 600 rpm with an angular momentum of 4 760 N·m·s; tilting the wheel's axis on motorised gimbals produces a torque on the station without using propellant. When the CMGs approach saturation, or for large manoeuvres, Russian thrusters take over. The station is flown slightly tilted, in a **torque-equilibrium attitude** where aerodynamic and gravity-gradient torques cancel on average.

![NASA astronauts Josh Cassada and Frank Rubio installing an iROSA on the starboard truss during a spacewalk in December 2022. The rolled-up array canister is left of centre; the older, gold-coloured array wing is behind them.](figures/photos/ch32_irosa.jpg){#fig:irosaeva width=58%}

Drag lowers the station by roughly 1–5 km per month, depending on solar activity. It is periodically **reboosted** — raised by a few kilometres — by the engines of Zvezda and docked Progress freighters, and since November 2024 also by Cargo Dragon, one of which (CRS-33, 2025–26) carried a propulsion kit in its trunk; ESA's ATV and some Cygnus missions provided reboosts in the past. Thrusters also perform **debris-avoidance manoeuvres** when a tracked object's collision probability exceeds about 1 in 10 000: about 40 between 1999 and 2024. In July 2021, shortly after Nauka docked, its thrusters fired unexpectedly and turned the whole station about one and a half revolutions before controllers regained control.

### Communications, Data and Robotics

Voice, telemetry and commands travel over S-band, and high-rate data and video over Ku-band, through NASA's **Tracking and Data Relay Satellites (TDRS)** in geostationary orbit, which give almost continuous coverage (Chapter 7); the Russian segment uses ground stations and Luch relay satellites. More than 50 computers run about 1.5 million lines of flight software and monitor about 350 000 sensors.

**Canadarm2**, a 17.6 m arm with seven joints and a latching "hand" at each end, can move end over end between grapple fixtures and ride a mobile base along the truss. It assembled much of the station, captures visiting cargo vehicles and moves spacewalkers. Its two-armed attachment **Dextre** handles smaller replaceable units (@fig:canadarm2dextre), and Kibo and Nauka carry their own arms. After a wrist joint failed in May 2026, spacewalkers replaced it with a spare on 30 June 2026.

![Canadarm2 with Dextre attached, extending from the Harmony module above the Sahara in August 2025.](figures/photos/ch32_dextre.jpg){#fig:canadarm2dextre width=56%}

### Crew, Research and Cost

The station normally hosts seven people — four launched on Crew Dragon and three on Soyuz, with seats swapped between the vehicles so that each segment always has trained crew. Nearly 3 000 investigations from more than 108 countries have used its racks, freezers, glove boxes, furnaces and external platforms, from protein crystal growth and combustion to Earth observation and the Alpha Magnetic Spectrometer. Total spending by all partners is often estimated at more than US$ 150 billion. NASA's Inspector General put NASA's own cost at about US$ 3 billion per year for operations and transport, or about US$ 4.1 billion per year including research and related activities — about 16 % of NASA's budget.

| Parameter | Value |
|---|---|
| Mass; dimensions | ≈ 420 t; 109 m × 73 m |
| Pressurised / habitable volume | 1 005 m³ / 388 m³ |
| Orbit | ≈ 415–420 km, 51.6°, 93 min |
| Crew | 7 (more during crew handovers) |
| Power | 8 wings + 6 iROSAs (≈ 215 kW in sunlight); 24 Li-ion batteries |
| Heat rejection | Two ammonia loops; 6 radiators, ≈ 70 kW |
| Attitude control | 4 CMGs (4 760 N·m·s each) + Russian thrusters |
| Communications | S- and Ku-band via TDRS; UHF for spacewalks and approaching vehicles |
| Robotics | Canadarm2 (17.6 m) with Dextre; Kibo and European arms |
| Docking ports | Up to 8 vehicles at once (Soyuz, Progress, Dragon, Cygnus, HTV-X) |

: International Space Station key figures (2026). {#tbl:issspecs}

### An Ageing Station

The oldest ISS modules have been in orbit since 1998. Since 2019 air has been leaking from the **PrK**, a small tunnel between Zvezda's main compartment and its aft docking port, through hairline cracks. In April 2024 the leak reached about 1.7 kg of air per day; NASA rated it its highest-level safety risk, and the hatch is normally kept closed. NASA and Roscosmos have not agreed on the root cause. The tunnel was reported to be holding pressure in January 2026, but the leak returned in May; on 5 June 2026 five crew members briefly sheltered in their Crew Dragon while Roscosmos began, then paused, a structural repair, and press reports later said Roscosmos would stop pressurising the tunnel. Such ageing problems are a main reason for retiring the station around 2030.

## Engineering a Station

### Choosing the Orbit

A station's **inclination** — the angle between its orbit and the equator — is usually set by its launch sites. A rocket launched due east reaches an inclination equal to the latitude of its launch site, and higher inclinations cost payload. The ISS flies at 51.6° because Russian vehicles from Baikonur (46° N) cannot launch due east without dropping stages on China; American vehicles from Florida (28.5° N) pay a payload penalty to reach it. Tiangong's 41.5° suits the Jiuquan launch site.

**Altitude** is a compromise. Lower is cheaper to reach — every kilometre of altitude costs payload for each crew and cargo flight — but the air is denser, so the station must spend more propellant fighting drag (@tbl:stnaltitude). Higher reduces drag but increases radiation exposure, as orbits approach the inner Van Allen belt, and the density of orbital debris, and makes Earth-observation instruments less sharp. During the Shuttle era the ISS flew as low as 330–350 km so that the Shuttle could deliver the heaviest modules; since 2011 it has been kept near 400–420 km.

Drag decays the orbit as described in Chapter 2:

$$\frac{da}{dt} = -\frac{\rho\,\sqrt{\mu a}}{B}, \qquad B = \frac{m}{C_D A}$$

where $\rho$ is the air density, $a$ the orbit radius, $\mu$ Earth's gravitational parameter and $B$ the ballistic coefficient. Holding altitude requires a velocity increment each year equal to the drag deceleration integrated over time, $\Delta v = \int \rho v^2/(2B)\,dt$. Because thermospheric density changes by a factor of about ten over the 11-year solar cycle, the reboost budget does too (@fig:stndecay). Without reboosts, an ISS-class station released at 420 km would re-enter within about one year at solar maximum and about six years at solar minimum.

![(a) Altitude of an ISS-class station left without reboost, starting from 420 km. (b) Propellant needed each year to hold a constant altitude with chemical thrusters, and with Hall-effect electric thrusters at moderate solar activity.](figures/out/ch32_decay.svg){#fig:stndecay width=98%}

| Altitude (km) | Decay, moderate activity (km/month) | Δv per year: min / moderate / max (m/s) | Propellant per year, moderate (t) | Life without reboost, moderate (years) |
|---|---|---|---|---|
| 350 | 6.5 | 19 / 45 / 106 | 7.0 | 0.6 |
| 380 | 3.7 | 10 / 25 / 65 | 3.9 | 1.1 |
| 400 | 2.5 | 6 / 17 / 46 | 2.7 | 1.7 |
| 420 | 1.7 | 4 / 12 / 34 | 1.9 | 2.5 |
| 450 | 1.0 | 2 / 7 / 22 | 1.1 | 4.3 |
| 500 | 0.4 | 1 / 3 / 11 | 0.5 | 11 |

: Drag penalty of altitude for a 450 t station with B = 150 kg/m², computed with the model of @fig:stndecay (specific impulse 290 s). {#tbl:stnaltitude}

::: example
**Example: annual reboost for an ISS-class station**

Take a station of 450 t, including docked vehicles, with an average drag area $C_D A$ ≈ 3 000 m², so that $B$ = 150 kg/m², at 410 km in moderate solar activity ($\rho$ ≈ 2.3 × 10⁻¹² kg/m³).

1. Orbital speed: $v = \sqrt{\mu/a} = \sqrt{3.986\times10^{14}/6.788\times10^{6}}$ = 7 663 m/s.
2. Drag deceleration: $\rho v^2/(2B)$ = 2.3 × 10⁻¹² × 7 663² / 300 = 4.5 × 10⁻⁷ m/s² — about 50 billionths of g.
3. Over a year (3.16 × 10⁷ s) this accumulates to **Δv ≈ 14 m/s**, and the orbit would sink by about 68 m per day (2.1 km per month) if not corrected.
4. With thrusters of $I_{sp}$ = 290 s ($v_e$ = 2 844 m/s), the propellant is $m(1 - e^{-\Delta v/v_e}) = 450\,000 \times (1 - e^{-14.1/2\,844})$ ≈ **2.2 t per year**.
5. At solar maximum the density is nearly three times higher: Δv ≈ 40 m/s and **6.3 t per year**. Hall thrusters ($I_{sp}$ ≈ 1 600 s) would need only about 0.4 t at moderate activity.

The reported ISS average of about 7 t per year is higher because it also covers attitude control and debris avoidance.
:::

### Power and Thermal Budgets

The angle between the orbit plane and the direction of the Sun, the **beta angle (β)**, changes continuously as the orbit plane precesses and Earth moves round the Sun; for the ISS it swings between about −75° and +75° over roughly two months. At β = 0 the station spends 36 of every 93 minutes in shadow; above β ≈ 70° it is in permanent sunlight (@fig:stnpowerthermal). The arrays must supply both the load and the battery charge for the next eclipse, and because storing energy in a battery and recovering it wastes about a third of it, the arrays must produce about 2.2 times the orbit-average load at low β. At high β, constant sunlight overheats some surfaces, so the attitude may be changed and visiting-vehicle traffic restricted.

![(a) Eclipse duration at 420 km and the ratio of array output to orbit-average load needed to recharge batteries, as functions of beta angle. (b) Radiator area needed to reject 10 kW as a function of radiator temperature for three effective sink temperatures.](figures/out/ch32_powerthermal.svg){#fig:stnpowerthermal width=98%}

The radiators must reject the whole electrical load plus the heat produced by the crew (about 100–150 W per person). Radiated flux follows the Stefan–Boltzmann law, $q = \varepsilon \sigma (T^4 - T_{sink}^4)$, so a radiator near 0 °C — cold enough to cool the cabin through heat exchangers — emits only about 200–250 W/m² even with a cold view of space, and much less when it sees the warm Earth or sunlight. That is why the ISS radiators are among its largest structures. Power, heat rejection and drag are coupled: larger arrays bring more heat to reject, larger radiators and more drag.

### Protecting Against Micrometeoroids and Debris

A station is a large target: the ISS presents more than 1 000 m² of pressurised-module surface to the particle environment described in Chapters 2 and 21. Its crew modules are protected by **Whipple shields** — a thin aluminium bumper spaced in front of the pressure wall, which breaks up an incoming particle into a spreading cloud of fragments — and by **stuffed Whipple shields** with layers of Nextel ceramic cloth and Kevlar between bumper and wall. The ISS uses more than 100 different shield configurations, the heaviest on forward-facing surfaces, which see the most debris impacts.

The performance of a shield is described by its **ballistic limit**: the diameter $d_c$ of the largest aluminium sphere it can stop, as a function of speed and impact angle (@fig:stnmmod). At low speeds (below about 3 km/s) a projectile stays intact and the shield behaves like a thick plate; between about 3 and 7 km/s the projectile shatters on the bumper and the shield becomes *more* effective with speed; above 7 km/s the fragments melt and vaporise, and $d_c$ falls slowly with speed. NASA's ballistic limit equation for the high-speed regime is

$$d_c = 3.918\; t_w^{2/3}\, \rho_p^{-1/3}\, \rho_b^{-1/9}\, (V\cos\theta)^{-2/3}\, S^{1/3} \left(\frac{\sigma}{70}\right)^{1/3}$$

in cm, with wall thickness $t_w$ and spacing $S$ in cm, projectile and bumper densities $\rho_p$, $\rho_b$ in g/cm³, speed $V$ in km/s, impact angle $\theta$ and wall yield strength $\sigma$ in ksi. Doubling the spacing increases $d_c$ by 26 %; a single wall of the same mass stops particles four to five times smaller. The ISS stuffed Whipple shields are designed to stop particles of about 1.3 cm at typical impact conditions. Larger, catalogued objects are avoided by manoeuvring, but objects between about 1 and 10 cm can be neither shielded against nor tracked (Chapter 21).

![(a) Ballistic limit of a Whipple shield and of a single aluminium wall of equal mass, from NASA's empirical equations. (b) Probability that a 100 m² module suffers no penetration, for the three wall designs, using the illustrative flux model of Chapter 2.](figures/out/ch32_mmod.svg){#fig:stnmmod width=98%}

::: example
**Example: penetration risk for a module over ten years**

A laboratory module exposes 100 m² of effective area to impacts. Typical debris strikes at 9 km/s and 45°.

1. **Shield.** A Whipple shield with a 1.6 mm aluminium bumper, a 10 cm gap and a 3.2 mm aluminium-alloy wall has $d_c$ ≈ 6.8 mm at these conditions; a single 4.8 mm wall of the same mass has $d_c$ ≈ 1.5 mm; the ISS stuffed Whipple stops about 13 mm.
2. **Flux.** The cumulative flux of particles larger than $d_c$ is read from the illustrative ISS-altitude curve of Chapter 2, which follows the shape of NASA's ORDEM debris model: about 1.5 × 10⁻³ per m² per year above 1.5 mm, 7 × 10⁻⁵ above 6.8 mm and 2 × 10⁻⁵ above 13 mm.
3. **Expected penetrations** in ten years: $N = F A T$ = 1.5, 0.073 and 0.021 respectively.
4. Impacts are random, so the **probability of no penetration** is $P = e^{-N}$: **0.22** for the single wall, **0.93** for the Whipple shield and **0.98** for the stuffed Whipple.
5. Ten such modules multiply $N$ by ten: PNP falls to about 0.81 even with the best shields. Not every penetration is catastrophic — a small hole leaks slowly enough to be found and sealed — so NASA also estimates the risk of evacuation or crew loss with tools such as BUMPER and MSCSurv.
:::

The ISS has suffered damage. Impacts chip its windows, which is why the Cupola has external shutters; a debris strike punched a 5 mm hole in Canadarm2's thermal blanket in 2021; and in December 2022 the coolant radiator of a docked Soyuz, MS-22, was punctured, probably by a micrometeoroid, so that it had to return uncrewed and a replacement Soyuz was launched. After Russia destroyed its Kosmos 1408 satellite in an anti-satellite test on 15 November 2021, the crew sheltered in their docked spacecraft while the station passed through the debris cloud.

### Habitable Volume and Layout

Volume is measured in three ways. **Pressurised volume** is everything inside the hull; **habitable volume** excludes the space taken by racks and fixed equipment; and **net habitable volume** is what remains free for people to move in once stowage and loose equipment are counted. In 2014 a NASA Human Research Program panel of experts recommended a minimum net habitable volume of 25 m³ per person for a Mars mission lasting about 912 days; its comparison listed about 120 m³ per person for Skylab, 45 for Mir and 34 for Salyut, while today's ISS offers about 55 m³ (388 m³ for seven people) (@fig:stnvolume). The ISS crew quarters — private sleeping cabins — are about 2.1 m³ each, the size of a telephone box.

![Habitable volume per person against the longest stay on several stations and spacecraft, with the minimum recommended by NASA's Human Research Program for a long Mars mission.](figures/out/ch32_volume.svg){#fig:stnvolume width=82%}

In weightlessness there is no natural up or down, but designers still give every module a consistent "floor" and "ceiling", with lighting overhead and labels the right way up, because people orient faster and make fewer mistakes. Handrails and foot restraints replace chairs, and fan and pump noise is a persistent habitability problem. Windows matter for morale as much as for operations: the Cupola, installed in 2010, gives a panoramic view used for robotics and photography (@fig:cupolacrew).

![ESA astronaut Sophie Adenot and NASA astronaut Jack Hathaway in the Cupola in May 2026, monitoring the automated approach of a Cargo Dragon.](figures/photos/ch32_cupola.jpg){#fig:cupolacrew width=42%}

## Supplying a Station

### Cargo Vehicles

Even recycling about 98 % of its water (Chapter 30), a crew of seven consumes several tonnes of food, gases, clothing and hygiene items a year, and the station also needs propellant, spares and experiments. Cargo vehicles differ in how much they carry up (**up-mass**), whether they can carry unpressurised cargo such as pumps and batteries outside, whether they can refuel and reboost the station, and whether anything comes back (**down-mass**) (@fig:stnlogistics, @tbl:cargovehicles). Most freighters are loaded with rubbish before they leave and burn up on re-entry; apart from small items carried in crew capsules, only Dragon returns experiments and failed hardware to Earth; Dream Chaser could do so if NASA later orders ISS flights.

![Cargo capacity per flight of station supply vehicles. Most freighters burn up with the station's waste; Cargo Dragon is currently the only vehicle that returns cargo.](figures/out/ch32_logistics.svg){#fig:stnlogistics width=92%}

JAXA's **HTV-X**, successor to the HTV, made its first flight on an H3 rocket on 26 October 2025; it was captured by Canadarm2 on 29 October (@fig:htvx1). Northrop Grumman's larger **Cygnus XL**, about a third roomier than its predecessor, first flew in September 2025 (@fig:cygnusxl). Sierra Space's winged **Dream Chaser** has repeatedly slipped: in September 2025 NASA removed its guaranteed ISS flights, and its first mission is a free-flying demonstration on a Vulcan rocket planned for late 2026 at the earliest.

| Vehicle | Operator | Since | Arrival | Up / down (t) | Notes |
|---|---|---|---|---|---|
| Progress MS | Roscosmos | 1978 (MS: 2015) | Automatic docking | ≈ 2.5 / 0 | Refuels and reboosts Russian segment |
| Cygnus / Cygnus XL | Northrop Grumman | 2013 / 2025 | Berthed by Canadarm2 | 3.75–5 / 0 | XL first flew Sept 2025 |
| Cargo Dragon | SpaceX | 2012 (Dragon 2: 2020) | Automatic docking | ≈ 6 / 3 | Ocean splashdown; reboost kit |
| HTV-X | JAXA | Oct 2025 | Berthed by Canadarm2 | ≈ 5.8 / 0 | Can fly up to 1.5 years after leaving |
| Tianzhou | CMSA | 2017 | Automatic docking | ≈ 6–7 / 0 | Supplies Tiangong; refuels it |
| Dream Chaser | Sierra Space | Not yet flown | (Berthing planned) | ≈ 5.5 / 1.85 | Winged; runway landing; free-flyer demo first |
| ATV; HTV | ESA; JAXA | 2008–14; 2009–20 | Docking; berthing | 7.7; 6 / 0 | Retired |

: Station cargo vehicles (October 2026). {#tbl:cargovehicles}

::: figrow
![JAXA's first HTV-X in the grip of Canadarm2 on 29 October 2025, carrying about 5.8 t of supplies.](figures/photos/ch32_htvx.jpg){#fig:htvx1}

![A Cygnus XL freighter waiting at its capture point, 12 m from the station, as Canadarm2 prepares to grapple it in April 2026.](figures/photos/ch32_cygnusxl.jpg){#fig:cygnusxl}
:::

### Docking and Berthing

Vehicles join a station in two ways. In **docking**, the visiting vehicle flies itself into contact: Soyuz and Progress use the Russian Kurs radar system and probe-and-drogue ports, while Dragon uses its own sensors and the androgynous International Docking System Standard (Chapter 31). In **berthing**, the vehicle flies to a capture point 10–12 m below the station and holds position with its thrusters disabled while an astronaut grapples it with Canadarm2 and installs it on a CBM port, where powered bolts pull the two rings together. Berthing needs no precision docking system on the visitor and gives a wide hatch for racks, but requires the arm and a trained crew.

Approaches follow strict rules: an **approach ellipsoid** of 4 × 2 × 2 km around the station and a **keep-out sphere** of 200 m radius that a vehicle may enter only after a "go" from mission control, along a defined corridor and with an automatic abort capability. Solar arrays are usually turned edge-on to protect them from thruster plumes.

## Expandable Habitats and Artificial Gravity

### Expandable Modules

A rigid module can be no wider than the rocket fairing that launches it — about 4.5 m for most modules so far. An **expandable** (or inflatable) module is launched folded and then pressurised in orbit, giving several times more volume per launch. Its wall is built from layers of fabric: inner gas bladders (usually redundant) that hold the air; a **restraint layer** of woven Kevlar or Vectran straps that carries the pressure load; many spaced layers of ceramic cloth and foam that act as a multi-shock micrometeoroid shield; multilayer thermal insulation; and an outer cover against atomic oxygen.

The restraint layer must resist a hoop load per unit length of $N = p\,r$. For a module 8.2 m across at one atmosphere (101 kPa), that is about 415 kN per metre of wall — the weight of 42 tonnes hanging from each metre — and the fabric must withstand about four times that. NASA's TransHab technology of the 1990s passed to Bigelow Aerospace, which flew the uncrewed Genesis I and II prototypes in 2006–07. The **Bigelow Expandable Activity Module (BEAM)**, about 1.4 t, was berthed to the ISS in April 2016 and expanded on 28 May 2016 to about 16 m³ (@fig:beamphoto). Planned as a two-year test, it is still attached a decade later and used for storage; its ownership passed to NASA in 2021 after Bigelow ceased operations. Sierra Space's **LIFE** habitat, about 8 m in diameter with about 285 m³ inside, burst at 77 psi and 74 psi (530 and 510 kPa) in full-scale tests in December 2023 and June 2024, 22–27 % above the 60.8 psi (four times operating pressure) that NASA recommends.

![BEAM (the fabric-covered module, lower centre), attached to the Tranquility node next to the shuttered Cupola and the Bishop airlock, photographed from the Russian segment in August 2022.](figures/photos/ch32_beamx2.jpg){#fig:beamphoto width=54%}

### Artificial Gravity

Weightlessness weakens bones, muscles and the heart and affects the eyes (Chapter 30). Exercise reduces but does not prevent these effects, and a rotating habitat could replace weight with centripetal acceleration:

$$a = \omega^2 r, \qquad a_{Cor} = 2\,\omega\, v_{rel}$$

where $\omega$ is the rotation rate, $r$ the radius and $v_{rel}$ the speed of a person moving inside the habitat. The **Coriolis acceleration** $a_{Cor}$ makes moving objects veer sideways, and turning the head in a rotating room confuses the inner ear, causing motion sickness. Experiments in rotating rooms suggest that almost everyone is comfortable at up to about 2 rpm, and that people can adapt to about 4–6 rpm (@fig:artgravity). A low rotation rate requires a large radius: for 1 g at 2 rpm, the radius is 224 m. A **gravity gradient** between head and feet is a further issue for small radii.

![Rotation rate against radius for 1 g and Mars-level artificial gravity, with commonly quoted comfort limits and some historical concepts.](figures/out/ch32_gravity.svg){#fig:artgravity width=90%}

::: example
**Example: a rotating habitat for 1 g at 2 rpm**

1. Rotation rate: ω = 2 × 2π/60 = 0.209 rad/s.
2. Radius for 1 g: $r = g/\omega^2$ = 9.81/0.209² = **224 m** — a structure almost half a kilometre across. Rim speed: $\omega r$ = 47 m/s.
3. Coriolis acceleration on a crew member walking at 1 m/s: 2 × 0.209 × 1 = 0.42 m/s² — about 4 % of their weight, pushing sideways.
4. Walking 1 m/s in the direction of rotation raises apparent weight by 4.3 %; walking the other way lowers it by 4.2 %.
5. Gravity gradient over a 1.8 m person: 1.8/224 = **0.8 %** — negligible. At 4 rpm the radius shrinks to 56 m, but the Coriolis acceleration doubles and the gradient reaches 3 %.

Mars gravity (0.38 g) at 2 rpm needs 85 m. A cheaper option is to spin two masses — a habitat and a spent stage or counterweight — connected by a tether.
:::

No crewed station has yet used artificial gravity. In 1966 Gemini 11 spun itself and an Agena stage on a 30 m tether, producing a tiny artificial gravity. On the ISS, JAXA's Multiple Artificial-gravity Research System centrifuge has kept mice at controlled artificial-gravity levels for comparison with weightless animals, and short-arm human centrifuges have been tested on the ground in bed-rest studies.

## After the ISS

### Retiring and Deorbiting the ISS

The partners plan to operate the ISS until 2030; Roscosmos said in April 2026 that it would begin rounding off its ISS work in 2028 and expected the deorbit to be completed in 2030. A 420-tonne station cannot be left to re-enter uncontrolled: tens of tonnes of dense parts — truss segments, docking rings, tanks — would survive and fall anywhere under its 51.6° ground track. It must instead be steered into a remote area of the South Pacific.

In June 2024 NASA awarded SpaceX a contract worth up to US$ 843 million for the **US Deorbit Vehicle (USDV)**, a heavily modified Dragon with 46 Draco thrusters and about 16 t of propellant; with launch, NASA puts the total at about US$ 1.5 billion. Launched about 18 months before the end, the USDV will dock at the forward port while the station sinks. The last crew will leave at about 330 km, some six months before re-entry; at about 225 km the USDV will begin a series of burns, the last of which, about four days later, aims the debris at the South Pacific — in early 2031 on current plans. Lowering the perigee from a 225 km circular orbit to about 50 km requires about 52 m/s, which for 450 t is about 8 t of propellant at $I_{sp}$ = 300 s; much of the remaining propellant is needed to control the station's attitude as aerodynamic torques grow during the final orbits.

### Commercial Stations

NASA wants to buy services on commercial stations rather than own one. Its **Commercial LEO Destinations (CLD)** programme gave Space Act Agreements worth US$ 415.6 million in December 2021 to Blue Origin, Nanoracks (now part of Voyager, for Starlab) and Northrop Grumman (which later joined Starlab); Axiom Space separately holds a contract to attach modules to the ISS. The programme was restructured repeatedly in 2025–26: an August 2025 directive lowered the minimum capability NASA would require, a proposal in March 2026 to attach a government-owned core module to the ISS was dropped in June, and on 9 October 2026 NASA issued its final request for proposals for firm-fixed-price contracts covering development, certification and services, with proposals due on 8 December 2026 and two or more awards expected in spring 2027. Because a commercial station must be certified and crewed before the ISS is deorbited, and schedules keep slipping, a gap in continuous US presence in orbit is possible (@tbl:futurestations).

**Vast**'s **Haven-1** would host four-person crews arriving by Crew Dragon for about two weeks at a time; Vast proposes a larger multi-module **Haven-2** for the NASA competition. **Axiom Space**, which has flown private crews to the ISS since 2022, changed its plan in December 2024 so that its first module, a power and thermal module, will attach to the ISS and later depart to join a habitat module as a free-flying station. **Starlab** is a single 8 m-diameter station to be launched fully outfitted on one Starship.

### National Stations: China, Russia and India

If the ISS ends on schedule, China's Tiangong will be the only government station in low Earth orbit, and its planned six-module expansion would double it. Russia's **Russian Orbital Station (ROS)** was redesigned in December 2025 to use the ISS's 51.6° orbit rather than a near-polar one, with its first modules attached to the ISS from about 2028. India's **Bharatiya Antariksh Station (BAS)** builds on the Gaganyaan crew vehicle and the SpaDeX docking experiment; its first module, of about 10 t, is to be launched on an LVM-3.

| Station | Developer | First launch (planned) | Configuration | Status, October 2026 |
|---|---|---|---|---|
| Haven-1 | Vast | NET Q1 2027 | 14 t, 45 m³; 4 crew for ≈ 2 weeks | Integration and tests; Haven Demo flew Nov 2025 |
| Axiom Station | Axiom Space | ≈ 2028 | Power module first on ISS, then joins Hab-1 to fly free | Modules in production |
| Starlab | Voyager, Airbus and partners | NET 2029, one Starship launch | 8 m diameter, ≈ 450 m³, 4 crew | Critical design review Feb 2026 |
| Orbital Reef | Blue Origin, Sierra Space | Not announced | Multi-module, LIFE habitats | Few public milestones |
| ROS | Roscosmos | 2028 | First modules attached to ISS, 51.6° | Redesigned Dec 2025 |
| Bharatiya Antariksh Station | ISRO | BAS-01 by 2028 | Five modules by 2035 | First module approved 2024 |
| Tiangong expansion | CMSA | Not dated | Six modules, ≈ 180 t | Plan shown 2023, confirmed 2026 |

: Successors and new stations (status as of October 2026). {#tbl:futurestations}

### Gateway and Surface Habitats

The **Lunar Gateway**, a small station planned for a near-rectilinear halo orbit around the Moon, was to begin with a Power and Propulsion Element (PPE) and a Habitation and Logistics Outpost (HALO). The FY2026 budget request proposed cancelling it, and on 24 March 2026 NASA paused Gateway "in its current form" in favour of a lunar surface base; by August 2026 the HALO hardware was being repurposed for lunar-surface demonstration missions, and the PPE was reported to be under study for other uses. Its future as a station is uncertain.

On the surface, NASA's Artemis Base Camp concept foresaw a pressurised rover and a fixed habitat near the lunar south pole; its Moon Base programme (March 2026) starts with demonstrations of surviving the lunar night. Surface habitats gain gravity, local materials and a planet that blocks half the sky, but must cope with abrasive dust, temperature swings of almost 300 °C on the Moon and no magnetic field. A 1 m layer of regolith (density about 1.5 g/cm³) provides about 150 g/cm² of shielding — enough against solar particle events, though several metres are needed to remove most of the cosmic-ray dose. Proposals include covering inflatable habitats with bagged regolith, sintering or 3D-printing regolith into walls, and using lava tubes (Chapters 30 and 41).

::: ai
**AI in station operations**

Station operations are moving towards autonomy. The ISS already uses automated fault detection and procedure execution, and NASA's **Astrobee** — three cube-shaped free-flying robots that navigate Kibo with cameras and fans (@fig:astrobeekoch) — has been used since 2019 to test autonomous inventory, inspection and mapping. DLR's **CIMON**, an AI-powered floating assistant with voice interaction, flew from 2018, and JAXA's Int-Ball camera drone films crew activities. Machine-learning models are being trained on years of station telemetry to predict failures of pumps, fans and CMGs before they happen, and commercial stations plan to operate with very small ground teams and no permanent crew. Chapter 46 discusses AI for human spaceflight in detail.
:::

![NASA astronaut Christina Koch testing the mobility of an Astrobee free-flying robot in the Kibo laboratory in July 2019.](figures/photos/ch32_astrobee.jpg){#fig:astrobeekoch width=42%}

::: key
**Key takeaways**

- Stations evolved from single modules (Salyut 1, Skylab) through resupply by freighters (Salyut 6) and modular assembly (Mir) to the 420 t ISS, crewed continuously since November 2000, and China's Tiangong, crewed continuously since 2022.
- A station is a coupled system: solar arrays sized for eclipses, radiators sized for the full load, CMGs for attitude, and propellant for reboost — about 4–40 m/s per year at ISS altitude, depending on the solar cycle.
- Orbit selection trades launch cost against drag: lowering the orbit from 420 to 350 km almost quadruples the reboost propellant, and solar maximum roughly triples it compared with average conditions.
- Whipple and stuffed Whipple shields stop particles up to about 1.3 cm; combining ballistic-limit equations with a flux model gives the probability of no penetration, which falls with area and time.
- Logistics depend on several freighters, most of them destroyed on re-entry; Cargo Dragon is the only vehicle returning cargo, and HTV-X and Cygnus XL entered service in 2025.
- Expandable habitats offer several times more volume per launch; artificial gravity at comfortable rotation rates needs radii of hundreds of metres.
- The ISS is to be deorbited by a SpaceX-built vehicle around 2030–31; commercial stations (Haven-1, Axiom, Starlab), Russia's ROS, India's BAS and an expanded Tiangong are planned, while Gateway has been paused.
:::

::: questions
**Review questions**

1. What design feature introduced on Salyut 6 made long-duration stations possible, and why?
2. Why did Skylab re-enter earlier than NASA had planned? Link your answer to the solar cycle.
3. Explain how a control moment gyroscope produces torque without propellant, and why the ISS still needs thrusters for attitude control.
4. Using @tbl:stnaltitude, estimate how much more propellant per year a station at 380 km needs than one at 420 km, at moderate solar activity. What are the advantages of the lower altitude?
5. At β = 0, an ISS-like station is in eclipse for 36 of 93 minutes. With path efficiencies of 0.65 through the battery and 0.85 directly, what array output is needed for a 100 kW orbit-average load?
6. Why is a Whipple shield more effective at 6 km/s than at 3 km/s? Sketch its ballistic-limit curve.
7. A module of 60 m² has a shield that stops particles up to 8 mm, and the flux above 8 mm is 5 × 10⁻⁵ per m² per year. What is the probability of no penetration over 15 years?
8. Compare docking and berthing. Why do Cygnus and HTV-X berth rather than dock?
9. What radius is needed for 0.38 g at 3 rpm? What Coriolis acceleration acts on a crew member walking at 1.2 m/s?
10. List the main candidates to succeed the ISS and the status of each as of October 2026. What is the risk of a "gap" in continuous human presence in orbit?
:::
