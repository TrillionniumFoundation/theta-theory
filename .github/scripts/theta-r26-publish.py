#!/usr/bin/env python3
"""Materialize ordinary R26 text sources, then publish an artifact-only child.
The compressed Git blobs are transport only. The mathematical source is committed
and pushed as ordinary files before any build; builds never modify that commit.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,io,json,lzma,os,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path.cwd(); P=Path('papers/General-Theta-Foundations-I-restart'); B=P/'r26-task-visible'
SOURCE_BRANCH='foundation/general-theta-restart-r26-task-visible-source-2026-10-10'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r26-task-visible-2026-10-10'
TRANSPORT_BLOBS=['f3da3d61c42e2ae3eef3ed64bc959c3285fc8bb4','498e33f0e1f4fc010658ff8a9b696a4a6811c9a7','9a1b9b0a9f8f4dc4998c011081d41f07ff8bb5f9','30418c74e5de748e202f9ac92a1ab41d906bb861','3019816fbdc37cab600952e8bf9ed44a71e64c46','9fe733b22480f2b51285fd599524b74352f471ef','55afd00701d95f6dabe0359c67b55e94ed7149a7']
TRANSPORT_SHA256='0da8a479f3c88de7c615bf52695d00a8b535faeeb9017c8d76e55ac197c52919'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d';REVIEW='623837ecd254175c0e0cc055d3f0ccf758f57516'
OLD='69b01457fed7b4757eb38e9825990b1a44f4ff1c';INTAKE='641c2968385a227fa48c9d615287aa57ecd6aead'
REPORT_BLOB='7b5b8fa3af91c2545563c41e8bce8fb5b95b7657'
ANCHORS={'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,'review/general-theta-restart-r25-retained-state-external-top4-referee-r25-2026-10-10':REVIEW,'referee-ready/general-theta-restart-r25-retained-state-2026-10-10':OLD,'foundation/general-theta-restart-r26-task-visible-research-2026-10-10':INTAKE}
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def cmd(*args):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'failed '+repr(args)+'\n'+p.stdout[-16000:]);return p.stdout.strip()
def git(*args):return cmd('git',*args)
def remote(branch):
    v=git('ls-remote','origin','refs/heads/'+branch);return v.split()[0] if v else None
def verifier():
    spec=importlib.util.spec_from_file_location('r26verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
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
    path=str(B/'review_inputs/R25_EXTERNAL_REFEREE_REPORT.md')
    check(git('rev-parse','HEAD:'+path)==REPORT_BLOB,'review input changed');result[path]=REPORT_BLOB
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result

def package(path,include_artifacts,binding):
    reports=[x for x in git('ls-files').splitlines() if x.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and x.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r26-publish.py','.github/workflows/theta-r26-task-visible.yml']+reports
    names=[]
    for name in git('ls-files',*scope).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R26_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)

def prepare():
    check(os.environ.get('GITHUB_REF_NAME')==SOURCE_BRANCH,'wrong source branch')
    bootstrap=git('rev-parse','HEAD');check(remote(SOURCE_BRANCH)==bootstrap,'source branch moved')
    git('fetch','--no-tags','origin',CANON,REVIEW,OLD,INTAKE)
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
            check(name not in ('SOURCE_MANIFEST.json','RESEARCH_CONTRACT.md'),'transport must preserve intake and derive manifest')
            dest=ROOT/B/p;check(not dest.exists(),'transport would overwrite existing source '+name)
            check(isinstance(value,str),'invalid text source');value=value.encode('utf-8');check(not any(c<32 and c not in (9,10) for c in value),'source control byte')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(value)
    m=verifier();files=m.sources();manifest={'schema':'theta-source-manifest-1','scope':'ordinary native sources; excludes build artifacts and evidence','files':{name:{'sha256':m.sha256((ROOT/B/name).read_bytes()),'git_blob_sha':m.git_hash('blob',(ROOT/B/name).read_bytes()),'bytes':(ROOT/B/name).stat().st_size} for name in files}}
    (ROOT/B/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    audit=m.verify();git('add',str(B))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') for n in changed),'ordinary source commit scope')
    git('commit','-m','source(theta restart R26): task-visible causal transfer, sharp retained-memory laws and complete proofs')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));check(tree==audit['native_source_tree_sha'],'ordinary native tree mismatch')
    check(remote(SOURCE_BRANCH)==bootstrap,'source lease changed; refusing push')
    git('push','origin','HEAD:refs/heads/'+SOURCE_BRANCH);check(remote(SOURCE_BRANCH)==source,'source push readback failed')
    check(not git('diff','--name-only'),'source verification mutated tracked files');preserved=preserve()
    data={'source_commit':source,'native_source_tree_sha':tree,'bootstrap_commit':bootstrap,'intake_commit':INTAKE,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_head':OLD,'preserved_objects':preserved,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'transport_blobs':TRANSPORT_BLOBS,'transport_sha256':TRANSPORT_SHA256,'stage':'SOURCE_ONLY; no build result asserted','publication_policy':'ordinary source committed and non-force pushed before build; artifacts create a new branch only; old branches unchanged'}
    out=Path(os.environ['RUNNER_TEMP'])/'r26-source-export';out.mkdir(exist_ok=True)
    count=package(out/'R26_ordinary_source.zip',False,data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r26-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=tree,SOURCE_EXPORT_DIR=str(out));print(json.dumps(data,sort_keys=True,indent=2))

def artifacts():
    source=os.environ['SOURCE_SHA'];tree=os.environ['EXPECTED_TREE']
    check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed')
    audit=verifier().verify();check(audit['native_source_tree_sha']==tree,'source projection mutated')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r26-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],limitations='Full native and complete retained companions only; finite checks and reproducibility are not continuum proof or priority certificates.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit scope')
    git('commit','-m','artifacts(theta restart R26): complete native and unchanged companion builds bound to ordinary source')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact must directly follow source')
    check(remote(SOURCE_BRANCH)==source,'source ref changed');check(remote(ARTIFACT_BRANCH) is None,'artifact branch already exists; refusing overwrite')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH);check(remote(ARTIFACT_BRANCH)==artifact,'artifact readback failed');check(remote(SOURCE_BRANCH)==source,'source changed')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r26-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R26_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_source_tree_sha':tree,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
