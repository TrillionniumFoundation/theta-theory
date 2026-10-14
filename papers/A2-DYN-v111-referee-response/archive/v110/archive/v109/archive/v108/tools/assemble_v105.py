#!/usr/bin/env python3
"""Compile all inherited mathematics, preserving the complete v104 article."""
from pathlib import Path
from check_v100 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble():
    from assemble_v104 import assemble as inherited
    inherited()
    target=PAPER/'build/supplement-source.tex'
    s=target.read_text()
    marker=r'\part{Endpoint-distance coarea and positive recovery}'
    require(s.count(marker)==1,'v104 article insertion boundary')
    s=s.replace(marker,archive(104,'Positive angular intervals and paid critical arms')+marker)
    s=s.replace('A2-DYN, revision 104; complete retained source through revision 103',
      'A2-DYN, revision 105; complete retained source through revision 104')
    require(s.count('Superseded dyadic notation.')==1,'historical correction notice')
    target.write_text(s)
if __name__=='__main__': assemble()
