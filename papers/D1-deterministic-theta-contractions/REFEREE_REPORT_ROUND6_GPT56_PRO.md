# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `954c497ce7c462ce9b1f06b9d8b1ceb43b267a5e`

## Editorial summary

The finite likelihood is now algebraically centered at the exact finite-volume mean, which corrects the previous non-mean-one density. The use of a projective system is also a cleaner abstract route than assuming density of exposed points.

The new global theorem is nevertheless vacuous for the platforms to which it is applied. Hypothesis (P1) asks for a global holomorphic logarithmic moment generating function on all of complex space, which even elementary Bernoulli laws do not possess because their complex mgfs have zeros. Hypothesis (P2) asks the gradient to diverge at infinity, which is impossible for bounded cylinder observables because tilted means remain in a bounded convex hull. A3 additionally permits phase coexistence, contradicting global differentiability. Thus no Sinai or hard-sphere projective source system in the series satisfies the stated hypotheses. The remaining conclusions are standard abstract consequences once those impossible assumptions and upstream theorems are granted, so D1 has no independent top-four contribution.

## Major mathematical objections

### 1. Hypothesis (P1) is impossible even for elementary finite variables

The paper assumes, for every projection,

\[
Q_{\varepsilon,m}\to Q_m
\quad\text{locally uniformly on }\mathbb C^{d_m},
\]

where

\[
Q_{\varepsilon,m}(z)=
\mu_\varepsilon^{-1}
\log E e^{\mu_\varepsilon z\cdot\pi_m(X_\varepsilon)}.
\]

A complex logarithm can be holomorphic on a domain only where the mgf is nonzero and a branch is fixed. Complex mgfs generally have zeros. For a Bernoulli variable with probabilities `p` and `1-p`,

\[
M(z)=1-p+pe^z
\]

vanishes at infinitely many complex points. Hence no single-valued holomorphic `log M` exists on all of `C`.

Scaling by `mu_epsilon` merely moves the zero set. The same issue occurs for finite-state cylinders of every platform. One may obtain analytic pressure on a zero-free neighborhood of each compact real source set after spectral separation; one cannot assume a global logarithm on all `C^{d_m}`.

Therefore the normal-family/Cauchy argument in `prop:r6-d1-normalization` cannot be based on (P1) as stated, and the assertion that A2 or B2 supplies this hypothesis is false. Those papers claim only local complex neighborhoods of bounded real charts.

### 2. Hypothesis (P2) is impossible for bounded cylinder projections

For a bounded finite-dimensional observable `Y=pi_m(X)`,

\[
\nabla Q_m(\theta)=E_\theta Y
\]

lies in the closed convex hull of the bounded support of `Y`. Its norm remains bounded for all real `theta`. It cannot satisfy

\[
|\nabla Q_m(\theta_n)|\to\infty
\quad\text{as }|\theta_n|\to\infty
\]

in any nonannihilated direction.

The projective systems used for path LDPs are explicitly built from bounded cylinder tests. Thus the paper's steepness condition excludes the very projections it later invokes. Standard essential smoothness for a pressure finite on all of `R^d` does not require gradient blow-up at infinity; the boundary of the effective domain is empty. The manuscript has replaced the correct Gärtner–Ellis hypothesis by a stronger, model-incompatible one.

### 3. Global differentiability is contradicted by the series' own phase-coexistence claims

A3 states that direct pressure can be the maximum of recurrent, survivor, and recession branches and that maximizing phase sets may contain several components. A maximum of distinct analytic pressure branches is generally nondifferentiable at coexistence.

D1 nevertheless assumes every finite projected pressure is differentiable on all of `R^{d_m}`. Quotienting conservation directions does not remove first-order phase transitions. Therefore the claimed Sinai interface does not satisfy (P2), even apart from the impossible gradient condition.

The hard-sphere source sewing theorem likewise gives local differentiability on regular bounded charts, not global differentiability for every source amplitude and projection.

### 4. The finite-dimensional Gärtner–Ellis conclusion is misstated

The proof says that finiteness, differentiability, and the paper's steepness condition give a full LDP at every point. The actual Gärtner–Ellis lower bound depends on lower semicontinuity, essential smoothness, and exposed points of the Legendre transform; different formulations require different domain assumptions. The manuscript neither states the standard theorem accurately nor treats support boundaries and nonexposed points.

If `Q_m` is finite and differentiable on all real space, essential smoothness at finite boundary is vacuous, but bounded-support rates can still have boundary points requiring an approximation argument. The invented infinity-gradient condition does not supply that argument because it fails in the bounded case. A correct finite-dimensional theorem must be stated and verified projection by projection.

### 5. The topology assumptions are insufficiently tied to a projective limit

The maps `pi_m` are said to separate points and generate the topology on compact sets. Dawson–Gärtner applies naturally to a projective-limit space with the initial projective topology. The proof first obtains an LDP in an unnamed “initial projective topology” and then says exponential tightness in `E` upgrades it to the full topology.

Such an upgrade requires the identity map between the two topologies to satisfy a precise inverse-contraction or exponentially-good compactness condition. Generating the topology only on compact sets can be enough with a careful exponential-tightness lemma, but that lemma is neither stated nor proved. Since the platform state spaces include weighted measures, defects, and path topologies, this is not a harmless abstraction.

### 6. None of the platform inputs establishes (P1)–(P4)

The paper says:

- A2 supplies global finite-cylinder twisted pressures;
- A3 supplies exponential tightness;
- B2 supplies every bounded real source;
- B3 supplies strict differentiability.

The individual reports show otherwise. A2's ambient spectrum and aperiodicity are unproved; A3's recession LDP and goodness are unproved; B2's cyclic estimate and lower bound fail; B3's covariance/differentiability theorem is formal. More narrowly, even the claims made in those papers are local in source and allow coexistence. They do not imply the global entire/differentiable/steep assumptions written here.

D1 is therefore a conditional abstract theorem with no verified model satisfying its hypotheses.

### 7. The conditioning theorem assumes nearly the whole result

The “B1-type exact coefficient property” is assumed for every bounded cylinder source and every constraint considered. It includes:

- existence of a source-dependent exact finite saddle;
- a uniform shell coefficient of subexponential cost; and
- positive constraint Hessian.

For hard spheres this is precisely the unproved B1 theorem. For Sinai or a generic projective constraint no such coefficient theorem exists. Once this property is assumed, the pressure infimum is a standard exponential-tilting calculation; D1 contributes no new microscopic argument.

### 8. Restricting an unconditioned rate to a constraint surface is not an alternative proof of a conditional LDP

The proof says that the conditional rate “alternatively” follows by restricting the good unconditioned rate to `Cx=a`. This is not true in general. Conditioning on shrinking neighborhoods or thin exact shells requires the denominator and local probabilities to have the correct exponential asymptotics. A good unconditioned LDP alone gives only upper/lower bounds for fixed neighborhoods and may not determine conditional behavior on a measure-zero surface.

The exact coefficient hypothesis is needed; it cannot be bypassed by the restriction formula. The manuscript's alternative sentence conceals this essential dependence.

### 9. The no-duality-gap claim needs convex linear structure and a constraint qualification

`thm:r6-d1-interchange` starts with jointly continuous “finite coordinate maps” but then uses adjoints and source conjugates, which require linear maps. At the primal rate level the two routes indeed share the same constrained infimum by definition. Equality with the conjugate of `Q^a(T^*eta)` is stronger.

That equality requires convexity and lower semicontinuity of the joint projected rate plus an appropriate relative-interior condition. Goodness and attainment of the primal infimum do not rule out a Fenchel duality gap. The proof asserts that finite differentiable steep pressure supplies the result, but those hypotheses are unavailable and the conditioning envelope can lose steepness at the boundary.

### 10. The exact likelihood theorem is correct only under a local analytic hypothesis, not (P1)

Substituting the finite center does make `L_epsilon(h)` the exact Radon–Nikodym density. This is a valid correction. The Gaussian limit needs only an analytic neighborhood of the fixed real source and convergence of second derivatives; it does not require an entire complex pressure.

The theorem should be retained as a finite-dimensional local lemma with explicit source-domain assumptions. It does not rescue the global projective LDP, and its process versions still depend on the invalid B3/A4 tightness interfaces.

### 11. The dynamic theorem is a standard variational identity, not a new rigidity result

An additive good path action generates a Lax–Oleinik semigroup by splitting and concatenation. A quadratic Gaussian action yields the standard entropic-gradient term. These are familiar convex/dynamic-programming facts. D1 neither proves additivity for the Sinai or hard-sphere microscopic rates nor supplies their missing compactness and tangent theorems.

Once the unavailable upstream inputs and impossible global assumptions are removed, the remaining material is better placed as a short abstract appendix to the papers where the hypotheses might eventually be proved.

## Required reconstruction

A viable revision must:

1. replace global complex analyticity by zero-free local complex charts around real sources;
2. state the correct finite-dimensional Gärtner–Ellis conditions for bounded and unbounded projections separately;
3. allow nondifferentiable coexistence pressures and use an alternative lower-bound method there;
4. prove the topology-upgrade lemma for the actual projective state spaces;
5. verify every hypothesis for at least one platform rather than citing disputed upstream labels;
6. keep the exact likelihood as a local theorem; and
7. move generic contraction/conditioning/dynamic identities into an appendix unless a genuinely new model-level commutation theorem is proved.

## Recommendation

**Reject; remove as a standalone submission.** The exact finite centering is repaired, but the new projective theorem assumes an entire complex log-mgf and infinity-steep gradients that elementary bounded cylinders cannot satisfy. Global differentiability also conflicts with the series' phase coexistence. D1 therefore has no verified model and packages standard consequences of assumptions stronger than the desired results.