---
title: Rocket Propulsion
hero: ch35
abstract: A rocket engine is a machine for throwing mass backwards as fast as possible. This chapter explains how engines and motors produce thrust and how performance is measured — specific impulse, characteristic velocity and thrust coefficient — and how a converging–diverging nozzle turns hot gas into a supersonic jet whose performance depends on altitude. It compares liquid, solid and hybrid propellants, explains the cycles that feed liquid engines, from pressure-fed thrusters to full-flow staged combustion and battery-driven pumps, and describes turbopumps, injectors, combustion instability, cooling, throttling and 3-D printing. It covers solid-motor ballistics, hybrid physics and engine testing, using the engines of 2026 as examples.
---

Every launch vehicle and almost every spacecraft moves by one principle: it carries its own propellant, releases the propellant's chemical energy as heat, and expels the hot products backwards through a nozzle at several kilometres per second. The reaction to that stream of mass is **thrust**. Engines burning liquid propellants are called **rocket engines**; those with propellant cast as a solid block are **rocket motors**.

A Super Heavy booster lights 33 Raptor engines that together produce about 80 MN — more than eight thousand tonnes-force — while a Rutherford engine on Rocket Lab's Electron weighs 35 kg and produces 25 kN. Both obey the same few equations. Chapter 34 shows how engines are combined into stages and derives the rocket equation, Chapter 36 surveys the world's launch vehicles, and Chapter 6 covers spacecraft thrusters and electric propulsion.

## How a Rocket Makes Thrust

### The Thrust Equation

Draw an imaginary boundary around an engine. Propellant enters at almost zero velocity and leaves through the nozzle exit at velocity $v_e$ with mass flow rate $\dot m$. Newton's second law says the force on the engine equals the rate at which momentum leaves the boundary, plus any unbalanced pressure force across the exit plane:

$$F = \dot m\, v_e + (p_e - p_a)\,A_e$$

The first term is the **momentum thrust**; the second, the **pressure thrust**, is positive if the gas at the exit plane (pressure $p_e$, area $A_e$) is at a higher pressure than the surrounding air ($p_a$) and negative if lower. In vacuum $p_a = 0$, so every engine produces more thrust in space than at sea level — 8 % more for the Merlin 1D, 23 % for the RS-25. Both terms together define the **effective exhaust velocity** $c = F/\dot m$, which therefore changes with altitude.

### Specific Impulse

Dividing the effective exhaust velocity by standard gravity $g_0$ = 9.806 65 m/s² gives the **specific impulse** in seconds:

$$I_{sp} = \frac{F}{\dot m\, g_0} = \frac{c}{g_0}$$

Specific impulse is the number of seconds that one kilogram of propellant can produce one kilogram-force of thrust — the "fuel economy" of a rocket. The rocket equation, $\Delta v = I_{sp}\, g_0 \ln(m_0/m_f)$ (Chapter 34), shows that the velocity a stage can deliver grows in direct proportion to it. Typical vacuum values are 250–290 s for solid motors, 310–340 s for kerosene, about 340–380 s for methane and 420–465 s for hydrogen engines. An engine's **thrust-to-weight ratio** measures how compact it is: about 35–60 for hydrogen engines and 70–185 for kerosene and methane engines.

### Characteristic Velocity and Thrust Coefficient

Two further parameters separate the work of the combustion chamber from that of the nozzle. When the flow is choked at the nozzle throat (explained below), the mass flow is fixed by the chamber pressure $p_c$ and the throat area $A_t$:

$$\dot m = \frac{p_c A_t}{c^*}, \qquad F = C_F\, p_c A_t, \qquad c = c^* C_F$$

The **characteristic velocity** $c^*$ ("c-star") depends only on the combustion gas — its temperature $T_c$, mean molar mass $\mathcal M$ and ratio of specific heats γ. It is 1 500–1 600 m/s for solid propellants, about 1 800 m/s for kerosene or methane with oxygen and 2 300–2 400 m/s for hydrogen–oxygen. The ratio of measured to theoretical $c^*$, the **c\* efficiency** (typically 95–99 %), shows how well the injector mixes and burns the propellants. The **thrust coefficient** $C_F$, typically 1.3–2.0, measures how much the nozzle amplifies the force that the chamber pressure would exert on the throat alone; it depends only on γ, the **expansion ratio** ε = $A_e/A_t$ and the ambient pressure.

## Nozzle Flow

### The Ideal Rocket

The nozzle turns heat into directed motion. For the **ideal rocket** — steady, one-dimensional flow of a perfect gas with constant γ, no friction and no heat loss — the energy equation gives the exit velocity:

$$v_e = \sqrt{\frac{2\gamma}{\gamma-1}\,\frac{R_u T_c}{\mathcal M}\left[1-\left(\frac{p_e}{p_c}\right)^{(\gamma-1)/\gamma}\right]}$$

where $R_u$ = 8 314 J/(kmol·K). Exhaust velocity therefore rises with $\sqrt{T_c/\mathcal M}$: light exhaust matters as much as a hot flame. Hydrogen–oxygen burns slightly cooler than kerosene–oxygen, but its exhaust (mean molar mass about 13.5 kg/kmol) is much lighter than kerosene's (about 23.5). With γ = 1.2 and a pressure ratio of 1 000 the formula gives 4 200 m/s for hydrogen and 3 270 m/s for kerosene. Because the bracket approaches 1 slowly, higher pressure ratios add little velocity.

### Area, Mach Number and the Throat

Subsonic gas accelerates in a narrowing duct, supersonic gas in a widening one, so a rocket nozzle converges to a **throat**, where the flow reaches exactly Mach 1, and then diverges — the **de Laval nozzle**. For γ = 1.2 the throat pressure is 56 % and the throat temperature 91 % of the chamber values, so the throat carries the highest heat load. Downstream the Mach number climbs to 3–5 (@fig:nozzleflow), following the **area–Mach relation**:

$$\frac{A}{A_t} = \frac{1}{M}\left[\frac{2}{\gamma+1}\left(1+\frac{\gamma-1}{2}M^2\right)\right]^{\frac{\gamma+1}{2(\gamma-1)}}$$

![The de Laval nozzle. (a) Area ratio needed to reach each Mach number for several values of γ, with the expansion ratios of three real engines. (b) Pressure, temperature, velocity and Mach number along a nozzle with ε = 40: pressure falls by almost half before the throat, and most of the velocity is gained within a few throat diameters downstream of it.](figures/out/ch35_nozzleflow.svg){#fig:nozzleflow width=98%}

Once the throat is **choked**, no disturbance can travel upstream, so the mass flow depends only on chamber conditions and throat area; designers size an engine by choosing $p_c$ and $A_t$ first. A simple 15° conical nozzle loses 1.7 % of thrust because the exhaust leaves at an angle (divergence factor $(1+\cos α)/2$ = 0.983); most engines use a contoured **bell nozzle** that gives the same performance at about 80 % of the cone's length.

### Expansion Ratio and Altitude

A nozzle gives its best thrust when exit pressure equals ambient pressure. If $p_e > p_a$ it is **under-expanded** and the plume balloons outwards after the exit. If $p_e < p_a$ it is **over-expanded**: the air squeezes the jet into the diamond-shaped shock pattern seen in sea-level engine tests, and the pressure term subtracts thrust. Below roughly 40 % of ambient pressure the flow **separates** from the wall inside the nozzle, and asymmetric separation produces side loads that can break it. A first-stage nozzle is therefore a compromise: it must work at sea level but spends most of its burn at altitude (@fig:altitudeisp).

With the same chamber, a nozzle of ε = 16 gives 300 s at sea level and 330 s in vacuum; a vacuum nozzle of ε = 165, like the Merlin Vacuum's, gives 364 s in space but would separate violently at sea level. Vehicles solve the problem with stages: first-stage engines use moderate expansion ratios (Merlin 1D 16, Raptor 34, RD-180 37), upper-stage engines large ones (Vinci 240, RL10B-2 280). The RL10B-2 and Vinci also have **extendible nozzles** that slide out after staging; **dual-bell** and **aerospike** nozzles, which adapt to the surrounding pressure, have been tested many times but none has yet powered an orbital launch.

![Why nozzles are sized for altitude (chamber pressure 10 MPa). (a) Specific impulse versus expansion ratio for three ambient pressures; the best ratio grows from about 12 at sea level to infinity in vacuum. (b) Isp during ascent for a sea-level nozzle (ε = 16), an intermediate one and a vacuum nozzle (ε = 165); the dashed curve is an ideal nozzle that adapts to the surroundings.](figures/out/ch35_altitude.svg){#fig:altitudeisp width=98%}

![The 27 Merlin engines of a Falcon Heavy at lift-off with NASA's Nancy Grace Roman Space Telescope on 30 August 2026. The sea-level engines are slightly over-expanded at lift-off.](figures/photos/ch35_fh27.jpg){#fig:fh27engines width=56%}

Real engines fall short of the ideal through incomplete mixing, boundary-layer losses, exhaust divergence and chemistry that lags the falling temperature. Comparing published vacuum Isp with ideal values computed for each engine's own conditions gives about 92 % for the Merlin 1D, 94 % for the RD-180, 95 % for Raptor, 97 % for the RL10B-2 and 98 % for the RS-25; solid motors lose a little more because alumina droplets lag behind the gas.

::: example
**Example: specific impulse of the RS-25 from c\* and the thrust coefficient**

The RS-25 burns hydrogen and oxygen at a mixture ratio of 6.0, with $p_c$ = 20.6 MPa and ε = 69. Its rated vacuum thrust is 2 279 kN.

1. **Characteristic velocity.** An equilibrium calculation gives a theoretical $c^*$ of 2 322 m/s; with a c\* efficiency of 99 %, $c^*$ = 2 299 m/s.
2. **Exit pressure.** With γ = 1.2 the area–Mach relation gives $M_e$ = 4.6 for ε = 69 and $p_e/p_c$ = 0.001 05, so $p_e$ = 21.6 kPa.
3. **Thrust coefficient.** In vacuum $C_F$ = 1.855 (momentum) + 0.072 (pressure term $p_e ε/p_c$) = 1.927. At sea level subtract $p_a ε/p_c$ = 0.339: $C_F$ = 1.587.
4. **Specific impulse.** $I_{sp} = c^* C_F/g_0$ = 2 299 × 1.927 / 9.807 = **452 s** in vacuum (published: 452.3 s) and 372 s at sea level (published: 366 s).
5. **Throat size.** $A_t = F/(C_F p_c)$ = 2 279 000 / (1.927 × 20.6 × 10⁶) = 0.0574 m², a throat 27 cm across. The mass flow $p_c A_t/c^*$ is **514 kg/s** — a tonne of propellant every two seconds.
:::

::: example
**Example: sizing a first-stage nozzle**

A kerosene engine must give 850 kN at sea level with $p_c$ = 10 MPa, γ = 1.2 and $c^*$ = 1 746 m/s (97 % of 1 800 m/s). To keep the nozzle short and avoid separation, choose an exit pressure of 70 kPa.

1. **Expansion ratio.** $p_c/p_e$ = 143; the isentropic relations give $M_e$ = 3.6 and **ε = 15.6**.
2. **Thrust coefficient.** Momentum term 1.685; pressure term (70 − 101.3) kPa × 15.6 / 10 MPa = −0.049; so $C_F$ = 1.636 at sea level. Since $p_e/p_a$ = 0.69 > 0.4, the flow stays attached.
3. **Throat and exit.** $A_t = F/(C_F p_c)$ = 0.0520 m² (diameter 25.7 cm); $A_e = ε A_t$ = 0.810 m² (diameter **1.02 m**).
4. **Performance.** $I_{sp}$ = 291 s at sea level and 320 s in vacuum, where thrust rises to 932 kN; the mass flow is 298 kg/s. The Merlin 1D (ε = 16, 845/914 kN, 282/311 s) is close, with slightly lower real efficiency.
:::

## Propellants

### Choosing a Combination

A good combination releases much energy per kilogram, produces light exhaust, is dense, storable, safe and cheap, and can cool the chamber. None is best at everything (@tbl:propellantperf, @fig:propperf).

**Liquid hydrogen with liquid oxygen** (LOX/LH₂) gives the highest Isp of any practical chemical combination, but hydrogen is a cryogenic liquid at 20 K with a density of only 71 kg/m³; its tanks are huge, must be insulated against boil-off, and can embrittle metals. Hydrogen powers upper stages and core stages that burn from the ground up (RS-25, Vulcain 2.1, LE-9, YF-77). Engines run fuel-rich, at O/F 5–6 instead of the stoichiometric 7.9, because lighter exhaust and smaller hydrogen tanks more than repay the lost energy.

**Kerosene with oxygen** (LOX/RP-1, a highly refined kerosene) is dense and cheap, and the fuel is stored at room temperature; its drawbacks are lower Isp and **coking** — carbon deposits in cooling channels and soot on turbines — which complicates reuse. SpaceX chills Falcon 9's oxygen well below its boiling point and its kerosene below room temperature to pack more propellant into the tanks. **Methane with oxygen** ("methalox") sits between the two: better Isp than kerosene, far denser than hydrogen, little coking, and a boiling point (112 K) close to that of oxygen (90 K), so the tanks can share a bulkhead and each propellant can pressurise its own tank with its own vapour. Methane can also be made on Mars. China's Zhuque-2 was the first methane-fuelled rocket to reach orbit, on 12 July 2023, followed by, among others, Vulcan (January 2024), New Glenn (January 2025), China's Zhuque-3 (December 2025) and, in September 2026, Starship.

**Storable hypergolic propellants** — nitrogen tetroxide (NTO) with monomethylhydrazine (MMH), unsymmetrical dimethylhydrazine (UDMH) or UH25 (UDMH with 25 % hydrazine hydrate) — ignite on contact and stay liquid at room temperature for years. They power spacecraft (Chapter 6), some upper stages and India's Vikas engine, but are highly toxic.

| Propellants | O/F | *T*~c~ (K) | *c*\* (m/s) | *I*~sp~ SL / vac (s) | Bulk density (kg/m³) | Storage |
|---|---|---|---|---|---|---|
| LOX/LH₂ | 6.0 | 3 490 | 2 305 | 382 / 456 | 361 | Both cryogenic (90 K, 20 K) |
| LOX/CH₄ | 3.6 | 3 565 | 1 823 | 307 / 372 | 833 | Both cryogenic (90 K, 112 K) |
| LOX/RP-1 | 2.6 | 3 674 | 1 793 | 300 / 361 | 1 025 | Fuel storable |
| NTO/MMH | 2.0 | 3 362 | 1 755 | 288 / 342 | 1 186 | Storable, hypergolic |
| NTO/UDMH | 2.6 | 3 426 | 1 726 | 286 / 342 | 1 174 | Storable, hypergolic |
| APCP solid | — | — | ≈ 1 550 | 242 / 268–280 | ≈ 1 800 | Cast; storable for years |

: Propellant performance. Liquid values are theoretical (shifting equilibrium, chamber pressure 6.9 MPa, sea-level Isp with optimum expansion, vacuum Isp with ε = 50), computed for this book; solid values are delivered figures of the Shuttle booster and GEM 63XL. {#tbl:propellantperf}

![Theoretical performance of liquid bipropellants versus mixture ratio. (a) Vacuum Isp peaks on the fuel-rich side of stoichiometric because lighter exhaust compensates for less heat. (b) Chamber temperature peaks near stoichiometric; running fuel-rich also keeps walls and turbines cooler. Dots mark mixture ratios typical of real engines.](figures/out/ch35_propellants.svg){#fig:propperf width=98%}

### Density versus Specific Impulse

A stage's tanks, structure and drag grow with the *volume* of its propellant, not its mass. For a fixed tank volume the total impulse is proportional to the **density impulse** $ρ\, I_{sp}$, where ρ is the bulk density of the combination. By this measure kerosene (370 kg·s/L) beats hydrogen (165 kg·s/L) by more than a factor of two, and solids (about 500 kg·s/L) do better still (@fig:densityimpulse). This is why most first stages and strap-on boosters burn kerosene, methane or solid propellant, while hydrogen is favoured for upper stages, where every second of Isp is multiplied through the rocket equation.

![The density–impulse trade. Each line shows how theoretical vacuum Isp and bulk density change as the mixture ratio varies; dots mark mixture ratios typical of real engines, and grey curves join combinations with equal density impulse.](figures/out/ch35_densityisp.svg){#fig:densityimpulse width=82%}

## Liquid-Propellant Engines

### Feeding the Chamber

Propellants must reach the injector at a pressure 20–30 % above chamber pressure, so that the injector's pressure drop isolates the feed system from chamber fluctuations. The simplest method is to pressurise the tanks with helium (**pressure-fed**). But tank wall thickness grows with pressure ($t = p r/σ$ for a cylinder of radius $r$ and allowable stress σ): a 3 m diameter aluminium-alloy tank needs walls 1.5 mm thick at 0.3 MPa but 15 mm at 3 MPa. Pressure-fed engines are therefore limited to chamber pressures of about 0.7–2 MPa and to spacecraft and small stages. Large stages keep their tanks at a few bar and raise the pressure with **turbopumps** — pumps driven by a turbine — and the way the turbine is powered defines the **engine cycle** (@fig:enginecycles, @tbl:cyclecompare).

### Engine Cycles

A **gas generator** burns a few per cent of the propellants very fuel-rich (below about 1 000 K) to drive the turbine and dumps the exhaust overboard: simple, but it costs several seconds of Isp. In an **expander** cycle the fuel, usually hydrogen, absorbs heat in the cooling jacket and then drives the turbine before being injected; nothing burns in the turbine, so failures tend to be benign and restarts easy, but the heat available limits the size of closed expanders such as the RL10 (flying since 1963) and Vinci. The **expander-bleed** variant dumps its turbine flow and allows larger engines such as Japan's 1.47 MN LE-9.

![The main liquid-engine cycles. Blue lines carry oxidiser, orange fuel, red hot gas. Gas-generator engines dump their turbine exhaust; expander engines drive the turbine with fuel heated in the cooling jacket; staged-combustion engines send all turbine exhaust into the main chamber; electric-pump engines use battery-powered motors.](figures/out/ch35_cycles.svg){#fig:enginecycles width=94%}

In **staged combustion**, a **preburner** burns all of one propellant with a little of the other, and the hot gas drives the turbine and then flows into the main chamber, so nothing is wasted. The Soviet Union pioneered the **oxidiser-rich** version — the RD-253 (1965), NK-33 and the RD-170 family, including the RD-180 and RD-191 — which needs special alloys because hot oxygen attacks most metals; the YF-100, BE-4 and Archimedes use it too. The RS-25 uses the **fuel-rich** version, with one preburner for each turbopump. **Full-flow staged combustion** (FFSC) passes *all* of both propellants through turbines — a fuel-rich preburner drives the fuel pump and an oxygen-rich one the oxygen pump — giving cooler turbines and no need for a seal between fuel-rich gas and oxygen on one shaft. After Soviet and US ground demonstrators, SpaceX's Raptor, first flown in 2019, became the only FFSC engine to fly; Raptor 3 runs at about 33 MPa, the highest chamber pressure of any flying engine.

Rocket Lab's Rutherford replaces the turbine with two brushless electric motors of about 37 kW each, spinning near 40 000 rpm on lithium-polymer batteries. The pumps are simple and easy to control, but battery mass grows with power and burn time, so the **electric-pump** cycle suits only small engines; Electron's second stage even jettisons spent batteries in flight.

| Cycle | What drives the turbine | Typical *p*~c~ (MPa) | Strengths | Weaknesses | Examples |
|---|---|---|---|---|---|
| Pressure-fed | No turbine: tank pressure | 0.7–2 | Simplest; easy restarts | Heavy tanks; low Isp | Spacecraft engines, AJ10, Aestus |
| Gas generator | Small fuel-rich combustor; exhaust dumped | 5–12 | Simple, easy to develop | Wastes a few per cent of flow | Merlin, F-1, Vulcain 2.1, CE-20 |
| Expander (closed / bleed) | Fuel heated in the cooling jacket | 4–6 / ≈ 10 | Benign failures; restartable | Heat pickup limits size | RL10, Vinci; LE-9, BE-3U |
| Staged combustion | Preburner gas, then main chamber | 10–27 | High Isp and pressure | Complex; hot oxygen (ox-rich) | RD-180, BE-4, YF-100; RS-25 |
| Full-flow staged comb. | Two preburners; all flow through turbines | 30–33 | Cooler turbines; no interpropellant seal | Most complex | Raptor |
| Electric pump | Battery and electric motors | Low (not published) | Simple; precise control | Battery mass | Rutherford |

: Liquid-engine cycles compared. {#tbl:cyclecompare}

::: figrow
![A complete F-1 engine, 5.8 m tall. Five of these gas-generator engines powered each Saturn V first stage; the turbopump and turbine exhaust manifold are visible on the side of the tube-wall chamber.](figures/photos/ch35_f1.jpg){#fig:f1engine}

![Space Shuttle main engine No. 1 being fitted with a new turbopump at the Kennedy Space Center in June 2010. The staged-combustion powerhead sits above the nozzle, which is covered in blue.](figures/photos/ch35_ssme.jpg){#fig:ssmeprocessing}
:::

### Turbopumps

Pump power is $P = \dot m\,Δp/(ρ\,η)$, where $Δp$ is the pressure rise and η the efficiency, so light hydrogen is expensive to pump. Raising the RS-25's 73 kg/s of hydrogen (71 kg/m³) by about 40 MPa at 75 % efficiency needs about 55 MW — close to the 53 MW (71 140 hp) rating of its high-pressure fuel turbopump, which spins at about 35 000 rpm (@fig:ssmeprocessing). 
At the pump inlet the danger is **cavitation**: if the local pressure falls below the propellant's vapour pressure, bubbles form and collapse, destroying performance and eroding blades. The margin is the **net positive suction head** (NPSH), the excess of inlet pressure over vapour pressure expressed as a height of liquid. Designers provide it with tank pressure, subcooled propellants, **inducers** (helical impellers that tolerate some cavitation) and, on the RS-25, low-pressure boost pumps.

### Injectors and Combustion Instability

The **injector** atomises and mixes the propellants through hundreds or thousands of holes. Kerosene engines often use **impinging** jets; hydrogen engines use **coaxial** elements in which fast hydrogen gas shears a central stream of liquid oxygen (the RS-25 main injector has 600); Russian engines favour **swirl** elements; and Merlin, like the Apollo lunar descent engine, uses a single central **pintle** that throttles well. A good injector releases 96–99 % of the theoretical energy.

The chamber is also an organ pipe. If heat release couples with a pressure wave, the wave grows until it destroys the engine. Low-frequency instability ("chugging") couples with the feed system — or with the whole vehicle's structure, when it is called **pogo** — while high-frequency acoustic instability ("screech") is the most destructive. In a chamber about 1 m across, where sound travels at about 1 100 m/s, the first transverse (tangential) mode lies near 650 Hz. Cures include **baffles** that divide the injector face, acoustic cavities that absorb the dangerous frequencies, and changes to the injection pattern.

::: history
**Taming the F-1**

The F-1, which produced 6.8 MN at sea level, remains the most powerful single-chamber liquid engine ever flown. In June 1962 one destroyed itself on the test stand through high-frequency instability. Rocketdyne and NASA spent more than three years and about 2 000 full-scale tests on injector and baffle variants, setting off small charges inside the running chamber to trigger instability. The final design, with copper baffles and a modified injection pattern, damped such disturbances within about 45 ms. No F-1 failed in flight: 65 engines powered 13 Saturn V launches.
:::

### Cooling

Near the throat of a high-pressure engine the heat flux exceeds 100 MW/m², about a thousand times that of a kitchen hot-plate, and the gas is hotter than any structural metal can survive. In **regenerative cooling** the fuel flows through channels in the wall before injection, returning the heat to the chamber; modern chambers use copper alloys with milled channels, while the RS-25 nozzle is made of 1 080 brazed tubes (@fig:sts93tubes). **Film cooling** protects the wall with a layer of fuel or, on Vulcain 2, re-injected turbine exhaust; **ablative** walls char and erode slowly; **radiation-cooled** nozzle extensions of niobium alloy or carbon–carbon (Merlin Vacuum, RL10B-2) glow and radiate their heat to space; and **dump cooling** passes a little fuel through the wall of a nozzle extension and out of its exit.

![Coolant tubes inside main engine No. 3 of Space Shuttle Columbia after STS-93 in July 1999. A pin ejected from the injector at ignition punctured three tubes; the resulting hydrogen leak made the engines shut down 0.16 s early, leaving Columbia about 5 m/s short.](figures/photos/ch35_tubes.jpg){#fig:sts93tubes width=44%}

### Ignition, Throttling and Restart

Merlin is ignited by **TEA–TEB**, a mixture of triethylaluminium and triethylborane that bursts into green flame on contact with oxygen; each start consumes a dose, so the supply carried limits restarts. The RS-25, RL10 and Raptor use electrically ignited **torch igniters**, and hypergolic engines need no igniter at all. Restarting in space also needs settled propellant (Chapter 6), chill-down of pumps and lines and careful sequencing; if too much propellant accumulates before ignition, a **hard start** can damage the engine. **Throttling** limits loads near maximum dynamic pressure and makes landing possible; it requires enough injector pressure drop at low thrust to avoid instability. The RS-25 throttles between 67 % and 109 % of rated thrust, the BE-4 between 40 and 100 % and the RD-191 between 27 and 105 %.

### Additive Manufacturing

Rocket engines suit **additive manufacturing** (metal 3-D printing): they are built in small numbers from costly alloys with complex internal passages. Laser powder-bed fusion now produces injectors, chambers with integral cooling channels (including NASA's GRCop copper alloys), manifolds and pump housings in one piece instead of dozens of brazed parts. Rutherford is mostly printed; Raptor still uses printed parts, and Raptor 3 moved much of its plumbing into the engine's main structure; and up to half of Prometheus by mass is printed, part of its aim to cost a tenth as much as Vulcain 2. Porosity, rough passages and uncertain fatigue life mean printed parts still need extensive testing.

![Engineers at NASA's Marshall Space Flight Center prepare a 3-D printed turbopump for a test in 2016. At full power it pumped 2.3 m³ of liquid methane per minute, enough for an engine of about 156 kN.](figures/photos/ch35_amturbo.jpg){#fig:amturbopump width=46%}

## Engines of 2026

@tbl:enginespecs and @fig:enginemap compare the main engines of 2026. Chamber pressures have risen from about 7 MPa for the F-1 to 33 MPa for Raptor 3, making engines smaller for their thrust; methane has become the fuel of new reusable boosters in the United States, China and Europe; and thrust-to-weight ratios of 140–185 for the newest kerosene and methane engines, against about 54 for the RS-25, show the weight penalty of pumping hydrogen.

Several engines changed status in 2025–26. Raptor 3 first flew on Starship Flight 12 on 22 May 2026. Blue Origin is raising the BE-4 to about 2.85 MN with subcooled propellants, but a New Glenn booster exploded in a pre-launch hot fire on 28 May 2026 (@tbl:propfailures). India hot-fired the CE-20 at an uprated 22 tonnes-force in 2026, Prometheus awaits hop tests on Europe's Themis demonstrator, and Rocket Lab moved the first launch of Neutron, with its Archimedes engines, to 2027 after problems with a composite tank.

| Engine | Cycle | Propellants | Thrust SL / vac (kN) | *I*~sp~ vac (s) | *p*~c~ (MPa) | T/W |
|---|---|---|---|---|---|---|
| Merlin 1D (US) | GG | LOX/RP-1 | 845 / 914 | 311 | 9.7 | ≈ 180 |
| Raptor 2 (US) | FFSC | LOX/CH₄ | 2 256 / — | ≈ 347 | 30 | 141 |
| Raptor 3 (US) | FFSC | LOX/CH₄ | 2 452 / — | ≈ 350 | 33 | 164 |
| RS-25 (US) | SC fuel-rich | LOX/LH₂ | 1 859 / 2 279 | 452 | 20.6 | 54 |
| BE-4 (US) | SC ox-rich | LOX/CH₄ | 2 450 → 2 850 | — | 13.4 | — |
| BE-3U (US) | Exp. bleed | LOX/LH₂ | — / 711 → 890 | — | — | — |
| RL10B-2 (US) | Expander | LOX/LH₂ | — / 110 | 465.5 | 4.4 | ≈ 37 |
| RD-180 (RU) | SC ox-rich | LOX/RP-1 | 3 830 / 4 150 | 338 | 26.7 | 71 |
| RD-191 (RU) | SC ox-rich | LOX/RP-1 | 1 920 / 2 090 | 337 | 25.8 | 85 |
| Vulcain 2.1 (EU) | GG | LOX/LH₂ | — / ≈ 1 370 | ≈ 432 | 11.7 | — |
| Vinci (EU) | Expander | LOX/LH₂ | — / 180 | 457 | 6.0 | ≈ 33 |
| Prometheus (EU) | GG | LOX/CH₄ | ≈ 980 | — | 10 | — |
| YF-100 (CN) | SC ox-rich | LOX/RP-1 | 1 200 / 1 340 | 335 | 18 | — |
| YF-77 (CN) | GG | LOX/LH₂ | 518 / 700 | 428 | 10.1 | — |
| TQ-12 (CN) | GG | LOX/CH₄ | 658 / 745 | 337 | 10.1 | — |
| LE-9 (JP) | Exp. bleed | LOX/LH₂ | — / 1 471 | 426 | 10 | ≈ 62 |
| Rutherford (NZ) | Electric pump | LOX/RP-1 | 25 / 26 | 343 | — | ≈ 73 |
| Archimedes (US) | SC ox-rich | LOX/CH₄ | 730 / 890 | ≈ 365 | 10 | — |
| Vikas (IN) | GG | NTO/UH25 | 737 / 821 | 293 | 5.85 | — |
| CE-20 (IN) | GG | LOX/LH₂ | — / ≈ 200 | 442 | 6.0 | ≈ 35 |

: Launch-vehicle engines in 2026. GG = gas generator, SC = staged combustion, FFSC = full-flow staged combustion. Raptor Isp: vacuum value of the sea-level engine; Rutherford and Archimedes vacuum figures: vacuum versions; arrows: uprating announced in 2025. T/W from sea-level thrust where available, otherwise vacuum thrust; "—" not published. CN China, EU Europe, IN India, JP Japan, NZ New Zealand, RU Russia. Sources: manufacturers and agencies, checked October 2026. {#tbl:enginespecs}

![Launch-vehicle engines of 2026. (a) Thrust and vacuum specific impulse; marker shape gives the propellant, colour the cycle. (b) Chamber pressure: most staged-combustion engines run two to three times higher than gas-generator engines, although the methane-fuelled BE-4 and Archimedes use moderate pressures.](figures/out/ch35_enginemap.svg){#fig:enginemap width=96%}

## Solid Rocket Motors

### Anatomy

A solid motor is a pressure vessel filled with propellant. The **case** — steel or, increasingly, carbon-fibre composite — is lined with rubbery insulation, and the propellant **grain** is cast inside it around a shaped mandrel that leaves an internal channel. An **igniter** fires hot gas down the channel, and the burning surface advances until it reaches the insulation. The ablative **nozzle**, with a graphite or carbon–carbon throat, is often partly submerged in the case and mounted on a flexible bearing for steering.

Large motors use **ammonium perchlorate composite propellant** (APCP): ammonium perchlorate oxidiser and aluminium powder in a rubbery binder. The Shuttle boosters used 69.8 % ammonium perchlorate, 16 % aluminium, 12 % PBAN binder, 2 % epoxy curing agent and 0.2 % iron oxide catalyst; newer motors use an HTPB binder. Solids are dense, store for years and give enormous thrust from a simple structure, but have lower Isp, exhaust containing hydrogen chloride, no shut-down once lit, and the danger that a crack or void over-pressurises the case.

### Burn Rate and Chamber Pressure

The burning surface recedes at a rate that depends mainly on pressure, following **Saint-Robert's law** $r = a\,p_c^{\,n}$, where $a$ depends on the propellant and its temperature and the exponent $n$ is typically 0.3–0.5. Gas is produced at $ρ_p r A_b$ ($ρ_p$ the propellant density, $A_b$ the burning area) and leaves through the nozzle at $p_c A_t/c^*$. Equating the two gives the chamber pressure:

$$p_c = \left(a\,ρ_p\,c^*\,K_n\right)^{1/(1-n)}, \qquad K_n = A_b/A_t$$

The equilibrium is stable only if $n < 1$ (@fig:srmequil): a small rise in pressure then increases the nozzle outflow more than the gas production, so the pressure falls back. The exponent $1/(1-n)$ also amplifies any change in burning area. With $n$ = 0.35, a 10 % increase in $K_n$ — from a crack, a debond or the grain geometry — raises the pressure by 16 %; with $n$ = 0.7, by 37 %. Designers therefore choose low-exponent propellants and inspect grains for voids by X-ray tomography. Burn rate also rises with grain temperature.

![Solid-motor ballistics. (a) Gas generated by the grain and gas discharged through the nozzle balance at the operating point, which is stable because n < 1. (b) Equilibrium pressure versus the ratio of burning area to throat area; a high pressure exponent makes the motor sensitive to small changes in burning area.](figures/out/ch35_srmequil.svg){#fig:srmequil width=98%}

::: example
**Example: equilibrium pressure and thrust of a solid motor**

A motor has $A_t$ = 0.10 m² and $A_b$ = 32 m² ($K_n$ = 320). The propellant has $ρ_p$ = 1 770 kg/m³, $c^*$ = 1 550 m/s and $n$ = 0.35, and burns at 7 mm/s at 7 MPa, so $a = 0.007/(7\times10^6)^{0.35}$ = 2.81 × 10⁻⁵ in SI units.

1. **Pressure.** $a ρ_p c^* K_n$ = 2.81 × 10⁻⁵ × 1 770 × 1 550 × 320 = 24 700; raised to the power 1/(1 − 0.35) = 1.538, this gives $p_c$ = **5.73 MPa**.
2. **Burn rate and mass flow.** $r = a p_c^{\,n}$ = 6.53 mm/s; $\dot m = ρ_p r A_b$ = 370 kg/s, equal to $p_c A_t/c^*$, as it must be.
3. **Thrust.** With a sea-level $C_F$ of 1.55, $F = C_F p_c A_t$ = **0.89 MN** and $I_{sp}$ = 245 s.
4. **Burn time and margin.** A neutral grain with a 0.40 m web burns for 0.40/0.006 53 ≈ **61 s**; a crack adding 10 % burning area would raise $p_c$ to 6.63 MPa.
:::

### Grain Geometry

A solid motor cannot be throttled, so its thrust history is designed into the grain. The burning surface advances at the same rate everywhere; if its area grows, thrust rises (**progressive**), if constant it is **neutral**, if it shrinks **regressive** (@fig:graingeometry). An internal tube burns progressively; stars, wagon wheels and slotted grains are nearly neutral; combined shapes give high lift-off thrust followed by a lower sustain level. The Shuttle boosters' forward segment had an 11-point star that burned away early, cutting thrust by about a third through the period of maximum aerodynamic pressure.

![Grain geometry sets the thrust history. Top: cross-sections with burn-back contours every 5 cm of web, computed by tracing the advancing burning surface. Bottom: thrust versus time for each grain with the same size and propellant. The internal tube rises, the external-burning rod falls, and the star leaves slivers that burn out slowly.](figures/out/ch35_grains.svg){#fig:graingeometry width=92%}

### Segmented and Monolithic Boosters

The largest motors are built from **segments** joined at the launch site by **field joints** sealed with O-rings. On 28 January 1986, at about 2 °C, cold O-rings in the aft field joint of Challenger's right booster failed to seal; hot gas escaped, breached the external tank, and the vehicle broke up 73 s after lift-off, killing all seven crew. The redesigned joint added a capture feature, a third O-ring and heaters.

NASA's Space Launch System uses five-segment boosters, each producing about 16 MN — together more than 75 % of lift-off thrust — for 126 s. The first composite-cased Booster Obsolescence and Life Extension (BOLE) motor ran for more than two minutes on 26 June 2025, but its nozzle suffered an anomaly near the end of the burn (@fig:boletest). Europe uses **monolithic** carbon-fibre motors: the P120C serves Ariane 6 and Vega-C, and the larger P160C first flew on Ariane 6 in June 2026. Vulcan's GEM 63XL boosters lost a nozzle in October 2024 and suffered an apparent burn-through in February 2026, after which the US Space Force paused national-security launches on Vulcan; an improved motor was static-fired in April 2026, and Vulcan had not flown again by mid-October 2026 (@tbl:solidmotors). A large solid motor cannot be switched off; range safety destroys it by splitting the case.

| Motor (vehicle) | Propellant (t) | Max thrust (kN) | *I*~sp~ vac (s) | Burn (s) | Case |
|---|---|---|---|---|---|
| SLS five-segment booster | ≈ 726 | ≈ 16 000 | — | 126 | Steel, 5 segments |
| Shuttle SRB (1981–2011) | ≈ 500 | ≈ 14 700 | 268 | 123 | D6AC steel, 4 segments |
| S200 (LVM3) | ≈ 205 | 5 150 | 274.5 | ≈ 130 | Maraging steel, 3 segments |
| P160C (Ariane 6, 2026) | 156 | ≈ 4 780 | — | — | Carbon fibre, monolithic |
| P120C (Ariane 6, Vega-C) | ≈ 142 | ≈ 4 500 | — | ≈ 135 | Carbon fibre, monolithic |
| GEM 63XL (Vulcan) | 47.9 | 2 061 | 280 | 87 | Carbon fibre, monolithic |

: Large solid rocket motors. Values are rounded; "—" = not published. {#tbl:solidmotors}

![Northrop Grumman and NASA fire the BOLE five-segment demonstration motor horizontally at Promontory, Utah, on 26 June 2025.](figures/photos/ch35_bole.jpg){#fig:boletest width=60%}

## Hybrid Rockets

A **hybrid rocket** stores a liquid or gaseous oxidiser — nitrous oxide, oxygen or hydrogen peroxide — in a tank and a solid fuel, usually a rubber such as HTPB or a wax, in the chamber. The oxidiser flows down a port in the fuel grain; fuel vaporises from the surface and burns in a flame within the boundary layer. With oxidiser and fuel kept apart, hybrids are safe to store, can be throttled and restarted with the oxidiser valve, and tolerate cracks in the grain.

Because the flame is fed by heat transferred through the boundary layer, the fuel **regression rate** depends not on pressure but on the oxidiser mass flux $G = \dot m_{ox}/A_{port}$: $r = a\,G^{\,n}$, with $n$ ≈ 0.5–0.8. HTPB regresses at only about 0.5–2 mm/s, several times slower than a solid propellant burns (@fig:hybridregression), so hybrids need long grains or several ports, which waste volume and leave unburnt slivers. Paraffin-based fuels, which form a thin liquid layer that sheds droplets into the flow, regress about three times faster. As the port widens the oxidiser flux falls, so even with constant oxidiser flow the **mixture ratio shifts**: O/F varies as $r_{port}^{\,2n-1}$, drifting upwards by about 20 % in a 40 s burn for typical exponents.

![Hybrid rocket physics. (a) Regression rate versus oxidiser mass flux for HTPB and paraffin fuels, compared with a typical solid propellant. (b) Mixture ratio during a 40 s burn with constant oxidiser flow through one circular port; only for n = 0.5 would it stay constant.](figures/out/ch35_hybrid.svg){#fig:hybridregression width=98%}

Hybrids have flown on SpaceShipOne and SpaceShipTwo, whose RocketMotorTwo burned nitrous oxide with a rubber and later a polyamide fuel (Chapter 9), and on Nammo's Nucleus sounding rocket (hydrogen peroxide and HTPB), which reached about 107 km in 2018. Australia's Gilmour Space built its Eris orbital launcher around Sirius hybrids burning hydrogen peroxide with a 3-D printed fuel grain, four of about 115 kN each on the first stage. Eris's first flight failed about 14 s after lift-off on 30 July 2025; a second is expected around the end of 2026.

![A hybrid rocket motor developed by Sierra Nevada Corporation for the Dream Chaser spaceplane, firing near San Diego in 2010. It was fired three times in one day to demonstrate restarts.](figures/photos/ch35_hybrid.jpg){#fig:hybridfiring width=52%}

## Testing and Qualification

### Test Stands and Campaigns

Engines are developed by testing: combustion stability, turbopump dynamics and chamber life cannot yet be predicted well enough to skip hot fire. A programme moves from component tests — injector elements, preburners, a turbopump on a "powerpack" rig — to complete engines, stages and often the whole vehicle on the pad. Development engines are run beyond their limits.

NASA's **Stennis Space Center** in Mississippi tested every Space Shuttle main engine and tests the RS-25s for SLS: its Fred Haise (A-1) stand certified the new production RS-25 in 2023, running it at up to 113 % power, and a January 2026 hot fire cleared engine 2063 for Artemis IV, while the B-2 stand fired the complete SLS core stage in 2021 (shown under the chapter title). SpaceX's **McGregor** site in Texas has about a dozen stands on which Merlin and Raptor engines are fired before delivery. At the German Aerospace Center's **Lampoldshausen** site the P5 stand tests Vulcain 2.1, P4.1 tests Vinci under simulated altitude conditions, and P5.2 fires the complete Ariane 6 upper stage. Upper-stage engines with large nozzles are fired in **altitude-simulation** facilities, vacuum chambers in which the exhaust, passing through a diffuser, helps hold the low pressure (@fig:merlinstand, @fig:rl10chamber).

::: figrow
![A Merlin engine mounted on a test stand at SpaceX's McGregor facility in Texas, where engines are hot-fired before they fly.](figures/photos/ch35_merlintest.jpg){#fig:merlinstand width=86%}

![An RL10 in the vacuum test chamber at Aerojet Rocketdyne's West Palm Beach facility, Florida, in 2016. It was one of two engines built for the Centaur upper stage of the Atlas V that would launch Starliner's crewed flight test.](figures/photos/ch35_rl10.jpg){#fig:rl10chamber width=77%}
:::

**Qualification** shows that a design meets its requirements with margin: engines are run for several times their mission duration, at the corners of the allowed ranges of thrust, mixture ratio and inlet conditions, and through many starts. The RS-25 has accumulated more than 1.1 million seconds of hot fire. Every flight engine then passes an **acceptance test** to catch defects.

### Engine-Out and Failure Modes

Clustering allows engine-out survival: Falcon 9 lost an engine on the CRS-1 mission in October 2012 and still delivered Dragon to orbit; on Starship Flight 12 one of 33 Raptor 3s shut down early during ascent, yet the vehicle still reached its planned trajectory. Controllers shut an engine down when a **redline** — a limit on pressure, temperature, speed or vibration — is crossed, and many vehicles are held down for a few seconds after ignition so that a fault can stop the launch (@tbl:propfailures).

| Event | What happened | Consequence or lesson |
|---|---|---|
| F-1 development, 1962–65 | High-frequency combustion instability destroyed engines on the stand | Baffles, injector redesign, bomb tests |
| Challenger, 28 Jan 1986 | Cold O-rings let hot gas escape from a booster field joint | Joint redesign; temperature limits; decision-making reform |
| STS-93, 23 Jul 1999 | Injector pin punctured three nozzle coolant tubes | Hydrogen leak; main engines shut down early |
| Falcon 9 Starlink 9-3, Jul 2024 | Oxygen leak chilled the Merlin Vacuum; hard start at relight | Satellites left in a 135 km perigee orbit and lost |
| Vulcan, Oct 2024 and Feb 2026 | GEM 63XL nozzle lost; later an apparent burn-through | National-security flights paused; nozzle improved |
| New Glenn, 28 May 2026 | Booster exploded during pre-launch hot fire | Traced to the main oxygen valve of one BE-4 |

: Propulsion failures that changed engineering practice. {#tbl:propfailures}

## Beyond Chemical Propulsion

Chemical rockets are limited by the energy stored in their propellants: hydrogen and oxygen release about 13 MJ per kilogram, which in practice caps vacuum Isp near 470 s. Missions that need large velocity changes over months use **electric propulsion**, which accelerates ions or plasma to 15–50 km/s at tiny thrust (Chapter 6); nuclear thermal rockets, solar sails and other advanced concepts are covered in Chapter 42. 

::: ai
**AI in rocket propulsion**

Combustion instability suits machine learning because it is hard to predict from first principles but leaves signatures in pressure data. Researchers at DLR and the University of Cambridge trained Bayesian neural networks on pressure signals from a hydrogen–oxygen research combustor and forecast the onset of instability about half a second ahead — early enough for a controller to react. Engine teams also use machine-learning surrogates of slow simulations and anomaly detection on hot-fire data. **Computational engineering** tools generate whole engine geometries from requirements: in December 2024 the Dubai company LEAP 71 hot-fired a 5 kN kerosene–oxygen aerospike designed largely by its software and printed in copper. Chapter 52 discusses AI in design and manufacturing; certification still rests on hot fire.
:::

::: key
**Key takeaways**

- Thrust is $\dot m v_e + (p_e - p_a)A_e$; specific impulse $F/(\dot m g_0)$ measures propellant efficiency, while $c^*$ and $C_F$ separate the performance of the chamber from that of the nozzle.
- A de Laval nozzle chokes at the throat, so $\dot m = p_c A_t/c^*$; exhaust velocity grows with $\sqrt{T_c/\mathcal M}$, which is why hydrogen engines reach 420–465 s.
- Nozzles are sized for altitude: sea-level engines use expansion ratios of about 15–40 to avoid flow separation, vacuum engines 60–280.
- Propellants trade Isp against density, storability and handling; dense propellants suit first stages, hydrogen upper stages, and methane has become the fuel of new reusable boosters.
- Engine cycles differ in how they drive the turbopumps: gas generators are simple, expanders benign, staged combustion efficient; full-flow Raptor 3 reaches 33 MPa.
- A solid motor settles at $p_c = (aρ_p c^* K_n)^{1/(1-n)}$; grain shape sets its thrust history and a low exponent keeps it tolerant of defects. Hybrids are safe and throttleable but regress slowly and shift mixture ratio.
- Engines are proven by hot fire, from components to whole vehicles, with margins found by exceeding limits.
:::

::: questions
**Review questions**

1. Write the thrust equation and explain why an engine gives more thrust in vacuum than at sea level. By how much does the RS-25's thrust rise from sea level to vacuum?
2. A combustion gas has $c^*$ = 1 800 m/s and the nozzle a vacuum $C_F$ of 1.85. What is the vacuum Isp? For $p_c$ = 10 MPa and a thrust of 1 MN, what throat diameter is needed?
3. Using the exit-velocity formula, explain why hydrogen–oxygen gives a higher Isp than kerosene–oxygen although its flame is cooler.
4. What happens to the flow in an over-expanded nozzle, and why do first-stage engines not use the large nozzles of upper-stage engines?
5. Using density impulse, explain why most first stages burn kerosene, methane or solid propellant while many upper stages burn hydrogen.
6. Compare the gas-generator, expander and staged-combustion cycles. Why is the closed expander limited to engines of a few hundred kilonewtons?
7. What is NPSH, and how do designers prevent cavitation at a pump inlet?
8. A solid motor with n = 0.4 runs at 6 MPa. A debond increases the burning area by 15 %. Estimate the new chamber pressure and explain why a high pressure exponent is dangerous.
9. Why does the mixture ratio of a hybrid drift during the burn, and how do paraffin fuels help with the low regression rate of HTPB?
:::
