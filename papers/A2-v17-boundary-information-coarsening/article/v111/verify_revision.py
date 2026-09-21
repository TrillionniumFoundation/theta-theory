#!/usr/bin/env python3
"""Finite exact diagnostics and source/preservation checks, not a proof verifier.

Run: python3 verify_revision.py --out evidence/diagnostics.json
CI additionally passes --repository REPOSITORY_ROOT.
Dependency: sympy. Universal statements are proved in the manuscript.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import subprocess
from pathlib import Path
import sympy as sp

BASE = "043495e949f535554c5540c24b679b4aafa6a31d"
PREFIX = "papers/A2-v17-boundary-information-coarsening/article/v111/"
PRIME = 1000003


def rref(matrix: list[list[int]], prime: int = PRIME):
    a = [[v % prime for v in row] for row in matrix]
    if not a:
        return a, []
    pivots = []
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = pow(a[row][col], -1, prime)
        a[row] = [(v * scale) % prime for v in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [(x - scale * y) % prime for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    rr, piv = rref(a)
    width = len(a[0])
    columns = []
    for f in range(width):
        if f in piv:
            continue
        col = [0] * width
        col[f] = 1
        for i, p in enumerate(piv):
            col[p] = -rr[i][f] % PRIME
        columns.append(col)
    return [list(row) for row in zip(*columns)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) % PRIME
             for col in zip(*b)] for row in a]


def convolution(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def products(spaces):
    cols = []
    for space in spaces:
        frame = transpose(space)
        for i, f in enumerate(frame):
            for g in frame[i:]:
                cols.append(convolution(f, g))
    return transpose(cols)


def codimension_diagnostics():
    cases = strata = 0
    for k in range(5, 65):
        for c in range(4, k):
            q, p = c*(c+1)//2, 2*k-1
            for L in range(1, 7):
                if L*q < p:
                    continue
                target = min(L*q-p+1, L*c-3)
                candidates = []
                for r in range(1, k+1):
                    hr = 2*r-1 if r < k else 2*k-2
                    for s in range(max(0, c-k+r), min(c, r//2)+1):
                        D = (c-s)*(r-s) + s*(s+1)//2
                        value = L*D-hr
                        assert value >= target, (k,c,L,r,s,value,target)
                        candidates.append(value)
                        strata += 1
                # This stronger finite check is a diagnostic, not needed by the proof.
                assert min(candidates) == target, (k,c,L,min(candidates),target)
                cases += 1
    return {"parameter_cases": cases, "feasible_rank_strata": strata,
            "k_range": [5,64], "contacts_range": [1,6], "all_passed": True}


def generic_product_witnesses(rng):
    data = []
    for k,c,L in [(5,4,1),(7,5,1),(8,5,1),(10,6,1),(11,6,1),
                  (13,7,1),(9,4,2),(12,4,3),(16,4,4),(20,5,3)]:
        for attempt in range(100):
            spaces = [[[rng.randrange(-7,8) for _ in range(c)]
                       for _ in range(k)] for _ in range(L)]
            if all(rank(U)==c for U in spaces) and rank(products(spaces))==2*k-1:
                break
        else:
            raise AssertionError((k,c,L,"no witness found"))
        data.append({"k":k,"c":c,"L":L,"rank":2*k-1,"frames":spaces})
    return data


def native_witnesses(rng):
    data = []
    for k,d in [(7,2),(8,3),(10,4)]:
        roots = list(range(1,k+1))
        clocks = list(range(k+2,3*k+3))
        assert len(clocks)==2*k+1
        J = []
        for ri in roots:
            numerator = 1
            denominator = 1
            coeff = [1]
            for t in clocks:
                numerator = numerator*(ri-t) % PRIME
            for rj in roots:
                if rj != ri:
                    denominator = denominator*(ri-rj)**2 % PRIME
                    coeff = convolution(coeff, [-rj,1])
            scale = numerator*pow(denominator,-1,PRIME) % PRIME
            J.append([scale*v % PRIME for v in coeff])
        assert rank(J)==k
        for attempt in range(100):
            A = [[rng.randrange(1,8)] + [rng.randrange(-7,8) for _ in range(d-1)]
                 for _ in range(k)]
            if rank(A)!=d:
                continue
            tangent = [[row[0]*x for x in row] for row in A]
            normal = nullspace(transpose(tangent))
            U = multiply(transpose(J),normal)
            if rank(products([U])) != 2*k-1:
                continue
            passed = True
            for mask in range(1,1 << (k-1)):
                signs = [1]+[-1 if mask & (1 << (i-1)) else 1 for i in range(1,k)]
                augmented = [row+[sign*row[0]] for row,sign in zip(A,signs)]
                if rank(augmented) != d+1:
                    passed = False
                    break
            if passed:
                break
        else:
            raise AssertionError((k,d,"no separated native witness"))
        data.append({"k":k,"d":d,"A":A,"roots":roots,"clocks":clocks,
                     "product_rank":2*k-1,"nonconstant_sign_tests":(1 << (k-1))-1})
    return data


def secant_witness(rng):
    k,c,x,y = 9,6,10,11
    hv = [x**j+2*y**j for j in range(k)]
    basis = [[(-hv[j] if i==0 else 3 if i==j else 0)
              for j in range(1,k)] for i in range(k)]
    for _ in range(100):
        mixing = [[rng.randrange(-4,5) for _ in range(c)] for _ in range(k-1)]
        # Keep integer coefficients, not residues, for exact evaluation identities.
        U = [[sum(a*b for a,b in zip(row,col)) for col in zip(*mixing)] for row in basis]
        if rank(U)==c and rank(products([U]))==2*k-2:
            break
    else:
        raise AssertionError("no corank-one secant witness")
    values = []
    for f in transpose(U):
        fx = sum(v*x**i for i,v in enumerate(f))
        fy = sum(v*y**i for i,v in enumerate(f))
        assert fx+2*fy == 0
        values.append((fx,fy))
    for fx,fy in values:
        for gx,gy in values:
            assert fx*gx-4*fy*gy == 0
    return {"k":k,"c":c,"x":x,"y":y,"frame":U,
            "exact_annihilator_weights":[1,-4],"exact_rank":2*k-2,
            "rank_justification":"integer annihilator upper bound plus modular lower bound"}


def statistical_identities():
    D = sp.Matrix([[1,0,1,2,-1],[0,1,2,-1,1],[1,1,0,1,2]])
    Lam = sp.diag(1,2,3,4,5)
    Sigma = D*Lam*D.T
    B = Lam*D.T*Sigma.inv()
    assert D*B == sp.eye(3)
    assert B.T*Lam.inv()*B == Sigma.inv()
    residual = Lam-Lam*D.T*Sigma.inv()*D*Lam
    assert D*residual == sp.zeros(3,5)
    full = sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0]])
    bad = sp.Matrix([[1,2,0],[0,1,1]])
    for L, expected in [(full,3),(bad,2)]:
        info = L.T*(L*Sigma*L.T).pinv()*L
        assert info.rank()==expected
        assert info*Sigma*info==info
        assert info.nullspace()==L.nullspace()
        if expected==3:
            assert info==Sigma.inv()
    O = sp.Matrix([[1,1,0],[0,2,1],[0,0,1]])
    K = O.T*O
    G = O.T*Sigma.inv()*O
    assert K*G.inv()*K == O.T*Sigma*O
    H = sp.Matrix([[2,1,0,1],[1,3,1,0],[0,1,2,1],[1,0,1,3]])
    I = H.T*H+sp.eye(4)
    Iuu,Iuv,Ivu,Ivv = I[:2,:2],I[:2,2:],I[2:,:2],I[2:,2:]
    Q = Ivv-Ivu*Iuu.inv()*Iuv
    E = (-Ivu*Iuu.inv()).row_join(sp.eye(2))
    assert E*I*E.T==Q
    assert E*I[:,:2]==sp.zeros(2,2)
    return {"exact_rational_checks":10,"all_passed":True,
            "scope":"matrix identities only, not simulation or proof of an asymptotic theorem"}


def preservation(repo: Path | None):
    if repo is None:
        return {"status":"not_run_no_repository", "base":BASE}
    def git(*args):
        return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()
    head = git("rev-parse","HEAD")
    changed = git("diff","--name-status",BASE,head).splitlines()
    allowed_other = {"A2_REVISION_V111_INDEX.md", ".github/workflows/a2-v111-verify.yml"}
    for line in changed:
        status,path = line.split("\t",1)
        assert status=="A", ("inherited modification",line)
        assert path.startswith(PREFIX) or path in allowed_other, ("unexpected path",path)
    pins = {
        "article/v110/paper.tex":"51c9ab6b56035f97356870e82734d116980451b9",
        "article/v109/paper.tex":"1ec9ddd8cfc54d96902f29ccd4221225178ce142",
        "article/v108/paper.tex":"2d364b96f3753c49d233d8140fb0335857443683",
        "article/v104/parts/05-experiment.tex":"d143a906ea38283ea3ec6342f35c0948c820c6d8",
    }
    for path,expected in pins.items():
        actual=git("rev-parse",head+":papers/A2-v17-boundary-information-coarsening/"+path)
        assert actual==expected,(path,actual,expected)
    return {"status":"passed","base":BASE,"head":head,
            "added_paths":len(changed),"modified_or_deleted_inherited_paths":0,"pins":pins}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=Path("evidence/diagnostics.json"))
    parser.add_argument("--repository",type=Path)
    args=parser.parse_args()
    rng=random.Random(20260921)
    root=Path(__file__).resolve().parent
    sources={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob("*.tex"))}
    report={"status":"passed","prime":PRIME,"seed":20260921,
            "warning":"Finite diagnostics do not certify universal proofs or journal-level novelty.",
            "codimension":codimension_diagnostics(),
            "generic_product_witnesses":generic_product_witnesses(rng),
            "native_witnesses":native_witnesses(rng),
            "secant_witness":secant_witness(rng),
            "statistical_identities":statistical_identities(),
            "preservation":preservation(args.repository),"tex_sha256":sources}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"codimension":report["codimension"],
                      "product_witnesses":len(report["generic_product_witnesses"]),
                      "native_witnesses":len(report["native_witnesses"]),
                      "secant_rank":report["secant_witness"]["exact_rank"],
                      "preservation":report["preservation"]["status"]},indent=2))


if __name__=="__main__":
    main()
