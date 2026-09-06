#!/usr/bin/env python3
"""Anchor v14 historical snapshots and preservation records to the reviewed v13.

The complete new mathematical sources are already committed, not generated
by this script. Source snapshots, opening prose/notation and manifests are
prepared here. Publication fails unless all source bytes match the locally
built and tested revision's predeclared manifest digest.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
BASE = REPO/'papers/A1-english-v13'
ROOT = REPO/'papers/A1-english-v14'
SOURCE_DIGEST = '1fe2a9fa1f304664889baf1ba3d6f60112e01e484d0613e7c015812630a1a682'
PRESERVATION_DIGEST = '643e5f7c50942b98acd5a47f80e0fdecbc2149e29638771b0911b6c6ade13dcd'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    tree = subprocess.check_output(['git','rev-parse','HEAD:papers/A1-english-v13'],cwd=REPO,text=True).strip()
    if tree != '56a4340a02dbc10a5d7ed510f9c1beee38aa6d64':
        raise ValueError('The reviewed v13 source subtree changed')
    data = (BASE/'SOURCE_MANIFEST.json').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob != 'de4345eb94c864f2e102f4a013f95f1cfc5be1ab':
        raise ValueError('The reviewed source manifest changed')
    manifest = json.loads(data)
    for name,expected in manifest['sha256'].items():
        if sha((BASE/name).read_bytes()) != expected:
            raise ValueError('Reviewed source hash mismatch: '+name)
    snapshots = ['BUILD_REPORT.json','PRESERVATION_REPORT.json','SOURCE_MANIFEST.json',
        'README.md','RESPONSE_TO_REFEREE.md','HISTORICAL_DERIVATION_MAP.md',
        'LITERATURE_VERIFICATION.md','NUMERICAL_EVIDENCE.md','PROOF_LEDGER.md',
        'VISUAL_INSPECTION.md','build.py','validate.py','main.tex']
    (ROOT/'history').mkdir(exist_ok=True)
    for name in snapshots:
        shutil.copyfile(BASE/name,ROOT/'history'/('V13_'+name))
    shutil.copyfile(BASE/'sections/introduction.tex',ROOT/'history/V13_introduction.tex')
    with tempfile.TemporaryDirectory() as temporary:
        working = Path(temporary)/'v13'
        shutil.copytree(BASE,working,ignore=shutil.ignore_patterns('build','validation','__pycache__','*.pdf','*.aux','*.log','*.out'))
        subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=working,check=True)
        expanded = (working/'build/expanded.tex').read_text()
    proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',expanded,re.S)
    ledger = {'revision':13,'submission':'fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6',
        'review':'00b0844a7c2fb16b3231abf163d5004fd9e253cd',
        'artifact_sha256':'2e567e4267501d0ca6789e485f817656169b34a0b27940f002c32728419dd0dd',
        'source_manifest_blob':blob,'verified_source_files':len(manifest['sha256']),
        'proof_sha256':[sha(x.encode()) for x in proofs],
        'named_results':re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}',expanded)}
    pattern = r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}'
    ledger['statement_sha256'] = [sha(m.group().encode()) for m in re.finditer(pattern,expanded,re.S)]
    encoded = (json.dumps(ledger,indent=2)+'\n').encode()
    if sha(encoded) != PRESERVATION_DIGEST:
        raise ValueError('The complete v13 proof/statement inventory differs from the checked baseline')
    (ROOT/'V13_PRESERVATION_MANIFEST.json').write_bytes(encoded)
    classical = (BASE/'sections/classical.tex').read_text()
    opening = ('\\section{Interpolation and the analytic inputs}\\label{sec:classical}\n'
        'The interpolation identities in this section are classical. They fix the\n'
        'normalization used in the geometric argument; they do not assert\n'
        'statistical attainment. The independent repository derivation of the\n'
        'finite spectral comparison is acknowledged in \\cite{A1v9note}.\n\n')
    (ROOT/'sections/classical.tex').write_text(opening+classical[classical.index('\\begin{lemma}'):])
    # Restore definitions used by the unchanged exact-information statements.
    intro_path = ROOT/'sections/introduction.tex'
    intro = intro_path.read_text()
    anchor = 'and let $mA$ denote sums of exactly $m$ members of $A$, with $0A=\\{0\\}$.\n'
    addition = ('Write $h_A(m)=|mA|$. For the exact information statements let\n'
        '$I=[l,u]$, where $0\\le l<u<\\infty$, and let the prior have full support\n'
        'on $I$. The collision-uniform results below specialize to $I=[0,1]$.\n')
    if addition not in intro:
        if intro.count(anchor) != 1:
            raise ValueError('Exact setup notation anchor is not unique')
        intro_path.write_text(intro.replace(anchor,anchor+addition))
    visual_path = ROOT/'VISUAL_INSPECTION.md'
    visual = visual_path.read_text()
    note = ('After the final notation audit restored the definitions of $h_A(m)$ and\n'
        'the interval $I$, pages 1 and 2 were rendered and inspected again at readable\n'
        'resolution. The page count and the cited theorem locators are unchanged.\n\n')
    if note not in visual:
        anchor = 'This is a rendered-layout check, not an independent proof review of all\n72 pages.'
        if visual.count(anchor) != 1:
            raise ValueError('Visual-inspection note anchor is not unique')
        visual_path.write_text(visual.replace(anchor,note+anchor))
    # Remove stale generated receipts only in the new directory, never its baseline.
    shutil.rmtree(ROOT/'validation',ignore_errors=True)
    for name in ['main.pdf','BUILD_REPORT.json','PRESERVATION_REPORT.json']:
        (ROOT/name).unlink(missing_ok=True)
    subprocess.run([sys.executable,'manifest.py','--write'],cwd=ROOT,check=True)
    source = (ROOT/'SOURCE_MANIFEST.json').read_bytes()
    if sha(source) != SOURCE_DIGEST:
        print(source.decode())
        raise ValueError('Transmitted source differs from the locally verified revision')
    print(json.dumps({'verified_v13_sources':len(manifest['sha256']),
        'retained_proofs':len(proofs),'retained_statements':len(ledger['statement_sha256']),
        'v14_source_manifest_sha256':sha(source)},indent=2))

if __name__ == '__main__':
    main()
