# General Theta Foundations I — eighth decision-spectrum revision

Author: Qian Qi. Date: 23 September 2026.

`paper.pdf` is the canonical journal article. `complete-development.pdf` preserves the same canonical material plus all preceding mathematical bodies. The companion is not an alternative canonical article. Native entry points are `main.tex` and `development.tex`.

## Rebuild

From the repository root, with Python 3.11+, NumPy, SciPy, pdfTeX/LaTeX, Latin Modern, AMS packages, microtype, geometry and hyperref installed:

```sh
python3 papers/GTF-I-v8-decision-spectrum/build.py
```

`requirements.txt` records the numerical versions used for the finite LP diagnostics. The analytic proofs do not depend on those diagnostics. A complete source archive contains all inherited inputs needed by both TeX entry points; rebuilding does not require downloading any older branch or paper.

The builder checks the SHA-256 identity of every inherited input, executes ordinary and optimized current diagnostics and all seven inherited suites, rejects each specified incorrect variant, compiles both PDFs to stable references, verifies retained and shared labels, and records the actual source identity. A genuine Git checkout of the remote repository is distinguished from the local 133-file source-archive reconstruction.

## Review materials

`RESPONSE_TO_REFEREE.md` (latest nominal-v8 report), `RESPONSE_TO_V7_R2.md` (earlier complete reply), `PROOF_LEDGER.md`, `RESOURCE_SIGNATURES.md`, `HISTORY_AUDIT.md`, `HISTORY_INPUT_MANIFEST.json`, `HISTORY_NATIVE_INVENTORY.json` and `LITERATURE_AUDIT.md` describe the revision and its actual scope. `INHERITED_INPUTS.json` pins the predecessor archive. `SOURCE_MANIFEST.json` pins the new source inputs. Rendering and rebuild verification are separate evidence records.

## Branch delivery

Intended new working branch: `revision/general-theta-foundations-i-v8-decision-spectrum-2026-09-23`.  
Intended frozen review branch: `revision/general-theta-foundations-i-v8-decision-spectrum-referee-ready-2026-09-23`.  
Remote base: `fc6d51a47b42a3f097ea530b67616591c421db3b`.

The existing remote v8-spectrum branch is not overwritten. The delivery includes an additions-only patch and a guarded import script. The current environment has read-only GitHub connector functions and cannot resolve github.com from the terminal. Local publication is therefore not represented as an update to a GitHub branch; the final handoff record states the observed status explicitly.

No old source edition, review or main branch is modified by this revision. Mathematical validity and novelty require independent evaluation; successful compilation and finite checks identify the submitted object, not its acceptance.


## Pinned dependency checks

`PIPELINE_DEPENDENCIES.json` supplies eleven machine-readable theorem adapters/statuses, including the current A2 v122 statistical source and its separate independent primary chain. `python3 papers/GTF-I-v8-decision-spectrum/verify_pipeline.py` checks local identity/label consistency. Add `--remote` to check the watched GitHub branch heads; a moved ref or unavailable network is a failure, not evidence of freshness. This watched-ref check does not discover arbitrary newly named branches, so a new review freeze also requires explicit branch discovery.
