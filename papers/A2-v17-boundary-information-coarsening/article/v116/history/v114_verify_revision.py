#!/usr/bin/env python3
"""Source preservation, exact finite diagnostics, and PDF receipts; not a proof checker."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = '63daaeee1da5a1ee3ac569584e06f55081073da0'
PREFIX = 'papers/A2-v17-boundary-information-coarsening/article/v114/'
OLD = PREFIX.replace('/v114/', '/v113/')
P = 1009

def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=HERE, text=True).strip()

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def rref(a: list[list[int]], width: int | None = None):
    width = len(a[0]) if a else (width or 0)
    a = [[x % P for x in row] for row in a]
    pivots, r = [], 0
    for j in range(width):
        i = next((i for i in range(r, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[r], a[i] = a[i], a[r]
        inv = pow(a[r][j], -1, P)
        a[r] = [x*inv % P for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                t = a[i][j]
                a[i] = [(x-t*y) % P for x, y in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    return a, pivots

def rank(a: list[list[int]]) -> int:
    return len(rref(a)[1])

def nullspace(a: list[list[int]], width: int) -> list[list[int]]:
    a, pivots = rref(a, width)
    out = []
    for j in range(width):
        if j in pivots:
            continue
        v = [0]*width
        v[j] = 1
        for i, p in enumerate(pivots):
            v[p] = -a[i][j] % P
        out.append(v)
    return out

def exponents(k: int, m: int):
    for ids in itertools.combinations_with_replacement(range(k), m):
        yield tuple(ids.count(i) for i in range(k))

def polar_diagnostics() -> dict:
    records = []
    cases = [(4,2,[(0,1)]),(7,2,[(0,1,2,3,4)]),
             (6,2,[(0,1,2),(0,1,3)]),(5,3,[(0,1,2)]),
             (5,3,[(0,1),(0,2)]),(5,4,[(0,1,2)])]
    for k, m, contacts in cases:
        mons = list(exponents(k,m)); index = {v:i for i,v in enumerate(mons)}
        sources = [(nu,v) for nu,u in enumerate(contacts) for v in mons
                   if all(not v[i] or i in u for i in range(k))]
        e = len(sources)
        target = min(8,e,len({v for _,v in sources})+1)
        coords = [(nu,i,j) for nu,u in enumerate(contacts) for i in u
                  for j in range(k) if j not in u]
        M = len(coords)
        for seed in range(1,9):
            rng = random.Random(10000*m+100*k+seed)
            beta = [[rng.randrange(P) for _ in mons] for _ in range(target)]
            for _,v in sources:
                beta[0][index[v]] = 0
            B = []
            for nu,v in sources:
                row = []
                for eta,i,j in coords:
                    if eta != nu or not v[i]:
                        row.append(0); continue
                    w = list(v); w[i]-=1; w[j]+=1
                    row.append(v[i]*beta[0][index[tuple(w)]] % P)
                B.append(row)
            C = [[beta[t][index[v]] for t in range(1,target)] for _,v in sources]
            jac = [b+c for b,c in zip(B,C)]
            Q = nullspace([list(col) for col in zip(*B)],e)
            tau = [[sum(q[i]*C[i][t] for i in range(e)) % P
                    for q in Q] for t in range(target-1)]
            h, rb, rt, rj = len(Q), rank(B), rank(tau), rank(jac)
            need(rb+rt==rj,'polar quotient rank identity failed')
            a = e-target+1
            tangent = M+target-1-rj
            need(tangent==M-a+h-rt,'polar tangent identity failed')
            for j in range(1,h+3):
                need((rj < e-j+1)==(rt < h-j+1),'Fitting rank threshold failed')
            if m==2:
                H = [[beta[0][index[tuple(int(t==i)+int(t==j) for t in range(k))]]
                      for j in range(k)] for i in range(k)]
                dims = [len(u)-rank([[H[i][j] for j in u] for i in range(k)])
                        for u in contacts]
                need(h==sum(math.comb(d+1,2) for d in dims),
                     'quadratic radical/polar dimension mismatch')
            records.append({'k':k,'m':m,'contacts':[len(u) for u in contacts],
                            'seed':seed,'source_rank':e,'target_rank':target,
                            'plane_rank':rb,'polar_rank':h,'residual_rank':rt,
                            'incidence_tangent_dimension':tangent})
    return {'field_prime':P,'case_count':len(records),'cases':records}

def fibre_diagnostics() -> dict:
    import sympy as sp
    result = []
    for c in range(1,5):
        aa = sp.symbols(f'a0:{c}'); bb = sp.symbols(f'b0:{c}'); xx=aa+bb
        rel = [aa[i]*bb[i] for i in range(c)]
        rel += [aa[i]*bb[j]+aa[j]*bb[i] for i in range(c) for j in range(i+1,c)]
        G = sp.groebner(rel,*xx,order='grevlex')
        for i,j,k in itertools.product(range(c),repeat=3):
            need(G.reduce(aa[i]*aa[j]*bb[k])[1]==0,'mixed cubic survives')
            need(G.reduce(aa[i]*bb[j]*bb[k])[1]==0,'mixed cubic survives')
        leading = [poly.LM(order=G.order).exponents for poly in G.polys]
        hilbert = []
        for d in range(5):
            actual = sum(not any(all(x>=y for x,y in zip(exp,lm)) for lm in leading)
                         for exp in exponents(2*c,d))
            expected = 1 if d==0 else 2*math.comb(c+d-1,d)+(math.comb(c,2) if d==2 else 0)
            need(actual==expected,'fibre Hilbert series mismatch')
            hilbert.append(actual)
        result.append({'c':c,'hilbert_coefficients_degrees_0_to_4':hilbert})
    x,y,z,w,u,v = sp.symbols('x y z w u v')
    A=sp.Matrix([[2,1,u,v],[0,3,v,u],[0,0,x,y],[0,0,z,w]])
    need(sp.expand(A.det()-6*(x*w-y*z))==0,'normal block determinant failed')
    return {'groebner_checks':result,'normal_block_determinant':True}

def expanded(path: Path, seen: set[Path] | None = None) -> str:
    seen = set() if seen is None else seen
    need(path not in seen,'duplicate or recursive input: '+str(path))
    seen.add(path)
    text = path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expanded(HERE/m.group(1),seen),text)

def checks(baseline_directory: Path | None) -> dict:
    whole = expanded(HERE/'paper.tex')
    labels = re.findall(r'\\label\{([^}]+)\}',whole)
    need(not [k for k,v in Counter(labels).items() if v>1],'duplicate labels')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',whole))
    need(refs<=set(labels),'undefined references: '+str(refs-set(labels)))
    bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',whole))
    cites = {x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',whole)
             for x in group.split(',')}
    need(cites<=bib,'undefined citations: '+str(cites-bib))
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',whole,re.S).group(1)
    need(len(abstract.split())<=200,'abstract over 200 tokens')
    if baseline_directory:
        old_paths = sorted(baseline_directory.rglob('*.tex'))
        old_data = {str(x.relative_to(baseline_directory)):x.read_bytes() for x in old_paths}
        source_commit = None
        changes = None
    else:
        git('merge-base','--is-ancestor',BASE,'HEAD')
        source_commit = git('rev-parse','HEAD')
        changed = git('diff','--name-status',BASE,'HEAD').splitlines()
        permitted = {'A2_REVISION_V114_INDEX.md','.github/workflows/a2-v114-referee.yml'}
        for line in changed:
            f = line.split('\t')
            need(f[0]=='A' and (f[1].startswith(PREFIX) or f[1] in permitted),
                 'out-of-scope/non-additive change: '+line)
        changes = len(changed)
        old_names = git('ls-tree','-r','--name-only',BASE,'--',OLD).splitlines()
        old_data = {x[len(OLD):]:git('show',BASE+':'+x).encode()+b'\n'
                    for x in old_names if x.endswith('.tex')}
        # git() strips outer whitespace; use byte-exact reads for preservation.
        old_data = {x:subprocess.check_output(['git','show',BASE+':'+OLD+x],cwd=HERE)
                    for x in old_data}
    old_whole='\n'.join(x.decode() for x in old_data.values())
    old_labels=set(re.findall(r'\\label\{([^}]+)\}',old_whole))
    old_bib=set(re.findall(r'\\bibitem\{([^}]+)\}',old_whole))
    need(old_labels<=set(labels),'lost v113 labels: '+str(old_labels-set(labels)))
    need(old_bib<=bib,'lost v113 bibliography keys')
    unchanged=['parts/02-global-geometry.tex','parts/02b-component-structure.tex',
               'parts/03-realization-stability.tex','parts/04-statistical-experiments.tex',
               'parts/04b-uniform-constants.tex','parts/05-complements.tex']
    for name in unchanged:
        need((HERE/name).read_bytes()==old_data[name],'changed retained source: '+name)
    retained={x:digest(data) for x,data in old_data.items()}
    manifest={str(x.relative_to(HERE)):digest(x.read_bytes()) for x in sorted(HERE.rglob('*'))
              if x.is_file() and 'evidence' not in x.relative_to(HERE).parts
              and x.suffix in {'.tex','.md','.py','.b64'}}
    if source_commit:
        for path,sha in manifest.items():
            committed=subprocess.check_output(['git','show','HEAD:'+PREFIX+path],cwd=HERE)
            need(digest(committed)==sha,'uncommitted source file: '+path)
    return {'source_commit':source_commit,'baseline_review_commit':BASE,
            'local_uncommitted_check':source_commit is None,'additions_only':source_commit is not None,
            'changed_file_count':changes,'old_label_count':len(old_labels),
            'label_count':len(labels),'bibliography_key_count':len(bib),
            'old_bibliography_key_count':len(old_bib),
            'byte_exact_retained_parts':unchanged,'old_source_sha256':retained,
            'source_sha256':manifest,'abstract_whitespace_tokens':len(abstract.split())}

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline-directory',type=Path)
    ap.add_argument('--with-pdf',action='store_true')
    ap.add_argument('--source-only',action='store_true')
    args=ap.parse_args()
    receipt=checks(args.baseline_directory)
    spec=importlib.util.spec_from_file_location('inherited',HERE/'verify_v113_diagnostics.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt['inherited_finite_diagnostics']=mod.diagnostics()
    receipt['new_finite_diagnostics']={'polar':polar_diagnostics(),'fibre':fibre_diagnostics()}
    receipt['verification_scope']='finite consistency diagnostics and source/PDF checks, not proof certification'
    receipt['python_version']=sys.version
    if args.with_pdf:
        pdf,log=HERE/'paper.pdf',HERE/'paper.log'
        need(pdf.exists() and pdf.read_bytes().startswith(b'%PDF-'),'invalid or missing PDF')
        text=log.read_text(errors='replace')
        errors=['undefined references','undefined citations','multiply defined','! LaTeX Error',
                '! Undefined control sequence','Overfull \\hbox','Overfull \\vbox']
        need(not any(x in text for x in errors),'PDF build warning/error')
        need(not re.search(r"(?:Reference|Citation) [`'].*?undefined",text),'undefined reference/citation')
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        receipt['pdf']={'sha256':digest(pdf.read_bytes()),'bytes':pdf.stat().st_size,
                        'pages':int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1)),
                        'overfull_boxes':0,'log_sha256':digest(log.read_bytes())}
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    name='BUILD_RECEIPT.json' if args.with_pdf else 'SOURCE_RECEIPT.json'
    (evidence/name).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in
                     {'inherited_finite_diagnostics','new_finite_diagnostics','old_source_sha256','source_sha256'}},indent=2))

if __name__=='__main__':
    main()
