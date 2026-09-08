# A1 v32 — causal compatibility and finite certificates

This directory is the integrated English revision source for subsequent referee review.

Branch: `revision/a1-english-v32-causal-certificates-2026-09-08`

## Reading entry points

- `main.tex`: complete article entry, including the inherited attained collision classification, the new nonregenerative compatibility and certificate sections, and all inherited graph and regenerative sections.
- `companions.tex`: complete inherited companion entry, unchanged.
- `v32/new_results.tex`: the full new proof module, byte-identical to the delivered v32 revision package.
- `RESPONSE_TO_REFEREE.md`: the complete delivered response, byte-identical to that package. Its preparation-session status paragraphs describe the earlier preparation, before this source publication; they are not the current publication status.
- `v32/model_ledger.tex` and `v32/positioning.tex`: model conventions and theorem-level positioning.
- `revision-v32/SOURCE_PUBLICATION.json`: pinned provenance and publication scope.

## Preservation

The whole native v30 directory is inherited by using its Git tree `42235c2a07fe24eb8d2cd07dcf6c58a933f01f81` as the base of this new directory. All inherited proof and history subtrees remain unchanged. The replaced main entry, README, response and build entry are additionally retained under `v32/inherited_entrypoints/`. The original `papers/A1-english-v30-multilevel/` directory and all existing review files are unchanged in the repository.

The new introduction uses the prepared opening and compatibility text through TeX inputs rather than duplicating those two components inline. It retains the original substantive introduction body and its main theorem input. The bibliography wrapper composes with the inherited bibliography; it does not remove entries.

## Source-first publication and build status

The owner requested publication to GitHub before further build work. This is a source publication through the authenticated Git data API, not an execution of the preparation package's build-gated `apply_revision.py --build --push` command.

The complete main-and-companion build has NOT been executed or visually inspected in this publication step. No successful CI result or formal mathematical verification is asserted. The earlier 13-page new-results PDF remains a separately delivered artifact; this source publication does not claim that PDF is a complete article-and-companion build. Historical v30 diagnostic and build records copied with the source remain historical, not v32 validation.

## Build from this directory

```bash
python3 build.py --manuscript-commit "$(git rev-parse HEAD)"
```

The native builder requires `pdflatex`, compiles both full volumes without shell escape, exports cross-volume labels, and rejects unresolved references and overfull boxes by default. Its presence is not evidence of an executed build. No workflow, repository protection, permission, existing branch or main-branch content is changed by this source publication.
