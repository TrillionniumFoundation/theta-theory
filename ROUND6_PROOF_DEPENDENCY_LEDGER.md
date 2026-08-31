# Round-six proof-dependency ledger

**Report branch:** `review/round5-gpt56-pro-harsh-11paper-2026-08-31`  
**Revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`

## Controlling non-circular order

```text
A1

A2  ->  A3  ->  A4  ->  C2
 |               |         |
 +---------------+-------> D1

B2-GC  ->  B1  ->  B2-MC  ->  B3  ->  B4  ->  C1
   |                                  |        |
   +----------------------------------+-----> C2
                                      |        |
                                      +------> D1
```

- **B2-GC** is the trace-regular grand-canonical actual-contact pressure and
  lower-bound theorem.  It does not use B1.
- **B1** conditions B2-GC at an exact finite-volume source-dependent saddle.
- **B2-MC** transfers the already proved grand-canonical joint LDP through B1.
- **B3** uses the B2 action and B1 initial covariance to construct the global
  gauge dual and exact-centred Gaussian process.
- **B4** constructs the kinetic action semigroup and full-BBGKY perturbed tests
  only after B2/B3.
- **C1** retains the complete posterior/history state and uses B2/B4 for its
  kinetic limit.
- **C2** uses A4 conditional kernels and B3 exact-centred Gaussian limits; it
  does not assume present-state Markovity at finite scale.
- **D1** is last.  It proves an abstract projective theorem from the finite
  pressures and exponential tightness already established upstream.  It does
  not assume an exposed-point density property.

## Paper gates

| Paper | Principal gate | New controlling labels |
|---|---|---|
| A1 | one graph-completed self-return section, full-port work, physical trace response | `lem:r6-a1-section`, `thm:r6-a1-suspension`, `prop:r6-a1-work`, `thm:r6-a1-response` |
| A2 | fixed ambient trace field, complete Dolgopyat estimate, correct window regimes | `lem:r6-a2-ambient`, `thm:r6-a2-spectrum`, `thm:r6-a2-dolgopyat`, `thm:r6-a2-master-llt` |
| A3 | explicit recession coordinate and rate-dense admissible Markov recovery | `lem:r6-a3-compact`, `lem:r6-a3-markov`, `thm:r6-a3-variational`, `thm:r6-a3-collision-ldp` |
| A4 | common Ray process, genuine Doob eigenfunction, zero-mode realization, conditional rough kernels | `thm:r6-a4-ray`, `thm:r6-a4-eigen`, `thm:r6-a4-decay`, `thm:r6-a4-conditional` |
| B1 | compound-Poisson characteristic theorem and exact finite saddle | `lem:r6-b1-poisson`, `thm:r6-b1-saddle`, `thm:r6-b1-characteristic`, `thm:r6-b1-coefficient` |
| B2 | trace-regular contact class, root-inclusive Gramian, future-preserving source theorem, GC/MC LDP | `lem:r6-b2-trace-class`, `lem:r6-b2-gramian`, `thm:r6-b2-cyclic`, `thm:r6-b2-gc-ldp`, `thm:r6-b2-mc-ldp` |
| B3 | local/global source separation, closed gauge, covariance cohomology, cumulant process CLT | `thm:r6-b3-duality`, `thm:r6-b3-gauge`, `thm:r6-b3-kernel`, `thm:r6-b3-gaussian` |
| B4 | genuine law-coordinate algebra, full triangular corrector, weak-energy compactness and comparison | `lem:r6-b4-algebra`, `thm:r6-b4-generator`, `thm:r6-b4-comparison`, `thm:r6-b4-limit` |
| C1 | observation-aware Bayes kernel, strategy DPP, Chernoff exponent, exact-centred LAN | `lem:r6-c1-bayes`, `thm:r6-c1-law`, `thm:r6-c1-testing`, `thm:r6-c1-lan` |
| C2 | coercive strict dual, complete-history likelihood, conditional kernels, one-Hilbert memory | `thm:r6-c2-strict`, `thm:r6-c2-optional`, `thm:r6-c2-girsanov`, `thm:r6-c2-memory` |
| D1 | finite-dimensional steep LDPs, projective passage, exact conditioning/contraction and likelihoods | `thm:r6-d1-projective`, `thm:r6-d1-conditioning`, `thm:r6-d1-interchange`, `thm:r6-d1-lan` |

## Fail-closed publication rules

`main` may be changed only if the exact revision commit satisfies all of the
following:

1. all eleven latest referee reports are present and inventoried;
2. every paper-level `main.tex` loads exactly one
   `ROUND6_POSITIVE_CLOSURE.tex`;
3. the controlling module is byte-identical to its registered round-six source
   and contains no ASCII control bytes;
4. every theorem-like environment has a proof and every local reference
   resolves inside the same paper;
5. counterexample-aware checks reject the superseded A1 core-work, A2
   zero-space/wide-window, A3 no-defect, A4 zero-free/orthogonality, B1 fake
   singleton block, B2 arbitrary-`L1` ledger, B3 one-domain/compensator, B4
   moment-topology/monotone-truncation, C1 KL-error/limiting-centre, C2
   noncoercive/present-state, and D1 P3/limiting-centre formulations;
6. the dependency graph above is acyclic;
7. all eleven papers clean-build with no undefined references or citations;
8. a fresh hostile rereview is run on the exact materialized bytes;
9. the pre-publication `main` ref is archived before `main` is moved;
10. a final tag and exact-source certificate identify the published commit.

Build success is necessary but is not treated as external journal acceptance.
