# Theta-Theory — eleven-paper external-review tree

The default branch contains the current eleven manuscript sources, their paper-level referee material, and the minimal build metadata. Historical manuscript series, cumulative derivations, proof-audit bundles, generated PDFs, migration payloads, and candidate trees are preserved on archive/review/series branches and are not controlling sources on `main`.

## Papers

1. `papers/A1-exact-benchmarks`
2. `papers/A2-sinai-homological-pressure`
3. `papers/A3-full-empirical-path-ldp`
4. `papers/A4-history-memory-universal-pressure`
5. `papers/B1-microcanonical-preparation`
6. `papers/B2-collision-clusters-dynamic-ldp`
7. `papers/B3-hamilton-boltzmann-cotangents`
8. `papers/B4-nonlinear-kinetic-semigroups`
9. `papers/C1-information-risk-sensitive-saddles`
10. `papers/C2-cotangent-rigidity-tangent-representations`
11. `papers/D1-deterministic-theta-contractions`

Each paper folder contains:

- one controlling `main.tex`;
- one `references.bib`;
- `README.md` and `REFEREE_GUIDE.md`;
- the original `REFEREE_REPORT.md`; and
- the independent `REFEREE_REPORT_GPT56_PRO.md`.

Series-level review indexes are stored at:

- `papers/REFEREE_REPORTS_INDEX.md`
- `papers/GPT56_PRO_REFEREE_REPORTS_INDEX.md`

Generated PDFs and LaTeX build products are intentionally untracked.

## Build

```bash
make all
```

The eleven source manuscripts were reconstructed from the SHA-256-pinned clean source package, structurally audited, and compiled successfully before promotion. The manuscripts remain research drafts; successful compilation is not a mathematical correctness certificate.

## Referee round-two revision branch

On `revision/referee-round-positive-closure-11paper-2026-08-30`, all eleven controlling manuscripts include a positive-closure addendum. The exact branch head, build result, and external rereview status are recorded in `REVISION_STATUS.md`.
