# General Theta Foundations I — complete R77 source

Start with [START_HERE.md](START_HERE.md). The source continues R76 source `891643799f2dfb2737ad5c147bf8def2d460630b` at publication `6943acf6ef96340c0387a18fe51d4855cac52823`. Only the independent R77 source and its sibling publication directory are added; the predecessor and all other paper trees remain unchanged.

## Native reproduction

Requirements: Python 3.11 or later; the Python dependencies in `requirements.txt`; native `pdflatex`, `pdftotext`, and `pdfinfo`, with the AMS, Latin Modern, microtype and cross-reference packages used by the retained preamble. Install Python dependencies into a separate virtual environment:

```bash
python3 -m venv /tmp/theta-r77-env
/tmp/theta-r77-env/bin/python -m pip install -r requirements.txt
```

From the R77 source directory, with the exact **source commit** from the sibling publication receipt checked out:

```bash
/tmp/theta-r77-env/bin/python seal_source.py --check
/tmp/theta-r77-env/bin/python build_theorem_map.py --check
/tmp/theta-r77-env/bin/python verify.py --source-commit "$(git rev-parse HEAD)" --out /tmp/theta-r77-strict-reproduction
```

Use a fresh output directory. The verifier rejects a wrong HEAD, wrong computed source tree, missing or changed inherited files, outside-paper changes, incomplete diagnostic execution, `assert`-based diagnostics that disappear under `-O`, unequal ordinary/optimized output, unresolved references/citations, duplicate labels and overfull boxes. It executes all 23 inherited and three new diagnostic suites twice, and three native passes each for main, supplement and R58 companion. It checks the native theorem index against the sealed 235-entry document/number/page/source map.

The actual verification environment records Python and library versions; a source manifest does not prove dependencies were installed. `requirements.txt` retains the pinned NumPy 2.3.5, SciPy 1.17.0 and SymPy 1.14.0 specification.

For a standalone source bundle or edited working copy:

```bash
/tmp/theta-r77-env/bin/python verify.py --draft --out /tmp/theta-r77-draft-reproduction
```

This emits `DRAFT_COMPILE_COMPLETE`, never a source-commit PASS. `--skip-diagnostics` is allowed only in draft mode and is explicitly recorded. Build outputs must remain outside the source tree. No LaTeX shell escape is used.

## Updating a future author revision

Copy this complete source into another independent paper directory and branch. Preserve this source commit and its manifest. After any mathematical or layout changes, rebuild the paired native index, regenerate the author map, revise the response/status/provenance, and seal the complete inventory. Strict final verification must run only after committing that source, with publication records committed separately. Do not edit a prior report or source tree to manufacture continuity.

## Interpretation

The diagnostics test specified finite instances, exact rational identities and floating tolerances. They are not substitutes for the written all-word, arbitrary-group, continuum or optimality proofs. No general quantifier-elimination computation is claimed. An internal AI challenge is not an independent human review. A local strict PASS is not a hosted CI run.

## Complete historical text reconstruction

All 7,024 authenticated historical text blobs are recoverable without a network call from the unchanged five base archive parts, the 168-member delta and the 192-member all-ref extension. The strict verifier executes the reconstruction check. From this source directory it may also be run separately:

```bash
python provenance/r77-audit/history-delta/verify_history_delta.py \
  --manifest provenance/r77-audit/history-delta/HISTORY_DELTA_MANIFEST.json \
  --base-parts provenance/r77-audit/history-base-parts \
  --delta provenance/r77-audit/history-delta/HISTORICAL_TEXT_DELTA_R77.tar.gz \
  --index provenance/r77-audit/full-scan/HISTORICAL_TEXT_INDEX.json.gz \
  --extension provenance/r77-audit/all-ref-scope-extension/ADDITIONAL_TEXT_CORPUS.tar.gz \
  --extension-index provenance/r77-audit/all-ref-scope-extension/ADDITIONAL_TEXT_INDEX.json.gz \
  --receipt /tmp/theta-r77-history.json
```

The checker reads archive members without extracting paths, authenticates each original Git blob and SHA-256, rejects duplicates and compares the complete index. Historical failure/materialization logs are retained as attempts; only the final reconstruction receipt states what was successfully authenticated. This is source authentication, not a new proof verdict on the archived mathematics.
