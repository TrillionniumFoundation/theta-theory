# A2 v89 build and validation receipt

## Exact source scope

The native local build used the complete source from manuscript commit `3de72a935ce643ea22e522ba7a6c233331d76247`: `rigidity_v89.tex` and all twelve `article/v89/*.tex` modules. The files were assembled from the committed text and Git blob identities, not from a substitute abbreviated manuscript. All thirteen source digests are in `SOURCE_HASHES.tsv`. The subsequent response-package commit leaves those sources unchanged.

This environment did not contain a full clone of the repository. Therefore no local full-repository preservation run is claimed. The separate live GitHub comparison is recorded in `PRESERVATION_AND_SUBMISSION_BOUNDARY.md`.

## Native compilation — completed

Command, run from the manuscript directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v89.tex
```

Environment: pdfTeX `3.141592653-2.6-1.40.26` from TeX Live `2025/dev/Debian`; latexmk `4.86`. The completed PDF records creation time `2026-09-19T06:38:23Z`. The build command exited successfully and latexmk reported all targets up to date after resolving the cross-references.

| Check | Observed result |
| --- | --- |
| PDF | 25 pages; 508788 bytes; US Letter |
| Title/author | Projective polynomial observations: observable conditioning and singular inference / Qian Qi |
| Undefined references or citations | 0 in final log |
| Duplicate labels | 0 in final log |
| Overfull boxes | 0 in final log |
| Underfull boxes | 0 in final log |
| Other LaTeX warnings/errors | 0 in final log |
| Render | All 25 pages rendered at 120 dpi; contact sheets reviewed, with detailed inspection of dense formulas and references |

Local PDF SHA-256:
`6de1df65d37e6f5e8690202be613a051836a48305582af3bd836d0f50cacdcbb`

Final native log SHA-256:
`0394b4763ff1e50c057bb017f1c5bc757e20a16f0ff331f2b9b66c6e3791dc30`

The PDF and native log are supplied with the local handoff archive. The repository contains the complete TeX sources and this receipt; this document does not claim that the binary PDF has been committed to Git. Rebuilding can change PDF bytes through timestamps or TeX versions without changing the source.

## New local mathematical diagnostics — completed, limited scope

Ten groups passed with Python `3.13.5`, NumPy `2.3.5`, SymPy `1.14.0`. `LOCAL_VERIFICATION_RESULTS.json` records the actual outputs and all twelve module hashes. They cover exact gcd kernels, the full-span d+2 count, the low-complexity 2d obstruction, the general rational module, observable joint inverses and orthogonal invariance, the normalization gauge, positive degree-d product families with fixed marginals, real-rooted moving multiplicity alternatives, a maximizing local metric direction at a cross-component collision, and the source control-character scan.

These are finite symbolic and numerical regression checks. They are not a formal proof checker, an independent referee report, or a journal-level originality assessment.

The new diagnostic script's upload was blocked by the connector's safety determination. It was not uploaded through another endpoint and is not claimed to exist in this branch. Its local SHA-256 is `7e1657b833851ad0f5a0b65199ee0f473bbb3636f84394be27d7d23dbba63649`. The JSON is a result record, not a claim that readers can execute that unavailable script from this branch. The independently readable mathematical proofs are in the principal article.

## GitHub Actions — not credited as a completed build

The added read-only workflow is `.github/workflows/a2-v89-manuscript.yml`. It checks additions-only preservation, runs the inherited `verification/verify_v88.py`, compiles the entire v89 article, and uploads build artifacts if executed. Its inherited verifier's `--output` interface was read back from the repository.

Initial source-commit runs:

- push: `35426660101`;
- pull request: `35426670472`, job `105853726721`.

At the validation readback on 19 September 2026, the PR job was `queued`, with no conclusion and no executed steps. No successful remote build or new-suite Actions run is asserted. Subsequent runs triggered by the documentation commit have their own heads and must be checked separately. Workflow existence, queued status and local compilation are three different facts.

## Review boundary

The source is submitted for a further independent referee review. The checks above establish source identity, a completed native typesetting build and specified finite diagnostics. They do not establish mathematical correctness of every proof or exhaustive priority relative to the literature.
