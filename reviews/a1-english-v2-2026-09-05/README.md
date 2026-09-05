# A1 English-v2 independent referee review

**Recommendation:** Reject in the present form at the requested Annals / Inventiones / JAMS / Acta benchmark. This is an independent AI-assisted referee-style assessment, not an appointed journal review or editorial decision.

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md). The report distinguishes the main contribution/significance objection from three repairable statement-scope issues and a derived statistical separation result. It does not claim that the one-collision whole-preparation formula is false.

| File | Purpose |
|---|---|
| [REFEREE_REPORT.md](REFEREE_REPORT.md) | Detailed English report: verdict, main proof audit, explicit counterexamples and repairs, statistical singularity, literature comparison, and substantive revision requirements. |
| [CLAIM_AUDIT.md](CLAIM_AUDIT.md) | All 63 proof-bearing statements, with source anchors and individually qualified assessments. |
| [REVIEW_MANIFEST.json](REVIEW_MANIFEST.json) | Exact revision/source identities, review coverage, artifact hashes, and explicit limitations. |
| [referee_checks.py](referee_checks.py) | Independently written finite diagnostics; not the author's test suite. |
| [CHECK_RESULTS.json](CHECK_RESULTS.json) | Actual local execution receipt: 12 checks, zero failures/errors/skips, plus direct geometric sampling results. |
| [source/](source/) | Byte-identical frozen source tree actually reviewed, preserved as a Git subtree. |

## Which revision?

Revision branch: `revision/a1-english-v2-referee-2026-09-05`  
Observed/rechecked head: `c9455e8236ccc58137833402be8cd77bd25e62af`  
Frozen mathematical source tree: `900059b847980a27be4866d495b00eeb96562dc5`

At inspection, the branch's publication workflow had failed and the intended path `papers/A1-english-v2/main.tex` was absent. The report therefore audits the workflow-pinned source tree, not an imaginary successfully published PDF. Its unchanged contents are available here under `source/`. The workflow failure cause was not established by the returned run/job metadata.

No manuscript text, revision branch, main branch, or pull-request approval was changed by this review. The review branch adds this directory to the observed revision commit. No manuscript PDF build or author-suite rerun is claimed.

## Main findings

The single-collision tube identity and its stated weak distributional response appear sound under their printed smooth-density/test assumptions. The principal rejection reason is insufficient demonstrated depth and novelty of the integrated contribution. M1 concerns the unreset bias term in Proposition 4.4; M2 concerns density traces in Theorem 12.2; M3 concerns preparation regularity in Theorem 13.3. Their broad-reading counterexamples and narrower valid repairs are given explicitly.

S1 proves that the complete exact collision record has infinite cross-radius relative entropy and is not TV-continuous, despite its negative-Sobolev response. This does not invalidate the separate regular Bernoulli collision-bit experiment; it explains why those two experiments cannot be interchanged in a likelihood or control theorem.

## Reproduce the referee diagnostics

From this directory, with Python >=3.10, NumPy and SymPy installed:

```sh
python referee_checks.py --output CHECK_RESULTS.local.json
```

The committed script's Git blob hash matches the script executed locally. The committed receipt records its SHA-256 and environment versions. These finite checks are supporting diagnostics, not formal theorem verification or evidence of long-time response.
