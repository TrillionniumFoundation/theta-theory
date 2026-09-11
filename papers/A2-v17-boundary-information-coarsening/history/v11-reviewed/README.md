# A2 v11: nonlinear boundary laws and stable energy invariants

**Author:** Qian Qi. **Date:** 10 September 2026.

This is the complete English revision responding to the completed-v10 independent report. Start with `main.tex` and `RESPONSE_TO_REFEREES.md`. All prior A2 formal statements/proofs remain active; the original companion is `two_collision.tex`. This is native TeX, not a placeholder, initialization or encoded manuscript payload.

## Main additions
Theorem 10.1 gives a two-sided weighted Abel-flux coordinate for the full energy invariant. Theorem 13.1 and Corollary 13.2 reconstruct it from charged binary preparations with a refined sufficient exponent. Theorem 14.3 removes exact gap/area/multiplier calibration in a specified smooth physical class by an explicitly charged pilot. The target remains two labelled symmetrized energy profiles, not arbitrary asymmetric contact geometry. The old integer-norm acquisition and every finite-dimensional benchmark are retained.

## Build and verification
From this directory, with a TeX distribution providing `latexmk`, `pdflatex` and the declared packages:

```sh
python tools/build.py
python tools/run_all_checks.py
```

The build starts with fresh auxiliary state and disables shell escape. It builds `two_collision.pdf` before `main.pdf` to resolve the companion references. The full suite needs SymPy for inherited diagnostics. The new `tools/verify_v11.py` uses only the Python standard library and can also be run independently:

```sh
python tools/verify_v11.py --output verification/v11.normal.json
python -O tools/verify_v11.py --output verification/v11.optimized.json
```

The historical v9 verification inputs are authenticated by their hashes. A full repository checkout supplies the original v9 publication. In the standalone packet they are under `reference_v9`; alternatively use `python tools/run_all_checks.py --v9-source-dir PATH`. No network is used by these scripts. The scripts generate local `verification/` records. The committed `VERIFICATION.json` summarizes actual author-session runs; full logs and compiled PDFs accompany the revision packet. Binary PDFs are not duplicated in the native Git source tree.

## Reading map
Part I proves the physical relative law and identifies its nonlinear invariant. Part II gives both acquisition procedures, smooth-class self-calibration and endpoint experiments. Part III and the appendices retain the finite-dimensional experiments and complete historical applications. `PROOF_LEDGER.md` identifies the hypotheses and proof chain; `HISTORICAL_DERIVATION_AUDIT.md` identifies the prior derivations consulted.

## Source pins and limits
The base is author commit `f46dca20f3d1b73077522bb2041f463af033cb70`, reviewed at `2b893b931a894dfc9e7730b853f575124ffb5c55`. The authenticated v10 native tree is `452a9003b03ff8f6eed47e1f609a36a054271455`. The new branch is based on that review and adds a separate manuscript directory; no old path is removed. The preparation results are sufficient certificate-dependent bounds, not minimax statements for full profiles. Finite tests and successful builds are not formal proof certificates, an exhaustive novelty search, remote CI, or a journal decision.
