---
title: Synthetic Aperture Radar
hero: ch15
abstract: Synthetic aperture radar (SAR) satellites carry their own illumination — microwave pulses — and so can image the Earth day and night, through clouds, smoke and rain. By recording the echoes of thousands of pulses as the satellite moves and processing them together, a SAR synthesises an antenna kilometres long and achieves resolutions as fine as 16 cm from hundreds of kilometres away. This chapter explains how SAR works — pulse compression, aperture synthesis, imaging geometry and modes — how radar waves interact with the surface, and why SAR images look so different from photographs. It then covers SAR interferometry, which measures ground movements of millimetres and maps topography, the main applications, and the rapidly growing fleet of government and commercial radar satellites, from Sentinel-1 and NISAR to constellations of 100 kg smallsats.
---

## Why Radar?

Optical and infrared sensors are passive: they need sunlight or thermal emission and they cannot see through clouds, which cover about two-thirds of the Earth at any moment. In the humid tropics, weeks or months can pass without a single clear optical image. A **radar** (radio detection and ranging) sends its own microwave pulses and measures the echoes. Because microwaves with wavelengths of centimetres to decimetres pass almost unaffected through clouds, rain (except at the shortest wavelengths), smoke, dust and darkness, an imaging radar can observe any place on Earth at any time. This makes SAR indispensable for disaster response, maritime surveillance, sea-ice monitoring, defence and any application that requires guaranteed acquisitions.

Radar also measures things that optical sensors cannot. The echo depends on the **roughness**, **geometry** and **moisture** of the surface rather than its colour; longer wavelengths **penetrate** vegetation, dry soil and ice; and because the radar records the exact **phase** of the echo, two radar images can be combined to measure distance changes of a few millimetres — the basis of **SAR interferometry (InSAR)**.

### A Short History

Side-looking airborne radars were developed for military reconnaissance in the 1950s, and the synthetic-aperture principle was invented by Carl Wiley at Goodyear in 1951. The first civilian imaging radar in space was carried by NASA's **Seasat** in 1978, which operated for only 106 days but proved the value of SAR for oceanography and land studies (@fig:seasat). The Shuttle Imaging Radar experiments (SIR-A 1981, SIR-B 1984, and the multi-frequency, multi-polarisation **SIR-C/X-SAR** in 1994, @fig:sirc) and the Soviet **Almaz** missions followed. The era of operational SAR began with ESA's **ERS-1** (1991), Japan's **JERS-1** (1992) and Canada's **RADARSAT-1** (1995). In 2000 the **Shuttle Radar Topography Mission (SRTM)** mapped the topography of 80 % of the Earth's land in 11 days. Today, dozens of radar satellites are in orbit (@fig:sartimeline).

::: figrow
![Seasat's L-band SAR image of the Massachusetts coast and Cape Cod, acquired in 1978. Seasat was the first civilian satellite to carry an imaging radar.](figures/photos/ch15_seasat.jpg){#fig:seasat}

![The SIR-C/X-SAR antenna — 12 m long and weighing 11 tonnes — being prepared for its first Space Shuttle flight in 1994. It was the first spaceborne SAR to image in three frequencies (L, C and X) and multiple polarisations.](figures/photos/ch15_sirc.jpg){#fig:sirc}
:::

![Milestones in spaceborne SAR, from Seasat to the 2025 launches of NISAR, BIOMASS and Sentinel-1D.](figures/out/ch15_timeline.svg){#fig:sartimeline width=100%}

## Radar Fundamentals

### Ranging and the Radar Equation

A radar transmits a short pulse and measures the delay $\tau$ of its echo; the distance (range) to the target is $R = c\tau/2$. The power of the echo is given by the **radar equation**:

$$P_r = \frac{P_t\,G^2\,\lambda^2\,\sigma}{(4\pi)^3\,R^4\,L}$$

where $P_t$ is the transmitted power, $G$ the antenna gain, $\lambda$ the wavelength, $\sigma$ the **radar cross-section** of the target (m²) and $L$ the system losses. The $R^4$ term — the signal spreads out on the way to the target and again on the way back — makes spaceborne radar demanding: an echo from 800 km is $10^{12}$ times weaker than from 800 m. For extended natural surfaces, the radar cross-section is expressed per unit area as the dimensionless **backscatter coefficient** $\sigma^0$ (sigma-nought), usually quoted in decibels; it ranges from about −25 dB for calm water to +5 dB or more for urban areas.

### Imaging Geometry

An imaging radar looks **sideways**, perpendicular to its direction of flight (@fig:sargeom). Looking straight down would be useless: points equally distant on both sides of the ground track would return their echoes at the same time and could not be separated. The direction of flight is called **azimuth** (or along-track); the direction of the radar beam is called **range**. The angle between the beam and the vertical at the satellite is the **look angle**; the angle at the ground between the beam and the local vertical is the **incidence angle**, slightly larger because of the Earth's curvature. The strip of ground illuminated between **near range** and **far range** is the **swath**.

![Side-looking SAR imaging geometry. The radar measures distance along the slant range; images are later projected onto the ground.](figures/out/ch15_geometry.svg){#fig:sargeom width=94%}

### Range Resolution and Pulse Compression

Two targets can be separated in range if their echoes do not overlap. For a pulse of duration $\tau_p$, the slant-range resolution is $c\tau_p/2$; a 10 µs pulse would give 1.5 km. To achieve metre-scale resolution with enough energy, radars transmit a long pulse whose frequency changes linearly with time — a **chirp** — and compress it on reception with a **matched filter** (@fig:chirp). The resolution then depends only on the bandwidth $B$ of the chirp:

$$\delta_r = \frac{c}{2B}, \qquad \delta_{g} = \frac{c}{2B\sin\theta_i}$$

where $\delta_g$ is the ground-range resolution. A bandwidth of 50 MHz gives 3 m slant-range resolution; modern X-band systems use up to 600–1 200 MHz for resolutions of 25 cm or better. Pulse compression is a beautiful example of signal processing replacing raw power: the transmitter can operate at modest peak power for a long pulse while the receiver recovers the resolution of a pulse hundreds of times shorter.

![Pulse compression. A 10 µs chirp sweeping 50 MHz (left) is compressed by matched filtering into a peak about 18 ns wide (right), giving 3 m slant-range resolution. The sidelobes at −13 dB are usually reduced further by weighting.](figures/out/ch15_chirp.svg){#fig:chirp width=98%}

### The Synthetic Aperture

In the azimuth direction, a real antenna of length $L$ forms a beam of angular width about $\lambda/L$. At range $R$ the beam footprint — the real-aperture azimuth resolution — is $\lambda R/L$: for a C-band radar ($\lambda$ = 5.6 cm) with a 10 m antenna at 850 km range, about 4.7 km. To achieve 5 m resolution with a real aperture would require an antenna 10 km long.

The **synthetic aperture** principle solves this (@fig:synthetic). As the satellite moves, each point on the ground stays inside the beam for a time during which the satellite travels a distance $L_{sa} = \lambda R/L$ — the length of the **synthetic aperture**. During this time the radar transmits thousands of pulses and records the amplitude and phase of each echo. Because the distance to the target first decreases and then increases, the echo's phase follows a characteristic quadratic history (equivalently, its **Doppler frequency** sweeps from positive to negative). A processor matches this phase history — just as pulse compression matches the chirp in range — and focuses all the echoes from each target into a single sharp point. The resulting azimuth resolution for stripmap imaging is

$$\delta_a \approx \frac{L}{2}$$

a remarkable result: the resolution is **independent of range and wavelength**, and *smaller* antennas give *finer* resolution (because their wider beams illuminate each target for longer). A 10 m antenna gives 5 m resolution whether the satellite is at 500 or 800 km.

![Aperture synthesis. Each target is illuminated by many successive pulses as the satellite passes; coherent processing combines them into a virtual antenna kilometres long.](figures/out/ch15_synthetic.svg){#fig:synthetic width=94%}

Turning raw echoes into an image — **SAR focusing** — requires the processing of enormous amounts of data with precise knowledge of the satellite's orbit. Classical algorithms include the **range–Doppler**, **chirp scaling** and **omega-k** algorithms, which work efficiently in the frequency domain using fast Fourier transforms; the **back-projection** algorithm, computationally heavier but exact for any geometry, has become practical with GPUs. Focusing a single Sentinel-1 scene takes minutes on a modern server; some new satellites focus images on board.

### Constraints: PRF, Ambiguities and Antenna Size

The radar must transmit pulses at a **pulse repetition frequency (PRF)** high enough to sample the Doppler bandwidth of the echoes — at least one pulse each time the satellite moves half an antenna length, $\text{PRF} > 2v/L$ — but low enough that the echo from the whole swath arrives before the next pulse is sent. Violating these conditions creates **ambiguities**: ghost images displaced in azimuth or range. Together they imply a **minimum antenna area**:

$$A = L\,W > \frac{4\,v\,\lambda\,R\,\tan\theta_i}{c}$$

which grows with wavelength (@fig:antenna). C-band and L-band satellites therefore need antennas of 10–30 m², while X-band smallsats can use antennas of about 1–2 m². Wide swaths, fine resolution and low ambiguities cannot all be achieved simultaneously with a conventional single-beam radar — the central trade-off of SAR design. New techniques overcome it: **digital beamforming** with multiple receive channels (as in Germany's planned HRWS mission and Sentinel-1 Next Generation), and the **SweepSAR** technique of NASA–ISRO's NISAR, which illuminates a wide swath and uses a large reflector with an array feed to "sweep" a narrow receive beam across it, following the echoes.

![Minimum antenna area for unambiguous single-beam imaging versus incidence angle, compared with real systems.](figures/out/ch15_antenna.svg){#fig:antenna width=84%}

The sensitivity of a SAR is described by its **noise-equivalent sigma-zero (NESZ)** — the backscatter coefficient that gives a signal equal to the noise. Values of −20 to −25 dB are typical of large government SARs; smallsats achieve −15 to −20 dB. Surfaces darker than the NESZ, such as calm water, appear as noise.

## Frequency and Polarisation

### Radar Bands

The choice of wavelength is the most fundamental decision in SAR design (@tbl:radarbands). Shorter wavelengths give finer resolution with small antennas and respond to small-scale roughness and the tops of vegetation canopies; longer wavelengths penetrate deeper into vegetation, soils and ice and remain coherent over longer periods for interferometry (@fig:penetration).

| Band | Frequency | Wavelength | Main characteristics | Example missions |
|---|---|---|---|---|
| Ka | 26.5–40 GHz | 0.75–1.1 cm | Very fine resolution; affected by rain; altimetry | SWOT (KaRIn interferometer) |
| Ku | 12–18 GHz | 1.7–2.5 cm | Altimeters, scatterometers, precipitation radar | CryoSat-2, Sentinel-3/6 altimeters |
| X | 8–12 GHz | 2.4–3.8 cm | High resolution with small antennas; canopy-top scattering | TerraSAR-X, COSMO-SkyMed, ICEYE, Capella, Umbra |
| C | 4–8 GHz | 3.8–7.5 cm | Good all-round compromise; oceans, ice, land | ERS, Envisat, RADARSAT, Sentinel-1, Gaofen-3 |
| S | 2–4 GHz | 7.5–15 cm | Intermediate penetration | NISAR (S-band), NovaSAR-1, Kondor-FKA |
| L | 1–2 GHz | 15–30 cm | Penetrates vegetation; long-term coherence for InSAR | ALOS-2/4, SAOCOM, NISAR (L-band) |
| P | 420–450 MHz (space allocation) | ≈ 69 cm | Penetrates forest canopy to trunks; biomass | BIOMASS |

: Radar frequency bands used for Earth observation (IEEE letter designations). {#tbl:radarbands}

![Schematic penetration of radar waves of different wavelengths into a forest. X-band scatters mainly from leaves at the top of the canopy, while L- and P-band reach the branches, trunks and ground.](figures/out/ch15_penetration.svg){#fig:penetration width=94%}

### Polarisation

Radar waves are polarised: the electric field oscillates in a particular plane. Spaceborne SARs transmit and receive horizontally (H) or vertically (V) polarised waves. An image is described by its transmit and receive polarisations: **HH**, **VV** (co-polarised) and **HV**, **VH** (cross-polarised). Single-polarisation radars record one channel, **dual-pol** radars two (for example VV + VH, Sentinel-1's standard over land), and **quad-pol** (fully polarimetric) radars all four with their relative phases. Some missions use **compact polarimetry**, transmitting circular polarisation and receiving two linear polarisations, as an efficient compromise (RADARSAT Constellation Mission).

Polarisation reveals the scattering mechanism. Smooth surfaces and the ocean return mostly co-polarised energy; volume scattering by randomly oriented branches and leaves **depolarises** the wave, producing strong cross-polarised (HV) returns — making HV an excellent indicator of vegetation and biomass. **Polarimetric decompositions** (such as the Pauli, Freeman–Durden and Cloude–Pottier entropy/alpha decompositions) separate each pixel's response into surface, double-bounce and volume components, often displayed as red–green–blue colour images.

## How the Surface Looks to a Radar

### Brightness: Roughness, Geometry and Moisture

The brightness of a SAR image depends on how much energy is scattered back towards the radar (@fig:sarmech):

- **Smooth surfaces** (calm water, roads, runways, smooth sand) reflect the wave away like a mirror and appear **dark**. A surface is "smooth" if its height variations are small compared with the wavelength (the Rayleigh criterion), so the same surface can be smooth at L-band and rough at X-band.
- **Rough surfaces** (ploughed fields, wind-roughened water, rocky terrain) scatter in all directions and appear **brighter**.
- **Double-bounce** reflection — wave bouncing off the ground and then a vertical wall back to the radar — makes buildings, ships, bridges and flooded forests appear **very bright**. Corner reflectors used for calibration exploit this effect.
- **Volume scattering** within vegetation canopies, dry snow or sea ice produces moderate, depolarised returns.
- **Moisture** increases the dielectric constant of soils and vegetation and therefore their reflectivity — wet soil is brighter than dry soil — which allows SAR to measure soil moisture and to detect flooding under vegetation.

![The main scattering mechanisms that determine the brightness of SAR images.](figures/out/ch15_mechanisms.svg){#fig:sarmech width=98%}

Backscatter also depends strongly on the incidence angle (@fig:sigma0). Calm water reflects strongly only near vertical incidence and is black at normal SAR angles, which is why oil slicks — which damp the small capillary waves on the sea — appear as dark patches and can be detected. Forests are relatively insensitive to angle, while soils and the wind-roughened sea darken steadily with increasing incidence angle. The ocean's backscatter depends on wind speed and direction, which is how SAR and scatterometers measure **ocean winds**.

![Schematic variation of backscatter with incidence angle for different surfaces at C-band.](figures/out/ch15_sigma0.svg){#fig:sigma0 width=84%}

### Geometric Distortions

Because a radar measures distances rather than angles, terrain is distorted in characteristic ways (@fig:distortions):

- **Foreshortening**: slopes facing the radar appear compressed and bright.
- **Layover**: when a slope facing the radar is steeper than the incidence angle, its top is closer to the radar than its bottom and is imaged *before* it — mountains appear to lean towards the radar, and tall buildings lay over onto the street in front of them.
- **Shadow**: slopes facing away from the radar that are steeper than the grazing angle receive no energy and appear black.

![Radar geometric distortions in mountainous terrain: foreshortening, layover and shadow.](figures/out/ch15_distortions.svg){#fig:distortions width=96%}

Distortions are corrected by **terrain-corrected geocoding** using a DEM. Brightness variations due to slope can also be corrected — **radiometric terrain correction** converts backscatter to the "terrain-flattened" coefficient $\gamma^0$ — but layover and shadow areas contain no recoverable information. Combining images from ascending and descending passes, which look from opposite directions, fills many gaps.

### Speckle

SAR images have a characteristic grainy appearance called **speckle** (@fig:speckle). Each resolution cell contains many individual scatterers whose echoes add coherently with random phases; the sum varies randomly from pixel to pixel even over a uniform surface. Speckle is not noise in the usual sense — it is a real, deterministic consequence of coherent imaging that repeats if the same scene is imaged under identical conditions — but it makes single-look images hard to interpret. Speckle is reduced by **multi-looking** (averaging several independent looks, at the cost of resolution), by averaging images over time, and by adaptive filters (Lee, Frost, non-local means, and deep-learning despeckling).

![Speckle in a simulated SAR scene. Averaging 4 or 16 independent looks reduces the speckle but also reduces resolution.](figures/out/ch15_speckle.png){#fig:speckle width=98%}

::: figrow
![The first L-band image from NISAR, acquired on 21 August 2025, showing Mount Desert Island on the coast of Maine. Forests appear bright, water dark and urban areas very bright.](figures/photos/ch15_nisarfirst.jpg){#fig:nisarfirst}

![An early NISAR image of farmland and wetlands in North Dakota. Fields with different crops, moisture and roughness show distinct brightness; centre-pivot fields appear as circles.](figures/photos/ch15_ndakota.jpg){#fig:ndakota}
:::

## Imaging Modes

By steering its beam electronically (with a phased-array antenna) or mechanically (by rotating the spacecraft), a SAR can trade resolution against swath width in several **imaging modes** (@fig:sarmodes):

- **Stripmap**: the beam points at a fixed angle and sweeps a continuous strip; resolution about half the antenna length (typically 3–5 m), swath 30–80 km.
- **ScanSAR**: the beam switches periodically between several adjacent sub-swaths, illuminating each in short bursts. The swath becomes several times wider (250–500 km) at the cost of coarser azimuth resolution. ESA's **TOPS** (Terrain Observation by Progressive Scans) mode, used by Sentinel-1's Interferometric Wide-swath (IW) mode, also steers the beam forward-to-backward during each burst, giving uniform image quality across the swath — important for interferometry.
- **Spotlight**: the beam is steered backwards during the pass to keep illuminating the same small area for longer, synthesising a longer aperture and achieving resolutions of 0.25–1 m over a few kilometres. **Staring spotlight** and **dwell** modes extend this further.
- **Wave mode** collects small vignettes over the open ocean to measure wave spectra, and specialised modes such as NISAR's **SweepSAR** combine wide swaths with fine resolution.

![Schematic SAR imaging modes. Grey arrows show the ground track; the radar looks to the right.](figures/out/ch15_modes.svg){#fig:sarmodes width=98%}

![Resolution versus swath width for the imaging modes of representative SAR missions. Each system offers a family of modes along a line of roughly constant number of pixels across the swath.](figures/out/ch15_resswath.svg){#fig:resswath width=86%}

## SAR Interferometry

### The Principle

A SAR image is a matrix of complex numbers: each pixel has an **amplitude** (brightness) and a **phase** that depends on the exact two-way distance between the antenna and the scatterers in the pixel, measured in fractions of a wavelength. The phase of a single image looks random, because it includes the unknown arrangement of scatterers within each pixel. But if two images are acquired from nearly the same position, this random part is almost identical in both, and the **phase difference** between them — the **interferogram** — depends only on the difference in distance (@fig:insargeom):

$$\Delta\phi = \frac{4\pi}{\lambda}\,\Delta R$$

One complete cycle of phase (a **fringe**) corresponds to a change in distance of half a wavelength — 2.8 cm at C-band and 12 cm at L-band. Since phase can be measured to a small fraction of a cycle, InSAR measures distance changes of **millimetres** from hundreds of kilometres away.

![Geometry of SAR interferometry. The phase difference between two acquisitions depends on topography (through the baseline geometry) and on any movement of the ground between them.](figures/out/ch15_insargeom.svg){#fig:insargeom width=94%}

The interferometric phase has several contributions: the **topography** (because the two antennas view the terrain from slightly different positions separated by the **baseline**), any **deformation** of the ground along the line of sight between acquisitions, differences in **atmospheric delay** (mainly water vapour in the troposphere and electrons in the ionosphere), orbit errors, and noise. Different applications isolate different components.

### Measuring Topography

If the two images are acquired at the same time from two antennas separated by a known baseline — **single-pass** or **bistatic** interferometry — there is no deformation or atmospheric change, and the phase directly measures height. The **height of ambiguity**, the height change that produces one fringe, is $h_a = \lambda R \sin\theta/(2B_\perp)$, where $B_\perp$ is the perpendicular baseline; longer baselines give greater height sensitivity.

The **Shuttle Radar Topography Mission** (February 2000) used a C-band antenna in the Shuttle's payload bay and a second receive antenna on the end of a 60 m mast to map 80 % of the Earth's land surface between 60° N and 56° S, producing the first near-global high-resolution DEM (@fig:srtm). Germany's **TanDEM-X** mission (2010) flew a second satellite in close formation, a few hundred metres from TerraSAR-X, and produced the global **WorldDEM** / Copernicus DEM with 12 m posting and a vertical accuracy of a few metres — the most accurate consistent global elevation model.

![SRTM interferometric height of Lanai and West Maui, Hawaii. Each cycle of colours represents a fixed increment of elevation.](figures/photos/ch15_srtm.jpg){#fig:srtm width=72%}

### Measuring Deformation

**Differential InSAR (DInSAR)** uses two images taken days to years apart by the same satellite from nearly the same orbit. After the topographic phase is removed using a DEM, the remaining fringes show how the ground moved between the acquisitions. The first spectacular demonstration was the 1992 Landers, California, earthquake, imaged by ERS-1 (published in *Nature* in 1993). Since then InSAR has mapped the deformation of almost every major earthquake (@fig:izmit), volcanic inflation and deflation (@fig:mogi), landslides, glacier and ice-sheet flow, and subsidence caused by groundwater pumping, mining, oil and gas extraction and tunnelling.

![Wrapped interferogram from ERS-1 and ERS-2 data showing ground displacement from the magnitude 7.6 Izmit, Turkey, earthquake of 17 August 1999. Each colour cycle represents 28 mm of motion towards or away from the satellite.](figures/photos/ch15_izmit.jpg){#fig:izmit width=70%}

![Synthetic interferogram (left) and displacement profile (right) for a volcano inflating because of 12 million m³ of magma injected at 4 km depth (Mogi model). The radar measures only the component of motion along its line of sight, so the fringe pattern is asymmetric.](figures/out/ch15_mogi.png){#fig:mogi width=98%}

### Coherence, Time Series and Accuracy

InSAR works only if the scatterers within each pixel remain arranged in the same way between acquisitions — that is, if the images remain **coherent**. **Coherence** (0 to 1) measures this. It is high over cities and bare rock, but decays over vegetation as leaves move and plants grow, and is destroyed by snowfall, ploughing or flooding (@fig:coherence). Longer wavelengths stay coherent longer, which is why L-band missions such as ALOS-2 and NISAR are preferred over vegetated land, and why short revisit intervals (6–12 days) are valuable. Loss of coherence is itself useful: **coherence change detection** reveals damaged buildings after earthquakes and disturbed ground.

![Schematic decay of interferometric coherence with time between acquisitions for different surfaces and wavelengths.](figures/out/ch15_coherence.svg){#fig:coherence width=84%}

The biggest error source for deformation measurements is the **atmosphere**: variations in water vapour delay the radar signal by amounts equivalent to several centimetres. **Multi-temporal InSAR** techniques overcome this by analysing stacks of dozens to hundreds of images: **persistent scatterer interferometry (PSI)** identifies stable point-like targets (buildings, rocks, infrastructure) and estimates their motion history with millimetre-per-year precision, while **small baseline subset (SBAS)** methods analyse distributed targets. The **European Ground Motion Service (EGMS)**, launched by Copernicus in 2022, provides Sentinel-1 PSI ground-motion measurements for almost all of Europe, updated annually — billions of measurement points showing subsidence of cities, motion of landslides and the stability of dams, bridges and railways.

Other interferometric techniques include **along-track interferometry**, which uses two antennas separated in the flight direction to measure the velocity of moving targets such as ocean currents and vehicles (ground moving target indication, Chapter 19), and **SAR tomography**, which combines many baselines to resolve the vertical structure of forests and buildings — a key technique of ESA's BIOMASS mission. Where coherence is low, **offset tracking** measures large displacements (metres) by correlating image patches, for example to map glacier velocities.

## Applications

SAR has become essential in many fields (@tbl:sarapps).

| Field | Applications | Preferred band and technique |
|---|---|---|
| Disasters | Flood mapping (water appears dark), earthquake and landslide deformation, building damage, volcanic monitoring | All bands; amplitude change, coherence change, DInSAR |
| Oceans | Ship detection, oil-spill detection, ocean wind and waves, currents, internal waves | C and X; wave mode; along-track interferometry |
| Sea ice and polar regions | Ice type and concentration charts, iceberg tracking, ice-sheet velocity and grounding lines | C and L; ScanSAR; offset tracking |
| Geohazards and infrastructure | Subsidence of cities, mines and oilfields; stability of dams, bridges, railways, pipelines | C, L, X; PSI, SBAS time series |
| Forestry and carbon | Deforestation alerts in cloudy tropics, forest biomass and height | L, P; cross-polarisation, tomography |
| Agriculture | Crop type mapping, crop growth, soil moisture, rice paddies (flooded fields) | C, L; time series of polarimetric backscatter |
| Hydrology | Soil moisture, wetlands, snow water equivalent, river and lake levels | L, C; Ka-band interferometry (SWOT) |
| Defence and security | All-weather imaging, change detection, moving targets, maritime surveillance | X (high resolution), all modes |

: Major applications of spaceborne SAR. {#tbl:sarapps}

::: example
**Example: mapping a flood with Sentinel-1**

A major river floods during the monsoon, under persistent cloud.

1. Select a Sentinel-1 IW image acquired during the flood and a reference image from the same orbit before the flood.
2. Calibrate both to $\sigma^0$, apply terrain correction with the Copernicus DEM, and reduce speckle with a multi-temporal filter.
3. Open floodwater appears very dark (below about −18 dB in VV). Pixels that were bright before and dark now are classified as newly flooded; a threshold chosen automatically from the image histogram (Otsu's method) or a trained classifier separates water from land.
4. Flooded vegetation and flooded urban areas can appear *brighter* because of double bounce between water and trunks or walls; these are detected as increases in backscatter or drops in coherence.
5. Remove areas of radar shadow and permanent water using a height-above-nearest-drainage map and a reference water mask.

With free Sentinel-1 data typically available within a few hours of acquisition, and services such as the Copernicus Emergency Management Service and the Global Flood Monitoring system, flood maps can be produced the same day — regardless of clouds.
:::

## SAR Missions in 2026

### Government Missions

| Mission | Agency / country | Band | Launch | Key features |
|---|---|---|---|---|
| Sentinel-1A, 1C, 1D | EU Copernicus / ESA | C | 2014, 2024, 2025 | 693 km SSO, 12-day repeat per satellite; IW mode 250 km at 5 × 20 m; systematic global acquisitions, free data |
| RADARSAT Constellation Mission | Canada (CSA) | C | 2019 | Three satellites; 4-day repeat; compact polarimetry; maritime surveillance |
| TerraSAR-X / TanDEM-X / PAZ | Germany (DLR, Airbus) / Spain | X | 2007, 2010, 2018 | High resolution; bistatic interferometry (WorldDEM) |
| COSMO-SkyMed (1st and 2nd gen.) | Italy (ASI, Defence) | X | 2007– | Dual-use constellation; spotlight to 0.35 m class |
| ALOS-2 / ALOS-4 | Japan (JAXA) | L | 2014, 2024 | PALSAR-3 on ALOS-4 images a 200 km swath at 3 m |
| SAOCOM 1A/1B | Argentina (CONAE) | L | 2018, 2020 | Full polarimetry; soil moisture; cooperation with Italy |
| Gaofen-3 series | China | C | 2016– | Multi-mode, up to 1 m |
| EOS-04 (RISAT-1A) | India (ISRO) | C | 2022 | Agriculture, flood, forestry |
| Kondor-FKA | Russia | S | 2023, 2024 | Up to 1 m class |
| NISAR | NASA / ISRO | L + S | 2025 | 12 m reflector, SweepSAR, 242 km swath, 12-day repeat; global systematic coverage, free data |
| BIOMASS | ESA | P | 2025 | First spaceborne P-band SAR; forest biomass and height by tomography |
| ROSE-L | EU Copernicus / ESA | L | ≈ 2029 | Copernicus Expansion mission |
| Harmony | ESA | C (receive-only) | ≈ 2029 | Two satellites flying with a Sentinel-1 for multi-static measurements |

: Major government SAR missions (selected). {#tbl:sargov}

Two missions launched in 2025 stand out. **NISAR**, a partnership between NASA (L-band radar, 12 m deployable mesh reflector, data systems) and ISRO (S-band radar, spacecraft bus, GSLV launch), is the first radar mission to map nearly all of the Earth's land and ice surfaces twice every 12 days at two frequencies. Launched on 30 July 2025, it began its science phase in November 2025; its free data — tens of terabytes per day — will measure ground deformation, ice-sheet dynamics, forest biomass and agriculture globally. ESA's **BIOMASS**, launched on 29 April 2025, carries the first spaceborne P-band SAR. At 70 cm wavelength the radar penetrates to tree trunks, allowing the mass of forests — and hence their carbon content — to be estimated. Because P-band frequencies are shared with powerful military space-surveillance radars, BIOMASS is not permitted to operate over Europe and North America.

### The Commercial SAR Revolution

Until 2018, all SAR satellites were large government systems weighing 1–3 tonnes. In January 2018 the Finnish start-up **ICEYE** launched ICEYE-X1, the first SAR satellite under 100 kg. Its innovations — a compact X-band phased array, high-power gallium-nitride amplifiers, batteries that supply short bursts of several kilowatts, and agile spacecraft that rotate to perform spotlight imaging — showed that useful SAR imaging was possible from smallsats costing a few million dollars. By July 2026 ICEYE had launched 76 satellites, offered resolutions down to 16 cm with its fourth-generation design, and was producing about 50 satellites per year. Other commercial operators include **Capella Space** (USA, acquired in July 2025 by the quantum-computing company IonQ), **Umbra** (USA), **Synspective** (StriX, Japan), **iQPS** (QPS-SAR, Japan) and a growing number of Chinese commercial SAR companies (@fig:sarfleets).

![Active SAR satellites by operator or series in October 2026 (name-matched in the CelesTrak SATCAT, approximate).](figures/out/ch15_fleets.svg){#fig:sarfleets width=86%}

Commercial SAR constellations offer frequent revisit (several images per day of a target), fast tasking and delivery, and very high resolution, and have found strong markets in defence and intelligence (the war in Ukraine was a turning point), insurance (rapid flood extent after events), maritime monitoring and infrastructure. Government missions provide the systematic, well-calibrated, free global coverage needed for science and public services; the two are increasingly complementary.

![SIR-C/X-SAR multi-frequency image of the Kilauea volcano, Hawaii, in 1994. Colours combine L-band and C-band channels in different polarisations: rough young lava flows appear bright, smooth older surfaces darker.](figures/photos/ch15_kilauea.jpg){#fig:kilauea width=56%}

## Design Example: An X-band SAR Smallsat

::: example
**Example: sizing a 1 m-class SAR microsatellite**

*Requirements:* ≈ 1 m stripmap resolution, NESZ better than −15 dB, 550 km orbit, 30° incidence.

1. **Wavelength.** X-band (9.65 GHz, λ = 3.1 cm) allows a small antenna.
2. **Antenna.** A 3.2 m × 0.4 m phased array (1.28 m²) exceeds the minimum area of about 1.2 m² for these conditions (@fig:antenna). Stripmap azimuth resolution ≈ L/2 = 1.6 m; spotlight mode can do better.
3. **Bandwidth.** 300 MHz gives 0.5 m slant-range and 1.0 m ground-range resolution at 30° incidence.
4. **Gain.** With 60 % aperture efficiency, $G = 4\pi A\eta/\lambda^2 \approx 10\,000$ (40 dBi).
5. **Sensitivity.** With 800 W average radiated power (4 kW peak at 20 % duty cycle), slant range 650 km, 3 dB noise figure and 3 dB losses, the radar equation for distributed targets gives NESZ ≈ −15.6 dB — just meeting the requirement.
6. **Power.** 4 kW peak cannot come from a smallsat's solar arrays (a few hundred watts); a high-rate battery supplies imaging bursts of one to two minutes per orbit, recharged between collections.
7. **Data.** Sampling 300 MHz of bandwidth with 8-bit complex samples (reduced to about 4 bits by block-adaptive quantisation) produces a raw data rate of roughly 2–3 Gbit/s during imaging; a 20-second collection produces about 6 GB, downlinked over X-band or Ka-band.

The result — a satellite of about 100 kg with a deployable antenna — is close to the design of the first commercial SAR microsatellites.
:::

::: ai
**AI and SAR**

SAR images are difficult for humans to interpret but well suited to machine learning, which is now used for ship and aircraft detection, sea-ice classification, despeckling, flood and building-damage mapping, and translating SAR into optical-like images. Deep learning also helps unwrap interferometric phase, separate atmospheric noise from deformation in InSAR time series, and detect anomalies in millions of persistent scatterers — for example, early warning of landslides or structural failures. Chapter 44 discusses these methods.
:::

::: key
**Key takeaways**

- SAR provides its own microwave illumination and images day and night through clouds, smoke and rain.
- Range resolution comes from pulse bandwidth ($c/2B$) through pulse compression; azimuth resolution comes from aperture synthesis and is about half the antenna length, independent of range.
- The PRF constraints imply a minimum antenna area; resolution and swath trade off in stripmap, ScanSAR/TOPS and spotlight modes, and digital beamforming and SweepSAR relax the trade.
- Wavelength determines penetration and interferometric coherence: X-band for high resolution, C-band for all-round use, L- and P-band for forests and long-term interferometry.
- SAR brightness depends on roughness, geometry and moisture; images contain speckle and geometric distortions (foreshortening, layover, shadow).
- Interferometry measures topography (SRTM, TanDEM-X) and ground deformation with millimetre precision; persistent-scatterer time series monitor cities and infrastructure across whole continents.
- The SAR fleet now combines systematic government missions (Sentinel-1, NISAR, BIOMASS, ALOS-4) with fast-growing commercial constellations of 100 kg smallsats.
:::

::: questions
**Review questions**

1. Why can a SAR image through clouds, smoke and darkness while an optical imager cannot?
2. A SAR transmits a chirp of 300 MHz bandwidth. What is its slant-range resolution, and what is its ground-range resolution at an incidence angle of 35°?
3. A stripmap SAR has a 3.2 m long antenna. What is its approximate azimuth resolution, and why does it not depend on range?
4. Explain how the pulse repetition frequency constrains the minimum antenna area of a SAR.
5. Compare X-, C- and L-band SAR for forest mapping, sea-ice monitoring and high-resolution imaging of ports.
6. Describe foreshortening, layover and shadow, and explain what causes speckle.
7. In C-band differential interferometry (λ = 5.55 cm), how much line-of-sight ground motion does one full interferometric fringe represent?
8. How have commercial SAR constellations of 100 kg satellites changed what SAR can deliver, compared with large government missions?
:::
