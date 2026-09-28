#!/usr/bin/env python3
"""Exact finite diagnostics and source preservation for the A2 v14 revision.

Default mode requires the Git checkout and the pinned native v13 snapshot.
--algebra-only runs just the finite algebra and binds the new source files.
Neither mode certifies the analytic, geometric, or statistical proofs.
All checks use explicit exceptions and remain active under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import comb, factorial
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_TREE = 'ee946ef91770778839f15c8c35416d401e99ea1c'
NEW_INPUTS = ['article/01a_relative_observability.tex',
              'article/16_normal_form_comparison.tex',
              'article/31_regular_observability.tex']
COUNTS: Counter[str] = Counter()


def need(ok: bool, group: str, message: str) -> None:
    if not ok:
        raise RuntimeError(f'{group}: {message}')
    COUNTS[group] += 1


def determinant(matrix: list[list[Q]]) -> Q:
    a = [list(map(Q, row)) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError('Expected a square matrix')
    result = Q(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            result = -result
        d = a[k][k]
        result *= d
        for i in range(k + 1, n):
            f = a[i][k] / d
            for j in range(k + 1, n):
                a[i][j] -= f * a[k][j]
            a[i][k] = Q(0)
    return result


def node_matrix(left: list[Q], right: list[Q]) -> list[list[Q]]:
    n = len(right)
    if len(left) != n + 1:
        raise ValueError('Need n+1 left nodes and n right nodes')
    return ([[Q(1)] + [s**k for k in range(1, n + 1)] + [Q(0)]*n
             for s in left] +
            [[Q(1)] + [Q(0)]*n + [t**k for k in range(1, n + 1)]
             for t in right])


def vandermonde(nodes: list[Q]) -> Q:
    result = Q(1)
    for j in range(len(nodes)):
        for i in range(j):
            result *= nodes[j] - nodes[i]
    return result


def algebra() -> None:
    # Joint intercept: independent determinant expansion, including h scaling.
    for n in range(1, 11):
        left = [Q(i) for i in range(1, n + 2)]
        right = [Q(i) for i in range(1, n + 1)]
        d1 = Q(1)
        for k in range(1, n + 1):
            d1 *= factorial(k)**2
        need(determinant(node_matrix(left, right)) == d1,
             'joint_nodes', f'equispaced determinant n={n}')
        for h in [Q(1, 2), Q(1, 5), Q(1, 10)]:
            matrix = node_matrix([h*s for s in left], [h*t for t in right])
            need(determinant(matrix) == h**(n*(n+1))*d1,
                 'joint_nodes', f'scaled determinant n={n}, h={h}')
        l2 = [Q(i*i + 1, i + 1) for i in range(1, n + 2)]
        r2 = [Q(i + 2, i + 1) for i in range(1, n + 1)]
        expected = vandermonde(l2)*vandermonde(r2)
        for t in r2:
            expected *= t
        need(expected != 0 and determinant(node_matrix(l2, r2)) == expected,
             'joint_nodes', f'nonuniform determinant n={n}')
        singular = node_matrix(left[:-1] + [left[0]], right)
        need(determinant(singular) == 0, 'joint_nodes', f'repeated node n={n}')

    # The retained two-contact diagonal blocks, independently evaluated exactly.
    for c0 in [Q(11, 10), Q(3, 2), Q(2), Q(4)]:
        for c1 in [Q(11, 10), Q(3, 2), Q(2), Q(4)]:
            z = c0*c1 - 1
            for g in [Q(1, 2), Q(1), Q(3, 2)]:
                L0, L1 = g/(2*c0*z), g/(2*c1*z)
                for m in range(2, 16):
                    k = Q(4, 2**m*(m+1)*factorial(m)**2)
                    U, V = (1+2*z)**m, 1+2*m*z
                    difference = sum((Q(comb(m, r))*(2*z)**r
                                      for r in range(2, m+1)), Q(0))
                    need(U-V == difference and difference > 0,
                         'two_contact_blocks', 'positive eigenvalue difference')
                    mat = [[-k*L0**m*U, -k*L1**m*V],
                           [-k*L0**m*V, -k*L1**m*U]]
                    need(determinant(mat) == k*k*(L0*L1)**m*(U*U-V*V) > 0,
                         'two_contact_blocks', 'positive block determinant')
    k, L, z = Q(1, 12), Q(1, 12), Q(3)
    U, V = (1+2*z)**2, 1+4*z
    need(-k*L**2*U == -Q(49, 1728) and -k*L**2*V == -Q(13, 1728),
         'two_contact_blocks', 'quartic reference entries')

    # Implicit differentiation from F=I-st Delta(I)^n and p=t Delta(I)^n.
    # s,t are chosen to satisfy F=0 exactly; this is finite algebra, not an
    # existence or exponential-convergence check for an unknown nonlinear orbit.
    for n in range(1, 21):
        delta, derivative, I, s = Q(3, 4), Q(1, 10), Q(1, 1000), Q(1, 5)
        power = delta**n
        t = I/(s*power)
        F_I = 1-s*t*n*delta**(n-1)*derivative
        I_t = s*power/F_I
        direct = power+t*n*delta**(n-1)*derivative*I_t
        D = 1-n*I*derivative/delta
        need(direct == power/D, 'normal_form_algebra', f'implicit derivative n={n}')

    # Nontrivial canonical shears: independently pull du wedge dP back.
    for a in [Q(-1, 3), Q(0), Q(1, 4)]:
        for b in [Q(-1, 5), Q(0), Q(2, 5)]:
            for s, t in [(Q(0), Q(0)), (Q(1, 20), Q(-1, 30))]:
                for n in [1, 2, 7, 20]:
                    scale = Q(1, 2)**n
                    us, ut = 1+2*a*s, scale
                    ps, pt = -Q(1, 2)+a*s, scale/2
                    vs, vt = scale, 1+2*b*t
                    det = us*vt-ut*vs
                    numerator = us*pt-ut*ps
                    need(numerator == scale, 'projection_example', 'canonical wedge numerator')
                    need(numerator/det == scale/((1+2*a*s)*(1+2*b*t)-scale**2),
                         'projection_example', 'physical flux with projection')
    # Normalized area-compensator derivative at the disk, divided by pi.
    for M in range(2, 21):
        normalized = -Q(2*comb(2*M+2, M+1), 4**(M+1))
        need(normalized < 0, 'area_compensator', f'disk derivative M={M}')


def clean_tex(text: str) -> str:
    return re.sub(r'(?<!\\)%[^\n]*', '', text)


def active_sources(root: Path, entry: str = 'main.tex') -> dict[str, bytes]:
    pending, result = [entry], {}
    while pending:
        name = pending.pop()
        if name in result:
            continue
        path = root / name
        if not path.is_file():
            raise RuntimeError(f'Missing active source: {path}')
        result[name] = path.read_bytes()
        text = clean_tex(result[name].decode('utf-8'))
        for item in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
            if '#' in item or '\\' in item:
                raise RuntimeError(f'Unresolved dynamic TeX input in {name}: {item}')
            pending.append(item if item.endswith('.tex') else item + '.tex')
    return result


def blocks(data: bytes, envs: str) -> list[str]:
    text = data.decode('utf-8')
    pattern = r'\\begin\{(' + envs + r')\}.*?\\end\{\1\}'
    return [match.group(0) for match in re.finditer(pattern, text, re.S)]


def source_check() -> dict:
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=ROOT, text=True).strip())
    rel = ROOT.relative_to(repo).as_posix()
    archive_path = rel + '/history/v13-reviewed'
    native = subprocess.check_output(['git', 'rev-parse', f'HEAD:{archive_path}'],
                                     cwd=repo, text=True).strip()
    need(native == BASE_TREE, 'source', 'reviewed native tree identity')
    base = ROOT / 'history/v13-reviewed'
    before, after = active_sources(base), active_sources(ROOT)
    need(set(before) <= set(after), 'source', 'all old active source paths retained')
    permitted_changes = {'main.tex', 'article/29_two_flight_benchmark.tex'}
    retained_results = retained_proofs = 0
    envs = 'theorem|lemma|proposition|corollary|definition|remark'
    for name, old_data in before.items():
        if name not in permitted_changes:
            need(after[name] == old_data, 'source', f'unchanged native source {name}')
        old_results, old_proofs = blocks(old_data, envs), blocks(old_data, 'proof')
        need(blocks(after[name], envs) == old_results,
             'source', f'old formal statements unchanged in {name}')
        need(blocks(after[name], 'proof') == old_proofs,
             'source', f'old proofs unchanged in {name}')
        retained_results += len(old_results)
        retained_proofs += len(old_proofs)
    for name in NEW_INPUTS:
        need(name in after, 'source', f'new input reachable: {name}')
    texts = [clean_tex(v.decode('utf-8')) for v in after.values()]
    labels = [x for text in texts for x in re.findall(r'\\label\{([^}]+)\}', text)]
    need(len(labels) == len(set(labels)), 'source', 'no duplicate active labels')
    companion = active_sources(ROOT, 'two_collision.tex')
    external = {'TC-' + x for v in companion.values()
                for x in re.findall(r'\\label\{([^}]+)\}', clean_tex(v.decode('utf-8')))}
    refs = {x for text in texts for x in
            re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', text) if '#' not in x}
    missing = sorted(refs-set(labels)-external)
    need(not missing, 'source', f'unresolved labels: {missing}')
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',
                         after['main.tex'].decode(), re.S).group(1)
    need('every fixed finite-dimensional family' not in abstract,
         'source', 'no unconditional family quantifier in abstract')
    return {'reviewed_native_tree': native, 'retained_active_files': len(before),
            'current_active_files': len(after), 'retained_result_environments': retained_results,
            'retained_proof_environments': retained_proofs, 'unresolved_references': missing,
            'new_result_environments': sum(len(blocks(after[n], envs)) for n in NEW_INPUTS),
            'new_proof_environments': sum(len(blocks(after[n], 'proof')) for n in NEW_INPUTS)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--algebra-only', action='store_true')
    args = parser.parse_args()
    algebra()
    source = {'status': 'not_run_algebra_only'} if args.algebra_only else source_check()
    hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
              for name in ['main.tex', *NEW_INPUTS, 'tools/verify_v14.py']}
    result = {'schema': 'a2-v14-diagnostics-1',
              'scope': 'finite_exact_algebra_only' if args.algebra_only else 'finite_exact_algebra_and_source_preservation',
              'checks': dict(sorted(COUNTS.items())), 'total_checks': sum(COUNTS.values()),
              'source': source, 'sha256': hashes, 'mathematical_proof_certificate': False,
              'editorial_decision': False}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
