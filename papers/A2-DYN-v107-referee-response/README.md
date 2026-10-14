# A2-DYN — Revision 107

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**

Author: Qian Qi. Revision date: 14 October 2026.

## Referee manuscript

`main.tex` is the active article. It retains the original exact-return event, occupation/displacement labels, normalization, arithmetic zero classes, raw pointwise target and scalar-first conditional-law order. The paper is an AMS mathematical article with explicit hypotheses, theorem/proof statements, and a separate inherited supplement; no journal acceptance or independent certification is claimed.

New complete proof modules:

- `core/256_two_ended_envelope_and_moving_roof_comparison.tex`: endpoint passage; target-local comparison-window lemma; nonstationary, two-ended positive-envelope theorem; actual nested-roof and attained-level criteria; distinct bounded/growing-budget rates.
- `core/257_fractional_capacity_and_original_microscopic_source.tex`: maximal scalar capacity allocation for each fixed comparison family; positive monotonic improvement over either one-ended envelope; exact original microscopic-source decomposition and unchanged scalar target.

`appendices/v107_coverage_and_limit_order.tex` specifies coverage, trace loss versus capacity shortage, actual reach, physical overlap and the order of limits.

## Frozen sources

Controlling substantive report: `reviews/a2-dyn-v104-positive-interval-external-top4-review-2026-10-14/REFEREE_REPORT.md`, review commit `684c84c038c55d636285cd240f1ae2e8c85d461a`, report blob `a22f11ea053a7e22dbfcf2cd98b0489d6ef4bfc1`.

Latest author base: `d1aa59cefb5d1158a05f556ab9c7c38398f2e4fd`, paper tree `6acebbc6669612b32171bb9f50b5bbbd7b77459f` at `papers/A2-DYN-v106-referee-response`. This includes the subsequent v105 and v106 derivations. The v103 submission-state review is not substituted for the substantive v104 report.

All 255 inherited numbered core modules and the v106 logarithmic criterion remain byte-identical. Modules 256–257 are added. The full v106 directory remains unchanged in the repository; `provenance/v106-main.tex` is an additional exact snapshot. Earlier versions, alternate variants and other papers are not modified.

## Proof status and response

Read `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `SOURCE_MANIFEST.json` and `PUBLICATION_STATUS.json` for the current revision. Other inherited root-level historical records are archival, not current certification records; their original versions remain available in the frozen v106 directory.

The two-ended theorem pays all comparison endpoint-trace loss without a stationary entrance or a lower paired-trace fraction. The remaining source is uncovered or capacity-unallocated microscopic source with its original positive weight. Its global essential-height decay has not been proved. Neither the full raw LLT nor unrestricted downstream laws are promoted on the strength of this revision.

## Reproduction

From an exact Git checkout containing the baseline commit:

```sh
bash papers/A2-DYN-v107-referee-response/build.sh
```

The build verifies the exact checkout, allowed repository scope, frozen review and baseline tree, all inherited core blobs, active input links, and normal/optimized finite diagnostics. It assembles the inherited supplement and compiles both PDFs with shell escape disabled, checking reference stabilization and warnings. A recorder audit checks that every one of the 257 core modules was actually read by the main/supplement build.

The new workflow is `.github/workflows/a2-dyn-v107-positive-source-qualification.yml`. Its PDFs, logs, exact-SHA evidence and render previews are build artifacts. These checks establish source and typesetting facts, not an independent mathematical referee report.
