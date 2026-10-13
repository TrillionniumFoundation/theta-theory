#!/usr/bin/env python3
"""Assemble the complete v87 article without editing inherited sources."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    import assemble_v87
    assemble_v87.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Finite-count mixed moments and reachable optical concentration}'
    require(master.count(marker)==1,'v87 archive insertion boundary')
    insert=archive(87,'Complete segment traces and the original concentration source')
    sizing='\\begingroup\n\\small\n\\enlargethispage{2\\baselineskip}\n'
    require(insert.count(sizing)==1,'v87 bibliography wrapper')
    insert=insert.replace(sizing,'')
    page=r'''\let\ArchivePageRef\pageref
\renewcommand{\pageref}[1]{%
  \IfBeginWith{#1}{supp-}{%
    \StrBehind{#1}{supp-}[\ArchivePageTarget]%
    \ArchivePageRef{\ArchivePageTarget}%
  }{\ArchivePageRef{v87archive:#1}}%
}
'''
    insert=insert.replace(r'\paragraph{Retained revision-87 abstract.}',page+r'\paragraph{Retained revision-87 abstract.}')
    master=master.replace(marker,r'\input{appendices/v88_dependency_guide}'+'\n'+insert+marker)
    master=master.replace('A2-DYN, revision 87; complete retained source through revision 86',
                          'A2-DYN, revision 88; complete retained source through revision 87')
    require(master.count('hypertexnames=false')==1,'unique archive PDF targets')
    target.write_text(master)
if __name__=='__main__':assemble()
