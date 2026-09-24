# General Theta Foundations I — Revision 31

**Compatibility of Positive Memory and Online Simplex Synthesis**  
Qian Qi · 25 September 2026

Controlling r15 report: `cd793fde91fca07958c6c5bc3989e9c51a17540b`. Reviewed v30 publication: `a4abeb1c5e0323e5850e7f2446bf96fb1f7d4d8a`.

The work branch is `revision/general-theta-foundations-i-v31-compatible-memory-2026-09-25`. The publication workflow creates `revision/general-theta-foundations-i-v31-referee-ready-2026-09-25` only after a successful build. The revision descends from the controlling review and adds only the new package, its workflow and its root entry. No older manuscript, report, pipeline or branch is overwritten.

[Canonical English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r15](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed receipt](evidence/BUILD_RECEIPT.json)

[Unchanged v30 supporting article](supporting-results.pdf) · [Complete mathematical manuscript](complete-manuscript.pdf) · [Complete preserved development](complete-development.pdf) · [Source archive](evidence/SUBMISSION_SOURCES.zip)

## Mathematical advance

The canonical affine slice `L_t = aff(R_t) intersect P_t` is automatically closed under every positive normalized continuation shift. If each slice is a simplex, its vertices give a single rank-minimal machine. In particular, all cut ranks at most two imply simultaneous rank saturation. This is an explicit polyhedral test, not a search for the desired unknown transition tables.

At rank three, the paper supplies the compatibility obstruction missing from v30. A completely specified two-cut channel has separate minima 3 and 3, but its exact feasible profile region is the upward closure of `(3,4)` and `(4,3)`. This holds for `9/10 <= h <= 1`; the family has full support for `h<1`, and at `h=9/10` every answer probability is between 1/20 and 19/20. Both matching machines are written explicitly. The lower proof permits all stochastic state continuations and uses a quantitative forced-triangle bound. Thus separate rank saturation and causal rank saturation differ already at rank three.

Every additive stochastic encoder on a product input alphabet can be computed online without increasing its label count. Its scalar-coordinate minima yield a nonnegative mixture of local draws, and a weighted replacement process realizes that mixture with no retained summand selector. Consequently **every** simplex enclosing `eta*[-1,1]^n` in `[-1,1]^n` has an `(n+1)`-state online encoder using those same decoder vertices. For every dimension and positive signal, `K_n=n+1` if and only if either fixed-order or adaptive-acquisition peak is `n+1`.

The classical critical cube-absorption inclusions of Nevskii–Ukhalov therefore have explicit online implementations, including dimensions five and nine. The actual rational matrices and transition formulas are in the article and `evidence/CRITICAL_SIMPLEX_ROWS.json`. A normalized tensor construction gives further explicit critical encoders when `n+1=2^a*6^b*10^c`. Static geometry is attributed rather than claimed new.

The main text also corrects the checkpoint priority comparison: worst-case private-randomness RAC success and exact conditional synthesis have the same minimum alphabet, with no added shared seed. This is already the cube-containment geometry of Kondo et al., arXiv:2604.21274v3, Theorem 14 and Lemma 15. Exactification does not by itself bound the online cost of computing the replacement encoder. The additive theorem supplies that online step for its stated class.

## Resource and model boundaries

The principal exact counts concern clocked finite transducers with exact atomic stochastic rows. A separate proposition implements rational rows by fair bits and charges the phase, current input, old label and rejection-sampling prefix. The proper stochastic-language automaton, termination and residual-state normalization are defined internally. The inherited exponential residual-state/polynomial positive-state separation is proved in those conventions, not presented as a new historical succinctness claim.

The two-cut example is not an adaptive physical collision scheduler. The online simplex theorem concerns a single query following product acquisition. It does not determine all finite message counts, a sharp second-order interior-signal rate, a general adaptive policy optimum, or the independent A2/B4/C2 analytic gates. Those earlier results and obligations remain in the preserved sources and volumes.

## Reproduction

Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7 and a TeX installation supplying AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools, needspace and hyperref are sufficient.

```sh
python papers/GTF-I-v31-compatible-memory/verify.py
python -O papers/GTF-I-v31-compatible-memory/verify.py
python papers/GTF-I-v31-compatible-memory/build.py
```

After extracting the source ZIP, run `python GTF-I-v31-compatible-memory/build.py` from its parent directory. The archive includes exact predecessor inputs needed by the build; it includes no font files. The build executes v24–v31 regressions in normal and optimized Python, six new negative controls in both modes, three TeX passes, source binding, and predecessor text/raster checks. The workflow first publishes the native sources, builds that exact commit, then publishes PDFs and receipts without force.

The unchanged v30 article is retained as `supporting-results.pdf`. Its cumulative mathematical and historical volumes follow the complete new article and a divider. No old theorem is deleted or silently reclassified. Preservation and test counts are delivery evidence, not independent mathematical certification, priority clearance or journal acceptance.
