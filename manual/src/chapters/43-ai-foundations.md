---
title: "AI Foundations: Machine Learning for Space Engineers"
hero: ch43
abstract: Artificial intelligence now screens clouds on board satellites, flags anomalies in telemetry, maps the planet's forests and plans rover drives on Mars. This chapter gives space engineers the foundations needed to judge, specify and build such systems. It separates symbolic AI — rules, search and planning — from machine learning, traces how each wave of AI reached space from the expert systems of the 1980s to the foundation models of the 2020s, and maps the main problem types and learning paradigms onto space examples. It then explains, with equations and computed examples, how models learn by gradient descent, why they overfit, how classical methods work, how to measure performance honestly for rare events, and how spatial and temporal autocorrelation can make a useless model look excellent.
---

A modern Earth-observation satellite can collect more data in a day than its operators could inspect in a lifetime. NASA's Earth science archive alone held 178.7 PB at the end of September 2025 and was growing by about 160 TB a day; a single Sentinel-2 or Landsat scene contains tens of millions of pixels in a dozen spectral bands. Spacecraft generate their own flood of information too: a large mission may record thousands of telemetry channels, every second, for decades. Nobody can write explicit rules for every pattern hidden in such data. **Machine learning** — programs that improve their performance by learning from examples — has therefore become as much a part of the space engineer's toolkit as orbital mechanics or link budgets.

Machine learning is also easy to misuse. A model can score 99 % accuracy and be useless; it can pass every validation test and fail on the first image from a new region; it can learn the quirks of one sensor rather than the physics of the scene. This chapter builds the foundations needed to avoid these traps. It explains what artificial intelligence (AI) is and is not, how machines learn, which classical methods suit which problems, and how to measure performance honestly. The ten chapters that follow apply these ideas to deep learning, onboard computing, Earth observation, weather, autonomy, operations, security, science, industry and assurance.

## What AI Is — and Is Not

**Artificial intelligence** is the field of building computer systems that perform tasks which normally require human intelligence: perceiving, reasoning, planning, deciding and learning. The term was coined for a workshop at Dartmouth College in 1956. It does not imply consciousness or understanding, and it is not one technique but a family of them (@fig:aitaxonomy).

![How the families of AI relate. Symbolic AI encodes knowledge written down by people; machine learning learns it from data; deep learning is the part of machine learning that uses many-layer neural networks; foundation models are large deep networks pre-trained on huge unlabelled data sets. Statistics and estimation theory overlap machine learning. Every example is a space system discussed in this chapter.](figures/out/ch43_taxonomy.svg){#fig:aitaxonomy width=96%}

### Symbolic and Learned AI

**Symbolic AI** represents knowledge explicitly, in a form that people write and can read: rules ("if the bus voltage is below 26 V and the battery is discharging, then shed heater loads"), logical facts, models of how a system works, and search procedures that explore possible actions. Its main branches are **expert systems**, which apply hundreds or thousands of if–then rules elicited from specialists; **search and planning**, which find a sequence of actions that reaches a goal while respecting constraints; **constraint satisfaction and optimisation**, which find schedules or assignments that satisfy many conditions at once; **model-based diagnosis**, which explains symptoms by reasoning over a model of the hardware; and **fuzzy logic**, which lets rules hold to a degree between true and false.

**Machine learning (ML)** takes the opposite approach: instead of writing the rules, the engineer provides examples and an algorithm finds a function that fits them. A cloud detector is not told that "clouds are bright in the visible and moderately bright at 1.6 µm"; it is shown thousands of pixels labelled "cloud" or "clear" and works out a boundary between them. **Deep learning** is the branch of machine learning that uses neural networks with many layers, which can learn their own features directly from raw images, spectra or time series (Chapter 44). **Foundation models** are very large deep networks pre-trained on enormous unlabelled data sets and then adapted to many tasks.

@tbl:symbolicvslearned compares the two traditions. The boundary between them is not sharp: a rover's planner may call a learned terrain classifier, and a learned model may be wrapped in hand-written safety rules. Many of the strongest space systems combine both.

| Aspect | Symbolic AI | Machine learning |
|---|---|---|
| Source of knowledge | Experts write rules, models, constraints | Algorithm infers patterns from examples |
| Typical methods | Expert systems, search, planners, schedulers, fuzzy logic | Regression, trees, forests, SVMs, clustering, neural networks |
| Space examples | Shuttle INCO expert system, Hubble's SPIKE scheduler, Mars Express MEXAR2 | Sea-surface temperature regression, MODIS land cover, onboard cloud screening |
| Strengths | Transparent, predictable, verifiable against requirements | Handles patterns too complex to write down; improves with data |
| Weaknesses | Brittle outside its assumptions; costly to build and maintain | Needs representative labelled data; can fail silently on new inputs |
| Verification | Test each rule and path; formal methods possible | Statistical testing on held-out data; behaviour between samples uncertain |

: Symbolic AI and machine learning compared. {#tbl:symbolicvslearned}

### Why Symbolic Methods Still Matter in Space

Spaceflight puts a premium on **verifiability**. Flight software must be shown, before launch, to do what its requirements say in every mode the mission can enter (Chapter 6). A rule base or a planner can be reviewed line by line, tested path by path and sometimes proved correct with formal methods. A neural network with millions of weights cannot: its behaviour is known only at the points where it has been tested, and engineers must rely on statistics to argue about everything in between (Chapter 53).

For this reason the safety-critical layers of spacecraft — fault protection, safe modes, attitude control — are still built from explicit logic and classical control theory, while learned models are introduced where their errors are tolerable or can be caught: choosing which images to downlink, flagging telemetry for a human to inspect, proposing a plan that a validated planner then checks. Even the newest systems follow this pattern. When Perseverance drove 210 m and 246 m on 8 and 10 December 2025 along waypoints generated by a generative AI model, every command was first checked on a digital twin of the rover that tracked more than 500 000 telemetry variables, and the rover's own hazard-avoidance software stayed in charge of each step.

### Four Waves of AI in Space

AI reached space in waves, each riding on progress elsewhere in computing (@fig:aispacetimeline).

![Selected milestones of artificial intelligence in space, 1980–2026, sorted into symbolic AI, classical machine learning and deep learning, with general milestones of AI along the bottom. Filled circles mark operational use, diamonds flight demonstrations or pilots and open circles research or prototypes; each is dated by first use.](figures/out/ch43_timeline.svg){#fig:aispacetimeline width=100%}

**Expert systems and schedulers (1980s–1990s).** In 1985 NASA's Johnson Space Center began developing **CLIPS** (C Language Integrated Production System), a rule engine written in C because the LISP-based expert-system tools of the day rarely made it out of the laboratory into operations; released to the public, it is still maintained today. In 1988, during STS-26, two expert systems — one for the Shuttle's communications and instrumentation, used by the INCO flight controller, and one for its main engines — ran in Mission Control for the first time, beside the conventional displays so that controllers could compare them (@fig:incortds). Hubble's long-range observing plan has been built since shortly after its launch in April 1990 with **SPIKE**, a scheduler from the Space Telescope Science Institute (@fig:hubblespike). SPIKE expresses each constraint — Sun and Moon avoidance, target visibility, guide-star availability — as a "suitability" between 0 and 1 over time and searches for a schedule with the highest total suitability. An early stochastic neural network in SPIKE worked so well that its analysis produced the "min-conflicts" repair heuristic, still a standard technique for constraint problems. In May 1999 the Remote Agent experiment took control of Deep Space 1, the first time an AI planner and diagnosis system commanded a spacecraft (Chapter 48).

::: figrow
![Flight controller John Muratore at the INCO console in Mission Control in June 1988, during a simulation for STS-26. Beside him an operator works at the Real Time Data System, an expert-system workstation that monitored Shuttle telemetry.](figures/photos/ch43_inco.jpg){#fig:incortds}

![Hubble raised above Discovery's payload bay before its release in April 1990 (STS-31). Its long-term observing schedule has been built ever since with SPIKE, a constraint-based AI scheduler.](figures/photos/ch43_hubble.jpg){#fig:hubblespike}
:::

**Classical machine learning (1980s–2010s).** Statistical learning arrived quietly, often without the AI label. From the early 1980s NOAA computed sea-surface temperature from AVHRR's thermal channels with coefficients found by regressing satellite measurements against drifting buoys. In the early 1990s JPL and Caltech's SKICAT system used decision trees to classify faint stars and galaxies on the digitised Palomar sky survey, reaching about 94 % accuracy on objects too faint to classify by eye. From 2004 the Earth Observing-1 satellite ran onboard classifiers and a planner that retasked it automatically (see the box below), and from 2010 the AEGIS software let Opportunity and later Curiosity choose their own rock targets. Random forests and gradient-boosted trees became the workhorses of land-cover mapping.

**Deep learning (2012–).** In 2012 a deep convolutional network, AlexNet, cut the error rate of the ImageNet image-recognition contest from 26.2 % to 15.3 %, showing that networks trained on graphics processors (GPUs) could learn visual features better than any designed by hand. Space applications followed within a few years: in 2017 the operations team of NASA's SMAP satellite began piloting a recurrent neural network that flags anomalies in telemetry, and in 2018 JPL used networks pre-trained on everyday photographs to make NASA's archive of Mars images searchable by content. In September 2020 ESA's **Φsat-1** demonstrated a deep network screening an Earth-observation satellite's images for cloud on board, running on a low-power Intel Movidius Myriad 2 vision processor.

**Foundation models and generative AI (2020s).** The **transformer** architecture of 2017 made it possible to train networks with billions of parameters on unlabelled data; the term "foundation model" was coined in 2021. NASA and IBM released the Prithvi geospatial foundation model in 2023; its second version (December 2024) has 300 million or 600 million parameters and was pre-trained on about 4.2 million samples of harmonised Landsat and Sentinel-2 imagery. In February 2025 ECMWF made a machine-learned global weather model operational (Chapter 47). Hardware followed: a satellite carrying a data-centre GPU trained a small language model in orbit in December 2025, Planet's Pelican-4 detected aircraft in its own images over Alice Springs on 25 March 2026, and on 1 October 2026 Google and Planet launched a prototype carrying four tensor processing units for a year-long test (Chapter 45). Most of these are **demonstrations**; the operational systems of 2026 are still dominated by classical methods and carefully bounded deep networks.

## Problems, Data and Ways of Learning

### Ten Kinds of Problem

Before choosing an algorithm, an engineer must say what kind of output is wanted. @tbl:mlproblemtypes maps the ten problem types that cover almost all space applications onto examples from this book.

| Problem type | Output | Space example | Typical methods | Typical metric |
|---|---|---|---|---|
| Classification | A class for each input | Cloud or clear pixel; land-cover type | Boosted trees, random forests, CNNs | Precision, recall, F1 |
| Regression | A continuous value | Sea-surface temperature from radiances; forest biomass | Linear regression, forests, Gaussian processes | RMSE, MAE, bias |
| Semantic segmentation | A class for every pixel, keeping shapes | Flood extent, burn scars, building footprints | Convolutional encoder–decoders | Intersection over union |
| Object detection | Boxes and classes | Ships in radar images, aircraft at airports | CNN detectors | Mean average precision |
| Forecasting | Future values or event probabilities | Solar flares, geomagnetic storms, weather | Trees, SVMs, recurrent and graph networks | Skill scores, Brier score |
| Anomaly detection | "Normal" or "unusual" | Telemetry faults, radio interference | Prediction errors, isolation forests, autoencoders | Event precision and recall |
| Clustering | Groups found without labels | Spectral classes, solar-wind types | k-means, Gaussian mixtures | Cluster purity, Rand index |
| Dimensionality reduction | A few variables that summarise many | 8 461-channel IASI spectra sent as about 300 numbers | PCA, autoencoders | Variance explained |
| Ranking | An ordering by value | Which rock to zap, which image to downlink first | Scoring models | Precision of top-ranked items |
| Decision and control | Actions | Scheduling, rover driving, pointing | Planners, reinforcement learning | Reward, mission return |

: Machine-learning problem types and space examples. {#tbl:mlproblemtypes}

Anomaly detection and ranking show how ML often supports rather than replaces people (@fig:smapweigh, @fig:aegistarget). JPL's telemetry monitor for SMAP and Curiosity, described in 2018, learned to predict each of 82 telemetry channels from its recent history with a recurrent network and flagged values that departed from the prediction by more than a threshold set automatically from the recent errors; on 105 labelled anomaly sequences it achieved a precision of 87.5 % and a recall of 80 %. Even so, its authors reported that false positives kept it from becoming a central part of telemetry review — the usual fate of anomaly detectors whose alarms outnumber real faults. Curiosity's AEGIS software, by contrast, ranks candidate rocks in a navigation-camera image by brightness, size and shape criteria set by the science team and sends the best to the ChemCam laser; over 2.5 km of driving it picked the preferred material more than 93 % of the time, against about 24 % expected without it.

::: figrow
![NASA's SMAP satellite being weighed before launch at Vandenberg in November 2014. Since 2017 its operations team has piloted a neural-network system that flags anomalies in its telemetry.](figures/photos/ch43_smap.jpg){#fig:smapweigh}

![Ranking on Mars: after a 13 m drive on 14 July 2016 (sol 1400), Curiosity's AEGIS software picked the bright outcrop marked in this navigation-camera image (left); within 30 minutes ChemCam had fired its laser at nine points on it (right).](figures/photos/ch43_aegis.jpg){#fig:aegistarget}
:::

### Data, Features and Labels

Every ML problem starts with **data**: a set of examples, each described by **features** $x$ (pixel reflectances, telemetry values, orbital elements) and, for most problems, a **label** $y$ (the right answer). In remote sensing the features are often physical measurements, and good features encode physics. Clouds and snow are both bright at visible wavelengths, but snow absorbs strongly near 1.6 µm while water clouds do not (Chapter 13); a classifier given only visible bands confuses them (@fig:rockiessnow), while one given a short-wave infrared band can separate them. The examples in this chapter use exactly this two-band problem, with synthetic pixels drawn from eight surface and cloud types.

![Snow and cloud over the Rocky Mountains in a natural-colour MODIS image from the Aqua satellite, 19 December 2012. Both are bright in the visible; telling them apart needs a short-wave infrared band, in which snow is dark — the problem modelled in this chapter's examples.](figures/photos/ch43_rockies.jpg){#fig:rockiessnow width=50%}

Labels are usually the scarcest and most expensive ingredient. They come from experts drawing polygons on images, from field campaigns and in-situ sensors such as buoys and weather stations, from crowds of volunteers, from simulations, and from the logs of past operations. They are never perfect: in the EO-1 study described below, the classifiers correctly found small lakes that the expert had missed, and were scored as wrong. Label errors set a floor on the error any model can achieve and, as later sections show, give flexible models something false to memorise.

### Ways of Learning

The learning paradigms of @tbl:learnparadigms differ in what kind of supervision they need. In practice they are combined: a network may be pre-trained without labels, fine-tuned with a few thousand, and improved by asking experts to label the cases it finds most confusing.

| Paradigm | Labels needed | How it learns | Space example |
|---|---|---|---|
| Supervised | A label for every training example | Fits a mapping from features to labels | Onboard classifiers of EO-1; cloud masks |
| Unsupervised | None | Finds clusters or low-dimensional structure | Spectral clustering of images; PCA of IASI spectra |
| Self-supervised | None — the data supply their own targets | Predicts hidden parts of the input, e.g. masked image patches | Prithvi pre-trained on 4.2 million image samples |
| Semi-supervised | A few labels plus many unlabelled examples | Extends labels to similar unlabelled data | Mapping with a handful of field plots |
| Active learning | Chosen by the model | Asks for labels where it is most uncertain | Galaxy Zoo: 35–60 % fewer labelled galaxies needed |
| Transfer learning | Few, for the new task | Reuses a model trained on another task | Photo-trained networks fine-tuned on Mars images |
| Reinforcement learning | None; a reward signal instead | Learns actions by trial and error | Research on scheduling and guidance (Chapter 48) |

: Learning paradigms. {#tbl:learnparadigms}

Galaxy Zoo shows the value of combining people and machines. Launched in July 2007, it attracted about 150 000 volunteers who made some 50 million galaxy classifications in its first year. Its successors trained Bayesian convolutional networks that estimate how uncertain they are about each galaxy and send the most informative ones to volunteers; this **active learning** reduced the number of labelled galaxies needed by 35–60 %, depending on the feature being classified. **Reinforcement learning (RL)**, in which an agent learns a policy that maximises a cumulative reward through trial and error, is the paradigm behind game-playing programs and is being studied for scheduling, guidance and robotic manipulation; its space applications, still mostly in research, are covered in Chapter 48.

## The Mathematics of Learning

### Models, Losses and Empirical Risk

A **model** is a function $f_\theta(x)$ with adjustable **parameters** $\theta$ — two coefficients in a straight-line fit, millions of weights in a neural network. A **loss function** $\ell(f_\theta(x), y)$ measures how wrong a single prediction is. For regression the usual choice is the squared error $(f_\theta(x) - y)^2$. For classification the model outputs a probability $p$ that the label is 1, and the loss is the **cross-entropy**

$$ \ell = -\left[\, y \ln p + (1-y)\ln(1-p) \,\right], $$

which is zero for a confident correct answer and grows without limit for a confident wrong one. Learning means choosing the parameters that minimise the average loss over the $N$ training examples, the **empirical risk**:

$$ \hat R(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell\big(f_\theta(x_i), y_i\big). $$

What we really want is a small loss on future data, the **expected risk**; the empirical risk is only an estimate of it, and the difference between the two — the **generalisation gap** — is the central difficulty of machine learning.

### Gradient Descent

For a few models the minimum can be found in closed form; ordinary least squares, for example, solves a set of linear equations. In general it is found iteratively by **gradient descent**. The gradient $\nabla_\theta \hat R$ points uphill on the loss surface, so each step moves the parameters a little way downhill:

$$ \theta_{t+1} = \theta_t - \eta\, \nabla_\theta \hat R(\theta_t), $$

where the **learning rate** $\eta$ sets the step size. Computing the full gradient over millions of examples at every step is wasteful, so **stochastic gradient descent (SGD)** estimates it from a small random **mini-batch** $B$ of examples:

$$ \theta_{t+1} = \theta_t - \frac{\eta}{|B|} \sum_{i \in B} \nabla_\theta\, \ell\big(f_\theta(x_i), y_i\big). $$

Each step is noisy but cheap, and the noise even helps networks escape poor regions of the loss surface. Practical optimisers such as **Adam** add momentum (an average of recent gradients) and scale each parameter's step by the size of its recent gradients.

The learning rate is the most important setting of all. @fig:gdpaths shows gradient descent on the least-squares loss of a linear model with two strongly correlated predictors — a common situation, since neighbouring spectral bands or telemetry channels often move together. Correlation stretches the loss surface into a long narrow valley. Near a minimum any loss surface behaves like a quadratic with curvatures given by the eigenvalues $\lambda$ of its Hessian (here 0.083 and 1.92), and gradient descent is stable only if $\eta < 2/\lambda_{\max}$ = 1.04. A small step crawls along the valley floor; a step near the limit zig-zags across the valley yet converges fastest; a slightly larger one diverges. The ratio $\kappa = \lambda_{\max}/\lambda_{\min}$, here 23, is the **condition number**: the larger it is, the slower gradient descent converges, which is why inputs are routinely **standardised** to zero mean and unit variance before training.

![Gradient descent computed on the least-squares loss of a two-coefficient linear model whose predictors are strongly correlated (r = 0.9), which turns the loss surface into a long, narrow valley. (a) A small step (η = 0.1) crawls along the valley; η = 0.6 converges steadily; stochastic gradient descent with mini-batches of 10 samples wanders near the minimum. (b) Steps close to the stability limit zig-zag across the valley; η = 1.08 diverges. (c) After 60 iterations the loss is within 1.3 × 10⁻⁵ of its minimum for η = 1.0, 5 × 10⁻⁴ for η = 0.6 and 0.08 for η = 0.1.](figures/out/ch43_gdpaths.svg){#fig:gdpaths width=100%}

::: example
**Example: one gradient-descent step by hand**

A logistic-regression cloud detector computes $p = \sigma(w_1 x_1 + w_2 x_2 + b)$, where $x_1$ and $x_2$ are the visible and 1.6 µm reflectances and $\sigma(z) = 1/(1+e^{-z})$. It starts with all parameters zero and sees one cloudy pixel, $x = (0.70, 0.45)$, $y = 1$. The learning rate is $\eta$ = 0.5.

1. **Prediction.** $z = 0$, so $p = \sigma(0)$ = 0.5 and the cross-entropy loss is $-\ln 0.5$ = **0.693**.
2. **Gradient.** For logistic regression with cross-entropy the gradient takes a simple form: $\partial \ell/\partial w_j = (p - y)\,x_j$ and $\partial \ell / \partial b = p - y$. Here $p - y = -0.5$, so the gradients are $(-0.35, -0.225)$ for the weights and $-0.5$ for the bias.
3. **Update.** $w \leftarrow w - \eta \nabla_w \ell = (0.175, 0.1125)$ and $b \leftarrow 0.25$.
4. **Check.** Now $z = 0.175 \times 0.70 + 0.1125 \times 0.45 + 0.25$ = 0.423, $p$ = 0.604 and the loss has fallen to **0.504**. But a clear snow pixel, $x = (0.80, 0.10)$, now also gets $p$ = 0.599: the model has learned "bright means cloud". Only many more examples — including snow — and a model able to bend its boundary can fix this, as the next figures show.
:::

### Neural Networks and Backpropagation

A **neural network** builds a flexible function by stacking simple layers. Each layer multiplies its input vector by a weight matrix, adds a bias and passes the result through a non-linear **activation function**; the popular **ReLU** (rectified linear unit) simply replaces negative values by zero. A **multilayer perceptron (MLP)** with two hidden layers computes

$$ h_1 = \mathrm{ReLU}(W_1 x + b_1), \qquad h_2 = \mathrm{ReLU}(W_2 h_1 + b_2), \qquad p = \sigma(w_3^\top h_2 + b_3). $$

With enough hidden units such a network can approximate any reasonable function. Training uses the gradient of the loss with respect to every weight, computed by **backpropagation**: a forward pass stores each layer's output; a backward pass then applies the chain rule of calculus layer by layer, starting from $\partial \ell/\partial z = p - y$ at the output and multiplying by each layer's weights and activation slopes on the way back. The cost of the backward pass is about twice that of the forward pass, whatever the number of weights — which is why networks with billions of parameters can be trained at all (Chapter 44).

@fig:mlpoverfit shows such a network, written from scratch in a few dozen lines of numpy, learning the cloud-or-clear problem from only 100 labelled pixels, one label in ten deliberately wrong. For the first few dozen passes over the data, training and validation losses fall together. Then the network starts to fit the individual mislabelled pixels: training loss heads towards zero while the loss on 2 000 independent validation pixels climbs from 0.42 to 2.7. This is **overfitting**, and the simplest cure is **early stopping** — keeping the weights from the epoch with the lowest validation loss, here epoch 39. The early-stopped network classifies 85.9 % of 20 000 test pixels correctly; the network trained to the end, which scores 99 % on its own training data, manages only 79.3 %.

![A neural network written from scratch in numpy — two hidden layers of 64 ReLU units, about 4 400 parameters — trained by backpropagation on only 100 synthetic cloud and clear pixels, described by visible and 1.6 µm reflectance, with one label in ten deliberately wrong. (a) Training loss falls towards zero; validation loss is lowest at epoch 39 and then rises as the network memorises label errors. (b) The early-stopped network draws a smooth boundary and classifies 85.9 % of 20 000 test pixels correctly. (c) After 3 000 epochs the boundary wraps around individual mislabelled pixels and test accuracy falls to 79.3 %.](figures/out/ch43_mlpoverfit.svg){#fig:mlpoverfit width=100%}

### Regularisation, Bias and Variance

Any technique that discourages a model from fitting noise is called **regularisation**. Early stopping is one. Another adds a penalty on large weights to the empirical risk, $\hat R(\theta) + \lambda \lVert\theta\rVert^2$ (**weight decay**, or **ridge** regression for linear models); the penalty $\lambda \sum_j |\theta_j|$ (**lasso**) drives unimportant weights to exactly zero. Neural networks are also regularised by **dropout**, which randomly switches off units during training, and by **data augmentation**, which adds rotated, shifted or noisier copies of the training images. Trees are regularised by limiting their depth or the number of samples in each leaf.

The **bias–variance trade-off** explains why regularisation works. For squared loss, the expected error of a model on new data splits into three parts:

$$ \mathbb{E}\big[(y - \hat f(x))^2\big] = \underbrace{\big(\mathbb{E}[\hat f(x)] - f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathrm{Var}\big[\hat f(x)\big]}_{\text{variance}} + \sigma^2 . $$

**Bias** is the error of the average model, caused by assumptions too simple for the problem; **variance** is how much the fitted model changes from one training set to another; $\sigma^2$ is the **irreducible error** from noise in the data and labels, which no model can remove. Simple models underfit (high bias); flexible models overfit (high variance). @fig:learningcurves (a) shows the trade-off for decision trees on 1 000 pixels: the cross-validated error is lowest, 15.1 %, at a depth of 5. Panel (b) shows **learning curves** — test error against training-set size. Logistic regression levels off at about 31 % whatever the amount of data, because a straight line cannot separate snow from cloud; a random forest and a k-nearest-neighbour classifier keep improving, reaching 12.3 % and 12.1 % with 20 000 pixels, close to the irreducible 11.9 % set by the overlapping classes and the 10 % label noise. Learning curves answer a practical question: will collecting more labels help, or is a better model needed?

![(a) The bias–variance trade-off, computed for decision trees fitted to 1 000 synthetic cloud and clear pixels: training error falls towards zero as the tree deepens, while the cross-validated error is lowest (15.1 %) at depth 5 and rises to about 22 % for deep trees that memorise noise. (b) Learning curves: with more training pixels the test error of flexible models approaches the irreducible 11.9 % — 12.3 % for a random forest and 12.1 % for k-nearest neighbours with 20 000 pixels — whereas logistic regression stays near 31 % (high bias).](figures/out/ch43_learning.svg){#fig:learningcurves width=100%}

### Training, Validation and Test Sets

A model judged on its own training data will always look better than it is. The standard practice is to split the labelled data three ways. The **training set** is used to fit the parameters. The **validation set** is used to choose **hyper-parameters** — settings that are not learned, such as the learning rate, the network size or the tree depth — and to decide when to stop. The **test set** is locked away and used once, at the end, to estimate performance on new data. Every look at the test set that influences a design decision leaks information from it and makes the final estimate optimistic.

When data are scarce, **k-fold cross-validation** makes better use of them: the data are split into $k$ folds (often 5 or 10), the model is trained $k$ times on $k-1$ folds and tested on the remaining one, and the $k$ scores are averaged. Hyper-parameters are then tuned by **grid search**, **random search** or Bayesian optimisation over the cross-validated score — with the test set still untouched.

### Leakage: When Space Data Cheat

**Data leakage** occurs when information about the test data reaches the model during training, so that the test score no longer measures performance on genuinely new inputs. Some leaks are obvious — a feature computed from the label, or duplicated images in training and test sets. The most dangerous leak in space applications is subtle: **autocorrelation**. Neighbouring pixels in an image are alike, and so are consecutive samples of telemetry or successive days of solar activity. If samples are assigned to training and test sets at random, almost every test sample has a near-identical neighbour in the training set, and the model can score well by remembering places or times rather than by learning the physics that would carry it to a new region, a new season or a new satellite.

@fig:spatialcv makes the effect concrete. A random forest learns a synthetic target that is only partly explained by its predictors: half of it is a genuine function of one predictor, the rest a spatially smooth signal with a correlation length of 12 km that no predictor explains. Five further predictors are smooth random fields with no relation to the target at all — but they let the forest recognise *where* a sample is. Random five-fold cross-validation reports an excellent R² of 0.80. Cross-validation with **spatial blocks** larger than the correlation length reports about 0.25. Tested in an unseen region, the model scores −0.39 — worse than simply predicting the regional average — while the true relationship explains only 17 % of the variance there. The forest had learned a map of the training region, not a law of nature.

![Leakage through spatial autocorrelation, computed with a random forest on a synthetic 200 km × 100 km field. The target is half a genuine predictor plus a smooth spatial signal (correlation length 12 km) that no predictor explains; five further predictors are smooth random fields unrelated to the target, which let the forest recognise places. (a) The target, with training samples in the western half and test samples in an unseen eastern region. (b) Random five-fold cross-validation reports R² = 0.80 and spatial-block cross-validation about 0.25; the model's actual skill in the new region is −0.39, and even the true relationship explains only 17 % of the variance there.](figures/out/ch43_spatialcv.svg){#fig:spatialcv width=100%}

::: data
**Data box — spatial validation of biomass maps**

- In 2020 Ploton and colleagues rebuilt a typical large-scale mapping workflow: a random forest predicting above-ground forest biomass in central Africa from 9 MODIS and 27 environmental predictors, trained on an inventory of 11.8 million trees.
- With random 10-fold cross-validation the model appeared to explain more than half of the variation in biomass (R² = 0.53).
- With spatial cross-validation the same model explained only 14 % (R² = 0.14); when test plots more than about 100 km from any training plot were used, its predictive power was close to zero. Biomass in the data was spatially autocorrelated up to about 120 km.
- The authors concluded that ignoring spatial structure in validation produces over-optimistic accuracy claims, and that predictors with no real relationship to the target can appear powerful simply because they vary smoothly in space.
:::

The cure is to split the data the way the model will be used (@tbl:splitstrategies). If a map must be predicted far from training sites, the test data must be far from them too; if a forecast will be issued tomorrow, the model must be tested on days after all of its training data. The block size should exceed the range of autocorrelation, which can be estimated from a variogram of the residuals.

| Splitting strategy | How samples are assigned | Protects against | Space example |
|---|---|---|---|
| Random | Each sample independently | Nothing beyond chance; optimistic for autocorrelated data | Shuffled pixels from the same scenes |
| Spatial blocks | Whole tiles or regions to one fold | Memorising places | Land-cover or biomass maps |
| Buffered | Training samples near each test sample removed | Leakage across block edges | Field-plot validation |
| Time-series (forward chaining) | Train on the past, test on the future | Using the future to predict the past | Flare and storm forecasts |
| Grouped | Whole orbits, passes, instruments or missions to one fold | Memorising one sensor or event | Telemetry anomaly detection; multi-satellite products |

: Ways of splitting data, and the leakage each one prevents. {#tbl:splitstrategies}

## Classical Machine Learning

Deep networks dominate image and language tasks, but most operational space products still rest on the classical methods of @tbl:classicalml. They train quickly on modest data, run on modest hardware and are easier to understand and verify.

| Method | Key idea | Strengths | Limitations | Space use (status) |
|---|---|---|---|---|
| Linear regression | Weighted sum fitted by least squares | Fast, interpretable | Linear relations only | Sea-surface temperature from AVHRR (operational since the 1980s) |
| Logistic regression | Sigmoid of a weighted sum | Calibrated probabilities; baseline | Linear boundary | Baselines for flare and fire detection (research) |
| k-nearest neighbours | Vote or average of the $k$ closest examples | No training; local | Slow; needs few features | Finnish forest inventory (operational since about 1990) |
| Decision tree | Sequence of threshold tests | Readable rules | Unstable; overfits | SKICAT sky survey (1990s); MODIS land cover (2000s) |
| Random forest | Average of many randomised trees | Robust, little tuning | Large; less transparent | MODIS land cover since Collection 6 (operational) |
| Gradient boosting | Trees added to correct residual errors | Top accuracy on tabular data | Needs tuning | Sentinel-2 cloud probability (operational in data services) |
| Support vector machine | Maximum-margin boundary, kernels | Strong with few samples | Slow on very large data | EO-1 onboard classifiers (operational 2004–17) |
| k-means | Nearest-centroid clustering | Fast, simple | Choice of $k$; round clusters | Unsupervised image classification |
| Principal component analysis | Projection on main directions of variance | Compression, denoising | Linear only | IASI spectra disseminated as PC scores (since 2011) |
| Gaussian process | Prior over functions, posterior with error bars | Honest uncertainty | Cost grows as $N^3$ | Stellar-activity models in planet searches (research standard) |

: Classical machine-learning methods and their space uses. {#tbl:classicalml}

### Linear and Logistic Regression

**Linear regression** predicts $\hat y = w^\top x + b$ and chooses the weights that minimise the squared error, with the closed-form solution $w = (X^\top X)^{-1}X^\top y$. It is the oldest learning method in remote sensing. The **multichannel sea-surface temperature** algorithm that NOAA has used since the early 1980s exploits the fact that water vapour absorbs more at 12 µm than at 11 µm: the temperature is estimated as a weighted combination of the brightness temperature at 11 µm and the difference between the two channels, with coefficients found by regressing satellite measurements against simultaneous readings from drifting buoys. In 1985 its root-mean-square difference from ship and buoy measurements was about 0.5 °C (Chapter 16).

**Logistic regression** turns the weighted sum into a probability with the sigmoid function, $p = \sigma(w^\top x + b)$, and is trained by minimising cross-entropy, as in the worked example. Its decision boundary, $p$ = 0.5, is a straight line (a plane, in more dimensions). That makes it a good **baseline** — every new model should be compared with a simple one — and explains its failure in @fig:decisionbounds: no straight line can put snow on the clear side and cloud on the other.

![Decision boundaries of three classifiers trained on the same 2 000 synthetic pixels from eight surface and cloud types, with 10 % of labels wrong. Logistic regression can only draw a straight line and labels 96 % of snow pixels as cloud (test accuracy 68.6 %); a random forest (86.8 %) and the numpy neural network with early stopping (87.7 %) approach the best accuracy possible with these overlapping classes and noisy labels, 88.1 %, whose boundary — computed from the known class distributions — is shown dashed.](figures/out/ch43_boundaries.svg){#fig:decisionbounds width=100%}

### Nearest Neighbours

The **k-nearest-neighbour (k-NN)** method stores the training data and, for each new input, finds the $k$ closest examples and takes a majority vote (for classification) or an average (for regression). It needs no training and adapts to any boundary shape, but prediction is slow for large data sets and distances lose meaning when there are many features, the "curse of dimensionality". Since about 1990 Finland's multi-source national forest inventory has used k-NN to give every satellite pixel the timber volume, tree species and age of the field plots whose spectra it most resembles, producing forest maps and statistics for areas far too small for the field plots alone.

### Decision Trees, Random Forests and Gradient Boosting

A **decision tree** classifies by asking a sequence of threshold questions — "is the 1.6 µm reflectance above 0.3?" — each chosen to make the resulting groups as pure as possible, measured for example by the **Gini impurity** $G = 1 - \sum_k p_k^2$, where $p_k$ is the fraction of class $k$ in a group. Trees are readable and fast — the best tree JPL built for EO-1 needed at most 24 comparisons per pixel — but a deep tree memorises its training data, and a small change in the data can change the whole tree.

A **random forest** fixes this by averaging hundreds of trees, each grown on a random bootstrap sample of the data and choosing each split from a random subset of the features. The trees make different errors, so their average has much lower variance than any one of them. Random forests need little tuning and are the default classifier of land mapping; NASA's MODIS land-cover product switched from a single C4.5 decision tree in Collection 5 to a random forest in Collection 6, classifying the globe each year since 2001 at 500 m resolution. Hansen and colleagues' 2013 global forest-change maps applied decision-tree classifiers to about 654 000 Landsat scenes, using one million CPU-core hours spread over 10 000 computers in Google Earth Engine.

**Gradient boosting** builds trees in sequence instead: each new small tree $h_m$ is fitted to the errors (more precisely, the negative gradient of the loss) left by the ensemble so far, and added with a small weight $\nu$, so that $F_m(x) = F_{m-1}(x) + \nu\, h_m(x)$. Boosted trees, in libraries such as XGBoost and LightGBM, are usually the most accurate models for tabular data. Sentinel Hub's **s2cloudless** detector, a LightGBM model working on ten Sentinel-2 bands, underlies the cloud-probability layer distributed with Sentinel-2 imagery in Google Earth Engine — although, like any reflectance-based detector, it gives high probabilities over very bright surfaces such as snow and rooftops.

### Support Vector Machines

A **support vector machine (SVM)** chooses, among all the boundaries that separate two classes, the one with the widest **margin** — the largest gap to the nearest training points, which are called support vectors. For a linear boundary $w^\top x + b = 0$ the margin is $2/\lVert w \rVert$, so the SVM minimises

$$ \tfrac12 \lVert w \rVert^2 + C \sum_i \max\big(0,\; 1 - y_i (w^\top x_i + b)\big), $$

where labels are coded $y_i = \pm 1$ and the second term, the **hinge loss**, penalises points on the wrong side of the margin. A **kernel** such as the Gaussian $K(x, x') = \exp(-\gamma \lVert x - x' \rVert^2)$ lets the same mathematics draw curved boundaries. SVMs work well with few training samples, which made them popular in the 2000s. In 2015 Bobra and Couvidat used a Gaussian-kernel SVM on magnetic-field features of solar active regions, measured by the Solar Dynamics Observatory, to forecast M- and X-class flares within 24 hours, with a true skill statistic of 0.76 on 303 flaring and 5 000 non-flaring examples (Chapter 47).

::: history
**EO-1: learned classifiers in command**

NASA's Earth Observing-1, launched in 2000 as a technology demonstrator, became from 2003–04 the testbed of the **Autonomous Sciencecraft Experiment**: onboard software that analysed images from the Hyperion imaging spectrometer, detected floods, volcanic activity and changes in snow and ice, and replanned the satellite's next observations without waiting for the ground (@fig:eo1holuhraun). The payload computer was a Mongoose V processor of about 8 MIPS with 256 MB of memory, and only 12 of Hyperion's bands could be read on board. JPL compared four pixel classifiers for land, water, snow, ice and cloud: one built by an expert, the best of thousands of thresholded band ratios, a decision tree and a **linear SVM** on 11 bands, which needed just 11 multiplications and 11 additions per class for each pixel. On 50 expert-labelled test images (about 91 million pixels) the SVM classified 81.3 % of pixels correctly, the expert classifier 82.9 % and the decision tree 80.9 %. The averages hid a weakness: ice made up only 2 % of the test pixels, and the SVM found just 47.8 % of them. The expert and SVM classifiers were uploaded and ran on board; the team reported a hundred-fold increase in science returned per megabyte downlinked and a cut in the response time to events from days to hours. SVM classifiers ran on EO-1 for more than a dozen years, until the mission ended in 2017.
:::

![The Holuhraun eruption in Iceland on the night of 1 September 2014, imaged by EO-1 in false colour to emphasise the hottest vents and lava flows. Detecting such thermal events on board, and retasking the satellite to observe them again, was one of the jobs of EO-1's autonomy software.](figures/photos/ch43_eo1.jpg){#fig:eo1holuhraun width=50%}

### Clustering and Dimensionality Reduction

**k-means** clustering divides unlabelled data into $k$ groups. It starts from $k$ trial centres, assigns each sample to the nearest centre, moves each centre to the mean of its samples, and repeats; this minimises the total squared distance $\sum_i \lVert x_i - \mu_{c(i)} \rVert^2$ between samples and their cluster centres. Its variant ISODATA, which splits and merges clusters, has been used for unsupervised image classification since the 1970s: the analyst names each spectral cluster afterwards (Chapter 13). k-means finds clusters of similar size and round shape; it may split one class into two or merge two similar ones, and the number of clusters must be chosen, for example by looking for an "elbow" in the total distance as $k$ grows.

**Principal component analysis (PCA)** finds new axes, the eigenvectors of the data's covariance matrix $C = \frac{1}{N}\sum_i (x_i - \bar x)(x_i - \bar x)^\top$, ordered by the variance $\lambda_k$ along each. Keeping only the first few components compresses the data with little loss and removes noise. In @fig:kmeanspca two components hold 96.6 % of the variance of six-band pixels, and k-means, never shown a label, recovers the six cover types well (an adjusted Rand index of 0.89, where 1 means perfect agreement). PCA works at a much larger scale too: the IASI sounder on the Metop satellites measures 8 461 spectral channels, and since 2011 EUMETSAT has also distributed each spectrum as a few hundred principal-component scores — about 300, a 28-fold reduction — from which users can reconstruct the radiances with much of the instrument noise removed.

![Unsupervised learning on 3 000 synthetic six-band pixels. (a) The pure spectra used to generate them; each pixel is a shaded mixture dominated by one cover type, plus noise. (b) Principal component analysis compresses the six bands into two components that hold 96.6 % of the variance; k-means with six clusters, run without labels, finds groups (crosses: cluster centres) that match the dominant cover types with an adjusted Rand index of 0.89. (c) Variance explained by each component.](figures/out/ch43_kmeanspca.svg){#fig:kmeanspca width=100%}

### Gaussian Processes

A **Gaussian process (GP)** treats the unknown function itself as random, with a **covariance function** (kernel) $k(x, x')$ saying how strongly the function values at two inputs are correlated — typically more strongly the closer they are. Conditioning on $N$ noisy observations $y$ gives, at a new input $x_*$, a predictive mean and variance

$$ \mu_* = k_*^\top (K + \sigma_n^2 I)^{-1} y, \qquad \sigma_*^2 = k(x_*, x_*) - k_*^\top (K + \sigma_n^2 I)^{-1} k_*, $$

where $K$ is the matrix of kernel values between training inputs, $k_*$ the vector between them and $x_*$, and $\sigma_n^2$ the noise variance. The variance is the GP's great strength: it widens automatically away from the data, giving honest error bars. Its weakness is the $N \times N$ matrix inversion, whose cost grows as $N^3$, limiting exact GPs to tens of thousands of points. In geostatistics the same mathematics is called **kriging**. Gaussian processes are a standard tool for separating planetary signals from stellar activity in radial-velocity planet searches: in 2014 a GP model of activity in the star CoRoT-7 gave masses of 4.73 ± 0.95 and 13.56 ± 1.08 Earth masses for its two planets (Chapter 51). They also underlie **Bayesian optimisation**, used to tune hyper-parameters with few expensive trials.

### The Kalman Filter: Estimation Meets Learning

The **Kalman filter** (Chapter 6) estimates the state of a dynamic system — position and velocity, or attitude and gyro bias — from noisy measurements. It alternates two steps. The **prediction** propagates the state estimate and its covariance with a dynamic model, $\hat x^- = F \hat x$ and $P^- = F P F^\top + Q$, where $Q$ is the process noise. The **update** blends in a measurement $z$:

$$ K = P^- H^\top (H P^- H^\top + R)^{-1}, \qquad \hat x = \hat x^- + K (z - H \hat x^-), \qquad P = (I - K H) P^- , $$

where $H$ maps the state to the measurement, $R$ is the measurement noise and the **gain** $K$ weights the new information by the relative confidence in prediction and measurement. This is exact **Bayesian inference** for linear systems with Gaussian noise: the prior (prediction) times the likelihood (measurement) gives the posterior (update). Stanley Schmidt's group at NASA Ames adapted Kalman's 1960 theory to the non-linear problem of navigating Apollo to the Moon, and the resulting **extended Kalman filter** flew in the Apollo guidance computer (@fig:lovellgn).

![Jim Lovell at the guidance and navigation station of the Apollo 8 command module in December 1968, in a frame from 16 mm film. Star sightings made here were combined with a dynamic model in a recursive estimator of the kind adapted for Apollo at NASA Ames.](figures/photos/ch43_lovell.jpg){#fig:lovellgn width=56%}

Estimation theory and machine learning are two dialects of the same language. Least-squares orbit determination (Chapter 3) is linear regression; a Kalman filter can be seen as Gaussian-process regression in time, computed recursively; recursive least squares is online learning; and a neural network trained with weight decay is a maximum *a posteriori* estimate with a Gaussian prior on its weights. The difference is mostly one of emphasis. Estimation theory starts from a physical model with a few uncertain parameters and quantifies their uncertainty; machine learning starts from data with a flexible model of many parameters and worries most about generalisation. The best space systems use both: physics where it is known, learning where it is not, and estimation theory to keep track of what each knows.

## Measuring Performance

### From the Confusion Matrix to F1

For a two-class detector — fire or no fire, anomaly or normal — every prediction falls into one cell of the **confusion matrix**: a **true positive** (TP) is an event correctly flagged, a **false positive** (FP) a false alarm, a **false negative** (FN) a miss and a **true negative** (TN) a correct rejection. Chapter 13 shows the multi-class version used in map accuracy assessment, where precision is called user's accuracy and recall producer's accuracy. From the four counts come the main scores of @tbl:evalmetrics: **accuracy**, the fraction correct; **precision**, the fraction of alarms that are real; **recall** (probability of detection), the fraction of events found; the **false-alarm rate** (false-positive rate) among non-events; and the **F1 score**, the harmonic mean of precision and recall, which is high only if both are.

| Metric | Definition | Use it when | Caution |
|---|---|---|---|
| Accuracy | (TP + TN) / N | Classes are balanced | Meaningless for rare events |
| Precision | TP / (TP + FP) | False alarms are costly | Falls as events become rarer |
| Recall | TP / (TP + FN) | Misses are costly | Ignores false alarms |
| False-alarm rate | FP / (FP + TN) | Alarms per non-event matter | Looks tiny for rare events |
| F1 | 2 × precision × recall / (precision + recall) | One number for a rare class | Ignores true negatives; depends on threshold |
| ROC AUC | Area under recall versus false-alarm rate | Comparing rankings | Optimistic for rare events |
| Average precision | Area under precision versus recall | Rare events | Depends on prevalence |
| IoU | Area of overlap / area of union | Segmentation, boxes | Harsh on small objects |
| mAP | Mean of average precision over classes | Object detection | Depends on the IoU threshold used |
| RMSE, MAE | √(mean error²); mean of absolute error | Regression | RMSE stresses large errors |
| CSI | TP / (TP + FP + FN) | Event forecasts, detections | Depends on event rate |
| TSS | Recall − false-alarm rate | Flare and storm forecasts | Can be high with poor precision |
| Brier score | Mean of (forecast probability − outcome)² | Probability forecasts | Compare with climatology |

: Evaluation metrics. {#tbl:evalmetrics}

::: example
**Example: scoring a wildfire detector**

A thermal-infrared fire detector is tested on a scene of 1 000 000 land pixels that contains 500 fire pixels, checked by an independent high-resolution sensor (@fig:modisfires). It raises 620 alarms: 410 at real fires and 210 elsewhere.

1. **Counts.** TP = 410, FP = 210, FN = 500 − 410 = 90 and TN = 1 000 000 − 500 − 210 = 999 290.
2. **Precision** = 410 / 620 = **0.661**: one alarm in three is false. **Recall** = 410 / 500 = **0.820**. **F1** = 2 × 0.661 × 0.820 / (0.661 + 0.820) = **0.732**.
3. **False-alarm rate** = 210 / 999 500 = 2.1 × 10⁻⁴, the critical success index CSI = 410 / 710 = 0.577 and the true skill statistic TSS = 0.820 − 0.0002 = 0.820.
4. **Accuracy** = (410 + 999 290) / 1 000 000 = **99.97 %**. A "detector" that never raises an alarm scores 99.95 %. Accuracy cannot tell them apart; precision and recall can.
5. **Sensitivity.** If a season of sun glint doubles the false alarms to 420, precision falls to 0.494 and F1 to 0.617 — while accuracy barely changes, to 99.95 %.
:::

![Smoke from lightning-caused wildfires in northern California on 4 August 2015, in a natural-colour image from MODIS on Terra. Red outlines mark actively burning areas detected by MODIS's thermal bands — a detection problem in which fire pixels are a tiny fraction of the scene.](figures/photos/ch43_fires.jpg){#fig:modisfires width=56%}

### ROC and Precision–Recall Curves

Most classifiers output a score or probability, and the user chooses the **threshold** above which to raise an alarm. Lowering the threshold finds more events at the cost of more false alarms. The **receiver operating characteristic (ROC)** curve plots recall against false-alarm rate for every threshold; its area (AUC) is the probability that a randomly chosen event scores higher than a randomly chosen non-event. The **precision–recall (PR)** curve plots precision against recall; its area is the **average precision**.

For rare events the two tell very different stories (@fig:rocpr). A logistic-regression detector for a synthetic fire task with 1 % prevalence has a near-perfect-looking ROC area of 0.979, but at the default threshold of 0.5 it finds only 35 % of the fires, and its average precision is just 0.54. Applied to the same pixels but with fires making up 10 % or 50 % of the sample, the same detector reaches average precisions of 0.86 and 0.98 — its ROC curve does not change at all. Because the ROC curve divides false alarms by the huge number of non-events, it hides the fact that at 1 % prevalence even a small false-alarm rate produces as many false alarms as real ones. Accuracy is worse still: it stays above 97.5 % at every threshold, and a detector that never fires scores 99.0 %. This is the **accuracy paradox**. The best threshold depends on the relative costs of misses and false alarms, and must be chosen by the user of the system, not by the default of a software library.

![Why accuracy misleads for rare events, computed for a synthetic fire-detection task (2 001 fires among 200 000 test pixels, 5 % of clear pixels fire-like) and a logistic-regression detector. (a) The ROC curve looks excellent (area 0.979), yet at the default threshold of 0.5 the detector finds only 35 % of fires. (b) Precision–recall curves of the same detector at three prevalences: average precision 0.54 at 1 %, 0.86 at 10 % and 0.98 at 50 %. (c) Accuracy stays above 97.5 % at every threshold, while F1 peaks at 0.52.](figures/out/ch43_rocpr.svg){#fig:rocpr width=100%}

### Detection, Segmentation and Regression Metrics

For semantic segmentation and object detection the basic unit is the overlap between a predicted region $A$ and the true region $B$, the **intersection over union** $\mathrm{IoU} = |A \cap B| / |A \cup B|$. A detection usually counts as correct if its IoU with a true object exceeds 0.5. **Mean average precision (mAP)** averages the average precision over object classes, and sometimes over IoU thresholds from 0.5 to 0.95 — so mAP figures from different papers are comparable only if they use the same definition. For regression the usual scores are the **root-mean-square error** $\mathrm{RMSE} = \sqrt{\tfrac1N \sum_i (\hat y_i - y_i)^2}$, which emphasises large errors, the **mean absolute error** (MAE), the mean **bias**, and the coefficient of determination R², the fraction of the variance explained — which, as @fig:spatialcv showed, becomes negative when a model is worse than predicting the mean.

### Forecast Skill and Calibration

Space weather and meteorology add scores designed for forecasts of events. The **critical success index**, CSI = TP / (TP + FP + FN), ignores the many correct "no event" forecasts. The **true skill statistic**, TSS = recall − false-alarm rate, ranges from −1 to 1 and, unlike most scores, does not depend on how often events occur, which is why it is widely recommended for comparing flare forecasts made on different samples. A **skill score** compares a forecast with a reference such as climatology or persistence: $\mathrm{SS} = 1 - S/S_{\mathrm{ref}}$ for a score $S$ where lower is better.

Probabilistic forecasts must also be **calibrated**: of all the occasions on which a flare model says "30 % chance", about 30 % should see a flare. The **Brier score**, $\mathrm{BS} = \tfrac1N \sum_i (p_i - o_i)^2$ with outcomes $o_i$ of 0 or 1, rewards both calibration and sharpness, and a **reliability diagram** plots observed frequency against forecast probability. Many classifiers are poorly calibrated out of the box — modern deep networks tend to be over-confident, while boosted trees and SVMs distort probabilities in other ways — and can be recalibrated on validation data, for example by Platt scaling or isotonic regression. Calibration matters whenever probabilities feed decisions, such as whether to perform a collision-avoidance manoeuvre (Chapter 21).

### Rare Events

Fires, spacecraft anomalies, high-risk conjunctions and large solar flares are all rare, and rarity distorts every stage of learning. A model trained to minimise average loss can do well by ignoring the rare class altogether. Remedies include **re-weighting** the loss so that each rare example counts more, **re-sampling** (under-sampling the common class or generating extra rare examples), choosing the operating threshold for the actual costs, and — above all — evaluating with precision, recall and PR curves rather than accuracy. The EO-1 classifiers showed the problem in 2006: overall accuracy above 80 % concealed a recall of less than 50 % for ice, which made up 2 % of the pixels.

::: data
**Data box — rare events: ESA's collision-avoidance challenge**

- In 2019 ESA released 199 082 conjunction data messages for 15 321 close approaches involving its satellites between 2015 and 2019, each message with 103 attributes, and asked competitors to predict the final collision risk two days before closest approach.
- Only 515 events (3.4 %) had a final risk of 10⁻⁶ or more, 131 (0.9 %) of 10⁻⁵ or more and 30 of 10⁻⁴ or more.
- 96 teams made 862 submissions over two months. A naive forecast — "the final risk equals the latest known risk" — scored 0.694 on the competition's loss; only 12 teams beat it, and the winners only modestly.
- The organisers concluded that naive forecasts are a surprisingly strong benchmark that any future model must beat, that machine learning can improve on them, and that the unavoidable imbalance of the data limited off-the-shelf methods (Chapter 50).
:::

### How Sure Are We?

A test score is a statistical estimate, and must be quoted with its uncertainty. If a detector produces $k$ false alarms among $n$ independent negative test samples, the false-alarm rate $\hat p = k/n$ has a standard error of about $\sqrt{\hat p (1 - \hat p)/n}$, and an approximate 95 % confidence interval is $\hat p \pm 1.96$ standard errors; the **Wilson interval** is more accurate when $k$ is small. If no false alarms at all are seen in $n$ trials, the "rule of three" gives a 95 % upper limit of about $3/n$. Two models tested on the same samples should be compared with a paired test such as McNemar's, which looks only at the samples on which they disagree.

::: example
**Example: how big must the test set be?**

A requirement says that an onboard event detector must have a false-alarm rate of about 1 %, and that the test must measure it to within ±0.2 % at 95 % confidence.

1. **Sample size.** Solving $1.96\sqrt{p(1-p)/n} = E$ for $n$ gives $n = 1.96^2 \times p(1-p)/E^2 = 3.84 \times 0.01 \times 0.99 / 0.002^2$ = **9 508 negative samples**.
2. **Check.** With 95 false alarms in 9 508 samples, the Wilson 95 % interval is 0.82–1.22 % — as required.
3. **Correlation.** Pixels are not independent. If they come in clusters of 25 neighbouring pixels with an intra-cluster correlation of 0.2, the **design effect** is $1 + (25 - 1) \times 0.2$ = 5.8, and about **55 000 pixels** — some 2 200 independent clusters — are needed for the same precision.
4. **Rarer requirements.** Halving the interval needs four times the samples; measuring a 0.1 % rate to ±0.02 % needs about 96 000 independent negatives. If none of 3 000 test samples gives a false alarm, the rule of three says only that the rate is probably below 0.1 %.
5. **The positives too.** Recall needs its own sample of events: the 500 fire pixels of the wildfire example measure a recall of 0.82 only to within about ±0.034.
:::

## From Notebook to Operations

A model that performs well in a notebook is only the start. In operations it becomes one component of a data system (@fig:mlpipeline): it may run on the ground, in a processing chain or a cloud service, or — after verification on flight-like hardware — on the spacecraft itself, where it can decide what to downlink or whether to retask the sensor (Chapter 45). JPL's Dynamic Targeting experiment on the CogniSAT-6 cubesat in July and August 2025 is an example: the satellite tilted forward to look about 74–90 seconds ahead along its track, analysed the image for cloud on board, and then pointed its camera at the clearest scenes as it passed over them.

![Where machine learning sits in a space data system (top) and the nine-step workflow for building and operating a model (bottom). Models can run on the ground or, once verified, be uplinked to run on the spacecraft; new labels and error reports from users feed retraining when performance drifts.](figures/out/ch43_pipeline.svg){#fig:mlpipeline width=100%}

Operations bring problems that do not appear in a laboratory. Instruments degrade and are recalibrated, so the input distribution drifts. New satellites in a constellation have slightly different spectral responses. A model trained on one region or season is applied to another. Every one of these is a form of **distribution shift**, and the remedy is monitoring: tracking the distribution of inputs and outputs, comparing predictions with independent reference data, and retraining when performance falls. A model must also be versioned and documented like any other flight or ground software, with its training data, test results and known limitations recorded (Chapter 53).

::: note
**Practice: building an onboard cloud screen for a new imager**

1. **Define the decision.** The screen will decide which scenes are downlinked. State the cost of each error: a cloudy scene downlinked wastes about 1 % of a pass, while a clear scene discarded loses data for good — so recall for clear scenes matters most. Note the onboard limits on power, memory and processing time.
2. **Gather data.** Use raw data processed as it will be on board, not calibrated ground products. Cover all seasons, latitudes, Sun angles and surfaces — especially snow, ice, deserts, sun glint and smoke.
3. **Label.** Have experts mark cloud, thin cloud, shadow and clear; have a sample labelled twice to measure the label-error rate, which sets the floor on achievable error.
4. **Set a baseline.** Build a physics-based threshold test on visible and 1.6 µm bands and score it. Any learned model must beat it clearly.
5. **Split by space and time.** Assign whole scenes, regions and dates to training, validation and test sets; hold out at least one region and one season entirely, and lock the test set.
6. **Train and tune.** Start with gradient-boosted trees on band values and ratios, then try a small convolutional network. Tune on validation data only and use early stopping.
7. **Evaluate.** Report precision and recall for each surface type at the chosen threshold, with confidence intervals, and compare with the baseline. Inspect the worst errors by eye.
8. **Deploy and verify.** Convert the model to the flight processor's number format, check that its outputs match the ground version, and run it in "shadow mode" — deciding but not acting — before it controls the downlink.
9. **Monitor.** Track the fraction of scenes flagged and compare with ground cloud masks; retrain after sensor recalibration or when new regions are added.
:::

## Road Map of Part XIII

The remaining chapters of Part XIII build on these foundations (@tbl:part13roadmap). Chapter 44 explains the deep-learning architectures — convolutional networks, transformers, generative models — that dominate current research. Chapter 45 covers the data, labels and computers that ML needs, from ground data centres to radiation-tolerant processors running models in orbit. Chapters 46–52 apply the methods to each domain of the space ecosystem, distinguishing operational systems from demonstrations and research, and Chapter 53 asks how learned systems can be verified, secured and governed well enough to be trusted with missions and lives.

| Chapter | Topic | Questions answered |
|---|---|---|
| 44 | Deep learning, foundation models and generative AI | How do CNNs, transformers and large pre-trained models work, and what do they cost to train? |
| 45 | Data, computing hardware and edge AI in orbit | Where do training data and labels come from? Which processors can run models on board? |
| 46 | AI for Earth observation | How is AI used for mapping, change detection, disasters and onboard image triage? |
| 47 | AI for weather, climate and space weather | How do AI forecast models compare with physics, and can flares and storms be predicted? |
| 48 | AI for autonomy, navigation and robotics | How do planners, AutoNav, AEGIS and learned guidance make spacecraft independent? |
| 49 | AI for mission operations, communications and networks | How can anomaly detection, scheduling and cognitive radio reduce the work of operators? |
| 50 | AI for space situational awareness, defence and security | How does AI help track objects, assess conjunctions and interpret intelligence? |
| 51 | AI for space science, planetary exploration and human spaceflight | How does AI find planets, analyse planetary data and support crews? |
| 52 | AI in design, manufacturing, launch and the space business | How is AI changing design, inspection, launch operations and markets? |
| 53 | Trustworthy AI for space | How are learned systems verified, secured and governed? What comes next? |

: Road map of Part XIII. {#tbl:part13roadmap}

::: key
**Key takeaways**

- AI is a family of techniques: symbolic AI writes knowledge down as rules, plans and constraints; machine learning learns it from examples; deep learning and foundation models are learning with very large neural networks. Space systems usually combine them, with verifiable logic guarding learned components.
- AI reached space in waves — expert systems and schedulers in the 1980s (CLIPS, STS-26, SPIKE for Hubble), classical machine learning from the 1980s to the 2010s (regression SST, EO-1's onboard SVM, random-forest land cover), deep learning from about 2017 and foundation models in the 2020s; most systems flying in 2026 are still demonstrations.
- Learning means minimising empirical risk, usually by (stochastic) gradient descent; the learning rate must stay below 2/λ_max of the loss curvature, and standardising inputs speeds convergence.
- Flexible models overfit: regularisation, early stopping and validation data control the bias–variance trade-off, and learning curves show whether more data or a better model is needed.
- Spatial and temporal autocorrelation leak information between randomly split samples; split by blocks, regions, time or mission, or a model can look excellent (R² = 0.80) and be useless in a new region.
- Classical methods — regression, k-NN, trees, forests, boosting, SVMs, k-means, PCA, Gaussian processes, the Kalman filter — still underpin most operational products and are the baselines any new model must beat.
- For rare events accuracy is meaningless: report precision, recall, PR curves and skill scores at an operating threshold chosen for the real costs, with confidence intervals — about 9 500 independent negatives are needed to measure a 1 % false-alarm rate to ±0.2 %.
:::

::: pagebreak
:::

::: questions
**Review questions**

1. Explain the difference between symbolic AI and machine learning, giving a space example of each. Why are safety-critical functions such as safe mode still implemented with explicit logic?
2. Describe how Hubble's SPIKE scheduler represents constraints, and why a planner of this kind is easier to verify than a neural network.
3. For each of these tasks, name the problem type and a suitable metric: mapping flood extent from radar images; predicting the Kp index three hours ahead; choosing which of 50 images to downlink first; finding unusual behaviour in battery telemetry.
4. A loss surface has Hessian eigenvalues of 0.5 and 20. What is the largest stable learning rate for gradient descent, and what is its condition number? Why does standardising the inputs help?
5. Repeat the gradient-descent example for a clear vegetation pixel $x$ = (0.06, 0.22), $y$ = 0, starting from the updated parameters. How does the prediction change?
6. Sketch training and validation loss against epochs for a network that overfits. What is early stopping, and how do weight decay and data augmentation reduce overfitting?
7. Why did random cross-validation give R² = 0.80 in @fig:spatialcv when the model's skill in a new region was negative? How would you choose the block size for spatial cross-validation of a soil-moisture model?
8. Explain how a random forest reduces the variance of decision trees, and how gradient boosting differs. Why did EO-1 use a linear rather than a kernel SVM on board?
9. A conjunction-screening model raises 40 alerts in a year, of which 4 are real high-risk events, and misses 1. Compute its precision, recall and F1. Why is accuracy not useful here?
10. How many independent negative samples are needed to measure a false-alarm rate of 2 % to within ±0.5 % at 95 % confidence? How does spatial correlation between test pixels change the answer?
:::
