#!/usr/bin/env python3
"""Materialize ordinary R32 text sources, then publish an artifact-only child.
The compressed Git blobs are transport only; they are not manuscript source. The mathematical source is committed
and pushed as ordinary files before any build; builds never modify that commit.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,io,json,lzma,os,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path.cwd(); P=Path('papers/General-Theta-Foundations-I-restart'); B=P/'r32-bayesian-curvature'
SOURCE_BRANCH='foundation/general-theta-restart-r32-bayesian-curvature-source-2026-10-11'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r32-bayesian-curvature-2026-10-11'
TRANSPORT_BLOBS=['f6b313990b44e761ff3a18c3ef90a0ea72e7549b', 'fb25232681a8a90b0a45928fcd729226808a3419', '2f601c3c38a18a65adf1adc5badb0d22bc3877c8', '4765019f631ee0efe5a69fd4fa975a542855021a', 'be22ab4796aefb42784c8a4e93a3af41fbb93eeb', 'af5eb314b61938c24f77d7ae240ecc2c6c4b72cd', '18c3da12f7390780ad925357d7bf0e8e6a8a1e7c', 'd3f35a50cb5d74973f86239d2b55924a2142dff1', 'b8cab959b6eb1bae00740c9afc41b00eafb80f5c']
TRANSPORT_SHA256='eca92dd7d16077b4595d250afb7f22b7042895e8a394d40989d0f4ff36f1e219'
EXPECTED_PROJECTION='97c35f107294a7a07308ce06813507895f4a529c'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='204a9cc62c2c1ce48d0668f35c4bbc326118ebd7'
OLD='155677ec098ea24c45d93cd4848fbeb03577e94e'
MATHEMATICS='09eda58be2297ce885c7f2b4447f24fec3a0c9b4'
INTAKE='e799647343c5d2b6c892c3c2dde887439fd98a91'
REPORT_BLOB='dd9a1681b0e807e892c4c053640ec8e332ca94e1'
ANCHORS={
 'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,
 'review/general-theta-restart-r29-causal-energy-external-top4-referee-r29-2026-10-10':REVIEW,
 'referee-ready/general-theta-restart-r29-causal-energy-2026-10-10':MATHEMATICS,
 'foundation/general-theta-restart-r31-bayesian-information-research-2026-10-11':OLD,
 'foundation/general-theta-restart-r32-bayesian-curvature-research-2026-10-11':INTAKE,
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
    spec=importlib.util.spec_from_file_location('r32verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

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
    path=str(B/'review_inputs/R29_EXTERNAL_REFEREE_REPORT.md')
    check(git('rev-parse','HEAD:'+path)==REPORT_BLOB,'review input changed');result[path]=REPORT_BLOB
    path=str(P/'THEOREM_TARGETS.md');sha=git('rev-parse',CANON+':'+path)
    check(git('rev-parse','HEAD:'+path)==sha,'changed theorem targets');result[path]=sha
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result

def package(path,include_artifacts,binding):
    reports=[x for x in git('ls-files').splitlines() if x.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and x.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r32-publish.py','.github/workflows/theta-r32-bayesian-curvature.yml']+reports
    names=[]
    for name in git('ls-files',*scope).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R32_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
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
            check(name not in ('SOURCE_MANIFEST.json','RESEARCH_CONTRACT.md'),'transport must preserve intake and derive manifest')
            dest=ROOT/B/p;check(not dest.exists(),'transport would overwrite existing source '+name)
            check(isinstance(value,dict) and isinstance(value.get('sha256'),str),'invalid transport source')
            if 'text' in value:
                check(isinstance(value['text'],str),'invalid ordinary text');text=value['text']
            else:
                raise RuntimeError('full ordinary UTF-8 source required')
            value=text.encode('utf-8');check(hashlib.sha256(value).hexdigest()==decoded[name]['sha256'],'materialized source mismatch')
            check(not any(c<32 and c not in (9,10) for c in value),'source control byte')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(value)
    m=verifier();files=m.sources()
    manifest={'version':1,'scope':'All ordinary R32 text; excludes pinned review input and generated artifacts/evidence','files':{name:{'sha256':m.sha256((ROOT/B/name).read_bytes()),'git_blob_sha':m.git_hash('blob',(ROOT/B/name).read_bytes())} for name in files}}
    (ROOT/B/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    audit=m.verify();check(audit['ordinary_source_projection_tree_sha']==EXPECTED_PROJECTION,'preflight ordinary projection mismatch');check(audit['review_input_verified'],'missing immutable external report');git('add',str(B))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') for n in changed),'ordinary source commit scope')
    git('commit','-m','source(theta restart R32): normalized Bayesian defect, actual-mass transfer, raw realizations and complete proofs')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));projection=audit['ordinary_source_projection_tree_sha']
    check(projection==EXPECTED_PROJECTION,'ordinary projection changed')
    check(remote(SOURCE_BRANCH)==bootstrap,'source lease changed; refusing push')
    git('push','origin','HEAD:refs/heads/'+SOURCE_BRANCH);check(remote(SOURCE_BRANCH)==source,'source push readback failed')
    check(not git('diff','--name-only'),'source verification mutated tracked files');preserved=preserve()
    data={'source_commit':source,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'bootstrap_commit':bootstrap,'intake_commit':INTAKE,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_head':OLD,'preserved_objects':preserved,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'transport_blobs':TRANSPORT_BLOBS,'transport_sha256':TRANSPORT_SHA256,'stage':'SOURCE_ONLY; no build result asserted','publication_policy':'ordinary source committed and non-force pushed before build; artifacts create a new branch only; old branches unchanged'}
    out=Path(os.environ['RUNNER_TEMP'])/'r32-source-export';out.mkdir(exist_ok=True)
    count=package(out/'R32_ordinary_source.zip',False,data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r32-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=projection,NATIVE_DIRECTORY_TREE=tree,SOURCE_EXPORT_DIR=str(out));print(json.dumps(data,sort_keys=True,indent=2))

def artifacts():
    source=os.environ['SOURCE_SHA'];projection=os.environ['EXPECTED_TREE'];tree=os.environ['NATIVE_DIRECTORY_TREE']
    check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed')
    audit=verifier().verify();check(audit['ordinary_source_projection_tree_sha']==projection,'source projection mutated')
    check(git('rev-parse',source+':'+str(B))==tree,'source directory tree mismatch')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r32-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],limitations='Full native, complete R29 as G, corrected F with explicit title notice, and all retained companions only; finite checks and reproducibility are not continuum proof or priority certificates.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit scope')
    git('commit','-m','artifacts(theta restart R32): native and complete corrected/unchanged companions bound to ordinary source')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact must directly follow source')
    check(remote(SOURCE_BRANCH)==source,'source ref changed');check(remote(ARTIFACT_BRANCH) is None,'artifact branch already exists; refusing overwrite')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH);check(remote(ARTIFACT_BRANCH)==artifact,'artifact readback failed');check(remote(SOURCE_BRANCH)==source,'source changed')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r32-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R32_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
