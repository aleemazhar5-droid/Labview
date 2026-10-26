---
title: AI for Earth Observation
hero: ch46
abstract: Earth-observation satellites now collect far more images than people could ever look at, so most pixels are first seen by a machine. This chapter explains, from first principles and with small models trained from scratch, how AI turns pixels into information. It covers land-cover maps, objects, change, crop calendars, radar speckle, ships, floods and methane plumes. It then follows verified deployments in agriculture, forests, cities, oceans, disasters, greenhouse gases and development, as of October 2026. It describes AI on board satellites and smart tasking, the commercial analytics business and geospatial foundation models in practice. It ends with the traps — domain shift, label noise, biased samples, wrong area estimates and privacy — and how good practice avoids them.
---

Every day, Earth-observation (EO) satellites image the whole land surface several times over. Planet's fleet alone can collect about 200 million km² a day. Sentinel-1's radars see through cloud, day and night. Thermal, hyperspectral and very-high-resolution sensors add more. No team of people can inspect all of it. The images are only useful if software finds the floods, ships, fires, new buildings and methane leaks in them, quickly and reliably.

That software is increasingly **machine learning**: models whose behaviour is learned from examples rather than written as rules. This chapter shows how such models work on EO data, where they are used today, and where they fail. The hero image above shows centre-pivot fields in Kansas in a Landsat false-colour composite. Crop type, health and harvest date can all be read from such images by a trained model.

The physics of remote sensing is covered in Chapters 13–16. The learning methods themselves are explained in Chapters 43 and 44, and data and onboard hardware in Chapter 45. Weather and climate models are left to Chapter 47, and military uses to Chapter 50. Here we join the two: what a learning model needs to know about EO data, and what EO users need to know about learning models.

## From Pixels to Information

The key idea is that EO analysis is a short list of tasks — classify, segment, detect, compare, estimate — applied to images that are unlike everyday photographs. They have many spectral bands, a time dimension and an exact location on Earth. Each task has a matching family of models and a matching way to measure success (@tbl:eotaskmap).

The pipeline in @fig:eopipeline shows where the models sit. Raw data are calibrated and corrected into **analysis-ready data** (ARD) — pixels in physical units on a map grid (Chapter 13). Models turn ARD into maps, alerts and estimates. Users send back corrections and new labels, and some detections trigger new images of the same place. A growing share of the work also happens on the satellite itself.

![The EO data pipeline with AI. Each stage shrinks the data: terabytes of pixels a day become megabytes of maps and kilobytes of alerts. Three loops close the system: users supply new labels, detections cue new collections (tip-and-cue), and an onboard look-ahead camera can retask the satellite in under 90 seconds.](figures/out/ch46_pipeline.svg){#fig:eopipeline width=96%}

### What Makes EO Data Different

Four things set EO images apart from the photographs on which computer vision grew up. First, they have **many bands**: Sentinel-2 records 13, from blue to short-wave infrared, and imaging spectrometers record over 200. Second, they come in **time series**: the same field is seen every few days. Third, every pixel has a **location**, so neighbouring pixels are alike and nearby samples are not independent. Fourth, the **physics changes with the sensor**: radar measures surface roughness and moisture, not colour (Chapter 15).

Labels are scarce. A satellite can image a country in a day, but surveying land cover on the ground takes months. Many EO models are therefore trained on a few thousand labelled pixels, on labels made by other models, or on simulations (Chapter 45).

| Task | Output | Typical models | Usual metrics | EO examples |
|---|---|---|---|---|
| Scene classification | One label per image chip | CNN, vision transformer | Accuracy, F1 | Cloudy or clear; land-use type |
| Semantic segmentation | A class for every pixel | Random forest, U-Net, segmentation transformer | Overall accuracy, IoU | Land cover, floods, burn scars |
| Object detection | Boxes with labels | Faster R-CNN, YOLO, CFAR + classifier | Precision, recall, mean average precision | Ships, aircraft, vehicles |
| Instance segmentation | An outline per object | Mask R-CNN | Mask average precision | Building footprints, fields |
| Change detection | Changed pixels or objects | Siamese CNN, bi-temporal classifier | F1 of the change class | Deforestation, damage |
| Time-series classification | A label per pixel or field | Random forest, temporal CNN, attention | Accuracy, F1 | Crop type, phenology |
| Regression and retrieval | A physical quantity | Gradient boosting, CNN, physics + learning | RMSE, bias | Biomass, methane emission rate |
| Image-to-image | A new image | U-Net, GAN, diffusion model | PSNR, SSIM, task skill | Super-resolution, despeckling, SAR to optical |

: Common EO tasks, the models used for them and how they are scored. IoU is intersection over union, the overlap between mapped and true areas divided by their union. {#tbl:eotaskmap}

### Land Cover: Pixels and Neighbourhoods

**Land-cover mapping** gives every pixel a class such as water, forest, cropland or built-up land. The classic approach treats each pixel on its own. Its features are the reflectances in each band, plus indices such as the **normalised difference vegetation index**,

$$ \mathrm{NDVI} = \frac{\rho_\mathrm{NIR} - \rho_\mathrm{red}}{\rho_\mathrm{NIR} + \rho_\mathrm{red}}, $$

where $\rho$ is reflectance. Healthy plants reflect strongly in the near infrared (NIR) and absorb red light, so NDVI is high for vegetation and near zero for soil and water. A **random forest** — hundreds of decision trees, each trained on a random subset of the data, voting together (Chapter 43) — is still the workhorse for such pixel-based maps.

A pixel alone is often ambiguous. A dry field looks like bare soil, and a suburb is a mixture of roofs, roads and gardens. A **convolutional neural network** (CNN) looks at a neighbourhood instead. Each layer slides small filters over the image and sums weighted pixel values,

$$ y_{ij} = \sigma\Big(\sum_{c}\sum_{u,v} w_{c,uv}\, x_{c,\,i+u,\,j+v} + b\Big), $$

where $\sigma$ is a simple non-linear function. The filters learn textures and shapes as well as colours (Chapter 44). For whole maps, **encoder–decoder** networks such as the U-Net segment large tiles in one pass.

In @fig:eolandcover the two are compared on a synthetic six-class scene with Sentinel-2-like bands. Both models learned from 400 labelled pixels per class in the western half and were tested on all 12 800 pixels of the eastern half. The random forest on single pixels reached an overall accuracy of 80.2 %. Cropland was its weakest class, with an F1 score — the balance of precision and recall — of only 0.49, because fields at different growth stages look like grass or bare soil. A random forest given the same 5 × 5-pixel neighbourhoods reached 89.0 %. A small CNN with about 10 000 weights, written in numpy, reached 94.8 % and raised cropland F1 to 0.84. Context, not the network as such, did most of the work.

![Land-cover mapping of a synthetic scene. (a)–(d) Image, reference and two maps; models learned from the western half and were tested on the eastern half. (e) The CNN's remaining confusion is mostly cropland labelled as forest. (f) Neighbourhood information raises F1 for every mixed or textured class.](figures/out/ch46_landcover.svg){#fig:eolandcover width=98%}

The synthetic test is easier than reality: global maps reach overall accuracies of about 74–77 % (@tbl:eoproducts). But the ranking is typical. Pixel-based random forests remain strong baselines, and convolutional and transformer networks win where texture and shape matter.

### Objects: Ships, Aircraft and Buildings

**Object detection** finds each object and draws a box around it. Two-stage detectors first propose candidate regions and then classify them; one-stage detectors such as the YOLO family do both in one pass, which suits fast processing (Chapter 44). **Instance segmentation** outlines each object, which is what building-footprint maps need.

EO objects are small and rotated. A 50 m ship is five pixels long at 10 m resolution, and a car is a few pixels at 0.3 m. Detectors for EO therefore use rotated boxes, image pyramids and tiles that overlap so that objects on tile edges are not cut in half. Large public sets such as xView (over a million objects in 0.3 m images) and xBD (850 736 buildings before and after 19 disasters) made this progress possible (Chapter 45).

### Change Detection

Most EO questions are about **change**: what was cleared, flooded, built or burned. The simplest method subtracts an index between two dates and applies a threshold, for example flagging forest loss where $\Delta\mathrm{NDVI} = \mathrm{NDVI}_2 - \mathrm{NDVI}_1$ falls below −0.5. It is fast and easy to explain. But it reacts to every change in the index: harvests, seasons, haze, shadows and small misalignments between the images.

A **learned change detector** is trained on examples of the changes that matter and of those that do not. It sees both images, all bands and the local neighbourhood. Deep versions use **Siamese networks**, two copies of one encoder that process the two dates and compare their features.

The test in @fig:eochange makes the difference concrete. The task is to find forest clearings in a synthetic scene that also contains harvested fields, drying grass, haze, a cloud shadow and a one-pixel misregistration. Both methods were tuned on four other scenes. The best NDVI threshold (−0.55) found only 60 % of the cleared pixels, with a precision of 0.76 and an F1 of 0.67. A random forest on 16 bi-temporal features found 98 %, with a precision of 0.87 and an F1 of 0.92. It had learned that a drop in NDVI over a field is a harvest, not deforestation.

![Change detection on a synthetic scene where only forest clearings count as change. (a, b) False-colour images before and after. (c) An NDVI-difference threshold misses partly cleared patches and flags harvests. (d) A random forest trained on other scenes finds almost all clearings. (e) Precision, recall and F1 on the test scene.](figures/out/ch46_change.svg){#fig:eochange width=98%}

Dense time series go further. Algorithms such as CCDC and BFAST fit a seasonal curve to every pixel's history and flag a break when new data stop fitting it (Chapter 13). Operational forest alerts, described below, combine such statistics with machine learning.

### Time Series and Crop Types

Crops are best recognised by their **calendar**. Winter wheat greens up in spring and is harvested in summer. Maize and soybean start later. Grassland drops after each mowing (@fig:eocrops a). A model that sees the whole season can tell them apart even when single images cannot.

Clouds make the series irregular. One option is to fill the gaps by interpolation and give the filled series to a random forest. Another is **temporal attention**, which works directly on the clear dates. Each observation $t$ becomes a feature vector $h_t$ that encodes its value and its day of year. A learned query $q$ scores each date, and the model averages the dates with weights

$$ a_t = \frac{\exp(q \cdot k_t/\sqrt{d})}{\sum_{s\,\in\,\mathrm{clear}} \exp(q \cdot k_s/\sqrt{d})}, \qquad z = \sum_t a_t\, h_t , $$

where $k_t$ is a "key" computed from $h_t$ and $d$ its length. Cloudy dates simply drop out of the sum. The pooled vector $z$ is then classified. Garnot and colleagues' pixel-set encoder with temporal attention (2020) reached 94.2 % overall accuracy on the S2-Agri benchmark of French fields.

In @fig:eocrops both approaches are tested on synthetic NDVI series for six crops, with timing shifts and undetected thin cloud. A numpy attention network with six heads and about 5 000 weights matched a random forest on gap-filled series. Both reached 93.0 % with 20 % of dates cloudy and about 78 % with 80 % cloudy. Panel (c) shows what one head learned: it looks at early spring, which separates wheat and grass, and at early June, which separates the summer crops. On small, clean problems attention gives no free gain. Its advantages appear with large and varied training sets, many bands and irregular sampling across regions.

![Crop types from NDVI time series (synthetic data). (a) Mean seasonal curves ± one standard deviation, and the clear observations of one field. (b) Accuracy against the share of cloudy dates for a random forest on gap-filled series and a temporal-attention network. (c) Mean attention weights of one head for each crop.](figures/out/ch46_crops.svg){#fig:eocrops width=98%}

### Clouds, Sharper Images and Fusion

**Cloud and shadow masking** is the first step for any optical model, because cloud covers about two-thirds of Earth at any time. Rule-based masks such as Fmask test brightness, temperature and band ratios. Learned masks now do better. The s2cloudless detector uses gradient-boosted trees on ten Sentinel-2 bands, and CNNs trained on sets such as CloudSEN12 (49 400 patches) also find thin cloud and shadows. Missed thin cloud is a quiet source of error in every downstream product.

**Pan-sharpening** merges a sharp panchromatic band with coarser colour bands (Chapter 14). **Super-resolution** goes further and predicts detail finer than any band, for example 10 m Sentinel-2 images sharpened to 2.5 m. Networks trained on pairs of images from fine and coarse sensors learn plausible detail. But they can **hallucinate**: they may invent edges, cars or field boundaries that look real. Super-resolved images are useful for display and as model inputs, but they are not new measurements.

**Data fusion** combines sensors. Radar sees through cloud, optical data are easier to interpret, and the two together beat either alone for crops, floods and forests. Networks can even **translate** radar into optical-looking images. Such images help analysts read radar, but they must never be used as if they were observations.

### Radar: Speckle and Ships

Radar images carry **speckle**, the grainy pattern made when echoes from many small scatterers in a pixel add with random phases (Chapter 15). For a uniform surface with true reflectivity $R$, the measured intensity is

$$ I = R\, n, \qquad n \sim \Gamma(L, 1/L), $$

where $L$ is the number of independent looks averaged. A single-look image ($L = 1$) has a standard deviation equal to its mean. Smoothness is measured by the **equivalent number of looks**, $\mathrm{ENL} = \mu^2/\sigma^2$, over a uniform area.

Averaging neighbours raises ENL but blurs edges. The **Lee filter** (1980) adapts. It smooths where the image is uniform and keeps the original pixel where it is not:

$$ \hat R = \bar I + k\,(I - \bar I), \qquad k = \frac{1 - C_u^2/C_I^2}{1 + C_u^2}. $$

Here $\bar I$ is the local mean. $C_I$ and $C_u$ are the local and speckle-only coefficients of variation, the standard deviation divided by the mean. Learned filters instead train on pairs of speckled and clean images. Since real clean images do not exist, they use simulated speckle or several dates averaged together. Self-supervised methods train on speckled data alone.

In @fig:eodespeckle four filters are compared on a synthetic single-look scene. A 7 × 7 boxcar reached an ENL of 58 but blurred edges, with an error of 4.25 dB near them. The Lee filter reached an ENL of 42 and an overall error of 1.81 dB. A least-squares 9 × 9 linear filter, learned from data, cut the error to 1.49 dB. A small numpy network on the same 9 × 9 patches reached an ENL of 63 and an error of only 1.14 dB, and 2.08 dB near edges. The lesson: ENL alone rewards blurring, so always measure error near edges and small targets too.

**Ship detection** in radar is the classic EO detection task. Ships are bright metal on a darker sea. The standard detector is the **constant false alarm rate** (CFAR) test. It estimates the local sea brightness $\hat\mu$ from a ring of pixels around each test cell and declares a target when the cell exceeds $T = \alpha\hat\mu$. For exponential clutter with a known mean, the false-alarm probability is $P_{fa} = e^{-\alpha}$, so $\alpha = -\ln P_{fa}$. Real sea clutter is spikier, so $\alpha$ must be larger.

CFAR flags anything bright. Breaking waves, azimuth "ghosts" of bright objects and small islands all cause false alarms. A learned classifier can look at shape. In @fig:eoships, chips of synthetic K-distributed sea clutter contain ships 2–7 pixels long or look-alikes. At a false-alarm rate of 1 % per chip, cell-averaging CFAR found 53 % of ships, and 286 of its 300 false alarms were ghosts or wave spikes. A small numpy network found 74 %. Its area under the receiver operating characteristic (ROC) curve, which sums up performance at all thresholds, rose from 0.869 to 0.975. Its advantage was largest for weak ships, 5–11 dB above the clutter. In practice the two are chained: CFAR proposes candidates and a network confirms them.

![Speckle filtering of a synthetic single-look SAR scene. (a)–(d) Truth, speckled image, Lee filter and learned network (dB scale). (e) Equivalent number of looks in the outlined uniform region. (f) RMS error against the truth for all pixels and near edges.](figures/out/ch46_despeckle.svg){#fig:eodespeckle width=98%}

![Ship detection in synthetic SAR chips. (a) Ships at three signal-to-clutter ratios and three look-alikes. (b) ROC curves: detection probability against false alarms per chip. (c) Detection probability against ship brightness at 1 % false alarms.](figures/out/ch46_ships.svg){#fig:eoships width=98%}

### Spectra and Heights

**Hyperspectral images** record a full spectrum in each pixel (Chapter 14). Their pixels are often mixtures. The **linear mixing model** writes a pixel spectrum $x$ as

$$ x = \sum_{k} a_k\, e_k + \varepsilon, \qquad a_k \ge 0,\ \ \sum_k a_k = 1, $$

where $e_k$ are pure "endmember" spectra, such as soil, grass and roof, and $a_k$ their area fractions. **Unmixing** solves for the fractions. Learned methods add non-linear mixing and use the spatial context. Classifiers for hyperspectral data must also cope with hundreds of correlated, noisy bands and few labels. Dimension reduction and foundation models pre-trained on unlabelled cubes help (Chapter 44).

**3-D reconstruction** turns stereo pairs, radar interferometry or lidar into heights. Learned stereo matching fills gaps in shadows and on uniform roofs. Networks also estimate building heights from single images. Microsoft's building data set includes height estimates for more than 170 million buildings.

## Land: Crops, Forests, Cities and Water

On land, AI's main job is to make **wall-to-wall maps** that are updated often. Many are now free and global (@tbl:eoproducts).

| Product | Producer, first release | Input, resolution | Method | Reported quality or size |
|---|---|---|---|---|
| WorldCover | ESA, 2021 (2020 map) | Sentinel-1 and -2, 10 m, 11 classes | Supervised classifier on yearly band statistics | Overall accuracy 74.4 % (2020), 76.7 % (2021) |
| Dynamic World | Google, World Resources Institute, 2022 | Every Sentinel-2 image ≤ 35 % cloud, 10 m, 9 classes | Fully convolutional network; class probabilities | 73.8 % agreement with expert labels |
| WorldCereal | ESA consortium, 2023 (2021 maps) | Sentinel-1, -2, Landsat, 10 m | Gradient-boosted trees | Crop extent: user's 88.5 %, producer's 92.1 % |
| Global ML Building Footprints | Microsoft, 2022– | Bing Maps and Vexcel imagery, 2014–2025 | Segmentation network + polygon step | About 1.4 billion buildings; precision 92–97 % |
| Open Buildings v3 | Google, 2023 | 50 cm imagery; 58 million km² | Segmentation network | 1.8 billion buildings |
| Tree cover loss and alerts | Univ. of Maryland, Wageningen, Global Forest Watch | Landsat, Sentinel-2, Sentinel-1 | Decision trees, statistical change tests | Annual since 2000; weekly alerts |

: Global land products made with machine learning (status October 2026). {#tbl:eoproducts}

### Agriculture

**Crop-type maps** feed food-security outlooks, subsidy checks and insurance. In Europe, paying agencies use Sentinel time series to check farmers' declarations field by field. ESA's **WorldCereal** produced the first global, seasonal 10 m maps of temporary crops, maize, cereals and irrigation for 2021. Its crop-extent map had a user's accuracy of 88.5 % and a producer's accuracy of 92.1 %; crop types agreed with field data at least 80 % of the time. The maps were released in 2023 as open data and open code.

**Yield forecasting** is harder. Models combine vegetation indices through the season with weather, soil and past yields. Such models work well where long yield records exist and poorly where they do not, which is often where forecasts matter most. Field patterns like those in @fig:kazakhharvest are easy for people to read but differ greatly between regions.

::: figrow
![Fields in eastern Kazakhstan seen by Landsat 8 on 9 September 2013. Some are harvested and bare, others still green — the kind of pattern a crop-type model learns from a season of images.](figures/photos/ch46_kazakh.jpg){#fig:kazakhharvest}

![Forest loss in the Xingu basin, Brazil, from L-band radar: areas cleared before 1996 (black) and between 1996 and 2007 (red), from JERS-1 and ALOS-1 data. Radar alerts see through tropical cloud.](figures/photos/ch46_arcdefor.jpg){#fig:arcdeforest}
:::

### Forests and Deforestation Alerts

The University of Maryland's global forest-change maps processed about 654 000 Landsat scenes with decision trees in 2013. Updated every year, they are the basis of **Global Forest Watch**. Its 2025 data, released in April 2026, showed 4.3 million hectares of tropical primary forest lost. That was 36 % less than the record 6.7 million hectares of 2024, a year of extreme fires.

Annual maps are too slow for enforcement, so **alerts** were added. GLAD alerts flag new loss in each Landsat image at 30 m and later in Sentinel-2 at 10 m. The **RADD** alerts from Wageningen University use Sentinel-1 radar, which sees through the clouds that hide tropical forests for months (@fig:arcdeforest). They cover about 50 tropical countries at 10 m, with a new radar image every 6–12 days. An alert is raised from a single new radar image. It is confirmed when the disturbance probability exceeds 97.5 % within 90 days. Global Forest Watch merges these streams into "integrated alerts" used by governments, companies checking supply chains and journalists.

### Cities, Mines and Water

**Building footprints** are the base layer for population estimates, disaster planning and electrification. Microsoft has extracted about 1.4 billion footprints from aerial and satellite imagery, with regional precision of 92–97 % but recall as low as 71 % in Africa. Google's Open Buildings holds 1.8 billion detections across Africa, South and South-East Asia, Latin America and the Caribbean. Both are open and often fill gaps that community mapping has not reached.

**Mining** is a growing target. Amazon Mining Watch, from Earth Genome and partners, runs an ensemble of CNNs over Sentinel-2 to map gold mining in nine Amazon countries. Its August 2026 update reported about 99 % specificity and 90 % sensitivity, with maps updated every quarter since 2025. **Water and wetlands** are mapped from long Landsat records and from radar, which separates open water, flooded vegetation and dry land.

## Oceans and Maritime Awareness

At sea, the key question is "who is out there?" Ships are supposed to broadcast their identity and position through the **Automatic Identification System** (AIS). Many do not: their transponders are off, broken or not required. Satellite imagery finds these **"dark" vessels**, and machine learning makes it possible to do so for whole oceans.

::: history
**Mapping the dark fleet (Global Fishing Watch, 2024)**

In January 2024, Paolo and colleagues at Global Fishing Watch published the first global map of industrial vessels and offshore structures in *Nature*. They processed about 2 PB of imagery from 2017–2021: 753 030 Sentinel-1 radar scenes for vessels and about 2.5 million Sentinel-2 scenes for infrastructure. A CFAR detector proposed objects. Three deep CNNs then confirmed vessels (about 97.5 % accurate), estimated their length and separated fishing from non-fishing vessels (90.5 % accurate). Detections were matched against 53 billion AIS messages.

The study found 23.1 million vessel detections, about 63 300 vessels at sea at any moment. It concluded that 72–76 % of the world's industrial fishing vessels and 21–30 % of transport and energy vessels are not publicly tracked. It also counted about 28 000 offshore structures, with wind turbines more than doubling since 2017. Detection was above 70 % for 25 m vessels and above 90 % for vessels of 50 m or more. Smaller boats remain largely invisible to 10 m radar.
:::

Before this, the **xView3** challenge (2021–22) had released close to 1 000 Sentinel-1 scenes labelled for dark-vessel detection. Models had to find vessels, estimate their length and say whether they were fishing. Commercial services now combine radar, optical, radio-frequency and AIS data. One example is Vantor's (formerly Maxar's) Maritime Sentry, which uses AIS-to-optical and radar-to-optical tipping. Fully automatic cueing between different companies' satellites is still mostly at the research stage.

![More than 100 freighters waiting at the southern entrance of the Suez Canal on 4 April 2021, after the grounded Ever Given was freed, seen by ASTER on NASA's Terra satellite. Each bright dot is a ship — easy to count by eye here, but across whole oceans it is a job for detectors.](figures/photos/ch46_suez.jpg){#fig:suezships width=38%}

Other maritime tasks follow the same pattern. **Oil spills** damp the small waves that scatter radar, so they appear as dark slicks. The European Maritime Safety Agency's CleanSeaNet service has screened radar images for spills since April 2007. It alerts national authorities within 30 minutes of the image. The difficulty is look-alikes: calm water, algae and rain cells also appear dark, so classifiers use shape, context and wind. **Sea ice** charts are still drawn largely by expert analysts from radar. ESA's AutoICE challenge (2023) showed that a U-Net combining Sentinel-1 with passive-microwave data could map ice concentration, type and floe size together (Chapter 47).

## Disasters

In a disaster, speed matters more than perfection. The key idea is to deliver a good-enough map within hours of the first image, then improve it.

### Flood Mapping

Radar is the main tool for floods because rain clouds hide the ground from optical sensors. Calm open water reflects radar away from the satellite, so it appears dark (Chapter 15). The traditional method picks a backscatter threshold, often with **Otsu's method**. It chooses the threshold $t$ that maximises the between-class variance of the histogram.

$$ \sigma_B^2(t) = w_0(t)\, w_1(t)\, \big[\mu_0(t) - \mu_1(t)\big]^2 $$

Here $w_0$ and $w_1$ are the fractions of pixels below and above $t$, and $\mu_0$ and $\mu_1$ their mean values. Errors come from dark land (smooth sand, tarmac, radar shadow), from flooded forests and towns that look *brighter* because of double bounce between water and trunks or walls, and from wind-roughened water.

The synthetic Sentinel-1-like scene of @fig:eoflood shows these effects. Otsu's threshold of −14.4 dB on VV backscatter (vertical polarisation sent and received) gave a water IoU of 0.59. Adding a **height above nearest drainage** (HAND) mask, which removes land more than 10 m above the river, raised it to 0.64. It removed most radar-shadow false alarms but also some real ponds. A random forest that used both polarisations before and after the flood, plus HAND, reached 0.95. It found 1 836 of the 2 202 bright flooded-forest and flooded-urban pixels; the thresholds found almost none. Synthetic scenes flatter every method. Real scenes add wind, wet snow and errors in the labels themselves.

![Flood mapping from a synthetic Sentinel-1-like scene. (a) Backscatter after the flood. (b) Histogram with Otsu's threshold; radar shadow is as dark as water. (c) Reference, including bright flooded forest and buildings. (d) Threshold plus HAND mask. (e) A random forest using both dates and polarisations. (f) Water intersection over union.](figures/out/ch46_flood.svg){#fig:eoflood width=98%}

Operational systems already work this way. The Copernicus **Global Flood Monitoring** (GFM) service maps every new Sentinel-1 interferometric-wide-swath image automatically. It runs three independently developed algorithms, from LIST, DLR and TU Wien, and combines them by majority vote, with a likelihood layer for uncertainty. Since Sentinel-1A ended operations on 30 June 2026 after 12 years, GFM has used Sentinel-1C and -1D. The **Sen1Floods11** data set (2020) of 4 831 chips from 11 flood events showed a useful result: models trained on many automatically generated labels beat models trained on 446 hand-labelled chips.

![Flood proxy maps of Mozambique after Cyclone Idai in March 2019, made by NASA JPL's ARIA team from ICEYE, Sentinel-1 and ALOS-2 radar images. Light blue marks likely floodwater; the panels track the flood from 18 to 23 March.](figures/photos/ch46_idai.jpg){#fig:idaiflood width=82%}

::: example
**Example: how much does one Sentinel-1 pass map?**

Sentinel-1 orbits at 693 km. In interferometric wide-swath mode its swath is 250 km. How much area does a 10-minute acquisition cover, and can a model keep up?

1. **Orbital speed.** $v = \sqrt{\mu/(R_E + h)} = \sqrt{398\,600/7\,064} = 7.51$ km/s.
2. **Ground speed.** $v_g = v\,R_E/(R_E + h) = 7.51 \times 6\,371/7\,064 = 6.77$ km/s.
3. **Area.** In 600 s the ground track advances 6.77 × 600 = 4 065 km. Times 250 km, that is about 1.02 million km² — roughly the area of Egypt.
4. **Pixels.** At 10 m spacing, 1.02 × 10¹² m² / 100 m² = 1.0 × 10¹⁰ pixels per polarisation. Two polarisations at 2 bytes each are about 40 GB.
5. **Computing.** Cut into 512 × 512 tiles, that is about 38 800 tiles. At an assumed 50 billion operations per tile for a U-Net, the total is 1.9 × 10¹⁵ operations. A graphics processor sustaining 30 × 10¹² operations a second needs about 65 s.

Inference is not the bottleneck. Downloading, calibrating and terrain-correcting the data take longer, and the satellite returns only every 6 days (12 days for each of the two satellites).
:::

### Rapid Mapping and Damage Assessment

Two coordination systems turn images into maps for responders. The **International Charter "Space and Major Disasters"**, in operation since 2000, lets disaster agencies request free imagery from member space agencies. It reached activation number 1 052 in August 2026; 2024 set a record of 85 activations. The **Copernicus Emergency Management Service** (CEMS) adds on-demand mapping. For the Myanmar earthquake of March 2025 it delivered 93 maps from 106 post-event images. Most rapid maps are still drawn or checked by analysts, with AI speeding up the steps.

**Building damage** is assessed by comparing images from before and after. Models trained on xBD grade each building on a four-level scale, from no damage to destroyed. After the February 2023 earthquakes in Türkiye, Microsoft's AI for Good Lab, Planet and the Turkish disaster agency AFAD used such a model on imagery from the first three days. They estimated that 3 849 buildings were damaged or destroyed in four cities. The World Food Programme and Google Research built the open **SKAI** tool. A UN evaluation over nine events found that it covered about seven times more area and gave first results about six times faster, in under a day. A later study comparing two companies' damage maps for the same disaster found that they disagreed in many places. Maps from different models should be treated as estimates, not facts.

Radar change detection gives a complementary view (@fig:mariadamage). It needs no cloud-free image and no labels, but it marks any change in the radar echo, not damage as such.

::: figrow
![Damage proxy map of eastern Puerto Rico after Hurricane Maria (September 2017), from Sentinel-1 images before and after landfall. Red and yellow pixels in the San Juan inset mark likely damage.](figures/photos/ch46_mariadpm.jpg){#fig:mariadamage}

![Thick smoke from the Grasshopper wildfire near Mount Hood, Oregon, photographed from the International Space Station on 31 July 2026. Constellations such as FireSat aim to detect fires far smaller than this one.](figures/photos/ch46_grasshopper.jpg){#fig:grasshopperfire}
:::

### Wildfires

Active fires are found by their heat at 3.9 µm (Chapter 14). New constellations add machine learning and speed (@fig:grasshopperfire). The German company **OroraTech** had 20 thermal satellites of its FOREST series in orbit by October 2026. Its satellites carry a commercial AI module that detects fires on board and sends compact alerts rather than images. The nonprofit Earth Fire Alliance's **FireSat**, built by Muon Space with Google, launched a prototype in March 2025. Its first three operational satellites followed in July 2026, on SpaceX's Transporter-17. They aim to detect fires as small as 5 m × 5 m, with at least twice-daily revisits of fire-prone regions. The stated goal is hourly global revisit by 2029. In both systems, learning helps separate real fires from hot roofs, sun glint and volcanoes.

These services are summarised in @tbl:eodisasterai.

| Service | Data | What AI does | Status (Oct 2026) |
|---|---|---|---|
| Copernicus GFM | Every Sentinel-1 IW image | Three-algorithm ensemble flood maps with likelihood | Operational, global |
| International Charter | Member agencies' satellites | Mostly analyst mapping; AI tools in some workflows | Operational; > 1 050 activations |
| Copernicus EMS rapid mapping | Commercial and Copernicus images | Analyst maps, partly automated | Operational, on demand |
| xBD-trained damage models (e.g. Microsoft, SKAI) | Sub-metre optical, before and after | Building-by-building damage grades | Used in many disasters; accuracy varies |
| FireSat | Six-channel infrared constellation | Fire detection from small hot spots | First 3 operational satellites launched 2026 |
| OroraTech FOREST | Thermal smallsats | Fire detection on board | Commercial service; 20 satellites |

: AI in disaster services. {#tbl:eodisasterai}

## Greenhouse Gases and Human Development

The key idea of this section is that machine learning now finds individual sources of methane from space, and estimates how much they emit. The same tools of image regression also map wealth and poverty.

### Finding Methane Plumes

Methane traps about 80 times more heat than carbon dioxide over 20 years, but lasts only about a decade in the air. Stopping large leaks — "super-emitters" — is one of the quickest ways to slow warming. Methane absorbs sunlight near 1.65 and 2.3 µm. Imaging spectrometers detect it with a **matched filter**, which tests each pixel spectrum $x$ against the expected absorption signature $t$:

$$ \hat\alpha = \frac{(x - \mu)^{\top} \Sigma^{-1} t}{t^{\top} \Sigma^{-1} t}, $$

where $\mu$ and $\Sigma$ are the mean and covariance of the background spectra. The result $\hat\alpha$ is a map of methane enhancement. Bright surfaces, roads and some minerals produce false plumes, and checking every map by eye is slow.

Machine learning helps in two ways. CNNs separate real plumes from artefacts, and regression models estimate emission rates. Schuit and colleagues (2023) combined a CNN with a second classifier on TROPOMI data from Sentinel-5P. They found 2 974 plumes in 2021, with a mean source rate of about 44 t/h. In September 2026 Google and NASA JPL published MAPL-EMIT, a model for the EMIT spectrometer on the International Space Station. It was trained on 3.6 million physics-simulated plumes. It found about 50 % more plumes than human experts and more than 23 000 additional plumes worldwide.

| Mission | Pixel size | Role | Status (Oct 2026) |
|---|---|---|---|
| TROPOMI (Sentinel-5P) | About 5.5 × 7 km | Daily global mapping; finds the largest plumes | Operating |
| GHGSat constellation | About 25 m | Commercial point-source monitoring | Operating; more than a dozen satellites |
| EMIT (ISS) | 60 m | Imaging spectrometer; mineral dust and methane | Operating |
| Tanager-1 (Carbon Mapper, Planet) | About 30 m | Methane and CO₂ point sources | Operating since 2024 |
| Sentinel-2, Landsat | 20–30 m | Multispectral; detect only very large plumes | Operating |
| MethaneSAT (EDF) | About 100 × 400 m | Area-wide emissions | Lost on 20 June 2025 |

: Satellites used to find methane sources. {#tbl:eomethanesats}

::: data
**Data box — methane alerts in numbers**

- **UNEP's Methane Alert and Response System (MARS)**, launched in November 2022, combines satellite data with AI-assisted analysis and notifies governments and operators. By July 2026 it had sent more than 5 000 alerts to 33 countries.
- **Response.** Only 13 % of alerts receive a reply from the operator or government, up from about 1 % in 2024. More than 40 verified mitigations have been recorded in 10 countries.
- **Tanager-1's first year** (September 2024 – September 2025): about 5 392 published methane plumes and 1 234 CO₂ plumes. Of the methane plumes, 2 661 came from oil and gas, 1 327 from waste and 1 211 from coal.
- **Loss of MethaneSAT.** Contact with MethaneSAT was lost on 20 June 2025, about 15 months after launch. It had been designed to map emissions across whole oil and gas basins.
:::

![The first methane plume seen by Tanager-1, on 19 September 2024 over Karachi, Pakistan: a plume about 4 km long from a landfill. Carbon Mapper's preliminary estimate was about 1 200 kg of methane an hour.](figures/photos/ch46_tanager.jpg){#fig:tanagerplume width=44%}

### Estimating the Emission Rate

A plume shows how much methane is in the air, not how fast it is being released. The **integrated mass enhancement** (IME) method links the two. The IME is the total extra methane mass in the plume mask:

$$ \mathrm{IME} = \sum_{i \in \mathrm{mask}} \Delta\Omega_i\, A_i, $$

where $\Delta\Omega_i$ is the column enhancement in kg/m² and $A_i$ the pixel area. If the plume has length scale $L = \sqrt{A_\mathrm{mask}}$ and is carried by an effective wind $U_\mathrm{eff}$, the methane is renewed every $L/U_\mathrm{eff}$ seconds. The emission rate is then

$$ Q = \frac{U_\mathrm{eff}\, \mathrm{IME}}{L}. $$

The effective wind is not the wind at 10 m, $U_{10}$. It is **learned** from simulated plumes, usually as a straight line $U_\mathrm{eff} = \alpha U_{10} + \beta$. For Sentinel-2, published fits use $\alpha = 0.33$ and $\beta = 0.45$ m/s.

In @fig:eomethane this calibration is repeated with a simple plume model at 30 m pixels. A fit on 300 simulated plumes gave $U_\mathrm{eff} = 0.63\,U_{10} + 0.13$ m/s; the coefficients depend on the sensor, the mask rule and the plume model. On 146 test plumes the median error was 31 % with the true wind, and 37 % when the wind had a 1 m/s error. A single estimate can be wrong by a factor of two, so repeated passes matter more than any one number.

![The IME method on synthetic 30 m methane images. (a) A 1 500 kg/h plume with its detection mask. (b) Effective wind needed to recover the true emission, and a straight-line fit. (c) Estimated against true emission for test plumes, with exact wind and with a 1 m/s wind error.](figures/out/ch46_methane.svg){#fig:eomethane width=98%}

::: example
**Example: a methane emission rate from a plume**

A Sentinel-2 image shows a plume from a gas well. The plume mask holds 1 250 pixels of 20 m. The mean column enhancement in the mask is 100 ppb (parts per billion of the total air column). The 10 m wind from a weather model is 3.5 m/s. Assume a dry air column of 101 325 Pa / 9.81 m/s² = 10 329 kg/m².

1. **Unit conversion.** The air column holds 10 329 / 0.028 97 = 356 500 mol/m². A 1 ppb enhancement is 356 500 × 10⁻⁹ × 0.016 04 kg/mol = 5.72 × 10⁻⁶ kg/m².
2. **Mask area and length.** A = 1 250 × 400 m² = 0.5 km², so L = √(5 × 10⁵) = 707 m.
3. **IME.** 100 × 5.72 × 10⁻⁶ kg/m² × 5 × 10⁵ m² = 286 kg.
4. **Effective wind.** $U_\mathrm{eff}$ = 0.33 × 3.5 + 0.45 = 1.61 m/s.
5. **Emission rate.** Q = 1.61 × 286 / 707 = 0.649 kg/s ≈ 2 340 kg/h.
6. **Wind uncertainty.** With 2.5 or 4.5 m/s instead, Q is 1 860 or 2 820 kg/h, about ±20 %.

Sustained for a year, 2.3 t/h is about 20 500 t of methane. With a 20-year warming potential of about 80, that is about 1.6 million t of CO₂-equivalent — from one source.
:::

### Mapping Poverty

Surveys of household income are expensive and rare in many low-income countries. In 2016, Jean and colleagues showed in *Science* that a CNN could predict village wealth in five African countries from daytime satellite images. They trained it first to predict night-time lights, a cheap proxy for economic activity, and explained up to 75 % of the variation in surveyed wealth. In 2022 Chi and colleagues mapped relative wealth for all 135 low- and middle-income countries at 2.4 km resolution. They used satellite imagery with phone-network, connectivity and terrain data. Trained on surveys from 56 countries, the estimates explained 56–70 % of the variation in held-out survey wealth. In 2020 the Government of Togo used such maps, with phone data, to direct emergency cash transfers. The maps are estimates with known errors. Used for targeting, they can wrongly exclude poor households, so they should be checked against local knowledge.

## AI on Board and Smart Tasking

The key idea is to decide in orbit what is worth collecting and sending down, because downlink and imaging time are the scarce resources (Chapter 45). Two uses stand out: **screening** images on board, and **retasking** the satellite before it reaches a target.

### Demonstrations so far

ESA's **Φsat-1** (2020) showed that a deep network on a vision chip drawing only a watt or two could discard cloudy images in orbit. Its successor, **Φsat-2** (2024), carried several uploadable apps, including vessel and wildfire detection (Chapter 45). The main EO demonstrations are listed in @tbl:eoonboard. Most are still demonstrations; few run as part of a paying service.

| Mission or system | Year | What the AI does on board | Status (Oct 2026) |
|---|---|---|---|
| Φsat-1 (ESA) | 2020 | Discards images more than 70 % cloudy | Completed demonstration |
| Satellogic NewSat with Palantir Edge AI | 2022 | Runs third-party detection models | Demonstration |
| Φsat-2 (ESA, Open Cosmos) | 2024 | Cloud, vessel, fire and anomaly apps; map generation; compression | Demonstration; apps updated in orbit |
| CogniSAT-6 with JPL dynamic targeting | 2025 | Looks ahead, skips cloudy targets | First flight test, July 2025 |
| OroraTech FOREST | 2022– | Fire detection and alert compression | Commercial service |
| Planet Pelican-4 | 2026 | Aircraft detection on raw images (about 80 % accurate) | Demonstration, March 2026 |
| Compressed Prithvi model on Kanyini and IMAGIN-e | 2026 | Geospatial foundation model run in orbit | Research demonstration |

: Onboard AI for Earth observation. {#tbl:eoonboard}

::: history
**Dynamic targeting on CogniSAT-6 (2025)**

CogniSAT-6 is a 6U cubesat designed, built and operated by Open Cosmos. Its payload, from Ubotica, pairs a commercial AI processor with a hyperspectral camera from Simera Sense. It was launched in March 2024. In mid-July 2025, NASA JPL's **Dynamic Targeting** software flew on it for the first time. The satellite tilted 40–50° forward to image the ground about 500 km ahead. It analysed that image on board, judged whether the target was clear, and decided to image it or skip it — all in under 90 seconds and without human help. JPL's next steps are to hunt short-lived events such as storms, fires and eruptions, and to let a leading satellite pass targets to the ones behind it.
:::

### What Smart Tasking Is Worth

A satellite passing over a region can usually image only some of the possible targets. A Monte Carlo model in @fig:eotasking estimates the value of choosing well. A pass has 20 candidate targets and room for six images. An image is useful if it is less than 20 % cloudy. At a mean cloud cover of 67 %, blind tasking yields 0.75 clear images per pass. Tasking with a cloud forecast yields 1.78. A look-ahead camera on board yields 2.33, three times as many. At 30 % cloud the gains are smaller: 3.1, 4.8 and 5.7.

Screening after imaging is a different trade. It does not create clear images, but it stops cloudy ones from using the link. At 67 % cloud, keeping only images estimated under 50 % cloudy freed 70 % of the downlink. It raised the useful share of what was sent from 13 % to 42 %, and almost no clear image was lost.

![Clouds and onboard intelligence (Monte Carlo). (a) Clear images per pass from blind tasking, forecast-based tasking and an onboard look-ahead camera, against mean cloud cover. (b) Effect of onboard screening on the share of useful images sent down and on the downlink used.](figures/out/ch46_tasking.svg){#fig:eotasking width=98%}

**Tip-and-cue** extends the idea across a constellation. A wide-area sensor — a radar, a radio-frequency receiver or AIS — detects something, and a sharper sensor is tasked to look. A dark vessel found by radar can be imaged by an optical satellite on its next pass. Such chains are automated within single companies today. Between companies, and from satellite to satellite without a ground loop, they are mostly at the research stage.

## The EO Analytics Business

Most commercial value lies not in pixels but in answers. Novaspace valued the EO data and services market at about $5 billion in 2023 and expected it to pass $8 billion by 2033, with services rising from $3.1 billion to $4.9 billion. Defence is one of the main drivers of growth. Planet, one of the largest commercial imaging operators, reported revenue of $307.7 million for the year to January 2026, up 26 %, with a backlog of over $900 million.

Three changes define the business in 2026 (Chapter 52). First, operators sell **subscriptions and analytics** rather than single images: alerts for new construction, vessel lists, crop statistics. Second, data are sold as **AI-ready products**: calibrated, co-registered time series with cloud masks and standard tiling. EarthDaily, for example, launched six satellites in May 2026 for a constellation designed for broad-area change detection, with 22 spectral bands. Third, **foundation models** are moving into practice. Google's AlphaEarth embeddings summarise each 10 m pixel and year since 2017 as 64 numbers in Earth Engine. A small classifier on these embeddings can map a new class from relatively few labels. NASA and IBM's Prithvi models are fine-tuned for floods, burn scars and crops (Chapter 44).

::: example
**Example: images per day versus analysts**

A constellation collects about 200 million km² a day in scenes of about 32.5 km × 19.6 km, as PlanetScope does. Suppose an analyst needs 5 minutes to check one scene for new buildings and works 7 hours a day.

1. **Scenes per day.** 32.5 × 19.6 = 637 km² per scene; 200 × 10⁶ / 637 ≈ 314 000 scenes a day.
2. **Analyst capacity.** 7 × 60 / 5 = 84 scenes per analyst per day.
3. **Analysts needed.** 314 000 / 84 ≈ 3 740 analysts, every day, for one constellation and one question.
4. **With AI triage.** A change detector flags 2 % of scenes (6 280), and analysts also check a random 1 % of the rest (about 3 080) to watch for misses. That is about 9 360 scenes, or about 111 analysts.
5. **Pixels.** At 3 m, each scene holds about 71 million pixels per band, and the day about 2.2 × 10¹³.

The model does not replace the analysts. It points their attention and lets them spend time on what matters. Its miss rate, measured on the random checks, sets how far its output can be trusted.
:::

## Pitfalls and Good Practice

EO models fail in predictable ways. The key idea is that an accuracy figure means little unless you know where, when and how it was measured (@tbl:eopitfalls).

### Domain Shift

A model trained in one region, season or sensor often fails in another. Soils, crops, building styles, sun angles and atmospheric haze all differ. In @fig:eopitfalls (a), a random forest trained on one synthetic region lost accuracy as the test region became drier and hazier: from 77.8 % to 53.2 % at the largest shift. Adding random spectral changes to the training data helped only slightly and cost accuracy at home. Adding 240 labelled pixels from the new region kept 67.5 %. A few local labels are usually worth more than clever tricks.

Shifts also come from the data chain. A change in processing, such as a new radiometric baseline, alters every pixel slightly (Chapter 45). Models should be monitored after deployment and checked whenever the data chain changes.

### Labels, Imbalance and Validation

**Label noise** is common. Reference maps are out of date, photo-interpreters disagree, and labels from other models carry their errors along. **Class imbalance** is the rule: forest loss, ships and methane plumes are rare, so a model can look accurate while missing most of them (Chapter 43).

**Spatial autocorrelation** inflates accuracy. If training and test pixels come from the same fields, the test measures memory, not skill. Chapter 43 shows how random splits overstate accuracy compared with splits by region. Hold out whole regions, scenes or events.

**Geographic bias** follows from where labels exist. Many large labelled sets were built mainly from North America and Europe, so models often perform worst where data are needed most. Report accuracy by region, not just globally.

### Getting the Area Right

A map is often used to report an **area**: hectares of forest lost, or square kilometres flooded. Counting mapped pixels is biased whenever omission and commission errors do not cancel. Good practice, set out by Olofsson and colleagues (2014), uses a **stratified random sample** of reference points, checked independently, inside each map class. The estimated proportion of true class $k$ is

$$ \hat p_k = \sum_h W_h\, \frac{n_{hk}}{n_h}, \qquad \widehat{\mathrm{SE}}(\hat p_k) = \sqrt{\sum_h W_h^2\, \frac{\hat p_{hk}(1 - \hat p_{hk})}{n_h - 1}}, $$

where $W_h$ is the mapped share of stratum $h$, $n_h$ the number of samples in it, $n_{hk}$ those found to be class $k$, and $\hat p_{hk} = n_{hk}/n_h$.

In @fig:eopitfalls (b), a map of a million pixels finds 65 % of 30 000 true loss pixels and adds 4 000 false ones. Counting gives 2.35 % loss, while the truth is 3.00 %. The stratified estimate is unbiased. With 3 200 reference points, 95 % of repeated surveys fell between 2.61 % and 3.53 %. With only 100 points, the reported confidence interval contained the truth in only 37 % of surveys. The few omission errors hidden in the large "no loss" stratum were usually missed by the sample. Small samples give confident-looking but wrong intervals.

![Two pitfalls, computed. (a) Accuracy of a land-cover random forest as the test region drifts away from the training region, with two remedies. (b) Forest-loss area from pixel counting and from stratified sampling (Olofsson et al. 2014), against reference sample size.](figures/out/ch46_pitfalls.svg){#fig:eopitfalls width=98%}

| Pitfall | What goes wrong | Remedy |
|---|---|---|
| Domain shift | Accuracy falls in new regions, seasons or sensors | Train on varied data; add local labels; monitor drift |
| Label noise | Model learns the errors of its labels | Second interpreter on a sample; robust losses; clean the test set |
| Class imbalance | Rare events missed while accuracy looks high | Report recall, precision and PR curves; set thresholds for real prevalence |
| Spatial autocorrelation | Test scores overstated | Split by region, scene or event; use buffers |
| Geographic bias | Worst performance where data are scarcest | Collect labels in under-served regions; report by region |
| Biased area estimates | Pixel counts misreport change | Stratified reference sample; area-adjusted estimates with confidence intervals |
| Hallucinated detail | Generated images mistaken for data | Label synthetic outputs; never measure from them |

: Common pitfalls of AI for Earth observation and how to avoid them. {#tbl:eopitfalls}

### Explainability, Ethics and Privacy

**Explanations** help to catch shortcuts, such as a ship detector that keys on harbour walls rather than ships (Chapter 44). For maps, the most useful explanation is often simple: show the input images beside the output, with a per-pixel confidence.

**Privacy** matters more as resolution improves. At 30 cm, people cannot be recognised, but vehicles, crowds and the routines of a household can be. Combining imagery with other data can identify individuals. Licensing rules limit some collection; for example, the US rule on imagery of Israel was relaxed from 2 m to 0.4 m in 2020. Other ethical questions concern who controls alerts about people's land, and whether maps are used to help or to punish. Assurance and governance are treated in Chapter 53.

::: note
**Practice: building a flood-mapping model from Sentinel-1**

1. **Define the product.** Example: water extent at 20 m within 6 hours of each pass, scored by water-class IoU against hand-labelled chips, with a separate score for flooded vegetation.
2. **Get the data.** Use Sentinel-1 Ground Range Detected (GRD) images in VV and VH. Calibrate them to the backscatter coefficient σ⁰ and terrain-correct them with the Copernicus digital elevation model (DEM). Add a pre-flood reference image from the same orbit, a permanent-water map and a HAND layer.
3. **Get labels.** Start from Sen1Floods11 and similar open sets. Add hand labels from your region, including urban and forest floods, and have a second person relabel 10 % to measure label noise.
4. **Set a baseline.** Run Otsu's threshold on VV (in dB) with the HAND and permanent-water masks. Record its IoU; every model must beat it.
5. **Train.** Fit a random forest on per-pixel features (VV, VH, their changes, HAND), then a small U-Net on 256 × 256 tiles. Use flips and rotations for augmentation, never mixing tiles from one event across splits.
6. **Validate by event.** Hold out whole floods from other continents and seasons. Report IoU, precision and recall per event, and for open water and flooded vegetation separately.
7. **Check failure cases.** Inspect wind-roughened lakes, wet snow, sand, radar shadow and dense cities, and add labels where errors cluster.
8. **Deploy and monitor.** Run on each new image automatically, publish a confidence layer, and compare with GFM and analyst maps after every major event. Retrain when the sensor or processing changes.
:::

::: key
**Key takeaways**

- EO analysis reduces to a few tasks — segmentation, detection, change, time series and retrieval — on images with many bands, a time axis and a location. Neighbourhood and time information often matter more than the choice of network.
- Simple baselines stay strong. Random forests, NDVI differences, Lee filters, CFAR and Otsu thresholds should be beaten, by a measured margin, before a deep model is adopted.
- Operational AI products now map land cover, buildings, crops and forest loss globally, track dark vessels, map floods from every Sentinel-1 image and find methane plumes from orbit.
- Emission rates, flood areas and loss areas are estimates with real uncertainty: the IME method's single-plume errors are often 30–40 %, and pixel counts of maps are biased.
- Onboard AI is moving from demonstration to service. Look-ahead tasking can triple the clear images collected in cloudy regions, and screening frees much of the downlink.
- Most failures come from the data: domain shift, label noise, imbalance, spatially correlated validation and geographic bias. Split by region, sample properly and report uncertainty.
:::

::: questions
**Review questions**

1. Name the task type, a suitable model and a metric for: counting aircraft at airports; mapping burned area; classifying crop types from a season of images; estimating forest biomass.
2. In @fig:eolandcover, why did a random forest given 5 × 5 neighbourhoods gain almost nine points over the same forest on single pixels? Which classes gained most, and why?
3. Explain why an NDVI-difference threshold flags harvested fields as deforestation. What extra information did the learned detector of @fig:eochange use?
4. Write the temporal-attention weights for a time series in which two of five dates are cloudy. Why does attention not need gap filling?
5. Derive the CFAR multiplier $\alpha$ for exponential clutter and $P_{fa} = 10^{-6}$. Why do azimuth ghosts and breaking waves still cause false alarms?
6. Why can the equivalent number of looks reward a bad speckle filter? Which other measures would you report?
7. A flooded forest appears brighter in radar than the same forest when dry. Explain why, and how a flood-mapping model can still classify it as water.
8. A methane plume has an IME of 500 kg over a mask of 1 km². The 10 m wind is 5 m/s. Using $U_\mathrm{eff} = 0.33\,U_{10} + 0.45$ m/s, estimate the emission rate in kg/h, and its range if the wind is uncertain by ±1.5 m/s.
9. Using @fig:eotasking, estimate the number of clear images per pass at 55 % mean cloud cover for each tasking strategy. When would onboard screening be a poor choice?
10. A forest-loss map shows 2 000 km² of loss. A stratified sample shows that 20 % of mapped loss is false and that 1 % of the mapped "no loss" area of 98 000 km² is real loss. Estimate the true loss area and explain why pixel counting failed.
:::
