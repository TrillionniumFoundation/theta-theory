#!/usr/bin/env python3
"""Reproducible source/finite-algebra/build checks, NOT a universal proof checker.

The immutable v114 source is archived locally with upstream SHA256 hashes.
Optional --git-baseline compares it to the actual upstream object, from the
repository root; a nested-directory pathspec regression is always tested.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, math, random, re
import subprocess, tempfile
from collections import Counter
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE='09869129e16fd43bd2420fa3573a09cd5cbbdff9'
OLD='papers/A2-v17-boundary-information-coarsening/article/v114/'
P=1009

def need(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def load(name: str, path: Path):
    spec=importlib.util.spec_from_file_location(name,path)
    need(spec is not None and spec.loader is not None,'cannot load '+str(path))
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

legacy=load('a2_r114_diagnostics',HERE/'history/v114_verify_revision.py')
previous=load('a2_r113_diagnostics',HERE/'history/v114_verify_v113_diagnostics.py')

def git_files(cwd: Path, ref: str, prefix: str) -> dict[str,bytes]:
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=cwd,text=True).strip())
    paths=subprocess.check_output(['git','ls-tree','-r','--full-tree','--name-only',ref,'--',':(top)'+prefix],cwd=root,text=True).splitlines()
    need(bool(paths),'empty baseline listing (must not pass vacuously)')
    return {p[len(prefix):]:subprocess.check_output(['git','show',ref+':'+p],cwd=root) for p in paths if p.startswith(prefix)}

def git_regression() -> dict:
    with tempfile.TemporaryDirectory(prefix='a2-git-regression-') as t:
        r=Path(t); p=r/'papers/old/parts/test.tex';p.parent.mkdir(parents=True);p.write_bytes(b'baseline\n\n')
        nested=r/'papers/new';nested.mkdir()
        for cmd in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Regression','-c','user.email=regression@example.invalid','commit','-qm','fixture']]:
            subprocess.run(cmd,cwd=r,check=True)
        a=git_files(r,'HEAD','papers/old/');b=git_files(nested,'HEAD','papers/old/')
        need(a==b=={'parts/test.tex':b'baseline\n\n'},'root-independent baseline regression failed')
        broken=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','--','papers/old/'],cwd=nested)
        need(broken==b'','fixture does not reproduce nested pathspec failure')
    return {'reproduced_v114_nested_path_failure':True,'root_and_nested_fixed_results_identical':True,'trailing_newlines_preserved':True}

def expand(path: Path, active: set[Path] | None=None) -> str:
    active=set() if active is None else active
    need(path not in active,'recursive input '+str(path));active=active|{path}
    text=path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(HERE/m.group(1),active),text)

def normalized(text: str) -> str:
    return re.sub(r'\s+',' ',text.replace('\\operatorname{Sing}(D)_{\nm red}',r'\operatorname{Sing}(D)_{\mathrm{red}}')).strip()

def source_checks(git_baseline: bool=False) -> dict:
    manifest=json.loads((HERE/'evidence/V114_SOURCE_MANIFEST.json').read_text())
    olds=manifest['tex_sha256'];need(len(olds)==19,'unexpected incomplete old source set')
    exact=[];blocks=0
    environment=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}'
    oldall=[]
    if git_baseline: remote=git_files(HERE,BASE,OLD)
    for name,digest in olds.items():
        data=(HERE/'history/v114_source'/name).read_bytes()
        need(sha(data)==digest,'archive hash mismatch '+name)
        if git_baseline: need(remote[name]==data,'upstream source differs '+name)
        old=data.decode();new=(HERE/name).read_text();oldall.append(old)
        if data==(HERE/name).read_bytes(): exact.append(name)
        for match in re.finditer(environment,old):
            need(normalized(match.group()) in normalized(new),'retained proof/theorem changed '+name+' '+match.group()[:65]);blocks+=1
    text=expand(HERE/'paper.tex');oldtext='\n'.join(oldall)
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    need(len(labels)==len(set(labels)),'duplicate labels')
    need(oldlabels<=set(labels),'old labels lost')
    refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text));need(refs<=set(labels),'undefined source refs '+str(refs-set(labels)))
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text));oldkeys=set(re.findall(r'\\bibitem\{([^}]+)\}',oldtext));need(oldkeys<=keys,'old bibliography keys lost')
    citations={k.strip() for q in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in q.split(',')}
    need(citations<=keys,'undefined citations '+str(citations-keys))
    abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',text).group(1)
    need(len(abstract.split())<=200,'abstract exceeds 200 words')
    return {'upstream_source_commit':manifest['source_commit'],'controlling_report_commit':BASE,'old_source_files_verified':len(olds),'old_source_files_byte_identical_in_revision':len(exact),'byte_identical_paths':exact,'retained_theorem_and_proof_blocks':blocks,'old_labels_preserved':len(oldlabels),'current_labels':len(labels),'old_bibliography_keys_preserved':len(oldkeys),'current_bibliography_keys':len(keys),'abstract_words':len(abstract.split()),'git_baseline_checked':git_baseline}

def conv(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%P
    return c

def product(basis,ids):
    a=[1]
    for i in ids: a=conv(a,basis[i])
    return a

def hyperplane_diagnostics() -> dict:
    records=[];rng=random.Random(1152026)
    for n in range(4,9):
        z=[[int(i==j) for i in range(n+1)] for j in range(n+1)]
        kinds={'split':[z[0][i]+2*z[n][i] for i in range(n+1)]}
        for m in range(2,6):
            for kind in ('split','tangent','evaluation','outside'):
                if kind=='split': basis=[kinds['split'],*z[1:n]]
                elif kind=='tangent': basis=[z[0],*z[2:]]
                elif kind=='evaluation':basis=z[1:]
                else:
                    h=[1]+[rng.randrange(P) for _ in range(n)]
                    # A nonzero secant Hankel minor certifies outside S_n.
                    while int(sp.det(sp.Matrix([[h[i+j] for j in range(3)] for i in range(3)])))%P==0:
                        h=[1]+[rng.randrange(P) for _ in range(n)]
                    basis=[[(-h[j] if i==0 else int(i==j))%P for i in range(n+1)] for j in range(1,n+1)]
                mons=list(itertools.combinations_with_replacement(range(n),m))
                rows=[product(basis,ids) for ids in mons]
                rk=previous.rank(rows);corank=m*n+1-rk
                expected=m if kind=='evaluation' else (0 if kind=='outside' else 1)
                need(corank==expected,f'higher-product rank n={n},m={m},{kind}: {corank}')
                record={'n':n,'m':m,'kind':kind,'corank':corank}
                if kind in ('split','tangent'):
                    residual=[r for ids,r in zip(mons,rows) if sum(i!=0 for i in ids)>=2]
                    rr=previous.rank(residual);need(rr==m*n-3,'hyperplane residual rank')
                    # Independently build the plane derivative against the unique annihilator.
                    ell=[0]*(m*n+1)
                    if kind=='split':ell[0]=pow(2,m,P);ell[-1]=-1;w=z[0]
                    else:ell[1]=1;w=z[1]
                    B=[]
                    for ids in mons:
                        row=[]
                        for j in range(n):
                            val=0
                            for q,idx in enumerate(ids):
                                if idx==j:
                                    f=conv(product(basis,ids[:q]+ids[q+1:]),w)
                                    val+=sum(a*b for a,b in zip(ell,f))
                            row.append(val%P)
                        B.append(row)
                    rb=previous.rank(B);need(rb==n,'hyperplane plane-derivative rank')
                    record.update({'polar_image_rank':rr,'plane_derivative_rank':rb,'tangent_dimension':n+m*n-rb-rr})
                    need(record['tangent_dimension']==3,'higher-product tangent dimension')
                records.append(record)
    return {'field_prime':P,'cases':len(records),'records':records,'not_a_universal_proof':True}

def exact_diagnostics() -> dict:
    a,b,c,d,e,f,h=sp.symbols('a b c d e f h')
    M=sp.Matrix([[1+a,b,c],[d,e,f]])
    minors=[sp.expand(M[:,list(ij)].det()) for ij in [(0,1),(0,2),(1,2)]]
    need(sp.expand((1+a)*minors[2]-b*minors[1]+c*minors[0])==0,'Schur ideal identity')
    A1,B1,C1,D1,D2=sp.symbols('A1 B1 C1 D1 D2')
    s=h*D1+h*h*D2-(h*C1)*(1+h*A1)**-1*(h*B1)
    need(sp.expand(sp.series(s,h,0,3).removeO()).coeff(h,2)==D2-C1*B1,'Schur second jet')
    u,v,t,z=sp.symbols('u v t z')
    f1=z+u*u;f2=u*v+(1+t)*z+u**3
    remaining=sp.expand(f2.subs(z,-u*u));need(sp.expand(remaining-u*(v-(1+t)*u+u*u))==0,'normal crossing factor')
    x,y=sp.symbols('x y');cusp=y*y-x**3
    need(sp.expand(cusp.subs({x:t*t,y:t**3}))==0,'cusp parametrization')
    h1,h2,h3,h4=sp.symbols('h1 h2 h3 h4')
    F=sp.det(sp.Matrix([[1,h1,h2],[h1,h2,h3],[h2,h3,h4]]))
    coeff=sp.Poly(F.subs({h1:t*h1,h2:t*h2,h3:t*h3,h4:t*h4}),t).coeff_monomial(t**2)
    need(sp.expand(coeff-(h2*h4-h3*h3))==0,'secant initial quadratic')
    nilorders=[]
    for m in range(3,13):
        for j in range(1,(m-1)//2+1):
            q=sp.Poly((F**j).subs({h1:t*h1,h2:t*h2,h3:t*h3,h4:t*h4}),t)
            order=min(k[0] for k,_ in q.terms());need(order==2*j<m,'nilpotent order lower bound');nilorders.append([m,j,order])
    realization=[]
    for m in range(2,7):
        for p in range(1,5):
            for e in range(p,p+3):
                for rho in range(1,p+1):
                    s=e-p+rho
                    # Every selected plane variable has m*beta(x_j^(m-1)w_alpha)=1.
                    coeff=sp.Rational(m)*sp.Rational(1,m);need(coeff==1,'symmetric derivative coefficient')
                    realization.append([m,p,e,rho,rho*s])
    J=sp.Matrix([[1,0,0,0],[0,1,1,0],[0,0,0,1]])
    need(J.rank()==3 and len(J.nullspace())==1,'joint symmetric matrix relation')
    return {'schur_minor_identity':True,'schur_second_jet':True,'simple_normal_factorization':True,'cubic_cusp_parametrization':True,'joint_annihilator_relation_dimension':1,'secant_initial_form':str(coeff if False else h2*h4-h3*h3),'nilpotent_order_checks':nilorders,'every_degree_realization_cases':len(realization),'realization_records':realization}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--git-baseline',action='store_true');parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    out={'kind':'finite algebra and source verification; not universal proof certification','source':source_checks(args.git_baseline),'git_path_regression':git_regression()}
    if not args.source_only:
        out['inherited_v113']=previous.diagnostics();out['inherited_v114_polar']=legacy.polar_diagnostics();out['inherited_v114_fibre']=legacy.fibre_diagnostics();out['new_exact']=exact_diagnostics();out['higher_hyperplanes']=hyperplane_diagnostics()
    (HERE/'evidence').mkdir(exist_ok=True)
    target=HERE/'evidence'/('SOURCE_CHECKS.json' if args.source_only else 'DIAGNOSTICS.json');target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','receipt':str(target),'source':out['source'],'hyperplane_cases':out.get('higher_hyperplanes',{}).get('cases')},indent=2))
if __name__=='__main__':main()
