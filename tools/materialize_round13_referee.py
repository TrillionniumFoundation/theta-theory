#!/usr/bin/env python3
from pathlib import Path
from round13_config import PAPERS,SOURCES,PLATFORMS,ABSTRACTS
ROOT=Path(__file__).resolve().parents[1]
for folder in PAPERS:
    paper=ROOT/'papers'/folder
    src=ROOT/'revision'/'round13-referee-final'/SOURCES[folder]
    main=paper/'main.tex'; active=paper/'ROUND13_POSITIVE_CLOSURE.tex'
    if not src.is_file() or not main.is_file():
        raise SystemExit(f'missing source/main for {folder}')
    active.write_bytes(src.read_bytes())
    old=main.read_text(encoding='utf-8',errors='strict')
    marker=r'\begin{document}'
    pos=old.find(marker)
    if pos<0: raise SystemExit(f'no document marker in {main}')
    pre=old[:pos].rstrip()
    escaped=SOURCES[folder].replace('_',r'\_')
    body=(pre+'\n'+marker+r'''
\raggedbottom
\begin{abstract}
'''+ABSTRACTS[folder]+r'''
\end{abstract}
\maketitle
\noindent\textbf{Platform identifier:} \texttt{'''+PLATFORMS[folder]+r'''}. 
\noindent\textbf{Controlling revision:} \texttt{ROUND13-REFEREE-POSITIVE-CLOSURE}. 
\noindent\textbf{Registered proof source:} \texttt{'''+escaped+r'''}. 
\tableofcontents

\input{ROUND13_POSITIVE_CLOSURE.tex}

\section*{Scope and verification status}
This manuscript states positive theorem closure in the declared model-specific regular regime. Cross-paper inputs follow the round-thirteen dependency ledger. Repository source, proof-structure, direct-counterexample, and build gates are internal reproducibility checks and do not replace independent external mathematical review.
\printbibliography
\end{document}
''')
    main.write_text(body,encoding='utf-8')
print('ROUND13_MATERIALIZED 11/11')
