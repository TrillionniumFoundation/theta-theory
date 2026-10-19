#!/usr/bin/env python3
"""Render the actual final native PDF and record mechanical layout observations."""
from pathlib import Path
import datetime
import hashlib
import json
import fitz
from PIL import Image, ImageDraw

ROOT = Path('/workspace/scratch/b5cc344d4c8e/theta-theory/papers/A2-DYN-marked-boundary-source-author-revision')
OUT = ROOT / 'evidence/current-execution/marked-boundary-source-final-precision'
VIS = OUT / 'visual'
VIS.mkdir(parents=True, exist_ok=True)
pdf = OUT / 'native/main.pdf'
native = json.loads((OUT / 'native-typeset.json').read_text())
index = json.loads((ROOT / 'PROOF_INDEX.json').read_text())
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == native['pdf_sha256']
doc = fitz.open(pdf)
assert len(doc) == native['pages'] == index['evidence']['pdf']['page_count']
new_paths = {x['source_file'] for x in index['new_modules']}
new_pages = [x['pdf_page'] for x in index['labels'] if x['source_file'] in new_paths]
selected = sorted(set(range(1, 7)) | set(range(min(new_pages), max(new_pages)+3)) | {len(doc)})
outside = []
span_count = 0
for number, page in enumerate(doc, 1):
    rect = page.rect
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                if not span['text'].strip():
                    continue
                span_count += 1
                x0, y0, x1, y1 = span['bbox']
                if min(x0, y0) < -0.5 or x1 > rect.width+0.5 or y1 > rect.height+0.5:
                    outside.append({'page': number, 'bbox': list(span['bbox']), 'text': span['text']})
images = []
for number in selected:
    target = VIS / f'page-{number:03d}.png'
    doc[number-1].get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False).save(target)
    data = target.read_bytes()
    images.append({'page': number, 'file': target.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
sheets = []
for offset in range(0, len(images), 6):
    group = images[offset:offset+6]
    sheet = Image.new('RGB', (1300, 1815), 'white')
    draw = ImageDraw.Draw(sheet)
    for k, row in enumerate(group):
        im = Image.open(VIS/row['file']).convert('RGB')
        im.thumbnail((625, 560))
        x, y = (k % 2)*650 + 12, (k // 2)*605 + 28
        sheet.paste(im, (x, y))
        draw.text((x, y-20), f'Actual final PDF page {row["page"]}', fill='black')
    target = VIS/f'contact-{offset//6+1:02d}.png'
    sheet.save(target)
    data = target.read_bytes()
    sheets.append({'file': target.name, 'pages': [x['page'] for x in group], 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
receipt = {
    'executed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'pdf_sha256': native['pdf_sha256'], 'pages': len(doc),
    'mathematical_source_sha256': native['mathematical_source']['sha256'],
    'text_spans_checked': span_count, 'outside_page_text_spans': outside,
    'selected_actual_pages': selected, 'images': images, 'contact_sheets': sheets,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Actual PDF rendering and all-page text-bound checks. Visual inspection is recorded separately after viewing. No theorem certificate.',
    'status': 'passed' if not outside else 'requires_inspection',
}
(VIS/'RENDER_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k: receipt[k] for k in ['status', 'pages', 'pdf_sha256', 'text_spans_checked', 'outside_page_text_spans', 'selected_actual_pages']}))
