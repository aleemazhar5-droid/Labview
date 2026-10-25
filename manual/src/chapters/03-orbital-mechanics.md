---
title: Orbital Mechanics and Astrodynamics
hero: ch03
abstract: Orbital mechanics explains how spacecraft move under gravity. It tells us why satellites stay up, how long an orbit takes, how much velocity change a mission needs, how orbits drift because of Earth's shape and the Sun and Moon, how to rendezvous with another spacecraft, and how to travel between planets. This chapter builds the subject from Newton's and Kepler's laws to the practical tools of mission design - Hohmann transfers, plane changes, ground tracks, Lambert's problem, gravity assists and the Lagrange points - with worked examples throughout.
---

## From Newton to Kepler

### Gravity and the Two-Body Problem

Isaac Newton's law of universal gravitation states that two masses attract each other with a force proportional to the product of their masses and inversely proportional to the square of the distance between them:

$$F = \frac{G M m}{r^2}, \qquad G = 6.674\times10^{-11}\ \text{N m}^2\,\text{kg}^{-2}$$

For a satellite of negligible mass orbiting a planet of mass $M$, it is convenient to use the **gravitational parameter** $\mu = GM$, which is known far more precisely than $G$ or $M$ separately. For Earth, $\mu_\oplus = 398\,600.4418$ km³/s²; for the Sun, $\mu_\odot = 1.327\,124\times10^{11}$ km³/s². The equation of motion of the satellite relative to the planet's centre is

$$\ddot{\mathbf{r}} = -\frac{\mu}{r^3}\,\mathbf{r}$$

This is the **two-body problem**. It has an exact solution: the satellite moves on a **conic section** — a circle, ellipse, parabola or hyperbola — with the planet at one focus (@fig:conics). All the complexity of real orbits comes from small departures from this ideal, called **perturbations**.

![The four conic sections. Bound orbits are circles and ellipses; parabolas are the boundary case of escape; hyperbolas describe flybys and escape trajectories. All share the polar equation r = p/(1 + e cos ν) with the attracting body at a focus.](figures/out/ch03_conics.svg){#fig:conics width=70%}

### Kepler's Three Laws

Johannes Kepler deduced three laws from Tycho Brahe's observations of Mars, decades before Newton explained them:

1. **The orbit of a planet is an ellipse with the Sun at one focus.**
2. **A line joining the planet and the Sun sweeps out equal areas in equal times** (@fig:kepler2). Physically, this is conservation of angular momentum: the satellite moves fastest at its closest point (**periapsis**) and slowest at its farthest point (**apoapsis**).
3. **The square of the orbital period is proportional to the cube of the semi-major axis:**

$$T = 2\pi\sqrt{\frac{a^3}{\mu}}$$

![Kepler's second law: the two shaded sectors have equal area and are swept in equal times, so the satellite moves much faster near periapsis.](figures/out/ch03_kepler2.svg){#fig:kepler2 width=72%}

For Earth orbits, the words perigee and apogee are used; around the Sun, perihelion and aphelion; around the Moon, perilune (periselene) and apolune.

### The Geometry of the Ellipse

An ellipse is described by its **semi-major axis** $a$ (half the longest diameter) and **eccentricity** $e$ (how elongated it is; 0 for a circle). The orbit equation in polar form is

$$r = \frac{a(1-e^2)}{1 + e\cos\nu}$$

where $\nu$ is the **true anomaly**, the angle from periapsis to the satellite measured at the focus. The periapsis and apoapsis radii are $r_p = a(1-e)$ and $r_a = a(1+e)$ (@fig:ellipse).

![Geometry of an elliptical orbit. The central body sits at one focus; the other focus is empty. Periapsis and apoapsis lie at the ends of the major axis.](figures/out/ch03_ellipse.svg){#fig:ellipse width=86%}

### Energy and Speed: the Vis-Viva Equation

Two quantities are conserved in the two-body problem: the **specific mechanical energy** (energy per unit mass) and the **specific angular momentum**:

$$\varepsilon = \frac{v^2}{2} - \frac{\mu}{r} = -\frac{\mu}{2a}, \qquad h = |\mathbf{r}\times\mathbf{v}| = \sqrt{\mu a (1-e^2)}$$

Rearranging the energy equation gives the most useful single equation in orbital mechanics, the **vis-viva equation**:

$$v^2 = \mu\left(\frac{2}{r} - \frac{1}{a}\right)$$

It gives the speed anywhere on an orbit from the current radius and the semi-major axis alone. Special cases:

- **Circular orbit** ($r = a$): $v_c = \sqrt{\mu/r}$.
- **Escape** (parabola, $a\to\infty$): $v_{esc} = \sqrt{2\mu/r} = \sqrt{2}\,v_c$.
- **Hyperbolic excess speed** $v_\infty$ — the speed left over far from the planet: $v^2 = v_{esc}^2 + v_\infty^2$. Mission designers quote launch energy as $C_3 = v_\infty^2$ (km²/s²).

![Circular orbital speed, escape speed and orbital period as functions of altitude above Earth. At the ISS altitude a satellite circles the Earth every 92 minutes at 7.66 km/s; at GEO the period equals one sidereal day (23 h 56 min).](figures/out/ch03_speeds.svg){#fig:speeds width=88%}

::: example
**Worked example — the International Space Station's orbit**

The ISS flies at about 420 km, so $r = 6\,378 + 420 = 6\,798$ km.

- Circular speed: $v = \sqrt{398\,600/6\,798} = 7.657$ km/s (27 570 km/h).
- Period: $T = 2\pi\sqrt{6\,798^3/398\,600} = 5\,578$ s = 93.0 min, so about 15.5 orbits per day.
- Escape speed from this altitude: $\sqrt{2}\times7.657 = 10.83$ km/s, so leaving Earth from the ISS orbit would need $\Delta v = 3.17$ km/s.
:::

## Describing an Orbit: Orbital Elements and Reference Frames

### The Six Classical Orbital Elements

A satellite's position and velocity at an instant (six numbers: $\mathbf{r}$, $\mathbf{v}$) define its two-body orbit completely. An equivalent and more intuitive description uses six **Keplerian (classical) orbital elements** (@fig:elements):

| Element | Symbol | Describes |
|---|---|---|
| Semi-major axis | $a$ | Size of the orbit (and the period) |
| Eccentricity | $e$ | Shape |
| Inclination | $i$ | Tilt of the orbit plane relative to the equator (0°–180°; > 90° = retrograde) |
| Right ascension of the ascending node (RAAN) | $\Omega$ | Angle in the equatorial plane from the vernal equinox to the point where the satellite crosses the equator northward |
| Argument of periapsis | $\omega$ | Angle in the orbit plane from the ascending node to periapsis |
| True anomaly (or mean anomaly, or time of periapsis) | $\nu$ ($M$, $t_p$) | Position of the satellite on the orbit |

![The classical orbital elements. Two define the size and shape of the orbit (a, e), three its orientation in space (i, Ω, ω), and one the position of the satellite along it (ν).](figures/out/ch03_elements.svg){#fig:elements width=92%}

Some elements are undefined for special orbits: for circular orbits there is no periapsis (ω is replaced by the **argument of latitude** $u = \omega + \nu$), and for equatorial orbits there is no ascending node. For such orbits, engineers use **equinoctial elements**, which have no singularities and are preferred in numerical software and for electric-propulsion trajectory optimisation.

### Reference Frames and Time

Orbits are computed in **inertial** (non-rotating) frames, but ground stations, maps and GNSS work in **Earth-fixed** frames, and spacecraft attitude and rendezvous are described in **orbit-fixed** frames (@fig:frames):

- **Earth-centred inertial (ECI)** frames: today the **Geocentric Celestial Reference Frame (GCRF)**, closely aligned with the older **J2000** (EME2000) frame. The X-axis points to the vernal equinox, Z to the celestial north pole.
- **Earth-centred, Earth-fixed (ECEF)**: the **International Terrestrial Reference Frame (ITRF)** and its GNSS realisations (WGS 84 for GPS). It rotates with the Earth; converting to ECI requires precession, nutation, Earth rotation angle and polar motion, published by the International Earth Rotation and Reference Systems Service (IERS).
- **Orbit frames**: **RTN/RSW** (radial, transverse/along-track, normal) and **LVLH** (local vertical, local horizontal), used for relative motion, attitude pointing and orbit-determination covariance.
- **Body frame**: fixed to the spacecraft structure.

Precise work also needs precise **time scales**. These include International Atomic Time (TAI) and Coordinated Universal Time (UTC), which differs from TAI by an integer number of leap seconds (37 s since 2017). There are also GPS time (TAI − 19 s, no leap seconds), Terrestrial Time (TT = TAI + 32.184 s) and Barycentric Dynamical Time (TDB) for interplanetary ephemerides. Confusing these has caused real errors.

![Common reference frames: Earth-centred inertial and Earth-fixed frames, and the orbit-fixed radial / along-track / cross-track (RTN) frame attached to the satellite.](figures/out/ch03_frames.svg){#fig:frames width=88%}

### Two-Line Element Sets

The most widely distributed orbit format is the **two-line element set (TLE)** (@fig:tle), produced by the US Space Force for the public catalogue. TLEs are *mean* elements fitted for the **SGP4** analytical propagator. They are adequate for antenna pointing and general awareness (errors of about 1 km at epoch, growing by kilometres per day). But they are not adequate for precise conjunction assessment, which uses covariance-carrying ephemerides (Chapter 21). The fixed five-character catalogue-number field is close to exhaustion as tens of thousands of new objects are catalogued. An interim "Alpha-5" scheme replaces the first digit with a letter. So users are moving to the **CCSDS Orbit Mean-elements Message (OMM)** in XML, KVN or JSON, which has no such limit.

![Anatomy of a two-line element set (illustrative values). Each field occupies fixed columns; the last digit of each line is a checksum.](figures/out/ch03_tle.svg){#fig:tle width=98%}

## Where Is the Satellite? Kepler's Equation

Knowing the orbit is not the same as knowing where the satellite will be at a given time. Because the speed varies around an elliptical orbit, the true anomaly does not increase uniformly. Kepler solved this with two auxiliary angles (@fig:anomalies): the **mean anomaly** $M$, which does increase uniformly, $M = n(t - t_p)$ with **mean motion** $n = \sqrt{\mu/a^3}$; and the **eccentric anomaly** $E$, related to $M$ by **Kepler's equation**:

$$M = E - e\sin E$$

Given $M$, this transcendental equation is solved for $E$ by iteration (Newton's method converges in a few steps), and then

$$\tan\frac{\nu}{2} = \sqrt{\frac{1+e}{1-e}}\,\tan\frac{E}{2}, \qquad r = a(1 - e\cos E)$$

![The eccentric anomaly E is measured at the centre of the ellipse to the point on an auxiliary circle; the true anomaly ν is measured at the focus. Kepler's equation links E to the uniformly increasing mean anomaly M.](figures/out/ch03_anomalies.svg){#fig:anomalies width=82%}

Modern software usually avoids the anomalies altogether by integrating the equations of motion numerically (e.g., with Runge–Kutta or Gauss–Jackson integrators), which also allows any perturbing forces to be included. Analytical methods remain important for quick estimates, for onboard software with limited computing power, and for physical insight.

## Orbit Perturbations

Real orbits deviate from Keplerian ellipses because of additional forces. @fig:perturb compares their sizes.

![Magnitude of perturbing accelerations as a function of altitude for a typical satellite. Earth's oblateness (J₂) dominates in LEO after central gravity; drag dominates the decay of low orbits; the Sun and Moon dominate high orbits such as GEO.](figures/out/ch03_perturbations.svg){#fig:perturb width=90%}

### Earth's Oblateness (J₂)

The Earth is not a sphere: its equatorial radius (6 378.137 km) exceeds its polar radius (6 356.752 km) by 21 km. Its gravity field is expressed as a series of **spherical harmonics**; the largest term after the central field is the **J₂ zonal harmonic** ($J_2 = 1.082\,63\times10^{-3}$), about a thousand times larger than any other. The equatorial bulge exerts a torque on an inclined orbit, causing two secular drifts:

**Nodal regression** — the orbit plane precesses about Earth's axis:

$$\dot\Omega = -\frac{3}{2}\,n\,J_2\left(\frac{R_\oplus}{p}\right)^2\cos i$$

**Apsidal rotation** — the line of apsides rotates within the orbit plane:

$$\dot\omega = \frac{3}{4}\,n\,J_2\left(\frac{R_\oplus}{p}\right)^2\left(5\cos^2 i - 1\right)$$

where $p = a(1-e^2)$. For the ISS ($i = 51.6°$, 420 km), the node regresses by about 5° per day. This is why its ground track shifts each day, and why launch windows to the ISS move earlier by roughly 22 minutes per day.

These "perturbations" are put to good use in three special orbit families (@fig:j2):

- **Sun-synchronous orbits (SSO).** Choosing a slightly retrograde inclination (about 97–99° for altitudes of 500–1 000 km) makes $\dot\Omega = +0.9856°$/day, exactly matching the Earth's motion around the Sun. The orbit plane then keeps a constant angle to the Sun, so the satellite crosses each latitude at the same **local solar time** every day (e.g., Landsat at 10:00 descending node, Sentinel-2 at 10:30). This gives consistent lighting for imaging and stable thermal conditions. Dawn–dusk SSOs (06:00/18:00) are almost always in sunlight — ideal for radar satellites and solar-powered missions.
- **Critically inclined orbits.** At $i = 63.4°$ or $116.6°$, $5\cos^2 i - 1 = 0$, so the apsides do not rotate. The **Molniya** (12 h period) and **Tundra** (24 h) orbits use this to keep their apogee permanently over high northern latitudes.
- **Frozen orbits.** A suitable choice of $e$ and $\omega = 90°$ (using the J₃ harmonic) keeps the altitude profile over each latitude fixed — useful for altimetry missions such as Sentinel-3 and Jason/Sentinel-6.

![Left: nodal precession rate versus inclination for several altitudes; the dashed line marks the sun-synchronous rate. Right: inclination required for a sun-synchronous circular orbit as a function of altitude.](figures/out/ch03_j2.svg){#fig:j2 width=98%}

### Other Perturbations

- **Higher-order gravity.** Tesseral and sectoral harmonics include $J_{22}$, which is related to the ellipticity of the equator. They cause GEO satellites to drift east or west towards two stable points near 75° E and 105° W. They also cause resonances for orbits with periods that are simple fractions of a day. Precise orbit determination uses models such as EGM2008 or GGM05 to degree and order 100 or more, derived from the GRACE and GOCE missions.
- **Third-body gravity** from the Moon and Sun changes the inclination of GEO satellites by about 0.75–0.95° per year. This must be corrected by north–south station-keeping (about 45–50 m/s per year — the largest item in a GEO propellant budget).
- **Solar radiation pressure (SRP)** — sunlight carries momentum, producing a pressure of about 4.56 µN/m² on an absorbing surface at 1 AU (twice that on a perfect mirror). SRP perturbs eccentricity in GEO and is the main error source in GNSS orbit modelling; it is exploited by solar sails (Chapter 42).
- **Atmospheric drag** — dominant below about 600 km (Chapter 2).
- **Relativity, Earth tides, albedo and thermal re-radiation** — small effects that matter for centimetre-level orbits of geodetic and GNSS satellites.

## Orbital Manoeuvres

A manoeuvre changes the satellite's velocity by firing a thruster. The **velocity change** $\Delta v$ is the universal currency of mission design, because the rocket equation (Chapter 34) converts it directly into propellant mass:

$$\frac{m_{prop}}{m_0} = 1 - \exp\left(-\frac{\Delta v}{I_{sp}\,g_0}\right)$$

For chemical engines, burns are short compared with the orbital period and are treated as **impulsive** (instantaneous) changes.

### The Hohmann Transfer

The minimum-energy two-impulse transfer between two coplanar circular orbits, found by Walter Hohmann in 1925, uses an ellipse tangent to both (@fig:hohmann). The first burn at periapsis raises the apoapsis to the target radius; the second burn at apoapsis circularises:

$$\Delta v_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2r_2}{r_1 + r_2}} - 1\right), \qquad \Delta v_2 = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2r_1}{r_1+r_2}}\right)$$

The transfer takes half the period of the transfer ellipse: $t = \pi\sqrt{a_t^3/\mu}$ with $a_t = (r_1+r_2)/2$.

![The Hohmann transfer between circular orbits: a tangential burn at periapsis, a half-revolution coast on the transfer ellipse, and a tangential circularising burn at apoapsis.](figures/out/ch03_hohmann.svg){#fig:hohmann width=74%}

::: example
**Worked example — from a 300 km parking orbit to GEO**

$r_1 = 6\,678$ km, $r_2 = 42\,164$ km, so $a_t = 24\,421$ km.

- $v_{c1} = \sqrt{398\,600/6\,678} = 7.726$ km/s; speed at transfer perigee $= \sqrt{398\,600\,(2/6\,678 - 1/24\,421)} = 10.152$ km/s, so $\Delta v_1 = 2.426$ km/s.
- Speed at transfer apogee $= \sqrt{398\,600\,(2/42\,164 - 1/24\,421)} = 1.608$ km/s; $v_{GEO} = 3.075$ km/s, so $\Delta v_2 = 1.467$ km/s.
- Total: **3.89 km/s**; transfer time: $\pi\sqrt{24\,421^3/398\,600} = 18\,990$ s = **5.3 h**.

From Cape Canaveral (28.5°), the satellite must also remove its inclination. Doing this at apogee, where the speed is lowest, and combining it with the circularisation burn: $\Delta v_2 = \sqrt{1.608^2 + 3.075^2 - 2(1.608)(3.075)\cos 28.5°} = 1.83$ km/s. In practice the launcher performs the first burn (injecting into GTO) and the satellite's own engine performs the second, often split into several apogee burns. Launching from Kourou (5.2° N) saves about 0.3 km/s, which is why Kourou is favoured for GEO missions.
:::

### Bi-elliptic Transfers

A three-burn **bi-elliptic transfer** first goes beyond the target orbit. It can be cheaper than a Hohmann transfer when the radius ratio exceeds 11.94, and always is when it exceeds 15.58. But it takes much longer (@fig:bielliptic). It is rarely used for Earth orbits but illustrates that "minimum energy" depends on the constraints.

![Total Δv (normalised by initial circular speed) for Hohmann and bi-elliptic transfers. The Hohmann cost peaks at a radius ratio of 15.58; above that, a bi-elliptic transfer with a distant intermediate apoapsis is cheaper.](figures/out/ch03_bielliptic.svg){#fig:bielliptic width=84%}

### Plane Changes

Changing the orbit plane is expensive because the whole velocity vector must be rotated. A pure plane change by angle $\Delta i$ at speed $v$ costs

$$\Delta v = 2v\sin\frac{\Delta i}{2}$$

so it is best performed where the speed is lowest — at apoapsis, or at high altitude — and combined with other burns (@fig:planechange). Changing the plane of a LEO satellite by just 10° costs 1.3 km/s, more than most satellites carry. This is why the launch site latitude and launch azimuth, which set the initial inclination, are so important, and why constellations deploy separate planes from separate launches. Instead of plane changes, some constellations exploit differential nodal precession: satellites placed at slightly different altitudes drift apart in RAAN for free over months (Starlink, Planet).

![Δv needed for a plane change as a function of angle, for four orbital speeds. Plane changes are cheapest where the spacecraft moves slowest.](figures/out/ch03_plane_change.svg){#fig:planechange width=80%}

### Low-Thrust Transfers

Electric propulsion (Chapter 6) produces tiny thrust (millinewtons to a few newtons) for months. The orbit then spirals gradually; the impulsive approximation no longer applies. For a slow spiral between circular orbits, the Δv approaches the *difference in circular speeds*: $\Delta v \approx v_{c1} - v_{c2}$. This is larger than for a Hohmann transfer (4.6 km/s from LEO to GEO instead of 3.9 km/s). But the propellant efficiency is ten times higher, so far less propellant is used. The **Edelbaum equation** gives the optimal low-thrust transfer with a simultaneous plane change:

$$\Delta v = \sqrt{v_1^2 + v_2^2 - 2v_1 v_2\cos\left(\tfrac{\pi}{2}\Delta i\right)}$$

All-electric GEO satellites (Boeing 702SP, Airbus Eurostar Neo, Thales Spacebus Neo) spend four to six months raising their orbits from GTO.

## Rendezvous and Relative Motion

To dock with the ISS, a visiting vehicle must arrive at the same place at the same time with the same velocity. Rendezvous begins with **phasing**: because a lower orbit has a shorter period, a chaser in a slightly lower orbit gains on the target each revolution. When close (tens of kilometres), relative motion is described in the target's RTN frame by the linearised **Hill–Clohessy–Wiltshire (CW) equations**, valid for a circular target orbit with mean motion $n$:

$$\ddot x - 3n^2 x - 2n\dot y = 0, \qquad \ddot y + 2n\dot x = 0, \qquad \ddot z + n^2 z = 0$$

where $x$ is radial, $y$ along-track and $z$ cross-track. Their solutions produce counter-intuitive behaviour (@fig:cw): a thrust *forward* along the velocity raises the chaser, so it slows down and drops *behind*; a radial burn produces a closed loop with no net drift. Approaches are designed along the **V-bar** (target velocity vector) or **R-bar** (radial line). They include "hold points", corridors and abort trajectories that are passively safe. That is, they never collide with the target if thrusters fail.

![Relative motion of a chaser near a target in a 400 km orbit, from the Clohessy–Wiltshire solutions. Each trajectory starts from a simple initial condition and is shown for two orbits.](figures/out/ch03_cw.svg){#fig:cw width=92%}

Fast rendezvous profiles now let crews reach the ISS in about 3 hours (Soyuz and Progress since 2020) instead of the traditional 2 days; Crew Dragon typically takes 15–30 hours. Autonomous rendezvous uses relative GNSS, laser rangefinders (lidar) and cameras (Chapter 48).

## Orbit Determination

**Orbit determination (OD)** estimates a satellite's orbit from measurements. Common measurements are:

- **Range** (distance), from the two-way travel time of a radio signal or laser pulse (satellite laser ranging achieves millimetre precision);
- **Range-rate**, from the Doppler shift of the carrier signal;
- **Angles**, from antennas, optical telescopes or interferometers (e.g., Delta-DOR for deep space, Chapter 24);
- **Onboard GNSS**, which gives LEO satellites their own position to better than 10 m in real time and to centimetres after processing.

Because each measurement is noisy, OD combines many of them with a dynamical model. The **batch least-squares** method adjusts the initial state to minimise the weighted sum of squared residuals over a data arc; the **(extended) Kalman filter** updates the estimate sequentially as each measurement arrives. Both produce a **covariance matrix** — a statistical description of the uncertainty — which is essential for conjunction assessment and for planning manoeuvres. The quality of OD depends as much on the force models (drag, SRP) as on the measurements.

## Ground Tracks and Coverage

The **ground track** is the path traced on the Earth's surface by the point directly beneath the satellite. It combines the satellite's orbital motion with the Earth's rotation beneath it (@fig:groundtracks). Each successive pass of a LEO satellite crosses the equator about $360° \times T / T_{day}$ further west — about 23° for a 92-minute orbit. The maximum latitude reached equals the inclination (or 180° − i for retrograde orbits).

![Ground tracks of representative orbits: the ISS (51.6°), a sun-synchronous imaging orbit (98.2°), a 12-hour Molniya orbit that dwells over the northern hemisphere, a geostationary satellite (a fixed point) and an inclined geosynchronous orbit tracing a figure-eight.](figures/out/ch03_groundtracks.png){#fig:groundtracks width=100%}

A **repeat ground track** orbit returns over exactly the same points after an integer number of revolutions $N$ in an integer number of days $D$ ($N T = D \times T_{day,nodal}$). Landsat repeats after 233 orbits in 16 days; Sentinel-2 after 143 orbits in 10 days; Jason-3 after 127 orbits in about 9.9 days. Repeat orbits allow consistent comparison of images over time and accurate altimetry along fixed tracks.

The area a satellite can see — its **coverage** — depends on altitude and the minimum elevation angle at which a ground terminal can communicate. Coverage geometry and constellation design are covered in Chapter 11.

@tbl:orbits summarises the main Earth-orbit types.

Table: Principal Earth orbit types and their uses. {#tbl:orbits}

| Orbit | Typical altitude / shape | Inclination | Period | Main uses |
|---|---|---|---|---|
| Very low Earth orbit | 160–350 km, circular | any | 87–91 min | High-resolution imaging, technology demos, short-lived missions |
| Low Earth orbit (LEO) | 350–2 000 km | 0–90°+ | 91–127 min | Stations, EO, broadband constellations, science |
| Sun-synchronous (SSO) | 500–1 000 km | 97–99.5° | 95–105 min | Optical and radar EO, weather (polar), climate |
| Polar (non-SSO) | 700–1 400 km | ≈ 85–90° | 100–115 min | Iridium (86.4°), global coverage |
| Medium Earth orbit (MEO) | 8 000–23 300 km | 0–56° | 4.8–14 h | GNSS (≈20 000–23 200 km), O3b mPOWER (8 062 km, equatorial) |
| Geostationary (GEO) | 35 786 km, circular | 0° | 23 h 56 min | Communications, weather, missile warning, data relay |
| Inclined geosynchronous (IGSO) | 35 786 km | 30–60° | 23 h 56 min | QZSS, BeiDou IGSO, NavIC (regional navigation) |
| Molniya | 500 × 39 900 km | 63.4° | 12 h | High-latitude communications, early warning |
| Tundra | ≈ 25 000 × 46 000 km | 63.4° | 24 h | Sirius XM (formerly), QZSS (variant), Arctic comms |
| Geosynchronous transfer (GTO) | 200 × 35 786 km | launch-site dependent | 10.5 h | Transfer to GEO |
| Graveyard (super-synchronous) | GEO + ≥ 235 km | ≈ 0° | > 24 h | Disposal of GEO satellites |

## Interplanetary Trajectories

### Patched Conics and the Sphere of Influence

A spacecraft travelling to Mars is pulled by the Earth, Mars and the Sun at the same time. The **patched-conic approximation** splits the journey into segments, in each of which only one body matters, and "patches" them together at the boundary of each planet's **sphere of influence (SOI)**:

$$r_{SOI} \approx a_{planet}\left(\frac{m_{planet}}{m_{Sun}}\right)^{2/5}$$

Earth's SOI has a radius of about 925 000 km, Mars' about 577 000 km, and the Moon's (relative to Earth) about 66 000 km. A mission thus consists of a **hyperbolic departure** from Earth, a **heliocentric transfer** ellipse, and a **hyperbolic arrival** at Mars, where the spacecraft either flies by, brakes into orbit, or enters the atmosphere.

::: example
**Worked example — a Hohmann transfer from Earth to Mars**

Treating both orbits as circular and coplanar (1.000 and 1.524 AU): the transfer ellipse has $a = 1.262$ AU, so the flight time is half its period, $0.5 \times 1.262^{1.5}$ years = **259 days**. Earth's orbital speed is 29.78 km/s and the transfer perihelion speed is $29.78\sqrt{2\times1.524/2.524} = 32.73$ km/s, so the departure $v_\infty = 2.94$ km/s ($C_3 = 8.7$ km²/s²). From a 300 km parking orbit the injection burn is $\sqrt{8.7 + 2\times398\,600/6\,678} - 7.73 = 3.6$ km/s. At Mars the spacecraft arrives with $v_\infty = 2.65$ km/s. Because the planets must be correctly aligned at departure (Mars about 44° ahead of Earth), such opportunities recur only once every **synodic period** — 780 days, or about 26 months.
:::

### Lambert's Problem and Porkchop Plots

Real planetary orbits are elliptical and inclined, so mission designers solve **Lambert's problem**: find the orbit that connects position $\mathbf{r}_1$ at time $t_1$ to position $\mathbf{r}_2$ at time $t_2$. Solving it for a grid of launch and arrival dates gives a **porkchop plot** (@fig:porkchop) — contours of departure energy $C_3$ and arrival $v_\infty$ — the basic tool for choosing launch periods. The plot for the late-2026 Mars window, computed for this manual, shows a minimum $C_3$ of about 9.2 km²/s² for launch near 29 October 2026 and arrival in late August 2027. The two lobes are "Type I" (transfer angle less than 180°) and "Type II" (more than 180°) trajectories; the ridge between them is a near-180° transfer that requires a large plane change.

![Porkchop plot for Earth-to-Mars transfers in the 2026 launch opportunity. Solid blue contours: launch energy C3 (km²/s²); dashed red: arrival hyperbolic speed at Mars (km/s); dotted: time of flight.](figures/out/ch03_porkchop.svg){#fig:porkchop width=90%}

### Gravity Assists

A **gravity assist** (or swing-by) uses a close flyby of a planet to change a spacecraft's heliocentric velocity without propellant (@fig:gravityassist). In the planet's frame, the hyperbolic flyby only rotates the velocity vector by a turning angle $\delta$, with

$$\sin\frac{\delta}{2} = \frac{1}{1 + r_p v_\infty^2/\mu}$$

but in the Sun's frame the planet's orbital velocity is added before and after, so the spacecraft's speed can increase (passing behind the planet) or decrease (passing in front). Gravity assists made the Voyager "Grand Tour" possible and sent Cassini to Saturn via Venus–Venus–Earth–Jupiter. They slowed MESSENGER and BepiColombo enough to orbit Mercury. Parker Solar Probe uses them (seven Venus flybys) to approach within 6.2 million km of the Sun. Flybys can be "powered" (with a burn at periapsis, exploiting the **Oberth effect**: a burn is more effective where the speed is highest).

![Geometry of a gravity assist. Left: in the planet's frame the hyperbolic flyby rotates the excess velocity without changing its magnitude. Right: in the Sun's frame, adding the planet's orbital velocity shows a net gain in speed.](figures/out/ch03_gravity_assist.svg){#fig:gravityassist width=96%}

## Three-Body Dynamics and the Lagrange Points

When two massive bodies (such as Sun–Earth or Earth–Moon) orbit each other, a third small body moves in the **circular restricted three-body problem (CR3BP)**. In a frame rotating with the two primaries there are five equilibrium points — the **Lagrange points** L1 to L5 (@fig:lagrange). L1, L2 and L3 lie on the line through the primaries and are unstable (like a ball on a saddle). L4 and L5 form equilateral triangles with the primaries and are stable when the mass ratio is small. Jupiter's Trojan asteroids gather there.

![The Earth–Moon Lagrange points and contours of the Jacobi constant ("zero-velocity curves"), which bound the regions a spacecraft with a given energy can reach in the rotating frame.](figures/out/ch03_lagrange.svg){#fig:lagrange width=84%}

Spacecraft cannot sit exactly at an unstable point, but they can fly periodic **halo** or **Lissajous orbits** around it with small station-keeping burns (a few m/s per year):

- **Sun–Earth L1** (1.5 million km sunward) gives an uninterrupted view of the Sun and of the daylit Earth: SOHO, ACE, DSCOVR, Aditya-L1, SWFO-L1 and IMAP.
- **Sun–Earth L2** (1.5 million km anti-sunward) keeps the Sun, Earth and Moon on one side. This is ideal for cold infrared and survey telescopes: WMAP, Planck, Herschel, Gaia, JWST, Euclid and the Nancy Grace Roman Space Telescope.
- **Earth–Moon L1/L2** (about 61 000 km from the Moon) serve as relay and staging locations: China's Queqiao and Queqiao-2 relay satellites orbit near Earth–Moon L2 to support far-side landers.
- **Near-rectilinear halo orbits (NRHO)** are a family of L2 halo orbits that pass close over the lunar poles. They were tested by NASA's CAPSTONE CubeSat (2022) and were chosen for the planned Gateway station. Orion flew **distant retrograde orbits (DROs)**, very stable orbits around the Moon, on Artemis I.

The invariant manifolds of these orbits form low-energy "tubes" that connect them, enabling fuel-efficient transfers known as the **interplanetary superhighway**. The Genesis solar-wind sample-return mission and the GRAIL and CAPSTONE lunar missions used such low-energy trajectories.

## The Δv Budget

Mission designers summarise trajectories as a **Δv budget**: the list of all velocity changes the vehicle must provide, plus margins. @fig:dvmap gives approximate values for the most common legs in the Earth–Moon–Mars system.

![An approximate "Δv subway map" of the Earth–Moon–Mars system. Values are impulsive, one-way and indicative; real missions add gravity and steering losses, navigation corrections and margins. Aerobraking or aerocapture can replace most of the braking at planets with atmospheres.](figures/out/ch03_dv_map.svg){#fig:dvmap width=100%}

Table: Example Δv budget for a geostationary communications satellite (15-year life, launched to standard GTO). {#tbl:geodv}

| Item | Δv (m/s) | Notes |
|---|---|---|
| GTO → GEO (apogee raising, inclination removal from 27°) | 1 500–1 800 | Several apogee-engine burns; less from supersynchronous or low-inclination GTO |
| Station acquisition and longitude relocation | 10–30 | Drift to assigned orbital slot |
| North–south station-keeping | 45–50 per year (≈ 700 total) | Counteracts luni-solar inclination drift; often done with electric thrusters |
| East–west station-keeping | 1–5 per year | Counteracts J₂₂ longitude drift and SRP eccentricity |
| Momentum management | 5–20 | Depends on ADCS design |
| End-of-life disposal to graveyard orbit | 7–11 | ≥ 235 km above GEO (IADC guideline) |
| Margin | 3–5 % | Dispersions, contingencies |

::: key
**Key takeaways**

- Two-body orbits are conic sections; the vis-viva equation $v^2 = \mu(2/r - 1/a)$ gives the speed anywhere on an orbit, and Kepler's third law gives the period.
- Six orbital elements (a, e, i, Ω, ω, ν) describe an orbit; TLEs are mean elements for SGP4, not precise ephemerides.
- J₂ makes orbit planes precess; this enables sun-synchronous, critically inclined (Molniya/Tundra) and frozen orbits.
- Δv is the currency of mission design: LEO→GEO by Hohmann costs about 3.9 km/s; plane changes are expensive and done where speed is lowest.
- Rendezvous is governed by the counter-intuitive Clohessy–Wiltshire dynamics; orbit determination combines measurements and force models to produce states with covariance.
- Interplanetary missions are designed with patched conics, Lambert solutions and porkchop plots; gravity assists and Lagrange-point orbits extend what is possible with limited propellant.
:::

::: questions
**Review questions**

1. Use the vis-viva equation to find the speeds at perigee and apogee of a transfer orbit with perigee altitude 250 km and apogee altitude 35 786 km.
2. Calculate the period of a circular orbit at 700 km altitude.
3. List the six classical orbital elements. Which describe the orbit's size and shape, which its orientation, and which the satellite's position?
4. Why are two-line element sets unsuitable for precise collision assessment or precise pointing?
5. Explain how the Earth's *J*₂ term makes sun-synchronous orbits possible, and why such orbits are slightly retrograde.
6. Calculate the Hohmann-transfer Δv from a 300 km circular orbit to geostationary radius, ignoring the plane change. Why is the plane change usually combined with the apogee burn?
7. In the Clohessy–Wiltshire frame, what happens when a chaser spacecraft makes a small burn forward along its velocity? Why is this counter-intuitive?
8. What is a porkchop plot, and what does a mission designer read from it?
9. Describe the five Lagrange points of the Sun–Earth system and name a mission that uses L1 and one that uses L2.
:::
