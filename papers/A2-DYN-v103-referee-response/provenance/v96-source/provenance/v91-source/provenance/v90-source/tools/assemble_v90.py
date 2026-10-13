#!/usr/bin/env python3
"""Assemble the entire v89 article without changing any inherited source byte."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v89
    assemble_v89.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Untruncated residence moments and the raw local norm}'
    require(master.count(marker)==1,'v89 archive insertion boundary')
    addition=archive(89,'Critical distribution and the complete diffusive window')
    master=master.replace(marker,addition+marker)
    master=master.replace('A2-DYN, revision 89; complete retained source through weak-Lp revision 88',
                          'A2-DYN, revision 90; complete retained source through revision 89')
    require(master.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(master)

if __name__=='__main__':assemble()
