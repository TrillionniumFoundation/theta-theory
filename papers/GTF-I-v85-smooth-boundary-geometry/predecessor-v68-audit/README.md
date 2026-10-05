# General Theta Foundations I — Revision 68

**Quantitative article:** *Joint Instrument Coding Laws and Boundary-Uniform Rational Realization* (`quantitative.tex`, `paper.pdf`). The standalone article contains only the coding proof graph; its Choi and exact-validation prerequisites are proved within it.

**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

**Complete research edition:** `main.tex`, `COMPLETE_REVISION.pdf`. The complete previous proof graph, including all 394 prior active labels, is retained. All 115 v67 native files remain unchanged at their existing repository paths.

## New results

For m-outcome instruments M_d -> M_n on a fixed positive Choi-margin body, put s=d^2(mn^2-1). The optimal reusable legal-description length is

    (s/2) log2 N + s log2(1/delta) + O_(d,n,m,a)(1),

uniformly for N>=1 and 0<delta<=1/32. The remainder is independent of both N and delta. The metric is the unhalved final joint-state trace distance against one common causal quantum tester, with quantum memory, reference entanglement, feedback and bounded public stopping. The same memoryless instrument is reused. This sharpens the inherited v67 fixed-error theorem by a local binary-testing estimate.

For input-erasing, outcome-retaining preparation instruments, sigma_y>=0 and sum tr sigma_y=1, prescribe public rank bounds r_y. With

    v = sum_y r_y(2n-r_y) - 1,

the corresponding optimal length is

    (v/2) log2 N + v log2(1/delta) + O_(m,n,ranks)(1)

on the same joint parameter range, with no positive-eigenvalue margin. The full family has v=mn^2-1; pure prepared states have v=2n-2; classical m-outcome distributions have v=m-1. The singleton v=0 has zero description length. Matching lower bounds apply even when decoded preparation centres have ranks outside the promised target family.

The new rational factor codec preserves every zero outcome and never increases any block rank. It computes signed coordinate ratios through rational Schur residuals and integer square roots without representing the irrational Cholesky factors. The resulting PSD matrices have Gaussian-integer numerators and exact total trace one. A program-state identity reduces all adaptive tests of preparation instruments exactly to product-state trace distance.

These are reusable **description** laws, not mutable-workspace lower bounds, unknown-channel learning bounds or physical classical simulation. The general interior result still requires a fixed Choi margin; the boundary result is for preparation instruments, not arbitrary disturbing instruments. Constants are not optimized uniformly in growing dimensions. Inherited spectral, crossover and repeatable-probe results retain their original assumptions and complete proofs.

## Execution

    python preparation_codec.py adaptive --input inputs/preparation-boundary.json --horizon 1000 --error 1/1000 --ranks '[2,1,0]' > code.json
    python preparation_codec.py decode --input code.json
    python preparation_codec.py verify --input inputs/preparation-boundary.json --certificate code.json
    python check_preparation.py

The supplied input has input dimension 2, output dimension 3, three outcomes, ranks 2/1/0, and a small positive eigenvalue. The hexadecimal factor payload is not the JSON byte length; headers, the expanded Choi matrices and preprocessing memory are separate. `PREPARATION_CODEC_SCHEMA.md` defines the encoded data and certificate semantics. The inherited `instrument_codec.py` supplies the general positive-body construction.

## Reproduction and review

    python build_revision.py --isolated
    python build_revision.py --verify-published

The builder executes six exact suites in ordinary and optimized Python, typesets three manuscripts, checks preservation and every new theorem, and rebuilds a native archive in an empty directory. It compares all page text and rasters. The minimal `evidence/JOURNAL_PACKAGE.zip` contains the two focused proof graphs, PDFs, response and independent native verifier, without historical PDF dependencies. `evidence/RESEARCH_PACKAGE.zip` also contains the complete edition, programs and full revision records. Actual results are in generated receipts, not inferred from this README.

Work branch: `revision/general-theta-foundations-i-v68-boundary-uniform-coding-2026-10-03`.

Referee branch: `revision/general-theta-foundations-i-v68-referee-ready-2026-10-03`, created at the verified final candidate.

Base: v67 qualified publication `98a4b12126502ea41c620b58bad4b9aa30f9c72c`; v67 source `429a7cbe79c032386da934eb824d4ba31416ec44`; builder run `37107995113`. The latest controlling external report and audit are v67/r44, respectively `68c69a4a2e8b4e3b11c43a181806ab578584b719` and `7a9586cd8cf7995152fbbf501f3e47da4aa89900`. They review this exact v67 base, not v68. They appeared after the initial r43 survey and are answered in all 14 required and 24 detailed items. The v68 remote anchor was committed before substantive assembly. No predecessor branch is overwritten.

The final CI separately checks out and reconstructs the reviewed v67 publication without changing it. Its attestation identifies that checkout, not a fictitious v67 workflow trigger. The general-journal research objective remains unchanged. Independent expert priority, cryptographic author signature, proof-assistant verification, journal acceptance and A/B/C/D analytic closure are not certified by a source build.
