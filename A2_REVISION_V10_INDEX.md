# A2 v10 — observable boundary profiles

Revision branch: `revision/a2-v10-observable-boundary-profiles-2026-09-10`.

The current full English manuscript is [main.tex](papers/A2-v10-observable-boundary-profiles/main.tex). Its complete native source is in [the v10 directory](papers/A2-v10-observable-boundary-profiles). It needs no source restoration before reading or compilation.

## Source and review identity

The revision responds to [the completed-v9 referee report](reviews/a2-v9-nonlinear-compatibility-harsh-2026-09-10/REFEREE_REPORT.md) at `b756f4851669e34c7074ba61b5bcf48689756406`, on which this branch is based. The reviewed author source is `33ef794a398b23015651482e93be7667c08d6fad`. The parallel v9 initialization is not the manuscript revised here.

The new paper contains 104 native source and documentation files. Its Git tree is `452a9003b03ff8f6eed47e1f609a36a054271455`, independently matched to the locally built source. No pre-existing paper, history or review path is replaced or deleted.

## Referee entry points

[Response to E1–E4](papers/A2-v10-observable-boundary-profiles/RESPONSE_TO_REFEREES.md) gives the point-by-point changes. [Proof ledger](papers/A2-v10-observable-boundary-profiles/PROOF_LEDGER.md) gives the hypotheses and proof chain for Theorem 11.1 and Corollary 11.2. [Verification summary](papers/A2-v10-observable-boundary-profiles/VERIFICATION.json) records the actual local runs and PDF identities.

Section 10 adds the focused deautoconvolution comparison. Section 11 proves finite-preparation recovery of both full normalized boundary energy profiles from two oriented even-flight binary experiments, with an explicit sufficient preparation budget accounting for rare-event probability. The Section 1 table separates labelled full-profile observation from exact-family unlabelled inversion and the smooth nuisance envelope. The closing paragraph of Section 9 distinguishes reconstruction from odd-law validation.

All 168 completed-v9 formal statement and proof environments are retained byte for byte; the new article has 176. The full article builds to 97 pages and the unchanged companion to seven pages. The 249, 407 and new 223 finite-check suites pass in normal and optimized Python with per-suite byte-identical output. Their overlapping checks are not formal proof certificates or evidence of remote CI.

## Reproduction

```bash
cd papers/A2-v10-observable-boundary-profiles
python3 tools/build.py
python3 tools/verify_v10.py
python3 tools/run_all_checks.py
```

Requirements and historical diagnostic input resolution are explained in the [README](papers/A2-v10-observable-boundary-profiles/README.md). The native branch stores TeX sources and build instructions; the compiled PDFs and raw local logs are supplied in the accompanying revision packet. No successful remote workflow or journal acceptance is claimed.
