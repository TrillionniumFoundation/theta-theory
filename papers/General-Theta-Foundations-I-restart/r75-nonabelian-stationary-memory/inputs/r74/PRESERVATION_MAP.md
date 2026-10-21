# Preservation and mathematical authority — General Theta Foundations I, R74

R74 continues the complete R73 native source at commit
`e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`; its publication/base commit is
`39980d65d6665e52c30aa340cfb0e2eb199c0f9a`. Both contain the same **156-file**
paper tree, `0507d04ad0bebd20cb0ce609ab94f7cc67d11f56`, at
`papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form`.
The native source identity, rather than a version label or publication time,
controls this map.

## Complete file preservation

[R73_FILE_PRESERVATION.json](provenance/R73_FILE_PRESERVATION.json) lists **all
156 original files**, their original repository paths, Git modes, Git blobs,
byte counts and SHA-256 hashes, and their exact preserved paths within R74.
Every selected copy was compared byte for byte with its fixed Git blob.

| Preservation location | Files | Meaning |
|---|---:|---|
| Unchanged current file | 108 | Original bytes at the same relative source path. |
| Existing exact `inputs/r73/` archive | 44 | Replaced wrappers, records and other original material. |
| `inputs/r73/superseded/` | 4 | Original `THEOREM_MAP.md`, `references.tex`, `sections/01-current-overview.tex` and `sections/36-current-consequences.tex`, recovered directly from fixed Git blobs. |
| **Total** | **156** | **No missing original file; no byte-identity failure.** |

The old map is preserved at
[inputs/r73/PRESERVATION_MAP.md](inputs/r73/PRESERVATION_MAP.md). Original
wrappers, overview, conclusions, bibliography, responses, manifests, proof
ledgers and theorem maps remain recoverable. The R73 sibling and earlier
source folders remain unchanged; no recursive historical tree was copied
again merely to provide a new revision directory.

Three additional checks establish current source continuity:

| Retained object | Identity check |
|---|---|
| 47 native proof/support files | Every entry of [CURRENT_RETAINED_BODY_IDENTITIES.json](provenance/CURRENT_RETAINED_BODY_IDENTITIES.json) matches its original R73 Git blob and current bytes. These include theorem sections, seven technical supplement inputs, the figure and preamble. |
| 34-file independent companion | The complete current `companion-r58/` tree, including file modes, recomputes to `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`. |
| Original inline supplement proof sequence | From `\section{The finite Hankel determinant used by the new hierarchy}` to the end of `supplement.tex`, **32,284 bytes** remain identical; SHA-256 `a1505059fc305c8918875445ca07b5c69e79b16f1d247e402bad8089b101ead7`. The current assembly adds material before this sequence. |

These are byte-preservation checks. Proof correctness, compilation, independent
expert assessment and editorial decisions are different questions. Their
actual status belongs to the current proof audit and verification records.

## Mathematical families and current source authority

Section filenames below are under `sections/`; other paths are relative to
this directory. The main article and current technical supplement assemble
the complete proof bodies. The current [THEOREM_MAP.md](THEOREM_MAP.md),
theorem index and dependency map control current statement numbers and
hypotheses. Historical numbering and obsolete open-status wording remain
history, even where their original files are retained.

| Mathematical family | Complete current source bodies | Scope and continuity |
|---|---|---|
| Causal experiments, paid acquisition, actual-history comparison and common upper bound | `02-experiments.tex`, `03-main-theorem.tex`, `04-proof.tex` | General experiment statements retain their legality, resource and quantifier conditions. |
| Predictable state, information compression and task order | `A-predictive-quotient.tex`, `05-task-order.tex`, `14-reusable-continuation.tex` | Fixed-law, task-specific and universally predictive quotients retain different quantifiers. |
| Acquired geometry, singular and mixed strata, realizations and composition | `06-geometry.tex`, `07-realizations.tex`, `08-composition.tex`, `18-strata-phase.tex`, `B-boundaries.tex` | Local geometry retains its local hypotheses; implementation and calibration assumptions remain explicit. |
| Causal synthesis, finite-width defects, general loss and selection | `09-causal-synthesis.tex`, `10-width-defect.tex`, `11-loss-transfer.tex` | Fixed-dictionary convexity and optimization with a hard width constraint remain separate results. |
| Finite memory, continuation and zero-risk spectra | `12-finite-memory.tex`, `14-reusable-continuation.tex`, `15-zero-spectrum.tex` | Corrected support, compactness and zero-risk hypotheses remain controlling. |
| Rank-constrained discrimination, variational and spectral principles, two-stage reset and communication | `13-two-detectors.tex`, `16-reset-control.tex`; independent sources below | Arbitrary-rank pair detection and exact special-model formulas remain complete. Original rank cuts, reset experiments and communication interfaces are retained. |
| Performed-law compactness, risk attainment, primal-dual principles and sparse witnesses | `17-primitive-risk.tex`, `19-compact-risk.tex`, `20-primal-dual.tex`, `supplement-primal-dual.tex` | The full inherited proof chain remains active. A dual-support atom is not automatically a controller state. |
| Timing, boundary memory, robust ties, stopping rigidity and squared-sign models | `21-timing-memory.tex`, `22-boundary-memory.tex`, `23-robust-realization.tex`, `25-stopping-rigidity.tex`, `26-squared-memory.tex`, `27-r66-technical.tex` | Proven unique-decision and rigid-herald results retain their hypotheses; tied probability laws are not silently determinized. |
| Interior instrument simulation and physical dictionaries | `27-interior-instruments.tex`, `supplement-interior.tex`; bridge `39-instrument-realization.tex` | The R68 uniform-interior theorem, algebraic construction, small-noise exponent, several anchors and block extension were already proved. R74 preserves them without claiming a new discovery; superseded rediscovery drafts are identified under `provenance/author-research/superseded/`. |
| Spectral memory, leakage, arithmetic envelopes and growth spectra | `28-spectral-memory.tex`, `29-leakage-memory.tex`, `30-diophantine-spectrum.tex`, `supplement-spectral.tex`, `supplement-leakage.tex`, `supplement-arithmetic.tex` | All spectral, probability and arithmetic hypotheses remain. No unproved irrationality exponent is assigned to `(3+4i)/5`. |
| Compact reversible response, periodic memory, stochastic normal form, optimal core and rigidity | `31-reversible-control.tex`, `32-periodic-memory.tex`, `33-reversible-normal-form.tex`, `supplement-r72.tex`, `supplement-normal-form.tex` | Complete R72/R73 structure and exact examples are inherited. The normal form and counted initializer remain inputs to the contrast theory. |
| Algebraic decision and synthesis; finite nonrealizability and robustness certificates | `34-algebraic-synthesis.tex`, `35-finite-certificates.tex` | Exact algebraic inputs, compact reversibility and finite-probe scope remain explicit; no arbitrary-series decision or complexity optimum is asserted. |
| New terminal-contrast structure and sharp finite-group transitions | `37-contrast-memory.tex`, `38-quotient-memory.tex` | Small-positive-contrast saturation applies to any finite observable group. Quotient absorption requires normal stabilizers; the exact group-wide LP theorem assumes every subgroup normal. The `S_3` and `(F_2)^4` formulas are complete specified families. |
| Common contraction and conditional quantum-memory obstruction | `40-joint-contraction.tex`, `41-conditional-memory.tex` | The contraction certificate makes the classical invariant-polytope mechanism explicit. The qubit family combines rank three, uniformly positive outcomes, exact average depolarization and one-dependence with its exact finite-order or infinite-memory conclusion. Earlier peripheral-phase and finitely dependent non-HMM results receive priority credit. |
| Four-period damping closure | `supplement-r74-period-four.tex` | The threshold `1/sqrt(3)` is an explicit consequence of the retained first-sector theorem, not a new discovery. |

Earlier unassembled introductory inputs (`00-current-contributions.tex`,
`01-introduction.tex`, `01b-literature.tex`, `01c-assumption-flow.tex`,
`01d-decision-order.tex`) retain their original bytes as source history.
Their old contribution or status wording does not supersede the current
overview, response, priority analysis or research-status document. The
inherited scope inputs `C-scope.tex` and `D-current-scope.tex` remain in the
current supplement.

## Independently compilable companion and earlier source tree

`companion-r58/` preserves all 34 files of
`papers/General-Theta-Foundations-I-restart/r72-reversible-memory/retained/r58-native`
at commit `5463d93f0f22a7459efba8c44af1f8b326d92c34`, tree
`007a1d7d5f5b880c670fc6f47a812ebd476bfb00`. Proofs, bibliography,
diagnostics, lineage and the earlier response remain byte-identical. Its
absolute-calibration and nonintervening directional-sensing results retain
their own experimental and resource assumptions. This is a separate native
companion, not a new R74 contribution. Its actual compilation status belongs
to the current build receipt.

The complete R72 source remains pinned at the same commit, path
`papers/General-Theta-Foundations-I-restart/r72-reversible-memory`, tree
`5449385c491b0ef60a7744dcaa744f52d1e251fe`. Its recursive history remains in
place. The earlier preservation maps and current full-history inventory
provide traceability without another recursive copy into R74.

## Original finite-order measurement and reset sources

These are actual immutable native repository identities. Their trees were
rechecked in the current inventory.

| Preserved line | Commit and native repository path | Tree |
|---|---|---|
| TR-OMG-1: ordered finite-use measurement and resource geometry | [`df7ed618813224b058b97c6cbda720ad936e2c53`, `papers/GTF-I-v89-resource-profile`](https://github.com/TrillionniumFoundation/theta-theory/tree/df7ed618813224b058b97c6cbda720ad936e2c53/papers/GTF-I-v89-resource-profile) | `fd01ad0775aa4a807267e070e047a3b2ab16a875` |
| TR-OMD-1: ordered measurement discrimination and reset memory | [`ca5aa12d0a77c07e815639199eeb185b6d7a0f1c`, `papers/GTF-I-v96-referee-resolution`](https://github.com/TrillionniumFoundation/theta-theory/tree/ca5aa12d0a77c07e815639199eeb185b6d7a0f1c/papers/GTF-I-v96-referee-resolution) | `0b21c654dd51c9582d7b0c34a87cf1c8e224dac0` |
| Complete v96 native mathematical resolution | [`d19a424f19ab5c1492b621a55bb3c8a20de7392d`, `papers/GTF-I-v96-referee-resolution`](https://github.com/TrillionniumFoundation/theta-theory/tree/d19a424f19ab5c1492b621a55bb3c8a20de7392d/papers/GTF-I-v96-referee-resolution) | `8781d9c11be56ab5306594523f267c824397f709` |

The v96 publication commit `30449959be3565d16031af69da86ed26d3ad422b`
does not replace its native source commit. The frozen v2–v96 development
archive remains at `e38f757ee13158c315e9328c961eb84e3e9a000d`.

The v96 no-message result is not restricted to the old equal-prior example.
For each fixed pure acquisition under its full old-support condition, the
labelwise continuation-function concavity criterion has its stated
necessary-and-sufficient scope. The nonconcavity instrument witness, old-cut
rank restrictions, support-inverse optimizer and local water-filling geometry
remain separate proved results. The v95 local equal-prior calculation remains
an additional special case. R74's response-memory theorems do not replace
these independent results.

## Historical evidence and current authority

The current controlling records include `provenance/BASELINE_LOCK.json`,
`BASELINE_AUDIT.md`, `BASELINE_REFRESH_RECEIPT.json`,
`BASELINE_SOURCE_IDENTITIES.json`, `CURRENT_REFS.json`,
`REFEREE_STATUS_AT_BASELINE.md` and `current-full-scan/`. The deposited R65
report and its receipt and commit retain their original identities.
Historical responses and author-team AI challenges remain evidence of the
stated kind; they do not become independent human referee reports.

Twenty historical provenance files or aliases, including an explicit R73
delivery alias, have exact verified copies under `inputs/r73/provenance/`.
The inventory lists their canonical archival locations after comparison with
the original Git objects. Old control objects, branch snapshots, scans,
challenges and delivery records remain historical evidence. Their canonical
archive paths control preservation regardless of whether a redundant copy
also exists at a former active path; this inventory does not assert that
such duplicate paths are absent.

A1/A2, B4/C2 and the eleven-paper Theta pipeline retain their independent or
unproved dependencies. Process limits, nonlinear generators, filtering LAN
and posterior contraction are not upgraded by the present finite-memory
results. The General Theta Foundations I identity and the Annals / Acta /
Inventiones / JAMS objective remain intact; byte preservation and finite
diagnostics provide no editorial endorsement.
