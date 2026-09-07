#!/usr/bin/env python3
"""Materialize and build both v25 volumes without changing the v24 source.

Requires Python 3.10+, the inherited offline builder, and its TeX tools.
Run from any directory: python papers/A1-english-v25/build_v25.py
Use --prepare-only for source, reference and preservation checks without TeX.
This is not a formal proof checker or an independent referee report.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'A1-english-v24'
REVIEW = 'c7fee8b92fd779573bd3b9ccdf5e37183c5cefa6'
SUBMISSION = '6f648bc3da0543e8361b4053ae7da33cb172f597'
BASE_TREE = '79d66f7b4fd132923d28068f283b88f59276ec21'
BASE_MAIN = '3452fde8106234dedc729d12a7c4a92e4bb84030'


def git_blob(data: bytes) -> str:
    header = b'blob ' + str(len(data)).encode('ascii') + b'\0'
    return hashlib.sha1(header + data).hexdigest()


def checked_run(args: list[str], cwd: Path, log: Path) -> None:
    with log.open('w', encoding='utf-8') as stream:
        proc = subprocess.run(args, cwd=cwd, stdout=stream,
                              stderr=subprocess.STDOUT, text=True, check=False)
    if proc.returncode:
        raise RuntimeError('Command failed: ' + repr(args) + '\n' +
                           log.read_text(errors='replace')[-4000:])


def check_baseline() -> dict[str, Any]:
    source = BASE / 'main.tex'
    if not source.is_file():
        raise FileNotFoundError('The pinned sibling papers/A1-english-v24 is required')
    actual = git_blob(source.read_bytes())
    if actual != BASE_MAIN:
        raise ValueError('The reviewed v24 main entry point has changed')
    identity: dict[str, Any] = {'main_git_blob': actual, 'expected_tree': BASE_TREE}
    git = shutil.which('git')
    if git:
        location = subprocess.run([git, 'rev-parse', '--show-toplevel'], cwd=BASE,
                                  capture_output=True, text=True, check=False)
        if location.returncode == 0:
            top = Path(location.stdout.strip()).resolve()
            relative = BASE.resolve().relative_to(top).as_posix()
            tree = subprocess.run([git, 'rev-parse', 'HEAD:' + relative], cwd=top,
                                  capture_output=True, text=True, check=False)
            if tree.returncode == 0:
                if tree.stdout.strip() != BASE_TREE:
                    raise ValueError('The committed v24 dependency tree is not the reviewed native tree')
                dirty = subprocess.run([git, 'diff', '--quiet', 'HEAD', '--', relative],
                                       cwd=top, check=False)
                if dirty.returncode:
                    raise ValueError('The v24 dependency working tree contains changes')
                identity['mode'] = 'native Git tree and tracked working bytes verified'
                return identity
    identity['mode'] = ('offline source package: main blob and inherited source audit; '
                        'no claim of a locally verified native Git tree')
    return identity


def load_builder(stage: Path) -> Any:
    spec = importlib.util.spec_from_file_location('_theta_v24_build', stage / 'build.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the inherited builder')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check_blocks(builder: Any, before: str, after: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    categories = [('statements', builder.FORMAL), ('proofs', ('proof',)),
                  ('definitions_and_remarks', ('definition', 'remark'))]
    for category, environments in categories:
        old = builder.blocks(before, environments)
        new = builder.blocks(after, environments)
        if old - new or any(new[key] != count for key, count in old.items()):
            raise ValueError('An inherited v24 block changed, disappeared or was duplicated: ' + category)
        result[category] = {'preserved_byte_identical': sum(old.values()),
                            'added': sum((new - old).values())}
    old_labels = set(builder.labels(before))
    if old_labels - set(builder.labels(after)):
        raise ValueError('An inherited v24 label disappeared')
    result['inherited_labels_preserved'] = len(old_labels)
    result['scope'] = 'Source-block identity and routing, not mathematical validity.'
    return result


def build(prepare_only: bool) -> dict[str, Any]:
    identity = check_baseline()
    work = ROOT / 'build-v25'
    work.mkdir(exist_ok=True)
    stage = work / 'source'
    # This is an explicitly generated directory inside the new revision only.
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(BASE, stage)
    for name in ('main.pdf', 'companions.pdf'):
        (stage / name).unlink(missing_ok=True)
    helper = stage / 'materialize.py'
    bootstrap = ([sys.executable, str(helper)] if helper.exists() else
                 [sys.executable, str(stage / 'build.py'), '--prepare-only'])
    checked_run(bootstrap, stage, work / 'materialize.log')
    builder = load_builder(stage)
    baseline = builder.expand(stage / 'main.tex') + '\n' + builder.expand(stage / 'companions.tex')
    shutil.copy2(ROOT / 'main.tex', stage / 'main.tex')
    shutil.copytree(ROOT / 'v25', stage / 'v25', dirs_exist_ok=True)
    additions = (stage / 'v25/references.tex').read_text()
    references = stage / 'references-main.tex'
    old_bib = references.read_text()
    key_pattern = r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}'
    old_keys = set(re.findall(key_pattern, old_bib))
    new_keys = re.findall(key_pattern, additions)
    if len(new_keys) != len(set(new_keys)) or old_keys.intersection(new_keys):
        raise ValueError('An additional bibliography key is duplicated')
    end = '\\end{thebibliography}'
    if old_bib.count(end) != 1:
        raise ValueError('Unexpected inherited main bibliography structure')
    references.write_text(old_bib.replace(end, additions + '\n' + end))
    # The unchanged historical writer does not know the new citation keys.
    # Both inherited bibliographies have just been generated and audited;
    # retain them, adding only the two explicit main-volume entries above.
    builder.write_bibliographies = lambda: None
    current = builder.expand(stage / 'main.tex') + '\n' + builder.expand(stage / 'companions.tex')
    preservation = check_blocks(builder, baseline, current)
    legacy = builder.prepare() if prepare_only else builder.build()
    artifacts: dict[str, Any] = {}
    if not prepare_only:
        for name in ('main.pdf', 'companions.pdf'):
            source = stage / name
            if not source.is_file() or source.stat().st_size == 0:
                raise RuntimeError('The builder did not produce ' + name)
            shutil.copy2(source, ROOT / name)
            artifacts[name] = {'bytes': source.stat().st_size,
                               'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
    (ROOT / 'main-expanded-v25.tex').write_text(builder.expand(stage / 'main.tex'))
    (ROOT / 'companions-expanded-v25.tex').write_text(builder.expand(stage / 'companions.tex'))
    source_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [ROOT / 'main.tex', ROOT / 'build_v25.py',
                               *sorted((ROOT / 'v25').rglob('*.tex'))]}
    return {'version': 25, 'status': 'passed', 'build_executed': not prepare_only,
            'controlling_review_commit': REVIEW, 'reviewed_submission_commit': SUBMISSION,
            'baseline_identity': identity, 'v24_preservation': preservation,
            'source_sha256': source_hashes, 'artifacts': artifacts,
            'inherited_builder_receipt': legacy,
            'scope': ('Executed source checks and, when build_executed is true, both LaTeX builds. '
                      'The nested historical source audit retains its original lineage. '
                      'This is not independent peer review, a CI receipt, or a formal proof certificate.')}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    filename = 'PRESERVATION_REPORT_V25.json' if args.prepare_only else 'BUILD_REPORT_V25.json'
    destination = ROOT / filename
    destination.unlink(missing_ok=True)
    try:
        report = build(args.prepare_only)
    except Exception as exc:
        failure = {'version': 25, 'status': 'failed', 'error': str(exc),
                   'scope': 'No successful build is certified by this failure record.'}
        (ROOT / 'BUILD_FAILURE_V25.json').write_text(json.dumps(failure, indent=2) + '\n')
        raise
    destination.write_text(json.dumps(report, indent=2) + '\n')
    (ROOT / 'BUILD_FAILURE_V25.json').unlink(missing_ok=True)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
