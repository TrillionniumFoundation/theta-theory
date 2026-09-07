# A1 English v25

## Attainable information, exponent collisions, and adaptive order

This revision responds to the v24 independent referee report. It retains the complete v24 scalar classification and its companion, and adds a graph-batch experiment, an adaptive-order converse, and a resolution-dependent ordering transition. It does not present deterministic shared-memory composition or classical cutwidth as newly discovered results.

## Immutable source basis

| Role | Commit |
|---|---|
| Controlling review | `c7fee8b92fd779573bd3b9ccdf5e37183c5cefa6` |
| Reviewed v24 submission | `6f648bc3da0543e8361b4053ae7da33cb172f597` |
| Earlier shared-memory development, Sections 8–9 | `da5abea9f40244879115d5fbcfbda375bc9a123e` |

The controlling report is `reviews/a1-english-v24-harsh-independent-2026-09-07/REFEREE_REPORT.md` in this branch's base history. Its Git blob is `f1e6cdf0aa308171977678ed3fcc9ee6b3521e30`.

The native `papers/A1-english-v24` tree is `79d66f7b4fd132923d28068f283b88f59276ec21`. The earlier shared-memory source is on `revision/a1-english-v10-shared-memory-composition-2026-09-06`, not the different v10-effective branch. It is cited at its immutable commit, not claimed to have been copied into this directory.

## Manuscripts and preservation

The principal entry point is [main.tex](main.tex). The additional introduction and all new statements and proofs are ordinary LaTeX files under [v25](v25). The original introduction, scalar experiments, attainable-image geometry, complete collision flags, checkpoint classification, causal realization, and collision-phase proofs are included from the unchanged sibling `../A1-english-v24` directory. The original principal theorem's concluding proof is retained verbatim in the new entry point.

The complete companion entry point remains [the unchanged v24 companions.tex](../A1-english-v24/companions.tex), with all of its source dependencies retained. The build materializes it alongside the revised main volume; the adaptive theorem does not acquire a new dependency on companion-only results. Source sharing is explicit: the original manuscript is not replaced by a synopsis, and the new directory is not falsely described as a byte-for-byte duplicate of the entire historical tree.

`build_v25.py` copies the immutable v24 dependencies into this revision's generated `build-v25/source` directory, overlays the additions, and builds both volumes there. It never rewrites the original v24 directory or the referee report. It also emits expanded LaTeX for continuous reading. Source-block counters compare the complete v24 main-plus-companion statements, proofs, definitions, remarks and labels with their revised counterparts, including multiplicities.

## Reproduction

From a checkout containing this branch:

```sh
python papers/A1-english-v25/build_v25.py --prepare-only
python papers/A1-english-v25/diagnostics.py > /tmp/a1-v25-diagnostics.json
python -O papers/A1-english-v25/diagnostics.py > /tmp/a1-v25-diagnostics-optimized.json
cmp /tmp/a1-v25-diagnostics.json /tmp/a1-v25-diagnostics-optimized.json
python papers/A1-english-v25/build_v25.py
```

The build needs Python 3.10 or newer and the same TeX/document utilities as v24. Native checkouts are checked against the pinned v24 tree and tracked working bytes. An offline source package is explicitly identified as such rather than being certified as a locally verified native Git tree.

A successful preparation writes `PRESERVATION_REPORT_V25.json`. A successful complete build writes `BUILD_REPORT_V25.json`, `main.pdf`, `companions.pdf`, `main-expanded-v25.tex`, and `companions-expanded-v25.tex`. Failure writes `BUILD_FAILURE_V25.json` and exits nonzero. A receipt is evidence only for the exact source hashes it records. Merely providing these commands or a build script is not a claim that a fresh run succeeded. Previously generated v24 PDFs and receipts are not v25 validation.

The inherited builder retains its checks for unresolved references, duplicate labels, overfull boxes and unsettled cross-volume references. Its historical source audit remains labelled by its original lineage inside the new receipt. No GitHub Actions success, independent v25 referee review, or formal proof certification is asserted by this source release.

## Mathematical reading order

Read the retained scalar classification first. Then read `v25/graph_model.tex` for the exact batch resources, query construction, risk quantifiers and deterministic product reduction; `v25/adaptive_proof.tex` for the regular box, common report-bearing subevent and finite-trace converse; and `v25/graph_consequences.tex` for the bit law, fixed-calibration exponent and three-edge ordering transition. The detailed review response and proof-obligation ledger are separate from the mathematical exposition.

The new graph theorem assumes independent edge priors, exogenous commands, fixed graph/horizons, and vertex-batch memory checkpoints. These are explicit hypotheses of a new experiment. They do not weaken or replace the retained scalar theorem with its original raw-trial resource convention. Constants are uniform in calibration and integer memory budget, including exact collisions, but are not claimed uniform in graph size.

Finite diagnostics check capped profile algebra, exact collision orders, small graph layouts, actual normalized-volume samples and negative controls for conditioning and quantifier mistakes. They do not prove the continuum theorem or settle journal significance. Whether the added structural result changes the referee's significance assessment remains a matter for the next review.
