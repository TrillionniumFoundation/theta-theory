#!/usr/bin/env python3
"""Independent exact finite checks; not a formal certificate of the proofs."""
from __future__ import annotations
import hashlib, importlib.util, itertools as it, json, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent

def require(ok: bool, msg: str) -> None:
    if not ok: raise AssertionError(msg)

def symmetric(n: int, prefix: str):
    xs=s.symbols(' '.join(f'{prefix}{i}{j}' for i in range(n) for j in range(i,n)))
    if n==1: xs=(xs,)
    A=s.zeros(n)
    for x,(i,j) in zip(xs,it.combinations_with_replacement(range(n),2)):
        A[i,j]=A[j,i]=x
    return tuple(xs),A

def canonical(polys,variables):
    """Reduced row-space basis over QQ in sparse monomial coordinates."""
    pivots={}
    for f in polys:
        row={ex:Fraction(c) for ex,c in s.Poly(f,*variables,domain=s.QQ).terms() if c}
        for pivot,base in sorted(pivots.items(),reverse=True):
            a=row.get(pivot,Fraction(0))
            if not a: continue
            for mon,c in base.items():
                row[mon]=row.get(mon,Fraction(0))-a*c
                if not row[mon]: del row[mon]
        if not row: continue
        pivot=max(row);a=row[pivot];row={mon:c/a for mon,c in row.items()}
        for base in pivots.values():
            a=base.get(pivot,Fraction(0))
            if a:
                for mon,c in row.items():
                    base[mon]=base.get(mon,Fraction(0))-a*c
                    if not base[mon]: del base[mon]
        pivots[pivot]=row
    return tuple((p,tuple(sorted(v.items()))) for p,v in sorted(pivots.items()))

def minors(A,q):
    if q==0:return [s.Integer(1)]
    n=A.rows;out=set()
    for rows in it.combinations(range(n),q):
        for cols in it.combinations(range(n),q):
            f=s.Poly(s.expand(A.extract(rows,cols).det()))
            if not f.is_zero:out.add(s.expand(f.as_expr()/f.LC()))
    return sorted(out,key=str)

def products(generators,count):
    return [s.prod(items) for items in it.combinations_with_replacement(generators,count)]

def universal(n,h):
    aa,A=symmetric(n,'a');xx,X=symmetric(n,'x');z=s.symbols('z')
    # The apolar injection is split over QQ. Its coefficient space computes
    # precisely the ideal of ell_A^p, without using the proposed minor formula.
    detpower=s.Poly(s.expand((X+z*A).det()**h),z)
    rows=[]
    for p in range(1,n*h+1):
        coeff=s.Poly(detpower.nth(p),*xx).coeffs()
        q,r=divmod(p,h)
        expected=[s.expand(a*b) for a in products(minors(A,q),h-r)
                  for b in (products(minors(A,q+1),r) if r else [s.Integer(1)])]
        left=canonical(coeff,aa);right=canonical(expected,aa)
        require(left==right,f'QQ coefficient spaces n={n},h={h},p={p}')
        rows.append({'p':p,'q':q,'s':r,'coefficient_span_dimension':len(left),
                     'equal_QQ_row_spaces':True})
    print(f'Universal coefficient spans passed: n={n},h={h}',flush=True)
    return {'n':n,'h':h,'field':'QQ','powers':rows}

def combinatorics():
    rows=[]
    for n in range(2,10):
        for h in range(1,6):
            for p in range(1,n*h+1):
                q,r=divmod(p,h)
                for a in range(n):
                    exponent=(h-r)*max(q-a,0)+r*max(q+1-a,0)
                    require(exponent==max(p-h*a,0),'all boundary exponents')
            for q in range(2,n):
                total=0
                for p in range(1,n*h):
                    k,r=divmod(p,h)
                    total+=(h-r if k==q else 0)+(r if k+1==q else 0)
                require(total==h*h,'Segre graph product exponents')
            rows.append({'n':n,'h':h,'boundary_and_graph_exponents_checked':True})
    return rows

def contact_profiles():
    rows=[]
    for n in range(2,6):
        for tail in it.combinations_with_replacement(range(5),n-1):
            es=(0,)+tail
            for h in range(1,4):
                values=[]
                for p in range(n*h+1):
                    q,r=divmod(p,h)
                    value=h*sum(es[:q])+(r*es[q] if r else 0)
                    via=sum(max(p-h*a,0)*(es[a]-es[a-1]) for a in range(1,n))
                    require(value==via,'contact valuation reconstruction')
                    values.append(value)
                recovered=[(values[h*(r+1)]-2*values[h*r]+values[h*(r-1)])//h for r in range(1,n)]
                require(recovered==[es[i]-es[i-1] for i in range(1,n)],'second differences')
                rows.append({'e':es,'h':h})
    return {'profile_count':len(rows),'all_equalities_pass':True,
            'example_e':[0,1,3],'example_h':2,'example_power_valuations':[0,0,1,2,5,8]}

def nilpotent_base():
    e,x,y,z=s.symbols('e x y z')
    F=s.Poly(s.expand(((x+z*e)*y)**2),z)
    reduced=[s.rem(F.nth(p),e**3,e) for p in range(1,5)]
    require(reduced==[2*e*x*y**2,e**2*y**2,0,0],'nonreduced base coefficients')
    return {'base':'QQ[e]/(e^3)','n':2,'h':2,'matrix':'diag(e,0)',
            'power_ideals':['(e)','(e^2)','0','0'],'checked_from_determinant_coefficients':True}

def main():
    ap=__import__('argparse').ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v155'/'check_v155.py')],check=True)
        previous=HERE.parent/'v155'/'EXACT_CHECKS_V155.json'
        require(json.loads(previous.read_text())['all_checks_pass'],'v155 rerun')
        (HERE/'INHERITED_V155_CHECKS_RERUN.json').write_bytes(previous.read_bytes())
        inherited=True
    cases=[universal(n,h) for n,h in [(2,1),(2,2),(2,3),(3,1),(3,2),(3,3),(4,1)]]
    out={'revision':157,'all_checks_pass':True,'universal_coefficient_tests':cases,
         'boundary_graph_tests':combinatorics(),'spectral_contact_tests':contact_profiles(),
         'nonreduced_base_test':nilpotent_base(),'inherited_v155_suite_rerun':inherited,
         'historical_28_checks_rerun':False,'general_proofs_certified_by_computation':False,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V157.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All v157 exact checks passed.',flush=True)
if __name__=='__main__':main()
