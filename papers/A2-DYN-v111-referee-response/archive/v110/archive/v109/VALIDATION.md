# Current validation summary — revision 109

This is the active validation entry point. Every status file under `archive/v108` is historical. Neither a compilation nor a finite matrix check is a proof of the organizing local limit theorem.

## Current-article local checks

The standalone current article was compiled with native `pdflatex`, with shell escape disabled and recorder output enabled. It produced a 12-page PDF, with stable references and no LaTeX, hyperref or overfull-box warnings. All 12 pages were rendered and visually inspected in a contact sheet; the endpoint proof and final residual statement were also checked from the source.

Normal and optimized Python produced identical diagnostic output: 518 exact rational optical/continuant cases, 450 floating Schur-complement cases, and 1,536 positive-part residual comparisons. The largest relative optical identity discrepancy in the recorded local run was `1.5860513327842167e-15`. These finite checks include visited-grazing versus unvisited-clearance diagnostics; they do not verify physical coverage or asymptotic shortage decay.

The original model source has exact Git blob `6af1dcb4548e1b5dd82b9a330dead6e04fd09797`. Local proof-source and diagnostic SHA-256 values are recorded in `provenance/local-validation.json`.

## Exact-checkout remote qualification

The dedicated workflow is `.github/workflows/a2-dyn-v109-source-and-manuscript.yml`. At the preparation of this manuscript commit, no successful run for this new manuscript SHA is predeclared. The earlier source-freeze-only commit is not mathematical qualification of the later manuscript.

The encoded build additionally compiles the complete archived article and supplement and checks recorder coverage of all 259 old modules and both new modules. This full archived build was not run in the local standalone directory. Its result is to be read from the exact-SHA workflow output, not inferred from the preceding revision's success.

The two v108 jobs did subsequently complete successfully; the separate provenance record preserves that later observation without changing the controlling report's freeze-time queued status.

## Mathematical verification boundary

The regular-point optical derivative estimate, original incident-component pairing construction, physical coarea summation and fixed-window spectral/pressure averages are retained source-pinned inputs. The current paper proves the stated endpoint passage and visited-grazing payment using them. It does not certify the global pairing construction independently, prove the remaining nongrazing microscopic abundance estimate, or assert a full raw LLT. No independent human review or formal proof certification is represented as having occurred.
