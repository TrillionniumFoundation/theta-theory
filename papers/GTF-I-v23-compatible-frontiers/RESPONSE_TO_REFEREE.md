# Response to the sixth external referee report

**Manuscript:** General Theta Foundations I, revision v23  
**Author:** Qian Qi  
**Controlling report:** `reviews/general-theta-foundations-i-v22-external-harsh-top4-r6-2026-09-24/REFEREE_REPORT.md` at `37ff0991b2764ce2fba14541c6191b26661e000e`  
**Reviewed manuscript:** v22 at `88832f95b7dd0b8cc4a3061280a6e31f9fa67319`.

We thank the referee for separating the genuine v22 improvements from the
remaining necessity problem. The revision does not respond by weakening
the physical objective or replacing the program by a smaller one. It adds
a complete full-profile converse and an exact genuinely noisy class,
then reorganizes the article around those statements. All earlier
canonical mathematical modules remain included. The previous organizing
theorem and proof are preserved in an appendix, and the entire 553-page
predecessor development is preserved separately in the complete volume.

## 1. The principal mathematical change

The new central object is the compatible occupation array. Conservation
alone permits inadmissible access to the hidden environment. Quadratic
proportionality equations enforce a common observer transition on every
hidden history giving the same observable register/input row. Theorem
`thm:v23-occupation` proves both necessity and reconstruction, including
zero-occupation rows and cross-epoch row sharing for autonomous machines.
Theorem `thm:v23-dual` applies classical positivity certificates to this
exact feasible set and proves a complete upper-certificate hierarchy for
the full minimax value. Every feasible controller remains a lower witness;
dyadic witnesses and compact-family nets give matching limits. No
minimax interchange or fixed-width convexification is used.

This is supplemented by structural results rather than offered as a
standalone polynomial encoding. Theorem `thm:v23-interval` gives an exact
Bayesian recursion of compatible posterior interval partitions for binary
finite observations, arbitrary finite profiles and bounded losses,
including finite controlled choices. Theorem
`thm:v23-minimax-recursion` gives an exact receiver-curve recursion for
all stochastic one-/two-state controllers at every finite horizon in the
uncontrolled binary experiment. It propagates attainable channels and
Blackwell domination, not convex combinations of entire machines.

Theorem `thm:v23-bsc` solves every three-report profile with overlapping
binary noise. Put d=p(1-p)(1-2p). With two middle states its Bayesian value
is 1-p+d/2, but its stochastic minimax value is 1-p+d/3. Three middle
states attain 1-p+d. The proof reduces every stochastic two-report
summary by a common binary garbling, solves the remaining equal-error
threshold problem, and supplies the nonnegative factorized gap
`eq:v23-gap-certificate`. Thus it is a continuum all-machine converse,
not an exhaustive grid presented as a proof. The strict d/6 gap from
free mixing identifies the compatibility constraint's statistical effect.

## 2. Responses to the numbered substantive objections

### Sections 1–2: preserve the credited v22 results

All credited results survive, including the finite-horizon tournament,
arbitrary-prior revelation frontier, active retained-law transport,
three physical resource regimes and separate confidence amplifier.
Their source files are unchanged and remain in the canonical input graph.
The new proof does not rely on claiming that the referee found a local
error in v22; the report expressly did not do so.

### Sections 3–5: make exactness and generality meet; solve overlapping noise

The complete occupation formulation now characterizes the same
`V^{clk}_{sigma,K}(B,G)` as the constructive algorithms. The two-sided
certificate limits apply to all finite experiments and, with certified
kernel nets, compact finite-alphabet families. A common continuation
matrix is required across every incoming state: its separate column
projections cannot be optimized independently. This necessity is proved
and illustrated before the noisy recursions.

The noisy class is no longer erasure–revelation. Its report laws can have
common support at every time. The Bayesian recursion treats general
loss matrices and finite controlled experiment choices; optimal partitions
are recomputed from the attained occupation list, not assumed nested.
The minimax binary-register recursion covers arbitrary finite horizons.
The exact three-report formulas demonstrate a strict intermediate-memory
penalty and the failure of unpriced stochastic mixtures.

The certificate limit is a complete converse, not a universal asymptotic
rate or an efficient algorithm. The restricted noisy frontier is exact,
not a claim that the tournament's general K-dependent bound is everywhere
optimal. These distinctions are made in the main theorem and proofs.

### Sections 6–7: clock, description, precision and calibration

The notation explicitly distinguishes clocked and autonomous classes.
Shared-row occupation equations give an autonomous optimization problem
without pretending that adding a clock is memory-free. The time-dependent
noisy recursions are labelled clocked; their proof does not extend the
Bayesian purification argument to a repeatedly used autonomous row.

Section `sec:v23-acquisition` defines the resource tuple and its partial
order on fixed codes and schedules. A bounded finite description/precision
class is optimized as a finite class; unrestricted rows on a fixed
architecture use the exact occupation formulation. Architectural unions
are explicit. This is not an unproved universal short Pareto formula.

Theorem `thm:v23-calibration` acquires a fixed response list's target
means from actual target preparations and charges its entire retained
counter vector through training and validation. The count is
M >= log(2K/beta)/(2 rho^2), with dyadic M and (M+1)^K counter states.
The combined score loss includes 2 rho + 2 beta. This is deliberately
not hidden in read-only calibration. The exact two-state minimax rule
uses the rational coin 2/3; the manuscript explicitly says it is not
exactly a finite fair-bit operation and prices its dyadic approximation
on the refined schedule.

### Sections 8–9: physical frontier and the bridge theorem

Corollary `cor:v23-reset-consumer` puts the original reset and physical
protocols in the same occupation class as the converse. The response-cover
and physical machines supply lower witnesses; every dual certificate
bounds every other auditor of the same declared full profile. Compact
physical kernel families use the same net limit. The physical construction
is thus connected to a general necessity theorem, rather than to the
unrelated erasure formula.

The three physical points remain attainable points. This revision does
not report an evaluated fixed-N collision Pareto boundary, nor replace
3 <= W_phys <= 12 by an unsupported equality. Route B of the report is
not claimed completed. The new response pursues Routes A and C; numerical
or scaling evaluation of the physical converse remains a substantive
original target, not a target deleted from the program.

### Section 10: confidence complexity

Corollary `cor:v23-confidence` gives a genuinely matched confidence
frontier for the declared Bernoulli interface produced by the inherited
mean-gap transformation. With three independent repetitions and the
atomic profile (2,2,2), the optimal maximum error is
p-p(1-p)(1-2p)/3; with middle width three it is p-p(1-p)(1-2p).
The composite alternative interval is handled by monotone coupling and
its least endpoint. The lower bound constrains every machine using this
interface, not only the proposed amplifier. Inner-audit states, coin
sampling and preparation counts are charged in the physical implementation.

A richer raw physical auditor is not constrained to this interface. Its
lower bound requires its own occupation problem. The endpoint must be
present before the coin-interface lower bound is transferred to a physical
subfamily. These conditions are stated immediately after the corollary.

### Sections 11–13: active transport, residual relaxations and Route II

The retained-kernel telescoping theorem remains scoped and unchanged.
It is credited as a standard mechanism, not a new general filtration
stability theorem. Weighted/joint residual bounds remain useful relaxations.
The new complete converse retains all compatibility equations instead of
calling those relaxations complete. Exact function computation, Bayesian
reward, minimax reward and confidence remain separate objectives.

Route II now has a general full-profile necessity formulation, an exact
noisy finite-profile theory and theorem-level reset/confidence consumers.
It does not acquire a universal scaling law merely from the existence
of a certificate hierarchy. The response identifies the precise achieved
statements rather than declaring every objective of Route II resolved.

### Sections 14–17: foundations and the historical pipeline

The positive-kernel, preparation, causality and executable-test foundations
remain the initial objects. Finite protocols are a resource-controlled
subcategory. Their exact optimization layer is a finite G3 realization,
not a proof of every general resource/precision/singular-rate assertion
in the blueprint. The complete namespaced historical graph is retained.

The primary A2 geometric chain remains independent. No artificial arrow
from a finite-state theorem is introduced. The original B4 normalized
linear resolvent difference fails on constants and is not used as a
proof of range, compactness, control transfer or correctors. The original
C2 strict-dual/form/rigidity/optional-projection aggregate is not deduced
from the bounded Gaussian consumer. Those original targets and source
materials remain intact. This revision adds an actual necessary/sufficient
finite resource theorem, not a declaration of eleven-paper closure.

### Section 18: theorem-level attribution

The revised introduction and crosswalk explicitly compare the new
statements with likelihood-ratio quantization (Tsitsiklis, Section III),
semialgebraic POMDP occupation constraints (Muller–Montufar, Example 15,
Theorem 16 and Remark 19), and Putinar's positivity theorem and Powers'
rational certificate theorem. These classical mechanisms are not claimed
as newly invented. Finite clocks, filtered comparison and residual
minimization retain their inherited citations.

The original Norberg proof text was sought again but not obtained.
A definitive proof/page comparison with that text remains incomplete.
No theorem is claimed absent from it on the basis of an inaccessible
source. The exact priority boundary of the noisy formulas also deserves
independent literature review; a supplied proof is not an exhaustive
priority certificate. The manuscript makes its mathematical increment
explicit without an unsupported first-in-literature claim.

### Sections 19–20: article architecture and evidence

The article now begins with one dependency chain: occupation realization,
complete converse, common continuations, noisy recursion, exact frontier,
calibration and consumers. The prior technical developments follow as the
supporting experimental and transport theory. No historical mathematical
module is removed; the old organizing theorem is in an appendix. This
responds to the request for an intelligible theorem architecture without
arbitrary deletion. The canonical article consequently is not made
shorter merely to improve its page count.

Diagnostics target false convexification, observable-row violations,
shared-row violations, calibration underpricing, wrong receiver order,
and an impossible exact fair-bit implementation. They supplement written
proofs. Counts, successful builds and preservation manifests do not prove
mathematical novelty or correctness of the general theorems.

## 3. Technical-request disposition

| Request | Revision location and disposition |
|---|---|
| 21.1 Clock in notation | Main theorem; exact occupation/shared-row classes; noisy theorems visibly clocked. |
| 21.2 Resource partial order | Section on acquisition and resource order; fixed code/schedule and explicit embeddings. |
| 21.3 Calibration acquisition | Sampled-calibration theorem and retained-counter bound, not an oracle. |
| 21.4 Noisy converse paired with constructions | Complete full-profile dual plus exact noisy recursions and all-profile three-report law. General tournament scaling optimality is not asserted. |
| 21.5 Overlapping reports / general losses | Binary posterior recursion with general finite losses and controlled choices; uncontrolled minimax receiver recursion. |
| 21.6 Physical frontier | General all-auditor certificate bridge proved; an evaluated collision Pareto law remains to be established. |
| 21.7 Active transport scope | Retained-law scope and unchanged caveats. |
| 21.8 Distinguish objectives | Bayesian/minimax strict gap and separate confidence-interface theorem. |
| 21.9 Literature audit | New primary-source comparisons completed as recorded; original Norberg proof comparison still incomplete. |
| 21.10 Canonical design | Main proof chain reorganized; all mathematics retained rather than discarded to shorten the article. |

## 4. Resubmission claim

The submitted claim is a full-profile necessity/sufficiency and converse
framework with exact noisy Bayesian and minimax evaluations and fully
priced consumers. It is not a claim that a generic optimization encoding
alone is a top-four result, that physical frontier evaluation has been
finished, that the entire pipeline has one root, or that this revision
has been independently certified. The revised theorems and their
attribution are offered for a fresh substantive referee assessment.
