# Response to the controlling A2 v36 referee report — v38

We thank the referee for distinguishing the successful mathematical repairs
in v36 from the remaining questions about the stationary exponent and the
scope of the inverse. We retain the original topic and every proof in the
intervening v37 manuscript. The controlling report is the report at
`3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`, reviewing author source
`2559749a038fd2b5ec46d7cc74fdb4bd844b266a`. The immediate source of this
further revision is v37, `02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d`.
A newer referee report is not assumed or invented.

## 1. The two substantive questions in report section 7

The existing v37 response proves exact response-period rigidity without a
periodicity prior, removes the supplied homothety origins and component
matching, and matches the stationary polynomial exponent on one common
uniform-disk experiment. Those proofs are preserved without alteration in
`14_global_response.tex`, `15_unregistered_footprints.tex`,
`16_sharp_stationary.tex`, and `16a_shrinking_upper.tex`. They are not
represented as new v38 achievements. The remaining logarithmic factor is
stated explicitly. These are theorem claims for fresh mathematical review,
not conclusions of a journal or a proof assistant.

The new sections strengthen the connection between the exact invariant and
its active data, rather than changing the problem. `17_finite_stencil.tex`
proves that the exact occupation at one point is a finite-dimensional
functional of a fixed set of scalar response values. The same functional
has a uniform modulus for arbitrary corrupted data, not only for a pair of
physically admissible experiments. Its numerical output has primal and dual
certificates. This removes the iteration-horizon factor in noisy evaluation
and yields an explicit epsilon^-2 occupation sampling law with a fixed
number of nominal sites.

`18_isotropic_rigidity.tex` shows that the exact inverse is not specific to
a four-direction compass. The exit argument uses bounded increments, zero
mean, positive second moment, and separation. For uniform directions the
calibration scalar is a perimeter deficit, independent of a chosen axis.
The resulting origin-free geometric inverse and complete ambiguity theorem
retain arbitrary separated convex configurations and unknown launch laws.
Neither result is presented as a passive trajectory or spectral theorem.

## 2. Raw mean pairs versus differences — report section 6.1

The fixed-stencil inverse and general displacement period theorem use only
`g = F-R`. The component width and perimeter deficits require the raw forward
mean `F`. The retained killed-adjoint area normalization remains the route
that uses reciprocal differences alone. The abstract refers to mean pairs
when it discusses footprint deficits; the new isotropic section ends with
this distinction. No raw-mean statistic is attributed to difference-only data.

## 3. Local rare query — report section 6.2

The one-sided rare collision remains local to the protected tubular bracket
of one isolated expanded component. The new global pointwise occupation
inverse does not assert that the rare event is a global membership test.
An important separate issue is proved in the finite-stencil theorem: a
computational killing boundary may contain other physical positive
components. Every stopping payoff is bounded above by nonnegative terminal
occupation, and the target's containing-component exit attains equality.
No physical boundary-zero oracle is inserted into the algorithm.

## 4. Controls and resource accounting — report section 6.3

For the new pointwise experiment, `M=(2K+1)^2` is the number of distinct
nominal sites, `2M` is the number of forward/reverse command-labelled batches,
and every repeated Bernoulli attempt is included in the displayed budget.
The stencil depends on the prior diameter-to-step ratio, not the requested
accuracy. Exact rational targets and step sizes give rational programs;
precision of the empirical means and arithmetic is accounted separately.
A supplied coarse footprint-location bound is still needed to turn a nominal
stencil into a predetermined bounded physical launch aperture. Manufacturing,
metrology, and travel costs are not silently included in a bit count.
The retained finite boundary reconstruction continues to count sampled
normalization centers separately from boundary-search sites.

## 5. Separation margins — report section 6.4

The general reciprocal inverse requires `ell + Delta < d`; the compass
special case is `t + Delta < d`. The retained rare-collision construction
requires the stronger `2t + Delta < d`. Isolated width and perimeter
normalizations also state their stronger separation explicitly. These are
different hypotheses for different parts of the result, not an unannounced
change in the comparator class.

## 6. Homothety and registration — report section 6.5

The retained v37 theorem learns independently translated footprint origins,
relative scales, and the centered physical first footprint. The new isotropic
theorem proves the same complete geometric ambiguity without a preferred
axis: a common translation and independent footprint shifts by obstacle
periods. Exact homothety, setting labels, and prescribed reciprocal joint laws
remain assumptions. The densities need not be scaled copies. Distinct scales
suffice for the exact inverse; uniform finite stability retains a scale gap.
No physical certification of homothety is claimed from these theorems.

## 7. Matched minimax quantifiers — report section 6.6

The full v37 matching proof remains active. Its fixed positive uniform-disk
spread, common physical class, C2 geometric loss, fixed confidence and
worst-case expected-cost criterion are stated in the minimax corollary.
The lower bound allows the more informative class of arbitrary short commands;
the upper bound is realized by the pooled compass, so both classes have the
same polynomial power. One logarithm remains; sharpness for every density
boundary exponent or an isotropic finite acquisition scheme is not asserted.
The new fixed-stencil theorem estimates occupation and does not replace this
boundary problem by a weaker loss.

## 8. Presentation and reproducibility

The main article uses theorem--proof exposition and retains all inherited
arguments. New hypotheses are printed with their results. Historical change
logs, proof ledgers and validation receipts are outside the mathematical
narrative. All 24 inherited v37 core inputs are active and byte-identical.
The source validator checks this assertion rather than relying on prose.
The new finite diagnostics enumerate all 512 deterministic stopping policies
of a 3-by-3 killed walk and check the associated flow, budget, stability and
interval algebra. They also test a nonzero computational boundary and the
perimeter normalization. These checks do not certify continuum geometry.

We submit the strengthened manuscript for further referee assessment at the
requested benchmark. We make no claim that the editorial judgment is already
reversed or that a successful source build establishes the new theorems.
