# Proof audit — General Theta Foundations I, R74

This is an author proof and evidence record. Complete written proofs are the mathematical basis of the manuscript. Separately assigned AI proof challenges and finite calculations assist error detection; they are not independent human referees, proof-assistant certificates or editorial decisions. All claims are conditional on their printed hypotheses.

## New proof obligations and their resolution

| Obligation | Written argument and exact scope |
|---|---|
| Attain the representation lower bound using legal probability tables | `thm:r74-low-contrast` separates the constant and zero-average modules, embeds the latter equivariantly in a minimum permutation module, perturbs the uniform preparation and scales a zero-sum decoder. Explicit positive constants ensure every row is a probability row. Zero-average output columns are handled separately. Every finite observable group and finite output set are included. |
| Preserve invariants at positive contrast and retain endpoints | An invertible equivariant residual map preserves group, module and residual equality for `t>0`. Finite actions, compact parameter spaces and decoder mixing give closed initial budget intervals. Algebraic endpoint effectiveness uses expressly credited real quantifier elimination; it is not claimed executed for every input. |
| Remove the preparation/decoder bilinearity without an unjustified normality assumption | `lem:r74-normal-orbits` proves the quotient invariance only for normal stabilizers. `thm:r74-quotient-lp` is unrestricted precisely when every subgroup is normal. Distinct orbit types are merged, zero masses are discarded, and the inverse construction is explicit. A nonnormal `S_3` negative control is retained in diagnostics. |
| Obtain true lower certificates for a union of low-budget machines | `thm:r74-quotient-dual` gives the exact support function for each selected quotient family. The four-bit proof classifies every low-budget family and uses a witness for each possible partition. It does not infer a global union separator from one LP. The perturbation radius is a sufficient lower certificate, not a sharp radius or an off-line upper. |
| Prove matching transitions rather than infer them from rank | The `S_3` proof excludes all actions of size at most five by explicit standard-module coefficient constraints and matches the threshold with a three-point controller. The four-bit proof keeps dimension and module support fixed, excludes all costs at most eleven above `3/5`, and supplies exact degree-ten and degree-twelve constructions. |
| Construct one all-command contracting realization | `thm:r74-contraction` uses one supplied norm and one whole-ball probability margin. A maximal separated net gives an invariant core; actual prefix labels enter it. The stated count includes the pure starting label. The result is a quantitative application of classical positive-realization geometry, without a minimality or joint-spectral-radius decision claim. |
| Verify the physical conditional example | The Choi calculation proves all three displayed branches completely positive, with a strict `I_4/16` margin for the third. Their sum is exactly depolarizing; all outcome floors are uniform. Direct cylinder calculations prove stationarity, one-dependence and Hankel rank three. |
| Exclude every smaller classical hidden model | The productive/reachable zero-branch restriction has bounded relative powers. The observed three-mode cylinder forces a peripheral phase. The irreducible equality argument makes cycle lengths multiples of its order. At the lower size, a weighted full cycle and the pure-start word probabilities force a contradiction. This holds for arbitrary real nonnegative hidden tables, not only physical dictionaries. |
| Match the conditional lower and charge initialization | One regular polygon is invariant for every normalized branch; the third has radius at most `5/11`. Its barycentric rows preserve each subnormalized branch and hence every word. A stationary mixed initialization exists. One added counted anchor attains `q+1`, and the lower proves its necessity. `sin(theta)!=0` excludes the degenerate one-/two-mode cases. |

The primary mechanism comparisons are in `LITERATURE_AND_PRIORITY.md`. In particular, FRDN phase obstructions and commensurate memory phenomena precede this family; the current claim concerns its simultaneous properties and exact pure-start rigidity.

## Historical corrections and retained authority

All 185 predecessor statement labels remain active in the current compiled pair. The active R74 increment has twelve labels: eleven main statements and one supplement corollary explicitly recording the inherited R69 period-four consequence. This is a statement inventory, not a novelty count.

A proposed R74 posterior-interiority theorem was recognized during the historical cross-check as already proved **more strongly in R68**. The complete retained theorem includes several preparations, sparse rows, algebraic construction, paid block clocks, complete stopped laws including nontermination, costs and a stronger state-positive noise exponent. The duplicate draft and its weaker dictionary lower were removed from the active source graph and preserved in `provenance/author-research/superseded/`. The current section 39 is an unnumbered bridge to the original proof. The new finite instrument diagnostic exercises that inherited theorem and is not evidence of a new R74 discovery.

The period-four transition at `1/sqrt(3)` already follows from `thm:r69-sector-phase`. The new corollary corrects an obsolete open-status description. The older R73 finite-probe gap and sufficient `89/90` interval remain valid, nonsharp certificates. Robust tied closure on the declared R66/R67 rigid class likewise remains closed.

The 47 pinned current source bodies and the 32,284-byte inherited supplement suffix are unchanged from R73. The complete 34-file R58 companion has tree `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`. The per-file preservation inventory records every R73 source file and its retained exact body. Original causal transfer, predictive compression, performed laws, variational/dual principles, finite-order measurement, two-stage reset, communication/memory separation, rank-constrained discrimination, geometry and strategy realizability keep their own proof authority. Preservation is not a claim of a fresh reproof of every historical result.

## Separately assigned author-team challenges

`provenance/author-research/AUTHOR_TEAM_CHALLENGE_R74.md` reconstructs the new structural proofs and conditional classification. `provenance/author-research/INDEPENDENT_AI_CHALLENGE_INSTRUMENTS.md` reconstructs the physical dictionary and conditional-family arguments, records the R68 duplication correction, and identifies inspected source snapshots. The adjective independent in that historical filename means a separately assigned AI task within the author workflow; it does not mean an external human expert. `provenance/author-research/VERIFIER_PORT_AUDIT.md` checks the verifier's actual R74 counters, source conventions and inherited-byte checks. Attribution-only changes receive explicit addenda where checked. A changed hash alone is never represented as a new proof review.

The challenge also supplied a distinct exact script, `challenge_c2_four.py`, which enumerates all 67 subspaces of the four-dimensional binary character space and all 69,728 quotient families of cost at most eleven, then checks the active-support reduction and explicit dual norms. This is a finite independent reconstruction of one model's combinatorics, not an exhaustive proof of the general group theorem.

## Diagnostic design and actual precommit executions

The final strict verifier runs eighteen scripts, each in ordinary Python and `python -O`, verifies byte-identical stdout, valid positive counts, successful exit and a reported pass, and rejects removable Python `assert` gates. The fourteen inherited script bodies are checked against actual R73 Git blobs.

| Newly added diagnostic | Actual development execution | Scope |
|---|---:|---|
| `diagnostics_r74_contrast.py` | 3,173 exact; no floating probes | Rational quotient controllers, first-command initialization, all 26 partition witnesses, Fourier modes, `S_3` spanning and nonnormal negative control. |
| `diagnostics_r74_noisy.py` | 9,012 exact; no floating probes | Common-contraction construction, rational qubit branches, exact word identities and finite-order polygon examples. |
| `diagnostics_r74_instruments.py` | 873 exact; no floating probes | Inherited R68 operator intertwining for two noncommuting state-dependent instruments, counted preparation, zero branches, finite words, two adaptive policies and costs. |
| `challenge_c2_four.py` | 5,170 exact; no floating probes | Separately reconstructed finite subgroup-family enumeration and rational payoff certificate norms. |

These are actual development records retained with their code hashes under `provenance/author-research/`; they are not substituted for the final source-bound execution. The final `BUILD_RECEIPT.json` in the publication packet determines which suites actually ran at the committed source, all arithmetic totals and the new PDF hashes. Finite diagnostics do not prove continuum assertions, perform general quantifier elimination or certify formal correctness.

## Native source-bound validation

`seal_source.py` records every regular source file except the root manifest itself and declared cache directories. It checks the exact predecessor index, retained bodies and supplement suffix, R65 report and full companion tree. The manifest is an inventory, not a build verdict.

Strict `verify.py` requires a full forty-character source SHA equal to actual HEAD. It checks the recomputed current paper tree against that commit, the unchanged complete R73 tree and ancestry, and every changed path against the new source-directory boundary. It compares the supplement suffix with bytes read from the actual predecessor Git object, not just a declared hash. It verifies the manifest before and after execution and refuses in-tree or reused output directories.

The native paired build performs three `pdflatex` passes each for main and supplement, importing genuine references without AMS `tocindent` dimensions. The complete retained companion receives three separate passes. Shell escape is disabled. Undefined or multiply defined references, overfull boxes and unresolved rerun warnings fail the gate. Actual auxiliary files produce the 197-entry theorem index, which must equal the sealed index including source, label, number and page. Each PDF receives an actual page count and SHA-256. Rendered-page inspection is separately recorded after the strict build.

The final precommit layout draft completed at 39 main pages, 144 supplement pages and 37 companion pages, with 197 indexed statements and no final fatal warning. It deliberately skipped diagnostics and has status `DRAFT_COMPILE_COMPLETE`. It is not the final strict build, and its PDF hashes are not delivery identities.

Local strict execution, remote publication and hosted CI are separate evidence classes. The R65 terminal run `38861581555` succeeded only at `ee79ca9114f8009d62c056d07381b766645e3fc4`; its retained receipt closes that historical readback issue. No unobserved current hosted run, human assessment, formal proof or journal decision is claimed.
