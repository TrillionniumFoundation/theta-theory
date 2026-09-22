#!/usr/bin/env python3
"""Record the actual build; do not confuse compilation with proof checking."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

HERE=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    sources={}
    for p in sorted(HERE.rglob('*')):
        rel=p.relative_to(HERE)
        if p.is_file() and p.suffix in {'.tex','.py','.sh'} and rel.parts[0] not in {'evidence','crossrefs'}:
            sources[str(rel)]=sha(p)
    source_sha=os.environ.get('MATHEMATICAL_SOURCE_SHA') or None
    if source_sha is not None and not re.fullmatch('[0-9a-f]{40}',source_sha):
        raise ValueError('MATHEMATICAL_SOURCE_SHA must be a full commit SHA')
    products={}
    for doc in ('geometry','paper','applications'):
        pdf,log=HERE/(doc+'.pdf'),HERE/(doc+'.log')
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        text=log.read_text(errors='replace')
        bad=[line for line in text.splitlines() if any(x in line for x in
             ('There were undefined references','There were multiply-defined labels',
              'Citation `','Reference `','Fatal error occurred','Emergency stop'))]
        if bad:
            raise RuntimeError(f'{doc}: unresolved final-pass diagnostics: '+str(bad))
        overfull=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt too wide\)',text)]
        products[doc]={'sha256':sha(pdf),'bytes':pdf.stat().st_size,'pages':pages,
                       'log_sha256':sha(log),'unresolved_references_or_citations':0,
                       'overfull_hbox_count':len(overfull),
                       'max_overfull_hbox_pt':max(overfull,default=0)}
    manifest={'mathematical_source_commit':source_sha,'sources_sha256':sources}
    (HERE/'evidence/SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    receipt={'revision':120,'mathematical_source_commit':source_sha,
             'last_math_change_commit':source_sha,
             'workflow_commit':os.environ.get('GITHUB_SHA') or None,
             'controlling_review_commits':['b409ec5eb4dfbb75850d90bff69a78604d3a512b'],
             'source_manifest_sha256':sha(HERE/'evidence/SOURCE_MANIFEST.json'),
             'diagnostics_sha256':sha(HERE/'evidence/DIAGNOSTICS.json'),
             'products':products,
             'tex_engine':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
             'run_id':os.environ.get('GITHUB_RUN_ID') or None,
             'source_date_epoch':os.environ.get('SOURCE_DATE_EPOCH'),
             'build_completed':True,'proof_certification':False,
             'priority_certification':False,
             'product_commit_recorded_separately':'evidence/PUBLISHED.json',
             'visual_inspection_recorded_separately':True}
    (HERE/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
