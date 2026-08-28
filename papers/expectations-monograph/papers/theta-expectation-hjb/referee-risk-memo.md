# Paper 2 Referee-Risk Memo

This memo records the current submission posture for
`A First-Principles Construction of theta-Expectations from Deterministic
Billiards`.

## Current Verdict

Paper 2 is now a coherent standalone article draft.  Its main proof burden is
the deterministic HJB/theta-expectation construction, while singular-billiard
response theory is imported from Paper 1 through a named theorem interface.
The current package has a clean PDF build, bibliography, and one retained
submission PDF.

## Main Referee Risks

### R1. Imported Paper 1 theorem may look conditional

Status: controlled, but venue-dependent.

Mitigation already in the draft:

- The introduction states the dependency chain from primitive billiard geometry
  to Paper 1's response package to the HJB limit.
- The response input is isolated in `ass:paper1_response_input`.
- The Paper 2 proof does not repeat the singular-billiard response proof.

Remaining action:

- Once Paper 1 has an external preprint/submission identifier, cite it in the
  introduction and bibliography instead of relying only on the internal
  companion-paper description.

### R2. Viscosity comparison and half-relaxed closure may be challenged

Status: materially addressed.

Mitigation already in the draft:

- The residual identity freezes the actual contact jet.
- The sub/supersolution argument uses normalized contact-frozen perturbed tests.
- The comparison theorem uses a Crandall-Ishii doubled-variable proof.
- The bibliography now cites the standard viscosity/comparison and
  half-relaxed stability references.
- The technical appendices now record the full finite-response micro-action
  ledger, endpoint-jet realization, endpoint reciprocity, exact prelimit action
  graph, specular endpoint-variation cancellation, moving-boundary trace
  control, contact-frozen and recursive corrector hierarchy, branch residual
  constant ledger, four-scale residual identity, half-relaxed passage,
  synchronized doubled-variable comparison, density-to-state upgrade,
  coefficient comparison ledger, Green-Kubo correlation Hilbert
  factorization, terminal-value stability, concrete nonconvex parameter window,
  concrete parameter-choice recipe, full branch residual checks,
  smooth-approximation closure, a dimensionless parameter audit table, and a
  normalized numerical certificate with a stability margin.

Remaining action:

- If a PDE-focused venue asks for numerics beyond an inequality certificate,
  add a true orbit/parameter experiment rather than changing the main theorem.

### R3. Nonconvexity could look formal

Status: addressed in the main text.

Mitigation already in the draft:

- The concrete example uses a finite-horizon triangular Lorentz cell.
- Two deformation modes and the observable bump are explicit normalized smooth
  bumps.
- The dominance inequality separates the direct negative action term from
  Paper 1 response-corrector bounds.
- Non-subadditivity is proved from a short-time Hamiltonian defect using two
  smooth terminal payoffs.

Remaining action:

- If a referee asks for numerics beyond the normalized certificate, add a small
  experiment illustrating the already-normalized parameter audit rather than
  weakening the theorem.

### R4. The paper might drift back into the original monograph

Status: controlled.

Mitigation already in the draft:

- Paper 1 proofs are not duplicated.
- BSDE, Girsanov, and Cameron-Martin formulae are mentioned only as downstream
  exclusions or Paper 3 inputs.
- The visible theorem map is journal-facing and no longer prints internal
  source-line references.

Remaining action:

- Do not add representation-calculus material during Paper 2 revisions unless
  the venue explicitly requests it.

### R5. Target-journal framing remains unsettled

Status: open positioning question, not a proof gap.

Likely framing choices:

- Probability journal: emphasize deterministic construction of a nonlinear
  expectation and the failure of subadditivity/G-expectation structure.
- PDE/control journal: emphasize the fully nonlinear HJB limit, comparison,
  and nonconvex Hamiltonian.
- Dynamical-systems-adjacent venue: emphasize Paper 1 as the technical engine
  and keep Paper 2 as the application theorem.

## Current QA Facts

- `theta-expectation-hjb.pdf` is 27 pages and 482590 bytes.
- Single PDF SHA256:
  `c8c55404f9464029fd8f3f7454f4756d0daa465fe381b0187bffa1944a8c9cf7`.
- Final build command: three
  `pdflatex -interaction=nonstopmode -halt-on-error main.tex` runs after the
  technical appendix merge, with BibTeX already current.
- Log scan is clean for fatal errors, LaTeX errors, undefined citations,
  undefined references, undefined control sequences, and overfull boxes.
- Remaining warnings are underfull hboxes in narrow table/import rows.

## Recommended Next Step

If staying on Paper 2, the next content edit should be venue-specific appendix
proof polish or a true numerical orbit experiment if a venue asks for one.
Otherwise, shift to Paper 3's sign-convention/application appendix.  Venue
framing can wait until the content gap is smaller.
