---
title: AI for Space Situational Awareness, Defence and Security
hero: ch50
abstract: More than 35 000 objects are catalogued in Earth orbit, and the number of close approaches grows with the square of that number. This chapter shows where machine learning and optimisation help to keep track of it all, and where they do not. It covers streak detection, data association, orbit prediction with learned corrections, storm-time drag, conjunction screening and triage, manoeuvre detection, light-curve characterisation and re-entry. It then turns, from open sources only, to defence and intelligence uses — imagery exploitation, tip-and-cue, emitter recognition, missile tracking, battle management, proximity operations, deception and human–machine teaming — and ends with the law, policy and stability questions they raise. Small models run in Python make each method concrete.
---

Space situational awareness (SSA) means knowing what is in orbit, where it is going and what it is doing. The hero image above shows an older side of the job. Engineers of NASA's Orbital Debris Program Office are recording impact craters on a Hubble camera that astronauts brought home in 2009. Every crater is a small piece of evidence about the debris population. Today the evidence arrives as millions of radar and telescope observations a day. Software must turn them into orbits, warnings and decisions for more than fifteen thousand active satellites.

That software increasingly includes machine learning (ML) — models that learn patterns from examples rather than following hand-written rules. The same methods also serve defence and intelligence. They sift satellite images for change, fuse signals from many sensors and point the next satellite at the right place. This chapter explains both uses. It separates what is operational, what has been demonstrated and what is still research, as of October 2026. Defence topics are covered from open sources only and without operational detail.

The chapter builds on the engineering background of Chapter 21 (SSA and debris), Chapters 19 and 20 (national-security space and missile warning) and Chapter 22 (space weather). Learning methods are introduced in Chapters 43 and 44, data and onboard computing in Chapter 45 and imagery analysis in Chapter 46. Autonomy for rendezvous is covered in Chapter 48 and the assurance of AI in Chapter 53.

## Space Situational Awareness at Machine Scale

The key idea of this section is that SSA is a pipeline, from raw sensor data to decisions. Physics does most of the work. Learning helps at a few points where the data are messy, the volume is large or the physics is uncertain.

### From Sensors to Decisions

@fig:ssapipeline50 shows the chain. **Sensors** — radars, telescopes, space-based cameras and commercial networks (Chapter 21) — produce raw data. **Detection** finds objects in that data. **Association** decides which known object each detection belongs to. Detections that match nothing are called **uncorrelated tracks** (UCTs). **Orbit determination** fits an orbit to each object's observations and predicts where it will go. The results form the **catalogue**. In October 2026 the public catalogue held about 35 000 objects in orbit, of which about 17 000 were working satellites.

From the catalogue, **screening** finds every close approach in the next few days. **Risk triage** decides which of them matter. Operators then **decide** whether to manoeuvre and **coordinate** with each other. Alongside this runs **behaviour analysis**: spotting manoeuvres and break-ups and learning what each object is.

Most of this pipeline is classical. Orbit determination uses least-squares fits and Kalman filters (Chapter 43), and screening uses geometry. The US Space Force declared its new catalogue software, ATLAS, operational in September 2025. It is replacing a system that dates from the 1980s. Its Unified Data Library pools government and commercial sensor data, and its 2025 Data and AI Strategic Action Plan names space domain awareness as a main focus for AI. @tbl:ssatasks50 summarises where learning fits.

![The space situational awareness pipeline. The data path (top) turns sensor data into a catalogue; the services path (bottom) turns the catalogue into warnings and decisions. Tags give the status in 2026 of machine learning at each step.](figures/out/ch50_pipeline.svg){#fig:ssapipeline50 width=96%}

| Task | Classical method | Where learning helps | Status (2026) |
|:---|:---|:---|:---|
| Detecting objects in images | Matched filters, stacking | CNN detectors for streaks and faint objects | Research; first pipelines |
| Associating detections | Gating and global assignment | Learned similarity after break-ups | Research |
| Predicting orbits | Numerical propagation, fitted drag | Learned corrections of prediction errors | Research |
| Thermospheric density | Empirical and data-assimilating models | Fast surrogates with uncertainty | Research |
| Conjunction triage | Probability of collision thresholds | Ranking events from CDM histories | Research; pilots |
| Manoeuvre detection | Residual tests, CUSUM | Classifiers on orbit histories | Commercial services |
| Characterisation | Expert reading of light curves | Classifiers of light curves | Research; commercial |
| Radar tasking | Fixed schedules and priorities | Learned detection probability | Commercial (vendor-reported) |

: Space situational awareness tasks, their classical methods and the places where machine learning helps. {#tbl:ssatasks50}

### Finding Faint Streaks

A satellite moves across the sky while a telescope tracks the stars. In a long exposure it therefore appears as a **streak**, not a point. A faint streak spreads its light over many pixels, so no single pixel stands out from the noise. The classic answer is the **matched filter**: correlate the image with a template shaped like the expected streak. For white noise this is the best linear detector.

Suppose the template $s_i$ matches the signal and the noise has standard deviation $\sigma$ per pixel. The filter output then has a signal-to-noise ratio of

$$ \mathrm{SNR}_{\mathrm{MF}} = \frac{\sqrt{\sum_i s_i^2}}{\sigma} \approx \frac{A}{\sigma}\sqrt{\sqrt{\pi}\,\sigma_{\mathrm{psf}}\,L}, $$

Here $A$ is the peak brightness along the streak, $L$ its length and $\sigma_{\mathrm{psf}}$ the width of the blur. A long streak therefore collects signal from many pixels. The catch is that the direction and length are unknown. The filter must be applied at many angles and positions, and each extra trial adds chances for a false alarm.

@fig:streak50 shows this on a synthetic star field. A 64-pixel streak whose peak is only 0.55 times the noise is invisible to the eye. After bright stars are masked, the matched filter finds it at 7.3σ. In the Monte Carlo test, at the same rate of 0.1 false alarm per frame, the matched filter detected half of the streaks at a peak signal of 0.34σ. A point-source detector needed 0.62σ, so the streak filter reached objects about 1.8 times fainter.

![Streak detection by matched filtering. (a) Synthetic frame with stars and a faint streak (circle). (b) Matched-filter output, maximum over 36 angles, after masking stars. (c) Detection probability against the streak's peak signal-to-noise ratio per pixel, for a point-source filter and a line matched filter at 0.1 false alarm per frame.](figures/out/ch50_streak.svg){#fig:streak50 width=98%}

Learning enters in two ways. Convolutional networks (CNNs, Chapter 44) can be trained on real frames to find streaks of any shape while ignoring satellite trails, cosmic rays and stars. A 2026 study trained an object detector on 2 335 telescope images and reported 94 % precision and 97 % recall. Networks also help with **synthetic tracking**: shifting and adding many short frames along trial velocities, so that faint objects build up while noise averages out. Both are in research use and in some commercial pipelines. Matched filtering and stacking remain the operational workhorses.

Moving-object detection is older than satellites. Asteroid surveys find objects by their motion against the stars, as in @fig:neo2018la. The same software problems — faint signals, many trials and false alarms — run through both fields.

![Discovery images of asteroid 2018 LA, taken by the Catalina Sky Survey on 2 June 2018. The small object (circled) moves between frames against fixed stars. It entered the atmosphere over Botswana about eight hours later.](figures/photos/ch50_2018la.jpg){#fig:neo2018la width=48%}

### Association and Uncorrelated Tracks

Each new detection must be linked to a catalogue object. The usual measure is the **Mahalanobis distance** between the detection $\mathbf{z}$ and the predicted position $\hat{\mathbf{z}}$:

$$ d^2 = (\mathbf{z}-\hat{\mathbf{z}})^{\mathsf T}\,\mathbf{S}^{-1}\,(\mathbf{z}-\hat{\mathbf{z}}), $$

where $\mathbf{S}$ is the combined covariance of prediction and measurement. It measures distance in units of uncertainty. A **gate** rejects pairs with $d^2$ above a threshold, such as 13.8 for 99.9 % confidence in two dimensions.

Association is easy when objects are far apart. It is hard after a launch that releases dozens of satellites together, or after a break-up. Then many predictions overlap and a greedy rule — give each object its nearest detection — makes chains of mistakes. **Global assignment** instead chooses all links at once to minimise the total cost $\sum_{ij} c_{ij}x_{ij}$, where $x_{ij}=1$ links object $i$ to detection $j$. The Hungarian method solves this exactly.

@fig:assoc50 tests both rules on a synthetic radar pass over a cluster of 24 objects. When the spacing was twice the prediction error, global assignment linked 76 % of objects correctly and the greedy rule 47 %. Both reach about 98 % when the objects are eight errors apart. Detections that match nothing become UCTs. They may be new fragments, unknown objects or simply wrong associations — so each UCT costs analyst time.

Learning helps by improving the inputs. Better predictions shrink the ellipses, and learned similarity — from brightness, radar cross-section or radio signatures — separates objects that geometry alone cannot. Research also uses multi-target trackers that keep several hypotheses alive until new data resolve them.

![Data association after a cluster deployment. (a) One synthetic pass: predicted positions with 2σ ellipses, detections, global-assignment links (green right, red wrong) and unmatched detections (UCTs). (b) Share of objects correctly associated against the ratio of spacing to prediction error.](figures/out/ch50_assoc.svg){#fig:assoc50 width=98%}

### Orbit Prediction: Physics Plus Learning

In low Earth orbit (LEO), the largest error in an orbit prediction is usually drag. Drag lowers the semi-major axis $a$ at a rate $\dot a = -\rho B\sqrt{\mu a}$, where $\rho$ is air density, $B$ the ballistic coefficient ($C_D A/m$) and $\mu$ Earth's gravitational parameter. A lower orbit is faster, so a density error makes the object run ahead of or behind its prediction. For a fractional density error $\varepsilon$, the along-track error grows with the square of time:

$$ \Delta s(t) \approx \tfrac{3}{4}\, n\, \varepsilon\, |\dot a|\, t^2, $$

where $n$ is the mean motion. At 450 km, with $|\dot a|$ = 50 m/day and $n$ ≈ 96.6 rad/day, a 20 % density error gives about 0.7 km after one day and 6.5 km after three. This quadratic growth is why conjunction warnings beyond a few days are unreliable.

Operators fight it by fitting a drag scale factor to recent tracking data. Learning adds a **hybrid** step. A physics propagator makes the prediction. A learned model $g_\theta$ predicts the propagator's typical error, which is then removed.

$$ \hat{\mathbf{x}}(t) = \mathbf{f}_{\mathrm{phys}}(\mathbf{x}_0, t) + g_\theta(\text{features}). $$

The features include the forecast horizon, altitude, space-weather indices and the errors the propagator made in the recent past. Peng and Bai (2018) showed the idea with neural networks, support vector machines and Gaussian processes on a simulated catalogue. The physics keeps the prediction sensible; the learned part corrects patterns that the physics misses.

@fig:drag50 runs this on 160 synthetic objects over a 240-day record with storms. Fitting the drag scale to 48 hours of data halved the median three-day error, from 3.2 km to 1.75 km. A small neural network on top did not help on average: its median three-day error was 1.98 km. But in the days after storms it cut the median one-day error from 0.75 km to 0.24 km. The lesson is general. A learned correction must be tested separately in the conditions that matter, because a gain in one regime can hide a loss in another.

![Storm-time drag and a hybrid correction. (a) Synthetic Ap index (top) and density at 450 km relative to quiet conditions: truth with a lagged storm response and an empirical model with a weaker, unlagged response. (b) Median along-track error against forecast horizon for three predictors, for all test epochs (solid) and for epochs just after storms (dashed).](figures/out/ch50_drag.svg){#fig:drag50 width=98%}

### Density and Drag During Storms

Geomagnetic storms heat the thermosphere and can multiply density at satellite heights several times (Chapter 22). Empirical models such as NRLMSIS and JB2008 capture average behaviour. The US Space Force's High Accuracy Satellite Drag Model (HASDM) goes further: it adjusts density every few hours from the observed drag of dozens of calibration objects. Learning offers fast **surrogates** of such models. Licata, Mehta and colleagues compressed 20 years of HASDM density maps with principal component analysis and trained a network on the result. Their model reproduced the database with about 10 % error and gave calibrated uncertainty, even during storms. Such models are in research use; operational density still comes from physics and data assimilation.

::: data
**The May 2024 storm and the catalogue**

- **Strength.** The storm of 10–11 May 2024 was the strongest in two decades, with the planetary ap index reaching 400.
- **Density.** Model density at 400 km rose to about six times its value 12 hours before.
- **Forecasts.** The 0–3-day ap forecasts underestimated the rise by 100–300.
- **Decay.** One Earth-observation satellite's decay rate jumped from 38 m to 180 m per day.
- **Operators.** Before the storm about 300 of nearly 10 000 active LEO satellites were manoeuvring. Afterwards thousands manoeuvred together — nearly half of all active LEO satellites, mostly Starlink.
- **Consequence.** Mass manoeuvres invalidate the conjunctions predicted for the coming week, so screening has to restart from new orbits.

Source: Parker and Linares, Journal of Spacecraft and Rockets (2024), from public two-line element data.
:::

## Conjunction Assessment and Space Traffic

The key idea of this section is a funnel. Billions of possible pairs shrink to thousands of close approaches a day and then to a handful of decisions. Computing handles the first steps easily. The hard part is deciding which few events deserve a manoeuvre.

### Screening at Scale

A catalogue of $N$ objects has $N(N-1)/2$ pairs. Screening programs do not test every pair at every moment. They first apply cheap **filters**. The **apogee–perigee filter** drops pairs whose altitude ranges do not overlap. Orbit-path and time filters then drop pairs whose orbits never come close, or whose closest points are never reached at the same time.

@fig:screen50 shows the result for a synthetic catalogue shaped like today's. The apogee–perigee filter keeps about 21 % of pairs, because most objects crowd into LEO. The number of real close approaches is far smaller. A kinetic-gas estimate — treating objects as molecules in shells of the atmosphere — gives about 1 400 pairs within 1 km per day for 35 000 objects. Pairs inside one constellation are left out, because their orbits are designed to keep apart. Every count grows as $N^2$. Doubling the catalogue, for example by tracking smaller debris, quadruples the work.

![Conjunction-screening workload. (a) Pairs per screening run and close approaches per day against catalogue size, for a synthetic catalogue shaped like the 2026 public one. (b) The screening funnel for 50 000 objects.](figures/out/ch50_screening.svg){#fig:screen50 width=98%}

::: example
**Example: daily screening workload for a 50 000-object catalogue**

The numbers come from the synthetic catalogue of @fig:screen50.

1. **Pairs.** $N(N-1)/2 = 50\,000 \times 49\,999/2 = 1.25 \times 10^9$ pairs.
2. **Filter.** The apogee–perigee filter (±10 km) keeps 21.3 %, or $2.67 \times 10^8$ pairs.
3. **Brute-force check.** Testing each surviving pair every minute for seven days takes $2.67\times10^8 \times 10\,080 = 2.7\times10^{12}$ distance checks. At $10^9$ checks per second, that is 45 minutes on one processor core, or 27 seconds on 100 cores. Computing is not the bottleneck.
4. **Close approaches.** The kinetic-gas estimate gives about 72 700 pairs within 5 km and 2 900 within 1 km each day — about a million a year within 1 km.
5. **People.** Suppose 1 % of the 1 km events needed an analyst for two hours. That would be 29 reviews and 58 hours a day — about 12 full-time analysts at 1 800 working hours a year.

This is why triage — choosing which events deserve people — matters more than raw computing speed.
:::

### Triage: Which Events Matter?

For each close approach, a **conjunction data message** (CDM) gives the predicted miss and the uncertainty of both objects (Chapter 21). The **probability of collision** $P_c$ is the chance that the true miss is smaller than the combined hard-body radius $R$. For a round uncertainty of standard deviation $\sigma$ in the encounter plane and $R \ll \sigma$,

$$ P_c \approx \frac{R^2}{2\sigma^2}\exp\!\left(-\frac{d^2}{2\sigma^2}\right), $$

where $d$ is the predicted miss distance. For a fixed miss distance, $P_c$ peaks at $R^2/(e\,d^2)$ when $\sigma = d/\sqrt2$. With larger uncertainty, $P_c$ falls again. This is **dilution**: a poorly tracked object looks safe because nobody knows where it is.

Each event produces a series of CDMs, typically about three a day for a week. The uncertainty shrinks as tracking accumulates, so $P_c$ jumps around (@fig:triage50). Operators usually decide about two days before the closest approach, the last moment for a cheap manoeuvre. The question for learning is whether the history of an event's CDMs predicts its final risk better than the latest value alone.

::: history
**The Kelvins collision-avoidance challenge (2019)**

In 2019 ESA ran a two-month machine-learning competition on its Kelvins platform. ESA's Space Debris Office released a database of 15 321 conjunction events and 199 082 CDMs, collected in 2015–2019 for its satellites. The data became public in October 2019. Each CDM had 103 attributes. Only 30 events had a final risk of 10⁻⁴ or more. Teams had to predict the final risk from CDMs available two days before closest approach.

Ninety-six teams made 862 submissions. The main result surprised many: the **naive forecast** — the latest known risk — was very hard to beat. Later tests with gradient-boosted trees beat it by about 1.3 % in the F2 score, a small but statistically clear gain. The organisers concluded that naive forecasts are an "unavoidable benchmark" for any future method (Uriot et al., 2022).
:::

@fig:triage50 repeats the experiment on 40 000 synthetic events. Each has a true miss within 3 km, a hard-body radius of 15 m, shrinking and partly wrong covariances, and missing CDMs. An event counts as high risk if its final $P_c$ is at least 10⁻⁵. Ranking events by their latest $P_c$ at two days and flagging the top 40 per 1 000 caught 39 % of the high-risk ones. Gradient-boosted trees using the whole CDM history caught 46 %. The common rule "latest $P_c \ge 10^{-4}$" flagged 48 events per 1 000 and caught 45 %; the trees caught 51 % with the same number of alerts. The gain is real but modest, as in the Kelvins challenge. No method can recover information that the tracking data do not contain.

![Conjunction triage on synthetic CDM sequences. (a) Probability of collision against time to closest approach for example events. (b) Share of final high-risk events caught against the number of events flagged per 1 000, for ranking by the latest Pc and for gradient-boosted trees.](figures/out/ch50_triage.svg){#fig:triage50 width=98%}

The last resort, when warning comes too late to manoeuvre, is to protect the people. On 24 March 2012 the six crew members of the International Space Station took shelter in their two Soyuz spacecraft as a debris fragment passed close by (@fig:issshelter2012).

![Expedition 30 crew members in the ISS Zvezda module on 24 March 2012, preparing to shelter in their Soyuz spacecraft because a piece of debris could pass close to the station.](figures/photos/ch50_shelter.jpg){#fig:issshelter2012 width=56%}

::: example
**Example: probability-of-collision thresholds and manoeuvre numbers**

A fleet of 1 000 satellites each has 300 close approaches a year with a miss distance inside $D$ = 5 km. Assume the true miss is spread evenly over that disc, the hard-body radius is $R$ = 5 m and the final uncertainty is $\sigma$ = 100 m.

1. **Risk without avoidance.** Each event has a collision chance of $R^2/D^2 = 10^{-6}$. The fleet expects $1\,000 \times 300 \times 10^{-6} = 0.3$ collisions a year.
2. **Trigger distance.** Setting $P_c$ equal to the threshold $P_{\mathrm{th}}$ gives $d_{\mathrm{th}} = \sigma\sqrt{2\ln\!\left(R^2/(2\sigma^2 P_{\mathrm{th}})\right)}$. For 10⁻⁴ this is 225 m.
3. **Manoeuvres.** The share of events inside $d_{\mathrm{th}}$ is $(d_{\mathrm{th}}/D)^2 = 2.0\times10^{-3}$. That is 0.61 manoeuvres per satellite per year, or 606 for the fleet.
4. **Residual risk.** The risk left in events below the threshold is $2\sigma^2 P_{\mathrm{th}}/R^2$ = 8 % of the total. A threshold of 10⁻⁴ thus removes 92 % of the risk; 10⁻⁵ removes 99.2 % for 1.16 manoeuvres per satellite per year.
5. **Poor tracking.** With $\sigma$ = 500 m the largest possible $P_c$ is $5\times10^{-5}$. A 10⁻⁴ threshold then never triggers, although the true risk is unchanged. A threshold of 3 × 10⁻⁷ removes 99.4 % of the risk but needs 31 manoeuvres per satellite per year.

Better tracking reduces manoeuvres more than any threshold rule can (@tbl:pcthreshold50).
:::

| Threshold $P_{\mathrm{th}}$ | Trigger miss, σ = 100 m | Manoeuvres per satellite-year | Risk removed | Manoeuvres per satellite-year, σ = 500 m | Risk removed, σ = 500 m |
|---:|---:|---:|---:|---:|---:|
| 10⁻³ | 67 m | 0.05 | 20 % | never triggers | 0 % |
| 10⁻⁴ | 225 m | 0.61 | 92 % | never triggers | 0 % |
| 10⁻⁵ | 311 m | 1.16 | 99.2 % | 9.7 | 80 % |
| 3 × 10⁻⁷ | 408 m | 2.0 | 99.98 % | 30.7 | 99.4 % |

: Manoeuvre numbers and risk removed for different collision-probability thresholds, from the worked example (300 events a year within 5 km, hard-body radius 5 m). {#tbl:pcthreshold50}

### Automated Decisions and Coordination

At the largest scale, decisions are already automatic. Starlink satellites receive warnings and plan and execute their own avoidance manoeuvres. They made more than 200 000 such manoeuvres in the six months to May 2026, at a threshold of 3 × 10⁻⁷ (Chapter 48). This is rule-based autonomy rather than learning, and it works because the operator controls both the rules and the satellites. The weak point is data. Most of Starlink's reported misses came from poor or late predictions of the other object.

Coordination between operators is the next step. ESA's **CREAM** project (Collision Risk Estimation and Automated Mitigation), begun in 2020, aims to cut operator workload, false alerts and response time. In August 2025 its ground prototype, built by GMV and Guardtime, could issue alerts, propose manoeuvres and support coordination. ESA was preparing a pilot phase and in-orbit demonstrations, first as a software payload on other satellites. @tbl:ssasystems50 lists the main systems and their status.

In the USA, civil conjunction services are moving from the military to the Office of Space Commerce's **TraCSS**. In July 2026 it was still a pilot, with 62 users covering more than 11 000 satellites. Congress funded the office at $52.5 million for 2026, but the 2027 budget request did not mention TraCSS. Europe's EU SST protected more than 700 satellites in 2026. It reported 15 639 close approaches in 2023, of which about 1 000 were high risk.

| System | Operator | What it does | Status (October 2026) |
|:---|:---|:---|:---|
| ATLAS and Space-Track | US Space Force | Catalogue processing; public data and CDMs | Operational (ATLAS from Sept. 2025) |
| TraCSS | US Office of Space Commerce | Civil conjunction service | Pilot: 62 users, >11 000 satellites (July 2026); funding contested |
| EU SST | EU Space Surveillance and Tracking | Collision avoidance, re-entry, fragmentation services | Operational; >700 satellites protected |
| CREAM | ESA with GMV and Guardtime | Automated risk assessment, manoeuvre design, coordination | Ground prototype; pilots and in-orbit demonstration in preparation |
| Starlink onboard avoidance | SpaceX | Autonomous screening response and manoeuvres | Operational |
| LeoLabs services | LeoLabs | Radar catalogue; ML manoeuvre, break-up and behaviour detection | Commercial (vendor-reported) |
| Agatha | Slingshot Aerospace for DARPA | Flags outlier satellites in constellations | Research and development (2023–24) |

: Selected conjunction, coordination and behaviour-analysis systems. Sources: operators' and agencies' public statements. {#tbl:ssasystems50}

## Watching Behaviour: Manoeuvres, Characterisation and Re-entry

The key idea of this section is that a catalogue must know not only where objects are but how they behave. Has a satellite moved? Is it tumbling? Will it re-enter soon? Learning is most useful here, because behaviour leaves subtle patterns in long data histories.

### Manoeuvre Detection

A manoeuvre is a sudden change in velocity. A burn of 1 cm/s along the track of a LEO satellite raises its semi-major axis by about 18 m. That is less than the noise in a single orbit estimate, and drag changes keep blurring the picture. Yet missed manoeuvres corrupt predictions, and unexplained ones may signal intent.

The classical tool is the **cumulative sum** (CUSUM) test. A short-term model predicts the next estimate. The standardised residual $r_k$ feeds two running sums,

$$ S_k^{\pm} = \max\!\left(0,\; S_{k-1}^{\pm} \pm r_k - \kappa\right), $$

which raise an alarm when either exceeds a threshold $h$. The allowance $\kappa$ absorbs normal noise. A step change pushes one sum steadily upward, so CUSUM detects small persistent shifts that a single-point test would miss.

A learned classifier instead looks at a whole window of data around each moment. It learns what a burn looks like compared with a storm or an outlier. @fig:maneuver50 compares the two on 240 synthetic satellites. Each has 60 days of orbit estimates every six hours, drag that rises in storms and burns of 15–150 m. At one false alarm per satellite per month, a tuned CUSUM found 39 % of burns within two days and gradient-boosted trees found 49 %. At 0.3 false alarms the gap widened to 22 % against 43 %. Both found nearly all the large burns. The small ones, below about two noise widths, stayed hard.

![Manoeuvre detection in noisy orbit estimates. (a) One synthetic satellite: semi-major axis minus its smooth decay, with burns (green dashed lines), the CUSUM statistic and the classifier score. (b) Share of burns detected within two days against false alarms per satellite per month.](figures/out/ch50_maneuver.svg){#fig:maneuver50 width=98%}

Commercial providers now sell such detection. LeoLabs says it uses machine learning to detect manoeuvres in real time, score unusual "patterns of life" across its catalogue and spot new objects from deployments or break-ups. It also reports that learned radar scheduling lets it track objects 40 % more often. These are vendor claims without independent evaluation. Slingshot Aerospace's **Agatha**, built for the US Defense Advanced Research Projects Agency (DARPA) from 2023, takes a different route. It was trained on simulated constellations and uses **inverse reinforcement learning** — inferring goals from observed behaviour — to flag satellites that act unlike their neighbours.

Behaviour analysis matters most in geostationary orbit, where inspector satellites manoeuvre near others. In mid-2025 China's Shijian-21 and Shijian-25 appear to have docked in GEO, probably to test refuelling, and separated in late 2025. China did not confirm the operation. Commercial trackers such as COMSPOC and S2a followed it from the ground, and the US Space Force reportedly watched with its GSSAP inspector satellites.

### Characterising Objects from Light Curves

A **light curve** is an object's brightness over time. A stable, pointed satellite shines steadily. A tumbling rocket body brightens twice per turn as its long side faces the observer. A tumbling panel flashes when its flat surface briefly acts as a mirror. Period, amplitude and shape thus reveal what an object is and how it moves.

A good starting point is a set of physical **features**. The **Lomb–Scargle periodogram** finds the strongest period in unevenly sampled data. Skewness and the share of bright outliers measure flashes. The autocorrelation at the best period tests whether the pattern repeats. A classifier then learns from labelled examples.

@fig:lightcurve50 tests this on synthetic two-minute light curves of three classes. A random forest on nine features was 96–97 % accurate up to 0.1 magnitude of noise and 84 % at 0.3 magnitude. The most useful features were periodogram power, skewness and autocorrelation. A rule using amplitude alone managed only 53–59 %. Real studies report similar trends. Classifiers trained on light curves from Russia's Mini-MegaTORTORA wide-field camera reach about 75 % for three broad classes and 85–92 % for some finer tasks. Results differ with the class definitions, so the 2024 RoBo6 data set was released as a common benchmark.

![Light-curve classification. (a) Synthetic light curves of a stable satellite, a tumbling cylinder and a tumbling panel. (b) Accuracy against photometric noise for a random forest on nine features and for a rule using amplitude alone. (c) Confusion matrix of the forest at 0.3 magnitude noise.](figures/out/ch50_lightcurve.svg){#fig:lightcurve50 width=98%}

Radar adds a second view. **Radar cross-section** — how strongly an object reflects radio waves — varies with size, shape and attitude. Imaging radars such as Germany's TIRA can make pictures of satellites, which networks can help interpret. Characterisation feeds association, because two objects with different light curves are unlikely to be the same. It also feeds risk, because a tumbling derelict cannot manoeuvre.

### Re-entry Prediction

About 2 000 catalogued objects re-enter each year (Chapter 21). Predicting when an uncontrolled object will re-enter is hard because the final days are dominated by drag at low altitude, where density is least certain. A common rule of thumb is an uncertainty of about 10–20 % of the remaining lifetime. A prediction made a day ahead is therefore uncertain by a few hours, or tens of thousands of kilometres along the track.

Learning has been tried here too. Salmaso, Trisolini and Colombo (2023) trained a sequence-to-sequence network on the altitude histories of more than 400 re-entered objects, adding the drag term, solar activity and area-to-mass ratio as inputs. It worked best for objects similar to its training set, a familiar limit of learned models. Controlled re-entries avoid the problem, as for ESA's ATV-3 in 2012 (@fig:atv3reentry).

![The destructive re-entry of ESA's Automated Transfer Vehicle-3 (Edoardo Amaldi) over the South Pacific on 3 October 2012, photographed from the International Space Station. The re-entry was controlled, so the time and place were known in advance.](figures/photos/ch50_atv3.jpg){#fig:atv3reentry width=56%}

## AI in Defence and Intelligence Space Systems

The key idea of this section is that defence uses of AI in space are mostly about **attention**. Sensors now collect far more than people can look at. Machines filter, flag and cue; people check, judge and decide. This section uses open sources only. It describes what governments and companies have said publicly, without operational detail.

### Imagery Exploitation at National Scale

Satellite imagery has shaped wars since the first reconnaissance satellites (Chapter 19). In 1991 Space Shuttle crews photographed the Kuwaiti oil fires set during the Gulf War (@fig:kuwaitfires). Today hundreds of commercial and government imaging satellites revisit most places several times a day. No analyst workforce could inspect all those images, so automated **object detection** and **change detection** (Chapter 46) now do the first pass.

![Smoke from burning oil wells north of Kuwait City, photographed from the Space Shuttle in April 1991 after the Gulf War. Space imagery has been part of conflict monitoring ever since.](figures/photos/ch50_kuwait.jpg){#fig:kuwaitfires width=34%}

::: history
**From Project Maven to NGA Maven**

- **2017.** The US Department of Defense set up an Algorithmic Warfare team, known as Project Maven, to apply computer vision to drone video and other imagery. It was operational by 2018.
- **2022.** Parts of Maven moved to the National Geospatial-Intelligence Agency (NGA), which handles imagery and maps.
- **November 2023.** NGA made NGA Maven a formal programme of record.
- **May 2025.** NGA's director reported more than 20 000 active users across more than 35 military tools, available to all services and combatant commands. Targeting timelines in one exercise fell "from hours to minutes". The ceiling of the related Maven Smart System contract rose to about $1.3 billion through 2029.
- **June 2025.** NGA began labelling intelligence products that are "100 percent machine-generated", with no human hand in the template or its release — the first of the 18 US intelligence agencies to do so routinely.

Sources: Breaking Defense and DefenseScoop reporting of NGA statements, 2025.
:::

NGA also buys analytics from industry. Its Luno A contract (September 2024, up to $290 million, ten companies) covers computer vision for monitoring infrastructure. Luno B (January 2025, about $200 million) covers wider analytics, including AI-based change detection.

At national scale the main enemy is the false alarm. Clouds, shadows, seasons and small misregistrations all look like change. @fig:changefa50 shows the arithmetic. A country of 500 000 km² divided into 30 m cells has 5.6 × 10⁸ cells per look. Even a tiny per-cell false-alarm rate produces more alerts than any team can read.

![False alarms of automated change detection at national scale. (a) False alerts per pass over 500 000 km² against the per-cell false-alarm probability, for three cell sizes, with the range a team can review in a day. (b) Share of alerts that are real changes for 30 m cells, for different numbers of real changes per pass, and with confirmation by a second independent look.](figures/out/ch50_changefa.svg){#fig:changefa50 width=98%}

::: example
**Example: false alarms in automated change detection over a country**

A detector screens 500 000 km² in 30 m cells after each pass. It finds 90 % of real changes and has a false-alarm probability of 10⁻⁴ per cell. There are 1 000 real changes per pass.

1. **Cells.** $500\,000\ \text{km}^2 / (30\ \text{m})^2 = 5.56 \times 10^8$ cells.
2. **False alerts.** $5.56 \times 10^8 \times 10^{-4} = 55\,556$ per pass.
3. **Real alerts.** $0.9 \times 1\,000 = 900$.
4. **Precision.** Only $900/(900 + 55\,556) = 1.6\ \%$ of alerts are real.
5. **Target.** For half of the alerts to be real, the false-alarm rate must fall to $900/5.56\times10^8 = 1.6 \times 10^{-6}$ per cell.
6. **Second look.** Confirming each alert with an independent second image squares the false-alarm rate to 10⁻⁸. False alerts drop to about 6, while detection falls to 81 %. Precision becomes 99.3 %.

Step 6 assumes independent errors. Real clutter repeats from image to image, so the gain is smaller in practice. This is why measured false-alarm rates, not textbook ones, must drive the design.
:::

### Activity-Based Intelligence and Tip-and-Cue

**Activity-based intelligence** looks for patterns of activity rather than single objects: ships that meet at sea, vehicles that gather before an exercise, a radar that switches on at unusual times. It needs data from many sources over long periods. Machine learning helps to build a picture of normal behaviour and flag departures from it.

**Tip-and-cue** turns such flags into new collection (@fig:tipcue50). A wide-area sensor, such as a radar satellite or a radio-frequency receiver, notices something. Software then tasks a high-resolution satellite or another sensor to look again. The US National Reconnaissance Office (NRO) has described its **Sentient** research programme as an automated tipping-and-cueing system. In 2025 it told Congress that its new constellations and ground systems will "fuse data across collection platforms" to automate tipping and cueing. By mid-2026 the NRO had made 14 launches of its proliferated LEO constellation and said it had hundreds of satellites in orbit.

![Tip-and-cue across constellations. Machine steps (blue) detect, fuse and cue new collection; human decision points (orange) review evidence and make decisions. An adversary (red) tries to deceive both sensors and models.](figures/out/ch50_tipcue.svg){#fig:tipcue50 width=94%}

Radar satellites are central to maritime monitoring because they see through cloud and darkness. In an early example from 1994, the Space Shuttle's imaging radar recorded a ship and its 28 km wake in the Atlantic (@fig:sirship).

![A Spaceborne Imaging Radar-C/X-SAR image of the north-east Atlantic taken from Space Shuttle Endeavour on 11 April 1994. The bright spot at left is a ship and the dark line its 28 km wake, probably lengthened by discharged oil. The area shown is about 35 km × 65 km.](figures/photos/ch50_sarship.jpg){#fig:sirship width=70%}

### Signals and Emitters

Radio receivers in orbit locate and classify emitters, such as radars, satellite phones and ship transponders (Chapter 19). Learning helps in two ways. **Signal classification** recognises the type of signal from its modulation (Chapter 49). **Specific emitter identification** goes further: it tells apart individual transmitters of the same type from tiny hardware imperfections, such as oscillator drift and amplifier distortion — a radio fingerprint.

Open research shows what is possible. In 2023 researchers at Oxford fingerprinted Iridium satellite transmitters from about 1.7 million recorded messages, using an autoencoder and a twin ("Siamese") network. Against messages replayed with a software-defined radio — a spoofing attack — the system had an equal error rate of 12 %. Commercial operators such as HawkEye 360 use clusters of satellites to geolocate signals and flag ships that switch off their identification beacons.

### Missile Warning and Tracking

Missile-warning satellites stare at the Earth in the infrared and must find a rocket plume among clouds, sun glints and fires (Chapter 20). Classical processing subtracts the background, applies thresholds and confirms detections by tracking them over several frames. Learning is being studied for clutter suppression, event classification and **track fusion** — combining detections from several satellites and radars into one three-dimensional track. The US Space Force accepted its new FORGE missile-warning ground processing for operations in September 2025. Public material says little about the use of learning in operational chains. Errors here could have grave consequences, so changes demand long testing.

### Battle Management and Golden Dome

Missile defence must turn tracks into decisions in minutes. **Battle management, command and control** (BMC2) software links sensors to interceptors and proposes which interceptor should engage which threat. The US **Golden Dome** programme, launched by executive order in January 2025, aims at a layered homeland defence that includes space sensors and possibly space-based interceptors.

Public facts are limited and changing. In April 2026 the Space Force gave 12 companies agreements worth up to $3.2 billion for space-based interceptor prototypes. Golden Dome's director, General Michael Guetlein, calls the command-and-control layer the programme's "glue layer". A consortium of nine firms demonstrated part of it in early 2026, and initial operational capability is planned for 2028. He put the cost at $185 billion through 2035. A Congressional Budget Office estimate in May 2026, for an illustrative architecture, put it at about $1.2 trillion over 20 years. In September 2026 Guetlein said that the military must decide "at machine speed". He saw a role for AI in helping leaders sift data and present options. How far humans stay in each decision has not been described in public detail.

### Autonomy for Rendezvous and Proximity Operations

Inspector satellites, servicers and possible weapons all fly close to other spacecraft. Their guidance and navigation methods are covered in Chapter 48. The defence angle is speed and secrecy. In June 2026 the Space Force's **Victus Haze** exercise launched a Rocket Lab spacecraft 16 hours and 42 minutes after the order to launch. It was to rendezvous with True Anomaly's Jackal spacecraft for several months of proximity operations. Such missions rely on onboard autonomy: the ground cannot react quickly enough when two satellites are tens of metres apart. They also stress SSA, because observers must decide quickly whether an approach is inspection, servicing or a threat (@tbl:defenceai50).

| Application | Example (public) | What the machine does | Status (October 2026) |
|:---|:---|:---|:---|
| Imagery exploitation | NGA Maven; NGA Luno contracts | Detects objects and change; drafts reports | Operational at scale |
| Tip-and-cue | NRO Sentient; proliferated constellation | Flags events; tasks other sensors | Described as operational in part; details classified |
| Emitter identification | SatIQ research; commercial RF constellations | Recognises signal types and individual transmitters | Research; commercial geolocation operational |
| Missile-warning processing | FORGE; SDA Tracking Layer | Rejects clutter; builds and fuses tracks | Operational processing; learning mostly research |
| Battle management | Golden Dome C2 consortium | Pairs threats with interceptors; presents options | In development; demonstrations 2026 |
| Proximity operations | Victus Haze; GSSAP; Shijian-21/25 | Guides approach; classifies others' approaches | Demonstrations and operations |

: Defence and intelligence uses of AI in space systems, from open sources. {#tbl:defenceai50}

### Deception and Counter-AI

Every detector invites an attempt to fool it. Classic **deception** uses decoys, camouflage and emission control. In 2023–24 analysts of commercial imagery found aircraft outlines painted on Russian airfields, including Tu-95 bomber shapes at Engels. The UK Ministry of Defence noted in 2024 that helicopters were still landing on the painted fighter outlines, which undermined the deception. Commercial imagery separated the paintings from real aircraft easily.

AI adds new targets. An **adversarial patch** is a printed pattern designed to make a neural network miss an object. A 2020 study showed that a patch covering about 10 % of an aircraft hid it from a common detector in aerial images, although only digitally. Training data can be poisoned, and models can be probed until they reveal their blind spots. Defences include training on adversarial examples, combining different sensors — a painted shape has no radar or heat signature — and keeping people in the review loop. Chapter 53 covers the security of AI in more depth.

### Human–Machine Teaming

Automation changes how people think. **Automation bias** is the tendency to accept a machine's suggestion without checking. Its opposite, **disuse**, follows when a system cries wolf too often. Good teaming gives each side what it does best. Machines sift volume and keep track of many objects. People bring context, scepticism and responsibility.

Three practices help. Systems should show their evidence and confidence, not just a verdict. Operators should train with systems that sometimes fail, so that they learn when to doubt them. And the design should state clearly who decides what. NGA's label for machine-generated products is one example of making the machine's role visible. Flight dynamics officers at NASA, who own trajectory decisions for crewed missions, offer another model of human authority supported by software (@fig:artemisfdo).

![Flight controller Julie Reed at the flight dynamics officer console in Mission Control, Houston, on 1 December 2022, as Orion left its distant retrograde orbit around the Moon during Artemis I. Software computes the trajectory options; a named person owns the decision.](figures/photos/ch50_fdo.jpg){#fig:artemisfdo width=40%}

## Law, Ethics and Policy

The key idea of this section is that existing law applies to AI, but states disagree on whether new rules are needed. Space adds special worries about stability, because satellites are fragile and hard to defend.

### Rules for Autonomy in Weapons

The main US policy is **Department of Defense Directive 3000.09**, "Autonomy in Weapon Systems", updated on 25 January 2023. It requires that systems let commanders and operators exercise "appropriate levels of human judgment over the use of force". Autonomous weapon systems need a senior-level review before formal development and again before fielding. The directive does not ban such weapons, and it does not require a human to approve every individual engagement. In June 2026 a presidential memorandum, NSPM-11, ordered an update of the directive within 90 days and a review every year. No revised text had been published by late October 2026.

### International Norms

The USA launched the **Political Declaration on Responsible Military Use of Artificial Intelligence and Autonomy** in February 2023 and revised it in November 2023. It is a non-binding set of commitments: legal reviews, human accountability, testing, and safeguards such as the ability to disengage systems that behave unexpectedly. Almost 60 states had endorsed it by late 2024. Other forums run in parallel (@tbl:aipolicy50).

| Instrument | Year | Type | Main content | Status (October 2026) |
|:---|:---|:---|:---|:---|
| DoD Directive 3000.09 | 2012; updated 2023 | US policy | Human judgement over force; senior reviews | In force; update ordered June 2026 |
| Political Declaration | 2023 | Non-binding, ~60 states | Responsible military AI practices | Endorsements open |
| NATO AI strategy | 2021; revised 2024 | Alliance policy | Six principles of responsible use; testing | In force |
| REAIM summits | 2023, 2024, 2026 | Multi-stakeholder | Blueprint (Seoul); "Pathways to Action" (A Coruña) | About 35 states endorsed 2026 text (reported) |
| UN General Assembly resolutions | 2023, 2024, 2025 | Non-binding | Concern about lethal autonomous weapons | Resolution 80/57: 164 for, 6 against |
| CCW expert group (GGE) | 2016–2026 | Treaty forum, consensus | Elements of a possible instrument | Consensus report Sept. 2026; Review Conference Nov. 2026 |

: Policy and legal instruments on military AI and autonomy. {#tbl:aipolicy50}

Under the Convention on Certain Conventional Weapons (CCW), with 128 states parties, a group of governmental experts has discussed **lethal autonomous weapon systems** since 2016. Its mandate ended in 2026. At its final session (31 August–4 September 2026) it agreed by consensus on elements that could form the basis of an instrument. The Seventh Review Conference, on 16–20 November 2026, will decide whether to open negotiations. The USA and Russia have opposed new legally binding rules. Many other states and the International Committee of the Red Cross want a treaty. NATO's revised 2024 strategy keeps its six principles: lawfulness, responsibility and accountability, explainability and traceability, reliability, governability and bias mitigation.

### Stability and Escalation in Space

AI could make space more stable or less. Better SSA helps: knowing quickly that a close approach is an accident, not an attack, reduces the risk of overreaction. Shared data and automated coordination make accidents less likely. But speed cuts both ways. If machines classify a manoeuvre as hostile within seconds, decision makers may feel pressure to respond before checking. Errors in one system can trigger responses in another, as in financial "flash crashes". And satellites that support nuclear command and early warning (Chapter 20) are especially sensitive. Misreading an attack on them could escalate a conflict quickly.

Common proposals include keeping human decision points for any action against a satellite, exchanging data on manoeuvres, testing systems against realistic deception, and agreeing norms against destructive anti-satellite tests (Chapter 19).

### Export Controls and Dual Use

Almost everything in this chapter is **dual-use**: the same tracker serves a commercial operator and an air force. Space hardware falls under export controls such as the US International Traffic in Arms Regulations and Export Administration Regulations, and the multilateral Wassenaar Arrangement. Advanced AI chips have been controlled since 2022. A US rule of January 2025 that would also have limited exports of AI chips and model weights to most countries was rescinded in May 2025, and no replacement had been issued by mid-2026. Engineers should expect rules on chips, models and SSA data to keep changing and should check them early in any international project.

## Lessons from the Experiments

@tbl:mlsummary50 collects the results of this chapter's experiments. All used synthetic data with fixed random seeds, so they illustrate methods rather than measure real systems.

| Task and condition | Baseline | Learned or optimised method | Result |
|:---|:---|:---|:---|
| Streak detection | Point-source filter | Line matched filter | 1.8× fainter |
| Association, spacing 2σ | Greedy nearest neighbour | Global assignment | 76 % vs 47 % |
| Drag after storms, one day | Fitted drag scale | Plus neural network | 0.24 vs 0.75 km |
| Triage, 40 alerts per 1 000 | Latest Pc | Boosted trees | 46 % vs 39 % |
| Manoeuvres, 1 false alarm a month | CUSUM | Boosted trees | 49 % vs 39 % |
| Light curves, 0.3 mag noise | Amplitude rule | Random forest | 84 % vs 59 % |

: Summary of this chapter's synthetic experiments. {#tbl:mlsummary50}

Four lessons stand out. Physics and geometry carry most of the load. Learning gives real but moderate gains, mostly where data are noisy or patterns are subtle. Gains must be measured in the conditions that matter, such as storms or low false-alarm rates. And no model can create information that the sensors did not collect.

::: note
**Practice: building a manoeuvre-detection pipeline**

1. **Define the need.** Decide which satellites to watch, the smallest burn that matters (for example 2 cm/s) and how quickly it must be found. Agree how many false alarms per day the analysts can handle.
2. **Gather data.** Collect orbit histories — two-line elements, ephemerides or your own orbit fits — with their uncertainties. Add space-weather indices, because storms mimic burns.
3. **Get labels.** Use operators' published manoeuvre histories, such as constellation ephemerides, or ask cooperating operators. Mark storms, deployments and orbit-raising phases separately.
4. **Build a baseline.** Fit a smooth decay model and run a CUSUM test on the residuals. Tune its window and allowance on training satellites only.
5. **Add a learned model.** Train a gradient-boosted classifier on windows of residuals and space-weather features. Split by satellite and by time, never at random, to avoid leakage (Chapter 43).
6. **Score like an operator.** Report the share of burns found within the required time at your false-alarm budget. Report results for small burns and storm periods separately.
7. **Estimate each burn.** For every alarm, fit the size, direction and time of the burn and its uncertainty. A flag without an estimate is of little use.
8. **Run in shadow mode.** Run beside existing tools for months. Review every alarm and missed burn with analysts.
9. **Monitor and retrain.** Track precision monthly. Retrain after new satellite types, new sensors or a change in solar activity.
10. **Share what you find.** Publish detected manoeuvres in a standard format, with their uncertainty, so that screening services and other operators can use them at once.

The same steps work for break-up detection and for change detection in imagery.
:::

::: key
**Key takeaways**

- About 35 000 objects are catalogued in orbit (October 2026). The number of close approaches grows with the square of that number: 50 000 objects make about 1.25 × 10⁹ pairs and thousands of approaches within 1 km a day.
- Most of the SSA pipeline is physics and geometry. Learning helps with faint detections, association, prediction errors, density during storms, triage, manoeuvre detection and characterisation — mostly in research or commercial services so far.
- Along-track errors grow with the square of time, so density errors dominate LEO predictions. Hybrid models that learn a correction to physics can help after storms but must be tested regime by regime.
- In conjunction triage the latest probability of collision is a strong baseline, as ESA's 2019 Kelvins challenge showed. Better tracking reduces manoeuvres more than any threshold rule, because poor tracking dilutes the probability.
- In defence, AI's main job is managing attention: NGA Maven had more than 20 000 users in 2025, and tip-and-cue links constellations. At national scale, false alarms set the limit — 10⁻⁴ per cell gives over 55 000 false alerts per pass over 500 000 km².
- Adversaries can deceive both sensors and models with decoys, camouflage and adversarial patterns. Fusing different sensors and keeping people in the review loop are the main defences.
- US policy requires "appropriate levels of human judgment over the use of force". International talks on autonomous weapons reached a consensus text in 2026, with the decision on negotiations due in November 2026.
:::

::: questions
**Review questions**

1. A 40-pixel streak has a peak brightness of 0.5σ per pixel and a blur of $\sigma_{\mathrm{psf}}$ = 1.5 px. Estimate its matched-filter signal-to-noise ratio. Why does searching over many angles reduce the real gain?
2. Explain the Mahalanobis distance and the role of a gate. Why does global assignment outperform the greedy rule in @fig:assoc50 when objects are close together?
3. Using $\Delta s \approx \tfrac34 n\varepsilon|\dot a|t^2$, estimate the along-track error after two days for a satellite at 450 km with $|\dot a|$ = 50 m/day and a 30 % density error.
4. In @fig:drag50 the neural-network correction helped after storms but not on average. Give two reasons, and say how you would test such a model before using it.
5. For a catalogue of 100 000 objects, how many pairs are there? By what factor does the number of daily close approaches change compared with 50 000 objects?
6. What is dilution in the probability of collision? Using the formula in this chapter, find the largest possible $P_c$ for a miss of 300 m and a hard-body radius of 10 m.
7. What did ESA's Kelvins challenge teach about machine learning for conjunction triage? Why is the latest risk such a strong baseline?
8. Compare CUSUM and a learned classifier for manoeuvre detection. Why do storms cause false alarms, and how can space-weather data reduce them?
9. A change detector screens 200 000 km² in 10 m cells with a false-alarm probability of 10⁻⁶ per cell. How many false alerts per pass does it make? What would confirmation by a second look achieve, and why is the real gain smaller?
10. Describe two ways AI in space systems could make a crisis more stable and two ways it could make it less stable. What human decision points would you keep?
:::
