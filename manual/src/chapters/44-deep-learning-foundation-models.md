---
title: Deep Learning, Foundation Models and Generative AI
hero: ch44
abstract: Deep neural networks now map floods from radar, find fresh craters on Mars, forecast the weather and help plan rover drives. This chapter explains how they work, from first principles and with small networks written and trained from scratch. It covers the building blocks of deep networks and the scaling laws that govern them; convolutional networks for images; recurrent networks, transformers and graph networks for telemetry, sequences and meshes; and generative models from autoencoders to diffusion. It then describes self-supervised foundation models for Earth, Sun and Moon, large language models and agents, physics-informed learning, uncertainty quantification and explainability. Verified examples show what each method has achieved in space as of October 2026, and where it can fail.
---

Chapter 43 showed how a small neural network learns by gradient descent. **Deep learning** stacks many such layers — tens to hundreds — and trains them on large data sets. The network then learns its own features from raw pixels, spectra or telemetry, instead of relying on features chosen by an engineer. Since about 2012 this approach has overtaken older methods in image recognition, speech, translation and, since 2023, global weather forecasting.

This chapter explains the main families of deep networks, each in plain words with its key equations, then its space uses. Most figures come from small numpy networks trained for this book, so every number can be checked. Data and onboard processors are covered in Chapter 45, applications in Chapters 46–52 and assurance in Chapter 53.

## Building Blocks of Deep Networks

A deep network is a chain of simple, differentiable steps. Each step is cheap; the power comes from stacking many of them and fitting millions of weights to data. Almost every modern network uses the same few parts: linear layers, activations, careful initialisation, normalisation, residual connections and an adaptive optimiser.

### Neurons, Activations and Layers

An artificial **neuron** computes a weighted sum of its inputs, adds a bias and passes the result through an **activation function** $f$: $y = f(\mathbf{w}^\top \mathbf{x} + b)$. A **layer** is many neurons side by side, so it computes $\mathbf{h} = f(W\mathbf{x} + \mathbf{b})$. Without the activation, any stack of layers would collapse into a single matrix multiplication and could only draw straight boundaries.

@fig:dlblocks (a) shows the common activations. The **sigmoid** and **tanh** squash inputs into a fixed range; their slope is almost zero for large inputs, which slows learning. The **rectified linear unit (ReLU)**, $\max(0, z)$, has slope 1 for every positive input and is cheap to compute. **GELU** and **SiLU** are smooth versions of it used in transformers. For classification the last layer uses the **softmax**, $p_k = e^{z_k}/\sum_j e^{z_j}$, which turns scores into probabilities that sum to one.

![Building blocks, computed in numpy. (a) Common activations. (b) Activation spread through 30 ReLU layers: He initialisation (variance 2/n) keeps it near 1; 1/n and 4/n make it vanish or explode, unless layer normalisation is used. (c) One small network trained by three optimisers, each at its best learning rate.](figures/out/ch44_blocks.svg){#fig:dlblocks width=100%}

### Training: Backpropagation and Optimisers

Training uses **backpropagation**, which applies the chain rule backwards through the layers to find the gradient of the loss with respect to every weight (Chapter 43). Plain **stochastic gradient descent (SGD)** then steps each weight downhill. Two refinements make training much faster.

**Momentum** keeps a running sum of past gradients, $\mathbf{v}_t = \beta \mathbf{v}_{t-1} + \mathbf{g}_t$, and steps along it, $\theta_t = \theta_{t-1} - \eta \mathbf{v}_t$, with $\beta \approx 0.9$. Like a heavy ball, it rolls through small bumps and along narrow valleys. **Adam** also tracks the mean square of each weight's gradient and divides by its square root:

$$ \mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1-\beta_1)\mathbf{g}_t, \quad \mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1-\beta_2)\mathbf{g}_t^2, \quad \theta_t = \theta_{t-1} - \eta\,\frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}, $$

where $\hat{\mathbf{m}}_t$ and $\hat{\mathbf{v}}_t$ are corrected for their start at zero, $\beta_1$ = 0.9 and $\beta_2$ = 0.999. Each weight thus gets its own step size. In @fig:dlblocks (c), a network with two hidden layers of 64 units learns a smooth two-dimensional function. After 10 epochs (passes through the data) the validation error is 0.088 with plain SGD, 0.050 with momentum and 0.033 with Adam. After 40 epochs Adam reaches 0.020, against a noise floor of 0.010. Large models also use a **learning-rate schedule**: a short warm-up, then a slow decay.

### Initialisation, Normalisation and Regularisation

Deep networks are fragile at the start. If the initial weights are slightly too small, the signal shrinks at every layer; if slightly too large, it explodes. @fig:dlblocks (b) sends random inputs through 30 ReLU layers. With weight variance $1/n$ ($n$ inputs per neuron) the spread of the activations falls to 3 × 10⁻⁵ of its starting value. With $4/n$ it grows to 4 × 10⁴. **He initialisation**, with variance $2/n$, keeps it near 1, because ReLU zeroes half of its inputs. Gradients flowing backwards suffer the same fate, which is why badly initialised deep networks do not learn.

**Normalisation layers** fix the scale during training as well. **Layer normalisation** rescales each sample's activations to zero mean and unit variance, then applies a learned scale $\gamma$ and shift $\beta$: $y = \gamma (x - \mu)/\sigma + \beta$. **Batch normalisation** does the same across a mini-batch. **Dropout** randomly zeroes 10–50 % of units during training, so the network cannot rely on any single one.

### Scaling Laws

Since 2020, studies of language models have found that test loss falls smoothly, as a **power law**, as the number of parameters $N$, the number of training tokens $D$ and the compute $C$ grow. Hoffmann and colleagues (2022) fitted

$$ L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}, \qquad C \approx 6ND, $$

with $E$ = 1.69, $A$ = 406.4, $B$ = 410.7, $\alpha$ = 0.34 and $\beta$ = 0.28. $E$ is the loss that no model can beat, set by the randomness of language itself. The cost rule $C \approx 6ND$ counts about six floating-point operations (FLOP) per parameter per training token: two for the forward pass and four for the backward pass.

The formula answers a practical question: for a fixed compute budget, how big should the model be? @fig:scalinglaws computes it. For 10²² FLOP the best choice is about 5 billion parameters trained on about 320 billion tokens, giving a loss of 2.14. A 1-billion-parameter model trained with the same compute on five times more data reaches only 2.20. With these constants the optimal model size grows as $C^{0.45}$ and the data as $C^{0.55}$, so data matter as much as parameters.

![Scaling laws from the published fit of Hoffmann et al. (2022). (a) Predicted loss against model size and data; dashed lines join points of equal compute, and the red line marks the best split. (b) Loss against compute: each fixed model size flattens, while the compute-optimal curve keeps falling.](figures/out/ch44_scaling.svg){#fig:scalinglaws width=100%}

Two cautions apply. First, for budgets of 10²⁰–10²⁴ FLOP these published constants imply 40–100 tokens per parameter. The paper's other two methods recommend about 20. A 2024 replication traced the difference to errors in this fit. Second, the constants are for mostly English text. Earth-observation and weather models show similar trends, but with their own constants.

## Convolutional Networks for Images

Images have structure: nearby pixels are related, and a coastline or a crater looks the same wherever it appears. A **convolutional neural network (CNN)** builds these facts into its design. It is the workhorse of image analysis in space, from cloud masks to crater catalogues.

### Convolution, Pooling and Receptive Field

A **convolution layer** slides a small grid of weights, the **kernel**, over the image. At each position it multiplies the kernel by the pixels beneath and sums the result. Output channel $c'$ at pixel $(i, j)$ is

$$ y_{i,j,c'} = b_{c'} + \sum_{c} \sum_{u=0}^{k-1} \sum_{v=0}^{k-1} w_{u,v,c,c'}\; x_{i+u,\,j+v,\,c}. $$

Here $c$ counts input channels and the kernel is $k \times k$ pixels. The same kernel is used everywhere — **weight sharing** — so a layer needs only $k^2 c\, c'$ weights, whatever the image size. Each output channel is a **feature map** that responds to one pattern. In @fig:convmaps, hand-made kernels detect edges, texture and spots in a Landsat 5 image of Las Vegas. **Max-pooling** then keeps the largest value in each 4 × 4 block. A trained CNN learns similar filters in its first layer and combines them into shapes and objects in deeper layers.

![Feature maps of a real satellite image: fixed kernels applied to a 480 × 480-pixel crop of a Landsat 5 false-colour image of Las Vegas (2 November 2011). (b–e) Edge, texture and spot filters; (f) texture energy; (g) ReLU and 4 × 4 max-pooling of (b); (h) receptive-field growth with depth.](figures/out/ch44_convmaps.svg){#fig:convmaps width=100%}

The **receptive field** is the patch of input that can influence one output pixel. Twelve stacked 3 × 3 layers see only 25 × 25 pixels. Adding 2 × 2 pooling after every second layer widens this to 316 pixels. **Dilated (atrous) convolutions** space the kernel taps apart; doubling the spacing at each layer gives 8 191 pixels after 12 layers, without losing resolution (@fig:convmaps h). Context matters: telling a lake from a cloud shadow needs a view of the surroundings.

### Residual Networks

Simply stacking more layers eventually makes networks harder to train. **Residual networks (ResNets)** (2015) fixed this with a shortcut: each block learns a correction $F(\mathbf{x})$ and outputs $\mathbf{y} = \mathrm{ReLU}(F(\mathbf{x}) + \mathbf{x})$ (@fig:cnnarch). An unneeded block can learn $F \approx 0$ and pass its input straight through, and gradients flow back through the shortcuts undiminished. An ensemble of ResNets, the deepest with 152 layers, won the 2015 ImageNet competition with a top-5 error of 3.57 %. Residual connections are now in almost every deep network.

![Three convolutional architectures. Top: a small classifier for 256 × 256-pixel, four-band chips, with the data shape after each stage (see the worked example). Bottom: a residual block, and a U-Net whose skip connections copy fine detail from encoder to decoder.](figures/out/ch44_cnnarch.svg){#fig:cnnarch width=94%}

::: example
**Example: parameters and operations of a small CNN**

The classifier at the top of @fig:cnnarch takes 256 × 256-pixel chips with four bands. It has three 3 × 3 convolution layers with 32, 64 and 128 channels, with 2 × 2 pooling before the second and third. Global average pooling and a dense layer for 10 classes follow.

1. **One layer.** A convolution has $k^2 c_{in} c_{out} + c_{out}$ parameters and needs $H W k^2 c_{in} c_{out}$ multiply–accumulate operations (MACs). Layer 1: 9 × 4 × 32 + 32 = **1 184 parameters**, and 256 × 256 × 9 × 4 × 32 = 75.5 million MACs.
2. **Layers 2 and 3.** Layer 2 has 9 × 32 × 64 + 64 = 18 496 parameters at 128 × 128 pixels (302 million MACs). Layer 3 has 9 × 64 × 128 + 128 = 73 856 parameters at 64 × 64 pixels (also 302 million MACs).
3. **Head.** Pooling has no weights; the dense layer has 128 × 10 + 10 = 1 290.
4. **Totals.** The network has **94 826 parameters** and needs 679 million MACs, or **1.36 GFLOP** (two operations per MAC), per chip.
5. **Weight sharing.** A dense layer mapping the same input to the same 256 × 256 × 32 output would need 5.5 × 10¹¹ weights — about six million times more than the whole network.
6. **A whole scene.** A 10 000 × 10 000-pixel scene holds about 1 526 chips: about 2.1 × 10¹² operations, or some 2 seconds on a processor sustaining 10¹² operations per second (1 TOPS; Chapter 45).
:::

### Object Detection

**Object detection** finds each object in an image and draws a box around it with a class label. **Two-stage detectors**, such as Faster R-CNN (2015), first propose regions that might contain an object, then classify and refine each one. They are accurate but slower. **One-stage detectors**, such as the YOLO ("you only look once", 2016) family, divide the image into a grid and predict boxes and classes for every cell in a single pass. Overlapping boxes for the same object are then merged by **non-maximum suppression**. Ultralytics' YOLO26, released in January 2026, removes that step by predicting one box per object directly. Detection is scored by mean average precision (mAP, Chapter 43). Ships, aircraft and vehicles in satellite images are detected this way (Chapter 46), as are craters and boulders on planetary surfaces.

::: history
**Landmark: AI finds fresh craters on Mars (2020)**

- Fresh impacts on Mars are found by comparing before-and-after images, a slow task for people. JPL researchers trained a classifier on 6 830 Context Camera (CTX) images from Mars Reconnaissance Orbiter.
- Running up to 750 copies in parallel on a JPL cluster, it scanned about 112 000 CTX images, at about 5 seconds per image against about 40 minutes for a human.
- Its first confirmed find was a cluster of craters up to about 4 m across in Noctis Fossae, formed between March 2010 and May 2012. HiRISE confirmed it on 26 August 2020 (@fig:aicraters), and more than 20 further candidates were queued for follow-up.
- The network did not replace the scientists: it ranked the archive so that HiRISE looked where a discovery was likely.
:::

![The first crater cluster on Mars found by artificial intelligence, seen by HiRISE on Mars Reconnaissance Orbiter. A classifier flagged the dark spots in Context Camera images; HiRISE confirmed fresh craters made by one impactor that broke apart.](figures/photos/ch44_marscraters.jpg){#fig:aicraters width=55%}

### Semantic Segmentation

**Semantic segmentation** assigns a class to every pixel: water or land, cloud or clear, sand or bedrock. The **U-Net** (2015) is an encoder–decoder (@fig:cnnarch): the encoder shrinks the image while widening the view, the decoder up-samples back to full resolution, and **skip connections** copy fine detail across. **DeepLab** (2014–18) instead uses dilated convolutions and a pyramid of dilation rates to capture context at several scales. @tbl:visionarch summarises the vision architectures and their space uses.

DeepMoon (2019) trained a U-Net on lunar elevation maps. It recovered 92 % of the craters in its test catalogue and nearly doubled the number found, though about 11 % of the new detections checked by hand were false. NASA JPL's **AI4Mars** project collected about 326 000 crowd-sourced labels on about 35 000 rover images, marking soil, bedrock, sand and big rocks (@fig:ai4marsphoto). A DeepLabv3 network trained on them classified more than 96 % of test pixels correctly. Terrain classifiers of this kind support Curiosity's drive planning on the ground (Chapter 48).

| Task | Architecture | Key idea | Space example |
|---|---|---|---|
| Scene classification | ResNet, EfficientNet, ViT | Deep features, one label per image | Land-use classes, image triage on board |
| Object detection | Faster R-CNN; YOLO family | Region proposals; single-pass grid | Ships, aircraft, craters, boulders |
| Semantic segmentation | U-Net, DeepLab | Encoder–decoder with skips; dilation | Floods, clouds, burn scars, Mars terrain |
| Instance segmentation | Mask R-CNN | Box plus per-object mask | Building footprints, individual fields |
| Super-resolution | Residual CNNs, GANs, diffusion | Learned up-sampling | Sharpening multispectral bands |

: Vision architectures and typical space uses. {#tbl:visionarch}

![The public AI4Mars labelling tool. Volunteers outlined soil, bedrock, sand and large rocks in Curiosity images to train terrain-segmentation networks.](figures/photos/ch44_ai4mars.jpg){#fig:ai4marsphoto width=75%}

## Sequences, Transformers and Graphs

Telemetry, light curves and solar-wind data are **sequences**, in which the past helps predict the future. Weather on a sphere and satellite networks are better described as **graphs**. This section covers networks for both, including the now-dominant transformer.

### Recurrent Networks, LSTM and Temporal Convolutions

A **recurrent neural network (RNN)** reads a sequence one step at a time and keeps a **hidden state** that summarises what it has seen: $\mathbf{h}_t = \tanh(W_h \mathbf{h}_{t-1} + W_x \mathbf{x}_t + \mathbf{b})$. Gradients are multiplied by one matrix per step backwards through time, so they shrink or explode over long sequences. Plain RNNs forget after a few tens of steps.

The **long short-term memory (LSTM)** network (1997) adds a separate **cell state** $\mathbf{c}_t$ and three gates, each a sigmoid between 0 and 1. The forget gate $\mathbf{f}_t$ decides what to keep, the input gate $\mathbf{i}_t$ what to add and the output gate $\mathbf{o}_t$ what to show:

$$ \mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t, \qquad \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t), $$

where $\odot$ means element-by-element multiplication. Because the cell state is updated by addition, information and gradients survive hundreds of steps. The **gated recurrent unit (GRU)** (2014) is a lighter version with two gates. In 2018 JPL researchers used LSTMs to predict telemetry from the SMAP satellite and the Curiosity rover; large prediction errors flagged anomalies (Chapter 49).

A **temporal convolutional network (TCN)** applies one-dimensional convolutions that look only at the past (**causal** convolutions), with dilations 1, 2, 4, 8 and so on. With kernel size $k$ and $L$ layers, its receptive field is $1 + (k-1)(2^L - 1)$ samples: 2 047 samples for $k$ = 3 and ten layers. Unlike an RNN, a TCN processes all time steps in parallel during training. @tbl:seqmodels compares the options.

| Model | How it remembers | Parallel training | Cost per sequence | Typical space use |
|---|---|---|---|---|
| RNN | Hidden state | No | Linear in length | Rarely used alone today |
| LSTM / GRU | Gated cell state | No | Linear | Telemetry prediction, anomaly detection |
| TCN | Dilated causal convolutions | Yes | Linear | Fast onboard forecasting, event detection |
| Transformer | Attention over all past steps | Yes | Quadratic in length | Long telemetry, solar time series, language |

: Sequence models compared. {#tbl:seqmodels}

### Attention

**Attention** lets each element of a sequence look directly at every other element and weigh its importance. Each input vector is projected into a **query** $\mathbf{q}$ ("what am I looking for?"), a **key** $\mathbf{k}$ ("what do I contain?") and a **value** $\mathbf{v}$ ("what do I pass on?"). Stacking them into matrices $Q$, $K$ and $V$ gives **scaled dot-product attention**:

$$ \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V. $$

Each softmax row holds weights that sum to one, so each output is a weighted average of the values. The weights are large where the query matches the key. Dividing by $\sqrt{d_k}$, where $d_k$ is the key length, keeps the softmax in a range with useful gradients. For forecasting, a **causal mask** sets the weights on future positions to zero.

In @fig:attnweights, a single attention layer trained in numpy predicts the next sample of noisy periodic "telemetry". The period is 16 steps, but the model was not told this. After 4 000 training steps it looks back 15 and 31 steps, each with a mean weight of 0.21. These are the samples at the same phase one and two cycles before the predicted one. Averaging several noisy copies of the same phase cancels much of the noise. On new sequences its error is 0.331, against 0.551 for repeating the last value and 0.425 for copying the value one period earlier. The noise sets a floor of 0.30.

![A causal self-attention layer trained in numpy on noisy periodic signals. (a) One test sequence and its forecast. (b) Mean learned attention weights: bright diagonals one and two periods back. (c) Mean weight against look-back: 0.21 at 15 and at 31 steps. Test RMSE 0.331, against 0.551 for persistence.](figures/out/ch44_attention.svg){#fig:attnweights width=96%}

### The Transformer

The **transformer** (2017) is built from attention. Each layer has a **multi-head attention** block: several attention operations in parallel, so that different heads can track different relationships. A small two-layer network, applied to each position, follows. Both parts have residual connections and layer normalisation. A layer of width $d$ has about $12d^2$ weights: $4d^2$ for the attention projections and $8d^2$ for the position-wise network.

Attention ignores order, so each element's position is added to its input vector as a **positional encoding**. The original transformer used sine waves of different frequencies, $PE_{p,2i} = \sin(p/10\,000^{2i/d})$ and $PE_{p,2i+1} = \cos(p/10\,000^{2i/d})$; many newer models learn them.

The **vision transformer (ViT)** (2020) cuts an image into patches, typically 16 × 16 pixels, and treats them as a sequence of "words". The **Swin transformer** (2021) limits attention to windows of 7 × 7 patches and shifts the windows between layers so that information still spreads. Prithvi uses ViTs; Microsoft's Aurora weather model uses a three-dimensional Swin transformer.

For time series, transformers treat each time step, or a short patch of steps, as a token. They can relate events far apart, such as a solar active region seen again one rotation (27 days) later. But they are not always better: a 2023 study found that a simple linear model beat several transformer forecasters on standard benchmarks. Always compare with persistence, climatology and a linear model.

### Why Attention Is Expensive

Attention compares every token with every other one, so its cost grows with the **square** of the sequence length $n$. Per layer, the projections and position-wise network cost about $24nd^2$ FLOP and the attention itself $4n^2d$. The first term dominates for short sequences, the second for long ones.

::: example
**Example: attention cost for an image split into 16 × 16 patches**

Take a ViT-Base layer: width $d$ = 768 and 12 heads.

1. **A 224 × 224 image** gives (224/16)² = **196 patches**. The linear parts cost 24 × 196 × 768² = 2.8 GFLOP and attention 4 × 196² × 768 = 0.12 GFLOP: only 4 % of the layer. The attention matrices of all 12 heads, stored in 16-bit numbers, take about 1 MB.
2. **A 1 024 × 1 024 image** gives 4 096 patches. Linear parts: 58 GFLOP; attention: 51.5 GFLOP, now 47 % of the cost. The score matrices take 4 096² × 12 × 2 bytes = **403 MB per layer**.
3. **A 4 096 × 4 096 solar image** from SDO gives 65 536 patches. Attention costs 13 200 GFLOP per layer — 93 % of the total — and its score matrices would need **103 GB per layer**, more than most processors hold.
4. **Windows.** Restricting attention to 7 × 7-patch windows, as in Swin, cuts the attention cost to 4 × 65 536 × 49 × 768 = 9.9 GFLOP, about 1 340 times less.
5. **Conclusion.** Full-resolution images and long records need windowed, sparse or memory-efficient attention. The Surya solar model, for example, combines spectral filtering with long- and short-range attention to handle 4 096 × 4 096-pixel SDO images.
:::

### Graph Neural Networks

Many space problems are naturally **graphs**: nodes joined by edges. Weather on a sphere can be held on the points of a mesh, and a constellation is satellites joined by inter-satellite links. A **graph neural network (GNN)** learns on such structures by **message passing**. Each node $i$ holds a feature vector $\mathbf{h}_i$. In each layer, every neighbour $j$ sends a message computed by a small network $\phi$. The node then updates itself with another network $\psi$:

$$ \mathbf{m}_{ij} = \phi(\mathbf{h}_i, \mathbf{h}_j, \mathbf{e}_{ij}), \qquad \mathbf{h}_i \leftarrow \psi\Big(\mathbf{h}_i, \sum_{j} \mathbf{m}_{ij}\Big), $$

where $\mathbf{e}_{ij}$ describes the edge, such as its length and direction. The same small networks are used at every node, so a GNN works on graphs of any size. After $L$ layers each node has heard from nodes up to $L$ edges away.

Google DeepMind's **GraphCast** (2023) maps the atmosphere from a 0.25° grid (about one million points, 37 pressure levels) onto an icosahedral mesh, passes messages 16 times and decodes the result back to the grid. The mesh is made by splitting each triangle of an icosahedron into four, six times over (@fig:icomesh). The finest level has 40 962 nodes about 120 km apart. Its "multi-mesh" keeps the edges of all coarser levels too, so its 327 660 directed edges include links about 7 000 km long, and information crosses the globe in a few steps. With 36.7 million parameters, it makes a 10-day forecast in under a minute (Chapter 47).

![The icosahedral mesh of graph-network weather models, computed by repeated subdivision. (a) Levels 0–2 overlaid. (b) Level 4, 2 562 nodes. (c) Message passing at one node. Level 6 has 40 962 nodes with a mean spacing of 120 km.](figures/out/ch44_mesh.svg){#fig:icomesh width=100%}

ECMWF's operational AIFS model, running since 25 February 2025, also uses graph layers to encode and decode the grid, with a transformer in between. GNNs for routing traffic through constellations and for screening conjunctions are still mostly research (Chapters 49 and 50).

## Generative Models

A **generative model** learns the probability distribution of its training data and can draw new samples from it: new images, new weather states, new designs. In space engineering this supports super-resolution, synthetic training data, filling gaps under clouds, ensemble forecasts and design exploration. @tbl:genmodels compares the main families.

| Family | How it generates | Strengths | Weaknesses | Space uses |
|---|---|---|---|---|
| Autoencoder, VAE | Decodes a point from a compact latent space | Compression, smooth latent space | Blurry samples | Anomaly detection, compression |
| GAN | Generator trained to fool a discriminator | Sharp images, fast sampling | Unstable training, misses modes | Super-resolution, SAR-to-optical translation |
| Diffusion | Removes noise step by step | High quality, covers all modes | Many steps, slow sampling | Ensemble weather (GenCast), downscaling |
| Flow matching | Follows a learned velocity field from noise to data | Straighter paths, fewer steps | Newer, less tested | Fast image and weather generation |
| Autoregressive | Predicts the next token or patch | Flexible, works for text | Errors accumulate | Language models, any-to-any EO models |

: Families of generative model. {#tbl:genmodels}

### Autoencoders and Variational Autoencoders

An **autoencoder** squeezes its input through a narrow **latent** layer and then reconstructs it, so it must capture the main structure of the data in a few numbers. Inputs that it reconstructs badly are unusual, which makes autoencoders popular for telemetry anomaly detection (Chapter 49).

A **variational autoencoder (VAE)** (2013) makes the latent space probabilistic. Its encoder outputs a mean and spread for a latent vector $\mathbf{z}$. Training maximises a lower bound on the log-probability of the data.

$$ \log p(\mathbf{x}) \ \ge\ \mathbb{E}_{q(\mathbf{z}|\mathbf{x})}\big[\log p(\mathbf{x}|\mathbf{z})\big] - \mathrm{KL}\big(q(\mathbf{z}|\mathbf{x})\,\|\,p(\mathbf{z})\big). $$

The first term rewards good reconstructions. The second keeps the latent codes close to a simple Gaussian, so new samples can be made by decoding random $\mathbf{z}$. VAE samples tend to be blurry, but their compact latents are used inside many larger models.

### Generative Adversarial Networks

A **generative adversarial network (GAN)** (2014) trains two networks against each other. A **generator** $G$ turns random noise $\mathbf{z}$ into a fake sample, and a **discriminator** $D$ tries to spot the fakes. They play the game:

$$ \min_G \max_D \; \mathbb{E}_{\mathbf{x}}\big[\log D(\mathbf{x})\big] + \mathbb{E}_{\mathbf{z}}\big[\log\big(1 - D(G(\mathbf{z}))\big)\big]. $$

GANs make sharp images quickly. They have been used to sharpen satellite images and to make radar images look optical. Their training is unstable, and they can suffer **mode collapse**, producing only a few kinds of output. A GAN can also invent plausible detail: a "super-resolved" building or crater must never be mistaken for a measurement.

### Diffusion Models

**Diffusion models** learn to reverse a gradual noising process. The **forward process** adds a little Gaussian noise at each of $T$ steps, with variances $\beta_t$, until only noise remains. Its useful property is that the noisy sample at any step can be written in one go:

$$ q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\!\big(\sqrt{\bar\alpha_t}\,\mathbf{x}_0,\ (1-\bar\alpha_t)\,\mathbf{I}\big), \qquad \bar\alpha_t = \prod_{s=1}^{t}(1-\beta_s). $$

A network $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$ is trained to predict the noise that was added, with the simple loss $\mathbb{E}\,\lVert \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\rVert^2$. To generate, the **reverse process** starts from pure noise and removes a little predicted noise at each step:

$$ \mathbf{x}_{t-1} = \frac{1}{\sqrt{1-\beta_t}}\left(\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right) + \sigma_t \mathbf{z}, $$

where $\mathbf{z}$ is fresh noise and $\sigma_t$ a set variance. The noise predictor is, in effect, learning the direction towards more probable data at every noise level.

In @fig:diffusion2d, a complete diffusion model written in numpy learns a ring of eight clusters. It uses 100 noise steps and a network with three hidden layers of 128 units, trained for 9 000 steps (a little over a minute on a desktop processor). The reverse process gathers 4 000 points of pure noise onto the ring. Of the generated points, 98.5 % lie within three standard deviations of a cluster centre, against 98.7 % of real samples. Every cluster gets 10.9–14.0 % of the points, close to the ideal 12.5 %, so no mode has been lost.

![A two-dimensional diffusion model trained in numpy. (a) Training data: eight clusters on a ring. (b–e) Samples during the reverse process, from pure noise at step 100 to step 0. (f) Training loss. 98.5 % of samples fall within 3σ of a cluster, and every cluster is populated.](figures/out/ch44_diffusion.svg){#fig:diffusion2d width=100%}

**Flow matching** (2022) is a close relative. It draws a straight line from a noise sample $\mathbf{x}_0$ to a data sample $\mathbf{x}_1$, $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$, and trains a network to predict the velocity $\mathbf{x}_1 - \mathbf{x}_0$. Sampling integrates $d\mathbf{x}/dt = \mathbf{v}_\theta(\mathbf{x}, t)$, and the straighter paths need fewer steps.

### Generative Models in Space

The most important space use so far is **ensemble weather forecasting**. Google DeepMind's **GenCast** (December 2024) is a diffusion model on the sphere that generates 15-day, 0.25° forecasts as ensembles of 50 or more members. On 2019 weather it beat ECMWF's ensemble on 97.2 % of 1 320 combinations of variable, level and lead time. One member takes about 8 minutes on one TPU v5 processor. For hurricanes (@fig:miltonphoto), forecasters need the probability of each track, not one best guess (Chapter 47).

![Hurricane Milton, a Category 5 storm, in the Gulf of Mexico, seen from the International Space Station on 8 October 2024. Diffusion-based ensembles aim to give the probabilities of tracks and intensities of storms like this.](figures/photos/ch44_milton.jpg){#fig:miltonphoto width=62%}

Generative models also **downscale** coarse fields: NVIDIA's CorrDiff research model turns 25 km atmospheric data into 2 km detail over Taiwan. They create **synthetic training data**, such as rendered spacecraft images (Chapter 45), and propose structures in **generative design** (Chapter 52). TerraMind can generate a land-cover map or radar-like image from an optical one. In every case the output is a plausible sample, not a measurement.

## Foundation Models and Self-Supervised Learning

A **foundation model** is a large network pre-trained on huge amounts of unlabelled data, then adapted to many tasks with few labels. In space, labelled flood maps or flare catalogues take experts months to build, while satellites collect petabytes of unlabelled data. Foundation models exploit that imbalance (@fig:fmpipeline).

![How foundation models are built and used. Self-supervised pre-training on unlabelled archives produces an encoder that turns any input into embeddings. Small labelled data sets then adapt it to each task, and results are checked against a task-specific baseline.](figures/out/ch44_fmpipeline.svg){#fig:fmpipeline width=96%}

### Learning Without Labels

**Self-supervised learning** invents a training task from the data itself. In **masked autoencoding (MAE)** (2021) the image is cut into patches, typically 75 % of them are hidden, and the network must reconstruct the missing ones. To fill in a hidden field or coastline, it must learn what landscapes, seasons and clouds look like.

**Contrastive learning** teaches the network that two views of the same thing should map to nearby vectors. The views might be two crops of a scene, radar and optical images of the same place, or an image and its caption. Views of different things should map far apart. The common **InfoNCE** loss for a pair of embeddings $\mathbf{z}_i$ and $\mathbf{z}_j$ is

$$ \ell_{ij} = -\log \frac{\exp\big(\mathrm{sim}(\mathbf{z}_i, \mathbf{z}_j)/\tau\big)}{\sum_{k \ne i} \exp\big(\mathrm{sim}(\mathbf{z}_i, \mathbf{z}_k)/\tau\big)}, $$

where sim is the cosine similarity and $\tau$ a "temperature" setting. In 2021 an image–text model trained this way on 400 million captioned images learned to recognise objects it had never been labelled for.

The output of a pre-trained encoder is an **embedding**: a vector of tens to thousands of numbers that summarises a pixel, patch, image or day. Similar inputs have similar embeddings. Google DeepMind's **AlphaEarth Foundations** (July 2025) summarises a year of optical, radar, lidar and other data for every 10 m patch of land in 64 numbers. Annual layers for 2017–2025 are open in Google Earth Engine. Users map crops or change with a simple model on top. Google reports about 24 % lower error than the other approaches it tested.

### Adapting a Foundation Model

There are three main ways to adapt a pre-trained model (@fig:fmpipeline). A **linear probe** freezes the encoder and trains only a small classifier on its embeddings; it is cheap and hard to overfit. **Full fine-tuning** updates all weights with a new task head; it is usually the most accurate but needs memory for every weight's gradients and optimiser state.

**Parameter-efficient fine-tuning** sits in between. Its most popular form, **low-rank adaptation (LoRA)** (2021), freezes each large weight matrix $W_0$. It learns a small correction made of two thin matrices:

$$ W = W_0 + BA, \qquad B \in \mathbb{R}^{d\times r}, \ A \in \mathbb{R}^{r\times k}, \ r \ll d, k. $$

Here $r$ is the rank. For a 1 024 × 1 024 matrix with $r$ = 8, the correction has 16 384 trainable numbers instead of 1 048 576 — 1.6 %. For a 175-billion-parameter language model, the LoRA authors cut the trainable parameters about 10 000-fold and the memory about threefold. **Few-shot learning** goes further, adapting from a handful of examples.

### Earth and Space Foundation Models

Since 2023 many foundation models have been released for Earth observation (@tbl:eofms) and for the atmosphere, the Sun and the Moon (@tbl:physfms). Most are open. They differ in data, size and design, so their published scores are hard to compare.

| Model | Developer, year | Pre-training data | Size (parameters) | Licence |
|---|---|---|---|---|
| SatMAE | Stanford, 2022 | fMoW RGB and Sentinel-2 images, with time | ViT-B, ViT-L | Public code and weights |
| Prithvi-EO-1.0 | NASA, IBM, 2023 | > 1 TB of HLS optical time series, contiguous US | 100 M | Apache-2.0 |
| SkySense | Ant Group, Wuhan Univ., 2024 | 21.5 M optical and SAR time series | 2.06 B | Non-commercial research |
| Clay v1.5 | Clay Foundation, 2024 | ~70 M chips: Sentinel-1/2, Landsat, NAIP, MODIS, others | 632 M (311 M encoder) | Apache-2.0 |
| Prithvi-EO-2.0 | NASA, IBM, Jülich, 2024 | 4.2 M global HLS time series, 2014–23 | 300 M, 600 M | Apache-2.0 |
| TerraMind | IBM, ESA Φ-lab, Jülich, 2025 | 9 M aligned samples, 9 modalities incl. SAR, DEM, text | Base, Large | Apache-2.0 |
| AlphaEarth Foundations | Google DeepMind, 2025 | Optical, radar, lidar, climate | 64-number embeddings | Embeddings CC-BY 4.0 |
| OlmoEarth | Allen Institute for AI, 2025 | ~10 TB optical, radar and map layers | 1.4 M–300 M | OlmoEarth Artifact License |

: Earth-observation foundation models (status October 2026). HLS: Harmonized Landsat Sentinel-2. {#tbl:eofms}

| Model | Developer, year | Pre-training data | Size | Main uses | Licence |
|---|---|---|---|---|---|
| Prithvi WxC | NASA, IBM, 2024 | 160 MERRA-2 variables, 40 years | 2.3 B | Downscaling, gravity waves, forecasts | CDLA-Permissive-2.0 |
| Aurora | Microsoft, 2024 (Nature 2025) | > 1 million hours of geophysical data | 1.3 B | Weather, air quality, waves, cyclones | MIT |
| Surya | NASA, IBM, 2025 | 9 years of SDO images, ~218 TB | 366 M | Flares, solar wind, active regions | Apache-2.0 |
| Lunar Foundation Model | NASA, IBM, 2026 | ~2 M tile bundles from LRO, Kaguya, GRAIL and others | ViT-B size | Craters, ice prospecting | Apache-2.0 |
| INDUS | NASA, IBM, 2024 | 60 B tokens of science text | 125 M encoder, smaller variants | Search, retrieval | Apache-2.0 |
| EVE | ESA Φ-lab, Pi School, 2026 | Earth-science text, open base model | 24 B | Question answering with sources | Open release planned |

: Foundation models for the atmosphere, Sun, Moon and science text (status October 2026). {#tbl:physfms}

::: data
**Data box — Prithvi-EO-2.0 in numbers**

- **Data.** About 4.2 million samples from the global Harmonized Landsat Sentinel-2 archive (@fig:landsat9photo), each 256 × 256 pixels at 30 m with four time steps, from 2014–2023.
- **Compute.** 400 epochs on the JUWELS Booster supercomputer in Jülich: about 21 000 GPU-hours on 80 A100 processors for the 300-million-parameter model, and about 58 000 GPU-hours on 240 processors for the 600-million version.
- **Gains.** About 8 % better than Prithvi-EO-1.0 on the GEO-Bench suite. Burn scars: 90.5 % mean intersection-over-union (mIoU), against 86.9 % for version 1.0; floods: 90.3 % against 88.3 %.
- **Few labels.** Landslide mapping with about 1 % of the training data, some 50 images: 67.0 % mIoU, against 59.7 % for a U-Net trained from scratch.
:::

Foundation models do not always win. On the PANGAEA benchmark, the TerraMind authors report a mean mIoU of 59.6 % for their large model and 58.4 % for the base model. A U-Net trained for each task scored 57.6 %, and the first Prithvi model 51.0 %: only TerraMind beat the U-Net. Foundation models are most valuable when labels are scarce, tasks change often or data types must be combined.

The same recipe now reaches beyond Earth. **Surya** (August 2025) was pre-trained on about nine years of full-resolution images from the Solar Dynamics Observatory (@fig:sdophoto). Fine-tuned with LoRA, it segmented active regions with an intersection-over-union of 0.768 and, in preliminary tests, forecast flares about 16 % better than existing benchmarks. The **NASA-IBM Lunar Foundation Model** (September 2026) cut the error of a polar-ice prospectivity map by about 22 % compared with a general vision model. Its developers state that it is not yet validated for operational decisions.

::: figrow
![Landsat 9 at Vandenberg Space Force Base on 16 August 2021, before encapsulation. Harmonised Landsat and Sentinel-2 data trained the Prithvi Earth-observation models.](figures/photos/ch44_landsat9b.jpg){#fig:landsat9photo width=62%}

![The Solar Dynamics Observatory with its arrays deployed in pre-launch tests, 2009. About nine years of its images, some 218 TB, trained the Surya model.](figures/photos/ch44_sdo.jpg){#fig:sdophoto}
:::

::: history
**Landmark: the first foundation model in orbit (2025–26)**

- Researchers from Adelaide University, ESA Φ-lab, Thales Alenia Space and the SmartSat Cooperative Research Centre compressed Prithvi-EO-2.0-300M for spacecraft processors.
- They used knowledge distillation: training a small "student" network to copy the large "teacher". It cut the width from 1 024 to 256 and the file from 1.2 GB to 73 MB, about 16 times smaller. Accuracy on cloud detection stayed within about one percentage point, and biomass error within 3 %.
- The compact model ran on the IMAGIN-e payload on the International Space Station, on an ordinary 16-core ARM processor, using an uploaded test set. For South Australia's Kanyini cubesat, the December 2025 preprint reported only ground tests on an engineering model. In May 2026 NASA reported that the model had also been uploaded to Kanyini. It called it the first geospatial foundation model deployed in orbit.
- Open weights spared the team from training its own model. Onboard hardware and compression are discussed in Chapter 45.
:::

## Large Language Models and Agents

A **large language model (LLM)** is a transformer trained to predict the next piece of text. Scaled to billions of parameters and trillions of words, this simple task yields systems that answer questions, summarise documents, write code and follow instructions. In 2025 such models even helped plan a Mars rover drive.

### How Language Models Are Trained

Text is first split into **tokens**: common words, parts of words or single characters, typically about three-quarters of an English word each. A model with parameters $\theta$ learns to give a high probability to each actual next token. **Pre-training** minimises the average negative log-probability over a huge text corpus:

$$ \mathcal{L}(\theta) = -\frac{1}{T}\sum_{t=1}^{T} \log p_\theta(x_t \mid x_1, \dots, x_{t-1}). $$

To predict well, the model must absorb grammar, facts and some reasoning patterns, but it only continues text. **Instruction tuning** fine-tunes it on examples of requests and good answers. In **reinforcement learning from human feedback (RLHF)**, people rank alternative answers, a **reward model** learns their preferences, and the language model is tuned to please it. In a 2022 study, raters preferred a 1.3-billion-parameter model tuned this way to an untuned one over 100 times larger.

The **context window** is the amount of text the model can consider at once. In 2026 leading commercial models accepted about a million tokens, well over a thousand pages, though they use long contexts less reliably than advertised. **Multimodal** models also accept images, diagrams or audio, often turning image patches into tokens with a ViT.

### Retrieval, Tools and Agents

A language model's knowledge is frozen at training time and may be wrong. **Retrieval-augmented generation (RAG)** helps with both. Documents such as requirements, anomaly reports and standards are split into passages and turned into embeddings. For each question, the nearest passages are retrieved and placed in the prompt, and the model answers from them with citations. NASA and IBM's **INDUS** models (2024), trained on 60 billion tokens of science text, support this kind of search. ESA's **Earth Virtual Expert (EVE)** combines a 24-billion-parameter domain-tuned model with retrieval and a hallucination check; it had about 350 pilot users in March 2026.

**Tool use** lets a model call programs: a calculator, a database, an orbit propagator or a code interpreter. An **agent** wraps the model in a loop — plan, call tools, read the results, repeat — until the goal is reached. In December 2025 JPL engineers let commercial vision–language models plan waypoints for two Perseverance drives, of 210 m and 246 m. Every command was first checked on JPL's digital twin of the rover, which simulates over 500 000 telemetry variables (@fig:roverdriver).

![A JPL rover driver plans a Curiosity drive, using 3D glasses to see the terrain's shape. In December 2025, vision–language models proposed waypoints for two Perseverance drives; people checked every command on a digital twin.](figures/photos/ch44_roverdrivers.jpg){#fig:roverdriver width=56%}

### Hallucination

A language model generates fluent text whether or not it knows the answer. A confident, plausible but false statement is called a **hallucination**. Retrieval reduces it but does not remove it. A 2025 study of commercial legal-research tools built on RAG found that they still gave false or unsupported answers to 17–33 % of test questions.

In engineering this is a serious hazard: a wrong torque value or an invented requirement looks exactly like a correct one. Treat language-model output as a draft from an unverified source. Answers should cite sources that people can check, and safety-related changes need normal engineering review. Space uses are discussed in Chapters 49 (operations assistants), 52 (systems engineering) and 53 (assurance).

::: example
**Example: memory for a 7-billion-parameter language model**

A typical open model of this size has 32 transformer layers of width 4 096.

1. **Weights.** At 16 bits (2 bytes) per parameter: 7 × 10⁹ × 2 = **14 GB**. At 8 bits: **7 GB**. At 4 bits: **3.5 GB**, or about 3.7 GB with one 16-bit scale factor per 64 weights (4.25 bits per weight).
2. **Key–value cache.** During generation each layer stores a key and a value vector for every token: 2 × 32 × 4 096 × 2 bytes = 0.5 MB per token. A 4 096-token context needs **2.1 GB**; 32 768 tokens need **17 GB** — more than the 16-bit weights.
3. **Full fine-tuning.** Adam in mixed precision needs about 16 bytes per parameter for weights, gradients, two moments and a 32-bit master copy: about **112 GB** before activations.
4. **LoRA.** Rank-16 adapters on two projection matrices per layer add 32 × 2 × 16 × (4 096 + 4 096) = **8.4 million** trainable parameters, 0.12 % of the model. Their optimiser state needs about 0.13 GB.
5. **Conclusion.** With 4-bit weights and LoRA, the model can be fine-tuned on one 24 GB processor and run on a laptop, but it is far too large for most flight computers (Chapter 45).
:::

## Physics, Uncertainty and Explanation

Space engineering needs more than a good average score. A model must respect physics, say how sure it is and give reasons that engineers can check.

### Physics-Informed Networks and Neural Operators

A **physics-informed neural network (PINN)** (2019) adds the governing equations to the loss. If the physics is written as a differential equation $\mathcal{N}[u] = 0$, the network $u_\theta$ is trained on

$$ \mathcal{L} = \frac{1}{N_d}\sum_{i=1}^{N_d} \big|u_\theta(\mathbf{x}_i) - u_i\big|^2 + \lambda\,\frac{1}{N_r}\sum_{j=1}^{N_r} \big|\mathcal{N}[u_\theta](\mathbf{x}_j)\big|^2. $$

The first term fits the $N_d$ measurements. The second penalises the **residual** of the equations at $N_r$ points, where no data are needed; derivatives come from the same automatic differentiation used in backpropagation. Martin and Schaub's PINN gravity models learn the potential of an irregular asteroid such as Eros and take the acceleration as its gradient, which helps them extrapolate.

A **neural operator** learns a mapping between whole functions, such as from today's weather field to tomorrow's. The **Fourier neural operator (FNO)** (2020) applies a fast Fourier transform, multiplies the lowest frequencies by learned weights $R_\phi$ and transforms back: $v_{l+1} = \sigma\big(W v_l + \mathcal{F}^{-1}[R_\phi \cdot \mathcal{F}(v_l)]\big)$. Working with frequencies, it can be trained at one resolution and applied at another (Chapter 47).

A **surrogate** or **emulator** is a fast network trained to imitate a slow simulation, such as fluid dynamics or a climate model, enabling thousands of design trades (Chapter 52). **Differentiable simulators** compute gradients through the physics itself, so a trajectory or antenna shape can be optimised directly.

In @fig:densitysurrogate, a small network learns atmospheric density from 0 to 600 km from a standard-atmosphere model. Within that range its median error is 0.75 %, with a worst case of 27 % at the ground, the edge of the range. Above 600 km, where it has never seen data, the error grows to −12 % at 800 km and −54 % at 1 000 km. A hybrid that adds a learned correction to a constant-scale-height model fits better in range (median 0.57 %, worst case 6.9 %). But it extrapolates even worse, −90 % at 1 000 km, because the real scale height keeps rising as light helium takes over: a hybrid is only as good as its physics. Nor is speed automatic. Here the closed-form physics model is about ten times faster than the network, so surrogates pay off only when the model they replace is expensive.

![A neural surrogate of atmospheric density, trained in numpy on 0–600 km only. (a) Density from the physics model and two surrogates. (b) Error: below 1 % on average in range, tens of per cent beyond it. (c) Time for a million evaluations: here the physics model is about ten times faster.](figures/out/ch44_surrogate.svg){#fig:densitysurrogate width=92%}

### Uncertainty Quantification

Every prediction has two kinds of uncertainty. **Aleatoric** uncertainty is noise in the data themselves, such as a sensor's random error; more data do not reduce it. **Epistemic** uncertainty is the model's ignorance, largest where training data are sparse or absent; more data do reduce it. A useful model should report both.

A network can learn aleatoric uncertainty by predicting a mean $\mu(x)$ and a variance $\sigma^2(x)$, trained with the Gaussian negative log-likelihood $\tfrac12 \log \sigma^2 + (y - \mu)^2 / (2\sigma^2)$. For epistemic uncertainty, the methods in @tbl:uqmethods compare several plausible models. A **deep ensemble** trains several networks from different random starts; their disagreement measures epistemic uncertainty. The total variance is the mean of the members' variances plus the variance of their means.

| Method | Captures | Extra cost | Guarantee | Notes |
|---|---|---|---|---|
| Mean–variance network | Aleatoric | None | None | Overconfident far from data |
| Deep ensemble | Both | 5–10 × training and running | None | Simple, strong baseline |
| Monte Carlo dropout | Mostly epistemic | Many passes at run time | None | Cheap to add; often underestimates |
| Bayesian neural network | Both | High | Only if the prior and approximation are right | Hard to scale |
| Conformal prediction | Total (calibrated) | A calibration set | Coverage if data are exchangeable | Wraps any model |

: Ways to quantify the uncertainty of a neural network. {#tbl:uqmethods}

**Monte Carlo dropout** keeps dropout on at prediction time and treats many passes as an ensemble. **Bayesian neural networks** place probability distributions on the weights. **Conformal prediction** wraps any model in intervals with guaranteed coverage. On a separate calibration set of $n$ points it computes the scores $s_i = |y_i - \hat y_i|/\hat\sigma_i$. It takes $q$ as the $\lceil (n+1)(1-\alpha) \rceil$-th smallest score and reports $\hat y \pm q\hat\sigma$. If new data are **exchangeable** with the calibration data, meaning drawn from the same distribution, a fraction of at least $1-\alpha$ of the intervals will contain the truth.

In @fig:uqconformal, the noise of a regression problem grows across the input range. In range, the spread of five ensemble members alone covers the truth only 5 % of the time: they agree with each other but ignore the noise. The ensemble's total variance gives 87 % coverage at a nominal 90 %; conformal intervals give 91.7 % (absolute) and 90.4 % (normalised). Outside the range, the members disagree, with 40 times more epistemic spread, so the normalised intervals widen and still cover 98 %. The fixed-width band covers only 57 %: its guarantee assumed data like the calibration set.

![A deep ensemble of five numpy networks with conformal prediction. (a) Data, ensemble mean, member spread and a 90 % normalised conformal band. (b) Coverage of nominal 90 % intervals: member spread alone 5 %, total variance 87 %, conformal 91.7 % and 90.4 % in range; outside it, only variance-scaled intervals hold.](figures/out/ch44_uq.svg){#fig:uqconformal width=100%}

In space weather, Licata and Mehta (2022) trained a thermospheric-density model with calibrated uncertainty on US Space Force density data. A 2026 study of flare-intensity forecasts found that conformalised quantile regression gave the best coverage with the narrowest intervals. Calibrated uncertainty lets a conjunction analyst or forecaster decide whether to act (Chapters 47 and 50).

### Explainability

**Explainable AI** tries to show why a model produced its output. A **saliency map** shows the gradient of the output with respect to each input pixel: where a small change would most alter the answer. **Grad-CAM** (2017) weights the feature maps $A^k$ of the last convolution layer by the average gradient of the class score $y^c$, $\alpha_k^c = \frac{1}{Z}\sum_{i,j}\partial y^c / \partial A^k_{ij}$, and shows $\mathrm{ReLU}\big(\sum_k \alpha^c_k A^k\big)$ as a heat map. **Integrated gradients** (2017) average the gradient along a straight path from a neutral baseline image $\mathbf{x}'$ to the input:

$$ \mathrm{IG}_i(\mathbf{x}) = (x_i - x'_i)\int_0^1 \frac{\partial F\big(\mathbf{x}' + a(\mathbf{x} - \mathbf{x}')\big)}{\partial x_i}\, da. $$

The attributions add up exactly to $F(\mathbf{x}) - F(\mathbf{x}')$. **SHAP** values (2017) share a prediction among the input features using Shapley values from game theory: each feature's average contribution over all subsets of the others.

Explanations are most useful for catching **shortcuts**, where a model learns an accidental cue instead of the real signal. In @fig:xaishortcut, radar-like chips contain sea clutter and, in half of them, a ship. In the biased training set a bright quay strip along one edge accompanies 95 % of the ships. The trained network scores 95 % on similar test chips but 63 % when the strip appears at random, finding only 28 % of ships without one. Integrated gradients expose the shortcut: the strip, 8 % of the pixels, carries 68 % of the net evidence for "ship". When the strip is replaced by sea, detections fall from 98 % to 26 %. A network trained on clean data scores 84–85 % on both test sets, and its strip carries 1 % of the evidence.

![Explaining a ship detector that learned a shortcut (synthetic data, numpy networks). (a) Training chips, and what each model uses, averaged over 600 test ships beside a quay strip: gradient saliency looks alike, but integrated gradients show the strip dominating the shortcut model. (b) Its accuracy falls from 95 % to 63 % on unbiased data.](figures/out/ch44_xai.svg){#fig:xaishortcut width=100%}

The same figure shows the limits of explanation. The plain gradient maps of the two models look alike, and the strip carries only 7 % of the biased model's gradient: two methods, two answers. A 2018 study found that some popular saliency methods gave almost the same maps for trained and untrained networks. Test explanations, for example by removing the highlighted input and checking that the output changes.

Pandey and colleagues (2023) trained a convolutional network to forecast M-class and larger solar flares from full-disk magnetograms, with a true skill statistic of about 0.51. Guided Grad-CAM showed that it attended to active regions, even near the edge of the disk. Such an explanation supports a model but cannot prove it correct (Chapter 53).

::: note
**Practice: fine-tuning an Earth-observation foundation model with few labels**

1. **Define the task and the baseline.** For example, map flood water at 30 m within six hours of a pass. Choose the metric (water-class IoU) and a simple baseline, such as a water-index threshold or a small U-Net.
2. **Choose the model.** Pick an open model pre-trained on data like yours — Prithvi-EO-2.0 for HLS imagery, TerraMind for radar plus optical. Check its licence.
3. **Label a little, well.** Label 50–200 chips from many regions, seasons and event types. Have a second expert relabel 10 % of them to measure label noise.
4. **Split by place and time.** Hold out whole events and regions for validation and testing (Chapter 43). Never let chips from the same scene fall on both sides of a split.
5. **Start with a probe.** Freeze the encoder and train a small segmentation head on its embeddings. This takes minutes and sets a floor.
6. **Then adapt.** Add LoRA adapters (rank 8–16) or fine-tune all weights with a low learning rate (10⁻⁵–10⁻⁴), with early stopping on the validation set.
7. **Compare honestly.** Report the foundation model, the probe and the baseline on the locked test set, with confidence intervals. Keep the simplest model that meets the requirement.
8. **Check failure modes.** Inspect errors by surface type: cloud shadow, terrain shadow, urban areas, wet snow. Add labels where errors cluster.
9. **Calibrate and document.** Add conformal intervals, record data, version and limits in a model card, and monitor after deployment (Chapters 45 and 53).
:::

::: key
**Key takeaways**

- Deep networks stack linear layers and non-linear activations. They train reliably only with careful initialisation, normalisation, residual connections and optimisers such as Adam.
- Scaling laws predict how loss falls with parameters, data and compute; for a fixed budget, model size and data should grow together.
- CNNs exploit weight sharing in images: U-Nets and DeepLab segment, YOLO-type and two-stage networks detect. A small CNN may have under 100 000 weights yet need over a gigaflop per chip.
- Attention cost grows with the square of sequence length, so large images and long records need windowed or sparse attention. Graph networks pass messages on meshes.
- Diffusion models generate by removing noise step by step and underpin ensemble weather forecasts; generated outputs are samples, not measurements.
- Foundation models such as Prithvi, TerraMind, AlphaEarth, Aurora and Surya adapt to new tasks with few labels, but must still beat a simple baseline.
- Language models hallucinate: use retrieval with citations and human review. Check every model for extrapolation, calibration and shortcuts.
:::

::: questions
**Review questions**

1. Why can a network without activation functions draw only straight decision boundaries? Why is ReLU preferred to the sigmoid in hidden layers?
2. Using @fig:dlblocks, explain what goes wrong when the weight variance in a 30-layer ReLU network is 1/n or 4/n, and how He initialisation and layer normalisation fix it.
3. Using $C \approx 6ND$, estimate the training compute of a 1-billion-parameter model trained on 20 billion tokens. Would extra compute be better spent on a bigger model or on more data?
4. Compute the parameters and multiply–accumulate operations of a 3 × 3 convolution with 64 input and 64 output channels on a 128 × 128 feature map. How would they change for a 5 × 5 kernel?
5. Which architecture would you use to count ships, to map flood extent and to outline individual buildings? Explain why.
6. Write the scaled dot-product attention equation and explain the roles of the queries, keys, values and the factor $\sqrt{d_k}$. In @fig:attnweights, why does the trained head look back 15 and 31 steps rather than 16 and 32?
7. A transformer must process a 2 048 × 2 048 image in 16 × 16 patches. How many tokens is that, and how much memory do the 16-bit attention scores of 12 heads need per layer? Suggest two ways to reduce it.
8. Write the forward process of a diffusion model and state what the network learns to predict. Why is a super-resolved image not a measurement?
9. Describe masked autoencoding and LoRA. A team has 60 labelled landslide chips: outline how they should use a foundation model and how they would show it beats a U-Net.
10. In @fig:uqconformal, why does the member spread alone cover only 5 % of test points, and why does the fixed-width conformal band fail outside the training range? What does exchangeability mean for a space-weather model during a record storm?
:::
