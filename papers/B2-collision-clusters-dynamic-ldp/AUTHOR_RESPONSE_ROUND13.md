# Author response — Round Thirteen — B2-collision-clusters-dynamic-ldp

**Referee report:** `papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND12_GPT56_PRO.md`  
**Locked report tree:** `0b58d25307d28a9f06313aea4ef32c4d6e58c16e`  
**Controlling proof source:** `revision/round13-referee-final/B2_GLOBAL_TRAJECTORY_CLUSTER_LDP.tex`  
**Objections addressed: 8/8**

There is no approximate mesh sewing.  Fixed-horizon genealogies are dominated by one factorial majorant; each cyclic genealogy is treated by its true Jacobi map and removed by dominated convergence.

## Objection-to-proof map

### 1. Dominated convergence does not give the stated linear-in-block-length modulus

Resolved in: `thm:r13-b2-pressure`.

### 2. Without the factor \(h\), the sewing theorem does not close

Resolved in: `thm:r13-b2-pressure`.

### 3. Nonvanishing of the physical Jacobi determinant is not proved for every genealogy

Resolved in: `lem:r13-b2-jacobi`.

### 4. The genealogy sum requires a uniform majorant that is not constructed

Resolved in: `lem:r13-b2-majorant`, `thm:r13-b2-cycles`.

### 5. The trace graph does not automatically possess all iterated traces used later

Resolved in: `thm:r13-b2-trace`.

### 6. The kinetic Hodge repair is not a proved right inverse for the nonlinear balance complex

Resolved in: `thm:r13-b2-ldp`.

### 7. Local analytic pressure does not by itself give the global rate

Resolved in: `thm:r13-b2-pressure`, `thm:r13-b2-ldp`.

### 8. The microcanonical statement is invalid independently through B1

Resolved in: `thm:r13-b2-micro`.

## Scope

The response preserves the paper and its positive theorem program.  The superseded mechanism is not used in the controlling source.  Repository verification establishes source identity, proof-structure coverage, regression checks, and reproducible compilation; external mathematical review remains separate.
