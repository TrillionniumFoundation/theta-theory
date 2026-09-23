#!/usr/bin/env python3
"""Frozen source/label contracts; not a mathematical proof checker."""
from pathlib import Path
import hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
g=json.loads((HERE/'PIPELINE_GRAPH.json').read_text());previous_path=ROOT/g['inherited_graph']['path']
need(hashlib.sha256(previous_path.read_bytes()).hexdigest()==g['inherited_graph']['sha256'],'Inherited graph identity')
old=json.loads(previous_path.read_text());by={x['component']:x for x in g['components']}
need(set(by)=={x['component']for x in old['components']} and len(by)==11,'Eleven historical components')
for c in old['components']:
    for k,v in c.items():need(by[c['component']].get(k)==v,'Changed inherited field '+c['component']+'.'+k)
need(g['new_internal_edges'][:len(old['new_internal_edges'])]==old['new_internal_edges'],'Changed inherited edges')
labels=set()
for p in (ROOT/'papers').rglob('*.tex'):labels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
for label in g['new_theorem_spine']:need(label in labels,'Missing new proof label '+label)
for c in g['components']:
    need(c['full_historical_target_closed_by_v17'] is False,'Unsupported whole-target closure')
    for edge in c['v17_edges']:
        for label in edge['labels']:need(label in labels,'Missing consumer label '+label)
need(by['A2']['primary_chain']['verified_gtf_dependency'] is False,'Unsupported primary A2 dependency')
reviews=[]
for name in ('controlling_review','additional_review'):
    r=g[name];p=subprocess.run(['git','rev-parse',r['commit']+':'+r['path']],cwd=ROOT,text=True,capture_output=True)
    if p.returncode==0:need(p.stdout.strip()==r['git_blob'],'Review blob mismatch '+name)
    if os.environ.get('GITHUB_ACTIONS')=='true':need(p.returncode==0,'Remote review not fetched '+name)
    reviews.append({'role':name,'commit':r['commit'],'git_blob':r['git_blob'],'checked_from_git':p.returncode==0})
print(json.dumps({'status':'passed','components':11,'preserved_component_fields':True,'reviews':reviews,'new_internal_edges':len(g['new_internal_edges'])-len(old['new_internal_edges']),'new_C2_edges':len(by['C2']['v17_edges']),'new_B4_edges':len(by['B4']['v17_edges']),'full_historical_B4_closed':False,'full_historical_C2_closed':False,'scope':'Source identities, preserved fields and label existence, not semantic proof verification.'},indent=2))
