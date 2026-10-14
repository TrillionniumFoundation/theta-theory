#!/usr/bin/env python3
"""Retain the complete v90 article and all 213 inherited cores."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v90
    assemble_v90.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Critical distribution and the complete diffusive window}'
    require(text.count(marker)==1,'v90 archive insertion boundary')
    text=text.replace(marker,archive(90,'All-scale original-source oscillation')+marker)
    text=text.replace('A2-DYN, revision 90; complete retained source through revision 89',
                      'A2-DYN, revision 91; complete retained source through revision 90')
    require(text.count('Superseded dyadic notation.')==1,'dyadic notice retained')
    require(text.count('hypertexnames=false')==1,'unique PDF targets')
    target.write_text(text)

if __name__=='__main__':assemble()
