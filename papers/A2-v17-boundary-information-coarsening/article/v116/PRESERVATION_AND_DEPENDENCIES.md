# Preservation and dependencies — A2 revision 116

The controlling source is v115 at `acfd3d57e0053e1b03df53020fd8e79e14599c03`; the controlling report is R115 at `1cb4e00c86699247454d21dbec2dcce01a9c6b8b`.

`history/v115_source/` contains all 24 immediately reviewed TeX files, exactly. Their SHA256 hashes are in `evidence/V115_SOURCE_MANIFEST.json`. `history/R115_REFEREE_REPORT.md` preserves the complete controlling report. Earlier v114 history is retained.

The active revision retains all 158 old theorem/lemma/proposition/corollary/proof blocks, all 201 labels, and all 27 bibliography keys. Seventeen active files remain byte-identical. The original introduction is retained under a more specific section heading; the new introduction and three new mathematical sections precede it. Hyperplane proof expansions are additions, not replacements of old proof blocks. The prior-work section gains an explicit comparison for the new family. The author and complete application program are preserved.

The geometry article and archival paper contain the same geometric source parts. The complete archival paper then includes every original application appendix. `make_crossrefs.py` exports only the opposite reading copy's labels, to avoid duplicate definitions.

The conductor reduction and contact-pencil classification have a self-contained dependency chain: elementary pencil multiplication, first-normal-layer surjectivity, exact coherent cokernel transport, finite-algebra determinant, primary exponents, and finite normalization. The earlier polar/quadratic/hyperplane results and all application proofs are not hypotheses for that chain.

The build computes current source/label counts instead of relying on this document. It checks archived bytes and active retention before compiling. A hash mismatch, a lost old environment, an undefined label, a missing citation, or a final LaTeX warning aborts the build. The receipt binds actual source bytes, PDFs, and logs to the mathematical-source commit; it does not certify the mathematical proofs.

Only the new revision branch is used. The original v115 and review directories are preserved; unrelated papers and branches are not updated.
