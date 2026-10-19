# Space Exploration & Aerospace Engineering — Reference Manual: Build Plan

Target: ≥1000-page A4 PDF engineering reference manual, written in simple words but technically deep,
with photos (NASA public domain), diagrams, charts, tables, and equations. Current to October 2026.
Includes a detailed Part on AI across the space ecosystem.

## Toolchain
- Content: `src/chapters/NN-slug.md` (pandoc Markdown). Math with `$...$` / `$$...$$` (MathJax SVG).
- Figures: `figures/src/chNN.py` → `figures/out/*.svg|png` (matplotlib, shared `tools/figlib.py`).
- Photos: `tools/fetch_photos.py` (NASA Image Library, public domain) → `figures/photos/*.jpg` + `credits.json`.
- Build: `python3 tools/build.py` → per-chapter HTML → Chromium PDF → header/footer overlay → merged
  `output/Space_Aerospace_Engineering_Reference_Manual.pdf` with TOC, List of Figures/Tables, bookmarks.

## Markup conventions
- Figure: `![Caption text.](figures/out/ch03_hohmann.svg){#fig:hohmann width=80%}` → auto "FIGURE 3.4".
- Table: pipe table followed/preceded by `Table: Caption {#tbl:id}` → auto "TABLE 3.2".
- Cross-ref: `@fig:id`, `@tbl:id` → "Figure 3.4" / "Table 3.2".
- Callouts: `::: note`, `::: key`, `::: example`, `::: warning`, `::: data` fenced divs; first line `**Title**`.
- Chapter file front: `# Title {.chapter}` plus optional `<div class="ch-abstract">…</div>`.

## Outline (Parts / Chapters)  — status: [ ] todo, [x] done
Part I — Foundations
- [x] 01 The Space Ecosystem: An Overview
- [x] 02 The Space Environment
- [x] 03 Orbital Mechanics and Astrodynamics
- [x] 04 Spacecraft Systems Engineering
- [x] 05 Spacecraft Subsystems I: Structures, Thermal, Power, Mechanisms
- [x] 06 Spacecraft Subsystems II: ADCS, Propulsion, C&DH, Flight Software
- [x] 07 Space Communications and the Ground Segment
Part II — Near-Space and Suborbital
- [x] 08 High-Altitude Platforms and Space Balloons
- [x] 09 Sounding Rockets and Suborbital Vehicles
- [x] 10 Spaceplanes, Reentry and Reusable Vehicles
Part III — Satellites in Earth Orbit
- [x] 11 Earth Orbits, Constellations and Small Satellites
- [x] 12 Satellite Buses and Payload Instruments
Part IV — Earth Observation and Remote Sensing
- [x] 13 Remote Sensing Fundamentals
- [x] 14 Electro-Optical / Infrared Satellites
- [x] 15 Synthetic Aperture Radar Satellites
- [x] 16 Weather and Environmental Satellites
Part V — Communication and Navigation
- [x] 17 Communication Satellites
- [x] 18 Global Navigation Satellite Systems
Part VI — Military, Intelligence and Security Space
- [x] 19 National Security Space and Signals Intelligence
- [x] 20 Missile Early Warning Satellites
- [x] 21 Space Surveillance, Orbital Debris and SSA
Part VII — Space Environmental Science
- [x] 22 Space Weather
- [x] 23 Magnetospheric and Ionospheric Physics
Part VIII — Deep Space Exploration
- [x] 24 Deep-Space Mission Design
- [x] 25 Planetary Orbiters
- [x] 26 Space Probes and Flyby Missions
- [x] 27 Landers and Entry, Descent & Landing
- [x] 28 Planetary Rovers and Aerial Explorers
- [x] 29 Sample-Return Missions
Part IX — Human Spaceflight and Habitation
- [x] 30 Human Spaceflight Fundamentals and Life Support
- [x] 31 Crewed Spacecraft
- [x] 32 Space Stations and Habitats
- [x] 33 Extravehicular Activity Systems
Part X — Launch Systems and Infrastructure
- [x] 34 Launch Vehicle Engineering
- [x] 35 Rocket Propulsion
- [x] 36 Launch Vehicles of the World
- [x] 37 Spaceports and Ground Infrastructure
Part XI — Space Observatories
- [ ] 38 Space Telescope Engineering
- [ ] 39 Great Observatories and Deep-Space Telescopes
Part XII — Emerging Frontiers
- [ ] 40 In-Space Servicing, Assembly and Manufacturing
- [ ] 41 Space Resources and Asteroid Mining
- [ ] 42 Advanced Propulsion
Part XIII — Artificial Intelligence in the Space Ecosystem
- [ ] 43 AI Foundations for Space Systems
- [ ] 44 AI in Earth Observation, Weather and Climate
- [ ] 45 AI for Autonomy, GNC and Mission Operations
- [ ] 46 AI for SSA, Defense, Science, Exploration and Human Spaceflight
- [ ] 47 AI Across Design, Manufacturing, Launch and the Space Business; Assurance and Governance
Appendices
- [ ] A Constants, Units and Conversions
- [ ] B Equation Quick Reference
- [ ] C Solar System Data
- [ ] D Radio Frequency Bands and Allocations
- [ ] E Mission and Vehicle Databases
- [ ] F Timeline of Spaceflight
- [ ] G Acronyms and Abbreviations
- [ ] H Glossary
- [ ] I Standards, Sources and Further Reading
- [ ] J Image Credits
- [ ] Index

## Status / page tracking (per-chapter PDF pages)
01:17 02:18 03:21 04:18 05:17 06:16 07:15 08:17  → avg ≈17. Target ≥22 for chapters 09+ (≈6 500–7 500 words,
15+ figures, 6–8 tables). Later pass: add "Review questions" to every chapter and expand ch01–07 by ~1 500 words.
Workflow per chapter: photos (search → photo_list.json → fetch → contact sheet) → figures/src/chNN.py → preview →
text → build --only NN → commit.
