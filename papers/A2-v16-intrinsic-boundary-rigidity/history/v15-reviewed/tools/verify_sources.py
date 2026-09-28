#!/usr/bin/env python3
"""Read-only byte preservation and TeX dependency checks; not a proof checker."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / 'history/v14-reviewed'
NATIVE_TREE = '5506d189c55aff9b2e67dc9bfee9602615e0909a'
EDITS = {'main.tex', 'article/16_normal_form_comparison.tex',
         'article/31_regular_observability.tex'}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def object_hash(kind: str, payload: bytes) -> str:
    return hashlib.sha1(kind.encode() + b' ' + str(len(payload)).encode()
                        + b'\0' + payload).hexdigest()


def tree_hash(path: Path) -> str:
    entries = []
    for p in path.iterdir():
        need(not p.is_symlink(), f'Unexpected symlink: {p}')
        directory = p.is_dir()
        mode = '40000' if directory else ('100755' if p.stat().st_mode & 0o111 else '100644')
        sha = tree_hash(p) if directory else object_hash('blob', p.read_bytes())
        entries.append((p.name.encode() + (b'/' if directory else b''),
                        mode.encode() + b' ' + p.name.encode() + b'\0' + bytes.fromhex(sha)))
    return object_hash('tree', b''.join(v for _, v in sorted(entries)))


def tex_inputs(path: Path) -> list[str]:
    return re.findall(r'\\input\{([^}]+)\}', path.read_text())


def dependency_closure(base: Path, entry: str) -> set[Path]:
    seen: set[Path] = set()
    def visit(relative: str) -> None:
        path = (base / relative).with_suffix('.tex').resolve()
        need(path.is_relative_to(base.resolve()), f'External TeX input: {path}')
        need(path.is_file(), f'Missing TeX input: {path}')
        if path in seen:
            return
        seen.add(path)
        for sub in tex_inputs(path):
            visit(sub)
    visit(entry)
    return seen


def main() -> None:
    actual_tree = tree_hash(FROZEN)
    need(actual_tree == NATIVE_TREE, 'Frozen native v14 tree does not match its Git pin')
    prior_files = [p for p in FROZEN.rglob('*') if p.is_file()]
    changed = []
    for old in prior_files:
        rel = old.relative_to(FROZEN).as_posix()
        new = ROOT / 'complete' / rel
        need(new.is_file(), f'Inherited file missing: {rel}')
        if new.read_bytes() != old.read_bytes():
            changed.append(rel)
            need(rel in EDITS, f'Unlisted inherited change: {rel}')
    need(set(changed) == EDITS, 'The three declared companion edits must be present')
    old_main = (FROZEN / 'main.tex').read_text()
    new_main = (ROOT / 'complete/main.tex').read_text()
    need(tex_inputs(FROZEN / 'main.tex') == tex_inputs(ROOT / 'complete/main.tex'),
         'Historical mathematical input order changed')
    a = old_main.index('\\subsection*{Acknowledgments}')
    b = old_main.index('\\appendix', a)
    need((ROOT / 'V14_ACKNOWLEDGMENTS_PRESERVED.tex').read_text() == old_main[a:b],
         'Historical acknowledgments not preserved verbatim')
    # Proof-containing main-body bytes outside the relocated acknowledgments
    # remain identical; title/abstract/reading convention are front matter.
    start = '\\input{article/01_introduction}'
    need(old_main[old_main.index(start):a] ==
         new_main[new_main.index(start):new_main.index('\\subsection*{Acknowledgment}')],
         'Companion main mathematical input block changed')
    need(old_main[b:] == new_main[new_main.index('\\appendix'):],
         'Companion appendix sequence changed')
    old16 = (FROZEN / 'article/16_normal_form_comparison.tex').read_text()
    new16 = (ROOT / 'complete/article/16_normal_form_comparison.tex').read_text()
    left = 'For the same physical section at both ends,'
    right = '\\begin{remark}[A nonconstant amplitude with a linear normal form]'
    need(old16[:old16.index(left)] == new16[:new16.index(left)] and
         old16[old16.index(right):] == new16[new16.index(right):],
         'Article 16 changed beyond the chart-convention paragraph')
    old31 = (FROZEN / 'article/31_regular_observability.tex').read_text()
    new31 = (ROOT / 'complete/article/31_regular_observability.tex').read_text()
    replacement = ('All these finitely many probabilities then belong to\n'
                   '$[p_*,1-p_*]$ for some $p_*>0$, after decreasing the collar if\nnecessary.')
    corrected = ('The nodes were chosen inside a common physical collar on which every\n'
                 'selected probability is strictly between zero and one. Continuity on\n'
                 'the now fixed compact ball gives a common $p_*>0$ such that all these\n'
                 'probabilities belong to $[p_*,1-p_*]$. No subsequent change of the\n'
                 'nodes or collar is needed.')
    need(old31.count(replacement) == 1 and old31.replace(replacement, corrected) == new31,
         'Article 31 changed beyond the probability-margin correction')
    entries = {'primary': (ROOT, 'main.tex'),
               'complete': (ROOT / 'complete', 'main.tex'),
               'two_collision': (ROOT / 'complete', 'two_collision.tex')}
    closures = {key: dependency_closure(base, name) for key, (base, name) in entries.items()}
    all_sources = set().union(*closures.values())
    manifest = {}
    for path in sorted(all_sources):
        payload = path.read_bytes()
        manifest[path.relative_to(ROOT).as_posix()] = {
            'git_blob': object_hash('blob', payload),
            'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)}
    canonical = json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()
    environments = {}
    for name in ('theorem', 'proposition', 'lemma', 'corollary', 'proof'):
        pattern = re.compile(r'\\begin\{' + name + r'\}')
        environments[name] = sum(len(pattern.findall(p.read_text())) for p in closures['complete'])
    print(json.dumps({'schema': 'a2-v15-source-preservation-1', 'status': 'passed',
        'frozen_native_v14_tree': actual_tree, 'inherited_files_preserved': len(prior_files),
        'unchanged_inherited_files': len(prior_files) - len(changed),
        'declared_direct_source_edits': sorted(changed),
        'retained_top_level_inputs': len(tex_inputs(FROZEN / 'main.tex')),
        'dependency_files': {k: len(v) for k, v in closures.items()},
        'companion_environments': environments,
        'mathematical_source_manifest_sha256': hashlib.sha256(canonical).hexdigest(),
        'source_manifest': manifest, 'formal_proof_certificate': False}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
