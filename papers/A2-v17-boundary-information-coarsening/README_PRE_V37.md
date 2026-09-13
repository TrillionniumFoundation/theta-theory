# A2 v35 — integrated referee response and native verification

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · Complete English author revision · September 13, 2026

Branch: `revision/a2-v35-referee-integration-native-verification-2026-09-13`.

[Complete native main](main.tex) · [Native companion](two_collision.tex) · [Point-by-point response](RESPONSE_TO_REFEREE_V35.md) · [Current execution record](VERIFICATION_V35.md) · [Preservation](PRESERVATION_V35.md) · [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V35.md) · [Addressed referee report](../../reviews/a2-v33-external-harsh-top4-2026-09-13/REFEREE_REPORT.md)

## Revision identity

The latest addressed report is `d51c06689ba540711b2f890beb35eb235dba13e4`, which reviewed v33 at `b577cffcb3ca5597cb4905269bea9de3bd4ead38`. The intervening v34 author source is `127f9334f15c5fb12307bd691973d1eb44e499e8`; it is preserved, not described as having passed a later referee review. The present assembled source and actual build identities are recorded separately in `VERIFICATION_V35.md`.

## Mathematical revision

The proof of `thm:v22-vector-boundary-gaussian` now contains the one-mark Taylor expansion, the compact-uniform mean limit `E Delta_n = J_Sigma h + o_K(1)`, and the centered independent-sum fourth-moment estimate before restoring the mean. Each excluded observation contributes zero; censoring one observation does not erase the other summands. The existing v34 likelihood-tilting and quadratic-risk proposition remains active.

No theorem is replaced by a weaker claim. The eight theorem/lemma statements in the changed chapter and the abstract are byte-for-byte unchanged. All 52 direct inputs remain in the same order, with the exact 36-input auxiliary compendium retained. Finite and compact Gaussian comparisons, the laboratory-transverse count record, signed-versus-folded data, physical preparation costs and fixed-order stability qualifications remain distinct.

## Verification

`tools/check_revision_v35.py` supplies 24 finite arithmetic and source-preservation diagnostics, with identical ordinary and optimized output. The exact inherited companion has a successful seven-page native local build. The isolated vector syntax check is not a complete manuscript and its external references are not treated as resolved. The branch-specific workflow invokes `tools/build_submission.py` for both complete native entries and retains the actual source archive and failure logs as well as successful products. **Only the execution record, not the presence of this workflow, establishes what actually ran.**

The historical directory name remains stable so existing relative inputs and companion links are not broken. [The previous active main](history/v34/main.tex), [the previous vector chapter](history/v34/article/18a_vector_boundary_information_v26.tex), and [the previous paper entry](README_PRE_V35.md) are retained by exact Git blob. Referee correspondence stays outside the mathematical article. This revision is for independent re-review, not a statement of journal acceptance.
