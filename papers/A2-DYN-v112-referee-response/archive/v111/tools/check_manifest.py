#!/usr/bin/env python3
"""Check active manuscript bytes and explicitly scoped claims."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check():
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 111, 'revision identity')
    for name, expected in manifest['active_blobs'].items():
        require(blob((ROOT / name).read_bytes()) == expected, 'changed active bytes: ' + name)
    require(manifest['active_blobs']['model.tex'] == '6af1dcb4548e1b5dd82b9a330dead6e04fd09797',
            'original physical model or pointwise target changed')
    claims = json.loads((ROOT / 'PUBLICATION_STATUS.json').read_text())
    require(claims == manifest['claims'], 'inconsistent claim ledgers')
    for key in ('full_raw_return_LLT_proved', 'primary_referee_request_closed',
                'remaining_localized_shortage_height_decay_proved',
                'clearance_witness_target_roof_summation_proved',
                'independent_human_review', 'formal_proof_certificate'):
        require(claims[key] is False, 'unsupported claim: ' + key)
    require(claims['original_source_preserved_by_positive_identity'] is True, 'source preservation')
    return dict(status='passed', revision=111, checked_active_files=len(manifest['active_blobs']),
                scope='active source bytes and claim consistency only', formal_proof_certificate=False)


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
