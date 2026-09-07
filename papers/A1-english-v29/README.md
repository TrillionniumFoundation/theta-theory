# A1 English v29 — occupation-flow revision

**Attainable information, exponent collisions, and adaptive memory**  
Qian Qi — 8 September 2026

Revision branch: `revision/a1-english-v29-occupation-flow-2026-09-08`.

## Manuscript and review basis

`main.tex` is the complete principal manuscript. `companions.tex` is the complete, separately compiled companion. The new directory is based on the entire native v28 Git tree, not on sibling-directory fallbacks or downloaded inputs. All inherited scalar, collision, causal, graph, separator, phase, policy-menu, evaluated-model and localized growing-graph developments remain active. No existing repository directory or branch is replaced.

The controlling report remains `review-basis-v26/REFEREE_REPORT.md`, read at `19fbf4fe0e7495afd537de73a63670a9cf5616e0` and assessing `a2e5d3737085241137211f1cf21393d5bcafa1ce`. The integration base is the published localized v28 commit `090f9875d71a7765d60838f737508f0b17bdc9da`. An earlier unpublished occupation-flow draft was recovered and incorporated under **v29** labels; it is not confused with the published localized v28. `NATIVE_SOURCE_RECORD_V29.json` records that provenance.

## Mathematical addition

`v29/occupation.tex` gives the occupation-measure converse, its dominance over the separator integral, and exactness within the class specified by local random-path bounds. `v29/initial_information.tex` retains the pre-acquisition information constraint, proves a perspective-flow refinement and an exact dual, and specializes these results to graph experiments with explicitly counted finite decoder descriptors. `v29/evaluated_refinement.tex` evaluates every density, recovery and evidence factor in the unchanged two-trial experiment.

The new all-budget coefficient is `1/8306688`. Keeping the old event and constants already gives an exact factor four over its separator certificate; using the complete known first-failure law gives the exact ratio `1499109768/1071875` over that old certificate. The factor below `4.06` against the sharp statistical coefficient is a high-resolution comparison, not a finite-budget ratio theorem. Sharpness of the path relaxation is not equality with every statistical minimax risk.

`RESPONSE_TO_REFEREE.md` provides the point-by-point response. `PROOF_LEDGER.md` lists active labels, dependencies and quantifiers. The v28 response, ledger and main entry point are retained as explicitly named baseline files. Older receipt files keep their historical version meanings.

## Reproduce

With the full branch checked out and Python 3.10 or newer:

```sh
python papers/A1-english-v29/build.py --prepare-only
python papers/A1-english-v29/build.py
```

The second command also requires `pdflatex` and the packages in `preamble.tex`. It creates a separate `build-v29/native` directory, alternates both volumes through five passes, uses label-only external auxiliaries, and rejects undefined, duplicate or unsettled references and overfull boxes. It does not rewrite original source. `build-v29/BUILD_RECORD_V29.json` records actual success or failure. Neither command downloads dependencies.

For the new finite diagnostics alone:

```sh
python papers/A1-english-v29/diagnostics_v29.py
python -O papers/A1-english-v29/diagnostics_v29.py
```

## Executed validation scope

The new finite diagnostic suite was rerun: **11,345 explicit checks**, with byte-identical ordinary and optimized output. The twelve-page `new-proofs.tex` component was typeset separately in three passes, with inherited references explicitly represented as source locators. It is not the complete principal manuscript. Session and rendering receipts are under `validation/`.

**No completed native two-volume build or successful GitHub Actions run is asserted for this revision session.** The full source has been integrated; the separate new-proof PDF and successful finite tests must not be presented as full-manuscript typesetting or mathematical certification. The significance judgment remains for renewed independent review, not for a test counter or publication receipt.
