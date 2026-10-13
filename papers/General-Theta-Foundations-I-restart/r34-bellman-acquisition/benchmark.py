#!/usr/bin/env python3
"""Executable diagnostic for Section 5.1: 61 total states, 779 thresholds.
The rational table is exact. Floating log/exp execution is a diagnostic, not
an uncharged exact arithmetic implementation; Section 8.2 supplies its contract.
"""
from __future__ import annotations
import argparse,json,math
from bisect import bisect_left
from fractions import Fraction as F

def table()->dict:
    widths=(10,20,30);phases=[];old=[F(1,2)]
    for phase,m in enumerate(widths,1):
        boundaries=[F(1,4)+F(j,2*m) for j in range(1,m)]
        rows=[]
        for q in old:
            # y_j = log(ratio_j)/2. Every stored ratio is rational and positive.
            ratios=[((b-F(1,4))/(F(3,4)-b))*(1-q)/q for b in boundaries]
            rows.append({'incoming_q':str(q),'exp_2y_thresholds':[str(r) for r in ratios]})
        centers=[F(1,4)+F(2*j-1,4*m) for j in range(1,m+1)]
        phases.append({'phase':phase,'width':m,'rows':rows,'codepoints':[str(q) for q in centers]});old=centers
    count=sum(len(r['exp_2y_thresholds']) for p in phases for r in p['rows'])
    if count!=779:raise RuntimeError('incorrect threshold inventory')
    return {'initial_label':0,'total_dynamic_labels':61,'phase_widths':[1,10,20,30],'threshold_count':count,'terminal_scalar_codepoints':30,'categorical_response':'(q,1-q)','squared_excess_upper':'1/648','checkpoint_61_upper':'1/29768','phases':phases,'arithmetic_scope':'Exact rational programme data; computing logarithms and comparing an approximated real report requires a declared precision and boundary-error certificate.'}

def execute(reports:list[float])->dict:
    if len(reports)!=3 or not all(math.isfinite(y) for y in reports):raise ValueError('exactly three finite real reports are required')
    program=table();local=0;trace=[0];offset=1
    for y,phase in zip(reports,program['phases']):
        row=phase['rows'][local];thresholds=[math.log(float(F(x)))/2 for x in row['exp_2y_thresholds']]
        local=bisect_left(thresholds,y);trace.append(offset+local);offset+=phase['width']
    q=F(program['phases'][-1]['codepoints'][local])
    return {'diagnostic_trace':trace,'terminal_q_exact':str(q),'response':[float(q),float(1-q)],'halt_after_reports':3,'free_clock':False,'warning':'The diagnostic host stores a trace only for inspection; the mathematical controller stores the single phase-labelled state. Floating report comparisons require Section 8.2 error accounting.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--reports',type=float,nargs=3);args=ap.parse_args()
    print(json.dumps(execute(args.reports) if args.reports is not None else table(),sort_keys=True,indent=2))
if __name__=='__main__':main()
