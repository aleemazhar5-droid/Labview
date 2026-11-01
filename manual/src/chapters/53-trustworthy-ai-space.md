---
title: "Trustworthy AI for Space: Assurance, Security, Governance and Outlook"
hero: ch53
abstract: Machine learning now helps to forecast weather, screen images, plan operations and steer robots. Before a learned function may act on its own in space, engineers must show that it is safe, secure and lawful. That is hard: behaviour is learned from data rather than written down, and it can fail silently when conditions change. The chapter reviews the standards that appeared in 2024–26 and the main assurance methods — design domains, testing, formal verification, runtime monitors and assurance cases — with small experiments that show their strengths and limits. It covers attacks on learned systems and their defences, the fast-changing law of AI, the energy cost of computing and an outlook to 2035. It ends with a review of Part XIII.
---

A spacecraft's flight software is among the most carefully checked code in the world. Every requirement is written down, every line is traced to a requirement, and every branch is tested. A neural network breaks this pattern. Its behaviour is not written by people. It is learned from examples and stored in millions of numbers that nobody can read. Yet Chapters 43–52 show learned functions spreading into weather forecasting, image screening, operations, navigation and design. The question is no longer whether AI can help, but how far we can trust it and how we can show that trust to others.

This chapter is about that showing. **Assurance** means collecting evidence that a system is good enough for its job, and building an argument from that evidence that an independent reviewer can check. The hero image shows NASA's Katherine Johnson Independent Verification and Validation Facility in Fairmont, West Virginia. Since 1993, engineers there who are independent of each project have checked the software of NASA missions. Learned software needs the same scrutiny, with new tools.

The chapter explains why learned systems are hard to assure, surveys the standards and describes assurance methods, with small experiments run for this book. It then covers attacks, law and ethics as of October 2026, and an outlook to 2035. It closes Part XIII with a synthesis. Learning methods are explained in Chapters 43 and 44, and onboard hardware in Chapter 45.

## Why Learned Systems Are Hard to Assure

The key idea of this section is that classical assurance checks code against a written specification. A learned model has neither readable code nor a complete specification, so the evidence must come from data, tests and protection around the model.

### Behaviour Learned from Data

A learned model $f_\theta$ has parameters $\theta$ chosen to make the average loss small on $n$ training examples (Chapter 43). What matters in service is the loss on the inputs it will actually meet, drawn from the operational distribution $P_\mathrm{op}$.

$$ \hat R(\theta)=\frac{1}{n}\sum_{i=1}^{n}\ell\big(f_\theta(\mathbf{x}_i),y_i\big), \qquad R_\mathrm{op}(\theta)=\mathbb{E}_{(\mathbf{x},y)\sim P_\mathrm{op}}\,\ell\big(f_\theta(\mathbf{x}),y\big). $$

If training, test and operational data all come from the same distribution, the test error is a fair estimate of $R_\mathrm{op}$. If they do not — a **distribution shift** — nothing in training limits the error. Four problems follow:

- **The specification gap.** Nobody can define "a crater" or "a safe landing site" completely in words. The labelled examples become the real specification, so the data must be checked as carefully as requirements.
- **Opacity.** The model is a large set of numbers. No single number maps to a requirement, and code-coverage measures used for normal software say little about what a network has learned.
- **Shift.** Light, seasons, detectors and targets change. A model can be excellent on its test set and poor in orbit, often without any sign that it is wrong.
- **Fragility.** Tiny, carefully chosen changes to an input can flip the output (see the section on security). Models with the same test accuracy can also behave very differently on unfamiliar inputs.

### A Small Experiment in Distribution Shift

@fig:shift53 makes these points concrete. A small neural network learns to label 16 × 16-pixel surface patches as plain ground, crater or boulder. The patches are synthetic. Each is drawn from a height map and lit by the Sun using a simple shading law. In training the Sun always comes from the west, between 20° and 45° above the horizon. That set of conditions is the model's **operational design domain (ODD)**: the conditions in which it is meant to work.

![Distribution shift in a learned crater and boulder classifier. (a) Example patches; the bottom row lies outside the training conditions. (b) Accuracy under noise, a halved detector gain, blur, and changes of Sun elevation and direction. (c) Accuracy and the share of craters called boulders as the Sun moves away from the training direction.](figures/out/ch53_shift.svg){#fig:shift53 width=100%}

Inside its domain the network is 99.2 % accurate. It shrugs off some changes that look large to a person. With noise of 0.2 (half the brightness of an average pixel), accuracy is still 92.1 %, and halving the detector gain changes almost nothing. Other changes are fatal. With the Sun 90° from the training direction, accuracy falls to 47.7 %. With the Sun from the east, it falls to 34.3 %, no better than guessing among three classes. More than 90 % of craters are then called boulders, because a crater lit from one side looks like a boulder lit from the other. Very low or very high Sun and strong blur also cost 21–27 points.

Three lessons carry over to real systems. The ODD must list every factor that changes the input, not just the obvious ones. Each factor must be tested across its range, including just outside the domain. And the failures are silent. With the Sun from the east, 95 % of the wrong answers came with more than 90 % confidence.

### How Classical Flight Software Is Assured

Space and aviation software standards share one idea: the worse a failure's consequences, the more evidence is required. The European standards ECSS-E-ST-40C (software engineering) and ECSS-Q-ST-80C (software product assurance), both revised in April 2025, assign each function a **criticality category** from A to D. The category follows from the severity of the worst hazard it can cause. NASA's NPR 7150.2D classifies software from Class A (human-rated) to Class F (general computing). Civil aviation uses DO-178C (also published as ED-12C), with design assurance levels (DAL) A–E. @tbl:criticality53 compares the schemes.

At the top levels, every requirement is traced to code and tests, and structural coverage shows that tests exercised every decision in the code. **MC/DC**, for example, requires each condition in a decision to be shown to change the outcome on its own. A network has almost no branches, so such measures are trivially met and prove nothing. The new ML guidance therefore adds evidence about data, learning and runtime behaviour on top of the classical process.

| Scheme | Levels | Top level means | What the top level demands | Status of ML |
|:---|:---|:---|:---|:---|
| ECSS-Q-ST-80C Rev.2 (2025) | Categories A–D | Failure can cause loss of life or of the system | Full verification, independent review, strict coverage | ML handbook covers B–D only |
| NASA NPR 7150.2D (2022) | Classes A–F | Human-rated software | Full process, IV&V where required | Handbook topics added 2025 |
| DO-178C / ED-12C (2011) | DAL A–E | Catastrophic failure condition | 71 objectives; MC/DC structural coverage | No ML provisions; ED-324 in work |
| EASA AI concept papers | AI levels 1–3 | Level 3: advanced automation | Learning assurance plus classical assurance | Level 3 in consultation (2026) |

: How space and aviation standards rank software by criticality, and where machine learning stands in October 2026. MC/DC: modified condition/decision coverage. {#tbl:criticality53}

## Standards and Guidance, 2024–26

The key idea of this section is that the first ML assurance standards now exist, but they are mostly guidance for lower criticality. No standard yet allows a learned function to be the only protection against a catastrophic failure.

@tbl:standards53 lists the main documents. Space has one dedicated document so far. **ECSS-E-HB-40-02A**, the European machine-learning handbook, was published on 15 November 2024. It covers whether to use ML at all, data management, training, model verification, system-level evaluation and a **safety cage** architecture (described below). It is guidance, not a binding standard, and covers criticality categories B–D; category A is out of scope for now. In 2025 NASA added topics on AI to its Software Engineering Handbook, under the existing NPR 7150.2 classes.

| Document | Body and date | Scope | Status, October 2026 |
|:---|:---|:---|:---|
| ECSS-E-HB-40-02A | ECSS, Nov 2024 | ML handbook: data, training, verification, safety cage | Guidance; categories B–D |
| ECSS-E-ST-40C Rev.1, ECSS-Q-ST-80C Rev.2 | ECSS, Apr 2025 | Space software engineering and assurance | In force |
| NPR 7150.2D; handbook topics 7.25, 8.25 | NASA, 2022; 2025 | Software classes; AI in engineering and assurance | In force; guidance |
| AI Roadmap 2.0; Concept Paper Issue 2 | EASA, 2023; 2024 | Learning assurance, AI levels 1–2 | Guidance; Issue 3 consulted Jun–Aug 2026 |
| NPA 2025-07 | EASA, Nov 2025 | First AI rules for aviation | Proposal; consultation closed 2026 |
| ED-324 / ARP6983 | EUROCAE WG-114, SAE G-34 | Process standard for aeronautical AI | Drafting |
| ISO/IEC 22989, 23053 | ISO/IEC, 2022 | AI concepts, terms, ML framework | Published |
| ISO/IEC 23894; 42001 | ISO/IEC, 2023 | AI risk management; AI management system | Published; 42001 certifiable |
| ISO/IEC TR 24029-1; 24029-2 | ISO/IEC, 2021; 2023 | Robustness of neural networks; formal methods | Published |
| ISO/IEC TR 5469 | ISO/IEC, Jan 2024 | Functional safety and AI | Published (report) |
| AI RMF 1.0; AI 600-1 | NIST, 2023; 2024 | Voluntary risk framework; generative-AI profile | Revision ordered 2025; none by Oct 2026 |
| UL 4600 | UL, 2020; 3rd ed. 2023 | Safety cases for autonomous products | Published |

: Standards and guidance for assuring AI, as of October 2026. {#tbl:standards53}

Aviation is further ahead, and space engineers follow its lead. The European Union Aviation Safety Agency (EASA) defines three **AI levels**. Level 1 assists a human. Level 2 is human–AI teaming. Level 3 is "advanced automation", with little or no human oversight. EASA's Concept Paper Issue 2 (2024) gave guidance for Levels 1 and 2. In November 2025 EASA proposed its first binding AI rules, in Notice of Proposed Amendment (NPA) 2025-07. A proposed Issue 3 of the concept paper, published on 3 June 2026, extends the guidance to reinforcement learning and to Level 3. A joint EUROCAE–SAE group, set up in 2019, is drafting the process standard ED-324 (ARP6983 in the USA); it was unpublished in October 2026.

General standards come from the joint ISO and IEC committee on AI. ISO/IEC 42001 (December 2023) defines an AI management system that organisations can be certified against, as ISO 9001 does for quality. ISO/IEC TR 5469 (January 2024) covers AI inside safety functions, conventional safety functions guarding AI, and AI used to design safety functions. The voluntary AI Risk Management Framework of the US National Institute of Standards and Technology (NIST) has four functions: govern, map, measure and manage. A revision ordered in July 2025 had not appeared by October 2026. **UL 4600** is the best model for the argument itself. Instead of prescribing a process, it asks for a complete, checkable **safety case** for an autonomous product.

::: history
**Landmark: the first design-assurance study for neural networks (2020–21)**

- In 2019–20 EASA and the Swiss company Daedalean studied how a neural network could be certified for a safety-related avionics task. The case study was a camera-based system guiding an aircraft to a runway.
- Their March 2020 report, *Concepts of Design Assurance for Neural Networks* (CoDANN), introduced **learning assurance**: evidence about the data, the learning process and generalisation, added to the usual software assurance.
- It proposed the **W-shaped process** (@fig:wshape53): the classical V of design and verification, with a second V for data and learning inserted in the middle.
- A second study (May 2021) applied the ideas to visual traffic detection, and the US Federal Aviation Administration assessed them in 2022. These studies shaped the EASA concept papers and the ECSS handbook.
:::

![A W-shaped learning-assurance life cycle, simplified after the EASA concept papers. Orange steps are new for machine learning; dotted lines link each verification step to the step it checks. In operation, monitoring and incidents feed new data and a new pass through the W.](figures/out/ch53_wshape.svg){#fig:wshape53 width=92%}

## Building the Evidence: Assurance Methods

The key idea of this section is that no single method is enough. Assurance combines a defined domain, good data, tests, small proofs and runtime protection, tied together in an argument.

### Design Domain, Data and Requirements

Everything starts with the **ODD**. For a lunar hazard detector, it lists altitude, speed, Sun elevation and azimuth, terrain types, dust, camera settings and sensor health, each with a range. The data must then **cover** the domain: every combination that matters must appear often enough to train and test on. Coverage is never complete in many dimensions, so engineers sample key factors on grids, fill the rest randomly and record what is missing.

Data need their own paperwork. A **datasheet** for a dataset (proposed in 2018) records how the data were collected and labelled, who labelled them, how they were split and what is known to be missing. A **model card** (2019) records what a model is for, how it was tested, on which slices of the domain, and its known limits. Both are now part of the model registry in a good machine-learning operations (MLOps) pipeline (Chapter 45).

**Requirements for an ML component** go beyond "accuracy above 99 %". They state performance for each slice of the domain, such as each Sun elevation band, and cover robustness, stability, calibrated confidence (Chapter 44), timing, memory and behaviour under radiation upsets (Chapter 45). Each must be testable and traced to evidence.

### Robustness Testing

Robustness tests change inputs in controlled ways. **Corruption tests** add noise, blur, compression, stray light, dead pixels and changes of gain, as in @fig:shift53. **Metamorphic tests** use known relations instead of labels. For example, a crater shifted by two pixels must stay a crater. **Adversarial tests** search for the worst input within a small budget (see the section on security below). Tests can show weaknesses but never prove their absence. Still, they are cheap and find most real problems early.

### Formal Verification of Neural Networks

Formal verification aims to **prove** a property for every input in a region, not just for the inputs tested. The usual property is **local robustness**: for an input $\mathbf{x}_0$, no input within distance $\varepsilon$ changes the decision. In the $L_\infty$ norm the region is a box: each input value may move by up to $\varepsilon$.

The simplest sound method is **interval bound propagation (IBP)**. It pushes the whole box through the network layer by layer. Write the box as a centre $\mathbf{c}$ and a radius $\mathbf{r}$. A linear layer with weights $\mathbf{W}$ and bias $\mathbf{b}$ maps it to

$$ \mathbf{c}' = \mathbf{W}\mathbf{c} + \mathbf{b}, \qquad \mathbf{r}' = |\mathbf{W}|\,\mathbf{r}, $$

where $|\mathbf{W}|$ takes the absolute value of every weight. A ReLU unit, $\max(0,z)$, never decreases, so it simply clips both ends of each interval at zero. At the output, if the lowest possible score of the predicted class exceeds the highest possible score of every other class, the property is proved. IBP is fast, but its boxes grow at each layer. It can fail to prove a property that is true.

**Complete** methods give an exact answer: either a proof or a counter-example. They encode each ReLU exactly, either with logic in a satisfiability-modulo-theories (SMT) solver or with a binary variable in a **mixed-integer linear program (MILP)**. The Reluplex solver (2017) used this approach to verify properties of the neural networks proposed for the ACAS Xu aircraft collision-avoidance system. Today's leading tools combine fast bounds with branch-and-bound search. One of them, α,β-CROWN, won the annual international verification competition VNN-COMP every year from 2021 to 2025.

![Proving robustness on a tiny network. (a) A learned "safe or unsafe" boundary for landing sites from slope and rock cover, with the largest box around six test points that interval bound propagation (IBP) can prove robust and the true largest box from an exact mixed-integer solver. (b) Share of test points proved robust against the box size.](figures/out/ch53_ibp.svg){#fig:ibp53 width=100%}

@fig:ibp53 compares the methods on a toy landing-site classifier with two inputs: slope and rock cover. The network has two hidden layers of 16 ReLU units and is 96.4 % accurate. For 106 correctly classified test points, IBP proved a median radius equal to 1.2° of slope. The exact MILP radius was 4.0°: IBP proved, on average, only 46 % of the true radius. A gradient attack found counter-examples only beyond the exact radius, as it must. At a radius of 1° (one degree of slope and one point of rock cover), IBP certified 62 % of points and the exact method 90 %.

The exact method took under a second per point here, but its cost can grow exponentially with network size. Complete verification works for small and medium networks, not for large vision or language models. And local robustness is not correctness: a network can be provably robust and still wrong. Formal methods therefore suit small, critical networks — controllers, monitors, surrogates — and specific properties such as "never command thrust above the limit".

### Runtime Monitors and Safety Cages

If a model cannot be fully verified, it can be **contained**. The **simplex architecture** (Lui Sha, 2001) runs an unverified high-performance controller beside a simple verified one. A verified switch hands control to the simple one whenever the system nears the edge of a safe region. Chapter 48 shows a simplex "shield" on a learned lunar-landing controller. The ECSS handbook calls the general idea a **safety cage** (@fig:cage53). An input monitor checks that inputs lie inside the domain. An output monitor checks that outputs are plausible. A verified arbiter uses the learned result only if both checks pass.

![A safety-cage (simplex) architecture for an onboard learned function. Only the arbiter, monitors and baseline need the highest assurance; the learned function can sit at a lower category.](figures/out/ch53_cage.svg){#fig:cage53 width=94%}

The cage changes the assurance problem. The arbiter, monitors and baseline are small and conventional, so classical methods can verify them to a high category. The learned function then needs less assurance, because its failures are caught.

A common input monitor measures how far an input's internal features lie from the training data. With hidden features $\mathbf{h}$, and class means $\boldsymbol\mu_k$ and covariances $\boldsymbol\Sigma_k$ from training data, the score is the **Mahalanobis distance** to the nearest class.

$$ d^2(\mathbf{x}) = \min_k\,(\mathbf{h}-\boldsymbol\mu_k)^{\mathsf T}\,\boldsymbol\Sigma_k^{-1}\,(\mathbf{h}-\boldsymbol\mu_k). $$

A large $d^2$ means the input looks unlike anything seen in training, so the monitor rejects it. The threshold sets the trade between false alarms and missed detections. A simpler baseline flags inputs for which the network's top **softmax** probability is low.

![Runtime monitoring of the patch classifier. (a) Mahalanobis distances for inputs inside the design domain and for three kinds of input outside it. (b) Receiver operating characteristic (ROC) curves for the Mahalanobis and softmax monitors. (c) Availability against hazardous errors for safety cages built from each monitor.](figures/out/ch53_ood.svg){#fig:ood53 width=100%}

@fig:ood53 tests both monitors on the patch classifier. Three kinds of outside input were used: Sun from the east, a detector fault with bad columns and hot pixels, and an unseen terrain type (a long trough). With the threshold set so that only 5 % of in-domain inputs are rejected, the Mahalanobis monitor caught 92 % of faults and 60 % of unseen terrain. The softmax monitor caught 21 % and 22 %. Neither monitor saw the Sun problem well (30 % and 9 %). A crater lit from the east really does look like a familiar boulder, so the network's features look normal too. The cure is not a better image monitor but a **domain check on data the spacecraft already knows**: the Sun's direction comes from navigation. The design lesson: check the domain directly wherever possible, and use learned monitors only for what cannot be checked directly.

**Uncertainty-aware decisions** extend the idea. The model reports a calibrated probability or a conformal prediction set (Chapter 44), and the logic acts only when the uncertainty is small enough for what is at stake. Otherwise it asks the ground or falls back to a safe default.

::: example
**Example: what a safety cage costs and buys**

Take the patch classifier of @fig:ood53 and a stream of inputs. 90 % lie inside its domain and 10 % outside, split equally among Sun from the east, detector faults and unseen terrain. A **hazardous error** is an input on which the learned function acts and is wrong; a flagged input goes to a safe fallback.

1. **No cage.** In-domain errors: 0.90 × 1.1 % = 1.0 % of all inputs. Outside: 3.3 % × (65 % + 18 % + 100 %) = 6.1 %, since unseen terrain is always mislabelled. Total **7.1 %**, with 100 % availability.
2. **Mahalanobis cage.** Reject inputs with $d^2$ above the 95th percentile of in-domain scores. Availability falls to **89.4 %** and hazardous errors to **3.2 %**.
3. **Add the Sun-angle check.** All Sun-from-east inputs are now rejected. In-domain inputs keep 0.90 × 95 % = 85.5 % availability with 0.65 % errors. Faults that slip through add 0.3 % availability and almost no errors. Unseen terrain passes 40 % of the time, adding 1.3 % to both. Total: availability **87.1 %**, hazardous errors **2.0 %**.
4. **Trade.** The cage cut hazardous errors by a factor of 3.6 for a loss of 12.9 points of availability. Two-thirds of the remaining hazard is unseen terrain, so the next step is an output check, such as a slope from lidar, not a tighter threshold.

A cage turns an unbounded failure mode into a known rate of fallbacks. Whether the trade is worth it depends on what the fallback costs: a slower landing, a lost image, or an aborted manoeuvre.
:::

::: history
**Landmark: a neural network flies a satellite under a watchdog (2026)**

- In July 2026 the US Air Force Research Laboratory (AFRL) reported a new flight test. A neural network had controlled a CubeSat's attitude for one orbit without human help.
- The network was trained by reinforcement learning (Chapter 48), then tested in simulation and in the laboratory before upload.
- Two runtime-assurance systems flew with it in **shadow mode**: an "AI watchdog" that detects unverified situations and would switch to backup systems, and a "guardrail" that would intervene near predefined safety limits. They observed and logged, but did not take control.
- AFRL gave no performance figures, and the flight was a demonstration. But it follows the pattern this chapter recommends: learned control, conventional limits, and evidence from shadow mode before monitors get authority.
:::

### Testing, Simulation and Independent Review

Statistical testing gives the most direct evidence: run the function on many independent inputs drawn from the domain and count failures. If $n$ tests show no failures, the failure probability $p$ is below a bound $p_\mathrm{U}$ with confidence $C$ when $(1-p_\mathrm{U})^n = 1-C$. Rearranged,

$$ n = \frac{\ln(1-C)}{\ln(1-p)} \approx \frac{-\ln(1-C)}{p}, $$

which at 95 % confidence gives the "rule of three": $n \approx 3/p$ (@fig:tests53).

::: example
**Example: how many tests prove a failure rate below 10⁻⁴?**

A learned hazard detector must mislabel fewer than one landing-site image in 10 000, with 95 % confidence.

1. **No failures allowed.** $n = \ln(0.05)/\ln(1-10^{-4}) =$ **29 956** independent test images, close to $3/p = 30\,000$.
2. **Other confidence levels.** At 90 %, 23 025 images; at 99 %, 46 049.
3. **One failure seen.** If one test fails, the campaign must grow to **47 437** images to support the same claim (binomial distribution).
4. **A smaller campaign.** 10 000 images with no failure support only $p < 3.0 \times 10^{-4}$.
5. **The catch.** The images must be independent and drawn from the operational domain. A thousand frames from one descent are not a thousand independent tests. For aviation's catastrophic level of 10⁻⁹ per flight hour, the same rule needs 3 × 10⁹ hours, about 342 000 years of testing.

Testing alone can support moderate failure rates. Rare-failure claims need architecture: a verified cage around the learned part, so that its failures are caught rather than merely counted.
:::

![What testing can show. (a) Independent tests needed to demonstrate a failure probability, for several confidence levels and with one failure allowed. (b) The 95 % upper bound on the failure probability after a test campaign, for 0, 1 or 5 failures seen.](figures/out/ch53_tests.svg){#fig:tests53 width=96%}

**Simulation** supplies the volume. Landers, rovers and rendezvous systems are tested on millions of simulated scenarios, with **scenario coverage** measured over the ODD. But a learned model can exploit flaws of the simulator, and synthetic images differ from real ones (the sim-to-real gap; Chapter 45). The answer is a ladder of evidence: simulation, then hardware-in-the-loop tests with real cameras and computers, field and flight tests (@fig:morpheus53), and shadow-mode operation in space.

Three other kinds of evidence complete the picture:

- **Explainability as evidence.** Attribution maps (Chapter 44) show which inputs drove a decision and catch shortcuts, such as a ship detector that looks at the quay. They only support other evidence: methods can disagree, and a plausible map does not prove a correct model.
- **MLOps traceability.** Every deployed model must be traceable to its code, data version, settings and test results, so that it can be rebuilt and an anomaly traced to its cause (Chapter 45).
- **Independent verification and validation (IV&V).** A team that did not build the model repeats key tests, writes its own adversarial cases and reviews the argument. This matters even more for ML, because the developers' data choices are themselves a source of error.

![NASA's Morpheus prototype lander lifting off on free flight 15 at Kennedy Space Center in December 2014. During the 97-second flight its autonomous landing and hazard avoidance sensors surveyed a field of hazards, chose a safe site and guided the lander to it. Flight tests like this close the gap between simulation and reality.](figures/photos/ch53_morph3.jpg){#fig:morpheus53 width=56%}

@tbl:methods53 summarises what each method can and cannot show.

| Method | What it shows | Main strength | Main limit | Use in space, 2026 |
|:---|:---|:---|:---|:---|
| Design domain and data coverage | Data match the conditions of use | Basis for all other evidence | Never complete in many dimensions | ECSS and EASA guidance |
| Statistical testing | Bound on failure rate | Simple and convincing | About 3/p independent tests | Standard practice |
| Robustness tests | Stability to noise, blur, attacks | Finds weaknesses early | Cannot show their absence | Growing practice |
| Formal verification | Proof over an input region | A real guarantee | Small networks, local properties | Research; aviation benchmarks |
| Runtime monitors, safety cage | Catches outside inputs and bad outputs | Handles the unknown | Misses look-alikes; costs availability | Flight demos (shadow mode) |
| Explanations | Which inputs drove a decision | Reveals shortcuts | Not proof; methods disagree | Reviews and audits |
| Simulation, hardware in the loop | System behaviour in many scenarios | Volume and rare cases | Sim-to-real gap | Standard for autonomy |
| Traceability, IV&V | What was built, checked by others | Audit and repeatability | Discipline and cost | NASA IV&V since 1993 |

: Assurance methods for learned functions: what each shows and its limits. {#tbl:methods53}

### Putting It Together: the Assurance Case

The evidence is joined by an **assurance case**: a structured argument that a system is acceptably safe (or secure) for a given use in a given domain. **Goal Structuring Notation (GSN)** draws it as a tree (@fig:gsn53). Each goal is a claim. A strategy explains how it is broken into sub-goals. Each sub-goal ends in evidence. Context and assumptions are stated, so that a reviewer can attack them.

::: note
**Practice: writing an assurance case for an onboard ML function**

1. **State the claim and its limits.** Write the top goal in one sentence naming the function, the hazard and the domain. "The detector does not make landing less safe inside its domain" is checkable; "the AI is safe" is not.
2. **Define the domain.** List every factor that changes the input — light, geometry, terrain, sensor state, radiation — with ranges. Note which factors the spacecraft can measure directly.
3. **Fix the criticality.** Run a hazard analysis. Decide which parts must reach which category, and design a cage so that the learned part can sit at category C or D.
4. **Choose a strategy.** Argue over the life cycle (requirements, data, learning, implementation, operations) and over the runtime protection. Assign each sub-goal an owner.
5. **Collect evidence for each sub-goal.** Datasheet and coverage report; tests per domain slice with confidence bounds; robustness and adversarial tests; proofs for the monitor; bit-exact checks on the flight computer; radiation and fault-injection results.
6. **Attack your own case.** List "defeaters": ways each claim could be false. Unseen terrain, label errors, a monitor blind spot. Add evidence or change the design until each is answered.
7. **Get independent review.** A team that did not build the system reviews the case and data; record their findings and your answers.
8. **Keep it alive.** Every retraining, new domain or anomaly in orbit reopens the case. Version it with the model.
:::

![An assurance case in Goal Structuring Notation for a learned hazard detector on a lunar lander (simplified). Each claim must end in evidence that a reviewer can inspect.](figures/out/ch53_gsn.svg){#fig:gsn53 width=96%}

## Security: Attacks on Learned Systems

The key idea of this section is that learning creates new ways to attack a system. An attacker can target the data, the model or the inputs, as well as the computers and links around them.

Learned systems add attacks at every stage of the life cycle (@tbl:attacks53). NIST's taxonomy of adversarial machine learning (March 2025) groups them into evasion, poisoning and privacy attacks, plus supply-chain and prompt-injection attacks on generative AI.

| Attack | Stage | What the attacker needs | Example | Main defences |
|:---|:---|:---|:---|:---|
| Evasion (adversarial examples) | Operation | Control of inputs | Patches hid aircraft from a detector (2020, Ch. 50) | Robust training, input checks, sensor fusion |
| Poisoning and backdoors | Training data | Write access to a data source | 0.01 % of a web-scale set for $60 (2023) | Provenance, hashes, data audits |
| Model extraction and inversion | Deployment | Query access | Copying a cloud analytics model | Rate limits, privacy-preserving training |
| Supply chain | Development | A shared model or library | About 100 malicious models on a public hub (2024) | Signed artefacts, safe file formats, scans |
| Prompt injection, leakage | Operation | Text the assistant will read | Instructions hidden in a log or document (Ch. 49) | Treat text as data; limit tools; human approval |
| Classic cyber attack | All | Network access | KA-SAT modems wiped (2022, Ch. 49) | Segmentation, encryption, NIST IR 8401 |

: Attacks on learned systems across the life cycle, with examples and defences. {#tbl:attacks53}

### Adversarial Examples

An **adversarial example** is an input changed slightly, on purpose, so that a model gets it wrong. Such inputs were first described in 2013. The simplest way to make one is the **fast gradient sign method (FGSM)** of 2014. It moves every pixel by $\varepsilon$ in the direction that most increases the loss:

$$ \mathbf{x}' = \operatorname{clip}_{[0,1]}\big(\mathbf{x} + \varepsilon\,\operatorname{sign}\nabla_{\mathbf{x}}\,\ell(f_\theta(\mathbf{x}),y)\big). $$

**Projected gradient descent (PGD)** repeats small steps of this kind and keeps the result within $\varepsilon$ of the original. It is the standard strong attack for testing.

@fig:fgsm53 attacks the patch classifier of @fig:shift53. Random noise of up to ±26 grey levels (of 255) hardly matters: accuracy stays above 97.9 %. A crafted change of only ±8 levels cuts accuracy to 77.6 % with FGSM and 74.5 % with PGD. At ±13 levels PGD leaves 50.2 %, and at ±26 levels 18.0 %. The example crater, 96 % "crater" before the attack, becomes a 99.6 % "boulder", yet a person sees no difference. **Adversarial training**, which mixes attacked examples into training, helps: the retrained network keeps 95.3 % against PGD at ±8 levels and 85.2 % at ±13. It still falls to 47.7 % at ±26 levels.

How real is the threat in space? A digital attack needs access to the pixels — in the onboard computer, the ground pipeline or the data link — so normal cyber security is the first defence. **Physical** attacks need no such access. Printed patches, paint patterns and decoys can change what a sensor sees (Chapter 50). Defences are layered: robust training, input checks, several sensors (optical and radar rarely share the same blind spot), and people reviewing important decisions.

![Adversarial examples on the patch classifier. (a) A crater, an FGSM change of at most ±8 grey levels per pixel, and the result, which the network calls a boulder. (b) Accuracy against the size of the change for random noise, FGSM and PGD attacks, and for a network trained on adversarial examples.](figures/out/ch53_fgsm.svg){#fig:fgsm53 width=100%}

### Poisoning, Backdoors and the Supply Chain

**Data poisoning** inserts bad examples into training data. A **backdoor** is a poisoning that teaches the model a hidden trigger: the model behaves normally until a pattern appears, then outputs what the attacker wants. Large datasets built from the web are easy targets. In 2023 a team showed that, for about US$60, an attacker could have bought expired internet domains hosting images for two popular web-scale datasets. Through them, it could have controlled 0.01 % of a dataset of hundreds of millions of image–text pairs. Space datasets are smaller and better curated, but they are open and re-used, so labels, benchmarks and archives need provenance checks and cryptographic hashes.

**Pre-trained models** are a supply-chain risk like any third-party software. In February 2024 security researchers found about 100 models on a popular public model hub that ran hidden code when loaded, through an unsafe file format. Most were probably tests by other researchers, but one opened a remote connection to the user's computer. A downloaded model must be treated as untrusted code: loaded only in safe formats, scanned and signed.

A model offered as a service can also be **extracted** — copied by training on its answers — or probed to reveal its training data (**model inversion** and **membership inference**). Rate limits, coarse outputs and training that limits memorisation reduce the risk.

### Language Models in Operations

Language-model assistants (Chapters 44 and 49) add two specific risks. In **prompt injection**, text that the assistant reads — a web page, an email, an anomaly report — contains instructions that it follows, even if the attacker never talks to the assistant. **Data leakage** happens when an assistant reveals confidential procedures, keys or personal data it has seen. The defences are architectural. Treat all retrieved text as data, never as commands. Give the assistant the fewest tools and permissions it needs. Keep a human approval step before any command reaches a spacecraft.

### Securing AI-Enabled Space Systems

Learned components live inside ordinary space systems, so classical space cyber security comes first (Chapters 7 and 49). NIST's report IR 8401 (December 2022) applies its Cybersecurity Framework to the satellite ground segment. The Aerospace Corporation's **SPARTA** framework (first released in October 2022) catalogues attacks on spacecraft: in 2026 it listed 9 tactics and 85 techniques. In Europe, the NIS2 directive already covers operators of space ground infrastructure. The proposed EU Space Act of June 2025 would add space-specific cyber rules; it was still being negotiated in October 2026.

::: data
**Data box — attacking satellites on purpose, 2023**

- **OPS-SAT (April 2023).** In an exercise run with ESA before the CYSAT conference in Paris, four researchers from Thales took control of the application environment of ESA's OPS-SAT test satellite. They inserted code that could, for example, mask areas in its images. ESA kept control of the satellite throughout.
- **Moonlighter (June 2023).** The Aerospace Corporation and the US Space Systems Command built Moonlighter, a CubeSat designed to be hacked. It launched on 5 June 2023 on a cargo flight to the ISS.
- **Hack-A-Sat 4 (August 2023).** At the DEF CON 31 conference in Las Vegas, five finalist teams attacked Moonlighter in orbit. An Italian team, mHACKeroni, won the US$50 000 first prize.
- **Why it matters for AI.** The OPS-SAT attack could alter imagery at the source. A learned function downstream would analyse falsified data with full confidence, so integrity checks belong before the model.
:::

A sound defence for an AI-enabled mission combines four layers:

- **Protect the pipeline**: signed data, models and code; separate networks for training, ground operations and commanding; secure model upload with rollback (Chapter 45).
- **Harden the model**: adversarial and corruption tests, robust training and monitoring of input statistics.
- **Contain the model** in a safety cage, so that a fooled model cannot command a hazardous action.
- **Keep people in the loop** for irreversible decisions, and train them to spot a model under attack.

## Governance, Law and Ethics

The key idea of this section is that AI law is moving fast and differs between regions. In October 2026 it touches space mostly through data, ground services and products sold on Earth, and less through onboard functions.

### The European Union AI Act

The **AI Act**, Regulation (EU) 2024/1689, is the first broad AI law. It entered into force on 1 August 2024 and sorts AI uses by risk. Unacceptable practices, such as social scoring, are banned. These bans, and a duty to build staff AI literacy, apply from 2 February 2025. **High-risk** systems — for example safety components of critical infrastructure, or AI in products under EU safety law such as medical devices — need risk management, data governance, logging, human oversight, accuracy and robustness. They also need conformity assessment. Providers of **general-purpose AI models** have had transparency and copyright duties since 2 August 2025. Fines for banned practices reach €35 million or 7 % of world turnover. AI used only for military or national-security purposes is excluded.

In 2026 a "digital omnibus" amendment, agreed in May and published in July, delayed the rules for stand-alone high-risk systems to 2 December 2027, and for high-risk AI in regulated products to 2 August 2028. Transparency duties, such as labelling AI-generated content, still apply from August 2026. For space engineers the main routes into the Act are data services used in critical infrastructure and, through EASA's rules, AI in aviation; NPA 2025-07 is partly a response to the Act. Most onboard spacecraft functions are not listed as high-risk, but customers increasingly ask for the same evidence.

### The United States

US policy turned in 2025 from managing AI risk to accelerating adoption. Executive Order 14110 of 2023 was revoked on 20 January 2025. Executive Order 14179 (23 January 2025) and America's AI Action Plan (July 2025) stress innovation, infrastructure and exports. Memoranda of April 2025 tell federal agencies to appoint chief AI officers, list their AI uses and apply minimum practices to "high-impact" ones. Executive Order 14365 (December 2025) directs federal action against state AI laws judged "onerous". A national policy framework of March 2026 asked Congress to pre-empt conflicting state laws. As of October 2026 there is no general federal AI statute, and state AI laws continue to apply. Military AI rules are described in Chapter 50.

### China, the United Kingdom and Others

**China** regulates specific services. Interim measures for generative AI services, with registration of algorithms, took effect in August 2023. Rules requiring visible and hidden labels on AI-generated content took effect on 1 September 2025. An amendment adding the first AI article to the Cybersecurity Law, adopted in October 2025, took effect on 1 January 2026. The **United Kingdom** has no general AI law. It relies on existing regulators applying shared principles. Its AI Safety Institute was renamed the AI Security Institute in February 2025.

### International Agreements

The **Council of Europe Framework Convention on AI** is the first binding international treaty on AI and human rights. It opened for signature in Vilnius on 5 September 2024. The EU ratified it in May 2026, but it needs five ratifications, including three Council of Europe member states, to enter into force. At the United Nations, the **Global Digital Compact** (September 2024) led to resolution 79/325 of August 2025. It created an Independent International Scientific Panel on AI, whose 40 members were appointed in February 2026, and a **Global Dialogue on AI Governance**. The Dialogue first met in Geneva on 6–7 July 2026, shortly after the Panel released a preliminary report. A series of summits — Bletchley Park (2023), Seoul (2024), Paris (2025) and New Delhi (February 2026) — produced non-binding declarations. The New Delhi Declaration had 91 signatories, including the USA, the UK and China. @tbl:governance53 summarises the main instruments.

| Instrument | Jurisdiction | Type | Key dates | Status, October 2026 |
|:---|:---|:---|:---|:---|
| AI Act, Reg. (EU) 2024/1689 | European Union | Binding, risk-based | In force Aug 2024; bans Feb 2025 | High-risk rules delayed to Dec 2027 and Aug 2028 |
| Executive orders, Action Plan, OMB memos | United States | Executive policy | Jan–Jul 2025; Dec 2025 | No general federal AI law; state laws apply |
| Generative-AI measures, labelling rules | China | Binding regulations | Aug 2023; Sep 2025 | In force; AI added to Cybersecurity Law Jan 2026 |
| Sector-based principles | United Kingdom | Regulators' guidance | 2023–25 | No general AI law |
| Framework Convention on AI | Council of Europe | Treaty | Opened Sep 2024 | Ratified by the EU; not yet in force |
| Global Digital Compact; Scientific Panel; Global Dialogue | United Nations | Non-binding | 2024; 2025; Jul 2026 | Panel report Jul 2026; next Dialogue May 2027 |
| New Delhi Declaration | 91 signatories | Non-binding | Feb 2026 | Signed |

: Main AI governance instruments as of October 2026. Military AI is covered in Chapter 50. {#tbl:governance53}

### Export Controls

Space hardware has long been export-controlled; the USA eased licensing of some spacecraft items to close allies in October 2024. Advanced AI chips have been controlled since 2022. A US rule of January 2025 that would have limited chip and model-weight exports worldwide was rescinded in May 2025. In January 2026 the USA moved some high-end chips to case-by-case licensing for China, combined with a 25 % import duty. Engineers buying processors for an AI payload, or sharing models and training data with foreign partners, should check controls early (Chapter 50).

### Agency Principles and Human Oversight

NASA published a *Framework for the Ethical Use of Artificial Intelligence* in April 2021. It sets six principles: fair; human-centric and societally beneficial; explainable and transparent; accountable; secure and safe; and scientifically and technically robust. NASA appointed its first chief AI officer in May 2024. By October 2026 NASA's web pages referred to the same framework as one for "super intelligence". ESA works through the ECSS standards and EU law. Defence users follow principles such as the US Department of Defense's five of 2020: responsible, equitable, traceable, reliable and governable.

![The Artemis II flight control team in the White Flight Control Room at NASA's Johnson Space Center during the crew's lunar flyby on 6 April 2026. Every principle for trustworthy AI comes back to people like these, who must understand, question and, when necessary, overrule the tools they use.](figures/photos/ch53_artemisfcr.jpg){#fig:artemisfcr53 width=66%}

All these documents call for **meaningful human oversight**. In practice that means operators who understand what a tool can and cannot do (@fig:artemisfcr53). They need the time and information to question it, and the authority to overrule it. It also means guarding against **automation bias**: the tendency to accept a machine's answer because it is usually right. Interfaces should show confidence and reasons, and training should include cases where the tool is wrong.

### Privacy and Dual Use

Satellites now see the ground at 30 cm or better, and some revisit a site many times a day (@fig:lax53). One image reveals little about a person. But learned detectors can track vehicles, ships and crowds over months and link them to other data, building a "pattern of life" that can identify people. The results can then be personal data under laws such as the EU's General Data Protection Regulation. Good practice limits resolution and retention to what a task needs, aggregates results, and logs who queried what. Almost every tool in Part XIII is also **dual-use**: the same detector serves a port authority and an army (Chapter 50).

![Los Angeles International Airport (top) and the surrounding city, photographed from the International Space Station on 29 May 2026. Learned detectors can count aircraft, cars and ships in images like this; combined over time, such counts raise questions of privacy and dual use.](figures/photos/ch53_lax.jpg){#fig:lax53 width=50%}

### The Environmental Cost of Computing

The International Energy Agency estimated that data centres used about 415 TWh in 2024, about 1.5 % of the world's electricity. It expects this to roughly double, to about 945 TWh, by 2030, with AI the main driver (@fig:citylights53). The energy for one training run can be estimated from the compute: a model with $N$ parameters trained on $D$ tokens needs about $C = 6ND$ floating-point operations (Chapter 44). Then

$$ E \approx \frac{C}{F_\mathrm{peak}\,u}\;P_\mathrm{acc}\;k_\mathrm{host}\;\mathrm{PUE}, $$

where $F_\mathrm{peak}$ is the peak speed of one accelerator, $u$ the fraction of it actually used, and $P_\mathrm{acc}$ its power. The factor $k_\mathrm{host}$ adds host computers and networking, and the power usage effectiveness (PUE) adds cooling and other data-centre overheads.

![City lights from Tokyo to Osaka and Hiroshima, photographed from the International Space Station on 15 September 2025. Data centres for AI are a fast-growing part of the electricity demand that lights scenes like this.](figures/photos/ch53_cities.jpg){#fig:citylights53 width=54%}

![Energy and emissions of training. (a) Electricity per training run against compute, for 2020-era efficiency (from a published estimate for a 175-billion-parameter model) and for assumed 2024–26 accelerators. (b) Emissions of the worked example on three electricity grids, and of one year of a popular inference service.](figures/out/ch53_energy.svg){#fig:energy53 width=96%}

::: example
**Example: energy and carbon to train a mid-size model**

Estimate the cost of training a 7-billion-parameter model on 2 trillion tokens — a mid-size language model, or a large Earth-observation foundation model (Chapter 44).

1. **Compute.** $C = 6 \times 7\times10^9 \times 2\times10^{12} = 8.4 \times 10^{22}$ operations.
2. **Accelerator time.** Assume 989 × 10¹² operations per second at peak and 40 % utilisation: $8.4\times10^{22} / (3.96\times10^{14})$ s = **59 000 accelerator-hours**, or 4.8 days on 512 accelerators.
3. **Power.** 0.7 kW per accelerator × 1.3 for hosts and network × PUE 1.2 = 1.09 kW. One run: 59 000 h × 1.09 kW = **64 MWh**.
4. **Real projects.** Failed runs, tuning and evaluation often triple the total: **193 MWh**.
5. **Carbon.** On a low-carbon grid (30 g CO₂/kWh): **5.8 t**. At the 2025 world average of 458 g/kWh: **88 t**. On a coal-heavy grid (800 g/kWh): **155 t**.
6. **Use.** One million queries a day at 0.24 Wh each — a median reported by one large provider in 2025 — need 88 MWh a year, or 40 t CO₂ at the world average. A popular service can use more energy in two years of answers than in training.

For comparison, a 175-billion-parameter model trained in 2020 was estimated at 1 287 MWh and 552 t CO₂; the assumed modern hardware uses about 5 times less energy per operation. The grid changes the carbon by a factor of 27.
:::

Onboard inference uses only a few watts (Chapter 45); the large costs lie on the ground, in training, storage and serving.

### Workforce and Skills

Trustworthy AI needs people who understand both machine learning and safety-critical engineering, and they are rare. Data scientists seldom know hazard analysis, and many assurance engineers have never trained a model. Mixed teams and training on the new standards are closing the gap.

## Outlook to 2035

The key idea of this section is to separate what has happened from what may happen. Projections are marked with a confidence level.

@fig:roadmap53 sets out one view of the next decade. First, the facts as of October 2026. Learned weather forecasts have been operational at the European Centre for Medium-Range Weather Forecasts (ECMWF) since February 2025 (Chapter 47). Foundation models for Earth observation and the Sun are openly available (Chapter 44). Onboard AI has flown on several small satellites (Chapters 45 and 46), and a neural network has flown a satellite's attitude for one orbit. Single operators already run autonomous collision avoidance across thousands of satellites (Chapter 48). No learned function has yet been certified as the sole protection against a catastrophic failure in space or aviation.

![An outlook to 2035. Shaded bars run from first use to the estimated year of routine use (diamonds), coloured by the author's confidence. Grey notes give the status in October 2026. These are projections, not facts.](figures/out/ch53_roadmap.svg){#fig:roadmap53 width=100%}

The projections, with confidence:

- **Foundation models for Earth and space (high confidence).** Shared pre-trained models will be the normal starting point for EO, weather and heliophysics products by about 2030. Assuring a *base model* then becomes a shared task, like qualifying a processor.
- **Certified ML in safety-related functions (medium).** Aviation will probably certify Level 1–2 functions first, once ED-324 and EASA's rules are final. Space will follow at ECSS category B, inside safety cages, in the early 2030s.
- **Autonomous constellations (medium).** Coordination between operators — who moves when two satellites meet — needs shared rules and data more than better models (Chapters 21 and 50).
- **AI-designed spacecraft (low).** Algorithms already shape parts: evolved antennas flew on NASA's ST5 in 2006 (Chapter 52). A spacecraft designed largely by AI is unlikely before 2035, because every design must still be verified.
- **Human–AI teaming on the Moon (low).** Artemis astronauts are expected to land from about 2028 (@fig:ltv53). Assistants for traverses, procedures and medical care will be tried first in analogue tests (@fig:jett53), and trusted only as far as they can explain themselves.
- **Orbital computing and servicing (low).** Both are at the demonstration stage (Chapters 40 and 45) and depend more on hardware and economics than on AI.

::: figrow
![NASA astronauts Joe Acaba and Mark Vande Hei test Lunar Outpost's Pegasus lunar terrain vehicle prototype at Johnson Space Center in September 2026. NASA selected Lunar Outpost and Astrolab in May 2026 to build the first lunar terrain vehicles.](figures/photos/ch53_ltv.jpg){#fig:ltv53}

![Flight controllers at Johnson Space Center guiding simulated moonwalks in Arizona's San Francisco Volcanic Field during the JETT 5 field test in May 2024. Analogue tests like this are where decision-support tools for surface operations can be tried before flight.](figures/photos/ch53_jett.jpg){#fig:jett53}
:::

Several problems remain open:

- **Assuring foundation models** trained by others on data nobody can fully inspect.
- **Monitors with guarantees**: detecting inputs outside the domain that look familiar, as in @fig:ood53.
- **Verification at scale** for convolutional and transformer networks, and for properties beyond local robustness.
- **Assurance of learning in orbit**, when a model updates itself from new data.
- **Agents that act**: language-model systems that use tools need limits that can be checked.
- **Common evidence formats**, so that a model qualified by one organisation can be re-used by another.

## Part XIII in Review

Part XIII began with the foundations of machine learning and ends with trust. @tbl:part13synthesis gathers the main lesson of each chapter.

| Chapter | Topic | Central lesson | Most mature use, 2026 |
|:--|:------|:----------|:-------|
| 43 | AI foundations | Test on data split by place and time; report uncertainty | Classical ML in data products |
| 44 | Deep learning, foundation models | Pre-train once, adapt many times; check calibration | Open EO and weather models |
| 45 | Data, hardware, edge AI | Data and radiation, not algorithms, limit onboard AI | Cloud screening, triage demos |
| 46 | Earth observation | Domain shift and area estimation decide real accuracy | Land cover, floods, methane |
| 47 | Weather, climate, space weather | Learned forecasts rival physics but need its analyses | ECMWF AIFS operational |
| 48 | Autonomy and robotics | Learning helps perception; verified logic keeps control | Rover and avoidance autonomy |
| 49 | Operations and networks | Alert budgets, not accuracy, decide usefulness | Telemetry anomaly tools |
| 50 | SSA, defence, security | Physics carries most of the load; people keep decisions | Tracking, imagery triage |
| 51 | Science and human spaceflight | ML is a funnel; discoveries need independent checks | Planet vetting, alert brokers |
| 52 | Design, manufacturing, launch, business | AI speeds design and inspection; verification stays | Generative parts, inspection |
| 53 | Trustworthy AI | Assure data, model and runtime; contain what cannot be proved | Handbooks; shadow-mode demos |

: Part XIII in one table: the lesson of each chapter and the most mature use as of October 2026. {#tbl:part13synthesis}

Three threads run through all eleven chapters. First, **physics and engineering still carry most of the load**: learning works best as a fast approximation, a filter or a perception layer inside a well-understood system. Second, **data decide everything** — how they were collected, labelled and split, and how far operation differs from training. Third, **trust is earned by evidence and architecture together**. A model is trusted when its domain is defined, its performance honestly measured, its failures contained and its behaviour visible to people. Space has always demanded this discipline; machine learning makes it more necessary, not less.

::: key
**Key takeaways**

- Learned behaviour comes from data, not a written specification, and fails silently outside its design domain. A crater classifier fell from 99.2 % to 34.3 % when the Sun came from the other side, while noise barely mattered.
- The first ML assurance documents exist — ECSS-E-HB-40-02A (2024), EASA's concept papers and NPA 2025-07, ISO/IEC 42001 and TR 5469 — but they cover lower criticality. No learned function is yet the sole protection against a catastrophic failure.
- Evidence combines a defined domain with data coverage, statistical testing (about 3/p failure-free tests: 29 956 for 10⁻⁴), robustness tests, formal proofs for small networks, traceability and independent review.
- A safety cage contains what cannot be proved. Here it cut hazardous errors from 7.1 % to 2.0 % for 12.9 points of availability; checking the domain directly (Sun angle) beat any learned monitor for that factor.
- Attacks target data, models and inputs: changes of ±8 grey levels cut accuracy to 74.5 %, and poisoning web-scale data can cost tens of dollars. Defences are layered: secure pipelines, robust training, cages and people.
- AI law diverges: the EU AI Act's high-risk rules now apply from December 2027 and August 2028; the USA has no general AI statute; China regulates services and labels; international agreements are mostly non-binding.
- Training a 7-billion-parameter model takes about 190 MWh including experiments; the grid changes its emissions 27-fold, and a popular service can use more energy answering queries than training.
:::

::: questions
**Review questions**

1. Write the empirical and operational risks. Why does a low test error say nothing about performance after a distribution shift? Give two space examples.
2. In @fig:shift53, why is the classifier robust to noise and gain but not to the Sun's direction? What would you add to its design domain and its test plan?
3. Compare ECSS criticality categories, NASA software classes and DO-178C levels. Why do structural-coverage measures such as MC/DC say little about a neural network?
4. Describe the W-shaped learning-assurance process. Which steps are new compared with classical software, and what evidence does each produce?
5. Show how interval bound propagation passes a box through a linear layer and a ReLU. Why is it sound but incomplete? What did @fig:ibp53 show about the size of the gap?
6. Draw a safety cage for a learned star-tracker or crater-navigation function. Which parts need the highest assurance category, and why?
7. Using the Mahalanobis monitor results, explain why some outside inputs are hard to detect. How does a direct domain check change the cage's trade between availability and hazard?
8. How many independent failure-free tests demonstrate a failure probability below 10⁻³ with 99 % confidence? Why can testing alone never support 10⁻⁹ per hour?
9. Explain FGSM and PGD. Why does random noise of the same size barely affect the classifier while a crafted change does? List four defences for a spacecraft image pipeline.
10. A company will train a 7-billion-parameter foundation model and sell flood maps from it to an EU water authority. Which legal, security and environmental questions should it answer first?
:::
