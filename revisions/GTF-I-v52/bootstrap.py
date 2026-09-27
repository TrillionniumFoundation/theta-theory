#!/usr/bin/env python3
"""Materialize the frozen v52 source recipe without modifying its predecessor."""
from __future__ import annotations
import argparse
import bz2
import hashlib
import json
from pathlib import Path, PurePosixPath

PATCH_SHA = '1ab06ab91906c7b594f80f48d340c059417d80783445b98d8ae328e838c37737'
BASE = '6363748923a5623801a53cfdb507a776aad414c3'
REVIEW = '9d2f516b4113016f57fc8193c24ba192f8f782d5'
AUDIT_BEFORE = 'bcafec4f2b120bd1fe1a80f8c0ad6f3fbca31ebb5e2178fcec28f07c269e2741'
AUDIT_AFTER = '33a55ac81e2bd298e49d4b91c7cd280e11618a97185ba65f5fb65ee7c039816c'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(root: Path, name: str) -> Path:
    rel = PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or rel.suffix not in {'.tex', '.py', '.json', '.md'}:
        raise ValueError('Unsafe native source name: ' + name)
    target = root.joinpath(*rel.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Native source path escapes root: ' + name)
    return target


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    root = ap.parse_args().root.resolve()
    transfer = root / 'revisions/GTF-I-v52'
    old = root / 'papers/GTF-I-v51-compatible-lifts'
    new = root / 'papers/GTF-I-v52-quantitative-lifts'
    raw = bz2.decompress(b''.join((transfer / f'part-{i:02}.bz2').read_bytes() for i in range(1, 5)))
    if digest(raw) != PATCH_SHA:
        raise ValueError('Source recipe digest mismatch')
    patch = json.loads(raw)
    if (patch['schema'], patch['base_publication'], patch['review_commit']) != ('gtf52.source-patch/1', BASE, REVIEW):
        raise ValueError('Unexpected source genealogy')
    expected = patch['source_hashes']
    if len(expected) != 59 or not set(patch['files']).issubset(expected):
        raise ValueError('Unexpected native source inventory')
    assembled: dict[str, bytes] = {}
    for name, wanted in expected.items():
        source = safe_path(old, patch['aliases'].get(name, name))
        recipe = patch['files'].get(name)
        if recipe is None:
            data = source.read_bytes()
        elif 'text' in recipe:
            data = recipe['text'].encode('utf-8')
        else:
            previous = source.read_bytes()
            if digest(previous) != recipe['base_sha256']:
                raise ValueError('Frozen predecessor mismatch: ' + name)
            lines = previous.decode('utf-8').splitlines(keepends=True)
            fragments = []
            for item in recipe['lines']:
                if isinstance(item, str):
                    fragments.append(item)
                elif (isinstance(item, list) and len(item) == 2 and
                      all(type(x) is int for x in item) and 0 <= item[0] <= item[1] <= len(lines)):
                    fragments.append(''.join(lines[item[0]:item[1]]))
                else:
                    raise ValueError('Invalid line recipe: ' + name)
            data = ''.join(fragments).encode('utf-8')
        if digest(data) != wanted:
            raise ValueError('Assembled source digest mismatch: ' + name)
        assembled[name] = data
    # Verified bibliographic metadata correction, before native commit/qualification.
    # The article's bibliography and mathematical source are unchanged by this step.
    name = 'LITERATURE_AUDIT.md'
    if digest(assembled[name]) != AUDIT_BEFORE:
        raise ValueError('Bibliographic preimage mismatch')
    text = assembled[name].decode('utf-8')
    changes = [
        ('“Finite convergence of the Moment-SOS hierarchy for polynomial optimization on the simplex,”',
         '“On the complexity of matrix Putinar’s Positivstellensatz,”'),
        ('this revision proves its sharper finite-convergence results',
         'this revision proves its matrix-valued degree bounds'),
    ]
    for before, after in changes:
        if text.count(before) != 1:
            raise ValueError('Bibliographic correction precondition failed')
        text = text.replace(before, after)
    assembled[name] = text.encode('utf-8')
    if digest(assembled[name]) != AUDIT_AFTER:
        raise ValueError('Bibliographic correction digest mismatch')
    for name, data in assembled.items():
        target = safe_path(new, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != data:
            raise ValueError('Refusing to overwrite divergent native source: ' + name)
        target.write_bytes(data)
    print(json.dumps({'schema': 'gtf52.assembly/1', 'native_sources': len(assembled),
                      'recipe_sha256': PATCH_SHA, 'base_publication': BASE,
                      'review_commit': REVIEW, 'corrected_audit_sha256': AUDIT_AFTER}, sort_keys=True))


if __name__ == '__main__':
    main()
