#!/usr/bin/env python3
"""Publish immutable ordinary R43 source before building, then an artifact-only child.
Compressed blobs are transport, never the manuscript source. All old refs are read-only.
"""
from __future__ import annotations
import argparse,base64,hashlib,importlib.util,json,lzma,os,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path.cwd();P=Path('papers/General-Theta-Foundations-I-restart');B=P/'r43-stopped-occupation'
SOURCE_BRANCH='foundation/general-theta-restart-r43-stopped-occupation-source-2026-10-12'
ARTIFACT_BRANCH='artifacts/general-theta-restart-r43-stopped-occupation-2026-10-12'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='65bd07d89b04274c587d2ae4100511d99c39b0f2'
OLD='c35942510a26598f1cdd50e2699487753a6a02fb'
INTAKE='8b65f645320530713c134ce677d31dba2e2c26a1'
R38_SOURCE='159f92128d690221395fd550b186af6abdc5f6ba'
R38_ARTIFACT='616f35afcafddda1c3166568be8c77c7ea424fb9'
REPORT='3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21'
PROJECTION='bdbbac591826cff47200a6e0601dcdd48e5400c9'
TRANSPORT_SHA256='f85c3b2593bf540249f17be442b815a2ea0c190c77d56fb495181b40524e8e30'
BLOBS=['bbb89e50f719371c86d0666e7916b2dba4baad90', '88abedc475541d232f39c231ad1f7630d4b63d41', '1face800a818caf592dc4e3e233acc4f277f56eb', '7b444a85771576cdf539fef13f9a659b4dcde2fb', '35a1ce38c3412e503208c94b576cbc2ef2bdbf33', '9ed0e82c3681da92f92e08d588e8080041306970', '7f3e74b38a7197e1371e74ddbf4c86bb0f6f4da9', '0ea7de00b15f596410b7e392007e3ba3bea76005', '0157428db058c5492b3f09e462cf19ee9b710ffe']
ANCHORS={'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,'review/general-theta-restart-r32-bayesian-curvature-external-top4-referee-r32-2026-10-11':REVIEW,'foundation/general-theta-restart-r42-stopped-transfer-research-2026-10-12':OLD,'artifacts/general-theta-restart-r38-finite-acquisition-2026-10-12':R38_ARTIFACT,'foundation/general-theta-restart-r38-finite-acquisition-source-2026-10-12':R38_SOURCE}
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def cmd(*args):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'failed '+repr(args)+'\n'+p.stdout[-20000:]);return p.stdout.strip()
def git(*args):return cmd('git',*args)
def remote(branch):
    v=git('ls-remote','origin','refs/heads/'+branch);return v.split()[0] if v else None
def audit():
    spec=importlib.util.spec_from_file_location('r43verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.verify()
def environment(**values):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in values.items():f.write(f'{k}={v}\n')
def preserve():
    result={}
    for line in git('ls-tree',OLD+':'+str(P)).splitlines():
        meta,name=line.split('\t',1);path=str(P/name);sha=meta.split()[2]
        check(git('rev-parse','HEAD:'+path)==sha,'inherited source altered '+path);result[path]=sha
    for name in ('General_Theta_Foundations_v0.1.md','RESTART_CHARTER.md','REALIZATION_REGISTRY.md'):
        path='foundations/general-theta/'+name;sha=git('rev-parse',CANON+':'+path)
        check(git('rev-parse','HEAD:'+path)==sha,'control altered '+path);result[path]=sha
    path=str(P/'THEOREM_TARGETS.md');sha=git('rev-parse',CANON+':'+path)
    check(git('rev-parse','HEAD:'+path)==sha,'targets altered');result[path]=sha
    path=str(B/'review_inputs/R32_EXTERNAL_REFEREE_REPORT.md')
    check(git('rev-parse','HEAD:'+path)==REPORT,'report identity differs');result[path]=REPORT
    for branch,sha in ANCHORS.items():check(remote(branch)==sha,'read-only anchor moved: '+branch)
    return result

def package(path,artifacts,binding):
    reports=[n for n in git('ls-files').splitlines() if n.startswith('GENERAL_THETA_FOUNDATIONS_I_RESTART_') and n.endswith('.md')]
    scope=[str(P),'foundations/general-theta','.github/scripts/theta-r43-publish.py','.github/workflows/theta-r43-stopped-occupation.yml']+reports
    names=[]
    for n in git('ls-files',*scope).splitlines():
        parts=Path(n).parts
        if '__pycache__' in parts:continue
        if ('artifacts' in parts or 'evidence' in parts) and not(artifacts and n.startswith(str(B)+'/')):continue
        if (ROOT/n).is_file():names.append(n)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n in names:z.write(ROOT/n,n)
        z.writestr('R43_SOURCE_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)

def prepare():
    check(os.environ.get('GITHUB_REF_NAME')==SOURCE_BRANCH,'wrong source branch')
    bootstrap=git('rev-parse','HEAD');check(remote(SOURCE_BRANCH)==bootstrap,'source lease moved')
    git('fetch','--no-tags','origin',CANON,REVIEW,OLD,INTAKE,R38_SOURCE,R38_ARTIFACT)
    check(git('rev-parse','HEAD^')==INTAKE,'bootstrap parent differs from canonical intake')
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    preserved=preserve();pieces=[]
    for blob in BLOBS:
        req=urllib.request.Request('https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/blobs/'+blob,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
        with urllib.request.urlopen(req,timeout=60) as response:data=json.load(response)
        piece=base64.b64decode(data['content']);check(hashlib.sha1(b'blob '+str(len(piece)).encode()+b'\0'+piece).hexdigest()==blob,'transport Git identity mismatch');pieces.append(piece)
    archive=b''.join(pieces);check(hashlib.sha256(archive).hexdigest()==TRANSPORT_SHA256,'transport archive mismatch')
    decoded=json.loads(lzma.decompress(archive).decode());check(isinstance(decoded,dict) and 'SOURCE_MANIFEST.json' in decoded,'ordinary manifest missing')
    for name,value in decoded.items():
        p=Path(name);check(not p.is_absolute() and '..' not in p.parts and p.parts and not any(v in p.parts for v in ('artifacts','evidence','__pycache__','.git','review_inputs')),'unsafe source entry')
        dest=ROOT/B/p
        check(isinstance(value,dict) and isinstance(value.get('text'),str),'ordinary text required')
        content=value['text'].encode();check(hashlib.sha256(content).hexdigest()==value['sha256'],'source content hash mismatch')
        check(not any(c<32 and c not in (9,10) for c in content),'source control byte')
        if dest.exists():
            check(name=='RESEARCH_INTAKE.md' and dest.read_bytes()==content,'would overwrite existing source '+name)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
    a=audit();check(a['ordinary_source_projection_tree_sha']==PROJECTION and a['review_input_verified'],'ordinary projection/report mismatch')
    git('add',str(B));changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') for n in changed),'ordinary source commit scope')
    git('commit','-m','source(theta restart R43): preparation-injected stopped occupation, matching first-run controlled resource laws, two raw kernels and singular strata')
    source=git('rev-parse','HEAD');tree=git('rev-parse','HEAD:'+str(B));check(remote(SOURCE_BRANCH)==bootstrap,'source lease changed')
    git('push','origin','HEAD:refs/heads/'+SOURCE_BRANCH);check(remote(SOURCE_BRANCH)==source,'source readback differs')
    check(not git('diff','--name-only'),'ordinary source changed');preserved=preserve()
    data={'stage':'SOURCE_ONLY; no build success asserted','source_commit':source,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':PROJECTION,'bootstrap_commit':bootstrap,'intake_commit':INTAKE,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_head':OLD,'inherited_completed_source':R38_SOURCE,'inherited_completed_artifacts':R38_ARTIFACT,'preserved_objects':preserved,'read_only_anchor_heads':ANCHORS,'source_branch':SOURCE_BRANCH,'artifact_branch':ARTIFACT_BRANCH,'transport_blobs':BLOBS,'transport_sha256':TRANSPORT_SHA256,'publication_policy':'ordinary source committed and non-force pushed before build; artifacts create-only new ref; old branches unchanged'}
    out=Path(os.environ['RUNNER_TEMP'])/'r43-source-export';out.mkdir(exist_ok=True)
    count=package(out/'R43_ordinary_source.zip',False,data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(dict(data,packaged_files=count),sort_keys=True,indent=2)+'\n')
    (Path(os.environ['RUNNER_TEMP'])/'r43-binding.json').write_text(json.dumps(data))
    environment(SOURCE_SHA=source,EXPECTED_TREE=PROJECTION,NATIVE_DIRECTORY_TREE=tree,SOURCE_EXPORT_DIR=str(out));print(json.dumps(data,sort_keys=True,indent=2))

def artifacts():
    source=os.environ['SOURCE_SHA'];tree=os.environ['NATIVE_DIRECTORY_TREE']
    check(git('rev-parse','HEAD')==source and not git('diff','--name-only'),'build changed source commit or files')
    a=audit();check(a['ordinary_source_projection_tree_sha']==PROJECTION,'ordinary projection changed')
    check(git('rev-parse',source+':'+str(B))==tree,'source directory binding changed')
    receipt=json.loads((ROOT/B/'evidence/BUILD_RECEIPT.json').read_text());check(receipt['status']=='PASS' and receipt['source_commit']==source,'build source binding failed')
    data=json.loads((Path(os.environ['RUNNER_TEMP'])/'r43-binding.json').read_text())
    data.update(stage='BUILT',hosted_run_id=os.environ['GITHUB_RUN_ID'],hosted_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),preserved_objects=preserve(),source_audit=a,delivery_pdfs=receipt['delivery_pdfs'],limitations='Native R43, complete R38 as K, R37 as J, R34 as I, R32 as H and all retained companions; original R27 and corrected F distinguished. Build/finite checks are not continuum proofs, whole-history re-certification, priority or journal acceptance.')
    (ROOT/B/'evidence/SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(B/'artifacts'),str(B/'evidence'));changed=git('diff','--cached','--name-only').splitlines()
    check(changed and all(n.startswith(str(B/'artifacts')+'/') or n.startswith(str(B/'evidence')+'/') for n in changed),'artifact commit scope')
    git('commit','-m','artifacts(theta restart R43): full stopped-occupation manuscript and unchanged complete companions bound to source')
    artifact=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==source,'artifact must directly follow source')
    check(remote(SOURCE_BRANCH)==source and remote(ARTIFACT_BRANCH) is None,'source changed or artifact ref exists')
    git('push','origin','HEAD:refs/heads/'+ARTIFACT_BRANCH)
    check(remote(ARTIFACT_BRANCH)==artifact and remote(SOURCE_BRANCH)==source,'artifact/source readback differs')
    data.update(artifact_commit=artifact,stage='ARTIFACTS_PUBLISHED',non_force_create_only=True)
    out=Path(os.environ['RUNNER_TEMP'])/'r43-delivery';out.mkdir(exist_ok=True)
    count=package(out/'General_Theta_Foundations_I_R43_source_and_build_packet.zip',True,data)
    summary={'source_commit':source,'artifact_commit':artifact,'native_directory_tree_sha':tree,'ordinary_source_projection_tree_sha':PROJECTION,'packaged_files':count,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.zip')}}
    (out/'DELIVERY_SHA256.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');environment(ARTIFACT_SHA=artifact,DELIVERY_DIR=str(out));print(json.dumps(summary,sort_keys=True,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(prepare if args.stage=='source' else artifacts)()
