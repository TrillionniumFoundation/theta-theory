# A2 revision 100

Principal entry: `papers/A2-v17-boundary-information-coarsening/rigidity_v100.tex`.
The article is `article/v100/paper.tex` relative to that directory.
The archive entry is `rigidity_v100_archive.tex`; the complete entry is `rigidity_v100_complete.tex`.

Read `RESPONSE_TO_REFEREE.md` for the pointwise response, `SOURCE_MANIFEST.json` for source pins, and `LOCAL_VALIDATION.json` for the exact boundary of executed validation.

## Reproduction from the repository root

```sh
gzip -dc revisions/a2-v100/EXACT_DIAGNOSTICS.json.gz > revisions/a2-v100/EXACT_DIAGNOSTICS.json
python -m pip install sympy==1.14.0
python scripts/verify_a2_v100_math.py --output a2-v100-artifacts/EXACT_DIAGNOSTICS.json --check revisions/a2-v100/EXACT_DIAGNOSTICS.json
python scripts/audit_a2_v100.py --source-only --output a2-v100-artifacts/SOURCE_RECEIPT.json
python scripts/build_a2_v100.py
python scripts/audit_a2_v100.py --output a2-v100-artifacts/RUNTIME_RECEIPT.json
```

The JSON archive is deterministic gzip with timestamp zero. It expands to 26,929 bytes with SHA-256 `02d4c016514a1d20b9e6716cfee6ab2453d335fe9ff3bd9621f9d60761a90213`. Its Git blob is `e988807eca572daf4ad7876a20aca18c1b263cad`. The expanded JSON is a generated working copy, not a replacement for the committed lossless record.

Native dependencies: Python 3.10 or later, SymPy 1.14.0, latexmk, pdflatex, the standard LaTeX extra/science and recommended font packages, lmodern, and pdfinfo. The workflow installs these dependencies. No shell escape, branch mutation, or automatic merge is used.

The archive includes v99 complete, which includes v98 complete, v97 complete and the v96 historical source graph. The recursive builder handles these PDF dependencies before compiling the new wrappers. Every inherited source remains unchanged.

A workflow definition is not a build result. Only a completed head-bound runtime receipt records an actual principal/archive/complete native build. No such success is asserted by the local validation record.
