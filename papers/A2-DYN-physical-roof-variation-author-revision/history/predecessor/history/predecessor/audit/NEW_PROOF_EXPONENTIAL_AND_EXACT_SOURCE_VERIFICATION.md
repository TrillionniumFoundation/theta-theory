# Internal verification of anchor-layer contraction and the exact central observation source

This is an author-side reconstruction of the new proof bodies, not a new referee report, journal endorsement, or independent human-specialist certification. It checks the mathematical implications and their scopes. Finite rational or index checks are auxiliary verification of the written inequalities, not a proof of a continuous billiard statement. The native proofs themselves quantify over the complete original geometric family and all relevant global minima.

## Source identities and resolved application scope

The mathematically inspected native bodies have the following current SHA-256 identities in `core/`. The final 308 identity includes the isolated typographic reflow documented immediately below:

| Native body | SHA-256 |
|---|---|
| `305_central_physical_clock_and_exact_sections.tex` | `f354724c43b98d2fc54119d7fb74604b4e47306919e348528fb6f35924f8cb3a` |
| `308_anchor_layer_exponential_localization.tex` | `e217d1348b7c01853b2024a53a7236eb1ce85ab788a8d3a54026d200e45e076a` |
| `309_uniform_exact_central_record_source.tex` | `136ee041cacd61c9080e4d692929b57a6d15553d553eef09ad81cb7fd69374c8` |

The first application check identified a formal issue: the opening context of 305 originally obtained physicality only through the older polynomial source complement and its depth `D_0`, whereas 309 supplies physicality by a new exponential source complement. The deterministic clock and phase proofs themselves only need two actual regular central subrecords and the original global comparison minimum. The final 305 opening now explicitly states that general deterministic scope for `d >= 1` and `2d < m`; the old source complement is identified as one sufficient route to physicality. This resolves the cross-application without assuming, or artificially imposing, a comparison between two unrelated source thresholds. The final 309 threshold notation is `J_obs,D_obs`, distinct from inherited notation.

The clock and source verification file for 305–306 remains a record of the earlier proof-body reconstruction. Its earlier hash of 305 is superseded by the hash here only for this explicit scope addition; its checked finite clock identity and constants have not been changed.

### Typographic-only addendum for 308

The original mathematically inspected 308 source had SHA-256 `1bc7f3e77818205d5265bfc8f372cbd472d52c5e1bf4be15c6f7c5e3c44c414c` (12,164 bytes). The current source has SHA-256 `e217d1348b7c01853b2024a53a7236eb1ce85ab788a8d3a54026d200e45e076a` (12,168 bytes). Direct byte comparison verifies that the entire difference is one bounded replacement: the unchanged inequality `\max\{rA_H,2A_F\}<10^8=C` moves from inline math to display math, with its sentence punctuation and the following sentence reflowed. No inequality, constant, hypothesis, quantifier, label, or proof step changes.

The preserved before source is `evidence/current-execution/initial-validation/308_before_typographic_reflow.tex`; the contemporaneous record is `evidence/current-execution/initial-validation/TYPOGRAPHIC_REFLOW.json`. Their hashes match the independently computed before/after hashes above. The receipt records the initial build's 4.97733 pt overfull box and three zero compilation exit codes; this audit verifies the isolated source reflow and does not claim a new compilation or layout result. The mathematical reconstruction below remains applicable to the current 308 bytes.

## 1. Common active geometry of every global minimum

Lemma `ae-common-minima` uses a convex product of the original closed disks. The midpoint of two minimizers is feasible. Convexity of the sum of Euclidean edge lengths, together with equality of the minimum values, implies that the sum of the individual nonnegative triangle-inequality defects is zero. Every individual defect therefore vanishes. Consecutive disks have a fixed positive separation, so none of the edge vectors is zero. Equality in the triangle inequality makes corresponding edge vectors positive parallel, with equal unit directions.

The Cartesian gradients depend only on these ordered unit directions, so the gradients agree at all coordinates for all minima. A nonzero coordinate gradient has a unique minimizing point on its disk, namely the opposite radial support point. A zero internal gradient means that the two adjacent unit directions agree. Thus the active index set and the locations of all active vertices agree. Endpoint gradients have norm one and the endpoints are active. Along an inactive chain, the differences of corresponding edge vectors are longitudinal. Summing them from the preceding common active vertex proves the stated longitudinal form of any remaining nonuniqueness.

This proof does not assert uniqueness of every inactive vertex, physicality of the complete comparison polygon, or a continuation through an omitted obstacle. None of those stronger conclusions is needed. The case with one flight is covered by the same endpoint and triangle-equality argument.

## 2. Exact hard-interval work and the strict layer contraction

Use the inherited notation `delta_i = Y_i-Q_i`, `e_i = vhat_i-v_i`, `H_i = c_i |delta_i|^2`, and `F_i = ell_i |e_i|^2`. The original variational inequality is

\[
 (e_i-e_{i-1})\cdot\delta_i\ge H_i/R.
\]

Its sign agrees with the disk support inequality at the reference and the minimum inequality at the comparison point. On an interval with anchor endpoints `u<v`, finite summation by parts yields

\[
 \frac1R\sum_{u<i<v}H_i+
 \frac12\sum_{u\le i<v}(\ell_i+\tau_i)|e_i|^2
 \le e_{v-1}\cdot\delta_v-e_u\cdot\delta_u.
\]

The exact edge identity `e_i dot (delta_{i+1}-delta_i) = (ell_i+tau_i)|e_i|^2/2` fixes the sign and the coefficient. Both boundary flights occur in this identity; neither can be silently removed.

At each endpoint, Young's inequality with coefficient `tau_-/4` pays the boundary work by `tau_- |e|^2/4 + |delta|^2/tau_-`. An edge incident to one cut retains at least `ell_i |e_i|^2/2`. When `v=u+1`, the same flight pays both endpoint terms; its remaining coefficient is still at least `ell_i/2` because `tau_i >= tau_-`. Thus the hard-interval lemma is valid even with no interior contact. The endpoint inequalities `|delta_u|^2 <= H_u/a_0` and `|delta_v|^2 <= H_v/a_0` use reference anchors only. No incidence or activity assumption about the comparison minimum enters this payment.

For the full depth energy, the positive gap gives `E_0 <= G <= E_R(Q)`. Contact and flight energies spend one shared positive budget. Replacing this by two separate copies of the deficit would weaken the constants, but is unnecessary and is not done.

If `2(d+N)>m`, the inner energy is empty. Otherwise the original physical `N`-flight turning bound supplies anchors

\[
 u\in[d+1,d+N-1],\qquad
 v\in[m-d-N+1,m-d-1].
\]

They satisfy `u < d+N <= m-d-N < v`. All inner energy terms are included in the hard interval. Both anchor contact terms lie in the removed shell `E_d-E_{d+N}`. This yields

\[
 \mathcal E_{d+N}\le
 \frac{r}{a_0\tau_-}(\mathcal E_d-\mathcal E_{d+N}),
 \qquad
 \mathcal E_{d+N}\le q_{\rm a}\mathcal E_d.
\]

The exact rational computation is

\[
 a_0=1/416640,\quad r=47/100,\quad \tau_-=3/50,
 \quad\kappa=3263680,\quad
 q_{\rm a}=3263680/3263681.
\]

The case `m=2(d+N)` retains a single central contact and is covered by the strict anchor inequalities above. Iteration on depths `0,N,2N,...`, followed by monotonicity, gives `E_d <= E_R(Q) q_a^floor(d/N)` for every depth. Anchors may be chosen afresh at every layer; no compatibility of these choices is required. All constants are uniform in the original word, radius, length and global minimum. The fixed-word physical closure is allowed because the physical turning/anchor statement and the variational inequalities are already available there. This is a deterministic estimate through inactive minima, not an integration of derivatives along an assumed smooth physical branch.

## 3. Shared-energy localization and failure witnesses

For depths below `N`, the already proved global position and transverse budgets apply with exponent zero. At depths at least `N`, the local interval `[d-N,m-d+N]` contains the required central target positions and flights. Its positive contact and flight terms are jointly bounded by `E_{d-N}`. The constants therefore combine by a maximum:

\[
 S_d\le\max(rA_H,2A_F)\mathcal E_{d-N},\qquad
 \sum\beta_i^2\le\max(rB_H,2B_F)\mathcal E_{d-N}.
\]

The explicit rational inequalities `max(r A_H,2 A_F)<10^8=C` and `max(r B_H,2 B_F)<B_G+B_E` hold for the inherited displayed constants. In particular `r A_H` is approximately `97,848,470.58`, and `r B_H=166,401,368.08`, below `B_G+B_E=167,592,641.36`. These numbers only check the algebraic comparison; the exact rational inequalities are what the proof uses. The exponent is exactly `j(d)=max(0,floor(d/N)-1)`; the one-layer shift is retained.

At an inactive internal comparison contact, `2c_i <= |e_i|+|e_{i-1}|`. Both adjacent flights lie in the energy at depth `d_i-1`, including when `d_i=1`. Their nonnegative sum yields

\[
 c_i^2\le E_R(Q)\tau_-^{-1}
             q_{\rm a}^{\lfloor(d_i-1)/N\rfloor}.
\]

The transverse witness is a single summand of the full transverse budget. Its conversion to an original clearance witness uses the strict strip regime `beta_i<tau_-/2`; 309 enforces this regime explicitly. These conclusions hold for every minimum simultaneously, so selecting a particular minimizer is not necessary to define the bad original source.

## 4. The exact section collar and outgoing collision states

The original section is the union of four squares of side `1/100` and one rectangle of sides `3/25,3/10`. For `rho<=1/200`, each rectangle satisfies the required inner-collar condition `2rho<=min(w,h)`. Its closed boundary collar has coordinate area at most `4rho(w+h)`. Equality at an inner degenerate rectangle is harmless, because the boundary has zero coordinate area. On the angular circle a coordinate-seam crossing has the same area; any clipping at the momentum boundary decreases it.

The boundary of a finite union is contained in the union of the individual boundaries. Summing their areas gives `4rho * (1/2)=2rho`. Multiplication by the actual invariant density `1/(4pi)` proves the exact source estimate `nu(section collar)<=rho/(2pi)`. No independence or disjointness of the collars is asserted.

At an active internal comparison vertex, the coordinate minimum condition gives a point on the original circle and an exterior specular pair of directions with strictly positive incidence. Hence the outgoing phase state exists, with `|p|<1`, even before proving that the two listed adjacent flights are first-hit flights. The phase estimate is a comparison of these collision coordinates. It does not prematurely identify a complete physical orbit.

The elementary estimate is

\[
 d_\infty(x_i,\widehat x_i)^4
 \le 8|e_{i-1}|^4+24R_-^{-4}|\delta_i|^4.
\]

Since a difference of unit vectors has norm at most two, the first term is bounded using the actual flight energy at depth `d_i-1`. The index inequality `floor((d_i-1)/N)>=j(d_i)` is correct for every `d_i>=1`, including exact multiples of `N`. The contact term follows from the position budget. Enlarging the resulting coefficient `64/tau_-` to the common `128/tau_-` is valid and supplies

\[
 K_\phi=128/\tau_-+24C/R_-^4.
\]

This point-state estimate also covers the central singleton contact when the record length is even.

## 5. The logarithmic source threshold

Write `q=q_a`. Let `M` be the maximum inside the numerator of the displayed threshold in 309. With

\[
 J_{\rm obs}=1+\lceil M/(-\log q)\rceil,
 \qquad D_{\rm obs}=N J_{\rm obs},
\]

every `d>=D_obs` has `j(d)>=ceil(M/(-log q))`. Consequently `q^{j(d)}<=exp(-M)`. The three entries of `M` imply, respectively,

\[
 A_\Gamma q^{j(d)/2}\le\delta_{\rm flux}/2,
 \quad A_cq^{j(d)/2}\le1/2,
 \quad A_\phi q^{j(d)/4}\le h_0.
\]

The maximum with zero handles nonpositive logarithmic entries correctly. The first bound gives both the required strict flux range and the strict strip regime. The threshold is fixed before all collision limits. Its conservative size does not change either the original guard constant `q_0=47/53` or the microscopic guard schedule. The proof never identifies `q_a` with `q_0`.

## 6. Full positive source, one conditional normalization, and the geometric tails

The event in 309 is defined by explicit original all-center clearances, original incidences, and original distances to the unchanged section boundary. These are Borel functions on the actual regular collision records; at fixed `R,m` the union is finite. There is no measurability inference from an uncountable projection of auxiliary minima.

For any original Borel roof set, multiply the elementary union bound first by the exact original event, the bounded positive factor `0<=h<=1`, and the original roof indicator. Then integrate against `nu_R^*=c_*^{-1}1_{Y_R^*}nu`. Only on the upper side are these factors discarded. This pays `c_*^{-1}` exactly once. The roof remains the full original `L_R(Q)` throughout.

The source estimates at a single index are the actual flux `nu(Gamma<=u)<=u/R`, the exact incidence law `1-sqrt(1-u^2)<=u^2`, and the just-proved section collar `rho/(2pi)`. The closed clearance event is obtained by decreasing open widths inside the strictly valid flux range. Collision-measure invariance transports the estimates to each index. There is no collision independence assumption.

There are at most two indices at any depth, and at most `N` depths in a block with fixed `floor(d/N)`. For `D>=N` and `alpha>0`,

\[
 \sum_{d\ge D}q^{\alpha j(d)}
 \le\frac{Nq^{\alpha j(D)}}{1-q^\alpha}.
\]

Using `alpha=1/2,1,1/4` gives exactly the three coefficients printed in 309:

\[
 \frac{2N A_\Gamma}{R_-c_*},\qquad
 \frac{2N A_c^2}{c_*},\qquad
 \frac{N A_\phi}{\pi c_*}.
\]

Their denominators are respectively `1-sqrt(q)`, `1-q`, and `1-q^(1/4)`. The contact-collar coefficient correctly includes the two-depth multiplicity and the factor `1/(2pi)`. The finite full physical source is included before extending its depth sum to the infinite geometric tail and before taking any radius, label, time-length or bounded-weight supremum.

The resulting positive measure bound is uniform total mass, and therefore total variation. It does not use a lower bound for a microscopic conditioning probability. It does not establish essential roof height, and no density statement for the exceptional source is inferred from the mass estimate.

## 7. Simultaneous physicality and exact central labels

Outside the explicit incidence event, the inactive-contact witness contradicts the strict lower original incidence at every included depth, for every global minimum. Thus every included comparison contact is active. Outside the explicit clearance event, the transverse witness and the strict strip lemma provide positive clearance from every third disk on each included flight. The exterior specular law keeps this flight outside the two incident disks. Consequently its listed next contact is the true first hit; there is no unlisted ghost collision.

Outside the explicit section event, the original state's boundary distance is strictly greater than its uniform phase discrepancy. The unchanged section indicator therefore agrees at each central contact, including the terminal one. The common ordered centers give exact central displacement and collision count. Occupation is summed over `[D,m-D)` and the terminal section test is separate. No original selector is changed or smoothed, and no outer endpoint of the comparison polygon is declared physical.

All bounds are simultaneous over the minima. Neither unique minimizers nor a measurable minimizer selection is needed for the source-complement conclusion. The common-active-geometry lemma is consistent with this conclusion, but the source proof does not depend on a uniqueness assertion.

## 8. Original roof costs, conditional density payment, and Fourier scope

On the actual central subrecords, the exact finite clock identity gives

\[
 T_d^{\rm clock}=R^{-1}\sum_{d<i<m-d}H_i
                   +\tfrac12\sum_{d\le i<m-d}F_i.
\]

It is contained in the depth energy, so its exponential upper bound has coefficient one times `E_R(Q)`. The endpoint work `W_d` is retained exactly. The uncorrected physical clock difference is not identified with this positive bulk cost.

For the full central phase sum, the incoming direction at the terminal state duplicates only the last included edge. The bound `64/tau_- sum F +24R_-^{-4}S_d` therefore yields the common `K_phi`. The transverse cost is the full transverse budget. All of these costs use the original full roof, exact event and one conditional measure in their positive pushforwards.

The displayed unscaled roof-height payment is conditional on precisely native Input `v112-geometric-pressure` and the already specified original pressure/roof-angle identities. This input is not replaced by finite convexity or by the source mass estimate. The persistent low-load factor is covered because its previously proved one-copy coefficient satisfies `0<=h<=1`. Arbitrary unbounded optical or singular boundary weights are outside this statement.

For `d_m=ceil(theta m)`, fixed `0<theta<1/2`, the inequalities `2d_m<m` and `d_m>=D_obs` hold for all sufficiently large `m`. The index estimate `j(d_m)>=theta m/N-2` gives `q^{j(d_m)}<=q^{-2}exp(-lambda_0 m)`, where `lambda_0=theta |log q|/N`. The fixed factor `q^{-2}` is legitimate before all uniform suprema. Multiplication by the original `m^2` normalization still gives decay of the specified costs.

On the source complement, every central section decision agrees exactly. Thus the exact Fourier comparison has zero occupation-label error and only the clock error bounded by `|s| T_d^{clock}`, with the endpoint roof phase retained. The estimate is uniform over all lattice and return twists and `|s|<=exp(lambda m)` for each fixed `lambda<lambda_0`. This is a pointwise frequency-range comparison under the stated source/pressure scope; it is not a bound on the complete unbounded-frequency integral.

## Conclusion and precise remaining scope

The final 308–309 proof bodies pass this internal reconstruction of signs, interval endpoints, shared budgets, source coefficients, logarithmic depth threshold, Borel definition and conditional normalization. The formal 305 application-scope issue was corrected explicitly before this freeze. No further mathematical gap was found in these stated implications.

The new mechanism proves an exponential deterministic contraction and a uniformly vanishing complete deep physical/section failure source in original-source total mass. The specified comparison costs additionally have conditional original-roof height payment. The full raw pointwise local limit theorem remains distinct: the shallow source, normalized density of the exceptional source, full guarded comparison-pool capacity, paired singular boundaries, microscopic conditional probabilities and necessary full spectral-frequency estimates must still close the original ordered shortage limit. The new `D -> infinity` source limit is not substituted for the required outermost `B -> infinity` limit. All these restrictions are present in the inspected statements and are essential to their accuracy.
