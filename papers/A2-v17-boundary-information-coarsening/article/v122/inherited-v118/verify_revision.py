#!/usr/bin/env python3
"""Exact finite regression checks. These do not certify the general proofs."""
from pathlib import Path
import itertools, json, math, random, re
import sympy as sp
HERE=Path(__file__).resolve().parent

def basis(e,h):
    return sorted((a for a in itertools.product(range(h),repeat=e) if sum(a)<h),key=lambda a:(sum(a),a))
def mul(p,q,limit):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            ab=tuple(x+y for x,y in zip(a,b))
            if sum(ab)<limit: r[ab]=r.get(ab,0)+c*d
    return {a:c for a,c in r.items() if c!=0}
def power(p,n,limit,e):
    q={(0,)*e:sp.Integer(1)}
    for _ in range(n): q=mul(q,p,limit)
    return q

def substitution_tests():
    cases=[]
    for e,h in [(2,3),(2,4),(2,5),(3,3),(3,4),(4,3)]:
        bas=basis(e,h); N=math.comb(e+h-1,e+1)
        for seed in range(3):
            rng=random.Random(118000+100*e+10*h+seed)
            xs=[{a:sp.Integer(rng.randint(-2,2)) for a in bas if sum(a)>0} for _ in range(e)]
            M=sp.Matrix([[xs[i][tuple(int(j==l) for l in range(e))] for i in range(e)] for j in range(e)])
            if seed==2:
                for j in range(e): xs[-1][tuple(int(j==l) for l in range(e))]=xs[0][tuple(int(j==l) for l in range(e))]
                M=sp.Matrix([[xs[i][tuple(int(j==l) for l in range(e))] for i in range(e)] for j in range(e)])
            cols=[]
            for alpha in bas:
                p={(0,)*e:sp.Integer(1)}
                for i,n in enumerate(alpha):p=mul(p,power(xs[i],n,h,e),h)
                cols.append([p.get(a,0) for a in bas])
            T=sp.Matrix.hstack(*(sp.Matrix(c) for c in cols))
            actual=T.det(method='domain-ge'); expected=M.det()**N
            assert actual==expected,(e,h,seed)
            cases.append({'e':e,'h':h,'length':len(bas),'exponent':N,'seed':seed,'linear_det':str(M.det()),'identity_verified':True})
    # Full symbolic length-six matrix, including independent quadratic terms.
    a,b,c,d=sp.symbols('a b c d'); u=sp.symbols('u0:6')
    bas=basis(2,3)
    xs=[{(1,0):a,(0,1):b,(2,0):u[0],(1,1):u[1],(0,2):u[2]},
        {(1,0):c,(0,1):d,(2,0):u[3],(1,1):u[4],(0,2):u[5]}]
    cols=[]
    for alpha in bas:
        p={(0,0):sp.Integer(1)}
        for i,n in enumerate(alpha):p=mul(p,power(xs[i],n,3,2),3)
        cols.append([p.get(v,0) for v in bas])
    T=sp.Matrix.hstack(*(sp.Matrix(c0) for c0 in cols))
    assert sp.factor(T.det()-(a*d-b*c)**4)==0
    return cases

def split_alpha(alpha,j,h,n):
    total=sum(alpha); sizes=[h]*j
    rem=total-j*h
    for i in range(j):
        t=min(rem,n-h); sizes[i]+=t; rem-=t
    assert rem==0
    left=list(alpha); out=[]
    for size in sizes:
        v=[0]*len(alpha)
        for i in range(len(alpha)):
            t=min(size,left[i]);v[i]=t;left[i]-=t;size-=t
        assert size==0;out.append(tuple(v))
    assert not any(left)
    return out

def conductor_tests():
    rows=[]
    for e,h,m in [(1,2,2),(2,3,2),(2,3,3),(3,3,2),(2,4,2)]:
        n=2*h-1;lim=m*n+1
        u={(0,)*e:sp.Integer(1)}
        for i in range(e):u[tuple(1 if j==i else 0 for j in range(e))]=sp.Integer(i+1)
        u[(2,)+(0,)*(e-1)]=sp.Integer(2)
        bb=[a for a in basis(e,lim) if sum(a)>=h]
        for alpha in bb:
            t=sum(alpha); j=next(j for j in range(1,m+1) if j*h<=t<=j*n)
            factors=split_alpha(alpha,j,h,n)
            assert all(h<=sum(v)<=n for v in factors)
            poly={(0,)*e:sp.Integer(1)}
            for v in factors:poly=mul(poly,{v:sp.Integer(1)},lim)
            poly=mul(poly,power(u,m-j,lim,e),lim)
            assert poly[alpha]==1
            assert all(sum(v)>t or v==alpha for v in poly)
            assert all(h<=sum(v)<=m*n for v in poly)
        rows.append({'e':e,'h':h,'n':n,'m':m,'triangular_columns':len(bb),'diagonal_entries_all_one':True})
    for h in range(2,10):
        n=2*h-2;exponents={0}|set(range(h,n+1))
        assert 2*h-1 not in {i+j for i in exponents for j in exponents}
    return rows

def action_tests():
    s=sp.symbols('s');T=sp.Matrix([[0,0],[-s*s,0]])
    theta=sp.Matrix.hstack(sp.Matrix([1,0,0,1]),sp.Matrix(list(T)),sp.zeros(4,1))
    minors=[sp.factor(theta.extract(rr,cc).det()) for rr in itertools.combinations(range(4),2) for cc in itertools.combinations(range(3),2)]
    assert set(x for x in minors if x!=0)<={s*s,-s*s}
    assert any(x!=0 for x in minors)
    assert theta.subs(s,0).rank()==1 and theta.subs(s,1).rank()==2
    assert all(theta.extract(rr,range(3)).det()==0 for rr in itertools.combinations(range(4),3))
    a,b,c,d,e,f=sp.symbols('a b c d e f')
    X=sp.Matrix([[a,b],[c,-a]]);Y=sp.Matrix([[d,e],[f,-d]])
    comm=X*Y-Y*X
    assert sp.expand(comm[0,0]-(b*f-c*e))==0
    assert sp.expand(comm[0,1]-2*(a*e-b*d))==0
    assert sp.expand(comm[1,0]+2*(a*f-c*d))==0
    return {'codimension_two_rank_one_ideal':'(s^2)','geometric_action_ranks':[2,1],
            'all_three_minors_zero':True,'traceless_bracket_wedge_identity':True}

def preservation():
    data=json.loads((HERE/'evidence/PRESERVATION.json').read_text())
    assert not data['missing_old_labels']
    current=set()
    for source in list(HERE.glob('*.tex'))+list((HERE/'parts').glob('*.tex')):
        current.update(re.findall(r'\\label\{([^}]+)\}',source.read_text()))
    assert set(data['old_labels']) <= current
    for p in (HERE/'parts').glob('*.tex'):
        text=p.read_text()
        for env in ['theorem','proof','lemma','proposition','corollary','remark']:
            assert text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),(p,env)
    return {k:data[k] for k in ['retained_old_label_count','new_label_count','missing_old_labels']}

def main():
    out={'kind':'exact finite regression diagnostics; not proof certification',
         'substitution':substitution_tests(),'symbolic_e2_h3_full_nonlinear_identity':True,
         'conductor':conductor_tests(),'action':action_tests(),'preservation':preservation(),
         'proof_certification':False,'priority_certification':False}
    (HERE/'evidence/DIAGNOSTICS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
