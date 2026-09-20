# A2 revision 102 — referee entrypoint

**Title:** Intrinsic metric data and cancellation laws for polynomial observations.

**Branch:** `revision/a2-v102-intrinsic-metric-contact-walls-2026-09-20`.

**Controlling review:** `9e7caa42cce40587828f7e8357c119e127a56805`, reviewing v101 source `d1654974140410eb356240d3121c5f36267a89d2`.

Start with [the new principal source](papers/A2-v17-boundary-information-coarsening/article/v102/paper.tex) and [the point-by-point response](revisions/a2-v102/RESPONSE_TO_REFEREE.md). The central results are the canonical residual-tensor envelope, the exact finite ray-probe criterion and adaptive metric-class lower bound, the endpoint effective metric, and the cancellation-uniform polynomial probability wall theorem.

The principal entrypoint is `papers/A2-v17-boundary-information-coarsening/rigidity_v102.tex`. The `_supporting` entrypoint retains the complete reviewed v101 article. The `_archive` entrypoint retains v101 and its entire historical archive. The `_complete` entrypoint includes the new principal followed by that archive, with no deletion or duplicate supporting volume.

Local principal compilation and finite diagnostics are recorded in [LOCAL_VALIDATION.json](revisions/a2-v102/LOCAL_VALIDATION.json) and [EXACT_DIAGNOSTICS.json](revisions/a2-v102/EXACT_DIAGNOSTICS.json). They do not certify the full historical build or the mathematical proofs. The branch-scoped native job writes `revisions/a2-v102/native/RUNTIME_RECEIPT.json` only after successful principal/supporting/archive/complete compilation and source binding. A queued workflow is not a successful receipt.

Reproduce the finite diagnostics:

```sh
python3 scripts/check_a2_v102.py --output /tmp/a2-v102-exact.json
```

Build the principal alone:

```sh
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v102.tex
```

Build and bind the full native graph from the repository root:

```sh
python3 scripts/build_a2_v102.py --dry-run
python3 scripts/build_a2_v102.py
```
