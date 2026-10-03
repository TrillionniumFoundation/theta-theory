# A2 v27 — fixed-aperture first-impact rigidity

Qian Qi · 3 October 2026

**Reference-free certification from intrinsic boundary laws** remains the title. The controlling v26 report is `24b9c5f6a586a35975e6f6b67d25ec431390f57a`, reviewed author head `8c6f1113296c5401258ff052e5ce734fabfb3909`. Read `main.tex`, especially Theorem 1.2 and its complete Section 1 proof, then `RESPONSE_TO_REFEREES.md`.

## New mathematical conclusion

One first-impact **position law** in one fixed laboratory square determines the entire periodic obstacle union and its full translation lattice. A finite experiment uses at most `C nu^(-3/4) log(C/(nu delta))` attempted launches, localized to `epsilon_x <= c nu^(3/2)`, for a `C nu` error in the matched finite-presentation C2 metric. The existing numerical lattice bound guarantees that every type and two generating translates of a root body are in the covered aperture. Period saturation is proved before area is calculated.

The new route uses no endpoint histogram, return-channel selection, expanding aperture, adaptive relocation of auxiliary clouds, unknown free-area normalization or rotation/reflection margin. Disks are allowed. It still requires resettable uniform spatial launches, independent directions, calibrated first-impact localization and common laboratory coordinates, finite C^{6,beta} bounds, separation/curvature/lattice bounds and a gap between translation types. It is not a passive, spectral or count-only result. Launch count is not end-to-end or bit complexity.

## Preservation

The original seven v26 chapters remain active. Six mathematical core files are byte-identical; only the clearance passage in the seventh is corrected. Exactly two physical endpoint components are excluded from the other-solid test, with endpoint supports and collar distances handled separately.

`retained/v26/` is the exact reviewed tree `eb47d317f691162303de1686f6c9233cb9d8ccb4`. `retained/v25/` remains tree `c48d900f6596eea1e8df1f729481674fb1bf6175`, including all earlier nested manuscripts. `complete/` remains the original supplement tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. No previous paper or review path is changed. The requested mathematical-journal target and periodic-billiard inverse topic remain.

## Validation

Python 3.10+, NumPy/SciPy for retained diagnostics, latexmk, TeX Live with the declared packages and Poppler pdfinfo are required.

```sh
python3 tools/validate_v27.py
python3 tools/validate_v27.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
```

The native driver requires complete source pins and every declared script. Missing tools are errors, never a source-archive-only success fallback. It executes the new diagnostics, source-gate negative controls, the current and reviewed v26 primary builds, and the unchanged full v25/v24 qualification chain. That chain retains raw historical layout warnings and discloses reversible stage-only wrappers without changing the archived mathematical sources.

Initial local primary-only execution passed 3,295 finite diagnostics plus 14 validation-contract checks in ordinary and optimized Python, with identical output, and produced a 24-page primary without final TeX diagnostics. This was source-content execution, not an authenticated remote checkout. Consult `DELIVERY_STATUS.md` and actual receipts for subsequent scope. A workflow definition, a queued run or a source archive is not a full-package pass. No build or finite test certifies the proofs, executes a physical sensor, establishes priority or decides journal significance.
