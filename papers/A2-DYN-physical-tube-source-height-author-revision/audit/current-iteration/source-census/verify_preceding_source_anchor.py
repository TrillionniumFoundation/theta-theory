#!/usr/bin/env python3
"""Exercise the added preceding-author anchor using a small private fixture.

The actual article is read only. Source mutations occur only in the temporary
74-file fixture. These are preservation-gate checks, not mathematical tests.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--article', type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.article.resolve()
    spec = importlib.util.spec_from_file_location('source_manifest_gate', root / 'tools/package_source_manifest.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    complete_history = helper.verify_history(root)
    anchor_data = (root / helper.GLOBAL_MINIMIZER_ANCHOR_PATH).read_bytes()
    anchor = json.loads(anchor_data)
    checks = [{'case': 'all_actual_legacy_and_preceding_sources', 'accepted': True}]
    with tempfile.TemporaryDirectory(prefix='a2dyn-anchor-') as temporary:
        fixture = Path(temporary)
        ap = fixture / helper.GLOBAL_MINIMIZER_ANCHOR_PATH
        ap.parent.mkdir(parents=True, exist_ok=True)
        ap.write_bytes(anchor_data)
        for group in anchor['groups'].values():
            for row in group['files']:
                target = fixture / row['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / row['path'], target)
        helper.verify_global_minimizer_history(fixture)
        checks.append({'case': 'exact_74_file_fixture', 'accepted': True})

        def must_reject(case):
            try:
                helper.verify_global_minimizer_history(fixture)
            except helper.VerificationError as error:
                checks.append({'case': case, 'rejected': True, 'diagnostic': str(error)})
            else:
                raise RuntimeError('Preservation mutation was accepted: ' + case)

        row = next(row for row in anchor['groups']['active_inherited_core_260_309']['files'] if row['path'].startswith('core/308_'))
        target = fixture / row['path']
        raw = target.read_bytes()
        target.write_bytes(raw + b'\n% altered prior proof\n')
        must_reject('changed_prior_core_308')
        target.write_bytes(raw)

        target = fixture / 'model.tex'
        raw = target.read_bytes()
        target.unlink()
        must_reject('missing_original_physical_model')
        target.write_bytes(raw)

        ap.write_bytes(anchor_data + b'\n')
        must_reject('changed_pinned_anchor_cannot_be_refrozen')
        ap.write_bytes(anchor_data)
        helper.verify_global_minimizer_history(fixture)
        checks.append({'case': 'restored_exact_fixture', 'accepted': True})
    print(json.dumps({'scope': 'Native-source preservation gate only', 'optimized_python': not __debug__,
                      'legacy_anchor_sha256': complete_history['anchor_sha256'],
                      'preceding_anchor_sha256': complete_history['preceding_author_native']['anchor_sha256'],
                      'checks': checks, 'passed': True}, indent=2))


if __name__ == '__main__':
    main()
