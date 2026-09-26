#!/usr/bin/env python3
"""Exact regression checks for the written v171 proofs; not proof certificates."""
from __future__ import annotations
import argparse, hashlib, json, math, platform, subprocess, sys, time
from pathlib import Path
from itertools import product
import sympy as S
HERE=Path(__file__).resolve().parent
PARTS=['duality-base-change-v171.tex','self-contained-chain-v171.tex',
       'tangent-covers-v171.tex','diagonal-proof-completion-v171.tex']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def tangent_valuations():
    cases=0
    for r,s,i in product(range(2,14),range(2,14),range(1,35)):
        if i<=r:
            g=math.gcd(r*s,i);alpha,beta,e,f=s*i//g,i//g,r*s//g,g
            k=((r*s-1)*i-r*s)//g+1
        else:
            g=math.gcd(r,i*s);alpha,beta,e,f=i*s//g,r//g,r*s//g,g
            k=((r-1)*i*s-r)//g+1
        assert r*alpha==i*e and e*f==r*s
        assert k==(r-1)*alpha+(s-1)*beta-e+1 and k>=0
        assert (f*k)%2==0
        raw_disc=(r-1)*i*s+(s-1)*min(i,r)
        assert raw_disc-(r*s-g)==f*k
        if i<r:assert s*beta==alpha<e
        if i==r:assert (alpha,beta,e,f)==(s,1,s,r)
        if i>r:assert alpha>e==s*beta
        cases+=1
    return {'cases':cases,'identities_and_parity_passed':True}

def exact_discriminants():
    v,t,w=S.symbols('v t w');records=[]
    for r,s,i in product(range(2,4),range(2,4),range(1,7)):
        polynomial=(t-v**s)**r-w*t**i
        disc=S.Poly(S.discriminant(polynomial,v),t)
        order=min(m[0] for m,c in disc.terms() if c!=0)
        expected=(r-1)*i*s+(s-1)*min(i,r)
        assert order==expected,(r,s,i,order,expected)
        records.append({'r':r,'s':s,'i':i,'discriminant_order':order})
    return {'method':'Exact resultant/discriminant over Q[t,w], not numerical roots',
            'records':records,'passed':True}

def square_trace_lattice():
    e,h=S.symbols('e h')
    mz=S.Matrix([[0,h,0,0],[1,0,0,0],[0,0,0,h],[0,0,1,0]])
    mv=S.Matrix([[0,0,e*h,-e*h],[0,0,-e,e*h],[1,0,0,0],[0,1,0,0]])
    one=S.eye(4)
    assert mz*mz==h*one and mv*mv==e*(h*one-mz) and mz*mv==mv*mz
    mats=[one,mz,mv,mz*mv]
    gram=S.Matrix(4,4,lambda i,j:S.trace(mats[i]*mats[j]))
    discB=S.factor(gram.det());incl=S.diag(1,e,1,e)
    discA=S.factor((incl.T*gram*incl).det())
    normJac=S.factor((4*e*mz*mv).det())
    assert S.simplify(discA-e**4*discB)==0 and discA==normJac
    assert discB==256*e**2*h**3*(h-1)
    # (A:B)=eB: e times each normal basis vector is in the A lattice,
    # and closure under multiplication by z forces all four coefficients divisible by e.
    assert all(not S.denom(x).has(e) for x in incl.inv()*(e*one))
    A,B,C,D=S.symbols('A B C D')
    coeff=S.Matrix([A,e*B,C,e*D])
    product_z=incl.inv()*mz*coeff
    assert product_z[1]==A/e and product_z[3]==C/e
    return {'normal_basis':['1','z','v','zv'],'raw_basis':['1','ez','v','ezv'],
            'normal_trace_discriminant':str(discB),'raw_trace_discriminant':str(discA),
            'jacobian_norm':str(normJac),'inclusion_determinant':str(incl.det()),
            'ordinary_conductor':'e B_1','passed':True}

def square_charts_and_arcs():
    e,z,v,c,q,u,k,t=S.symbols('e z v c q u k t')
    F1=v*v-e*z*(z-1);F2=v*v-c*(1-q)
    assert S.factor(F2.subs({c:e*z*z,q:1/z})-F1)==0
    assert S.factor((u+v*v-u*u*k).subs({u:e*z,k:1/e})-F1)==0
    singular=S.solve([F1,S.diff(F1,e),S.diff(F1,z),S.diff(F1,v)],(e,z,v),dict=True)
    assert len(singular)==2 and {x[z] for x in singular}=={0,1}
    g=S.groebner([F1,e*z,v],v,e,z)
    assert list(g.polys)[0].as_expr()==v and g.reduce(e*z)[1]==0
    h=S.groebner([F2,c*q,v],v,c,q)
    assert h.reduce(c)[1]==0
    for sub in ({z:-1,v:t,e:t*t/2},{z:1+t,v:t,e:t/(1+t)}):
        assert S.factor(F1.subs(sub))==0
        uu=S.factor((e*z).subs(sub));cc=S.factor((e*z*z).subs(sub))
        assert uu!=0 and S.factor(cc-uu-t*t)==0
        assert S.limit(uu*uu/(cc*cc),t,0)==1
    for j in range(2,18):
        Hj=1-v**(j-2)*q
        cc=v*v/Hj;uu=cc*v**(j-2)*q;ww=q*q*Hj**(j-2)
        assert S.factor(cc-uu-v*v)==0 and S.factor(ww-uu*uu/cc**j)==0
        Hn=1-v**(j-1)*q
        assert S.factor(cc.subs(q,v*q)-v*v/Hn)==0
        assert S.factor((ww/cc).subs(q,v*q)-q*q*Hn**(j-1))==0
    return {'singular_middle_points':[{'e':0,'z':0,'v':0},{'e':0,'z':1,'v':0}],
            'node_ring':'k[e,z]/(ez)','last_fibre_ring':'k[q]',
            'normal_overlap_identities':True,'two_actual_arcs_verified':True,
            'endpoint_induction_checked_through':18,'passed':True}

def unequal_conductor():
    # A=k[(3,0),(2,1),(0,3)] inside B=third Veronese.
    bound=90;A={(3*i+2*j,j+3*k) for i in range(31) for j in range(31) for k in range(31)}
    points=0
    for x,y in product(range(31),repeat=2):
        if (x+y)%3:continue
        # B=A+Aw with w=(1,2); this is exact by w^2=v theta.
        actual=(x,y) in A and (x+1,y+2) in A
        predicted=x>=2 # exceptional valuation in cover coordinates equals x.
        assert actual==predicted,(x,y,actual,predicted)
        points+=1
    return {'normal_ring':'third Veronese','ordinary_conductor':'(u,v)B',
            'fibre_ring':'k[w,theta]/(w^2)','monomials_checked':points,'passed':True}

def diagonal_identity():
    checks=0
    for r,s,i in product(range(1,13),range(1,13),range(1,20)):
        g=math.gcd(r,i*s);A=i*s//g;B=r//g;e=r*s//g
        assert (r-1)*A+(s-1)*B-e+1==(r*i*s-r-i*s)//g+1
        checks+=1
    return {'recovery_of_all_diagonal_orders':checks,'passed':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true')
    args=ap.parse_args();start=time.monotonic();inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v170/check_v170.py')],check=True,
                       stdout=(HERE/'inherited-v170-command.log').open('w'),stderr=subprocess.STDOUT)
        data=json.loads((HERE.parent/'v170/EXACT_CHECKS_V170.json').read_text())
        assert data['all_checks_pass'] and data['inherited_v169_full_chain_rerun']
        (HERE/'INHERITED_V170_CHECKS_RERUN.json').write_text(json.dumps(data,indent=2)+'\n')
        inherited=True
    report={'revision':171,'python':platform.python_version(),'sympy':S.__version__,
            'auxiliary_only':True,'all_checks_pass':True,
            'inherited_v170_full_chain_rerun':inherited,
            'tangent_valuation_identities':tangent_valuations(),
            'exact_discriminants':exact_discriminants(),
            'trace_lattice':square_trace_lattice(),
            'square_normalizations_fibres_and_arcs':square_charts_and_arcs(),
            'unequal_conductor_chart':unequal_conductor(),
            'diagonal_recovery':diagonal_identity(),
            'source_sha256':{n:sha(HERE/n) for n in PARTS},
            'duration_seconds':round(time.monotonic()-start,3)}
    (HERE/'EXACT_CHECKS_V171.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'inherited':inherited,'seconds':report['duration_seconds']},indent=2))
if __name__=='__main__':main()
