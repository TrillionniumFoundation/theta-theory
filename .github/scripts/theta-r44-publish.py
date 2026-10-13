#!/usr/bin/env python3
"""New-branch-only ordinary-source and artifact publication; old refs are read-only."""
from __future__ import annotations
import argparse,ast,base64,hashlib,importlib.util,json,lzma,os,shutil,subprocess,zipfile
from pathlib import Path
ROOT=Path.cwd();P=Path('papers/General-Theta-Foundations-I-restart');B=P/'r44-stopping-disintegration'
BRANCH='foundation/general-theta-restart-r44-stopping-disintegration-research-2026-10-12'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d';REVIEW='65bd07d89b04274c587d2ae4100511d99c39b0f2'
R43='1909092aeccc74b227fb568eafad6e958efb62d5';REPORT='3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21'
PROJECTION='701db04f35ed3956ab4a51415fe9d03796912573'
TRANSPORT='b2a53a6f5f2fd8344c7e201369e3a20151dc311adb5032e8be97eb79e923d161'
PARTS=['81fe03c60fe76542a96370852cd86c72a229af61','cf42d5a08c46130d4ae02b7e62b3277a458478b1','ff7e2acf104036fd5567529a93a9706f915434dd','ad58943b15045aba80868d2d7734fec1dca94512','3d65d4f0b708e2cf2fd74fc89b91b48f1e557a35','4e2fb61ccba7538e235d884cc2f037a1884c7117','d478ee1070362908bdab31beafbbacb5ac3d974b','f27e71f5c18e9bd5c0a3ee6ecf16b9b887f2b6e0','cfeae39b4dbf19965682ae472e24ba3337f2ea56']
ANCHORS={'foundation/general-theta-foundations-i-restart-2026-10-06':CANON,'review/general-theta-restart-r32-bayesian-curvature-external-top4-referee-r32-2026-10-11':REVIEW,'foundation/general-theta-restart-r43-stopped-occupation-source-2026-10-12':R43,'foundation/general-theta-restart-r38-finite-acquisition-source-2026-10-12':'159f92128d690221395fd550b186af6abdc5f6ba','artifacts/general-theta-restart-r38-finite-acquisition-2026-10-12':'616f35afcafddda1c3166568be8c77c7ea424fb9'}
TMP=Path(os.environ['RUNNER_TEMP'])/'r44-publication';TMP.mkdir(exist_ok=True)
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def git(*args):
    p=subprocess.run(['git',*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'git failed '+repr(args)+'\n'+p.stdout[-20000:]);return p.stdout.strip()
def ghsh(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def remote(branch):
    s=git('ls-remote','origin','refs/heads/'+branch);return s.split()[0] if s else None
def pins():
    result={name:remote(name) for name in ANCHORS};check(result==ANCHORS,'old anchor moved');return result
def env(**values):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in values.items():f.write(f'{k}={v}\n')
def audit():
    spec=importlib.util.spec_from_file_location('r44verify',ROOT/B/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.verify()
def original_objects(ref):
    result={}
    for line in git('ls-tree','-r',ref,'--',str(P),'foundations/general-theta').splitlines():
        meta,name=line.split('\t',1)
        if name.startswith(str(B)+'/'):continue
        result[name]=meta.split()[2]
    return result
def preserved(objects):
    for path,sha in objects.items():check(git('rev-parse','HEAD:'+path)==sha,'inherited object changed '+path)
    return len(objects)
def decode(parts,digest,destination,allow_intake=False):
    raw=b''
    for path,sha in parts:
        piece=path.read_bytes();check(ghsh(piece)==sha,'transport Git mismatch');raw+=piece
    check(hashlib.sha256(raw).hexdigest()==digest,'transport concatenation mismatch')
    records=json.loads(lzma.decompress(raw));check('SOURCE_MANIFEST.json' in records,'manifest absent')
    for name,item in records.items():
        p=Path(name);check(not p.is_absolute() and '..' not in p.parts and not {'artifacts','evidence','review_inputs','.git','transport'}.intersection(p.parts),'unsafe source path')
        content=item['text'].encode();check(hashlib.sha256(content).hexdigest()==item['sha256'],'ordinary hash mismatch')
        dst=destination/p
        if dst.exists() and dst.read_bytes()!=content:check(allow_intake and name=='RESEARCH_INTAKE.md','would replace inherited source '+str(dst))
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(content)
    return len(records)
def package(path,binding,artifacts):
    names=[]
    for name in git('ls-files',str(P),'foundations/general-theta','.github/scripts/theta-r44-publish.py','.github/workflows/theta-r44-stopping-disintegration.yml').splitlines():
        parts=Path(name).parts
        if {'__pycache__','transport'}.intersection(parts):continue
        if {'artifacts','evidence'}.intersection(parts) and not (artifacts and name.startswith(str(B)+'/')):continue
        if (ROOT/name).is_file():names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R44_PUBLICATION_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)
def source():
    check(os.environ.get('GITHUB_REF_NAME')==BRANCH,'wrong branch');bootstrap=git('rev-parse','HEAD');check(remote(BRANCH)==bootstrap,'bootstrap lease moved');pins()
    objects=original_objects(bootstrap)
    old={}
    for node in ast.parse((ROOT/'.github/scripts/theta-r43-publish.py').read_text()).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try:old[node.targets[0].id]=ast.literal_eval(node.value)
            except (ValueError,TypeError):pass
    recovered=decode([(ROOT/B/'transport'/f'r43.part{i:02}',sha) for i,sha in enumerate(old['BLOBS'])],old['TRANSPORT_SHA256'],ROOT/P/'r43-stopped-occupation')
    count=decode([(ROOT/'.github/data'/f'theta-r44.part{i:02}',sha) for i,sha in enumerate(PARTS)],TRANSPORT,ROOT/B,True)
    report=ROOT/P/'r43-stopped-occupation/review_inputs/R32_EXTERNAL_REFEREE_REPORT.md';check(ghsh(report.read_bytes())==REPORT,'review blob mismatch')
    dest=ROOT/B/'review_inputs/R32_EXTERNAL_REFEREE_REPORT.md';dest.parent.mkdir(exist_ok=True);shutil.copyfile(report,dest)
    a=audit();check(a['ordinary_source_projection_tree_sha']==PROJECTION and a['review_input_verified'],'ordinary projection/review mismatch')
    git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    git('add',str(B),str(P/'r43-stopped-occupation'))
    changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(B)+'/') or n.startswith(str(P/'r43-stopped-occupation')+'/') for n in changed),'ordinary source scope')
    git('commit','-m','source(theta restart R44): global stopped realization, preparation and terminal disintegration, controlled matching transfer and raw-kernel proofs; retain deposited R43')
    s=git('rev-parse','HEAD');check(remote(BRANCH)==bootstrap,'source lease moved');git('push','origin','HEAD:refs/heads/'+BRANCH);check(remote(BRANCH)==s,'source readback mismatch');preserved(objects)
    data={'stage':'ORDINARY_SOURCE_PUBLISHED; build not yet certified','source_commit':s,'bootstrap_commit':bootstrap,'canonical_commit':CANON,'review_commit':REVIEW,'inherited_R43_bootstrap':R43,'inherited_R43_source_projection':old['PROJECTION'],'ordinary_source_projection_tree_sha':PROJECTION,'native_directory_tree_sha':git('rev-parse','HEAD:'+str(B)),'source_audit':a,'decoded_R44_files':count,'recovered_R43_files':recovered,'transport_sha256':TRANSPORT,'source_branch':BRANCH,'read_only_anchor_heads':pins(),'preserved_objects':objects,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'policy':'non-force new-branch-only; ordinary source before build; R43 old branch unchanged'}
    (TMP/'binding.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');out=TMP/'source';out.mkdir();package(out/'R44_ordinary_source.zip',data,False);(out/'SOURCE_EXPORT.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    env(SOURCE_SHA=s,EXPECTED_TREE=PROJECTION,SOURCE_EXPORT_DIR=str(out),R44_PUBLICATION_DIR=str(TMP));print(json.dumps({k:v for k,v in data.items() if k!='preserved_objects'},indent=2))
def artifacts():
    data=json.loads((TMP/'binding.json').read_text());s=data['source_commit'];check(git('rev-parse','HEAD')==s and remote(BRANCH)==s and not git('diff','--name-only'),'source changed during build')
    check(audit()['ordinary_source_projection_tree_sha']==PROJECTION,'ordinary source mutated');preserved(data['preserved_objects']);pins()
    receipt=json.loads((TMP/'BUILD_RECEIPT.json').read_text());check(receipt['status']=='PASS' and receipt['source_commit']==s and receipt['ordinary_source_projection_tree_sha']==PROJECTION,'build source binding')
    out=ROOT/B/'artifacts';ev=ROOT/B/'evidence';out.mkdir(exist_ok=True);ev.mkdir(exist_ok=True)
    pdfs=list((TMP/'build').glob('*.pdf'));check(len(pdfs)==19,'delivery PDF count')
    for p in pdfs:shutil.copyfile(p,out/p.name)
    shutil.copyfile(TMP/'build/R44_LATEX_BUILD.log',ev/'R44_LATEX_BUILD.log');shutil.copyfile(TMP/'BUILD_RECEIPT.json',ev/'BUILD_RECEIPT.json')
    data.update(stage='BUILT',delivery_pdfs=receipt['delivery_pdfs'],total_delivery_pages=receipt['total_delivery_pages'],total_isolated_pdf_builds=receipt['total_isolated_pdf_builds'],read_only_anchor_heads=pins(),limitations=receipt['limitations'])
    (ev/'SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(out),str(ev));changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(out)+'/') or n.startswith(str(ev)+'/') for n in changed),'artifact scope')
    git('commit','-m','artifacts(theta restart R44): nineteen full mathematical PDFs and immutable-source build receipt')
    a=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==s and remote(BRANCH)==s,'artifact ancestry/lease');git('push','origin','HEAD:refs/heads/'+BRANCH);check(remote(BRANCH)==a,'artifact readback');pins()
    data.update(stage='ARTIFACTS_PUBLISHED',artifact_commit=a)
    delivery=TMP/'delivery';delivery.mkdir();files=package(delivery/'General_Theta_Foundations_I_R44_source_and_build_packet.zip',data,True)
    summary={'source_commit':s,'artifact_commit':a,'ordinary_source_projection_tree_sha':PROJECTION,'native_directory_tree_sha':data['native_directory_tree_sha'],'packaged_files':files,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'packet_sha256':hashlib.sha256((delivery/'General_Theta_Foundations_I_R44_source_and_build_packet.zip').read_bytes()).hexdigest(),'total_delivery_pages':receipt['total_delivery_pages']}
    (delivery/'ARTIFACT_PUBLICATION.json').write_text(json.dumps(summary,indent=2)+'\n');env(ARTIFACT_SHA=a,DELIVERY_DIR=str(delivery));print(json.dumps(summary,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(source if args.stage=='source' else artifacts)()
