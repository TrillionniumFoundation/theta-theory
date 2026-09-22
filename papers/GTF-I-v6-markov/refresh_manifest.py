#!/usr/bin/env python3
"""Refresh only the new revision's input hashes after intentional source edits."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
PREFIX=ROOT.relative_to(REPO).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inherited_path=REPO/'papers/GTF-I-v5-intrinsic/SOURCE_MANIFEST.json'
    prior=json.loads(inherited_path.read_text())
    inputs=dict(prior['input_sha256'])
    for name,digest in inputs.items():
        if not (REPO/name).is_file() or sha(REPO/name)!=digest:
            raise SystemExit('Refusing changed inherited input: '+name)
    inputs[inherited_path.relative_to(REPO).as_posix()]=sha(inherited_path)
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if (p.is_file() and p.suffix in {'.tex','.py','.md','.json'}
            and 'evidence' not in rel.parts and '__pycache__' not in rel.parts
            and p.name!='SOURCE_MANIFEST.json'):
            inputs[p.relative_to(REPO).as_posix()]=sha(p)
    manifest={'edition':'GTF I sixth Markov revision',
      'review_commit':'ee210f3cfe3b4923ef51310e20cd8b20a6a367e1',
      'review_report_blob':'2fee1ac088b7452eb87423cf36d9dca9b55e138b',
      'review_report_path':'reviews/general-theta-foundations-i-v5-intrinsic-2026-09-22/REFEREE_REPORT.md',
      'reviewed_v5_snapshot':'1fe6b459213ab86e5e49872490a1ec05eb0e0741',
      'input_sha256':dict(sorted(inputs.items())),
      'preserved_trees':prior['preserved_trees'],
      'scope':'Hashes identify sources and preservation, not mathematical truth or independent review.'}
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print('Bound',len(inputs),'source inputs')
if __name__=='__main__':main()
