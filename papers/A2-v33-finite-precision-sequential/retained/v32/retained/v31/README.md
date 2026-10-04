# A2 v31 — reciprocal commands and mean-exit reconstruction

Qian Qi · 4 October 2026

Primary: **Scalar collision laws and recognition of periodic dispersing billiards**, `main.tex`, 26 pages in the actual local build. The controlling report is v29 at `6444b57768313ac68978b3ee04a428b4832ccb6e`. This revision builds on the completed v30 source `c01118b11779b6161cc34e311f840e5ab36a019c`; no newer referee report is assumed. The topic and Annals/Acta/Inventiones/JAMS target are retained.

## Mathematical revision

**Theorem 9.2** replaces almost-sure bounded stopping by a mean-exit estimate. For centered bounded displacements with second moment at least v_*, H=(D+b)^2/v_* bounds the mean exit. A geometric Bellman inverse reconstructs occupation from its measured Markov difference without a supplied zero set. Comparing two physical occupations, even with different zero sets, gives ||u-u'|| <= H ||g-g'||. No common positive drift or nonsingular covariance is required.

**Corollary 9.3** admits every nontrivial bounded calibrated displacement law with steps shorter than component separation. Its positive-probability escape-cone constant is explicit and may be large. **Proposition 9.4** proves locality on one fixed enlarged aperture, using killed rather than periodically wrapped updates.

**Theorem 10.1** implements four pooled directions by exact grid shifts. Each center supplies only two pooled bit means, not direction-resolved probabilities. The finite algorithm has conditional C2 error O(nu), O(nu^-3) spatial centers, O(nu^-3 log(C/(nu delta))) attempts and O(nu^-6) arithmetic/fixed-kernel evaluations on the known-margin periodic class. Rational intervals enclose the local iterate and, with the proved tail, the protected occupation. Constants include the exit-time and patch-margin priors and are not optimized.

Solid starts and free misses both give zero in the all-attempt denominator. Reciprocal input coupling, localized commands, calibration, smoothness and the known positive nonperiod margin remain substantive inputs. These are not uniformly prepared count-germ or passive spectral results. The computational random walk is not a physical multi-collision trajectory.

## Preservation and reading route

The opening reciprocal theorem summarizes the additions. Sections 9–10 give their complete proofs. All nine v30 core files remain active and byte-identical in Sections 1–8 and the retained introduction. The entire v30 native paper tree `1a6f8f32ec62aec586883e67753b3a72895f875c` is supplied at `retained/v30`, including its nested sources and original receipts. The earlier retained/v29 path also remains present. No original paper, review or workflow is overwritten.

The declared full package is **14 documents**: this primary plus the exact thirteen-document v30 package. Duplicate archival paths are not counted twice. See `SUBMISSION_MAP.md` and `RESPONSE_TO_REFEREES.md`.

## Verification and reproduction

The actual local primary qualification passed **8,513 finite math/source checks and 49 validation-contract checks**, with identical ordinary and optimized Python output. The 26-page primary compiled without final TeX warnings, undefined references or overfull/underfull boxes. All pages were rendered for inspection; the mathematical/tool manifest remained unchanged. The local receipt states source-content execution, not an authenticated checkout or a full-package/hosted pass.

The v30 run `37137333074` was independently read as successful at the v30 SHA. That is historical evidence, not borrowed v31 qualification. The new read-only exact-SHA workflow verifies retained native trees, runs current and inherited suites, builds all fourteen documents, and archives source/PDF/log/receipt evidence including failures. Its own run supplies the actual hosted outcome.

Requirements: Python 3.10+, NumPy/SciPy for inherited suites, latexmk, TeX Live LaTeX extras/recommended fonts, and Poppler pdfinfo.

```sh
python3 tools/validate_v31.py
python3 tools/validate_v31.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
python3 tools/reciprocal_intervals.py examples/compass-two-by-two.json
```

The rational CLI takes explicit forcing intervals and a certified survival upper bound. It never infers those physical/confidence inputs from bits. The old root v30 tools are preserved historical files; the current validator delegates the actual v30 package under retained/v30. Finite diagnostics and compilation do not certify continuum proofs, physical calibration, priority or editorial acceptance.
