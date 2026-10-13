#!/usr/bin/env python3
"""Add the complete v92 article without modifying its inherited source bytes."""
from pathlib import Path
from check_v93 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v92
    assemble_v92.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{The unweakened critical limit and all-radius source control}'
    require(text.count(marker)==1,'v92 archive boundary')
    text=text.replace(marker,archive(92,'One-sided lower inversion and positive-reference conditioning')+marker)
    text=text.replace('A2-DYN, revision 92; complete retained source through revision 91',
                      'A2-DYN, revision 93; complete retained source through revision 92')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic correction')
    require(text.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(text)

if __name__=='__main__':assemble()
