# Complete preservation map — R80 from the actual R79 author source

## Exact baseline and complete inventory

The controlling predecessor is source commit `90cae2f5aca243b39d3a2194a4d6e0696671a101`, through publication commit `a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2`, paper subtree `582c4a664cb571c63927940ab7ef08be869cf10b`. The manifest SHA-256 is `e603a906514127a45525deef79fc4462d74d7784e57d5f6da0b6af108a3fd1a6`. The entire 806-file source was copied to the independent R80 source directory. All original branches and paper directories remain untouched.

`provenance/R79_COMPLETE_PRESERVATION.json` maps **every** predecessor path to an exact current or archival path, with byte count, Git blob and SHA-256. Unchanged files stay at their original relative paths. Any replaced editorial wrapper or tool is also preserved under `inputs/r79/`, including the prior main/supplement wrappers, introduction, references, response, maps, manifests and verifier. The fixed predecessor manifest and actual old Git tree prevent the new map from silently shortening the inventory. File executable modes are checked as well as bytes.

## Active mathematics and independent chains

| Mathematical material | Current traceable location |
|---|---|
| All 252 R79 statements and full current proof bodies | Main/supplement native inputs; `THEOREM_INDEX.json` provides current locators |
| Exact original 252-record proof authority | `inputs/r79/THEOREM_DEPENDENCIES.json`; every nondisplay proof field is retained in the new complete ledger |
| General nonreset support, dark feasibility, model quantifiers and algebraic frontier | `sections/54-robust-instrument-frontier.tex`, byte-identical |
| Same-label regularization, uniform primitive stability, history convergence and positive-success refinement | `sections/55-memory-regularization.tex`, byte-identical |
| Golden-ratio frontier and hidden-model routing boundary | `sections/56-exact-hidden-model.tex`, byte-identical |
| Reported-reset frontier, exact resource hierarchies and optimal reset memory | `sections/16-reset-control.tex`, `sections/52-optimal-reset-memory.tex`, `sections/53-reset-memory-frontier.tex` |
| Shared preparation, group/Fourier realization and initialization charges | Main retained Sections 31, 43, 45, 49, 51; complete related group/Fourier proofs in the current supplement |
| Original actual-history causal comparison and paid realization | `sections/02-experiments.tex`–`sections/04-proof.tex` and the associated current supplement |
| Predictive state, information compression, finite-order quantum measurement, two-stage reset, memory/communication, rank-constrained discrimination, optimality and duality | Independent developments in the current supplement, with all old labels retained |
| Spectral, geometric and boundary results | Current supplement's complete original sections, with local/global scope unchanged |
| Independently scoped R58 work | `companion-r58/`, exact tree `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`, separately compiled |
| Earlier derivations, raw reports, responses, proof ledgers and failed/valid execution history | Inherited `inputs/` and `provenance/` chains, supplemented by `provenance/r80-audit/` |

The protected mathematical body inventory contains **73 exact files** in `provenance/R80_RETAINED_BODY_IDENTITIES.json`. The supplement's inherited suffix, starting at its first retained mathematical input, is **33,060 bytes**, SHA-256 `aae18c3f8ac8fdb63e6763ae86b8c31568a036302e6b150896649d995b47d4ee`. New front matter may explain the current reading route without changing that suffix. New theorems occupy new source files; no old proof is silently rewritten or removed.

## Historical corpus

The fresh census covers 1,309 refs, 875 distinct authenticated heads, 2,715 ancestor commits and 7,273 scoped text blobs. The retained corpus is authenticated as a base plus successive deltas; its archives are not redundantly expanded into the source tree. The new 72-blob delta and portable checker live under `provenance/r80-audit/`. The complete records retain original reports and superseded or failed material as history, without promoting those files to current proof premises or new independent reviews.

## Mechanical enforcement and its limits

`seal_source.py` checks the fixed old manifest, all mapped file identities and modes, protected bodies, supplement suffix, companion tree, report body and inherited label set. `verify.py` additionally compares the entire old inventory to the immutable predecessor Git tree and rejects changes outside the new source directory. `build_theorem_map.py` retains every nondisplay inherited proof record and updates only actual native locators plus a new R79 authority layer.

Preservation establishes traceability and absence of silent deletion. It does not assert that the current authors have independently re-proved every historical statement or that all historical conjectures are now theorems. Edition-relative words such as “new” inside unchanged inherited bodies refer to their original author layer; the current front matter states what this revision actually adds.
