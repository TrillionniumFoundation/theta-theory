# Resource ledger for the new physical audit

| Resource | Charged value |
|---|---:|
| Candidate training preparations | 2 |
| Fresh candidate validation preparations | 1 |
| Fresh target validation preparations | 1 |
| Total preparations | 4 |
| Report/mark updates | 12 |
| Decision labels | 5 |
| Peak clocked persistent labels | 12 |
| Separate calibration samples or counters | 0 |
| Random bits or stochastic selector | 0 |
| Explicit autonomous phase-tagged states | at most 75 |

Full profile: (1,2,3,3,4,5,5,10,12,10,10,7,3).
Training marks are read and discarded. Validation marks are used.
The event and row are selected before either validation. Candidate and
target validations are independent of training. No first-bit buffer or
candidate-event accumulator lies outside the profile.

The theorem proves N_c(W)=2 for W>=12 on the stated threshold interval.
It does not prove that twelve is the smallest feasible peak. The earlier
minimum decision alphabet of three remains valid with longer training;
the shortest new audit uses five decision labels. Old resource points
are therefore retained rather than deleted under a different resource
order.

For R confidence repetitions, total preparations are 4R and a clocked
implementation uses at most 12(2R+1) labels. This is an upper construction,
not a confidence lower frontier. Atomic autonomous stochastic updates in
the separate binary example are not equated with their fair-bit-expanded
implementation; time, precision and state costs are stated separately.
