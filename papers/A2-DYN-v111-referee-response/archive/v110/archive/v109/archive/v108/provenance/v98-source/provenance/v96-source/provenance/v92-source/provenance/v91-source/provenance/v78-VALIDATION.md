# Exact-source qualification — revision 78

`bash build.sh` requires an exact Git checkout; `bash build.sh --local` is restricted to non-CI archive checks. Neither mode skips the complete supplement.

The source verifier pins v77 paper tree `dcdbbd9d49cc707bdcf6a1d41066ac26cdfd39b6` and the v76 controlling review blob `6857e4851ff12b7d0828f4eb661152e131fba091`. It checks byte preservation of 176 inherited cores, every inherited Python source, appendix, bibliography and provenance file, and every v77 top-level snapshot. It verifies that all inherited claim flags remain unchanged, especially the unproved raw endpoint.

Finite fixtures check the optical inverse and forcing bounds, finite-product variation, the target-Jacobian split, polynomial current coefficients, coincident-decision jumps and retention of nonzero arithmetic peak factors. Explicit exceptions, rather than Python assertions, remain active under optimization. All recent and inherited diagnostic fixtures run in normal and optimized modes with matching output.

Native TeX must stabilize its references with no LaTeX/package warning, overfull box, undefined reference or missing character. Recorder coverage must contain all 179 core files: six in the article and 176 in the supplement, with the three retained journal cores appearing in both. PDF word geometry is checked page by page; article pages and selected supplement pages are rendered.

Workflow: `.github/workflows/a2-dyn-v78-qualification.yml`. Qualification is attached to actual completed runs at the author SHA. A new workflow file or passing v77 run does not itself qualify v78. Builds and finite fixtures do not certify continuum proofs, settle the geometric estimate or stand in for independent specialist review.
