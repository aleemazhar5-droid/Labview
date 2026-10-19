---
title: Human Spaceflight Fundamentals and Life Support
hero: ch30
abstract: A human being is the most demanding payload a spacecraft can carry. Every day each crew member consumes almost a kilogram of oxygen and several kilograms of water and food, and produces carbon dioxide, heat and waste that must be removed. Weightlessness weakens bones, muscles, the heart and even the eyes, while cosmic radiation slowly raises the risk of cancer. This chapter explains how the body adapts to spaceflight and how crews are protected: the radiation environment and dose limits, the design of cabin atmospheres, the metabolic budget, and the environmental control and life support systems (ECLSS) that recycle air and water on the International Space Station. It closes with food, medicine, psychology, the history of fatal accidents and the safety standards that govern crewed vehicles in 2026.
---

On 12 April 1961, Yuri Gagarin completed one orbit of the Earth in Vostok 1 and landed 108 minutes after launch. By mid-2026 about 780 people from 55 countries had flown above 100 km — a crew small enough to fit into a single airliner, but one that has lived continuously in orbit since November 2000. People are sent into space because they bring what machines still lack: judgement in unforeseen situations, dexterity for repairs and assembly, and a field scientist's eye — five Shuttle crews serviced and upgraded the Hubble Space Telescope, and Apollo astronauts chose the most telling rocks on the Moon.

The price is steep. A crewed spacecraft must provide a pressurised, breathable, temperature-controlled bubble; remove carbon dioxide, heat, moisture and waste; supply water and food; protect against radiation and fire; keep the crew healthy; and bring them home — with far higher reliability than an uncrewed spacecraft. This chapter covers the biology and the life support engineering; the vehicles themselves are described in Chapter 31, space stations and habitats in Chapter 32, and spacesuits in Chapter 33.

## Humans in Space: How Long and How Far

Human spaceflight has progressed in steps of duration (@fig:spacerecords). Gemini 7 showed in 1965 that people could survive the two weeks needed for a lunar mission, and Skylab and the Soviet Salyut and Mir stations pushed single flights from one month to over a year. The record of **437.7 days**, set by the Russian physician Valeri Polyakov on Mir in 1994–95, still stands in 2026. The longest flights on the International Space Station (ISS) are those of Oleg Kononenko and Nikolai Chub (374 days, 2023–24) and of Sergey Prokopyev, Dmitri Petelin and Frank Rubio (371 days, 2022–23, the US record, extended when their Soyuz MS-22 sprang a coolant leak). In June 2024 Kononenko became the first person to spend 1 000 days in space, finishing his fifth flight with 1 111 days in total; Peggy Whitson holds the US and women's cumulative record of 695 days.

![Single-flight duration record from Vostok 1 to Polyakov's 437.7 days on Mir, with the other flights that have lasted longer than 300 days. A crewed Mars mission of the conjunction class would last about twice as long as the record.](figures/out/ch30_records.svg){#fig:spacerecords width=94%}

A round trip to Mars would last 500–1 000 days with no resupply and no quick return, and everything in this chapter — from bone loss to recycling — becomes harder as missions grow longer and further from Earth.

## The Human Body in Weightlessness

In orbit the crew falls freely with the spacecraft, so nothing presses the body against a floor (Chapter 2). Tissues tuned to 1 g respond within minutes to months (@fig:bodyadapt). Most changes are adaptations rather than illnesses, but they become problems on return to gravity — on Earth, the Moon or Mars.

![How the body changes in weightlessness. (a) A simple model of bone loss in the hip during 6- and 12-month flights and of recovery after landing. (b) Typical onset and duration of the main changes.](figures/out/ch30_body.svg){#fig:bodyadapt width=98%}

### Fluids, Heart and Eyes

On Earth, gravity pulls blood and tissue fluid towards the legs. In weightlessness about two litres shift towards the chest and head within hours: faces become puffy, legs thin and noses feel blocked. The body treats the extra fluid in the chest as an overload and excretes it, so blood plasma volume falls by roughly 10–20 % within days, and the reflexes that control blood pressure weaken. After landing many astronauts suffer **orthostatic intolerance** — dizziness or fainting when standing up — so crews drink salt water before entry, wear compression garments and are often helped out of the capsule.

A more puzzling effect, first described in 2011, concerns the eyes. **Spaceflight-associated neuro-ocular syndrome (SANS)** comprises swelling of the optic disc where the nerve enters the eye, folds in the choroid layer behind the retina, flattening of the back of the eyeball and a shift towards long-sightedness. Imaging studies suggest that most long-duration crew members show some of these signs; in one prospective ISS study about two-thirds had optic-disc swelling by the 150th day of flight. The likely cause is the headward fluid shift, which keeps pressure in the veins of the head slightly raised all the time. Crews monitor their eyes with optical coherence tomography and ultrasound (@fig:sansexam), and lower-body negative-pressure devices that draw fluid back towards the legs are being tested. Some changes persist for years, making SANS a leading health concern for Mars missions.

### Balance and Motion Sickness

The inner ear's otolith organs sense linear acceleration and the direction of gravity. In free fall they send signals that conflict with what the eyes see, and more than half of all space travellers suffer **space motion sickness** — nausea, vomiting, headache and lethargy — during the first two or three days. Spacewalks are not scheduled during this period, because vomiting inside a helmet could be fatal. The brain relearns to rely on vision and touch, but must readapt on return: astronauts walk unsteadily for days after landing — a serious matter for a crew stepping onto Mars after months in transit. Astronauts also grow up to about 3 % taller as the discs between the vertebrae expand, which often causes back pain.

### Bone and Muscle

Bone is constantly rebuilt in response to the loads placed on it. Without body weight, the hip and lumbar spine lose mineral at **1–1.5 % per month** — about as much in one month as an elderly person loses in a year. The calcium released raises the risk of kidney stones. After landing, bone is rebuilt only slowly: a study of 45 crew members on 4–6-month flights found that it took about nine months to recover half of the loss, and that recovery was largely complete only after about three years. @fig:bodyadapt (a) shows what this implies for a one-year mission without effective exercise: a loss of 12–18 % in the hip, with years needed to recover.

Muscles that keep us upright — the calves, thighs and back — waste fastest. Even with exercise, ISS crews in a 2009 study lost about 13 % of calf muscle volume and almost a third of calf muscle power over six months. The main countermeasure is exercise, about two hours every day, on three machines:

- the **Advanced Resistive Exercise Device (ARED)**, which uses vacuum cylinders to provide up to about 2.7 kN (600 lbf) of resistance for squats, dead-lifts and heel raises (@fig:aredphoto);
- the **T2 treadmill**, on which the astronaut is held down by a harness and bungee cords;
- a **cycle ergometer** for aerobic exercise (CEVIS, replaced around 2023 by the smaller FERGO).

Since ARED arrived in late 2008, crews who also eat enough and take vitamin D have lost markedly less bone than earlier crews, and drugs that slow bone breakdown (bisphosphonates) have been tested in flight. Exercise has an engineering cost: more oxygen, heat and humidity, vibration that must be isolated from the structure, and equipment that a small Mars transit vehicle can barely accommodate.

::: figrow
![NASA astronaut Nick Hague exercising on the Advanced Resistive Exercise Device in the ISS Tranquility module, October 2024.](figures/photos/ch30_ared.jpg){#fig:aredphoto}

![NASA astronaut Jonny Kim, assisted by JAXA astronaut Takuya Onishi, performing an eye ultrasound scan on the ISS in May 2025 to look for signs of SANS.](figures/photos/ch30_eyeus.jpg){#fig:sansexam}
:::

### Immune System, Sleep and the Twins Study

Spaceflight also disturbs the immune system: dormant herpes viruses reactivate and are shed in the saliva of many crew members, and skin rashes are common. Sleep is short — about six hours a night on average for Shuttle and ISS crews, despite 8.5 hours being scheduled — disturbed by noise, a sunrise every 92 minutes and workload.

The most detailed picture of these changes came from NASA's **Twins Study** (2015–16). Scott Kelly spent 340 days on the ISS while his identical twin Mark, also an astronaut, stayed on Earth as a genetic control (@fig:twinsshot). In flight, Scott's telomeres — the protective ends of the chromosomes — unexpectedly lengthened, then shortened rapidly after his return; thousands of genes changed their activity, most returning to normal within six months; and his cognitive test performance dropped after landing. A 2024 package of 44 papers on the three-day private Inspiration4 flight found similar molecular changes even on a short mission, most of which faded within months. Spaceflight is a whole-body stress that people tolerate well for months, but whose long-term effects are still being measured.

@tbl:microgeffects summarises the main effects and their countermeasures.

| Body system | Effect in weightlessness | Typical size | Countermeasures |
|------------|----------------------|------------------|----------------------|
| Fluids, heart | Headward fluid shift; fainting on return | ≈ 2 L shifted; plasma −10⁠–⁠20 % | Fluid loading before entry, compression garments |
| Balance | Motion sickness; unsteady after landing | Over half of crew, first 2–3 days | Medication, post-flight rehabilitation |
| Bone | Loss from hip and spine; kidney stones | 1–1.5 % per month | ARED exercise, diet, vitamin D, drugs |
| Muscle | Atrophy of postural muscles | Calf power ≈ −30 % in 6 months | Treadmill, ARED, ergometer, ≈ 2 h/day |
| Eyes (SANS) | Optic-disc swelling, choroidal folds | Signs in most long-duration crew | Monitoring; negative-pressure devices studied |
| Immune, sleep | Virus reactivation; ≈ 6 h of sleep | Many crew members | Lighting schedules, sleep stations |

: Main effects of weightlessness on the human body and their countermeasures. {#tbl:microgeffects}

![Scott Kelly giving himself a flu vaccination aboard the ISS in September 2015, part of the Twins Study investigation of how the immune system responds in flight.](figures/photos/ch30_twins.jpg){#fig:twinsshot width=50%}

## Radiation: The Long-Term Hazard

Radiation is the one hazard that grows steadily with every day outside the Earth's protection. Chapter 2 describes the sources and Chapter 22 the solar storms; for a crew they mean three things:

- **Galactic cosmic rays (GCRs)**: atomic nuclei at close to the speed of light, arriving continuously and almost impossible to stop. The rare heavy nuclei such as iron (**HZE** particles, for high charge Z and energy E) leave dense tracks of damage through cells.
- **Solar particle events (SPEs)**: rare bursts of protons that are easier to shield, but can deliver a dangerous dose within hours to an unprotected crew.
- **Trapped particles** in the Van Allen belts, which dominate the dose in low Earth orbit and during transits of the belts.

### Dose, Risk and Limits

The energy deposited per kilogram of tissue is the **absorbed dose**, in grays (1 Gy = 1 J/kg). Weighting it for the greater damage done by heavy ions and for the sensitivity of each organ gives the **effective dose**, in sieverts (Sv). Doses above about 1 Gy within hours cause acute radiation sickness; at the lower doses of spaceflight the concern is an increased lifetime risk of cancer, and possible damage to the heart and central nervous system.

@tbl:raddoserates lists measured dose rates. A six-month ISS mission gives about 70–160 mSv, depending on the solar cycle; Scott Kelly received 146 mSv in 340 days. Outside the magnetosphere the rate jumps: the Radiation Assessment Detector on the Curiosity rover measured 1.84 mSv per day during its cruise to Mars in 2011–12 and 0.64 mSv per day on the surface, where the planet blocks half the sky. On the Moon, China's Chang'e 4 lander measured about 1.4 mSv per day.

In 2022 NASA adopted a single **career limit of 600 mSv** effective dose for all astronauts, regardless of age or sex. It corresponds to a calculated mean 3 % risk of dying from radiation-induced cancer for the most sensitive group (a 35-year-old woman), and replaced earlier limits that allowed older men a higher dose than young women. For comparison, international recommendations limit radiation workers on Earth to an average of 20 mSv per year. NASA also requires that shielding keep the dose from a large SPE — modelled on the October 1989 event — below 250 mSv. @fig:crewdose compares mission doses with the limit: low-Earth-orbit and lunar missions fit comfortably, but a Mars mission does not.

| Environment | Dose rate | Notes |
|---|---|---|
| Earth's surface | ≈ 0.007 mSv/day | 2.4 mSv per year world average |
| ISS (400 km, 51.6°) | 0.4–0.9 mSv/day | Mostly trapped protons and GCRs |
| Lunar surface | ≈ 1.4 mSv/day | Chang'e 4, 2019 (solar minimum) |
| Interplanetary cruise | ≈ 1.8 mSv/day | Curiosity RAD, 2011–12 |
| Mars surface | ≈ 0.64 mSv/day | Curiosity RAD, 2012–13 |
| Large SPE in deep space | Up to hundreds of mSv in a day | Depends strongly on shielding |

: Measured radiation dose rates for crews. {#tbl:raddoserates}

![Radiation doses for crews. (a) Estimated effective doses for different missions compared with NASA's 600 mSv career limit. (b) Dose accumulated during conjunction-class and opposition-class Mars missions: the limit is reached during the surface stay.](figures/out/ch30_dose.svg){#fig:crewdose width=98%}

### Shielding and Storm Shelters

Shielding is specified by its **areal density** — mass per unit area, in g/cm² — because what matters is how much material a particle must cross. A spacecraft wall provides only a few g/cm²; racks, water and stowage inside add more. For SPE protons, shielding works well: the lower-energy protons stop, and NASA estimates that typical aluminium or polyethylene shielding halves the average SPE dose. For GCRs it barely helps — only about 7 % — because the most energetic nuclei pass through any practical thickness and break up into showers of **secondary** particles, including neutrons, that add their own dose. Hydrogen-rich materials such as polyethylene and water work better than aluminium because they fragment incoming ions without producing many secondaries.

The practical strategy is to accept the GCR dose, limit mission duration, and provide a **storm shelter** for SPEs: a small volume, surrounded by water, food and stowage, where the crew retreats for the hours to days of an event. Warnings come from the space-weather forecasters described in Chapter 22. During Artemis I in 2022 two female-torso phantoms, Helga and Zohar, flew in Orion's passenger seats carrying thousands of dosimeters (@fig:phantoms). Dose rates differed by a factor of four between the least and most shielded positions, turning the spacecraft through 90° halved the dose rate in the inner belt, and a well-placed shelter could keep the dose from a very large SPE below about 150 mSv. On Artemis II in April 2026 a planned in-flight shelter demonstration was shortened to prepare for entry: building the shelter from stowage, already practised on the ground, was skipped, and only the ventilation of an astronaut sheltering in a locker was tested.

![The radiation phantoms Helga (below) and Zohar (above) installed in Orion's passenger seats before Artemis I in August 2022. Zohar wears the AstroRad radiation-protection vest.](figures/photos/ch30_phantoms.jpg){#fig:phantoms width=60%}

::: example
**Example: radiation dose for a Mars mission**

A conjunction-class mission spends 180 days travelling to Mars, 500 days on the surface and 180 days returning. Use the Curiosity RAD dose rates: 1.84 mSv/day in cruise and 0.64 mSv/day on the surface. Ignore SPEs, which the storm shelter is designed to handle.

1. Cruise dose: 360 days × 1.84 mSv/day = **662 mSv** — already above the 600 mSv career limit.
2. Surface dose: 500 days × 0.64 mSv/day = **320 mSv**.
3. Total: 982 mSv, **164 %** of the limit. Following the dose day by day (@fig:crewdose b), the limit is reached on mission day 600, after 420 of the 500 days on the surface.
4. An opposition-class mission (220 days out, 30 days on Mars, 220 days back) gives 1.84 × 440 + 0.64 × 30 = **829 mSv** — shorter, but still over the limit because more time is spent in deep space.
5. To stay within 600 mSv with a 500-day surface stay, the total transit time would have to be below (600 − 320)/1.84 = **152 days** — 76 days each way, beyond chemical propulsion. Thicker shielding hardly helps against GCRs; the options are faster propulsion (Chapter 42), flying near solar maximum when GCRs are weaker, or a deliberate decision to accept a higher risk.
:::

## Designing the Cabin Atmosphere

Engineers choose the cabin's total pressure and oxygen fraction, balancing four hazards: **hypoxia** (too little oxygen), **oxygen toxicity** (too much), **fire**, and **decompression sickness** when moving to a spacesuit at lower pressure. Lower pressure also reduces hull loads and leakage.

### Oxygen and Hypoxia

What the lungs care about is the partial pressure of oxygen in the air reaching them. Air entering the lungs is saturated with water vapour at body temperature, which takes up 47 mmHg (6.3 kPa) regardless of altitude, so the **inspired oxygen partial pressure** is

$$ P_{IO_2} = (P_{total} - 6.3\ \text{kPa}) \times F_{O_2} $$

where $F_{O_2}$ is the oxygen fraction. At sea level this gives 149 mmHg (19.9 kPa). NASA's standard for crewed spacecraft (NASA-STD-3001, Volume 2) treats 145–155 mmHg as normal, limits mild hypoxia to no lower than 127 mmHg, and sets 356 mmHg as the highest value tolerable indefinitely, since breathing very high oxygen pressures damages the lungs and, at extreme levels, causes seizures. On the summit of Everest the inspired value is only 43 mmHg. @fig:cabinatmos maps these limits onto the two design variables and shows the choices made for real spacecraft.

![The cabin atmosphere design space. Curves of constant inspired oxygen pressure show the hypoxic, normal and hyperoxic regions; the dashed line marks the 30 % oxygen level at which spacecraft materials are commonly tested for flammability.](figures/out/ch30_atmos.svg){#fig:cabinatmos width=94%}

### Fire

Materials burn faster as the oxygen fraction rises, and in weightlessness, with no buoyant convection, flames become spherical and slow but can persist where on Earth they would go out. The danger was established tragically on 27 January 1967, when a fire swept through the Apollo 1 command module during a ground test, killing Gus Grissom, Ed White and Roger Chaffee. The cabin held pure oxygen at about 115 kPa and contained flammable nylon netting and Velcro; a spark from wiring started a fire that spread in seconds, and the inward-opening hatch could not be opened against the cabin pressure. NASA changed the launch atmosphere to 60 % oxygen and 40 % nitrogen (vented to pure oxygen at 34.5 kPa during ascent), replaced flammable materials, and fitted a quick-opening hatch.

Today, materials for US crewed vehicles must pass an upward flame-spread test, commonly run at 30 % oxygen and 70.3 kPa, the worst case expected in flight. NASA's Saffire experiments (2016–24) burned large samples inside departing Cygnus cargo ships, providing the first data on how big fires grow in weightlessness.

### Decompression Sickness

Nitrogen dissolved in body tissues forms bubbles if the surrounding pressure falls quickly — **decompression sickness (DCS)**, the divers' "bends". Spacesuits work at low pressure to stay flexible: the US suit at 29.6 kPa of pure oxygen, the Russian Orlan at about 40 kPa (Chapter 33). A crew member moving from a sea-level cabin, with 80 kPa of nitrogen in the tissues, into a suit at 29.6 kPa would have a ratio of tissue nitrogen pressure to suit pressure of 2.7 — far too high. Astronauts therefore **prebreathe** pure oxygen for hours before a spacewalk, sometimes with exercise or a night at reduced pressure (the "campout").

A lower-pressure cabin with more oxygen shortens prebreathe dramatically. NASA's **exploration atmosphere** — 56.5 kPa (8.2 psi) with 34 % oxygen — leaves about 37 kPa of nitrogen in the tissues, a ratio of only 1.26 to the suit, so about 15 minutes of in-suit prebreathe would suffice for frequent surface spacewalks. Its inspired oxygen pressure, 128 mmHg, is like living at about 1 200 m altitude. The penalty is fire: a 2026 NASA assessment found that most spacecraft subsystems would need material changes at 34 % oxygen, and far fewer at 70.3 kPa (10.2 psi). As of 2026 the atmosphere for lunar landers and surface habitats is still being evaluated. @tbl:cabinatmospheres compares the choices.

| Vehicle or regime | Total pressure | O₂ fraction | O₂ partial pressure | N₂ ratio to 29.6 kPa suit |
|---|---|---|---|---|
| Mercury, Gemini, Apollo (in flight) | 34–38 kPa | 100 % | 34–38 kPa | ≈ 0 |
| Skylab (1973–74) | 34.5 kPa | ≈ 72 % | 24.8 kPa | 0.33 |
| ISS, Soyuz, Shuttle, Crew Dragon, Orion | 101.3 kPa | 21 % | 21.3 kPa | 2.70 |
| Shuttle pre-EVA; ISS campout | 70.3 kPa | 26.5 % | 18.6 kPa | 1.75 |
| Exploration atmosphere (studied) | 56.5 kPa | 34 % | 19.2 kPa | 1.26 |

: Cabin atmospheres of crewed spacecraft. The last column is the tissue nitrogen pressure after long exposure divided by the suit pressure; higher values need longer oxygen prebreathe. {#tbl:cabinatmospheres}

Early US spacecraft used pure oxygen at about 35 kPa to save mass: thinner walls, simpler life support, no nitrogen tanks. Soviet spacecraft used sea-level air, a choice the ISS inherited at the cost of long prebreathe.

## The Human Metabolic Budget

A crew member burns food with oxygen. NASA's *Baseline Values and Assumptions Document* (BVAD) defines a reference astronaut of 82 kg who exercises for 90 minutes a day (@tbl:metabolicbudget). The ratio of carbon dioxide produced to oxygen consumed — the **respiratory quotient** — is about 0.86, so more carbon dioxide is exhaled, by mass, than oxygen inhaled. The body also makes about half a kilogram of water a day from food and loses about three kilograms as vapour that the cabin air system must condense.

Two lessons stand out from @fig:metabolicbal. Water dominates — about 4.5 kg of it passes through a person every day, four-fifths of the total — which is why water recycling pays off fastest. And although oxygen is a small mass, it must be supplied, and carbon dioxide removed, continuously: a few hours of failure can be dangerous.

![Daily mass balance of one crew member. Inputs and outputs balance at 5.67 kg per day; most of the mass flowing through a person is water.](figures/out/ch30_massbal.svg){#fig:metabolicbal width=96%}

| Item | kg per crew member per day | Notes |
|---|---|---|
| Oxygen consumed | 0.90 | Older design value 0.84 |
| Carbon dioxide produced | 1.09 | Older design value 1.00 |
| Food solids (dry) | 0.80 | 12.8 MJ of energy |
| Food as supplied on ISS | 2.39 | Including water and 0.43 kg packaging |
| Drinking and food-preparation water | 3.22 | Plus 0.76 kg water in food |
| Breath and sweat water | 2.95 | Removed as humidity condensate |
| Urine | 1.48 | 1.42 kg water |
| Faeces | 0.13 | 0.10 kg water |
| Metabolic heat | 12.4 MJ | 144 W average; half as latent heat |

: The metabolic budget of one crew member (NASA BVAD, 2022). {#tbl:metabolicbudget}

### Carbon Dioxide

Carbon dioxide is toxic well before it displaces oxygen. Concentrations of a few per cent cause headaches, rapid breathing and impaired thinking, and above about 5–10 % they become incapacitating. ISS crews reported headaches at partial pressures of about 3–5 mmHg, and analysis showed that the odds of a headache doubled with every 1 mmHg increase; NASA-STD-3001 now limits the one-hour average to 3 mmHg (0.4 kPa).

Small cabins leave little margin (@fig:co2buildup a). If the scrubber stops at 2.5 mmHg in a capsule with 2.5 m³ of air per person, the level climbs by 7 mmHg per hour, reaching 1 % in about 45 minutes and 2 % in under two hours; on the ISS, whose pressurised volume of about 900 m³ gives some 130 m³ per person for a crew of seven, the same rise takes about a day and a half. With scrubbing, the steady-state level is inversely proportional to the air flow the scrubber cleans (panel b).

![Carbon dioxide in a closed cabin. (a) Rise in partial pressure after carbon dioxide removal stops, for different free gas volumes per crew member. (b) Steady-state partial pressure as a function of the effective scrubber flow.](figures/out/ch30_co2.svg){#fig:co2buildup width=98%}

::: example
**Example: sizing a lithium hydroxide scrubber**

A four-person capsule must remove carbon dioxide for a five-day free flight with non-regenerable lithium hydroxide (LiOH). Each crew member produces 1.0 kg of CO₂ per day.

1. CO₂ to remove: 4 × 5 × 1.0 = **20 kg**.
2. Chemistry: 2 LiOH + CO₂ → Li₂CO₃ + H₂O. Two moles of LiOH (2 × 23.95 g) absorb one mole of CO₂ (44.01 g), so the theoretical capacity is 0.92 kg of CO₂ per kg of LiOH and the minimum LiOH mass is 20/0.92 = **21.8 kg**.
3. Real beds are never fully used, because the gas breaks through before the last granules react. Shuttle practice was a 7 kg canister for four crew-days, or 1.75 kg per crew-day: **35 kg**, five canisters.
4. By-products: the reaction releases 18/44 × 20 = **8.2 kg of water** that the humidity system must remove, and about 2.1 MJ of heat per kilogram of CO₂ — some 25 W per crew member.
5. Air flow: to hold 3 mmHg (0.16 mol of CO₂ per m³ at 22 °C) the bed must remove 91 mol/day = 1.05 × 10⁻³ mol/s; capturing 90 % per pass, the fan must move 1.05 × 10⁻³ / (0.16 × 0.9) ≈ **7.2 L/s** through it (@fig:co2buildup b).
:::

## Environmental Control and Life Support Systems

The **environmental control and life support system (ECLSS)** controls pressure and oxygen, removes carbon dioxide and trace contaminants (**air revitalisation**), controls temperature and humidity, supplies and recovers water, manages waste, and detects and suppresses fire. @fig:eclssflow shows how these are linked on the ISS, the most complete system ever flown, and @tbl:eclsstech compares the technologies.

![Simplified ECLSS flow diagram of the ISS US segment. Air is scrubbed of CO₂, which a Sabatier reactor combines with hydrogen from the oxygen generator to make water; urine, humidity condensate and recovered brine water are purified for drinking and for electrolysis.](figures/out/ch30_eclss.svg){#fig:eclssflow width=98%}

### Removing Carbon Dioxide

Short missions use **lithium hydroxide** canisters that are thrown away when full: Apollo, the Shuttle and Crew Dragon all used them. The most famous are those of Apollo 13. After the oxygen-tank explosion in April 1970 the three astronauts sheltered in the lunar module, whose round canisters were sized for two people for two days; the command module's spare canisters were square. Engineers in Houston devised a way to connect them with plastic bags, cardboard and tape, and the crew built the "mailbox" from instructions read up to them (@fig:mailbox). Soyuz uses potassium superoxide, which absorbs carbon dioxide and releases oxygen, with LiOH as a supplement.

Long missions need **regenerable** systems. The ISS Carbon Dioxide Removal Assembly (**CDRA**) passes cabin air through beds of zeolite — a mineral with molecular-sized pores — that adsorb carbon dioxide; a full bed is heated and exposed to vacuum to drive the gas out while a second bed takes over. Desiccant beds first remove water, which would block the zeolite, and return it to the cabin. The Russian **Vozdukh** works on the same swing principle with three beds of an amine sorbent. A redesigned Four Bed CO₂ Scrubber, delivered in 2021, now serves as a primary system. Orion uses an **amine swing bed**, regenerated by exposure to vacuum every few minutes — compact, but it vents some water overboard.

### Making Oxygen

Short missions carry oxygen as high-pressure gas or cryogenic liquid. The ISS makes its own by **electrolysis** of water: the US Oxygen Generation Assembly (@fig:ogsrack) and the Russian Elektron split water into oxygen for the cabin and hydrogen. Each kilogram of oxygen requires 1.13 kg of water and, even for an ideal cell, about 5 kWh of electrical energy; real electrolysers need more. Backup oxygen comes from tanks delivered by cargo vehicles and from **solid-fuel oxygen generators** — "candles" of lithium perchlorate that release oxygen when burned. A candle on Mir caught fire in February 1997, filling the station with smoke.

![The "mailbox" built by the Apollo 13 crew to use the command module's square lithium hydroxide canisters in the lunar module, April 1970.](figures/photos/ch30_mailbox.jpg){#fig:mailbox width=36%}

### Closing the Oxygen Loop

Electrolysis consumes water, and carbon dioxide removed from the cabin still contains oxygen. Since 2010 the ISS has recovered part of it with a **Sabatier reactor**, which combines carbon dioxide with hydrogen from the oxygen generator over a heated catalyst:

$$ \mathrm{CO_2 + 4\,H_2 \rightarrow CH_4 + 2\,H_2O} $$

The water returns to electrolysis. The methane is vented, taking half of the hydrogen with it, and because there is not enough hydrogen to convert all the carbon dioxide, the Sabatier closes only about 50 % of the oxygen loop. Future systems may recover hydrogen from the methane or use the **Bosch reaction** (CO₂ + 2 H₂ → C + 2 H₂O), which leaves solid carbon instead.

::: figrow
![NASA astronaut Nichole Ayers servicing components of the Oxygen Generation System rack in the ISS Destiny laboratory, May 2025.](figures/photos/ch30_ogs.jpg){#fig:ogsrack}

![NASA astronaut Jessica Watkins servicing the Water Recovery System rack in the Tranquility module, June 2022.](figures/photos/ch30_wrs.jpg){#fig:wrsrack}
:::

### Trace Contaminants, Temperature and Humidity

People, materials and equipment release hundreds of trace gases — ammonia, alcohols, aldehydes, siloxanes, carbon monoxide — that would accumulate in a sealed cabin. Activated charcoal adsorbs most of them and a heated catalytic oxidiser burns the rest, while filters remove dust and microbes. Fans keep the air moving, because without convection exhaled carbon dioxide would collect around a sleeping astronaut's head. A **condensing heat exchanger**, cooled by the internal water loop, keeps the cabin at about 18–27 °C and removes the 3 kg per person per day of water vapour, which joins the water recovery system as condensate.

### Recovering Water

The ISS **Water Recovery System** (@fig:wrsrack) has two parts. The **Urine Processor Assembly** distils pretreated urine in a rotating drum at low pressure, recovering about 85 % of its water, and a newer **Brine Processor Assembly** extracts most of the rest from the concentrated brine. The **Water Processor Assembly** treats the distillate and humidity condensate with filters and ion-exchange beds, oxidises the remaining organic compounds in a catalytic reactor, and adds iodine against microbes. In June 2023 NASA announced that the system had reached its goal of recovering **98 %** of the water, up from 93–94 % before the brine processor. The Russian segment recycles humidity condensate and uses silver ions as a biocide.

### Waste, Hygiene and Fire

Toilets use air flow instead of gravity to carry waste away; the compact Universal Waste Management System, installed on the ISS in 2020, also flies on Orion. Faeces are stored and burned up in departing cargo vehicles, and crews wash with wet towels and rinseless shampoo. Smoke detectors sit in the ventilation ducts. From 2015 the US segment's carbon dioxide extinguishers were replaced by water-mist units, because carbon dioxide would create an atmosphere the crew's emergency masks cannot filter. In a fire the crew stops the ventilation, removes power, dons oxygen masks and, if necessary, retreats to the docked vehicles.

### Open and Closed Loops

Recycling hardware is heavy, consumes power and needs spares, while stored consumables cost mass every day, so the choice depends on mission duration (@fig:eclsstrade). An analysis of ISS hardware for a four-person, 450-day Mars transit found that the complete regenerative system, with three sets of spares, has a mass of 7 062 kg and replaces about 32 kg of supplies per day. It pays for itself after about 220 days — about 240 days if the residual resupply of oxygen and filters is counted — and halves the life support mass of a 450-day transit. Carbon dioxide removal pays off within about three months, but the oxygen generator, with its heavy spares, takes 557 days.

| Function | Open loop | ISS US segment | ISS Russian segment | Capsules |
|---|---|---|---|---|
| CO₂ removal | LiOH canisters | CDRA, Four Bed CO₂ Scrubber (zeolite) | Vozdukh (amine beds) | LiOH (Dragon); amine swing bed (Orion); KO₂ (Soyuz) |
| O₂ supply | Gas or liquid tanks | Electrolysis (OGA) | Electrolysis (Elektron); candles | Tanks |
| CO₂ reduction | None, CO₂ discarded | Sabatier (since 2010) | None | None |
| Water | Stored, or fuel-cell water (Apollo, Shuttle) | Urine and brine processors, WPA: 98 % | Condensate recovery | Stored |
| Trace gases | Charcoal | Charcoal and catalytic oxidiser | Similar system | Charcoal, filters |

: ECLSS technologies of crewed spacecraft. {#tbl:eclsstech}

![Open versus closed life support. (a) Cumulative mass of life support supplies for four crew with open-loop storage and with an ISS-type regenerative system. (b) Days needed for each ISS subsystem to save its own mass, including three sets of spares.](figures/out/ch30_trade.svg){#fig:eclsstrade width=98%}

The ultimate step is a **bioregenerative** system, in which plants and microbes recycle air, water and food. The Soviet BIOS-3 facility in Krasnoyarsk supported three people for 180 days in 1972–73, with wheat and vegetables providing part of the food. China's Lunar Palace 1 ran for 370 days in 2017–18 with rotating crews of volunteers and reported about 98 % closure of the material cycle, and ESA's MELiSSA programme is testing a loop of bacterial and plant compartments in Barcelona. Because one person's oxygen and food would need several tens of square metres of lit crops, plants will long supplement packaged food rather than replace physico-chemical systems. NASA's Veggie and Advanced Plant Habitat chambers on the ISS have grown lettuce, mustard greens, radishes and chile peppers (@fig:appeppers).

![Chile peppers growing in the Advanced Plant Habitat on the ISS in November 2021, during Expedition 66.](figures/photos/ch30_peppers.jpg){#fig:appeppers width=58%}

::: example
**Example: consumables for a 30-day lunar surface mission**

Three astronauts spend 30 days on the Moon with open-loop life support. Use the BVAD values: oxygen 0.89 kg, water 3.2 kg, food 1.83 kg (packaged) per crew member per day, and LiOH at the Shuttle rate of 1.75 kg per crew-day, scaled up for a CO₂ output of 1.085 kg (assuming the canister rating corresponds to the older 1.0 kg design value).

1. Crew-days: 3 × 30 = **90**.
2. Oxygen: 90 × 0.89 = **80 kg**.
3. Water (drinking, food preparation, minimal hygiene): 90 × 3.2 = **288 kg**.
4. Food: 90 × 1.83 = **165 kg**.
5. LiOH: 90 × 1.75 × 1.085 = **171 kg**.
6. Total: **704 kg**, or about **775 kg** with a 10 % margin — before tanks, cabin leakage and gas lost through the airlock on each spacewalk.

An ISS-type regenerative system would weigh several tonnes, so open loop is clearly right for 30 days. Water dominates, so a condensate recycler would be the first system worth adding for longer stays.
:::

## Living and Working in Space

### Food

Space food must be safe, nutritious, light and appetising for months. ISS menus offer some 200 items: thermostabilised pouches, freeze-dried dishes rehydrated with hot water, irradiated meat, natural-form foods such as nuts and tortillas (which do not make crumbs), and powdered drinks; salt and pepper come as liquids. Meals are a social event (@fig:issmeal). The ISS food supply has grown to 2.39 kg per person per day including packaging, which makes up almost a fifth of it. For Mars, food must keep its nutrients for up to five years, longer than current foods do.

::: figrow
![Expedition 31 crew members sharing a meal near the galley of the Zvezda service module, May 2012.](figures/photos/ch30_meal.jpg){#fig:issmeal}

![The four volunteers of NASA's CHAPEA Mission 2 inside the 3D-printed simulated Mars habitat at Johnson Space Center, November 2025.](figures/photos/ch30_chapea.jpg){#fig:chapeacrew}
:::

### Habitability and Medical Care

Each ISS crew member has a sleeping station the size of a telephone booth, with a sleeping bag tied to the wall and a door to shut out the noise of fans and pumps. Habitable volume, noise, lighting, privacy and window views all affect performance and morale on long missions (Chapter 32).

ISS medical care relies on two trained **crew medical officers**, a medical kit with ultrasound scanner, defibrillator and drugs, and flight surgeons on the ground; serious illness means returning home in a docked capsule. In January 2026 NASA's Crew-11 returned about a month early, the first time an ISS mission was ended for medical reasons; the affected crew member was reported stable. A Mars crew, with radio delays of up to 22 minutes each way and months from home, must diagnose and treat emergencies themselves.

### Psychology and Isolation

Isolation, confinement, monotony and separation from family are among the hardest problems of long missions. Agencies select crews for stability and teamwork and provide psychological support. **Analogue missions** on Earth test this: Mars-500 confined six men in a mock spacecraft in Moscow for 520 days in 2010–11, and Hawaii's HI-SEAS ran missions of up to a year on Mauna Loa. NASA's **CHAPEA** (Crew Health and Performance Exploration Analog) placed four volunteers in a 160 m² 3D-printed habitat at Johnson Space Center for 378 days in 2023–24, with simulated equipment failures, resource limits and communication delays; the second CHAPEA crew entered in October 2025 and is due to emerge at the end of October 2026 (@fig:chapeacrew).

## Crew Safety and Risk

### Lessons Paid For in Lives

Eighteen people have died in four accidents on orbital missions, and three more in the Apollo 1 ground test (@tbl:crewlosses). Each accident changed how crewed spacecraft are designed and managed. The Soyuz 11 crew died during re-entry in 1971 when a valve opened as the modules separated and the cabin lost its air; they were not wearing pressure suits, and every Soyuz crew since has worn the Sokol suit for launch and landing. Both Shuttle losses were preceded by warning signs — eroded booster seals, foam strikes on earlier flights — that had come to be accepted as normal, a pattern known as the "normalisation of deviance".

Many more crews have survived serious failures: the Apollo 13 explosion (1970); the Soyuz T-10-1 pad fire (1983) and Soyuz MS-10 booster failure (2018), thanks to launch escape systems; the Mir fire and collision (1997); and the Starliner thruster problems of 2024, after which its crew came home on a Crew Dragon. They show why crewed vehicles need **abort** capability in every phase, **safe havens**, and margins for the unexpected.

### Human-Rating Requirements

NASA's requirements are set out in its human-rating process (NPR 8705.2C, with technical requirements in NASA-STD-8719.29 since 2023) and in **NASA-STD-3001**, whose Volume 1 covers crew health, including radiation limits, and Volume 2 (Revision F, July 2026) habitability and the cabin environment. Key principles are that the system must tolerate at least one failure without catastrophe — with the actual level (one, two or more) set by safety analysis — unless a component is designed for minimum risk (like structures and pressure vessels); that the crew can abort and escape; and that the crew can monitor and control the vehicle manually.

Risk is also set as a number: NASA's Commercial Crew Program required that the probability of **loss of crew** on a mission of up to 210 days to the ISS be no worse than 1 in 270, and no worse than 1 in 500 for ascent and entry. NASA later estimated that the first Shuttle flight in 1981 carried a risk of about 1 in 12, and the mature Shuttle about 1 in 90 — consistent with two losses in 135 flights. Reliability and risk analysis (Chapter 4) identifies the dominant contributors, but experience shows that the largest risks are often the ones nobody modelled.

| Accident | Date | Crew lost | Cause | Main consequences |
|--------------|----------|------|-------------------|-------------------|
| Apollo 1 (ground test) | 27 Jan 1967 | 3 | Fire in pure oxygen at 115 kPa; inward-opening hatch | Materials, 60/40 launch atmosphere, quick-opening hatch |
| Soyuz 1 | 24 Apr 1967 | 1 | Main parachute failed to deploy; reserve tangled | Parachute system redesign |
| Soyuz 11 | 30 Jun 1971 | 3 | Valve opened at module separation; cabin depressurised | Pressure suits for launch and entry |
| Challenger (STS-51-L) | 28 Jan 1986 | 7 | Solid-booster joint seal failed in cold weather | Booster redesign, crew escape system, management reform |
| Columbia (STS-107) | 1 Feb 2003 | 7 | Foam strike broke the wing's leading edge; vehicle broke up on entry | Inspection and repair in orbit, Shuttle retirement in 2011 |

: Fatal accidents in human spaceflight. {#tbl:crewlosses}

::: ai
**AI for crew health and life support**

A Mars crew will have to handle medical emergencies without real-time help from the ground. In 2025 NASA and Google tested a prototype clinical decision-support assistant for long-duration crews; in simulated cases it reached the correct diagnosis 74–88 % of the time, depending on the condition, and similar tools could guide an astronaut through an ultrasound scan. Life support is a natural target for machine learning too: ECLSS telemetry — pressures, flows, temperatures, valve positions — can train models that detect developing faults before they become failures, and in 2025 researchers demonstrated supervised anomaly detection and diagnosis on data from the European Columbus module's ECLSS. Such **predictive maintenance** would let a crew far from Earth replace the right part before it fails and carry fewer spares (Chapter 46).
:::

::: key
**Key takeaways**

- About 780 people have flown in space; the longest single flight is 437.7 days and the longest cumulative time 1 111 days, while a Mars mission would last up to 900 days.
- Weightlessness shifts fluids headward and causes motion sickness, eye changes (SANS), bone loss of 1–1.5 % per month and muscle atrophy; about two hours of daily exercise is the main countermeasure.
- Deep-space crews receive about 1.8 mSv per day from cosmic rays; a Mars mission would exceed NASA's 600 mSv career limit. Storm shelters handle solar particle events, but shielding barely reduces the cosmic-ray dose.
- Cabin atmospheres balance hypoxia, fire and decompression sickness: the ISS uses sea-level air, while NASA has studied 56.5 kPa with 34 % oxygen for lunar surface operations.
- Each crew member consumes about 0.9 kg of oxygen, 3–4 kg of water and 1.8–2.4 kg of packaged food per day and produces 1.1 kg of carbon dioxide and 144 W of heat.
- The ISS ECLSS removes CO₂ with zeolite beds, makes oxygen by electrolysis, recovers half of the oxygen with a Sabatier reactor and recycles 98 % of its water; it pays back its mass after about 7–8 months, so open loops suit short missions and recycling suits long ones.
- Four accidents on orbital missions and the Apollo 1 fire killed 21 people; Commercial Crew vehicles must meet a loss-of-crew risk no worse than 1 in 270 per mission.
:::

::: questions
**Review questions**

1. Why do astronauts suffer orthostatic intolerance after landing? Give two countermeasures.
2. A crew member loses hip bone at 1.2 % per month for 9 months. Estimate the loss at landing and how much is recovered a year later (9-month half-time).
3. Why does shielding reduce the dose from solar particle events much more than that from galactic cosmic rays? Why is polyethylene better than aluminium?
4. Using the dose rates in @tbl:raddoserates, calculate the dose for a 180-day lunar surface mission (with 10 days of transit) and compare it with the 600 mSv career limit.
5. Calculate the inspired oxygen partial pressure, in mmHg, for a cabin at 70.3 kPa with 26.5 % oxygen. Is it within NASA's normoxic range?
6. Why is a low-pressure, oxygen-rich cabin attractive for a lunar lander that supports frequent spacewalks, and what is its main disadvantage?
7. A four-person crew sits in a capsule with 10 m³ of free air when its scrubber fails at a CO₂ partial pressure of 2.5 mmHg. How long until the partial pressure reaches 15 mmHg?
8. How do the CDRA, the oxygen generator and the Sabatier reactor work together, and why does the Sabatier close only about half of the oxygen loop?
9. Using @fig:eclsstrade, explain why Apollo carried stored oxygen and water while the ISS recycles them. Which subsystem pays back its mass fastest?
10. What did the Apollo 1, Soyuz 11 and Columbia accidents each teach designers of crewed spacecraft?
:::
