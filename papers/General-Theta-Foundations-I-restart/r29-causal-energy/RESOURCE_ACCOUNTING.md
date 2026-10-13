# Resource accounting

| Resource | Sequential | Autonomous / simulator | Status |
|---|---|---|---|
| Actual calls | n relative reports + 1 preparation + 1 audit | N=n+2; c calls per simulated report adds cn and explicit setup/audit | exact interface, not iid sample shorthand |
| Persistent labels | m_t after report t; phase externally declared | M >= 1+sum m_t; erased upper reserves one inactive label in each phase | exact circle optimum; matching orbit rates |
| Persistent bits | ceil(log2 m_t) for the phase-local state | ceil(log2 M) for the whole autonomous state | does not include program constants |
| Simulator labels | report morphism explicitly given | at most M S for composition, not a minimal-state equality | Haar-fill simulator uses one persistent state |
| Program description | finite centers and update/readout representation | circle upper O(M(p+log M)+n log M) bits | finite precision, not free real constants |
| Temporary workspace | erased between calls | circle O(p+log M)+W_rep(p) | report access model specified |
| Numerical/report precision | h=2^-p | decision-mismatch probability at most C sum m_t h; readout error C n h | not report-law TV equivalence |
| Online arithmetic | current report + one retained label | circle O(n(p+log M)^2)+n T_rep(p) | precompilation separately finite; no general efficient synthesis claim |
| Allocation | one division of M-1 by n | O((log M+log n)^2) bit operations | exact optimal circle allocation |
| Physical time | sum of actual operation durations | not replaced by the count N | conditional on instrument timing certificate |
| Fixed-start accessibility | additional L paid initialization calls | gate and prefix clock require an extra counted tester | not hidden in a constant |
| Calibration | one invisible fixed sign coordinate | minimax exactly adds delta^2 | actual alternative, not arbitrary tolerance |
| Causal deficiency | protected audit, report deadlines, no extra physical access | epsilon comparable to 1-w for the actual hidden-report experiment | no claim for arbitrary deficiency allowance |

The query index and audit outcome are generated after response commitment and cannot be used by the observer. Pauli or generalized audit effects are queried one at a time; a joint measurement is not supplied. The quantum system is the object being predicted, not free observer quantum storage.
