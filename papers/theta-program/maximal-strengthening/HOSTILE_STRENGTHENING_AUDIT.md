# Hostile audit of the five maximal θ-Theory strengthenings

**Date:** 2026-08-28  
**Scope:** internal mathematical and dependency audit  
**External peer review:** not performed

## Audit rule

A strengthening is accepted only if it has one of the following forms:

1. an explicit actual system satisfying every theorem field;
2. a theorem over a named packet whose fields are used in the proof;
3. a counterexample/maximality theorem proving that a stronger requested
   statement is false.

Reclassification alone does not count as a positive actual theorem, and an
actual source-specific channel is not renamed as generic.

---

## Finding S1 — “specular Sinai U3” was ambiguous

A third derivative of one invariant average, a third derivative of the full
operator, and a generic noncoboundary pressure U3 are different claims.

### Repair

`SPECULAR_SINAI_RADIAL_U3.md` proves two exact actual channels for a genuinely
nonconjugate radial family:

- arbitrary finite-order invariant-projector response by differentiated
  invariance;
- arbitrary finite-order exact-coboundary twisted response by gauge conjugacy.

The nonconjugacy witness is the changing trace of a period-two monodromy:

\[
\operatorname{tr}M
=2+4\kappa_1\tau+4\kappa_2\tau
+4\kappa_1\kappa_2\tau^2,
\]

\[
\frac d{da}\operatorname{tr}M(0)
=-\frac{4d(d-R_2)}{R_1^2R_2}\ne0.
\]

The complete source identity

\[
\sum_{k=1}^j\binom jkL_0^{[k]}\rho_0^{(j-k)}
=(I-L_0)\rho_0^{(j)}
\]

was checked against the Leibniz derivative of `L_a rho_a=rho_a`.

The generic centered noncoboundary geometry-only theorem is explicitly denied
by the split-surjective face-defect result.  This is a maximality boundary, not
an omitted lemma.

---

## Finding S2 — compactness alone does not uniformize BDL

A compact parameter set cannot create a Dolgopyat/nonintegrability witness if
one degenerates at a parameter.

### Repair

`MOVING_FAMILY_HIGH_FREQUENCY_BDL.md` requires a strict
`BDL-FAMILY-WITNESS-v1`.  Openness is applied to the finite-time strict witness,
and only then is compactness used to take a finite cover.  Parameter
resolvent derivatives are restricted to graded generator letters.

The ordered-composition formulas were checked:

\[
R'=RG_1R,
\]

\[
R''=RG_2R+2RG_1RG_1R,
\]

\[
R'''=RG_3R+3RG_2RG_1R+3RG_1RG_2R+6RG_1RG_1RG_1R.
\]

The stronger single-pointwise-weight domain is excluded by the unbounded ratio
of consecutive grazing weights.

---

## Finding S3 — “optimal WIP rate” was over-typed twice

First, no exponent is optimal simultaneously in endpoint, uniform, Hölder,
fractional-Sobolev, and rough-path metrics.  Second, the quantitative
Stein--Dirichlet theorem used by the draft does not estimate every Lipschitz
rough functional; its finite-dimensional step needs regularity of the pulled-
back second derivative.

### Repair

`OPTIMAL_ENHANCED_WIP_RATE.md` now fixes:

```text
p>6,
1/3<eta-1/p,
eta<1/2,
```

the step-two fractional-Sobolev rough topology, and the normalized regular
Stein--Dirichlet test class `Sigma_(eta,p)`.  The law distance is

\[
d_{SD}^{\eta,p}(\mu,\nu)
=
\sup_{\|F\|_{\Sigma_{\eta,p}}\le1}
|\mu(F)-\nu(F)|.
\]

The upper rate is exactly the rate proved by the Stein finite-dimensional
replacement plus Brownian bridge interpolation:

\[
d_{SD}^{\eta,p}
\le CN^{-(1/2-\eta)}.
\]

A lower test in the **same class** is

\[
F_N(\mathbf x)
=c_0N^{-3/2+\eta}
\sum_k
\phi(\sqrt N D_{k,N}(\pi_1\mathbf x)),
\]

where `phi` is smooth, even, bounded, and nonnegative.  The scaled midpoint
directions have uniform Cameron--Martin norm and disjoint supports, so the
first three derivative bounds of `F_N` are uniform.  It vanishes on every
affine mesh walk, while Brownian midpoint defects give

\[
\mathbb EF_N(\mathbf B_\Sigma)
=cN^{-(1/2-\eta)}.
\]

Thus the upper and lower rates match in `d_SD^(eta,p)`.  The full bounded-
Lipschitz Kantorovich--Rubinstein exact rate is explicitly not claimed.

The accumulated nonautonomous block exponent was rechecked:

\[
\epsilon^{-2}m_\epsilon^{-(1+\delta)}\to0,
\qquad
\epsilon^2m_\epsilon\to0,
\qquad
\delta=1/2-\eta.
\]

For `m_epsilon=epsilon^{-kappa}` this is exactly

\[
2/(1+\delta)<\kappa<2.
\]

---

## Finding S4 — general pure-strategy Isaacs is false

Mixed minimax plus compactness does not yield a pure saddle.

### Repair

Matching pennies `F(u,v)=uv`, `u,v in {-1,1}`, gives

\[
H^-=-1,
\qquad H^+=1,
\]

but mixed value zero.  The correct compact theorem is

\[
\text{pure saddle exists}
\quad\Longleftrightarrow\quad H^-=H^+.
\]

For the positive actual class, the saddle operator

\[
\mathcal G=(-D_uF,D_vF)
\]

is strongly monotone when `F` is strongly concave in `u` and strongly convex
in `v`; the mixed Hessian terms cancel in the symmetric part.  The scalar
four-branch saddle formulas were independently solved from the first-order
system:

\[
u_*=(\mu b-\gamma c)/(\gamma^2+\lambda\mu),
\]

\[
v_*=(-\gamma b-\lambda c)/(\gamma^2+\lambda\mu).
\]

---

## Finding S5 — the first weighted/path construction retained incompatible fast state

The initial draft used the doubling-map state as an iid uniform and retained a
fast filter variable in a limiting PPDE without its generator.

### Repair

The observation noise is now generated by a two-sided deterministic Bernoulli
shift on `[0,1]^Z`; its coordinate uniforms are exactly iid under product
Lebesgue measure.

The weighted filter and path branches are separated and then coupled by
stationary averaging.  For the fast stationary filter,

\[
\epsilon^2\sum_{n<O(\epsilon^{-2})}
[H(\pi_n)-\bar m]=O_{L^2}(\epsilon),
\]

so the belief variable disappears from the slow path limit and only `bar m`
enters the drift.

The limiting delay equation is Markov on the segment space.  Its value equation
now contains the horizontal shift generator:

\[
\partial_tV+\mathcal SV+b_*\cdot\partial_0V
+\frac12\operatorname{Tr}(a\partial_{00}^2V)+\ell_*=0.
\]

The payoff includes an integral and a maximum over the entire terminal window,
so the branch is genuinely path-dependent.

---

## Audit verdict

```yaml
strengthening_items_audited: 5
substantive_scope_or_formula_repairs: 6
actual_positive_systems:
  - nonconjugate_radial_specular_invariant_and_coboundary_U_infinity
  - compact_BDL_family_with_actual_radial_all_frequency_channel
  - four_branch_optimal_fractional_Sobolev_Stein_Dirichlet_rate
  - four_branch_unique_pure_Isaacs_game
  - deterministic_noncompact_filter_and_delay_path_evaluation
maximality_or_counterexample_results:
  - generic_geometry_only_noncoboundary_U3_no_go
  - universal_single_grazing_weight_domain_no_go
  - topology_or_test_class_free_optimal_rate_no_go
  - full_Lipschitz_KR_rate_not_supplied_by_Stein_class
  - unrestricted_pure_saddle_no_go
known_internal_strengthening_gaps_after_audit: 0
external_peer_review: NOT_PERFORMED
mathematical_proof_certified_externally: false
formal_credit: 0
```

The final three fields are mandatory.  This audit is an internal proof attack,
not an external correctness certificate.
