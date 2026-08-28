# Referee Revision Patch Requests

- slug: A_Theory_of__Expectations
- generated_at: 2026-06-12 10:10:32
- source_matrix: logs/paperctl/A_Theory_of__Expectations/20260612_101030_referee_revision_planner/referee-revision-matrix.csv
- source_planner_dir: logs/paperctl/A_Theory_of__Expectations/20260612_101030_referee_revision_planner
- status: requested-not-applied

These are execution requests for future patch workers. This file does not
apply or merge manuscript edits.

## Request 01: theory-boundary

- matrix_rank: 1
- status: REQUESTED_NOT_APPLIED
- persona: theory
- severity: fatal
- risk_class: theory-boundary
- fix_class: claim downgrade
- objection: Theory referee: the strongest formal or contribution claim needs an explicit assumption/proof/comparison boundary at the cited source location before it can survive a hostile review.
- source_locator: submission/AoM/A_Theory_of__Expectations/main.tex:10
- evidence_locator: submission/AoM/A_Theory_of__Expectations/draft/referee-loop-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-patch-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-plan-status.md, submission/AoM/A_Theory_of__Expectations/draft/substantive-referee-loop-status.md
- evidence_status: weak_inventory_only
- proposed_fix: Add or tighten local assumptions and comparison scope around the cited claim; downgrade any theorem-level or optimality language not backed by the located proof/evidence.
- evidence_needed: weak_inventory_only: submission/AoM/A_Theory_of__Expectations/draft/referee-loop-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-patch-status.md, submission/AoM/A_Theory_of__Expectations/draft/referee-revision-plan-status.md, submission/AoM/A_Theory_of__Expectations/draft/substantive-referee-loop-status.md
- verification: compile plus theorem/assumption text search; keep claim wording tied to local proof/evidence
- patch_scope: patch-only; merge through paperctl merge-patch; post-patch judge required

### Worker Instructions

1. Inspect only local source and local artifacts.
2. Implement the smallest patch that resolves this objection, or mark it
   blocked with the missing local evidence.
3. Do not invent evidence, human decisions, reviewer facts, portal facts,
   acceptance status, or external outcomes.
4. Do not upload, email, submit, or merge directly.
5. Queue the patch through paperctl and run the listed verification before
   requesting merge.

## Request 02: artifact-anchor

- matrix_rank: 2
- status: REQUESTED_NOT_APPLIED
- persona: empirical-repro
- severity: fatal
- risk_class: artifact-anchor
- fix_class: evidence artifact
- objection: Empirical/repro referee: visible result, table, figure, or benchmark language needs an exact artifact/checksum/command anchor rather than broad empirical assurance.
- source_locator: submission/AoM/A_Theory_of__Expectations/main.tex:63
- evidence_locator: submission/AoM/A_Theory_of__Expectations/README.md
- evidence_status: candidate_found
- proposed_fix: Attach the claim to an existing local artifact, table source, checksum, or command log; if no direct artifact supports it, downgrade the result claim.
- evidence_needed: candidate_found: submission/AoM/A_Theory_of__Expectations/README.md
- verification: rerun artifact audit or gate command and record checksum; verify cited artifact path exists
- patch_scope: patch-only; merge through paperctl merge-patch; post-patch judge required

### Worker Instructions

1. Inspect only local source and local artifacts.
2. Implement the smallest patch that resolves this objection, or mark it
   blocked with the missing local evidence.
3. Do not invent evidence, human decisions, reviewer facts, portal facts,
   acceptance status, or external outcomes.
4. Do not upload, email, submit, or merge directly.
5. Queue the patch through paperctl and run the listed verification before
   requesting merge.

## Request 03: reproducibility-protocol

- matrix_rank: 3
- status: REQUESTED_NOT_APPLIED
- persona: empirical-repro
- severity: major
- risk_class: reproducibility-protocol
- fix_class: experiment/regeneration
- objection: Empirical/repro referee: the reproducibility layer must expose enough local commands, seeds, manifests, or checksums to regenerate the cited evidence.
- source_locator: submission/AoM/A_Theory_of__Expectations/main.tex:36
- evidence_locator: submission/AoM/A_Theory_of__Expectations/README.md
- evidence_status: candidate_found
- proposed_fix: Promote the relevant README/manifest/command evidence into the revision packet, or mark the request blocked and soften reproducibility claims.
- evidence_needed: candidate_found: submission/AoM/A_Theory_of__Expectations/README.md
- verification: run compile/gate and check README/manifest/checksum references before any merge
- patch_scope: patch-only; merge through paperctl merge-patch; post-patch judge required

### Worker Instructions

1. Inspect only local source and local artifacts.
2. Implement the smallest patch that resolves this objection, or mark it
   blocked with the missing local evidence.
3. Do not invent evidence, human decisions, reviewer facts, portal facts,
   acceptance status, or external outcomes.
4. Do not upload, email, submit, or merge directly.
5. Queue the patch through paperctl and run the listed verification before
   requesting merge.

## Request 04: anonymity-process

- matrix_rank: 4
- status: REQUESTED_NOT_APPLIED
- persona: checklist-anonymity
- severity: fatal
- risk_class: anonymity-process
- fix_class: anonymity/process-trace cleanup
- objection: Checklist/anonymity referee: source contains portal-facing anonymity or process-trace risk terms at the cited location.
- source_locator: submission/AoM/A_Theory_of__Expectations/main.tex:185
- evidence_locator: submission/AoM/A_Theory_of__Expectations/README.md
- evidence_status: candidate_found
- proposed_fix: Run or cite the local anonymity/process-trace audit; remove internal review/process terms from manuscript-facing files if any are present.
- evidence_needed: candidate_found: submission/AoM/A_Theory_of__Expectations/README.md
- verification: run anonymity/process-trace audit if available, then compile and scan source/PDF text
- patch_scope: patch-only; merge through paperctl merge-patch; post-patch judge required

### Worker Instructions

1. Inspect only local source and local artifacts.
2. Implement the smallest patch that resolves this objection, or mark it
   blocked with the missing local evidence.
3. Do not invent evidence, human decisions, reviewer facts, portal facts,
   acceptance status, or external outcomes.
4. Do not upload, email, submit, or merge directly.
5. Queue the patch through paperctl and run the listed verification before
   requesting merge.

## Request 05: patch-scope

- matrix_rank: 5
- status: REQUESTED_NOT_APPLIED
- persona: checklist-anonymity
- severity: major
- risk_class: patch-scope
- fix_class: manuscript edit
- objection: Checklist/anonymity referee: every accepted objection must become a bounded patch with a response matrix and post-patch closure check; broad rewriting would create new review risk.
- source_locator: submission/AoM/A_Theory_of__Expectations/main.tex:183
- evidence_locator: patch_queue + merge-patch + post-patch judge
- evidence_status: process_required
- proposed_fix: Route each fix through the structured request queue, patch worker, post-patch judge, and merge-patch discipline.
- evidence_needed: process_required: patch_queue + merge-patch + post-patch judge
- verification: post-patch judge must report closure before queued_for_merge or closed state
- patch_scope: patch-only; merge through paperctl merge-patch; post-patch judge required

### Worker Instructions

1. Inspect only local source and local artifacts.
2. Implement the smallest patch that resolves this objection, or mark it
   blocked with the missing local evidence.
3. Do not invent evidence, human decisions, reviewer facts, portal facts,
   acceptance status, or external outcomes.
4. Do not upload, email, submit, or merge directly.
5. Queue the patch through paperctl and run the listed verification before
   requesting merge.

## Global Boundary

- No manuscript edit is authorized by this request file alone.
- No evidence may be invented.
- No upload, email, external submission, or portal action is authorized.
- All accepted edits must be queued as patches and merged serially.
