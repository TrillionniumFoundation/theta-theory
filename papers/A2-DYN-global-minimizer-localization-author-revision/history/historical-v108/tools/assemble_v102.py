#!/usr/bin/env python3
"""Preserve and assemble the complete actual v100 article, not the v101 alias."""
from pathlib import Path
from check_v100 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    import assemble_v100
    assemble_v100.assemble()
    p=PAPER/'build/supplement-source.tex';text=p.read_text()
    marker=r'\part{Global momentum uniqueness and marked physical pressure}'
    require(text.count(marker)==1,'v100 archive insertion boundary')
    text=text.replace(marker,archive(100,'Uniform geometric capacity and the positive paired trace')+marker)
    text=text.replace('A2-DYN, revision 100 (uniform capacity); complete retained source through revision 99',
                      'A2-DYN, revision 102; complete retained source through actual revision 100')
    ref=PAPER/'build/v99-archive-references.tex';refs=ref.read_text()
    if r'\bibitem{DZUniform}' not in refs:
        extra=(PAPER/'journal-references-v100.tex').read_text().split(r'\bibitem{DZUniform}',1)[1].split(r'\end{thebibliography}',1)[0]
        refs=refs.replace(r'\end{thebibliography}',r'\bibitem{DZUniform}'+extra+r'\end{thebibliography}')
    (PAPER/'build/v102-archive-references.tex').write_text(refs)
    text=text.replace(r'\input{build/v99-archive-references}',r'\input{build/v102-archive-references}')
    require(text.count('Superseded dyadic notation.')==1,'historical notation notice')
    p.write_text(text)
if __name__=='__main__':assemble()
