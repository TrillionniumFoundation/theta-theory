# Resource ledger — v23

The immutable v22 ledger is preserved in `history/v22/RESOURCE_LEDGER.md`.
The following are new entries, not replacements of the old physical task.

| Result | Charged resources | Exactness / precision |
|---|---|---|
| Compatible occupation value | Fixed full schedule, all observable register rows, every retained random variable | All stochastic rows; shared-row constraints give the autonomous class. |
| Complete dual | The same class as its feasible controller witnesses | Converging certified upper bounds; no efficient degree or finite-termination claim. |
| Binary Bayesian recursion | Arbitrary finite profile; clocked independent/controlled finite observations | General finite loss and prior; deterministic optimum at the declared atomic schedule. |
| Binary minimax receiver recursion | Uncontrolled independent observations; each register has one or two labels | All stochastic machines at every finite horizon; no free global selector. |
| Three-report frontier | Three raw reports; profile after each report; terminal readout | At (2,2,2), minimax 1-p+d/3 versus Bayes 1-p+d/2. Middle width three yields 1-p+d. |
| Terminal 2/3 coin | Atomic rational row, or explicitly refined fair-bit schedule | Finite fair bits give an approximation, not exact 2/3. Error at most 2^-r; refined sampler peak at most 12. |
| Calibration | M target draws, MKr fair bits, counter vector C=(M+1)^K, held word | Calibration peak 3dC, total peak C max(3d,W); error 2 rho + 2 beta in expected score. |
| Confidence consumer | Three base audits, inner states and coin sampler, outer two-/three-label state | Exact lower bound only for the stated coin interface; 3(b+2) raw preparations, not three raw observations. |

On a fixed layout, a dyadic row with s outputs can be encoded by its first
s-1 numerators in (s-1)(r+1) bits. The layout, program, dictionary and
clock convention are separately specified. A sample-dependent calibration
vector is persistent data, never free read-only description.

Atomic and bit-refined schedules are different resource points. The
partial order compares numerical caps only after a common schedule/code
or explicit embedding has been supplied. Autonomous embedding uses at
most the sum of all phase-register sizes, but this is not claimed optimal.

The inherited collision points (399,40602), (320000,1604), and
(12800*2^400,12) remain attainable clocked points. They are not declared
Pareto optimal. Their full-profile values now admit the general converse
and compact-net certificates under the stated finite-kernel hypotheses.
