# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`C2_ACCRETIVE_FORM_FUNCTOR.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The model-specific rigidity, optional-projection limit, and universal contraction claims are not proved.

## 1. Overall assessment

The paper contains two useful corrections. It explicitly transports varying Hilbert realizations to a fixed reference space and includes the derivative of the metric/transport in response formulas. It also observes that a finite-dimensional compression of a dissipative resolvent is strictly accretive in the open right half-plane, which can indeed imply invertibility of the compression under the stated finite-dimensional domain assumptions.

These local functional-analytic observations do not establish the manuscript's global claims. The weighted strict-dual theorem is incompletely proved and contains an unstated existence assumption; the type-(B) and form hypotheses are not verified for any of the platforms; the Livšic/closed-gauge rigidity statements require major model-specific theorems; changing-filtration kernel convergence is promoted to process-level optional-projection, stochastic-exponential, Girsanov, and BSDE convergence without a martingale-representation argument; and the “typed contraction category” largely builds desired conclusions into its morphism definition.

## 2. Decisive mathematical objections

### 2.1. [MAJOR] The weighted strict topology and its dual are not proved as stated

The manuscript defines `\beta_W` sequentially/netwise by boundedness in `\|F/W\|_\infty` and uniform convergence on `W`-compact sets. A locally convex topology must be specified by a family of seminorms or an equivalent standard construction. The proof of `thm:r17-c2-dual` then argues that a continuous functional is bounded on compactly supported unit sets and patches Riesz measures over a compact exhaustion.

This does not establish continuity on the full strict topology or the finite weighted variation

\[
\int W\,d|\mu|<\infty.
\]

One must prove compatibility of the local measures, countable additivity on the full Borel sigma-field, and a global weighted bound from a single neighborhood of zero, not from separate bounds that may grow with the compact set. Conversely, dominated convergence for a net uniformly bounded by `W` requires weighted tightness and the exact topology; it is not enough to cite it informally.

The theorem may be true for an appropriately defined weighted strict topology, but the submitted proof does not establish it.

### 2.2. [FATAL as stated] The assertion that constants are not in the coboundary closure uses an unstated invariant probability

The proof says that a nonzero constant has nonzero integral under a probability and therefore cannot lie in the closed coboundary span. This requires the existence of an invariant probability in `\mathcal M_W(E)`. The theorem assumes only a continuous weighted flow `\Theta_t`; a general flow on a Polish space need not possess any invariant probability with finite `W` moment.

Without such a measure, the annihilator may be trivial and the separation argument fails. The theorem must either assume an invariant weighted probability or prove one from explicit compactness/dissipativity conditions. This is a concrete logical gap in the active statement.

The continuity of `F\mapsto F\circ\Theta_t` on `C_W(E)` also requires a bound such as `W(\Theta_t x)\le C_tW(x)` and continuity in `t` in the weighted strict topology. “Continuous weighted flow” is not defined to include these properties.

### 2.3. [MAJOR] The type-(B) resolvent response is only a conditional abstract lemma, not a platform theorem

Under a fixed dense form domain `V`, uniform sectorial coercivity, and `C^2` form dependence in `\mathcal L(V,V^*)`, the inverse differentiation formula is standard. The paper, however, does not verify any of these hypotheses for A4's history generator, B4's nonlinear kinetic object, the memory generators, or the varying prepared measures.

There is also a notation issue: `\widetilde L_\eta` is treated both as the generator associated with a dissipative semigroup and through a coercive form `a_\eta`, with the sign relation between `A_\eta` and `L_\eta` left implicit. The displayed derivative `D_\eta\widetilde L_\eta` is generally an operator `V\to V^*`, not an operator on `H_0`; the exact typing and signs must be maintained throughout.

Thus `thm:r17-c2-connection` is at most an abstract proposition under strong assumptions, not evidence that the theta-theory platforms possess the announced response calculus.

### 2.4. [MAJOR] The form-level compression requires hypotheses not stated

For an operator-domain resolved space, the accretivity calculation in `thm:r17-c2-memory` is plausible:

\[
\Re(C_\eta(z)r,r)>0,
\qquad \Re z>0,
\]

provided the transported generator is genuinely dissipative in the fixed inner product. Finite dimensionality then yields invertibility.

The form-level extension is not obtained by simply “blocking the weak equation.” To decompose `V` into `\mathcal R\oplus\mathcal R^\perp`, one needs the projection onto `\mathcal R` to preserve `V` continuously, and the complementary form block must be invertible/coercive on `V\cap\mathcal R^\perp`. The Schur complement must be defined as a bounded matrix and related to the compressed resolvent. None of these properties is proved.

Covariant differentiation of the Schur complement also requires differentiability of the projections and complementary inverses in fixed spaces. The theorem lists these derivative terms but does not establish their existence.

### 2.5. [FATAL] Equality of perturbed pressures does not yield the stated model-specific rigidity by the submitted proof

If two full perturbed pressure functionals agree on a strong neighborhood and are differentiable in a convergence-determining class, equality of equilibrium expectations—and potentially of equilibrium laws—is plausible. The paper then makes much stronger conclusions.

For the Sinai platform it claims that equality of periodic sums implies

\[
F_1-F_2=\text{constant} + \text{closed dynamical coboundary}
\]

in the A3 weighted potential space. This requires a Livšic theorem for the precise countable renewal shift, with its recurrence, regularity, summability, and unbounded-weight conditions, plus closedness of the coboundary range in the chosen topology. None of these hypotheses is stated or proved. Periodic orbit approximation itself is nontrivial in a countable noncompact coding.

For hard spheres, equality against all balanced finite-action variations is said to identify the annihilator as the balance gauge `(r,-\Delta r)` plus collision invariants. B3's claimed closed-range theorem is local, based on an invalid `H^1_v` observability estimate, and does not characterize the global annihilator of the nonlinear finite-action path space. Boundary, endpoint, positivity, and microcanonical constraints can add annihilator directions. The asserted rigidity is therefore unproved.

### 2.6. [FATAL] The hypotheses of the changing-filtration theorem are neither sufficient nor verified

Theorem `thm:r17-c2-optional` assumes that A4/C1 conditional kernels converge in a regular chart and likelihood ratios are uniformly bounded in `L^{1+\delta}`. It concludes process-level extended weak convergence of

\[
\left(X^\varepsilon,L^\varepsilon,
E[L_T^\varepsilon\mid\mathcal G_t^\varepsilon]\right).
\]

Convergence of conditional expectations of bounded continuous future cylinders at each fixed time is not enough. One needs a theorem controlling the varying filtrations, joint finite-dimensional conditional laws at multiple times, right-continuous modifications, and tightness of the optional-projection processes. Doob's maximal inequality bounds the supremum of a martingale in `L^p`; it does not by itself give a time-modulus or Aldous tightness when the filtrations and jump structures vary.

The approximation of `L_T` by bounded continuous cylinders also requires a common path topology and uniform integrability compatible with the conditional kernels. An `L^{1+\delta}` bound gives uniform integrability, but not density of cylinder functions in `L^1` uniformly over changing laws without additional regularity.

The A4/C1 conditional-kernel convergence invoked as input is itself unproved.

### 2.7. [FATAL] An optional projection is not automatically the claimed Cameron–Martin stochastic exponential

Even if

\[
M_t=E[L_T\mid\mathcal G_t]
\]

is the limit of the optional projections, it is only known to be a positive `\mathcal G_t`-martingale. To represent it as a stochastic exponential driven by the limiting observed Gaussian noise, one needs a martingale representation property for the limiting filtration and identification of the stochastic logarithm/bracket. If the observation filtration is smaller than the full Gaussian filtration or contains additional information, such a representation is not automatic.

The proof simply says that the B3/A4 limiting likelihood has Cameron–Martin form and therefore the projected likelihood is the limiting stochastic exponential. Conditional expectation of a stochastic exponential onto a subfiltration need not retain the same integrand or even the same explicit exponential form without nonlinear filtering/innovation theory.

Consequently, the claims that Girsanov transformations and bounded risk-sensitive BSDE representations commute with the microscopic limit require separate stability theorems for semimartingale characteristics, filtrations, drivers, terminal data, and uniform integrability. None is provided.

### 2.8. [FATAL] The “typed contraction category” embeds conclusions into the definition

A morphism is defined to include a continuous or “exponentially approximable” state map, a strict adjoint, a bounded pullback on strong sources, and an intertwining map on the form bundle. Theorem `thm:r17-c2-functor` then states that rates, pressures, covariances, cotangents, and memory commute.

Several conclusions are not formal consequences of the listed data:

1. an exponentially approximable map yields an extended contraction only under a precise superexponential approximation and exponential-tightness theorem;
2. the finite-volume pressure identity `Q_T(G)=Q(T^*G)` requires the microscopic observable to be exactly the pullback and the normalizations to match;
3. differentiating limiting pressures requires uniform differentiability and interchange of limit and derivative;
4. covariance push-forward requires convergence in a topology where `T` and `T^*` act continuously;
5. memory Schur complements commute only under explicit block-unitary/similarity and domain conditions, not an informal “commuting square.”

The proof says that all maps and topologies are “part of the definition.” That makes the theorem partly bookkeeping rather than a mathematical universality result. The class of genuine model morphisms satisfying these strong assumptions is not shown to contain any nontrivial examples or to be closed under composition with all required estimates.

## 3. Dependency consequences

C2 depends on A3/A4 and B3/B4/C1, which fail independent review. Its potentially valid abstract accretivity lemma does not rescue the model-specific rigidity, filtering, and contraction conclusions. D1 cites C2 for componentwise contraction and tangent commutation; that use is not licensed.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a standard, explicitly seminormed weighted strict topology and a complete duality proof;
2. an invariant-measure hypothesis for the coboundary-annihilator statement;
3. verification of fixed form domains, coercivity, and metric transport for each actual platform;
4. a rigorous form Schur-complement theorem with projection/domain hypotheses;
5. separate countable-shift Livšic and hard-sphere annihilator theorems in the exact spaces used;
6. a changing-filtration convergence theorem with finite-dimensional and Aldous-type conditions;
7. a martingale-representation/innovation proof before claiming stochastic-exponential, Girsanov, or BSDE limits;
8. a nonvacuous category of explicitly verified morphisms and precise extended-contraction/differentiation hypotheses.

## 5. Recommendation

**Reject.** The transported metric connection and right-half-plane compression observation are useful local facts. The paper's advertised rigidity, optional-projection, stochastic, and universal functorial conclusions are not consequences of those facts and remain unproved. The manuscript would need to be separated into several substantial, model-specific papers before it could be evaluated as complete mathematics.