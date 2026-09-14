#!/usr/bin/env python3
"""Independent finite checks for the A2 v47 referee report.

No author diagnostic is imported. Exact rational checks are finite functional
negative controls, not billiard realizations or a proof certificate. Optional
artifact auditing needs PyMuPDF and the extracted native-source archive.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def finite_checks() -> dict:
    # In radial-area coordinate z=|x|^2, the quadratic cap has density
    # 2(d-z)/d^2 on [0,d]. The CDF is 2z/d-z^2/d^2.
    cases = 0
    for i in range(1, 21):
        for j in range(1, 16):
            d, D = F(i, 7), F(i, 7) + F(j, 11)
            crossing = d * D / (d + D)
            cdf_d = 2 * crossing / d - crossing**2 / d**2
            cdf_D = 2 * crossing / D - crossing**2 / D**2
            require(cdf_d - cdf_D == (D-d)/(D+d), "Offset TV identity")
            cases += 1
    d, err, J = F(1), F(1, 10000), 100
    tv_amplified = J*err/(2*d+J*err)
    tv_unamplified = err/(2*d+err)
    require(tv_amplified > 90*tv_unamplified, "Timing negative control")

    # The exact sup-norm tube area for the grid on [-r1,r1]^2:
    # an expanded outer square minus q^2 eroded cell interiors.
    tube_cases = 0
    for q in range(1, 101):
        r1 = F(3, 2)
        delta = 2*r1/q
        for r in (F(0), delta/20, delta/3, delta, 2*r1):
            exact = (2*r1+2*r)**2 - q*q*max(F(0), delta-2*r)**2
            upper = 8*r*(r1+r)*(q+1)
            require(F(0) <= exact <= upper, "Grid-tube bound")
            tube_cases += 1

    # Refining-grid negative control: P uniform on [0,1]^2. Map each
    # odd vertical column left by delta, leaving even columns unchanged.
    # This pairs columns, gives displacement delta->0, and vector L1=1.
    refinement = []
    for q in (2, 4, 16, 64, 256):
        delta = F(1,q)
        column_masses = [F(0) for _ in range(q)]
        for column in range(q):
            target = column - 1 if column % 2 else column
            column_masses[target] += F(1, q)
        vector_l1 = sum(abs(mass - F(1, q)) for mass in column_masses)
        require(vector_l1 == 1, "Refining-grid control")
        refinement.append({"q": q, "max_displacement": str(delta), "vector_l1": str(vector_l1)})
    # q=1: a right translation of uniform measure on the unit square
    # crosses only its outer edge, so removing outer edges predicts zero.
    r = F(1,100)
    outer_edge_l1 = 2*r
    require(outer_edge_l1 > 0, "Outer-edge negative control")
    # q=2: collapse x in [1/2-r,1/2) onto x=1/2 (right half-open cell).
    # This creates singular image mass on an edge, yet L1=2r.
    edge_atom_l1 = 2*r
    require(edge_atom_l1 <= 2 * (8*r*(F(1,2)+r)*3), "Edge-atom bound")

    # Exact budget check with synthetic constants, not a realized table.
    eta, e, a, h0 = F(1,10), F(1,50), F(1,4), F(1,8)
    Cbin, r1, Cchi, Hoff, Hstar, C0, tau = F(1), F(1), F(2), F(2), F(3), F(1), F(1,2)
    q = max(1, math.ceil(8*Cbin*r1/eta))
    delta = 2*r1/q
    J = 2
    while 2*C0*tau**J > eta/32:
        J += 2
    hs = [h0/2, a/2, J*e/4, eta/(64*Hoff), (r1/Cchi)**2,
          (eta/(1024*Hstar*r1*(q+1)*Cchi))**2]
    h = min(hs)
    sn, sd = math.isqrt(h.numerator), math.isqrt(h.denominator)
    require(sn*sn == h.numerator and sd*sd == h.denominator, "Synthetic square resolution")
    r = Cchi*F(sn,sd)
    vg = h/J
    bf = 2*C0*tau**J
    bo = 2*Hoff*h
    bc = 2*Hstar*8*r*(r1+r)*(q+1)
    require(Cbin*delta <= eta/4, "Mesh budget")
    require(bf <= eta/32 and bo <= eta/32 and bc <= eta/32, "Bias budget")
    require(2*vg <= e/2 and h <= a, "Gap/offset budget")
    eps_sel = min(e/2,eta/4)
    probability_argument = 2*(eta/8+bf+bo+bc)+Cbin*delta+eps_sel
    require(probability_argument <= 15*eta/16 < eta, "Joint probability budget")
    require(2*vg+eps_sel <= e, "Joint gap budget")
    groups, alpha = 6, 0.05
    K = q*q+1
    n = math.ceil(64/float(eta)**2 * (math.sqrt(K)+math.sqrt(2*math.log(groups/alpha)))**2)
    un = math.sqrt(K/n)+math.sqrt(2*math.log(groups/alpha)/n)
    require(un <= float(eta/8)*(1+1e-14), "Sample-size check")
    # Finite cap algebra: mean >= 2n+8 log(L/alpha_c), so exp(-mean/8)
    # <= alpha_c/L and n <= mean/2.
    alpha_c, pstar = 0.025, 0.003
    cap = math.ceil((2*n+8*math.log(groups/alpha_c))/pstar)
    mu = cap*pstar
    require(n <= mu/2 and -mu/8 <= math.log(alpha_c/groups), "Cap check")
    return {
        "status": "passed", "offset_exact_cases": cases, "tube_exact_cases": tube_cases,
        "timing_control": {"true_tv": str(tv_amplified), "unamplified_tv": str(tv_unamplified)},
        "refining_grid_control": refinement, "outer_edge_vector_l1": str(outer_edge_l1),
        "edge_atom_vector_l1": str(edge_atom_l1),
        "synthetic_budget": {"q": q, "J": J, "h": str(h), "n": n,
          "probability_argument": str(probability_argument), "eta": str(eta),
          "successful_sampling_bound": format(un,'.15g')},
        "scope": "Finite identities and functional controls only; no billiard realization, optimal-rate claim, or formal proof certificate."
    }


def audit(native: Path, source: Path, rebuilt: Path | None, archive: Path | None) -> dict:
    report = json.loads((native/'build-report.json').read_text())
    for rel, expected in report['evidence_files'].items():
        data = (native/rel).read_bytes()
        require(len(data)==expected['bytes'] and digest(data)==expected['sha256'], f"Evidence mismatch: {rel}")
    require(digest((native/'native-source.zip').read_bytes()) == report['source_archive_sha256'], "Source ZIP hash")
    manifest = json.loads((native/'active-source-manifest.json').read_text())
    unique = {}
    for entries in manifest.values():
        for rel, expected in entries.items():
            if rel in unique:
                require(unique[rel]==expected, f"Conflicting entry: {rel}")
            unique[rel]=expected
    for rel, expected in unique.items():
        data = (source/rel).read_bytes()
        require(len(data)==expected['bytes'] and digest(data)==expected['sha256'] and blob(data)==expected['git_blob'], f"Active input mismatch: {rel}")
    result = {"evidence_entries_verified":len(report['evidence_files']),
              "unique_active_inputs_verified":len(unique), "source_commit":report['source_commit'],
              "source_zip_sha256":digest((native/'native-source.zip').read_bytes())}
    if archive is not None:
        result['artifact_zip_sha256']=digest(archive.read_bytes())
    if rebuilt is not None:
        import fitz
        products = {}
        for name in ('main','two_collision'):
            pa, pb = native/f'{name}.pdf', rebuilt/f'{name}.pdf'
            da, db = fitz.open(pa), fitz.open(pb)
            require(len(da)==len(db), f"Page count mismatch: {name}")
            text_mismatch, pixel_mismatch = [], []
            for i in range(len(da)):
                if da[i].get_text()!=db[i].get_text(): text_mismatch.append(i+1)
                aa,bb=da[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False),db[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
                if (aa.width,aa.height,aa.samples)!=(bb.width,bb.height,bb.samples): pixel_mismatch.append(i+1)
            products[name]={"pages":len(da),"native_sha256":digest(pa.read_bytes()),
                "rebuilt_sha256":digest(pb.read_bytes()),"text_mismatch_pages":text_mismatch,
                "pixel_mismatch_pages_72dpi":pixel_mismatch}
            require(not text_mismatch and not pixel_mismatch, f"Content mismatch: {name}")
        result['products']=products
    result['status']='passed'
    result['scope']='Byte/provenance and reproduction checks only; pixel agreement is not individual visual inspection.'
    return result


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',type=Path)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--rebuilt',type=Path)
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    result={'finite_checks':finite_checks()}
    if args.native or args.source:
        require(args.native is not None and args.source is not None, 'Both --native and --source are required')
        result['artifact_audit']=audit(args.native,args.source,args.rebuilt,args.archive)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
