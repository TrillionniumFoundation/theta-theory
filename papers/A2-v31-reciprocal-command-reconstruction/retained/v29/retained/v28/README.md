# A2 v28 — local period recognition with repeated shapes

Qian Qi · 3 October 2026

**Primary:** *Reference-free certification from intrinsic boundary laws*, `main.tex`. The controlling referee report is the latest v26 report at `24b9c5f6a586a35975e6f6b67d25ec431390f57a`, report blob `49d522f04930a0c4d9b3fd3ac3c555a8895596eb`. This revision builds on the already published v27 at `f230e014911f3b7104db0ec742969789ed5a88c9`; it does not present that earlier publication as new work or invent a v27 referee report.

## Mathematical reading route

**Theorem 1.2** determines the whole periodic union, its full translation lattice, primitive component multiplicity and primitive free area from the support of one fixed-aperture first-impact position law. Individual shape separation is removed. Equal disks and repeated congruent obstacles are allowed, and a bounded presentation need not be primitive. Local origins and return windows are not required by this route; controlled independent launches, a common laboratory frame, a bounded period presentation and calibrated localization remain explicit.

**Lemma 1.3** is the new geometric mechanism: a candidate translation is a global period precisely when it preserves every component in a bounded central patch in both directions. The unknown presentation bound ensures that the patch contains representatives of every component orbit. Matching one pair of equal bodies is not enough. **Lemma 1.4** bounds the index of the unknown full group over the given existential presentation by the number of component orbits, and proves that protected short candidates generate that full group.

**Theorem 1.6** gives finite-confidence recovery on numerical patch-mismatch classes, with `O(nu^(-3/4) log(C/(nu delta)))` attempted launches, localization error `O(nu^(3/2))`, and `C2` geometric error `O(nu)`. The margin concerns false period candidates, not separation between individual shapes. **Corollary 1.7** gives pointwise eventual recovery when the numerical margin is unknown. **Proposition 1.8** gives an exact repeated-disk example showing why uniform recovery of the full discrete period structure cannot ignore an approaching symmetry increase.

The title, periodic-billiard boundary-law topic and requested mathematical-journal target are unchanged. No passive-orbit, count-only, minimax or formal-proof claim is added.

## Preservation

All **eight v27 core files** remain active and byte-identical. The new proof is `core/00_local_period_recognition.tex`. The complete native v27 paper is retained at `retained/v27`, tree `c9e18bc786b795e61a6ed8c0048249bb14713a04`, including its exact v26/v25 sources, earlier articles and complete Supplement S. The endpoint-excluding clearance correction remains active in `core/03_recognition.tex`; the historical uncorrected text remains only in its explicitly preserved source snapshot. No earlier repository paper or review path is edited.

## Reproduction

Requirements: Python 3.10+, NumPy/SciPy for inherited diagnostics, `latexmk`, a LaTeX installation with `amsart`, Latin Modern and the listed packages, and Poppler `pdfinfo`.

```sh
python3 tools/validate_v28.py
# From a clean checkout, qualify the current primary and ten retained documents:
python3 tools/validate_v28.py --all-volumes --require-checkout \
  --expected-commit "$(git rev-parse HEAD)"
```

The native driver checks exact source pins, all eight retained active core blobs, the entire retained v27 tree, the workflow digest and the triggering SHA. It runs new diagnostics and negative controls in ordinary and optimized Python, builds this primary, and invokes the unchanged v27 driver for all ten retained documents. A stale/partial receipt, missing tool or skipped qualification cannot become a full-package pass.

The new finite suite covers all 4,095 nonempty uncoloured 4-by-3 motifs and 728 nonempty two-colour 3-by-2 motifs, independent finite-patch/global-period comparisons, primitive multiplicity, Hermite covolumes, noisy patch thresholds, the symmetry-jump example and source integrity. These finite tests are not a proof certificate or a physical sensor execution.

`verification/local` records the actual local execution scope. A local validation snapshot is not a remote clone or a hosted result. The exact-SHA workflow `.github/workflows/a2-v28-verify.yml` unconditionally installs tools and qualifies the full package, then archives actual logs and PDFs, including failures. A successful source archive alone is never described as a full pass. Historical raw layout diagnostics and disclosed stage-only layout wrappers remain visible in the inherited receipts.

`RESPONSE_TO_REFEREES.md`, `PROOF_LEDGER.md`, `HISTORICAL_AND_LITERATURE_AUDIT.md` and `DELIVERY_STATUS.md` give the correction map, assumptions, provenance and actual verification limits.
