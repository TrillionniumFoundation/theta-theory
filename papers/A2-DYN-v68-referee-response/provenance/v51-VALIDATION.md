# Validation: revision 51

The source verifier checks the exact full v49 paper tree; all 107 inherited core modules, 135 inherited scripts and compiled appendices; retention of every inherited mathematical label; complete TeX inclusions, references and citations; the ordinary-source Merkle tree; and the new workflow hash. Both the latest v50 submission-status report and substantive v49 report are checked by Git blob hash in strict mode.

Normal and optimized finite checks must agree. Finite tests cover the signed convolution/source identity, positive-part contraction, separate positive residuals, exact conditional minorization and residual mixture mass, rational band exponents, a thin-hole negative control, and positive-spike/forward-likelihood negative controls. The inherited v49--v37 finite checks and six geometry/return diagnostics are also executed. These tests are not continuum proof verification.

`build.sh` uses strict source verification and native TeX without shell escape. The dynamic receipt is created only after a clean stabilized build; GitHub execution requires the exact event SHA, run ID, matching committed ordinary paper tree, and clean scoped source. The workflow renders pages selected from actual theorem labels.

An explicit `--local-preflight` verifier option allows a missing report only outside GitHub Actions, reports the missing path, and is not a manuscript qualification. No workflow invokes that option. A preflight output does not substitute for the strict remote receipt. Static source files never predeclare a run successful.

Baseline manuscript evidence: v49 response run 37825377112 and copy run 37825400351. Baseline freeze-only evidence: v50 run 37861340498. Neither is new v51 execution evidence.
