# Referee Revision Plan Status

- slug: A_Theory_of__Expectations
- updated_at: 2026-06-12 10:10:30
- latest_substantive_referee_prompt: logs/paperctl/A_Theory_of__Expectations/20260612_101027_substantive_referee_worker/substantive-referee-prompt.md
- latest_substantive_prompt_manifest: logs/paperctl/A_Theory_of__Expectations/20260612_101027_substantive_referee_worker/prompt_versions/referee-model-review-v1/manifest.json
- latest_referee_model_review_json: logs/paperctl/A_Theory_of__Expectations/20260612_101027_substantive_referee_worker/referee-model-review.json
- latest_substantive_referee_report: logs/paperctl/A_Theory_of__Expectations/20260612_101027_substantive_referee_worker/substantive-referee-report.md
- latest_substantive_revision_plan: logs/paperctl/A_Theory_of__Expectations/20260612_101027_substantive_referee_worker/revision-plan.md
- latest_revision_planner_report: logs/paperctl/A_Theory_of__Expectations/20260612_101030_referee_revision_planner/referee-revision-planner-report.md
- latest_revision_matrix: draft/referee-revision-matrices/latest-referee-revision-matrix.csv
- latest_status: planned-not-applied
- latest_source_mode: referee_model_review_json

## Revision Matrix

The matrix CSV is proposed by this patch at:

`draft/referee-revision-matrices/latest-referee-revision-matrix.csv`

```csv
rank,persona,severity,objection,risk_class,fix_class,source_locator,evidence_locator,evidence_status,proposed_fix,evidence_needed,verification,patch_scope,status
1,theory,fatal,Theory referee: the strongest formal or contribution claim needs an explicit assumption/proof/comparison boundary at the cited source location before it can survive a hostile review.,theory-boundary,claim downgrade,submission/AoM/A_Theory_of__Expectations/main.tex:10,"submission/AoM/A_Theory_of__Expectations/draft/referee-loop-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-patch-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-plan-status.md, submission/AoM/A_Theory_of__Expectations/draft/substantive-referee-loop-status.md",weak_inventory_only,Add or tighten local assumptions and comparison scope around the cited claim; downgrade any theorem-level or optimality language not backed by the located proof/evidence.,"weak_inventory_only: submission/AoM/A_Theory_of__Expectations/draft/referee-loop-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-patch-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-plan-status.md, submission/AoM/A_Theory_of__Expectations/draft/substantive-referee-loop-status.md",compile plus theorem/assumption text search; keep claim wording tied to local proof/evidence,patch-only; merge through paperctl merge-patch; post-patch judge required,MODEL_REVIEWED_NOT_APPLIED
2,empirical-repro,fatal,"Empirical/repro referee: visible result, table, figure, or benchmark language needs an exact artifact/checksum/command anchor rather than broad empirical assurance.",artifact-anchor,evidence artifact,submission/AoM/A_Theory_of__Expectations/main.tex:63,submission/AoM/A_Theory_of__Expectations/README.md,candidate_found,"Attach the claim to an existing local artifact, table source, checksum, or command log; if no direct artifact supports it, downgrade the result claim.",candidate_found: submission/AoM/A_Theory_of__Expectations/README.md,rerun artifact audit or gate command and record checksum; verify cited artifact path exists,patch-only; merge through paperctl merge-patch; post-patch judge required,MODEL_REVIEWED_NOT_APPLIED
3,empirical-repro,major,"Empirical/repro referee: the reproducibility layer must expose enough local commands, seeds, manifests, or checksums to regenerate the cited evidence.",reproducibility-protocol,experiment/regeneration,submission/AoM/A_Theory_of__Expectations/main.tex:36,submission/AoM/A_Theory_of__Expectations/README.md,candidate_found,"Promote the relevant README/manifest/command evidence into the revision packet, or mark the request blocked and soften reproducibility claims.",candidate_found: submission/AoM/A_Theory_of__Expectations/README.md,run compile/gate and check README/manifest/checksum references before any merge,patch-only; merge through paperctl merge-patch; post-patch judge required,MODEL_REVIEWED_NOT_APPLIED
4,checklist-anonymity,fatal,Checklist/anonymity referee: source contains portal-facing anonymity or process-trace risk terms at the cited location.,anonymity-process,anonymity/process-trace cleanup,submission/AoM/A_Theory_of__Expectations/main.tex:185,submission/AoM/A_Theory_of__Expectations/README.md,candidate_found,Run or cite the local anonymity/process-trace audit; remove internal review/process terms from manuscript-facing files if any are present.,candidate_found: submission/AoM/A_Theory_of__Expectations/README.md,"run anonymity/process-trace audit if available, then compile and scan source/PDF text",patch-only; merge through paperctl merge-patch; post-patch judge required,MODEL_REVIEWED_NOT_APPLIED
5,checklist-anonymity,major,Checklist/anonymity referee: every accepted objection must become a bounded patch with a response matrix and post-patch closure check; broad rewriting would create new review risk.,patch-scope,manuscript edit,submission/AoM/A_Theory_of__Expectations/main.tex:183,patch_queue + merge-patch + post-patch judge,process_required,"Route each fix through the structured request queue, patch worker, post-patch judge, and merge-patch discipline.",process_required: patch_queue + merge-patch + post-patch judge,post-patch judge must report closure before queued_for_merge or closed state,patch-only; merge through paperctl merge-patch; post-patch judge required,MODEL_REVIEWED_NOT_APPLIED
```

## Boundary

No manuscript edit, evidence generation, upload, email, submission, or merge is
authorized by this status file. It is a patch-only planning artifact.
