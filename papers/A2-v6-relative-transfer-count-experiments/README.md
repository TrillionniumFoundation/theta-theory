# A2 v5 — statistical contact rigidity

**Qian Qi. Collision threshold laws and statistical contact rigidity in periodic dispersing billiards. September 9, 2026.**

`main.tex` is the complete native English manuscript, not a patch note or an abstract. It includes the general threshold proofs, the relative half-line determinant and physical law, the nonlinear examples, conditional observations, unlabelled inversion, marked and moving-cut responses, and all circular appendices. `two_collision.tex` is the unchanged full companion.

## Reading order

The main argument runs from geometric localization to relative boundary factorization, physical probability, and nonlinear contact determination. New proofs are in `v5/20_contact_rigidity.tex`, `v5/40_pairwise_inverse.tex`, and `v5/50_self_calibration.tex`. `RESPONSE_TO_REFEREE_V5.md` maps the controlling review to exact source labels; `PROOF_LEDGER_V5.md` records hypotheses and proof dependencies.

The contact inverse proves all-order triangular jet recovery and analytic continuation in the identical-even class, including an independent-jet geometric realization. The one-flight comparison is stated explicitly. The pairwise inverse uses four amplitudes and proves the optimal exponent 1/3, while retaining the distinct circular-reference exponent 1/2. Local self-calibration uses a coarse onset bracket and charges the fine calibration preparations in its cost.

## Reproduction

From this directory, install the packages in `tools-v5/requirements.txt` and a TeX distribution containing `amsart`, `lmodern`, `microtype`, `geometry`, `xr-hyper`, and `hyperref`. Run:

```sh
python tools-v5/build.py
```

This audits native input paths and labels, executes the diagnostics normally and under `python -O`, requires byte-identical outputs within that environment, compiles the companion and the complete manuscript, and records build logs and hashes under `verification-v5/`. The dedicated branch-scoped GitHub workflow has read-only repository permissions and uploads the complete source/PDF/log package. It never merges, changes permissions, or pushes generated changes.

The initial local run completed 175 finite checks (136 exact, 39 ordinary floating non-interval), identically with and without optimization. Its exact script identity and result digest are in `verification-v5/local_checks_summary.json`. These finite checks are not certificates of the infinite-dimensional, inverse, or statistical theorems; those are supported by the written proofs.

## Preservation and provenance

The branch starts from review commit `ec861ecfcdd83a81880c1a9082becc19b0c76977`, which reviews manuscript `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`. The controlling report is copied byte-for-byte into `review-basis-v4/`. The `v2`, `v3`, `v4`, `sections`, `history`, and legacy `tools` trees are retained by their original Git tree identities. All inherited mathematical proof files used by the new main article are unmodified. The rewritten introduction and comparison replace presentation, not theorem scope or proof content. Every older manuscript, report, and repository workstream remains unchanged on this branch.

The manuscript is an author revision for independent re-review, not a journal decision or a proof-assistant certification.
