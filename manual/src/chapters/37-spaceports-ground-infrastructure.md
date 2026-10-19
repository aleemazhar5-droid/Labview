---
title: Spaceports and Ground Infrastructure
hero: ch37
abstract: Every orbital rocket leaves from a few hectares of concrete surrounded by thousands of square kilometres of cleared sky and sea. This chapter explains how launch sites are chosen — latitude, reachable inclinations, safe corridors over the ocean, weather and logistics — and surveys the world's spaceports, from Florida, which hosted a third of all launches in 2025, to new sites in Norway, Australia and India. It then looks inside a launch complex: flame trenches, water deluge, umbilical towers, propellant farms and the three ways of assembling a rocket. It follows a launch campaign through the range, the countdown and the weather rules, and ends with noise, environmental licensing, and launching from aircraft and ships.
---

A rocket spends weeks at its launch site and minutes flying from it. A modern **spaceport** combines an assembly hall, a chemical plant storing hundreds of tonnes of liquids at −253 °C to −183 °C, a deluge system that pours more than a million litres of water in half a minute, a tracking network watching thousands of kilometres of ocean, and a marine and aviation operation that clears the rocket's path and recovers what comes back.

In 2025 the world made 330 orbital launch attempts. More than half — 175 — left from just two places in the United States: Florida's Space Coast (109) and Vandenberg in California (66). China flew 93 times from four centres and from ships; Rocket Lab's private site on New Zealand's Mahia Peninsula launched 17 times, more than Russia's Baikonur and Plesetsk together. This chapter explains why the sites are where they are and what happens on them; the vehicles are described in Chapters 34 and 36.

## Choosing a Launch Site

### Latitude, Azimuth and Inclination

Chapter 34 showed that a rocket launched from latitude φ on **azimuth** *Az* (the compass direction of flight, measured clockwise from north) enters an orbit of inclination *i* given by

$$\sin Az = \frac{\cos i}{\cos \varphi}$$

Because |sin *Az*| cannot exceed 1, a direct launch can reach only inclinations between φ and 180° − φ: Kourou (5.2° N) can reach almost any orbit, Plesetsk (62.9° N) nothing below 62.9° without an expensive turn. Each allowed inclination can be reached flying north-east or south-east (north-west or south-west for a retrograde orbit), because the equation has two solutions, *Az* and 180° − *Az* (@fig:azimuthcurves). A launch due east gives the lowest inclination, *i* = φ; a polar orbit needs a launch due north or south; a sun-synchronous orbit (97–98°) a launch slightly west of north or south.

![(a) Launch azimuth needed to reach each orbit inclination from four sites (north-going solution; the south-going launch into the same orbit flies at 180° − Az). (b) The velocity a rocket gains from Earth's rotation depends only on the inclination of the orbit, 465 m/s × cos i; the dots mark the largest gain each site can obtain, by launching due east.](figures/out/ch37_azimuth.svg){#fig:azimuthcurves width=98%}

Earth's rotation carries the pad east at 465 m/s × cos φ: 463 m/s at Kourou, 409 m/s at Cape Canaveral, 212 m/s at Plesetsk. Only the component along the orbit helps, and it equals 465 m/s × cos *i* — the same for every site that can reach that inclination; the component across the orbit must be cancelled. For the International Space Station's 51.6° orbit latitude therefore matters little. It matters greatly for orbits inclined *less* than the site's latitude, above all the geostationary orbit, because turning the orbital plane after launch is expensive.

::: example
**Example: an ISS orbit and a geostationary transfer from Kourou and from Baikonur**

Kourou lies at 5.24° N; Baikonur at 45.96° N. Assume a 200 km parking orbit (7 784 m/s).

1. **ISS orbit (51.64°).** From Kourou, sin *Az* = cos 51.64° / cos 5.24° = 0.6209 / 0.9958 = 0.6235, so *Az* = 38.6°. From Baikonur, sin *Az* = 0.6209 / 0.6950 = 0.8934, so *Az* = 63.2°.
2. **Rotation gain.** Kourou's surface moves at 463 m/s, Baikonur's at 323 m/s. The speed the rocket must add is the vector difference between orbital velocity and ground velocity, $\sqrt{v^2 - 2 v v_r \sin Az + v_r^2}$. This gives a gain of 280 m/s at Kourou and 287 m/s at Baikonur: the equatorial site's extra rotation points across the orbit and is wasted.
3. **Geostationary transfer.** Launching due east, Kourou reaches a transfer orbit inclined about 5°. Baikonur's drop zones keep its launches at 51.5° or more, so a satellite would have to remove 51.6° of inclination at apogee, where it moves at 1.60 km/s and must reach 3.07 km/s. The combined burn is $\Delta v = \sqrt{v_1^2 + v_2^2 - 2 v_1 v_2 \cos \Delta i}$ = 1.49 km/s from Kourou against 2.43 km/s from Baikonur.
4. **Propellant.** With a 320 s apogee engine ($v_e$ = 3.14 km/s), the propellant share of the satellite's mass is $1 - e^{-\Delta v / v_e}$: 38 % from Kourou and 54 % from Baikonur. This is why Proton's Breeze-M upper stage performs most of the plane change itself in a long, multi-burn ascent, and why Europe built its spaceport near the equator.
:::

### What the Rotation Is Worth

Of the roughly 9.3 km/s of ideal Δv needed to reach low orbit (Chapter 34), typically 0.2–0.45 km/s comes free from the spin of the Earth. The next example puts a price on it.

::: example
**Example: the payload value of Earth's rotation**

Take an expendable two-stage kerosene rocket similar to Falcon 9: first stage 411 t of propellant, 25.6 t dry, average specific impulse 296 s; second stage 107.5 t of propellant, 4.0 t dry, 348 s.

1. Solving the rocket equation stage by stage for an ideal Δv of 9 300 m/s gives a payload of **21.9 t**.
2. Repeating for 9 400 m/s gives 21.1 t: each extra 100 m/s costs about 0.82 t, or 3.8 % of the payload.
3. A due-east launch from Kourou (463 m/s) rather than Cape Canaveral (409 m/s) gains 54 m/s, about 0.45 t; rather than Plesetsk (212 m/s), 251 m/s, or **2.2 t** — 10 % of the payload.
4. A sun-synchronous orbit (97.5°) is slightly retrograde: the rocket loses 61 m/s to rotation wherever it launches, about 0.5 t.
:::

### Safety Corridors and Overflight

Geometry says which orbits a site *could* reach; safety says which it *may*. Rockets drop spent stages and fairings along their path, and a failing vehicle can scatter debris wherever its **instantaneous impact point** — where it would land if the engines stopped — happens to be. Ranges therefore allow only azimuths whose early flight and drop zones lie over the sea or empty land (@fig:corridormap). Cape Canaveral launches between north-east, along the US coast to inclinations of about 57°, and east-south-east over the Atlantic; Vandenberg launches south over the Pacific; Kourou has open ocean to the north and east; Starship leaves Starbase over the Gulf of Mexico and passes between Florida and Cuba.

![Initial launch corridors from four spaceports in the Americas: great-circle paths for the first 2 200 km on the azimuth needed for each inclination.](figures/out/ch37_corridors.png){#fig:corridormap width=96%}

The corridors leave a fingerprint in the orbits each site actually uses (@fig:incflown). Baikonur, deep inside Kazakhstan, drops its stages in designated zones on the steppe; partly to keep them out of China, it launches no lower than about 51.5°, which is why the ISS orbits at 51.6°. Palmachim, on Israel's coast, launches westward over the Mediterranean to avoid overflying its neighbours, so every satellite launched from Israel flies a retrograde orbit inclined 139–143°. Sriharikota's polar launches must turn ("dog-leg") to avoid Sri Lanka, one reason India is building a second spaceport farther south. Florida had not launched into a polar orbit since February 1969 until a Falcon 9 flew south along the coast on 30 August 2020; this "polar corridor" has since carried the PACE satellite and, in April 2025, the first crewed polar flight, Fram2.

![Inclinations reached by successful orbital launches from 15 spaceports, 2010–2026, against the band each site's latitude allows (shaded). Clusters reveal the corridors: 51.6° at Baikonur, 43° and 53° (Starlink) at the Cape, 97–98° at Vandenberg, Taiyuan and Jiuquan, 139–143° at Palmachim. Open circles are geostationary missions whose upper stages removed inclination in orbit.](figures/out/ch37_incflown.svg){#fig:incflown width=100%}

### Weather, Logistics and Politics

A launch site also needs tolerable weather (Florida's thunderstorms are discussed below), ports and roads for stages up to 9 m in diameter, power, fresh water, a workforce and an airport. Large stages are often built far away: the SLS core stage reaches Florida by barge from New Orleans, Ariane 6 stages cross the Atlantic by ship and Soyuz rockets reach Baikonur by rail. SpaceX builds Starship beside its pads at Starbase, a company town incorporated as a city in May 2025.

Politics shapes the map as much as physics. Russia leases Baikonur from Kazakhstan for $115 million a year until 2050 and built Vostochny, in its own Far East, to depend less on it. China placed Jiuquan, Taiyuan and Xichang far inland for security, which is why their spent stages fall on land. And many countries want a "sovereign" launch site even if it flies only a few times a year.

## The World's Spaceports

### Where Rockets Fly From

About 40 sites, counting airfields used for air launch, have sent rockets towards orbit; 22 did so in 2025 (@fig:spaceportmap). Over the whole space age the busiest has been Plesetsk, with 1 688 launches, mostly Soviet military satellites, followed by Baikonur (1 560) and Cape Canaveral with Kennedy (1 401). Since 2016 the world launch rate has nearly quadrupled, and the growth came almost entirely from Florida, Vandenberg and China (@fig:sitetrend).

![Orbital launch attempts from each spaceport, 2016–2025 (bubble area), coloured by activity in 2025. Florida, Vandenberg and China's four centres dominate; Rocket Lab's Mahia site in New Zealand outflew every Russian site.](figures/out/ch37_worldmap.png){#fig:spaceportmap width=100%}

![Orbital launch attempts per year by spaceport, 2000–2026. Florida and Vandenberg together hosted 175 of the 330 attempts in 2025; China's launch rate has risen sixfold since 2010.](figures/out/ch37_trend.svg){#fig:sitetrend width=96%}

@tbl:spaceports summarises the busiest spaceports and @tbl:newspaceports the smaller and newer ones.

| Spaceport | Latitude | Main pads and vehicles (2026) | 2025 | Notes |
|------------|----|----------------------|---|------------|
| Cape Canaveral SFS & Kennedy Space Center (USA) | 28.5° N | SLC-40, LC-39A (Falcon 9, Falcon Heavy); SLC-41 (Atlas V, Vulcan); LC-36 (New Glenn); LC-39B (SLS) | 109 | Busiest site; Starship pads at LC-39A and SLC-37 under construction |
| Vandenberg SFB (USA) | 34.7° N | SLC-4E (Falcon 9); SLC-6 (Falcon, being rebuilt); SLC-2W (Firefly Alpha); SLC-8 (Minotaur) | 66 | Polar and sun-synchronous launches south over the Pacific |
| Starbase, Texas (USA) | 26.0° N | Pads 1 and 2 (Starship) | 5 | Up to 25 launches a year approved in 2025 |
| Jiuquan (China) | 41.0° N | LC-43/91 (Long March 2F, crews); LC-43/94–95 (Long March 2C/2D, 4); commercial pads (Kuaizhou, Ceres-1, Zhuque, Long March 12B) | 34 | China's crewed launch site, in the Gobi Desert |
| Wenchang (China) | 19.6° N | LC-101 (Long March 5), LC-201 (Long March 7/7A), LC-301 (Long March 10); commercial Pads 1–2 (Long March 8, 12, 10B) | 21 | Coastal; heavy lift, station cargo and lunar missions |
| Xichang (China) | 28.2° N | LC-2, LC-3 (Long March 3A/3B/3C) | 19 | Geostationary and BeiDou launches; stages fall inland |
| Mahia, LC-1 (New Zealand) | 39.3° S | LC-1A, LC-1B (Electron) | 17 | Private; up to 120 launch opportunities a year |
| Taiyuan (China) | 38.8° N | LC-9, LC-9A, LC-16 (Long March 2, 4, 6, 6A) | 12 | Sun-synchronous and polar orbits |
| Plesetsk (Russia) | 62.9° N | Site 43 (Soyuz-2), Site 35 (Angara) | 9 | Military; high inclinations only |
| Kourou, Guiana Space Centre (France/ESA) | 5.2° N | ELA-4 (Ariane 6), ZLV (Vega-C); ELM-Diamant (micro-launchers, planned) | 7 | Near-equatorial; ocean to the north and east |
| Chinese sea launches | ≈ 35° N | Ships from Haiyang, Shandong (Long March 11, Jielong-3, Ceres-1S, Gravity-1) | 7 | 28 launches since 2019, all successful |
| Baikonur (Kazakhstan, leased by Russia) | 46.0° N | Site 31 (Soyuz crew and cargo); Site 81 (Proton); Site 45 (Soyuz-5) | 6 | Site 31 damaged in November 2025, repaired by March 2026 |
| Sriharikota, SDSC-SHAR (India) | 13.7° N | First and Second Launch Pads (PSLV, GSLV, LVM3, SSLV) | 5 | Third Launch Pad approved January 2025 |
| Tanegashima (Japan) | 30.4° N | Yoshinobu LP-1, LP-2 (H3) | 4 | H-IIA retired June 2025 |

: The world's busiest spaceports. "2025" is the number of orbital launch attempts that year (GCAT, J. McDowell). {#tbl:spaceports}

### The Americas

**Florida** is two neighbouring sites run as one range. NASA's Kennedy Space Center owns Launch Complex 39, built for the Saturn V: Pad 39A is leased to SpaceX for Falcon 9 and Falcon Heavy and is being equipped for Starship; Pad 39B was rebuilt for the Space Launch System, which flew Artemis II from it on 1 April 2026. Cape Canaveral Space Force Station hosts SpaceX's busiest pad, SLC-40, which has also launched crews since 2024; United Launch Alliance's SLC-41 for Atlas V and Vulcan; Blue Origin's LC-36 for New Glenn, where a booster exploded during a hot-fire test in May 2026; and pads being rebuilt for newcomers such as Relativity and Stoke. In late 2025 the Air Force approved SLC-37 for up to 76 Starship launches a year.

**Vandenberg**, on the Californian coast, is America's polar spaceport; its 66 launches in 2025 were almost all Falcon 9s from SLC-4E. In October 2025 the Air Force approved up to 100 Falcon launches a year from SLC-4 and a rebuilt SLC-6; the California Coastal Commission, worried about sonic booms and wildlife, objected, and the dispute went to court. **Wallops**, in Virginia, hosts Antares and Minotaur pads and Rocket Lab's LC-2 for Electron and LC-3 for Neutron, whose debut has slipped to 2027. At **Starbase**, in southern Texas, Starship's second pad, with a water-cooled flame trench, flew all three Starship flights of 2026, including the first orbital flight on 28 September.

Europe's spaceport is the **Guiana Space Centre** at Kourou, run by the French space agency CNES with ESA. Ariane 6 flies from ELA-4 and Vega-C from the Vega pad; the Soyuz pad fell idle when Russia withdrew in 2022, and the old Diamant site is being rebuilt for European micro-launchers. Brazil's **Alcântara**, at 2.3° S, hosted its first orbital attempt in more than 20 years in December 2025, when Innospace's HANBIT-Nano failed about 30 s after lift-off.

### Russia and Kazakhstan

**Baikonur**, on the Kazakh steppe, launched Sputnik and Gagarin and is still Russia's only site for crews and ISS cargo. Soyuz rockets are assembled horizontally, rolled to the pad by train and raised by a hydraulic erector (@fig:soyuzrail). On 27 November 2025, during the launch of Soyuz MS-28, the mobile service cabin under the rocket at Site 31, not properly secured after retraction, fell into the flame trench. With Gagarin's original pad retired in 2019, Russia briefly had no pad for crewed flights; more than 150 workers rebuilt the cabin, installing 19 m members weighing 17 t each, and the pad was cleared for a Progress launch in March 2026. Site 45 flew the first Soyuz-5 on a suborbital test on 30 April 2026.

::: figrow
![A Soyuz rocket rolled out by train to Site 31 at Baikonur, September 2023. Assembled horizontally, it travels on the transporter-erector that will raise it at the pad.](figures/photos/ch37_soyuzrail.jpg){#fig:soyuzrail}

![The erector raising a Soyuz into the launch table at Site 31, September 2024. The four support arms of the pad will hold the rocket by its waist until lift-off.](figures/photos/ch37_soyuzerect.jpg){#fig:soyuzerect}
:::

**Plesetsk**, 800 km north of Moscow, launches military Soyuz-2 and Angara rockets; **Vostochny**, in the Far East, has launched Soyuz-2 since 2016 and Angara A5 since 2024, but only twice in 2025.

### China

China has four state launch centres and a growing commercial sector. **Jiuquan**, in the Gobi Desert, launches Shenzhou crews and, increasingly, commercial rockets from new pads nearby — among them LandSpace's Zhuque-3, whose booster touched down on its legs in August 2026, although a fire followed. **Taiyuan** specialises in sun-synchronous orbits and **Xichang**, in Sichuan, in geostationary and BeiDou missions. Both lie inland: spent stages carrying toxic hypergolic residue fall in mountain valleys, and residents downrange are warned to shelter or leave.

**Wenchang**, on Hainan Island, is the coastal site for Long March 5 and 7 and the new crew-capable Long March 10, whose first stage flew a suborbital test from the new pad LC-301 in February 2026. Beside it, the **Hainan commercial launch site**, China's first commercial spaceport, opened its two pads in 2024–25, flew Long March 10B's maiden flight on 10 July 2026 and was building Pads 3 and 4 for more than 60 launches a year. China also launches solid rockets from **ships** sailing from Haiyang in Shandong (see the last section).

### India, Japan, Korea and the Middle East

India's **Satish Dhawan Space Centre** on Sriharikota Island has two pads; in January 2025 the government approved a third (₹3 985 crore, about four years to build) for the Next Generation Launch Vehicle. **Kulasekarapattinam**, at 8.4° N in Tamil Nadu, is being built for SSLV and private rockets, with a first launch planned for 2027.

Japan launches H3 from the Yoshinobu complex at **Tanegashima**, where rockets are stacked in an assembly building and moved to the pad on a mobile launcher (@fig:tanegashima). The H-IIA made its final flight in June 2025; H3 failed in December 2025 and returned to flight in mid-2026. The solid Epsilon S, delayed by two motor explosions in tests, was being prepared at **Uchinoura** for a launch by March 2027. South Korea's **Naro Space Center** launched Nuri successfully in November 2025, the first time with industry as prime contractor, and again in October 2026.

![An H-IIA rocket carrying the Global Precipitation Measurement Core Observatory rolls out on its mobile launcher to Launch Pad 1 at Tanegashima in February 2014. The red-and-white masts are lightning towers.](figures/photos/ch37_h2a.jpg){#fig:tanegashima width=40%}

Israel launches Shavit rockets from **Palmachim** air base; Iran uses the **Imam Khomeini Spaceport** near Semnan and the military site at **Shahroud**; North Korea's **Sohae** last launched, unsuccessfully, in May 2024.

### New and Small Spaceports

Small launchers have prompted a wave of new sites, many at high latitudes where polar orbits can be reached over empty sea (@tbl:newspaceports). Isar Aerospace's Spectrum failed 30 s into its first flight from **Andøya**, Norway, in March 2025 but reached orbit on 5 September 2026 — the first orbital launch from continental Western Europe. RFA One stood on the pad at **SaxaVord** in Shetland in July 2026 but was removed for investigation.

| Spaceport | Latitude | Operator and vehicle | Status (October 2026) |
|-----------|----|--------------|----------------|
| Andøya (Norway) | 69.3° N | Isar Aerospace Spectrum | Failed March 2025; reached orbit 5 September 2026 |
| SaxaVord, Shetland (UK) | 60.8° N | RFA One | Awaiting first launch; rocket de-stacked July 2026 |
| Esrange (Sweden) | 67.9° N | Firefly Alpha (LC-3C) | First orbital launch targeted 2028 |
| Kulasekarapattinam (India) | 8.4° N | ISRO SSLV, private rockets | Under construction; first launch 2027 |
| Bowen (Australia) | 20.0° S | Gilmour Space Eris | First flight failed after 14 s (July 2025); second planned late 2026 |
| Alcântara (Brazil) | 2.3° S | Innospace HANBIT-Nano | First flight failed (December 2025) |
| Spaceport Kii (Japan) | 33.5° N | Space One Kairos | Three failures (2024–26) |
| Spaceport America (USA) | 33.0° N | Virgin Galactic (suborbital) | Delta-class spaceplane being prepared for flight tests |

: Selected new and smaller spaceports. {#tbl:newspaceports}

## Inside a Launch Complex

### The Pad: Mounts, Trenches and Deflectors

At the heart of every pad is the **launch mount**, a steel table that carries the rocket through **hold-down clamps** (@fig:padschem). Liquid-fuelled rockets ignite a few seconds before release while computers confirm that every engine has reached full thrust; if one misbehaves, everything shuts down with the vehicle still clamped — a **hold-down abort**.

![Main elements of a liquid-propellant launch pad. The exhaust passes through the flame hole into a trench, where a deflector turns it sideways; water floods the mount and trench at ignition; umbilicals deliver propellant, gas, power and data until lift-off; lightning masts and propellant storage stand at a safe distance.](figures/out/ch37_pad.svg){#fig:padschem width=98%}

The exhaust, at 2–4 km/s and up to about 3 000 °C, passes through a hole in the mount into a **flame trench**, a concrete channel where a wedge-shaped **flame deflector** turns it sideways. At Pad 39B the trench is more than 130 m long and lined with about 96 000 heat-resistant bricks, and the deflector, completed in 2018, is built from some 150 steel plates of up to 1.8 t each (@fig:flamedeflector). Without a trench the jet strikes the ground directly: on Starship's first flight in April 2023, Super Heavy's 33 engines dug a crater under the mount and threw concrete across the site. SpaceX then fitted a water-cooled steel plate under the mount, and its second Starbase pad has a full trench.

![The new main flame deflector in the flame trench at Launch Complex 39B in May 2018, built to divert the exhaust of the Space Launch System sideways along the trench.](figures/photos/ch37_deflector.jpg){#fig:flamedeflector width=58%}

### Water: Deluge and Sound Suppression

Ignition creates a sharp pressure pulse, the **ignition overpressure**, which reflects from the trench onto the rocket; on the first Space Shuttle flight in 1981 it knocked off or damaged 164 heat-shield tiles. Lift-off also radiates about 200 dB of sound power, which shakes the payload (Chapter 34). The cure is water sprayed into the exhaust and over the mount, which absorbs energy as it is shattered into droplets and turned to steam. At Pad 39B a 400 000-gallon (1.5 million litre) tower empties in under 30 s, at a peak of about 70 m³/s (@fig:wetflow); the Shuttle's 300 000 gallons flowed for 41 s, starting 6.6 s before main-engine start; Ariane 6 receives about a quarter of an Olympic pool in 20 s. Most of the white cloud seen at lift-off is this water turned to steam.

![A test of the Pad 39B sound-suppression system in September 2019: water pours over the SLS mobile launcher and through its flame hole into the trench.](figures/photos/ch37_wetflow.jpg){#fig:wetflow width=60%}

### Umbilicals, Towers and Catch Arms

Until lift-off the rocket is fed through **umbilicals** — hoses and cables for propellant top-up, pressurant gas, conditioned air, power and data — attached by quick-disconnect plates that separate in the last seconds or as the vehicle rises. Upper-stage umbilicals hang from swing arms on a **service tower**, which for crewed launches also carries a **crew access arm** and an escape system; tail umbilicals at the base retract into protective housings at lift-off. These interfaces are a common cause of scrubs: Artemis I was delayed from August to November 2022 partly by hydrogen leaks at a quick-disconnect on its tail service mast.

SpaceX's Starship towers add a new function: their two "chopstick" arms stack the booster and ship on the mount and, since Flight 5 in October 2024, catch the returning booster in mid-air, making the tower a crane, umbilical tower and landing pad in one.

### Propellants and Gases

A pad is also a cryogenic plant (@tbl:padcommodities). NASA's newest hydrogen sphere at Pad 39B, finished in 2022, holds about 4 700 m³ of usable liquid hydrogen — the largest such tank in the world — and its glass-bubble insulation cuts boil-off by 40–50 % compared with the perlite of its 1960s neighbour. Transfer lines are **vacuum-jacketed** to limit heat leaks.

| Commodity | Storage | Density (kg/m³) | Used for | Main hazard |
|--------|----------|-----|---------|---------|
| Liquid oxygen (LOX) | −183 °C; Falcon 9 subcools to about −207 °C | 1 141 (more when subcooled) | Oxidiser for most liquid rockets | Intense fire with any fuel; cold burns |
| Liquid hydrogen (LH₂) | −253 °C | 71 | Fuel (SLS, Ariane 6, H3, Centaur) | Invisible flame; leaks; embrittlement |
| Liquid methane (LCH₄) | −162 °C | 422 | Fuel (Starship, Vulcan, New Glenn, Zhuque) | Flammable vapour cloud |
| RP-1 kerosene | Ambient; Falcon 9 chills to about −7 °C | ≈ 810 | Fuel (Falcon, Soyuz, Electron, Long March 6/7) | Fire |
| Hydrazine, MMH, N₂O₄ | Ambient, sealed | 1 000–1 450 | Spacecraft thrusters; some upper stages | Toxic, carcinogenic; ignite on contact |
| Helium, nitrogen | Gas at 20–40 MPa | — | Pressurant; purges | Asphyxiation; stored energy |

: Commodities stored and handled at a typical launch site. {#tbl:padcommodities}

Cold propellant is denser: Falcon 9 chills its oxygen to about −207 °C, 24 °C below its boiling point, and its kerosene to about −7 °C. Because the propellant then warms in the tanks, it is loaded only in the last 35 minutes, with the crew already aboard on Dragon flights — a "load and go" procedure NASA approved in 2018. Spacecraft propellants are **hypergolic** (they ignite on contact) and toxic; they are loaded days or weeks earlier in a payload processing facility by technicians in protective suits (@fig:scapefuel), before the spacecraft is sealed in its fairing (Chapter 34).

![Fuelling technicians in self-contained atmospheric protective ensemble (SCAPE) suits take a sample of monomethylhydrazine before loading it into NASA's Solar Dynamics Observatory at a payload processing facility near Kennedy Space Center in January 2010.](figures/photos/ch37_scape.jpg){#fig:scapefuel width=58%}

### Assembling the Rocket

Rockets are assembled in one of three ways (@fig:integrationmodes). **Vertical assembly and transfer** stacks the vehicle on a mobile launcher inside a tall building, such as NASA's 160 m Vehicle Assembly Building, and carries it to the pad. The crawler-transporter weighs about 3 000 t, can carry 8 200 t and creeps the 6.8 km to Pad 39B at 1.6 km/h, burning some 390 litres of diesel per kilometre, while hydraulic jacks keep its load level on the ramp (@fig:crawlerpad). A second, taller mobile launcher for SLS Block 1B was abandoned in 2026 after its cost grew from $383 million to about $1.8 billion. Japan, China and United Launch Alliance use the same principle with platforms on rails or tow vehicles.

![Three ways to assemble a launch vehicle: (a) stacked vertically in an assembly building and carried to the pad on a mobile launcher; (b) integrated horizontally in a hangar and raised at the pad by a transporter-erector; (c) assembled vertically on the pad inside a mobile gantry that rolls away before launch.](figures/out/ch37_integration.svg){#fig:integrationmodes width=98%}

**Horizontal integration**, the Soviet tradition followed by SpaceX and Rocket Lab, joins the stages lying down in a simple hangar; a transporter-erector then raises the rocket at the pad (@fig:soyuzrail). The payload is usually mated horizontally too, which some national-security satellites cannot tolerate, so in 2020 SpaceX proposed a mobile service tower at Pad 39A for vertical integration. **Vertical integration on the pad** builds the rocket in place inside a mobile gantry: Ariane 6's, at ELA-4, is 90 m tall, weighs about 8 200 t and rolls 120 m away before launch.

![The crawler-transporter that carried NASA's Space Launch System to Launch Pad 39B in March 2022, with the rocket standing on its mobile launcher at the pad in the background. The crawler rides on four double-tracked trucks, each driven by four 375 hp electric motors.](figures/photos/ch37_crawler.jpg){#fig:crawlerpad width=40%}

## The Range: Tracking, Safety and Recovery

### Instrumentation and Telemetry

The **range** is everything beyond the pad that keeps a launch safe and observed: radars, telemetry antennas, optical trackers, weather instruments and a control centre. The US Space Force runs the Eastern Range from Florida (Space Launch Delta 45) and the Western Range from Vandenberg (Space Launch Delta 30); NASA runs Wallops and CNES Kourou, each with downrange tracking stations. During ascent the range receives telemetry and compares the instantaneous impact point with pre-set limits. Since 2017 most American launches have carried an **autonomous flight safety system** that makes any destruct decision on board (Chapter 34), so ranges depend less on tracking radars and can support launches in quick succession.

### Hazard Areas in the Sky and at Sea

Before each launch the range defines **hazard areas** where falling stages, fairings or failure debris could land. Aircraft are kept out by notices issued through the Federal Aviation Administration (FAA), ships by navigational warnings, and a single boat inside the zone can halt the count — the range is "fouled". If a vehicle breaks up unexpectedly, the FAA can activate a **debris response area**: when Starship Flight 7 broke up over the Caribbean on 16 January 2025, dozens of airliners were held or diverted, and debris was reported on the Turks and Caicos Islands.

### Recovery Fleets and Landing Zones

Reusable rockets have turned ranges into recovery operations. SpaceX's three autonomous **droneships**, two in the Atlantic and one in the Pacific, wait about 600 km downrange for boosters (@fig:corridormap), and other ships collect fairing halves from the sea. Boosters that fly back land on concrete **landing zones**; at Cape Canaveral Landing Zone 1 was retired when its lease ended in July 2025, and LZ-40 beside SLC-40 took its first booster on 13 February 2026. Dragon capsules have splashed down off California since 2025, after pieces of their jettisoned trunks reached land in Australia and North Carolina. Blue Origin lands New Glenn boosters on the ship *Jacklyn*, and in July 2026 China caught a Long March 10B first stage in a net of cables on the ship *Linghangzhe*.

## The Launch Campaign and Countdown

### From Arrival to Lift-off

A campaign begins weeks before the countdown. A large satellite typically arrives four to eight weeks before launch, is tested, fuelled, mated to its adapter and encapsulated. The rocket's stages are checked, joined and often test-fired on the pad — a **static fire** — or put through a **wet dress rehearsal**, a countdown with propellant loading that stops before ignition. Falcon 9 is usually rolled out within a day of launch, Soyuz two days before, while SLS spends weeks at the pad.

### The Countdown

The countdown is a scripted sequence (@tbl:f9countdown). The **launch director** polls each team at set points ("go/no-go"), built-in **holds** give time to catch up, and in the last minutes an automatic sequencer takes over, ready to stop if any measurement drifts out of limits.

| Time (min:s) | Event |
|---|------------|
| −38:00 | Launch director verifies "go" for propellant load |
| −35:00 | RP-1 loading begins; first-stage LOX loading begins |
| −16:00 | Second-stage LOX loading begins |
| −07:00 | Pre-launch engine chill begins |
| −05:00 | Dragon transfers to internal power |
| −01:00 | Flight computer begins final checks; tanks pressurised for flight |
| −00:45 | Launch director verifies "go" for launch |
| −00:03 | Engine controller commands ignition sequence |
| 00:00 | Lift-off |

: Falcon 9 countdown milestones for a Dragon cargo mission from LC-39A (CRS-29, NASA, November 2023; times approximate). {#tbl:f9countdown}

The **launch window** may last hours for a sun-synchronous satellite, or be **instantaneous** for a mission that must meet the ISS, leaving no time to resolve a problem.

### Launch Commit Criteria

Weather causes about half of all scrubs at Cape Canaveral: in 2020 the 45th Weather Squadron reported that 49 % of scrubs were due to weather, which affected 24 % of all countdowns. The rules are written as **launch commit criteria** (@tbl:wxcriteria). Wind limits protect the vehicle on the pad and in the jet stream; cloud and lightning rules protect it from **triggered lightning** — a rocket and its long, ionised plume can trigger a strike in a field too weak to produce lightning on its own, as happened to Apollo 12 in 1969 and to Atlas-Centaur 67, destroyed in 1987. Electric-field mills around the pads measure the field continuously.

| Parameter | Do not launch if… |
|----|--------------|
| Ground wind | Sustained wind at 49 m (162 ft) on the pad exceeds 13.4 m/s (30 mph) |
| Upper-level winds | Wind shear aloft could cause control problems |
| Lightning | Lightning within 18.5 km (10 nautical miles) of the pad or flight path in the last 30 min, unless specific conditions are met |
| Anvil clouds | Within 18.5 km of an attached anvil (with exceptions) or of any detached anvil |
| Cumulus clouds | Within 18.5 km of cumulus with tops colder than freezing, unless distance rules are met |
| Thick clouds | Flight through a layer more than 1.4 km thick extending into freezing temperatures |
| Electric field | Field mills within 9.3 km of the pad read more than ±1 500 V/m (or ±1 000 V/m under some conditions) in the last 15 min |
| Abort weather | Wind, waves or rain at more than 50 downrange splashdown sites exceed the limits for a Dragon abort |

: Weather launch commit criteria for a crewed Falcon 9 from Florida (NASA fact sheet, abridged). {#tbl:wxcriteria}

Florida is America's thunderstorm capital. In 1950–80 the Cape averaged 76 thunderstorm days a year, 80 % of them from May to September, peaking at 16 in July (@fig:capeweather); summer storms build in the afternoon, when sea breezes from both coasts collide. A 2024 study of 18 years of field-mill records found that 88 % of successful launches in 2005–2020 lifted off in hours when the climatological chance of violating the electric-field rule was 15 % or less.

![(a) Mean number of days with thunderstorms per month at Cape Canaveral, 1950–52 and 1957–80. (b) The probability that an afternoon launch has flown after a given number of daily attempts, if any thunderstorm day forbids launch and there is a 10 % chance of a non-weather scrub each day.](figures/out/ch37_weather.svg){#fig:capeweather width=98%}

![Lightning near Launch Complex 39B on 10 June 2022, with the Artemis I rocket on the pad. The pad's three 180 m masts and their wires carry strikes to ground away from the vehicle.](figures/photos/ch37_lightning.jpg){#fig:padlightning width=56%}

::: example
**Example: the odds of a summer scrub**

A satellite must launch in a two-hour window starting at 14:00 local time from Cape Canaveral. Use the thunderstorm climatology of @fig:capeweather as the chance that lightning rules forbid an afternoon window, and assume a 10 % chance that a technical problem scrubs any attempt, independent of the weather.

1. **July:** 16 thunderstorm days in 31, so the chance of good weather is 1 − 0.516 = 0.484. The chance of launching on a given attempt is 0.484 × 0.90 = **0.44**.
2. The number of attempts follows a geometric distribution, with mean 1/0.44 = **2.3 attempts**. The chance of having launched within three days is 1 − (1 − 0.44)³ = 0.82, so about one campaign in five will still be waiting after three days.
3. **January:** 1 thunderstorm day in 31 gives 0.97 × 0.90 = 0.87 per attempt, a mean of 1.15 attempts, and a 99.8 % chance of launching within three days — though winter cold fronts bring strong upper-level winds instead.
4. Over the year, 76 thunderstorm days in 365 is a 21 % chance, close to the 24 % of countdowns that weather affects. A morning window, when storms are rare, is the best cure.
:::

### Scrubs, Holds and Recycles

When a criterion is violated the count **holds**; if the problem cannot be cleared within the window, the launch is **scrubbed**. The **turnaround** to the next attempt depends on draining and replacing propellant and fixing the fault: Falcon 9 often tries again 24 hours later, a hydrogen-fuelled vehicle may need two days or more, and a mission tied to a planetary window may wait weeks.

## Environment, Community and Regulation

### Noise and Sonic Booms

A rocket's **sound power** is a small fraction η, the **acoustic efficiency**, of the mechanical power of its jet, ½ × thrust × exhaust speed. Measurements 1.4–1.8 km from the Artemis I launch gave SLS a sound power level of 202.4 dB (re 1 pW) and an efficiency of 0.33 %, below the 0.5 % long assumed; Falcon 9 radiates about 196 dB and the Saturn V about 205 dB. Treating the rocket as a source above hard ground gives the levels of @fig:launchnoise. The model reproduces SLS's measured 137 dB at 1.43 km and predicts 123 dB at 10 km from Super Heavy, close to the 125 dB recorded by Brigham Young University researchers about 10 km from Starbase on Starship Flight 5. The 120 dB contour lies about 4.5 km from a Falcon 9, 9 km from SLS and 14 km from Super Heavy.

![Maximum overall sound level against distance for five launch vehicles, from their sound power assuming hemispherical spreading over hard ground and a 5 dB directivity gain. Points are measurements at the Artemis I launch and during Starship Flight 5.](figures/out/ch37_noise.svg){#fig:launchnoise width=92%}

The model ignores absorption by the air, small at the low frequencies (10–100 Hz) where rocket noise is strongest, and weather, which can focus sound far from the pad. Returning boosters add **sonic booms**: at Starbase the boom of the descending Super Heavy was the strongest pressure event of the flight, and booms lie at the centre of California's objections to more Vandenberg launches.

### Debris, Wildlife and Water

Spaceports often share land with wildlife because their safety zones keep people out: Kennedy Space Center lies within the Merritt Island National Wildlife Refuge, Starbase among protected tidal flats, and Vandenberg's coast hosts nesting shorebirds and seals. Operators control lighting that disorients nesting sea turtles, monitor deluge water (which picks up hydrochloric acid from solid motors) and survey debris thrown out at lift-off. Downrange, falling stages have contaminated drop zones in Kazakhstan and China with the toxic fuel UDMH.

### Licensing and Environmental Review

In the United States the FAA licenses launches, re-entries and spaceport operators. Its performance-based rule, **14 CFR Part 450**, adopted in 2021, became the only licensing route in March 2026, when the older licences expired; it caps the expected casualties from each launch at 1 × 10⁻⁴ (Chapter 34). Federal decisions also need review under the **National Environmental Policy Act** — an environmental assessment where impacts are expected to be modest, or a full environmental impact statement that can take years. The May 2025 approval of 25 Starship launches a year from Starbase followed an assessment; SLC-37 and the Vandenberg increase needed full statements. Executive Order 14335 of August 2025 told the FAA to revise Part 450 and agencies to use simpler "categorical exclusions" for routine launch actions.

Elsewhere, the UK Civil Aviation Authority licenses spaceports and launches under the Space Industry Act 2018; France's 2008 Space Operations Act gives CNES responsibility for safety at Kourou; Australia, New Zealand and Japan passed launch laws in 2016–18; and India authorises private launches through its regulator IN-SPACe. All implement the Outer Space Treaty principle that a state is liable for damage caused by objects it launches (Chapter 1).

## Launching from the Air and the Sea

A rocket launched from an aircraft or a ship can choose its latitude and azimuth, avoid overflying land and escape a fixed site's weather; air launch also saves a little Δv by starting above the densest air (@tbl:airsealaunch). Northrop Grumman's **Pegasus** has flown 46 times since 1990, latterly from the L-1011 *Stargazer* at about 12 km (@fig:pegasusmate); its latest flight, on 3 July 2026 from Kwajalein, carried a servicer to raise the orbit of NASA's Swift observatory. Virgin Orbit's **LauncherOne**, dropped from a Boeing 747, reached orbit four times in six attempts; after a failure from Spaceport Cornwall on 9 January 2023 — the first orbital attempt from the UK — the company closed.

![A Pegasus XL rocket carrying NASA's NuSTAR telescope, attached beneath the L-1011 carrier aircraft Stargazer in June 2012. The aircraft carries the rocket to about 12 km and releases it over the ocean.](figures/photos/ch37_pegasus.jpg){#fig:pegasusmate width=60%}

**Sea Launch**, an American–Russian–Ukrainian–Norwegian venture, sailed a converted oil platform from Long Beach to the equator and launched Zenit-3SL rockets 36 times from 1999 to 2014; in 2007 one exploded on the platform. China is now the leading sea launcher: since a Long March 11 flew from a barge in the Yellow Sea in June 2019, solid rockets such as Jielong-3, Ceres-1S and Gravity-1 have flown 28 times from ships based at Haiyang and Yangjiang. Solid rockets need little ground support; cryogenic propellants are far harder to handle on a moving deck.

| System | Platform | Flights | Period | Status (2026) |
|---------|----------|---------|-----|------|
| Pegasus (Northrop Grumman) | L-1011 *Stargazer* (earlier NB-52) | 46, of which 4 failed or partly failed | 1990–2026 | Flown occasionally |
| LauncherOne (Virgin Orbit) | Boeing 747 *Cosmic Girl* | 6, of which 4 succeeded | 2020–23 | Company closed 2023 |
| Sea Launch (Zenit-3SL) | *Odyssey* platform at the equator, 154° W | 36, of which 3 failed | 1999–2014 | Ended; platform moved to Russia |
| Chinese sea launches | Barges and ships in the Yellow and South China Seas | 28, all successful | 2019–26 | Expanding |
| Russian submarine launches | Shtil' and Volna from submarines in the Barents Sea | 3, of which 1 failed | 1998–2006 | Ended |

: Air and sea launch systems (flights from GCAT, J. McDowell). {#tbl:airsealaunch}

::: ai
**AI on the launch range**

As launch rates climb, ranges are turning to software (Chapter 47). Scheduling several launches a day is an optimisation problem — windows, hazard areas, airspace closures and shared tracking and recovery assets — for which algorithms can propose conflict-free timetables. Weather is a second target: the 45th Weather Squadron's lightning forecasts still rely on statistical tools, but the Air Force Institute of Technology has trained machine-learning models on a decade of weather-balloon data to automate them, and a model from NASA Marshall and the University of Alabama in Huntsville detected 84 % of lightning 15–30 minutes ahead with a 22 % false-alarm rate (Chapter 44). Autonomous flight safety systems remain deliberately simple, verifiable rules; machine learning for debris-risk estimates or faster airspace release must meet the same safety standards.
:::

::: key
**Key takeaways**

- A site at latitude φ can launch directly into inclinations from φ to 180° − φ, with sin *Az* = cos *i* / cos φ. Rotation adds 465 m/s × cos *i*; latitude matters most for geostationary missions.
- Safety corridors decide which azimuths are allowed, explaining Baikonur's 51.6°, Palmachim's retrograde orbits and Florida's polar corridor of 2020.
- In 2025 Florida (109) and Vandenberg (66) hosted more than half of the world's 330 orbital attempts; China flew 93 times, and Rocket Lab's Mahia site outflew Russia.
- A pad combines a flame trench and deflector, a deluge of up to 70 m³/s, umbilical towers, lightning masts and a cryogenic farm. Rockets are stacked vertically and carried out, integrated horizontally and erected, or built on the pad.
- The range tracks the flight, clears hazard areas in the sky and at sea, and recovers boosters, fairings and capsules.
- Weather causes about half of Florida's scrubs; on a July afternoon the chance of launching on a given day can fall below one in two.
- Noise, sonic booms, debris and wildlife make licensing and environmental review a pacing item for new launch sites.
:::

::: questions
**Review questions**

1. Derive the range of inclinations reachable by a direct launch from latitude φ. Which inclinations can Vostochny (51.8° N) reach, and in which two directions can it launch into a 70° orbit?
2. Why does a launch into the ISS orbit gain almost the same velocity from Earth's rotation at Kourou as at Baikonur, while a geostationary mission gains far more at Kourou?
3. Using the worked example's sensitivity (0.82 t per 100 m/s), estimate how much payload a sun-synchronous mission loses to Earth's rotation, and how much a due-east launch from Kourou gains over one from Cape Canaveral.
4. Explain the reasons for Palmachim's westward launches, Sriharikota's dog-leg and Baikonur's minimum inclination of 51.6°.
5. List the main elements of a launch pad and the purpose of each. Why do pads need water at ignition, and what happened when Starship first launched without a flame trench or deluge?
6. Compare vertical assembly and transfer, horizontal integration and vertical integration on the pad. Give one advantage and one drawback of each, with an example vehicle.
7. What is triggered lightning, and which launch commit criteria are designed to prevent it?
8. A launch window opens at 15:00 in August at Cape Canaveral. Using @fig:capeweather and a 10 % technical-scrub probability, estimate the expected number of attempts and the chance of launching within two days.
9. Using the noise model, estimate the distance at which a Falcon Heavy (three Falcon 9 cores) would produce 120 dB. Why might real levels differ?
10. What are the advantages and limitations of air and sea launch? Why are most sea launches today made by solid-fuelled rockets?
:::
