---
title: AI for Weather, Climate and Space Weather
hero: ch47
abstract: Between 2022 and 2026 machine learning changed weather forecasting faster than any idea since the first computer forecasts. This chapter explains how. It recalls how physics models and data assimilation turn satellite data into forecasts, then follows the learned models from the first research papers to operational service at ECMWF, NOAA and other centres. It shows how they are built and trained, how their skill is measured fairly, and where they still fall short. It covers machine learning inside the observing chain, nowcasting, climate emulators, downscaling and digital twins. It ends with space weather: flares, coronal mass ejections, geomagnetic storms and the slow road to operations. Small models trained in Python make each idea concrete.
---

Weather forecasting is one of the largest users of satellite data. It is also where machine learning has changed operational practice fastest. In 2022 a learned weather model was a research curiosity. By October 2026 learned models were running every day at the European Centre for Medium-Range Weather Forecasts (ECMWF), the US National Oceanic and Atmospheric Administration (NOAA), Germany's weather service and China's. A learned model at the US National Hurricane Center slightly beat the official track forecasts of 2025 at some lead times.

These models did not appear from nowhere. They learned from decades of **reanalysis**, the best reconstruction of past weather, made by physics models that absorbed billions of satellite observations. They still start from analyses made the same way. The hero image above shows Hurricane Matthew nearing Florida on 7 October 2016, seen by NOAA's GOES-East satellite. Images like this one are the raw material of every learned forecast.

This chapter builds on Chapter 16 (weather satellites and forecasting), Chapters 22 and 23 (the space environment) and Chapters 43 and 44 (learning methods). Data and computing are covered in Chapter 45, and AI for Earth observation in Chapter 46.

## From Physics to Learning

The key idea of this section is that a forecast needs two things: a good picture of the atmosphere now, and a good rule for how it changes. For 70 years both came from physics. Machine learning first replaced the rule, and is now starting on the picture.

### The Forecasting Chain

A modern weather service is a pipeline (@fig:wxpipeline). Observations come from satellites, weather balloons (radiosondes), aircraft, ships, buoys, radars and ground stations. They are checked, corrected for instrument biases and thinned. **Data assimilation** then combines them with a short-range forecast, the **background**, to make the **analysis**: the best estimate of the whole atmosphere at one moment. A **numerical weather prediction (NWP)** model then steps the analysis forward in time by solving the equations of fluid flow, heat and moisture. Finally, the output is corrected statistically and turned into products and warnings.

![The weather forecasting chain and the places where machine learning enters it. Learned models trained on reanalysis now run alongside physics models (4); end-to-end systems that learn directly from observations (6) are still research.](figures/out/ch47_pipeline.svg){#fig:wxpipeline width=96%}

Variational data assimilation finds the atmospheric state $\mathbf{x}$ that best fits both the background $\mathbf{x}_b$ and the observations $\mathbf{y}$. It does this by minimising a cost function:

$$ J(\mathbf{x}) = \tfrac12 (\mathbf{x}-\mathbf{x}_b)^{\mathsf T} \mathbf{B}^{-1} (\mathbf{x}-\mathbf{x}_b) + \tfrac12 \big(\mathbf{y}-H(\mathbf{x})\big)^{\mathsf T} \mathbf{R}^{-1} \big(\mathbf{y}-H(\mathbf{x})\big). $$

Here $\mathbf{B}$ and $\mathbf{R}$ are the error covariances of the background and of the observations, and $H$ is the **observation operator**. For a satellite sounder, $H$ is a radiative-transfer model that computes the radiances the instrument would see through the model atmosphere (Chapter 16). The four-dimensional version, **4D-Var**, fits observations spread over a 6–12-hour window. Every term in this equation is a place where learning can help, as the section on the observing chain shows.

### Reanalysis: the Training Set

A **reanalysis** runs one fixed assimilation system over decades of archived observations. Because the system never changes, the record is consistent in time. ECMWF's **ERA5**, produced for the European Union's Copernicus Climate Change Service, covers 1940 to the present. It gives hourly fields on a 0.25° grid (about 31 km) with 137 levels from the surface to about 80 km, and many products on 37 pressure levels. Its successor, ERA6, has been in production since 2025 at about 14 km. Its first decades are due for release towards the end of 2027.

Almost every learned global model has been trained on ERA5. A typical training set holds 1979–2017 or 1979–2018 at 6-hour intervals: about 57 000 global states, each with about a million grid points and tens to hundreds of variables. Later years are kept for testing. A learned model can only be as good as the reanalysis it imitates: it inherits ERA5's errors, its smoothing of small scales and its weak points, such as rainfall.

### Chaos Sets the Limit

The atmosphere is **chaotic**: small errors grow until the forecast is no better than a guess from climate statistics. Errors in the large-scale flow double in about one to two days, so medium-range forecasts lose most of their skill after 10–15 days. A better model or analysis can push that limit outwards, but cannot remove it.

## The Machine-Learning Weather Revolution, 2022–26

The key idea of this section is that within three years learned models went from first papers to running beside physics models in operations. They matched or beat the best physics models on most standard scores, at a tiny fraction of the computing cost.

### Landmark Models

@tbl:mlwxmodels lists the models that set the pace. **FourCastNet** (NVIDIA and partners, February 2022) produced a week-long global forecast at 0.25° in under two seconds. It matched ECMWF's physics model only at short lead times and for large-scale variables, but it showed what was possible. **Pangu-Weather** (Huawei, published in *Nature* in July 2023) was the first learned model reported to beat ECMWF's deterministic forecast on its main scores. It used a transformer that treats pressure levels and surface fields as one three-dimensional volume. **GraphCast** (Google DeepMind, *Science*, November 2023) was more accurate than ECMWF's high-resolution forecast (HRES) on 90 % of 1 380 verification targets. It made a 10-day forecast in under one minute on a single Google TPU v4 chip.

| Model | Developer, year | Architecture | Grid and step | Range | Status, October 2026 |
|---|---|---|---|---|---|
| FourCastNet | NVIDIA and partners, 2022 | Fourier neural operator | 0.25°, 6 h | About 1 week | Research; later versions in NVIDIA Earth-2 |
| Pangu-Weather | Huawei, 2023 | 3D transformer | 0.25°, 13 levels | 7 days and more | Research; run experimentally at ECMWF until May 2026 |
| GraphCast | Google DeepMind, 2023 | Graph network on a multi-mesh | 0.25°, 37 levels, 6 h | 10 days | Open; basis of NOAA's AIGFS |
| FengWu | Shanghai AI Laboratory and partners, 2023 | Multi-modal transformer | 0.25°, 37 levels | Useful to 10.75 days | Research |
| FuXi | Fudan University, 2023 | Cascade of three transformers | 0.25°, 6 h | 15 days | Research |
| NeuralGCM | Google, 2024 | Physics core plus learned physics | 2.8°–0.7° | Days to decades | Research; open |
| GenCast | Google DeepMind, 2024 | Diffusion ensemble | 0.25°, 12 h | 15 days, 50 members | Research; followed by WeatherNext 2 (2025) |
| Aurora | Microsoft, 2025 | 1.3-billion-parameter foundation model | 0.25° and 0.1° | 10 days; air quality, waves | Open; run experimentally at ECMWF until May 2026 |
| AIFS Single and ENS | ECMWF, 2024–25 | Graph encoder and decoder, transformer processor | 28–31 km, 6 h | 15 days; ENS 51 members | Operational since February and July 2025 |
| Aardvark Weather | Cambridge, Turing Institute, Microsoft, ECMWF, 2025 | End to end from observations | 1.41°, 5 levels | 10 days | Research |

: Landmark machine-learning global weather models. Ranges and grids are those of the first published versions. {#tbl:mlwxmodels}

Two further steps followed. **GenCast** (Google DeepMind, *Nature*, December 2024) produced ensembles instead of single forecasts. It was more skilful than ECMWF's physics ensemble (ENS) on 97.2 % of 1 320 targets, and on 99.8 % beyond 36 hours. Each 15-day member took about 8 minutes on one TPU v5 chip. **NeuralGCM** (Google, 2024) kept a differentiable physics core for the large-scale flow and learned only small-scale processes such as clouds. It stays stable over decades, so it can also simulate climate.

Foundation models followed (Chapter 44). **Aurora** (Microsoft, *Nature*, May 2025) was pre-trained on over a million hours of weather and climate data, then fine-tuned for forecasts at 0.1°, air pollution, ocean waves and cyclone tracks. In November 2025 Google DeepMind released **WeatherNext 2**. Its **functional generative network** injects random noise inside the network, so each run gives a different but realistic forecast. It makes hundreds of scenarios in under a minute on one TPU and drives the forecasts in Google's consumer products.


### Into Operations

The decisive change came when weather centres put learned models into daily service (@tbl:mlwxops). "Operational" means run every day on a fixed schedule, monitored, and delivered to users with a service commitment. In every case the learned model runs **beside** the physics model, not instead of it.

ECMWF built its own model (see the box below); NOAA started from an outside one. Through its Project EAGLE, it fine-tuned GraphCast on analyses from its own assimilation system. Of its three models of December 2025, **AIGFS** is a single forecast with better cyclone tracks but weaker intensity than the physics GFS. **AIGEFS** is a 31-member learned ensemble that needs about 9 % of the computing of the physics ensemble. **HGEFS** joins 31 physics and 31 learned members into one 62-member "grand ensemble" — the first such hybrid in operations, NOAA believes.

| Centre | System | In service | How it was built | Notes |
|---|---|---|---|---|
| ECMWF (Europe) | AIFS Single | 25 Feb 2025 | Own graph–transformer model, Anemoi software | 28 km, 4 runs a day to 15 days; open data; v2 on 12 May 2026 added waves |
| ECMWF | AIFS ENS | 1 Jul 2025 | Trained on CRPS | 50 members plus control, 31 km |
| NOAA (USA) | AIGFS, AIGEFS, HGEFS | Dec 2025 | GraphCast fine-tuned on NOAA analyses | 16-day forecast in about 40 min with 0.3 % of GFS computing; 31-member AI ensemble; 62-member hybrid |
| DWD (Germany) | AICON | Runs since Sep 2025; fully operational 2 Mar 2026 | Graph network built with Anemoi | About 13 km, to 180 h |
| CMA (China) | Fengqing | 2025 | With Tsinghua University | Rain skill comparable to physics models to 10 days |
| Met Office (UK) | FastNet | Not yet | With the Alan Turing Institute | Research; similar RMSE to the Met Office global model (2026) |

: Machine-learning global models at national and international centres, October 2026. {#tbl:mlwxops}

::: history
**Landmark: ECMWF's AIFS goes operational (2025–26)**

- **25 February 2025.** ECMWF put its **Artificial Intelligence Forecasting System (AIFS)** into operations, the first data-driven global model in service at a major international centre. It runs at 28 km beside the 9 km physics model (IFS). ECMWF reported gains of up to 20 % on some scores, including cyclone tracks, and about 1 000 times less energy per forecast.
- **Design.** A graph network maps the input grid onto an internal grid of about 1°, a transformer steps it forward 6 hours, and a decoder maps it back. Pre-trained on ERA5 (1979–2020) and fine-tuned on operational analyses, it trained in about a week on 64 GPUs. A 10-day forecast takes about 2.5 minutes on one GPU.
- **1 July 2025.** **AIFS ENS** followed: a 51-member ensemble trained on the continuous ranked probability score. ECMWF reported gains over the physics ensemble of up to 20 % for surface temperature.
- **12 May 2026.** Version 2 of both arrived with the physics model's new cycle, 50r1, and added ECMWF's first operational data-driven wave forecasts. The ensemble was re-tuned on analyses from the new cycle, because the learned model degrades when its starting analyses change.
- **Open by design.** AIFS forecasts are free open data (CC-BY-4.0). Its training software, Anemoi, is shared with national services; Germany's AICON is built on it.
:::

### Learning Directly from Observations

All the models above start from an analysis made by physics-based assimilation. The next step is to learn the whole chain. **Aardvark Weather** (Cambridge, the Alan Turing Institute, Microsoft Research and ECMWF; *Nature*, 2025) takes in raw data from scatterometers, sounders, geostationary imagers, stations, ships and radiosondes. It outputs forecasts on a 1.41° grid and for individual stations in about one second on four GPUs; ECMWF's physics system needs about 1 000 node-hours for assimilation and forecast. Using about 10 % of the input data of operational systems, it beat NOAA's GFS on many variables but trailed ECMWF's HRES in the upper atmosphere and at short range.

ECMWF's **GraphDOP** (2024–25) learns from satellite and in-situ observations alone and was skilful to about five days in its first version. A Google DeepMind preprint of September 2026, **WeatherNext 3**, ingests low-latency geostationary images and predicts station temperatures anywhere. These systems are research, but they could free learned forecasting from its dependence on physics-based analyses.

## How Learned Weather Models Work

The key idea of this section is that a learned weather model is a function that maps today's state to the state a few hours later. It is trained by comparing millions of its predictions with reanalysis, then applied again and again to reach the desired lead time.

### The Forecast as a Learned Time Step

Let $\mathbf{X}_t$ be the global state at time $t$: temperature, wind, humidity and geopotential on every level, plus surface fields. A learned model $f_\theta$ with parameters $\theta$ predicts the change over one step $\Delta t$, usually 6 hours:

$$ \hat{\mathbf{X}}_{t+\Delta t} = \mathbf{X}_t + f_\theta(\mathbf{X}_t, \mathbf{X}_{t-\Delta t}). $$

A 10-day forecast applies the model 40 times, each time feeding its own output back in. This is called an **autoregressive roll-out**. Predicting the change rather than the full state makes learning easier, because most of the atmosphere changes little in 6 hours.

Training minimises a weighted mean squared error between the model output and reanalysis over many past dates:

$$ \mathcal{L}(\theta) = \frac{1}{N} \sum_{\text{dates}} \sum_{j=1}^{J} \sum_{i,v,\ell} a_i \, w_v \, w_\ell \left(\hat{x}^{(j)}_{i,v,\ell} - x^{(j)}_{i,v,\ell}\right)^2 . $$

Here $i$ labels grid points, $v$ variables and $\ell$ levels. The **area weight** $a_i \propto \cos(\text{latitude})$ stops the crowded grid points near the poles from dominating. The weights $w_v$ and $w_\ell$ set how much each variable and level matter. The sum over $j$ covers several roll-out steps: fine-tuning on 2–12 steps teaches the model to correct its own errors, but also makes its forecasts smoother.

### Graphs, Transformers and Meshes

The network inside $f_\theta$ must let information travel across the globe. **Graph neural networks** (Chapter 44) pass messages between the nodes of a mesh. GraphCast and AIFS use an **encode–process–decode** structure (@fig:graphmesh). An encoder maps the latitude–longitude grid onto an internal mesh, a processor exchanges messages along its edges many times, and a decoder maps the result back as the predicted change. GraphCast's **multi-mesh** keeps the edges of every refinement level of an icosahedron, from 12 nodes up to 40 962. Long edges carry information quickly across the globe; short edges resolve local detail.

![(a) An icosahedral multi-mesh computed by repeated subdivision: each level splits every triangle into four, and the multi-mesh keeps the edges of all levels. (b) The encode–process–decode structure of a graph weather model and its autoregressive roll-out.](figures/out/ch47_mesh.svg){#fig:graphmesh width=96%}

**Transformers** (Chapter 44), used by Pangu-Weather, FuXi and Aurora, let patches of the globe attend to each other, usually within local windows to save memory. **Neural operators**, such as FourCastNet's, learn in Fourier or spherical-harmonic space. Once trained on enough data, all three designs reach similar skill; they differ mainly in memory and speed.

### Ensembles: Diffusion and CRPS Training

A single forecast trained on mean squared error has a known flaw. When the future is uncertain, the forecast that minimises squared error is the **average of all possible futures**. An average is smooth: a storm that may go left or right is forecast as a weak storm in the middle. The fix is to forecast a probability distribution, as physics ensembles do.

Two learned approaches are in use. **Diffusion models** (Chapter 44), as in GenCast, learn to turn random noise into a realistic weather state, step by step, conditioned on the current state. Each fresh noise sample gives another ensemble member. **CRPS training**, used by AIFS ENS and WeatherNext 2, adds noise inside the network and directly optimises the **continuous ranked probability score** of the ensemble.

$$ \mathrm{CRPS}(F, y) = \mathbb{E}\,|X - y| - \tfrac12\, \mathbb{E}\,|X - X'| $$

Here $X$ and $X'$ are independent members drawn from the forecast distribution $F$ and $y$ is what happened. The first term rewards members close to the truth. The second rewards spread between members, so the ensemble does not collapse to one forecast. For one deterministic forecast the CRPS reduces to the absolute error.

### A Learned Weather Model in Miniature

The ideas above can be tried on a small chaotic system. The **Lorenz-96 model** is a ring of 40 variables that behave like a weather quantity around a latitude circle.

$$ \frac{dx_k}{dt} = (x_{k+1} - x_{k-2})\,x_{k-1} - x_k + F , \qquad k = 1, \dots, 40 $$

The quadratic term moves "weather" around the ring, $-x_k$ damps it and $F = 8$ drives it, giving chaos. By a common convention, 0.05 time units count as 6 hours.

![A learned emulator of the chaotic Lorenz-96 system. (a) Truth and a 10-day emulator forecast as space–time diagrams. (b) Error growth for 200 forecasts: the emulator (blue) tracks the perfect physics model, beats a physics model with a 5 % forcing error (orange) and far outperforms persistence. (c) Error relative to the perfect model.](figures/out/ch47_l96.svg){#fig:l96emu width=100%}

We generated 3 000 days of 6-hourly "reanalysis" and trained a small neural network to predict the 6-hour change at each site from its 9 nearest neighbours. Like a graph model, the same network serves all sites. It has 2 881 parameters. We then ran 200 forecasts from initial states with small errors, as if from an imperfect analysis (@fig:l96emu). The learned emulator's error grew almost exactly like that of the perfect physics model: 0.74 against 0.71 after 3 days and 1.53 against 1.49 after 5 days. It beat a physics model with a 5 % error in its forcing, which reached 0.78 and 1.60. All three reached half the climatological spread after 5.5–5.7 days. Persistence — forecasting no change — was worse than climatology after just over a day. Chaos, not the model, set the limit.

The same emulator shows how ensembles help (@fig:l96ensfig). Twenty members started from perturbed analyses spread out as errors grew. After 10 days the ensemble-mean error was 2.81, against 3.56 for a single forecast. The **spread** — the scatter of the members — was 2.70. A spread close to the error of the ensemble mean means the ensemble is **well calibrated**: its uncertainty is honest. With perturbations only at the start, the spread was 4–7 % too small. Adding a little noise at each step, a crude stand-in for model error, brought spread and error to within a few per cent.

![An ensemble of the learned Lorenz-96 emulator. (a) Twenty members, their mean and the truth at one site. (b) The ensemble mean beats a single forecast, and its spread matches its error once a little model-error noise is added (green). (c) The ensemble mean loses "activity": it smooths towards climatology, as any forecast trained on squared error does.](figures/out/ch47_l96ens.svg){#fig:l96ensfig width=100%}

Panel (c) shows the price of the mean. The root-mean-square anomaly of a single forecast, its **activity**, stays at 3.6, like the truth. The ensemble mean's activity falls to 2.5 by day 10. A deterministic model trained on squared error over long roll-outs drifts towards the same smooth mean. This is why learned forecasts look blurred at long range, and why the best systems now forecast ensembles.

### Computing and Energy

Learned models are cheap to run and expensive to train (@fig:mlcost). The physics system behind ECMWF's HRES needs roughly 1 000 node-hours of a supercomputer for one assimilation and 10-day forecast. AIFS needs 2.5 minutes of one GPU, and GraphCast under a minute of one TPU. Even a 50-member GenCast ensemble needs only about 7 TPU-hours. Training is the expensive part: about 21 500 TPU-hours for GraphCast and 10 750 GPU-hours for AIFS.

![Energy for one forecast (a) and for training (b), on a logarithmic scale, from published run times and assumed power draws. A learned forecast uses thousands of times less energy, but it still needs an analysis made by the physics system.](figures/out/ch47_cost.svg){#fig:mlcost width=96%}

::: example
**Example: energy of one learned and one physics forecast**

Compare one 10-day forecast from AIFS with one from a physics model. The physics run time is not published, so it is an assumption: 100 nodes for 1 hour, at 0.6 kW per node including cooling. Assume 0.7 kW for one GPU with its share of host and cooling.

1. **Physics forecast.** E = 100 nodes × 1 h × 0.6 kW = 60 kWh.
2. **Learned forecast.** AIFS takes 2.5 min = 0.0417 h on one GPU: E = 0.0417 h × 0.7 kW ≈ 0.029 kWh, or about 105 kJ.
3. **Ratio.** 60 / 0.029 ≈ 2 000. ECMWF quotes about 1 000; the exact factor depends on the assumptions, but three orders of magnitude is robust.
4. **Training.** AIFS used about 64 GPUs for one week: 64 × 168 h × 0.7 kW ≈ 7 500 kWh. That equals about 125 physics forecasts, or two months of twice-daily runs. Training pays for itself quickly, even if repeated every year.
5. **What is not saved.** The learned forecast still starts from an analysis made by 4D-Var with the physics model; in the Aardvark paper's estimate, assimilation plus forecast take about 1 000 node-hours. Until assimilation is also learned, the saving for the whole system is far smaller than in step 3.
:::

![The Pleiades supercomputer at NASA's Ames Research Center in 2008. Physics-based weather and climate models need machines like this; learned models run on a single graphics processor once trained.](figures/photos/ch47_pleiades.jpg){#fig:pleiades47 width=60%}

## Measuring Skill Fairly

The key idea of this section is that a forecast is only as good as the test it passes. Learned models win most standard scores, but scores reward different things, and a smooth forecast can win a score while missing the storm.

### Scores

@tbl:wxscores lists the main scores. **RMSE** penalises large errors and rewards smooth forecasts. The **anomaly correlation coefficient (ACC)** measures how well the pattern of departures from climate is forecast:

$$ \mathrm{ACC} = \frac{\sum_i a_i (f_i - c_i)(o_i - c_i)}{\sqrt{\sum_i a_i (f_i - c_i)^2 \, \sum_i a_i (o_i - c_i)^2}} , $$

where $f$, $o$ and $c$ are forecast, observation and climatology, and $a_i$ are area weights. By convention, a 500 hPa height forecast with ACC above 0.6 still has useful skill.

| Score | What it measures | Typical use |
|---|---|---|
| RMSE | Size of errors; rewards smooth forecasts | Every variable and lead time |
| Anomaly correlation (ACC) | Pattern of departures from climate | 500 hPa height; useful while above 0.6 |
| CRPS | Accuracy and sharpness of a probability forecast | Ensembles; for one forecast equals absolute error |
| Spread–error ratio | Whether ensemble uncertainty is honest | Ensembles; ideal value 1 |
| Track and intensity error | Kilometres to the observed centre; wind or pressure error | Tropical cyclones |
| Critical success index (CSI) | Hits ÷ (hits + misses + false alarms) above a threshold | Rain, nowcasting |
| Power spectrum | Energy at each spatial scale | Detecting blurring |

: Common scores for weather forecasts. {#tbl:wxscores}

### Where Learned Models Win

On the scores of the WeatherBench 2 benchmark and the centres' own verification, the best learned models beat the best physics models for most upper-air variables from day 1 to day 10. The gains are largest for large-scale patterns, such as 500 hPa height, and for tropical-cyclone tracks, which depend mainly on the steering flow. Learned forecasts also jump around less from run to run, as DWD found for AICON.

::: data
**Data box — an AI model at the National Hurricane Center, 2025**

- In June 2025 Google DeepMind and Google Research opened Weather Lab, with an experimental cyclone model generating 50 scenarios out to 15 days. US National Hurricane Center forecasters saw its forecasts live throughout the season, beside the physics models.
- The 2025 Atlantic season had three Category 5 hurricanes, including Melissa (@fig:melissa47).
- NHC's verification report, published in spring 2026, found that the model's ensemble mean "slightly outperformed" the official Atlantic track forecasts at 12–72 hours. Its intensity forecasts had skill comparable to the official ones.
- In the eastern Pacific it did better still: between 48 and 120 hours it beat all other individual models, the official forecast and the consensus aids.
- The official forecasts themselves beat their 2020–24 average at all lead times. The learned model was one input to human forecasters, not a replacement.
:::

![Category 5 Hurricane Melissa about 80 km south of Jamaica, photographed from the International Space Station on 28 October 2025. Learned models forecast the tracks of such storms well; their peak intensity is harder.](figures/photos/ch47_melissa.jpg){#fig:melissa47 width=72%}

### Where They Fall Short

**Smoothing.** Models trained on squared error lose small-scale detail with lead time (@fig:l96ensfig). Their power spectra fall below the real atmosphere's at scales under a few hundred kilometres, so fronts broaden and rain spreads into drizzle.

**Extremes.** In a study of Storm Ciarán (November 2023), four learned models placed the storm well but all underestimated its peak winds, which gusted to 111 knots (about 205 km/h) in Brittany. A 2025–26 study of record-breaking heat, cold and wind found that ECMWF's HRES beat GraphCast, Pangu-Weather and FuXi at nearly all lead times. The learned models underestimated how often and how far records were broken. A model trained on the past struggles with states it has never seen — a growing problem as the climate warms.

**Intensity.** Learned models tend to underestimate the peak winds of tropical cyclones. A 0.25° grid is too coarse to resolve an eyewall, and the training data are themselves smooth. NOAA's AIGFS 1.0 and its hybrid ensemble were both weaker on intensity than their physics counterparts.

**Physical consistency.** Nothing forces a learned model to conserve mass or energy, or to keep winds balanced with pressure. Outputs are mostly close to balance because the training data are, but small errors matter when the output drives other models. Learned models also lack many of the hundreds of fields, such as cloud ice or radiation fluxes, that physics models provide.

**Dependence on analyses.** A learned model inherits every error of its starting analysis; ECMWF's ensemble had to be re-tuned when the physics assimilation changed in 2026. A system of learned models alone would still need the satellites, the assimilation and the physics model that create its inputs.

::: note
**Practice: evaluating a learned weather model fairly against a physics baseline**

1. **Fix the test period.** Use at least one full year, preferably two, that the model never saw in training or validation.
2. **Use the same starting point.** Start both models from the same analysis, or verify each against its own analysis and against observations. Verifying a model against the analysis it was trained to imitate flatters it.
3. **Match the resolution.** Compare on a common grid. Coarsening a high-resolution physics forecast removes its small-scale "double penalty" and makes the comparison fair.
4. **Score probabilistically.** Use CRPS and spread–error ratio for ensembles, RMSE and ACC for single forecasts. Report by region, season and lead time, with confidence intervals.
5. **Check the physics.** Plot power spectra, check mass and energy budgets, and look at balance between wind and pressure.
6. **Test the extremes.** Score storms, heatwaves and records separately, against station observations. Use event-based scores (CSI, hit rate) and tropical-cyclone track and intensity errors.
7. **Read real cases.** Have forecasters examine high-impact cases side by side. Track run-to-run consistency.
8. **Count the whole cost.** Include the assimilation that makes the analysis, the training and the retraining, not only the run time.
:::

## Machine Learning in the Observing Chain

The key idea of this section is that learning is useful long before the forecast model. It helps turn raw satellite signals into usable quantities, correct biases, speed up the physics inside assimilation, and forecast the next few hours.

### Retrievals from Satellites

A **retrieval** estimates a geophysical quantity, such as rain rate, from what an instrument measures. Geostationary imagers see cloud tops every 5–15 minutes but not the rain beneath. Microwave instruments in low orbit see the rain but pass only a few times a day (Chapter 16). Neural networks have linked the two since the 1990s. PERSIANN ("precipitation estimation from remotely sensed information using artificial neural networks") maps infrared cloud-top temperatures to rain rate, trained on microwave and radar estimates. Multi-satellite products such as NASA's IMERG have used such estimates to fill gaps between microwave passes.

Deep networks now use several channels and the pattern of clouds. GREMLIN, from Colorado State University's CIRA, turns GOES imagery and lightning data into synthetic radar maps. Assimilating them improved 12-hour forecasts over the mountainous western United States, where radar coverage is poor. It remained research in 2025.

**Tropical-cyclone intensity** from satellites still relies largely on the **Dvorak technique**: a trained analyst matches cloud patterns to an intensity scale. When only satellite estimates exist, the National Hurricane Center puts their uncertainty at 10–20 %. Convolutional networks trained on infrared and microwave images, with aircraft reconnaissance as ground truth, can make the estimate objective and repeatable. Most such networks are still research tools.

### Bias Correction, Quality Control and Fast Observation Operators

Every satellite channel has biases that drift with orbit, temperature and age. Operational 4D-Var corrects them with **variational bias correction**, using a few predictors per channel. Neural networks can learn more complex, state-dependent biases and flag radiances contaminated by cloud, a task now done with hand-tuned thresholds. Both remain mostly research.

The observation operator $H$ is costly: a radiative-transfer model runs for every observation in every iteration of 4D-Var. A network trained on that model can reproduce it many times faster, especially for cloudy and rainy scenes. It must also give accurate derivatives, because 4D-Var follows the gradient of $J$. Such emulators are a step towards learned assimilation (@tbl:obschainml).

| Task | Classical method | Learned approach | Status, 2026 |
|---|---|---|---|
| Rain from geostationary infrared | Cloud-top temperature thresholds | Neural networks since PERSIANN (1997); deep networks on many channels | Used in products; deep versions in research |
| Synthetic radar where radar is missing | None | Convolutional network on imager and lightning data (GREMLIN) | Research and demonstration |
| Tropical-cyclone intensity | Dvorak pattern matching | Convolutional networks on infrared and microwave images | Research |
| Radiance bias correction | Variational bias correction | Neural networks with state-dependent predictors | Research |
| Observation operator | Radiative-transfer models | Network emulators with accurate gradients | Research |
| Nowcasting rain, 0–2 h | Optical-flow extrapolation | Generative networks (DGMR, NowcastNet), MetNet-3 | MetNet-3 in Google products; others research |

: Machine learning in the observing and assimilation chain. {#tbl:obschainml}

### Nowcasting

A **nowcast** forecasts the next 0–6 hours, mainly for rain and storms. Physics models need time to "spin up" storms, so for the first hours the best tool has long been **extrapolation**: estimate how radar echoes move, then move the latest image along. The motion is found by **optical flow**, which assumes that rain is carried along unchanged.

$$ \frac{\partial R}{\partial t} + \mathbf{u}\cdot\nabla R = 0 , \qquad \hat{R}(\mathbf{r}, t + n\Delta t) = R(\mathbf{r} - n\,\mathbf{u}\,\Delta t,\; t) $$

The first equation defines the motion field $\mathbf{u}$, found by optimisation as the shift that best matches successive images. The second moves the latest image along $\mathbf{u}$. Systems based on this idea, such as STEPS and the open-source pySTEPS, run at many weather services.

@fig:nowcastcsi tests it on a synthetic radar field. Rain cells of many sizes grow and decay, small cells faster than large ones, while the whole field moves at 39 km/h. We estimated the motion by block matching across three pairs of frames. At 60 minutes, extrapolation reached a critical success index (CSI) of 0.42 for rain above 1 mm/h, against 0.33 for persistence. Extrapolation with the true motion reached 0.47, so the motion estimate cost a little skill. For heavy rain above 5 mm/h, the CSI fell to 0.18, because small intense cells die quickly.

![Nowcasting a synthetic advecting rain field. (a) The field now with estimated motion vectors, the truth 60 minutes later, the optical-flow extrapolation and a learned blend. (b) Critical success index for rain above 1 mm/h (solid) and 5 mm/h (dashed). (c) RMSE: the learned blend has the lowest error but loses heavy rain.](figures/out/ch47_nowcast.svg){#fig:nowcastcsi width=100%}

We then trained a simple learned correction. A regression predicted future rain from the extrapolated field smoothed at four scales, by minimising squared error on earlier frames. It had the lowest RMSE at every lead time: 3.27 mm/h at 60 minutes against 3.69 for extrapolation. Yet it scored worse on the CSI: at 60 minutes only 0.05 for heavy rain, against 0.18 for extrapolation. Squared-error training spreads rain into a smooth, light field, so intense cores vanish. This is the nowcasting version of the blurring seen in @fig:l96ensfig.

Deep-learning nowcasts face the same trap; the leading ones avoid it with generative training. **DGMR**, from DeepMind and the Met Office (*Nature*, 2021), makes sharp 90-minute forecasts from 20 minutes of radar. More than 50 Met Office meteorologists ranked it first in 89 % of cases. **NowcastNet** (Tsinghua University, *Nature*, 2023) joins a physical advection scheme to a generative network; 62 Chinese meteorologists ranked its 3-hour forecasts first in 71 % of cases. Google's **MetNet-3** (2023) forecasts rain, temperature and wind up to 24 hours ahead at 1–4 km from radar, satellite and station data. It runs in Google products for the United States and 27 European countries. NVIDIA's **StormScope** (January 2026) forecasts storms 0–6 hours ahead directly from geostationary images.

## Climate: Emulators, Downscaling and Digital Twins

The key idea of this section is that climate questions differ from weather questions. They ask about statistics over decades under conditions that have never occurred. Learning helps where it can be checked against physics, and is dangerous where it must extrapolate.

### Climate Emulators

A **climate emulator** is a fast learned model that imitates an expensive climate model. **Full emulators** step the atmosphere forward like a weather model but stay stable for centuries. ACE2, from the Allen Institute for AI, was trained on ERA5 and physics-model output and runs about 1 500 simulated years per day on one GPU at 1°. A coupled atmosphere–ocean version, SamudrACE, followed in 2025. **Reduced emulators** map emission scenarios to global or regional warming, so thousands of scenarios can be explored.

The danger is **extrapolation**. A weather model sees the same kinds of state in training and in use. A climate model is asked about a world warmer than anything in its training data. @fig:ebmemu shows what can happen. The "truth" is a two-layer **energy-balance model**: an upper ocean and atmosphere of heat capacity $C$, coupled to a deep ocean of heat capacity $C_d$.

$$ C \frac{dT}{dt} = F - \lambda(T)\,T - \gamma (T - T_d), \qquad C_d \frac{dT_d}{dt} = \gamma (T - T_d) $$

Here $F$ is the radiative forcing, $\lambda$ the climate feedback, which weakens slightly as the planet warms, and $\gamma$ the exchange with the deep ocean. Its equilibrium warming for doubled CO₂ is 3.7 K. We trained two emulators on three runs with forcing up to 3.7 W/m²: a historical run, a 1 % per year rise in CO₂ to doubling, and an abrupt doubling. Both emulators see the forcing smoothed over 1–400 years. One is linear, like a physical response function. The other is a small neural network (MLP).

![Emulating a two-layer energy-balance climate model. (a) Training forcing (black and shaded range) and two unseen test scenarios. (b) Under high forcing, outside the training range, the neural-network emulator (orange) fails, while the linear response emulator (blue) stays close. Adding an abrupt 4×CO₂ run to training (violet) fixes the network. (c) In an overshoot scenario inside the training range, all emulators work.](figures/out/ch47_climate.svg){#fig:ebmemu width=100%}

In an overshoot scenario that stayed within the training range, all emulators reproduced the truth to within 0.06 K. In a high-forcing scenario reaching 8.5 W/m² by 2100, the true warming was 5.47 K. The linear emulator gave 5.19 K: close, but low, because it cannot know that the feedback weakens. The neural network gave only 3.11 K. Its tanh units had saturated outside the range they were trained on. When an abrupt 4×CO₂ run was added to training, the network gave 5.36 K. The lesson applies to every learned climate model: **train on the conditions you will predict**, prefer structures that respect physics, and test outside the training range on purpose.

### Downscaling

Global models run at 10–100 km; impacts happen at 1 km. **Downscaling** fills the gap. Statistical downscaling regresses local weather on large-scale predictors. **Generative downscaling** adds realistic small-scale detail, giving many possible fine fields for one coarse input. NVIDIA's CorrDiff, trained with data from Taiwan's Central Weather Administration, maps 25 km ERA5 fields to about 2 km: a network predicts the mean field and a diffusion model adds the detail. The output must be checked against stations, because a network can invent convincing but false detail.

### Satellite Climate Records and Extremes

Learning from observations needs long, stable records. ESA's **Climate Change Initiative (CCI)** reprocesses decades of satellite data into over 100 consistent data sets, covering many of the 54 **essential climate variables** of the Global Climate Observing System. They are used to train and test learned models and to detect change. Statistical learning can even find the fingerprint of global warming in a single day's weather pattern. For **attribution** of extremes, learned models can generate thousands of plausible seasons to estimate how much more likely a heatwave has become. Their answers are only as good as their behaviour in the tails, which must be tested separately.

### Digital Twins of the Earth

A **digital twin** is a model kept in step with observations that users can query: "what if this heatwave happened in a world 2 °C warmer?". The EU's **Destination Earth**, run by ECMWF, ESA and EUMETSAT, has a Climate Change Adaptation twin and a Weather-Induced Extremes twin, both at kilometre scale. Phase 2 added learned components for land, ocean, sea ice, waves and hydrology. Phase 3 (June 2026–June 2028) will couple them into a European learned Earth-system model. NVIDIA's **Earth-2** is a platform of open models (@tbl:climateml); in January 2026 it added a 15-day model and a storm nowcaster.

| System | Developer, year | What it does | Status, October 2026 |
|---|---|---|---|
| ClimaX | Microsoft and partners, 2023 | Foundation model pre-trained on climate-model output | Research |
| ACE2, SamudrACE | Allen Institute for AI and partners, 2024–25 | Emulates atmosphere (and ocean) at 1°, about 1 500 years a day on one GPU | Research; open |
| NeuralGCM | Google, 2024 | Hybrid physics–learned model, stable for decades | Research; open |
| CorrDiff | NVIDIA, 2024 | Generative downscaling, 25 km to about 2 km | Open; developed with Taiwan's weather agency |
| Destination Earth | EU: ECMWF, ESA, EUMETSAT, 2022– | Kilometre-scale climate and extremes twins with learned parts | Phase 3, June 2026–June 2028 |
| Earth-2 | NVIDIA, 2024– | Platform of open weather and climate models | New models released January 2026 |
| ESA CCI | ESA, 2010– | Over 100 satellite climate data sets | Operational archive |

: Learning in climate science: selected systems. {#tbl:climateml}

## Space Weather

The key idea of this section is that space weather has the same forecasting needs as the weather, with far fewer observations. That makes machine learning attractive and also risky. The Sun is watched by a handful of spacecraft, and big storms are rare.

### Why Space Weather Is Hard to Learn

Space weather (Chapter 22) runs from the Sun to the ground. A flare or coronal mass ejection (CME) leaves the Sun. The solar wind carries it to the Earth in one to four days. It reaches the L1 monitors about an hour before the Earth. It then drives currents in the magnetosphere and ionosphere (Chapter 23). Each link has its own data and forecasting problem (@tbl:swml).

| Task | Main inputs | Typical learned method | Reported skill | Status |
|---|---|---|---|---|
| Solar flares (24 h) | Magnetogram features or images | SVM, CNN, foundation models | TSS about 0.5–0.8 in research | Research; human-led forecasts in operations |
| CME arrival time | Coronagraph images, CME speed | Regression, CNN | Mean absolute error 6–12 h on research samples | Research |
| Solar-wind speed at L1 | Solar EUV images | CNN with LSTM | RMSE 72–82 km/s, 4 days ahead | Research |
| Ground magnetic disturbance | L1 solar wind | Recurrent and graph networks (DAGGER) | 30 min ahead, worldwide | Research demonstration |
| Kp and Dst indices | L1 solar wind, past index | Neural networks, LSTM, Gaussian processes | Kp ensemble up to 72 h (GFZ) | Some products |
| Ionosphere (TEC) | GNSS maps, solar indices | LSTM, ConvLSTM | Better than climatological models in studies | Research |
| Radiation belts | Particle data, solar wind | Neural networks | Electron flux forecasts in studies | Research |

: Machine learning for space weather (selected tasks). TSS: true skill statistic. {#tbl:swml}

Three things make learning hard. Data are few: the best magnetograms, from the Solar Dynamics Observatory (SDO), cover only since 2010, about one and a half solar cycles. Events are rare: there are only a few dozen great storms in the whole space age. And the key quantity for geomagnetic storms, the north–south component of the magnetic field in a CME ($B_z$), cannot be measured until the CME reaches L1.

### Flare Forecasting from Magnetograms

Large flares come from active regions with strong, twisted magnetic fields, mapped by SDO's Helioseismic and Magnetic Imager (HMI). Features computed from each map include the total unsigned flux, the flux near the **polarity inversion line** where the field changes sign, electric currents and shear. These features, or the images themselves, feed a classifier that gives the probability of an M- or X-class flare in the next 24 hours.

Flares are rare, so accuracy is useless as a score. A model that always says "no flare" can be 98 % accurate. Flare forecasts are compared with the **true skill statistic** (Chapter 43):

$$ \mathrm{TSS} = \frac{\text{hits}}{\text{hits} + \text{misses}} - \frac{\text{false alarms}}{\text{false alarms} + \text{correct negatives}} , $$

the probability of detection minus the probability of false detection. It ranges from −1 to 1 and does not depend on how common flares are in the sample. In 2015 Bobra and Couvidat reached TSS 0.76 with a support vector machine on HMI features, though only about 42 % of its flare warnings came true. A 2019 comparison of operational systems over 2016–17 found that most scored above "no skill", with TSS values roughly from 0 to 0.5. No method was best on every score.

@fig:flaretss shows the method on synthetic data. A hidden "free energy" drives five magnetogram-like features and the chance of a flare, with an unobserved trigger added. The flare rate is 2 %. A logistic regression reached a maximum TSS of 0.68, and gradient-boosted trees 0.66. Panel (c) shows why TSS is used. Keep the detection and false-alarm rates fixed: TSS stays constant, but precision rises from 2.5 % at a 0.5 % event rate to 56 % at 20 %. Scores like precision and the Heidke skill score (HSS) cannot be compared between solar maximum and solar minimum.

![Flare forecasting on synthetic magnetogram features. (a) ROC curves for logistic regression and gradient boosting. (b) TSS and HSS against the decision threshold. (c) At fixed detection and false-alarm rates, TSS does not depend on the event rate; precision and HSS do.](figures/out/ch47_flare.svg){#fig:flaretss width=100%}

::: example
**Example: the true skill statistic from a flare contingency table**

The logistic model of @fig:flaretss was tested on 16 000 region-days, of which 315 had an M-class or larger flare. At its best threshold it gave 268 hits, 47 misses, 2 635 false alarms and 13 050 correct negatives.

1. **Probability of detection.** POD = 268 / (268 + 47) = 0.851.
2. **Probability of false detection.** POFD = 2 635 / (2 635 + 13 050) = 0.168.
3. **True skill statistic.** TSS = 0.851 − 0.168 = 0.683.
4. **Precision.** 268 / (268 + 2 635) = 0.092: only about 1 warning in 11 is followed by a flare.
5. **Accuracy.** (268 + 13 050) / 16 000 = 0.832. A forecast of "never" scores 0.980 but has TSS 0.
6. **Heidke skill score.** HSS = 2(ad − bc) / [(a + c)(c + d) + (a + b)(b + d)] = 0.136, with a–d the hits, false alarms, misses and correct negatives. False alarms keep it low.
7. **Meaning.** A high TSS shows that the model separates flaring from quiet regions, not that its warnings are usually right. Users who pay for false alarms should choose a higher threshold.
:::

Since 2018 deep networks have learned directly from magnetogram and extreme-ultraviolet images, with results similar to feature-based methods on small samples. The NASA–IBM **Surya** foundation model (August 2025) was pre-trained on about 218 TB of SDO data. Fine-tuned for flares, it beat existing benchmarks by about 16 % in preliminary tests (Chapter 44).

::: figrow
![The largest sunspot group of solar cycle 24, active region 12192, seen by SDO in October 2014. It produced six X-class flares, none of which launched a coronal mass ejection.](figures/photos/ch47_sunspot.jpg){#fig:ar12192}

![Magnetic loops above a fast-growing active region in extreme-ultraviolet light, imaged by SDO in June 2018. Flare forecasts learn from the magnetic fields beneath such loops.](figures/photos/ch47_activeregion.jpg){#fig:arloops47}
:::

Region 12192 (@fig:ar12192) is a warning about labels. It produced 6 X-class, 22 M-class and 53 C-class flares in one disk passage, yet none of its X-class flares launched a CME. A model trained to predict flares would rate it highly. A model trained to predict geomagnetic storms should not.

### CMEs and the Solar Wind

Forecasting when a CME will arrive is still hard. NASA's Community Coordinated Modeling Center collects real-time forecasts from many teams in its CME Scoreboard. A 2024 re-analysis found a mean absolute arrival-time error of 13.2 hours, a standard deviation of 17.4 hours and a bias of −2.5 hours (slightly early), little better than in 2013. Learned models report 6–12 hours on their own samples, such as 5.9 hours for a support vector machine on 182 CMEs and 9.75 hours for an ensemble on 363 CMEs. The samples differ, so the numbers cannot be compared directly.

Networks can also forecast the background solar wind. Coronal holes in extreme-ultraviolet images release fast wind that reaches the Earth 3–4 days later. An image network combined with a recurrent network forecast the wind speed at L1 four days ahead with an RMSE of 82 km/s; a later study reached 72 km/s. The physics-based WSA–Enlil model remains the operational standard.

### Geomagnetic Indices

Once the solar wind reaches L1, forecasts become much better, because the driver is measured. The **Dst index** measures the ring current that weakens the field at low latitudes during storms. **Kp** measures disturbance at mid-latitudes on a 0–9 scale (Chapter 22). A classic physics-based model links Dst to the solar-wind electric field $VB_s$, the solar-wind speed times the southward magnetic field:

$$ \frac{d\,\mathrm{Dst}^*}{dt} = Q(VB_s) - \frac{\mathrm{Dst}^*}{\tau(VB_s)} , $$

where $Q$ is the energy injection and $\tau$ a recovery time of several hours. Neural networks have forecast Dst and Kp since the early 1990s. Today's models include recurrent networks and Gaussian processes that also give uncertainty. GFZ in Potsdam runs a machine-learning Kp ensemble every hour, up to 72 hours ahead.

We built a synthetic test (@fig:dstfc). Four years of hourly solar wind, with recurring fast streams and random CMEs, drove the Dst model above. Three years were used for training and the fourth for testing; the test year held a −429 nT superstorm, stronger than any in training. With only past Dst, a linear model reduced the 3-hour-ahead RMSE from 11.1 nT for persistence to 9.4 nT. Adding L1 solar-wind data cut it to 6.9 nT, and a neural network with the same inputs to 6.1 nT. In storm hours the network's skill score against persistence, $1 - \mathrm{MSE}/\mathrm{MSE}_{\text{pers}}$, was 0.73. Most of the gain came from the L1 data; the network added a smaller step.

![Forecasting a Dst-like index from synthetic solar wind. (a) The largest test storm, beyond anything in training, with 3-hour forecasts. (b) RMSE over all test hours against lead time. (c) RMSE in storm hours. Upstream L1 data give most of the skill; a neural network adds more.](figures/out/ch47_dst.svg){#fig:dstfc width=100%}

NASA's **DAGGER** model (2023), from the Frontier Development Lab, used solar-wind data from upstream spacecraft such as ACE and Wind to forecast the ground magnetic disturbance worldwide, 30 minutes ahead. It runs in under a second and updates every minute. Its authors noted that its average errors were close to persistence and that it underestimated the strongest disturbances, near 1 000 nT. Like most work in this field, it is a research demonstration.

![An aurora with rare deep-red and purple colours over the Atlantic off Portugal, photographed from the International Space Station on 19 January 2026, during a geomagnetic storm that reached Kp 9−.](figures/photos/ch47_aurora.jpg){#fig:aurora2026 width=64%}

::: example
**Example: how much warning can an L1 monitor plus a learned model give?**

NOAA's SOLAR-1 observatory sits near L1, about 1.5 million km sunward of the Earth. Assume 4 minutes to downlink, process the data, run a learned model (under 1 s) and issue an alert.

1. **Slow wind, 400 km/s.** Travel time t = 1.5 × 10⁹ m / 4 × 10⁵ m/s = 3 750 s = 62.5 min. Warning ≈ 62.5 − 4 = 58.5 min.
2. **Fast CME, 750 km/s.** t = 2 000 s = 33.3 min; warning ≈ 29 min.
3. **Extreme CME, 1 500 km/s.** t = 1 000 s = 16.7 min; warning ≈ 13 min.
4. **What learning adds.** It cannot make the solar wind travel more slowly. It can turn the measured wind into a local forecast of ground disturbance or Kp within seconds, as DAGGER does for 30 minutes ahead at moderate speeds.
5. **Longer warnings.** A CME seen leaving the Sun gives one to four days of notice, but arrival errors of about 13 hours and the unknown $B_z$ make this a "watch", not a warning. ESA's planned Vigil spacecraft at L5 would see CMEs from the side and improve arrival times.
:::

### Ionosphere and Radiation Belts

The ionosphere delays GNSS signals in proportion to its **total electron content (TEC)** (Chapters 18 and 23). Global TEC maps from thousands of receivers form long image sequences, well suited to recurrent and convolutional networks. Studies report 1–24-hour forecasts that beat empirical models in quiet conditions but are weaker in storms, which are rare in training data. Neural networks driven by solar-wind and particle data also forecast radiation-belt electrons (Chapter 2) between the few spacecraft that measure them. Both remain mostly research.

### From Research to Operations

Operational space-weather centres have been slower than weather centres to adopt learned models. NOAA's Space Weather Prediction Center (SWPC), the Met Office Space Weather Operations Centre and ESA's Space Weather Service Network rely mainly on human forecasters. Their tools are physics models, such as WSA–Enlil and NOAA's Geospace model, and empirical rules. Learning appears in a few products, such as neural-network Kp forecasts. Three obstacles stand out: few events to validate against, the high cost of a missed storm, and the long, formal path from research to operations.

::: history
**Landmark: three decades of neural networks in space weather**

- **Early 1990s.** A group at the Swedish Institute of Space Physics in Lund began using neural networks to predict geomagnetic indices from solar-wind data. Within an ESA space-weather study around 2001 it built a real-time prototype forecast service.
- **2010s.** SDO magnetograms enabled image-based flare forecasting. Research classifiers reached TSS near 0.8; operational comparisons showed far lower skill.
- **2023.** NASA's DAGGER forecast ground magnetic disturbances worldwide 30 minutes ahead in under a second.
- **2025.** NASA and IBM released the Surya foundation model openly. NOAA's SWFO-L1 launched with NASA's IMAP on 24 September 2025, reached L1 in January 2026 and was renamed SOLAR-1 (@fig:swfo47).
- **2026.** Operational use was still limited to a few products; the bottleneck had moved from algorithms to validation and trust (Chapter 53).
:::

::: figrow
![NOAA's SWFO-L1 observatory, now SOLAR-1, being inspected at the Astrotech facility near Kennedy Space Center on 24 July 2025. It carries a coronagraph and solar-wind instruments for operational forecasts.](figures/photos/ch47_swfo.jpg){#fig:swfo47}

![The Falcon 9 carrying NASA's IMAP, the Carruthers Geocorona Observatory and SWFO-L1 at Launch Complex 39A on 22 September 2025, two days before launch.](figures/photos/ch47_imap.jpg){#fig:imap47}
:::

Space-weather forecasting will probably follow the weather path, more slowly. New monitors at L1, and later L5, will supply data, and long archives with agreed benchmarks will allow fair tests. Hybrid models that keep the physics of the solar wind and learn the rest are the most likely to earn forecasters' trust.

::: key
**Key takeaways**

- Learned weather models step the atmosphere forward 6 hours at a time and learn from ERA5 reanalysis. Since 2023 the best have matched or beaten physics models on most scores, using about a thousandth of the energy per forecast.
- ECMWF's AIFS (2025), NOAA's AIGFS, AIGEFS and HGEFS (December 2025), Germany's AICON and China's Fengqing run operationally — always beside physics models.
- Squared-error training smooths forecasts and weakens extremes; diffusion and CRPS-trained ensembles restore detail and honest uncertainty. Record extremes and cyclone intensity remain weak points.
- Learned models depend on physics-based analyses. End-to-end systems that learn from raw observations, such as Aardvark Weather and GraphDOP, are promising research.
- In the observing chain, learning helps with retrievals, bias correction, fast observation operators and nowcasting; nowcasts need generative training to keep heavy rain sharp.
- Climate emulators and downscaling are fast and useful, but learned models fail outside their training range. Digital twins such as Destination Earth combine physics and learning.
- Space weather has far less data and fewer events. Flare forecasts are compared by the true skill statistic, CME arrival errors are still about 13 hours, and L1 data plus learned models give tens of minutes of warning. Operational use is still limited.
:::

::: questions
**Review questions**

1. Explain why almost all learned weather models still depend on data assimilation and satellites, even though they replace the physics model.
2. Write the autoregressive update of a learned weather model. Why does it predict the change over 6 hours rather than the full state, and why is the loss weighted by the cosine of latitude?
3. In @fig:l96emu the learned emulator beats a physics model with a 5 % forcing error, yet all forecasts reach half the climatological spread after about 5.5–5.7 days. What limits the forecast range?
4. Why does a deterministic model trained on squared error produce smooth forecasts at long lead times? Use @fig:l96ensfig to explain how ensembles and CRPS training address this.
5. Give two reasons why the energy saving of a learned forecast is smaller for the whole forecasting system than for the forecast step alone.
6. List four weaknesses of learned weather models and a test from the Practice box that would reveal each.
7. In @fig:nowcastcsi the learned blend has the lowest RMSE but the worst CSI for heavy rain. Explain the difference and how DGMR avoided it.
8. Why did the neural-network climate emulator in @fig:ebmemu fail in the high-forcing scenario while the linear emulator did not? What would you change in its training?
9. A flare model gives 40 hits, 10 misses, 300 false alarms and 9 650 correct negatives. Compute its POD, POFD, TSS and precision. Would a satellite operator be satisfied?
10. A CME travels from L1 to the Earth at 900 km/s. With 5 minutes of processing latency, how much warning does an L1 monitor give? Why can a CME seen leaving the Sun not give a reliable warning days ahead?
:::
