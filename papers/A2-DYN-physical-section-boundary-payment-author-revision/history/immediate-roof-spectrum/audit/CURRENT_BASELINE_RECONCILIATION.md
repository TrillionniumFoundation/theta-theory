# Fresh A2-DYN source and carrier reconciliation

This is an author-revision provenance audit, not a new referee report. The fresh repository snapshot was captured on 23 October 2026 at 06:44:53 UTC. It contains 1,306 refs, including 436 A2-DYN refs: 249 revision, 178 review, four referee-copy, four referee-response and one research ref. Branch-role names are search hints; the source roles below are determined by their committed content.

## Complete census reconciliation

`CURRENT_SOURCE_CENSUS_DELTA.json` and `reconcile_source_census.py` record the executable reconciliation. Every one of the 435 refs in the inherited direct-source census occurs at exactly the same commit in the fresh snapshot. None disappeared or changed. The only added ref is `refs/heads/revision/a2-dyn-section-multipliers-exact-inversion-2026-10-23`, at `d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28`.

The inherited census records 219 commits, 120 distinct papers trees, 122 direct article trees, 93 reviews trees and 91 direct report-directory trees. Every ref-to-commit, commit-to-papers/reviews and papers/reviews-to-direct-article/report lookup closes. This is a fresh reconciliation of immutable commit and tree identities, supplemented by fresh retrieval of the new head's papers/article trees. It is not a claim that the 645 historical tree objects were all fetched a second time.

All 660 preserved native LaTeX bodies were read again from `research/historical-native/` and independently checked against the recorded byte count, Git blob SHA-1 and SHA-256. All checks pass. Each of the 120 direct historical article trees containing `main.tex` points to a main blob in this verified archive. Mere main-file presence does not certify input closure, build success or mathematical validity.

Two direct article trees lack `main.tex` and must not be presented as complete mathematical submissions:

| Historical directory | Article tree | Source role |
| --- | --- | --- |
| `papers/A2-DYN-v50-referee-response` | `58818bc4835ad9d7d689017174e1d8d6bb51809a` | Response packet, not a complete native manuscript |
| `papers/A2-DYN-clearance-jacobi-2026-10-15` | `4d30e4984ba0eda27927ee622a22a5cb18a44c55` | Incomplete source packet |

## Latest genuine native author source

The continuation baseline is `papers/A2-DYN-section-multipliers-exact-inversion-author-revision`, containing the inherited native mathematical chain through 332 and the complete native 333--335 proof bodies. Its source commit and evidence carrier are distinct:

| Identity | Mathematical source | Later evidence carrier |
| --- | --- | --- |
| Commit | `85f206907f56773e32fae9b61302924ca16603aa` | `d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28` |
| Root tree | `0a5bc8a95de43e7c4d381684f7ffa70b04cdbb4e` | `5ec7da36366d703d9e59a68245e90912639d18a0` |
| Article tree | `e4ddb6fd11e570dfc7bba9d5fd5a2fed051e78c7` | `381d0aa576a93d874bf974b0edcf090378aaa41b` |

The fresh GitHub compare receipt `SOURCE_TO_CARRIER_COMPARE.json` has source 85f2069 as its base and merge base; carrier d6c3c67 is exactly one commit ahead and zero behind. Its 30 changed paths are confined to the article's `PUBLICATION_STATUS.json`, `VALIDATION_REPORT.md` and `evidence/github/`. No LaTeX source, proof body, verifier, build script, workflow or other paper changes between these commits. Therefore the later carrier does not represent an additional mathematical revision.

The complete local author packet and actual compilation are independently verifiable from the parent's baseline rerun evidence. A readable/buildable packet does not imply that its final raw pointwise local limit theorem is proved. The current source itself records the remaining normalized local derivative/positive-source obligations. Fresh observations of the source and carrier CI were queued with no conclusion; these observations do not constitute completed CI.

## Controlling referee and applicable history

The latest substantive A2-DYN report remains the v115 double-clearance report, commit `f01482035a0b945b50f1f9c30f30ef35077558dc`, root tree `8c91a1709d4c8829d75f186b028e04ae7cb792a6`, report blob `9c68b0e8b31cd196c732514a29ebd44d95964243`. It expressly reviewed author commit `31792379408c5ace2c09284c2eb22d2331023433`, article tree `1cbc4d65c0b512292bd93535a2648ecdfc51415f`, native 270--276 against the inherited chain. It did not review 277--335. Its own description is author-requested AI-assisted review; it is not a journal decision or independent human specialist certification.

The complete 178-ref, 91-distinct-review-head time/content census, v114/v112/v73 applicable obligations and excluded v113 submission-state report are recorded in `FRESH_REFEREE_CHAIN_AUDIT.md` and `review-commit-census.json`. In particular, the v113 workflow/export assessment does not supplant v115's substantive mathematical questions. No favorable A2 geometry report is attributed to A2-DYN. The current mathematical continuation must answer v115's source-sum, shallow-source, capacity and exact-target requests in light of genuinely inherited later results; it must not relabel completed native 322/327--329/333--335 work as new.

## Reproduction

Run `python research/reconcile_source_census.py` from the task root. Its assertions verify the full 436-ref reconciliation, historical content lookup closure, every archived native blob, the main-file coverage and the source-to-carrier path restriction. This validates provenance and preservation. It is not a continuous-geometric or asymptotic proof.
