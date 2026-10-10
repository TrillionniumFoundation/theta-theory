#!/usr/bin/env python3
"""Build the native R9 and the unchanged R6 companion; never modify source."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import native_build
from supplement_build import cover_and_attach
from verify import ROOT, require, verify

COMPANION_SOURCE = '86472b72b62184ac542e7ea82c354b2c293ef59e'
COMPANION_TREE = '0b3839c841b02a173745d6d4fb3d997712ea9fe0'


def run(command):
    proc = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError('command failed: ' + repr(command) + '\n' + proc.stdout[-16000:])
    return proc.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-sha', default=os.environ.get('SOURCE_COMMIT'))
    parser.add_argument('--expected-tree')
    parser.add_argument('--output', default=str(ROOT / 'artifacts'))
    parser.add_argument('--receipt', default=str(ROOT / 'evidence' / 'BUILD_RECEIPT.json'))
    args = parser.parse_args()
    output = Path(args.output).resolve()
    receipt = Path(args.receipt).resolve()
    output.mkdir(parents=True, exist_ok=True)
    audit_before = verify()
    companion = ROOT.parent / 'r6-operational-transfer'
    require((companion / 'build.py').is_file(), 'missing pinned complete R6 companion')
    with tempfile.TemporaryDirectory(prefix='theta-r9-receipts-') as tmp:
        tmp = Path(tmp)
        native_receipt = tmp / 'native.json'
        original_argv = sys.argv[:]
        sys.argv = ['native_build.py', '--output', str(output), '--receipt', str(native_receipt)]
        if args.source_sha:
            sys.argv += ['--source-sha', args.source_sha]
        if args.expected_tree:
            sys.argv += ['--expected-tree', args.expected_tree]
        native_build.PAPER = 'General_Theta_Foundations_I_restart_r9.pdf'
        try:
            native_build.main()
        finally:
            sys.argv = original_argv
        (output / 'LATEX_BUILD.log').rename(output / 'NATIVE_LATEX_BUILD.log')
        companion_receipt = tmp / 'companion.json'
        run([sys.executable, str(companion / 'build.py'), '--source-sha', COMPANION_SOURCE,
             '--expected-tree', COMPANION_TREE, '--output', str(output),
             '--receipt', str(companion_receipt)])
        (output / 'General_Theta_Foundations_I_restart_r6.pdf').rename(
            output / 'General_Theta_Foundations_I_retained_technical_text.pdf')
        (output / 'LATEX_BUILD.log').rename(output / 'COMPANION_LATEX_BUILD.log')
        result = json.loads(native_receipt.read_text())
        retained = json.loads(companion_receipt.read_text())
        require(verify() == audit_before, 'native source changed during complete build')
        require(retained['native_source_tree_sha'] == COMPANION_TREE, 'companion binding mismatch')
        result['component'] = 'General Theta Foundations I restart R9'
        result['hosted_run_id'] = os.environ.get('HOSTED_RUN_ID') or os.environ.get('GITHUB_RUN_ID')
        result['companion'] = retained
        result['supplement'] = cover_and_attach(output/'General_Theta_Foundations_I_retained_technical_text.pdf', output/'General_Theta_Foundations_I_Supplement_S.pdf')
        result['companion_pdf'] = 'General_Theta_Foundations_I_Supplement_S.pdf'
        result['total_isolated_pdf_builds'] = 6
        result['technical_pdf_builds'] = 4
        result['cover_pdf_builds'] = 2
        result['limitations'] = ('Complete R9 native source and complete unchanged R6 companion only; '
                                'not every paper or historical version in the repository. '
                                'Finite regressions and reproducible PDFs do not prove theorems.')
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
