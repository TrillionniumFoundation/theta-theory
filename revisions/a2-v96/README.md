# A2 revision 96: review hand-off

**Branch:** `revision/a2-v96-uniform-stratified-spectral-laws-2026-09-20`  
**Baseline:** `ebb796e49ca51a62b90d92ec0d09819cfe8d00a4` (revision 95)  
**Controlling review:** `dbbad2d84c6a3b358bddabf84dc16f0b09b38634`, `reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`  
**Complete manuscript:** `papers/A2-v17-boundary-information-coarsening/rigidity_v96.tex`  
**Response:** `revisions/a2-v96/RESPONSE_TO_REFEREE.md`

The new main results classify the full identifiable portion of the named boundary cubic family across both first-channel ranks, prove a whole-model uniform expansion `omega_theta(t)=C(theta)sqrt(t)+O_H(t)`, and give a finite semialgebraic active-set partition on which `C^4` is rational. The weight-isolated region is included. All inherited mathematical and bibliography inputs remain active and byte-identical; all old entrypoints and review branches remain unchanged.

## Build and verify

From the repository root:

```sh
python -m pip install numpy scipy sympy
python scripts/audit_a2_v96.py --output build/a2-v96/source-receipt.json
python scripts/verify_a2_v96_math.py --output build/a2-v96/math-diagnostics.json
python scripts/exact_a2_v96_constants.py --output build/a2-v96/exact-constants.json
cd papers/A2-v17-boundary-information-coarsening
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -file-line-error rigidity_v96.tex
cd ../..
python scripts/audit_a2_v96.py \
  --fls papers/A2-v17-boundary-information-coarsening/rigidity_v96.fls \
  --log papers/A2-v17-boundary-information-coarsening/rigidity_v96.log \
  --pdf papers/A2-v17-boundary-information-coarsening/rigidity_v96.pdf \
  --output build/a2-v96/full-build-receipt.json
```

The branch-scoped workflow `.github/workflows/a2-v96-native.yml` runs these commands. It rejects changes outside the new revision files and any loss of inherited active inputs. Its receipt binds source hashes, the compiled input graph, log and PDF to runtime HEAD. Check the workflow conclusion and receipt at the actual reviewed SHA; a pending run is not a successful full build.

## Locally available evidence

`LOCAL_VALIDATION.json`, `MATH_DIAGNOSTICS.json` and `EXACT_CONSTANTS.json` record the evidence obtained during preparation. The separately marked `family_core_v96.tex` is an eight-page reading copy of only the new family arguments. That copy compiled cleanly and all its pages were visually inspected. It omits the retained general real-valuative theorem and appendices, and must not be represented as the complete paper. The full manuscript and exact-checkout source audit were not executed in the local staging directory.

Complete proofs are provided for independent mathematical scrutiny. Source audits, exact example calculations and finite regressions are not general proof verification, and no journal acceptance or independent referee approval is claimed.
