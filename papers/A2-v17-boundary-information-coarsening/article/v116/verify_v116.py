#!/usr/bin/env python3
"""Finite exact algebra and source-preservation checks; not a proof assistant.

Run from any directory.  --git-baseline additionally checks the frozen R115
Git object.  --extended computes the quartic m=4 Groebner comparison, which
is substantially slower and is not required by the ordinary build.
"""
from __future__ import annotations
import argparse, hashlib, itertools as it, json, re, subprocess
from collections import Counter
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE='1cb4e00c86699247454d21dbec2dcce01a9c6b8b'
PREFIX='papers/A2-v17-boundary-information-coarsening/article/v115/'
P=1009

def need(ok:bool,msg:str)->None:
    if not ok:raise AssertionError(msg)

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def expand(path:Path,seen:frozenset[Path]=frozenset())->str:
    need(path not in seen,'recursive input')
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(HERE/m[1],seen|{path}),path.read_text())

def source_checks(git_baseline:bool)->dict:
    man=json.loads((HERE/'evidence/V115_SOURCE_MANIFEST.json').read_text())
    env=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}'
    count=0;identical=[];oldtext=[]
    if git_baseline:
        root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip())
    for name,digest in man['tex_sha256'].items():
        old=(HERE/'history/v115_source'/name).read_bytes()
        need(sha(old)==digest,'archive digest '+name)
        if git_baseline:
            remote=subprocess.check_output(['git','show',BASE+':'+PREFIX+name],cwd=root)
            need(remote==old,'frozen Git baseline '+name)
        new=(HERE/name).read_bytes();oldtext.append(old.decode())
        if old==new:identical.append(name)
        for block in re.finditer(env,old.decode()):
            need(block[0] in new.decode(),'old mathematical block changed '+name)
            count+=1
    text=expand(HERE/'paper.tex');old='\n'.join(oldtext)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',old))
    need(len(labels)==len(set(labels)),'duplicate labels')
    need(oldlabels<=set(labels),'old label lost')
    refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text))
    need(refs<=set(labels),'undefined refs '+str(refs-set(labels)))
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    oldkeys=set(re.findall(r'\\bibitem\{([^}]+)\}',old))
    need(oldkeys<=keys,'old bibliography key lost')
    cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in c.split(',')}
    need(cites<=keys,'undefined bibliography key')
    abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',text)[1]
    need(len(abstract.split())<=200,'abstract over 200 words')
    apps=(HERE/'paper.tex').read_text().split(r'\appendix',1)[1]
    applabels=set(re.findall(r'\\label\{([^}]+)\}',re.sub(r'\\input\{([^}]+)\}',lambda m:expand(HERE/m[1]),apps)))
    for name in ['02k-quartic-primary.tex','02l-conductor-primary.tex']:
        part=(HERE/'parts'/name).read_text()
        dep=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',part))
        need(not dep&applabels,'new geometry depends on application label')
    return {'frozen_review_commit':BASE,'git_baseline_checked':git_baseline,'archived_active_tex_files':len(man['tex_sha256']),
            'old_theorem_and_proof_blocks_retained_verbatim':count,'old_labels_preserved':len(oldlabels),
            'old_bibliography_keys_preserved':len(oldkeys),'current_labels':len(labels),
            'unchanged_active_tex_files':len(identical),'unchanged_paths':identical,
            'abstract_words':len(abstract.split()),'new_geometry_has_no_application_dependencies':True}

def residual(n:int,m:int):
    t=sp.Symbol('t');hs=sp.symbols('h2:'+str(n+1));h={1:sp.S.Zero,**dict(zip(range(2,n+1),hs))};cols={}
    for ids in it.combinations_with_replacement(range(1,n+1),m):
        f=sp.Poly(sp.prod(t**j-h[j] for j in ids),t)
        cols[ids]=[sp.expand(f.nth(k)) for k in range(m*n+1)]
    piv={}
    for ids in cols:piv.setdefault(sum(ids),ids)
    need(set(piv)==set(range(m,m*n+1)),'missing monic pivot')
    out=[]
    for ids,c0 in cols.items():
        if ids in piv.values():continue
        c=c0.copy()
        for k in range(m*n,m-1,-1):
            v=c[k]
            if v:
                p=cols[piv[k]]
                for j in range(k+1):
                    if p[j]:c[j]=sp.expand(c[j]-v*p[j])
        if any(c[:m]):out.append(c[:m])
    R=sp.Matrix(m,len(out),lambda i,j:out[j][i])
    for k in range(m):
        for x in R.row(k):
            if x:need(min(sum(mon) for mon,co in sp.Poly(x,*hs).terms() if co)>=m-k,'row filtration')
    return hs,R

def quartic_exact(m:int)->dict:
    hs,R=residual(4,m);a,b,c=hs;C=sp.Symbol('C');F=a*c-b*b-a**3;quot=[];num=0
    for indices in it.combinations(range(R.cols),m):
        det=sp.expand(R[:,indices].det(method='domain-ge'))
        if not det:continue
        q,r=sp.div(det,F,*hs);need(r==0,'minor not divisible by secant equation')
        quot.append(sp.expand(q.subs(c,C+a*a)));num+=1
    G=sp.groebner(quot,a,b,C,order='grevlex');T=m*(m+1)//2
    mons=[sp.prod((a,b,C)[i] for i in ids) for ids in it.combinations_with_replacement(range(3),T-2)]
    target=sp.groebner(mons,a,b,C,order='grevlex')
    need(G==target,'quartic full ideal mismatch')
    return {'m':m,'residual_shape':list(R.shape),'nonzero_maximal_minors':num,'quotient_groebner_generators':len(G.polys),
            'T':T,'quotient_ideal':'(A,B,C)^'+str(T-2),'equality_over':'Q','exact_nilpotency_index':(T+1)//2}

def spanning_induction()->dict:
    coverage=[]
    # This enumerates the monomials in the proof, not the exponentially larger minors.
    for m in range(2,17):
        K=(m+1)*(m+2)//2-2;ordinary=exceptional=0
        for a in range(K+1):
            for b in range(K-a+1):
                c=K-a-b;deficit=2*a+b
                if deficit>=3:
                    found=False
                    for ap in range(min(a,m+1)+1):
                        for bp in range(min(b,m+1-ap)+1):
                            cp=m+1-ap-bp
                            if cp<=c and 2*ap+bp>=3:found=True;break
                        if found:break
                    need(found,'induction factor missing');ordinary+=1
                else:
                    need((a,b) in [(0,0),(0,1),(1,0),(0,2)],'unlisted exceptional monomial');exceptional+=1
        need(exceptional==4,'exception count');coverage.append({'from_m':m,'ordinary':ordinary,'exceptional':exceptional})
    A,B,C=sp.symbols('A B C');F=A*C-B*B
    base=sp.Matrix([[B,C,0],[-A*A,-A*B,F]])
    need([sp.expand(base[:,j].det()) for j in [(0,1),(0,2),(1,2)]]==[sp.expand(A*F),sp.expand(B*F),sp.expand(C*F)],'base minors')
    exc=sp.Matrix([[C,0,0],[-A*B,F,0],[0,0,C*F]])
    need(sp.expand(exc.det()-C*C*F*F)==0,'exceptional determinant')
    need(sp.expand(A*C**3*F-C*C*F*F-B*B*C*C*F)==0,'exceptional completion')
    return {'coverage':coverage,'symbolic_base_and_exceptional_identities':True,'not_a_universal_proof':True}

def convolution(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
    return c

def rank_mod(rows:list[list[int]])->int:
    if not rows:return 0
    M=[[int(v)%P for v in row] for row in rows];r=0
    for j in range(len(M[0])):
        k=next((i for i in range(r,len(M)) if M[i][j]),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r];inv=pow(M[r][j],-1,P);M[r]=[x*inv%P for x in M[r]]
        for i in range(r+1,len(M)):
            if M[i][j]:
                fac=M[i][j];M[i]=[(x-fac*y)%P for x,y in zip(M[i],M[r])]
        r+=1
        if r==len(M):break
    return r

def conductor_ranks()->dict:
    t=sp.Symbol('t');cases=[]
    data=[([(0,1),(1,1),(2,1),(3,1)],t), ([(0,1),(1,1),(2,1),(3,1)],t*(t-1)),
          ([(0,5)],t), ([(0,5)],t*t), ([(0,5)],t**3),
          ([(0,3),(1,2)],t), ([(0,3),(1,2)],t*t),
          ([(0,3),(1,2)],t*(t-1)), ([(0,3),(1,2)],t*t*(t-1))]
    for support,b in data:
        d=sum(e for _,e in support);n=2*d-1;g=sp.Poly(sp.prod((t-p)**e for p,e in support),t)
        def coeff(f):return [int(sp.Poly(f,t).nth(i))%P for i in range(n+1)]
        basis=[coeff(g.as_expr()*t**j) for j in range(n-d+1)]+[coeff(1),coeff(b)]
        heights={};jets=[]
        for point,e in support:
            lam=int(b.subs(t,point))%P
            ri=next((j for j in range(1,e) if int(sp.diff(b,t,j).subs(t,point)/sp.factorial(j))%P),e)
            heights[lam]=max(heights.get(lam,0),(e+ri-1)//ri);jets.append([point,e,lam,ri])
        q=sum(heights.values())
        for m in sorted(set([2,d-1,d])):
            rows=[]
            for ids in it.combinations_with_replacement(range(len(basis)),m):
                a=[1]
                for idx in ids:a=convolution(a,basis[idx])
                rows.append(a+[0]*(m*n+1-len(a)))
            rank=rank_mod(rows);expected=d-min(m+1,q)
            need(m*n+1-rank==expected,'conductor corank mismatch')
            cases.append({'support':support,'b':str(b),'n':n,'m':m,'q':q,'jets':jets,'corank':expected})
    return {'prime':P,'cases':cases,'count':len(cases),'not_a_universal_proof':True}

def index_forms()->dict:
    records=[];t=sp.Symbol('t')
    for es in [(1,1,1),(2,1),(3,),(2,2),(3,2),(4,)]:
        d=sum(es);rows=[];lams=[];first=[]
        for i,e in enumerate(es):
            coeff=sp.symbols('z'+str(i)+'_0:'+str(e));lams.append(coeff[0]);first.append(coeff[1] if e>1 else sp.Integer(1))
            z=sum(c*t**j for j,c in enumerate(coeff))
            pp=[sp.Poly(sp.expand(z**k),t) for k in range(d)]
            rows.extend([[p.nth(j) for p in pp] for j in range(e)])
        determinant=sp.expand(sp.Matrix(rows).det(method='domain-ge'))
        expected=sp.prod(first[i]**(e*(e-1)//2) for i,e in enumerate(es))*sp.prod((lams[j]-lams[i])**(es[i]*es[j]) for i in range(len(es)) for j in range(i+1,len(es)))
        need(sp.expand(determinant-expected)==0,'confluent determinant mismatch '+str(es))
        records.append({'multiplicities':es,'identity_over':'Z[jet coefficients]','factorization':str(expected)})
    return {'cases':records,'count':len(records)}

def main()->None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-only',action='store_true');p.add_argument('--git-baseline',action='store_true');p.add_argument('--extended',action='store_true');args=p.parse_args()
    result={'kind':'finite diagnostics and source checks, not formal proof certification','source':source_checks(args.git_baseline)}
    if not args.source_only:
        result.update({'quartic_exact':[quartic_exact(m) for m in ([2,3,4] if args.extended else [2,3])],
                       'weighted_induction':spanning_induction(),'contact_index_forms':index_forms(),'conductor_ranks':conductor_ranks()})
    dest=HERE/'evidence'/('V116_SOURCE_CHECKS.json' if args.source_only else 'V116_DIAGNOSTICS.json');dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','receipt':str(dest),'source':result['source']},indent=2))
if __name__=='__main__':main()
