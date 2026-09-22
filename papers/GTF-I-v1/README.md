# General Theta Foundations I — first complete manuscript

**Causal Experiments, Predictive Quotients, and Resource-Aware Reduction**  
Qian Qi · Version 1 · 22 September 2026

`main.tex` is the native, standalone English manuscript. It includes twelve main
sections, two appendices, all proofs claimed in this first paper, and a primary-source
bibliography. It does not need an A1/A2 checkout or historical source generator.
The build executed for this delivery produces **34 pages**.

The preserved Chinese research outline is at
[`../../foundations/general-theta/General_Theta_Foundations_v0.1.md`](../../foundations/general-theta/General_Theta_Foundations_v0.1.md).
The [implementation addendum](../../foundations/general-theta/GTF_I_IMPLEMENTATION_2026-09-22.md)
records what this paper proves and what remains a program-level research objective.

## Main results

- Positive causal experiment axioms and a minimal predictive quotient, with explicit
  finite/compact measurable-realization conditions rather than a universal smooth quotient.
- Executable causal reductions, charged simulator states, predictable total-variation
  error composition, and bounded-risk transfer under a common decision task.
- A finite-state emulation theorem combining quantization, numerical update errors,
  arbitrary common feedback controllers, and visible stopping.
- A concrete refreshing hidden Markov model with a binary commanded detector.
  Its optimal checkpoint and causal squared-prediction excess is comparable to
  `epsilon^2 M^(-2/d)` for every positive time and every integer budget, uniformly
  through epsilon=0 and over the declared refresh interval. One fixed codebook
  attains the upper bound for all times. The lower bound uses the actual command/report
  density and its exact Jacobian, not a fictitious uniform posterior.
- For a different, jointly attenuated terminal probe the order is `epsilon^4 M^(-2/d)`.
  The difference is physical query normalization, not an inconsistency.
- Fully stated posterior, entropy, score, response, and exponential-transform identities;
  twelve boundary examples separating information, memory, and asymptotic scales.

The hidden-state refresh is essential to the time-uniform result. Commands are
continuously distributed for its lower bound. Calibration is known to the machine.
The theorem is about retained labels, not a free claim about optimal computation time,
workspace, unknown calibration, or two-sided equivalence of infinite path laws.

## Build and replay

Requirements: Python 3.10+, a TeX installation providing `pdflatex`, `amsart`, Latin
Modern, `microtype`, and `hyperref`, and `pdfinfo` (Poppler). No nonstandard Python
package is required by the build or diagnostics.

```sh
cd papers/GTF-I-v1
python3 tools/verify.py
python3 -O tools/verify.py
python3 build.py
```

The PDF is generated as `build/main.pdf`. The optional branch-scoped publisher also
commits `paper.pdf` after a successful exact-source runner build; its separate receipt
records whether that publication actually occurred. `build/BUILD_RECEIPT.json` binds the exact
input hashes, PDF hash, actual compiler calls, ordinary/optimized diagnostic outputs,
and rejected negative controls. The checked delivery receipt is under `evidence/`;
raw local logs and the compiled PDF are included in the accompanying downloadable
source/PDF package. The Git source publication does not depend on a workflow runner.

Current execution: **977 finite checks**, identical ordinary/optimized output;
**two deliberately incorrect formulas rejected**; **three compiler passes**;
**no final undefined references or overfull boxes**. The page inspection record
reports its separate scope. These are finite reproducibility checks, not formal
verification of the universal proofs or a journal decision.

## Mathematical and publication status

This is an author-requested first research manuscript, not an independently refereed
or accepted paper. Classical kernel, sufficient-statistic, filtering, and quantization
results are attributed. `LITERATURE_AND_SCOPE.md` distinguishes the established
background from the two quantitative results developed here; it does not certify
exhaustive priority. `PROOF_LEDGER.md` lists all theorem-like statements and their
source locations. The conditional LDP and memory interfaces do not claim to prove
the outstanding Sinai or hard-sphere model theorems.

Publication adds this new directory, the General Theta outline/addendum, a root entry
index, and a branch-scoped PDF publication workflow. All pre-existing manuscripts and
branches remain unchanged. The workflow is triggered only by an explicit request file
on this revision branch and never writes to main.
