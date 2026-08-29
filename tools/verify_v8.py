#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
PAPERS=ROOT/'papers'
expected={
 'paper-I-liouville-ensembles',
 'paper-II-cell-homogenization',
 'paper-III-theta-generator',
 'paper-IV-control-information',
 'paper-V-rigidity-tangent'}
actual={p.name for p in PAPERS.iterdir() if p.is_dir() and p.name.startswith('paper-')}
assert actual==expected,(actual,expected)
for name in sorted(expected):
    d=PAPERS/name
    for f in ['main.tex','references.bib','README.md','REFEREE_GUIDE.md']:
        assert (d/f).is_file(),f'{name}/{f}'
    forbidden=list(d.glob('main-v*.tex'))+list(d.glob('main-final.tex'))+list(d.glob('main-round*.tex'))
    assert not forbidden,forbidden
    main=(d/'main.tex').read_text()
    tex='\n'.join(x.read_text() for x in sorted(d.rglob('*.tex')))
    assert 'TL1-LIO-v1' in tex or name in {'paper-IV-control-information','paper-V-rigidity-tangent'}
    assert '\\begin{document}' in main and '\\end{document}' in main
manifest=(PAPERS/'SERIES_MANIFEST.yaml').read_text()
assert 'TL1-LIO-v1' in manifest
assert 'finite_microcanonical_path_law_is_Markov' not in manifest
for old in ['paper-I-path-ensembles','paper-I-specular-ensembles','paper-II-specular-homogenization']:
    assert not (PAPERS/old).exists()
result={
 'status':'PASS_STRUCTURE',
 'paper_count':5,
 'active_papers':sorted(expected),
 'one_main_tex_per_paper':True,
 'one_references_bib_per_paper':True,
 'historical_versions':0,
 'load_bearing_platform':'TL1-LIO-v1'}
out=ROOT/'status'/'VERIFICATION_RECEIPT.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
