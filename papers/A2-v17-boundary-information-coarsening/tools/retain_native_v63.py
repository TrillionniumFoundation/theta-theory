#!/usr/bin/env python3
"""Version-scoped publication of the three complete source-matched v63 entries.

The retained v56 engine validates producer/consumer auxiliaries and Git blobs.
Its functions are reused unchanged; only the permitted delivery path is new.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from retain_native_v56 import prepare, verify
from source_provenance import require, write_json


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('prepare','verify'))
    parser.add_argument('--destination',required=True,type=Path)
    parser.add_argument('--source-commit')
    parser.add_argument('--evidence',type=Path)
    parser.add_argument('--run-id',default='')
    parser.add_argument('--ref',default='INDEX')
    parser.add_argument('--attestation',action='store_true')
    args=parser.parse_args()
    require(re.fullmatch(r'deliveries/a2-v63/[0-9a-f]{40}',args.destination.as_posix()) is not None,
            'Unexpected delivery path')
    if args.operation=='prepare':
        require(args.source_commit is not None and args.destination.name==args.source_commit
                and args.evidence is not None,'Invalid preparation arguments')
        result=prepare(args.evidence.resolve(),args.destination,args.source_commit,args.run_id)
        readme=args.destination/'README.md'
        readme.write_text(readme.read_text().replace('v56 review ledger','v63 review ledger'))
    else:
        result=verify(args.destination,args.ref)
        if args.attestation:
            require(args.ref!='INDEX','An index check is not a publication attestation')
            write_json(args.destination/'COMMITTED_OBJECTS_VERIFIED.json',result)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
