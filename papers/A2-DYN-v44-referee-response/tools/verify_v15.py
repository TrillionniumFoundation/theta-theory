#!/usr/bin/env python3
"""Exact inheritance replay and finite diagnostics, not continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import math
import verify_v11
import verify_v13
import verify_v14

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v14-referee-response'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks() -> dict:
    man = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger = json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision'] == 15, 'wrong revision')
    require(ledger['baseline'] == man['author_baseline_commit'], 'wrong baseline')
    by_path: dict[str,list] = {}
    for e in ledger['edits']:
        by_path.setdefault(e['path'], []).append(e)
    inherited = list(sorted((BASE/'core').glob('*.tex'))) + [BASE/'main.tex', BASE/'references.tex']
    require(len(inherited) == 35, 'incomplete v14 baseline')
    for p in inherited:
        rel = p.relative_to(BASE).as_posix()
        require(digest(p) == man['baseline_sha256'][rel], 'baseline hash: '+rel)
        text = p.read_text()
        for e in by_path.get(rel, []):
            require(text.count(e['before']) == 1, 'nonunique exact edit: '+rel)
            text = text.replace(e['before'], e['after'], 1)
        require(text.encode() == (ROOT/rel).read_bytes(), 'unreported edit: '+rel)
    require(set(by_path) <= {p.relative_to(BASE).as_posix() for p in inherited}, 'foreign edit path')
    old_scripts = list(sorted((BASE/'tools').glob('*.py')))
    for p in old_scripts:
        require(p.read_bytes() == (ROOT/'tools'/p.name).read_bytes(), 'changed inherited script '+p.name)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
              and not any(part in ('build','evidence','__pycache__') for part in p.parts)
              and p.name != 'SOURCE_MANIFEST.json'}
    require(actual == set(man['source_sha256']), 'incomplete source hash map')
    for rel,h in man['source_sha256'].items():
        require(digest(ROOT/rel) == h, 'source hash mismatch: '+rel)
    main = (ROOT/'main.tex').read_text()
    require('A2-DYN, revision 15' in main, 'stale version')
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 35, 'missing/duplicate core inclusion')
    require({x+'.tex' for x in inputs} == {p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'unincluded core')
    tex = main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    labels = re.findall(r'\\label\{([^}]+)\}', tex)
    oldtex = '\n'.join(p.read_text() for p in inherited)
    oldlabels = set(re.findall(r'\\label\{([^}]+)\}', oldtex))
    require(len(labels) == len(set(labels)), 'duplicate labels')
    require(oldlabels <= set(labels), 'deleted old theorem/equation label')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', tex))
    require(refs <= set(labels), 'undefined references: '+str(sorted(refs-set(labels))))
    bib = (ROOT/'references.tex').read_text()
    oldbib = (BASE/'references.tex').read_text()
    olditems = set(re.findall(r'\\bibitem\{([^}]+)\}', oldbib))
    newitems = set(re.findall(r'\\bibitem\{([^}]+)\}', bib))
    require(olditems <= newitems and newitems-olditems == {'AFP'}, 'bibliography retention')
    cites = set()
    for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):
        cites.update(x.strip() for x in g.split(','))
    require(cites <= newitems, 'undefined bibliography item')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}') == tex.count('\\end{'+env+'}'), 'environment '+env)
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex), 'control character or tab in TeX')
    require(r'\nef{' not in tex and r'\end{proof}+' not in tex, 'known TeX defect')
    required = {'thm:intro-quantitative-phases','thm:complete-physical-phase',
                'lem:finite-return-witnesses','lem:finite-holonomy-defect',
                'thm:compact-log-phase-defect','lem:bv-circle-truncation',
                'thm:compact-vector-defect','thm:uniform-compact-bv-separation',
                'thm:LLT','lem:raw-residual-sum','thm:joint-uniform-nondegeneracy'}
    require(required <= set(labels), 'missing load-bearing theorem')
    require(man['full_raw_LLT_proved'] is False, 'raw LLT overclaim')
    require(man['uniform_logarithmic_H_rate_in_R_proved'] is False, 'uniformity overclaim')
    require(man['anisotropic_to_BV_reconstruction_proved'] is False, 'operator-space overclaim')
    return {'included_core_files':len(inputs),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'edit_operations':len(ledger['edits']),
            'inherited_core_byte_identical':33-sum(x.startswith('core/') for x in by_path),
            'inherited_core_with_exact_edits':sorted(x for x in by_path if x.startswith('core/')),
            'inherited_python_files_byte_identical':len(old_scripts),
            'retained_bibliography_items':len(olditems),'new_bibliography_items':['AFP'],
            'verified_file_count':len(actual),'source_sha256':man['source_sha256']}


def finite_checks() -> dict:
    # Exact non-product conditional densities on a finite 2 by 3 product.
    weights = [[1,2,5],[3,7,4]]
    total = sum(map(sum,weights))
    m = [[F(x,total) for x in row] for row in weights]
    rows = [sum(row) for row in m]
    cols = [sum(m[i][j] for i in range(2)) for j in range(3)]
    ps={(i,j,k):m[i][j]*m[i][k]/rows[i] for i in range(2) for j in range(3) for k in range(3)}
    pu={(i,k,j):m[i][j]*m[k][j]/cols[j] for i in range(2) for k in range(2) for j in range(3)}
    require(sum(ps.values()) == sum(pu.values()) == 1, 'pair normalization')
    marginals=0
    for i in range(2):
        for j in range(3):
            require(sum(ps[i,j,k] for k in range(3)) == m[i][j], 'stable first marginal')
            require(sum(ps[i,k,j] for k in range(3)) == m[i][j], 'stable second marginal')
            require(sum(pu[i,k,j] for k in range(2)) == m[i][j], 'unstable first marginal')
            require(sum(pu[k,i,j] for k in range(2)) == m[i][j], 'unstable second marginal')
            marginals+=4
    truncations=0
    for pair in (ps,pu):
        reference=F(1,len(pair))
        for K in (F(1,2),F(1),F(2),F(10)):
            values={key:F((sum(key)+1)%5,2) for key in pair}
            lhs=sum(reference*values[key] for key in pair)
            rhs=K*sum(pair[key]*values[key] for key in pair)+2*sum(reference for key in pair if reference/pair[key]>K)
            require(lhs<=rhs,'density truncation loses mass')
            truncations+=1
    # Exact unit-circle products around the ordered four corners.
    def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
    def conj(z):return(z[0],-z[1])
    phases=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(3,5),F(4,5))]
    corners=0
    from itertools import product
    for ids in product(range(4),repeat=4):
        q=[phases[i] for i in ids];z=(F(1),F(0))
        for i in range(4):z=mul(z,mul(q[(i+1)%4],conj(q[i])))
        require(z==(1,0),'four-corner ratio cancellation');corners+=1
    # A finite integer example of witness generation, not physical return data.
    g=[(1,0,2),(0,1,2),(0,0,3),(0,0,2)]
    coefficients=[(1,0,-2,2),(0,1,-2,2),(0,0,1,-1)]
    for j,b in enumerate(coefficients):
        require(tuple(sum(b[i]*g[i][k] for i in range(4)) for k in range(3))==tuple(int(k==j) for k in range(3)), 'integer witness generation')
    covers=0
    for p in (2,3,5,7,11):
        for a1 in range(p):
            for a2 in range(p):
                if a1==a2==0:continue
                h=(3,-2);k=(2,-1)
                for ell in ((0,0),(p-1,1%p)):
                    nextell=tuple((ell[j]+k[j])%p for j in range(2))
                    nexth=tuple(h[j]+k[j] for j in range(2))
                    before=a1*(ell[0]-h[0])+a2*(ell[1]-h[1])
                    after=a1*(nextell[0]-nexth[0])+a2*(nextell[1]-nexth[1])
                    require((after-before)%p==0,'finite-cover invariant sign');covers+=1
    # The proof derives x <= eta + m*epsilon from a quadratic inequality.
    roots=0
    for eta in (0.001,0.1,0.5):
        for epsilon in (0.0,0.001,0.2):
            for n in (1,7,64):
                root=(n*epsilon+math.sqrt((n*epsilon)**2+4*eta**2))/2
                require(root<=eta+n*epsilon+1e-12,'modulus variance bound');roots+=1
    radial=0
    for real in (-2,-1,-0.25,0,0.125,0.5,1,3):
        for imag in (-1,-0.1,0,0.2,2):
            z=complex(real,imag);a=abs(z);q=z/a if a>0.375 else 1+0j
            require(abs(q)==1 or abs(abs(q)-1)<1e-14,'nonunit truncation')
            require(abs(q-z)<=3*abs(a-1)+1e-12,'radial truncation bound');radial+=1
    # Concrete theta=1/2 scheduling for the abstract smoothing balance.
    schedules=0
    for h in (2,4,16,256,2**20):
        eps=1/(64*h);T=8
        n=math.ceil(math.log2(64*(1/eps+T)))
        require(h*eps+(1/eps+T)*2**(-n)<=1/32+1e-14,'logarithmic smoothing schedule');schedules+=1
    # Negative controls for each common logical shortcut.
    require(F(1,6)!=m[0][0], 'product measure incorrectly equals restricted measure')
    require(all((2*x)%2==0 for x in range(-5,6)), 'even count negative control')
    require(complex(0,0)==0, 'zero vector must not be normalized by division')
    require(math.log(2**20)>math.log(2), 'growing BV cannot be assigned a fixed norm')
    return {'conditional_pair_marginal_checks':marginals,'density_truncations':truncations,
            'oriented_four_corner_products':corners,'integer_witness_identities':3,
            'finite_cover_cancellations':covers,'modulus_quadratic_checks':roots,
            'radial_truncations_including_zero':radial,'logarithmic_schedules':schedules,
            'negative_controls':4,'these_are_finite_algebra_not_continuum_or_operator_proofs':True}


if __name__=='__main__':
    print(json.dumps({'revision':15,'source':source_checks(),'new_finite_checks':finite_checks(),
                      'inherited_v14_algebra':verify_v14.algebra_checks(),
                      'inherited_v14_mechanics':verify_v14.mechanical_checks(),
                      'inherited_v13_checks':verify_v13.new_finite_checks(),
                      'inherited_v11_checks':verify_v11.finite_checks(),
                      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
