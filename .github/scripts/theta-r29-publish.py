#!/usr/bin/env python3
"""Materialize ordinary R29 text sources, then publish an artifact-only child.
The compressed Git blobs and pinned line deltas are transport only; they are not manuscript source. The mathematical source is committed
and pushed as ordinary files before any build; builds never modify that commit.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,io,json,lzma,os,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path.cwd(); P=Path('papers/General-Theta-Foundations-I-restart'); B=P/'r29-causal-energy'
SOURCE_BRANCH='foundation/general-theta-restart-r29-causal-energy-source-2026-10-10'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r29-causal-energy-2026-10-10'
TRANSPORT_BLOBS=['300b4654d221b7fb951f8707478d19a10c679d2e', 'b25d5de5ff2b1a5d76be75caddaeacff13ad22d1', '86f04572ffcd1bebd81aedb8e778502d7c240d23', '1f990762f7e1ad465b49cf3eb756ecbd4dedea9c', '7dc0f4ace2e6082569c4733653960f989d940de5', 'dee2b1f54a97498da1180bd1f381de1a35352938', '8bbfad90d319ab31cecd4b830cbc25cb17ada1a4', '31d1f10fa8ee300c2bc2072487e0d618391c7d3e', '7174cdfcf35137d2aa693e49bbb0d6f3741ca4ca']
TRANSPORT_SHA256='7fcb5065f01b434dc2ba51ef520f5d7847ed5ea4f1f8cbb1df68733162477438'
EXPECTED_PROJECTION='8e7a5a5ba3cb01124005a3c7a032197759a88e66'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='00cad841267ee714f20d71ca9734dc5d4014ee4f'
OLD='37826ed38311e247874c35674e668855402ed6ff'
MATHEMATICS='c5f05d1944251a95619d5cdad814c5c83646429c'
INTAKE='c929b4b525b90afbf79e598d0f03a202aea6b243'
REPORT_BLOB='79c032f1bd1697722d44206dfb28f48b1cdf2311'
ANCHORS={
 'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,
 'review/general-theta-restart-r27-occupation-modulus-external-top4-referee-r27-2026-10-10':REVIEW,
 'referee-ready/general-theta-restart-r27-occupation-modulus-2026-10-10':MATHEMATICS,
 'foundation/general-theta-restart-r28-accessible-occupation-research-2026-10-10':OLD,
 'foundation/general-theta-restart-r29-causal-energy-research-2026-10-10':INTAKE,
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
    spec=importlib.util.spec_from_file_location('r29verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

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
    path=str(B/'review_inputs/R27_EXTERNAL_REFEREE_REPORT.md')
    check(git('rev-parse','HEAD:'+path)==REPORT_BLOB,'review input changed');result[path]=REPORT_BLOB
    path=str(P/'THEOREM_TARGETS.md');sha=git('rev-parse',CANON+':'+path)
    check(git('rev-parse','HEAD:'+path)==sha,'changed theorem targets');result[path]=sha
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result

def package(path,include_artifacts,binding):
    reports=[x for x in git('ls-files').splitlines() if x.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and x.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r29-publish.py','.github/workflows/theta-r29-causal-energy.yml']+reports
    names=[]
    for name in git('ls-files',*scope).splitlines():
        parts=Path(name).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(include_artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R29_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
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
                bp=Path(value.get('base_path',''));check(not bp.is_absolute() and '..' not in bp.parts and bp.parts and bp.parts[0]=='r27-occupation-modulus','unsafe delta base')
                base_path=str(P/bp)
                original=subprocess.check_output(['git','show',MATHEMATICS+':'+base_path],cwd=ROOT)
                check(hashlib.sha256(original).hexdigest()==value.get('base_sha256'),'pinned delta base mismatch')
                rows=original.decode('utf-8').splitlines(keepends=True);edits=value.get('edits');check(isinstance(edits,list),'invalid edit list')
                frontier=0
                for edit in edits:
                    check(isinstance(edit,list) and len(edit)==3,'invalid edit')
                    i,j,s=edit;check(isinstance(i,int) and isinstance(j,int) and frontier<=i<=j<=len(rows) and isinstance(s,str),'invalid edit bounds');frontier=j
                for i,j,s in reversed(edits):rows[i:j]=[s]
                text=''.join(rows)
            value=text.encode('utf-8');check(hashlib.sha256(value).hexdigest()==decoded[name]['sha256'],'materialized source mismatch')
            check(not any(c<32 and c not in (9,10) for c in value),'source control byte')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(value)
    m=verifier();files=m.sources()
    manifest={'format':1,'description':'Ordinary mathematical text projection; pinned external review and subsequent evidence/artifacts are separately bound.','files':{name:{'sha256':m.sha256((ROOT/B/name).read_bytes()),'git_blob_sha':m.git_hash('blob',(ROOT/B/name).read_bytes())} for name in files}}
    (ROOT/B/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    audit=m.verify();check(audit['ordinary_source_projection_tree_sha']==EXPECTED_PROJECTION,'preflight ordinary projection mismatch');check(audit['review_input_verified'],'missing immutable external report');git('add',str(B))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') for n in changed),'ordinary source commit scope')
    git('commit','-m','source(theta restart R29): causal energy, exact clock allocation, homogeneous geometry and complete proofs')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));projection=audit['ordinary_source_projection_tree_sha']
    check(projection==EXPECTED_PROJECTION,'ordinary projection changed')
    check(remote(SOURCE_BRANCH)==bootstrap,'source lease changed; refusing push')
    git('push','origin','HEAD:refs/heads/'+SOURCE_BRANCH);check(remote(SOURCE_BRANCH)==source,'source push readback failed')
    check(not git('diff','--name-only'),'source verification mutated tracked files');preserved=preserve()
    data={'source_commit':source,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'bootstrap_commit':bootstrap,'intake_commit':INTAKE,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_head':OLD,'preserved_objects':preserved,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'transport_blobs':TRANSPORT_BLOBS,'transport_sha256':TRANSPORT_SHA256,'stage':'SOURCE_ONLY; no build result asserted','publication_policy':'ordinary source committed and non-force pushed before build; artifacts create a new branch only; old branches unchanged'}
    out=Path(os.environ['RUNNER_TEMP'])/'r29-source-export';out.mkdir(exist_ok=True)
    count=package(out/'R29_ordinary_source.zip',False,data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r29-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=projection,NATIVE_DIRECTORY_TREE=tree,SOURCE_EXPORT_DIR=str(out));print(json.dumps(data,sort_keys=True,indent=2))

def artifacts():
    source=os.environ['SOURCE_SHA'];projection=os.environ['EXPECTED_TREE'];tree=os.environ['NATIVE_DIRECTORY_TREE']
    check(git('rev-parse','HEAD')==source,'build altered HEAD');check(not git('diff','--name-only'),'tracked source changed')
    audit=verifier().verify();check(audit['ordinary_source_projection_tree_sha']==projection,'source projection mutated')
    check(git('rev-parse',source+':'+str(B))==tree,'source directory tree mismatch')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text())
    check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r29-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=audit,delivery_pdfs=receipt['delivery_pdfs'],limitations='Full native, new corrected companion F and complete retained companions only; finite checks and reproducibility are not continuum proof or priority certificates.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit scope')
    git('commit','-m','artifacts(theta restart R29): native and complete corrected/unchanged companions bound to ordinary source')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact must directly follow source')
    check(remote(SOURCE_BRANCH)==source,'source ref changed');check(remote(ARTIFACT_BRANCH) is None,'artifact branch already exists; refusing overwrite')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH);check(remote(ARTIFACT_BRANCH)==artifact,'artifact readback failed');check(remote(SOURCE_BRANCH)==source,'source changed')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r29-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R29_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':projection,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
