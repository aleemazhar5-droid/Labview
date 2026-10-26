---
title: "AI Foundations: Machine Learning for Space Engineers"
hero: ch43
abstract: Artificial intelligence now screens clouds on board satellites, flags anomalies in telemetry, maps the planet's forests and plans rover drives on Mars. This chapter gives space engineers the foundations needed to judge, specify and build such systems. It separates symbolic AI — rules, search and planning — from machine learning, traces how each wave of AI reached space from the expert systems of the 1980s to the foundation models of the 2020s, and maps the main problem types and learning paradigms onto space examples. It then explains, with equations and computed examples, how models learn by gradient descent, why they overfit, how classical methods work, how to measure performance honestly for rare events, and how spatial and temporal autocorrelation can make a useless model look excellent.
---

A modern Earth-observation satellite can collect more data in a day than its operators could inspect in a lifetime. NASA's Earth science archive alone held 178.7 PB at the end of September 2025. It was growing by about 160 TB a day, and a large mission may record thousands of telemetry channels every second for decades. Nobody can write explicit rules for every pattern hidden in such data. **Machine learning** — programs that improve their performance by learning from examples — has therefore become as much a part of the space engineer's toolkit as orbital mechanics or link budgets.

Machine learning is also easy to misuse. A model can score 99 % accuracy and be useless; it can pass every validation test and fail on the first image from a new region. This chapter builds the foundations needed to avoid these traps: what artificial intelligence (AI) is and is not, how machines learn, which classical methods suit which problems, and how to measure performance honestly. The ten chapters that follow apply these ideas across the space ecosystem.

## What AI Is — and Is Not

**Artificial intelligence** is the field of building computer systems that perform tasks which normally require human intelligence: perceiving, reasoning, planning, deciding and learning. The term was coined for a workshop at Dartmouth College in 1956. It implies neither consciousness nor understanding, and it is not one technique but a family of them (@fig:aitaxonomy).

![How the families of AI relate. Symbolic AI encodes knowledge written down by people; machine learning learns it from data; deep learning uses many-layer neural networks; foundation models are large networks pre-trained on huge unlabelled data sets. Statistics and estimation theory overlap machine learning. All examples are space systems discussed in this chapter.](figures/out/ch43_taxonomy.svg){#fig:aitaxonomy width=94%}

### Symbolic and Learned AI

**Symbolic AI** represents knowledge explicitly, in a form that people write and read: rules ("if the bus voltage is below 26 V and the battery is discharging, shed heater loads"), facts, models and search procedures. Its main branches are **expert systems**, which apply hundreds or thousands of if–then rules elicited from specialists, and **search and planning**, which find a sequence of actions that reaches a goal within constraints. **Constraint optimisation** builds schedules that satisfy many conditions at once. **Model-based diagnosis** explains symptoms by reasoning over a model of the hardware. In **fuzzy logic**, rules hold to a degree between true and false.

**Machine learning (ML)** takes the opposite approach: the engineer provides examples and an algorithm finds a function that fits them. A cloud detector is not told that "clouds are bright in the visible and moderately bright at 1.6 µm". Instead, it is shown thousands of pixels labelled "cloud" or "clear" and works out a boundary between them. **Deep learning** uses neural networks with many layers, which learn their own features from raw images, spectra or time series (Chapter 44). **Foundation models** are very large deep networks pre-trained on enormous unlabelled data sets and then adapted to many tasks.

@tbl:symbolicvslearned compares the two traditions. The boundary is not sharp: a rover's planner may call a learned terrain classifier, and a learned model may be wrapped in hand-written safety rules. Many of the strongest space systems combine both.

| Aspect | Symbolic AI | Machine learning |
|---|---|---|
| Source of knowledge | Experts write rules, models, constraints | Algorithm infers patterns from examples |
| Typical methods | Expert systems, planners, schedulers, fuzzy logic | Regression, trees, forests, SVMs, clustering, neural networks |
| Space examples | Shuttle INCO expert system, Hubble's SPIKE, Mars Express MEXAR2 | Sea-surface temperature regression, MODIS land cover, onboard cloud screening |
| Strengths | Transparent, predictable, verifiable against requirements | Handles patterns too complex to write down; improves with data |
| Weaknesses | Brittle outside its assumptions; costly to maintain | Needs representative labelled data; can fail silently on new inputs |

: Symbolic AI and machine learning compared. {#tbl:symbolicvslearned}

### Why Symbolic Methods Still Matter in Space

Spaceflight puts a premium on **verifiability**. Flight software must be shown, before launch, to do what its requirements say in every mode the mission can enter (Chapter 6). A rule base or planner can be reviewed line by line and sometimes proved correct with formal methods. A neural network's behaviour is known only where it has been tested, and engineers must argue statistically about everything in between (Chapter 53).

Safety-critical layers — fault protection, safe modes, attitude control — are therefore still built from explicit logic and classical control. Learned models are used where their errors are tolerable or can be caught: choosing images to downlink, flagging telemetry for a human, proposing plans that a validated planner checks. On 8 and 10 December 2025 Perseverance drove 210 m and 246 m along waypoints generated by a generative AI model. Every command was first checked on a digital twin of the rover that tracked more than 500 000 telemetry variables.

### Four Waves of AI in Space

AI reached space in waves, each riding on progress elsewhere in computing (@fig:aispacetimeline).

**Expert systems and schedulers (1980s–1990s).** In 1985 NASA's Johnson Space Center began developing **CLIPS**, a rule engine written in C because the LISP-based tools of the day rarely left the laboratory; it is still maintained. In 1988, during STS-26, two expert systems ran in Mission Control for the first time. One covered the Shuttle's communications and instrumentation and was used by the INCO flight controller; the other covered its main engines. Both ran beside conventional displays so that controllers could compare them (@fig:incortds). Hubble's long-range observing plan has been built since shortly after its launch in April 1990 with **SPIKE**, a scheduler from the Space Telescope Science Institute (@fig:hubblespike). SPIKE expresses each constraint — Sun and Moon avoidance, target visibility, guide-star availability — as a "suitability" between 0 and 1 over time and searches for the schedule with the highest total suitability. In May 1999 the Remote Agent experiment took control of Deep Space 1 (Chapter 48).

![Selected milestones of artificial intelligence in space, 1980–2026, sorted into symbolic AI, classical machine learning and deep learning, with general milestones of AI along the bottom. Filled circles mark operational use, diamonds flight demonstrations or pilots, open circles research or prototypes.](figures/out/ch43_timeline.svg){#fig:aispacetimeline width=100%}

::: figrow
![Flight controller John Muratore at the INCO console in June 1988, during a simulation for STS-26. Beside him an operator works at the Real Time Data System, an expert-system workstation that monitored Shuttle telemetry.](figures/photos/ch43_inco.jpg){#fig:incortds}

![Hubble above Discovery's payload bay before its release in April 1990 (STS-31). Its long-term observing schedule has been built ever since with SPIKE, a constraint-based AI scheduler.](figures/photos/ch43_hubble.jpg){#fig:hubblespike}
:::

**Classical machine learning (1980s–2010s).** Statistical learning arrived quietly, often without the AI label. From the early 1980s NOAA computed sea-surface temperature from AVHRR's thermal channels with coefficients found by regression against drifting buoys. In the early 1990s JPL and Caltech's SKICAT used decision trees to classify faint stars and galaxies on the digitised Palomar sky survey. It reached about 94 % accuracy on objects too faint to classify by eye. From 2003–04 Earth Observing-1 ran onboard classifiers and a planner that retasked it automatically, and from 2010 the AEGIS software let Opportunity and later Curiosity choose their own rock targets.

**Deep learning (2012–).** In 2012 a deep convolutional network, AlexNet, cut the error rate of the ImageNet image-recognition contest from 26.2 % to 15.3 %. It showed that networks trained on graphics processors (GPUs) could learn better visual features than any designed by hand. In 2017 NASA's SMAP team began piloting a recurrent neural network that flags telemetry anomalies, and in 2018 JPL used networks pre-trained on everyday photographs to make NASA's Mars images searchable by content. Launched in September 2020, ESA's **Φsat-1** demonstrated a deep network screening its images for cloud on board, on a low-power Intel Movidius Myriad 2 vision processor.

**Foundation models and generative AI (2020s).** The **transformer** architecture (2017) made it practical to train networks with billions of parameters on unlabelled data; "foundation model" was coined in 2021. NASA and IBM released the Prithvi geospatial foundation model in 2023; its second version (December 2024) has 300 or 600 million parameters, pre-trained on about 4.2 million samples of harmonised Landsat and Sentinel-2 imagery. In February 2025 ECMWF made a machine-learned global weather model operational (Chapter 47). In December 2025 a satellite carrying a data-centre GPU trained a small language model in orbit. Planet's Pelican-4 detected aircraft in its own images over Alice Springs on 25 March 2026. On 1 October 2026 Google and Planet launched a prototype carrying four tensor processing units for a year-long test (Chapter 45). Most of these are **demonstrations**; operational systems still rest mainly on classical methods and carefully bounded deep networks.

## Problems, Data and Ways of Learning

### Ten Kinds of Problem

Before choosing an algorithm, an engineer must say what output is wanted. @tbl:mlproblemtypes maps ten problem types onto space examples.

| Problem type | Output | Space example | Typical methods | Typical metric |
|---|---|---|---|---|
| Classification | A class for each input | Cloud or clear pixel; land-cover type | Boosted trees, forests, CNNs | Precision, recall, F1 |
| Regression | A continuous value | Sea-surface temperature; forest biomass | Linear regression, forests, Gaussian processes | RMSE, MAE, bias |
| Semantic segmentation | A class for every pixel, keeping shapes | Flood extent, burn scars, buildings | Convolutional encoder–decoders | Intersection over union |
| Object detection | Boxes and classes | Ships in radar images, aircraft | CNN detectors | Mean average precision |
| Forecasting | Future values or event probabilities | Solar flares, geomagnetic storms, weather | Trees, SVMs, recurrent and graph networks | Skill scores, Brier score |
| Anomaly detection | "Normal" or "unusual" | Telemetry faults, radio interference | Prediction errors, isolation forests | Event precision and recall |
| Clustering | Groups found without labels | Spectral classes, solar-wind types | k-means, Gaussian mixtures | Purity, Rand index |
| Dimensionality reduction | A few variables summarising many | 8 461-channel IASI spectra sent as about 300 numbers | PCA, autoencoders | Variance explained |
| Ranking | An ordering by value | Which rock to zap, which image to downlink first | Scoring models | Precision of top items |
| Decision and control | Actions | Scheduling, rover driving, pointing | Planners, reinforcement learning | Reward, mission return |

: Machine-learning problem types and space examples. {#tbl:mlproblemtypes}

Anomaly detection and ranking show ML supporting people (@fig:smapweigh, @fig:aegistarget). JPL's telemetry monitor for SMAP and Curiosity, described in 2018, used a recurrent network to predict each of 82 telemetry channels from its recent history. It flagged values that departed from the prediction by more than an automatically set threshold. On 105 labelled anomaly sequences it reached a precision of 87.5 % and a recall of 80 %. Even so, false positives kept it from becoming central to telemetry review. Curiosity's AEGIS ranks candidate rocks in navigation-camera images by criteria set by scientists and sends the best to the ChemCam laser. Over 2.5 km of driving it picked the preferred material more than 93 % of the time, against about 24 % expected without it.

::: figrow
![NASA's SMAP satellite being weighed before launch in November 2014. Since 2017 its operations team has piloted a neural-network system that flags anomalies in its telemetry.](figures/photos/ch43_smap.jpg){#fig:smapweigh}

![Ranking on Mars: after a 13 m drive on 14 July 2016, Curiosity's AEGIS software picked the bright outcrop marked in this navigation-camera image (left); within 30 minutes ChemCam had fired its laser at nine points on it (right).](figures/photos/ch43_aegis.jpg){#fig:aegistarget}
:::

### Data, Features and Labels

Every ML problem starts with **data**: examples described by **features** $x$ (reflectances, telemetry values, orbital elements) and usually a **label** $y$ (the right answer). Good features encode physics. Clouds and snow are both bright at visible wavelengths, but snow absorbs strongly near 1.6 µm while water clouds do not (Chapter 13). A classifier given only visible bands confuses them (@fig:rockiessnow), while one given a short-wave infrared band can separate them. This chapter's examples use this two-band problem, with synthetic pixels from eight surface and cloud types.

Labels are usually the scarcest ingredient. They come from experts drawing polygons, field campaigns and in-situ sensors, volunteers, simulations and operations logs, and they are never perfect. In the EO-1 study described below, the classifiers correctly found small lakes that the expert had missed — and were scored as wrong. Label errors set a floor on the achievable error and give flexible models something false to memorise.

### Ways of Learning

The learning paradigms of @tbl:learnparadigms differ in the supervision they need, and are often combined: a network may be pre-trained without labels and fine-tuned with a few thousand.

| Paradigm | Labels needed | How it learns | Space example |
|---|---|---|---|
| Supervised | A label for every example | Fits a mapping from features to labels | EO-1 onboard classifiers; cloud masks |
| Unsupervised | None | Finds clusters or low-dimensional structure | Spectral clustering; PCA of IASI spectra |
| Self-supervised | None — data supply their own targets | Predicts hidden parts of the input | Prithvi, pre-trained on 4.2 million image samples |
| Semi-supervised | A few labels, many unlabelled examples | Extends labels to similar data | Mapping from a handful of field plots |
| Active learning | Chosen by the model | Asks for labels where most uncertain | Galaxy Zoo: 35–60 % fewer labelled galaxies |
| Transfer learning | Few, for the new task | Reuses a model trained on another task | Photo-trained networks fine-tuned on Mars images |
| Reinforcement learning | None; a reward instead | Learns actions by trial and error | Scheduling and guidance research (Chapter 48) |

: Learning paradigms. {#tbl:learnparadigms}

Galaxy Zoo shows the value of combining people and machines. Launched in July 2007, it attracted about 150 000 volunteers who made some 50 million galaxy classifications in its first year. Later, Bayesian convolutional networks sent the galaxies they were least sure about to volunteers. This **active learning** cut the number of labelled galaxies needed by 35–60 %. **Reinforcement learning (RL)**, in which an agent learns by trial and error to maximise a reward, is covered in Chapter 48.

![Snow and cloud over the Rocky Mountains in a natural-colour MODIS image from Aqua, 19 December 2012. Both are bright in the visible; telling them apart needs a short-wave infrared band, in which snow is dark.](figures/photos/ch43_rockies.jpg){#fig:rockiessnow width=40%}

## The Mathematics of Learning

### Models, Losses and Empirical Risk

A **model** is a function $f_\theta(x)$ with adjustable **parameters** $\theta$ — two coefficients in a straight-line fit, millions of weights in a neural network. A **loss function** $\ell(f_\theta(x), y)$ measures how wrong one prediction is. For regression the usual choice is the squared error $(f_\theta(x) - y)^2$. For classification the model outputs a probability $p$ that the label is 1, and the loss is the **cross-entropy**

$$ \ell = -\left[\, y \ln p + (1-y)\ln(1-p) \,\right], $$

which is zero for a confident correct answer and grows without limit for a confident wrong one. Learning means choosing the parameters that minimise the average loss over the $N$ training examples, the **empirical risk**:

$$ \hat R(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell\big(f_\theta(x_i), y_i\big). $$

What we really want is a small loss on future data, the **expected risk**; the difference between the two — the **generalisation gap** — is the central difficulty of machine learning.

### Gradient Descent

For a few models, such as ordinary least squares, the minimum has a closed form; in general it is found iteratively by **gradient descent**. The gradient $\nabla_\theta \hat R$ points uphill on the loss surface, so each step moves the parameters a little way downhill (@fig:gdpaths):

$$ \theta_{t+1} = \theta_t - \eta\, \nabla_\theta \hat R(\theta_t), $$

where the **learning rate** $\eta$ sets the step size. Computing the full gradient over millions of examples at every step is wasteful, so **stochastic gradient descent (SGD)** estimates it from a small random **mini-batch** $B$:

$$ \theta_{t+1} = \theta_t - \frac{\eta}{|B|} \sum_{i \in B} \nabla_\theta\, \ell\big(f_\theta(x_i), y_i\big). $$

![Gradient descent on the least-squares loss of a linear model with correlated predictors (r = 0.9). (a) Small steps crawl; stochastic gradient descent (mini-batches of 10) wanders near the minimum. (b) Steps near the stability limit zig-zag; η = 1.08 diverges. (c) Excess loss after 60 iterations: 1.3 × 10⁻⁵ for η = 1.0, 5 × 10⁻⁴ for η = 0.6, 0.08 for η = 0.1.](figures/out/ch43_gdpaths.svg){#fig:gdpaths width=94%}

Each step is noisy but cheap. Practical optimisers such as **Adam** add momentum (an average of recent gradients) and scale each parameter's step by the size of its recent gradients.

The learning rate is the most important setting. @fig:gdpaths shows gradient descent on the least-squares loss of a linear model with two strongly correlated predictors, which stretch the loss surface into a narrow valley. Near a minimum any loss surface behaves like a quadratic with curvatures given by the eigenvalues $\lambda$ of its Hessian (here 0.083 and 1.92), and gradient descent is stable only if $\eta < 2/\lambda_{\max}$ = 1.04. A small step crawls along the valley; a step near the limit zig-zags yet converges fastest; a slightly larger one diverges. The ratio $\kappa = \lambda_{\max}/\lambda_{\min}$, here 23, is the **condition number**: the larger it is, the slower the convergence, which is why inputs are routinely **standardised** to zero mean and unit variance.

::: example
**Example: one gradient-descent step by hand**

A logistic-regression cloud detector computes $p = \sigma(w_1 x_1 + w_2 x_2 + b)$, where $x_1$ and $x_2$ are the visible and 1.6 µm reflectances and $\sigma(z) = 1/(1+e^{-z})$. It starts with all parameters zero and sees one cloudy pixel, $x = (0.70, 0.45)$, $y = 1$, with learning rate $\eta$ = 0.5.

1. **Prediction.** $z = 0$, so $p$ = 0.5 and the cross-entropy loss is $-\ln 0.5$ = **0.693**.
2. **Gradient.** For logistic regression $\partial \ell/\partial w_j = (p - y)\,x_j$ and $\partial \ell / \partial b = p - y$. Here $p - y = -0.5$, so the gradients are $(-0.35, -0.225)$ for the weights and $-0.5$ for the bias.
3. **Update.** $w \leftarrow w - \eta \nabla_w \ell = (0.175, 0.1125)$ and $b \leftarrow 0.25$.
4. **Check.** Now $z$ = 0.175 × 0.70 + 0.1125 × 0.45 + 0.25 = 0.423, $p$ = 0.604 and the loss has fallen to **0.504**. But a clear snow pixel, $x = (0.80, 0.10)$, now also gets $p$ = 0.599: the model has learned "bright means cloud". Only more examples — including snow — and a model able to bend its boundary can fix this.
:::

### Neural Networks and Backpropagation

A **neural network** builds a flexible function by stacking simple layers. Each layer multiplies its input vector by a weight matrix, adds a bias and applies a non-linear **activation function**; the popular **ReLU** (rectified linear unit) replaces negative values by zero. A **multilayer perceptron (MLP)** with two hidden layers computes

$$ h_1 = \mathrm{ReLU}(W_1 x + b_1), \qquad h_2 = \mathrm{ReLU}(W_2 h_1 + b_2), \qquad p = \sigma(w_3^\top h_2 + b_3). $$

Training needs the gradient of the loss with respect to every weight, computed by **backpropagation**. A forward pass stores each layer's output. A backward pass then applies the chain rule layer by layer, starting from $\partial \ell/\partial z = p - y$ at the output and multiplying by each layer's weights and activation slopes on the way back. The backward pass costs only about twice the forward pass, which is why networks with billions of parameters can be trained (Chapter 44).

@fig:mlpoverfit shows such a network, written from scratch in numpy, learning the cloud-or-clear problem from only 100 pixels, one label in ten deliberately wrong. At first training and validation losses fall together. Then the network starts to fit the mislabelled pixels: training loss heads towards zero, while the loss on 2 000 independent validation pixels climbs from 0.42 to 2.7. This is **overfitting**, and the simplest cure is **early stopping** — keeping the weights from the epoch with the lowest validation loss, here epoch 39. The early-stopped network classifies 85.9 % of 20 000 test pixels correctly; trained to the end, it scores 99 % on its own training data but only 79.3 % on the test pixels.

![A numpy neural network (two hidden layers of 64 ReLU units, about 4 400 parameters) trained by backpropagation on 100 synthetic cloud and clear pixels, one label in ten wrong. (a) Validation loss is lowest at epoch 39, then rises as the network memorises label errors. (b) The early-stopped network: 85.9 % of 20 000 test pixels correct. (c) After 3 000 epochs the boundary wraps around mislabelled pixels: 79.3 %.](figures/out/ch43_mlpoverfit.svg){#fig:mlpoverfit width=100%}

### Regularisation, Bias and Variance

Any technique that discourages a model from fitting noise is **regularisation**. Early stopping is one; another adds a penalty on large weights, $\hat R(\theta) + \lambda \lVert\theta\rVert^2$ (**weight decay**, or **ridge** regression for linear models); the penalty $\lambda \sum_j |\theta_j|$ (**lasso**) drives unimportant weights to zero. Networks are also regularised by **dropout**, which randomly switches off units in training, and **data augmentation** with rotated or noisier copies of images; trees, by limiting depth.

The **bias–variance trade-off** explains why regularisation works. For squared loss, the expected error on new data splits into three parts:

$$ \mathbb{E}\big[(y - \hat f(x))^2\big] = \underbrace{\big(\mathbb{E}[\hat f(x)] - f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathrm{Var}\big[\hat f(x)\big]}_{\text{variance}} + \sigma^2 . $$

**Bias** comes from assumptions too simple for the problem; **variance** is how much the fitted model changes between training sets; $\sigma^2$ is the **irreducible error** from noise in data and labels. Simple models underfit (high bias); flexible models overfit (high variance). @fig:learningcurves (a) shows the trade-off for decision trees on 1 000 pixels: the cross-validated error is lowest, 15.1 %, at a depth of 5. Panel (b) shows **learning curves** — test error against training-set size. Logistic regression levels off at about 31 % whatever the amount of data, because a straight line cannot separate snow from cloud. A random forest and a k-nearest-neighbour classifier reach 12.3 % and 12.1 % with 20 000 pixels. That is close to the irreducible 11.9 % set by overlapping classes and 10 % label noise. Learning curves show whether more labels or a better model is needed.

![(a) The bias–variance trade-off for decision trees fitted to 1 000 synthetic cloud and clear pixels: cross-validated error is lowest (15.1 %) at depth 5 and rises to about 22 % for deep trees. (b) Learning curves: flexible models approach the irreducible error of 11.9 % as training data grow; logistic regression stays near 31 % (high bias).](figures/out/ch43_learning.svg){#fig:learningcurves width=100%}

### Training, Validation and Test Sets

Labelled data are split three ways. The **training set** fits the parameters. The **validation set** is used to choose **hyper-parameters** — settings that are not learned, such as the learning rate, network size or tree depth — and to decide when to stop. The **test set** is locked away and used once, at the end; every look at it that influences a design decision makes the final estimate optimistic. When data are scarce, **k-fold cross-validation** trains the model $k$ times, each time testing on a different fifth or tenth of the data, and averages the scores, with the test set still untouched.

### Leakage: When Space Data Cheat

**Data leakage** occurs when information about the test data reaches the model during training, so that the test score no longer measures performance on genuinely new inputs. The most dangerous leak in space applications is **autocorrelation**. Neighbouring pixels are alike, and so are consecutive telemetry samples or successive days of solar activity. With a random split, almost every test sample has a near-twin in the training set. The model can then score well by remembering places or times, rather than by learning physics that would carry it to a new region or season.

@fig:spatialcv makes the effect concrete. A random forest learns a synthetic target made of a genuine function of one predictor plus a stronger smooth spatial signal (correlation length 12 km) that no predictor explains. Five further predictors are smooth random fields unrelated to the target — but they let the forest recognise *where* a sample is. Random five-fold cross-validation reports an excellent R² of 0.80. Cross-validation with **spatial blocks** larger than the correlation length reports about 0.25. Tested in an unseen region, the model scores −0.39 — worse than predicting the regional average — while the true relationship explains only 17 % of the variance there. The forest had learned a map, not a law of nature.

![Leakage through spatial autocorrelation, computed with a random forest on a synthetic 200 km × 100 km field. (a) The target, with training samples in the western half and test samples in an unseen eastern region. (b) Random five-fold cross-validation reports R² = 0.80 and spatial-block cross-validation about 0.25; the actual skill in the new region is −0.39, and even the true relationship explains only 17 % of the variance there.](figures/out/ch43_spatialcv.svg){#fig:spatialcv width=100%}

::: data
**Data box — spatial validation of biomass maps**

- In 2020 Ploton and colleagues rebuilt a typical mapping workflow: a random forest predicting forest biomass in central Africa from 9 MODIS and 27 environmental predictors, trained on an inventory of 11.8 million trees.
- With random 10-fold cross-validation the model appeared to explain more than half of the variation (R² = 0.53); with spatial cross-validation, only 14 % (R² = 0.14). For test plots more than about 100 km from any training plot, its predictive power was close to zero; biomass was spatially autocorrelated up to about 120 km.
- Predictors with no real relationship to the target, the authors concluded, can appear powerful simply because they vary smoothly in space.
:::

The cure is to split the data the way the model will be used. Maps that must be predicted far from training sites need **spatial blocks**, or **buffers** that remove training samples near each test sample, larger than the range of autocorrelation (estimated from a variogram of the residuals). Forecasts need **forward chaining**: train on the past, test on later periods only. Products from several satellites or instruments need **grouped** splits that keep each orbit, pass, sensor or mission within one fold.

## Classical Machine Learning

Deep networks dominate image and language tasks, but most operational space products still rest on the classical methods of @tbl:classicalml. They train quickly on modest data and hardware and are easier to verify.

::: pagebreak
:::

| Method | Key idea | Strengths | Limitations | Space use (status) |
|---|---|---|---|---|
| Linear regression | Weighted sum fitted by least squares | Fast, interpretable | Linear only | AVHRR sea-surface temperature (operational since 1980s) |
| Logistic regression | Sigmoid of a weighted sum | Probabilities; baseline | Linear boundary | Baselines for flare and fire detection |
| k-nearest neighbours | Vote of the $k$ closest examples | No training | Slow; few features | Finnish forest inventory (operational since about 1990) |
| Decision tree | Sequence of threshold tests | Readable | Unstable; overfits | SKICAT (1990s); MODIS land cover (2000s) |
| Random forest | Average of randomised trees | Robust, little tuning | Large; opaque | MODIS land cover since Collection 6 |
| Gradient boosting | Trees added to correct errors | Top accuracy on tables | Needs tuning | Sentinel-2 cloud probability (operational) |
| Support vector machine | Maximum-margin boundary | Good with few samples | Slow on big data | EO-1 onboard classifiers (2004–17) |
| k-means | Nearest-centroid clustering | Fast, simple | Choice of $k$ | Unsupervised image classification |
| PCA | Main directions of variance | Compression, denoising | Linear only | IASI spectra as PC scores (since 2011) |
| Gaussian process | Prior over functions | Honest error bars | Cost grows as $N^3$ | Stellar-activity models (research) |

: Classical machine-learning methods and their space uses. {#tbl:classicalml}

### Linear and Logistic Regression

**Linear regression** predicts $\hat y = w^\top x + b$ and chooses the weights that minimise the squared error, with the closed-form solution $w = (X^\top X)^{-1}X^\top y$. NOAA's **multichannel sea-surface temperature** algorithm exploits the fact that water vapour absorbs more at 12 µm than at 11 µm. Temperature is a weighted combination of the 11 µm brightness temperature and the difference between the channels. The coefficients are found by regression against simultaneous readings from drifting buoys. In 1985 its root-mean-square difference from ship and buoy data was about 0.5 °C (Chapter 16).

**Logistic regression** turns the weighted sum into a probability, $p = \sigma(w^\top x + b)$, and is trained by minimising cross-entropy, as in the worked example. Its decision boundary, $p$ = 0.5, is a straight line (a plane, in more dimensions). That makes it a good **baseline** — every new model should be compared with a simple one. It also explains its failure in @fig:decisionbounds: no straight line can put snow on the clear side and cloud on the other.

![Decision boundaries of three classifiers trained on the same 2 000 synthetic pixels from eight surface and cloud types, 10 % of labels wrong. Logistic regression labels 96 % of snow pixels as cloud (test accuracy 68.6 %); a random forest (86.8 %) and the early-stopped numpy network (87.7 %) approach the best possible 88.1 %, whose ideal boundary is dashed.](figures/out/ch43_boundaries.svg){#fig:decisionbounds width=100%}

### Nearest Neighbours

The **k-nearest-neighbour (k-NN)** method stores the training data and, for each new input, takes a majority vote (classification) or an average (regression) of the $k$ closest examples. It needs no training and adapts to any boundary shape, but prediction is slow for large data sets and distances lose meaning when there are many features — the "curse of dimensionality". Since about 1990 Finland's multi-source national forest inventory has used k-NN to give every satellite pixel the timber volume, species and age of the field plots whose spectra it most resembles.

### Decision Trees, Random Forests and Gradient Boosting

A **decision tree** asks a sequence of threshold questions, such as "is the 1.6 µm reflectance above 0.3?". Each question is chosen to make the resulting groups as pure as possible, measured for example by the **Gini impurity** $G = 1 - \sum_k p_k^2$, where $p_k$ is the fraction of class $k$ in a group. Trees are readable and fast — the best tree JPL built for EO-1 needed at most 24 comparisons per pixel — but deep trees memorise their training data and are unstable.

A **random forest** averages hundreds of trees, each grown on a random bootstrap sample of the data and choosing each split from a random subset of features. The trees make different errors, so their average has much lower variance. NASA's MODIS land-cover product switched from a C4.5 decision tree in Collection 5 to a random forest in Collection 6, classifying the globe each year since 2001 at 500 m resolution. Hansen and colleagues' 2013 global forest-change maps applied decision trees to about 654 000 Landsat scenes, using one million CPU-core hours in Google Earth Engine.

**Gradient boosting** builds trees in sequence. Each new small tree $h_m$ is fitted to the errors (strictly, the negative gradient of the loss) left by the ensemble so far. It is added with a small weight $\nu$, so $F_m(x) = F_{m-1}(x) + \nu\, h_m(x)$. Boosted trees, in libraries such as XGBoost and LightGBM, are usually the most accurate models for tabular data. Sentinel Hub's **s2cloudless** detector is a LightGBM model working on ten Sentinel-2 bands. It underlies the cloud-probability layer distributed with Sentinel-2 imagery in Google Earth Engine, although it gives high probabilities over very bright surfaces such as snow.

### Support Vector Machines

A **support vector machine (SVM)** chooses, among all boundaries that separate two classes, the one with the widest **margin** — the largest gap to the nearest training points, the support vectors. For a linear boundary $w^\top x + b = 0$ the margin is $2/\lVert w \rVert$, so the SVM minimises

$$ \tfrac12 \lVert w \rVert^2 + C \sum_i \max\big(0,\; 1 - y_i (w^\top x_i + b)\big), $$

with labels coded $y_i = \pm 1$; the second term, the **hinge loss**, penalises points on the wrong side of the margin. A **kernel** such as the Gaussian $K(x, x') = \exp(-\gamma \lVert x - x' \rVert^2)$ lets the same mathematics draw curved boundaries. In 2015 Bobra and Couvidat used a Gaussian-kernel SVM to forecast M- and X-class flares within 24 hours (Chapter 47). It worked on magnetic-field features of solar active regions measured by the Solar Dynamics Observatory, and reached a true skill statistic of 0.76 on 303 flaring and 5 000 non-flaring examples.

::: history
**EO-1: learned classifiers in command**

NASA's Earth Observing-1, launched in 2000 as a technology demonstrator, became from 2003–04 the testbed of the **Autonomous Sciencecraft Experiment**. This onboard software analysed images from the Hyperion spectrometer, detected floods, eruptions and changes in snow and ice, and replanned observations without waiting for the ground (@fig:eo1holuhraun). The payload computer was a Mongoose V of about 8 MIPS with 256 MB of memory, and only 12 of Hyperion's bands could be read on board. JPL compared four pixel classifiers for land, water, snow, ice and cloud: one built by an expert, the best of thousands of thresholded band ratios, a decision tree and a **linear SVM** on 11 bands. The SVM needed just 11 multiplications and 11 additions per class for each pixel. On 50 expert-labelled test images (about 91 million pixels) the SVM classified 81.3 % of pixels correctly, the expert classifier 82.9 % and the tree 80.9 %. The averages hid a weakness: ice made up only 2 % of the test pixels, and the SVM found just 47.8 % of them. The expert and SVM classifiers ran on board — the SVMs for more than a dozen years, until the mission ended in 2017. The team reported a hundred-fold increase in science returned per megabyte downlinked.
:::

![The Holuhraun eruption in Iceland on 1 September 2014, imaged by EO-1 in false colour to emphasise the hottest vents and lava flows. Detecting such thermal events on board, and retasking the satellite to observe them again, was one of the jobs of EO-1's autonomy software.](figures/photos/ch43_eo1.jpg){#fig:eo1holuhraun width=46%}

### Clustering and Dimensionality Reduction

**k-means** clustering divides unlabelled data into $k$ groups. It starts from $k$ trial centres, assigns each sample to the nearest centre, moves each centre to the mean of its samples, and repeats, minimising the total squared distance $\sum_i \lVert x_i - \mu_{c(i)} \rVert^2$. Its variant ISODATA, which splits and merges clusters, has been used for unsupervised image classification since the 1970s; the analyst names each spectral cluster afterwards (Chapter 13). The number of clusters must be chosen, for example from an "elbow" in the total distance as $k$ grows.

**Principal component analysis (PCA)** finds new axes, the eigenvectors of the covariance matrix $C = \frac{1}{N}\sum_i (x_i - \bar x)(x_i - \bar x)^\top$, ordered by the variance $\lambda_k$ along each. Keeping only the first few components compresses the data and removes noise. In @fig:kmeanspca two components hold 96.6 % of the variance of six-band pixels, and k-means, never shown a label, recovers the six cover types well (adjusted Rand index 0.89, where 1 is perfect agreement). The IASI sounder on the Metop satellites measures 8 461 spectral channels. Since 2011 EUMETSAT has also distributed each spectrum as about 300 principal-component scores — a 28-fold reduction. Users reconstruct the radiances from them with much of the instrument noise removed.

![Unsupervised learning on 3 000 synthetic six-band pixels, each a shaded, noisy mixture dominated by one cover type. (a) The pure spectra. (b) PCA compresses six bands into two components holding 96.6 % of the variance; k-means with six clusters, run without labels, finds groups (crosses: centres) matching the cover types (adjusted Rand index 0.89). (c) Variance explained by each component.](figures/out/ch43_kmeanspca.svg){#fig:kmeanspca width=100%}

### Gaussian Processes

A **Gaussian process (GP)** treats the unknown function itself as random, with a **kernel** $k(x, x')$ saying how strongly the function values at two inputs are correlated — typically more strongly the closer they are. Conditioning on $N$ noisy observations $y$ gives, at a new input $x_*$, a predictive mean and variance

$$ \mu_* = k_*^\top (K + \sigma_n^2 I)^{-1} y, \qquad \sigma_*^2 = k(x_*, x_*) - k_*^\top (K + \sigma_n^2 I)^{-1} k_*, $$

where $K$ holds the kernel values between training inputs, $k_*$ those between them and $x_*$, and $\sigma_n^2$ is the noise variance. The variance widens away from the data, giving honest error bars; the cost of the $N \times N$ matrix inversion grows as $N^3$. In geostatistics the same mathematics is called **kriging**. GPs are a standard tool for separating planetary signals from stellar activity in radial-velocity planet searches. In 2014 a GP model of activity in the star CoRoT-7 gave masses of 4.73 ± 0.95 and 13.56 ± 1.08 Earth masses for its two planets (Chapter 51). They also underlie **Bayesian optimisation** of hyper-parameters.

### The Kalman Filter: Estimation Meets Learning

The **Kalman filter** (Chapter 6) estimates the state of a dynamic system — position and velocity, or attitude and gyro bias — from noisy measurements. Its **prediction** step propagates the estimate and its covariance with a dynamic model, $\hat x^- = F \hat x$ and $P^- = F P F^\top + Q$, where $Q$ is the process noise. Its **update** blends in a measurement $z$:

$$ K = P^- H^\top (H P^- H^\top + R)^{-1}, \qquad \hat x = \hat x^- + K (z - H \hat x^-), \qquad P = (I - K H) P^- , $$

where $H$ maps the state to the measurement, $R$ is the measurement noise and the **gain** $K$ weights new information by the relative confidence in prediction and measurement. This is exact **Bayesian inference** for linear systems with Gaussian noise: prior (prediction) times likelihood (measurement) gives the posterior (update). Stanley Schmidt's group at NASA Ames adapted Kalman's 1960 theory to the non-linear problem of navigating Apollo to the Moon, and the resulting **extended Kalman filter** flew in the Apollo guidance computer (@fig:lovellgn).

![Jim Lovell at the guidance and navigation station of Apollo 8 in December 1968, in a frame from 16 mm film. Star sightings made here were combined with a dynamic model in a recursive estimator of the kind adapted for Apollo at NASA Ames.](figures/photos/ch43_lovell.jpg){#fig:lovellgn width=52%}

Estimation theory and machine learning are two dialects of one language. Least-squares orbit determination (Chapter 3) is regression, and a Kalman filter can be seen as Gaussian-process regression in time. A network trained with weight decay is a maximum *a posteriori* estimate with a Gaussian prior on its weights. Estimation starts from physics with few parameters; learning starts from data with many. The best systems use physics where it is known and learning where it is not.

## Measuring Performance

### From the Confusion Matrix to F1

For a two-class detector — fire or no fire, anomaly or normal — every prediction falls into one cell of the **confusion matrix**. A **true positive** (TP) is an event correctly flagged and a **false positive** (FP) is a false alarm. A **false negative** (FN) is a miss and a **true negative** (TN) is a correct rejection. In map accuracy assessment (Chapter 13) precision is called user's accuracy and recall producer's accuracy. @tbl:evalmetrics lists the scores built from these counts. **Precision** is the fraction of alarms that are real, **recall** (probability of detection) the fraction of events found, and the **F1 score** their harmonic mean, which is high only if both are.

| Metric | Definition | Use it when | Caution |
|---|---|---|---|
| Accuracy | (TP + TN) / N | Classes are balanced | Meaningless for rare events |
| Precision | TP / (TP + FP) | False alarms are costly | Falls as events become rarer |
| Recall | TP / (TP + FN) | Misses are costly | Ignores false alarms |
| F1 | 2 × precision × recall / (precision + recall) | One number for a rare class | Depends on threshold |
| ROC AUC | Area under recall versus false-alarm rate | Comparing rankings | Optimistic for rare events |
| Average precision | Area under precision versus recall | Rare events | Depends on prevalence |
| RMSE, MAE | √(mean error²); mean absolute error | Regression | RMSE stresses large errors |
| CSI | TP / (TP + FP + FN) | Event forecasts | Depends on event rate |
| TSS | Recall − false-alarm rate | Flare and storm forecasts | Can be high with poor precision |
| Brier score | Mean of (probability − outcome)² | Probability forecasts | Compare with climatology |

: Evaluation metrics. {#tbl:evalmetrics}

::: example
**Example: scoring a wildfire detector**

A thermal-infrared fire detector is tested on a scene of 1 000 000 land pixels containing 500 fire pixels, checked by an independent high-resolution sensor (@fig:modisfires). It raises 620 alarms: 410 at real fires and 210 elsewhere.

1. **Counts.** TP = 410, FP = 210, FN = 500 − 410 = 90 and TN = 1 000 000 − 500 − 210 = 999 290.
2. **Precision** = 410 / 620 = **0.661**: one alarm in three is false. **Recall** = 410 / 500 = **0.820**. **F1** = 2 × 0.661 × 0.820 / (0.661 + 0.820) = **0.732**.
3. **False-alarm rate** = 210 / 999 500 = 2.1 × 10⁻⁴; CSI = 410 / 710 = 0.577; TSS = 0.820 − 0.0002 = 0.820.
4. **Accuracy** = (410 + 999 290) / 1 000 000 = **99.97 %** — but a "detector" that never raises an alarm scores 99.95 %. Accuracy cannot tell them apart; precision and recall can.
5. **Sensitivity.** If a season of sun glint doubles the false alarms to 420, precision falls to 0.494 and F1 to 0.617, while accuracy barely changes (99.95 %).
:::

![Smoke from lightning-caused wildfires in northern California on 4 August 2015, in a natural-colour image from MODIS on Terra. Red outlines mark actively burning areas detected by MODIS's thermal bands — a detection problem in which fire pixels are a tiny fraction of the scene.](figures/photos/ch43_fires.jpg){#fig:modisfires width=38%}

### ROC and Precision–Recall Curves

Most classifiers output a score, and an alarm is raised above a chosen **threshold**; lowering it finds more events but raises more false alarms. The **receiver operating characteristic (ROC)** curve plots recall against false-alarm rate for every threshold; its area (AUC) is the probability that a random event scores higher than a random non-event. The **precision–recall (PR)** curve plots precision against recall; its area is the **average precision** (@fig:rocpr).

![Why accuracy misleads for rare events: a logistic-regression detector on a synthetic fire task (2 001 fires among 200 000 test pixels; 5 % of clear pixels fire-like). (a) The ROC area is 0.979, yet at threshold 0.5 only 35 % of fires are found. (b) Average precision is 0.54 at 1 % prevalence, 0.86 at 10 % and 0.98 at 50 %. (c) Accuracy stays above 97.5 % at all thresholds from 0.05 to 0.95; F1 peaks at 0.52.](figures/out/ch43_rocpr.svg){#fig:rocpr width=94%}

For rare events the two tell very different stories. A logistic-regression detector for a synthetic fire task with 1 % prevalence has a near-perfect-looking ROC area of 0.979. Yet at the default threshold of 0.5 it finds only 35 % of the fires, and its average precision is just 0.54. On samples in which fires make up 10 % or 50 % of the pixels, the same detector reaches average precisions of 0.86 and 0.98 — its ROC curve does not change at all. Because the false-alarm rate divides by the huge number of non-events, the ROC curve hides the fact that even a small rate then produces as many false alarms as detections. Accuracy is worse still: it stays above 97.5 % at every threshold from 0.05 to 0.95, and a detector that never fires scores 99.0 % — the **accuracy paradox**. The threshold should be set from the real costs of misses and false alarms, not by a software default.

### Detection, Segmentation and Regression Metrics

For segmentation and object detection the basic unit is the **intersection over union** $\mathrm{IoU} = |A \cap B| / |A \cup B|$ of predicted and true regions; a detection usually counts as correct if its IoU exceeds 0.5. **Mean average precision (mAP)** averages the average precision over classes, sometimes also over IoU thresholds of 0.5–0.95, so mAP figures are comparable only under the same definition. For regression the usual scores are the **root-mean-square error** $\mathrm{RMSE} = \sqrt{\tfrac1N \sum_i (\hat y_i - y_i)^2}$, which emphasises large errors, and the **mean absolute error** (MAE). Others are the mean **bias** and R², the fraction of variance explained. As @fig:spatialcv showed, R² becomes negative when a model is worse than predicting the mean.

### Forecast Skill and Calibration

Forecasts of events use further scores. The **critical success index**, CSI = TP / (TP + FP + FN), ignores the many correct "no event" forecasts. The **true skill statistic**, TSS = recall − false-alarm rate, ranges from −1 to 1 and does not depend on how often events occur. That is why it is widely recommended for comparing flare forecasts made on different samples. A **skill score**, $\mathrm{SS} = 1 - S/S_{\mathrm{ref}}$, compares a score $S$ (lower is better) with that of a reference such as climatology or persistence.

Probabilistic forecasts must also be **calibrated**: of all the occasions on which a flare model says "30 % chance", about 30 % should see a flare. The **Brier score**, $\mathrm{BS} = \tfrac1N \sum_i (p_i - o_i)^2$ with outcomes $o_i$ of 0 or 1, rewards both calibration and sharpness, and a **reliability diagram** plots observed frequency against forecast probability. Many classifiers are poorly calibrated out of the box. Modern deep networks tend to be over-confident, while boosted trees and SVMs distort probabilities in other ways. They can be recalibrated on validation data, for example by Platt scaling or isotonic regression. Calibration matters whenever probabilities feed decisions, such as collision-avoidance manoeuvres (Chapter 21).

### Rare Events

Fires, anomalies, high-risk conjunctions and large flares are all rare, and a model that minimises average loss can do well by ignoring the rare class. Remedies include **re-weighting** the loss, **re-sampling** the classes, setting the threshold for the actual costs and evaluating with precision, recall and PR curves rather than accuracy. The EO-1 classifiers showed the problem: overall accuracy above 80 % concealed a recall below 50 % for ice, which made up 2 % of the pixels.

::: data
**Data box — rare events: ESA's collision-avoidance challenge**

- In 2019 ESA released 199 082 conjunction data messages for 15 321 close approaches involving its satellites between 2015 and 2019, each with 103 attributes. It asked competitors to predict the final collision risk two days before closest approach.
- Only 515 events (3.4 %) had a final risk of 10⁻⁶ or more, 131 (0.9 %) of 10⁻⁵ or more and 30 of 10⁻⁴ or more.
- 96 teams made 862 submissions over two months. A naive forecast — "the final risk equals the latest known risk" — scored 0.694 on the competition's loss; only 12 teams beat it, and the winners only modestly.
- The organisers concluded that naive forecasts are a surprisingly strong benchmark that machine learning can beat, but that the data's imbalance limited off-the-shelf methods (Chapter 50).
:::

### How Sure Are We?

A test score must be quoted with its uncertainty. If a detector produces $k$ false alarms among $n$ independent negative samples, the rate $\hat p = k/n$ has a standard error of about $\sqrt{\hat p (1 - \hat p)/n}$. An approximate 95 % confidence interval is $\hat p \pm 1.96$ standard errors. The **Wilson interval** is more accurate when $k$ is small. If no false alarms are seen in $n$ trials, the "rule of three" gives a 95 % upper limit of about $3/n$. Two models tested on the same samples are compared with a paired test such as McNemar's.

::: example
**Example: how big must the test set be?**

A requirement says that an onboard event detector must have a false-alarm rate of about 1 %, measured to within ±0.2 % at 95 % confidence.

1. **Sample size.** Solving $1.96\sqrt{p(1-p)/n} = E$ for $n$ gives $n = 1.96^2 \times 0.01 \times 0.99 / 0.002^2$ = **9 508 negative samples**.
2. **Check.** With 95 false alarms in 9 508 samples, the Wilson 95 % interval is 0.82–1.22 %, as required.
3. **Correlation.** Pixels are not independent. Suppose they come in clusters of 25 neighbouring pixels with an intra-cluster correlation of 0.2. The **design effect** is then 1 + (25 − 1) × 0.2 = 5.8, and about **55 000 pixels** — some 2 200 independent clusters — are needed.
4. **Rarer requirements.** Halving the interval needs four times the samples; a 0.1 % rate measured to ±0.02 % needs about 96 000 independent negatives.
5. **The positives too.** The 500 fire pixels of the wildfire example measure its recall of 0.82 only to within about ±0.034.
:::

## From Notebook to Operations

In operations a model becomes one component of a data system (@fig:mlpipeline). It may run on the ground, in a processing chain or cloud service. After verification on flight-like hardware it may also run on the spacecraft itself, where it can decide what to downlink or whether to retask the sensor (Chapter 45). In JPL's Dynamic Targeting experiment on the CogniSAT-6 cubesat in July–August 2025, the satellite looked about 74–90 seconds ahead along its track. It analysed the image for cloud on board and then pointed its camera at the clearest scenes.

::: note
**Practice: building an onboard cloud screen for a new imager**

1. **Define the decision.** The screen decides which scenes are downlinked. State the cost of each error — a cloudy scene wastes link capacity, a discarded clear scene is lost — and the onboard power, memory and time limits.
2. **Gather data.** Use data processed as on board, not ground products, covering all seasons, latitudes, Sun angles and surfaces — especially snow, ice, deserts, glint and smoke.
3. **Label.** Have experts mark cloud, thin cloud, shadow and clear; label a sample twice to measure the label-error rate.
4. **Set a baseline.** Score a physics-based threshold test on visible and 1.6 µm bands; any learned model must beat it clearly.
5. **Split by space and time.** Assign whole scenes, regions and dates to each set; hold out a region and a season entirely, and lock the test set.
6. **Train and tune.** Start with boosted trees on bands and ratios, then try a small convolutional network; tune on validation data only.
7. **Evaluate.** Report precision and recall per surface type at the chosen threshold, with confidence intervals; inspect the worst errors by eye.
8. **Deploy and verify.** Convert the model to the flight processor's number format, check its outputs against the ground version, and run it in "shadow mode" — deciding but not acting — before it controls the downlink.
9. **Monitor.** Compare flagged fractions with ground cloud masks; retrain after recalibration or for new regions.
:::

![Where machine learning sits in a space data system (top) and the nine-step workflow for building and operating a model (bottom). Models run on the ground or, once verified, are uplinked to the spacecraft; new labels and error reports from users feed retraining when performance drifts.](figures/out/ch43_pipeline.svg){#fig:mlpipeline width=92%}

Operations bring **distribution shift**: instruments degrade and are recalibrated, new satellites have slightly different spectral responses, and models meet new regions and seasons. The remedy is monitoring inputs and outputs, comparing predictions with independent reference data, and retraining when performance falls. A model must also be versioned and documented like any other flight or ground software, with its training data, test results and known limitations recorded (Chapter 53).

## Road Map of Part XIII

The rest of Part XIII builds on these foundations (@tbl:part13roadmap). Chapters 44 and 45 cover deep-learning methods, data and computers, and Chapters 46–52 apply them to each domain of the space ecosystem. Chapter 53 asks how learned systems can be verified, secured and governed well enough to be trusted.

| Chapter | Topic | Main themes |
|----|---------------------------|---------------------------------|
| 44 | Deep learning, foundation models and generative AI | CNNs, transformers, pre-trained and generative models |
| 45 | Data, computing hardware and edge AI in orbit | Data, labels, processors for onboard AI |
| 46 | AI for Earth observation | Mapping, change detection, disasters, image triage |
| 47 | AI for weather, climate and space weather | AI forecasts versus physics; flares and storms |
| 48 | AI for autonomy, navigation and robotics | Planners, AutoNav, learned guidance, RL |
| 49 | AI for mission operations, communications and networks | Anomaly detection, scheduling, cognitive radio |
| 50 | AI for space situational awareness, defence and security | Tracking, conjunctions, intelligence |
| 51 | AI for space science, planetary exploration and human spaceflight | Planet finding, planetary data, crew support |
| 52 | AI in spacecraft design, manufacturing, launch and the space business | Design, inspection, launch operations, markets |
| 53 | Trustworthy AI for space | Verification, security, governance, outlook |

: Road map of Part XIII. {#tbl:part13roadmap}

::: key
**Key takeaways**

- Symbolic AI writes knowledge down as rules and plans; machine learning learns it from examples. Space systems combine them, with verifiable logic guarding learned parts.
- AI reached space in waves — expert systems and schedulers, classical machine learning, deep learning, foundation models; most AI flying in 2026 is still demonstration.
- Learning minimises empirical risk by (stochastic) gradient descent, with learning rates below $2/\lambda_{\max}$; regularisation, early stopping and validation data control overfitting.
- Spatial and temporal autocorrelation leak information between random splits; split by block, region, time or mission, or a useless model can score R² = 0.80.
- Classical methods — regression, k-NN, trees, forests, boosting, SVMs, k-means, PCA, Gaussian processes, Kalman filters — still underpin most operational products.
- For rare events report precision, recall and skill scores with confidence intervals, not accuracy; a 1 % false-alarm rate needs about 9 500 independent negatives to measure to ±0.2 %.
:::

::: questions
**Review questions**

1. Contrast symbolic AI and machine learning, with a space example of each. Why is safe mode still implemented with explicit logic?
2. Describe how Hubble's SPIKE scheduler represents constraints, and why a planner of this kind is easier to verify than a neural network.
3. Name the problem type and a suitable metric for: mapping flood extent from radar images; predicting the Kp index three hours ahead; choosing which of 50 images to downlink first; finding unusual behaviour in battery telemetry.
4. A loss surface has Hessian eigenvalues of 0.5 and 20. What is the largest stable learning rate for gradient descent, and what is the condition number? Why does standardising the inputs help?
5. Repeat the gradient-descent example for a clear vegetation pixel $x$ = (0.06, 0.22), $y$ = 0, starting from the updated parameters. How does the prediction change?
6. Sketch training and validation loss against epochs for a network that overfits. What are early stopping, weight decay and data augmentation?
7. Why did random cross-validation give R² = 0.80 in @fig:spatialcv when the model's skill in a new region was negative? How would you choose the block size for spatial cross-validation of a soil-moisture model?
8. How does a random forest reduce the variance of decision trees, and how does gradient boosting differ? Why did EO-1 use a linear SVM on board?
9. A conjunction-screening model raises 40 alerts in a year, of which 4 are real high-risk events, and misses 1. Compute its precision, recall and F1. Why is accuracy not useful here?
10. How many independent negatives are needed to measure a 2 % false-alarm rate to ±0.5 % at 95 % confidence? How does spatial correlation change this?
:::
