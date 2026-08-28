# Paper 2 Risk Register

## R1. Paper 2 Could Become a Monograph Again

- Severity: blocker.
- Referee concern: if response theory, HJB proof, and representation calculus
  all reappear, the paper will look like the original 247-page manuscript.
- Mitigation:
  - cite Paper 1 as the response-theory engine;
  - include only the response interface theorem;
  - move BSDE/Girsanov to Paper 3.

## R2. First-Principles Claim Could Look Conditional

- Severity: blocker.
- Referee concern: importing Paper 1 might look like assuming the hard part.
- Mitigation:
  - phrase Paper 1 as a companion theorem derived from primitive billiards;
  - keep the dependency chain visible in the introduction;
  - make the finite-response port microscopic and inspectable.

## R3. Concrete Example Is Required

- Severity: high.
- Referee concern: nonconvexity and non-subadditivity may look formal unless
  there is a concrete billiard/port example.
- Mitigation:
  - include a main-text example specifying table family, port read-outs, and the
    Taylor coefficient responsible for nonconvexity;
  - avoid hiding the example in an appendix.
- Current status: `main.tex` now contains a concrete triangular-lattice
  finite-horizon Lorentz cell, two normal deformation modes, a concrete
  observable form, and an inspectable nonconvexity coefficient proposition with
  a dominance inequality.  The deformation modes and observable bump are now
  explicit normalized smooth bumps.  The response bound `C_resp(x)` is now
  decomposed into Paper 1 exported constants for projector response, reduced
  resolvent response, moving-trace insertion, and regularity loss, and each
  constant is tied to exact Paper 1 theorem labels in the source inventory.
  Paper 2 now also has a bibliography/provenance pass for the macroscopic
  viscosity, homogenization, and nonlinear-expectation tools.  The appendix
  now adds a normalized numerical certificate for the concrete-port
  inequalities and an open stability margin for nearby smooth ports.

## R4. HJB Comparison and Viscosity Closure Must Be Clean

- Severity: high.
- Referee concern: anisotropic weak convergence and viscosity half-relaxed
  limits may not obviously interact.
- Mitigation:
  - isolate perturbed-test residual identity;
  - state comparison theorem for the derived HJB;
  - keep microscopic singular-set issues behind the Paper 1 response interface.
- Current status: `main.tex` now contains a corrector hierarchy definition,
  deterministic residual identity lemma, sub/supersolution residual
  proposition, Crandall-Ishii comparison modulus, and comparison/uniqueness
  theorem for the derived terminal-value HJB.  The comparison proof has been
  replaced by a doubled-variable argument using the finite-response
  coefficient modulus.  The sub/sup residual proof and the main homogenization
  proof have been expanded with contact-frozen perturbed tests, paired relaxed
  envelopes, comparison closure, and Liouville-a.e. extraction.  The residual
  identity now includes the contact-jet freezing, scale cancellation,
  order-one invariant/centered split, and anisotropic residual bounds.  The
  Paper 1 citation hooks now name the imported response-package components, and
  the journal-facing theorem map no longer prints internal source-line
  references.  A standalone `technical-appendix.tex` now adds the first technical HJB
  proof-ledger layer: finite-response micro-action, contact-frozen corrector
  hierarchy, four-scale residual identity, normalized-gauge half-relaxed
  passage, density-to-state upgrade, coefficient comparison, and
  nonconvexity/subadditivity algebra.  The second appendix pass added the
  exact prelimit action graph, closed prelimit Hamilton-Jacobi identity,
  residual constant ledger, branch residual summation, uniform sub/sup residual
  modulus, and concrete parameter window for the nonconvex port.  The third
  pass now adds endpoint-jet realization, endpoint reciprocity, specular
  endpoint-variation cancellation, moving branch-boundary trace control,
  recursive corrector hierarchy closure, synchronized admissible densities, and
  a doubled-variable comparison refinement.  The fourth pass adds a
  correlation Hilbert bundle, Green-Kubo coboundary-kernel criterion,
  correlation-factor transport, Green-Kubo comparison trace estimate,
  terminal-value stability, and a concrete parameter-choice recipe.  The fifth
  pass adds full branch residual checks: central branch residual families,
  moving-boundary trace residuals, high-strip cutoff, and the final branch
  residual modulus.  The sixth pass adds admissible-density smoothing,
  perturbed-test smoothing, smooth-approximation closure, and a dimensionless
  parameter audit table for the concrete nonconvex port.  The seventh pass adds
  a normalized numerical certificate and stability margin for the concrete-port
  inequalities.  Remaining work is no
  longer the first HJB proof layer; it is finer migration from the long master
  source, especially venue-specific proof polish or a true numerical orbit
  experiment if requested.

## R5. Subadditivity Failure Must Be Stated Precisely

- Severity: medium.
- Referee concern: saying "not G-expectation" is vague.
- Mitigation:
  - prove a short-time Hamiltonian defect;
  - show exact payoffs producing failure of subadditivity;
  - state which G-expectation axiom is not satisfied.
- Current status: `main.tex` now proves the short-time semigroup defect from
  two smooth terminal payoffs with prescribed gradients and zero Hessians at
  the contact point.  The proof uses the terminal-value convention
  `Etheta_t[phi](x)=u(0,x)` and shows a strict violation of subadditivity.

## R6. Target Journal Positioning

- Severity: medium.
- Referee concern: probability journals may want a probabilistic theorem, while
  PDE/control journals may want cleaner PDE structure.
- Mitigation:
  - make the theorem statement visibly probability/PDE hybrid;
  - keep representation material short;
  - choose target after Paper 1 stabilizes.
- Current status: `submission-package-checklist.md` and `referee-risk-memo.md`
  now record the two main posture options: probability-facing nonlinear
  expectation framing versus PDE/control HJB framing.  This is now a venue
  choice rather than a draft-blocking mathematical risk.
