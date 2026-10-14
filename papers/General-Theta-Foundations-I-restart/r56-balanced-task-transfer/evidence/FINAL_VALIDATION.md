# Final validation of the R56 delivery

The immutable mathematical source is `808ef512a73d5b1911257af2669a4e7ed97107ed`. The fully stored binary artifact head is `5db80e9d1ffeb7345456ef3dedbb167d7bcdf926`. The next evidence-only commit adds four files here and does not revise either mathematics or PDF bytes.

## Actual provenance and publication correction

The source follows the pinned canonical restart and retained R55 input. Removing only the 46 declared new source/publication files from the full source listing reconstructs the original retained root `320cd3865d007d74eba8dfa8656b96f619a28793`. All inherited paths, including all four control files, are preserved.

The initial artifact commit `14163ae4c88360d2772575b1a62f6922aff696fa` stored build/source receipts and the complete source ZIP. Inherited ignore rules kept the 28 PDFs and log in Actions rather than Git. This was discovered during independent tree reconstruction, not silently treated as success. Infrastructure commit `dd2719470fd48bbfe9e09f34fb633abf04ef714b` and binary commit `5db80e9d1ffeb7345456ef3dedbb167d7bcdf926` subsequently stored the exact original, individually hash-verified PDF and log bytes. All intermediate roots were reconstructed independently. The binary commit is therefore not a direct child of the source commit. No source re-write or PDF re-generation occurred during this correction.

The complete build run is [38496786241](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/38496786241). Explicit binary preservation is [38497851798](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/38497851798). Both completed successfully.

## Rebuild and comparison

A fresh root was populated from the actual downloaded hosted source packet. Its 1,301 inputs comprise 1,193 direct Git-blob matches and 108 files verified by transitive pinned historical transport or exact review-copy identity. All 1,301 were unchanged after the complete independent build.

Hosted and independent environments each completed 66 isolated PDF builds, three passes each, including the complete retained chain. The native ordinary and optimized regressions agree: 2,631 exact finite checks and 188 floating checks. Inherited nested counters are not added together as independent tests. Source audit records 38 ordinary files plus manifest, 61 labels, 73 references, 12 bibliography items, 24 citation uses, 20 formal statements, and 14 active TeX inputs.

The 19-page native manuscript and 27 optional retained companions total 688 pages. Every page was rendered and compared using PyMuPDF 1.26.7, RGB, no alpha, at 97.2 dpi. All normalized text, page counts and rendered pixels agree across TeX Live 2023 and 2025. PDF byte hashes differ across those environments; repeated builds within each environment are byte-identical. All 19 native pages were visually inspected. The other 669 pages were automatically compared, not claimed as a new manual reading of all historical mathematics. There are no undefined references or overfull boxes in the build receipts.

## Mathematical audit boundary

The raw balance/reference/effort hypotheses remain explicit. The two intervention realizations score post-command targets; the Gaussian application is separately nonintervening. Exact Borel attainment is separated from finite-description approximation. Gate-rate degeneration, arbitrary unknown-kernel learning, general stateful-simulator invariance, efficient synthesis, and matched total computational-resource lower bounds remain outside the proved claims. Preservation and CI are not mathematical breakthroughs or an independent top-four acceptance certificate.
