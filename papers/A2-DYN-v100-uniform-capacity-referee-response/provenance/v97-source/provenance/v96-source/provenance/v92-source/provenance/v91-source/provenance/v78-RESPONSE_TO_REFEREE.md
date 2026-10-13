# Response to the external report on A2-DYN revision 76

**Author:** Qian Qi. **Revision:** 78, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v76-external-top4-review-2026-10-11/REFEREE_REPORT.md`, commit `fd9875f55291c7804f8dc12f8b73b5886046b168`, blob `6857e4851ff12b7d0828f4eb661152e131fba091`.

**Preserved author baseline:** v77, commit `2d88b8e6cc5dd1ebc72aaec5c77fffb08bf20e2f`, paper tree `dcdbbd9d49cc707bdcf6a1d41066ac26cdfd39b6`. At task initialization the latest visible external report was v76; v77 had already responded to it and completed both qualification runs. This revision builds on that work rather than overwriting it or representing v77 as a new external report.

We thank the referee for requiring an estimate on the complete original source, not merely a reformulation or a per-word optical bound. The title, physical model, exact labels, actual-return interpretation, original section normalization, original guard, all arithmetic classes and original pointwise objective are unchanged. The revision makes a specific complete-source estimate: the guard-distortion contribution is bounded by `C epsilon^{-1} sqrt(r)` in the ordered `m^2` norm. True exits and physical volume distortion are kept separately and are not declared controlled by that result.

## 1. Complete transport estimate — §§15–17 and 20.1

Theorem `thm:v78-separation` proves the estimate just stated. Its argument does not bound the number of words. On each surviving physical state it separates the change of the guard from loss of coarea volume, transfers the guard error with the target-direction Jacobian, and then sums the entire target fiber. The result is bounded by the *unweighted translated target density*. Averaging that target before the collision limit brings the already stated fixed-width input into play; no pointwise unweighted estimate is assumed. This is a complete exact-label bound, not a normalization identity or a fixed-count variation assertion.

Theorem `thm:v78-endpoint` inserts it into the original error. The residual budget contains exactly the original weighted true-exit mass and physical coarea-volume loss. A quantitative power bound for that complete budget remains to be proved. The qualitative ordered criterion is also proved necessary and sufficient under the stated analytic input. We do not declare the primary referee request closed, nor replace the organizing theorem by a smoothed law.

## 2. Explicit field, parameter control and guard drift — §§8,17 and 20.2

The explicit v77 field is unchanged. Module 177 applies the normalized inverse already present in module 140 at arbitrary regular endpoints: all contact first derivatives decay as `q0^depth`, with constants independent of the collision count and all positive internal incidences. This first-order result needs neither the tapered-incidence continuation hypothesis nor a uniform physical neighborhood. Incidences are differentiated as scalar products with physical flight velocities, not by dividing the derivative of momentum by an incidence. Clearances use Hausdorff motion of the physical flight segment, so switching the minimizing third disk does not invalidate the estimate.

Along the explicit forward field the endpoint length is uniformly `O(sqrt(h))`. Summation of the original product guard then gives `|W(Phi_h x)-W(x)| <= K epsilon^{-1} sqrt(h)`. The exponential depth ratio is `q0^(3 depth/4)`, whose complete sum is bounded independently of `m`. The guard is unchanged and need not be monotone. This closes its contribution in the averaged transport estimate; it does not claim a uniform estimate for optical-volume distortion.

## 3. Complete optical sum — §§10–11,16 and 20.3

All per-word optical factors are retained. The new collision-normalized guard argument sums the *physical target measure* through coarea covariance, rather than multiplying a single-word estimate by word cardinality. Every actual word of the exact label is included. This controls one full contribution. A complete pressure or surface-current bound for the remaining geometric contribution is still not supplied, and finite formula complexity is not used as a substitute.

## 4. True exits and regular section decisions — §§5–9,16 and 20.4

Proposition `prop:v78-exit-localization` places every finite forward exit in tapered layers of actual incidence, third-disk clearance or section-edge distance, including initial, internal and terminal tests. Forward critical termination is excluded by the retained field theorem; when all other limiting margins remain positive, the physical word and field continue. The conclusion is a source inclusion, not a pointwise estimate of that layer.

Module 179 gives a further exact treatment of internal section decisions. On a compact regular domain, the sum of the two oriented flux traces is `(z-1) F_D(z)` in the occupation generating variable. The exact `n` coefficient is `F_{D,n-1}-F_{D,n}`. Coincident tests and jumps by more than one visit are included. This identity keeps the labels separately and takes signed sums before absolute values. It does not erase initial/terminal section boundaries, grazing or first-hit transitions. No convergence of separately absolute-valued fluxes on an exhaustion is inferred.

## 5. Critical transport and global scope — §§12–13 and 20.5

The v77 global critical-safe field and positive angular critical residue are preserved with their proofs. Module 177 extends its square-root endpoint motion to every contact and every original guard factor, uniformly across all regular survivors, without selecting or summing Morse radii. Critical points do not become artificial exits. The remaining geometric Jacobian and true boundary terms near critical roofs are not assigned a sign or a uniform concentration bound by this observation.

## 6. Qualification repair and new exact-SHA evidence — §3 and 20.6

The v77 repair is retained: the producer writes `evidence/certify_excursion.json`, and the build passes precisely that path to the byte-preserved `verify_v2.py`. The v77 response run `38112312062` and copy run `38112318836` both succeeded at the frozen v77 SHA. These are baseline results only.

The new v78 workflow qualifies the new SHA, pins the v77 source tree and controlling v76 report, checks preservation and both execution modes, and compiles the complete article and supplement. Its required recorder union is all 179 cores. The complete v77 article is retained in the supplement with scoped reference names to prevent its reused v76 labels from colliding with the earlier article; original source bytes remain in provenance and inherited core files remain unmodified. Actual v78 run results are reported separately, not inferred from the presence of the workflow.

## 7. Specialist audits — 20.7

The new audit map identifies normalized contact response, physical margin derivatives, target coarea covariance, exact signed section flux and arithmetic peak factors. No independent human specialist approval or formal proof certificate is claimed. The full inherited archive is preserved and compiled; that is not a claim to have independently re-proved all 176 prior modules.

## 8. Scalar closure, arithmetic and downstream statements — §18 and 20.8

The scalar-first path remainder and positive-reference restrictions are unchanged. No arithmetic zero class is divided by. Proposition `prop:v78-peak-difference` explicitly retains the leading factor `e^(i v_j)-1` at a nonzero occupation peak. An ordinary index difference does not gain a half power there unless that leading contribution is separately removed. The stated Gaussian hypothesis concerns the surface-current primitive and is not imported from a volume-source multiplier theorem. All spectral bands and physical widths are fixed before the collision limit. Unconditional path, clock and likelihood conclusions are not promoted while the complete geometric estimate is unproved.

## 9. Journal architecture and preservation — §19

The journal contains the unchanged physical formulation, the retained endpoint field and recoupling, and three new theorem-proof modules. It states the concrete complete-source estimate with its exact dependence and distinguishes it from the remaining geometric proof obligation. The supplement preserves the full preceding article and all inherited mathematics. Previous papers, historical records and external review branches are unchanged; no alternative topic, specialist-journal replacement or reduced target is substituted.
