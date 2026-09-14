# A2 v42 — actual verification ledger

Date: September 14, 2026. This ledger concerns the source revision on `revision/a2-v42-native-source-referee-response-2026-09-14`, descended from the v41 report at `e162532115071265cf73b97a5069f33628347cfe`.

## Source-revision checkpoint

The exact native v41 main, preamble, auxiliary wrapper, introduction, proof-architecture section, geometric setup, protocol scope, observation hierarchy, single-offset inverse and rerooting lemma were recovered locally and checked against their Git blob identities. Recovery of this subset is not recovery of the complete native closure.

The revised single-offset chapter has Git blob `aea44fc8ed3273174a225b143d3fdf5b5c9b5a19`; its predecessor has blob `63ed36efd417cd23e6f869952627719de00e6ef7`. All theorem, proposition and corollary environments in those two chapters were compared programmatically and found byte-identical. The detailed global proof is expanded by a net 28 lines. The proposed native main has blob `1ab0293dfbc619e2d216f0de77145ee8b90e72f4`; its only changes at this checkpoint are revision/date metadata and the single-offset chapter input. There remain 54 literal direct main inputs, counting preamble and bibliography, and 36 inputs in the unchanged auxiliary compendium.

## Actual hosted attempt

The first v42 hosted attempt concerns infrastructure commit `4d78f5d3850cfae79df6b13c30176e9c64222efe`, before activation of the new mathematical chapter. Its mathematical source is still the inherited v41 source.

| Field | Actual retrieved value |
|---|---|
| Workflow | A2 v42 source-pinned native submission |
| Run | `34798984887` |
| Head | `4d78f5d3850cfae79df6b13c30176e9c64222efe` |
| Job | `103837618309`, `native` |
| Run/job conclusion | `failure` |
| Job created/started | `2026-09-14T02:22:20Z` |
| Job completed | `2026-09-14T02:22:24Z` |
| Executed steps | `[]` |
| Runner ID/name | `0` / empty string |

The run and job metadata were actually retrieved through the authenticated repository connector. An empty step list is not a TeX log. No executed compiler command, native PDF, page count, or visual inspection is established by this attempt, and no cause is inferred from the metadata alone.

## C2 status at this checkpoint

**Open.** The complete native main and companion have not yet been source-matched, compiled and visually inspected in this v42 execution record. The local source subset, an inherited companion build, earlier software tests, numerical diagnostics and the workflow configuration do not close this item. No successful C2 certificate is issued here.

The required evidence remains: exact source and active recursive inputs, complete native main and companion outputs, actual commands/tool versions/exit status, raw logs and recorders, generated companion-auxiliary provenance, PDF identities and rendered-page coverage. Any additional evidence must state its own source commit and the scope actually executed.

## Inherited findings, not new executions

The v41 referee's independently executed diagnostic families, earlier author software regressions and earlier companion or fixture builds keep their historical status. They were not rerun at this source-revision checkpoint. The v41 source review is likewise not a new all-dependency proof audit by this revision.
