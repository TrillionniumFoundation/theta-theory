# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `15cd43f9eef326010c4a1db068be5652aa8b145a`

## Overall assessment

The revision addresses several objections from the preceding circulation. The clock sign is now typed consistently with the twist `exp(<xi,kappa>-s tau)`, moving singularities are represented by an augmented current component, and the authors attempt an explicit temporal-UNI/Dolgopyat argument rather than citing a black-box roof packet.

These are meaningful changes. The main local-limit theorem is nevertheless false on its stated window range, and the proofs of the moving-cut bundle and high-frequency estimate remain outlines rather than complete billiard estimates. Since the pressure-root and conditioning theorems depend on that local-limit theorem, the central claims are not established.

## Decisive error: the roof-window asymptotic cannot hold for all `b_n=o(n)`

The theorem assumes

\[
b_n\to\infty,\qquad b_n=o(n),
\]

and claims

\[
\mathbb P\{S_n\kappa=k_n,\ S_n\tau\in[t_n-b_n,t_n+b_n]\}
\sim
 e^{-nI}\frac{2b_n}{(2\pi n)^{3/2}\sqrt{\det\Sigma}}.
\]

This is incompatible with the central-limit scale when `b_n` is much larger than `sqrt(n)`. Take, for example,

\[
b_n=n^{3/4}.
\]

The centered roof interval then contains asymptotically all of the one-dimensional Gaussian roof mass. Conditional on a central two-dimensional lattice displacement, the joint probability is therefore of order

\[
n^{-1},
\]

not

\[
b_n n^{-3/2}=n^{-3/4}.
\]

The proposed right-hand side would eventually exceed the correct conditional roof mass by a factor of order `n^{1/4}`. This is not a missing error term; it is the wrong leading regime.

A local interval asymptotic proportional to `2b_n` can hold only in a genuinely local regime such as

\[
b_n=o(\sqrt n),
\]

with additional uniform smoothing estimates. For windows comparable with or larger than `sqrt(n)`, the Gaussian interval probability itself must appear in the leading term.

The proof also states that fixed-width boundary smoothing has relative error `O(b_n^{-1})` and that saddle variation costs `O(b_n/n)`. Even in the local regime the variation of a Gaussian density across the interval is naturally controlled by quantities such as `b_n^2/n` (and by the location of the center), not uniformly by `b_n/n` as written.

This error invalidates the stated local-limit theorem, its ratio corollary, and the final current-clock conditioning theorem.

## Further major objections

### 1. The all-depth moving-cut Banach bundle is not constructed

The manuscript introduces one current coordinate for every iterated singularity component and asserts that births, deaths, tangencies, and intersections are absorbed by an absolutely summable boundary-current series. The proof does not establish the required facts:

- local finiteness and compatibility of the all-depth incidence structure;
- a complete definition of the current-to-density and density-to-current blocks of the transfer operator;
- boundedness of branch multiplication by the vector/roof weight on the augmented current space;
- invariance of the physical embedded subspace under the chart changes;
- compatibility of one-sided traces at multiple intersections; or
- differentiability of the Riesz projector in the moving parameter after infinitely many cuts.

The inequality involving `eta^{d(V)-d(W)}` is asserted from the ordinary growth lemma, but no derivation is supplied for the trace-current multiplicities and intersection terms. This is the principal new functional-analytic theorem of the paper and cannot be compressed into a paragraph.

There is also a typing inconsistency: the multiplier lemma is stated on `B_R` and `B_{R,w}`, while the spectral theorem is claimed on the augmented spaces `mathbb B_R`. The action of multiplication on the current component is not defined.

### 2. The temporal-UNI geometry is not verified at the level claimed

The two triangular words are plausible candidates, but the proof does not fully establish that they define inverse branches of one common induced stable quotient over a radius-independent base. In particular, the manuscript must verify:

- the complete regularity of both polygon words for every radius in the interval;
- the existence of the common connector without creating additional singular intersections;
- uniform non-grazing bounds for every internal collision;
- the relation between the endpoint generating-function derivative and the induced roof after stable holonomy; and
- the claimed `3/4` derivative bound after elimination of all internal variables.

The displayed internal Hessian is simply declared positive from dispersing curvature. The polygonal length functional may have sign conventions and endpoint constraints which require an explicit matrix calculation; positivity of each boundary curvature alone does not prove the asserted two-by-two lower bound.

### 3. The Dolgopyat estimate is a proof programme, not a proof

The “uniform return and cancellation block” assumes that a fixed positive fraction of every standard family reaches one common UNI interval in `O(log |t|)` iterates and can be paired with bounded distortion. Establishing this for a billiard quotient with moving singularities is precisely the difficult Dolgopyat theorem.

The manuscript does not construct the Dolgopyat operators, cutoff functions, cone invariance, non-concentration estimate, or iteration scheme in the augmented norm. It also does not show that the quotient high-frequency contraction intertwines with the full anisotropic collision operator, especially on the newly added current coordinates.

The final estimate

\[
C(1+|t|)^A\exp\{-cn/\log(2+|t|)\}
\]

is therefore unsupported.

### 4. Aperiodicity in the displacement coordinate is asserted from unnamed “open branches”

The proof says that four open branches with displacements `±e_1,±e_2` force the lattice frequency to vanish. Those branches, their common domains, and their periodic/return words are not constructed. For an induced quotient, displacement sums also include the connector and return word. A full-span arithmetic theorem must be proved for the actual induced cocycle, not inferred from possible one-flight directions in the billiard.

### 5. The covariance/Livšic argument is incomplete

Zero asymptotic variance implies a coboundary only under a precise spectral/cohomological theorem on the chosen function space. The proof invokes a Gordin decomposition and matching current traces without establishing either. Periodic-word tests then use the same unproved UNI and displacement branches.

Thus the uniform positive-definiteness of the full three-dimensional covariance remains open.

### 6. The physical pressure-root conclusions are downstream of the invalid LLT packet

Formal differentiation of a simple pressure root gives the stated mean and Schur-complement covariance formulas. Strict positivity, local invertibility, and quantitative two-sided conditioning, however, rely on the unproved covariance and local-limit theorems. The final closure theorem therefore does not follow.

## What would constitute a serious paper

A potentially significant submission could focus on one result only: a genuinely complete, radius-uniform vector-displacement/roof spectral and local-limit theorem for this Lorentz family. It would need:

1. a fully defined parameter bundle of anisotropic spaces;
2. uniform Lasota--Yorke and multiplier estimates;
3. an explicit induced temporal-UNI construction;
4. a complete Dolgopyat argument;
5. correct separate local, central, and wide-window LLT regimes; and
6. a ratio theorem with a precisely stated window range.

The projective-pressure and endogenous-field interpretation should be secondary corollaries.

## Recommendation

**Reject.** The round-four revision identifies the correct analytic target but does not prove it, and its headline local-limit formula is directly false for part of the stated `b_n=o(n)` regime.