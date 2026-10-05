# General Theta Foundations I — Revision 77

## Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements

This revision answers both R50 reports on completed v76. It retains the matrix geometry and entropy theorems, proves a common learner on the full effect body in every finite input dimension, and gives a deterministic finite exact encoder and decoder at the optimal fixed-dimensional payload order. A further corollary attains the training and description orders simultaneously. The general mathematics journal objective is retained.

The reviewed head is `c041c011274973728a8cc55029192c057696aa43`, with native-source parent `a107cd1a0f7ec4e356e807f5f49c7ab998553552`. The reports are frozen verbatim in `FROZEN_R50_REPORT.md` and `FROZEN_R50_PIPELINE_AUDIT.md`; `CONTROLLING_REPORTS.json` records their branches, commits, Git blobs and SHA-256 digests. They review v76. No external referee assessment of v77 is inferred from those reports or from the internal checks supplied here.

## Mathematical results

The interface is the ordered binary, input-consuming channel

\[
\mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
+\operatorname{tr}((I_d-E)\rho)|0\rangle\langle0|,
\qquad0\preceq E\preceq I_d.
\]

The device returns a classical outcome and no residual quantum system. The experiment may retain external references. The distance `d_N` uses unhalved final-state trace norm, at most `N` calls, common adaptive control and bounded public stopping. Nonadaptive experiments may entangle all inputs with a reference, but do not condition later inputs on earlier outcomes.

### Geometry and entropy retained from v76

For `M=(E+F)/2`, `H=F-E` and `V=M(I_d-M)`, set

\[
Q_N(E,F)^2=N\langle H,(L_V+R_V+N^{-1}\operatorname{Id})^{-1}H\rangle_{\mathrm{HS}}.
\]

Theorem `thm:matrixmetric76` proves, for all `d,N >= 1`,

\[
\frac{\min\{1,Q_N\}}{8192d}
\le d_N^{\mathrm{na}}(E,F)\le d_N(E,F)\le\min\{2,8Q_N\}.
\]

Every rank and spectral multiplicity is included. In particular, `d_N <= 65536d d_N^na` uniformly in `N`. The form is a comparison modulus, not an exact distance or exact optimum. Theorem `thm:matrixcover76` gives, for each fixed `d`,

\[
\mathcal C_N(\mathfrak E_d,\delta)
\asymp_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2},
\quad N\ge1,\quad0<\delta\le\delta_d.
\]

Uniform volume bounds concern actual operational balls, including singular boundary centres. Balanced prefixes in the spectral endpoint integral account for the logarithmic exponent. All earlier qubit, preparation, instrument, coherent and readout results retain their original statements and error ranges.

### Common learning on the entire matrix body

New Theorem `thm:matrixlearning77` constructs one experiment, common to every unknown effect in `E_d`, with

\[
\sup_{E\in\mathfrak E_d}\mathbb P_E\{d_N(\mathcal M_E,\mathcal M_{\widehat E})>\delta\}\le\eta,
\qquad M\le Cd^4N\delta^{-2}\log(d/\eta).
\]

The constants `C` and the small accuracy threshold `delta_0` are absolute, `N,d >= 1`, and `0 < eta <= 1/8`. The call bound holds on every record; each entangled block uses at most `N` calls. A scalar Bernoulli subfamily gives `M >= c N delta^-2 log(1/eta)` even for reference-assisted adaptive training. Thus the training rate is

\[
\Theta_d\!\left(N\delta^{-2}\log(1/\eta)\right)
\]

for every fixed `d`. The explicit upper factor `d^4` is not claimed optimal.

The proof calibrates both `E+I/N` and `I-E+I/N`, controls the additional variance under two-dimensional compression, and assembles learned coordinates in the calibrated quadratic norm. All choices use observations and public parameters. A finite legal rational grid returns an effect in the original public basis. The qubit subprocedure now specifies first-rejection stopping, guarded phase recovery, deterministic fallbacks, conditional confidence budgets and a cost bound on exceptional records.

### Exact descriptions and learning into a payload

New Theorem `thm:matrixcodec77` constructs a deterministic finite dictionary from public `(d,N,delta)`: enumerate a legal rational grid with denominator `ceil(32dN/delta)` and compare exact rational values of `Q_N^2`. Inward rounding and greedy assignment give operational error at most `11 delta/16`. Every fixed-length word decodes to a legal effect, including unused indices.

For fixed `d` in the stated small-error range, the optimal payload length is

\[
\frac{d^2}{2}\log_2N+
\lfloor d/2\rfloor\log_2\log(N+2)+d^2\log_2(1/\delta)+O_d(1).
\]

Corollary `cor:matrixlearnedcode77` runs learning and coding each at accuracy `delta/2`, giving total error at most `27 delta/32` on success. It attains the same training and payload orders with no additional device calls. The payload converse uses a fixed public decoder into legal memoryless ordered binary effects.

The exact dictionary construction is exhaustive. Its ambient candidate count is `(K+1)^d(2K+1)^{d(d-1)}`; storage uses `O(M_code d^2)` rational entries. Polynomial runtime and optimal workspace are not claimed. The statistical learner is specified and proved mathematically; a physical-device training implementation is not represented as executed.

## Manuscripts and review package

| File | Role |
|---|---|
| `paper.pdf` / `quantitative.tex` | Self-contained focused article: matrix geometry, entropy, qubit learning, matrix learning, exact coding, full qubit prerequisites and literature comparison |
| `STRUCTURAL_PAPER.pdf` / `structural.tex` | Independently complete structural companion with inherited hypotheses and proofs |
| `COMPLETE_REVISION.pdf` / `main.tex` | Complete research edition preserving the historical proof development and adding the new results |
| `RESPONSE_TO_REFEREE.md` | R01–R20, D01–D36 and proof-pipeline acceptance-gate crosswalk |
| `PROOF_AUDIT.md` / `PROOF_STATUS.json` | Proof dependencies, verification boundaries and exact claim status |
| `LITERATURE_AUDIT.md` / `INDEPENDENT_REVIEW_BRIEF.md` | Primary-source theorem comparisons and concrete specialist priority questions |
| `HISTORY_AND_PIPELINE_AUDIT.md` | Historical derivation routes and broader analytic programme status |
| `PRESERVATION_MANIFEST.json` / `PROOF_TEXT_PRESERVATION.json` | All 296 predecessor native files, all 658 complete-edition labels and explicit proof-text changes |
| `RESOURCE_LEDGER.md` / `RESOURCE_LEDGER.json` | Training, horizon, block size, memory, preparation, payload, runtime and workspace |
| `evidence/JOURNAL_PACKAGE.zip` | Focused and structural articles, all active native TeX inputs and standalone verifier |
| `evidence/RESEARCH_PACKAGE.zip` | Complete native source, three PDFs and source-bound verification evidence |

The focused article moves 149 inherited labels to the complete research edition; every one remains actively typeset there. All 658 labels from the preceding complete edition remain active. The moved-label list and its destination are machine checked. No historical proof section is removed. Previous author-side audits and original revised passages are retained in `predecessor-v76-audit/`; the entire v76 directory and earlier review branches remain unchanged.

## Exact arithmetic interfaces

`matrix_metric.py` computes exact pair-modulus certificates for Gaussian-rational matrices with full PSD tests and a rational Sylvester solve. It reports proved comparison bounds, never the exact adaptive optimum. See `MATRIX_METRIC_SCHEMA.md`.

`matrix_codec.py` implements the complete finite dictionary algorithm. See `MATRIX_CODEC_SCHEMA.md`. A small complete example is:

```sh
python matrix_codec.py encode --input examples/matrix-codec-scalar-source.json --horizon 1 --accuracy 1/2 > scalar-code.json
python matrix_codec.py decode --input scalar-code.json
python matrix_codec_check.py
```

Complete theorem dictionaries are executed in six scalar cases. Separate complete small two- and three-dimensional grids test enumeration and legality kernels; the actual two-dimensional theorem grid is checked on an explicitly identified finite prefix only. A resource cutoff returns an incomplete-construction error and emits no codebook or payload. Finite checks do not prove continuum covering or statistical risk statements.

## Reproduction and source identity

Use `requirements.txt`, pdfLaTeX with AMS and TikZ packages, and the recorded environment. From this directory:

```sh
python build_revision.py --isolated
python build_revision.py --verify-published
```

The builder runs 15 exact suites under ordinary and optimized Python with identical results, compiles three manuscripts, rejects unresolved references, citations and bad boxes, and checks every page for clipping. Isolated native-ZIP reconstruction must reproduce every page's text and raster. The journal verifier rebuilds both articles without a historical PDF, repository history or other external manuscript file.

`evidence/BUILD_RECEIPT.json` identifies the actual native-source commit. `SOURCE_HASHES.json`, `THEOREM_LOCATIONS.json`, `PAGE_CHECKS.json` and `PACKAGE_MANIFEST.json` bind sources and artifacts. Publication is a direct child of that source commit. The v77 GitHub Actions workflow checks the exact publication head read-only and attaches reconstruction receipts. An earlier revision's successful receipt is not evidence for this revision.

The revision branches are:

- `revision/general-theta-foundations-i-v77-r50-response-2026-10-04`
- `revision/general-theta-foundations-i-v77-native-source-2026-10-04`
- `revision/general-theta-foundations-i-v77-referee-ready-2026-10-04`

The ready alias is assigned after final-head verification. Independent human specialist priority judgment remains an explicitly uncompleted part of R03. Source hashes, internal proof checks and CI do not supply a human authorship signature, journal acceptance or A/B/C/D programme closure.
