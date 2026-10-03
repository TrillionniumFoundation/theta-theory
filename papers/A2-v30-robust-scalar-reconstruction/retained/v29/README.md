# A2 v29 — scalar collision laws and full-period recognition

Qian Qi · 3 October 2026

Primary article: **Scalar collision laws and recognition of periodic dispersing billiards**, `main.tex` (12 pages in the actual local build). The controlling report is the latest v28 report at `a067c123c5702decb4b7146cf57961a65afe5c88`; the reviewed author source is `3ac2df58d175010f338dd6ae8af84158c1590d20`. The billiard collision-law inverse topic and the requested Annals/Acta/Inventiones/JAMS target remain unchanged. The revised title names the actual primary theorem rather than the older supplementary return-law project.

## Principal results

Theorem 1.1 proves the exact fixed-horizon reversal identity. Opposed first-collision bits, paired with translated starting distributions, give the spatial finite difference of the obstacle indicator. No impact coordinates, collision angles or collision times are recorded. Solid-start failures and misses both produce zero and remain in the preparation denominator.

Theorem 1.2 explicitly inverts that difference by the negative minimum of partial sums along a bounded chain. Component diameter and separation force a zero somewhere on each chain; a free reference point is not supplied. The same argument works for nonnegative mollified occupation and gives an error independent of the smoothing scale. Theorem 3.4 combines the scalar inverse with the retained complete-patch period criterion, recovering the entire periodic union, full lattice and primitive orbit count with repeated shapes and arbitrary symmetries.

Theorem 4.1 gives finite-confidence recovery on the **known nonperiod patch-margin class B_eta**, with all geometric and C6 priors explicit. A deterministic grid of localized launch laws gives a conditional sufficient attempt bound `C_eta nu^-3 log(C_eta/(nu delta))`, with input localization scale `O(nu^(3/2))`. This is not a minimax bound, an efficient infinite-class search algorithm, or a uniform discrete guarantee without eta. Corollary 4.3 gives pointwise eventual recovery when the margin is not known.

The reduction is in the recorded output, not in every resource: localized spatial launch control and two calibrated collimated directions are substantive inputs. This is **not** a solution of the earlier uniformly prepared exact analytic count-only problem, a passive-trajectory inverse, or a spectral-rigidity theorem. The exact data are two functionals of spatial launch densities, not two real numbers. The finite theorem uses an explicitly finite command list.

## Referee route and preservation

Read Sections 1–2 for the new scalar inversion, Section 3 for exact periodic recognition, Section 4 for finite confidence, and Section 5 for information categories and the recent local-periodicity comparison. `RESPONSE_TO_REFEREES.md` addresses all six required corrections individually. `PROOF_LEDGER.md` separates new arguments, reused geometry, assumptions and diagnostics.

**Supplement P** at `retained/v28/` is the entire reviewed v28 paper tree, unchanged: `b17c9c051f3e279d6f7610e3d1c5e56d0733216a`. Its nine active mathematical inputs and every nested supplementary volume remain available. No earlier theorem is replaced by the new protocol. The retained spatial first-impact theorem still has its own `nu^-3/4` sufficient attempt bound under a known patch margin and its output-localization assumption.

Earlier author versions are **repository-deposited/source-qualified revisions**, not journal publications. The historical v28 README's phrase “already published” is corrected here and in the source-status note, while the frozen reviewed snapshot remains byte-identical. Previous manuscript and referee paths are not edited.

## Reproduction

Run `python3 tools/validate_v29.py` for the primary. In an exact Git checkout run:

```sh
python3 tools/validate_v29.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"
```

The full mode checks the exact retained native tree, invokes the unchanged v28 qualification chain at the current SHA, and requires twelve documents in total. Dependencies are Python 3.10+, LaTeX/amsart/Latin Modern/microtype, latexmk and Poppler; inherited diagnostic suites also require NumPy and SciPy. The read-only workflow installs them, checks out its exact triggering SHA without persistent credentials, and archives native sources plus actual logs/PDFs including failures.

The actual local primary-only run passed **18,945 finite mathematical/source diagnostics** and **19 adversarial validation-contract checks**, in normal and optimized Python with identical outputs. The 12-page primary compiled with no final TeX warnings, unresolved references or overfull/underfull boxes. Its twelve rendered pages were inspected. New source hashes were unchanged during validation.

That run was **source-content execution, not an authenticated Git checkout**. It did not execute the eleven retained documents. `verification/local/receipt.json` records the actual scope with null source-commit/run fields. `SOURCE_PINS.json` binds every new mathematical/tool file and the new workflow. A queued or configured workflow is not a successful hosted full-package run; the current workflow must supply its own receipt. Historical v28 hosted success is not relabelled as v29 evidence.

Finite checks do not certify continuum arguments, sensor feasibility, literature priority, or journal acceptance. The exact-source qualification likewise concerns reproducibility, not an independent referee decision.
