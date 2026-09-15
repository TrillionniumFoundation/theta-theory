#!/usr/bin/env python3
"""Preservation and finite controls for the complete analytic-contact inverse.

The nonlinear variational fixture solves finite stationary billiard chains.
It tests the envelope identity, not the infinite-dimensional inverse theorem.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
import re
import numpy as np
from scipy.optimize import root
from source_provenance import blob_id, graph, require
from materialize_revision_v59 import P, ARCHIVE, CHANGES, NEW, revised, dependency_map
from materialize_revision_v57 import BLOCK, REF, DEPENDENCY, APPLICATION
from check_revision_v57 import references_by_unit, validate_roles
from check_revision_v58 import block_controls


def preservation()->dict:
    baseline=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:i for g in baseline.values() for n,i in g.items()}
    require(len(old)==121,'Unexpected baseline union')
    counts=Counter(); total=0
    for name,info in old.items():
        data=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
                and blob_id(data)==info['git_blob'],'Baseline identity: '+name)
        text,current=data.decode(),(P/name).read_text()
        require(current==(revised(name,text) if name in CHANGES else text),'Unprescribed edit: '+name)
        before,after=list(BLOCK.finditer(text)),list(BLOCK.finditer(current))
        require([m.group() for m in before]==[m.group() for m in after],
                'An inherited statement/proof changed: '+name)
        counts.update(m.group(1) for m in before);total+=len(before)
        require(set(re.findall(r'\\label\{([^}]+)\}',text))<=set(re.findall(r'\\label\{([^}]+)\}',current)),
                'Inherited label removed')
    added=Counter(m.group(1) for m in BLOCK.finditer((P/NEW).read_text()))
    require(added=={'lemma':2,'theorem':1,'proof':3},'Unexpected new blocks')
    union=set(); ec={}; labels_count={}
    for entry,group in baseline.items():
        active=graph(P,entry+'.tex')
        require(active==set(group)|({NEW} if entry!='two_collision' else set()),'Entry graph: '+entry)
        union|=active; ec[entry]=len(active)
        text='\n'.join((P/n).read_text() for n in sorted(active))
        labels=re.findall(r'\\label\{([^}]+)\}',text)
        require(len(labels)==len(set(labels)),'Duplicate label: '+entry);labels_count[entry]=len(labels)
        refs=set(REF.findall(text))
        external=set(dependency_map()['external_reference_roles']) if entry=='rigidity' else set()
        if entry=='main':external|={r for r in refs if r.startswith('TC-')}
        require(refs<=set(labels)|external,'Unresolved labels: '+str(refs-set(labels)-external))
        cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in c.split(',')}
        bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
        require(cites<=bib,'Missing citation: '+str(cites-bib))
    require(len(union)==122,'Unexpected active union')
    return {'inherited_active_sources':len(old),'byte_identical_in_place':len(old)-len(CHANGES),
        'archived_amended_inputs':list(CHANGES),'active_sources':len(union),
        'inherited_statement_proof_blocks':total,'verbatim_blocks':total,
        'inherited_inventory':dict(sorted(counts.items())),'added_inventory':dict(sorted(added.items())),
        'entry_counts':ec,'entry_label_counts':labels_count,
        'scope':'Per source path; includes shared display copies, not a census of independent theorems.'}


def dependencies()->dict:
    declared=json.loads((P/'journal/DEPENDENCY_MAP_V59.json').read_text())
    require(declared==dependency_map(),'Current dependency declaration differs')
    roles=declared['external_reference_roles'];units={}
    for name in graph(P,'rigidity.tex'):units.update(references_by_unit((P/name).read_text()))
    validate_roles(units,roles);require(DEPENDENCY in units[APPLICATION],'Acquisition input lost')
    return {'external_reference_roles':roles,'occurrences':len(declared['occurrences']),
        'new_analytic_proof_external_full_theorem_inputs':[],
        'scope':'Reading-derived roles checked against syntax, not a semantic proof certificate.'}


def analytic_tail_controls()->dict:
    rows=[]
    for rho in (F(1,3),F(3,5),F(9,10),F(99,100)):
        # W=2 and a*=1/2 are deliberately loose valid operator-model constants.
        m=4
        while 8*rho**m/(1-rho**m)>=F(1,2):m+=1
        q=8*rho**m/(1-rho**m)
        require(q<F(1,2),'Tail contraction')
        require(2/(1-q)<4,'Tail inverse bound')
        # Exact finite sums sit below the infinite visit bound.
        partial=sum(rho**(i*m) for i in range(1,11))
        require(partial<=rho**m/(1-rho**m),'Visit sum')
        rows.append({'rho':str(rho),'chosen_tail_order':m,'q':float(q)})
    # A synthetic analytic weighted-composition operator with a nonzero lower part.
    # Truncated polynomial arithmetic is exact. This fixture is not a billiard action.
    import sympy as s
    z=s.symbols('z'); N=9; alpha=1+z/8; f=z/3+z*z/24
    L=s.zeros(N-2)
    for j,n in enumerate(range(3,N+1)):
        poly=s.Poly(s.expand(alpha*z**n+2*f**n),z)
        for i,k in enumerate(range(3,N+1)):L[i,j]=poly.coeff_monomial(z**k)
    require(any(L[i,j]!=0 for i in range(N-2) for j in range(i)),'Fixture has no lower coupling')
    require(L.det()!=0,'Finite analytic quotient not invertible')
    require(L.inv()*L==s.eye(N-2),'Finite quotient inverse')
    diagonal=s.diag(*L.diagonal())
    require(diagonal.inv()*L!=s.eye(N-2),'Omitted lower-coupling control failed')
    # Schwarz tail estimate is false without the stipulated vanishing order.
    require(F(1)>F(1,2)**6,'Missing-vanishing negative control')
    # Complex-disc smallness cannot be inferred from small real-interval size.
    T=s.chebyshevt(12,z)
    require(abs(complex(T.subs(z,s.I)))>1000,'Strong-topology distinction control')
    return {'tail_choices':rows,'nonlinear_composition_quotient_orders':[3,N],
        'negative_controls':['omitted lower coupling','missing high-order vanishing','real interval is not complex-disc norm'],
        'scope':'Exact finite analytic operator fixtures; no claim of a general Banach-space numerical certificate.'}


def chain_data(y: np.ndarray,u: float,N: int,eps: float):
    x=np.r_[u,y,0.0]; types=np.arange(N+1)%2
    kap=np.array([1.2,2.3])[types]; cubic=np.array([.16,-.11])[types]
    quartic=np.array([.08,.05])[types]; ec=np.array([.7,-.4])[types]; eq=np.array([.2,.3])[types]
    c=cubic+eps*ec; q=quartic+eps*eq
    psi=kap*x*x/2+c*x**3+q*x**4
    dp=kap*x+3*c*x*x+4*q*x**3
    dd=kap+6*c*x+12*q*x*x
    h=1+psi[:-1]+psi[1:]; diff=x[:-1]-x[1:]; length=np.sqrt(h*h+diff*diff)
    nl=h*dp[:-1]+diff; nr=h*dp[1:]-diff
    grad=nr[:-1]/length[:-1]+nl[1:]/length[1:]
    left=(dp[:-1]**2+h*dd[:-1]+1)/length-nl*nl/length**3
    right=(dp[1:]**2+h*dd[1:]+1)/length-nr*nr/length**3
    cross=(dp[:-1]*dp[1:]-1)/length-nl*nr/length**3
    Hess=np.diag(right[:-1]+left[1:])+np.diag(cross[1:-1],1)+np.diag(cross[1:-1],-1)
    action=math.fsum(float(a-1) for a in length)
    eta=ec*x**3+eq*x**4; w=h/length
    envelope=math.fsum(float(v) for v in w*(eta[:-1]+eta[1:]))
    return action,grad,Hess,envelope,float(w[0]*eta[0]),x


def finite_nonlinear_envelope()->dict:
    rows=[]; max_residual=0.; max_error=0.
    c=math.sqrt(2.2*3.3); t=math.exp(-math.acosh(c)); lam=math.sqrt(2.2/3.3)*t
    for N in (8,16,24):
        for u in (-.055,.035,.065):
            initial=np.array([u*(t**i if i%2==0 else lam*t**(i-1)) for i in range(1,N)])
            def solve(eps):
                res=root(lambda y:chain_data(y,u,N,eps)[1],initial,
                         jac=lambda y:chain_data(y,u,N,eps)[2],tol=1e-12)
                vals=chain_data(res.x,u,N,eps)
                require(np.max(np.abs(vals[1]))<5e-13,'Stationarity residual')
                return vals
            a=solve(0.); step=1e-4; plus=solve(step); minus=solve(-step)
            difference=(plus[0]-minus[0])/(2*step)
            err=abs(difference-a[3]); max_error=max(max_error,err)
            max_residual=max(max_residual,float(np.max(np.abs(a[1]))))
            require(err<2e-9,'Finite envelope/finite-difference mismatch')
            require(abs(a[4])>1e-5 and abs(difference-(a[3]+a[4]))>1e-5,
                    'Doubled endpoint visit not detected')
            require(np.all(np.linalg.eigvalsh(a[2])>0),'Nonconvex stationary-chain Hessian')
            require(np.all(np.abs(a[5][1:])<=.6**np.arange(1,N+1)*abs(u)),
                    'Fixture does not have contracted visits')
            rows.append({'flights':N,'endpoint':u,'envelope_derivative':float(a[3]),
                         'central_difference_error':err})
    return {'cases':rows,'maximum_stationarity_residual':max_residual,
        'maximum_envelope_error':max_error,
        'negative_control':'double initial visit',
        'scope':'Finite stationary chains for actual polynomial reflecting graphs; no infinite-flight or global-periodic certificate.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'dependency_roles':dependencies(),
        'analytic_operator_controls':analytic_tail_controls(),
        'finite_nonlinear_envelope':finite_nonlinear_envelope(),
        'retained_uniform_block_controls':block_controls()},indent=2,sort_keys=True))
