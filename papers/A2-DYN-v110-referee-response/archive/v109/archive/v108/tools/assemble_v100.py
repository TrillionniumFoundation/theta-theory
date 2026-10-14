#!/usr/bin/env python3
"""Include the complete preserved v99 article with a separate reference namespace."""
from pathlib import Path
from check_v100 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    import assemble_v99
    assemble_v99.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Quadratic momentum caps and paired physical traces}'
    require(text.count(marker)==1,'v99 archive insertion boundary')
    text=text.replace(marker,archive(99,'Global momentum uniqueness and marked physical pressure')+marker)
    text=text.replace('A2-DYN, revision 99; complete retained source through revision 98',
                      'A2-DYN, revision 100 (uniform capacity); complete retained source through revision 99')
    require(text.count('Superseded dyadic notation.')==1,'active historical correction notice')
    target.write_text(text)
if __name__=='__main__':assemble()
