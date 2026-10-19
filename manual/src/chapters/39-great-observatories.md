---
title: Great Observatories and Deep-Space Telescopes
hero: ch39
abstract: Most of the light in the Universe never reaches the ground. Space telescopes recover the gamma rays, X-rays, ultraviolet and infrared that the atmosphere absorbs, see sharper than turbulent air allows and measure brightness steadily enough to find Earth-sized planets. This chapter tells the story of NASA's four Great Observatories — Hubble, Compton, Chandra and Spitzer — and of the James Webb Space Telescope, which by 2026 had seen galaxies 280 million years after the Big Bang and analysed the air of distant worlds. It explains redshift, look-back time and the several meanings of cosmic distance, reviews the survey, exoplanet, high-energy and cosmic-microwave missions, and describes the fleet operating in October 2026 and the observatories planned for the 2030s and 2040s.
---

An astronomer on the ground looks out through a thick, warm, moving filter. Earth's atmosphere absorbs all gamma rays and X-rays, almost all ultraviolet light and most of the infrared; water vapour glows brightly at infrared wavelengths; and turbulence smears every star into a shimmering blob about one arcsecond (1″, 1/3 600 of a degree) across. A telescope above the atmosphere escapes all three problems. It can observe at any wavelength, reach the sharpness set by the physics of diffraction, and measure a star's brightness to a few parts per million for weeks at a time.

Since 1990 these advantages have produced some of the most productive scientific instruments ever built. This chapter describes what space telescopes do and what they have found: the **Great Observatories** programme, the James Webb Space Telescope (JWST), the survey and exoplanet missions, the high-energy and cosmic-microwave observatories, and the fleet that is operating or planned in October 2026. How these telescopes are engineered — mirrors, detectors, cryogenics and pointing — is the subject of Chapter 38; here the focus is on missions, capabilities and results.

## Why Observe from Space

### The Atmospheric Filter

@fig:obsspectrum shows which parts of the electromagnetic spectrum reach the ground. Only two broad **windows** are open: the optical window from about 0.3 to 1 µm, with some partial windows in the near-infrared, and the radio window from about 1 cm to 15 m. Everything else must be observed from above most or all of the atmosphere. High-energy photons are absorbed by atoms in the upper atmosphere; ultraviolet light below 0.3 µm is absorbed by ozone; infrared light is absorbed and re-emitted by water vapour and carbon dioxide; and the ionosphere reflects radio waves longer than about 15 m. Balloons and sounding rockets (Chapters 8 and 9) can sample some of these bands for hours or minutes, but only satellites can observe for years.

![Wavelength coverage of the main space observatories, past, present and planned. The strip at the top shows schematically where Earth's atmosphere is opaque, partly transparent or clear: gamma-ray, X-ray, ultraviolet and far-infrared astronomy is possible only from space.](figures/out/ch39_emcoverage.svg){#fig:obsspectrum width=96%}

### Sharpness, Darkness and Stability

Even in the open windows, space wins on three counts.

- **Resolution.** A perfect telescope of diameter $D$ observing at wavelength $\lambda$ cannot separate points closer than about $\theta = 1.22\,\lambda/D$ radians, the **diffraction limit**. For Hubble's 2.4 m mirror at 0.5 µm this is 0.05″, twenty times sharper than typical ground-based seeing. Adaptive optics on large ground telescopes now correct turbulence in the near-infrared, but only over small fields and with lower stability.
- **Background.** The night sky glows faintly because of airglow in the upper atmosphere, and in the infrared the atmosphere and the telescope itself shine like a warm oven. A telescope cooled to 40 K in deep space has an infrared background many orders of magnitude lower, which is why JWST, with a quarter of the collecting area of the largest ground telescopes, is far more sensitive than any of them at wavelengths beyond about 2 µm.
- **Stability.** Starlight twinkles because of turbulence (scintillation). Above the atmosphere, a star's brightness can be measured continuously to tens of parts per million, the precision needed to see an Earth-sized planet cross a Sun-like star.

The price is high. A space telescope must fit inside a launch-vehicle fairing (about 5 m in diameter), survive launch, work without adjustment by hand, and usually cannot be repaired. Cost per square metre of collecting area is hundreds of times that of a ground telescope. The two approaches are therefore complementary: the largest ground telescopes, such as the 39 m Extremely Large Telescope under construction in Chile, collect more light, while space telescopes provide wavelengths, sharpness and stability that the ground cannot.

### Where Space Telescopes Fly

The choice of orbit trades access, thermal environment and observing efficiency (@fig:obsorbits). Hubble, Fermi, NuSTAR and IXPE fly in **low Earth orbit (LEO)**, where they are easy to reach and launch, can downlink data often and are shielded from much of the radiation by Earth's magnetic field — but Earth hides most targets for part of every 95-minute orbit and the warm planet heats the spacecraft. X-ray telescopes such as Chandra and XMM-Newton use **highly elliptical orbits** reaching a third of the way to the Moon, so that they spend most of their time above the radiation belts and can make uninterrupted observations lasting more than a day. TESS uses a unique orbit in 2:1 resonance with the Moon.

The cold, quiet observatories — WMAP, Planck, Herschel, Gaia, JWST, Euclid and Roman — go to a **halo orbit around the Sun–Earth L2 point**, 1.5 million km beyond Earth (Chapter 3). There the Sun, Earth and Moon always lie in roughly the same direction, so one sunshield can block all three. Kepler and Spitzer used **Earth-trailing heliocentric orbits**, slowly drifting away from Earth; when they were switched off they were 170 and 266 million km away respectively.

![Where astronomical observatories fly, from the low orbits of Hubble and the X-ray and gamma-ray missions to the Sun–Earth L2 point and Earth-trailing solar orbits.](figures/out/ch39_orbits.svg){#fig:obsorbits width=92%}

## NASA's Great Observatories

In the 1980s NASA planned four large observatories, each covering a different part of the spectrum and each designed to work alongside the others: the **Hubble Space Telescope** (visible and ultraviolet), the **Compton Gamma Ray Observatory**, the **Chandra X-ray Observatory** and the **Spitzer Space Telescope** (infrared). Three were launched by the Space Shuttle. The four never flew all at once — Compton came down in 2000, three years before Spitzer was launched — but two remain in service in 2026 (@tbl:greatobs).

| Observatory | Band | Telescope | Launch | Orbit | End | Signature results |
|---|---|---|---|---|---|---|
| Hubble | 0.115–1.7 µm | 2.4 m mirror | 24 Apr 1990, STS-31 | LEO, 28.5° | Operating | Deep fields; expansion rate; dark energy |
| Compton (CGRO) | 20 keV–30 GeV | Four instruments, 17 t | 5 Apr 1991, STS-37 | LEO, 28.5° | Deorbited 4 Jun 2000 | Gamma-ray bursts are cosmic; blazars |
| Chandra | 0.1–10 keV | 1.2 m nested mirrors, 0.5″ | 23 Jul 1999, STS-93 | ≈ 64-hour HEO | Operating | Dark matter in Bullet Cluster; black holes |
| Spitzer | 3.6–160 µm | 0.85 m, helium-cooled | 25 Aug 2003, Delta II | Earth-trailing | 30 Jan 2020 | TRAPPIST-1 planets; first exoplanet light |

: NASA's four Great Observatories. {#tbl:greatobs}

### Hubble Space Telescope

Hubble is a 2.4 m Ritchey–Chrétien reflector (Chapter 12) about 13 m long with a mass of about 11 t. Space Shuttle Discovery released it on 25 April 1990 at an altitude of about 615 km (@fig:obssts31). Within weeks it was clear that the images were blurred: the primary mirror had been polished very precisely to the wrong shape. A spacing error of 1.3 mm in the optical test device used during polishing (the null corrector) had made the mirror about 2.2 µm too flat at its edge, producing **spherical aberration**, in which light from the edge and the centre of the mirror comes to focus at different points.

![Hubble held by Discovery's robotic arm on 25 April 1990, during deployment on mission STS-31, with one solar array unrolled and the second still stowed.](figures/photos/ch39_sts31.jpg){#fig:obssts31 width=66%}

Because the error was known exactly, it could be corrected exactly, like prescribing spectacles. The first servicing mission (STS-61, December 1993) installed the **Wide Field and Planetary Camera 2**, which had the correction built into its own optics, and **COSTAR**, a set of small corrective mirrors on deployable arms that fed the other instruments. Every later instrument included its own correction, and COSTAR was removed in 2009. Astronauts visited Hubble five times between 1993 and 2009, replacing gyroscopes, batteries, solar arrays and every original science instrument (the spacewalks are described in Chapter 33, and servicing as an industry in Chapter 40). The last visit, Servicing Mission 4 in May 2009, installed Wide Field Camera 3 and the Cosmic Origins Spectrograph, which remain in use with the Advanced Camera for Surveys and the Space Telescope Imaging Spectrograph.

Hubble's results span astronomy. Its **Key Project** measured the expansion rate of the Universe, the **Hubble constant**, to about 10 % (72 ± 8 km/s per megaparsec) in 2001; its observations of distant supernovae helped show in 1998 that the expansion is accelerating, the evidence for **dark energy**. The **Hubble Deep Field** (1995) and **Ultra Deep Field** (2004) — long exposures of apparently empty patches of sky — revealed thousands of galaxies and traced how they grew. Hubble found that almost every large galaxy has a supermassive black hole at its centre, watched comet Shoemaker–Levy 9 hit Jupiter in 1994, and made the first detection of an exoplanet's atmosphere (sodium in HD 209458 b, 2001). Its images, such as the "Pillars of Creation" in the Eagle Nebula (@fig:obspillars), are among the most widely recognised scientific pictures ever made.

![The "Pillars of Creation" in the Eagle Nebula, re-imaged by Hubble in near-infrared light in 2014. Infrared light passes through much of the dust, revealing stars behind and inside the columns of cold gas.](figures/photos/ch39_pillars.jpg){#fig:obspillars width=60%}

**Hubble in 2026.** On 19 September 2026 Hubble completed its 200 000th orbit; it has made more than 1.7 million observations in 36 years. Its gyroscopes, which sense the rotation of the spacecraft, are its main ageing problem: of the six installed in 2009, two still work. Since June 2024 Hubble has operated in **one-gyro mode**, keeping the second as a spare. This reduces the area of sky it can observe at any moment from about 80 % to 40–50 % and initially cut the number of observations by about a tenth, a loss largely recovered since by better scheduling. There have been no safe-mode events since the change, and STScI expects both remaining gyroscopes, of an improved design, to last into the mid-2030s. Atmospheric drag is slowly lowering the orbit, now about 470 km: the Space Telescope Science Institute (STScI) estimates a less than 10 % chance of re-entry before 2032 and a median re-entry date in late 2033 unless Hubble is boosted. NASA studied a privately funded reboost by a SpaceX Crew Dragon in 2022–24 and declined it in June 2024, citing the risks to the telescope; in 2026 it said it would consider a reboost if Hubble's operating costs could be reduced. Budget pressure is the other threat: STScI was told in 2025 to plan for operating budgets about a fifth lower for 2026–28.

### Compton Gamma Ray Observatory

At about 17 t, the **Compton Gamma Ray Observatory** (CGRO) was the heaviest astronomical observatory flown up to that time (@fig:obsgro). Its four instruments covered photon energies from 20 keV to 30 GeV. The **Burst and Transient Source Experiment** (BATSE) recorded 2 704 **gamma-ray bursts** — brief, intense flashes of gamma rays — and showed that they come equally from all directions rather than concentrating along the Milky Way. This proved that bursts are not local but occur at cosmological distances, which makes them the most powerful explosions known. The **EGRET** telescope found that the high-energy gamma-ray sky is dominated by **blazars**: galaxies whose central black holes fire jets of particles almost directly at us. After one of its gyroscopes failed in December 1999, NASA chose to bring the observatory down under control rather than risk an uncontrolled re-entry of its dense components; it fell into the Pacific Ocean on 4 June 2000.

![The Compton Gamma Ray Observatory held by Atlantis's robotic arm during checkout on mission STS-37 in April 1991. The large cylinders are parts of the COMPTEL and EGRET telescopes.](figures/photos/ch39_gro.jpg){#fig:obsgro width=56%}

### Chandra X-ray Observatory

X-rays do not reflect from a mirror at normal incidence; they penetrate it. They can be focused only by **grazing incidence**, glancing off a polished surface at angles of about a degree, much as a stone skips across water. Chandra's mirror is therefore four nested pairs of nearly cylindrical iridium-coated shells, the largest 1.2 m across, with a focal length of 10 m (Chapter 38 explains the optics). Its angular resolution of 0.5″ is still the sharpest of any X-ray telescope. Columbia deployed Chandra on 23 July 1999, on the first Shuttle mission commanded by a woman, Eileen Collins (@fig:obschandrabay); an Inertial Upper Stage then lifted it into an orbit that now ranges from 12 650 to 136 200 km above Earth, with a period of 63.5 hours. With its upper stage, Chandra was the heaviest payload ever launched by the Shuttle (22.8 t).

![Chandra, with its Inertial Upper Stage, in Columbia's payload bay shortly before being tilted up for release on 23 July 1999.](figures/photos/ch39_chandrabay.jpg){#fig:obschandrabay width=54%}

Chandra sees the hot Universe: gas at millions of degrees in clusters of galaxies, the remnants of exploded stars, and matter falling into black holes and neutron stars. In 2006, Chandra's map of hot gas in the colliding **Bullet Cluster**, compared with the mass distribution measured by gravitational lensing, showed that most of the mass had passed through the collision while the gas had been slowed — direct evidence for **dark matter**. With JWST in 2023 it detected X-rays from **UHZ1**, a growing black hole seen when the Universe was less than 500 million years old. @fig:obscrab shows how Chandra combines with other observatories: each wavelength reveals a different part of the same object.

![The Crab Nebula, the remnant of a supernova seen in 1054, combining radio (Very Large Array), infrared (Spitzer), visible (Hubble), ultraviolet (XMM-Newton) and X-ray (Chandra) data. The X-rays (purple-white) come from the most energetic particles near the central pulsar.](figures/photos/ch39_crab.jpg){#fig:obscrab width=56%}

Chandra has also become the symbol of a budget problem. NASA's budget requests for 2025 and 2026 proposed winding it down to save its operating cost of about US$ 70 million a year. Astronomers and Congress objected: the enacted appropriation for fiscal year 2026 (signed in January 2026) gave astrophysics US$ 1.595 billion and directed at least US$ 63 million to Chandra, enough for a "minimum-cost mission" with reduced staff. The request for 2027, published in April 2026, would cut NASA astrophysics by about 65 % to US$ 552 million and end Chandra and Fermi; a House committee bill rejected the cut, but no 2027 budget had been enacted in October 2026.

### Spitzer Space Telescope

Spitzer, the infrared Great Observatory, pioneered a design that JWST later followed: it was **launched warm**. Earlier infrared telescopes such as IRAS (1983) and ISO (1995) were enclosed in large tanks of liquid helium. Spitzer launched with only its instruments inside a small helium cryostat; its 0.85 m beryllium telescope cooled itself by radiating heat to space, helped by cold helium vapour vented from the cryostat, in an Earth-trailing orbit far from the warm Earth (@fig:obsspitzer). The helium lasted until May 2009, after which Spitzer continued for more than ten years in a "warm mission" using the two shortest-wavelength channels of its camera, which still worked at the telescope's new equilibrium temperature of roughly 30 K.

![Spitzer at Cape Canaveral being readied for launch in 2003. The telescope tube sits above the spacecraft bus, shaded by the solar panel on the right.](figures/photos/ch39_spitzer.jpg){#fig:obsspitzer width=40%}

Spitzer made the first detections of light emitted by planets around other stars (2005), mapped the temperature of a hot Jupiter across its surface, found a huge, faint ring around Saturn, and in 2017 helped establish that the cool dwarf star **TRAPPIST-1** has seven Earth-sized planets. Its Earth-trailing orbit, ideal for cooling, slowly carried it away from Earth, so that its antenna had to point ever closer to the Sun to send data home. NASA switched it off on 30 January 2020.

## The James Webb Space Telescope

JWST was conceived in the 1990s as Hubble's successor optimised for the infrared, because the light of the first galaxies, emitted as ultraviolet and visible light, is stretched by the expansion of the Universe into the infrared. Built by NASA with the European and Canadian space agencies, it is the largest and most complex scientific spacecraft ever launched (@tbl:jwstspecs). Its development took about 25 years and cost about US$ 10 billion, including the first five years of operations.

| Parameter | Value |
|---|---|
| Primary mirror | 6.5 m; 18 hexagonal segments of gold-coated beryllium; 25.4 m² collecting area |
| Wavelength range | 0.6–28.5 µm (visible red to mid-infrared) |
| Instruments | NIRCam (camera), NIRSpec (spectrograph), MIRI (mid-infrared), NIRISS and Fine Guidance Sensor |
| Sunshield | Five Kapton layers, 21.2 × 14.2 m; Sun side ≈ 360 K, cold side ≈ 40 K |
| Operating temperature | Telescope ≈ 40 K; MIRI 7 K (cryocooler) |
| Mass and orbit | About 6.2 t; halo orbit around Sun–Earth L2 |
| Launch | 25 December 2021, Ariane 5, Kourou |
| Lifetime | Propellant for about 20 years |

: The James Webb Space Telescope at a glance. {#tbl:jwstspecs}

![The 18 segments of JWST's primary mirror, fully assembled in the clean room at NASA's Goddard Space Flight Center in 2016. Each segment is 1.3 m across and can be moved by tiny actuators to bring the whole mirror into focus.](figures/photos/ch39_jwstmirror.jpg){#fig:obsjwstmirror width=64%}

### Launch and Commissioning

Because the mirror and sunshield were far larger than any fairing, JWST was launched folded (@fig:obsjwstmirror). Its deployment involved about 344 **single-point failures** — mechanisms whose failure would have ended the mission — including 107 release devices on the sunshield alone. Over the two weeks after launch the sunshield unfolded and tensioned, the secondary mirror swung out on its tripod and the two side wings of the primary mirror locked into place, all without serious problems. JWST reached L2 on 24 January 2022. Engineers then spent three months aligning the 18 segments to within a few tens of nanometres using images of a star, so that they act as one mirror. The Ariane 5 launch was so accurate that JWST saved enough propellant for about 20 years of operations instead of the 10 originally planned.

The first images were released on 12 July 2022. The first deep field (@fig:obsdeepfield), a 12.5-hour exposure of the galaxy cluster SMACS 0723, reached infrared depths beyond those of Hubble's deepest fields, which had taken weeks. Performance exceeds requirements: the images are sharper and the background lower than specified. One surprise was the damage from **micrometeoroids** (dust grains travelling at tens of km/s): an impact in May 2022 permanently distorted one mirror segment slightly. Since then JWST limits the time spent pointing towards the direction of its orbital motion, where impacts are most energetic.

![JWST's first deep field: the galaxy cluster SMACS 0723 in near-infrared light (2022). The cluster's mass acts as a gravitational lens, magnifying and stretching the images of galaxies far behind it into arcs.](figures/photos/ch39_deepfield.jpg){#fig:obsdeepfield width=60%}

### The First Galaxies

How far back can a telescope see? Light from a distant galaxy is stretched by the expansion of space by a factor $(1+z)$, where $z$ is the **redshift**. Hydrogen absorbs all light bluer than the Lyman-α line at 121.6 nm, so a young galaxy disappears abruptly below the wavelength $121.6\,(1+z)$ nm. @fig:obsredshift shows that for $z > 13$ this **Lyman break** moves beyond 1.7 µm, the red limit of Hubble's cameras: Hubble cannot see such galaxies at all. Hubble's most distant galaxy, GN-z11, was found in 2016 at a redshift later measured by JWST as 10.6.

![Observed wavelength of four bright spectral lines as a function of redshift, compared with the ranges of Hubble and JWST's instruments. At redshifts above about 13, even ultraviolet Lyman-α light arrives at wavelengths longer than Hubble can detect.](figures/out/ch39_redshiftlines.svg){#fig:obsredshift width=90%}

JWST has repeatedly broken the distance record, each time confirming the redshift with a spectrum rather than relying on colours alone. In 2024 the JADES survey confirmed **JADES-GS-z14-0** at $z$ ≈ 14.3 (refined to 14.18 by the ALMA radio telescope); in 2025 the MoM survey measured **MoM-z14** at $z$ = 14.44 (published in January 2026), seen just 280 million years after the Big Bang. As of October 2026 no galaxy had been spectroscopically confirmed at a greater distance. The surprise is not the distance but the brightness: JWST finds more luminous galaxies at redshifts above 10 than most models predicted, suggesting that early star formation was more efficient, or the first stars more luminous, than assumed. The puzzle is an active topic of research, not a contradiction of the standard cosmological model.

### Early Black Holes

JWST has also found black holes much earlier and larger than expected. Besides UHZ1, it found evidence of an actively feeding black hole in GN-z11 and discovered a population of compact, very red objects nicknamed **"little red dots"**, common about 600 million to 1.5 billion years after the Big Bang. Many appear to contain black holes millions of times the Sun's mass hidden in dense gas; in 2025 a team reported one of the earliest confirmed, CAPERS-LRD-z9, seen about 500 million years after the Big Bang. How black holes became so massive so quickly — whether they began as the collapse of huge gas clouds ("heavy seeds") or grew unusually fast from the remnants of the first stars — is one of the main questions JWST is addressing.

### Exoplanet Atmospheres

When a planet passes in front of its star, a little starlight filters through its atmosphere. Molecules absorb at characteristic wavelengths, so the planet appears slightly larger at those wavelengths: this **transmission spectrum** reveals the atmosphere's composition. In its first months JWST made the first clear detection of **carbon dioxide** in an exoplanet atmosphere, that of the hot Saturn WASP-39 b, followed by sulphur dioxide produced by starlight-driven chemistry — the first photochemistry seen on an exoplanet. Measurements of heat emitted by the rocky planets TRAPPIST-1 b and c suggest that they have little or no thick atmosphere.

The most publicised case shows the limits of the method. **K2-18 b** is a planet about two and a half times Earth's radius in the habitable zone of a red dwarf. JWST detected methane and carbon dioxide there in 2023, and in April 2025 a team reported mid-infrared evidence, at a confidence level of about three standard deviations, for dimethyl sulphide, a gas produced on Earth mainly by marine life. Independent reanalyses of the same data found the evidence insufficient: different but reasonable choices in data reduction and atmospheric modelling remove the signal. In October 2026 the claim remains unconfirmed. The lesson is that molecular features from small planets amount to tens of parts per million, close to the limits of the instruments, so claims of biosignatures demand several independent lines of evidence.

### JWST in 2026

JWST attracts more demand than any observatory before it. For its fifth observing cycle, which began on 1 July 2026, astronomers submitted 2 930 proposals requesting about 99 800 hours — roughly twelve times the time available. It has also checked Hubble's measurements of the variable stars used to calibrate the cosmic distance ladder and confirmed that they are not biased by crowding. Different calibrations still give values of the Hubble constant from about 70 to 73 km/s/Mpc, against 67–68 km/s/Mpc inferred from the cosmic microwave background: this **Hubble tension** remains unexplained. Its budget is under pressure too: the 2027 request proposed reduced operating funds for both JWST and Hubble.

## Reading the Distant Universe: Redshift, Time and Distance

Because light travels at a finite speed, a telescope that looks far away also looks back in time. In an expanding Universe, however, "how far away" has several meanings. The relationship between redshift and time depends on the cosmological model; the standard model, **flat ΛCDM** (a Universe dominated today by dark energy, Λ, and cold dark matter), with a Hubble constant $H_0$ = 67.7 km/s/Mpc and a matter density parameter $\Omega_m$ = 0.31, gives a present age of 13.79 billion years. The age of the Universe when light was emitted at redshift $z$ is

$$ t(z) = \int_z^\infty \frac{dz'}{(1+z')\,H(z')}, \qquad H(z) = H_0\sqrt{\Omega_m (1+z)^3 + \Omega_r (1+z)^4 + \Omega_\Lambda}, $$

where $\Omega_r \approx 9\times10^{-5}$ is the small contribution of radiation and $\Omega_\Lambda = 1 - \Omega_m - \Omega_r$. The **look-back time** is the present age minus $t(z)$. @fig:obslookback shows both and @tbl:cosmodist lists values computed from these equations.

![(a) Look-back time and age of the Universe at the time light was emitted, as functions of redshift. (b) Four measures of distance. Light from MoM-z14 travelled for 13.5 billion years, but the galaxy is now about 34 billion light-years away.](figures/out/ch39_lookback.svg){#fig:obslookback width=98%}

Four distances are in common use (@fig:obslookback b):

- **Light-travel distance**: the look-back time multiplied by the speed of light. It is what press releases usually quote ("13.5 billion light-years"), but it does not correspond to any distance that could be measured with a ruler.
- **Comoving distance**: the distance to the object *today*, if the expansion could be frozen and a ruler laid out. It is larger than the light-travel distance because space has expanded while the light was in transit; the edge of the observable Universe lies about 46 billion light-years away.
- **Angular-diameter distance**: the distance that relates an object's true size to the angle it appears to cover. Strangely, it reaches a maximum near $z \approx 1.6$ and then *decreases*: very distant galaxies appear larger than galaxies of the same size at intermediate distance, because we see them as they were when they were closer to us.
- **Luminosity distance**: the distance that relates an object's true power to the flux received, used with "standard candles" such as type Ia supernovae. It is larger than the comoving distance by a factor $(1+z)$ because photons lose energy and arrive less often.

| Redshift $z$ | Example | Look-back time (Gyr) | Age then (Myr) | Comoving distance (Gly) | Angular-diameter distance (Gly) |
|---|---|---|---|---|---|
| 1 | Peak era of star formation | 7.94 | 5 860 | 11.1 | 5.54 |
| 2 | Quasar epoch | 10.51 | 3 280 | 17.3 | 5.77 |
| 6 | End of reionisation | 12.86 | 930 | 27.5 | 3.93 |
| 10.6 | GN-z11 | 13.36 | 436 | 31.9 | 2.75 |
| 14.44 | MoM-z14 | 13.51 | 283 | 33.9 | 2.19 |
| 1 100 | Cosmic microwave background | 13.79 | 0.37 | 45.3 | 0.041 |

: Time and distance in flat ΛCDM ($H_0$ = 67.7 km/s/Mpc, $\Omega_m$ = 0.31); 1 Gly = 10⁹ light-years. {#tbl:cosmodist}

::: example
**Example: look-back time to redshift 14**

A galaxy's spectrum shows the Lyman break at 1.82 µm. How long ago did its light leave it, and how old was the Universe then?

1. **Redshift.** $1 + z = 1.824/0.1216 = 15.0$, so $z$ = 14.0. The break lies beyond Hubble's 1.7 µm limit; only JWST can measure it.
2. **Quick estimate.** At this redshift matter dominates, $H(z) \approx H_0\sqrt{\Omega_m}(1+z)^{3/2}$, and the integral gives $t \approx \tfrac{2}{3}\,(1/H_0)/[\sqrt{\Omega_m}(1+z)^{3/2}]$. With $1/H_0$ = 14.44 Gyr: $t \approx \tfrac{2}{3} \times 14.44/(0.557 \times 58.1)$ = **0.298 Gyr**.
3. **Exact integral.** Numerical integration including dark energy and radiation gives $t$ = **296 million years**, within 1 % of the estimate — dark energy was negligible then.
4. **Look-back time.** 13.79 − 0.30 = **13.50 billion years**: the light has travelled for 97.9 % of cosmic history.
:::

::: example
**Example: how far, and how big?**

For the same galaxy at $z$ = 14.0, use @tbl:cosmodist and @fig:obslookback to compare distances and to decide whether JWST can resolve it.

1. **Light-travel distance**: 13.5 billion light-years (Gly), the number usually quoted.
2. **Comoving distance today**: integrating $c/H(z)$ from 0 to 14 gives 10 330 Mpc = **33.7 Gly**, 2.5 times the light-travel distance.
3. **Distance when the light left**: comoving distance ÷ $(1+z)$ = 33.7/15.0 = **2.25 Gly** — the galaxy was then only a sixth as far as the light-travel distance suggests. In a flat universe this equals the angular-diameter distance.
4. **Angular size**: a galaxy 500 parsecs (1 630 light-years) across subtends $500\ \text{pc}/688.6\ \text{Mpc} = 7.3\times10^{-7}$ rad = **0.15″**.
5. **Resolution**: JWST's diffraction limit at 2 µm is $1.22 \times 2\times10^{-6}/6.5$ = 3.75 × 10⁻⁷ rad = **0.077″**, half the galaxy's size, so JWST resolves it into roughly two resolution elements across. Hubble at 1.6 µm (0.17″) could not, even if the light were inside its band.
6. **Luminosity distance**: $(1+z)$ × comoving = **505 Gly**. Its flux is therefore 15² = 225 times lower than a naive inverse-square estimate using the comoving distance.
:::

## Surveys and Exoplanet Hunters

Not every space telescope points at one object at a time. **Survey missions** observe large parts of the sky systematically to build catalogues, measure the shape of the Universe or find rare events. Their power is measured less by aperture alone than by **étendue**, the product of collecting area and field of view, which sets how fast they can map the sky (@fig:obsapertures b).

### Finding Planets: Kepler and TESS

When a planet of radius $R_p$ crosses a star of radius $R_\star$, the star dims by the **transit depth** $\delta = (R_p/R_\star)^2$ (@fig:obstransit a). For Earth crossing the Sun this is only 84 parts per million (ppm); for Jupiter it is about 1 %. Only a small fraction of planetary systems are aligned so that transits are visible — $R_\star/a$ for a planet at distance $a$, 0.47 % for an Earth–Sun analogue — so a transit survey must monitor tens or hundreds of thousands of stars.

![(a) Transit depth versus planet radius for four types of star, with the photometric precision of Kepler and TESS. (b) The signal of one atmospheric scale height in transmission for selected planets: hydrogen-rich giants give hundreds of ppm, rocky planets with nitrogen-rich air only a few ppm.](figures/out/ch39_transit.svg){#fig:obstransit width=98%}

NASA's **Kepler** (2009–18), whose 0.95 m Schmidt telescope fed a 95-megapixel camera with a 115-square-degree field (@fig:obskepler), stared at one patch of sky in Cygnus and Lyra for four years, measuring the brightness of about 150 000 stars every 30 minutes. After the second of its four reaction wheels failed in 2013, engineers used the pressure of sunlight to balance the spacecraft, and the **K2** mission observed a series of fields along the ecliptic until the propellant ran out in October 2018. Kepler showed that planets are the rule rather than the exception, that the most common planets in the Galaxy are between the sizes of Earth and Neptune — a type absent from the Solar System — and that a substantial fraction of Sun-like stars — estimates range from about one in ten to one in two — have an Earth-sized planet in the habitable zone.

![The Kepler spacecraft in a clean room at Ball Aerospace in Boulder, Colorado, in 2008, before launch. The sunshade covers the opening of the telescope tube.](figures/photos/ch39_kepler.jpg){#fig:obskepler width=40%}

The **Transiting Exoplanet Survey Satellite (TESS)**, launched in 2018, has four 10.5 cm cameras that together cover a 24° × 96° strip of sky, observing each strip for 27 days. It has covered more than 98 % of the sky, concentrating on bright, nearby stars whose planets can be followed up by JWST and by ground-based spectrographs that measure their masses. By October 2026 it had identified 8 151 candidate planets ("TESS Objects of Interest") and 1 012 confirmed planets, and it continues in its third extended mission. ESA's **CHEOPS** (2019) complements it with a 32 cm telescope that measures the radii of known planets very precisely.

::: example
**Example: can TESS find an Earth twin?**

An Earth-sized planet orbits a Sun-like star (1.0 $R_\odot$, 1.0 $M_\odot$) once a year. For a bright star TESS reaches about 60 ppm of noise in one hour of data.

1. **Depth**: $\delta = (6\,371/695\,700)^2$ = 8.4 × 10⁻⁵ = **84 ppm**.
2. **Duration** of a central transit: $T \approx (P/\pi)\,(R_\star/a)$ = (8 766 h/π) × (695 700/149.6 million) = **13.0 hours**.
3. **Noise over one transit**: 60 ppm/√13 = 16.6 ppm, giving a signal-to-noise ratio of 84/16.6 = **5.0**.
4. **Detection** conventionally needs a ratio of about 7.1, i.e. (7.1/5.0)² ≈ **2 transits** — two years of continuous observation. TESS watches most stars for only 27 days, so it essentially cannot find Earth twins; and only 0.47 % of such systems transit at all. This is the job of PLATO, which will stare at the same fields for two years or more.
5. **Around a small red dwarf** (0.2 $R_\odot$), the same planet in the habitable zone (about 0.07 AU) orbits in 14 days with a depth of **2 100 ppm**. Even with three times higher noise from the fainter star, one 1.5-hour transit gives a ratio of about 14, and TESS sees two transits per sector. This is why most small temperate planets known — and those JWST can study — orbit red dwarfs.
:::

By October 2026 the NASA Exoplanet Archive listed **6 451 confirmed planets** (@fig:obsexoplanets). Three-quarters (4 785) were found by transits, and more than half of all known planets came from Kepler and K2 (3 337). The archive passed 6 000 in September 2025, with more than 8 000 candidates awaiting confirmation. @tbl:exomissions summarises the main space missions.

![Exoplanet discoveries by year and method (NASA Exoplanet Archive, October 2026). The peaks in 2014 and 2016 are statistical validations of large batches of Kepler candidates.](figures/out/ch39_exoplanets.svg){#fig:obsexoplanets width=98%}

| Mission | Years | Method | Telescope / field | Role and status (Oct 2026) |
|---|---|---|---|---|
| CoRoT (CNES/ESA) | 2006–13 | Transit | 27 cm | First space transit survey |
| Kepler / K2 (NASA) | 2009–18 | Transit | 0.95 m, 115 deg² | Planet statistics; 3 337 planets |
| Gaia (ESA) | 2013–25 | Astrometry | 2 × 1.45 m × 0.5 m | Giant planets expected in DR4 |
| TESS (NASA) | 2018– | Transit | 4 × 10.5 cm, 2 304 deg² | Bright nearby stars; 1 012 planets |
| CHEOPS (ESA) | 2019– | Transit follow-up | 32 cm | Precise radii |
| JWST (NASA/ESA/CSA) | 2021– | Spectroscopy, imaging | 6.5 m | Atmospheres of known planets |
| Roman (NASA) | 2026– | Microlensing, coronagraph | 2.4 m, 0.28 deg² | Cold planets; >1 000 expected |
| PLATO (ESA) | 2027– | Transit | 26 × 12 cm | Earth analogues around Sun-like stars |
| Ariel (ESA) | 2029– | Spectroscopy | 1.1 × 0.7 m | Atmospheres of about 1 000 planets |
| HWO (NASA) | 2040s | Direct imaging | ≈ 6 m | Search for life on ~25 Earth-like planets |

: Space missions for finding and characterising exoplanets. {#tbl:exomissions}

### Gaia: Mapping the Galaxy

ESA's **Gaia** (2013–25) measured the positions, distances and motions of nearly two billion stars from the Sun–Earth L2 point. Two telescopes looking 106.5° apart scanned the sky as the spacecraft rotated, projecting both fields onto a focal plane of 106 CCDs with nearly a billion pixels, and the angle between stars in the two fields was measured to between about ten and a few tens of micro-arcseconds — roughly the angle covered by a coin on the Moon seen from Earth. Its **parallaxes** (the apparent annual shift of a star caused by Earth's orbit) give distances for over a billion stars; its second data release (2018) revealed, among much else, the remains of a dwarf galaxy that merged with the Milky Way about 10 billion years ago, and the third (2022) catalogued 1.8 billion sources. After more than three trillion observations, science operations ended on 15 January 2025 and the spacecraft was switched off on 27 March 2025 in a retirement orbit around the Sun. The fourth data release, based on 5.5 years of data and more than 500 TB, is scheduled for December 2026; a final release is expected around 2030.

### Mapping the Dark Universe: Euclid, SPHEREx and Roman

**Euclid** (ESA, launched July 2023) is a 1.2 m telescope with a visible imager and a near-infrared spectrometer and photometer covering a 0.53-square-degree field — more than a hundred times Hubble's main camera. Over six years it is mapping about a third of the sky to measure the shapes of more than a billion galaxies. The tiny, coherent distortions of those shapes by the gravity of intervening matter (**weak gravitational lensing**) and the three-dimensional clustering of galaxies reveal how dark matter is distributed and how dark energy has driven the expansion. Its first "quick" release in March 2025 covered 63 square degrees and 26 million galaxies; the first cosmology release is being published in two steps from November 2026.

**SPHEREx** (NASA), launched in March 2025 together with the heliophysics mission PUNCH, carries a small 20 cm telescope but splits light into 102 colours from 0.75 to 5 µm. In December 2025 it completed its first spectral map of the whole sky, the first of four planned in its two-year mission. Its goals include measuring the faint patterns that **cosmic inflation** — the very rapid expansion believed to have occurred in the first instant after the Big Bang — left in the distribution of galaxies, and surveying ices in star-forming clouds.

The **Nancy Grace Roman Space Telescope** (NASA) uses a 2.4 m mirror — the same size as Hubble's, from a telescope donated by the US National Reconnaissance Office — with a 300-megapixel Wide Field Instrument whose field is about 200 times larger than that of Hubble's infrared camera. It was launched on a Falcon Heavy on 30 August 2026, ahead of schedule, and was being commissioned on its way to L2 in October 2026, with the first science images expected in early 2027 (@fig:obsroman). Over five years Roman will map dark energy with weak lensing, supernovae and galaxy clustering, monitor the crowded centre of the Milky Way to find more than a thousand planets by **gravitational microlensing** (the brief brightening of a star when a planet passes in front of it), and test a coronagraph designed to suppress starlight by a factor of 10⁸ or more to image giant planets directly. Its lifecycle cost is about US$ 4 billion.

![The Nancy Grace Roman Space Telescope being encapsulated in the Falcon Heavy payload fairing at Kennedy Space Center on 21 August 2026, nine days before launch.](figures/photos/ch39_romanfairing.jpg){#fig:obsroman width=44%}

China's **Xuntian** (Chinese Space Station Telescope, CSST) is a 2 m survey telescope with a field of about 1.1 square degrees, planned for launch in 2027. It will fly in the same orbit as the Tiangong space station so that it can dock for servicing and upgrades. ESA's **PLATO**, with 26 small cameras on one platform, is due for launch on Ariane 6 in January 2027 to find Earth-sized planets in the habitable zones of Sun-like stars and to measure the stars' ages from their oscillations, and **Ariel** (2029) will measure the atmospheres of about a thousand known exoplanets.

## High-Energy and Time-Domain Astronomy

X-ray and gamma-ray observatories study the most violent events in the Universe, many of which last only seconds to days. Modern high-energy astronomy is therefore a **time-domain** discipline: wide-field monitors detect a flare or burst, and the observatory or its partners swing narrow-field telescopes onto it within minutes, alerting the world through the General Coordinates Network.

- **Fermi** (NASA, 2008) combines the Large Area Telescope (20 MeV to over 300 GeV), which surveys the whole gamma-ray sky every three hours and has catalogued about 7 000 sources, with a burst monitor (8 keV–40 MeV). On 17 August 2017 Fermi detected a short gamma-ray burst 1.7 seconds after the LIGO and Virgo detectors recorded gravitational waves from two merging neutron stars (GW170817), opening **multi-messenger astronomy**.
- **Swift** (NASA, 2004) could turn to a new gamma-ray burst within one to two minutes and observe it with X-ray and ultraviolet/optical telescopes, localising well over a thousand bursts. It was never designed for servicing, and the high solar activity of 2024–25 made its orbit decay much faster than predicted. NASA paid Katalyst Space US$ 30 million for a robotic spacecraft to grab Swift and raise its orbit; it was launched on a Pegasus XL on 3 July 2026, but attitude-control problems left it unable to capture Swift, and the attempt was abandoned on 19 August. On 19 October 2026 Swift was at about 280 km and descending quickly; NASA had curtailed science observations earlier in the year to slow the decay, and it was expected to re-enter within weeks.
- **NuSTAR** (NASA, 2012) was the first telescope to focus hard X-rays (3–79 keV), using a 10 m mast that unfolded in orbit to give the long focal length that grazing-incidence optics need at high energy.
- **IXPE** (NASA–Italy, 2021) measures the **polarisation** of X-rays, revealing the geometry of magnetic fields in pulsars, magnetars and black-hole jets.
- **XRISM** (JAXA with NASA and ESA, 2023) carries **Resolve**, a microcalorimeter that measures the energy of each X-ray photon from the tiny temperature rise it causes in a detector cooled to 0.05 K, giving 20–30 times finer spectral resolution than X-ray CCDs. Its protective gate valve has failed to open, which blocks X-rays below about 1.7 keV, but the instrument works superbly at higher energies and operations have been extended to 2030.
- **eROSITA**, the German telescope on the Russian–German Spektr-RG spacecraft (2019), completed four all-sky X-ray surveys before it was placed in safe mode in February 2022 after Russia's invasion of Ukraine. Its second data release (July 2026) catalogues about two million X-ray sources.
- **Einstein Probe** (Chinese Academy of Sciences with ESA, Germany and France, January 2024) uses "lobster-eye" optics, modelled on the eyes of crustaceans, to watch 3 600 square degrees of sky at once in soft X-rays, and has found many new transients; ESA has extended its participation to 2029. The Chinese–French **SVOM** (June 2024) detects gamma-ray bursts and follows up Einstein Probe alerts.

ESA's **XMM-Newton** (1999), with three large X-ray telescopes, continues alongside Chandra, giving Europe a long-lived workhorse for X-ray spectroscopy.

## The Microwave Sky, Radio Interferometry and Gravitational Waves

The **cosmic microwave background (CMB)** is light released when the Universe became transparent, 370 000 years after the Big Bang, now stretched by a factor of 1 100 into microwaves. Three missions turned its study into precision cosmology. NASA's **COBE** (1989) showed that the CMB has a perfect blackbody spectrum at 2.725 K and detected tiny temperature variations of a few parts in 100 000 — the seeds of all later structure — work recognised by the 2006 Nobel Prize in Physics. **WMAP** (2001–10) mapped those variations across the whole sky from L2, and ESA's **Planck** (2009–13) mapped them in nine frequency bands with three times better resolution. Planck's final results (2018) fixed the age of the Universe at 13.8 billion years and its composition at about 5 % ordinary matter, 27 % dark matter and 68 % dark energy, with $H_0$ = 67.4 ± 0.5 km/s/Mpc.

Radio astronomy needs no help to see through the atmosphere, but space extends the size of an interferometer. Russia's **RadioAstron** (Spektr-R, 2011–19) carried a 10 m antenna on an orbit reaching about 350 000 km and combined its signals with ground radio telescopes to form a virtual telescope almost the size of the Moon's orbit, achieving resolutions of about ten micro-arcseconds.

The next frontier is not light at all. The **Laser Interferometer Space Antenna (LISA)**, adopted by ESA in January 2024 with NASA participation and planned for launch on Ariane 6 in 2035, will fly three spacecraft in a triangle 2.5 million km on a side, measuring changes in their separations of a few picometres with lasers. It will detect low-frequency **gravitational waves** from merging supermassive black holes throughout the Universe, from compact binary stars in the Milky Way and, perhaps, from the early Universe — signals that ground-based detectors such as LIGO cannot hear.

## The Fleet in 2026 and the Road Ahead

@fig:obsgantt shows how missions have succeeded one another since 1990, and @tbl:obsfleet lists the main observatories operating or approved in October 2026. Three trends stand out. First, missions last far longer than planned: Hubble was expected to work for 15 years, Chandra for five, and both are still operating after more than a quarter of a century. Second, international partners now provide much of the capability: Europe leads Gaia, Euclid, PLATO, Ariel, LISA and NewAthena; China operates Einstein Probe and SVOM and is preparing Xuntian; Japan leads XRISM. Third, apertures grow slowly (@fig:obsapertures a) because they are limited by fairings and cost, so progress also comes from larger fields, better detectors and colder telescopes.

![Timeline of major space observatories, 1990–2040. Bars show operating life from launch; hatched bars are planned missions starting at their target launch dates.](figures/out/ch39_gantt.svg){#fig:obsgantt width=94%}

| Mission | Lead | Band | Aperture | Orbit | Launch | Status, Oct 2026 |
|---|---|---|---|---|---|---|
| Hubble | NASA/ESA | 0.115–1.7 µm | 2.4 m | LEO 470 km | 1990 | Operating, one-gyro mode |
| Chandra | NASA | 0.1–10 keV | 1.2 m | HEO | 1999 | Operating, minimum-cost |
| XMM-Newton | ESA | 0.15–15 keV | 3 × 0.7 m | HEO | 1999 | Operating |
| Swift | NASA | γ, X-ray, UV | 0.3 m (UVOT) | LEO 280 km | 2004 | Re-entry expected within weeks |
| Fermi | NASA | 8 keV–300 GeV | Detectors | LEO 490 km | 2008 | Operating; ended in 2027 request |
| NuSTAR | NASA | 3–79 keV | 2 optics | LEO 540 km | 2012 | Operating |
| TESS | NASA | 0.6–1.0 µm | 4 × 10.5 cm | Lunar resonance | 2018 | Operating, third extension |
| CHEOPS | ESA | 0.33–1.1 µm | 0.32 m | LEO 700 km | 2019 | Operating |
| eROSITA (SRG) | Germany/Russia | 0.2–10 keV | 7 × 0.36 m | L2 | 2019 | Off since 2022; data released |
| IXPE | NASA/ASI | 2–8 keV | 3 optics | LEO 530 km | 2021 | Operating |
| JWST | NASA/ESA/CSA | 0.6–28.5 µm | 6.5 m | L2 | 2021 | Operating, Cycle 5 |
| Euclid | ESA | 0.55–2.0 µm | 1.2 m | L2 | 2023 | Surveying; DR1 from Nov 2026 |
| XRISM | JAXA/NASA | 1.7–12 keV | 2 × 0.45 m | LEO 550 km | 2023 | Operating to 2030 |
| Einstein Probe | CAS/ESA | 0.3–10 keV | Lobster-eye | LEO 600 km | 2024 | Operating |
| SVOM | CNSA/CNES | γ, X-ray, optical | 0.44 m (VT) | LEO 625 km | 2024 | Operating |
| SPHEREx | NASA | 0.75–5.0 µm | 0.2 m | LEO 650 km | 2025 | Second all-sky map |
| Roman | NASA | 0.48–2.3 µm | 2.4 m | L2 | 2026 | Commissioning |
| PLATO | ESA | 0.5–1.0 µm | 26 × 0.12 m | L2 | 2027 | Launch Jan 2027 |
| Xuntian (CSST) | China | 0.25–1.0 µm | 2 m | Near Tiangong | 2027 | In development |
| Ariel | ESA | 0.5–7.8 µm | 1.1 × 0.7 m | L2 | 2029 | In development |
| PRIMA | NASA | 24–235 µm | 1.8 m | L2 | 2033 | Selected Sept 2026 |
| LISA | ESA/NASA | Gravitational waves | 3 × 0.3 m | Heliocentric | 2035 | Adopted 2024 |
| NewAthena | ESA | 0.2–12 keV | ≈ 2.5 m | L1/L2 halo | Late 2030s | Adoption 2027 |
| HWO | NASA | UV–near-IR | ≈ 6 m | L2 | 2040s | Concept studies |

: Major space observatories operating or approved in October 2026. {#tbl:obsfleet}

![(a) Primary-mirror diameter of space telescopes against launch year. (b) Survey power (étendue): collecting area multiplied by the field of view of the main camera. Wide-field survey telescopes map the sky thousands of times faster than Hubble or JWST.](figures/out/ch39_apertures.svg){#fig:obsapertures width=98%}

### New Missions

In September 2026 NASA selected **PRIMA**, a cryogenically cooled 1.8 m far-infrared telescope, as the first mission in a new **Probe** class with a cost cap of US$ 1.2 billion; it is to be launched in 2033 to study how galaxies, stars and planets form, filling the far-infrared gap left by Spitzer and Herschel. NASA is also building the UVEX ultraviolet explorer (about 2030), and Israel's ULTRASAT ultraviolet transient survey is due to be launched in 2027 on a NASA-provided launch. ESA's **NewAthena** X-ray observatory, with a large silicon-pore mirror and a microcalorimeter spectrometer, is planned for adoption in 2027 and launch in the late 2030s.

### Habitable Worlds Observatory

The US astronomy decadal survey of 2021 recommended, as NASA's next great observatory, a telescope of about 6 m that could directly image Earth-like planets around Sun-like stars and search their spectra for oxygen, water and methane. The **Habitable Worlds Observatory (HWO)** would need a coronagraph that suppresses starlight by a factor of 10¹⁰ — an Earth seen from 30 light-years is ten billion times fainter than its star and separated from it by only 0.1″ — and wavefront stability of picometres for hours. NASA is maturing these technologies and aims for a launch in the early 2040s, possibly with robotic servicing at L2. The programme's funding is uncertain: Congress provided about US$ 150 million for 2026, but the 2027 request proposed almost nothing.

### A Fragile Golden Age

In October 2026 astronomers have more capability in space than ever — JWST, Roman, Euclid, SPHEREx, XRISM and Einstein Probe all new, and Hubble and Chandra still productive. Yet the US budget requests of 2025 and 2026 proposed ending many operating missions, Hubble's and JWST's budgets are being reduced, and Swift is being lost to drag. Older observatories cost relatively little to run compared with their scientific output — typically tens of millions of dollars a year for missions that cost billions to build — so their fate depends on whether agencies and legislatures treat them as productive assets or as expenses to be cut.

::: ai
**AI in space astronomy**

Modern observatories produce more data than people can inspect. Machine learning classifies **transients**: ground surveys such as the Vera C. Rubin Observatory, which released its first images in 2025, are expected to issue millions of alerts per night, and classifiers running in "alert brokers" decide within minutes which supernovae, tidal-disruption events or X-ray counterparts deserve follow-up by Swift-like satellites. In **exoplanet vetting**, neural networks trained on Kepler light curves separate true transits from eclipsing binaries and instrumental artefacts; one such network found the eighth planet of Kepler-90 in 2017, and NASA's ExoMiner validated 301 new Kepler planets in 2021. **Galaxy morphology** is classified by deep networks trained on volunteers' labels from the Galaxy Zoo project, now being applied to Euclid's images. Neural networks also estimate photometric redshifts from colours and remove instrumental noise from JWST spectra — but their outputs must be validated, because a subtle bias can mimic a discovery (Chapter 46).
:::

::: key
**Key takeaways**

- The atmosphere blocks gamma rays, X-rays, most ultraviolet and most infrared light, blurs images and adds background; space telescopes gain wavelength coverage, diffraction-limited sharpness and photometric stability at a cost about a hundred times higher per square metre.
- NASA's four Great Observatories — Hubble, Compton, Chandra and Spitzer — covered the spectrum from gamma rays to the far infrared. Hubble (one-gyro mode, median re-entry late 2033) and Chandra (minimum-cost operations) still worked in October 2026.
- JWST (6.5 m, 0.6–28.5 µm, L2) has seen galaxies to $z$ = 14.44, only 280 million years after the Big Bang, found unexpectedly early black holes and measured exoplanet atmospheres; the K2-18 b biosignature claim remains unconfirmed.
- In flat ΛCDM, light from $z$ = 14 left its source 13.5 billion years ago; the source is now about 34 billion light-years away but was only 2.25 billion light-years away when the light left. Light-travel, comoving, angular-diameter and luminosity distances differ greatly.
- A transiting Earth dims a Sun-like star by 84 ppm for 13 hours; TESS's 27-day sectors favour planets around red dwarfs, and PLATO will hunt true Earth analogues. 6 451 exoplanets were confirmed by October 2026, three-quarters by transits.
- Survey telescopes (Gaia, Euclid, SPHEREx, Roman, Xuntian) gain power from wide fields rather than aperture; high-energy missions (Fermi, Swift, IXPE, XRISM, Einstein Probe, SVOM) work as a rapid-response network for transients.
- The future includes PLATO and Xuntian (2027), Ariel (2029), PRIMA (2033), LISA (2035), NewAthena and the Habitable Worlds Observatory, but budget threats to operating missions are serious.
:::

::: questions
**Review questions**

1. List three reasons for putting a telescope in space and, for each, one wavelength range or measurement where it is decisive.
2. What caused Hubble's spherical aberration, and why could it be corrected completely with COSTAR and new instruments?
3. Compare low Earth orbit, a highly elliptical orbit and a halo orbit around Sun–Earth L2 for an infrared telescope and for an X-ray telescope.
4. Why must X-ray telescopes use grazing-incidence mirrors, and how does this affect their size and focal length?
5. Explain why the most distant galaxies are invisible to Hubble but visible to JWST. At what redshift does the Lyman break pass 1.7 µm?
6. A galaxy has $z$ = 6. Using @tbl:cosmodist, state its look-back time, the age of the Universe when its light left, and its comoving distance. Why is the comoving distance larger than the light-travel distance?
7. Calculate the transit depth and central-transit duration of a Neptune-sized planet (3.9 Earth radii) in a 30-day orbit around a Sun-like star.
8. Why is the K2-18 b dimethyl-sulphide claim considered unconfirmed, and what would be needed to establish a biosignature?
9. Define étendue, and explain why SPHEREx, with a 20 cm telescope, can map the sky faster than JWST.
10. Discuss the arguments for and against continuing to fund old observatories such as Hubble and Chandra when new missions need money.
:::
