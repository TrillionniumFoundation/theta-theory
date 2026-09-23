#!/usr/bin/env python3
"""Check source identities and declared edges, not mathematical truth."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
ledger=json.loads((P/'PROOF_STATUS.json').read_text()); graph=json.loads((P/'PIPELINE_GRAPH.json').read_text())
labels=set();count=0
for f in P.glob('*.tex'): labels.update(re.findall(r'\\label\{([^}]+)\}',f.read_text()))
for row in ledger['statements']:
 f=P/row['source_file']
 if hashlib.sha256(f.read_bytes()).hexdigest()!=row['source_sha256']:raise RuntimeError('Statement source changed: '+f.name)
 if row['id'] not in labels:raise RuntimeError('Missing label '+row['id'])
 count+=1
for edge in graph['current_edges']:
 for k in ('from','to'):
  if edge[k] not in labels and edge[k]!='C2:v18-bounded-gaussian-consumer':raise RuntimeError('Missing edge endpoint '+edge[k])
components=graph['inherited_v17_declarations']
if isinstance(components,list): names={x.get('id',x.get('component')) for x in components}
else:names=set(components)
if not {'A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','D1'}<=names:raise RuntimeError('Missing historical component')
if graph['current_credit']['A2_primary_chain']!='independent_not_consumed':raise RuntimeError('Artificial A2 dependency')
if graph['current_credit']['full_historical_program_closed_by_gtf_v18']:raise RuntimeError('Unsupported aggregate closure')
for row in graph['historical_statement_dispositions']:
 for x in row['repaired_by']:
  if x not in labels:raise RuntimeError('Unknown repair theorem '+x)
print(json.dumps({'scope':'source/hash/declared-contract check only; not an analytic proof check','canonical_statement_sources':count,'labels':len(labels),'current_edges':len(graph['current_edges']),'historical_components':sorted(names),'historical_dispositions':len(graph['historical_statement_dispositions']),'A2_dependency_not_invented':True,'full_historical_closure_not_asserted':True},indent=2))
