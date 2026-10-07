# Resource accounting table

| Coordinate | Definition / cut | New contribution and retained boundaries |
|---|---|---|
| Raw acquisitions N_raw | Every physical preparation, failed attempt, hold, pilot, reset and executed terminal probe | Recurrent singular model: 1+n+1; one-probe model: N+1. No postselection clock |
| Predictive labels M | Total labels between calls; discarded reports cannot be reread | Countable upper uses one anchor plus at most M-1 grid labels; a component/prefix pair is one counted label |
| Simulator state R | Observation-dependent simulator memory | Product upper M*R*D_c*Q only when implemented; identity thinning comparison has no retained report state |
| Controller state D_c | Retained action-selection state | Fixed exploration in matching laws; unrestricted optimized control not inferred |
| Clock / phase Q | Observation-dependent retained timing information | Exogenous horizon may be public; adaptive timing is not free memory |
| Temporary workspace W | Erased before next call / cut | Rational arithmetic and current packets charged; W surviving bits enlarge retained alphabet by 2^W |
| Program P | Finite instructions and readonly data | Infinite real sequences not free; procedural rational prefixes and known finite protocol data have finite descriptions |
| Calibration b_cal / delta | Known input interface or indistinguishable apparatus alternatives | Local metric perturbations add before squaring; one-probe delta is compulsory sign ambiguity |
| Numerical input b_num | Actual accessible packet precision | L=2^b cells in one-probe theorem; no bypass by an exact real input |
| Physical time tau | Every call and computation, including waiting and terminal output | Holds have zero new rounding but nonzero physical cost |

The main theorem is exact Borel mathematics. Its finite-bit upper requires effective allocation and primitives on a declared feasible region. Total-resource converse is proved for semantic exact tags and noisy information cuts, not for optimal transient workspace, program or runtime in every experiment class. Common bounded-loss errors from causal morphisms add; primitive state errors add in root mean square before squaring; direct product implementation cardinalities multiply.
