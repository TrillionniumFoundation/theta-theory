# Resource accounting

| Resource | Exact charge | Role-aware refinement / limitation |
|---|---|---|
| Persistent observer labels | One fixed finite alphabet, only memory between calls | State stopping l+t; event stopping max(l,t) for the constructed role machine |
| Terminal values | Fixed decoder of committed label, never current report | <=M event; <=M-B typed under a same-witness B-live lower |
| Halting / commitment | State-only fixed type OR final emitted event | The event ends execution; it is not a continuing free mode bit |
| Clock, port, controller phase, seeds | Must be encoded if used between calls | No free physical-port input, external clock or program-selection seed |
| Raw acquisition | Every gate failure and productive call paid | kappa=1+1/p0 in heralded examples; final physical audit separate |
| Approximate attempts | Conditional cost <=kappa_+ | Design beta costs <=kappa_+ beta/(1-beta a), not kappa_+ beta |
| Program description | Fixed thresholds, dictionaries, pulse tables and code | Ideal Borel constants distinguished from finite computable description |
| Temporary workspace | Within-call digitizer registers, comparisons and integration scratch | Cannot retain information across calls without state charge |
| Calibration / numerical precision | Physical control error, report approximation and readout errors separately certified | be rare-selection task scale; root errors add before squaring where applicable |
| Simulator | Continuing K states and terminal E export classes | lK live, tE terminal; pair products under composition, not minimality |
| Physical time | Actual gate/productive/audit durations and evaluation work | Separate conditional cost or killed-potential certificate |
| Joint erasure task | One initial call + core + one final audit | Typed 7+3m states; event max(7,3m); sufficient, not claimed minimal |
| Dyadic implementation | 45 threshold data bits, two 15-bit scratch coordinate registers, fresh flip bit, fixed output | Three typed labels (2 encoding bits) or two event labels (1 bit); core calls <161, total with audit <162 |

The error parameters a,e in approximate task balance are not the same object as the attained calibration delta or causal deficiency epsilon. The manuscript keeps all four quantities distinct. A stated upper tolerance is never automatically a minimax lower penalty.
