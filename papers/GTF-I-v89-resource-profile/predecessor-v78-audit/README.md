# General Theta Foundations I — Revision 78

## Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements

This revision answers both R51 reports on completed v77. It retains the full matrix geometry, entropy, common learning and exact coding results, and adds a sharp independent-block learning law, an adaptive information lower bound coupling dimension and accuracy, a dimension-free interior comparison, a sharp joint interior learning law, and finite trusted-control specifications. The research subject and general mathematics journal objective are retained.

The reviewed final head is `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`, with qualified native source `91df620ec7b6e02a6f0fe1c7798639c2626c742b`. The external report is `96a3666ed516ea12fcdb8ede341b7082e4ff2c78`; the pipeline audit is `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`. Both are frozen verbatim in `FROZEN_R51_REPORT.md` and `FROZEN_R51_PIPELINE_AUDIT.md`. `CONTROLLING_REPORTS.json` records their branches, Git blobs and SHA256 identities. They review v77; no outside review of v78 is inferred from those reports or from internal proof checks.

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

Retained Theorem `thm:matrixlearning77` constructs one experiment, common to every unknown effect in `E_d`, with

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

Retained Theorem `thm:matrixcodec77` constructs a deterministic finite dictionary from public `(d,N,delta)`: enumerate a legal rational grid with denominator `ceil(32dN/delta)` and compare exact rational values of `Q_N^2`. Inward rounding and greedy assignment give operational error at most `11 delta/16`. Every fixed-length word decodes to a legal effect, including unused indices.

For fixed `d` in the stated small-error range, the optimal payload length is

\[
\frac{d^2}{2}\log_2N+
\lfloor d/2\rfloor\log_2\log(N+2)+d^2\log_2(1/\delta)+O_d(1).
\]

Corollary `cor:matrixlearnedcode77` runs learning and coding each at accuracy `delta/2`, giving total error at most `27 delta/32` on success. It attains the same training and payload orders with no additional device calls. The payload converse uses a fixed public decoder into legal memoryless ordered binary effects.

The exact dictionary construction is exhaustive. Its ambient candidate count is `(K+1)^d(2K+1)^{d(d-1)}`; storage uses `O(M_code d^2)` rational entries. Polynomial runtime and optimal workspace are not claimed. The statistical learner is specified and proved mathematically; a physical-device training implementation is not represented as executed.

### Sharp independent-block resource law

Theorem `thm:blocklearning78` specifies a training interface with fresh quantum blocks of at most `b` calls. Classical feedback, arbitrary storage of completed outputs, quantum instruments at block boundaries, and collective final processing are permitted. Until its last call, the entire current block, including its reference and unused probes, is isolated from older quantum registers. Block lengths are declared before execution and charged in full; their sum is bounded on every record.

For `d>=2`, `1<=b<=N`, small absolute `delta` and `0<eta<=1/8`,

\[
 c\frac{N^2}{b\delta^2}\log(1/\eta)
 \le M_b^\star(d,N,\delta,\eta)
 \le Cd^4\frac{N^2}{b\delta^2}\log(d/\eta).
\]

Thus fixed-dimensional minimax training has order `Theta_d((N^2/b) delta^-2 log(1/eta))`. The scalar `d=1` order remains `Theta(N delta^-2 log(1/eta))` independently of `b`. The upper proof uses `d_N<=ceil(N/b)d_b`; the lower proof uses a projective pair and a history-weighted root-fidelity potential. It includes conditional feedback and bounded stopping without treating the records as independent.

Independent Choi-pair acquisition followed by collective tomography belongs to `b=1`. Accordingly, the theorem gives a direct worst-case quadratic-horizon lower bound for this acquisition class on the complete binary effect body. This restriction is different from the number of already acquired output copies processed coherently in a final measurement.

`cor:blocklearnedcode78` combines this learner with the retained exact matrix codec, at no additional device calls and the same fixed-dimensional optimal payload order.

### Dimension, accuracy and the noisy interior

Lemma `lem:weakmeasurementinfo78` proves that a call to an effect `E_x=I/2+H_x`, `||H_x||op<=r`, increases information about a finite unknown label by at most `log(1+4r^2)`. The input may already be correlated with the label through earlier coherent adaptive calls. The proof calculates the noncommuting collision expression using support inverses and then applies the conditional information identity.

An operator-norm packing of real dimension `d^2` and a Bernoulli future-loss witness give Theorem `thm:dimensionlower78`:

\[
 M\ge c d^2N\delta^{-2},
 \qquad d,N\ge1,\quad0<\delta\le2^{-13},\quad0<\eta\le1/8.
\]

This lower bound already holds on `I/4<=E<=3I/4` and allows arbitrary coherent adaptive training. Together with the existing Mele--Bittel upper bound, it gives joint operator-norm learning order `Theta(d^2 epsilon^-2)` at fixed confidence (`cor:binaryoperatorlearning78`). No multiplicative confidence logarithm is inferred from the packing argument.

Lemma `lem:interiormetric78` proves a dimension-free comparison with `min(1,sqrt(N)||E-F||op)` when both effects lie in `[I/8,7I/8]`. Reanalysing the legal binary Choi estimator on the promised family `[I/4,3I/4]` then gives

\[
 M_{\rm int}^\star(d,N,\delta,1/8)
 =\Theta(d^2N\delta^{-2}),
\]

jointly in `d,N,delta`, with absolute constants (`thm:interiorlearning78`). The upper uses fresh one-call acquisition and collective final processing; the lower permits unrestricted coherent training. Existing tomography therefore does admit a linear-horizon analysis in this fixed interior. The projective boundary prevents that rate uniformly on the whole body for one-call acquisition.

In the common small-error range, full-body independent-block training has lower order

\[
 \delta^{-2}\bigl(d^2N+(N^2/b)\log(1/\eta)\bigr).
\]

The constructive full-body upper factor `d^4` remains unoptimized. The new sharp joint dimension law is explicitly the interior, fixed-confidence statement.

### Finite trusted preparation and control

Theorem `thm:finitecontrollearning78` gives finite classical specifications for the paper's common matrix and block learners. Run the ideal learner at the same loss target and failure `eta/2`; a total unhalved trace/diamond error at most `eta` on every record changes its output law in total variation by at most `eta/2`. The original `delta`, `eta`, block caps and call orders follow. Discontinuous decisions and failed records are included.

Algebraic basis selection, guarded phase roots, integer sample budgets, rational legalization and exact output legality are specified. Preparation and control approximations preserve tensor freshness and CPTP constraints. Direct descriptions can be exponential in block width; no efficient physical synthesis is asserted. This finite-control result concerns the paper's own explicit learners, not an additional implementation theorem for the imported collective Choi estimator.

## Manuscripts and review package

| File | Role |
|---|---|
| `paper.pdf` / `quantitative.tex` | Self-contained focused article: matrix geometry, entropy, common learning, exact coding, independent-block laws, dimension/interior results, finite control and complete qubit prerequisites |
| `STRUCTURAL_PAPER.pdf` / `structural.tex` | Independently complete structural companion with inherited hypotheses and proofs |
| `COMPLETE_REVISION.pdf` / `main.tex` | Complete research edition preserving the historical proof development and adding the new results |
| `RESPONSE_TO_REFEREE.md` | R01–R12, D01–D26, all 32 grouped pipeline gates and ten audit risks |
| `PROOF_AUDIT.md` / `PROOF_STATUS.json` | Proof dependencies, verification boundaries and exact claim status |
| `LITERATURE_AUDIT.md` / `INDEPENDENT_REVIEW_BRIEF.md` | Primary-source theorem comparisons and concrete specialist priority questions |
| `HISTORY_AND_PIPELINE_AUDIT.md` | Historical derivation routes and broader analytic programme status |
| `PRESERVATION_MANIFEST.json` / `PROOF_TEXT_PRESERVATION.json` | All 330 predecessor native files, all 707 complete-edition labels and explicit proof-text preservation |
| `RESOURCE_LEDGER.md` / `RESOURCE_LEDGER.json` | Training, horizon, block size, memory, preparation, payload, runtime and workspace |
| `evidence/JOURNAL_PACKAGE.zip` | Focused and structural articles, all active native TeX inputs and standalone verifier |
| `evidence/RESEARCH_PACKAGE.zip` | Complete native source, three PDFs and source-bound verification evidence |

All 707 predecessor complete-edition labels and all 205 predecessor focused labels remain active. The new mathematical sections are added to both source graphs. Every predecessor native file is preserved either at its unchanged relative path or, for revised editorial/tooling files, in `predecessor-v77-audit/`. The older 149-label relocation occurred in v77 and remains documented there; no further focused proof relocation is made in v78. Earlier manuscript directories and review branches remain unchanged.

## Exact arithmetic interfaces

`matrix_metric.py` computes exact pair-modulus certificates for Gaussian-rational matrices with full PSD tests and a rational Sylvester solve. It reports proved comparison bounds, never the exact adaptive optimum. See `MATRIX_METRIC_SCHEMA.md`.

`matrix_codec.py` implements the complete finite dictionary algorithm. See `MATRIX_CODEC_SCHEMA.md`. A small complete example is:

```sh
python matrix_codec.py encode --input examples/matrix-codec-scalar-source.json --horizon 1 --accuracy 1/2 > scalar-code.json
python matrix_codec.py decode --input scalar-code.json
python matrix_codec_check.py
```

`block_resource_check.py` adds finite exact horizon arithmetic, complete small GHZ laws, conditional branch potentials and noncommuting support-inverse identities. Its checks do not execute the statistical learners or certify continuum theorems.

Complete theorem dictionaries are executed in six scalar cases. Separate complete small two- and three-dimensional grids test enumeration and legality kernels; the actual two-dimensional theorem grid is checked on an explicitly identified finite prefix only. A resource cutoff returns an incomplete-construction error and emits no codebook or payload. Finite checks do not prove continuum covering or statistical risk statements.

## Reproduction and source identity

Use `requirements.txt`, pdfLaTeX with AMS and TikZ packages, and the recorded environment. From this directory:

```sh
python build_revision.py --isolated
python build_revision.py --verify-published
```

The builder runs the registered exact suites under ordinary and optimized Python with identical results, compiles three manuscripts, rejects unresolved references, citations and bad boxes, and checks every page for clipping. Isolated native-ZIP reconstruction must reproduce every page's text and raster. The journal verifier rebuilds both articles without a historical PDF, repository history or other external manuscript file.

`evidence/BUILD_RECEIPT.json` identifies the actual native-source commit. `SOURCE_HASHES.json`, `THEOREM_LOCATIONS.json`, `PAGE_CHECKS.json` and `PACKAGE_MANIFEST.json` bind sources and artifacts. Publication is a direct child of that source commit. The v78 GitHub Actions workflow checks the exact publication head read-only and attaches reconstruction receipts. An earlier revision's successful receipt is not evidence for this revision.

The revision branches are:

- `revision/general-theta-foundations-i-v78-r51-response-2026-10-04`
- `revision/general-theta-foundations-i-v78-native-source-2026-10-04`
- `revision/general-theta-foundations-i-v78-referee-ready-2026-10-04`

The ready alias is assigned after final-head verification. Independent human specialist priority judgment remains an explicitly uncompleted part of R02 / P01. Source hashes, internal proof checks and CI do not supply a human authorship signature, journal acceptance or A/B/C/D programme closure.
