# Response to the v38 external report: A2-DYN revision 39

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v38-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `44a673d7d0dd2662e679b99f344709ce6f832107` / `dadc2fc8896e471c2686e02389df82f075b9051f`.  
**Reviewed author SHA:** `00f8b9baa95a2fa9d29b1e2e7164dc0f5cb2938e`.  
**Frozen v38 paper tree:** `8b2b1d651e059c69827d10be0882c333a8901be1`.  
**New source:** `papers/A2-DYN-v39-referee-response/main.tex`.

We thank the referee for identifying the precise distinction between every diverging return-index window and a single index, and between fixed roof intervals and a raw pointwise density. We keep the original problem, section, title and all inherited mathematics. The revision addresses the arithmetic of the full occupation torus and the contribution of the actual section endpoints by two new proof chains. It does not set a previously uncontrolled inverse to zero.

## 1. Control of the full occupation torus

Theorem `thm:v39-section-source` proves new bounds on the physical source over the entire occupation torus away from zero. Let `U` be the actual unitary weighted collision operator, `z=exp(iv)`, and let `omega` be the displacement/centered-roof frequency. The exact identity is

```
(z^(-1)-1) eta = (U^(-1)-I) 1 + h,
||h||_2 <= C |omega|.
```

It gives the source spectral-window bound `(epsilon+C|omega|)/|z-1|`, the source resolvent bound `[2/(1+r)+C|omega|/(1-r)]/|z-1|`, and the Cesaro source bound `[2/M+C|omega|]/|z-1|`. These are source-vector estimates, not bounds for the full unitary resolvent.

At `omega=0`, the spectral measure of the actual section indicator is exactly `|lambda-1|^2/|z-1|^2` times the spectral measure of the constant function. Thus a pure occupation eigenphase at unit eigenvalue has zero section-to-section residue, even when that eigenphase exists. Absence of every phase is a sufficient but unnecessarily strong requirement for this particular residue.

Theorem `thm:v39-abel-section` gives an exact finite-time second difference for the original section-source transform. It yields bounded collision-clock partial sums and the Abel limit `c z/(1-z)`, with error at most `4(1-r)/|z-1|^2`. It is uniform on every closed occupation-torus complement. The `[0,m)` count and the same initial and terminal section are retained in the algebra.

This is a partial analytical advance on item 1, not its complete resolution. The full signed remainder in `prop:v38-exact-index-remainder` is still a fixed-`m` coefficient with nonzero physical frequencies. Neither its `m^2`-normalized cancellation nor the exact-index Gaussian asymptotic has been proved here. The article gives a finite stationary counterexample to the invalid inference from bounded partial sums to individual coefficient decay; it is not a counterexample to the billiard target.

## 2. Pointwise roof inversion

All common-correction, critical-edge, residual and roof-complement modules remain included. The bound `C(1+|J|)m^(-2)` remains a concentration bound and is not divided by `|J|`. The new source identity does not differentiate a coarea density or control its far roof frequencies. The common pointwise correction and pointwise roof-density theorem remain unclosed in this revision. No averaged object replaces the requested raw density.

## 3. The exact arithmetic obstruction

This item receives a new structural theorem rather than an appeal to physical finite-cover mixing. Define the group of measurable solutions of

```
q o T = exp(i(u.kappa + b tau + v eta + s)) q.
```

The joint positive covariance and local analytic expansion imply a uniform punctured neighborhood containing no such phase. To apply that estimate to merely measurable `q`, the proof approximates only the two bounded endpoint functions in `L1`; the physical record is not smoothed. The approximation is fixed before the collision-count limit.

Products and quotients of phases then make all nonzero differences uniformly separated. Packing in `T^3 x [-B,B]` gives at most `C(1+B)` resonances on a bounded roof band, uniformly in the radius. Complete physical rigidity applies only to the kernel `v=0`; it proves that the occupation projection is injective. It is not applied to a nonzero occupation phase.

Theorem `thm:v39-resonance-structure` concludes that the zero-roof subgroup is finite cyclic of uniformly bounded order. Either that is the whole group, or the roof projection is a single discrete lattice, with a uniform lower spacing bound and an irrational occupation coordinate on a roof generator. The theorem classifies possibilities; it does not assert the existence or exclusion of a nonzero member.

Proposition `prop:v39-induced-arithmetic` gives the exact all-frequency equivalence with

```
q_* o F = exp(i(u.kappa_* + b tau_* + s r_* + v)) q_*.
```

It identifies exactly why ordinary finite lattice-cover mixing does not automatically finish the occupation problem: `v` is a return spectral phase, while `s` multiplies the true collision count. The source cancellation above further distinguishes a phase from a nonzero residue in the required endpoints.

## 4. Orders of limits and uniformity

The inherited roof-band/occupation-strip order is unchanged. The group-separation radius comes from one uniform near-origin expansion, not from a strip width uniform in a growing roof band. Its packing constant is uniform in the radius. The measurable endpoint approximation is removed only after the fixed-frequency time limit. The new Abel estimate states `r` explicitly and is never substituted for the coefficient at `m`. The source resolvent retains the factor `|omega|/(1-r)` rather than declaring it uniformly small on a diffusive scale.

## 5. Bounds versus asymptotics

The four inherited leading theorems remain intact. The new introductory paragraph distinguishes resonance classification, source spectral cancellation, collision-clock partial sums and Abel limits. The exact-index upper bound, diverging-window Gaussian asymptotic, singleton Gaussian asymptotic and pointwise roof theorem retain separate statuses. The manifest does not equate an Abel limit with full occupation-torus coefficient cancellation.

## 6. Independent specialist review

No independent human specialist review has been obtained in this author revision. The new group theorem depends on the inherited joint small-frequency expansion, uniform positive covariance and complete physical phase theorem. The source identities need only the physical invariant measure and the integer-valued section. The audit map distinguishes those dependencies. Source qualification and finite models do not certify the continuum anisotropic imports.

## 7. Generality and novelty

The local-phase-exclusion argument applies whenever smooth-endpoint twisted pairings decay on a punctured joint neighborhood. The discrete-group deduction is then independent of billiard geometry. The source identity and its spectral and Abel consequences hold for any invertible probability-preserving system and any indicator section; they do not assume mixing. These facts are proved directly and are used here for the original Lorentz return source. They are not advertised as new general local-limit theorems or as historical priority claims. The existing theorem-level comparison with collision and suspension LLTs is retained. The DPZ multiplier result remains a one-step input and is not cited as a full-occupation-torus power theorem.

## 8. Submission burden and preservation

The revision retains the four leading theorems rather than adding a new purported singleton theorem. The new proof is placed directly after the exact-return complement, with a short introductory route. All 81 inherited core modules, all 91 inherited Python scripts, the bibliography and A--X appendix are byte-identical. All inherited mathematical labels are checked. Previous main and explanatory sources are preserved under provenance. No historical branch, old report or unrelated paper is modified.

The two v39 branches begin at the controlling v38 review commit. Dynamic qualification receipts identify the actual event SHA, workflow run, source hashes and PDF hash. The successful v38 runs are baseline evidence only; a v39 success is recorded only after the corresponding execution is observed.
