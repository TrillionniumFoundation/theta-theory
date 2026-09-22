#!/usr/bin/env python3
"""Source-bound checks and finite diagnostics, not a proof checker."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
import re
import subprocess
from collections import Counter
from pathlib import Path

BASE = '66220b85960a5a50db15342ccfacfbf1395bca88'
PREFIX = 'papers/A2-v17-boundary-information-coarsening/article/v113/'
OLD = PREFIX.replace('/v113/', '/v112/')
HERE = Path(__file__).resolve().parent
BLOBS = {
 '01-contact-native.tex': 'ea55d5e3b0f1d2316baaf88eaaf7c66b2e7074aa',
 '02-global-geometry.tex': 'f33676a3564e092f9e8bb6d2b7d7e504b9e7935b',
 '02b-component-structure.tex': 'd728969ccc2898ee8b29344a4383110ce0a97ced',
 '03-realization-stability.tex': '1410da1834f5d0f144f312bfc1766b9381e1447c',
 '04-statistical-experiments.tex': 'e52ed7b8d75f840e73bed815ca0441dc21a886c3',
 '05-complements.tex': '6d605bd740e5ca4a5f02b9faa661c24dca7004e6',
}
P = 1009

def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=HERE, text=True).strip()

def rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    a = [[x % P for x in row] for row in rows]
    r = 0
    for j in range(len(a[0])):
        i = next((i for i in range(r, len(a)) if a[i][j]), None)
        if i is None:
            continue
        a[r], a[i] = a[i], a[r]
        inv = pow(a[r][j], -1, P)
        a[r] = [x * inv % P for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][j]:
                t = a[i][j]
                a[i] = [(x - t * y) % P for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r

def inverse(a: list[list[int]]) -> list[list[int]]:
    n = len(a)
    b = [[x % P for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        i = next((i for i in range(j, n) if b[i][j]), None)
        if i is None:
            raise ValueError('singular matrix')
        b[j], b[i] = b[i], b[j]
        inv = pow(b[j][j], -1, P)
        b[j] = [x * inv % P for x in b[j]]
        for i in range(n):
            if i != j and b[i][j]:
                t = b[i][j]
                b[i] = [(x - t * y) % P for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]

def mm(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(x*y for x, y in zip(row, col)) % P for col in zip(*b)] for row in a]

def conv(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j] + x*y) % P
    return out

def products(u: list[list[int]]) -> list[list[int]]:
    return [conv(u[i], u[j]) for i in range(len(u)) for j in range(i, len(u))]

def dot(a: list[int], b: list[int]) -> int:
    return sum(x*y for x, y in zip(a, b)) % P

def isotropic(k: int, c: int, r: int, s: int, seed: int) -> tuple[list[list[int]], list[int], list[list[int]]]:
    """Exact finite-field evaluation construction, including a radical basis."""
    rng = random.Random(seed)
    xs = list(range(2, r + 2))
    g = [1]
    for x in xs:
        g = conv(g, [-x, 1])
    radical = [[0]*i + g + [0]*(k-r-1-i) for i in range(k-r)]
    d = c-s
    need(d <= len(radical) and 2*s <= r, 'infeasible test construction')
    vand = [[pow(x, j, P) for j in range(r)] for x in xs]
    vi = inverse(vand)
    while True:
        a = [[0]*r for _ in range(r)]
        for i in range(r):
            for j in range(i):
                a[i][j] = rng.randrange(P)
                a[j][i] = -a[i][j] % P
        plus = [[(int(i == j)+a[i][j]) % P for j in range(r)] for i in range(r)]
        minus = [[(int(i == j)-a[i][j]) % P for j in range(r)] for i in range(r)]
        try:
            q = mm(minus, inverse(plus))
            break
        except ValueError:
            pass
    sqrt_minus_one = next(i for i in range(P) if i*i % P == P-1)
    z = [[0]*s for _ in range(r)]
    for j in range(s):
        z[2*j][j], z[2*j+1][j] = 1, sqrt_minus_one
    vals = mm(q, z)
    coefs = mm(vi, vals)
    nonrad = [list(col) + [0]*(k-r) for col in zip(*coefs)]
    w = radical[:d]
    u = w + nonrad
    ell = [sum(pow(x, j, P) for x in xs) % P for j in range(2*k-1)]
    need(rank(u) == c, 'dependent isotropic frame')
    need(all(dot(ell, v) == 0 for v in products(u)), 'isotropy failure')
    return u, ell, w

def tangent_test(u: list[list[int]], ell: list[int], w: list[list[int]]) -> dict:
    k, c = len(u[0]), len(u)
    frame = [row[:] for row in u]
    complement = []
    for j in range(k):
        v = [int(i == j) for i in range(k)]
        if rank(frame + [v]) > len(frame):
            frame.append(v)
            complement.append(v)
    need(len(frame) == k, 'frame completion failed')
    pivot = next(i for i, x in enumerate(ell) if x)
    pairing = [[dot(ell, conv(v, f)) for f in u] for v in complement]
    rows = []
    for i in range(c):
        for j in range(i, c):
            row = [x for h, x in enumerate(conv(u[i], u[j])) if h != pivot]
            for h in range(c):
                for t in range(k-c):
                    row.append(((pairing[t][j] if h == i else 0) + (pairing[t][i] if h == j else 0)) % P)
            rows.append(row)
    rw = rank(products(w)) if w else 0
    predicted = c*(c+1)//2 - len(w)*(len(w)+1)//2 + rw
    actual = rank(rows)
    need(actual == predicted, 'residual tangent rank mismatch')
    return {'k': k, 'c': c, 'product_rank': rank(products(u)), 'jacobian_rank': actual,
            'predicted_jacobian_rank': predicted, 'radical_intersection_dimension': len(w)}

def diagnostics() -> dict:
    expected = {(5,7,1,4,2),(5,8,1,6,3),(6,10,1,8,4),(6,11,1,10,5),(7,13,1,12,6)}
    ties, checks = set(), 0
    for c in range(4, 17):
        q = c*(c+1)//2
        for l in range(1, 7):
            for k in range(c+1, min(90, (l*q+1)//2)+1):
                a, b = l*q-2*k+2, l*c-3
                for r in range(1, k+1):
                    h = 2*r-1 if r < k else 2*k-2
                    for s in range(max(0,c-k+r), min(c,r//2)+1):
                        cost = l*((c-s)*(r-s)+s*(s+1)//2)-h
                        need(cost >= min(a,b), f'rank gap fails at {(c,k,l,r,s)}')
                        checks += 1
                        if cost == min(a,b) and (r,s) not in {(2,1),(k,c)}:
                            ties.add((c,k,l,r,s))
    need(ties == expected, f'exception list mismatch: {ties}')
    phase = []
    for m in range(2,9):
        for l in range(1,6):
            reps = {min(x, tuple(-i % m for i in x)) for x in itertools.product(range(m), repeat=l-1)}
            predicted = (m**(l-1)+math.gcd(m,2)**(l-1))//2
            need(len(reps) == predicted, 'phase orbit mismatch')
            phase.append([m,l,predicted])
    fibres = []
    for c in range(2,7):
        mon2 = list(itertools.product(range(c), repeat=2))
        rels = [{(i,i):1} for i in range(c)] + [{(i,j):1,(j,i):1} for i in range(c) for j in range(i+1,c)]
        rank2 = rank([[r.get(m,0) for m in mon2] for r in rels])
        mon3 = [(i,j,k) for i in range(c) for j in range(i,c) for k in range(c)]
        rows = []
        for rel in rels:
            for a in range(c):
                r3 = {}
                for (i,j),v in rel.items():
                    key = (*sorted((a,i)), j)
                    r3[key] = r3.get(key,0)+v
                rows.append([r3.get(m,0) for m in mon3])
        need(c*c-rank2 == c*(c-1)//2 and rank(rows) == len(mon3), 'fibre algebra mismatch')
        fibres.append({'c':c,'nilradical_dimension':c*c-rank2,'mixed_cubic_quotient_dimension':0})
    tangent = []
    for c,k,r,s in [(5,7,4,2),(5,8,6,3),(6,10,8,4),(6,11,10,5),(7,13,12,6),(7,14,14,7),(8,18,18,8),(4,5,2,1),(4,10,6,1)]:
        for seed in range(1,31):
            u,ell,w = isotropic(k,c,r,s,seed)
            if (c,k)==(4,10) or rank(products(u)) == 2*k-2:
                out = tangent_test(u,ell,w)
                out.update({'annihilator_rank':r,'seed':seed})
                tangent.append(out)
                break
        else:
            raise RuntimeError(f'no corank-one test frame at {(c,k,r,s)}')
    wall = None
    for seed in range(1,31):
        ku,eta,_ = isotropic(23,9,23,9,seed)
        if rank(products(ku)) != 44:
            continue
        rng = random.Random(1000+seed)
        g = [0,-1,1]
        w = [conv(g,f) for f in ku]
        av = conv(g,[rng.randrange(P) for _ in range(23)])
        av[0],av[1] = (av[0]-1)%P,(av[1]+2)%P
        u = w+[av]
        ell = [0]+[P-1]*48
        if rank(products(u)) != 48:
            continue
        wall = tangent_test(u,ell,w)
        wall.update({'residual_product_rank':44,'residual_target_dimension':45,'source_dimension':55,'expected_jacobian_rank':54,'seed':seed})
        need(wall['jacobian_rank']==54, 'wall Jacobian mismatch')
        break
    need(wall is not None, 'wall diagnostic did not find a frame')
    return {'kind':'finite diagnostics; not universal proofs','field_prime':P,
            'rank_cost_cases':checks,'rank_ranges':{'c':[4,16],'L':[1,6],'k_cap':90},
            'nonendpoint_ties':sorted(ties),'phase_counts':phase,'fibre_algebra':fibres,
            'tangent_examples':tangent,'wall_example':wall}

def source_checks() -> dict:
    git('merge-base','--is-ancestor',BASE,'HEAD')
    head = git('rev-parse','HEAD')
    changes = git('diff','--name-status',BASE,'HEAD').splitlines()
    permitted = {'A2_REVISION_V113_INDEX.md','.github/workflows/a2-v113-referee.yml'}
    for line in changes:
        fields = line.split('\t')
        need(fields[0]=='A' and (fields[1].startswith(PREFIX) or fields[1] in permitted), 'non-additive/out-of-scope change: '+line)
    old_texts = []
    for name, sha in BLOBS.items():
        path = HERE/'parts'/name
        need(path.exists(), 'missing retained part: '+name)
        data = path.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        need(actual==sha, 'retained blob changed: '+name)
        need(git('rev-parse',BASE+':'+OLD+'parts/'+name)==sha, 'baseline blob mismatch')
        old_texts.append(data.decode())
    old_refs = git('show',BASE+':'+OLD+'references.tex')
    inputs = re.findall(r'\\input\{([^}]+)\}',(HERE/'paper.tex').read_text())
    need(all((HERE/x).exists() for x in inputs),'missing input')
    texts = [(HERE/'paper.tex').read_text()] + [(HERE/x).read_text() for x in inputs]
    whole = '\n'.join(texts)
    labels = re.findall(r'\\label\{([^}]+)\}', whole)
    duplicates = [k for k,v in Counter(labels).items() if v>1]
    need(not duplicates, 'duplicate labels: '+str(duplicates))
    inherited = set(re.findall(r'\\label\{([^}]+)\}','\n'.join(old_texts)))
    need(inherited <= set(labels),'lost inherited labels')
    refs = set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', whole))
    need(refs <= set(labels),'undefined labels: '+str(refs-set(labels)))
    bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',whole))
    old_bib = set(re.findall(r'\\bibitem\{([^}]+)\}', old_refs))
    need(old_bib <= bib,'lost bibliography keys')
    cited = {x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',whole) for x in group.split(',')}
    need(cited <= bib,'undefined citations: '+str(cited-bib))
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',whole,re.S).group(1)
    need(len(abstract.split()) <= 200,'abstract exceeds 200 whitespace tokens')
    manifest = {str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(HERE.rglob('*')) if p.is_file() and 'evidence' not in p.relative_to(HERE).parts and p.suffix in {'.tex','.md','.py'}}
    return {'source_commit':head,'baseline_commit':BASE,'additions_only':True,'changed_file_count':len(changes),
            'retained_blobs':BLOBS,'retained_label_count':len(inherited),'label_count':len(labels),
            'inherited_bibliography_keys':len(old_bib),'bibliography_keys':len(bib),
            'abstract_whitespace_tokens':len(abstract.split()),'sha256':manifest}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--diagnostics-only',action='store_true')
    ap.add_argument('--source-only',action='store_true')
    ap.add_argument('--with-pdf',action='store_true')
    args = ap.parse_args()
    receipt = {'diagnostics':diagnostics()}
    if not args.diagnostics_only:
        receipt.update(source_checks())
    if args.with_pdf:
        pdf,log = HERE/'paper.pdf',HERE/'paper.log'
        need(pdf.exists() and pdf.read_bytes().startswith(b'%PDF-'),'no valid PDF')
        need(log.exists(),'missing TeX log')
        text = log.read_text(errors='replace')
        forbidden = ['There were undefined references','undefined citations','multiply defined','! LaTeX Error','! Undefined control sequence']
        need(not any(x in text for x in forbidden),'unresolved TeX errors/warnings')
        need(not re.search(r"(?:Reference|Citation) [`'].*?undefined",text),'undefined reference/citation')
        info = subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        receipt['pdf'] = {'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'bytes':pdf.stat().st_size,
                          'pages':int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1)),
                          'overfull_hbox_count':text.count('Overfull \\hbox'),
                          'latex_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
    out = json.dumps(receipt,indent=2,sort_keys=True)+'\n'
    print(out)
    if not args.diagnostics_only:
        evidence = HERE/'evidence'
        evidence.mkdir(exist_ok=True)
        (evidence/('BUILD_RECEIPT.json' if args.with_pdf else 'SOURCE_RECEIPT.json')).write_text(out)

if __name__ == '__main__':
    main()
