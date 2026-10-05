# Revision 11 — proof dependencies and scope

## Frozen source

The mathematical baseline is the complete revision 10 at author commit `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`, reviewed at `a42dc1401007f9f8025c916106884e09d7d864f0`. All 27 baseline core files and all 14 baseline diagnostic scripts remain byte-identical. No historical theorem or proof is removed from the article.

## New proof chain

| Statement | Mathematical inputs | New conclusion |
|---|---|---|
| Lemma 22.1: compensation about the mark | Additivity of the physical record; invariance and invertibility of the actual first-return map; bounded collision compensation | Exact two-sided collision representation of the original n-return record, including k=0,n |
| Lemma 22.2: two-sided clock windows | Scalar collision correlation summability; section-density domination; actual visit-count equivalences | Forward and backward error `C(j+b)/b^2` without assuming b<=j; deterministic maximal bounds on negative as well as positive intervals |
| Proposition 22.3: marked stopping | Two clock windows; dyadic maximal estimate; bounded insertion | Uniform-in-k error `C M_a[n^-1/5+|v| n^-1/5 log n]`; no unbounded stopped sum is estimated on the exceptional event |
| Lemma 22.4: marked deterministic integral | Mean-preserving smoothing; small-residual collision variance; existing smooth collision spectral family; density and multiplier bounds | Exact middle-multiplier pairing; uniform estimates for two long blocks and for either short or zero block |
| Theorem 22.5 / Theorem C | Marked stopping and deterministic estimate; four-dimensional frequency integration | Single-return-mark central theorem with separate supremum and variation losses |
| Corollary 22.6: unchanged state-event conditioning | The preceding theorem with an indicator; invariance of the section probability | Central integral divided by the actual event mass; explicit restrictions on rarity and BV growth |
| Appendix C | Demers–Zhang source definitions and the existing local collision identification | Definition-by-definition source map; no new induced-space assertion |

## Exact identity and ordering

Put y=(F_R^*)^k x. The original centered record becomes

`sum_{j=-N^-_k(y)}^{N^+_(n-k)(y)-1} h_R(T_R^j y)`.

The backward interval contains k section visits and the forward interval contains n-k. The weight is exactly a(y), not an approximation to its value at a deterministic collision time. At deterministic lengths r,s and after smoothing, the exact pairing is

`ell(L_z^s M_(a_delta) L_z^r nu)`.

Only forward collision powers act on the anisotropic space. The rightmost power records the past segment after shifting its origin, the multiplier is at the marked state, and the leftmost power records the future segment. No independence of the past and future is assumed.

For two long blocks the principal amplitude differs from alpha_a by `O(M_a delta^-4 |z|)`. The principal comparison is split into

`lambda^(r+s)(A(z)-alpha_a) + alpha_a(lambda^(r+s)-Gaussian)`.

This order matters: it prevents multiplication of the cubic error by an unnecessary `delta^-2` multiplier loss. A block shorter than the logarithmic threshold is removed directly from the real exponent using bounded summands. Its Gaussian time coefficient is restored with an explicit error. A zero block is the identity and is not replaced by a spectral projection.

## Frequency and norm balance

The fixed choices are `U_n=n^(1/200)`, `delta_n=(1/4)n^(-1/14)`, and a sufficiently large logarithmic short-block threshold. The contribution from the insertion variation is **only**

`V_a delta_n U_n^4 = (1/4)V_a n^(-9/175)`.

The remaining factors carry M_a. The slowest exponent is `3/280` from observable unsmoothing; its logarithm is a square root. The other margins are `29/700`, `53/280`, `51/1400`, `9/50`, `7/40`, `19/40`, and `97/100`. All are strictly larger. The complementary-power term at the logarithmic threshold also decays faster. Source tests check these exact rational inequalities, but their validity as billiard estimates depends on the continuum proofs in the article.

For a return-state event E with `nu_R^*(E)>=c n^-beta` and indicator variation `O(n^kappa)`, the relative central error vanishes if `beta<3/280` and `beta+kappa<9/175`. These are sufficient bounds, not an optimal rarity threshold.

## Conditions not discharged

The covariance is still continuous and positive semidefinite. The measurable L2 coboundary characterization has not been upgraded to a periodic-evaluable representative. The collision operator with a smooth middle multiplier is not an anisotropic realization of the unbounded induced twist. The physical central radius is still `n^-99/200`; the intervening annulus, compact minor arcs and large roof frequencies are not estimated by the new theorem. No global critical/singular branch classification or n-dependent raw density derivative sum has been proved.

For marked raw inversion, the actual marked residual must still be integrable, have complementary integral `o(n^-2)`, and satisfy the local extracted-edge conditions, and the covariance must have a uniform positive lower bound. Multiple separated state factors and exact final lattice/flight-time constraints are not replaced by a single mark. The same-event corollary makes no change of conditioning event.

No build, finite diagnostic, or this ledger constitutes an independent human proof review or an editorial decision.
