# Revision 88 source and build qualification

Both `bash build.sh` and `bash build.sh --local` run normal and optimized finite diagnostics and compile the entire article and supplement. The local option is rejected in CI and does not qualify a remote checkout.

The verifier pins the v87 paper tree and controlling v85 report blob. It checks every inherited core, Python source, appendix, bibliography, provenance file and v87 top-level snapshot; all inherited claim flags must retain their values. The active count is 207. The actual recorder union must be exactly 207, with 204 inherited cores in the supplement and three new cores in the article.

The tests use explicit exceptions rather than assertions removed by Python optimization. They check capped layer-cake identities, complete overlapping pulse bounds, weighted segment traces including zero incoming gradient, and all norm/exponent arithmetic. The shrinking-spike fixture protects the distinction between finite local norms and essential height.

Native TeX references must stabilize with no LaTeX/package/pdfTeX warning, overfull box, undefined reference or missing character. All PDF word boxes are checked; every article page and selected archive pages are rendered. These tests establish build and finite-fixture properties, not mathematical certification.

A remote status is valid only when actual successful runs identify the final v88 author SHA. Neither the v87 baseline runs nor a local archive build substitutes for that evidence.
