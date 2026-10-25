---
title: Advanced Propulsion
hero: ch42
abstract: Chemical rockets have reached the limit set by the energy stored in their propellants, so travelling faster or farther needs another source of energy or a way to avoid carrying propellant at all. It shows, with worked numbers, why exhaust velocity and power decide every advanced concept. It covers high-power Hall and ion thrusters and the power-limited trajectories they fly; nuclear thermal rockets from NERVA to the cancelled DRACO; space fission reactors and NASA's SR-1 Freedom nuclear-electric mission planned for 2028; solar, electric and laser sails, including Breakthrough Starshot; fusion and antimatter; scramjets and rotating detonation engines; and tethers. It ends by explaining why "reactionless" drives and warp drives fail the test of physics.
---

Every spacecraft that has left Earth has done so on chemical rockets, whose energy is fixed by chemistry. The best practical combination, hydrogen and oxygen, gives an exhaust velocity of about 4.4 km/s (Chapter 35), and the rocket equation turns that limit into an exponential penalty for every extra kilometre per second of velocity change. A crewed round trip to Mars, a fast mission to the outer planets or a probe to another star needs a much faster exhaust or a way of pushing a spacecraft without carrying its reaction mass along.

Advanced propulsion splits into two families. The first raises the exhaust velocity with energy from somewhere other than the propellant — a nuclear reactor, solar arrays, fusion or antimatter. The second dispenses with propellant and pushes on sunlight, laser beams, the solar wind, a planet's magnetic field or the atmosphere. Some fly by the thousand, others have never left the laboratory, and a few contradict the laws of physics. This chapter sorts them by exhaust velocity, thrust, power per kilogram and maturity.

## The Tyranny of the Rocket Equation

The **rocket equation**, $\Delta v = v_e \ln(m_0/m_f)$, says that the velocity change Δv depends on the exhaust velocity $v_e$ and on the **mass ratio** — the starting mass $m_0$ divided by the mass $m_f$ left when the propellant is gone. Because the mass ratio is $e^{\Delta v/v_e}$, it grows exponentially once Δv exceeds the exhaust velocity (@fig:rocketeqtyranny). A hydrogen–oxygen stage needs a mass ratio of 2.75 to go from low Earth orbit (LEO) into Mars orbit on the cheapest trajectory (4.5 km/s), but 12 for the 11 km/s that the ion-propelled Dawn accumulated (Chapter 24). Doubling the exhaust velocity takes the square root of the mass ratio; multiplying it by ten turns an impossible mission into a routine one.

![The rocket equation for five exhaust velocities. (a) Mass ratio against velocity change. (b) The velocity change each technology gives when two-thirds of the vehicle is propellant.](figures/out/ch42_rocketeq.svg){#fig:rocketeqtyranny width=96%}

### Energy, Power and Thrust

A faster exhaust has a price: the power it carries away, the **jet power**, is

$$P_{jet} = \tfrac{1}{2}\dot m v_e^2 = \tfrac{1}{2} F v_e ,$$

so, for a given thrust $F$, doubling the exhaust velocity doubles the power needed. A chemical rocket carries its power in its propellant — each F-1 engine of the Saturn V had a jet power near 9 GW — but an electric thruster must be fed by solar arrays or a reactor, and that power plant has mass. A thruster that turns a fraction η of its electrical input $P$ into jet power gives

$$F = \frac{2\eta P}{v_e} = \frac{2\eta P}{g_0 I_{sp}} ,$$

so a 12 kW thruster at 60 % efficiency and 2 600 s produces only about 0.56 N (@fig:propmap).

![Thrust and specific impulse of propulsion technologies. Dotted lines join points of equal jet power: more thrust at higher specific impulse demands power that only large reactors, fusion or beamed energy could supply.](figures/out/ch42_ptmap.svg){#fig:propmap width=92%}

Advanced propulsion is therefore a contest of energy sources and their **specific power** α, the power per kilogram of power and propulsion system. For a mission that thrusts for a time $t$, the best exhaust velocity of a power-limited rocket is of the order of the **characteristic velocity** $v_{ch} = \sqrt{2\eta\alpha t}$: a faster exhaust would need a heavier power plant than the propellant it saves. With α = 50 W/kg, η = 0.6 and one year of thrusting, $v_{ch}$ ≈ 43 km/s (Isp ≈ 4 400 s); with α = 10 W/kg it falls to 19 km/s (Isp ≈ 2 000 s), the territory of Hall thrusters. @tbl:advpropcompare summarises the options; technology readiness levels (TRLs, Chapter 4) run from 1 (principle observed) to 9 (proven in operation).

| Technology | Isp (s) | Thrust | Energy source | TRL (approx.) | Examples |
|---|---|---|---|---|---|
| Chemical (reference) | 300–465 | N to MN | Propellant | 9 | RL10, Raptor |
| Nuclear thermal | 850–950 | 10–1 000 kN | Fission reactor | 5–6 | NERVA XE-Prime, RD-0410 |
| Hall thruster | 1 200–3 000 | mN to 5 N | Electric | 9 (≤ 5 kW), 6–7 (12 kW) | Starlink, Psyche, AEPS |
| Gridded ion | 2 500–4 500 | 1–250 mN | Electric | 9 | Dawn, BepiColombo, NEXT-C |
| MPD, VASIMR | 1 500–6 000 | 1–100 N | Electric, 0.1–10 MW | 4–5 | VX-200, laboratory MPDs |
| FEEP, electrospray | 1 000–10 000 | µN to mN | Electric, watts | 9 | LISA Pathfinder, Enpulsion |
| Solar sail | no propellant | ≈ 8 µN/m² at 1 AU | Sunlight | 6–7 | IKAROS, LightSail 2, ACS3 |
| Electric or magnetic sail | no propellant | µN–mN (studies) | Solar wind | 2–3 | ESTCube-1 (not deployed) |
| Laser sail | no propellant | ≈ 670 N per 100 GW | Ground laser | 2 | Breakthrough Starshot |
| Fusion | 10⁴–10⁶ | N–kN (studies) | Fusion reactions | 1–3 | Daedalus, Direct Fusion Drive |
| Electrodynamic tether | no propellant | 0.1–1 N | Orbital energy, solar power | 5–6 | PMG, TSS-1R |
| Scramjet | 1 000–4 000 | kN | Fuel and air | 6 | X-43A, X-51A |

: Advanced propulsion at a glance (October 2026). TRLs are approximate, judged from flight and test history. {#tbl:advpropcompare}

## Advanced Electric Propulsion

Electric propulsion is already mass-produced — thousands of Hall thrusters fly on Starlink satellites, and ion and Hall engines have carried Dawn, BepiColombo and Psyche (Chapters 6 and 24). The frontier is power: tens to hundreds of kilowatts per spacecraft.

### Power-Limited Trajectories

A power-limited spacecraft thrusts for months (@fig:neptriptime), and the ideal strategy is to vary the specific impulse along the way: more thrust near departure and arrival, higher Isp in between. For such a variable-Isp rocket the propellant consumed depends only on the integral $J = \int a^2\,dt$ of the squared thrust acceleration, and with the power plant sized optimally the fraction of the initial mass left for payload and structure is

$$\frac{m_{payload}}{m_0} = \left(1 - \sqrt{\frac{J}{2\eta\alpha}}\right)^2 .$$

![Power-limited Earth–Mars transfers computed for this chapter. (a) Specific power needed for a given trip time when 50 %, 30 % or 10 % of the departing mass arrives as payload and structure. (b) The low-thrust velocity change. Escape and capture spirals at the planets are excluded.](figures/out/ch42_neptrip.svg){#fig:neptriptime width=96%}

$J$ rises roughly as the inverse cube of trip time. The figure applies this to a one-way trip from Earth escape to Mars capture, optimised numerically for each trip time. A slow spiral needs 5.7 km/s; a 100-day crossing needs 26 km/s and a 40-day crossing 67 km/s. If half the departing mass is to arrive as payload and structure, a 300-day trip needs α ≈ 23 W/kg, a 190-day trip about 110 W/kg, a 100-day trip about 1 kW/kg and a 40-day trip about 17 kW/kg. Solar-electric systems deliver of the order of tens of watts per kilogram at 1 AU; crewed crossings in a month or two would need power systems hundreds of times lighter.

Solar arrays are light and proven, but their output falls with the square of distance from the Sun — at Jupiter to 1/27 of its value near Earth. A reactor gives the same power anywhere, but small reactors manage only a few watts per kilogram and large ones are dominated by their radiators. Solar-electric propulsion suits the inner Solar System; nuclear-electric propulsion the outer planets and heavy cargo.

### High-Power Hall Thrusters

Hall thrusters (Chapter 6) used to wear out as ions eroded their ceramic channel walls. **Magnetic shielding**, developed at JPL in the 2010s, shapes the field to keep energetic ions off the walls, extending design lifetimes to tens of thousands of hours. NASA Glenn and Aerojet Rocketdyne (now L3Harris) used it in the 12 kW **Advanced Electric Propulsion System (AEPS)**, which gives about 0.6 N at about 2 600 s. Three AEPS flight thrusters passed acceptance tests in 2025 (@fig:aepsaccept) and were delivered for the **Power and Propulsion Element (PPE)** built for NASA's Gateway station. When NASA paused Gateway in March 2026, it reassigned the PPE as the bus of the nuclear-electric SR-1 Freedom mission described below; AEPS had by then completed environmental qualification, with a life test in preparation. In the laboratory, the three-channel X3 reached 102 kW in 2017 (@tbl:epthrusters).

### Gridded Ion Engines

Among gridded ion engines, NASA's 6.9 kW **NEXT-C** reaches an Isp of about 4 190 s with 0.24 N of thrust, and a laboratory NEXT engine ran for more than 50 000 hours. NEXT-C flew on the DART asteroid-deflection mission as a demonstration, but when it was first fired in December 2021 an anomaly appeared in the spacecraft's power electronics, and DART, which did not need it, relied on hydrazine thrusters (Chapter 26). The faint blue glow of the ion beam is the technology's signature (@fig:ds1ionglow).

### Magnetoplasmadynamic Thrusters and VASIMR

Above about 100 kW, electromagnetic devices take over. A **magnetoplasmadynamic (MPD)** thruster drives thousands of amperes through a plasma between a central cathode and a surrounding anode, and the magnetic field pushes the plasma out by the Lorentz force $\vec{j} \times \vec{B}$. MPD thrusters handle megawatts in a compact device at 1 500–6 000 s, but their electrodes erode and they are efficient only at very high power; a small pulsed version was carried by Japan's Space Flyer Unit in 1995.

The **Variable Specific Impulse Magnetoplasma Rocket (VASIMR)** of Ad Astra Rocket Company has no electrodes: radio waves ionise argon, a second antenna heats the ions at their cyclotron frequency, and a magnetic nozzle turns their gyration into exhaust. The VX-200 prototype reached 200 kW in 2009 and was measured at 72 % efficiency, about 4 900 s and 5.7 N; in July 2021 the VX-200SS ran for 88 hours at 80 kW. VASIMR has not flown; the fast crewed missions linked to it would need tens of megawatts at specific powers far beyond today's.

::: figrow
![Engineers at NASA Glenn position the third 12 kW AEPS flight thruster for acceptance testing in a vacuum chamber in 2025.](figures/photos/ch42_aeps.jpg){#fig:aepsaccept}

![A xenon ion engine of the type flown on Deep Space 1 under test in a JPL vacuum chamber; the faint blue glow is the ion beam.](figures/photos/ch42_ds1ion.jpg){#fig:ds1ionglow width=67%}
:::

### Field-Emission, Electrospray and Air-Breathing Thrusters

At the other extreme, **field-emission electric propulsion (FEEP)** pulls ions out of a liquid metal such as indium with about 10 kV on a sharp emitter, and **electrospray** thrusters do the same with ionic liquids. They give micronewtons to about a millinewton at 2 000–6 000 s or more: colloid thrusters provided drag-free control for NASA's experiment on ESA's LISA Pathfinder (2015–17), and Enpulsion had launched more than 200 indium FEEP systems by 2024.

For very low orbits (Chapter 14), **air-breathing electric propulsion** would collect the thin air as propellant: in 2018 an ESA-led team fired a Sitael thruster on a nitrogen–oxygen mixture representing the atmosphere at about 200 km, the first such test.

| Thruster | Type | Power | Isp (s) | Thrust | Status (Oct 2026) |
|---|---|---|---|---|---|
| AEPS (NASA, L3Harris) | Magnetically shielded Hall | 12 kW | ≈ 2 600 | ≈ 0.6 N | Three flight units delivered 2025 |
| X3 (Univ. of Michigan) | Hall, three channels | 102 kW | — | 5.4 N | Laboratory record, 2017 |
| NEXT-C (NASA, Aerojet) | Gridded ion | 6.9 kW | ≈ 4 190 | 0.24 N | Flown on DART, 2021 |
| VX-200 / VX-200SS (Ad Astra) | Helicon and ion-cyclotron heating | 200 kW / 80 kW | ≈ 4 900 | ≈ 5.7 N | Laboratory; 88-hour run, 2021 |
| Applied-field MPD | Electromagnetic | 0.1–1 MW | 1 500–6 000 | 1–100 N | Laboratory; small pulsed units flown |
| Indium FEEP (Enpulsion) | Field emission | tens of W | 2 000–6 000 | ≤ ≈ 1 mN | More than 200 launched |

: Electric thrusters at the frontier of power, efficiency and precision. {#tbl:epthrusters}

## Nuclear Thermal Propulsion

A **nuclear thermal rocket (NTR)** replaces the combustion chamber with a fission reactor (@fig:ntpnepschem). Liquid hydrogen cools the nozzle walls, then flows through hundreds of channels in the hot fuel and leaves at 2 500–2 800 K. The reactor adds energy without adding mass, so the propellant can be the lightest gas of all. Exhaust velocity scales as $\sqrt{T/\mathcal{M}}$, where $\mathcal{M}$ is the exhaust's molar mass; hydrogen at 2 g/mol gives about twice the exhaust velocity of a hydrogen–oxygen engine, whose exhaust is mostly steam. The result is 850–950 s at thrusts of tens to hundreds of kilonewtons.

### Reactor Physics in Brief

A uranium-235 nucleus that absorbs a neutron splits, releasing about 200 MeV and two or three neutrons; when on average exactly one of these causes another fission, the reactor is **critical**. Slow ("thermal") neutrons cause fission far more readily than fast ones, so most rocket reactors include a **moderator** — graphite, zirconium hydride or beryllium — that slows them by collisions. **Control drums** around the core, cylinders with a neutron absorber such as boron carbide on one face, rotate to absorb more or fewer neutrons. A **shield** between reactor and tank stops neutrons and gamma rays; elsewhere the spacecraft relies on distance.

The fuel must survive hot hydrogen, which attacks graphite: Rover/NERVA used uranium carbide particles in graphite coated with niobium or zirconium carbide, and today's programmes study carbides and "cermets" of uranium dioxide in tungsten. The 1960s reactors used highly enriched uranium (over 90 % U-235); current designs use **high-assay low-enriched uranium (HALEU)**, just under 20 %, which is unusable for weapons without further enrichment and far cheaper to secure, at the cost of a larger core.

![Principles of nuclear propulsion. (a) In a nuclear thermal rocket, hydrogen cools the nozzle and is then heated in the reactor core. (b) In nuclear electric propulsion, reactor heat is partly converted into electricity for ion or Hall thrusters; radiators reject the rest.](figures/out/ch42_ntpnep.svg){#fig:ntpnepschem width=94%}

### Rover and NERVA

The United States tested about twenty nuclear rocket reactors between 1959 and 1972 in **Project Rover** and the **NERVA** (Nuclear Engine for Rocket Vehicle Application) programme at Jackass Flats, Nevada (@tbl:ntphistory). Phoebus-2A ran at 4 082 MW in 1968, still the most powerful nuclear rocket reactor ever operated, and the small Pewee delivered hydrogen at 2 550 K. The XE-Prime engine of 1969, fired downwards in a test stand, was started 28 times and produced about 247 kN. The programme, which had cost about US$ 1.4 billion, was cancelled in January 1973 (@fig:kiwinozzle); the Soviet RD-0410 was ground-tested at Semipalatinsk but never flew. Those tests vented exhaust carrying fission products into the open air; a new ground test must capture and filter it, one reason modern programmes are expensive.

![Technicians at NASA's Lewis (now Glenn) Research Center manufacture a nozzle for the Kiwi B-1-B nuclear rocket engine in a vacuum oven in 1964.](figures/photos/ch42_kiwi.jpg){#fig:kiwinozzle width=50%}

| Reactor or engine | Year | Reactor power | Milestone |
|---|---|---|---|
| Kiwi-B4E | 1964 | 937 MW | Full-power run and restart |
| Phoebus-2A | 1968 | 4 082 MW | Most powerful nuclear rocket reactor |
| Pewee | 1968 | 503 MW | Exit gas 2 550 K, Isp ≈ 850–900 s |
| NERVA XE-Prime | 1969 | ≈ 1 140 MW | 247 kN, 28 starts, flight-like engine |
| RD-0410 (USSR) | 1970s–80s | 196 MW | 35 kN, 910 s, ground tests only |
| DRACO (DARPA, NASA) | 2023–25 | — | HALEU flight demonstration; cancelled 2025 |

: Milestones of nuclear thermal propulsion. {#tbl:ntphistory}

### DRACO and After

In 2023 DARPA and NASA started **DRACO** (Demonstration Rocket for Agile Cislunar Operations), with Lockheed Martin building the spacecraft and BWX Technologies the HALEU reactor, aiming for an in-orbit test as early as 2027. NASA's budget request for 2026 then provided nothing for nuclear thermal or nuclear electric propulsion, and in mid-2025 DARPA closed DRACO, citing the experiment's cost, the difficulty of ground testing and the falling cost of conventional launch. Congress nevertheless set aside at least US$ 110 million for nuclear thermal propulsion in NASA's 2026 appropriation, which the administrator told the Senate in April 2026 NASA would spend. Russian and Chinese work, mostly on nuclear-electric systems, is hard to judge from public sources.

### Faster to Mars

The prize for crewed missions is time. @fig:marsntpchem compares single-stage chemical and nuclear thermal vehicles delivering 60 t into a high Mars orbit. Faster transfers need more Δv at both ends: 4.5 km/s for the 259-day minimum-energy transfer, 5.5 km/s for 180 days and 8.8 km/s for 120 days. With 300 t in LEO, the chemical vehicle can make the crossing in about 180 days and the nuclear one in about 120. Shorter transits matter because interplanetary crews receive about 1.8 mSv of cosmic radiation per day (Chapter 30).

![Faster Mars transfers computed for this chapter. (a) Impulsive Δv from a 400 km Earth orbit to a 1-sol (250 × 33 793 km) Mars orbit against transit time. (b) Initial mass in low Earth orbit for chemical and nuclear thermal stages delivering 60 t.](figures/out/ch42_marstrip.svg){#fig:marsntpchem width=96%}

::: example
**Example: six months to Mars — chemical or nuclear?**

A transfer vehicle must deliver 60 t (habitat and lander) from a 400 km LEO into a 1-sol Mars orbit in 180 days. The trajectory model gives a trans-Mars injection of 3.93 km/s and an orbit insertion of 1.56 km/s: Δv = 5.49 km/s.

1. **Chemical (Isp 450 s, $v_e$ = 4.41 km/s).** Mass ratio $R = e^{5.49/4.41}$ = 3.47. If tanks, engines and structure weigh 12 % of the propellant, the final mass is $m_f = 60/[1 − 0.12(R − 1)]$ = 85.3 t and the initial mass $m_0 = R\,m_f$ = **296 t**, of which 211 t is propellant.
2. **Nuclear thermal (Isp 900 s, $v_e$ = 8.83 km/s).** $R = e^{5.49/8.83}$ = 1.86. Bulky hydrogen tanks weigh 20 % of the propellant, plus 10 t of engines and shielding: $m_f = (60 + 10)/(1 − 0.20 × 0.86)$ = 84.6 t and $m_0$ = **158 t**, with 73 t of propellant.
3. The nuclear vehicle needs about half the mass in LEO. Spending the same 300 t on it instead shortens the trip to about **118 days**, cutting the crew's dose in transit from about 0.33 Sv to 0.22 Sv.
4. The price is hydrogen's low density (71 kg/m³): 73 t fills about 1 000 m³, to be kept at 20 K for months (Chapter 40 discusses boil-off).
:::

## Nuclear Electric Propulsion and Space Reactors

Nuclear electric propulsion (NEP) separates energy from reaction mass completely: reactor heat is partly converted into electricity for ion or Hall thrusters (@fig:ntpnepschem b). Its weak point is waste heat. A closed Brayton converter, in which a helium–xenon gas loop drives a turbine and alternator, is about 20–30 % efficient, so a 1 MWe system at 25 % must reject about 3 MW. A radiator at 500 K with an emissivity of 0.9 sheds only about 3.2 kW per square metre from each face, so it would need some 470 m², nearly two tennis courts.

### Reactors in Space So Far

The United States has flown one reactor: **SNAP-10A**, launched in April 1965, which produced about 500 W of electricity for 43 days before an electrical failure shut it down. The Soviet Union flew 33: 31 **BES-5 Buk** reactors of about 3 kWe powered radar ocean-reconnaissance satellites (RORSATs) between 1970 and 1988, and two **TOPAZ** thermionic reactors of about 5 kWe flew in 1987 (@tbl:spacereactors). RORSATs boosted their reactors into storage orbits about 900 km high after use, but in January 1978 Kosmos 954 failed to and scattered radioactive debris across northern Canada. The accident shaped the United Nations principles on nuclear power sources in space (1992), including the rule that a reactor must not go critical before reaching its operating orbit or interplanetary trajectory.

### Kilopower and Fission Surface Power

NASA's modern work began with **Kilopower**, a family of 1–10 kWe concepts with a solid cast uranium core, passive sodium heat pipes and Stirling engines. The **KRUSTY** prototype (Kilopower Reactor Using Stirling Technology) was tested in Nevada from November 2017 to March 2018, ending with a 28-hour full-power run that simulated start-up, failed heat pipes and failed Stirling engines — the first test of a new US space-reactor design in decades. In 2022 NASA and the Department of Energy funded three industry designs for a 40 kWe **Fission Surface Power** system for the Moon (@fig:fsptdu).

Policy then accelerated. A NASA directive in August 2025 called for a lunar reactor of at least 100 kWe ready for launch around 2030, and in April 2026 a White House memorandum (NSTM-3) launched a National Initiative for American Space Nuclear Power, calling for reactors in orbit as early as 2028 and on the Moon by 2030. The first lunar unit, **Lunar Reactor-1**, is specified in an August 2026 draft solicitation at no less than 20 kWe — a smaller first step than the 2025 goal — with a landing intended in 2030 to power a lunar base through the 14-day night (Chapter 41).

### SR-1 Freedom

The most ambitious near-term project is **Space Reactor-1 (SR-1) Freedom**, announced by NASA Administrator Jared Isaacman in March 2026 as the first spacecraft to use a fission reactor for propulsion beyond Earth orbit. A reactor designed by Idaho National Laboratory, fuelled with HALEU uranium dioxide and cooled by heat pipes, will produce at least 20 kWe through a closed Brayton converter supplied by Sierra Lobo. It sits behind a boron-carbide shield at the end of a boom with radiator fins and will be switched on only after leaving Earth orbit, to drive the xenon Hall thrusters of the repurposed Gateway PPE (built by Lanteris Space Systems, part of Intuitive Machines since January 2026) through an electric-propulsion system of up to 48 kW. SR-1 is due to launch in December 2028 and reach Mars about a year later with three Ingenuity-derived helicopters (the SkyFall mission) to scout landing sites; its reported cost is about US$ 2.1 billion without them. The schedule is tight — the reactor was still being designed in October 2026 — but SR-1 would be the first US reactor launched in more than 60 years. Russia's proposed megawatt-class "Zeus" nuclear tug has shown no public progress since 2021.

![A 10 kW Stirling power-conversion unit for NASA's Fission Surface Power Technology Demonstration Unit at Glenn Research Center; four such units would turn 180 kW of reactor heat into 40 kW of electricity.](figures/photos/ch42_fsptdu.jpg){#fig:fsptdu width=46%}

| System | Country | Years | Electrical power | Conversion | Status |
|---|---|---|---|---|---|
| SNAP-10A | USA | 1965 | ≈ 0.5 kW | Thermoelectric | Flown; 43 days |
| BES-5 Buk | USSR | 1970–88 | ≈ 3 kW | Thermoelectric | 31 flown on RORSATs |
| TOPAZ | USSR | 1987 | ≈ 5 kW | Thermionic | 2 flown |
| KRUSTY (Kilopower) | USA | 2017–18 | 1 kW class | Stirling | Ground test; 28 h at full power |
| SR-1 Freedom | USA | 2028 (planned) | ≥ 20 kW | Closed Brayton | In development; drives Hall thrusters |
| Lunar Reactor-1 | USA | 2030 (planned) | ≥ 20 kW | — | Draft solicitation, August 2026 |

: Space fission power systems, flown and planned. {#tbl:spacereactors}

## Sailing on Light

### Radiation Pressure

Light carries momentum: a beam of power $P$ pushes on an absorbing surface with a force $P/c$, and on a perfect mirror facing it with $2P/c$. At 1 AU sunlight delivers 1 361 W/m², a pressure of 4.54 µN/m² on an absorber and 9.08 µN/m² on a perfect mirror. A flat sail of area $A$, tilted at a **cone angle** α to the sunlight and with an overall efficiency η (about 0.85, allowing for absorption and wrinkles), feels

$$F = \frac{2\eta P_\odot A}{c}\cos^2\alpha .$$

Dividing by mass gives the **characteristic acceleration** $a_c$ at normal incidence, which depends only on the **areal density** σ = m/A of the whole spacecraft (@fig:sailperf a, @tbl:solarsails). Sail acceleration and solar gravity both fall with the square of distance, so their ratio — the **lightness number** β — is the same everywhere. Tilting the sail by about 35° gives the largest push along the orbit, raising it in an outward spiral; tilting it the other way spirals inwards. For a slow spiral from radius $r_0$ to $r$ the time is about

$$T \approx \frac{\sqrt{\mu_\odot/r_0}\;\left|(r/r_0)^{3/2} - 1\right|}{3 \times 0.385\,a_c} ,$$

where 0.385 is cos²α sin α at the optimum angle (@fig:sailperf b).

![Solar-sail performance computed for this chapter. (a) Characteristic acceleration at 1 AU against the areal density of the whole spacecraft, with the sails flown so far. (b) Time to spiral from Earth's orbit to the distances of Mars, Mercury and Jupiter: lines from the spiral formula, dots from numerical trajectories.](figures/out/ch42_sail.svg){#fig:sailperf width=96%}

| Mission | Operator | Launch | Sail area | Mass | Outcome |
|---|---|---|---|---|---|
| IKAROS | JAXA | 2010 | 196 m² | ≈ 310 kg | Venus flyby |
| NanoSail-D2 | NASA | 2010 | 10 m² | ≈ 4 kg | Deorbit test |
| LightSail 2 | Planetary Soc. | 2019 | 32 m² | ≈ 5 kg | Sailed in LEO |
| NEA Scout | NASA | 2022 | 86 m² | 14 kg | Never contacted |
| ACS3 | NASA | 2024 | 80 m² | 16 kg | Deployed; boom bent |
| Solar Cruiser | NASA | — | ≈ 1 670 m² | — | Cancelled 2023 |

: Solar-sail missions. Masses are for the whole spacecraft. {#tbl:solarsails}

### Sails Flown So Far

JAXA's **IKAROS**, launched with the Venus orbiter Akatsuki in 2010, was the first interplanetary solar sail. It unfolded a 14 m square of 7.5 µm polyimide film by spinning, carried thin-film solar cells and steered with liquid-crystal panels of switchable reflectivity; JAXA measured a force of 1.12 mN. NASA's **NanoSail-D2** and The Planetary Society's **LightSail 2** followed in Earth orbit; LightSail 2 raised its orbit by about 2 km in its first days of sailing. NASA's 86 m² **NEA Scout**, launched on Artemis I in 2022, was never heard from (@fig:neascoutdeploy), and the nearly 1 700 m² **Solar Cruiser** was not confirmed for flight and was closed out in 2023. The **Advanced Composite Solar Sail System (ACS3)**, a 16 kg, 12-unit CubeSat, deployed an 80 m² sail on four 7 m carbon-fibre composite booms in August 2024 (@fig:acs3orbit). One boom was later reported bent and the sail was not actively steered, but the deployment proved booms that larger sails will need.

::: figrow
![Engineers at NASA's Marshall Space Flight Center deploy a flight-like engineering unit of the 86 m² NEA Scout solar sail, first unfurled there in August 2016.](figures/photos/ch42_neascout.jpg){#fig:neascoutdeploy}

![The ACS3 sail seen by one of the spacecraft's four wide-angle cameras during deployment in orbit on 28 August 2024: reflective quadrants and a composite boom, curved by the lens.](figures/photos/ch42_acs3.jpg){#fig:acs3orbit}
:::

### Electric and Magnetic Sails

The solar wind, streaming outwards at about 400 km/s, carries far less momentum than sunlight but can be intercepted by structures much lighter than film. Pekka Janhunen's **electric sail** (2004) would spin out thin tethers tens of kilometres long, charged to about 20 kV, whose electric fields repel solar-wind protons over a width far greater than the wires. Because the electron sheaths around the wires widen as the solar wind thins, the thrust falls only as 1/r rather than 1/r². Estonia's ESTCube-1 (2013) and Finland's Aalto-1 (2017) carried tether experiments, but neither managed to unreel its tether. A **magnetic sail** would deflect the solar wind with a large superconducting loop or a plasma-inflated magnetic bubble; none has been tested in flight.

::: example
**Example: sailing from Earth's orbit to Mars's**

A sail of 1 600 m² of 2.5 µm aluminised film (about 3.5 g/m², 5.6 kg) is held by 6 kg of composite booms and carries a 40 kg spacecraft: 51.6 kg in all.

1. **Areal density:** σ = 51.6 kg/1 600 m² = 32.2 g/m².
2. **Force at 1 AU:** $F$ = 2 × 0.85 × 4.54 µN/m² × 1 600 m² = **12.3 mN**, so $a_c$ = 12.3 mN/51.6 kg = **0.239 mm/s²** and β = 0.239/5.93 = 0.040.
3. **Δv budget:** at the optimum cone angle the push along the orbit is 0.385 × 0.239 = 0.092 mm/s², or 2.9 km/s per year at 1 AU, falling as the sail moves out.
4. **Spiral time:** with $\sqrt{\mu_\odot/r_0}$ = 29.8 km/s and $(1.524)^{3/2} − 1$ = 0.881, $T$ ≈ 29 800 × 0.881/(3 × 0.385 × 0.000239) s = 9.5 × 10⁷ s ≈ **3.0 years** to Mars's distance; the numerical trajectory gives 3.3 years, against 0.7 years for a chemical Hohmann transfer.
5. A one-year trip would need $a_c$ ≈ 0.72 mm/s², or σ ≈ 11 g/m² for the whole spacecraft — beyond any sail yet built. Sails win where the Δv is enormous, such as stations hovering sunward of L1, where no propellant supply would last.
:::

## Beamed Energy and the Interstellar Challenge

The nearest star system, Alpha Centauri, is 4.37 light-years — about 276 000 AU — away. Voyager 1, the fastest object leaving the Solar System at about 17 km/s (3.6 AU per year), would need some 77 000 years to cover that distance. Reaching another star within a lifetime needs a tenth to a fifth of the speed of light.

### Breakthrough Starshot

In 2016 the Breakthrough Initiatives announced **Starshot**, with US$ 100 million for research into leaving the engine on the ground. A phased array of about ten million lasers totalling up to 100 GW, spread over about a square kilometre, would focus on a sail a few metres across carrying a gram-scale "StarChip" with cameras, a laser transmitter and a radioisotope power source. Accelerating at about 10 000 g for some minutes, the probe would reach 15–20 % of the speed of light, pass Alpha Centauri about 20 years later and send images home by laser. A cost model by Kevin Parkin put the ground system at about US$ 8 billion, with an optimum 4.1 m sail accelerated for about nine minutes.

The physics is simple and severe (@fig:starshotlaser). A perfectly reflecting sail struck by 100 GW feels $2P/c$ = 667 N; on a 2 g probe that is 34 000 g. But a laser beam spreads by diffraction: an array of diameter $D$ focuses light of wavelength λ into a spot about $2.44\,\lambda L/D$ across at distance $L$, so a 3 km array keeps a 4.1 m sail fully lit only to about 4.7 million km, some 12 times the distance to the Moon. Beyond that the captured power falls with the square of distance and the relativistic Doppler shift weakens the push, so most of the speed is gained in the first three minutes.

![Starshot-class laser sails computed for this chapter: 100 GW from a 3 km array at 1.064 µm, a 4.1 m perfectly reflecting sail and total masses of 1, 2 and 5 g. (a) Speed against time. (b) Acceleration against distance from the laser.](figures/out/ch42_starshot.svg){#fig:starshotlaser width=96%}

The engineering is far harder: a sail under a micrometre thick that reflects almost all of an intense beam and rides it stably, ten million lasers phased through a turbulent atmosphere, survival of dust impacts at 60 000 km/s, and data sent home across 4 light-years. Starshot's first phase judged these problems to have credible conceptual solutions, but the programme was paused in 2024 to seek broader support.

::: example
**Example: the numbers behind a laser sail**

A 2 g probe (1 g sail, 1 g chip) with a 4.1 m perfectly reflecting sail is pushed by 100 GW of 1.064 µm laser light from a 3 km array.

1. **Force and acceleration:** $F = 2P/c$ = 2 × 10¹¹ W/3.00 × 10⁸ m/s = **667 N**, a pressure of 51 Pa on the 13.2 m² sail; $a = F/m$ = 3.3 × 10⁵ m/s² ≈ **34 000 g**.
2. **Without diffraction**, reaching 0.2c (6.0 × 10⁷ m/s) would take $v/a$ = 180 s over $v^2/2a$ = 5.4 million km.
3. **Diffraction distance:** $L_0 = Dd/2.44\lambda$ = 3 000 × 4.1/(2.44 × 1.064 × 10⁻⁶) m = 4.7 × 10⁹ m. The simulation in @fig:starshotlaser reaches 0.17c there after 179 s and 0.22c after 10 minutes, 31 million km out.
4. **Energy:** the laser emits 100 GW × 600 s = 60 TJ; the probe's kinetic energy at 0.2c, $(\gamma − 1)mc^2$, is 3.7 TJ — an efficiency of about 6 %.
5. **Heating:** absorbing just 10⁻⁵ of the beam, the sail would have to shed 1 MW from 13 m², so it must be an almost perfect dielectric mirror. At 0.2c, Alpha Centauri is about 22 years away.
:::

### Fusion and Antimatter

Fusion releases about four times more energy per kilogram than fission, and its charged products could in principle be directed out as exhaust by magnetic fields (@fig:fuelenergy). The British Interplanetary Society's **Project Daedalus** (1973–78) designed an uncrewed two-stage probe of about 54 000 t — mostly deuterium–helium-3 pellets ignited by electron beams 250 times a second — to carry a 450 t payload to Barnard's Star, 5.9 light-years away, at 12 % of the speed of light in about 50 years. Earlier, **Project Orion** (1958–65) studied a ship pushed by small nuclear explosions, until the 1963 test-ban treaty ended it.

![Energy released per kilogram of reacting fuel and the corresponding ideal exhaust speed, computed from reaction energies. Each step from chemistry to fission, fusion and annihilation multiplies the energy by orders of magnitude.](figures/out/ch42_energy.svg){#fig:fuelenergy width=90%}

No fusion device has yet produced more energy than its whole system consumes. The US National Ignition Facility first achieved ignition in December 2022, releasing 3.15 MJ from a capsule heated by 2.05 MJ of laser light, but its lasers drew about 300 MJ from the grid. Compact propulsion concepts such as the **Direct Fusion Drive**, based on the Princeton field-reversed configuration, are estimated to give 2.5–5 N per megawatt of fusion power at about 10 000 s; they remain small laboratory experiments.

Matter–antimatter annihilation converts all of the mass into energy: 1 g of antimatter meeting 1 g of matter releases 1.8 × 10¹⁴ J, as much as a 43-kiloton explosion. But antimatter is made in particle accelerators one particle at a time, at minute efficiency. CERN makes about 10¹² antiprotons a day, and all it has ever produced amounts to less than 10 nanograms; at that rate a gram would take billions of years. Antimatter rockets remain thought experiments.

## Breathing Air and Detonating Fuel

### Scramjets and Combined Cycles

A hydrogen–oxygen rocket carries about 6 kg of oxygen for every kilogram of hydrogen. Air-breathing engines avoid that mass and reach fuel-specific impulses of 1 000–4 000 s, but only inside the atmosphere (Chapter 10). Above about Mach 5 the air must stay supersonic through the combustor, the regime of the **scramjet**. NASA's X-43A (@fig:x43nose) reached Mach 9.6 for about 10 seconds in November 2004, and the US Air Force's X-51A flew for 210 s at up to Mach 5.1 in 2013. Combined-cycle engines switch between modes: the British SABRE design pre-cooled incoming air from about 1 000 °C to −150 °C in a fraction of a second to run as an air-breathing rocket up to Mach 5.5 before switching to pure rocket mode. Its developer, Reaction Engines, tested the pre-cooler at Mach 5 conditions in 2019 but entered administration in October 2024, and its intellectual property was being sold in 2025.

![The X-43A scramjet research vehicle — the small wedge at the nose of its modified Pegasus booster — under the wing of NASA's B-52B on 15 November 2004, the day before its record Mach 9.6 flight.](figures/photos/ch42_x43nose.jpg){#fig:x43nose width=50%}

### Rotating Detonation Engines

Conventional rocket engines burn propellant at almost constant pressure. In a **rotating detonation engine (RDE)**, propellants injected into an annular channel are consumed by one or more detonation waves — shock waves coupled to combustion — racing around the annulus at about 2 km/s, thousands of times a second. Detonation raises the pressure as it burns, so analyses predict a higher specific impulse for the same propellants, and the thin reaction zone allows a much shorter chamber. In July 2021 Nagoya University and JAXA flew an RDE in space for the first time on the S-520-31 sounding rocket, producing about 500 N for 6 seconds. At NASA's Marshall Space Flight Center a 3D-printed copper-alloy rotating detonation rocket engine (RDRE) produced more than 18 kN in 2022 and fired for 251 seconds at more than 26 kN in September 2023 (@fig:rdrefire); in May 2025 the US company Venus Aerospace flew an RDRE-powered test vehicle from Spaceport America. Stabilising the waves and cooling the walls are the main challenges.

![A 251-second hot fire of a full-scale, 3D-printed rotating detonation rocket engine at NASA's Marshall Space Flight Center in 2023, producing more than 26 kN (5 800 lbf) of thrust.](figures/photos/ch42_rdre.jpg){#fig:rdrefire width=52%}

## Propellantless and Exotic Ideas

### Tethers

A long conducting wire moving through Earth's magnetic field acts as a generator. Its **motional EMF** is $vBL$: about 2 kV for a 10 km tether in low orbit, where v = 7.6 km/s and B ≈ 30 µT (@fig:tetherschem). If the circuit is closed through the ionosphere by plasma contactors, a current flows and the magnetic force $I\vec{L} \times \vec{B}$ opposes the motion: 1 A gives about 0.3 N of drag, enough to deorbit dead satellites without propellant (Chapter 21). Driving the current the other way with solar power turns the tether into a motor that raises the orbit. NASA's Plasma Motor Generator (1993) tested both modes with a 500 m tether, and on the TSS-1R mission in February 1996 Space Shuttle Columbia deployed an Italian satellite on a conducting tether to 19.7 km, generating about 3 500 V and nearly 0.5 A before arcing burned through the tether and it broke.

![Tethers. (a) An electrodynamic tether in Earth's magnetic field: the induced current feels a force opposing the motion (or, driven by solar power, along it). (b) A rotating tether catches a slow payload at the bottom of its swing and releases it faster at the top, giving up momentum.](figures/out/ch42_tether.svg){#fig:tetherschem width=88%}

Non-conducting tethers exchange momentum mechanically. In 1993 the SEDS-1 experiment lowered a 26 kg payload on a 20 km tether below a Delta II stage and cut it loose into a re-entry trajectory, and in 2007 the student-built YES2 deployed 31.7 km of tether — the longest structure ever deployed in space. The ultimate tether, a **space elevator** from the equator to beyond geostationary orbit, fails on materials: even with a cable ten times thicker at geostationary altitude than at the ground, it would need a breaking length of about 2 100 km under Earth's gravity, against about 400 km for the best commercial fibres.

Two propellant-free techniques already serve missions: gravity assists (Chapter 24) and atmospheric braking. **Aerocapture** — a single deep pass through a planet's atmosphere inside an aeroshell to brake straight into orbit — has not yet flown, but could cut the mass of an orbiter for Uranus, Neptune or Titan by a third or more (Chapter 25).

### Reactionless Drives and Warp Drives

Every working propulsion system conserves momentum: something — exhaust, photons, the solar wind, a planet's magnetic field — must carry momentum the other way. The **EmDrive**, a closed, tapered microwave cavity proposed around 2001, was claimed to produce thrust without exhaust; a NASA Eagleworks paper in 2016 reported about 1.2 mN per kilowatt. Tests at TU Dresden with new thrust balances and suspensions reproduced the apparent thrust and then made it disappear: it came from thermal expansion of the mountings and from currents in the power cables interacting with Earth's magnetic field. The 2021 results bounded any anomalous force below that of a photon rocket of the same power — 3.3 µN per kilowatt, the push of simply shining the microwaves into space — more than a thousand times below the earlier claims. "Mach-effect" thrusters tested the same way also failed to show real thrust.

In 1994 Miguel Alcubierre showed that Einstein's equations allow, mathematically, a "warp bubble" that contracts space ahead of a ship and expands it behind, carrying it faster than light without local motion. It needs negative energy density — "exotic matter" unknown in bulk — and the first estimates of the energy required exceeded the mass-energy of the observable universe. Later designs cut the energy enormously but not to zero, and a bubble could not be steered from inside, because its front edge would lie beyond the reach of any signal from the ship. Warp drives remain an exercise in general relativity, not a propulsion technology.

::: ai
**AI in advanced propulsion**

Plasma thrusters are hard to model: electrons in a Hall thruster cross the magnetic field far faster than classical collisions allow, and no first-principles theory yet predicts this "anomalous" transport. Researchers have used Bayesian inference and machine learning on plasma measurements to build data-driven transport models and fast design surrogates. In fusion, reinforcement learning has controlled the shape of a tokamak plasma at EPFL's TCV device (2022). Mission designers train neural networks to approximate optimal low-thrust control and explore millions of trajectories quickly, and fleets with thousands of Hall thrusters produce telemetry suited to anomaly detection (Chapters 48 and 52).
:::

::: key
**Key takeaways**

- Mass ratio grows as $e^{\Delta v/v_e}$, and jet power ½$Fv_e$ makes faster exhaust cost power.
- Electric propulsion is scaling up (12 kW AEPS built, 100 kW run), but 100-day Mars trips need about 1 kW/kg.
- Nuclear thermal rockets (850–950 s) roughly halve the LEO mass of a six-month Mars transfer; DRACO was cancelled in 2025.
- Space fission power is returning: SR-1 Freedom (≥ 20 kWe, nuclear-electric) is planned for December 2028, Lunar Reactor-1 for 2030.
- Sails flown reach about 0.05 mm/s²; a one-year trip to Mars's distance needs about 11 g/m².
- A 100 GW laser could push a gram-scale sail to about 0.2c in minutes, but the engineering is unsolved and Starshot is paused.
- Scramjets, detonation engines and tethers serve niches; reactionless and warp drives fail the tests of physics.
:::

::: questions
**Review questions**

1. Compare mass ratios for Δv = 10 km/s at $v_e$ = 4.4, 8.8 and 40 km/s. Why not raise $v_e$ without limit?
2. A 50 kW Hall-thruster system works at 60 % efficiency and 2 500 s. What is its thrust, and how long would it take to give a 20 t spacecraft 5 km/s?
3. Define specific power α. Using @fig:neptriptime, explain why a 40-day crewed trip to Mars is unrealistic with present technology.
4. How does a nuclear thermal rocket achieve about twice the specific impulse of a hydrogen–oxygen engine? What roles do the moderator, control drums and shield play?
5. Why was DRACO cancelled, and why is ground-testing an NTR harder now than in the 1960s?
6. A 1 MWe nuclear-electric system has 25 % efficient Brayton converters and radiators at 500 K (emissivity 0.9). Estimate the radiator area and explain why radiators dominate NEP mass.
7. A 4 kg CubeSat carries a 40 m² sail. Calculate its characteristic acceleration at 1 AU (η = 0.85) and the time to spiral out to 1.5 AU.
8. Why does a laser sail's push collapse beyond a certain distance, and how does doubling the array diameter change it?
9. How does a rotating detonation engine work? Describe two tests made since 2021.
10. Why do careful experiments rule out the EmDrive? What thrust must any device radiating 1 kW of electromagnetic power produce?
:::
