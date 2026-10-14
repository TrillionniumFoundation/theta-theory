#!/usr/bin/env python3
"""Assemble the complete v84 article and a page-resolved dependency guide."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v84
    assemble_v84.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Untruncated optical potentials and complete first-exit surface mass}'
    require(master.count(marker)==1,'v84 archive insertion boundary')
    insert=(r'\input{appendices/v85_dependency_guide}'+'\n'+
            archive(84,'Residence persistence and paired physical boundary transfer'))
    master=master.replace(marker,insert+marker)
    master=master.replace('A2-DYN, revision 84; complete retained source through revision 83',
                          'A2-DYN, revision 85; complete retained source through revision 84')
    target.write_text(master)

if __name__=='__main__':assemble()
