# General Theta Foundations I — Revision 76

## Finite-Use Geometry of Ordered Binary Quantum Measurements

Revision 76 responds to both r49 reports on completed v75. It extends the full biased-qubit theory to the entire ordered binary effect body in every fixed finite input dimension, proves a multi-logarithmic entropy law, and constructs a common learner for an unknown biased qubit measurement. All inherited proof labels remain active. The general mathematics journal objective is retained.

`FROZEN_R49_REPORT.md` and `FROZEN_R49_PIPELINE_AUDIT.md` preserve the reports verbatim. `CONTROLLING_REPORTS.json` pins their branches, commits, Git blobs, and SHA256 digests. They review predecessor `16b78c8edef566300ea21300908854ad83455879`, whose native source is `efa7b14e2a42c6276f6748f98e3a15f2da018db3`; they do not constitute an external review of v76.

## Main results

For `0 <= E,F <= I_d`, put `M=(E+F)/2`, `H=F-E`, `V=M(I_d-M)`, and

\[
Q_N(E,F)^2=N\langle H,(L_V+R_V+N^{-1}\operatorname{Id})^{-1}H\rangle_{\rm HS}.
\]

Theorem `thm:matrixmetric76` proves, for every `d,N >= 1`,

\[
\frac{\min\{1,Q_N\}}{8192d}
\le d_N^{\rm na}(E,F)\le d_N(E,F)\le\min\{2,8Q_N\}.
\]

The upper distance includes arbitrary references, common adaptation, feedback, and bounded public stopping. The normalization is unhalved trace norm. Horizontal dilations and a regularized Sylvester split give the upper bound; compressed nonadaptive tests give the converse, at every rank and multiplicity. In particular `d_N <= 65536d d_N^na` uniformly in the horizon, without asserting equality of the optima.

Theorem `thm:matrixcover76` gives, at each fixed `d`,

\[
\mathcal C_N(\mathfrak E_d,\delta)
\asymp_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2},
\quad N\ge1,\quad0<\delta\le\delta_d.
\]

Actual operational balls have uniformly controlled weighted volume, including at singular boundary centres. A spectral integral counts nested pairs approaching opposite support endpoints. The cumulative exponent of a signed endpoint sector is `S_j^2/2`; each balanced prefix contributes a logarithm. Rational legal centres attain the same order. The description length is

\[
\frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
    +d^2\log_2(1/\delta)+O_d(1).
\]

Theorem `thm:commonlearn76` supplies one experiment for every unknown effect in `E_2`, with bias, contrast, and direction all unknown. The optimum worst-case training budget for error `delta` in the future-`N` adaptive distance and failure at most `eta` is

\[
\Theta\bigl(N\delta^{-2}\log(1/\eta)\bigr),
\quad0<\delta\le\delta_0,\quad0<\eta\le1/8.
\]

Randomized GHZ signs cancel unknown bias; empirical amplitudes choose the block length; fresh samples estimate both endpoints. Each entangled block has at most `N` calls. A scalar Bernoulli subfamily gives the matching converse. Rational rounding and the retained exact qubit code yield one optimal-order reusable word without further calls.

## Manuscripts and review material

| File | Role |
|---|---|
| `paper.pdf`, `quantitative.tex` | Focused article: new matrix results and common learning first, detailed qubit geometry and code next, all earlier supporting quantitative proofs in appendices |
| `STRUCTURAL_PAPER.pdf`, `structural.tex` | Independently complete structural companion with inherited hypotheses and proofs |
| `COMPLETE_REVISION.pdf`, `main.tex` | Complete research edition preserving historical mathematical development and adding the new results |
| `RESPONSE_TO_REFEREE.md` | Responses to all 20 required revisions and 36 detailed r49 comments, the broadening requests, and the pipeline audit |
| `PROOF_AUDIT.md`, `PROOF_STATUS.json` | New proof dependencies and exact claim boundaries |
| `LITERATURE_AUDIT.md`, `INDEPENDENT_REVIEW_BRIEF.md` | Primary-source comparisons and concrete next-review questions |
| `HISTORY_AND_PIPELINE_AUDIT.md` | Historical source lineage and the unchanged analytic pipeline status |
| `PRESERVATION_MANIFEST.json`, `PROOF_TEXT_PRESERVATION.json` | Predecessor native hashes, retained proof labels, and explicit text changes |
| `RESOURCE_LEDGER.md`, `RESOURCE_LEDGER.json` | Payload, training calls, exact algebra, workspace, and hardware accounting |
| `figures/effect-body76.tex` | Native figure of the qubit spectral triangle and a specified double-cone section |

The focused introduction and comparison are short and theorem-led. The earlier instrument, preparation, coherent, observable-readout, noise-transition, and unbiased-boundary proofs remain complete in its appendices. The complete edition retains their historical order. All 266 native predecessor files are pinned; previous author-side audits and comparison text are archived in `predecessor-v75-audit/`. Earlier manuscript directories and review branches remain immutable inputs.

## Exact arithmetic and construction

`matrix_metric.py` computes exact midpoint-modulus certificates for supplied Gaussian-rational pairs, checks legality at every rank, and replays the complete pair-bound result. `MATRIX_METRIC_SCHEMA.md` specifies the interface. Four examples have actual Hilbert dimensions one through four, including noncommuting effects and rank-two projections.

```sh
python matrix_metric.py compute --input inputs/matrix-effect-3.json --horizon 7
python matrix_metric.py verify --input inputs/matrix-effect-3.json --certificate certificate.json --horizon 7
python check_matrix_geometry.py
python check_common_learning.py
```

The first command prints a certificate; save its JSON as `certificate.json` for the second. Inherited codecs remain unchanged. Their schemas distinguish qubit Bloch-coordinate count from actual Hilbert dimension.

The learner has a complete written construction and exact finite checks of GHZ and boundary identities. Those checks are not a physical learning run or a full learner implementation. Arbitrary-dimensional rational covering existence is distinct from an implemented optimal encoder in arbitrary dimension.

## Reproduction and source identity

Use the pinned `requirements.txt`, pdfLaTeX with AMS packages and TikZ, and the recorded environment. From this directory:

```sh
python build_revision.py --isolated
python build_revision.py --verify-published
```

The builder runs 14 exact suites in ordinary and optimized Python with identical results, compiles all three manuscripts, rejects unresolved references/citations and bad boxes, and checks every page for clipping. An isolated native-source reconstruction must reproduce every page's text and raster. The focused journal ZIP has an independent verifier requiring no historical PDF or repository history.

Generated evidence records the actual source commit, source hashes, theorem locations, page signatures, regression results, and package digests. Publication is a direct child of the native-source commit. The v76 GitHub workflow checks the exact submitted publication read-only, separately rebuilds the journal package, and attaches receipts to that exact workflow run. Only executed receipts establish successful reproduction.

The work branch is `revision/general-theta-foundations-i-v76-r49-response-2026-10-04`; the native-source and referee-ready branches use `v76-native-source` and `v76-referee-ready` with the same date. The ready branch is assigned after publication verification succeeds.

The r49 concerns are addressed through new theorems, complete proofs, and revised presentation. External evaluation of significance and priority remains a separate judgment. Source receipts are not human authorship signatures, independent priority clearance, or closure certificates for the A/B/C/D analytic programme.
