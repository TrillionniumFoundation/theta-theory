#!/usr/bin/env python3
"""Negative controls for the source gate; no TeX or network subprocesses."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('v27_validation', HERE/'validate_v27.py')
if spec is None or spec.loader is None:
    raise RuntimeError('cannot import validation gate')
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)
checks = 0


def require(value: bool) -> None:
    global checks
    if not value:
        raise RuntimeError('validation-contract negative control failed')
    checks += 1


def rejects(call) -> None:
    try:
        call()
    except (RuntimeError, FileNotFoundError, KeyError, ValueError):
        require(True)
    else:
        require(False)


def main() -> None:
    root = HERE.parent
    for missing in ('SOURCE_PINS.json', 'tools/verify_v27.py', 'tools/validate_v27.py',
                    'tools/test_validation_contract.py', 'core/00_fixed_aperture.tex'):
        with tempfile.TemporaryDirectory() as directory:
            stage = Path(directory)
            for name in ('main.tex', 'references.tex', 'SOURCE_PINS.json'):
                shutil.copy2(root/name, stage/name)
            shutil.copytree(root/'core', stage/'core')
            shutil.copytree(root/'tools', stage/'tools', ignore=shutil.ignore_patterns('__pycache__'))
            require(validation.check_sources(stage)['schema'] == 'a2-v27-source-pins-1')
            (stage/missing).unlink()
            rejects(lambda: validation.check_sources(stage))
    with tempfile.TemporaryDirectory() as directory:
        stage = Path(directory)
        for name in ('main.tex', 'references.tex', 'SOURCE_PINS.json'):
            shutil.copy2(root/name, stage/name)
        shutil.copytree(root/'core', stage/'core')
        shutil.copytree(root/'tools', stage/'tools', ignore=shutil.ignore_patterns('__pycache__'))
        with (stage/'core/00_fixed_aperture.tex').open('a') as stream:
            stream.write('% deliberate source corruption\n')
        rejects(lambda: validation.check_sources(stage))
    require(validation.require_expected_commit('a'*40, 'a'*40) is None)
    rejects(lambda: validation.require_expected_commit('a'*40, 'b'*40))
    rejects(lambda: validation.require_expected_commit(None, 'a'*40))
    print(json.dumps({'status': 'passed', 'checks': checks,
        'scope': 'missing-file, source-corruption and exact-commit negative controls',
        'formal_proof_certificate': False}, sort_keys=True))


if __name__ == '__main__':
    main()
