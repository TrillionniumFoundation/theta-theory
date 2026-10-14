#!/usr/bin/env python3
"""Fail on unresolved TeX references, duplicate labels, or overfull boxes."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

P = Path(__file__).resolve().parents[1]
text = (P / 'build/main.log').read_text(errors='replace')
patterns = [r'LaTeX Warning:.*undefined', r'Reference .* undefined',
            r'Citation .* undefined', r'There were undefined references',
            r'Label .* multiply defined', r'There were multiply-defined labels',
            r'Overfull \\[hv]box', r'Rerun to get', r'Please rerun', r'^! ']
issues = [pattern for pattern in patterns if re.search(pattern, text, re.M)]
if issues:
    raise RuntimeError('TeX diagnostics: ' + repr(issues))
info = subprocess.check_output(['pdfinfo', str(P / 'build/main.pdf')], text=True)
match = re.search(r'^Pages:\s+(\d+)', info, re.M)
if not match:
    raise RuntimeError('pdfinfo page count missing')
print(json.dumps(dict(status='passed', pages=int(match.group(1)), unresolved_references=0,
                      multiply_defined_labels=0, overfull_boxes=0,
                      pdf_sha256=hashlib.sha256((P / 'build/main.pdf').read_bytes()).hexdigest(),
                      scope='typesetting only; not mathematical correctness'), indent=2, sort_keys=True))
