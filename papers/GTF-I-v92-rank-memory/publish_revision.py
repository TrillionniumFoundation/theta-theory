#!/usr/bin/env python3
"""Print source-qualified publication inventory; does not commit or push."""
import json
from build_revision import ROOT,require,git,check_source,source_commit_inventory
inv,_=check_source()
r=json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
require(r['source_commit']==git('rev-parse','HEAD') and r['qualified_git_source'] and r['isolated_native_rebuild'] and r['standalone_journal_rebuild'],'publish only the qualified native source')
source_commit_inventory(r['source_commit'],inv)
print(json.dumps({'schema':'gtf89.publication-plan/1','source_commit':r['source_commit'],'publication_parent':r['source_commit'],'generated_manifest':'evidence/PACKAGE_MANIFEST.json','documents':r['documents'],'read_only':True},indent=2,sort_keys=True))
