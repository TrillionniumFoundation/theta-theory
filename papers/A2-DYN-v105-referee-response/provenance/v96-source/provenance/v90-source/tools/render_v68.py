#!/usr/bin/env python3
"""Render actual theorem pages and record PDF/TeX evidence, not proof certification."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

aux = (ROOT/'build/main.aux').read_text()
labels = ['thm:intro-v68-germs','thm:intro-v68-height','lem:v68-analytic-margins',
          'lem:v68-root-order','thm:v68-angular-germ-classification',
          'thm:v68-relative-radial-profile','prop:v68-annular-comparison',
          'thm:v68-all-order-height','end:v68-new-mathematics',
          'thm:v66-uniform-morse','thm:v66-ordered-collar-trace','app:v68-retained-front']
pages = {1}
locations = {}
for label in labels:
    found = re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^{}]*)\}\{([0-9]+)\}', aux)
    require(found is not None, 'missing theorem page: '+label)
    locations[label] = {'number':found[1], 'page':int(found[2])}
    pages.add(int(found[2]))
pages.update(range(1, locations['end:v68-new-mathematics']['page']+1))
(ROOT/'evidence').mkdir(exist_ok=True)
for page in sorted(pages):
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','100','-png','-singlefile',
                    str(ROOT/'build/main.pdf'),str(ROOT/'evidence'/('page-'+str(page)))], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
info = subprocess.check_output(['pdfinfo',str(ROOT/'build/main.pdf')], text=True)
count = re.search(r'^Pages:\s+(\d+)',info,re.M)
require(count is not None, 'PDF page count')
receipt = {'revision':68,'checkout_sha':os.environ.get('GITHUB_SHA'),
           'ref':os.environ.get('GITHUB_REF'), 'run_id':os.environ.get('GITHUB_RUN_ID'),
           'pdf_pages':int(count[1]),'pdf_sha256':sha(ROOT/'build/main.pdf'),
           'main_tex_sha256':sha(ROOT/'main.tex'),'theorem_locations':locations,
           'rendered_pages':sorted(pages),'continuum_proof_certified':False,
           'independent_human_review':False}
(ROOT/'evidence/build-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
