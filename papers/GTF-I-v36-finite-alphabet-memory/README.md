# General Theta Foundations I — Revision 36

**Finite Alphabets, Spectral Gaps, and Hidden Memory**  
Qian Qi · 25 September 2026

Controlling r20 review: `6da551c5b804b683240d5f5631e1c4f5689e21bd`. Reviewed v35 publication: `aabc0731a0c913f7b9e75e6efc08f7af665bdf23`; its native source: `0ae43a2180d07bda18384697a33da48d3fc1562a`.

Work branch: `revision/general-theta-foundations-i-v36-finite-alphabet-memory-2026-09-25`. A separate referee-ready branch is published after the source-bound build. Only new revision paths are added; old manuscripts, reports, other paper branches and `main` are not changed.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r20](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Small referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## Theorem spine

The packet contraction is stated for a complete fresh word W, its group product g(W), and an arbitrary endpoint kernel T_W. Equal-product words may have different kernels. Independence is imposed on the whole word and the earlier process, not merely on the product.

For a fixed finite orthogonal alphabet with an absolute L2 gap on the sphere, at fixed signal and small uniform row-TV error,

```
c (N/log(N+1))^((d-1)/2) <= W_(N,epsilon) <= W_(N,0) <= C N^((d-1)/2).
```

The logarithmic gap is retained. Mixing uses B_k=O(log(k+1)) ordinary input symbols, not a free Haar command. The converse allows arbitrary hidden states and arbitrary cut-dependent stochastic matrices. The exact upper uses a rational stereographic sphere net and sparse common command rows. Thus the polynomial exponent is (d-1)/2, but a matched order up to constants is not claimed for this class.

Five explicit rational SO(3) matrices meet the hypothesis through Bourgain–Gamburd's spectral-gap theorem, with density and algebraicity checked in the article. Their width is between c N/log(N+1) and C N, while each separate positive minimum is four. Their numerical probabilities have an exact single-qubit implementation. Chen–Wu's current strict-cutpoint result supplies a five-state *language* simulator, not a fixed-accuracy probability simulator; these objectives are distinguished directly.

A second fixed finite noncommuting class acts by permutations, conjugations and resonant rotations of planar modes. Its width is exactly Theta(N^(1/3)) in asymptotic order, for fixed badly approximable angle and fixed error below rho/2. An explicit at-most-five-generator class acts irreducibly and has no continuous one-dimensional character seeing its irrational rotations. Its lower bound uses a cyclic sublanguage; its upper uses the full monomial structure. This is not a classification of every finite noncommuting gate set.

A sparse-row dyadic compiler uses O(K log(N/delta)) labels with finite fair coins, including the input latch, old label, branch node and bit position. It is self-paced and nonuniform, and gives fixed-error implementation rather than exact irrational sampling. The leading label-bit coefficients are 1/3 and (d-1)/2 in the two respective classes.

## Reproduction

Python 3.11+, SymPy 1.14.0, mpmath, PyMuPDF 1.26.7, and a TeX installation providing AMS, Latin Modern, geometry, microtype, booktabs, mathtools, needspace and hyperref suffice.

```sh
python papers/GTF-I-v36-finite-alphabet-memory/verify.py
python -O papers/GTF-I-v36-finite-alphabet-memory/verify.py
python papers/GTF-I-v36-finite-alphabet-memory/build.py --core-only
python papers/GTF-I-v36-finite-alphabet-memory/build.py
```

The core archive extracts to one package. From its parent run `python GTF-I-v36-finite-alphabet-memory/build.py --core-only`. The full archive additionally includes frozen inputs for historical regression and preservation. No standalone font files are distributed.

The workflow publishes native source first, binds the build to that commit, independently rebuilds the small core, and then publishes PDFs and receipts without force. Consult the actual receipt for executed status. Finite checks include rational gates, Bloch identities, word collisions, explicit rational short-horizon rows, monomial numerical rows, interval packing and dyadic sampling. They do not establish an infinite-dimensional spectral gap or any asymptotic theorem.

## Preservation and boundaries

[Unchanged v35 article](supporting-results.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full rebuilding archive](evidence/SUBMISSION_SOURCES.zip)

All previous proofs remain at unchanged repository paths and in unchanged appended volumes. The v35 general packet implication is supplied with the corrected full-word proof here; the published predecessor is not silently edited. The old compact-input theorem remains separate and is not counted as a finite-alphabet theorem.

The new spectral-gap class has a logarithmic order gap; no numerical gap constant or all-irrational classification is claimed. The matched monomial class has its stated structural hypothesis. Exact atomic rows, finite-coin fixed-error synthesis, strict-cutpoint languages and uniform numerical probabilities are different tasks. Independent historical A2/B4/C2 gates and fully adaptive collision scheduling are not declared solved. Source binding and successful tests are reproducibility evidence, not independent proof, exhaustive priority clearance or a journal decision.
