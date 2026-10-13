#!/usr/bin/env python3
"""Retain all v83 text; qualify historical module 189 at its inclusion."""
from pathlib import Path
from check_v77 import require
from assemble_v83 import archive
PAPER=Path(__file__).resolve().parents[1]

def assemble() -> None:
    import assemble_v83
    assemble_v83.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Retained critical-source criterion}'
    require(master.count(marker)==1,'v83 archive insertion boundary')
    master=master.replace(marker,archive(83,'Untruncated optical potentials and complete first-exit surface mass')+marker)
    old=r'\input{core/189_dyadic_critical_source_criterion}'
    require(master.count(old)==1,'historical module 189 must be qualified once')
    note=r'''\begin{quote}\small
\textbf{Superseded dyadic notation.}
The next module is retained as a historical source, not as an active
reference for its dyadic integration formula. The active convention is
\[
 \ell_j=2^{-j}r,\qquad
 \int_{\ell_j/2}^{\ell_j}v(t+s)\,ds
   =\int_{t+\ell_j/2}^{t+\ell_j}v(u)\,du.
\]
The variable in the first integral is an offset. The complete microscopic
tail is formed before the collision limsup. This corrected convention,
used in the active article, supersedes the ambiguous historical display;
no decay conclusion is inferred from this editorial correction.
\end{quote}
'''
    master=master.replace(old,note+old)
    master=master.replace('A2-DYN, revision 83; complete retained source through revision 82',
                          'A2-DYN, revision 84; complete retained source through revision 83')
    target.write_text(master)

if __name__=='__main__':assemble()
