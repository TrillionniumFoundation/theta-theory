# A2 v4 — uniform collision thresholds and nonlinear boundary laws

**Uniform collision thresholds and nonlinear boundary laws in periodic dispersing billiards**  
Qian Qi — September 9, 2026.

Revision branch: `revision/a2-v4-nonlinear-boundary-laws-2026-09-09`.  
Controlling review: `26b05bf0c6483a326d078c99393f4a34434bcc18`.  
Reviewed v3 manuscript: `3f8ad0a5b718818a22c0e2e47378d4d6c93473a1`.

## Manuscript and response

`main.tex` is the complete English article: **44 pages** in the recorded native build. `two_collision.tex` is the unchanged complete **7-page** companion. `RESPONSE_TO_REFEREE_V4.md` answers OBS-R1, OBS-R2 and OBS-R3 individually; `PROOF_LEDGER_V4.md` gives the hypotheses and proof dependencies. The exact controlling report is retained in `review-basis-v3/REFEREE_REPORT.md` in the repository.

The principal addition is a nonlinear two-boundary theorem. Sections 5–6 construct half-line stationary segments, prove exponentially accurate factorization of the relative flux, derive a fixed-offset physical law and the first poles of its onset series, and realize a fixed-area geometric family invisible to every leading endpoint matrix but separated by a nonlinear coefficient with derivative `sqrt(3)/2`. Proposition 8.1 states the exact one-flight factorization of the leading hierarchy. Theorem 8.2 gives fixed-order multi-offset extrapolation with expected and high-probability preparation cost; Proposition 8.3 propagates physical-window calibration error. Theorems 10.1–10.2 prove a positive, sharp one-half-Hoelder stability scale relative to the circular table, including the complete absolute-amplitude sequence topology.

The general smooth periodic geometric class is retained. The entire old article tree is the basis of this new directory: its original `v3/`, `v2/`, circular sections, companion and historical derivations remain. Old entrypoints are also archived under `history/v3-publication/`. All 123 old active labels remain; the result count changes from 29 to 41. No original paper or review is removed from the repository.

## Reproduce

From this directory, with Python 3.10 or later, TeX Live with the standard AMS packages, NumPy, SciPy and SymPy:

```sh
python build.py
python v4/verify_boundary_laws.py > /tmp/a2-v4.json
python -O v4/verify_boundary_laws.py > /tmp/a2-v4-O.json
cmp /tmp/a2-v4.json /tmp/a2-v4-O.json
python v3/verify_observability.py
python v2/verify_geometry.py
python tools/verify_thresholds.py
```

The builder compiles both real entrypoints without shell escape, checks auxiliary convergence, rejects unresolved references and overfull boxes, and verifies the actual recorder input closure. `verification-v4/NATIVE_BUILD.json` records the exact compiled source hashes and PDF hashes. PDFs are generated locally by this command and are supplied in the downloadable native package; the repository publication is native source, not an asserted remote PDF build.

`verification-v4/VALIDATION_SUMMARY.json` records 252 new checks and 257/328/411 retained checks, each executed normally and with `-O` with byte-identical outputs. It includes output hashes, environment and physical-quadrature measurements. The full execution JSON and compiler logs are in the downloadable package; the repository includes the runnable scripts and compact receipts. `PRESERVATION.json` and `VISUAL_INSPECTION.json` record source retention and the visual checks.

The package contains the complete native build closure, PDFs and local evidence, not an export of every historical repository file. The repository tree retains the full historical subtrees. The temporary source-export workflow failed and is removed from the delivered tree; no remote CI success is claimed. Finite diagnostics are not continuum or interval proofs. The analytical arguments remain subject to independent referee review; no journal acceptance or unrestricted long-time billiard limit theorem is asserted.
