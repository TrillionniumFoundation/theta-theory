# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — Sinai Homological Pressure  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`  
**Nature of this report:** independent mathematical review; compilation and checksum verification receive no theorem credit.

## Executive assessment

The paper proposes a potentially serious program: uniform spectral theory for vector displacement and roof twists in a parameter family of finite-horizon periodic Lorentz gases, a projective empirical-process LDP, an analytic physical-pressure root, and a quantitative two-sided conditioning theorem for current and clock.

If the first and last items were proved with the announced uniformity, they could form the core of a strong paper. They are not proved. The manuscript places the actual billiard analysis inside named “packets,” then treats those packets as routine inputs. It also makes invalid logical jumps from local finite-dimensional Gärtner–Ellis information to a full projective LDP and from exponential-rate information to a submacroscopic ratio/local-limit theorem.

## Major mathematical objections

### 1. The uniform twisted-billiard spectral theorem is the missing main theorem

Analytic perturbation theory begins only after a common functional-analytic framework has been built. For a radius-dependent billiard family, the phase space, singularity partitions, grazing geometry, and regularity scales vary. A valid theorem must construct common anisotropic spaces or canonical identifications and verify, uniformly in the parameter:

- one-step expansion and complexity bounds;
- distortion and homogeneity-strip estimates;
- control of grazing and singularity preimages;
- strong/weak Lasota–Yorke inequalities;
- boundedness of multiplication by displacement and roof weights;
- analytic dependence of the full vector/roof twist;
- spectral simplicity in a complex neighborhood;
- lattice span, aperiodicity, and exclusion of peripheral modes;
- compatible left/right eigenvectors and normalized Doob transforms.

The manuscript cites a framework in which such conclusions follow *provided these hypotheses are established*. It does not establish them for the announced family and weights. Naming this the “principal imported analytic packet” is an admission that the principal theorem is absent.

### 2. Local Gärtner–Ellis bounds do not imply the claimed Dawson–Gärtner LDP

For each finite collection of observables, the manuscript obtains at most a local pressure branch near the origin and bounds for sets lying in the associated gradient image. Dawson–Gärtner requires full compatible LDPs for all finite projections, with good rate functions. A family of local exposed-point bounds is not such an input.

Product compactness of bounded coordinate ranges cannot manufacture missing lower bounds, extend the pressure branch beyond its proven domain, or prove compatibility of the proposed finite-dimensional rates. Consequently the supremum over cylinder potentials defines a convex candidate functional, not a demonstrated empirical-process rate function.

The additional assertion of strict convexity modulo coboundaries for arbitrary higher-block potentials is also unproved and not even formulated on a precise quotient.

### 3. The global variational pressure is not justified by a local analytic branch

The paper extends a local Legendre transform lower-semicontinuously and then identifies it with a global variational formula over invariant measures. Such an identity requires a duality theorem for a specified function/measure pairing, an established full rate, and control of the effective domain. None is supplied by the local spectral branch.

Outside the simple-eigenvalue neighborhood, the paper may define a candidate convex continuation. It may not use that continuation as a proved microscopic pressure or as a canonical normalization for later phases.

### 4. Positive definiteness and inverse-map claims require non-coboundary/aperiodicity theorems

The formal implicit differentiation of the pressure-root equation is standard. Strict positive definiteness of the covariance of

\[
\kappa-v\tau
\]

in every nonzero homology direction, uniformly in geometry and under nearby tilts, is not formal. It requires exclusion of vector/clock coboundaries, full-rank arithmetic information, and stability under perturbation. Referring back to the unproved local-limit packet is circular.

Without this result, the asserted local diffeomorphism between tilt and velocity/current is not established.

### 5. The two-sided current/clock conditioning estimate needs a joint local-limit theorem

Conditioning on an exact \(\mathbb Z^2\) displacement and on a roof-time interval of width \(b_n=o(n)\) is far more precise than an LDP. A ratio theorem at this resolution requires a joint lattice/non-lattice local limit or Edgeworth expansion with:

- a Fourier decomposition and major/minor arc bounds;
- uniform spectral estimates for complex twists;
- smoothing control for the clock interval;
- denominator lower bounds;
- uniformity with central-cylinder insertions; and
- treatment of the regime \(b_n\ll\sqrt n\).

A Laplace principle supplies exponential rates, not local probabilities or conditional ratios. The announced error

\[
O((n-m)^{-1/2}+b_n/n+b_n^{-1}+\text{mismatch})
\]

is unsupported by any derivation. The claim that no temporal local-limit input is needed is untenable.

### 6. Higher-block twists are a second hidden spectral theorem

The empirical-process argument later invokes twisted operators for arbitrary dynamically Hölder block potentials, whereas the earlier packet concerns only displacement and roof. Passing to higher-block extensions across billiard singularities requires construction of the extensions, multiplier estimates, and spectral simplicity on each finite-dimensional domain. These are not consequences of the two-observable packet.

### 7. The paper conflates a research program with a completed proof

Several paragraphs have the logical form “standard machinery gives X” where X is precisely the nonstandard, model-specific statement: parameter-uniform billiard spaces, vector/roof local limits, or higher-block spectral control. At a top journal, these are the paper, not preliminaries that may be elided.

## Dependency assessment

A2 is an upstream gate for the later prepared-phase and filtering constructions. Until the uniform spectral/local-limit theorem is proved, no downstream paper may use its Doob data, quantitative conditioning, strict covariance, or uniform tilted mixing as certified input.

## What could become a viable paper

The authors should remove the projective-LDP and universal-pressure superstructure and prove one theorem completely: a parameter-uniform vector displacement/roof spectral and joint local-limit theorem for the specified Lorentz family. A correctly scoped ratio-conditioning corollary could then be added. That would be a serious submission; the present omnibus package is not.

## Recommendation

**Reject.** The load-bearing billiard theorem is imported rather than proved, and two central deductions—the projective LDP and submacroscopic conditioning theorem—do not follow from the stated inputs.
