# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `15cd43f9eef326010c4a1db068be5652aa8b145a`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/A2_UNIFORM_BUNDLE_THREE_REGIME_LLT.tex`, blob `0db68b69b75eb69d2893f7cee05168f4f5c7cb7b`

## Source-control verdict

The A2 controlling source is unchanged from round four. The proposed three-regime replacement is present only under `revision/round5-referee-final/`; the branch materializer failed on A1 before copying any of the eleven packets, so A2 was never installed, compiled, or subjected to the promised hostile gates.

The active theorem therefore still contains the elementary wide-window contradiction recorded in the previous report: it is linear in `b_n` throughout `b_n=o(n)`, even when `b_n` is much larger than `sqrt(n)` and the roof probability must saturate. That alone requires rejection. The candidate correctly recognizes the three Gaussian regimes, but its new functional-analytic and local-limit proofs are not complete.

## Audit of the proposed round-five replacement

### 1. The fixed-reference bundle is incompatible with zero trace spaces at births and deaths

The candidate uses a radius-independent label set and declares that a label whose geometric singular component is empty at a radius is assigned the zero trace space. It then claims, on a parameter chart crossing births and deaths, boundedly invertible identifications

\[
J_{R,j}:\mathbb B_R\longrightarrow\mathbb B_j
\]

with one fixed reference Banach space.

This is impossible as stated. A nonzero trace summand on one side of a birth cannot be uniformly isomorphic to the zero space on the other side. If the reference space retains the coordinate, the map from the zero summand is not onto; if it deletes the coordinate, the map from the nonzero summand is not injective. One needs a larger ambient distribution space in which vanishing geometric components are represented by coefficients tending to zero, or non-invertible embeddings plus a bundle/field-of-spaces formalism. The asserted Banach-bundle theorem cannot follow from the definitions given.

### 2. Second parameter derivatives require more singular trace orders than are provided

Moving a discontinuity once creates a delta-type boundary current. Differentiating it again creates derivatives of boundary distributions and derivatives of incidence maps. The candidate includes only order-zero and order-one oriented traces, but claims `C^2` dependence of the complete operator and Riesz projector across all-depth tangencies and intersections. No calculation shows that this trace tower is closed under two parameter derivatives.

The estimates involving `C0`, `C1`, and the depth weight control combinatorial counts; they do not by themselves define the current-to-current blocks, intersection inclusion–exclusion maps, or their second derivatives. This is the principal new theorem of the paper and remains a programme.

### 3. The Dolgopyat theorem is still assumed inside its proof

The proposed proof says that a fixed fraction of every standard family reaches one common UNI magnet in `O(log |t|)` iterates and can then be paired with a uniform cutoff loss. For a dispersing billiard with moving singularities, proving exactly this statement requires:

- construction of invariant Dolgopyat cones on the quotient and current blocks;
- a non-concentration estimate near cutoff boundaries;
- control of one-sided trace pairing through singular descendants;
- distortion estimates for the paired branches;
- recovery of proper standard families after cancellation; and
- a complete iteration argument in the frequency-adapted norm.

The packet names these steps but does not prove them. The one displayed `L^2` contraction does not imply the announced strong-to-weak operator estimate without those missing estimates.

### 4. The “uniform three-regime” theorem is too broad even after fixing the wide-window formula

The Gaussian interval bracket is the correct form across local, central, and wide windows. However the theorem assumes only `b_n=o(n)`. It does not require `b_n` to diverge, remain above a smoothing scale, or even avoid exponentially small windows. A multiplicative `1+o(1)` cannot be uniform when the Gaussian bracket itself can be arbitrarily small: an absolute Fourier/smoothing error of `o(n^{-1})` is not a relative error for a window whose mass is much smaller than one.

The proof’s choice of a smoothing width through a sequence `gamma_n` is regime dependent and does not supply one uniform estimate over the theorem’s full class. A valid statement must specify, separately, the local interval scale, the central Gaussian scale, and the wide-window regime, including the allowed centre displacement and a lower bound on the interval mass when a relative asymptotic is claimed.

### 5. Covariance positivity is reduced to an unproved Livšic assertion

The packet says that zero variance gives a quotient coboundary and then evaluates two special return words. For billiards on an anisotropic all-depth space, the implication from zero asymptotic variance to a Hölder coboundary with compatible one-sided traces is a theorem requiring proof. It is not a formal consequence of the spectral gap, especially on the newly introduced trace-current completion.

### 6. Higher-block and central-insertion uniformity remains unproved

The local-limit theorem is later used with central path cylinders and for conditioned path laws. The packet does not construct the corresponding higher-block extensions on the augmented bundle or prove uniform projector estimates with insertions. A scalar twisted spectrum does not automatically give total-variation convergence of every fixed window.

## Genuine improvement

The candidate correctly fixes the sign convention for the roof twist and replaces the false wide-window factor by a conditional Gaussian interval mass. It also attempts to confront moving singularities and temporal non-integrability directly. These are the right problems. They are not solved at top-journal proof level in the present text.

## Required reconstruction

The authors must first choose a mathematically coherent field of anisotropic/trace spaces across singularity births, prove the complete operator and parameter estimates, and then give a genuine Dolgopyat argument. The LLT should be stated in explicitly separated regimes with relative-error hypotheses appropriate to each window scale.

## Recommendation

**Reject.** The active manuscript still contains a false local-limit theorem. The unmaterialized candidate corrects that elementary formula but introduces an inconsistent Banach-bundle construction and leaves the load-bearing billiard/Dolgopyat analysis unproved.