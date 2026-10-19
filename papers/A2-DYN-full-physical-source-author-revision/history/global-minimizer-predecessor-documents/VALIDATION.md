# Validation and reproducibility record

This file explains what the actual command records verify. Every mathematical claim is supported by its native proof body and dependency statement; neither these programs nor a successful workflow is a continuum-proof certificate.

## Current completed local executions

| Execution | Actual result | Evidence |
|---|---|---|
| Recovered complete predecessor native paper | Three pdfLaTeX passes succeeded; 127 pages; no unresolved or overfull diagnostics | evidence/current-execution/predecessor-native-recovery/PREDECESSOR_NATIVE_REBUILD.json |
| Current complete new native paper | Three pdfLaTeX passes and pdfinfo succeeded; 147 pages; no undefined references/citations, duplicate labels, overfull boxes or missing glyphs | evidence/current-execution/recovered-native-typeset/native-typeset.json |
| Complete finite mathematical suite | 19 programs in normal and optimized Python, 38 actual commands; all passed; corresponding stdout/details byte-identical | evidence/current-execution/recovered-complete-math/mathematical-checks.json |
| Current six-body localization verifier | Normal and optimized executions succeeded with identical corresponding outputs; all six current body hashes checked | evidence/current-execution/recovered-localization/receipt.json |
| Historical original native assembly | Original assembler, six pdfLaTeX passes and two pdfinfo reads succeeded; clean 26-page main and 883-page supplement | evidence/current-execution/historical-recovery/20261018T164336583551Z/REBUILD_RECEIPT.json |
| Exact inherited source identity | All 699 original Git blobs, 1178 retained paths, byte length/SHA-256/Git SHA matched | audit/recovery/KNOWN_GIT_BLOB_RESTORE.json |
| Current proof navigation | 59 source files, all 50 core bodies included once, 691 labels and actual PDF destinations verified | PROOF_INDEX.json |

The current main source has SHA-256 **84f3c43cd538c6f377b20bdb49a0cf2aa8a002e8eca7aa0196d3e59a967d57b1**. The first clean recovered current PDF has SHA-256 **dcdb6209a19210fc286706d08c61919816adb54cfcd205aa22279bc4c3005991**; its aux SHA-256 is **5b09b45509c710c713e2a9684c519413e8f789502f172f0003fade9b50282d73**. Later builds of the same source may change PDF metadata and hash. Their own receipt, rather than this earlier fingerprint, identifies each output.

The complete suite and that first typesetting run used mathematical-source fingerprint **5cc7dfc81194a1206c5d940ad210f83f43412fde6438fbcfc7def16008a65030**, whose file list is in both receipts. The proof-index tool and manifest output exclusions were subsequently finalized. The final all-phase execution is retained separately under evidence/current-execution/final-complete; it records the actual final tool/source fingerprint and source-manifest verification. No earlier fingerprint is relabeled as its own.

## What the new verifier checks

The program tools/verify_localization.py has explicit failure gates that remain active under Python optimization. It evaluates the exact rational coefficient and integer-index arguments and separately performs finite floating diagnostics on the original physical disks. It records its own and all six current mathematical source hashes.

Its exact coverage includes:

- Cutoff Young coefficients, variation signs, one shared positive gap, endpoint deficit, deep-energy normalization and nonlinear \(d^{-3}\) recurrence.
- The interior anchor threshold, hard-interval cut work, both boundary flights and the shared-flight case.
- The 94-collision layer indexing, empty intervals and the retained central singleton.
- Contact, direction and square-transverse coefficient comparisons; the original \(R_-\), \(r\), \(\tau_-\), \(C\), \(N\) and \(a_0\) remain fixed.
- The physical clock boundary term and phase estimate's repeated terminal incoming edge.
- Exact section-collar coefficient and single section normalization.
- Three exponential source tails and their integer depth schedules.
- The \(m^2/d^3\) rate and exponential frequency range for specified original-roof costs.
- Exact rational enclosure of the logarithmic threshold: \(J_{\rm obs}=149881785\), \(D_{\rm obs}=14088887790\). These conservative finite constants are not practical-time claims and are not replacements for the original guard \(q_0=47/53\).

The actual recorded counts include 360 hard intervals, 167 anchor layers and 130305 incoming-phase index cases. The finite numerical part includes 15 original physical records with an exactly identified alternating-word global minimum, 861 closed-segment all-center strip diagnostics, 33 central clock/phase comparisons and 42 point-phase comparisons. These sample counts are taken from executed output. They do not quantify the continuum of all physical trajectories.

Two negative controls are substantive. A feasible but nonminimal comparison violates the supposed cutoff conclusion when global minimality is dropped. An actual clock diagnostic violates the bound obtained by deleting endpoint work. The program requires both controls to reject those incorrect simplifications.

The native proofs establish the uniform statements; exact finite checks verify their displayed arithmetic/indices, while floating diagnostics provide reproducible implementation checks. They cannot establish full singular trajectories, source height, pressure, capacity or the raw pointwise LLT.

## Inherited mathematical checks

The retained suite executes these unchanged inherited programs:

check_finite, check_research, check_load, check_clearance, check_critical_coarea, check_two_mark, check_cross_flight, check_angular_source, check_uniform_growth, check_momentum_critical, check_radial_coarea, check_endpoint_localization, check_reflection_resolvent, check_physical_tubes, check_critical_clock, check_global_variational, check_sublevel, and check_summable_source.

The nineteenth program is the new localization verifier. Every command line, working directory, UTC start/end, exit status, source identity and output hash is saved. Normal/optimized outputs are compared after the commands actually finish. An absent output, nonzero command or differing comparison fails the gate. Parallel execution does not drop errors from another job.

## Native typesetting and visual inspection

The current driver performs three actual pdfLaTeX passes and a pdfinfo read. It checks the final log and rejects unresolved references, duplicate labels, overfull boxes and missing glyphs. Two retained AMS advisories about foreign commands (\(\backslash\)atopwithdelims and \(\backslash\)over) are recorded; they are not misreported as unresolved references or successful mathematical tests.

All 147 pages were rendered into a contact sheet and visually inspected after recovery. Full-size pages 1, 123 and 128 were also inspected for title/abstract readability, the anchor-layer proof, the logarithmic threshold, exceptional-source definition and full-source theorem. The rendered temporary PNGs were safely removed during disk recovery; the actual PDF remains available and regenerates the same layout. No visual pass is treated as a proof of an inequality.

The proof navigation checks actual named PDF destinations, not merely aux labels. Three inherited labels have a one-page aux/destination discrepancy; both values are recorded, and the heading was checked on the real destination page. The new proof locators are based on this current compilation, not the lost previous 104-label index.

## Honest historical failures and successful reconstruction

The old predecessor's 982-entry source manifest included 881 unavailable entries. Its workflow at fb99e4d67ef74912f6c69b05c9abff3207572e7a failed. Rebuilding its 103 actual native files does not convert that archival qualification into a success.

During recovery, the first historical build failed because SymPy was missing. The next wrapper execution returned successful commands but exposed nine unresolved cross-document references when main was compiled before its supplement. That result is marked as a quality failure. The corrected helper builds the supplement first, uses the original assembler unchanged, checks the source identity and rejects reference/layout faults; its next actual clean execution produced the 26/883-page pair. The failed attempts and their assessment remain in evidence/current-execution/historical-recovery.

The pre-maintenance successful 147-page PDF and manifest have different identities and lost execution bytes. They are described only as prior observed results in MAINTENANCE_RECOVERY_AUDIT.md. New logs are not fabricated as recovered old logs.

## Current source verification and publication separation

The frozen SOURCE_MANIFEST.json covers current inputs, original source and retained audits. Generated build directories, current execution outputs, delivery outputs, proof navigation and post-publication status receipts are excluded from input hashing to avoid self-referential manifests. The transport manifest separately covers delivered files, including those outputs.

The helper verifies the immutable inherited anchor before comparing current membership and every current input hash. It never silently updates an old source hash. The final source check also verifies full TeX closure, each core's single inclusion, report identities and the false status of the uncompleted final raw LLT/inversion.

Only the new article directory and dedicated workflow are added to the fixed parent tree. Actual ref readbacks, tree isolation checks and the current workflow outcome belong to PUBLICATION_STATUS.json and delivery/publication. An author/referee-copy alias is not a review. A workflow that merely freezes metadata or skips the native build is not complete-manuscript CI.

## Reproduction

~~~bash
python3 -m pip install -r requirements.txt
bash build.sh
~~~

For separate stages:

~~~bash
python3 tools/package_source_manifest.py . verify
python3 tools/validate_revision.py source --output build/current
python3 tools/validate_revision.py math --output build/current
python3 tools/validate_revision.py typeset --output build/current
python3 history/historical-v108/rebuild_history.py
~~~

The local restored interpreter is Python 3.12.14, with numpy 2.3.5, scipy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0. The dedicated GitHub workflow pins Python 3.11 and records its actual dependency and TeX versions. The final mathematical status remains independent of which of these reproducibility checks succeeds.
