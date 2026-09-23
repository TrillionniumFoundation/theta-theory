#!/usr/bin/env python3
"""Reproducible finite regressions; analytic statements are proved in the manuscript."""
from __future__ import annotations
import argparse,copy,json,sys
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
import certified_data as data

COUNT=0

def check(ok: bool,message: str)->None:
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(message)

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',default='');args=parser.parse_args();m=args.mutant
    for u in ((Q(0),Q(0)),(Q(1,10**20),Q(0)),(Q(1,3),Q(2,3)),(Q(1,17),Q(7,19))):
        for v in ((Q(0),Q(0)),(Q(1,7),Q(3,7)),(Q(1),Q(0)),(Q(0),Q(1))):
            s=sum(u);left=s*data.tv(data.normalize(u),data.normalize(v)) if s else Q(0)
            bound=sum(abs(x-y) for x,y in zip(u,v))
            if m=='zero_prefix' and sum(v)==0:bound=Q(0)
            check(left<=bound,'Weighted normalization, including zero rounded prefix')
    results=[]
    for d in (8,32,128,512):
        tree=data.finite_tree(d);rho=Q(0) if m=='omit_rationalization' else tree['rho']
        maximum=Q(0)
        for policy in product(range(2),repeat=3):
            p=data.feedback_law(tree,policy);q=data.feedback_law(tree,policy,True)
            check(sum(p)==1 and sum(q)==1,'Normalized coherent generated law')
            error=data.tv(p,q);maximum=max(error,maximum)
            check(error<=rho,'Marked feedback rationalization error')
            # An exposed independent selector with two different controllers.
            p2=data.feedback_law(tree,tuple(1-a for a in policy));q2=data.feedback_law(tree,tuple(1-a for a in policy),True)
            jointp=tuple(Q(1,3)*x for x in p)+tuple(Q(2,3)*x for x in p2)
            jointq=tuple(Q(1,3)*x for x in q)+tuple(Q(2,3)*x for x in q2)
            check(data.tv(jointp,jointq)<=rho,'Exposed-selector joint marked rationalization')
        results.append({'denominator':d,'rho':str(rho),'worst_feedback_TV':str(maximum)})
    check(results[0]['rho']!=results[-1]['rho'],'Rational refinement is actually nontrivial')
    tree=data.finite_tree(128)
    check(any(sum(tree['joint'][k])>0 and sum(tree['rounded_joint'][k])==0 for k in tree['joint']), 'Test exercises a positive but rounded-zero prefix')
    exact=data.physical_sign_certificate();checker=data.load_checker();raw=exact['input']
    if m=='drop_mark':
        # Replace the physical target table by an independent mark with the same marginals.
        for ai in range(2):
            for mask in range(16):raw['tests'][16*ai+mask]['terms'][0][0]=str(Q(mask.bit_count(),4))
        problem=checker.Problem.load(raw);certificate=checker.make_certificate(problem,2)
        check(Q(certificate['lower'])==Q(1,4),'Actual mark cannot be replaced by an independent copy')
    else:
        check(Q(exact['certificate']['lower'])==Q(1,4),'Exact physical sign lower certificate')
        check(Q(exact['certificate']['upper'])==Q(1,4),'Exact physical sign upper witness')
    problem=checker.Problem.load(exact['input'])
    if m=='false_lower':
        bad=copy.deepcopy(exact['certificate']);bad['lower']='1/3'
        # A faulty producer asserts a false bound; the independent checker must reject it.
        checker.check_certificate(problem,bad)
        raise ValueError('designated mutant survived')
    bad=copy.deepcopy(exact['certificate']);bad['cells']=bad['cells'][1:]
    try:checker.check_certificate(problem,bad)
    except ValueError:check(True,'Independent checker rejects missing cell')
    else:check(False,'Missing certificate cell was accepted')
    gram=data.bump_gram();r=Q(0) if m=='wrong_gram' else Q(gram['R'])
    check(r==4*Q(gram['I1'])/(Q(1,4)**2*Q(gram['I0'])),'Nonzero microscopic Gram residual')
    check(Q(gram['alpha_squared_upper'])<Q(gram['alpha_upper'])**2,'Rational physical error bound')
    # Packing lower-bound identity on explicit random channels, no floating tolerance.
    features=((Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)));n=3;dim=2;K=2
    for first in product(range(5),repeat=n):
        rows=tuple((Q(i,4),1-Q(i,4)) for i in first)
        variance=Q(0);purity=Q(0)
        for symbol in range(K):
            mass=sum(rows[h][symbol] for h in range(n))/n
            if not mass:continue
            posterior=tuple(rows[h][symbol]/(n*mass) for h in range(n))
            purity+=mass*sum(x*x for x in posterior)
            for j in range(dim):
                mean=sum(posterior[h]*features[h][j] for h in range(n))
                variance+=mass*sum(posterior[h]*(features[h][j]-mean)**2 for h in range(n))
        check(purity<=Q(K,n),'Posterior purity budget bound')
        lower=Q(1,2)*(1-Q(K,n))
        if m=='omit_half':lower=1-Q(K,n)
        check(variance>=lower,'Marked prediction packing lower bound')
    # Intrinsic witness lower-size example: fewer parameter tests leave a witness.
    for n in range(2,7):
        gamma=Q(1,2*n*(n-1));L=1-Q(1,n)-gamma
        for k in range(1,n):
            check(1-Q(1,k)<L,'Fewer-than-n identity event tests cannot certify the claimed strict lower bound')
    # A genuinely convergent enriched path family for a skew generator.
    # Cayley nodes are rational unit vectors and d_j=L(v_j+v_{j+1})/2.
    # Both endpoint residual norms are at most h/2; the integrated bound is h/2.
    last=None
    for steps in (1,2,4,8,16,32):
        h=Q(1,steps);den=1+h*h/4;c=(1-h*h/4)/den;ss=h/den
        x,y=Q(1),Q(0);bound=Q(0) if m=='omit_path_defect' else h/2
        for j in range(steps):
            xx,yy=c*x-ss*y,ss*x+c*y;dx,dy=(xx-x)/h,(yy-y)/h
            check(xx*xx+yy*yy==1,'Exact rational Cayley node norm')
            check(dx==-(y+yy)/2 and dy==(x+xx)/2,'Midpoint generator identity')
            for rx,ry in ((dx+y,dy-x),(dx+yy,dy-xx)):
                check(rx*rx+ry*ry<=bound*bound,'Enriched path endpoint residual enclosure')
            x,y=xx,yy
        if last is not None:check(bound==last/2,'Certified path residual converges geometrically')
        last=bound
    true_value=Q(1,4);finite_lower=finite_upper=Q(3,10);presentation=Q(3,50)
    lo=finite_lower-(0 if m=='false_interval' else presentation)
    hi=finite_upper+(0 if m=='false_interval' else presentation)
    check(lo<=true_value<=hi,'Same-budget interval must include presentation errors')
    if m:raise ValueError('designated mutant survived')
    evidence=Path(__file__).parent/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'EXACT_PHYSICAL_DATA.json').write_text(json.dumps(data.export_examples(),indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':COUNT,'rationalization':results,
       'physical_sign_value':'1/4','nonzero_physical_R':'192','nonzero_physical_error_upper':'1/100000',
       'scope':'Finite exact arithmetic and examples, not a semantic proof certificate or general collision integrator.'},indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError) as e:
        print('FAILED: '+str(e));sys.exit(1)
