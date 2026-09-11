# Canonical A2 v21 source pointer

The historical directory name `papers/A2-v17-boundary-information-coarsening/` is retained because many reviewed derivation modules, build scripts and cross-references already use it. The directory name is provenance, not the active manuscript version.

For the revision branch

`revision/a2-v21-nondominated-registered-transfer-2026-09-11`

the **canonical article entry point is**

`papers/A2-v17-boundary-information-coarsening/main.tex`.

The active v21 replacement modules selected by that entry point are:

- `article/01_introduction_v21.tex`
- `article/23a_signed_endpoint_rigidity_v21.tex`
- `article/18a_vector_boundary_information_v21.tex`
- `article/18b_raw_physical_multirate_v21.tex`

All other inputs of `main.tex` are retained reviewed modules or auxiliary material. Files with `_v18`, `_v19` or `_v20` in their names that are not selected by `main.tex` remain historical derivation sources and are not competing canonical manuscripts.

The exact native-build workflow for this branch is

`.github/workflows/a2-v21-native-build.yml`.

`RESPONSE_TO_REFEREE_V21.md`, `PROOF_LEDGER_V21.md`, `HISTORICAL_DERIVATION_AUDIT_V21.md`, and `ACTIVE_SOURCE_MANIFEST_V21.md` are navigation/submission-history documents; none replaces the TeX proofs in the canonical article.
