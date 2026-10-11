# Resource accounting

| Resource | Actual implementation | Not interchangeable with |
|---|---|---|
| Raw acquisitions N | includes preparation, failed/alive calls, ending reports and any separately executed audit call | a free number of successful reports |
| Persistent labels M | full current action/controller/termination/readout state; label committed before score | total program bits or real-valued workspace |
| Retained control plus predictor | QJ pairs; control q survives preparation, predictor may initialize from verified known prior | J labels with a free Q-state controller |
| Boundary regularity H | norm of group inverse of actual boundary matrix; product predictor has H+2 | extra memory or a primitive assumption implied by positivity |
| Simulator private state R | direct product MR; new boundary recurrence must be checked | unchanged M by data processing alone |
| Readout program | one fixed vector/decision per label, common to every unknown model | true-parameter-specific optimal decoders |
| Probability/partition program | explicit finite table, report-cell description, denominator and decision precision | free exact reals in a persistent register |
| Temporary workspace | arithmetic, report-cell location and fresh random sampling; cleared between calls | an uncounted output or intercycle record |
| Planning | exhaustive count in `eq:count`, certified integrations and tail truncation | polynomial synthesis |
| Calibration delta | per-update metric error in generic composition; inaccessible fixed coordinate in attained lower | automatically unavoidable loss for every allowed tolerance |
| Physical time | classwise expected source duration, with target-call versus source-call distinction | a global ratio of model/class averages |

The raw queue's explicit 17/N bound counts one preparation plus the busy period. The joint sharpness construction scores an actual audit on each data call as part of the marked physical kernel; an implementation using a separate audit call changes N and the cycle length and must be charged. Its at most 3 floor(M/3) labels include a reused zero-score preparation label. The three bit outputs are 0, 1, 1/2. The full loss normalization is diam(K)^2+5, covering arbitrary calibration decisions in [-delta,delta].

Same-M effective certification is proved for the graph architecture. Program, scratch, numerical precision, planning time, source physical time and minimal simulator memory do not yet have a complete matched joint lower region.
