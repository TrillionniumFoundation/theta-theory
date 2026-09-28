#!/usr/bin/env python3
"""Finite and source-structure diagnostics; not a theorem or placement certificate."""
from __future__ import annotations
import hashlib,json,re,math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def text(path): return (ROOT/path).read_text()
def expand(path,seen=None):
    seen=set() if seen is None else seen
    need(path not in seen,'Repeated input '+path);seen.add(path)
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(m[1]+('' if m[1].endswith('.tex') else '.tex'),seen),text(path))
def main():
    baseline=json.loads(text('verification/v76-baseline-preservation.json'))
    need(baseline['base_commit']=='89d5a3aa3e9f00a806d48f19f6f6831770184d76','Wrong baseline')
    need(baseline['base_tree']=='8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d','Wrong tree')
    need(len(baseline['files'])==1017,'Incomplete baseline')
    for name,spec in baseline['files'].items():
        need((ROOT/name).is_file(),'Deleted inherited path '+name)
        data=(ROOT/(spec['archive'] or name)).read_bytes()
        need(len(data)==spec['bytes'] and hashlib.sha256(data).hexdigest()==spec['sha256'],'Unpreserved '+name)
    entries={stem:expand(stem+'.tex') for stem in ('rigidity','main','two_collision')}
    active=set()
    for stem,source in entries.items():
        labs=re.findall(r'\\label\{([^}]+)\}',source)
        need(len(labs)==len(set(labs)),'Duplicate labels '+stem); active.update(labs)
    inherited=set(json.loads(text('verification/v76-inherited-labels.json')))
    need(len(inherited)==1435 and inherited<=active,'Inactive old statement')
    alias=set(re.findall(r'\\vFullAlias\{([^}]+)\}',text('journal/full_reference_routes_v75.tex')))
    plabel=set(re.findall(r'\\label\{([^}]+)\}',entries['rigidity']))
    refs=set(re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}',entries['rigidity']))
    need(refs<=plabel|alias,'Unresolved principal refs: '+repr(sorted(refs-plabel-alias)))
    bodies=[('journal/core/periodic_contact_v75.tex','journal/core/periodic_contact_v76.tex',r'\subsection{Fixed geometric marks'),('journal/core/positive_curvature_v75.tex','journal/core/positive_curvature_v76.tex','Throughout this section')]
    for old,new,marker in bodies:
        need(text(old).split(marker,1)[1]==text(new).split(marker,1)[1],'Altered inherited proof '+new)
    relative=text('journal/core/periodic_relative_v76.tex')
    old=text('article/10a_periodic_itinerary_relative_v64.tex')
    begin=r'\subsection{The geometric Jacobi operator}';end='The extension above concerns the geometric forward mechanism'
    need(old.split(begin)[1].split(end)[0]==relative.split(begin)[1].split(end)[0],'Altered relative proofs')
    for new in ('periodic_contact_v76','positive_curvature_v76','periodic_relative_v76'):
        prose=text('journal/core/'+new+'.tex')
        for stale in ('local analytic coordinate theorem of the preceding section','gives an inverse of the complete analytic action map','bounds that follow keep'):
            need(stale not in prose,'Stale principal transition')
    for stem in ('main','rigidity'):
        need('A2 revision 76;' in text(stem+'.tex'),'Stale entry version')
        for label in ('prop:v76-determinant','prop:v76-envelope','cor:v76-phase-stability','sec:v76-conditioning'):
            need('\\label{'+label+'}' in entries[stem],'New result not active '+stem+':'+label)
    # Exact heterogeneous positive Jacobi fixture, not a geometric realization.
    R=s.Rational;k=[R(1),R(1,10),R(1,5)];a=[R(9,10),R(1,5),R(2,5)]
    c=[(k[(i-1)%3]*(1/a[(i-1)%3]-1)-k[i]*(1-a[i]))/2 for i in range(3)]
    sh=[k[i]+c[i]-k[i]*a[i] for i in range(3)]
    need(all(x>0 for x in c+sh),'Nonpositive Jacobi fixture')
    for i in range(3):
        need(s.simplify(sh[i]-k[i]-c[i]+k[i]**2/(k[i]+c[(i+1)%3]+sh[(i+1)%3]))==0,'Riccati fixture')
    A=s.zeros(3);m=3;rho=s.prod(a)
    for i in range(3): A[i,(i+1)%3]=a[i]**m
    w=s.ones(3,1)
    for i in range(2):w[i+1]=rho*w[i]/a[i]**m
    K=6*A*(s.eye(3)-A).inv();theta=6*rho/(1-rho)
    need(A*w==rho*w and K*w==theta*w,'Phase weighting or orientation')
    need(theta==R(27,58) and theta<1,'Geometric mean condition')
    need((s.eye(3)-K).inv().applyfunc(lambda x: int(bool(x>=0)))==s.ones(3),'Visit inverse not positive')
    # Cauchy/Schwarz bounds are proved in text; test exact off-diagonal cancellation.
    t,x,y,d0,d1=s.symbols('t x y d0 d1',real=True)
    D=s.diag(d0,d1);E=s.Matrix([[0,x],[y,0]])
    det=(s.eye(2)+D+t*E).det();f=s.log(det)
    need(s.diff(f,t).subs(t,0)==0,'Nonzero first off-diagonal variation')
    need(s.simplify(s.diff(f,t,2).subs(t,0)+2*x*y/((1+d0)*(1+d1)))==0,'Wrong quadratic variation')
    for n in (2,4,9):
        T=s.diag(*([0]*n));T[:2,:2]=D+t*E
        need(s.simplify((s.eye(n)+T).det()-det)==0,'Padding changes determinant')
    # Scalar order table: exact rational comparisons, no rounded boundary decisions.
    table=[]
    for ar in (R(1,2),R(9,10),R(99,100)):
        order=3
        while 6*ar**order/(1-ar**order)>=1:order+=1
        target=3
        while 6*ar**target/(1-ar**target)>R(1,2):target+=1
        th=6*ar**order/(1-ar**order)
        table.append({'a':str(ar),'minimum_order':order,'half_tail_order':target,'alpha_s1':str(R(1,2*(order+1)+1)),'theta':round(float(th),9)})
    need([z['minimum_order'] for z in table]==[3,19,194],'Wrong strict order')
    need([z['half_tail_order'] for z in table]==[4,25,256],'Wrong target margin')
    h,q,dA,dB=s.symbols('h q dA dB',nonzero=True)
    Q=(1-h/dA)/(1-h/dB);H=dA*dB*(1-q)/(dB-dA*q)
    need(s.simplify(H.subs(q,Q)-h)==0,'Two-offset inverse')
    need(s.simplify(s.diff(H,q).subs(q,Q)+dA*(dB-h)**2/(dB*(dB-dA)))==0,'Two-offset conditioning')
    # Extremely small reference mass cancels symbolically before taking a limit.
    eps,c0,dN,B0,Z0=s.symbols('eps c0 dN B0 Z0',nonzero=True)
    need(s.cancel((c0*dN*B0)/(c0*dN*Z0))==B0/Z0,'Rarity normalization')
    print(json.dumps({'status':'passed','baseline_files_preserved':1017,'changed_originals_archived':['main.tex','rigidity.tex'],'inherited_active_labels':len(inherited),'current_active_labels':len(active),'principal_labels':len(plabel),'principal_external_aliases':len(alias),'unchanged_core_proof_bodies':3,'phase_fixture':{'kind':'positive Jacobi/visit algebra only; not a realized table','theta':str(theta),'weight_condition_number':str(max(w)/min(w)),'scalar_max_phase_minimum_order':19,'phase_order':3},'conditioning_table':table,'offdiagonal_and_quotient_algebra':'passed','optimization_safe':True,'scope':'Finite algebra, active references, semantic regression phrases, and byte preservation; not formal proof verification, optimality, exhaustive history audit, or journal acceptance.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
