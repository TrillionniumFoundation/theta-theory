# General Theta Foundations I — revision 25

**Controlled Experiment Duality and Exact Marked Minimax Laws**  
Qian Qi · 24 September 2026

This revision responds to the latest eighth report at `c5c1a0d64f830bc3f036292357d8bbe2dbd04ca6` and retains the reviewed v24 package at `ad1336e48e414b2c01e928b844c796ab4765178b`.

The canonical English manuscript is [paper.pdf](paper.pdf), assembled as [main.tex](main.tex). The [complete mathematical manuscript](complete-manuscript.pdf) and [complete development](complete-development.pdf) append the unaltered predecessor volumes. The [response](RESPONSE_TO_REFEREE.md) maps all r8 mathematical and secondary requests. [Theorem locations](evidence/THEOREM_LOCATIONS.json) and the [executed build receipt](evidence/BUILD_RECEIPT.json) give the final theorem numbers, pages, checks and source commit.

## New results

The exact one-preparation marked collision value is `(85-7*sqrt(73))/64`. `marked-minimax.tex` proves a larger continuous marked-target family with an explicit least-favorable two-point prior and an optimal response, certified by a full-parameter square identity. It also computes the zero-preparation endpoint.

`controlled-dual.tex` proves a finite-action controlled posterior-predictive dual without a common dominating action, with one fixed adversarial parameter, stopping, protocol constraints, attainment, supersolution certificates and stability. A noisy-robust strict adaptive advantage illustrates the distinction. The equality is unrestricted-memory; the upper certificates cover constrained-memory architectures.

`physical-bridge.tex` gives the full original interface, collision geometry and positive-noise actual-mark coupling locally. `physical-improvement.tex` strengthens the threshold interval of the retained exact two-preparation theorem. The deterministic physical audit still has five event labels, peak twelve, and four preparations in total.

`joint-revelation.tex` gives the exact law `(1-(1-alpha)^N)*(1-1/K)` for a separate preparation/decision-memory family, with exact integer thresholds and matching resource scales. Its atomic alphabet and decision-width conventions are not substituted for the collision bit-level peak.

## Reproduction

Use Python 3.11 or newer, SymPy 1.14.0, PyMuPDF 1.26.7, and a TeX installation supplying AMS, Latin Modern, geometry, microtype, booktabs, mathtools and hyperref. From the repository root:

```sh
python papers/GTF-I-v25-controlled-minimax/verify.py
python -O papers/GTF-I-v25-controlled-minimax/verify.py
python papers/GTF-I-v25-controlled-minimax/build.py
```

`build.py` pins the v24 source by Git blob hash, assembles the full current article, executes ordinary and optimized new/v24 regressions and negative controls, compiles three times, rejects undefined references and overfull boxes, and verifies all appended predecessor pages. It writes only the new package and its new root entry. `evidence/SUBMISSION_SOURCES.zip` includes the current sources and the exact predecessor files needed to reproduce the build without repository history. It includes no font files.

The original paths and review are preserved by additive commits and by the frozen ancestry. The workflow is restricted to `revision/general-theta-foundations-i-v25-controlled-minimax-2026-09-24` and publishes the new package to that branch and `revision/general-theta-foundations-i-v25-referee-ready-2026-09-24`. Read actual workflow and receipt results, rather than inferring successful execution from this description.

## Exact scope

The collision least peak at two preparations, the full width-3-through-11 boundary, and `U2` are not solved here. The revelation law is a different exact resource family. The stationary autonomous bound is classical. The original Norberg full-proof comparison, B4/C2 aggregate obligations and eleven-paper closure are not claimed. These targets remain in the historical pipeline. Neither finite tests nor a successful build constitutes independent proof certification, originality clearance or journal acceptance.
