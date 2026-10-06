# General Theta Foundations I — Revision 90, R59 response

**Primary manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*.

**Paper directory:** [`papers/GTF-I-v90-operational-memory`](papers/GTF-I-v90-operational-memory).

**Controlling report:** R59 at `a7d030d635a2bb40c8b4f7f2265df877bad95492`; companion proof/pipeline audit at `994c41dbeec1da13b6b6486876855fa30ad7cfd5`. Both reports are frozen verbatim in the paper directory. The four-leading-general-mathematics-journal objective and ordered-measurement topic are unchanged.

## Manuscripts and review route

| Object | File | Pages | Purpose |
|---|---|---:|---|
| Primary | [paper.pdf](papers/GTF-I-v90-operational-memory/paper.pdf) | 49 | Current article; start here |
| Current linked supplement | [BINARY_SUPPLEMENT.pdf](papers/GTF-I-v90-operational-memory/BINARY_SUPPLEMENT.pdf) | 87 | Dependency proofs and preserved auxiliary consequences |
| Independent structural article | [STRUCTURAL_PAPER.pdf](papers/GTF-I-v90-operational-memory/STRUCTURAL_PAPER.pdf) | 41 | Unchanged active structural source graph |
| Complete research edition | [COMPLETE_REVISION.pdf](papers/GTF-I-v90-operational-memory/COMPLETE_REVISION.pdf) | 263 | Full mathematical archive, not a second submission |

The [point-by-point response](papers/GTF-I-v90-operational-memory/RESPONSE_TO_REFEREE.md) addresses R01–R15 and D01–D30. The [pipeline derivation](papers/GTF-I-v90-operational-memory/PIPELINE_DERIVATION_V90.md) and [primary-source comparison](papers/GTF-I-v90-operational-memory/LITERATURE_AUDIT.md) give the dependency and literature routes.

The principal mathematical response to the score-separation objection is **Theorem 15.2, page 39**, with the filtered-swap identity and equality characterization in **Lemma 15.3**. The complete unit-reset upper includes arbitrary receiver instruments, classical feedback and unrestricted receiver dimension. The all-adaptive upper derives its positive tester blocks, positive complements and causal marginals directly from a physical circuit. Independent maximally entangled pairs and an antisymmetric two-input state attain the respective upper bounds. The seven-device qubit instance gives `3/5 < 13/20 < 4/5`. Corollary 15.5 supplies the perturbation margin; Proposition 15.6 normalizes arbitrary real hard thresholds.

The game is a binary decision on a finite ensemble whose device index is selected once for both calls. The single-call averaged channels coincide. No arbitrary fixed-pair theorem or complete ancillary-dimension hierarchy is inferred.

Numbering note: historical response and pipeline references such as “Section 82” use **source-module indices**. `sections/82-operational-memory-hierarchy.tex` compiles as Section 15 in the primary and Section 81 in the complete edition. The printed theorem/page mapping is recorded in `evidence/THEOREM_LOCATIONS.json`.

## Exact source and publication identities

- Native source: `e9f9673d7648c64e167994533e4b6f8a859fc2be`, branch `revision/general-theta-foundations-i-v90-native-completion-2026-10-06`.
- Artifact-only publication: `80e543020199edd7e9b9c908c78410aef7ae4dd6`, branch `revision/general-theta-foundations-i-v90-publication-completion-2026-10-06`.
- Completion branch: `revision/general-theta-foundations-i-v90-r59-completion-2026-10-06`.

The qualified native build passed all 30 suites normally and under `python -O`, with identical results, a complete isolated source reconstruction and a standalone journal-package reconstruction. Its [build receipt](papers/GTF-I-v90-operational-memory/evidence/BUILD_RECEIPT.json) records 746 native files, all 710 predecessor files preserved in active or byte-identical audit paths, and all 998 predecessor complete-edition labels retained. Old proof paragraphs are retained; the 40 relocated labels remain in the current linked supplement. There are no unresolved references/citations or reported overfull/underfull boxes. The complete-edition log retains three font-expansion warnings; it is not described as warning-free.

### Actual transport record

Actions run `37391691284`, job `112038006854`, completed the native build and both reconstructions, created the exact commits above, and uploaded artifact `11381328726` (`ca981b6466a844813e912b7b8dc7221c3f0f2f2d4e4470c8403efa3edf9820a2`, SHA-256). Its **overall conclusion is failure**: the final atomic ref update was rejected after GitHub timed out checking workflow permissions on the two new refs. This is not a successful publication-job badge.

The GitHub API subsequently confirmed that the exact publication object and native parent existed on the server. The native and publication refs were created through the connected GitHub API; the completion ref was then fast-forwarded from the checked expected SHA `981fd0bf62096d1d71abff95b0c530127f8af573`, without force, to the same publication object. No manuscript, build receipt or publication byte was changed in this handoff. The API handoff was sequential, not atomic. This actual transport record supersedes the prospective atomic-push description in the native release notes. It does not reuse the earlier failed v90 artifact as qualification.

## Final-head qualification

`GENERAL_THETA_FOUNDATIONS_I_V90_FINAL_HEAD_REQUEST.json` is a metadata-only request, not a success certificate. The `final-head` job in `.github/workflows/gtf-v90-completion.yml` checks out the triggering SHA with read-only permissions and no persisted write credentials, executes `build_revision.py --verify-published`, reconstructs the native and standalone journal archives, checks all submitted hashes and uploads `gtf90-completion-exact-final-head-<SHA>`. Only an actually successful job and matching `verified_head` receipt qualify that exact final SHA. The review-ready alias is assigned to that SHA only after the receipt is observed. No receipt is committed back to the head it verifies.

For an independent local replay at the selected review head:

```sh
python papers/GTF-I-v90-operational-memory/build_revision.py --verify-published
```

Use the [standalone journal package](papers/GTF-I-v90-operational-memory/evidence/JOURNAL_PACKAGE.zip) for the linked article submission or the [complete research package](papers/GTF-I-v90-operational-memory/evidence/RESEARCH_PACKAGE.zip) for the full audit trail.

Neither reconstruction nor the internal proof audit is an independent human priority opinion. R59's R04/P05 therefore remains an external specialist-review question. The earlier referee's venue judgment is retained for reconsideration against the new theorem; it is not redescribed as acceptance. No main-branch merge, review-branch rewrite, physical-reset calibration or unrelated Theta-program analytic closure is represented by this revision.
