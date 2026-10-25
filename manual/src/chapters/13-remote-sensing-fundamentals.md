---
title: Remote Sensing Fundamentals
hero: ch13
abstract: Remote sensing is the science of measuring things without touching them. From orbit, satellites measure the light, heat and radio waves leaving the Earth and turn them into maps of crops, forests, cities, oceans, ice and air. This chapter explains the physics that makes this possible - electromagnetic radiation, its interaction with the atmosphere and the surface, and the spectral signatures that identify materials - and the engineering concepts used to describe sensors: spatial, spectral, radiometric and temporal resolution, image quality, geometric correction, processing levels and analysis-ready data. It ends with the methods used to turn images into information and the open-data ecosystem that has made satellite data a global public good.
---

## What Remote Sensing Is

**Remote sensing** means acquiring information about an object from a distance, usually by measuring electromagnetic radiation that the object reflects or emits. Satellites have made it possible to observe the whole planet repeatedly, consistently and objectively. The first weather satellite, TIROS-1, returned its first television images of clouds in April 1960. The US CORONA reconnaissance programme returned film capsules from 1960. **Landsat 1**, launched in July 1972, began the longest continuous record of Earth's land surface — a record that continues today with Landsat 8 and 9. Since 2008, all Landsat data have been free. Since 2014 the European Union's **Copernicus** programme has provided free and open data from its Sentinel satellites. Together they have transformed Earth observation (EO) into a global public good used by millions.

Remote sensing systems are classified by the source of the energy they measure:

- **Passive optical** systems measure reflected sunlight (visible, near-infrared and short-wave infrared, about 0.4–2.5 µm). They only work in daylight and are blocked by clouds.
- **Passive thermal** systems measure radiation emitted by the surface and atmosphere (mid-wave and long-wave infrared, about 3–14 µm). They work day and night but are blocked by clouds.
- **Passive microwave** systems measure natural microwave emission. They see through most clouds but have coarse resolution.
- **Active** systems — radar and lidar — provide their own illumination. Radar works day and night through clouds (Chapter 15); lidar measures heights and atmospheric profiles precisely.

The complete remote-sensing chain (@fig:chain) links a source of energy, its passage through the atmosphere and its interaction with the surface. It continues with the return trip through the atmosphere, the sensor, and the processing and analysis that turn measurements into decisions.

![The remote-sensing chain: illumination, interaction with the atmosphere and surface, measurement by the sensor, and processing into information for users.](figures/out/ch13_chain.svg){#fig:chain width=94%}

## Electromagnetic Radiation

### Waves, Photons and the Spectrum

Electromagnetic radiation travels at the speed of light $c$ = 299 792 458 m/s. Its wavelength $\lambda$ and frequency $\nu$ are related by $c = \lambda\nu$, and each photon carries an energy $E = h\nu = hc/\lambda$, where $h = 6.626\times10^{-34}$ J s is Planck's constant. Remote-sensing wavelengths span from about 0.3 µm (ultraviolet) to tens of centimetres (microwave radar) — a range of a million to one (Chapter 12, @fig:spectrum).

### Thermal Emission: Planck's Law

Every object above absolute zero emits radiation. An ideal emitter — a **blackbody** — emits a spectral radiance given by **Planck's law**:

$$B_\lambda(T) = \frac{2hc^2}{\lambda^5}\,\frac{1}{e^{hc/\lambda k_B T} - 1}$$

Two consequences are central to remote sensing (@fig:blackbodies):

- **Wien's displacement law**: the peak wavelength is $\lambda_{max} = 2\,898\ \mu\text{m·K}/T$. The Sun (≈ 5 800 K) peaks near 0.5 µm — which is why our eyes evolved to see there. The Earth's surface (≈ 300 K) peaks near 10 µm. A forest fire (≈ 1 000–1 200 K) peaks at 2.4–2.9 µm, which is why fires are detected in the mid-wave infrared around 4 µm.
- **Stefan–Boltzmann law**: the total emitted power per unit area is $M = \varepsilon\sigma T^4$; hot objects radiate enormously more energy than cool ones.

Real surfaces emit less than a blackbody by a factor called the **emissivity** $\varepsilon(\lambda)$ (0–1). Water and vegetation have thermal-infrared emissivities of 0.97–0.99; bare rocks and soils vary from 0.85 to 0.98, and their emissivity spectra identify minerals.

![Planck curves for sunlight, a wildfire, the Earth's surface and cold cloud tops, each normalised to its peak.](figures/out/ch13_blackbodies.svg){#fig:blackbodies width=86%}

### Radiometric Quantities

Engineers use precise quantities to describe radiation:

| Quantity | Symbol | Unit | Meaning |
|---|---|---|---|
| Radiant flux | $\Phi$ | W | Power |
| Irradiance | $E$ | W m⁻² | Power arriving per unit area |
| Radiant exitance | $M$ | W m⁻² | Power leaving per unit area |
| Radiance | $L$ | W m⁻² sr⁻¹ | Power per unit area per unit solid angle — what a sensor pixel measures |
| Spectral radiance | $L_\lambda$ | W m⁻² sr⁻¹ µm⁻¹ | Radiance per unit wavelength |
| Reflectance | $\rho$ | dimensionless | Fraction of incident radiation reflected |
| Brightness temperature | $T_B$ | K | Temperature of a blackbody producing the measured radiance |

: Radiometric quantities used in remote sensing. {#tbl:radquant}

A sensor measures **radiance** at the top of the atmosphere. Converting it to **top-of-atmosphere (TOA) reflectance** removes the effect of solar illumination:

$$\rho_{TOA} = \frac{\pi\,L_\lambda\,d^2}{E_{sun,\lambda}\cos\theta_s}$$

where $d$ is the Earth–Sun distance in AU, $E_{sun,\lambda}$ the exo-atmospheric solar irradiance and $\theta_s$ the solar zenith angle. Removing the effects of the atmosphere then gives **surface reflectance** — the property of the ground itself.

## Interaction with the Atmosphere

Between the Sun, the ground and the sensor, the atmosphere **scatters** and **absorbs** radiation:

- **Rayleigh scattering** by gas molecules (much smaller than the wavelength) is proportional to $\lambda^{-4}$. Blue light (450 nm) scatters roughly four to five times more than red light (650 nm). This is why the sky is blue and why images in the blue band look hazy (@fig:scattering).
- **Mie scattering** by aerosols (dust, smoke, sea salt, pollution particles of similar size to the wavelength) depends more weakly on wavelength and produces the whitish haze over cities and deserts. The **aerosol optical depth (AOD)** at 550 nm ranges from about 0.05 in clean air to more than 2 in heavy smoke or dust.
- **Absorption** by water vapour, carbon dioxide, ozone and oxygen removes radiation in specific bands (Chapter 12, @fig:windows). Sensors observe the surface through the **atmospheric windows**.
- **Clouds** block optical and infrared radiation completely; on average about 67 % of the Earth is cloud-covered at any time — a fundamental limitation that makes all-weather radar so valuable.

![Vertical optical depth for Rayleigh scattering by air molecules and for two aerosol types as a function of wavelength. Short wavelengths are attenuated far more.](figures/out/ch13_scattering.svg){#fig:scattering width=84%}

The radiance reaching a sensor over a dark surface may be more than half **path radiance** — light scattered into the sensor by the atmosphere without ever touching the ground. **Atmospheric correction** removes these effects using radiative-transfer models (e.g., 6S, MODTRAN, libRadtran) and information on aerosols, water vapour and ozone, often retrieved from the image itself (e.g., using dark-target or "dense dark vegetation" methods). Operational processors such as ESA's Sen2Cor and NASA's LaSRC/LEDAPS produce surface-reflectance products for Sentinel-2 and Landsat.

## Interaction with the Surface: Spectral Signatures

### Why Things Look Different

When radiation strikes a surface it may be reflected, absorbed or transmitted. The fraction reflected depends on wavelength in ways that are characteristic of each material — its **spectral signature** (@fig:signatures):

- **Healthy vegetation** absorbs strongly in the blue and red (by chlorophyll, for photosynthesis) and reflects a little more in the green (which is why leaves look green). It reflects strongly in the near-infrared (40–50 %) because of scattering in the internal cell structure of leaves. The sharp rise between red and near-infrared at about 0.70–0.75 µm is the **red edge**; its position shifts with chlorophyll content and plant stress. In the short-wave infrared, reflectance falls in the water absorption bands at 1.45 and 1.94 µm; drier leaves reflect more.
- **Soils and rocks** generally show gently increasing reflectance with wavelength, modified by moisture (wetter soils are darker) and organic matter. Iron oxides (absorption near 0.9 µm) and clay and carbonate minerals (absorption features near 2.2 and 2.3 µm) also modify it — the basis of geological mapping.
- **Water** reflects little except in the blue and green, and absorbs almost everything beyond about 0.75 µm — so water appears black in near-infrared images, making shorelines and floods easy to map. Suspended sediment and phytoplankton change the visible reflectance of water, the basis of **ocean-colour** remote sensing.
- **Snow** is highly reflective in the visible but much darker in the short-wave infrared, whereas clouds stay bright — a property used to distinguish snow from cloud.
- **Built surfaces** (concrete, asphalt, roofs) have relatively flat, moderate spectra.

![Schematic spectral reflectance signatures of common surface materials, with Landsat 8/9 OLI bands shaded. Differences in these curves allow materials to be distinguished from orbit.](figures/out/ch13_signatures.svg){#fig:signatures width=92%}

### Bidirectional Reflectance

Real surfaces are not perfect diffuse (Lambertian) reflectors: their brightness depends on the directions of illumination and viewing, described by the **bidirectional reflectance distribution function (BRDF)**. Forests appear brightest when viewed with the Sun behind the observer (the "hot spot", where shadows are hidden); water shows sharp **sun glint** in the specular direction. Wide-swath sensors and agile satellites that view at different angles must correct for BRDF effects to compare observations.

### Spectral Indices

Simple combinations of bands — **spectral indices** — capture key surface properties and are widely used because they are easy to compute and interpret:

| Index | Formula | Use |
|---|---|---|
| Normalised Difference Vegetation Index (NDVI) | $(\rho_{NIR} - \rho_{red})/(\rho_{NIR} + \rho_{red})$ | Vegetation greenness and density |
| Enhanced Vegetation Index (EVI) | $2.5(\rho_{NIR} - \rho_{red})/(\rho_{NIR} + 6\rho_{red} - 7.5\rho_{blue} + 1)$ | Vegetation in dense canopies, less atmospheric effect |
| Normalised Difference Water Index (NDWI, McFeeters) | $(\rho_{green} - \rho_{NIR})/(\rho_{green} + \rho_{NIR})$ | Open water |
| Normalised Difference Moisture Index (NDMI) | $(\rho_{NIR} - \rho_{SWIR1})/(\rho_{NIR} + \rho_{SWIR1})$ | Vegetation water content |
| Normalised Burn Ratio (NBR) | $(\rho_{NIR} - \rho_{SWIR2})/(\rho_{NIR} + \rho_{SWIR2})$ | Burn severity (difference before/after fire, dNBR) |
| Normalised Difference Snow Index (NDSI) | $(\rho_{green} - \rho_{SWIR1})/(\rho_{green} + \rho_{SWIR1})$ | Snow cover |
| Normalised Difference Built-up Index (NDBI) | $(\rho_{SWIR1} - \rho_{NIR})/(\rho_{SWIR1} + \rho_{NIR})$ | Urban areas |

: Widely used spectral indices. NIR = near-infrared; SWIR1 ≈ 1.6 µm; SWIR2 ≈ 2.2 µm. {#tbl:indices}

![Red and near-infrared reflectance of six surface types (left) and the resulting NDVI (right). Healthy vegetation gives NDVI values of 0.6–0.9; bare soil 0.1–0.2; water and clouds near zero or negative.](figures/out/ch13_ndvi.svg){#fig:ndvi width=98%}

::: figrow
![Centre-pivot irrigated fields in the desert of Al Jowf, Saudi Arabia, imaged by NASA's ASTER instrument in false colour, where vigorous vegetation appears red because it reflects strongly in the near-infrared.](figures/photos/ch13_aljowf.jpg){#fig:aljowf}

![The San Francisco Bay Area in an ASTER false-colour composite. Vegetation is red; urban areas appear blue-grey; water is dark.](figures/photos/ch13_sf.jpg){#fig:sfbay}
:::

## The Four Resolutions

A remote-sensing system is characterised by four kinds of resolution (@fig:fourres):

![The four resolutions of a remote-sensing system: spatial, spectral, radiometric and temporal.](figures/out/ch13_four_res.svg){#fig:fourres width=100%}

**Spatial resolution** is the size of the smallest feature that can be distinguished. It is commonly expressed by the **ground sampling distance (GSD)** — the distance between pixel centres on the ground — although true resolving power also depends on optical quality and motion (see MTF below). EO systems range from about 30 cm (very-high-resolution commercial imagers) to 1–2 km (global weather imagers).

**Spectral resolution** is the number, position and width of the spectral bands. **Panchromatic** sensors have one broad band; **multispectral** sensors have 4–20 bands; **hyperspectral** (imaging spectroscopy) sensors have 100–400 contiguous narrow bands (5–10 nm wide) that record a near-continuous spectrum for every pixel (Chapter 14).

**Radiometric resolution** is the sensor's ability to distinguish small differences in brightness. It is set by the number of bits used to record each pixel (8-bit = 256 levels; Landsat 9 uses 14 bits = 16 384 levels) and, more fundamentally, by its signal-to-noise ratio.

**Temporal resolution** is how often the same place is observed (revisit time), from 30 seconds (geostationary "rapid scan" over storms) to 16 days (a single Landsat) or longer.

These resolutions trade against one another and against swath width, data volume and cost. A satellite cannot image a wide area at very fine resolution in hundreds of bands every day, all at the same time. @fig:tradespace shows how today's systems span the trade space.

![Ground sampling distance versus swath width for representative EO systems. Most sensors lie near a line corresponding to a few tens of thousands of pixels across the swath, the practical limit of detector arrays and data rates.](figures/out/ch13_tradespace.svg){#fig:tradespace width=92%}

## Image Quality

### Modulation Transfer Function

GSD alone does not tell how sharp an image is. A sensor blurs the scene through optical diffraction and aberrations, the finite size of each detector pixel, motion of the satellite and pointing jitter during the exposure, and the atmosphere. The **modulation transfer function (MTF)** describes how much contrast the system preserves as a function of spatial frequency; the system MTF is the product of the MTFs of each contributor (@fig:mtf). A common specification is the MTF at the **Nyquist frequency** (one cycle per two pixels): values of 0.1–0.3 are typical. Too low and images look soft; too high and fine patterns produce **aliasing** artefacts.

![Contributions to the modulation transfer function of a typical EO imager. The system MTF is the product of optics, detector and motion terms; its value at the detector Nyquist frequency is a key image-quality specification.](figures/out/ch13_mtf.svg){#fig:mtf width=82%}

### Signal-to-Noise Ratio

The **signal-to-noise ratio (SNR)** expresses how well the signal stands above random noise from photon statistics (shot noise, $\sqrt{N}$ for $N$ photo-electrons), detector dark current, read-out electronics and quantisation. A related figure of merit is the **noise-equivalent change in reflectance (NEΔρ)** or, for thermal sensors, the **noise-equivalent temperature difference (NEΔT)** — typically 0.05–0.1 K for modern thermal imagers. This figure states the smallest change that can be detected. SNR improves with larger apertures, wider bands, longer integration time (using time-delay integration, TDI) and cooler detectors (Chapter 12).

### Interpretability: NIIRS and GIQE

For high-resolution imagery, users care about what tasks an image supports. The US **National Imagery Interpretability Rating Scale (NIIRS)** rates images from 0 to 9 by the objects that can be identified. NIIRS 5 allows individual rail cars to be identified by type, and NIIRS 6 distinguishes between car types (sedans and station wagons). NIIRS 7 allows individual rail ties to be identified. The **General Image Quality Equation (GIQE)** estimates NIIRS from GSD, the relative edge response (a measure of sharpness), image processing gain and SNR. Halving the GSD raises NIIRS by about one level.

## Geometry: Putting Pixels on the Map

### Sources of Geometric Distortion

A raw image is not a map. Its geometry is distorted by:

- the **viewing geometry** — off-nadir viewing stretches pixels and makes them oblique;
- **Earth's curvature and rotation** during a push-broom scan (the image is skewed westward as the Earth turns beneath it);
- **terrain relief** — elevated points appear displaced away from the nadir point (@fig:relief);
- **platform position and attitude errors** from GNSS and star trackers; and
- **sensor geometry** — lens distortion and focal-plane alignment.

![Relief displacement: the top of a tall object (or mountain) appears shifted away from nadir by d = h·tan θ. Without correction, a 1 000 m mountain imaged 20° off nadir would be displaced by 364 m.](figures/out/ch13_relief.svg){#fig:relief width=84%}

### Geolocation and Orthorectification

**Geolocation** computes the ground position of each pixel by projecting its line of sight from the satellite's position and attitude onto the Earth's surface model. Before ground control, modern satellites achieve geolocation accuracy of better than 5 m CE90 for very-high-resolution systems and about 10–15 m for Landsat-class sensors. With **ground control points (GCPs)** and precision processing, the Landsat and Sentinel-2 archives are co-registered to better than one pixel.

**Orthorectification** removes the effects of terrain and viewing geometry using a **digital elevation model (DEM)** — a gridded map of surface heights. The result is an **orthoimage** in which every pixel is at its true map position, like a map. Global DEMs widely used for this purpose include the SRTM (Shuttle Radar Topography Mission, 2000, 30 m) and the Copernicus DEM (derived from TanDEM-X, 30 m and 90 m global). Others are ALOS World 3D (30 m) and NASADEM.

For commercial satellites, the camera model is often distributed as **rational polynomial coefficients (RPCs)**. These are ratios of cubic polynomials that map ground coordinates (latitude, longitude, height) to image coordinates. They let users orthorectify images without knowing the proprietary sensor model.

### Map Projections and Coordinate Systems

Orthoimages are delivered in a **map projection** — a mathematical transformation of the curved Earth onto a flat plane. The most common for EO is the **Universal Transverse Mercator (UTM)** system, which divides the Earth into 60 zones 6° wide; Sentinel-2 and Landsat products are delivered in UTM tiles. Global products often use a geographic latitude–longitude grid, sinusoidal (MODIS) or equal-area grids (EASE-Grid). All coordinates refer to a **datum**, today almost always WGS 84 (Chapter 18).

## Processing Levels and Analysis-Ready Data

### From Raw Bits to Information

Space agencies classify data products by **processing level** (@fig:levels):

- **Level 0** — raw instrument data at full resolution, time-ordered, with communications artefacts removed.
- **Level 1A/1B** — data with radiometric calibration applied (Level 1B in radiance units) and geolocation information attached.
- **Level 1C/1T** — orthorectified, map-projected TOA reflectance or radiance (e.g., Sentinel-2 L1C, Landsat L1TP).
- **Level 2** — derived geophysical variables at the same resolution: surface reflectance, land-surface temperature, sea-surface temperature, cloud masks.
- **Level 3** — variables mapped onto uniform space–time grids, often composited over days or months (e.g., monthly global NDVI).
- **Level 4** — model output or results from analysis of lower-level data (e.g., gross primary productivity, crop yield, carbon flux).

![Data processing levels from raw telemetry (Level 0) to model-based information products (Level 4).](figures/out/ch13_levels.svg){#fig:levels width=96%}

### Calibration and Validation

**Calibration** establishes the link between the sensor's digital numbers and physical units. It begins with pre-flight laboratory calibration against standards traceable to national metrology institutes. In orbit, it continues with on-board calibrators (solar diffusers, lamps, blackbodies) and observations of the Moon (whose reflectance is extremely stable). It also uses **vicarious calibration** sites with stable bright surfaces (such as Railroad Valley in Nevada, La Crau in France and Gobabeb in Namibia, part of the **RadCalNet** network). Finally, there is **cross-calibration** between satellites viewing the same place at nearly the same time. The radiometric accuracy of good modern sensors is about 3–5 % absolute and better than 1 % relative stability. Upcoming climate-benchmark missions, such as the UK-led ESA mission **TRUTHS**, aim for SI-traceable accuracy of 0.3 % or better so that they can serve as "standards in space" for other sensors.

**Validation** checks derived products against independent reference data — field measurements, airborne campaigns, in-situ networks (such as AERONET for aerosols, FLUXNET for carbon fluxes and Argo floats for the ocean) — and reports their uncertainty. The international **Committee on Earth Observation Satellites (CEOS)** coordinates calibration and validation among agencies.

### Analysis-Ready Data

Most users do not want to correct each image themselves. **Analysis-ready data (ARD)** are satellite data processed to a minimum set of requirements — calibrated, geometrically corrected, atmospherically corrected to surface reflectance, cloud-masked, with per-pixel quality information — so that users can analyse them directly. CEOS has defined the **CEOS Analysis Ready Data (CEOS-ARD)** framework (formerly CARD4L) for optical, thermal and radar data; Landsat Collection 2, Sentinel-2 L2A and the harmonised Landsat–Sentinel (HLS) dataset are examples. HLS combines Landsat 8/9 and the Sentinel-2 satellites into a single 30 m surface-reflectance record with a revisit of 2–3 days.

### Cloud Platforms, Data Cubes and Standards

Earth-observation archives now grow by many petabytes per year. The Copernicus Sentinel satellites alone produce more than 15 TB of data per day, and a single radar mission such as NISAR adds tens of terabytes per day. Instead of downloading data, users increasingly bring their algorithms to the data on **cloud computing platforms**:

- **Google Earth Engine** — a planetary-scale analysis platform with a multi-petabyte catalogue of Landsat, Sentinel, MODIS and many other datasets, free for research and non-commercial use;
- the **Copernicus Data Space Ecosystem** — the EU's platform providing free access to all Sentinel data with processing services;
- **Microsoft Planetary Computer**, **Amazon Web Services Open Data** and the **NASA Earthdata Cloud**, which hosts NASA's archive in AWS;
- national **data cubes** such as Digital Earth Australia and Digital Earth Africa, which organise ARD into time series for every pixel of a country or continent.

Common open standards make this possible. **Cloud-Optimized GeoTIFF (COG)** files are organised so that a program can read just the part of an image it needs over the internet. **Zarr** stores multidimensional arrays in chunks. The **SpatioTemporal Asset Catalog (STAC)** specification provides a common way to describe and search EO data across providers.

## Turning Images into Information

### Visual Interpretation and Colour Composites

Humans interpret images using tone, colour, texture, pattern, shape, size, shadow, context and association. Multispectral data are displayed by assigning three bands to the red, green and blue channels of a display. A **true-colour** composite (red, green, blue bands) looks like a photograph. A **false-colour infrared** composite (near-infrared, red, green displayed as red, green, blue) makes healthy vegetation bright red, as in @fig:aljowf and @fig:gardencity, and is the traditional way to assess vegetation. A **SWIR composite** (SWIR2, NIR, red) highlights burned areas and active fires while seeing through smoke, as in @fig:rimfire.

::: figrow
![Centre-pivot irrigated fields near Garden City, Kansas, in a Landsat 7 false-colour composite. Each circle is typically 800 m or 1.6 km in diameter; colour shows crop vigour and growth stage.](figures/photos/ch13_gardencity.jpg){#fig:gardencity}

![The 2013 Rim Fire near Yosemite, California, imaged by MODIS on NASA's Terra satellite. The smoke plume streams north-east; thermal and short-wave infrared bands map the active fire front through the smoke.](figures/photos/ch13_rimfire.jpg){#fig:rimfire}
:::

### Classification

**Image classification** assigns each pixel (or object) to a class such as forest, cropland, water or urban:

- In **unsupervised classification** (e.g., k-means, ISODATA), an algorithm groups pixels into spectral clusters, which the analyst then labels.
- In **supervised classification**, the analyst provides labelled training samples, and a classifier learns to recognise each class. Traditional classifiers include maximum likelihood; modern ones include **random forests**, support vector machines, gradient-boosted trees and **deep learning** (convolutional neural networks and transformers — see Part XIII).
- **Object-based image analysis (OBIA)** first segments the image into homogeneous objects (fields, buildings) and then classifies the objects using their spectral, shape and context attributes — useful for high-resolution imagery.

Global land-cover maps are now produced at 10 m resolution: ESA WorldCover (2020, 2021), Esri/Impact Observatory's annual land cover and Google's **Dynamic World**, which classifies every Sentinel-2 image in near-real time using deep learning.

### Accuracy Assessment

A map is only useful if its accuracy is known. Accuracy is assessed by comparing the map with independent **reference data** collected by a statistically valid sample and tabulating the result in a **confusion matrix** (also called an error matrix):

| Map class ↓ / Reference → | Forest | Crop | Water | Urban | Total | User's accuracy |
|---|---|---|---|---|---|---|
| Forest | 182 | 12 | 1 | 2 | 197 | 92.4 % |
| Crop | 15 | 141 | 0 | 9 | 165 | 85.5 % |
| Water | 1 | 0 | 88 | 1 | 90 | 97.8 % |
| Urban | 2 | 11 | 1 | 84 | 98 | 85.7 % |
| Total | 200 | 164 | 90 | 96 | 550 | |
| Producer's accuracy | 91.0 % | 86.0 % | 97.8 % | 87.5 % | | **Overall 90.0 %** |

: Example confusion matrix for a four-class land-cover map with 550 validation samples (illustrative values). {#tbl:confusion}

From the confusion matrix (@tbl:confusion), **overall accuracy** is the fraction of samples correctly classified (here 495/550 = 90.0 %). **User's accuracy** (the complement of commission error) tells a map user how often a pixel labelled "crop" really is crop. By contrast, **producer's accuracy** (the complement of omission error) tells the map producer how much of the real crop was found. Best practice (Olofsson et al., 2014) also uses the matrix to correct area estimates for map errors and to report confidence intervals.

### Change Detection and Time Series

Many of the most important applications are about **change**: deforestation, urban growth, flood extent, crop development, glacier retreat. Methods include:

- **image differencing and ratioing** of bands or indices between two dates (e.g., differenced NBR for burn severity);
- **post-classification comparison** of two classified maps;
- **time-series analysis** of every observation of a pixel over years or decades, using algorithms such as LandTrendr, CCDC (Continuous Change Detection and Classification) and BFAST, which model seasonal cycles and detect breaks;
- **deep-learning change detection**, which learns to recognise meaningful changes (new buildings, damage) while ignoring irrelevant ones (shadows, season).

Dense time series are possible because of free data and combined constellations. The Global Forest Watch annual tree-cover-loss maps (University of Maryland) are based on the full Landsat archive since 2000. These maps, and the GLAD and RADD near-real-time deforestation alerts (using Landsat, Sentinel-2 and Sentinel-1 radar), are examples used by governments and companies to enforce laws and supply-chain commitments.

![Lake Mead on the Colorado River seen by ASTER on NASA's Terra satellite. Comparison of images from 2000 and 2015 reveals the light-coloured "bathtub ring" of exposed shoreline left as the water level fell by about 40 m to a record low.](figures/photos/ch13_lakemead.jpg){#fig:lakemead width=86%}

### From Pixels to Physical Variables

Beyond classification, remote sensing retrieves quantitative **geophysical variables** by inverting physical models: leaf-area index, soil moisture, land-surface temperature, sea-surface height, ocean chlorophyll concentration, aerosol optical depth, trace-gas columns. The Global Climate Observing System (GCOS) has defined 55 **Essential Climate Variables (ECVs)**, more than half of which can be observed globally only from space. ESA's Climate Change Initiative and the Copernicus Climate Change Service produce long, consistent satellite records of many of them.

## The Open-Data Revolution and the Users

### Data Policy

For its first decades, satellite data were expensive: a Landsat Thematic Mapper scene cost about US $4 400 in the 1990s, and most data were never used. In 2008 the US Geological Survey made the entire Landsat archive free to all users, and downloads increased from about 25 000 scenes per year to millions. In 2014 the EU adopted a **full, free and open** data policy for Copernicus. Studies have estimated the annual economic benefit of open Landsat data at several billion US dollars. Other agencies, including JAXA, INPE (Brazil), CSA and ISRO, have followed with open policies for many of their datasets.

Commercial data, by contrast, are licensed. Very-high-resolution optical and SAR imagery from companies such as Maxar (Vantor), Airbus, Planet, BlackSky, ICEYE, Capella and Umbra is sold under licences that restrict redistribution. Governments are often anchor customers through programmes such as the US National Reconnaissance Office's Electro-Optical Commercial Layer. Another is NASA's Commercial SmallSat Data Acquisition (CSDA) programme, which buys data for use by NASA-funded scientists.

National regulations also govern remote sensing. In the USA, commercial remote-sensing systems are licensed by NOAA's Commercial Remote Sensing Regulatory Affairs office under a tiered system introduced in 2020; Germany has the SatDSiG data security law; other countries have similar rules. Internationally, the **UN Principles Relating to Remote Sensing of the Earth from Outer Space** (1986) state that remote sensing shall be carried out for the benefit of all countries. They also state that a sensed state shall have access to data concerning its territory on a non-discriminatory basis. Privacy concerns grow as resolution improves, although at 30 cm individuals cannot be identified.

### Applications

| Sector | Typical applications | Typical data |
|---|---|---|
| Agriculture | Crop type and area, crop health, yield forecasting, irrigation, insurance | Sentinel-2, Landsat, Planet, Sentinel-1, MODIS/VIIRS |
| Forestry and carbon | Deforestation alerts, forest biomass and height, carbon credits verification | Landsat, Sentinel-1/2, GEDI lidar, BIOMASS radar, ICESat-2 |
| Water resources | Reservoir levels, irrigation water use, snow cover, groundwater change | SWOT, Landsat thermal, GRACE-FO, MODIS snow |
| Disasters | Flood, fire, earthquake and storm mapping, damage assessment | SAR constellations, VHR optical, VIIRS fire, GOES/Himawari |
| Urban and infrastructure | Urban growth, informal settlements, subsidence, building footprints | VHR optical, InSAR (Sentinel-1, ICEYE), night lights |
| Oceans and coasts | Sea-surface temperature, ocean colour, oil spills, ship detection, coastal erosion | Sentinel-3, PACE, SAR, AIS from space |
| Climate and atmosphere | Greenhouse gases, aerosols, ozone, ice sheets, sea-level rise | OCO-2/3, Sentinel-5P, Copernicus Sentinel-6, ICESat-2, CryoSat-2 |
| Defence and security | Monitoring of facilities, borders, maritime domain awareness | VHR optical, SAR, RF geolocation (Chapter 19) |
| Finance and insurance | Commodity monitoring, parametric insurance, supply-chain verification | Optical and SAR constellations, analytics platforms |
| Public health | Disease vector habitats, heat stress, air quality | Thermal, aerosol and land-cover data |

: Major application areas of Earth observation. {#tbl:applications}

The **International Charter "Space and Major Disasters"** was founded in 2000 by ESA, CNES and CSA. It now unites some 17 space agencies and operators who provide satellite data free of charge to countries affected by major disasters. It has been activated more than 900 times. The Copernicus Emergency Management Service and UN-SPIDER/UNOSAT provide rapid mapping services.

::: example
**Example: estimating the irrigated area of a district**

An analyst wants the area of irrigated cropland in a 5 000 km² district during the dry season.

1. Select all Sentinel-2 L2A (surface reflectance) images for the dry season and mask clouds using the scene classification layer.
2. Compute NDVI for each image and take the maximum value composite per pixel (to capture peak green-up).
3. Collect 400 training samples (irrigated, rain-fed, natural vegetation, bare, water, urban) from field visits and very-high-resolution images.
4. Train a random-forest classifier using the dry-season NDVI time series plus selected bands.
5. Classify the district and assess accuracy with 600 independent stratified-random samples; suppose the overall accuracy is 88 % and the user's and producer's accuracies for "irrigated" are 84 % and 90 %.
6. Use the error matrix to adjust the mapped area: if 610 km² is mapped as irrigated, the bias-corrected estimate (Olofsson method) might be 640 ± 45 km² at 95 % confidence.

The entire workflow can run in a few minutes on a cloud platform at zero data cost — a task that would have taken months and thousands of dollars in data purchases in the 1990s.
:::

::: ai
**AI in remote sensing (preview)**

Machine learning now underpins most large-scale EO mapping. Deep convolutional networks and vision transformers segment buildings, roads and fields; detect ships, aircraft and vehicles; and classify land cover. **Geospatial foundation models** pre-trained on millions of unlabelled images — such as NASA–IBM's Prithvi, Clay, SatMAE and Google's AlphaEarth Foundations embeddings — can be fine-tuned for new tasks with few labels. Part XIII (Chapters 43–53) covers these methods in depth, including on-board AI that decides which images to keep and downlink.
:::

::: key
**Key takeaways**

- Remote sensing measures electromagnetic radiation reflected or emitted from the Earth. Planck's law and Wien's law explain why reflected sunlight dominates at 0.4–2.5 µm and thermal emission at 3–14 µm.
- The atmosphere scatters (strongly at short wavelengths) and absorbs (in gas bands) radiation; sensors observe through atmospheric windows and use atmospheric correction to retrieve surface reflectance.
- Each material has a characteristic spectral signature. Vegetation's red-edge contrast underlies NDVI and many other indices.
- Spatial, spectral, radiometric and temporal resolution trade against each other and against swath, data volume and cost.
- Image quality depends on MTF and SNR, not just GSD; NIIRS and GIQE relate them to interpretability.
- Geometric correction (geolocation and orthorectification with a DEM) turns images into maps; calibration and validation make measurements trustworthy.
- Data progress from Level 0 to Level 4; analysis-ready data, open standards (COG, STAC, Zarr) and cloud platforms let users analyse petabytes without downloading them.
- Classification, change detection and time-series analysis, with rigorous accuracy assessment, turn images into information. Free and open Landsat and Copernicus data have made EO a global public good.
:::

::: questions
**Review questions**

1. Using Wien's law, find the wavelength of peak emission for the Sun (5 772 K) and for the Earth's surface (300 K). What does this imply for optical and thermal sensors?
2. Why does the sky look blue, and why do Earth-observation sensors avoid the strong water-vapour and CO₂ absorption bands for surface imaging?
3. Calculate the NDVI for a vegetated pixel (red reflectance 0.05, near-infrared 0.45) and for bare soil (red 0.25, near-infrared 0.30).
4. Describe the four resolutions of a remote-sensing system and give an example of a trade-off between two of them.
5. Why can two imagers with the same ground sample distance produce images of very different quality?
6. Why does orthorectification need a digital elevation model? What happens to geolocation accuracy in mountainous terrain without one?
7. A classification is checked at 500 points: 180 forest correctly mapped, 20 forest mapped as non-forest, 30 non-forest mapped as forest and 270 non-forest correct. Calculate the overall accuracy and the user's and producer's accuracies for forest.
8. What are analysis-ready data, and how do cloud platforms and standards such as COG and STAC change the way users work with satellite archives?
:::
