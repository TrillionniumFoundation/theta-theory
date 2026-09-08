# A1 v35 — clustered spectra and native two-volume revision

**Attainable information and causal compression at exponent collisions**  
Qian Qi — 8 September 2026.

Revision branch: `revision/a1-english-v35-spectrum-native-2026-09-08`.  
Controlling review: `review/a1-english-v34-harsh-independent-2026-09-08`, commit `a177077ede2b64e11af1efb016eaa6bb5ddf2a13`.  
Reviewed manuscript: `03a4788efb3cf643bc2cd60257c5ed290bb0570d`.

## Manuscript and response

`main.tex` is the complete English article; `companions.tex` is the complete companion. The principal collision-uniform, every-integer-budget theorem, its acquired tangent, positive-mass confluent flags, global covers, and common causal realization are retained. The finite-cell, purification, compatibility, precision and exact-example results remain active.

The current article has **42 pages**, and the complete companion **159 pages**, in the recorded native build. The reviewed v34 article was independently built in the same preparation session: **39 pages** plus **159 pages**. Neither count is inferred from the historical v33 build.

Read `RESPONSE_TO_REFEREE_V35.md` for R34.1–R34.3 and `PROOF_LEDGER_V35.md` for the dependency and preservation map. The new mathematical comparison is in `v35/spectral_comparison.tex`: Proposition 13.1, Corollaries 13.2–13.3 and Remark 13.4. It compares the entire clustered spectrum and superresolution minimax results with the acquired prediction problem, with parameters and resources kept distinct.

This directory is based on the **entire** reviewed v34 native tree. All inherited historical subtrees, inactive versions, previous reports and companion sources remain available. The old main entrypoint, README and build wrapper are preserved under `history/`. In the active two-volume sources, all **218** inherited theorem-like statements remain verbatim; **205 of 207** inherited proof blocks remain verbatim. The two edited blocks remove duplicate calculations by referring to their full proof in the preceding Blackwell proposition. No theorem is replaced by an unproved summary.

## Reproduce the native build

From this directory, with Python 3.10 or later and a complete TeX Live installation:

```sh
python build.py
python v35/verify_revision.py > /tmp/a1-v35-checks.json
python -O v35/verify_revision.py > /tmp/a1-v35-checks-O.json
cmp /tmp/a1-v35-checks.json /tmp/a1-v35-checks-O.json
python v35/author_verify_revision.py
python v35/independent_core_checks.py
```

The new comparison diagnostics require `sympy` and `mpmath`. The inherited exact diagnostics use the Python standard library. `build.py` invokes `v35/build_native.py`; it cleans generated entrypoint products, compiles both complete native volumes, exports actual labels, verifies convergence, compares TeX-recorder inputs with the declared source closure, and rejects unresolved references or overfull boxes. It does not use the historical changed-module smoke harness or external-reference stubs.

`verification-v35/NATIVE_BUILD_V35.json` and `NATIVE_BUILD_V34_CURRENT.json` record source Git hashes, compiler, pass results, log hashes, cross-volume export hashes and PDF hashes. `PRESERVATION.json`, `VALIDATION_SUMMARY.json` and `VISUAL_INSPECTION.json` record separate source, execution and sampled layout checks. The v35 build is content-addressed and precedes its publication commit; a null source-commit field is intentional, not a claim to have compiled an unspecified remote version. Generated PDFs, the full execution receipts and stdout logs are supplied in the accompanying downloadable review package; PDF binaries are not required to rebuild this repository source.

The analytic proofs, not the number of checks or pages, support the mathematical assertions. No formal proof-assistant verification, exhaustive priority search, global continuous-controller optimization or GitHub Actions execution is claimed by these receipts.
