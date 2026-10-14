#!/usr/bin/env python3
"""Compile the complete preceding author article without altering its source."""
from pathlib import Path
from check_v100 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble():
    from assemble_v103 import assemble as inherited
    inherited()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Positive paired coarea and the relative transverse clock}'
    require(text.count(marker)==1,'v103 complete article insertion boundary')
    text=text.replace(marker,archive(103,'Endpoint-distance coarea and positive recovery')+marker)
    text=text.replace('A2-DYN, revision 103; complete retained source through revision 102',
                      'A2-DYN, revision 104; complete retained source through revision 103')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic correction notice')
    target.write_text(text)
if __name__=='__main__':assemble()
