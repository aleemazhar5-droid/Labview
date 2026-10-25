---
title: Great Observatories and Deep-Space Telescopes
hero: ch39
abstract: Most of the light in the Universe never reaches the ground. Space telescopes recover the gamma rays, X-rays, ultraviolet and infrared that the atmosphere absorbs, see sharper than turbulent air allows and measure brightness steadily enough to find Earth-sized planets. This chapter tells the story of NASA's four Great Observatories — Hubble, Compton, Chandra and Spitzer — and of the James Webb Space Telescope, which by 2026 had seen galaxies 280 million years after the Big Bang and analysed the air of distant worlds. It explains redshift, look-back time and the several meanings of cosmic distance, reviews the survey, exoplanet, high-energy and cosmic-microwave missions, and describes the fleet operating in October 2026 and the observatories planned for the 2030s and 2040s.
---

An astronomer on the ground looks out through a thick, warm, moving filter. Earth's atmosphere absorbs all gamma rays and X-rays, almost all ultraviolet light and most of the infrared; water vapour glows brightly in the infrared; and turbulence smears every star into a shimmering blob about one arcsecond (1″, 1/3 600 of a degree) across. A telescope above the atmosphere escapes all three problems. It can observe at any wavelength, reach the sharpness set by diffraction, and measure a star's brightness to a few parts per million for weeks at a time.

This chapter covers the missions, capabilities and results of space observatories, from NASA's **Great Observatories** to the fleet of October 2026; how they are engineered — mirrors, detectors, cryogenics and pointing — is the subject of Chapter 38.

## Why Observe from Space

### The Atmospheric Filter

@fig:obsspectrum shows which parts of the electromagnetic spectrum reach the ground. Only two broad **windows** are open: the optical window from about 0.3 to 1 µm, with partial windows in the near-infrared, and the radio window from about 1 cm to 15 m. Gamma rays and X-rays are absorbed high in the atmosphere, ultraviolet by ozone and infrared by water vapour and carbon dioxide; the ionosphere reflects long radio waves. Balloons and sounding rockets (Chapters 8 and 9) sample some bands briefly; only satellites observe for years.

![Wavelength coverage of the main space observatories, past, present and planned. The strip at the top shows schematically where Earth's atmosphere is opaque, partly transparent or clear: gamma-ray, X-ray, ultraviolet and far-infrared astronomy is possible only from space.](figures/out/ch39_emcoverage.svg){#fig:obsspectrum width=86%}

### Sharpness, Darkness and Stability

Even in the open windows, space wins three ways.

- **Resolution.** A perfect telescope of diameter $D$ observing at wavelength $\lambda$ cannot separate points closer than about $\theta = 1.22\,\lambda/D$ radians, the **diffraction limit**. For Hubble's 2.4 m mirror at 0.5 µm this is 0.05″, twenty times sharper than typical ground-based seeing. Adaptive optics now correct turbulence on large ground telescopes in the near-infrared, but only over small fields.
- **Background.** Airglow in the upper atmosphere makes the night sky glow, and in the infrared the atmosphere and the telescope itself shine like a warm oven. A telescope cooled to 40 K in deep space has an infrared background many orders of magnitude lower, which is why JWST, with a third of the collecting area of the largest ground telescopes, is far more sensitive than any of them beyond about 2 µm.
- **Stability.** Starlight twinkles (scintillation). Above the atmosphere a star's brightness can be measured continuously to tens of parts per million, the precision needed to see an Earth-sized planet cross a Sun-like star.

The price is high. A space telescope must fit inside a fairing about 5 m across, survive launch and work without adjustment by hand, and it can rarely be repaired; its cost per square metre of collecting area is hundreds of times that of a ground telescope. The two approaches are complementary: giant ground telescopes such as the 39 m Extremely Large Telescope under construction in Chile collect more light, while space telescopes provide wavelengths, sharpness and stability that the ground cannot.

### Where Space Telescopes Fly

The orbit trades access, thermal environment and observing efficiency (@fig:obsorbits). **Low Earth orbit (LEO)**, used by Hubble, Fermi, NuSTAR and IXPE, is cheap to reach and shielded by Earth's magnetic field, but Earth hides most targets for part of every 95-minute orbit and warms the spacecraft. X-ray telescopes such as Chandra use **highly elliptical orbits** (HEO) reaching a third of the way to the Moon, above the radiation belts for most of the time. The cold, quiet observatories — WMAP, Planck, Herschel, Gaia, JWST, Euclid and Roman — use **halo or Lissajous orbits around the Sun–Earth L2 point**, 1.5 million km beyond Earth (Chapter 3), where the Sun, Earth and Moon always lie on one side and one sunshield can block all three. Kepler and Spitzer used **Earth-trailing solar orbits**, drifting slowly away; when they were switched off they were 170 and 266 million km from Earth.

![Where astronomical observatories fly, from the low orbits of Hubble and the X-ray and gamma-ray missions to the Sun–Earth L2 point and Earth-trailing solar orbits.](figures/out/ch39_orbits.svg){#fig:obsorbits width=82%}

## NASA's Great Observatories

In the 1980s NASA planned four large observatories, each covering a different part of the spectrum: the **Hubble Space Telescope** (visible and ultraviolet), the **Compton Gamma Ray Observatory**, the **Chandra X-ray Observatory** and the **Spitzer Space Telescope** (infrared). Three were launched by the Space Shuttle. The four never flew all at once — Compton came down three years before Spitzer was launched — but two remain in service in 2026 (@tbl:greatobs).

| Observatory | Band | Telescope | Launch | Orbit | End | Signature results |
|---|---|---|---|---|---|---|
| Hubble | 0.115–1.7 µm | 2.4 m mirror | 24 Apr 1990, STS-31 | LEO, 28.5° | Operating | Deep fields; expansion rate; dark energy |
| Compton (CGRO) | 20 keV–30 GeV | 4 instruments, 17 t | 5 Apr 1991, STS-37 | LEO, 28.5° | Deorbited 4 Jun 2000 | Gamma-ray bursts are cosmic; blazars |
| Chandra | 0.1–10 keV | 1.2 m nested mirrors, 0.5″ | 23 Jul 1999, STS-93 | ≈ 64-hour HEO | Operating | Dark matter in Bullet Cluster; black holes |
| Spitzer | 3.6–160 µm | 0.85 m, helium-cooled | 25 Aug 2003, Delta II | Earth-trailing | 30 Jan 2020 | TRAPPIST-1 planets; first exoplanet light |

: NASA's four Great Observatories. {#tbl:greatobs}

### Hubble Space Telescope

Hubble is a 2.4 m Ritchey–Chrétien reflector (Chapter 12) with a mass of about 11 t. Space Shuttle Discovery released it on 25 April 1990 at an altitude of about 615 km (@fig:obssts31). Within weeks it was clear that the images were blurred: the primary mirror had been polished very precisely to the wrong shape. A 1.3 mm spacing error in the optical test device used during polishing (the null corrector) had made the mirror about 2.2 µm too flat at its edge, causing **spherical aberration** — light from the edge and the centre of the mirror came to focus at different points.

![Hubble held by Discovery's robotic arm on 25 April 1990, during deployment on mission STS-31, with one solar array unrolled and the second still stowed.](figures/photos/ch39_sts31.jpg){#fig:obssts31 width=56%}

Because the error was known exactly, it could be corrected exactly, like prescribing spectacles. The first servicing mission (STS-61, December 1993) installed a new camera with the correction built in and **COSTAR**, small corrective mirrors on deployable arms that fed the other instruments. Astronauts visited Hubble five times between 1993 and 2009, replacing gyroscopes, batteries, solar arrays and every original instrument (Chapters 33 and 40); the last visit installed Wide Field Camera 3 and the Cosmic Origins Spectrograph, which still work alongside two older instruments.

Hubble measured the expansion rate of the Universe, the **Hubble constant**, to about 10 % (72 ± 8 km/s per megaparsec) in 2001, and its observations of distant supernovae helped show in 1998 that the expansion is accelerating — the evidence for **dark energy**. Its **Deep Fields** (1995, 2004), long exposures of apparently empty sky, revealed thousands of galaxies and traced how they grew. It found that almost every large galaxy has a central supermassive black hole and made the first detection of an exoplanet's atmosphere (2001). Its images, such as the "Pillars of Creation" (@fig:obspillars), are among the best-known scientific pictures ever made.

**Hubble in 2026.** On 19 September 2026 Hubble completed its 200 000th orbit, after more than 1.7 million observations. Of the six gyroscopes installed in 2009, two still work, and since June 2024 Hubble has used only one, keeping the other as a spare. This **one-gyro mode** halves the sky it can reach at any moment and initially cut observations by about a tenth, but STScI reported no safe-mode events in the two years that followed. Drag is slowly lowering the orbit, now about 470 km: the Space Telescope Science Institute (STScI) puts the chance of re-entry before 2032 below 10 %, with a median date in late 2033. NASA declined a privately funded Crew Dragon reboost in June 2024, citing risks to the telescope, but said in 2026 that it would consider a reboost if operating costs fell; STScI has meanwhile been told to plan for budgets about a fifth lower.

### Compton Gamma Ray Observatory

At about 17 t, the **Compton Gamma Ray Observatory** (CGRO) was the heaviest astronomical observatory flown up to that time (@fig:obsgro). Its four instruments covered photon energies from 20 keV to 30 GeV. The **Burst and Transient Source Experiment** (BATSE) recorded 2 704 **gamma-ray bursts** — brief, intense flashes of gamma rays — and showed that they come equally from all directions rather than concentrating along the Milky Way. Bursts must therefore occur at cosmological distances, which makes them the most powerful explosions known. The **EGRET** telescope showed that the high-energy sky is dominated by **blazars**, galaxies whose central black holes fire jets almost straight at us. After a gyroscope failed in 1999, NASA steered the observatory to a controlled re-entry over the Pacific on 4 June 2000.

### Chandra X-ray Observatory

X-rays penetrate a mirror at normal incidence and can be focused only by **grazing incidence**, glancing off a polished surface at about a degree, as a stone skips across water. Chandra's mirror is four nested pairs of nearly cylindrical iridium-coated shells, the largest 1.2 m across, with a 10 m focal length (Chapter 38); its 0.5″ resolution is still the sharpest of any X-ray telescope. Columbia deployed Chandra on 23 July 1999, on the first Shuttle mission commanded by a woman, Eileen Collins (@fig:obschandrabay); an Inertial Upper Stage then lifted it into an orbit that now ranges from 12 650 to 136 200 km above Earth, with a period of 63.5 hours. With its upper stage, Chandra was the heaviest payload ever launched by the Shuttle (22.8 t).

::: figrow
![The Compton Gamma Ray Observatory held by Atlantis's robotic arm during checkout on mission STS-37 in April 1991. The large cylinders are parts of the COMPTEL and EGRET telescopes.](figures/photos/ch39_gro.jpg){#fig:obsgro}

![Chandra, with its Inertial Upper Stage, in Columbia's payload bay shortly before being tilted up for release on 23 July 1999.](figures/photos/ch39_chandrabay.jpg){#fig:obschandrabay}
:::

Chandra sees the hot Universe: million-degree gas in galaxy clusters, the remnants of exploded stars and matter falling into black holes. In 2006 its map of hot gas in the colliding **Bullet Cluster**, compared with the mass mapped by gravitational lensing, showed most of the mass passing through the collision while the gas was slowed — direct evidence for **dark matter**. With JWST in 2023 it detected X-rays from **UHZ1**, a growing black hole seen less than 500 million years after the Big Bang. @fig:obscrab shows how Chandra combines with other observatories: each wavelength reveals a different part of the same object.

::: figrow
![The "Pillars of Creation" in the Eagle Nebula, re-imaged by Hubble in near-infrared light in 2014. Infrared light passes through much of the dust, revealing stars behind and inside the columns of cold gas.](figures/photos/ch39_pillars.jpg){#fig:obspillars width=80%}

![The Crab Nebula, the remnant of a supernova seen in 1054, combining radio (Very Large Array), infrared (Spitzer), visible (Hubble), ultraviolet (XMM-Newton) and X-ray (Chandra) data. The X-rays (purple) come from the most energetic particles near the central pulsar.](figures/photos/ch39_crab.jpg){#fig:obscrab width=80%}
:::

Chandra has also become a symbol of budget pressure. NASA's requests for 2025 and 2026 proposed winding it down to save about US$ 70 million a year; Congress refused, and the 2026 appropriation (signed in January 2026) gave astrophysics US$ 1.595 billion and Chandra at least US$ 63 million, enough for a "minimum-cost mission". The 2027 request would cut astrophysics by about 65 %, to US$ 552 million, ending Chandra and Fermi; a House committee rejected the cut, but no 2027 budget had been enacted in October 2026, and a stopgap continuing resolution held NASA at its 2026 level until 11 December.

### Spitzer Space Telescope

Spitzer pioneered a design that JWST later followed: it was **launched warm**. Earlier infrared telescopes such as IRAS (1983) and ISO (1995) sat inside large tanks of liquid helium; Spitzer kept only its instruments in a small cryostat, and its 0.85 m beryllium telescope cooled by radiating to space, helped by vented helium vapour, in an orbit far from the warm Earth (@fig:obsspitzer). The helium lasted until May 2009, after which Spitzer worked for ten more years in a "warm mission" using the two shortest-wavelength channels of its camera, which still functioned at the telescope's new temperature of roughly 30 K.

Spitzer made the first detections of light emitted by exoplanets (2005), found a huge, faint ring around Saturn, and in 2017 helped show that the cool dwarf star **TRAPPIST-1** has seven Earth-sized planets. As it drifted away its antenna had to point ever closer to the Sun to send data home, and NASA switched it off on 30 January 2020.

![Spitzer at Cape Canaveral being readied for launch in 2003. The telescope tube sits above the spacecraft bus, shaded by the solar panel on the right.](figures/photos/ch39_spitzer.jpg){#fig:obsspitzer width=26%}

## The James Webb Space Telescope

JWST was conceived in the 1990s as Hubble's infrared successor, because the ultraviolet and visible light of the first galaxies is stretched by cosmic expansion into the infrared. Built by NASA with the European and Canadian space agencies, it is the largest and most complex scientific spacecraft ever launched (@tbl:jwstspecs). It took about 25 years to develop and cost about US$ 10 billion, including the first five years of operations.

### Launch and Commissioning

JWST's mirror and sunshield were launched folded (@fig:obsjwstmirror). Its deployment involved about 344 **single-point failures** — items whose failure would have ended the mission. In the two weeks after launch the sunshield unfolded and tensioned and the mirror wings locked into place; JWST reached L2 on 24 January 2022, and engineers spent three months aligning the 18 segments to within tens of nanometres so that they act as one mirror. The accurate Ariane 5 launch left propellant for about 20 years instead of the 10 planned.

The first images were released on 12 July 2022. The first deep field (@fig:obsdeepfield), a 12.5-hour exposure of the galaxy cluster SMACS 0723, reached infrared depths beyond those of Hubble's deepest fields, which had taken weeks. Image quality and background beat requirements. One surprise was **micrometeoroid** damage: an impact in May 2022 slightly distorted one segment, and JWST now limits the time it points towards its direction of orbital motion, where impacts are most energetic.

::: figrow
![The last of JWST's 18 primary-mirror segments being lowered into place by a robotic arm at NASA's Goddard Space Flight Center in February 2016, completing the mirror.](figures/photos/ch39_jwstmirror.jpg){#fig:obsjwstmirror}

![JWST's first deep field (2022): the cluster SMACS 0723 acts as a gravitational lens, stretching background galaxies into arcs.](figures/photos/ch39_deepfield.jpg){#fig:obsdeepfield width=76%}
:::

| Parameter | Value |
|---|---|
| Primary mirror | 6.5 m; 18 hexagonal segments of gold-coated beryllium; 25.4 m² collecting area |
| Wavelength range | 0.6–28.5 µm (visible red to mid-infrared) |
| Instruments | NIRCam (camera), NIRSpec (spectrograph), MIRI (mid-infrared), NIRISS and Fine Guidance Sensor |
| Sunshield | Five Kapton layers, 21.2 × 14.2 m; Sun side above 350 K, cold side ≈ 40 K |
| Operating temperature | Telescope ≈ 40 K; MIRI 7 K (cryocooler) |
| Mass and orbit | About 6.2 t; halo orbit around Sun–Earth L2 |
| Launch | 25 December 2021, Ariane 5, Kourou |
| Lifetime | Propellant for about 20 years |

: The James Webb Space Telescope at a glance. {#tbl:jwstspecs}

### The First Galaxies

Cosmic expansion stretches light from a distant galaxy by a factor $(1+z)$, where $z$ is the **redshift**. Neutral hydrogen absorbs light bluer than the Lyman-α line at 121.6 nm, so a young galaxy vanishes abruptly below $121.6\,(1+z)$ nm. @fig:obsredshift shows that for $z > 13$ this **Lyman break** lies beyond 1.7 µm, the red limit of Hubble's cameras: Hubble cannot see such galaxies at all. Hubble's most distant galaxy, GN-z11 (2016), lies at $z$ = 10.6.

![Observed wavelength of four bright spectral lines as a function of redshift, compared with the ranges of Hubble and JWST's instruments. Above a redshift of about 13, even ultraviolet Lyman-α light arrives at wavelengths longer than Hubble can detect.](figures/out/ch39_redshiftlines.svg){#fig:obsredshift width=82%}

JWST has repeatedly broken the distance record, confirming each redshift with a spectrum. In 2024 the JADES survey confirmed **JADES-GS-z14-0** at $z$ ≈ 14.3 (refined to 14.18 by the ALMA radio telescope); in 2025 the MoM survey measured **MoM-z14** at $z$ = 14.44 (published in January 2026), seen just 280 million years after the Big Bang. As of October 2026 no galaxy had been spectroscopically confirmed at a greater distance. The surprise is less the distance than the brightness: JWST finds more luminous galaxies above $z$ = 10 than most models predicted, suggesting that early star formation was more efficient than assumed — an active research problem rather than a contradiction of standard cosmology.

JWST has also found black holes earlier and larger than expected: besides UHZ1, a feeding black hole in GN-z11 and many compact, very red **"little red dots"** that appear to hide black holes of millions of solar masses in dense gas, one of them (CAPERS-LRD-z9, reported in 2025) seen about 500 million years after the Big Bang. Whether such black holes began as collapsing giant gas clouds or grew unusually fast from the remnants of the first stars is one of JWST's central questions.

### Exoplanet Atmospheres

When a planet passes in front of its star, a little starlight filters through its atmosphere. Molecules absorb at characteristic wavelengths, so the planet appears slightly larger at those wavelengths: this **transmission spectrum** reveals the atmosphere's composition. In its first months JWST made the first clear detection of **carbon dioxide** in an exoplanet atmosphere, that of the hot Saturn WASP-39 b, and found sulphur dioxide made by starlight-driven chemistry. Heat measurements of the rocky planets TRAPPIST-1 b and c suggest little or no thick atmosphere.

**K2-18 b**, about two and a half times Earth's radius and in the habitable zone of a red dwarf, shows the limits of the method. JWST detected methane and carbon dioxide there in 2023, and in April 2025 a team reported evidence at about three standard deviations for dimethyl sulphide, a gas made on Earth mainly by marine life. Independent reanalyses found that different but reasonable choices of data reduction and atmospheric model remove the signal, and in October 2026 the claim remains unconfirmed. Features from small planets amount to tens of parts per million, close to instrumental limits, so a biosignature claim demands several independent lines of evidence.

### JWST in 2026

JWST attracts more demand than any observatory before it: for its fifth cycle, which began on 1 July 2026, astronomers submitted 2 930 proposals requesting about twelve times the time available. It has confirmed that Hubble's measurements of the variable stars calibrating the distance ladder were not biased by crowding, yet calibrations still give Hubble constants of about 70–73 km/s/Mpc, against 67–68 km/s/Mpc from the cosmic microwave background — the unexplained **Hubble tension**. Its budget is under pressure too: the 2027 request proposed reduced operating funds for JWST and Hubble.

## Reading the Distant Universe: Redshift, Time and Distance

Looking far away means looking back in time, but in an expanding Universe "how far" has several meanings. The standard model, **flat ΛCDM** (a Universe dominated today by dark energy, Λ, and cold dark matter), with Hubble constant $H_0$ = 67.7 km/s/Mpc and matter density $\Omega_m$ = 0.31, gives a present age of 13.79 billion years. The age of the Universe when light was emitted at redshift $z$ is

$$ t(z) = \int_z^\infty \frac{dz'}{(1+z')\,H(z')}, \qquad H(z) = H_0\sqrt{\Omega_m (1+z)^3 + \Omega_r (1+z)^4 + \Omega_\Lambda}, $$

where $\Omega_r \approx 9\times10^{-5}$ is the small contribution of radiation and $\Omega_\Lambda = 1 - \Omega_m - \Omega_r$. The **look-back time** is the present age minus $t(z)$ (@fig:obslookback, @tbl:cosmodist). Four distances are in common use:

- **Light-travel distance**: look-back time × speed of light — the figure press releases quote, though no ruler could measure it.
- **Comoving distance**: the distance to the object *today*, if the expansion could be frozen and a ruler laid out. It exceeds the light-travel distance because space expanded while the light was in transit; the edge of the observable Universe is about 46 billion light-years away.
- **Angular-diameter distance**: relates an object's true size to the angle it covers. It peaks near $z \approx 1.6$ and then *decreases*: very distant galaxies look larger than galaxies of the same size at intermediate distance, because we see them as they were when they were closer to us.
- **Luminosity distance**: relates an object's power to the flux received, as used with "standard candles" such as type Ia supernovae. It exceeds the comoving distance by a factor $(1+z)$, because photons lose energy and arrive less often.

![(a) Look-back time and age of the Universe when the light was emitted, as functions of redshift. (b) Four measures of distance. Light from MoM-z14 travelled for 13.5 billion years, but the galaxy is now about 34 billion light-years away.](figures/out/ch39_lookback.svg){#fig:obslookback width=98%}

::: example
**Example: look-back time to redshift 14**

A galaxy's spectrum shows the Lyman break at 1.824 µm. How long ago did its light leave, and how old was the Universe then?

1. **Redshift.** $1 + z = 1.824/0.1216 = 15.0$, so $z$ = 14.0. The break lies beyond Hubble's 1.7 µm limit; only JWST can measure it.
2. **Quick estimate.** At this redshift matter dominates, $H(z) \approx H_0\sqrt{\Omega_m}(1+z)^{3/2}$, and the integral gives $t \approx \tfrac{2}{3}\,(1/H_0)/[\sqrt{\Omega_m}(1+z)^{3/2}]$. With $1/H_0$ = 14.44 Gyr: $t \approx \tfrac{2}{3} \times 14.44/(0.557 \times 58.1)$ = **0.298 Gyr**.
3. **Exact integral.** Numerical integration including dark energy and radiation gives $t$ = **296 million years**, within 1 % of the estimate — dark energy was negligible then.
4. **Look-back time.** 13.79 − 0.30 = **13.50 billion years**: the light has travelled for 97.9 % of cosmic history.
:::

| Redshift $z$ | Example | Look-back time (Gyr) | Age then (Myr) | Comoving distance (Gly) | Angular-diameter distance (Gly) |
|---|---|---|---|---|---|
| 1 | Star-formation peak | 7.94 | 5 860 | 11.1 | 5.54 |
| 2 | Quasar era | 10.51 | 3 280 | 17.3 | 5.77 |
| 6 | Reionisation ends | 12.86 | 930 | 27.5 | 3.93 |
| 10.6 | GN-z11 | 13.36 | 436 | 31.9 | 2.75 |
| 14.44 | MoM-z14 | 13.51 | 283 | 33.9 | 2.19 |
| 1 100 | CMB | 13.79 | 0.37 | 45.3 | 0.041 |

: Time and distance in flat ΛCDM ($H_0$ = 67.7 km/s/Mpc, $\Omega_m$ = 0.31); 1 Gly = 10⁹ light-years. {#tbl:cosmodist}

::: example
**Example: how far, and how big?**

For the same galaxy at $z$ = 14.0, compare the distances and decide whether JWST can resolve it.

1. **Light-travel distance**: 13.5 billion light-years (Gly), the number usually quoted.
2. **Comoving distance today**: integrating $c/H(z)$ from 0 to 14 gives 10 330 Mpc = **33.7 Gly**, 2.5 times the light-travel distance.
3. **Distance when the light left**: comoving distance ÷ $(1+z)$ = 33.7/15.0 = **2.25 Gly**, only a sixth of the light-travel distance. In a flat universe this equals the angular-diameter distance.
4. **Angular size**: a galaxy 500 parsecs (1 630 light-years) across subtends $500\ \text{pc}/688.6\ \text{Mpc} = 7.3\times10^{-7}$ rad = **0.15″**.
5. **Resolution**: JWST's diffraction limit at 2 µm is $1.22 \times 2\times10^{-6}/6.5$ = 3.75 × 10⁻⁷ rad = **0.077″**, half the galaxy's size, so JWST resolves it into about two resolution elements across. Hubble at 1.6 µm (0.17″) could not, even if the light were in its band.
6. **Luminosity distance**: $(1+z)$ × comoving distance = **505 Gly**, so the flux is 15² = 225 times lower than an inverse-square estimate using the comoving distance.
:::

## Surveys and Exoplanet Hunters

**Survey missions** observe large parts of the sky systematically to build catalogues, measure the shape of the Universe or find rare events. Their power depends less on aperture than on **étendue**, the product of collecting area and field of view, which sets how fast they map the sky (@fig:obsapertures b).

### Finding Planets: Kepler and TESS

When a planet of radius $R_p$ crosses a star of radius $R_\star$, the star dims by the **transit depth** $\delta = (R_p/R_\star)^2$ (@fig:obstransit a): 84 parts per million (ppm) for Earth crossing the Sun, about 1 % for Jupiter. Only a fraction $R_\star/a$ of systems, for a planet at distance $a$, are aligned so that transits occur — 0.47 % for an Earth–Sun analogue — so a transit survey must monitor tens of thousands of stars or more.

NASA's **Kepler** (2009–18) used a 0.95 m Schmidt telescope and a 95-megapixel camera covering 115 square degrees (@fig:obskepler) to measure about 150 000 stars in Cygnus and Lyra every 30 minutes for four years. When a second reaction wheel failed in 2013, engineers balanced the spacecraft against sunlight pressure, and the **K2** mission observed fields along the ecliptic until the propellant ran out in October 2018. Kepler showed that planets are the rule rather than the exception, that the commonest planets in the Galaxy are between Earth and Neptune in size — a type absent from the Solar System — and that a substantial fraction of Sun-like stars (estimates range from about one in ten to one in two) have an Earth-sized planet in the habitable zone.

![(a) Transit depth versus planet radius for four types of star, with the photometric precision of Kepler and TESS. (b) Signal of one atmospheric scale height in transmission for selected planets: hydrogen-rich planets give tens to hundreds of ppm, rocky planets with nitrogen-rich air from a fraction of a ppm (Earth around the Sun) to about 15 ppm (TRAPPIST-1 e around a tiny star).](figures/out/ch39_transit.svg){#fig:obstransit width=98%}

The **Transiting Exoplanet Survey Satellite (TESS)**, launched in 2018, has four 10.5 cm cameras covering a 24° × 96° strip of sky, which it observes for 27 days before moving on. It has covered more than 98 % of the sky, concentrating on bright, nearby stars whose planets can be weighed from the ground and studied by JWST. By October 2026 it had flagged 8 151 "TESS Objects of Interest" — possible planets, some later shown to be false alarms — and 1 012 of its discoveries were confirmed planets; it continues in its third extended mission. ESA's **CHEOPS** (2019), a 32 cm telescope, measures the radii of known planets precisely.

::: example
**Example: can TESS find an Earth twin?**

An Earth-sized planet orbits a Sun-like star (1.0 $R_\odot$, 1.0 $M_\odot$) once a year. For a bright star TESS reaches about 60 ppm of noise in one hour.

1. **Depth**: $\delta = (6\,371/695\,700)^2$ = 8.4 × 10⁻⁵ = **84 ppm**.
2. **Duration** of a central transit: $T \approx (P/\pi)\,(R_\star/a)$ = (8 766 h/π) × (695 700/149.6 million) = **13.0 hours**.
3. **Noise over one transit**: 60 ppm/√13 = 16.6 ppm, giving a signal-to-noise ratio of 84/16.6 = **5.0**.
4. **Detection** conventionally needs a ratio of about 7.1, i.e. (7.1/5.0)² ≈ **2 transits** — a continuous baseline of more than a year. TESS watches most stars for only 27 days, so it essentially cannot find Earth twins, and only 0.47 % of such systems transit at all. That is the job of PLATO, which will stare at the same fields for two years or more.
5. **Around a small red dwarf** (0.2 $R_\odot$), the same planet in the habitable zone (about 0.07 AU) orbits in 14 days with a depth of **2 100 ppm**. Even with three times the noise from the fainter star, one 1.5-hour transit gives a ratio of about 14, and TESS sees two transits per sector. This is why most known small temperate planets — and those JWST can study — orbit red dwarfs.
:::

By October 2026 the NASA Exoplanet Archive listed **6 451 confirmed planets** (@fig:obsexoplanets), with more than 8 000 candidates awaiting confirmation; three-quarters (4 785) were found by transits, and over half (3 337) by Kepler and K2. @tbl:exomissions summarises the main space missions.

![Exoplanet discoveries by year and method (NASA Exoplanet Archive, October 2026). The peaks in 2014 and 2016 are statistical validations of large batches of Kepler candidates.](figures/out/ch39_exoplanets.svg){#fig:obsexoplanets width=98%}

| Mission | Years | Method | Telescope / field | Role and status (Oct 2026) |
|---|---|---|---|---|
| Kepler / K2 (NASA) | 2009–18 | Transit | 0.95 m, 115 deg² | Planet statistics; 3 337 planets |
| TESS (NASA) | 2018– | Transit | 4 × 10.5 cm, 2 304 deg² | Bright nearby stars; 1 012 planets |
| JWST (NASA/ESA/CSA) | 2021– | Spectroscopy, imaging | 6.5 m | Atmospheres of known planets |
| Roman (NASA) | 2026– | Microlensing, coronagraph | 2.4 m, 0.28 deg² | Cold planets; >1 000 expected |
| PLATO (ESA) | 2027– | Transit | 26 × 12 cm | Earth analogues around Sun-like stars |
| Ariel (ESA) | 2029– | Spectroscopy | 1.1 × 0.7 m | Atmospheres of about 1 000 planets |
| HWO (NASA) | 2040s | Direct imaging | ≈ 6 m | Search for life on ~25 Earth-like planets |

: Space missions for finding and characterising exoplanets. {#tbl:exomissions}

### Gaia: Mapping the Galaxy

ESA's **Gaia** (2013–25) measured the positions, distances and motions of nearly two billion stars from L2. Two telescopes 106.5° apart scanned the sky as the spacecraft rotated, imaging onto nearly a billion pixels, so that angles between stars were measured to ten to a few tens of micro-arcseconds — roughly the size of a coin on the Moon seen from Earth. Its **parallaxes**, the annual shifts of stars caused by Earth's orbit, give distances to over a billion stars, and its data revealed the debris of a dwarf galaxy that merged with the Milky Way about 10 billion years ago. Science operations ended on 15 January 2025; the fourth data release, from 5.5 years of data and more than 500 TB, is scheduled for December 2026.

### Mapping the Dark Universe: Euclid, SPHEREx, Roman and Xuntian

**Euclid** (ESA, July 2023), a 1.2 m telescope with a 0.53-square-degree field — over a hundred times that of Hubble's main camera — is mapping a third of the sky in six years to measure the shapes of more than a billion galaxies. Their tiny, coherent distortions by intervening matter (**weak gravitational lensing**) and the clustering of galaxies reveal how dark matter is distributed and how dark energy has driven the expansion. Its first quick release (March 2025) covered 63 square degrees and 26 million galaxies; the first major data release (DR1) begins in November 2026 with images and catalogues of about 1 900 square degrees, while the weak-lensing and clustering products needed for cosmology follow in mid-2027. NASA's **SPHEREx** (March 2025) splits light into 102 colours from 0.75 to 5 µm with a 20 cm telescope; it completed the first of four planned all-sky spectral maps in December 2025, seeking imprints of **cosmic inflation** — the extremely rapid expansion thought to have occurred in the first instant after the Big Bang — and surveying interstellar ices.

The **Nancy Grace Roman Space Telescope** (NASA, about US$ 4 billion) pairs a 2.4 m mirror, donated by the US National Reconnaissance Office, with a 300-megapixel camera whose field is about 200 times that of Hubble's infrared camera. Launched on a Falcon Heavy on 30 August 2026, ahead of schedule (@fig:obsroman), it was being commissioned on its way to L2 in October 2026, with first science images expected in early 2027. Over five years it will map dark energy, find more than a thousand planets towards the Galactic centre by **gravitational microlensing** (the brief brightening of a background star as a planet passes in front of it) and test a coronagraph required to detect planets 10⁷ times fainter than their star (ground tests reached better than 5 × 10⁻⁸), a step towards the 10¹⁰ needed for Earth twins.

::: figrow
![The Kepler spacecraft in a clean room at Ball Aerospace in Boulder, Colorado, in 2008. The white dust cover on the sunshade was jettisoned after launch.](figures/photos/ch39_kepler.jpg){#fig:obskepler width=74%}

![The Nancy Grace Roman Space Telescope being encapsulated in its Falcon Heavy payload fairing at Kennedy Space Center on 21 August 2026, nine days before launch.](figures/photos/ch39_romanfairing.jpg){#fig:obsroman width=74%}
:::

China's 2 m **Xuntian** survey telescope (CSST, 1.1-square-degree field) is to be launched in 2027 into the orbit of the Tiangong station, where it can dock for servicing. ESA's **PLATO**, with 26 small cameras, is due for launch on Ariane 6 in early 2027 (ESA's mission page gives April) to find Earth-sized planets in the habitable zones of Sun-like stars, and **Ariel** (2029) will measure the atmospheres of about a thousand exoplanets.

## High-Energy and Time-Domain Astronomy

X-ray and gamma-ray observatories study the most violent events in the Universe, many lasting seconds to days, so high-energy astronomy is a **time-domain** discipline: wide-field monitors detect a burst and narrow-field telescopes swing onto it within minutes.

- **Fermi** (NASA, 2008) combines the Large Area Telescope (20 MeV to over 300 GeV), which surveys the whole gamma-ray sky every three hours and has catalogued about 7 000 sources, with a burst monitor (8 keV–40 MeV). On 17 August 2017 it detected a short gamma-ray burst 1.7 seconds after LIGO and Virgo recorded gravitational waves from merging neutron stars, opening **multi-messenger astronomy**.
- **Swift** (NASA, 2004) could turn to a new burst in about a minute and observe it with X-ray and ultraviolet/optical telescopes; it observed more than 2 000 gamma-ray bursts. The high solar activity of 2024–25 made its orbit decay much faster than predicted. NASA paid Katalyst Space US$ 30 million for a robotic spacecraft to grab Swift and raise its orbit; launched on a Pegasus XL on 3 July 2026, it suffered attitude-control problems, and the attempt was abandoned on 19 August. Below 275 km drag prevented steady pointing: Swift made its last observation on 20 October 2026, NASA ended the mission on 23 October, and re-entry is expected within weeks.
- **NuSTAR** (NASA, 2012) was the first telescope to focus hard X-rays (3–79 keV), using a 10 m mast unfolded in orbit for the long focal length grazing-incidence optics need. **IXPE** (NASA–Italy, 2021) measures X-ray **polarisation**, revealing the geometry of magnetic fields in pulsars and black-hole jets.
- **XRISM** (JAXA with NASA and ESA, 2023) carries **Resolve**, a microcalorimeter that measures each X-ray photon's energy from the tiny temperature rise it causes in a detector at 0.05 K, with 20–30 times finer spectral resolution than X-ray CCDs. Its protective gate valve has failed to open, blocking X-rays below about 1.7 keV, but it works superbly at higher energies and operations have been extended to 2030.
- **eROSITA**, the German telescope on Russia's Spektr-RG (2019), completed four all-sky X-ray surveys before being idled in February 2022 after Russia's invasion of Ukraine; its July 2026 release lists about two million sources.
- **Einstein Probe** (China with ESA, Germany and France, January 2024) uses "lobster-eye" optics, modelled on crustacean eyes, to watch 3 600 square degrees at once in soft X-rays and has found many new transients; the Chinese–French **SVOM** (June 2024) detects gamma-ray bursts and follows up its alerts. ESA's **XMM-Newton** (1999) remains Europe's X-ray spectroscopy workhorse.

## Microwaves, Radio and Gravitational Waves

The **cosmic microwave background (CMB)** is light released 370 000 years after the Big Bang, when the Universe became transparent, now stretched 1 100-fold into microwaves. NASA's **COBE** (1989) showed that it has a perfect blackbody spectrum at 2.725 K and detected temperature variations of a few parts in 100 000 — the seeds of all later structure — work recognised by the 2006 Nobel Prize in Physics. **WMAP** (2001–10) mapped those variations over the whole sky from L2, and ESA's **Planck** (2009–13) mapped them in nine frequency bands with about three times better resolution. Planck's final results (2018) gave an age of 13.8 billion years, a composition of about 5 % ordinary matter, 27 % dark matter and 68 % dark energy, and $H_0$ = 67.4 ± 0.5 km/s/Mpc.

In radio astronomy space extends the size of an interferometer: Russia's **RadioAstron** (2011–19) linked a 10 m orbiting antenna, reaching about 350 000 km from Earth, with ground radio telescopes, achieving resolutions of about ten micro-arcseconds.

The next frontier is not light at all. The **Laser Interferometer Space Antenna (LISA)**, adopted by ESA in January 2024 with NASA participation and planned for launch on Ariane 6 in 2035, will fly three spacecraft in a triangle 2.5 million km on a side and use lasers to measure picometre changes in their separations. It will detect low-frequency **gravitational waves** from merging supermassive black holes and compact binary stars, which ground-based detectors such as LIGO cannot hear.

## The Fleet in 2026 and the Road Ahead

@fig:obsgantt shows how missions have succeeded one another since 1990, and @tbl:obsfleet lists the main observatories operating or approved in October 2026. Missions outlive their plans — Hubble was designed for 15 years and Chandra for five; Europe, China and Japan now lead many missions; and apertures grow slowly, limited by fairings and cost (@fig:obsapertures a), so progress comes largely from wider fields, better detectors and colder telescopes.

| Mission | Lead | Band | Aperture | Orbit | Launch | Status |
|---|---|---|---|---|---|---|
| Hubble | NASA/ESA | 0.115–1.7 µm | 2.4 m | LEO 470 km | 1990 | One-gyro mode |
| Chandra | NASA | 0.1–10 keV | 1.2 m | HEO | 1999 | Minimum-cost |
| Swift | NASA | γ, X-ray, UV | 0.3 m | LEO 265 km | 2004 | Ended Oct 2026 |
| Fermi | NASA | 8 keV–300 GeV | Detectors | LEO 490 km | 2008 | Budget threat |
| TESS | NASA | 0.6–1.0 µm | 4 × 10.5 cm | HEO | 2018 | Extended |
| JWST | NASA/ESA/CSA | 0.6–28.5 µm | 6.5 m | L2 | 2021 | Cycle 5 |
| Euclid | ESA | 0.55–2.0 µm | 1.2 m | L2 | 2023 | Surveying |
| XRISM | JAXA/NASA | 1.7–12 keV | 2 × 0.45 m | LEO 525 km | 2023 | Operating |
| Einstein Probe | CAS/ESA | 0.3–10 keV | Lobster-eye | LEO 600 km | 2024 | Operating |
| SPHEREx | NASA | 0.75–5.0 µm | 0.2 m | LEO 650 km | 2025 | Surveying |
| Roman | NASA | 0.48–2.3 µm | 2.4 m | L2 | 2026 | Commissioning |
| PLATO | ESA | 0.5–1.0 µm | 26 × 0.12 m | L2 | 2027 | Final testing |
| Xuntian | China | 0.25–1.0 µm | 2 m | LEO | 2027 | Building |
| Ariel | ESA | 0.5–7.8 µm | 1.1 × 0.7 m | L2 | 2029 | Building |
| PRIMA | NASA | 24–235 µm | 1.8 m | L2 | 2033 | Selected |
| LISA | ESA/NASA | Grav. waves | 3 × 0.3 m | Solar orbit | 2035 | Adopted |
| NewAthena | ESA | 0.2–12 keV | ≈ 2.5 m | L-point | 2037 | Study |
| HWO | NASA | UV–near-IR | ≈ 6 m | L2 | 2040s | Concept |

: Major space observatories operating or approved in October 2026 (launch years of future missions are targets). {#tbl:obsfleet}

![Timeline of major space observatories, 1990–2040. Bars show operating life from launch; hatched bars are planned missions starting at their target launch dates.](figures/out/ch39_gantt.svg){#fig:obsgantt width=80%}

![(a) Primary-mirror diameter of space telescopes against launch year. (b) Survey power (étendue): collecting area multiplied by the field of view of the main camera. Wide-field survey telescopes map the sky thousands of times faster than Hubble or JWST.](figures/out/ch39_apertures.svg){#fig:obsapertures width=94%}

### New Missions and the Habitable Worlds Observatory

In September 2026 NASA selected **PRIMA**, a cryogenically cooled 1.8 m far-infrared telescope, as the first mission in a new **Probe** class with a cost cap of US$ 1.2 billion; due for launch in 2033, it will study how galaxies, stars and planets form, filling the gap left by Spitzer and Herschel. The UVEX ultraviolet explorer (about 2030) and Israel's ULTRASAT (2027) will survey the ultraviolet sky, and ESA's **NewAthena** X-ray observatory is planned for adoption in 2027 and launch in the late 2030s.

The 2021 US astronomy decadal survey recommended as NASA's next great observatory a telescope of about 6 m to image Earth-like planets around Sun-like stars and search their spectra for oxygen, water and methane. This **Habitable Worlds Observatory (HWO)** needs a coronagraph suppressing starlight by 10¹⁰ — an Earth seen from 30 light-years is ten billion times fainter than its star and only 0.1″ from it — and a wavefront stable to picometres. NASA aims for launch in the early 2040s, but funding is uncertain: Congress provided about US$ 150 million for 2026, while the 2027 request proposed almost nothing.

Astronomers thus have more capability in space than ever, yet budget requests propose ending productive missions that cost tens of millions a year to run after costing billions to build.

::: ai
**AI in space astronomy**

Machine learning classifies **transients**: ground surveys such as the Vera C. Rubin Observatory, which released its first images in 2025, are expected to issue millions of alerts per night, and classifiers in "alert brokers" decide within minutes which supernovae, tidal-disruption events or X-ray flares deserve follow-up by satellites such as Einstein Probe. In **exoplanet vetting**, neural networks trained on Kepler light curves separate true transits from eclipsing binaries and instrumental artefacts; one found the eighth planet of Kepler-90 in 2017, and NASA's ExoMiner validated 301 new Kepler planets in 2021. **Galaxy morphology** is classified by deep networks trained on volunteers' labels from the Galaxy Zoo project, now applied to Euclid images. All such outputs must be validated, because a subtle bias can mimic a discovery (Chapter 51).
:::

::: key
**Key takeaways**

- Space telescopes gain wavelengths the atmosphere blocks, diffraction-limited sharpness and photometric stability, at hundreds of times the ground's cost per square metre.
- Of NASA's Great Observatories, Hubble (one-gyro mode, median re-entry late 2033) and Chandra (minimum-cost operations) still worked in October 2026; Compton and Spitzer ended in 2000 and 2020.
- JWST has seen galaxies to $z$ = 14.44, 280 million years after the Big Bang, found surprisingly early black holes and measured exoplanet atmospheres; the K2-18 b biosignature claim is unconfirmed.
- Light from $z$ = 14 left 13.5 billion years ago from a source now 34 billion light-years away, which was 2.25 billion light-years away when the light left: cosmic distances must be defined carefully.
- A transiting Earth dims a Sun-like star by 84 ppm for 13 hours. Of 6 451 confirmed exoplanets (October 2026), three-quarters were found by transits; PLATO will hunt true Earth analogues.
- Survey telescopes gain power from wide fields; high-energy missions form a rapid-response network.
- PLATO and Xuntian (2027), Ariel (2029), PRIMA (2033), LISA (2035), NewAthena and the Habitable Worlds Observatory lie ahead, but budget threats to operating missions are serious.
:::

::: questions
**Review questions**

1. Give three reasons for putting a telescope in space, with an example of each.
2. What caused Hubble's spherical aberration, and why could it be corrected completely?
3. Compare LEO, HEO and an L2 halo orbit for an infrared telescope and for an X-ray telescope.
4. Why must X-ray telescopes use grazing-incidence mirrors, and with what consequences?
5. Why can JWST, but not Hubble, see galaxies beyond $z$ ≈ 13?
6. Using @tbl:cosmodist, give the look-back time, age at emission and comoving distance for $z$ = 6. Why does the comoving distance exceed the light-travel distance?
7. Find the transit depth and duration for a 3.9 Earth-radius planet in a 30-day orbit around a Sun-like star.
8. Why is the K2-18 b dimethyl-sulphide claim unconfirmed, and what would establish a biosignature?
9. Define étendue, and explain why SPHEREx, with a 20 cm telescope, maps the sky faster than JWST.
10. Discuss the case for and against funding old observatories such as Hubble and Chandra when new missions need money.
:::
