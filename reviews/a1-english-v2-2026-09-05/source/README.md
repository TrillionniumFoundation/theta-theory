# A1 — Realizable Mechanical Experiments, Path Selection, and Response

**English research edition 2.0 — 5 September 2026**  
Author named in the manuscript: Qian Qi.

This is the complete English replacement of the earlier Chinese A1 working
manuscript. It is a substantive expansion, not a word-for-word translation.
The original Chinese manuscript, PDF, and ZIP are not included here.

## Read the paper

`main.pdf` is the compiled manuscript. `main.tex`, `references.tex`, and
`sections/` form its complete source. `A1_English_Full_Manuscript_2026-09-05.tex`
is a separately compiled self-contained source. `PROOF_LEDGER.md` maps every
theorem/proposition/lemma/corollary to its source and actual PDF page.

The paper has 20 main sections and four technical appendices. Its main chains
are mechanical instruments -> chronological path laws -> attainable selection
and information -> predictive and resource states -> geometric response ->
whole-preparation finite-time Lorentz verification. Standard measure theory,
information identities, prediction concepts, and hybrid-sensitivity techniques
are attributed explicitly; the package makes no priority or journal-acceptance
claim.

## New substantive content

* An exact relative-entropy deficit for constrained realizability, with solved
  coarse-preparation and density-cap problems and a first-order cap response.
* A canonical measurement shear retaining back-action and finite apparatus
  preparation, rather than silently adding independent microscopic noise.
* Parameter-family predictors, retained likelihood information, residual
  resources, legal pasting, and a compact continuous-alphabet theorem with
  explicit positive-density hypotheses.
* Test-dependent approximation and derivative budgets, without requiring
  singular deterministic path laws to be close in total variation.
* A complete short-horizon incoming-tube assembly over the **entire smooth
  preparation** of the periodic Lorentz table, including arbitrarily grazing
  incidence. The horizon is strictly shorter than the uniform minimum
  intercollision distance, so there is at most one collision.
* Direct collision-bit identification, positive Fisher information and QMD,
  without an added Gaussian readout; general noisy channels are subsequent
  information-losing extensions.
* Actual completed-record acceptance, exact trial budgets, and the impossibility
  of changing the equilibrium short-time hit fraction by direction-only
  preparation. This last statement is an explicit restricted-operation result,
  not an impossibility claim about other interventions.

For the triangular cell, `R in [0.45, 0.47]` and `0 < T < 0.06`, the natural
unit-speed equilibrium preparation has

    p_R(T) = 2 R T / (sqrt(3)/2 - pi R^2).

The complete record has all finite orders of strong negative-Sobolev radius
response in the corresponding reporting spaces. This is not a long-time
multiple-collision response theorem or a full hard-sphere dynamic LDP.

## Reproduce

Python 3.10+ is recommended. Install the Python dependencies:

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 tools/build_and_verify.py
```

A TeX installation must supply `pdflatex`, Latin Modern and the standard packages
listed in `main.tex` (including `microtype`, `mathtools`, `bookmark`, `geometry`,
`enumitem`, and `fancyhdr`). A typical TeX Live installation with
`texlive-latex-extra` and `lmodern` is sufficient. No fonts are distributed.

The verifier builds the split and single-file sources three times each in
separate temporary directories with `-no-shell-escape`. It runs the finite
test suite, checks local source hashes before and after execution, rejects
undefined references/citations, missing characters and overfull boxes, and
compares the two PDFs page by page at a fixed render resolution. It writes
`validation/VERIFICATION.json`, test/build logs, and `PROOF_LEDGER.md`.
The source is not changed by the verifier. `SOURCE_MANIFEST.json` is a byte
integrity record, not mathematical certification.

## Evidence and scope

`validation/VERIFICATION.json` reports the executions actually performed.
`validation/VISUAL_AUDIT.json` records the separate page inspection.
`validation/previous_delivery_identity.json` contains only filenames, byte
counts and hashes of the superseded Chinese deliverables, not their contents.
`validation/CLEANUP.json` records removal of the local superseded deliverables;
it does not claim to remove previous chat attachments or rewrite Git history.

Exact rational and symbolic checks are distinguished from floating quadrature
and finite geometric samples in the test source. Passing tests does not prove
an infinite-dimensional theorem. The written proofs remain open to independent
specialist review. No proof assistant, remote CI, or journal review is claimed.

## Downstream boundaries

Theorems explicitly scoped to finite alphabets, compact positive continuous
observation densities, regular collision chambers, or the one-collision Lorentz
window retain those hypotheses. Long-time many-collision response requires a
new global assembly estimate. Kinetic, thermodynamic and hydrodynamic limits,
long-time posterior contraction, and a prescribed nonconvex theta generator
are not silently imported or declared completed.

This delivery does not modify the theta-theory GitHub repository.
