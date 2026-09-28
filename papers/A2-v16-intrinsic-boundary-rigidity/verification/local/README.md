# Local source-content evidence

`receipt.json` is the actual primary-only execution receipt. `blob_manifest.json` identifies the exact locally executed source bytes by SHA-256 and Git blob ID. The receipt deliberately has null Git commit/tree and hosted run fields because this execution was performed in a container source directory. Remote publication does not change that execution category.

The complete raw local logs and built primary PDF are supplied in the accompanying conversation validation archive. Their exact digests are in the receipt. The receipt's short log names refer to that execution's `verification/current/` directory; the log bytes are not duplicated here in the Git repository. Running `tools/run_validation.py` creates a fresh `verification/current/` with raw logs and a new receipt. The hosted workflow uploads those current logs and all built PDFs as a commit-labelled artifact.

Supplement S was preserved by Git tree identity but not rebuilt in this local execution. No result here constitutes an independent proof certificate or a completed hosted run.
