# Response to the R56 external referee report

The reviewed object is `a47d5f4c13bf93e82e7eaeef5dbb53c2c2a0c764`; the report is `73d3876b1186672d83ab2df515221bff2abd391f`, root report blob `15c692a39c17a34a408e2979f049c87b804179f8`. We accept the substantive objection: a lower on live labels alone did not justify subtracting those labels from the terminal dictionary under the written observer semantics. This is a mathematical repair, not an editorial reinterpretation of the old theorem.

## 1. Complete stopping semantics and a stronger repair

Definition `def:stopping` defines both interfaces before risks. Commands at intercall boundaries depend only on the retained label; physical port, clock and old reports are not free inputs. The terminal decoder is a fixed function of the retained label alone. State stopping has a globally fixed halt map and disjoint live/output types. Event stopping emits an irreversible commitment event during a productive transition, so the same label can serve both roles on different paths. The event is part of the public stopped transcript, not a hidden persistent mode bit.

Lemma `lem:packing` proves complete-path-law-preserving packing with l+t versus max(l,t) labels. Theorem `thm:main` separates the checkpoint lower, event lower, typed lower, and constructive upper. Under matched effort and identity exports it proves R_cp(N,m)=Q_m, R_st(N,M)=Q_(M-B), and R_ev(N,M)=Q_M. It also states an overlap-count extension and unequal-effort sandwiches. All old state thresholds are recomputed, including two-port feasibility, both exact raw realizations, binary Gaussian sensing, the dyadic example and the joint erasure/calibration task. We do not use the valid three-state construction to rule out a two-state event implementation.

## 2. State-dependent approximate task balance

Theorem `thm:approx` permits conditional report and task defects on every surviving history and every model. It proves cost <= kappa_+ beta/(1-beta a), risk <= (Q_m(beta)+beta e)/(1-beta a). At a fixed budget b=N/kappa_+, beta=b/(1+ba) yields upper (1+ba)Q_m(b/(1+ba))+be. First-attempt acceptance handles the small-budget boundary separately. The all-strategy reference lower is unchanged.

Proposition `prop:approx-moments` verifies the defects from unnormalized report, first and second moments. Corollary `cor:raw-approx` verifies them from imperfect classical flips and Pauli control weights without transition, variance or eigenvalue floors. Proposition `prop:sharp-approx` gives exact finite/raw witnesses for the be task-error scale and the waiting denominator, plus an all-program indistinguishability example where absence of first-moment balance leaves reference profile zero but minimax risk one. This last elementary converse is credited as classical decision reasoning, not a universal obstruction to the research programme.

## 3. A nonintervening continuous-target application

Theorem `thm:directional` studies X=aU+sigma G_d with current U on the sphere, arbitrary intercall hidden evolution, known sensor constants, static directions and a uniform refreshed reference admitted. The target is unchanged by sensing. It derives the actual radial posterior and obtains max(D_d(b),rho_m^2) <= R <= min(1,(sqrt(U_d(b))+rho_m)^2). This implies the matching (1+log b)^(-1/2)+m^(-2/(d-1)) law, exact risk one when m<=d, eventual improvement for m>=d+1, fixed-width limit rho_m^2, and leading noise constant (d-1)sigma/(a sqrt(2 log b)). The two converse terms use different admitted witnesses and are correctly combined by maximum. No unknown-sensor learning or externally recognized open-problem solution is claimed.

## 4. Literature, proof structure and resource accounting

The abstract makes reference/balance sufficiency and post-command versus nonintervening tasks explicit. The title remains the required General Theta Foundations I title; the scope is explicit rather than disguised by a topic change. The native bibliography now includes Cuesta-Albertos–Gordaliza–Matran (1997) and Garcia-Escudero–Gordaliza (1999). The introduction maps h<=b to retained fraction 1/b and credits population trimmed quantization. It also compares the different fixed-batch objective of Block–Polyanskiy (2023) and Shin–Pang–Jun (2026). The profile itself and classical rejection are not claimed as new.

Proposition `prop:role-composition` charges live simulator states and terminal export classes separately, including all continuing clocks and seeds. It composes their pairs multiplicatively and their complete-law deficiencies additively. It is a resource-certified implementation law, not an uncharged invariance claim under arbitrary stateful simulators. A proof/hypothesis diagram separates Borel existence, approximate balance and effective implementation. Generic effective synthesis remains potentially exhaustive.

## 5. Remaining requests not represented as closed

We have not obtained an intrinsic all-kernel necessary-and-sufficient balance classification, globally minimal stateful-simulator memory, matched optimal program/workspace/time complexity, unknown-kernel learning, or a universal unbounded-audit/infinite-dimensional extension. The new directional application is broader than binary sign sensing, but its external novelty and general-journal importance require independent assessment. These are mathematical research obligations, not reasons to abandon the mother problem. No numerical or build result is presented as a substitute for the continuous proofs.

The complete R56 source, its reviewed statements and all companions are preserved. This response is accompanied by a request-by-request and technical-comment concordance, proof ledger, dependency graph, assumption matrix and resource audit.
