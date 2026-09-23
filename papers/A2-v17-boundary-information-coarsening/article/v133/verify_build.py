#!/usr/bin/env python3
"""Write an executed, source-bound mechanical receipt; not a mathematical certificate."""
from pathlib import Path
import hashlib
import json
import re
import fitz

ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'PROVENANCE_MANIFEST.json').read_text())
log=(ROOT/'geometry.log').read_text(errors='replace')
visited=set()
def visit(name):
    if name in visited: return ''
    p=ROOT/name
    if '..' in Path(name).parts or not p.is_file():
        raise RuntimeError(f'Missing/nonlocal LaTeX input: {name}')
    visited.add(name)
    text=p.read_text()
    return text+'\n'+''.join(visit(child) for child in re.findall(r'\\input\{([^}]+)\}',text))
source=visit('geometry.tex')
labels=re.findall(r'\\label\{([^}]+)\}',source)
with fitz.open(ROOT/'geometry.pdf') as pdf:
    pages=len(pdf); first=pdf[0].get_text()
    all_text='\n'.join(p.get_text() for p in pdf)
new=json.loads((ROOT/'evidence/REVISION133_EXACT.json').read_text())
old132=json.loads((ROOT/'evidence/REVISION132_EXACT.json').read_text())
old131=json.loads((ROOT/'evidence/REVISION131_EXACT.json').read_text())
generic=json.loads((ROOT/'evidence/GENERIC_BOUNDARY_CERTIFICATES.json').read_text())
checks={
 'pdf_exists':(ROOT/'geometry.pdf').stat().st_size>100000,
 'full_manuscript_not_abridged':pages>=71,
 'version_on_title_page':'Revision 133' in first,
 'no_undefined_references':'undefined references' not in log.lower(),
 'no_undefined_citations':'undefined citations' not in log.lower(),
 'no_latex_error':'! LaTeX Error' not in log and '\n! ' not in log,
 'no_duplicate_labels':len(labels)==len(set(labels)) and 'multiply defined' not in log.lower(),
 'all_inputs_local':True,
 'all_inherited_compiled_inputs_retained':set(manifest['inherited_compiled_inputs'])<=visited,
 'all_inherited_compiled_labels_retained':set(manifest['inherited_mathematical_labels'])<=set(labels),
 'all_source_hashes_match':all(sha(ROOT/p)==v for p,v in manifest['assembled_sha256'].items()),
 'new_exact_checks_passed':new['ok'],
 'both_nonzero_block_witnesses':len(new['two_diagonal_coefficient_polynomials'])==2,
 'all_24_raising_checks':new['raising_operator_checks']==24,
 'flag_line_all_30240_quadrics':new['flag_line_pluecker_quadrics_checked']==30240,
 'inherited132_checks_passed':old132['ok'] and old132['lie_generators_checked']==16,
 'inherited_smooth_witness_retained':old132['inherited_smooth_Cstar']['linear_quotient_determinant']=='27787/432',
 'inherited131_checks_passed':old131['ok'],
 'inherited_embedded_length_three':generic['generic_embedded_saturation']['a1_b3_W3']['embedded_vertex_length']==3,
 'readout_functoriality_exceptional_theorems_compiled':all(label in labels for label in [
  'lem:universal-schur-readout','lem:readout-exterior-twist','lem:common-g-functoriality',
  'thm:exceptional-component-fibres','cor:exceptional-candidate-bound','ex:exceptional-flag-line']),
 'inherited_descent_and_sharp_laws_compiled':all(label in labels for label in [
  'lem:galois-packet-descent','lem:power-certified-packets','prop:descended-packet-torsion',
  'thm:sharp-global-jacobian-depth','thm:generic-intrinsic-web']),
 'inverse_precedes_atlas':(ROOT/'geometry.tex').read_text().index('12-intrinsic-web')<(ROOT/'geometry.tex').read_text().index('01b-boundary-atlas'),
 'no_stale_revision_narrative':not re.search(r'(?:Revision 12[0-9]|preceding revision|this revision)',source),
}
receipt={
 'revision':133, 'source_commit':manifest['assembly_commit'],
 'reviewed_commit':manifest['reviewed_commit'], 'controlling_review_commit':manifest['controlling_review_commit'],
 'controlling_review':manifest['controlling_review'],
 'source_origin':'Complete immutable v132 source; guarded transformations and hash-checked overlays. Publication commit follows execution.',
 'pdf_pages':pages,'pdf_sha256':sha(ROOT/'geometry.pdf'),
 'checks':checks, 'compiled_inputs':sorted(visited), 'source_sha256':manifest['assembled_sha256'],
 'overfull_box_warnings':[line for line in log.splitlines() if 'Overfull' in line],
 'evidence_scope':{
  'scripts_executed':['exact_k3.py','exact_corank_two.py','stratified_rank_two.py',
    'boundary_atlas.py','generic_boundary_atlas.py','revision131_exact.py','revision132_exact.py','revision133_exact.py'],
  'new_exact_checks':new,
  'structural_proofs_not_machine_certified':new['structural_proofs_not_machine_certified'],
  'documentary_open':['Ballico 1993 full-text theorem-level comparison'],
  'not_claimed':['complete higher-corank W3/W4 embedded-primary atlas',
    'codimension or irreducible-component classification of all exceptional strata',
    'equality of component pairs implies isomorphism of exceptional failure schemes',
    'journal-issued referee acceptance or journal acceptance']},
 'ok':all(checks.values())}
(ROOT/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='source_sha256'},indent=2))
if not receipt['ok']: raise SystemExit('v133 mechanical verification failed')
