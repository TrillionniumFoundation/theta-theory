#!/usr/bin/env python3
"""Materialize ordinary R34 text sources, then publish an artifact-only child.
The compressed Git blobs are transport only; they are not manuscript source. The mathematical source is committed
and pushed as ordinary files before any build; builds never modify that commit.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,io,json,lzma,os,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path.cwd(); P=Path('papers/General-Theta-Foundations-I-restart'); B=P/'r34-bellman-acquisition'
SOURCE_BRANCH='foundation/general-theta-restart-r34-bellman-acquisition-source-2026-10-11'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r34-bellman-acquisition-2026-10-11'
TRANSPORT_BLOBS=['24be3c31dd1aeda811866b5fc371693a599519ea', 'd1e20b9c9c3eacba0e76e58910eabd1e95c9eb54', '4a2ccf018d58938984d4059de99f0a82695166ca', '5eff76f20ab685348bc15281636fe2cd5b6b017b', '24b75716270bc1271fe034630a4e99e4f3f4be3f', '936aab6cf80f670a207e4d5849574c4138f6d7a7', 'e07182fe50a13ca05859daf6179c51c37ed2b4fc', '40a05e0bb3de2c606816da5b16c4fbd1e3e025ff', 'a315d7f3a5d988b7ca7a5a0c587bb494ca6f509a', 'e854e5ef76c81789a065136419e06992ba7b15ba']
TRANSPORT_SHA256='6be437d2c7daec1815a2eea25fd2991140b1457fe4bea2d01a93e12acb0df8c3'
EXPECTED_PROJECTION='eb89296ea9a5a1e3c42a08f573825ed86c21cd25'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='65bd07d89b04274c587d2ae4100511d99c39b0f2'
OLD='74e221a3fc94b44600d3c7b6717d7e4370097ed4'
MATHEMATICS='0982c854ddc20c2725f12f0fed67d61111776158'
INTAKE='5bc7f10b41e572d00d927c94e0fbc5f6ec0ba531'
REPORT_BLOB='3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21'
ANCHORS={
 'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,
 'review/general-theta-restart-r32-bayesian-curvature-external-top4-referee-r32-2026-10-11':REVIEW,
 'referee-ready/general-theta-restart-r32-bayesian-curvature-2026-10-11':MATHEMATICS,
 'foundation/general-theta-restart-r33-controlled-acquisition-research-2026-10-11':OLD,
 'foundation/general-theta-restart-r34-bellman-acquisition-research-2026-10-11':INTAKE,
}

def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def cmd(*args):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'failed '+repr(args)+'\n'+p.stdout[-16000:]);return p.stdout.strip()
def git(*args):return cmd('git',*args)
def remote(branch):
    v=git('ls-remote','origin','refs/heads/'+branch);return v.split()[0] if v else None
def verifier():
    spec=importlib.util.spec_from_file_location('r34verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def environment(**values):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in values.items():f.write(f'{k}={v}\n')
def preserve():
    result={}
    for line in git('ls-tree',OLD+':'+str(P)).splitlines():
        meta,name=line.split('\t',1);path=str(P/name);sha=meta.split()[2]
        check(git('rev-parse','HEAD:'+path)==sha,'changed inherited source '+path);result[path]=sha
    for name in ('General_Theta_Foundations_v0.1.md','RESTART_CHARTER.md','REALIZATION_REGISTRY.md'):
        path='foundations/general-theta/'+name;sha=git('rev-parse',CANON+':'+path)
        check(git('rev-parse','HEAD:'+path)==sha,'changed control '+path);result[path]=sha
    path=str(B/'review_inputs/R32_EXTERNAL_REFEREE_REPORT.md')
    check(git('rev-parse','HEAD:'+path)==REPORT_BLOB,'review input changed');result[path]=REPORT_BLOB
    path=str(P/'THEOREM_TARGETS.md');sha=git('rev-parse',CANON+':'+path)
    check(git('rev-parse','HEAD:'+path)==sha,'changed theorem targets');result[path]=sha
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result

def package(path,include_artifacts,binding):
    reports=[x for x in git('ls-files').splitlines() if x.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and x.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r34-publish.py','.github/workflows/theta-r34-bellman-acquisition.yml']+reports
    names=[]
    for name in git('ls-files',*scope).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R34_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)

def prepare():
    check(os.environ.get('GITHUB_REF_NAME')==SOURCE_BRANCH,'wrong source branch')
    bootstrap=git('rev-parse','HEAD');check(remote(SOURCE_BRANCH)==bootstrap,'source branch moved')
    git('fetch','--no-tags','origin',CANON,REVIEW,OLD,MATHEMATICS,INTAKE)
    check(git('rev-parse','HEAD^')==INTAKE,'bootstrap must descend directly from canonical intake')
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    preserved=preserve()
    pieces=[]
    for blob in TRANSPORT_BLOBS:
        url=f'https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/blobs/{blob}'
        req=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
        with urllib.request.urlopen(req,timeout=60) as response:data=json.load(response)
        piece=base64.b64decode(data['content'])
        check(hashlib.sha1(b'blob '+str(len(piece)).encode()+b'\0'+piece).hexdigest()==blob,'transport piece identity mismatch')
        pieces.append(piece)
    archive=b''.join(pieces);check(hashlib.sha256(archive).hexdigest()==TRANSPORT_SHA256,'transport hash mismatch')
    decoded=json.loads(lzma.decompress(archive).decode('utf-8'));check(isinstance(decoded,dict),'invalid transport dictionary')
    if decoded:
        for name,value in decoded.items():
            p=Path(name);check(not p.is_absolute() and '..' not in p.parts and p.parts and not any(v in p.parts for v in ('artifacts','evidence','__pycache__','.git','review_inputs')),'unsafe source entry')
            dest=ROOT/B/p
            check(not dest.exists() or name=='RESEARCH_CONTRACT.md','transport would overwrite existing source '+name)
            if dest.exists():
                check(git('rev-parse','HEAD:'+str(B/p))==git('rev-parse',INTAKE+':'+str(B/p)), 'intake contract changed before own revision')
            check(isinstance(value,dict) and isinstance(value.get('sha256'),str),'invalid transport source')
            if 'text' in value:
                check(isinstance(value['text'],str),'invalid ordinary text');text=value['text']
            else:
                raise RuntimeError('full ordinary UTF-8 source required')
            value=text.encode('utf-8');check(hashlib.sha256(value).hexdigest()==decoded[name]['sha256'],'materialized source mismatch')
            check(not any(c<32 and c not in (9,10) for c in value),'source control byte')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(value)
    check('SOURCE_MANIFEST.json' in decoded,'transport lacks immutable ordinary manifest')
    m=verifier()
    audit=m.verify();check(audit['ordinary_source_projection_tree_sha']==EXPECTED_PROJECTION,'preflight ordinary projection mismatch');check(audit['review_input_verified'],'missing immutable external report');git('add',str(B))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') for n in changed),'ordinary source commit scope')
    git('commit','-m','source(theta restart R34): feedback-uniform acquired overlap, Bellman resource transfer, raw realizations and complete proofs')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));projection=audit['ordinary_source_projection_tree_sha']
    check(projection==EXPECTED_PROJECTION,'ordinary projection changed')
    check(remote(SOURCE_BRANCH)==bootstrap,'source lease changed; refusing push')
    git('push','origin','HEAD:refs/heads/'+SOURCE_BRANCH);check(remote(SOURCE_BRANCH)==source,'source push readback failed')
    check(not git('diff','--name-only'),'source verification mutated tracked files');preserved=preserve()
    data={'source_commit':source,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'bootstrap_commit':bootstrap,'intake_commit':INTAKE,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_head':OLD,'preserved_objects':preserved,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'transport_blobs':TRANSPORT_BLOBS,'transport_sha256':TRANSPORT_SHA256,'stage':'SOURCE_ONLY; no build result asserted','publication_policy':'ordinary source committed and non-force pushed before build; artifacts create a new branch only; old branches unchanged'}
    out=Path(os.environ['RUNNER_TEMP'])/'r34-source-export';out.mkdir(exist_ok=True)
    count=package(out/'R34_ordinary_source.zip',False,data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r34-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=projection,NATIVE_DIRECTORY_TREE=tree,SOURCE_EXPORT_DIR=str(out));print(json.dumps(data,sort_keys=True,indent=2))

def artifacts():
    source=os.environ['SOURCE_SHA'];projection=os.environ['EXPECTED_TREE'];tree=os.environ['NATIVE_DIRECTORY_TREE']
    check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed')
    audit=verifier().verify();check(audit['ordinary_source_projection_tree_sha']==projection,'source projection mutated')
    check(git('rev-parse',source+':'+str(B))==tree,'source directory tree mismatch')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r34-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],limitations='Full native R34, complete reviewed R32 as H and its fourteen-PDF retained delivery; corrected F remains explicitly distinguished. Builds are not continuum proof, global history re-certification, priority or journal-importance certificates.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit scope')
    git('commit','-m','artifacts(theta restart R34): native and complete corrected/unchanged companions bound to ordinary source')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact must directly follow source')
    check(remote(SOURCE_BRANCH)==source,'source ref changed');check(remote(ARTIFACT_BRANCH) is None,'artifact branch already exists; refusing overwrite')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH);check(remote(ARTIFACT_BRANCH)==artifact,'artifact readback failed');check(remote(SOURCE_BRANCH)==source,'source changed')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r34-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R34_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
