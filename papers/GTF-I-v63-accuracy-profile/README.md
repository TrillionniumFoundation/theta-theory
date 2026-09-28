# General Theta Foundations I — Revision 63

**Stochastic Widths at Exponential Accuracy and Spectral Entropy on Spheres**

Companion: **Finite Physical Actions and a Strong Converse for Repeatable Observations**.

The current mathematical addition is `sections/30-exponential-accuracy.tex`. It is loaded by `quantitative.tex` and by the complete archival `main.tex`. `structural.tex` remains an independent proof-complete article. No predecessor PDF is needed to read either focused paper.

## Main statements

For a symmetric 2r-command orthogonal action on S^p with full spherical Koopman norm at most 2 sqrt(2r-1)/(2r), the pure spherical interface satisfies a uniform crossover bound

    exp(-C sqrt(N log(N+2))) min((2r-1)^N, ((N+1)/e)^(p/2))
      <= W_(N,e)
      <= C' min((2r-1)^N, ((N+1)/e)^(p/2)).

Errors lie below a fixed e0<1; e=0 is included with 1/0=infinity. The same lower tradeoff holds with N replaced by the number of positive cuts of width at most k, while all other widths are unrestricted.

For the fixed rational six-command LPS Bloch experiment with legal D2 outputs and Frobenius error epsilon_N, log(1/epsilon_N)/N -> a implies

    log W_(N,epsilon_N)/N -> min(a, log 5).

The exact profile 5^t and its robust interval epsilon<=25^(-N)/16 are inherited from v62. The Theta(N/epsilon_N) theorem for subexponential inverse accuracy is also retained. The new result determines the full exponential rate, not a uniform multiplicative equivalent at the transition, an optimal subexponential factor, or the exact beginning of saturation.

## Reproduction

Run `python build.py --check-isolated` with Python, SymPy, PyMuPDF and LaTeX. The build executes new and inherited checks in ordinary/optimized modes, reconstructs the compiler examples, typesets all preserved documents, and independently rebuilds a native-only source archive. `evidence/BUILD_RECEIPT.json` records actual results and exact source identity; this README is not a receipt.

`evidence/JOURNAL_PACKAGE.zip` is a smaller independently rebuildable package containing the two focused papers, only their active TeX inputs, the response and a verifier. `evidence/REFEREE_PACKAGE.zip` additionally contains the complete archival edition and provenance.

`accuracy_profile.py` emits exact-rational sufficient exclusion witnesses. Example:

    python accuracy_profile.py --horizon 100 --width 10 --error 1/931322574615478515625 --block-length 10 --terms 8

An `excluded` result is a rigorous arithmetic consequence of the stated imported LPS hypothesis and the written block-budget theorem. An inconclusive result is not a feasible realization. Finite word, polynomial and interval tests do not prove the full spectral theorem or universal mathematics.

## Pinned ancestry

Base v62 final head: `3be9f51ed1c33ed9262339a8d3999dab3400f33f`; candidate `a27a156c0090881100e4e986eb1a398f475a04c1`; native source `2483a41906387f7718020991f0262a07357cbf12`.

The latest located external report remains r40 at `4a99da0aab823418d95631d5dbbd8e9b8178994d`, with companion audit `02c642d3c08774d2dbaee939ffb2eee57b545f92`, both reviewing v61. No v62-specific report was located in the initial survey. Revision 62's improvements are inherited, not presented as new v63 results. All 410 predecessor native files are preserved byte-for-byte.

Work branch: `revision/general-theta-foundations-i-v63-accuracy-profile-2026-09-28`.
Referee branch: `revision/general-theta-foundations-i-v63-referee-ready-2026-09-28`.

The clock, arbitrary real tables, construction, lookup, arithmetic and exact sampling are uncharged in the primary label-width invariant. The new exponential-accuracy bound is not a polynomial-runtime claim in encoded precision. Causal results retain repeatable fresh-probe hypotheses. Independent priority, signatures, journal acceptance and A/B/C/D analytic closure are not certified by this package.
