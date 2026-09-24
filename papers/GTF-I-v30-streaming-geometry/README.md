# General Theta Foundations I — Revision 30

**Positive Realization and Exact Streaming Memory**  
Qian Qi · 24 September 2026

Controlling r14 report: `c039e5bc8bc8b30fca92246bc1458f66214522e1`. Reviewed v29 publication: `b0bd13753456c15815b174db1106e2ce6ee7433b`. Work branch: `revision/general-theta-foundations-i-v30-streaming-geometry-2026-09-24`. The referee-ready branch is created only after successful source-bound publication.

[Focused English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r14](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Unaltered v29 supporting article](supporting-results.pdf) · [Complete mathematical manuscript](complete-manuscript.pdf) · [Complete preserved development](complete-development.pdf) · [Source archive](evidence/SUBMISSION_SOURCES.zip)

## Main results

The support-component rank profile is simultaneously attainable **if and only if** each component admits a rank-sized enclosing simplex in its causal affine slice and all chosen generators satisfy the common positive shift equations. Internal generators need not be residuals and the residual hulls need not be simplices. This is a criterion for simultaneous rank saturation, not an algorithm for unrestricted minimum positive rank. For fully listed algebraic data its existential polynomial constraints are decidable.

For every fixed signal `0 < eta < 1`, define `I(eta)=1-h2((1+eta)/2)`. The binary-query channel has

```
n*I(eta) <= log2 K_n <= n*I(eta)+O_eta(log(n+1)),
n*I(eta) <= log2 W_n^ad <= log2 W_n^fo
          <= n*I(eta)+O_eta(sqrt(n*log(n+1))).
```

The first quantity is checkpoint complexity. The other two price the whole adaptive-acquisition or fixed-order streaming run. Every conditional output probability is synthesized exactly. The upper proof includes the entire raw block buffer and all codeword labels. The entropy exponent is classical in random-access coding and is credited to Ambainis–Nayak–Ta-Shma–Vazirani; it is **not** presented as a new information exponent. The exact channel and charged streaming conclusions are stated separately.

At uniform row-TV tolerance epsilon, the three asymptotic rates become `I(max(eta-2*epsilon,0))`. This concerns one query after installation. Jointly independent answers to all n queries are a different channel and have rank `2^n` even at arbitrarily small nonzero signal.

An explicit reservoir encoder achieves the exact acquisition profile `t+1`, and peak `n+1`, throughout `0 < eta <= 1/(2*n-1)`. A necessary simplex bound is `eta <= 1/n`; whenever a Hadamard matrix of order n+1 exists, a charged online encoder attains that threshold exactly. This includes every `n=2^k-1`. No unproved general Hadamard existence assertion is used.

The probabilistic-residual comparison includes an explicit finite stochastic language with at least `2^n` residual-automaton states and a rational positive realization with at most `(n+1)*(n+2)/2+n*(n+1)+1` states, including the clock and query buffer. A formal proposition separates ordinary rank, nonnegative rank, affine-restricted generators, residual-state size and queried block normalization.

## Focus and preservation

The journal-facing `paper.pdf` contains the new theorem spine and its proofs, not the accumulated v29 appendices. No old result is deleted: `supporting-results.pdf` is the unaltered v29 article, and the complete mathematical and development volumes append the unaltered v29 cumulative volumes after the entire current article and a divider. Original repository paths are unchanged. Preservation is not counted as theorem novelty.

## Reproduction

Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7, and TeX packages supplying AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools, needspace and hyperref suffice. From the repository root:

```sh
python papers/GTF-I-v30-streaming-geometry/verify.py
python -O papers/GTF-I-v30-streaming-geometry/verify.py
python papers/GTF-I-v30-streaming-geometry/build.py
```

The source archive uses sibling package directories; after extraction, run `python GTF-I-v30-streaming-geometry/build.py`. It includes the exact prior verification inputs and supporting PDFs needed by this build, not standalone font files. The build executes the v24–v30 regressions in normal and optimized Python, tests intentionally wrong v30 controls in both modes, compiles three times, and checks all preserved predecessor page texts and representative raster pages. Read the actual receipt for executed results.

The workflow publishes native sources first, then builds that native commit and publishes the artifacts without force to the work and referee-ready branches. The trigger commit, native source commit and final artifact commit are distinct provenance fields.

## Precise boundaries

No exact finite integer phase diagram for every n and eta, sharp second-order streaming cost, generic controlled-policy optimization, or fully adaptive collision-validation optimum is claimed. Known exact atomic rows are distinct from finite-bit or acquired-calibration implementations. Independent A2/B4/C2 and the historical eleven-paper gates are preserved. The 2002 PRFA publisher record/abstract and the full cited 2006 residual treatment were inspected; an exhaustive original-chapter/Heller/Norberg proof-level priority clearance is not claimed. See `LITERATURE_AUDIT.md` for source access and theorem distinctions.
