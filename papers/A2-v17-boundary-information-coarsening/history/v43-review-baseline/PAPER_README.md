# A2 v42 — complete native manuscript and response to the v41 referee

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 14, 2026

The current branch is `revision/a2-v42-native-source-referee-response-2026-09-14`. The directory name `A2-v17` is a stable historical path, not the current manuscript version.

[Complete native main](main.tex) · [Native companion](two_collision.tex) · [Current referee response](RESPONSE_TO_REFEREE_V42.md) · [Actual verification ledger](VERIFICATION_V42.md) · [Preservation and historical dependencies](PRESERVATION_AND_DEPENDENCIES_V42.md) · [Addressed v41 report](../../reviews/a2-v41-independent-harsh-top4-2026-09-13/REFEREE_REPORT.md).

## Source and mathematical revision

The addressed report is pinned at `e162532115071265cf73b97a5069f33628347cfe`; its reviewed submission is `c730a60bbc8af2a4c6e432813c31dccc897828e7`. The native manuscript retains the complete three-part argument, auxiliary compendium and bibliography. Its 54 literal direct inputs include the preamble and bibliography; the auxiliary compendium retains all 36 of its inputs.

The revised [single-offset inverse chapter](article/23f_single_offset_law_inverse_v42.tex) retains the complete density inverse, fixed-order stability and finite-flight reconstruction. In its detailed periodic-determination proof, the supplied signature-rigid tree is explicitly rerooted at an obstacle incident to the anchoring frame. The proof then recovers the lattice, places every obstacle orbit in the same frame and compares two admissible realizations in one gauge. No incidence, observation, registration assumption, symmetry hypothesis, or restriction on the stated finite jet order is added. All theorem, proposition and corollary statements in this chapter are byte-identical to their predecessor.

The predecessor chapter remains at [its original path](article/23f_single_offset_law_inverse_v26.tex). The exact preceding native entry and both preceding README files are preserved in [history/v41-review-baseline](history/v41-review-baseline). These are archival source snapshots; their relative paths retain their original manuscript-root interpretation.

## Evidence and delivery

The [verification ledger](VERIFICATION_V42.md) distinguishes new executions from inherited results. At this source-revision checkpoint, the hosted run `34798984887` failed with an empty executed-step list and runner ID zero. That is not a compiler test and does not close C2. The complete main and native companion, their source-matched recursive inputs, raw execution evidence, and rendered-page inspection remain the required delivery standard. A fixture, a companion-only build or mathematical diagnostic count is not substituted for it.

The inherited [native build protocol](NATIVE_BUILD_PROTOCOL_V38.md) and fail-closed builder remain available. The [v42 workflow](../../.github/workflows/a2-v42-native-submission.yml) checks out its exact triggering commit and attempts both complete native entries; its existence is not evidence of successful execution.

This is the sole current A2 response/evidence entry on this branch. Earlier responses and audits retain their historical identities. The manuscript is provided for another independent referee examination, not as a claim of journal acceptance or universal proof certification.
