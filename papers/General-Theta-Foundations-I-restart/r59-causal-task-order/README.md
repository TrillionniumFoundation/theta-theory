# General Theta Foundations I — restart revision R59

**Referee entry:** `main.tex`, built as `artifacts/General_Theta_Foundations_I_R59.pdf`.
**Complete mathematical companion:** byte-preserved `retained/r58-native/main.tex`, built as `artifacts/General_Theta_Complete_Companion_R58.pdf`.

This is a new Foundations manuscript written from canonical restart `18000b21e4bfd89180ccb069e46ac0f21621f34d`, not a v96 copy or a new continuous legacy version. The title and mother problem are unchanged. The latest completed referee report at initial inspection is pinned at `73d3876b1186672d83ab2df515221bff2abd391f` and reproduced in `inputs/review/`. The subsequent R57 and R58 research mathematics is explicitly inherited, not counted as R59 novelty.

The central theorem proves affine task-order resource transfer on actual causal occupation. Its new consequences are fixed-relative-error all-scale transfer, raw singular task-order certificates, a mixed-dimensional acquired-mass law, constructive positive-evidence quotient realization, and guarded finite command calibration. Source-built finite tests do not certify continuum proofs or journal significance. `PROOF_LEDGER.md` and `SCOPE_AUDIT.md` identify the exact established statements and remaining research questions.

## Rebuild

Use Python 3.12 on Linux x86_64 and TeX Live with amsart, lmodern, mathtools, microtype, booktabs, geometry and hyperref, plus `pdftotext`/`pdfinfo`.

```bash
python3 -m venv /tmp/theta-r59-env
/tmp/theta-r59-env/bin/python -m pip install --require-hashes -r requirements.lock
/tmp/theta-r59-env/bin/python verify.py
OPENBLAS_NUM_THREADS=1 /tmp/theta-r59-env/bin/python regression.py > /tmp/r59-normal.json
OPENBLAS_NUM_THREADS=1 /tmp/theta-r59-env/bin/python -O regression.py > /tmp/r59-optimized.json
cmp /tmp/r59-normal.json /tmp/r59-optimized.json
/tmp/theta-r59-env/bin/python build.py --out /tmp/r59-build
```

For a read-only committed-source rebuild, run `python rebuild.py --source <source-commit> --out /tmp/r59-clean --against /tmp/r59-build`. The dedicated GitHub workflow repeats this from a fresh runner with read-only repository permissions.

Other Python/platform wheel selections use `requirements.txt` and require their own environment receipt; the provided hash lock targets the recorded platform. `verify.py --seal` is an explicit maintainer operation which regenerates the outer source manifest; a reviewer should run `verify.py` without it. Original retained build/verification scripts and their old manifests are preserved historical inputs, not the entry points for this packet.

`artifacts/BUILD_RECEIPT.json` binds the source commit and document hashes. `evidence/` binds ordinary/optimized regressions, clean-source rebuild and final read-only publication checks. Each stage names its preceding SHA; no receipt purports to contain its own commit hash. The final referee-ready ref is an assembled review package, not a claim of mathematical acceptance.

## Long-term control

The authoritative starting branch remains `foundation/general-theta-foundations-i-restart-2026-10-06`. Its four controlling files are preserved as pinned inputs, unmodified at their original paths. New work must keep prepared causal experiments, executable future tests, predictive quotient, resource-certified causal morphisms, actual acquisition geometry and resource–resolution–risk transfer in that order of mathematical responsibility. A realization does not become the mother theorem merely by changing its title. Historical review, realization and frozen archive refs are not rewritten. Every successor must preserve substantive mathematical material, distinguish inherited results from new proofs, and expose remaining gaps without replacing the mother problem by a survey or a narrower topic.
