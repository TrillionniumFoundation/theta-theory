from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil

W=Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019b')
R=W.parent/'theta-theory/papers/A2-DYN-full-physical-source-author-revision'
D=R/'delivery/publication/full-physical-source-20261019'
C1='694952d7d6b886d0087e8560da721bfc980adbc3'
C2='228ec6a639d4d195a1a8b869a04dae6f49fece0e'
MATH='ebe48d08b94fc0dceecce96ecef8e0bc81d91918521ee1ba24558d549d558b26'
MANIFEST='13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997'
def require(ok,message):
    if not ok: raise RuntimeError(message)
def put(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

parser=argparse.ArgumentParser()
parser.add_argument('--ci-directory',type=Path,required=True)
parser.add_argument('--verification',type=Path,required=True)
args=parser.parse_args()
v=json.loads(args.verification.read_bytes())
require(v['status']=='passed' and v['actual_current_ci_success_verified'] is True,'Actual CI verification must pass')
require(v['exact_head']==C2 and v['run_id']==39229329979,'Wrong actual CI head/run')
require(v['article_tree_sha']=='826219579509e91c87c8dfb0c6348e2c42dba178' and v['root_tree_sha']=='431dfd86fcd60e50a1469af38343afc470527752','Wrong tested trees')
require(v['mathematical_source_sha256']==MATH and v['frozen_manifest_sha256']==MANIFEST,'Wrong tested mathematical source')
require(v['frozen_inputs_verified_against_tested_head']==1668 and v['frozen_input_bytes']==122736124,'Wrong source manifest extent')
require(v['math_commands_verified']==46 and v['normal_optimized_actual_pairs_verified']==37 and v['native_pages']==174,'Wrong actual execution extent')
require(v['native_tool_inputs_verified_against_tested_head']==101 and v['actual_pdflatex_passes']==3,'Wrong native inputs/build')
require(v['continuum_mathematical_proof_certificate'] is False and v['independent_human_specialist_certification'] is False,'Overstated mathematical status')
require(hashlib.sha256((R/'SOURCE_MANIFEST.json').read_bytes()).hexdigest()==MANIFEST,'Frozen manifest changed')
require(args.verification.resolve().is_relative_to(args.ci_directory.resolve()),'Verification must lie in the archived actual CI directory')
require((W/'remote-verification-C2').is_dir(),'Missing independent C2 remote verification')

for n in ['C2_FILE_IDENTITIES.json','C2_ROOT_EXPECTED.json','C2_INITIAL_REMOTE_READBACKS.json','C2_TRANSPORT_EXECUTION_RECEIPTS.json','C2_DELTA_SCOPE.json','C2_TREE_PLAN.json']:
    shutil.copy2(W/n,D/n)
shutil.copy2(W/'remote-verification/README.md',D/'C1-remote-verification/README.md')
shutil.copytree(W/'remote-verification-C2',D/'C2-remote-verification',dirs_exist_ok=True)
shutil.copytree(args.ci_directory,D/'actual-C2-ci',dirs_exist_ok=True)
shutil.copy2(__file__,D/'prepare_c3_documents.py')

refs=['revision/a2-dyn-full-physical-source-2026-10-19','referee-response/a2-dyn-full-physical-source-2026-10-19','referee-copy/a2-dyn-full-physical-source-2026-10-19']
relative_verification='delivery/publication/full-physical-source-20261019/actual-C2-ci/'+args.verification.resolve().relative_to(args.ci_directory.resolve()).as_posix()
current_ci={
    'status':v['run_status'],'conclusion':v['run_conclusion'],
    'run_id':v['run_id'],'run_url':'https://github.com/TrillionniumFoundation/theta-theory/actions/runs/'+str(v['run_id']),
    'job_id':v['job_id'],'tested_commit':C2,
    'tested_root_tree':v['root_tree_sha'],'tested_article_tree':v['article_tree_sha'],
    'actual_job_steps_verified':v['actual_job_steps_verified'],
    'artifact_id':v['artifact_id'],'artifact_bytes':v['artifact_bytes'],
    'artifact_sha256':v['artifact_sha256'],'artifact_files':v['artifact_files'],
    'verified_utc':v['verified_utc'],'verification_receipt':relative_verification,
    'mathematical_commands_verified':v['math_commands_verified'],
    'normal_optimized_output_pairs_verified':v['normal_optimized_actual_pairs_verified'],
    'native_pages':v['native_pages'],'native_pdf_sha256':v['native_pdf_sha256'],
    'fresh_historical_receipt':v['fresh_historical_receipt'],
    'fresh_historical_commands_verified':v['fresh_historical_commands_verified'],
    'historical_documents':v['historical_documents'],
    'actual_current_ci_success_verified':True,
    'containing_evidence_commit_is_separate_from_tested_head':True,
    'scope':'Actual completed dedicated workflow, exact C2 checkout, source/output/artifact integrity. The containing publication-evidence successor preserves the same mathematical source and is not a separately executed CI checkout.',
}
status=json.loads((R/'PUBLICATION_STATUS.json').read_bytes())
status.pop('new_refs_last_observed_at',None)
status.update({
    'publication_state':'complete native author revision with actual successful C2 CI and archived post-CI publication evidence',
    'source_carrier_commit':C1,'tested_commit':C2,'evidence_commit_parent':C2,
    'new_refs':refs,'current_ci':current_ci,
    'mathematical_source_sha256':MATH,'source_manifest_sha256':MANIFEST,
    'source_manifest_inputs':1668,'source_manifest_bytes':122736124,
    'full_raw_pointwise_llt_complete':False,'four_coordinate_inversion_complete':False,
    'unresolved_original_interfaces':['full shallow same-roof positive-source capacity and essential-height shortage','positive singular-pairing/short-segment endpoint trace charges','unrestricted full physical word-pressure input','remaining uniform spectral/high-frequency, exact arithmetic, microscopic conditional and long-time inversion interfaces'],
})
put(R/'PUBLICATION_STATUS.json',status)
receipt={
    'schema':'A2-DYN-full-physical-source-publication-v1',
    'recorded_utc':datetime.now(timezone.utc).isoformat(),
    'state':'actual completed C2 CI verified; post-CI evidence successor of the tested commit',
    'base_commit':'fdf2603c8bf422314f199fa431086485a0d1ebb5',
    'complete_source_commit':C1,'complete_source_article_tree':'f0e29499f0d5de75103b6f52cc464945071ea04b',
    'complete_source_files':2688,'complete_source_bytes':285948269,
    'tested_commit':C2,'tested_root_tree':v['root_tree_sha'],'tested_article_tree':v['article_tree_sha'],
    'tested_article_files':2710,'tested_article_bytes':292904889,
    'new_author_refs':refs,'containing_evidence_commit_parent':C2,
    'mathematical_source_sha256':MATH,'source_manifest_sha256':MANIFEST,
    'frozen_source_inputs':1668,'frozen_source_bytes':122736124,
    'actual_ci':current_ci,
    'local_native_pdf':{'path':'delivery/A2-DYN-full-physical-source-author-revision.pdf','pages':174,'sha256':'cbf13c010cb2eff0ca1f8fa14a4753aa32c8418c0d75c00135c7db8f016c0de9'},
    'native_scope':{'inherited_core':[260,313],'new_core':[314,315],'new_complete_proofs':14,'complete_active_bodies':56,'reachable_TeX_files':66,'native_labels':811},
    'scope':'Only the new A2-DYN article and dedicated workflow are added to the fixed baseline. The containing evidence commit changes only three explicitly manifest-excluded root metadata files and adds publication/source-gate evidence. Final Git commit/ref/tree identities are independently read after push; no self-referential containing commit SHA is invented here.',
    'full_raw_pointwise_llt_complete':False,'four_coordinate_inversion_complete':False,
    'independent_human_referee_or_journal_acceptance_claimed':False,
}
put(R/'PUBLICATION_RECEIPT.json',receipt)
put(D/'ACTUAL_CI_PUBLICATION_SUMMARY.json',receipt)
(R/'REMOTE_TRANSPORT_STATUS.md').write_text(f'''# Complete author source and actual successful CI

The complete first author source was actually committed and pushed as **{C1}**, from the fixed complete predecessor **fdf2603c8bf422314f199fa431086485a0d1ebb5**. Its 2,688 actual files, 285,948,269 bytes and all 108 descendant subtrees were independently reconstructed from nontruncated GitHub readbacks. The article tree is **f0e29499f0d5de75103b6f52cc464945071ea04b** and repository root **56031be3c69251f8eadce010b38d576eaf9497e6**.

The subsequent nonforce metadata push **{C2}** actually triggered [GitHub Actions run {v['run_id']}](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/{v['run_id']}). Its observed outcome is **completed / success**, with all **{v['actual_job_steps_verified']}** job steps successful. The exact tested article tree is **{v['article_tree_sha']}**, in root **{v['root_tree_sha']}**. All 2,710 tested article files retain their expected identities.

## Actual downloaded and verified output

Artifact **{v['artifact_id']}** was actually downloaded: **{v['artifact_bytes']:,} bytes**, SHA-256 **{v['artifact_sha256']}**. Every one of its **{v['artifact_files']}** file members was read, CRC-checked and hashed. The independent verifier matched all 1,668 frozen source inputs, all 101 native/tool inputs, all 46 mathematical commands and 37 normal/optimized output pairs. It verified the actual three TeX passes, 174-page native PDF and matching native auxiliary labels, and selected the historical nine-command rebuild actually produced after this run's native phase, yielding the original 26-page main and 883-page supplement. Earlier carried-in historical receipts remain separately identified.

The exact job log, API observations, original ZIP, complete artifact member manifest, command-level verification and invocation return codes are retained under `delivery/publication/full-physical-source-20261019/actual-C2-ci/`. The verified CI native PDF has SHA-256 **{v['native_pdf_sha256']}**. The delivered local native PDF has its separate actual hash; neither build is silently substituted into the other's receipt.

## Post-CI evidence commit and source identity

The commit containing this record is a publication-evidence successor of the tested C2 head. It preserves the full mathematical-source fingerprint **{MATH}** and source-manifest SHA-256 **{MANIFEST}**. Its commit message suppresses a redundant CI event because it adds observed publication evidence and updates only three explicitly excluded publication metadata files. It is **not** represented as a separately executed CI checkout. A fresh actual source gate verifies the unchanged frozen inputs after evidence assembly.

The three new author refs are `revision/a2-dyn-full-physical-source-2026-10-19`, `referee-response/a2-dyn-full-physical-source-2026-10-19`, and `referee-copy/a2-dyn-full-physical-source-2026-10-19`. Each is advanced with a nonforce, expected-parent update. Final containing-commit and ref identities are read after that push. Earlier articles, companion material, reviews and workflows retain their original tree objects; no existing review ref is repurposed.

The new theorems concern complete physical-source roof regularity, actual singular bulk integrability, critical-band volume and the complete deep-source/regular-interior budgets in their stated norms. Successful CI and source transport do not complete the original essential-height shortage, singular trace charges, unrestricted pressure or final raw pointwise local limit and four-coordinate inversion interfaces. Those objectives and their minimal remaining closure conditions remain explicit in the manuscript, response and ledger.
''')
print(json.dumps({'actual_CI_verified':True,'tested_commit':C2,'run':v['run_id'],'artifact':v['artifact_id'],'archived_ci_files':sum(p.is_file() for p in (D/'actual-C2-ci').rglob('*')),'scientific_source_changed':False}))
