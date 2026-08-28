# Paper 2 Execution Plan

## Phase 0: Current State

- Paper 1 response-theory has a single-PDF submission package and compiles.
- Paper 2 now has a standalone article draft with bibliography/provenance pass
  and seven technical appendix passes.
- Master `main.tex` remains the source ledger.

## Phase 1: Skeleton Hardening

Goal: make Paper 2's contribution visible in one theorem.

Tasks:

1. Keep the response theorem as an imported companion theorem.
2. State the finite-response prelimit data.
3. State effective coefficients and HJB operator.
4. State deterministic HJB convergence theorem.
5. State theta-expectation semigroup theorem.

Exit criteria:

- Paper 2 compiles independently.
- Paper 2 does not contain Paper 1 proofs or Paper 3 representations.

## Phase 2: Theorem Extraction

Goal: replace source-ledger placeholders with compressed theorem statements.

Tasks:

1. Extract `def:effective_hamiltonian_normalized`.
2. Extract `prop:coefficient_structure`.
3. Extract `lem:deterministic_residual_identity`.
4. Extract `prop:subsuper_residuals_full_branch`.
5. Extract `thm:main_homogenization`.
6. Extract nonconvexity, constructive example, and non-subadditivity.
7. Extract theta-expectation properties.

Exit criteria:

- Every main theorem statement has local definitions.
- Source line references are recorded in theorem inventory.

## Phase 3: Proof Extraction

Goal: provide a readable HJB/homogenization proof without duplicating Paper 1.

Tasks:

1. Write finite-response coefficient derivation.
2. Write corrector cancellation proof.
3. Write residual identity proof.
4. Write viscosity sub/supersolution proof.
5. Write comparison/uniqueness proof.
6. Write nonconvexity and non-subadditivity proof.

Exit criteria:

- Main HJB theorem has a complete proof.
- Paper 1 is cited only through its exported response theorem.

## Phase 4: Example

Goal: include one inspectable nonconvex billiard/port example.

Tasks:

1. Choose a simple finite-response port with explicit Taylor data.
2. Show how it deforms the billiard table/read-outs.
3. Compute the Hamiltonian defect producing nonconvexity.
4. Connect the defect to subadditivity failure.

Exit criteria:

- Example appears in main text.
- Referee can inspect the primitive port data.

## Phase 5: QA

Goal: prepare a realistic target-journal draft.

Tasks:

1. Compile twice. `[done]`
2. Run BibTeX and scan for undefined references/citations. `[done]`
3. Remove internal source-line and extraction terms from `main.tex`. `[done]`
4. Check page count. `[done: 9 pages]`
5. Verify no BSDE/Girsanov material is used as proof input. `[done]`
6. Produce a referee-risk memo or submission package checklist. `[done]`
7. Add first technical appendix for HJB proof details. `[done: 7 pages]`
8. Add second appendix pass for the exact prelimit action graph, branch
   residual constants, and concrete nonconvex parameter window. `[done: 9-page
   appendix]`
9. Add third appendix pass for endpoint/specular variation, recursive
   corrector closure, and doubled-variable comparison refinements. `[done:
   12-page appendix]`
10. Add fourth appendix pass for Green-Kubo correlation factorization,
    terminal-value stability, and concrete parameter-choice recipe. `[done:
    14-page appendix]`
11. Add fifth appendix pass for full branch residual checks. `[done:
    15-page appendix]`
12. Add sixth appendix pass for smooth approximation closure and a
    dimensionless parameter audit table. `[done: 17-page appendix]`
13. Add seventh appendix pass for a normalized numerical certificate and
    stability margin for the concrete nonconvex port. `[done: 18-page
    appendix]`
14. Continue content migration if treating Paper 2 as a flagship proof paper.
   `[open]`
