---
title: Electro-Optical and Infrared Imaging Satellites
hero: ch14
abstract: Electro-optical and infrared (EO/IR) satellites are cameras in orbit. They range from government "workhorse" missions such as Landsat and Sentinel-2, which map the whole land surface every few days at 10–30 m, through commercial constellations of hundreds of shoebox-sized satellites that image the planet daily, to very-high-resolution satellites that can see objects 30 cm across. This chapter explains how these systems are designed — telescopes, focal planes, time-delay integration, agility and data handling — and why the laws of optics and photon statistics set their limits. It then covers thermal infrared imaging for temperature and fire, imaging spectroscopy (hyperspectral) for minerals, vegetation chemistry and methane, global moderate-resolution imagers, and the state of the industry in 2026.
---

## The Family of EO/IR Imagers

**Electro-optical (EO)** sensors convert visible and near-infrared light into electrical signals; **infrared (IR)** sensors extend this to the short-wave, mid-wave and long-wave infrared. Together they form the largest and most familiar class of Earth-observation satellites. Their principal parameters — resolution, spectral bands, swath and revisit — were introduced in Chapter 13; their instrument building blocks (telescopes, detectors, scanning methods) in Chapter 12. This chapter looks at complete systems.

EO/IR satellites are usually grouped by their spatial resolution, which largely determines their applications, size and cost (@tbl:eoclasses).

| Class | GSD | Swath | Typical missions | Typical uses |
|---|---|---|---|---|
| Low resolution | 250 m – 5 km | 1 000 – 3 000 km | MODIS, VIIRS, Sentinel-3, geostationary imagers | Weather, climate, ocean colour, fires, global vegetation |
| Medium resolution | 10 – 100 m | 100 – 300 km | Landsat 8/9, Sentinel-2, CBERS, Resourcesat | Land cover, agriculture, forestry, water, change monitoring |
| High resolution | 1 – 10 m | 10 – 60 km | PlanetScope, SPOT 6/7, Gaofen-1, RapidEye (retired) | Field-level agriculture, mapping, monitoring |
| Very high resolution (VHR) | 0.25 – 1 m | 5 – 20 km | WorldView, Pléiades Neo, SkySat, BlackSky, Jilin-1, Cartosat-3 | Urban mapping, infrastructure, defence and intelligence, disaster damage |
| Extremely high resolution | < 0.25 m | < 5 km | Military reconnaissance; very-low-orbit commercial concepts | Detailed object identification |

: Classes of EO/IR imaging satellites. {#tbl:eoclasses}

There is also a sharp division between **government science and operational missions**, which emphasise calibration accuracy, long-term continuity and free data, and **commercial missions**, which emphasise resolution, revisit, responsiveness and fast delivery to paying customers. The two are increasingly complementary: scientists use commercial data under licence, and companies build value-added products on top of free government data.

## Landsat and Sentinel-2: The Workhorses

### Landsat — Fifty Years of Land Observation

The Landsat programme is managed jointly by NASA (which builds and launches the satellites) and the US Geological Survey (which operates them and archives and distributes the data). It has observed the Earth's land surface continuously since 1972 (@fig:landsat). Its value comes from **continuity**: the same places observed in consistent, carefully cross-calibrated ways for more than five decades, providing the longest record of human and natural change on the land surface.

![The Landsat missions. Landsat 5 holds the record for the longest-operating Earth-observation satellite (28.8 years). The free-data decision of 2008 transformed the use of the archive.](figures/out/ch14_landsat.svg){#fig:landsat width=96%}

Landsat 8 (launched 2013) and Landsat 9 (2021) fly in the same 705 km sun-synchronous orbit with a 10:00 a.m. descending-node crossing. Each repeats its ground track every 16 days. They are spaced half a cycle apart, so together they revisit every point every **8 days**. Each carries two instruments:

- The **Operational Land Imager (OLI / OLI-2)**, built by Ball Aerospace, is a **push-broom** imager with a four-mirror telescope. Its focal plane of 14 modules carries more than 6 500 detectors per spectral band across the 185 km swath (twice as many for the panchromatic band). It has nine bands — including a coastal-aerosol band (0.43–0.45 µm) and a cirrus band (1.36–1.39 µm) for detecting thin high clouds — at 30 m (15 m panchromatic). Landsat 9's OLI-2 records data with 14-bit quantisation, giving more brightness levels than Landsat 8's 12 bits.
- The **Thermal Infrared Sensor (TIRS / TIRS-2)**, built by NASA Goddard, images in two long-wave bands (10.6–11.2 and 11.5–12.5 µm) at 100 m. It uses **quantum-well infrared photodetectors (QWIPs)** cooled to about 43 K by a cryocooler. TIRS-2 corrected a stray-light problem discovered in TIRS on Landsat 8.

Landsat 7, launched in 1999, suffered a failure of its scan-line corrector in 2003 that left wedge-shaped gaps in its images. Even so, it continued to provide useful data until January 2024 and was decommissioned in June 2025. The planned successor, **Landsat Next**, was originally conceived as a three-satellite "superspectral" constellation with 26 bands, 10–20 m resolution and a 6-day revisit, launching around 2030–31. It was restructured in the US administration's 2026 budget proposal, and its final architecture was still under review in 2026.

### Sentinel-2 — The Copernicus High-Resolution Imager

The European Union's **Sentinel-2** mission, developed by ESA with Airbus as prime contractor, has become the most widely used medium-resolution optical mission. Each satellite carries the **Multispectral Instrument (MSI)**, a push-broom imager with a 15 cm three-mirror anastigmat telescope and two focal planes (visible/near-infrared silicon and short-wave infrared HgCdTe). It records **13 spectral bands**: four at 10 m, six at 20 m and three atmospheric bands at 60 m, across a **290 km swath**. Its three **red-edge** bands at 705, 740 and 783 nm are especially valuable for vegetation monitoring (@fig:eobands).

The satellites fly at 786 km with a 10:30 a.m. descending node; each repeats every 10 days and two together give a **5-day revisit** at the equator — 2–3 days at mid-latitudes, where swaths overlap. Sentinel-2A was launched in 2015, 2B in 2017 and **2C in September 2024** on the last flight of Europe's Vega rocket. Sentinel-2C took over from 2A in early 2025, and 2A continues in an extended campaign. Sentinel-2D is planned for about 2028, and a **Sentinel-2 Next Generation** with finer resolution and more bands is planned for the 2030s.

![Spectral bands of representative EO/IR sensors. Commercial imagers concentrate bands in the visible and near-infrared; science missions add short-wave and thermal infrared bands for atmospheric correction, geology, fire and temperature.](figures/out/ch14_bands.svg){#fig:eobands width=98%}

| Parameter | Landsat 8/9 | Sentinel-2A/B/C |
|---|---|---|
| Operators | NASA (development) / USGS (operations) | EU Copernicus programme; developed and operated by ESA |
| Orbit | 705 km SSO, 10:00 descending | 786 km SSO, 10:30 descending |
| Revisit (one / two satellites) | 16 / 8 days | 10 / 5 days |
| Swath | 185 km | 290 km |
| Bands | 9 reflective + 2 thermal | 13 reflective |
| Resolution | 15 m pan, 30 m MS, 100 m thermal | 10, 20 and 60 m |
| Quantisation | 12 bit (L8), 14 bit (L9) | 12 bit |
| Data volume | ≈ 1 500 scenes per day (two satellites) | ≈ 1.6 TB of compressed data per satellite per day |
| Data policy | Free and open (since 2008) | Free, full and open (since 2014) |

: Comparison of the two leading medium-resolution land-imaging missions. {#tbl:landsats2}

The two missions are complementary. Landsat has the longer record, thermal bands and stringent calibration; Sentinel-2 has finer resolution, red-edge bands and more frequent revisit. NASA's **Harmonized Landsat and Sentinel-2 (HLS)** product combines them into a single 30 m surface-reflectance record with observations every 2–3 days.

Other national programmes contribute medium-resolution data: the China–Brazil **CBERS** series, India's **Resourcesat** (LISS-III and AWiFS) and China's **Gaofen-1/6** wide-field cameras. Commercial wide-area constellations also contribute, such as **EarthDaily**, which is building a constellation designed for scientific-grade daily global coverage.

## Very-High-Resolution Imaging

### The Optics of Seeing Small Things

For a push-broom imager, the ground sampling distance is set by the detector pixel pitch $p$, the telescope focal length $f$ and the altitude $h$:

$$\text{GSD} = \frac{p\,h}{f}$$

A satellite at 600 km with 5 µm detectors therefore needs a **10 m focal length** to achieve 30 cm GSD. Such long focal lengths are folded into compact telescopes with three or four curved mirrors (Chapter 12).

A long focal length alone is not enough: the aperture must be large enough that diffraction does not blur the image. The smallest resolvable separation on the ground is roughly given by the Rayleigh criterion:

$$r \approx 1.22\,\frac{\lambda\,h}{D}$$

For λ = 0.6 µm and h = 600 km, resolving 30 cm requires an aperture of at least 1.5 m by this criterion. In practice, however, systems sample somewhat finer than the Rayleigh limit and recover detail through processing (@fig:optics). This is the fundamental reason why very-high-resolution satellites are large. WorldView-3 has a 1.1 m telescope and weighs about 2 800 kg, while a 3U CubeSat with a 9 cm aperture cannot do better than about 3 m. It also explains the military reconnaissance satellites believed to have 2.4 m mirrors, and the commercial ventures aiming for 10 cm. These either use very large telescopes or fly much lower (see "Very low Earth orbit" below).

![Diffraction-limited ground resolution versus telescope aperture at three altitudes, with the published panchromatic GSD of representative systems. Small apertures (Sentinel-2) are deliberately not diffraction-limited; VHR systems sample at or slightly beyond the diffraction limit.](figures/out/ch14_optics.svg){#fig:optics width=86%}

### Not Enough Photons: Time-Delay Integration

The second limit is light. As the GSD shrinks, each pixel collects light from a smaller area, for a shorter time. The satellite moves 7 km/s over the ground, so a 31 cm pixel is crossed in about 45 µs. @fig:photons estimates the number of photo-electrons collected per pixel in one line time for several systems. A 10 m Sentinel-2 pixel collects tens of thousands of electrons, but a 31 cm WorldView-3 pixel collects only a few hundred. This gives a shot-noise-limited signal-to-noise ratio of about 20, far too low for good imagery.

![Estimated photo-electrons per pixel collected in one line time for representative imagers. VHR systems collect far fewer photons per line and rely on time-delay integration (TDI) or frame stacking to reach useful signal-to-noise ratios.](figures/out/ch14_photons.svg){#fig:photons width=90%}

The solution is **time-delay integration (TDI)**. A TDI detector has many rows (stages) of pixels aligned along the direction of motion. As the image of a ground point moves across the detector, the charge collected in one row is shifted to the next row in exact synchrony. In this way the same ground point is integrated by 8, 16, 32, 64 or more rows in succession. The signal grows in proportion to the number of stages $N$ while the shot noise grows only as $\sqrt{N}$. Modern VHR focal planes use CCD or CMOS TDI detectors with up to 64–128 stages, selectable to adapt to illumination — fewer stages for bright desert, more for dark forest or low sun. TDI requires extremely precise synchronisation between the charge transfer and the ground image motion, which depends on altitude, satellite speed, viewing angle and Earth rotation; errors smear the image.

Frame cameras, such as those on PlanetScope Doves and SkySats, use another approach. They take many overlapping short exposures and combine ("stack") them on the ground. This also allows **super-resolution** processing that recovers detail finer than a single frame.

### Agility, Pointing and Collection Modes

A VHR satellite with a swath of only 10–15 km would take years to map the whole Earth. Instead, VHR satellites are **agile**: they rotate the whole spacecraft to point the telescope at targets up to 30–45° away from the ground track, using control-moment gyroscopes (CMGs) or large reaction wheels (Chapter 6). An agile satellite can typically retarget across hundreds of kilometres in about ten seconds, collecting many separate targets on a single pass or sweeping its view to build an area larger than its swath (@fig:modes).

![Collection modes of an agile VHR satellite: a long strip along the ground track, an area mosaic built from adjacent strips on one pass, a stereo pair from fore and aft views, and many point targets collected in rapid succession.](figures/out/ch14_modes.svg){#fig:modes width=98%}

Off-nadir viewing has a cost: the distance to the ground increases and the ground is viewed obliquely, so the GSD grows (@fig:offnadir). At 30° off nadir, a satellite with 31 cm nadir GSD produces imagery with about 40 cm (geometric mean) GSD; at 45°, about 60 cm. Oblique views also suffer more atmospheric haze, longer building shadows and greater layover of tall structures — so customers specify a maximum off-nadir angle when ordering.

![Ground sampling distance versus off-nadir angle for a WorldView-3-like satellite. The dashed curve gives the distance from the ground track: viewing up to 30° off nadir gives access to a strip about 725 km wide.](figures/out/ch14_offnadir.svg){#fig:offnadir width=86%}

### Stereo Imaging and 3-D Mapping

By imaging the same area from two different directions on the same pass — looking forward and then backward — an agile satellite collects a **stereo pair**. Tall features appear shifted (parallax) between the two images in proportion to their height. Photogrammetric software measures the parallax by automatically matching features and computes a **digital surface model (DSM)** (@fig:stereo). The precision of height measurement depends on the ratio of the stereo base to the height (B/H) and the precision of image matching. VHR stereo pairs routinely produce DSMs with 1–2 m vertical accuracy. They are used to build 3-D city models, measure volumes of mines and stockpiles, and produce terrain data for defence and aviation. Some missions, such as Japan's ALOS PRISM (2006–2011) and the Chinese ZY-3 series, carry two or three fixed cameras looking forward, nadir and backward to collect stereo continuously.

![Stereo imaging geometry. Two views separated by base B from height H see a tall feature displaced by parallax; height precision is approximately the matching precision multiplied by H/B.](figures/out/ch14_stereo.svg){#fig:stereo width=88%}

### Pan-Sharpening

Most VHR satellites collect a high-resolution **panchromatic** band and lower-resolution (typically 4×) **multispectral** bands. The panchromatic band collects more light because it is wide, so its pixels can be smaller with the same SNR. **Pan-sharpening** combines the two to create a colour image with the panchromatic resolution (@fig:pansharpen). Methods range from simple ratio (Brovey) and intensity–hue–saturation substitution to Gram–Schmidt, wavelet and, increasingly, deep-learning fusion. Pan-sharpening is cosmetically excellent but can distort the spectral values, so scientists usually prefer the original multispectral data for quantitative analysis.

![Pan-sharpening simulated with part of a Landsat scene: coarse multispectral data (left) and a sharp panchromatic image (centre) combine into a sharp colour image (right).](figures/out/ch14_pansharpen.png){#fig:pansharpen width=98%}

### The Commercial VHR Landscape

The commercial VHR industry began in 1999, when **IKONOS** became the first commercial satellite to sell 1 m imagery. Since then, resolution has improved steadily, limited as much by regulation as by technology (@fig:evolution). In the USA, commercial imaging satellites are licensed by NOAA. The resolution permitted for sale was relaxed from 0.5 m to 0.25 m in 2014. In 2020 fixed limits were replaced by a tiered system that considers what is already available on the world market.

![Best panchromatic GSD of civil and commercial imaging satellites by launch year, and the US licensing limit for commercial sale.](figures/out/ch14_evolution.svg){#fig:evolution width=90%}

| System (operator, country) | First launch | Altitude | Pan / MS GSD | Swath | Notes |
|---|---|---|---|---|---|
| WorldView-3 (Vantor, USA) | 2014 | 617 km | 0.31 / 1.24 m | 13 km | 8 VNIR + 8 SWIR bands, CAVIS atmospheric sensor |
| WorldView Legion (Vantor, USA) | 2024 | 518 km | 0.34 / 1.36 m (0.29 m best) | 10 km | Six ≈ 630 kg satellites (two SSO, four mid-inclination); rapid revisit |
| Pléiades Neo (Airbus, France) | 2021 | 620 km | 0.30 / 1.2 m | 14 km | Two in orbit; two lost in a 2022 Vega C failure |
| Cartosat-3 (ISRO, India) | 2019 | ≈ 510 km | ≈ 0.25 / 1.1 m | 16 km | Government system; data sold commercially |
| SuperView Neo-1 (Siwei/CASC, China) | 2022 | ≈ 530 km | 0.3 / 1.2 m | 12 km | Part of a larger Chinese commercial fleet |
| Jilin-1 (Chang Guang, China) | 2015 | 500–650 km | 0.5–1 m (several types) | 10–150 km | Largest Chinese commercial constellation; video and wide-field types |
| KOMPSAT-3A (KARI, Korea) | 2015 | 528 km | 0.55 / 2.2 m | 12 km | Also a 5.5 m mid-wave infrared camera |
| SkySat (Planet, USA) | 2013 | ≈ 450 km | 0.5 m (ortho) | ≈ 6 km | Frame camera; up to 90 s video; many images per day |
| BlackSky Gen-3 (BlackSky, USA) | 2025 | ≈ 450 km | 0.35 m | ≈ 5 km | Small agile satellites; rapid tasking |
| Pelican (Planet, USA) | 2023 | ≈ 500 km | ≈ 0.5 m (Gen 1); 0.3 m class (Gen 2) | — | On-board AI processing; up to 32 planned |
| NewSat Mark IV (Satellogic, Argentina/USA) | 2020 | ≈ 470 km | ≈ 0.7 m / ≈ 25 m hyperspectral | 5 km | Low-cost microsatellites |

: Representative very-high-resolution imaging satellites in 2026 (approximate values from operators' published specifications). {#tbl:vhr}

The market is dominated by government customers. In the USA, the National Reconnaissance Office's **Electro-Optical Commercial Layer** contracts (awarded in 2022 to Maxar — now **Vantor** — BlackSky and Planet) buy commercial imagery for defence and intelligence users. Many other governments buy imagery or entire satellites. Since Russia's invasion of Ukraine in 2022, commercial imagery has been used openly by governments, news media and researchers on an unprecedented scale, demonstrating the role of commercial EO as an independent source of information.

### Very Low Earth Orbit

Because resolution improves in proportion to altitude for a given aperture, some companies are pursuing **very low Earth orbit (VLEO)** — below about 400 km. Halving the altitude from 600 to 300 km halves the GSD for the same telescope, increases the light received per pixel area, and reduces the power needed for radar or optical communications. The penalties are atmospheric drag and atomic-oxygen erosion (Chapter 2): a satellite at 250–300 km must thrust almost continuously to stay in orbit. Precedents include ESA's GOCE gravity mission (2009–2013), which flew at about 255 km using an ion engine, and JAXA's **SLATS** (Tsubame), which in 2019 set a record by imaging from 167 km. The US company **Albedo** launched its first VLEO satellite, **Clarity-1**, in March 2025 to demonstrate 10 cm visible and 2 m thermal imaging. It operated for several months, but contact was later lost and it re-entered in June 2026. Air-breathing electric propulsion, which collects the thin atmosphere itself as propellant, is being studied as a long-term enabler (Chapter 42).

## Constellations: Trading Resolution for Revisit

### The PlanetScope Revolution

In 2013 the start-up **Planet** (then Planet Labs) began launching "Doves" — 3U CubeSats with a 9 cm telescope and a frame camera — in large "Flocks". The company's insight was that many cheap satellites in sun-synchronous orbits, each with a modest 24 km swath, could image **almost the entire landmass of the Earth every day** at about 3–4 m resolution. The current **SuperDove** generation records eight bands, including coastal blue, yellow and red-edge bands designed to be interoperable with Sentinel-2. Each satellite has a lifetime of only a few years, so the fleet is constantly replenished; in October 2026 about 90 Doves were active (@fig:fleets).

![Active commercial and government optical imaging satellites by operator or series in October 2026 (name-matched in the CelesTrak SATCAT, approximate).](figures/out/ch14_fleets.svg){#fig:fleets width=88%}

Daily imaging changed the questions that could be asked. Instead of a few cloud-free images per year, analysts can follow a construction site, a crop field, a mine or a refugee camp day by day. The trade-off is radiometric and geometric consistency: hundreds of small satellites with slightly different sensors require careful cross-calibration, often against Sentinel-2 and Landsat.

### How Many Satellites for Daily Coverage?

The time to cover the whole equator with nadir-looking imagers can be estimated simply. Each satellite makes about 14.6 orbits per day, and each ascending (or descending) pass covers a strip as wide as its swath. Covering the 40 075 km equator therefore takes about

$$T \approx \frac{40\,075\ \text{km}}{14.6\times\text{swath}\times N}\ \text{days}$$

for $N$ satellites (@fig:revisit). Two Landsats with 185 km swaths need about 7–8 days, and two Sentinel-2s with 290 km swaths about 5. MODIS, with a 2 330 km swath, covers the Earth every 1–2 days with a single satellite. About 130 Doves with 24 km swaths achieve near-daily coverage. Agile VHR satellites do not cover the Earth systematically: their "revisit" is the time between opportunities to point at a given target. This is typically less than a day for a constellation of a few satellites at different local times. For the mid-inclination WorldView Legion satellites over populated latitudes, it is down to about an hour.

![Idealised days needed for full equatorial coverage versus the number of satellites, for four swath widths, compared with real systems.](figures/out/ch14_revisit.svg){#fig:revisit width=84%}

### Data Volume and Delivery

Imaging satellites produce enormous amounts of data. A push-broom VHR imager with 0.3 m pixels and a 13 km swath generates about 23 000 lines per second, each of about 43 000 pixels — about 1 gigapixel per second before multispectral bands. On-board **compression** (JPEG 2000 or the CCSDS 122 image-compression standard, typically 2:1 to 4:1 with near-lossless quality) and large solid-state recorders (terabits) buffer the data until it can be downlinked. Downlink uses **X-band** (typically 0.5–3 Gbit/s on modern satellites) or **Ka-band** links to networks of ground stations at high latitudes (Svalbard, Inuvik, Troll in Antarctica) and around the world (Chapter 7). Some operators now relay data through **optical inter-satellite links** or data-relay satellites such as the European Data Relay System (EDRS), which relays Sentinel data from LEO via GEO at 1.8 Gbit/s.

For customers, the key metric is the time from **tasking request to image delivery**. Modern operators accept orders through web portals and application programming interfaces (APIs), plan collections automatically, and deliver orthorectified images within hours — sometimes minutes — of collection. Planet's Pelican and BlackSky's Gen-3 satellites include on-board processors that can run AI models to detect objects and send alerts before the full image is downlinked (Part XIII).

## Thermal Infrared Imaging

### Why Measure Temperature from Space?

Thermal infrared (TIR) sensors measure radiation emitted by the surface, from which **land-surface temperature (LST)** and **emissivity** are derived (Chapter 13). Surface temperature is one of the most informative variables about the land. It responds immediately to water stress (plants that cannot transpire heat up), drives urban heat islands, and reveals volcanic activity, geothermal resources and industrial heat sources. It is also the key input for mapping **evapotranspiration** — the water used by crops — which is essential for water management in arid regions.

::: figrow
![Land-surface temperature over Los Angeles during an August 2020 heat wave, measured by ECOSTRESS on the International Space Station. Streets and roofs exceeded 50 °C, while parks and the coast stayed far cooler.](figures/photos/ch14_laheat.jpg){#fig:laheat}

![ECOSTRESS land-surface temperature during the Apple Fire in California, 1 August 2020. The active fire front exceeded 200 °C, and the smoke plume appears cooler than the surrounding ground.](figures/photos/ch14_applefire.jpg){#fig:applefire}
:::

### Thermal Instrument Design

Thermal imaging is harder than visible imaging for three reasons:

1. **Diffraction:** at 10 µm, the diffraction limit is about 17 times coarser than at 0.6 µm for the same aperture. So thermal pixels are larger (typically 60–100 m from LEO for science missions, 3–10 m from VHR systems with large apertures).
2. **Detectors:** sensitive photon detectors for the long-wave infrared (mercury cadmium telluride, HgCdTe; QWIPs; strained-layer superlattices) must be cooled to 40–80 K by mechanical cryocoolers. Uncooled **microbolometers**, which sense the heating of a tiny suspended membrane, are cheaper and smaller and are used by many small satellites, but are less sensitive and slower.
3. **Self-emission:** at room temperature, the telescope and instrument themselves glow in the thermal infrared. Thermal instruments therefore cool their optics or baffles, use cold stops, and calibrate frequently by viewing an on-board **blackbody** of known temperature and a cold reference (deep space).

The sensitivity of a thermal sensor is expressed as the **noise-equivalent temperature difference (NEΔT)** — 0.03–0.1 K for science instruments at 300 K.

### Retrieving Temperature and Emissivity

The radiance measured by a thermal sensor depends on both the temperature and the emissivity of the surface, and on the atmosphere's emission and absorption — mainly by water vapour. Several methods untangle these:

- **Split-window algorithms** use two adjacent bands (around 11 and 12 µm) in which water vapour absorbs differently; the brightness-temperature difference between them corrects for the atmosphere. They are widely used for sea-surface temperature, where emissivity is known.
- **Temperature–emissivity separation (TES)** was developed for ASTER and is used for ECOSTRESS. It uses five or more bands and an empirical relationship between the spectral contrast and minimum emissivity to solve for both temperature and the emissivity spectrum.
- **Emissivity spectra** in the 8–12 µm range identify minerals (@fig:emissivity): silicate rocks show strong "reststrahlen" features near 8–10 µm whose positions shift with silica content, while carbonates show features near 11.3 µm. Multispectral thermal data from ASTER, with five TIR bands, have been used extensively for geological mapping.

![Thermal-infrared emissivity spectra of common surface materials (schematic) with the ASTER thermal bands. Quartz shows strong reststrahlen features; vegetation and water are nearly black bodies.](figures/out/ch14_emissivity.svg){#fig:emissivity width=86%}

### Detecting Fires

Active fires are among the most important things to detect from space. Their detection relies on Planck's law (@fig:fire). A 1 000 K fire emits thousands of times more radiance than a 300 K background at **3.9 µm** (mid-wave infrared), but only about 30 times more at 11 µm. A fire covering just 0.01 % of a 1 km pixel (100 m²) raises the pixel's 3.9 µm brightness temperature by about 10 K but its 11 µm temperature by only 0.2 K. Fire-detection algorithms therefore look for pixels that are much hotter at 3.9 µm than at 11 µm and than their neighbours. They use the excess radiance to estimate the **fire radiative power (FRP)**, which is related to the rate at which biomass is burned.

![Brightness temperature of a pixel containing a small fire versus the fraction of the pixel burning. The 3.9 µm band is far more sensitive to small hot fires than the 11 µm band.](figures/out/ch14_fire.svg){#fig:fire width=84%}

NASA's **Fire Information for Resource Management System (FIRMS)** distributes active fire detections from MODIS (1 km) and VIIRS (375 m) within about three hours of observation worldwide. Geostationary imagers (GOES-R, Himawari, Meteosat Third Generation) detect fires every 5–10 minutes (Chapter 16). Dedicated commercial constellations are now adding faster, finer fire detection. The German company **OroraTech** had 20 thermal satellites of its FOREST series in orbit by October 2026, aiming at a global revisit of about 30 minutes. The Earth Fire Alliance's **FireSat** constellation, developed with Muon Space and Google, aims to detect fires as small as 5 m × 5 m.

| Mission | Operator | Launch | TIR resolution | TIR bands | Status (2026) |
|---|---|---|---|---|---|
| ASTER (Terra) | NASA / Japan | 1999 | 90 m | 5 | Operating; Terra nearing end of mission |
| Landsat 8 / 9 TIRS | NASA / USGS | 2013 / 2021 | 100 m | 2 | Operating |
| ECOSTRESS (ISS) | NASA JPL | 2018 | ≈ 70 m | 5 (3 used since 2019) | Operating |
| VIIRS | NOAA / NASA | 2011, 2017, 2022 | 375–750 m | 7 MWIR/LWIR | Operating (Suomi NPP, NOAA-20, NOAA-21) |
| FOREST series | OroraTech (Germany) | 2022– | ≈ 200 m | MWIR + LWIR | 20 satellites in orbit |
| HiVE (SkyBee) | constellr (Germany) | 2025– | ≈ 30 m class | 4 | First satellites in orbit |
| VanZyl | Hydrosat (USA) | 2024– | ≈ 50–70 m | Multi-band | Early constellation |
| TRISHNA | CNES / ISRO | late 2020s | 57 m | 4 | In development |
| LSTM | EU Copernicus / ESA | ≈ 2029 | ≈ 50 m | 5 | In development |
| SBG-TIR | NASA / ASI | ≈ 2029 | ≈ 60 m | 8 | In development |

: Thermal infrared imaging missions (resolution and dates approximate). {#tbl:thermal}

### Night-Time Lights

The **Day/Night Band (DNB)** of VIIRS is sensitive enough to image city lights, gas flares, fishing boats and moonlit clouds at night (@fig:nile). NASA's **Black Marble** products correct these images for moonlight, atmosphere and seasonal effects to produce daily, monthly and annual maps of night-time lights. These maps are used to estimate economic activity and population, monitor power outages after disasters and conflicts, and track light pollution.

![City lights along the Nile Valley and Delta imaged by the VIIRS Day/Night Band on 13 October 2012. About 97 % of Egypt's population lives on less than 5 % of its land, along the river, which stands out as a ribbon of light through the dark desert.](figures/photos/ch14_nile.jpg){#fig:nile width=52%}

## Imaging Spectroscopy (Hyperspectral)

### The Hypercube

A **hyperspectral imager**, or **imaging spectrometer**, records a continuous spectrum for every pixel — typically 200–300 contiguous bands 5–10 nm wide covering 0.4–2.5 µm. The result is a three-dimensional **hypercube** with two spatial dimensions and one spectral dimension (@fig:hypercube). Where a multispectral sensor can tell vegetation from soil, an imaging spectrometer can identify specific minerals (by their narrow absorption features) and estimate leaf chemistry (chlorophyll, water, nitrogen, lignin). It can also map phytoplankton types in water and detect gases such as methane and carbon dioxide by their absorption.

![A hyperspectral data cube (left) records a full spectrum for every pixel (right). Narrow absorption features — here the 2.20 µm aluminium–hydroxyl feature of clay minerals — identify materials that broad-band sensors cannot distinguish.](figures/out/ch14_hypercube.png){#fig:hypercube width=98%}

Most imaging spectrometers are push-broom instruments in which a slit selects one line on the ground. A dispersing element then spreads the light from each point along the slit into a spectrum across a two-dimensional detector. This element is a prism or a diffraction grating, often in compact **Offner** or **Dyson** designs. Each detector frame thus contains one spatial line and its full spectrum. Achieving high SNR in hundreds of narrow bands requires large apertures and long dwell times, which is why space hyperspectral systems usually have 30–60 m pixels and narrow swaths (30–80 km). Calibration is demanding: errors of a fraction of a nanometre in the spectral position of bands ("smile" and "keystone" distortions) can corrupt the retrieval of narrow absorption features.

### Missions

NASA's **Hyperion** on EO-1 (2000–2017) was the first civil spaceborne imaging spectrometer, with 220 bands at 30 m. Today, several missions are operating and more are coming (@tbl:hyper).

| Mission | Operator | Launch | GSD | Spectral range / bands | Notes |
|---|---|---|---|---|---|
| PRISMA | ASI (Italy) | 2019 | 30 m (5 m pan) | 0.4–2.5 µm, ≈ 240 | Second generation in development |
| DESIS (ISS) | DLR / Teledyne | 2018 | 30 m | 0.4–1.0 µm, 235 | Commercial access |
| HISUI (ISS) | Japan METI | 2019 | 20 × 31 m | 0.4–2.5 µm, 185 | |
| EnMAP | DLR (Germany) | 2022 | 30 m | 0.42–2.45 µm, > 220 | Science mission, open data |
| EMIT (ISS) | NASA JPL | 2022 | 60 m | 0.38–2.5 µm, 285 | Mineral dust sources; methane plumes |
| Tanager-1 / -2 | Carbon Mapper / Planet / JPL | 2024 / 2026 | ≈ 30 m | 0.4–2.5 µm | Methane and CO₂ point sources |
| Firefly | Pixxel (India) | 2025 | ≈ 5 m | VNIR, > 150 | Commercial constellation |
| CHIME | EU Copernicus / ESA | ≈ 2029 | 30 m | 0.4–2.5 µm | Copernicus Expansion mission |
| SBG-VSWIR | NASA | 2030s | ≈ 30 m | 0.4–2.5 µm | Recommended by the 2017 Decadal Survey |

: Spaceborne imaging spectrometers (approximate characteristics). {#tbl:hyper}

### Seeing Methane

One of the most consequential new uses of imaging spectroscopy is mapping **methane plumes** from individual facilities — leaking oil and gas wells, pipelines, coal mines and landfills. Methane absorbs sunlight in narrow bands near 1.65 and 2.3 µm; a plume of excess methane slightly deepens these absorptions in the pixels it covers, and matched-filter algorithms detect this signature (@fig:methane). Because methane is a powerful greenhouse gas with a short atmospheric lifetime (about a decade), finding and fixing large leaks — "super-emitters" — is one of the fastest ways to slow global warming. EMIT detected hundreds of methane plumes in its first years; Carbon Mapper's Tanager satellites and the commercial **GHGSat** constellation, which uses Fabry–Pérot interferometers with about 25 m resolution, specialise in this task. Chapter 16 describes broader mapping of methane and carbon dioxide over regions and the globe. This is done by spectrometers such as TROPOMI on Sentinel-5P, NASA's OCO-2/3, Japan's GOSAT series (including GOSAT-GW, launched in June 2025) and Europe's future CO2M mission. The Environmental Defense Fund's MethaneSAT, launched in 2024 to quantify emissions from whole oil and gas basins, was lost in June 2025 after about a year in orbit.

![A cluster of 12 methane plumes detected by NASA's EMIT imaging spectrometer over a 400 km² oil and gas field in southern Uzbekistan on 1 September 2022. Each purple plume marks a source releasing methane at a high rate.](figures/photos/ch14_methane.jpg){#fig:methane width=90%}

## Global Imagers: MODIS, VIIRS and Their Successors

The **Moderate Resolution Imaging Spectroradiometer (MODIS)**, on NASA's Terra (1999) and Aqua (2002) satellites, has been one of the most productive scientific instruments ever flown. It has 36 spectral bands from 0.41 to 14.4 µm, at 250 m (two bands), 500 m (five bands) and 1 km. Its 2 330 km swath covers the whole Earth every one to two days. Its standard products — surface reflectance, vegetation indices, land cover, snow and ice, fires, aerosols, clouds, ocean colour and sea-surface temperature — have been used in tens of thousands of scientific papers. Terra and Aqua are well beyond their design lives and have run out of the fuel needed to maintain their overpass times, so their observations are drifting and will end in the next few years.

The **Visible Infrared Imaging Radiometer Suite (VIIRS)** continues the MODIS record operationally on the NOAA–NASA Suomi NPP (2011), NOAA-20 (2017) and NOAA-21 (2022) satellites. It has 22 bands at 375 m and 750 m, and a 3 040 km swath that leaves no gaps between orbits even at the equator. In Europe, **Sentinel-3**'s OLCI (ocean and land colour) and SLSTR (sea and land surface temperature) instruments provide similar global observations with an emphasis on climate-quality accuracy. These sensors are described further in Chapter 16.

![The Hyperion imaging spectrometer on NASA's EO-1 satellite views Iceland's Eyjafjallajökull volcano on 2 May 2010. Visible bands (left) show only ash plume and snow; combinations using short-wave infrared bands (centre and right) reveal the hot lava flow extending north from the vent.](figures/photos/ch14_eyja.jpg){#fig:eyja width=90%}

## Design Example: A Small VHR Imaging Satellite

::: example
**Example: sizing a 0.5 m small-satellite imager**

*Requirement:* 0.5 m panchromatic GSD from a 500 km orbit, 6 km swath.

1. **Focal length.** With a CMOS TDI detector of 5.5 µm pixels: $f = p\,h/\text{GSD} = 5.5\times10^{-6}\times 500\,000/0.5 = 5.5$ m.
2. **Aperture.** The Rayleigh limit at 0.6 µm for 0.5 m is $D = 1.22\lambda h/r = 0.73$ m. Choosing a 0.5 m aperture (f/11) gives an optical sampling ratio $Q = \lambda f/(D\,p) = 1.2$ — slightly under-sampled relative to the optics, a common compromise that keeps the telescope compact. The system MTF at Nyquist will be about 0.1.
3. **Swath and detector.** 6 km / 0.5 m = 12 000 pixels across the swath, for example three staggered 4 096-pixel TDI arrays.
4. **Line rate.** Ground speed at 500 km ≈ 7.06 km/s, so the line rate is 7 060 / 0.5 ≈ 14 100 lines per second.
5. **Signal.** Using the method of @fig:photons, a 0.5 m aperture with 0.5 m pixels collects roughly 1 000 photo-electrons per line time in the panchromatic band. With 16–32 TDI stages, this rises to 16 000–32 000 electrons and a shot-noise SNR above 100 for bright targets.
6. **Data rate.** 12 000 pixels × 14 100 lines/s × 12 bits ≈ 2.0 Gbit/s for the panchromatic band, plus about 25 % for four multispectral bands at 2 m. With 3:1 compression this is about 0.85 Gbit/s; a 10-second, 70 km long image produces about 1 GB.
7. **Downlink.** An X-band link at 800 Mbit/s over a 6-minute ground-station pass can return about 36 GB per pass — some 36 such images.
8. **Agility.** To collect 20 targets per pass, the satellite must slew roughly 1–2° per second and settle within a few seconds — requiring CMGs or high-torque reaction wheels and a rigid structure with good jitter isolation.

The result is a satellite of roughly 150–250 kg — similar to commercial systems such as BlackSky Gen-3 or Planet's Pelicans.
:::

::: ai
**AI on EO/IR satellites**

Optical imaging is where AI in space is most mature. On-board neural networks screen out cloudy images before downlink (ESA's Φ-sat-1 first demonstrated this in 2020), detect ships, aircraft and vehicles, and generate alerts within minutes of collection. On the ground, deep learning performs super-resolution, pan-sharpening, cloud removal and automatic change detection over entire countries. Chapters 45 and 46 discuss these applications in detail.
:::

::: key
**Key takeaways**

- EO/IR satellites range from global imagers (≈ 1 km) through medium-resolution workhorses (10–30 m) to very-high-resolution systems (≈ 0.3 m).
- Landsat (since 1972) and Sentinel-2 (since 2015) provide free, well-calibrated imagery of the whole land surface every few days and are combined in harmonised products.
- Resolution is limited by diffraction ($r \approx 1.22\lambda h/D$) and by the number of photons per pixel; VHR systems need large apertures, long focal lengths and time-delay integration.
- Agile satellites point off nadir to collect many targets, area mosaics and stereo pairs, at the cost of coarser GSD at large angles.
- Constellations of small satellites trade resolution for revisit: about 90 Doves image the land surface almost daily at 3–4 m.
- Thermal infrared sensors measure surface temperature and emissivity, essential for water use, urban heat, geology and fire detection; fire detection exploits the extreme sensitivity of the 3.9 µm band to small hot sources.
- Imaging spectrometers record hundreds of narrow bands, identifying minerals, plant chemistry and methane plumes from individual facilities.
- MODIS is ending after more than two decades; VIIRS and Sentinel-3 continue the global record.
:::

::: questions
**Review questions**

1. Calculate the diffraction-limited ground resolution of a telescope with a 1.1 m aperture at 0.55 µm from 500 km altitude.
2. What is time-delay integration, and why do very-high-resolution imagers need it?
3. Why does ground sample distance degrade when an agile satellite images far off nadir?
4. How are stereo pairs collected, and what products are made from them?
5. Explain the trade between resolution and revisit using the PlanetScope constellation as an example.
6. Why is the 3.9 µm band so sensitive to small fires? Use Planck's law in your answer.
7. What is an imaging spectrometer's "hypercube", and how can imaging spectroscopy detect methane from individual facilities?
8. Why are Landsat and Sentinel-2 data often combined, and what must be done to harmonise them?
:::
