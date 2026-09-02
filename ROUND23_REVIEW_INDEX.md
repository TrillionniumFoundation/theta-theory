# Round-Twenty-Three review index

**Revision branch:** `revision/round23-referee-positive-closure-11paper-2026-09-02`  
**Report answered:** `REFEREE_REPORT_ROUND22_GPT56_PRO_HARSH.md`  
**Point-by-point response:** `REFEREE_ROUND22_RESPONSE.md`  
**Historical derivation audit:** `ROUND23_HISTORICAL_DERIVATION_AUDIT.md`  
**Dependency order:** `ROUND23_PROOF_DEPENDENCY_LEDGER.md`  
**Explicit counterexample regressions:** `ROUND23_MATHEMATICAL_REGRESSIONS.md`

## Canonical source order

1. `papers/A1-exact-benchmarks/ROUND23_POSITIVE_CLOSURE.tex`
2. `papers/A2-sinai-homological-pressure/ROUND23_POSITIVE_CLOSURE.tex`
3. `papers/B2-collision-clusters-dynamic-ldp/ROUND23_POSITIVE_CLOSURE.tex` -- local grand-canonical forest part
4. `papers/A3-full-empirical-path-ldp/ROUND23_POSITIVE_CLOSURE.tex`
5. `papers/A4-history-memory-universal-pressure/ROUND23_POSITIVE_CLOSURE.tex`
6. `papers/B1-microcanonical-preparation/ROUND23_POSITIVE_CLOSURE.tex`
7. `papers/B2-collision-clusters-dynamic-ldp/ROUND23_POSITIVE_CLOSURE.tex` -- exact-number/global LDP part
8. `papers/B3-hamilton-boltzmann-cotangents/ROUND23_POSITIVE_CLOSURE.tex`
9. `papers/B4-nonlinear-kinetic-semigroups/ROUND23_POSITIVE_CLOSURE.tex`
10. `papers/C1-information-risk-sensitive-saddles/ROUND23_POSITIVE_CLOSURE.tex`
11. `papers/C2-cotangent-rigidity-tangent-representations/ROUND23_POSITIVE_CLOSURE.tex`
12. `papers/D1-deterministic-theta-contractions/ROUND23_POSITIVE_CLOSURE.tex`

B2 appears twice because its local rooted grand-canonical forest theorem is an upstream input to B1, while its exact-number/microcanonical corollary imports B1.  The source marks this split explicitly and does not use the later half in the earlier proof.

## Eight decisive report checks

- A4: no regular-point residue; exact Feshbach kernel; generic `z^{-1} PLQLP` term.
- B1: normalized reference law and explicit activity; `q_N(0,0)=0`.
- B3: collision defect `h=deltaGamma-DA_f[u]`; zero quadratic cost at `h=0`.
- C1: deterministic hidden Dirac kernels are not dominated; observations only are stratified/dominated.
- A3: ordered stopped word and physical path are state coordinates.
- A3: legal recovery kernels are absolutely continuous conditional reference laws.
- B4: superquadratic containment moment, excluding escaping-energy sequences.
- Downstream propagation: C2 and D1 use only the corrected interfaces.

## Build and verification entrypoints

```bash
python tools/activate_round23.py
python tools/verify_round23.py
```

The GitHub workflow `.github/workflows/verify-round23-referee-closure.yml` runs activation, the explicit mathematical regressions, clean builds of all eleven projects, content hashes, and a second fail-closed verification.  A generated `ROUND23_BUILD_MANIFEST.json` is evidence of that source/build run only; it is not external theorem validation.

## Referee reading recommendation

Read the point-by-point response first, then the eight decisive replacement sections identified above, then follow the dependency order.  Historical status files and older PDFs are retained for provenance but are not part of the Round-Twenty-Three proof claim.
