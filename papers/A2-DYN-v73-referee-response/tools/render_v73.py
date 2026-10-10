#!/usr/bin/env python3
"""Record actual TeX inputs, page geometry and deterministic preview pages."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess
from html.parser import HTMLParser

P = Path(__file__).resolve().parents[1]
B = P/'build'
E = P/'evidence'
E.mkdir(exist_ok=True)

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

pdf = B/'main.pdf'
info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
match = re.search(r'^Pages:\s+(\d+)', info, re.M)
require(match is not None, 'PDF page count absent')
total = int(match.group(1))
aux = (B/'main.aux').read_text()
label = re.search(r'\\newlabel\{end:v73-new-mathematics\}\{\{[^}]*\}\{(\d+)\}', aux)
require(label is not None, 'new mathematics end label absent')
last_new = int(label.group(1))
require(1 <= last_new <= min(total, 40), 'unexpected new proof route length')
loaded = set()
for line in (B/'main.fls').read_text().splitlines():
    if line.startswith('INPUT '):
        path = Path(line[6:])
        path = (path if path.is_absolute() else P/path).resolve()
        if path.parent == (P/'core').resolve() and path.suffix == '.tex':
            loaded.add(path.name)
expected = {x.name for x in (P/'core').glob('*.tex')}
require(loaded == expected and len(loaded) == 163, 'not all retained proofs were actually compiled')

bbox = E/'main-bbox.html'
subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
class BoxParser(HTMLParser):
    # Poppler's mathematical glyph text can contain XML-1.0-forbidden
    # control characters. Parse the HTML geometry, not the glyph payload;
    # preserve the raw bbox output and validate every page and word box.
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page = None
        self.page_count = 0
        self.word_count = 0

    def handle_starttag(self, tag, attrs) -> None:
        a = dict(attrs)
        if tag == 'page':
            require(self.page is None, 'nested geometry page')
            self.page = (float(a['width']), float(a['height']))
            self.page_count += 1
        elif tag == 'word':
            require(self.page is not None, 'word outside geometry page')
            width, height = self.page
            x0, y0, x1, y1 = (float(a[k.lower()]) for k in ('xMin','yMin','xMax','yMax'))
            require(-1 <= x0 <= x1 <= width+1 and -1 <= y0 <= y1 <= height+1,
                    'text outside physical page')
            self.word_count += 1

    def handle_endtag(self, tag) -> None:
        if tag == 'page':
            require(self.page is not None, 'unmatched geometry page end')
            self.page = None

parser = BoxParser()
parser.feed(bbox.read_text())
parser.close()
require(parser.page is None and parser.page_count == total, 'incomplete PDF geometry')
require(parser.word_count > 0, 'no PDF word boxes')
word_count = parser.word_count
pages = sorted(set(range(1,last_new+1)) | {total})
for page in pages:
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1400','-png','-singlefile',
                    str(pdf),str(E/f'preview-{page:04d}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
record = {'scope':'native rendering, recorder and page-geometry checks; not mathematical certification',
          'checkout_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),
          'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(), 'pages':total,
          'new_mathematics_ends_on_page':last_new,'preview_pages':pages,
          'compiled_core_count':len(loaded),'compiled_core_files':sorted(loaded),
          'page_bounded_word_boxes':word_count,'formal_proof_certificate':False,'independent_human_review':False}
(E/'v73-render-and-recorder.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps(record,indent=2,sort_keys=True))
