#!/usr/bin/env python3
"""Retain the entire v93 article and all inherited mathematics unchanged."""
from pathlib import Path
from check_v94 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]


def assemble() -> None:
    import assemble_v93
    assemble_v93.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{One-sided lower inversion and positive-reference conditioning}'
    require(text.count(marker)==1,'v93 archive insertion boundary')
    text=text.replace(marker,archive(93,'Absolute optical traces and signed ancestral upper forcing')+marker)
    text=text.replace('A2-DYN, revision 93; complete retained source through revision 92',
                      'A2-DYN, revision 94; complete retained source through revision 93')
    require(text.count('Superseded dyadic notation.')==1,'historical dyadic correction')
    require(text.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(text)


if __name__=='__main__':
    assemble()
