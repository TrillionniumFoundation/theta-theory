#!/usr/bin/env python3
"""Preserve and include the complete v97 article and all 234 old cores."""
from pathlib import Path
from check_v98 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v97
    assemble_v97.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Exact-label physical continuation and occupation}'
    require(text.count(marker)==1,'v97 archive insertion boundary')
    text=text.replace(marker,archive(97,'Capped coarea occupation and failure-source recovery')+marker)
    text=text.replace('A2-DYN, revision 97; complete retained source through revision 96',
                      'A2-DYN, revision 98; complete retained source through revision 97')
    require(text.count('Superseded dyadic notation.')==1,'historical offset notice')
    target.write_text(text)

if __name__=='__main__': assemble()
