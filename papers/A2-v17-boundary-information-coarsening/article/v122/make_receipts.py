#!/usr/bin/env python3
"""Source/product binding and LaTeX postflight for this revision only."""
from pathlib import Path
import hashlib,json,os,re,subprocess
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source={str(p.relative_to(D)):sha(p) for p in sorted(D.rglob('*')) if p.is_file()
        and not any(x in p.relative_to(D).parts for x in ('evidence','crossrefs','__pycache__','inherited-v118','inherited-v119'))
        and p.suffix in ('.tex','.py','.sh','.md','.json')}
products={};warnings={}
for doc in ('paper','geometry','applications'):
    log=(D/(doc+'.log')).read_text(errors='replace')
    bad=[line for line in log.splitlines() if re.search(r'(Reference|Citation).*undefined|There were undefined|multiply defined|^! ',line)]
    if bad: raise RuntimeError(doc+': unresolved LaTeX errors: '+repr(bad))
    over=[line for line in log.splitlines() if 'Overfull \\hbox' in line]
    warnings[doc]={'overfull_hboxes':over}
    if over: raise RuntimeError(doc+': overfull boxes: '+repr(over))
    pdf=D/(doc+'.pdf')
    info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    products[doc]={'file':pdf.name,'sha256':sha(pdf),'pages':pages}
receipt={'revision':122,'source_commit':os.environ.get('SOURCE_COMMIT_SHA','local source snapshot; not a git-commit claim'),
         'source_hashes':source,'products':products,'latex_postflight':warnings,
         'proof_certification':False,'priority_certification':False}
(D/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'products':products,'latex_postflight':warnings},indent=2))

labels=('lem:restriction-contraction','prop:quadratic-ramification',
        'prop:admissible-ramification','lem:global-two-stratum',
        'thm:ramification-primary','thm:primary-powers-intrinsic',
        'prop:ramification-flat-family','lem:nonuniruled-cancellation',
        'thm:intrinsic-ramification-recovery','cor:intrinsic-elliptic-distinction')
mapping={}
for doc in ('geometry','paper'):
    aux=(D/(doc+'.aux')).read_text()
    mapping[doc]={}
    for label in labels:
        pattern=r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^}]+)\}\{([^}]+)\}'
        match=re.search(pattern,aux)
        if not match: raise RuntimeError('Missing compiled label: '+doc+' '+label)
        mapping[doc][label]={'number':match.group(1),'page':match.group(2)}
(D/'evidence/THEOREM_MAP.json').write_text(json.dumps(mapping,indent=2)+'\n')
