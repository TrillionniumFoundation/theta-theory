# General Theta Foundations I — Revision 95

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

The controlling report is v90/R60, external commit `cf13712c54e9ef0c9c54a240b1f26efc78cc3568` and pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Their frozen texts are unchanged. The immediate source baseline is v94 at remote head `db6739da3487be8787a67fc175b9086bd62f0e80`, native commit `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`, publication `0919ff61895716ea3de1d6a0f2a6a291935764d0`. No report on v91–v94 was found in the branch survey. These are observed predecessor identities, not identities of this local revision.

### New mathematical result

Printed Primary Section 21 solves the equal-prior, fixed-pure-initial-acquisition problem for the complete reset class with old receiver dimension at most two and any fresh reference dimension at least two. Put `q=max(lambda_max(rho),1/2)` and `v=4q(1-q)`. The exact value is

```
P_(2,ell)^eq(rho) = 1/2 + t^2 psi_d(v)/(2d(d+1)),
psi_d(v) = d-1 + (2d-1)v/[2(d-1+d sqrt((d(d-2)+(2d-1)v)/(d^2-1)))].
```

The upper covers every legal mixed, feedback, countably branching and limiting protocol with the prescribed initial pure acquisition. At most d commuting rank-two atoms give an attaining physical recorded instrument. A fresh reference of dimension two suffices, irrespective of the larger allowed dimension. The optimal fresh weights are explicit and generally nonuniform.

For qubits the restriction on the old receiver loses no effective Schmidt dimension: every initial density matrix is covered. With `u=sqrt(det(rho))` the value is

```
1/2 + (t^2/12) [1+6u^2/(1+4u)].
```

No nontrivial recorded receiver instrument or message is needed in this qubit case. The result supplies the exact loss from the rank-two optimum and a calibrated upper bound on the initial largest eigenvalue. It does not identify the equal-prior value for an old receiver of arbitrary larger dimension.

### Reading route

Start with `paper.pdf` / `quantitative.tex` and its new Section 21. The one linked `BINARY_SUPPLEMENT.pdf` / `supplement.tex` supplies all current auxiliary proofs. `REPRODUCIBILITY.md` is the short submission note. `RESPONSE_TO_REFEREE.md` answers every R01–R15 and D01–D30. The complete research edition and independent structural article remain archival/independent objects, not additional premises or significance claims.

The source modules through 87 and all prior active labels are retained. Current audits replace their predecessor versions only after exact copies are retained under `predecessor-v94-audit/`. The v94 general spectral-envelope lemma is explicitly credited as an inherited premise; the centered-swap leaf, its closed formula and its operational consequences are new here.

### Verification

```
python build_revision.py --check-source
python equal_prior_initial_check.py
python -O equal_prior_initial_check.py
python equal_prior_initial.py examples/equal-prior-initial.json --bits 80
python build_revision.py --isolated
python build_revision.py --verify-published
```

Production verification requires an actual source Git commit and runs all 37 suites normally and optimized, reconstructs the whole source archive, and rebuilds the two-document journal package. Finite tests and rendered-page identities are not continuum proofs. Read the emitted diagnostics rather than assuming absence of warnings.

### Delivery identity

This revision was authored and verified locally. The active GitHub connector exposed reads but no write actions, and direct network access was unavailable. No v95 remote branch, push, Actions check, legacy status or human signature is claimed. Build receipts identify actual local Git objects; applying the source to a remote-backed checkout requires a new native commit and a fresh build. Independent human specialist priority clearance remains unobtained. The journal objective is unchanged, and no journal acceptance is claimed.

Use the root `apply_revision95.py` with the accompanying native archive to apply this exact source on the pinned remote base. That script stages only the new paper directory and uses a new non-force branch. It pushes the native source before typesetting when explicitly invoked with `--push`; it must then generate new publication evidence bound to that actual commit. Inherited `publish_revision.py` is historical and is not the v95 delivery entry point.
