#!/usr/bin/env python3
"""Apply only the inspected AMS abstract pagination correction to v46.

The complete abstract, all mathematical source modules and every proof are
unchanged. The initial 244-page native build remains on its products branch.
"""
from pathlib import Path
import hashlib,importlib.util
P=Path('papers/A2-v17-boundary-information-coarsening')
OLD='e03944f219b88340adf7195b8b1be24f5c14d69c'
NEW='5b2b1cdff72c290674b0e910b0001dd35e202f44'

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def main():
    path=P/'main.tex';data=path.read_bytes()
    if blob(data) not in (OLD,NEW):raise RuntimeError('Unexpected v46 main source')
    if blob(data)==OLD:
        before='\\end{abstract}\n\\maketitle'
        after=r'''\end{abstract}
% Permit the full abstract to flow across pages rather than displacing it
% as an indivisible box and leaving an otherwise empty title page.
\makeatletter
\def\@setabstracta{%
  \ifvoid\abstractbox\else
    \skip@20\p@ \advance\skip@-\lastskip
    \advance\skip@-\baselineskip \vskip\skip@
    \unvbox\abstractbox \prevdepth\z@
  \fi}
\makeatother
\maketitle'''
        text=data.decode()
        if text.count(before)!=1:raise RuntimeError('Missing unique abstract anchor')
        result=text.replace(before,after).encode()
        if blob(result)!=NEW:raise RuntimeError('Pagination target differs from local reviewed source')
        path.write_bytes(result)
    spec=importlib.util.spec_from_file_location('initial_v46','.github/revision-sources/a2-v46-integrate.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.TARGET['main.tex']=NEW
    module.verify_targets()

if __name__=='__main__':main()
