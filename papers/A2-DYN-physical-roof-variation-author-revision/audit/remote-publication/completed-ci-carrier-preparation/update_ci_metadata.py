#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import json
A=Path('/workspace/scratch/35c64a3513c5/theta-theory-next/papers/A2-DYN-physical-roof-variation-author-revision')
S=Path('/workspace/scratch/35c64a3513c5/new-round-current-ci-success')
V=json.loads((S/'ARTIFACT_VERIFICATION.json').read_text())
J=json.loads((S/'jobs-39526895726.json').read_text())['jobs'][0]
if V['status']!='passed' or V['tested_sha']!='6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9' or V['checks_completed']!=1333:raise RuntimeError('Unexpected verified artifact')
if J['conclusion']!='success' or any(s['conclusion']!='success' for s in J['steps']):raise RuntimeError('Unexpected job steps')
SOURCE=V['tested_sha'];PENDING='d46ba004ff1ac8d44dab04549daff7e3c0e5f205'
p=A/'PUBLICATION_STATUS.json';d=json.loads(p.read_text())
if d['current_revision_ci']['state']!='queued_not_executed':raise RuntimeError('Unexpected preceding CI state')
d['schema']='a2-dyn-physical-roof-variation-publication-v3'
d['scope']='Published complete mathematical source, completed local release, and independently verified successful remote CI at the exact source commit. Source-stage and pending-state metadata remain preserved; later evidence carriers change no frozen mathematical/build input.'
d['updated_utc']=datetime.now(timezone.utc).isoformat()
d['current_revision_ci']={
 'state':'completed_and_artifact_verified','observed_at_utc':'2026-10-21T01:48:57Z',
 'run_id':V['run_id'],'run_attempt':V['attempt'],'run_url':V['remote_run'],
 'requested_head_sha':SOURCE,'actual_tested_checkout_sha':SOURCE,
 'status':'completed','conclusion':'success','job_id':V['job_id'],
 'job_status':'completed','job_conclusion':'success','job_started_at':J['started_at'],
 'job_completed_at':J['completed_at'],'runner_id':J['runner_id'],
 'executed_steps':V['steps'],'all_steps_successful':True,'artifact_count':1,
 'artifact_id':V['artifact_id'],'artifact_bytes':V['artifact_bytes'],
 'artifact_sha256':V['artifact_sha256'],'artifact_file_members':V['artifact_file_members'],
 'checkout_verified_from_execution':True,'verified_mathematical_commands':V['finite_check_commands'],
 'verified_normal_optimized_comparisons':V['normal_optimized_comparisons'],
 'verified_native_compile':True,'native_pdf_pages':V['native_pages'],
 'native_tex_files':V['native_tex_files'],'native_pdf_sha256':V['native_pdf_sha256'],
 'verified_historical_compile':True,'historical_pdf_pages':V['historical_pages'],
 'historical_repository_wide_gate_executed':False,
 'artifact_downloaded':True,'artifact_verified':True,'receipt_consistency_checks':V['checks_completed'],
 'readback':'audit/current-ci-success-readback/ARTIFACT_VERIFICATION.json',
 'workflow_manually_rerun':False,'source_or_workflow_repair_required':False,
 'job_log':'audit/current-ci-success-readback/job-118983561729.sanitized.log',
 'job_log_redaction_receipt':'audit/current-ci-success-readback/JOB_LOG_RETRIEVAL.json',
 'scope':'Actual remote source-bound command receipts and artifact bytes have been verified. Consistency checks, finite mathematical diagnostics and successful compilation are not a continuum-proof certificate.'}
d['earlier_pending_ci_readback']={'observed_at_utc':'2026-10-21T01:37:28.119Z','carrier_commit':PENDING,
 'readback':'audit/current-ci-readback/PENDING_CI_READBACK.json','carrier_metadata':'audit/remote-publication/pending-carrier/','preserved_without_rewriting':True}
d['remote_publication']['pending_evidence_carrier_commit']=PENDING
d['remote_publication']['evidence_carrier']='This version is an evidence-only child of pending_evidence_carrier_commit, which is a child of source_commit. Its actual commit identity is supplied by Git ancestry and the branch ref; no future self-hash is fabricated.'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
p=A/'VALIDATION.md';s=p.read_text()
start=s.index('## Remote CI and publication\n');end=s.index('\n## Mathematical status\n',start)
section=f'''## Remote CI and publication

The previous complete article's successful run at `86c947eccea6029258d9a362624866a475118a66` was freshly re-read under `audit/prior-ci-readback/`. That predecessor execution remains separate from this revision.

The complete new source was published as **`{SOURCE}`**, root `ad34fd91ad2f1c6e594d3bbe437417aba524bf87`, article `4f41b3a98487a1ae0507d40390aca030c5520e19`, on `revision/a2-dyn-physical-roof-variation-2026-10-21`. All 5,261 source additions were confined to the new article and its dedicated workflow. Independent readback verified all **130** frozen file modes, Git blobs and SHA-256 values, the 78-file native TeX closure, workflow mirror and 129-file driver digest. The earlier local release executed these same frozen bytes before publication.

The actual [new remote run **39526895726**, attempt 1]({V['remote_run']}) **succeeded** at exactly `{SOURCE}`. Job **118983561729** ran from **2026-10-21T01:39:52Z** to **01:44:23Z**; all **11 steps** succeeded. The artifact's checkout receipt independently records the same source SHA and a successful build. No source/workflow repair or manual rerun was required.

Artifact **12314306857** was actually downloaded: **10,808,391 bytes**, **225 file members**, SHA-256

`{V['artifact_sha256']}`.

All ZIP member CRCs and extracted bytes were verified. The independent artifact readback completed **1,333 receipt/byte/identity consistency checks**. These are readback checks, not 1,333 extra mathematical executions. The actual remote execution comprises **68 mathematical commands**, **59** matching normal/optimized comparisons, three native LaTeX passes, the **233-page** native document with **78** actual TeX inputs, and the **390-source** historical assembly with **26-/883-page** PDFs. Every recorded command exit, source digest, actual log hash, comparison and declared compiler-input closure was reconstructed. The historical repository-wide gate remains explicitly unexecuted.

The actual remote native PDF has SHA-256

`{V['native_pdf_sha256']}`.

It is retained separately in `audit/current-ci-success-readback/artifact/current/native/main.pdf`. The local release PDF and its distinct hash above remain preserved. Neither PDF is substituted for the other execution's output.

The decoded job log is retained with narrowly identified authentication-header-reference lines removed. `JOB_LOG_RETRIEVAL.json` preserves its raw decoded-content hash, saved-content hash, exact redaction line list and reason. No credential or temporary signed download URL is stored. Mathematical and compilation logs from the artifact are retained exactly.

The first **readback-verifier** attempt expected a generated untracked build directory; the actual post-run status was empty, a clean checkout. That attempt, its script and output remain preserved. Only this readback predicate was corrected to accept clean status or the sole declared generated directory; the exact diff and successful subsequent execution are retained. This was not a CI, manuscript or mathematical-program failure, and no source repair or CI rerun was performed.

At the earlier observation `2026-10-21T01:37:28.119Z`, the run was still queued with no runner, steps or artifacts. That real snapshot is preserved in `audit/current-ci-readback/` and the pending evidence carrier `{PENDING}`. The later success is added under **`audit/current-ci-success-readback/`**; it does not rewrite the earlier observation. The source-stage metadata remains under `audit/remote-publication/source-release/`, and the complete pending-carrier metadata remains under `audit/remote-publication/pending-carrier/`.

This later evidence-only carrier preserves every frozen mathematical/build input and the workflow. Its `[skip ci]` commit records the actual successful source run, not a new mathematical test target. `PUBLICATION_STATUS.json` records source, local release, actual tested checkout, pending history and verified artifact as distinct identities.
'''
p.write_text(s[:start]+section+s[end:])
p=A/'README.md';s=p.read_text()
old='The full local entrypoint succeeded: 68 mathematical commands, 59 normal/optimized comparisons, the 233-page native manuscript and the 26-/883-page historical rebuild. The new [remote run 39526895726](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39526895726) was still **queued and unexecuted** at `2026-10-21T01:37:28.119Z`: no runner, steps or artifacts. Its requested head is the source commit above; no actual tested checkout is claimed. See `PUBLICATION_STATUS.json`, `VALIDATION.md` and `audit/current-ci-readback/` for this exact distinction.'
new=f'''Both the complete local entrypoint and the [actual remote run 39526895726]({V['remote_run']}) succeeded. The remote job tested exactly `{SOURCE}` and completed all 11 steps from 01:39:52 to 01:44:23 UTC: 68 mathematical commands, 59 normal/optimized comparisons, the 233-page native manuscript and the 26-/883-page historical rebuild. Artifact 12314306857 was downloaded and all 225 member files verified, with 1,333 receipt/identity checks. See `audit/current-ci-success-readback/`, `VALIDATION.md` and `PUBLICATION_STATUS.json`.

The earlier queued observations and pending evidence carrier `{PENDING}` remain intact. The later evidence-only child records completed CI without altering the mathematical source, workflow or prior execution evidence.'''
if s.count(old)!=1:raise RuntimeError('Unexpected README status')
p.write_text(s.replace(old,new))
p=A/'HISTORY_PRESERVATION_AUDIT.md'
p.write_text(p.read_text()+f'''\n## Successful current CI and preserved pending carrier\n\nThe later actual CI success is recorded separately: run 39526895726, job 118983561729, exact tested source `{SOURCE}`, all 11 steps successful from 01:39:52Z to 01:44:23Z. Artifact 12314306857 was downloaded and verified against its ZIP digest, all 225 members and source-bound command receipts. It contains the actual 68 mathematical commands, 59 normal/optimized comparisons, 233-page native manuscript and 26-/883-page historical PDFs. The success packet and its actual readback attempt history are in `audit/current-ci-success-readback/`.\n\nThe pending evidence carrier `{PENDING}` has parent `{SOURCE}`, root `3ec1a39998cef76f23fc1985a0df78bc0033bf4c`, article `2c542d7a279a7bc6fb8ea64dfa372e9bc1dcd9e4`. It recorded the truthful earlier 01:37 pending observation. Its exact metadata and actual protected ref-update receipts are preserved under `audit/remote-publication/pending-carrier/`; the subsequent success does not revise that history. Both evidence carriers leave all 130 frozen mathematical/build inputs and the dedicated workflow unchanged.\n\nThe next complete census, at `2026-10-21T01:48:10.271936+00:00` through `01:48:10.589175+00:00`, still has 1,300 heads / 434 A2-DYN refs. Relative to the post-source snapshot, exactly two heads moved: this authorized A2-DYN source branch to the pending evidence carrier, and the independently updated General Theta R75 branch from `bc2952aa9a9695fe9985d491a4156b8975024285` to `2c103f924720435700e947cc8df31b8b648f61e9`. The other 1,298 heads remained unchanged, with no additions or deletions. All 433 original A2-DYN refs and all 178 review refs remain unchanged.\n\nThe concurrent R75 descendant is a direct child whose complete delta adds only `papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory-publication`, tree `de90da14131edaee7aa96a0417dbca02c5e77b01`. Reconstructed before/after Git trees verify that all 139 other root entries, 55 other paper siblings and 30 pre-existing General Theta children are unchanged. No A2-DYN source, report, response, workflow or publication change is present. Full receipts are in `audit/remote-publication/r75-publication-followup/`. The independent concurrent branch movement is recorded rather than incorrectly attributed to this A2-DYN revision or suppressed from the final census.\n''')
p=A/'RESPONSE_TO_REFEREE.md'
p.write_text(p.read_text()+f'''\n## 8. Completed current CI addendum\n\nThe source run later completed successfully: run 39526895726, attempt 1, exact checkout `{SOURCE}`, job 118983561729, all 11 steps successful from 01:39:52Z to 01:44:23Z. The actually downloaded artifact 12314306857 and all 225 member files were verified. They establish the actual remote 68 mathematical commands, 59 normal/optimized comparisons, 233-page native manuscript with 78 TeX inputs, and 26-/883-page historical rebuild. The 1,333 readback consistency checks are not additional mathematical executions or an expert certificate. `audit/current-ci-success-readback/` retains the artifact, actual logs/receipts, exact source identity and successful verification.\n\nSection 7's earlier 01:37 pending observation remains true at its recorded time and is preserved in carrier `{PENDING}`. The completed-CI evidence is appended on the same authorized branch, with all frozen proof/build/workflow bytes unchanged. The first artifact-verifier attempt's overly specific post-run-status expectation, its one-predicate correction and the successful next readback are all retained; the CI itself required no repair or rerun. The historical repository-wide gate remains unexecuted.\n\nThe final census also records the independent General Theta R75 publication descendant, whose complete Git-tree delta contains no A2-DYN change. All original A2-DYN author, review, copy and response heads remain unchanged. Successful execution advances proof reproducibility; it does not close the normalized same-roof shortage, remaining joint analytic inputs or the final raw pointwise/inverse theorem.\n''')
p=A/'PROOF_DEPENDENCY_LEDGER.md';s=p.read_text()
old='record the completed local build and the pending remote run at its requested source SHA, without treating queued metadata as execution or either form of evidence as a continuum-proof certificate.'
new='record the completed local build and the independently verified successful remote run at the exact tested source SHA. The earlier queued observations remain preserved separately. Neither finite execution nor compiled output is a continuum-proof certificate.'
if s.count(old)!=1:raise RuntimeError('Unexpected ledger CI wording')
s=s.replace(old,new)
s+='''\n### Actual successful remote execution\n\nRun 39526895726 tested source `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9` and completed all 11 steps successfully. The independently downloaded artifact verifies 68 mathematical commands, 59 normal/optimized comparisons, a 233-page native manuscript and the 26-/883-page preserved historical rebuild. The 1,333 readback checks concern byte identities and actual execution receipts; they do not add mathematical hypotheses or promote an unresolved dynamical input. Earlier queued observations and the first readback-predicate correction remain preserved. The native pressure proof and its 27-file acyclicity reconstruction are unchanged.\n'''
p.write_text(s)
print(json.dumps({'metadata_updated':6,'verified_run':V['run_id'],'actual_tested_source':SOURCE,'all_steps_successful':True,'frozen_source_modified':False}))
