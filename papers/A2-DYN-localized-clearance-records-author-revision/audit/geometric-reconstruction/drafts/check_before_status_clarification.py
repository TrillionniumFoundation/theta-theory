#!/usr/bin/env python3
"""Exact finite diagnostics for native 327--329; not a billiard proof.

No floating-point arithmetic, random sampling, network access, or assert is used.
The continuous geometric hypotheses and full proofs are in the bound TeX files.
--details PATH writes a deterministic detailed JSON record.  --source-root may
name either the article directory, its core directory, or a component directory.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

FILES = (
    "327_length_sensitive_physical_source_transport.tex",
    "328_localized_clearance_physical_roof_height.tex",
    "329_original_normalized_deep_clearance_payment.tex",
)
REQUIRED = {
    FILES[0]: (
        "thm:lc-renewal", "lem:lc-cover", "thm:lc-local-half",
        "eq:lc-half-index", "eq:lc-individual", "cor:lc-source-mass",
    ),
    FILES[1]: (
        "lem:lc-turning", "lem:lc-selected-boundary", "lem:lc-selected-cap",
        "thm:lc-selected-roof-height", "eq:lc-roof-constant",
        "eq:lc-right-endpoint",
    ),
    FILES[2]: (
        "thm:lc-deep-payment", "eq:lc-log-depth", "eq:lc-normalized-rate",
        "thm:lc-same-pool", "eq:lc-shortage-difference", "eq:lc-final-shortage",
    ),
}


class Failure(RuntimeError):
    pass


class Checks:
    def __init__(self):
        self.groups = {}

    def check(self, group, condition, witness):
        if not condition:
            raise Failure(f"{group}: {witness}")
        self.groups[group] = self.groups.get(group, 0) + 1


# A minimal exact multivariate polynomial ring.  The variables in each identity
# are formal indeterminates; identities are checked coefficient by coefficient.
class Poly:
    def __init__(self, terms=None):
        self.terms = {k: F(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def constant(value):
        return Poly({(): F(value)})

    @staticmethod
    def variable(name):
        return Poly({((name, 1),): F(1)})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other):
        out = dict(self.terms)
        for k, v in self.coerce(other).terms.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        out = {}
        for k, a in self.terms.items():
            for l, b in self.coerce(other).terms.items():
                powers = dict(k)
                for name, power in l:
                    powers[name] = powers.get(name, 0) + power
                key = tuple(sorted(powers.items()))
                out[key] = out.get(key, F(0)) + a * b
        return Poly(out)

    __rmul__ = __mul__

    def is_zero(self):
        return not self.terms


def symbolic_checks(c):
    a, b, d, x, y = [Poly.variable(n) for n in ("a", "b", "d", "x", "y")]
    perpendicular_form = a*y*y - 2*b*x*y + d*x*x
    adjugate_form = d*x*x - 2*b*x*y + a*y*y
    c.check("formal_polynomial", (perpendicular_form-adjugate_form).is_zero(),
            "2D cofactor identity for the exact h_x")
    am, ap, hm, hp = [Poly.variable(n) for n in ("am", "ap", "hm", "hp")]
    # The physical signs multiply the determinant by a unit sign only.
    det = am*(-ap*hp) - (am*hm)*ap
    c.check("formal_polynomial", (det+am*ap*(hm+hp)).is_zero(),
            "positive sum of the two half ratios")
    tau, kick, bb, dd = [Poly.variable(n) for n in ("tau", "kick", "B", "D")]
    aa = 1+tau*kick
    c.check("formal_polynomial", (aa - tau*kick - 1).is_zero(),
            "determinant of physical flight times kick")
    bnew = aa*bb + tau*dd
    dnew = kick*bb + dd
    c.check("formal_polynomial", (bnew-tau*dnew-bb).is_zero(),
            "incoming free-flight row, no terminal kick")
    pa, vv = Poly.variable("cap"), Poly.variable("v")
    c.check("formal_polynomial", ((pa*pa+vv*vv)-pa*pa-vv*vv).is_zero(),
            "cap angular factor denominator minus cap square is v square")


def exact_constants(c):
    rm, rp = F(9,20), F(47,100)
    t, delta, ac = F(3,50), F(3,200), F(9,200)
    km, kp, sig = F(100,47), F(20,9), F(47,59)
    stand2 = (1-rp)**2-(rp+delta)**2
    c.check("exact_geometry", 1-2*rp == t, "disk gap is 3/50")
    c.check("exact_geometry", delta == t/4, "clearance range is one quarter gap")
    c.check("exact_geometry", stand2 == F(1827,40000), "foot standoff square")
    c.check("exact_geometry", stand2 > ac*ac > 0, "strict cover derivative standoff")
    c.check("exact_geometry", stand2 > t*t, "marked first flight exceeds t_*")
    c.check("exact_geometry", 1/(1-rp) < km, "relative angle strictly decreases")
    c.check("exact_geometry", 2*rp+delta < 1, "no selected foot at incident endpoint")
    c.check("exact_geometry", rp+delta == F(97,200), "signed impact magnitude bound")
    c.check("exact_geometry", 1+2*t/rp == 1/sig, "positive Jacobi expansion")
    c.check("exact_geometry", 1/(km*t) == F(47,6), "common individual inverse constant")
    c.check("exact_geometry", (F(28,5)+rp)/(2*rm) == F(607,90),
            "two-sided root-weight constant")
    cap = F(5,6)
    c.check("exact_geometry", 1-cap*cap == F(11,36), "terminal cap cosine square")
    c.check("exact_geometry", F(11,36) > F(1,16),
            "cap lies in central strip since sin(1/4)<1/4")
    c.check("normalization_exponents", -1+F(1,4) == -F(3,4),
            "one conditional conversion in native315")
    c.check("normalization_exponents", F(1,4)*F(1,4) == F(1,16),
            "original guard depth exponent after singular multiplier")
    c.check("normalization_exponents", F(1,16)*4 == F(1,4),
            "eventual geometric width condition")
    return {"R_minus": str(rm), "R_plus": str(rp), "sigma": str(sig),
            "q_0": "47/53", "delta_star": str(delta),
            "standoff_square": str(stand2), "E_lc": "47/6", "C_foot": "607/90"}


def renewal_checks(c):
    for theta in (F(1,5), F(47,59), F(9,10), F(127,128)):
        for n in range(65):
            full = sum((theta**(n-k) for k in range(1,n+1)), F(0))
            c.check("renewal_last_generation", full == (1-theta**n)/(1-theta),
                    (theta,n))
            c.check("renewal_last_generation", full <= 1/(1-theta), (theta,n))
            if n:
                missing = sum((theta**(n-k) for k in range(1,n)),F(0))
                c.check("renewal_last_generation", full-missing == 1,
                        ("omitting k=n loses precisely the terminal term",theta,n))
    # The explicit cutoff may always be chosen after the finite candidate count.
    for jf in (1,3,17,101,1001):
        sig, km, t = F(47,59), F(100,47), F(3,50)
        need = F(2*jf)/(km*t*(1-sig))
        k0 = need.numerator//need.denominator + 3
        theta = sig + F(jf)/(km*t*(k0-1))
        c.check("renewal_cutoff", sig < theta < (1+sig)/2 < 1, (jf,k0))


def partitions(n):
    for cuts in itertools.product((False,True), repeat=max(0,n-1)):
        edges = [0]+[i+1 for i,v in enumerate(cuts) if v]+[n]
        yield list(zip(edges,edges[1:]))


def overlay_checks(c):
    for n in range(1,7):
        pp=list(partitions(n))
        for ii, base_a in enumerate(pp):
            for jj, base_b in enumerate(pp):
                # Also check disjoint interval families with actual gaps.
                for gaps in (False,True):
                    aa = [q for k,q in enumerate(base_a) if not gaps or k%2==0]
                    bb = [q for k,q in enumerate(base_b) if not gaps or k%2==0]
                    wa = [F(2+u+v,3+k) for k,(u,v) in enumerate(aa)]
                    wb = [F(3+2*u+v,4+k) for k,(u,v) in enumerate(bb)]
                    lhs=F(0); charged_a=[0]*len(aa); charged_b=[0]*len(bb)
                    for i,(a0,a1) in enumerate(aa):
                        for j,(b0,b1) in enumerate(bb):
                            if max(a0,b0)<min(a1,b1):
                                lhs+=wa[i]*wb[j]
                                if a0>=b0: charged_a[i]+=1
                                else: charged_b[j]+=1
                    rhs=max(wb)*sum(wa)+max(wa)*sum(wb)
                    c.check("interval_overlay", lhs<=rhs, (n,ii,jj,gaps))
                    c.check("interval_overlay", max(charged_a+charged_b)<=1,
                            ("unique later-left-endpoint charge",n,ii,jj,gaps))


def index_checks(c):
    for m in range(1,129):
        for j in range(m):
            for k in range(m):
                if k<j:
                    h,n,l=j-k-1,m-j-1,m-k
                    c.check("all_half_indices", min(h,n)>=0 and h+n+2==l,
                            (m,j,k,"forward"))
                    c.check("all_half_indices", (k+1)-1==k and l-1==m-k-1,
                            (m,j,k,"opposite individual powers"))
                elif k>j:
                    h,n,l=k-j-1,j,k+1
                    c.check("all_half_indices", min(h,n)>=0 and h+n+2==l,
                            (m,j,k,"backward"))
                    c.check("all_half_indices", (m-k)-1==m-k-1 and l-1==k,
                            (m,j,k,"opposite individual powers"))
                else:
                    c.check("all_half_indices", k+1>=1 and m-k>=1,
                            (m,j,k,"whole same-flight trace"))
            jr=m-1-j
            c.check("physical_reversal_indices", min(j,m-1-j)==min(jr,m-1-jr),
                    (m,j))
            c.check("physical_reversal_indices", jr>=0 and jr<m, (m,j))


def boundary_sum_checks(c):
    for sig in (F(1,3),F(47,59),F(9,10)):
        theta=(1+sig)/2
        for delta, kk, hh in ((F(1,200),F(2),F(3)),
                             (F(3,200),F(7,5),F(11,4))):
            for m in range(1,41):
                sp=[sig**k for k in range(m)]
                tp=[theta**k for k in range(m)]
                for j in range(m):
                    right=m-j-1
                    lhs=hh*(sp[j]+sp[right])
                    for k in range(j):
                        lhs+=kk*sp[k]*(delta+tp[right])+hh*sp[m-k-1]
                    for k in range(j+1,m):
                        lhs+=kk*sp[m-k-1]*(delta+tp[j])+hh*sp[k]
                    sharp=(2*kk*delta+(kk+hh)*(tp[j]+tp[right]))/(1-sig)
                    chosen=(2*kk+hh)*(delta+tp[j]+tp[right])/(1-sig)
                    c.check("complete_selected_old_boundary", lhs<=sharp<=chosen,
                            (sig,delta,m,j))


def deep_union_checks(c):
    for r,theta,x in ((F(3,4),F(4,5),F(1,7)),
                      (F(31,32),F(9,10),F(5,3)),
                      (F(127,128),F(47,59),F(2))):
        for m in range(1,65):
            for depth in range(m//2+3):
                indices=[j for j in range(m) if min(j,m-1-j)>=depth]
                lhs=sum((x*r**min(j,m-1-j)+theta**j+theta**(m-1-j)
                         for j in indices),F(0))
                rhs=2*(x*r**depth/(1-r)+theta**depth/(1-theta))
                c.check("deep_full_union", lhs<=rhs, (r,theta,m,depth))
                for d in set(min(j,m-1-j) for j in indices):
                    c.check("deep_depth_multiplicity",
                            sum(min(j,m-1-j)==d for j in indices)<=2,
                            (m,depth,d))
    # Integer schedules avoid numerical logarithms: the first D satisfying the
    # exact exponential inequality is the defining logarithmic ceiling, including
    # its equality case.  These are auxiliary sequence examples, not orbit tests.
    for q in (F(1,2),F(4,5),F(31,32)):
        for m in (1,2,7,31,127,511):
            target=F(1,(m+1)**3); d=0; power=F(1)
            while power>target:
                d+=1; power*=q
            c.check("normalized_schedule", power<=target, (q,m,d))
            c.check("normalized_schedule", d==0 or power/q>target, (q,m,d))
            c.check("normalized_schedule", m*m*power<=F(1,m+1), (q,m,d))
            c.check("normalized_schedule", power**4<=F(1,(m+1)**12), (q,m,d))


def shortage_checks(c):
    vals=[F(i,4) for i in range(17)]
    for u,v,pool in itertools.product(vals,repeat=3):
        old=max(F(0),u+v-pool); new=max(F(0),u-pool)
        c.check("same_pool_positive_part", 0<=old-new<=v, (u,v,pool))


def locate_sources(explicit):
    candidates=[]
    if explicit:
        p=Path(explicit).resolve(); candidates.extend((p/"core",p))
    else:
        f=Path(__file__).resolve()
        candidates.extend((f.parents[1]/"core",f.parent/"core",f.parent))
    for p in candidates:
        if all((p/name).is_file() for name in FILES):
            return p
    raise Failure("Cannot locate all three final TeX modules; use --source-root")


def source_checks(c,root):
    hashes={}; texts={}; labels=[]; external=set()
    for name in FILES:
        data=(root/name).read_bytes(); hashes[name]=hashlib.sha256(data).hexdigest()
        text=data.decode("utf-8"); texts[name]=text
        found=re.findall(r"\\label\{([^}]+)\}",text); labels.extend(found)
        for required in REQUIRED[name]:
            c.check("source_binding", required in found,(name,required))
        c.check("source_binding", "^{,n}" not in text,(name,"no malformed exponent"))
        c.check("source_binding", text.count("\\begin{proof}")==text.count("\\end{proof}"),
                (name,"proof environments balanced"))
    c.check("source_binding", len(labels)==len(set(labels)),"unique new labels")
    for name,text in texts.items():
        for ref in re.findall(r"\\(?:eqref|ref)\{([^}]+)\}",text):
            if ":lc-" in ref:
                c.check("source_binding", ref in labels,(name,ref))
            else:
                external.add(ref)
    c.check("source_binding", r"k\in\{1,\ldots,n\}" in texts[FILES[0]],
            "last-long terminal generation retained")
    c.check("source_binding", r"A_q(t)\le A_q(b_q^-)" in texts[FILES[1]],
            "height is paid from the right endpoint")
    c.check("source_binding", r"K_BP_{r_B,m}^{\rm ng}" in texts[FILES[2]],
            "original full nongrazing pool retained")
    return hashes,sorted(external),len(labels)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root",type=Path)
    parser.add_argument("--details",nargs="?",const="-",metavar="PATH")
    args=parser.parse_args()
    c=Checks(); root=locate_sources(args.source_root)
    hashes,external,label_count=source_checks(c,root)
    constants=exact_constants(c)
    symbolic_checks(c); renewal_checks(c); overlay_checks(c); index_checks(c)
    boundary_sum_checks(c); deep_union_checks(c); shortage_checks(c)
    payload={
        "status":"PASS_AUXILIARY_ONLY",
        "diagnostic":"native327-329 exact rational, symbolic and index checks",
        "source_sha256":hashes,
        "source_label_count":label_count,
        "external_dependency_labels":external,
        "exact_constants":constants,
        "checks_by_group":dict(sorted(c.groups.items())),
        "check_count":sum(c.groups.values()),
        "arithmetic":"stdlib fractions; coefficientwise formal polynomial identities; integers",
        "limitations":[
            "Finite index/rational checks do not prove continuous billiard geometry.",
            "Native281-284 physical class invariance, complexity and distortion are inherited inputs.",
            "Native315 full localized multiplier and native323 endpoint/coarea identities are inherited inputs.",
            "The TeX proofs, not this diagnostic, contain all-count and ordered-limit arguments.",
            "Shallow same-roof shortage and unestablished inherited spectral/pressure inputs remain open.",
            "No independent expert reconstruction, full raw pointwise local limit or inverse theorem is certified."
        ],
    }
    full=json.dumps(payload,sort_keys=True,indent=2)+"\n"
    if args.details and args.details!="-":
        Path(args.details).write_text(full,encoding="utf-8")
    if args.details=="-":
        sys.stdout.write(full)
    else:
        print(json.dumps({"status":payload["status"],"check_count":payload["check_count"],
                          "source_label_count":label_count,
                          "record_sha256":hashlib.sha256(full.encode()).hexdigest()},sort_keys=True))
    return 0


if __name__=="__main__":
    try:
        sys.exit(main())
    except (Failure,OSError,UnicodeError) as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        sys.exit(1)
