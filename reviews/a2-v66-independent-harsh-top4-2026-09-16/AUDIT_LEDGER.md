# Audit ledger: independent A2 v66 referee assessment

September 16, 2026. This ledger supports `REFEREE_REPORT.md`; it is not a formal proof certificate or a commissioned journal review.

## Frozen provenance

Repository: `TrillionniumFoundation/theta-theory`.

Actual compiled source: `38f798a9b28237420f070a032d3601f0bee72cde`. Its repository tree, from the GitHub commit record, is `9f84161ab64f615400d52e3ddf09252d9c5e3f23`. The manuscript subtree reconstructed from the frozen manifest is `c693d717577dc5f501f2a86ec937cfa36bf6ce4e`, agreeing with the native build record. The source prefix is `papers/A2-v17-boundary-information-coarsening/`.

The completed native-products head used as the review parent is `c11a0427289f88c4c83e3932bd28569ae2c00db8`, on `revision/a2-v66-native-products-35063645908-1`. The source-to-products GitHub comparison has two delivery commits, with additions under the v66 delivery directory and no changed compiled mathematical input. The first discovery snapshot did not list a separate v66 review-ready ref. No such ref is assumed.

Native run `35063645908`, attempt 1, artifact `10433187185`. The workflow preparation SHA `1905e88bf320f5d72d8789bd47567eb83a1fd822` is not the compiled source. Downloaded artifact SHA-256: `81998d447b67fba243b860d639b68e31876a1d8f048f0941c8c2bd41cf628876`. Native source ZIP SHA-256: `71717de6722961d584101ee28c3bc936e32261fbc146fed94c5c44c758677461`.

Previous review: `7f4603531f7b97a23ce627fec47b7ddc5f4f9912`, reviewing v65 source `06a197e4d11bc3d4193e9f0b7904105df35875fa`. The v65 artifact already present in the conversation was extracted as the byte-level baseline, and its source manifest was reverified. The v65 review's complete local report was available in the prior audit archive; the curvature comparison and placement/presentation requests were directly re-read.

The current response and new module were also fetched through GitHub at the compiled SHA. The new module has blob `4ea7cca000a98ea7ac6d48bd9d4f12e5becb94a9`, matching the downloaded bytes. Reconstructing the manuscript tree and comparing manifest hashes does not independently reconstruct the entire repository tree or authenticate authorship/signatures.

## Mathematical coverage

The complete new `article/10c_global_curvature_inverse_v66.tex` (313 lines), common abstract and introductory synthesis were read. All four new statements and proofs were examined. Particular obligations: endpoint multiplicities; the converse from a positive Riccati solution to the actual decaying half-line; positive-orthant contraction; image membership; global versus local inversion; finite-order propagation; and the exact analytic continuation clause.

The direct dependency reading includes v65 graph-coordinate and two-offset arguments (lines 1–202), actual-smooth envelope and signed cyclic blocks (208–346), the protected holomorphic construction (348–454), and the finite-flight/whole-table/conditional-stability interfaces (541–650). The v64 two-ended relative proof at lines 186–359 was re-examined. The earlier complete analytic operator theorem and conditional-continuation lemma are retained inputs, not newly certified in every detail. The opening, response, cover-letter argument, historical audit, and current dependency ledger were checked for scope consistency.

Excluded from a fresh complete proof certification: all earlier finite-chain/full-phase prerequisites, every inherited Banach-space and analytic-continuation proof detail, all unregistered global/lattice and moving-family arguments, the complete statistical and calibration catalogue, and the companion. No claim is made that all 480 pages were checked line by line. No count of distinct mathematical theorems is inferred from source-block preservation.

### R66-m1: finite-iteration propagation

The new report identifies a minor quantitative issue in the final sentence of Proposition 10.4's proof, lines 308–310. Its curvature-only iteration certificate cannot be used as a coefficient-one error bound for every reconstructed higher jet. The report supplies actual local smooth normal-contact profiles, computes the cubic response, and gives an exact control exceeding the raw curvature certificate. The appropriate conclusion is `C_M * (flight error + density error + curvature iteration error)` on the existing compact class. This follows from the preceding smooth finite-jet recursion; the exact-fixed-point proposition and global uniqueness theorem are not refuted.

The response-only a priori/a posteriori terminology is addressed in the same comment, without creating a second mathematical blocker. The importance recommendation is independent of this correction.

## Source and build verification

`verify_delivery.py` is reused from the preceding independent review. It imports no author checker. It checks lengths, SHA-256 values, Git blob identities, recorded modes in the reconstructed subtree, active inputs and build-report evidence. Actual results: 837 frozen files, 123 main inputs, 55 principal inputs, one companion input, 134 distinct active inputs, 45 evidence files. The active per-entry sum exceeds the union because inputs are shared.

`compare_baseline.py` verifies both extracted source manifests, compares bytes and recorded Git modes, and checks archived originals. It found all 818 v65 paths retained: 811 unchanged and seven modified with exact originals. All 131 inherited active paths remain active. The three added active paths are the common abstract, synthesis, and new proof module. The full v64 periodic-forward, v65 periodic-inverse, v62 finite-experiment, v25 pilot, and companion files are unchanged. The result is recorded in `AUDIT_RESULTS.json` and full `SOURCE_DIFF.json` in the audit package.

Fresh compilation was performed in a clean copy of the frozen manuscript source, without copying native auxiliary outputs into that copy. Build order: companion, full manuscript, principal article. All builds disabled shell escape and succeeded. Final products have 7, 324 and 149 pages, respectively. All 480 pages match the native outputs in extracted text and same-renderer 72-dpi RGB arrays. PDF byte identity is false. The full log has four underfull-box notices; the principal and companion have none. No final-log match for undefined references/citations, missing characters, overfull boxes or LaTeX errors was found.

Actual direct visual inspection was of principal pp. 2, 45, 46, 47 and 48, rendered at 108 dpi. No clipping or unreadable formula was observed on those pages. All-page render comparison is not all-page visual inspection. The initial attempted streaming build invocation was unsupported by the container; the actual builds were then completed with ordinary synchronous calls. This did not require changing the source or reusing native auxiliaries.

## Independent mathematical diagnostics

`independent_checks.py` uses Python fractions and mpmath; it imports no author code and uses no removable assertions. Exact rational test data are independently generated from positive periodic Jacobi contractions, with their corresponding curvature and action data. The program checks the Schur recurrence, inverse iteration bounds from three initializations, two-point inverse inequalities, terminal-tail elimination and finite Dirichlet comparisons. It also includes nonimage, nonmonotone, boundary, and stopping-error amplification controls.

Actual counts: 56 rational data sets (periods 2–8), 1,176 iteration-error inequalities, 57 two-point inverse inequalities, 168 exact terminal-tail eliminations and 168 finite Dirichlet comparisons. Endpoint double-count tests are elementary algebraic controls, not independent geometric experiments. Eight 70-digit numerical cases check inversion and the curvature differential against centered differences; three normal two-site cases and a nonnegative boundary datum are included. The source code and results state that arbitrary rational Jacobi coefficients are not claimed to be realized by global billiard tables.

Normal and optimized Python runs emitted identical JSON. SHA-256 of the full emitted JSON: `af20b653964ffdb222d76c26ac30b68abe85834ddfb5eda6635a26f16e691a1e`. High-precision discrepancies are finite numerical checks, not certified analytic error bounds. The author's current preservation/mathematical checker was not rerun.

## Primary-source checks

The author-hosted Bálint–De Simoi–Kaloshin–Leguil PDF was opened through web tools and printed pp. 9–10 were viewed using the PDF screenshot tool, including Theorem D, Corollary E and Remark 2.3. Bolotin–Treschev's arXiv PDF was opened and printed p. 12, containing Theorem 2.1 and orientation discussion, was viewed. The primary arXiv records of De Simoi–Kaloshin–Leguil, Finamore–Leguil and Florio–Leguil v5 were refreshed for their observation assumptions and correction notice. Their URLs and bibliographic data are in the report. No claim of a complete literature proof audit or exhaustive priority search is made.

## Reproduction

Extract native artifact `10433187185` into `WORK/artifact/`. Extract its `native-source.zip` into `WORK/source/`, producing `WORK/source/SOURCE_MANIFEST.json` and `WORK/source/source/`. For the baseline comparison, extract the v65 source ZIP into `WORK/baseline/` and place its active-source manifest at `WORK/baseline/active-source-manifest.json`.

From the review directory, using Python 3, mpmath, PyMuPDF, latexmk, pdflatex and the manuscript's required TeX packages:

```sh
python verify_delivery.py WORK
python compare_baseline.py WORK
python verify_delivery.py WORK --build two_collision
python verify_delivery.py WORK --build main
python verify_delivery.py WORK --build rigidity
python verify_delivery.py WORK --compare
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

Begin with no existing `WORK/rebuild/` for a fresh compilation audit. The verifier emits `REPRODUCTION_RESULTS.json` and retains build outputs in `WORK`; the comparator emits `SOURCE_DIFF.json`. These utilities make no network requests. New PDF file hashes depend on the fresh build and are not expected to be identical across environments or timestamps.

Only this review directory is added on the new review branch. No manuscript source, old report, native delivery, default-branch ref or repository permission is changed. No pull-request approval, journal endorsement, or merge is implied.
