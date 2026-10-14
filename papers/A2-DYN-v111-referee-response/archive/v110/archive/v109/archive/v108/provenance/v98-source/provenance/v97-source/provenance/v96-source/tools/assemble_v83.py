#!/usr/bin/env python3
"""Assemble byte-preserved v81/v82 articles and the whole inherited supplement."""
from pathlib import Path
import re
from check_v77 import require

PAPER=Path(__file__).resolve().parents[1]


def archive(version: int, title: str) -> str:
    old=(PAPER/'provenance'/f'v{version}-main.tex').read_text()
    abstract=old.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    body=re.split(r'\\input\{journal-references(?:-v\d+)?\}',old.split(r'\maketitle',1)[1],maxsplit=1)[0]
    require(r'\end{document}' not in body,'historical bibliography delimiter')
    prefix=r'''\part{TITLE}
\begingroup
\let\ArchiveLabel\label
\let\ArchiveRef\ref
\renewcommand{\label}[1]{\ArchiveLabel{NAMESPACE:#1}}
\renewcommand{\ref}[1]{%
  \IfBeginWith{#1}{supp-}{%
    \StrBehind{#1}{supp-}[\ArchiveTarget]%
    \ArchiveRef{\ArchiveTarget}%
  }{\ArchiveRef{NAMESPACE:#1}}%
}
\makeatletter
\let\ltx@label\label
\makeatother
\paragraph{Retained revision-VERSION abstract.}
'''.replace('TITLE',title).replace('NAMESPACE',f'v{version}archive').replace('VERSION',str(version))
    note=''
    if version==82:
        note=r'''\paragraph{Source clarification for the retained dyadic formula.}
The following historical article is reproduced without editing its source.
In its module 189, the intervals named $I_j(t)$ are absolute roof intervals,
whereas the integrand $v(t+s)$ uses an offset. The active revision resolves
this notation by integrating $s$ from $\ell_j/2$ to $\ell_j$, or equivalently
$v(u)$ over $(t+\ell_j/2,t+\ell_j]$. Its full microscopic tail is formed
before the collision limsup. See the active article's ordered-tail theorem;
no historical smallness condition is promoted by this clarification.
'''
    return prefix+note+abstract+'\n'+body+'\n\\endgroup\n'


def assemble() -> None:
    import verify_v81 as inherited
    inherited.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    marker=r'\part{Singular insertions and common exact-label fibers}'
    require(master.count(marker)==1,'complete inherited insertion boundary')
    insert=archive(82,'Retained critical-source criterion')+archive(81,'Joint endpoint localization and critical optical insertions')
    master=master.replace(marker,insert+marker)
    master=master.replace('A2-DYN, revision 81; complete retained source through revision 80',
                          'A2-DYN, revision 83; complete retained source through revision 82')
    # v81 inherited article references point into v81's supplement. Those
    # unprefixed sources remain in the assembled archive below both additions.
    target.write_text(master)

if __name__=='__main__':
    assemble()
