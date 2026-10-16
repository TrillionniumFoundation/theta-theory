#!/usr/bin/env python3
"""Local source check; --repository additionally checks real Git ancestry and isolation."""
from pathlib import Path
import argparse,json,subprocess
from check_manifest import check,require
P=Path(__file__).resolve().parents[1]
BASE='d98549fc721f757ad2a4b5918d57110368acbf9f'
ACTIVE='papers/A2-DYN-v115-double-clearance-author-revision/'
WORKFLOW='.github/workflows/a2-dyn-v115-double-clearance-20261015.yml'
def git(*args): return subprocess.check_output(['git',*args],cwd=P,text=True).strip()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repository',action='store_true');args=parser.parse_args()
    out=check()
    if args.repository:
        git('cat-file','-e',BASE+'^{commit}');git('merge-base','--is-ancestor',BASE,'HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v112-referee-response')=='5e74283f6084ea46f1aae0ba398cbca4c8ea821f','v112 original packet changed')
        require(git('rev-parse','HEAD:papers/A2-DYN-clearance-roof-2026-10-15')=='c2e9e83f39985a34690300433f4b40de4f1f88ac','prior v114 original article changed')
        require(git('rev-parse',f'HEAD:{ACTIVE}provenance/v114-frozen')=='c2e9e83f39985a34690300433f4b40de4f1f88ac','new v114 frozen archive mismatch')
        changes=git('diff','--no-renames','--name-status',BASE,'HEAD').splitlines()
        for line in changes:
            status,path=line.split('\t',1)
            require(status=='A' and (path.startswith(ACTIVE) or path==WORKFLOW),'out-of-scope change: '+line)
        out.update(repository_ancestor_verified=True,add_only_paths=len(changes),head=git('rev-parse','HEAD'))
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
