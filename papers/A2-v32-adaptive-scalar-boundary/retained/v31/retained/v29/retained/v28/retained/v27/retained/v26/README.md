# A2 v26 — collision-generated geometry and whole-table certification

Qian Qi · 3 October 2026

Primary manuscript: **Reference-free certification from intrinsic boundary laws**, `main.tex` (18 pages in the actual local build). The controlling report is the v25 assessment at `aec09874d30f06dcbac1d1b7858fe96364f9d8d7`, reviewing `7151ddcd8b29516a8a6f8fa5043b97c49206b3ae`.

This revision completes and strengthens the pre-existing six-chapter mathematical checkpoint `61d75febcbc46e14573129985bb54a26979e4afb`. All six mathematical chapters remain byte-identical and active. The added Chapter 3 proves compensated support reconstruction under the same C6,beta prior. It does not replace any earlier theorem by a weaker one.

## Referee reading route

Definition 1.1 lists the directed numerical priors. Theorems 1.2–1.4 establish collision-generated confidence geometry, finite bridge recognition and whole-table certification. The apparatus uses independently resettable spatial launches, calibrated times and localized impacts; it receives no boundary-height, derivative, arclength, body-identity, period or distance-to-solid query. Its local range covers complete nearby bodies, not merely an infinitesimal contact patch. It is not a passive trajectory or count-only sensor.

The new Lemma 3.1 and Theorem 3.2 use the signed kernel `(4 phi_h-phi_(2h))/3`, whose moments through degree three cancel. The C2 error is bounded by `2 C_phi e h^(-2)+B6 h^4`. Positive curvature radius is proved separately, so signed averaging is not mistakenly assumed to preserve convexity. The auxiliary launch budget improves from `C nu^(-3/2) log(C/(nu zeta))` to `C nu^(-3/4) log(C/(nu zeta))`, with localization tolerance at most `c nu^(3/2)`.

Corollary 3.3 reduces cumulative launch work through epoch m from order `m^(11/2) log m` to `m^(19/4) log m`, retaining the same certificate, accuracy and stopping tail. The choice `a >= 6` still gives finite expected launch work. Constants depend on the declared priors; arithmetic, localization work, travel and setup are not part of the launch count.

Theorem 5.2 uses the normalized intrinsic endpoint laws and a positive completion-defect gap to exclude missing types and unsaturated observed period subgroups. Section 6 refreshes every provisional classification from retained raw proposals. Section 7 distinguishes the sensors and verifies the closest travelling-time comparisons. Two windows are two growing two-dimensional histograms, not two scalar measurements.

## Preservation

`retained/v25` is the exact reviewed v25 paper tree `c48d900f6596eea1e8df1f729481674fb1bf6175`, including all nested history. `complete` remains the original tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. The six preserved v26 core files have native tree `47f95eb3ad8d9d20b71d017ecb431bf1c0e0583b`. The new primary proofs are self-contained. Older analytic, local-probe, moment, count-fiber and relative-law conclusions remain available in the retained volumes with their original scope.

`RESPONSE_TO_REFEREES.md` maps the report's requests to the manuscript. `MATHEMATICAL_SOURCE_PINS.json` binds the published mathematical files. No earlier paper path, review branch or unfinished v26 branch is overwritten. The topic and requested mathematical-journal target are retained; no editorial outcome is asserted.

## Actual verification and delivery limitation

The local primary passed **7,453 finite assertions**, with identical ordinary and optimized Python output. The 18-page PDF compiled without final TeX warnings, undefined references or overfull/underfull boxes. All pages were rendered and inspected. This was source-content execution from a SHA-bound native archive plus the new local files, not a Git checkout or physical experiment.

**The GitHub write containing the two new validation scripts was blocked before execution.** That blocked action was not retried through another route. The scripts and actual local logs are supplied in the accompanying downloadable source package, but are not installed on this remote branch. The current read-only workflow therefore archives native sources only and explicitly records that no full-package qualification has occurred. The earlier v25 hosted success and the v26 source-archive run are not v26 full-build evidence.

The supplied package includes `tools/verify_v26.py`, `tools/validate_v26.py`, their exact source manifest, and the actual `verification/local` receipt. Its primary-only command is `python3 tools/validate_v26.py`; full qualification requires installation of these files and an actual exact-SHA checkout running `python3 tools/validate_v26.py --all-volumes --require-checkout`. `DELIVERY_STATUS.md` records the current boundary.

Finite diagnostics and compilation are not independent proof certification, literature-priority evidence or a journal decision.
