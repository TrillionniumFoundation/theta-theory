# Author internal reconstruction check: native 330–332

## Conclusion and exact scope

This is a read-only author-internal cross-check of the new analytic continuation,
not an external referee report, journal assessment, or independent specialist
certification of the inherited Lorentz-gas theory. I read the full current
330–332 proof bodies and checked the interfaces requested by the integrating
author: summed label variation, section jumps, the conservative return tower,
complete collision-tail removal, positive kernel normalization, both polynomial
normalizations, Borel observation scope, the actual conditional denominator,
and the Gauss/endpoint derivatives in the weak operator theorem.

**One concrete norm omission was found in the original 332 corollary and has
been corrected by the integrating author.** The corrected integrated source
retains arbitrary bounded label coefficients and multiplies their translation
bound by their supremum norm. I read that correction and its proof sentence.
Within the scope described below, I found no additional mathematical error in
the checked new arguments. This conclusion does not independently reconstruct
every inherited finite-horizon, homogeneous-curve, singular-boundary, coarea,
pressure, or joint spectral theorem.

I did not edit any final TeX file, checker, or integrated proof. The only file
written for this task is this separate check. The new proofs remain author
proofs under their stated physical model and inherited native dependencies.
The absence of an external specialist reconstruction is an evidence status,
not by itself a reason to downgrade an inherited complete author theorem.

## Source identities checked

Initial component directory:
`/workspace/scratch/35c64a3513c5/final-analytic/`.

Corrected integrated directory:
`/workspace/scratch/35c64a3513c5/theta-theory-round3/papers/A2-DYN-localized-clearance-records-author-revision/core/`.

| Source | SHA-256 read in this check |
|---|---|
| `330_all_label_physical_roof_variation.tex` | `cd3f5485c418e3aa01b3e13f52c3fb3173b06967e3c4d0666177650135b358ba` |
| `331_return_tower_and_polynomial_likelihood.tex` | `bb1783264d74bacf50bb831cf5a0151b660f7e2e5571363f4b759afe6a8c072f` |
| Original component `332_endpoint_tested_marked_roof_operator.tex` | `f7bf3f87e4435102541168bc17b9bde3671bc3588680dccb0352bb747e738154` |
| Corrected integrated `332_endpoint_tested_marked_roof_operator.tex` | `618aaa348f7ebe40cc62a54f26a458ee9863194364b7c84a000046f79a86e16d` |

The original 330 and 331 component hashes agree with the integrated copies.
For 332 the integrating author preserves the earlier source, before/after
hashes, checker changes and correction description in
`audit/integration-proof-correction/`. I read `BEFORE.json`,
`CORRECTION.json`, and the corrected corollary and proof.

I consulted the actual predecessor interfaces in native 260, 288, 315 and
323–325. The pinned predecessor is commit
`03d651b8709d28d90aa435fc12d608ad9c945e23`, article tree
`3010c90e2363dfe1808101a3e992eb02643c28f1`. Their use here does not claim a
fresh independent reconstruction of the entire predecessor.

## 1. Concrete finding and verified correction

### Missing norm for general bounded label coefficients

**Location:** original 332, `cor:wo-fourier`, final translation assertion.

The original sentence allowed “any bounded label coefficients” but bounded
the resulting density's translation error by
`V_m^w(a,b,Psi) |h|`, without the coefficient norm. For coefficients
`c_ell`, the correct general bound is

\[
 \left\|\sum_\ell c_\ell
       \{f_\ell(\cdot+h)-f_\ell\}\right\|_1
 \le \sup_\ell|c_\ell|\,
       \mathcal V_m^w(a,b,\Psi)|h|.
\]

The omission matters because multiplying every coefficient by an arbitrarily
large scalar multiplies the nonzero translation error by that scalar, while
the original right side would remain fixed. Any nonzero compactly supported
physical component has a nonzero translation difference for some nonzero
shift, so arbitrary rescaling cannot have a coefficient-independent bound.

The exact elementary diagnostic retained by the integrating author uses
`f=1_[0,1]`, `h=1/4`, `c=2`. Then `TV(Df)=2`, the actual translation
norm of `c f` is `1`, the uncorrected upper side is `1/2`, and the corrected
upper side is `1`. This is an algebraic diagnostic for the BV norm scaling;
it is not claimed to be a simulated or exact Lorentz-gas trajectory density.

**Verified integrated correction:** the corollary now displays
`sup_ell|c_ell| V_m^w(a,b,Psi)|h|`. Its proof explicitly bounds the
combined derivative by the coefficient supremum times the summed derivative
norm before applying the BV translation estimate. This establishes the full
stated class of general bounded numerical label coefficients. Coefficients
are constant within each label, not arbitrary roof-dependent multipliers.
The unit-modulus marked operator bound is unchanged.

No further issue found in this check remains uncorrected in the inspected
integrated 330–332 sources.

## 2. Native 330: summed labels and the section-jump budget

**Checked locations:** `thm:av-all-bv`, `eq:av-all-constant`,
`eq:av-all-tv`, `cor:av-label-tests`; inherited
`eq:rv-section-budget`, `lem:rv-jumps`, and `thm:cs-charge`.

The proof sums the label vector before estimating variation. At a regular
point its vector is either zero or one unit vector. Hence a physical
endpoint contributes at most one positive coarea trace, regardless of the
number of attainable occupation or displacement labels. The interior
variation is the scalar variation of the unchanged weighted coarea
coefficient. These facts justify using `D_base^w` once for the full vector.
They do not result from adding a separate common bound for every label.

At an ordinary interior section crossing, one occupation changes by one.
If the initial and terminal tests hold, one unit vector becomes another;
its l1 jump is two. At an initial or terminal membership crossing, a unit
vector appears or disappears, with l1 cost one. The initial occupation is
included in that transition. The terminal membership does not create a
visit at index `m`. Coincident visit changes can be telescoped and charged
once per changed interior visit and endpoint membership. Artificial seams
with unchanged vector cancel before absolute values.

The inherited canonical side budgets are one-copy side charges. Therefore
`D_base^w+B_sec,end+2 B_sec,int` has the required factors: the two incident
traces on a regular side have already been combined into its jump. There
is no further factor two for the same side, and no missing factor two for
the vector transition. The twenty original rectangle sides and all true
collision indices are already in the inherited complete positive sums.

The exact labels partition the original section source with the terminal
membership retained. Consequently their total L1 mass is at most one,
not merely `1/c_*`. Every component is nonnegative and has compact support
in the original physical interval `[m tau_-,m tau_+]`. Its zero extension
has variation at least twice its essential height. Summing gives the
stated summed height; Tonelli applied to the derivative measure gives the
summed L1 translation bound. Independent scalar tests for a finite label
set justify the summed variation without a hidden infinite-dimensional
integration theorem; increasing that finite set is a nonnegative limit.

The bounded label-test corollary explicitly assumes modulus at most one.
Its coefficients are numerical label tests, independent of the roof and
trajectory within a label. No BV assertion is made for an arbitrary Borel
trajectory selector. This distinction is preserved in 331 and 332.

## 3. Native 331: true return tower without saturation

**Checked locations:** `lem:av-tower`, `lem:av-return-components`,
`eq:av-tower-moment`, `eq:av-return-bv`.

The recurrence argument is sufficient on the original section. If `E`
consists of section points with no future return, the sets `T^j E` are
disjoint by invertibility and have the same measure. Finiteness of the
collision probability makes `E` null. Points with finitely many future
visits lie in a countable union of its preimages. Repeating for the
inverse map gives the required past recurrence. No ergodicity or
independence is used.

The sets `T^a {x in Y:r(x)=a}` partition the section up to a null set:
the nearest strictly earlier section visit is unique. This proves
invariance of the induced map with the original normalization.

The tower levels `T^j {x in Y:r(x)>j}` are pairwise disjoint. The proof
therefore obtains exactly

\[
 \int_Y r\,d\nu
 =\nu\!\left(\bigsqcup_{j\ge0}T^j\{x\in Y:r(x)>j\}\right)
 \le1.
\]

It does not assume that this union saturates the entire collision space,
and it does not use the equality version of Kac's formula without that
condition. The integral is proved finite by this identity, rather than
presupposed. Dividing by `c_*` and using induced invariance yields
`E N_n <= n/c_*`; Markov's inequality gives the stated complete tail
`P(N_n>L)<=n/(c_*L)`. The physical-time bound follows from the unchanged
pointwise inequality `S_n<=tau_+ N_n`.

Starting in the section, `N_n=m` is exactly terminal membership at time
`m` together with `n` visits among `0,...,m-1`, including the initial
visit and excluding the terminal one. The collision component of the
return law is consequently the old exact density, with no shifted
occupation convention. Its complete mass is one by successive recurrence.
Fixing the occupation label in the summed variation theorem decreases
the positive derivative sum; adding `m<=L` gives `D_all^1 L`.

## 4. Complete tail removal and the positive kernel

**Checked locations:** `lem:av-kernel`, `thm:av-likelihood`,
`cor:av-exact-fourier`.

The kernel normalization and transform were rederived directly. Its
piecewise cubic transform is C2. The jumps of its third derivative at
`-1,-1/2,0,1/2,1` are exactly
`12,-48,72,-48,12`, giving

\[
 t^4\int\eta(s)e^{-its}\,ds
 =24\cos t-96\cos(t/2)+72
 =192\sin^4(t/4).
\]

Together with `int eta=3/4`, this gives precisely
`k(t)=3/(8 pi) [sin(t/4)/(t/4)]^4`, including its value at zero.
Its integrable fourth-power tail justifies inversion and the second
moment calculation `int t^2 k(t)dt=-eta''(0)=12`. Cauchy–Schwarz then
bounds the first absolute moment by `sqrt(12)`. Scaling gives transform
`eta(s/b)` and first moment `kappa_ker/b`.

A fresh exact rational calculation in this check verified all fifteen
C2 joins, the integral `3/4`, the five third-derivative jumps, and the
coefficient-scaling example above. These calculations supplement the
written identities; they certify no continuous billiard statement.

The proof restriction `Q^L` and its tail `H^L` are positive submeasures
and are never renormalized. For the full law, `H^L` and `k_b*H^L` both
have mass `delta`, so their difference costs at most `2 delta` in the
full variation convention. For the trajectory event error, the indicator
and likelihood both lie in `[0,1]`, so the discarded proof part costs
only `delta`. The factor difference between the two displayed bounds is
correct. All actual collision counts remain in the law, event, and
likelihood used in the conclusions.

For a union of at most `J` intervals,
`|I triangle (I+h)|<=2J|h|`. Combining this with
`||p||_infinity<=TV(Dp)/2` gives the event cost
`J |h| TV(Dp)`; integrating the positive kernel produces exactly
`kappa_ker J V_L/b`. This works for arbitrarily short original intervals
without changing the physical event. A bounded Borel trajectory
observation is handled by the positive bound on
`E |1_A-lambda_A,b|`, not by assigning a BV derivative to that observation.

The full finite-band identity uses three integer-character variables
(two displacement coordinates and true collision count at a fixed
return index), and one real roof Fourier variable. Its normalization
is `(2 pi)^(-4)`. With the stated positive Fourier convention,
`exp(i s t) hat{1_I}(-s)` has the correct sign. All torus frequencies
are present. Bounded frequency support and finite interval length
justify the one-label Fubini step before any collision truncation.
General events are positive sums of one-label likelihoods, so the
proof does not interchange an infinite complex label series without
a convergence argument.

## 5. Both polynomial normalizations and actual conditional mass

**Checked locations:** `cor:av-polynomial`, `cor:av-fixed-collision`,
`cor:av-denominator`.

At fixed return index `n`, the three exponents are exactly

\[
 n^2\frac{n}{L_n}=O(n^{-P}),\qquad
 n^2\frac{J_n L_n}{b_n}
 =O\bigl(n^{2+\kappa+(P+3)-(2P+\kappa+5)}\bigr)
 =O(n^{-P}).
\]

The ceiling satisfies `n^(P+3)<=L_n<=2n^(P+3)` for `n>=1`.
For the law error the absence of `J_n` only improves the bound since
`kappa>=0`. At fixed collision count, no tail restriction is needed;
`m^2 J_m/b_m=O(m^(2+kappa-(P+kappa+2)))=O(m^(-P))`.
For the guarded fixed-count source, its original epsilon is fixed,
and the variation constant retains that dependence. None of these
substitutions changes the original geometric outer-limit order.

These are absolute probability/trajectory approximation estimates.
They are not roof-density essential-supremum errors obtained by
dividing by an arbitrary interval length, and they do not establish a
microscopic conditional denominator. The source says this explicitly.

For an information event `H`, the weights
`a=1_H 1_A`, `b=1_H lambda_A,b` obey `E|a-b|<=E`. If the actual
mass `p=E a` exceeds `E`, then the likelihood mass is positive.
Adding and subtracting `b dnu*/p` gives precisely the full variation
bound `2E/p`. If instead the likelihood mass exceeds `E`, using
`p>=p_b-E` yields the stated `2E/(p_b-E)`. This is valid for any
positive finite base measure, including the fixed-collision
subprobability. The proof does not import a lower bound from a larger
event, condition on a zero arithmetic class, or transfer automatically
to an entrance law carrying an unbounded return-roof weight.

## 6. Native 332: Gauss derivatives, the singular moment, and operator scope

**Checked locations:** `lem:wo-derivatives`, `eq:wo-gauss`,
`eq:wo-interior-momentum`, `thm:wo-bv`, `eq:wo-full-moment`, and the
corrected `cor:wo-fourier`.

On the original regular capped endpoint-action branch,
`g=grad F=z e` with `e` fixed. Direct differentiation gives

\[
 q_z=G^{-1}e,\qquad t_z=zH,\qquad
 H=e^{\mathsf T}G^{-1}e,
\]

and consequently

\[
 q_t=\frac{G^{-1}e}{zH},\qquad z_t=\frac1{zH}.
\]

The factor `H` is present. The inherited endpoint cap and Hessian
bounds imply `1/Lambda_circ<=H<=1/lambda_circ` and
`||q_t||_infinity<=Lambda_circ/(lambda_circ z)`. The exact first
variation `g=R(-p_0,p_m)` then bounds each endpoint momentum
speed by `Lambda_circ/(R_- z)`. The two coordinate partial
norms of each endpoint test therefore yield exactly
`C_test,end=Lambda_circ(lambda_circ^(-1)+R_-^(-1))`.

For interior momenta, the proof differentiates the geometric tangential
component `p_i=v_i dot u_i`, rather than a square root of an incidence.
For the terminal momentum it uses the incoming flight, whose tangential
component is preserved by reflection. Combining the native unweighted
endpoint Jacobi estimate with the flight direction bound gives

\[
 |D_q p_i[\eta]|
 \le J_*\left[1+\frac{R_+}{\tau_-}(1+\sigma^{-1})\right]
            s_i\|\eta\|_\infty=C_c s_i\|\eta\|_\infty.
\]

This is the same finite constant already defined in native 288;
there is no extra `1/c_i`. The endpoint cases and `m=1` are included
because each existing adjacent `s` is at most `sigma^(-1)s_i`.
The sum `sum_(i=0)^m s_i=2(1-sigma^(m+1))/(1-sigma)` gives the
stated uniform phase budget when the observable partial derivatives
are uniformly bounded.

The product rule for the smooth multiplier yields its extra derivative
bound divided by `z`. The original coarea coefficient already contains
`1/c_*`, and its full integral is exactly

\[
 \int\sum_w\int A_w/z\,dt\,d\theta
 =c_*^{-1}\int_{\mathcal C_{m,R}}z^{-1}\,d\nu
 \le c_*^{-1}\int I_m/z\,d\nu
 \le J_\times/c_*.
\]

Thus `J_test` contains exactly one conditioning factor. The separately
conditioned version of native 315 is not inserted and divided by
`c_*` again. The complete near-critical positive bulk remains in
this moment estimate. Smooth tests have bounded one-sided values at
physical boundaries; incoming critical charges are multiplied by their
norm bound, and the actual zero grazing trace remains zero. Regular
section jumps use the same one-copy vector costs as 330.

The bilinear form defines the stated weak map from `C1` into its linear
dual. Unit-modulus exact label phases preserve the summed L1 and
variation budgets. The endpoint norm factors in the displayed operator
bound are conservative but valid. The corrected general coefficient
translation statement now has the required coefficient supremum.

Crucially, every orbit derivative here varies the two endpoint angles
of a fixed actual stationary branch. The initial physical momentum is
not fixed during that variation. No estimate identifies this derivative
with `D T_R^i` at a fixed initial phase point, and no uniform bound on
the expanding long-time forward map is asserted. The final paragraph
explicitly preserves that distinction for the four-coordinate inverse
problem. The weak `1/|s|` estimate is also explicitly distinguished
from a strong anisotropic spectral estimate and from decay in returns;
it is not integrable over the full high-frequency line.

## 7. What this check does not close

The check confirms the new elementary/probabilistic/analytic steps at
the stated native interfaces after the one norm correction. It does
not independently reconstruct every global physical endpoint chart,
singular-null source coverage, canonical side budget, all-word momentum
kernel or complete multiplier proof. Those remain inherited author
mathematical dependencies with their original scope and evidence.

Neither these new estimates nor this check completes the original
endpoint-layer same-pool shortage, a strong joint spectral/arithmetic
expansion, all microscopic selected-event denominator bounds, the raw
pointwise local limit, or the long-time four-coordinate inverse.
Arbitrary Borel trajectory observations have the positive likelihood
error bound, not an asserted BV norm. The full physical collision
chain, original section, all labels and physical clock remain unchanged
throughout the checked arguments.
