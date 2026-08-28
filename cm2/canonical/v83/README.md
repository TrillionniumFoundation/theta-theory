# CM2 v83 unified single-tree publication

This directory joins the original `main`, PR #1 and recovered local Library materials through v82 without rewriting either Git parent.

Start at `canonical/CM2_UNIFIED_TREE_INDEX.md`.

The tree distinguishes exact PR sources, exact local-Library report bytes, exact intermediate documents and non-authoritative reconstructed chronology. Eight exact reports are stored in a deterministic tar.gz represented by ordered base64 parts; the builder and verifier reconstruct and hash-check it. v79 remains preserved historically but is `WITHDRAWN_LATEST_WINS`; the controlling positive boundary remains `ACTUAL_LOCAL_PACKETS_REQUIRED`.

```bash
python3 tools/cm2-scripts/verify_unified_tree.py --repo .
python3 cm2/canonical/v83/build_v83.py --out /tmp/cm2-v83 --self-test
```
