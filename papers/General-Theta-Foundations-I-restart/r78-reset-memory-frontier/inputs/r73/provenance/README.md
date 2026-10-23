# Source and historical evidence

Start with `BASELINE_LOCK.json` and `BASELINE_AUDIT.md`. `CONTROL_OBJECTS.json`
pins the controlling mathematical inputs and latest deposited report by commit,
Git blob and SHA-256. `REFS_SNAPSHOT.json` preserves all actual branch identities
observed before the new author branch was published; new R73 author work is not
retroactively counted as a competing baseline.

`HISTORICAL_TEXT_INDEX.json.gz` contains one record per exact historical text
blob, with every recorded changed-path/commit occurrence, its byte length,
encoding and both hashes. The original bytes remain in the immutable repository
objects and old source trees. Recursive archive copies are not copied again
into the current manuscript directory. A complete deduplicated text corpus can
be reproduced with the scanner's `--corpus` option; it is not needed to compile
the self-contained current author package.

To reproduce the content inventory from a clone that contains the pinned commit
and blob objects, run:

```bash
python3 provenance/scan_theta_history.py \
  --repo /path/to/theta-theory \
  --refs provenance/REFS_SNAPSHOT.json \
  --out /tmp/general-theta-history-audit --corpus

python3 provenance/classify_theta_reviews.py \
  --repo /path/to/theta-theory \
  --refs provenance/BRANCH_PROVENANCE.json \
  --out /tmp/general-theta-history-audit
```

The scanner deliberately does not perform hidden network fetches. In a partial
clone, `--inventory-only` lists any missing blobs; those must first be fetched
from their recorded immutable commits/paths. The actual resumed scan used Git
transport and then the GitHub plugin for intermediate blobs; all fallback
identities and checks are recorded in `PLUGIN_BLOB_RETRIEVAL.jsonl`.

`REVIEW_DIFF_CLASSIFICATION.json` includes both report candidates in a branch
head's delta and report candidates already present in its tree. A manifest-only
head can append to a real review, while an inherited report, a copied report,
an empty branch and a pipeline audit are not new independent assessments.

`CURRENT_RETAINED_BODY_IDENTITIES.json` and
`SUPPLEMENT_SUFFIX_IDENTITY.json` concern byte preservation in the new current
source. `PINNED_INDEPENDENT_TREES.json` concerns separate native companion
sources. Their roles are explained in the root `PRESERVATION_MAP.md`.

The old R65 Actions result in `R65_HOSTED_TERMINAL_RECEIPT.json` is pinned to
`ee79ca9114f8009d62c056d07381b766645e3fc4`. It does not certify any later source.
The present manuscript's build and diagnostic results are supplied by the
current publication receipts, separately bound to the new source commit.
