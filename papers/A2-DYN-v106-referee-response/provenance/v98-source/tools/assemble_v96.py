#!/usr/bin/env python3
"""Assemble the full prior article, with source bytes preserved."""
from pathlib import Path
from check_v96 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v95
    assemble_v95.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Radial entrance packets and signed projected forcing}'
    require(text.count(marker)==1,'v95 article insertion boundary')
    text=text.replace(marker,archive(95,'Two-ended packets and intrinsic radial residence')+marker)
    text=text.replace('A2-DYN, revision 95; complete retained source through revision 94',
                      'A2-DYN, revision 96; complete retained source through revision 95')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic clarification')
    require(text.count('hypertexnames=false')==1,'unique historical PDF targets')
    target.write_text(text)

if __name__=='__main__':assemble()
