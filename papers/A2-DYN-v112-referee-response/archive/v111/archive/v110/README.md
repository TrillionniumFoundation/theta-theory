# A2-DYN — revision 110

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi — October 14, 2026

## Referee entry points

`main.tex` is the revised article, with all active v109 model, input and proof modules retained. It compiles to `build/main.pdf` (18 pages in the local validation). New Sections 7–8 prove the positive variation payment and the persistent-guarded reduction; Appendix B supplies the detailed optical/cofactor/endpoint arguments. `RESPONSE_TO_REFEREE.md` answers the controlling v109 report. `PROOF_LEDGER.md` states precisely what is proved, inherited and still required.

The complete reviewed article and its complete historical tree are preserved under `archive/v109`. This directory is an exact Git-tree copy, not an abbreviated reconstruction. The report itself is frozen in `provenance/REFEREE_REPORT_v109.md`. Original repository paths remain untouched.

## Mathematical scope

The original exact-label raw pointwise local limit theorem remains the target. The newly proved payment bounds an actual positive submeasure of the original microscopic source by O(B^(-95/384)); the new remainder retains persistent guarded nongrazing source and the full original nongrazing comparison capacity. The ordered height decay of that final remainder is not proved here. This is recorded in the article and in `PUBLICATION_STATUS.json`, without replacing the target by an averaged law or a different model.

## Build and checks

From this directory run:

```sh
bash build.sh
```

The build requires Python 3, pdfLaTeX, the standard AMS/Latin Modern/microtype/geometry/hyperref/mathrsfs packages, and Poppler. It runs exact finite checks in normal and optimized Python, verifies the active manuscript manifest, stabilizes references, rejects unresolved references and overfull boxes, and writes PDF page renders. It does not equate a successful build with a proved continuum theorem.

For strict committed-source verification from the repository checkout, run:

```sh
python3 tools/check_source.py
python3 -O tools/check_source.py
```

This additionally verifies the exact historical tree, controlling referee blob, unchanged original paths and permitted scope of additions. It has no bypass mode. The dedicated GitHub workflow runs these strict checks at its own exact commit SHA and builds the revised active article. The unchanged historical supplements remain available with their original build entry points under `archive/v109`; the v110 workflow does not claim to rebuild them all.

## Frozen provenance

Controlling review: `cdf0149246de7dd6b68b0b276d9dc1c4ca5537c2`.  
Reviewed author: `ab0ad79b9c101b82c80e33511529588d101a45c0`.  
Preserved v109 tree: `99e677d4a40f087fc21a2c050e1cc4f43e3ef155`.  
Remote initial v110 source freeze: `5dd17967af39b4a831f2c69424a95219332fc30d`.

`VALIDATION.md` separates local execution, inherited exact-SHA evidence and any newly observed remote execution. A missing or queued run is not a successful qualification.
