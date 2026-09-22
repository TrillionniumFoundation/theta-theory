#!/usr/bin/env python3
"""Check pinned theorem adapters; --remote additionally requires exact live refs."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
COMPONENTS={'A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','D1'}

def require(ok:bool,message:str)->None:
    if not ok:raise ValueError(message)

def check_heads(contract:dict,observed:dict)->None:
    for branch,expected in contract['watched_refs'].items():
        require(observed.get(branch)==expected,'Stale or unavailable dependency ref: '+branch)

def validate(contract:dict)->dict:
    rows=contract['components'];require({r['component'] for r in rows}==COMPONENTS and len(rows)==11,'Expected exactly eleven unique components')
    labels=set()
    for path in (REPO/'papers').rglob('*.tex'):
        labels.update(re.findall(r'\\label\{([^}]+)\}',path.read_text(errors='replace')))
    for row in rows:
        require(row['status'] in {'verified_protocol_adapter','conditional_interface_only','independent_not_consumed'},'Unknown dependency status')
        for key in ['hypotheses','transported_quantity','remaining_model_specific_work','historical_source']:
            require(bool(row[key]),'Missing contract field '+key)
        require(row['historical_gate_used_as_premise'] is False,'Historical gate imported without a new proof')
        require(set(row['gtf_theorem_labels'])<=labels,'Unknown GTF theorem label in '+row['component'])
        if row['status']=='verified_protocol_adapter':
            require(row['adapter_label'] in labels,'Missing adapter statement for '+row['component'])
            require(bool(row.get('protocol_source',{}).get('commit')),'Missing protocol source commit')
    a2=next(r for r in rows if r['component']=='A2');src=a2['protocol_source']
    data=(HERE/src['retained_copy']).read_bytes()
    require(hashlib.sha256(data).hexdigest()==src['sha256'],'A2 protocol byte identity changed')
    require(hashlib.sha1(('blob %d\0'%len(data)).encode()+data).hexdigest()==src['git_blob'],'A2 protocol Git blob mismatch')
    require(a2['primary_chain']['verified_gtf_dependency'] is False,'Independent A2 primary chain falsely marked dependent')
    check_heads(contract,contract['watched_refs'])
    bad=dict(contract['watched_refs']);bad[next(iter(bad))]='0'*40
    try:check_heads(contract,bad)
    except ValueError:pass
    else:raise ValueError('Moved-ref negative control survived')
    return {'status':'passed','components':len(rows),'verified_protocol_adapters':2,'historical_model_gates_imported':0,'a2_protocol_blob_checked':True,'moved_ref_negative_control':'rejected','live_heads_checked':False}

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--remote',action='store_true',help='Check watched branch HEADs through git; network/authentication errors fail');args=ap.parse_args()
    try:
        contract=json.loads((HERE/'PIPELINE_DEPENDENCIES.json').read_text());result=validate(contract)
        if args.remote:
            observed={}
            for branch in contract['watched_refs']:
                p=subprocess.run(['git','ls-remote','--exit-code','--heads','https://github.com/TrillionniumFoundation/theta-theory.git','refs/heads/'+branch],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
                require(p.returncode==0 and bool(p.stdout.strip()),'Remote dependency check unavailable: '+p.stderr.strip())
                observed[branch]=p.stdout.split()[0]
            check_heads(contract,observed);result['live_heads_checked']=True
        result['scope']='Identity/declaration consistency only; not proof of hypotheses or discovery of every future newly named branch.'
        print(json.dumps(result,indent=2));return 0
    except (ValueError,KeyError,OSError,subprocess.TimeoutExpired) as exc:
        print('FAILED: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
