# A2 v14 — independent harsh referee packet

**Date:** 11 September 2026. **Frozen author commit:** `e136929b120912586266fb78e0ae7b3c9d43bfd6`.

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md). The recommendation is negative for acceptance at the requested four-journal level, principally on significance. The previous principal requests are closed, and no fatal error was found in the inspected new proofs. This is an author-requested AI-assisted assessment, not a journal decision or a formal proof certificate.

[SCALAR_LINEARIZATION_AND_WIDTH_BENCHMARK.md](SCALAR_LINEARIZATION_AND_WIDTH_BENCHMARK.md) supplies a complete scalar comparison and explains exactly what the width datum contains. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) pins the reading scope and distinguishes executed verification from author claims.

## Reproduce the independent diagnostics

The source is [verify_review.py](verify_review.py); the recorded result is [verification.json](verification.json). The script requires Python 3, NumPy and SciPy. The recorded environment and versions are in the JSON. From this directory:

```sh
python3 verify_review.py --output diagnostics.normal.json
python3 -O verify_review.py --output diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

The recorded paired runs passed 3,216 explicit checks with byte-identical outputs. Exact rational checks and floating-point local Euclidean stationary-bridge checks are reported separately. Numerical low-order consistency is not a proof of all stated theorems. Different numerical environments may change final floating-point digits.

Only this new review directory is added. Author manuscripts and previous branches remain unchanged.
