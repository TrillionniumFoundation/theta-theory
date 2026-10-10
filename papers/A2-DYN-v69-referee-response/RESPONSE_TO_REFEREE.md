# Response to the external report on A2-DYN revision 68

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**New revision:** 69, 10 October 2026  
**Controlling report:** `reviews/a2-dyn-v68-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Report commit / blob:** `7fd1ca003cebd920e3f5a1f7af136e4c86cadcf4` / `6c2501c22189fb04ee565d844003a589c6272f07`  
**Reviewed author commit:** `c8268a608a971c6832bcfed2a827af951e84c577`  
**Frozen complete author paper tree:** `dce4295d9d660f64e4d25bb0463045dddc546249`  
**Active source:** `papers/A2-DYN-v69-referee-response/main.tex`  
**Author refs:** `revision/a2-dyn-v69-referee-response-2026-10-10` and `revision/a2-dyn-v69-referee-copy-2026-10-10`.

## 1. Mathematical response

We thank the referee for separating the correctness of the new angular-germ and annular arguments from their incomplete coverage of the original physical source. In particular, the distinction between a shrinking inner collar and a complete chart is essential. We have not treated the previous component theorem as the unrestricted pointwise theorem.

The revision retains the original Lorentz problem, title, actual-return record and finite arithmetic transition kernel. It does not adopt a different model or a different publication target. Three new mathematical modules enlarge the controlled original source.

First, module 149 constructs a comparison density with the clearance multiplier omitted but with the entire physical itinerary and exact-label indicator retained. This is an actual positive physical measure, not the full reversible trace and not measure assigned to a nonphysical continuation. A direct two-endpoint event comparison proves its ordered positive-width collar bound.

Second, module 150 applies the original guard's absolute Lipschitz bound on the inner source. The guard is no longer placed in an annular denominator. This removes the positive-center-guard hypothesis and its relative condition number from the height theorem. Every finite angular birth order is still allowed. On the angular-only stratum, for center values at most delta, the original clearance height is bounded by

    6 C H F_chi,K(H) min{1, delta + C_g epsilon^(-1) sqrt(2H)}.

For zero center value this gives

    6 sqrt(2) C C_g epsilon^(-1) H^(3/2) F_chi,K(H).

This includes infinitely flat guards without assigning a finite analytic order to them. It also covers arbitrarily small positive center guards without a further cutoff. The angular certificate remains explicit; the assertion is not a complete zero-center-source theorem outside the stated strata.

Third, module 151 uses finite-scale angular occupation on the actual physical source, not its germ. It proves a height estimate on an entire fixed radial interval, including portions beyond a certified germ disk and labels born only at positive radius, on explicit angular-ratio strata. It also gives a physically weighted moment sufficient for the high-ratio tail. The moment implication is proved; the required uniform Lorentz moment bound is not assumed or reported as proved.

The new main source compiles all 148 inherited core modules and all eight inherited appendices. The three additions bring the active core count to 151. Every inherited mathematical label, Python source and the bibliography is preserved. The complete preceding abstract and introduction are compiled in a historical appendix rather than deleted.

## 2. The positive comparison is not a replacement of the source

Let B be the original one-hot physical and exact-label indicator and let D be the first-clearance multiplier. The original density is the angular coarea integral of w B D. The comparison density is the integral of w B. Only D has been omitted, and only in an upper comparison. The original first-hit tests, initial and terminal section conditions, occupation at collisions 0 through m-1, displacement, and normalization are unchanged.

The exact inequality is

    b_clr(t_z+u) <= min{1, g_z + L_g sqrt(2u)} b_hat(t_z+u).

There is no division by g_z. The common physical density distortion and the polar coarea cancellation are the inherited ones. Summing the positive comparison collars gives an upper bound by the unchanged exact-return event with two endpoint momentum strips. The inherited fixed-width local law then gives C(w+s) for a center interval of length w and a collar of width s. It does not differentiate an interval local limit.

This proof allows any subfamily because every subfamily is dominated by the same event. No word count, label count, regularity norm of the selector, or separation of critical values is introduced.

## 3. Response to the required mathematical changes in Section 22

### 22.1. Physical weighted tightness of persistence

The guard part of the old persistence number is removed from the new height theorem, rather than estimated by an invalid fixed-count exhaustion. The angular-only number is p^a = max{1/r*, 2 k^a}; zero angular germs receive only their certified zero radius. On positive-center nonzero germs, p^a is no larger than the preceding persistence number.

The ordered tail of this angular certificate is not proved. We also give an alternative finite-scale ratio V based on the essential angular maximum divided by its actual positive radial average. Module 151 proves a high-V source bound from the moment

    limsup_m sup_(R,lambda,t) m^2 sum_(t_z in [t-S,t])
        V_z(S)^(1+alpha) q_hat_(z,S;lambda).

This is physically weighted and retains the exact label. The corresponding tail factor is T^(-alpha), with the explicitly stated density-distortion factor. It is not an unweighted count. The finite value of V at every fixed chart does not establish finiteness of this ordered moment; that obligation remains open. The old angular-condition tail is not identified with either new quantity.

### 22.2. Zero-center guards

Addressed by a new source theorem on every fixed angular-persistence stratum. Theorem `thm:v69-absolute-guard-height` proves the H^(3/2) zero-center bound above using only the original Lipschitz guard. The proof also applies to a guard which is infinitely flat at zero. It does not replace it by an analytic model. The theorem for center values at most delta provides a continuous small-center estimate and includes all positive-center cases at delta=1.

The complete zero-center height beyond the angular and finite-scale strata is not declared closed. Its remaining source is retained in the disjoint decomposition.

### 22.3. Source outside the germ disk and inner collar

Addressed by a separate finite-scale comparison rather than an inference from the shrinking inner theorem. For a fixed interval I=(a,b) inside (0,S), define V(I,S) from the actual physical angular fractions over that entire interval and averaging collar. Theorem `thm:v69-finite-scale-height` bounds the source on V<=T by

    C T exp{K_chi(sqrt(2b)+sqrt(2S))}
        min{1,delta+L_g sqrt(2b)} (b-a+S).

No analytic germ or fixed cyclic order on the whole interval is needed. In particular the complete radius (0,S) has bound 2 C T S exp{2 K_chi sqrt(2S)}. This includes later births and outer parts beyond the recorded germ disk on these strata. A fixed finite radial partition is permitted; no infinite dyadic sum is moved through the collision limsup.

The high-ratio tail and source beyond S remain explicit. Shrinking S is not said to make its exterior small.

### 22.4. Remaining positive clearance classes

The new partition is source-level, disjoint and exhaustive:

    b_clr = b_angular_inner + o69 + t69 + e69.

After the angular inner restriction is assigned, o69 contains the remaining selected-chart source below S with V<=T; t69 contains the remaining source below S with V>T; e69 contains everything else. The original outside source, failed taper, selected grazing, noncritical rank, uncovered states and omitted outer annuli are in e69. Zero-center and zero-germ source is allocated by these actual restrictions, not deleted.

The first two terms now have explicit ordered bounds. The latter two remain obligations, with a physical-moment sufficient condition supplied for t69. No complete estimate for e69 is asserted.

### 22.5. Complete first-incidence height

The inherited inverse-incidence argument in module 131 was examined together with its determinant gain and full finite-count coarea bound. Its exponential collision-count constant is preserved explicitly. It is not inserted as an ordered fixed-band estimate. The complete first-incidence height remains a separate positive term in the new endpoint budget. A proof of this term is still required.

### 22.6. Complete clearance height

The new canonical inequality combines the enlarged inner theorem, the full fixed-radius ratio-stratum theorem and the exact remaining source. It does not substitute their sum for the entire clearance source without its tail and exterior. This provides two controlled positive pieces where the prior budget had only one, but is not a complete clearance-height theorem.

### 22.7. Unrestricted pointwise theorem

The original target is retained verbatim in mathematical content, with the same central normalization and arithmetic reference. The new budget is

    E_M <= C_M B^(-1/192) + H(b_epsilon(B)^inc)
           + 6 C H F_chi,K(H)
           + 2 C T S exp{2 K_chi sqrt(2S)} + H(t69) + H(e69).

The parameters are fixed before the collision limsup. The final three missing complete-source obligations are not set to zero. Consequently the full pointwise theorem is not reported as established by this revision.

### 22.8. Same-roof consequences

The full-source hypotheses for unrestricted same-roof bridges, forward essential likelihood and roof-conditioned path laws are unchanged. No pointwise conclusion is inferred from integrated bridge convergence or from the new partial height estimates. The corresponding status flags remain false.

### 22.9. Independent specialist verification

No independent human audit has been obtained. We retain the distinction between author-side derivation, finite diagnostics, native compilation and independent verification. The principal specialist inputs are the complete primitive physical decisions, selected-contact chart and relative density, uniqueness/disjointness of the physical chart restrictions, and the exact-label two-endpoint local bound. Module 151 does not need analytic-germ classification, which shortens its imported geometric route.

### 22.10. Proof burden and journal narrative

The new introduction states two principal results, their exact hypotheses and the original endpoint budget. Modules 149--151 appear first. `JOURNAL_ROUTE.md` identifies the shortest load-bearing chain. Historical openings are compiled at the end, and validation/provenance discussion is placed in separate files. No inherited proof was arbitrarily removed. The complete source remains lengthy; the new ordering does not pretend that source preservation resolves every editorial concern about the full architecture.

### 22.11. Generality route

We retain the original Lorentz topic. No unrelated realization is added to change the paper's subject or to substitute for the remaining physical endpoint. The positive comparison and moment-transfer lemmas are stated with quantitatively identifiable quantities, but no second singular-hyperbolic realization is claimed without verification.

## 4. Technical and presentation comments in Section 23

Comments 1--5: the unweighted angular fraction, guarded fraction and roof density remain distinct. The new comparison density and its positive-width trace receive hats. Neither is the full reversible atomic trace. The old angular condition number, old guard-relative persistence, new angular-only persistence and finite-scale ratio have different definitions. The analytic, inactive-sign, Morse and physical collar radii are not conflated.

Comments 6--15: no count-uniform analytic radius or finite birth-order maximum is asserted. All primitive tests and truly coincident root germs remain in the inherited analytic proof. Finite jet agreement is not used as an analytic identity. The positive one-sided root ordering and null angular boundaries remain unchanged. The guard is only Lipschitz; zero center values are treated by absolute domination, never division.

Comments 16--25: all density statements use a common coarea representative almost everywhere. The factor 2 pi and polar cancellation remain explicit. The annular denominator is used only under 2K sqrt(H)<1. The angular family is fixed independently of H. The finite-scale family is fixed before the collision limit. All finite orders are summed before taking that limit. The single positive outer annulus is retained for the angular theorem, and the contributing center intervals are displayed. Coincident centers add positively. No count-dependent persistence cutoff is chosen.

Comments 26--30: the shrinking source interpretation is explicit. A separate fixed-radius theorem treats the outer part on its own strata. Every partial result is followed by the complete positive remainder, and the incidence term remains visible. Small support, small mass, or fixed-count finiteness is not used as an essential-height bound. The finite arithmetic transition kernel and all zero classes remain unchanged.

Comments 31--36: variation densities, probability total variation, path dual norms and essential-supremum density are not interchanged. The fixed-band order is preserved. The shrinking-collar corollary uses positive domination by a fixed-width source before taking that fixed width to zero, not a spectral estimate at a moving width. Each author ref has an independent exact-SHA qualification run; only actual completed receipts establish success. Inherited false status flags remain false. Operational evidence is separated from the journal argument.

## 5. Preservation and validation

The frozen review and author source are retained unchanged. All 148 inherited core files, every inherited Python file, all eight inherited appendices and the bibliography are byte-identical in the new complete directory. Every previous compiled input and mathematical label remains included. The full v68 main and manifest also have explicit byte-identical provenance copies, and the preceding opening statements are compiled verbatim in `appendices/v68_frontmatter.tex`. Replaced metadata remains available in the unchanged source-pinned baseline directory.

The new finite diagnostic suite has 2,335 checks in normal and optimized Python, including angular orders up to one million, absolute zero-center domination, a flat guard, finite-scale later births, zero-average conventions, physical density distortion, positive weighted-tail inequalities and disjoint source allocation. Negative controls distinguish an unguarded comparison from an invalid guarded-annulus denominator, and reject fixed-count exhaustion or small mass as a height proof. These are finite algebraic and synthetic profile checks, not physical realization theorems for every Lorentz word.

Exact-SHA qualification verifies source identity, the complete effective inherited status map, all compiled inputs and labels, stabilized native TeX without shell escape, and the actual new proof pages. The workflow records the actual commit and active tree rather than predicting its own future SHA. It runs on both author refs. Successful workflow receipts are evidence of those checks, not a continuum proof certificate or human referee endorsement.

## 6. Result of this revision

The principal advance is the removal of the guard-relative obstruction from the source-height argument. Zero-center and arbitrarily small positive-center guards are now included on the angular strata, with an extra square-root gain at zero center. A second, germ-independent theorem controls the entire chosen radial interval on finite-scale physical strata and exposes the precise weighted tail needed to remove that cutoff.

The original unrestricted pointwise problem is unchanged. Its remaining ordered physical tail, exterior-clearance and complete first-incidence estimates are not declared solved. This revision supplies new proofs and a more inclusive exact source decomposition for the next external assessment, while preserving the distinction between those achievements and the complete endpoint.
