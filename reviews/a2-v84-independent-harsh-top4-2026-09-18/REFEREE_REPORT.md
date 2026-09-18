# Independent harsh referee report on A2 revision 84

## 1. Review target and recommendation

Repository: TrillionniumFoundation/theta-theory

Reviewed revision branch: **revision/a2-v84-secant-detector-space-2026-09-18**

Pinned revision commit: **b3da64f38742459620d624ea9a565abb3550aba9**

Principal entry point: **papers/A2-v17-boundary-information-coarsening/rigidity_v84.tex**

Expanded entry point: **papers/A2-v17-boundary-information-coarsening/rigidity_v84_full.tex**

Controlling previous report read in this revision:
**reviews/a2-v83-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md**
(blob f74de36ff17126c6667c0ccecd9310c85e74dde5).

I read the full new v84 principal source, with particular attention to the new detector-space, finite-record, common-lift, and boundary-distance blocks. I also compared the mathematical role of these additions against the objections in the v83 report.

**Recommendation at the Annals / Inventiones / Acta / JAMS level: reject in the present form.**

This recommendation is materially different from a claim that the revision is mathematically unsound. On this source review I do **not** find a short fatal counterexample to the new core theorems. Revision 84 is a substantial and serious improvement. Several major v83 objections are now genuinely closed or substantially narrowed. The remaining problem is the conceptual and editorial scale of the contribution at the requested four-leading-general-journals level.

The strongest new mathematics is now:

1. a quotient-secant / quotient-tangent criterion for regular scalar identification in a finite-dimensional detector function space;
2. finite stable designs on compact action classes and a generic d+5-clock result for analytic spaces;
3. explicit protected-pole, sign-changing-kernel, and action-divisor families;
4. a global description of the q+2 polynomial ambiguity fibre;
5. finite-record recovery of a component covering and monodromy under quantitative sampling, signal, and Lipschitz assumptions;
6. an observable compatibility test for two coprime reconstructed exact lifts on a common invariant domain;
7. a reduction from uncalibrated two-arm projective records to the classical boundary-distance rigidity theorem for simple surfaces.

These are real additions. In my view, however, they still do not produce a theorem whose mathematical depth or breadth is commensurate with the requested journal class.

---

## 2. What v84 genuinely fixes

Revision 84 should receive explicit credit for responding to the previous report at theorem level rather than by cosmetic rewriting.

### 2.1 The detector-space objection is substantially closed

The v83 paper classified a particular sampled codimension-two quotient under a positive-kernel hypothesis. That was too narrow to support the broader detector-space language.

The new Definition 4.1 and Theorem thm:v84-design move to the actual function space. The secant condition

- excludes exact collisions in the quotient C(K_T)/F;

and the tangent condition

- excludes first-order loss of identifiability in the same quotient.

The finite-subcover argument then turns functional regular separation into a finite stable deadline design on every compact action class.

This is a real conceptual improvement.

### 2.2 The positive-kernel restriction is no longer structural to the general theory

Proposition prop:v84-no-positive gives a fixed two-dimensional detector space for which every nonzero sampled annihilator kernel changes sign, yet six clocks identify the scalar model.

This directly answers the v83 criticism that the positive-kernel machinery might be the hidden structural assumption of the theory.

### 2.3 The lower-bound fibre is now global rather than merely local

Theorem thm:v84-fibre parametrizes the full q+2-clock polynomial ambiguity fibre by one scalar parameter through the primitive F of the positive Cauchy product kernel.

This is substantially stronger than the previous implicit-function lower bound. The finite-record two-point risk corollary is also a clean way to convert exact nonidentifiability into an estimation obstruction.

### 2.4 The finite-data / covering objection is substantially closed

Theorem thm:v84-mesh is not just a reference-local continuation theorem. It specifies a finite experiment:

- a triangulated endpoint domain;
- repeated readout pairs at every vertex and clock;
- supplied signal, separation, and Lipschitz margins;
- pointwise compact-class fitting;
- nearest-column edge transport;
- exact face cocycle recovery;
- covering and monodromy reconstruction.

This is much closer to an observable finite-record theorem than anything in v83.

### 2.5 The common-lift premise is partially replaced by an observable exact test

Theorem thm:v84-compatible correctly observes that on one common invariant domain, two exact lifts R and S are powers of a unique common lift with coprime counts r,s exactly when they commute and satisfy R^s=S^r as full exact lifts.

The recursive word-domain definition also repairs the ambiguity surrounding negative Bezout exponents and local domains.

### 2.6 The geometric application is no longer only the engineered shear

The simple-surface application is a genuine pre-existing inverse problem. The detector is no longer tuned to a special integrable shear formula. The theorem explicitly reduces the uncalibrated selective two-arm observation to boundary distance, then invokes the classical simple-surface boundary rigidity theorem.

This is much better than v83 as an application section.

### 2.7 Most of the v83 technical comments are now handled cleanly

The revision explicitly states:

- gauge regularity;
- the ambient off-model affine target;
- the fixed-stratum limitation of the global noisy inverse;
- the dependence of stability constants;
- monodromy compatibility for disconnected coverings;
- recursive word domains;
- the role of absolute primitives;
- covered rather than automatically global suspensions;
- the domain support of the unsampled perturbation;
- the known nature of the exponential shape parameter;
- a broader bibliography.

I would not recycle the v83 technical report against this version.

---

## 3. Major concern: the new “general detector-space theory” is still primarily a regular-embedding criterion, not a structural classification

The paper now says, correctly, that the logarithmic action curve should be studied modulo the detector space F. This is the right invariant language.

But Theorem thm:v84-design has a limitation that matters at the requested journal level.

The two defining conditions of “regularly separating” are essentially:

1. the quotient secant map is injective;
2. its differential is injective.

Once those two properties are assumed, the existence of a finite stable design on a compact parameter class is obtained by compactness of normalized differences and normalized tangents.

That theorem is correct-looking and useful. But as a classification theorem it remains close to the formal statement:

> a compact finite-dimensional regularly embedded nonlinear family can be separated by finitely many evaluation functionals.

### R84-M1. The paper still lacks an intrinsic classification of detector spaces

The conditions are exact, but they are not yet a deep structural characterization of which finite-dimensional detector spaces satisfy them.

For a general F, checking

Gamma(a)-Gamma(a') in F => a=a'

for all action pairs may be essentially as hard as solving the original identification problem.

Likewise, checking that no quotient tangent vanishes is a regularity test, not a classification by an independently recognizable invariant.

The protected-pole family and the sign-changing-kernel example are useful verifiable subclasses, but they do not yet produce a broad detector-space taxonomy.

For a top-four general journal, I would want one of the following:

- a necessary-and-sufficient characterization in terms of a recognized geometric or approximation-theoretic property of F;
- a sharp dimension/sample theorem for a broad natural class;
- a classification of maximal regularly admissible enlargements under natural closure operations;
- a relation to total positivity, extended Chebyshev systems, rational approximation, or variation-diminishing structure that is strong enough to decide admissibility without replaying the full secant equation.

At present the quotient language unifies the scalar part conceptually, but it does not yet classify the detector spaces in a way that feels mathematically inevitable.

---

## 4. Major concern: the d+5 generic analytic theorem is a dimension-counting/unisolvence principle whose novelty is not yet established

Lemma lem:v84-evaluations and Theorem thm:v84-generic are elegant. The incidence argument correctly avoids an illegitimate uncountable union of exceptional clock sets.

The proof mechanism, however, is very general:

- a nonzero real-analytic one-variable function has isolated finite-order zeros;
- an incidence set with N sampled zeros can locally be solved for the N clock variables over a p-dimensional parameter chart;
- if N>p, its projection to clock space has measure zero.

This is essentially a generic-evaluation / unisolvence argument for a finite-dimensional analytic family.

### R84-M2. The paper must establish what is genuinely new about the generic analytic design theorem

The manuscript now cites FRI and Prony literature, but it still does not place Theorem thm:v84-generic against the broader interpolation, unisolvent sampling, transversality, and finite-dimensional nonlinear embedding literature.

The theorem may well be new in this exact quotient-logarithm formulation. That is not the same as the proof principle being new.

The present count d+5 is also explicitly only sufficient and is obtained from the dimension d+4 of the collision family. There is no matching lower bound, no sharpness mechanism for general analytic F, and no theorem showing that d+5 is qualitatively optimal in a nontrivial class.

At a specialist inverse-problems or approximation journal, this can be a useful theorem. At a top-four general journal, the authors need to explain why this is more than a clean application of a generic unisolvence principle to their parameterized family.

---

## 5. Major concern: the explicit detector families are correct-looking but still specialized rational zero-counting

The protected-pole theorem, the no-positive-kernel example, and the action-divisor theorem are the technically strongest evidence that the general quotient criterion is not empty.

I checked the degree counts and residue logic at source level. I do not see an immediate contradiction:

- q+k+5 sampled zeros give q+k+4 derivative zeros, forcing a numerator of degree at most q+k+3 to vanish;
- protected residues recover detector coefficients;
- moving residues recover the ordered action pair;
- the tangent calculation uses double moving poles to force the action derivatives to vanish;
- the sign-changing-kernel example uses zero integral of the Cauchy kernel against the interval to rule out a one-sign annihilator;
- the divisor theorem correctly exposes a common polynomial factor as a projective gauge.

These are good calculations.

### R84-M3. The family of examples still does not amount to one deeper theorem

Each class is controlled by a different elementary mechanism:

- divided differences and two interval moments;
- rational zero counting and residues;
- a sign-change integral;
- gcd/lcm arithmetic of action polynomials.

The paper calls the quotient secant geometry the central invariant, but the strongest concrete results are still proved case by case.

A more compelling theorem would derive these examples from a single robust property of the detector/action curve and predict sharp sampling complexity from that property.

Without that, the manuscript still reads as a powerful collection of solvable structured families rather than the discovery of a general rigidity principle.

---

## 6. Major concern: the finite-record covering theorem is useful but rests on strong supplied margins and an existence estimator

Theorem thm:v84-mesh is a substantial improvement and, in my view, basically the right way to formulate a finite covering-recovery result.

But its statistical and algorithmic content should not be overstated.

The theorem assumes:

- a known triangulation and mesh size;
- repeated observations at every vertex and every clock;
- a known signal lower bound sigma_*;
- a known channel signature gap s_*;
- known Lipschitz bounds L_U and L_Xi along all local lifts;
- bounded compact parameter classes K_B;
- a global pointwise inverse Lipschitz modulus C_0 over those classes;
- a minimization over K_B, with existence but no computational guarantee.

The covering is then recovered by nearest-column synchronization under a margin inequality.

### R84-M4. This is finite-data recovery under a certified design, not self-calibrating inference

That distinction is now stated more honestly than in earlier versions, but it matters for significance.

The theorem does **not** solve:

- model-order selection without a signal floor;
- adaptive spatial sampling;
- certification of interstitial Lipschitz/separation margins from the observed records;
- computationally tractable global fitting over K_B;
- minimax-optimal sample complexity for the covering or geometric parameters;
- recovery when different components approach a collision at a rate tied to n or h.

The proof architecture is a standard and reasonable one: concentration, pointwise inversion, nearest-neighbor matching, cocycle gluing.

For a top-four general journal, I would need either a sharper statistical theory or a genuinely new topological/statistical phenomenon, not only a correct finite-sample wrapper around an already-separated inverse.

---

## 7. Major concern: the boundary-distance application is natural, but almost all geometric rigidity is imported

Theorem thm:v84-surface is the most important improvement in presentation and application.

It considers a simple surface and two arms with actions

- the boundary distance d_g(x,y);
- an unknown constant reference delay tau_* strictly larger than every boundary distance.

The scalar/latent theorem recovers the unordered pair of actions; the known ordering identifies the smaller one with d_g; the larger one is tau_*. The cited boundary-distance rigidity theorem then determines the metric up to a boundary-fixing isometry.

This is clean.

It is also thin as a new geometric theorem.

### R84-M5. The geometric difficulty begins after the paper has already recovered the full boundary distance

The new contribution is a calibration-removal front end for exact full boundary-distance data.

The genuinely hard geometric statement—rigidity of a simple surface from boundary distance—is classical and imported wholesale.

The theorem assumes projective deadline matrices at **every ordered boundary pair**. It does not address:

- sparse boundary pairs;
- partial boundary data;
- noise-to-metric stability;
- finite sampling of the boundary;
- nonsimple metrics;
- unknown reference-arm ordering;
- a reference delay varying in an unknown low-dimensional family;
- a detector class coupled to the geometry rather than pointwise arbitrary polynomial coefficients.

Thus the application is natural enough to answer the previous “engineered shear only” criticism, but it does not itself create a new boundary-rigidity theorem of comparable depth to the cited geometric result.

A top-four-level geometric application should make the selective/projective observation model solve a previously difficult geometric inverse problem, not merely reproduce full classical boundary-distance data under a reference-arm design.

---

## 8. Major concern: the common-lift compatibility theorem is useful certification, but algebraically elementary once its domain hypotheses hold

Theorem thm:v84-compatible is correct-looking and useful.

Once R and S are exact diffeomorphisms of the same invariant domain and r,s are coprime, the conditions

RS=SR and R^s=S^r

are exactly the group-theoretic compatibility relations needed for

g=R^u S^v.

This cleanly removes the previous unverified “common lift” premise on the region where all reconstructed graph pieces glue into two honest exact diffeomorphisms.

### R84-M6. The difficult geometry has been moved into the invariant-domain and graph-consistency hypotheses

The theorem does not infer an invariant domain from arbitrary partial sheets.

It assumes that observable graph checks succeed on an open Omega and that both reconstructed count maps are diffeomorphisms Omega -> Omega.

Once that is available, the Bezout reconstruction is nearly formal group theory.

This is an important correctness repair. It is not, in my view, a major new rigidity theorem.

The next conceptual advance would have to derive a large invariant domain, or certify near-compatibility under noise by a stability theorem for approximate roots/powers, rather than only state the exact algebraic test.

---

## 9. Major concern: the paper still does not have one theorem that controls all modules

Revision 84 is more unified than v83. The secant/tangent quotient is a genuine organizing idea.

But the full manuscript still consists of several layers whose mathematical engines are largely independent:

1. latent spectral factorization of projective matrices;
2. scalar quotient inversion;
3. finite-dimensional analytic evaluation design;
4. compactness-based stability;
5. permutation/covering synchronization;
6. finite-record concentration and mesh gluing;
7. exact-lift group algebra;
8. an imported boundary-rigidity theorem.

### R84-M7. The quotient invariant does not yet govern the whole theorem stack

The scalar quotient explains the action/detector ambiguity. It does not, by itself, explain:

- why two unknown readout channels should be recoverable;
- the topology of the component covering;
- the finite-record synchronization threshold;
- exact-lift compatibility;
- geometric rigidity of the resulting metric.

At the target journal level, I am still missing the result that makes these modules appear as manifestations of one new mathematical structure rather than a well-engineered synthesis.

The paper is now coherent. It is not yet inevitable.

---

## 10. Major concern: the literature audit is improved but still too narrow for the breadth of the claims

The bibliography is materially better than v83. It now includes:

- FRI / Prony references;
- Kato;
- Hatcher;
- Hoeffding;
- Pestov--Uhlmann;
- Stefanov--Uhlmann--Vasy.

This is progress.

### R84-M8. The principal novelty comparison is still incomplete

In particular, the manuscript should compare its new theorems with literature on:

- unisolvent interpolation and generic evaluation of finite-dimensional analytic function spaces;
- transversality / embedding arguments for finite-dimensional nonlinear parameter families;
- nonlinear sampling and stable parameter recovery beyond the specific FRI references cited;
- generalized Chebyshev systems and rational/logarithmic interpolation;
- statistical synchronization and permutation recovery under separation margins;
- noisy latent-mixture/tensor identification with unknown component number;
- stability of boundary distance / lens data recovery under measurement error;
- inverse problems with unknown source, gain, calibration, or sensor response.

The paper now says more carefully what it is **not** claiming. That is good. But a top-four referee also needs a convincing “closest predecessor” paragraph for every principal theorem.

At present I cannot tell from the manuscript whether the generic d+5 design result, the compact-class finite-evaluation theorem, or the mesh synchronization theorem is genuinely new as an abstract theorem, or primarily a new specialization/application of standard principles.

---

## 11. Major concern: the noisy theory and the geometric application remain disconnected

The paper now contains both:

- a finite-record noisy theorem on a spatial mesh;
- an exact continuum boundary-distance theorem.

But the two are not joined.

### R84-M9. There is no theorem propagating finite selective records to a stable metric reconstruction

For the simple-surface application, the paper assumes exact projective deadline matrices at every ordered boundary pair.

The finite-record theorem, by contrast, gives piecewise affine recovery of the latent centered field on a triangulated endpoint domain under supplied margins.

A substantially stronger paper would connect these:

1. sample finitely many boundary pairs and finitely many readout records;
2. recover boundary distance with an explicit uniform error;
3. invoke or prove an appropriate boundary-rigidity stability theorem;
4. obtain a quantitative metric error in a specified gauge/topology.

That would produce a genuinely integrated inverse problem.

Right now the statistics and geometry remain adjacent rather than combined.

---

## 12. Major concern: the paper has crossed the point where another incremental detector family would help

Revision 84 already contains:

- polynomial log-detectors;
- an exponential example;
- general regularly separating finite-dimensional spaces;
- analytic generic designs;
- protected logarithmic singularities;
- a no-positive-annihilator example;
- action divisors.

This is enough evidence that the phenomenon is not restricted to one toy family.

### R84-M10. Further progress now requires a change of scale, not another family or constant

I would not regard v85 as materially stronger merely because it adds another explicit detector basis, another clock count, another CI package, or another synthetic mechanical example.

The paper now needs one theorem that changes its conceptual scope.

---

## 13. Detailed source-level proof audit

This section records what I checked and where I do or do not presently see a correctness issue.

### 13.1 Theorem thm:v84-design

The normalized-difference argument is sound in outline.

The three regimes for the normalization size t are the right ones:

- t -> infinity leaves a nonzero normalized detector direction;
- t -> t_0 in (0,infinity) is excluded by secant injectivity;
- t -> 0 produces a nonzero quotient tangent, excluded by the tangent condition.

Finite-dimensional compactness of the detector coefficients and compactness of the action class then give compact closure in C(K_T). A finite collection of point evaluations separates that compact normalized family.

I do not see a short counterexample.

What should be made more explicit in a final version is the exact norm used on the two-action parameter, and the fact that a compact K contained in the off-diagonal action set stays a positive distance from the diagonal and from the clock singularity.

### 13.2 Lemma lem:v84-evaluations

The finite-order-zero incidence proof is clever and appears valid.

At an incidence point, using the equation involving the derivative one order below the first nonzero T-derivative gives an N by N diagonal derivative matrix in the clock variables. The incidence subset is therefore locally contained in a graph over the p-dimensional parameter coordinates. Countability then gives a null projection when N>p.

This argument should be presented as an incidence-dimension theorem, because that is its real content.

### 13.3 Theorem thm:v84-generic

The collision family has dimension d+4. Thus d+5 clocks are enough for the generic null-set argument.

The tangent-degeneracy family has even smaller effective dimension after coefficient normalization.

The theorem looks correct as a sufficient almost-everywhere design statement.

My objection is significance/sharpness, not an identified algebraic defect.

### 13.4 Theorem thm:v84-poles

The rational derivative / Rolle count is consistent.

For a scalar collision, after differentiating and clearing k protected and at most four moving simple poles, the numerator degree bound q+k+3 is sufficient. q+k+5 sample zeros force one more derivative zero than this degree permits.

The residue argument then separates protected coefficients from moving action poles.

The tangent argument uses double moving poles and similarly forces the derivative coefficients to vanish.

No immediate defect found.

### 13.5 Proposition prop:v84-no-positive

The zero-integral identity for every sampled annihilator follows directly from annihilating 1 and h.

Because a nonzero Cauchy kernel is continuous on [a,b] and cannot have one strict sign with zero integral, every such annihilator kernel takes both signs.

The six-clock zero-counting proof also appears internally consistent.

This is a good counterexample to any attempt to make a positive annihilator necessary.

### 13.6 Theorem thm:v84-divisors

The projective common-factor gauge is a genuine and useful observation.

Recovering reduced ratios D_b/D_c determines the common gcd only up to replacing the common factor by another monic factor of the same degree with roots in the admissible interval.

The lcm argument for E_b=D_b/G is correct-looking.

The manuscript appropriately warns that stable rootwise recovery near multiplicities is a separate issue.

### 13.7 Theorem thm:v84-fibre

This is one of the cleanest additions.

At q+2 clocks the single annihilator fixes only

F(x)-F(y)=d.

Since F is strictly increasing, the fibre is exactly one open interval in the u=F(y) coordinate, with a unique nuisance polynomial for each point.

This is materially stronger than the old local IFT lower bound.

### 13.8 Theorem thm:v84-mesh

The concentration calculation and the separation inequality are consistent.

The edge-matching inequality is the correct one:

same-component fitted distance <= L_U h + 2 e_n;

different-component fitted distance >= s_* - L_U h - 2 e_n.

Thus 2 L_U h + 4 e_n < s_* gives unique nearest matching.

The face cocycle then reconstructs the covering in the expected simplicial way.

A polished version should explicitly state that the covering reconstruction is controlled by the 2-skeleton of the fixed triangulation, which makes the topological step completely transparent in dimensions above two.

### 13.9 Theorem thm:v84-compatible

The group identity is correct once R and S are full exact diffeomorphisms of the same invariant domain.

The phrase “as full exact lifts” is essential because equality of phase maps without primitive equality would be insufficient.

No correctness objection here.

### 13.10 Theorem thm:v84-surface

As stated, the reduction is correct.

The strict apparatus inequality

sup d_g < tau_* < T_1

labels the recovered unordered actions by magnitude. The smaller one is the boundary distance and the larger one is the reference delay. The classical simple-surface boundary-distance rigidity theorem supplies the metric conclusion.

The theorem is exact full-data geometry. It should not be sold as a noisy or finite-boundary-sampling result.

---

## 14. Technical and exposition comments

These are secondary to the editorial concerns above.

### R84-T1. Define the action-pair norm in Theorem thm:v84-design

The inequality uses |a-a'| for a=(x,y). State the norm explicitly and keep it fixed throughout the compactness proof.

### R84-T2. State the compact separation from the diagonal in the finite-design theorem

A compact K subset of A automatically has positive distance from x=y. Say this explicitly because it is what makes all action derivatives uniformly bounded and avoids confusion with degeneration of the tangent model.

### R84-T3. Make the incidence lemma's parameter dimension bookkeeping explicit

For the generic scalar collision, list the d nuisance coordinates and four action coordinates. For the tangent family, list the normalized coefficient charts and the two action coordinates. This will make the d+5 count easier to audit.

### R84-T4. Distinguish generic unisolvence from quantitative conditioning

The d+5 theorem gives almost-everywhere injectivity and local smooth inversion. It does not give a useful lower bound on the smallest sampled Jacobian singular value for a randomly chosen clock tuple. The manuscript should keep generic identifiability separate from numerical conditioning.

### R84-T5. State a closed definition of the compact classes K_B

The current prose describes them by bounds and margins. A displayed definition would make compactness and the minimization estimator easier to verify.

### R84-T6. Clarify the status of C_0

C_0 is a global inverse modulus over the declared compact exact class modulo permutations. It is not produced from the data. Make this explicit in the theorem statement, not only in the preceding prose.

### R84-T7. State whether readout samples are independent across vertices and clocks

The union-bound proof only needs the per-cell concentration assumptions in the stated form, but the experiment should state the independence structure cleanly.

### R84-T8. Explain the simplicial covering reconstruction through the 2-skeleton

The face relations are enough because covering monodromy is a pi_1 object. One sentence invoking the 2-skeleton/cellular approximation would make the proof more standard and readable.

### R84-T9. In the surface theorem, emphasize that every ordered boundary pair is observed

This is a continuum full-data assumption. It should appear in the first sentence of the theorem's discussion so readers do not mistake it for a finite acquisition theorem.

### R84-T10. Separate “boundary-fixing isometry” from “metric equality”

Use one consistent geometric formulation: equality up to pullback by a diffeomorphism fixing the boundary.

### R84-T11. The boundary-distance application does not need the global component-covering machinery

At each boundary pair the two-arm inversion is pointwise. State this explicitly. It will actually make the logic cleaner.

### R84-T12. The reference arm is an important structural assumption

The paper correctly admits it. I would elevate it further: the geometric reduction is not calibration-free in an absolute sense; it replaces calibrated channels and detector coefficients by a known two-arm architecture, an ordering gap, and a constant reference action.

### R84-T13. The protected-pole theorem should separate exact root identities from conditioning near pole collisions

The protected poles are fixed outside I, so the exact theorem is fine. If the paper discusses robustness, the dependence on distance between moving actions and protected poles should be made explicit.

### R84-T14. Do not let the expanded historical edition compete with the principal paper

The 12-line principal entry point is now coherent. For journal submission, I strongly recommend keeping the principal v84 article as the only manuscript under editorial review and treating the inherited expanded edition as repository background.

### R84-T15. The bibliography still needs theorem-by-theorem closest-predecessor paragraphs

Merely increasing the reference count is not enough. The comparison should be attached to each new theorem.

---

## 15. Status of the v83 major objections

| v83 issue | v84 status |
|---|---|
| M1: central theorem too close to two-moment/Chebyshev plus spectral factorization | **Improved but not closed**. General quotient secant/tangent theory is new structure, but still a regular-embedding criterion plus compactness. |
| M2: sampled quotient is not a detector function-space theory | **Substantially closed** by thm:v84-design. |
| M3: positive-kernel hypothesis is restrictive | **Closed as a necessity objection** by prop:v84-no-positive. |
| M4: global stability is fixed-stratum reference-local | **Closed as a scope/statement issue**; the limitation is now explicit. |
| M5: no observable finite-data algorithm | **Substantially closed** by thm:v84-mesh, under strong supplied design/margin assumptions. |
| M6: quotient metric is reference-dependent | **Partly closed**; finite mesh recovery learns covering type, while the C^m noisy inverse remains fixed-stratum. |
| M7: geometry assumes supplied global organization | **Partly closed** by observable graph consistency/common-lift tests, but invariant-domain and apparatus structure remain supplied. |
| M8: positive hypotheses not near-optimal | **Improved** by unsampled-region obstruction, regular detector criterion, and exact fibres; still no broad near-optimal geometric acquisition theorem. |
| M9: only engineered physical example | **Substantially closed** by the simple-surface boundary-distance reduction. |
| M10: literature positioning too thin | **Improved but still a major issue**. |
| M11: sharpness only local | **Closed for the polynomial scalar problem** by thm:v84-fibre and the finite-record risk corollary. |
| M12: theorem stack lacks a unifying invariant | **Improved but not closed**. The quotient secant/tangent picture unifies the scalar layer, not the whole latent/topological/geometric stack. |

This is why v84 deserves a fresh evaluation rather than an automatic continuation of the v83 rejection.

---

## 16. What would justify another top-four review

I would only recommend another four-leading-general-journals-style review if the next revision changes the mathematical scale in at least one of the following ways.

### 16.1 A genuinely structural detector-space theorem

For example:

- classify regularly separating spaces in a broad natural category;
- give a sharp sample-complexity invariant;
- characterize maximal admissible nuisance spaces;
- prove a total-positivity / Chebyshev / variation theorem that makes the current examples corollaries.

### 16.2 A fully integrated finite noisy geometric inverse problem

For example:

- finitely many boundary pairs and finitely many records;
- recovery of approximate boundary distance;
- quantitative propagation to a metric stability result;
- explicit rates and identifiability thresholds.

That would connect the strongest statistical and geometric parts of the paper rather than placing them side by side.

### 16.3 A natural inverse problem where the new observation model removes a real open obstruction

The present simple-surface theorem removes calibration before applying a solved full-data rigidity theorem.

A more consequential application would remove unknown detection/readout from a setting where calibrated or marked data are currently essential to the mathematical theorem itself.

### 16.4 A sharp robust theory beyond fixed margins

A theorem with minimax lower and upper bounds, unknown order, near-collision scaling, or adaptive design would materially deepen the finite-record part.

### 16.5 A new global geometric theorem for partial return data

Derive the invariant domain or common lift from incomplete observations under intrinsic dynamical hypotheses, rather than assuming the region on which the graph tests already close.

---

## 17. Final assessment

Revision 84 is a serious improvement and, in several respects, the first version of this A2 line that has a coherent answer to the broad detector-space question.

The strongest achievements are:

- the move from one sampled positive-kernel quotient to a function-space secant/tangent formulation;
- the proof that positive annihilators are not necessary;
- the global q+2 ambiguity fibre;
- finite-record recovery of the component covering and monodromy under explicit margins;
- observable exact compatibility of coprime return lifts;
- a natural simple-surface boundary-distance reduction.

I do **not** reject this revision because I believe the central calculations are obviously wrong. On the contrary, the new proofs I audited look substantially more mature than the earlier rounds.

I reject it at the requested editorial level because the deepest new abstract result is still, at base, a regular finite-dimensional quotient-embedding criterion combined with compactness and analytic incidence counting; the explicit detector families are handled by specialized rational zero counting; the finite-record covering theorem uses strong supplied margins and standard synchronization logic; and the geometric application recovers classical full boundary-distance data before importing the actual rigidity theorem.

That is a publishable research program. It is not yet, in my judgment, a paper of the conceptual scale expected at Annals, Inventiones, Acta, or JAMS.

**Final recommendation: reject in the present form at the four-leading-general-journals level.**

I would be willing to reassess only after a revision that adds a theorem changing the conceptual scale, rather than another incremental detector family, clock count, verification layer, or synthetic example.
