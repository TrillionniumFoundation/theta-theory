# Publication archive restoration and received-file verification

Copy **both** `restore_archives.py` and `verify_received.py` into the final
publication directory before generating `DELIVERY_MANIFEST.json`. The
receiver imports the restoration module; neither script requires a third
helper or any nonstandard Python package. They do not modify the sealed
manuscript source, assign a source SHA or create a validation receipt.

## Commands for the received publication

From the complete publication directory:

```bash
python verify_received.py
python restore_archives.py --out /tmp/general-theta-r75-restored
```

Both commands verify the entire delivery and all archive contents. The
second additionally restores the three complete archives. It retains an
existing output only if its exact size and SHA-256 match; a different
existing file is rejected without replacement. Archive members are read for
verification, never extracted by these helpers.

`--root /path/to/publication` selects a different received directory. The
optional `--expect-source-commit` and `--expect-paper-tree` arguments compare
the manifests against independently pinned full 40-character Git identities.
Supply the actual final identities from the publication entry; no guessed or
pending identity belongs in either manifest. The self-excluding delivery
manifest is authenticated externally by the publication's Git commit or its
independently obtained hash.

An output directory outside the publication is simplest. Reconstruction
directly into the publication directory is also supported if the three
filenames appear in `optional_local_reconstructions_excluded`. Other nested
output directories and unmanifested publication files are rejected to keep
the delivery inventory exact.

## Required manifest shapes

The scripts preserve the R74 manifest format and derive the revision from
the actual schema. For the new publication use:

- `DELIVERY_MANIFEST.json`, schema `theta.r75.delivery-manifest.v1`, with
  actual `source_commit`, `source_paper_tree`, `manifest_excludes_itself: true`
  and `files` records containing `path`, `bytes`, `sha256` for **every** other
  delivered file, including both scripts, all archive parts, the parts
  manifest, readable PDFs and execution evidence.
- `archives/ARCHIVE_PARTS.json`, schema
  `theta.r75.lossless-archive-parts.v1`, with the same actual `source_commit`
  and three `archives` records. Each record has `file`, `bytes`, `sha256`,
  `format: "ordered raw byte concatenation"` and ordered `parts`, each with
  `path`, `bytes`, `sha256`. Part identities must agree with the delivery
  manifest, and their byte counts must sum to the complete archive size.
- Standard complete archive filenames end in `_Source.zip`,
  `_Validation.zip`, and `_Historical_Text_Corpus.tar.gz`. These identify
  their roles. An optional `role` field may explicitly say `source`,
  `validation`, or `historical`; exactly one of each is required.
- ZIP payloads normally have a top directory named after the ZIP filename
  without `.zip`. An optional archive-record `archive_prefix` can specify a
  different top directory.

The source ZIP must contain the complete sealed source directory, including
its native `SOURCE_MANIFEST.json`, without extra payload files. Every native
manifest row's size, SHA-256 and Git blob are checked. The complete Git paper
tree is reconstructed using the declared file modes and compared with the
delivery's actual `source_paper_tree`. The source manifest itself is included
in that Git-tree computation. The current theorem-index hash is retained for
comparison with the stored strict execution receipt.

The historical TAR.GZ is the complete inherited `blobs/<git-blob>.txt`
corpus. Every member is checked against the source ZIP's authenticated
`provenance/current-full-scan/HISTORICAL_TEXT_INDEX.json.gz`: exact member
set, size, SHA-256, Git blob and reversible declared text encoding. This
supports the four retained Latin-1 legacy logs without silently converting
their bytes. The complete TAR.GZ SHA-256 must also match its archive record.

The validation ZIP must contain an internal `ARCHIVE_MANIFEST.json` with
schema `theta.r75.validation-archive.v1`, the actual `source_commit`,
`manifest_excludes_itself: true` and exact `files` rows. Its payload file set
must equal those rows plus the manifest itself. Every row is read completely,
which also checks ZIP CRCs. The optional archive-record `internal_manifest`
can select a different relative manifest path.

The validation manifest's optional `build_receipt` defaults to
`build/BUILD_RECEIPT.json`. That stored receipt must report the actual
successful **strict** run for the same source commit/tree, with unchanged
source, no skipped diagnostics, normal/optimized identity and the matching
sealed theorem index. Its source-manifest hash and source-file count must
match the delivered source ZIP. If a top-level `BUILD_RECEIPT.json` is also
delivered, its bytes must match the archived copy. The manuscript, supplement
and companion PDF hashes must match this receipt; their extracted text files
are expected at `build/<text_file>` inside the validation archive.

## What PASS means

The helpers issue a PASS only after received bytes, archive parts,
reassembled archives, exact payload membership, source Git-tree identity,
historical text and the stored strict execution evidence agree. They **read**
the stored build and diagnostic results; they do not execute them again.
They do not prove mathematics, establish novelty, conduct independent human
refereeing or record an editorial decision.

`SCRIPT_VALIDATION.json` records helper validation against the actual
completed **R74** delivery, including all 275 source files, all 6,432 corpus
members and all 178 validation payload files, plus named corruption and
no-overwrite controls. It is development evidence for these helpers. It is
not a substitute for running them on the final actual R75 publication.

Once the real-SHA strict R75 run succeeds, generate the actual archives and
manifests, run `verify_received.py` against the completed R75 publication,
and retain that actual output separately. Include any such retained output
inside the delivery manifest only after accounting for the dependency order;
do not create a self-hashing manifest cycle.
