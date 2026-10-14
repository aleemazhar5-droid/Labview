---
title: High-Altitude Platforms and Space Balloons
hero: ch08
abstract: The stratosphere, 18 to 50 kilometres above the ground, is too thin for ordinary aircraft and too dense for satellites. Balloons have explored it for more than a century, and a new generation of solar-powered aircraft and airships - high-altitude platform stations, or HAPS - aims to hover there for months as "pseudo-satellites". This chapter explains the physics of buoyancy and solar-powered flight, the types of balloons and HAPS, their engineering challenges, their applications in science, telecommunications, Earth observation and defence, and the current state of the industry.
---

## Near Space: The Edge of the Atmosphere

"Near space" usually means the region between the highest altitude of conventional aircraft (about 18–20 km) and the lowest altitude of satellites (about 100–160 km). Its lower part, the stratosphere, has properties that make it uniquely useful:

- **Above the weather.** Almost all clouds, storms and turbulence lie in the troposphere below 12–18 km.
- **Above most of the atmosphere.** At 20 km, 95 % of the atmosphere's mass lies below; at 40 km, 99.7 %. Telescopes see in infrared, ultraviolet and X-ray bands that never reach the ground, and cosmic-ray detectors meet primary particles before they shower.
- **Close to the ground.** A platform at 20 km is 25–30 times closer than a low-orbit satellite and 1 800 times closer than a geostationary one. It can see the ground in fine detail with modest optics and communicate with ordinary phones.
- **Calm winds.** Average winds reach a minimum between about 17 and 23 km (@fig:winds), between the tropospheric jet stream and the stronger stratospheric winds above.
- **Above controlled airspace.** In most countries, airspace above about 18 km (FL600 in Europe and the US Class E airspace above FL600) is lightly used, which simplifies operations — although regulators are still developing rules for long-duration HAPS.

Its challenges are equally distinctive: air density at 20 km is only 7 % of sea level (and 0.4 % at 40 km), temperatures fall to −56 °C or lower (−80 °C near the tropical tropopause), ultraviolet radiation and ozone attack materials, and cooling by convection is weak.

![Typical wind speed versus altitude at mid-latitudes. The "HAPS layer" between about 17 and 23 km has the weakest winds, making station-keeping practical.](figures/out/ch08_winds.svg){#fig:winds width=72%}

## The Physics of Buoyancy

### Archimedes in the Stratosphere

A balloon floats when the weight of the air it displaces equals the total weight of the balloon, its gas and its payload. The net (free) lift of a volume $V$ of lifting gas is

$$L = V\,(\rho_{air} - \rho_{gas})\,g = V\,\rho_{air}\left(1 - \frac{M_{gas}}{M_{air}}\right) g$$

assuming the gas and surrounding air have the same pressure and temperature, where $M$ is the molar mass. Helium ($M$ = 4.0 g/mol) gives 86 % of the lift of a vacuum; hydrogen ($M$ = 2.0 g/mol) 93 %. Hydrogen is cheaper and lifts more but is flammable; helium is inert but scarce and expensive, and some programmes (including Loon and many weather services) use hydrogen.

Because air density falls exponentially with height, the lift of each cubic metre of gas falls by a factor of about 160 between sea level and 40 km (@fig:lift). A balloon must therefore expand enormously as it rises. A NASA 40 MCF (million cubic feet) zero-pressure balloon has a volume of 1.13 million m³ at float — large enough to hold a football stadium — yet at launch only a small bubble at its top is filled with helium; the rest of the polyethylene film hangs limp below.

![Left: net lift per cubic metre of helium and hydrogen versus altitude. Right: balloon volume required at float to carry a given payload, assuming the total system mass is about 1.6 times the suspended load.](figures/out/ch08_lift.svg){#fig:lift width=100%}

::: example
**Worked example — how big a balloon for a 2-tonne telescope at 38 km?**

At 38 km the US Standard Atmosphere gives ρ ≈ 0.0058 kg/m³. Each cubic metre of helium lifts $0.0058\times(1 - 4.00/28.96) = 0.0050$ kg = 5.0 g. The suspended load of 2 000 kg plus the balloon film (≈ 1 800 kg for a 1 million m³ balloon), ballast, parachute and rigging gives a gross mass of about 3 200–4 000 kg, so the balloon needs about **650 000–800 000 m³** at float. NASA would fly this on a 29–40 MCF balloon (0.8–1.13 million m³). The film is polyethylene only about 20 µm thick — thinner than a sandwich bag — so that the balloon itself does not become too heavy.
:::

### Thermal Effects and Super-Pressure

The lift of a balloon depends on the gas temperature. During the day, sunlight and upwelling infrared warm the gas above the surrounding air ("superheat"), increasing lift; at sunset the gas cools by 20–40 K and lift falls sharply. This drives the main design distinction between balloon types:

- A **zero-pressure balloon** is open at the bottom through vent ducts, so internal and external pressures are equal. When the gas cools at night it contracts, the balloon loses lift and sinks; to stop the descent, ballast (fine steel shot or glass beads) is dropped. Each night costs typically 5–10 % of the gross mass in ballast, limiting flights to days or a few weeks — except in polar summer, when the Sun never sets (@fig:diurnal).
- A **super-pressure balloon (SPB)** is sealed. It is designed so that, even when the gas is coldest at night, it is still fully inflated with a slight overpressure; at noon the overpressure rises, but the volume (and therefore the altitude) barely changes. Super-pressure balloons can fly for months without ballast. The challenge is building a hull that withstands the pressure difference: NASA uses a "pumpkin" design of polyethylene gores with high-strength load tendons, while Loon used a smaller, simpler polyethylene envelope.

![Schematic altitude history over four days for zero-pressure and super-pressure balloons. Night-time descent forces a zero-pressure balloon to drop ballast; a super-pressure balloon holds altitude.](figures/out/ch08_diurnal.svg){#fig:diurnal width=88%}

## Types of Balloons

@fig:balloontypes and @tbl:balloons summarise the main families.

![The three main families of free balloons: latex sounding balloons that burst, zero-pressure balloons that vent gas, and sealed super-pressure balloons.](figures/out/ch08_balloon_types.svg){#fig:balloontypes width=96%}

Table: Main types of free balloons. {#tbl:balloons}

| Type | Typical volume | Payload | Float altitude | Duration | Main users |
|---|---|---|---|---|---|
| Latex sounding (weather) balloon | 1–3 m³ at launch (bursts at ≈ 10 m diameter) | 0.1–3 kg (radiosonde) | Rises to 30–35 km, bursts | 1.5–3 h | Weather services: ≈ 800 stations launch twice daily (≈ 1 500 per day worldwide) |
| Small zero-pressure | 1 000–100 000 m³ | 5–500 kg | 25–35 km | Hours–days | Universities, atmospheric chemistry, technology tests |
| Large zero-pressure ("heavy lift") | 0.3–1.13 million m³ | 1 000–3 600 kg | 35–42 km | 1 day (conus), 10–57 days (polar) | NASA, CNES, JAXA, ISRO: astrophysics, cosmic rays |
| Super-pressure (scientific) | ≈ 530 000 m³ (18.8 MCF) | up to ≈ 1 t | ≈ 33 km | Weeks–months | NASA SPB programme (Wanaka, New Zealand) |
| Small super-pressure | 10–500 m³ | 1–50 kg | 15–20 km | Weeks–months | CNES Stratéole-2, Loon (ended 2021), Aerostar, World View |
| Montgolfière / infrared balloon | variable | small | 20–30 km | Weeks | CNES (historic MIR balloons), Venus concepts |
| Tethered aerostat | 100–10 000 m³ | 50–1 000 kg | 0.5–5 km | Weeks | Border surveillance, telecom relays |

### Scientific Ballooning

Balloons have been scientific platforms since Victor Hess discovered cosmic rays on a manned balloon flight in 1912 (Nobel Prize 1936). In the space age they remain the cheapest way to reach near-space conditions with heavy instruments, and they are an important training ground for instrument scientists. Notable achievements include:

- **BOOMERanG** (1998) and **MAXIMA** — balloon-borne measurements of the cosmic microwave background that established that the universe is geometrically flat.
- **BLAST** — sub-millimetre surveys of star-forming galaxies; **SPIDER** — CMB polarisation from Antarctica.
- **CREAM** and **SuperTIGER** — direct measurements of heavy cosmic-ray nuclei; SuperTIGER flew 55 days over Antarctica in 2012–13.
- **GUSTO** (Galactic/Extragalactic ULDB Spectroscopic Terahertz Observatory) — a terahertz telescope that flew about 57 days over Antarctica from December 2023, a record for a NASA heavy-lift balloon.
- **COSI** — a Compton gamma-ray telescope whose 2016 super-pressure flight paved the way for the COSI satellite (launch planned 2027).
- **EUSO-SPB2** (2023) — ultra-high-energy cosmic-ray and neutrino detection from a super-pressure balloon.
- **Stratéole-2** (CNES/LMD) — fleets of small super-pressure balloons drifting for months in the tropical lower stratosphere, measuring winds, temperature, water vapour and waves; they also provided validation data for the Aeolus wind lidar satellite.

NASA's **Columbia Scientific Balloon Facility (CSBF)**, operated from Palestine, Texas, launches from Fort Sumner (New Mexico), Palestine, McMurdo Station (Antarctica), Kiruna (Sweden), Wanaka (New Zealand) and Alice Springs (Australia). Antarctic **long-duration balloon (LDB)** flights exploit the austral summer — continuous daylight and a circumpolar wind pattern that returns the balloon close to McMurdo after one to three circuits of the continent. CNES operates from Aire-sur-l'Adour, Kiruna, Timmins (Canada) and the Seychelles; JAXA from Taiki (Hokkaido); ISRO from Hyderabad.

::: figrow
![A NASA super-pressure balloon carrying the COSI gamma-ray telescope ready for launch from McMurdo Station, Antarctica, in the 2014–15 campaign.](figures/photos/ch08_ldb.jpg){#fig:ldbphoto}

![The launch vehicle holds the ANITA radio-antenna payload, which searches for ultra-high-energy neutrinos interacting in the Antarctic ice, moments before a long-duration balloon launch.](figures/photos/part2.jpg){#fig:anita}
:::

### Balloon Operations

A heavy-lift launch begins before dawn in calm winds (typically below 3 m/s at the surface and in the first few hundred metres). The payload hangs from a launch vehicle — a large mobile crane — while the balloon is laid out on a ground cloth and its top bubble is inflated with helium through fill tubes. On release, the bubble rises and lifts the rest of the balloon off the ground; the launch vehicle drives underneath to release the payload smoothly. Ascent takes 2–3 hours at about 5 m/s.

At float, the payload is controlled from the ground through line-of-sight telemetry, Iridium, TDRS or Starlink links. The flight is terminated by command: a pyrotechnic cutter releases the payload, which descends on a large parachute, while a rip panel opens the balloon so that it falls separately. Recovery teams then retrieve payloads, sometimes from remote Antarctic plateaus by aircraft. Safety rules forbid termination over populated areas, which limits flights from continental sites.

Engineers' main challenges include balloon film reliability (cold embrittlement at the tropopause), thermal control of payloads (convective cooling is weak but not absent), pointing of telescopes from a swinging gondola (arcsecond-level pointing is achieved with momentum wheels, reaction against the flight train, and star cameras), power (solar panels), and communications.


### Balloon and Gondola Design

**Envelope design.** A zero-pressure balloon at float takes up a "natural shape" — an inverted teardrop in which the film carries tension only along the meridians (@fig:naturalshape). The shape is computed by solving the equilibrium between internal gas pressure (which increases with height inside the balloon, because the gas column is lighter than the surrounding air), film weight and the tension carried by **load tapes** that run from the apex to the base along every seam. NASA's large balloons are made from dozens to more than 200 **gores** — long, narrow panels of linear low-density polyethylene film 20–38 µm thick, heat-sealed together. The film must stay flexible at the −80 °C tropopause, resist ultraviolet light, and have no pinholes. Manufacturing is done by hand on tables more than 100 m long; a 40 MCF balloon contains about 24 hectares of film.

![Construction of a zero-pressure balloon at float. Load tapes along the gore seams carry the payload weight to the apex; vent ducts release gas when the balloon is fully inflated.](figures/out/ch08_natural_shape.svg){#fig:naturalshape width=86%}

**Super-pressure hulls.** NASA's 18.8 MCF super-pressure balloon uses a "pumpkin" shape: the film bulges between high-strength tendons so that the film itself carries only a small local stress while the tendons carry the global load. Developing a reliable pumpkin balloon took more than a decade because of a deployment instability ("clefting") in which the lobes fold incorrectly during inflation. Flights from Wanaka, New Zealand, have lasted up to about 55 days at mid-latitudes; a 2025 campaign carried the HIWIND thermospheric wind instrument on a flight of about 17.5 days and launched a second balloon intended for up to 100 days.

**Gondolas.** The science payload hangs in a **gondola** — an aluminium or carbon-fibre frame carrying the instrument, solar panels, batteries, flight computers, telemetry, and crush pads for landing (@fig:gondola). Astrophysics gondolas point telescopes to a few arcseconds: azimuth is controlled by a motorised pivot that torques against the balloon flight train and by a reaction wheel, while elevation is controlled by driving the telescope itself; attitude is sensed with daytime star cameras, gyros, GPS compasses and sun sensors. Gondolas must survive a parachute landing at 5–8 m/s and, for the heaviest payloads, the "opening shock" of the parachute (up to 8–10 g).

![A typical balloon-borne astrophysics gondola. Solar panels hang outside; the instrument points by torquing against the flight train.](figures/out/ch08_gondola.svg){#fig:gondola width=86%}

### Radiosondes: Balloons for Every Weather Forecast

The most numerous balloons by far are the small latex balloons that carry **radiosondes** — the backbone of upper-air meteorology since the 1930s. About 800 stations in the WMO Global Observing System launch them, mostly at 00 and 12 UTC, adding up to roughly 1 500 soundings per day worldwide. A modern radiosonde (for example the Vaisala RS41, Graw DFM-17 or Meteomodem M20) weighs 80–110 g and measures temperature (with a small platinum or thermistor sensor), relative humidity (thin-film capacitive sensor), pressure (or derives it from GNSS height) and — by tracking its GNSS position — winds. It transmits at around 400 MHz to a ground receiver for the 1.5–2-hour ascent, reaching 30–35 km before the balloon bursts (@fig:sounding).

![A schematic mid-latitude radiosonde profile: temperature falls through the troposphere to the tropopause, the dew point shows how moist the air is, and winds peak in the jet stream near 10–12 km.](figures/out/ch08_sounding.svg){#fig:sounding width=90%}

Radiosonde data, though few compared with satellite observations, are among the most valuable inputs to numerical weather prediction because they measure vertical profiles directly and serve as an absolute reference to calibrate satellite sounders (Chapter 16). **Dropsondes**, released from aircraft into hurricanes and storms, use the same technology in reverse. Weather-balloon launch stations are increasingly automated with "autolaunchers" that inflate and release balloons without staff.

## High-Altitude Platform Stations (HAPS)

### The Pseudo-Satellite Concept

A **high-altitude platform station** (the ITU term) or **high-altitude pseudo-satellite** is an aircraft, airship or balloon that stays in the stratosphere — typically at 18–25 km — for weeks to months, holding position over a region like a geostationary satellite but much closer to the ground. HAPS promise:

- **Telecommunications** directly to unmodified phones (4G/5G "cell tower in the sky") over an area 100–200 km across, with latency below a millisecond, for rural connectivity, disaster recovery and events.
- **Earth observation** with persistence: continuous imaging of one area at 10–20 cm resolution, rather than a satellite snapshot once or twice a day — for wildfire monitoring, maritime surveillance, border security, crop monitoring and environmental science.
- **Navigation augmentation** and **defence** applications such as communications relays and persistent intelligence, surveillance and reconnaissance (ISR).
- **Rapid deployment** without launch: a HAPS can be repositioned or recovered and upgraded.

The ITU allocated spectrum for HAPS (in bands near 2 GHz, 6 GHz, 21–31 GHz and 38–48 GHz) at WRC-19 and, at WRC-23, approved the use of HAPS as **IMT base stations (HIBS)** in mobile bands below 2.7 GHz, allowing them to serve ordinary phones.

![Coverage radius on the ground versus platform altitude for three minimum elevation angles. A stratospheric platform covers a city-sized region; a LEO satellite covers a much larger area but moves away within minutes.](figures/out/ch08_coverage.svg){#fig:coverage width=86%}

### Three Architectures

HAPS designs fall into three families (@fig:hapsarch), each with distinct trade-offs:

![The three HAPS architectures and their main advantages and limitations.](figures/out/ch08_haps_arch.svg){#fig:hapsarch width=98%}

**Solar-powered fixed-wing aircraft (heavier than air).** Extremely light, high-aspect-ratio wings covered in solar cells power electric propellers by day and charge batteries for the night. Airbus' **Zephyr** — now operated by **AALTO HAPS** — has a 25 m wingspan and a mass of about 75 kg; in 2022 it flew 64 days continuously, and AALTO reported a new record of about 67 days in 2025, with commercial service targeted from 2026 (including an operating base in Kenya). BAE Systems' **PHASA-35** (35 m span, 150 kg) completed stratospheric trials in 2023–2024; AeroVironment/SoftBank's **Sunglider** (78 m) flew to the stratosphere in 2020. NASA's **Pathfinder**, **Centurion** and **Helios** prototypes pioneered the concept: Helios reached a record 29.5 km in 2001 before breaking up in turbulence in 2003.

![NASA's Helios prototype, a 75 m solar-electric flying wing, taking off from the Pacific Missile Range Facility on Kauai, Hawaii, for its 2001 record flight to an altitude of 29 524 m — a record for a non-rocket-powered aircraft in sustained horizontal flight.](figures/photos/ch08_helios.jpg){#fig:helios width=84%}

**Airships (lighter than air, powered).** Stratospheric airships use helium for lift and solar-powered propellers to hold position. Their large volume (typically 50–100 m long) gives large solar arrays and payloads of 100 kg or more. **Sceye** (USA) has flown a series of stratospheric airship tests from New Mexico since 2021, including a long-distance mission, and announced plans with SoftBank to start pre-commercial services in Japan in 2026. Thales Alenia Space's **Stratobus** and Lockheed Martin's **HiSentinel** are other examples. The difficulty is drag: a large envelope must push against winds that can exceed 20–30 m/s at times.

**Free balloons with altitude control (lighter than air, unpowered).** Google's **Loon** (2013–2021) showed that super-pressure balloons can be "steered" by changing altitude to catch winds blowing in different directions, using an air-ballast pump (a "ballonet") and machine-learning navigation (Chapter 44). Loon flew more than 40 million km in total, set a record of 312 days aloft for one balloon, and provided emergency LTE service in Puerto Rico after Hurricane Maria (2017) and commercial service in Kenya (2020) before closing in 2021 because the business case did not close. Its flight data were published for research. **Aerostar** (Thunderhead balloons) supplies similar balloons for US defence experiments; **World View**, **Urban Sky**, **Near Space Labs** and others offer stratospheric imaging and ride services.

### Engineering Challenges

**Energy closure.** The defining problem of solar HAPS is surviving the night. The platform must collect enough energy during the day to fly all day and night. @fig:hapsenergy shows that at the equator a horizontal wing collects about 10 kWh/m²/day, but at 50° latitude in winter only about 2 kWh/m²/day — with 16-hour nights. With present batteries (lithium-ion at 250–350 Wh/kg; lithium-sulphur and silicon-anode cells promising 400–500 Wh/kg) and solar cells (thin-film or lightweight multi-junction, 20–30 %), most fixed-wing HAPS can operate year-round only within about ±25–35° of the equator. Batteries often make up 30–40 % of the aircraft mass.

![Clear-sky solar irradiance on a horizontal wing at 20 km over one day for four latitude/season combinations. The energy collected per day ranges from about 12 kWh/m² in midsummer at 50° N to 2 kWh/m² in midwinter — the central design challenge for solar HAPS.](figures/out/ch08_haps_energy.svg){#fig:hapsenergy width=88%}

The power needed for level flight follows from aerodynamics. For an aircraft of mass $m$, wing area $S$, lift coefficient $C_L$ and drag coefficient $C_D$ flying at air density $\rho$:

$$P_{level} = \frac{D\,v}{\eta_{prop}} = \frac{m g}{\eta_{prop}}\,\frac{C_D}{C_L}\sqrt{\frac{2 m g}{\rho S C_L}}$$

Because $\rho$ at 20 km is 14 times smaller than at sea level, the flight speed — and power — is $\sqrt{14} \approx 3.7$ times greater for the same aircraft. HAPS aircraft therefore have very low wing loadings (2–4 kg/m², a hundred times less than an airliner), very high lift-to-drag ratios (25–40), and must be extraordinarily light.

**Structural fragility and weather.** The lightest structures are vulnerable during ascent and descent through the troposphere, where turbulence and gusts are strongest. Most HAPS losses have occurred in these phases: Helios broke up in turbulence in 2003; a Zephyr crashed after 64 days in 2022; Facebook's Aquila programme ended in 2018 after a landing accident. Launch windows require calm surface winds.

**Station-keeping.** To act as a pseudo-satellite, a platform must stay within a station-keeping circle of perhaps 5–20 km radius. Aircraft fly loiter patterns; airships push against the wind; balloons use altitude control or fleets.

**Thermal and materials.** Cold temperatures (−60 to −80 °C) reduce battery capacity and make films brittle; ultraviolet radiation and ozone degrade polymers; solar cells run hot in weak convection.

**Regulation.** Long-endurance HAPS require certification and airspace rules that do not yet exist in many countries; flights through lower airspace must be coordinated with air-traffic control.


### HAPS Payloads

**Telecommunications payloads.** A HAPS base station uses a phased-array or multi-beam antenna that projects tens of "cells" onto the ground, each acting like a terrestrial cell sector. Because the platform moves within its station-keeping circle and changes attitude, beams are steered electronically to stay fixed on the ground. The feeder link to a ground gateway (or to a satellite) uses Ka- or E-band, or free-space optics. Japan's SoftBank/HAPSMobile demonstrated LTE connectivity from Sunglider in 2020 and 5G-class links from Sceye in later tests; Loon's balloons relayed traffic between balloons over hundreds of kilometres using millimetre-wave mesh links. Capacity per HAPS is typically hundreds of Mbit/s to a few Gbit/s.

**Earth-observation payloads.** At 20 km, a camera with a 10 cm aperture achieves sub-metre resolution; 20–30 cm resolution is achievable with payloads of only a few kilograms. HAPS EO payloads include visible/near-infrared cameras, thermal infrared cameras for wildfire detection, hyperspectral imagers, and small synthetic aperture radars. Their key advantage is **persistence** — the same area can be watched continuously for hours or days, enabling detection of change and movement that satellites revisiting once a day would miss.

**Science payloads.** Stratospheric aircraft and airships can carry in-situ sensors for ozone, water vapour and aerosols, and long-duration balloons carry instruments for gravity-wave, atmospheric-chemistry and climate studies.

::: data
**Data box — representative HAPS (2026)**

| Platform | Type | Span / length | Mass | Payload | Endurance (demonstrated) |
|---|---|---|---|---|---|
| AALTO Zephyr S | Solar aircraft | 25 m | ≈ 75 kg | ≈ 5 kg | ≈ 64–67 days |
| BAE PHASA-35 | Solar aircraft | 35 m | ≈ 150 kg | ≈ 15 kg | Stratospheric trials (hours–days) |
| Sceye | Solar airship | ≈ 65 m | ≈ 1 t-class | 100–250 kg (planned) | Multi-day missions |
| Loon (retired) | Super-pressure balloon | 15 m diameter | ≈ 75 kg (+ payload) | ≈ 15 kg | 312 days (record) |
| NASA super-pressure | Balloon | 0.53 million m³ | ≈ 2.5 t system | ≈ 1 t | ≈ 55 days (2016 record flights) |
:::

### Applications and Business Case

The HAPS industry has experienced several boom-and-bust cycles: Google (Loon, Titan), Facebook (Aquila) and others invested heavily in the 2010s and withdrew. The renewed wave in the mid-2020s rests on better batteries, regulatory progress (WRC-23 HIBS decisions), defence demand for persistent ISR and communications, and partnerships with mobile network operators (e.g., SoftBank, NTT Docomo, Deutsche Telekom, Vodafone in trials). HAPS compete with — and complement — LEO direct-to-device satellites (Chapter 17), drones, and terrestrial towers. Their advantages are persistence over one area, low latency, high capacity density and low cost per unit area served; their disadvantages are weather sensitivity during ascent/descent, latitude limits and the need for fleets to provide continuous service.

## Other Near-Space Vehicles

- **High-altitude aircraft.** The Lockheed U-2 and NASA's **ER-2** fly at up to about 21 km with a pilot in a pressure suit, carrying Earth-science instruments that test future satellite sensors. NASA's WB-57 (18 km) supports eclipse observations and launch tracking.
- **High-altitude drones.** RQ-4 Global Hawk (18 km, 34+ h endurance) and Chinese, European and Israeli equivalents.
- **Stratospheric tourism.** Several companies planned pressurised-capsule balloon flights to about 30 km. Space Perspective (Neptune capsule) flew an uncrewed test in 2024 but ran into financial difficulty and was acquired by the Spanish company **EOS X Space** in 2025; Zephalto (France) and Halo Space (Spain) pursue similar concepts. Such flights are not spaceflight by any definition but offer views of Earth's curvature and the black sky.
- **Record jumps.** Joseph Kittinger (31.3 km, 1960), Felix Baumgartner (39.0 km, 2012, supersonic freefall) and Alan Eustace (41.4 km, 2014) used balloons to test pressure suits and parachute systems relevant to crew escape.

![NASA's ER-2 high-altitude research aircraft in flight. Flying at up to 21 km, ER-2s carry prototypes of satellite instruments and collect validation data for Earth-observation missions.](figures/photos/ch08_er2.jpg){#fig:er2 width=78%}

![Operating altitude versus typical or record endurance for atmospheric and stratospheric platforms. HAPS occupy a niche between aircraft (hours) and satellites (years).](figures/out/ch08_platforms.svg){#fig:platforms width=90%}


## Case Studies

### Loon: Navigating by the Wind

Loon's balloons were 15 m-diameter super-pressure envelopes carrying about 15 kg of electronics powered by solar panels. Each balloon could change its altitude between about 15 and 20 km by pumping air into or out of an internal ballonet. Because winds at different altitudes blow in different directions, choosing an altitude was equivalent to choosing a direction. A fleet-management system combined global weather forecasts with real-time wind measurements from the balloons themselves to plan altitude changes. In 2020 Loon published results showing that a **deep reinforcement-learning controller**, trained in simulation, kept balloons near their target station more effectively than the hand-engineered controller — one of the first operational uses of reinforcement learning in aerospace (Chapter 44). Loon's lessons for the industry included the value of fleet operations, the importance of regulatory partnerships in each country, and the difficulty of competing economically with terrestrial towers and LEO satellites.

### Zephyr: Surviving the Night

Zephyr's flights illustrate the energy balance of solar HAPS. The aircraft climbs through the troposphere at dawn, reaches the stratosphere by mid-morning, and continues climbing to 21–23 km while its batteries charge. At night it slowly descends — storing energy as altitude in a glider-like "potential-energy battery" — to about 15–18 km by dawn, when the cycle repeats. Zephyr's record flights were made from Arizona in northern summer, when nights are short; year-round operation is planned from low-latitude bases such as Kenya.

### Stratéole-2: Science in the Tropical Stratosphere

The French–American Stratéole-2 programme launches fleets of small super-pressure balloons from the Seychelles that drift around the Earth in the tropical lower stratosphere at 18–20 km for up to three months. They carry instruments for winds, temperature, water vapour, aerosols and clouds, and lidar and GNSS radio-occultation profilers. The data improve understanding of the quasi-biennial oscillation, gravity waves and stratospheric water vapour, and validated the Aeolus Doppler wind lidar satellite.

## Safety and Regulation

Free balloons are regulated as aircraft. In the United States, 14 CFR Part 101 sets rules for unmanned free balloons: heavy balloons (payloads above 6 lb with certain density limits, or above 12 lb) require notification of air-traffic control, position reporting, lighting, and a reliable termination system. ICAO Annex 2 provides the international framework, and balloons crossing borders need overflight permissions. Scientific balloon programmes conduct casualty-risk analyses for descent and terminate flights only over unpopulated areas. HAPS aircraft are being certified under special conditions developed by the European Union Aviation Safety Agency (EASA), the US FAA and national authorities, and ICAO is developing provisions for operations above FL600 ("higher airspace operations").

## Balloons on Other Worlds

Balloons can also explore other planets. In 1985 the Soviet **Vega 1** and **Vega 2** missions released two 3.5 m helium balloons into the atmosphere of **Venus** at about 54 km altitude; they floated for about 46 hours each, travelling more than 11 000 km in the super-rotating winds and transmitting data to an international network of radio telescopes on Earth. NASA and JPL have studied variable-altitude "aerobots" for Venus (tested in the Nevada desert in 2022), and Titan's thick, cold atmosphere would make balloon (or rotorcraft) flight easy — the basis of NASA's Dragonfly mission (Chapter 28). Mars' thin atmosphere makes balloons very large; concepts use super-pressure or solar-heated Montgolfière designs.

## Near Space as a Test Bed for Space Systems

The stratosphere above 30 km has less than 1 % of sea-level pressure and conditions resembling Mars' surface pressure (≈ 600 Pa at about 35 km). It is therefore used to test:

- **Mars entry, descent and landing systems** — NASA's Viking parachutes (1972) and the **Low-Density Supersonic Decelerator (LDSD)** tests (2014–2015) were dropped from balloons at 37 km and accelerated by rockets to Mars-relevant supersonic speeds.
- **Space instruments** — detectors, star trackers and telescopes are flown on balloons before satellite missions.
- **Mars aircraft and balloons** — prototypes of planetary aerial vehicles.
- **Astrobiology** — sampling of microbes carried to the stratosphere and survival studies.

::: key
**Key takeaways**

- The stratosphere offers a unique vantage point: above weather and most of the atmosphere, close to the ground, with a wind minimum near 20 km.
- Balloon lift comes from displaced air; lift per cubic metre falls about 160-fold from sea level to 40 km, so stratospheric balloons reach volumes of up to 1.13 million m³.
- Zero-pressure balloons vent gas and must drop ballast at night; sealed super-pressure balloons hold altitude for months.
- HAPS — solar aircraft, airships and steerable balloons — aim to be persistent "pseudo-satellites" for telecom and Earth observation; the energy balance of the night limits fixed-wing HAPS to lower latitudes with current batteries.
- After earlier boom-and-bust cycles, HAPS are approaching commercial service in the mid-2020s, supported by ITU spectrum decisions and defence demand; balloons remain the cheapest route to near-space science.
:::
