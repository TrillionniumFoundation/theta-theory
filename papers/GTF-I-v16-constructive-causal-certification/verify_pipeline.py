#!/usr/bin/env python3
"""Source/label contract checks. Not semantic verification of theorem proofs."""
from pathlib import Path
import hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
g=json.loads((HERE/'PIPELINE_GRAPH.json').read_text());snap=json.loads((HERE/'REPOSITORY_SNAPSHOT.json').read_text())
p=ROOT/g['inherited_graph']['path'];need(hashlib.sha256(p.read_bytes()).hexdigest()==g['inherited_graph']['sha256'],'Inherited graph hash mismatch')
previous=json.loads(p.read_text());by={c['component']:c for c in g['components']}
need(set(by)=={c['component'] for c in previous['components']} and len(by)==11,'Component inventory changed')
for c in previous['components']:
    for key,value in c.items():need(by[c['component']].get(key)==value,'Inherited component field altered: '+c['component']+'.'+key)
need(g['new_internal_edges'][:len(previous['new_internal_edges'])]==previous['new_internal_edges'],'Inherited internal edges altered')
labels=set()
for p in (ROOT/'papers').rglob('*.tex'):labels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
for label in g['new_theorem_spine']:need(label in labels,'Absent new label '+label)
for c in g['components']:
    need(c['full_historical_target_closed_by_v16'] is False,'Unsupported whole-target closure')
    for edge in c.get('v16_edges',[]):
        for label in edge['labels']:need(label in labels,'Absent consumer label '+label)
for edge in g['new_internal_edges']:
    for label in edge['from']+[edge['to']]:need(label in labels,'Absent internal label '+label)
need(g['edition']=='General Theta Foundations I, sixteenth constructive-causal-certification revision','Wrong edition')
need(g['schema']=='gtf.typed-dependency-graph.v16','Wrong schema')
need(g['base_commit']=='09d5540897d592a5e434f7431bfff470b4ebad1a','Wrong actual manuscript base')
need(snap['controlling_review']==g['controlling_review'],'Review snapshot mismatch')
need(snap['latest_named_review']['expected_report_present'] is False,'An unavailable review must not be claimed as read')
need(by['A2']['primary_chain']['verified_gtf_dependency'] is False,'Unsupported A2 primary dependency')
r=g['controlling_review'];p=subprocess.run(['git','rev-parse',r['commit']+':'+r['path']],cwd=ROOT,text=True,capture_output=True)
if p.returncode==0:need(p.stdout.strip()==r['git_blob'],'Deposited review blob mismatch')
if os.environ.get('GITHUB_ACTIONS')=='true':need(p.returncode==0,'Remote build did not retrieve the frozen deposited report')
print(json.dumps({'status':'passed','components':11,'inherited_component_fields_preserved':True,'review_blob_checked_from_git':p.returncode==0,'review_not_a_review_of_complete_v15':True,'latest_named_r2_report_available_at_snapshot':False,'new_internal_edges':len(g['new_internal_edges'])-len(previous['new_internal_edges']),'new_B4_edges':len(by['B4']['v16_edges']),'full_historical_B4_closed':False,'scope':'Source identities, edition, preserved fields and label existence; not analytic proof checking.'},indent=2))
