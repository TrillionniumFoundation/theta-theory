# A2 — revision 71

**Boundary laws and smooth contact rigidity of periodic dispersing billiards** — Qian Qi

September 17, 2026. The directory's historical v17 name is not its current revision.

## Complete manuscripts

[Principal article](rigidity.tex), [complete technical manuscript](main.tex), and the unchanged [two-collision companion](two_collision.tex) retain all inherited mathematical content. The full periodic relative-law/smooth-contact/finite-preparation proof chain remains first. The new [local observation section](article/10f_local_observation_comparison_v71.tex) and [lens comparison](article/00k_lens_comparison_v71.tex) answer the concrete data/prior-art issue in the latest report without weakening the central theorem or replacing its proof.

## Response and provenance

[Point-by-point response](RESPONSE_TO_REFEREE_V71.md) · [Cover letter](COVER_LETTER_V71.md) · [Proof dependency ledger](journal/DEPENDENCY_LEDGER_V71.md) · [Historical reading and preservation](HISTORICAL_DERIVATION_AUDIT_V71.md) · [Primary-source comparison](LITERATURE_CHECK_V71.md).

The report is frozen at `f1d516c0033256d50ca23d87cc5a40fef8f72d45`; its reviewed manuscript subtree is `63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b`. All 911 reviewed source paths remain. The six edited originals and full baseline manifest are retained in [history/v70-review-baseline](history/v70-review-baseline/). All 138 earlier active TeX inputs remain; three new shared inputs are added. The five central proof modules are byte-exact.

## Reproduction

From a clean Git checkout run `python -B tools/build_revision_v71.py --output-dir /absolute/path/outside/manuscript`. The native engine freezes tracked Git objects, verifies recorders and producer auxiliaries, builds all three entries with shell escape disabled, and compares normal/optimized finite diagnostics. The v71 conservation check reconstructs reviewed v70 bytes to run its unchanged diagnostic. These checks are not mathematical certification. Raw ZIP-mode and committed-product verification remain separate.

Source-matched products, completed run identity and actual visual-inspection scope are recorded in the root `A2_REVISION_V71_REVIEW_READY.md` after publication. A workflow definition alone is not a successful build. Exceptional significance remains a matter for independent mathematical assessment, not a diagnostic flag.
