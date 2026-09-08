# Response to Referee Round Twenty-Two

**Referee source:** `REFEREE_REPORT_ROUND22_GPT56_PRO_HARSH.md`  
**Inherited source branch:** `revision/round21-referee-positive-closure-11paper-2026-09-02`  
**Positive reconstruction branch:** `revision/round23-referee-positive-closure-11paper-2026-09-02`  
**Policy:** preserve the advertised positive programme; replace every refuted definition, state space, normalization, or inference by a typed construction with an active proof and a regression check.

We thank the referee for giving explicit counterexamples rather than only requesting more detail.  The Round-Twenty-Three revision treats those counterexamples as design constraints.  It does not defend the refuted mechanisms, does not convert them into no-go results, and does not obtain closure by changing status words.  Each active `main.tex` now imports a new `ROUND23_POSITIVE_CLOSURE.tex`; the Round-Twenty-One sources and the full Round-Twenty-Two report remain in the repository as provenance.

## Executive correction map

| Paper | Decisive Round-Twenty-Two defect | Round-Twenty-Three positive replacement | Active labels |
|---|---|---|---|
| A1 | Hilbert membership was used as if it supplied exponential cylinder approximation; the random current and covariance were not typed | Separate current fibre, strongly measurable current observable, and response Banach domain with an explicit conditional-expectation tail; Bochner mean; verified projective martingale approximation and trace identity | `def:r23-a1-domain`, `thm:r23-a1-response`, `thm:r23-a1-fclt` |
| A2 | Real linear independence did not prove lattice aperiodicity; two returned orbit points were not independent integration variables | Periodic-data closed subgroup certificate using exact integer generators, two incommensurable roof differences, and coprime periods; two integrations in the original collision coordinates `(r,phi)` | `lem:r23-a2-arithmetic`, `thm:r23-a2-fourier`, `thm:r23-a2-llt` |
| A3 | Unordered empirical transitions did not determine the physical path; representative atoms had infinite KL; long one-excursion controls broke return-count compactness | Chronological marked point measure carrying complete excursions and terminal truncation; conditional-reference cell recovery; recession coordinate for order-`N` excursions; finite-memory source-inserted conditioning | `prop:r23-a3-order`, `lem:r23-a3-recovery`, `thm:r23-a3-ldp`, `cor:r23-a3-conditioned` |
| A4 | A Lyapunov sublevel was incorrectly truncated; a residue of a holomorphic full resolvent was adjoined; the memory transform was incorrectly claimed to be `O(z^-2)` | Separate Lyapunov, stable-influence, and bounded-metric scales; typed renewal maps; exact Schur--Feshbach/Mori--Zwanzig kernel `PLQ exp(tQLQ) QLP` with generic `z^-1 PLQLP`; genuine poles only | `lem:r23-a4-small`, `prop:r23-a4-renewal`, `thm:r23-a4-memory` |
| B1 | The unnormalised `1/N!` pressure contained `-log N`; block selection was not predictably typed; mixed Gaussian cross-covariance was omitted | Probability-normalised canonical MGF or explicit ideal-gas renormalisation; deterministic labelled blocks and adapted boundary-flat atlases; full joint covariance, conditional shift, and Schur complement | `prop:r23-b1-normalization`, `lem:r23-b1-block`, `thm:r23-b1-llt`, `thm:r23-b1-extraction` |
| B2 | Moments did not imply a grazing trace bound; singular geometry was not exhausted; no extra small factor was obtained on regular surplus contacts; reduced-state slice concatenation lost collision histories | `L^p(A_f)` regular trace class plus finite-entropy approximation; determinant-ideal sublevel estimate; transverse loop-opening factor `epsilon^alpha`; factorial hierarchy of complete collision histories with open half-edges; exact tilt concentration | `lem:r23-b2-loop`, `thm:r23-b2-gc-pressure`, `thm:r23-b2-gc-ldp`, `thm:r23-b2-mc` |
| B3 | Compact positivity did not give a global collision gap; deterministic-time cumulants did not imply stopping-time tightness; the action Hessian charged the zero-cost manifold | Global Maxwellian comparison; full-state restart and conditional history-cumulant bound; normal collision defect `h=delta Gamma-D A_f[u]`; Hessian `1/2 integral h^2/A_f` | `lem:r23-b3-gap`, `thm:r23-b3-range`, `thm:r23-b3-clt`, `thm:r23-b3-mosco` |
| B4 | A second-moment shell was not compact in a quadratic-growth topology; transfer began in a weaker metric; product collision continuity and comparison were missing | Propagated `(2+delta)` moment, `W_2` state topology, compact action sublevels, direct synchronous transfer, product collision convergence, explicit core/containment/comparison and BBGKY correctors | `lem:r23-b4-compact`, `prop:r23-b4-product`, `thm:r23-b4-resolvent`, `thm:r23-b4-limit` |
| C1 | An uncountable deterministic Dirac family cannot share a dominating state probability; aggregate local limits did not automatically give conditional densities; small evidence and policy-uniform information were unsupported | Deterministic push-forward prediction with no hidden-state density; domination only of observation strata; hidden-history-inserted density theorem; integrated numerator identity; convex belief reconstruction; explicit persistent excitation and identifiability | `prop:r23-c1-observation`, `thm:r23-c1-filter`, `prop:r23-c1-finite`, `thm:r23-c1-bvm` |
| C2 | The weighted strict topology/dual proof was invalid; the hard-sphere adjoint omitted the collision term; pressure derivatives did not directly yield periodic sums; weak convergence did not yield optional projections/brackets; a likelihood hitting zero cannot be a finite Brownian exponential | Pull back the standard strict topology through division by the weight; full adjoint `-partial_t-v.grad-L_f^*`; equilibrium localisation followed by Livsic; prediction-process convergence plus UT characteristics; strict positive equivalent likelihoods | `thm:r23-c2-dual`, `thm:r23-c2-annihilator`, `lem:r23-c2-periodic`, `thm:r23-c2-optional` |
| D1 | An LDP does not determine polynomial phase weights; phase-cell conditioning and noncompact separation were not proved; phasewise optimisation revealed the latent phase | Source-inserted local coefficient plus Morse--Bott expansion; rate-continuity tubular cells and exponential-tightness separation; complete phase-posterior state with one shared policy; dominance-qualified complex charts; phase-centred Gaussian mixtures | `lem:r23-d1-separation`, `thm:r23-d1-weights`, `thm:r23-d1-control`, `thm:r23-d1-gaussian` |

## Direct responses to the eight explicit counterexamples

### 1. A4 regular-point residue

The former transmission augmentation is deleted from the active proof.  The revised source observes that the residue of `(z-L)^{-1}` at a regular point is zero and never uses it as a generalized vector.  Actual singularities are treated only through genuine Riesz projections.  The reduced resolvent is related to the full generator by the closed-domain Schur--Feshbach identity in `thm:r23-a4-memory`.

### 2. A4 high-frequency memory asymptotic

The revised transform is

`Khat(z)=PLQ(z-QLQ)^(-1)QLP`

and its expansion begins with

`z^(-1) PLQLP + z^(-2) PLQ(QLQ)QLP + ...`.

Exponential decay is proved from the orthogonal semigroup estimate.  When an absolutely integrable vertical remainder is useful, the explicit leading pole `PLQLP/(z+omega)` is inverted separately.  No algebraic cancellation of the generic `z^-1` coefficient is asserted.

### 3. B1 factorial normalization

The canonical source functional is a moment generating function under a probability measure and equals one at zero source.  Its pressure is therefore exactly zero at the origin for every `N`.  Absolute free energy, when used, displays the `N!`/volume ideal-gas correction explicitly.  Exact-number extraction uses coefficient ratios, so the same factorial convention appears in numerator and denominator.

### 4. B3 zero-cost tangent

At a zero-cost path `Gamma=A_f`, the revised normal coordinate is

`h=delta Gamma-D A_f[u]`.

The collision quadratic form is `1/2 integral h^2/A_f`.  Therefore `delta Gamma=D A_f[u]` has zero collision cost.  The general direct second derivative of `A ell(q)` is also recorded before chart corrections, so the referee's scalar test is reproduced rather than bypassed.

### 5. C1 deterministic Dirac domination

The hidden transition remains the Dirac push-forward `delta_{Phi_theta^a(x)}` and is never assigned a density.  Only the observation kernel is dominated.  Belief prediction is a push-forward, after which Bayes multiplication uses the observation density.  This type separation removes the impossible common-state domination premise while retaining a positive Feller filtering theorem.

### 6. A3 loss of temporal order

Every excursion mark contains the full physical trajectory, and every atom of the empirical object carries its scaled chronological start coordinate.  The path is obtained by ordering those atoms and concatenating their marks.  Two Eulerian orderings with the same unordered transition counts remain distinct states.

### 7. A3 atomic recovery

The recovered control on a partition cell is the reference kernel conditioned on that cell, multiplied by the desired cell probability.  It is absolutely continuous and its relative entropy is exactly the coarse-grained KL, bounded by the original KL by data processing.  No representative Dirac mass is introduced into a non-atomic kernel.

### 8. B4 escaping quadratic energy

The invariant shell now has a uniform `(2+delta)` velocity moment and uses `W_2`.  The referee's sequence with mass `n^-2` at velocity `n` has `(2+delta)` moment of order `n^delta` and therefore exits every fixed shell.  Uniform integrability of the second moment then upgrades narrow compactness to `W_2` compactness and permits passage to the product collision measure.

## Cross-paper proof order

The active noncircular order is

```text
A1
A2 -> A3 -> A4
B2-GC -> B1 -> B2-MC -> B3 -> B4
(A2,A3,A4,B1,B2-GC,B2-MC,B3,B4) -> C1
(A3,A4,B3,B4,C1) -> C2
(A1,A2,A3,A4,B1,B2-GC,B2-MC,B3,B4,C1,C2) -> D1
```

B2's grand-canonical history pressure and LDP are proved before exact-number extraction.  B1 then returns a local coefficient to B2-MC.  B3 constructs the Gaussian process before identifying the second epi-derivative.  B4 derives comparison independently of the nonlinear graph limit.  C1 derives conditional observation kernels with the hidden history retained.  C2 imports the corrected C1 prediction process.  D1 uses upstream local coefficients, not only their exponential contractions.

## New mathematical tools introduced in Round Twenty-Three

1. **Measurable current response domain:** an explicit Bochner/projective norm separates geometric current regularity from stochastic approximation regularity.
2. **Periodic annihilator certificate:** exact lattice generators, irrational roof differences, and coprime periods prove triviality of the full periodic character.
3. **Chronological excursion measure:** order, complete path marks, terminal truncation, and recession mass coexist in one stopped state.
4. **Conditional-reference entropy quantisation:** finite-state recovery without singular atoms and with exact coarse KL.
5. **Two-scale history compactification:** remote mark size and remote influence are controlled by different geometric weights.
6. **Exact Schur--Feshbach memory calculus:** time-domain decay, high-frequency expansion, and reduced resolvents share one closed-domain block identity.
7. **Transverse loop opening:** each independent surplus collision contributes an additional geometric small factor after tree coarea reduction.
8. **Open-half-edge history composition:** finite-time hard-sphere propagation retains exactly the correlations crossing a time slice.
9. **Defect-coordinate kinetic Hessian:** second variation is normal to the zero-cost collision manifold.
10. **Superquadratic Wasserstein shell:** energy compactness and nonlinear product continuity use the same topology.
11. **Integrated-evidence filtering:** zero evidence and infinite observation reference measure are controlled without pointwise Bayes continuity.
12. **Equilibrium localisation bridge:** pressure identities are converted to periodic identities by a separate zero-temperature theorem before Livsic.
13. **Prediction-process convergence interface:** optional projections, innovations, and brackets are transported under explicit extended convergence.
14. **Morse--Bott phase coefficient calculus:** all polynomial, determinant, lattice, saddle, and conditioning factors enter phase coexistence weights.

## Verification and scope

`tools/verify_round23.py` checks active-source identity, theorem/proof balance, citation closure, the declared dependency DAG, and executable algebraic regressions for the referee's counterexamples.  The Round-Twenty-Three workflow clean-builds all eleven manuscripts and records source/PDF hashes.  These are fail-closed reproducibility checks.  They do not replace independent mathematical review, but every objection in the Round-Twenty-Two report now has an explicit active construction, proof location, and regression target rather than a status assertion.
