#!/usr/bin/env python3
"""Independent finite checks for the frozen A2 v75 workflow archive.

Usage: python INDEPENDENT_CHECKS.py /path/to/a2-v75-native.zip
Requires Python 3.10+, SymPy and PyMuPDF. Does not execute manuscript code,
extract archive paths, access the network, rebuild TeX, or certify theorems.
Every failed check raises an exception, including under python -O.
"""
from __future__ import annotations
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
import zipfile

SOURCE = '89d5a3aa3e9f00a806d48f19f6f6831770184d76'
TREE = '8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d'
ARTIFACT = 'e51cc502c53d82018f5160715d7e0f75f9b872d79d6b7125585a2be41ee31cdf'


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_object(kind: str, data: bytes) -> bytes:
    return hashlib.sha1(f'{kind} {len(data)}\0'.encode() + data).digest()


def git_tree(records: dict[str, tuple[str, bytes]]) -> str:
    root: dict = {}
    for path, value in records.items():
        parts = path.split('/')
        require(all(p and p not in ('.', '..') for p in parts), 'Unsafe source path')
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        require(parts[-1] not in node, 'Duplicate source path')
        node[parts[-1]] = value

    def encode(node: dict) -> bytes:
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                entries.append((name.encode() + b'/', b'40000 ' + name.encode()
                                + b'\0' + git_object('tree', encode(value))))
            else:
                mode, blob = value
                entries.append((name.encode(), mode.encode() + b' ' + name.encode()
                                + b'\0' + blob))
        return b''.join(v for _, v in sorted(entries))
    return git_object('tree', encode(root)).hex()


def finite_algebra() -> dict:
    import sympy as s
    R = s.Rational
    k = [R(1), R(6, 5), R(4, 5)]
    a = [R(1, 5), R(3, 10), R(2, 5)]
    c = [(k[(j-1) % 3] * (1/a[(j-1) % 3]-1)
          - k[j]*(1-a[j]))/2 for j in range(3)]
    sh = [k[j]+c[j]-k[j]*a[j] for j in range(3)]
    require(all(x > 0 for x in c), 'Positive curvature fixture')
    for j in range(3):
        nxt = (j+1) % 3
        require(s.simplify(sh[j] - k[j]-c[j]
                          + k[j]**2/(k[j]+c[nxt]+sh[nxt])) == 0,
                'Riccati identity')
        phi = sh[j]-k[j]+k[j]**2/(k[j]+sh[nxt]+c[nxt])
        require(s.simplify(phi-c[j]) == 0, 'Inverse fixed point')
    # Exact nonconstant Jacobi/cofactor/transfer checks; P=6 returns frames.
    Q = [s.Matrix([[1+2*c[j]/k[j], 1/k[j]], [2*c[j], 1]])
         for j in range(3)]
    M = s.eye(2)
    for j in range(6):
        M = Q[j % 3]*M
    transfer = []
    for n in (1, 2, 3):
        N = 6*n
        H = s.zeros(N-1)
        for i in range(1, N):
            H[i-1, i-1] = k[(i-1) % 3]+k[i % 3]+2*c[i % 3]
            if i < N-1:
                H[i-1, i] = H[i, i-1] = -k[i % 3]
        cof = s.prod(k[j % 3] for j in range(N))/H.det()
        Mn = M**n
        require(s.simplify(cof-1/Mn[0, 1]) == 0, 'Cofactor/transfer mismatch')
        require(s.simplify(Mn[0, 1]-M[0, 1]*s.chebyshevu(n-1, s.trace(M)/2)) == 0,
                'Cayley-Hamilton normalization mismatch')
        transfer.append(N)
    signed = []
    for r in (3, 4):
        sigma = [(-1 if j == 1 else 1)*R(1, j+2) for j in range(r)]
        lam = s.prod(sigma)
        for n in (2, 3, 4, 7):
            T = s.zeros(r)
            for j in range(r):
                T[j, (j+1) % r] = sigma[j]**n
            I = s.eye(r)
            C = (I+T)*(I-T).inv()
            require(T**r == lam**n*I, 'Cyclic power')
            target = (1-(-1)**r*lam**n)/(1-lam**n)
            require(s.simplify(C.det()-target) == 0, 'Signed determinant')
            signed.append([r, n])
    u, v, p, d, d1, d2 = s.symbols('u v p d d1 d2', nonzero=True)
    A = -p*u+u**2
    C = p*v+2*v**2
    h = A+C
    quotient = (1-h/d1)/(1-h/d2)
    require(s.simplify(d1*d2*(1-quotient)/(d2-d1*quotient)-h) == 0,
            'Two-offset quotient')
    cross = d*(d-A-C)/((d-A)*(d-C))
    require(s.simplify(s.diff(cross, u, v).subs({u: 0, v: 0})-p**2/d**2) == 0,
            'Single-offset mixed derivative')
    rad = s.symbols('R', positive=True)
    f = (d+p*u-p*v)/(4*rad**2*d)
    H = s.Matrix(2, 2, lambda i,j: s.integrate(f*u**i*v**j,
                   (u, -rad, rad), (v, -rad, rad)))
    require(s.simplify(H.det()-p**2*rad**4/(9*d**2)) == 0, 'Affine determinant')
    avec = p*rad**2/(3*d)
    require(s.simplify(H.inv()-s.Matrix([[0, 1/avec],[-1/avec, 1/avec**2]]))
            == s.zeros(2), 'Affine inverse')
    f0 = (4+u/2-v/2)/16
    f1 = f0+(u**2-R(1,3))*(v**2-R(1,3))/100
    def compressed(fx):
        m = s.Matrix([[s.integrate(fx*v**j, (v,-1,1)) for j in range(2)]])
        n = s.Matrix([s.integrate(fx*u**j, (u,-1,1)) for j in range(2)])
        hh = s.Matrix(2,2,lambda i,j:s.integrate(fx*u**i*v**j,(u,-1,1),(v,-1,1)))
        return m, n, hh
    m, n, hh = compressed(f0)
    require(compressed(f1) == (m,n,hh), 'Invisible perturbation compression')
    require(s.simplify((m*hh.inv()*n)[0]-f0) == 0, 'Nonsymmetric reconstruction')
    require(s.simplify((m*hh.inv().T*n)[0]-f0) != 0, 'Transpose negative control')
    require(s.simplify((m*hh.inv()*n)[0]-f1) != 0, 'Finite rank negative control')
    coefficient = lambda fx: s.Matrix(3,3,lambda i,j:s.expand(fx).coeff(u,i).coeff(v,j))
    require(coefficient(f0).rank() == 2 and coefficient(f1).rank() == 3,
            'Kernel ranks')
    thresholds = []
    for ar in (R(1,2), R(9,10), R(99,100)):
        order = 3
        while 6*ar**order/(1-ar**order) >= 1:
            order += 1
        thresholds.append({'a':str(ar),'minimum_m_at_least_3':order,
                           'tail_bound':float(6*ar**order/(1-ar**order))})
    return {'exact_heterogeneous_transfer_flights':transfer,
            'exact_positive_curvatures':list(map(str,c)),
            'exact_action_hessians':list(map(str,sh)),
            'signed_cycle_cases':signed, 'two_offset_and_clock_identities':True,
            'affine_conditioning_identity':True, 'nonsymmetric_reconstruction':True,
            'rank_three_negative_control':True, 'weighted_thresholds':thresholds,
            'qualification':'Finite algebra only. The polynomial kernels are not asserted to be billiard realizations.'}


def inspect(archive: Path) -> dict:
    import fitz
    raw = archive.read_bytes()
    require(digest(raw) == ARTIFACT, 'Unexpected workflow archive digest')
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        manifest = json.loads(outer.read('frozen-source-manifest.json'))
        require(manifest['source_commit'] == SOURCE, 'Source commit mismatch')
        records = {}
        with zipfile.ZipFile(io.BytesIO(outer.read('native-source.zip'))) as z:
            files = {n.removeprefix('source/'):z.read(n) for n in z.namelist()
                     if n.startswith('source/') and not n.endswith('/')}
            require(set(files) == set(manifest['files']), 'File-set mismatch')
            for path, m in manifest['files'].items():
                data = files[path]
                blob = git_object('blob', data)
                mode = '100755' if (z.getinfo('source/'+path).external_attr >> 16) & 0o111 else '100644'
                require(len(data) == m['bytes'] and digest(data) == m['sha256']
                        and blob.hex() == m['git_blob'] and mode == m['mode'],
                        'Source bytes/hash/mode mismatch: '+path)
                records[path] = (mode,blob)
        tree = git_tree(records)
        require(tree == TREE == manifest['source_tree'], 'Reconstructed tree mismatch')
        retention = json.loads(files['verification/v75-baseline-preservation.json'])
        archived = []
        old_records = {}
        for path, m in retention['files'].items():
            require(path in files, 'Removed original source path')
            held = m['archive'] or path
            data = files[held]
            require(digest(data) == m['sha256'] and len(data) == m['bytes'],
                    'Baseline-retention mismatch')
            old_records[path] = (records[held][0],git_object('blob',data))
            if m['archive']:
                archived.append(path)
        baseline_tree = git_tree(old_records)
        require(baseline_tree == retention['base_tree'], 'Restored v74 tree mismatch')
        dep = json.loads(files['DEPENDENCY_MAP_V75.json'])
        for cut in dep['shared_core_slices'].values():
            prefix = files[cut['full_original']].split(cut['split_marker'].encode())[0]
            require(prefix == files[cut['principal']], 'Principal slice mismatch')
        def closure(entry):
            seen = set()
            def walk(path):
                if path in seen:
                    return
                require(path in files, 'Missing active input '+path)
                seen.add(path)
                text = re.sub(r'(?<!\\)%[^\n]*', '', files[path].decode())
                for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
                    require('\\' not in child, 'Unsupported dynamic input')
                    walk(child if child.endswith('.tex') else child+'.tex')
            walk(entry)
            return seen
        entry_closures = {e:closure(e) for e in ('rigidity.tex','main.tex','two_collision.tex')}
        union = set().union(*entry_closures.values())
        active_text = '\n'.join(files[p].decode() for p in union)
        labels = set(re.findall(r'\\label\{([^}]+)\}',active_text))
        old_labels = json.loads(files['verification/v75-active-labels.json'])['inherited_labels']
        require(set(old_labels) <= labels, 'Inherited active label lost')
        principal_text = '\n'.join(files[p].decode() for p in entry_closures['rigidity.tex'])
        principal_labels = set(re.findall(r'\\label\{([^}]+)\}',principal_text))
        refs = set(re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}',principal_text))
        aliases = set(dep['external_aliases'])
        missing = refs-principal_labels-aliases
        require(not missing, 'Unresolved principal labels: '+repr(missing))
        pdfs = {}
        for entry, expected_pages in [('rigidity',48),('main',369),('two_collision',7)]:
            data = outer.read(entry+'.pdf')
            with fitz.open(stream=data,filetype='pdf') as doc:
                pages = len(doc)
            require(pages == expected_pages, 'PDF page count mismatch')
            pdfs[entry] = {'pages':pages,'sha256':digest(data)}
        return {'schema':1,'source_commit':SOURCE,'source_tree':tree,
                'artifact_sha256':digest(raw),'artifact_id':10482862451,
                'verified_source_files':len(records),'restored_v74_tree':baseline_tree,
                'retained_baseline_files':len(retention['files']),
                'archived_originals':archived,'exact_principal_slices':2,
                'retained_inherited_labels':len(old_labels),'active_union_labels':len(labels),
                'literal_input_closure_sizes':{k:len(v) for k,v in entry_closures.items()},
                'principal_external_aliases':sorted(aliases),
                'unresolved_principal_references':sorted(missing),'pdfs':pdfs,
                'finite_checks':finite_algebra(),
                'scope':'No TeX rebuild, author-script execution, formal verification, or complete re-audit of the full technical catalogue.'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python INDEPENDENT_CHECKS.py a2-v75-native.zip')
    print(json.dumps(inspect(Path(sys.argv[1])),indent=2,sort_keys=True))
