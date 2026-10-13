# Resource accounting

| Resource | Model and charge | Construction / limitation |
|---|---|---|
| Real acquisition N | sup_theta E tau<=N, tau>=1 | same in both transfer directions; rational N for finite synthesis |
| Persistent labels M | all live, control, stopping and decoder labels | regularization reuses existing terminal; exact rare frontier uses <=M-1 live phases plus one terminal |
| Retained data/program | executable transition table, probabilities, legal outputs | description bits separately charged; no stored exact posterior or model theta |
| Clock | no free external step index | auxiliary CTMC exponential times only prove an inequality; actual machine is discrete, each phase call paid |
| Audit | occurs after terminal commitment; unavailable for routing | one extra physical call in rare preparation/instrument tasks and specified raw audit cost in other realizations |
| Preparation/setup | physically prepares actual distribution | not erased from full physical count; b cannot be conditioned away |
| Workspace | digitization, current report and coin generation | transient workspace and current report precision explicitly separate from M |
| Numerical/calibration | raw prep error delta0, one-call eta, audit alpha | new sufficient eta=O(a^2/N), not a universal delta^2 lower bound |
| Finite rare-clock description | one-sided rational root and dyadic phase probability | Q^-1 <= (v/2)min(1,k b^2/N^2), total mean reduction <=v; actual mean never exceeds N |
| Physical time | acquisition, digitization, planning and audit costs | not equal to label count; finite global search not claimed efficient |
| Causal simulator | parameter-independent action/report/strategy/clock/audit compatibility | state budget multiplies by simulator-state count; call budget transforms by its cost certificate; bounded errors add only under the declared common task |

R48 finite synthesis, retained attained calibration/erasure laws, and fixed-deadline M-n rules retain their own scopes. Expected stopping, deterministic deadlines, checkpoint labels, and autonomous total states are not interchangeable budgets.
