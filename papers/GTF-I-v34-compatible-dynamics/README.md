# General Theta Foundations I — Revision 34

**Fourier Budgets for Hidden Causal Memory**  
Qian Qi · 25 September 2026

Controlling r18 report: `ee524c3e210ede7d6ff927c2bd2a2a1a104cb28c`. Reviewed v33 publication: `aab96108125317342e51e6a946efc4d778429338`; its native source is `243e670a5be8628b9f4eaf60338348032357bcab`.

Work branch: `revision/general-theta-foundations-i-v34-compatible-dynamics-2026-09-25`. Successful source-bound publication also creates `revision/general-theta-foundations-i-v34-referee-ready-2026-09-25` without force.

[Focused English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r18](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Independently buildable core](evidence/CORE_SOURCES.zip)

## New all-hidden-state result

The main experiment still has four seed symbols, two command symbols, two coordinate queries and binary answers. Its probability margin is uniform in the horizon; each separate positive minimum remains three. The lower bound now applies to **all** hidden clocked realizations without passing through exponentially many vertices of projected sections.

For independent fair test commands, conditional past phases define a positive circle measure on at most K_t atoms. A homogeneous angular averaging inequality bounds all harmonic perturbations by one telescoping amplitude loss. A finite Fejer potential gives

```
#{0 <= t < N: K_t <= k} beta_(2k)(alpha) <= 18 k^3/kappa^2,
beta_m(alpha)=min_(1<=l<=m) sin^2(pi*l*alpha).
```

Wordwise row-TV error epsilon<1/20 implies kappa=1/10-2*epsilon. At every badly approximable angle, unrestricted hidden width is at least a constant times N^(1/5). At the golden angle, exactness gives

```
max(3,(N/16200)^(1/5)) <= W_N < 2*max(5,(40*N)^(1/3)).
```

The rational rotation `(3+4i)/5` instead gives `N <= 7200 W_N^3 25^(2W_N)`, hence a logarithmic lower bound, improving the former doubly logarithmic one. No bounded-type property is assumed for that angle.

The finite Blackwell garbling/deficiency formula is attributed explicitly. Its executable sequential composition and the new Fourier theorem give a quantitative total-defect lower bound for every proposed small-width diagram of the rotation experiment. Equivariant LP/PSD lifts are compared in the main text; no permutation symmetry is imposed on the main converse. Fixed-length autonomous and anytime autonomous tasks are defined separately.

## Reproduction

Use Python 3.11+, SymPy 1.14.0, mpmath and PyMuPDF 1.26.7, plus an AMS-capable TeX installation with Latin Modern, geometry, microtype, booktabs, mathtools, array, needspace and hyperref. From the repository root:

```sh
python papers/GTF-I-v34-compatible-dynamics/verify.py
python -O papers/GTF-I-v34-compatible-dynamics/verify.py
python papers/GTF-I-v34-compatible-dynamics/build.py
```

For a standalone review, extract CORE_SOURCES.zip and run `python GTF-I-v34-compatible-dynamics/build.py --core-only`. The full source archive includes exact predecessor inputs and verification scripts needed for the cumulative build; it includes no font files. The build binds native sources to the recorded commit, executes v24–v34 regressions in ordinary/optimized modes, runs deliberately invalid v34 controls, compiles three times, renders all current pages, and checks predecessor preservation. Actual results belong to the receipt, not this description.

## Preserved materials and scope

[Unchanged v33 article](supporting-results.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full rebuilding inputs](evidence/SUBMISSION_SOURCES.zip)

No predecessor path, review, or independent paper branch is modified. The large archives are optional provenance, not the compact journal submission. The exact hidden exponent remains between 1/5 and 1/3 at bounded type. No general optimal-lift algorithm, fully adaptive collision theorem, sharp rational order, noisy-tag theorem or A2/B4/C2 aggregate closure is claimed. Classical comparison, harmonic identities, symmetric lifts and spectral mechanisms are credited. Finite checks and successful publication are not independent proof verification, priority clearance or a journal decision.
