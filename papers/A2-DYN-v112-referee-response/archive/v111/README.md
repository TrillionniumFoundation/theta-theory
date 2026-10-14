# A2-DYN — revision 111

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi — October 14, 2026

## Referee entry points

`main.tex` is the complete active article (25 pages in local validation). Sections 9–11 contain the new global roof–angle uniqueness theorem, target-roof marked pressure theorem and collision-normalized incidence-witness payments. Sections 1–8 and both preceding appendices are retained, with the two requested local proof clarifications.

`RESPONSE_TO_REFEREE.md` answers the latest v110 report. `PROOF_LEDGER.md` records the exact new proofs, retained historical inputs, limit order and remaining estimate. `PUBLICATION_STATUS.json` distinguishes proved components from the still-required full localized-shortage limit.

The complete v110 packet, including its earlier historical archive, is preserved byte-for-byte under `archive/v110`. The frozen report is `provenance/REFEREE_REPORT_v110.md`. Three exact historical optical/pressure proof anchors are copied into `provenance`. The original repository paths are unchanged.

## Mathematical endpoint

The original exact-label raw pointwise local limit theorem is unchanged. This revision proves a complete target-roof weighted physical sum, not just a per-itinerary bound. It pays collision-deep and sufficiently numerous incidence witnesses in the m^2-normalized essential-height topology at each fixed B. Equation `eq:v111-remaining` retains shallow incidence and arbitrary-depth clearance witnesses; its full decay is not claimed.

## Build

From this directory:

```sh
bash build.sh
```

Requirements: Python 3, pdfLaTeX with the standard AMS/Latin Modern/microtype/geometry/hyperref/mathrsfs packages, and Poppler. No Python third-party package is required for the diagnostics. The build checks active source hashes and both diagnostic suites in normal and optimized Python, stabilizes references, rejects unresolved citations and overfull boxes, and renders all active PDF pages.

From a committed Git checkout, strict provenance checks are:

```sh
python3 tools/check_source.py
python3 -O tools/check_source.py
```

These verify the exact original/archive trees, frozen referee blob, historical proof anchors and scope of all additions. There is no bypass mode. The dedicated workflow runs them against its exact commit SHA and builds the current article. Historical preservation is checked by Git object identity; the workflow does not claim to rebuild all earlier supplements.

## Frozen provenance

Controlling v110 review: `fb1240d2f8c0562a148d559df5a8d9c3bd2d5e39`.  
Reviewed author commit: `0abce3fcfbc735ff5cc6d085279abea5f32a7a22`.  
Exact archived tree: `89ec727b370bf21d66d7086041f75d7868671d4b`.  
Initial v111 remote checkpoint: `d9902135448bcf1ea02cde20bd6ea21fbb16c6a0`.

`VALIDATION.md` separates actual local checks, the later observed v110 CI completion, and any newly observed v111 qualification. Successful source/software checks are not formal mathematical proof certificates.
