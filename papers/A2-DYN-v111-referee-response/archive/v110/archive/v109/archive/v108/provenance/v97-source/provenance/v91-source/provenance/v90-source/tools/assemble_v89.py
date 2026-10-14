#!/usr/bin/env python3
"""Include the complete weak-Lp v88 article with a distinct reference namespace."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    import assemble_v88
    assemble_v88.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Complete segment traces and the original concentration source}'
    require(text.count(marker)==1,'v88 archive boundary')
    addition=archive(88,'Untruncated residence moments and the raw local norm')
    text=text.replace(marker,r'\input{appendices/v89_dependency_guide}'+'\n'+addition+marker)
    text=text.replace('A2-DYN, revision 88; complete retained source through revision 87',
                      'A2-DYN, revision 89; complete retained source through weak-Lp revision 88')
    target.write_text(text)
if __name__=='__main__':assemble()
