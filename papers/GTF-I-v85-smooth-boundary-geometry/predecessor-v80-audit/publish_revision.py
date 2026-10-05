#!/usr/bin/env python3
"""Validate v80 artifacts and emit a read-only Git Data publication inventory.

The caller creates blobs and a publication commit whose sole parent is the
qualified native source. This program never commits, pushes or rebuilds files.
"""
import json
import sys
sys.dont_write_bytecode = True
from build_revision import ROOT, require, git_output, committed_source, verify_artifacts, generated_inventory


def main():
    receipt, inventory, _ = verify_artifacts(ROOT)
    head = git_output(ROOT, 'rev-parse', 'HEAD')
    require(receipt['source_commit'] == head, 'publish from the actual qualified native source commit')
    committed_source(ROOT, head, inventory)
    require(git_output(ROOT, 'rev-parse', head+'^{tree}') == receipt['source_git_tree'],
            'qualified native Git tree differs')
    require(not git_output(ROOT, 'status', '--porcelain', '--untracked-files=no'),
            'tracked native checkout changed before publication')
    files = generated_inventory(ROOT)
    print(json.dumps({'schema': 'gtf80.publication-plan/1', 'source_commit': head,
                      'source_git_tree': receipt['source_git_tree'], 'publication_parent': head,
                      'generated_files': files, 'documents': receipt['documents'],
                      'source_inventory_sha256': receipt['source_inventory_sha256'],
                      'artifact_digests_cross_checked': True,
                      'direct_source_child_required': True, 'read_only': True},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
