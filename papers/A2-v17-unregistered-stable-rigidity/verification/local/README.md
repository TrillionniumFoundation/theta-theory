# Actual local execution

`receipt.json` is a losslessly compacted copy of the validator's actual primary-only receipt. Its null commit, tree and hosted-run fields are intentional: local files were copied from authenticated connector output and compared by Git blob hash, not obtained through an authenticated Git checkout. `SOURCE_PINS.json` binds those exact primary/tool contents to the published tree.

The original eight stdout logs, final primary TeX log and unmodified pretty-printed receipt are supplied with the conversation's local verification archive. Archive SHA-256: `183888364d0d65b3123c352e55ea6ecd2e095b2d23b81619a8f2ddd0a3a4d849`. The log names in the receipt refer to that execution directory/archive; they do not pretend the raw logs are stored beside this compact receipt. The separately supplied 29-page PDF has SHA-256 `6380819ca65cde65446d05b10cb2dfb606272ba92337d2202d919eb3125662a0`.

The hosted workflow uploads its own complete actual output directory, including logs and staged supplementary PDFs. Its success must be checked from that run, not inferred from this local primary receipt. Re-running the validator may change timestamps and PDF metadata, and must produce a new receipt rather than overwrite the historical meaning of this one.
