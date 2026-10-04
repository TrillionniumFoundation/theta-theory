# A2 v23 — sequential record discovery and unknown-cell preparation

Qian Qi · 29 September 2026

Primary manuscript: **Reference-free certification from intrinsic boundary laws**, `main.tex`. The actual local primary build has **23 pages**. This revision responds to the latest retrieved v22 report at `ecfe49c9ab244ade504c9a727a4d110f72db4433`, which reviewed author head `ef51836da1744fc4a7133e3a3fd0e85848c73dc6`. The topic and requested Annals/Acta/Inventiones/JAMS standard are retained; no editorial acceptance is asserted.

## Referee reading route

Theorem 1.1 states the new sequential acquisition result, proved as Theorem 7.1 and Corollary 7.2. Sections 2–4 retain the full local inverse, exact completion identity and reference-free noisy arithmetic. Section 5 constructs a laboratory-square sampler without supplied period vectors or a cell boundary, and charges its finite-size bias. Section 6 proves a small-witness bound, adaptive arrival estimates, a geometric producer and pointwise margin exhaustion. Section 7 gives all-epoch soundness, almost-sure stopping and a stopping tail under uniform discovery hazards. Section 8 gives the theorem-level literature and information-category comparisons. `RESPONSE_TO_REFEREES.md` addresses all nine required corrections; `PROOF_LEDGER.md` records assumptions and scope.

The witness bound is `r0 + 1 + floor(log2 Q)` and does not assume a primitive recorded cycle pair. With per-witness arrival hazard at least `p`, the late-epoch stopping tail is at most `delta/[8(k+1)^6] + w exp(-pk)`. The explicit validation schedule has finite expected launch cost. The sampler's total-variation error is at most `min(1, 8 V1 b/(A0 L))`; histogram recovery includes its amplification by `h^-4`, rather than treating finite-square data as exact quotient data.

The producer assumptions remain substantive. It must return genuine replayable local branches and periodic gates that recognize all translated occurrences. The concrete realization uses body-list, shortest-pair and clearance access. It is **not** a theorem of record discovery from unmarked trajectories alone. Soundness does not require a discovery hazard; termination does. The analytic, shape, symmetry, area and local physical priors remain explicit. No whole-table minimax or exact analytic count-only conclusion is inferred.

## Complete preservation

`retained/v22` is the entire reviewed v22 paper tree, unchanged: `65c432ddf3233b4931a15e1ee86cbc051503e682`. It includes the v21 and v18 companions, all previous proof inputs, statistical testing, tools, ledgers and historical receipts. Three active primary mathematical files are reused byte-for-byte from v22. `complete` is the original entire Supplement S tree, `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. `SUPPLEMENT_MAP.md` lists the six current entry documents. Earlier repository papers and review paths are unchanged.

## Reproduction and actual evidence

Requirements: Python 3.10+, NumPy, SciPy, LaTeX with amsart/Latin Modern/microtype/needspace, latexmk and Poppler pdfinfo. From this directory:

```sh
python3 tools/validate_v23.py
# In a clean checkout containing the retained volumes:
python3 tools/validate_v23.py --all-volumes --require-checkout
```

The actual local source-content run passed **7,230 new finite diagnostics** and **3,635 selected retained diagnostics**, with identical normal and optimized Python output. The retained selection includes 90 nonlinear stationary-ray curvature comparisons, with maximum absolute error `1.2312545871751013e-08`. The complete 23-page primary compiled without final TeX warnings, undefined references or overfull/underfull boxes, and the rendered layout was inspected. Its mathematical and tool source manifest was unchanged.

This was **primary-only source-content execution, not an authenticated Git checkout**. No retained volume was rebuilt in that run. No physical scanner was executed. `verification/local/receipt.json` records actual commands, exits, times and digests with null checkout/run fields; the six command logs are archived beside it. `SOURCE_PINS.json` and `PUBLICATION_BINDING.json` bind the tested contents to published native Git objects.

The read-only workflow checks out the exact triggering commit, verifies both retained tree identities, runs new and retained diagnostics, and builds the primary plus five retained documents in staged copies. It uploads actual receipts, logs and PDFs, including failures. A workflow definition, queue entry or successful local primary run is not a successful hosted full-package build. Consult the workflow associated with the final revision SHA; no hosted success is asserted in this source record.

Finite diagnostics and compilation do not establish all-order proof correctness, mathematical priority or a journal decision. The companion history remains provenance, not a replacement for validation of this revision.
