# Evidence navigation

- `../BUILD_RECEIPT.json`: the actual successful strict run at the exact source commit.
- `../VISUAL_QA_RECEIPT.json` and `visual/`: actual rendered-page inspection scopes and limitations.
- `HOSTED_CI_OBSERVATION.json`: observed matching-run count; no unobserved CI success.
- `PRE_FETCH_BUILD_FAILURE.json`: retained unsuccessful identity-check attempt.
- `remote-refresh/`: final branch snapshots and content-based delta classification.
- `EXECUTION_NOTES.md`: relationship between these observations.

The downloadable validation ZIP includes these records and the original native logs, diagnostic stdout/stderr, PDF text extractions, auxiliary files and raster inspection evidence. Original report-local paths describe where the inspection occurred. In the ZIP, all visual records and their images are together under `visual/`; build files are under `build/`. Scientific sources and the full historical text corpus are separate, hashed archives.
