# Rebuild protocol

Run `python verify.py`, `python regression.py` and `python -O regression.py`. Normal and optimized output must agree. Run `build.py` with the exact remote ordinary-source commit and expected native tree; it performs two isolated native builds, each with three TeX passes, and rebuilds the full pinned R24 packet recursively. Outputs and receipts must be outside ordinary source, under artifacts/evidence or an external directory.

The manifest checks all ordinary UTF-8 files, SHA-256, Git blob identities and the native tree. The TeX recorder checks actual input files, labels, references, bibliography usage and balanced formal environments. Build logs reject overfull boxes and undefined references. Finite diagnostics use exact rational identities except explicitly labeled quantum matrix diagnostics; neither class verifies continuum proofs.

The source commit, artifact child and final evidence child are distinct. An independent rebuild must download the actual remote artifact and hash all input files before and after. PDF byte parity is required within a fixed environment; cross-environment page/text/render parity is reported separately and must not be described as byte parity if it is not. The final evidence commit must not modify ordinary source or PDFs.

No old review/realization/archive branch is a write target. The initial canonical anchor remains independently identifiable. A ref-update attempt blocked by the tool is not claimed successful; subsequent delivery uses append-only newly named refs and records the actual returned heads.
