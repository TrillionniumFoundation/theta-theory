# R76 publication helper contract

`restore_archives.py` and `verify_received.py` are standard-library-only
receiving tools for **General Theta Foundations I, R76**. They are ported
from the unchanged R75 publication helpers. Their current source commit,
source tree and complete source-file count are read from the actual delivery
and source manifests; those values are not hardcoded. The initial sealed
source had 501 files. The corrected source
`891643799f2dfb2737ad5c147bf8def2d460630b` has 507 files after preserving the
initial diagnostic-path failure and correction evidence. The receiver
requires equality with the actual sealed manifest and strict receipt rather
than trusting either observed count alone. The component-test receipt's
501-file observation records its earlier test time; it is not a receiver
gate or a claim that the corrected source contains only 501 files.

The fixed controls are the complete R75 source/publication, the R65 report,
the 386-file predecessor inventory, 209 inherited and 220 current indexed
statements, 20 inherited and 23 current diagnostic scripts, 59 protected
inputs, the complete 34-file R58 companion, and the 6,664-object historical
scan. These identify this revision; an old delivery is rejected even if its
filename suggests R76.

## Required publication layout

The two helpers sit beside `DELIVERY_MANIFEST.json`. The publication includes
`archives/ARCHIVE_PARTS.json`, every declared archive part, the three compiled
PDFs, top-level `BUILD_RECEIPT.json`, and top-level `THEOREM_INDEX.json`.
Other publication documents and evidence may be included, provided every
file is listed in the delivery manifest. Unlisted files and symlinks are
rejected. The manifest excludes its own self-hash explicitly.

Three complete archives are required: source ZIP, validation ZIP and
historical text TAR.GZ. Archive parts are concatenated as raw bytes in their
declared order. Each part and each complete archive has an exact byte count
and SHA-256. A part cannot be shared between two archives. Part lengths must
sum to the complete archive length. Optional complete local reconstructions
may be excluded from the delivery inventory only by their exact declared
complete archive names; if present, they are verified too.

### Manifest schemas and fields

| Artifact | Required schema | Required binding and payload fields |
|---|---|---|
| `DELIVERY_MANIFEST.json` | `theta.r76.delivery-manifest.v1` | `source_commit`, `source_paper_tree` are full lowercase 40-hex identities; `manifest_excludes_itself: true`; `files` records each `path`, `bytes`, `sha256`; optional `optional_local_reconstructions_excluded` names only declared complete archives. |
| `archives/ARCHIVE_PARTS.json` | `theta.r76.lossless-archive-parts.v1` | Same `source_commit`; exactly three `archives`, with roles `source`, `validation`, `historical`; each has `file`, `bytes`, `sha256`, `format: ordered raw byte concatenation`, and ordered `parts` records. |
| Native source manifest inside source ZIP | `theta.r76.exact-source-manifest.v1` | The actual output of the current `seal_source.py`, including exact source file paths, modes, sizes, Git blobs, SHA-256 values, and its fixed predecessor/report/preservation/index controls. |
| `ARCHIVE_MANIFEST.json` inside validation ZIP | `theta.r76.validation-archive.v1` | Same `source_commit`; `manifest_excludes_itself: true`; complete `files` records; `build_receipt` defaults to `build/BUILD_RECEIPT.json`. |
| Stored strict build receipt | `theta.r76.native-verification.v1` | The actual successful output of current `verify.py`: strict mode, exact source SHA/tree/manifest, all 23 suite records, all 220 native locators, and all three native document records. A draft or diagnostics-skipped receipt is rejected. |

An archive record may supply `archive_prefix`. Otherwise ZIP member names
begin with the complete archive filename minus `.zip`, followed by `/`.
The source ZIP must contain the exact native source manifest and exactly its
listed payload files. The validation ZIP must contain its internal manifest
and exactly its listed files. Its archive record may override
`internal_manifest`; the default is `ARCHIVE_MANIFEST.json`.

## Source and predecessor checks

The receiver rehashes every source ZIP payload, reconstructs its exact Git
tree including modes and the manifest blob, and compares that tree with the
delivery pin. It then checks:

- R75 source `bc2952aa9a9695fe9985d491a4156b8975024285`, publication
  `2c103f924720435700e947cc8df31b8b648f61e9`, source tree
  `497886b8961cf12001bbea66909757f93bb8d1ee` and independently fixed old
  manifest SHA-256
  `4485cd06e12a3615f56c15a472c05f58781437ba66e5de8b9f54f104215696f3`.
- Every one of the 386 fixed predecessor files at its current or archived
  destination, including modes, byte lengths, SHA-256 and Git blobs.
- All 59 protected current mathematical/support inputs, derived from the
  exact previous protected inventory plus the four R75 mathematical files.
- The exact 32,284-byte inline supplement suffix and complete R58 tree
  `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`.
- R65 report commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, Git blob
  `d1ff9c5662390156ee212c82b173e86a21180e84`, SHA-256
  `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`.
- The current 220-label native theorem index, including all 209 exact
  inherited labels, the source label bodies, native locators and inherited
  flags.
- All 23 declared diagnostic script identities, including byte-identical
  retention of the 20 R75 diagnostic sources.

The historical index is exactly
`provenance/R76-baseline/full-scan/HISTORICAL_TEXT_INDEX.json.gz` inside the
source. The TAR.GZ contains one `blobs/<git-blob>.txt` member for every indexed
object, without missing or extra members. All **6,664 objects and
91,682,814 original bytes** are checked by byte length, SHA-256, Git blob and
reversible declared text decoding. This is an identity/content scan, not a
proof check of every historical argument.

## Stored execution evidence checks

The validation archive preserves the actual strict build output under
`build/`. Each diagnostic record identifies its ordinary/optimized stdout
and stderr filenames. Both stdout files must be byte-identical, match their
stored hashes and parsed receipt report, and match the script hash in the
delivered source ZIP. Each report's grouped counts and exact/floating counts
must agree. All 23 reports must sum to the global strict receipt totals.
No diagnostic count is hardcoded beyond the suite inventory.

The stored receipt must authenticate the actual R76 source path, unchanged
source tree, predecessor ancestry/preservation, all 220 native statements,
unskipped diagnostics, and all three completed native documents. Every
published PDF is rehashed against that receipt. The extracted text files
must remain in the validation archive at `build/<text_file>` with the
recorded hashes. If also published at top level, those copies must match.
The top-level strict receipt and theorem index must match their archived and
sealed source counterparts.

These checks read stored evidence. They do not execute a new build or a new
diagnostic, fetch GitHub, authenticate a human reviewer, certify mathematical
correctness, or infer a journal decision. An independently trusted source
SHA and tree should be passed through `--expect-source-commit` and
`--expect-paper-tree` to bind the receiving operation to the intended release.

## Commands and restoration behavior

Run `python verify_received.py --root PATH` to check a complete publication.
The optional expected-source flags each require a full lowercase 40-hex
identity. Output is a JSON receiving-verification receipt.

Run `python restore_archives.py --root PATH --out OUTPUT_DIRECTORY` with the
same optional expected-source flags to first verify the complete publication
and then restore all three complete archives. A different existing output
file is never overwritten. Identical existing reconstructions are retained.
Outputs must be outside the publication directory, or exactly in that
directory when all three reconstruction names are explicitly allowed by the
delivery manifest. Partial files created by a failed restoration are removed;
preexisting files are left alone.

## Executed helper tests

`test_publication_helpers.py` executes 27 small component challenges, with
byte-identical ordinary and `-O` outputs. They include a complete three-role
transport round trip, wrong independent pins, old-revision rejection, one
changed byte, a truncated part, reordered parts despite consistently updated
outer manifests, unlisted payloads, duplicate JSON/ZIP members, unsafe paths,
ZIP symlinks, a changed inner ZIP payload, Git-tree path collisions and wrong
predecessor/report/statement-count declarations.

The real current historical corpus was also checked directly, without
copying it. `PUBLICATION_HELPER_SCRIPT_VALIDATION_R76.json` records the actual
helper hashes, component report hash, all 6,664 history identities and the
scope of those executions. These tests do not report a final release PASS:
the completed actual publication still requires its own full receiving and
restoration runs after the final strict receipt and manifests exist.
