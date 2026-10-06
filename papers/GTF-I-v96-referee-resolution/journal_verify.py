#!/usr/bin/env python3
"""Reconstruct the v96 primary and supplement without repository or historical PDFs."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import fitz

ROOT = Path(__file__).resolve().parent
EPOCH = '1791244800'
DOCS = {'quantitative.tex': 'paper.pdf', 'supplement.tex': 'BINARY_SUPPLEMENT.pdf'}
EXTRAS = {'paper.pdf','BINARY_SUPPLEMENT.pdf','REPRODUCIBILITY.md','JOURNAL_README.md','requirements.txt','journal_verify.py','THEOREM_MAP.md','RESPONSE_TO_REFEREE.md'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def relative(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and name == path.as_posix(),
            'unsafe manifest path: '+name)
    return path


def graph(entry, seen=None):
    if seen is None:
        seen = set()
    entry = relative(str(Path(entry).with_suffix('.tex'))).as_posix()
    require(entry not in seen, 'duplicate or recursive active input: '+entry)
    seen.add(entry)
    text = (ROOT/entry).read_text()
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        graph(name, seen)
    return seen


def signature(path):
    pages = []
    with fitz.open(path) as document:
        for page in document:
            text = page.get_text(sort=True)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            for block in page.get_text('blocks'):
                x0, y0, x1, y1 = block[:4]
                require(x0 >= -1 and y0 >= -1 and x1 <= page.rect.width+1 and y1 <= page.rect.height+1,
                        'clipped text in '+path.name+' page '+str(page.number+1))
            pages.append({'page': page.number+1, 'text_sha256': sha(text.encode()),
                          'raster_sha256': sha(pix.samples), 'width': pix.width,
                          'height': pix.height, 'characters': len(text)})
    return {'pages': len(pages), 'page_checks': pages, 'sha256': sha(path.read_bytes())}


def main():
    manifest_bytes = (ROOT/'JOURNAL_MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest['schema'] == 'gtf96.journal/1'
            and manifest['repository_dependencies'] is False
            and manifest['historical_PDF_dependencies'] is False
            and manifest['source_date_epoch'] == int(EPOCH), 'wrong standalone journal identity')
    require(re.fullmatch(r'[0-9a-f]{40}', manifest['source_commit']) is not None,
            'standalone manifest must identify the qualified native source')
    require(set(manifest['documents']) == set(DOCS.values()), 'the primary and supplement are required')
    for name, digest in manifest['files'].items():
        require(sha((ROOT/relative(name)).read_bytes()) == digest, 'submitted file differs: '+name)
    active = set()
    for entry in DOCS:
        active.update(graph(entry))
    require(set(manifest['files']) == active | EXTRAS,
            'journal inventory differs from the two active source graphs and editorial files')
    for name in DOCS.values():
        require(signature(ROOT/name) == manifest['documents'][name], 'submitted PDF differs: '+name)
    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE='1', TZ='UTC')
    with tempfile.TemporaryDirectory(prefix='gtf96-journal-readonly-') as directory:
        dest = Path(directory)
        for name in sorted(active):
            (dest/name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/name, dest/name)
        (dest/'build').mkdir()
        for cycle in range(4):
            for entry in DOCS:
                run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                      '-file-line-error','-output-directory=build', entry], cwd=dest, env=env,
                                     capture_output=True, timeout=180)
                require(run.returncode == 0, run.stdout.decode(errors='replace')[-6000:])
                if entry in ('quantitative.tex','supplement.tex'):
                    own=set()
                    for name in graph(entry):
                        own.update(re.findall(r'\\label\{([^}]+)\}',(dest/name).read_text()))
                    stem=Path(entry).stem
                    lines=(dest/'build'/(stem+'.aux')).read_text().splitlines()
                    kept=[line for line in lines if (match:=re.match(r'\\newlabel\{([^}]+)\}',line))
                          and match.group(1) in own]
                    (dest/'build'/('xref-'+stem+'.aux')).write_text('\n'.join(kept)+'\n')
        for entry, pdf in DOCS.items():
            stem = Path(entry).stem
            log = (dest/'build'/(stem+'.log')).read_text(errors='replace')
            require(not any(text in log for text in ['There were undefined references',
                    'There were undefined citations', 'multiply defined', 'Undefined control sequence',
                    'Rerun to get cross-references right']), 'unresolved references in '+entry)
            require(not re.findall(r'(?:Overfull|Underfull) \\[^\n]+', log), 'unresolved typesetting boxes in '+entry)
            rebuilt = signature(dest/'build'/(stem+'.pdf'))
            require(rebuilt['page_checks'] == manifest['documents'][pdf]['page_checks'],
                    'standalone rebuilt text or rasters differ: '+pdf)
    for name, digest in manifest['files'].items():
        require(sha((ROOT/name).read_bytes()) == digest, 'verification modified an input: '+name)
    require((ROOT/'JOURNAL_MANIFEST.json').read_bytes() == manifest_bytes, 'verification modified the manifest')
    print(json.dumps({'schema': 'gtf96.journal-rebuild/1', 'status': 'success',
                      'source_commit': manifest['source_commit'], 'source_date_epoch': int(EPOCH),
                      'documents': {name: {'pages': info['pages'], 'sha256': info['sha256']}
                                    for name, info in manifest['documents'].items()},
                      'active_source_files': len(active), 'read_only': True,
                      'independent_proof_certification': False,
                      'quantifier_elimination_learner_executed': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
