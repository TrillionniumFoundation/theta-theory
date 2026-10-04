# Proof ledger — A2 v37

This ledger identifies the new arguments and their retained dependencies. It
does not replace the proofs. Result numbers refer to the native 65-page
primary; labels are stable source identifiers.

## 1. New proved statements

| Result | Label | Main dependency and proof obligation |
| --- | --- | --- |
| Lemma 2.1, uniform exit from a positive component | lem:global-exit | Quadratic compass martingale; a step cannot jump to another expanded component; Markov block-tail iteration |
| Theorem 2.2, global scalar-to-occupation inverse | thm:global-occupation | Reciprocal Poisson identity and Lemma 2.1; stopped payoff, positivity, comparison, unknown-set iteration and truncation |
| Corollary 2.3, finite-field locality | cor:global-field-locality | Finite compass reachability and the contraction of averaging followed by the positive part |
| Theorem 2.4, response rigidity for the full period group | thm:global-response-rigidity | Translation covariance of Theorem 2.2, separated component permutation, support cancellation and discreteness |
| Lemma 3.1, footprint deficit | lem:registration-deficit | Retained isolated flux identity and translation-invariant coordinate widths; arbitrary component choice |
| Theorem 3.2, geometric inverse without a supplied origin | thm:registration-rigidity | Global occupation, deficits, Steiner additivity and cancellation of the common support envelope |
| Corollary 3.3, complete geometric ambiguity | cor:registration-fiber | Theorem 3.2 and pointwise coupling under common translation and independent period offsets |
| Lemma 3.4, cancellation of the periodic patch defect | lem:registration-period-margin | Common support addition and equality of laboratory center differences; reduction by the presentation lattice |
| Theorem 3.5, finite unregistered reconstruction | thm:registration-finite | Retained coarse acquisition and period locking, Proposition 4.5, isolated scalar sampling, primitive-orbit averages and finite offset enumeration |
| Corollary 3.6, finite nonperiodic configurations | cor:registration-finite-cloud | Complete protected acquisition, component averages, centroid sums and the scalar deficit; no period decision |
| Lemma 4.1, effective collision boundary | lem:effective-collision-boundary | Convex sweep shape derivative; paired-arc cancellation; active-arc and facet strips in collision and complement |
| Lemma 4.2, uniform short-command Hellinger contraction | lem:all-short-hellinger | Lemma 4.1 along a support interpolation; bounded variation of the two 2/3 powers and 3/4-Hölder conversion |
| Lemma 4.3, binary information from Hellinger diameter | lem:hellinger-capacity | Relative-entropy radius at the endpoint midpoint and an exact Bernoulli Hellinger comparison, including endpoints |
| Theorem 4.4, stationary lower power for arbitrary short commands | thm:sharp-stationary-lower | Physical bump packing, common-index command capsule, Lemmas 4.2–4.3 and stopped Fano accounting |
| Proposition 4.5, shrinking-layer rare-collision controller | prop:shrinking-rare | Retained local rare query, certified radial brackets, safeguarded contraction, geometric confidence schedule and finite rounding |
| Corollary 4.6, stationary minimax power | cor:stationary-minimax | Theorem 4.4, Proposition 4.5, inclusion of command designs and conversion of a deterministic cap to expected cost |

## 2. Global occupation proof

The relevant stochastic walk is virtual. It is used to invert exact mean data,
and its stopping time is not treated as an observed physical free-start flag.
The physical experiment remains the reciprocal binary experiment.

Expanded components have diameter at most `D+Delta` and mutual gaps exceeding
`t`. Until exit, the virtual walk stays within the selected component; at exit
it has occupation zero, because a step cannot reach another component. The
quadratic martingale gives `E tau<=H` uniformly. Restarting the estimate after
each block gives the tail estimate.

For any allowed integrable stopping time, the stopped Poisson identity gives
the payoff `v(x)-E v(X_tau)<=v(x)`. The actual component exit attains equality,
although the reconstruction need not know that exit rule in advance. Comparing
the same class of stopping rules for two forcings proves the Lipschitz bound.
Finite-horizon dynamic programming gives the obstacle iteration. Using the
exit time truncated at the horizon proves the stated error bound.

The period argument uses whole functions on the plane. A response period is
an occupation period by the inverse; it maps each connected positive component
onto one such component. Equality of their support functions after translation
cancels the unknown footprint. Discreteness follows from separation of the
original components. A discrete rank-two translation group is a lattice, and
local finiteness leaves finitely many component orbits in a compact cell.

## 3. Unregistered support inversion

The width deficit is positive because every footprint is full-dimensional.
Choosing different obstacles at different settings leaves the deficit
unchanged. Consequently its ratio measures physical operating scale and
requires no cross-setting matching or common origin.

All centered component supports are uniformly bounded and Lipschitz. Their
pointwise infimum is therefore finite and Lipschitz even for an infinite
collection. Taking this infimum commutes with adding the same footprint
support. Distinct scale factors allow subtraction. No convexity or attainment
of the envelope itself is required.

The reconstruction uses centered supports only to identify the footprint.
It subtracts that recovered addend from the original laboratory support of
each component, so it retains the relative placement of components. Equality
of the reconstructed unions determines each registration coset. The converse
fiber proof moves an actual launch by `h+pi_i` and the obstacle union by `h`;
the period `pi_i` cancels in every collision indicator. It establishes
sufficiency for the complete binary laws, not merely for support positivity.

Finite periodic reconstruction uses a finite average over primitive component
orbits instead of sampling an infinite infimum. Support addition leaves the
centers and the matching defect unchanged. To apply the original bounded-patch
margin to a center difference, reduce each endpoint separately by the supplied
presentation lattice; the defect is unchanged by the resulting period shift.
Finite registration enumerates component-center differences and bounded
lattice coefficients. A known coarse bound on setting translations supplies
the aperture and enumeration bounds while leaving their values unknown.

For finite nonperiodic clouds, complete acquisition replaces period reduction.
Each setting contains one expanded component per original body. Component
support averages cancel the same shape average, and centroid averages identify
the relative translation. The argument does not require an ordering of the
components at different settings.

## 4. Uniform Hellinger geometry

The hard family lies in a fixed smooth neighborhood of a disk. The effective
boundary estimate is asserted and proved on that family; arbitrary smooth
convex bodies are not needed for the lower bound.

Parameterizing the entering arc by arclength, the sweep map has Jacobian
`|n dot e|`. Strict convexity and a small launch radius give at most two active
intervals and uniform local graph constants. In the middle half of an active
arc interval of length `ell`, `|n dot e|>=c ell`. The distance to the launch
circle and the length to its exit in the sweep direction yield a strip whose
area is at least `c ell^3`. The directional disk-exit length is at most the
physical command length precisely because the other paired endpoint is
outside the disk. Thus this estimate remains valid for tiny commands; it
does not divide by a fixed positive lower bound on command length.

Facet chords have the same cubic area bound. Inward normal strips on the
original boundary and outward normal strips on the swept boundary prove the
complementary estimate. Pairing the physical and swept curved derivatives
cancels the common interior part, leaving the effective active measure.

After normalization by disk area, the derivative estimate is
`|P'|<=C epsilon min(P,1-P)^(1/3)`. Both `P^(2/3)` and `(1-P)^(2/3)` vary by
`O(epsilon)`. Taking 3/4 powers yields the squared-Hellinger exponent `3/2`,
including endpoints. Parameter-independent random mixtures preserve the
bound. The geometry is uniform over all nominal centers and controlled
directions and over any fixed positive compact interval of allowed disk
radii in the stated small-radius range.

For the physical packing, enlarging the full command capsule by its uniform
Hausdorff perturbation selects a common indexed component throughout the
parameter family. The launch disk and swept segment cannot encounter two
components under the chosen strict separation. Responses from fixed
components are parameter-independent; responses from the variable component
satisfy the Hellinger bound. This establishes the conditional information
bound after arbitrary adaptive histories.

The entropy argument uses a stopped record, includes the controller's
independent seed, and obtains a bound by expected attempts through truncation
and monotone convergence. It never replaces expected cost by a deterministic
sample budget. Infinite expected cost satisfies the lower bound directly.

## 5. Shrinking layers and resource accounting

At bracket width `w_j`, use physical layer `e_j=w_j/(4A)`. A positive label
retains `[mid-Ae_j, upper]`; a negative label retains
`[lower, mid+Ae_j]`. On a successful query the true radius remains inside;
on every record the retained width is `3w_j/4`. This gives a deterministic
number of levels and attempt cap even on failure records.

For `M_h` radial searches and `K` levels, allocate per-test failure
`delta/(4M_h) * 2^(-(K-1-j))`. The total allowance is bounded, while the
geometric sums of level costs and confidence logarithms are dominated by the
finest scale. Therefore the boundary attempt cost has one logarithm. Nominal
rounding uses a reserve smaller than half the smallest layer and stays inside
the original protected tube. All endpoints and updates can be dyadic.

An integrated scalar sample is one fresh attempted bit at one sampled nominal
center. It contributes to both `N` and `J`, even if its coordinate was used
before; `S` counts unique coordinates only. The `nu^(-2)` scalar cost remains
explicit in the unregistered theorem. Digital descriptions include settings,
batch repetition counts and every batch center.

## 6. Retention and executable checks

All reviewed proof bodies are unchanged. The source gate compares the active
v37 closure against the pinned v36 closure and finds all 162 historical labels
and all 43 historical proof bodies. The active counts are 233 labels, 59 proofs
and 62 formal statements. No historical paper directory is overwritten.

The validation suite checks source identity, closure, historical preservation,
finite diagnostics, contract behavior under ordinary and optimized Python,
and the native TeX build. The diagnostics include finite models of the new
occupation, registration, layer-allocation and Hellinger calculations alongside
the retained tests. Their role is to expose finite algebra and implementation
errors. They are not substituted for the continuum geometric, stochastic or
inverse proofs listed above.
