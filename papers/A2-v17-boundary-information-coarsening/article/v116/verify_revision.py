#!/usr/bin/env python3
"""Source preservation and exact finite diagnostics. NOT proof certification.
All ranks use modular Gaussian elimination, never floating point. Symbolic
identities use exact polynomial arithmetic. Run from any working directory.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, re
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
P=1009

def need(ok: bool, msg: str) -> None:
    if not ok: raise RuntimeError(msg)
def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def expand(path: Path, seen: set[Path]|None=None) -> str:
    seen=set() if seen is None else set(seen)
    need(path not in seen,'recursive input '+str(path)); seen.add(path)
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(HERE/m.group(1),seen),path.read_text())
def norm(s: str) -> str: return re.sub(r'\s+',' ',s).strip()
def source_checks() -> dict:
    manifest=json.loads((HERE/'evidence/V115_SOURCE_MANIFEST.json').read_text())
    olds=manifest['tex_sha256']; need(len(olds)==24,'incomplete pinned source manifest')
    oldall=[]; identical=[]; count=0
    env=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}'
    for name,digest in olds.items():
        archived=HERE/'history/v115_source'/name
        need(sha(archived)==digest,'archive hash changed '+name)
        active=HERE/name; need(active.exists(),'removed source '+name)
        old=archived.read_text(); new=active.read_text(); oldall.append(old)
        if sha(active)==digest: identical.append(name)
        for block in re.finditer(env,old):
            need(norm(block.group()) in norm(new),'lost or changed old proof/theorem '+name+' '+block.group()[:80]); count+=1
    full=expand(HERE/'paper.tex'); old='\n'.join(oldall)
    labels=re.findall(r'\\label\{([^}]+)\}',full)
    need(len(labels)==len(set(labels)),'duplicate source labels')
    prior=set(re.findall(r'\\label\{([^}]+)\}',old)); need(prior<=set(labels),'old label lost')
    refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',full)); need(refs<=set(labels),'missing refs '+str(refs-set(labels)))
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',full)); oldkeys=set(re.findall(r'\\bibitem\{([^}]+)\}',old)); need(oldkeys<=keys,'old bibliography key lost')
    cites={k.strip() for q in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',full) for k in q.split(',')}
    need(cites<=keys,'missing citations '+str(cites-keys))
    abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',full).group(1)
    need(len(abstract.split())<=200,'abstract too long')
    return {'controlling_review_commit':manifest['review_commit'],'reviewed_revision_commit':manifest['reviewed_revision_commit'],'archived_tex_files':len(olds),'byte_identical_active_files':len(identical),'byte_identical_paths':identical,'retained_old_theorem_and_proof_blocks':count,'retained_old_labels':len(prior),'current_labels':len(labels),'retained_old_bibliography_keys':len(oldkeys),'current_bibliography_keys':len(keys),'abstract_words':len(abstract.split()),'universal_proof_certification':False}

def trim(a):
    a=[int(x)%P for x in a]
    while len(a)>1 and a[-1]==0: a.pop()
    return a
def add(a,b): return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%P
    return trim(c)
def rem(a,g):
    a=trim(a); g=trim(g)
    while len(a)>=len(g) and a!=[0]:
        s=len(a)-len(g); v=a[-1]*pow(g[-1],-1,P)%P
        for j,x in enumerate(g): a[s+j]=(a[s+j]-v*x)%P
        a=trim(a)
    return a
def rows_basis(rows,width=None):
    if not rows: return []
    width=max(map(len,rows)) if width is None else width
    pivots={}
    for row in rows:
        a=[int(x)%P for x in row]+[0]*(width-len(row))
        for j in range(width):
            if a[j]==0: continue
            if j in pivots:
                v=a[j]; b=pivots[j]; a=[(x-v*y)%P for x,y in zip(a,b)]
            else:
                inv=pow(a[j],-1,P); pivots[j]=[(x*inv)%P for x in a]; break
    return [pivots[j] for j in sorted(pivots)]
def solve_square(matrix,rhs):
    a=[[int(x)%P for x in row]+[int(y)%P] for row,y in zip(matrix,rhs)]; n=len(a)
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]); a[j],a[k]=a[k],a[j]
        inv=pow(a[j][j],-1,P); a[j]=[(x*inv)%P for x in a[j]]
        for k in range(n):
            if k!=j:
                v=a[k][j]; a[k]=[(x-v*y)%P for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]
def hermite(parts,jets):
    d=sum(parts); matrix=[]; rhs=[]; g=[1]
    for x,(di,jet) in enumerate(zip(parts,jets)):
        for r in range(di):
            matrix.append([0 if j<r else math.comb(j,r)*pow(x,j-r,P)%P for j in range(d)]); rhs.append(jet[r])
        for _ in range(di): g=mul(g,[-x,1])
    return g,trim(solve_square(matrix,rhs))
def expected_s(parts,jets):
    groups={}
    for di,jet in zip(parts,jets):
        e=next((j for j in range(1,di) if jet[j]%P),di)
        groups[jet[0]%P]=max(groups.get(jet[0]%P,0),(di+e-1)//e)
    return sum(groups.values())
def global_diagnostics():
    records=[]
    partitions=[(4,),(3,1),(2,2),(2,1,1),(1,1,1,1),(5,),(3,2),(2,2,1),(1,1,1,1,1)]
    for parts in partitions:
        d=sum(parts)
        for mode in ('separated','ramified','one_collision','all_collide'):
            jets=[]
            for i,di in enumerate(parts):
                value=7+i if mode in ('separated','ramified') else (7 if mode=='all_collide' or i<2 else 7+i)
                j=[value]+[(r+2+i)%P for r in range(1,di)]
                if mode=='ramified' and di>=2: j[1]=0
                jets.append(j)
            if all(all(x==0 for x in j[1:]) for j in jets) and len({j[0] for j in jets})==1: continue
            g,v=hermite(parts,jets); s=expected_s(parts,jets)
            for offset in (0,1):
                n=2*d-1+offset; a=[2,1]; b=rem(mul(a,v),g)
                W=[[0]*i+g for i in range(n-d+1)]
                U=rows_basis(W+[a,b],n+1); need(len(U)==n-d+3,'pencil lift dimension')
                span=U; power=[1]; powers=[[1]]
                for _ in range(1,6): power=rem(mul(power,v),g); powers.append(power)
                for m in range(2,6):
                    prev=span
                    span=rows_basis([mul(x,y) for x in prev for y in U],m*n+1)
                    cond=rows_basis([mul(x,y) for x in W for y in prev],m*n+1)
                    finite=rows_basis(powers[:m+1],d)
                    corank=m*n+1-len(span); pred=d-min(m+1,s)
                    need(corank==pred,'global corank '+str((parts,mode,n,m,corank,pred)))
                    need(len(cond)==m*n+1-d,'conductor surjectivity '+str((parts,mode,n,m)))
                    need(len(finite)==min(m+1,s),'minimal polynomial formula')
                    records.append({'partition':parts,'mode':mode,'n':n,'m':m,'global_corank':corank,'finite_rank':len(finite),'conductor_rank':len(cond),'s':s})
    return {'prime':P,'cases':len(records),'records':records,'not_universal_proof':True}

def symbolic_diagnostics():
    z,t=sp.symbols('z t'); records=[]
    for parts in ((4,),(3,1),(2,2),(2,1,1),(1,1,1,1),(5,),(3,2)):
        d=sum(parts); ls=sp.symbols('l0:'+str(len(parts))); rows=[]; expected=sp.Integer(1)
        for i,di in enumerate(parts):
            cs=sp.symbols('c'+str(i)+'_1:'+str(di)) if di>1 else []
            v=ls[i]+sum(cs[r-1]*z**r for r in range(1,di))
            columns=[sp.Poly(sp.expand(v**j),z) for j in range(d)]
            rows.extend([[q.nth(r) for q in columns] for r in range(di)])
            if di>1: expected*=cs[0]**math.comb(di,2)
        for i in range(len(parts)):
            for j in range(i+1,len(parts)): expected*=(ls[j]-ls[i])**(parts[i]*parts[j])
        determinant=sp.Matrix(rows).det(method='domain-ge')
        need(sp.expand(determinant-expected)==0,'confluent determinant '+str(parts))
        records.append({'partition':parts,'determinant_identity':True,'formula':str(expected)})
    g=t**3*(t-1); v=t**2; d=4
    coeffs=sp.symbols('g0:4'); gg=t**4+sum(coeffs[i]*t**i for i in range(4))
    cols=[sp.Poly(sp.rem((t*t)**j,gg,t),t) for j in range(d)]
    Delta=sp.factor(sp.Matrix([[q.nth(i) for q in cols] for i in range(d)]).det())
    point={coeffs[0]:0,coeffs[1]:0,coeffs[2]:0,coeffs[3]:-1}
    gradient=[sp.diff(Delta,x).subs(point) for x in coeffs]
    need(Delta.subs(point)==0 and any(x!=0 for x in gradient),'smooth total / triple fibre example')
    normalization=[]
    for h,q,w,lam in [(t*t,t*(t-1),1,0),(t*t-1,(t-2)*(t-3),t+2,4),(t*t,t*t,t,3)]:
        gg=sp.expand(h*q); vv=sp.expand(lam+h*w)
        columns=[sp.Poly(sp.rem(vv**j,gg,t),t) for j in range(4)]
        need(sp.Matrix([[x.nth(i) for x in columns] for i in range(4)]).det()==0,'normalization parametrization')
        normalization.append({'g':str(gg),'v':str(vv),'determinant_zero':True})
    layer_cases=0
    for exponents in itertools.product(range(1,7),repeat=3):
        for q in range(1,max(exponents)+2):
            target=tuple(max(e-q,0) for e in exponents)
            for a in ((0,0,0),(1,2,3),(6,6,6),target):
                need(all(x+q>=e for x,e in zip(a,exponents))==all(x>=e for x,e in zip(a,target)),'nilradical colon exponents')
            layer_cases+=1
    return {'confluent_identities':records,'normalization_examples':normalization,'smooth_total_nonreduced_fibre':{'g':str(g),'v':str(v),'determinant_with_v_t_squared':str(Delta),'gradient_in_g':list(map(str,gradient)),'fixed_fibre_nilpotency':3},'nilradical_colon_cases':layer_cases,'not_universal_proof':True}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-only',action='store_true'); args=ap.parse_args()
    out={'result':'PASS','kind':'exact finite diagnostics and source preservation; NOT universal proof certification','source':source_checks()}
    if not args.source_only: out.update({'global_contact_cases':global_diagnostics(),'symbolic':symbolic_diagnostics()})
    target=HERE/'evidence'/('SOURCE_CHECKS.json' if args.source_only else 'DIAGNOSTICS.json')
    target.parent.mkdir(exist_ok=True); target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','source':out['source'],'global_cases':out.get('global_contact_cases',{}).get('cases'),'receipt':str(target)},indent=2))
if __name__=='__main__': main()
