# Response to the external v36 referee report

**Manuscript:** Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_

**Revision:** A2 v37, 4 October 2026

**Controlling report commit:** `3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`

**Reviewed author commit:** `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`

We have revised the paper around the two substantive questions in §7 of the
report: a general scalar inverse and rigidity principle beyond a supplied
periodic presentation, and the unresolved polynomial stationary sample gap.
The new Sections 2–4 give complete proofs addressing both questions. The title,
collision observation, geometric reconstruction problem and earlier results
are retained. The six distinctions requested in §6 are explicit in the
introduction and in the corresponding statements.

The principal changes are the following.

| Question in the report | New result | Location |
| --- | --- | --- |
| Can the exact scalar response determine crystallinity without assuming periodicity? | Global occupation inverse and equality of the complete response and configuration period groups | Theorems 2.2 and 2.4, pp. 5–7 |
| Can the supplied common homothety origin be removed? | Scale and footprint recovery with independent unknown setting translations and no cross-setting component correspondence | Theorem 3.2 and Corollary 3.3, pp. 8–9 |
| Is there a finite counterpart with the additional controls charged? | Periodic and finite nonperiodic reconstruction with explicit registration and resource bounds | Theorem 3.5 and Corollary 3.6, pp. 10–12 |
| Is the stationary upper power necessary? | Uniform short-command Hellinger contraction, a matching stopped-transcript lower bound and a one-logarithm upper bound | Lemmas 4.1–4.3, Theorem 4.4, Proposition 4.5 and Corollary 4.6, pp. 13–19 |

## 1. The global exact inverse and full period group

The exact global theorem is formulated before the finite periodic theory.
Let `O` be any nonempty locally finite union of compact convex bodies with
nonempty interiors, common diameter bound `D`, and mutual separation at least
`d`. A stationary launch law has an unknown convex footprint of diameter at
most `Delta` and an integrable density positive almost everywhere on its
interior. We fix a compass step satisfying `t+Delta<d`.

The available raw means are `F,R`. Their difference `g=F-R` obeys
`g=(T-I)v`, where `v` is the occupation field. Its positive components are
the separated expanded bodies `C+(-A)`. The new inverse does not ask for these
components, an aperture containing them, or the launch density as input.

Lemma 2.1 proves a common exit-time bound

`H=(D+Delta+t)^2/t^2`,

and a geometric block-tail estimate for the virtual compass walk. Theorem 2.2
then proves both the stopped variational formula and the constructive iteration

`v_0=0`, `v_(N+1)=max(0,T v_N-g)`.

The error is bounded uniformly by `2^(-floor(N/ceil(2H)))`. On the admissible
class the inverse is Lipschitz, with constant `H`. Corollary 2.3 quantifies the
finite region of forcing values needed for a fixed number of iterations and
the accumulated effect of forcing error.

The inverse commutes with translation. A period of `g` therefore permutes the
expanded positive components. Convex support-function cancellation removes
their common footprint. Conversely a period of the obstacle union preserves
both physical response means. Theorem 2.4 obtains

`Per(F,R)=Per(g)=Per(v)=Per(O)`.

The period group is discrete because a nonzero translation cannot preserve one
compact component and distinct components are separated. Two independent
response periods therefore characterize rank-two crystallinity. The theorem
does not assume a periodic presentation, a finite species list, smoothness or
a positive nonperiod-patch margin.

The data are the exact full response fields of the original collision
experiment. This full-field assertion has different acquisition quantifiers
from a uniform decision based on finitely many observations in one fixed
window. The retained finite period theorem continues to state its patch
margin. The old finite-patch discussion has been reconciled with the new exact
criterion without changing its proof.

## 2. Homothetic reconstruction with no supplied origin

The v36 direct-width normalization is retained and extended. At setting `i`,
write the physical footprint as

`A_i=b_i+rho_i A_0`, `s(A_0)=0`, `rho_1=1`.

Every setting translation `b_i`, the footprint and the scale ratios are
unknown. At least two scales are distinct. Densities may differ from setting
to setting. Exact homothety and the setting labels remain part of the model.

Choose any expanded component `P` at setting `i`. Its collision-width deficit

`d_i=W(P)-(2/t) integral_(E_P) F_i = W(A_i)`

is independent of the obstacle chosen. It follows that `rho_i=d_i/d_1`.
This removes the component-matching cone used by the retained fixed-origin
construction. No identical shape, asymmetric component or species label needs
to be selected across settings.

For the exact possibly infinite collection, let `L_i` be the pointwise lower
envelope of the Steiner-centered supports of all its expanded components.
Steiner centering and support addition give

`L_i(u)=inf_C p_C^circ(u)+rho_i p_(-A_0)(u)`.

The same obstacle term occurs at every setting. Thus, for any `rho_k!=1`,

`p_(-A_0)=(L_k-L_1)/(rho_k-1)`.

The lower envelope need not attain its infimum and need not itself be a support
function. Uniform diameter bounds make it finite and Lipschitz; the exact
identity proves that its displayed difference is the required physical support.
Subtracting the footprint addend from each laboratory support reconstructs
`O-b_i`, including its first harmonic. This is Theorem 3.2.

Corollary 3.3 gives the entire geometric fiber, in both directions. Two
experiments with identical response pairs have geometries related by

`O'=O+h`, `A_i'=A_i+h+pi_i`, `pi_i in Per(O)`.

Conversely every such transformation preserves the collision laws, by coupling
the launch offsets with the same translations. The nuisance densities are not
asserted to be uniquely identified. Relative setting translations are recovered
as cosets modulo the full obstacle period group. A finite nonperiodic union has
no nonzero translation period, so its relative translations are ordinary
vectors.

Theorem 3.5 gives the finite periodic reconstruction. A fixed scale-gap bound
controls inversion. A known coarse bound on the unknown `b_i` keeps the
required acquisition region within a fixed aperture. Primitive-orbit averages
replace the exact infinite envelopes. Lemma 3.4 proves that adding a common
centered support preserves the periodic matching defect, including the
reduction of center-difference candidates into the protected patch. The
registration search has an explicit bounded integer enumeration. This supplies
the finite consequences instead of treating the exact envelope formula as an
algorithm for an infinite list.

Corollary 3.6 treats a finite nonperiodic configuration with a known bound on
its component count and a protected aperture containing all components and
response envelopes. Component averages replace primitive-orbit averages;
averaged Steiner points recover the relative translations. Neither periodicity
nor a nonperiod-patch margin is needed in this corollary.

## 3. The stationary exponent

The report's v36 bracket had lower power `(s+1)/(s-2)` and upper power
`(3s/2+1)/(s-2)`, for `s=6+beta` and a uniform-disk law. The new lower bound
has the latter power and retains the stronger arbitrary-short-command design.

The essential estimate is proved directly for collision sweeps. For a nearby
smooth physical body `C`, a launch disk `D`, and any command `te`, write

`A=area(D intersect ((C+[-te,0])\C))`.

The derivative of this area along a support interpolation has two curved
boundary contributions. They cancel where the paired original and swept
points both lie in `D`. Only active arcs and sweep facets remain. Lemma 4.1
bounds their effective normal-variation measure by
`C min(A, area(D)-A)^(1/3)`. The proof includes both collision and complementary
area and is uniform in all centers and directions, including `t` tending to
zero. In the physical packing it is enough to prove this estimate in a fixed
small `C^2` neighborhood of the disk, which is the stated geometric class.

Lemma 4.2 integrates that derivative estimate and proves

`H^2(Ber(P_0),Ber(P_1)) <= C epsilon^(3/2)`

when the support discrepancy is at most `epsilon`. The proof handles means
at zero and one; no positive lower bound on a collision probability is imposed.
Lemma 4.3 converts the Hellinger diameter of a Bernoulli family into a
posterior-uniform mutual-information bound.

The retained physical packing has `log M` of order `h^(-1)`, centered `C^2`
separation of order `h^(s-2)`, and support diameter of order `h^s`. The command
capsule is enlarged by the uniform packing perturbation to select the same
indexed physical component across all parameters. Thus the conditional
information in every attempted response is at most `C h^(3s/2)`, even after
an adaptive history. The stopped-transcript argument then proves

`sup_O E_O T >= c nu^(-(3s/2+1)/(s-2))`.

The lower theorem permits exact nominal positions, arbitrary controlled
directions, lengths in `[0,t_max]`, and a disclosed positive compact interval
of disk radii. The actual launch realization is unobserved, as in the original
experiment. It does not rely on excluding very short commands.

Proposition 4.5 improves the upper construction by using a layer proportional
to the current radial bracket width. A safeguarded update contracts every
bracket by `3/4`, whichever binary label occurs. Confidence allowances increase
toward the more expensive fine levels; their geometric cost sum removes one
logarithm while preserving a deterministic cap on the total attempts.

Corollary 4.6 states the final comparison on one bounded physical class, one
common disk-law experiment, the same accuracy, confidence, and worst-case
expected-cost criterion:

`c nu^(-q_0) <= N*_short <= N*_pool <= C nu^(-q_0) log(C/(nu delta))`,

where `q_0=(3s/2+1)/(s-2)`. The pooled compass is a subdesign of the allowed
short commands. The upper deterministic cap also bounds expected cost. Hence
the polynomial gap is closed for both designs. The remaining logarithm and
sharp confidence dependence are not resolved by this corollary. The broader
unknown-density upper theorem is retained without declaring its power sharp
for every boundary-mass exponent or for launch radii tending to zero.

## 4. Point-by-point response to the qualifications in §6

### 6.1. Raw mean pairs and reciprocal differences

The abstract and §1 now call the datum a pooled reciprocal response pair.
Sections 2 and 3 define `g=F-R` explicitly. The global occupation inverse uses
`g`; the new footprint deficits use the raw forward means `F_i`. The
independent area normalization in §8.3–8.4 remains a theorem from reciprocal
differences alone, with its full smaller-root and finite-adjoint proofs. We
do not infer a forward-width integral from a difference-only data field.

### 6.2. Locality of the rare query

The introduction states that every rare query lies in the protected tubular
neighborhood of an acquired component bracket. Proposition 7.2 retains the
complete local hypothesis and proof. The shrinking-layer construction stays
inside the original bracket neighborhood and reserves room for rounding.
Global recovery is supplied by the independently proved stopped-Poisson
theorem, not by extending the rare-query exterior-zero assertion to arbitrary
centers.

### 6.3. Centers, batches and repetitions

Section 1.4 defines `N` as attempted bits, `J` as center-labelled batches with
later revisits counted again, and `S` as distinct spatial sites. A randomly
sampled center for a scalar integral is one single-attempt batch. In particular
`S<=J<=N`. With `q_gamma=((gamma+3/2)s+1)/(s-2)`, Theorem 3.5 gives

`N <= C nu^(-q_gamma) log(C/(nu delta)) + C nu^(-2) log(C/delta)`,

`S <= J <= C nu^(-1/(s-2)) log(C/nu) + C nu^(-2) log(C/delta)`.

Both formulas retain the normalization term. The finest nominal mesh is
`O(nu^(s/(s-2)))`; the batch list, including settings and repetition counts,
has description length at most `C J log(C/(nu delta))`. These are observation
and digital-control bounds. Physical travel and metrology are not assigned
zero cost by these formulas.

### 6.4. Stronger separation for the faster design

Equation (1.7) prominently requires `2t+max_i diam(A_i)<d_0` for the rare-query
and unregistered flux construction. The adjacent paragraph states the weaker
`t+max_i diam(A_i)<d_0` requirement of the retained signed-query construction.
The sharp minimax corollary explicitly chooses its pooled step within the
stronger design class. The retained comparison of the older bounds has also
been reconciled with these conditions.

### 6.5. What homothety supplies and what is recovered

The v36 fixed-origin result remains intact. The new Section 3 removes the
supplied origins and recovers independent setting translations modulo the
exact geometric gauge. It also dispenses with cross-setting component
correspondence. Exact homothety and labelled settings remain assumptions;
quantitative finite stability retains a scale gap and geometry bounds. For
bounded-aperture acquisition the unknown translations have a known coarse
bound. These conditions are stated where they are used, rather than hidden
in the term calibration.

### 6.6. A matched minimax criterion

Corollary 4.6 defines both infima over the same physical class and success
criterion using worst-case expected attempts. The lower theorem applies to a
more informative command class containing the upper design, and its loss is
weaker than the reconstruction loss. These inclusions justify the complete
chain of inequalities. The larger unknown-density upper class is discussed
separately from this fixed-common-disk minimax conclusion.

## 5. Historical derivations, literature and presentation

The source audit pins the latest report and reviewed author tree. We read the
earlier unregistered, intrinsic-period and finite-aperture arguments in v17,
v19 and v21, as well as the rate and calibration sources used by v36. Their
analytic network, image, label and periodic-cover observations are not
identified with the present scalar collision field. The historical ledger
records the native source identities and the precise dependencies.

Section 10 credits the classical potential-theoretic, convex-geometric,
boundary-estimation and information-theoretic ingredients. The focused
literature audit adds unknown-probe morphological reconstruction and weighted
cap geometry, explaining their different observations and losses. The new
claims concern the positive occupation inverse, its full-period consequence,
the unregistered geometric fiber and the uniform physical Hellinger estimate.

The primary uses the `amsart` theorem-proof structure. The exact inverses and
sharp statistical theorem now lead the mathematical narrative. All nineteen
reviewed core inputs remain active; all 162 reviewed labels and all 43
reviewed proof bodies are retained, with the latter byte-identical. The 65-page
revision contains sixteen additional proved formal statements. The complete
localized and calibration developments remain in Appendices A–H.

## 6. Source delivery and verification

The report correctly records that v36 had already repaired source delivery.
Version 37 continues that working mechanism and pins the new manuscript and
workflow. It does not present the old v35 defect as an unresolved issue in the
controlling report.

The validator checks all active source inputs, preserved trees, historical
proof bodies and labels; runs finite diagnostics and contract checks in normal
and optimized Python; and compiles the actual primary. A publication run is
bound to the exact checkout SHA. The hosted artifact includes the PDF, complete
source archives, final log, source pins, receipt and binding. The receipt is
the authority for the result of that particular run. The finite diagnostics
support the displayed finite identities and edge cases; the mathematical
proofs are in the article. This revision is submitted for renewed assessment
of the expanded theorem package.
