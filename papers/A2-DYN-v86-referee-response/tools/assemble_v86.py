#!/usr/bin/env python3
"""Add the full byte-preserved v85 article with resolved reference namespaces."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v85
    assemble_v85.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Residence persistence and paired physical boundary transfer}'
    require(master.count(marker)==1,'v85 archive insertion boundary')
    insert=archive(85,'Complete residence bands and zero-residence source')
    # Strip only the unclosed bibliography font group, whose bibliography is
    # printed by the retained supplement. The original snapshot is unchanged.
    sizing='\\begingroup\n\\small\n\\enlargethispage{2\\baselineskip}\n'
    require(insert.count(sizing)==1,'v85 bibliography wrapper')
    insert=insert.replace(sizing,'')
    page=r"""\let\ArchivePageRef\pageref
\renewcommand{\pageref}[1]{%
  \IfBeginWith{#1}{supp-}{%
    \StrBehind{#1}{supp-}[\ArchivePageTarget]%
    \ArchivePageRef{\ArchivePageTarget}%
  }{\ArchivePageRef{v85archive:#1}}%
}
"""
    insert=insert.replace(r'\paragraph{Retained revision-85 abstract.}',page+r'\paragraph{Retained revision-85 abstract.}')
    master=master.replace(marker,r'\input{appendices/v86_dependency_guide}'+'\n'+insert+marker)
    master=master.replace('A2-DYN, revision 85; complete retained source through revision 84',
                          'A2-DYN, revision 86; complete retained source through revision 85')
    target.write_text(master)

if __name__=='__main__':assemble()
