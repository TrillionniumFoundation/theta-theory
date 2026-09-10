#!/usr/bin/env python3
"""Finite independent diagnostics for A2 v10; not formal proof verification.

Dependencies: Python 3.10+, sympy. No manuscript code is imported.
Use --repo /path/to/theta-theory for a checkout containing the frozen commit;
or --source-dir PATH --inventory PATH for the authenticated source packet.
Optional --v9-source-dir checks the pinned completed-v9 manifest and retention.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sympy as s

COMMIT = 'f46dca20f3d1b73077522bb2041f463af033cb70'
PREFIX = 'papers/A2-v10-observable-boundary-profiles'
TREE = '452a9003b03ff8f6eed47e1f609a36a054271455'
V9_MANIFEST = '53ad7d0d5ff948758c4dedf437dc78f623303ba404449ce49d527233ec0d6218'
COUNTS: Counter[str] = Counter()


def check(ok: object, category: str, label: str) -> None:
    if not bool(ok):
        raise RuntimeError(f'{category}: {label}')
    COUNTS[category] += 1


def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def tree_hash(entries: dict[str, tuple[str, str]]) -> str:
    nested: dict = {}
    for name, value in entries.items():
        parts = name.split('/')
        node = nested
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    def walk(node: dict) -> str:
        body = b''
        for name, value in sorted(node.items(), key=lambda kv: (kv[0] + ('/' if isinstance(kv[1], dict) else '')).encode()):
            mode, sha = ('40000', walk(value)) if isinstance(value, dict) else value
            body += mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(sha)
        return git_hash('tree', body)
    return walk(nested)


def authenticate(args: argparse.Namespace) -> tuple[Path, dict]:
    expected: dict[str, tuple[str, str]] = {}
    if args.repo:
        source = args.repo / PREFIX
        raw = subprocess.check_output(['git', '-C', str(args.repo), 'ls-tree', '-rz', COMMIT + ':' + PREFIX])
        for record in raw.split(b'\0'):
            if not record:
                continue
            meta, name = record.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            if kind != 'blob':
                raise RuntimeError('Unexpected non-blob source entry')
            expected[name.decode()] = (mode, sha)
    else:
        if not args.source_dir or not args.inventory:
            raise ValueError('Supply --repo, or both --source-dir and --inventory')
        source = args.source_dir
        inventory = json.loads(args.inventory.read_text())
        expected = {name: ('100644', item['git_blob']) for name, item in inventory.items()}
    actual = {}
    for name, (mode, sha) in expected.items():
        observed = git_hash('blob', (source / name).read_bytes())
        check(observed == sha, 'source_blob', name)
        actual[name] = (mode, observed)
    computed = tree_hash(actual)
    check(computed == TREE, 'source_tree', 'native directory tree')
    return source, {'commit': COMMIT, 'native_files': len(actual), 'tree': computed}


def expand(source: Path, name: str, stack: tuple = ()) -> str:
    if name in stack:
        raise RuntimeError('Cyclic TeX input')
    text = (source / name).read_text()
    return re.sub(r'\\input\{([^}]+)\}', lambda m: expand(source, m[1] + '.tex', stack + (name,)), text)


def formal_blocks(source: Path) -> list[str]:
    pattern = r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}'
    return [m[0] for m in re.finditer(pattern, expand(source, 'main.tex'))]


def moment(i: int, j: int) -> F:
    a = F(1)
    for r in range(i):
        a *= F(2*r + 1, 2)
    for r in range(j):
        a *= F(2*r + 1, 2)
    return 2*a / math.factorial(i+j+2)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path)
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--inventory', type=Path)
    p.add_argument('--v9-source-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    source, identity = authenticate(args)
    retention = None
    if args.v9_source_dir:
        base = args.v9_source_dir
        raw = (base / 'MANIFEST.sha256').read_bytes()
        check(hashlib.sha256(raw).hexdigest() == V9_MANIFEST, 'v9_integrity', 'manifest')
        for row in raw.decode().splitlines():
            sha, name = row.split(None, 1)
            name = name.strip().lstrip('*')
            check(hashlib.sha256((base / name).read_bytes()).hexdigest() == sha, 'v9_integrity', name)
        old, new = Counter(formal_blocks(base)), Counter(formal_blocks(source))
        check(not (old-new), 'environment_retention', 'all old blocks retained verbatim')
        retention = {'v9_blocks': sum(old.values()), 'v10_blocks': sum(new.values()), 'old_blocks_retained_verbatim': True}
    x = s.symbols('x')
    half = s.Rational(1, 2)
    for i in range(5):
        for j in range(5):
            exact_integral = s.simplify(2*s.gamma(i+half)*s.gamma(j+half)/(s.pi*s.gamma(i+j+3)))
            q = moment(i,j)
            check(exact_integral == s.Rational(q.numerator,q.denominator), 'exact_math', f'simplex moment {i},{j}')
    ratios = []
    for n in range(4, 41):
        lam = 2*moment(n,0)
        central = F(4*math.comb(2*n,n), 4**n*(n+1)*(n+2))
        check(lam == central, 'exact_math', f'linearized monomial multiplier {n}')
        # On [0,1], m=4, a_n=(1/20)n^-4; both signs lie in K_4(2,1/2;1).
        amp = F(1,20*n**4)
        upper_sum = 1 + amp*sum(math.prod(range(n-r+1,n+1)) for r in range(5))
        check(upper_sum <= 2 and 1-amp >= F(1,2), 'exact_math', f'fixed regularity ball {n}')
        ratios.append(1/(lam*n*(n-1)))
    check(all(a < b for a,b in zip(ratios[4:],ratios[5:])), 'exact_math', 'C2 inverse ratios strictly increase for tested n >= 8')
    for r in range(1,9):
        abel_coefficient = s.simplify(r*s.gamma(r)*s.gamma(half)/s.gamma(r+half))
        check(s.simplify(abel_coefficient**2) <= 16*r, 'exact_math', f'mixed-norm Abel benchmark {r}')
    for m in range(4,8):
        h = s.Rational(1,8)
        nodes = [k*h for k in range(1,m+1)]
        for degree in range(m):
            poly = s.interpolate([(z,z**degree) for z in nodes],x)
            check(s.expand(poly-x**degree)==0, 'exact_math', f'positive-node reproduction m={m},degree={degree}')
        errors=[]
        for hh in [h,h/2]:
            pp=s.interpolate([(k*hh,(k*hh)**m) for k in range(1,m+1)],x)
            errors.append(s.diff(pp-x**m,x,3).subs(x,0))
        check(errors[0] == 2**(m-3)*errors[1] and errors[1]!=0, 'exact_math', f'first-cell approximation order m={m}')
    noise=[]
    for h in [s.Rational(1,8),s.Rational(1,16)]:
        pp=s.interpolate([(k*h,(-1)**k) for k in range(1,5)],x)
        noise.append(s.diff(pp,x,3))
    check(noise[1]==8*noise[0] and noise[0]!=0, 'exact_math', 'scalar noise cubic amplification')
    M,t=s.symbols('M t',positive=True)
    tilt=t/(M+t/3)
    exponent=-tilt*t+M*tilt**2/(2*(1-tilt/3))
    check(s.simplify(exponent+t**2/(2*(M+t/3)))==0, 'exact_math', 'Bernoulli mgf exponent')
    m=s.symbols('m',integer=True,positive=True)
    check(s.simplify(2+(2+6)/(m-3)-(2+8/(m-3)))==0, 'exact_math', 'preparation exponent before bridge penalty')
    d,j,dg=s.symbols('d j dg',positive=True)
    check(s.diff(((d+j*dg)/d)**2,dg).subs(dg,0)==2*j/d, 'exact_math', 'gap normalization sensitivity')
    g,delta=s.symbols('g delta',positive=True)
    ratio=s.sinh(j*(g+delta))/s.sinh(j*g)
    check(s.simplify(s.diff(ratio,delta).subs(delta,0)-j/s.tanh(j*g))==0, 'exact_math', 'multiplier normalization sensitivity')
    results={'schema':'a2-v10-independent-referee-checks-v1','status':'pass','source':identity,
             'retention':retention,'counts':dict(COUNTS),'math_imports_manuscript_code':False,
             'formal_proof_verification':False,'remote_ci':False,
             'C2_inverse_ratio_samples': {str(n): str(ratios[n-4]) for n in [4,10,20,40]},
             'limitations':'Finite exact arithmetic and source checks, not a proof of analytic theorems, a statistical simulation, or an optimal physical sampling lower bound.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(results,sort_keys=True,indent=2)+'\n')
    print(json.dumps(results,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
