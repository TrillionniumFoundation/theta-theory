#!/usr/bin/env python3
"""Source integrity and finite exact stress tests; not universal proof verification."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import random
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "cafc6c1bd403dae4acc66177fb43feee54c02b1d"
PREFIX = "papers/A2-v17-boundary-information-coarsening/article/v112/"
SPEC = importlib.util.spec_from_file_location("a2_v111_diagnostics", ROOT.parent / "v111" / "verify_revision.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("The immutable sibling v111 diagnostic module is required")
OLD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OLD)
PRIME = OLD.PRIME
rank, products, nullspace = OLD.rank, OLD.products, OLD.nullspace
multiply, transpose, convolution = OLD.multiply, OLD.transpose, OLD.convolution

def structural_diagnostics():
    cases = strata = 0
    for c in range(8,25):
        for k in range(2*c+1,97):
            for L in range(1,7):
                q,p=c*(c+1)//2,2*k-1
                if L*q<p:
                    continue
                a,b=L*q-p+1,L*c-3
                assert a-b==L*c*(c-1)//2-(2*k-5)
                cases += 1
                for r in range(1,k+1):
                    for s in range(max(0,c-k+r), min(c,r//2)+1):
                        D=(c-s)*(r-s)+s*(s+1)//2
                        h=2*r-1 if r<k else 2*k-2
                        val=L*D-h
                        if (r,s)==(2,1):
                            assert val==b
                        elif (r,s)==(k,c):
                            assert val==a
                        else:
                            assert val>min(a,b),(c,k,L,r,s,val,a,b)
                        strata += 1
    return {"stable_parameter_cases":cases,"strict_gap_strata":strata,
            "ranges":{"c":[8,24],"k":["2c+1",96],"L":[1,6]},
            "universal_proof":"Lemma 5.2, not this enumeration"}


def signed_tangent_diagnostics(rng):
    out=[]
    for k,c,signs in [(25,10,[1]),(17,8,[1,1]),(17,8,[1,-1]),(19,8,[1,-1])]:
        L=len(signs);p=2*k-1;q=c*(c+1)//2
        a,b=L*q-p+1,L*c-3
        assert a>=b
        for attempt in range(100):
            spaces=[]
            for sign in signs:
                # x=0, y=1, t=2. Integer frames in the prescribed signed hyperplane.
                hv=[(1 if j==0 else 0)+2*sign for j in range(k)]
                basis=[[(-hv[j] if i==0 else hv[0] if i==j else 0)
                        for j in range(1,k)] for i in range(k)]
                mix=[[rng.randrange(-5,6) for _ in range(c)] for _ in range(k-1)]
                U=[[sum(x*y for x,y in zip(row,col)) for col in zip(*mix)] for row in basis]
                spaces.append(U)
            if any(rank(U)!=c for U in spaces) or rank(products(spaces))!=p-1:
                continue
            residual=[]
            for U in spaces:
                W=multiply(U,nullspace([U[0]]))
                residual.append(W)
            if rank(products(residual))==p-4:
                break
        else:
            raise AssertionError("no signed witness")
        jac=[]
        for nu,U in enumerate(spaces):
            columns=transpose(U)
            for i,f in enumerate(columns):
                for j in range(i,c):
                    g=columns[j]
                    # Derivatives in affine ell and full frames; subtract one scaling and L*c*c gauges.
                    row=convolution(f,g)+[0]*(L*k*c)
                    Hf=[(f[0] if z==0 else 0)-4*sum(f) for z in range(k)]
                    Hg=[(g[0] if z==0 else 0)-4*sum(g) for z in range(k)]
                    assert f[0]*g[0]-4*sum(f)*sum(g)==0
                    for z in range(k):
                        row[p+nu*k*c+i*k+z]+=Hg[z]
                        row[p+nu*k*c+j*k+z]+=Hf[z]
                    jac.append(row)
        jr=rank(jac)
        assert jr==p-1+b,(k,c,signs,jr,p-1+b)
        dim=p+L*k*c-jr-1-L*c*c
        assert dim==L*c*(k-c)-b
        out.append({"k":k,"c":c,"signs":signs,"a":a,"b":b,
                    "product_rank":p-1,"residual_product_rank":p-4,
                    "incidence_jacobian_rank_mod_prime":jr,"scheme_tangent_dimension":dim,
                    "integer_frames":spaces})
    return out


def label_preservation(root):
    prior=root.parent/'v111'
    old='\n'.join(p.read_text() for p in prior.rglob('*.tex'))
    new='\n'.join(p.read_text() for p in root.rglob('*.tex'))
    labels=lambda text:set(re.findall(r'\\label\{([^}]+)\}',text))
    removed=labels(old)-labels(new)
    assert not removed,sorted(removed)
    exact=[]
    for name in ('02-global-geometry.tex','03-realization-stability.tex','05-complements.tex'):
        assert (prior/'parts'/name).read_bytes()==(root/'parts'/name).read_bytes()
        exact.append(name)
    return {"inherited_labels_retained":len(labels(old)),"new_labels":len(labels(new)-labels(old)),
            "removed_labels":[],"byte_identical_parts":exact}


def preservation(repo: Path | None):
    if repo is None:
        return {"status":"not_run_no_repository", "base":BASE}
    def git(*args):
        return subprocess.check_output(["git","-C",str(repo),*args],text=True).strip()
    head = git("rev-parse","HEAD")
    changed = git("diff","--name-status",BASE,head).splitlines()
    allowed_other = {"A2_REVISION_V112_INDEX.md", ".github/workflows/a2-v112-verify.yml"}
    for line in changed:
        status,path = line.split("\t",1)
        assert status=="A", ("inherited modification",line)
        assert path.startswith(PREFIX) or path in allowed_other, ("unexpected path",path)
    pins = {
        "article/v111/paper.tex":"a491bc71bd9114a349bbdfb69765fb028b23047b",
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("evidence/diagnostics.json"))
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    rng = random.Random(20260921)
    sources = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(ROOT.rglob("*.tex"))}
    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text())
    assert sources == manifest["tex_sha256"], "Mathematical input manifest mismatch"
    report = {"status":"passed", "prime":PRIME, "seed":20260921,
              "warning":"Finite diagnostics do not certify universal proofs or journal-level novelty.",
              "codimension":OLD.codimension_diagnostics(),
              "structural":structural_diagnostics(),
              "signed_tangents":signed_tangent_diagnostics(rng),
              "label_preservation":label_preservation(ROOT),
              "generic_product_witnesses":OLD.generic_product_witnesses(rng),
              "native_witnesses":OLD.native_witnesses(rng),
              "secant_witness":OLD.secant_witness(rng),
              "statistical_identities":OLD.statistical_identities(),
              "preservation":preservation(args.repository), "tex_sha256":sources,
              "manifest_checked":True}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"], "codimension":report["codimension"],
                      "structural":report["structural"],
                      "signed_tangent_examples":len(report["signed_tangents"]),
                      "preservation":report["preservation"]["status"]},indent=2))

if __name__ == "__main__":
    main()
