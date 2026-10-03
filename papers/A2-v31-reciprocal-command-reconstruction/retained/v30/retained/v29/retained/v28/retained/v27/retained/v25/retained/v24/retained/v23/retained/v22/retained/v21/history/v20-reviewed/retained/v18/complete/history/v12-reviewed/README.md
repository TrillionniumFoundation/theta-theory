# A2 v12 — Nonlinear boundary laws and two-contact rigidity

Complete English revision by Qian Qi, September 10, 2026, responding to the independent v11 report at `bcde40b514e4dc00a3252f2d0710002a2caeac7b`.

## Read the revision

Compile `main.tex` for the complete 117-page article, including every inherited active proof and the reorganized appendices. Compile `two_collision.tex` for the unchanged 7-page companion. `RESPONSE_TO_REFEREES.md` answers the report point by point. `PROOF_LEDGER.md` identifies the precise new statements and their dependencies.

The main geometric addition is Theorem 9.1: a block-triangular inverse for two independent even contacts, including coincident curvatures. Theorems 10.1 and 10.3 give independent physical realization at fixed leading data and fixed-window binary observation with physical alternatives. The main general-profile addition is Section 13: the integrated-flux two-derivative gain, higher-order positive-node acquisition and smooth-class self-calibration with sufficient accuracy power `2+6/(m-1/2)+gamma_+/|log(tau)|`. The referee's contribution to this quantitative improvement is credited explicitly.

The general relative law still assumes neither symmetry nor finite horizon. Evenness and supplied separate contact curvatures are hypotheses of the geometric graph inverse only. The full-profile experiment retains its supplied labels, boxes, collars and regularity/convergence certificates. Its rates are sufficient bounds, not full-profile minimax claims.

## Build and check

With Python 3, SymPy and a TeX installation containing `latexmk`, `pdflatex`, AMS packages, `lmodern`, `microtype`, `mathtools`, `mathrsfs`, `geometry`, `longtable`, `booktabs`, `xr-hyper` and `hyperref`:

```sh
python tools/build.py
python tools/run_all_checks.py
python tools/verify_v12.py --output verification/v12.normal.json
python -O tools/verify_v12.py --output verification/v12.optimized.json
cmp verification/v12.normal.json verification/v12.optimized.json
```

The clean build produces `main.pdf` and `two_collision.pdf`. The suite runner reproduces inherited diagnostics in a disposable copy with the pinned v11 main/introduction/bibliography, then verifies current v12 content and retention independently of narrative order. In a full repository checkout, the two required historical diagnostic inputs are authenticated and decoded from the retained `.publication/a2-v9` payload; the delivery archive also includes their uncompressed copies. No network or repository mutation is needed. Raw logs and detailed outputs are generated under `verification/` and accompany the delivery archive.

The reviewed native tree had 110 files. All 192 inherited active theorem/lemma/proposition/corollary/proof environments remain typeset and byte-identical; the current total is 212. Original v11 front matter and tooling are archived under `history/v11-reviewed`, and the answered report under `history/v11-referee`. Source retention is not proof certification.

## Source identity

The author source is `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`, manuscript tree `35a9fad03d7f1ee41f2c8661ee3c7aa58047bbad`. The revision is published on the new branch `revision/a2-v12-two-contact-rigidity-2026-09-10` as a descendant of the v11 review commit. Earlier manuscript and review directories are unchanged. See `SOURCE_PINS.json`, `HISTORICAL_DERIVATION_AUDIT.md` and `VERIFICATION.json` for the source checks, actual local verification and its limitations.
