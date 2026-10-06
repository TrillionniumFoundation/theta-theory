# General Theta Foundations I — Revision 91

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This revision responds to the v90/R60 external report at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568` and the companion proof/pipeline audit at `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Both reports are frozen verbatim. The mathematical predecessor is the reviewed v90 head `906e6e12841816f07e4ca31137690fd18bb65853`. The ordered-measurement topic and four-leading-general-mathematics-journal objective are unchanged.

### Start here

Read `paper.pdf` and its linked `BINARY_SUPPLEMENT.pdf`. The primary's new Section 15 gives a general reset variational principle and an attained dual; Section 16 retains the earlier exact biased-prior hierarchy; Section 17 proves the equal-prior hierarchy. Printed numbering takes precedence over the archival source-module indices 83, 82 and 84. Exact theorem/page locations are generated in `evidence/THEOREM_LOCATIONS.json`.

For any finite two-call ordered-measurement decision experiment, with arbitrary priors and rewards, the optimal unit-reset value is the maximum, over one common density matrix, of a sum of upper concave envelopes. It is attained using at most `rank(rho)^2` receiver-instrument outcomes per first device label and quantum receiver dimension at most `d_1*d_2`, separate from the finite classical record. Hermitian majorants yield an attained dual and contact conditions. This is an exact value characterization, including fixed-pair problems, not a claim that every pair has a strict resource advantage.

For the finite shared-basis experiment with equal hypothesis priors, the exact three-class values are

```
P_ca    = 1/2 + t^2(d-1)/(2d(d+1)),
P_reset = 1/2 + t^2(d-1)/(2d^2),
P_all   = 1/2 + t^2/(2d).
```

They give `7/12 < 5/8 < 3/4` for the seven qubit devices at `t=1`. The old `3/5 < 13/20 < 4/5` theorem is retained, not replaced. Both proofs bound the complete intended strategy classes and exhibit attainments. The same hidden device is selected once for both calls; independent redraws erase the signal. The equal-prior theorem and a channel/prior/law perturbation neighborhood remove reliance on a specially tuned prior.

### Preservation and review

The fixed-tube support/covariance trichotomy, allocation second moment `V`, hard policy budget `Q`, finite remainders, common readouts and structural article remain active. Every preceding native file is retained at its original path, with an exact predecessor copy when a current file changes. Only registered additive paragraphs alter the old hierarchy module. Stale current audit headings are replaced by v91 audits; the old audits remain under `predecessor-v90-audit/`. No unrelated paper or review branch is modified.

`RESPONSE_TO_REFEREE.md` addresses R01–R15 and D01–D30. `PROOF_AUDIT.md`, `HISTORY_AND_PIPELINE_AUDIT.md`, `INTERNAL_MATHEMATICAL_REVIEW.md` and `LITERATURE_AUDIT.md` are current v91 records. Independent human priority assessment remains outstanding and is not inferred from these documents.

```sh
python build_revision.py --check-source
python reset_variational_check.py
python equal_prior_check.py
python build_revision.py --isolated
python build_revision.py --verify-published
```

Production qualification is the actual source-bound build receipt, not this README. It executes all 33 suites normally and under `python -O`, reconstructs the native archive and reconstructs the standalone primary/supplement package. The final-head receipt is kept outside the exact commit it verifies. `STRUCTURAL_PAPER.pdf` and `COMPLETE_REVISION.pdf` belong to the research archive, not the initial journal package.


## General classical-versus-quantum receiver criterion

Primary Section 15 additionally proves Theorem `classicalroof91`: complete classical readout is exactly the same common-barycenter problem with atoms restricted to rank-one density matrices. A complete first measurement can be spectrally refined without loss, and a rank-one Gram factor carries only a known receiver state; these give both operational directions. Compact graph convexification and the same strictly feasible hypograph dual give attained classical primal and dual optima. Corollary `gapcertificate91` then gives necessary and sufficient certificates of a strict retained-receiver advantage, and all-density dual contacts characterize equality. This extends the R60 breadth response to an exact general comparison criterion, not merely an evaluated example.

The finite receiver dimensions refer to retained registers at the recording cuts, not to all temporary workspaces of a selected implementation of an instrument. The dual majorizations remain universal requirements and are not checked by sampling.


## R60 completion: quantitative optimality and normalization

The already landed v91 native source at `d28546aad99cd1ce3846ca74ccedb90c24ebd37b` is preserved by `STAGED_V91_BASELINE.json` and `staged-v91-audit/`. Its existing general variational theorem, classical pure-atom criterion, and both exact hierarchies remain active. The completion adds Corollary `contactdefect91` in Primary Section 15 and Lemma `stableswap91` / Corollary `resetstability91` in Primary Section 17. Printed numbers and pages are generated from the actual manuscript, not inferred from source-module numbers.

The general defect identity separates spectral slack, all-density majorization slack and leaf optimization loss, each nonnegative. The stable centered-swap equality bounds the squared trace distances of both normalized Gram factors from the scalar density by `K_d Delta`, with `c_d=d-1-1/d` and `K_d=d(1+9/(2c_d))`. The proof keeps the two nonnegative defects `1-f^2` and `tr(ab)-f^2/d` and handles singular states using a unitary extension of the polar factor. Summation over the complete reset normal form gives weighted near-optimal rigidity at the explicit relative scale `epsilon/t^2`. Gram weights, actual history probabilities, uniqueness of dilations and physical reset calibration are explicitly distinguished.

The normal-form text also gives an explicit direct-sum realization of public seeds and distinguishes implemented protocols from abstract norm-closure limits. This does not narrow the optimized class: general seed laws and tester limits retain their continuous values, and the finite maximizing realization still attains the full class optimum. The added `rigidity_check.py` has exact diagonal, singular, complex noncommuting, dual-defect and normalization fixtures; no finite check replaces a universal proof. There are now 33 production regression suites, with actual execution status recorded only in the build receipt.
