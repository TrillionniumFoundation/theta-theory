# Response to the independent report on A2 v85

**Manuscript:** *Action rigidity from selective observations*, Qian Qi  
**Revision:** 86, 18 September 2026  
**Controlling report:** `reviews/a2-v85-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`  
**Report commit:** `65cd70c44e1bb5f679bd3e0397c6d66da139102c`  
**Reviewed manuscript commit:** `4f3d2ab5259b8deda67e1ec6ea9a6151a405ddd4`

We thank the referee for distinguishing proof objections from the question of mathematical scale. This revision adds three theorem groups rather than treating source readiness or a revised novelty statement as a substitute for mathematics. The complete v85 principal body and all companion inputs remain present. New statements are placed first in the principal manuscript; the same canonical body is used by the expanded edition.

## 1. Beyond rational partial fractions

Section 4, **An intrinsic detector theorem on a compact double**, replaces the rational coordinate by a compact real Riemann surface. The action curve consists of primitives of normalized third-kind differentials. Theorem `thm:v86-divisor` classifies regular separation by finitely many integral-charge and normalized second-kind obstructions. Its tests use the complete meromorphic differentials, including their holomorphic period corrections. On positive-genus surfaces, matching principal parts alone is not the criterion.

Lemma `lem:v86-normalized` includes the normalization argument: the real-period map on holomorphic differentials is a real-linear isomorphism, by the compact harmonic-function argument. Riemann--Roch supplies the initial prescribed principal parts. Holomorphic detector spaces on positive-genus surfaces give explicit nonrational admissible examples. The rational theorem is recovered on the sphere, rather than merely repeated in different notation.

Theorem `thm:v86-branched` additionally keeps the **original** logarithmic action law under a finite meromorphic clock map. It classifies nonrational detector primitives by finite fibre-residue and tangent tests, allows ramified action values, and proves the sufficient count `deg D + 4m + 2g`. An elliptic-integral detector on a real elliptic curve is an explicit example. Thus the extension is not obtained solely by replacing the physical action law.

## 2. Clock complexity and the status of the pole budget

Theorem `thm:v86-divisor-budget` gives the intrinsic sufficient count `deg D + 2g + 4`. Clearing the sphere's point at infinity recovers exactly the v85 formula `D_f + 6 + max(ell,-2)`. The zero count and the period-sensitive classification now arise from the same geometric setting.

We do **not** label this sufficient meromorphic budget optimal. The manuscript explicitly records the necessary dimension bound `N >= dim(F_E)+2`, and identifies the extra oriented-interval structure responsible for the sharper polynomial count. Thus an optimal sampling theorem for every meromorphic subspace is not claimed to have been proved.

There is instead a new sharp threshold in the structured experiment requested in item 7: two clocks, independently of a detector degree bound, versus a one-clock metric ambiguity. This is not a contradiction to the pointwise `q+3` theorem. Sharing changes the quotient on the clock-by-space observation domain.

## 3. Honest adaptation at singular channels

Section 3 replaces the unspecified regular-class inverse constant by an explicit degenerating modulus in the constant-relative-detector, binary, three-clock experiment. With `rho = |det U det V|`, Theorem `thm:v86-product-modulus` proves a one-sided inverse bound of order `min(1,delta/rho)`, uniformly against candidates in the full closed model, including singular candidates.

The cancellation needed for the sharp power occurs in the determinant of the affine matrix polynomial `(T-h)P(T)`. The proof isolates this step; it does not multiply generic spectral condition numbers. Theorem `thm:v86-adaptive` gives honest coverage over the singular model, an observable determinant-based diameter certificate, expected length at most `C_zeta min(1,1/(sqrt(N)rho))`, and squared risk at most `C min(1,1/(N rho^2))`. Neither procedure receives a rank floor. The expectation proof controls all sample outcomes, rather than leaving a fixed-probability exceptional event with full diameter.

Theorem `thm:v86-singular-lower` proves matching minimax risk over classes `rho >= rho_0`, including `rho_0=0`, and honest expected-length lower bounds at explicit least-favourable points. The transition is `sqrt(N)rho` of order one; for equally weak contrasts it is `N epsilon^4` of order one. This is an honest locally adaptive statement with a matching impossibility boundary, not merely validity without a supplied floor.

## 4. The hard geometric input

The existing finite noisy metric certificate is retained, with the Stefanov--Uhlmann stability hypotheses unchanged. The new shared-apparatus result changes the selective observations sufficient for determining boundary distances. Its surface corollary then invokes Pestov--Uhlmann. Neither result is presented as a new general boundary-distance rigidity theorem, a non-simple theorem or a partial-data theorem.

The new mathematical contribution to the geometric experiment is the exact structured-nuisance threshold, including actual metric alternatives under a fixed reference and fixed relative detector at one clock. No geometric hypothesis has been silently weakened to manufacture that conclusion.

## 5. Reconstruction versus a certificate

The introduction explicitly distinguishes exact identification, finite calibration, statistical confidence sets and an effective infinite-dimensional inversion algorithm. Proposition `prop:v86-calibration` supplies a finite calculation for the shared clock constants: at most sixteen orientation choices and four-by-two linear systems. Its two-site smooth inverse is a **local** correctly labelled statement. The four-site result does not claim globally labelled recovery of arbitrary isolated action values at exceptional swapped roots; continuity is used in the field theorem.

The infinite-dimensional noisy metric object remains a confidence/stability certificate. The existing finite-dictionary result keeps its supplied-dictionary premise. No efficient geometric algorithm is claimed without a construction.

## 6. A nonregular experiment rather than another regular rate

The new lower-bound family changes the two actions while rescaling both channel contrasts so that **both observed marginals are exactly fixed**. The remaining joint-law difference is

`(epsilon_u epsilon_v / 4) (lambda_t^(-2)-1) e e^T`,

independent of the clock. It is proportional to the product, and vanishes identically when either contrast is zero. This is the matching mechanism for the determinant-product upper bound. The v85 regular `N^(-1)` result remains available as a separate finite-dimensional geometric theorem; it is not promoted as the new statistical contribution.

## 7. A sharp threshold under genuinely shared nuisance

Theorem `thm:v86-shared` assumes a constant unknown reference and a shared detector **including its relative throughput**, while allowing both unknown channels to vary with the spatial site. Two clocks identify any continuous action field with no open plateau, without supplied labels. Directly matched false calibrations permit at most one action value; swapped calibrations permit at most two. This finite obstruction proves the global field theorem and the four-site calibration result.

Boundary distances of a simple metric have no open plateau, by the first-variation argument in Lemma `lem:v86-no-plateau`. Corollary `cor:v86-shared-geometry` consequently gives two-clock recovery on simple surfaces modulo boundary-fixing diffeomorphisms. Its one-clock lower bound keeps the reference and detector fixed and uses a small scaling family of actual metrics. An explicit channel transformation keeps every one-clock matrix identical, with positive full-rank probability channels throughout. The auxiliary transformation need not itself be stochastic; positivity is proved for the actual transformed channels.

An unrestricted shared detector still has an unobserved decomposition into reference delay and its two detector values. The theorem recovers the action and the two effective clock constants, not unsampled detector values. For a constant relative detector the reference and throughput are separately recovered by the displayed formulas.

## 8. Structural organization

The principal manuscript now begins with the experiment-indexed observation quotient: pointwise detector functions, shared clock-only nuisance on a product domain, and the noise-scale modulus of the matrix map. The new proofs calculate each relevant obstruction rather than identifying all three experiments with the same scalar quotient. In the binary three-clock experiment, exact singular fibres, the inverse modulus and honest diameter are generated by the same determinant-product mechanism.

We do not assert that one scalar invariant also proves a geometric boundary-distance theorem. The separation between acquisition identifiability and geometric rigidity is explicit. All prior modules remain accessible after the new theorem groups, rather than being deleted to make the architecture appear shorter.

## 9. Closest predecessors

The new theorem groups contain explicit closest-predecessor paragraphs. Matrix-pencil factorization is attributed to latent-structure identification, not claimed as new. Modulus-based recovery, honest adaptation and weak-identification obstructions are compared with Donoho, Cai--Low and Dufour. Riemann--Roch and normalization are compared with Forster and Grushevsky--Krichever--Norton. The metric conclusions explicitly identify the imported Pestov--Uhlmann and Stefanov--Uhlmann steps.

The additional claims are the shared-nuisance permutation obstruction and sharp clock threshold, the product modulus and its marginal-preserving attaining family, and the divisor--period classification for action-preserving detector spaces.

## 10. Isolated rank lemma and proof audit points

Lemma `lem:v86-rank` isolates observable rank versus latent rank, including the probability normalization required by the upper singular-value inequality. It also proves the observable determinant comparison and its perturbation bound.

The verification script checks the matrix-pole identity, determinant factorization, rank-one-span cancellation, the one-clock channel transformation, exact marginal preservation and the joint interaction formula symbolically. It enumerates four-site orientation choices and tests a weak-channel grid numerically. These are diagnostics, not formal proof certification. The field argument at coincident profiles, the compact inverse argument and the positive-genus analytic reasoning require mathematical review; they are supplied as proofs in the text.

## 11. Source readiness and preservation

At source preparation, the self-contained new-results extract `rigidity_v86_core.tex` compiled natively to 15 pages. Its 47 labels and 8 cited entries had no missing or duplicate references; the rendered pages were inspected. The full principal and expanded editions use inherited sources not replaced in this revision. Their separate native build and whole-repository preservation checks are specified by `.github/workflows/a2-v86-manuscript.yml` and must be read from the actual run, not inferred from the core build.

The source commit adds files only. The verification script compares every inherited path against the controlling review commit and checks that every companion input is retained in order. A successful CI run will store the native verification, source commit, logs and PDFs; a pending or failed run is not a successful build. The report's mathematical recommendation is not treated as changed by compilation alone.

## Material submitted for renewed review

The principal entry point is `papers/A2-v17-boundary-information-coarsening/rigidity_v86.tex`; the preserved expanded edition is `rigidity_v86_full.tex`. The core extract provides a directly compiled reading copy of the new theorem groups, not a substitute for the complete principal manuscript. This response identifies the precise new statements and the claims not being made, so the next referee can audit the mathematical changes independently.
