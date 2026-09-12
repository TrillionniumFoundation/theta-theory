#!/usr/bin/env python3
"""Finite diagnostics and explicitly scoped source audits for A2 v26.

The finite cases are regression checks, not proofs of the manuscript's
infinite-dimensional theorems. Default mode requires the complete native
main and companion graphs. --math-only and --changed-sources are narrower
modes and label their output accordingly. No required check uses assert.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = '47057587d104074f0e1dde54c1d5d6abb629378f'
REPLACEMENTS = {
    'article/01_introduction_v25.tex': 'article/01_introduction_v26.tex',
    'article/18a_vector_boundary_information_v22.tex': 'article/18a_vector_boundary_information_v26.tex',
    'article/18c_full_endpoint_time_information_v23.tex': 'article/18c_full_endpoint_time_information_v26.tex',
    'article/25b_augmented_global_reconstruction_v25.tex': 'article/25b_augmented_global_reconstruction_v26.tex',
}
NEW = [
    'article/23f_single_offset_law_inverse_v26.tex',
    'article/29b_direct_position_benchmark_v26.tex',
    'article/18f_domination_and_position_comparison_v26.tex',
]
PINNED = {
    'article/18a_vector_boundary_information_v22.tex': 'f0f79ad0bd3ccbb91c3e0b374d355d917e253162',
    'article/18c_full_endpoint_time_information_v23.tex': 'da01c23f356069b9441370edab1f7095c7406e2c',
    'article/23a_signed_endpoint_rigidity_v22.tex': 'facc0674006967debca05ab4196002e8a7f5b886',
    'article/25a_common_observables_v25.tex': '82df03f99c1d6ac322161381e063d2f107f048ed',
    'article/18c1_endpoint_time_deficiency_v25.tex': 'e03e7eb7e450e6c467f898444d8b72b5fddfd093',
    'tools/build_submission.py': '233b6f37ff4912b99793460634983ac9b8da379b',
}
INPUT = re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')
LABEL = re.compile(r'\\label\{([^{}]+)\}')
REF = re.compile(r'\\(?:eqref|ref|pageref|autoref|cref|Cref)\*?\{([^{}]+)\}')
CITE = re.compile(r'\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^{}]+)\}')
BIB = re.compile(r'\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def poly(p: list[F], x: F) -> F:
    value = F(0)
    for c in reversed(p):
        value = value*x+c
    return value


def add(p: list[F], q: list[F]) -> list[F]:
    return [a+b for a,b in zip(p,q)]


def mul(p: list[F], q: list[F]) -> list[F]:
    return [sum((p[i]*q[n-i] for i in range(n+1)), F(0))
            for n in range(len(p))]


def div(p: list[F], q: list[F]) -> list[F]:
    require(q[0] != 0, 'zero series divisor')
    out: list[F] = []
    for n, c in enumerate(p):
        out.append((c-sum((q[i]*out[n-i] for i in range(1,n+1)), F(0)))/q[0])
    return out


def scale(c: F, p: list[F]) -> list[F]:
    return [c*x for x in p]


def positive_sqrt(q: F) -> F:
    require(q > 0, 'nonpositive anchor defect')
    a,b = math.isqrt(q.numerator),math.isqrt(q.denominator)
    require(a*a == q.numerator and b*b == q.denominator,
            'test anchor defect is not an exact rational square')
    return F(a,b)


def inverse_matrix(a: list[list[F]]) -> list[list[F]]:
    n=len(a)
    m=[row[:]+[F(int(i == j)) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if m[i][j]),None)
        require(pivot is not None,'singular Vandermonde matrix')
        m[j],m[pivot]=m[pivot],m[j]
        d=m[j][j]
        m[j]=[x/d for x in m[j]]
        for i in range(n):
            if i != j:
                d=m[i][j]
                m[i]=[x-d*y for x,y in zip(m[i],m[j])]
    return [row[n:] for row in m]


def finite_checks() -> dict:
    counts: Counter[str] = Counter()
    shapes=[
        [F(0),F(0),F(1,2),F(1,15),F(1,40)],
        [F(0),F(0),F(3,4),F(-1,12),F(1,30)],
        [F(0),F(0),F(2,5),F(1,20),F(1,25),F(-1,100)],
    ]
    amp=[F(3,2),F(1,4),F(1,8),F(-1,30)]
    grid=[F(i,12) for i in range(-3,4)]
    for s,d,z,a in itertools.product(shapes,[F(1,2),F(1),F(2)],
                                     [F(2,3),F(1),F(7,3)],[F(-1,5),F(1,5)]):
        def density(u:F,v:F)->F:
            return poly(amp,u)*poly(amp,v)*(d-poly(s,u)-poly(s,v))/z
        def ratio(u:F,v:F)->F:
            return density(u,v)*density(F(0),F(0))/(density(u,F(0))*density(F(0),v))
        q=positive_sqrt(1-ratio(a,a))
        for u,v in itertools.product(grid,repeat=2):
            su,sv=poly(s,u),poly(s,v)
            require(density(u,v)>0,'interior test outside support')
            require(1-ratio(u,v) == su*sv/((d-su)*(d-sv)), 'rank-one cancellation')
            t=(1-ratio(u,a))/q
            require(d*t/(1+t) == su,'signed action recovery')
            b=density(u,F(0))/density(F(0),F(0))*(1+t)
            require(b == poly(amp,u)/amp[0],'amplitude recovery')
            counts['rational_density_cases']+=1
    for order,a in itertools.product([3,4,6,8,10],[F(-1,5),F(1,5)]):
        one=[F(1)]+[F(0)]*order
        s=[F(0),F(0),F(1,2)]+[F((-1)**i,30*(i+1)) for i in range(3,order+1)]
        b=[F(3,2)]+[F((-1)**i,20*(i+1)) for i in range(1,order+1)]
        d=F(1)
        sa,ba=poly(s,a),poly(b,a)
        f00=b[0]*b[0]*d
        fua=scale(ba,mul(b,add(scale(d-sa,one),scale(F(-1),s))))
        fu0=scale(b[0],mul(b,add(scale(d,one),scale(F(-1),s))))
        f0a=b[0]*ba*(d-sa)
        R=div(scale(f00,fua),scale(f0a,fu0))
        t=scale((d-sa)/sa,add(one,scale(F(-1),R)))
        recovered=div(scale(d,t),add(one,t))
        recovered_b=mul(scale(F(1)/f00,fu0),add(one,t))
        require(recovered == s,'formal action jets, including odd orders')
        require(recovered_b == scale(F(1)/b[0],b),'formal amplitude jets')
        counts['formal_jet_cases']+=1
    for x,r,n in itertools.product([F(1,4),F(1,2),F(3,4)],
                                    [F(2,3),F(1),F(5,3)],range(3,11)):
        a=(1+x**(2*n))/(1-x**(2*n))
        c=2*x**n/(1-x**(2*n))
        b,e=r**n*c,r**(-n)*c
        require(a*a-b*e == 1,'determinant-one jet block')
        q0,q1=F(n,7),F(-n-1,9)
        y0,y1=a*q0+b*q1,e*q0+a*q1
        require((a*y0-b*y1,-e*y0+a*y1) == (q0,q1),'jet block inverse')
        counts['determinant_block_cases']+=1
    for m,a in itertools.product([2,3,4,6],[F(1,4),F(1,8),F(1,16)]):
        nodes=[F(2*i-m,2*(m+1)) for i in range(m+1)]
        v=[[x**j for j in range(m+1)] for x in nodes]
        vi=inverse_matrix(v)
        p=[F(0),F(0)]+[F(1,j+2) for j in range(2,m+2)]
        eps=a**(m+1)
        y=[poly(p,a*x)+F((-1)**i,2)*eps for i,x in enumerate(nodes)]
        coef=[sum((row[i]*y[i] for i in range(m+1)),F(0)) for row in vi]
        maxres=max(abs(p[-1]*(a*x)**(m+1)+F((-1)**i,2)*eps)
                   for i,x in enumerate(nodes))
        for j in range(m+1):
            err=abs(coef[j]/a**j-p[j])*math.factorial(j)
            bound=sum(abs(z) for z in vi[j])*maxres/a**j*math.factorial(j)
            require(err<=bound,'scaled interpolation remainder bound')
        counts['interpolation_cases']+=1
    lam=[0.25,0.5,0.75]
    for mask in [(0,0,0),(1,1,1),(1,0,1),(0,1,1)]:
        excluded=sum(v for v,keep in zip(lam,mask) if not keep)
        require(abs(math.exp(excluded)*math.exp(-excluded)-1)<1e-14,
                'envelope normalization')
        for ns in itertools.product(range(5),repeat=3):
            common=math.exp(-sum(lam))*math.prod(v**n/math.factorial(n)
                                                 for v,n in zip(lam,ns))
            admissible=all(keep or n == 0 for keep,n in zip(mask,ns))
            rn=math.exp(excluded) if admissible else 0.0
            target=(math.exp(-sum(v for v,k in zip(lam,mask) if k))*
                    math.prod(v**n/math.factorial(n) for v,n,k in zip(lam,ns,mask) if k)
                    if admissible else 0.0)
            require(abs(common*rn-target)<1e-13,'Poisson envelope configuration density')
            counts['poisson_configuration_cases']+=1
    for theta in [F(1,10),F(1,4),F(1,2)]:
        mass=theta**2/(1+theta)**2
        require(mass>0 and mass<1,'reference-exclusive mass under Lebesgue domination')
        counts['reference_exclusive_cases']+=1
    caps=[2,9,4,40,30,75,61]
    bounds=[max([i+1]+caps[:i+1]) for i in range(len(caps))]
    for budget in range(1,101):
        selected=[s for s,b in enumerate(bounds,1) if b<=budget]
        if selected:
            s=max(selected)
            require(caps[s-1]<=budget,'restart policy exceeds budget')
            j=2*((s+1)//2)
            require(j%2 == 0 and j>=s,'restart policy minimum-flight requirement')
        counts['budget_restart_cases']+=1
    return {'status':'passed','case_counts':dict(sorted(counts.items())),
            'total_cases':sum(counts.values()),
            'scope':'Finite exact/rational and finite numerical regression cases; not theorem certification.'}


def strip_comments(text: str) -> str:
    return re.sub(r'(?<!\\)%[^\n]*','',text)


def blob_sha(path: Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def changed_audit(baseline_dir: Path | None) -> dict:
    files=['main.tex',*REPLACEMENTS.values(),*NEW]
    texts={p:(ROOT/p).read_text(encoding='utf-8') for p in files}
    for p,t in texts.items():
        require('non-dominated' not in t.lower(), 'obsolete scalar/Poisson classification in '+p)
        begins=Counter(re.findall(r'\\begin\{([^}]+)\}',t))
        ends=Counter(re.findall(r'\\end\{([^}]+)\}',t))
        require(begins == ends,'unbalanced environment counts in '+p)
    declared=[label for t in texts.values() for label in LABEL.findall(strip_comments(t))]
    require(len(declared) == len(set(declared)),'duplicate label in changed sources')
    for old,new in REPLACEMENTS.items():
        if old.endswith('introduction_v25.tex') or old.endswith('reconstruction_v25.tex'):
            continue
        p=ROOT/old
        if not p.is_file() and baseline_dir:
            p=baseline_dir/Path(old).name
        require(p.is_file(),'historical source unavailable for preservation check: '+old)
        require(blob_sha(p) == PINNED[old],'historical source blob mismatch: '+old)
        t=p.read_text(encoding='utf-8')
        require(set(LABEL.findall(t)) <= set(LABEL.findall(texts[new])),
                'lost historical labels in '+new)
        require(t.count(r'\begin{proof}') == texts[new].count(r'\begin{proof}'),
                'proof count changed unexpectedly in '+new)
        # All displayed mathematics in the two terminology corrections is retained.
        displays=re.findall(r'\\\[(.*?)\\\]|\\begin\{(?:equation|align)\*?\}(.*?)\\end\{(?:equation|align)\*?\}',t,re.S)
        normalized_new=re.sub(r'\s+','',texts[new])
        for pair in displays:
            display=next((x for x in pair if x),'')
            require(re.sub(r'\s+','',display) in normalized_new,
                    'displayed mathematical block lost in '+new)
    main=texts['main.tex']
    for path in [*REPLACEMENTS.values(),*NEW,'article/99_auxiliary_compendium_v19.tex',
                 'article/23a_signed_endpoint_rigidity_v22.tex','v5/references_v25.tex']:
        require(path[:-4] in INPUT.findall(main),'required active input absent: '+path)
    for old in REPLACEMENTS:
        require(old[:-4] not in INPUT.findall(main),'superseded input still active: '+old)
    return {'status':'passed','scope':'Changed-source syntax/labels and pinned terminology-proof preservation only.',
            'changed_files':files,'changed_labels':len(declared),
            'historical_terminology_sources_verified':2,
            'native_recursive_graph':'not_checked_in_this_mode'}


def native_audit() -> dict:
    graphs: dict[str,set[str]]={}
    texts: dict[str,str]={}
    def visit(path: str, seen: set[str]) -> None:
        require(not Path(path).is_absolute() and '..' not in Path(path).parts,
                'nonlocal native input: '+path)
        if path in seen:
            return
        p=ROOT/path
        require(p.is_file(),'missing complete native source: '+path)
        seen.add(path)
        t=strip_comments(p.read_text(encoding='utf-8'))
        texts[path]=t
        for raw in INPUT.findall(t):
            visit(raw if raw.endswith('.tex') else raw+'.tex',seen)
    for entry in ['main.tex','two_collision.tex']:
        graphs[entry]=set()
        visit(entry,graphs[entry])
    for path,expected in PINNED.items():
        require((ROOT/path).is_file(),'missing retained pinned source: '+path)
        require(blob_sha(ROOT/path) == expected,'changed retained pinned source: '+path)
    labels={e:set(x for p in ps for x in LABEL.findall(texts[p])) for e,ps in graphs.items()}
    for entry,paths in graphs.items():
        declared=[x for p in paths for x in LABEL.findall(texts[p])]
        repeated=[x for x,n in Counter(declared).items() if n>1]
        require(not repeated,'duplicate native labels: '+repr(repeated))
        bib=set(x for p in paths for x in BIB.findall(texts[p]))
        available=set(labels[entry])
        if entry == 'main.tex':
            available.update('TC-'+x for x in labels['two_collision.tex'])
        refs=set(x.strip() for p in paths for z in REF.findall(texts[p]) for x in z.split(','))
        cites=set(x.strip() for p in paths for z in CITE.findall(texts[p]) for x in z.split(','))
        require(not refs-available,'unresolved native references: '+repr(sorted(refs-available)))
        require(not cites-bib,'unresolved native citations: '+repr(sorted(cites-bib)))
    changed=changed_audit(None)
    return {'status':'passed','scope':'Complete literal-braced native source graph, labels, citations, pinned files and changed-source audit. Not a TeX execution.',
            'entrypoint_files':{e:len(v) for e,v in graphs.items()},
            'union_tex_files':len(texts),'pinned_files':len(PINNED),
            'changed_source_audit':changed,
            'sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(texts)}}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--math-only',action='store_true')
    modes.add_argument('--changed-sources',action='store_true')
    parser.add_argument('--baseline-dir',type=Path)
    args=parser.parse_args()
    report={'revision':'A2 v26','review_base_commit':BASE,'finite_diagnostics':finite_checks()}
    if args.math_only:
        report['source_audit']={'status':'not_run','scope':'math-only invocation'}
    elif args.changed_sources:
        report['source_audit']=changed_audit(args.baseline_dir)
    else:
        report['source_audit']=native_audit()
    print(json.dumps(report,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
