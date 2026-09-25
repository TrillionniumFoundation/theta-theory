#!/usr/bin/env python3
"""Build complete v160 manuscripts from hash-locked v159/v158 sources.

Only the v160 directory is a publication target. Intermediate historical
masters are regenerated locally without changing their derivation inputs.
All predecessor mathematical blocks are retained byte for byte.
"""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v159'
PIN={
 'assemble_v159.py':'20ebe625dab53e657f243f1186097eca8be931cfb2f2f3e74fbee387faae0ae7',
 'check_v159.py':'09449297c4765aeb8ffe5b7ba1ef2557b962dc74057077c8181adb4dbd20b10a',
 'frontmatter_v159.py':'43a6768f319551c8bb48051d5ea81ad53ed03f86178b3309410ce9abdc648b95',
 'modular-boundary-v159.tex':'475380fb514973d1297a577180585d39b5fefa5230c7750f65ff93fa4cdce7b7',
}
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def once(text:str,before:str,after:str)->str:
    if text.count(before)!=1:raise RuntimeError('Nonunique assembler anchor: '+before)
    return text.replace(before,after,1)
def main()->None:
    for name,h in PIN.items():
        if digest(PREV/name)!=h:raise RuntimeError('Predecessor input changed: '+name)
    subprocess.run([sys.executable,str(PREV/'assemble_v159.py')],check=True,capture_output=True,text=True)
    code=(HERE.parent/'v158'/'assemble_v158.py').read_text()
    code=once(code,"PREV=HERE.parent/'v157'/'geometry.tex'","PREV=HERE.parent/'v159'/'geometry.tex'")
    code=once(code,"PREV_HASH='ef88694ccf51ed23f55bc6dd5e8b9354a8054efbaa227b7b117632699df9a9ed'","PREV_HASH='e3764d4678d65b3d66c7a35773b1e98d349ac915efffa299910d9129bd32f401'")
    code=once(code,'from frontmatter_v158 import','from frontmatter_v160 import')
    code=once(code,"('power-foundations-v158.tex','intrinsic-envelope-v158.tex','singular-power-geometry-v158.tex','hilbert-boundary-v158.tex')","('incidence-blowup-v160.tex',)")
    code=once(code,"'The intrinsic source and its apolar envelope'}","'The intrinsic source and its apolar envelope','Universal property of the intrinsic envelope','The incidence centre from failure multiplication'}")
    code=once(code,"'A computed boundary of the pencil incidence space','Singularities of the universal power-zero schemes'","'The simple corank-two incidence modification','A computed boundary of the pencil incidence space','Ordinary collision strata and their Hilbert fibres','Singularities of the universal power-zero schemes'")
    code=once(code,".replace('revision 157','revision 158')",".replace('revision 159','revision 160')")
    code=code.replace('revision 158},pdfauthor','revision 160},pdfauthor').replace("'revision':158","'revision':160")
    code=code.replace('PREVIOUS_FRONTMATTER_V157','PREVIOUS_FRONTMATTER_V159')
    for name in ('PAPER_MAP','NONDELETION','BUILD_RECEIPT','EXACT_CHECKS'):
        code=code.replace(name+'_V158',name+'_V160')
    code=code.replace('INHERITED_V157_CHECKS_RERUN','INHERITED_V159_CHECKS_RERUN')
    code=once(code,"('frontmatter_v158.py','power-foundations-v158.tex','intrinsic-envelope-v158.tex','singular-power-geometry-v158.tex','hilbert-boundary-v158.tex','assemble_v158.py','check_v158.py')","('frontmatter_v160.py','incidence-blowup-v160.tex','assemble_v160.py','check_v160.py')")
    code=once(code,"if __name__=='__main__':main()",'')
    namespace={'__file__':str(HERE/'assemble_v160.py'),'__name__':'a2_v160_assembler'}
    exec(compile(code,str(HERE/'inspected-assembler-v160.py'),'exec'),namespace)
    namespace['main']()
    for name in ('NONDELETION_V160.json','BUILD_RECEIPT_V160.json'):
        p=HERE/name;r=json.loads(p.read_text())
        r.update(preserved_derivation_commit='a27bd7fcea5c4ef04cdd8748411cdeab7ba42855',
                 preserved_v159_input_sha256=PIN,predecessor_master_generated_from_locked_derivations=True,
                 predecessor_remote_pdf_publication_succeeded=False,
                 v157_labels_retained=352,v157_math_blocks_retained=236,
                 v158_labels_retained=390,v158_math_blocks_retained=257,
                 v159_labels_retained=405,v159_math_blocks_retained=268)
        p.write_text(json.dumps(r,indent=2)+'\n')
    print('Complete v160 source assembly finished.')
if __name__=='__main__':main()
