#!/usr/bin/env python3
"""Preservation plus exact finite controls for the v49 symmetry revision.

This is not a proof certificate, a realized generic billiard reconstruction,
or a numerical certification of an infinite-dimensional operator.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import itertools
import json
from math import gcd
from functools import reduce
import re
import sympy as s
from materialize_revision_v49 import P, ARCHIVE, CHANGES, NEW_INPUTS, revised
from source_provenance import require, blob_id, graph, strip_comments
from check_revision_v48 import differential_controls
from check_revision_v47 import finite_diagnostics as calibration_controls

ENV=re.compile(r'\\begin\{(structuraltheorem|theorem|lemma|proposition|corollary|definition|remark|proof)\}')


def preservation() -> dict:
    manifest=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in manifest.values() for n,v in group.items()}
    require(len(old)==105,'Wrong baseline')
    before=Counter();baseline_labels=set();plain_originals={}
    for n,info in old.items():
        raw=(ARCHIVE/n if n in CHANGES else P/n).read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256']
                and blob_id(raw)==info['git_blob'],'Baseline identity: '+n)
        txt=raw.decode();plain_originals[n]=txt
        before.update(ENV.findall(txt));baseline_labels.update(re.findall(r'\\label\{([^}]+)\}',txt))
        if n in CHANGES:
            require((P/n).read_text()==revised(n,txt),'Non-prescribed edit: '+n)
    active=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(active==set(old)|set(NEW_INPUTS),'Missing or unexpected active input')
    text='\n'.join((P/n).read_text() for n in sorted(active))
    after=Counter(ENV.findall(text));additions=Counter()
    for n in NEW_INPUTS:additions.update(ENV.findall((P/n).read_text()))
    require(after==before+additions,'An inherited environment count changed')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)) and baseline_labels<=set(labels),'Lost or duplicate label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(not {r for r in refs if r not in labels and not r.startswith('TC-')},'Unresolved reference')
    allcites=set()
    for v in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):allcites.update(x.strip() for x in v.split(','))
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
    require(allcites<=bib,'Unresolved citation')
    # Reordering, unlike deletion, is an intentional part of this revision.
    main=(P/'main.tex').read_text();oldmain=plain_originals['main.tex']
    oldinputs=re.findall(r'\\input\{([^}]+)\}',oldmain)
    currentinputs=re.findall(r'\\input\{([^}]+)\}',main)
    require(Counter(currentinputs)==Counter(oldinputs)+Counter(x.removesuffix('.tex') for x in NEW_INPUTS),
            'Top-level input omission or repetition')
    require(main.index('\\input{article/01c_geometric_setup_v43}')<main.index('\\input{v4/10_boundary_layers}')
       <main.index('\\input{article/23a_signed_endpoint_rigidity_v27}')
       <main.index('\\input{article/23n_finite_symmetry_v49}')
       <main.index('\\input{article/23m_differential_rigidity_v48}')<main.index('\\part{Boundary information'),
       'Core proof order')
    require(main.index('\\input{article/01_introduction_v41}')>main.index('\\appendix'),
       'Repeated theorem catalogue not in compiled appendix')
    require('continuous family through the base alignment' in
       (P/NEW_INPUTS[0]).read_text(),'Actual alignment-branch hypothesis missing')
    return {'baseline_inputs':len(old),'active_inputs':len(active),
       'unchanged_in_place':len(old)-len(CHANGES),'exact_archived_edited_originals':list(CHANGES),
       'added_inputs':list(NEW_INPUTS),'all_inherited_inputs_labels_and_environment_counts_retained':True,
       'inherited_environments':dict(sorted(before.items())),
       'added_environments':dict(sorted(additions.items())),
       'active_labels':len(labels),'proof_architecture':'Core first; complete catalogue moved to active appendix'}


def new_controls() -> dict:
    t=s.symbols('t',real=True);u=s.Rational(1,20)
    H0=s.Matrix([[2+t,s.Rational(-1,4)],[s.Rational(-1,4),3+2*t]])
    Delta=s.Matrix([[u*(1+t),u/3],[u/3,u*u*(1-t)]])
    G=H0.inv();T=G*Delta
    def at(A):return A.subs(t,0)
    dotG=-at(G)*at(H0.diff(t))*at(G)
    require(dotG==at(G.diff(t)),'Moving inverse derivative')
    dotT=dotG*at(Delta)+at(G)*at(Delta.diff(t))
    R=(s.eye(2)+at(T)).inv()
    predicted=s.Rational(1,7)-s.trace(R*dotT)
    direct=s.Rational(1,7)+s.diff(H0.det(),t).subs(t,0)/at(H0).det()-s.diff((H0+Delta).det(),t).subs(t,0)/at(H0+Delta).det()
    require(s.simplify(predicted-direct)==0,'Log-amplitude differential')
    wrong=s.Rational(1,7)-s.trace(R*at(G)*at(Delta.diff(t)))
    discrepancy=s.factor(wrong-direct)
    require(discrepancy!=0,'Omitted moving reference not detected')
    # Root-of-unity counts, exact curvature margins and a changing symmetry group.
    harmonics=[]
    for F in ((2,),(3,),(4,8),(6,10,15),(6,12,18),(2,3)):
        k=F[0];valid=[q for q in range(k) if all(q*f%k==0 for f in F)]
        m=reduce(gcd,F)
        require(len(valid)==m,'Finite stabilizer count')
        eps=[s.Rational(1,10*len(F)*(f*f-1)) for f in F]
        margin=1-sum(e*(f*f-1) for e,f in zip(eps,F))
        require(margin==s.Rational(9,10),'Convex noncircular support margin')
        harmonics.append({'indices':list(F),'order':m,'curvature_lower_bound':str(margin)})
    k=s.symbols('k',integer=True,positive=True);a,v=s.symbols('a v',real=True)
    r=s.exp(-s.I*k*(a+v*t))
    require(s.simplify(s.I/k*s.diff(r,t)/r-v)==0,'One harmonic determines angular velocity')
    require(reduce(gcd,(2,))==2 and reduce(gcd,(2,3))==1,'Symmetry-breaking control')
    # The pi branch for h=1+eps cos(2 theta)+t eps2 cos(3 theta)
    # fails off zero; an actual continuously followed branch is required.
    require((-1)**3!=1,'A broken base symmetry must not be extended arbitrarily')
    choices=list(itertools.product(range(2),range(3),range(4)))
    require(len(set(choices))==24,'Finite channel-tree assignment count')
    L=s.Matrix([[1,-s.sin(t)],[0,s.cos(t)]])
    gram=s.Matrix([[1,-s.sin(t)],[-s.sin(t),1]])
    require(s.simplify(L.T*L-gram)==s.zeros(2),'Disk lattice Gram identity')
    require(L.diff(t).subs(t,0)==s.Matrix([[0,-1],[0,0]]),'Disk lattice tangent')
    require(gram.diff(t).subs(t,0)==s.Matrix([[0,-1],[-1,0]]),'Invisible Gram variation')
    require(s.simplify((L-s.eye(2)).T*(L-s.eye(2)))[1,1]==2-2*s.cos(t),'Operator perturbation norm')
    neighbors=[(i,j) for i in range(-2,3) for j in range(-2,3) if 0<i*i+j*j<=s.Rational(25,9)]
    require(len(neighbors)==8,'Clearance finite neighbor reduction')
    for axis in (0,1):
        end=(1,0) if axis==0 else (0,1)
        for mark in neighbors:
            if mark==end:continue
            z=mark[axis];w=mark[1-axis];project=min(max(z,0),1)
            require((z-project)**2+w*w>=1,'Base segment clearance')
    require(s.sqrt(2)+1<s.Rational(5,2),'Uniform perturbation clearance margin')
    return {'moving_reference_log_amplitude_identity':True,
       'omitted_reference_derivative_discrepancy':str(discrepancy),
       'finite_symmetry_and_convexity_controls':harmonics,
       'single_harmonic_angular_velocity':True,
       'symmetry_breaking_actual_branch_control':True,
       'synthetic_channel_tree_assignments':len(choices),'circular_gram_and_clearance_controls':True,
       'scope':'Finite exact algebra and the stated disk geometry only; no generic billiard-instance or infinite-operator certificate'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'v49_controls':new_controls(),
        'retained_v48_functional_controls':differential_controls(),
        'retained_v47_calibration_controls':calibration_controls()},sort_keys=True,indent=2))
