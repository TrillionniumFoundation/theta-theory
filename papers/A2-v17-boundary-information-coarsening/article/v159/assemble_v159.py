#!/usr/bin/env python3
"""Materialize v159 without editing the locked v157/v158 inputs.

The source transformation below reuses the already inspected preservation and
three-PDF assembler. Every edit is explicit and checked against a unique anchor.
The emitted manuscripts are complete UTF-8 LaTeX files, not encoded bundles.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v158'
PIN={
 'assemble_v158.py':'d6ec47cfd6b3600a1b9f999672f6e5ca86d7910b9fcedd8e31e94fb221c4b9e8',
 'check_v158.py':'30f3a8a5f454cb17861065fdb8a1894ec142e7dd5b83df5d9b06cf6e48dbb1f0',
 'frontmatter_v158.py':'8d3d4651130a7f73346a991fce2451a120e8c7420c2f378d5b535457b1dbe8a5',
 'hilbert-boundary-v158.tex':'23899e01f863827290cb73d4c29a6df4dfc86585577192ec7e9b24282af64876',
 'intrinsic-envelope-v158.tex':'09e50050884cb4a07bf2019e467a0b340f0575f5ec091d720b1e32e9e244c6a0',
 'power-foundations-v158.tex':'729eaf6d82eccbf265e1aadf0bf97ee2cf4ae909b0ff17d4bdfd657573a0cfa8',
 'singular-power-geometry-v158.tex':'9438c51a437a599a6527e7b51131e922af67c4bf3cb87b0ff7f85792d92fc24b',
}

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def once(text: str, before: str, after: str) -> str:
    if text.count(before)!=1:
        raise RuntimeError('Nonunique assembler anchor: '+before)
    return text.replace(before,after,1)

def main() -> None:
    for name,expected in PIN.items():
        if digest(PREV/name)!=expected:
            raise RuntimeError('Locked derivation source changed: '+name)
    # This only regenerates an intermediate master in the working tree. It does
    # not publish or claim a previously materialized v158 submission.
    subprocess.run([sys.executable,str(PREV/'assemble_v158.py')],check=True,
                   stdout=subprocess.PIPE,text=True)
    code=(PREV/'assemble_v158.py').read_text()
    code=once(code,"PREV=HERE.parent/'v157'/'geometry.tex'","PREV=HERE.parent/'v158'/'geometry.tex'")
    code=once(code,"PREV_HASH='ef88694ccf51ed23f55bc6dd5e8b9354a8054efbaa227b7b117632699df9a9ed'",
              "PREV_HASH='45ddef54017a93a39f533b0a099793acfb748b0849156f9cf43838d564e376e4'")
    code=once(code,'from frontmatter_v158 import','from frontmatter_v159 import')
    code=once(code,"('power-foundations-v158.tex','intrinsic-envelope-v158.tex','singular-power-geometry-v158.tex','hilbert-boundary-v158.tex')","('modular-boundary-v159.tex',)")
    code=once(code,"'The intrinsic source and its apolar envelope'}","'The intrinsic source and its apolar envelope','Universal property of the intrinsic envelope'}")
    code=once(code,"'A computed boundary of the pencil incidence space','Singularities of the universal power-zero schemes'","'A computed boundary of the pencil incidence space','Ordinary collision strata and their Hilbert fibres','Singularities of the universal power-zero schemes'")
    code=once(code,".replace('revision 157','revision 158')",".replace('revision 158','revision 159')")
    code=code.replace('revision 158},pdfauthor','revision 159},pdfauthor')
    code=code.replace("'revision':158","'revision':159")
    code=code.replace('PREVIOUS_FRONTMATTER_V157','PREVIOUS_FRONTMATTER_V158')
    for name in ('PAPER_MAP','NONDELETION','BUILD_RECEIPT','EXACT_CHECKS'):
        code=code.replace(name+'_V158',name+'_V159')
    code=code.replace('INHERITED_V157_CHECKS_RERUN','INHERITED_V158_CHECKS_RERUN')
    code=once(code,"('frontmatter_v158.py','power-foundations-v158.tex','intrinsic-envelope-v158.tex','singular-power-geometry-v158.tex','hilbert-boundary-v158.tex','assemble_v158.py','check_v158.py')",
              "('frontmatter_v159.py','modular-boundary-v159.tex','assemble_v159.py','check_v159.py')")
    code=once(code,"if __name__=='__main__':main()",'')
    namespace={'__file__':str(HERE/'assemble_v159.py'),'__name__':'a2_v159_assembler'}
    exec(compile(code,str(HERE/'inspected-assembler-v159.py'),'exec'),namespace)
    namespace['main']()
    for name in ('NONDELETION_V159.json','BUILD_RECEIPT_V159.json'):
        p=HERE/name;record=json.loads(p.read_text())
        record.update(
            base_complete_revision_commit='a6d34cd2bb2075c64015f3667dbf3f391665cefd',
            preserved_derivation_commit='61c7a13fa1ce2c65777b9ca7a8e5f6c17dd6ca48',
            preserved_derivation_input_sha256=PIN,
            predecessor_master_generated_from_locked_derivations=True,
            v158_preexisting_complete_pdf_asserted=False,
            v157_labels_retained=352,v157_math_blocks_retained=236,
            v158_labels_retained=390,v158_math_blocks_retained=257)
        p.write_text(json.dumps(record,indent=2)+'\n')
    print('Complete v159 source assembly finished.',flush=True)
if __name__=='__main__':main()
