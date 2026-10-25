---
title: Weather and Environmental Satellites
hero: ch16
abstract: Every weather forecast you see depends on satellites. Geostationary satellites watch storms develop minute by minute over a third of the planet, while polar-orbiting satellites carry sounders that measure the temperature and humidity of the atmosphere layer by layer across the whole globe twice a day. Their observations are fed into numerical weather prediction models that now forecast as well five days ahead as they did three days ahead in the 1980s. This chapter explains the global satellite observing system, the instruments that make it work and the physics of atmospheric sounding, and then turns to environmental and climate monitoring — atmospheric composition and air quality, clouds, precipitation and radiation, oceans, sea level, sea ice and ice sheets — illustrated with real satellite records. It ends with the arrival of AI weather models.
---

## Satellites and the Weather

On 1 April 1960, NASA's **TIROS-1** returned the first television picture of the Earth's clouds from orbit. Forecasters immediately saw storms and weather systems that had been invisible to the scattered network of ground stations, especially over the oceans. Within a few years, the **Nimbus** research satellites (from 1964) had demonstrated the first instruments to measure atmospheric temperature profiles from space. **ATS-1** (1966) then returned the first images of the full Earth disc from geostationary orbit. Operational geostationary satellites followed — the US **SMS/GOES** series (1974–75), Europe's **Meteosat** and Japan's **GMS** (both 1977) — and polar-orbiting satellites became the backbone of global forecasting.

Today, meteorological satellites are coordinated internationally through the World Meteorological Organization (WMO) and the **Coordination Group for Meteorological Satellites (CGMS)**. Their data are exchanged freely between nations under WMO resolutions — one of the most successful examples of international cooperation in space. More than 90 % of the observations assimilated into modern global weather forecasts come from satellites, and they account for most of the improvement in forecast skill over the past four decades.

### The Space-Based Global Observing System

The WMO's baseline architecture combines two orbital regimes (Chapter 11):

- **Geostationary (GEO) satellites** at 35 786 km provide continuous observation of about a third of the Earth from a fixed position over the equator. A ring of five or six satellites covers the globe between about 60° N and 60° S (@fig:georing). They are ideal for watching rapidly developing weather — thunderstorms, hurricanes, fog, fires, volcanic ash — and for deriving winds by tracking cloud and water-vapour features between successive images (**atmospheric motion vectors**). Their weakness is poor coverage of polar regions and the coarse resolution imposed by their great distance.
- **Low-Earth-orbit (LEO) polar satellites** in sun-synchronous orbits at 800–850 km cover the entire globe twice a day from close range, carrying the **sounders** that are the most important data source for numerical weather prediction. The WMO baseline calls for three orbital planes — early morning, mid-morning and afternoon — so that every place on Earth is observed at least every four hours (@fig:orbitslt). Europe (Metop) provides the mid-morning orbit, the USA (JPSS) the afternoon orbit, and China (FY-3E) has filled the previously empty early-morning orbit since 2021.

![Primary meteorological geostationary satellites in 2026. Shading shows how many satellites view each point at a usable angle; overlap provides backup and stereo views of clouds.](figures/out/ch16_georing.svg){#fig:georing width=100%}

![The three sun-synchronous orbit planes of the WMO polar-orbiting baseline, viewed from above the North Pole. Each plane keeps a fixed orientation relative to the Sun, so a satellite always crosses the equator at the same local solar times.](figures/out/ch16_orbitslt.svg){#fig:orbitslt width=80%}

These are complemented by a growing number of other missions: **GNSS radio-occultation** constellations, **scatterometers** and **microwave imagers**, research missions with radars and lidars, and, increasingly, commercial providers selling weather data to governments.

## Geostationary Weather Satellites

### The Current Generation

Since 2015 every geostationary weather operator has introduced a new generation of satellites with dramatically improved imagers (@tbl:geosats). The common design is represented by the US **Advanced Baseline Imager (ABI)**, Japan's **Advanced Himawari Imager (AHI)** and Europe's **Flexible Combined Imager (FCI)**. It scans the full disc in about 10 minutes in 16 spectral channels, with 0.5–1 km resolution in visible channels and 2 km in the infrared. At the same time it scans smaller regions every few minutes or even every 30 seconds (@fig:abiscan).

| Operator | Series (current satellites) | Positions | Imager | Other instruments |
|---|---|---|---|---|
| USA (NOAA/NASA) | GOES-R: GOES-18 (West), GOES-19 (East) | 137° W, 75° W | ABI, 16 channels | GLM lightning mapper; space weather sensors; CCOR-1 coronagraph on GOES-19 |
| Europe (EUMETSAT/ESA) | Meteosat Third Generation: MTG-I1 (Meteosat-12), MTG-I2, MTG-S1; plus MSG | 0°, 9.5° E, 45.5° E | FCI, 16 channels | LI lightning imager; IRS hyperspectral sounder and Sentinel-4 UVN on MTG-S1 |
| Japan (JMA) | Himawari-9 (Himawari-8 backup) | 140.7° E | AHI, 16 channels | Himawari-10 (≈ 2029) to add a hyperspectral sounder |
| China (CMA) | Fengyun-4A, 4B | ≈ 86.5° E, 105° E | AGRI | GIIRS hyperspectral sounder; LMI lightning imager |
| South Korea (KMA) | GEO-KOMPSAT-2A | 128.2° E | AMI, 16 channels | Space weather; GEMS air quality on GK-2B |
| India (IMD/ISRO) | INSAT-3D, 3DR, 3DS | 74°–82° E | 6-channel imager | 19-channel infrared sounder |
| Russia (Roshydromet) | Elektro-L N2–N4 | 76° E, 165.8° E, etc. | MSU-GS | — |

: Operational geostationary meteorological satellites in 2026 (selected). {#tbl:geosats}

![Interleaved scanning of the GOES Advanced Baseline Imager in its standard mode: the full disc every 10 minutes, the continental USA every 5 minutes, and two 1 000 km mesoscale boxes every minute.](figures/out/ch16_abiscan.svg){#fig:abiscan width=94%}

The GOES-R series illustrates the state of the art. Each satellite weighs about 5 200 kg at launch and carries the ABI, the **Geostationary Lightning Mapper (GLM)**, solar and space-environment instruments and a data-relay payload. ABI's 16 channels include two visible, four near-infrared and ten infrared bands; three water-vapour channels at 6.2, 6.9 and 7.3 µm map moisture at different heights, and the 3.9 µm channel detects fires and fog. GOES-16 was launched in 2016, GOES-17 in 2018, GOES-18 in 2022 and GOES-19 in June 2024. The ABI on GOES-17 suffered a cooling-system problem that degraded some infrared channels for several hours per night, and GOES-17 was replaced by GOES-18 in 2023. GOES-19 became the operational GOES-East satellite in April 2025. The follow-on **GeoXO** programme plans its first launch in 2032, adding a hyperspectral infrared sounder and an atmospheric-composition instrument.

![GOES-U (now GOES-19) on its Falcon Heavy rocket before launch in June 2024. The satellite became the operational GOES-East in April 2025.](figures/photos/ch16_goesu.jpg){#fig:goesu width=72%}

### Lightning from Orbit

Lightning mappers fly on the newest geostationary satellites: GLM on GOES, the **Lightning Imager (LI)** on MTG and the **Lightning Mapping Imager (LMI)** on Fengyun-4. They detect the brief optical flashes of lightning at the oxygen emission line of 777.4 nm, day and night. They use staring detector arrays that take about 500 frames per second, and on-board processing that subtracts the bright background of sunlit clouds. Rapid increases in total lightning ("lightning jumps") often precede severe weather such as hail and tornadoes, and lightning data help pilots and air-traffic controllers avoid storms over the oceans, where radar coverage is absent.

### Geostationary Sounding

In 2016 China's **Fengyun-4A** carried the first hyperspectral infrared sounder in geostationary orbit (GIIRS). In July 2025 Europe launched **MTG-S1** with the **Infrared Sounder (IRS)**, which measures about 1 700 spectral channels over Europe every 30 minutes. Geostationary sounders track the evolution of temperature and humidity in the hours before storms form — precisely the information needed for forecasting severe convection. MTG-S1 also carries the Copernicus **Sentinel-4** ultraviolet–visible–near-infrared spectrometer for hourly air-quality monitoring over Europe.

## Polar-Orbiting Weather Satellites

### The Main Systems

| System | Operator | Equator crossing | Satellites (2026) | Key instruments |
|---|---|---|---|---|
| JPSS | NOAA / NASA (USA) | 13:30 (afternoon) | Suomi NPP (2011), NOAA-20 (2017), NOAA-21 (2022); JPSS-4 from 2027 | VIIRS, CrIS, ATMS, OMPS, CERES |
| EPS / EPS-SG | EUMETSAT / ESA (Europe) | 09:30 (mid-morning) | Metop-B (2012), Metop-C (2018), Metop-SG A1 (2025); Metop-SG B1 (late 2026) | IASI and IASI-NG, AMSU-A/MHS and MWS, ASCAT and SCA, METimage, radio occultation, Sentinel-5 |
| Fengyun-3 | CMA (China) | early morning, morning, afternoon | FY-3C to FY-3G (FY-3E in the 05:30 orbit, FY-3G for precipitation radar) | MERSI, HIRAS, MWTS, MWHS, GNOS |
| Meteor-M | Roshydromet (Russia) | morning | Meteor-M N2-2 to N2-4 | MSU-MR, IKFS-2, MTVZA |
| DMSP | US Space Force | various | Last satellites near end of life | SSMIS microwave imager/sounder |

: Operational polar-orbiting meteorological satellites (selected). {#tbl:leosats}

The European **Metop Second Generation (EPS-SG)** programme illustrates the trend to specialisation. Instead of one large satellite, it uses two series flying together. **Metop-SG A** (sounding and imaging) carries METimage, IASI-NG, MWS, the 3MI multi-viewing polarimeter, radio occultation and the Copernicus Sentinel-5 atmospheric-composition spectrometer. **Metop-SG B** (microwave imaging and scatterometry) carries SCA, MWI, the ICI ice-cloud imager, radio occultation and Argos. The first A satellite was launched on 13 August 2025 on an Ariane 6.

### Sounders: Measuring the Atmosphere Layer by Layer

The most valuable instruments for weather forecasting are **sounders**, which measure the vertical profiles of temperature and humidity. They exploit a simple idea (@fig:weighting). In a spectral band where an atmospheric gas of known concentration absorbs strongly, the radiation that reaches space comes only from high in the atmosphere, because radiation from below is absorbed. Where it absorbs weakly, radiation from lower down escapes. A sounder measures many channels from the centre to the edge of an absorption band, such as the 15 µm band of CO₂ or the 50–60 GHz band of oxygen. The concentrations of these gases are well known. In this way the sounder samples the temperature at a range of heights. Each channel's sensitivity to different heights is described by its **weighting function**. Channels in water-vapour bands (6.3 µm and 183 GHz) similarly sample humidity.

![Idealised weighting functions of six sounding channels. Each channel senses a layer of the atmosphere a few kilometres thick; together they provide a temperature profile.](figures/out/ch16_weighting.svg){#fig:weighting width=78%}

**Infrared sounders** offer fine vertical resolution. The hyperspectral sounders now flying are NASA's **AIRS** (2002, 2 378 channels), Europe's **IASI** (2006, 8 461 channels), the US **CrIS** (2011, 2 211 channels) and China's HIRAS. They measure the infrared spectrum in thousands of narrow channels and provide temperature profiles with about 1 K accuracy in 1 km layers. **IASI-NG** on Metop-SG doubles IASI's spectral resolution and halves its noise. Infrared sounders cannot see through clouds, however.

**Microwave sounders** (AMSU-A, MHS, ATMS, MWHS, and the new MWS) have coarser resolution but see through all but the thickest precipitating clouds. So they observe the atmosphere in exactly the stormy regions that matter most for forecasts. @fig:mwspectrum shows the absorption lines they use. Microwave sounders have consistently been found to have the largest single impact on global forecast skill.

![Schematic transmittance of the atmosphere at microwave frequencies. Sounders use the oxygen bands near 60 and 118 GHz for temperature and the water-vapour line at 183 GHz for humidity; window channels see the surface and precipitation.](figures/out/ch16_mwspectrum.svg){#fig:mwspectrum width=94%}

**Microwave imagers** (SSMIS, AMSR2, GMI, MWI) measure emission from the surface and the atmosphere at window frequencies, from which they derive precipitation, total water vapour, cloud liquid water, sea-surface wind speed, sea ice and snow. The SSMIS instruments on the ageing US military DMSP satellites provided about half of the world's microwave imagery. The planned end of these satellites — and NOAA's decision in 2025 to stop processing their data publicly — raised concerns among hurricane forecasters about gaps in observations of storm structure. This also increased the importance of newer instruments and commercial microwave small satellites.

### GNSS Radio Occultation

A remarkably powerful technique uses signals from navigation satellites (@fig:radioocc). As a GPS, Galileo, GLONASS or BeiDou satellite sets or rises behind the Earth's limb as seen from a LEO satellite, its signals pass through the atmosphere and are bent by refraction. A receiver on the LEO satellite measures the extra delay with millimetre precision. From this, the **bending angle** — and hence the refractivity, temperature, pressure and humidity of the atmosphere — can be computed as a function of height. **Radio occultation (RO)** measurements are self-calibrating (based on time measurements traceable to atomic clocks), unaffected by clouds and highly precise in the upper troposphere and stratosphere. They are used to "anchor" the bias corrections of other satellite instruments.

![GNSS radio occultation. A signal from a navigation satellite is bent as it passes through the atmosphere on its way to a receiver in low Earth orbit.](figures/out/ch16_radioocc.svg){#fig:radioocc width=94%}

The US–Taiwan **COSMIC-2** constellation (2019) provides about 5 000 tropical occultations per day, and Metop carries the GRAS receiver. Since about 2020, commercial companies such as **Spire** and **PlanetiQ** have sold radio-occultation data from constellations of small satellites to NOAA, EUMETSAT and other agencies — one of the first successful commercial weather-data markets. Spire also measures reflected GNSS signals (GNSS-R) for ocean winds and soil moisture.

### Winds

Wind is the hardest weather variable to observe from space. Most wind information comes from **atmospheric motion vectors**, found by tracking clouds and water-vapour features in successive geostationary images. It also comes from **scatterometers** such as ASCAT on Metop. These measure ocean-surface wind speed and direction from the radar backscatter of wind-driven ripples observed from several directions. ESA's **Aeolus** (2018–2023) was the first satellite to carry a Doppler wind lidar, measuring wind profiles directly by the Doppler shift of laser light backscattered by molecules and aerosols. Despite technical difficulties with the laser, Aeolus clearly improved forecasts, particularly in the tropics, and an operational follow-on (EPS-Aeolus) is planned for the 2030s.

## From Observations to Forecasts

### Numerical Weather Prediction and Data Assimilation

A weather forecast is produced by a **numerical weather prediction (NWP)** model that solves the equations of fluid dynamics and thermodynamics for the atmosphere on a three-dimensional grid. For the global model of the European Centre for Medium-Range Weather Forecasts (ECMWF), this grid is today about 9 km horizontally and 137 levels vertically. Because the atmosphere is chaotic, a forecast can only be as good as its **initial conditions** — the best estimate of the current state of the whole atmosphere, called the **analysis**.

Producing the analysis is the job of **data assimilation** (@fig:nwpflow). Every 6 or 12 hours, tens of millions of observations — over 90 % of them from satellites — are compared with a short-range forecast (the "first guess"). Modern systems assimilate satellite **radiances** directly, rather than retrieved temperatures. A fast **radiative-transfer model** (such as RTTOV or CRTM) computes what each instrument channel would measure given the model atmosphere. An optimisation algorithm (**4D-Var**, ensemble Kalman filters or hybrids) then adjusts the model state to fit all the observations over a time window as well as possible, weighted by their expected errors. Instrument biases are corrected continuously within the system, using unbiased "anchor" observations such as radiosondes and GNSS radio occultation.

![The data-assimilation and forecasting cycle used by operational weather centres.](figures/out/ch16_nwpflow.svg){#fig:nwpflow width=96%}

The result has been called a "quiet revolution": forecast skill has improved by about one day per decade, so that a five-day forecast today is as accurate as a three-day forecast in the 1980s (@fig:skill). One of the clearest signs of the satellites' contribution is the closing of the gap between the Northern and Southern Hemispheres around 2000. The Southern Hemisphere has few ground observations; once satellite radiances were assimilated directly, its forecasts became nearly as good as those of the well-observed north.

![Schematic evolution of medium-range forecast skill. Skill has risen steadily, and the Southern Hemisphere caught up with the Northern Hemisphere as satellite data assimilation matured.](figures/out/ch16_skill.svg){#fig:skill width=86%}

Studies measure each observing system's contribution, either by denying data in experiments or by adjoint-based "forecast sensitivity to observation impact" methods. They consistently find that microwave sounders, hyperspectral infrared sounders, GNSS radio occultation and atmospheric motion vectors are among the most valuable observations, together with conventional radiosondes and aircraft reports.

### AI Weather Models

Machine-learning models can be trained on decades of ECMWF's **ERA5 reanalysis** — itself a product of assimilating satellite data. Since 2022, such models have matched or beaten physics-based models on many forecast scores, while running thousands of times faster. Notable models include NVIDIA's FourCastNet (2022), Huawei's Pangu-Weather and Google DeepMind's GraphCast (2023) and GenCast (2024). In February 2025 ECMWF made its own **Artificial Intelligence Forecasting System (AIFS)** operational. It was the first data-driven global model in an operational service at a major international centre, and was followed by an AI ensemble (AIFS ENS) in July 2025. These models still depend on conventional data assimilation for their initial conditions, and therefore on satellite observations; research models that learn to forecast directly from raw observations are under development. Part XIII discusses these advances in detail.

## Atmospheric Composition and Air Quality

### Ozone

Satellites played a central role in one of the great environmental success stories. The ozone layer, at 15–35 km, absorbs harmful solar ultraviolet radiation. After British Antarctic Survey scientists reported the **Antarctic ozone hole** in 1985 from ground measurements, NASA's Total Ozone Mapping Spectrometer (TOMS) on Nimbus-7 revealed its full extent. The **Montreal Protocol** (1987) and its amendments phased out the chlorofluorocarbons responsible, and satellites have monitored the result ever since (@fig:ozone). The ozone hole still forms every southern spring but has begun to shrink; full recovery is expected around 2066 over the Antarctic.

![Size of the Antarctic ozone hole and minimum total ozone, 1979–2025, from satellite measurements.](figures/out/ch16_ozone.svg){#fig:ozone width=88%}

![The Antarctic ozone hole on 1 October 2010 seen by the Ozone Monitoring Instrument on NASA's Aura satellite. Blue and purple show the lowest ozone.](figures/photos/ch16_ozone.jpg){#fig:ozonemap width=40%}

Ozone and other trace gases are measured by **ultraviolet–visible spectrometers** that observe sunlight scattered by the atmosphere and identify gases by their absorption features. Examples are TOMS (1978–2005), the Dutch–Finnish **OMI** on Aura (2004), **OMPS** on Suomi NPP and NOAA-20/21, and GOME-2 on Metop. Since 2017, **TROPOMI** on the Copernicus **Sentinel-5 Precursor** has mapped nitrogen dioxide, ozone, sulphur dioxide, formaldehyde, carbon monoxide and methane daily, with pixels of 5.5 × 3.5 km.

### Air Quality from Geostationary Orbit

Air pollution changes hour by hour with traffic, industry and weather. A **geostationary air-quality constellation** now observes the world's three most populated northern regions every daylight hour (@fig:aqgeo). Korea's **GEMS** on GEO-KOMPSAT-2B (2020) covers Asia, and NASA's **TEMPO** (2023, hosted on a commercial communications satellite) covers North America. Copernicus **Sentinel-4** on MTG-S1 (2025) covers Europe and North Africa. These instruments map pollutants such as nitrogen dioxide at neighbourhood scales and show their daily cycles — rush-hour peaks, ship tracks, wildfire smoke — for the first time.

![Fields of regard of the geostationary air-quality constellation.](figures/out/ch16_aqgeo.svg){#fig:aqgeo width=96%}

### Greenhouse Gases

Measuring carbon dioxide from space is extremely demanding. Adding all of humanity's emissions for a year changes the atmospheric concentration by only about 0.5 %. A large power plant raises it locally by a fraction of a percent. Dedicated missions use high-resolution spectrometers in the near-infrared and short-wave infrared absorption bands of CO₂ (1.6 and 2.06 µm) and of oxygen (0.76 µm, to measure the total air column). They aim for a precision of better than 0.25 %. Missions include Japan's **GOSAT** (2009), **GOSAT-2** (2018) and **GOSAT-GW** (2025), NASA's **OCO-2** (2014) and **OCO-3** on the ISS (2019), China's TanSat (2016) and the French **MicroCarb** (2025). Europe's **CO2M** constellation, the first Copernicus Expansion mission, is designed to monitor anthropogenic CO₂ emissions at the scale of countries and large cities for verification of the Paris Agreement. Methane — whose super-emitters are mapped by imaging spectrometers (Chapter 14) — is measured globally by TROPOMI and GOSAT.

## Clouds, Aerosols, Precipitation and the Energy Budget

### Profiling Radars and Lidars

Passive sensors see mostly the tops of clouds. Active instruments reveal their vertical structure. From 2006 until 2023, NASA's **CloudSat** (94 GHz cloud radar) and the NASA–CNES **CALIPSO** (lidar) flew in the "A-Train" formation with Aqua and Aura, revolutionising understanding of clouds and aerosols. Their successor, the ESA–JAXA **EarthCARE** (launched May 2024), combines an atmospheric lidar (ATLID), the first **Doppler cloud-profiling radar** in space (provided by Japan), a multispectral imager and a broadband radiometer. Its aim is to understand how clouds and aerosols affect the Earth's energy balance — the largest uncertainty in climate projections.

### Precipitation

The US–Japan **Tropical Rainfall Measuring Mission (TRMM, 1997–2015)** carried the first precipitation radar in space. Its successor, the **Global Precipitation Measurement (GPM)** Core Observatory (2014, @fig:gpm), carries a dual-frequency precipitation radar (Ku- and Ka-band) and a 13-channel microwave imager. GPM serves as a calibration reference for a constellation of about ten microwave imagers and sounders from several nations. Together with geostationary infrared data, they feed the **IMERG** product, which maps rainfall worldwide every 30 minutes on a 0.1° grid. Small satellites are joining: NASA's **TROPICS** CubeSats (2023) observe tropical cyclones with microwave sounders roughly every hour.

![The GPM Core Observatory during testing at NASA Goddard. Its dual-frequency precipitation radar and microwave imager calibrate a whole constellation of precipitation-sensing satellites.](figures/photos/ch16_gpm.jpg){#fig:gpm width=46%}

### The Earth's Energy Budget

The climate is governed by the balance between absorbed sunlight and emitted thermal radiation. The **CERES** instruments, flying since 1997 on TRMM, Terra, Aqua, Suomi NPP and NOAA-20, measure reflected solar and emitted longwave radiation. Combined with ocean heat-content measurements, they show that the Earth's **energy imbalance** roughly doubled between 2005 and 2019, to about 1 W/m² — energy that is warming the oceans. Total solar irradiance has been measured from space since 1978, most recently by NASA's TSIS-1 on the ISS, showing that changes in the Sun are far too small to explain recent warming. Future missions such as the UK–ESA TRUTHS aim to set SI-traceable climate benchmarks (Chapter 13).

## Oceans

### Sea-Surface Temperature and Ocean Colour

Sea-surface temperature (SST) has been measured from space since the 1970s with infrared radiometers (AVHRR, and today VIIRS and Sentinel-3's dual-view SLSTR). SLSTR uses two viewing angles to correct for the atmosphere. Microwave radiometers (AMSR2) are also used, and these see through clouds. SST drives the weather and climate — it fuels hurricanes, defines El Niño, and is a key input to forecasts.

**Ocean colour** sensors measure the subtle colour of the sea to derive chlorophyll concentration, sediments and harmful algal blooms. Chlorophyll concentration shows the abundance of phytoplankton, which produce about half of the world's oxygen and form the base of the marine food web. After SeaWiFS (1997–2010), MODIS and Sentinel-3's OLCI, NASA's **PACE** mission (launched February 2024, @fig:pace) carries the first hyperspectral ocean-colour instrument (OCI). OCI measures the full spectrum from ultraviolet to near-infrared in 5 nm steps, so that different types of phytoplankton can be distinguished. PACE also carries two polarimeters for aerosols and clouds.

![NASA's PACE spacecraft being prepared for launch in December 2023. Its Ocean Color Instrument measures more than 200 wavelengths.](figures/photos/ch16_pace.jpg){#fig:pace width=66%}

### Satellite Altimetry and Sea Level

A radar **altimeter** measures the height of the sea surface by timing radar pulses reflected vertically from the ocean (@fig:altimetry). The satellite's orbit must be known with centimetre accuracy, which is achieved with GNSS receivers, the French DORIS system and laser ranging. Corrections are also applied for the ionosphere, water vapour, sea state and tides. The sea-surface height can then be measured to about 2–3 cm along each ground track. Ocean currents, eddies and El Niño show up as bumps and dips of tens of centimetres in the sea surface.

![Principle of satellite radar altimetry. Sea-surface height is the orbit height minus the measured range, corrected for atmospheric and sea-state effects.](figures/out/ch16_altimetry.svg){#fig:altimetry width=88%}

Since the US–French **TOPEX/Poseidon** mission (1992), a series of reference altimetry missions has measured global mean sea level with continuous, cross-calibrated precision (@fig:sealevel). These are Jason-1 (2001), Jason-2 (2008), Jason-3 (2016), **Sentinel-6 Michael Freilich** (2020) and **Sentinel-6B** (launched November 2025). The record shows a rise of about 10 cm since 1993, at a rate that has roughly doubled, driven by ocean warming (thermal expansion) and by melting glaciers and ice sheets.

![Global mean sea level from the reference altimetry missions, 1993–2025, with a quadratic fit showing acceleration.](figures/out/ch16_sealevel.svg){#fig:sealevel width=88%}

The NASA–CNES **SWOT** mission (2022) introduced a new technique: a Ka-band radar interferometer (KaRIn) with two antennas on a 10 m boom. It measures water-surface height across two 50 km swaths rather than along a single line. SWOT resolves ocean eddies ten times smaller than before and measures the height and slope of rivers and lakes worldwide — the first global survey of fresh water from space (@fig:swot).

![SWOT's first-light sea-surface height measurements off the US East Coast (2023), showing fine-scale ocean features within the wide swath compared with conventional altimetry.](figures/photos/ch16_swot.jpg){#fig:swot width=50%}

## The Cryosphere and Land

### Sea Ice and Ice Sheets

Passive microwave radiometers have mapped polar sea ice every day since 1978, regardless of clouds and polar darkness, because ice and open water emit microwaves very differently. The record shows a dramatic decline in Arctic sea ice, especially at the end of summer (@fig:seaice): the September minimum extent has fallen by about 12 % per decade, with a record low in 2012. Antarctic sea ice changed little until 2016, then fell sharply, with record lows in 2023.

![Minimum sea-ice extent in the Arctic (September) and Antarctic (February) from the passive-microwave record, 1979–2026.](figures/out/ch16_seaice.svg){#fig:seaice width=88%}

Radar altimeters (ESA's **CryoSat-2**, 2010) and laser altimeters (NASA's **ICESat-2**, 2018) measure the thickness of sea ice and the changing height of ice sheets and glaciers. The US–German **GRACE** (2002–2017) and **GRACE Follow-On** (2018) missions measure tiny changes in the Earth's gravity field to "weigh" ice sheets and groundwater. They do this by tracking the distance between two satellites 220 km apart to within a fraction of a micrometre, with microwave and laser ranging. They show Greenland losing about 270 billion tonnes of ice per year and Antarctica about 150 billion tonnes, and reveal groundwater depletion in regions such as northern India and California's Central Valley.

### Soil Moisture and Land

ESA's **SMOS** (2009) and NASA's **SMAP** (2015) measure soil moisture and ocean salinity with L-band (1.4 GHz) radiometers, exploiting a protected frequency band where the emission of the surface depends strongly on its water content. SMOS uses a Y-shaped interferometric array of 69 small antennas to synthesise a large aperture; SMAP uses a 6 m rotating mesh antenna. Land-surface monitoring by optical, thermal and radar missions is described in Chapters 13–15.

::: data
**Data box: Essential Climate Variables from space**

Of the 55 Essential Climate Variables defined by the Global Climate Observing System, more than half can only be observed globally from space. Long, stable, cross-calibrated satellite records are a foundation of the assessments of the Intergovernmental Panel on Climate Change (IPCC). Examples are those produced by ESA's Climate Change Initiative, the EUMETSAT Climate Monitoring Satellite Application Facility and NOAA's climate data records. Producing them requires overlap between successive satellites, careful recalibration of old instruments and the reprocessing of decades of data.
:::

::: example
**Example: why a sounder channel "sees" a particular height**

Consider a channel in which the absorption optical depth of the whole atmosphere is $\tau_0 = 40$, in an atmosphere where the absorbing gas density falls with a scale height $H$ = 7.5 km. The optical depth above height $z$ is $\tau(z) = \tau_0 e^{-z/H}$, and the radiation from height $z$ reaching space is attenuated by $e^{-\tau(z)}$. The weighting function $W(z) = d(e^{-\tau(z)})/dz$ peaks where $\tau(z) = 1$:

$$z_{peak} = H \ln \tau_0 = 7.5 \times \ln 40 \approx 28\ \text{km}$$

A channel with $\tau_0 = 4$ peaks at about 10 km; one with $\tau_0 = 600$ at about 48 km (@fig:weighting). The weighting functions are each about 10–15 km wide, which is why sounders need many overlapping channels and why the retrieved profiles are smooth. Hyperspectral sounders with thousands of channels sharpen the vertical resolution considerably.
:::

::: ai
**AI in weather and environmental monitoring**

Artificial intelligence is transforming every stage of the chain. Uses include on-board cloud detection and data compression, fast neural-network radiative-transfer models for data assimilation, and nowcasting of thunderstorms from geostationary imagery. Others are retrieval of precipitation and atmospheric composition, and global AI forecast models such as ECMWF's AIFS. Chapter 47 discusses AI for weather, climate and Earth-system science in depth.
:::

::: key
**Key takeaways**

- Weather satellites are coordinated globally through WMO and CGMS; satellites supply more than 90 % of the observations used in global forecasts.
- Geostationary imagers (ABI, AHI, FCI) scan the full disc every 10 minutes in 16 channels and small regions every 30–60 seconds; lightning mappers and geostationary sounders are the newest additions.
- Polar orbiters in early-morning, mid-morning and afternoon orbits carry infrared and microwave sounders, the most valuable data for numerical weather prediction; GNSS radio occultation provides unbiased anchor measurements.
- Sounding works because channels with different absorption strengths sense different heights (weighting functions).
- Data assimilation combines observations with models; forecast skill has improved by about a day per decade, and AI forecast models became operational in 2025.
- Satellites monitor the ozone layer, air quality (now hourly from geostationary orbit), greenhouse gases, clouds, precipitation and the Earth's energy budget.
- Altimetry shows global sea level rising about 10 cm since 1993 at an accelerating rate. Passive microwave records show Arctic summer sea ice declining about 12 % per decade, and gravity missions weigh the ice sheets' losses.
:::

::: questions
**Review questions**

1. Why are both geostationary and polar-orbiting satellites needed for weather forecasting? What does each do best?
2. Explain how infrared and microwave sounders measure temperature at different heights using weighting functions.
3. Why are GNSS radio-occultation measurements described as "unbiased", and why are they valuable for anchoring other observations?
4. What is data assimilation? Why has forecast skill improved by about one day per decade?
5. How do AI weather-forecast models differ from physics-based numerical models, and what are their present limitations?
6. Why is air-quality monitoring from geostationary orbit an important advance over polar-orbiting measurements?
7. Global mean sea level has risen about 10 cm since 1993. What is the average rate, and why is the present rate higher than the average?
8. Which satellite techniques measure sea ice, ice-sheet mass and soil moisture? Give one mission for each.
:::
