# A2 v7 — critical boundary experiments

The current article is `main.tex`: **Relative boundary laws and statistical reconstruction in periodic dispersing billiards**, Qian Qi, September 9, 2026. The observed clean build has 72 pages. The independent `two_collision.tex` companion has 7 pages and its source is unchanged.

This directory is based on the **complete** remote v6 manuscript tree `50f7fdb275a23d7a74234f4e1347c4934be8b8b8`, reviewed at author commit `4ca186258c92dcbc75accc4eb576e307cc612189`. The controlling independent report is pinned at `f1728f5d96ea01b1326daf9a6a36352b2e270be1` and copied verbatim in `review-basis-v6/`. Historical v2–v6 source, proof chapters, reports, tools, and the companion are retained. The old repository directories are not modified.

## Entry points for renewed review

`RESPONSE_TO_REFEREE_V7.md` addresses V6-R1–R4 point by point. `PROOF_LEDGER_V7.md` gives theorem dependencies and observation assumptions. `SOURCE_PINS_V7.json` fixes input identities and edited-source blob hashes. `VERIFICATION_V7.json` distinguishes printed proofs, local finite diagnostics, actual clean compilation, and page inspection from remote CI or formal verification.

The new mathematical files are `v7/10_critical_experiments.tex`, `v7/20_measurable_reconstruction.tex`, `v7/30_count_lower_bounds.tex`, and `v7/40_fixed_bracket_acquisition.tex`. The introduction's observation table and statistical framing are in `v7/00_scope.tex`.

The new main results are Theorems 7.1 and 7.3 (unequal-contact support overlap and the actual positive-offset joint experiment limit), Lemma 8.1 (Borel compact reconstruction), Theorem 20.2 (physical binary-count lower bound), and Theorem 21.2 (count-only reconstruction from a fixed local bracket with capped waits). Their assumptions and asymptotic regimes are not interchangeable.

## Reproduce locally

A Python 3 environment with SymPy, SciPy, and NumPy is needed for all three diagnostic suites. A TeX distribution providing `latexmk`, `pdflatex`, AMS packages, Latin Modern, microtype, xr-hyper, longtable, and booktabs is needed for the PDFs.

```sh
python tools-v7/verify_revision.py --output verification-v7/v7_normal.json
python -O tools-v7/verify_revision.py --output verification-v7/v7_optimized.json
cmp verification-v7/v7_normal.json verification-v7/v7_optimized.json
python review-basis-v6/independent_checks.py --output verification-v7/referee_normal.json
python -O review-basis-v6/independent_checks.py --output verification-v7/referee_optimized.json
cmp verification-v7/referee_normal.json verification-v7/referee_optimized.json
python tools-v6/verify_revision.py > verification-v7/v6_author_normal.json
python -O tools-v6/verify_revision.py > verification-v7/v6_author_optimized.json
cmp verification-v7/v6_author_normal.json verification-v7/v6_author_optimized.json
python tools-v7/build.py
```

`tools-v7/build.py` starts from empty auxiliary state in a temporary directory and builds the companion before the cross-referencing article. It writes `main.pdf`, `two_collision.pdf`, and build evidence under `verification-v7/`. Compiled PDFs and full local run outputs are supplied in the portable revision packet; the GitHub revision's controlling deliverable is the complete buildable source tree and its compact verification record. The portable packet contains the active standalone build and audited support material, not the whole repository.

The observed finite counts are 134 new v7 checks, 190 unchanged referee checks, and 147 unchanged v6 author checks; normal and optimized outputs match in the recorded environment. These are not proof certificates, interval calculations, global billiard simulations, or a claim of journal acceptance. Read the theorem proofs and the explicit limitations in the verification record.
