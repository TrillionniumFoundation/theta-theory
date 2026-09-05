# theta-theory — Round 49 active revision

The current submission is **Logarithmic-Depth Boundary Identification with Bounded Probes and Retained State**, responding to the Round 48 referee report.

Start with [`ROUND49_REVIEW_INDEX.md`](ROUND49_REVIEW_INDEX.md), the [main manuscript source](ROUND49_REVISION.tex), and the [point-by-point response](AUTHOR_RESPONSE_ROUND48.md). The [retained-results supplement](ROUND49_RETAINED_RESULTS.tex) preserves the earlier homogeneous inference results. Source identities, actual verification scope, and PDF hashes are recorded in `ROUND49_PUBLICATION.json` and the verifier-generated `ROUND49_VERIFICATION.json`.

The new attainable result uses the original bounded-duration exploration law, an explicit fast clock, and bounded baseline profiles committed within diagnostic blocks, with feedback between blocks. It uses retained state and the exact likelihood of all completed readouts to attain logarithmic depth with deterministically linear elapsed time. It also strengthens the unrestricted-feedback posterior bounds and repairs the two confidence guarantees identified in Round 48.

All historical manuscripts, reports, and their provenance remain in the full revision branch. The new main article does not rely on historical verification JSON files as mathematical proofs. The source-capsule commit is a reproducible complete active-source closure, not a deletion of historical materials from this branch. No journal acceptance or formal proof certification is claimed.

The new implementation, test suite, and source verifier are supplied in the accompanying review bundle because the GitHub tool blocked their upload. Their SHA256 hashes are pinned in the committed manifest, and the actual execution receipt distinguishes them from Git-bound mathematical sources. The new program files are not claimed to exist on this branch until separately supplied from that bundle.
