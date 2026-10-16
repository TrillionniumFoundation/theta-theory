# Actual local execution evidence

`LOCAL_RUN_SUMMARY.json` is extracted from the actual completed 33-command receipt. `LOCAL_COMMAND_INDEX.tsv` retains each command-record name, UTC interval, measured duration, exit code and log SHA-256. `VISUAL_INSPECTION.json` records the rendered-page check. These observations refer to the source-manifest digest in the summary, not to an unspecified branch or future CI run.

The complete uncompressed receipt, its lossless gzip copy, all stdout logs and command arguments, raw physical cases, exact native PDFs and earlier failed/interrupted attempts are retained in the full downloadable preservation delivery. The larger outputs are not duplicated in this new Git evidence directory. The summary records the complete receipt, gzip, raw-case and PDF hashes so the delivery can be verified. Run `bash build.sh all` to produce a new independently timestamped receipt and outputs from this exact source.

All inherited evidence elsewhere in this article remains unchanged. This local evidence is not a remote CI completion, independent expert certificate, or proof of the final raw LLT. Actual remote commit/ref/workflow observations belong to the separate post-push receipt.
