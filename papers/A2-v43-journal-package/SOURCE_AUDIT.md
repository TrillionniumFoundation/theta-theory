# Source and verification audit — A2 v43

This is an author-side, AI-assisted source audit, not an independent human
proof review. `tools/qualify_v43.py` is the current entry point.

The native source inventory is frozen in `SOURCE_PINS.json`. Publication mode
requires the exact `--expected-head`, verifies every tracked package/workflow
blob, rejects a dirty checkout and checks that the commit descends directly
from the controlling review. Only additions in the v43 package and its workflow
are permitted. Historical paper/review trees and active v42 proof/label content
are checked independently of the new front matter.

The package contract pins the complete finite-interface source, exact-section
sources, cross-document labels and owners, and current document headings. It
requires the default `a_m^(-2)` budget to precede the explicitly named retained
all-node alternative. Its acyclic dependency graph separates common factor
reconstruction from the two acquisition designs. Negative tests mutate these
contracts and require rejection, including missing companion and stale ledgers.

Both existing finite diagnostic suites run unchanged under ordinary and
optimized Python and must return identical successful output. The current
contract tests are additional editorial/source checks, not additional continuum
proofs. Both PDFs must compile with no shell escape, reach stable cross-document
auxiliaries and pass the final log and actual-input-closure checks.

The journal archive must contain both PDFs and all current source inputs and
front matter. It excludes historical front matter, verification tools and old
source manifests. Its member set and content hashes are checked after writing.
A manifest inside binds the members to the exact commit; the receipt outside
binds the archive itself. Source-only capture does not report a successful PDF
build, and `--development` never certifies a remote commit.

The local container could not resolve github.com for a Git clone. The already
mounted v42 exact-source artifact supplied the development copy. Remote reads,
branch creation and publication use the connected GitHub actions. Development
and remote evidence remain distinct rather than claiming a local clone occurred.
