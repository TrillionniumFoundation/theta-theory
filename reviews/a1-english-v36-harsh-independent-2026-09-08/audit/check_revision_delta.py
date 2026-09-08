#!/usr/bin/env python3
"""Check the bounded v35-to-v36 active source delta, without editing either tree.

Usage: python check_revision_delta.py --old-root V35 --new-root V36
This checks source preservation and exact algebra, not general theorem correctness.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def blocks(root: Path, manifest: dict, names: str) -> Counter:
    found = Counter()
    pattern = re.compile(r'\\begin\{('+names+r')\}.*?\\end\{\1\}', re.S)
    for name in manifest:
        for match in pattern.finditer((root/name).read_text()):
            found[match.group(0)] += 1
    return found


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--old-root', type=Path, required=True)
    ap.add_argument('--new-root', type=Path, required=True)
    args = ap.parse_args()
    base_path = args.new_root/'verification-v35/NATIVE_BUILD_V35.json'
    current_path = args.new_root/'verification-v36/NATIVE_BUILD_V36.json'
    require(blob(base_path.read_bytes()) == '1e5f92cf41b563779ad702c85ee440a470a689fe', 'Base manifest identity')
    require(blob(current_path.read_bytes()) == 'f4dbd653b585f0fa446d95653b247b3bffd14268', 'Current manifest identity')
    old = json.loads(base_path.read_text())['source_git_blob']
    delta = json.loads(current_path.read_text())['source_manifest']
    new = dict(old)
    for name in delta['delete']:
        del new[name]
    new.update(delta['replace_or_add'])
    for root, manifest in ((args.old_root, old), (args.new_root, new)):
        require(all(blob((root/name).read_bytes()) == sha for name,sha in manifest.items()), 'Source mismatch')
    common = set(old)&set(new)
    same = sorted(p for p in common if old[p] == new[p])
    changed = sorted(p for p in common if old[p] != new[p])
    require(len(old)==len(new)==80 and len(same)==77 and changed==['main.tex'], 'Unexpected active delta')
    summary = {}
    for key,names in (('statement_blocks','theorem|lemma|proposition|corollary|definition|remark|example'),('proof_blocks','proof')):
        before,after = blocks(args.old_root,old,names),blocks(args.new_root,new,names)
        summary[key] = {'old':sum(before.values()), 'new':sum(after.values()),
                        'verbatim_multiset_matches':sum((before&after).values())}
    require(summary['statement_blocks']=={'old':222,'new':222,'verbatim_multiset_matches':220}, 'Unexpected statement block delta')
    require(summary['proof_blocks']=={'old':210,'new':210,'verbatim_multiset_matches':209}, 'Unexpected proof block delta')
    H=F(16)
    requirement=5*(3+F(1,16))
    require(requirement==F(245,16) and requirement<H, 'Common H bound')
    # Exponent pairs (rho,tau) after substituting each balancing budget.
    terms=((F(0),F(0),F(-1,3)),(F(1,2),F(0),F(-1,4)),(F(4,9),F(2,9),F(-2,9)))
    def substitute(budget):
        return [[str(a+c*budget[0]),str(b+c*budget[1])] for a,b,c in terms]
    at_first=substitute((-6,0)); at_second=substitute((2,-8))
    require(at_first[:2]==[['2','0'],['2','0']], 'First balance')
    require(at_second[1:]==[['0','2'],['0','2']], 'Second balance')
    result={'schema':'v36-independent-bounded-delta-v1',
        'reviewed_commit':'8f074b8027627a71a81a362b9d15f47975e1f3ae',
        'old_active_source_count':len(old),'new_active_source_count':len(new),
        'same_path_and_bytes':len(same),'changed_common_paths':changed,
        'old_only_paths':sorted(set(old)-set(new)), 'new_only_paths':sorted(set(new)-set(old)),
        **summary,'normalization':{'H':str(H),'maximum_requirement':str(requirement),'strict_margin':str(H-requirement)},
        'envelope_term_exponents_at_first_balance':at_first,
        'envelope_term_exponents_at_second_balance':at_second,
        'scope':'Active input closure and block-text preservation only; does not count or certify every inactive historical file or proof.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
