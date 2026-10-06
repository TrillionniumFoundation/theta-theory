# Reproducibility note — General Theta Foundations I, Revision 95

The journal object is `quantitative.tex` with one linked `supplement.tex`. The standalone journal archive contains exactly their active source dependencies, this note, the journal README, the independent verification script and a hash manifest. It needs neither the repository history nor any historical PDF. The separate research package preserves the entire mathematical and audit record.

Install TeX Live with amsart, the supplied LaTeX package dependencies and Latin Modern; Python, PyMuPDF 1.26.7, SymPy 1.14.0 and NumPy 2.3.5 are used by the full verification. No physical device or external service is contacted by the numerical suites. All trace/diamond norms in the manuscript are unhalved; probabilities retain their factor one half.

From an extracted standalone journal archive, run:

```
python journal_verify.py
```

From the complete native archive in a Git checkout at its native-source commit, run:

```
python build_revision.py --isolated
```

This runs all 37 regression suites normally and with `python -O`, compares their JSON results, builds four linked documents, reconstructs the native archive in a separate temporary directory, and rebuilds the two-document journal archive. The additional Section 21 suite distinguishes exact symbolic/rational checks, numerical sanity cases and negative controls. Finite replay is not a substitute for the written proof.

The fixed-spectrum evaluator accepts exact rational eigenvalues and a rational deformation parameter:

```
python equal_prior_initial.py examples/equal-prior-initial.json --bits 80
```

Its rational bounds enclose the algebraic value proved for old receiver dimension two. It does not verify that an experimental acquisition has the claimed Gram, eigenbasis, preparation cut or error norm.

The submitted local source and PDF identities appear in `evidence/BUILD_RECEIPT.json`. Read emitted diagnostics literally. The local final-object verification is not a GitHub Actions check. No v95 remote push was performed by this session. A remote-backed publication must create its own native commit and rebuild at that commit rather than relabel these local receipts.
