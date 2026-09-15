#!/usr/bin/env python3
"""v55 retention and exact finite probability controls; not theorem certification."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
import re
from materialize_revision_v55 import (P, ARCHIVE, CHANGES, MODULE, revised,
                                     waiting_blocks, ADDED_ITEMS, ADDED_PROOF)
from source_provenance import require, blob_id, graph
from check_revision_v50 import ENV, BLOCK
from check_revision_v54 import (finite_controls as v54_controls, small_window_controls,
 window_controls, v51_controls, two_branch_controls, v49_controls, v48_controls, v47_controls)


def preservation() -> dict:
    manifest=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:v for group in manifest.values() for n,v in group.items()}
    require(len(old)==111,'Wrong v54 input count')
    before=Counter(); old_labels=set(); exact=0; expanded=[]
    for name,info in old.items():
        data=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
                and blob_id(data)==info['git_blob'],'Baseline identity: '+name)
        text=data.decode(); current=(P/name).read_text()
        before.update(ENV.findall(text)); old_labels.update(re.findall(r'\\label\{([^}]+)\}',text))
        if name in CHANGES: require(current==revised(name,text),'Unexpected edit: '+name)
        else: require(current==text,'Unprescribed inherited change: '+name)
        exceptions=waiting_blocks(text) if name==MODULE else ()
        for match in BLOCK.finditer(text):
            block=match.group(0)
            if block in exceptions:
                expanded.append({'file':name,'environment':match.group(1),
                                 'old_sha256':hashlib.sha256(block.encode()).hexdigest()})
            else:
                require(block in current,'Missing inherited block: '+name)
                exact+=1
        require(re.findall(r'\\input\{([^}]+)\}',text)==re.findall(r'\\input\{([^}]+)\}',current),
                'Input order changed: '+name)
    old_statement,old_proof=waiting_blocks((ARCHIVE/MODULE).read_text())
    new_statement,new_proof=waiting_blocks((P/MODULE).read_text())
    require(new_statement.replace(ADDED_ITEMS,'',1)==old_statement,'Old theorem text was removed')
    require(new_proof.replace(ADDED_PROOF+'\n','',1)==old_proof,'Old proof text was removed')
    require(len(expanded)==2,'Only existing stopping theorem/proof may expand')
    active=graph(P,'main.tex')|graph(P,'two_collision.tex')
    require(active==set(old),'Active input graph differs')
    joined='\n'.join((P/n).read_text() for n in sorted(active))
    require(Counter(ENV.findall(joined))==before,'Statement/proof inventory changed')
    labels=re.findall(r'\\label\{([^}]+)\}',joined)
    require(len(labels)==len(set(labels)) and old_labels<=set(labels),'Lost or duplicate labels')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',joined))
    require(not {r for r in refs if r not in labels and not r.startswith('TC-')},'Unresolved references')
    cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',joined) for k in c.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',joined))
    require(cites<=bib,'Unresolved citations')
    main=(P/'main.tex').read_text()
    require(main.index(r'\input{article/01_introduction_v41}')>main.index(r'\appendix'),'Catalogue inactive')
    return {'baseline_inputs':111,'active_inputs':len(active),'unchanged_in_place':107,
        'archived_exact_originals':list(CHANGES),'inherited_blocks_verbatim':exact,
        'additively_expanded_blocks':expanded,'old_expanded_block_text_exactly_recoverable':True,
        'inherited_environments':dict(sorted(before.items())), 'new_environments':{},
        'active_labels':len(labels),'unresolved_references_or_citations':[]}


def tv(a,b):
    require(len(a)==len(b),'Different supports')
    return sum(abs(x-y) for x,y in zip(a,b))/2

def risk(a,b): return sum(min(x,y) for x,y in zip(a,b))/2

def stopped(p,q,b):
    counts=[(1-p)**b]+[p*(1-p)**(k-1) for k in range(1,b+1)]
    full=[counts[0]]+[x*y for x in counts[1:] for y in q]
    require(sum(counts)==sum(full)==1,'Unnormalized stopped law')
    return counts,full


def reduction_controls() -> dict:
    pairs=[(F(3,4),F(1,4)),(F(1,2),F(1,4)),(F(2,3),F(1,3)),
           (F(1,16),F(1,1024)),(F(4,5),F(3,5))]
    marks=[((F(1,3),F(2,3)),(F(1,2),F(1,2))),
           ((F(1),F(0)),(F(0),F(1))),
           ((F(1,2),F(1,2)),(F(1,2),F(1,2)))]
    total=0; ties=0; strict=0
    for p0,p1 in pairs:
        for b in (1,2,3,5,11,23):
            K=max(k for k in range(1,b+1)
                  if p0*(1-p0)**(k-1)>=p1*(1-p1)**(k-1))
            formula=((1-p0)**K+1-(1-p1)**K)/2
            for q0,q1 in marks:
                c0,f0=stopped(p0,q0,b); c1,f1=stopped(p1,q1,b)
                a0,a1=1-c0[0],1-c1[0]; eta=tv(q0,q1)
                _,sim0=stopped(p0,q0,b); _,sim1=stopped(p1,q0,b)
                require(sim0==f0 and tv(sim1,f1)==a1*eta,'Count simulation error')
                rc,rf=risk(c0,c1),risk(f0,f1)
                require(rc==formula and 0<=rc-rf<=a1*eta/2,'Count/full risk comparison')
                if rc>rf: strict+=1
                overlap=((1-p0)**b+sum(min(p0*(1-p0)**(k-1)*x,p1*(1-p1)**(k-1)*y)
                    for k in range(1,b+1) for x,y in zip(q0,q1)))/2
                require(overlap==rf,'Full overlap formula')
                # The bit simulation uses the conditional FULL zero law, not just its mark.
                bit_sim0=[1-a0]+[a0*x/a0 for x in f0[1:]]
                bit_sim1=[1-a1]+[a1*x/a0 for x in f0[1:]]
                require(bit_sim0==f0 and tv(bit_sim1,f1)<=a1,'Bit simulation error')
                require(a0-a1<=tv(f0,f1)<=a0,'Shared cemetery bound')
                # Count-preserving kernel preserves the entire charged-count law.
                for c,ff in ((c0,sim0),(c1,sim1)):
                    projected=[ff[0]]+[sum(ff[1+2*j:1+2*(j+1)]) for j in range(b)]
                    require(projected==c,'Count or censoring flag changed')
                for k in range(1,b+1):
                    if p0*(1-p0)**(k-1)==p1*(1-p1)**(k-1):
                        alternate=((1-p0)**(k-1)+1-(1-p1)**(k-1))/2
                        require(alternate==formula,'Likelihood tie has inconsistent risk')
                        ties+=1
                total+=1
    require(ties>0 and strict>0,'Missing tie or unequal-mark controls')
    # A strict off-by-one threshold error must change the risk.
    p0,p1=F(1,2),F(1,4)
    require(((1-p0)**2+1-(1-p1)**2)/2!=((1-p0)**3+1-(1-p1)**3)/2,
            'Threshold off-by-one negative control')
    limits=[]
    for m in (32,128,512):
        pp0=1/m**2; pp1=1/m**4
        for lam in (0,1,2):
            b=m if lam==0 else lam*m*m
            a0=-math.expm1(b*math.log1p(-pp0));a1=-math.expm1(b*math.log1p(-pp1))
            bound=a1+max(abs(a0-(1-math.exp(-lam))),a1)
            require(bound<4/m if lam==0 else bound<6/m**2,'Bernoulli limit rate control')
            limits.append({'m':m,'lambda':lam,'Le_Cam_upper_bound':format(bound,'.9g')})
    pp0,pp1,b=1e-3,1e-6,10**9
    kb=min(b,math.floor(1+math.log(pp0/pp1)/(math.log1p(-pp1)-math.log1p(-pp0))))
    rc=(math.exp(kb*math.log1p(-pp0))-math.expm1(kb*math.log1p(-pp1)))/2
    rb=(math.exp(b*math.log1p(-pp0))-math.expm1(b*math.log1p(-pp1)))/2
    require(rb>.49 and rc<.005,'Large-cap bit/count separation not detected')
    return {'exact_finite_laws':total,'tie_decisions_checked':ties,'strict_full_mark_improvements':strict,
        'count_kernel_error_exact':True,'charge_distribution_preserved':True,
        'finite_intensity_Le_Cam_controls':limits,
        'large_cap_example':{'p0':pp0,'p1':pp1,'cap':b,'threshold':kb,
                             'count_risk':format(rc,'.10g'),'bit_risk':format(rb,'.10g')},
        'negative_controls':['off-by-one count threshold','bit is not sufficient uniformly over all caps',
                             'unequal terminal marks can strictly improve the exact full risk'],
        'scope':'Finite exact laws and numerical limit controls, not a proof of the physical relative law or an unknown-profile estimator.'}

if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
      'preservation':preservation(),'reduction_controls':reduction_controls(),
      'retained_v54_controls':v54_controls(),'retained_v53_controls':small_window_controls(),
      'retained_v52_controls':window_controls(),'retained_v51_controls':v51_controls(),
      'retained_v50_controls':two_branch_controls(),'retained_v49_controls':v49_controls(),
      'retained_v48_controls':v48_controls(),'retained_v47_controls':v47_controls()},indent=2,sort_keys=True))
