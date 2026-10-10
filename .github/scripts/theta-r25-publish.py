#!/usr/bin/env python3
"""Immutable source verification and create-only R25 artifact publication."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,subprocess,zipfile
from pathlib import Path
ROOT=Path.cwd();P=Path('papers/General-Theta-Foundations-I-restart');B=P/'r25-retained-state'
SOURCE_BRANCH='foundation/general-theta-restart-r25-retained-state-source-2026-10-10'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r25-retained-state-2026-10-10'
EXPECTED_TREE='9b0100d1724d24c1ff8dc55c6e1250a7417720db'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d';REVIEW='36422feadc4ccb99aaf12efb33a18bfd44cb3646'
IMPORT='16fbfe516d3a8bd993ae8f1b6784ee07d52c4957';DRAFT='0ffcb5c85ccf9b5d199f240506314d0cf507eecd'
REPORT='GENERAL_THETA_FOUNDATIONS_I_RESTART_R24_RENEWAL_GEOMETRY_EXTERNAL_REFEREE_REPORT_R24.md'
ANCHORS={'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,'review/general-theta-restart-r24-renewal-geometry-external-top4-referee-r24-2026-10-10':REVIEW,'foundation/general-theta-restart-r25-retained-state-research-2026-10-10':CANON,'foundation/general-theta-restart-r25-retained-state-manuscript-2026-10-10':DRAFT}
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def cmd(*args):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'failed '+repr(args)+'\n'+p.stdout[-18000:]);return p.stdout.strip()
def git(*args):return cmd('git',*args)
def remote(branch):
    text=git('ls-remote','origin','refs/heads/'+branch);return text.split()[0] if text else None
def verifier():
    spec=importlib.util.spec_from_file_location('r25verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def preserve():
    result={}
    for line in git('ls-tree',REVIEW+':'+str(P)).splitlines():
        meta,name=line.split('\t',1);path=str(P/name);old=meta.split()[2]
        check(git('rev-parse','HEAD:'+path)==old,'changed inherited object '+path);result[path]=old
    for path in ['foundations/general-theta/General_Theta_Foundations_v0.1.md','foundations/general-theta/RESTART_CHARTER.md','foundations/general-theta/REALIZATION_REGISTRY.md',REPORT]:
        old=git('rev-parse',REVIEW+':'+path);check(git('rev-parse','HEAD:'+path)==old,'changed pinned file '+path);result[path]=old
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result
def environment(**values):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in values.items():f.write(f'{k}={v}\n')
def package(path,include_artifacts,binding):
    names=[]
    root_reports=[x for x in git('ls-files').splitlines() if x.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and x.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r25-publish.py','.github/workflows/theta-r25-retained.yml']+root_reports
    for name in git('ls-files',*scope).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R25_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)
def prepare():
    check(os.environ.get('GITHUB_REF_NAME')==SOURCE_BRANCH,'wrong source branch')
    source=git('rev-parse','HEAD');check(remote(SOURCE_BRANCH)==source,'source branch changed')
    git('fetch','--no-tags','origin',CANON,REVIEW,IMPORT,DRAFT)
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    old=preserve();audit=verifier().verify();tree=git('rev-parse','HEAD:'+str(B))
    check(tree==EXPECTED_TREE==audit['native_source_tree_sha'],'ordinary source tree mismatch')
    check(git('rev-parse','HEAD^')==DRAFT,'source must be a direct child of published manuscript')
    check(not git('diff','--name-only'),'source verification mutated tracked files')
    data={'source_commit':source,'native_source_tree_sha':tree,'draft_commit':DRAFT,'canonical_first_import_commit':IMPORT,'canonical_commit':CANON,'review_commit':REVIEW,'preserved_objects':old,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'stage':'SOURCE_ONLY; no build result asserted','publication_policy':'No existing branch is updated; source stays fixed and artifact branch must not exist before publication.'}
    export=Path(os.environ['RUNNER_TEMP'])/'r25-source-export';export.mkdir(exist_ok=True)
    count=package(export/'R25_ordinary_source.zip',False,data)
    (export/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r25-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=tree,SOURCE_EXPORT_DIR=str(export));print(json.dumps(data,sort_keys=True,indent=2))
def artifacts():
    source=os.environ['SOURCE_SHA'];check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed')
    audit=verifier().verify();check(audit['native_source_tree_sha']==EXPECTED_TREE,'source projection mutated')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r25-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],limitations='Full native and declared complete companions only; finite checks and rebuilds are not continuum proof or priority certificates.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit changes ordinary source')
    git('commit','-m','artifacts(theta restart R25): immutable native and complete retained builds')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact not direct child of source')
    check(remote(SOURCE_BRANCH)==source,'source ref changed');check(remote(ARTIFACT_BRANCH) is None,'artifact destination already exists; refusing update')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH)
    check(remote(ARTIFACT_BRANCH)==artifact,'artifact readback failed');check(remote(SOURCE_BRANCH)==source,'source ref was changed')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r25-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R25_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_source_tree_sha':EXPECTED_TREE,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
