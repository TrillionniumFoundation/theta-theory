#!/usr/bin/env python3
"""Finite algebraic and source-graph diagnostics for A2 v25; not a proof checker."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

BASE = 'c35b31b1924a1621374eab72ee60e4cb5ab37df5'
PAPER = 'papers/A2-v17-boundary-information-coarsening'
NEW = [
 'article/01_introduction_v25.tex',
 'article/23e_signature_stability_v25.tex',
 'article/18c1_endpoint_time_deficiency_v25.tex',
 'article/29a_signed_one_flight_benchmark_v25.tex',
 'article/25a_common_observables_v25.tex',
 'article/25b_augmented_global_reconstruction_v25.tex',
 'article/25c_analytic_variation_bundles_v25.tex',
 'v5/references_v25.tex',
]
PRESERVED = [
 'v3/10_geometry_action.tex', 'v3/20_integration.tex',
 'v4/10_boundary_layers.tex', 'v5/15_differentiated_operators.tex',
 'v6/10_experiment_transfer.tex', 'v5/references_v18.tex',
 'article/23a_signed_endpoint_rigidity_v22.tex',
 'article/23b_intrinsic_multichannel_rigidity_v23.tex',
 'article/23d_rank_two_lattice_recovery_v24.tex',
 'article/18a_vector_boundary_information_v22.tex',
 'article/18b0_anchored_realization_v22.tex',
 'article/18b_raw_physical_multirate_v22.tex',
 'article/18d_count_endpoint_multirate_v23.tex',
 'article/18d1_intrinsic_count_geometry_v24.tex',
 'article/99_auxiliary_compendium_v19.tex', 'two_collision.tex',
 'article/01_introduction_v24.tex',
 'article/23e_quantitative_gluing_stability_v24.tex',
 'article/18c1_endpoint_time_deficiency_v24.tex',
 'article/25a_uniform_physical_global_v24.tex',
]

def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)

def mm(a: list, b: list) -> list:
    return [[sum((x*y for x,y in zip(row,col)), F(0))
             for col in zip(*b)] for row in a]

def transpose(a: list) -> list:
    return [list(x) for x in zip(*a)]

def inverse(a: list) -> list:
    n = len(a)
    work = [[F(x) for x in row] + [F(int(i==j)) for j in range(n)]
            for i,row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if work[i][j]), None)
        require(pivot is not None, 'singular exact matrix')
        work[j], work[pivot] = work[pivot], work[j]
        d = work[j][j]
        work[j] = [v/d for v in work[j]]
        for i in range(n):
            if i != j:
                c = work[i][j]
                work[i] = [v-c*w for v,w in zip(work[i],work[j])]
    return [row[n:] for row in work]

def eye(n: int) -> list:
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]

def finite_checks() -> dict:
    counts = Counter()
    for x in [F(1,2), F(2,3), F(3,4), F(4,5)]:
        for n in range(3,11):
            c = (1+x**(2*n))/(1-x**(2*n))
            s = 2*x**n/(1-x**(2*n))
            for r in [F(1,2),F(1),F(3,2)]:
                a = [[c,r**n*s],[r**(-n)*s,c]]
                b = [[c,-r**n*s],[-r**(-n)*s,c]]
                require(mm(a,b)==eye(2), 'determinant-one inverse')
                counts['exact_jet_blocks'] += 1
    for g,kappa in [(F(3,4),F(1,3)),(F(4,3),F(1,2))]:
        require((1+g*kappa)**2-1==g*g, 'fixed quadratic action witness')
        counts['gap_witnesses'] += 1
    require(F(3,4)!=F(4,3), 'augmented gaps do not separate')
    rot = [[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    for m in [[[2,1],[0,3]],[[1,0],[2,1]],[[3,-1],[2,2]]]:
        for l in [[[2,F(1,2)],[0,3]],[[1,-1],[1,2]]]:
            v = mm(l,m)
            recovered = mm(v,inverse(m))
            require(recovered==l, 'rank-two lattice inverse')
            require(mm(transpose(mm(rot,l)),mm(rot,l))==mm(transpose(l),l),
                    'Gram rotational invariance')
            counts['exact_lattice_cases'] += 1
    cos4 = [1,0,-1,0]
    sin4 = [0,1,0,-1]
    for nodes,m in [([0,2],2),([0,1],3),([0,1,2],2),([0,1,2,3],2)]:
        d = (len(nodes)-1)*(m+1)+m
        rows=[]
        for node in nodes:
            for r in range(m+1):
                row=[F(int(r==0))]
                for n in range(1,d+1):
                    phase=(n*node+r)%4
                    row.extend([F(n**r*cos4[phase]),F(n**r*sin4[phase])])
                rows.append(row)
        gram=mm(rows,transpose(rows))
        right=mm(transpose(rows),inverse(gram))
        require(mm(rows,right)==eye(len(rows)), 'analytic Hermite right inverse')
        counts['exact_Hermite_right_inverses'] += 1
    for j in [2,6,20,60]:
        for h in [F(1,10),F(1,100),F(1,1000)]:
            for g in [F(1,2),F(3,4),F(7,6),F(2)]:
                l=math.ceil((j*g-j*F(1,2))/h)+1
                t=j*F(1,2)+l*h
                require(h<=t-j*g<=2*h, 'pilot interior grid witness')
                for excess in [h/F(7),h,2*h]:
                    estimate=(j*g+excess-h)/j
                    require(j*abs(estimate-g)<=h, 'pilot gap bracket')
                    counts['exact_pilot_brackets'] += 1
    def radius(t: float) -> float:
        return 3+math.cos(2*t)+0.5*math.cos(3*t)
    def sig(t: float) -> tuple:
        r=radius(t)
        rp=-2*math.sin(2*t)-1.5*math.sin(3*t)
        return 1/r,-rp/r**3
    for t in [0.01,0.02,0.05,0.1,0.2,0.3]:
        a,b=sig(t),sig(-t)
        require(abs(a[0]-b[0])<1e-14, 'scalar paired signature witness')
        require(abs(a[1]-b[1])>1e-5, 'oriented derivative fails to distinguish')
        counts['oval_paired_signatures'] += 1
    require(F(17,2)/F(9,2)**3==F(68,729), 'oval immersion derivative')
    for eps in [F(1,1000),F(1,100),F(1,10)]:
        for s in [F(-1,4),F(0),F(1,4)]:
            require(6*s*s+4-2*eps>0, 'enriched noisy-match Hessian')
            counts['noisy_match_Hessian_cases'] += 1
    for j in range(1,21):
        g=F(j+2,3); u=F(j,100); v=F(-j,120)
        p0=F(2,3)*u*u+F(1,5)*u**3
        p1=F(1,2)*v*v-F(1,7)*v**3
        require((g+p0)**2+u*u-u*u==(g+p0)**2 and g+p0>0,
                'one-flight first slice')
        require((g+p1)**2+v*v-v*v==(g+p1)**2 and g+p1>0,
                'one-flight second slice')
        counts['exact_one_flight_slices'] += 2
    for k in [20,40,100,1000]:
        r=F(4)
        for z in [F(-1),F(-1,2),F(0),F(1,2),F(1)]:
            p=(r-z)/(k-z)
            require(abs(k*p-(r-z))<=F(6,k-1), 'uniform layer intensity')
            require(k*p*p<=F(30,k), 'binomial-Poisson bound')
            a=math.sqrt(1+float(z)/k)-1
            b=math.sqrt(1-float(z)/k)-1
            h2=(a*a+b*b)/2
            require(h2<=2/k**2, 'bulk relative-density Hellinger bound')
            counts['layer_bulk_cases'] += 1
    for j in range(1,11):
        theta=j/9; phi=j/7
        n=(math.cos(theta),math.sin(theta)); t=(-n[1],n[0])
        p=(2.0+j,-3.0+j/2)
        x=(p[0]+0.12*t[0]+0.02*n[0],p[1]+0.12*t[1]+0.02*n[1])
        ph=(p[0]+0.001,p[1]-0.002)
        def rotate(a):
            return (math.cos(phi)*a[0]-math.sin(phi)*a[1],
                    math.sin(phi)*a[0]+math.cos(phi)*a[1])
        def move(a):
            b=rotate(a); return (b[0]+1000,b[1]-2000)
        y,q,tt=move(x),move(ph),rotate(t)
        u=sum(a*(b-c) for a,b,c in zip(t,x,ph))
        uu=sum(a*(b-c) for a,b,c in zip(tt,y,q))
        require(abs(u-uu)<1e-10, 'sensor-frame equivariance')
        counts['sensor_equivariance_cases'] += 1
    return dict(sorted(counts.items()))

INPUT=re.compile(r'\\(?:input|include)\s*\{([^}]+)\}')
LABEL=re.compile(r'\\label\s*\{([^}]+)\}')
REF=re.compile(r'\\(?:eqref|ref|pageref|autoref|[Cc]ref)\s*\{([^}]+)\}')
CITE=re.compile(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}')
BIB=re.compile(r'\\bibitem(?:\[[^\]]*\])?\s*\{([^}]+)\}')

def source_checks(root: Path) -> dict:
    require((root/'main.tex').is_file(), 'missing complete native source root')
    def text(path: Path) -> str:
        return re.sub(r'(?<!\\)%[^\n]*','',path.read_text(encoding='utf-8'))
    def graph(entry: str, found: dict) -> None:
        if entry in found: return
        file=root/entry
        require(file.is_file(), 'missing active TeX input: '+entry)
        found[entry]=text(file)
        for raw in INPUT.findall(found[entry]):
            rel=raw if raw.endswith('.tex') else raw+'.tex'
            require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,
                    'nonlocal input')
            graph(rel,found)
    graphs={}
    for entry in ['two_collision.tex','main.tex']:
        found={}; graph(entry,found); graphs[entry]=found
    companion=set(LABEL.findall('\n'.join(graphs['two_collision.tex'].values())))
    counts={}
    for entry,found in graphs.items():
        combined='\n'.join(found.values())
        labels=LABEL.findall(combined); duplicates=[x for x,c in Counter(labels).items() if c>1]
        external={'TC-'+x for x in companion} if entry=='main.tex' else set()
        known=set(labels)|external
        refs={x.strip() for group in REF.findall(combined) for x in group.split(',')}
        cites={x.strip() for group in CITE.findall(combined) for x in group.split(',')}
        missing_refs=sorted(refs-known); missing_cites=sorted(cites-set(BIB.findall(combined)))
        require(not duplicates, entry+' duplicate labels: '+repr(duplicates))
        require(not missing_refs, entry+' unresolved references: '+repr(missing_refs))
        require(not missing_cites, entry+' unresolved citations: '+repr(missing_cites))
        counts[entry]={'active_files':len(found),'labels':len(labels),'citations':len(cites)}
    active=graphs['main.tex']
    for rel in NEW:
        require(rel in active,'new module is not active: '+rel)
        raw=(root/rel).read_bytes()
        require(not any(b<32 and b not in (9,10) for b in raw),'control byte: '+rel)
    for rel in PRESERVED:
        require((root/rel).is_file(),'missing retained derivation: '+rel)
    poisson=active['article/18c1_endpoint_time_deficiency_v25.tex']
    require(r'd\Lambda_z^R=\rho(u,v)' in poisson,'incorrect Poisson density token')
    old=graphs['main.tex']['main.tex']
    for inactive in ['article/01_introduction_v24','article/23e_quantitative_gluing_stability_v24',
                     'article/18c1_endpoint_time_deficiency_v24','article/25a_uniform_physical_global_v24']:
        require('\\input{'+inactive+'}' not in old,'superseded claim is still active')
    oldbib=set(BIB.findall(text(root/'v5/references_v18.tex')))
    newbib=set(BIB.findall(text(root/'v5/references_v25.tex')))
    require(oldbib<=newbib and 'MeisterReiss' in newbib,'bibliography retention')
    git=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=root,
                       capture_output=True,text=True,check=False)
    checked=0
    if git.returncode==0:
        repo=Path(git.stdout.strip())
        for rel in PRESERVED:
            p=subprocess.run(['git','show',BASE+':'+PAPER+'/'+rel],cwd=repo,
                             capture_output=True,check=False)
            require(p.returncode==0,'cannot inspect pinned source: '+rel)
            require(p.stdout==(root/rel).read_bytes(),'historical derivation changed: '+rel)
            checked+=1
    hashes={rel:hashlib.sha256((root/rel).read_bytes()).hexdigest()
            for rel in ['main.tex']+NEW}
    return {'graphs':counts,'pinned_unchanged_files':checked,'new_source_sha256':hashes,
            'retained_bibliography_items':len(oldbib)}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--math-only',action='store_true')
    parser.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    result={'status':'passed','scope':'Finite identities, witnesses, bounds, and optional native source graph; not theorem certification.',
            'finite_checks':finite_checks()}
    if not args.math_only:
        result['source_checks']=source_checks(args.source_root.resolve())
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
