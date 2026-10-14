#!/usr/bin/env python3
"""Include the full preceding article without rewriting inherited source bytes."""
from pathlib import Path
from check_v99 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]
def assemble() -> None:
    import assemble_v98
    assemble_v98.assemble()
    target=PAPER/'build/supplement-source.tex'
    text=target.read_text()
    marker=r'\part{Capped coarea occupation and failure-source recovery}'
    require(text.count(marker)==1,'v98 archive insertion boundary')
    text=text.replace(marker,archive(98,'Quadratic momentum caps and paired physical traces')+marker)
    text=text.replace('A2-DYN, revision 98; complete retained source through revision 97',
                      'A2-DYN, revision 99; complete retained source through revision 98')
    require(text.count('Superseded dyadic notation.')==1,'historical offset notice')
    # The historical global bibliography predates the pressure citation.
    # Supply it to the assembled archive, leaving every old bibliography byte intact.
    refs=(PAPER/'references.tex').read_text()
    extra=(PAPER/'journal-references-v99.tex').read_text().split(r'\bibitem{BDPressure}',1)[1].split(r'\end{thebibliography}',1)[0]
    require(r'\bibitem{BDPressure}' not in refs,'duplicate archive pressure citation')
    refs=refs.replace(r'\end{thebibliography}',r'\bibitem{BDPressure}'+extra+r'\end{thebibliography}')
    (PAPER/'build/v99-archive-references.tex').write_text(refs)
    require(text.count(r'\input{references}')==1,'archive bibliography boundary')
    text=text.replace(r'\input{references}',r'\input{build/v99-archive-references}')
    target.write_text(text)
if __name__=='__main__':assemble()
