<!-- ## BEGIN METADATA ##
title::Fractal reaction kinetics.
date:: July 26 2018
## END METADATA ## -->

# Fractal reaction kinetics.

Just about every chemistry protocol involves stirring/mixing well. A homogeneous reaction mixture greatly simplifies reaction kinetics studies, as you can assume that what you read at one point applies to the entire solution. But what about when you can't mix well (say you have solid or gelatinous reactants)? Or you have an odd surface area of reaction?

While reading about some of the assumptions behind the [Michaelis-Menten and Briggs-Haldane analyses of reaction kinetics](https://en.wikipedia.org/wiki/Michaelis–Menten_kinetics) (i.e., we're dealing with elementary, bimolecular reactions with equilibrium/quasi-steady-state on enzyme complex concentration) to try and remember what \\(K_m\\) meant in [this paper's abstract](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2138926/), I noted an interesting line about reactions in the cytoplasm:

> The first step in the derivation applies the law of mass action, which is reliant on free diffusion. However, in the environment of a living cell where there is a high concentration of proteins, the cytoplasm often behaves more like a gel than a liquid, limiting molecular movements and altering reaction rates.[20] Although the law of mass action can be valid in heterogeneous environments,[21] it is more appropriate to model the cytoplasm as a fractal, in order to capture its limited-mobility kinetics.[22]

That really interested me, so I ended up looking up what it would mean to model the cytoplasm as a fractal and found a 1988 paper by Kopelman on the subject ([DOI: 10.1126/science.241.4873.1620](https://www.researchgate.net/publication/6019289_Fractal_Reaction_Kinetics)). It's worth trying to reiterate the points of the paper. (I definitely still have questions that I'll actively list out as I go.)

## What does fractal kinetics even *mean*?

Say we have an elementary bimolecular reaction between reactants A and itself (or A and B), and the product AA (or AB) exits solution (deposition or evaporation). Normally, we want to stir a mixture of A (and B) well in order for the reaction to occur as expected (perhaps not as vigorously if the components of the mixture have a free energy of mixing that favors desegregation/maximizing the A-B interface). Would we be able to get away with not continually mixing? Well, if we aren't mixing, we'd be relying on *the diffusion of the particles* to get close enough to each other in order to react. If the particles' ability to diffuse were hindered in some way, it would be reflected in the rate of reaction. So instead of having a simple reaction-order of 2, you'd have something different.

But wait, if we aren't mixing things, then the initial distribution of reactants matters quite a bit, doesn't it? Places where reactants ended up right next to each other will react incredibly quickly, while other places with more distant reactants will do so far more slowly. So, while we keep the reaction second-order, the rate coefficient ends up being a function of time:

\\(rate = k(t)[A]^2\\)

where

\\(k(t) = k_{t=1} t^{-h}\\)

for some h in \\([0,1]\\). Seemingly without explanation, the value of h is \\(h = 1 - d_s / 2\\). \\(d_s\\) is the **spectral dimension** of the (fractal) space under consideration and is defined by the recurrence probability P(t) of a random walker: \\(P(t) \sim t^{-d_s / 2}\\).
*Question: How does one actually calculate a recurrence probability to find a space's spectral dimension, or vice-versa? (I'm guessing this is something about fractals I just don't know about, or perhaps on stochastic processes (specifically Wiener processes). Unfortunately, the paper points to a ~450 page textbook without any particular page range...)*

Also somewhat magically, it turns out that for all **random fractals** (fractals that aren't constructed from a simple recursive algorithm, e.g. Koch snowflake or Sierpinski gasket (I think? Not explained.)) of Euclidean dimension in which the fractal is embedded \\(d = 2, 3, \cdots\\), have \\(d_s \approx 4/3\\) and so \\(h = 1/3\\) for A-A reactions. *Question: Where does this magic 4/3 come from? (More fractal/random-walk background I don't know about?)*

### Steady-state reaction kinetics.

Earlier, we were talking about a batch reaction (dump everything in at once and let it go). But what about if we can reach a steady-state on a fractal-like reaction (e.g. where reactants are limited by diffusion, or are limited to a fractal-like surface)? Well, intuitively, since there is less possible space for a reactant to land on compared to the unconstrained version of the entire (3-D) container, we'd imagine that the relative order would be greater than 2.

And in fact, this is true! For a rate equation of \\(rate = K[A]^X\\), we have in the diffusion-limited case
\\(X = 1 + 2/d_s = 1 + (1 - h)^{-1}\\)

These must be expected values since again, the reaction is heterogeneous across the area of reaction. For fractal spaces, \\(d_s < d_f < d\\) (where \\(m \sim x^{d_f}\\), \\(m\\) is a measure of "mass", and \\(x\\) is a measure of "length" (like a diameter)). *Question: Why does this inequality hold for fractal spaces? In particular, the first inequality, \\(d_s < d_f\\)?* So we can bound \\(d_s\\) by \\(d_f\\) and assert that fractal spaces can have ludicrously high power relations (and in fact values of \\(X \approx 75\\) have been shown in "dust-like" spaces, i.e. spaces with fractal dimension \\(0 < d_f < 1\\)).

## Fractals -- neat *and* relevant!

Besides being incredibly neat, fractals show up all over nature.
The example that motivated me to read the paper was on reactions in cytoplasm (and other gel-like substances) having these fractal-like kinetics.
The paper also references chemical reactions involving **excitons** (electron/electron-hole pairs) as exhibit fractal kinetics. Surface chemistry can exhibit fractal-like kinetics if "shredded", as such shredding leads to "isolated islands" on which the chemicals can react and these islands have shown to have fractal-like kinetics.
Reactions in thin cylindrical tubes where chemicals take much longer to react than to reach the edge of the cylinder, fractal-like kinetics (\\(h = 1/2\\)) occur.

Having a better sense of how these fractal kinetics would be important in modeling chemical reactions properly in areas that lend itself to fractal-like behavior. Since some places are biologically relevant (e.g. cytoplasm), this would be worth knowing to establish onset of pharmaceutical action, and perhaps can inform the drug's viability (e.g. if it gets swept away by peroxisomes before doing anything due to "lagging" in the capillary bed (a fractal-like location in the human body) or the cytoplasm of the target cell, it probably isn't a good candidate drug). Also, often, steady-state approximations are assumed in initial theorizing of pharmacokinetic models. So if we have an incorrect power law, all our calculations would be quite noticeably off.

Yet another way a seemingly odd branch of mathematics makes a fascinating insertion into the natural world!

### Further reading on fractals.

I have yet to be able to answer a good number of the above questions due to the paper citing a ~450-page textbook on fractals as justification for the facts I did not know. The book is [*The Fractal Geometry of Nature* by Benoit Mandelbrot](http://www.dsf.unica.it/~fiore/libricorsoptr/The_Fractal_Geometry_of_Nature.pdf), after whom [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) is named.

\- DK, 7/27/18