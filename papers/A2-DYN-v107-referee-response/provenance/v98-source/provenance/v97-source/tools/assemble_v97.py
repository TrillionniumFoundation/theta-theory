#!/usr/bin/env python3
"""Append the complete v96 article without editing any historical source."""
from pathlib import Path
from check_v97 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v96
    assemble_v96.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Two-ended packets and intrinsic radial residence}'
    require(text.count(marker)==1,'v96 article insertion boundary')
    text=text.replace(marker,archive(96,'Exact-label physical continuation and occupation')+marker)
    text=text.replace('A2-DYN, revision 96; complete retained source through revision 95',
                      'A2-DYN, revision 97; complete retained source through revision 96')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic clarification')
    require(text.count('hypertexnames=false')==1,'unique historical PDF targets')
    target.write_text(text)

if __name__=='__main__':assemble()
