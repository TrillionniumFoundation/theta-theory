# Reproducing the submitted article and supplement

This package contains the Revision 91 primary and its linked supplement, their active source dependencies, and a read-only verifier. The research repository separately preserves all historical derivations, responses, exact regression programs, native-source identities and the complete research edition.

With Python, PyMuPDF 1.26.7 and a TeX distribution providing amsmath, amsthm, amssymb, hyperref, xr-hyper, geometry, microtype and Latin Modern, run:

```sh
python journal_verify.py
```

The verifier checks the archive input hashes, reconstructs both documents in a temporary directory and compares their page identities with the supplied manifest. The publication build used the tool versions recorded in its external build receipt. Cross-platform PDF byte identity is not asserted; the package verifier specifies the page/text/render comparison it performs.

The independent structural article and complete research edition are not additional premises of the submitted quantitative paper. Reconstruction is evidence of object identity and execution, not proof of mathematical correctness or originality.
