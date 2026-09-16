#!/usr/bin/env python3
"""Source preservation and finite diagnostic controls; not a proof certificate."""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
from source_provenance import blob_id, graph, require

P = Path(__file__).resolve().parents[1]
BASE = '71e0bd6306f54466728c2e6e781bb0f422c5cfb0'
PREFIX = 'papers/A2-v17-boundary-information-coarsening'
ALLOWED = {'main.tex', 'rigidity.tex', 'README.md'}
CORE = 'article/23f2_finite_experiment_analytic_inverse_v62.tex'
OVERVIEW = 'article/00c_finite_experiment_overview_v62.tex'
ROUTE = 'journal/full_reference_routes_v62.tex'


def git(*args: str) -> bytes:
    cp = subprocess.run(['git', *args], cwd=P, capture_output=True)
    require(cp.returncode == 0, cp.stderr.decode(errors='replace'))
    return cp.stdout


def controls() -> dict:
    # Exhaustive finite binomial probabilities, not Monte Carlo evidence.
    tail_cases = bernstein_cases = 0
    for n in (2, 5, 10, 25, 50):
        for p in (Fraction(1, 10), Fraction(1, 3), Fraction(1, 2), Fraction(4, 5)):
            probabilities = [Fraction(math.comb(n, k))*p**k*(1-p)**(n-k) for k in range(n+1)]
            require(sum(probabilities) == 1, 'Bad finite binomial normalization')
            exact = sum(probabilities[k] for k in range(n+1) if k <= n*p/2)
            require(float(exact) <= math.exp(-float(n*p)/8)+1e-14, 'Lower-tail failure')
            tail_cases += 1
            for x in (1.0, 2.0, 4.0):
                radius = math.sqrt(2*float(p)*x/n)+2*x/(3*n)
                exact = sum(probabilities[k] for k in range(n+1) if abs(k/n-float(p)) > radius)
                require(float(exact) <= 2*math.exp(-x)+1e-14, 'Cell Bernstein failure')
                bernstein_cases += 1
    tube_cases = 0
    for h in (Fraction(1, 2), Fraction(1, 5), Fraction(1, 10)):
        for q in (Fraction(0), Fraction(1, 100), Fraction(1, 4), Fraction(1, 2)):
            r = h*q
            require((h+2*r)**2-(h-2*r)**2 == 8*h*r, 'Cell tube identity')
            require(h*h+8*h*r <= 5*h*h, 'Displaced-cell mass bound')
            tube_cases += 1
    # Outside-category normalization is indispensable even in a 3-category model.
    inside, cell = Fraction(3, 5), Fraction(1, 5)
    require(cell/inside != cell, 'Omitted-outside negative control failed')
    # Error scales with r/h, not r: refute the false mesh-independent bound.
    require(8*Fraction(1, 10000)/Fraction(1, 100) > 8*Fraction(1, 10000),
            'Cell-bias negative control failed')
    schedules = 0
    for omega in (.05, .2, .7):
        for gamma in (.4, 1.0, 3.0):
            for power in (4, 12):
                denominator = power*omega+gamma
                for logratio in (10.0, 30.0, 90.0):
                    j = 2*math.floor(logratio/(2*denominator))
                    require(j % 2 == 0, 'Flight parity')
                    target = math.exp(-omega*logratio/denominator)
                    require(math.exp(-omega*j) <= math.exp(2*omega)*target*(1+1e-12), 'Rounding bound')
                    require(math.exp(denominator*j-logratio) <= 1+1e-12, 'Budget exponential bound')
                    require(math.exp(-omega*j) >= target*(1-1e-12), 'Lower rounding control')
                    schedules += 1
    # h_pil=h^4, scan cost h_pil^-3, hence h^-12, not h^-4.
    h=Fraction(1,10); eps=h**4
    require(eps**-3 == h**-12 and eps**-3 > h**-4, 'Pilot cost negative control')
    return dict(exact_binomial_tail_cases=tail_cases, exact_bernstein_cases=bernstein_cases,
                exact_cell_tube_cases=tube_cases, even_schedule_cases=schedules,
                negative_controls=['omitted outside category', 'mesh-independent displacement', 'free pilot'],
                scope='Finite checks only; no certification of relative limits, analytic inversion or significance')


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-manifest', type=Path)
    args=ap.parse_args()
    if args.baseline_manifest:
        m=json.loads(args.baseline_manifest.read_text())
        require(m['source_commit']==BASE, 'Wrong baseline manifest')
        baseline={n: v['git_blob'] for n,v in m['files'].items()}
    else:
        baseline={}
        for row in git('ls-tree','--full-tree','-r','-z',BASE+':'+PREFIX).split(b'\0'):
            if row:
                meta,name=row.split(b'\t',1)
                _,kind,oid=meta.decode().split()
                require(kind=='blob','Unexpected baseline object')
                baseline[name.decode()]=oid
    require(len(baseline)==753 and ALLOWED.issubset(baseline), 'Incomplete/unexpected frozen baseline')
    changed=[]
    for name,oid in baseline.items():
        f=P/name
        require(f.is_file() and not f.is_symlink(), 'Missing inherited path: '+name)
        if blob_id(f.read_bytes())!=oid:
            require(name in ALLOWED, 'Historical source changed: '+name)
            changed.append(name)
    require(set(changed)==ALLOWED, 'Unexpected amended paths')
    for name in ALLOWED:
        require(blob_id((P/'history/v61-review-baseline'/name).read_bytes())==baseline[name], 'Incorrect original archive')
    current={stem:graph(P,stem+'.tex') for stem in ('main','rigidity','two_collision')}
    with tempfile.TemporaryDirectory() as tmp:
        q=Path(tmp)
        for name in baseline:
            if name.endswith('.tex'):
                target=q/name; target.parent.mkdir(parents=True,exist_ok=True)
                origin=P/('history/v61-review-baseline/'+name if name in ALLOWED else name)
                target.write_bytes(origin.read_bytes())
        old={stem:graph(q,stem+'.tex') for stem in current}
        for stem in current:
            extra=set() if stem=='two_collision' else {CORE,OVERVIEW}
            if stem=='rigidity': extra.add(ROUTE)
            require(current[stem]==old[stem]|extra,'Changed old active proof graph: '+stem)
        # Retain old direct inputs in their order, allowing the route's additive wrapper.
        pat=r'\\input\{([^}]+)\}'
        for stem in ('main','rigidity'):
            prev=re.findall(pat,(q/(stem+'.tex')).read_text())
            now=re.findall(pat,(P/(stem+'.tex')).read_text())
            now=[x.replace('journal/full_reference_routes_v62','journal/full_reference_routes_v56') for x in now]
            now=[x for x in now if x+'.tex' not in {CORE,OVERVIEW}]
            require(prev==now,'Inherited input ordering changed: '+stem)
    text=(P/CORE).read_text()
    for label in ('lem:v62-finite-densities','thm:v62-finite-contact','thm:v62-budget',
                  'cor:v62-calibration','cor:v62-total-budget'):
        require('\\label{'+label+'}' in text,'Missing new statement: '+label)
    counts={kind:len(re.findall(r'\\begin\{'+kind+r'\}',text)) for kind in ('lemma','theorem','corollary','proof')}
    require(counts=={'lemma':1,'theorem':2,'corollary':2,'proof':5},'Statement/proof inventory')
    print(json.dumps(dict(baseline=BASE,inherited_files=len(baseline),unchanged_inherited_files=len(baseline)-len(changed),
        changed_inherited_paths=sorted(changed), archived_originals=sorted(ALLOWED),
        active_files_per_entry={s:len(v) for s,v in current.items()},active_union=len(set().union(*current.values())),
        new_environments=counts,finite_controls=controls(),proof_certification=False),indent=2,sort_keys=True))

if __name__=='__main__': main()
