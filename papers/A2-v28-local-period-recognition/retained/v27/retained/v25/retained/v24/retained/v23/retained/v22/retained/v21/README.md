# A2 v21 — finite apertures and persistent sufficient data

**Qian Qi · 29 September 2026**

Primary manuscript: *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*, `main.tex`, **29 pages** in the actual local build. The controlling referee report is the v20 report at `40e9f1beaf49bf7f870f2f6f73ac027feab1a84e`, reviewing `c376e802e6e86735888dcd685f987c7a8f475903`.

## Main results

Read Theorems 1.1–1.2, then Section 7. Theorem 7.4 replaces a supplied quotient by the unknown period lattice with an exhaustive, unquotiented finite-aperture scan. Under explicit number, diameter and covering bounds, its radius is

`B = rho0 + D0 + (r0-1)(R+2D0) + xi`, where `R>2rho0` and `xi>0`.

Every necessary bridge orbit has a midpoint in that disk. Lemma 7.2 proves that recovered whole-pair geometric keys identify precisely the same undirected translation orbit, so the inverse removes translated duplicates and reverse returns without given integer labels. Padding reduces scanner selection to finitely many geometric pair/clearance tests. Exhaustiveness and geometric selection access remain explicit assumptions; the scanner is not constructed from unmarked trajectories.

Proposition 7.5 extracts a period-generating witness with at most `r+1+floor(log2 n)` records. Theorem 7.6 makes this finite witness persistent without freezing all redundant channels. Proposition 7.7 constructs a genuine cutoff-crossing physical family. Theorem 7.9 gives conditional finite-histogram recovery from qualified unlabelled lists retaining the witness, while the remainder can vary. The local analytic/generic prior, witness retention, qualification and onset brackets are explicit; neither arbitrary erasures nor stable recovery of the discontinuous full catalogue topology is claimed.

Section 7.5 supplies the nearest relative-neighborhood, visibility-complex and free-bitangent comparisons, including a directly proved gap-relative subgraph proposition. The old lens/travel-time, moment/count and statistical comparisons remain in Section 8. Two windows mean density functions or growing histograms, not two scalar observations. The topic and mathematical-journal target are retained; no minimax or exact analytic count-only theorem is inferred.

## Preservation

All **six v20 mathematical core files** remain active and byte-identical. The entire reviewed v20 tree `3b34e4156b3ff621df9c1a3fb8aece4c66f1f07b` is preserved at `history/v20-reviewed`, including nested history and execution evidence.

Supplement R remains the whole v18 paper at `retained/v18`, tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`. Supplement S and its auxiliary document remain in `complete`, tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. Nothing is removed from prior manuscript, review or unrelated-paper paths. `SUPPLEMENT_MAP.md` specifies all reading and build routes.

## Reproduction and actual local evidence

Requirements: Python 3.10+, NumPy/SciPy, latexmk, LaTeX with amsart/Latin Modern/microtype and Poppler pdfinfo.

```sh
python3 tools/validate_v21.py
# Exact checkout, including archived and supplementary sources:
python3 tools/validate_v21.py --all-volumes --require-checkout
```

The actual local primary-only run passed **70,662 finite diagnostics**: 43,928 retained-base checks on the current input graph and 26,734 new finite checks. Normal and optimized Python outputs were identical. The retained numerical suite made 90 nonlinear stationary-ray curvature comparisons with maximum absolute error `1.2312545871751013e-08`. Counts include finite algebra, graph/orbit models and source bookkeeping; they are not counts of independently certified theorems.

The 29-page primary compiled with no final TeX warnings, undefined references or overfull/underfull boxes. All 29 rendered pages were inspected. Source hashes were unchanged by validation. `verification/local/receipt.json` and its logs record actual commands, exits and digests. That run was **source-content execution, not an authenticated Git checkout**, and did not rebuild the retained volumes. It retains null commit/run fields instead of borrowing v20's hosted result.

A separate read-only workflow checks out the exact triggering commit, verifies source pins and all retained tree identities, reruns current and archived diagnostics, and builds the current primary, Supplement R, both Supplement S documents and the archived v20 primary. It uploads actual logs and PDFs, including failures. Its definition or queued status is not a completed hosted pass. Consult the run for this exact revision; no hosted success is asserted by this source README.

`RESPONSE_TO_REFEREES.md` answers all six v20 correction headings. `PROOF_LEDGER.md` separates hypotheses, proofs and diagnostic scope. `LITERATURE_AUDIT.md` records primary-source access and its limits. Finite checks and compilation do not establish formal proof certification, priority, or a journal decision.
