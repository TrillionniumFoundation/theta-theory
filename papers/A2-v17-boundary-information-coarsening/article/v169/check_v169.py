#!/usr/bin/env python3
"""Finite exact checks for A2 v169. These checks do not certify general proofs."""
from __future__ import annotations
import argparse, hashlib, itertools, json, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as S
from sympy.polys.matrices import DomainMatrix
HERE=Path(__file__).resolve().parent

def require(ok:bool, msg:str):
    if not ok: raise AssertionError(msg)

def minimal(ps):
    out=[]; low=10**30
    for x,y in sorted(set(ps)):
        if y<low: out.append((x,y));low=y
    return set(out)
def mul(A,B): return minimal((u+x,v+y) for u,v in A for x,y in B)
def power(A,n):
    out={(0,0)}
    for _ in range(n):out=mul(out,A)
    return out

def factor(a,m):
    E=[m-j+1 for j in range(1,a)]+[(m-a+1)*(m-a+2)//2]
    C=(a-1)*m*(m+1)//2
    P={(C,0)}
    for j,v in enumerate(E,1):P=mul(P,power({(1,0),(0,j)},v))
    return C,E,P

def row_factorization():
    records=[]
    for a in range(2,9):
        for m in sorted({a,a+1,a*(a+1)//2+1}):
            rows=[set() for _ in range((a+1)*m+1)]
            for h in range(m+1):
                for l in range(m-h+1):
                    for i in range(m+1):rows[i+a*(m-h-l)+(a-1)*l].add((h,l))
            prod={(0,0)}
            for n,raw in enumerate(rows):
                rr=minimal(raw);require(bool(rr),'no zero row')
                d=a*m-n
                if d<0:expected={(0,0)}
                else:
                    h0=max(0,(d-m+a-2)//(a-1));r=d-a*h0
                    expected={(h0,0)}
                    if r>0:
                        u,rho=divmod(r,a)
                        expected=mul(expected,power({(1,0),(0,a)},u))
                        if rho:expected=mul(expected,{(1,0),(0,rho)})
                require(rr==expected,f'row formula a={a} m={m} n={n}')
                prod=mul(prod,rr)
            C,E,expected=factor(a,m)
            require(prod==expected,f'all-order determinant factorization a={a} m={m}')
            require(min(u for u,v in prod)==C and min(v for u,v in prod)==0,'content exactly b^C')
            records.append(dict(a=a,m=m,rows=len(rows),content=C,exponents=E,minimal_generator_count=len(prod)))
    return records

def monic_and_generic():
    x,F,G,R,e,h,c,z,b,k=S.symbols('x F G R e h c z b k')
    records=[]
    for a in range(2,7):
        for i in range(1,a):
            pol=[x*R-e*h*F]+[x**(a-j)*F**(j-1)*G-e**(i+1-j)*h**(i-j)*R**j for j in range(1,i+1)]+[R**(i+1)-h*x**(a-i-1)*F**i*G]
            rho=(Fraction(a-i-1,i+1)+Fraction(a-i,i))/2
            wx=10*rho.denominator;wr=1+10*rho.numerator
            order=lambda t:(t[0]*wx+t[1]+t[2]+t[3]*wr,t)
            gb=S.groebner(pol,x,F,G,R,order=order,domain=S.QQ.poly_ring(e,h))
            require(len(gb.polys)==len(pol),'no additional middle Groebner generator')
            require(all(p.LC(order=order)==1 for p in gb.polys),'monic middle Groebner basis')
            mapping={F:x**a,G:e**(i+1)*h**i,R:e*h*x**(a-1)}
            require(all(S.expand(p.subs(mapping,simultaneous=True))==0 for p in pol),'generic curve equations')
            jac=S.det(S.Matrix([[S.diff(e**(i+1)*h**i,e),S.diff(e**(i+1)*h**i,h)],[h,e]]))
            require(S.expand(jac-e**(i+1)*h**i)==0,'relative canonical Jacobian')
            records.append(dict(a=a,chart=i,generators=len(pol),monic=True))
        pol=[x*R-c*F]+[x**(a-j)*F**(j-1)*G-z*c**(a-j)*R**j for j in range(1,a+1)]
        gb=S.groebner(pol,x,F,G,R,order='lex',domain=S.QQ.poly_ring(c,z))
        require(len(gb.polys)==len(pol) and all(p.LC()==1 for p in gb.polys),'monic terminal Groebner basis')
    return records

def mons(ds,dt):
    if ds<0 or dt<0:return []
    return [(ds-i,i,j0,j1,dt-j0-j1) for i in range(ds+1) for j0 in range(dt+1) for j1 in range(dt-j0+1)]
def rank(mat):return DomainMatrix.from_Matrix(mat).convert_to(S.QQ).rank()

def special_equations(a,p,q,beta,gamma):
    s,t,F,G,R=S.symbols('s t F G R');V=(s,t,F,G,R)
    if p<=q:
        k=gamma/beta if p==q else S.Integer(0)
        return V,[(s**(a-1)*R-k*t**(a-1)*G,a-1,1),(t**a*G,a,1),(t*R,1,1)]
    if p>=a*q:
        z=beta/gamma**a if p==a*q else S.Integer(0)
        return V,[(t*R,1,1)]+[(t**(a-j)*F**(j-1)*G-(z*R**a if j==a else 0),a-j,j) for j in range(1,a+1)]
    for i in range(1,a):
        if i*q<=p<=(i+1)*q:
            e=beta/gamma**i if p==i*q else S.Integer(0)
            h=gamma**(i+1)/beta if p==(i+1)*q else S.Integer(0)
            return V,[(t*R-e*h*s*F,1,1)]+[(t**(a-j)*F**(j-1)*G-e**(i+1-j)*h**(i-j)*s**(a-j)*R**j,a-j,j) for j in range(1,i+1)]+[(s**(a-i-1)*R**(i+1)-h*t**(a-i-1)*F**i*G,a-i-1,i+1)]
    raise AssertionError('uncovered arc')

def cubic_hilbert_kernels():
    a=3;m=7;qq=(a+1)*m+1;cols=mons(m,m);N=len(cols);pos={v:i for i,v in enumerate(cols)}
    beta=S.Integer(2);gamma=S.Integer(3)
    profiles=[(1,2),(1,1),(3,2),(2,1),(5,2),(3,1),(4,1)]
    records=[]
    for p,q in profiles:
        weights=[min(p*v[3]+q*v[4] for v in cols if v[1]+a*v[2]+(a-1)*v[4]==r) for r in range(qq)]
        L=S.zeros(qq,N)
        for j,col in enumerate(cols):
            _,i,j0,j1,j2=col;r=i+a*j0+(a-1)*j2
            if p*j1+q*j2==weights[r]:L[r,j]=beta**j1*gamma**j2
        require(rank(L)==qq,'cubic primitive quotient rank')
        vs,ideals=special_equations(a,p,q,beta,gamma)
        relations=[]
        for f,ds,dt in ideals:
            for mon in mons(m-ds,m-dt):
                poly=S.Poly(f*S.prod(x**n for x,n in zip(vs,mon)),*vs)
                row=[S.Integer(0)]*N
                for ex,coeff in poly.terms():row[pos[ex]]=coeff
                relations.append(row)
        H=S.Matrix(relations)
        require(L*H.T==S.zeros(qq,H.rows),'cubic listed ideal annihilated by primitive matrix')
        hr=rank(H);require(hr==N-qq,f'cubic full degree-seven ideal, p={p} q={q}, rank={hr}')
        require(sum(weights)==56*p+7*min(p,q)+6*min(p,2*q)+15*min(p,3*q),'cubic raw order')
        records.append(dict(p=p,q=q,beta=2,gamma=3,quotient_rank=qq,ideal_rank=hr,columns=N,raw_minor_order=sum(weights)))
    return records

def punctual_algebras():
    x,F,R=S.symbols('x F R');records=[]
    for a in range(3,10):
        for i in range(1,a):
            I=[x*R,R**(i+1)]+[x**(a-j)*F**(j-1) for j in range(1,i+1)]
            gb=S.groebner(I,x,F,R)
            basis=[x**(a-i+u)*F**v for u in range(i-1) for v in range(i-1-u)]
            require(len(basis)==i*(i-1)//2,'open punctual length')
            require(all(gb.reduce(t)[1]==t for t in basis),'open punctual basis independent standard monomials')
            require(all(gb.reduce(R*t)[1]==0 for t in basis),'R kills punctual module')
        for j in range(2,a+1):
            d=a-j;I=[x*R,R**j-2*x**d*F**(j-1)]+[x**(a-r)*F**(r-1) for r in range(1,j)]
            gb=S.groebner(I,R,x,F)
            basis=[x**(d+1+u)*F**v for u in range(j-2) for v in range(j-2-u)]
            require(len(basis)==(j-1)*(j-2)//2,'wall punctual length')
            require(all(gb.reduce(t)[1]==t for t in basis),'wall punctual independence')
            require(all(gb.reduce(R*t)[1]==0 for t in basis),'wall R-annihilation')
        powers=[sum(1 for u in range(r,a-1) for v in range(a-1-u)) for r in range(1,a-1)]
        require(powers==[(a-r)*(a-r-1)//2 for r in range(1,a-1)],'nilradical power lengths')
        records.append(dict(a=a,punctual_length=(a-1)*(a-2)//2,nilpotence_order=a-1,power_lengths=powers))
    return records

def rees_and_fan():
    records=[]
    for a in range(2,7):
        m=a;C,E,P=factor(a,m);J={(u-C,v) for u,v in P}
        eta=[sum(e*min(i,j) for j,e in enumerate(E,1)) for i in range(1,a+1)]
        for n in [1,2,3]:
            Jn=power(J,n)
            for u in range(n*sum(E)+2):
                actual=min(v for x,v in Jn if x<=u)
                expected=max([0]+[n*eta[i-1]-i*u for i in range(1,a+1)])
                require(actual==expected,'Rees inequalities recover every monomial row')
        rays=[(1,0)]+[(i,1) for i in range(a,0,-1)]+[(0,1)]
        require(all(u*y-v*x==1 for (u,v),(x,y) in zip(rays,rays[1:])),'unimodular all-order fan')
        records.append(dict(a=a,rays=rays,self_intersections=[-2]*(a-1)+[-1],inequalities_exact=True))
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        prev=HERE.parent/'v167'
        subprocess.run([sys.executable,str(prev/'check_v167.py')],check=True)
        data=json.loads((prev/'EXACT_CHECKS_V167.json').read_text())
        require(data['all_checks_pass'] and data['inherited_v166_full_chain_rerun'],'entire predecessor chain')
        (HERE/'INHERITED_V167_CHECKS_RERUN.json').write_text(json.dumps(data,indent=2)+'\n');inherited=True
    data={'revision':169,'inherited_v167_full_chain_rerun':inherited,
          'purpose':'Finite regression checks, not a certificate of general proof, originality, or editorial merit.'}
    for key,fn in [('row_factorizations',row_factorization),('monic_chart_checks',monic_and_generic),('cubic_Hilbert_kernels',cubic_hilbert_kernels),('punctual_algebras',punctual_algebras),('Rees_inequalities_and_fan',rees_and_fan)]:
        print('Checking',key,flush=True);data[key]=fn()
    data['all_checks_pass']=True
    (HERE/'EXACT_CHECKS_V169.json').write_text(json.dumps(data,indent=2)+'\n')
    print('All new finite checks passed; inherited full chain rerun:',inherited)
if __name__=='__main__':main()
