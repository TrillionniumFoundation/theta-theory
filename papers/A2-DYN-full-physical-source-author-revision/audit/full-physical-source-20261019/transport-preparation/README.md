# Read-only transport preparation for the full physical source revision

Prepared from the freshly read complete baseline commit
`fdf2603c8bf422314f199fa431086485a0d1ebb5`, root tree
`d90e88848644a25b2d9f2e3a28383f4908d2a646`, and 2,088-file article tree
`f5c90ecd279dd116330c5d90fa31cae2b0d6f61e`. The current iteration's complete
baseline identity receipt is pinned by SHA256
`2dbbbad489541592bd034b08bffeefb8491c68a9c8be8909349415f9c53c2de2`.
All 70 subtree hashes reconstruct exactly. The four fresh root/control-tree
receipts also reconstruct exactly and agree with the preceding actual C3
transport receipt.

## Current status

`INITIAL_LOCAL_INVENTORY.json` is an explicitly **provisional, unfrozen**
observation at 2026-10-19 08:28:09 UTC. It records 2,644 files and 283,200,230
bytes, including actual inherited and new build evidence. There are 577 paths
with bytes or modes different from their baseline-relative paths, and no
baseline path has been removed. Of the current paths, 2,304 reuse known
baseline blobs, including copies stored at other paths. This snapshot is not
the final mathematical source/manifest freeze and must be regenerated after
all authorized writers stop.

`INITIAL_ROOT_SCOPE.json` is the corresponding local canonical publication
construction. It adds exactly the new article
`papers/A2-DYN-full-physical-source-author-revision` and the new dedicated
workflow `.github/workflows/a2-dyn-full-physical-source-20261019.yml`.
All 212 existing article entries and all 174 existing workflows are preserved.
Counts become 213 article entries and 175 workflows. Among the 187 repository
root entries, only the `papers` and `.github` pointers change. Within `.github`,
only the `workflows` pointer changes. This verifies a proposed tree construction;
it does not claim that every unrelated branch ref remains stationary.

The workflow and its article-local `ci/` copy were checked for equal Git mode,
size, blob identity, and SHA256. No previous article, workflow, root file, remote
object, or ref was changed by this preparation.

## Adapter

The iteration-level `transport_revision.py` performs local byte reads and
canonical Git object hashing. It excludes only `.git` and `__pycache__` path
components. It includes build directories, binary PDFs, logs, previous CI
archives, and all other actual files. Literal symbolic links would be encoded
as Git mode `120000` rather than followed; none were present at the observation.
File and path-set stability are checked over each scan, and invalid traversal
or changed-blob chunk reads fail explicitly, including under Python `-O`.

The `scan`, `tree_digest`, and `git_blob` functions remain available for local
payload preparation. CLI actions are `baseline`, `inventory`, `stats`, `changes`,
`scope`, and `chunk`. All output paths must lie in the iteration work directory.
The `--final` flag records an explicit caller declaration that all writers have
stopped; it never creates a commit, sends an object, or infers a remote success.

After the source and delivery records are ready, a final inventory can be
produced with:

```sh
python -B iteration-20261019b/transport_revision.py inventory --final \
  --output /workspace/scratch/b5cc344d4c8e/iteration-20261019b/TRANSPORT_TO_PUBLISH.json
```

The final scope can similarly be computed with `scope --final --output ...`.
For an upload chunk, `chunk --path RELATIVE_PATH --offset N --length N
--expected-sha GIT_BLOB_SHA` emits the requested bytes as base64 and checks the
complete current blob against the expected identity. Network publication and
actual commit/ref readback remain separate root-agent operations.

## Metadata successor helper

The optional `prepare_metadata_transport.py` requires the exact prior carrier
inventory, declared parent commit, and final source-manifest/workflow SHA256
pins. It runs the actual source manifest verification and prepares cumulative
tree batches, large-blob identities, and canonical file/delta receipts locally.
It rejects deletion of an existing path and any modification of existing bytes
except `PUBLICATION_STATUS.json`. New files must be beneath the explicit
publication or publication-source-gate prefixes.

The helper has been syntax/CLI checked; its metadata preparation has **not**
been run because a final tested carrier and frozen source pins do not yet exist
at this observation. The helper explicitly does not verify or assert CI success.
Any new source-gate prefix can be supplied at invocation, but must remain under
`evidence/current-execution/`; publication metadata must remain under
`delivery/publication/`.

`ADAPTER_READ_ONLY_CHECKS.json` retains the completed canonical identity,
scope, exact chunk, and invalid-input checks. `TRANSPORT_ADAPTER_IDENTITIES.json`
records both helper file identities and the unexecuted metadata-helper status.
These are transport checks, with no claim to prove the continuous mathematics.
