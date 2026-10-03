#!/usr/bin/env python3
"""Exact finite diagnostics and source-retention checks, not a proof certificate.
Standard library only. Checks remain active under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
from v12_finite_block_reference import finite_block_row, sh, ch

ROOT = Path(__file__).resolve().parents[1]
CHECKS = []

def check(name, condition, kind="exact_algebra"):
    if not condition:
        raise RuntimeError("Failed: " + name)
    CHECKS.append({"name": name, "kind": kind, "status": "pass"})

def sha(data):
    return hashlib.sha256(data).hexdigest()

def block(c0, c1, g, m):
    z = c0*c1-1
    scales = [g/(2*c0*z), g/(2*c1*z)]
    k = F(4, 2**m*(m+1)*math.factorial(m)**2)
    U, V = (1+2*z)**m, 1+2*m*z
    return [[-U*k*scales[0]**m, -V*k*scales[1]**m],
            [-V*k*scales[0]**m, -U*k*scales[1]**m]]

def schur_row(c0, c1, g, m, b):
    cb, co = [c0, c1][b], [c0, c1][1-b]
    h = (cb-F(1, 2)/co)/g
    off = -F(1, 2)/(co*g)
    det = h*h-off*off
    inv00, inv01 = h/det, -off/det
    vu = inv00
    vw = (inv00+inv01)/(2*co*co)
    k = F(4, 2**m*(m+1)*math.factorial(m)**2)
    own = -k*vu**m
    other_action = -k*vw**m
    other_twist = -(g/co)*F(4, 2**m*(m+1)*math.factorial(m)*math.factorial(m-1))*vw**(m-1)
    row = [F(0), F(0)]
    row[b], row[1-b] = own, other_action+other_twist
    return row, det, vu, vw

def sources(rel="main.tex", stack=()):
    if rel in stack:
        raise RuntimeError("Input cycle: " + rel)
    text = (ROOT/rel).read_text()
    out = [(rel, text)]
    for name in re.findall(r"\\input\{([^}]+)\}", text):
        out += sources(name+".tex", stack+(rel,))
    return out

PATTERN = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}", re.S)

def run():
    for c0 in [F(11,10), F(3,2), F(2), F(4)]:
        for c1 in [F(11,10), F(3,2), F(2), F(4)]:
            for g in [F(1,2), F(1), F(3,2)]:
                z = c0*c1-1
                for m in range(2,11):
                    tag = f"{c0}_{c1}_{g}_{m}"
                    U, V = (1+2*z)**m, 1+2*m*z
                    mat = block(c0, c1, g, m)
                    check("binomial_separation_"+tag, U-V == sum(F(math.comb(m,r))*(2*z)**r for r in range(2,m+1)) > 0)
                    check("positive_determinant_"+tag, mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0] > 0)
                    for b in (0,1):
                        row, det, vu, vw = schur_row(c0,c1,g,m,b)
                        cb, co = [c0,c1][b], [c0,c1][1-b]
                        check(f"schur_action_twist_{tag}_{b}", row == mat[b])
                        check(f"ellipse_scales_{tag}_{b}", det == cb*z/(co*g*g) and vu == g*(1+2*z)/(2*cb*z) and vw == g/(2*co*z))
                    # Direct inversion checks column scaling as well as signs.
                    a,b = mat[0];c,d = mat[1];det=a*d-b*c
                    inverse = [[d/det,-b/det],[-c/det,a/det]]
                    check("inverse_"+tag, all(sum(inverse[i][k]*mat[k][j] for k in (0,1)) == int(i==j) for i in (0,1) for j in (0,1)))
    reference_count = 0
    for lam in [F(1,3), F(1,2), F(2,3), F(4,5)]:
        c = ch(lam,1)
        for r in [F(1), (c+1)/2, 2/(c+1)]:
            for g in [F(1),F(3,2)]:
                c0,c1=c*r,c/r
                check(f"reference_physical_{lam}_{r}_{g}", c0>1 and c1>1)
                for m in range(2,11):
                    target=block(c0,c1,g,m)
                    actual=[finite_block_row(lam,r,g,m,2,b) for b in (0,1)]
                    check(f"v12_routine_at_two_flights_{lam}_{r}_{g}_{m}",actual==target,"prior_routine_crosscheck")
                    reference_count += 1
    check("disk_normalization", block(F(2),F(2),F(1),2) == [[-F(49,1728),-F(13,1728)],[-F(13,1728),-F(49,1728)]])
    for n in range(1,13):
        determinant = math.prod(range(1,n+1))*math.prod(j-i for i in range(1,n+1) for j in range(i+1,n+1))
        check(f"positive_window_vandermonde_{n}",determinant>0)
    for m in range(4,13):
        nu=F(m)-F(1,2)
        check(f"retained_flux_rate_{m}",2+F(6)/nu > 2+F(2,m))
    check("retained_m4_power",2+F(6)/(F(4)-F(1,2))==F(26,7))
    active=sources();names=[n for n,_ in active];text="\n".join(t for _,t in active)
    check("unique_inputs",len(names)==len(set(names)),"source_integrity")
    check("valid_control_characters",all(ord(c)>=32 or c in "\n\r\t" for c in text),"source_integrity")
    baseline=json.loads((ROOT/"history/v12-active-blocks.json").read_text())
    hashes=[sha(m.group(0).encode()) for _,s in active for m in PATTERN.finditer(s)]
    old_hashes=[sha(m.group(0).encode()) for name,s in active if name in baseline["inputs"] for m in PATTERN.finditer(s)]
    digest=sha(("\n".join(sorted(old_hashes))+"\n").encode())
    check("all_212_reviewed_blocks_retained",baseline["block_count"]==len(old_hashes)==212 and digest==baseline["sorted_block_multiset_sha256"],"source_integrity")
    check("all_reviewed_inputs_retained",set(baseline["inputs"])<=set(names),"source_integrity")
    labels=re.findall(r"\\label\{([^}]+)\}",text)
    check("unique_labels",len(labels)==len(set(labels)),"source_integrity")
    refs=re.findall(r"\\(?:ref|eqref)\{([^}]+)\}",text)
    check("resolved_references",all(r in labels or r.startswith("TC-") for r in refs),"source_integrity")
    keys=set(re.findall(r"\\bibitem\{([^}]+)\}",text))
    cites={k.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",text) for k in group.split(",")}
    check("resolved_citations",cites<=keys,"source_integrity")
    check("main_results_present",{"thm:v13-two-flight","cor:v13-jet-coordinates","thm:v13-two-flight-observation","thm:v8-main-relative","thm:v12-self-calibrated"}<=set(labels),"source_integrity")
    retained={rel:sha((ROOT/rel).read_bytes()) for rel in names if rel not in {"main.tex","article/01_introduction.tex","v5/references.tex","article/29_two_flight_benchmark.tex"}}
    return {"schema":"a2-v13-diagnostics-v1","status":"pass","counts":{"total":len(CHECKS),**dict(Counter(c["kind"] for c in CHECKS))},"checks":CHECKS,
        "reference_comparisons":reference_count,"retention":{"reviewed_blocks":212,"active_blocks":len(hashes),"all_reviewed_blocks_byte_identical":True,"active_inputs":len(names)},
        "active_retained_file_sha256":retained,
        "limitations":["Finite exact algebra is not a formal proof certificate.","The inherited v12 routine is tested at j=2; no nonlinear billiard simulation is claimed.","No increasing-order conditioning or full-profile minimax assertion is made.","Local compilation and tests are not a remote CI run."]}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=ROOT/"verification/v13.normal.json")
    args=parser.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","counts","retention","reference_comparisons")},sort_keys=True))
