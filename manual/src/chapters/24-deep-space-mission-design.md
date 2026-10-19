---
title: Deep-Space Mission Design
hero: ch24
abstract: Sending a spacecraft to another world is an exercise in patience and precision. Launch windows open only every few years; journeys last months to decades; signals take minutes to hours to arrive; sunlight fades; radiation, dust and extreme temperatures test every component. This chapter explains how deep-space missions are designed: interplanetary trajectories and launch windows — with launch opportunities to Mars computed for 2026–2041 — gravity assists, low-thrust electric propulsion, orbit insertion and aerobraking, cislunar and libration-point orbits, deep-space navigation and communications, power and thermal design across the Solar System, planetary protection, and the life cycle and cost of a flagship mission. It ends with the fleet of deep-space missions active in 2026.
---

## The Challenge of Deep Space

Deep-space missions — to the Moon, planets, asteroids, comets, the Sun and beyond — face constraints that Earth-orbiting satellites rarely meet:

- **Energy and time**: escaping the Earth and changing orbit around the Sun require velocity changes of several kilometres per second, and journeys last from days (to the Moon) to more than a decade (to the outer planets).
- **Launch windows** dictated by planetary alignment, which for Mars open only once every 26 months.
- **Distance**: radio signals take up to hours to arrive, so spacecraft must operate autonomously and data rates are limited.
- **Power and temperature**: sunlight falls with the square of the distance from the Sun, and spacecraft experience extremes from the heat near Mercury or the Sun to the cold of the outer Solar System.
- **Environment**: intense radiation at Jupiter, dust near comets, unknown surfaces at landing sites.
- **No second chance**: a missed orbit insertion or a failed landing usually ends the mission.

Missions are commonly classified as **flybys**, **orbiters**, **landers**, **rovers** and **sample-return** missions (Chapters 25–29), and grouped by agencies into cost classes. NASA's **Discovery** programme (cost cap around $500–600 million) and **New Frontiers** programme (around $1 billion) compete missions among scientists, while **flagship** missions such as Cassini, Perseverance and Europa Clipper cost several billion dollars. ESA's Science Programme distinguishes small, medium and large missions; China's **Tianwen** and **Chang'e** series, JAXA's sample-return missions and ISRO's Mars and lunar missions have made deep-space exploration a truly international enterprise. The two Voyager spacecraft, launched in 1977, are still returning data from interstellar space; on 18 November 2026 Voyager 1 reaches one light-day — about 26 billion km — from the Earth.

## Interplanetary Trajectories

### Escape and Hyperbolic Excess Speed

Trajectory design uses the **patched-conic** approximation (Chapter 3): near each body, the spacecraft follows a conic section governed by that body alone; between bodies, it follows an ellipse around the Sun. The energy with which a spacecraft leaves the Earth is described by its **hyperbolic excess speed** $v_\infty$ — its speed relative to the Earth after escape — or by the **characteristic energy** $C_3 = v_\infty^2$, the standard way launch-vehicle performance is quoted for interplanetary missions. The velocity change needed to depart from a circular parking orbit of radius $r$ is

$$\Delta v = \sqrt{v_{esc}^2 + v_\infty^2} - v_{circ}, \qquad v_{esc} = \sqrt{\frac{2\mu}{r}},\; v_{circ}=\sqrt{\frac{\mu}{r}}$$

which, by the **Oberth effect**, is much less than $v_\infty$ added to the escape speed separately: a burn deep in a gravity well, at high speed, gains the most energy.

### Hohmann Transfers and the Cost of Getting There

The minimum-energy transfer between two circular coplanar orbits is the **Hohmann transfer** (Chapter 3), an ellipse tangent to both orbits (@fig:hohmannplanets). @fig:c3planets compares the launch energies and flight times: Venus and Mars are relatively cheap (C3 of about 6–9 km²/s²), Mercury surprisingly expensive — a spacecraft must shed the Earth's orbital speed to fall towards the Sun — and the outer planets require C3 values of 80–140 km²/s² and flight times of years to decades. Only a few launch vehicles can deliver useful masses at such energies, which is why outer-planet missions rely on gravity assists.

![Hohmann transfer ellipses from the Earth to Venus, Mars and Jupiter, drawn to scale.](figures/out/ch24_orbits.svg){#fig:hohmannplanets width=72%}

![Launch energy (C3) and flight time for Hohmann transfers from the Earth to each planet.](figures/out/ch24_c3planets.svg){#fig:c3planets width=88%}

### Launch Windows

A transfer works only if the target planet arrives at the end of the transfer at the right moment, so launches must take place when the planets are in the right relative positions. These **launch opportunities** recur at the **synodic period** of the two planets: about 584 days for Venus, 780 days (26 months) for Mars, and about 13 months for Jupiter and the more distant planets (@tbl:synodic). Each opportunity is a **launch period** of a few weeks, with a daily **launch window** of minutes to hours determined by the launch site and parking orbit.

| Planet | Synodic period with Earth | Hohmann transfer time | Typical C3 (km²/s²) |
|---|---|---|---|
| Mercury | 116 days | 3.5 months | ≈ 57 (direct; real missions use Venus and Mercury flybys) |
| Venus | 584 days (1.6 yr) | 4.8 months | ≈ 6–10 |
| Mars | 780 days (2.1 yr) | 8.5 months | ≈ 8–17 depending on opportunity |
| Jupiter | 399 days (1.1 yr) | 2.7 years | ≈ 77–85 |
| Saturn | 378 days (1.04 yr) | 6.0 years | ≈ 105–110 |

: Synodic periods and transfer characteristics. {#tbl:synodic}

Because planetary orbits are elliptical and inclined, the real transfers are found by solving **Lambert's problem** (Chapter 3) for many combinations of launch and arrival dates and plotting the results as a "porkchop plot" (@fig:porkchop in Chapter 3). Repeating this computation for each Mars opportunity (@fig:marswindows) shows that their quality varies over a cycle of about 15–17 years, as Mars's eccentric orbit brings it closer to or farther from the Earth at opposition: the 2033 opportunity requires the least energy in the next decade, while 2037 is among the most demanding. Transfers shorter than half an orbit are called **Type I**, longer ones **Type II**.

![Minimum launch energy and the corresponding arrival speed for each Mars launch opportunity from 2026 to 2041, computed with a Lambert solver (flight times limited to 130–340 days).](figures/out/ch24_marswindows.svg){#fig:marswindows width=94%}

## Gravity Assists

### Borrowing Momentum from Planets

A spacecraft flying past a planet enters and leaves the planet's sphere of influence with the same speed relative to the planet, but its direction is turned through an angle that depends on how close it passes and how fast it is moving (@fig:gaturn). Seen from the Sun, adding the planet's orbital velocity to this rotated relative velocity changes the spacecraft's heliocentric speed and direction — a **gravity assist** that can add or remove several kilometres per second without using propellant (Chapter 3, @fig:gravityassist). Massive planets such as Jupiter can turn a spacecraft by large angles even at high speeds; small bodies like Mars or the Moon give only modest changes.

![Maximum turn angle of a spacecraft's velocity during a flyby, as a function of the approach speed v∞, for different bodies.](figures/out/ch24_gaturn.svg){#fig:gaturn width=84%}

### Gravity Assists in Practice

Gravity assists have made the exploration of the Solar System possible:

- **Mariner 10** (1973) used Venus to reach Mercury — the first gravity assist.
- **Voyager 1 and 2** (1977) exploited a rare alignment of the outer planets, recurring only every 175 years, to tour Jupiter, Saturn, Uranus and Neptune.
- **Galileo** (1989) and **Cassini** (1997) used Venus and Earth flybys (VEEGA and VVEJGA trajectories) because their launch vehicles could not send them directly to Jupiter or Saturn.
- **MESSENGER** (2004) used six flybys to slow down enough to orbit Mercury; **BepiColombo** (2018) used nine — one of Earth, two of Venus and six of Mercury — before entering orbit around Mercury in November 2026.
- **Parker Solar Probe** used seven Venus flybys to lower its perihelion to 6.1 million km.
- ESA's **JUICE** (2023) performed the first-ever lunar–Earth double flyby in 2024 and a Venus flyby in 2025, with further Earth flybys in 2026 and 2029 before arriving at Jupiter in 2031; NASA's **Europa Clipper** (2024) flew past Mars in March 2025 and returns to Earth in December 2026 on its way to Jupiter in 2030 (@fig:clippertimeline).

Once in orbit around a giant planet, missions use repeated flybys of its moons to reshape their orbits — Cassini made more than 120 flybys of Titan, and Europa Clipper will make about 49 flybys of Europa. Designing such **tours** is a combinatorial problem solved with tools such as Tisserand graphs and global optimisation.

## Low-Thrust Trajectories

**Electric propulsion** (Chapter 6) produces only millinewtons to a fraction of a newton of thrust, but with exhaust velocities 5–10 times higher than chemical rockets, it can provide total velocity changes of 10 km/s or more with modest propellant (@fig:lowthrust). Instead of short impulsive burns, the engine operates for months or years, spiralling the spacecraft gradually from one orbit to another.

![Propellant mass fraction versus mission Δv for chemical and electric propulsion.](figures/out/ch24_lowthrust.svg){#fig:lowthrust width=84%}

NASA's **Deep Space 1** (1998) demonstrated ion propulsion; JAXA's **Hayabusa** (2003) used it for the first asteroid sample return; NASA's **Dawn** (2007) used three ion engines to orbit two different bodies — Vesta and Ceres — achieving a record total Δv of about 11 km/s (@fig:dawn). ESA–JAXA's BepiColombo, NASA's Psyche (launched in 2023 with Hall-effect thrusters, flying past Mars in May 2026 on its way to the metal-rich asteroid Psyche in 2029) and many smaller missions use electric propulsion. Low-thrust trajectories are designed with numerical optimisation methods that balance thrust direction and timing against propellant use and flight time.

![Artist's impression of NASA's Dawn spacecraft approaching Ceres, its xenon ion engine glowing blue. Dawn's ion engines provided about 11 km/s of velocity change over its mission.](figures/photos/ch24_dawn.jpg){#fig:dawn width=70%}

## Arrival: Orbit Insertion, Aerobraking and Aerocapture

A spacecraft arrives at its target on a hyperbolic trajectory and must slow down to be captured. **Orbit insertion** burns of 0.5–1.5 km/s are typical at Mars and Venus and can exceed 2 km/s at Mercury or for low orbits at the giant planets; they must be executed at precisely the right moment, often during a communication blackout behind the planet, entirely autonomously. Failures have ended several missions: Mars Observer (1993) was lost just before insertion, and Mars Climate Orbiter (1999) flew too deep into the atmosphere because one team used imperial units and another metric units in navigation software — the most famous units error in engineering history.

To save propellant, many Mars and Venus orbiters first enter a large elliptical orbit and then use **aerobraking**: dipping repeatedly into the upper atmosphere at periapsis, they lose a little energy on each pass until the orbit is circularised. Mars Global Surveyor, Mars Odyssey, Mars Reconnaissance Orbiter, ESA's Trace Gas Orbiter and Venus Express all aerobraked; it takes months and careful monitoring of atmospheric density. **Aerocapture** — a single pass deep through the atmosphere inside a heat shield to go directly from a hyperbolic to an elliptical orbit — could save even more mass, especially at Uranus and Neptune, but has not yet been flown.

## Cislunar Space and Libration Points

Missions near the Moon and the Sun–Earth Lagrange points use the dynamics of the three-body problem (Chapter 3). The Sun–Earth **L1** and **L2** points, 1.5 million km from the Earth, host solar observatories (SOHO, DSCOVR, Aditya-L1) and astronomical telescopes (Gaia, JWST, Euclid, Roman) in large **halo** or **Lissajous** orbits around the unstable equilibrium points, requiring small station-keeping manoeuvres every few weeks.

Around the Moon, new families of orbits have become important (@fig:cislunar). The **near-rectilinear halo orbit (NRHO)**, a highly elongated halo orbit around the Earth–Moon L2 point with a period of about 6.5 days, was selected for the planned Gateway station and tested by the small CAPSTONE spacecraft in 2022; it is stable, almost always in view of the Earth, and accessible from both the Earth and the lunar surface (though Gateway itself was paused in 2026). Artemis I's Orion flew in a **distant retrograde orbit (DRO)**, a very stable orbit around the Moon. **Low-energy (ballistic) transfers**, which loop out to about 1.5 million km and exploit the Sun's gravity, take three to four months instead of three days but save hundreds of metres per second of Δv; they were used by Korea's Danuri, CAPSTONE, Japan's SLIM and ispace's Hakuto-R commercial landers.

![Orbits and transfers in cislunar space (schematic, not to scale).](figures/out/ch24_cislunar.svg){#fig:cislunar width=94%}

## Navigating in Deep Space

### Radiometric Tracking

Deep-space navigation is mostly done from the ground. Large antennas of NASA's **Deep Space Network (DSN)** — complexes at Goldstone (California), Madrid and Canberra, spaced about 120° apart in longitude so that every spacecraft is always in view of one — measure:

- **range**, by timing a coded signal sent to the spacecraft and returned by its transponder, to an accuracy of about 1 m;
- **range-rate**, from the Doppler shift of the carrier, to about 0.05 mm/s;
- **angular position**, by **delta differential one-way ranging (ΔDOR)** (@fig:ddor): two widely separated stations observe the spacecraft and then a quasar close to it in the sky; the difference in arrival times gives the spacecraft's direction with an accuracy of about one nanoradian — about 200 m at the distance of Mars.

Navigators combine these measurements with dynamical models — gravity of all relevant bodies, solar radiation pressure, thruster firings, even the thermal recoil of radiation from the spacecraft — in an **orbit determination** filter, and design **trajectory correction manoeuvres** to keep the spacecraft on course. Errors at a target are expressed in the **B-plane** (@fig:bplane), the plane through the target body perpendicular to the incoming asymptote; delivering a Mars lander to its entry corridor requires B-plane accuracy of a few kilometres.

![Delta-DOR: comparing the arrival of a spacecraft's signal at two distant stations with that of a nearby quasar gives a very precise direction.](figures/out/ch24_ddor.svg){#fig:ddor width=92%}

![The B-plane used to target planetary flybys, orbit insertion and atmospheric entry.](figures/out/ch24_bplane.svg){#fig:bplane width=90%}

### Optical and Autonomous Navigation

Near a target, cameras provide **optical navigation**: images of a moon or asteroid against background stars give its direction relative to the spacecraft with high precision. Autonomous navigation systems close the loop on board: NASA's **AutoNav** (Deep Space 1, Deep Impact, Stardust) and the **SMART Nav** system that guided DART into Dimorphos in 2022 identified their targets in images and steered without help from the ground in the final hours. Landing systems use **terrain-relative navigation** (Chapter 27). Experimental techniques include navigation using X-ray pulsars as natural clocks (demonstrated by NASA's SEXTANT on the ISS) and onboard atomic clocks that enable one-way ranging (Chapter 18).

## Communications, Power and Thermal Design

### Talking Across the Solar System

Light takes 1.3 seconds to reach the Moon, between 3 and 22 minutes to reach Mars, and almost a day to reach Voyager 1 (@fig:lighttime). Spacecraft therefore carry out pre-programmed sequences autonomously and protect themselves with fault-protection software that can put them in a safe mode and wait for instructions. Data rates fall with the square of distance (Chapter 7): a Mars orbiter can return several megabits per second, while Voyager 1 sends about 160 bit/s. The DSN's 70 m antennas (@fig:dsn) and arrays of 34 m antennas, ESA's ESTRACK 35 m deep-space antennas, and Chinese, Indian and Japanese deep-space networks support all missions; NASA's Deep Space Optical Communications experiment on Psyche demonstrated laser data rates of hundreds of megabits per second from tens of millions of kilometres.

![One-way light time to destinations across the Solar System.](figures/out/ch24_lighttime.svg){#fig:lighttime width=88%}

![The 70 m antenna DSS-43 at the Canberra Deep Space Communication Complex in Australia — the only antenna able to send commands to Voyager 2, which is below the Earth's equatorial plane.](figures/photos/ch24_dsn.jpg){#fig:dsn width=70%}

### Power

At Jupiter, sunlight is 27 times weaker than at the Earth; at Saturn, 90 times (@fig:solarpower). Missions as far as Jupiter can use very large solar arrays combined with efficient cells that work at low intensity and low temperature: Juno's three arrays span about 20 m and produce about 500 W at Jupiter; Europa Clipper's span 30.5 m; ESA's JUICE carries 85 m² of cells; and NASA's Lucy, with two 7.3 m circular arrays, reaches 5.7 AU. Beyond about Jupiter, missions need **radioisotope power**: radioisotope thermoelectric generators (RTGs) convert the heat of plutonium-238 decay into about 100–300 W of electricity for decades. Voyager, Galileo, Cassini, New Horizons, Curiosity and Perseverance all use RTGs; the supply of plutonium-238 — whose US production restarted in the 2010s — limits how many such missions can fly.

![Solar irradiance as a function of distance from the Sun. Large solar arrays have powered missions out to Jupiter; beyond, radioisotope power is required.](figures/out/ch24_power.svg){#fig:solarpower width=86%}

::: figrow
![Europa Clipper — NASA's largest planetary spacecraft, with solar arrays spanning 30.5 m — being unpacked at Kennedy Space Center in May 2024 before its launch in October 2024.](figures/photos/ch24_clipper.jpg){#fig:clippercraft}

![One of Lucy's two 7.3 m circular solar arrays being deployed in a test in August 2021. Lucy is visiting Trojan asteroids at the distance of Jupiter's orbit using solar power.](figures/photos/ch24_lucy.jpg){#fig:lucy}
:::

### Thermal Extremes and Radiation

Thermal design must cope with radiation intensities from many times the Earth's value (Parker Solar Probe's heat shield reaches about 1 400 °C) to almost nothing in the outer Solar System, where spacecraft rely on radioisotope heater units and electrical heaters to keep propellant and batteries warm. At Jupiter, radiation is so intense that Juno and Europa Clipper protect their electronics inside **radiation vaults** with thick titanium or aluminium walls, and their orbits are designed to limit time in the worst regions.

## Planetary Protection

Spacecraft must not contaminate other worlds with terrestrial organisms that could confuse the search for life or alter habitable environments, and samples returned to Earth must not pose a risk to the biosphere. The **COSPAR planetary protection policy**, implementing Article IX of the Outer Space Treaty, assigns missions to categories (@tbl:planetaryprotection).

| Category | Mission type and target | Requirements |
|---|---|---|
| I | Any mission to bodies of no interest for chemical evolution or life (e.g. Mercury, undifferentiated asteroids) | None |
| II | Missions to bodies of significant interest but with remote chance of contamination (Venus, the Moon, comets, Jupiter, Saturn, Titan) | Documentation and impact-avoidance analysis |
| III | Flybys and orbiters of bodies with a significant chance of contamination (Mars, Europa, Enceladus) | Limits on impact probability or bioburden |
| IV | Landers and probes to these bodies | Strict cleaning and sterilisation; IVc for special regions (e.g. Martian ice or brines) |
| V | Sample return to Earth: "unrestricted" (Moon, asteroid Ryugu) or "restricted" (Mars, Europa) | Restricted: break the chain of contact; containment and biohazard testing |

: COSPAR planetary-protection categories (simplified). {#tbl:planetaryprotection}

The Viking landers of 1976 were heat-sterilised as complete spacecraft; today's Mars landers are cleaned to limits of a few hundred thousand bacterial spores, and spacecraft at the end of their missions near Jupiter and Saturn — Galileo and Cassini — were deliberately plunged into the planets to avoid any possibility of crashing on Europa or Enceladus.

## From Idea to Arrival: The Mission Life Cycle

Deep-space missions follow the project life cycle of Chapter 4, but over unusually long timescales. Europa Clipper illustrates this (@fig:clippertimeline): studies began more than a decade before its launch in October 2024; its cruise includes Mars (2025) and Earth (2026) gravity assists; and its science phase at Jupiter, beginning in 2030, will last about four years. Its life-cycle cost is about $5 billion.

![The life cycle of NASA's Europa Clipper mission, from concept studies to the end of its prime science phase.](figures/out/ch24_clipper.svg){#fig:clippertimeline width=96%}

## The Deep-Space Fleet in 2026

| Destination | Active or en-route missions (selected) |
|---|---|
| Moon | LRO (USA), Chandrayaan-2 orbiter (India), Danuri (Korea), Chang'e-4 and Queqiao relays (China), commercial and Artemis missions (Chapters 25–27) |
| Sun and heliosphere | Parker Solar Probe, Solar Orbiter, SOHO, IMAP, Aditya-L1, PUNCH |
| Mercury | BepiColombo (ESA/JAXA), Mercury orbit insertion November 2026 |
| Mars | Mars Odyssey, MRO, MAVEN, Mars Express, ExoMars TGO, Tianwen-1 orbiter, Hope; Curiosity and Perseverance rovers; ESCAPADE twin smallsats en route; MMX launching to Phobos in October 2026 |
| Jupiter | Juno (in orbit since 2016; extended operations uncertain after 2025); JUICE (arrival 2031) and Europa Clipper (arrival 2030) en route |
| Asteroids and comets | Lucy (Trojans), Psyche (arrival 2029), Hera (Didymos–Dimorphos, arrival November 2026), OSIRIS-APEX (Apophis, 2029), Hayabusa2 extended mission (2031), Tianwen-2 (Kamoʻoalewa, sample return ≈ 2027) |
| Outer Solar System and beyond | New Horizons (Kuiper Belt), Voyager 1 and 2 (interstellar space) |

: Selected deep-space missions in operation or en route in October 2026. {#tbl:deepfleet}

::: example
**Example: the Δv budget of a 2026 Mars orbiter**

From @fig:marswindows, the best 2026 opportunity requires C3 ≈ 9.2 km²/s² (v∞ ≈ 3.0 km/s) with launch on about 29 October 2026 and arrival with v∞ ≈ 2.7 km/s.

1. *Departure* from a 300 km parking orbit ($r$ = 6 671 km): $v_{circ}$ = 7.73 km/s, $v_{esc}$ = 10.93 km/s; $v_p = \sqrt{10.93^2 + 9.2} = 11.34$ km/s, so Δv ≈ 3.61 km/s — normally provided by the launch vehicle's upper stage.
2. *Trajectory corrections* during cruise: typically 20–50 m/s.
3. *Mars orbit insertion* at 250 km altitude ($r$ = 3 640 km, μ = 42 828 km³/s²): the hyperbolic periapsis speed is $\sqrt{2\mu/r + v_\infty^2} = \sqrt{23.53 + 7.13} = 5.54$ km/s. To capture into an elliptical orbit with a period of one Martian day (a = 20 450 km), the periapsis speed must be $\sqrt{\mu(2/r - 1/a)} = 4.63$ km/s, so the insertion burn is about 0.91 km/s.
4. *Aerobraking* then lowers the apoapsis to a low circular science orbit over several months, saving about 1.2 km/s compared with doing the same with the engine.

With a bipropellant engine of 320 s specific impulse, the 0.95 km/s of spacecraft-provided Δv requires propellant equal to about 26 % of the spacecraft's mass at launch.
:::

::: ai
**AI in deep-space mission design**

Machine learning and global optimisation are accelerating trajectory design (searching enormous spaces of gravity-assist sequences and low-thrust profiles), autonomous navigation and fault protection, scheduling of DSN antennas, and the analysis of returned data. Future spacecraft will need far greater on-board autonomy to explore distant worlds with hours of communication delay (Chapters 45 and 46).
:::

::: key
**Key takeaways**

- Deep-space missions are constrained by energy, launch windows, distance, power, environment and the need for autonomy.
- Departure energy is expressed as C3 = v∞²; Hohmann transfers to Venus and Mars need C3 ≈ 6–10 km²/s², to the outer planets 80–140 km²/s².
- Launch opportunities recur at synodic periods (26 months for Mars); their quality varies with orbital geometry — 2033 is the best Mars window of the next decade.
- Gravity assists and low-thrust electric propulsion make otherwise impossible missions feasible; BepiColombo needed nine flybys to reach Mercury, Dawn achieved 11 km/s of Δv with ion engines.
- Orbit insertion, aerobraking and (future) aerocapture capture spacecraft at their targets; NRHOs, DROs and low-energy transfers are reshaping cislunar operations.
- Navigation relies on DSN range, Doppler and ΔDOR plus optical and autonomous navigation; light time ranges from seconds (Moon) to a day (Voyager 1).
- Solar power works to about Jupiter; beyond, RTGs are needed. Radiation vaults protect electronics at Jupiter.
- Planetary protection categories govern cleanliness and sample return; flagship missions take 15–20 years from concept to science.
:::

::: questions
**Review questions**

1. List six constraints that make deep-space missions harder than Earth-orbit missions.
2. Calculate the Δv needed to depart from a 200 km circular parking orbit with a C3 of 10 km²/s².
3. Why do Mars launch opportunities recur every 26 months, and why are some windows better than others?
4. Explain how a gravity assist can increase a spacecraft's speed relative to the Sun without violating energy conservation.
5. How did Dawn achieve a total Δv of about 11 km/s, and why would that have been impossible with chemical propulsion?
6. Compare orbit insertion by propulsive burn, aerobraking and aerocapture.
7. Describe range, Doppler and ΔDOR tracking, and the information each provides.
8. Why is solar power practical out to about Jupiter but not beyond? What do missions to the outer Solar System use instead?
:::
