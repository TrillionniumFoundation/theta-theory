# A2 v37 — native manuscript and referee response

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 13, 2026.

The stable `A2-v17-boundary-information-coarsening` directory contains the current unabridged native source; its directory name is not the revision number. The current branch is `revision/a2-v37-referee-closure-native-submission-2026-09-13`.

[Main manuscript](main.tex) · [Native two-collision companion](two_collision.tex) · [Response to the latest referee](RESPONSE_TO_REFEREE_V37.md) · [Verification](VERIFICATION_V37.md) · [Preservation](PRESERVATION_V37.md) · [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V37.md).

## Version identity

The [v36 referee report](../../reviews/a2-v36-external-harsh-top4-2026-09-13/REFEREE_REPORT.md) is pinned to review commit `01e772030042ffde9df125c0d40401aee2aabd17` and reviews submission `0802bfa20533feff55bf5620d39d6399d5e778f5`. This revision descends from that review commit. Its mathematical-source commit is `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294`; the documentation/evidence commit preserves the native files at that commit.

## Changes and retained scope

In `thm:v26-single-offset-global`, part (3) now explicitly assumes realizability, connected analytic strictly convex obstacle boundaries, a connected marked lifted-channel graph, a rank-two anchoring pair based in one channel frame, and a rooted signature-rigid spanning tree reaching every obstacle orbit. The full-table reference is `thm:v24-uncalibrated-periodic-rigidity`. The proof first recovers the lattice and its Gram form, then propagates obstacle placements along the tree.

No theorem, observation level, compact-parameter conclusion or auxiliary proof is removed. In particular the signed all-order inverse, intrinsic periodic reconstruction, common-orientation quotient, moving-ceiling comparison, original-alternative moment argument, compact Le Cam passage and charged physical acquisition remain in the native input chain. The old entry and edited chapter are preserved under [history/v36](history/v36); the old navigation is [README_PRE_V37.md](README_PRE_V37.md).

## Actual verification, not a submission-readiness claim

[Focused diagnostic output](verification/v37/diagnostics.json) records eight passing families, including re-execution of the six latest-referee checks. Ordinary and optimized Python outputs are identical. [Execution metadata](verification/v37/execution.json) separates those checks from the actual seven-page native companion build.

**C2 is still open:** the complete native main and its PDF were not built or inspected in this session. The new hosted run failed without executed steps or artifacts. The companion PDF and full local evidence are delivered as attachments to the revision conversation; their identities are recorded in the ledger. The repository retains the companion source, command, final log and driver output, but no full-main PDF is supplied here.

To rerun the focused checks from a checkout of this revision branch:

```sh
python papers/A2-v17-boundary-information-coarsening/tools/check_revision_v37.py > diagnostics.normal.json
python -O papers/A2-v17-boundary-information-coarsening/tools/check_revision_v37.py > diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

The inherited complete build driver is `tools/build_submission.py`. Its reproducible full-checkout invocation and the still-required PDF inspection are recorded in [VERIFICATION_V37.md](VERIFICATION_V37.md). Configuration of that command is not reported as an executed full build.
