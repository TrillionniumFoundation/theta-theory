#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json
ARTICLE=Path('/workspace/scratch/35c64a3513c5/theta-theory-next/papers/A2-DYN-physical-roof-variation-author-revision')
SOURCE='6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9'
OBSERVED='2026-10-21T01:37:28.119Z'
ROOT='ad34fd91ad2f1c6e594d3bbe437417aba524bf87'
TREE='4f41b3a98487a1ae0507d40390aca030c5520e19'
RUN='https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39526895726'
def replace(name,old,new):
 p=ARTICLE/name;s=p.read_text()
 if s.count(old)!=1:raise RuntimeError(f'Expected one replacement in {name}: {s.count(old)}')
 p.write_text(s.replace(old,new))
p=ARTICLE/'PUBLICATION_STATUS.json';s=json.loads(p.read_text())
if s['remote_publication']['state']!='not_yet_published':raise RuntimeError('Metadata has already been updated')
s['schema']='a2-dyn-physical-roof-variation-publication-v2'
s['scope']='Published complete mathematical source and completed local author release, with actual queued current-revision CI readback. The later evidence-only carrier is identified by Git ancestry and its final ref; no unobserved checkout, execution or artifact is claimed.'
s['updated_utc']=datetime.now(timezone.utc).isoformat()
s['remote_publication']={
 'state':'source_published_and_independently_read_back',
 'source_commit':SOURCE,'source_root_tree':ROOT,'source_article_tree':TREE,
 'source_parent':'4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e',
 'workflow_blob':'6246879e13fdd5937ebf9c5a9787c24baefb59b5',
 'source_changed_paths':5261,'source_change_status':'all_additions_within_new_article_and_dedicated_workflow',
 'published_frozen_files_independently_verified':130,
 'source_readback':'audit/current-ci-readback/PUBLISHED_SOURCE_READBACK.json',
 'publication_receipts':'audit/remote-publication/',
 'source_release_metadata_preserved':'audit/remote-publication/source-release/',
 'evidence_carrier':'This document is carried by a metadata/evidence-only child of source_commit; identify the carrier by the repository commit containing this version. The future carrier SHA is not self-embedded.'}
s['current_revision_ci']={
 'state':'queued_not_executed','observed_at_utc':OBSERVED,'run_id':39526895726,
 'run_attempt':1,'run_url':RUN,'run_created_at':'2026-10-21T01:22:05Z',
 'requested_head_sha':SOURCE,'status':'queued','conclusion':None,
 'job_id':118983561729,'job_status':'queued','job_conclusion':None,
 'runner_id':0,'executed_steps':0,'artifact_count':0,
 'actual_tested_checkout_sha':None,'checkout_verified_from_execution':False,
 'verified_mathematical_commands':0,'verified_native_compile':False,
 'verified_historical_compile':False,'artifact_downloaded':False,'artifact_verified':False,
 'readback':'audit/current-ci-readback/PENDING_CI_READBACK.json',
 'scope':'The published source has been verified independently. Queued workflow metadata does not establish a runner checkout or any remote command execution.',
 'workflow_manually_rerun':False,'failure_cause_inferred':False}
s['local_validation']['frozen_bytes_verified_identical_to_published_source']=SOURCE
s['local_validation']['actual_git_checkout_at_release_claimed']=False
s['local_validation']['source_identity_note']='The release executed frozen local bytes before publication; independent readback subsequently verified all 130 frozen published inputs. It was not a later local checkout of the published commit.'
s['pressure_dependency_acyclicity']={'state':'internally_reconstructed','source_commit':SOURCE,'source_files':27,
 'record':'audit/mathematical-reconstruction/pressure-dependency-acyclicity/DEPENDENCY_ACYCLICITY_326.md',
 'independent_human_certification':False}
p.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
replace('VALIDATION.md',
'At the local source-freeze stage, the new dedicated workflow is prepared but its remote execution has not yet occurred. `PUBLICATION_STATUS.json` and the post-publication audit will record the actual new source commit, run, tested SHA, job outcome and artifact after retrieval. A branch name, workflow definition, queued job or local success is not a remote success.',
f'''The complete source was published as **`{SOURCE}`**, root tree `{ROOT}`, article tree `{TREE}`, on `revision/a2-dyn-physical-roof-variation-2026-10-21`. Git/API readback confirms the exact parent and all 5,261 additions, confined to the new article and its dedicated workflow. A separate direct source readback verified all **130** frozen file modes, Git blobs and SHA-256 values, the 78-file native TeX closure, workflow mirror and 129-file driver digest. The locally built bytes are therefore the published mathematical bytes. The local release occurred before publication; it is not represented as a later checkout of that commit.

The source push created [run **39526895726**, attempt 1]({RUN}) at `2026-10-21T01:22:05Z`. At the actual final CI observation **`{OBSERVED}`**, the run and job **118983561729** remained **queued**, with conclusion null, runner ID zero, **zero executed steps** and **zero artifacts**. The independent job-step endpoint also returned an empty list. No remote checkout SHA, test execution, compile, job log or artifact verification is therefore asserted for this revision. The workflow's planned 68 commands and 59 comparisons are not remote execution results. The cause of the queue is not inferred.

`audit/current-ci-readback/` preserves the initial and subsequent actual snapshots, the independently fetched published input bytes and their manifest, and the unexecuted artifact-verification program. `PUBLICATION_STATUS.json` records the same pending state. This evidence-only descendant keeps every frozen mathematical/build input and the workflow unchanged; `[skip ci]` prevents its metadata packaging from being mistaken for a second mathematical test target. The exact source-stage metadata remains in `audit/remote-publication/source-release/`.''')
replace('README.md',
'The final publication record separates the mathematical source commit, the actual tested CI commit and any later evidence-only carrier.',
f'''The published mathematical source commit is **`{SOURCE}`**, article tree `{TREE}`. All 130 frozen inputs were independently read back and match the completed local release. The later evidence-only child preserves these bytes and the original source-stage records.

The full local entrypoint succeeded: 68 mathematical commands, 59 normal/optimized comparisons, the 233-page native manuscript and the 26-/883-page historical rebuild. The new [remote run 39526895726]({RUN}) was still **queued and unexecuted** at `{OBSERVED}`: no runner, steps or artifacts. Its requested head is the source commit above; no actual tested checkout is claimed. See `PUBLICATION_STATUS.json`, `VALIDATION.md` and `audit/current-ci-readback/` for this exact distinction.''')
replace('HISTORY_PRESERVATION_AUDIT.md',
'Current successful CI readback is added separately; the historical observation that a job was queued is not rewritten into a fictitious contemporary success.',
'The predecessor\'s successful CI readback and this revision\'s queued CI observations are added separately; a historical observation that a job was queued is not rewritten into a fictitious contemporary success.')
p=ARTICLE/'HISTORY_PRESERVATION_AUDIT.md'
p.write_text(p.read_text()+f'''\n## Published source and post-push reconciliation\n\nThe complete new source is `{SOURCE}`, parent `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e`, root `{ROOT}`, article `{TREE}`. Its sole tree delta has 5,261 additions: 5,260 article files and the dedicated workflow. The preserved predecessor subtree still has the exact original tree `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`. The independent frozen-input readback verifies all 130 mathematical/build files and the workflow identity. Source-stage metadata is preserved byte for byte under `audit/remote-publication/source-release/`; the later evidence-only child changes no frozen input.\n\nThe fresh post-push census at `2026-10-21T01:24:45.727845+00:00` through `01:24:46.046360+00:00` contains **1,300 heads**, including **434 A2-DYN refs / 218 distinct head commits**. All 1,299 pre-push heads, including all **433 old A2-DYN refs** and all 178 review refs, are unchanged. The only addition relative to the pre-push census is this source branch. Relative to the initial 1,298-head census, the additional concurrent General Theta R75 branch was also inspected: its complete final delta is confined to `papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory`. Six complete nonrecursive Git-tree reads and reconstruction of their hashes confirm that it adds no A2-DYN source, review, response, workflow or publication change. It supplies no replacement A2-DYN baseline or controlling report.\n\nThe complete raw snapshots, exact R75 ancestry and all tree-scope receipts are in `audit/remote-publication/post-publication-provenance/`. The raw 1,300-head snapshot has SHA-256 `cb505b15cbbdad49e250dfe02c427562238c41fefebcc651344c773cd897eb06`. These are timestamped preservation facts, not claims about unobserved later changes by other repository users.\n\nThe new source push created CI run 39526895726. At `{OBSERVED}` it was still queued with no runner, executed steps or artifacts. The source's actual local build and the predecessor's actual successful remote run remain separate evidence. No successful new remote execution is claimed.\n''')
p=ARTICLE/'RESPONSE_TO_REFEREE.md'
p.write_text(p.read_text()+f'''\n## 7. Actual publication addendum\n\nThe complete source and this response were published together at `{SOURCE}`, article tree `{TREE}`, on the one authorized new revision branch. All 130 frozen mathematical/build files were independently read back and match the bytes used for the completed local release: 68 mathematical commands, 59 normal/optimized comparisons, and actual native/historical PDFs of 233, 26 and 883 pages. The final statement-level acyclicity reconstruction for 326 is preserved separately; it identifies the exact differential in native 313 and confirms that the old full-word pressure premise is downstream, not an ancestor. This is an internal author reconstruction, not a new referee opinion.\n\nAt `{OBSERVED}`, the actual new CI run 39526895726 and job 118983561729 were still queued, with no runner, steps or artifacts. No remote checkout or successful remote mathematical execution is claimed. `audit/current-ci-readback/` contains the actual snapshots and source identities; `VALIDATION.md` distinguishes the completed local release from the pending remote run. The evidence-only child of the source commit preserves all proof bytes and the original source-stage publication records.\n\nThe post-source census contains 1,300 heads / 434 A2-DYN refs; all 1,299 pre-push heads and all 433 prior A2-DYN refs remain unchanged at that observation. The concurrent General Theta R75 branch was checked through exact tree identities and contains no A2-DYN delta. It neither changes the controlling report nor supplies a favorable A2-DYN review.\n''')
print(json.dumps({'source_commit':SOURCE,'ci_state':'queued_not_executed','ci_observed_at':OBSERVED,'updated_metadata':['PUBLICATION_STATUS.json','VALIDATION.md','README.md','HISTORY_PRESERVATION_AUDIT.md','RESPONSE_TO_REFEREE.md'],'frozen_mathematical_source_modified':False}))
