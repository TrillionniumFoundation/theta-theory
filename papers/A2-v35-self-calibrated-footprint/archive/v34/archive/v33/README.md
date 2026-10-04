# A2 v33 — finite controls, sequential observations and physical resolution

Qian Qi · 4 October 2026

**Primary:** *Scalar collision laws and recognition of periodic dispersing billiards*, `main.tex`. The actual local primary build has 21 pages. The controlling review is the v32 report at `058d2b7b773038cfa7e43f7f52a3b79fdc4107f6`, report blob `e38199da9ea49227f48b94eef8d04b3ee8da871c`. The reviewed author head is `eeb171d4e00242c9813c10e2124556b2cee480d3`. The new mathematical checkpoint is `a3c4b12d2d56d67a7569e3b239f0bcea8f546ee3`.

## Mathematical reading route

Theorem 1.3 summarizes the additions. Theorem 4.1 gives finite dyadic commands, their binary description length, and a separate conservative numerical-work bound under effective-prior assumptions. Lemma 7.1 makes the laboratory gauge and Steiner centering explicit. Lemma 7.2 proves the stopped-transcript information inequality; Theorem 7.3 gives the expected-attempt lower bound without assuming a deterministic cap.

Lemma 8.1 is a physical common-response coupling for nearby separated convex swept bodies. It changes actual start positions within the allowed error, rather than changing a sensor label artificially. Theorem 8.2 consequently gives a necessary position-calibration power matching the sufficient power of the retained reconstruction. With `s=6+beta`, the two necessary resources are expected attempts of order at least `nu^(-1/(s-2))` and position tolerance no coarser than a constant times `nu^(s/(s-2))`. The sufficient attempt bound has logarithmic overhead. No sharp confidence/logarithm or actuator-production cost is claimed.

The calibration converse is specifically for worst-case bounded position errors that may depend on the table, command and nominal start, as permitted by the original coupling model, and for command lengths bounded strictly below component separation. It is not a statement about a single fixed common offset, a known mean-zero noise law, arbitrarily long trajectories, or a sensor that observes actual start positions. Its necessity concerns position error; time and angle can be exact.

The active localized compass sensor, translated reciprocal nominal reverse law, fresh preparations, all-attempt normalization, bounded periodic prior and known positive nonperiod-patch margin remain explicit. No free-start flag, impact location, passive spectral invariant or inference of crystallinity is introduced.

## Preservation

All six v32 proof chapters are active in the new primary and byte-identical, with original core tree `b0655672858cd000e2c6d939f681ec47b35eb716`. The whole reviewed v32 paper is included unchanged as Supplement R32 at `retained/v32`, native tree `2a7d949f43dcb7b84d4a85ef8a4436349f615493`. This includes its tools, receipts and complete nested submission history. No old manuscript, referee report or unrelated paper is edited. The new package adds one primary to the fifteen declared v32 documents.

## Reproduction

Dependencies: Python 3.10+, NumPy, SciPy, Shapely, latexmk, a LaTeX installation with amsart/Latin Modern/microtype, and Poppler pdfinfo.

```sh
python3 tools/validate_v33.py
# Full qualification in an actual checkout of this revision:
python3 tools/validate_v33.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
```

The local source-content run passed 117,772 new finite diagnostics, 36 new validation-contract checks, 11,647 retained v32 diagnostics and 42 retained contract checks. Each ordinary/optimized pair was identical. The new geometric diagnostic tested 4,500 starts; 224 had differing nominal bits, including 104 solid-entry and 120 swept-exit cases, and all admitted the tested common physical response within the displacement budget. These are finite polygon/numerical controls, not an execution of the physical sensor or a proof of the continuum lemma.

The 21-page primary has no final TeX warnings, undefined references or overfull/underfull boxes. All pages were rendered and inspected. `verification/local/receipt.json` records the actual commands, exits, digests and null checkout/run fields. The primary-source validation ZIP supplied with this revision contains the exact local logs and receipt. The local run rebuilt only the primary; it did not qualify all retained PDFs at a new checkout SHA.

The read-only v33 workflow checks out its exact triggering SHA and delegates the unchanged v32 full validator at that same SHA. Its sixteen-document result, actual logs, source archive and PDFs are uploaded even on failure. A workflow definition or queued run is not a successful hosted qualification. Consult its actual receipt; no hosted success is inferred from the previous v32 success. Finite checks and compilation do not establish independent proof certification, literature priority, apparatus feasibility or journal acceptance.
