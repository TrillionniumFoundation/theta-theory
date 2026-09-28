#!/usr/bin/env python3
"""Source preservation and exact finite controls for the A2 v50 revision.

The all-lattice and infinite-flight arguments are in the manuscript. These
controls verify displayed identities, not an arbitrary billiard inverse.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from materialize_revision_v50 import P,ARCHIVE,CHANGES,NEW_INPUTS,revised
from source_provenance import require,blob_id,graph
from check_revision_v49 import new_controls as v49_controls
from check_revision_v48 import differential_controls as v48_controls
from check_revision_v47 import finite_diagnostics as v47_controls

ENV=re.compile(r'\\begin\{(structuraltheorem|theorem|lemma|proposition|corollary|definition|remark|proof)\}')
BLOCK=re.compile(r'\\begin\{(structuraltheorem|theorem|lemma|proposition|corollary|definition|remark|proof)\}.*?\\end\{\1\}',re.S)


def preservation() -> dict:
    groups=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==106,'Wrong baseline count')
    before=Counter();oldlabels=set();oldmain='';retained_blocks=0
    for name,info in old.items():
        raw=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256']
                and blob_id(raw)==info['git_blob'],'Baseline identity: '+name)
        text=raw.decode();before.update(ENV.findall(text))
        oldlabels.update(re.findall(r'\\label\{([^}]+)\}',text))
        current=(P/name).read_text()
        if name in CHANGES:
            require(current==revised(name,text),'Non-prescribed edit: '+name)
        for match in BLOCK.finditer(text):
            require(match.group(0) in current,'Inherited statement or proof changed: '+name)
            retained_blocks+=1
        if name=='main.tex':oldmain=text
    active=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(active==set(old)|set(NEW_INPUTS),'Omitted or unexpected active input')
    text='\n'.join((P/name).read_text() for name in sorted(active))
    additions=Counter()
    for name in NEW_INPUTS:additions.update(ENV.findall((P/name).read_text()))
    require(Counter(ENV.findall(text))==before+additions,'Inherited environment count changed')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'Lost or duplicate label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(not {r for r in refs if r not in labels and not r.startswith('TC-')},'Unresolved reference')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):
        cites.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
    require(cites<=bib,'Unresolved bibliography key')
    oldorder=re.findall(r'\\input\{([^}]+)\}',oldmain)
    main=(P/'main.tex').read_text();neworder=re.findall(r'\\input\{([^}]+)\}',main)
    require([n for n in neworder if n+'.tex' not in NEW_INPUTS]==oldorder,'Inherited input order changed')
    require(Counter(neworder)==Counter(oldorder)+Counter(n.removesuffix('.tex') for n in NEW_INPUTS),
            'Input omission or repetition')
    require(main.index(r'\input{article/01_introduction_v41}')>main.index(r'\appendix'),
            'Collected statements no longer in active appendix')
    return {'baseline_inputs':len(old),'active_inputs':len(active),
        'unchanged_in_place':len(old)-len(CHANGES),'exact_archived_edited_originals':list(CHANGES),
        'new_inputs':list(NEW_INPUTS),'inherited_order_preserved':True,
        'all_inherited_statement_and_proof_blocks_preserved_verbatim':retained_blocks,
        'inherited_environments':dict(sorted(before.items())),
        'added_environments':dict(sorted(additions.items())),
        'active_labels':len(labels),'unresolved_references_or_citations':[]}


def two_branch_controls() -> dict:
    a=s.sqrt(2)/2;R=s.Rational(101,1000);h0=s.Rational(1,10);eps=s.Rational(1,1000)
    Lp=s.Matrix([[1,a],[0,a]]);Lm=s.Matrix([[1,-a],[0,a]])
    require(h0-15*eps==s.Rational(17,200),'Curvature radius bound')
    require(s.sqrt(1-a)>2*R,'All-lattice separation margin')
    require(a-R>s.Rational(3,5),'Original-channel clearance margin')
    gaps=(1-2*(h0+eps),1-2*(h0-eps))
    require(gaps==(s.Rational(399,500),s.Rational(401,500)),'Original exact gaps')
    J=s.Matrix([[0,-1],[1,0]])
    require(J*Lp[:,1]==Lm[:,1],'Proper pair congruence')
    candidates=[s.Matrix.hstack(s.Matrix([1,0]),J**q*Lp[:,1]) for q in range(4)]
    dets=[s.simplify(L.det()) for L in candidates]
    require(dets==[a,a,-a,-a],'Four candidate determinants')
    retained=[L for L in candidates if L.det()>0]
    require(retained==[Lp,Lm] and len(retained)==2,'Positive orientation filter')
    require(len(candidates)!=len(retained),'Omitting orientation filter not detected')
    require(Lp.T*Lp==s.Matrix([[1,a],[a,1]]) and Lm.T*Lm==s.Matrix([[1,-a],[-a,1]]),
            'Marked Gram forms')
    require(Lp.T*Lp!=Lm.T*Lm,'Dropping marks would erase the required comparison')
    m,n=s.symbols('m n',integer=True)
    for L in (Lp,Lm):
        require(s.simplify(s.det(s.Matrix.hstack(L[:,0],L*s.Matrix([m,n])))-a*n)==0,
                'All-lattice first-channel perpendicular identity')
        require(s.simplify(s.det(s.Matrix.hstack(L[:,1],L*s.Matrix([m,n])))+a*m)==0,
                'All-lattice second-channel perpendicular identity')
        w=L*s.Matrix([1,1])
        require(s.simplify(s.det(s.Matrix.hstack(w,L*s.Matrix([m,n])))-a*(n-m))==0,
                'All-lattice added-channel perpendicular identity')
    lp=s.sqrt(2+s.sqrt(2));lm=s.sqrt(2-s.sqrt(2));c=a/lp
    require(s.simplify((Lp*s.Matrix([1,1])).dot(Lp*s.Matrix([1,1]))-lp**2)==0,
            'Added positive-branch length')
    require(s.simplify((Lm*s.Matrix([1,1])).dot(Lm*s.Matrix([1,1]))-lm**2)==0,
            'Added negative-branch length')
    require(lp-2*R>1 and lm+2*R<1,'Scalar gap separator')
    require(c<lm and c<lp and c<a/lm and c>2*R,'Actual-segment clearance margin')
    # Center directions of the added pairs are not normal-contact directions.
    theta=s.symbols('theta',real=True)
    h=h0+eps*s.cos(4*theta)
    slopes=[s.diff(h,theta).subs(theta,x) for x in (s.pi/8,3*s.pi/8)]
    require(slopes==[-s.Rational(1,250),s.Rational(1,250)],'Nonradial support derivative control')
    require(all(v!=0 for v in slopes),'A center-line closest-point shortcut would be invalid')
    return {'proper_symmetry_order':4,'raw_relative_assignments':4,'orientation_valid_realizations':2,
        'determinants':[str(x) for x in dets],'original_gaps':[str(x) for x in gaps],
        'curvature_radius_lower_bound':str(h0-15*eps),'marked_gram_forms_distinct':True,
        'all_lattice_determinant_identities':True,'added_channel_mark':[1,1],
        'added_center_lengths':[str(lp),str(lm)],'gap_separator_threshold':1,
        'actual_added_segment_clearance_lower_bound':str(c-2*R),
        'added_center_normal_support_derivatives':[str(x) for x in slopes],
        'negative_controls':['four unfiltered assignments are not four realizations',
          'different marked Gram forms cannot be erased','added closest segments cannot be assumed radial'],
        'scope':'Exact displayed identities and margins; the all-lattice, exact-fiber and law arguments are proved in the manuscript.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'v50_two_branch_controls':two_branch_controls(),
        'retained_v49_controls':v49_controls(),'retained_v48_controls':v48_controls(),
        'retained_v47_controls':v47_controls()},sort_keys=True,indent=2))
