# General Theta Foundations I — Revision 92

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This revision continues the response to R60 at external commit `cf13712c54e9ef0c9c54a240b1f26efc78cc3568` and pipeline-audit commit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. These reports reviewed v90, not v91 or v92. Both are frozen verbatim. The immediate mathematical base is the already published v91 completion `ce2616a9f5d870d5cf4c8ee254a728544a0bea6a`, with native source `e7ea7aa87c77d79119fe9f4cad273ac97997089e`. Its results are inherited, not attributed to this revision as newly discovered. The ordered-measurement topic and four-leading-general-mathematics-journal objective are unchanged.

### Journal route

Start with `paper.pdf` and the single linked `BINARY_SUPPLEMENT.pdf`. The standalone journal package contains these two documents, their current source dependencies and `REPRODUCIBILITY.md`, not the historical audit corpus. `COMPLETE_REVISION.pdf` is the full research archive; `STRUCTURAL_PAPER.pdf` is the independent source-unchanged article. These are not additional premises of the quantitative paper.

The new Primary Section 18 (source module 85) gives an attained two-coordinate receiver-dimension hierarchy for arbitrary finite two-call experiments. The old register is counted after the first recorded receiver instrument; the fresh reference is counted during the second call. Initial references and temporary workspaces before that cut are not constrained. Mixed instruments are Kraus-refined into a classical record, and mixed fresh states are sampled into the record: a forbidden extra coherent purification is never used to satisfy a dimension bound.

The general optimum is a common-barycenter concave envelope over first Gram atoms of rank at most k and fresh Grams of rank at most ell. The primal, universal-majorant dual and finite maximizing realization are attained; at most rank(rho)^2 first-receiver outcomes per first label and final retained dimension k*ell suffice. This includes arbitrary fixed-pair decision problems without asserting strict gaps in all of them.

For the fixed finite shared-basis family, put r=min(k,ell) and L=2(d+1)-t^2. The exact successes are

```
biased prior: (d+1)/L + t^2(r-1)/(2rL)
equal prior: 1/2 + t^2(dr-1)/(2dr(d+1)).
```

Cyclic rank-r compression instruments attain these values. Every increase of the smaller threshold gives an exact positive increment for t>0. The proof includes mixed inputs, receiver feedback, countable records, null histories and closure limits. At d=2,r=1 the centered-swap equality has an exceptional family; the manuscript and checker explicitly retain it. Saturation is the full reset value, not the all-adaptive value. The initial first-call reference in the attaining construction has dimension d; these are recording-cut dimensions, not an all-times workspace bound.

### Preservation and R60 response

The 792 v91 native files and all active predecessor proof sections are preserved; changed editorial/build files have exact `predecessor-v91-audit/` copies. The v91 general variational and classical-envelope theorems, biased/equal-prior triples, quantitative contact defects and near-optimal Gram rigidity remain active. The earlier fixed-tube support/covariance geometry, profile V, hard Q, finite remainder terms and common readouts are unchanged. No old mathematical section is edited or removed.

`RESPONSE_TO_REFEREE.md` covers R01–R15 and D01–D30 with printed primary sections first. `PROOF_AUDIT.md`, `HISTORY_AND_PIPELINE_AUDIT.md` and `INTERNAL_MATHEMATICAL_REVIEW.md` are current v92 records; their old versions remain in the archive. `PIPELINE_DERIVATION_V92.md` records the additional dependency chain. `LITERATURE_AUDIT.md` compares the actual recording cuts to the primary sources of Ohst et al. and Zonnios–Binder. Independent human priority review remains outstanding.

### Reproduction

```sh
python build_revision.py --check-source
python rank_hierarchy_check.py
python -O rank_hierarchy_check.py
python build_revision.py --isolated
python build_revision.py --verify-published
```

The production build runs 34 suites in both Python modes and reconstructs both complete native sources and the standalone journal package. Actual source/publication identities and results are recorded in the generated evidence, not asserted by this README. A separate read-only workflow verifies the exact final submitted SHA without changing its files. No independent human authorship signature, priority clearance, hardware reset calibration or whole-Theta analytic closure is inferred from that run.
