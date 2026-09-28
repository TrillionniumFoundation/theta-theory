# A2 v32 — compact local experiments and complete native submission

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · Complete English author revision · September 12, 2026

Branch: `revision/a2-v32-compact-lecam-native-submission-top4-2026-09-12`.  
Mathematical-source commit: `35fd4ccef1b5785692de512635f7240a4df0d641`.  
Review parent: `9edd5f48d91b74d09718149de6e2c3550c375f20`.  
Reviewed predecessor: `e1f6304f6069869ac323e7d1a634a619faa4bc32`.

[Complete native manuscript](main.tex) · [Native companion](two_collision.tex) · [Point-by-point response](RESPONSE_TO_REFEREE_V32.md) · [Source preservation](PRESERVATION_V32.md) · [Execution record](VERIFICATION_V32.md) · [Historical dependencies examined](HISTORICAL_DERIVATION_AUDIT_V32.md) · [Addressed referee report](../../reviews/a2-v31-external-harsh-top4-2026-09-12/REFEREE_REPORT.md)

## Mathematical revision

The compact-experiment section proves a finite-net passage lemma and obtains a uniform total-variation modulus from the existing linearly vanishing support Hellinger estimate. It upgrades the original endpoint experiments, including singular information, to two-sided Le Cam convergence on each fixed compact local set. The fixed-window endpoint theorem inherits this conclusion through the existing exact/ideal comparison, common reference caps and success-weighted finite-bridge transfer.

The count--endpoint chapter now states both compact Le Cam limits explicitly. Its proof retains the original fast hyperbolic, slow iso-hyperbolic and gap scales; includes mixed Taylor remainders; compares exact geometric waiting laws in Hellinger distance; separates the independent uncapped factors; and accounts for cap and finite-bridge errors afterward. The chapter uses theorem and equation references instead of revision-era prose.

The signed inverse, off-model equivariance, common-orientation classification, moving-ceiling Poisson kernels, physical calibration, charged global reconstruction, direct-position benchmark and all auxiliary mathematics remain in the complete manuscript. The original count chapter remains archived in its original path; its stable theorem labels are implemented by the expanded active chapter, not duplicated in the active graph.

## Verification and review status

The local finite diagnostics pass in ordinary and optimized Python with identical output. A five-page isolated syntax check used the actual preamble and the two new sections, without theorem or reference stubs; its sixteen external labels remain explicitly unresolved. This is not a submission PDF.

**C2 is not certified by these local checks.** The complete native build workflow archives the immutable full source, builds `two_collision.tex` and `main.tex`, and retains real logs even when a build fails. The [execution record](VERIFICATION_V32.md) reports what actually ran and distinguishes intended commands from successful evidence. A successful compilation would still require inspection of the complete PDF.

The historical directory name remains unchanged. [The previous main](main_pre_v32.tex) and [previous paper entry](README_PRE_V32.md) are preserved by exact Git blob. This author revision is for independent re-review, not an assertion of journal acceptance.
