from pathlib import Path
import hashlib
import json
import re
import subprocess
import fitz

ROOT = Path(__file__).resolve().parent
log = (ROOT / 'geometry.log').read_text(errors='replace')
with fitz.open(ROOT / 'geometry.pdf') as doc:
    pages = len(doc)
    first = doc[0].get_text()
    text = '\n'.join(p.get_text() for p in doc)
texfiles = list(ROOT.rglob('*.tex'))
source = '\n'.join(p.read_text() for p in texfiles)
includes = re.findall(r'\\input\{([^}]+)\}', source)
local = all((ROOT / p).is_file() and '..' not in Path(p).parts for p in includes)
cert = json.loads((ROOT / 'evidence/REVISION131_EXACT.json').read_text())
generic = json.loads((ROOT / 'evidence/GENERIC_BOUNDARY_CERTIFICATES.json').read_text())
checks = {
  'pdf_exists': (ROOT / 'geometry.pdf').stat().st_size > 100000,
  'pdf_retains_full_volume': pages >= 40,
  'version_on_title_page': 'Revision 131' in first,
  'no_undefined_references': 'undefined references' not in log.lower(),
  'no_undefined_citations': 'undefined citations' not in log.lower(),
  'no_latex_error': '! LaTeX Error' not in log,
  'all_tex_inputs_local': local,
  'new_exact_script_passed': cert['ok'],
  'inherited_generic_embedded_length_three': generic['generic_embedded_saturation']['a1_b3_W3']['embedded_vertex_length'] == 3,
  'no_old_coefficient_one_assertion': 'coefficient of the unique' not in source,
}
manifest = json.loads((ROOT / 'PROVENANCE_MANIFEST.json').read_text())
checks['assembled_source_hashes_match'] = all(
    hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == sha
    for p, sha in manifest['assembled_sha256'].items())
labels = re.findall(r'\\label\{([^}]+)\}', source)
checks['no_duplicate_labels'] = len(labels) == len(set(labels))
receipt = {
 'revision': 131,
 'source_commit': manifest['assembly_commit'],
 'source_origin': 'Expanded v131 source assembled from the immutable reviewed commit plus staging files at source_commit; publication commit is subsequent and is checked by file hashes.',
 'reviewed_commit': manifest['reviewed_commit'],
 'controlling_review': manifest['controlling_review'],
 'pdf_pages': pages,
 'pdf_sha256': hashlib.sha256((ROOT / 'geometry.pdf').read_bytes()).hexdigest(),
 'checks': checks,
 'source_sha256': manifest['assembled_sha256'],
 'overfull_box_warnings': [line for line in log.splitlines() if 'Overfull' in line],
 'evidence_scope': {
   'scripts_executed': ['exact_k3.py','exact_corank_two.py','stratified_rank_two.py','boundary_atlas.py','generic_boundary_atlas.py','revision131_exact.py'],
   'exact_finite_checks': ['inherited generic Groebner and saturation regressions','integer Fischer polynomial pairing and coefficient 1/35','Sym^2 of a generic 2x3 matrix maximal-minor coefficient spaces','squarefree incidence intersection','binomial layer-length sum'],
   'structural_proofs_not_machine_certified': ['primary-quotient spreading and packet exhaustion','no-new-torsion and relative local lengths','global sharp depth and minimal supports','proper incidence resolution and geometric cross-corank construction','general quotient-induced symbolic-power and colon theorems'],
   'documentary_open': ['Ballico 1993 full-text theorem comparison'],
   'not_claimed': ['complete embedded W3/W4 primary atlas','original-web generic injectivity','journal acceptance']
 },
 'ok': all(checks.values())
}
(ROOT / 'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'source_sha256'}, indent=2))
if not receipt['ok']:
    raise SystemExit('v131 verification failed')
