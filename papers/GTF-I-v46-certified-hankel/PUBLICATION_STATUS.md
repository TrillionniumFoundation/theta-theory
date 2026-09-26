# Publication status — source-review release

This revision's complete LaTeX input graph and author response are published as readable files. The mathematical source is available for referee scrutiny. The branch is not labelled as a remotely verified binary release.

## Evidence that exists

The local full build completed with a 26-page article, ordinary/optimized agreement, sixteen negative-control executions, twenty-six predecessor source checks, 1,765 preserved-page text comparisons and twelve sampled predecessor raster comparisons. The local build receipt identifies `local-uncommitted` rather than inventing a GitHub source binding. The final input parser was subsequently changed locally from symbolic parsing to rational-literal parsing; its ordinary and optimized regression outputs agree. Local delivery records must keep these two observations distinct unless a fresh full build is executed.

## Remote status at this release

The source transport and branch-specific workflow were pushed before direct native-source publication. Workflow `36260243370`, triggered by `d158ff0f5f45bcbad96a2fadd8b9d0848a892638`, was still queued at the last read and had executed no steps. There is no remote success receipt for this release. Publishing additional native sources advances the branch beyond that trigger; any old job must still satisfy the ordinary non-force push checks and cannot silently overwrite this source revision.

The tool blocked the direct native `certify.py` write. This release does not retry that blocked write through a different tool, encoding or executable indirection. The prior already-committed transport is preserved as provenance, not treated as a completed native verifier release. New `certify.py`, `verify.py` and `build.py` are not claimed to be readable native files in this source-review commit. They are available in the separately delivered local package.

The planned `v46-referee-ready` automated release is distinct from the manually published `v46-source-review` branch. A future successful Actions build is not assumed here. Neither local testing nor the source-review label is independent mathematical or priority certification.
