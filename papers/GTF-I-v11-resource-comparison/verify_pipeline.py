#!/usr/bin/env python3
"""Validate frozen source/label declarations, not mathematical implications."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
g=json.loads((HERE/'PIPELINE_GRAPH.json').read_text())
p=ROOT/g['inherited_manifest']['path']
need(hashlib.sha256(p.read_bytes()).hexdigest()==g['inherited_manifest']['sha256'],'Inherited graph digest mismatch')
old=json.loads(p.read_text()); expected={c['component']:c for c in old['components']}
need({c['component'] for c in g['components']}==set(expected),'Eleven-component inventory mismatch')
need(len(g['components'])==11,'Wrong component count')
labels=set()
for p in (ROOT/'papers').rglob('*.tex'):
    labels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
for c in g['components']:
    need(c['inherited_status']==expected[c['component']]['status'],'Inherited status altered')
    need(c['full_historical_target_closed_by_v11'] is False,'Unsupported historical closure declaration')
    for k in c['inherited_theorem_labels']:need(k in labels,'Absent inherited label '+k)
    for edge in c['new_edges']:
        for k in edge['labels']:need(k in labels,'Absent new label '+k)
a2=next(c for c in g['components'] if c['component']=='A2')
need(a2['primary_chain']['verified_gtf_dependency'] is False,'A2 primary dependency misdeclared')
review=g['controlling_review']; git=subprocess.run(['git','rev-parse',review['commit']+':'+review['path']],cwd=ROOT,text=True,capture_output=True)
if git.returncode==0:need(git.stdout.strip()==review['git_blob'],'Review source mismatch')
print(json.dumps({'status':'passed','components':11,'new_microscopic_edges':2,'review_blob_checked_from_git':git.returncode==0,'primary_a2_dependency':False,'scope':'Source identity, schema and label-existence checks; not theorem verification.'},indent=2))
