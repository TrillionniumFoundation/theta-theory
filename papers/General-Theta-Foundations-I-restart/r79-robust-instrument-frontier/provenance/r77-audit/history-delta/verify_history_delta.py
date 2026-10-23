#!/usr/bin/env python3
"""Authenticate the unchanged R76 history corpus plus the small R77 deltas.

The check reconstructs the exact indexed member set and bytes. It does not
claim a recompressed tarball has the same incidental gzip metadata as another
archive. No archive is extracted to disk, no network or Git operation occurs,
and no mathematical theorem is checked.
"""
import argparse
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticate_file(path, fixed):
    raw=path.read_bytes()
    require(len(raw)==fixed['bytes'] and sha(raw)==fixed['sha256'],
            'Archive/index identity differs: '+str(path))
    return raw


def members(raw, name):
    result={}
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
        for member in archive:
            require(member.isfile(), 'Nonregular archive member: '+member.name)
            path=Path(member.name)
            require(len(path.parts)==2 and path.parts[0]=='blobs' and path.suffix=='.txt',
                    'Unexpected archive path: '+member.name)
            blob=path.stem
            require(len(blob)==40 and all(c in '0123456789abcdef' for c in blob),
                    'Invalid Git blob name: '+member.name)
            require(blob not in result, 'Duplicate archive member: '+member.name)
            content=archive.extractfile(member).read()
            require(len(content)==member.size, 'Truncated archive member: '+member.name)
            got=hashlib.sha1(f'blob {len(content)}\0'.encode()+content).hexdigest()
            require(got==blob, 'Content/Git identity mismatch: '+member.name)
            result[blob]={'bytes':len(content),'sha256':sha(content)}
    return result


def check_index(index_raw, reconstructed, name):
    index=json.loads(gzip.decompress(index_raw))
    expected={row['git_blob']:{'bytes':row['bytes'],'sha256':row['sha256']} for row in index}
    require(len(expected)==len(index), 'Duplicate indexed member: '+name)
    require(reconstructed==expected, 'Reconstructed member identities differ from '+name)
    return {'unique_text_blobs':len(expected),'authenticated_uncompressed_bytes':sum(x['bytes'] for x in expected.values())}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',required=True,type=Path)
    base=parser.add_mutually_exclusive_group(required=True)
    base.add_argument('--base',type=Path,help='unchanged complete R76 historical archive')
    base.add_argument('--base-parts',type=Path,help='directory containing its five unchanged original parts')
    parser.add_argument('--delta',required=True,type=Path)
    parser.add_argument('--index',required=True,type=Path,help='fresh 6832-member named-line index')
    parser.add_argument('--extension',type=Path,help='optional all-ref scope extension corpus')
    parser.add_argument('--extension-index',type=Path)
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    manifest_raw=args.manifest.read_bytes();manifest=json.loads(manifest_raw)
    require(manifest['schema']=='theta.r77.history-base-plus-delta.v1','Unknown manifest schema')
    if args.base:
        base_raw=authenticate_file(args.base,manifest['base'])
    else:
        chunks=[]
        for part in manifest['base']['parts']:
            chunks.append(authenticate_file(args.base_parts/Path(part['path']).name,part))
        base_raw=b''.join(chunks)
        require(len(base_raw)==manifest['base']['bytes'] and sha(base_raw)==manifest['base']['sha256'],
                'Concatenated base archive identity differs')
    base_members=members(base_raw,'base')
    require(len(base_members)==manifest['base']['member_count'],'Wrong base member count')
    delta_raw=authenticate_file(args.delta,manifest['delta'])
    delta_members=members(delta_raw,'delta')
    require(len(delta_members)==manifest['delta']['member_count'],'Wrong delta member count')
    require(not set(base_members)&set(delta_members),'Delta repeats a base member')
    combined={**base_members,**delta_members}
    index_raw=authenticate_file(args.index,manifest['current_index'])
    current=check_index(index_raw,combined,'current full index')
    extension=None
    require(bool(args.extension)==bool(args.extension_index),'Extension archive/index must be supplied together')
    if args.extension:
        extra_raw=authenticate_file(args.extension,manifest['all_ref_extension']['archive'])
        extra=members(extra_raw,'all-ref extension')
        require(not set(extra)&set(combined),'All-ref extension repeats a reconstructed member')
        extra_index=authenticate_file(args.extension_index,manifest['all_ref_extension']['index'])
        extension=check_index(extra_index,extra,'all-ref extension index')
        combined.update(extra)
    receipt={'schema':'theta.r77.history-delta-reconstruction.v1','status':'PASS',
             'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'manifest_sha256':sha(manifest_raw),
             'base_archive_sha256':sha(base_raw),'base_members':len(base_members),
             'delta_archive_sha256':sha(delta_raw),'delta_members':len(delta_members),
             'current_named_line_reconstruction':current,'all_ref_extension':extension,
             'total_unique_text_blobs':len(combined),
             'total_authenticated_uncompressed_bytes':sum(x['bytes'] for x in combined.values()),
             'duplicate_members':0,'hash_mismatches':0,
             'scope':'Exact archive-member and source-index reconstruction only. This is not reproof, formal verification, independent human assessment or an editorial decision.'}
    raw=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
    if args.receipt:args.receipt.write_text(raw)
    print(raw,end='')


if __name__=='__main__':
    main()
