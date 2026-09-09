# A2 v3 — uniform thresholds and endpoint curvature recovery

**Uniform collision thresholds and endpoint curvature recovery in periodic dispersing billiards**  
Qian Qi — September 9, 2026.

Branch: `revision/a2-geometric-thresholds-v3-observability-2026-09-09`.  
Controlling review: `fbe11e631e2e8f19eacff804cebbc5496d1fb822`.  
Reviewed manuscript: `daeea828a7666acc42adcabdb9ab9057e9e1bac7`.

## Read the manuscript

`main.tex` is the complete current English article: **31 pages** in the recorded native build. `two_collision.tex` is the unchanged complete companion: **7 pages**. The main article first proves a shortest-channel criterion for arbitrary separated positive-curvature periodic configurations, then a reusable uniform Dirichlet/relative-flux lemma and its physical integration. A new inverse theorem recovers both contact curvatures from two centered Euclidean endpoint variances, uniformly in odd flight number and at equal curvatures. An analytic fixed-amplitude geometric family, finite-offset/sampling bounds and the physical preparation cost make the distinction between count data and record data explicit.

`RESPONSE_TO_REFEREE_V3.md` addresses GTC-R1–GTC-R5 separately. `PROOF_LEDGER_V3.md` identifies hypotheses, proof dependencies and retained results. The restricted exact unlabelled inverse remains, with its area identity and circular coalescence calculation. Smooth-test and transverse moving-cut response remain. Appendices A–G retain the circular hierarchy and its full explicit formulas.

The repository directory is based on the **entire** reviewed v2 native subtree. Original `v2/`, `sections/`, previous report and history subtrees remain. Old publication entry files are also preserved under `history/v2-publication/`. The controlling report is preserved by its exact Git blob in `review-basis-v2/REFEREE_REPORT.md`. The local downloadable package contains the complete native build inputs, PDFs, execution logs and response; it is not a full export of every repository history object.

## Reproduce

With Python 3.10 or later, a full TeX Live installation, NumPy, SciPy and SymPy:

```sh
python build.py
python v3/verify_observability.py > /tmp/a2-v3.json
python -O v3/verify_observability.py > /tmp/a2-v3-O.json
cmp /tmp/a2-v3.json /tmp/a2-v3-O.json
python v2/verify_geometry.py
python tools/verify_thresholds.py
```

The builder compiles both real entrypoints, rejects unresolved references and overfull boxes, verifies auxiliary-file convergence and compares actual recorder inputs with the declared closure. No theorem or reference stubs are used. `verification-v3/NATIVE_BUILD.json` identifies every compiled source. The build preceded the publication commit, so source object hashes—not an invented pre-existing commit—identify its inputs.

`EXECUTION_RECORD.json`, `OBSERVABILITY_CHECKS.json`, inherited replays, `PRESERVATION.json` and `VISUAL_INSPECTION.json` record executed checks and their limits. The new suite has 257 finite checks, and the two inherited suites have 328 and 411; each was executed in ordinary and optimized Python with identical output. Numerical quadrature and grid checks are not interval proofs. All-page thumbnail balance and enlarged samples were visually checked; full-size inspection of every page is not claimed.

The mathematical proofs, not page counts or tests, support the results. This is a new revision for independent assessment, not a claim of journal acceptance, global shape rigidity, an unlabelled noisy inverse at coalescence, or an unrestricted long-time limit theorem.
