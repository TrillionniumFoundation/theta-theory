# R3 Hard Mathematical Referee Report

## Verdict

**Reject in current article form / major narrowing still required.  Readiness score: 4.1 / 10.  Confidence: 4 / 5.**

The R2 manuscript is much cleaner than the R1 object: it has a forward dependency ledger, explicit scope paragraphs, cleaner log output, and better separation between deterministic derivation and downstream probabilistic representation.  The main mathematical objection remains structural.  The manuscript still asks a referee to accept an entire program -- singular billiard geometry, anisotropic spectral theory, Dolgopyat suspension resolvents, moving-singularity response, full-gradient correctors, viscosity homogenization, nonconvex nonlinear expectations, and representation theory -- as one 246-page article.

## What Improved Since R1

- The final compiled `main.log` inspected before the R3 scope patch is clean: no unresolved references or citations, no overfull/underfull boxes, and no LaTeX or natbib warnings.
- The finite-response port is now repeatedly described as mechanical data rather than an oracle for effective HJB coefficients.
- The prelimit full-gradient jet construction and response-to-cell audit identities are more explicit than in R1.
- Part II now says the probabilistic representation layer is downstream of the deterministic semigroup.

These repairs remove several presentation objections.  They do not remove the central proof-burden objection.

## Blocking Concerns

### 1. The main theorem still relies on an exceptionally strong response package

The theorem around `main.tex` line 6088 advertises deterministic homogenization from ordinary billiard geometry and a finite-response port.  But the proof also needs, uniformly across the moving billiard bundle, all of the following:

- anisotropic Banach spaces stable under moving singularities;
- Lasota--Yorke estimates and spectral gaps for the singular collision maps;
- suspension resolvent estimates;
- differentiability of invariant objects and resolvents under moving singularity sets;
- exact regularity-loss bookkeeping for response terms entering the cell equations;
- viscosity comparison for the resulting degenerate, gradient-dependent HJB.

Each item is a publishable-level technical theorem.  The manuscript contains ordered proof ledgers and local arguments, but a skeptical referee will still ask whether the response package is being proved in full generality or effectively assumed.  The safest article-level statement is conditional on the closed geometric-response package, not universal for arbitrary finite-horizon billiard families.

### 2. "First principles" is still vulnerable unless carefully scoped

The paper's intended meaning is defensible: the effective coefficients are not inserted from a stochastic macroscopic model.  However, without explicit scoping, "first principles" can be read as "ordinary dispersing billiard assumptions alone imply the full spectral/resolvent/response/homogenization chain."  That stronger reading is not yet referee-safe.

The finite-response port also creates a second risk.  It is a microscopic mechanism, but it is expressive enough to shape the Hamiltonian defect used later for non-subadditivity.  The paper should not imply that all nonconvexity is forced by billiard chaos alone; it is produced by deterministic billiard dynamics plus the specified admissible port.

### 3. The response theory remains the load-bearing weak point

Moving-singularity response for dispersing billiards is the hardest technical segment.  The manuscript tracks trace terms, weak spaces, reduced resolvents, and regularity losses, but it does not yet present the response theorem in the style a specialist referee would expect: exact spaces, exact loss counts, uniform constants, domain transport maps, and a clear separation between cited known theory and new proof.

This is not a matter of wording.  The response formula feeds the cell equations and therefore the effective Hamiltonian.  If the response theorem is weakened, the main theorem must weaken too.

### 4. The article is still too large and internally repetitive

At more than sixteen thousand source lines and 246 compiled pages before this R3 repair, the manuscript reads as a monograph or proof ledger, not a normal mathematics journal article.  Many appendix sections restate the deterministic/acyclic structure rather than isolating one checkable estimate.  Even if the mathematics is ultimately correct, the current shape makes it hard for referees to identify the one new theorem they are being asked to verify.

### 5. Part II is acceptable only as optional representation theory

The BSDE and Girsanov sections are mostly scoped correctly after R2, but the introduction and conclusion still risk making them sound like part of the first-principles derivation.  They require additional regularity, smooth decoupling fields, and non-degenerate factorization assumptions that are stronger than the positive-semidefinite Green--Kubo tensor produced by the core construction.

## R3 Repair Applied

This round applies a conservative source patch to reduce overclaim risk:

- The abstract now says the construction is under a closed geometric, finite-response, transfer-resolvent, and moving-singularity response package.
- A new `Scope of the first-principles claim` paragraph states what "first principles" means and what it does not mean.
- The introduction now describes the result as conditional within the stated billiard-response hypotheses.
- The main homogenization theorem title and opening hypotheses now state the closed billiard-response package explicitly.
- The conclusion now says "conditional first-principles construction" rather than unqualified completion.

This does not solve the deeper article-shape problem.  It makes the manuscript more honest and less vulnerable to immediate rejection for overclaiming.

## Recommended Next Reconstruction

1. Choose a narrow submission theorem: either the conditional theta-expectation/HJB theorem, or the singular billiard response theorem, but not both as equally new cores.
2. Move the full spectral/resolvent/response package into a named assumption block if the target article is about nonlinear expectations.
3. Move most appendix proof-ledger material to a companion monograph or technical supplement.
4. Keep Part II as an optional representation appendix under explicit non-degeneracy and smoothness assumptions.
5. Add one concrete billiard/port example where the coefficients or Hamiltonian defect can be inspected without relying only on abstract realization language.

## Final Recommendation

The project has a real mathematical program, and the current source is now much cleaner than R1.  It is still not a submission-ready article.  The strongest next move is not another broad "prove everything" pass; it is a narrowing pass that turns the paper into a conditional, checkable theorem with a technical appendix, while reserving the complete singular-billiard response program for a separate work.
