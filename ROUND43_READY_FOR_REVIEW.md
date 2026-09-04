# Round 43 v2 ready for independent review

This branch is a fully materialized, line-addressable strengthening of the
Round 43 response to `REFEREE_REPORT_ROUND42_GPT56_PRO_HARSH.md`.  The
canonical article is `ROUND43_REVISION.tex`; no source generator, runtime
source rewrite, or write-enabled workflow is needed to read or build it.

The v2 manuscript adds an exact response–moment recursion, a finite
Gram/Hankel reconstruction algorithm with explicit condition propagation, a
concrete shrinking-depth coefficient radius, and a no-washout adaptive
protocol with linear physical-time cost and honest finite-sample coefficient
cylinders.  The existing full two-sided posterior LDP remains in force for the
logarithmic-washout protocol.

At the review freeze the branch retains exactly one verification workflow,
`.github/workflows/verify-round43.yml`, with read-only repository permissions.
Referees should freeze the final branch head named in the review request and
compare `round43/SOURCE_MANIFEST.json`, `ROUND43_LOCAL_VERIFICATION.json`, and
the committed `ROUND43_REVISION.pdf` against that immutable object.  The proof
ledger distinguishes mathematical arguments from executable consistency
checks and does not claim proof-assistant certification.
