#!/usr/bin/env python3
"""Publish prewritten, hash-bound R52 source; no research code is generated here."""
from __future__ import annotations
import argparse, hashlib, json, lzma, os, pathlib, shutil, subprocess, zipfile
ROOT=pathlib.Path.cwd()
REL=pathlib.Path('papers/General-Theta-Foundations-I-restart/r52-stopped-experiment')
OLD=REL.parent/'r51-causal-acquisition'
PROJECTION='d732491ca53d7bc337b89631847106c1dd862cbb'
PARTS=['2526363122de6f84ab2eb1b6fa5aa7244ba05ce0','836c4a9e5d970a4d688e2a39934319a8815be87e','38451d54e8b497c87de87103b2cb9716e670ba20','35fa0c7766e2eee28efe63a7c56696d591e70a5d','0dfb99e3491cebdcd53d142f5660cc92e5097c4b','67631267d42581b7667d0ce358fc711fc6402cd5','67968d0a586b8cfc96494bcf5bb3ee2e19bdb73c','3e97ea0d7b7bf7314aaff1a21ff0057a431af15b','86e7a76b2cdb785ca4fcff2118b60cd6e6ec7627','569cbb26647742f774564d5e9293830d81cb3613','e09084887f40755b5c413bede0c6fe5f8eef13c9','f59c2f2f48c9e63409e6903d68dbb36a6b340683','bd49dd23a16fd06fe5f37a492df91f2170031c35']
def require(ok:bool,message:str)->None:
    if not ok: raise RuntimeError(message)
def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def blob(data:bytes)->str:return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def pinned(path:pathlib.Path,sha:str)->bytes:
    data=path.read_bytes();require(blob(data)==sha,'input blob mismatch: '+str(path));return data
def materialize()->None:
    dst=ROOT/REL;old=ROOT/OLD
    require(not dst.exists(),'refusing to replace existing manuscript source')
    raw=b''.join(pinned(ROOT/f'.github/data/theta-r52-source-part{i:02}.xzpart',sha) for i,sha in enumerate(PARTS))
    require(digest(raw)=='a5e393e41ff33b56cf11862fc1051ffd1b41062a0e160472d97432d2c5dda5fb','source transport digest mismatch')
    records=json.loads(lzma.decompress(raw));require(len(records)==33,'source record count')
    for name,text in records.items():
        rel=pathlib.Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts and not {'.git','artifacts','evidence','transport'}.intersection(rel.parts),'unsafe source path')
        f=dst/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(text.encode())
    for name,sha in {'verify.py':'403281709f84bc8ba9fcf5e479abbedf471f1989','RECOVERY_PINS.json':'d735e6a854d29b55b0afdd6c8d9eb616a5f2879b'}.items():
        (dst/name).write_bytes(pinned(old/name,sha))
    s=pinned(old/'build.py','2499c2d00a67062714a58b9f73c490c446959d26').decode()
    s=s.replace('r49-acquired-risk','__PREDECESSOR_DIR__').replace('_R49_','__PREDECESSOR_PDF_TAG__').replace('restart_R49.pdf','__PREDECESSOR_MAIN__').replace('retained_complete_R49','__PREDECESSOR_RECEIPT__').replace('Full R49 manuscript','__PREDECESSOR_SCOPE__')
    s=s.replace('r51-causal-acquisition','r52-stopped-experiment').replace('theta-r51-','theta-r52-').replace('R51','R52')
    s=s.replace('__PREDECESSOR_DIR__','r51-causal-acquisition').replace('__PREDECESSOR_PDF_TAG__','_R51_').replace('__PREDECESSOR_MAIN__','restart_R51.pdf').replace('__PREDECESSOR_RECEIPT__','retained_complete_R51').replace('__PREDECESSOR_SCOPE__','Full R51 manuscript')
    s=s.replace('General_Theta_Foundations_I_R52_Companion_AcquiredRisk.pdf','General_Theta_Foundations_I_R52_Companion_CausalAcquisition.pdf')
    (dst/'build.py').write_bytes(s.encode())
    archive=old/'artifacts/R51_prepared_sources.zip'
    require(digest(archive.read_bytes())=='5eeeb76433dc03ce8e47948e6f7eedc40099d11611422c20121e2be02b13e02c','retained source archive digest mismatch')
    inventory={}
    with zipfile.ZipFile(archive) as z:
        for name in sorted(z.namelist()):
            rel=pathlib.Path(name)
            if name.endswith('/') or {'.git','artifacts','evidence','__pycache__'}.intersection(rel.parts) or rel.suffix not in {'.tex','.py','.md','.json'}:continue
            data=z.read(name);inventory[name]={'sha256':digest(data),'git_blob_sha':blob(data)}
    require(len(inventory)==1113,'historical inventory count')
    (dst/'HISTORY_INVENTORY.json').write_text(json.dumps({'scope':'Actual locally supplied ordinary dependency inventory; byte identity is not fresh proof verification','retained_head':'48562025a70d6b93ca826fb0e16342a2c6296b65','files':inventory},sort_keys=True,indent=2)+'\n')
    subprocess.run(['python3',str(dst/'gaussian_certificate.py'),'--write'],check=True)
    reviews=[(ROOT/'GENERAL_THETA_FOUNDATIONS_I_RESTART_R32_BAYESIAN_CURVATURE_EXTERNAL_REFEREE_REPORT_R32.md','R32_EXTERNAL_REFEREE_REPORT.md','3731f79996e11cdac66ce7c8a3ee5fdf1fffcd21'),(old/'REFEREE_RESPONSE.md','R51_REFEREE_RESPONSE.md','51038ba15d22d385a7df3aa962bae7ae60ecea51'),(old/'REFEREE_COMMENT_CONCORDANCE.md','R51_REFEREE_COMMENT_CONCORDANCE.md','aa5acdc7d889c341f336ec5f8e8a12657aed9d19')]
    for source,name,sha in reviews:
        target=dst/'review_inputs'/name;target.parent.mkdir(exist_ok=True);target.write_bytes(pinned(source,sha))
    require(digest((dst/'SOURCE_MANIFEST.json').read_bytes())=='72aa2108c5aa8ac1f374500781fcf3aacb3d8b6310101cec77ad96ef95570a3c','source manifest digest mismatch')
    for name,record in json.loads((dst/'PINNED_INPUTS.json').read_text())['controls'].items():pinned(ROOT/name,record['git_blob_sha'])
    audit=json.loads(subprocess.check_output(['python3',str(dst/'verify.py')]))
    require(audit['ordinary_source_projection_tree_sha']==PROJECTION,'ordinary source projection mismatch')
    print(json.dumps(audit,sort_keys=True,indent=2))
def artifacts()->None:
    out=pathlib.Path(os.environ['RUNNER_TEMP'])/'r52-output';dst=ROOT/REL/'artifacts'
    require(not dst.exists(),'refusing to overwrite artifact directory');dst.mkdir()
    receipt=json.loads((out/'BUILD_RECEIPT.json').read_text())
    require(receipt['status']=='PASS' and receipt['source_commit']==os.environ['R52_SOURCE_SHA'],'unbound or failed build')
    require(receipt['ordinary_source_projection_tree_sha']==PROJECTION,'built source projection mismatch')
    require(len(receipt['delivery_pdfs'])==25 and sum(x['pages'] for x in receipt['delivery_pdfs'].values())==633,'complete delivery page count mismatch')
    require(receipt['total_isolated_pdf_builds']==60,'retained build count mismatch')
    pins=json.loads((ROOT/REL/'PINNED_INPUTS.json').read_text())
    publication={'source_commit':os.environ['R52_SOURCE_SHA'],'workflow_trigger_commit':os.environ['GITHUB_SHA'],'workflow_run_id':os.environ['GITHUB_RUN_ID'],'canonical':pins['canonical_head'],'retained_head':pins['latest_complete_head'],'retention_commit':pins['new_retention_commit'],'external_review_head':pins['external_review_head'],'ordinary_source_projection_tree_sha':PROJECTION,'files_sha256':{f.name:digest(f.read_bytes()) for f in sorted(out.iterdir()) if f.is_file()},'scope':'R52 native and complete R51 retained mathematical chain; not all repository papers. Builds do not certify proof correctness, priority or journal significance.'}
    (out/'PUBLICATION_RECEIPT.json').write_text(json.dumps(publication,sort_keys=True,indent=2)+'\n')
    for f in out.iterdir():
        if f.is_file():shutil.copyfile(f,dst/f.name)
def packets()->None:
    temp=pathlib.Path(os.environ['RUNNER_TEMP']);out=temp/'r52-output';pack=temp/'r52-packets';native=pack/'native';native.mkdir(parents=True)
    for f in out.iterdir():
        if f.is_file() and (f.suffix!='.pdf' or f.name=='General_Theta_Foundations_I_restart_R52.pdf'):shutil.copyfile(f,native/f.name)
    for name,key in [('SOURCE_SHA.txt','R52_SOURCE_SHA'),('ARTIFACT_SHA.txt','R52_ARTIFACT_SHA')]: (native/name).write_text(os.environ[key]+'\n')
    (native/'GIT_TREE.txt').write_bytes(subprocess.check_output(['git','ls-tree','-r','HEAD']))
    pdfs=sorted(f for f in out.glob('*.pdf') if f.name!='General_Theta_Foundations_I_restart_R52.pdf');require(len(pdfs)==24,'retained PDF count')
    for i,f in enumerate(pdfs):
        group=pack/f'retained-{i//8+1}';group.mkdir(exist_ok=True);shutil.copyfile(f,group/f.name)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['materialize','artifacts','packets']);args=parser.parse_args()
    {'materialize':materialize,'artifacts':artifacts,'packets':packets}[args.mode]()
