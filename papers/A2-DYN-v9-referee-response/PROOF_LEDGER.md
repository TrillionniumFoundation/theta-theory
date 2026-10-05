# Proof dependency ledger — A2-DYN revision 9

Source baseline: author `36427a184ea256f0336fbc431dc76110a9b14592`; controlling review and parent `9d1904397400529aae4a5d3cccede9081b4dfb33`.

## New proved chain

| Statement | Inputs actually used | Conclusion and scope |
|---|---|---|
| `lem:physical-bv` | Fixed finite horizon, finite physical root choices, parameterized semialgebraic cell decomposition, finite section perimeter | Uniform first variation of one-collision observables in initial coordinates |
| `lem:bv-smoothing` | Even reflection, positive convolution, BV translation estimate | Mean preservation, L1 error O(delta), C2 cost O(delta^-2) |
| `prop:bv-correlation` | Inherited smooth collision spectral splitting and multiplier, preceding smoothing | Uniform exponential two-observable collision correlations; residual sum variance O(m delta log(1/delta)) |
| `thm:collision-covariance` | Uniform collision correlation tail and bounded finite-itinerary continuity | Absolutely convergent continuous PSD Gamma_R; smoothing error O(delta log(1/delta)) |
| `lem:smooth-collision-expansion` | Genuine smooth collision endomorphisms, uniform resolvent contours | Analytic eigenvalue on radius a delta^2, explicit Hessian and cubic remainder O(delta^-6 |z|^3) |
| `thm:actual-record-gaussian` | Shrinking-scale collision estimate, exact stopped compensation, count variance and dyadic maximum | Actual return Gaussian covariance D_R=Gamma_R/c_*; uniform compact-frequency rate n^-1/26 sqrt(log n) |
| `thm:gaussian-kernel-coboundary` | Summable collision correlations, bounded variances at zero, mean ergodic theorem, stopping identity | Kernel iff collision/induced L2 coboundary; no periodic representative asserted |
| `thm:collision-functional` | Smooth fourth moments, slower smoothing, residual maximum, chronological products | Uniform path-space collision CLT for uniformly bounded BV initial densities |
| `thm:actual-return-functional` | Collision functional theorem, actual uniform return clock, genuine exponential return tail | Uniform actual induced functional CLT, covariance D_R |
| `cor:physical-functional-gaussian` | Collision FCLT under tau_R/bar tau_R initial density, physical clock, bounded partial flights | Unconditioned stationary displacement/count functional CLT |

No independence of successive return blocks, no independent-flight model, and no induced spectral gap are used in this chain. The collision Banach-space input is identified in `COLLISION_INPUT_MAP.md`; it is not an assertion about the hard section indicator as a multiplier.

## Retained mathematical package

The twenty-one inherited core files retain their theorem, lemma, proposition, corollary, definition, and proof environments. This includes physical periodic arithmetic and coercivity, exact critical edges, the raw and localized inversion criteria, exact means, moving-domain stability, soft killing, cumulative return tails, common renewal, first-order clocks, conditioned unfinished-block control, and stronger closure criteria. Four inherited files receive exposition updates, and the complementary projection in the renewal section is renamed. `SOURCE_MANIFEST.json` and `tools/verify_v9.py` give the exact preservation rule and hashes.

## Distinct estimates still needed for the raw endpoint

| Requirement | Why the new theorems do not imply it |
|---|---|
| Actual anisotropic induced family, Fredholm and quantitative phase reconstruction | The new spectral endomorphisms are smooth collision twists, not the unbounded induced twists |
| Periodic-evaluable regularity and uniform positive definiteness | An L2 coboundary is an almost-everywhere identity; the selected periodic orbits have measure zero |
| Induced Green–Kubo summability or induced leading-eigenvalue expansion | Actual Gaussian covariance is obtained by stopping collision sums, not by either of these stronger constructions |
| Complete critical/singular raw residual sum with actual n-dependence | Initial-coordinate BV and trajectory deletion do not bound second derivatives of inverse-coarea densities |
| Strict frequency splice and integrated complementary-frequency tail | A fixed compact set of rescaled central frequencies does not exhaust the Fourier integral |
| Weighted density estimates and relative exact-event boundary control | An unconditioned process limit and a same-event path comparison do not change a shrinking exact conditioning event |

The full raw LLT, weighted local limits, and independently reviewed proof acceptance are not certified by this ledger or by the build.
