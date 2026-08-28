# Three-Paper Split Plan for `A_Theory_of__Expectations`

- Date: 2026-07-07
- Master source: `main.tex`
- Planning file only: no TeX source has been moved by this plan.

## Purpose

The split is not a retreat from the first-principles claim.  It is a way to make
that claim referee-checkable.  The current master manuscript asks one article to
carry three different referee loads:

1. singular billiard geometry, anisotropic transfer theory, suspension
   resolvents, and moving-singularity response;
2. deterministic homogenization to a nonconvex HJB equation and the resulting
   theta-expectation;
3. downstream payoff-dependent representation theory, including BSDE and
   Girsanov formulae.

These belong to overlapping but different referee communities.  The master file
should be kept as a source ledger while the submission-facing work is split into
three shorter papers.

## Dependency Order

```text
Paper 1: primitive billiard response theory
    -> Paper 2: first-principles theta-expectation and nonconvex HJB
        -> Paper 3: post-derivation representation calculus
```

Paper 2 should cite Paper 1 as the source of the verified response package.
Paper 3 should cite Paper 2 as the source of the nonlinear semigroup.

## Paper 1

### Working Title

`First-Principles Response Theory for Finite-Horizon Dispersing Billiards with Moving Singularities`

### Core Claim

Starting from primitive billiard geometry and a compact finite-response
mechanical port, derive the analytic response package needed later:

- a.e. global collision map with singularities;
- homogeneity strips, cone fields, distortion, and growth lemma;
- anisotropic Banach spaces and Lasota-Yorke estimates;
- map spectral gap and suspension resolvent;
- moving-singularity response formula;
- uniform multi-response bounds and finite regularity-loss budget.

The paper should end before the macroscopic HJB theorem becomes the main
object.  HJB can appear only as motivation for why the response package matters.

### Primary Main Theorem

Candidate statement:

> Under the primitive finite-horizon dispersing billiard geometry and the compact
> finite-response port, the singular collision map and suspension flow admit a
> uniform anisotropic spectral-resolvent theory, and all coefficient derivatives
> required by the later homogenization problem satisfy the stated
> moving-singularity response bounds with an explicit finite regularity-loss
> budget.

### Source Allocation from `main.tex`

Core source:

- Introduction material only as needed: `main.tex:215-334`.
- Microscopic billiards from geometric first principles: `main.tex:585-1363`.
- Global billiard map with singularities: `main.tex:2274-2567`.
- Transfer operators and deterministic spectral regularization:
  `main.tex:2568-3685`.
- Cell problems and parameter response, up to response calculus:
  `main.tex:3686-4358`.
- Quantitative closure of the critical deterministic estimates:
  `main.tex:6382-6847`.

Appendix or supplement source:

- Derivative formulae, collision coordinates, curvature, reflection, singular
  strata, finite horizon, homogeneity strips, cones, curvature recurrence,
  Jacobians, distortion, complexity, holonomy, invariant density, anisotropic
  norms, Lasota-Yorke, spectral gap, suspension resolvent, and parameter
  regularity: approximately `main.tex:7911-11177`.
- Forward dependency graph and uniform constants material:
  `main.tex:14406-15080`.

### Keep Out of Paper 1

- The full nonlinear HJB limit theorem, except as motivation.
- Theta-expectation axioms and nonlinear semigroup theory.
- BSDE and Girsanov representation theory.

### Target Journals

High target:

- `Inventiones Mathematicae`
- `Annales Scientifiques de l'ENS`
- `Journal of the European Mathematical Society`

Realistic strong target:

- `Communications in Mathematical Physics`
- `Ergodic Theory and Dynamical Systems`
- `Journal of Modern Dynamics`
- `Nonlinearity`

### Minimum Submission Shape

- 45-70 pages main text.
- One central response theorem.
- Exact Banach spaces and loss counts in the main body.
- Long proof ledgers moved to appendix or supplement.

## Paper 2

### Working Title

`A First-Principles Construction of theta-Expectations from Deterministic Billiards`

Alternative:

`Deterministic Billiards, Nonconvex HJB Equations, and theta-Expectations`

### Core Claim

Using the verified response package of Paper 1, derive a nonlinear HJB equation
from deterministic billiard mechanics and use it to construct a nonconvex
theta-expectation outside the subadditive G-expectation framework.

This is the flagship paper for the first-principles nonlinear expectation claim.

### Primary Main Theorem

Candidate statement:

> For the deterministic slow-fast billiard system with the finite-response port,
> the prelimit viscosity-duality solutions converge, after anisotropic pairing
> and then Liouville-a.e. extraction, to the unique viscosity solution of the
> derived nonconvex HJB equation.  The diffusion tensor and Hamiltonian are
> deterministic transfer-resolvent outputs, and the induced nonlinear semigroup
> defines a theta-expectation that is not generally subadditive.

### Source Allocation from `main.tex`

Core source:

- Revised introduction and first-principles adequacy criterion:
  `main.tex:215-527`.
- Deterministic micro-action and exact prelimit HJ equation:
  `main.tex:1364-2245`.
- Effective coefficients and analytic two-scale equation:
  `main.tex:4359-6381`.
- Main homogenization and end-to-end deterministic derivation:
  `main.tex:6132-6381`.
- Critical closure only as cited from Paper 1 or short appendix:
  `main.tex:6382-7214`.
- Microscopic origin of nonconvexity and non-subadditivity:
  `main.tex:7215-7480`.
- Acyclic deterministic derivation and dependency closure:
  `main.tex:7481-7612`.
- Conclusion: `main.tex:7900-7906`.

Appendix or supplement source:

- Comparison for the effective HJB: `main.tex:7930-8019`.
- Corrector cancellation and viscosity proof details:
  `main.tex:11178-11702`.
- Finite-horizon and a.e. collision-map details only as citations or
  compressed appendices: `main.tex:12229-12592`.
- Subsolution, supersolution, comparison, and full branch checks:
  `main.tex:12775-13139` and `main.tex:14050-14372`.
- Green-Kubo, corrector hierarchy, half-relaxed limits, nonconvexity algebra:
  `main.tex:15216-15755`.

### Keep Out of Paper 2

- Full proof of the singular-billiard response theory if Paper 1 is available.
- Detailed BSDE and Girsanov representation theory.
- Repeated proof-ledger sections that do not directly support the HJB theorem.

### Target Journals

High target:

- `Annals of Applied Probability`
- `Probability Theory and Related Fields`
- `Annales de l'Institut Henri Poincare, Probabilites et Statistiques`
- `Archive for Rational Mechanics and Analysis`

PDE/control target:

- `Annales de l'Institut Henri Poincare C, Analyse Non Lineaire`
- `SIAM Journal on Control and Optimization`
- `Communications in Partial Differential Equations`

Very high-risk option:

- `Annals of Mathematics`, only if the paper is rebuilt as a clean 50-70 page
  theorem paper and Paper 1 is a credible companion/preprint supporting the
  response theory.

### Minimum Submission Shape

- 50-75 pages main text.
- One visible theorem: deterministic billiards to theta-expectation.
- Paper 1 cited as the response-theory engine.
- A concrete billiard/port example included in the main text, not only in an
  abstract realization theorem.
- Representation material reduced to a short final section or moved to Paper 3.

## Paper 3

### Working Title

`Representation Calculus for theta-Expectations`

Alternative:

`Payoff-Dependent BSDE and Girsanov Formulae for Nonconvex theta-Expectations`

### Core Claim

Given the nonlinear semigroup derived in Paper 2, develop the post-derivation
representation calculus: payoff-dependent linearization, carre-du-champ,
calibrated diffusion representation, BSDE representation, and nonlinear
Girsanov/Cameron-Martin formulae.

This paper should not claim to derive the first-principles billiard mechanism.
It represents the semigroup after the derivation.

### Primary Main Theorem

Candidate statement:

> For the theta-expectation semigroup generated by the derived nonconvex HJB
> equation, each sufficiently smooth payoff determines a linearized generator and
> calibrated diffusion representation.  Under the stated nondegeneracy and
> smoothness assumptions, this yields a decoupled FBSDE and a semigroup-level
> Girsanov/Cameron-Martin formula.

### Source Allocation from `main.tex`

Core source:

- Part II: `main.tex:7631-7889`.
- Foundational theta-expectation properties: `main.tex:7634-7666`.
- Linearity obstruction: `main.tex:7667-7694`.
- Linearization, carre-du-champ, and Ito calculus: `main.tex:7695-7795`.
- BSDE representation: `main.tex:7796-7844`.
- Girsanov transformation: `main.tex:7845-7888`.
- Post-derivation representation hierarchy: `main.tex:7889-7899`.

Appendix or supplement source:

- Calibrated nonlinear semigroup representation and perturbations:
  `main.tex:11703-12052`.
- Detailed calibrated linear generator, gradient-vs-BSDE integrand, and
  parabolic orientation: `main.tex:13321-13685`.
- Calibrated calculus after deterministic derivation:
  `main.tex:15756-15890`.

### Keep Out of Paper 3

- Full billiard response theory.
- Full deterministic homogenization proof.
- Any claim that BSDE or Girsanov representation is primitive in the
  first-principles derivation.

### Target Journals

Primary target:

- `Stochastic Processes and their Applications`
- `Annals of Applied Probability`
- `Electronic Journal of Probability`
- `SIAM Journal on Control and Optimization`

Application-specific option:

- `Finance and Stochastics`, if a robust-pricing or model-uncertainty example is
  added.

### Minimum Submission Shape

- 35-55 pages main text.
- Clear statement that the semigroup is an input from Paper 2.
- All nondegeneracy and smoothness assumptions stated up front.
- No dependence on billiard technical lemmas except through Paper 2's HJB
  theorem.

## Master Source Policy

Keep `main.tex` as a monograph/source ledger until all three papers have clean
extracted drafts.  Do not delete it.  Do not try to make it the submission
version.  The master source remains useful for:

- theorem provenance;
- proof dependency checking;
- appendix extraction;
- cross-paper consistency;
- future monograph or technical supplement.

## Extraction Order

1. Create three new draft roots:
   - `papers/response-theory/`
   - `papers/theta-expectation-hjb/`
   - `papers/representation-calculus/`
2. Build Paper 1 first, because Papers 2 and 3 need its response theorem as an
   external theorem/preprint.
3. Build Paper 2 second, using Paper 1 as the response engine and keeping the
   first-principles claim central.
4. Build Paper 3 last, after Paper 2 fixes notation for the nonlinear semigroup.

## Immediate Next Actions

1. Freeze the current `main.tex` as the master source for extraction.
2. Create a Paper 1 skeleton with title, abstract, theorem map, and section
   headings.
3. Move no proof text yet; first create theorem inventory tables for Paper 1.
4. After Paper 1 skeleton is stable, repeat for Paper 2 and Paper 3.
5. Only then begin copying/reducing TeX content from `main.tex`.

## Referee-Risk Notes

- The phrase `first principles` should mean primitive deterministic billiard
  mechanics plus verified response theory, not a broad philosophical claim.
- The finite-response port must remain microscopic mechanical data, never an
  oracle for the effective Hamiltonian.
- Moving-singularity response is the load-bearing risk.  Paper 1 must present it
  in specialist style: exact spaces, exact loss counts, uniform constants, domain
  transport maps, and clear separation of known theory from new proof.
- Paper 2 needs one inspectable concrete billiard/port example.
- Paper 3 must keep BSDE/Girsanov language downstream of the deterministic
  semigroup.
