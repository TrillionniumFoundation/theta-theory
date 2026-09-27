# Response to the v54/r36 referee report — Revision 55

Controlling report: review commit `9c92a08458b92fd831010dca835de8e2239f82fc`, blob `85a4bd2e1d4d6b02cb2360a66c25253148e8f2c1`. Predecessor: v54 publication `1eb16a3f857d17a91dc1c82906ef16a5965a47d2`.

This is a mathematical revision, not a change of journal target or a deletion of the earlier results. The complete preceding native bundle is preserved. We distinguish a proved statement in the manuscript from finite regression evidence and from an independent editorial or priority judgment.

## Principal response to the structural objections

The stationary result is now intrinsic to every compact group and every finite dense alphabet: transition randomness can be removed without enlarging the register or its uniform error. A joint-group feasibility invariant gives the unrestricted stationary minimum, and finite observable quotients give an equality-inclusive existence criterion. For clocked machines, all nonempty exact-return languages are treated by their eventual arithmetic phases. Infinite component groups are handled on both strict sides of the component radius and at the exact zero-error boundary. A second sharp quantitative example has linear exact width on an infinite profinite group, while every positive error permits a bounded stationary realization.

These results directly address report sections 4.1, 4.2, 4.4 and 4.6. The matrix-semigroup mechanism itself is classical and newly credited explicitly. The revision does not claim a classification of arbitrary irreversible physical semigroups, matched rates for all compact nonabelian representations, the exact unit-amplitude planar rate, or a practical total-complexity bound. The unrestricted positive-error clocked boundary on a general infinite component group is not equated with the stationary boundary. These are limits of the displayed theorems, not changes to any retained conclusion.

## Required revision items

### R36 9.1 — Standalone claim and presentation

The title and abstract now lead with stochastic purification and compact-group numerical interfaces. The main text separates stationary and clocked quantifiers before giving results. Repository provenance is recorded here and in the history audit, not treated as mathematical evidence of significance.

### R36 9.2 — Priority and the classical matrix-semigroup ingredient

The audit was extended to the primary paper of Flor (1969), including its idempotent and bounded-group theorems and its attribution to Brown and Schwarz. The manuscript expressly credits that classical structure. Its new reduction tracks the physical coordinate in a joint semigroup, keeps the prescribed uniform error, and does not assume the hidden rows satisfy physical relations. This is a targeted author-side comparison, not an independent human priority clearance; no exhaustive novelty certification is claimed.

### R36 9.3 — Synchronization and return phases

Lemmas `lem:returnperiod55` and `lem:phasegroup55` show that every nonempty exact-return language is eventually the multiples of its gcd, and identify the reachable phase subgroup. Theorem `thm:phases55` gives the exact phase threshold and counts narrow cuts in every cut residue, not just one block phase. Proposition `prop:parity55` proves that even horizons can be exact with one label while odd horizons diverge. The stationary purification and finite-quotient theorems need no return word at all.

### R36 9.4 — Classification and quantitative hypotheses

The original full-subcritical Diophantine lower bound and exact polygon upper bound are retained with their distinct alphabet and amplitude hypotheses. Corollary `cor:unitnoise55` now covers unit amplitude at every positive subcritical error by an explicit amplitude-loss budget; it does not assert an exact upper bound at unit amplitude. Theorem `thm:adiclinear55` supplies a second sharp quantitative model: a fixed continuous 2-adic interface with linear exact width, an all-width occupation bound, and bounded width at every positive error. No badly approximable angle is inferred from algebraic matrix entries.

### R36 9.5 — Unrestricted stationary stochastic minimum

The question is answered structurally, rather than only restated as an open problem. Theorem `thm:purification55` removes transition randomness without increasing width or uniform error, retaining randomized initialization. Theorem `thm:stationaryminimum55` characterizes the exact unrestricted stationary minimum by finite permutation choices and joint-group feasibility. Theorem `thm:effectivemin55` makes this characterization terminating for rational orthogonal polynomial categorical data. Proposition `prop:C655` proves a strict separation: five unrestricted stochastic labels versus six deterministic quotient labels. None of these assertions identifies the horizon-specific minimum with the stationary minimum.

### R36 9.6 — Effectivity and costs

The new stationary procedure has a finite width bound and at most `(k!)^|A|` permutation tuples at each width. Its group closures are augmented rational orthogonal closures, followed by a stated existential-universal real-algebraic feasibility problem. The manuscript separately describes closure construction, real components, radius elimination, algebraic Haar projection, localizer/word-law enumeration, gap certification and fixed-horizon word constraints. It does not claim a useful total bit-complexity bound or an implemented general closure/QE solver.

### R36 9.7 — Resource accounting

Both models explicitly count all advertised persistent labels, including unused padding; retained private information is part of the register. The external clock, horizon, arbitrary real descriptions, real arithmetic and exact sampling remain uncharged only where stated. Numerical decoder dimension is distinguished from a sampled terminal answer register. The rational finite-bit compiler remains preserved under its own hypotheses.

### R36 9.8 — A nonsymmetric curved categorical example

Proposition `prop:curved55` uses a proper interior ellipse in each component of a circle times a two-element group. The component centers `(1/2,1/3,1/6)` and `(1/6,1/3,1/2)` are unique and nonuniform, their radii are `1/12`, and the union radius is `1/4`. Thus the two components cannot be merged at the sharp threshold. The proof computes the whole-law TV radius, not separate event tolerances.

### R36 9.9 — Pipeline boundaries

All independent analytic pipeline closure flags remain false. The revision neither assumes nor discharges raw Fourier/density limits, stopped entropy recovery, canonical shell conditioning, process CLT/Mosco, nonlinear Nisio theory, filtering/QMD/LAN or labelled posterior contraction. The complete local manuscript ancestry is preserved and the Round-Seventeen dependency graph is explicitly recorded in the history audit.

## All thirty local comments

### R36 local 01 — Unused labels

Definitions `def:stationary55` and `def:machine54` explicitly count every declared label, including zero-mass padding.

### R36 local 02 — Decoder versus answer register

The introduction and clocked model distinguish the numerical decoder vector from an actually sampled terminal register; the latter is charged separately when requested.

### R36 local 03 — Compact image

The quotient-radius introduction and component-radius definition say explicitly that continuous coset images are compact.

### R36 local 04 — Unreachable pairs

The original upper proof continues to include and count all advertised seed-component pairs, even if unreachable at a given horizon.

### R36 local 05 — Positive inverse approximation

Lemma `lem:positive54` now writes `u^(r-1)=u^r u^(-1)` and explains why the exponent remains positive when `r>=2`.

### R36 local 06 — Openness hypothesis

The positive-word lemma now repeats finite component count at the step where openness of K is used. The infinite-component proof instead passes to a finite Lie quotient and never assumes K is open.

### R36 local 07 — Repeated centers

The finite-gap proof retains the explicit permission for repeated centers.

### R36 local 08 — Fixed coefficient choices

The calibration and residual sections retain fixed coefficient vectors/maps before defining every norm-dependent constant.

### R36 local 09 — Uniform strict localization margin

The finite subcover argument retains compact minimization and the strict margin at a minimizing center, not merely pointwise strictness.

### R36 local 10 — Expected localizer bound

The residual proof now displays `E p_i <= 1 + ||a_p_i|| Q` before using it in the decoder comparison.

### R36 local 11 — Dependencies of constants

Immediately after the occupation constant formula the dependencies of B, the contraction defect, chi, A and L_k are listed. Phase constants have their own dependency statement.

### R36 local 12 — Cut zero convention

All new clocked occupation conclusions count only cuts `1,...,N`. The dyadic Hankel lower bound can use cut zero internally, but its occupation statement again excludes it.

### R36 local 13 — Simplex diameter

A remark explicitly gives simplex TV diameter one, half-diameter one half, and the distinct three-vertex radius two thirds.

### R36 local 14 — Connected unitary group

The consequences section explicitly states that U(d) is connected.

### R36 local 15 — Full torus surjectivity

The original toral consequence retains surjectivity onto the full product torus in its statement; no proper subtorus is substituted.

### R36 local 16 — Bound on b

The arithmetic section explicitly derives `b<=1/2` by testing a coordinate unit vector.

### R36 local 17 — Two integer parameters

Localization r and rotation count s are distinguished in the harmonic section, algebraic-circle section, and added arithmetic remark. The return period is separately scoped.

### R36 local 18 — Positive block length

The arithmetic remark states `L>=2`, hence `B=s(L-1)>=1` for every k>=1.

### R36 local 19 — Open packing balls

Both orbit-packing proofs retain open balls at half the separation, so equality creates no double counting.

### R36 local 20 — Facet support

The polygon proof now displays the facet normals and inequalities `<n_j,x> <= cos(pi/q)` before the dilation calculation.

### R36 local 21 — Reflection and orientation

The polygon proof explicitly sends vertex v_j to v_(-j mod q) under the standard reflection, preserving the selected vertex set.

### R36 local 22 — Negative nearest integers

The comparable-denominator proof explicitly states that residues are modulo q even when some p_i are negative.

### R36 local 23 — Algebraic degree

The arithmetic remark makes rational independence of `1,xi,...,xi^s` explicit and connects it to the nonzero norm input.

### R36 local 24 — Real orthogonal closure

The effectivity discussion states exactly the real-zero-set/Euclidean-closure fact inside O(D), attributes it to BJKP, and distinguishes real from complex components.

### R36 local 25 — Algebraic Haar moments

The effectivity proof and cost discussion describe algebraic fixed-subspace bases, Gram inverses, isolating data and exact sign comparisons; no numerical Haar quadrature is used.

### R36 local 26 — Rational targets

The finite-horizon proof and cost discussion explicitly observe that rational word matrices and polynomial readouts give rational targets.

### R36 local 27 — Multiplication convention

Component updates remain left multiplication. The stationary joint closure uses the inverse physical coordinate precisely so concatenation agrees with chronological row products.

### R36 local 28 — Generator equivariance

The quotient proof retains the argument that generator equivariance implies full finite-group equivariance because generator images generate C.

### R36 local 29 — Unit-amplitude endpoint

The zero-error planar endpoint is separated from the newly proved positive-error unit-amplitude corollary. No limiting use of a zero enclosure slack is made.

### R36 local 30 — Finite checks and universal proofs

The test script, proof-status record, build receipt, and this response explicitly separate finite rational assertions and rendered reproducibility from written universal proofs and independent priority assessment.

## Preservation and validation

`PRESERVATION_MANIFEST.json` freezes all 91 native v54 files. All active mathematical conclusions of v54 remain in the new main article; the original v54 text and every nested historical proof remain independently buildable. The source-bound qualification compiles five documents and executes all retained regression suites. The main article adds complete proofs, not deferred proof sketches.

`evidence/THEOREM_LOCATIONS.json` maps every displayed label to its actual compiled number and page. `evidence/BUILD_RECEIPT.json` identifies the exact native source commit, dependency versions, assertion counts, negative controls, five PDF results, preservation checks, and isolated all-page text/raster comparison. A successful build is evidence of reproducibility, not a formal proof certificate or a guarantee of acceptance.
