# Three-Paper Content Coverage Audit

- Date: 2026-07-09
- Master source: `main.tex`
- Extracted drafts:
  - `papers/response-theory/`
  - `papers/theta-expectation-hjb/`
  - `papers/representation-calculus/`
- Consolidated package checklist:
  - `draft/three-paper-package-checklist.md`

## Executive Verdict

Yes: a large amount of material from the master manuscript is not yet present
in the three extracted papers.

This is not evidence that files were lost.  The master `main.tex` remains the
source ledger.  But the current extracted papers are much closer to clean
submission-facing skeletons/interface drafts than to full content-preserving
splits of the master manuscript.

The current split is useful as a dependency-clean package, but it is not yet a
complete extraction of the original long manuscript.

## Size Audit

Raw source sizes:

| File | Lines | Words | Bytes |
| --- | ---: | ---: | ---: |
| `main.tex` | 16230 | 102827 | 869901 |
| `papers/response-theory/main.tex` | 1898 | 9780 | 88221 |
| `papers/response-theory/proof-ledger-appendix.tex` | 5002 | 24507 | 225203 |
| `papers/theta-expectation-hjb/main.tex` | 877 | 3620 | 37029 |
| `papers/theta-expectation-hjb/technical-appendix.tex` | 1692 | 7751 | 69578 |
| `papers/representation-calculus/main.tex` | 523 | 2110 | 20375 |
| extracted total | 9992 | 47768 | 440406 |

The extracted TeX word count is about 47% of the master after the first
thirty-five Paper 1 proof-ledger repair passes, the Paper 1 single-PDF appendix
merge, the first seven Paper 2 technical-appendix passes, the Paper 2
single-PDF appendix merge, and the Paper 3 sign/application pass.  This is
still the main
reason the extracted papers feel short.

PDF/page state:

| Draft | Current PDF pages |
| --- | ---: |
| Paper 1 integrated manuscript | 72 |
| Paper 2 integrated manuscript | 27 |
| Paper 3 | 6 |

The original split plan expected much larger submission papers:

- Paper 1 minimum submission shape: 45-70 pages.
- Paper 2 minimum submission shape: 50-75 pages.
- Paper 3 was intended as a shorter downstream representation paper; it now
  has a first sign-convention/application pass, but can still be expanded for
  a target venue.

## Planned Source Allocation Versus Current Extraction

The split plan assigned these master-source word counts:

| Allocation | Master lines | Master words | Current extracted words | Verdict |
| --- | ---: | ---: | ---: | --- |
| Paper 1 planned core | 3330 | 20026 | 9780 main shell words + 24507 appendix words | substantially compressed |
| Paper 1 planned appendix/proof ledger | 3942 | 27298 | first thirty-five proof-ledger/master-appendix migration passes integrated into appendices, 24507 appendix words | major omission if full proof required |
| Paper 2 planned core | 3303 | 17634 | 3620 main shell words | heavily compressed |
| Paper 2 planned appendix/proof detail | 2389 | 15862 | first seven HJB technical-appendix passes integrated, 7751 appendix words | major omission still open if standalone flagship paper |
| Paper 3 planned core/detail | 1291 | 8288 | 2110 | compressed; less fatal but still incomplete |
| Intro/meta/front matter | 581 | 5195 | mostly omitted/summarized | likely acceptable unless positioning is needed |
| Closure/other proof ledgers | 478 | 3146 | mostly omitted/summarized | probably acceptable if not repeated |

## Theorem/Label Density Audit

| File | Unique labels | Theorem-like blocks |
| --- | ---: | ---: |
| master `main.tex` | 517 | 312 |
| Paper 1 main | 43 | 39 |
| Paper 1 proof-ledger appendix | 121 | 118 |
| Paper 2 main | 20 | 20 |
| Paper 2 technical appendix | 54 | 54 |
| Paper 3 | 18 | 17 |

The extracted papers do not preserve most of the master theorem/lemma/proof
ledger structure.  They preserve selected theorem interfaces and a few proof
spines.

## Paper-by-Paper Findings

### Paper 1: Response Theory

Current state:

- Strongest of the three extracted papers.
- Has a single integrated 72-page PDF with a main response package,
  moving-trace bounds, differentiated resolvent words, constant ledger,
  branch-calculus source lemmas, and proof-ledger appendices covering primitive
  collision, singular strata,
  homogeneity/growth/distortion, stable holonomy and summability, compact
  embedding, anisotropic transfer, invariant-density/Hopf-chain closure,
  Lasota-Yorke spectral closure, Dolgopyat high-frequency induction,
  suspension resolvent, branchwise constant propagation, branchwise parameter
  regularity, moving-boundary traces, trace recovery, invariant-density
  construction details, Dolgopyat pair-selection constants, branchwise
  derivative-tree bookkeeping, finite-word stratification, moving-boundary
  response constant checks, worked grazing branch-change/double-trace/terminal
  tail cases, exact coordinate-atlas refinements for triple trace,
  near-tangent branch-change, determinant lower-bound cells,
  repeated-generator trace derivatives, determinant/trace constant alignment
  with the main appendix, anisotropic norm-reference alignment, finite-horizon
  nonintegrability input ledger, curvature-coordinate cone recurrence,
  strip-complexity growth balance, standard-family preservation, roof/flow-box
  transition details, roof derivative recurrence, Jacobian/distortion
  derivative hierarchy, weighted-transfer derivative closure,
  peripheral-spectrum audit states, Hopf-chain aperiodicity subcases,
  finite-audit peripheral-spectrum exclusion, finite-time branch-composition
  examples, worked Dolgopyat cancellation windows, a two-branch cancellation
  estimate, bad-window/terminal recovery, stable-holonomy constants,
  quantitative holonomy product checks, trace-transport constant checks,
  invariant-density Cesaro-window/tightness and derivative source examples,
  Dolgopyat amplitude--phase margin and phase sublevel-counting constants,
  worked moving-boundary response models, single-wall normal response,
  two-letter response word examples, higher-order moving-boundary response
  subcases, worked spectral-projector recording windows, finite-recording
  spectral projector checks, a projector-derivative observable response
  example, worked finite-word response examples, artificial strip-boundary
  cancellation, mixed finite-word response word closure,
  target-venue proof-dependency convention, referee dependency-discharge
  ledger, target-venue dependency closure,
  forward uniform-constant graph window, uniform input-to-branch reduction,
  forward constant-graph closure, canonical collision-coordinate branch ledger,
  branchwise impact/reflection derivative expansion, canonical branch
  summability/distortion closure, boundary curvature/reflection/flux ledger,
  reflection and flux variation formula, singular-strata zero-measure subcase
  closure, parameter-uniform curvature-atlas refinement, curvature-tensor
  recurrence with parameters, multi-impact corner chart closure, high-order
  parameter derivative tree examples, finite-atlas transition derivative
  estimates, parameter-tree/atlas-transition closure, high-order
  reduced-resolvent word examples, terminal-tail constant checks,
  resolvent-word terminal-tail closure, Lasota--Yorke margin audit window,
  compact-embedding Hennion radius check, spectral-gap margin closure,
  finite Hopf-connectivity ledger, invariant-density uniqueness finite audit,
  Hopf finite-power aperiodicity closure,
  Kato projector differentiability window, contour projector derivative
  formula check, Kato projector-resolvent word closure,
  suspension low-frequency contour window, zero-pole cancellation contour
  check, low-frequency suspension reduced-resolvent closure,
  Dolgopyat finite-window induction ledger, bad-window recycling estimate,
  finite-window high-frequency closure,
  high-frequency contour differentiability window, dyadic contour derivative
  bound, inverse-Laplace high-frequency correlation closure,
  flow-observable lifting window, section-to-suspension norm comparison,
  correlation-to-response observable example closure,
  and local chart casework.
- Has clean compile/package status for `response-theory.pdf`.

Major master material still not fully extracted:

- Remaining fine collision-coordinate and branchwise calculations from
  `main.tex:7911-11177` beyond the canonical branch ledger now migrated.
- Remaining boundary-curvature and singular-strata casework beyond the first
  reflection/flux variation and zero-measure subcase closure.
- Remaining high-order curvature tensor and corner-atlas variants beyond the
  first parameter-uniform curvature recurrence, multi-impact closure, and
  finite-atlas transition estimates.
- Further uniform-constant refinements around the forward dependency graph from
  `main.tex:14406-15080` beyond the first local closure now migrated.
- Many appendix-level proofs named in the split plan:
  collision coordinates, curvature tensors, reflection laws, singular strata,
  stable holonomy, invariant density,
  anisotropic norms, Lasota-Yorke, spectral gap, suspension resolvent, and
  parameter regularity.

Risk:

- For a specialist dynamical-systems submission, the current 72-page single PDF
  is just above the nominal 45-70 page planning window, but page count is not
  the same as a content-complete proof companion for the strongest
  first-principles response claim.
- Even after thirty-five proof-ledger/reference-alignment passes and the
  single-PDF appendix merge, the integrated proof-ledger appendix is not yet a
  full replacement for the large proof-ledger appendix allocation.

Recommended repair:

1. Keep Paper 1 in the integrated single-PDF appendix posture unless a target
   venue explicitly requires a different upload shape.
2. Use the post-merge proof-depth/venue audit before adding more material: if a
   hard 70-page cap applies, trim 2--4 pages of crosswalk/dependency prose
   first.
3. Add more proof-detail only for a specific missing specialist subcase, not as
   generic page growth.
4. Keep Paper 1 main text compact, but keep the integrated appendices genuinely
   specialist-auditable.

### Paper 2: HJB/theta-Expectation

Current state:

- Has Paper 1 import interface, effective coefficients, residual identity,
  contact-frozen tests, sub/sup residuals, comparison, HJB limit,
  nonconvexity, concrete Lorentz-cell example, non-subadditivity, bibliography,
  and submission package.
- Now has seven technical-appendix passes covering finite-response
  micro-action, endpoint-jet realization, endpoint reciprocity, exact prelimit
  action graph, specular endpoint variation, moving-boundary trace control,
  contact-frozen and recursive corrector hierarchy, branch residual constants,
  full branch residual checks, four-scale residual identity, half-relaxed
  viscosity passage, smooth approximation closure, synchronized
  doubled-variable comparison, density-to-state upgrade, coefficient
  comparison, Green-Kubo correlation Hilbert factorization, terminal-value
  stability, concrete nonconvex parameter window and recipe, dimensionless
  parameter audit table, normalized numerical certificate with stability
  margin, and nonconvexity/subadditivity algebra.
- It is clean and readable.

Major master material still not fully extracted:

- Deterministic micro-action and exact prelimit Hamilton-Jacobi machinery from
  `main.tex:1364-2245` now has appendix ledgers with endpoint jets,
  reciprocity, the action graph, closed prelimit HJ identity, specular endpoint
  variation, and moving-boundary trace control.
- Effective coefficient and analytic two-scale equation material from
  `main.tex:4359-6381` now has corrector, residual, Green-Kubo correlation,
  comparison-trace, terminal-stability, full branch residual, and smooth
  approximation ledgers but is still compressed relative to the master.
- Corrector cancellation, comparison,
  finite-horizon/a.e. collision-map dependencies, Green-Kubo/corrector
  hierarchy, half-relaxed limits, and nonconvexity algebra from the planned
  appendix ranges are still compressed after the first seven technical-appendix
  passes, but the most visible prelimit-action, doubled-comparison,
  Green-Kubo, terminal-stability, branch-residual, smooth-approximation, and
  parameter-window gaps are now represented.

Risk:

- Paper 2 is now a 27-page integrated article with technical appendices, but
  still not a 50-75 page flagship proof paper.
- If submitted as-is, a referee could say the HJB convergence proof still
  relies on compressed proof ledgers.

Recommended repair:

1. Continue expanding the HJB technical appendices only for venue-specific proof
   polish.  First seven passes are integrated.
2. Add a true numerical orbit/parameter experiment only if a venue requests
   more than the normalized inequality certificate.
3. Keep BSDE/Girsanov excluded.
4. Preserve the concrete nonconvex example in main text.

### Paper 3: Representation Calculus

Current state:

- Has dependency guardrail, representation window, linearity obstruction,
  payoff-calibrated generator, calibrated diffusion, gradient-vs-\(Z\) lemma,
  BSDE, sign-convention/parabolic orientation ledger, Girsanov formula, a short
  robust-pricing/model-uncertainty stress illustration, post-derivation
  calibration, bibliography, and submission package.

Major master material still not fully extracted:

- Calibrated nonlinear semigroup details from `main.tex:11703-12052`.
- Detailed calibrated generator material from `main.tex:13321-13451` is still
  compressed, while the sign-convention/orientation proof from
  `main.tex:13636-13685` is now represented in the main text.
- Post-derivation calibration ledgers from `main.tex:15756-15890` are only
  summarized.
- The robust-pricing/model-uncertainty example is present only as a short
  calibrated stress-test illustration.

Risk:

- Less severe than Papers 1 and 2, because Paper 3 can plausibly be a short
  note if the target is narrow.
- Still too thin for a standalone stochastic-analysis paper unless expanded
  with a more detailed well-posedness appendix or target-specific application.

Recommended repair:

1. If targeting probability/stochastic analysis, expand the stochastic-equation
   well-posedness assumptions and regularization passage.
2. If targeting finance, expand the robust-pricing stress illustration into a
   small worked example.
3. Keep the fixed-payoff calibration guardrail visible.

## What Was Probably Correctly Omitted

The following master content can remain out of the submission drafts unless a
specific target venue needs it:

- Repeated acyclicity and dependency-closure ledgers.
- Internal source/provenance line markers.
- Broad motivational comparisons to non-commutative probability and regularity
  structures, except as short introduction/context paragraphs.
- Repeated proof dependency tables that duplicate the theorem inventories.
- Any representation material inside Paper 2 or HJB material inside Paper 3.

## Bottom Line

The current three-paper split is dependency-clean but not content-complete.

If the goal is to create clean working submission drafts, the current state is
useful.  If the goal is to preserve the full mathematical support of the
original manuscript, then yes, many details remain in master `main.tex` and
must still be extracted into appendices.

Priority order for repair:

1. Continue Paper 1 specialist proof details if the first-principles response
   theorem is the immediate target.
2. Continue Paper 2 HJB technical appendices with venue-specific proof polish,
   or add a true numerical experiment only if requested.
3. Top-level three-paper package checklist after appendix changes.
4. Target-specific Paper 3 introduction and optional application expansion.
