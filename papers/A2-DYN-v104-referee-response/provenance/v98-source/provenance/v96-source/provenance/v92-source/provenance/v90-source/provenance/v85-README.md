# A2-DYN revision 85

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Start with `main.tex`, `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md` and `SOURCE_MANIFEST.json`. `supplement.tex` assembles the complete inherited mathematics, the entire v84 article, and a compact input/equation/proof-page guide. This is an author revision for further external scrutiny, not a commissioned journal decision or proof certificate.

Controlling report: v84 at `ef77954a0faa2677028edf971327edca35051ead`, blob `29a2d3e77b637e34b107d8b9638fea51bc104e64`. Author baseline: v84 at `f94ff549308db3fbba2087be0852c3f1e4d0739a`, paper tree `ddae47df392cc5ca659cdef8250f96a0ff33fcab`.

Modules 196–198 formalize the measurable segment-to-source map, audit the positive-cutoff constant, estimate every complete positive residence band, and obtain full cutoff-uniform surface and critical height bounds. The full zero-residence tail is identified with the limiting surface height and compared to an actual collision-source restriction. The original pointwise target is unchanged; both microscopic charge-zero requirements remain unproved.

Run `bash build.sh` in an exact Git checkout. `bash build.sh --local` permits only a non-CI archive check and does not qualify a remote checkout. Both modes require the complete supplement. Qualification workflow: `.github/workflows/a2-dyn-v85-qualification.yml`. Use actual completed runs at the final author SHA, not a previous successful baseline run. Current status authority is the active manifest; inherited checkpoints are historical.
