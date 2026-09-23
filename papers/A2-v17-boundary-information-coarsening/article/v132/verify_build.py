#!/usr/bin/env python3
"""Source-bound mechanical receipt; never a certificate of structural proofs."""
from pathlib import Path
import hashlib
import json
import re
import fitz
ROOT = Path(__file__).resolve().parent
log = (ROOT/'geometry.log').read_text(errors='replace')
with fitz.open(ROOT/'geometry.pdf') as doc:
    pages=len(doc); first=doc[0].get_text()
source='\n'.join(p.read_text() for p in sorted(ROOT.rglob('*.tex')))
includes=re.findall(r'\\input\{([^}]+)\}',source)
manifest=json.loads((ROOT/'PROVENANCE_MANIFEST.json').read_text())
new=json.loads((ROOT/'evidence/REVISION132_EXACT.json').read_text())
old=json.loads((ROOT/'evidence/REVISION131_EXACT.json').read_text())
generic=json.loads((ROOT/'evidence/GENERIC_BOUNDARY_CERTIFICATES.json').read_text())
labels=re.findall(r'\\label\{([^}]+)\}',source)
checks={
 'pdf_exists':(ROOT/'geometry.pdf').stat().st_size>100000,
 'expanded_manuscript_retains_full_volume':pages>=63,
 'version_on_title_page':'Revision 132' in first,
 'no_undefined_references':'undefined references' not in log.lower(),
 'no_undefined_citations':'undefined citations' not in log.lower(),
 'no_latex_error':'! LaTeX Error' not in log,
 'all_tex_inputs_local':all((ROOT/p).is_file() and '..' not in Path(p).parts for p in includes),
 'no_duplicate_labels':len(labels)==len(set(labels)),
 'all_inherited_mathematical_labels_preserved':set(manifest['inherited_mathematical_labels'])<=set(labels),
 'new_exact_script_passed':new['ok'],
 'all_16_gl4_generators_checked':new['lie_generators_checked']==16,
 'same_smooth_witness_separates':new['inherited_smooth_Cstar']['linear_quotient_determinant']=='27787/432',
 'inherited_revision131_exact_passed':old['ok'],
 'inherited_generic_embedded_length_three':generic['generic_embedded_saturation']['a1_b3_W3']['embedded_vertex_length']==3,
 'source_hashes_match':all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in manifest['assembled_sha256'].items()),
 'no_stale_revision_prose':not re.search(r'(?:Revision 12[0-9]|preceding revision|this revision)', '\n'.join(p.read_text() for p in (ROOT/'parts').glob('*.tex'))),
 'no_finite_image_descent_shortcut':'Their finite images descend the packets' not in source,
 'two_descent_mechanisms_present':all(s in source for s in ['lem:galois-packet-descent','lem:power-certified-packets','prop:descended-packet-torsion']),
 'intrinsic_web_theorem_present':'thm:generic-intrinsic-web' in source,
}
receipt={
 'revision':132, 'source_commit':manifest['assembly_commit'],
 'source_origin':'Expanded source copied from immutable reviewed v131 source, modified only by recorded v132 patch; publication commit follows build and is bound by hashes.',
 'reviewed_commit':manifest['reviewed_commit'],
 'controlling_review':manifest['controlling_review'],
 'pdf_pages':pages, 'pdf_sha256':hashlib.sha256((ROOT/'geometry.pdf').read_bytes()).hexdigest(),
 'checks':checks, 'source_sha256':manifest['assembled_sha256'],
 'overfull_box_warnings':[s for s in log.splitlines() if 'Overfull' in s],
 'evidence_scope':{
  'scripts_executed':['exact_k3.py','exact_corank_two.py','stratified_rank_two.py','boundary_atlas.py','generic_boundary_atlas.py','revision131_exact.py','revision132_exact.py'],
  'new_exact_checks':['35-by-210 Jacobian matrix','C C^*=48 I','idempotent rank-35 projector','all sixteen gl4 matrix-unit equivariance identities','five-coordinate diagonal Pluecker witness','two quadratic restrictions and reduced pencil intersection','same separating condition at independently certified smooth C_*'],
  'structural_proofs_not_machine_certified':['effective Galois ideal descent and cocycle','power-certified geometric packets in arbitrary characteristic','downstairs no-new-torsion and local lengths','intrinsic deepest stratum and tensor ruling orientation','Cauchy coefficient-space readout','generic intrinsic web reconstruction and Torelli-packet separation','all inherited structural geometric proofs'],
  'documentary_open':['Ballico 1993 full-text theorem-by-theorem comparison'],
  'not_claimed':['complete transverse W3/W4 primary atlas at coranks three/four','complete primary specialization across the seven-component incidence family','numerical degree of the K3-only Torelli map','reconstruction at every exceptional web','journal acceptance']},
 'ok':all(checks.values())}
(ROOT/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='source_sha256'},indent=2))
if not receipt['ok']: raise SystemExit('v132 mechanical verification failed')
