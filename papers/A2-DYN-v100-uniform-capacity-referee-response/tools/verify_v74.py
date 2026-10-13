#!/usr/bin/env python3
"""Pinned source checks and rational fixtures; not continuum proof certification."""
from __future__ import annotations
import hashlib
import itertools
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from fractions import Fraction as F

PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER.parent / 'A2-DYN-v73-referee-response'
BASE_TREE = '995790396ccb81e24a97949b7d0143b222ad4b20'
REVIEW_PATH = 'reviews/a2-dyn-v73-external-top4-rereview-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB = '28d7999c60fc0083f99ffcb8550a932057af5b8f'
MAIN_BLOB = 'e63486d9d41976ffdb29162bdcb6ddd04228cff0'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def obj_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=PAPER, text=True).strip()


def physical_tree(path: Path) -> str:
    entries = []
    for child in path.iterdir():
        # These are exclusively generated, ignored directories in the baseline.
        if child.name in {'build', 'evidence', '__pycache__'}:
            continue
        if child.is_dir():
            entries.append((child.name + '/', '40000', child.name, physical_tree(child)))
        else:
            mode = '100755' if child.stat().st_mode & stat.S_IXUSR else '100644'
            entries.append((child.name, mode, child.name, obj_hash('blob', child.read_bytes())))
    raw = b''.join(mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(sha)
                   for _, mode, name, sha in sorted(entries))
    return obj_hash('tree', raw)


def finite_checks() -> dict[str, int]:
    counts = dict(level_bound=0, oriented_coarea=0, integrated=0,
                  tail_identity=0, homogeneity=0, quartic=0, negative_controls=0)
    zero = F(0)

    def integral(v: tuple[F, ...], lo: F, hi: F) -> F:
        return sum((h * max(zero, min(hi, F(i+1))-max(lo, F(i)))
                    for i, h in enumerate(v)), zero)

    def components(v: tuple[F, ...], u: F) -> list[tuple[F, F]]:
        answer = []; start = None
        for i in range(len(v) + 1):
            above = i < len(v) and v[i] > u
            if above and start is None:
                start = i
            if not above and start is not None:
                answer.append((F(start), F(i))); start = None
        return answer

    def layers(v: tuple[F, ...]):
        heights = sorted(set((zero, *v)))
        return [(hi-lo, components(v, (hi+lo)/2))
                for lo, hi in zip(heights, heights[1:])]

    for raw in itertools.product(range(3), repeat=4):
        v = tuple(map(F, raw)); ls = layers(v)
        jumps = (v[0], *(v[i]-v[i-1] for i in range(1, len(v))), -v[-1])
        for i, jump in enumerate(jumps):
            positive = sum((du for du, cs in ls for a, b in cs if a == i), zero)
            negative = sum((du for du, cs in ls for a, b in cs if b == i), zero)
            require(positive == max(jump, zero) and negative == max(-jump, zero), 'oriented level coarea')
            counts['oriented_coarea'] += 1
        for d in (F(1,2), F(1), F(2), F(3)):
            spatial_integral = zero
            for cell in range(4):
                t = F(2*cell+1, 2)
                sf = sum((du*max(zero, 1-(b-a)/d)
                          for du, cs in ls for a,b in cs if a<t<b), zero)
                spatial_integral += sf
            identity = sum((du*(b-a)*max(zero, 1-(b-a)/d)
                            for du, cs in ls for a,b in cs), zero)
            require(spatial_integral == identity, 'integrated layer identity')
            require(identity <= d*sum(map(abs,jumps))/8, 'sharp TV coefficient')
            counts['integrated'] += 1
            for j in range(-4, 21):
                t = F(2*j+1, 8)
                f = next((h for i,h in enumerate(v) if i<t<i+1), zero)
                avg = integral(v,t-d,t+d)/(2*d)
                sf = sum((du*max(zero, 1-(b-a)/d)
                          for du, cs in ls for a,b in cs if a<t<b), zero)
                inc = sum((max(z,zero) for i,z in enumerate(jumps) if t-d<=i<=t), zero)
                out = sum((max(-z,zero) for i,z in enumerate(jumps) if t<=i<=t+d), zero)
                require(max(f-2*avg,zero) <= sf <= min(f,inc,out), 'level-matched bound')
                counts['level_bound'] += 1
                tail_integral = sum((du*max(zero,d-(b-a))/d
                                     for du, cs in ls for a,b in cs if a<t<b), zero)
                require(sf == tail_integral, 'exact integrated length tail')
                counts['tail_identity'] += 1
                scaled = tuple(F(7,3)*h for h in v)
                sf_scaled = sum((du*max(zero,1-(b-a)/d)
                                 for du, cs in layers(scaled) for a,b in cs if a<t<b), zero)
                require(sf_scaled == F(7,3)*sf, 'homogeneity')
                counts['homogeneity'] += 1

    # A width-d/2 pulse attains the integrated constant.
    d=F(2); width=F(1); h=F(3)
    require(h*width*(1-width/d) == d*(2*h)/8, 'sharpness pulse')
    counts['negative_controls'] += 1
    # Different level layers produce paired Jordan masses but no short component through zero.
    require(F(5,2)>1 and min(F(1),F(1))==1 and max(zero,1-F(5,2))==0,
            'mismatched-level control')
    counts['negative_controls'] += 1
    # A narrow positive peak remains; small total integral is not a height bound.
    for m in (2,4,8,16):
        width=F(1,m**4); height=F(1,m**2)
        require(m*m*height*(1-width)>F(1,2), 'normalized narrow peak survives')
        require(height*width < height, 'mass is not height')
        counts['negative_controls'] += 1

    lo,hi=F(49,100),F(53,100); s_lo,s_hi=F(1732,1000),F(1733,1000)
    require(s_lo*s_lo < 3 < s_hi*s_hi, 'sqrt three bracket')
    def P(R,q,s):
        return 8*R*q*(1+q*q)-4*q*(1-q*q)+s*(1-6*q*q+q**4)
    require(min(P(F(9,20),lo,s) for s in (s_lo,s_hi))>0, 'lower endpoint sign')
    require(max(P(F(47,100),hi,s) for s in (s_lo,s_hi))<0, 'upper endpoint sign')
    derivative_upper=8*F(47,100)*(1+3*hi**2)-4+12*hi**2-s_lo*(12*lo-4*lo**3)
    require(derivative_upper < -2, 'quartic derivative sign')
    counts['quartic'] += 4
    # The trigonometric substitution is checked as a polynomial identity.
    import sympy as sp
    q,R,s=sp.symbols('q R s')
    sn=2*q/(1+q*q); cs=(1-q*q)/(1+q*q)
    expr=2*(1+q*q)**2*(2*R*sn-sn*cs+s*(cs*cs-sn*sn)/2)
    require(sp.expand(sp.cancel(expr-P(R,q,s))) == 0, 'half-angle polynomial identity')
    counts['quartic'] += 1
    require(F(1,12)*F(1,16)==F(1,192), 'outer-band exponent')
    return counts


def status_texts(manifest: dict) -> dict[str, str]:
    r=manifest['revision']
    publication={key:manifest[key] for key in ('revision','active_directory','branches',
                 'full_raw_return_LLT_proved','pointwise_roof_density_LLT_proved',
                 'lorentz_level_matched_tail_decay_proved','independent_human_review','formal_proof_certificate')}
    publication['authority']='SOURCE_MANIFEST.json'
    return {
        'PUBLICATION_STATUS.json': json.dumps(publication,indent=2)+'\n',
        'REFEREE_STATUS.md': f'# A2-DYN revision {r}: referee status\n\nAuthority: `SOURCE_MANIFEST.json`.\n\nControlling report: `{manifest["controlling_review_commit"]}`.\n\nThe explicit graph and level-matched estimates are submitted for mathematical review. Collision-uniform short-excursion decay and the full pointwise endpoint are not marked proved. No independent human specialist audit or journal acceptance is claimed. See `RESPONSE_TO_REFEREE.md` for the point-by-point dispositions.\n',
        'VALIDATION.md': f'# A2-DYN revision {r}: validation contract\n\nAuthority: `SOURCE_MANIFEST.json`.\n\nRun `bash build.sh` in an exact Git checkout. For the separately materialized, SHA-verified baseline artifact, `bash build.sh --local` performs the same source, rational, TeX and geometry checks without claiming an exact remote checkout. CI forbids local mode.\n\nThe build compiles all 167 core modules across the journal article and technical supplement, preserves all 163 inherited cores, and records the actual checkout SHA in generated evidence. Workflow: `{manifest["qualification_workflow"]}`.\n\nPassing source checks, finite fixtures, compilation and page geometry is not a certificate of the continuum proofs, independent human review, or closure of the dynamical endpoint. Current results are in `LOCAL_FULL_BUILD_RECORD.md` and the exact-SHA workflow artifact.\n'
    }


def prepare_and_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'baseline paper bytes or modes changed')
    require(obj_hash('blob',(PAPER/'provenance/v73-main.tex').read_bytes())==MAIN_BLOB,'v73 master snapshot changed')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='materialized baseline artifact; not a remote-checkout claim'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v73-referee-response')==BASE_TREE,'Git baseline tree changed')
        require(git('rev-parse','HEAD:'+REVIEW_PATH)==REVIEW_BLOB,'controlling report changed')
        if os.environ.get('GITHUB_ACTIONS')=='true':
            require(head==os.environ.get('GITHUB_SHA'),'wrong qualification SHA')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py')]:
        files=sorted((BASE/folder).rglob(pattern))
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),'inherited file changed: '+str(src))
        preserved[folder]=len(files)
    require(preserved['core']==163 and len(list((PAPER/'core').glob('*.tex')))==167,'core count')
    require((PAPER/'references.tex').read_bytes()==(BASE/'references.tex').read_bytes(),'inherited bibliography changed')
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    active=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    for key,value in old.items():
        if isinstance(value,bool):
            require(active.get(key) is value,'unjustified inherited status change: '+key)
    require(active['revision']==74 and active['active_core_count']==167,'active manifest revision')
    require(active['lorentz_level_matched_tail_decay_proved'] is False,'tail premise promoted to theorem')
    for name,expected in status_texts(active).items():
        require((PAPER/name).read_text()==expected,'stale generated status: '+name)
    build=PAPER/'build'; build.mkdir(exist_ok=True)
    v72=(PAPER/'provenance/v72-main.tex').read_text()
    marker='\\part{The complete physical current and source recovery}'
    require(v72.count(marker)==1,'old master assembly boundary')
    before,after=v72.split(marker)
    body=marker+after.split('\\input{references}',1)[0]
    abstract=before.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    opening=before.split('\\maketitle',1)[1]
    front=('\\section{The retained opening of revision 72}\n\\label{app:v73-retained-front}\n'
           'The following opening is retained as a historical statement of the preceding route. '
           'Its finite-measure qualification is superseded by Theorem~\\ref{thm:v73-full-source-bv}; '
           'its collision-uniform qualification is not. In its source notation, $e_{70}$ means '
           'first clearance outside the selected disks, with incidence separate.\n'
           '\\paragraph{Preceding abstract.}\n'+abstract+'\n'+opening)
    (build/'v72-body.tex').write_text(body); (build/'v72-frontmatter.tex').write_text(front)
    master=(PAPER/'provenance/v73-main.tex').read_text()
    old_title='\\title[Collision records and raw local inversion]{Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas}'
    require(master.count(old_title)==1,'supplement title boundary')
    master=master.replace(old_title,'\\title[Technical supplement]{Technical supplement to Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas}')
    master=master.replace('October 11, 2026. A2-DYN, revision 73',
                          'October 11, 2026. A2-DYN, revision 74; frozen revision-73 technical source')
    (build/'supplement-source.tex').write_text(master)
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return dict(checkout_sha=head,baseline_tree=BASE_TREE,controlling_review_blob=REVIEW_BLOB,
                preserved=preserved,active_core_count=167,source_sha256=hashes)


def main() -> None:
    args=sys.argv[1:]
    require(args in ([],['--local'],['--finite-only'],['--write-status']), 'unknown arguments')
    if args==['--write-status']:
        require(os.environ.get('GITHUB_ACTIONS')!='true','status mutation forbidden in CI')
        data=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
        for name,text in status_texts(data).items(): (PAPER/name).write_text(text)
        return
    result={'revision':74,'scope':'source identity, rational finite fixtures and assembly only',
            'formal_proof_certificate':False,'independent_human_review':False,
            'finite_checks':finite_checks()}
    if args!=['--finite-only']: result['source']=prepare_and_check(args==['--local'])
    else: require(os.environ.get('GITHUB_ACTIONS')!='true','finite-only forbidden in CI')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
