# Author-team AI challenge: interior-posterior instrument realization

## Role and scope

This is a focused mathematical challenge by a separate author-team AI agent.
It is not an independent human referee report, proof-assistant verification,
or an editorial recommendation. The review inspected the full written proofs
in the following native sources, at these SHA-256 identities:

- `sections/39-instrument-realization.tex`:
  `82e89bdc449da8a7bb006eb1f94092ebe44cb86cf9cb383a6b1283f35a9952f0`.
- `supplement-r74-instruments.tex`:
  `0da5e3c4bb0df933ffbdf20ad21757f555ffa554d4e0253c5e8ec6b3e9e29ffc`.

No substantive mathematical gap was found in these scoped proofs. This is a
bounded author-side assessment and not a guarantee that no further error can
be found.

## Load-bearing steps checked

1. The pure-state distance is Hilbert--Schmidt chord distance on projective
   space and satisfies the triangle inequality. The invariant ball measure is
   `r^(2h-2)`, obtained by the squared-coordinate simplex distribution of
   normalized independent complex Gaussian variables.
2. A maximal family separated by more than `r=sqrt(eta/h)` has disjoint
   radius-`r/2` balls. The packing bound gives
   `K <= (4h/eta)^(h-1)`, and maximality gives an `r`-net. No equality of
   Euclidean vector distance and projective chord distance was silently used.
3. For a Hermitian test matrix with largest eigenvalue `a` and smallest `z`,
   the net gives support at least `a-(eta/h)(a-z)`. The inequality
   `ha-tr(H) >= a-z` has the correct direction and implies domination of the
   support function of the shrunken density body. Compact convex separation
   proves containment.
4. Each positive branch posterior is in that physical polytope. Multiplying
   its barycentric row by the actual state-dependent outcome probability gives
   a nonnegative outcome matrix. Zero-probability branches are genuinely zero
   positive operators and give zero rows. Summing over both outcomes and new
   labels gives one by trace preservation.
5. The initial state is an explicitly counted extra label. It is not an
   uncharged random preparation, unknown-input encoding, or hidden extra call.
   The operator intertwining identity covers the empty history as well as the
   first actual command-outcome operation.
6. Taking traces of the full operator identity gives history laws; pairing
   with a terminal effect gives the terminal laws, including a POVM chosen
   from the visible history. The same policy kernels multiply both laws.
   Cylinder equality extends to path laws; almost surely finite stopping and
   the bounded-score/nonnegative-cost assertions follow as stated.
7. The exceptional cases `eta=1` and `h=1` are correctly separated. The
   physical-dictionary count is not advertised as an optimal unrestricted
   simulator count or an efficient computation bound.
8. In the dictionary lower proof, `lambda_max >= 1-s > 1/2` makes the largest
   eigenvalue simple and bounds all remaining eigenvalues by `s`. With
   `x=|<psi,u>|^2`, the inequality
   `<psi,sigma psi> <= x+s(1-x)` gives
   `1-x <= s/(1-s)`. The cap-measure and union bounds prove
   `K >= ((1-s)/s)^(h-1)`. Thus the fixed-dimension small-noise exponent is
   matched for the declared universal physical-dictionary problem.

## Nonblocking constructive refinement

If exact algebraic dictionary construction is separately asserted, it can be
made explicit. Pure projectors with algebraic entries are dense. A greedy
selection of algebraic centers at mutual distance greater than `r` terminates
by the same packing bound. If the current family fails to cover with closed
radius-`r` balls, continuity supplies an algebraic witness at distance greater
than `r` from all current centers. For algebraic `eta`, real quantifier
elimination can decide that condition and produce an algebraic witness.
Afterward the branch decompositions are finite linear feasibility problems.
This is a terminating exact construction, without a practical complexity
claim. The current scoped theorem already proves existence without relying
on this additional algorithmic statement.

## Additional exact diagnostic actually executed

`diagnostics_r74_instruments.py` constructs a distinct seven-label example:
six pure Pauli states as an octahedral core, plus a known pure preparation
with Bloch vector `(0,3/5,4/5)` as the counted initial label. The two commands
are projective measurements on the `z` axis and axis `(3/5,0,4/5)`, followed
on every observed branch by depolarization of strength `eta=3/4`.

The commands have genuinely state-dependent outcome probabilities; their
unconditioned channels are noncommuting. Two zero-probability rows occur.
The script checks exact Choi positivity and a CP posterior-noise certificate,
all branch/operator identities on all seven labels, and the full
subnormalized operators of every command-outcome history through length
four. Full Bloch coordinates include the imaginary Pauli direction.

It also enumerates two specified bounded policies: one deterministic
feedback/first-success stopping rule and one randomized visible-history
command-and-stopping rule. A history-dependent terminal POVM is included.
Their stopped laws, bounded score expectations and nonnegative call-cost
expectations agree exactly. These finite policies are diagnostics; the
universal adaptive theorem rests on its written proof.

The script completed under both ordinary Python and `python -O`, with
byte-identical JSON reports:

- **873 exact checks; zero floating probes.**
- Diagnostic source SHA-256:
  `f5c3222e01e88b6630e3904a9634d46b75aeb1b2d2414fb571bdd1a82ab796af`.
- Ordinary and optimized report SHA-256:
  `0290cd88f9b61d96f4787e91035e4913aff5372408bfc9b565752c55bc11f920`.

The report records each group's actual count and exact rational expected
costs/scores. No test depends on Python `assert`, and no minimality of this
seven-label example or lower bound for arbitrary hidden realizations is
inferred from its construction.

## Addendum: algebraic construction and synopsis quantifiers

The algebraic construction proposed above has now been incorporated into
`sections/39-instrument-realization.tex`. I reread the revised native proof
and its closing algorithmic paragraph at SHA-256
`f8e6af94a79bda8a98cb675966777b9c9a1ea7a8ebe533ec61e40b14483b66ac`.
This addendum extends the earlier scoped review; the earlier source hashes
remain recorded above and are not replaced retroactively.

The added argument is valid. A complex Hermitian rank-one projector can be
described in real coordinates by polynomial equations `P*=P`, `P^2=P`, and
`tr(P)=1`; its eigenvalues are then zero or one, so positivity needs no
extra unproved condition. The condition that its projective chord distance
from each previously chosen projector exceed `sqrt(eta/h)` is equivalent
to the polynomial strict inequality
`tr((P-P_i)^2)/2 > eta/h`. Thus, for real-algebraic `eta` and previously
chosen algebraic projectors, existence and a sample point are finite
real-algebraic tasks. A nonempty semialgebraic set over the real algebraic
numbers has an algebraic sample, obtainable by real quantifier elimination
with sample-point construction. No claim that the sample remains in the
original coefficient number field is needed or made.

Each successful step adds a point at distance strictly greater than `r`
from all earlier points. The unchanged packing argument prevents more than
`floor((4h/eta)^(h-1))` such points. Therefore the procedure terminates.
At termination no projector is farther than `r` from all centers, which is
exactly the closed-ball covering property used by the support-function
argument. The original cardinality and containment conclusions follow
without an additional approximation error. The fixed known initial state
is still counted separately.

For algebraic primitives and initial state, the resulting branch outputs,
their traces, and all coefficients of the finite barycentric feasibility
systems are algebraic. Feasibility is guaranteed by containment, and a
nonempty bounded algebraic linear system admits an algebraic solution.
Zero-probability branches are handled directly without division. Terminal
decoder entries are algebraic when the supplied POVMs are algebraic. The
text explicitly makes no efficiency claim. No substantive mathematical gap
was found in these additions, and no new numerical diagnostic is required
for this symbolic construction.

I also compared the main abstract and introduction against the exact
instrument theorem and finite/infinite family at these source identities:

- `main.tex`:
  `fe0a89e24c53352f270078a167188b906e9f324aaf6e6bdc478f0954641bdb78`.
- `sections/01-current-overview.tex`:
  `b8fb8b79efd67e0e71c7224b2cc3f2be0c733b3e3b25be93aa7b4a3c027ca4da`.
- `sections/41-conditional-memory.tex`:
  `cc14bc7bac53b52ef7b13b5259e16c32b828a7b198dd7e7a31ea084c96e81c7a`.

The advertised instrument conclusions agree with their precise proofs:
posterior positivity is imposed on every observed branch, the simulator
uses one fixed known preparation and counts its pure initializer, the
dictionary bound is not asserted to be the unrestricted minimum, and the
stationary qubit family has exact unrestricted counts `q`, `q+1`, or
infinity under the declared initialization conventions. The finite-order
case has `q >= 3` because the family assumes `sin(theta) != 0`. Its
uniformly positive outcome probabilities are not confused with uniformly
interior posterior states. The introduction credits the earlier invariant
polytope and one-dependent non-HMM mechanisms and limits the contribution
to the stated simultaneous properties and sharp resource law.

Three editorial quantifier points were sent to the integrating author:

1. **Substantive synopsis correction:** the abstract's phrase "For groups
   with normal subgroups" is too broad for the exact quotient optimization.
   The theorem in Section 38 assumes every subgroup is normal. The correct
   phrase is "For groups whose subgroups are all normal" or an equivalent
   explicit Dedekind-group condition. The introduction and theorem already
   state the stronger condition correctly.
2. **Define the finite phase parameter:** the abstract should say that `q`
   is the finite order of the conditional phase, with `q >= 3`, and that
   the infinite case means a phase that is not a root of unity. Its shorter
   "according to its conditional phase" formulation leaves `q` undefined
   in the abstract, although the introduction and theorem are precise.
3. **Match the stopping terminology:** in the introduction's instrument
   summary, "stopped laws" should preferably read "almost surely finite
   stopped laws", as in the theorem. Equality of full path laws is proved,
   but a terminal experiment at an infinite stopping time is not defined.

These findings concern the displayed hashes. This addendum does not claim
that the requested synopsis edits have already been integrated or that any
later changed source has been inspected. It adds no expert endorsement,
formal verification, editorial assessment, or new test-run claim.

## Controlling attribution correction after the historical audit

The subsequent full historical audit established that the proposed Section 39
is a consolidation of results already proved in retained R68 Section 27,
not a new general instrument theorem of R74. I have now read that retained
source directly. This correction supersedes any novelty implication in the
earlier challenge record; the earlier positive proof assessment was a
correctness check of the displayed draft, not a historical-priority check.

The retained file `sections/27-interior-instruments.tex`, SHA-256
`a332eeddf728e01cc907b3e19cbff526539e65a1ff823aa1b366fa87b75aebe8`,
already contains the same projective-net dictionary bound, the branchwise
interior condition, adaptive history and stopped-law identities, counted
preparations, and a terminating algebraic construction. It additionally
contains multiple preparation anchors, at most `d^2` successors per branch,
same-policy risk preservation, nontermination and mean-cost statements, and
finite-block interiority with its clock counted. Its universal physical
dictionary lower `s^(-(d-1))` is stronger than the proposed consolidation's
`((1-s)/s)^(d-1)` lower. These valid retained conclusions must not be replaced
by the weaker consolidation or reported as discoveries of this revision.

The active `sections/39-instrument-realization.tex`, SHA-256
`e909b6a0bda9318ef2ceeea1fc0a3c0432d8fdd76e7d1412a719c9f6706c25f4`,
is now an unnumbered explanatory bridge to those R68 results. The examined
draft remains preserved as
`provenance/author-research/superseded/39-interior-consolidation.tex`, with
the previously recorded hash `f8e6af94...83b66ac`; its weaker dictionary
supplement is preserved beside it, with hash `0da5e3c4...e29ffc`.

The **873 exact checks** in `diagnostics_r74_instruments.py` are fresh finite
diagnostics of the **retained R68 instrument realization theory**. They
are not evidence for a new R74 general posterior-positivity theorem. The
executed results, source hash, and ordinary/optimized report identities
remain valid; this correction changes their attribution and contribution
classification, not the actual run history.

The new mathematical focus is the finite-group contrast and quotient
results in Sections 37--38, the explicit supplied-coordinate contraction
construction in Section 40 as a quantified application of classical positive
realization, and Section 41's sharp unrestricted classical-memory law for
the specified rank-three, uniformly positive, exactly depolarizing qubit
family. The inherited R68 average-interiority counterexample itself did not
prove the unrestricted `q`, `q+1`, or infinite lower of Section 41.
