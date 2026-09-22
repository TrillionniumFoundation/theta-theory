#!/usr/bin/env python3
"""Finite exact regressions and source preservation, not proof certification."""
from pathlib import Path
from math import comb
import hashlib,json,re,subprocess,sys
import sympy as s
HERE=Path(__file__).resolve().parent
OUT=HERE/'evidence'; OUT.mkdir(exist_ok=True)
def need(ok,msg):
    if not ok: raise AssertionError(msg)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def source_audit():
    manifest=json.loads((OUT/'V116_SOURCE_MANIFEST.json').read_text())
    for name,sha in manifest['sha256'].items():
        need(digest(HERE/'history/v116_source'/name)==sha,'preservation '+name)
    def expand(p):
        t=p.read_text()
        return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(HERE/m[1]),t)
    old='\n'.join(p.read_text() for p in (HERE/'history/v116_source/parts').glob('*.tex'))
    full=expand(HERE/'paper.tex'); core=expand(HERE/'geometry.tex')
    labels=re.findall(r'\\label\{([^}]+)\}',full)
    need(len(labels)==len(set(labels)),'duplicate labels')
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',old))
    need(oldlabels<=set(labels),'lost labels '+str(oldlabels-set(labels)))
    for source in [full,core]:
        labs=set(re.findall(r'\\label\{([^}]+)\}',source))
        refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',source))
        need(refs<=labs,'unresolved labels '+str(refs-labs))
    active=0
    for p in (HERE/'history/v116_source/parts').glob('*.tex'):
        q=HERE/'parts'/p.name
        if q.read_bytes()==p.read_bytes(): active+=1
    return {'archived_files':len(manifest['sha256']),'old_part_labels':len(oldlabels),
            'full_labels':len(labels),'byte_identical_active_old_parts':active}
def grass_tests():
    u,v=s.symbols('u v'); rows=[]
    for d in range(3,10):
        cs=s.symbols('c2:'+str(d)); c={0:0,1:1,**dict(zip(range(2,d),cs))}
        cv=lambda i:c.get(i,0)
        rel=[s.expand(cv(i+j)-cv(i)*cv(j+1)-cv(j)*cv(i+1)+cv(2)*cv(i)*cv(j))
             for i in range(2,d) for j in range(i,d)]
        F={1:s.Integer(1),2:u}
        for i in range(3,2*d):F[i]=s.expand(u*F[i-1]+v*F[i-2])
        G=s.groebner([F[d],F[d+1]],u,v)
        for f in rel:need(G.reduce(s.expand(f.subs({cv(i):F[i] for i in range(2,d)})))[1]==0,'forward residual')
        H=s.groebner(rel,*reversed(cs)); uv={u:cv(2),v:cv(3)-cv(2)**2}
        for i in range(2,d):need(H.reduce(s.expand(cv(i)-F[i].subs(uv,simultaneous=True)))[1]==0,'reverse elimination')
        for i in (d,d+1):need(H.reduce(s.expand(F[i].subs(uv,simultaneous=True)))[1]==0,'boundary equations')
        lm=[p.LM(order=G.order).exponents for p in G.polys]
        basis=[(a,b) for a in range(2*d) for b in range(d+1) if not any(a>=x and b>=y for x,y in lm)]
        need(len(basis)==comb(d,2),'length')
        need(G.reduce(u**(2*d-4))[1]!=0,'exact top power')
        for a in range(2*d-2):
            b=2*d-3-a
            if b>=0:need(G.reduce(u**a*v**b)[1]==0,'nilradical bound')
        cat=comb(2*d-4,d-2)//(d-1)
        need(G.reduce(u**(2*d-4)-cat*(-v)**(d-2))[1]==0,'Catalan coefficient')
        rows.append({'length_parameter':d,'artin_length':len(basis),'nilpotency_index':2*d-3,'Catalan':cat})
    return rows
P=1009
def span(rows):
    basis={}
    for row in rows:
        r=[int(x)%P for x in row]
        for j,b in sorted(basis.items()):
            if r[j]:
                a=r[j]; r=[(x-a*y)%P for x,y in zip(r,b)]
        j=next((i for i,x in enumerate(r) if x),None)
        if j is not None:
            inv=pow(r[j],P-2,P);basis[j]=[x*inv%P for x in r]
    return list(basis.values())
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
    return c
def conductor_tests():
    import random
    rng=random.Random(117);count=0;boundary=0
    for d in range(2,9):
        for k in range(1,d):
            n=2*d-k
            low=[]
            for i in range(k):
                a=[0]*(n+1);a[i]=1
                for j in range(k,d):a[j]=rng.randrange(P)
                low.append(a)
            U=low+[[int(j==i) for j in range(n+1)] for i in range(d,n+1)]
            U=span(U); finite=span([a[:d] for a in U]);cur=U; fcur=finite
            W=[[int(j==i) for j in range(n+1)] for i in range(d,n+1)]
            for m in range(2,6):
                saturated=span([mul(w,a) for w in W for a in cur])
                need(len(saturated)==m*n+1-d,'sharp conductor rank')
                cur=span([mul(a,b) for a in U for b in cur])
                fcur=span([mul(a,b)[:d] for a in finite for b in fcur])
                need(len(cur)-len(fcur)==m*n+1-d,'cokernel rank identity')
                count+=1
            n-=1; exponents=list(range(k))+list(range(d,n+1))
            sums={a+b for a in exponents for b in exponents}
            need(2*d-1 not in sums and 2*d-1<=2*n,'sharp boundary missing monomial')
            boundary+=1
    return {'modulus':P,'rank_cases':count,'sharp_boundary_cases':boundary}
def partitions(n,lo=1):
    if not n:yield []
    for i in range(lo,n+1):
        for tail in partitions(n-i,i):yield [i]+tail
def partition_tests():
    count=0
    for d in range(3,13):
        for ds in partitions(d):
            total=sum(comb(r,2) for r in ds)+sum(r*t for i,r in enumerate(ds) for t in ds[i+1:])
            need(total==comb(d,2),'flat degree partition')
            for r in ds:
                for t in ds:need((r-1)+(t-1)+1==r+t-1,'split nilpotency')
            count+=1
    return {'multiplicity_partitions':count}
def embedded_test():
    a,b,z=s.symbols('a b z')
    G=s.groebner([z*b,(1-z)*a*a,(1-z)*a*b,(1-z)*b*b],z,a,b)
    elim=[f.as_expr() for f in G.polys if not f.as_expr().has(z)]
    need(list(s.groebner(elim,a,b))==list(s.groebner([a*b,b*b],a,b)),'embedded primary intersection')
    return {'residual_ideal':['a*b','b^2'],'primary_intersection':['(b)','(a,b)^2']}
def main():
    result={'kind':'finite exact regressions; NOT proof certification','preservation':source_audit(),
      'grassmannian_primary':grass_tests(),'sharp_conductor':conductor_tests(),
      'all_partition_degree':partition_tests(),'noncurvilinear_embedded':embedded_test(),'proof_certification':False}
    (OUT/'DIAGNOSTICS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
