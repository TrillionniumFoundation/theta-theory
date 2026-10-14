# Response to the external referee: A2-DYN revision 62

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v60-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Review commit / blob:** `47263fb3033b4545ed3b1e96646f56c9812e7de4` / `5e2f3538ce3d09d3ee1075464f05c2e6354e0709`.  
**Reviewed v60 author source:** `5559cde546c7e3925dfa8706ee499eef93f813f1`.  
**Immediate v61 author baseline:** `3fb563abbef5a119164cc92a360e6e8434e0d92b`.  
**New complete article:** `papers/A2-DYN-v62-referee-response/main.tex`.

We thank the referee for distinguishing the perturbed Markov coarea theorem from the original Lorentz height problem. The source now available includes a complete intervening author revision: v61 proves inverse-incidence cancellation, finite-count incidence gains and transverse clearance coarea. Revision 62 retains that work and addresses its rank-deficient physical clearance source. The title, original problem, exact record and arithmetic reference are unchanged. No older referee report is treated as the latest assessment.

## 24.1. Original Lorentz incidence height

The v61 proof is retained verbatim. In particular, the inverse product of all actual incidence cosines is integrable with finite-count roof height bounded by `C A^m`, and the first-incidence source has width gain `C A^m epsilon`. These are genuine physical bounds but not the ordered `m^2`-scaled height limit requested by the report.

The new caustic reduction also needs to retain a small incidence occurring *after* a first clearance. Its positive pointwise envelope is proved explicitly:

`1_{min_i c_i < chi} <= sum_{i=0}^m chi/c_i <= (m+1) chi I_m`.

Applying the inherited inverse-incidence density theorem bounds this part by `C A^m (m+1) chi`. It is not relabelled as the first-incidence source. Thus the reduction does not erase the later history which the report correctly requires us to keep.

## 24.2. Original next-collision clearance height

This is the principal addition. Module 133 replaces a purely first-order rank cutoff by a derivative along the actual roof level. The total roof is recentered at the original image collision `j+1`, including all backward and forward flights. In a pivot chart the tangent derivative is

`D_i = partial_{i'} - (F_{i'}/F_i) partial_i`.

The full variable coefficient is differentiated at every subsequent order. A divided-difference lemma gives a sublevel-length bound from `|D_i^r Z|>=b`. The physical auxiliary collision graph, augmented by its fixed-order jets, gives `C_r A_r^m` graph pieces with coefficient-independent complexity. Coarea then proves

`ess sup_t sum_{n,k}|b^{epsilon,ft_r(a,b),w}(t)| <= C_r M A_r^m a^(-1)(epsilon/b)^(1/r)`.

At order two this includes a vanishing first clearance derivative on a regular roof fiber; v61's nonzero-Jacobian estimate does not cover such a point. The source failing the finite-type thresholds is kept positively, not assumed empty. The proof uses no continued orbit across a physical seam.

Module 134 gives a further geometric localization. On the closure of original physical words with all incidences at least chi, the exact seam `|Z|=R` and rank equation `det D(F,Z)=0` define a compact caustic in `(R,t)`. The one-flight derivative `partial_phi Z=L_d>=ell_*` forces F to be constant on each connected seam/rank component at a fixed R. The sign-component bound therefore gives at most `C A^m` roof values in each radius fiber. A counting overcover is used only to bound values; no positive source is placed on nonphysical continuations.

A compact semialgebraic separation inequality gives constants `C_{m,chi},N_{m,chi}`. Outside a distance-h neighborhood, when `epsilon<=h^N/(4C)`, the actual determinant is at least `h^N/(2C)`. The complete clearance source minus its retained caustic source consequently has height at most

`C M A^m [(m+1)chi + C_{m,chi} epsilon h^(-N_{m,chi})]`.

The distance is in parameter–roof space, so radius transitions are retained. The cap, selected witness and all exact labels are unchanged.

## 24.3. Unrestricted pointwise theorem

The new corollaries insert the finite-type or caustic positive remainder into the already established raw-error representation. They are complete finite-count theorems, with proofs in the article. They do not claim that the entire retained source has small essential height.

In particular, `A_r^m`, `C_{m,chi}` and `N_{m,chi}` have not been bounded in the ordered central limit required by the report. Taking epsilon exponentially small in m is not a permitted substitute for fixing the auxiliary band, taking the collision-count limit, and then enlarging the band. Both unrestricted Lorentz height flags and the unrestricted pointwise LLT flag therefore remain false. The target theorem and all its arithmetic terms are retained, not downgraded to a different observation topology.

## 24.4. Exact-roof consequences

The finite arithmetic kernel and its zero classes remain in the principal reference. The revision does not assert unrestricted same-roof bridges, forward essential likelihood convergence, or exact-roof path laws on the basis of the new reductions. A separate corollary bounds the *mass* of the explicitly geometric caustic neighborhood using its power tube measure and the inherited weak `L^(145/144)` estimate. Its exponent is `1/145`. That mass bound is not used as a height bound or as permission to delete roof values. Exact-roof densities and conditioning remain almost-everywhere statements in a common disintegration, and no conditional law is assigned to a zero denominator.

## 24.5. Breadth and the positive coarea criterion

This revision follows the physical route rather than claiming a second non-Markov realization. It proves new inputs on the actual circular Lorentz geometry: fixed-order fiber-jet complexity and geometric seam/rank localization. The Markov modules 128–130 are retained verbatim and their successful model theorem is not transferred by analogy. The finite-type estimate explains one additional verifiable mechanism beyond a globally monotone word coordinate; it does not verify uniform finite type at every physical point.

## 24.6. Independent specialist review

No independent human specialist audit is represented as completed. The audit map now identifies the implicit physical jets, graph-interval count, original image-side witness, physical-side seam closure, constant-roof critical components, compact separation inequality and the retained caustic source. The divided-difference, polynomial fixture and source-partition regressions check finite algebra and normalization only. They do not certify the inherited anisotropic operator chain or either ordered Lorentz height limit.

## 24.7. Arithmetic presentation

No Gaussian is substituted for the canonical finite arithmetic reference. All inherited arithmetic-transition, residue and zero-class statements are preserved. The new estimates are positive exact-label bounds and require no residue-triviality claim. Probability total variation remains one half of variation mass in the inherited statements.

## 24.8. Journal proof route and preservation

The article-level synopsis adds the two physical results without expanding the number of leading theorems. Modules 131–134 occur together at the start of the complete-record part. The short route is: the exact first-defect source and one-flight image geometry; the contact determinant and finite-word level graph; the finite-type coarea theorem; then the physical caustic and positive raw-error corollary. The rest of the original paper remains compiled. No historical theorem, proof, Markov calculation or appendix is deleted.

All 132 inherited core modules, 179 inherited scripts, 1761 inherited labels and the compiled A–X synopsis are preserved. The former main file and thirteen other v61 editorial records are archived verbatim. The new bibliography entry is append-only. Source qualification is tied to the new SHA and is not borrowed from the successful v61 run.

## 24.9. Literature comparison

The sublevel estimate uses classical divided differences and Rolle's theorem. The fixed-degree sign-component bound is pinned to Basu–Pollack–Roy, Section 3.2, equation (3.3). The compact separation inequality is Coste's semialgebraic Łojasiewicz theorem, with its exact hypothesis `f=0 implies d=0` checked on the physical-side compact graph. None of those general tools is advertised as new.

The addition within this paper is their use on the *complete original* first-clearance source with exact return labels, image-side marking and later incidences retained. Its geometric remainder is determined by physical seam/rank values rather than by a maximal-function level set defined from the unknown density. This is distinct from the finite-state coefficient argument in v60 and from classical fixed-observable collision or suspension local limits. It is not a claim that the unrestricted Lorentz endpoint or historical-priority question has been settled.

## Technical comments and verification

All thirty technical comments in the report remain applicable to their named inherited statements. The two Markov integer counts, endpoint factor, exact coarea denominator, suffix rewards, positive tilted envelope, Gaussian-tail truncation, count-dependent perturbation range, critical fractional phase and damping constants are untouched. The new physical proofs retain next-collision marking and the original positive source throughout. No finite diagnostic is promoted to continuum proof evidence.

The completed author packet is offered for further substantive review of the finite-type and caustic proofs together with the retained Lorentz program. It is not a journal acceptance, an independent audit or a full pointwise proof certificate.
