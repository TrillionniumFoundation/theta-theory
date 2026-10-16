# Author response: exact radial coarea and explicit physical horizon

This is an author revision of **Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**, not a new referee report. The original full raw pointwise theorem and four-coordinate inversion target are unchanged. The present result does not establish either final target.

## Frozen source and applicable assessment

Immediate author baseline: `d95f70b68e910e48202da2dae52f92d1b1435fe6`; repository tree `bac734aa0324f383b25f18efea71d078d9b045b5`; native article tree `bc2131c31c0b0590175ea414617a2b23a7d62f3d`; path `papers/A2-DYN-momentum-critical-source-author-revision`. Its complete Library native packet, including the diagnostic omitted in the previous remote tree, was recovered and freshly rebuilt: 78 pages, all ten diagnostic programs run normally and with `-O`, actual command receipts preserved. The old remote CI remains a separate observation, not a local build result.

Controlling assessment: commit `f01482035a0b945b50f1f9c30f30ef35077558dc`, report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`, retained as `provenance/REFEREE_REPORT_v115.md`. It expressly reviews the v114–v115 increment. It is an author-requested AI-assisted assessment, not an independent human or journal-commissioned report. The v112 assessment at `d7fd0b24314d7341f9a611130bb650371d2d5ef2`, blob `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`, remains a historical dependency. No A2 geometry review is used as A2-DYN evidence.

All active bodies 260–285 and the seven original model/interface/audit TeX files remain byte-identical. Bodies 284–285, already present in the baseline, are not new contributions here. The new bodies are **286–287**. Original main, response, ledgers, manifests and preparation-time statements are preserved under `provenance/momentum-*`; their historical wording is not silently updated.

## Actual new mathematical contribution

**Core 286** proves a collision-uniform reduced endpoint metric away from the critical point (`lem:rc-metric`), exact radial roof coarea with its physical normalization (`thm:rc-coarea`), non-asymptotic quadratic critical-band geometry (`lem:rc-band-geometry`), constancy of the limiting physical roof on a connected physical fan (`prop:rc-critical-roof-constancy`), and complete one-copy Borel critical-band/inverse-gradient budgets (`thm:rc-band`). The latter use the retained all-time momentum kernel, with its stated curve-growth dependencies. There is no Taylor remainder to sum in these new band estimates. General Borel cuts do not require a tangent-sector limit. Actual approaches to visited tangencies are covered from the regular side; a derivative or prescribed trace at the singular endpoint is not invented.

**Core 287** proves independently, by a four-direction lattice-row covering, that every physical free-flight length is at most `sqrt(3847/124) < 28/5` (`thm:eh-horizon`). This is a proof for all points, directions and radii in the original family, not a simulation maximum. Exact quadratic-form counting gives enclosing bounds `N_f,N_circ <= 150`, `N_pair <= 162`, `J_f <= 301` and at most `1201` angular first-hit intervals (`cor:eh-counts`). The intrinsic supremum and intrinsic candidate sets are not redefined as their enclosing bounds.

## Point-by-point response to the report

### 1. Recommendation and overall mathematical endpoint
We do not claim that these additions change the assessment into acceptance or prove a top-four-complete raw LLT. The two additions are continuum geometric/proof-completeness results. The original target, rather than a weaker replacement, remains in `model.tex` and `inputs.tex`. No theorem is removed to manufacture closure.

### 2. Frozen source and chronology
The baseline is chosen from actual readable native TeX and a fresh build, not the largest numbered branch. The momentum author and copy refs have the same baseline SHA. Workflow-only v113 and documentation-only successors are not treated as new mathematics. See `REVISION_BASE.json` and `HISTORY_PRESERVATION_AUDIT.md` for exact identities and retrieval limits.

### 3. Qualification evidence
The fresh predecessor qualification is stored separately from current qualification. Current commands, exit codes, tool versions, source hashes, diagnostic results, PDF hashes and typesetting logs are emitted by `tools/qualify_radial.py`. Both normal and optimized runs are required to agree. Source/CI success is not a proof certificate. The previous absent `check_angular_source.py` is restored with its original blob identity; the current source gate requires it, with no missing-file exemption.

### 4. Scope of the audit
The current proof-by-proof reconstruction concerns 286–287 and the precise optical/kernel interfaces used by them. We preserve but do not claim to have independently reconstructed all 259 earlier historical modules, all branches, or the complete spectral/arithmetic chain. This response does not substitute a new referee review for author revision.

### 5. Inherited positive-source obstruction
The original positive source, nongrazing pool and residual identity in 269 are unchanged. The new source estimate is not a new residual definition. It does not assert that low incidence load implies scarcity or that a positive-radius radial cut has zero mass.

### 6. Exact one-mark physical flux
Core 270 is unchanged. Core 287 supplies an explicit enclosing finite-candidate budget for its geometry. The mark is still an unvisited obstacle; no artificial collision is inserted and no real collision is hidden.

### 7. Uniform transverse clearance geometry
Core 271 and its standoff remain unchanged. The horizon proof in 287 is independent of clearance marks. Neither the uniform lower flight bound `3/50` nor the clearance cap `3/200` changes.

### 8. Exact-record disintegration and the missing pointwise bridge
Core 273 is unchanged. In 286, selectors retain initial/terminal section tests, exact `(n,k,m)`, actual roof intervals and the original `nu_R^*`. The synchronized momentum root sum is explicitly distinguished from the same-physical-roof sum evaluated at different branch radii. The latter bridge remains unproved.

### 9. Long-record clearance-to-roof Jacobian
Core 274 is retained. New `eq:rc-gradient` follows by inverting `D_q zeta=R^{-1}DG`, and `eq:rc-coarea-density` cancels the two polar radial factors exactly. The proof audits the factor `4*pi*c_*`, the factor `R`, and the nonzero optical mixed Hessian. Analytic specular derivative tests independently exercise these identities; their finite success does not prove the continuum theorem.

### 10. Finite-type charts and folds
The inherited fold theorem and its hypotheses remain unchanged. New 286 does not assert that all folds are critical-origin arms. It avoids local Taylor errors for its defined actual radial arms, but does not remove the common-roof fold-summation obligation or assign zero mass to positive-radius terminations.

### 11. Critical roofs and reversing periodic trajectories
Core 275 is unchanged, including actual periodic/normal geometry and reversal conventions. New `prop:rc-critical-roof-constancy` proves that the limiting roof is constant on each actual connected fan. The auxiliary difference `L-a` selects a subset only; it is never substituted for physical time `L` in the LLT or record.

### 12. Monodromy coefficient
Core 285 already replaced the critical leading coefficient's pressure dependency using the momentum kernel. That is inherited, not repackaged as current novelty. Core 286 extends the endpoint Hessian bounds away from the critical point, using the same true Schur variational structure. The old coefficient formula and its proof remain present.

### 13. Critical local coarea and boundaries
The old finite-C1 sector result is not overwritten by a false Borel trace theorem. The new Borel result is a non-asymptotic collision-source budget. It needs no boundary-sector limit or third-derivative bound. Its regular-side approach to visited tangencies does not define a trace measure on those tangencies. The distinction is stated in the theorem and its final scope paragraph.

### 14. Same-flight two-mark transversality
Core 276 is unchanged. Core 287 gives `N_pair <= 162` with an explicit enclosing radius and an exact integer table, strengthening the auditability of its finite geometric constant. This does not turn a two-mark theorem into a first-order clearance theorem.

### 15. Ordered two-mark coarea
The ordered mark convention, two signs and normalization in 276 are unchanged. The finite lattice counts are candidate-difference bounds, not numbers of physical words or independent marks.

### 16. Quadratic excess/unique-mark mass
The exact factorial normalization remains unchanged. The current radial band theorem is a different collision-source statement; no quadratic mark estimate is multiplied by `m^2` at fixed outer width and declared negligible.

### 17. Limits of the two-mark result
We retain these limitations. The new all-direction horizon proves a geometric input, not capacity abundance. The new critical-band budget does not pay the entire first-order source.

### 18.1. Complete clearance chart sum
**Partly advanced, not closed.** `lem:rc-metric`, `lem:rc-band-geometry` and `thm:rc-band` eliminate individual Taylor radii/remainders and smooth-cut assumptions for the complete stated radial-arm source family. They hold at every band width and are uniform before the collision/radius/record supremum. Arms terminating at positive momentum radius, general folds, paired traces and the full `m^2 L^infty` roof sum still require estimates. This is not represented as the report's requested complete normalized chart theorem.

### 18.2. Single-mark and cross-flight clearance
Cores 277–283 already supply the real cross-flight source mechanism and its curve-growth argument. They are preserved. No claim is made that an unscaled one-/two-mark mass bound supplies the missing first-order target-roof insertion theorem.

### 18.3. Critical and boundary budgets
**Partly advanced, not closed.** The complete leading regular/finite-C1 sector budget in 285 is inherited. New 286 proves uniform exact critical-band and inverse-gradient budgets for arbitrary Borel selectors, including regular-side singular approaches. The paired minimum of two endpoint traces is not automatically dominated by interior collision density, and the unbounded insertion `I_m` is not silently included in the new inverse-gradient bound. Both transfers remain explicit obligations.

### 18.4. Low-incidence shallow source
**Open.** The original low-load source is not bounded by the new radial theorem in general. No independence, uniform paid fraction or automatic disappearance of its positive mass is asserted.

### 18.5. Nongrazing capacity abundance
**Open.** The pool, its physical normalization and its definition are unchanged. Finite lattice abundance is not comparison capacity abundance. A genuine roofwise comparison or a direct original-source scarcity theorem remains necessary.

### 18.6. Inherited global inputs
**Not independently certified.** The exact Demers–Zhang growth hypothesis and its retained geometric verification are identified in `LITERATURE_AUDIT.md`. Whole-cylinder pressure, full pairing multiplicity and singular trace passage, spectral/arithmetic inversion and conditional denominators have not been certified by the current finite programs or by that external growth lemma.

### 19. Significance at the four-journal benchmark
We provide new complete geometric proofs with exact scope, not a new publication recommendation. Their contribution is the removal of nonquantitative horizon dependence and Taylor/sector dependencies in a real source budget. We do not represent that contribution as a completed top-four-level raw LLT or a substitute scientific objective.

### 20. Required major completion
None of the four requested alternatives—complete normalized clearance, full original-roof insertion, capacity abundance, or direct shortage decay—is claimed completed. The minimum closure remains the unchanged `eq:uc-open-limit` / `eq:v112-remaining`: complete physical source sum, original exact labels and roof essential supremum, `m^2` scaling, the collision limsup with all B-dependent widths fixed, and only then the outer B limit. The precise unproved same-roof and paired-source transfers are displayed at the end of core 286; the ledger records their dependencies rather than renaming the residual.

### 21.1. Paired author/copy refs
The new revision is prepared for paired author and referee-copy refs resolving to one theorem-bearing commit. The post-push receipt, not this preparation-time document, records their actual SHAs. No existing review or author ref is moved.

### 21.2. Preparation metadata and publication facts
`PUBLICATION_STATUS.json` and `REVISION_BASE.json` explicitly describe their preparation-time scope. Actual remote commit/tree/ref and exact-SHA workflow observations are in the separate post-push receipt. Old null/preparation fields remain historical in frozen provenance, not current status claims.

### 21.3. Distinct provenance of increments
270–273, 274–275, 276, 277–280, 281–283, 284–285 and 286–287 are distinguished in the ledger and introductory source history. Only 286–287 are new here.

### 21.4. Explicit horizon and lattice count
**Resolved by a new all-direction proof**, not by inserting a numerical guess. The exact bound is `sqrt(3847/124) < 28/5`; enclosing candidate counts are 150 and 162, and the original intrinsic counts are bounded by them. See `thm:eh-horizon` and the complete integer table in `cor:eh-counts`.

### 21.5. Mark conventions
Ordered/unordered factorial and witness/count conventions are preserved in 276–280. The new integer counts refer only to lattice centers/differences in explicit enclosing disks.

### 21.6. Total variation versus essential roof height
The distinction remains explicit. Neither a total-variation bound, synchronized-momentum density nor a collision-source band mass is used as a same-roof essential-height bound.

### 21.7. Reversal set images
The physical image/preimage convention and exact event in 275 are unchanged. No new event obtained by reversal is substituted for `Pi` in 286.

### 21.8. Local critical component versus global density
The preceding coordinate-ball/sector result retains its original local meaning. The new result is a complete sum over the explicitly defined one-copy arm class, not the whole density near a roof containing other components. Physical fans have their own constant limiting roof; different fans may have different roofs.

### 21.9. Exact-SHA CI
The dedicated workflow verifies the exact checked-out SHA and all required source files before running diagnostics/typesetting. A queued or running workflow is not reported as completed. Local source/build/finite checks are not independent dynamical proof certification.

### 22. Final assessment
The response preserves the original manuscript and all active proof bodies, adds genuine mathematical and proof-completeness results, and makes the still-unclosed raw target precise. It neither deletes the governing theorem nor asserts that the remaining positive source disappears. Independent specialist reconstruction of the load-bearing dynamical chain and completion of the original ordered shortage limit remain necessary for a full mathematical claim.
