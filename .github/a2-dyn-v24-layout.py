#!/usr/bin/env python3
"""Two explicit typography repairs; qualify candidate, create immutable objects only."""
from pathlib import Path
import base64,hashlib,json,os,subprocess,sys,urllib.request
root=Path('papers/A2-DYN-v24-referee-response').resolve()
sys.path.insert(0,str(root/'tools'))
import verify_v24 as verify
prior_tree='71f93457a7bd69fefe7649db90b0dba1ff0ef4f9'
if verify.tree_hash(root).hex()!=prior_tree:raise RuntimeError('unexpected ordinary source before typography repair')
abstract_before='''A multiscale comparison over the actual return-clock deviations gives
fourth-root stopping errors in every fixed finite moment and Gaussian
polynomial moments with one actual-return insertion. Combined with
finite-order damped unsmoothing, it preserves the original marked
central error rate on a wider prescribed-count Fourier band.
'''
abstract_after='''Multiscale stopping further yields all fixed marked Gaussian moments and
fourth-root comparison errors, preserving the original central rate on a
wider prescribed-count Fourier band.
'''
main=(root/'main.tex').read_text()
if main.count(abstract_before)!=1:raise RuntimeError('abstract repair not unique')
(root/'main.tex').write_text(main.replace(abstract_before,abstract_after,1))
ledger=json.loads((root/'INHERITED_EDITS.json').read_text())
found=0
for edit in ledger['edits']:
    if abstract_before in edit['after']:
        if edit['after'].count(abstract_before)!=1:raise RuntimeError('ledger abstract not unique')
        edit['after']=edit['after'].replace(abstract_before,abstract_after,1)
        found+=1
if found!=1:raise RuntimeError('abstract edit ledger missing')
(root/'INHERITED_EDITS.json').write_text(json.dumps(ledger,indent=2,sort_keys=True)+'\n')
source=root/'core/50_multiscale_stopping.tex'
s=source.read_text()
before=r'''Recenter at $y=(F_R^*)^kx$. The original numerator becomes the
integral of $a(y)(Z_{n,k,R}(y)/\sqrt n)^{\otimes d}$.
'''
after=r'''Recenter at $y=(F_R^*)^kx$. The original numerator is
\[
 \int_{Y_R^*}a(y)
       \left(\frac{Z_{n,k,R}(y)}{\sqrt n}\right)^{\otimes d}\dd\nu(y).
\]
'''
if s.count(before)!=1:raise RuntimeError('display repair not unique')
source.write_text(s.replace(before,after,1))
changed=['main.tex','INHERITED_EDITS.json','core/50_multiscale_stopping.tex']
manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
for name in changed:manifest['source_sha256'][name]=verify.digest(root/name)
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
verify.source_checks()
# This candidate build is not the final event-source qualification. No
# source changes occur in the final read-only workflow after the tree is attached.
env=os.environ.copy()
for key in ('GITHUB_SHA','GITHUB_RUN_ID','GITHUB_RUN_ATTEMPT'):env.pop(key,None)
subprocess.run(['bash',str(root/'build.sh')],check=True,env=env)
expected=verify.tree_hash(root).hex()
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json',
 'Content-Type':'application/json','User-Agent':'a2-dyn-typography-objects'}
api='https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/'
def post(endpoint,body):
    if endpoint not in ('blobs','trees'):raise RuntimeError('immutable objects only')
    req=urllib.request.Request(api+endpoint,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)
entries=[]
for name in changed+['SOURCE_MANIFEST.json']:
    data=(root/name).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    result=post('blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})
    if result['sha']!=blob:raise RuntimeError('blob identity mismatch '+name)
    entries.append({'path':name,'mode':'100644','type':'blob','sha':blob})
result=post('trees',{'base_tree':prior_tree,'tree':entries})
if result['sha']!=expected:raise RuntimeError('assembled tree differs from verified ordinary source')
checks=json.loads((root/'evidence/v24-source-and-finite-checks.json').read_text())
receipt={'paper_tree':expected,'prior_paper_tree':prior_tree,'changed_blobs':entries,
 'candidate_build_passed':True,'final_event_source_qualified':False,
 'inherited_core_files_byte_identical':checks['source']['inherited_core_byte_identical'],
 'retained_math_labels':checks['source']['retained_mathematical_labels'],
 'candidate_pdf_sha256':verify.digest(root/'build/main.pdf'),
 'repairs':['condense only the new abstract summary','display the exact recentered moment integral'],
 'mathematical_conclusions_changed':False,'branch_refs_changed':False,'commits_created':False}
Path('v24-layout-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
