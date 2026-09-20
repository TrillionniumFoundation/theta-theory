#!/usr/bin/env python3
"""Source-bound native A2 v104 build, including an exact v103 source replay.

The v103 source is compiled in a detached worktree at its actual trigger SHA.
Only after its successful receipt do we reuse its four byte-verified native PDFs.
All v104 targets are then compiled from the current pinned commit. A composite
receipt is emitted only after both stages and all source/log checks succeed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
REVIEW = 'f38495b78e52496d78b44cb5d461fbec65ff530b'
V103_SOURCE = '618b0b098654f53e61a782138272349df92d16ad'
SUFFIXES = ('', '_supporting', '_archive', '_complete')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8')


def run(argv: list[str], cwd: Path, log: Path) -> None:
    with log.open('w', encoding='utf-8') as output:
        subprocess.run(argv, cwd=cwd, stdout=output, stderr=subprocess.STDOUT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'revisions/a2-v104/native')
    args = parser.parse_args()
    output = args.output.resolve()
    allowed = (ROOT/'revisions/a2-v104').resolve()
    if output == allowed or not output.is_relative_to(allowed):
        raise ValueError('Output must be a child of revisions/a2-v104')
    head = git('rev-parse', 'HEAD')
    changes = git('diff', '--name-status', REVIEW, head).splitlines()
    if any(not line.startswith('A\t') for line in changes):
        raise RuntimeError('Inherited path modified; addition-only preservation failed')
    own = [Path(__file__), ROOT/'scripts/check_a2_v104.py', ROOT/'.github/workflows/a2-v104.yml',
           PAPER/'article/v104/paper.tex', *sorted((PAPER/'article/v104/parts').glob('*.tex')), *[PAPER/f'rigidity_v104{s}.tex' for s in SUFFIXES]]
    sources = {}

    def bind(path: Path, expected_sha256: str | None = None) -> None:
        path = path.resolve()
        relative = path.relative_to(ROOT).as_posix()
        committed = subprocess.check_output(['git', 'show', f'{head}:{relative}'], cwd=ROOT)
        if path.read_bytes() != committed:
            raise RuntimeError(f'Input differs from pinned commit: {relative}')
        digest = sha(path)
        if expected_sha256 is not None and digest != expected_sha256:
            raise RuntimeError(f'Inherited replay source changed: {relative}')
        sources[relative] = digest

    for path in own:
        bind(path)
    plan = {'source_head': head, 'source_tree': git('rev-parse', 'HEAD^{tree}'),
            'review_base': REVIEW, 'v103_exact_replay_head': V103_SOURCE,
            'preservation': 'addition-only relative to controlling v103 review',
            'changes': changes, 'source_sha256': sources,
            'steps': ['compile current principal', 'run exact v103 native builder at its trigger commit',
                      'verify inherited source identity and all replay outputs',
                      'reuse only replay-receipted PDFs', 'compile all four current targets',
                      'emit composite native receipt']}
    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    write(output/'BUILD_PLAN.json', plan)
    run([sys.executable, str(ROOT/'scripts/check_a2_v104.py'), '--output',
         str(output/'EXACT_DIAGNOSTICS.json')], ROOT, output/'exact-console.log')

    def compile_target(name: str) -> None:
        run(['latexmk', '-pdf', '-g', '-interaction=nonstopmode', '-halt-on-error',
             '-file-line-error', '-recorder', name+'.tex'], PAPER, output/(name+'-console.log'))
        logfile = PAPER/(name+'.log')
        text = logfile.read_text(errors='replace')
        if any(token in text for token in ('LaTeX Error:', 'There were undefined references', 'multiply defined')):
            raise RuntimeError(f'Unresolved native log: {name}')
        if re.search(r'(?:Reference|Citation)\s+[^\n]+undefined', text):
            raise RuntimeError(f'Unresolved reference/citation: {name}')
        if name == 'rigidity_v104' and any(token in text for token in ('Overfull \\', 'Underfull \\')):
            raise RuntimeError('Principal typography requires inspection')
        if not (PAPER/(name+'.pdf')).is_file():
            raise RuntimeError(f'Missing native PDF: {name}')
        for ext in ('.pdf', '.log', '.fls', '.aux', '.out', '.toc'):
            path = PAPER/(name+ext)
            if path.is_file():
                shutil.copy2(path, output/path.name)

    compile_target('rigidity_v104')
    temp = Path(tempfile.mkdtemp(prefix='a2-v103-replay-'))
    worktree = temp/'source'
    replay_outputs = {}
    try:
        subprocess.run(['git', 'worktree', 'add', '--detach', str(worktree), V103_SOURCE],
                       cwd=ROOT, check=True)
        run([sys.executable, 'scripts/build_a2_v103.py'], worktree, output/'v103-replay-console.log')
        oldout = worktree/'revisions/a2-v103/native'
        receipt = json.loads((oldout/'RUNTIME_RECEIPT.json').read_text())
        if receipt['status'] != 'native_passed' or receipt['source_head'] != V103_SOURCE:
            raise RuntimeError('v103 replay receipt does not bind the exact source')
        for relative, digest in receipt['source_sha256'].items():
            bind(ROOT/relative, digest)
        for relative, metadata in receipt['outputs'].items():
            if sha(oldout/relative) != metadata['sha256']:
                raise RuntimeError(f'Replay artifact hash mismatch: {relative}')
        shutil.copytree(oldout, output/'v103-exact-replay')
        for suffix in SUFFIXES:
            name = f'rigidity_v103{suffix}.pdf'
            src = oldout/name
            if name not in receipt['outputs']:
                raise RuntimeError(f'Unreceipted cache PDF: {name}')
            shutil.copy2(src, PAPER/name)
            replay_outputs[name] = sha(src)
        plan['v103_receipt_sha256'] = sha(oldout/'RUNTIME_RECEIPT.json')
    finally:
        if worktree.exists():
            subprocess.run(['git', 'worktree', 'remove', '--force', str(worktree)], cwd=ROOT, check=True)
        shutil.rmtree(temp, ignore_errors=True)

    for suffix in SUFFIXES[1:]:
        compile_target(f'rigidity_v104{suffix}')
    generated = {f'rigidity_v104{s}.pdf' for s in SUFFIXES}
    generated_suffixes = {'.aux', '.out', '.toc', '.bbl', '.blg', '.log', '.fls', '.fdb_latexmk'}
    for suffix in SUFFIXES:
        recorder = PAPER/f'rigidity_v104{suffix}.fls'
        for line in recorder.read_text(errors='replace').splitlines():
            if not line.startswith('INPUT '):
                continue
            path = Path(line[6:])
            path = (PAPER/path).resolve() if not path.is_absolute() else path.resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                continue
            if path.parent == PAPER and path.name in replay_outputs:
                if sha(path) != replay_outputs[path.name]:
                    raise RuntimeError('Cached replay PDF changed during build')
            elif path.parent == PAPER and path.name in generated:
                continue
            elif path.suffix not in generated_suffixes:
                bind(path)
    for relative, digest in sources.items():
        if sha(ROOT/relative) != digest:
            raise RuntimeError(f'Source changed during build: {relative}')
    plan['reused_native_pdf_sha256'] = replay_outputs
    plan['v104_native_targets'] = [f'rigidity_v104{s}.tex' for s in SUFFIXES]
    write(output/'BUILD_PLAN.json', plan)
    artifacts = {p.relative_to(output).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
                 for p in sorted(output.rglob('*')) if p.is_file()}
    record = {**plan, 'status': 'native_passed', 'outputs': artifacts,
              'pdflatex': subprocess.check_output(['pdflatex','--version'], text=True).splitlines()[0],
              'python': sys.version, 'github_run_id': os.environ.get('GITHUB_RUN_ID'),
              'scope': 'Exact v103 source-native full graph replay plus all four v104 native volumes; inherited inputs and reused native PDFs verified by SHA256. Finite diagnostics are not proof verification.',
              'receipt_commit_convention': 'Compiled source head above; a later artifact-only commit is not asserted to compile its own hash.'}
    write(output/'RUNTIME_RECEIPT.json', record)
    print(json.dumps({'status': 'native_passed', 'source_head': head, 'output': str(output)}))


if __name__ == '__main__':
    main()
