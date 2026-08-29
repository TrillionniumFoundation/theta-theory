# Retention decision: similarity Lorentz and four-branch moving seam

## Decision

Both result families remain mathematically useful and must be retained, but neither
should continue to compete with the new specular open-billiard candidate as the sole
physical flagship.

| Platform | Active-tree decision | v5 role |
| --- | --- | --- |
| `SL-SIM-v1` similarity Lorentz | **Retain in compact form** | Conjugate specular benchmark, exact response sanity check, and maximality/no-bypass theorem. |
| `FB4-EXACT-v1` four-branch moving seam | **Retain as a first-class benchmark** | Exact nonzero moving-partition response, all-order operator calculus, exact innovations, explicit pressure/covariance and CI oracle. |
| `OB3-MG-v1` moving open billiard | **Promote after integration and review** | Candidate physical flagship for response → physical clock → correlated rough limit → DPP → HJB. |

Historical source variants and large evidence trees remain only on
`archive/full-v4-pre-governance-2026-08-29`. Retention here means extracting one short,
current, theorem-scoped specification for each benchmark—not restoring the archived
version forest.

## Similarity Lorentz: why it is still useful

The similarity family preserves genuine specular dispersing Lorentz dynamics and can
start from a broad finite-horizon base table. Its normalized collision map is fixed,
while displacement and roof observables transform explicitly. This gives:

- an exact positive-control theorem for physical coefficient response;
- a clean benchmark for collision-to-physical-time normalization;
- access to correlated fixed-Lorentz rough limits and noncommuting slow vector fields;
- a regression test for signs, rotations, scaling powers and covariance conventions;
- the `SIMILARITY-MAXIMALITY` conclusion: exact global straight-line/specular
  conjugacy cannot be extended to general shape deformation.

That last item is strategically important: it proves that a general moving-obstacle
theorem cannot be obtained by searching for a broader coordinate trick.

### What is no longer justified

Similarity Lorentz must not be advertised as resolving a nonzero moving-singularity
operator source. In common coordinates the normalized collision map is fixed. It is a
conjugate benchmark, not the main answer to the old S1–S3 objection.

### Retained form

Keep only:

1. the exact conjugacy and coefficient formulas;
2. the all-order finite-dimensional chain rule;
3. the marked-period/scaling identities;
4. the maximality theorem and scope warning;
5. a small algebraic verifier.

Do not retain a separate versioned manuscript stack in the active tree.

## Four-branch moving seam: why it is still useful

The four-branch family remains the strongest exact benchmark for genuinely nonzero
moving partitions. It supplies, on one fully explicit operator family:

- moving seams and a nonzero saltus/source derivative;
- uniform regularity-loss bounds and product CM2;
- complete finite-difference convergence;
- arbitrary finite operator derivatives and repeated insertion formulas;
- exact predictable innovations under adaptive selectors;
- closed pressure, covariance and branch-roof formulas;
- tensor-product constructions in arbitrary finite dimension;
- a pointwise microscopic recursion that is easy to test mechanically.

These properties make it an unusually valuable theorem-interface and CI oracle. The
specular open-billiard route is physically stronger, but its geometry and analysis are
less suitable for exact symbolic regression tests.

### What is no longer justified

The four-branch platform must not be presented as a standard specular Lorentz gas or as
the sole physical realization of the full series. Its exact reset removes the long
correlation and nontrivial rough-area difficulties that the open-billiard flagship is
intended to retain.

### Retained form

Keep one canonical benchmark specification containing:

1. branch widths, seams and operator formula;
2. derivative and CM2 theorems;
3. exact-reset/innovation theorem;
4. pressure, covariance and roof formulas;
5. finite-dimensional verification code.

Move narrative duplication, old receipts and all versioned papers to the archive only.

## Placement in the five-paper series

### Paper I

- flagship: open-billiard geometric response and symbolic desingularization;
- `FB4-EXACT-v1`: exact all-order response benchmark;
- `SL-SIM-v1`: conjugate control and maximality theorem.

### Paper II

- flagship: actual open-billiard roof, physical-time coefficients and correlated rough
  data;
- `FB4-EXACT-v1`: exact pressure/full-frequency benchmark;
- `SL-SIM-v1`: scaling and normalization sanity check.

### Paper III

- flagship: correlated same-system microscopic DPP/HJB route;
- `FB4-EXACT-v1`: exact-innovation and explicit theta-recursion benchmark;
- `SL-SIM-v1`: optional fixed-fast-map homogenization example only.

Papers IV–V may reuse benchmark outputs only through named Paper III interfaces.

## Final retention rule

```yaml
similarity_lorentz:
  delete: false
  primary_platform: false
  retain_as: conjugate_benchmark_and_maximality_boundary

four_branch_moving_seam:
  delete: false
  primary_physical_platform: false
  retain_as: exact_nonzero_response_and_CI_benchmark

archived_version_forests:
  restore_to_active_tree: false
```
