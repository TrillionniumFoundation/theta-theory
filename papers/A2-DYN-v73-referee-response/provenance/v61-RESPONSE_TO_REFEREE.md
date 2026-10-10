# Response to the v60 external referee: A2-DYN revision 61

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v60-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Review commit / report blob:** `47263fb3033b4545ed3b1e96646f56c9812e7de4` / `5e2f3538ce3d09d3ee1075464f05c2e6354e0709`.  
**Reviewed author commit:** `5559cde546c7e3925dfa8706ee499eef93f813f1`.  
**Frozen complete v60 paper tree:** `a0c6bac46a3022b8d66b077816d770dbcd55d79b`.  
**Revised manuscript:** `papers/A2-DYN-v61-referee-response/main.tex`.

We thank the referee for distinguishing the perturbed Markov theorem from the remaining Lorentz height problem. This revision returns directly to the original circular Lorentz source. It does not add another model or present the abstract criterion as a verification of its own hypotheses. Two new sections establish physical coarea estimates at every finite collision count. They retain the exponential count dependence, so they are advances toward the requested essential-height limits, not claims that those limits have already been established.

The title, exact four-coordinate record, full arithmetic transition kernel, and unrestricted two-sided pointwise objective remain unchanged. All 130 inherited core modules, all 175 inherited Python files, the bibliography, and compiled appendices are retained byte-for-byte. All 1742 inherited mathematical labels remain. The former main source and thirteen other editorial/provenance files are archived verbatim.

## 24.1 Lorentz incidence height

**New result:** Theorem `thm:v61-inverse-incidence-density` proves that the unbounded original-orbit insertion

`I_m = product_{j=0}^m cos(phi o T^j)^(-1)`

is integrable, and its full roof pushforward has essential height at most `C A^m`, uniformly in the radius. It simultaneously controls any product with incidence exponents in `[0,1]`, and includes a sum over the exact return/displacement labels. This is not an estimate of a smoothed or relabelled source.

The proof uses the actual endpoint action. Its cross derivative is

`|F_uv| = c_0 c_m product(t_j) / det(A)`,

where `A` is the internal tridiagonal contact matrix. Writing `A=L+D`, with `L` a nonnegative Dirichlet path Laplacian and `D_jj=2/(R c_j)`, gives `det(A)>=product(2/(R c_j))`. Thus every inverse incidence cancels in the endpoint density, including both endpoint factors. The remaining density is bounded exponentially in the word length. The existing coefficient-independent level-complexity estimate, extended explicitly to endpoint coordinate slices, and positive curvature near normal endpoints give a full coarea bound. Arbitrarily small positive interior incidence is included by exhaustion, without crossing a singularity.

Lemma `lem:v61-determinant-gain` also proves the selected-contact ratio

`det(A^(S))/det(A) <= product_{j in S} 53 c_j/(6+47 c_j)`.

The comparison matrix changes only diagonal potentials in an algebraic inequality; it is not identified with a hypothetical physical replacement orbit.

Corollary `cor:v61-incidence-height-gain` applies this to the **original first-physical-incidence source**, including guard transitions. It proves

`ess sup_t sum_{n,k} |b_inc^(epsilon,w)(t)| <= C M A^m epsilon`.

The depth sum is geometric, so there is no additional factor equal to the number of contacts. Simultaneous specified small-incidence conditions gain the product of their widths. Bounded insertions are dominated before pushforward.

**Not yet closed:** at fixed `epsilon`, `m^2 A^m epsilon` need not vanish. The theorem gives genuine density control and unbounded same-roof incidence moments, but it is not the central-scale incidence limit required in the report. That status remains false.

## 24.2 Lorentz clearance height

**New result:** Section `sec:v61-clearance-coarea` works with the actual first defective flight and its responsible nonincident disk. Its clearance coordinate is `Z_d o T^(j+1)`, with the next-collision convention retained even at the final flight. It splits the complete positive clearance source according to

`|det D_(alpha,p)(L_m,Z_d o T^(j+1))| >= eta`

or its complement. The two source pieces sum exactly to the old clearance source. The rank-deficient piece is not discarded.

Theorem `thm:v61-transverse-clearance` proves the essential-height bound

`ess sup_t sum_{n,k} |b_tr^(epsilon,eta,w)(t)| <= C M A^m epsilon/eta`.

This follows from the two-dimensional area formula on the original physical graph. A nonzero-rank fiber is isolated. The bounded-degree auxiliary collision graph gives an exponential multiplicity bound before any elimination. Integrating the second coordinate over its actual thin clearance interval supplies its width, and summing the geometric flight-depth widths retains a constant independent of the number of marks. All exact-label restrictions and the first-defect guard are preserved in the source; their removal is used only for a positive upper comparison.

**Not yet closed:** the rank-deficient clearance source has no new essential-height bound. In particular a normal-to-normal critical word has zero roof differential, so a clearance defect there belongs to the retained piece. The proof does not sweep such a word across the physical competing-hit seam.

## 24.3 Unrestricted pointwise theorem

Equation `eq:v61-rank-localized-error` combines the new physical bounds with the old positive raw-error representation. Its finite error budget is explicit:

`e_(B,m) + C m^2 A^m epsilon(B) (1+eta^(-1))`,

after retaining the positive rank-deficient clearance term. For each fixed band the inherited `e_(B,m)` has limsup `C B^(-1/192)`. No interchange of the collision and band limits is made. In particular, exponentially increasing the band to defeat the new count factor is not justified by a fixed-band spectral theorem. The full pointwise theorem is therefore not marked proved.

The new results reduce neither the record nor the requested topology. They identify explicit geometric mechanisms and the remaining count/rank estimates for the same positive sources.

## 24.4 Unrestricted consequences

The existing pointwise lower law allows division at the **same original roof** on a class with canonical reference at least `d>0`. The resulting finite-count incidence probability bound is `C_d m^2 A^m epsilon`; its scope is stated exactly. Arithmetic zero classes receive no denominator. Unrestricted same-roof bridges, forward essential likelihood and pointwise conditioned path laws remain unasserted until the original height requirements are met.

## 24.5 Breadth and the original topic

No further baker or surrogate system is introduced. The two new theorems are proved on the original Lorentz table. The previous perturbed Markov coarea and pressure-contact results remain compiled and retain their original scope. They are not counted as multiple non-Markov realizations and are not used to verify a Lorentz geometric hypothesis by analogy.

## 24.6 Specialist audit

No independent human audit has been obtained. `SPECIALIST_AUDIT_MAP.md` identifies the new checks: the contact Schur complement away from critical endpoints, simultaneous incidence cancellation, endpoint level complexity, unbounded-source integrability, the isolated-fiber count, the physical witness assignment, and the next-collision mark. The inherited anisotropic, arithmetic and Markov audits remain separate. Native compilation and finite checks certify none of these continuum arguments.

## 24.7 Arithmetic presentation

Every old finite arithmetic phase, damped residue and zero class remains in the principal statements. The geometric estimates are positive source bounds and do not replace the canonical reference by an unmodulated Gaussian. No residue-triviality theorem is claimed.

## 24.8 Proof route and preservation

The new physical sections appear first in Part I. Their short route is the endpoint action/complexity of module 94, the exact contact determinant of module 96, and the original next-collision clearance envelope of module 105. The reader need not pass through the independent Markov calculation to inspect them. All earlier mathematics remains compiled. The preceding main source, response, ledger, status and validation records are preserved in provenance rather than silently overwritten in history.

## 24.9 Literature comparison

The area/coarea formula and determinant monotonicity are not new general principles. The new statements concern their complete, exact-label use with the unbounded product of inverse physical incidences and with the true competing-hit coordinate of this Lorentz family. Their count dependence is stated, not hidden in a uniform-limit claim. Classical billiard cell local limits, endpoint mixing local limits and suspension local-limit theory are retained as background; none is cited as already proving either missing essential-height limit. The finite-state literature comparison and every qualifier of the v60 Markov theorem are unchanged.

## Technical comments and evidence

All thirty technical comments in Section 25 are respected in their inherited statements: the two integer counts, terminal-state factor, positive tilted bound, truncated Gaussian tails, cylinder-depth restriction, joining state, coarea denominator, both endpoint intervals, arithmetic profile, critical fractional phase, probability-TV convention and almost-everywhere qualifiers remain verbatim. For the new bounds, threshold uniformity and the exponential collision-count constants appear beside the inequalities. The ordinary source verifier checks all inherited identities and labels, and the new finite tests include endpoint factors, contact Schur complements, selected-contact ratios, geometric depth sums and two-coordinate area calculations. Negative controls explicitly retain the failure of a mass-to-height inference at rank loss and of a one-branch formula when multiplicity is two.

Both new dated revision branches are based on the frozen v60 report commit. Their read-only qualification workflow records the exact source tree, event SHA, run and attempt, PDF hash and rendered theorem pages. Success is an execution fact reported only after the run finishes; it is not a mathematical proof certificate.
