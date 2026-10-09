#!/usr/bin/env python3
"""Append-only publication for the explicitly authorized R24 research branch."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path.cwd();P=Path('papers/General-Theta-Foundations-I-restart');B=P/'r24-renewal-geometry'
BRANCH='foundation/general-theta-restart-r24-renewal-geometry-research-2026-10-09'
OPENING='e524d576c0f147e6fcd2cc7828c28cd79233d826'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d';REVIEW='212bec0b6f254990552584db35473e0ac108e2d7';R23='6dd51dd292bb70e8bd3015d3c376f8c335862d66'
REPORT='GENERAL_THETA_FOUNDATIONS_I_RESTART_R22_DISCOUNTED_RESPONSE_EXTERNAL_REFEREE_REPORT_R22.md'
ANCHORS={'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,'review/general-theta-restart-r22-discounted-response-external-top4-referee-r22-2026-10-09':REVIEW,'foundation/general-theta-restart-r23-regenerative-transfer-research-2026-10-09':R23}
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def cmd(*args):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'failed '+repr(args)+'\n'+p.stdout[-18000:]);return p.stdout.strip()
def git(*args):return cmd('git',*args)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def remote(branch):return git('ls-remote','origin','refs/heads/'+branch).split()[0]
def verifier():
    spec=importlib.util.spec_from_file_location('r24verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def preserve():
    result={}
    entries=git('ls-tree',OPENING+':'+str(P)).splitlines()
    for line in entries:
        meta,name=line.split('\t',1)
        if name==B.name:continue
        path=str(P/name);old=meta.split()[2];now=git('rev-parse','HEAD:'+path)
        check(now==old,'changed inherited tree '+path);result[path]=old
    for path in ['foundations/general-theta/General_Theta_Foundations_v0.1.md','foundations/general-theta/RESTART_CHARTER.md','foundations/general-theta/REALIZATION_REGISTRY.md',REPORT]:
        old=git('rev-parse',OPENING+':'+path);check(git('rev-parse','HEAD:'+path)==old,'changed pinned file '+path);result[path]=old
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'anchor moved: '+branch)
    return result
def manifest():
    m=verifier();files={}
    for name in m.sources():
        data=(ROOT/B/name).read_bytes();files[name]={'sha256':m.sha256(data),'git_blob_sha':m.git_hash('blob',data)}
    (ROOT/B/'SOURCE_MANIFEST.json').write_text(json.dumps({'format':'native-ordinary-source-v1','files':files},sort_keys=True,indent=2)+'\n')
    return m.verify()
def environment(**values):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in values.items():f.write(f'{k}={v}\n')
def package(path,include_artifacts,binding):
    names=[]
    for name in git('ls-files',str(P),'foundations/general-theta','.github/scripts/theta-r24-publish.py','.github/workflows/theta-r24-renewal.yml',REPORT).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if Path(name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R24_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)
def prepare():
    check(os.environ.get('GITHUB_REF_NAME')==BRANCH,'wrong branch')
    bootstrap=git('rev-parse','HEAD');check(remote(BRANCH)==bootstrap,'branch changed before source publication')
    git('fetch','--no-tags','origin',OPENING,CANON,REVIEW,R23)
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    old=preserve();audit=manifest();git('add',str(B/'SOURCE_MANIFEST.json'))
    if git('diff','--cached','--name-only'):
        git('commit','-m','source(theta restart R24): bind complete ordinary manuscript and audit manifest')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));check(tree==audit['native_source_tree_sha'],'native Git tree mismatch')
    check(remote(BRANCH)==bootstrap,'source lease changed');git('push','origin','HEAD:refs/heads/'+BRANCH)
    check(remote(BRANCH)==source,'source readback mismatch')
    data={'source_commit':source,'native_source_tree_sha':tree,'bootstrap_commit':bootstrap,'opening_import_commit':OPENING,'canonical_commit':CANON,'review_commit':REVIEW,'r23_contract_commit':R23,'preserved_objects':old,'anchor_readback':ANCHORS,'stage':'SOURCE_ONLY; no build result asserted'}
    export=Path(os.environ['RUNNER_TEMP'])/'r24-source-export';export.mkdir(exist_ok=True)
    count=package(export/'R24_ordinary_source.zip',False,data)
    (export/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r24-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=tree,BOOTSTRAP_SHA=bootstrap,SOURCE_EXPORT_DIR=str(export))
    print(json.dumps(data,sort_keys=True,indent=2))
def artifacts():
    source=os.environ['SOURCE_SHA'];check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed during build')
    audit=verifier().verify();check(audit['native_source_tree_sha']==os.environ['EXPECTED_TREE'],'source projection mutated')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'bad build source receipt')
    old=preserve();data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r24-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=old,source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],non_force_push=True,limitations='Integrity and finite arithmetic checks, not continuum proof or priority certification. Only native R24 and retained companions are rebuilt.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit has source changes')
    git('commit','-m','artifacts(theta restart R24): full immutable builds and source-bound receipts')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact not direct child of source')
    check(remote(BRANCH)==source,'artifact publication lease changed');git('push','origin','HEAD:refs/heads/'+BRANCH);check(remote(BRANCH)==artifact,'artifact readback mismatch')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED')
    out=Path(os.environ['RUNNER_TEMP'])/'r24-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R24_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_source_tree_sha':os.environ['EXPECTED_TREE'],'packaged_files':count,'files':{p.name:digest(p) for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['source','artifacts']);a=p.parse_args()
    (prepare if a.stage=='source' else artifacts)()
