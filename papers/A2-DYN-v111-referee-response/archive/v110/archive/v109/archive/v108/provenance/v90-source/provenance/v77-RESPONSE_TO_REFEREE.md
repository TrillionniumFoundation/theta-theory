# Response to the external report on A2-DYN revision 76

**Author:** Qian Qi. **Revision:** 77, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v76-external-top4-review-2026-10-11/REFEREE_REPORT.md`, at `fd9875f55291c7804f8dc12f8b73b5886046b168`, blob `6857e4851ff12b7d0828f4eb661152e131fba091`.

We thank the referee for separating the correct local transport and optical arguments from the unproved complete-source estimate. We retain the original raw pointwise local limit problem, its complete exact labels, the original section normalization and guard, all arithmetic classes, and the established order of limits. This revision adds three proof modules without deleting or changing any of the 173 inherited mathematical modules. The full preceding journal article is reproduced in the supplement and preserved verbatim in provenance.

## 1. Complete transport estimate — report §§15–17 and 20.1

We replace unspecified field choice by the explicit field in Theorem `thm:v77-field`, and construct a more permissive *angle-preserving* subcoupling after the full physical word sum. The new observable is the physical momentum angle `theta=arg(-p0,pm)`, not a cap normal. Formula `eq:v77-angular-sum` is an exact coarea sum over actual states of the unchanged exact event. Theorem `thm:v77-recoupling` proves that the unmatched mass is the integral of the positive difference of the two **complete** angular densities. It is no greater than the forward stopped-flow defect for our explicit field. It can recover genuine word exits when another actual state with the same label and angle supplies matching target mass. It neither pools labels nor splices nonphysical trajectories.

Theorem `thm:v77-persistence` and Theorem `thm:v77-closure` insert this complete angular defect into the original ordered scalar error. The organizing pointwise theorem still requires the collision-normalized bound `eq:v77-remaining`. We have **not proved that bound**. Accordingly this principal request is advanced but not closed. We do not replace it by the integrated normalization or by finite-count variation. The new estimate is a sufficient route on the unchanged source, not an assertion that all prior two-sided scalar moduli are larger.

## 2. Explicit roof field — report §§8,17 and 20.2

Module 174 proves the endpoint-angle Hessian inequality

`R diag(c0,cm) <= K <= (47/6) I`.

Both endpoints belong to the unchanged section, where `|p|<9/10`. Thus `lambda0 I <= K <= Lambda0 I` with `lambda0=9 sqrt(19)/200`, `Lambda0=47/6`, uniformly in collision count, radius, exact labels, all internal incidences and all positive clearances. The proof differentiates the physical supporting action for the lower bound and uses the fixed-internal-contact trial form for the upper bound. It does not infer convexity of a disconnected physical domain.

The field is uniquely defined by `XL=1`, `X theta=0`, equivalently `Xq=K^{-1}g/(g^T K^{-1}g)`. It is a formula on physical states and uses neither the unknown scalar density nor the guard. Endpoint-angle lifts differ only by translations, so there is no cap partition or partition-of-unity construction. The field exists on every regular exact-event state away from its critical set.

The radial and endpoint-motion estimates are collision-uniform. True physical boundaries still stop the flow. Uniform lifetime or weighted divergence through those boundaries has **not** been inferred from the motion estimate. Formula `eq:v77-drift-formula` displays precisely the remaining third-derivative and amplitude terms; its cancellation removes the quadratic constant-density divergence, but its local derivative constants are not declared collision-uniform.

## 3. Full optical sum — report §§10–11,16 and 20.3

Module 175 retains the positive optical recursion and simultaneous incidence factors in every term of the actual coarea sum. The exact identity `eq:v77-angular-total` sums all true words before integration and gives the original weighted source mass, at most one. It is a genuine integrated summability identity, not a word-cardinality estimate.

At fixed count, the physical graph gives finite inverse fibers and a definable angular threshold density. Module 176 proves finite roof variation for the angular density before scalar projection. Its constants `N_m,J_m,C_m` are explicitly kept as fixed-count constants. Neither the integrated identity nor this finiteness provides an `m^{-2}` local pressure or concentration estimate. The dynamically normalized part of this request remains open.

## 4. True boundary exits — report §§5–9,16 and 20.4

The new coupling takes its marginals from the full original source at both roofs. Any mass not matched at the same exact label and physical angle is charged to `Delta`. The angular current formula `eq:v77-angular-flux` contains the physical bulk divergence and oriented true boundary flux. Artificial chart interfaces cancel because they carry the same physical state and opposite orientations. True singular, first-hit and section-decision boundaries are not erased by a null-set argument. Incoming and outgoing *actual* mass can cancel only after their signed pushforward at the same angle and label.

Distributional convergence under exhaustion is proved from convergence of omitted source mass. Finite variation of the resulting complete current is proved separately by the threshold argument. No total-variation convergence of separately absolute-valued exhaustion terms is claimed. The collision-uniform negative-current strip bound remains unproved.

## 5. Critical transport without collision-dependent collars — report §§12–13 and 20.5

The new field has `d|g|^2/dh` between `2 lambda0` and `2 Lambda0` on every forward survivor. Hence a forward orbit cannot reach an interior critical point. Its endpoint-angle length and both endpoint momentum displacements are `O(sqrt(h))` with constants independent of the word or a Morse radius. These conclusions hold on the entire regular exact event; they do not require summing a family of local radii or gluing local fields.

Proposition `prop:v77-angular-residue` also computes the positive angular critical entrance profile and recovers the exact scalar jump after integration. A neighborhood is used only to compute that local residue, not as a width in the collision limit. The third derivatives, angular amplitudes and true boundary contributions near critical regions still require a complete quantitative concentration estimate. The global construction and favorable critical direction are proved; uniform summed distortion is not.

## 6. Exact-SHA qualification — report §3 and 20.6

The historical `tools/verify_v2.py` remains byte-identical. The revised build explicitly calls it with `evidence/certify_excursion.json`, exactly the file written by its producer. No alias, ignored failure or skipped supplement is introduced. All six inherited diagnostic scripts and the new and recent finite fixtures are checked in normal and optimized Python. Both modes must agree.

The new exact-SHA workflow pins the v76 paper tree and the controlling v76 report blob, checks all inherited source bytes, compiles the article and complete 173-core supplement, and checks actual recorder coverage of all 176 active modules. Local archive builds are explicitly distinguished from exact remote checkout runs. A source change implementing these checks is not itself a passing-run claim; the actual run result and source SHA are reported separately as generated evidence.

## 7. Independent audits — report 20.7

`SPECIALIST_AUDIT.md` identifies the physical support/Hessian argument, global angle observable, coarea multiplicities, maximal same-angle coupling, signed angular current, critical residues, and the inherited scalar/spectral interfaces for specialist review. No independent human reviewer has been represented as having approved them. Finite algebra and builds are not proof certificates.

## 8. Downstream normalization — report §18 and 20.8

Module 176 retains the same positive path remainder with scalar mass `m^2 b`. Its bounded-Lipschitz norm is controlled only after scalar closure. Path ratios are restricted to classes with a positive scalar-reference lower bound; arithmetic zero classes are never normalized. Clock transfer and likelihood retain their separate inherited assumptions. None is promoted to an unconditional theorem while `eq:v77-remaining` is unproved.

## 9. Journal presentation and preservation — report §19

The article retains its title, physical model, complete record and principal objective. The new results are organized as definitions, lemmas, theorems and proofs with explicit constants and dependence statements. The full previous mathematical article, all historical proofs, bibliographies, appendices and Python sources are preserved; no other paper directory is edited. `SOURCE_MANIFEST.json` is the current authority for the status of each assertion.
