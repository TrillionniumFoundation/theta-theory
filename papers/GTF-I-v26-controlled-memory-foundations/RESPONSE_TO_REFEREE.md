# Response to the ninth referee report — General Theta Foundations I

**Revision 26 · 24 September 2026**

Controlling report: `reviews/general-theta-foundations-i-v25-external-harsh-top4-r9-2026-09-24/REFEREE_REPORT.md`, frozen at `568301ff5d8991af9a99a478371c1c4993d0bcd1`. Reviewed predecessor: v25 at `818ca30bab506cfedaf6aee4c32bedff70c1e251`.

We accept the report's distinction between a sound unrestricted controlled minimax calculation and a theorem about an actual finite register. We also accept that an exact one-preparation family does not answer the multi-preparation question. The revision addresses these points through new analytic theorems, not through another rational U1 certificate or additional diagnostic counts. The original broad foundations title is retained and the foundational spine is restored to the canonical article. Existing mathematical arguments remain available in the article and unchanged predecessor volumes.

The principal new calculation is an exact two-preparation saddle, together with a continuous two-preparation marked family. A second result gives a sharp, fully charged informative-control memory obstruction, including an exact strict gap caused by free controller mixing. The opening now states and proves an acquired causal transport theorem with simultaneous calibration, quantization, model-error and register costs. The final consumer theorem uses these results in a complete confidence/simulation guarantee.

The stable theorem labels below refer to native source; `evidence/THEOREM_LOCATIONS.json` supplies the actual compiled theorem numbers and pages.

## 15.1 / Route A — informative controlled selection with actual finite memory

**Substantively addressed by a sharp finite-profile theorem and a resource-exact nonlinear formulation.**

`controlled-memory.tex`, `thm:memory-dp`, defines legal common row prescriptions on a specified finite register profile. Its occupation bundle is a deterministic offline design state indexed by the fixed parameter and hidden execution state. It is not a posterior or history supplied to the runtime machine. At each time one chooses a single prescription common to every hidden history with the same visible inputs. The terminal worst-case parameter is evaluated after the entire execution; nature is not allowed to change parameters after reports. Absorbing stopping states, frozen validation events, action buffers and phases belong to the execution profile. Shared autonomous rows must be fixed once; optimizing them anew at each time is expressly disallowed.

The maximum worst-case value is the backward dynamic value and equals the infimum over its nonlinear supersolutions. This is exact but can be computationally difficult. We do not identify this variational formulation with an efficient algorithm or a linear least-favorable-prior dual for nonconvex finite-memory controllers.

`thm:routing-gap` then solves a family rather than stopping at a formulation. The unknown parameter is (i,j), with m routing indices and a binary hidden target. One preparation reports i. Only K labels may survive to choose a branch-specific sensing action. A branch reveals j only when selected correctly. The same K-state register must carry the relevant observation and determine the informative choice. These sensing actions are incomparable.

The exact value is

```
V(m,K) = 1 / (2*ceil(m/K)).
```

The converse covers randomized encoders, randomized action rows and stopping. It follows from the stochastic-decoder row constraint and a sharp pigeonhole bound, and is attained by balanced routing fibers and complementary frozen events. A free ex ante mixture of complete K-label controllers instead has exact value `K/(2*m)`. At m=3,K=2 these are 1/4 and 1/3. The mixture's persistent interval selector is not free: one explicit realization needs up to mK labels, and the strict converse excludes a K-label realization when the values differ.

The profile is bounded by `(1,K,m,3,6,3)`. In particular, the m-state chosen-action buffer is visible in the account. We do not call K the uniform peak of that machine. This is a genuine multicut constraint and a matched theorem for informative selection through that constraint. `cor:routing-noise` proves persistence for full-support training rows by a uniform path coupling. The general mixed/behavioral distinction and the elementary counting ingredients are classical; the stated family, exact frozen-validation values and resource accounting are the precise claims.

## 15.2 / Route B — the original collision N–W frontier

**Strengthened on the original W>=12 segment; the minimum-width question is not claimed solved.**

Previously the two-preparation machine supplied a deterministic lower bound m2, without computing the unrestricted U2 upper value. `thm:two-saddle` now computes U2 exactly. `cor:two-physical-exact` realizes that exact value at peak twelve against the full original private candidate class. A common-garbling physical subfamily supplies the matching upper bound against every allowed architecture. Consequently the ideal physical two-preparation score, not merely its preparation count, is exact for every W>=12.

The new event-selection row does not enlarge the five-event alphabet. At training count zero it randomizes between old events h0 and h1; at count four between h4 and h3. It then discards the count and retains one selected event for both validations. The exposed profile is `(1,2,3,3,4,5,5,5,10,12,10,10,7,3)`. The extra width-five cut is explicitly included. The previous microscopic estimates and validation residual compiler are preserved, not replaced by an informal atomic-mask argument.

The exact score is U2 at Q*, and the physical value for a target within beta in total variation lies in `[U2-beta,U2+beta]`. Hence the preparation theorem now covers `U1+beta <= c < U2-beta`, still at two training preparations and four total preparations.

`prop:tau-precision` separates the exact atomic random row from a finite fair-bit implementation, proves a uniform `(5/16)*2^(-b)` score loss and counts its origin, comparison flag and phase buffer. This prevents an algebraic coin from being silently treated as a finite-bit device.

This result does not determine the least possible peak at N=2 or exclude all widths 3 through 11. Those are retained mathematical targets. The new theorem is a strict strengthening of the original physical segment, not a substitution of the separate revelation coordinate for physical peak width.

## 15.3 / Route C — multi-preparation marked minimax theory

**Addressed by exact U2 and an explicit continuous U2 family.**

For the original collision target, let r be the unique root in `(1/3,7/20)` of

```
2*r^3 + 25*r^2 - 3 = 0.
```

Then

```
U2 = (-r^3 + 6*r^2 - 3*r + 14)/32
   = 0.4261127787966559...
```

The least-favorable prior has equal masses at `p=q=(1+-sqrt(r))/2`. The optimal response uses the total S of the four actual training report bits; the two actual training marks are discarded by the construction, not altered in the adversarial response class. Its rows on 000,001,110,111 are

```
S=0: (tau,0,1,1)       S=1: (1,0,1,1)
S=2: (1,1,1,1)         S=3: (1,1,0,1)
S=4: (1,1,0,tau)
tau = 6*(-r*r+4*r-1)/(r*(3*r+25)).
```

The proof gives a global square factorization in `u=(p+q-1)^2`, strict monotonicity in `v=(p-q)^2`, and the full posterior coefficient table. It proves both the all-parameter lower bound and the unrestricted full-marked-word Bayes upper bound. Conditional exchangeability of the training arrangements and independent marks justifies grouping coefficients by S; it is not an assumption that every competitor uses only S. Equality at both prior support points closes the primal/dual match.

`two-preparation-family.tex`, `thm:two-family`, extends the result to every mark bias `6/25 <= gamma <= 13/50`. Its root solves

```
r^3 + (13-2*gamma)*r^2 + (3-12*gamma)*r - (1+2*gamma) = 0,
```

and its exact value is

```
U2(gamma) = [-r^3 + (7-4*gamma)*r^2 - 3*r + 13 + 4*gamma]/32.
```

The theorem supplies a common isolating interval, a legal randomized response, a matching prior, a parameter-square certificate, and explicit posterior coefficient signs uniformly throughout the gamma interval. Thus it is genuinely N=2 on a continuous target family, not another deformation that remains at N=1. The original gamma-family U1 proof remains unchanged. We do not infer an all-N recurrence from the two computed levels.

## 15.4 — arbitrary integer revelation laws

**The powers-of-two restriction is removed in several exact regimes; Bayes and minimax values are distinguished.**

`prop:integer-erasure` gives the arbitrary-m,K uniform-prior Bayes value `rho*B(m,K)`, where `m=Kq+s`, `rho=1-(1-alpha)^N`, and

```
B(m,K) = 1 - [(K-s)*q^2+s*(q+1)^2]/m^2.
```

It proves a matching minimax construction for `rho <= m/(m+s)` and the exact perfect-reveal minimax endpoint `1-ceil(m/K)/m`. When K does not divide m, the perfect-reveal endpoint is strictly smaller than the Bayes value. A balanced fiber formula by itself therefore would not answer the minimax question: symmetrization may require a retained partition selector.

`thm:two-label-erasure` gives the complete law for every m and N at K=2:

```
V(N,m,2) = min(2*w*b*rho, w),
w=floor(m/2)/m, b=ceil(m/2)/m.
```

The initialization law is explicit on the low-reveal branch; the high-reveal branch starts in the larger fiber. Both use the same two actual labels and no revelation flag. For odd m there is a saturation transition at `rho=m/(m+1)`. This is not obtained by replacing powers of two in the old formula mechanically.

For K>=3 above the exact low-reveal range, the article supplies bounds and retains the exact constrained dynamic optimization, not an unsupported closed formula. Partial/noisy revelation is not presented as already solved by this erasure result. The full-support informative-control theorem is a separate noise-robust result. The revelation model remains an illustrative exact resource family, not the main foundations claim or a surrogate for collision width.

## 15.5 / Route D — restore the canonical foundations spine

**Restored in the English canonical article rather than evaded by narrowing the title.**

`foundations.tex` begins with A0–A5 and proves prepared path construction, future-test quotient and update closure, posterior barycenters/convex order, entropy loss and normalized response. It distinguishes pointwise predictive equivalence from measurable quotient realization, and a prepared posterior from a statistic uniform over unknown parameters.

The attainable-resolution development proves the exact checkpoint quantization identity under the actual acquisition law, and a matching online `M^(-2/d)` law under finite-cover, contractive-update and acquired small-ball hypotheses. The lower bound uses probability mass, not merely dimension of a reachable set. The upper bound is a compatible finite-state update, not repeated free access to the discarded history. These arguments restore the historical G1/G3 route; standard quantization and coupling ingredients are identified as such.

`thm:joint-transport` is the simultaneous resource statement. Its recurrence carries numerical error, calibration error and quantization error. Its uniform path defect includes model mismatch, calibration failure and output-kernel discrepancies. Its executing state budget is `C_cal * R_t * M_t * K_t`, and its preparation budget includes the calibration trials and all simulator calls. A finite categorical calibration corollary supplies an explicit Hoeffding confidence allowance and a retained count-register bound. Shared feedback and stopping are compared at identical visible prefixes; no assumption that a discontinuous controller acts identically at two different approximate posteriors is made.

The controlled finite-profile theorem is then formulated as an actual finite causal execution within this object. It is not the checkpoint quantizer, and its occupation bundle is not a newly free state. The relation to unrestricted policy-tree duality is made precise by the exact gap theorem. This restores the framework without claiming that general positivity alone implies contraction, density, uniform calibration or unbounded operator closure.

## 15.6 / Route E — theorem-level downstream necessity

**A real local consumer is proved; no false global pipeline dependency is asserted.**

`consumer-transfer.tex`, `thm:transported-consumer`, proves finite-confidence error bounds for independent physical audit blocks with the new exact mean margin, finite precision and sum-register costs. It then transports the entire repeated audit through the acquired causal simulator. The source experiment need not have independent blocks after shared calibration: its final error event is controlled through the full path-law defect.

The proof directly uses the exact U2 saddle, the original local microscopic bridge, the residual compiler, the new precision implementation and the joint calibration/simulation theorem. The sharper mean and confidence exponent cannot be obtained merely by relabeling the old deterministic m2 certificate. The downstream theorem states every additional simulator hypothesis.

This does not demonstrate that an existing independent A2 geometric theorem now essentially uses the controlled dual, nor that the B4 or C2 analytic requirements have disappeared. Their original routes remain intact. We therefore do not mark the report's strongest program-wide necessity request as universally closed. The new consumer is a checked proof dependency, not a metadata edge offered as a substitute for one.

## 15.7 — adjacent controlled-experiment literature

**Direct primary-source comparisons added, with the Norberg boundary maintained.**

The introduction and literature crosswalk now compare the posterior stopping equation of Naghshvar–Javidi (Section 3, equation (4)), the controlled/open-loop error-exponent comparison of Nitinawarat–Atia–Veeravalli (Theorem 2 and its example), and the sequential-design ancestry of Chernoff. They distinguish those decision costs and asymptotic results from our fixed-horizon signed validation functional and charged finite-register constraints. The bibliography includes all three requested references.

We additionally compare the mixed/behavioral and polynomial-optimization setting of Zheng–Sim–Varvitsiotis, and retain the existing POMDP, finite-memory testing, randomized/stationary and adversarial-testing comparisons. Dynamic programming, imperfect-recall nonconvexity, quantization and positivity hierarchies are not claimed new. The exact controlled ceiling law, continuous multi-preparation saddle and their specific resource realizations are the new mathematical claims.

The original full proof of Norberg's comparison has not been obtained for an independent proof-by-proof analysis in this revision. Accordingly no originality separation from its most general results is asserted; the narrowly stated boundary is retained.

## Section 16 — withdrawn requests and preservation

We respect the withdrawn requests. The revision does not present another rational U1 bound, another common-row proof, another adaptive-advantage illustration, a longer metadata graph, or a preservation receipt as its mathematical advance. The already accepted arguments are kept because they are needed and because deleting them would lose useful constructions. Execution receipts are included for reproducibility of the submitted files only.

The canonical source retains the predecessor's complete substantive mathematical body and all five v25 theorem modules. It adds the new foundation, finite-memory, multi-preparation, integer-revelation and consumer modules. One obsolete sentence saying the maximum two-preparation score was not determined is replaced by the precise new result and the remaining width distinction. The introduction is rewritten as an integrated mathematical introduction, while the previous full article and cumulative volumes are appended without alteration in the separate preservation volumes. Historical reports and other papers are unchanged.

## What the next referee is being asked to assess

The submitted claims are the exact statements and proofs above. In particular, the continuous U2 family and the informative-action finite-register gap are candidates for the report's Routes C and A. The acquired causal transport theorem restores the requested foundations architecture and supplies a stated downstream interface. Whether their combined depth and significance meet a particular general-mathematics journal standard remains a matter for independent review. Build success, algebraic regression counts, and the existence of this response are not offered as an answer to that editorial judgment.
