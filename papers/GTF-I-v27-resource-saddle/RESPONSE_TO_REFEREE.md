# Response to the tenth external referee report

**General Theta Foundations I — revision 27**  
**Saddle Geometry and the Memory of Causal Experiments**  
24 September 2026

Controlling report: `reviews/general-theta-foundations-i-v26-external-harsh-top4-r10-2026-09-24/REFEREE_REPORT.md`, frozen at `6018ed8f31d758b35eacc48079104e5895fc9591`. Reviewed predecessor: v26 at `466bfcdcb8b7d594d3924dbfa82b4c6e29368858`; native predecessor source `92fd55a9541acfc14665f6275b455dc148fda2d3`.

The report recognizes the previous finite-memory routing theorem, exact U2 and continuous family, restored foundations spine, and local consumer. Its remaining request is synthesis: a general principle that produces new consequences, not another collection of finite tables. We address that request by connecting a statistical saddle's exposed face, its contact equations on Bayes ties, and compatible positive realization of its continuation channels. This connection yields new memory converses for the original marked audit and a law governing least-favorable priors at every preparation number.

## Principal mathematical change

A Bayes best response to the U2 least-favorable prior can use just three events: set both indifferent coordinates to one. It is not minimax. Its score touches the saddle value but has a nonzero derivative at the supporting parameter. Therefore neither the prior's sign pattern alone nor the minimal machine for an arbitrarily selected Bayes tie rule answers the memory question.

The new argument first imposes contact at both supporting parameters. This makes the two averaged indifferent coordinates equal. Stationarity then fixes their common value to the strictly interior t_gamma. The resulting five response rows require three cube vertices and one extra generator in each of two disjoint faces. This proves that every optimal audit needs five states at the decision cut, even with arbitrary stochastic encoding and continuation. The old five-event construction is thus shown to be optimal at that cut.

Repeating the argument on future output channels rather than expected event responses gives eight deterministic vertices and four extra disjoint faces at the candidate validation's second-bit cut. In the candidate-first serial validation class, twelve is the exact whole-schedule peak. The order of validation is an explicit hypothesis. The earlier original interface does not impose that order, so this result is not relabeled as the optimum over all validation orders.

## 12.1 — Structural constrained control beyond the routing geometry

**Addressed by a general saddle-realization criterion and new matching memory consequences.**

In `saddle-realization.tex`, Proposition `prop:outer-normal-form` represents all wirings over a fixed finite causal interface and register profile by normalized positive matrix products. Row sums of an action/report matrix are independent of the unread report. Mandatory action and report buffers are split into their charged cuts. The equivalent continuation generators must satisfy common one-step shift identities; separate cutwise nonnegative ranks are not asserted sufficient.

Theorem `thm:saddle-realization` identifies the realizable part of the unrestricted saddle:

```
S* = {Bayes-optimal response arrays} intersect {g_theta >= U for every theta}.
U - V_K = min_C [(U - prior-average(C)) + (prior-average(C) - min_theta g_theta(C))].
```

Both losses are nonnegative. Exact attainment is equivalent to a compatible positive realization of a member of S*. Compactness gives a strict value loss if the constrained realizations miss that set. Contact and, at interior smooth supporting points, stationarity hold on all prior-support parameters, including directions with zero Bayes coefficient.

The algebraic loss identity is elementary and is not advertised as a new nonconvex minimax interchange. Its useful content is the realization criterion together with the contact constraints: the next theorems apply it to an entire exposed saddle face and exclude every small stochastic architecture, not a specified transition graph. This also makes the distinction from the v26 occupation Bellman formulation explicit.

Lemma `lem:face-packing` gives a reusable stochastic-generator lower bound. It allows arbitrary probability channels as internal generators; it does not silently restrict machines to deterministic history residuals. Proposition `prop:saddle-transport` proves invariance under exact one-state causal recodings and quantified transport with state products under approximate morphisms.

Classical positive-realization, invariant-cone and nonnegative-rank mechanisms are explicitly attributed to Heller, Vidyasagar, and Gillis–Glineur. The claim is not priority for positive realization. The new concrete use is the passage from Bayes indifference through minimax contact to exact causal memory.

## 12.2 — A physical sample-memory converse

**Addressed by an exact order-independent decision count and an exact scheduled peak.**

`exact-memory.tex`, Theorem `thm:five-memory`, proves for every `6/25 <= gamma <= 13/50` that attaining the exact two-preparation value requires five post-training states, and that five suffice. The lower bound permits adaptive training gates, stopping, unrestricted upstream finite memory, independent target-only calibration and stochastic row/event continuations. The all-on common-garbling subfamily is only a lower-bound device; the matching construction is valid against the original private candidate class.

The proof is not based on the assumption that every optimizer depends only on the total training count. Strict Bayes signs force each individual interior-count word. At the extreme counts, the actual independent training marks are averaged only as a proof device. Contact and stationarity fix those averages. Any actual K-state encoder still gives a positive factorization of these averaged rows, so the face-packing converse applies to all full-word responses.

Corollary `cor:strict-four` gives a uniform positive gap for decision width at most four and hence for total peak at most four. The gap is defined through a compact finite-dimensional relaxation. Its positivity is proved; a numerical magnitude is not claimed. The explicit physical Gaussian-tail bound tends to zero uniformly in collision distance, so the decision-memory distinction persists for all sufficiently small positive sensor noise. We do not infer that the previously allowed maximum noise 1/24 automatically lies below this unevaluated gap.

Theorem `thm:serial-twelve` proves that the minimum peak is twelve **when the candidate's entire validation is read before any target validation report**. Randomized encoders, frozen gate policies, and internal event/residual compression remain allowed. The proof uses eight required deterministic output channels plus four additional disjoint faces after the candidate's second report and before its mark. It does not assume an event name must continue to occupy memory after a residual replaces it.

The converse treats actual output laws: a deterministic zero output is not confused with a random output of mean zero. Fresh gate coins enter the continuation channel and do not provide an uncharged past-dependent input. All eight required raw prefixes have positive probability in the supporting subfamily; all four target diagonal words have positive target probability.

The ideal target has support restrictions that can affect reverse-order validation. Consequently the least peak over reverse-order or interleaved protocols is not declared twelve. The unrestricted-order five-state decision theorem and the forward-order twelve-state peak theorem are separate results. This distinction preserves the original interface rather than narrowing it silently.

## 12.3 — A structural law in preparation number

**Addressed for every N by an endpoint law and localization of every least-favorable prior.**

`preparation-localization.tex`, Theorem `thm:prior-localization`, applies to every continuous compact family on a finite alphabet. Let `d(theta)=TV(Q,P_theta)` and `d*=min d`. Then

```
d* - sqrt((|Omega|-1)/N) <= U_N <= d*,     U_N increases to d*.
Integral (d-d*) d mu_N <= sqrt((|Omega|-1)/N)
```

for every exact least-favorable prior mu_N. Thus every weak limit is supported on the closest-experiment set. This is not an extrapolation of a finite-N event table. It uses the same parameter-independent empirical rule as a competitor in the prior game. The empirical estimation ingredient already appears in the preserved decision-spectrum development and is credited accordingly; the new conclusion concerns all optimizing priors.

For the marked product family, Theorem `thm:marked-contact-geometry` computes the contact set directly:

```
s_gamma = sqrt((1+gamma)/2)
d_gamma = 2*s_gamma - 1 - gamma/2
C_gamma = {(s_gamma,s_gamma),(1-s_gamma,1-s_gamma)}.
```

The complete piecewise overlap calculation proves these are all minimizers and derives the uniform intrinsic growth bound

```
TV(Q_gamma,b(p,q)) - d_gamma >= (7/2300) dist((p,q),C_gamma)^2.
```

The independent mark need not be estimated, so the all-N error is `sqrt(3/N)`. Every least-favorable prior has squared distance to C_gamma at most `(2300/7)*sqrt(3/N)` on average. For every symmetric minimizing prior, its W2 distance from the equal mixture on C_gamma is at most `sqrt(2300/7)*(3/N)^(1/4)`. Hence the limiting symmetric least-favorable law is unique. At gamma=1/4 the limiting value is `sqrt(10)/2 - 9/8`.

The exact v26 U1 and U2 saddles remain in the article. The new theorem identifies their all-N limiting geometry without claiming that every finite-N optimum has a two-point prior or that the conservative rates are sharp. It supplies the structural conclusion requested by the referee rather than an isolated N=3 formula.

## 12.4 — Foundations conclusions not encoded in metric hypotheses

**Addressed through intrinsic positive realization and contact geometry.**

The new memory counts come from experimental coefficients, their equality conditions, and convex-face geometry. No dimension, entropy exponent, contraction rate or small-ball condition is assumed in those converses. The quadratic growth inequality for the limiting marked contact set is likewise derived from the atom probabilities and the product constraint, rather than added as a metric hypothesis.

The broad normal form is invariant under the specified exact causal recodings, and its attainable values transport under executable approximate morphisms with explicit state products. This is a resource-equivalence statement on the typed causal objects. It does not claim that every classical information comparison preserves memory at zero simulator cost.

The earlier conditional online M^(-2/d) theorem is preserved with its original hypotheses and attribution; it is not relabeled as a new unconditional law.

## 12.5 — Downstream necessity and the repository pipeline

**A new essential local proof dependency is established; historical aggregate dependencies are not fabricated.**

The exact five-state and serial twelve-state physical memory converses require the new contact-realization theorem and the preceding exact U2 saddle. The v26 upper compiler alone could not prove either lower bound. The intrinsic contact theorem is in turn essential to the quantitative all-N prior localization. These are actual dependencies between proofs, not metadata edges.

The existing transported confidence consumer, calibration/quantization theorem and full microscopic bridge remain. The historical A2 geometric root, B4 nonlinear semigroup gates, C2 strict/form/optional-projection gates and the eleven-paper program are retained at their original paths. The present finite-state argument is not claimed to replace their independent geometric or unbounded-operator analyses. The report explicitly did not require every proposed route; we pursue the structural and physical routes rather than declaring an unproved program-wide closure.

## Other comments and preservation

Theorem hierarchy is reorganized around the saddle-realization principle and its memory/localization consequences. The introduction distinguishes general mechanisms, exact consequences, physical schedule conventions and inherited results. Native AMS theorem/proof exposition is retained; proof details are not replaced by computational receipts.

The entire substantive v26 body is reversibly retained in the assembly, apart from a precisely recorded update pointing its old open-width remark to the new schedule-specific result. All eleven v26 mathematical modules are byte-identical copies. The original paths remain unchanged; both cumulative predecessor volumes are appended unchanged. Their preservation is delivery evidence, not a mathematical answer to the referee.

The tests check exact tie identities, stationarity, interval positivity, face separation, deterministic continuation vertices, and the intrinsic contact constants. Negative controls include illegally accepting the three-event Bayes tie rule and allowing action probabilities to depend on an unread report. Prior regression suites remain part of the build. Neither finite checks nor compilation certify theorem priority or an editorial outcome.

## Precise remaining distinctions

The manuscript does not identify the minimum total peak over all validation orders; the serial twelve-state result is explicitly ordered. It does not evaluate the numerical four-state gap, give sharp large-N rates, classify every finite-N least-favorable prior, or close the historical A2/B4/C2 aggregates. These statements are not weakened substitutes for the new results: the exact decision-memory theorem, exact forward serial peak, all-N endpoint, intrinsic contact geometry and universal prior-localization inequalities are proved in full.
