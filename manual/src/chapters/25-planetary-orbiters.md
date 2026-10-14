---
title: Planetary Orbiters
hero: ch25
abstract: Orbiters are the workhorses of planetary exploration. Circling a world for years, they map its whole surface, probe beneath it with radar, weigh its interior through its gravity field, sample its atmosphere and magnetic environment, and relay the data of landers and rovers back to Earth. This chapter explains how orbits are designed around bodies as different as the Moon, Mars, Venus, Mercury, the giant planets and small asteroids, describes the instruments that orbiters carry, and reviews the orbiter missions — from Luna 10 and Mariner 9 to Juno, Cassini and BepiColombo — that have transformed our knowledge of the Solar System, including those operating in 2026.
---

## Why Orbit?

A flyby gives a few hours of close observation; an orbiter can observe a world for years, through changing seasons and lighting, at resolutions limited only by its instruments and its orbit. Orbiters provide:

- **global mapping** of surface composition, topography, geology and temperature;
- **long-term monitoring** of atmospheres, weather, seasonal ice caps and active processes such as dust storms, volcanism and geysers;
- **interior structure**, through precise measurements of the gravity and magnetic fields;
- **reconnaissance** of landing sites and safety;
- **communication relays** for surface missions.

| Body | First orbiter | Year | Notes |
|---|---|---|---|
| Moon | Luna 10 (USSR) | 1966 | First spacecraft to orbit another body |
| Mars | Mariner 9 (USA) | 1971 | First to orbit another planet; mapped Mars after a global dust storm |
| Venus | Venera 9 (USSR) | 1975 | Orbiter of the first lander mission to return surface images |
| Jupiter | Galileo (USA) | 1995 | With an atmospheric entry probe |
| Asteroid | NEAR Shoemaker (USA) | 2000 | Orbited and then landed on Eros |
| Saturn | Cassini (USA/Europe/Italy) | 2004 | Carried ESA's Huygens Titan probe |
| Mercury | MESSENGER (USA) | 2011 | Found water ice in permanently shadowed polar craters |
| Dwarf planets | Dawn (USA) | 2011, 2015 | Orbited Vesta and then Ceres |
| Comet | Rosetta (Europe) | 2014 | Deployed the Philae lander on 67P/Churyumov–Gerasimenko |

: First orbiters of Solar System bodies. {#tbl:firstorbiters}

## Designing Orbits Around Other Worlds

### Gravity Fields and Perturbations

The basic orbital mechanics are the same everywhere (Chapter 3), but each body's mass, size, rotation, shape and gravity field produce different orbits (@fig:planetperiods). A low orbit around the Moon takes about two hours; around Mars about 1 hour 50 minutes; around Earth about 90 minutes.

![Orbital period as a function of altitude around the Moon, Mercury, Mars, Venus and the Earth.](figures/out/ch25_periods.svg){#fig:planetperiods width=84%}

Irregularities in the gravity field strongly affect low orbits:

- The **Moon** has concentrations of mass under its large impact basins (**mascons**), discovered by tracking Lunar Orbiter spacecraft in 1968. They perturb low orbits so strongly that most low lunar orbits crash within months unless maintained. Only certain **frozen orbits**, at inclinations of about 27°, 50°, 76° and 86°, are naturally stable for long periods. NASA's **GRAIL** twin spacecraft (2012) measured the lunar gravity field with unprecedented precision by tracking the distance between them, revealing the structure of the lunar crust.
- **Mars** has a large equatorial bulge ($J_2$ about twice the Earth's), which allows **sun-synchronous orbits** that pass over each point at the same local time (@fig:marssso). Because Mars's year is longer, the required precession is slower, and its sun-synchronous orbits are nearly polar (about 93°). Most Mars orbiters since Mars Global Surveyor use them.
- **Venus** rotates once every 243 days (backwards) and has almost no bulge, so sun-synchronous orbits are impossible; a near-polar orbit lets the planet rotate slowly beneath it, and NASA's **Magellan** (1990–1994) mapped 98 % of the surface with radar over three Venusian days (@fig:venusmap).
- **Small bodies** — asteroids and comet nuclei — have such weak, irregular gravity that orbits are slow (hours to weeks) and strongly perturbed by solar radiation pressure and outgassing. OSIRIS-REx orbited the 500 m asteroid Bennu at about 1 km — the smallest body ever orbited.

![Sun-synchronous inclination as a function of altitude for Mars and the Earth.](figures/out/ch25_sso.svg){#fig:marssso width=84%}

### Thermal and Radiation Constraints

Orbits are also shaped by the environment. At **Mercury**, sunlight is up to 10 times more intense than at the Earth and the dayside surface reaches 430 °C, radiating heat back at the spacecraft; MESSENGER flew a highly elliptical orbit to limit time over the hot surface, shaded behind a ceramic-cloth sunshade, and BepiColombo's orbiters use high-temperature multilayer insulation and radiators that view away from the planet. At **Jupiter**, the radiation belts dominate orbit design (Chapter 23): Juno's elongated polar orbit (@fig:junoorbit) dives beneath the belts at each perijove, minimising the dose per orbit.

![Juno's 53-day polar orbit passes between Jupiter's atmosphere and its most intense radiation belts at each close approach (schematic).](figures/out/ch25_juno.svg){#fig:junoorbit width=94%}

### Moon Tours

At the giant planets, orbiters use repeated flybys of the large moons to change their orbits (Chapter 24). Cassini's 13-year tour of the Saturn system included more than 120 Titan flybys and 23 close Enceladus flybys; it ended with the **Grand Finale** of 2017 — 22 orbits through the 2 000 km gap between the rings and the planet's atmosphere, followed by a deliberate plunge into Saturn to protect Enceladus and Titan from contamination (@fig:finale, @fig:finaleart).

![Cassini's Grand Finale: 22 orbits through the gap between Saturn's rings and atmosphere, followed by the final plunge (schematic).](figures/out/ch25_finale.svg){#fig:finale width=90%}

![Artist's impression of Cassini diving between Saturn and its rings during the Grand Finale in 2017.](figures/photos/ch25_finale.jpg){#fig:finaleart width=80%}

## Getting Into Orbit

### The Orbit-Insertion Burn

A spacecraft arrives at a planet on a hyperbola, moving faster than the local escape speed. To be captured, it must fire its main engine near closest approach and slow down by

$$\Delta v_{\text{insertion}} = \sqrt{v_\infty^2 + \frac{2\mu}{r_p}} - v_{\text{capture}},$$

where $v_\infty$ is the arrival speed relative to the planet (Chapter 24), $r_p$ is the periapsis radius and $v_{\text{capture}}$ is the periapsis speed on the desired capture orbit. Two facts dominate the design (@fig:insertion):

- **Capturing into a long ellipse is much cheaper than capturing into a low circular orbit.** At Mars, the difference is more than 1 km/s. Most orbiters therefore first enter a long, elliptical orbit and lower it later.
- **Deep gravity wells make capture cheap.** Because the burn is made where the spacecraft is moving fastest (the Oberth effect), Jupiter and Saturn can be entered for a few hundred metres per second — Juno's Jupiter orbit insertion in 2016 needed about 542 m/s (a 35-minute burn) and Cassini's Saturn insertion in 2004 about 626 m/s (96 minutes). Mercury, with a shallow well deep inside the Sun's, is the hardest planet to orbit, which is why MESSENGER and BepiColombo needed six or more planetary flybys to reduce their arrival speed.

![Orbit-insertion Δv. (a) At Mars, capturing into a long ellipse rather than a low circular orbit saves more than 1 km/s. (b) Capture into a long ellipse costs least at the giant planets with their deep gravity wells.](figures/out/ch25_insertion.svg){#fig:insertion width=96%}

Orbit insertion is a **critical event**: it happens at a fixed time that cannot be postponed, often while the spacecraft is behind the planet and out of contact, so it must be fully autonomous, with fault protection that keeps the burn going through most failures. Losses have shaped today's practice. **Mars Observer** fell silent in 1993 just before insertion, probably after a propellant line ruptured while its tanks were being pressurised. **Mars Climate Orbiter** was lost in 1999 because ground software reported thruster impulse in pound-force seconds while the navigation software expected newton-seconds; the error accumulated over the cruise, and the spacecraft passed about 57 km above the surface instead of the planned 140–150 km. Japan's **Akatsuki** failed to enter Venus orbit in 2010 when its main engine was damaged, but engineers kept it alive for five years in a solar orbit and inserted it in December 2015 using only its small attitude thrusters — one of the great recoveries in spaceflight.

### Aerobraking and Aerocapture

After capture, the orbit must be lowered from a long ellipse to the low science orbit. Doing this with the engine at Mars would cost another 1.2 km/s, so orbiters at Mars and Venus use **aerobraking**: the spacecraft lowers its periapsis to about 100–130 km, where each pass through the thin upper atmosphere removes a few metres per second of velocity, gradually shrinking the apoapsis (@fig:aerobrake). The solar arrays act as a drag brake. Ground teams (and increasingly onboard software) manage the **aerobraking corridor**: small burns at apoapsis raise or lower the periapsis to keep dynamic pressure and heating within limits, because the density of the upper atmosphere can change by 30 % or more from one orbit to the next during dust storms. Aerobraking has three phases: the **walk-in** (periapsis lowered step by step into the atmosphere), the **main phase** (hundreds of drag passes) and the **walk-out** (periapsis raised out of the atmosphere when the target apoapsis is reached).

| Mission | Planet | Years | Duration and notes |
|---|---|---|---|
| Magellan | Venus | 1993 | First aerobraking, used to circularise the orbit for gravity mapping |
| Mars Global Surveyor | Mars | 1997–1999 | About 16 months; slowed by a damaged solar-array hinge |
| Mars Odyssey | Mars | 2001–2002 | About 3 months |
| Mars Reconnaissance Orbiter | Mars | 2006 | 426 drag passes in about 5 months; from 35-hour to 2-hour orbit |
| Venus Express | Venus | 2014 | Experimental campaign at the end of the mission |
| ExoMars Trace Gas Orbiter | Mars | 2017–2018 | About 11 months, interrupted by solar conjunction |

: Aerobraking campaigns. {#tbl:aerobraking}

![Aerobraking at Mars (illustrative model of an MRO-like orbiter). (a) Hundreds of drag passes shrink the orbit from a 35-hour ellipse to the 2-hour science orbit. (b) Each pass removes only a few metres per second; together they provide about 1.2 km/s — the equivalent of hundreds of kilograms of propellant.](figures/out/ch25_aerobrake.svg){#fig:aerobrake width=96%}

**Aerocapture** goes further: the spacecraft, protected by an aeroshell, makes a single deep pass through the atmosphere to slow from hyperbolic speed directly into orbit, using lift to steer to the right exit conditions. It has never been flown, but studies show it could reduce the mass of orbiters bound for Uranus, Neptune or Titan by a third or more, and it is a candidate technology for a future Uranus orbiter (Chapter 42).

::: example
**Example: capturing at Mars**

An orbiter of 2 000 kg arrives at Mars from the 2026 launch window with $v_\infty$ = 2.67 km/s (Chapter 24). Its periapsis is 300 km (radius 3 696 km); its engine has a specific impulse of 320 s.

1. Speed at periapsis on the arrival hyperbola: $\sqrt{2.67^2 + 2 × 42\,828/3\,696}$ = 5.50 km/s.
2. **Option A — direct capture into a 300 km circular orbit** (speed $\sqrt{\mu/r}$ = 3.40 km/s): Δv = 2.10 km/s. By the rocket equation, $1 - e^{-2\,100/(320 × 9.81)}$ = 49 % of the arrival mass — 976 kg — would be propellant.
3. **Option B — capture into a 35-hour ellipse** (semi-major axis 25 825 km, apoapsis altitude about 44 600 km, periapsis speed 4.64 km/s): Δv = 0.87 km/s, using 24 % of the mass — 482 kg.
4. Lowering the 35-hour orbit to the 300 km circle with the engine would cost another 1.23 km/s; by aerobraking, it costs only a few tens of metres per second for corridor control and the final periapsis raise.
5. Option B plus aerobraking saves about 450 kg — almost a quarter of the arrival mass — at the cost of about 5 months of intensive operations before the science mission starts.
:::

## What Orbiters Carry

### Instruments

Planetary orbiters carry many of the instrument types described in Chapter 12, adapted to their targets (@tbl:orbiterinstruments).

| Instrument type | Measures | Examples |
|---|---|---|
| High-resolution cameras | Morphology, geology, landing-site hazards | HiRISE (MRO, 25–30 cm/pixel), LROC (LRO, 0.5 m), CaSSIS (TGO), HiRIC (Tianwen-1) |
| Context and stereo cameras | Regional mapping, topography | CTX (MRO, 6 m), HRSC (Mars Express), Kaguya Terrain Camera |
| Visible–infrared imaging spectrometers | Minerals, ices, hydrated materials | CRISM (MRO), OMEGA (Mars Express), M3 (Chandrayaan-1), MISE (Europa Clipper) |
| Thermal infrared radiometers | Surface temperature, thermal inertia, rock abundance | THEMIS (Odyssey), Diviner (LRO) |
| Gamma-ray and neutron spectrometers | Elemental composition, subsurface hydrogen (ice) | Mars Odyssey GRS, Lunar Prospector, MESSENGER |
| Radar sounders | Subsurface layers, ice, Europa's ice shell | MARSIS (Mars Express), SHARAD (MRO), REASON (Europa Clipper), RIME (JUICE) |
| Laser and radar altimeters | Topography, shape, tides | MOLA (MGS), LOLA (LRO), BELA (BepiColombo), GALA (JUICE) |
| Radio science / gravity | Interior structure, atmospheres by radio occultation | GRAIL, Juno, all orbiters' telecom systems |
| Magnetometers, particles and fields | Magnetic fields, plasma, induced fields from oceans | Galileo, Juno, MAVEN, Europa Clipper |
| Atmospheric spectrometers | Trace gases, winds, escape | TGO's NOMAD and ACS, MAVEN's IUVS, Juno's MWR |

: Typical planetary orbiter instruments. {#tbl:orbiterinstruments}

The **High Resolution Imaging Science Experiment (HiRISE)** on NASA's Mars Reconnaissance Orbiter, with a 0.5 m telescope, resolves objects about a metre across from 300 km. It has photographed landers descending under their parachutes (@fig:hiriseedl), tracked the movement of dunes and avalanches, and certified the safety of every NASA landing site since 2008.

![HiRISE on Mars Reconnaissance Orbiter photographed the Perseverance rover hanging under its parachute during its descent to Jezero crater on 18 February 2021, while travelling at about 3 km/s relative to the rover.](figures/photos/ch25_hiriseedl.jpg){#fig:hiriseedl width=92%}

**Radar sounders** operating at a few megahertz penetrate hundreds of metres to kilometres into ice and dry rock (@fig:sounder). On Mars, they have mapped the layered polar caps, buried glaciers at mid-latitudes and the thickness of ice deposits — essential information for future human missions seeking water.

![Principle of orbital radar sounding of subsurface layers.](figures/out/ch25_sounder.svg){#fig:sounder width=90%}

### Relays for Surface Missions

Landers and rovers have small antennas and limited power, and they can talk directly to the Earth only at low data rates. Orbiters overhead act as **relays** (@fig:relay): a rover transmits to an orbiter at UHF during a pass of about ten minutes at up to about 2 Mbit/s, and the orbiter forwards the data to the Deep Space Network over its high-gain antenna. Most of the data from NASA's Mars rovers have been relayed this way, mainly by Mars Odyssey and MRO, with MAVEN and ESA's Trace Gas Orbiter; Chinese missions use Tianwen-1's orbiter and, on the Moon's far side, the Queqiao relay satellites. Ageing relay orbiters — Odyssey was launched in 2001 and MRO in 2005 — are a growing concern for future Mars surface missions.

![Relay of data from a Mars rover via an orbiter.](figures/out/ch25_relay.svg){#fig:relay width=88%}

## Orbiters World by World

### The Moon

The Moon has been orbited by more spacecraft than any other body. After Luna 10 (1966), NASA's five **Lunar Orbiters** (1966–67) photographed potential Apollo landing sites and 99 % of the surface. A long gap followed until **Clementine** (1994) and **Lunar Prospector** (1998), whose neutron spectrometer detected excess hydrogen at the poles — possibly water ice in permanently shadowed craters. The 2000s brought ESA's ion-propelled **SMART-1**, Japan's **Kaguya**, China's **Chang'e-1** and **Chang'e-2**, and India's **Chandrayaan-1**, whose NASA-supplied Moon Mineralogy Mapper detected hydroxyl and water molecules on the sunlit surface in 2009.

NASA's **Lunar Reconnaissance Orbiter (LRO)**, launched in 2009 and still operating, has mapped the Moon in unprecedented detail: its cameras resolve the Apollo landers and astronauts' tracks, its laser altimeter has produced a global topographic map, and its Diviner radiometer found the coldest places measured in the Solar System — about 25 K in polar craters (@fig:lroearthrise). Its companion **LCROSS** deliberately crashed a rocket stage into the crater Cabeus in 2009 and detected water in the ejecta. Today, India's **Chandrayaan-2** orbiter, Korea's **Danuri** (with NASA's ShadowCam, which images inside shadowed craters by faint reflected light) and China's Queqiao relays orbit the Moon, preparing for the Artemis and Chinese crewed landings (Chapters 27, 31).

![Earthrise as seen by NASA's Lunar Reconnaissance Orbiter in 2015, with the crater Compton on the Moon's far side in the foreground.](figures/photos/ch25_earthrise.jpg){#fig:lroearthrise width=52%}

### Mars

Mars has had a continuous orbital presence since 1997 (@fig:marsorbiters). **Mariner 9** (1971) revealed giant volcanoes, canyons and dry river valleys; the **Viking orbiters** (1976) mapped the planet; **Mars Global Surveyor** (1997–2006) measured its topography with a laser altimeter (MOLA) and discovered remnant crustal magnetism. **Mars Odyssey** (2001) found hydrogen-rich ground — ice — beneath the surface at high latitudes; ESA's **Mars Express** (2003) and NASA's **Mars Reconnaissance Orbiter** (2006) discovered clays and sulphates formed in water, revealing a warmer, wetter early Mars, and imaged active processes from avalanches to seasonal carbon-dioxide jets. NASA's **MAVEN** (2014) showed how the solar wind has stripped Mars's atmosphere, ESA–Roscosmos's **Trace Gas Orbiter** (2016) placed strict limits on atmospheric methane, India's **Mangalyaan** (2014–2022) was the first Asian Mars orbiter, the UAE's **Hope** (2021) studies the atmosphere from a high orbit, and China's **Tianwen-1** (2021) delivered the Zhurong rover. NASA's twin **ESCAPADE** smallsats, launched in 2025, will study the Martian magnetosphere from 2027.

![Orbiters at Mars since 1971. Six orbiters from four agencies and the UAE were operating in 2026.](figures/out/ch25_marstimeline.svg){#fig:marsorbiters width=94%}

![Artist's concept of NASA's Mars Reconnaissance Orbiter, with its 3 m high-gain antenna and large solar arrays. Since 2006 it has returned more data than all other Mars missions combined.](figures/photos/ch25_mro.jpg){#fig:mro width=60%}

### Venus

Venus's thick clouds hide its surface from optical cameras, so orbiters use radar. The Soviet **Venera 15 and 16** (1983) and NASA's **Magellan** (1990–1994) mapped it, revealing a young volcanic surface (@fig:venusmap). ESA's **Venus Express** (2006–2014) and Japan's **Akatsuki** (2015–2024) studied its atmosphere, including the "super-rotation" in which the cloud tops circle the planet in four days. Three new orbiters were planned — NASA's **VERITAS**, ESA's **EnVision** and ISRO's **Shukrayaan** — together with NASA's DAVINCI descent probe, although US budget pressures in 2025–26 made the NASA missions' future uncertain.

![A global radar view of Venus from Magellan data, centred on 180° longitude. Venus's surface is dominated by volcanic plains and highlands.](figures/photos/ch25_venus.jpg){#fig:venusmap width=48%}

### Mercury

NASA's **MESSENGER** (2011–2015) was the first Mercury orbiter. It found that Mercury's surface is unexpectedly rich in volatile elements such as sulphur and potassium, that its magnetic field is offset to the north, and that permanently shadowed craters near its poles contain water ice — on the planet closest to the Sun (@fig:mercury). The ESA–JAXA **BepiColombo** mission, launched in 2018, comprises two orbiters: ESA's Mercury Planetary Orbiter and JAXA's Mio, carried by a transfer module with electric propulsion. After a thruster power problem in 2024 delayed its arrival by about a year, it enters orbit around Mercury in November 2026.

![MESSENGER colour mosaic of Mercury's surface. Enhanced colours reveal variations in composition between volcanic plains and older terrain.](figures/photos/ch25_mercury.jpg){#fig:mercury width=94%}

### Jupiter

**Galileo** (1995–2003) dropped a probe into Jupiter's atmosphere and found evidence from magnetic-field measurements that Europa, Ganymede and Callisto have subsurface oceans. **Juno**, in orbit since 2016, studies Jupiter's interior from a polar orbit (@fig:junoorbit): it found that the planet's core is "dilute" — mixed with the surrounding envelope — that its zonal winds extend about 3 000 km deep, and that its poles are covered by clusters of giant cyclones. Its JunoCam has produced spectacular images (@fig:grs). Two new missions are on their way: NASA's **Europa Clipper** will make about 49 close flybys of Europa from 2030 to assess its habitability, and ESA's **JUICE** will tour the Galilean moons from 2031 before entering orbit around Ganymede in 2034 — the first spacecraft to orbit a moon of another planet.

![Jupiter's Great Red Spot imaged by JunoCam on Juno in July 2017 (enhanced colour). The storm, larger than the Earth, extends about 300 km below the clouds.](figures/photos/ch25_grs.jpg){#fig:grs width=92%}

### Saturn

**Cassini–Huygens** (2004–2017), a collaboration of NASA, ESA and the Italian Space Agency, was one of the most successful planetary missions. It delivered the Huygens probe to the surface of Titan (Chapter 27), found hydrocarbon lakes and seas near Titan's poles, and in 2005 discovered water-vapour and ice plumes erupting from the south pole of Enceladus (@fig:enceladus), fed by a subsurface ocean that contains salts, silica and organic molecules — making Enceladus one of the most promising places to search for life.

![Plumes of ice and water vapour rising from the south polar region of Enceladus, back-lit by the Sun, imaged by Cassini.](figures/photos/ch25_enceladus.jpg){#fig:enceladus width=44%}

### Small Bodies

Orbiting small bodies demands precise navigation in very weak gravity. NASA's **NEAR Shoemaker** orbited Eros for a year and landed on it in 2001; **Dawn** orbited Vesta (2011–12) and Ceres (2015–18), finding bright salt deposits on Ceres; ESA's **Rosetta** accompanied comet 67P/Churyumov–Gerasimenko for two years (2014–2016) as it passed perihelion. The sample-return missions Hayabusa2 and OSIRIS-REx also mapped their asteroids from orbit before collecting samples (Chapter 29). ESA's **Hera** will arrive at the binary asteroid Didymos–Dimorphos in November 2026 — a month earlier than first planned — to measure the effects of NASA's DART impact of 2022, and NASA's **Psyche** will orbit the metal-rich asteroid Psyche from 2029.

| Mission | Agency | Target | Arrival | Status (Oct 2026) |
|---|---|---|---|---|
| LRO | NASA | Moon | 2009 | Operating |
| Chandrayaan-2 orbiter | ISRO | Moon | 2019 | Operating |
| Danuri (KPLO) | KARI | Moon | 2022 | Operating |
| Mars Odyssey, MRO, MAVEN | NASA | Mars | 2001, 2006, 2014 | Operating (relay and science) |
| Mars Express, ExoMars TGO | ESA (TGO with Roscosmos until 2022) | Mars | 2003, 2016 | Operating |
| Hope | UAE | Mars | 2021 | Operating |
| Tianwen-1 orbiter | CNSA | Mars | 2021 | Operating |
| Juno | NASA | Jupiter | 2016 | Extended operations uncertain after 2025 |
| BepiColombo (MPO, Mio) | ESA, JAXA | Mercury | Nov 2026 | Orbit insertion |
| Hera | ESA | Didymos–Dimorphos | Nov 2026 | Final approach |
| Europa Clipper, JUICE | NASA, ESA | Jupiter system | 2030, 2031 | En route |
| Psyche | NASA | Asteroid Psyche | 2029 | En route |

: Planetary orbiters operating or arriving in 2026 (selected). {#tbl:orbiters2026}

## Ending an Orbiter Mission

Orbiters usually end when they run out of propellant for attitude control, when a critical component fails, or when funding stops. How they end is governed by **planetary protection** (Chapter 24): an orbiter must not contaminate a world that might host life, or that future missions will search for life.

- **Disposal into the planet.** Galileo was deliberately plunged into Jupiter in 2003 and Cassini into Saturn in 2017, so that they could never crash into Europa, Enceladus or Titan. Juno's mission plan also ends with a plunge into Jupiter.
- **Long-lived parking orbits.** Mars orbiters that have not been sterilised must stay in orbit for at least 20 years after launch (with 99 % probability) and 50 years (with 95 % probability). When Dawn ran out of hydrazine in 2018, it was left in an orbit around Ceres that is expected to remain stable for decades.
- **Controlled impacts.** Where contamination is not a concern, orbiters often end with an impact that is itself an experiment: LCROSS, GRAIL's twin spacecraft (2012) and LADEE (2014) impacted the Moon, MESSENGER crashed into Mercury in 2015, and Rosetta made a slow descent onto comet 67P in 2016, taking images until the final seconds.
- **Unplanned endings.** Mars Global Surveyor was lost in 2006 after a software error pointed a solar array wrongly and exposed its battery to the Sun; India's Mangalyaan fell silent in 2022, probably after a long eclipse drained its battery; contact with Akatsuki was lost in 2024.

::: example
**Example: choosing a Mars mapping orbit**

A new Mars orbiter must image the surface at the same local time each day (to keep shadows consistent) from an altitude of about 300 km.

1. Mars's $J_2$ = 1.96 × 10⁻³, radius 3 396 km and μ = 42 828 km³/s² give, at 300 km, a mean motion $n = \sqrt{\mu/a^3}$ = 9.2 × 10⁻⁴ rad/s.
2. The orbit plane must precess 360° in one Martian year (687 days): $\dot\Omega$ = 1.06 × 10⁻⁷ rad/s.
3. From $\dot\Omega = -\tfrac{3}{2} n J_2 (R/a)^2 \cos i$, $\cos i = -0.052$, so $i ≈ 93.0°$ (@fig:marssso).
4. The ground track shifts westward by about 28° of longitude per orbit (Mars rotates 360° in 24.6 hours while the orbit takes about 1.9 hours), so a camera with a 6 km swath needs thousands of orbits — several Earth years — to map the planet completely, as MRO's Context Camera did.
5. Planetary protection (Category III) requires the orbit to remain above the atmosphere for at least 20 years after launch, which a 300 km orbit easily satisfies if the spacecraft is clean or later raised.
:::

::: ai
**AI for planetary orbiters**

Planetary scientists use machine learning to detect craters, landslides, dust devils and new impacts in millions of orbital images, to map minerals from hyperspectral data, and to prioritise downlink of the most interesting observations. On board, autonomous instruments can detect transient events — such as plumes, storms or impacts — and decide what to observe and return (Chapter 46).
:::

::: key
**Key takeaways**

- Orbiters provide global, long-duration mapping, interior measurements and relays for surface missions.
- Orbit design depends on each body: lunar mascons allow only a few frozen low orbits; Mars's bulge allows nearly polar sun-synchronous orbits; Venus and Mercury pose thermal challenges; Jupiter's radiation shapes Juno's orbit; small bodies have weak, irregular gravity.
- Instruments include high-resolution cameras (HiRISE, about 30 cm/pixel), imaging spectrometers, radar sounders, altimeters, gravity science and particle and field sensors.
- Key discoveries include water ice at the lunar and Mercurian poles, Mars's watery past and atmospheric loss, Venus's volcanic surface, Jupiter's dilute core, and Enceladus's ocean plumes.
- In 2026, orbiters operate at the Moon, Mars and Jupiter; BepiColombo and Hera arrive at Mercury and Didymos, and Europa Clipper and JUICE are en route to Jupiter.
:::
