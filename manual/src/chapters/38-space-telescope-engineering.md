---
title: Space Telescope Engineering
hero: ch38
abstract: A space telescope is a precision optical instrument that must survive launch, unfold or cool itself in orbit, hold its aim to a few thousandths of an arcsecond and send home data from as far as 1.5 million kilometres away. This chapter explains why astronomers go to space at all — atmospheric absorption, blurring and glow — and then the engineering that follows: diffraction-limited optics, segmented and grazing-incidence mirrors, detectors from CCDs to microcalorimeters, sunshields and cryocoolers, fine guidance and jitter control, the choice of orbit, servicing and testing, and the data chain from downlink to public archive. Worked examples size the resolution, photon budget and thermal shielding of real observatories.
---

The first telescope to leave the atmosphere was a small spectrograph on a captured V-2 rocket in 1946, which recorded the Sun's ultraviolet spectrum for the first time. Eighty years later, the James Webb Space Telescope (JWST) — a 6.5 m segmented mirror held below 50 K behind a sunshield the size of a tennis court — observes galaxies that formed less than 300 million years after the Big Bang, while the 36-year-old Hubble Space Telescope still works in low Earth orbit and the Nancy Grace Roman Space Telescope, launched on 30 August 2026, is on its way to the Sun–Earth L2 point.

Every one of these observatories is a compromise between physics and engineering. A larger mirror collects more light and sees finer detail, but must fit inside a rocket fairing. A colder telescope sees fainter infrared sources, but needs sunshields, radiators or refrigerators. A more distant orbit is thermally quiet, but cannot be visited for repairs and has a weaker radio link. This chapter explains these trade-offs and the technology used to resolve them. The general principles of optical payloads and radiometry are introduced in Chapter 12; the history and science of individual observatories are covered in Chapter 39; and robotic servicing and in-space assembly in Chapter 40.

## Why Go to Space?

### The Atmosphere as a Filter

Earth's atmosphere is transparent in only two broad windows: visible light with the near ultraviolet and a few near-infrared bands, and radio waves from about 1 cm to about 20 m (@fig:atmoswindows). Almost everything else is absorbed high above the ground:

- **Gamma rays and hard X-rays** are scattered and absorbed by atomic nuclei and electrons (Compton scattering and pair production). Even at balloon altitudes of 35–40 km, the residual few grams per square centimetre of air removes much of the signal.
- **Soft X-rays and extreme ultraviolet** are stopped by photoelectric absorption in nitrogen and oxygen at 80–150 km, which is why X-ray astronomy began on sounding rockets in 1962 (Chapter 9).
- **Ultraviolet** light below about 300 nm is absorbed by ozone at 20–50 km and by molecular oxygen higher up.
- **Infrared** light is absorbed in many bands by water vapour and carbon dioxide; only narrow windows reach high, dry mountain sites, and the far infrared (30–300 µm) requires aircraft altitudes or above.
- **Long radio waves** (beyond about 20 m) are reflected by the ionosphere.

![Altitude at which half of the incoming radiation from space has been absorbed, as a function of wavelength. Only visible light and radio waves reach the ground; X-ray, gamma-ray, ultraviolet and most infrared astronomy must be done from balloons, rockets or spacecraft.](figures/out/ch38_atmos.svg){#fig:atmoswindows width=96%}

@tbl:atmosbands summarises where each band can be observed from.

| Band | Wavelength / energy | Main absorber | Lowest useful platform | Example space telescopes |
|---|---|---|---|---|
| Gamma rays | > 100 keV | Nuclei, electrons | Balloon (partly); satellite | Fermi, Swift BAT, INTEGRAL |
| X-rays | 0.1–100 keV | Photoelectric absorption | Rocket or satellite | Chandra, XMM-Newton, XRISM, NuSTAR |
| Ultraviolet | 10–320 nm | O₂, O₃ | Rocket or satellite | Hubble (COS, STIS), GALEX |
| Visible | 0.32–0.9 µm | (none) | Ground (blurred) | Hubble, Gaia, Euclid VIS |
| Near/mid infrared | 0.9–30 µm | H₂O, CO₂ | Mountain (windows only) | JWST, Spitzer, WISE, Roman |
| Far infrared | 30–300 µm | H₂O | Aircraft, balloon | Herschel, planned PRIMA |
| Sub-mm, radio | 0.3 mm–20 m | H₂O (sub-mm) | Ground, high dry sites | Planck (CMB), space VLBI |

: Where each band of the electromagnetic spectrum can be observed from. {#tbl:atmosbands}

### Seeing, Diffraction and Sky Brightness

Even where the air is transparent, it is not still. Turbulent cells of air with slightly different temperatures act as moving lenses and smear a star's image into a flickering blob — astronomical **seeing**. At the best mountain sites the blur is about 0.4–1 arcsecond (″; 1″ = 4.85 µrad), regardless of the telescope's size. A 2.4 m telescope in space is limited instead by **diffraction** to about 0.05″ in visible light, more than ten times sharper. Ground telescopes now partly correct seeing with **adaptive optics** — deformable mirrors that cancel the distortion hundreds of times per second — but the correction works best in the infrared, over small fields, near a bright guide star, and never reaches the stability of a space telescope's image, which can stay the same for years.

The atmosphere also **glows**. Emission lines from hydroxyl (OH) radicals 85 km up make the near-infrared night sky hundreds of times brighter than the faint galaxies astronomers want to see, and scattered moonlight and city lights add more. In space, the darkest background is **zodiacal light**: sunlight scattered and re-emitted by interplanetary dust. Near Earth's orbit it has a visible surface brightness of about 22–23 magnitudes per square arcsecond — roughly ten times darker than the best ground sites in the near infrared and comparable in the visible — and it is the background that sets the limiting magnitude of Hubble and JWST.

### The Infrared Problem: Telescopes That Glow

Everything warm emits infrared radiation. A telescope at room temperature (about 290 K) radiates like a blackbody peaking near 10 µm, multiplied by the emissivity of its mirrors — typically a few per cent. @fig:coldtelescope shows the result: at 10 µm a 290 K telescope emits about a million times more power into each resolution element than the faint galaxies JWST studies. The only cure is to make the telescope cold. At 40 K, JWST's own emission is negligible below about 15 µm and only starts to dominate its background at the longest wavelengths of its Mid-Infrared Instrument (MIRI). A far-infrared telescope must be colder still — Herschel's mirror was at about 85 K and was limited by its own glow, and future far-infrared missions aim for a few kelvin. This single fact drives the sunshields, orbits and cryogenic engineering described later in this chapter.

![Thermal emission from a telescope with mirror emissivity 0.05 at three temperatures, compared with faint galaxies of AB magnitude 25 and 30. A warm telescope outshines faint infrared sources by factors of up to a million; cooling to 40 K removes the problem below about 15 µm, and only a few-kelvin telescope is dark in the far infrared.](figures/out/ch38_thermal.svg){#fig:coldtelescope width=92%}

## Optics: Collecting and Focusing Light

### The Diffraction Limit

A telescope does two jobs: it **collects** light, in proportion to its area, and it **resolves** detail, in proportion to its diameter. Because light is a wave, a circular aperture of diameter $D$ cannot focus a point source to a point. It produces an **Airy pattern** — a bright core surrounded by faint rings — whose first dark ring lies at

$$\theta = 1.22\,\frac{\lambda}{D}$$

where $\lambda$ is the wavelength (@fig:airyresolution). Two stars closer than about this angle merge into one (the **Rayleigh criterion**). The core contains 84 % of the light. A central obstruction, such as the secondary mirror of a Cassegrain telescope, slightly narrows the core but moves light into the rings, which matters for high-contrast imaging.

![(a) The Airy pattern of a circular aperture and the effect of a central obstruction, compared with a seeing-limited image of the same total flux. (b) Diffraction-limited resolution versus aperture at five wavelengths; ground-based seeing is shown for comparison.](figures/out/ch38_resolution.svg){#fig:airyresolution width=98%}

To exploit the diffraction limit, the detector must **sample** the image finely enough: the Nyquist criterion requires at least two pixels across $\lambda/D$. JWST's NIRCam short-wavelength channel has 31 mas (milliarcsecond) pixels, matched to 2 µm; Hubble's cameras use 40–50 mas pixels in the visible, slightly undersampled, and recover the lost detail by combining several dithered exposures.

::: example
**Example: resolution of a 6.5 m telescope at 2 µm**

JWST has an effective diameter of 6.5 m. What is its resolution at 2 µm, and how does it compare with Hubble and with the ground?

1. Diffraction limit: $\theta = 1.22 × 2 × 10^{-6} / 6.5$ = 3.75 × 10⁻⁷ rad. Multiplying by 206 265″/rad gives 0.077″ = 77 mas.
2. Nyquist sampling needs pixels of $\lambda/(2D)$ = 3.08 × 10⁻⁷ / 2 rad = 32 mas — almost exactly NIRCam's 31 mas short-wavelength pixels.
3. Hubble at 0.5 µm: $\theta$ = 1.22 × 0.5 × 10⁻⁶ / 2.4 = 52 mas. JWST at 2 µm is slightly coarser than Hubble in the visible, but at 0.7 µm (its shortest wavelengths) it reaches 27 mas.
4. Ground seeing of 0.8″ is ten times worse than JWST at 2 µm. At the distance of the Moon (384 400 km), 77 mas corresponds to 144 m; JWST could separate two car headlights 1.5 m apart at a distance of about 4 000 km.
:::

### Telescope Designs

Almost all space telescopes are reflectors, because mirrors work at all wavelengths from the ultraviolet to the far infrared, have no chromatic aberration and can be supported from behind. The common designs (illustrated in Chapter 12) are:

- **Cassegrain** — a concave primary and a convex secondary that folds the light back through a hole in the primary, giving a long focal length in a short tube. Hubble is an f/24 **Ritchey–Chrétien** (RC) Cassegrain, in which both mirrors are hyperbolic to remove coma and give a sharp field of about 0.3°.
- **Three-mirror anastigmat (TMA)** — a third curved mirror corrects astigmatism and field curvature, giving a wide, flat field. JWST, Euclid (a compact **Korsch** variant) and Roman are TMAs; Roman's 0.28 square-degree field is about 100 times Hubble's infrared field.
- **Off-axis (unobscured)** designs tilt the mirrors so that the secondary does not block the beam. They produce a clean Airy pattern without diffraction spikes from support struts, which is why the planned Habitable Worlds Observatory (HWO) is studying off-axis apertures for coronagraphy.
- **Schmidt** cameras, with a thin corrector plate in front of a spherical mirror, give very wide fields; Kepler used a 0.95 m Schmidt to stare at 115 square degrees.

The **focal ratio** (f-number, focal length divided by aperture) sets the plate scale. A long focal ratio such as Hubble's f/24 spreads the image over more pixels, allowing fine sampling with large detector pixels; a fast system (f/1–f/3) concentrates light for wide-field surveys but is harder to align.

### Mirrors: Materials and Lightweighting

A mirror must keep its shape to a small fraction of the wavelength — typically 10–30 nm rms for a visible or near-infrared telescope — while being launched at several g, cooled or heated by tens of kelvin, and held without distortion in zero gravity. The material is chosen for low thermal expansion, high stiffness per unit mass and good thermal conductivity (@tbl:mirrormaterials).

| Material | Density (g/cm³) | Stiffness E (GPa) | Expansion near 20 °C (ppm/K) | Conductivity (W/m·K) | Used on |
|---|---|---|---|---|---|
| ULE glass (titania–silica) | 2.2 | 68 | ≈ 0 ± 0.03 | 1.3 | Hubble, Roman |
| Zerodur (glass-ceramic) | 2.5 | 90 | ≈ 0 ± 0.02 | 1.5 | Chandra, many ground telescopes |
| Beryllium | 1.85 | 300 | 11 (near zero below 100 K) | 216 | JWST, Spitzer, IRAS |
| Silicon carbide | 3.2 | 420 | 2.2 | 180 | Herschel, Gaia, Euclid |
| Aluminium alloy | 2.7 | 69 | 23 | 167 | Small and cryogenic IR telescopes |

: Typical properties of space mirror materials (room-temperature handbook values). {#tbl:mirrormaterials}

Glass mirrors are **lightweighted** by fusing thin face sheets to a honeycomb core. Hubble's 2.4 m ULE primary (@fig:hstprimary) weighs about 828 kg instead of the roughly 3 600 kg of a solid blank, an areal density of about 180 kg/m². Thirty years later, Roman's mirror of the same size weighs 186 kg — less than a quarter as much. **Beryllium** is as stiff as steel but lighter than aluminium; its expansion coefficient falls almost to zero below 100 K, which is why it was chosen for JWST and Spitzer, but it is toxic to machine and must be polished cold-and-warm repeatedly to remove cryogenic distortion. **Silicon carbide** combines high stiffness and conductivity; Herschel's 3.5 m primary was brazed from 12 SiC petals and machined from 720 kg down to 240 kg, about 25 kg/m².

![Hubble's 2.4 m primary mirror at Perkin-Elmer in 1979. The ultra-low-expansion glass face sheets are fused to a honeycomb core to cut its mass to about 828 kg.](figures/photos/ch38_hstmirror.jpg){#fig:hstprimary width=60%}

Hubble also taught the most expensive lesson in optical testing. Its primary was polished very precisely — to the wrong shape. A lens in the **null corrector**, the test instrument used to check the mirror's shape, was out of position by about 1.3 mm, so the mirror's edge was about 2 µm too flat, producing **spherical aberration** that spread 85 % of a star's light into a halo. The error had been hinted at by a cross-check with a different instrument and dismissed. It was corrected in 1993 by optics designed with the same error in reverse (Hubble Servicing Missions, below). The lesson — test the flight hardware end-to-end, with independent methods, "test as you fly" — shaped every later programme.

### Segmented and Deployable Mirrors

Fairing diameter limits a monolithic mirror to about 4–5 m, or perhaps 8 m in future heavy-lift vehicles (Chapter 34). JWST's 6.5 m primary is therefore made of 18 hexagonal beryllium segments, each about 1.32 m across flat to flat and weighing about 20 kg, coated with roughly 100 nm of gold, which reflects about 99 % of infrared light. Two wings of three segments each fold back for launch and are swung into place in orbit. The secondary mirror is held 7 m in front of the primary on a deployable tripod.

Folding a mirror means that its alignment must be set in space. Each JWST segment sits on six actuators (a **hexapod**) that adjust its position and tilt, plus a seventh that changes its radius of curvature, moving in steps of roughly ten nanometres (@fig:jwstactuator). Commissioning in February–April 2022 followed a sequence of **wavefront sensing and control (WFSC)**:

1. **Segment identification and image stacking** — each segment initially formed its own image of a bright star (18 dots); the segments were tilted one by one until all 18 images overlapped.
2. **Coarse phasing** — a dispersed-fringe sensor in NIRCam measured piston (height) differences between segments to a few micrometres, then less than a micrometre.
3. **Fine phasing** — NIRCam took deliberately defocused images through weak lenses, and **phase-retrieval** software computed the wavefront error across the whole pupil, which was then corrected with the actuators.

The result was better than required: the total wavefront error at NIRCam is typically 60–80 nm rms, against a prediction of under 100 nm, and the segments drift by less than 10 nm between measurements made every two days. Small corrections every month or two keep the image quality stable. One surprise was a micrometeoroid that struck segment C3 in May 2022, larger than the pre-launch models predicted; the segment's error rose from about 56 to more than 250 nm, was partly corrected to 178 nm by readjusting the segment, and adds about 9 nm rms to the telescope's total. JWST now limits the time it spends looking along its direction of orbital motion, where impacts are more energetic.

![A JWST engineering-model mirror segment with its gold coating. The actuators that position the segment and adjust its curvature are mounted behind it.](figures/photos/ch38_actuator.jpg){#fig:jwstactuator width=56%}

### Grazing Incidence, Coded Masks and Pair Telescopes

X-rays penetrate a normal mirror instead of reflecting. They reflect only at **grazing incidence** — at angles of less than about 1° to the surface — and the critical angle shrinks as photon energy rises. A **Wolter type I** telescope therefore uses a paraboloid followed by a hyperboloid, each a narrow ring, and nests several pairs inside one another to increase the collecting area (@fig:xgammaoptics). Chandra has four nested pairs of iridium-coated Zerodur shells, the largest 1.23 m across, with a 10 m focal length (@fig:chandrahrma); its 1 484 kg mirror assembly gives a resolution better than 0.5″, still the sharpest X-ray image ever made. XMM-Newton trades sharpness for area with three modules of 58 thin, gold-coated nickel shells each; NuSTAR reaches 79 keV with 133 shells per optic coated with **multilayers** — alternating thin layers of heavy and light materials that reflect like a crystal — at the end of a 10 m deployable mast.

Above about 100 keV even grazing optics fail. **Coded-aperture** cameras such as Swift's Burst Alert Telescope (BAT) place a mask of about 52 000 lead tiles one metre above a detector of 32 768 cadmium zinc telluride (CZT) crystals; each source casts a shifted shadow of the mask, and software decodes the overlapping shadows to locate gamma-ray bursts within minutes anywhere in a sixth of the sky. At energies above about 20 MeV, gamma rays are detected individually: in a **pair-conversion telescope** such as Fermi's Large Area Telescope (LAT), a photon converts into an electron–positron pair in a thin tungsten foil, silicon strip detectors track the pair, and a caesium iodide calorimeter measures its energy.

![Optics for high-energy astronomy: (a) nested Wolter-I grazing-incidence mirrors focus X-rays after two reflections; (b) a coded mask casts a shadow pattern that encodes the direction of each source; (c) a pair-conversion telescope tracks the electron and positron created by a gamma ray.](figures/out/ch38_highenergy.svg){#fig:xgammaoptics width=98%}

![The nested mirror shells of Chandra's High Resolution Mirror Assembly being assembled at Eastman Kodak in Rochester, New York.](figures/photos/ch38_hrma.jpg){#fig:chandrahrma width=56%}

### Blocking the Star: Coronagraphs and Starshades

An Earth-like planet seen in reflected light is extremely faint compared with its star. With a geometric albedo of 0.2, its brightness relative to the star is $A_g (R_p/a)^2$ ≈ 3.6 × 10⁻¹⁰ at full phase and about 1.2 × 10⁻¹⁰ when half-lit, and at 10 parsecs it lies only 0.1″ from its star — about six times $\lambda/D$ for a 6 m telescope in visible light. Seeing it requires suppressing the starlight by ten billion times close to the diffraction limit.

A **coronagraph** blocks the star's image with a small mask in the focal plane, then removes the diffracted light with a **Lyot stop** in a re-imaged pupil. JWST's NIRCam and MIRI carry coronagraphs that reach contrasts of about 10⁻⁴–10⁻⁵ — enough for young, self-luminous giant planets in the infrared. Roman's Coronagraph Instrument is the first in space with two **deformable mirrors** to correct wavefront errors actively, and aims to show contrasts of 10⁻⁷ or better. Reaching 10⁻¹⁰ requires a telescope whose wavefront is stable to picometres over hours, roughly ten times more stable than Roman, together with a coronagraph about a hundred times deeper — the central technology challenge for HWO, which NASA's project office aims to bring to maturity before a mission concept review around 2029–30.

The alternative is a **starshade**: a flower-shaped screen tens of metres across, flying tens of thousands of kilometres in front of the telescope, whose petal shape diffracts the starlight away from the telescope while the planet's light passes by (@fig:starshadetest). Laboratory starshade masks have reached 10⁻¹⁰ contrast, but a starshade must fly to a new position for every target star, using days to weeks of travel and propellant. NASA closed out its starshade technology activity in April 2025 and HWO's baseline is a coronagraph.

![A half-scale starshade with four petals deployed at NASA's Jet Propulsion Laboratory in 2014. The precise petal edges diffract starlight away from the telescope's line of sight.](figures/photos/ch38_starshade.jpg){#fig:starshadetest width=58%}

## Detectors

### From Photons to Electrons

A detector converts photons into electrical charge and counts it. Its key properties are **quantum efficiency (QE)** — the fraction of photons that produce a detected electron — **read noise**, **dark current** (charge generated thermally even in darkness), format and radiation tolerance. @tbl:astrodetectors summarises the main types.

| Detector | Range | Operating temperature | Typical format | Examples |
|---|---|---|---|---|
| Silicon CCD | 0.2–1.0 µm | 150–190 K | 2k × 4k, 4k × 4k | Hubble ACS and WFC3, Gaia (106 CCDs), Euclid VIS (36 CCDs) |
| Silicon CMOS | 0.3–1.0 µm | 200–300 K | Up to 4k × 4k | Star trackers, small telescopes, guide cameras |
| HgCdTe (H2RG, H4RG) | 0.6–5.3 µm | 35–100 K | 2k × 2k (18 µm); 4k × 4k (10 µm) | JWST NIRCam, NIRSpec; Euclid NISP; Roman WFI |
| Si:As impurity band | 5–28 µm | < 7 K | 1k × 1k | JWST MIRI, Spitzer, WISE |
| Bolometers | 60 µm–3 mm | 0.1–0.3 K | Hundreds to thousands of pixels | Herschel SPIRE, Planck HFI |
| X-ray CCD | 0.2–12 keV | ≈ 150 K | 1k × 1k | Chandra ACIS, XMM-Newton EPIC |
| Microcalorimeter | 0.3–12 keV | 0.05 K | 6 × 6 | XRISM Resolve |
| CZT | 3–150 keV | ≈ 290 K | Thousands of crystals | Swift BAT, NuSTAR |

: Detectors used in space astronomy. {#tbl:astrodetectors}

**Charge-coupled devices (CCDs)** store photoelectrons in potential wells and shift them, pixel by pixel, to a single low-noise amplifier. They reach QE above 90 % with thinned, back-illuminated sensors and read noise of 2–4 electrons. Their weakness in space is **radiation damage**: protons create traps that capture charge as it is shifted, smearing images along the readout direction. Hubble's CCDs lose charge-transfer efficiency every year, and the pipeline now corrects each pixel with a model of the traps. **CMOS** sensors put an amplifier in every pixel, read out faster, need less power and tolerate radiation better, and are replacing CCDs in many new instruments.

Infrared photons have too little energy to free electrons in silicon. **Mercury cadmium telluride (HgCdTe)**, whose band gap is tuned by its mercury-to-cadmium ratio, is bonded pixel by pixel with indium bumps to a silicon readout circuit. Teledyne's **H2RG** (2048 × 2048 pixels of 18 µm) is used throughout JWST's near-infrared instruments and Euclid's NISP; Roman's Wide Field Instrument uses 18 **H4RG-10** arrays (4096 × 4096 pixels of 10 µm) for about 300 million pixels (@fig:nircamfpa). These arrays are read non-destructively: the charge in each pixel is sampled many times "up the ramp" during an exposure, which averages down read noise and lets the software find and remove cosmic-ray hits as sudden jumps. Beyond 5 µm, JWST's MIRI uses arsenic-doped silicon (Si:As) **blocked-impurity-band** detectors, which must be colder than 7 K.

![A replacement focal-plane assembly for JWST's Near Infrared Camera being aligned under a three-dimensional microscope at NASA Goddard. Each assembly holds HgCdTe detector arrays on a precisely flat mount.](figures/photos/ch38_fpa.jpg){#fig:nircamfpa width=58%}

### Beyond Photon Counting: Bolometers and Microcalorimeters

At far-infrared and millimetre wavelengths, detectors measure the **heat** deposited by radiation. A **bolometer** is a tiny absorber on a weak thermal link to a cold bath; a sensitive thermometer — a doped semiconductor, or a **transition-edge sensor (TES)** held on the edge of its superconducting transition — measures its warming. Planck's High Frequency Instrument cooled its "spider-web" bolometers to 0.1 K and mapped the cosmic microwave background to a few millionths of a kelvin. **Kinetic inductance detectors (KIDs)**, superconducting resonators whose frequency shifts when photons break Cooper pairs, can be read by the thousand on a single wire and are being developed for future far-infrared missions.

An X-ray **microcalorimeter** applies the same idea to single photons. XRISM's Resolve instrument, launched in 2023, has a 6 × 6 array of absorbers at 50 mK, cooled by adiabatic demagnetisation refrigerators; each X-ray photon warms its pixel by a few millikelvin, and the pulse height gives its energy to about 4.5 eV at 6 keV — about 30 times better than an X-ray CCD — resolving the motions of hot gas in galaxy clusters. Its protective gate valve has failed to open, limiting it to energies above about 1.7 keV. Hard X-rays and gamma rays are detected in thick, dense semiconductors such as **CZT**, which work at room temperature, or in scintillating crystals read by photomultipliers or photodiodes.

### Noise and the Photon Budget

Whether a source is detectable depends on how many photons arrive compared with the noise. The **signal-to-noise ratio (SNR)** of a point source measured in an aperture of $n_{pix}$ pixels is

$$\text{SNR} = \frac{S}{\sqrt{S + n_{pix}\,(B + D\,t + n_{read}\,\sigma_{read}^2)}}$$

where $S$ is the number of source electrons, $B$ the sky electrons per pixel, $D$ the dark current, $t$ the exposure time and $\sigma_{read}$ the read noise for each of $n_{read}$ readouts. Faint sources are **background-limited**: SNR grows only as $\sqrt{t}$, so a tenfold longer exposure gains a factor of 3.2 in SNR, or 1.25 magnitudes. A larger telescope helps twice — it collects more light, and its smaller diffraction image includes less sky. @fig:snrmag shows the result for three apertures; in one hour, a 2.4 m telescope reaches SNR = 10 at V ≈ 27.2 and a 6.5 m telescope at V ≈ 29.3.

![Signal-to-noise ratio versus magnitude for 0.3 m, 2.4 m and 6.5 m diffraction-limited space telescopes observing in the visible for 1 hour (solid) and 10 hours (dashed). The dot marks the worked example.](figures/out/ch38_snr.svg){#fig:snrmag width=90%}

::: example
**Example: how many photons from a 25th-magnitude star?**

A V = 25 star is observed for one hour with a Hubble-sized telescope (2.4 m aperture, 33 % central obstruction) through a V filter (550 nm, 88 nm wide) with 30 % overall throughput.

1. A V = 0 star delivers 3.63 × 10⁻¹¹ W m⁻² nm⁻¹. Each 550 nm photon carries $hc/\lambda$ = 3.61 × 10⁻¹⁹ J, so the photon flux is 1.0 × 10⁸ photons s⁻¹ m⁻² nm⁻¹.
2. V = 25 is 10⁻¹⁰ times fainter: 1.0 × 10⁻² photons s⁻¹ m⁻² nm⁻¹, or 0.88 photons s⁻¹ m⁻² in the 88 nm band.
3. Collecting area: $(\pi/4) × 2.4^2 × (1 - 0.33^2)$ = 4.03 m², giving 3.6 photons/s; with 30 % throughput, 1.07 electrons/s, or 3 850 electrons per hour, of which 80 % (3 080) fall in the measuring aperture.
4. Noise: the zodiacal sky (22.7 mag/arcsec²) adds 335 electrons in the 0.010 arcsec² aperture, dark current 337 and read noise 673 (19 pixels, four readouts of 3 electrons). Total noise = √(3 080 + 335 + 337 + 673) = 66.5 electrons.
5. SNR = 3 080 / 66.5 ≈ **46**. A single star of magnitude 25 — about 100 million times fainter than the faintest star visible to the naked eye — delivers roughly one photon per second to Hubble.
:::

## Keeping Cold and Clean

### Passive Cooling and Sunshields

The simplest way to cool a telescope is to let it radiate to deep space (about 3 K) while shading it from the Sun, Earth and Moon. A surface that sees only cold space settles at a temperature where the heat it radiates, $\varepsilon \sigma T^4$, equals the heat leaking in from warmer parts. Because radiation falls with the fourth power of temperature, a 40 K surface can reject only 0.15 W per square metre even with perfect emissivity, so every milliwatt leaking from the warm spacecraft must be intercepted.

JWST's **sunshield** is the extreme example (@fig:jwstsunshield). Five membranes of Kapton E, the first 50 µm thick and the rest 25 µm, coated with about 100 nm of aluminium and, on the two Sun-facing layers, doped silicon to reflect sunlight, spread about 21 m by 14 m. More than 200 kW of sunlight falls on the first layer, which reaches up to about 383 K (110 °C) in NASA's thermal models; only about 23 mW reaches the telescope side, where the last layer is near 36–40 K. The layers never touch, and they are **flared** — closer at the centre and wider apart at the edges — so that heat radiated into each gap escapes sideways to space rather than passing to the next layer (@fig:sunshieldmodel).

![JWST's full-size sunshield test unit stacked and unfurled in a cleanroom in 2014. The five membranes, each thinner than a human hair, are separated by gaps that let heat escape out of the edges.](figures/photos/ch38_sunshield.jpg){#fig:jwstsunshield width=64%}

![(a) The five flared sunshield layers between the Sun and the telescope. (b) Layer temperatures in two simple radiative models: a sealed stack, in which heat can only pass through the layers, and vented layers, in which each layer passes on about a tenth of the heat it receives.](figures/out/ch38_sunshield.svg){#fig:sunshieldmodel width=96%}

::: example
**Example: why the sunshield gaps must be open**

At L2 sunlight delivers $S$ = 1 361 / 1.01² = 1 334 W/m², so the 200 kW on JWST's first layer implies about 150 m² facing the Sun.

1. A flat plate absorbing all this sunlight and radiating from one face would reach $(S/\sigma)^{1/4}$ = 392 K — close to the first layer's 383 K maximum.
2. **Sealed stack.** If the five layers formed a closed sandwich with low-emissivity (ε = 0.05) faces, each of the four gaps would have a radiative resistance of $(2/\varepsilon - 1)$ = 39. With the first layer at 360 K and the last at 40 K, the heat flow is $q = \sigma (360^4 - 40^4) / (4 × 39)$ = 6.1 W/m², or about 900 W over 150 m².
3. A 40 K surface can radiate at most $\sigma T^4$ = 0.15 W/m². To reject 6.1 W/m², the cold layer would have to warm to at least 102 K even with perfect emissivity — useless for a mid-infrared telescope.
4. **Vented layers.** The real leak of 23 mW over 150 m² is 0.15 mW/m², about 40 000 times less. Almost all the heat leaves through the open edges of the gaps. Each vented layer passes on roughly a tenth of the heat it receives, so five layers give a temperature ratio of about $(10^{-4})^{1/4}$ ≈ 0.1 from first to last — 360 K to 36 K, as @fig:sunshieldmodel shows.
:::

### Cryocoolers and Cryogens

Passive cooling stops at about 30–40 K for a large telescope near Earth. Colder detectors need active cooling. Early infrared missions carried **cryostats** of liquid or superfluid helium, which evaporated over the mission: Spitzer's helium lasted from 2003 to May 2009, after which it continued in a "warm" mission at about 30 K using its two shortest-wavelength channels; Herschel's 2 300 litres of superfluid helium ran out in April 2013, ending its science; WISE used solid hydrogen. Spitzer pioneered the **warm launch**: only the instruments were inside the cryostat, and the telescope cooled in space by radiating from its black outer shell, so the tank could be much smaller.

Mechanical **cryocoolers** avoid running out. JWST's MIRI detectors must stay below 7 K (nominally about 6.2 K), and passive cooling reaches only about 40 K. Its cooler (@fig:miricooler) uses a three-stage **pulse-tube** precooler, driven by a compressor in the warm spacecraft bus, to cool helium gas to about 14 K, where it provides about a quarter of a watt of cooling; the helium then flows through about 10 m of thin tubing to a **Joule–Thomson** stage beside MIRI, where expansion through an orifice less than 1 mm wide cools it to about 6 K. The only moving parts are two horizontally opposed piston pairs, balanced so that they do not shake the telescope. Planck's 0.1 K stage used a dilution refrigerator, and XRISM's 50 mK stage uses magnetic refrigeration backed by a helium tank and coolers.

![The flight cryocooler for JWST's Mid-Infrared Instrument after testing at JPL in 2016. It cools MIRI's detectors to below 7 K, about 30 K colder than the rest of the telescope.](figures/photos/ch38_cryocooler.jpg){#fig:miricooler width=58%}

### Stray Light and Contamination

Light that reaches the detector by any path other than the intended one is **stray light**: sunlight or earthshine scattered off baffles and struts, light from bright stars outside the field, or thermal glow from warm structures. Designers trace millions of rays through a computer model of the telescope (Chapter 12) and then add **baffles**, black coatings and **field stops**. Each mirror surface must also be extremely smooth: microroughness of a few nanometres scatters light into a broad halo that hides faint objects near bright ones.

**Contamination** is the other enemy. Organic molecules **outgassing** from adhesives, cables and insulation condense on cold optics; a film a few nanometres thick can absorb much of the far-ultraviolet light, which is why Hubble's UV instruments degrade slowly. Space materials are screened for outgassing (typically less than 1 % total mass loss and 0.1 % collected condensable material in vacuum), hardware is baked in vacuum, and assembly takes place in cleanrooms with dry-nitrogen purges. Water is the hardest contaminant to eliminate. After launch in July 2023, **Euclid**'s throughput fell steadily as water ice, released by insulation that had absorbed moisture on the ground, condensed on its cold mirrors. ESA heated the fold and tertiary mirrors to 160 K in March 2024 and the fold mirror again in June 2024, recovering about 15 % of the lost light; throughput has been stable since (@fig:euclidlaunch).

![ESA's Euclid in the cleanroom being secured to the adapter of its Falcon 9 launcher in June 2023. The white cylinder houses the 1.2 m silicon-carbide telescope; the black solar panels also shade it from the Sun.](figures/photos/ch38_euclid.jpg){#fig:euclidlaunch width=60%}

## Pointing and Stability

### Sensing and Control

A telescope must point at its target, then hold it still for the whole exposure. Coarse pointing uses **sun sensors**, **star trackers** and **gyroscopes**, as on any spacecraft (Chapter 6). The final step is a **fine guidance sensor (FGS)** that measures the position of a guide star in the telescope's own focal plane, so that flexing of the structure between a separate star tracker and the science instrument does not matter. Hubble's three FGS are interferometers that sense a guide star's position to a few milliarcseconds; its pointing control holds a target to about 7 mas rms over 24 hours, using four **reaction wheels** as actuators. JWST's FGS images guide stars at 16 frames per second and steers a **fine steering mirror** to remove residual motion; in orbit its pointing jitter is about 1 mas per axis, several times better than required.

Pointing error blurs the image and lowers its peak brightness, as @fig:jitterblur shows. A useful rule is that jitter should be less than about a tenth of $\lambda/D$: for Hubble at 0.5 µm that is 4–5 mas, and for a future 6 m ultraviolet–optical telescope, about 2 mas. Coronagraphy is far stricter, because pointing drift moves the star's light off the mask: HWO studies call for sub-milliarcsecond pointing combined with picometre wavefront stability.

![Effect of line-of-sight jitter on (a) image width and (b) peak brightness for three telescopes. Hubble's 7 mas requirement and JWST's measured jitter of about 1 mas are marked.](figures/out/ch38_jitter.svg){#fig:jitterblur width=96%}

### Disturbances and Isolation

The main sources of jitter are inside the spacecraft. **Reaction wheels** spinning at thousands of revolutions per minute have tiny imbalances that shake the structure at the wheel speed and its harmonics; **cryocooler compressors**, **thermal snaps** as structures change temperature, and **solar-array flexing** add more. Hubble's original solar arrays vibrated each time the telescope passed from shadow into sunlight — 16 times a day — until stiffer arrays were installed in 1993 and 2002. Engineers attack jitter in four ways: balancing and choosing wheel speeds that avoid structural resonances; **isolating** the wheels on soft mounts or isolating the whole telescope from the spacecraft bus (JWST has a passive isolator in its deployable tower); stiffening and damping the structure; and closing a fast optical loop with a fine steering mirror. Microvibration is analysed with detailed structural models and measured on the ground with wheels running (Chapter 12).

### Hubble's Gyroscopes

Hubble's gyroscopes measure rotation by sensing the precession of a spinning wheel floating in fluid, connected by thin wires called **flex leads**. These leads corrode, and 8 of the 22 gyros flown on Hubble have failed. Hubble carries six and normally uses three. Servicing Mission 4 replaced all six in 2009 — the last time this could be done. After a gyro gave faulty readings and repeatedly put the telescope into safe mode in 2024, NASA switched Hubble to **one-gyro mode** in June 2024, keeping its second working gyro in reserve. Magnetometers, sun sensors and star trackers now fill the gaps in attitude knowledge during slews. The cost is about 12 % lower efficiency (85 to 74 orbits of observing a week), more time to acquire guide stars, a smaller part of the sky available at any time, and the inability to track moving targets closer than Mars; image quality is unchanged. NASA estimated a better than 70 % chance of keeping at least one gyro working through 2035, and by late 2025 Hubble's observing success rate had returned to more than 90 %.

### Scanning Telescopes

Not every telescope points and stares. **Gaia** spun once every six hours, sweeping two fields of view across the sky while its 106 CCDs moved charge across the chips in step with the star images — **time-delay integration**, the space-astronomy equivalent of a pushbroom scanner (Chapter 14). Repeated scans over 10.5 years measured nearly two billion stars' positions to tens of microarcseconds. **Survey telescopes** such as WISE and SPHEREx scan the whole sky systematically, and Planck spun at one revolution per minute to map the microwave background. Scanning simplifies the attitude control — a spinning spacecraft is naturally stable — but requires precise knowledge of the spin axis and a detector readout synchronised to the motion.

## Where to Put a Telescope

The orbit sets a telescope's thermal environment, the fraction of time it can observe, its data rate and whether it can be serviced (@fig:telescopeorbits and @tbl:orbittrades).

![Telescope orbits: (a) low Earth orbit (Hubble), Chandra's highly elliptical orbit and TESS's lunar-resonant orbit, to scale; (b) a halo orbit around Sun–Earth L2 (schematic); (c) the slow drift of an Earth-trailing telescope such as Kepler, shown in a frame rotating with the Earth.](figures/out/ch38_orbits.svg){#fig:telescopeorbits width=98%}

**Low Earth orbit** is cheap to reach and was the only orbit the Space Shuttle could service, which is why Hubble flies at about 470 km. But Earth blocks about half of the sky on each 95-minute orbit, the telescope passes through the **South Atlantic Anomaly**, where trapped protons swamp the detectors, and its thermal environment swings between sunlight and shadow 16 times a day. Hubble keeps its mirrors at about 21 °C with heaters for stability and spends only about half its time collecting science data. Swift, Fermi and NuSTAR also use LEO, where Earth's magnetic field shields them from cosmic rays.

**Highly elliptical orbits** give long uninterrupted views. Chandra's orbit, now about 12 650 × 136 200 km with a period of about 64 hours, keeps it above the radiation belts for most of each orbit, allowing exposures of more than a day. TESS uses a 2:1 resonance with the Moon, in a stable orbit reaching beyond the Moon's distance.

**Sun–Earth L2**, 1.5 million km beyond Earth on the anti-Sun side, has become the standard location for large infrared and survey telescopes: Herschel, Planck, Gaia, JWST, Euclid and now Roman. The Sun, Earth and Moon always lie in roughly the same direction, so a single sunshield can block all three, and the thermal environment is almost constant. L2 is unstable, so telescopes fly **halo orbits** around it with small station-keeping manoeuvres every few weeks; JWST's precise launch and efficient course corrections left it enough propellant for more than 20 years. **Earth-trailing** heliocentric orbits, used by Spitzer and Kepler, are even more stable and need no station-keeping, but the telescope drifts away from Earth — Kepler fell behind by about 7° a year — so its radio link weakens with time.

| Orbit | Examples | Thermal environment | Observing efficiency | Downlink | Servicing |
|---|---|---|---|---|---|
| LEO (400–600 km) | Hubble, Swift, Fermi, NuSTAR | Cycles every 95 min; Earth heat | ≈ 50 %; Earth blocks half the sky | Relay satellites or ground passes; Mbit/s | Possible (Shuttle; future vehicles) |
| Highly elliptical | Chandra, XMM-Newton, TESS | Variable; long stable arcs | High; exposures of days | Ground stations near apogee | No |
| Sun–Earth L2 halo | JWST, Euclid, Gaia, Roman | Constant; Sun, Earth, Moon on one side | Very high; large field of regard | Deep-space antennas; tens to hundreds of Mbit/s | Not designed for it |
| Earth-trailing | Spitzer, Kepler | Very stable and cold | Very high | Weakens as distance grows | No |

: Trade-offs between orbits for space telescopes. {#tbl:orbittrades}

## Building, Testing and Servicing

### Test as You Fly

A space telescope cannot be fixed after launch unless it was designed for servicing, so everything that can be tested on the ground is tested, at the temperatures and in the configuration it will fly. Optics are measured with **interferometers** and **null correctors**, now cross-checked by independent methods. Complete observatories are shaken on vibration tables, exposed to the acoustic roar of launch, and tested in **thermal-vacuum** chambers. JWST's telescope and instruments spent about 100 days in 2017 inside Chamber A at NASA's Johnson Space Center — a 37 m high vacuum chamber built for Apollo — cooled to cryogenic temperatures by liquid nitrogen and gaseous helium shrouds, while an optical system of reference sources checked that the 18 segments could be aligned at their operating temperature (@fig:chamberatest).

![JWST's telescope and science instruments inside Chamber A at NASA's Johnson Space Center in 2017, before cryogenic vacuum testing that simulated the cold of space.](figures/photos/ch38_chambera.jpg){#fig:chamberatest width=48%}

Ground tests cannot reproduce zero gravity, so gravity sag is predicted with finite-element models and verified by turning mirrors face-up and face-down. Deployments are rehearsed with the hardware supported by counterweights or air bearings. JWST's sunshield and mirror wings were deployed many times on the ground; in space, after launch on 25 December 2021, the full sequence of about 50 major deployments took two weeks and worked first time.

### Hubble Servicing Missions

Hubble was designed to be serviced. It has handholds, standard bolts, and **orbital replacement units** — instruments, batteries, gyroscopes, computers — that astronauts could exchange during spacewalks from the Space Shuttle (Chapter 33). Five servicing missions between 1993 and 2009 corrected its optics, replaced every instrument at least once and extended its life by decades (@tbl:hstservicing).

| Mission | Date | Shuttle | Main work |
|---|---|---|---|
| SM1 | Dec 1993 | Endeavour (STS-61) | COSTAR corrective optics; WFPC2 with built-in correction; new solar arrays and gyros |
| SM2 | Feb 1997 | Discovery (STS-82) | STIS spectrograph; NICMOS infrared camera; solid-state data recorder |
| SM3A | Dec 1999 | Discovery (STS-103) | All six gyros after Hubble entered safe mode; new main computer |
| SM3B | Mar 2002 | Columbia (STS-109) | Advanced Camera for Surveys; rigid solar arrays; NICMOS cryocooler; power control unit |
| SM4 | May 2009 | Atlantis (STS-125) | WFC3 and COS; repair of ACS and STIS; six gyros; batteries; soft-capture fixture |

: The five Hubble servicing missions. {#tbl:hstservicing}

The first mission was the most dramatic: astronauts installed COSTAR — a set of small deployable mirrors that refocused light for three instruments — and replaced the Wide Field/Planetary Camera with a new one whose internal optics compensated for the mirror error (@fig:sm1wfpc). Servicing turned Hubble into a 36-year observatory whose instruments are still among the most capable in the ultraviolet and visible. Without shuttle visits, its orbit is slowly decaying; NASA has considered, but not ordered, a commercial reboost, and without one Hubble is expected to re-enter in the 2030s.

![Astronaut Jeffrey Hoffman holds the original Wide Field/Planetary Camera in Endeavour's payload bay during the first Hubble servicing mission in December 1993, after replacing it with WFPC2.](figures/photos/ch38_wfpc.jpg){#fig:sm1wfpc width=42%}

### Assembling the Next Generation in Space

JWST shows how far a folded telescope can go: a 6.5 m aperture inside a 5 m fairing. Larger apertures — 10–20 m or more — may need to be assembled in orbit from segments launched separately, by robots or astronauts, and then aligned with the same wavefront sensing used on JWST. Studies of HWO have included design features such as standard interfaces and a location at L2 that a future servicing vehicle could reach, so that instruments could be upgraded as Hubble's were. Robotic servicing, refuelling and in-space assembly are covered in Chapter 40.

## From Photons to Archives

### Downlink and Onboard Storage

Data volume grows with detector size and observing efficiency, and the downlink must keep pace (@tbl:telescopedata). Hubble sends about 18 GB of science data a week through NASA's Tracking and Data Relay Satellites. JWST records data on a 68 GB solid-state recorder and sends up to about 57 GB a day to the Deep Space Network's 34 m antennas on a 25.9 GHz Ka-band link at up to 28 Mbit/s — about 4.5 hours of transmission. Euclid returns about 100 GB of compressed data a day in a four-hour pass, and Roman, with its 300-megapixel camera, will send about 1.4 TB a day at up to 500 Mbit/s to stations in New Mexico, Australia and Japan, more than all of Hubble's data in a year.

| Telescope | Launched | Aperture | Band | Orbit | Science data per day |
|---|---|---|---|---|---|
| Hubble | 1990 | 2.4 m | 0.115–2.5 µm | LEO, 470 km | ≈ 2.6 GB |
| Chandra | 1999 | 1.2 m (outer shell) | 0.1–10 keV | 12 650 × 136 200 km | Small (photon lists) |
| JWST | 2021 | 6.5 m | 0.6–28.5 µm | L2 halo | ≈ 57 GB (28 Mbit/s Ka-band) |
| Euclid | 2023 | 1.2 m | 0.55–2.0 µm | L2 halo | ≈ 100 GB (≈ 75 Mbit/s K-band) |
| Roman | 2026 | 2.4 m | 0.48–2.3 µm | L2 halo | ≈ 1.4 TB (up to 500 Mbit/s Ka-band) |

: Comparison of five major space telescopes and their data rates. {#tbl:telescopedata}

### Pipelines and Archives

Raw telescope data are useless without calibration. Each observatory runs a **pipeline** that turns detector readouts into science products: for JWST, stage 1 fits the slope of each pixel's ramp and removes cosmic rays, stage 2 applies flat fields, flux calibration and world coordinates, and stage 3 combines dithered exposures into mosaics, spectra or catalogues. The software is open source, and data are reprocessed as calibrations improve, so the archive always offers the best current version.

The **Mikulski Archive for Space Telescopes (MAST)** at the Space Telescope Science Institute holds data from about 20 NASA missions, including Hubble, JWST, TESS and soon Roman; it already exceeded 3 petabytes in 2017 and has grown rapidly since, with copies in commercial clouds so that researchers can analyse data where they are stored. ESA runs equivalent archives for Gaia, Euclid and XMM-Newton. Most observations become public after a proprietary period of up to a year, and a large share of published papers now use archival data rather than new observations. In effect the archive, not the telescope, is the observatory's final product.

::: ai
**AI in space telescope operations**

Machine learning now appears throughout a space telescope's life (Chapter 46). Neural networks trained on simulated defocused images can estimate wavefront errors directly from star images — a fast complement to iterative phase retrieval for segmented mirrors such as JWST's and for the ultra-stable control future coronagraphs will need. Scheduling has used artificial intelligence since Hubble's SPIKE planner, developed at STScI in the late 1980s with constraint-based search, and modern schedulers optimise thousands of observations against pointing, thermal and data-volume constraints. In data reduction, deep-learning models flag cosmic-ray hits and detector artefacts, classify galaxy shapes and find rare objects in surveys of billions of sources — Euclid's first quick data release combined neural networks with citizen scientists to search for strong gravitational lenses. The challenge is trust: every automated decision must be validated against physics and reproducible in the archive (Chapter 47).
:::

::: key
**Key takeaways**

- The atmosphere absorbs gamma rays, X-rays, ultraviolet and most infrared light, blurs images through seeing and glows in the infrared; space gives access to the whole spectrum, diffraction-limited images and a dark, stable sky.
- Resolution is set by 1.22 λ/D and sensitivity by collecting area and background; JWST's 6.5 m mirror resolves 77 mas at 2 µm, and a 2.4 m telescope detects V = 27 in an hour at SNR = 10.
- Large apertures use lightweighted glass, beryllium or silicon carbide, and segmented, deployable mirrors aligned in orbit by wavefront sensing to tens of nanometres; X-ray telescopes need nested grazing-incidence mirrors and gamma rays coded masks or pair-conversion trackers.
- Infrared telescopes must be cold: JWST's five-layer, edge-vented sunshield cuts 200 kW of sunlight to about 23 mW, and a cryocooler takes MIRI below 7 K.
- Fine guidance sensors, quiet reaction wheels, isolation and fast steering mirrors hold pointing to milliarcseconds; Hubble has operated on one gyroscope since 2024.
- Sun–Earth L2 offers a cold, stable environment for large telescopes at the cost of servicing; Hubble's five servicing missions showed the value of designing for repair and upgrade.
- Data rates have grown from gigabytes per week (Hubble) to terabytes per day (Roman), making pipelines and public archives as important as the telescopes themselves.
:::

::: questions
**Review questions**

1. Explain why X-ray and far-infrared astronomy must be done from above the atmosphere, but visible astronomy can be done from the ground. What does a space telescope gain in the visible?
2. Calculate the diffraction limit of a 1.2 m telescope at 0.8 µm and at 2 µm, in milliarcseconds. What pixel size would Nyquist-sample each?
3. Using @fig:coldtelescope, explain why JWST's MIRI is limited by the telescope's own emission at its longest wavelengths. What would be gained by cooling the telescope to 10 K?
4. Compare beryllium, ULE glass and silicon carbide as mirror materials for (a) a room-temperature ultraviolet telescope and (b) a 40 K infrared telescope.
5. Describe the three main steps used to align JWST's 18 mirror segments in orbit. Why could the alignment not be completed on the ground?
6. Why do X-ray telescopes use grazing incidence, and why are several mirror shells nested inside one another?
7. A 6 m telescope observes an Earth twin at 15 pc in visible light (0.5 µm). How many multiples of λ/D separate planet and star, and what contrast must the coronagraph reach?
8. Repeat the worked photon-budget example for a 6.5 m telescope (same throughput and obstruction). By what factor does the SNR improve, and why is it more than the ratio of collecting areas' square root?
9. Explain why the gaps between JWST's sunshield layers are open at the edges, using the sealed-stack calculation in the worked example.
10. List the advantages and disadvantages of LEO, a highly elliptical orbit and Sun–Earth L2 for a new ultraviolet–optical telescope that should be serviceable.
:::
