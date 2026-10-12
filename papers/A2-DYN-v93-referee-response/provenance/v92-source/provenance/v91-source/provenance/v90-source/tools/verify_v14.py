#!/usr/bin/env python3
"""Source replay and finite diagnostics; not a certificate of continuum proofs."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import mpmath as mp
import verify_v11
import verify_v13

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v13-referee-response'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict:
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger = json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision'] == 14, 'wrong revision')
    require(ledger['baseline'] == manifest['author_baseline_commit'], 'wrong edit baseline')
    by_path = {}
    for item in ledger['edits']:
        by_path.setdefault(item['path'], []).append(item)
    inherited = list(sorted((BASE/'core').glob('*.tex'))) + [BASE/'main.tex']
    require(len(inherited) == 32, 'incomplete v13 article')
    for path in inherited:
        rel = path.relative_to(BASE).as_posix()
        require(digest(path) == manifest['baseline_sha256'][rel], 'wrong baseline: '+rel)
        text = path.read_text()
        for item in by_path.get(rel, []):
            require(text.count(item['before']) == 1, 'nonunique inherited edit: '+rel)
            text = text.replace(item['before'], item['after'], 1)
        require(text.encode() == (ROOT/rel).read_bytes(), 'unaccounted inherited change: '+rel)
    require(set(by_path) <= {p.relative_to(BASE).as_posix() for p in inherited}, 'unknown inherited edit')
    old_scripts = sorted((BASE/'tools').glob('*.py'))
    for path in old_scripts + [BASE/'references.tex']:
        require(path.read_bytes() == (ROOT/path.relative_to(BASE)).read_bytes(),
                'changed inherited diagnostic or bibliography: '+path.name)
    actual_sources = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                      if p.is_file() and not any(x in p.parts for x in ('build','evidence','__pycache__'))
                      and p.name != 'SOURCE_MANIFEST.json'}
    require(actual_sources == set(manifest['source_sha256']), 'manifest omits or invents files')
    for rel, sha in manifest['source_sha256'].items():
        require(digest(ROOT/rel) == sha, 'source hash mismatch: '+rel)
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 14' in main, 'stale revision')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs)==len(set(inputs))==33, 'missing or duplicate core inclusion')
    require({x+'.tex' for x in inputs} == {p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'unincluded core file')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldtex='\n'.join(p.read_text() for p in BASE.rglob('*.tex'))
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)), 'duplicate labels')
    require(oldlabels <= set(labels), 'deleted inherited label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs <= set(labels), 'unresolved references: '+str(sorted(refs-set(labels))))
    citations=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):
        citations.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    require(citations<=bib,'unresolved bibliography item')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r\t' for c in tex),'control character')
    require(r'\nef{' not in tex and r'\end{proof}+' not in tex,'known malformed TeX')
    needed={'lem:regular-collision-product','lem:exact-collision-action',
            'prop:measurable-roof-rigidity','thm:physical-phase-rigidity',
            'lem:no-spatial-coboundary','thm:joint-uniform-nondegeneracy',
            'thm:intro-joint-nondegeneracy','cor:elliptic-central-inversion',
            'thm:LLT','lem:raw-residual-sum','thm:marked-return-band'}
    require(needed<=set(labels),'missing old or new central theorem')
    require(manifest['uniform_positive_definiteness_proof_included'] is True,'missing proof status')
    require(manifest['full_raw_LLT_proved'] is False,'unsupported raw LLT status')
    return {'included_core_files':len(inputs),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'inherited_core_byte_identical':31-sum(x.startswith('core/') for x in by_path),
            'inherited_core_with_exact_replayed_edits':sorted(x for x in by_path if x.startswith('core/')),
            'edit_operations':len(ledger['edits']),'inherited_python_files_byte_identical':len(old_scripts),
            'verified_file_count':len(actual_sources),'source_sha256':manifest['source_sha256']}


def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def algebra_checks() -> dict:
    a=((0,-1),(1,1)); eye=((1,0),(0,1)); powers=[eye]
    for _ in range(6): powers.append(mm(powers[-1],a))
    require(powers[3]==((-1,0),(0,-1)) and powers[6]==eye,'rotation order')
    require(all(eye[i][j]+powers[2][i][j]+powers[4][i][j]==0 for i in range(2) for j in range(2)),'three-rotation cancellation')
    vectors=0
    for x in range(-12,13):
        for y in range(-12,13):
            if x==y==0: continue
            det=x*(-x+y)-y*y
            require(det==-(x*x-x*y+y*y) and -det>=F(x*x+y*y,2)>0,'rotation rank')
            vectors+=1
    phases=0
    for den in range(1,65):
        for num in range(den):
            s=F(num,den)
            if (2*s).denominator==(3*s).denominator==1:
                require(s.denominator==1,'constant phase survived both rotations')
            phases+=1
    # Coordinate rectangles check the differential-form sign, not billiard laminations.
    areas=0
    for r in (F(9,20),F(23,50),F(47,100)):
        for dx in (F(1,100),F(1,20),F(1,7)):
            for dp in (F(1,90),F(1,11)):
                p0=F(-1,3); p1=p0+dp
                integral=r*p0*dx-r*p1*dx
                require(integral==-r*dx*dp and integral!=0,'Stokes sign')
                areas+=1
    covers=0
    for k1 in range(-3,4):
        for ell1 in range(2):
            h1=F(2,7); hnext=h1-k1; ellnext=(ell1+k1)%2
            difference=hnext+ellnext-h1-ell1
            require(difference.denominator==1 and difference.numerator%2==0,'finite-cover invariant sign')
            covers+=1
    # Negative controls: inversion alone has rank one; the two-product
    # alone does not eliminate a constant phase equal to pi.
    require(1*(-2)-2*(-1)==0,'inversion-only negative control')
    # Constant phase pi is not ruled out by the two-product alone, but is by the three-product.
    require((2*F(1,2)).denominator==1 and (3*F(1,2)).denominator!=1,'two-product-only negative control')
    return {'rotation_vector_cases':vectors,'rational_phase_cases':phases,
            'signed_stokes_rectangles':areas,'finite_cover_cases':covers,
            'negative_controls':2,'count_phase':'91/5000',
            'qualitative_geometry_not_certified_by_algebra':True}


def mechanical_checks() -> dict:
    """High-precision finite physical branches; not a continuum billiard certificate."""
    mp.mp.dps=65
    rt3=mp.sqrt(3)
    def physical(r,alpha,p):
        n=(mp.cos(alpha),mp.sin(alpha)); tang=(-n[1],n[0]); q=(r*n[0],r*n[1])
        v=tuple(mp.sqrt(1-p*p)*n[i]+p*tang[i] for i in range(2))
        candidates=[]
        for i in range(-4,5):
            for j in range(-4,5):
                if i==j==0: continue
                d=(mp.mpf(i)+mp.mpf(j)/2,mp.mpf(j)*rt3/2)
                delta=tuple(d[k]-q[k] for k in range(2))
                proj=sum(delta[k]*v[k] for k in range(2))
                disc=r*r-sum(x*x for x in delta)+proj*proj
                if disc<=0: continue
                tau=proj-mp.sqrt(disc)
                if tau>mp.mpf('1e-40'): candidates.append((tau,(i,j)))
        require(bool(candidates),'no physical hit in finite diagnostic')
        candidates.sort(); tau,label=candidates[0]
        # All omitted centers have norm >=5*sqrt(3)/2, so cannot beat this short flight.
        require(tau<1 and 5*rt3/2-2*r>1,'insufficient finite enumeration bound')
        require(len(candidates)==1 or candidates[1][0]-tau>mp.mpf('1e-10'),'near competing root in diagnostic')
        return tau,label
    def branch(r,alpha,p,label):
        n=(mp.cos(alpha),mp.sin(alpha)); tang=(-n[1],n[0]); q=(r*n[0],r*n[1])
        v=tuple(mp.sqrt(1-p*p)*n[i]+p*tang[i] for i in range(2))
        i,j=label; d=(mp.mpf(i)+mp.mpf(j)/2,mp.mpf(j)*rt3/2)
        delta=tuple(d[k]-q[k] for k in range(2)); proj=sum(delta[k]*v[k] for k in range(2))
        tau=proj-mp.sqrt(r*r-sum(x*x for x in delta)+proj*proj)
        n2=tuple((q[k]+tau*v[k]-d[k])/r for k in range(2))
        alpha2=mp.atan2(n2[1],n2[0]); p2=-v[0]*n2[1]+v[1]*n2[0]
        return tau,alpha2,p2
    samples=0; derivatives=0; symmetries=0; max_action=mp.mpf(0); max_symmetry=mp.mpf(0)
    for r in map(mp.mpf,('0.45','0.46','0.47')):
        for alpha in map(mp.mpf,('0.17','0.61','1.29','2.37')):
            for p in map(mp.mpf,('-0.6','-0.17','0.23','0.58')):
                tau,label=physical(r,alpha,p); _,alpha2,p2=branch(r,alpha,p,label)
                for coordinate in range(2):
                    if coordinate==0:
                        dt=mp.diff(lambda a:branch(r,a,p,label)[0],alpha)
                        da=mp.diff(lambda a:branch(r,a,p,label)[1],alpha)
                        rhs=r*p2*da-r*p
                    else:
                        dt=mp.diff(lambda pp:branch(r,alpha,pp,label)[0],p)
                        da=mp.diff(lambda pp:branch(r,alpha,pp,label)[1],p)
                        rhs=r*p2*da
                    error=abs(dt-rhs); max_action=max(max_action,error)
                    require(error<mp.mpf('1e-48'),'physical action differential failed')
                    derivatives+=1
                rotated=label
                for j in range(1,6):
                    rotated=(-rotated[1],rotated[0]+rotated[1])
                    rt,rl=physical(r,alpha+j*mp.pi/3,p)
                    require(rl==rotated,'physical label rotation failed')
                    max_symmetry=max(max_symmetry,abs(rt-tau))
                    require(abs(rt-tau)<mp.mpf('1e-48'),'physical time rotation failed')
                    symmetries+=1
                samples+=1
    return {'precision_decimal_digits':mp.mp.dps,'physical_states':samples,
            'action_partial_derivatives':derivatives,'rotation_checks':symmetries,
            'max_action_absolute_error':mp.nstr(max_action,8),
            'max_rotation_time_error':mp.nstr(max_symmetry,8),
            'finite_checks_not_product_structure_or_ergodicity_proofs':True}


if __name__=='__main__':
    print(json.dumps({'revision':14,'source':source_checks(),
       'new_exact_algebra':algebra_checks(),'new_finite_mechanics':mechanical_checks(),
       'inherited_v13_checks':verify_v13.new_finite_checks(),
       'inherited_v11_checks':verify_v11.finite_checks(),
       'full_raw_LLT_certified':False,'continuum_proof_certified':False},indent=2,sort_keys=True))
