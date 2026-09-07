# Response to the A1 v11 referee report

**Revision 12 — 6 September 2026**  
**Manuscript:** *Sparse observation algebras and certified memory across exponent collisions*  
**Controlling review:** `7492bf0d74236e866048ef9e5e5b28e4ea9a7f56`  
**Reviewed submission:** `f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0`  
**New branch:** `revision/a1-english-v12-referee-response-2026-09-06`

We thank the referee for distinguishing the examined principal mathematics from
the evidentiary force of the numerical suite. We reproduce the transition
mutation and retain its failure evidence. The revision adds an independent
construction contract, integrated adaptive physical diagnostics, a precise
arithmetic correction, the version-specific citation repair, and new
common-advice stability results. It does not replace the full collision profile
by a weaker floor, restrict the original arbitrary fixed full-support prior
result, remove the attained lower bound, or discard established specializations.

The manuscript remains a complete theorem–proof treatment. This response and
numerical inventories are separate from that article. No test count or source
preservation count is offered as an editorial significance argument.

## P11.1 — Collapsed transition tables

**Agreed and reproduced on the exact v11 source.** The script
`tests/reproduce_v11_transition.py` checks the three source SHA-256 values before
and after running the unchanged v11 suite. With the referee's replacement at
both call sites, 775 of 1,389 entries change across 52 compiler calls, yet all
8,207 checks pass. The resulting receipt is
`validation/V11_OLD_MUTATION_REPRODUCED.json`. This result is intentionally
retained as a successful reproduction of an old defect, not reclassified as an
acceptable construction.

**Independent acceptance condition.** The new `construction_contracts.py`
imports none of the compiler's distance, rounding, greedy, or transition
helpers. It re-enumerates the feasible history lists and implements its own
exact ties-to-even rounding and farthest-first selection. It checks the
representative histories and state counts, every transition minimum with the
fixed smallest-index tie rule, and every clipped dyadic output. The numerical
lists and their radii are fixed before any supplied transition is inspected.
The checker does not use `Audit.exact_vectors` or trust its reported radii.

For a correct transition, the appended representative history is itself a
member of the next grid list. Hence its selected approximate distance is at
most the already fixed radius `r[n+1]`. After accounting for two numerical
errors, the true transition allowance is `r[n+1]+2 tau`. This is proved in
`thm:construction-contract`, with the complete causal recurrence. A corrupt
target cannot obtain a larger acceptance allowance by changing its residual.

Both adaptive routines invoke this gate before accepting any program or
stopping certificate. The original `verify_program` and its residual theorem
remain valid for arbitrary programs, including poor ones; their purpose is not
silently changed. Fixed-precision callers can invoke the same independent gate
explicitly, as the interval tests do.

**The same mutation is defeated.**
`tests/reject_v11_transition_on_v12.py` applies the exact two-call-site collapse
to v12 and the unchanged v11 suite. The legacy physical residual checks still
pass; we report this rather than hiding it. During adaptive construction the
new gate rejects the program on a nearest-transition and fixed-cover violation.
The suite can no longer finish. In the recorded execution the rejection occurs
after 17 calls, with 572 changed entries among 1,002 seen. The receipt is
`validation/V12_REJECTS_OLD_MUTATION.json`.

**Additional negative controls and scale checks.** The new physical suite
independently rejects collapse, last-state, erased-state, erased-command and
erased-report mutations, only counting a control when at least one entry
actually changes. It also tests a wrong nearest-centre tie. The fixed reference
allowance is asserted unchanged under mutations. All old decoder controls
remain in the unchanged v11 suite.

The interval family is exercised for `M=1,2,4,8,16,32`. Its optimal radius is
proved to be `1/(8M)`, the correct grid error is at most twice this radius, and
the collapsed error is always `1/4`. The finite tests compare to this exact
mutation-independent scale. `prop:residual-comparison` includes the continuum
argument and explicitly attributes the diagnostic to the referee's technical
note. This is a comparison of two different mathematical assertions, not a
counterexample to the original construction theorem.

## P11.2 — Integrated adaptive physical interface

**Addressed with a deliberately stated feasible domain.** Twelve physical
programs now combine a positive three-cell monomial detector, a fixed hidden
parameter and full-support prior, successively requested perturbed coefficient
and moment data, adaptive stopping, independently checked transitions, and
execution of the resulting index-only program. The calibration cases are
`a=(0,1,2)`, `a=(0,1,2+10^-12)`, and `a=(0,1,2+1/7)`. The first two use the
uniform prior; the separated case also exercises the prior with density
`3 t^2`. Every trial, including a rejected report, is retained.

At every attempted precision, signed finite dyadic perturbations are supplied.
At exact collision, coincident formal labels deliberately have unequal
numerical advice values. The explicit quotient certificate and independently
computed exponent-keyed truths check the requested state and query tolerances.
The complete trace records each input tolerance, observed name error, quotient
allowance, candidate count, radius, stopping bracket and first successful scale.

There are two precisely specified domains. The first is the complete
subexperiment with command alphabet
`{(1/4,3/4,1/4),(3/4,1/4,3/4)}`. All histories through two prefix trials and all
remaining product-probe queries are tested, for `M=1,2,4`. This has genuine
command, state and report dependence. The second is the entire continuous line
`g=(u,u,u)`, `1/4<=u<=3/4`, at `M=2`. On that line, accepted cell `j` has
likelihood `u k_j` and rejection has likelihood `1-u`; the scalar factors cancel
from the posterior. A one-code command quotient is therefore exact over that
whole line. Five off-grid values are used to test its identity and trajectories;
they are not falsely described as a fine net of the full command cube.

For each physical fixture, an independent exact covering oracle computes the
unrestricted-centre maximum-norm radius of the finite reachable set. A set of
points fits in a radius-e box exactly when its diameter is at most `2e`, so
M-box covering is decided by exhaustive colouring of the incompatibility graph.
The numerical radius is not used as ground truth. The tests check **every**
stopping bracket against this independent true radius, the final two-sided
bracket, the first-success scale, and the final program's query errors against
a data-fixed recurrence. For the continuous line the exact quotient gives the
same finite reachable set. Payload entry counts, bits, excluded overhead,
actual query errors, and every nonvacuous mutation are recorded.

These diagnostics do not validate the full command cube, the four-cell
five-trial resource phases, every asymptotic regime, or the continuum theorem
by enumeration. The manuscript's full-cube theorem and all its proofs remain
unchanged; the finite-alphabet experiment is not used to claim its asymptotic
lower rate. This distinction is also present in the historical memory-risk
source and is made explicit in `NUMERICAL_EVIDENCE.md`.

## P11.3 — Exact intermediate bit lengths

**Corrected without changing the sufficient precision law.** In the proof of
`thm:profile-adaptive`, the incorrect additive exact-working-precision sentence
is replaced by: input/output accuracy uses `b+O(1)` places, while the exhibited
exact rational evaluator uses `O_fixed(b+1)`-bit intermediates. A multiplicative
constant depending on the fixed circuit is not an additive overhead.

The new `lem:rational-workspace` proves this by induction over the finite
arithmetic circuit and separately proves that `(2^b-1)^N/2^(Nb)` has reduced
denominator exactly `2^(Nb)`. Exact tests check several b and N. The existing
rational-operation count still excludes oracle time and is not relabelled a
bit-operation count. No rounded-arithmetic theorem is asserted without a
rounding proof. The before/after proof hashes and the sole authorized exception
to byte-identical v11 proof preservation are in `PROOF_CORRECTIONS.json`.

## P11.4 — Version-specific literature reference

**Corrected and checked against the primary PDF.** Both
`sections/comparison.tex` and `references.tex` now identify the discounted
result as **Theorem 5.2 in arXiv:1503.02244v3**. Printed page 32 / PDF index 31
was retrieved and visually inspected, as was printed page 35 / PDF index 34,
where Theorem 5.3 is the average-cost result. The comparison's substantive
assumptions and objectives are unchanged. `LITERATURE_VERIFICATION.md` records
the exact version and the targeted checks of the other two primary papers.

## E11.1 — The non-routine claim and a substantive consequence

We agree that different output formats, extra test counts, or substitutions
into a table-size formula do not establish exceptional mathematical
significance. The introduction and comparison continue to identify the main
geometric mechanism: a complete collision-sensitive flag is attained by actual
positive experiments for an arbitrary fixed full-support prior, uniformly
through additive collisions, and a separate global cover matches its order.
This is the input connecting the exterior profile to prediction and memory.
Greedy selection and a finite-horizon error recurrence are classical tools.

A precise comparison is now supplied in `prop:residual-comparison`: a valid
residual bound plus exact representative outputs does not itself imply
covering-order realization. Its positive counterpart,
`thm:construction-contract`, states the additional construction condition and
proves the desired bound. We do not claim that no result could be deduced from
other literature together with additional hypotheses; the comparison concerns
exactly the displayed assertions.

The new consequence is **stable realization from one imperfect numerical
name**, not another rearrangement of program-size exponents:

- `lem:paired-history` bounds same-history state discrepancies directly by
  finite coefficient/moment discrepancies, hence gives Hausdorff and
  M-covering-radius stability with no additive-gap inverse.
- `lem:prior-envelope` checks uniformity on a stated dominated family over an
  arbitrary full-support reference measure; `cor:profile-stability` transfers
  this to the full collision profile even when equality patterns change.
- `thm:common-advice` proves that one common finite name constructs one program
  simultaneously for every compatible system, stopping at scale
  `e_E(M)+rho` without selecting a hidden true model.
  `cor:uncertain-monomial` gives regret `O(Xi_N+delta^2)` in each compatible
  physical experiment. The new hypothesis is an explicit uncertainty model,
  not a weakening of the original fixed-prior theorem.
- `prop:advice-floor` gives a positive fixed detector and two compatible priors
  for which a genuine observable query has a prediction gap after an identical
  positive-probability report event. Combined with the retained memory lower
  law, this gives sharp regret `M^-2+delta^2` for the common-advice experiment.

The proofs are in the article, including first-success inequalities,
prior-dependent uniformity checks, the exact detector and priors, query command,
and the unconditional two-point calculation. The elementary two-point method
is not advertised as new. These statements give the sharp geometry an
interpretation under unresolved finite-data identities. They are offered for
mathematical and editorial assessment, not as a predetermined answer about
acceptance by a named journal.

## E11.2 — Three distinct meanings of certification

The manuscript and `PROOF_LEDGER.md` separate (i) numerical evaluation error,
(ii) the residual bound of a particular table, and (iii) the constructed table's
covering-order guarantee. The checker does not purport to certify an arbitrary
input oracle. A residual receipt is not used as an optimality acceptance test.
Source hashes, build success and finite numerical checks are not represented
as formal proof certificates.

## E11.3 — Preserve the submitted mathematics, not a chronological tally

The full paper retains all 62 v11 named results and all 59 proofs: 58
byte-identical plus the single documented P11.3 prose correction. All 10 pinned
historical core files are unchanged, all 49 v10 proofs remain byte-identical,
and the old v10 and v11 test files are preserved. Nine additional proved
results are inserted as a logically ordered section before the appendices.
The original appendix hypotheses, including mechanical specializations, remain
explicit. The full old response and historical/proof maps are retained in
`history/`; no old review or revision branch is modified.

## Executed evidence and boundaries

`validate.py` checks every source manifest entry, executes the inherited v10
suite (7,904 assertions), unchanged v11 suite (8,207), exact old transition
mutation reproduction, new v12 suite (26,158), and the same mutation against
the new gate. It then compiles the complete manuscript in three TeX passes and
checks references and overfull warnings. The locally built manuscript has
62 pages. Page contact sheets covering all pages and detailed new-theorem
pages were visually inspected; see `VISUAL_INSPECTION.md`.

The separate old v10 referee and old v10 mutation scripts are not claimed as
rerun by this revision's validator. Their historical evidence is retained in
the repository. The new source/build receipts report the exact executions
performed, rather than inheriting an earlier author's execution claims. No
all-eleven-paper re-review, exhaustive priority search, or formal proof-assistant
verification is claimed. Passing the concrete checks removes those particular
diagnostic objections; the significance of the combined mathematics remains
for the next independent review.
