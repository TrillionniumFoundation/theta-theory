#!/usr/bin/env python3
"""Prepare the three v56 native entries and verify fetched committed Git objects.

A filesystem receipt is deliberately NOT a publication receipt.  The workflow
force-stages only its delivery subtree, publishes a new products branch,
fetches it, verifies all Git blobs, and commits a separate attestation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from source_provenance import blob_id, require, safe_relative, sha256, write_json


def git(*args: str) -> bytes:
    p=subprocess.run(['git',*args],capture_output=True)
    require(p.returncode==0,'Git read failed: '+' '.join(args)+'\n'+p.stderr.decode(errors='replace'))
    return p.stdout


def validate(evidence: Path, source: str) -> dict:
    report=json.loads((evidence/'build-report.json').read_text())
    require(report['status']=='passed' and report['source_commit']==source,'Wrong or failed source build')
    for name,expected in report['evidence_files'].items():
        p=evidence/safe_relative(name)
        require(p.is_file() and not p.is_symlink() and p.stat().st_size==expected['bytes'] and sha256(p)==expected['sha256'],'Artifact mismatch: '+name)
    for stem in ('main','two_collision','rigidity'):
        item=report['entries'][stem]
        require(item['status']=='passed' and item['returncode']==0 and item['source_integrity']=='verified','Native source not verified: '+stem)
        require(sha256(evidence/(stem+'.pdf'))==item['product']['sha256'],'PDF mismatch: '+stem)
    for consumer,producers in (('main',('two_collision',)),('rigidity',('two_collision','main'))):
        imported=json.loads((evidence/(consumer+'-imported-generated-inputs.json')).read_text())
        recorder=json.loads((evidence/(consumer+'-recorder-inputs.json')).read_text())
        require(set(imported)=={p+'.aux' for p in producers},'Unexpected imported producer set: '+consumer)
        for producer in producers:
            aux=producer+'.aux'; info=imported[aux]
            require(info['producer_source_commit']==source and info['sha256']==sha256(evidence/aux)
                    and recorder['generated_inputs'][aux]['sha256']==info['sha256']
                    and info['producer_pdf_sha256']==report['entries'][producer]['product']['sha256']
                    and info['producer_recorder_sha256']==sha256(evidence/(producer+'-recorder-inputs.json')),
                    'Producer/consumer mismatch: '+consumer+'/'+aux)
    for normal in evidence.glob('*-normal.json'):
        opt=normal.with_name(normal.name.replace('-normal.json','-optimized.json'))
        require(opt.is_file() and normal.read_bytes()==opt.read_bytes(),'Optimization parity failed: '+normal.name)
    return report


def prepare(evidence: Path, destination: Path, source: str, run_id: str) -> dict:
    require(not destination.exists(),'Refusing to overwrite historical delivery')
    validate(evidence,source)
    files={}
    for p in sorted(evidence.iterdir()):
        require(p.is_file() and not p.is_symlink(),'Nonregular artifact entry')
        require(p.suffix.lower() not in ('.ttf','.otf','.pfb','.pfa','.woff','.woff2'),'Standalone font distribution prohibited')
        data=p.read_bytes()
        files[p.name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':blob_id(data)}
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(evidence,destination)
    receipt={'source_commit':source,'publication_run_id':run_id,'native_build_status':'passed',
      'retention_status':'Verified artifact copy only; publication is certified separately by COMMITTED_OBJECTS_VERIFIED.json',
      'mathematical_certification':False,'files':files}
    write_json(destination/'REPOSITORY_RETENTION.json',receipt)
    (destination/'README.md').write_text('# Source-matched native delivery\n\nSource commit: `'+source+'`.\n\nAll three complete native PDFs, their source archive, raw logs, recorders and build evidence are retained here. `REPOSITORY_RETENTION.json` hashes the copied artifact but does not claim publication. `COMMITTED_OBJECTS_VERIFIED.json` identifies the fetched products commit whose Git blobs were verified after push. Neither a build nor these hashes certify the mathematical theorems. Visual coverage is recorded separately in the v56 review ledger.\n')
    return receipt


def verify(destination: Path, ref: str) -> dict:
    index=ref=='INDEX'
    resolved='INDEX' if index else git('rev-parse','--verify',ref+'^{commit}').decode().strip()
    prefix=':' if index else resolved+':'
    def read(name: str) -> bytes:
        return git('cat-file','blob',prefix+(destination/safe_relative(name)).as_posix())
    receipt=json.loads(read('REPOSITORY_RETENTION.json'))
    errors=[]; verified={}
    for name,expected in receipt['files'].items():
        try:
            data=read(name)
            actual={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':blob_id(data)}
            require(actual==expected,'Git object differs: '+name)
            verified[name]=actual
        except Exception as exc:errors.append(name+': '+str(exc))
    require(not errors,'Missing or changed Git objects:\n'+'\n'.join(errors))
    report=json.loads(read('build-report.json'))
    require(report['source_commit']==receipt['source_commit'] and report['status']=='passed','Committed build report mismatch')
    return {'status':'passed','verified_ref':resolved,
      'verification_scope':'Git index, not publication' if index else 'Committed Git blobs read after resolving the requested ref',
      'source_commit':receipt['source_commit'],'destination':destination.as_posix(),
      'verified_file_count':len(verified),'files':verified,'mathematical_certification':False}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('prepare','verify'))
    parser.add_argument('--destination',required=True,type=Path)
    parser.add_argument('--source-commit')
    parser.add_argument('--evidence',type=Path)
    parser.add_argument('--run-id',default='local-diagnostic')
    parser.add_argument('--ref',default='INDEX')
    parser.add_argument('--attestation',action='store_true')
    args=parser.parse_args()
    require(re.fullmatch(r'deliveries/a2-v56/[0-9a-f]{40}',args.destination.as_posix()) is not None,'Unexpected delivery path')
    if args.mode=='prepare':
        require(args.source_commit is not None and args.destination.name==args.source_commit and args.evidence is not None,'Invalid preparation arguments')
        result=prepare(args.evidence.resolve(),args.destination,args.source_commit,args.run_id)
    else:
        result=verify(args.destination,args.ref)
        if args.attestation:
            require(args.ref!='INDEX','An index check is not a publication attestation')
            write_json(args.destination/'COMMITTED_OBJECTS_VERIFIED.json',result)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
