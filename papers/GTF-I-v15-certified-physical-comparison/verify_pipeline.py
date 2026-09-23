#!/usr/bin/env python3
"""Check frozen source identities and label contracts, not analytic proofs."""
from pathlib import Path
import hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
g=json.loads((HERE/'PIPELINE_GRAPH.json').read_text())
p=ROOT/g['inherited_manifest']['path']
need(hashlib.sha256(p.read_bytes()).hexdigest()==g['inherited_manifest']['sha256'],'Inherited graph digest mismatch')
expected={c['component']:c for c in json.loads(p.read_text())['components']}
need({c['component'] for c in g['components']}==set(expected),'Eleven-component inventory mismatch')
need(len(g['components'])==11,'Wrong component count')
labels=set()
for p in (ROOT/'papers').rglob('*.tex'):
    labels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
edge_counts={k:0 for k in ('new_edges','v12_edges','v13_edges','v14_edges','v15_edges')}
for c in g['components']:
    need(c['inherited_status']==expected[c['component']]['status'],'Inherited status altered')
    need(c['full_historical_target_closed_by_v15'] is False,'Unsupported full historical closure')
    for label in c['inherited_theorem_labels']:need(label in labels,'Absent inherited label '+label)
    for kind in edge_counts:
        for edge in c.get(kind,[]):
            edge_counts[kind]+=1
            for label in edge['labels']:need(label in labels,'Absent edge label '+label)
for edge in g['new_internal_edges']:
    for label in edge['from']+[edge['to']]:need(label in labels,'Absent internal label '+label)
a2=next(c for c in g['components'] if c['component']=='A2')
need(a2['primary_chain']['verified_gtf_dependency'] is False,'A2 primary dependency misdeclared')
need(g['edition']=='General Theta Foundations I, fifteenth certified-physical-comparison revision','Wrong live edition')
review=g['controlling_review']; git=subprocess.run(['git','rev-parse',review['commit']+':'+review['path']],cwd=ROOT,text=True,capture_output=True)
if git.returncode==0:need(git.stdout.strip()==review['git_blob'],'Review source mismatch')
if os.environ.get('GITHUB_ACTIONS')=='true':need(git.returncode==0,'Remote build did not verify the controlling review blob')
previous_path=ROOT/g['inherited_graph']['path']
need(hashlib.sha256(previous_path.read_bytes()).hexdigest()==g['inherited_graph']['sha256'],'Previous graph digest mismatch')
previous=json.loads(previous_path.read_text())
by_component={c['component']:c for c in g['components']}
for c in previous['components']:
    for key,value in c.items():need(by_component[c['component']].get(key)==value,'Inherited component field altered: '+c['component']+'.'+key)
need(g['new_internal_edges'][:len(previous['new_internal_edges'])]==previous['new_internal_edges'],'Inherited internal edges altered')
need(g['base_commit']=='5c855fde40aa40bb3d79e7473b2a78a54e4e3d9f','Unexpected controlling review base')
ancestor=subprocess.run(['git','merge-base','--is-ancestor',review['commit'],g['base_commit']],cwd=ROOT,capture_output=True)
if os.environ.get('GITHUB_ACTIONS')=='true':need(ancestor.returncode==0,'Controlling review not the base ancestor')
snapshot=json.loads((HERE/'REPOSITORY_SNAPSHOT.json').read_text())
need(snapshot['controlling_review']==review,'Snapshot review mismatch')
print(json.dumps({'status':'passed','components':11,'edge_counts':edge_counts,'new_internal_edges':len(g['new_internal_edges']),'review_blob_checked_from_git':git.returncode==0,'primary_a2_dependency':False,'freshness_separate':True,'scope':'Source identity, inventory and label-existence checks; not semantic proof verification.'},indent=2))
