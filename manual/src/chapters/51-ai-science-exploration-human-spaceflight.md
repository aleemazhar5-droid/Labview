---
title: AI for Space Science, Planetary Exploration and Human Spaceflight
hero: ch51
abstract: Space science now produces far more data than people can inspect. A survey telescope sends millions of alerts a night, and orbiters have imaged whole planets at metre scale. A crew on the way to Mars will be twenty minutes from help. This chapter shows how machine learning finds planets in light curves, classifies transients, maps galaxies and lenses, estimates redshifts and speeds up gravitational-wave analysis. It then turns to craters, boulders and minerals on other worlds, to science autonomy on rovers, and to AI for crew health, assistants, robots, smart habitats and Earth-independent operations. Small experiments, run from scratch, show what each method does and where it fails. Status is given as of October 2026.
---

Science missions are built to collect data. For most of the space age, people could look at all of it. Astronomers inspected every photographic plate, and planetary geologists mapped every image by hand. That is no longer possible. Kepler watched about 200 000 stars every 30 minutes for four years. The Vera C. Rubin Observatory now sends up to several million alerts each night. Orbiters around the Moon and Mars have returned millions of images sharp enough to show single boulders.

Machine learning (ML) helps in two ways. As a **filter and ranker**, it sorts a flood of data so that people look first at what most likely matters. As a **fast approximation** to slow physics, it gives in a second an answer that a full calculation needs hours to produce. Either way, scientists make the final decision. The hero image shows a third role: a robot that works beside a crew on the International Space Station (ISS).

This chapter covers astronomy, the Sun, planetary science and human spaceflight. Telescopes are described in Chapters 38 and 39, planetary missions in Chapters 24–29 and human spaceflight in Chapters 30–33. Learning methods are explained in Chapters 43 and 44, onboard computing in Chapter 45, and rover autonomy in Chapter 48.

## Why Science Needs Machine Learning

The key idea is that data now grow faster than the number of people who can look at them. Learning methods turn huge archives into short lists that people can check.

### The Data Deluge

The data rates of some major science facilities are compared in @tbl:sciencedata. Light curves call for signal detection, images for object detection and segmentation. Alert streams need decisions within minutes, while archives can be mined for years.

| Facility | Data rate or volume | Main learning tasks |
|---|---|---|
| Kepler (2009–18) | ≈ 200 000 stars every 30 min | Planet search and vetting |
| TESS (2018–) | Most of the sky in 27-day sectors | Vetting thousands of candidates |
| Gaia (2013–25) | > 500 TB for its fourth release (Dec 2026) | Classifying stars and their motions |
| Euclid (2023–) | ≈ 100 GB per day | Shapes, lenses, morphology |
| SDO (2010–) | About 1.5 TB per day | Solar features and event catalogues |
| Rubin LSST (2025–) | ≈ 10 TB per night; up to ~7 million alerts | Real/bogus, transient classes, redshifts |
| LIGO–Virgo–KAGRA | About 250 candidates in 2023–25 | Glitches, rapid parameter estimation |
| SKA (2030s) | ≈ 700 PB of products per year (estimate) | Imaging, radio transients |

: Data rates of some major science facilities and the learning tasks they drive (status October 2026). {#tbl:sciencedata}

### Funnels, Not Oracles

A discovery usually passes through a **funnel**: a search finds many candidates, filters remove most of them, and people examine the rest. Three real funnels are shown in @fig:discoveryfunnel. Kepler's final search of 198 709 stars produced 34 032 "threshold-crossing events" (TCEs): signals strong enough to pass the detection limit. Only 4 034 survived as planet candidates. A neural network then scored 1 922 unlabelled candidates, and 301 were validated as new planets.

![Discovery funnels from published numbers. (a) Kepler's final search and the ExoMiner validation of 301 new planets. (b) The ExoMiner++ catalogue for two-minute TESS data. (c) The Euclid Q1 search for strong gravitational lenses. Each step removes most of the objects left by the step before.](figures/out/ch51_funnel.svg){#fig:discoveryfunnel width=98%}

Machine learning sits at the narrow middle of each funnel. It must keep nearly all real objects (high **recall**) while passing few false ones (high **precision**; Chapter 43). A model that ranks well saves years of human effort. A model that hides a class of objects can bias a whole field.

### From Pixels to Alerts

A typical pipeline for a survey telescope is shown in @fig:sciencealerts. The observatory side is automatic. Images are calibrated and a deep "template" image of the same field is subtracted. Anything that has changed leaves a residual. A first network rejects artefacts — cosmic rays, satellite trails and bad subtractions — that are far more common than real changes. Alerts then go to **brokers**: software services that add information from catalogues, classify each object and pass it to the science teams that asked for it.

![A survey alert pipeline, modelled on the Vera C. Rubin Observatory. Learning appears at three points: rejecting artefacts, classifying alerts in the brokers, and ranking targets for follow-up. Confirmed classes return as labels and improve the next models.](figures/out/ch51_alerts.svg){#fig:sciencealerts width=98%}

The loop at the bottom matters as much as the arrows at the top. Every spectrum taken for follow-up becomes a new label, so the models learn from their own mistakes.

## Exoplanets: Finding Small Signals in Big Data

Planet searches find far more false signals than planets. Learning is most useful in **vetting**: deciding which signals are real.

### Searching Light Curves

When a planet crosses its star, the star dims by the transit depth $\delta = (R_p/R_\star)^2$ (Chapter 39). An Earth-sized planet in front of a Sun-like star gives 84 parts per million (ppm). Noise from the detector, from the star and from the spacecraft is usually larger than that for a single transit. The signal becomes visible only when many transits are added together.

The standard search is **box least squares (BLS)**. It tries every period $P$, every phase and a few transit durations. For each trial it folds the light curve and compares the mean flux inside a box with the mean outside. The result is a signal-to-noise ratio:

$$ \mathrm{SNR} = \frac{\hat\delta}{\sigma}\sqrt{n_\mathrm{in}} . $$

Here $\hat\delta$ is the measured depth, $\sigma$ the noise per point and $n_\mathrm{in}$ the number of points in transit. A signal with SNR above a threshold, 7.1 for Kepler, becomes a TCE.

A search on simulated data is shown in @fig:blssearch. Two years of photometry at 30-minute cadence contain starspots, gaps and white noise of 250 ppm per point. A planet 1.3 times Earth's radius, with a depth of 142 ppm, is hidden in it; one transit has an SNR of only 1.7. The light curve is first **detrended**: a two-day running median removes the starspot signal. The BLS search over 40 000 trial periods then finds a peak at 17.632 days (true value 17.63) with SNR 8.3 from 42 transits. The next-highest unrelated peak reaches 6.4.

![A transit search on simulated data. (a) Two years of photometry with starspot modulation; the orange line is the trend removed before the search. (b) Box-least-squares signal-to-noise against trial period; the peak lies at the planet's period, with weaker peaks at half and twice the period. (c) Data folded at the recovered period, binned (dark points) and compared with the injected transit (red).](figures/out/ch51_transit.svg){#fig:blssearch width=90%}

The recovered box depth is 130 ppm, a little less than the 142 ppm injected. Limb darkening makes a real transit rounded rather than box-shaped, and detrending removes a little depth. Such losses are why pipelines fit a physical transit model after the search.

### Vetting with Neural Networks

Most TCEs are not planets. In Kepler's final catalogue, 88 % of them did not become planet candidates. Some are **eclipsing binaries**: pairs of stars that eclipse each other. Their eclipses are often V-shaped, may show a shallow secondary eclipse half an orbit later, and may differ in depth between odd and even events. Others are instrumental artefacts, such as sudden drops in pixel sensitivity, or stellar variability that the search mistook for a dip.

Kepler's team first vetted signals by eye, then with the **Robovetter**, a set of expert rules. Each rule tests one property, such as a secondary eclipse or a shift of the star's image during the dip. In 2017 Google and Harvard researchers trained a **convolutional neural network** (Chapter 44) on about 15 000 labelled Kepler signals. Their network, AstroNet, looked at two "views" of each folded light curve: the whole orbit and a zoom on the transit. It reached about 96 % accuracy on test data.

::: history
**Landmark: Kepler-90i, the first planet found by a neural network (December 2017)**

- AstroNet was run on 670 stars that already had several known planet candidates. Weak signals around such stars are more likely to be real.
- It found Kepler-90i, a planet about 30 % larger than Earth with a 14.4-day orbit, and Kepler-80g. Kepler-90 became the first known star with eight planets, tying the Solar System.
- The team said openly that the network also produced many false positives. Each new planet was confirmed by further statistical tests and by checking the folded data by hand.
- The code was released openly in 2018, and learned vetting has since become a standard step in planet searches.
:::

NASA's **ExoMiner** (2021) went further. Its network has separate branches for transit shape, secondary eclipse, odd–even depths and image centroids, so it can explain why a signal looks false. On Kepler test data it kept 93.6 % of planets at a precision of 99 %, against 76.3 % for the best earlier classifier. Applied to 1 922 unlabelled candidates, it gave 368 a score above 0.99, and 301 of these were validated as new planets. **ExoMiner++** (2025) adapted the method to TESS, partly by transfer learning from Kepler labels. It flagged 7 330 of 147 568 two-minute-cadence TESS signals as planet candidates.

In @fig:transitvetting the idea is repeated on 36 000 synthetic folded signals. They include planets, several kinds of eclipsing binary and artefacts, with SNR from 6 to 40. A small numpy neural network sees the raw global and local views. A logistic-regression vetter sees only four hand-made tests: secondary eclipse, V shape, asymmetry and depth just outside the transit. Both were trained on 24 000 signals and tested on 8 000.

![Vetting synthetic transit signals. (a) Examples of a planet, an eclipsing binary and an artefact, with the network's planet score. (b) Precision against recall: the network keeps far more planets at high precision than a classifier built on four hand-made tests. (c) The fraction of planets kept at 98 % precision, by signal-to-noise ratio.](figures/out/ch51_vetting.svg){#fig:transitvetting width=98%}

The network reached 92.0 % accuracy. At 95 % precision it kept 84.8 % of planets, against 43.7 % for the hand-made tests. At 99 % precision the gap widened: 58.7 % against 6.5 %. The network gained most at low SNR, where single tests are noisy but the whole shape still carries information. Diluted background binaries, with weak secondaries and U-shaped eclipses, stayed hard for both. In real data they are rejected by other evidence, such as shifts of the star's image or spectra from the ground.

![The Transiting Exoplanet Survey Satellite (TESS) being lifted onto a work stand at Kennedy Space Center in February 2018. Its four cameras produce thousands of candidate signals that learned vetting tools help to sort.](figures/photos/ch51_tess.jpg){#fig:tessclean width=60%}

### Radial Velocities and Stellar Noise

Transits give a planet's size. Its mass comes from the **radial-velocity** method: the star's spectrum shifts as the planet pulls it back and forth. Earth makes the Sun wobble by only about 9 cm/s. Starspots and convection on the star's surface change the shapes of its spectral lines. They produce false velocity signals of around 1 m/s, ten times larger than the planet.

**Gaussian processes** (Chapter 43) are the usual tool: they model the star's activity as correlated noise, fitted together with the planet's orbit. In 2022 a team trained a convolutional network on the line shapes in more than 600 solar spectra from the HARPS-N solar telescope, taken over three years. It reduced the scatter of the solar velocities from 1.75 m/s to 1.04 m/s — a large step, but still ten times too much to find an Earth twin.

::: example
**Example: an Earth twin in Kepler data, and the false-alarm budget**

Kepler's noise for a bright, quiet Sun-like star was about 30 ppm over 6.5 hours. An Earth-sized planet in a one-year orbit gives a depth of 84 ppm and a central transit of about 13 hours.

1. **Noise over one transit.** Noise falls as the square root of time: 30 × √(6.5/13) = **21.2 ppm**. One transit gives SNR = 84/21.2 = **4.0**.
2. **Several transits.** Four transits give 4.0 × √4 = **7.9**, just above the 7.1 threshold. Three transits give **6.8**, which is below it. About 3.2 transits are needed, so an Earth twin is at the edge of a four-year mission.
3. **Why 7.1?** For pure Gaussian noise, the chance of a value above 7.1σ is 6.2 × 10⁻¹³. Suppose each of the 198 709 stars needs about five million independent trials of period, phase and duration. That is 10¹² tests, which gives about **0.6** false alarms. The threshold was set for exactly this reason.
4. **Reality.** Real noise is not Gaussian. The search produced 34 032 TCEs, and 88 % were not planet candidates.
5. **Human cost.** At five minutes per signal, vetting all TCEs by eye would take about 2 840 hours, or nearly two working years. A neural network scores them all in minutes.

The threshold controls false alarms from random noise; vetting controls false alarms from everything else. Learned vetting does not lower the threshold. It makes the work above the threshold affordable.
:::

## The Time-Domain Sky

The key idea of this section is speed. Transients fade in hours to weeks, so they must be classified while they can still be observed.

### Rubin and the Alert Brokers

The **Vera C. Rubin Observatory** in Chile has an 8.4 m telescope and the world's largest astronomical camera, with 3 200 megapixels. Its Legacy Survey of Space and Time (LSST) images the whole southern sky every few nights for ten years. Each image is compared with a template within about a minute. Every change becomes an **alert**: a small packet with the measurement, image cut-outs and the object's history.

::: data
**Data box — Rubin's first year of alerts**

- **First look.** First images were released in June 2025. The first world-public alerts reached the brokers on the night of 24 February 2026, about 800 000 of them.
- **Survey.** The ten-year survey formally began in mid-2026. The camera takes an image about every 40 s and the observatory produces about 10 TB of data a night.
- **Alerts.** The design allows 10 000 alerts per image and about 1 000 images a night, or 10 million alerts. The current estimate is up to 7 million a night and about 20 billion over the survey.
- **Speed and size.** 98 % of alerts must leave within 60 s of readout; each packet is up to 82 KB.
- **Brokers.** Seven "full-stream" brokers receive every alert: ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair and Pitt-Google. Two downstream services take subsets, one for Solar System objects.
- **Early science.** In about six weeks of early test surveys, Rubin found more than 11 000 new asteroids, including 33 near-Earth objects.
:::

Brokers were rehearsed for years. In the 2018 **PLAsTiCC** challenge, more than 1 000 teams classified simulated Rubin light curves, with only about 7 850 labelled for training. The winner degraded bright training objects to look faint and distant, then used gradient-boosted trees. The lesson — make the training set look like the data — applies far beyond astronomy.

### Classifying Transients

A survey light curve is sparse: each object is seen every few days, in different filters, with noisy fluxes. Classifiers work on the raw sequence or on features such as rise time, decline rate, peak colour and periodicity. A **random forest** (Chapter 43) takes a vote among many decision trees $T_b$, each trained on a random sample of the data.

$$ \hat{y}(\mathbf{x}) = \operatorname{mode}\{T_1(\mathbf{x}), \dots, T_B(\mathbf{x})\} . $$

ALeRCE, one of the Rubin brokers, has long used such a forest for light curves, alongside a convolutional network that classifies image cut-outs.

A small version is shown in @fig:transientclass. Synthetic two-band light curves of five classes were generated: type Ia supernovae, type II and type Ib/c supernovae, active galactic nuclei (AGN) and periodic variable stars. Each had 28–45 irregular epochs with noise. A random forest of 200 trees used 15 features and was trained on 6 000 objects.

![Classifying synthetic transient light curves. (a) Examples of a type Ia supernova, a type II supernova and an active galactic nucleus. (b) Confusion matrix for full light curves. (c) Accuracy, and recall for each class, as more days of data arrive after the first detection.](figures/out/ch51_transients.svg){#fig:transientclass width=98%}

With full light curves the forest classified 96.1 % of 3 000 test objects correctly. Most errors confused type Ia with type Ib/c supernovae, which also happens in real data. The useful number is the early one. Five days after the first detection, accuracy was only 66.5 %, and type Ib/c supernovae were recognised just 37 % of the time. After 20 days it reached 85.8 %. Astronomers want spectra *before* the peak, so brokers must rank objects while the classification is still uncertain. They therefore report probabilities, not labels.

::: example
**Example: Rubin's alert stream against human attention**

Take 7 million alerts in a 10-hour night.

1. **Rate.** 7 000 000 / 36 000 s = **194 alerts per second**.
2. **People.** If a trained person needs 3 s to glance at one alert, a night's stream needs 5 830 hours of attention. That is about **730 people** working 8-hour shifts, every night for ten years.
3. **Data.** At up to 82 KB per alert, the stream is about 550 GB a night. Most alerts concern known variable stars and asteroids.
4. **Follow-up.** Suppose the world's telescopes can take 100 spectra of new transients a night. That is one alert in **70 000**.
5. **What machine learning must do.** It must remove artefacts, recognise known variables and asteroids, and rank the rest. A 1 % error in a filter applied to 7 million alerts is still 70 000 mistakes a night. Errors must be counted, not just accuracy.

No human team can read the stream. People decide which questions to ask the brokers, check the top of each ranked list, and take the spectra that create new labels.
:::

### Radio Bursts and Gravitational Waves

**Fast radio bursts (FRBs)** are millisecond flashes of radio waves from distant galaxies. In 2018 a convolutional network re-analysed five hours of Green Bank Telescope data from Breakthrough Listen. It found 72 new bursts from the repeating source FRB 121102, on top of the 21 found by the original search. The second CHIME/FRB catalogue (2026) lists 4 539 bursts from 3 641 sources. At this rate, sorting real bursts from radio interference must be automatic.

**Gravitational-wave** detectors measure changes in arm length smaller than a proton. The standard search is a **matched filter**. It correlates the data with a bank of theoretical waveforms $h$, weighting each frequency $f$ by the detector noise $S_n(f)$.

$$ \rho^2 = 4 \int_0^\infty \frac{|\tilde{h}(f)|^2}{S_n(f)}\,df . $$

The fourth observing run of LIGO, Virgo and KAGRA ran from May 2023 to 18 November 2025 and produced about 250 candidate signals. Learning helps at three points. **Gravity Spy** combines volunteers and a network to classify detector "glitches", short noise bursts that can mimic signals. Research pipelines such as Aframe search for signals with neural networks in milliseconds, though they do not yet issue official alerts.

The biggest gain is in **parameter estimation**. Standard Bayesian sampling of a merger's masses, spins and sky position can take hours to days. **Simulation-based inference** instead trains a network on millions of simulated signals to output the posterior directly. In March 2025 a team reported DINGO-BNS, which infers all 17 parameters of a neutron-star merger in about one second. Its sky positions were about 30 % more precise than those of the standard rapid method. Such speed lets telescopes point at a kilonova before it fades.

Learning can also improve the instrument itself. In September 2025 researchers from Google DeepMind and LIGO reported **Deep Loop Shaping**, a reinforcement-learning controller (Chapter 48) for one mirror-alignment loop at LIGO Livingston. It cut control noise between 10 and 30 Hz by more than 30 times, and by up to 100 times in narrow bands. It was a demonstration on one loop, not yet part of routine observing.

## Galaxies, Lenses and Cosmology

Learning turns images of billions of galaxies into measurements: shapes, distances and the rare objects among them.

### Galaxy Shapes

**Galaxy Zoo**, launched in 2007, asked volunteers to classify galaxy images (Chapter 43). Its labels trained **Zoobot**, a family of networks that predict how volunteers would answer each question about a galaxy. In 2023 Zoobot measured detailed shapes for 8.67 million galaxies in the DESI Legacy Imaging Surveys. For Euclid, tests on simulated images suggest that about 800 million galaxies in the wide survey could be measured reliably.

In 2024 a network trained on labelled Hubble images was adapted to the sharper, redder images of the James Webb Space Telescope (JWST). It classified about 20 000 distant galaxies in the CEERS survey and agreed with visual classifications 80–90 % of the time. Moving a model between instruments with few new labels is called **domain adaptation** (Chapter 45).

### Strong Lenses in Euclid

A massive galaxy bends the light of a galaxy behind it into arcs or rings. Such **strong lenses** weigh the dark matter in the lensing galaxy and test cosmology, but only roughly one galaxy in ten thousand shows one. Euclid's first quick release (March 2025) covered 63 square degrees. An ensemble of networks, including Zoobot, ranked the galaxies. Volunteers on the Space Warps project then inspected the best candidates, and experts graded and modelled them.

The result was a catalogue of 497 galaxy–galaxy lenses, 250 of them "grade A"; 243 of those were new. The same engine is expected to yield about 7 000 high-confidence lenses in the first major data release (from late 2026), and more than 100 000 in the full survey.

### Photometric Redshifts

Most galaxies are too faint for a spectrum, so their distance must be estimated from colours in a few broad filters. This is a **photometric redshift**. Spectral features, such as the 4000 Å break and the Lyman break, move through the filters as redshift grows. Learning methods map colours directly to redshift, trained on galaxies whose spectroscopic redshifts are known. Quality is measured by the normalised scatter of $\Delta z = (z_\mathrm{phot} - z_\mathrm{spec})/(1 + z_\mathrm{spec})$:

$$ \sigma_\mathrm{NMAD} = 1.4826 \times \operatorname{median} \left| \Delta z - \operatorname{median}(\Delta z) \right| , $$

and by the fraction of **outliers** with $|\Delta z| > 0.15$. Rubin's goals for its "gold" sample, brighter than magnitude 25.3 in the i band, are a scatter below 0.02 (requirement 0.05) and fewer than 10 % outliers.

In @fig:photozrf, a random forest is tested on 60 000 synthetic galaxies observed in six Rubin-like filters. Trained on a representative sample of 30 000, it reached a scatter of 0.017 with 12.0 % outliers. Errors grew steeply for faint galaxies, from 0.007 at i ≈ 20 to 0.13 at i ≈ 25. Then the forest was trained only on galaxies brighter than i = 22.5 and nearer than z = 1.2, like a typical spectroscopic sample. The outlier fraction rose to 19.4 %, and to 61 % for the faintest galaxies. A model cannot learn what its training set never shows.

![Photometric redshifts from a random forest. (a) Photometric against true redshift when the training set represents the whole population. (b) The same when training uses only bright, nearby galaxies: faint and distant galaxies are pulled to the wrong redshifts. (c) Outlier fraction against brightness for both cases.](figures/out/ch51_photoz.svg){#fig:photozrf width=98%}

### Simulation-Based Inference in Cosmology

Cosmology usually compresses a survey into a few summary statistics, such as the two-point correlation of galaxy positions, and fits them with a formula. Much information lies in the non-linear structure that such summaries miss. **Simulation-based inference (SBI)** uses Bayes' theorem,

$$ p(\boldsymbol\theta \mid \mathbf{x}) \propto p(\mathbf{x} \mid \boldsymbol\theta)\, p(\boldsymbol\theta) , $$

without writing down the likelihood $p(\mathbf{x} \mid \boldsymbol\theta)$. Instead, thousands of simulated universes with known parameters $\boldsymbol\theta$ train a network to estimate the posterior. The SimBIG project applied this to part of the BOSS galaxy survey. Using the full three-dimensional galaxy field, it constrained the clustering amplitude $\sigma_8$ 2.65 times more tightly than a standard power-spectrum analysis of the same data. The method is only as good as its simulations: if they miss a physical effect, the answer is precise but wrong.

Learning also works inside telescope pipelines (Chapter 38), flagging cosmic rays and artefacts and separating overlapping objects. Landmark results in astronomy are listed in @tbl:astroailandmarks.

| Result | Year | Data | Method | Outcome | Status (Oct 2026) |
|---|---|---|---|---|---|
| AstroNet | 2017 | Kepler | 1-D CNN | Kepler-90i, Kepler-80g | Research, open code |
| ExoMiner | 2021 | Kepler | Explainable CNN | 301 validated planets | Planets in NASA archive |
| ExoMiner++ | 2025 | TESS | Transfer learning | 7 330 candidates | Public catalogue |
| FRB 121102 search | 2018 | Green Bank | CNN | 72 new bursts | Research |
| Galaxy Zoo DESI | 2023 | DESI imaging | Zoobot CNN | 8.67 million galaxies | Public catalogue |
| Euclid lens engine | 2025 | Euclid Q1 | CNN ensemble + volunteers | 497 lenses | In Euclid pipeline |
| SimBIG | 2023–24 | BOSS | Simulation-based inference | σ₈ 2.65× tighter | Research |
| DINGO-BNS | 2025 | LIGO–Virgo | Neural posterior | 17 parameters in 1 s | Research |
| Deep Loop Shaping | 2025 | LIGO Livingston | Reinforcement learning | Control noise ÷ 30–100 | Demonstration |
| Rubin brokers | 2026 | LSST alerts | Forests, CNNs, RNNs | Real-time classes | Operational |

: Landmark uses of machine learning in astronomy. CNN: convolutional neural network; RNN: recurrent neural network. {#tbl:astroailandmarks}

## The Sun: Features and Event Catalogues

The key idea is that heliophysics needs *catalogues*: lists of every flare, sunspot group, filament and eruption, with times and positions. Forecasting space weather is covered in Chapter 47. Here the aim is to describe what happened.

The Solar Dynamics Observatory (SDO) sends about 1.5 TB of images a day. Around its launch in 2010, NASA funded a **Feature Finding Team** to build automatic detection modules. Their reports feed the **Heliophysics Event Knowledgebase** (HEK), which scientists search for, say, every filament that erupted near an active region. A 2016 study counted more than 280 000 event reports for seven kinds of solar phenomenon. Coronagraph catalogues such as CACTus detect coronal mass ejections automatically, and are compared with catalogues made by people.

The early modules used thresholds, edge detection and tracking. Since about 2018, convolutional networks have segmented coronal holes, filaments and active regions in several wavelengths at once; the Surya foundation model is described in Chapter 44. The challenge is consistency. A catalogue that changes its detector can create false trends over the 11-year solar cycle, so versions must be recorded and old data reprocessed.

## Planetary Surfaces and Science Autonomy

Planetary images and spectra become maps — of craters, rocks and minerals — and those maps drive landing, driving and sampling decisions. Learning makes global maps possible. Physics decides what they mean.

### Craters and Surface Ages

On airless bodies, craters accumulate at a known rate. Counting them dates a surface: more craters per square kilometre means an older surface. The method rests on two functions calibrated with Apollo and Luna samples (Chapter 29). The **production function** gives the shape of the size distribution, and the **chronology function** gives the density of craters larger than 1 km, $N_1$, after $T$ billion years. For the Moon, Neukum and colleagues (2001) give

$$ N_1(T) = 5.44 \times 10^{-14} \left( e^{6.93\,T} - 1 \right) + 8.38 \times 10^{-4}\, T \quad \text{per km}^2 . $$

The first term describes the heavy bombardment of the early Moon; the second, the nearly constant rate since about 3 billion years ago.

Counting small craters by hand is slow and inconsistent between people, so trained detectors now do it at planetary scale. In 2020 a team used transfer learning on Chang'e-1 and Chang'e-2 data to find 109 956 new lunar craters. In 2021 a detector trained on HiRISE images found about 90 million craters in the Context Camera mosaic of Mars. Rays of small secondary craters then traced a group of Martian meteorites to their source craters in the Tharsis region. Crater detection for navigation is covered in Chapter 48.

A detector does not see every crater. Small craters, only a few pixels across, are often missed, and shadows or boulders can be mistaken for craters. The fix is to measure **completeness** $c(D)$ and the false-positive density $f(D)$ by testing the detector on images with known craters. A model age is then fitted by **maximum likelihood**. Suppose $k_i$ craters are counted in size bin $i$ of an area $A$. The expected count $\lambda_i$ and the log-likelihood are

$$ \lambda_i(T) = A \, \Delta N_i(T) \, c_i + A f_i , \qquad \ln L(T) = \sum_i \left[ k_i \ln \lambda_i - \lambda_i \right] , $$

Here $\Delta N_i$ is the number per unit area in bin $i$ from the production and chronology functions.

In @fig:craterages this is applied to a synthetic 10 km² lunar surface aged 50 million years, imaged at 1.5 m per pixel. The synthetic detector finds half the craters 7 pixels across and 95 % of large ones. About 40 % of its detections between 6 and 10 m are false. Fitting the raw counts at all sizes gives an age of 17 million years, three times too young. Counting only craters of 30 m and larger gives an unbiased median of 49 million years, but with a spread of ±13 %. Correcting for completeness and false positives, and fitting from 12 m upwards, gives 51 million years with a spread of only ±3 %.

![Crater-count dating with an imperfect detector. (a) Cumulative crater densities for one synthetic count, with model curves for three ages; raw detections fall below the truth at small sizes. (b) Ages from 200 repeated counts: raw counts at all sizes are far too young; corrected counts are accurate and precise. (c) Age uncertainty against count area.](figures/out/ch51_craters.svg){#fig:craterages width=98%}

The lesson applies to every automated catalogue: a detector's errors must be measured and modelled, not just reduced. Small craters also reach **equilibrium** on old surfaces, where new craters erase old ones as fast as they form. Below that size, no detector can date the surface.

### Boulders, Rockfalls and Landslides

Boulders tell geologists how deep the regolith is and how surfaces erode. They are also hazards for landers and rovers (Chapter 27). In 2020 a convolutional network searched images from the Narrow Angle Camera (NAC) of NASA's Lunar Reconnaissance Orbiter for boulders that had rolled downhill. It mapped 136 610 such rockfalls and showed that impacts trigger most of them. In 2025 a team mapped about 94 million boulders larger than about 4.5 m, using 635 000 NAC images between 60° S and 60° N.

Shadows hide some of the most valuable terrain. Permanently shadowed craters near the lunar poles may hold water ice (Chapter 41). In 2021 a deep-learning tool called HORUS removed noise from NAC images of these craters, lit only by faint light scattered from nearby slopes. It revealed features a few metres across at about 1.5 m per pixel. It was later used to examine candidate target regions for NASA's VIPER rover.

Such mapping projects are summarised in @tbl:planetmaps. Fresh impacts found by a classifier in Mars orbiter images are described in Chapter 44.

| Project | Body, data | Method | Result | Use |
|---|---|---|---|---|
| Lunar rockfalls (2020) | Moon, LRO NAC | CNN detector | 136 610 rockfalls | Erosion; hazards |
| Chang'e craters (2020) | Moon, Chang'e-1/2 | Transfer learning | 109 956 new craters | Crater ages |
| HORUS (2021) | Moon, NAC in shadow | Physics-guided denoising | ≈ 1.5 m images of shadowed craters | Ice prospecting, VIPER |
| Mars craters (2021) | Mars, CTX mosaic | CNN detector | ≈ 90 million craters | Meteorite source craters |
| AI4Mars (2021) | Mars, rover images | Crowd labels + segmentation | 326 000 labels | Terrain classes for driving |
| Lunar boulders (2025) | Moon, 635 000 NAC images | CNN detector | ≈ 94 million boulders | Regolith depth; landing |

: Planetary mapping with machine learning. {#tbl:planetmaps}

### Minerals from Spectra

Minerals absorb light at characteristic wavelengths. Olivine has a broad band near 1.05 µm, pyroxenes absorb near 0.9 and 1.9 µm, and clays and carbonates have narrow bands between 2.2 and 2.5 µm (Chapter 13). Imaging spectrometers record hundreds of wavelengths for every pixel. CRISM, on NASA's Mars Reconnaissance Orbiter, did this at about 18 m per pixel from 2006 until it was retired in April 2023. Its maps of carbonates in Jezero crater helped select the landing site of Perseverance (@fig:jezerocrism).

![Minerals in Jezero crater, mapped by the CRISM imaging spectrometer and the Context Camera on Mars Reconnaissance Orbiter. Green marks carbonates; red marks olivine-rich sand. Maps like this helped NASA choose Perseverance's landing site.](figures/photos/ch51_jezero.jpg){#fig:jezerocrism width=62%}

A pixel usually contains several minerals. In **linear spectral unmixing**, the spectrum $\mathbf{x}$ of a pixel is modelled as a weighted sum of pure "endmember" spectra, the columns of a matrix $\mathbf{E}$.

$$ \mathbf{x} = \mathbf{E}\,\mathbf{a} + \mathbf{n}, \qquad a_k \ge 0, \quad \sum_k a_k = 1 . $$

The abundances $\mathbf{a}$ are found by least squares with both constraints. This is called **fully constrained least squares (FCLS)**. When no spectral library is available, **non-negative matrix factorisation (NMF)** can estimate endmembers and abundances together, but its endmembers need not be pure minerals.

In @fig:specunmix both methods are applied to a synthetic scene of 3 456 pixels with 221 bands. It contains a carbonate- and clay-bearing fan, an olivine-rich channel, pyroxene and dust. The endmembers vary from pixel to pixel in band depth and brightness, and topographic shading changes the overall brightness. With the right library, FCLS recovered the abundances with errors of 5.0–7.4 percentage points. Unconstrained least squares gave similar average errors, but 5.3 % of its abundances were negative, which is physically impossible. NMF found endmembers that differed from the true minerals by 8–19° in spectral angle.

![Linear unmixing of a synthetic hyperspectral scene. (a) The five endmember spectra; dotted lines mark key absorption bands. (b) True against estimated abundances from fully constrained least squares. (c–d) True and estimated carbonate abundance. (e) Fit residual when the clay (smectite) spectrum is left out of the library: the error outlines where the clay is.](figures/out/ch51_unmixing.svg){#fig:specunmix width=98%}

Panel (e) shows the most useful diagnostic. With smectite removed from the library, the fit residual rose sharply where smectite was present; its 99th percentile was 2.8 times the median. The residual map points to minerals the library lacks. In fine-grained real surfaces, light passes through several grains and mixing is non-linear. Networks trained on laboratory mixtures are an active research topic, but their results are still checked against band positions a spectroscopist can explain.

### Landing Sites, Traverses and Resources

Before a landing, engineers must know where the ground is safe. JPL's **SPOC** (Soil Property and Object Classification) network classifies terrain in HiRISE images into types such as sand, bedrock and ridges. It was used to judge how easily a rover could drive at candidate landing sites for Perseverance. The **AI4Mars** project (2021) collected about 326 000 terrain labels on 35 000 rover images from volunteers, ten per image. A segmentation network trained on them reached more than 96 % accuracy on an expert-labelled test set.

Resource prospecting combines these tools (Chapter 41). Maps of shadowed craters, boulders, slopes and temperature are merged to find ice that a rover could reach. The NASA–IBM Lunar Foundation Model (2026) is one example; Chapter 44 gives its results and limits.

### Science Autonomy on Rovers and Probes

A rover or probe can also decide what to measure. The first steps were small. In 2006 the Mars Exploration Rovers received software that looked for dust devils and clouds in sequences of images. It first detected a dust devil on board Spirit in April 2007. On dust-devil sequences it cut the data volume by about 75 %, because only frames with moving features were sent home.

**AEGIS** (Chapter 48) picks rock targets for the laser spectrometers on Curiosity and Perseverance. By May 2026 it had chosen 596 targets on Curiosity and 293 on Perseverance. Perseverance's X-ray spectrometer **PIXL** goes further. Its hexapod mount places it close to a rock, and it scans a postage-stamp-sized patch with thousands of X-ray shots. Its **adaptive sampling** software watches the results. When it sees minerals of interest, such as carbonates or phosphates, it stops and collects data for longer (@fig:pixlscan). Each decision is made on Mars, without waiting for the ground.

![A PIXL scan of the rock target "Thunderbolt Peak", recorded by Perseverance on 8 July 2024. Each dot marks a point hit by the X-ray beam; colours show the minerals detected. PIXL's software can lengthen its measurements on board when it finds minerals of interest.](figures/photos/ch51_pixl.jpg){#fig:pixlscan width=62%}

Future probes to icy moons may have to detect a plume or outburst and re-plan within hours. In sample curation (Chapter 29), learning could help find rare grains in images and keep records consistent between laboratories, without ever risking irreplaceable material. Onboard science autonomy is summarised in @tbl:onboardscience.

| System | Mission | What it decides | Since | Status (Oct 2026) |
|---|---|---|---|---|
| Dust-devil and cloud detection | Spirit, Opportunity | Which frames to send home | 2006–07 | Missions ended |
| Autonomous Sciencecraft | EO-1 | Re-plans imaging after events (Chapter 48) | 2004 | Mission ended 2017 |
| AEGIS | Opportunity, Curiosity, Perseverance | Laser targets after a drive | 2010 | Operational |
| PIXL adaptive sampling | Perseverance | Where to dwell longer in a scan | 2021 | Operational |
| Vision-language route planning | Perseverance | Ground-planned waypoints (Chapter 48) | 2025 | Demonstrated |
| Onboard plume or outburst detection | Icy moons, comets | When to re-target | — | Research |

: Onboard science autonomy on planetary missions. {#tbl:onboardscience}

## AI for Human Spaceflight

A crew far from Earth must become its own doctor, engineer and mission control. AI can help, but only if it works without a link to Earth and its advice can be checked.

### Watching Crew Health

Wearable sensors measure the body continuously. Canada's **Bio-Monitor** has been used on the ISS since early 2019 (@fig:biomonitorshirt). It is a stretchable shirt with a headband and a small recorder. It tracks heart activity, breathing, skin temperature, blood pressure and blood oxygen during work, exercise and sleep. On Artemis II in April 2026, all four astronauts wore wrist devices for the ARCHeR study. These logged movement, sleep and exposure to light around the Moon.

![Canadian astronaut David Saint-Jacques demonstrates the Bio-Monitor smart shirt on the ISS in January 2019. Its sensors record heart activity, breathing, blood pressure, blood oxygen and skin temperature.](figures/photos/ch51_biomonitor.jpg){#fig:biomonitorshirt width=58%}

Such data are only useful if someone looks at them. Learning methods can build a **personal baseline** for each astronaut, the normal range of heart rate, temperature and sleep, and flag departures from it. A rising resting heart rate and temperature can precede the symptoms of an infection. The statistics are those of anomaly detection (Chapter 49), but a miss can cost a life.

### Exploration Medicine

On the ISS, a sick astronaut can come home within hours. In January 2026, NASA's Crew-11 returned about a month early, the first time an ISS crew was brought home for medical reasons (Chapter 30). A Mars crew will have no such option for many months. Its medical kit, training and software must cover almost everything that can go wrong.

NASA plans medical kits with simulation. Its **Integrated Medical Model** runs Monte Carlo missions over about 100 medical conditions. Each simulated case uses drugs and supplies from the kit, and untreated conditions count as risk, so planners can choose the kit that lowers risk most for its mass. A newer tool, IMPACT, adds conditions that matter for exploration.

Decision support is the next step. In 2025 NASA and Google tested a prototype **Crew Medical Officer Digital Assistant**. It takes speech, text and images, works with little or no link to Earth and records each recommendation. Physicians, one of them an astronaut, graded it with the structured exams used for medical students. Its diagnoses were correct in 88 % of runs for an ankle injury, 80 % for ear pain and 74 % for flank pain. NASA called these early results; the tool is not approved for use.

**Ultrasound** is the main imaging tool in space, but good images need skill. On the ISS, experts on the ground guide astronauts in real time, which will not work with a 40-minute round trip. ESA's ALISSE prototype (2024) uses a network trained on hundreds of thousands of labelled scans. It tells the user where to move the probe and how likely it is that the image shows the right organ. In tests on kidneys and bladders, nine out of ten images taken by untrained students were clinically acceptable.

**Behavioural health** may be the hardest part (Chapter 30). ARCHeR also studied stress, cognition and teamwork, and researchers are testing whether voice, sleep and activity patterns give early warning of fatigue or conflict. Such monitoring raises questions of privacy and trust, so crews must agree to it and control what is shared.

### Assistants and Robots in the Cabin

Voice assistants that can read procedures, log work and answer questions have been tested for several years (@tbl:crewai). Language models now make them far more capable. Their main risk is the confident wrong answer, or **hallucination** (Chapter 44). For crew use, an assistant must quote its sources, such as the procedure, the step and the telemetry, so that the astronaut can check them.

::: history
**Landmark: from CIMON to language models in orbit (2018–2025)**

- **CIMON** (Crew Interactive Mobile Companion), a floating sphere built by Airbus and IBM for the German space agency DLR, reached the ISS in July 2018. On 15 November 2018 it recognised Alexander Gerst, talked with him and showed procedures. It returned to Earth in August 2019.
- **CIMON-2** arrived in December 2019, adding tone analysis to judge a speaker's mood. Its speech processing ran on ground servers.
- **Callisto** flew inside Orion on the uncrewed Artemis I mission in late 2022, testing an offline voice assistant and video calls (@fig:callistoorion).
- In **August 2024** a generative language model ran on HPE's Spaceborne Computer-2 on the ISS. The Space Llama project followed in April 2025, with an open-source model tuned for station science.
- In **July 2025** China delivered the **Wukong AI** model to its Tiangong station. Its onboard part helped crew members prepare for a spacewalk.
- Also in **July 2025**, JAXA astronaut Takuya Onishi used CIMON in the Columbus module to command JAXA's Int-Ball2 camera drone in Kibo (@fig:cimonichiban). It was the first time robots of two agencies worked together on the ISS.
:::

::: figrow
![JAXA astronaut Takuya Onishi sets up CIMON in the ISS's Kibo module on 18 July 2025, for a test in which it commanded the free-flying camera robot Int-Ball2.](figures/photos/ch51_cimon.jpg){#fig:cimonichiban}

![The Callisto technology demonstration inside the Orion crew module on Artemis I, 18 November 2022. The payload tested an offline voice assistant and video calls for future crews.](figures/photos/ch51_callisto.jpg){#fig:callistoorion}
:::

Robots are the physical side of the same idea. **Astrobee**, the free-flyer in the hero image, has tested autonomous inventory and inspection since 2019, and JAXA's **Int-Ball2** films crew activities (Chapter 48). For a Mars habitat, the goal is a robot that keeps the station running while the crew sleeps or works outside, and before any crew arrives.

| System | Who, where | Function | Years | Status (Oct 2026) |
|---|---|---|---|---|
| Bio-Monitor | CSA, ISS | Wearable vital signs | 2019– | In use for research |
| ARCHeR wrist devices | NASA, Artemis II | Sleep, activity, light exposure | 2026 | Flown |
| CIMON, CIMON-2 | DLR, Airbus, IBM; ISS | Voice assistant, robot control | 2018– | Demonstrations; used in 2025 |
| Callisto | Lockheed Martin; Orion | Offline voice assistant | 2022 | Flown once (uncrewed) |
| Space Llama | Booz Allen, Meta, HPE; ISS | Language model on board | 2025– | Demonstration |
| Wukong AI | China; Tiangong | Language model, EVA preparation | 2025– | In use (reported) |
| Medical Officer Digital Assistant | NASA, Google | Diagnosis support | 2025 | Prototype, ground tests |
| ALISSE | ESA, GMV | Ultrasound guidance | 2024 | Prototype |
| Columbus ECLSS toolchain | Airbus, ESA | Anomaly detection, diagnosis | 2020– | Ground pilot |
| Astrobee, Int-Ball2 | NASA; JAXA | Free-flying robots | 2019–; 2023– | Operational test beds |

: AI systems for crew support (status October 2026). {#tbl:crewai}

### Smart Habitats and Predictive Maintenance

A habitat is a machine that keeps people alive (Chapters 30 and 32). Its fans, pumps, valves and filters wear out, and on a Mars mission every failed part must be fixed with a spare carried from Earth. Detecting wear early lets the crew plan repairs and can reduce the spares carried.

The European Columbus module on the ISS sends about 17 000 telemetry parameters. Its life-support system alone produces more than 1 000 signals sampled once a second. Since about 2020, Airbus has trained autoencoders on these data to learn normal behaviour. In 2025 researchers described a ground toolchain, integrated at Airbus, that detects anomalies, diagnoses their cause and recommends actions. An ESA project, ORBIT-STAR, built an onboard demonstrator that sends event messages to ground and crew.

A synthetic test shows why learned models help (@fig:fanprognosis). A fleet of 60 cabin fans ran for 1 100 days. Each wore out at a random time, and its vibration, current and temperature rose in its last weeks. But the fans also changed speed, and the cabin warmed and cooled. A fixed vibration limit therefore either alarmed whenever a fan ran fast, or alarmed late. **Gradient-boosted trees** — many small trees, each correcting the errors of the ones before — learned to predict "failure within 30 days" from the raw signals and their trends. They were trained on 40 fans and tested on 20 others. Allowing at most 0.5 false alarms per fan-year, the model gave a median warning of 29 days and warned of every failure. The fixed limit gave 15 days and missed 15 % of failures.

![Predictive maintenance of synthetic cabin fans. (a) One test fan before its failure: raw vibration rises whenever the fan runs fast; the speed-normalised signal and the model's risk score rise only as wear grows. (b) Median warning time against false alarms per fan-year, for gradient-boosted trees and a fixed vibration limit.](figures/out/ch51_eclss.svg){#fig:fanprognosis width=98%}

Real fleets are smaller and failures rarer, so models must share data across similar units and stations (Chapter 49).

### Earth-Independent Operations

On the ISS, mission control answers within seconds. At Mars the one-way **light-time** — the time a signal takes to cross the distance $d$, $\tau = d/c$ — is 3 to 22 minutes. A ground answer takes at least $2\tau$ plus the time experts need to respond. For about two weeks near **solar conjunction**, when Mars is behind the Sun, there is no reliable link at all. In @fig:marsdelay this is computed from the orbits of Earth and Mars for 2026–29. Mars was within 2° of the Sun from 1 to 17 January 2026, and will be again from 11 to 30 March 2028.

![Why a Mars crew must decide for itself. (a) One-way light-time between Earth and Mars in 2026–29 and the resulting ground loop, with solar conjunctions shaded. (b) Approximate time available to act in several emergencies and failures, compared with the ground loop for the Moon, for Mars near and far, and for solar conjunction.](figures/out/ch51_delay.svg){#fig:marsdelay width=98%}

NASA's analogue missions test this. The second one-year CHAPEA mission, with four volunteers in a 3-D-printed Mars habitat in Houston, ran from 19 October 2025 to 31 October 2026 with simulated communication delays.

::: example
**Example: autonomy requirements for a Mars crew with a 20-minute delay**

Assume a one-way light-time of 20 minutes and 30 minutes for experts on Earth to respond.

1. **Ground loop.** 2 × 20 + 30 = **70 minutes** for one question and answer. A diagnosis that needs three exchanges takes **3.5 hours**.
2. **Emergencies.** A fire, a fast air leak, cardiac arrest, a severe allergic reaction or a toxic leak must be handled within seconds to tens of minutes. The ground cannot help in time. Procedures, alarms and decision support must all be on board and work offline.
3. **Slower failures.** Four crew members exhale about 1.0 kg of CO₂ each per day. In 100 m³ of air at 22 °C, the partial pressure rises by $\dot{m}RT/(MV)$ ≈ **93 Pa per hour**. From 0.4 to 1.0 kPa takes **6.5 hours**, about 5.5 ground loops. The ground can advise, but onboard diagnosis should find the cause in the first hour.
4. **Conjunction.** For about 16–18 days no link is possible. A 900-day mission includes at least one conjunction. Any illness or failure in that window must be handled alone.
5. **Requirements.** The crew needs offline medical decision support, guided imaging, health monitoring with personal baselines, prognostics for critical spares, and a searchable record of every procedure. All must keep working if a computer fails, so simple manual procedures remain the backup.

The ground's role shifts from control to support. It reviews logs, updates models and plans the next days, while the crew and its software handle the present.
:::

### Augmented Reality for EVA and Maintenance

**Augmented reality (AR)** overlays instructions on what a person sees. In NASA's Project Sidekick, Microsoft HoloLens headsets reached the ISS in December 2015 (@fig:hololenskelly). In "remote expert" mode, engineers on the ground saw what the astronaut saw and drew guidance into the view. In "procedure" mode, the headset showed animated steps. With Mars delays, only the procedure mode is practical.

![NASA astronaut Scott Kelly wears a Microsoft HoloLens headset on the ISS on 20 February 2016, during Project Sidekick, a test of augmented reality for crew procedures.](figures/photos/ch51_hololens.jpg){#fig:hololenskelly width=50%}

Learning adds recognition: a headset that recognises a part, checks that the right bolt is being turned and records each step. For spacewalks (Chapter 33), helmet displays could show suit data, routes and procedures. Such systems must be verified like flight software, because a wrong overlay can be worse than none.

## Validating an AI Discovery

A discovery made with machine learning must pass the same tests as any other, and some extra ones. A network's score is a ranking, not a probability that an object is real, until it is calibrated.

Three kinds of evidence matter. **Completeness** says how many real objects the method finds, measured by injecting fake signals into real data, as in the crater example. **Reliability** says how many of the claimed objects are real, measured with known false positives and with independent data. **Physical plausibility** asks whether the object makes sense, such as a transit shape that fits its star. Learned models can also exploit quirks of a data set, such as a camera artefact that happens to correlate with a class. This **leakage** (Chapter 43) is found only by careful checks.

Status needs the same care (@tbl:astroailandmarks, @tbl:onboardscience, @tbl:crewai). Most science results so far come from archives on the ground, with people checking the final list. Onboard science autonomy is operational only in narrow, well-tested forms, such as AEGIS and PIXL. AI for crew health and assistance is still at the stage of demonstrations and prototypes.

::: note
**Practice: validating an AI discovery before publication**

1. **Freeze the test set.** Set aside labelled data that the model never sees during development, split by object, region or time so that neighbours cannot leak between sets.
2. **Inject and recover.** Insert synthetic signals — transits, craters, lenses — into real data and run the full pipeline. Report completeness against signal strength and size.
3. **Beat a baseline.** Compare with the simplest established method, such as BLS with hand-made vetting, template matching or a χ² fit. Report both on the same data.
4. **List the false-positive scenarios.** For each candidate, check every known impostor: eclipsing binaries, background stars, artefacts, shadows, unmodelled minerals. Use evidence the model did not see, such as centroids, spectra or other instruments.
5. **Calibrate the score.** Convert scores to probabilities with held-out data, then combine them with prior rates to estimate the chance that each object is a false positive.
6. **Explain and ablate.** Check which inputs drive a decision, and remove them one at a time. A planet score that depends on a detector edge is a warning.
7. **Confirm independently.** Seek follow-up with a different method or instrument, or ask an independent team to repeat the analysis.
8. **Publish everything needed to repeat it.** Release code, model weights, data versions, thresholds and the selection function, so that later studies can correct for what the method missed.
:::

::: key
**Key takeaways**

- Science data now outgrow human attention: Rubin can send up to about 7 million alerts a night, and Kepler's final search produced 34 032 signals. Machine learning acts as a filter and ranker in a discovery funnel; people make the final decision.
- Learned vetting finds planets that rules miss. AstroNet found Kepler-90i in 2017, and ExoMiner validated 301 Kepler planets. In this chapter's test, a small network kept 84.8 % of planets at 95 % precision, against 43.7 % for hand-made tests.
- Training sets must represent the data. Random-forest photometric redshifts trained only on bright, nearby galaxies had 19.4 % outliers instead of 12.0 %.
- Speed creates science: transients must be classified within days, and neutron-star mergers can now be characterised in about one second.
- Automated catalogues of craters, boulders and minerals now cover whole planets, but detectors must be calibrated. Ignoring completeness made a 50-million-year surface look 17 million years old.
- Onboard science autonomy is operational in narrow forms: AEGIS selects laser targets and PIXL lengthens its scans on Mars without waiting for Earth.
- A Mars crew faces a ground loop of over an hour and two weeks without contact at conjunction. Medical decision support, guided ultrasound, assistants and predictive maintenance are promising, but mostly prototypes in October 2026.
:::

::: questions
**Review questions**

1. Explain the discovery funnel with Kepler's numbers. Why does a 7.1σ threshold still leave tens of thousands of false signals?
2. A planet gives a depth of 200 ppm and 3-hour transits. The noise is 300 ppm per 30-minute point. How many transits are needed for SNR 7.1?
3. In @fig:transitvetting, why does the neural network gain most at low signal-to-noise ratio? Which false positives remain hard, and how are they rejected in practice?
4. Rubin sends 7 million alerts in a 10-hour night. If a broker's filter has a 0.5 % false-positive rate for "young supernova", how many false candidates does it pass? Why should brokers report probabilities rather than labels?
5. Define $\sigma_\mathrm{NMAD}$ and the outlier fraction for photometric redshifts. Why did training on bright, nearby galaxies hurt faint galaxies most?
6. What does simulation-based inference avoid writing down? What is its main weakness?
7. Using the lunar chronology function, estimate $N_1$ for surfaces aged 0.05, 1 and 3.5 billion years. Why does the exponential term matter only for old surfaces?
8. Explain how completeness and false positives bias crater-count ages. How are they measured?
9. Write the linear mixing model with its constraints. How can the fit residual reveal a mineral missing from the library?
10. List the conditions that decide whether a Mars crew must act without help from Earth. Which AI tools would you fly first, and how would you verify them?
:::
