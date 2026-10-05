# Author-side proof audit — Revision 63

This is a self-audit of written arguments, not an independent referee report or formal proof-assistant certificate. The full v62 audit is retained under `retained-v62/PROOF_AUDIT.md`.

## 1. Preserve the logarithm in the entropy defect

The new inequality is not obtained by multiplying the old one-step constant by a block length. For rotated probability densities f_j and their mixture g, entropy loss is exactly the weighted sum D(f_j||g). The classical inequality D_1>=D_(1/2), followed by convexity of minus log and Cauchy–Schwarz, bounds this loss from below by -2 log ||T sqrt(f)||_2. The invariant component is bounded using the orbitwise support measure. This yields -log(kappa^2+(1-kappa^2)theta), without linearizing minus log.

All zero-density issues are handled by the extended-value convention and approximation. The mixture dominates every positive-weight component, so the component divergences in this application are finite. The general lemma retains the projection onto all invariants. Only the later transitive-sphere specialization identifies that projection with constants.

## 2. Formal words, actual positive averages, and full spectra

The radial polynomial identity is in the formal group algebra and holds after every orthogonal action, including actions with relations. The second recurrence is S_2=A^2-(q+1)I; using q at this step would be false. Subsequent recurrences have coefficient q. The Chebyshev bound is applied to the entire self-adjoint Koopman operator on the mean-zero space. A first-harmonic norm is insufficient.

P_b is a positive uniform average over actual executable formal words with no adjacent inverse pair. The signed polynomial representation is only a way of estimating that average, not an implementation with negative transition probabilities. Reversing a word preserves the uniform formal nonbacktracking law and agrees with the global chronological convention. Blocks are independent of each other; the letters inside one block are not iid. The machine is conditioned on the whole word when forming its actual composite row.

For q=3 and b=4 the conservative eta_b equals exactly 1/4. The lemma uses a non-strict inequality and the tests preserve this boundary. For LPS q=5, b>=4 gives a strictly smaller number. Pinochet Lobos–Pittet's exact radial norm is sharper than our elementary bound and is credited rather than rediscovered.

## 3. Calibration, drift and arbitrary widths

At the first selected cut, an externally fixed physical prefix makes the physical unit vector deterministic, regardless of randomized hidden initialization. Its centroid mass is therefore one. Terminal mean correctness and legal decoder norm at most one give residual centroid mass at least 1-e. The total loss across selected blocks is at most e.

The transport proof only uses the weighted centroid flow for a finite law of orthogonal maps. Hence it applies to one entire nonbacktracking word as an atom. Arbitrary fixed fillers rotate the auxiliary density without changing its entropy. The actual row includes all intermediate hidden processing. No identity word, commuting filler, lower bound on state masses or bound on intermediate widths is assumed.

Each selected register has at most k directions. With h=(eta_b/(A_m k))^(1/p), their smoothed support occupies at most eta_b of the round sphere. The entropy defect is d_b=-log(2 eta_b-eta_b^2); transport contributes C_m/h sqrt(M e/(1-e)). The entropy range is log(D_m A_m k/eta_b), because the sphere dimension p equals m-1. Using a lower orbit dimension in this range without changing the smoothing geometry would be unjustified. This is why the new crossover is a spherical theorem, not automatically a theorem for every compact homogeneous orbit.

For positive narrow cuts, greedy spacing b retains at least ceil(J/b) cuts. Thus M=ceil(J/b)-1 gaps can be used; cut zero is excluded from J. For a peak bound, cuts 0,b,...,floor(N/b)b give M=floor(N/b). Prefix and final suffix are deterministic words of the required lengths.

## 4. Joint asymptotics without exchanging limits

The inversion is a deterministic dichotomy: after subtracting the constant entropy offset, either log k pays a fraction of H or the transport term does. No limit is taken in a machine parameter space. With n=N or n=J, b=ceil(sqrt(n log(n+2))) and lambda=n^(-1/2), the first term loses O(sqrt(n log n)) in its logarithm. The second loses the same amount through eta_b, but retains e^(-p/2). The residual denominator is uniform for e<=e0<1.

A finite enlargement of the constant handles small n using k>=1 and min(q^n,((n+1)/e)^(p/2))<=q^n. The e=0 case is treated separately before division by e. Thus the bound is uniform over the whole stated error range, including zero; it is not obtained by taking a positive-error limit in a horizon-specific upper construction.

The exact upper machine stores reduced physical products; the free-word ball gives a universal C_q q^N bound even if the action has relations. The second upper machine is the existing quadratic spherical inner-hull construction with amplitude slack e/2. The better of two different admissible machines gives the minimum of the bounds. This does not assert that one machine is simultaneously optimal for every error.

## 5. Rational Bloch specialization and the three regimes

Bloch Euclidean error equals sqrt(2) times Frobenius error. This fixed conversion does not change exponential accuracy rates, but is retained in the finite certificate. The six rational matrices are the same LPS input as v62; no identity letter is added. The exact 5^t count is a coset count with cyclic stabilizer, not the free-group ball count used for the general upper estimate.

For subexponential inverse error, inherited Theta(N/epsilon_N) is stronger. For exponential inverse error, the new rate is min(a,log 5). For epsilon<=25^(-N)/16, the inherited exact profile remains stronger. At a=log 5 we assert 5^(N-o(N)) width, not exact equality 5^N or a sharp leading constant.

## 6. Sufficient arithmetic certificates

The executable checker bounds log(x) by range reduction and the positive atanh series with a rational tail bound. A rational u>sqrt(2) with u*epsilon<1 bounds xi from above. The elementary pi<4 bound yields a conservative squared transport cost. A strictly positive lower gap whose square exceeds that upper cost proves exclusion. No floating-point comparison determines an exclusion.

The verifier recomputes every field; it rejects tampered source parameters and witnesses. A false exclusion flag means inconclusive. The tests check exact recurrence identities, rational interval consistency, strict example witnesses, boundary conventions and negative controls. They do not establish universal analysis or the imported Ramanujan input.

## 7. Independent scope

The repeatable-probe causal theorem and general terminal stationarization are preserved with their original hypotheses. No new causal exponent or irreversible realization classification is claimed. The entropy on a smoothed sphere is not the stopped-path entropy gate of the independent A/B/C/D pipeline. No aggregate flag changes.
