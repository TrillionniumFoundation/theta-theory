# General Theta Foundations I — Revision 55

**Stochastic Purification and Sharp Noise Thresholds for Compact Group Experiments**  
Qian Qi · 27 September 2026

This revision responds to the complete v54/r36 report. Its mathematical center is a width-preserving and error-preserving stationary purification theorem for arbitrary compact groups. It yields an exact characterization of the unrestricted stationary minimum and a finite-observable-quotient existence criterion, without executable returns or finite component assumptions. The clocked results separately treat return phases, infinite-component strict thresholds and the exact boundary. An explicit 2-adic experiment has linear exact width and bounded width at every positive error.

## Referee entry points

[Main manuscript](paper.pdf) · [Readable LaTeX source](main.tex) · [Response to r36](RESPONSE_TO_REFEREE.md) · [Frozen controlling report](FROZEN_R36_REPORT.md) · [Proof/scope record](PROOF_STATUS.json) · [Actual build receipt](evidence/BUILD_RECEIPT.json) · [Portable referee package](evidence/REFEREE_PACKAGE.zip) · [Native sources](evidence/CORE_SOURCES.zip)

The build receipt, not this README, determines the validation state and exact qualified source commit. The submitted text is an independent article, not an assertion of closure of the repository's analytic A/B/C/D program.

## Retained mathematical material

The entire 91-file native v54 source bundle is retained byte-for-byte in `retained-v54/`, including all 72 native v53 files and their nested 59-file v52 supplement. The v54 radius article, scalar predecessor, companion notes, and cumulative supplement are separately rebuilt as `RADIUS_PREDECESSOR.pdf`, `SCALAR_PREDECESSOR.pdf`, `COMPANION_NOTES.pdf`, and `COMPLETE_SUPPLEMENT.pdf`. No prior mathematical theorem or proof was discarded to obtain the new main article.

## Reproduction

Use Python 3.11 with `sympy==1.14.0`, `PyMuPDF==1.26.7`, and a TeX Live installation containing AMS, Latin Modern, microtype, geometry and hyperref. From this directory run:

```sh
python build.py --check-isolated
```

The command verifies the pinned report and all retained hashes, reexecutes new and inherited exact checks in normal and optimized Python, compiles all five documents, and independently rebuilds the native archive. Every page's extracted text and raster is compared. It makes no network request and performs no remote write. The report must be present; `--local-missing-report` is only a local preparation mode and cannot qualify a publication.

Work branch: `revision/general-theta-foundations-i-v55-stochastic-purification-2026-09-27`.  
Referee branch: `revision/general-theta-foundations-i-v55-referee-ready-2026-09-27`.
