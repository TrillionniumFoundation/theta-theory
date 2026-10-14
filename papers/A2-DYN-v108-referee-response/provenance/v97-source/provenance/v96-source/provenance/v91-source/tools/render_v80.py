#!/usr/bin/env python3
"""PDF page geometry and recorder coverage, not mathematical certification."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from check_v77 import require

PAPER = Path(__file__).resolve().parents[1]
BUILD, EVIDENCE = PAPER / 'build', PAPER / 'evidence'


def inspect(name: str) -> dict:
    pdf, bbox = BUILD / (name + '.pdf'), EVIDENCE / (name + '-bbox.html')
    subprocess.run(['pdftotext', '-bbox', str(pdf), str(bbox)], check=True)
    cleaned = ''.join(c for c in bbox.read_text() if ord(c) >= 32 or c in '\n\r\t')
    doc = ET.fromstring(cleaned)
    pages = [e for e in doc.iter() if e.tag.endswith('}page') or e.tag == 'page']
    require(bool(pages), 'empty PDF')
    words = 0
    for number, page in enumerate(pages, 1):
        width, height = float(page.attrib['width']), float(page.attrib['height'])
        for item in page.iter():
            if not (item.tag.endswith('}word') or item.tag == 'word'):
                continue
            x0, y0, x1, y1 = [float(item.attrib[k]) for k in ('xMin', 'yMin', 'xMax', 'yMax')]
            require(all(math.isfinite(x) for x in (x0, y0, x1, y1)), 'nonfinite PDF box')
            require(-.5 <= x0 <= x1 <= width + .5 and -.5 <= y0 <= y1 <= height + .5,
                    f'{name} page {number}: text outside page')
            words += 1
    inputs = set()
    for line in (BUILD / (name + '.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            match = re.search(r'(?:^|/)core/([^/]+\.tex)$', line[6:])
            if match:
                inputs.add(match.group(1))
    return {'pages': len(pages), 'words': words, 'core_modules': sorted(inputs),
            'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()}


def main() -> None:
    require(sys.argv[1:] in ([], ['--local']), 'unknown render arguments')
    local = False  # Both modes require the complete supplement.
    names = ('main',) if local else ('main', 'supplement')
    result = {name: inspect(name) for name in names}
    require(len(result['main']['core_modules']) == 8, 'new journal recorder coverage')
    if not local:
        expected = {p.name for p in (PAPER / 'core').glob('*.tex')}
        union = set(result['main']['core_modules']) | set(result['supplement']['core_modules'])
        require(len(expected) == 185 and union == expected, 'complete recorder coverage')
        require(len(result['supplement']['core_modules']) == 182, 'inherited supplement coverage')
    result['scope'] = 'page geometry and actual TeX recorder coverage; no proof certification'
    (EVIDENCE / 'v80-render.json').write_text(json.dumps(result, indent=2) + '\n')
    for name in names:
        numbers = range(1, result[name]['pages'] + 1) if name == 'main' else [1, 2, result[name]['pages']]
        for number in numbers:
            subprocess.run(['pdftoppm', '-f', str(number), '-l', str(number), '-singlefile', '-r', '90', '-png',
                            str(BUILD / (name + '.pdf')), str(EVIDENCE / f'{name}-{number:03d}')],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(json.dumps({name: {'pages': result[name]['pages'], 'cores': len(result[name]['core_modules'])}
                      for name in names}, indent=2))


if __name__ == '__main__':
    main()
