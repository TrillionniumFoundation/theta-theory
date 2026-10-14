#!/usr/bin/env python3
"""Compile the entire retained v91 article without changing inherited files."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v91
    assemble_v91.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{All-scale original-source oscillation}'
    require(text.count(marker)==1,'v91 archive insertion boundary')
    text=text.replace(marker,archive(91,'The unweakened critical limit and all-radius source control')+marker)
    text=text.replace('A2-DYN, revision 91; complete retained source through revision 90',
                      'A2-DYN, revision 92; complete retained source through revision 91')
    require(text.count('Superseded dyadic notation.')==1,'historical correction retained')
    require(text.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(text)
if __name__=='__main__':assemble()
