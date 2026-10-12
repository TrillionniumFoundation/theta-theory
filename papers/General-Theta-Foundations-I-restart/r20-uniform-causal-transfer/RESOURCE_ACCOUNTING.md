# Resource-accounting table

| Coordinate | Exact role in R20 | What is not free |
|---|---|---|
| Raw acquisitions n | actual observer calls in the fixed prepared experiment | hidden extra observations, rereading reports, choosing a fresh model each call |
| Persistent labels M | whole autonomous tuple, including decision, stop, PC and retained randomness | exact posterior, true parameter, clock or simulator state outside Z |
| External timing | phase index free only in explicitly external interface | converting that observer to an internal deadline without paying phase labels |
| Programme description | P(b+1)+M ceil(log2 K_rho)+M+ceil(log2 M), plus declared cell/readout descriptions and interpreter | real constants depending on the inaccessible actual model |
| Temporary workspace | row-sampling bound plus cell/readout scratch; erased at persistent cuts | retaining a seed or temporary table across cuts |
| Table access / execution | stated read-only random-access convention, row sampling O((A+M)(b+1)) plus actual cell/readout costs | sequential-tape lookup charged as if random access were free |
| Report resolution h | complete-law physical-instrument error E_h | treating partition cell count as acquired geometric dimension |
| Probability/readout resolution Q,rho | beta_Q; support-preserving rounding and uniform terminal loss net | adding new positive edges when exact stopping is required |
| Parameter resolution s | supplied model net, uniform Omega_n(s), offline | providing the true parameter to the deployed programme |
| Evaluation tolerance eta | certified per-candidate/per-model risk enclosures | a sampled risk or locally optimized controller as a global lower |
| Calibration / misspecification delta | ambient same-support model modulus; sharp offset delta^2 in the calibration task | assuming every allowed error tolerance is attained as a lower bound |
| Deficiency epsilon | complete stopped/scored-law bound for one parameter-independent simulator | one-step report closeness used as adaptive full-law equivalence |
| Simulator state S | at most MS observer/simulator product states | simulator clock, readout transform or internal model estimate uncharged |
| Source calls C(n) | at-most unless exact completion separately certified | fixed-time to stopping-time inference without proof |
| Planning/model-net enumeration | finite but potentially enormous; explicit candidate bound times net size | describing exhaustive search as efficient or optimal in total bits/time |

The calibration experiment has two observer-visible observations. An optional final physical audit is unavailable before the immutable decision; counting it gives N=3 physical calls, not a three-observation observer. Task-apparatus/readout-adapter costs must be stated under that convention. The matrix realization uses classical observer memory, not quantum storage.

Matched resource statements are: exact minimax finite-label value, effective two-sided all-programme error certificate, inherited regular and blind N/M curves at their stated scope, and the calibration threshold plus attained offset square. The full jointly optimal programme/workspace/time/simulator region is not proved.

The attained erasure extension uses seven total labels and a one-state common simulator. It makes two observer acquisitions; a separately charged scored audit, if physically implemented, occurs after the decision. No phase clock is free, and no claim of a minimal seven-state threshold is made. Its actual deficiency is a(1/2-p_minus), not the erasure probability a itself.
