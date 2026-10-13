#!/usr/bin/env python3
"""Publish ordinary source first, then a read-only build's artifact-only child.
Only the new R45 research ref is writable. Old branches and existing blobs are immutable.
"""
from __future__ import annotations
import argparse,ast,hashlib,importlib.util,json,lzma,os,shutil,subprocess,zipfile
from pathlib import Path
ROOT=Path.cwd(); P=Path('papers/General-Theta-Foundations-I-restart'); B=P/'r45-adapted-stopping'
BRANCH='foundation/general-theta-restart-r45-adapted-stopping-research-2026-10-12'
PROJECTION='3a48f0deb1a3a185892ee264afe23a9e8e42b030'
TRANSPORT='9192f58a87dd8f691d8b82743025942d5f1de8479ac1142ca93e6b9b485c65df'
PARTS=['ac3a5a97906b4ff68bde841aea793f268eed2a1a','3742c07af0169ca7959d654dd8a1c128eea06ff4','a50d3e1adadc1d7184d96df38087f2e58fb1ea09','001a44990611b5880ac4103861c36d44c59b3072','f0993ca8e9aee0caf7549f1bf3d35c7ba661138b','9793d9e35f6700707f8d97adf404d7f936d85945','54c59a684fe4b7d2dfbf63143438a5dd6b8eb66d','d6f750ff3ab33e1c0f4067707e31dda84626895f','03da6482f9b0be2f700da4c7c7d2003a2329783d','db32d2aa1ed5866128a790ebc244877679ad1b40']
REPORT='3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21'
REPORT_NAME='GENERAL_THETA_FOUNDATIONS_I_RESTART_R32_BAYESIAN_CURVATURE_EXTERNAL_REFEREE_REPORT_R32.md'
FIXED={'foundation/general-theta-foundations-i-restart-2026-10-06':'18000b21e4bfd89180ccb069e46ac0f21621f34d','review/general-theta-restart-r32-bayesian-curvature-external-top4-referee-r32-2026-10-11':'65bd07d89b04274c587d2ae4100511d99c39b0f2','foundation/general-theta-restart-r43-stopped-occupation-source-2026-10-12':'1909092aeccc74b227fb568eafad6e958efb62d5','foundation/general-theta-restart-r44-stopping-disintegration-research-2026-10-12':'fd97bedc63e130a39006bd46d35f3f309edb0093'}
HISTORICAL=['realization/causal-predictive-memory-v1-2026-10-06','realization/causal-resource-memory-v1-2026-09-28','realization/finite-input-actions-v1-2026-09-27','realization/streaming-memory-space-v1-2026-09-28','realization/finite-physical-actions-v1-2026-09-28','realization/ordered-measurement-geometry-v1-2026-10-05','realization/ordered-measurement-discrimination-v1-2026-10-06','archive/general-theta-development-v2-v96-frozen-2026-10-06']
TMP=Path(os.environ['RUNNER_TEMP'])/'r45-publication'; TMP.mkdir(exist_ok=True)
def check(ok,msg):
    if not ok: raise RuntimeError(msg)
def git(*args):
    p=subprocess.run(['git',*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    check(p.returncode==0,'git '+repr(args)+' failed\n'+p.stdout[-20000:]); return p.stdout.strip()
def ghash(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def remote(branch):
    v=git('ls-remote','origin','refs/heads/'+branch); return v.split()[0] if v else None
def pins(expected=None):
    heads={line.split()[1].removeprefix('refs/heads/'):line.split()[0] for line in git('ls-remote','--heads','origin').splitlines()}
    got={b:heads.get(b) for b in list(FIXED)+HISTORICAL}
    check(all(got[b]==s for b,s in FIXED.items()),'fixed read-only anchor moved')
    check(all(got[b] for b in HISTORICAL),'historical branch not found')
    if expected is not None:check(got==expected,'read-only anchor changed during publication')
    return got
def env(**items):
    with open(os.environ['GITHUB_ENV'],'a') as f:
        for k,v in items.items(): f.write(f'{k}={v}\n')
def literals(name):
    values={}
    for node in ast.parse((ROOT/'.github/scripts'/name).read_text()).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try: values[node.targets[0].id]=ast.literal_eval(node.value)
            except (ValueError,TypeError): pass
    return values
def decode(parts,digest,destination):
    raw=b''
    for path,sha in parts:
        piece=path.read_bytes();check(ghash(piece)==sha,'transport blob mismatch '+str(path));raw+=piece
    check(hashlib.sha256(raw).hexdigest()==digest,'transport concatenation mismatch')
    records=json.loads(lzma.decompress(raw));check('SOURCE_MANIFEST.json' in records,'missing source manifest')
    for name,item in records.items():
        p=Path(name);check(not p.is_absolute() and '..' not in p.parts and not {'artifacts','evidence','review_inputs','.git','transport'}.intersection(p.parts),'unsafe ordinary path')
        data=item['text'].encode();check(hashlib.sha256(data).hexdigest()==item['sha256'],'source SHA256 differs '+name)
        dst=destination/p;check(not dst.exists() or dst.read_bytes()==data,'would replace existing source '+str(dst))
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    return len(records)
def audit(directory=B):
    spec=importlib.util.spec_from_file_location('r45_publication_verify',ROOT/directory/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.verify()
def objects(ref):
    result={}
    for line in git('ls-tree','-r',ref).splitlines():
        meta,path=line.split('\t',1); result[path]=meta
    return result
def preserved(before):
    after=objects('HEAD');check(all(after.get(k)==v for k,v in before.items()),'existing Git object changed')
    return {'existing_git_objects':len(before),'all_existing_objects_unchanged':True,'map_sha256':hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest()}
def package(path,binding,products=False):
    names=[]
    scope=[str(P),'foundations/general-theta',REPORT_NAME,'.github/scripts/theta-r45-publish.py','.github/workflows/theta-r45-adapted-stopping.yml']
    for name in git('ls-files',*scope).splitlines():
        p=Path(name)
        if {'__pycache__','transport'}.intersection(p.parts) or p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}: continue
        if {'artifacts','evidence'}.intersection(p.parts) and not(products and name.startswith(str(B)+'/')): continue
        if p.suffix in {'.zip','.xz','.gz','.png','.jpg'}: continue
        if (ROOT/p).is_file(): names.append(name)
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:z.write(ROOT/name,name)
        z.writestr('R45_PUBLICATION_BINDING.json',json.dumps(binding,sort_keys=True,indent=2)+'\n')
    return len(names)
def source():
    check(os.environ.get('GITHUB_REF_NAME')==BRANCH,'write requested on wrong branch')
    bootstrap=git('rev-parse','HEAD');check(remote(BRANCH)==bootstrap,'bootstrap lease moved')
    anchor=pins(); before=objects(bootstrap)
    old43=literals('theta-r43-publish.py');old44=literals('theta-r44-publish.py')
    c43=decode([(ROOT/P/'r44-stopping-disintegration/transport'/f'r43.part{i:02}',s) for i,s in enumerate(old43['BLOBS'])],old43['TRANSPORT_SHA256'],ROOT/P/'r43-stopped-occupation')
    c44=decode([(ROOT/'.github/data'/f'theta-r44.part{i:02}',s) for i,s in enumerate(old44['PARTS'])],old44['TRANSPORT'],ROOT/P/'r44-stopping-disintegration')
    c45=decode([(ROOT/'.github/data'/f'theta-r45.part{i:02}',s) for i,s in enumerate(PARTS)],TRANSPORT,ROOT/B)
    report=(ROOT/REPORT_NAME).read_bytes();check(ghash(report)==REPORT,'latest pinned review differs')
    for name in ('r43-stopped-occupation','r44-stopping-disintegration','r45-adapted-stopping'):
        dst=ROOT/P/name/'review_inputs/R32_EXTERNAL_REFEREE_REPORT.md';check(not dst.exists() or dst.read_bytes()==report,'review input replacement')
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(report)
    for directory,projection in [('r43-stopped-occupation',old43['PROJECTION']),('r44-stopping-disintegration',old44['PROJECTION']),('r45-adapted-stopping',PROJECTION)]:
        a=audit(P/directory);check(a['ordinary_source_projection_tree_sha']==projection and a['review_input_verified'],'source/review audit failed '+directory)
    a=audit();git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    allowed=[str(P/n)+'/' for n in ('r43-stopped-occupation','r44-stopping-disintegration','r45-adapted-stopping')]
    git('add',*[n[:-1] for n in allowed]);changed=git('diff','--cached','--name-only').splitlines()
    check(changed and all(any(n.startswith(p) for p in allowed) for n in changed),'source write scope')
    git('commit','-m','source(theta restart R45): adapted stopping occupation theorem, raw classical/quantum realizations, unbuffered extension and matching mean-acquisition laws; preserve all prior source')
    source_sha=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==bootstrap,'ordinary source ancestry')
    preservation=preserved(before);check(remote(BRANCH)==bootstrap,'source lease moved')
    git('push','origin','HEAD:refs/heads/'+BRANCH);check(remote(BRANCH)==source_sha,'source readback differs');pins(anchor)
    data={'stage':'ORDINARY_SOURCE_PUBLISHED; not yet build-certified','source_commit':source_sha,'bootstrap_commit':bootstrap,'source_branch':BRANCH,'ordinary_source_projection_tree_sha':PROJECTION,'native_directory_tree_sha':git('rev-parse','HEAD:'+str(B)),'source_audit':a,'recovered_R43_files':c43,'recovered_R44_files':c44,'native_R45_files':c45,'transport_sha256':TRANSPORT,'read_only_anchor_heads':anchor,'preservation':preservation,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'policy':'Only new R45 research ref is pushed, without force; ordinary source then artifact-only child. Old R44 build remains failed, historical branches unchanged.'}
    (TMP/'binding.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');(TMP/'before_objects.json').write_text(json.dumps(before,sort_keys=True))
    out=TMP/'source';out.mkdir(exist_ok=True);package(out/'R45_ordinary_source.zip',data)
    (out/'SOURCE_EXPORT.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    env(SOURCE_SHA=source_sha,EXPECTED_TREE=PROJECTION,SOURCE_EXPORT_DIR=str(out),R45_PUBLICATION_DIR=str(TMP));print(json.dumps(data,indent=2))
def artifacts():
    data=json.loads((TMP/'binding.json').read_text());s=data['source_commit'];before=json.loads((TMP/'before_objects.json').read_text())
    check(git('rev-parse','HEAD')==s and remote(BRANCH)==s and not git('diff','--name-only'),'source changed during build')
    check(audit()['ordinary_source_projection_tree_sha']==PROJECTION,'native ordinary source mutated');preserved(before);pins(data['read_only_anchor_heads'])
    receipt=json.loads((TMP/'BUILD_RECEIPT.json').read_text());check(receipt['status']=='PASS' and receipt['source_commit']==s and receipt['ordinary_source_projection_tree_sha']==PROJECTION,'build source binding mismatch')
    out=ROOT/B/'artifacts';ev=ROOT/B/'evidence';out.mkdir(exist_ok=True);ev.mkdir(exist_ok=True)
    pdfs=list((TMP/'build').glob('*.pdf'));check(len(pdfs)==20,'expected 20 complete delivery PDFs')
    for p in pdfs:shutil.copyfile(p,out/p.name)
    shutil.copyfile(TMP/'build/R45_LATEX_BUILD.log',ev/'R45_LATEX_BUILD.log');shutil.copyfile(TMP/'BUILD_RECEIPT.json',ev/'BUILD_RECEIPT.json')
    data.update(stage='BUILT',delivery_pdfs=receipt['delivery_pdfs'],total_delivery_pages=receipt['total_delivery_pages'],total_isolated_pdf_builds=receipt['total_isolated_pdf_builds'],limitations=receipt['limitations'])
    (ev/'SOURCE_PUBLICATION.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    git('add','-f',str(out),str(ev));changed=git('diff','--cached','--name-only').splitlines();check(changed and all(n.startswith(str(out)+'/') or n.startswith(str(ev)+'/') for n in changed),'artifact-only write scope')
    git('commit','-m','artifacts(theta restart R45): twenty complete PDFs and immutable-source full-build receipt')
    a=git('rev-parse','HEAD');check(git('rev-parse','HEAD^')==s and remote(BRANCH)==s,'artifact ancestry/lease mismatch');git('push','origin','HEAD:refs/heads/'+BRANCH)
    check(remote(BRANCH)==a,'artifact readback differs');preserved(before);pins(data['read_only_anchor_heads']);data.update(stage='ARTIFACTS_PUBLISHED',artifact_commit=a)
    delivery=TMP/'delivery';delivery.mkdir(exist_ok=True);packet=delivery/'General_Theta_Foundations_I_R45_source_and_build_packet.zip';count=package(packet,data,True)
    summary={k:data[k] for k in ('source_commit','artifact_commit','ordinary_source_projection_tree_sha','native_directory_tree_sha','hosted_run_id','total_delivery_pages','total_isolated_pdf_builds')};summary.update(packaged_files=count,packet_sha256=hashlib.sha256(packet.read_bytes()).hexdigest())
    (delivery/'ARTIFACT_PUBLICATION.json').write_text(json.dumps(summary,indent=2)+'\n');env(ARTIFACT_SHA=a,DELIVERY_DIR=str(delivery));print(json.dumps(summary,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['source','artifacts']);args=ap.parse_args();(source if args.stage=='source' else artifacts)()
