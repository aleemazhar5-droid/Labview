---
title: Data, Computing Hardware and Edge AI in Orbit
hero: ch45
abstract: Every AI system in space rests on two foundations, data and computers, and both are hard to get right. This chapter follows data from sensor to model. It covers the petabyte archives, the many kinds of space data, how labels are made, and the benchmarks, competitions and synthetic data used to train and test models. It then explains the MLOps practices that keep models honest in operations. Next it turns to hardware. It shows why radiation flips bits in neural networks, how to protect them, which processors fly in 2026, and how compression lets models fit. It then weighs processing on board against processing on the ground. It ends with updating models in orbit, federated learning across constellations, and the physics and economics of orbital data centres.
---

A modern Earth-observation satellite collects far more data than its radio link can send home. A model on the ground must wait for the data; a model in orbit must live with little power, intense radiation and a computer that cannot be repaired. Either way, it is only as good as the data it learned from. This chapter is about these two foundations of space AI: **data** and **computing hardware**.

The numbers are large. NASA's Earth science archive held 178.7 PB at the end of September 2025 and grew by about 160 TB a day. Yet in 2020 ESA's Φsat-1 screened its images with a deep neural network running on a vision chip of about 1 W. In 2025 a satellite carrying a data-centre graphics processor (GPU), of a kind that draws several hundred watts, trained a small language model in orbit. The hero image above shows HPE's Spaceborne Computer-2 on the International Space Station (ISS), which brought commercial servers and a GPU to orbit in 2021.

Chapters 43 and 44 explain the learning methods, and Chapters 46–53 apply them and ask how far to trust them. Radiation, flight computers and radio links are introduced in Chapters 2, 6 and 7.

## Data for Space AI

The key idea of this section is simple: in space AI, data are plentiful but labels are scarce. Archives hold petabytes, yet a carefully labelled training set is often a few gigabytes.

### How Much Data?

Archives dwarf the data sets that models are trained on (@fig:datavolumes). NASA's Earth Observing System Data and Information System (EOSDIS) is the largest, and 116.2 PB of it already sits in commercial cloud storage. The **Copernicus Data Space Ecosystem**, the European Union's archive, held about 91 PB online at the end of 2025, and its users downloaded 129.9 PB directly that year. **NISAR**, the NASA–ISRO radar satellite launched in July 2025, is expected to produce close to 85 TB of products a day and up to about 140 PB in three years. The **Vera C. Rubin Observatory** in Chile, which began its ten-year survey in 2026, records about 20 TB a night. It issues about 10 million alerts a night, each within about 60 seconds.

![Data volumes in the space ecosystem. (a) Archives hold tens to hundreds of petabytes, while widely used AI training and benchmark sets are thousands to tens of millions of times smaller. (b) Daily flows: what users download and archives ingest (blue) is far more than any single spacecraft can send down (violet).](figures/out/ch45_volumes.svg){#fig:datavolumes width=96%}

Telemetry — the housekeeping measurements a spacecraft sends about its own health — is smaller but richer in structure. ESA's anomaly-detection benchmark of 2024 holds 1.55 billion data points from two missions, yet only 7.32 GB compressed. Most telemetry has never been labelled.

### Kinds of Data

Each form of space data needs different models and has different traps (@tbl:spacedatatypes). Optical images resemble photographs, so everyday computer-vision methods transfer well. Radar images do not: they are speckled, complex-valued and taken from the side (Chapter 15). Telemetry, light curves and solar data are time series. Text — anomaly reports, logs and procedures — is the newest data type for space AI (Chapter 49).

| Data type | Examples | Structure | Typical AI tasks | Main traps |
|---|---|---|---|---|
| Optical multispectral | Landsat, Sentinel-2, Planet | 3–13 bands, 0.3–60 m pixels | Land cover, objects, change | Clouds, shadows, haze, sensor differences |
| Hyperspectral | EnMAP, PRISMA, Tanager-1 | 200+ bands per pixel | Minerals, methane, crops | Noisy bands, huge volumes |
| Synthetic aperture radar | Sentinel-1, NISAR, ICEYE | Complex amplitude and phase | Floods, ships, ice, ground motion | Speckle, side-looking geometry |
| Telemetry | Housekeeping channels | Multichannel time series | Anomaly detection, forecasting | Few labelled faults, mode changes |
| Spectra and light curves | Space telescopes, Rubin | 1-D signals over wavelength or time | Classification, transient alerts | Uneven sampling, rare classes |
| Text and logs | Anomaly reports, procedures | Free text | Search, summarising, assistants | Jargon, confidential content |

: Main types of space data for AI. {#tbl:spacedatatypes}

### Labels: Where the Truth Comes From

A **label** is the answer a model should learn: "this pixel is water", "this telemetry interval is an anomaly". Labels are the most expensive part of most projects, and there are four main ways to obtain them.

**Expert labels** are drawn by trained analysts. They are the most reliable but slow and costly. The So2Sat LCZ42 data set took 15 experts six months, and they judged 85 % of the labels correct. Even experts disagree, so a good project labels a sample twice and measures the disagreement.

**Crowdsourced labels** come from many volunteers or paid workers. They are cheaper but less reliable, so several people label each item and their answers are combined by vote.

**Weak labels** come from existing sources that were not made for training, such as OpenStreetMap buildings and roads or national land-cover maps. They are cheap and cover huge areas, but they contain errors. Some errors are random. Others are **systematic**: a map may omit new buildings, so the model learns that buildings are bare soil.

**Active learning** lets the model choose which samples experts should label next. The simplest rule, **uncertainty sampling**, labels the samples the current model is least sure about. One measure is the **margin** between the two most likely classes,

$$ m(x) = p_{(1)}(x) - p_{(2)}(x), $$

where $p_{(1)}$ and $p_{(2)}$ are the largest and second-largest predicted probabilities. A small margin means the sample lies near a decision boundary, where a new label teaches the most. Another measure is the **entropy** $H(x) = -\sum_k p_k(x) \ln p_k(x)$.

In @fig:labelstrategies a random forest classifies synthetic eight-band pixels. In panel (a), margin sampling with 210 labels reaches 91.3 % accuracy, while random sampling reaches only 91.2 % with 600 labels. Active learning needed about a third as many labels. In panel (b), random label errors barely matter: the forest still scores 90.2 % with half of all labels wrong, because the errors are spread over five other classes. A systematic map gap is far worse. When 40 % of urban pixels are labelled as soil, urban recall — the share of urban pixels found — falls from 87.4 % to 58.6 %. At 50 % it falls to 30.7 %.

![Two labelling strategies, computed with random forests on synthetic eight-band pixels of six classes. (a) Active learning by margin sampling (blue) reaches 91.3 % accuracy with 210 labels; random sampling (grey) is still below that with 600. (b) Random label errors (blue) hurt little; systematic errors that turn urban pixels into soil (orange), as when a reference map misses buildings, destroy the model's ability to find urban areas.](figures/out/ch45_labels.svg){#fig:labelstrategies width=96%}

The lesson is clear. Random noise can be averaged away; systematic omissions cannot. Weak labels should be checked against a small expert-labelled sample before they are trusted.

### Analysis-Ready, AI-Ready and FAIR Data

**Analysis-ready data (ARD)** are calibrated, geolocated, corrected to surface reflectance and cloud-masked, so that users can analyse them directly (Chapter 13). **AI-ready data** go further. They are cut into consistent patches or time windows, paired with labels, split into training, validation and test sets, and documented. ESA's **Major TOM** collection (2024) is an example. It offers 2 245 886 Sentinel-2 patches of 1 068 × 1 068 pixels covering more than half of Earth's surface; the L2A part alone is about 23 TB.

Good data sets follow the **FAIR principles** of 2016. Data should be **Findable**, with persistent identifiers and searchable metadata, and **Accessible** through open protocols. They should be **Interoperable**, in common formats and vocabularies, and **Reusable**, with clear licences and records of their origin. In Earth observation, the SpatioTemporal Asset Catalog (STAC) and Cloud-Optimized GeoTIFF (COG) formats put these principles into practice.

**Licensing** matters as much as format. Copernicus and Landsat data are free and open for any use. Many benchmark sets allow only non-commercial use; CloudSEN12, for example, carries a CC-BY-NC 4.0 licence. A model may inherit such limits, so the licence of every training set must be recorded before a model is sold or flown.

## Benchmarks, Competitions and Synthetic Data

A **benchmark** is a fixed data set with an agreed task and score, so that different methods can be compared fairly. Benchmarks drive progress, but they also mislead when models are tuned to them rather than to the real problem.

### Benchmark Data Sets

Widely used benchmarks are listed in @tbl:spacebenchmarks. Most Earth-observation sets come from the free Sentinel-1 and -2 data or from commercial imagery donated for research. SPEED+ serves spacecraft pose estimation, and the NASA and ESA telemetry sets serve anomaly detection.

| Benchmark | Year | Data | Size | Task |
|---|---|---|---|---|
| EuroSAT | 2019 | Sentinel-2, 13 bands | 27 000 patches | 10 land-cover classes |
| BigEarthNet (v2.0 2024) | 2019 | Sentinel-2 (+ Sentinel-1 in v2.0) | 590 326 patches (v2.0: 549 488 pairs) | Multi-label land cover |
| SEN12MS | 2019 | Sentinel-1, Sentinel-2, MODIS | 180 662 triplets | Land cover |
| So2Sat LCZ42 | 2020 | Sentinel-1 and -2 | 400 673 patch pairs | 17 local climate zones |
| SpaceNet 1–8 | 2016–22 | Commercial 0.3–0.5 m imagery | SpaceNet 8: 850 km² | Buildings, roads, floods |
| xView | 2018 | WorldView-3, 0.3 m | > 1 million objects, 1 400 km² | 60 object classes |
| fMoW | 2018 | High-resolution multispectral | 1 047 691 images | 63 land-use categories |
| xBD | 2019 | Before and after disasters | 850 736 buildings, 19 disasters | Damage level |
| CloudSEN12 | 2022 | Sentinel-2 and -1 | 49 400 patches | Cloud and shadow masks |
| SPEED+ | 2021 | Rendered and laboratory images | 59 960 + 9 531 images | Spacecraft pose |
| SMAP/MSL (Telemanom) | 2018 | Spacecraft telemetry | 82 channels, 105 anomalies | Anomaly detection |
| ESA-ADB | 2024 | Telemetry of two missions | 1.55 billion points, 844 events | Anomaly detection |

: Benchmark data sets for space AI. {#tbl:spacebenchmarks}

Three traps recur. **Leakage**: neighbouring patches in training and test sets look alike, so random splits overstate accuracy (Chapter 43); BigEarthNet v2.0 therefore splits by geography. **Saturation**: once top scores pass 98 %, a benchmark no longer separates good methods from great ones. **Label quality**: errors in a benchmark's own labels cap the score any honest model can reach.

### Competitions and Research Sprints

ESA's **Kelvins** platform has run open competitions on real mission problems since 2016. Topics have included Mars Express power, PROBA-V super-resolution, collision avoidance and spacecraft pose. In the **OPS-SAT case** (July–October 2022), teams built a small, quantisation-aware model from few labelled images to run on board OPS-SAT.

NASA's **Frontier Development Lab (FDL)** was created in 2016 by NASA, the SETI Institute and Trillium Technologies. It brings machine-learning researchers and space scientists together for research sprints of eight to ten weeks; a European version has run with ESA in Oxford. Sprints produce prototypes, and turning one into an operational system takes years.

### Synthetic Data and the Sim-to-Real Gap

Some data cannot be collected in advance: nobody has thousands of labelled photographs of a particular satellite tumbling in orbit. Engineers therefore **render** synthetic images with computer graphics, or generate synthetic telemetry from a **digital twin** — a simulation detailed enough to stand in for the spacecraft.

The danger is the **sim-to-real gap**: a model that excels on synthetic data fails on real data, because rendering never captures every detail of lighting, materials, optics and noise. SPEED+ measures this gap. A pose network trained on its rendered images scored 0.16 on synthetic validation images (lower is better). It scored 1.21 on laboratory images lit by a lightbox and 1.73 under a lamp that mimics the Sun — eight to eleven times worse.

**Domain randomisation** is the main defence. Instead of rendering the most realistic images possible, the engineer randomises everything that should not matter — lighting, background, texture, blur, noise, gain. The model then learns the one thing that stays constant, the object itself. Formally, training minimises the expected loss over the randomisation parameters $\xi$:

$$ \min_\theta \; \mathbb{E}_{\xi \sim p(\xi)} \Big[ L\big(f_\theta(\mathrm{render}(s, \xi)),\, y(s)\big) \Big], $$

where $s$ is the scene (here, the spacecraft's pose), $y(s)$ its label and $f_\theta$ the network. With luck, the real world is just one more random draw.

A toy renderer shows the effect (@fig:simtoreal). A numpy network trained on clean renders identifies a spacecraft's orientation perfectly on similar images. On "real" images with a different Sun angle, an Earth background, blur and noise, its accuracy falls to 70.3 % at half severity and 26.5 % at full severity. The same network trained on randomised renders keeps 99.6 % and 65.2 %. Randomisation narrows the gap but does not close it. The winners of ESA's 2021 pose challenge also used **domain adaptation**, which trains the network so that its internal features look the same for synthetic and real images.

![The sim-to-real gap, computed with a numpy network (400 inputs, 96 hidden units, 8 orientation classes) on 20 × 20-pixel renders of a toy spacecraft. (a) Examples from the clean training set (A), the randomised training set (B) and the "real" test set at full severity. (b) Accuracy on 3 000 "real" images as the domain shift grows; chance is 12.5 %.](figures/out/ch45_simreal.svg){#fig:simtoreal width=96%}

## MLOps: From Archive to Operations

**MLOps** (machine-learning operations) is the set of practices that take a model into reliable service and keep it there. The key idea is that a model is never finished. It is one stage in a loop of data, training, testing, deployment and monitoring that runs for the life of the mission.

### The End-to-End Pipeline

The loop for an Earth-observation mission is drawn in @fig:mlopsflow. Data flow from the sensor through the ground stations into processing and the archive. Labels are attached, and a frozen **snapshot** of training data is taken. Models are trained, registered and tested against validation gates. A model that passes is deployed on the ground or, after further checks, uplinked. Monitoring watches for drift and triggers retraining. The data shrink at each step, from terabytes a day to a model of megabytes.

![An end-to-end MLOps pipeline from satellite to model to user. Data volumes shrink from terabytes per day at the downlink to megabytes for the model. A model passes validation gates before it is deployed on the ground or uplinked; monitoring closes the loop by triggering relabelling and retraining when the data drift.](figures/out/ch45_pipeline.svg){#fig:mlopsflow width=100%}

### Versions, Registries and Validation Gates

Four habits make a pipeline trustworthy.

1. **Version the data.** Each training snapshot gets a unique identifier, often a hash of its contents, so that any model can be traced to the exact data it saw.
2. **Track experiments.** Every training run records its code version, settings, random seeds and results, so that it can be reproduced.
3. **Register models.** A **model registry** stores each released model with its version, data identifier and test results. It adds a **model card**: a short note on what the model is for, how it was tested and where it fails.
4. **Gate releases.** A **validation gate** is a test the model must pass before release. It checks accuracy by region, season and surface type, and robustness to noise and calibration changes. It also checks memory, time and power on the flight processor, and **bit-exact** agreement with the ground reference.

### Monitoring for Drift

After launch the world changes. Detectors age, calibration is updated, and seasons bring snow and smoke. This is **drift**: the data no longer match the data the model learned from. Labels arrive slowly in operations, so drift is usually detected first from the inputs. A common statistic is the **population stability index (PSI)**. For each bin $i$ of a variable, it compares the share $p_i$ of training data with the share $q_i$ of current data.

$$ \mathrm{PSI} = \sum_i (q_i - p_i)\,\ln\frac{q_i}{p_i}. $$

Values below 0.1 are usually taken as stable, and values above 0.25 signal a large shift.

In @fig:driftmonitor a deployed classifier watches a detector that loses 0.1–0.6 % of its gain per month. At month 33, a ground-processing change raises two short-wave infrared bands by 20 %. Without retraining, accuracy slides from 93.7 % to 91.2 % by month 32, then drops to 80.3 %. With a PSI alarm at 0.1, the monitor fires at months 22 and 33. Each time the model is retrained on 2 000 newly labelled pixels and recovers to about 92–93 %.

![Drift monitoring, computed with a random forest on synthetic eight-band pixels over 48 months. (a) A model that is never retrained (red) loses accuracy slowly as the detector ages and suddenly after a processing change; a model retrained when the alarm fires (green) recovers. (b) The largest population stability index across the bands, with the alarm threshold and the two alarms.](figures/out/ch45_drift.svg){#fig:driftmonitor width=96%}

### Cloud Platforms and Ground Compute

Most training and much inference happens on the ground, close to the archives (@tbl:eocloudplatforms). Users send their code to the data instead of downloading petabytes. Chapter 13 introduces these platforms; their status in October 2026 is summarised here.

| Platform | Operator | What it offers | Status, October 2026 |
|---|---|---|---|
| Google Earth Engine | Google | Catalogue of more than 80 PB and 1 000 data sets; analysis on Google's servers | Free for research; commercial use through Google Cloud |
| Copernicus Data Space Ecosystem | European Commission, ESA | About 91 PB online; all Sentinel data; processing services | Opened January 2023; replaced the old Open Access Hub (closed November 2023); 542 622 users at end of 2025 |
| NASA Earthdata Cloud | NASA, on Amazon Web Services | 116.2 PB of the 178.7 PB EOSDIS archive | Operational; serves NISAR products |
| AWS Open Data | Amazon | Free hosting of public data sets, including Landsat, Sentinel-2 and SpaceNet | Operational |
| Microsoft Planetary Computer | Microsoft | Open-data catalogue with a STAC search interface; paid "Pro" service for private data | Free computing hub retired June 2024; catalogue continues |

: Cloud platforms for Earth-observation AI. {#tbl:eocloudplatforms}

Training large models also needs clusters of GPUs or tensor processing units (TPUs), in the cloud or in agency supercomputers (@fig:discoverhpc). A foundation model may occupy hundreds of accelerators for weeks, so compute time is budgeted like ground-station time.

![Racks of the Discover supercomputer at the NASA Center for Climate Simulation at Goddard Space Flight Center. Ground clusters like this, and commercial cloud services, do most of the training for space AI.](figures/photos/ch45_discover.jpg){#fig:discoverhpc width=60%}

## Radiation and AI Hardware

The key idea of this section is that a neural network is a large block of numbers held in memory, and radiation changes numbers. Some changes are harmless; a few are catastrophic. Good design finds and protects the few.

### How Radiation Disturbs Computers

Chapter 2 explains radiation and its effects; here is a short reminder. **Total ionising dose (TID)** slowly degrades transistors as charge builds up in their oxides; it is measured in krad(Si). **Single-event effects** are caused by one energetic particle. A **single-event upset (SEU)** flips a stored bit. A **single-event functional interrupt (SEFI)** hangs a processor until it is reset. A **single-event latch-up (SEL)** creates a short circuit that can destroy the chip unless the power is cut quickly.

The upset rate of a memory comes from folding its measured **cross-section** $\sigma(L)$, the sensitive area per bit, with the flux of particles at each linear energy transfer $L$.

$$ R = \int \sigma(L)\, \frac{d\Phi}{dL}\, dL \quad \text{upsets per bit per second.} $$

Measured rates give a feel for the result. Static memory (SRAM) on two Chinese internet satellites at 1 050–1 425 km recorded about 7.6 × 10⁻⁷ upsets per bit per day, mostly over the South Atlantic Anomaly. At that rate, a model of 3.4 million 8-bit weights (27.2 Mbit) would collect about 21 upsets a day; stored as 32-bit floating-point numbers, about 83.

### Why Neural Networks Are Vulnerable

A network's **weights** are its learned parameters, stored in memory for the whole mission. Its **activations** are intermediate results, recomputed for every input. An upset in an activation spoils one result. An upset in a weight spoils every result until the memory is repaired.

Not all bits are equal. A 32-bit floating-point number has 1 sign bit, 8 exponent bits and 23 fraction bits. Flipping a low fraction bit changes a weight slightly. Flipping the highest exponent bit can multiply it by about 2¹²⁸, or 10³⁸, and one such weight turns the network's output into garbage. An 8-bit integer weight can change by at most 255 quantisation steps, so its errors are bounded.

A flip in control logic, program code or a register can hang the processor or corrupt a whole layer. Errors that go unnoticed are called **silent data corruption (SDC)**. They are more dangerous than crashes, which at least announce themselves.

### Mitigation

Engineers combine several defences, from hardware to algorithms.

- **Triple modular redundancy (TMR)** keeps three copies and takes a majority vote. If each copy works with probability $R$, the voted system works with probability $R_\text{TMR} = 3R^2 - 2R^3$, better than $R$ whenever $R > 0.5$.
- **Error-correcting codes (ECC)** add check bits to each memory word. The common **SEC-DED** Hamming code adds 8 bits to each 64-bit word (12.5 % overhead). It corrects any single-bit error and detects any double error.
- **Scrubbing** reads and rewrites memory regularly, correcting single errors before a second one lands in the same word. With $n$ bits per word and upset probability $p$ per bit between scrubs, the chance of two errors in a word is about $\binom{n}{2}p^2$. Halving the scrub interval quarters it.
- **Watchdogs** restart a processor that stops responding, and current limiters cut power within microseconds of a latch-up.
- **Selective hardening** protects only the most sensitive parts: the exponent bits of weights, the first and last layers, or the control code. A cheap software version is a **range check** that clamps any weight larger than its known maximum.
- **Algorithm-based fault tolerance (ABFT)** checks the arithmetic. For a matrix product $C = AB$, the column sums must satisfy $\mathbf{1}^\top C = (\mathbf{1}^\top A)\,B$; checking this is cheap.
- **Redundant inference** runs the model twice, or on two processors, and compares the answers.

The fault-injection experiment in @fig:bitflipnet tests these defences on a small network of 4 992 weights. Random bit flips are injected into its stored weights. Unprotected float32 weights are the weakest. At a bit-error rate of 10⁻⁴, the median accuracy is still 94.1 %, but one trial in ten falls to 90.0 % or less. At 10⁻³ the median collapses to 19.0 %, because almost every trial hits a high exponent bit. A simple range check keeps 93.8 % at 10⁻³, and int8 storage keeps 93.0 % with no protection at all. SEC-DED ECC without scrubbing keeps the float32 median at full accuracy up to 10⁻³, but fails at 10⁻², when many words collect two errors. Int8 with ECC keeps a median of 86.5 % at 10⁻², and TMR keeps nine trials in ten at full accuracy up to 10⁻³. On the top axis, 10⁻⁴ equals about 130 days in LEO without scrubbing.

![Radiation fault injection into a numpy network (8 inputs, two hidden layers of 64 units, 6 classes) trained on synthetic pixels; 40 random trials per point. (a) Unprotected memory: float32 weights fail once a high exponent bit flips; a range check or int8 storage removes most of the damage. (b) Protection with SEC-DED ECC on 64-bit words (no scrubbing) and with triple modular redundancy; the grey dashed line repeats unprotected float32 for reference.](figures/out/ch45_bitflips.svg){#fig:bitflipnet width=98%}

The experiment points to a practical recipe. Store weights as integers. Protect them with ECC and scrub often. Add a range check. Keep a protected golden copy of the model to reload when the ECC reports an uncorrectable error.

### Radiation Testing

No calculation replaces a test. **TID tests** expose parts to a cobalt-60 gamma source (ESCC 22900, MIL-STD-883 Method 1019). **Single-event tests** fire heavy ions or protons from an accelerator at a working device and count upsets, interrupts and latch-ups (ESCC 25100, JESD57). For AI processors, the best test runs the real model during exposure and checks every output, which measures silent data corruption directly.

Several AI processors have been tested this way. Intel's Myriad 2 vision chip passed a 36-hour beam test at CERN in late 2018, and later tests, unmodified, clearing it for Φsat-1. Heavy-ion tests at GANIL in France on NVIDIA Jetson Orin NX and Xavier NX modules found that about 80 % of events were correctable upsets, with no destructive latch-up. The HiMassSEE experiment on the ISS measured the environment that causes such events (@fig:himasssee).

::: data
**Data box — radiation testing of TPUs for Project Suncatcher**

Google published Project Suncatcher in November 2025. It studied AI computing in a cluster of 81 satellites in a dawn–dusk orbit at about 650 km. Trillium (v6e) TPUs were tested with 67 MeV protons at the UC Davis Crocker Nuclear Laboratory.

- Dose behind 10 mm of aluminium: about 150 rad(Si) a year, 750 rad(Si) in five years.
- The high-bandwidth memory showed irregularities after 2 krad(Si), about 2.7 times the five-year dose. One chip showed no hard failure up to 15 krad(Si).
- Silent data corruption in logic and on-chip memory: about one event per 14.4–20 rad. At one inference per second, that is about one bad result in three million.
- Uncorrectable memory errors: about one per 44 rad. Functional interrupts: about one per 5 krad per chip, and one per 450 rad for the host processor.

On 1 October 2026 a prototype with four TPUs, built with Planet, was launched on SpaceX's Transporter-18 for a year-long test.
:::

![The HiMassSEE detector kit in the US Laboratory of the ISS in August 2012. It measured how heavy shielding changes the radiation that causes single-event effects in electronics.](figures/photos/ch45_himasssee.jpg){#fig:himasssee width=52%}

## Processors for AI in Orbit

Space processors fall into three families. **Radiation-hardened** processors are designed and built to survive large doses and to be immune to latch-up. They are reliable but lag commercial chips by one to two decades. **Radiation-tolerant** parts, such as space-grade field-programmable gate arrays (FPGAs) and adaptive systems-on-chip, use commercial technology with careful design and testing. **Commercial** processors — vision chips, GPUs and TPUs — are screened, tested, shielded and supervised. @tbl:aiprocessors lists examples, and @fig:aichipperf plots their peak throughput and efficiency.

| Processor | In space | Peak throughput | Power | Radiation approach | Example use |
|---|---|---|---|---|---|
| RAD750 (BAE Systems) | 2005 | 400 DMIPS at 200 MHz | 5 W (CPU) | Hardened, 200 krad–1 Mrad | Curiosity, Perseverance, JWST |
| GR740, 4 × LEON4 (Frontgrade Gaisler) | Flight parts 2021 | 1 700 DMIPS at 250 MHz | < 3 W (typical core) | Hardened, 300 krad; latch-up immune | ESA missions, servicing vehicles |
| PIC64-HPSC (Microchip, NASA) | Samples 2025 | 28 130 DMIPS; 2 TOPS int8 | Not published | Hardened, 100 krad (tested to 200) | In qualification; not yet flown |
| Versal AI Core XQRVC1902 (AMD) | Shipping 2023 | 133 TOPS int8 | Up to about 130 W | Tolerant; latch-up immune; scrubbing | Payload data processing |
| Myriad 2 (Intel Movidius) | 2020 | > 100 GFLOPS (fp16) | About 1 W | Commercial; proton-tested | Φsat-1 cloud screening |
| Myriad X (Intel Movidius) | 2024 | 1 TOPS (neural engine) | Similar to Myriad 2 | Commercial | CogniSAT-6 |
| Snapdragon 801 (Qualcomm) | 2021 | 4 cores at 2.26 GHz | Not published | Commercial; tested | Ingenuity on Mars |
| T4 GPU (NVIDIA) in Spaceborne Computer-2 | 2021 | 130 TOPS int8 | 70 W | Commercial, inside the ISS | Edge computing on the ISS |
| Jetson Orin NX (NVIDIA) | 2024 | 100 TOPS sparse (about 50 dense) | 10–25 W | Commercial; heavy-ion tested; shielded | Aethero cubesat |
| H100 GPU (NVIDIA) | 2025 | About 2 000 TOPS int8 | Up to 700 W | Commercial | Starcloud-1 |
| TPU v6e (Google) | 2026 | 1 836 TOPS int8 per chip | Not published | Commercial; proton-tested | Suncatcher prototype (4 chips) |
| Three-Body satellite (ADA Space, Zhejiang Lab) | 2025 | 744 TOPS per satellite | Not published | Not published | 12-satellite computing constellation |

: Processors for AI in space, with vendor peak figures. DMIPS: millions of Dhrystone instructions per second, a CPU benchmark. TOPS: trillions of operations per second. {#tbl:aiprocessors}

![Processors for AI in orbit, plotted from the values in @tbl:aiprocessors. (a) Peak throughput by year first flown or available rose by about seven orders of magnitude from the RAD750 to the H100. (b) Peak operations per watt: the best commercial AI engines reach about 2 000–2 800 GOPS per watt, against 0.08 for the RAD750 — but CPU instructions and int8 neural-network operations are not directly comparable.](figures/out/ch45_procperf.svg){#fig:aichipperf width=98%}

The comparison needs care. A CPU instruction does more varied work than an 8-bit multiply–add, vendors quote peaks, and real networks reach perhaps 10–50 % of them. Even so, the gap is real. The RAD750 delivers about 0.08 GOPS per watt; Myriad 2 about 100; a Jetson Orin NX about 2 000; an H100 about 2 800.

NASA's **High-Performance Spaceflight Computing (HPSC)** project aims to narrow the gap for hardened parts. Microchip's PIC64-HPSC, announced in July 2024, has eight 64-bit RISC-V cores with vector units. NASA's figures give it about 1 343 times the speed of the GR740 on its SpaceBench benchmark at 1 GHz. As of mid-2026, its chips were in radiation, thermal and shock testing; none had flown.

**FPGAs** are chips whose logic can be rewired after manufacture, which suits high-rate payload processing. AMD's space-grade Versal AI Core adds 400 small AI engines to an FPGA. It completed Class B qualification in December 2022 and has shipped since early 2023. A lidless version aiming at the stricter Class Y is planned to fly from 2027.

Commercial chips dominate new demonstrations because they are thousands of times more efficient. Planet's Pelican-4, for example, used a Jetson Orin module to detect aircraft in its own images on 25 March 2026. The price is risk. The Ingenuity helicopter flew 72 times on Mars between April 2021 and January 2024 on a Snapdragon 801 phone processor (@fig:ingenuitysnap). Its team accepted that the chip was less robust than flight parts, and two small microcontrollers ran the time-critical flight control.

![NASA's Ingenuity Mars helicopter photographed by Perseverance's Mastcam-Z on 5 April 2021, the mission's 45th sol. Its navigation ran on a Qualcomm Snapdragon 801, a commercial smartphone processor.](figures/photos/ch45_ingenuity.jpg){#fig:ingenuitysnap width=56%}

::: history
**Φsat-1: deep learning screens images in orbit**

Φsat-1 was an ESA cubesat. It was launched on 2/3 September 2020 on Vega flight VV16 into a sun-synchronous orbit at about 530 km. Its HyperScout-2 hyperspectral camera fed an Intel Myriad 2 vision chip of about 1 W. On it ran CloudScout, a small convolutional network developed with the University of Pisa. It kept images less than 70 % cloudy for downlink. Because no real images yet existed, it was trained on Sentinel-2 images processed to imitate the new camera. On test images it was 92 % accurate with 1 % false positives, taking about a third of a second per image at about 2 W. ESA estimated that discarding cloudy images could save about 30 % of the downlink. Φsat-1 showed that a commercial AI chip could survive and work in orbit.
:::

## Making Models Fit: Compression

The key idea of compression is that most networks are far larger and more precise than they need to be. Removing the excess saves memory, uplink time, energy and radiation exposure, often with almost no loss of accuracy.

### Quantisation

**Quantisation** stores weights and activations as integers with fewer bits. In symmetric quantisation with $b$ bits, a scale factor

$$ s = \frac{\max |w|}{2^{\,b-1} - 1} $$

maps each weight $w$ to the integer $q = \mathrm{round}(w/s)$, clipped to $\pm(2^{b-1}-1)$. The network then uses $\hat w = s\,q$. The rounding error is roughly uniform between $\pm s/2$, so its variance is $s^2/12$. Each extra bit halves $s$ and improves the signal-to-noise ratio by about 6 dB. One scale per tensor is simplest; one scale per output neuron or channel fits uneven weights better.

**Post-training quantisation (PTQ)** converts a trained network directly. **Quantisation-aware training (QAT)** fine-tunes the network with quantised weights in the forward pass, so that it learns to tolerate rounding. Rounding has no useful gradient. QAT therefore uses the **straight-through estimator**, which passes the gradient through the rounding step as if it were absent.

These methods were applied to the 5 126-parameter network of @fig:bitflipnet (@fig:quantprune). At 8 and 6 bits, PTQ loses nothing measurable: 94.3 % in every case. At 4 bits it loses about one point (93.2 % per tensor, 93.7 % per neuron). At 2 bits — weights of −1, 0 or +1 times a scale — PTQ collapses to 16.7 % per tensor and 51.5 % per neuron, while QAT still reaches 93.2 %. Model size falls from 20.0 kB to 5.9 kB at 8 bits and 2.3 kB at 2 bits; the 32-bit biases and scales set a floor.

### Pruning, Distillation and Efficient Architectures

**Pruning** removes weights that matter little, usually the smallest in magnitude. Panel (c) of @fig:quantprune shows that removing 80 % of the weights without retraining drops accuracy to 75.2 %. After ten epochs of fine-tuning with the remaining weights, it recovers to 94.2 %. At 95 % pruning the fine-tuned network keeps 89.5 %. Pruning saves memory only if the hardware can skip zeros, either through sparse formats or by removing whole neurons or channels.

![Model compression of the numpy network from @fig:bitflipnet, computed on 8 000 synthetic test pixels. (a) Post-training quantisation (PTQ) is harmless down to 6 bits; below 4 bits only quantisation-aware training (QAT) holds accuracy. (b) Model size, including 32-bit biases and scales. (c) Magnitude pruning: removing most weights works only with fine-tuning.](figures/out/ch45_compress.svg){#fig:quantprune width=98%}

**Knowledge distillation** trains a small "student" network to imitate a large "teacher". The student learns from the teacher's soft probabilities, which carry more information than hard labels. Its loss has two terms:

$$ L = (1-\alpha)\,\mathrm{CE}(y, p_s) + \alpha\, T^2\, \mathrm{KL}\big(p_t^{(T)} \,\|\, p_s^{(T)}\big), $$

Here CE is the cross-entropy with the true labels and KL the Kullback–Leibler divergence between the two networks' outputs. The "temperature" $T$ softens both distributions, and $\alpha$ weights the two terms.

**Efficient architectures** are designed small from the start. Mobile networks replace a standard convolution with a **depthwise separable** one: a per-channel spatial filter followed by a 1 × 1 convolution that mixes channels. For a $k \times k$ kernel and $N$ output channels, this cuts the work by a factor of about $1/N + 1/k^2$ — nearly nine times for 3 × 3 kernels. Chapter 44 describes these architectures.

::: example
**Example: sizing an onboard cloud screen**

A small satellite will run a cloud-screening network the size of MobileNetV2: 3.4 million parameters and about 0.30 billion multiply–accumulates (MACs) for each 224 × 224-pixel tile. The processor draws 5 W and has a peak of 1 TOPS in int8; assume it reaches 30 % of peak.

1. **Model size.** In float32: 3.4 × 10⁶ × 4 bytes = 13.6 MB. In int8: 3.4 MB, four times smaller.
2. **Uplink time.** At 256 kbit/s, the int8 model takes 3.4 × 8 × 10⁶ / 256 000 ≈ 106 s — one pass. The float32 model needs 425 s.
3. **Work per tile.** Each MAC is two operations, so 0.6 × 10⁹ operations per tile. At 0.3 × 10¹² operations per second, one tile takes 2.0 ms.
4. **Energy per inference.** E = P t = 5 W × 2.0 ms = 10 mJ per tile.
5. **Per image.** A 10 000 × 10 000-pixel image holds about 2 000 tiles: about 4 s and 20 J. Screening 300 images a day uses about 1.7 Wh — small beside the energy needed to downlink the images it rejects.
6. **Radiation.** The int8 weights are 27.2 Mbit. At 7.6 × 10⁻⁷ upsets per bit per day, expect about 21 upsets a day. With SEC-DED ECC and daily scrubbing, a double error in one 72-bit word would occur only about once in four years.

For comparison, CloudScout on Φsat-1 was reported to take about 0.33 s at about 1.8 W, roughly 0.6 J per image.
:::

## On Board or on the Ground?

Every mission must decide where its models run. The key trade is between the cost of sending data down and the cost of processing them in orbit.

### The Downlink Bottleneck

A pushbroom imager with $N$ pixels across its track, ground sample distance $g$ and ground speed $v_g$ scans $v_g/g$ lines per second. With $N_b$ bands of $b$ bits each, its data rate is

$$ R = N \, \frac{v_g}{g} \, N_b \, b. $$

At 1 m resolution, 20 000 pixels across, 4 bands and 12 bits, that is 6.7 Gbit/s. A link's daily capacity is its rate times the daily contact time with ground stations. The two are compared in @fig:downlinkgap. An X-band link of 0.5 Gbit/s with 40 minutes of contact a day carries 0.15 TB. A Ka-band link of 3.5 Gbit/s carries 1.05 TB, and an optical link of 100 Gbit/s for 20 minutes carries 15 TB in clear weather. Applied to Sentinel-2's bands, the same model gives about 4.4 TB a day. That is consistent with the 1.5 TB a day each satellite sends after onboard compression of about 3:1.

![Data generated by imagers versus what links can carry. (a) Daily data from pushbroom imagers imaging 30 % of the time, against assumed daily capacities of X-band, Ka-band and optical links; Sentinel-2's reported 1.5 TB a day is shown for comparison. (b) A budget for a 3 m imager with a 24 km swath: lossless compression, cloud screening and sending only detections reduce 2.9 TB a day to 8 GB.](figures/out/ch45_downlink.svg){#fig:downlinkgap width=98%}

Optical links change the picture (Chapter 7). NASA's TBIRD cubesat sent 4.8 TB in a single pass of under five minutes in April 2023, at 200 Gbit/s. But clouds block lasers, so optical ground stations must be spread across regions with clear skies (@fig:dss13optical).

### Cloud Screening

About two-thirds of Earth is covered by cloud at any moment. More than a decade of MODIS observations gives a global cloud fraction of about 67 %: about 55 % over land and 72 % over ocean (@fig:cloudyearthmap). For an optical imager, most cloudy pixels are useless, so a model that discards them on board saves link capacity and ground storage. The risk is a **false negative** — a clear image wrongly discarded is lost forever.

::: figrow
![Average cloud cover from MODIS on Terra and Aqua. About 67 % of Earth's surface is typically cloud-covered, most of all over the oceans.](figures/photos/ch45_cloudyearth.jpg){#fig:cloudyearthmap}

![The 34 m antenna DSS-13 at Goldstone, California, fitted with an optical terminal (centre) to receive laser signals from NASA's Psyche spacecraft. Clouds and daylight limit optical links, a reason to send less data.](figures/photos/ch45_laserdownlink.jpg){#fig:dss13optical}
:::

::: example
**Example: downlink saved by onboard cloud screening**

A small satellite carries a 3 m imager with 8 000 pixels across (a 24 km swath). It has 4 bands of 12 bits, images 30 % of the time over land, and downlinks on X-band at 0.5 Gbit/s.

1. **Raw data.** 8 000 × (7 000 / 3) lines/s × 4 × 12 bits = 0.90 Gbit/s; over 30 % of a day this is 2.90 TB.
2. **Compression.** Lossless compression of 2:1 gives 1.45 TB a day. That needs 6.5 hours of X-band contact — far more than a small network of stations provides.
3. **Cloud statistics.** Assume scene cloud fractions follow a U-shaped beta distribution with a mean of 55 %, typical of land: many scenes are nearly clear and many nearly overcast. Then 42.6 % of scenes are more than 70 % cloudy.
4. **Screening.** Discarding those scenes leaves 0.83 TB a day and cuts the contact time to 3.7 hours. The discarded scenes held about 70 % of all cloudy pixels but only about 9 % of the clear ones.
5. **Detections only.** If the mission needs only objects such as ships, sending small image chips around detections (1 % of pixels) reduces the volume to about 8 GB a day — under three minutes of contact.

The screen saves about 40 % of the link but costs 9 % of the clear pixels. Whether that trade is right depends on the mission's users.
:::

### Latency, Power, Thermal and Verification Costs

Downlink is not the only factor (@tbl:onboardground). Onboard processing can cut the delay from observation to alert from hours to minutes. It also lets a satellite retask itself, as JPL's dynamic-targeting experiment on CogniSAT-6 did in 2025 (Chapter 43). But every watt of computing must be generated, stored for eclipse and rejected as heat, and flight software must be verified to a higher standard.

| Factor | Processing on board | Processing on the ground |
|---|---|---|
| Downlink | Products and alerts, megabytes to gigabytes | All raw data, terabytes |
| Latency | Seconds to minutes (with relays) | Hours, waiting for passes and processing |
| Computing | Limited; tolerant parts lag | Practically unlimited GPUs and TPUs |
| Power and heat | Adds 1–700 W to the bus | Cheap mains power |
| Updating models | Limited by uplink; must be re-verified | Any time |
| Re-analysis | Discarded data are lost | Full archive kept for future methods |
| Assurance | Flight-software standards; hard to fix | Normal software practice |

: Trade-offs between onboard and ground processing. {#tbl:onboardground}

The usual answer is a mix: simple, well-tested models on board to screen, compress and alert, and heavier models on the ground.

## Updating AI in Orbit

A model frozen at launch will age (see @fig:driftmonitor). The key idea of this section is that space AI must be designed to be updated safely, like any other flight software.

### Uploading New Models

Uploading a model needs four things. The flight software must accept new applications without a full reload. The uplink must carry the model, which 8-bit storage makes easier. Each upload must be authenticated. And a rollback path must restore the previous version if the new one fails.

Missions now demonstrate this routinely. ESA's **Φsat-2**, a 6U cubesat built by Open Cosmos and launched on 16 August 2024, runs its AI on Ubotica's CogniSAT processing board. Its applications run on the NanoSat MO Framework and can be installed and updated from the ground. At launch it carried four: image-to-map conversion, cloud detection, vessel detection and image compression. Two more — marine anomaly detection and wildfire detection — were uploaded after launch. Its operational phase from April 2025 to March 2026 was used to fine-tune the applications in orbit.

::: history
**OPS-SAT: a flying laboratory for software**

ESA's OPS-SAT, a 3U cubesat launched on 18 December 2019, was built to let outside teams test new software on a real spacecraft. ESA described its experimental computer as about ten times more powerful than those on its other spacecraft of the time. By its re-entry on 22–23 May 2024, 134 teams from 26 countries had run more than 284 experiments. Firsts included training machine-learning models on board and retraining them with live data. Its 2022 Kelvins competition asked teams to build small, quantised image classifiers designed to run on the satellite. OPS-SAT showed that frequent, safe software changes are possible when the spacecraft is designed for them.
:::

### Software-Defined Payloads and Split Computing

A **software-defined payload** is one whose function is set largely by software: a radio whose waveforms can change, or an imager whose processing chain can be replaced. Packaged as containers, its applications can serve several customers on one satellite.

**Split computing** divides a network between satellite and ground. The first layers run on board and turn the image into compact features, which are sent down to the rest of the network. Splitting where the features are smallest saves downlink without fitting the whole model on board.

### Federated Learning across Constellations

**Federated learning** trains one model across many devices without collecting their raw data. In a constellation, each satellite trains on its own images and sends only model updates, megabytes instead of terabytes. A ground station or lead satellite averages them. In the standard **FedAvg** algorithm, the new global weights are a weighted mean:

$$ w_{t+1} = \sum_{k=1}^{K} \frac{n_k}{n}\, w_{t+1}^{(k)}, $$

Here $w_{t+1}^{(k)}$ are the weights trained by satellite $k$ in round $t$ on its $n_k$ samples, and $n = \sum_k n_k$.

The simulation in @fig:fedlearnorbit has ten satellites, each seeing a different mix of surfaces, as if one flew mostly over ocean and another over desert. A satellite training alone reaches only 71.1 % on average on a balanced test set, and pooling all data on the ground gives 93.7 %. FedAvg reaches 79.0 % after 10 rounds and 88.6 % after 40 without moving any raw data. The remaining gap comes from the satellites' very different data, a known weakness of simple averaging.

![Federated learning across a constellation. (a) Each satellite trains on its own images and sends only model updates for averaging; the new global model is sent back. (b) Computed with numpy networks (8–32–6) on synthetic pixels: FedAvg (blue) approaches the accuracy of pooling all data on the ground (green dashed) and far exceeds satellites training alone (red dotted).](figures/out/ch45_fedlearn.svg){#fig:fedlearnorbit width=98%}

As of October 2026, federated learning across satellites remains **research**. Simulation studies have adapted it to intermittent contacts and to about 100 satellites, but no in-orbit demonstration across a constellation had been reported.

## Computing in Orbit: Orbital Data Centres

The boldest idea in this chapter turns edge AI inside out: put data-centre computers into orbit, powered by sunlight and cooled by radiating heat to space. The physics allows it, but the engineering and economics are unproven.

### Demonstrations and Proposals

The main projects as of October 2026 are listed in @tbl:orbitalcompute.

| Project | Who | When | What | Status |
|---|---|---|---|---|
| Spaceborne Computer-2 | HPE, NASA | 2021–23; upgraded unit 2024 | Commercial servers and a T4 GPU inside the ISS | Demonstration, in use |
| Kepler optical relay | Kepler Communications | Launched January 2026 | 10 relay satellites with optical links and GPU modules | Operational service since August 2026 |
| Three-Body Computing Constellation | ADA Space, Zhejiang Lab | May 2025 | 12 satellites, 744 TOPS each, laser links up to 100 Gbit/s | Demonstration; up to 2 800 planned |
| Starcloud-1 | Starcloud | November 2025 | One H100 GPU on a 60 kg satellite | Demonstration; Starcloud-2 reported slipped to 2027 |
| Suncatcher prototype | Google, Planet | 1 October 2026 | Four TPUs; one-year test | Demonstration; 81-satellite cluster studied |
| Orbital data centre filing | SpaceX | FCC filing January 2026 | Up to one million satellites at 500–2 000 km | Proposal |
| ASCEND | Thales Alenia Space, EU | Study 2023–24 | 10 MW by 2036, 1 GW by 2050 | Study |

: Computing in orbit: demonstrations and proposals, October 2026. {#tbl:orbitalcompute}

**Spaceborne Computer-2** showed the first benefit: less data to send. In a 2021 genomics test it reduced 182 GB of raw data to 13 MB of results, over a link limited to about two hours a week at up to 250 KB/s.

China's **Three-Body Computing Constellation** is the largest effort so far. Its first 12 satellites, launched on 14 May 2025, offer about 5 POPS (peta-operations per second) combined, linked by lasers. In February 2026 Chinese state media reported ten AI models deployed, two with 8 billion parameters. **Starcloud-1**, launched on 2 November 2025, carried one H100 GPU. In December 2025 the company reported training a small language model on the works of Shakespeare in orbit. Both are demonstrations; neither yet sells computing at scale.

### Cooling: the Radiator Problem

In orbit, the only way to lose heat is to radiate it, and almost all the power a processor uses becomes heat. A radiator panel of area $A$, emissivity $\varepsilon$ and temperature $T$ rejects

$$ P = \varepsilon\, \sigma\, A \left(T^4 - T_\text{sink}^4\right) - \alpha\, A\, q_\text{abs}, $$

Here $\sigma$ is the Stefan–Boltzmann constant, 5.67 × 10⁻⁸ W m⁻² K⁻⁴. The flux $q_\text{abs}$ is the sunlight and Earth infrared that the panel absorbs (Chapter 5). At 300 K with $\varepsilon$ = 0.9, each side radiates 413 W/m². Because of the fourth power, area grows steeply as temperature falls (@fig:radiatorarea). Hotter chips mean smaller radiators, but electronics age faster when hot.

![Radiator physics for computing in orbit. (a) Area needed to reject 1 kW: at 300 K a two-sided panel in LEO needs 1.6 m²; the ISS's real radiators need about four times the ideal area because of environmental loads, fin efficiency and margins. (b) Solar-array and radiator areas grow in step with computing power; a gigawatt-class facility would need about 1.6 km² of radiator and 2.9 km² of solar array.](figures/out/ch45_radiator.svg){#fig:radiatorarea width=96%}

The ISS gives a reality check (@fig:issradiators). Its external active thermal control system rejects up to 70 kW with six radiator wings, each 23.3 m × 3.4 m, for 475 m² of panel. That is 6.8 m² per kW, against an ideal of about 1.6 m² per kW for two-sided panels near 280 K.

![The ISS after Atlantis undocked in May 2010 (STS-132). Between the large solar-array wings, the white radiator panels on the truss reject up to 70 kW of heat — about what seven eight-GPU AI servers produce.](figures/photos/ch45_issflyaround.jpg){#fig:issradiators width=62%}

::: example
**Example: a radiator for 10 kW of computing**

A 10 kW AI server — about one machine with eight data-centre GPUs — must reject its heat at 300 K in low Earth orbit. Assume a two-sided panel with emissivity 0.9, absorbing 100 W/m² from Earth and the Sun on each side.

1. **Ideal flux.** εσT⁴ = 0.9 × 5.67 × 10⁻⁸ × 300⁴ = 413 W/m² per side.
2. **Ideal area.** With no absorbed flux, A = 10 000 / (2 × 413) = 12.1 m².
3. **With environment.** Net flux 413 − 100 = 313 W/m² per side, so A = 10 000 / (2 × 313) = 16.0 m².
4. **With margin.** Allow 30 % for fin efficiency, temperature drops and degradation: about 21 m².
5. **Mass.** ISS radiator wings weigh about 14 kg/m² (1 123 kg for 79 m²), giving about 290 kg.
6. **Launch cost.** At about $3 600/kg, the radiator alone costs about $1.1 million to launch. The solar array for 10 kW needs another 29 m².

At 350 K the area before margin would fall to 7.5 m², if the chips tolerate the heat.
:::

### Economics

The economic case rests on three claims. Sunlight in a dawn–dusk orbit is almost continuous; Google estimates that panels in some orbits collect up to eight times the yearly energy of a panel at mid-latitudes. No land, water or grid connection is needed. And launch costs are falling.

Google's Suncatcher study puts numbers on the last point. At about $200/kg, possible by the mid-2030s, launched power would cost about $810 per kilowatt per year. Terrestrial data centres pay $570–3 000. At a current price of about $3 600/kg, the estimate is $14 700 per kilowatt per year. The **ASCEND** study for the EU found orbital data centres feasible only if launchers became ten times less polluting over their life cycle.

The counter-arguments are strong. Radiators and solar arrays are large and heavy. Failed chips cannot be swapped. Radiation causes silent errors, as the Suncatcher tests showed. Data must still cross limited links to Earth, and crowded orbits add debris risk (Chapter 21). For now, orbital data centres are serious demonstrations and bold proposals, not an industry.

::: note
**Practice: qualifying an AI payload for a small satellite**

1. **Define the function and its criticality.** State what the model decides and what happens if it is wrong; keep it out of safety-critical loops. The European handbook ECSS-E-HB-40-02A (November 2024) gives guidance.
2. **Budget resources.** Set limits for power, energy per orbit, heat, memory, mass and data volume. Estimate throughput at 20–30 % of the processor's peak.
3. **Choose hardware and protection.** Predict the dose and upset rate for the orbit (Chapter 2) with a design margin of at least two. Add a latch-up current limiter, a watchdog and a radiation-tolerant supervisor for any commercial chip.
4. **Test for radiation.** Run total-dose tests on parts from the flight lot. Run proton or heavy-ion tests with the real model executing, logging every upset, interrupt and wrong output.
5. **Freeze and quantise the model.** Compare the flight version bit for bit with the ground reference on the locked test set. Measure accuracy, time and energy on the flight hardware.
6. **Inject faults.** Flip bits in weights, activations and code. Choose ECC, scrub interval and range checks that hold accuracy at the predicted upset rate with margin.
7. **Test the environment.** Run vibration, thermal-vacuum and electromagnetic tests with the processor at full load in the hot case.
8. **Secure updates.** Package the model as an application with signed uploads, version records and a rollback path. Keep safe mode independent of the AI.
9. **Plan operations.** Commission in shadow mode — deciding but not acting — and downlink samples to check the decisions. Then monitor for drift.
:::

![A NanoRacks deployer, held by the Kibo laboratory's robotic arm, releases cubesats from the ISS in February 2014. Many AI payloads are first proven on small satellites like these.](figures/photos/ch45_cubesats.jpg){#fig:cubesatdeploy width=58%}

::: key
**Key takeaways**

- Archives hold hundreds of petabytes, but labelled, AI-ready data are scarce. Active learning can cut labelling about threefold; systematic label errors harm far more than random ones.
- Benchmarks enable fair comparison but leak, saturate and contain label errors. Synthetic data need domain randomisation and adaptation to cross the sim-to-real gap.
- MLOps — versioned data, tracked experiments, model registries, validation gates and drift monitoring — keeps a model trustworthy for the life of a mission.
- Radiation flips stored bits. Float32 weights fail when an exponent bit flips; int8 storage, range checks, ECC with scrubbing and TMR restore robustness.
- Commercial AI chips are thousands of times more efficient than hardened CPUs but need testing, shielding and supervision; hardened parts such as PIC64-HPSC are closing the gap slowly.
- Quantisation to 8 bits costs almost nothing, and QAT, pruning and distillation go further. Onboard screening saves downlink but discards data for ever.
- Models in orbit must be updatable, as Φsat-2 and OPS-SAT showed. Federated learning and orbital data centres remain research and demonstration, limited by radiators, radiation and economics.
:::

::: questions
**Review questions**

1. Compare expert, crowdsourced and weak labels. How does margin sampling choose what to label next?
2. In @fig:labelstrategies, why does random label noise of 50 % reduce accuracy only slightly, while 50 % of urban pixels labelled as soil cuts urban recall to about 31 %?
3. What is the sim-to-real gap? Use the SPEED+ numbers to describe its size, and explain how domain randomisation and domain adaptation reduce it.
4. List the stages of an MLOps pipeline. What should a validation gate check before a model is uplinked?
5. Compute the PSI for a band where the training data fall into four bins in proportions 0.25 each and current data in proportions 0.10, 0.20, 0.30 and 0.40. Is retraining advised?
6. Why does a single flipped exponent bit in a float32 weight do so much more damage than a flipped bit in an int8 weight? How do ECC, scrubbing and range checks work together?
7. A model has 10 million int8 weights in SRAM with 7.6 × 10⁻⁷ upsets per bit per day. How many upsets occur per day, and how often must memory be scrubbed so that a 72-bit ECC word rarely holds two errors?
8. Explain post-training quantisation and quantisation-aware training. Why did 2-bit PTQ fail in @fig:quantprune while 2-bit QAT kept 93.2 %?
9. A 0.5 m imager with 30 000 pixels across, 4 bands and 12 bits images 20 % of the time. Estimate its daily data volume and compare it with X-band and optical links. What onboard processing would you propose?
10. Estimate the radiator area needed to reject 100 kW at 330 K from a two-sided panel absorbing 100 W/m² per side. Discuss two technical and two economic obstacles to orbital data centres.
:::
