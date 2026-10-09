#!/usr/bin/env python3
"""Source replay and finite algebra. This does not certify continuum proofs."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re
import mpmath as mp
import verify_v11
import verify_v13
import verify_v14
import verify_v15
import verify_v16 as old

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v16-referee-response'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks() -> dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==17, 'revision')
    require(ledger['baseline']==man['author_baseline_commit'], 'baseline identity')
    edits={}
    for e in ledger['edits']: edits.setdefault(e['path'],[]).append(e)
    require(set(edits)=={'main.tex'}, 'unlisted inherited edit class')
    old_core=sorted((BASE/'core').glob('*.tex'))
    require(len(old_core)==37, 'baseline core count')
    inherited=old_core+[BASE/'main.tex',BASE/'references.tex']
    for p in inherited:
        rel=p.relative_to(BASE).as_posix()
        require(digest(p)==man['baseline_sha256'][rel], 'baseline hash '+rel)
        text=p.read_text()
        for e in edits.get(rel,[]):
            require(text.count(e['before'])==1, 'edit not unique '+rel)
            text=text.replace(e['before'],e['after'],1)
        require(text.encode()==(ROOT/rel).read_bytes(), 'unreported edit '+rel)
    scripts=sorted((BASE/'tools').glob('*.py'))
    for p in scripts:
        require(p.read_bytes()==(ROOT/'tools'/p.name).read_bytes(), 'inherited script '+p.name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and not any(x in ('build','evidence','__pycache__') for x in p.parts)
            and p.name!='SOURCE_MANIFEST.json'}
    require(actual==set(man['source_sha256']), 'source map completeness')
    for rel,h in man['source_sha256'].items(): require(digest(ROOT/rel)==h, 'source hash '+rel)
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 17' in main, 'version metadata')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==39, 'core inclusion count')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'unlisted core')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in inherited)))
    require(len(labels)==len(set(labels)), 'duplicate label')
    require(oldlabels<=set(labels), 'deleted mathematical label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels), 'unresolved references '+str(refs-set(labels)))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    cites=set()
    for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex): cites.update(x.strip() for x in g.split(','))
    require(cites<=items, 'unresolved citations')
    require((ROOT/'references.tex').read_bytes()==(BASE/'references.tex').read_bytes(), 'bibliography changed')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'), 'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex), 'TeX control character')
    expected={'thm:intro-peripheral-neighborhood','lem:quadratic-endpoint-budget',
              'lem:joint-collision-phase-defect','prop:joint-collision-vector-defect',
              'lem:exact-peripheral-lift','thm:joint-return-spectral-defect',
              'lem:section-grid-reconstruction','lem:compression-defect-comparison',
              'thm:compressed-peripheral-resolvent','prop:compressed-finite-time-comparison',
              'thm:LLT','thm:joint-uniform-nondegeneracy','lem:raw-residual-sum'}
    require(expected<=set(labels), 'missing load-bearing theorem')
    for key in ('full_raw_LLT_proved','full_complementary_integral_proved','raw_second_derivative_sum_proved',
                'anisotropic_to_BV_reconstruction_proved','full_peripheral_circle_uniformly_controlled',
                'uncompressed_power_decay_proved'):
        require(man[key] is False, 'unsupported full-closure flag '+key)
    return {'included_core_files':len(inputs),'inherited_core_byte_identical':len(old_core),
            'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'exact_inherited_edits':len(ledger['edits']),
            'unchanged_bibliography_items':len(items),'verified_file_count':len(actual),
            'source_sha256':man['source_sha256']}

# Exact Gaussian-rational arithmetic; all finite maps below are diagnostic models.
add=old.add; sub=old.sub; mul=old.mul; scale=old.scale; square=old.square
ONE=old.ONE; ZERO=old.ZERO; UNITS=old.UNITS; sumz=old.sumz

def norm2(v): return sum((square(x) for x in v),F(0))
def vsub(v,w): return [sub(a,b) for a,b in zip(v,w)]
def vadd(v,w): return [add(a,b) for a,b in zip(v,w)]
def power(op,v,n):
    for _ in range(n):v=op(v)
    return v

def finite_checks() -> dict:
    mp.mp.dps=60
    tower_cases=0; wrong_unshifted=0; one_level_cases=0
    for size,Y in ((11,[0,1,5]),(17,[0,3,10,13]),(23,[0,1,8,15,19])):
        k=len(Y); c=F(k,size)
        eta=[int(i in Y) for i in range(size)]
        a=[(i*i+3*i+1)%7-3 for i in range(size)]
        inc=[k*a[i]-sum(a)*eta[i] for i in range(size)]
        lengths=[(Y[(j+1)%k]-Y[j])%size for j in range(k)]
        for xi in range(4):
            for mode in range(4):
                f=[scale(F((j+mode)%4,2) if mode else F(1),UNITS[(2*j+mode)%4]) for j in range(k)]
                Q=[None]*size; Q0=[None]*size; ret=[]; tops=set()
                for j,y in enumerate(Y):
                    phase=0
                    for t in range(lengths[j]):
                        x=(y+t)%size
                        Q0[x]=mul(UNITS[phase%4],f[j])
                        Q[x]=mul(UNITS[(phase+(xi if t else 0))%4],f[j])
                        phase+=inc[x]
                    ret.append(sub(f[(j+1)%k],mul(UNITS[(phase+xi)%4],f[j])))
                    tops.add((y+lengths[j]-1)%size)
                    one_level_cases+=int(lengths[j]==1)
                require(all(x is not None for x in Q),'tower partition')
                require(all(Q[i]==mul(UNITS[0 if eta[i] else xi],Q0[i]) for i in range(size)), 'age-zero phase multiplier')
                D=[sub(Q[(i+1)%size],mul(UNITS[(inc[i]+xi*eta[i])%4],Q[i])) for i in range(size)]
                require(all(D[i]==ZERO for i in range(size) if i not in tops),'nontop defect')
                require(norm2(D)/size==c*norm2(ret)/k,'peripheral top normalization')
                require(norm2(Q)/size==c*sum((lengths[j]*square(f[j]) for j in range(k)),F(0))/k,'height norm')
                bad=[sub(Q[(i+1)%size],mul(UNITS[(inc[i]+xi)%4],Q[i])) for i in range(size)]
                wrong_unshifted+=int(norm2(bad)!=norm2(D))
                tower_cases+=1
    require(wrong_unshifted>0 and one_level_cases>0,'spectral-phase negative controls')
    shifts=0; cancellation_lines=0
    for c in (F(2,7),F(3,11),F(5,23)):
        for xi in (F(-3,5),F(0),F(2,9)):
            sig=c*xi
            for z in ((F(1,3),F(-2,5),F(3,7),F(1,11)),(F(0),F(0),sig,F(0))):
                w=list(z);w[2]-=sig
                for e in (0,1):
                    h=[F(2,3),F(-4,7),1-F(e)/c,F(5,9)]
                    lhs=sig+sum((w[i]*h[i] for i in range(4)),F(0))
                    rhs=sum((z[i]*h[i] for i in range(4)),F(0))+xi*e
                    require(lhs==rhs,'exact affine spectral shift')
                    shifts+=1
                if all(v==0 for v in w) and xi:
                    require(sum((v*v for v in w),F(0))+sig*sig>0,'lost pure collision constant phase')
                    cancellation_lines+=1
    phase_times=0
    for s in (mp.mpf(1)/32,mp.mpf(1)/16,mp.mpf(1)/8):
        for ell in (1,5,20,100,500):
            j=ell+int(mp.ceil(mp.fmod(mp.pi-ell*s,2*mp.pi)/s))
            for sign in (-1,1):
                require(ell<=j<=ell+int(mp.ceil(2*mp.pi/s))+1,'dephasing time window')
                require(mp.cos(j*sign*s)<=-mp.mpf(3)/4,'opposite half-circle')
                phase_times+=1
    compression=0; inequality=0; telescope=0; visible_leak=0
    for N,groups in ((6,[[0,1],[2,3],[4,5]]),(8,[[0,1,2,3],[4,5,6,7]])):
        def P(v):
            out=[ZERO]*N
            for g in groups:
                avg=scale(F(1,len(g)),sumz(v[i] for i in g))
                for i in g:out[i]=avg
            return out
        for twist in range(4):
            phases=[UNITS[(i*i+twist*i)%4] for i in range(N)]
            def U(v):return [mul(phases[i],v[(i+1)%N]) for i in range(N)]
            def A(v):return P(U(v))
            for mode in range(4):
                f=P([scale(F((i+mode)%5-2),UNITS[(i+mode)%4]) for i in range(N)])
                S=norm2(f)
                if not S:continue
                require(norm2(U(f))==S,'unitary model')
                for lam in UNITS:
                    Af=A(f)
                    C=norm2(vsub(Af,[mul(lam,x) for x in f]))
                    R=norm2(vsub(U(f),[mul(lam,x) for x in f]))
                    require(R==C+S-norm2(Af),'orthogonal leakage identity')
                    if C<=S:
                        require(R*R<=9*C*S,'physical to compressed residual')
                        inequality+=1
                    compression+=1
            f=[ONE]*N
            for n in range(1,9):
                left=vsub(power(A,f,n),P(power(U,f,n)))
                right=[ZERO]*N
                for j in range(n):
                    u=power(U,f,j)
                    term=power(A,P(U(vsub(P(u),u))),n-1-j)
                    right=vadd(right,term)
                require(left==right,'exact finite-time telescoping')
                visible_leak+=int(norm2(left)>0)
                telescope+=1
    require(visible_leak>0,'discarded-projection error was not detected')
    grids=0
    for n in (2,3,4,8):
        for mode in range(3):
            a=[[F((-1)**(i+j)) if mode==0 else F((i+2*j+mode)%5-2) for j in range(n)] for i in range(n)]
            S=sum((v*v for row in a for v in row),F(0))/(n*n)
            M=max(abs(v) for row in a for v in row)
            L1=sum((abs(v) for row in a for v in row),F(0))/(n*n)
            jumps=sum((abs(a[i+1][j]-a[i][j]) for i in range(n-1) for j in range(n)),F(0))
            jumps+=sum((abs(a[i][j+1]-a[i][j]) for i in range(n) for j in range(n-1)),F(0))
            jumps+=sum((abs(a[0][j])+abs(a[-1][j]) for j in range(n)),F(0))
            jumps+=sum((abs(a[i][0])+abs(a[i][-1]) for i in range(n)),F(0))
            BV=L1+jumps/n
            require((M+BV)**2<=100*n*n*S,'grid traces and inverse mesh budget')
            grids+=1
    feasible=[]
    for beta,gamma in ((F(1,2),F(2,5)),(F(79,100),F(2,5)),(F(1,4),F(1,6))):
        require(beta<min(F(4,5),2*gamma),'subexponential admissibility')
        feasible.append({'beta':str(beta),'gamma':str(gamma),'slack':str(min(F(4,5),2*gamma)-beta)})
    require(not F(4,5)<min(F(4,5),2*F(2,5)),'equality cannot replace strict slack')
    require(F(2,5)<F(79,100)<F(4,5),'new quadratic budget is strictly stronger')
    require(F(1,2)-F(99,200)==F(1,200) and F(1,2)-F(2,5)==F(1,10),'rescaling')
    return {'peripheral_variable_height_tower_cases':tower_cases,'length_one_top_occurrences':one_level_cases,
            'wrong_constant_per_collision_rejections':wrong_unshifted,'affine_phase_shift_cases':shifts,
            'cancellation_line_cases':cancellation_lines,'dephasing_time_cases':phase_times,
            'exact_compression_identities':compression,'compression_residual_inequalities':inequality,
            'exact_power_telescopes':telescope,'nonzero_discretization_error_cases':visible_leak,
            'grid_boundary_variation_cases':grids,'strict_subexponential_budgets':feasible,
            'finite_models_are_not_continuum_or_spectral_certificates':True}

if __name__=='__main__':
    print(json.dumps({'revision':17,'source':source_checks(),'new_finite_checks':finite_checks(),
                      'inherited_v16_checks':old.finite_checks(),
                      'inherited_v15_checks':verify_v15.finite_checks(),
                      'inherited_v14_algebra':verify_v14.algebra_checks(),
                      'inherited_v14_mechanics':verify_v14.mechanical_checks(),
                      'inherited_v13_checks':verify_v13.new_finite_checks(),
                      'inherited_v11_checks':verify_v11.finite_checks(),
                      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
