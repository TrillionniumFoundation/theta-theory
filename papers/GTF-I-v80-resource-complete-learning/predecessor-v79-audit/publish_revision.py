#!/usr/bin/env python3
"""Emit generated-artifact inventory at the qualified v79 native source."""
from pathlib import Path
import json
from build_revision import ROOT, DOCS, sha, require, git_output, committed_source, check_source

def main():
    checked, inv = check_source(ROOT)
    r = json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
    head = git_output(ROOT, 'rev-parse', 'HEAD')
    require(r['schema'] == 'gtf79.build/1' and r['qualified_git_source']
            and r['source_commit'] == head and r['isolated_native_rebuild']
            and r['standalone_journal_rebuild'], 'current native build not qualified')
    committed_source(ROOT, head, inv)
    files = {n: sha((ROOT/n).read_bytes()) for n in DOCS.values()}
    for p in sorted((ROOT/'evidence').rglob('*')):
        if p.is_file(): files[p.relative_to(ROOT).as_posix()] = sha(p.read_bytes())
    print(json.dumps({'schema': 'gtf79.publication-plan/1', 'source_commit': head,
                      'publication_parent': head, 'generated_files': files,
                      'documents': r['documents'], 'read_only': True}, indent=2, sort_keys=True))

if __name__ == '__main__': main()
