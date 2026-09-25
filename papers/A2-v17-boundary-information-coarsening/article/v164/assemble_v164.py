#!/usr/bin/env python3
"""Build v164 from the complete v163 master without editing historical inputs."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v163'
PIN='306ca556cd7a6eb268e0fce483c0dbb9fe0f4d9421261bb44fba063356daadc6'
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def once(text:str,before:str,after:str)->str:
    if text.count(before)!=1:raise RuntimeError('Assembler anchor missing or nonunique: '+before)
    return text.replace(before,after,1)
def main()->None:
    original=PREV/'assemble_v163.py'
    if digest(original)!=PIN:raise RuntimeError('Predecessor assembler hash mismatch')
    code=original.read_text()
    code=once(code,"PREV=HERE.parent/'v162'/'geometry.tex'","PREV=HERE.parent/'v163'/'geometry.tex'")
    code=once(code,"PREV_HASH='7ccaca8309f9de7da7c134e2c96cf2b82266e3bba1f7a1402f8ee5533b97058d'","PREV_HASH='dd84a26f3e7fce5c9a37ea40188c3542442ef24c24d67d21d38c1661534110c5'")
    code=once(code,"BASE='299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8'","BASE='40a72ddfd85e16363385a1b64b922d61055e875c'")
    code=once(code,"INPUTS=('embedded-comparison-v163.tex','complete-contact-fibre-v163.tex','products-and-strata-v163.tex','tangent-and-effective-v163.tex')","INPUTS=('collision-wall-crossing-v164.tex','effective-collisions-v164.tex')")
    code=once(code,"'Tangent maps, linearizations, and effective transfer']","'Tangent maps, linearizations, and effective transfer','Collisions under the effective inverse']")
    code=once(code,"'The complete first nonreduced contact fibre','Products and adjacency for the first nonreduced boundary'","'The complete first nonreduced contact fibre','Collision of two incidence points','Products and adjacency for the first nonreduced boundary'")
    code=code.replace('frontmatter_v163','frontmatter_v164')
    code=once(code,"code=code.replace('revision 158},pdfauthor','revision 163},pdfauthor')","code=code.replace('revision 158},pdfauthor','revision 164},pdfauthor').replace('September 25, 2026','September 26, 2026')")
    code=once(code,".replace('revision 162','revision 163')",".replace('revision 163','revision 164').replace('September 25, 2026','September 26, 2026')")
    code=code.replace('FRONTMATTER_V162','FRONTMATTER_V163')
    code=code.replace('revision=163','revision=164')
    code=code.replace('PAPER_MAP_V163','PAPER_MAP_V164').replace('NONDELETION_V163','NONDELETION_V164')
    code=code.replace('BUILD_RECEIPT_V163','BUILD_RECEIPT_V164').replace('THEOREM_INDEX_V163','THEOREM_INDEX_V164')
    code=code.replace('EXACT_CHECKS_V163','EXACT_CHECKS_V164').replace('INHERITED_V162_CHECKS_RERUN','INHERITED_V163_CHECKS_RERUN')
    code=code.replace("('v161','v162','v163')","('v161','v162','v163','v164')")
    code=code.replace("'assemble_v163.py','check_v163.py'","'assemble_v164.py','check_v164.py'")
    namespace={'__file__':str(HERE/'assemble_v164.py'),'__name__':'a2_v164_assembly'}
    exec(compile(code,str(HERE/'generated_assembly.py'),'exec'),namespace)
    namespace['main']()
    for name in ('BUILD_RECEIPT_V164.json','NONDELETION_V164.json'):
        p=HERE/name;r=json.loads(p.read_text())
        r['predecessor_assembler_sha256']=PIN
        r['complete_reviewed_v162_tip']='299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8'
        r['post_review_v163_tip']='40a72ddfd85e16363385a1b64b922d61055e875c'
        r['no_new_external_independent_paper_I_audit_obtained']=True
        p.write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
