# General Theta Foundations I — Revision 64

## Manuscripts

**Quantitative:** *Spectral Entropy, Stochastic Widths, and Uniform Streaming Space* — `paper.pdf`, source `quantitative.tex`.

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* — `STRUCTURAL_PAPER.pdf`, source `structural.tex`.

**Complete research edition:** `COMPLETE_REVISION.pdf`, source `main.tex`. This includes the entire previous active mathematical development and the new theorem, rather than replacing old results with a summary.

## New theorem

For the fixed six rational LPS Bloch rotations, with legal numerical density-matrix outputs, a single deterministic one-pass program achieves Frobenius error `2^(-L)` using, for `N >= 2` and `L >= 2`,

    O(min(N, L + log(N+1))) writable bits.

Every randomized one-pass simulator satisfying even the weaker mean-output error condition needs the same space order. The lower theorem permits unlimited internal computation and arbitrary horizon-dependent stochastic updates. The upper theorem counts integer registers, temporary storage, parameter parsing, addresses, a validation counter and binary numerical output. It uses no real advice table, external command-time clock, exact sampler or quantum state preparation.

The main new proof is `sections/31-uniform-streaming.tex`, including the finite bit–accuracy obstruction, boundary reduction, directed-rounding lemma, complete algorithm and exact-precision fallback. The full-action LPS gap remains an imported premise for the lower bound. The elementary rounding and configuration techniques are not claimed as new general principles.

A further corollary proves the same space order for any fixed rational orthogonal alphabet with a rational unit seed, a full action gap and an all-direction cap law, when the legal outputs are the Euclidean unit ball. It does not claim that coordinate truncation preserves an arbitrary orbit hull or higher-dimensional density-matrix cone.

The prior v62 return-free occupation and causal strong converse, and v63 exponential accuracy crossover, remain in the proof graphs and retain their own significance and limitations. The new bit-space equivalence does not claim optimal leading constants or eliminate the remaining multiplicative gap in label width.

## Executable reference

The standard-library-only program reads two decimal parameter lines and then a one-pass stream of six command letters:

    printf '8\n2\nxXyYzZxx\n' | python streaming.py

Here `x,X,y,Y,z,Z` denote `A1,A1*,A2,A2*,A3,A3*`. Identity and unknown commands are rejected. A common-denominator density matrix is returned with signed hexadecimal numerators. Huge requested precision values are scanned with saturation at N. The interpreter's allocator is not claimed to be an optimal bit machine; the written theorem accounts for the program's integer recurrence in the binary bit model.

Run `python check_streaming.py` for exact-rational finite regression. The retained `inherited_check_v63.py` and `accuracy_profile.py` test the earlier sufficient-exclusion arithmetic. `qubit_compiler.py` remains the separate sparse stochastic-table and causal compiler; it is not silently substituted for the new integer streamer.

## Reproduction and review

Run `python build_revision.py --isolated` with Python, PyMuPDF, SymPy, pdflatex and the usual AMS/Latin Modern LaTeX packages. It compiles all three manuscripts, compares normal and optimized test output, checks preserved proof labels and source hashes, and reconstructs from the revision's native archive in an empty directory. Actual results are in `evidence/BUILD_RECEIPT.json`, not inferred from this README.

`evidence/JOURNAL_PACKAGE.zip` contains the two focused manuscripts, their active TeX inputs, the response, a short manifest and a native verifier. `evidence/RESEARCH_PACKAGE.zip` also includes the complete manuscript and executable tools. The repository retains all historical material at its existing paths. The exact-final-head workflow has contents-read permission only and publishes an external CI artifact.

Read `RESPONSE_TO_REFEREE.md` for the ten required revisions and twenty-four detailed comments; `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md` and `HISTORY_AND_PIPELINE_AUDIT.md` separate new mathematics, inherited results, primary literature and historical dependencies. No author-side document is described as an independent expert endorsement.

## Branches and ancestry

Work branch: `revision/general-theta-foundations-i-v64-uniform-streaming-2026-09-28`.

Referee branch: `revision/general-theta-foundations-i-v64-referee-ready-2026-09-28` (created at the completed publication head).

Base: v63 publication `f5c1e5d6eacecc1597fba18697a715f8e7844e09`. Controlling v61/r40 report: `4a99da0aab823418d95631d5dbbd8e9b8178994d`; companion audit: `02c642d3c08774d2dbaee939ffb2eee57b545f92`. The predecessor native archive's Git blob is `d8b3e752460b1b2f8a453b99926bbf722b21d08a`.
