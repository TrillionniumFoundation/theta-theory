#!/usr/bin/env python3
"""Build the complete A2 v6 manuscript and retained companion locally."""
from __future__ import annotations
import re
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    if shutil.which('latexmk') is None:
        raise SystemExit('latexmk is required; install a TeX distribution first.')
    # The main article imports labels from two_collision.aux via xr.
    # Build that independent companion first, including on a clean checkout.
    for stem in ('two_collision', 'main'):
        subprocess.run(['latexmk', '-pdf', '-interaction=nonstopmode',
                        '-halt-on-error', f'{stem}.tex'], cwd=root, check=True)
        pdf = root / f'{stem}.pdf'
        if not pdf.is_file() or pdf.stat().st_size == 0:
            raise RuntimeError(f'Missing output: {pdf}')
        log = (root / f'{stem}.log').read_text(errors='replace')
        bad = re.findall(r'^.*(?:LaTeX Warning:|Package .* Warning:|Overfull|'
                         r'Undefined control sequence|multiply defined).*$',
                         log, flags=re.MULTILINE)
        if bad:
            raise RuntimeError(f'{stem}: unresolved build diagnostics:\n' + '\n'.join(bad))
        print(f'OK: {pdf.name} ({pdf.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
