#!/usr/bin/env python3
"""Read-only Poppler rendering and labeled contact sheets for R76 draft QA."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF_ROOT = ROOT.parent / 'draft02'
FILES = {
    'supplement': 'General_Theta_Foundations_I_R76_Supplement.pdf',
    'companion': 'General_Theta_Foundations_I_R76_Retained_Companion_R58.pdf',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('document', choices=FILES)
    ap.add_argument('--pages', nargs='*', type=int)
    args = ap.parse_args()
    pdf = PDF_ROOT / FILES[args.document]
    reader = PdfReader(pdf)
    out = ROOT / args.document
    out.mkdir(parents=True, exist_ok=True)
    before = digest(pdf)
    if args.pages:
        commands = []
        for page in args.pages:
            prefix = out / f'full-page-{page:03d}'
            cmd = ['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile',
                   '-r', '150', '-png', str(pdf), str(prefix)]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            commands.append(cmd)
        suffix = 'full-resolution-render.json'
        images = [out / f'full-page-{p:03d}.png' for p in args.pages]
        pages = args.pages
    else:
        prefix = out / 'overview-page'
        commands = []
        digits = len(str(len(reader.pages)))
        for first in range(1, len(reader.pages)+1, 12):
            last = min(len(reader.pages), first+11)
            complete = True
            for page in range(first, last+1):
                raster = out / f'overview-page-{page:0{digits}d}.png'
                try:
                    im = Image.open(raster)
                    im.load()
                except (OSError, ValueError):
                    complete = False
                    if raster.exists():
                        raster.unlink()  # only this task's incomplete generated PNG
            if complete:
                continue
            cmd = ['pdftoppm', '-f', str(first), '-l', str(last),
                   '-r', '60', '-png', str(pdf), str(prefix)]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            commands.append(cmd)
        rasters = sorted(out.glob('overview-page-*.png'))
        if len(rasters) != len(reader.pages):
            raise ValueError('Rendered page count does not match the input PDF')
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
        except OSError:
            font = ImageFont.load_default()
        images = []
        for start in range(0, len(rasters), 12):
            chunk = rasters[start:start+12]
            canvas = Image.new('RGB', (1162, 2074), '#dfe3e8')
            draw = ImageDraw.Draw(canvas)
            for j, raster in enumerate(chunk):
                im = Image.open(raster).convert('RGB')
                im.thumbnail((370, 479), Image.Resampling.LANCZOS)
                x = 14 + (j % 3) * 386
                y = 12 + (j // 3) * 516
                draw.text((x, y), f'{args.document} — PDF page {start+j+1}',
                          fill='#111111', font=font)
                canvas.paste(im, (x, y+27))
                draw.rectangle((x-1, y+26, x+im.width, y+27+im.height),
                               outline='#6b7280', width=1)
            target = out / f'contact-{start+1:03d}-{start+len(chunk):03d}.png'
            canvas.save(target)
            images.append(target)
        suffix = 'overview-render.json'
        pages = list(range(1, len(reader.pages)+1))
    after = digest(pdf)
    if before != after:
        raise RuntimeError('Input PDF changed during read-only rendering')
    receipt = {
        'kind': 'render receipt; no visual-view claim',
        'document': args.document,
        'input_path': str(pdf),
        'input_sha256': before,
        'input_pdf_pages': len(reader.pages),
        'rendered_pages': pages,
        'commands': commands,
        'images': [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)} for p in images],
    }
    (out/suffix).write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'document': args.document, 'input_sha256': before,
                      'rendered_page_count': len(pages), 'display_images': len(images)}))


if __name__ == '__main__':
    main()
