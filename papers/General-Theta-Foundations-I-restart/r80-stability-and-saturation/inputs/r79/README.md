# General Theta Foundations I — complete R79 author source

This is an author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, continued from the complete R78 source at `e0377beea364e456af2301f5e4fec98fe343cbcb`. The research identity and the target of Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae and Journal of the AMS are retained. No editorial acceptance or independent expert endorsement is asserted.

Start at [START_HERE.md](START_HERE.md). The current mathematical addition is same-memory controller-label regularization and a primitive stability bound for the entire optimal cost frontier, uniform in all label budgets, for nonreset finite-dimensional quantum instruments with a fixed hidden model. Exact support verification and finite-model algebraic synthesis are inherited, explicitly credited and retained. Under a uniform per-command success floor the stability bound improves to Lipschitz with locally sharp scalar constants. A separate two-model experiment has the exact frontier `2, (1+sqrt(5))/2, 3/2, ...`.

## Current deliverables

The sibling [publication directory](../r79-robust-instrument-frontier-publication/) contains the native main article, current technical supplement, unchanged independent R58 companion, source-bound build receipt, actual diagnostic outputs, native logs and source/publication handshake. Its `PUBLICATION_RECEIPT.json` identifies the exact source commit. This source commit does not certify its own future execution: the later publication child supplies that evidence.

The mathematical source is `main.tex`, `supplement.tex`, `sections/`, the retained supplementary native files and `companion-r58/`. [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md) answers all ten major and forty technical items in the latest applicable deposited report and carries forward historical residual questions. [THEOREM_MAP.md](THEOREM_MAP.md) and [THEOREM_DEPENDENCIES_R79.md](THEOREM_DEPENDENCIES_R79.md) distinguish current locators, inherited authorities, logical premises, classical ingredients and the new proof chain.

## Native reproduction

Use Python 3.11 or later with `requirements.txt`, native `pdflatex`, `pdftotext`, `pdfinfo` and the TeX packages in `preamble.tex`. For example:

```bash
python3 -m venv /tmp/theta-r79-env
/tmp/theta-r79-env/bin/python -m pip install -r requirements.txt
```

Check out the exact **source commit** recorded in the publication receipt, not the later publication commit. In this source directory run:

```bash
/tmp/theta-r79-env/bin/python -B seal_source.py --check
/tmp/theta-r79-env/bin/python -B build_theorem_map.py --check
/tmp/theta-r79-env/bin/python -B verify.py --source-commit "$(git rev-parse HEAD)" --out /tmp/theta-r79-strict-reproduction
```

The output directory must be fresh and outside this source. Strict verification binds the real Git HEAD, computed source tree, complete unchanged R78 tree, all 694 preserved predecessor files, all 240 inherited statements, all 252 current statement locators, the retained mathematical proof bodies and the complete independent R58 companion. Its diff gate allows additions only inside this independent R79 source directory relative to the pinned R78 source commit.

All 27 inherited diagnostic suites and two current suites run ordinarily and under `python -O`, with byte-identical outputs required. Explicit checks reject disabled-assert diagnostics, missing suites, inconsistent counts, undefined citations/references, duplicate labels and overfull boxes. The main article, supplement and companion each receive three native LaTeX passes with shell escape disabled. Actual versions and counts are reported only in the execution receipt.

For an edited working copy or standalone source, use:

```bash
python -B verify.py --draft --out /tmp/theta-r79-draft
```

Draft mode reports `DRAFT_COMPILE_COMPLETE`, not a source-commit PASS. `--skip-diagnostics` is allowed only in draft mode. After mathematical or layout edits, copy the actual newly compiled theorem index into the source, regenerate the dependency map, update complete preservation pointers if necessary, and reseal before committing.

## Historical authentication and evidence

The portable history checkers authenticate 7,201 distinct historical text blobs: the unchanged 7,137-blob R78 reconstruction and the 64-blob R79 delta. The all-ref census records 1,307 remote heads, 873 unique head commits and 2,711 ancestors at its frozen snapshot. All raw head commit payloads and selected manuscript/report dependencies are bound to exact hashes. These counts identify an authenticated historical corpus; they are not a claim that every historical mathematical assertion is correct.

The R65 report remains the latest deposited substantive referee report with surviving objections. It evaluated R65, not this revision, and R66–R78 already supplied substantive responses. No empty or misleadingly named review branch, internal AI challenge, pipeline audit or native build is promoted to a new independent review. Details are in [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md).

Written arguments establish the quantified claims at the level of ordinary mathematical proofs. Finite exact and floating diagnostics, source authentication, native compilation, remote publication, hosted CI, formal proof checking, independent human evaluation and editorial judgment are separate categories. This project records the first four when actually performed; the receipt states the exact status of the others. General real quantifier elimination is a proved effectivity statement, not a claimed executed computation for arbitrary input.
