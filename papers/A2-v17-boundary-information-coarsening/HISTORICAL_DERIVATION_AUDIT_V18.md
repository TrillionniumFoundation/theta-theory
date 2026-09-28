# Historical derivation audit — A2 v18

## Revision ancestry

The v18 branch is descended directly from review commit `d713b345ed58b8949cafa430954c5a82e1d159fd`, which reviewed author head `106836283ebe3fabee0479df8976d24f6dbe0bf6`. No earlier author or review branch is rewritten.

## Derivation route retained

1. The alternating stationary action and Jacobi Hessian give the exact normal multiplier, endpoint whitening and determinant cancellation. The physical flux is the mixed endpoint derivative multiplied by residual-time volume.
2. The half-line actions and determinant amplitudes control the normalized nonlinear physical law on a nonshrinking collar, uniformly in every fixed mixed derivative.
3. The physical determinant amplitude is identified with the normalized scalar stable-return density through finite Schur concatenation; this is a physical identification, not a claim that scalar linearization itself is new.
4. The v6/v7 transfer chain retains failed preparations and supplies the uniform positive-offset-to-tangent TV error. The full tangent record has an erasure transition at scale `q_j=e^{-j gamma}`.
5. Residual-time integration changes the successful tangent density to a two-dimensional positive-part quadratic density. Its support boundary moves and the density vanishes linearly there, producing a logarithmically divergent score variance and the scale `r_j=q_j^2 log(1/q_j)`.
6. The v18 boundary-information theorem isolates the general regular-hypersurface coefficient and corrects the finite/supercritical quantifier scope. The supercritical TV conclusion continues to follow from Hellinger affinity.
7. The v8 critical-subsample argument transfers the endpoint supercritical limit to the physical positive-offset experiment without requiring the full supercritical accumulated tangent error to vanish.
8. The independent-contact jet inverses, analytic realization, complete profile inverse, Abel stability, calibration and adaptive/stopped results retain their existing proofs and hypotheses. They are not reinterpreted as consequences of the new information theorem.

## Architectural change

No historical theorem module is deleted. The active entry point replaces only the front-matter narrative and the boundary-information presentation. The old `article/01_introduction.tex` and `article/18_boundary_information.tex` remain byte-preserved in the branch for provenance, while `main.tex` selects `article/01_introduction_v18.tex` and `article/18_boundary_information_v18.tex`.

The revised hierarchy is:

`nonlinear relative geometry -> boundary/profile invariant -> residual-time coarsening -> intrinsic boundary information -> sharp physical observation hierarchy`,

with profile acquisition, calibration, adaptive experiments and auxiliary minimax modules treated as downstream applications rather than coequal themes.

## Audit limits

This revision rechecked the latest referee report, the v17 historical audit and proof ledger, the active relative/endpoint information sources, the build workflow, and the nonregular-support literature used for the new positioning. It does not claim that every historical appendix has been independently re-proved in this round. Existing proof ledgers and source pins continue to record their own inspection boundaries.
