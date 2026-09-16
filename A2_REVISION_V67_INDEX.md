# A2 revision 67: the relative-law/contact mechanism

Revision branch: `revision/a2-v67-relative-law-mechanism-2026-09-16`.
Report answered: `review/a2-v66-independent-harsh-top4-2026-09-16`, immutable head `3d49684cc6c9bad36d80c99dc46af276f53fae18`.
Reviewed compiled source: `38f798a9b28237420f070a032d3601f0bee72cde`.
Reviewed manuscript tree: `c693d717577dc5f501f2a86ec937cfa36bf6ce4e`.
Expected complete revised manuscript tree: `5ba7cc8f87aaadd2e3f734c41bb030668e15cff7`.

## Complete manuscripts

[Principal article](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Full technical manuscript](papers/A2-v17-boundary-information-coarsening/main.tex) · [Two-collision companion](papers/A2-v17-boundary-information-coarsening/two_collision.tex).

The principal and full entries contain the complete correction in the existing `article/10c_global_curvature_inverse_v66.tex` and the revised common opening and abstract. Historical filenames and theorem labels remain stable; the entry metadata identifies revision 67. No new active proof module is added.

## Response and mathematical change

[Point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V67.md) · [Historical derivation audit](papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V67.md) · [Dependency ledger](papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V67.md) · [Primary-literature comparison](papers/A2-v17-boundary-information-coarsening/LITERATURE_CHECK_V67.md) · [Validation scope](papers/A2-v17-boundary-information-coarsening/VALIDATION_V67.md) · [Cover letter](papers/A2-v17-boundary-information-coarsening/COVER_LETTER_V67.md).

The residual stopping bound is proved, and curvature stopping error is propagated through a specified signed finite-jet recursion with a recursive Lipschitz constant. The corrected complete bound is `C_M(tau^N+epsilon)+L_M E_m`, not coefficient-one addition. The exact global inverse, no-closeness analytic identification, whole-obstacle conclusion with fixed lattice and visitation, complete local analytic inverse, and the separate weaker-data and charged results are retained at their full stated strength.

The main theorem now states the relative physical law together with the actual geometric inverse. Its significance case rests on this combined mechanism, with the existing equal-leading-data family and nonlinear stable return consequences made explicit. The quantitative correction is not called a new major theorem or a settled editorial significance decision.

## Preservation and delivery protocol

All 837 inherited manuscript paths remain. The eight edited originals are archived byte-exactly; the other 829 are unchanged. The active union remains 134 inputs. Review reports, old deliveries, default branch and A1 source are not rewritten.

The committed source payload is a deterministic patch against the reviewed tree, not a deferred proof generator. The native workflow authenticates its checksum and every edited baseline file, applies the already-written text, checks the complete final manuscript tree, commits and pushes the actual source, and builds all three complete entries. It then retains the PDFs, complete source archive, auxiliaries and logs on a new native-products revision branch and verifies the pushed Git blobs. Actual source/run/product identities and final visual coverage are recorded in `A2_REVISION_V67_REVIEW_READY.md` only after successful execution.
