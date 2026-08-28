# Final hostile audit of the five maximal strengthenings

**Date:** 2026-08-28  
**Scope:** θ-Theory only  
**Rule:** a claim passes only if the stated hypotheses produce the stated object without an unnamed genericity, topology or representation upgrade.

## Finding F1 — cohomological conjugacy did not differentiate the full reduced resolvent

Earlier wording could be read as if

\[
L_{a,q}=e^{qc(a)}M_{e^{-qg_a}}L_aM_{e^{qg_a}}
\]

made every parameter derivative of `R_a` automatic.  It does not: differentiating the full reduced resolvent still requires parameter control of `L_a` on the relevant graded spaces.

**Repair:** the actual radial theorem now exports only invariant-projector/source U3 and constant-plus-coboundary twisted eigendata.  Generic noncoboundary full-resolvent U3 remains under the Paper-I graded packet.

## Finding F2 — one changing periodic orbit could be permuted by a conjugacy

A changing multiplier on an unnamed orbit does not by itself exclude a conjugacy which permutes periodic orbits.

**Repair:** the actual table is chosen with a unique shortest regular period-two orbit and a positive isolation gap.  Its continuous-time period and its collision-map Jacobi trace both change, so no time-preserving flow conjugacy or local `C^1` map conjugacy can permute it away.

## Finding F3 — compact geometry did not imply high-frequency family differentiability

Fixed-table BDL estimates plus compactness do not automatically define parameter derivatives on one common anisotropic graph domain.

**Repair:** the unconditional actual theorem is the exact similarity family.  On transported spaces

\[
\widetilde A_a=s(a)^{-1}A_0,
\]

so all-frequency bounds and derivatives are exact.  Nonconjugate family response is stated only under a complete graded generator-symbol packet.

## Finding F4 — “optimal rate” lacked a standard full law metric

A matching rate in a restricted Stein/Dirichlet test class would not be an optimal Wasserstein rate for the rough path law.

**Repair:** the controlling theorem uses full `W_1` for the fractional-Sobolev step-two rough-path metric.  The Gaussian shift admits an exact Brownian-grid coupling for the upper bound and a 1-Lipschitz distance-to-polygonal-subspace test for the lower bound.

## Finding F5 — second-level bridge error required a separate estimate

First-level interpolation estimates alone do not control an enhanced rough path.

**Repair:** the technical bridge note decomposes the second-level difference into local bridge iterated integrals and bridge/coarse cross terms.  Chen's identity and scaling show that the rough-metric square-root contribution has the same or faster rate.

## Finding F6 — pure Isaacs could not be universally positive

Matching pennies has no pure saddle.

**Repair:** the compact theorem is the exact equivalence

```text
pure saddle exists  <=>  H_minus = H_plus.
```

The noncompact positive theorem is restricted to a strong concave-convex coercive class, where the saddle operator is strongly monotone.

## Finding F7 — a pointwise Hamiltonian saddle did not yet verify the path game

Optimizing the Hamiltonian is not by itself a proof that the stochastic path game has a value.

**Repair:** `TECHNICAL_NOTE_ENTROPIC_GAME_VERIFICATION.md` applies functional Ito calculus and completes squares:

\[
-cp^2+pu+pv-\frac\mu2u^2+\frac\nu2v^2
=-\frac\mu2(u-p/\mu)^2
 +\frac\nu2(v+p/\nu)^2.
\]

This yields the lower/upper inequalities, the pure saddle, the path DPP, PPDE and BSDE value.  Uniform cylindrical approximation removes classical terminal regularity.

## Finding F8 — weighted noncompact “actualization” needed a concrete prior-forgetting mechanism

A Lyapunov moment bound alone does not imply filter stability.

**Repair:** the actual hidden process is i.i.d. Gaussian under a deterministic product shift.  Prediction maps every prior to the same Gaussian law in one step; bounded nondegenerate observations preserve all weighted moments.  Prior forgetting is exact, not asymptotic or assumed.

## Formula audit

The following were checked independently in a Python reasoning environment:

- period-two Jacobi trace multiplication;
- strict sign of its radial derivative;
- exact similarity-resolvent factorization;
- quadratic saddle value and cross-term cancellation;
- a valid fractional-Sobolev rough-path parameter window;
- Cole-Hopf cancellation;
- observation nondegeneracy.

## Verdict

```yaml
hostile_findings: 8
hostile_findings_repaired: 8
requested_strengthening_frontiers: 5
positive_frontiers_with_actual_witness: 5
universal_false_variants_with_terminal_no_go_or_iff: 5
known_internal_mathematical_gaps: 0
external_peer_review: NOT_PERFORMED
mathematical_proof_certified_externally: false
formal_credit: 0
```

The last three fields are essential.  This audit closes known internal defects; it is not an external correctness certificate or a journal verdict.
