# General Theta Foundations I — Revision 73

## Manuscripts

**Noise-Uniform Readout Geometry and Reusable Instrument Descriptions**: `quantitative.tex` → `paper.pdf`.

**Finite Physical Actions and a Strong Converse for Repeatable Observations**: inherited structural companion, `structural.tex` → `STRUCTURAL_PAPER.pdf`.

`main.tex` → `COMPLETE_REVISION.pdf` contains the complete research edition. All 482 previously active mathematical labels and all 197 predecessor native files are preserved; the predecessor paths are not modified. Actual counts and source identity are verified by the build and exact-head receipts.

## Principal new result

For labelled equatorial qubit readouts with public visibility lambda in [0,1], define

    K = lambda * sqrt(N * min(N, 1/(1-lambda^2))),
    K(N,1)=N, K(N,0)=0.

Theorem `thm:noisycoding73` proves, for circular angle distance h,

    (1/64) min(1,K h) <= d_N <= min(2,K h).

It follows that the optimal fixed-length reusable description is

    log2(1+K/delta)+O(1),  N>=1, 0<delta<=2^-10,

with absolute constants uniform in N, lambda and delta. Lower centres may be arbitrary legal memoryless instruments. Upper centres have rational circle coordinates; their effects are rational when the public visibility is rational. Completely erased readout has exactly zero optimal payload. The upper bound controls references, quantum memory, adaptive feedback and bounded public stopping. The lower tester uses explicit finite GHZ blocks and parity/majority statistics.

If 1-lambda_N^2=N^(-alpha+o(1)) approaches zero, the fixed-small-error horizon coefficient is (1+min(alpha,1))/2. This noise-dependent approach to the projective boundary is not obtained by holding an interior positive margin fixed. The familiar metrological noise crossover and classical simulation methods are credited; a new priority claim is not attached to those principles.

With labelled conditional states of ranks at most r_+,r_- in dimension n, let V=sum_y[r_y(2n-r_y)-1]. Corollary `cor:noisypreparation73` adds (V/2)log2 N+V log2(1/delta) to the readout length, at fixed dimension/ranks and sufficiently small error. Rational upper codes preserve the conditional ranks. The public visibility is not learned or encoded as a varying target coordinate.

## Exact rational interface

    python noisy_readout_codec.py encode --input inputs/noisy-readout.json --horizon 257 --error 1/1024 > code.json
    python noisy_readout_codec.py decode --input code.json > instrument.json
    python noisy_readout_codec.py verify --input inputs/noisy-readout.json --certificate code.json

For the conditional qutrit example use `inputs/noisy-conditional.json` and add `--ranks '[1,3]'` at encoding. The output uses input-first unnormalized Choi matrices. Signed chart digits are packed into a fixed-length integer index. Canonical JSON is a transport envelope, not the charged payload. Integer square-root comparisons choose the grid without floating-point decisions. Bare decoding establishes a legal codeword, not its relationship to an unknown target; verification re-encodes the entire supplied target and compares the canonical object.

`python check_noisy_readout.py` executes finite exact regression, including both visibility endpoints, huge horizons, tiny rational errors, GHZ tensor probabilities, Bernoulli products, full small chart alphabets, singular conditional outputs, CLI replay and malformed certificates. It does not prove continuum packing or all adaptive testers. All nine inherited suites execute unchanged in ordinary and optimized modes.

## Reproduction

Run `python build_revision.py --isolated`. Required: Python, PyMuPDF, SymPy, pdflatex and the AMS/Latin Modern packages. Every unresolved reference/citation and overfull/underfull box fails the build. All three native manuscripts are reconstructed in an empty directory, and every page's text/raster is compared. `evidence/BUILD_RECEIPT.json` reports executed results, not assertions inferred from this README.

`evidence/JOURNAL_PACKAGE.zip` contains the two focused PDFs, active TeX dependencies, response and independent verifier. `evidence/RESEARCH_PACKAGE.zip` includes the complete edition and exact code. Previous PDFs are not forward proof dependencies. The final-head workflow has contents-read permission only and writes an attestation outside the reviewed tree.

## Ancestry and review

Base v72: `12296ed387dbc197ff7cb854d3a78d0bf964960e`; publication `b3a5f6ecb34826eaca9feba40ccf77d003fa02f2`; native `f9ced3761b5c0497dfe5ec363126a393b6641e6e`. Source run `37139560991` and final run `37139862122` succeeded. The downloaded v72 qualification artifact is `11279179574`.

The latest located external report remains v71/r46 `b78c1dddd41de645edf207bc415406b3fc1b5e83`; companion audit `43e6713de2aa65f65e649df7cd90e2a95fc83a06`. It does not independently review v72 or v73. The v72 varying observable readout, rational flag atlas and ambient seizing results are inherited, not relabelled as this revision's discoveries. Their complete proofs are retained.

The new remote work anchor `3f1f8eb18f88bbc9069662cdb4d5fe6b05795024` was pushed before the substantive revision. Work branch: `revision/general-theta-foundations-i-v73-noisy-readout-crossover-2026-10-04`. Referee alias, after exact-head verification: `revision/general-theta-foundations-i-v73-referee-ready-2026-10-04`.

The response maps all sixteen required revisions and twenty-six detailed comments without changing the general-journal objective. The new theorem is noise-uniform in an explicit boundary family, not a general instrument tangent-cone classification or a learning/workspace/hardware theorem. Independent priority, authorship signature and journal acceptance are not certified. All analytic A/B/C/D aggregate flags remain false.
