# Audit ledger — independent A2 v63 referee assessment

Date: September 16, 2026. This ledger accompanies `REFEREE_REPORT.md`. It records actual checks and their limits; it is not a proof certificate.

## Frozen objects

Repository: `TrillionniumFoundation/theta-theory`.

- Compiled mathematical source: `f5517519440b897707ddc60deeafba19e86bb5a5`.
- Review-ready head: `ecf359fcaf72e649f0c2a411bdd155bba3c82708`.
- Review-ready repository tree: `c9c715ac0c11bdf5c42bd7fb3c5ca24b0002f013`.
- Manuscript subtree reconstructed from the frozen manifest and source: `b042811c7ceb2c5fd841b2a03ab0b8c232c39dce`.
- Manuscript directory: `papers/A2-v17-boundary-information-coarsening/`.
- Workflow run / attempt / artifact: `35050788011` / `1` / `10428569064`.
- Native artifact SHA-256: `2a2c8d78236274484f1fd3ff6ba905a01ee4eab4c0c2d60e363c5b9670af79ba`, matching the GitHub artifact digest.
- Native source ZIP SHA-256: `e819269bdbf65d38da8369ae9f8aa180aa6422d7b6bea69db6706336b7c09691`.
- v62 baseline source: `037c80dc44d8191e6f808591ea0651e813234d06`; baseline artifact `10427846002`.
- Baseline artifact SHA-256: `e02c1f9bb6cb60ad1cbd08dfd1923f2e92672d52ab97ec7f2e6d10b6da2710bc`.
- Addressed v62 report: `a568573d1d4a5d976f6db3c54122d97c769acd38`.

The actual compiled source is distinct from the workflow preparation SHA. The GitHub comparison from compiled source to review-ready head has three subsequent delivery commits and no compiled mathematical input changes. The finite-experiment module's corrected ending was fetched directly at the compiled source; its Git blob `5b5284c6fffb3ac4be504aa545b1abd647fc2153` matches the downloaded file.

Hash consistency identifies compared content, not authorship, journal endorsement, or mathematical truth. The subtree is reconstructed using modes recorded in the Git source manifest; this does not independently authenticate the entire repository tree or the filesystem permissions produced by ZIP extraction.

## Mathematical reading and exclusions

The entire current finite-experiment module (474 lines) and entire physical position-pilot module (266 lines) were read. The correction, failed-history time accounting, binomial-count conditioning, histogram normalization, measurable realizable-image selector, displaced-cell bounds, and both rate balances were examined directly. The two-ended relative boundary module (386 lines), physical flux interface, and four-density inverse were also re-examined. The active principal introduction and structural statements, shared 53-line comparison, current response, cover letter, dependency ledger, and literature note were checked for consistency.

The complete v59 Banach-space inverse and v60 continuation proof are retained previously scoped inputs, not a new complete audit of those modules. The full earlier finite-chain/full-phase prerequisites, every global matching/lattice and moving-family proof, all graph/support conversions, the complete quartic example, the remaining statistical catalogue, and the companion's mathematics are outside fresh full certification. Page-by-page mechanical reproduction is not a line-by-line proof audit.

Zelditch's published Annals hypothesis and theorem pages (printed 208–209) were checked in parsed text and actual PDF screenshots. The comparison does not conflate the published reversing-involution class with independent evenness of both graphs. Other primary records were checked for the cited scope and correction notices, not for all their proofs or an exhaustive priority search.

## Source and preservation checks

`verify_delivery.py` is an earlier independent referee utility, inspected and freshly executed here; it imports no manuscript checker. It verifies lengths, SHA-256 values and Git blob identities of all **784 frozen files**, reconstructs the manuscript subtree, checks the files listed in the three active-source manifests, and verifies **45 build-report evidence entries** and native product hashes. Active-manifest counts are 116 full, 48 principal and one companion, union **127**. These counts are not an independent semantic proof census or a new theorem-dependency proof.

The separately written `compare_baseline.py` verifies both downloaded source manifests. All 767 baseline paths remain: 759 are unchanged in bytes and recorded mode; eight are changed with byte-exact originals in `history/v62-review-baseline/`. All 126 baseline active paths remain. The only new active path is `article/00d_orbit_local_comparison_v63.tex`. Five lemma/theorem/corollary statement bodies in the finite-experiment module were extracted syntactically and are byte-identical. This does not claim that every proof block was semantically analyzed or counted.

## Fresh builds and visual coverage

A clean copy of the extracted source, with no native generated auxiliaries imported, was built in companion/full/principal order. The command template is

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' ENTRY.tex
```

All builds returned zero. Principal/full/companion page counts are **125/301/7**. All **433 pages** match the delivered PDFs in extracted text and same-renderer **72-dpi RGB arrays**, using PyMuPDF **1.26.7**. PDF bytes differ. Native and fresh SHA-256 values are retained in `AUDIT_RESULTS.json`.

Final logs have no match for undefined references/citations, missing characters, overfull boxes or LaTeX errors. There are three full-manuscript underfull notices, none in the principal or companion. Visual inspection actually covered principal pp. **9, 66, 68, 69** at **108 dpi**. No clipping or unreadable mathematical expression was observed on those pages. All-page computational parity is not all-page visual inspection.

## Independent finite mathematical controls

`independent_checks.py` was newly written for this round, imports no author checker, and uses no removable assertions. Actual output records:

- 100 exact rational grid configurations, 500 onset locations, and 400 worst-duration comparisons, including integral and nonintegral grid lengths and equal gap bounds. The superseded two-epsilon bound fails in 52 configurations; the corrected bound holds in all.
- 1,476 exact multinomial conditional-count factorizations for fixed attempts; 36 numerical evaluations of pilot zero-success/union bounds.
- Four symbolic exponent identities, a symbolic boundary-tube identity, and 12 exact displaced-cell mass inequalities.

Normal and optimized Python outputs are identical. The full emitted JSON SHA-256 is `16aa044178c8808a12f7c9356de8dd7e79884e964e41acc25881d038e2ff4431` in this environment. Floating-point last digits in the numerical probability section can vary across environments. The author's preservation and numerical checker was **not rerun**.

These tests are finite arithmetic/probability controls, not billiard realizations or proofs of infinite-dimensional inversion, trace-class convergence, global continuation, statistical minimax optimality, or the entire risk theorem. The analytic and probabilistic arguments in the report, not finite sample counts, justify the scoped mathematical assessment.

## Reproduction

Use Python 3 with SymPy and PyMuPDF, and a TeX installation with `latexmk` and the manuscript's required packages. Extract artifact `10428569064` into `WORK/artifact/`, then extract its `native-source.zip` into `WORK/source/`, producing `WORK/source/SOURCE_MANIFEST.json` and `WORK/source/source/`. Start without a `WORK/rebuild/` directory. From this review directory run:

```sh
python verify_delivery.py WORK
python verify_delivery.py WORK --build two_collision
python verify_delivery.py WORK --build main
python verify_delivery.py WORK --build rigidity
python verify_delivery.py WORK --compare
python compare_baseline.py BASELINE_ARTIFACT.zip CURRENT_ARTIFACT.zip > SOURCE_DIFF.json
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS_OPTIMIZED.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS_OPTIMIZED.json
```

The comparison script uses the complete artifact ZIPs, not the nested native-source ZIPs. The verifier writes actual reproduction results and retains fresh-build outputs in `WORK`. It makes no network request. The downloadable audit archive additionally retains the actual outputs, fresh build logs, and the four viewed page images from this run.

## Repository changes

The review is placed on a new branch based on the frozen review-ready head. Its files are restricted to `reviews/a2-v63-independent-harsh-top4-2026-09-16/`. Manuscripts, previous reviews, native deliveries, default-branch refs, protections and permissions are not changed. No pull-request approval or merge is implied by this assessment.
