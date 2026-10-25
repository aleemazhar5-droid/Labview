---
title: Space Telescope Engineering
hero: ch38
abstract: A space telescope is a precision optical instrument that must survive launch, unfold or cool itself in orbit, hold its aim to a few thousandths of an arcsecond and send home data from as far as 1.5 million kilometres away. This chapter explains why astronomers go to space at all — atmospheric absorption, blurring and glow — and then the engineering that follows: diffraction-limited optics, segmented and grazing-incidence mirrors, detectors from CCDs to microcalorimeters, sunshields and cryocoolers, fine guidance and jitter control, the choice of orbit, servicing and testing, and the data chain from downlink to public archive. Worked examples size the resolution, photon budget and thermal shielding of real observatories.
---

The first view of the Sun from above the ozone layer came in October 1946, when a spectrograph on a captured V-2 rocket recorded its ultraviolet spectrum. Eighty years later, the James Webb Space Telescope (JWST) observes galaxies as they were less than 300 million years after the Big Bang. Its 6.5 m segmented mirror is held below 50 K behind a sunshield the size of a tennis court. The 36-year-old Hubble Space Telescope still works in low Earth orbit. The Nancy Grace Roman Space Telescope, launched on 30 August 2026, is on its way to the Sun–Earth L2 point.

Every one of these observatories is a compromise between physics and engineering. A larger mirror collects more light and sees finer detail, but must fit inside a rocket fairing. A colder telescope sees fainter infrared sources, but needs sunshields or refrigerators. A more distant orbit is thermally quiet, but cannot be visited for repairs and has a weaker radio link. This chapter explains these trade-offs. Optical payloads and radiometry in general are introduced in Chapter 12; the history and science of individual observatories are covered in Chapter 39, and in-space servicing and assembly in Chapter 40.

## Why Go to Space?

### The Atmosphere as a Filter

Earth's atmosphere is transparent in only two broad windows: visible light with a few near-infrared bands, and radio waves from about 1 cm to 20 m (@fig:atmoswindows). Gamma rays and hard X-rays are scattered and absorbed by nuclei and electrons, so that even balloons at 35–40 km lose much of the signal. Soft X-rays and extreme ultraviolet light are absorbed by nitrogen and oxygen at 80–150 km, which is why X-ray astronomy beyond the Sun began on a sounding rocket in 1962 (Chapter 9). Ozone absorbs ultraviolet light below about 300 nm. Water vapour and carbon dioxide absorb most of the infrared, leaving narrow windows at high, dry sites. The ionosphere reflects radio waves longer than about 20 m. @tbl:atmosbands lists the lowest platform from which each band can be observed.

![Altitude at which half of the incoming radiation from space has been absorbed, as a function of wavelength. Only visible light and radio waves reach the ground; X-ray, gamma-ray, ultraviolet and most infrared astronomy must be done from balloons, rockets or spacecraft.](figures/out/ch38_atmos.svg){#fig:atmoswindows width=86%}

### Seeing, Diffraction and Sky Brightness

Even where the air is transparent, it is not still. Turbulent cells of air at slightly different temperatures act as moving lenses and smear a star into a flickering blob — astronomical **seeing**. At the best mountain sites the blur is about 0.4–1 arcsecond (″; 1″ = 4.85 µrad), whatever the telescope's size. A 2.4 m telescope in space is limited instead by **diffraction** to about 0.05″ in visible light. Ground telescopes now partly correct seeing with **adaptive optics**. But the correction works best in the infrared, over small fields near a bright guide star. It never matches the stability of a space image, which can stay the same for years.

The atmosphere also **glows**: emission lines from hydroxyl radicals near 90 km make the near-infrared night sky bright. In space the darkest background is **zodiacal light**, sunlight scattered and re-emitted by interplanetary dust. Its visible brightness is about 22–23 magnitudes per square arcsecond — somewhat darker than the darkest ground sites. In the near infrared it is hundreds of times darker than the sky seen from the ground. It is this background that sets the limiting magnitude of Hubble and JWST.

### The Infrared Problem: Telescopes That Glow

Everything warm emits infrared radiation. A telescope at room temperature radiates like a blackbody peaking near 10 µm, multiplied by its mirrors' emissivity of a few per cent. @fig:coldtelescope shows the consequence. At 10 µm a 290 K telescope puts a few hundred million times more power into each resolution element than a galaxy of AB magnitude 25. The only cure is cold. At 40 K, JWST's own emission is fainter than even a 30th-magnitude galaxy below about 12 µm and dominates its background only at the longest wavelengths of its Mid-Infrared Instrument (MIRI). Herschel's mirror, at about 85 K, was limited by its own glow, and future far-infrared missions aim for a few kelvin. This single fact drives the sunshields, orbits and cryogenics described later.

![Thermal emission from a telescope (mirror emissivity 0.05) at three temperatures, compared with faint galaxies of AB magnitude 25 and 30. Cooling to 40 K removes the problem below about 12–15 µm; only a few-kelvin telescope is dark in the far infrared.](figures/out/ch38_thermal.svg){#fig:coldtelescope width=84%}

| Band | Wavelength / energy | Main absorber | Lowest useful platform | Space telescopes |
|---|---|---|---|---|
| Gamma rays | > 100 keV | Nuclei, electrons | Balloon (partly), satellite | Fermi, Swift BAT |
| X-rays | 0.1–100 keV | Photoelectric absorption | Rocket, satellite | Chandra, XMM-Newton, XRISM |
| Ultraviolet | 10–320 nm | O₂, O₃ | Rocket, satellite | Hubble, GALEX |
| Visible | 0.32–0.9 µm | (none) | Ground (blurred) | Hubble, Gaia, Euclid |
| Near/mid infrared | 0.9–30 µm | H₂O, CO₂ | Mountain (windows only) | JWST, Spitzer, Roman |
| Far infrared | 30–300 µm | H₂O | Aircraft, balloon | Herschel, planned PRIMA |
| Sub-mm and radio | 0.3 mm–20 m | H₂O (sub-mm) | Ground, high dry sites | Planck (microwave background) |

: Where each band of the electromagnetic spectrum can be observed from. {#tbl:atmosbands}

## Optics: Collecting and Focusing Light

### The Diffraction Limit

A telescope **collects** light in proportion to its area and **resolves** detail in proportion to its diameter. Because light is a wave, a circular aperture of diameter $D$ focuses a point source into an **Airy pattern** — a bright core surrounded by faint rings — whose first dark ring lies at

$$\theta = 1.22\,\frac{\lambda}{D}$$

where $\lambda$ is the wavelength (@fig:airyresolution). Two stars closer than about this angle merge into one (the **Rayleigh criterion**). The core holds 84 % of the light; a central obstruction, such as a Cassegrain secondary mirror, moves light into the rings, which matters for high-contrast imaging. To exploit the diffraction limit, the detector must have at least two pixels across $\lambda/D$ (**Nyquist sampling**). Hubble's cameras, with 40–50 mas (milliarcsecond) pixels, are undersampled about twofold in the visible (Nyquist at 0.5 µm needs 21 mas). They recover detail by combining several offset ("dithered") exposures.

![(a) The Airy pattern of a circular aperture and the effect of a central obstruction, compared with a seeing-limited image of the same total flux. (b) Diffraction-limited resolution versus aperture at five wavelengths; ground-based seeing is shown for comparison.](figures/out/ch38_resolution.svg){#fig:airyresolution width=96%}

::: example
**Example: how sharp is a 6.5 m telescope?**

JWST has an effective diameter of 6.5 m. What is its resolution at 2 µm, and how does it compare with Hubble and with the ground?

1. Diffraction limit: $\theta = 1.22 × 2 × 10^{-6} / 6.5$ = 3.75 × 10⁻⁷ rad. Multiplying by 206 265″/rad gives 0.077″ = 77 mas.
2. Nyquist sampling needs pixels of $\lambda/(2D)$ = 32 mas — almost exactly the 31 mas pixels of JWST's NIRCam short-wavelength channel.
3. Hubble at 0.5 µm: $\theta$ = 1.22 × 0.5 × 10⁻⁶ / 2.4 = 52 mas. JWST at 2 µm is slightly coarser than Hubble in the visible, but at 0.7 µm it reaches 27 mas.
4. Ground seeing of 0.8″ is ten times worse. At the Moon's distance (384 400 km), 77 mas corresponds to 144 m; JWST could separate two car headlights 1.5 m apart at about 4 000 km.
:::

### Telescope Designs

Almost all space telescopes are reflectors: mirrors work from the ultraviolet to the far infrared, have no chromatic aberration and can be supported from behind. The main designs (illustrated in Chapter 12) are the **Cassegrain**, with a concave primary and a convex secondary that folds the light back through a hole in the primary. Hubble is an f/24 **Ritchey–Chrétien** Cassegrain, whose two hyperbolic mirrors remove coma over a wide field. The other main design is the **three-mirror anastigmat (TMA)**, whose third curved mirror corrects astigmatism and field curvature to give a wide, flat field. JWST, Euclid (a compact Korsch variant) and Roman are TMAs; Roman's 0.28 square-degree field is about 200 times that of Hubble's infrared camera. **Off-axis** designs tilt the mirrors so that the secondary and its struts do not block the beam. This gives a clean Airy pattern without diffraction spikes. That is why the planned Habitable Worlds Observatory (HWO) is studying an off-axis aperture for coronagraphy.

### Mirrors: Materials and Lightweighting

A mirror must keep its shape to a small fraction of the wavelength — typically 10–30 nm rms for a visible or near-infrared telescope. It must do so while being launched at several g, cooled or heated by tens of kelvin and held without distortion in weightlessness. The material is chosen for low thermal expansion, high stiffness per unit mass and good thermal conductivity (@tbl:mirrormaterials).

| Material | Density (g/cm³) | Stiffness (GPa) | Expansion at 20 °C (ppm/K) | Conductivity (W/m·K) | Used on |
|---|---|---|---|---|---|
| ULE glass | 2.2 | 68 | ≈ 0 ± 0.03 | 1.3 | Hubble, Roman |
| Zerodur glass-ceramic | 2.5 | 90 | ≈ 0 ± 0.02 | 1.5 | Chandra |
| Beryllium | 1.85 | 300 | 11 (≈ 0 below 100 K) | 216 | JWST, Spitzer |
| Silicon carbide | 3.2 | 420 | 2.2 | 180 | Herschel, Gaia, Euclid |
| Aluminium alloy | 2.7 | 69 | 23 | 167 | Small and cryogenic telescopes |

: Typical room-temperature properties of space mirror materials. {#tbl:mirrormaterials}

Glass mirrors are **lightweighted** by fusing thin face sheets to a honeycomb core. Hubble's 2.4 m primary (@fig:hstprimary) weighs about 828 kg instead of roughly 3 600 kg for a solid blank; Roman's mirror of the same size weighs only 186 kg. **Beryllium** is as stiff as steel but lighter than aluminium, and its expansion almost vanishes below 100 K. That is why JWST and Spitzer use it. Each JWST segment was measured at cryogenic temperature and re-polished warm with the inverse of its cold distortion. **Silicon carbide** combines stiffness and conductivity: Herschel's 3.5 m primary was brazed from 12 SiC petals and machined from 720 kg down to 240 kg.

![Hubble's 2.4 m primary mirror being ground at Perkin-Elmer in Danbury, Connecticut, around 1979. Its ultra-low-expansion glass face sheets are fused to a honeycomb core to cut its mass to about 828 kg.](figures/photos/ch38_hstmirror.jpg){#fig:hstprimary width=52%}

Hubble also taught the most expensive lesson in optical testing. Its primary was polished very precisely — to the wrong shape. A lens in the **null corrector**, the instrument used to check the mirror's figure, was misplaced by about 1.3 mm, so the mirror's edge was about 2 µm too flat. The resulting **spherical aberration** spread most of a star's light into a wide halo. Two cross-checks with other instruments had hinted at the error and been dismissed. The lesson — test flight hardware end-to-end, with independent methods ("test as you fly") — has shaped every programme since.

### Segmented and Deployable Mirrors

Fairing diameter limits a monolithic mirror to about 4–5 m today. JWST's 6.5 m primary is therefore made of 18 hexagonal beryllium segments, each about 1.32 m across flats and weighing about 20 kg. They are coated with about 100 nm of gold, which reflects some 99 % of infrared light. Two wings of three segments fold back for launch, and the secondary mirror is held in front of the primary by a deployable tripod.

Each segment sits on six actuators (a **hexapod**) that set its position and tilt, plus a seventh that changes its curvature, moving in steps of roughly ten nanometres (@fig:jwstactuator). Commissioning in February–April 2022 followed a **wavefront sensing and control** sequence. First, each segment formed its own image of a bright star, and the 18 images were tilted one by one until they overlapped. Then **coarse phasing** with a dispersed Hartmann sensor in NIRCam measured and removed height (piston) differences between segments. Finally, in **fine phasing**, NIRCam took deliberately defocused images through weak lenses, and **phase-retrieval** software computed the wavefront error across the whole pupil for the actuators to correct.

The result beat the requirement. The wavefront error at NIRCam is typically 60–80 nm rms, against a prediction of under 100 nm. The segments drift by less than 10 nm between checks every two days, with small corrections every month or two. One surprise was a micrometeoroid that hit segment C3 in May 2022, larger than pre-launch models predicted. It raised that segment's error from about 56 to more than 250 nm rms, partly corrected to 178 nm. This added about 9 nm to the telescope total. JWST now limits the time it spends looking along its direction of orbital motion, where impacts are more energetic.

![A JWST engineering-model mirror segment with its gold coating. The actuators that position the segment and adjust its curvature are mounted behind it.](figures/photos/ch38_actuator.jpg){#fig:jwstactuator width=50%}

### Grazing Incidence, Coded Masks and Pair Telescopes

X-rays penetrate a normal mirror; they reflect only at **grazing incidence**, at angles below about 1°, and the critical angle shrinks as photon energy rises. A **Wolter type I** telescope therefore uses a ring-shaped paraboloid followed by a hyperboloid, and nests several pairs to increase the collecting area (@fig:xgammaoptics). Chandra has four nested pairs of iridium-coated Zerodur shells, the largest 1.23 m across, with a 10 m focal length (@fig:chandrahrma). Its 1 484 kg mirror assembly resolves better than 0.5″, still the sharpest of any X-ray telescope. XMM-Newton trades sharpness for area with three modules of 58 thin gold-coated nickel shells each. NuSTAR reaches 79 keV with 133 shells per optic coated with **multilayers** — alternating heavy and light layers that reflect like a crystal. The optics sit at the end of a 10 m deployable mast.

At higher energies, imaging uses shadows. Swift's Burst Alert Telescope places a **coded mask** of about 52 000 lead tiles one metre above 32 768 cadmium zinc telluride (CZT) crystals. Each source casts a shifted shadow of the mask. Software decodes the overlapping shadows to locate gamma-ray bursts within seconds. Above about 20 MeV, where a gamma ray mostly turns into matter, each photon is tracked individually. In a **pair-conversion telescope** such as Fermi's Large Area Telescope, a photon turns into an electron–positron pair in a thin tungsten foil. Silicon strip detectors track the pair, and a caesium iodide calorimeter measures its energy.

![Optics for high-energy astronomy: (a) nested Wolter-I grazing-incidence mirrors focus X-rays after two reflections; (b) a coded mask casts a shadow pattern that encodes the direction of each source; (c) a pair-conversion telescope tracks the electron and positron created by a gamma ray.](figures/out/ch38_highenergy.svg){#fig:xgammaoptics width=98%}

![The nested mirror shells of Chandra's High Resolution Mirror Assembly being assembled at Eastman Kodak in Rochester, New York.](figures/photos/ch38_hrma.jpg){#fig:chandrahrma width=50%}

### Blocking the Star: Coronagraphs and Starshades

An Earth-like planet is extremely faint next to its star. With a geometric albedo of 0.2 its brightness relative to the star is $A_g (R_p/a)^2$ ≈ 3.6 × 10⁻¹⁰ at full phase and about 1.2 × 10⁻¹⁰ when half-lit. At 10 parsecs it lies only 0.1″ from the star — about six times $\lambda/D$ for a 6 m telescope in visible light. Seeing it requires suppressing starlight ten-billion-fold close to the diffraction limit.

A **coronagraph** blocks the star's image with a small focal-plane mask, then removes the diffracted light with a **Lyot stop** in a re-imaged pupil. JWST's coronagraphs reach contrasts of order 10⁻⁵, enough for young, self-luminous giant planets in the infrared. Roman's Coronagraph Instrument is the first in space to correct wavefront errors actively with two **deformable mirrors**, and aims to show contrasts of 10⁻⁷ or better. Reaching 10⁻¹⁰ needs a telescope roughly ten times more stable than Roman, with a wavefront steady to picometres over hours, and a coronagraph about a hundred times deeper. This is the central technology challenge for HWO, whose project office aims to mature it before a mission concept review at the end of the decade. However, NASA's FY2027 budget request (not enacted by October 2026) proposed cutting HWO's funding from US$150 million to US$5 million.

The alternative is a **starshade**: a flower-shaped screen tens of metres across, flying tens of thousands of kilometres in front of the telescope, whose petals diffract starlight away while the planet's light passes by (@fig:starshadetest). Laboratory masks have reached 10⁻¹⁰ contrast, but a starshade must travel for days to weeks between target stars. NASA closed out its starshade technology activity in April 2025, and HWO's baseline is a coronagraph.

![A half-scale starshade with four petals deployed at NASA's Jet Propulsion Laboratory in 2014. The precisely shaped petal edges diffract starlight away from the telescope.](figures/photos/ch38_starshade.jpg){#fig:starshadetest width=52%}

## Detectors

### From Photons to Electrons

A detector converts photons into electrical charge and measures it. Its key properties are **quantum efficiency (QE)** — the fraction of photons that produce a detected electron — **read noise**, **dark current** (charge generated thermally in darkness), format and radiation tolerance (@tbl:astrodetectors).

**Charge-coupled devices (CCDs)** store photoelectrons in potential wells and shift them pixel by pixel to one low-noise amplifier, reaching QE above 90 % and read noise of 2–4 electrons. Their weakness in space is **radiation damage**: proton-induced traps capture charge as it is shifted, smearing images. Hubble's CCDs lose transfer efficiency every year, and its pipeline corrects each pixel with a model of the traps. **CMOS** sensors put an amplifier in every pixel, read out faster, need less power and tolerate radiation better.

| Detector | Range | Temperature | Typical format | Examples |
|---|---|---|---|---|
| Silicon CCD | 0.2–1.0 µm | 150–190 K | 4k × 4k | Hubble, Gaia (106 CCDs), Euclid VIS (36) |
| Silicon CMOS | 0.3–1.0 µm | 200–300 K | Up to 4k × 4k | Star trackers, guide cameras, small telescopes |
| HgCdTe (H2RG, H4RG) | 0.6–5.3 µm | 35–100 K | 2k × 2k, 4k × 4k | JWST, Euclid NISP, Roman WFI |
| Si:As impurity band | 5–28 µm | < 7 K | 1k × 1k | JWST MIRI, Spitzer, WISE |
| Bolometers | 60 µm–3 mm | 0.1–0.3 K | 10²–10³ pixels | Herschel SPIRE, Planck HFI |
| X-ray CCD | 0.2–12 keV | ≈ 150 K | 1k × 1k | Chandra ACIS, XMM-Newton EPIC |
| Microcalorimeter | 0.3–12 keV | 0.05 K | 6 × 6 | XRISM Resolve |
| CZT | 3–150 keV | ≈ 290 K | 10⁴ crystals | Swift BAT, NuSTAR |

: Detectors used in space astronomy. {#tbl:astrodetectors}

Infrared photons have too little energy to free electrons in silicon. **Mercury cadmium telluride (HgCdTe)**, whose band gap is set by its composition, is bonded pixel by pixel with indium bumps to a silicon readout circuit. Teledyne's **H2RG** (2048 × 2048 pixels of 18 µm) serves JWST's near-infrared instruments and Euclid; Roman uses 18 **H4RG-10** arrays (4096 × 4096 pixels of 10 µm), about 300 million pixels (@fig:nircamfpa). These arrays are read non-destructively many times "up the ramp" during an exposure, which averages down read noise and lets software remove cosmic-ray hits as sudden jumps. Beyond 5 µm, MIRI uses arsenic-doped silicon **blocked-impurity-band** detectors.

![A replacement focal-plane assembly for JWST's Near Infrared Camera being aligned under a three-dimensional microscope at NASA Goddard. Each assembly holds HgCdTe detector arrays on a precisely flat mount.](figures/photos/ch38_fpa.jpg){#fig:nircamfpa width=52%}

### Bolometers and Microcalorimeters

At far-infrared and millimetre wavelengths, detectors measure the **heat** deposited by radiation. A **bolometer** is a tiny absorber on a weak thermal link to a cold bath, with a sensitive thermometer — a doped semiconductor or a **transition-edge sensor** held on the edge of superconductivity. Planck cooled its bolometers to 0.1 K and mapped the cosmic microwave background to millionths of a kelvin. **Kinetic inductance detectors**, superconducting resonators read by the thousand on one wire, are being developed for future far-infrared missions.

An X-ray **microcalorimeter** measures the heat of single photons. XRISM's Resolve, launched in 2023, has a 6 × 6 array at 50 mK, cooled by adiabatic demagnetisation refrigerators. The tiny temperature rise from each photon gives its energy to about 4.5 eV at 6 keV — some 30 times finer than an X-ray CCD. This reveals the motions of hot gas in galaxy clusters. Its protective gate valve has failed to open, limiting it to energies above about 1.7 keV. Hard X-rays and gamma rays are absorbed in thick, dense semiconductors such as **CZT**, which work at room temperature, or in scintillating crystals.

### Noise and the Photon Budget

Whether a source is detectable depends on how many photons arrive compared with the noise. The **signal-to-noise ratio (SNR)** of a point source measured in an aperture of $n_{pix}$ pixels is

$$\text{SNR} = \frac{S}{\sqrt{S + n_{pix}\,(B + D\,t + n_{read}\,\sigma_{read}^2)}}$$

where $S$ is the number of source electrons, $B$ the sky electrons per pixel, $D$ the dark current, $t$ the exposure time and $\sigma_{read}$ the read noise for each of $n_{read}$ readouts. Faint sources are **background-limited**: SNR grows only as $\sqrt{t}$, so a tenfold longer exposure gains 1.25 magnitudes. A larger telescope helps twice — it collects more light, and its smaller image includes less sky. In one hour, a 2.4 m telescope reaches SNR = 10 at V ≈ 27.2 and a 6.5 m telescope at V ≈ 29.3 (@fig:snrmag).

![Signal-to-noise ratio versus magnitude for 0.3 m, 2.4 m and 6.5 m diffraction-limited space telescopes observing in the visible for 1 hour (solid) and 10 hours (dashed). The dot marks the worked example.](figures/out/ch38_snr.svg){#fig:snrmag width=80%}

::: example
**Example: how many photons from a 25th-magnitude star?**

A V = 25 star is observed for one hour with a 2.4 m telescope (33 % central obstruction) through a V filter (550 nm, 88 nm wide) with 30 % overall throughput.

1. A V = 0 star delivers 3.63 × 10⁻¹¹ W m⁻² nm⁻¹. Each 550 nm photon carries $hc/\lambda$ = 3.61 × 10⁻¹⁹ J, so the flux is 1.0 × 10⁸ photons s⁻¹ m⁻² nm⁻¹.
2. V = 25 is 10⁻¹⁰ times fainter: 0.88 photons s⁻¹ m⁻² across the 88 nm band.
3. Collecting area $(\pi/4) × 2.4^2 × (1 - 0.33^2)$ = 4.03 m² gives 3.6 photons/s; with 30 % throughput, 1.07 electrons/s, or 3 850 per hour, of which 80 % (3 080) fall in the measuring aperture.
4. Noise: zodiacal sky (22.7 mag/arcsec²) adds 335 electrons, dark current 337 and read noise 673 (19 pixels, four readouts of 3 electrons). Total noise = √(3 080 + 335 + 337 + 673) = 66.5 electrons.
5. SNR = 3 080 / 66.5 ≈ **46**. A star some 40 million times fainter than the faintest visible to the naked eye (V ≈ 6) yields about one detected photon per second on a Hubble-sized telescope.
:::

## Keeping Cold and Clean

### Passive Cooling and Sunshields

The simplest way to cool a telescope is to let it radiate to deep space while shading it from the Sun, Earth and Moon. Radiation scales with the fourth power of temperature, so a 40 K surface can reject only 0.15 W per square metre even with perfect emissivity. Every milliwatt leaking from the warm spacecraft must therefore be intercepted.

JWST's **sunshield** is the extreme example (@fig:jwstsunshield). Five membranes of Kapton E, the first 50 µm thick and the rest 25 µm, span about 21 m by 14 m. They are coated with about 100 nm of aluminium and, on the two Sun-facing layers, doped silicon. More than 200 kW of sunlight falls on the first layer, which reaches up to about 383 K in NASA's thermal models. Only about 23 mW reaches the telescope side, where the last layer is near 36–40 K. The layers never touch, and they are **flared** — closer at the centre and wider apart at the edges — so that heat radiated into each gap escapes sideways to space (@fig:sunshieldmodel).

![JWST's full-size sunshield test unit stacked and unfurled in a cleanroom. The five membranes, each thinner than a human hair, are separated by gaps that let heat escape out of the edges.](figures/photos/ch38_sunshield.jpg){#fig:jwstsunshield width=56%}

![(a) The five flared sunshield layers between the Sun and the telescope. (b) Layer temperatures in two simple radiative models: a sealed stack, in which heat can only pass through the layers, and vented layers, each of which passes on about a tenth of the heat it receives.](figures/out/ch38_sunshield.svg){#fig:sunshieldmodel width=94%}

::: example
**Example: why the sunshield gaps must be open**

At L2, sunlight delivers $S$ = 1 361 / 1.01² = 1 334 W/m², so the 200 kW on JWST's first layer implies about 150 m² facing the Sun.

1. A plate absorbing all this sunlight and radiating from one face reaches $(S/\sigma)^{1/4}$ = 392 K — close to the first layer's 383 K maximum.
2. **Sealed stack.** If the five layers formed a closed sandwich with low-emissivity faces (ε = 0.05), each of the four gaps would have a radiative resistance of $(2/\varepsilon - 1)$ = 39. With the first layer at 360 K and the last at 40 K, the heat flow is $q = \sigma (360^4 - 40^4) / (4 × 39)$ = 6.1 W/m², about 900 W in all.
3. To radiate 6.1 W/m², the cold layer would have to warm to at least 102 K even with perfect emissivity — far too warm for a mid-infrared telescope.
4. **Vented layers.** The real leak, 23 mW over 150 m², is 0.15 mW/m² — about 40 000 times less. Suppose each vented layer passes on a tenth of the heat it receives. Then four steps reduce the radiated flux by 10⁻⁴ and the temperature by $(10^{-4})^{1/4}$ = 0.1: from 360 K to 36 K, as @fig:sunshieldmodel shows.
:::

### Cryocoolers and Cryogens

Passive cooling stops at about 30–40 K for a large telescope near Earth. Early infrared missions carried **cryostats** of liquid helium that slowly boiled away. Spitzer's lasted from 2003 to 2009, after which it continued a "warm" mission at about 30 K. Herschel's 2 300 litres of superfluid helium ran out in April 2013, ending its science. Spitzer pioneered the **warm launch**: only the instruments sat inside the cryostat, and the telescope cooled in space by radiating from its black outer shell.

Mechanical **cryocoolers** do not run out. JWST's MIRI detectors must stay below 7 K. Its cooler (@fig:miricooler) uses a three-stage **pulse-tube** precooler, driven by a compressor in the warm spacecraft bus, to chill helium gas to about 14 K. The helium then flows about 10 m to a **Joule–Thomson** stage beside MIRI. There, expansion through an orifice less than 1 mm wide cools it to about 6 K. The only moving parts are horizontally opposed pistons, balanced so as not to shake the telescope. For 0.1 K and below, Planck used a dilution refrigerator and XRISM uses magnetic refrigeration.

![The flight cryocooler for JWST's Mid-Infrared Instrument after testing in 2016, before it was shipped to Northrop Grumman for installation on the spacecraft. It cools MIRI's detectors to below 7 K, about 30 K colder than the rest of the telescope.](figures/photos/ch38_cryocooler.jpg){#fig:miricooler width=52%}

### Stray Light and Contamination

**Stray light** is sunlight or earthshine scattered off baffles and struts, light from bright stars outside the field, or glow from warm structures. It is controlled with baffles, black coatings and field stops. These are designed by tracing millions of rays through a model of the telescope (Chapter 12). Mirror microroughness of a few nanometres scatters light into a halo that hides faint objects near bright ones.

**Contamination** is the other enemy. Molecules **outgassing** from adhesives, cables and insulation condense on cold optics; a film a few nanometres thick absorbs far-ultraviolet light. Space materials are screened for outgassing (typically below 1 % total mass loss and 0.1 % condensable material), baked in vacuum and assembled in cleanrooms under dry-nitrogen purge. Water is the hardest contaminant to eliminate. After **Euclid**'s launch in July 2023 its throughput fell steadily as water released by insulation condensed as ice on its cold mirrors. In March 2024 ESA warmed a mirror behind the main optics from about 126 K to 160 K for under two hours, and repeated the procedure in June. The visible camera regained about 15 % more light, and throughput has been stable since (@fig:euclidlaunch).

![ESA's Euclid being secured to the adapter of its Falcon 9 launcher in June 2023. The white cylinder houses the 1.2 m silicon-carbide telescope; the black solar panels also shade it from the Sun.](figures/photos/ch38_euclid.jpg){#fig:euclidlaunch width=52%}

## Pointing and Stability

### Sensing and Control

Coarse pointing uses sun sensors, star trackers and gyroscopes, as on any spacecraft (Chapter 6). The final step is a **fine guidance sensor (FGS)** that measures a guide star's position in the telescope's own focal plane, so that flexing between a separate star tracker and the instrument does not matter. Hubble's three interferometric FGS and four **reaction wheels** hold a target to about 7 mas rms over 24 hours. JWST's FGS reads guide stars 16 times a second and drives a **fine steering mirror**; in orbit its jitter is about 1 mas per axis, several times better than required.

Jitter blurs the image and lowers its peak brightness (@fig:jitterblur). A useful rule is that it should stay below about a tenth of $\lambda/D$: 4–5 mas for Hubble at 0.5 µm, and about 2 mas for a future 6 m ultraviolet–optical telescope. Coronagraphy is stricter still, because drift moves starlight off the mask; HWO studies discuss sub-milliarcsecond pointing together with picometre wavefront stability.

![Effect of line-of-sight jitter on (a) image width and (b) peak brightness for three telescopes. Hubble's 7 mas requirement and JWST's measured jitter of about 1 mas are marked.](figures/out/ch38_jitter.svg){#fig:jitterblur width=94%}

Most jitter comes from inside the spacecraft. **Reaction wheels** spinning at thousands of revolutions per minute have tiny imbalances that shake the structure; cryocooler compressors, **thermal snaps** and flexing solar arrays add more. Hubble's first solar arrays vibrated every time the telescope crossed from shadow into sunlight, until stiffer arrays were fitted in 1993 and 2002. Engineers balance wheels and choose speeds that avoid structural resonances. They mount wheels or whole telescopes on soft **isolators** (JWST has a passive isolator between its bus and telescope). They also stiffen and damp the structure, and close fast optical loops with steering mirrors.

### Hubble's Gyroscopes

Hubble's gyroscopes sense rotation through a spinning wheel floating in fluid, connected by thin wires called **flex leads** that corrode; by 2023, 8 of the 22 gyros flown had failed. Hubble carries six and normally used three. Servicing Mission 4 replaced all six in 2009 — the last time this was possible. After a gyro repeatedly gave faulty readings in 2024, NASA switched Hubble to **one-gyro mode** in June 2024, keeping its other working gyro in reserve. Magnetometers, sun sensors and star trackers fill the gaps during slews. NASA expected about 12 % lower efficiency (74 instead of 85 orbits of observing a week) and slower target acquisition. It also expected less sky available at any time and no tracking of targets closer than Mars. Image quality is unchanged. NASA estimated a better than 70 % chance of at least one gyro working through 2035; by late 2025 the observing success rate was back above 90 %, with no safe-mode events since the switch.

### Scanning Telescopes

Not every telescope stares. **Gaia** spun once every six hours, sweeping two fields of view across the sky. As it spun, its 106 CCDs moved charge in step with the star images — **time-delay integration**, as in pushbroom Earth imagers (Chapter 14). Over 10.5 years it measured positions of nearly two billion stars to tens of microarcseconds. Planck spun once a minute to map the microwave background, and WISE and SPHEREx scanned the whole sky. Scanning simplifies attitude control but demands precise knowledge of the spin axis and a readout synchronised to the motion.

## Where to Put a Telescope

The orbit sets a telescope's thermal environment, observing efficiency, data rate and whether it can be serviced (@fig:telescopeorbits, @tbl:orbittrades).

![Telescope orbits: (a) low Earth orbit (Hubble), Chandra's highly elliptical orbit and TESS's lunar-resonant orbit, to scale; (b) a halo orbit around Sun–Earth L2 (schematic); (c) the slow drift of an Earth-trailing telescope such as Kepler, in a frame rotating with the Earth.](figures/out/ch38_orbits.svg){#fig:telescopeorbits width=93%}

**Low Earth orbit** is cheap to reach and was the only orbit the Space Shuttle could service, so Hubble flies at about 470 km. But Earth hides most targets for part of every 95-minute orbit. The telescope crosses the **South Atlantic Anomaly**, where trapped protons swamp the detectors, and it passes from sunlight to shadow about 15 times a day. Heaters hold Hubble's mirrors at about 21 °C. **Highly elliptical orbits** give long, uninterrupted views: Chandra's 64-hour orbit, now about 12 650 × 136 200 km, keeps it above the radiation belts for most of each orbit. TESS uses a stable 2:1 resonance with the Moon.

**Sun–Earth L2**, 1.5 million km beyond Earth on the anti-Sun side, has become the standard home of large infrared and survey telescopes: Herschel, Planck, Gaia, JWST, Euclid and, from December 2026, Roman. The Sun, Earth and Moon always lie in roughly the same direction, so one sunshield blocks all three, and the thermal environment is almost constant. L2 is unstable, so telescopes fly **halo orbits** around it with small station-keeping burns every few weeks; JWST's accurate launch left propellant for more than 20 years. **Earth-trailing** heliocentric orbits, used by Spitzer and Kepler, need no station-keeping, but the telescope drifts away — Kepler fell behind by about 7° a year — so its radio link weakens with time.

| Orbit | Examples | Thermal | Observing efficiency | Downlink | Servicing |
|---|---|---|---|---|---|
| LEO | Hubble, Swift, Fermi | Cycles every 95 min | ≈ 50 % | Relay satellites, ground passes | Possible |
| Highly elliptical | Chandra, XMM-Newton, TESS | Long stable arcs | High; day-long exposures | Ground stations | No |
| Sun–Earth L2 | JWST, Euclid, Gaia, Roman | Nearly constant | Very high | Deep-space antennas | Not designed for it |
| Earth-trailing | Spitzer, Kepler | Very stable, cold | Very high | Weakens with distance | No |

: Trade-offs between orbits for space telescopes. {#tbl:orbittrades}

## Building, Testing and Servicing

### Test as You Fly

A telescope that cannot be repaired is tested on the ground at the temperatures and in the configuration it will fly. Complete observatories are shaken on vibration tables, exposed to the acoustic roar of launch and tested in **thermal-vacuum** chambers. JWST's telescope and instruments spent about 100 days in 2017 inside Chamber A at NASA's Johnson Space Center — a 36 m tall chamber built for Apollo. They were cooled by liquid-nitrogen and helium shrouds while optical tests confirmed that the segments could be aligned at operating temperature (@fig:chamberatest). Gravity sag, which cannot be removed on the ground, is predicted with finite-element models and checked by testing mirrors face-up and face-down. JWST's deployments were rehearsed many times; after launch on 25 December 2021, its roughly 50 major deployments took two weeks and all worked.

### Hubble Servicing Missions

Hubble was designed to be serviced, with handholds, standard bolts and **orbital replacement units** — instruments, batteries, gyroscopes, computers — that astronauts could exchange during spacewalks from the Space Shuttle (Chapter 33). Five missions between 1993 and 2009 corrected its optics, replaced all of its original instruments and extended its life by decades (@tbl:hstservicing).

| Mission | Date | Shuttle | Main work |
|---|---|---|---|
| SM1 | Dec 1993 | Endeavour (STS-61) | COSTAR corrective optics; WFPC2; new solar arrays and gyros |
| SM2 | Feb 1997 | Discovery (STS-82) | STIS spectrograph; NICMOS infrared camera; solid-state recorder |
| SM3A | Dec 1999 | Discovery (STS-103) | All six gyros after Hubble entered safe mode; new computer |
| SM3B | Mar 2002 | Columbia (STS-109) | Advanced Camera for Surveys; rigid solar arrays; NICMOS cryocooler |
| SM4 | May 2009 | Atlantis (STS-125) | WFC3 and COS; repair of ACS and STIS; six gyros; batteries |

: The five Hubble servicing missions. {#tbl:hstservicing}

On the first mission astronauts installed COSTAR — small deployable mirrors that refocused light for three instruments — and replaced the Wide Field/Planetary Camera with WFPC2, whose internal optics compensated for the mirror error (@fig:sm1wfpc). Without shuttle visits, Hubble's orbit is slowly decaying, from more than 600 km at its launch in 1990 to about 470 km in 2026. NASA has studied but not ordered a commercial reboost; without one, STScI's median forecast for re-entry is late 2033.

::: figrow
![JWST's telescope and science instruments inside Chamber A at NASA's Johnson Space Center in 2017, before cryogenic vacuum testing that simulated the cold of space.](figures/photos/ch38_chambera.jpg){#fig:chamberatest}

![Astronaut Jeffrey Hoffman holds the original Wide Field/Planetary Camera in Endeavour's payload bay during the first Hubble servicing mission in December 1993, after replacing it with WFPC2.](figures/photos/ch38_wfpc.jpg){#fig:sm1wfpc}
:::

### Assembling the Next Generation in Space

JWST shows how far folding can go: a 6.5 m aperture inside a 5 m fairing. Apertures of 10–20 m may need to be assembled in orbit from separately launched segments, by robots or astronauts, and aligned with the same wavefront sensing used on JWST. HWO studies include standard interfaces and an orbit a future servicing vehicle could reach, so that instruments could be upgraded as Hubble's were (Chapter 40).

## From Photons to Archives

### Downlink and Storage

Data volume grows with detector size, and the downlink must keep pace (@tbl:telescopedata). Hubble sends about 18 GB of science data a week through NASA's Tracking and Data Relay Satellites. JWST stores data on a 68 GB solid-state recorder. It sends up to about 57 GB a day to the Deep Space Network's 34 m antennas on a 25.9 GHz Ka-band link. At up to 28 Mbit/s, this takes about 4.5 hours of transmission. Euclid returns about 100 GB of compressed data a day in a four-hour pass. Roman will send about 1.4 TB a day at up to 500 Mbit/s to stations in New Mexico, Australia and Japan — more than Hubble returns in a year.

| Telescope | Launched | Aperture | Band | Orbit | Data per day |
|---|---|---|---|---|---|
| Hubble | 1990 | 2.4 m | 0.115–1.7 µm | LEO, 470 km | ≈ 2.6 GB |
| Chandra | 1999 | 1.2 m (outer shell) | 0.1–10 keV | 12 650 × 136 200 km | Small (photon lists) |
| JWST | 2021 | 6.5 m | 0.6–28.5 µm | L2 halo | ≈ 57 GB (28 Mbit/s) |
| Euclid | 2023 | 1.2 m | 0.55–2.0 µm | L2 halo | ≈ 100 GB (≈ 75 Mbit/s) |
| Roman | 2026 | 2.4 m | 0.48–2.3 µm | L2 halo | ≈ 1.4 TB (≤ 500 Mbit/s) |

: Five major space telescopes and their data rates. {#tbl:telescopedata}

### Pipelines and Archives

Raw data are useless until calibrated. Each observatory runs a **pipeline**. For JWST, stage 1 fits the slope of each pixel's ramp and removes cosmic rays, and stage 2 applies flat fields, flux calibration and sky coordinates. Stage 3 combines dithered exposures into mosaics, spectra and catalogues. Data are reprocessed as calibrations improve. The **Mikulski Archive for Space Telescopes (MAST)** at the Space Telescope Science Institute holds data from about 20 NASA missions, including Hubble, JWST and TESS, and soon Roman. It passed 3 petabytes in 2017 and has grown rapidly since. Copies are kept in commercial clouds so that researchers can analyse data where they are stored. Most observations become public within a year, and archival research now produces a large share of published papers — the archive, not the telescope, is the observatory's lasting product.

::: ai
**AI in space telescope operations**

Machine learning appears throughout a space telescope's life (Chapter 51). Neural networks trained on simulated defocused star images can estimate wavefront errors directly, complementing iterative phase retrieval. Scheduling has used artificial intelligence since Hubble's SPIKE planner, built at STScI in the late 1980s around constraint-based search; modern schedulers juggle thousands of observations and their constraints. In data reduction, deep-learning models flag cosmic rays and detector artefacts, classify galaxy shapes and find rare objects among billions. Euclid's first quick data release combined neural networks with citizen scientists to search for strong gravitational lenses. The challenge is trust: every automated decision must be validated against physics and be reproducible from the archive (Chapter 53).
:::

::: key
**Key takeaways**

- The atmosphere absorbs gamma rays, X-rays, ultraviolet and most infrared light, blurs images and glows; space offers the whole spectrum, diffraction-limited images and a dark, stable sky.
- Resolution is set by 1.22 λ/D and sensitivity by collecting area and background. JWST resolves 77 mas at 2 µm, and a 2.4 m telescope reaches V ≈ 27 at SNR = 10 in an hour.
- Large apertures use lightweighted glass, beryllium or silicon carbide, and segmented mirrors aligned in orbit to tens of nanometres; X-ray telescopes need nested grazing-incidence mirrors, gamma rays coded masks or pair-conversion trackers.
- Infrared telescopes must be cold: JWST's edge-vented, five-layer sunshield cuts 200 kW of sunlight to about 23 mW, and a cryocooler takes MIRI below 7 K.
- Fine guidance sensors, quiet wheels, isolation and steering mirrors hold pointing to milliarcseconds; Hubble has operated on one gyroscope since 2024.
- Sun–Earth L2 gives large telescopes a cold, stable home at the cost of servicing; Hubble's five servicing missions showed the value of designing for repair.
- Data rates have grown from gigabytes a week (Hubble) to terabytes a day (Roman); pipelines and archives matter as much as telescopes.
:::

::: questions
**Review questions**

1. Why must X-ray and far-infrared astronomy be done above the atmosphere? What does a space telescope gain in the visible?
2. Calculate the diffraction limit of a 1.2 m telescope at 0.8 µm and at 2 µm in milliarcseconds, and the pixel size that Nyquist-samples each.
3. Using @fig:coldtelescope, explain why MIRI is limited by the telescope's own emission at its longest wavelengths. What would cooling the telescope to 10 K gain?
4. Compare beryllium, ULE and SiC mirrors for a warm UV and a 40 K infrared telescope.
5. Describe the steps used to align JWST's 18 segments in orbit. Why could the alignment not be completed on the ground?
6. Why do X-ray telescopes use grazing incidence and nested mirror shells?
7. A 6 m telescope observes an Earth twin at 15 pc at 0.5 µm. How many multiples of λ/D separate planet and star, and what contrast is needed?
8. Repeat the photon-budget example for a 6.5 m telescope. Why does the SNR improve by more than the ratio of diameters?
9. Use the sealed-stack calculation to explain why JWST's sunshield gaps are open.
10. Compare LEO, a highly elliptical orbit and Sun–Earth L2 for a new ultraviolet–optical telescope that should be serviceable.
:::
