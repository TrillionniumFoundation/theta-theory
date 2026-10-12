# Resource accounting

| Resource | Core theorem | Joint retained-bit experiment | Simulator / digital layer |
|---|---|---|---|
| Preparation | one paid call | one joint paid preparation | mapped explicitly, no free restart |
| Raw observations | exactly n passive calls | one BIT + n FILTER calls | source calls per virtual call declared |
| Terminal audit | one call after response commitment | one joint audit of Z_n,U,theta | protected in complete scored joint law |
| Physical N | n+2 | n+3 | cumulative clock map composes |
| Scheduled labels | at most m_t | product tags if chosen | simulator product S*m_t |
| Autonomous labels | 1+sum m_t<=M, feasible M>=n+1 | feasible M>=n+2; vanishing joint excess needs phasewise two tags; effective Q=max(1,M-2n-1) | total pair states M*S; counters included |
| Persistent bits | ceil(log2 M) | same for complete machine | ceil(log2(M*S)), not all bits |
| Read-only program | exact Borel tables or separately certified finite constants | fixed imputation/offset rule and core program | O(kMp)+primitive descriptions+O(M log M) conservative codepoint upper |
| Temporary workspace | none granted as unbounded register | no uncharged retained U or previous reports | explicit p-bit numerical working storage; larger oracle workspace extra |
| Calibration | known primitives for core | inaccessible ±delta alternative, response cannot read sign | general kernel perturbation governed by coupling, not automatically delta² |
| Deficiency | complete-law comparison only | actual epsilon=a/2, protected bit audit | errors additive under common task, reverse bound needs reverse morphism |
| Numerical precision | exact-label theorem separate | same distinction | boundary h, failure tails xi, readout v and primitive mismatch zeta separate |
| Runtime | finite horizon, exact internal halt | prescribed action word chosen from labels | naive codepoint search + primitive certified evaluation; no optimal-time claim |

The integer counts in thm:joint are not the rough three-tag product count used by earlier constructions. Two imputed-bit tags attain the matching order. The small-budget lower is a physical independence/phase bottleneck, not an assumed product architecture. Additional reusable simulator state must still multiply the observer budget. Gate/prefix counters in preserved temporal tests belong to their extra tester interface.
