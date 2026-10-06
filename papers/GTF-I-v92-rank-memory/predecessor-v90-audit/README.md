# General Theta Foundations I — Revision 90

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This is the completed response to R59. The controlling external report is pinned at `a7d030d635a2bb40c8b4f7f2265df877bad95492`; its companion proof/pipeline audit is pinned at `994c41dbeec1da13b6b6486876855fa30ad7cfd5`. Both are frozen verbatim in this directory. The reviewed v89 is `df7ed618813224b058b97c6cbda720ad936e2c53`. The paper topic and four-leading-general-mathematics-journal objective are unchanged.

### Mathematical contribution and reading route

The primary retains the fixed-tube discrimination trichotomy, the complete profile second moment `V=sum n_r^2`, and the hard reset-policy square budget `Q`. Its new Section 82 proves a finite-ensemble operational separation, not merely strict inclusion of tester sets. For a once-selected basis device, input dimension `d>=2`, deformation `0<=t<=1`, and `L=2(d+1)-t^2`, the three exact optimal Bayes values are

```
classical complete-measure-and-reprepare: (d+1)/L
unit reset, unrestricted receiver:       (d+1)/L+t^2(d-1)/(2dL)
all two-call adaptive protocols:         (d+1+t^2)/L.
```

The qubit instance gives `3/5 < 13/20 < 4/5`. The upper for unit reset includes arbitrary receiver instruments and classical feedback. A filtered-swap identity, with its exact equality condition, proves the upper; independent maximally entangled pairs attain it. The all-adaptive upper now has a direct circuit-to-tester derivation of positivity, complement positivity and causal marginals. A first-moment identity explains why a single call, or independently redrawing the alternative each call, cannot supply the same signal.

Read `paper.pdf` / `quantitative.tex` first; `BINARY_SUPPLEMENT.pdf` / `supplement.tex` contains the linked current dependency proofs and preserved auxiliary consequences. `STRUCTURAL_PAPER.pdf` / `structural.tex` is the source-unchanged independent structural article. `COMPLETE_REVISION.pdf` / `main.tex` is the complete research archive, not a second submission. `RESPONSE_TO_REFEREE.md` answers R01–R15 and D01–D30; `PIPELINE_DERIVATION_V90.md` gives the proof chain, and `LITERATURE_AUDIT.md` records the primary-source comparisons.

### Preservation and verification

All 710 predecessor native files are preserved at their active paths or in the byte-identical `predecessor-v89-audit` records. All 998 predecessor complete-edition labels remain active. The earlier mathematical sections retain their complete text, with only registered additive convention paragraphs; relocating auxiliary sections to the linked supplement does not delete them. `staged-v90-audit` preserves the exact v90 staging files subsequently refined during completion.

```sh
python build_revision.py --check-source
python memory_check.py
python budget_domain_check.py
python build_revision.py --preflight         # local check, not publication qualification
python build_revision.py --isolated          # run at the exact native-source Git commit
python build_revision.py --verify-published  # read-only publication/final-head reconstruction
```

The production build runs all 30 regression suites normally and under `python -O`, reconstructs the complete native archive, and rebuilds the standalone journal package. Exact source, page and artifact identities are in `evidence/BUILD_RECEIPT.json` and its linked manifests. The root final-head request is only a request; only the separately observed read-only Actions receipt qualifies the exact final SHA.

The finite game is a binary decision on a finite ensemble with a shared hidden device index across its two uses. It is not an arbitrary fixed-pair theorem or a complete ancillary-memory-dimension hierarchy. Fixed-tube constants are still fixed-object dependent. Regression and reconstruction do not certify mathematical originality, physical reset calibration, independent human review, or the separate A2/B4/C2/eleven-paper/whole-program analytic closures.
