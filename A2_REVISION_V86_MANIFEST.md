# A2 revision 86 — shared apparatus, singular transition, divisor--period classification

Branch: `revision/a2-v86-shared-nuisance-singular-transition-2026-09-18`.
Base: controlling v85 review commit `65cd70c44e1bb5f679bd3e0397c6d66da139102c`.
Reviewed v85 manuscript: `4f3d2ab5259b8deda67e1ec6ea9a6151a405ddd4`.

## Reading entry points

All manuscript paths below are under `papers/A2-v17-boundary-information-coarsening/`.

- `rigidity_v86.tex`: complete principal manuscript; new theorems followed by the complete v85 principal body.
- `rigidity_v86_full.tex`: the identical principal body followed by every preserved companion input.
- `rigidity_v86_core.tex`: self-contained new-results extract, explicitly labelled as an extract.
- `article/v86/02_shared_nuisance.tex`: sharp two-clock shared-apparatus action/metric theorem and one-clock metric alternative.
- `article/v86/03_singular_transition.tex`: determinant-product inverse modulus, honest adaptation and matching singular lower bounds.
- `article/v86/04_meromorphic_structure.tex`: compact-real-surface divisor--period detector classification and sufficient intrinsic clock budget.

Response: `reviews/a2-v86-response-to-v85-2026-09-18/RESPONSE_TO_REFEREE.md`.

## Non-destructive construction

No inherited file is replaced. Both new complete editions use `article/v86/principal_body.tex`, which includes the unchanged `article/v85/principal_body.tex`. Only its first heading is contextually renamed by a TeX wrapper. The expanded companion's input order is preserved. Old theorems, hypotheses and historical derivations remain available in their original files and in the new assembled editions.

## Reproduction

From the manuscript directory, with Python, NumPy, SymPy and a native TeX installation:

```sh
python verification/verify_v86.py --output verification/v86-verification.json
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v86.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v86_full.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v86_core.tex
```

The source check requires the controlling base commit in the local Git object store. A standalone new-core checkout can instead use `--core-only`; that mode deliberately does not report inherited-source verification.

## Evidence at source preparation

The new core passed symbolic and numerical diagnostics and native compilation (15 pages), with resolved references/citations and rendered-page inspection. `verification/v86-core-verification.json` records the exact scope and source hashes. The diagnostics are not mathematical proof certification. A separate branch-specific workflow checks all three editions and all inherited paths. Its native result, logs and source SHA are the authority for the full build; the core result alone is not a claim that the full principal or expanded build passed.

## Scope of the mathematical additions

The shared theorem shares the detector's relative throughput as well as its clock dependence; both readout channels remain unknown and spatially variable. The singular exponent is established for binary channels and a constant relative detector with three clocks. The intrinsic meromorphic clock count is sufficient, not a universal optimal count. Classical geometric rigidity and stability inputs retain their hypotheses. These distinctions are part of the statements, not omitted qualifications.
