# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `6fa8639339ebae9a19122cbdba339ec6f275b562`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

There is no revised C2 manuscript on the declared branch. The strict-dual argument, abstract form response, rigidity claims, changing-filtration theorem, and contraction category are unchanged. No missing invariant-measure, form-domain, Livšic, optional-projection, or martingale-representation hypotheses have been added.

## 2. Unresolved fatal defects

### 2.1. Weighted strict duality and the coboundary conclusion remain incomplete

The topology is described through bounded nets and local convergence rather than by a proved locally convex seminorm construction. Patching Riesz measures over compact sets does not by itself establish a single countably additive measure with finite weighted variation or continuity on the full topology.

More concretely, the assertion that nonzero constants are outside the closed coboundary span uses integration against an invariant probability. The theorem assumes only a weighted continuous flow and neither assumes nor proves existence of any invariant probability with finite `W` moment. Without such a functional, the separation argument fails. Weighted continuity of composition also needs a bound on `W\circ\Theta_t` that is not stated.

### 2.2. The type-(B) and form-compression results are only conditional abstract lemmas

Under a fixed coercive form domain, differentiable forms, and a fixed reference Hilbert space, inverse differentiation is standard. The paper does not verify these hypotheses for A4, B4, or any prepared platform. In the form-level memory statement, the projection must preserve the form domain and the complementary block must be coercively invertible; those conditions are absent. Differentiability of projections and Schur complements is likewise not proved.

### 2.3. The model-specific rigidity statements remain unsupported

Equality of full perturbed pressures may imply equality of suitable expectations under strong differentiability assumptions. It does not automatically yield a Livšic theorem for the precise countable, noncompact, weighted Sinai coding or closedness of the coboundary range. Neither theorem is stated. For hard spheres, B3's local and invalid observability estimate does not characterize the global annihilator of all finite-action balanced paths; endpoint, boundary, positivity, and microcanonical constraints may add directions.

### 2.4. The changing-filtration theorem remains false at the stated level of generality

Convergence of one-time conditional kernels for bounded cylinders does not imply process-level extended weak convergence of optional projections under changing filtrations. Multi-time consistency, right-continuous versions, Aldous tightness, and a common path topology are needed. Doob's maximal inequality controls moments of a martingale supremum but does not provide a time modulus for varying jump structures.

Even if the optional projection converged, a positive martingale is not automatically a stochastic exponential driven by the claimed observed Gaussian noise. A martingale representation or innovation theorem for the limiting filtration and identification of the stochastic logarithm are indispensable. Conditional expectation of a full-filtration exponential onto a smaller filtration need not preserve its integrand or simple form. The Girsanov and BSDE conclusions therefore do not follow.

### 2.5. The contraction category remains largely definitional

The morphism definition assumes continuous or exponentially approximable state maps, bounded source pullbacks, strict adjoints, and form intertwiners. The theorem then announces precisely the rate, pressure, derivative, covariance, and memory commutations that require additional exponential-equivalence, differentiability, and block-domain hypotheses. No nontrivial model morphisms are verified. Building the required properties into the morphism does not prove universality for the advertised platforms.

## 3. Editorial consequence

A revised paper must separate the valid abstract lemmas from model-specific claims, add an invariant-measure hypothesis, prove the form-domain conditions, establish exact Livšic/annihilator theorems, and supply a genuine changing-filtration plus innovation theorem. None is present.

## 4. Recommendation

**Reject without reconsideration.** The local functional-analytic observations do not establish the advertised rigidity and stochastic universality.