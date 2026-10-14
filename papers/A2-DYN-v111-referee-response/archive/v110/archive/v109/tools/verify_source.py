#!/usr/bin/env python3
"""Check exact source provenance, preservation and claim boundaries."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
P=Path(__file__).resolve().parents[1]
ACTIVE='papers/A2-DYN-v109-referee-response'
BASE='e863e8c110ffee472b3d10163a129a2bcfe9c0e1'
OLD='papers/A2-DYN-v108-referee-response'
TREE='e66a1dec484f419d88c05f12a7e2ec5310430448'
REPORT='reviews/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14/REFEREE_REPORT.md'
REPORT_BLOB='5080564a78a192984acc272bc31c7ef8165bda4e'

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def git(*args):
    return subprocess.check_output(['git',*args],cwd=P,text=True).strip()
def entries(ref):
    raw=subprocess.check_output(['git','ls-tree','-rz','--full-tree',ref],cwd=P)
    out={}
    for item in raw.split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1); mode,kind,sha=meta.decode().split()
            need(kind=='blob','unexpected tree leaf')
            out[path.decode()]=(mode,sha)
    return out

def verify():
    need(not sys.argv[1:],'no bypass')
    head=git('rev-parse','HEAD')
    if os.environ.get('GITHUB_ACTIONS')=='true':
        need(head==os.environ.get('GITHUB_SHA'),'not exact checkout')
    need(git('rev-parse','HEAD:'+OLD)==TREE,'changed author source')
    need(git('rev-parse','HEAD:'+ACTIVE+'/archive/v108')==TREE,'archive not exact')
    need(git('rev-parse','HEAD:'+REPORT)==REPORT_BLOB,'changed report')
    allowed={'A2_DYN_V109_REVISION_INDEX.md','.github/workflows/a2-dyn-v109-source-and-manuscript.yml'}
    changed=git('diff','--name-only',BASE,head).splitlines()
    need(all(n.startswith(ACTIVE+'/') or n in allowed for n in changed),'unrelated changes')
    old=entries('HEAD:'+OLD); current=entries('HEAD:'+ACTIVE)
    need(len([n for n in old if n.startswith('core/') and n.endswith('.tex')])==259,'historical core count')
    need(len([n for n in current if n.startswith('core/') and n.endswith('.tex')])==2,'new core count')
    for name,(mode,sha) in current.items():
        path=P/name; data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        need(actual==sha,'working bytes: '+name)
        need(bool(path.stat().st_mode & 0o111)==(mode=='100755'),'mode: '+name)
        if name.endswith('.tex') and not name.startswith('archive/'):
            need(all(b in (9,10,13) or b>=32 for b in data),'control character: '+name)
    need(current['model.tex'][1]=='6af1dcb4548e1b5dd82b9a330dead6e04fd09797','physical target changed')
    manifest=json.loads((P/'SOURCE_MANIFEST.json').read_text())
    need(manifest['revision']==109 and manifest['total_core_count']==261,'manifest identity')
    for key in ('full_raw_return_LLT_proved','primary_referee_request_closed','nongrazing_residual_height_decay_proved','independent_human_review','formal_proof_certificate'):
        need(manifest['claims'][key] is False,'unsupported claim: '+key)
    need(json.loads((P/'PUBLICATION_STATUS.json').read_text())==manifest['claims'],'claim records disagree')
    return {'revision':109,'checkout_sha':head,'paper_tree':git('rev-parse','HEAD:'+ACTIVE),
            'historical_tree':TREE,'report_blob':REPORT_BLOB,'preserved_historical_files':len(old),
            'historical_core_count':259,'new_core_count':2,'original_problem_blob_preserved':True,
            'unrelated_paths_unchanged':True,'formal_proof_certificate':False}
if __name__=='__main__': print(json.dumps(verify(),sort_keys=True,indent=2))
