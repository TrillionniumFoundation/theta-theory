# General Theta Foundations I — Revision 32

**Causal Width Beyond Cutwise Positive Rank**  
Qian Qi · 25 September 2026

Controlling r16 review: `0e69fdcfc11067a7de9a6122fc603f6a5e2253d8`. Reviewed v31 publication: `90dc2c8f0c75e2cfbb95cc61b247ce4d5e216eb9`.

Work branch: `revision/general-theta-foundations-i-v32-causal-width-2026-09-25`. A separate `revision/general-theta-foundations-i-v32-referee-ready-2026-09-25` is published only after the executed build succeeds. Older manuscripts, reports and pipeline paths are unchanged.

[Canonical article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r16](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Small referee package](evidence/REFEREE_PACKAGE.zip) · [Core sources](evidence/CORE_SOURCES.zip) · [Full reproduction sources](evidence/SUBMISSION_SOURCES.zip)

## Principal result

A fixed-alphabet binary-response family has separate positive minimum exactly three at every internal cut, with all response probabilities uniformly between `(1-sqrt(2)/10)/2` and `(1+sqrt(2)/10)/2`, yet its minimum simultaneous clocked width tends to infinity. For the golden-angle rotation:

```
max(3, log2(N/24000000)/6) <= W_N
                          <= min(3*(N+1),4*ceil(sqrt(N+1))).
sum_(t<N) 2^(-6*K_t) <= 24000000 for every feasible profile.
```

The lower proof permits arbitrary hidden continuations and unrelated rows at every epoch. It projects the *reachable affine section* of the hidden probability simplex, rather than illegally mapping every unit hidden state into the observable plane. A geometric volume expansion must be paid at every step. The upper construction gives explicit normalized transition rows and exactly realizes every conditional probability.

The rational rotation `[[3,-4],[4,3]]/5` gives the same qualitative unbounded separation with rational channel data, effective algebraic excluded-horizon certificates, and rational `3*(N+1)`-state realizations. No logarithmic constant is transferred to this angle without proof.

A verifiable-tag composition theorem makes entire feasible profile sets add as Minkowski sums. Its m-fold two-cut application has exact region `K1,K2>=3m`, `K1+K2>=7m`, and peak `ceil(7m/2)`. That tagged example has output zeros; the rotation example supplies full support independently.

## Classical boundary and model

Irrational-rotation stationary positive-realization obstructions, invariant cones, accessible quotients, and weighted reservoir sampling are explicitly credited. The new comparison is finite-horizon and allows time-varying stochastic rows, while keeping every separate positive minimum equal to three. The main statement does not rely on one repeated matrix's peripheral spectrum.

These are exact atomic-row, clocked transducer counts, not succinct-program or arithmetic complexity. The row table is known program data. Exact rational fair-bit implementation has separately charged sampling workspace. The golden-angle coefficients are specified computable reals. The bounds are not sharp; general adaptive experimental-policy optimization and the fully adaptive collision-validation optimum are not claimed.

## Reproduction

Use Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7, and TeX supplying AMS, Latin Modern, geometry, microtype, booktabs, mathtools, needspace and hyperref.

```sh
python papers/GTF-I-v32-causal-width/verify.py
python -O papers/GTF-I-v32-causal-width/verify.py
python papers/GTF-I-v32-causal-width/build.py
```

For the small core archive, extract and run `python GTF-I-v32-causal-width/build.py --core-only`. This compiles and verifies the focused paper without requiring archival PDFs. The full source archive uses sibling package directories and contains the frozen predecessor files required for the complete build; after extraction run `python GTF-I-v32-causal-width/build.py`. No font files are included.

The build binds source hashes, verifies ordinary/optimized checks and explicit invalid controls, compiles three times, rejects unresolved references and overfull boxes, and records exact theorem pages. In the complete build it replays v24–v31 checks and verifies every appended predecessor page's text plus representative raster samples. Read the executed receipt rather than assuming those commands succeeded.

## Preserved mathematics

[Unchanged v31 article](supporting-results.pdf) · [Complete mathematical manuscript](complete-manuscript.pdf) · [Complete historical development](complete-development.pdf)

These are optional archival artifacts, not part of the small referee package or proof obligations for the new article. All v31 native sources and earlier repository paths remain intact. The inherited two-cut proof is restated in Appendix A and labeled as inherited. Historical A2/B4/C2 analytic gates are not inferred from these finite-state results.
