#!/usr/bin/env python3
"""Apply the tested source delta plus the subdirectory-independent checker fix."""
import argparse
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('materializer',HERE/'materialize-a2-v74.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
FINAL_TREE='48787e35d236d4a896abe328d78eff0ef154fdee'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('operation',choices=('materialize','handoff'))
p.add_argument('--products-branch',required=True)
p.add_argument('--source-commit')
p.add_argument('--products-commit')
a=p.parse_args()
if a.operation=='materialize':
    base.materialize(a.products_branch)
    patch=(HERE/'a2-v74-preservation-fix.patch').read_bytes()
    base.git('apply','--check','--directory='+base.PREFIX,'-',data=patch)
    base.git('apply','--index','--directory='+base.PREFIX,'-',data=patch)
    base.require(base.git('write-tree','--prefix='+base.PREFIX+'/').decode().strip()==FINAL_TREE,
                 'Final manuscript tree differs from tested checker fix')
    base.EXPECTED_TREE=FINAL_TREE
    base.write_entry(None,None,a.products_branch)
    base.git('add','--','README.md','A2_REVISION_V73_REVIEW_READY.md','A2_REVISION_V74_REVIEW_READY.md')
else:
    base.require(bool(a.source_commit and a.products_commit),'Missing immutable references')
    base.EXPECTED_TREE=FINAL_TREE
    base.write_entry(a.source_commit,a.products_commit,a.products_branch)
