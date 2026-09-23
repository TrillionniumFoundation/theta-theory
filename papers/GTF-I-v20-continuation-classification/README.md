# General Theta Foundations I — v20

**Continuation Complexity and Stable Causal Certification**

This is the full English revision responding to the external v19 round-four report at commit `01679f4eac720dfd256594333e577b5db8145246`. The reviewed predecessor is `9cf70fe7c8aa289d1be26934451e223364aa06ef`.

Start with `paper.pdf` and `RESPONSE_TO_REFEREE.md`. `complete-development.pdf` appends the predecessor's entire 340-page development without changing any predecessor page. `main.tex` and its local inputs are the complete canonical source. `evidence/THEOREM_LOCATIONS.json` supplies the compiled statement numbers and pages.

## Principal additions

The decision-continuation spectrum classifies the number of states needed at a charged training--validation cut, with a uniform finite-sample realization. Its first two values on the ideal private marked collision family are exactly 1/8 and 3/8. Three states are necessary and sufficient for uniform physical expected score above 2/5. The lower bound permits arbitrary finite training schedules and feedback-row selection; a feedback-pushforward subfamily reduces every post-cut continuation to the same response geometry.

A deterministic three-event selector uses 399 informative candidate trials, one optional ignored candidate trial, and two validations. Its full trial-cut residual profile is computed exactly, including stochastic exact implementations. The maximum is 20,301 at trial cut 200. At every scheduled bit-acquisition or validation epoch, 40,602 states suffice (sixteen bits). These are different claims: exact physical task complexity at one cut; exact profile for the specified rule; an implementation upper bound for peak memory over all successful algorithms.

Weighted distinguishing-suffix graphs give distribution-sensitive error and Bayes-regret bounds for finite-valued terminal decisions. Three explicit measure-change/coupling-version lemmas support the retained global entropic transport theorem. The old two-count rule, its nineteen-bit bound, and all inherited mathematical modules are retained; an explicit phase-state table is added.

## Reproduction

From a repository checkout, install `requirements.txt` and a LaTeX distribution with `amsart`, `lmodern`, and TikZ, then run:

```sh
python papers/GTF-I-v20-continuation-classification/build.py
```

The build requires the unchanged predecessor at `papers/GTF-I-v19-referee-resolution/`. It executes normal and optimized diagnostics, twelve negative-control executions, three LaTeX passes, source-hash checks, and text/raster equality for every appended predecessor page. Build success is not independent mathematical certification or a journal acceptance assessment.

## Proof and publication status

The new results have written proofs and executed finite diagnostics. Independent mathematical review is pending. The original Norberg proof-level literature crosswalk remains unverified because the original full text was not obtained. The full eleven-paper historical program, the general B4 nonlinear kinetic aggregate, and the broader C2 aggregate are not certified by this revision. Their original targets and files remain preserved, with explicit theorem-level status rather than branch-name status.
