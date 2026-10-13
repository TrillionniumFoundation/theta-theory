#!/usr/bin/env python3
"""Add the complete v94 article without changing inherited mathematical bytes."""
from pathlib import Path
from check_v95 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v94
    assemble_v94.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Absolute optical traces and signed ancestral upper forcing}'
    require(text.count(marker)==1,'v94 archive insertion boundary')
    text=text.replace(marker,archive(94,'Radial entrance packets and signed projected forcing')+marker)
    text=text.replace('A2-DYN, revision 94; complete retained source through revision 93',
                      'A2-DYN, revision 95; complete retained source through revision 94')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic correction')
    require(text.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(text)

if __name__=='__main__':assemble()
