# Source audit for the A2 v13 canonical rereview

## Review identity

- Repository: `TrillionniumFoundation/theta-theory`
- Canonical source branch: `revision/a2-v13-major-revision-canonical-2026-09-28`
- Frozen source commit: `0e54099f079232df233316ae6fe7986fc51b7ea1`
- Frozen source tree: `41f68e02205e10d48e917559f0f5092c10799948`
- Manuscript directory: `papers/A2-v13-two-flight-relative-invariants`
- Review branch: `review/a2-v13-external-harsh-top4-rereview-2026-09-28`
- Review date: 2026-09-28
- Requested standard: Annals / Acta / Inventiones / JAMS

The canonical source branch is a ref to the 10 September 2026 A2 v13 commit. It is not a later manuscript commit. The report therefore evaluates the mathematical source at that immutable SHA and separately records that no post-v13 response is present.

## Directly read source

The following native files were read directly at the frozen source commit.

### Entry point and revision record

- `papers/A2-v13-two-flight-relative-invariants/main.tex`
- `papers/A2-v13-two-flight-relative-invariants/README.md`
- `papers/A2-v13-two-flight-relative-invariants/RESPONSE_TO_REFEREES.md`
- `papers/A2-v13-two-flight-relative-invariants/PROOF_LEDGER.md`
- `papers/A2-v13-two-flight-relative-invariants/HISTORICAL_DERIVATION_AUDIT.md`
- `papers/A2-v13-two-flight-relative-invariants/LITERATURE_VERIFICATION.md`
- `papers/A2-v13-two-flight-relative-invariants/VERIFICATION.json`
- `papers/A2-v13-two-flight-relative-invariants/SOURCE_PINS.json`

### Main claims and closest dependencies

- `article/01_introduction.tex`
- `article/02_finite_results.tex`
- `article/15_operator_comparison.tex`
- `article/20_boundary_compatibility.tex`
- `article/21_abel_stability.tex`
- `article/22_deautoconvolution.tex`
- `article/23_two_contact_rigidity.tex`
- `article/24_physical_image.tex`
- `article/28_regularized_observation.tex`
- `article/29_two_flight_benchmark.tex`
- relevant calibration passages in `article/27_profile_calibration.tex`
- selected relative-action, integration and boundary-layer statements in:
  - `v3/10_geometry_action.tex`
  - `v3/20_integration.tex`
  - `v4/10_boundary_layers.tex`
  - `v5/15_differentiated_operators.tex`

The rereview concentrated on theorem statements, hypotheses, information sets, last-jet calculations, the normalizing conventions, and the proof junctions needed for the recommendation. It did not certify every retained appendix result.

## Prior review history consulted

The following reports were read as historical inputs, not adopted as authority.

- `reviews/a2-v13-independent-harsh-relative-law-2026-09-10/REFEREE_REPORT.md`
  at commit `f29d8f96e87bf46db2ffbe8217caa09563c5e536`
- `reviews/a2-v13-independent-harsh-normal-form-2026-09-10/REFEREE_REPORT.md`
  at commit `b3f0ad5843782c221651c9189fc156d20865cab1`
- `reviews/a2-v13-independent-harsh-normal-form-2026-09-10/ANALYTIC_NORMAL_FORM_BENCHMARK.md`
  at the same review commit
- the v12 report identified in the author response at
  `2ae2751f61224b66f314915fd5fc22f6321b606f`

The earlier v13 reports disagree on whether the appropriate requested-level recommendation is rejection or focused major revision. This rereview independently separates correctness, statement scope, and requested-level significance.

## External literature checked

The following primary or institutional sources were used only for targeted scope checks.

- De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4 / Inventiones Mathematicae 233 (2023), for the analytic period-two setting, local Birkhoff-normal-form mechanism, and global marked-length theorem.
- Finamore–Leguil, arXiv:2510.18983v1, for the enriched marked-length spectrum and global finite-horizon conclusion cited by the manuscript.
- Zelditch, *Inverse spectral problem for analytic domains, II*, Annals of Mathematics 170 (2009), for the stated analytic symmetry classes and spectral determination comparison.

This was not an exhaustive novelty search. No claim is made that one of these papers already proves the full A2 smooth relative law or observation theorem.

## Independent exact-rational diagnostics

`verify_review.py` is self-contained and imports no author verification code.

It reconstructs:

- the printed two-flight block;
- the Schur-complement row from the quadratic action;
- the other-contact twist contribution;
- the endpoint and middle-coordinate variances;
- the binomial separation;
- the inverse identity.

Grid:

- \(c_0,c_1\in\{11/10,3/2,2,4\}\);
- \(g\in\{1/2,1,3/2\}\);
- \(m=2,\ldots,15\);
- both orientations.

Result:

- 672 geometry/order cases;
- 8,064 grid checks passed;
- one additional printed quartic example passed;
- 8,065 total checks;
- deterministic identifier digest recorded in `verification.json`.

These checks establish finite algebraic consistency on the stated grid. They are not a proof of the stationary implicit-function theorem, the all-order degree argument, the smooth relative theorem, or the statistical results.

## Findings tied to exact source locations

### False abstract quantifier

`main.tex` says that “every fixed finite-dimensional family” is observable at two flights.

`article/29_two_flight_benchmark.tex`, Theorem `thm:v13-two-flight-observation`, instead fixes a physical analytic family of Theorem `thm:v12-realization`, allows constants to depend on that family and \(M\), and says that the family and leading data are supplied.

`article/24_physical_image.tex`, Theorem `thm:v12-realization`, constructs a particular locally full-rank analytic family near a disk geometry. It does not quantify over arbitrary finite-dimensional families.

The report's distant-obstacle translation family directly separates the abstract claim from the theorem.

### Missing forward comparator

`article/01_introduction.tex` compares the data and conclusions with global inverse-spectral results.

`article/15_operator_comparison.tex` compares the proof with discrete Hill/cofactor identities, inverse decay, trace-class determinant continuity, and Morse transport.

Neither section states the restricted analytic local-normal-form endpoint calculation described in the report. Thus the comparison with the closest forward mechanism is absent from the frozen source.

### Canonical alias

The branch `revision/a2-v13-major-revision-canonical-2026-09-28` resolves to the same source commit reviewed by the two 10 September v13 reports. No source delta exists between the canonical ref and `0e54099f079232df233316ae6fe7986fc51b7ea1`.

## Activities not claimed

This rereview does not claim:

- an independent successful full TeX build;
- reproduction of the author's 3,295-check suite;
- reproduction of prior reviewers' diagnostic suites;
- remote CI execution;
- a nonlinear billiard simulation;
- formal verification;
- exhaustive checking of all 218 formal environments;
- exhaustive literature clearance;
- an official journal decision.

The recommendation is based on direct source reading, exact finite-block diagnostics, an explicit counterfamily to the abstract quantifier, a restricted normal-form comparison, and a top-four-level assessment of the completed theorem package.
