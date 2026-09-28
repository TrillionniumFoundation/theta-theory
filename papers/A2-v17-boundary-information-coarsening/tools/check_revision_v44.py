#!/usr/bin/env python3
"""Check full v43 preservation, additive v44 sources and static references."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import re
from source_provenance import blob_id, graph, require, strip_comments

ROOT=Path(__file__).resolve().parents[1]
SOURCE='22d9b930a426cdb2c62984a5a3e5875e95e05e79'
BASE='history/v43-review-baseline/main.tex'
ADDED={'article/01e_realization_overview_v44.tex','article/23i_nonsymmetric_periodic_realization_v44.tex'}


def main() -> None:
    ledger=json.loads((ROOT.parents[1]/'deliveries/a2-v43'/SOURCE/'active-source-manifest.json').read_text())
    verified=0
    for entry,items in ledger.items():
        for name,item in items.items():
            p=ROOT/(BASE if name=='main.tex' else name)
            require(p.is_file() and blob_id(p.read_bytes())==item['git_blob'], 'Historical source changed: '+name)
            verified+=1
    old=graph(ROOT,BASE); current=graph(ROOT,'main.tex')
    require((old-{BASE})|{'main.tex'}|ADDED==current,'Native input closure changed beyond the two additions')
    a=(ROOT/BASE).read_text(); b=(ROOT/'main.tex').read_text()
    inputs=re.compile(r'\\(?:input|include)\{([^}]+)\}')
    names={x[:-4] for x in ADDED}
    require([x for x in inputs.findall(b) if x not in names]==inputs.findall(a),'Inherited direct input order changed')
    restored=b.replace('revision 44','revision 43')
    for name in sorted(names): restored=restored.replace('\\input{'+name+'}\n','')
    restored=restored.replace('An explicit nonsymmetric periodic family realizes all the incidence and\nclearance conditions together; two support harmonics register its recovered\ncurve images and expose both independent deck holonomies.\n','')
    require(restored==a,'Undeclared main text change')
    texts=[strip_comments((ROOT/x).read_text()) for x in sorted(current)]
    text='\n'.join(texts)
    label=re.compile(r'\\label\{([^}]+)\}')
    labels=label.findall(text)
    external={'TC-'+x for x in label.findall((ROOT/'two_collision.tex').read_text())}
    missing=set(re.findall(r'\\(?:eqref|ref|pageref|autoref)\*?\{([^}]+)\}',text))-set(labels)-external
    require(not missing,'Unresolved references: '+repr(sorted(missing)))
    require(not [x for x,n in Counter(labels).items() if n>1],'Duplicate labels')
    cited={k.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in group.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
    require(cited<=bib,'Unresolved citations')
    env=r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}'
    oldtext='\n'.join((ROOT/x).read_text() for x in sorted(old))
    print(json.dumps({'revision':'A2 v44','status':'passed','reviewed_source_commit':SOURCE,
      'review_commit':'6f7de242000a7db2bf473276b8e1792104c7cd42',
      'verified_baseline_manifest_entries':verified,'main_recursive_tex_files':len(current),
      'companion_recursive_tex_files':len(graph(ROOT,'two_collision.tex')),
      'retained_baseline_statements':dict(Counter(re.findall(env,oldtext))),
      'added_statements':dict(Counter(re.findall(env,'\n'.join((ROOT/x).read_text() for x in ADDED)))),
      'duplicate_labels':[],'unresolved_references':[],'unresolved_citations':[],
      'mathematical_certification':False},indent=2,sort_keys=True))


if __name__=='__main__':main()
