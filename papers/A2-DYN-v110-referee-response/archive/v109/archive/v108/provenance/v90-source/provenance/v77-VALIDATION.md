# A2-DYN v77 validation contract

`bash build.sh` requires an exact Git checkout. `bash build.sh --local` accepts a materialized source archive only outside CI and still builds both PDFs and every inherited module; it cannot certify a remote commit. The verifier reconstructs and checks the complete v76 paper tree, preserves every inherited core, appendix, Python source and bibliography, and checks current claims without mutating them. An exact checkout also checks the v76 report blob and GITHUB_SHA.

Finite checks include exact symbolic field/coarea/drift identities, the rational section constants, quadratic flow and Jacobian fixtures, angular critical integrals, rational maximal-coupling marginals, angular BV inequalities, and ordered exponent algebra. The inherited v74/v75/v76 finite fixtures remain active. Six older diagnostic scripts run in both normal and optimized Python. The historical verifier receives `evidence/certify_excursion.json` explicitly, fixing the v76 producer/consumer mismatch without changing that inherited source.

Native TeX must stabilize without LaTeX/package warnings, undefined references, overfull boxes or missing characters. The actual recorder union must cover all 176 active modules: three in the journal and 173 in the supplement. All page boxes are checked; the article pages and sample supplement pages are rendered. Evidence binds to the exact checkout and is uploaded with the source archive by `.github/workflows/a2-dyn-v77-qualification.yml`.

A successful run establishes only the specified preservation, finite-fixture, build and layout checks. It is not a proof of the full raw LLT, independent human review, or formal certification. Passing status must be read from the actual workflow run, not inferred from this contract.
