# Executed diagnostics and their scope — A1 v16

`validate.py` runs six unchanged author suites, then checks source preservation and builds the complete manuscript. Expected author assertion counts are: v10 7,904; v11 8,207; v12 26,158; v13 12,944; v14 7,400; v15 5,868; total 68,481. These are inherited regression suites executed anew, not new v16 mathematical results.

The optional `--prior-review` flag executes the original v15 referee script, pinned by SHA-256 `7b406a8a4bd16e61a0c5017232b20d0a9126d9d63150c343e84b7da8e3f4f22d`. It requires 1,800 exact assertions and `status=PASS`. This is a regression execution of a previously independent diagnostic, not a fresh independent referee report. Its five negative-control families are deliberate mutations, not defects found in the submitted manuscript.

The script writes current JSON receipts only after executing the tests. Each result includes source/output digests, the interpreter and, in GitHub Actions, the workflow input commit and run ID. The build records PDF page count and hash, preservation results, three TeX passes and absence of undefined-reference or overfull warnings. The standalone validation does not require a neighboring old paper; the optional reviewer run requires the full repository's immutable review script.

No numerical run proves continuum-uniform constants, an optimal minimax law, arbitrary-horizon behavior, novelty, or mathematical significance. The paper's retained proofs address the theorem statements. Source hashes establish preservation, not formal proof verification. Previous receipts are archived under `history/` and are never counted as current successful executions. Visual inspection is documented separately in `VISUAL_INSPECTION.md`.
