#!/usr/bin/env python3
"""Compare every page with the v36 PDFs; allow only the main edition date.

Requires PyMuPDF. This checks output equivalence, not mathematical correctness.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import fitz


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(baseline: Path, current: Path) -> dict:
    result = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'renderer': 'MuPDF '+fitz.VersionBind, 'raster_comparison_scale': 1.0,
        'scope': 'Every page; native text and RGB pixels at 72 dpi', 'volumes': {}}
    for stem in ('main', 'companions'):
        old_path, new_path = baseline/(stem+'.pdf'), current/(stem+'.pdf')
        with fitz.open(old_path) as old, fitz.open(new_path) as new:
            if len(old) != len(new):
                raise RuntimeError('Changed page count: '+stem)
            text_changes, pixel_changes = [], []
            for i in range(len(old)):
                before, after = old[i].get_text(), new[i].get_text()
                if before != after:
                    text_changes.append(i+1)
                expected = before.replace('September 8, 2026', 'September 9, 2026') if stem == 'main' and i == 0 else before
                if expected != after:
                    raise RuntimeError(f'Unexpected text change: {stem} page {i+1}')
                p = old[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
                q = new[i].get_pixmap(matrix=fitz.Matrix(1,1), alpha=False)
                if (p.width,p.height,p.samples) != (q.width,q.height,q.samples):
                    pixel_changes.append(i+1)
            expected_changes = [1] if stem == 'main' else []
            if pixel_changes != expected_changes:
                raise RuntimeError(f'Unexpected raster change: {stem}, {pixel_changes}')
            result['volumes'][stem] = {'pages': len(new),
                'baseline_pdf_sha256': digest(old_path), 'pdf_sha256': digest(new_path),
                'pages_with_text_changes': text_changes, 'pages_with_pixel_changes': pixel_changes,
                'all_other_pages_text_and_pixel_identical': True}
    result['status'] = 'PASS'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--current', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(compare(args.baseline.resolve(), args.current.resolve()), indent=2))
