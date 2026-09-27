# General Theta Foundations I — Revision 52

**Quantitative and Noisy Finite-Group Rigidity for Stochastic Realizations**  
Qian Qi · 27 September 2026

This is the revision responding to report r33 on Revision 51. The mathematical submission remains a general-journal research article. It is not replaced by a negative-results document, a reduced claim set, or a proposed downgrade in venue.

## Reading the revision

[Complete article](paper.pdf) · [Focused core excerpt](CORE_ARGUMENT.pdf) · [Native source](main.tex) · [Response to r33](RESPONSE_TO_REFEREE.md)

[Build receipt](evidence/BUILD_RECEIPT.json) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Source hashes](evidence/SOURCE_HASHES.json) · [Referee package](evidence/REFEREE_PACKAGE.zip) · [Complete isolated source archive](evidence/CORE_SOURCES.zip)

The complete article retains the entire active mathematical development of v51: all 201 loaded labels and all its theorem/proof modules remain present. The new main argument precedes the explicitly marked retained appendices. The core PDF is an excerpt, not a substitute for those proofs. The original v51 introduction is also retained verbatim as `V51_INTRODUCTION_RETAINED.tex` for provenance; its mathematical displays are present in the revised introduction. All previous repository paths and branches remain untouched.

## Main advances

Theorem `noisy-finitegroup52` proves that for every fixed `0 <= epsilon < rho/(2D)`, bounded clocked stochastic width over all horizons is equivalent to a finite generated orthogonal group. It applies to arbitrary widths without a reachability-rank or conditioning assumption. The proof identifies the finite-orbit subspace and uses finite executable word distortion on its orthogonal complement.

Theorem `height52` gives a rational-height lower bound `W_(N,epsilon) >= (log N - O(log log N))/(4 log c)` for planar rotations of infinite order, including alphabets with additional noncommuting commands. It does not assume a Diophantine exponent.

Theorem `beta52` makes one-surplus occupation effective: `beta_3(rho) >= 1 + rho^3/1024`. At `rho=1/10`, the exact six-state frontier holds for every `N >= 9,216,009` in the stated signed-permutation class. This sufficient horizon is deliberately coarse.

Theorems `conditioned52` and `computable-six52` give two different positive-error geometric results: an explicit arbitrary-width bound under a supplied reachable-basis conditioning bound, and an unconditional terminating algebraic procedure for a six-state noise interval. The latter procedure has not been executed at the illustrative large horizon. No numerical unconditional noise threshold is claimed.

Theorem `sos52` supplies a convergent global certificate hierarchy over unknown sections, using the classical Putinar–Lasserre mechanism. Proposition `counts52` prices its input and explicitly includes range invariance in the local Farkas system. Theorem `uniform52` gives a horizon-uniform rational finite-group compiler, with table size, workspace, and random-bit costs separated from label width.

## Reproduction

From this directory, with Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7, and a LaTeX distribution providing `amsart`, `lmodern`, and the packages in `main.tex`:

```sh
python build.py --check-core
```

The build runs v52 and five inherited exact regression suites both normally and with `python -O`; checks a resource-exhaustion negative control; compiles the article; verifies all inherited labels and the preservation manifest; renders every page; and rebuilds the complete source archive in isolation with page-text and page-raster equality. The build receipt binds these results to `GTF_SOURCE_COMMIT` when that environment variable is supplied.

The tests check finite identities and supplied certificates. They are not independent verification of the universal theorems, an exhaustive priority search, or closure of the separate A/B/C/D analytic pipeline. See [proof status](PROOF_STATUS.json), [history audit](HISTORY_AUDIT.md), and [resource ledger](RESOURCE_LEDGER.md).
