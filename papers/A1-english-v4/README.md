# A1 English revision 4.0 — structural and robust operational theory

**Qian Qi · September 6, 2026**

**A1: Realizable Mechanical Experiments, Path Selection, and Response**  
*Selection rank, solved costly readout gates, and a quantitative positive-polynomial hierarchy for controlled detectors*

## Referee entrance

[Main LaTeX manuscript](main.tex) · [Proof sections](sections/) · [Point-by-point response](RESPONSE_TO_REFEREE.md) · [Proof ledger](PROOF_LEDGER.md) · [Historical derivation map](HISTORICAL_DERIVATION_MAP.md) · [Executed diagnostics](validation/DIAGNOSTICS.json) · [Build receipt](validation/BUILD.json)

This is a new self-contained principal manuscript, not an addendum requiring an unpublished source tree. The build contains **25 pages**, including the contents, six main sections, two appendices and references. Its 17 local diagnostics passed; the costly-gate performance inequality has a separate exact rational interval certificate. These facts are reproducibility evidence, not an independent acceptance decision or formal verification of the general proofs.

## What is submitted for the next review

Theorem 2.3 gives a necessary-and-sufficient coefficient-rank criterion for a full attainable failure family, an explicit Gram-matrix realization radius and polynomial-class rank stability. Rank `r` gives normalized `n`-report product dimension `n(r-1)`, including rank-deficient spaces. The local dimension statement is not a claim of a global minimal embedding for every singular rank-deficient product space.

Theorem 2.4 specializes this to the counted Lorentz apparatus: passive fixed-mode likelihoods have maximal dimension `n`, while selectable all-censoring histories have dimension `3n`; the attainable coefficient cube has an explicit radius that degenerates as detector amplitude vanishes. This is a comparison across known command histories, not a claim that a fixed garbling increases information.

Theorem 3.4 incorporates the referee-derived endpoint-gate result with attribution. Theorem 4.1 then solves the positive-cost last-cartridge problem: one collision acceptance arc and four candidate mode/decision values. Proposition 4.2 proves a strict gain above `8e-4` over **all constant, report-blind gates**, with a gain above `7e-4` surviving a full-support prior perturbation. This is not described as a multi-stage temporal adaptivity gap.

Theorems 5.1–5.2 build a mechanically realizable positive-polynomial hierarchy for continuous collision detectors. They preserve placement/no-hit laws, common gates and failed-attempt accounting, and convert model error into uniform complete-policy regret, explicit degree requirements and finite lookup sizes. A changed detector is not mislabeled coefficient roundoff, and is not asserted to preserve the original cubic cutoff.

The principal chamber theorem now requires the specified smooth reporting map; the gate body is a subset of `R^5`, not universally intrinsically five-dimensional. The earlier biased-entropy, two-trace and transported-preparation repairs are retained, including an explicit external-boundary flux and Eulerian bulk derivatives.

## Source control and history

Controlling review: `574f2315a136d8b401644d8a3eeeb93c87887010`, branch `review/a1-english-v3-harsh-referee-2026-09-05`.

Reviewed v3: `025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6`, source tree `ec09fa385c5fdcc5f2aece59a6b7f0806bfbb8ea`.

New revision branch: `revision/a1-english-v4-structural-robust-control-2026-09-06`.

The new branch descends from the review commit. Existing main, review and previous revision sources are not edited. The [historical companion](../A1-english-v3/foundations/) remains available unchanged in its prior location; its old edition and validation records are historical, not v4 execution claims. The principal v4 build does not depend on it.

## Reproduce

From this directory:

```sh
python tests/test_revision.py
python build_and_verify.py
```

The tests use Python, NumPy and SymPy; the rational certificate separately needs only the standard library. The build needs `pdflatex`, standard LaTeX packages used in `main.tex`, Latin Modern, and `pdfinfo`. It performs three no-shell-escape passes and rejects undefined references/citations, missing characters and overfull boxes. It writes `A1_REVIEW.pdf` locally. The checked-in source and build receipt do not imply a GitHub-hosted PDF binary or successful GitHub Actions run.

The separate rational certificate can be executed as:

```sh
python tests/rational_gate_certificate.py
```

`validation/VISUAL_REVIEW.json` records the local PDF render inspection. No original v3 author suite or referee 20-check script was rerun in this revision; their historical receipts are not counted among the 17 v4 diagnostics. Test results do not substitute for the all-budget dimension, compact selection, physical coverage or approximation proofs.
