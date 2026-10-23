#!/usr/bin/env python3
"""Exact auxiliary checks for native341. No simulated orbit is a proof."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import re
import tarfile

def qtext(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def pv(i, n=9):
    e=[0]*n; e[i]=1
    return {tuple(e): Q(1)}

def pa(*args):
    out={}
    for p in args:
        for e,a in p.items(): out[e]=out.get(e,Q(0))+a
    return {e:a for e,a in out.items() if a}

def pm(*args):
    out={(0,)*9:Q(1)}
    for p in args:
        nxt={}
        for e,a in out.items():
            for f,b in p.items():
                ef=tuple(x+y for x,y in zip(e,f))
                nxt[ef]=nxt.get(ef,Q(0))+a*b
        out={e:a for e,a in nxt.items() if a}
    return out

def ps(a,p):
    return {e:a*v for e,v in p.items() if a*v}

def matmul(a,b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(2)),Q(0))
                       for j in range(2)) for i in range(2))

def run(source,draft):
    Rmax=Q(47,100); tau=Q(3,50); kmin=Q(100,47); U=Q(170,9)
    ccap_sq=Q(19,100); sig=Q(47,59); E=Q(47,6)
    Qsq=U*U/(ccap_sq*kmin*kmin)
    assert Qsq==Q(799*799,81*19)
    foot_sq=(1-Rmax)**2-Rmax**2
    assert foot_sq==Q(3,50) and foot_sq>tau*tau

    # Formal polynomial certificate of the backward sign, after multiplying
    # both expressions by positive Kminus*Kplus.
    R,c0,cm,Vm,Vp,dalpha0,dalpham,p0,pend=[pv(i) for i in range(9)]
    Km=pm(c0,Vm); Kp=pm(cm,Vp)
    dp0=ps(Q(-1),pm(R,c0,Vm,dalpha0))
    dpend=pm(R,cm,Vp,dalpham)
    direct=pm(pa(ps(Q(-1),pm(R,p0,dalpha0)),pm(R,pend,dalpham)),Km,Kp)
    balance=pa(pm(p0,dp0,Kp),pm(pend,dpend,Km))
    assert direct==balance
    wrong_backward=pa(ps(Q(-1),pm(p0,dp0,Kp)),pm(pend,dpend,Km))
    assert direct!=wrong_backward

    # Exact finite checks of the general interval-overlay inequality, including
    # its TRUNCATED weights. These are abstract intervals, not billiard data.
    rng=random.Random(341)
    grid=[Q(i,12) for i in range(1,12)]
    overlay_cases=0
    for case in range(600):
        ca=sorted([Q(0),Q(1)]+rng.sample(grid,rng.randint(0,9)))
        cb=sorted([Q(0),Q(1)]+rng.sample(grid,rng.randint(0,9)))
        ia=list(zip(ca[:-1],ca[1:])); jb=list(zip(cb[:-1],cb[1:]))
        aw=[Q(rng.randint(1,20),20*len(ia)) for _ in ia]
        bw=[Q(rng.randint(1,20),20*len(jb)) for _ in jb]
        eta=Q(rng.randint(1,24),24)
        atr=[min(a,eta) for a in aw]
        overlays=[(i,j) for i,I in enumerate(ia) for j,J in enumerate(jb)
                  if max(I[0],J[0])<min(I[1],J[1])]
        original=sum((aw[i]*bw[j] for i,j in overlays),Q(0))
        truncated=sum((atr[i]*bw[j] for i,j in overlays),Q(0))
        generic=max(bw)*sum(aw)+max(aw)*sum(bw)
        trunc_rhs=max(bw)*sum(atr)+max(atr)*sum(bw)
        assert original<=generic
        assert truncated<=trunc_rhs
        assert trunc_rhs<=max(bw)*sum(aw)+eta*sum(bw)
        overlay_cases+=1
    # Pointwise a(v)<=eta does not imply sup_I a<=eta. With a(v)=v,
    # I=(0,1), eta=1/2, the selected weighted integral is 1/8, not zero.
    pointwise_selected_integral=Q(1,8)
    assert pointwise_selected_integral>0
    assert min(Q(1),Q(1,2))==Q(1,2)

    index_pairs=0
    for m in range(2,257):
        for i in range(1,m):
            L=max(i,m-i); s=min(i,m-i)
            eps=E*sig**(L-1); As=E*sig**(s-1)
            eta_sq=E*eps
            assert 0<eps<=E and 0<As<=E
            assert eps*eps<=eta_sq  # eps <= sqrt(E eps)
            assert eps*(eps+As)<=2*E*eps
            assert 2*(L-1)>=m-2
            # The final root factor is sqrt(E eps)=E sigma^((L-1)/2).
            assert eta_sq==E*E*sig**(L-1)
            index_pairs+=1

    # Actual optical matrix formulas are inherited277/324. This finite rational
    # check catches sign/determinant errors in the reused physical formulas.
    matrix_cases=0
    for source_kind in ("horizontal","vertical"):
        for incidence in (Q(1,5),Q(3,5),Q(1)):
            seed=(Rmax*incidence,Q(1)) if source_kind=="horizontal" else (Q(0),Q(1))
            M=((Q(1),Q(0)),(Q(0),Q(1)))
            for count in range(1,25):
                P=((Q(1),tau),(Q(0),Q(1)))
                K=((Q(1),Q(0)),(2/(Rmax*incidence),Q(1)))
                M=matmul(P,M)
                B=M[0][0]*seed[0]+M[0][1]*seed[1]
                D=M[1][0]*seed[0]+M[1][1]*seed[1]
                assert B>0 and D>0
                assert M[0][0]*M[1][1]-M[0][1]*M[1][0]==1
                M=matmul(K,M)
                matrix_cases+=1

    # Counterexample to an UNUSED inference: strict convexity + separated
    # half actions + arbitrarily small twist do not exclude isoroof arcs.
    # S-=x^2-delta*t*sqrt(1-x^2)+2t^2,
    # S+=z^2+delta*t*z+2t^2, delta in (0,1].
    # At t=0, S_t=delta(z-sqrt(1-x^2)), S=1 on z=sqrt(1-x^2).
    # On x in [2/5,3/5], |t|<=1/10, the following exact lower bounds
    # give positive half and full Hessians for all delta in (0,1].
    hxx_lower=Q(2)-Q(1,10)/Q(4,5)**3
    mixed_square_upper=Q(3,4)**2
    left_det_lower=4*hxx_lower-mixed_square_upper
    right_det_lower=Q(8)-1
    full_schur_lower=8-mixed_square_upper/hxx_lower-Q(1,2)
    assert hxx_lower==Q(231,128)
    assert left_det_lower==Q(213,32)>0
    assert right_det_lower==7
    assert full_schur_lower==Q(1107,154)>0

    # Two labels are distinct probability-mass traces, so their full l1 jump
    # is two. A bound of one would silently lose a physical trace.
    signed_label_jump=abs(Q(1)-0)+abs(0-Q(1))
    assert signed_label_jump==2

    inherited={}
    for prefix in ("277","281","283","284","317","319","323","324","336"):
        choices=sorted((source/"core").glob(prefix+"_*.tex"))
        assert len(choices)==1, (prefix,choices)
        p=choices[0]; data=p.read_bytes()
        inherited[prefix]={"path":str(p.relative_to(source)),"git_blob":blob(data),
                           "sha256":hashlib.sha256(data).hexdigest()}
    archive=source/"history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz"
    raw=archive.read_bytes(); seen={}; close=[]; roof_candidates=[]
    with tarfile.open(archive,"r:gz") as tf:
        for item in tf:
            if not item.isfile() or not item.name.endswith(".tex"): continue
            data=tf.extractfile(item).read(); txt=data.decode("utf-8","replace")
            digest=blob(data); seen[digest]=txt
            if re.search(r"constant[- ]roof|isoroof|stationary.{0,24}source",txt,re.I):
                title=re.search(r"\\section(?:\[[^\]]*\])?\{([^}]+)",txt)
                roof_candidates.append({"git_blob":digest,"member":item.name,
                                        "title":title.group(1) if title else None})
            if (re.search(r"constant[- ]roof|isoroof|stationary.{0,24}source",txt,re.I)
                and re.search(r"overlay|opposition|wedge|truncat",txt,re.I)):
                title=re.search(r"\\section(?:\[[^\]]*\])?\{([^}]+)",txt)
                close.append({"git_blob":digest,"member":item.name,
                              "title":title.group(1) if title else None})
    assert len(seen)==660
    d=draft.read_bytes()
    return {
      "status":"PASS",
      "limits":"Exact algebra and finite diagnostics supplement the native proof; no continuous physical theorem, source-growth premise or raw LLT is certified by this script.",
      "draft":{"path":str(draft),"git_blob":blob(d),"sha256":hashlib.sha256(d).hexdigest()},
      "constants":{"Q_squared":qtext(Qsq),"Q":"799/(9*sqrt(19))",
                   "E":qtext(E),"sigma":qtext(sig),"zero_clearance_foot_distance_squared_lower":qtext(foot_sq)},
      "backward_first_variation":{"formal_polynomial_identity":True,"incorrect_minus_backward_term_rejected":True},
      "overlay":{"exact_rational_cases":overlay_cases,"truncated_weight":"min(sup_I a,eta)",
                 "component_count":0,"pointwise_cutoff_negative_control_selected_integral":qtext(pointwise_selected_integral)},
      "exponents":{"m_range":[2,256],"index_pairs":index_pairs,"half_factor":"sigma^((max(i,m-i)-1)/2)",
                   "all_indices_factor":"(m-1)*sigma^((m-2)/4)",
                   "analytic_limit":"For each fixed q, (q+1)log m - (m-2)log(59/47)/4 tends to -infinity."},
      "positive_optics":{"rational_matrix_cases":matrix_cases,"determinant":1,
                         "note":"These algebraic parameters are not asserted to encode real full billiard trajectories."},
      "unused_inference_counterexample":{"type":"abstract smooth separated actions, not a Lorentz-gas counterexample",
          "half_actions":["x^2-delta*t*sqrt(1-x^2)+2t^2","z^2+delta*t*z+2t^2"],
          "domain":"2/5<=x<=3/5, |t|<=1/10, 0<delta<=1",
          "constant_roof_arc":"t=0, z=sqrt(1-x^2), S=1, S_t=0",
          "hxx_lower":qtext(hxx_lower),"left_half_determinant_lower":qtext(left_det_lower),
          "right_half_determinant_lower":qtext(right_det_lower),"full_schur_lower":qtext(full_schur_lower),
          "conclusion":"Strict convexity and small nonzero half-action twists alone cannot exclude a constant-roof arc."},
      "signed_exact_label_jump_factor":signed_label_jump.numerator,
      "inherited_sources":inherited,
      "novelty":{"archive":str(archive),"sha256":hashlib.sha256(raw).hexdigest(),
                 "distinct_native_tex_blobs":len(seen),"candidate_hits":close,
                 "all_constant_roof_or_stationary_source_candidates":roof_candidates,
                 "new_mechanism":"actual first-variation balance + single opposition quadrant + pointwise truncated interval overlay + optical canonical-side transversality",
                 "scope":"Text search with read comparison to324 and336; not a formal semantic novelty theorem."}
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=Path("/workspace/scratch/52177605cd92/a2-work/papers/A2-DYN-physical-roof-jump-spectrum-author-revision"))
    p.add_argument("--draft",type=Path,default=Path(__file__).with_name("341_interior_section_isoroof_payment.tex"))
    p.add_argument("--output",type=Path,default=Path(__file__).with_name("341_EXACT_CHECKS_AND_NOVELTY.json"))
    a=p.parse_args(); report=run(a.source.resolve(),a.draft.resolve())
    a.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":report["status"],"output":str(a.output),
         "overlay_cases":report["overlay"]["exact_rational_cases"],
         "index_pairs":report["exponents"]["index_pairs"],
         "archive_blobs":report["novelty"]["distinct_native_tex_blobs"],
         "archive_candidate_hits":len(report["novelty"]["candidate_hits"]),
         "scope":report["limits"]},ensure_ascii=False))

if __name__=="__main__": main()

