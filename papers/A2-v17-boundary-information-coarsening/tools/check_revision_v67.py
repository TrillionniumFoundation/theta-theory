#!/usr/bin/env python3
"""A2 v67 finite controls and exact source retention; not a proof certificate.

Uses only the Python standard library. Run with Python and Python -O; outputs
must agree. Numeric tests use exact rational arithmetic, including signed blocks.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'history/v66-review-baseline'
EDITED = {
    'main.tex', 'rigidity.tex', 'README.md',
    'article/00g_contact_synthesis_v66.tex', 'article/00h_abstract_v66.tex',
    'article/10c_global_curvature_inverse_v66.tex',
    'journal/references_v56.tex', 'v5/references_v43.tex',
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def norm(v: list[F]) -> F:
    return max(map(abs, v), default=F(0))


def distance(v: list[F], w: list[F]) -> F:
    return norm([a - b for a, b in zip(v, w)])


def phi(k: list[F], s: list[F], z: list[F]) -> list[F]:
    r = len(k)
    return [max(F(0), s[i] - k[i] + k[i]**2 /
                (k[i] + s[(i + 1) % r] + z[(i + 1) % r])) for i in range(r)]


def qbound(k: list[F], s: list[F]) -> F:
    return max((k[i] / (k[i] + s[(i + 1) % len(k)]))**2 for i in range(len(k)))


def eye(r: int) -> list[list[F]]:
    return [[F(i == j) for j in range(r)] for i in range(r)]


def matadd(a, b, sign=1):
    return [[x + sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matnorm(a):
    return max(sum(map(abs, row), F(0)) for row in a)


def inverse(a):
    r = len(a)
    w = [row[:] + ir for row, ir in zip(a, eye(r))]
    for j in range(r):
        pivot = next((i for i in range(j, r) if w[i][j]), None)
        require(pivot is not None, 'Singular signed block')
        w[j], w[pivot] = w[pivot], w[j]
        factor = w[j][j]
        w[j] = [x/factor for x in w[j]]
        for i in range(r):
            if i != j:
                factor = w[i][j]
                w[i] = [x-factor*y for x, y in zip(w[i], w[j])]
    return [row[r:] for row in w]


def block(k, s, v, signs, degree):
    r = len(k)
    shift = [[F(0) for _ in range(r)] for _ in range(r)]
    for i in range(r):
        shift[i][(i+1) % r] = (signs[i]*k[i] /
                    (k[i]+s[(i+1) % r]+v[(i+1) % r]))**degree
    inv = inverse(matadd(eye(r), shift))
    b = matmul(matadd(eye(r), shift, -1), inv)
    require(b == matadd([[2*x for x in row] for row in inv], eye(r), -1),
            'Resolvent identity failed')
    return b


def active_graph(base: Path, entry: str, visited=None, old=False):
    visited = set() if visited is None else visited
    if entry in visited:
        return visited
    visited.add(entry)
    p = BASE/entry if old and entry in EDITED else base/entry
    require(p.is_file(), 'Missing active input: '+entry)
    # TeX comments not preceded by an odd escape count; filenames use no escaped %.
    text = re.sub(r'(?<!\\)%[^\n]*', '', p.read_text())
    for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', text):
        active_graph(base, name if name.endswith('.tex') else name+'.tex', visited, old)
    return visited


def source_checks():
    m = json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    unchanged, archived = 0, []
    for name, rec in m['files'].items():
        path = ROOT/name
        require(path.is_file(), 'Removed inherited path: '+name)
        expected = BASE/name if name in EDITED else path
        data = expected.read_bytes()
        require(len(data) == rec['bytes'] and hashlib.sha256(data).hexdigest() == rec['sha256']
                and blob(data) == rec['git_blob'], 'Inherited bytes differ: '+name)
        if name in EDITED:
            archived.append(name)
        else:
            unchanged += 1
    old = {e: active_graph(ROOT, e+'.tex', old=True)
           for e in ('main', 'rigidity', 'two_collision')}
    new = {e: active_graph(ROOT, e+'.tex') for e in old}
    for e in old:
        require(old[e] == new[e], 'Changed active input inventory: '+e)
    module = (ROOT/'article/10c_global_curvature_inverse_v66.tex').read_text()
    previous = (BASE/'article/10c_global_curvature_inverse_v66.tex').read_text()
    for label in re.findall(r'\\label\{([^}]+)\}', previous):
        require('\\label{'+label+'}' in module, 'Removed old statement/equation: '+label)
    for phrase in ('eq:v67-residual-error','eq:v67-complete-stopping-error',
                   'eq:v67-off-fixed-recursion','eq:v67-propagation-constants'):
        require(phrase in module, 'Missing quantitative proof element: '+phrase)
    return {'inherited_files': len(m['files']), 'unchanged_bytes': unchanged,
            'edited_files_with_exact_archives': sorted(archived),
            'active_union': len(set().union(*new.values())),
            'active_by_entry': {e:len(v) for e,v in new.items()},
            'all_inherited_labels_retained_in_corrected_module': True,
            'mode_scope': 'Git modes checked separately in the frozen/native source manifests'}


def rational_checks():
    iterations = residuals = positive_certificates = evaluations = pairs = blocks = 0
    cases = []
    for r in range(2, 10):
        for seed in range(8):
            k = [F(20+(3*i+seed) % 7, 20) for i in range(r)]
            a = [F(4+(i+seed) % 3, 20) for i in range(r)]
            c = [F(0)]*r
            for i in range(r):
                j=(i+1)%r
                c[j]=(k[i]/a[i]-k[i]-k[j]+k[j]*a[j])/2
            s=[k[i]+c[i]-k[i]*a[i] for i in range(r)]
            require(min(c)>0 and min(s)>0, 'Invalid rational positive class')
            require(phi(k,s,c)==c, 'Schur identity failed')
            q=qbound(k,s);require(0<q<1, 'Invalid contraction bound')
            z=[F(0)]*r;first=norm(phi(k,s,z))
            for m in range(13):
                zp=phi(k,s,z);e=distance(zp,z)/(1-q)
                err=distance(z,c)
                require(err<=q**m*first/(1-q), 'First-increment bound failed')
                require(err<=e, 'Residual bound failed')
                iterations+=1;residuals+=1
                eta=F(1,1000*(m+1))
                w=[x+(-1)**i*eta for i,x in enumerate(zp)]
                require(err<=(distance(w,z)+eta)/(1-q), 'Inexact evaluation bound failed')
                evaluations+=1
                if min(z)>e:
                    require(min(c)>0,'False positive image certificate')
                    positive_certificates+=1
                z=zp
            cases.append((k,s,c))
            st=[s[i]+F((i+seed)%4+1,100) for i in range(r)]
            at=[k[i]/(k[i]+st[(i+1)%r]+c[(i+1)%r]) for i in range(r)]
            alpha=max(at)
            dstar=max(k[i]/(k[i]+st[(i+1)%r]+c[(i+1)%r])**2 for i in range(r))
            v=[c[i]+F(i+1,100) for i in range(r)]
            signs=[F(-1 if (i+seed)%3==0 else 1) for i in range(r)]
            for n in range(3,7):
                b=block(k,st,c,signs,n);bv=block(k,st,v,signs,n)
                bound=(1+alpha**n)/(1-alpha**n)
                beta=2*n*alpha**(n-1)*dstar/(1-alpha**n)**2
                require(matnorm(b)<=bound,'Signed block norm bound failed')
                require(matnorm(matadd(b,bv,-1))<=beta*distance(c,v),
                        'Signed block Lipschitz bound failed')
                blocks+=1
    # Compare two distinct realized quadratic data with identical flight lengths.
    for k,s,c in cases:
        a=[F(1,4)]*len(k);d=[F(0)]*len(k)
        for i in range(len(k)):
            j=(i+1)%len(k);d[j]=(k[i]/a[i]-k[i]-k[j]+k[j]*a[j])/2
        t=[k[i]+d[i]-k[i]*a[i] for i in range(len(k))]
        qs=qbound(k,[min(x,y) for x,y in zip(s,t)])
        require(distance(c,d)<=(1+qs)/(1-qs)*distance(s,t),'Data Lipschitz bound failed')
        pairs+=1
    require(phi([F(1)]*2,[F(1,10),F(10)],[F(0),F(109,11)])==[F(0),F(109,11)],
            'Positive nonimage control failed')
    s=[F(3,4)]*2;k=[F(1)]*2;c=[F(1,4)]*2
    z1=phi(k,s,[F(0)]*2);z2=phi(k,s,z1)
    require(z1[0]>c[0]>z2[0], 'Nonmonotone iteration control failed')
    e1=qbound(k,s)*norm(z1)/(1-qbound(k,s))
    require(e1==F(12,77),'Referee curvature certificate mismatch')
    a=1/(1+s[1]+z1[1]);q3=(1-a**3)/(1+a**3)*F(90,7)
    err=q3-10
    require(a==F(14,29) and err==F(48740,189931) and err>e1,
            'Coefficient-one cubic propagation control failed')
    # The other implementation recomputes actual tails; compare the irrational
    # closed expression by squaring positive rational quantities, without floats.
    require(F(65)>((10+e1)*F(2093,2754))**2,
            'Actual-tail cubic amplification control failed')
    beta3=2*3*F(1,2)**2*F(1,4)/(1-F(1,2)**3)**2
    l3=max(F(1),beta3*F(90,7))
    require(err<=l3*distance(z1,c)<=l3*e1,'Corrected cubic propagation bound failed')
    return {'positive_periodic_quadratic_cases':len(cases),'periods':list(range(2,10)),
            'exact_first_increment_checks':iterations,'exact_residual_checks':residuals,
            'inexact_evaluation_checks':evaluations,'positive_stopping_certificates':positive_certificates,
            'two_point_data_checks':pairs,'signed_block_norm_and_lipschitz_checks':blocks,
            'positive_nonimage_and_nonmonotonicity_controls':True,
            'R66_m1':{'first_increment_bound':str(e1),'observed_Schur_cubic_error':str(err),
                      'coefficient_one_is_false':True,'sufficient_cubic_L3':str(l3),
                      'actual_tail_alternative_checked_by_exact_squaring':True},
            'scope':'Finite exact arithmetic controls, not global billiard realization or infinite-dimensional proof certification'}


def main():
    print(json.dumps({'revision':67,'status':'passed','source':source_checks(),
                      'mathematical_controls':rational_checks()},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
