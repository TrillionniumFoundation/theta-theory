#!/usr/bin/env python3
"""Assemble the complete unchanged v102 article and all inherited mathematics."""
from pathlib import Path
from check_v100 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    from assemble_v102 import assemble as inherited
    inherited()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Uniform geometric capacity and the positive paired trace}'
    require(text.count(marker)==1,'v102 archive insertion boundary')
    text=text.replace(marker,archive(102,'Positive paired coarea and the relative transverse clock')+marker)
    text=text.replace('A2-DYN, revision 102; complete retained source through actual revision 100',
                      'A2-DYN, revision 103; complete retained source through revision 102')
    require(text.count('Superseded dyadic notation.')==1,'historical correction notice')
    target.write_text(text)
if __name__=='__main__':assemble()
