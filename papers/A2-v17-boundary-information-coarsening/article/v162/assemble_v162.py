#!/usr/bin/env python3
"""Apply the v162 allocation to the pinned complete v161 assembler.

This is ordinary, auditable source reuse. The complete predecessor source
and all its mathematical blocks are checked by the inherited assembler.
Only v162 outputs are publication targets.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'v161/assemble_v161.py'
PIN='60c78967b52187b3fcbafef869aa7f7f2711b4b591ac91e0423f731c1de56aa4'
def once(text,before,after):
    if text.count(before)!=1:raise RuntimeError('Nonunique assembler anchor: '+before)
    return text.replace(before,after,1)
def main():
    if hashlib.sha256(PREVIOUS.read_bytes()).hexdigest()!=PIN:
        raise RuntimeError('Locked v161 assembler changed')
    code=PREVIOUS.read_text()
    changes={
        'from frontmatter_v161 import':'from frontmatter_v162 import',
        "'revision 161},pdfauthor'":"'revision 162},pdfauthor'",
        "PREV=HERE.parent/'v160'/'geometry.tex'":"PREV=HERE.parent/'v161'/'geometry.tex'",
        "PREV_HASH='ebe53861e6313880a01b8bda8e80930f209c1b20c7c9ed1e6b78b52cffa27d73'":"PREV_HASH='2243b35ce726c25c8cf84b6e2301e2b0e1fc1e3da77b096e677a5ead814805d7'",
        "REVIEW='596df442f9155c79b6b33378c0a208259385b2ae'":"REVIEW='3d22c10f34d889081000232bb8f2241d5988fc37'",
        "BASE='58c33453bf01d1f73083cb744d0479ecdc3dcf2f'":"BASE='9e3b6639021a5f1fdb725961c7a7b6bb9cf55779'",
        "INPUTS=('multiple-incidence-v161.tex','higher-contact-v161.tex','effective-boundary-v161.tex')":"INPUTS=('versal-contacts-v162.tex','euclidean-boundary-v162.tex','technical-completions-v162.tex','invariant-deformations-v162.tex')",
        "'Effective boundary groupoids and relative lifting obstructions']":"'Effective boundary groupoids and relative lifting obstructions','Algebraic envelope forms and invariant relative deformations']",
        "'Multiple reduced incidence and its complete Hilbert boundary','Higher contact, thick tails, and singular multiplication graphs']":"'Versal contact coordinates for regular symmetric pencils','Euclidean charts of the ambient Hilbert boundary','A non-equidimensional ambient Hilbert fibre','Multiple reduced incidence and its complete Hilbert boundary','Higher contact, thick tails, and singular multiplication graphs']",
        ".replace('revision 160','revision 161')":".replace('revision 161','revision 162')",
        "label.endswith('v161')":"label.endswith(('v161','v162'))",
        "if __name__=='__main__':main()":"",
    }
    for before,after in changes.items():code=once(code,before,after)
    code=code.replace('Complete v160 source hash mismatch','Complete v161 source hash mismatch')
    code=code.replace('_FRONTMATTER_V160','_FRONTMATTER_V161')
    for name in ('PAPER_MAP','NONDELETION','BUILD_RECEIPT','THEOREM_INDEX','EXACT_CHECKS'):
        code=code.replace(name+'_V161',name+'_V162')
    code=code.replace('INHERITED_V160_CHECKS_RERUN','INHERITED_V161_CHECKS_RERUN').replace('revision=161','revision=162')
    code=code.replace("'frontmatter_v161.py','assemble_v161.py','check_v161.py'","'frontmatter_v162.py','assemble_v162.py','check_v162.py'")
    ns={'__file__':str(HERE/'assemble_v162.py'),'__name__':'v162_source_assembly'}
    exec(compile(code,str(PREVIOUS),'exec'),ns)
    ns['main']()
if __name__=='__main__':main()
