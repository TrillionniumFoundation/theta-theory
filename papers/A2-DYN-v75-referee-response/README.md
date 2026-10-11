# A2-DYN revision 75

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas** — Qian Qi.

The active journal manuscript is `main.tex`; the complete technical supplement is `supplement.tex`. Build with `bash build.sh` in an exact checkout, or `bash build.sh --local` for a separately materialized source copy outside CI. Outputs are `build/main.pdf` and `build/supplement.pdf`.

This revision responds to the v74 report at `18c51226fbc3bcc580ae66bee926d944be590c81`. Its parent manuscript is v74 at `5a4704bc945d75e0fa181983a7b66a5dc5a73350`, paper tree `02bac634205e7f776793ba330c98c11039fd71d5`.

## New proof route

Module 168 constructs a single strongly convex supporting action on each of at most 256 endpoint-cap rectangles. It agrees with the actual physical roof on every regular piece of a word, including disconnected pieces. Its physical Hessian is bounded below by `50/47` and above by `1360/9`, independently of the collision count and every positive incidence and clearance.

Module 169 uses that global comparison to bound the coarea integral of all physical level pieces of one word by `2*pi/lambda`, without a level-complexity factor. It gives an exact positive Gauss trace for the original return density and sharpens the inherited complete inverse-incidence height bound.

Module 170 relates the complete trace's paired roof modulus to the short-superlevel-component tail. The physical collision-normalized weighted-word modulus is still to be proved. The original scalar pointwise target, exact labels, arithmetic zero classes and downstream conditional path claims are unchanged; a wordwise geometric estimate is not recorded as full LLT closure.

## Preservation and handoff

All 167 inherited core modules, 12 appendices, 216 inherited Python files and both bibliographies are byte-preserved. The full v74 mathematical article is incorporated into the technical supplement together with the preceding complete pipeline. The journal compiles the three new modules; recorder verification requires all 170 cores across the two documents. Replaced active files are preserved under `provenance/v74-*`; inherited input maps remain historical reference material, not the current status authority.

`SOURCE_MANIFEST.json` is authoritative for claims. `RESPONSE_TO_REFEREE.md` answers every v74 request. `SPECIALIST_AUDIT.md` is the current v75 audit map, superseding the stale v73 file only in this new revision. Exact-SHA build evidence is produced by `.github/workflows/a2-dyn-v75-qualification.yml`. Finite tests and compilation are not proof certification or independent human review.
