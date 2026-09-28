#!/usr/bin/env python3
"""Check selected-source provenance and active proof preservation; not a proof checker."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def flatten(path: Path, trail: tuple[Path, ...] = ()) -> tuple[str, set[Path]]:
    path = path.resolve()
    if not path.is_relative_to(ROOT) or path in trail:
        raise ValueError(f"unsafe or cyclic TeX input: {path}")
    text = path.read_text(encoding="utf-8")
    files = {path}
    def expand(match: re.Match[str]) -> str:
        name = match.group(1)
        target = ROOT / (name if name.endswith('.tex') else name + '.tex')
        body, dependencies = flatten(target, trail + (path,))
        files.update(dependencies)
        return body
    return re.sub(r'\\input\{([^}]+)\}', expand, text), files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT/'SOURCE_PRESERVATION_V79.json').read_text())
    errors: list[str] = []
    blobs = {}
    for name, specification in manifest['original_files'].items():
        data = (ROOT/name).read_bytes()
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        blobs[name] = digest
        if digest != specification['expected_git_blob']:
            errors.append(f"upstream blob mismatch: {name}")
    old, old_files = flatten(ROOT/'rigidity_v78.tex')
    new, new_files = flatten(ROOT/'rigidity_v79.tex')
    proof_pattern = r'\\begin\{proof\}(.*?)\\end\{proof\}'
    old_proofs = re.findall(proof_pattern, old, re.S)
    new_proofs = re.findall(proof_pattern, new, re.S)
    retained = sum(body in new_proofs for body in old_proofs)
    if retained != len(old_proofs):
        errors.append('original active proof body missing or changed')
    labels = re.findall(r'\\label\{([^}]+)\}', new)
    old_labels = set(re.findall(r'\\label\{([^}]+)\}', old))
    missing = sorted(old_labels-set(labels))
    duplicates = sorted({label for label in labels if labels.count(label)>1})
    refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', new)
    unresolved = sorted(set(refs)-set(labels))
    if missing or duplicates or unresolved:
        errors.append('label preservation, uniqueness or reference closure failed')
    bib = set(re.findall(r'\\bibitem\{([^}]+)\}', new))
    old_bib = set(re.findall(r'\\bibitem\{([^}]+)\}', old))
    cites = {key.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', new)
             for key in group.split(',')}
    if not old_bib <= bib or not cites <= bib:
        errors.append('bibliography preservation or citation closure failed')
    report = {
        'kind': 'source_integrity_not_mathematical_certification',
        'status': 'PASS' if not errors else 'FAIL',
        'pinned_review_commit': manifest['base_commit'],
        'scope': manifest['source_scope'],
        'original_blob_count': len(blobs), 'git_blobs': blobs,
        'original_proof_bodies': len(old_proofs), 'retained_original_proof_bodies': retained,
        'new_proof_bodies': len(new_proofs),
        'original_label_count': len(old_labels), 'new_label_count': len(labels),
        'missing_original_labels': missing, 'duplicate_labels': duplicates,
        'unresolved_references': unresolved,
        'bibliography_keys': sorted(bib),
        'active_v79_files': sorted(str(path.relative_to(ROOT)) for path in new_files),
        'errors': errors,
    }
    text = json.dumps(report, indent=2) + '\n'
    print(text, end='')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
