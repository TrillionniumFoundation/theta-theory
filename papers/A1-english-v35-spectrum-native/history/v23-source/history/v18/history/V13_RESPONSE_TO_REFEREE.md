# Response to the v12 referee report — A1 revision 13

**Manuscript:** *Sparse observation algebras and certified memory across exponent collisions*  
**Author:** Qian Qi  
**Controlling review:** `f2638b4910ee6245e9df4f641a2ed861bc4960b7`  
**Reviewed v12 submission:** `71907d83ba4eb235949e2a929b4b7f85349e96e5`  
**New branch:** `revision/a1-english-v13-referee-response-2026-09-06`

The review identifies two genuine failures of the executable acceptance interface,
an integration-evidence gap, and a substantive question about the consequences of
the collision-uniform geometric theorem. We address these separately. The first
two findings are not counterexamples to the printed geometric theorem; they are
counterexamples to treating internal consistency as compliance with a requested
construction. The new manuscript does not equate repairing them with journal
acceptance.

The complete English manuscript and all appendices remain assembled by `main.tex`.
All 68 complete v12 proofs remain byte-identical, and all 71 named results remain
present. Six proved results have been added, bringing the counts to 74 proof
blocks and 77 theorem/lemma/proposition/corollary labels. Ten inherited core
files retain their pinned Git blob identities. Preservation is checked against
the actual v12 source, not inferred from an earlier completion summary.

## P12.1 — Precision must belong to the request

**Correction.** `ConstructionRequest` in `construction_contracts.py` binds the
horizon, command/report alphabets, budget, output precision, per-stage state and
query dimensions, raw input-error hypothesis, total rounding allowance, and
identity of the complete finite numerical name. `bind_request` constructs this
object and freezes all state and query evaluations **before** calling the
compiler. Both `adaptive_compile` and `robust_adaptive_compile` use it.

`inspect_construction` now requires the independent request as a keyword-only
argument. There is no fallback that obtains the horizon or precision from the
returned program. A precision mismatch raises `ContractError` before any stopping
bracket is issued. The checker rebuilds the candidate lists, deterministic
farthest-first representatives, nearest transitions and query outputs from the
bound data. Query vectors are frozen during that rebuilding and not re-evaluated
later against a possibly stateful callback. The original `Program` and `Machine`
are unchanged; the only persistent mutable field remains the integer index.

The independently specified error budget is

`raw_error + 2^(-requested_bits-1) <= total_error`.

At adaptive mesh `h=2^-b`, requested precision is `b+2`, raw error is bounded by
`tau/2`, and rounding costs at most `h/8`. The stopping bracket uses
`request.total_error`, not a returned table's declaration. Accuracy of supplied
moments remains an external hypothesis: hashing a name or checking its entries
does not establish accuracy against an unknown experiment.

**Mathematical location.** Definition `def:bound-request` and Proposition
`prop:request-conformance`, in `sections/request_conformance.tex`, connect this
interface to the unchanged construction and radius theorems. This proposition
is an implementation implication, not an additional geometric foundation.

**Evidence.** `tests/reproduce_v12_contracts.py` re-executes the referee fault
models against the three original blob-pinned v12 modules. It reproduces all four
accepted false precision brackets, including the two radius exits and the two
floor/tolerance exits. The four unmodified controls have valid brackets.
`tests/test_v13.py` then rejects the coarse-precision attack at both adaptive
call sites for M=1 and M=2. It also rejects merely restoring the requested
precision field, and restoring that field while rescaling the incorrect output
integers. The true radius remains exactly `1/(8M)` throughout; no radius or
residual allowance is enlarged to make the attack pass.

A deliberately changed internal computation can occasionally produce exactly the
same valid table. The new suite includes such a one-label control and correctly
accepts it. The contract is about the returned construction, not about detecting
every change to unused internal computations or to untrusted audit vectors.

## P12.2 — The requested horizon and interfaces cannot be redefined

The same request object binds `T`, the `T+1` state-coordinate schemas and the
ordered query interfaces before synthesis. Application-supplied schemas are
checked on every frozen input history. When schemas are obtained from numerical
inputs, these are external inputs read before synthesis, never the returned
program's stage counts. Returned precision and stage lengths are checked first;
then state-count metadata, table dimensions, query lengths, representatives,
transitions and outputs are checked against that request.

The historical two-stage-to-one-stage mutation is reproduced on unmodified v12:
both entry points return an accepted one-stage object, whose requested second
transition raises `IndexError`. The v13 tests reject this mutation at both entry
points before returning a program. They additionally reject padded copies of
short-horizon tables, falsified state-count metadata, query truncation, genuine
multi-query swaps, and incompatible external state/query schemas. Bad raw-error
plus rounding budgets and a changed frozen numerical name are rejected as well.

The older collapsed-transition control remains in the suite and remains rejected.
No new persistent field, extra label, historical tape or runtime oracle is used.

## P12.3 — One physical program from one common moment name

`physical_common_name` in `tests/test_v13.py` uses one fixed rational formal
moment table of degrees through N=3, centered on `(a_0,a_1,a_2)=(0,1,2)` with a
uniform reference prior and signed entry perturbations. Its declared entry
accuracy is `delta=2^-26`. The same table is used at every refinement and for
all compatible experiments. It is not regenerated using each true model.

For each label budget M=1,2,4, `robust_adaptive_compile` is called once. That
single immutable integer/dyadic program is then executed against four physical
experiments: two priors with densities `1 +/- (delta/2)(t-1/2)` at the exact
collision, and two uniform-prior experiments with exponent gaps
`a_2-2a_1=+/-delta/4`. Every moment discrepancy is checked exactly. A common
positive-evidence quotient bound fixes the advice floor before synthesis.

Acquisition uses the complete two-command alphabet written in the test, with
four reports and two acquisition stages. Every one of its 64 length-two
histories is executed in each model, and every checkpoint query is checked.
There are 768 complete model/program paths across the three budgets. Physical
truth uses a separate exponent-keyed polynomial algebra and exact prior
integrals, not compiler states or an audit's claimed radii. The actual future
probe commands are checked to lie in the common admitted cube with `eta=1/8`.

For every model, an independent exhaustive box-cover/graph-coloring calculation
gives the true unrestricted-centre finite covering radius. All 120 returned
model-specific brackets are checked. The receipt records the fixed moment-name
hash, one program hash per budget repeated across all four models, requested
schemas and tolerances, actual state/query discrepancies, all stopping stages,
and the unaltered construction recurrence allowances.

This is an end-to-end finite physical execution across an additive equality.
It is not full-cube enumeration, a numerical proof of the continuum theorem, or
an execution of the N=5 asymptotic saturation phases.

## E12.1 — The geometric theorem remains the principal input

We agree that correct bookkeeping, greedy covering, error recurrences and
request validation are not separate new foundations. The comparison section
continues to distinguish these classical steps from uniform physical
attainment of the complete normalized flag and the matching global cover.
The collapsed interval example is retained in its proper role: it separates
two assertions about an arbitrary program, not the geometric theorem from all
prior approximation theorems.

The additional conclusion now concerns a complete minimax problem rather than
only program size or a valid perturbation upper bound. At a fixed interior
common moment name, the sharp persistent-memory term is the full collision
profile. Its interaction with uncertainty yields a saturation threshold that
retains all exterior-volume terms. The theorem does not discover a new
lower-bound method; it uses an elementary overlap calculation to complete a
classification whose nontrivial memory term comes from attained geometry.

## E12.2 — A two-sided noisy-collision law beyond the rank-two witness

The original rank-two proposition and its proof remain unchanged. A new main
section, `sections/uncertainty_geometry.tex`, adds:

**Theorem `thm:sharp-common-moments`.** Fix a dominated full-support prior family
`D={nu:c_- mu_0 <= nu <= c_+ mu_0}` and an interior subfamily with fixed measure
margin `lambda`. Suppose a rational name `y` is within `delta/2` of the moment
vector of an interior center `(a,mu)`. The actual consistency class contains
**all** calibrations and priors whose moments are within `delta` of that same
name. The common-program minimax risk, for both criteria, is comparable to

`Xi_N(M,a) + delta^2`,

uniformly across K, including exact collision strata and their intersections.
The upper program is constructed from `y`; the center is not supplied to it.

The proof first establishes `lem:overlap-tilt`, an exact posterior separation
identity with overlapping (not necessarily equal) history laws. Then
`lem:uniform-collision-ambiguity` perturbs the center prior by
`1 +/- (delta/2)(t^{a_1}-mu(t^{a_1}))`. Both priors stay inside D and inside
the **same** moment consistency class. Uniform positivity preserves a lower
bound on posterior variance at every fixed-horizon history. A fixed actually
executable product probe separates their predictions by order delta.
The common exploration laws overlap uniformly, giving unconditional squared
regret of order delta squared even to a rule retaining the full history.
The old intrinsic lower theorem supplies the independent Xi term. The common
advice upper theorem and profile stability supply the matching upper bound.

The interior prior margin and the unused half of the name's error budget are
necessary stated hypotheses, not hidden choices. We do not claim this lower
bound for every boundary/singleton consistency class, or for calibration-only
uncertainty with a known exact prior. None of these new hypotheses restricts
the original arbitrary fixed full-support-prior theorem.

**Corollary `cor:advice-saturation`.** The exact profile inequality
`Xi_N(M,a) <= delta^2` is equivalent to

`M >= max_{n,ell} V_{N-n,ell}(a) delta^(-ell)`.

Thus the threshold is sensitive to all collision scales, not just rank or a
separated power-law floor.

**Corollary `cor:uncertain-intersections`.** For the original four-cell,
five-trial two-parameter arrangement, the complete noisy risk has the four
terms

`max{M^(-1/3), rho^(1/2)M^(-1/4), (rho^2 tau)^(2/9)M^(-2/9), delta^2}`.

Its saturation threshold has order

`max{delta^(-6), rho^2 delta^(-8), rho^2 tau delta^(-9)}`.

Along `u=theta, v=theta+theta^k`, the three advice-accuracy regimes are separated
by `delta` of orders `theta` and `theta^k`, including arbitrarily large fixed
contact order k. This is a concrete consequence at the already studied
intersecting collision strata, with a full proof rather than a new simulation
claim.

## E12.3 — Scope of the resubmission

This response offers a stronger mathematical consequence, a repaired executable
interface and new integrated evidence for independent consideration. It does
not infer four-journal significance from passing tests, count implementation
lemmas as independent breakthroughs, or assert acceptance on behalf of a
referee. The original full profile, fixed-horizon assumptions, arbitrary
fixed full-support priors, actual acquired-history probabilities, global cover,
causal converse, exact-label realization and all special-case appendices remain.
No infinite-horizon or nonmonomial replacement is used to evade the review.

The source is a complete `amsart` English manuscript with theorem/proof
organization, explicit quantifiers, unchanged proof dependencies and
version-pinned literature comparisons. Author-response and test commentary
are kept in this response and the evidence documents, not inserted into
principal proof arguments.

## Reproduction and review trail

Run `python3 validate.py` inside `papers/A1-english-v13/`. It checks source
identities, runs the v10 and v11 author suites, reproduces the old v11 mutation,
runs the ported v12 suite, retains the rejection of the old mutation,
reproduces the new v12 faults against pinned v12 sources, runs v13 diagnostics,
checks complete-proof preservation, and builds the full PDF in three passes.
When run in the complete repository it also executes the **unchanged original
v12 referee script** and records its output separately. The local author
reproduction is not mislabeled as an independent referee report.

`SOURCE_MANIFEST.json`, `V12_PRESERVATION_MANIFEST.json`,
`validation/REVISION_VALIDATION.json`, `validation/V13_DIAGNOSTICS.json`, and
`PRESERVATION_REPORT.json` are the exact identity/evidence entry points.
The prior submission, original review and historical branches are unchanged.
