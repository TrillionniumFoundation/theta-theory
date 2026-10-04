#!/usr/bin/env python3
"""Source-preservation checks and finite algebra; not continuum certification."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def closure(path: Path, stack: tuple[Path, ...] = ()) -> list[Path]:
    path = path.resolve()
    require(path.is_relative_to(ROOT), 'manuscript input leaves paper directory')
    require(path not in stack, 'cyclic TeX input')
    text = path.read_text(encoding='utf-8')
    result = [path]
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        child = ROOT / name
        if not child.suffix:
            child = child.with_suffix('.tex')
        result.extend(closure(child, stack + (path,)))
    return result


def finite_algebra() -> dict[str, int]:
    counts = {'nonnegative_L1_identity': 0, 'uniform_integrability_bound': 0,
              'conditional_ratio_bound': 0, 'suspension_normalization': 0}
    for h in range(9):
        for g in range(9):
            require(abs(h-g) == h+g-2*min(h,g), 'L1 identity')
            counts['nonnegative_L1_identity'] += 1
            for a in (F(1,2), F(2), F(5)):
                lhs = h if h > a else 0
                rhs = 2*abs(h-g) + (2*g if g > a/2 else 0)
                require(lhs <= rhs, 'UI truncation bound')
                counts['uniform_integrability_bound'] += 1
    for br in (F(1,5), F(1,2), F(4,5)):
        for change in (F(-1,20), F(0), F(1,20)):
            bs = br + change
            for ar in (-br, F(0), br):
                for a_s in (-bs, F(0), bs):
                    d = abs(change)
                    bound = (abs(ar-a_s)+d)/(br-d)
                    require(abs(ar/br-a_s/bs) <= bound, 'positive denominator')
                    counts['conditional_ratio_bound'] += 1
    weights = [F(1,3), F(2,3)]
    roofs = [F(2), F(5)]
    mean = sum(w*h for w,h in zip(weights,roofs))
    require(sum(w*h/mean for w,h in zip(weights,roofs)) == 1,
            'stationary normalization')
    for q in (F(0), F(1), F(2), F(4), F(5), F(6)):
        containing = sum(w*h for w,h in zip(weights,roofs) if h > q)/mean
        age = sum(w*max(h-q,0) for w,h in zip(weights,roofs))/mean
        require(0 <= age <= containing <= 1, 'length-biased bound')
        counts['suspension_normalization'] += 1
    return counts


def run() -> dict:
    paths = closure(ROOT/'main.tex')
    require(len(paths) == len(set(paths)), 'duplicate active source input')
    text = '\n'.join(p.read_text(encoding='utf-8') for p in paths)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    require(len(labels) == len(set(labels)), 'duplicate label')
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', text)
    require(set(refs) <= set(labels), 'unresolved source reference')
    blocks = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', text, re.S)
    hashes = Counter(sha256(p.encode()).hexdigest() for p in blocks)
    baseline = json.loads((ROOT/'PROOF_BASELINE.json').read_text())
    for key in ('v2_proof_body_sha256',):
        require(not (Counter(baseline[key])-hashes), 'v2 proof changed or removed')
    require(set(baseline['v2_labels']) <= set(labels), 'v2 label removed')
    v1 = baseline['v1']
    require(not (Counter(v1['proof_body_sha256'])-hashes), 'v1 proof changed')
    require(set(v1['active_labels']) <= set(labels), 'v1 label removed')
    for name, expected in baseline['unchanged_v2_files'].items():
        require(sha256((ROOT/name).read_bytes()).hexdigest() == expected,
                'retained source changed: '+name)
    require(len(blocks) == 28 and len(labels) == 78, 'unexpected source inventory')
    return {
        'schema': 'a2-dyn-v3-source-and-finite-audit-1', 'status': 'passed',
        'proof_blocks': len(blocks), 'labels': len(labels),
        'v2_proofs_preserved': len(baseline['v2_proof_body_sha256']),
        'v2_labels_preserved': len(baseline['v2_labels']),
        'v1_proofs_preserved': len(v1['proof_body_sha256']),
        'v1_labels_preserved': len(v1['active_labels']),
        'finite_algebra': finite_algebra(),
        'source_sha256': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                          for p in paths},
        'formal_continuum_certificate': False, 'full_raw_LLT_verified': False,
        'independent_human_review': False,
        'scope': 'Literal source closure, byte preservation and finite exact algebra only.'
    }


if __name__ == '__main__':
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc)}))
        raise SystemExit(1)
