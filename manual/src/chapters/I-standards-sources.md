---
title: Standards, Data Sources and Further Reading
abstract: Where to go next — the engineering standards that govern spacecraft design, test, operations, debris mitigation and artificial intelligence; the open data services used to produce the figures and tables in this manual; and a selected reading list of textbooks, handbooks and reports for each Part of the book.
---

This manual explains principles and gives typical numbers. Real projects are built to standards and checked against primary data. This appendix lists the most widely used standards, the open data sources behind the computed figures and tables, and a short list of recommended books and reports. Standards are revised frequently; always use the issue specified in your contract or agency requirements.

## Engineering Standards

### Who Writes Space Standards

| Organisation | What it publishes | Access |
|---|---|---|
| ECSS — European Cooperation for Space Standardization | More than 100 standards, plus handbooks, for project management (M), engineering (E), product assurance (Q) and sustainability (U), used by ESA and European industry | Free at ecss.nl |
| NASA | NASA Procedural Requirements (NPR), Standards (NASA-STD) and Handbooks (NASA-HDBK) | Free at standards.nasa.gov and nodis3.gsfc.nasa.gov |
| US Space Force / Aerospace Corporation | Space and Missile Systems Center standards (SMC-S series), mission-assurance guides | Mostly public |
| CCSDS — Consultative Committee for Space Data Systems | Data-system and communication protocols ("Blue Books") adopted by more than 30 agencies | Free at public.ccsds.org |
| ISO TC 20/SC 14 | International standards for space systems and operations (with ISO/IEC JTC 1/SC 42 for AI) | Purchase |
| ITU-R | Radio Regulations and Recommendations on propagation, interference and coordination | Free (Radio Regulations) at itu.int |
| IADC and UN COPUOS | Space debris mitigation and long-term sustainability guidelines | Free |
| AIAA, IEEE, SAE | Industry standards (e.g. AIAA S-series for pressure vessels and mass properties; IEEE 1149, SpaceWire under ECSS) | Purchase |

: Main producers of space standards. {#tbl:apxstdorgs}

### Selected Standards by Topic

::: small
| Topic | Standard | Title or subject | Chapter |
|---|---|---|---|
| Project management | NASA NPR 7120.5 | NASA Space Flight Program and Project Management Requirements | 4 |
| Systems engineering | NASA NPR 7123.1; NASA/SP-2016-6105 Rev 2 | Systems Engineering Processes and Requirements; NASA Systems Engineering Handbook | 4 |
| | ECSS-E-ST-10C | Space engineering — System engineering general requirements | 4 |
| | ISO/IEC/IEEE 15288 | Systems and software engineering — System life cycle processes | 4 |
| Risk classification | NASA NPR 8705.4 | Risk Classification for NASA Payloads (classes A–D) | 4 |
| Verification and test | ECSS-E-ST-10-03C | Space engineering — Testing | 4, 5 |
| | GSFC-STD-7000B (GEVS) | General Environmental Verification Standard for GSFC flight programs | 4, 5 |
| | SMC-S-016 | Test Requirements for Launch, Upper-Stage and Space Vehicles | 4, 34 |
| Space environment | ECSS-E-ST-10-04C; ECSS-E-ST-10-12C | Space environment; methods for the calculation of radiation received and its effects | 2, 22 |
| Structures | NASA-STD-5001; ECSS-E-ST-32C | Structural design and test factors of safety; structural general requirements | 5 |
| Thermal control | ECSS-E-ST-31C | Thermal control general requirements | 5 |
| Mechanisms | ECSS-E-ST-33-01C | Mechanisms | 5 |
| Electrical and power | ECSS-E-ST-20C | Electrical and electronic | 5 |
| Propulsion | ECSS-E-ST-35C | Propulsion general requirements | 6, 35 |
| Attitude and orbit control | ECSS-E-ST-60-30C | Satellite attitude and orbit control system requirements | 6 |
| Software | ECSS-E-ST-40C; ECSS-Q-ST-80C; NASA NPR 7150.2; RTCA DO-178C | Software engineering; software product assurance; NASA software requirements; airborne software (often used as a reference) | 6, 53 |
| EEE components | ECSS-Q-ST-60C; NASA EEE-INST-002 | Electrical, electronic and electromechanical components; parts selection and screening | 5, 12 |
| Ground segment and operations | ECSS-E-ST-70C | Ground systems and operations | 7 |
| Space data links | CCSDS 131.0-B, 132.0-B, 231.0-B, 232.0-B, 732.0-B, 732.1-B | TM and TC synchronisation and coding; TM, TC, AOS and Unified Space Data Link protocols | 7 |
| Packets and files | CCSDS 133.0-B; 727.0-B; 734.2-B | Space Packet Protocol; CCSDS File Delivery Protocol (CFDP); Bundle Protocol (delay-tolerant networking) | 7 |
| RF and optical links | CCSDS 401.0-B; 141.0-B | Radio frequency and modulation systems; optical communications physical layer | 7 |
| Proximity links | CCSDS 211.0-B | Proximity-1 space link protocol (Mars relay) | 7, 28 |
| Data compression | CCSDS 121.0-B; 122.0-B; 123.0-B | Lossless data compression; image data compression; multispectral and hyperspectral compression | 12, 13 |
| Orbit and conjunction data | CCSDS 502.0-B; 508.0-B | Orbit Data Messages; Conjunction Data Message | 3, 21 |
| Radio spectrum | ITU Radio Regulations (2024 edition) | International allocation and coordination rules | 7, 17, App. D |
| Propagation | ITU-R P.618, P.676, P.837, P.838 | Earth–space propagation, gaseous attenuation, rain rate and rain attenuation | 7, App. D |
| CubeSats | CubeSat Design Specification Rev. 14.1 (Cal Poly); ISO 17770 | Mechanical and electrical interface requirements for CubeSats | 11 |
| Debris mitigation | ISO 24113:2023; ECSS-U-AS-10C; IADC-02-01; NASA-STD-8719.14; ESA ESSB-ST-U-007 | Debris mitigation requirements, including post-mission disposal and casualty-risk limits | 21 |
| Debris policy | UN COPUOS Space Debris Mitigation Guidelines (2007); Guidelines for the Long-term Sustainability of Outer Space Activities (2019); FCC five-year rule (in force 2024) | International and national debris guidelines and rules | 21 |
| Launch and re-entry safety | FAA 14 CFR Part 450; DAFMAN 91-710 | US commercial launch and re-entry licensing; range safety user requirements | 34, 37 |
| Human spaceflight | NASA-STD-3001 Vols 1 and 2; NASA Human Integration Design Handbook | Crew health and human-system design requirements | 30–33 |
| Planetary protection | COSPAR Policy on Planetary Protection; NASA NPR 8715.24 | Contamination control for missions to other worlds | 24, 29 |
| Machine learning in space software | ECSS-E-HB-40-02A (15 November 2024) | Machine learning qualification handbook | 45, 53 |
| AI management and risk | ISO/IEC 22989:2022; ISO/IEC 23053:2022; ISO/IEC 23894:2023; ISO/IEC 42001:2023; NIST AI RMF 1.0 (2023) | AI concepts; ML framework; AI risk management; AI management systems | 53 |
| AI regulation and aviation guidance | Regulation (EU) 2024/1689 (EU AI Act); EASA AI Concept Paper Issue 2 (2024) | Risk-based regulation of AI systems; guidance for machine-learning applications in aviation | 53 |

: Selected standards and guidelines cited in this manual. {#tbl:apxstandards}
:::

## Open Data Sources

Most figures in this manual that show real data were computed from the following open sources, which readers can use to reproduce and extend them.

::: small
| Source | Content | Used in |
|---|---|---|
| GCAT — General Catalog of Artificial Space Objects (J. McDowell, planet4589.org) | Every launch and catalogued object since 1957, with orbits, masses and owners (CC-BY 4.0) | Chapters 1, 11, 36, 37; Appendix E |
| CelesTrak (celestrak.org) and Space-Track.org | Orbital elements (TLE/OMM), satellite catalogue, debris counts, space weather indices | Chapters 3, 11, 21 |
| JPL Horizons and NAIF SPICE | Planetary, satellite and spacecraft ephemerides; mission geometry kernels | Chapters 3, 24–29; Appendix C |
| JPL Solar System Dynamics (ssd.jpl.nasa.gov) | Physical and orbital data for planets, moons, asteroids and comets; small-body database | Chapters 24–29, 41; Appendix C |
| NASA Planetary Fact Sheets (NSSDCA) | Planetary data and mission records | Appendix C |
| NOAA Space Weather Prediction Center; SILSO (Royal Observatory of Belgium) | Solar-wind data, geomagnetic indices, sunspot number | Chapters 22, 23 |
| NASA Exoplanet Archive | Confirmed exoplanets and their properties | Chapter 39 |
| Copernicus Data Space Ecosystem; USGS EarthExplorer | Sentinel and Landsat imagery and products | Chapters 13–16, 46 |
| ECMWF (ERA5 reanalysis, open forecast data) | Weather and climate data for numerical and machine-learning models | Chapters 16, 47 |
| ESA DISCOS and the annual ESA Space Environment Report | Debris and re-entry statistics | Chapter 21 |
| UCS Satellite Database (to 2023) | Active satellites by purpose and owner | Chapters 1, 11 |
| NASA Technical Reports Server (ntrs.nasa.gov) | NASA technical reports, conference papers and mission documents | All |
| eoPortal (ESA) | Mission and instrument descriptions | Chapters 12–16 |
| ITU Space Network List; ITU-Rpy software | Satellite network filings; ITU-R propagation models in Python | Chapter 17; Appendix D |
| NASA Image and Video Library (images.nasa.gov) | Public-domain photographs used throughout this manual | All; Appendix J |

: Open data sources. {#tbl:apxdatasources}
:::

## Further Reading

### Part I — Foundations

- J. R. Wertz, D. F. Everett and J. J. Puschell (eds.), *Space Mission Engineering: The New SMAD*, Microcosm Press, 2011 — the standard reference for mission and spacecraft sizing.
- P. Fortescue, G. Swinerd and J. Stark (eds.), *Spacecraft Systems Engineering*, 4th ed., Wiley, 2011.
- H. D. Curtis, *Orbital Mechanics for Engineering Students*, 4th ed., Butterworth-Heinemann, 2020.
- D. A. Vallado, *Fundamentals of Astrodynamics and Applications*, Microcosm Press (latest edition).
- R. R. Bate, D. D. Mueller and J. E. White, *Fundamentals of Astrodynamics*, Dover, 1971 (2nd ed. 2020).
- A. C. Tribble, *The Space Environment: Implications for Spacecraft Design*, revised ed., Princeton University Press, 2003.
- D. G. Gilmore (ed.), *Spacecraft Thermal Control Handbook, Vol. I*, 2nd ed., The Aerospace Press, 2002.
- F. L. Markley and J. L. Crassidis, *Fundamentals of Spacecraft Attitude Determination and Control*, Springer, 2014.
- NASA, *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2, 2016.
- NASA Ames Research Center, *State-of-the-Art of Small Spacecraft Technology* (updated annually).
- G. Maral, M. Bousquet and Z. Sun, *Satellite Communications Systems*, 6th ed., Wiley, 2020.

### Parts II–III — Near Space, Suborbital Flight and Satellites

- M. D. Griffin and J. R. French, *Space Vehicle Design*, 2nd ed., AIAA, 2004.
- NASA Sounding Rockets Program Office, *Sounding Rocket Program Handbook* (NASA Wallops Flight Facility).
- Cal Poly CubeSat Laboratory, *CubeSat Design Specification*, Rev. 14.1, 2022.

### Parts IV–V — Earth Observation, Communications and Navigation

- C. Elachi and J. van Zyl, *Introduction to the Physics and Techniques of Remote Sensing*, 3rd ed., Wiley, 2021.
- T. M. Lillesand, R. W. Kiefer and J. W. Chipman, *Remote Sensing and Image Interpretation*, 7th ed., Wiley, 2015.
- A. Moreira *et al.*, "A tutorial on synthetic aperture radar", *IEEE Geoscience and Remote Sensing Magazine*, 1(1), 2013.
- T. Pratt and J. E. Allnutt, *Satellite Communications*, 3rd ed., Wiley, 2019.
- P. Misra and P. Enge, *Global Positioning System: Signals, Measurements, and Performance*, 2nd ed., Ganga-Jamuna Press, 2006.
- P. J. G. Teunissen and O. Montenbruck (eds.), *Springer Handbook of Global Navigation Satellite Systems*, Springer, 2017.

### Parts VI–VII — Security, Debris and the Space Environment

- H. Klinkrad, *Space Debris: Models and Risk Analysis*, Springer, 2006.
- ESA Space Debris Office, *ESA's Annual Space Environment Report* (published each year).
- Secure World Foundation, *Global Counterspace Capabilities: An Open Source Assessment* (updated annually).
- M. G. Kivelson and C. T. Russell (eds.), *Introduction to Space Physics*, Cambridge University Press, 1995.
- D. Hastings and H. Garrett, *Spacecraft–Environment Interactions*, Cambridge University Press, 1996.

### Part VIII — Deep-Space Exploration

- S. Kemble, *Interplanetary Mission Analysis and Design*, Springer, 2006.
- A. J. Ball, J. R. C. Garry, R. D. Lorenz and V. V. Kerzhanovich, *Planetary Landers and Entry Probes*, Cambridge University Press, 2007.
- R. D. Braun and R. M. Manning, "Mars exploration entry, descent and landing challenges", *Journal of Spacecraft and Rockets*, 44(2), 2007.
- A. A. Siddiqi, *Beyond Earth: A Chronicle of Deep Space Exploration, 1958–2016*, NASA SP-2018-4041, 2018.

### Parts IX–X — Human Spaceflight and Launch

- W. J. Larson and L. K. Pranke (eds.), *Human Spaceflight: Mission Analysis and Design*, McGraw-Hill, 2000.
- NASA, *Human Integration Design Handbook*, NASA/SP-2010-3407 (revised).
- G. P. Sutton and O. Biblarz, *Rocket Propulsion Elements*, 9th ed., Wiley, 2017.
- D. K. Huzel and D. H. Huang, *Modern Engineering for Design of Liquid-Propellant Rocket Engines*, AIAA, 1992.
- D. M. Goebel, I. Katz and I. G. Mikellides, *Fundamentals of Electric Propulsion*, 2nd ed., Wiley/JPL Space Science and Technology Series.
- R. W. Humble, G. N. Henry and W. J. Larson (eds.), *Space Propulsion Analysis and Design*, McGraw-Hill, 1995.

### Parts XI–XII — Observatories and Emerging Frontiers

- P. Y. Bely (ed.), *The Design and Construction of Large Optical Telescopes*, Springer, 2003.
- J. P. Gardner *et al.*, "The James Webb Space Telescope Mission", *Publications of the Astronomical Society of the Pacific*, 135, 068001, 2023.
- K. F. Long, *Deep Space Propulsion: A Roadmap to Interstellar Flight*, Springer, 2012.
- V. Badescu (ed.), *Moon: Prospective Energy and Material Resources*, Springer, 2012.
- F. von der Dunk and F. Tronchetti (eds.), *Handbook of Space Law*, Edward Elgar, 2015.

### Part XIII — Artificial Intelligence

- S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020.
- I. Goodfellow, Y. Bengio and A. Courville, *Deep Learning*, MIT Press, 2016.
- C. M. Bishop and H. Bishop, *Deep Learning: Foundations and Concepts*, Springer, 2024.
- G. Camps-Valls, D. Tuia, X. X. Zhu and M. Reichstein (eds.), *Deep Learning for the Earth Sciences*, Wiley, 2021.
- ECSS, *ECSS-E-HB-40-02A Machine Learning Handbook*, 15 November 2024.

::: note
**Keeping up to date**

Space changes quickly. For current events, the most reliable sources are the agencies themselves (NASA, ESA, JAXA, CNSA, ISRO, Roscosmos press releases), company announcements checked against independent trackers, Jonathan McDowell's *Jonathan's Space Report*, Gunter's Space Page, the trade press (SpaceNews, SpacePolicyOnline, NASASpaceflight, Spaceflight Now) and peer-reviewed journals (*Acta Astronautica*, *Journal of Spacecraft and Rockets*, *Advances in Space Research*, *Remote Sensing of Environment*). Cross-check any number that matters against a primary source.
:::
