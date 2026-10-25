---
title: Space Resources and Asteroid Mining
hero: ch41
abstract: Every kilogram of propellant, water or shielding used beyond Earth orbit must be lifted out of a deep gravity well at great cost. Space resources — ice and oxygen-rich rock on the Moon, carbon dioxide and ice on Mars, water and metals in asteroids — promise to cut that cost by making what is needed where it is needed. This chapter quantifies the "gear ratio" that makes local production attractive, surveys what is known about each resource, and explains the processes that turn regolith and ice into water, oxygen, propellant, metals and building material, with their energy costs. It then reviews the prospecting missions from LCROSS to VIPER, the rise and fall of asteroid-mining companies, the economics of selling space metals on Earth, and the laws that decide who may own what is extracted.
---

Polar explorers of the nineteenth century hauled everything they needed on sledges until they learned to hunt and to build shelters from snow. Spaceflight is still in the sledge-hauling era: every Apollo crew carried all its oxygen, water and propellant from Earth, and every robotic lander since has done the same. Because of the exponential rocket equation, the penalty is severe — with the assumptions used in this chapter, placing one kilogram on the lunar surface requires about 130 kg of rocket on the launch pad.

**In situ resource utilisation (ISRU)** — from the Latin *in situ*, "in place" — means producing useful materials from what is found at the destination. The most valuable products are mundane: **oxygen**, about four-fifths of the propellant mass of hydrogen–oxygen and methane–oxygen rockets; **water**, for drinking, growing food and radiation shielding; and **regolith**, the loose rock and dust covering the Moon, Mars and asteroids, for building landing pads, roads and shelters. Further away in time and economic plausibility lie metals for construction in space, and precious metals and helium-3 for sale on Earth.

This chapter starts with the arithmetic that makes space resources attractive, then surveys the resources, the chemistry and energy cost of extracting them, the prospecting missions, the companies that have tried to mine them and the law that governs ownership. Landers and rovers are covered in Chapters 27 and 28, propellant transfer in orbit in Chapter 40 and life support in Chapter 30.

## Why Use Space Resources?

### The Gear Ratio

The rocket equation (Chapter 34), $\Delta v = v_e \ln(m_0/m_f)$, makes the mass needed grow exponentially with the velocity change. Reaching low Earth orbit (LEO) takes about 9.4 km/s including losses, so even a large launcher delivers only about 4 % of its lift-off mass to orbit. From LEO, a further 4.0 km/s reaches low lunar orbit (LLO) and 5.9 km/s the lunar surface. The ratio between the mass leaving Earth and the mass delivered is called the **gear ratio** of a destination (@fig:gearratio a).

![The gear ratio of space resources. (a) Mass that must leave its source for each kilogram of propellant delivered to four destinations: Earth lift-off mass for propellant launched from Earth, and lunar propellant for a reusable lunar tanker. (b) Earth lift-off mass per kilogram of propellant delivered to low lunar orbit or Earth–Moon L1, against the productivity of a lunar plant (kilograms produced per kilogram of plant and tanker landed from Earth).](figures/out/ch41_gear.svg){#fig:gearratio width=98%}

With hydrogen–oxygen stages of specific impulse 450 s whose empty mass is 10 % of their propellant, each kilogram delivered to LLO needs 2.9 kg in LEO and about 73 kg at lift-off; each kilogram on the lunar surface needs 5.3 kg in LEO and 132 kg at lift-off. Propellant made on the Moon starts at the bottom of a far shallower gravity well — the Moon's escape velocity is 2.4 km/s against Earth's 11.2 km/s, and there is no atmosphere. A reusable tanker that carries lunar propellant to LLO, keeping enough to fly back down, burns only about 1.1 kg for every kilogram it delivers: a gear ratio of 2.1 instead of 73. Delivery to the Earth–Moon L1 point, a proposed depot site, costs 2.7.

The comparison reverses in LEO. A tanker can brake into LEO using the atmosphere (aerobraking), so the outbound trip needs only about 2.8 km/s, but it then needs the full 5.9 km/s to return to the Moon. Each kilogram delivered costs 34 kg of lunar propellant — worse than launching from Earth — unless the tanker refuels at L1 on the way back, which cuts the figure to about 4. Lunar propellant is most valuable close to the Moon, where Earth-launched propellant is most expensive.

### When Does Local Production Pay?

A lunar plant is not free: its excavators, reactors, power system and tanker must be landed from Earth at 132 kg of lift-off mass per kilogram. The figure of merit is the plant's **productivity** $P$, the mass of product made over its life divided by its own landed mass. @fig:gearratio b shows that lunar propellant delivered to LLO beats Earth-launched propellant once $P$ exceeds about 3.8, and at L1 once it exceeds about 5.2. Chemical plants on Earth produce their own mass in days or weeks; the open question is whether a lunar plant can survive abrasive dust, temperatures from 40 K to 390 K and years without maintenance long enough to do the same.

::: example
**Example: the leverage of a lunar-orbit tanker**

A reusable tanker with an empty mass of 10 t carries 30 t of liquid oxygen and hydrogen from a polar plant to a depot in low lunar orbit and returns. Its engines have $I_{sp}$ = 450 s ($v_e$ = 4 413 m/s); each leg needs Δv = 1.9 km/s.

1. Mass ratio per leg: $R = e^{1\,900/4\,413}$ = 1.538.
2. Ascent propellant (10 t of tanker plus 30 t of cargo): 40 × (1.538 − 1) = 21.5 t. To return, the empty tanker keeps 10 × 0.538 = 5.4 t, so it delivers 30 − 5.4 = **24.6 t** per trip.
3. Lunar production per trip: 21.5 + 30 = 51.5 t — a gear ratio of 51.5 / 24.6 = **2.09**.
4. Delivering 24.6 t from Earth instead would need 24.6 × 2.90 = 71.5 t in LEO, or about **1 790 t** of launch vehicle at lift-off.
5. Suppose the plant, its power supply and the tanker land 40 t from Earth (5 290 t at lift-off) and produce 100 t of propellant a year for 10 years ($P$ = 25). They deliver 1 000 / 2.09 = 478 t to LLO, at 5 290 / 478 = **11 kg** of Earth lift-off mass per kilogram, against 73 kg for Earth-launched propellant — a sixfold gain. At $P$ = 3.8 the advantage vanishes.
:::

The same logic applies to Mars, where an ascent from the surface needs about 4–5 km/s (Chapter 29), and to products other than propellant: a tonne of regolith piled over a habitat as radiation shielding is a tonne that need not be launched.

## What Is Out There

The resources differ in concentration by a factor of a billion — from oxygen, nearly half of every rock, to helium-3, a few parts per billion of lunar soil (@tbl:resinventory). @fig:rescomp compares the elemental make-up of typical feedstocks.

| Resource | Where | Typical concentration | Main products | Key uncertainty |
|---|---|---|---|---|
| Polar water ice | Lunar cold traps (≈ 40 000 km²) | 0 to > 10 % by mass; 5.6 % in LCROSS plume | Water, H₂, O₂ | Amount, depth, patchiness |
| Oxides in regolith | Everywhere on the Moon | O 41–45 %, Fe up to 15 %, Al up to 14 % | O₂, Fe, Si, Al, Ti | Energy per kg |
| Solar-wind volatiles | Lunar regolith, esp. Ti-rich mare | H tens of ppm; ³He ≈ 4–20 ppb | H₂O, ³He | Very low grade |
| Atmospheric CO₂ | All of Mars | 95 % of a 0.6 kPa atmosphere | O₂, CO, CH₄ (with H₂) | Power, dust |
| Water on Mars | Poles, buried ice, soil | ≈ 2 % in soil to near-pure ice | Water, H₂ | Depth and access |
| Carbonaceous asteroids | Outer main belt; some NEAs | Up to ≈ 18 % water-equivalent, C 3–4 % | Water, carbon, organics | Access, anchoring |
| Metallic asteroids | Rare; Psyche; a few NEAs | Fe–Ni ≈ 90 %+, platinum-group metals 10–40 ppm | Metals | Composition, market |

: The main resources beyond Earth. {#tbl:resinventory}

![Elemental composition (by mass) of representative feedstocks: lunar highland and mare soils, Martian soil at Gale crater, and the meteorite types that correspond to C-, S- and M-type asteroids.](figures/out/ch41_composition.svg){#fig:rescomp width=96%}

### Lunar Regolith

The Moon is covered by **regolith**, rock fragments, glass and dust produced by four billion years of meteorite impacts, about 4–5 m deep on the dark volcanic plains (**maria**) and 10–15 m in the older **highlands**. Most grains are smaller than 1 mm, and every one is an oxide: oxygen makes up 41–45 % of the mass, bound to silicon, aluminium, iron, calcium, magnesium and titanium. Highland soils are rich in aluminium and calcium from the mineral plagioclase. Mare soils carry up to about 20 % FeO and, in the "high-titanium" basalts sampled by Apollo 11 and 17, 10 % or more of the iron–titanium oxide **ilmenite** (FeTiO₃), the favourite feedstock for oxygen extraction (@fig:ilmenitethin). Volcanic glass beads, such as the orange soil found by Apollo 17 (@fig:orangesoil), are also rich in iron and titanium oxides and react readily.

::: figrow
![Photomicrograph of a thin slice of Apollo 11 basalt 10022. Black grains are ilmenite, light blue and white grains are plagioclase and the brightly coloured grains are pyroxene.](figures/photos/ch41_ilmenite.jpg){#fig:ilmenitethin}

![The orange soil discovered by Apollo 17 at Shorty crater in December 1972 — tiny beads of volcanic glass rich in titanium and iron.](figures/photos/ch41_orange.jpg){#fig:orangesoil}
:::

Regolith also holds atoms of the **solar wind** — hydrogen, helium, carbon and nitrogen implanted into grain surfaces — with hydrogen at tens of parts per million (ppm), highest in fine, ilmenite-rich mare soils. On the western near side, the **Procellarum KREEP Terrane** is enriched in potassium (K), rare-earth elements (REE) and phosphorus (P), together with thorium and uranium mapped from orbit by Lunar Prospector. Its rare-earth concentrations are hundreds of times those of primitive meteorites but far below those of rich ores on Earth: they are of scientific rather than commercial interest.

### Ice at the Poles

The Moon's spin axis is tilted only 1.54° to the ecliptic, so crater floors near the poles never see the Sun (Chapter 28). In these **permanently shadowed regions (PSRs)** the Diviner radiometer on NASA's Lunar Reconnaissance Orbiter (LRO) measures temperatures below 40 K, and about 25 K in the coldest places. Water molecules delivered by comets, asteroids, volcanic gases or the solar wind hop across the surface until they land in such a **cold trap**, where they freeze and stay. @fig:icestability shows why: exposed ice at 114 K loses about a metre per billion years by sublimation, but at 150 K it loses kilometres. Carbon dioxide ice needs temperatures below about 60 K.

![Sublimation loss of exposed water and carbon dioxide ice in vacuum, versus temperature. Water ice survives for billions of years only below about 110–115 K, which on the Moon means permanently shadowed crater floors; CO₂ ice survives only in the coldest of them.](figures/out/ch41_icestab.svg){#fig:icestability width=90%}

The evidence accumulated over three decades:

- **Lunar Prospector** (1998) found excess hydrogen at both poles with a neutron spectrometer: hydrogen nuclei slow the neutrons leaking from the surface.
- NASA's Moon Mineralogy Mapper on India's **Chandrayaan-1** (2008–09) detected hydroxyl and water bound in minerals across much of the surface; a 2018 reanalysis found the infrared signature of water ice exposed in some PSRs.
- **LCROSS** (9 October 2009) crashed a spent 2.3 t Centaur upper stage into Cabeus crater and flew through the plume. It measured 5.6 ± 2.9 % water by mass in the ejecta, together with hydrogen sulphide, ammonia, sulphur dioxide, carbon dioxide and methanol — useful, but also contaminants that a water plant must remove.
- **LRO** (since 2009) mapped cold traps and found ultraviolet hints of patchy surface frost. **ShadowCam** on Korea's Danuri orbiter, imaging PSRs by light scattered from nearby sunlit terrain, found in 2026 no widespread surface ice above about 20–30 % by mass, only a few patches 20–50 m across consistent with more than 10 % ice.
- **Chandrayaan-3**'s ChaSTE probe measured 82 °C on a Sun-facing slope at 69° S in 2023, implying that steep pole-facing slopes at high latitudes may keep ice near the surface even outside PSRs.

Cold traps, including countless "micro cold traps" a few metres across, cover about 40 000 km², some 60 % of it in the south. How much ice they hold is uncertain by orders of magnitude. If the top metre of all of them held LCROSS-like 5.6 % ice at a regolith density of 1 500 kg/m³, the total would be about 3 billion tonnes — enough for a propellant industry of a thousand tonnes a year for millions of years. ShadowCam's results suggest that the real deposits are patchy, mostly buried and mixed with regolith, which is why prospecting on the ground matters so much.

### Helium-3: A Realistic Assessment

Helium-3, a light helium isotope carried by the solar wind, is often cited as a reason to mine the Moon, because its fusion with deuterium releases most of its energy as charged particles rather than neutrons. The arithmetic is daunting. Lunar regolith contains on average about 4 parts per billion (ppb) of helium-3, and 10–20 ppb in the richest titanium-bearing mare soils, where ilmenite retains it best. One litre of the gas at standard conditions weighs 0.135 g, so at 10 ppb about 13 t of regolith must be dug and heated to several hundred degrees Celsius to release a litre — 34 t at 4 ppb. Deuterium–helium-3 fusion also needs plasma temperatures several times higher than the deuterium–tritium reaction, which no power plant has yet used to produce net electricity.

The near-term market is **cryogenics**: helium-3 is essential for the dilution refrigerators that cool quantum computers to millikelvin temperatures, and for neutron detectors. It sells for about US\$ 2 500–3 000 per litre — some US\$ 20 million per kilogram — because terrestrial supply, mostly from the decay of tritium, is tiny. The start-up **Interlune** has agreements to supply 3 litres to the US Department of Energy by April 2029 and up to 10 000 litres a year in 2028–37 to the cryostat maker Bluefors. At 10 ppb, 10 000 litres a year would mean processing about 135 000 t of regolith a year, or 15 t every hour without pause. Helium-3 is a credible niche product, not an energy source for Earth.

### Mars

Mars offers two resources almost everywhere: an atmosphere that is 95 % carbon dioxide at a mean surface pressure of about 0.6 kPa, and water. The polar caps hold a few million cubic kilometres of ice, enough to cover the planet about 20 m deep, but they are far from the low latitudes where landing is easiest. Closer to hand, NASA's Phoenix lander scraped into ice a few centimetres below the soil at 68° N in 2008, orbital radar has mapped buried glaciers at mid-latitudes, and fresh craters imaged by the HiRISE camera expose ice within a metre of the surface as far from the poles as about 40° (@fig:marsicecrater). Even ordinary soil in Gale crater releases about 2 % of its mass as water when Curiosity heats it.

![A small, fresh impact crater on Mars that has exposed bright subsurface ice, surrounded by polygon-patterned ground, imaged by the HiRISE camera on Mars Reconnaissance Orbiter. Craters like this are used to map shallow ice near candidate landing sites.](figures/photos/ch41_marsice2.jpg){#fig:marsicecrater width=64%}

### Asteroids

Asteroids are classified by their reflectance spectra. Three classes matter most:

- **C-type** (carbonaceous) asteroids are dark, dominate the outer main belt and match carbonaceous chondrite meteorites. The most primitive, the CI chondrites, contain clays holding water equivalent to about 18 % of their mass, plus 3–4 % carbon and organic compounds — confirmed by samples from Ryugu and Bennu (Chapter 29).
- **S-type** (stony) asteroids dominate the inner belt and are the commonest type among known near-Earth asteroids. They match ordinary chondrites, which in the H group contain 15–19 % metallic iron–nickel. NEAR Shoemaker orbited the 34 km S-type Eros in 2000–01 (@fig:erosmosaic) and confirmed such a composition.
- **M-type** asteroids have spectra and radar echoes suggestive of metal. Iron meteorites, their likely counterparts, are about 90 % iron and 5–10 % nickel, with 10–40 ppm of **platinum-group metals** (platinum, palladium, rhodium, iridium, osmium, ruthenium) — several times the grade of the richest ores on Earth, which hold a few grams per tonne.

The largest M-type, **16 Psyche**, about 220 km across, was long thought to be the bare iron core of a shattered protoplanet; its bulk density of 3 400–4 100 kg/m³ suggests instead perhaps 30–60 % metal by volume, mixed with rock and pore space. NASA's Psyche spacecraft (@fig:psychesc), launched in October 2023 and driven by Hall-effect thrusters, flew past Mars in May 2026 and will arrive in 2029. Headline claims that Psyche is "worth" quintillions of dollars multiply its mass by today's metal prices and are meaningless, because such supply would collapse those prices.

::: figrow
![Mosaic of the northern hemisphere of the S-type asteroid Eros, 34 km long, imaged by NEAR Shoemaker in 2000.](figures/photos/ch41_eros.jpg){#fig:erosmosaic}

![NASA's Psyche spacecraft in a clean room near Kennedy Space Center in June 2023, during final assembly before its launch to the metal-rich asteroid 16 Psyche.](figures/photos/ch41_psyche.jpg){#fig:psychesc}
:::

For mining, the important asteroids are the **near-Earth asteroids (NEAs)**, whose orbits come within 1.3 astronomical units of the Sun. On 19 October 2026 the JPL Small-Body Database listed 42 782, including 875 larger than about 1 km and 11 758 larger than about 140 m; the Vera C. Rubin Observatory and NASA's NEO Surveyor, due for launch in 2027, will multiply the number known (Chapter 26).

@fig:neadelta estimates how easy they are to reach, in the spirit of the classic method of Eugene Shoemaker and Eleanor Helin (1978): a spacecraft leaves a 400 km orbit, follows an ellipse from Earth's orbit to the asteroid's farthest point from the Sun and matches its velocity there, sharing the plane change optimally between the two burns. About 900 known NEAs need less Δv than a trip to low lunar orbit (4.0 km/s), and about 14 600 less than 6 km/s, close to the cost of landing on the Moon. The catch is size: only 7 of the easiest are larger than 140 m, and only about 25 objects larger than 1 km lie below 6 km/s. Accessible NEAs also have Earth-like orbits, so launch and return opportunities recur only every few years or decades, and their weak gravity means that a miner must anchor itself or enclose its target — Bennu's surface behaved like a fluid of loose rubble when OSIRIS-REx touched it.

![Accessibility of the 42 782 known near-Earth asteroids. (a) Distribution of the estimated Δv from low Earth orbit to rendezvous, for all NEAs and for those larger than about 140 m. (b) Number of NEAs below a given Δv, by size. Dashed lines mark the Δv from LEO to low lunar orbit and to the lunar surface.](figures/out/ch41_neadv.svg){#fig:neadelta width=98%}

## Turning Rock and Ice into Products

Three process chains dominate ISRU planning (@fig:isruchains): extracting and splitting water from lunar polar ice; reducing the oxides of ordinary regolith to free oxygen and metals; and, on Mars, splitting atmospheric carbon dioxide and combining it with hydrogen from ice to make methane. @tbl:isruprocesses compares the main processes.

![The three main ISRU process chains: water ice to propellant and life-support consumables at the lunar poles; oxygen and metals from ordinary lunar regolith; and oxygen and methane from the Martian atmosphere and ice.](figures/out/ch41_isruflow.svg){#fig:isruchains width=96%}

| Process | Feedstock | Temperature | Products | Max. O₂ (kg/t) | Status (Oct 2026) |
|---|---|---|---|---|---|
| Ice extraction + electrolysis | Icy polar regolith | −120 to +100 °C | H₂O, H₂, O₂ | Depends on ice | Lab tests; prospecting from 2027 |
| H₂ reduction of ilmenite | Mare soil, volcanic glass | 900–1 050 °C | O₂ (via H₂O), Fe, TiO₂ | 10–35 | Field tests in Hawaii (2008–10) |
| Carbothermal reduction | Any regolith | > 1 600 °C (melt zone) | O₂ (via H₂O), slag | 250–290 | Vacuum demonstration 2023 |
| Molten regolith electrolysis | Any regolith | ≈ 1 600 °C | O₂, Fe, Si, Al | 420–450 | Lab; Blue Alchemist |
| Molten salt (FFC) electrolysis | Any regolith | ≈ 900–950 °C | O₂, metal alloy powder | 400–430 | Lab (ESA, Metalysis) |
| Solid-oxide CO₂ electrolysis | Mars atmosphere | ≈ 800 °C | O₂, CO | — | Flown: MOXIE, 122 g O₂ |
| Sabatier reaction | CO₂ + H₂ | 300–400 °C | CH₄, H₂O | — | Operating on ISS since 2010 |

: Main ISRU processes. Maximum oxygen yields are theoretical, for typical lunar soils. {#tbl:isruprocesses}

### Water from Icy Regolith

The simplest chain digs polar regolith, heats it to drive off the ice as vapour, freezes the vapour on a cold surface, purifies it and splits it. The machines must dig soil at 40–100 K, where ice-cemented regolith may be as hard as weak rock, and work in darkness. Prototypes such as NASA's **RASSOR** and **IPEx** use counter-rotating bucket drums whose digging forces cancel, so a light robot can excavate in one-sixth gravity without being pushed backwards (@fig:ipexphoto). Alternatives heat the ground in place: a heated drill releases vapour from a borehole, or — in one "thermal mining" proposal — mirrors on a crater rim reflect sunlight onto icy ground beneath a dome, and the vapour freezes on cold plates.

The thermal energy has two main terms: warming the regolith that comes with the ice, and the latent heat of sublimation (2.83 MJ/kg). @fig:iceenergy shows that at 30 % ice sublimation dominates and about 3.3 MJ is needed per kilogram of water; at 2 % ice, 49 kg of rock must be warmed per kilogram of water and the total more than doubles. Real plants lose heat and capture only part of the vapour, so the practical figure may be twice the ideal.

![Thermal energy needed to extract water from icy regolith. (a) Energy per kilogram of water versus ice content, for heating to 250 K or 373 K; dashed lines assume only half the heat reaches the feedstock. (b) Breakdown at 250 K for four ice contents: at low concentration, most energy goes into heating rock.](figures/out/ch41_iceenergy.svg){#fig:iceenergy width=98%}

**Electrolysis**, $2\mathrm{H_2O} \rightarrow 2\mathrm{H_2} + \mathrm{O_2}$, needs at least 15.9 MJ per kilogram of liquid water — more than the extraction. It yields hydrogen and oxygen in the mass ratio 1 : 8, while hydrogen–oxygen engines burn them at about 1 : 5.5–6, leaving surplus oxygen for life support. Liquefaction adds more: oxygen liquefies at 90 K, which radiators can reach near the poles, but hydrogen needs 20 K and active refrigeration, and both boil off in storage (Chapter 40).

::: example
**Example: power for a polar water plant**

A plant mines regolith containing 5 % ice by mass and must produce 100 t of water a year. The regolith starts at 40 K and is warmed to 250 K.

1. Regolith processed: 19 kg per kilogram of water, so **1 900 t a year**, or 5.2 t a day.
2. Ideal thermal energy (@fig:iceenergy): warming the regolith 1.61 MJ, warming the ice 0.24 MJ, sublimation 2.83 MJ — **4.7 MJ** per kilogram of water; 9.4 MJ/kg if only half the heat reaches the feedstock.
3. Electrolysis at 70 % efficiency: 15.9 / 0.7 = 22.7 MJ/kg. Total about **32 MJ** (8.9 kWh) per kilogram of water.
4. Annual energy: 100 000 kg × 32 MJ = 3.2 TJ; divided by the 3.16 × 10⁷ s in a year, an average of **about 100 kW**, day and night — the output of the fission reactor NASA plans to have ready for the Moon by about 2030 — before liquefaction and losses.
5. Products: 11.2 t of hydrogen and 88.8 t of oxygen. At a mixture ratio of 6 : 1 the hydrogen supports 78 t of propellant, leaving 22 t of oxygen for breathing or an oxygen-rich engine.
:::

### Oxygen from Ordinary Regolith

Ice exists only at the poles, but oxygen is everywhere. Freeing it from the strong bonds of silicates and oxides takes at least the enthalpy of formation of the oxides — 18 MJ per kilogram of oxygen for ilmenite and about 30 MJ/kg for complete reduction of typical soil — and the soil must be heated to 900–1 600 °C. @fig:o2yield compares four processes.

- **Hydrogen reduction.** Hot hydrogen removes the oxygen bound to iron, $\mathrm{FeTiO_3} + \mathrm{H_2} \rightarrow \mathrm{Fe} + \mathrm{TiO_2} + \mathrm{H_2O}$, at 900–1 050 °C; the water is electrolysed and the hydrogen recycled. Only iron oxide reacts, so the yield is about 1 % of the mass of high-titanium soil and most of the energy heats rock that yields nothing, unless the ilmenite is first concentrated magnetically or electrostatically. NASA field tests on Mauna Kea in Hawaii in 2008 and 2010 ran small hydrogen-reduction and carbothermal plants on volcanic soil.
- **Carbothermal reduction.** Methane passed over molten regolith above about 1 600 °C reduces silicates too, producing carbon monoxide and hydrogen, which are converted back into methane and water; yields reach 25–30 % of the regolith mass. In April 2023 NASA's Carbothermal Reduction Demonstration, a Sierra Space reactor heated by a laser in place of concentrated sunlight, extracted oxygen from lunar simulant in a vacuum chamber for the first time.
- **Molten regolith electrolysis (MRE).** As in aluminium smelting, a current through regolith melted at about 1 600 °C releases oxygen at an inert anode, while iron and silicon collect at the cathode. MRE frees almost all the oxygen and yields metals, but needs anodes that survive hot, corrosive melts. Blue Origin's **Blue Alchemist**, partly funded by a US\$ 34.7 million NASA award, has used MRE to make solar cells from simulant; it passed its critical design review in 2025, with an autonomous vacuum-chamber demonstration planned for 2026.
- **Molten salt (FFC Cambridge) electrolysis.** A regolith pellet forms the cathode in molten calcium chloride at about 950 °C; oxygen ions migrate to the anode, leaving metal alloy powder. Researchers working with ESA and the UK company Metalysis extracted 96 % of the oxygen from a simulant in 2020. The regolith never melts, but graphite anodes release carbon dioxide rather than oxygen, so inert anodes are again the key development.

![Oxygen from lunar regolith. (a) Theoretical oxygen yield per tonne of highland and mare soil for four processes (log scale). (b) Minimum energy per kilogram of oxygen for mare soil: breaking the oxide bonds plus heating the regolith, without heat recovery.](figures/out/ch41_o2yield.svg){#fig:o2yield width=98%}

::: example
**Example: oxygen from ilmenite**

A hydrogen-reduction plant processes high-titanium mare soil containing 10 % ilmenite by mass and reduces 90 % of it at 1 300 K.

1. Ilmenite per tonne: 100 kg, or 100 000 / 151.7 = 659 mol of FeTiO₃, of which 593 mol is reduced.
2. Each mole gives one mole of water and, after electrolysis, half a mole of O₂: 593 × 16.0 g = **9.5 kg of oxygen per tonne** (0.95 %). The 1.2 kg of hydrogen is recycled.
3. Chemical energy: 288 kJ per mole of oxygen atoms, or 171 MJ per tonne — **18 MJ per kilogram of O₂**.
4. Heating a tonne of regolith from 250 K to 1 300 K takes about 1 110 MJ, or 117 MJ per kilogram of O₂ — six times the chemistry. Recovering 75 % of the heat from the spent soil cuts the total from 135 to 47 MJ/kg; concentrating the ilmenite to 50 % first cuts the heating term five times.
5. To make 10 t of oxygen a year the plant must dig and process about **1 050 t of soil**, or 2.9 t a day — why low-yield processes need beneficiation, and why ice is attractive where it exists.
:::

### Oxygen and Methane on Mars

On Mars the feedstock comes to the plant. NASA's **Mars Oxygen In-Situ Resource Utilisation Experiment (MOXIE)**, a 17 kg unit inside Perseverance (@fig:moxieinstall), compressed Martian air from about 0.6 kPa to near 100 kPa and passed it over solid-oxide electrolysis cells at 800 °C, where a current split carbon dioxide: $2\mathrm{CO_2} \rightarrow 2\mathrm{CO} + \mathrm{O_2}$. In 16 runs between April 2021 and August 2023, by day and night and in every season, it made 122 g of oxygen, at up to 12 g an hour and 98 % purity or better.

![Engineers lower MOXIE into the body of the Perseverance rover in 2020. The experiment made the first oxygen produced on another planet.](figures/photos/ch41_moxie.jpg){#fig:moxieinstall width=58%}

The scale-up is large. NASA estimates that a crewed Mars ascent vehicle would need about 25 t of oxygen; made over the 14 months before a crew arrives, that requires 2.4 kg an hour — 200 times MOXIE's best rate — and tens of kilowatts. Methane comes from the **Sabatier reaction**, $\mathrm{CO_2} + 4\mathrm{H_2} \rightarrow \mathrm{CH_4} + 2\mathrm{H_2O}$, over a nickel or ruthenium catalyst at 300–400 °C; on the ISS a Sabatier reactor has made water since 2010 from the crew's exhaled carbon dioxide and hydrogen left over from oxygen generation. The hydrogen would come from Martian ice, or from Earth, as Robert Zubrin and David Baker's 1990 "Mars Direct" plan proposed. A methane–oxygen engine burns about 3.6 kg of oxygen per kilogram of methane, so oxygen from the air alone supplies 78 % of the propellant — one reason SpaceX's Starship burns methane.

### Building with Regolith

By mass, the largest use of lunar material may be the least glamorous. Landing pads stop rocket exhaust from blasting regolith across a base; **berms** — walls of piled soil — shield equipment from ejecta; roads keep rovers out of dust; and a few metres of soil over a habitat protect a crew from cosmic radiation, solar storms and an equatorial day–night temperature swing of nearly 300 K. In June 2025 NASA's RASSOR robot built a berm about 0.9 m high from simulant at Kennedy Space Center (@fig:rassorberm).

::: figrow
![NASA's ISRU Pilot Excavator (IPEx), an excavator and dump truck in one, during a simulated lunar mission in a regolith testbed at Kennedy Space Center in August 2024.](figures/photos/ch41_ipex.jpg){#fig:ipexphoto}

![RASSOR, with counter-rotating bucket drums at each end, building a berm of simulated lunar regolith at Kennedy Space Center in June 2025.](figures/photos/ch41_rassor.jpg){#fig:rassorberm}
:::

**Sintering** fuses grain surfaces with focused sunlight, lasers or microwaves (which couple well to the tiny iron particles in lunar soil); **melting and casting** make glass and basalt-like solids; **binders** such as sulphur, which melts at 115 °C, make "sulphur concrete" without water; and **3D printing** builds walls layer by layer. ICON, which printed NASA's simulated Mars habitat for the CHAPEA missions (Chapter 30), is developing laser vitrification of lunar soil under a US\$ 57.2 million NASA contract running to 2028, and tested the flow of its printing material in lunar gravity on a New Shepard flight in February 2025. China plans to test solar-concentrator brick-making on its Chang'e 8 lander around 2028.

### Power: The Hidden Requirement

Every process is limited by power. The example plant above needs about 100 kW continuously for 100 t of water a year; oxygen from ordinary regolith needs more per kilogram. Ridges near the south pole, such as the rim of Shackleton crater, are sunlit for 80–90 % of the year, but inside the cold traps, and through the 14-day lunar night elsewhere, nuclear power is the practical choice. NASA and the US Department of Energy renewed their Fission Surface Power partnership in January 2026, aiming for a 100 kW reactor ready to launch by about 2030 and to run for at least 10 years; its waste heat could warm regolith while its electricity drives electrolysis.

## Prospecting: Finding the Ore

Miners distinguish a **resource** — material known to exist — from a **reserve**, the part that can be extracted at a profit with proven technology. No space resource is yet a reserve. Orbital data show where hydrogen and cold traps are, but not the form, depth and purity of the ice or how hard the soil is to dig; these can only be measured on the ground (@tbl:prospectmissions).

| Mission | Agency | Year | Method | Result or status (Oct 2026) |
|---|---|---|---|---|
| Lunar Prospector | NASA | 1998–99 | Neutron spectrometer | Hydrogen excess at both poles |
| Chandrayaan-1 | ISRO, NASA | 2008–09 | Infrared spectra, radar | Surface OH/H₂O; ice in some PSRs |
| LCROSS | NASA | 2009 | Impactor and shepherding probe | 5.6 ± 2.9 % water in Cabeus |
| LRO; ShadowCam on Danuri | NASA; KARI | 2009–; 2022– | Thermal, UV, neutron mapping; PSR imaging | Cold-trap maps; no extensive surface ice |
| Lunar Trailblazer | NASA | 2025 | Infrared and thermal mapping | Lost the day after launch |
| PRIME-1 (on IM-2) | NASA | 2025 | 1 m drill, mass spectrometer | Lander tipped over; no drilling |
| VIPER | NASA | late 2027 | Rover, 1 m drill, spectrometers | Revived 2025; on Blue Moon MK1 |
| Chang'e 7 | CNSA | 2027 | Orbiter, lander, rover, hopper | Missed 2026 launch window |
| PROSPECT (on IM-4) | ESA | 2027 | 1 m drill and gas laboratory | In preparation |
| LUPEX (Chandrayaan-5) | ISRO, JAXA | ≈ 2028 | Lander and rover with drill | In development |
| Chang'e 8 | CNSA | ≈ 2028 | ISRU and construction tests | In development |

: Lunar prospecting missions. {#tbl:prospectmissions}

### Bad Luck in 2025

Two missions launched on the same Falcon 9 in February 2025 showed how hard the work is. NASA's US\$ 94 million **Lunar Trailblazer** orbiter carried an infrared volatiles mapper and a thermal mapper built by the University of Oxford to map the form and abundance of polar water (@fig:trailblazerphoto). Contact was lost the day after launch, most likely because misaligned solar arrays let its batteries drain, and NASA ended the mission in July 2025. The primary payload, Intuitive Machines' IM-2 lander *Athena*, carried NASA's **PRIME-1**: the TRIDENT drill, designed to bring up regolith from 1 m depth in 10 cm steps, and the MSolo mass spectrometer to analyse the released gases (@fig:msolophoto). *Athena* landed on 6 March 2025 at 84.8° S, about 500 m from its target on the Mons Mouton plateau, but came to rest on its side in a crater and operated for only about 12 hours instead of 10 days. TRIDENT exercised its mechanisms but never drilled; MSolo made 43 scans, recording gases vented from the lander's own tanks.

::: figrow
![NASA's Lunar Trailblazer in a clean room at Lockheed Martin in 2023, after the Lunar Thermal Mapper (black box, upper right) was installed. The orbiter was lost the day after its launch in February 2025.](figures/photos/ch41_trailblazer.jpg){#fig:trailblazerphoto}

![Parts of the MSolo mass spectrometer, a modified commercial instrument, at Kennedy Space Center in 2020. MSolo flew on the IM-2 lander as part of PRIME-1.](figures/photos/ch41_msolo.jpg){#fig:msolophoto}
:::

### Next Steps on the Ground

NASA's half-tonne **VIPER** rover (Volatiles Investigating Polar Exploration Rover) carries a neutron spectrometer, a near-infrared spectrometer, MSolo and a TRIDENT drill to map ice across several kilometres of polar terrain (Chapter 28). NASA cancelled it in July 2024 over cost growth and delays, then revived it in September 2025 with a task order worth up to US\$ 190 million for Blue Origin to land it near Mons Mouton in late 2027 on the second Blue Moon MK1 lander. That depends on the first MK1 flight, which slipped to early 2027 after a New Glenn booster exploded during a static-fire test in May 2026.

China's **Chang'e 7** — orbiter, lander, rover and a small "hopper" designed to jump into a shadowed crater and analyse its water — missed its August 2026 launch window and is expected in 2027. ESA's **PROSPECT**, the ProSEED drill to about 1 m and the ProSPA gas laboratory originally developed for Russia's Luna 27, will fly on Intuitive Machines' IM-4 lander in 2027. India and Japan's **LUPEX** (Chandrayaan-5), an ISRO lander with a JAXA rover and drill, is planned for launch on an H3 rocket around 2028, and China's **Chang'e 8**, also around 2028, will test resource use and construction for the planned International Lunar Research Station.

The stakes rose in 2026, when NASA paused the Gateway lunar station and announced a plan for a permanent base near the south pole, starting with frequent robotic landings from 2027. Whether that base can live partly off the land depends on what these rovers and drills find.

## The Business of Space Mining

### The First Wave

Asteroid mining became a business proposition in April 2012, when **Planetary Resources** was unveiled in Seattle with backing from Google's Larry Page and Eric Schmidt and the film director James Cameron. It planned to find water-rich near-Earth asteroids with small prospecting telescopes and sell the water as propellant in space. **Deep Space Industries (DSI)** followed in 2013, and Luxembourg, which launched a national space-resources initiative in 2016, invested in Planetary Resources and agreed to co-fund work by DSI. Planetary Resources flew two test satellites, the second of which, Arkyd-6, tested an infrared imager for detecting water in 2018. With no customers for propellant in space and long timelines, investors lost patience: Planetary Resources was bought by the blockchain company ConsenSys in October 2018, and DSI by Bradford Space, which kept its water-propelled thruster, in January 2019.

### The Second Wave

A new generation of companies started with smaller, cheaper missions (@tbl:miningcompanies).

- **AstroForge** (founded 2022) aims to mine platinum-group metals from metallic NEAs. Its Brokkr-1 satellite, launched in April 2023 to test refining asteroid-like material in orbit, could not be commanded reliably and did not complete the test. Odin, a 100 kg spacecraft built for about US\$ 3.5 million to fly past the small asteroid 2022 OB5, which the company believes may be metallic, rode with IM-2 in February 2025; contact was never properly established and it was declared lost in March. DeepSpace-2, designed to land on 2022 OB5, was completed in June 2026 and is to ride on IM-3 in 2027.
- **Karman+** (Denver) raised US\$ 20 million in 2025 for a demonstration to rendezvous with an NEA and extract about 1 kg of material around 2027; it aims to sell water and regolith to satellite-servicing tugs in high orbits.
- **TransAstra** proposes "optical mining", using concentrated sunlight to drive volatiles out of an asteroid enclosed in a bag, and tested a small capture bag on the ISS in 2025.
- **Interlune** plans to harvest helium-3 from lunar regolith, with the purchase agreements described above.

| Company | Founded | Target | Missions flown | Outcome or status (Oct 2026) |
|---|---|---|---|---|
| Planetary Resources | 2012 (public) | Water from NEAs | Arkyd-3R (2015), Arkyd-6 (2018) | Acquired by ConsenSys, 2018 |
| Deep Space Industries | 2013 | Water from NEAs | None of its own | Acquired by Bradford Space, 2019 |
| AstroForge | 2022 | Platinum-group metals | Brokkr-1 (2023), Odin (2025) | Both failed; DeepSpace-2 due 2027 |
| Karman+ | early 2020s | Water, regolith for use in space | None yet | Demonstration targeted 2027 |
| TransAstra | 2015 | Volatiles by optical mining | Capture-bag test on ISS (2025) | Development |
| Interlune | 2020 | Lunar helium-3 | None yet | Contracts for delivery from 2028–29 |

: Space-mining companies. {#tbl:miningcompanies}

### Who Would Buy?

A space resource can be sold in two very different markets. **In space**, the competitor is material launched from Earth, and the gear ratio sets the price: propellant in lunar orbit is worth what it costs to deliver from Earth, thousands of dollars per kilogram. That market barely exists yet; it depends on government programmes such as Artemis and on reusable vehicles that need refuelling. **On Earth**, the competitor is terrestrial mining, and the product must be valuable enough per kilogram to pay for its return.

Platinum is the usual example. World mine supply in 2025 was about 170 t, and the price is volatile: in 2026 it reached a record of about US\$ 2 900 per troy ounce in January, fell to about US\$ 1 540 in July and stood near US\$ 1 700 (US\$ 55 000 per kilogram) in October. The more an asteroid miner sells, the further the price falls. @fig:ptprice uses a simple constant-elasticity demand model, in which a 1 % increase in supply lowers the price by 1/ε %, where ε is the **price elasticity of demand**. If demand is inelastic (ε = 0.3), the miner's revenue peaks at only about US\$ 1.2 billion a year, at 73 t a year; at ε = 0.6 the peak is US\$ 3.0 billion at 255 t a year. A single 100 m metallic asteroid with 20 ppm of platinum-group metals would hold about 50 t of them — enough, if it were all platinum and sold in one year, to cut the price by between a quarter and more than a half. Space mining for Earth markets caps its own revenue while costing billions of dollars to develop.

![Why space metals cannot simply be valued at today's prices. (a) Platinum price as supply from space mining is added to world mine output, for three values of the price elasticity of demand. (b) The miner's annual revenue, which reaches a maximum and then falls when demand is inelastic.](figures/out/ch41_economics.svg){#fig:ptprice width=96%}

The most plausible early business is therefore not precious metals but services to government exploration: prospecting data, payload delivery, demonstration contracts and, eventually, propellant and water sold in lunar orbit.

## Law and Policy

### Treaties

The **Outer Space Treaty** of 1967, ratified by more than 110 states including every major spacefaring nation, is the foundation of space law (Chapters 1 and 19). Article I guarantees the freedom of all states to explore and use outer space; Article II declares that outer space, "including the Moon and other celestial bodies, is not subject to national appropriation by claim of sovereignty, by means of use or occupation, or by any other means". Article VI makes states responsible for authorising and supervising their companies, and Article IX requires "due regard" for the interests of others. The treaty is silent on whether materials taken from a celestial body can be owned — though nobody objected when Apollo and Luna brought samples home.

The 1979 **Moon Agreement** declared the Moon and its natural resources "the common heritage of mankind" and called for an international regime to govern their exploitation once it became feasible. It entered into force in 1984 but was never joined by the United States, Russia or China; since Saudi Arabia's withdrawal took effect in January 2024 it has 17 parties, several of which — including Australia, Belgium, Mexico and the Netherlands — have also signed the Artemis Accords.

### National Laws and the Artemis Accords

Since 2015 several states have passed laws allowing their companies to own the resources they extract while disclaiming sovereignty over the body itself — the difference, supporters argue, between owning the fish and owning the sea (@tbl:spacereslaw). The United States led with the **Commercial Space Launch Competitiveness Act** of November 2015, followed by **Luxembourg** (2017), the **United Arab Emirates** (a 2019 space law and 2023 space-resources regulations) and **Japan** (2021). Under Japan's law the government licensed ispace in 2022 and again in 2024 to transfer ownership of lunar regolith to NASA — the first licences issued under the law.

That transfer was part of a symbolic programme: in December 2020 NASA agreed to buy small samples of regolith, collected and photographed on the Moon and left in place, from Lunar Outpost for US\$ 1, ispace Japan and ispace Europe for US\$ 5 000 each and Masten Space Systems for US\$ 15 000. By October 2026 no sale had been completed: ispace's landers crashed in April 2023 and June 2025, Masten went bankrupt in 2022, and Lunar Outpost's rover was aboard the toppled IM-2 lander.

The **Artemis Accords**, launched by NASA and the US State Department in October 2020 with eight founding signatories, had 76 signatories by late September 2026. Section 10 affirms that "the extraction of space resources does not inherently constitute national appropriation under Article II", and Section 11 introduces **safety zones** around operations to avoid harmful interference. China and Russia, which lead the rival International Lunar Research Station, have not signed and criticise the Accords as rule-making outside the United Nations.

| Instrument | Year | Parties or scope | Position on resources |
|---|---|---|---|
| Outer Space Treaty | 1967 | > 110 states | No national appropriation (Art. II); silent on extracted resources |
| Moon Agreement | 1979 | 17 states | "Common heritage of mankind"; future international regime |
| US Commercial Space Launch Competitiveness Act | 2015 | United States | US citizens may own and sell resources they recover |
| Luxembourg space-resources law | 2017 | Luxembourg | "Space resources are capable of being appropriated" |
| UAE space law and regulations | 2019, 2023 | United Arab Emirates | Licensing of resource activities |
| Japan Space Resources Act | 2021 | Japan | Licensed operators own what they extract |
| Artemis Accords | 2020– | 76 signatories (Sept 2026) | Extraction is not in itself appropriation; safety zones |
| COPUOS working group principles | 2021– | UN Legal Subcommittee | Non-binding principles in draft (2026) |

: Law and policy on space resources. {#tbl:spacereslaw}

### The United Nations Working Group

National laws cannot by themselves settle an international question. In 2021 the Legal Subcommittee of the UN **Committee on the Peaceful Uses of Outer Space (COPUOS)** set up a Working Group on Legal Aspects of Space Resource Activities, chaired by the Australian law professor Steven Freeland. In September 2026 it circulated a consolidated draft of non-binding "Initial Recommended Principles", which would recognise that extraction in accordance with the Outer Space Treaty is not by itself national appropriation and encourage voluntary sharing of benefits; consultations continue ahead of the Legal Subcommittee's April 2027 session. The open questions are practical: how large a safety zone may be and for how long, who may work in the few square kilometres of the best polar cold traps, and how to protect sites of scientific value — pristine ice that records the history of water in the inner Solar System — from contamination by mining.

::: ai
**AI for prospecting and mining**

Finding resources is pattern recognition in large datasets. Machine-learning classifiers map minerals and hydration from orbital spectra — M³, Diviner and Chandrayaan-2's radar and imaging spectrometer — and fuse them with temperature and topography to rank candidate ice sites; a deep-learning denoiser built around the physics of LRO's camera has turned noisy images of permanently shadowed craters into usable maps of boulders and craters for planning rover routes. For asteroids, networks classify the spectra of tens of thousands of objects observed by Gaia and will help sift the millions of detections expected from the Rubin Observatory. On the surface, communication delays and darkness demand autonomy: perception that works under headlights, digging controllers that adapt to unknown soil strength, coordination of fleets of excavators, haulers and processing plants, and fault detection in plants that must run unattended for years (Chapters 46, 48 and 51).
:::

::: key
**Key takeaways**

- The gear ratio drives ISRU: with typical assumptions a kilogram on the lunar surface costs about 130 kg at Earth lift-off and a kilogram in low lunar orbit about 73 kg, while lunar propellant delivered to low lunar orbit costs only about 2.1 kg of lunar production.
- A lunar plant pays only if it makes several times its own landed mass — about 3.8 times for delivery to low lunar orbit — before it fails; dust, cold and power make that uncertain.
- Oxygen is everywhere (41–45 % of lunar regolith; a 95 % CO₂ atmosphere on Mars); water ice is concentrated in polar cold traps below about 110 K, but its amount and distribution are uncertain, and 2026 images show no extensive thick surface ice.
- Water extraction needs about 3–7 MJ of heat per kilogram at 2–30 % ice, plus at least 15.9 MJ/kg for electrolysis; oxygen from ordinary regolith needs 18–30 MJ/kg for the chemistry alone, plus heat — power, probably nuclear, is the limiting resource.
- MOXIE made 122 g of oxygen on Mars in 2021–23; a crewed ascent needs a rate about 200 times higher. Ground prospecting suffered losses in 2025 (Lunar Trailblazer, PRIME-1); VIPER, Chang'e 7 and PROSPECT are due in 2027.
- Asteroid mining for Earth markets is limited by economics, because added supply collapses prices. The first wave of companies failed; the second (AstroForge, Karman+, Interlune) runs cheaper missions but has not yet succeeded in space.
- The Outer Space Treaty bans national appropriation but is silent on extracted resources; national laws (US 2015, Luxembourg 2017, UAE, Japan 2021) and the 76-signatory Artemis Accords allow ownership, while a UN working group drafts non-binding principles.
:::

::: questions
**Review questions**

1. Explain the "gear ratio" of a destination. Using the rocket equation with $I_{sp}$ = 450 s, show why a kilogram in low lunar orbit costs about 2.9 kg in low Earth orbit.
2. Why does lunar propellant delivered to low Earth orbit cost more lunar propellant per kilogram than delivery to low lunar orbit, even with aerobraking? How would a depot at L1 change this?
3. A lunar oxygen plant of 15 t (including power) makes 20 t of propellant a year. How many years must it run to pass the break-even productivity of 3.8 for delivery to low lunar orbit?
4. Using @fig:icestability, explain why water ice survives in permanently shadowed craters but not on sunlit polar terrain. What other volatiles did LCROSS detect, and why do they matter for a water plant?
5. Estimate the energy to extract 1 kg of water from regolith containing 2 % ice, and compare it with the energy to electrolyse the water.
6. Compare hydrogen reduction of ilmenite with molten regolith electrolysis in yield, temperature, by-products and main engineering challenge.
7. MOXIE produced up to 12 g of oxygen an hour. How long would one MOXIE take to make the 25 t needed for a crewed ascent, and how many would be needed to make it in 14 months?
8. How much lunar regolith must be processed to obtain 1 litre of helium-3 at 4 ppb? Why is helium-3 more likely to be sold for cryogenics than for fusion power?
9. Using the model of @fig:ptprice, explain why the revenue from selling asteroid platinum on Earth reaches a maximum. Why might water sold in lunar orbit be a better business?
10. Summarise how the Outer Space Treaty, the Moon Agreement, the US 2015 Act and the Artemis Accords treat the ownership of extracted resources, and name two questions the UN working group has still to resolve.
:::
