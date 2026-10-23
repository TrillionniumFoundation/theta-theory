#!/usr/bin/env python3
"""Portable full current census/report and immediate-source reconstruction."""
import argparse, hashlib, importlib.util, json, shutil, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def need(x,msg):
    if not x: raise ValueError(msg)

def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def main():
    audit=ROOT/'audit/current-337'
    mapping=json.loads((ROOT/'audit/ROOF_SPECTRUM_PREDECESSOR_FILE_IDENTITIES.json').read_text())
    # Rebuild only the exact selected 220-file baseline, never recursive history.
    with tempfile.TemporaryDirectory(prefix='a2-dyn-337-source-') as temp:
        baseline=Path(temp)
        for row in mapping:
            data=(ROOT/row['preserved_copy']).read_bytes()
            need(len(data)==row['bytes'] and sha(data)==row['sha256'] and blob(data)==row['git_blob'],
                 'Lost exact immediate source '+row['path'])
            dst=baseline/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
            if row['active_byte_identical']:
                need(sha((ROOT/row['path']).read_bytes())==row['sha256'],
                     'Modified inherited source '+row['path'])
        spec=importlib.util.spec_from_file_location('fresh337',audit/'verify_current_reconciliation.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        fresh=module.run(baseline,audit/'remote-refs-snapshot.json',audit)
    reports=json.loads((audit/'review-text-inventory.json').read_text())
    for row in reports:
        data=(ROOT/'history/all-91-review-heads'/(row['sha']+'.md')).read_bytes()
        need(len(data)==row['bytes'] and sha(data)==row['sha256'] and blob(data)==row['blob'],
             'Historical report mismatch '+row['sha'])
    need(len(reports)==91 and len({x['sha'] for x in reports})==91,'Incomplete report body census')
    native=[r for r in mapping if r['path'].endswith('.tex') and not r['path'].startswith('history/')]
    cores=[r for r in native if r['path'].startswith('core/')]
    need(len(native)==90 and len(cores)==78,'Immediate source completeness')
    need(all(r['active_byte_identical'] for r in cores),'Inherited proof body changed')
    result={'status':'PASS','selected_baseline_files_reconstructed':len(mapping),
            'native_predecessor_inputs':len(native),'byte_identical_inherited_core_proofs':len(cores),
            'all_report_bodies_rehashed':len(reports),'fresh_census':fresh,
            'scope':'Source identities and actual recorded CI state, not continuous mathematical validity.'}
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','selected_baseline_files_reconstructed',
                    'native_predecessor_inputs','byte_identical_inherited_core_proofs','all_report_bodies_rehashed']}))

if __name__=='__main__':main()
