#!/usr/bin/env python3
"""One-shot, hash-bound publication; never a manuscript build dependency."""
from __future__ import annotations
import base64,hashlib,json,lzma,os,shutil,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
B='papers/General-Theta-Foundations-I-restart/r19-effective-frontier'
P='papers/General-Theta-Foundations-I-restart/'
T='.github/theta-publication/r19-effective-frontier'
W='.github/workflows/general-theta-r19-effective-frontier.yml'
HELPER='.github/scripts/theta-r19-publish.py'
BRANCH='foundation/general-theta-restart-r19-effective-frontier-research-2026-10-09'
OPENING='f33ff4c9a6dbb36677516c92f51706b4deacf3f0'
CANONICAL='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='1c70af9be79e93af9db5ea9cfc2a0271e8fe47ac'
REPORT='4dac5985a5f4b57e6807c2eba5073228bde16fb1'
EXPECTED='ce14e0d57fef7aa415a4065cd3dac75172dd1efa'
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
    git('commit','-m',message);sha=git('rev-parse','HEAD')
    require(git('rev-parse','HEAD^')==expected,'parent mismatch')
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    head_is(sha);return sha

def source():
    require(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong publication branch')
    bootstrap=os.environ['GITHUB_SHA'];require(git('rev-parse','HEAD')==bootstrap,'wrong checkout');head_is(bootstrap)
    git('fetch','--no-tags','--depth=1','origin',OPENING,CANONICAL,REVIEW)
    meta=json.loads(Path(T+'/PAYLOAD_META.json').read_text());parts=[]
    require(meta['native_directory']==B and meta['native_source_tree']==EXPECTED,'transport destination mismatch')
    for i in range(meta['parts']):
        raw=Path(T+f'/part{i:02d}.xz').read_bytes();encoded=base64.b64encode(raw)
        require(h(encoded)==meta['part_sha256'][i],'transport part mismatch');parts.append(raw)
    compressed=b''.join(parts);require(h(compressed)==meta['compressed_sha256'],'compressed hash mismatch')
    encoded=base64.b64encode(compressed);require(h(encoded)==meta['encoded_sha256'] and len(encoded)==meta['encoded_bytes'],'encoded hash mismatch')
    raw=lzma.decompress(compressed);require(h(raw)==meta['payload_sha256'],'payload mismatch');obj=json.loads(raw)
    require(obj['schema']==2 and obj['native_directory']==B and len(obj['files'])==7,'payload schema mismatch')
    for name,text in obj['files'].items():
        p=PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts and isinstance(text,str),'unsafe native path')
        dest=Path(B)/p;require(not dest.is_symlink(),'native symlink forbidden');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(text.encode());dest.chmod(0o644)
    subprocess.check_call([sys.executable,B+'/prepare_r19.py'])
    require(set(p.relative_to(B).as_posix() for p in Path(B).rglob('*') if p.is_file())==set(meta['ordinary_paths']),'unexpected ordinary source file')
    audit=json.loads(subprocess.check_output([sys.executable,B+'/verify.py'],text=True));require(audit['native_source_tree_sha']==EXPECTED,'native verification mismatch')
    # The transport is no longer editable at the ordinary-source head. Its exact
    # bytes remain available in the immutable bootstrap ancestor.
    git('rm','-r','--',T);git('add','--',B)
    index=git('write-tree');require(git('rev-parse',index+':'+B)==EXPECTED,'indexed native tree differs')
    git('config','user.name','General Theta source publication');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    sha=commit_push('source(theta restart R19): effective causal frontier, support-preserving finite certificates and noncontracting raw realizations; complete proofs and audits',bootstrap)
    require(git('rev-parse',sha+':'+B)==EXPECTED,'ordinary source tree mismatch')
    env('SOURCE_SHA',sha);env('BOOTSTRAP_SHA',bootstrap)

def artifacts():
    source=os.environ['SOURCE_SHA'];require(git('rev-parse','HEAD')==source,'source changed before artifact commit')
    require(git('diff','--name-only')=='','tracked files changed during build')
    r=json.loads(Path(B+'/evidence/BUILD_RECEIPT.json').read_text())
    require(r['status']=='PASS' and r['source_commit']==source and r['native_source_tree_sha']==EXPECTED,'build/source binding mismatch')
    preserved={}
    for line in git('ls-tree',OPENING+':'+P.rstrip('/')).splitlines():
        info,name=line.split('\t',1)
        if name=='r19-effective-frontier':continue
        old=info.split()[2];new=git('rev-parse','HEAD:'+P+name);require(old==new,'inherited object changed: '+name);preserved[P+name]=new
    require(git('rev-parse',REVIEW+':GENERAL_THETA_FOUNDATIONS_I_RESTART_R18_CAUSAL_ALLOCATION_EXTERNAL_REFEREE_REPORT_R18.md')==REPORT,'review blob changed')
    for name in CONTROLS:
        old=git('rev-parse',CANONICAL+':'+name);new=git('rev-parse','HEAD:'+name);require(old==new,'canonical control changed');preserved[name]=new
    for name in git('diff','--name-only',OPENING,'HEAD').splitlines():
        require(name.startswith(B+'/') or name.startswith(T+'/') or name in (W,HELPER),'unrelated path changed: '+name)
    anchors={}
    for branch,expected in [('foundation/general-theta-foundations-i-restart-2026-10-06',CANONICAL),('review/general-theta-restart-r18-causal-allocation-external-top4-referee-r18-2026-10-09',REVIEW)]:
        actual=git('ls-remote','origin','refs/heads/'+branch).split()[0];require(actual==expected,'input anchor moved');anchors[branch]=actual
    item={'source_commit':source,'native_source_tree':EXPECTED,'bootstrap_commit':os.environ['BOOTSTRAP_SHA'],'opening_commit':OPENING,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'hosted_run_attempt':os.environ['GITHUB_RUN_ATTEMPT'],'preserved_objects':preserved,'anchor_readback':anchors,'report_commit':REVIEW,'report_blob':REPORT,'non_force_push':True,'source_regeneration_during_build':False,'delivery_pdfs':r['delivery_pdfs'],'limits':'Complete native R19 plus intact R18/V/U/T/S, not all repository papers. Regression and PDF checks are not continuum proofs or a priority determination.'}
    jsonwrite(B+'/evidence/SOURCE_PUBLICATION.json',item)
    git('add','-f','--',B+'/artifacts',B+'/evidence')
    sha=commit_push('build(theta restart R19): immutable-source PDFs and full hosted verification receipts',source)
    for name in git('diff','--name-only',source,sha).splitlines():require(name.startswith(B+'/artifacts/') or name.startswith(B+'/evidence/'),'artifact commit changed source')
    env('ARTIFACT_SHA',sha)

def packet():
    artifact=os.environ['ARTIFACT_SHA'];require(git('rev-parse','HEAD')==artifact,'wrong artifact head');head_is(artifact)
    out=Path(os.environ['RUNNER_TEMP'])/'theta-r19-delivery';out.mkdir(exist_ok=True)
    target=out/'General_Theta_Foundations_I_R19_source_and_build_packet.zip';selected={}
    files=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            if not name or not Path(name).is_file():continue
            choose=name.startswith(B+'/') or name.startswith('foundations/general-theta/') or name in (W,HELPER,P+'THEOREM_TARGETS.md')
            if name.startswith(P) and not name.startswith(B+'/'):
                rel=PurePosixPath(name[len(P):]);choose=not bool({'artifacts','evidence','__pycache__'}.intersection(rel.parts))
            if not choose:continue
            data=Path(name).read_bytes();z.writestr(name,data);selected[name]=h(data)
        report=subprocess.check_output(['git','cat-file','blob',REPORT]);reportname='EXTERNAL_R18_REFEREE_REPORT.md';z.writestr(reportname,report);selected[reportname]=h(report)
        item={'repository':'TrillionniumFoundation/theta-theory','research_branch':BRANCH,'canonical_commit':CANONICAL,'review_commit':REVIEW,'source_commit':os.environ['SOURCE_SHA'],'native_source_tree':EXPECTED,'artifact_commit':artifact,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'files_sha256':selected}
        z.writestr('REMOTE_PACKET_BINDING.json',json.dumps(item,sort_keys=True,indent=2)+'\n')
    jsonwrite(out/'DELIVERY_SHA256.json',{'zip_sha256':h(target.read_bytes()),'source_commit':os.environ['SOURCE_SHA'],'artifact_commit':artifact,'native_source_tree':EXPECTED,'hosted_run_id':os.environ['GITHUB_RUN_ID'],'files':len(selected)+1})
    print(json.dumps({'zip':str(target),'files':len(selected)+1,'bytes':target.stat().st_size,'artifact_commit':artifact},sort_keys=True))

if __name__=='__main__':
    require(len(sys.argv)==2 and sys.argv[1] in ('source','artifacts','packet'),'mode required')
    {'source':source,'artifacts':artifacts,'packet':packet}[sys.argv[1]]()
