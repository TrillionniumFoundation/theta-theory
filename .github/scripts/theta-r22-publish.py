#!/usr/bin/env python3
"""Hash-checked one-shot transport; never a build-time source generator."""
from __future__ import annotations
import base64,hashlib,json,lzma,os,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
B='papers/General-Theta-Foundations-I-restart/r22-discounted-response'
P='papers/General-Theta-Foundations-I-restart/'
T='.github/theta-publication/r22-discounted-response'
W='.github/workflows/general-theta-r22-discounted-response.yml'
HELPER='.github/scripts/theta-r22-publish.py'
BRANCH='foundation/general-theta-restart-r22-discounted-response-research-2026-10-09'
OPENING='5e958cf3b51b8e2dea8a669cc5890180f2958c80'
CANONICAL='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='1c580ed8c7b3bd05f1c8a04018a899895fcaf9c7'
REPORT='5eb8eb1de9643c81eb109da86f1d26c30fd26bb4'
R21='662b2fe5372f37d8fdc10142684d8db1003ca089'
EXPECTED='87751144b2241f66757cb67298b1c46326b03d9f'
CONTROLS=['foundations/general-theta/General_Theta_Foundations_v0.1.md','foundations/general-theta/RESTART_CHARTER.md','foundations/general-theta/REALIZATION_REGISTRY.md',P+'THEOREM_TARGETS.md']
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def h(b):return hashlib.sha256(b).hexdigest()
def env(k,v):
    with open(os.environ['GITHUB_ENV'],'a') as f:f.write(k+'='+v+'\n')
def jsonwrite(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def head_is(sha):require(git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]==sha,'remote branch changed; refuse publication')
def commit_push(message,expected):
    head_is(expected);require(git('rev-parse','HEAD')==expected,'unexpected local parent')
    git('commit','-m',message);sha=git('rev-parse','HEAD');require(git('rev-parse','HEAD^')==expected,'parent mismatch')
    git('push','origin','HEAD:refs/heads/'+BRANCH);head_is(sha);return sha

def source():
    require(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong publication branch')
    bootstrap=os.environ['GITHUB_SHA'];require(git('rev-parse','HEAD')==bootstrap,'wrong checkout');head_is(bootstrap)
    git('fetch','--no-tags','--depth=1','origin',OPENING,CANONICAL,REVIEW,R21)
    meta=json.loads(Path(T+'/PAYLOAD_META.json').read_text());parts=[]
    require(meta['native_directory']==B and meta['native_source_tree']==EXPECTED,'transport destination mismatch')
    for i in range(meta['parts']):
        raw=Path(T+f'/part{i:02d}.xz').read_bytes();require(h(raw)==meta['part_sha256'][i],'transport part mismatch');parts.append(raw)
    compressed=b''.join(parts);require(h(compressed)==meta['compressed_sha256'],'compressed hash mismatch')
    raw=lzma.decompress(compressed);require(h(raw)==meta['payload_sha256'],'payload mismatch');obj=json.loads(raw)
    require(obj['schema']==1 and obj['native_directory']==B,'payload schema mismatch')
    require(sorted(obj['files'])==meta['ordinary_paths'],'source inventory mismatch')
    for name,item in obj['files'].items():
        p=PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts,'unsafe native path')
        dest=Path(B)/p;require(not dest.is_symlink(),'native symlink forbidden');text=item['text'];require(isinstance(text,str),'invalid source')
        data=text.encode();require(h(data)==item['sha256'],'source hash mismatch: '+name)
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);dest.chmod(0o644)
    require(sorted(p.relative_to(B).as_posix() for p in Path(B).rglob('*') if p.is_file())==meta['ordinary_paths'],'unexpected source file')
    audit=json.loads(subprocess.check_output([sys.executable,B+'/verify.py'],text=True));require(audit['native_source_tree_sha']==EXPECTED,'native verification mismatch')
    git('rm','-r','--',T);git('add','--',B)
    index=git('write-tree');require(git('rev-parse',index+':'+B)==EXPECTED,'indexed source differs')
    git('config','user.name','General Theta source publication');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    sha=commit_push('source(theta restart R22): discounted common-controller response theorem, same-state effective frontier, singular realizations and full referee response',bootstrap)
    require(git('rev-parse',sha+':'+B)==EXPECTED,'source binding mismatch');env('SOURCE_SHA',sha);env('BOOTSTRAP_SHA',bootstrap)

def artifacts():
    source=os.environ['SOURCE_SHA'];require(git('rev-parse','HEAD')==source,'source moved before artifacts');require(git('diff','--name-only')=='','build mutated tracked source')
    r=json.loads(Path(B+'/evidence/BUILD_RECEIPT.json').read_text());require(r['status']=='PASS' and r['source_commit']==source and r['native_source_tree_sha']==EXPECTED,'build/source mismatch')
    preserved={}
    for line in git('ls-tree',OPENING+':'+P.rstrip('/')).splitlines():
        info,name=line.split('\t',1)
        if name=='r22-discounted-response':continue
        old=info.split()[2];new=git('rev-parse','HEAD:'+P+name);require(old==new,'inherited object changed: '+name);preserved[P+name]=new
    for name in CONTROLS:
        old=git('rev-parse',CANONICAL+':'+name);new=git('rev-parse','HEAD:'+name);require(old==new,'control changed');preserved[name]=new
    require(git('rev-parse',REVIEW+':GENERAL_THETA_FOUNDATIONS_I_RESTART_R20_UNIFORM_CAUSAL_TRANSFER_EXTERNAL_REFEREE_REPORT_R20.md')==REPORT,'review blob mismatch')
    for name in git('diff','--name-only',OPENING,'HEAD').splitlines():
        require(name.startswith(B+'/') or name.startswith(T+'/') or name in (W,HELPER),'unrelated change: '+name)
    anchors={}
    for branch,expected in [('foundation/general-theta-foundations-i-restart-2026-10-06',CANONICAL),('review/general-theta-restart-r20-uniform-causal-transfer-external-top4-referee-r20-2026-10-09',REVIEW)]:
        actual=git('ls-remote','origin','refs/heads/'+branch).split()[0];require(actual==expected,'input anchor moved');anchors[branch]=actual
    item={'source_commit':source,'native_source_tree':EXPECTED,'bootstrap_commit':os.environ['BOOTSTRAP_SHA'],'opening_import_commit':OPENING,'canonical_commit':CANONICAL,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'hosted_run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'preserved_objects':preserved,'anchor_readback':anchors,'report_commit':REVIEW,'report_blob':REPORT,'parallel_R21_pinned_contract':R21,'non_force_push':True,'source_regeneration_during_build':False,'delivery_pdfs':r['delivery_pdfs'],'limits':'Complete R22 and preserved R20/X/W/V/U/T/S; not all historical mathematics re-certified. Builds and finite checks are not continuum proofs or priority certificates.'}
    jsonwrite(B+'/evidence/SOURCE_PUBLICATION.json',item)
    git('add','-f','--',B+'/artifacts',B+'/evidence')
    sha=commit_push('build(theta restart R22): immutable-source PDF packet and full hosted receipts',source)
    for name in git('diff','--name-only',source,sha).splitlines():require(name.startswith(B+'/artifacts/') or name.startswith(B+'/evidence/'),'artifact commit changed source')
    env('ARTIFACT_SHA',sha)

def packet():
    artifact=os.environ['ARTIFACT_SHA'];require(git('rev-parse','HEAD')==artifact,'wrong artifact head');head_is(artifact)
    out=Path(os.environ['RUNNER_TEMP'])/'theta-r22-delivery';out.mkdir(exist_ok=True)
    target=out/'General_Theta_Foundations_I_R22_source_and_build_packet.zip';selected={}
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in subprocess.check_output(['git','ls-files','-z']).decode().split('\0'):
            if not name or not Path(name).is_file():continue
            choose=name.startswith(B+'/') or name.startswith('foundations/general-theta/') or name in (W,HELPER,P+'THEOREM_TARGETS.md')
            if name.startswith(P) and not name.startswith(B+'/'):
                rel=PurePosixPath(name[len(P):]);choose=not bool({'artifacts','evidence','__pycache__'}.intersection(rel.parts))
            if not choose:continue
            data=Path(name).read_bytes();z.writestr(name,data);selected[name]=h(data)
        data=subprocess.check_output(['git','cat-file','blob',REPORT]);name='EXTERNAL_R20_REFEREE_REPORT.md';z.writestr(name,data);selected[name]=h(data)
        item={'repository':'TrillionniumFoundation/theta-theory','research_branch':BRANCH,'canonical_commit':CANONICAL,'review_commit':REVIEW,'source_commit':os.environ['SOURCE_SHA'],'native_source_tree':EXPECTED,'artifact_commit':artifact,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'files_sha256':selected}
        z.writestr('REMOTE_PACKET_BINDING.json',json.dumps(item,sort_keys=True,indent=2)+'\n')
    jsonwrite(out/'DELIVERY_SHA256.json',{'zip_sha256':h(target.read_bytes()),'source_commit':os.environ['SOURCE_SHA'],'artifact_commit':artifact,'native_source_tree':EXPECTED,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'files':len(selected)+1})
    print(json.dumps({'zip':str(target),'files':len(selected)+1,'bytes':target.stat().st_size,'artifact_commit':artifact},sort_keys=True))
if __name__=='__main__':
    require(len(sys.argv)==2 and sys.argv[1] in ('source','artifacts','packet'),'mode required');{'source':source,'artifacts':artifacts,'packet':packet}[sys.argv[1]]()
