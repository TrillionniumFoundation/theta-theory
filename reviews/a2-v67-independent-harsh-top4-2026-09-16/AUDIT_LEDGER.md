# Audit ledger: independent A2 v67 review

Review date: September 16, 2026. This ledger accompanies `REFEREE_REPORT.md` and `AUDIT_RESULTS.json`. It is not a formal proof certificate.

## 1. Frozen provenance and read scope

Repository: `TrillionniumFoundation/theta-theory`.

| Object | Identity |
|---|---|
| Actual compiled source | `97b0c5bf15d6581c42b0f503bbe902c9d89b42db` |
| Reconstructed manuscript subtree | `5ba7cc8f87aaadd2e3f734c41bb030668e15cff7` |
| Referee-ready head / review parent | `c5633d2e4d4f2d7c2b34d4b05f9440fdc5a18591` |
| Referee-ready root tree | `298e3f1b1ce07b4b81d70b7058ff1b1b736d726f` |
| Source branch | `revision/a2-v67-relative-law-mechanism-2026-09-16` |
| Referee-ready branch | `revision/a2-v67-referee-ready-2026-09-16` |
| Native run / attempt / artifact | `35074257415` / `1` / `10437417575` |
| Workflow trigger, not compiled source | `08cbb69253a9abaada060336bac0a5d6beba08c6` |
| v66 baseline source | `38f798a9b28237420f070a032d3601f0bee72cde` |
| v66 baseline manuscript subtree | `c693d717577dc5f501f2a86ec937cfa36bf6ce4e` |
| v66 report | `3d49684cc6c9bad36d80c99dc46af276f53fae18` |
| Baseline artifact | `10433187185` |

The v67 artifact SHA-256 is `0be6400d1d4861df61a5a5396846cbdeca6faa18e19f17b68db85b494e847631`. Its frozen `native-source.zip` SHA-256 is `ce680676e981c88c291db440926d960c159184cb8db4a58b7a4fbb79f1bbf498`. The v66 artifact SHA-256 is `81998d447b67fba243b860d639b68e31876a1d8f048f0941c8c2bd41cf628876`.

GitHub branch discovery identified v67 as the newest revision at the opening snapshot. The six commits between the compiled source and the pinned referee-ready head add delivery/verification material and change the root entry point; they change no compiled mathematical input. The corrected module was fetched directly at the compiled commit as well as read in the downloaded archive. Its Git blob is `4a581b2181257d152b56167f60fff4f65454fa3b`.

The verifier reconstructs the manuscript subtree from all frozen files and recorded modes and compares it with the native build record. It does not reconstruct the entire repository tree or authenticate authorship. A hash match is a consistency result, not mathematical certification.

## 2. Actual mathematical coverage

The complete current `article/10c_global_curvature_inverse_v66.tex`, 431 lines, was read. The exact Schur converse, projected curvature map, residual certificate, global exact identification and complete finite-iteration propagation were analyzed. The unchanged filename does not imply unchanged contents. The new estimate is in Proposition 10.4, pp. 49–51, with its propagation constants in equation (10.13).

The revised common synthesis and abstract, both entry points, the response, cover letter, historical audit, dependency ledger and literature note were checked. The principal theorem and observation distinctions were compared with the actual proof inputs rather than accepted from the response alone.

Fresh dependency reading includes the graph-coordinate, two-offset extraction and actual-smooth envelope parts of `article/10b_periodic_contact_inverse_v65.tex` (especially lines 1–355); the Jacobi, relative determinant, integrated-amplitude and physical-time argument in `article/10a_periodic_itinerary_relative_v64.tex` (especially lines 1–475); and the complete 195-line `v4/20_nonlinear_information.tex`, including the realized area-preserving leading-data example.

The report does not freshly certify every earlier finite-chain/full-phase prerequisite, all details of the inherited analytic Banach inverse or real-to-disc theorem, every global matching/lattice and moving-family proof, the full statistical/calibration catalogue, or the companion. In particular, checking unchanged source bytes is not re-proving its contents. The mathematical reading is not described as a line-by-line audit of all 484 delivered pages.

## 3. Source and baseline verification

`verify_delivery.py` imports no author checker. It verifies lengths, SHA-256 values and Git blob identities, reconstructs a Git tree using the recorded modes, checks active input records and checks native build-report evidence and PDF hashes. Actual counts are 855 frozen files, 123 full-entry inputs, 55 principal-entry inputs and one companion input, with 134 distinct active inputs and 47 build-report evidence entries.

`compare_baseline.py` independently verifies both frozen manifests and source trees before comparing them. All 837 inherited source paths remain. There are 829 byte-identical inherited paths and eight edited paths, each with an exact archived original. No inherited Git mode changes. All 134 inherited active paths remain; none is added. The four explicitly tracked proof modules below are byte-identical:

- `article/10a_periodic_itinerary_relative_v64.tex`
- `article/10b_periodic_contact_inverse_v65.tex`
- `article/23f2_finite_experiment_analytic_inverse_v62.tex`
- `article/25a_common_observables_v25.tex`

The eight edited paths and 18 additional provenance/archive/response/tool paths are recorded in `AUDIT_RESULTS.json`. These figures count files, not distinct theorems or semantically preserved proof obligations. The author's preservation and mathematical checker was not rerun.

## 4. Fresh builds and actual visual inspection

The frozen manuscript tree was copied into a clean rebuild directory without seeding native generated auxiliary files. Companion, full manuscript and principal article were built in that order, so external auxiliaries were regenerated from their producers. Shell escape was disabled. All three builds returned zero.

All 484 pages match the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differ; both native and fresh hashes are retained. Final logs show four full-manuscript underfull-box notices, one principal notice, and none in the companion. The check found no final-log match for `undefined`, `Missing character`, `Overfull`, or `LaTeX Error`.

Direct visual inspection covered principal pp. 3, 46, 47, 49, 50, 51, 149 and 150 at 108 dpi. These pages cover the leading statement, curvature/residual result, complete propagation proof and nonlinear-information witness. No clipping or unreadable formula was observed there. All-page pixel equality is a mechanical comparison, not all-page visual inspection.

The checked environment used Python 3.13.5, SymPy 1.14.0, PyMuPDF 1.26.7, latexmk 4.86, and pdfTeX 1.40.26. Full version output is retained in the separate audit archive. Identical PDF bytes are not expected from another rebuild; the comparison separates byte identity, extracted text and rendering.

## 5. Independent finite mathematical controls

`independent_checks.py` imports no author code and uses no removable assertions. It performs exact rational/symbolic controls, not a rerun of the manuscript's own diagnostic.

**Curvature/residual controls.** Thirty positive scalar periodic Jacobi data sets, with periods two through seven, satisfy the Schur relation exactly. Three starting vectors and ten iterates each give 900 first-increment, 900 residual and 900 certified-inexact-evaluation inequalities. There are 840 successful sufficient positivity tests and 30 two-point bounds with rational residual enclosures. Nonimage and nonmonotone controls are retained. These are scalar contact data, not constructions of 30 globally closed billiard tables.

**Signed matrix controls.** Sixty block pairs at degrees three, four and five verify the resolvent derivative identity, derivative norm and two-point Lipschitz estimate. All 60 detect the deliberately incorrect commuted derivative. These tests do not evaluate all higher smooth remainders or independently prove the general finite-jet induction.

**Cubic propagation control.** The v66 example is reproduced exactly with the currently specified observed-Schur extension. Its cubic error is `48740/189931`; its old first-increment bound is `12/77`; its current residual bound is `42/319`. The sufficient constant `2160/343` covers the complete cubic discrepancy. This diagnoses the superseded coefficient-one sentence and checks its correction, not a failure of the revised theorem.

**Realized-information algebra.** The support-area polynomial, area-preserving tangent `z'(0)=-6/5`, fourth graph derivative `3-24s`, and nonlinear response `sqrt(3)/2` are checked exactly. The geometric convexity, clearance and analytic-family argument were read in the proof. These identities do not assert equal marked length spectra.

Normal and optimized Python produce identical complete JSON in this environment. Output SHA-256: `798d07309ca8efe4d0ae7010478f52301b7fd0244575ed48381e3a0b01e0dbe7`. Full emitted outputs accompany the separate archive. No finite check certifies arbitrary-order smooth differentiation, a trace-class limit, infinite-dimensional inversion, analytic continuation or a statistical risk theorem.

## 6. Primary-source check

The primary literature scope is recorded in L1–L5 of the report. Bálint–De Simoi–Kaloshin–Leguil's author-hosted paper was checked at Theorem D, Corollary E and Remark 2.3, printed pp. 9–10, including page images. Bolotin–Treschev's Theorem 2.1 and adjoining orientation discussion were checked on printed p. 12, including its page image. The official arXiv records for De Simoi–Kaloshin–Leguil, Finamore–Leguil and Florio–Leguil version 5 were refreshed. These are targeted theorem/observation-scope and record checks, not complete proof audits or an exhaustive priority search.

## 7. Reproduction

Obtain native artifact 10437417575 and extract its files into `WORK/artifact/`. Extract its `native-source.zip` into `WORK/source/`, producing `WORK/source/SOURCE_MANIFEST.json` and `WORK/source/source/`. For baseline comparison, similarly extract artifact 10433187185 and its source into `WORK/baseline/artifact/` and `WORK/baseline/source/`. Begin without an existing `WORK/rebuild/` directory for a fresh build. From this review directory run:

```sh
python verify_delivery.py "$WORK" > verification-source.txt
python verify_delivery.py "$WORK" --build two_collision > verification-companion.txt
python verify_delivery.py "$WORK" --build main > verification-main.txt
python verify_delivery.py "$WORK" --build rigidity > verification-rigidity.txt
python verify_delivery.py "$WORK" --compare > verification-comparison.txt
python compare_baseline.py "$WORK" > source-diff.json
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

The scripts require Python 3, SymPy, PyMuPDF and a TeX installation with the manuscript's packages. They make no network requests and do not download a moving branch. The delivery verifier writes `WORK/REPRODUCTION_RESULTS.json`, fresh PDFs/auxiliaries under `WORK/rebuild/`, and retained build output files. The comparator emits its results to standard output. `AUDIT_RESULTS.json` combines this run's machine findings with the frozen metadata and visual scope.

## 8. Review-only delivery

The new review starts from the pinned referee-ready head. Only files beneath `reviews/a2-v67-independent-harsh-top4-2026-09-16/` are added. Manuscript source, old reports, native deliveries, default-branch refs, protections and permissions are not modified. No pull-request approval, merge or journal decision is implied.
