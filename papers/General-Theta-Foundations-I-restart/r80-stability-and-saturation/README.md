# General Theta Foundations I — R80 author source

Begin with [START_HERE.md](START_HERE.md). This is the complete native English manuscript, paired technical supplement, independent retained companion, mathematical provenance and author response. It continues R79 source `90cae2f5aca243b39d3a2194a4d6e0696671a101` and publication `a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2` on an independent revision branch.

## Current files

| File or directory | Role |
|---|---|
| `main.tex`, `preamble.tex`, `references.tex`, `sections/` | Complete current main article and native mathematics |
| `supplement.tex`, `supplement-*.tex` | Current technical supplement, paired cross-references and retained independent proofs |
| `companion-r58/` | Exact separately compilable R58 companion |
| `RESPONSE_TO_REFEREE.md` | All ten major and forty technical R65 replies, plus historical obligations |
| `THEOREM_INDEX.json`, `THEOREM_MAP.md` | Actual native document, statement number, page and source inventory |
| `THEOREM_DEPENDENCIES.json`, `THEOREM_DEPENDENCIES_R80.md` | Complete inherited-plus-current author proof declarations |
| `provenance/R80_DECLARED_STATEMENTS.json` | Precisely scoped author additions, including explicitly classical material |
| `PRESERVATION_MAP.md`, `provenance/R79_COMPLETE_PRESERVATION.json` | Complete 806-file predecessor retention |
| `provenance/r80-audit/` | Fresh source/report selection, full-ref census and authenticated historical delta |
| `SOURCE_MANIFEST.json`, `seal_source.py` | Exact file/mode/hash inventory and inherited identities |
| `verify.py`, `diagnostics_*.py`, `requirements.txt` | Native source-bound reproduction and finite mathematical diagnostics |
| `../r80-stability-and-saturation-publication/` | Built PDFs, actual strict receipt, diagnostics, native logs, visual inspection and remote identity records |

## Strict reproduction

Use the exact **source SHA** recorded in the publication receipt, not the later publication commit. The strict verifier deliberately rejects a different Git HEAD, changed source bytes, absent predecessor objects, a modified old paper tree, unlisted files, a shortened inherited theorem inventory or a changed new-source boundary. A shallow checkout must contain the controlling R79 source and publication ancestor objects. Git-backed reproduction is different from compiling an unversioned downloaded folder.

The native tools are `pdflatex`, `pdftotext` and `pdfinfo`. Python dependencies are pinned in `requirements.txt`; an isolated environment can install that file. Use Python without bytecode output to keep the sealed source unchanged. From this source directory, with an entirely fresh output directory outside it:

```bash
python3 -B seal_source.py --check
python3 -B build_theorem_map.py --check
python3 -B verify.py --source-commit SOURCE_SHA_FROM_PUBLICATION_RECEIPT --out /tmp/theta-r80-reproduction
```

Replace the uppercase placeholder by the full forty-character source commit. The publication entry supplies the literal committed value. Do not run strict mode at the publication child and substitute its hash for the source hash.

The verifier authenticates all predecessor files and proof bodies; checks the author map; reconstructs the retained historical corpus and both successive deltas; runs every declared R61–R80 diagnostic in ordinary and optimized Python; requires byte-identical diagnostic outputs and explicit non-disabled checks; compiles main and supplement in alternating passes with paired auxiliary references; independently compiles the R58 companion; rejects unresolved citations, references, multiply defined labels and overfull boxes; and compares every compiled theorem locator to the sealed index. Its receipt records exact tool versions, source trees, counts and document hashes.

`--draft` is an explicit alternative for source development. It neither binds a committed source nor returns a final PASS. `--skip-diagnostics` is permitted only in draft mode. A failed attempt writes a failure receipt; later editing cannot change that receipt into success. Build outputs stay outside the source. The publication packet preserves relevant failed/draft attempts alongside the final source-bound result.

## Updating the source responsibly

The exact 252-entry R79 proof ledger is retained under `inputs/r79/`; its nondisplay fields are copied without semantic editing. New declarations are supplied separately, then combined with the actual native index by `build_theorem_map.py`. Automatically extracted LaTeX references are syntax, not automatically logical dependencies. A main/supplement move changes a locator, not the inherited proof authority.

After a mathematical or layout edit, obtain a new complete paired native index, update declarations and generated maps, refresh the complete predecessor preservation map if an editorial wrapper changed, and create a new source seal. Only then create a source commit and run strict verification on that actual SHA. The later publication child supplies receipts and PDFs without altering the mathematical source tree. Source sealing alone proves neither mathematics nor a successful build.

The general real-algebraic synthesis theorems prove computability under encoded hypotheses. The diagnostic scripts do not execute arbitrary quantifier elimination, certify worldwide priority or replace written proofs. The repository records no new independent human expert verdict or editorial acceptance.
