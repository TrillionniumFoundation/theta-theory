#!/usr/bin/env python3
"""Record actual source and PDF build results; fail on unresolved typesetting."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=os.environ.get('GITHUB_SHA','local-build')
    files=sorted(list(HERE.glob('*.tex'))+list((HERE/'parts').glob('*.tex'))+list(HERE.glob('*.py'))+list(HERE.glob('*.sh')))
    receipt={'source_commit':source,'review_head':'2c6f180fa0baf23386e0a46a64abe7503ea65b00',
             'sha256':{str(p.relative_to(HERE)):sha(p) for p in files}}
    (HERE/'evidence/SOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    pdfs={}
    for doc in ['geometry','paper','applications']:
        log=(HERE/(doc+'.log')).read_text(errors='replace')
        pages=int(re.search(r'Output written on .*?\((\d+) pages?',log,re.S).group(1))
        errors={'undefined_references':len(re.findall(r'(?:Reference|Citation) .*? undefined',log)),
                'undefined_summary':int('There were undefined references' in log),
                'duplicate_labels':int('There were multiply-defined labels' in log),
                'overfull_boxes':log.count('Overfull \\hbox')+log.count('Overfull \\vbox')}
        if any(errors.values()):raise RuntimeError(doc+': '+repr(errors))
        pdf=HERE/(doc+'.pdf')
        pdfs[doc+'.pdf']={'pages':pages,'sha256':sha(pdf),'bytes':pdf.stat().st_size,
                         'log_sha256':sha(HERE/(doc+'.log')),**errors}
    out={'kind':'actual v118 PDF build and source receipt','source_commit':source,
      'built_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'pdfs':pdfs,'diagnostics_sha256':sha(HERE/'evidence/DIAGNOSTICS.json'),
      'preservation_sha256':sha(HERE/'evidence/PRESERVATION.json'),
      'source_receipt_sha256':sha(HERE/'evidence/SOURCE_RECEIPT.json'),
      'pdflatex':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
      'proof_certification':False,'priority_certification':False,
      'open_priority_item':'E117.1: Ballico 1993 full theorem text not obtained'}
    (HERE/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
