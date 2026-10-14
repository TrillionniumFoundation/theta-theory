#!/usr/bin/env python3
"""Exact-source replay and finite checks; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import comb, log, exp
import hashlib
import json
import re
import mpmath as mp
import verify_v11
import verify_v13
import verify_v14
import verify_v15

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v15-referee-response'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks() -> dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==16,'revision')
    require(ledger['baseline']==man['author_baseline_commit'],'baseline identity')
    by_path={}
    for e in ledger['edits']:by_path.setdefault(e['path'],[]).append(e)
    inherited=sorted((BASE/'core').glob('*.tex'))+[BASE/'main.tex',BASE/'references.tex']
    require(len(inherited)==37,'baseline incomplete')
    for p in inherited:
        rel=p.relative_to(BASE).as_posix()
        require(digest(p)==man['baseline_sha256'][rel],'baseline hash '+rel)
        text=p.read_text()
        for e in by_path.get(rel,[]):
            require(text.count(e['before'])==1,'edit not unique '+rel)
            text=text.replace(e['before'],e['after'],1)
        require(text.encode()==(ROOT/rel).read_bytes(),'unreported inherited edit '+rel)
    require(set(by_path)=={'main.tex','references.tex'},'unexpected inherited modification')
    old_scripts=sorted((BASE/'tools').glob('*.py'))
    for p in old_scripts:
        require(p.read_bytes()==(ROOT/'tools'/p.name).read_bytes(),'inherited Python '+p.name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and not any(x in ('build','evidence','__pycache__') for x in p.parts)
            and p.name!='SOURCE_MANIFEST.json'}
    require(actual==set(man['source_sha256']),'incomplete source hash map')
    for rel,h in man['source_sha256'].items():require(digest(ROOT/rel)==h,'source hash '+rel)
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 16' in main,'version metadata')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    require(len(inputs)==len(set(inputs))==37,'core inclusions')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unincluded core')
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldtex='\n'.join(p.read_text() for p in inherited)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)),'duplicate label')
    require(oldlabels<=set(labels),'deleted label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined reference '+str(refs-set(labels)))
    olditems=set(re.findall(r'\\bibitem\{([^}]+)\}',(BASE/'references.tex').read_text()))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    require(olditems<=items and items-olditems=={'BPR'},'bibliography')
    cites=set()
    for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(x.strip() for x in g.split(','))
    require(cites<=items,'undefined bibliography')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'environment '+env)
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex),'TeX control character')
    required={'thm:intro-actual-return-defects','thm:near-origin-circle-defect','thm:near-origin-vector-defect',
              'lem:finite-record-variation','lem:exact-tower-defect','prop:tower-bv-approximation',
              'thm:actual-return-circle-defect','thm:actual-return-vector-defect','cor:actual-annulus-defect',
              'thm:joint-uniform-nondegeneracy','thm:LLT','lem:raw-residual-sum'}
    require(required<=set(labels),'load-bearing result missing')
    for key in ('full_raw_LLT_proved','full_complementary_integral_proved','raw_second_derivative_sum_proved','anisotropic_to_BV_reconstruction_proved'):
        require(man[key] is False,'unsupported full closure flag '+key)
    return {'included_core_files':len(inputs),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'inherited_core_byte_identical':35,
            'inherited_python_files_byte_identical':len(old_scripts),'exact_edits':len(ledger['edits']),
            'retained_bibliography_items':len(olditems),'new_bibliography_items':['BPR'],
            'verified_file_count':len(actual),'source_sha256':man['source_sha256']}

# Gaussian-rational complex arithmetic makes the finite identities exact.
def add(z,w):return(z[0]+w[0],z[1]+w[1])
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def scale(a,z):return(a*z[0],a*z[1])
def conj(z):return(z[0],-z[1])
def sub(z,w):return add(z,scale(-1,w))
def square(z):return z[0]*z[0]+z[1]*z[1]
ONE=(F(1),F(0)); ZERO=(F(0),F(0)); UNITS=[ONE,(F(0),F(1)),(-ONE[0],F(0)),(F(0),F(-1))]
def sumz(values):
    result=ZERO
    for z in values:result=add(result,z)
    return result

def finite_checks() -> dict:
    mp.mp.dps=60
    tower=0; age=0; wrong_top_norm=0
    for size,Y in ((11,[0,2,7]),(17,[0,3,10,13]),(23,[0,1,8,15,19])):
        k=len(Y); c=F(k,size)
        eta=[int(i in Y) for i in range(size)]
        a=[(i*i+3*i+1)%7-3 for i in range(size)]
        total=sum(a)
        # z*h is recorded in quarter turns, so all phases are exact.
        increments=[k*a[i]-total*eta[i] for i in range(size)]
        require(sum(increments)==0,'compensation mean')
        lengths=[(Y[(j+1)%k]-Y[j])%size for j in range(k)]
        for mode in range(4):
            f=[scale(F((j+mode)%4,2) if mode else F(1),UNITS[(2*j+mode)%4]) for j in range(k)]
            Q=[None]*size; ages=[None]*size; topdef=[]; retdef=[]
            for j,y in enumerate(Y):
                phase=0
                for t in range(lengths[j]):
                    x=(y+t)%size
                    require(Q[x] is None,'tower levels overlap')
                    Q[x]=mul(UNITS[phase%4],f[j]);ages[x]=t
                    phase+=increments[x]
                retdef.append(sub(f[(j+1)%k],mul(UNITS[phase%4],f[j])))
            require(all(x is not None for x in Q),'incomplete tower')
            defects=[sub(Q[(i+1)%size],mul(UNITS[increments[i]%4],Q[i])) for i in range(size)]
            lhs=sum(map(square,Q),F(0))/size
            rhs=c*sum((lengths[j]*square(f[j]) for j in range(k)),F(0))/k
            require(lhs==rhs,'lifted norm requires height weight')
            actual=sum(map(square,defects),F(0))/size
            rhs=c*sum(map(square,retdef),F(0))/k
            require(actual==rhs,'top-localized L2 defect')
            wrong=c*sum((lengths[j]*square(retdef[j]) for j in range(k)),F(0))/k
            wrong_top_norm+=int(wrong!=actual)
            def to_mp(fr):return mp.mpf(fr.numerator)/fr.denominator
            abs1=sum(mp.sqrt(to_mp(square(d))) for d in defects)/size
            abs2=to_mp(c)*sum(mp.sqrt(to_mp(square(d))) for d in retdef)/k
            require(abs(abs1-abs2)<mp.mpf('1e-50'),'top-localized L1 defect')
            for L in range(size+1):
                p=F(sum(t>=L for t in ages),size)
                expected=c*sum((max(t-L,0) for t in lengths),F(0))/k
                require(p==expected,'age tail uses integrated return tail')
                age+=1
            tower+=1
    require(wrong_top_norm>0,'incorrect height-weighted defect not detected')
    # A finite Markov word checks chronological multiplication, not billiard mixing.
    P=[[F(1,2),F(1,3),F(1,6)],[F(1,4),F(1,2),F(1,4)],[F(1,6),F(1,3),F(1,2)]]
    pi=[F(3,10),F(2,5),F(3,10)]
    left=[ONE,(F(1,3),F(2,3)),(F(-1,2),F(1,4))]
    right=[(F(2,3),F(1,5)),(F(-1,4),F(1,2)),ONE]
    weight=[UNITS[0],UNITS[1],UNITS[2]]
    def transfer(v):return [sumz(scale(P[j][i],v[j]) for j in range(3)) for i in range(3)]
    words=0;wrong_words=0;paths=0
    for l,m in ((0,2),(1,1),(1,2),(2,1)):
        N=2*l+m;exact=ZERO
        for states in product(range(3),repeat=N+1):
            pr=pi[states[0]]
            for j in range(N):pr*=P[states[j]][states[j+1]]
            term=mul(right[states[0]],left[states[-1]])
            for j in range(l,l+m):term=mul(term,weight[states[j]])
            exact=add(exact,scale(pr,term));paths+=1
        vec=[scale(pi[i],right[i]) for i in range(3)]
        for j in range(l):vec=transfer(vec)
        for j in range(m):vec=transfer([mul(weight[i],vec[i]) for i in range(3)])
        for j in range(l):vec=transfer(vec)
        paired=sumz(mul(left[i],vec[i]) for i in range(3))
        require(exact==paired,'chronological middle word')
        bad=[scale(pi[i],right[i]) for i in range(3)]
        for j in range(l):bad=transfer(bad)
        for j in range(m):bad=[mul(weight[i],transfer(bad)[i]) for i in range(3)]
        for j in range(l):bad=transfer(bad)
        wrong_words+=int(sumz(mul(left[i],bad[i]) for i in range(3))!=exact)
        words+=1
    require(wrong_words>0,'wrong multiplier order not detected')
    exponent=F(1,12)
    require(1-2*exponent==F(5,6),'perturbation domain')
    require(1-6*exponent==F(1,2),'relative cubic damping')
    require(exponent/2==F(1,24),'unsmoothing exponent')
    require(F(1,2)-F(99,200)==F(1,200),'inner rescaling')
    require(F(1,2)-F(2,5)==F(1,10),'outer rescaling')
    require(F(99,200)-F(2,5)==F(19,200)>0,'annulus not feasible')
    require(2*F(99,200)==F(99,100),'squared lower frequency')
    complexity=0
    for L in range(1,33):
        s=8*L;k=6*L;d=4
        bound=d*(2*d-1)**(k-1)*sum(comb(s,j)*4**j for j in range(min(k,s)+1))
        require(bound<=d*(2*d-1)**(k-1)*5**s,'finite binomial bound')
        require(log(bound)+L*log(12)<50*L*log(2+L),'safe finite-record budget')
        complexity+=1
    schedules=0
    for n in (10**12,10**30,10**60):
        for exponentH in (0,2,10):
            H=2*n**exponentH
            for a in (F(99,200),F(2,5)):
                r=float(n)**(-float(a));Lam=1+log(H)-log(r);K=Lam*log(2+Lam)
                require(K>0 and r*K<10,'annulus logarithmic schedule')
                schedules+=1
    # Accuracy selection is not circular: b*(1+|log b|)^2 tends to zero.
    accuracy=[exp(-j)*(1+j)**2 for j in (8,16,32,64)]
    require(all(accuracy[j+1]<accuracy[j] for j in range(3)),'accuracy dependence')
    return {'variable_height_tower_cases':tower,'exact_age_tail_checks':age,
            'wrong_height_weighted_defects_rejected':wrong_top_norm,
            'exact_chronological_words':words,'enumerated_markov_paths':paths,
            'wrong_multiplier_words_rejected':wrong_words,'rational_exponent_checks':7,
            'finite_complexity_budgets':complexity,'annulus_budget_schedules':schedules,
            'accuracy_dependence_checks':3,
            'finite_models_do_not_prove_continuum_or_operator_estimates':True}

if __name__=='__main__':
    print(json.dumps({'revision':16,'source':source_checks(),'new_finite_checks':finite_checks(),
                      'inherited_v15_checks':verify_v15.finite_checks(),
                      'inherited_v14_algebra':verify_v14.algebra_checks(),
                      'inherited_v14_mechanics':verify_v14.mechanical_checks(),
                      'inherited_v13_checks':verify_v13.new_finite_checks(),
                      'inherited_v11_checks':verify_v11.finite_checks(),
                      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
