# A2-DYN revision 37

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This is a new author manuscript responding to the latest v36 submission-state and supplementary referee report, not an alias for a review commit. The actual mathematical baseline is revision 35 at `fda52bb72045204b50159e8263c05afaa6a9dc58`; the controlling report is at `ef921b94134118b9b41a4ca8237c3f87a34a02bd`.

## Principal addition

Theorem 3 gives a local limit on the original four-coordinate actual-return record: displacement and collision count are exact, roof time lies in a fixed unscaled interval, and the genuine return index lies in a diffusive window. Modules 77--78 prove an exact bounded multiplier for the actual section, a mixed local--central occupation theorem, and an exact return/occupation disintegration. The Schur complement and the induced covariance normalization are explicit.

The strong-space faithfulness proof now concludes by the two defining strong seminorms, without assuming injectivity. Module 76 supplies the exact finite-cover mixing input. Module 79 verifies the compact action principle for a nonelliptic third/fourth-harmonic support family. The original title, model, raw-return target and all historical theorem-level content are retained.

## Source and verification

All 75 inherited core modules and the A--X appendix remain compiled. Seventy-three cores, all 83 inherited Python files, and the bibliography are byte-identical. Six exact replacements in cores 72 and 74 are recorded in `INHERITED_EDITS.json`; their old versions and the old main source are archived. The complete article has 79 core modules and three principal introductory theorems.

Run `bash papers/A2-DYN-v37-referee-response/build.sh` from the repository checkout. The exact-source workflow also renders pages located from actual theorem labels and emits SHA-bound execution receipts. Finite diagnostics and typesetting are not continuum proof certification. `RESPONSE_TO_REFEREE.md` gives the itemized response; `PROOF_LEDGER.md` records dependencies; `SPECIALIST_AUDIT_MAP.md` identifies independent audit targets.

The single-index return-frequency inversion, common pointwise raw correction and full return complement are not claimed proved by the new window theorem. No independent human review is claimed.
