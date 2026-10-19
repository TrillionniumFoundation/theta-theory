# Baseline, source identity and historical applicability audit

## Source decision for this author revision

This revision continues the complete native A2-DYN author manuscript at commit
`15ad3962de63f50911b765fe6608e722fe9b8c82`, in
`papers/A2-DYN-global-minimizer-localization-author-revision`. Its canonical
repository tree is `a1eccaf41b953cbcba430cf0ecf78195771db4a8` and its article tree is
`39f02eb2dab466bb742c7f96139a6535d7bb10ef`. The selection uses actual source
availability, immutable tree identities, a complete native input closure and a
fresh successful build. It does not infer mathematical completion from the
branch name, publication receipt, compiler or CI.

The complete current search found no newer A2-DYN author source or newly issued
A2-DYN referee report. The preceding author manuscript supplies all 50 native
core proof bodies 260–309, including the six localization and exact-source
modules added in the previous iteration. Those six bodies are inherited results
in this revision. The original architecture through core 259, all distinct
historical variants and all actual historical reports remain available.

This is an author revision. The controlling report remains the report committed
at `f01482035a0b945b50f1f9c30f30ef35077558dc`, which explicitly examined
`31792379408c5ace2c09284c2eb22d2331023433`. That report's direct mathematical scope
ends with core 276. It is not represented as a report on core 277–309, this
revision, or the new source-height arguments.

## 1. Complete current ref and immutable-source census

The fresh branch readback was completed at 2026-10-19T00:54:01.476Z. Fourteen
successive GitHub REST pages were obtained with `per_page=100`; page 13 has 87
records and page 14 is empty. All earlier pages have 100 records. The retained
readback therefore has 1,287 distinct repository refs and a closed pagination
boundary.

| Class | Current count | Scope |
|---|---:|---|
| All repository refs | 1,287 | Full branch enumeration, including other papers |
| A2-DYN-related refs | 423 | Exact current ref-to-commit mapping |
| Author/research/referee-copy/referee-response refs | 245 | Includes the single original research ref and the new paired publication refs |
| Distinct current A2-DYN author heads | 128 | Actual Git commit metadata and canonical root tree identity |
| A2-DYN review refs | 178 | Unchanged from the preceding complete report census |
| Distinct author root tree readbacks | 128 | Nonrecursive responses, with canonical Git hash recomputation |
| Distinct papers trees | 114 | Every A2-DYN article entry at the author heads |
| Distinct A2-DYN article trees | 116 | Full direct entries, including incomplete wrappers |
| Distinct native core trees | 112 | Actual numbered TeX proof entries |
| Distinct numbered native proof blobs | 361 | Modules 1–309, including genuine historical alternatives |

The 361 native contents are exactly the previously retained 355 distinct
variants through core 303 plus the six real modules 304–309. Repeated placements
and branch aliases are not counted as new mathematical results. The new source
census does not rely on a recursive repository response that might have been
truncated: all traversed trees are nonrecursive and all returned entries are
retained. Canonical Git tree hashes were recomputed from the actual entry
bytes for 515 source-tree responses; every check passed.

Relative to the preceding 1,283-ref census, no old ref moved or disappeared. The
only new A2-DYN refs are:

- `revision/a2-dyn-global-minimizer-localization-2026-10-18`;
- `referee-copy/a2-dyn-global-minimizer-localization-2026-10-18`;
- `referee-response/a2-dyn-global-minimizer-localization-2026-10-18`.

All three resolve to `15ad3962de63f50911b765fe6608e722fe9b8c82`. The fourth added
repository ref concerns General Theta R73. Its actual commit and papers tree
were inspected; that tree contains no A2-DYN article. It supplies no alternative
A2-DYN source. No `AGENTS.md` was present at the selected root, papers directory
or article directory; the complete author root/article scan also found none.

The reproducible receipts are under
[audit/current-iteration/source-census/](audit/current-iteration/source-census/):
`ALL_BRANCHES_READBACK.json`, `BRANCH_DELTA_FROM_PREVIOUS_CENSUS.json`, all five
`ALL_AUTHOR_*_READBACKS.json` files, `NUMBERED_NATIVE_VARIANT_WITNESSES.json` and
`SOURCE_CENSUS_VERIFICATION.json`. The included `verify_source_census.py` checks
the retained API entries, canonical Git hashes, ref coverage and local source
identities with explicit exceptions, including under optimized Python. The
source-identity procedure is distinct from mathematical validation.

## 2. Scientific source and subsequent publication identities

The selected head contains publication receipts added after the complete
scientific source. These identities are kept separate.

| Object | Commit | Canonical root tree | Role |
|---|---|---|---|
| Complete preceding scientific source | `e8ceec7e90b97c21c5719e3e13f730599eb12545` | `2b1b6aa59fabc919bff1d8cab3bb2f851ddef761` | Full native mathematics, historical sources and actual execution evidence |
| Source publication receipt and actual CI head | `878d3da9309ed7f71bce80c55cc52d96836ea920` | `5b26d7d7c8b4a4113c23c5acda93079e706bc71d` | Receipt successor; unchanged frozen mathematics |
| Selected complete author head | `15ad3962de63f50911b765fe6608e722fe9b8c82` | `a1eccaf41b953cbcba430cf0ecf78195771db4a8` | CI/dependency snapshot and publication metadata; `[skip ci]` carrier |
| Earlier summable-source author | `fb99e4d67ef74912f6c69b05c9abff3207572e7a` | `b27ab3cc197a4ed491fcf85ed7db3658ebbb85ef` | Complete active proof chain through 303, retained with its archive-manifest discrepancy |

The selected article has 1,645 actual files in 41 nonrecursive trees. Every
file was checked against its current remote Git blob, byte count and mode.
All 1,645 identities match the local baseline; there are zero mismatches.
The frozen source-input manifest has 1,316 entries, 64,061,657 bytes and SHA-256
`b5d4a6afba5da0f2de65ab439a90c53ea46dc3906736c36051ce9e2d64c16dac`.
Its frozen mathematical source/tool identity is
`6a75ad99bb5034581bb5d18e0cd2a6d008d87d17a97c40e76665ab14bd1c54f7`.

The selected baseline's literal native closure contains 59 TeX inputs,
including its complete 50-core chain. A fresh three-pass `pdflatex`
execution from the unchanged baseline, with outputs placed outside the old
article, produced 147 pages. All three compiler commands and `pdfinfo` returned
zero. The accepted log has no unresolved references/citations, multiply defined
labels, overfull boxes or missing glyphs. The two inherited AMS foreign-command
advisories remain disclosed. Source `main.tex` has SHA-256
`84f3c43cd538c6f377b20bdb49a0cf2aa8a002e8eca7aa0196d3e59a967d57b1`;
the new rebuild PDF has SHA-256
`5bb1ef6099d48c172601092cfcfbd6e840ce76250c3f4221bb76b0ea5abd6ad3`.
This is a new execution with its own output identity, not a recreation of an
old log or PDF under its old hash. The commands and diagnostics are in
`audit/current-iteration/source-census/baseline-build/REBUILD_RECEIPT.json`.

## 3. Controlling referee report and applicability

The controlling report is the exact 34,571-byte `REFEREE_REPORT.md` at
`reviews/a2-dyn-v115-double-clearance-external-top4-review-2026-10-15/`, with:

- report commit `f01482035a0b945b50f1f9c30f30ef35077558dc`;
- canonical report root tree `8c91a1709d4c8829d75f186b028e04ae7cb792a6`;
- report Git blob `9c68b0e8b31cd196c732514a29ebd44d95964243`;
- report SHA-256 `4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06`;
- explicitly reviewed author commit `31792379408c5ace2c09284c2eb22d2331023433`;
- reviewed author root tree `008dba443ce2ca29b3e276b1bf05bcf7021011c1`.

The report is an author-requested AI-assisted report, not a human journal
verdict. Its six major and nine minor objections remain the response framework,
with later native proofs evaluated on their own statements and hypotheses.
The actual source/report pairing matters: the report does not directly review
the later summable-source or global-minimizer author source. No favorable review
of the separate A2 geometry paper is attributed to A2-DYN.

All 90 distinct retrieved historical A2-DYN report texts remain byte-preserved.
The v112 report committed at `d7fd0b24314d7341f9a611130bb650371d2d5ef2`, blob
`0ad9f500c92db32ea4fc9f6d9ee28630b4484699`, remains relevant to historical source
and capacity obligations not superseded by an actual later proof. The current
[RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md) supplies the exact new responses;
the retained historical response matrices preserve the original objections.

## 4. Historical wrappers, unavailable objects and source completeness

The full census retains the distinction between complete manuscripts and
partial or administrative successors. The sublevel-clearance source at
`d5c81e1e6e9ec8d8bd121372966ad3b012445378`, with later receipt head
`796e70b65ec17bccb165e047534ed07dd4b148e0`, contributed genuine modules 300–301.
It did not independently replace the complete native main with a new qualified
whole manuscript. Preparation heads `ac6a9b5314f5253bea6ff3d4f7bef2103f7fe2a3`
and `53cce33a8d33db0b95a2375cb0ae33d5e801f437` have the observed unchanged papers
tree `25bf716fc75c59fa62df39784e4b494fa95122ab`. Qualification files, branch names
or successful preparation steps are not additional mathematical source bodies.

The original summable-source directory was freshly traversed at article tree
`5575389060a6ba0ddaa0079be066ae41b107a49c`: it contains exactly 103 files in four
trees. All 103 local preserved files match those actual remote source identities.
Its own old manifest lists 982 entries. Exactly 101 listed entries are present
with matching identities, 881 listed paths are absent, and the two actual
unlisted files are `PROOF_INDEX.json` and `SOURCE_MANIFEST.json`. This discrepancy
is still real; it is not repaired retrospectively by declaring an unavailable
archive to exist. Its complete active native proof chain and the broader
archive qualification are different claims.

Fresh 2026-10-19 requests again returned GitHub API 404 for the claimed local
predecessor commit `612cc64d6b5506981f337ccc019c6478e82b9b61`, archive-index blob
`244d6d0f0d3cbcce11955bcf18c2b38a7fdb14fd`, archive blob
`486d012476e251af0cf9bb2d93c70c095cbc3a56` and later CI archive blob
`c4041625d60e0dc93792206ca2ce3dd925bb4084`. The actual responses are retained in
`PUBLICATION_CHAIN_AND_UNAVAILABLE_OBJECT_READBACKS.json`. No evidence or source
identity is inferred from those unavailable objects.

## 5. Inherited completion, original model and the remaining obligations

The selected complete author source already contains the actual physical horizon
and angular curve-growth arguments, sublevel displacement bounds, all-center
clearance estimates, optical comparison structure, exponential anchor-layer
localization for every global minimizer, and the explicit positive-source Borel
exceptional set with exact section collars. The present iteration inherits their
proof bodies. It does not repackage those completed arguments as new results or
silently reopen discharged intermediate estimates.

The inherited exceptional-source estimate is a total-variation estimate. It
does not, by itself, give an essential bound on its density over the original
full physical roof after the required `m^2` normalization. Similarly, central
geometric comparison costs and an exact central collision/section record do not
by themselves settle shallow comparison capacity, singular paired traces,
physical multipliers, whole-cylinder pressure, complete Fourier tails or the
conditional microscopic return denominator. The new proof modules must be read
against these precise inherited boundaries. Their exact mathematical scope and
minimum remaining closure conditions are recorded in
[PROOF_LEDGER.md](PROOF_LEDGER.md).

The triangular lattice, radius interval `[9/20,47/100]`, unit physical speed,
collision measure `d alpha d p/(4 pi)`, original section normalization
`91/(10000 pi)`, original return event, complete collision words, original roof,
microscopic windows and ordered limits are retained. The original arithmetic
factor and four-coordinate raw inversion goal are not replaced by a comparison
Markov system, changed event or averaged limit. Conditional source-height
statements remain conditional on the explicitly named true-source pressure,
optical or chart inputs that they use.

## 6. Actual CI evidence and the new isolated delivery

The previous CI run `39151057063`, at exact scientific/receipt head
`878d3da9309ed7f71bce80c55cc52d96836ea920`, has now genuinely completed
successfully. Its native job `117744614636` and all eleven steps succeeded;
the run's update time is 2026-10-18T19:25:27Z. The retrieved artifact
`12147833077` contains actual source/math/typeset receipts for the unchanged
preceding mathematical source: 38 mathematical commands, a 147-page native main,
and the nine-command 390-source historical rebuild yielding 26/883 pages.
The earlier publication snapshot saying that the run was queued is preserved
as a correct observation at its original time. It is not rewritten as though
success had already been known.

That actual prior success does not qualify a new head. The new dedicated workflow
is `.github/workflows/a2-dyn-physical-tube-source-height-20261019.yml`, with its
identical article-local copy under `ci/`. It uses the actual preceding workflow's
complete native build sequence, pinned actions and dependencies, the new article
path and only the new author revision branch. Every older workflow and branch is
preserved. Current compilation, mathematical verification and post-publication
CI are reported in their own actual receipts and
[PUBLICATION_STATUS.json](PUBLICATION_STATUS.json); unobserved future outcomes
are not inferred from this baseline audit.

The new directory is
`papers/A2-DYN-physical-tube-source-height-author-revision`. Its source-manifest
helper verifies the unchanged original immutable anchor and a separate pinned
preceding-author anchor before freezing or checking current source. This guards
the entire inherited 260–309 native chain, all eight unchanged auxiliary/model
inputs and the sixteen preserved preceding author documents/helpers. The old
manifest, proof index, responses and helper sources remain exact historical
files. The preservation mechanism and all boundaries are detailed in
[HISTORY_PRESERVATION_AUDIT.md](HISTORY_PRESERVATION_AUDIT.md).
