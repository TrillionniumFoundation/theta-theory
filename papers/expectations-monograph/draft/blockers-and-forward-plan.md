# Blockers and Forward Plan

- Date: 2026-07-07
- Master source: `main.tex`
- Current strategy: three-paper split with `main.tex` preserved as source ledger.

## Strategic Objective

Preserve the first-principles claim by making it technically auditable.  The
route is not to weaken the claim, but to split the proof burden into three
papers with clean referee communities and explicit dependency interfaces.

## Global Dependency

```text
Blocker A: singular billiard response theory
    unlocks
Blocker B: deterministic homogenization to nonconvex HJB / theta-expectation
    unlocks
Blocker C: post-derivation representation calculus
```

## Key Blockers

### Blocker A: Moving-Singularity Response

- Location: Paper 1.
- Severity: highest.
- Why it blocks everything: the response formula feeds cell equations and
  effective coefficients.  If this is not specialist-clean, the first-principles
  HJB theorem in Paper 2 remains vulnerable.
- Required output:
  - exact anisotropic strong/weak spaces;
  - Banach-bundle transport maps;
  - branch-interior derivative terms;
  - moving-boundary trace terms;
  - projector/resolvent derivative identities;
  - finite regularity-loss table;
  - uniform constants over the finite-response family.

### Blocker B: First-Principles HJB Derivation

- Location: Paper 2.
- Severity: high.
- Why it blocks the main claim: this is the flagship theorem connecting
  deterministic billiard mechanics to theta-expectations.
- Required output:
  - Paper 1 response package cited as theorem input;
  - deterministic prelimit HJ equation;
  - full-gradient corrector ledger;
  - Green-Kubo tensor and Hamiltonian as transfer-resolvent outputs;
  - viscosity-duality convergence theorem;
  - one concrete billiard/port example showing nonconvexity and
    non-subadditivity.

### Blocker C: Representation Layer Contamination

- Location: Paper 3 and Paper 2 boundary.
- Severity: medium-high.
- Why it blocks acceptance: BSDE/Girsanov material can make referees think the
  paper imports stochastic primitives into the first-principles derivation.
- Required output:
  - Paper 2 must mention representation only as downstream;
  - Paper 3 must explicitly assume the Paper 2 semigroup;
  - all nondegeneracy and smoothness assumptions for BSDE/Girsanov must be
    stated up front.

### Blocker D: Proof-Ledger Repetition

- Location: all extracted papers.
- Severity: high.
- Why it blocks acceptance: current master source reads like a monograph and
  repeats acyclicity/dependency claims.
- Required output:
  - one dependency diagram per paper;
  - one theorem inventory per paper;
  - repeated proof ledgers moved to appendix or supplement;
  - no internal process, agent, hash, or provenance text in submission-facing
    files.

### Blocker E: Known/New Boundary

- Location: Paper 1.
- Severity: high.
- Why it blocks acceptance: a dynamical-systems referee will reject vague
  novelty around classical billiard facts.
- Required output:
  - table separating known results, standard adaptations, uniform-family
    strengthening, and new moving-response claims;
  - precise citations for Sinai billiards, singular hyperbolic maps,
    anisotropic transfer spaces, and Dolgopyat-type suspension estimates.

## Continuous Execution Plan

### Stage 1: Paper 1 Skeleton and Inventory

Status: started.

Artifacts:

- `papers/response-theory/main.tex`
- `papers/response-theory/theorem-inventory.md`
- `papers/response-theory/risk-register.md`
- `papers/response-theory/execution-plan.md`

Next actions:

1. Add a theorem-map table directly to Paper 1 `main.tex`.
2. Add a known/new contribution table.
3. Extract only theorem statements, not full proof text.
4. Normalize notation against master `main.tex`.

### Stage 2: Paper 1 Response-Theorem Hardening

Next actions:

1. Expand the moving Banach-bundle setup.
2. Define the trace operator and derivative decomposition before the response
   theorem.
3. Create a regularity-loss table.
4. Write a proof outline for each response derivative class.
5. Move formula-heavy details to appendix.

Exit criteria:

- A specialist can see exact spaces, operators, traces, and loss counts without
  reading the master source.

### Stage 3: Paper 2 Skeleton

Next actions:

1. Create `papers/theta-expectation-hjb/`.
2. State Paper 1 response package as imported theorem.
3. Build the deterministic prelimit-to-HJB theorem map.
4. Add the concrete billiard/port nonconvexity example to main text.
5. Keep BSDE/Girsanov out.

Exit criteria:

- Paper 2 has one flagship theorem and can stand as the first-principles
  nonlinear expectation paper.

### Stage 4: Paper 3 Skeleton

Next actions:

1. Create `papers/representation-calculus/`.
2. Treat the Paper 2 semigroup as the input.
3. State payoff-dependent linearization, BSDE, and Girsanov results.
4. Move all first-principles derivation language out of Paper 3.

Exit criteria:

- Paper 3 is clearly post-derivation stochastic analysis/control theory.

### Stage 5: QA and Packaging

Deferred until external disk writeback finishes.

Tasks:

1. Compile each extracted paper.
2. Scan for internal/process/provenance terms.
3. Check undefined references/citations.
4. Check page counts.
5. Prepare referee-risk memo for each paper.

## Immediate Next Step

Continue Paper 1 skeleton hardening:

1. add theorem-map and known/new tables to `papers/response-theory/main.tex`;
2. add a response loss-budget table placeholder;
3. create theorem-statement extraction checklist from `theorem-inventory.md`.
