#!/usr/bin/env python3
"""Preservation and finite controls for the conditional real-observation inverse.

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
from materialize_revision_v60 import P, ARCHIVE, CHANGES, NEW, revised, dependency_map
from materialize_revision_v57 import BLOCK, REF, DEPENDENCY, APPLICATION
from check_revision_v57 import references_by_unit, validate_roles
from check_revision_v58 import block_controls


def preservation()->dict:
    baseline=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:i for g in baseline.values() for n,i in g.items()}
    require(len(old)==122,'Unexpected baseline union')
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
    require(added=={'proposition':1,'lemma':1,'theorem':1,'proof':3},'Unexpected new blocks')
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
    require(len(union)==123,'Unexpected active union')
    return {'inherited_active_sources':len(old),'byte_identical_in_place':len(old)-len(CHANGES),
        'archived_amended_inputs':list(CHANGES),'active_sources':len(union),
        'inherited_statement_proof_blocks':total,'verbatim_blocks':total,
        'inherited_inventory':dict(sorted(counts.items())),'added_inventory':dict(sorted(added.items())),
        'entry_counts':ec,'entry_label_counts':labels_count,
        'scope':'Per source path; includes shared display copies, not a census of independent theorems.'}


def dependencies()->dict:
    declared=json.loads((P/'journal/DEPENDENCY_MAP_V60.json').read_text())
    require(declared==dependency_map(),'Current dependency declaration differs')
    roles=declared['external_reference_roles'];units={}
    for name in graph(P,'rigidity.tex'):units.update(references_by_unit((P/name).read_text()))
    validate_roles(units,roles);require(DEPENDENCY in units[APPLICATION],'Acquisition input lost')
    return {'external_reference_roles':roles,'occurrences':len(declared['occurrences']),
        'new_local_real_data_proof_external_full_theorem_inputs':[],
        'scope':'Reading-derived roles checked against syntax, not a semantic proof certificate.'}


def real_observation_controls()->dict:
    import sympy as sy
    from check_revision_v59 import analytic_tail_controls, finite_nonlinear_envelope
    z,u,v,d=sy.symbols('z u v d')
    S=lambda x: sy.Rational(3,5)*x*x+sy.Rational(1,7)*x**3+sy.Rational(1,11)*x**4
    U=lambda x: sy.Integer(1)+x/sy.Integer(5)
    V=lambda x: sy.Integer(1)-x/sy.Integer(7)
    f=lambda x,y: U(x)*V(y)*(d-S(x)-S(y))/sy.Integer(3)
    ratio=sy.cancel(f(u,v)*f(0,0)/(f(u,0)*f(0,v)))
    t=lambda x:S(x)/(d-S(x))
    require(sy.cancel(1-ratio-t(u)*t(v))==0,'Separate-factor identity')
    anchor=sy.Rational(1,32)
    recovered_t=sy.cancel((1-ratio.subs(v,anchor))/t(anchor))
    require(sy.cancel(d*recovered_t/(1+recovered_t)-S(u))==0,'Real action extraction')
    require(sy.diff(S(u),u,3).subs(u,0)!=0,'No odd coefficient in fixture')
    # A genuine finite-dimensional obstruction survives even though the high tail is small.
    rho=F(1,3); W=F(27); m=7
    require(W*rho**m/(1-rho**m)<1,'Resonance fixture tail not small')
    require(sy.expand(z**3-27*(z/3)**3)==0,'Resonant low block not detected')
    # An invertible multiplier is also necessary in the stated criterion.
    require(sy.expand((z*(1+z)).subs(z,0))==0,'Multiplier zero negative control')
    # Exact monomial checks of the interpolation bound with a common outer bound one.
    s,r,rc=F(1,16),F(1,4),F(3,4)
    A=2*(r+s)/s; b=(r+s)/(rc-s); C=rc/(rc-r)
    require(r+2*s<rc and A==10 and b==F(5,11),'Propagation radii')
    rows=[]
    theta=math.log(1/float(b))/math.log(float(A/b))
    for degree in range(3,81):
        eps=s**degree
        n=max(1,math.ceil(degree*math.log(1/float(s))/math.log(float(A/b))))
        bound=eps*A**(n-1)+C*b**n
        require(r**degree<=bound,'Interpolation majorant for degree '+str(degree))
        rows.append({'degree':degree,'interpolation_nodes':n})
    # Each omitted hypothesis fails on elementary analytic or real functions.
    require((r/s)**20>10**10,'Unbounded analytic class negative control')
    require(F(1)>100*s**20,'No same-disc continuity from real trace')
    require(theta<math.log(1/float(r))/math.log(1/float(s)),
            'Exponent inconsistent with monomial topology check')
    h=sy.symbols('h',positive=True)
    x,y=sy.symbols('x y',real=True)
    bump=4*sy.integrate(sy.integrate(h*(1-x/h)*(1-y/h),(x,0,h)),(y,0,h))
    require(sy.simplify(bump-h**3)==0,'Two-dimensional Lipschitz exponent')
    require(F(1)>100*F(1,10**12)**F(1,3),'Missing density regularity negative control')
    return {'separate_recording_cancellation_and_odd_action':True,
        'propagation_constants':{'A':str(A),'b':str(b),'theta':theta,'remainder_prefactor':str(C)},
        'exact_monomial_cases':rows,'resonant_low_block_with_small_tail':True,
        'fixed_Lipschitz_tent_mass':'h^3',
        'negative_controls':['singular low block','vanishing initial multiplier',
          'omitted analytic bound','omitted radius loss','omitted real Lipschitz bound'],
        'retained_analytic_operator_controls':analytic_tail_controls(),
        'retained_finite_stationary_envelope':finite_nonlinear_envelope(),
        'scope':'Finite algebra, interpolation and stationary-chain controls; not an infinite-dimensional proof certificate.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'dependency_roles':dependencies(),
        'real_observation_controls':real_observation_controls(),
        'retained_uniform_block_controls':block_controls()},indent=2,sort_keys=True))
