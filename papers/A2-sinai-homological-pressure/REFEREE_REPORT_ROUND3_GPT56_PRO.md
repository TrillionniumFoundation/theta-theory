# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `2ba786f07bcca1d5d806e6ecfddd9d7596a37930`

## Executive assessment

The revision correctly recognizes that the vector-displacement/roof spectral theorem, temporal aperiodicity, and submacroscopic current-clock ratio theorem are the real mathematical core. It no longer labels them as an imported packet; it attempts to supply a moving-cut Banach bundle, an explicit temporal-UNI construction, a high-frequency cancellation theorem, and a three-variable local limit argument.

This is the right reconstruction target. It is not a proof. Several decisive steps remain unsupported, and one sign convention in the local-limit theorem is wrong. More seriously, the repository’s own hostile audit identified the geometry and temporal-UNI arguments in the controlling module as defective and produced replacement files under `revision/round3-rereview/`; those replacements were never incorporated into the paper’s active `ROUND3_POSITIVE_CLOSURE.tex`. The publication candidate therefore still contains the text that the internal audit rejected.

A fully proved, parameter-uniform vector/roof spectral and local-limit theorem for this Lorentz family could be a significant paper. The present 400-line closure module compresses multiple research papers’ worth of billiard analysis into assertions and sketches.

## Improvements relative to the preceding circulation

1. The manuscript now attempts a common radius-dependent functional-analytic framework rather than merely citing one.
2. It separates low, intermediate, and high temporal frequencies and acknowledges that roof nonlattice control is indispensable.
3. It states a joint lattice/nonlattice local limit theorem rather than claiming that an LDP alone supplies a ratio estimate.
4. The pressure-root Hessian is correctly described as the Schur complement of the joint vector-clock covariance.

These are substantial conceptual improvements. They do not close the model-specific estimates.

## Major mathematical objections

### 1. The controlling geometry proof is incomplete and is not the internally proposed repair

The active module says that an unbounded free line reduces to one of “the three primitive corridor strips” and infers a uniform upper flight bound from the single margin

\[
2(9/20)-\sqrt3/2>0.
\]

A periodic corridor direction is indexed by an arbitrary primitive lattice vector. The required proof must use the row-spacing formula

\[
d_\perp(v)=\frac{\operatorname{area}(\Lambda)}{|v|}
\]

for every primitive direction, together with a compactness argument for irrational directions. The repository contains precisely such a replacement in `revision/round3-rereview/A2_UNIFORM_GEOMETRY.tex`, but `main.tex` does not input that file.

The same problem occurs in the expansion estimate. The controlling proof says that the one-step inverse-expansion sum is strictly below one for each table and then invokes continuity in the radius. For dispersing billiards with moving singularities, the stable statement is generally a finite-iterate growth estimate after a chartwise continuation of the singularity structure. The internal replacement changes the theorem accordingly, but the active manuscript retains the unproved one-step assertion.

### 2. The moving-cut atlas does not construct the anisotropic spaces required by the theorem

The atlas proof follows depth-one singular curves through finitely many tangencies and says that cutting at their endpoints makes the incidence pattern constant. The anisotropic norm and Lasota–Yorke estimates depend on all iterated singularity preimages, homogeneity strips, complexity growth, and holonomy regularity. A finite continuation of depth-one graphs does not establish:

- uniform admissible stable-curve families under arbitrary iteration;
- uniform complexity bounds for the iterated partitions;
- compact embedding of the strong ball into the weak space;
- differentiability in the radius of the transfer operator including moving-boundary terms; or
- compatibility of chart transition maps with the completed distributions.

The theorem that the resolvent, Riesz projector, and pressure are continuously differentiable in `R` is therefore asserted rather than derived.

### 3. The temporal-UNI construction in the controlling paper is not defined rigorously

The active text introduces inverse branches `h_R^+`, `h_R^-`, and `h_R^0` on a small interval and writes an infinite temporal-distance series, but it does not construct the induced quotient on which those are inverse branches, identify the collision points, solve the specular critical equations, or compute the endpoint derivative.

The proof’s estimate “the first unequal legs dominate the later paired legs” is not justified by the displayed geometry. The repository’s separate `A2_TEMPORAL_PACKET.tex` attempts to repair this by introducing a finite-connector Young magnet and polygonal generating functions. Again, that file is not part of the controlling manuscript.

Thus the principal nonintegrability lemma used for every high-frequency conclusion remains unproved in the submitted source.

### 4. The Dolgopyat/high-frequency estimate is a research theorem, not a paragraph

From a lower bound on one temporal-distance derivative, the manuscript jumps to

\[
\|\mathcal L_{R,iu,it}^n\|
\le C|t|^A\exp\{-cn/\log(2+|t|)\}.
\]

A proof requires adapted norms depending on the frequency, a standard-family decomposition, recurrence to the UNI set, control of branch pairing and phase derivatives, cancellation surviving the billiard singularities, and strong-to-weak iteration estimates. The phrases “pair the branches,” “one weight loses a fixed fraction,” and “the growth lemma returns a fixed fraction” do not supply these ingredients or track constants uniformly in `R` and the lattice frequency `u`.

The compact-annulus argument also assumes upper semicontinuity of the relevant spectral radius on a moving family of anisotropic spaces, which has not been proved.

### 5. The local-limit theorem has a clock-sign inconsistency

The twist is

\[
\exp\{\langle\xi,\kappa\rangle-s\tau\}.
\]

Therefore

\[
(\text{mean displacement},\text{mean roof})
=(\partial_\xi P,-\partial_sP),
\]

not `∇P=(a,b)` with `b` subsequently used as the positive mean of `T_n`. The repository’s internal audit explicitly noticed this sign. The active local-limit theorem and its proof do not correct it.

This is not merely notation: it affects the real saddle, the rate exponent, and the Gaussian covariance coordinates.

### 6. The submacroscopic interval analysis is not demonstrated

The theorem covers `b_n → ∞`, `b_n=o(n)`, including `b_n=o(sqrt n)`, and claims that smooth approximations of the roof indicator have Fourier error

\[
o(b_n n^{-3/2}).
\]

That conclusion does not follow from `b_n→∞` alone. One must choose upper and lower smoothings, quantify their boundary error under the tilted law, control their Fourier transforms on all three frequency regions, and prove that the smoothing scale is compatible with the high-frequency decay. None of these estimates appears.

The advertised quantitative conditional error

\[
O(n^{-1/2}+b_n/n+b_n^{-1})
\]

is likewise not derived from the asymptotic formula stated in the preceding theorem.

### 7. Covariance nondegeneracy uses an unstated Livšic theorem

The proof says that zero asymptotic variance makes `u·kappa-t tau` a measurable coboundary and that periodic-orbit identities plus aperiodicity force `(u,t)=0`. For a singular billiard map on anisotropic spaces, both implications require precise regularity and a Livšic/coboundary theorem. Neither is stated or proved. The peripheral-spectrum argument at imaginary frequency does not automatically establish strict positivity of the real covariance in the function class used.

### 8. The controlling paper is not standalone

The active `main.tex` contains only a preamble, abstract, and an input of the closure module. The module relies on previously defined `T_R`, `L_R`, `kappa_R`, `tau_R`, `mu_R`, lattice vectors, and coordinate conventions that are absent from the active paper. Compilation is not a substitute for mathematical definitions.

## Repository-materialization defect

The branch contains two explicit rereview replacements:

```text
revision/round3-rereview/A2_UNIFORM_GEOMETRY.tex
revision/round3-rereview/A2_TEMPORAL_PACKET.tex
```

They were written because the internal hostile audit rejected the corresponding active arguments. Neither is included by `papers/A2-sinai-homological-pressure/main.tex`. A publication gate cannot be based on proof files that are not part of the controlling manuscript.

## Editorial recommendation

**Reject.** The revision has identified a potentially important theorem, but has not proved it. A credible resubmission should be narrowed to the parameter-uniform vector/roof spectral and joint local-limit theorem, incorporate the corrected geometry and quotient-UNI constructions into the actual paper, provide the full anisotropic and high-frequency estimates, and derive the submacroscopic ratio theorem with explicit smoothing bounds. Only after that theorem exists should the pressure-root and conditioning consequences be presented.