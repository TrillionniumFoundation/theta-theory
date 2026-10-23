# General Theta Foundations I — R75 source entry

This is a complete author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, Qian Qi. The title, research identity and Annals / Acta / Inventiones / JAMS objective are retained.

## Current mathematical submission

The complete English main article is `main.tex`; its paired technical supplement is `supplement.tex`. The independent retained R58 companion is `companion-r58/main.tex`. Current native PDFs and actual source-bound execution receipts are in [the sibling publication entry](../r75-nonabelian-stationary-memory-publication/START_HERE.md), added in the publication child of the sealed source commit.

A minimal reading path is:

1. Introduction and response/resource conventions.
2. Retained reversible criterion, permutation-core normal form and contrast theorem.
3. New orbit multiplicity, normality/convexity and the complete symmetric-group contrast law and its boundary rigidity.
4. General stationary initialization and complete noisy-instrument realization.
5. The current supplement's stopped-law approximation and the explicitly referenced spectral/recurrent-projection proofs.
6. The retained actual-history comparison and the independent causal/optimization/geometric developments at their stated scopes.

The entire historical archive is available for traceability; it is not an implicit premise of every new theorem.

## Review and mathematical status

- [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md): all 10 major and 40 technical R65 comments, inherited closures and current additions.
- [THEOREM_MAP.md](THEOREM_MAP.md) and [THEOREM_INDEX.json](THEOREM_INDEX.json): actual current compiled statement numbers, pages and native sources.
- [THEOREM_DEPENDENCIES.json](THEOREM_DEPENDENCIES.json): logical proof prerequisites, explicit references and limits.
- [PROOF_AUDIT.md](PROOF_AUDIT.md): written proof checks, diagnostic scope and evidence distinctions.
- [RESEARCH_STATUS.md](RESEARCH_STATUS.md): precisely stated new results and remaining research obligations.
- [LITERATURE_AND_PRIORITY.md](LITERATURE_AND_PRIORITY.md): original literature checked and classical/inherited/new claim boundaries.
- [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md) and [PRESERVATION_MAP.md](PRESERVATION_MAP.md): immutable baseline/report identities and every inherited file's preserved destination.

The controlling author source is R74 at `29b999abf11c43709e64be58765aa1984d13ac91`, delivered at `c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0`. The latest substantive deposited report is R65 at `358481b21ceeeedb1205ebd30f86982e32a2cb04`; it reviewed the R65 submission, not later revisions. Its exact body is `provenance/R65_REFEREE_REPORT.md`. The fresh all-head/content audit found no later independent substantive report.

## Reproduction

Use the pinned packages in `requirements.txt` and native `pdflatex`, `pdftotext`, `pdfinfo`. On the **exact sealed source commit** recorded by the publication, run:

```bash
python verify.py --source-commit FULL_SOURCE_COMMIT_SHA --out /absolute/fresh/output
```

Strict mode verifies actual Git HEAD, the complete source manifest, all 275 predecessor files, the inherited proof bodies and companion, all 20 diagnostic suites in ordinary and optimized Python, and three native LaTeX passes per document. Its output is outside the immutable source.

For an edited or extracted source, `--draft` permits a native build but cannot issue a final source-commit PASS. `--skip-diagnostics` is allowed only in that draft mode. Diagnostic results are finite checks, not proof-assistant verification. Actual hosted Actions status is reported separately for the corresponding SHA. No human assessment or editorial decision is asserted.
