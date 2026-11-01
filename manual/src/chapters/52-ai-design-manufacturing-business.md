---
title: AI in Spacecraft Design, Manufacturing, Launch and the Space Business
hero: ch52
abstract: Long before a spacecraft flies, AI is at work in the engineering behind it. Algorithms now propose structures, search large design spaces with few simulations, check requirements, watch metal printers layer by layer and screen CT scans for flaws. On the launch range, learning helps with engine health, weather and scheduling. Flight-critical decisions stay with optimisation and fixed rules. In the business, models turn satellite data into market signals, price launch risk and size constellations. This chapter explains each method from first principles. Small experiments, run from scratch, measure what each method gains and where it fails. It closes with a safe way to bring AI tools into an engineering team. Status is given as of October 2026.
---

A spacecraft is shaped by thousands of decisions taken years before launch. Each is made with incomplete information and a fixed budget. Artificial intelligence (AI) now helps with many of them. It does not replace the engineer. It proposes options, searches faster and checks more data than people can.

The hero image shows the starting point of much of this work: an engineer at NASA's Marshall Space Flight Center explaining rocket-engine hardware made by additive manufacturing (3-D printing). Printing frees the designer from the limits of machining. An algorithm can then draw shapes that no person would draw. Printing also creates new risks, such as hidden pores in the metal, which learned models help to find.

This chapter follows a spacecraft from design to the market. Systems engineering is covered in Chapter 4, structures in Chapter 5, launch vehicles in Chapters 34–36 and spaceports in Chapter 37. Learning methods are explained in Chapters 43 and 44, and computing hardware in Chapter 45. Trust, assurance and governance are the subject of Chapter 53.

## AI Across the Life Cycle

The key idea of this chapter is simple. **AI proposes; physics, test and people verify.** A learned model can be wrong in ways that are hard to see. So nothing it produces enters the controlled design without passing the same checks as human work.

@fig:aipipeline52 shows where AI enters the life cycle. Each stage has its own tools, but they share two features. First, every output passes a **verification gate**: a high-fidelity analysis, a test, an inspection or a review by a responsible engineer. Second, every stage writes data into a **digital thread** — one linked record of requirements, models, analyses, build records and test results.

![Where AI helps in the life cycle of a spacecraft. Each stage has its own tools, but every output passes a verification gate before it enters the controlled design. A digital thread links all stages, so that test and flight results return as labelled data.](figures/out/ch52_pipeline.svg){#fig:aipipeline52 width=98%}

### Where the Value Lies

Early choices fix most of the cost of a programme (Chapter 4), so improving the concept saves more than speeding up drawing. Yet early stages have the least data, and models there must work from physics and small samples. Later stages, such as inspection, have plenty of data but little freedom to change the design.

### Operational, Demonstrated or Research?

Claims about AI range from routine use to press releases about prototypes. @tbl:aistatus52 sorts the main uses by status as of October 2026. "Operational" means used routinely on real programmes. "Demonstrated" means shown on real hardware or data but not yet routine. "Research" means published studies and prototypes.

| Use | Main method | Example | Status (Oct 2026) |
|---|---|---|---|
| Structural brackets and mounts | Topology optimisation, generative design | NASA Goddard "evolved structures"; RUAG Sentinel-1 bracket | Operational |
| Antennas | Evolutionary search | NASA ST5 antennas (2006) | Flown |
| Whole engines from requirements | Rule-based computational models | LEAP 71 engines, 5–20 kN | Demonstrated (hot fire) |
| Fast simulation | Neural surrogates and operators | Commercial tools (PhysicsX, Neural Concept) | Early operational |
| Requirements and documents | Language models, retrieval | ESA SpaceQA, NASA drafts | Pilots and research |
| Printer monitoring | Image segmentation | ORNL Peregrine | Operational in labs and industry |
| CT and visual inspection | Classifiers | Factory inspection | Operational in industry |
| Engine health | Redlines; learned detectors on the ground | Shuttle AHMS (2006–11) | Redlines flown; learning on ground |
| Satellite-data analytics | Detection, regression | Retail, shipping, commodities | Operational |
| Insurance and pricing | Statistical risk models | Launch and in-orbit risk, parametric cover | Operational |

: Main uses of AI in design, manufacturing, launch and business, with an example and their status as of October 2026. {#tbl:aistatus52}

## Design: Letting Algorithms Propose Shapes

The key idea of this section is that a computer can search shapes, not just check them. The engineer states the loads, the interfaces and the forbidden zones. The algorithm finds where material is needed.

### Evolutionary Design

The first computer-designed hardware in space was a small wire antenna. NASA's Space Technology 5 (ST5) mission needed an X-band antenna with a wide beam for three small satellites. In 2004 a team at NASA Ames used **evolutionary algorithms** to design it (@fig:st5photo).

An evolutionary algorithm copies natural selection. It starts with a population of random designs, here wire shapes with a few bends. Each design is scored by a simulation; the score is called its **fitness**. The best designs are copied with small random changes (**mutation**) and mixed together (**crossover**). After many generations the population converges on good designs. The method needs no gradients, so it works with any simulator, but it may need tens of thousands of evaluations.

![The three ST5 microsatellites on their payload structure at Vandenberg Air Force Base in February 2006, a month before launch. Each carried an X-band antenna whose shape was found by an evolutionary algorithm.](figures/photos/ch52_st5.jpg){#fig:st5photo width=58%}

::: history
**Landmark: the evolved antennas of ST5 (2006)**

- Jason Lohn of NASA Ames, Gregory Hornby of the University of California, Santa Cruz, and Derek Linden of JEM Engineering ran two evolutionary algorithms. One bent single wires; the other grew branching shapes.
- The winning antennas looked like bent paper clips. No human designer would have drawn them.
- Mid-project, the mission moved to a lower orbit and the requirements changed. The team changed the fitness function, evolved new designs, then built and tested two new antennas in about a month.
- Both performed about as well as a conventional antenna designed by a contractor. The three satellites were launched on 22 March 2006 on a Pegasus XL, carrying the first computer-evolved hardware in space.
:::

### Topology Optimisation

For structures, the most widely used method is **topology optimisation**. It decides where material should go inside a fixed design space. The space is divided into small finite elements. Each element $e$ gets a density $\rho_e$ between 0 (empty) and 1 (solid).

The popular **SIMP** method (solid isotropic material with penalisation) links the stiffness of an element to its density. The rule is

$$ E(\rho_e) = E_{\min} + \rho_e^{\,p}\,(E_0 - E_{\min}), \qquad p \approx 3 . $$

Here $E_0$ is the stiffness of solid material and $E_{\min}$ a tiny value that keeps the maths stable. The penalty $p$ makes half-dense elements poor value: they cost half the mass but give only an eighth of the stiffness. The optimiser therefore pushes elements towards 0 or 1.

The usual goal is the stiffest structure for a given mass. Stiffness is measured by its inverse, the **compliance** $c = \mathbf{F}^\top\mathbf{u}$: the work done by the load $\mathbf{F}$ through the displacements $\mathbf{u}$. The problem is

$$ \min_{\boldsymbol\rho}\; c(\boldsymbol\rho) \quad \text{subject to} \quad \mathbf{K}(\boldsymbol\rho)\,\mathbf{u} = \mathbf{F}, \qquad \sum_e \rho_e v_e \le V^\ast , $$

where $\mathbf{K}$ is the stiffness matrix, $v_e$ the volume of an element and $V^\ast$ the allowed volume. The gradient has a simple form. For each element, $\partial c/\partial \rho_e = -p\,\rho_e^{\,p-1}(E_0 - E_{\min})\,\mathbf{u}_e^\top \mathbf{k}_0 \mathbf{u}_e$, where $\mathbf{k}_0$ is the stiffness matrix of a solid element. Elements that store much strain energy gain material; the others lose it. A **filter** averages the densities over a small radius, which stops chequerboard patterns and sets a minimum member size.

The method is classical optimisation, not machine learning. It is still the engine under most "AI-designed" parts, so it belongs at the start of this chapter. @fig:simpcantilever shows it at work on a cantilever, clamped on the left and loaded at the right. The code is about a hundred lines of numpy. It follows the well-known "88-line" program published by Andreassen and colleagues in 2011.

![Topology optimisation of a cantilever with 40 % of the material, run from scratch. (a) The density field after 1, 5, 20 and 122 iterations; a truss-like structure emerges. (b) The compliance falls by a factor of eight in the first 30 iterations. (c) For the same stiffness, optimised designs need 24–33 % less mass than a plate of uniform thickness.](figures/out/ch52_topopt.svg){#fig:simpcantilever width=98%}

The run took 122 iterations. Compliance fell from 1 851 to 230 units, and most of the gain came in the first 30 steps. The final design is a set of struts and ties, like a bridge truss.

How much mass does this save? Compare a plate of the same outline, thinned until it is as stiff as the optimised part. Rounded to solid or empty, the optimised design uses 40.3 % of the material of a solid block and is 1.72 times as compliant. An equally stiff uniform plate needs 58.2 %, so the saving is 30.6 % of the mass; across volume fractions from 0.2 to 0.6 it was 24–33 %.

::: example
**Example: mass saving from topology optimisation**

A small satellite carries 25 aluminium brackets machined as plates of uniform thickness, 12.0 kg in total. Each bracket is replaced by a topology-optimised part with the same stiffness, using the ratio from @fig:simpcantilever.

1. **Mass ratio at equal stiffness.** The optimised design uses 40.3 % of the solid material; the equally stiff plate uses 58.2 %. The ratio is 0.403 / 0.582 = **0.692**.
2. **New mass.** 12.0 kg × 0.692 = **8.31 kg**. The saving is **3.69 kg** per satellite.
3. **Natural frequency.** The stiffness $k$ and the carried mass are unchanged, so $f = \tfrac{1}{2\pi}\sqrt{k/m}$ stays the same or rises slightly.
4. **Launch value.** At a reported rideshare price of about $7 000 per kilogram in 2026, 3.69 kg is worth about **$25 800** per satellite. For a batch of 100 satellites it is 369 kg.

The mass saving is real but modest per part. Its main value is often margin: kilograms freed for propellant, payload or growth late in the programme.
:::

### Generative Design in Practice

Commercial **generative design** tools wrap topology optimisation in a friendlier workflow. The engineer marks surfaces to keep, such as bolt holes, and zones to leave empty, such as an optical path. The tool returns many shapes, each checked for stress, frequency and how it can be made.

Industry uses such tools widely. RUAG Space, now Beyond Gravity, topology-optimised an antenna support bracket for Sentinel-1 and printed it in aluminium. It was half the mass of the original part and exceeded its stiffness requirement by more than 30 %; it was qualified for flight around 2016.

At NASA's Goddard Space Flight Center, research engineer Ryan McClelland has used such tools since about 2020 to design what he calls **evolved structures**. NASA reports that they can be up to two-thirds lighter than conventional parts, and that designs take an hour or two. They have been used on balloon telescopes, instruments and a mount for the since-cancelled Mars Sample Return programme (Chapter 29).

The best-documented case is a bracket for the **EXCITE** balloon telescope (@tbl:excitebracket and @fig:excitephoto). The bracket holds a 1.35 kg tip/tilt mirror stage to the back of the telescope. It must survive 10 g vertically and 3 g sideways. Its first natural frequency must be above 100 Hz, and its target mass was 0.2 kg.

| Design | Time | Mass (kg) | 1st mode (Hz) | Stress (MPa) | Cost, lead time |
|---|---|---|---|---|---|
| Human, best of 4 | 2 days | 0.27 | 65 | 103 | No quote |
| Generative, milled | ≈ 1 hour | 0.20 | 147 | 14.8 | $1 000, 3 days |
| Generative, printed | ≈ 1 hour | 0.20 | 177 | 11.2 | $2 000, 3 weeks |

: The EXCITE tip/tilt bracket: four human design iterations against generative designs that met the 0.2 kg target and the 100 Hz requirement. Data: R. McClelland, NASA Goddard (2023). {#tbl:excitebracket}

The human designs did not meet the frequency requirement at an acceptable mass. The generative designs met both, with seven to nine times less peak stress. McClelland stresses that people must still review every result. Left alone, the algorithm can make members too thin to build or inspect.

![The EXCITE balloon-borne telescope hanging in a hangar at NASA's Columbia Scientific Balloon Facility in Fort Sumner, New Mexico, before its test flight on 31 August 2024. Several of its mounts were evolved structures designed with generative software.](figures/photos/ch52_excite.jpg){#fig:excitephoto width=60%}

### Computational Engineering of Whole Systems

A rocket engine couples flow, combustion, heat transfer and structure. The Dubai company **LEAP 71** calls its approach **computational engineering**. Its software, Noyron, encodes engineering rules, physics and manufacturing limits as code, and generates a whole engine from a short specification. It is closer to an expert system than to a neural network: "AI-designed" can mean many things.

The results are measured by hot fire, not by claims. In June 2024 LEAP 71 fired a 5 kN kerosene–oxygen engine at Airborne Engineering in Westcott, UK. In December 2024 a printed aerospike of similar thrust ran hotter than intended, and the data were fed back into the model. In December 2025 the company reported two 20 kN methane–oxygen engines printed in a copper alloy. They went from specification to first firing in under three weeks. The bell-nozzle engine reached more than 93 % combustion efficiency. The aerospike reached its design chamber pressure of 50 bar but had problems at start-up. Engines of 200 kN and 2 000 kN were in manufacturing trials in 2026.

### Designing for the Printer

Printing changes what is cheap. In laser powder-bed fusion, a laser melts metal powder in layers about 30–60 µm thick. Complex internal channels cost little more than plain walls. But steep overhangs need supports, thin walls warp, and trapped powder and internal flaws must be found. Good design tools include these rules, so the optimiser proposes shapes that can be printed, cleaned and inspected.

## Exploring the Trade Space

The key idea of this section is sample efficiency. A detailed simulation of a spacecraft may take hours. Learning methods help by choosing which simulations to run.

### Multidisciplinary Design Optimisation

A spacecraft is a coupled system. A larger solar array gives more power but adds mass, drag and inertia. That changes the attitude control system, which changes power needs again. **Multidisciplinary design optimisation (MDO)** treats the whole design as one problem:

$$ \min_{\mathbf{x}} f(\mathbf{x}, \mathbf{y}) \quad \text{subject to} \quad g_j(\mathbf{x}, \mathbf{y}) \le 0, \qquad \mathbf{y}_i = A_i(\mathbf{x}, \mathbf{y}_{j \ne i}) . $$

Here $\mathbf{x}$ holds the design variables, such as orbit altitude. Each discipline $A_i$ — structures, thermal, power, orbit — computes outputs $\mathbf{y}_i$ that others need, and the constraints $g_j$ hold the requirements. Frameworks such as NASA's open-source OpenMDAO link the discipline codes and compute gradients. ESA's Concurrent Design Facility, open since 1998, does the same job with people and linked models.

When each evaluation is cheap, any optimiser works. When each takes hours, the number of runs becomes the limit. A surrogate model then stands in for the expensive analysis.

### Surrogate Models

A **surrogate** (or emulator) is a fast approximation fitted to a modest number of expensive runs. Engineers have used polynomial "response surfaces" for decades. **Gaussian processes (GPs)** are now the standard choice for small data sets (Chapter 43). A GP predicts both a mean $\mu(\mathbf{x})$ and an uncertainty $\sigma(\mathbf{x})$. The uncertainty grows away from the runs already made. That is exactly what is needed to decide where to look next.

### Bayesian Optimisation

**Bayesian optimisation (BO)** uses the GP to choose each new run. It scores every candidate design by an **acquisition function**. The most common is the **expected improvement** over the best value so far, $f^\ast$:

$$ \mathrm{EI}(\mathbf{x}) = \big(\mu - f^\ast\big)\,\Phi(z) + \sigma\,\phi(z), \qquad z = \frac{\mu - f^\ast}{\sigma} , $$

where $\Phi$ and $\phi$ are the cumulative and density functions of the standard normal distribution. The first term rewards designs that are predicted to be good. The second rewards designs that are uncertain and might be good. The run with the highest EI is made, the GP is refitted, and the loop repeats.

@fig:bayesoptdesign tests the method on a toy model of an Earth-observation smallsat. It stands in for an expensive simulation. There are four design variables: orbit altitude, telescope aperture, solar-array area and propellant mass. Lower orbits give sharper images but decay sooner unless propellant is carried. A larger aperture sharpens images but adds mass and heater power. The goal is image value per million dollars over the satellite's life. The best design lies at 428 km with a 0.44 m aperture, a 4.9 m² array and 16 kg of propellant.

![Bayesian optimisation against random search on a toy smallsat design model. (a) The Gaussian-process surrogate after four runs, along one variable, with its uncertainty band; expected improvement (EI) picks the next run where the model is both promising and uncertain. (b) Best design found against the number of expensive evaluations, over 12 independent runs. (c) Evaluations needed to come within 5 % of the optimum.](figures/out/ch52_bayesopt.svg){#fig:bayesoptdesign width=100%}

Only 0.38 % of random designs come within 5 % of the optimum. Random search therefore needs about 266 evaluations on average to find one. Bayesian optimisation needed a median of 22, and 11 of its 12 runs got there within 40. After 40 evaluations its median result was 97.6 % of the optimum, against 88.6 % for random search. Random search needed about 500 evaluations to reach 97 %.

::: example
**Example: simulations saved by Bayesian optimisation**

Suppose each evaluation in @fig:bayesoptdesign is a coupled thermal, structural and orbit simulation taking 8 hours on 256 processor cores.

1. **Runs to get within 5 % of the optimum.** Random search: about **266** on average. Bayesian optimisation: median **22**. The saving is 244 runs.
2. **Computer time.** 244 runs × 8 h = **1 952 hours**, or 81 days if run one after another.
3. **Core-hours.** 1 952 h × 256 cores ≈ **500 000 core-hours**. At an assumed $0.03 per core-hour, that is about **$15 000** of computing.
4. **Calendar time.** BO is sequential: 22 runs take 7.3 days. Random runs can be spread over many machines; with 10 in parallel, 266 runs take 8.9 days. Batch versions of BO choose several runs at once to close this gap.
5. **The real gain.** The computing cost is small. The calendar time and the engineer's attention are what matter, and BO gives a better design in the same time.

BO works best with up to about 20 variables and a smooth objective. With hundreds of variables, gradient-based MDO is usually better.
:::

### Neural Surrogates and Neural Operators

A GP becomes slow beyond a few thousand runs, because its cost grows with the cube of the number of points. For large simulation archives, **neural surrogates** take over. A neural network is trained on thousands of past simulations. It then predicts a new case in milliseconds. **Neural operators**, such as the Fourier neural operator (Chapter 44), learn a mapping from one field to another. For example, they can map a wing shape and flow conditions to the whole pressure field around it.

Uses include aerodynamic databases for launchers and capsules, thermal maps of electronics boxes and fast stress checks inside optimisation loops. Investors have noticed: PhysicsX (London) raised $135 million in June 2025 and Neural Concept (Switzerland) $100 million in December 2025. Both sell learned simulation tools to aerospace and other industries.

Two cautions apply. First, a surrogate is only trustworthy inside the range of its training data; Chapter 44 shows how errors explode outside it. Second, the final design must be checked with the full, validated simulation and by test. A surrogate is a tool for search, not for certification.

## AI for Systems Engineers

The key idea of this section is that language models are good at reading and drafting text, and poor at guaranteeing truth. They help most where a person checks every output.

### Checking Requirements

A good requirement is necessary, clear, verifiable and states one thing (Chapter 4). Bad ones contain "weak" words such as *adequate*, *as appropriate* or *user-friendly*, open values such as "TBD", or two requirements joined by "and". Rule-based checkers have flagged such patterns since the 1990s. NASA's Automated Requirement Measurement tool, for example, counted weak phrases and options in specifications.

Language models go further. They can judge whether a requirement is testable, suggest a measurable rewrite and find conflicts between documents. Researchers at the University of Strathclyde trained **SpaceTransformers** (2021). These language models were further trained on space-systems text and tested on recognising concepts in requirements from the European ECSS standards. Domain training improved results over general models. Still, any rewrite is a suggestion. A wrong unit or a lost tolerance in a requirement can survive into hardware.

### Searching Lessons Learned

Agencies hold decades of lessons in reports that few people read. **Retrieval-augmented generation (RAG)** combines a search engine with a language model (Chapter 44). The question is used to find relevant passages in a trusted archive, and the model answers from those passages with citations. ESA researchers built **SpaceQA**, a question-answering system over reports from ESA's Concurrent Design Facility. NASA teams have proposed and prototyped similar tools for the NASA Lessons Learned system and for tracing requirements. One team building a NASA retrieval tool found that some "wrong" answers were in fact correct. The guidance in the source documents had changed. A RAG system is only as current and as correct as its archive.

### Models from Text

**Model-based systems engineering** keeps the design in a connected model rather than in documents (Chapter 4). Its language, SysML, gained a textual form in **SysML v2**, formally adopted by the Object Management Group in 2025. A textual language is something language models can write. Research teams have built systems that draft SysML v2 models from natural-language descriptions. They report that a language model alone often produces invalid syntax. Adding a grammar checker and retrieval of correct examples makes the drafts much better. These are research tools in 2026.

### Code and Tests

Code assistants draft functions, unit tests and scripts. The evidence on productivity is mixed. In a controlled trial published by METR in July 2025, 16 experienced open-source developers completed 246 tasks. When AI tools were allowed, they took 19 % longer, although they believed they had been 20 % faster. Quality is also a concern. A 2022 study had a code assistant complete 89 security-relevant scenarios. About 40 % of the 1 689 programs it produced contained a vulnerability.

For flight software the rules do not change: NASA's NPR 7150.2 and ECSS-E-ST-40 still demand reviews, tests and traceability, whoever wrote the code. Assistants are most useful for ground tools, documentation and test cases. A person decides which tests are meaningful, and the tests themselves check the code.

### Data Security and Export Control

Engineering data are often export-controlled under ITAR or EAR (US export-control rules) or commercially sensitive. Sending them to a public online service can break the law or a contract, so agencies and primes use approved, access-controlled deployments. NASA's digital-engineering team used commercial language models to draft internal procedures. This saved months of work, and every output was treated as a draft to verify.

@tbl:seassist summarises the tools for systems engineers and the check that each one needs.

| Task | How AI helps | Main risk | Required check |
|---|---|---|---|
| Requirement quality | Flags vague, compound or untestable text; suggests rewrites | Changed meaning, lost tolerances | Owner approves every change |
| Lessons-learned search | Retrieves and summarises past reports with citations | Out-of-date or invented answers | Read the cited source |
| Traceability | Proposes links between requirements, design and tests | Missing or false links | Review by the systems engineer |
| SysML v2 drafting | Writes model text from descriptions | Invalid syntax, wrong semantics | Grammar check and model review |
| Code and tests | Drafts functions, test cases and scripts | Subtle bugs, security flaws | Standard review, static analysis, test |
| Report drafting | Turns data and notes into a draft | Plausible but wrong numbers | Check every number against its source |

: AI tools for systems engineers, the main risk of each and the check it needs. {#tbl:seassist}

## Manufacturing and Test

The key idea of this section is that factories produce data at a scale people cannot inspect by eye. Learning sorts the data so that people look first at what most likely matters. The cost of a missed flaw sets how the sorting is tuned.

### From One-Off to Mass Production

For most of the space age, satellites were built one at a time. That has changed (@fig:satproduction). In 2025, 4 511 payloads were launched, nineteen times as many as in 2015. Starlink satellites made up 70 % of them. Most payloads launched in 2025 weighed 500–2 500 kg, because Starlink's current satellites fall in that class.

![The shift to mass production. (a) Payloads launched each year, with Starlink shown separately; 2026 is to 13 October. (b) The share of payloads by mass class: small satellites rose from 2013, then mass-produced constellation satellites of 500–2 500 kg took over.](figures/out/ch52_production.svg){#fig:satproduction width=98%}

Factories now build satellites at rates once reserved for aircraft parts (@tbl:satfactories). SpaceX's filing for its 2026 share sale reported that its plant in Redmond, Washington, averaged about 70 Starlink satellites per week from December 2025 to April 2026. Amazon's factory in Kirkland, Washington, is designed to build up to five satellites per day at peak. Amazon says its test process there cut test time per satellite from months to days.

| Producer | Satellites | Rate | Source and status |
|---|---|---|---|
| SpaceX, Redmond (USA) | Starlink | ≈ 70 per week (Dec 2025–Apr 2026) | SpaceX share-sale filing, 2026 |
| Amazon, Kirkland (USA) | Amazon Leo (formerly Kuiper) | Up to 5 per day at peak | Company, design capacity |
| ICEYE (Finland) | Radar satellites | ≈ 50 per year, 100 planned from 2027 | Company |
| Typical science mission | One spacecraft | One in 5–10 years | — |

: Satellite production rates reported for 2025–26. {#tbl:satfactories}

At 70 satellites a week, no team can examine every weld, scan and test trace in detail. Statistical process control, automated inspection and anomaly detection become part of the production line. The same tools serve one-off science missions, where each part is precious and a missed flaw may end the mission.

### Watching the Printer

A metal printer builds a part from thousands of layers. Each layer is a chance for a flaw. **Lack-of-fusion** voids form where the laser did not melt enough powder. **Keyhole** pores form where it melted too deeply and trapped gas. Spatter, recoater streaks and warping cause other defects. Cameras, photodiodes and thermal sensors can watch every layer and every melt track. A build may produce tens of gigabytes of images.

Oak Ridge National Laboratory's **Peregrine** software is a leading example. It segments layer images with a convolutional network (Chapter 44) into classes such as powder, part, spatter and streaks, and raises alerts during the build. It was trained using X-ray computed tomography (CT) of finished parts as ground truth, and works with many makes of printer. By 2023, 15 US government laboratories used it, and 14 research licences had been granted to industry.

How small a flaw can such monitoring find? Non-destructive evaluation answers this with a **probability-of-detection (POD) curve**. Many flaws of known size are inspected, and each is recorded as a hit or a miss. A logistic curve in the logarithm of flaw size $a$ is fitted:

$$ \mathrm{POD}(a) = \frac{1}{1 + \exp\!\big(-(\ln a - \mu)/\sigma\big)} . $$

The key number is $a_{90/95}$: the flaw size found 90 % of the time, with 95 % confidence. For fracture-critical parts, the structure must tolerate any flaw smaller than this size (Chapter 5).

![Simulated in-situ monitoring of powder-bed fusion. (a) A melt-pool image of one layer; boxes mark spots darker than the local background. (b) Hit/miss probability-of-detection curves for an in-situ camera and for X-ray CT, with the 90/95 flaw size of each.](figures/out/ch52_ammonitor.svg){#fig:ampod width=98%}

@fig:ampod shows the idea with simulated data. A camera with 80 µm pixels blurs small flaws into the background. Its $a_{90/95}$ came out at about 406 µm. A CT scan with 25 µm voxels found flaws down to about 51 µm. These numbers are illustrative. Real values depend on the machine, the metal and the sensor, and must be measured for each process. The lesson holds, though. In-situ monitoring is a fast first screen and a record of the build. It does not replace CT for critical parts.

### Seeing Inside: CT and Visual Inspection

X-ray CT gives a 3-D density map of a part. A single scan holds billions of voxels, and an expert may need an hour to review it. A **classifier** can screen the scan and flag regions that look like pores or lack-of-fusion flaws. The expert then reviews only those regions.

Every screening model must choose a **threshold**. Above it a region is flagged; below it the part passes. The best threshold depends on what errors cost. Let a review cost $C_\mathrm{rev}$ and a missed defect cost $C_\mathrm{esc}$ (an "escape"). For a defect prevalence $\pi$, the expected cost per part is

$$ \text{cost} = (\text{fraction flagged}) \times C_\mathrm{rev} + \pi\,(1 - \text{recall})\, C_\mathrm{esc} , $$

where recall is the fraction of defects caught. If the model's probabilities are well calibrated, decision theory gives a simple rule: flag a part when $P(\text{defect}) > C_\mathrm{rev}/(C_\mathrm{rev} + C_\mathrm{esc})$. With a review costing $1 500 and an escape $250 000, the optimal threshold is about 0.6 %, not the 50 % that software uses by default.

@fig:ctinspection tests this on simulated CT patches. The patches contain pores and lack-of-fusion flaws. They also contain things that look like flaws but are not: ring and streak artefacts of the scanner, part edges and dense inclusions. Three screens were compared. The first is a classic **local-contrast rule**: smooth the image and flag the darkest spot relative to its surroundings. The second is a small neural network that sees the raw pixels. The third combines the two scores with a logistic regression.

![Screening synthetic X-ray CT patches. (a) Examples: sound material, a ring artefact, a pore and a lack-of-fusion flaw. (b) ROC curves of three screens; dots mark the minimum-cost operating points, and the square the network at its default threshold of 0.5. (c) Expected cost per part against the fraction of parts flagged; both baselines are far more expensive.](figures/out/ch52_inspection.svg){#fig:ctinspection width=100%}

The combined screen had the largest area under the ROC curve, 0.974, against 0.961 for the network and 0.946 for the rule. But the ranking by cost was closer than the ranking by ROC area. At the lowest-cost threshold, chosen on a separate validation set, the combined screen cost $521 per part. The rule cost $543 and the network alone $709. The network at its default threshold of 0.5 missed one defect in six and cost $1 381 per part. A well-designed physical rule is a strong baseline; a learned model must beat it where it matters.

::: example
**Example: cost–benefit of an inspection model**

A factory prints 2 000 flight parts a year. About 3 % contain a defect. Reviewing a part's CT scan costs $1 500; an escaped defect costs $250 000 on average, through later test failures, rework and mission risk. Use the results in @fig:ctinspection.

1. **No screening.** 2 000 × 0.03 × $250 000 = **$15.0 million** a year of expected escape cost.
2. **Expert review of every part.** 2 000 × $1 500 = **$3.0 million** a year, assuming the experts miss nothing.
3. **Combined screen at its best threshold.** It flags 22.2 % of parts (444 reviews) and catches 97.5 % of defects. The cost is 2 000 × $521 = **$1.04 million**, a saving of **$1.96 million** a year against full review.
4. **Escapes.** 2 000 × 0.03 × (1 − 0.975) = **1.5 defective parts** a year still escape. With the network at its default threshold, about **10** would escape.
5. **Sensitivity.** If escapes cost ten times more, the best threshold moves lower and more parts are reviewed. If the model is retrained or the printer changes, the threshold must be checked again.

The saving comes from choosing the threshold with real costs, not from a higher ROC area. For fracture-critical parts, the residual escapes must also be covered by design margins and proof tests.
:::

### Composites and Electronics

Carbon-fibre parts are checked by **ultrasonic C-scans**, which map echoes from inside the laminate, and by **thermography**, which watches heat spread after a flash. Classifiers learn to flag the patterns of delaminations, porosity and wrinkles. Electronics boards pass through **automated optical inspection (AOI)**, and X-ray machines check hidden solder joints. Deep learning has cut the false calls that used to send many good boards for manual review. Throughout, the threshold is tuned to the cost of escapes, and each model is rechecked on new production lots.

### Test Data: Vibration and Thermal Vacuum

Every flight unit goes through environmental tests (Chapter 4): vibration, acoustic, shock and thermal vacuum (@fig:shakerneos). A vibration test of a spacecraft may record hundreds of accelerometer channels. Before and after each full-level run, a **low-level sine sweep** measures the natural frequencies. If a main frequency shifts by more than a few per cent, something may have loosened or cracked. Engineers compare these "signatures" by eye, channel by channel.

Anomaly detection can make this comparison for every channel and flag the few that changed (Chapter 49 explains the methods). In thermal vacuum tests, models of expected temperatures flag a heater that switches too often or a sensor that drifts. Real test failures are rare, so most methods learn what "normal" looks like and flag departures. The test conductor makes the final call.

### Supply-Chain Risk

A spacecraft contains parts from hundreds of suppliers, some with a single source. **Supply-chain risk analytics** combine purchase records, supplier finances, news, export rules and shipping data. They flag parts at risk of delay, counterfeiting or obsolescence, as a ranked list for buyers and engineers to act on.

![The bus structure of NASA's NEO Surveyor on a shaker table at BAE Systems in Boulder, Colorado, during vibration testing in August 2025, with mass simulators standing in for the telescope and sunshade.](figures/photos/ch52_shaker.jpg){#fig:shakerneos width=54%}

## Launch: Where Learning Stays on the Ground

The key idea of this section is that the decisions made on board a rocket in flight use optimisation and fixed rules that can be verified. Learning helps on the ground: in tests, forecasts, schedules and analysis.

### Why Landing Guidance Is Optimisation

A booster must land on a small target at zero speed, within thrust limits. Chapter 48 shows how **convex optimisation** solves this problem. A convex problem has a single optimum, and modern solvers find it in a bounded number of steps. That gives three guarantees that a learned controller lacks. If a solution exists, it will be found. Every constraint will hold. The time needed can be bounded. Masten's tests of the G-FOLD algorithm in 2012–13 used this approach, and SpaceX engineers have described using it to land Falcon 9 boosters (@fig:f9landing).

A neural-network policy might land well in simulation, but it offers no such guarantees outside its training conditions (Chapter 48). Learning can still help by giving the solver a good starting guess, which speeds it up while the solver keeps every constraint.

![A Falcon 9 first stage landing at Landing Zone 40, Cape Canaveral Space Force Station, on 1 October 2026, after launching NASA's SpaceX Crew-13 mission. SpaceX engineers have described its landing guidance as convex optimisation solved in real time.](figures/photos/ch52_landing.jpg){#fig:f9landing width=50%}

### Engine and Vehicle Health

A turbopump that fails can destroy an engine in less than a second. **Redlines** — fixed limits on pressure, temperature or vibration — shut the engine down if any limit is crossed. They are simple, fast and verifiable. But a fixed limit must allow for every normal operating condition, so it is often set high and trips late.

A learned detector can find faults earlier by modelling how each sensor *should* behave at the current operating point. The residual — measured minus predicted — is small in normal running. Several residuals $\mathbf{e}$ are combined by the **Mahalanobis distance**,

$$ d^2 = \mathbf{e}^\top \boldsymbol\Sigma^{-1} \mathbf{e} , $$

where $\boldsymbol\Sigma$ is the covariance of the residuals in normal runs. This distance weights each residual by its usual spread and allows for correlations between channels.

@fig:enginehealth compares the two approaches on 300 simulated hot fires with a growing bearing fault. The engine throttles between 80 % and 109 % of rated power. The fixed redline, set just above the highest normal vibration, gave a median warning of only 5 seconds; 19 % of failures came with no warning at all. The learned detector gave a median warning of 58 seconds, with false alarms in 0.7 % of normal runs. Earlier warning in test means less damage to expensive test hardware.

![Health monitoring of simulated turbopump hot fires. (a) One run with a growing bearing fault: overall vibration stays under the fixed redline almost until failure. (b) The learned anomaly score crosses its threshold much earlier. (c) Warning time before failure over 300 faulty runs: the learned detector warns about a minute early, the redline only seconds early or not at all.](figures/out/ch52_engine.svg){#fig:enginehealth width=98%}

Why not fly the learned detector? A false shutdown in flight can lose a mission, and a learned model can fail on conditions it never saw. Learned detectors are used in ground tests, such as the RS-25 firings in @fig:rs25cert, and in analysis after flight. On board they are at most advisory, unless they meet the assurance standards of Chapter 53.

::: history
**Landmark: the Shuttle's Advanced Health Management System (2006–11)**

- The Space Shuttle main engine (SSME, later RS-25) ran its high-pressure turbopumps at tens of thousands of revolutions per minute. A failed bearing or blade could destroy the engine.
- The Advanced Health Management System upgraded the engine controller with digital signal processors and new software. It watched turbopump vibration in real time against a **vibration redline**, and could shut down an engine if vibration grew too high.
- It first flew in monitor-only mode on STS-116 in December 2006 and was then made active.
- The logic was deterministic: fixed signal processing and limits, verified like any flight software.
:::

![A full-duration hot fire of an RS-25 engine on the Fred Haise Test Stand at NASA's Stennis Space Center on 29 February 2024, during certification of new production engines for SLS. Each test records hundreds of sensor channels.](figures/photos/ch52_rs25.jpg){#fig:rs25cert width=62%}

### Weather, Lightning and the Range

Weather causes about half of all scrubs at Cape Canaveral (Chapter 37), and lightning rules are the hardest to meet. A model from NASA Marshall and the University of Alabama in Huntsville detected 84 % of lightning 15–30 minutes ahead, with a 22 % false-alarm rate. The Air Force Institute of Technology has trained models to automate the 45th Weather Squadron's daily lightning forecast (Chapter 47). The launch-commit criteria themselves remain fixed rules.

Busy ranges also need scheduling. Florida's Space Coast hosted a record 109 launches in 2025 and planned for 100–120 in 2026. Each launch needs a pad, a window, hazard areas at sea and in the air, tracking assets and recovery ships. Choosing a conflict-free timetable is an optimisation problem. Learning helps predict the inputs, such as the chance of a scrub or of a ship entering a hazard area. Launch teams rehearse these decisions in simulations (@fig:lccsim).

![The Artemis launch team in Firing Room 1 of the Launch Control Center at Kennedy Space Center during an Artemis II countdown simulation on 8 October 2025. Simulations like this test software, procedures and people against realistic failures.](figures/photos/ch52_lcc.jpg){#fig:lccsim width=50%}

### Flight Safety: Deterministic by Design

An **autonomous flight safety system (AFSS)** decides on board whether to end a flight that strays (Chapter 34). It uses the vehicle's own navigation and fixed rules, such as "terminate if the impact point crosses this line". Its first operational use was on Falcon 9 in February 2017. Here determinism is the point. Every rule can be reviewed, every path tested and every decision explained. Learning enters only upstream, for example in better models of falling debris used to draw the safety lines.

### Trajectories and Mission Design

Trajectory optimisation relies on mature numerical methods (Chapter 24). Learning helps by screening: surrogates estimate the propellant for thousands of candidate transfers in seconds, and networks give the solver starting guesses. The final trajectory is always computed and checked with the full physics.

@tbl:launchroles summarises the division of labour.

| Function | On board in flight | Role of learning |
|---|---|---|
| Landing and ascent guidance | Convex or classical optimisation | Starting guesses; offline design |
| Engine protection | Fixed redlines and logic | Ground-test anomaly detection; setting limits |
| Flight termination | Rule-based AFSS | Debris and risk models used to set rules |
| Launch weather | None (ground decision) | Lightning, wind and cloud forecasts |
| Range scheduling | None (ground decision) | Predicting scrubs, conflicts and delays |
| Trajectory design | Stored or optimised trajectory | Surrogates, warm starts, screening |

: Who decides what during a launch: verifiable logic on board, learning on the ground. {#tbl:launchroles}

## The Space Business

The key idea of this section is that the space business sells answers and manages risk. Learning turns satellite data into decisions. Statistics prices the risk of launch and operations. Optimisation sizes and prices the capacity of constellations.

### Selling Answers from Orbit

Most commercial value lies not in pixels but in what they reveal (Chapter 46). Analytics companies count cars, ships, aircraft and containers. They estimate crop yields, measure oil in storage tanks from the shadows of their floating roofs, and track ships. Customers include traders, insurers, governments and supply-chain managers.

Satellite-tracked shipping became big business. In November 2024 the analytics company Kpler agreed to buy Spire's maritime business, which tracks ships from orbit, for about $241 million. The deal closed in 2025. The best-studied use is in finance (see the box).

::: data
**Data box: satellite car-park counts and share prices**

A study published in 2025 in the *Journal of Financial and Quantitative Analysis* tested whether satellite data give investors an edge.

- **Data:** about 4.7 million daily counts of cars in the car parks of 67 078 stores of 44 major US retailers, 2011–2017. The counts came from RS Metrics and Orbital Insight, which used image analysis to count cars.
- **Signal:** an unusual change in how full the car parks were during a quarter predicted the retailer's earnings.
- **Returns:** in the three days around earnings announcements, retailers with fuller car parks beat the market by 1.66 %. Those with emptier car parks fell behind it by 3.10 %. The gap was 4.76 %.
- **Who gained:** mostly short sellers betting on bad news. Individual investors could not use the data, and share trading became less liquid around the reports.
- **Lesson:** satellite analytics carry real information. But unequal access to data can widen the gap between large and small investors rather than making prices fairer.
:::

### Insurance and Risk Models

Insurers cover launch failure and loss of a satellite in orbit. The market is small, with annual premiums of roughly $550–700 million in 2023–25, so one bad year can wipe out several good ones. On Earth, satellites also enable **parametric insurance**. It pays a fixed amount when a measured index crosses a trigger, such as wind speed or flood extent mapped by radar, with no claim assessment. Descartes Underwriting, for example, uses satellite imagery and machine learning to set triggers and pay quickly.

How does an insurer price a rocket that has flown only twice? The simplest honest model treats each flight as a coin toss with an unknown failure probability $p$. Prior knowledge is expressed as a **beta distribution**, $\mathrm{Beta}(\alpha, \beta)$. After $n$ flights with $k$ failures, the updated (posterior) estimate has mean

$$ \hat p = \frac{\alpha + k}{\alpha + \beta + n} . $$

This is the **beta–binomial** model. It lets each flight shift the estimate by an amount that depends on how much was already known.

![Launch risk from data. (a) Orbital launch failure rates by year from 1997 to 2025, with 90 % intervals, over the number of launch attempts. (b) A Bayesian estimate of the failure probability of a new rocket as it builds a record of successes, starting from the reported 45 % failure rate of maiden flights; one success brings it to 30 %, the reported rate for second flights.](figures/out/ch52_launchrisk.svg){#fig:launchfailbayes width=98%}

@fig:launchfailbayes applies the model. Across the world, 70 of 1 652 orbital launch attempts failed in 2016–25, a rate of 4.2 %. Maiden flights fail far more often: about 45 % according to the analysts Seradata, and second flights about 30 % since 1990. A prior of $\mathrm{Beta}(0.9, 1.1)$ has a mean of 45 %. After one success the model gives 30 %, matching the reported second-flight rate. After ten straight successes it gives 7.5 %, and after 20 it gives 4.1 % — the rate of the mature fleet. One failure in the first three flights keeps the estimate at 12.7 % even after ten more successes. Real underwriters add engineering judgement, the record of the company and the cost of the payload.

::: data
**Data box: space insurance, 2023–25**

- **2023:** the worst year on record. Claims were about $995 million against premiums of about $557 million. Two satellites caused most of the loss: ViaSat-3 Americas, whose large antenna failed to deploy (a claim of about $420 million), and Inmarsat-6 F2, lost to a power failure ($348 million). More than 85 % of losses came after the satellite had separated from the rocket, not from launch failures.
- **2024:** claims fell to about $211 million against premiums of about $580 million (Seradata). Insurers raised rates after 2023, and total working capacity shrank to about $550 million in 2024 and $502 million in 2025 (Gallagher).
- **2025:** a quiet year until the reported loss of the Spanish military satellite SpainSat NG-2 late in the year, insured for about $400 million.
:::

### Constellation Design and Capacity

A broadband constellation sells capacity where its users are. Satellites in an inclined orbit spend most time near the edges of their latitude range. For a circular orbit of inclination $i$, the density of satellites per unit area at latitude $\varphi$ varies as

$$ n(\varphi) \propto \frac{1}{\sqrt{\sin^2 i - \sin^2 \varphi}}, \qquad |\varphi| < i . $$

It is lowest at the equator and highest near latitude $\varphi = i$. @fig:shellcapacity (a) shows the number of satellites in view, above 25° elevation, for shells at 550 km. A shell at 53° inclination gives most coverage near 50° latitude, where much of the demand in North America and Europe lies. A polar shell is needed for high latitudes.

Choosing the mix of shells is an optimisation problem. In @fig:shellcapacity (b), a **linear programme** chooses how many satellites to put in each of five shells. It minimises the total while giving at least 12 satellites in view at 25–50° latitude, 4 elsewhere up to 60° and 2 up to 75°. The answer is 1 766 satellites in a mix of all five shells, with 798 at 53°. A single polar shell would need 3 095 satellites for the same requirement. Real operators solve much larger versions of this problem, with beams, spectrum, ground stations and launch costs. Learning helps with the input that matters most and is least certain: where demand will be.

![Constellation geometry and sizing. (a) Satellites in view above 25° elevation per 1 000 satellites, for shells at 550 km with different inclinations. (b) A linear programme chooses the number of satellites in each shell to meet an illustrative demand profile with the fewest satellites.](figures/out/ch52_capacity.svg){#fig:shellcapacity width=98%}

### Customers, Pricing and Spectrum

Capacity in a constellation is fixed in each place, but demand is not. When a cell fills, the operator must refuse new users or let service slow for everyone. Starlink has done both. From 2024 it charged a one-off "congestion charge" of $100 in some US areas. By 2025–26 the charge was reported at $250 to more than $1 000 in busy areas, and some cities were shown as sold out. Demand models forecast sign-ups by cell, churn models flag users likely to leave, and pricing balances revenue against quality of service.

Spectrum is the other scarce resource. New systems must coordinate their frequencies through the ITU and national regulators and respect interference limits. Learning helps operators detect and locate interference and manage their beams (Chapter 49); the rules themselves are set by treaties.

### AI Companies, Investment and New Demand

Money flowed into space in 2025–26, and much of it was linked to AI. The trackers differ, because they count different things, as @tbl:spacemoney shows. Seraphim reported a record $12.4 billion of space-technology venture investment in 2025. Space Capital, which counts a wider range of companies, reported a record $36 billion in the first quarter of 2026 alone. It named AI, geopolitics and computing in orbit as the drivers.

| Item | Figure | Source and note |
|---|---|---|
| Global space economy, 2025 | $686 billion (+12 %) | Space Foundation, July 2026 |
| Space-tech venture investment, 2025 | $12.4 billion (record) | Seraphim |
| Investment, Q1 2026 | $36 billion, 148 companies (record) | Space Capital (wide definition) |
| Investment, Q1 2026 | $9.4 billion, 82 companies | Novaspace (narrower definition) |
| SpaceX share sale, June 2026 | ≈ $75 billion ($85.7 billion with extra shares) | Largest on record |
| Space insurance premiums, 2025 | ≈ $675 million | Secondary sources |

: Money in the space business, 2025–26. Trackers use different definitions, so their figures cannot be compared directly. {#tbl:spacemoney}

The largest deal joined a space company and an AI company. In February 2026 SpaceX completed an all-share takeover of the AI company xAI. In June 2026 it sold shares to the public for about $75 billion at a valuation of about $1.77 trillion, the largest share sale on record. Its filing reportedly described plans for orbital data centres from about 2028. Google, with Planet, launched a prototype of its Suncatcher computing satellites in October 2026, and Starcloud flew a data-centre graphics processor in 2025. Chapter 45 discusses whether computing in orbit can compete with ground data centres.

AI creates demand for space in three ways. It needs data, such as images and weather records, to train models. It needs connectivity to reach ships, aircraft and remote sites. And, more speculatively, it may move computing itself into orbit. Each claim deserves the usual engineering test: what are the numbers, and has it flown?

## Bringing AI into an Engineering Team

The key idea of this section is that AI tools are engineering tools. They need requirements, verification and configuration control like any other. Teams that treat them this way gain speed without losing safety.

Most failures of AI in engineering are not dramatic. A generated number is copied into a report unchecked. A surrogate is used outside its range. A model trained on last year's printer is used on this year's. Ordinary engineering discipline catches each of them. The practice box gives a short workflow; Chapter 53 covers formal assurance, security and governance.

::: note
**Practice: introducing an AI tool into a spacecraft design team safely**

1. **State the job and the error budget.** Write down what the tool will do and what a wrong answer would cost. Example: "suggest bracket shapes; a wrong shape costs one re-analysis." Avoid uses where errors would reach flight hardware unchecked.
2. **Check the data rules.** Confirm with your export-control and security officers which data the tool may see. Use an approved deployment, and never paste controlled data into public services.
3. **Find a baseline.** Measure how the task is done today, by people or by simple rules. A new tool must beat that baseline on your own data, not on the vendor's examples.
4. **Test on held-out cases.** Keep a set of past problems with known answers that the tool never saw during tuning. Measure errors, false alarms and misses. For classifiers, set the threshold from real costs.
5. **Keep a human gate.** Decide who reviews each output and how. Nothing enters the controlled baseline — drawings, requirements, code or test reports — without the usual analysis, test or review.
6. **Record provenance.** Log the tool, its version, its inputs and the reviewer for each output that is used. Store this in the digital thread, so that any result can be traced and repeated.
7. **Watch for drift.** Re-check performance when the process, the supplier, the software version or the design space changes. Retire tools that no longer pass.
8. **Share lessons.** Report both successes and failures to the team's lessons-learned system, so that the next project starts from evidence.
:::

::: key
**Key takeaways**

- AI proposes; physics, test and people verify. Every AI output must pass the same verification gate as human work before it enters a controlled design.
- Most "AI-designed" structures rest on topology optimisation. In a 2-D test, it saved about 31 % of mass at equal stiffness. Goddard's EXCITE bracket met mass and frequency targets that four human iterations missed.
- Bayesian optimisation with a Gaussian-process surrogate found a near-optimal design in a median of 22 expensive runs, where random search needed about 266.
- Language models help with requirements, lessons learned, SysML v2 drafts and code. But they make plausible errors, and export-controlled data need approved tools.
- In manufacturing, the value of a screening model comes from choosing its threshold with real costs. In our test, the cost-optimal screen cost a third of full expert review, while the default threshold missed one defect in six.
- On rockets in flight, guidance, engine protection and flight safety use optimisation and fixed rules. Learning works on the ground: health monitoring in tests, weather, scheduling and design.
- In the business, AI turns satellite data into market signals, prices risk and sizes constellations. AI-linked investment and the SpaceX–xAI merger reshaped space finance in 2026.
:::

::: questions
**Review questions**

1. Explain why the SIMP method raises density to a power $p \approx 3$. What would happen with $p = 1$?
2. A topology-optimised bracket uses 40 % of the material of a solid block and is 1.7 times as compliant. What fraction of the solid material would a uniform plate of equal stiffness need, and what is the mass saving?
3. How does an evolutionary algorithm differ from a gradient-based optimiser? Give one advantage and one disadvantage of each.
4. Write the expected-improvement formula and explain the role of each of its two terms. Why does Bayesian optimisation need fewer evaluations than random search?
5. Name three tasks in systems engineering where language models help. For each, describe the check that must follow.
6. What does $a_{90/95}$ mean on a probability-of-detection curve, and why is it needed for fracture-critical printed parts?
7. A review costs $1 000 and an escaped defect $400 000. With calibrated probabilities, what threshold minimises the expected cost? Why is the default of 0.5 a poor choice?
8. Give three reasons why landing guidance uses convex optimisation rather than a learned policy.
9. Using a $\mathrm{Beta}(0.9, 1.1)$ prior, estimate the failure probability of a new rocket after five consecutive successes. How does one early failure change the picture?
10. Explain why satellites in a 53° shell give more coverage at 45° latitude than at the equator. How would an operator use this in planning capacity?
:::
