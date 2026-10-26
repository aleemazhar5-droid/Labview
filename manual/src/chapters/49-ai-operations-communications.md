---
title: AI for Mission Operations, Communications and Networks
hero: ch49
abstract: Every spacecraft is flown from the ground by people and software that watch its telemetry, plan its activities, schedule its contacts and send its commands. This chapter shows where machine learning and optimisation now help with that work, and where they do not yet. It covers anomaly detection in telemetry, from fixed limits to learned models, false-alarm budgets, prognostics of batteries and wheels, automation, digital twins and language-model assistants, and the human factors that decide whether they are trusted. It then turns to scheduling ground contacts and to communications - cognitive radio, signal recognition, adaptive coding, beam and spectrum management, interference, laser-mesh routing and 6G - and ends with the security of ground segments. Small models run in Python make each method concrete.
---

Spacecraft are flown from the ground. A flight control team watches the stream of **telemetry** (TM) — measurements that a spacecraft sends about its own health. It plans activities, books contacts with ground stations and sends **telecommands** (TC). The hero image above shows NASA's Artemis II flight control team in Houston on 10 April 2026, during the splashdown of the first crewed Moon mission in 54 years. Rooms like this one have worked in much the same way since Apollo: skilled people, many screens and fixed alarm limits.

Two trends are now changing this. The first is scale. A single observatory produces tens of thousands of telemetry channels, and one operator flies more than ten thousand satellites. The second is the arrival of practical machine learning, optimisation and language models. This chapter explains how these tools help to watch telemetry, predict failures, automate routine work, schedule ground networks, run radio links and route data through constellations. It separates what is operational, what has been demonstrated and what is still research, as of October 2026.

The chapter builds on Chapter 7 (communications and the ground segment), Chapter 11 (constellations) and Chapter 17 (communication satellites). The learning methods are explained in Chapters 43 and 44, and data and computing in Chapter 45. Autonomy on board the spacecraft is the subject of Chapter 48, space situational awareness and defence of Chapter 50, and assurance and security of AI of Chapter 53.

## Mission Operations Today

The key idea of this section is that mission operations are a loop: plan, command, monitor and analyse. Machine learning helps at every step, but the loop and the people in it remain.

### What a Control Centre Does

A **mission operations centre** holds the people and software that fly a spacecraft (Chapter 7). Its core is the **mission control system** (MCS). The MCS turns raw telemetry frames into named, calibrated parameters, checks them against limits, raises alarms and sends commands. Around it sit four other functions. **Flight dynamics** determines the orbit and plans manoeuvres. **Mission planning** turns requests into a timeline that respects power, thermal, data and visibility limits. The **ground network** provides antennas and contact time. **Engineering support** — subsystem experts on call — investigates anything unusual.

Work follows a daily cycle. Planners build tomorrow's timeline. Command sequences are checked on a simulator and uplinked in a ground contact. During each contact, controllers watch live telemetry and alarms. Afterwards, engineers look at trends in the stored data. When something goes wrong, an **anomaly report** records the symptoms, the cause and the fix. Years of these reports, with the telemetry, command logs and procedures, are the raw material for the learning methods in this chapter.

### How Much Telemetry?

Spacecraft telemetry is small in bytes but rich in structure. NASA's James Webb Space Telescope records telemetry at about 100 kbit/s. On the ground it is unpacked into about 36 000 named parameters, called **mnemonics**, with 4 000 more derived on the ground. Some are sampled every 0.064 s, others every 32 s or more. A 28-minute file holds about 10 million samples. EUMETSAT routinely reports about 46 000 housekeeping parameters for each Sentinel-3 satellite. @tbl:opsscale gives more examples.

| System | Scale | What it means for operations |
|---|---|---|
| James Webb Space Telescope | 36 000 telemetered + 4 000 derived points; ~100 kbit/s | Too many for people to watch; trending software is essential |
| Sentinel-3 (EUMETSAT) | ~46 000 housekeeping parameters per satellite | Learned outlier detection is trialled on a subset |
| ESA anomaly benchmark (2024) | 1.55 billion data points, 844 annotated events | Real anomalies are rare: 31–118 per mission |
| Planet Dove fleet (2018) | >200 satellites, >2 000 passes a day, 8 engineers | Operations run by exception; nominal passes automated |
| Starlink (June–November 2025) | 148 696 collision-avoidance manoeuvres in six months | Decisions too frequent for people to make one by one |

: Examples of the scale of modern operations. Sources: SpaceOps 2025 papers (JWST, Sentinel-3), ESA-ADB paper, Planet (IAC 2018) and SpaceX's report to the US Federal Communications Commission. {#tbl:opsscale}

### From One Satellite to Thousands

A traditional mission has a team for each spacecraft, with people on console around the clock. That model does not scale to constellations. In 2018 Planet flew more than 200 Dove imaging satellites with a team of eight engineers, five in Berlin and three in San Francisco. Its nominal operations — commanding each pass, scheduling contacts, reporting and delivering images — were fully automated. Python scripts acted as a virtual operator that fixed the most common anomalies. By 2022 this had cut daily fleet monitoring from about four hours to about 30 minutes. It also ended night shifts for the larger SkySat satellites.

This style is called **management by exception**. Software flies the nominal mission; people handle what the software cannot. At the largest scale, decisions are taken by machines because there are too many for people. Starlink satellites made 148 696 collision-avoidance manoeuvres between June and November 2025, mostly decided on board when the predicted collision probability exceeded about 3 in 10 million (Chapters 21 and 48).

@fig:opspipeline49 shows where learning and automation enter the ground segment. The data path runs from spacecraft to engineers. Decision support grows beside it: monitoring models trained on the archive, planning solvers, automation scripts, assistants and digital twins. Colours give the status in 2026. Monitoring and scheduling tools are operational in some centres. Language-model assistants are pilots, and natural-language commanding is research.

![Where learning and automation enter the ground segment. The data path (navy) runs from the spacecraft through the ground network and mission control system to the archive and the engineers. Decision-support functions (blue) are trained on the archive or fed by live telemetry; their status in 2026 is colour-coded.](figures/out/ch49_pipeline.svg){#fig:opspipeline49 width=96%}

## Watching Telemetry: Anomaly Detection

The key idea of this section is that a monitor must find rare, varied faults among millions of normal samples, while raising few false alarms. Learned models of normal behaviour find faults that fixed limits miss, but only if their false alarms are controlled.

### Limits and Their Limits

The classic monitor is the **limit check**. Each parameter has a lower and an upper limit, often a soft "warning" pair and a hard "alarm" pair. A value outside them raises an alarm. Limits can depend on the mode: a heater current is checked against one range when the heater is commanded on and another when it is off. Limit checks are simple, fast and easy to explain. They also catch most serious failures, because a failed unit usually drives some parameter far out of range.

Their weakness is everything else. A temperature can be normal for daylight but wrong in eclipse. A slow drift stays inside the limits for months, then crosses them when it is too late to act. And every limit that is set too tight produces false alarms. Each false alarm costs a person's attention, and too many teach people to ignore alarms.

The false-alarm budget is simple arithmetic. If $N$ channels are each checked $f$ times a second, and each check has a false-alarm probability $p$, the expected number of false alarms per day is:

$$ n_{\text{FA}} = N \, f \cdot 86\,400 \cdot p. $$

For a threshold at $k$ standard deviations of Gaussian noise, the two-sided probability is $p = 2Q(k)$, where $Q$ is the tail probability of the standard normal distribution. @fig:falsealarm49 applies this to 10 000 channels checked every 10 s. A 3σ threshold, common in textbook statistics, gives about 233 000 false alarms a day. Fewer than 10 a day needs about 5.3σ for perfectly Gaussian noise. Real telemetry noise has heavier tails, so empirical thresholds must be set from the data. Requiring several consecutive exceedances helps greatly when noise is independent, but much less when it is correlated in time.

![The false-alarm budget of a large telemetry set. (a) False alarms per day for 10 000 channels checked every 10 s, against the threshold in multiples of the noise standard deviation. (b) The per-check false-alarm probability allowed for 10 alarms a day, against the number of channels; the right axis gives the equivalent Gaussian threshold.](figures/out/ch49_falsealarm.svg){#fig:falsealarm49 width=96%}

::: example
**Example: false alarms per day for 10 000 channels**

A science satellite has 10 000 monitored channels, each checked every 10 s. The team can investigate about 10 alarms a day.

1. **Checks per day.** 10 000 × 86 400 s / 10 s = 8.64 × 10⁷ checks.
2. **At p = 10⁻⁶ per check.** 8.64 × 10⁷ × 10⁻⁶ ≈ **86 false alarms a day** — about nine times the budget. Checking every second instead would give 864.
3. **Allowed probability.** 10 / 8.64 × 10⁷ = **1.16 × 10⁻⁷** per check. For Gaussian noise this is a two-sided threshold of **5.3σ**.
4. **At a 5σ threshold.** p = 5.7 × 10⁻⁷, giving about 50 false alarms a day.
5. **Persistence.** Requiring three exceedances in a row at 3σ gives (2.7 × 10⁻³)³ ≈ 2 × 10⁻⁸ per check, or about 1.7 a day — if the noise is independent. Correlated noise raises this, so the rule must be tested on archived data.
6. **Lesson.** With thousands of channels, the per-channel false-alarm rate must be tiny. Any learned detector needs the same budget, set on real data.
:::

### Kinds of Anomaly

An **anomaly** is behaviour that differs from what is expected. Not every anomaly is a fault: a commanded manoeuvre or a calibration looks unusual the first time but is normal for the operators. ESA's benchmark calls these **rare nominal events**. @tbl:anomalytypes lists the main kinds of anomaly and the detectors that suit them.

| Kind | What it looks like | Example | Detectors that suit it |
|---|---|---|---|
| Point | One sample far from its neighbours | Bit flip, sensor glitch | Limits, prediction residuals |
| Contextual | Normal value at the wrong time or mode | Daylight temperature in eclipse | Models that use orbit phase and mode |
| Collective | Normal values in an abnormal sequence | Oscillating control loop | Sequence models, windowed features |
| Drift | Slow change of level or trend | Rising friction, sensor ageing | Trend tests, residuals against other channels |
| Multivariate | Each channel normal, their combination not | Current rises while load is unchanged | Cross-channel models, isolation forests |

: Kinds of telemetry anomaly and the detectors that suit them. {#tbl:anomalytypes}

### Learning What Normal Looks Like

Learned monitors share one idea: model normal behaviour from history, then score how far new data departs from it. There are three main families.

**Prediction-based** detectors forecast each channel and watch the error. A model $f$ predicts the value $x_t$ from recent history and from context $\mathbf{c}_t$, such as orbit phase and commanded mode. The standardised residual is

$$ z_t = \frac{|x_t - f(x_{t-L}, \dots, x_{t-1}, \mathbf{c}_t)|}{\sigma_{\text{res}}}, $$

where $\sigma_{\text{res}}$ is the residual spread on normal training data. An alarm is raised when $z_t$ exceeds a threshold. JPL's **Telemanom** system, described in 2018, used a **long short-term memory** (LSTM) network for each of 82 channels of the SMAP satellite and the Curiosity rover (Chapter 44). It smoothed the errors and set thresholds automatically from their recent distribution. On 105 labelled anomalies it reached 87.5 % precision and 80 % recall (Chapter 43).

**Reconstruction-based** detectors squeeze the data through a narrow layer and rebuild it. An **autoencoder** with encoder $h$ and decoder $g$ is trained so that $g(h(\mathbf{x})) \approx \mathbf{x}$ for normal data. The anomaly score is the reconstruction error $\lVert \mathbf{x} - g(h(\mathbf{x})) \rVert^2$. Patterns the network never saw are rebuilt badly.

**Distance- and isolation-based** detectors look at where a sample sits among the training data. The k-nearest-neighbour score is the distance to the $k$-th closest normal sample. A one-class support vector machine draws a boundary around normal data. An **isolation forest** (2008) builds random trees that split the data at random values of random features. Unusual points are isolated after few splits. The score is

$$ s(\mathbf{x}) = 2^{-\overline{h}(\mathbf{x}) / c(n)}, $$

where $\overline{h}$ is the average path length over the trees and $c(n)$ the average for $n$ normal points. Scores near 1 mean anomalous.

### A Test on Synthetic Telemetry

To see the strengths of each family, this chapter's script builds six housekeeping channels for a satellite in a 96-minute orbit with 36 % eclipse. Battery voltage, battery temperature, bus current, panel temperature, wheel speed and heater duty all follow the orbit, a commanded payload mode and a 14-day seasonal cycle. Slow unmodelled variations are added. Fourteen days train each detector. Fourteen more days test it, with 14 point, 12 contextual and 8 drift anomalies injected (@fig:tmanomalies).

Three detectors are compared. The **fixed limits** are the training minimum and maximum. The **learned predictive detector** is a small neural network for each channel, written in numpy. It predicts the channel from the other five channels, the orbit phase and the mode, and scores the largest standardised residual. The **isolation forest** from scikit-learn sees the channel values, orbit phase and their changes. Each detector's threshold lets 0.1 % of normal samples alarm — about 1.4 false alarms a day.

![Three injected anomalies and the detectors' responses. Top: a spike that stays inside the limits, a segment copied from the wrong part of the orbit, and a slow drift (navy; grey shows the signal without the anomaly; dashed lines are the fixed limits). Bottom: each detector's score divided by its alarm threshold.](figures/out/ch49_telemetry.svg){#fig:tmanomalies width=98%}

@fig:tmroc shows the results. The predictive network found all 34 injected events, and its sample-by-sample area under the ROC curve (AUC; Chapter 43) was 0.81. The fixed limits found all 8 drifts, but only after 45 % of each ramp, on average. They caught 5 of the 14 spikes — those that left the normal range — and 1 of the 12 contextual events. The isolation forest found only half the drifts and none of the spikes or contextual events.

![Detector performance on the synthetic test set. (a) Sample-by-sample receiver operating characteristic (ROC) curves on a logarithmic false-positive axis. (b) Share of injected events caught at a false-alarm rate of 0.1 % of normal samples.](figures/out/ch49_roc.svg){#fig:tmroc width=96%}

Two lessons follow. First, context is what makes learned detectors useful. The network knew the orbit phase and the other channels, so a value copied from daylight into eclipse stood out. Second, a generic detector is not automatically better than limits. The isolation forest's scores saturate outside the training range: a far-out spike is isolated no faster than the many normal points near the edge. A real system should therefore keep limit checks and add learned detectors beside them.

These synthetic data follow simple physics that a network learns easily. Real telemetry is harder, as the next section shows.

### Benchmarks and Real Results

Comparing detectors fairly needs real, labelled data. Until 2024 the main public sets were the SMAP and Curiosity channels released with Telemanom. ESA then published a much larger benchmark, built with operations engineers at its European Space Operations Centre (ESOC) in Darmstadt.

::: data
**Data box — ESA's anomaly-detection benchmark (ESA-ADB), 2024**

- **Data.** Real telemetry from three ESA missions, two used in the benchmark; 1.55 billion data points, 7.32 GB compressed. Developed by ESA with KP Labs (Poland); first released in June 2024.
- **Mission 1.** 76 channels (58 monitored), 14 years, 200 annotated events: 118 anomalies, 78 rare nominal events and 4 data gaps.
- **Mission 2.** 100 channels (47 monitored), 3.5 years, 644 events: only 31 anomalies, but 613 rare nominal events such as manoeuvres and resets.
- **Scoring.** Event-wise precision first, because operators care about false alarms; then which channels and subsystems were flagged, and timing.
- **Results.** An adapted Telemanom was best for Mission 1, with an event-wise F0.5 score of 0.968 for anomalies alone. A simple windowed isolation forest was best on a small channel subset of Mission 2 (0.949). No algorithm found the nine real anomalies hidden among Mission 2's rare nominal events, and adding channels added false detections.
- **Conclusion of the authors.** Typical algorithms are not yet good enough for operators; new methods are needed. A July 2026 follow-up found supervised graph networks more accurate, and simple unsupervised methods much cheaper to run.
:::

### Operational Tools

Learned monitors have been used in real control centres for about two decades, usually beside limit checks and for selected parameters. @tbl:monitoringtools summarises the best-documented ones.

| Tool | Organisation | Method | Status |
|---|---|---|---|
| Inductive Monitoring System (IMS) | NASA Ames | Clusters of nominal data; distance to nearest cluster | Used for ISS gyroscopes from about 2005; about a dozen ISS systems by 2012 |
| Novelty Detection | ESA/ESOC | k-nearest-neighbour outlier score on orbit statistics | Used on ESA missions in the 2010s; trialled by CNES in 2013 |
| NOSTRADAMUS | CNES with TeSA | One-class support vector machine | Prototype (2014), operational assessment |
| ATHMoS | DLR German Space Operations Center | Outlier detection; later neural prediction about 4.5 h ahead | Developed 2016–19 |
| Telemanom | NASA JPL | LSTM prediction and dynamic thresholds | Piloted on SMAP; false positives limited its use |
| CHART outlier tools | EUMETSAT | k-nearest neighbours; neural network | Routine on a subset of parameters; Sentinel-3 assessment (2025) |

: Learned telemetry monitors with published operational use or trials. {#tbl:monitoringtools}

EUMETSAT's experience is typical. Its Sentinel-3 flight control team ran two outlier detectors in parallel: a k-nearest-neighbour tool and a neural network. They found that the definition of the training data mattered more than the algorithm. A detector that is "mathematically right" can still bury a team in novel-but-harmless detections. Adding ground knowledge, such as the timeline of commanded operations, cut those detections. Engineers also needed to see *why* a parameter was flagged, which favoured simple methods. The tools did find real anomalies, including the signatures of micrometeoroid or debris impacts on the satellite.

::: history
**Landmark: twenty years of learned telemetry monitoring**

- **1988.** NASA's Mission Control in Houston tested expert systems beside conventional displays for Space Shuttle communications (Chapter 43).
- **About 2005.** ISS attitude-control engineers in Houston adopted NASA Ames' Inductive Monitoring System to watch a failing gyroscope. It was learned from months of normal data. By 2012 it watched about a dozen systems.
- **2010s.** ESA's Novelty Detection, CNES's NOSTRADAMUS and DLR's ATHMoS brought outlier detection to European control centres.
- **2018.** JPL's Telemanom showed that LSTM prediction with automatic thresholds could catch most labelled anomalies, but its false positives kept it from central use.
- **2024.** ESA released ESA-ADB, the first large, operator-labelled benchmark. It showed how far typical algorithms remain from operators' needs.
- **2025–26.** EUMETSAT reported its Sentinel-3 trial. ESOC's search assistant was in use on 14 missions, and the Aerospace Corporation and Google showed a proof-of-concept agent for triage in large constellations.
:::

### From Detection to Diagnosis

An alarm says that something is wrong. **Diagnosis** says what, and **root-cause analysis** says why. In a large constellation one fault often triggers dozens of alarms across subsystems. The first step is therefore to group alarms that share a time, a satellite and a likely cause.

Classical diagnosis uses engineering knowledge: fault trees, failure-mode tables and model-based reasoners that compare telemetry with a model of the system (Chapter 6). Learning adds three things. It can match a new alarm pattern to similar past anomalies in the archive. It can learn which alarms usually occur together and which one comes first, which hints at causation. And it can summarise the context — recent commands, space weather, ground-station problems — that an engineer would otherwise collect by hand.

In April 2026 the Aerospace Corporation and Google's public-sector arm showed a proof-of-concept tool for large constellations in low Earth orbit. It links an anomaly to recent payload tasks or space-weather events and proposes possible root causes. It is meant to replace minutes of manual cross-checking by on-call engineers between separate screens. It is decision support, not a replacement for engineers. A JPL research paper from 2025 tried similar "agentic" detection on Deep Space Network data systems. Its authors reported preliminary results that were not yet robust to false positives.

![Nzinga Tull, Hubble systems anomaly response manager, in the control room at NASA's Goddard Space Flight Center on 15 July 2021. A month earlier Hubble's payload computer had stopped, and the team switched to backup hardware to restore science. Diagnosis of this kind is still human work, supported by data tools.](figures/photos/ch49_hubbleops.jpg){#fig:hubbleanomaly width=62%}

## Prognostics and Health Management

The key idea of this section is that predicting *when* a part will fail is worth more than detecting that it has. Prognosis combines a physical degradation model with data, and must report its uncertainty honestly.

### Remaining Useful Life

**Prognostics and health management** (PHM) estimates the **remaining useful life** (RUL) of a component: the time until it can no longer meet its requirement. Batteries, reaction wheels, gyroscopes, thrusters and solar arrays all wear out in ways that can be trended.

A lithium-ion battery in low Earth orbit charges and discharges about 15 times a day, some 5 500 cycles a year. Its capacity fades. Early fade is often proportional to the square root of time, as a surface layer grows on the electrode. Later, fade can accelerate. A simple model of the capacity fraction $Q$ is

$$ Q(t) = 1 - a\sqrt{t} - b\,t^2 , $$

with the coefficients $a$ and $b$ learned from the satellite's own data. Because $Q$ is linear in $a$ and $b$, **Bayesian linear regression** gives their joint uncertainty in closed form. Thousands of sampled curves then give a distribution for the date when $Q$ falls below the end-of-life threshold.

@fig:batteryrul applies this to a synthetic battery with monthly capacity estimates and 1.2 % noise. The true end of life, at 70 % capacity, is at 6.06 years. A prognosis made after 2.5 years puts the end of life at 5.75 years (median), with a 90 % interval of 4.9–7.8 years. After 4.5 years of data the median is 6.35 years and the interval shrinks to 6.08–6.71 years. A straight line fitted at 2.5 years says 6.7 years, with no hint of its uncertainty. The model form matters: when this script also allowed a free linear term, the early intervals were far too narrow.

![Battery capacity-fade prognosis. (a) Monthly capacity estimates (dots), the true fade (dashed), prognoses made at 2.5 and 4.5 years with 90 % bands, and a straight-line fit. (b) The predicted end-of-life date from each prognosis.](figures/out/ch49_battery.svg){#fig:batteryrul width=96%}

Operators use exactly this kind of tool. Planet's PROTOS, built for the five RapidEye satellites, used a **Kalman filter** (Chapter 43) to estimate each battery's depth of discharge from charge counting and voltage. A fade model with measured temperatures predicted when each 15 Ah battery would reach 50 % capacity. A genetic algorithm then re-planned imaging, downlinks and heater use to slow the fade. Planet estimated a 15 % longer mission life for satellites already past their 7.25-year design life.

![NASA astronaut Andrew Morgan on the International Space Station's port truss on 11 October 2019, during a spacewalk to replace older nickel–hydrogen batteries with lithium-ion ones. Trending of battery capacity tells operators when such work is needed.](figures/photos/ch49_batteryeva.jpg){#fig:batteryeva49 width=60%}

### Wheels, Gyroscopes and Other Wear-Out Parts

Reaction wheels and gyroscopes have ended or reshaped several missions. Kepler lost its second wheel in 2013, which ended its original mission. Dawn lost wheels in 2010 and 2012 and finished its mission on thrusters. Hubble has flown with a single gyroscope since June 2024, which costs about 12 % of its observing efficiency.

Wheel health shows in friction torque, motor current, temperature and speed noise. A rise in drag torque at a given speed, or bursts of current noise, can precede failure by months. Learned models help in two ways: they remove normal dependence on speed and temperature, so that the residual trend shows wear, and they compare many identical wheels across a fleet. Most published wheel-prognosis work still uses ground life tests or single satellites. Fleet-wide learned prognosis is rarely documented in the open literature.

## Automating Operations

The key idea of this section is that automation should take over routine, well-understood work, while people keep the judgement and the authority. The newest tools — digital twins and language-model assistants — are useful when their output is checked.

### From Scripts to Lights-Out Operations

Automation in a control centre grows in steps (@tbl:autolevels). At the first level, people type every command. At the highest, software runs the mission and people are called only when something unusual happens. Most modern constellations work at the third or fourth level. Most flagship science missions work at the second, with automation for routine passes and people on console for critical events.

| Level | What software does | What people do | Typical use |
|---|---|---|---|
| 1 Manual | Displays data, checks limits | Send every command, watch every pass | Early operations, critical events |
| 2 Assisted | Runs approved procedures step by step | Start procedures, confirm critical steps | Science missions, GEO satellites |
| 3 Automated passes | Runs nominal contacts and planning | Review reports in working hours | Small constellations, mature missions |
| 4 Management by exception | Detects, triages and fixes known anomalies | Handle new problems, on call | Large constellations (e.g. Planet) |
| 5 Autonomy | Decides on board, including safety actions | Set goals and policies, audit | Collision avoidance, deep space (Chapter 48) |

: Levels of automation in spacecraft operations. {#tbl:autolevels}

**Lights-out operations** means that nobody is on console for routine passes. The ground system schedules contacts, uplinks the command load, downlinks data and checks health by itself. If a check fails, it pages an on-call engineer. The key technology is not AI but reliable procedure automation: scripts written in an operations language, tested on a simulator and placed under configuration control. Learning enters where rules are hard to write: deciding whether an unusual pattern is safe to ignore, or ranking which satellite to look at first.

### Ground Digital Twins

A **digital twin** is a model kept in step with one real system, using its own telemetry. In operations, the oldest form is the **operational simulator**. It runs the real flight software on emulated processors, with models of the rest of the spacecraft and its environment. Every command plan for a major mission is checked on such a simulator before uplink. Teams also train on it for failures.

Learning makes twins faster and closer to the real vehicle. Learned surrogate models can replace slow thermal or power models. Model parameters can be fitted to flight data as the spacecraft ages. Twins can then answer "what if" questions in seconds, such as how a new pointing plan will affect battery depth of discharge. In December 2025 JPL used a digital twin of Perseverance, which simulates more than 500 000 telemetry variables, to check rover drives proposed by vision–language models before they were sent to Mars (Chapters 44 and 48).

![OPTIMISM, the full-scale engineering twin of the Perseverance rover, at the Mars Yard garage at NASA's Jet Propulsion Laboratory on 29 October 2021. Physical test beds like this one and software twins are used to check commands before they are sent to Mars.](figures/photos/ch49_optimism.jpg){#fig:optimismtwin width=60%}

### Language-Model Assistants

Operations knowledge is scattered across procedures, design documents, test reports, anomaly reports, logs and the telemetry database. Finding the right page during an anomaly can take longer than fixing the fault. **Large language models** (LLMs; Chapter 44) can search, summarise and draft from this material. The safest pattern is **retrieval-augmented generation** (RAG): the system retrieves the relevant passages and the model answers from them, citing its sources.

ESOC's **Operations Companion (OCAI)** is the best-documented example. According to a 2025 paper, it was in use on 14 ESOC missions for search and for training new flight control teams. It combines keyword search, a semantic search on embeddings and a knowledge graph built from operations vocabulary. It covers telemetry and command archives, procedures, anomaly reports, manuals and logs. Language-model answers with references were being added. A commercial mission control system from Telespazio Germany planned to integrate it, with constellr's HiVE thermal-imaging constellation as the pilot mission.

Start-ups are also building language-model features into mission control software. One, Quindar, raised 18 million US dollars in November 2025 for software that covers planning, flight dynamics and command and control. Earlier that year it described an "AI autopilot" with manual override. Published evidence of how well such assistants work in real operations is still thin. @tbl:llmrisks lists the main risks and the usual defences.

| Risk | Example in operations | Defence |
|---|---|---|
| Hallucination | Invented limit value or procedure step | Answers only from retrieved sources, with citations; people check |
| Stale or wrong sources | Superseded procedure retrieved | Configuration-controlled document store; version tags |
| Over-trust | Operator accepts a plausible diagnosis | Show evidence and confidence; training; audits |
| Unsafe action | Assistant drafts a hazardous command | No direct command access; validation and approval gates |
| Data leakage | Export-controlled data sent to an outside service | Models hosted on site or in accredited clouds; access control |
| Prompt injection | Malicious text in a log or document changes behaviour | Treat retrieved text as data; restrict tools (Chapter 53) |

: Risks of language-model assistants in mission operations and common defences. {#tbl:llmrisks}

### Natural-Language Commanding

The next step — telling a spacecraft what to do in plain words — is still research. Since 2024 researchers have used language models as "operators" in simulations. In one, a model controlled spacecraft in a pursuit–evasion game built on the Kerbal Space Program simulator and ranked second in the challenge. Others propose language models that turn goals into plans for an onboard planner.

The risks are clear. A spoken request is ambiguous, while a telecommand must be exact. A model can produce a command that is valid in form but wrong in intent: the right command sent to the wrong unit, or at the wrong time. Any practical system therefore needs strict layers. The model translates the request into a structured command. The command is checked against the command database and flight rules. It is simulated on the digital twin. A person approves it, and critical commands keep their usual two-step protection.

### People and Automation

Automation changes the human job; it does not remove it. Decades of research in aviation and process control name three effects. **Automation bias** is the tendency to accept a machine's output without checking, or to miss what it fails to flag. **Trust calibration** is the match between how much people trust a tool and how reliable it is. Both over-trust and under-trust are harmful. **Skill fade** is the loss of manual skill and system knowledge when people rarely practise them.

These effects create an irony first described in 1983: the more reliable the automation, the less prepared people are for the rare day it fails. Good practice follows from this. Show the evidence behind each alert, not just a score. Report the detector's measured precision so that operators know how often it is right. Keep people practising on the simulator, including failure scenarios. And design the hand-over from software to person carefully, with enough context to act.

::: example
**Example: operator workload saved by automated triage**

A constellation of 300 satellites produces about 1 200 alarms a day. Most are known, harmless patterns such as eclipse transitions. Manual triage takes about 3 minutes per alarm.

1. **Manual workload.** 1 200 × 3 min = 3 600 min = **60 hours a day**, or 7.5 eight-hour shifts.
2. **Grouping.** Correlated alarms on the same satellite within 10 minutes are merged. With 3 alarms per group on average, there are 400 incidents.
3. **Classification.** A learned classifier closes 80 % of incidents as known patterns: 320 closed, **80 left** for people.
4. **Human review.** Each remaining incident gets more context and takes 6 minutes: 80 × 6 = 480 min = **8.0 hours**.
5. **Audit.** People spot-check 5 % of the closed incidents at 2 minutes each: 16 × 2 = 32 min.
6. **Result.** 8.5 hours instead of 60 hours a day — a saving of **86 %**, from 7.5 shifts to about 1.1.
7. **Price.** If 5 real anomalies a day pass through and the classifier wrongly closes 1 % of them, one real anomaly is missed every 20 days. The audit, and limit checks that bypass the classifier, are there to catch it.
:::

## Scheduling Contacts and Ground Networks

The key idea of this section is that antenna time is a scarce resource shared by many spacecraft. Optimisation, not learning, does most of the work, but learning helps to predict demand and to speed up solvers.

### The Deep Space Network

NASA's **Deep Space Network** (DSN) serves more than 40 missions with antennas at Goldstone, Madrid and Canberra (Chapter 7). Demand routinely exceeds capacity, often by up to 40 %. JPL reported that the gap between requested and schedulable time grew from about 300 hours a week in 2011–12 to about 500 hours by late 2015.

Since July 2011 the DSN has been scheduled with **Service Scheduling Software** (S3). Each mission enters its needs as requirements: how many hours, which antennas, which time windows. A scheduling engine turns them into tracks, using systematic search and then local repair to resolve conflicts. The draft is then negotiated among the missions, peer to peer. Research at JPL has tried deep reinforcement learning (2021) and mixed-integer programming (2021) for the same problem. These are still research. The hardest part is not the algorithm but agreeing what "fair" means among missions.

![The 70 m antenna DSS-14 at the Goldstone Deep Space Communications Complex in California, under the night sky in September 2025. Its time is shared among dozens of missions through an automated scheduling and negotiation process.](figures/photos/ch49_goldstone.jpg){#fig:dss14stars width=42%}

### Ground Stations as a Service

Small-satellite operators often buy antenna time instead of building stations. **Ground-station-as-a-service** (GSaaS) providers sell passes or minutes on shared networks through web interfaces (Chapter 7). Amazon Web Services opened AWS Ground Station in 2019. Microsoft retired its Azure Orbital Ground Station on 18 December 2024 and sold its ten 6 m antennas. KSAT reported nearly 300 antennas in 2022, and more than 52 000 passes in one month on its small-satellite network.

On a shared network, scheduling becomes a market with many users. Each operator wants enough contacts, with short gaps between them, at the lowest cost. The provider wants high antenna use without conflicts. Automated scheduling interfaces, with priorities and pre-emption rules, make this work. Learning helps to forecast demand and to predict which passes will fail through weather or equipment problems.

### Scheduling a Constellation's Contacts

The problem can be stated exactly. A **pass** $p$ is a window when satellite $s(p)$ is visible from station $g(p)$, from $t_p^{\text{start}}$ to $t_p^{\text{end}}$. A binary variable $x_p$ is 1 if the pass is used. Each antenna can track one satellite at a time, with a set-up gap between passes. Each satellite can talk to one station at a time and has $D_s$ gigabytes waiting. The delivered data $y_s$ is limited by both:

$$ \max \sum_s y_s + \lambda\, z \quad \text{subject to} \quad y_s \le D_s, \quad y_s \le \sum_{p:\,s(p)=s} R\,(t_p^{\text{end}} - t_p^{\text{start}})\, x_p, \quad z \le y_s / D_s \text{ for all } s, $$

with the antenna and satellite conflict constraints. Here $R$ is the downlink rate and $z$ is the share of data delivered for the worst-served satellite, so $\lambda$ buys fairness. This is a **mixed-integer linear programme** (MILP). Standard solvers handle problems with thousands of passes in seconds.

@fig:contactsched compares it with two greedy rules for 36 imaging satellites in six polar planes and three single-antenna stations: Svalbard, Inuvik and Awarua. Over 24 hours there are 827 visible passes. Each satellite has 100–300 GB waiting, 7 040 GB in all, at 3 GB a minute. At Svalbard more than one satellite is in view 54 % of the time, so passes compete. Taking passes first-come, first-served delivers 69.8 % of the data and leaves nine satellites below half. Taking the longest passes first delivers 76.9 %. The MILP, solved in under a second, delivers 81.6 %, and every satellite gets at least 66 %.

![Scheduling 36 satellites over three single-antenna stations for one day. (a) Number of satellites in view of each station during the first 6 hours; above the red line passes compete for one antenna. (b) Share of each satellite's waiting data delivered, sorted, for two greedy rules and the mixed-integer programme.](figures/out/ch49_schedule.svg){#fig:contactsched width=98%}

Real schedulers add many more constraints: antenna slew times, uplink needs, data generation through the day, station costs and weather. They re-plan several times a day as passes fail. Learning has two roles here. It can predict inputs, such as data volumes and pass reliability. It can also learn heuristics that speed up a solver, or policies that schedule directly, as in the DSN studies. The optimisation model above still provides the constraints and the yardstick.

## AI in Space Communications

The key idea of this section is that radios increasingly sense their environment and adapt to it. Learning helps to recognise signals, choose waveforms, share beams and spectrum, and find interference. Most of it is research or early deployment, but some is already inside commercial systems.

### Cognitive Radio and Spectrum Sensing

A **cognitive radio** senses its radio environment and changes its frequency, power, waveform or timing to work better. The simplest sensing method is **energy detection**: compare the power in a band with the noise floor. More advanced methods recognise the type of signal present, which is where learning enters.

NASA's **SCaN Testbed** on the International Space Station, operated from 2012, was the main flight laboratory for such ideas. It carried three software-defined radios that could be reprogrammed from the ground. In a 2018 experiment, a cognitive engine on the ground used reinforcement learning to choose channels. When jammed, it told the satellite transmitter to switch to the channel expected to stay clear longest. The closed loop worked against several types of jammer, but no throughput figures were published.

![The SCaN Testbed, then called CoNNeCT, during a test at NASA's Glenn Research Center before its launch to the International Space Station. Its three software-defined radios were used from 2012 to try reconfigurable and cognitive communication in orbit.](figures/photos/ch49_scantb.jpg){#fig:scantestbed width=52%}

### Recognising Signals

**Automatic modulation classification** identifies how a received signal is modulated — BPSK, QPSK, 16QAM and so on (Chapter 7). It is used in spectrum monitoring, interference hunting and signals intelligence (Chapter 19). The classical method uses **higher-order cumulants**: statistics of the complex baseband samples $y$ that differ between constellations but not with carrier phase. For example, with $M_{pq}=\mathrm{E}[y^{p-q}(y^*)^q]$,

$$ C_{40} = M_{40} - 3M_{20}^2, \qquad C_{42} = M_{42} - |M_{20}|^2 - 2M_{21}^2 . $$

Normalised by $M_{21}^2$, noise-free BPSK has $C_{42} = -2$, QPSK $-1$ and 16QAM $-0.68$. Noise pushes all of them toward zero.

Deep learning changed this field after 2016, when researchers fed raw I/Q samples to convolutional networks. Their open RadioML data sets grew to 24 modulations and 2.56 million examples, at signal-to-noise ratios from −20 to +30 dB (2018). Residual networks reached about 95 % accuracy at high SNR, and much less at low SNR.

@fig:modclass49 repeats the classical approach on synthetic signals. Six modulations used in satellite links are generated, 512 symbols each, with random phase, a small frequency offset, unknown gain and noise. Ten cumulant and amplitude features feed two classifiers. A depth-3 decision tree on only $|C_{40}|$ and $C_{42}$, a rule-like expert classifier, levels off at 83 % because it cannot separate 16QAM from 64QAM. Gradient-boosted trees on all ten features reach 98–99 % above 14 dB, 78 % at 6 dB and 39 % at 0 dB, against 17 % for chance. At 6 dB the dense QAM constellations are still confused with each other.

![Modulation classification of synthetic I/Q signals. (a) Accuracy against signal-to-noise ratio for a two-feature decision tree and for gradient-boosted trees on ten features. (b) Confusion matrix of the boosted trees at 6 dB.](figures/out/ch49_modclass.svg){#fig:modclass49 width=96%}

### Adaptive Coding and Modulation

Satellite links above 10 GHz fade in rain (Chapter 17). A link with **constant coding and modulation** (CCM) must use a robust waveform that works through the worst fade it is designed for. In clear sky, which is most of the time, it wastes capacity. **Adaptive coding and modulation** (ACM), standardised in DVB-S2 (2005) and DVB-S2X (2014), changes the modulation and code rate — the **MODCOD** — as the measured signal-to-noise ratio changes. The receiver reports its $E_s/N_0$ (energy per symbol over noise density). The transmitter then picks the most efficient MODCOD whose threshold is below the measured value minus a safety margin.

@fig:acmgain simulates one year of a Ka-band downlink with a clear-sky $E_s/N_0$ of 16 dB. Rain falls 5.4 % of the time, with fades from a standard log-normal model: 2.3 dB is exceeded 1 % of the time and 9.4 dB 0.1 % of the time. For 99.9 % availability, a fixed link must use 8PSK 3/5 at 1.78 bit/symbol. ACM driven by measurements 30 s old needs only a 0.6 dB margin and averages 4.10 bit/symbol — 2.3 times more — within 1 % of ideal ACM.

![Adaptive coding and modulation over a synthetic Ka-band rain-fade year. (a) Six hours around the year's deepest fade: Es/N0 (top) and spectral efficiency of fixed and adaptive MODCODs (bottom). (b) Mean throughput at 99.9 % availability for fixed coding, three ACM schemes and ideal ACM.](figures/out/ch49_acm.svg){#fig:acmgain width=98%}

Where does learning help? Not with a fast loop, which already works almost ideally. It helps when decisions must be made well ahead: planning a pass several minutes early, setting uplink power, or choosing beams and gateways. If the measurement is 5 minutes old, a fixed margin of 3.0 dB is needed and throughput falls to 3.31 bit/symbol. The script then learns a state-dependent margin from the first 90 days. It is a quantile of how much the fade can change, given the current fade and its trend. This raises throughput to 3.73 bit/symbol — 13 % more at the same availability — because the margin is small in clear sky and large in rain. Published research uses neural networks and weather radar or forecasts in the same role.

::: example
**Example: throughput gain of adaptive coding and modulation**

Use the results of @fig:acmgain for a carrier of 250 million symbols per second (Mbaud). Ignore framing overhead.

1. **Fixed coding.** 8PSK 3/5 needs 5.5 dB plus a 0.5 dB implementation margin; it works 99.912 % of the time. Throughput: 250 × 10⁶ × 1.78 × 0.99912 ≈ **445 Mbit/s**.
2. **ACM, 30 s loop.** Mean 4.096 bit/symbol: 250 × 10⁶ × 4.096 ≈ **1 024 Mbit/s**, a factor of **2.30**.
3. **Ideal ACM.** 4.130 bit/symbol, 1 033 Mbit/s: the 0.6 dB safety margin costs less than 1 %.
4. **Why so large?** In clear sky the link uses 32APSK 5/6 at 4.12 bit/symbol, which needs 14.3 dB plus margin. The fixed link must keep about 9.4 dB in reserve for rare fades.
5. **Five-minute-old data.** A fixed 3.0 dB margin gives 3.305 bit/symbol (826 Mbit/s). The learned, fade-dependent margin gives 3.727 bit/symbol (932 Mbit/s): **13 % more** at the same 99.9 % availability.
6. **Caveat.** The gain depends on climate, frequency and clear-sky margin. Systems with a smaller clear-sky margin gain less.
:::

### Beams, Power and Spectrum in High-Throughput and LEO Systems

Modern high-throughput satellites have hundreds of spot beams, and LEO broadband satellites steer many beams with phased arrays (Chapter 17). Demand is uneven: a city at night, an airport at noon, a ship crossing an ocean. **Beam hopping** lights each beam only part of the time, in a pattern that follows demand. The first over-the-air demonstration, in ESA's BEHOP project in June 2018, used DVB-S2X "superframes" through a conventional Eutelsat satellite. Digital payloads, such as those on Eutelsat Quantum (launched 2021) and many newer satellites, make such flexibility routine.

Choosing which beams to light, with how much power and bandwidth, is a large combinatorial problem that changes every few milliseconds to minutes. Operators use optimisation and heuristics. Since about 2018, many research papers have trained **deep reinforcement learning** agents for beam hopping, power control and channel allocation in GEO and LEO systems. In simulation they often beat simple heuristics in delay and throughput. Hybrid methods, in which a network proposes a pattern and an optimiser repairs it so that all constraints hold, are the most promising. Commercial operators rarely publish what their resource managers use, so the operational use of learning here is hard to confirm.

### Interference: Detection and Geolocation

Interference is a daily problem for satellite operators. Causes include badly pointed terminals, cross-polarised carriers, terrestrial 4G and 5G signals and, increasingly, deliberate jamming (Chapter 18 for navigation signals). Monitoring systems scan the spectrum around the clock. Learning helps in three steps, as in ESA's SkyMon project, completed in 2021. A model first recognises known carriers from their spectral shape. A detector then flags spectra that depart from the expected mask, and a classifier names the type of interference. Researchers at KTH and the Swedish Space Corporation showed in 2019 that LSTM models trained on real spectrum data could find short and long interference events in time and frequency.

Finding *where* an interferer is uses physics, not learning. The same uplink signal is received through the wanted satellite and a neighbouring one. The difference in arrival time and the difference in Doppler shift define curves on the Earth that cross at the transmitter. Learning can still help by matching carriers between satellites and by flagging unusual emitters (Chapter 19).

## Networks in Orbit

The key idea of this section is that a constellation with inter-satellite links is a network whose shape changes every second. Classical routing works well. Learning is studied for traffic prediction, failures and the joint control of space and ground networks.

### Routing in Laser Meshes

Iridium has routed calls through radio crosslinks since 1997, with up to four links per satellite. Starlink uses lasers. In January 2024 SpaceX reported more than 9 000 lasers in orbit carrying more than 42 petabytes a day. Links ran at up to 100 Gbit/s over distances up to 5 400 km. The constellation has grown much larger since. The US Space Development Agency's Transport Layer also links its satellites optically (Chapter 19).

In a **Walker-delta** shell (Chapter 11), each satellite can link to two neighbours in its own plane and one in each neighbouring plane. This gives a grid that wraps around the Earth. Routing then becomes a **shortest-path** problem on a graph: satellites are nodes, links are edges weighted by distance (delay), and Dijkstra's algorithm finds the fastest path. Because the satellites move, the graph is recomputed every few seconds. Light in vacuum travels about 47 % faster than in optical fibre, so long space paths can beat fibre.

@fig:lasermesh49 builds a 1 584-satellite shell at 550 km and 53°, with four laser links per satellite, using the networkx library. From London to New York the best path uses four satellites and three laser hops. The one-way delay is 21.2 ms, against about 35.5 ms for fibre that is 1.3 times longer than the great circle. London to Singapore takes 40.8 ms, against about 69 ms. When links fail at random, routing simply goes around them. With 30 % of links failed, the median delay hardly changes. Near 50 %, the grid starts to break into pieces, as theory predicts for a square grid, and some routes need long detours.

![Routing in a laser-linked Walker-delta constellation. (a) Snapshot of the 1 584 satellites (dots) and the shortest paths from London to New York and Singapore. (b) One-way delay against the share of laser links failed at random (median and 5–95 % band of 30 draws), with fibre estimates.](figures/out/ch49_routing.svg){#fig:lasermesh49 width=98%}

Where can learning add value? Shortest paths are easy; managing load is not. Traffic surges move with the Earth's rotation and the time of day. Ground gateways and laser terminals fail. Some links are lost each time a satellite crosses a plane boundary or points near the Sun. Research uses learned traffic forecasts, reinforcement-learning routing and graph neural networks to spread load and pre-compute routes. The bar is high: a learned router must beat well-tuned classical algorithms that are fast, predictable and easy to verify.

### Network Digital Twins and Self-Driving Networks

A **network digital twin** is a running model of a whole network: satellites, links, gateways, traffic and the control software. Operators use it to test changes before applying them — a new routing policy, a software update, a gateway closure. Learned models make twins fast enough to run in a loop. One example is a graph neural network that predicts delay and loss for a traffic pattern far faster than a packet-level simulator.

The long-term aim, shared with terrestrial telecoms, is a **self-driving network**. Operators state goals ("keep latency below 40 ms for this customer"), and software turns them into configurations, watches the result and corrects it. Large constellations already automate much of this. How much of it uses learning, rather than rules and optimisation, is rarely published.

### Toward AI-Native 6G Non-Terrestrial Networks

Satellites are joining the mobile standards. The 3GPP standards body added **non-terrestrial networks** (NTN) in Release 17 (2022), so that phones and IoT devices can use satellites. Release 19 (2025) added **regenerative payloads**, which carry a full base station on the satellite. 6G studies started in Release 20, including learning-based features of the radio interface such as compressed channel-state feedback. First 6G specifications are expected around 2028–29. The ITU's framework for 6G (IMT-2030), adopted in 2023, lists AI and ubiquitous connectivity among its aims.

"AI-native" means that learned models are built into the radio and network from the start, with standard ways to train, test and update them. For satellites this could cover beam management, handover prediction for fast-moving cells, Doppler and timing correction, and energy saving. All are research or pre-standard work in 2026. Direct-to-device services from Starlink, AST SpaceMobile and others (Chapter 17) give the commercial pull. @tbl:commsai49 summarises the status of AI across communications and networks.

| Problem | Typical method | Status (2026) |
|---|---|---|
| Spectrum monitoring, carrier recognition | Learned classifiers on spectra | Commercial products and ESA projects |
| Modulation classification | Cumulant features; convolutional and residual networks | Mature research; used in monitoring and signals intelligence |
| Interference detection | LSTM and anomaly detection on spectra | Demonstrated on real data; early products |
| ACM and power control | Feedback loops; learned fade prediction | ACM operational; learning research |
| Beam hopping, resource allocation | Optimisation; deep reinforcement learning | Optimisation operational; RL research |
| Anti-jamming channel selection | Reinforcement learning | Flight experiment (SCaN Testbed, 2018) |
| Laser-mesh routing | Shortest paths; learned traffic forecasts, RL | Classical operational; learning research |
| 6G NTN air interface | AI/ML features under study in 3GPP | Standards work |

: Status of AI in space communications and networks, October 2026. {#tbl:commsai49}

![The Tracking and Data Relay Satellite TDRS-L being prepared in January 2014, shortly before launch. Relay satellites, ground stations and laser meshes together form the networks whose contacts, links and routes must be scheduled.](figures/photos/ch49_tdrs.jpg){#fig:tdrsl49 width=38%}

## Securing Ground Segments and Links

The key idea of this section is that the ground segment is the easiest way into a space system. Machine learning helps defenders spot unusual behaviour, but attackers can target the learning itself (Chapter 53).

Ground systems are ordinary computer networks with special equipment attached: servers, operator workstations, modems, antennas and links to cloud services. They face the same attacks as any business network, plus some of their own. The best-known case came on 24 February 2022, the first day of Russia's full-scale invasion of Ukraine. Attackers abused the management network of Viasat's KA-SAT system to push a "wiper" program, later named AcidRain, to user modems. Tens of thousands of modems in Ukraine and across Europe stopped working. Spill-over cut remote monitoring of 5 800 wind turbines in Germany. The European Union attributed the attack to Russia in May 2022.

Learning-based defence works at several layers:

- **Network intrusion detection.** Models of normal traffic between ground-segment computers flag unusual connections, volumes or timing. Like telemetry monitors, they must meet a strict false-alarm budget.
- **Command anomaly detection.** A model of normal command sequences flags commands that are valid but unusual: wrong time, wrong order, wrong source. This adds to the encryption and authentication of telecommands (CCSDS Space Data Link Security; Chapter 7).
- **Telemetry for security.** The anomaly detectors described earlier can also reveal tampering, such as an unexpected mode change or a software reload.
- **Jamming and spoofing detection.** Learned classifiers on signal power, spectra and receiver statistics detect jamming of command links and spoofing of navigation signals (Chapter 18). Research has trained such detectors for intermittent jamming of telemetry and telecommand links.

The Aerospace Corporation's SPARTA framework, first released in October 2022, catalogues tactics and techniques against spacecraft. It includes attacks shown only in laboratories, because real ones are rarely reported. Defenders use it to plan detections and countermeasures. Two warnings apply to learned defences. They can be evaded by attackers who mimic normal behaviour or slowly poison the training data. And the learning systems — models, training pipelines and assistants — become new targets (Chapter 53).

::: note
**Practice: deploying an anomaly-detection system in a control centre**

1. **Start from the operators' needs.** Agree which subsystems matter most, what a useful alert looks like and how many alerts a day the team can handle — for example, 10. This budget sets every threshold.
2. **Assemble the data.** Collect several years of telemetry, command logs, timelines and anomaly reports. Label known anomalies and rare nominal events, such as manoeuvres and calibrations, with the engineers who saw them.
3. **Keep the baseline.** Keep limit checks running unchanged. The learned system adds alerts; it does not remove existing protection.
4. **Choose simple models first.** Start with per-channel prediction residuals and a nearest-neighbour or isolation-forest score, using orbit phase and commanded modes as inputs. Try deep networks only if they clearly do better on held-out data.
5. **Test like an operator.** Use a time-ordered split with a full year of test data. Score detected events, alerts per day and warning time, not just sample accuracy (ESA-ADB is a good template).
6. **Run in shadow mode.** Run the system beside normal operations for several months without paging anyone. Review every alert with the engineers and record whether it was useful.
7. **Explain each alert.** Show the channels involved, the expected and measured values, and similar past cases. Engineers will not act on a bare score.
8. **Plan for change.** Mark planned events so that they are not flagged, retrain after configuration changes and season shifts, and track alert precision every month.
9. **Go live gradually.** Start with one subsystem during working hours, with a named owner and a way to suppress or tune noisy detectors. Write down what the system does not cover.
:::

## Summary

Mission operations are moving from a few people watching every parameter of one spacecraft to small teams supervising fleets through software. Machine learning earns its place where rules are hard to write: telling unusual behaviour from normal, predicting wear-out, ranking alarms, finding documents and choosing waveforms. Optimisation does most of the scheduling. Classical algorithms still route most traffic. Across all of them, the hardest problems are false alarms, trust and verification, not raw accuracy. Chapter 50 applies similar methods to space situational awareness and defence, and Chapter 53 to their assurance.

::: key
**Key takeaways**

- Modern spacecraft produce tens of thousands of telemetry parameters (JWST about 40 000, Sentinel-3 about 46 000), and constellations fly hundreds to thousands of satellites. Operations are moving to automation and management by exception.
- The false-alarm budget drives every monitor: 10 000 channels checked every 10 s need fewer than about 1.2 × 10⁻⁷ false alarms per check to stay below 10 a day.
- Learned detectors that use context — orbit phase, mode and other channels — catch contextual anomalies and drifts that fixed limits miss. Generic detectors can do worse than limits, and real benchmarks such as ESA-ADB remain hard.
- Prognosis needs a physical degradation model, honest uncertainty and data from the vehicle itself. Predictions tighten as data accumulate.
- Language-model assistants are useful for search and drafting when grounded in controlled documents. Natural-language commanding is research and needs strict validation, simulation and human approval.
- Contact scheduling is an optimisation problem: in this chapter's example a mixed-integer programme delivered 81.6 % of waiting data, against 69.8 % for first-come scheduling, and served every satellite fairly.
- In communications, ACM roughly doubles Ka-band throughput over fixed coding. Learning helps most where decisions are made well ahead. Laser meshes route around many failures with classical shortest-path algorithms. Ground segments remain the main cyber target.
:::

::: questions
**Review questions**

1. A satellite has 4 000 channels sampled every 2 s. How many checks are made per day? What per-check false-alarm probability allows 5 false alarms a day, and what Gaussian threshold does that correspond to?
2. Explain the difference between point, contextual and drift anomalies, with one spacecraft example of each. Which kind can fixed limits never detect, and why?
3. Write the standardised residual used by a prediction-based detector. Why did the predictive network in @fig:tmanomalies detect a value copied from another part of the orbit, while the fixed limits did not?
4. Why did the isolation forest in @fig:tmroc miss spikes that left the normal range? What would you change in its inputs or in the system around it?
5. ESA-ADB scores detectors event by event and puts precision first. Why is this closer to operators' needs than sample-by-sample accuracy? What made Mission 2 hard?
6. In @fig:batteryrul, why is the 90 % interval for the end-of-life date much wider at 2.5 years than at 4.5 years? What would happen to the intervals if the model form were wrong?
7. List four risks of a language-model assistant in a control centre, and a defence against each. Why should such an assistant not send commands directly?
8. State the decision variables, constraints and objective of the contact-scheduling MILP. Why did first-come, first-served scheduling leave nine satellites below half their data?
9. A Ka-band link has a clear-sky Es/N0 of 16 dB and must tolerate a 9.4 dB fade. Using the DVB-S2 thresholds in this chapter, compare the spectral efficiency of fixed coding with that of ACM in clear sky. Why does a learned margin help more when decisions use 5-minute-old data than 30-second-old data?
10. In a laser mesh, why does the delay between London and New York change little when 30 % of links fail, yet rise sharply near 50 %? Give two ways in which learning could improve routing beyond shortest paths.
:::
