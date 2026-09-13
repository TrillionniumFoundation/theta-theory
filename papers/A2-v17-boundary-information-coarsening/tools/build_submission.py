#!/usr/bin/env python3
"""Build both unabridged native A2 entries from an immutable Git snapshot.

A passing build is not a mathematical correctness or visual-inspection
certificate. All available logs and input manifests are retained on failure.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from source_provenance import (PRODUCT_SUFFIXES, freeze_git_source, graph,
                               recorder_inputs, require, sha256, source_archive,
                               tex_roots, verify_copy, verify_generated, write_json)

SOURCE = Path(__file__).resolve().parents[1]
ENTRIES = ('two_collision', 'main')
DIAGNOSTICS = ('check_adaptive.py', 'check_revision_v32.py', 'check_revision_v38.py')


def run(cmd: list[str], cwd: Path, env: dict[str, str], output: Path) -> int:
    with output.open('wb') as stream:
        return subprocess.run(cmd, cwd=cwd, env=env, stdout=stream,
                              stderr=subprocess.STDOUT, check=False).returncode


def build_entry(stem: str, work: Path, out: Path, env: dict[str, str],
                files: dict, expected: set[str], external_roots: list[Path],
                imported_generated: dict | None = None) -> dict:
    result = {'status': 'started', 'entry': stem + '.tex',
              'layout_review': 'not performed by this script'}
    # -norc excludes user/project latexmk configuration; -recorder is explicit.
    cmd = ['latexmk', '-norc', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
           '-file-line-error', '-recorder',
           '-pdflatex=pdflatex -no-shell-escape -recorder %O %S', stem + '.tex']
    result['command'] = cmd
    try:
        verify_copy(work, files)
        verify_generated(work, imported_generated or {})
        require(stem + '.tex' in files and stem + '.tex' in expected, 'Unmanifested native entry')
        code = run(cmd, work, env, out / (stem + '-build.txt'))
        result['returncode'] = code
        require(code == 0, 'latexmk failed; available logs are preserved')
        log_file = work / (stem + '.log')
        require(log_file.is_file() and log_file.stat().st_size > 0, 'Missing or empty TeX log')
        log = log_file.read_text(errors='replace')
        flat = ''.join(log.splitlines())
        fatal = re.search(r'undefined references|undefined citations|'
                          r'(?:Reference|Citation) `.{0,250}?undefined|'
                          r'multiply[- ]defined|Missing character:|'
                          r'destination with the same identifier', flat, re.I)
        result['warnings'] = re.findall(r'.*(?:Warning:|Overfull \\[hv]box|Underfull \\[hv]box).*', log)
        require(fatal is None, 'Unresolved reference/citation, duplicate destination/label, or missing glyph')
        # Fail before issuing a successful product certificate if provenance is absent.
        recorded = recorder_inputs(stem, work, files, expected, external_roots, imported_generated)
        write_json(out / (stem + '-recorder-inputs.json'), recorded)
        result['source_integrity'] = 'verified'
        result['recorded_native_files'] = len(recorded['source_inputs'])
        pdf = work / (stem + '.pdf')
        require(pdf.is_file() and pdf.read_bytes().startswith(b'%PDF-'), 'Missing native PDF')
        cp = subprocess.run(['pdfinfo', str(pdf)], env=env, capture_output=True, text=True, check=False)
        (out / (stem + '-pdfinfo.txt')).write_text(cp.stdout + cp.stderr)
        require(cp.returncode == 0, 'pdfinfo failed')
        pages = re.search(r'^Pages:\s*(\d+)', cp.stdout, re.M)
        require(pages is not None and int(pages.group(1)) > 0, 'Invalid native PDF page count')
        result['product'] = {'pages': int(pages.group(1)), 'bytes': pdf.stat().st_size,
                             'sha256': sha256(pdf)}
        result['status'] = 'passed'
    except Exception as exc:
        result['status'] = 'failed'
        result['error'] = str(exc)
    finally:
        for suffix in PRODUCT_SUFFIXES:
            path = work / (stem + suffix)
            if path.is_file():
                shutil.copy2(path, out / path.name)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    require(out != SOURCE and SOURCE not in out.parents, 'Output must be outside the manuscript tree')
    require(not out.exists() or not any(out.iterdir()), 'Output directory must be absent or empty')
    out.mkdir(parents=True, exist_ok=True)
    report = {'status': 'started', 'entrypoints': [s + '.tex' for s in ENTRIES],
              'scope': 'Both complete native entries, including every recursive input and bibliography',
              'source_commit': None, 'errors': [], 'entries': {}, 'finite_diagnostics': {},
              'python_version': sys.version, 'python_executable': sys.executable,
              'visual_inspection': 'not performed; required separately for C2',
              'trust_boundary': 'Git and installed TeX toolchain; not hostile-compiler attestation'}
    try:
        with tempfile.TemporaryDirectory(prefix='a2-source-pinned-') as temporary:
            temporary = Path(temporary)
            snapshot = temporary / 'snapshot'
            manifest = freeze_git_source(SOURCE, snapshot, ENTRIES)
            write_json(out / 'frozen-source-manifest.json', manifest)
            source_archive(snapshot, manifest, out / 'native-source.zip')
            report.update({key: manifest[key] for key in
                           ('source_commit', 'source_tree', 'repository_tree', 'source_prefix', 'working_tree')})
            report['source_archive_sha256'] = sha256(out / 'native-source.zip')
            expected = {stem: graph(snapshot, stem + '.tex') for stem in ENTRIES}
            write_json(out / 'active-source-manifest.json', {
                stem: {name: manifest['files'][name] for name in sorted(expected[stem])} for stem in ENTRIES})
            report['active_tex_files'] = len(set().union(*expected.values()))
            # Do not inherit TeX search-path overrides or mutable user configuration.
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(('TEX', 'BIB', 'BST', 'VARTEX', 'LATEXMK'))}
            home = temporary / 'empty-home'
            home.mkdir()
            env.update({'HOME': str(home), 'TEXMFHOME': str(home / 'texmf'),
                        'SOURCE_DATE_EPOCH': '1789257600', 'FORCE_SOURCE_DATE': '1',
                        'TZ': 'UTC', 'LC_ALL': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'})
            for tool in ('git', 'latexmk', 'pdflatex', 'pdfinfo', 'kpsewhich'):
                require(shutil.which(tool) is not None, 'Required executable unavailable: ' + tool)
                cp = subprocess.run([tool, '-v' if tool == 'pdfinfo' else '--version'],
                                    env=env, capture_output=True, text=True, check=False)
                (out / (tool + '-version.txt')).write_text(cp.stdout + cp.stderr)
                require(cp.returncode == 0, 'Could not record version of ' + tool)
            roots = tex_roots(env)
            report['external_tex_roots'] = [str(root) for root in roots]
            for script in DIAGNOSTICS:
                results = []
                for opt, mode in (([], 'normal'), (['-O'], 'optimized')):
                    target = out / (Path(script).stem + '-' + mode + '.json')
                    code = run([sys.executable, '-B', *opt, str(snapshot / 'tools' / script)], snapshot, env, target)
                    results.append(target)
                    if code:
                        report['errors'].append(script + ' ' + mode + ' failed; see ' + target.name)
                if results[0].read_bytes() != results[1].read_bytes():
                    report['errors'].append(script + ': normal/optimized outputs differ')
                try:
                    report['finite_diagnostics'][script] = json.loads(results[0].read_text())
                except (ValueError, UnicodeError):
                    report['errors'].append(script + ': diagnostic output is not JSON')
            for stem in ENTRIES:
                work = temporary / ('compile-' + stem)
                shutil.copytree(snapshot, work)
                imported = {}
                if stem == 'main':
                    companion = report['entries'].get('two_collision', {})
                    require(companion.get('status') == 'passed',
                            'A source-verified companion build is required before the main')
                    aux = out / 'two_collision.aux'
                    require(aux.is_file(), 'Companion auxiliary output is missing')
                    shutil.copy2(aux, work / aux.name)
                    imported[aux.name] = {
                        'bytes': aux.stat().st_size, 'sha256': sha256(aux),
                        'producer_entry': 'two_collision.tex',
                        'producer_source_commit': manifest['source_commit'],
                        'producer_pdf_sha256': companion['product']['sha256'],
                        'producer_recorder_sha256': sha256(out/'two_collision-recorder-inputs.json')}
                    write_json(out/'main-imported-generated-inputs.json', imported)
                report['entries'][stem] = build_entry(stem, work, out, env,
                                                     manifest['files'], expected[stem], roots, imported)
                if report['entries'][stem]['status'] != 'passed':
                    report['errors'].append(stem + ': ' + report['entries'][stem]['error'])
            report['status'] = 'failed' if report['errors'] else 'passed'
    except Exception as exc:
        report['status'] = 'failed'
        report['errors'].append(str(exc))
    finally:
        report['evidence_files'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha256(p)}
                                    for p in sorted(out.iterdir()) if p.is_file() and p.name != 'build-report.json'}
        write_json(out / 'build-report.json', report)
    print(json.dumps(report, indent=2, sort_keys=True))
    if report['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
