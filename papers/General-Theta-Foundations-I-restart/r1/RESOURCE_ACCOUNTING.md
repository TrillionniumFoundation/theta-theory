# Resource-accounting table

| Resource | Quantity and bound | What is not inferred |
|---|---|---|
| Raw acquisitions | N including failures; source n_pil+n_Gamma N | successful observations do not replace raw N |
| Predictive persistent labels | m; retained grid index | not arbitrary real-valued posterior storage |
| Simulator state | R, joint count mR | not erased because simulator is a “map” |
| Controller state | D_c, joint count mRD_c | arbitrary history feedback need not have finite D_c |
| Clock | Q if stored internally, joint count mRD_cQ | public external time must be explicitly supplied and cannot carry extra data |
| Label bit encoding | ceil(log2(mRD_cQ)) sufficient for the product register | not a lower bound or total bit complexity |
| Workspace | current report + interval arithmetic + search registers; specified finite precision | no history tape or uncleared observation-dependent workspace persists between calls |
| Program/read-only data | grid/update/map descriptions; possibly O(m d b) table bits | constant description or computability does not follow from compact covering |
| Calibration | b_cal and any pilot observations/workspace | known calibration is not a free estimate of an unknown kernel |
| Numerical approximation | u_t in the state metric, terminal v_num in score norm | a tolerance alone is not a minimax error floor |
| Physical time | each raw model call costs one; morphism uses actual time map | number of informative updates need not equal time |

For the concrete HMM with a constant detector command the controller has one state.
For the sensor the attempt controller and hold logic also need only the retained
representative. Their raw horizon is externally enforced in the fixed-N experiment.
An internally implemented horizon counter has Q=N+1 states and is additionally
charged. Neither realization proves a matching lower bound for total memory with
that growing counter; the matched curves concern the predictive cut. Likewise no
optimal runtime/workspace/readonly-description tradeoff is claimed.

HMM finite-precision implementation: current report precision b, grid index log m,
rational calibration data and bounded-precision rational update. Workspace is
cleared after the next grid label is committed. Sensor: evaluate or scan finite
physical-coordinate representatives to precision b; return an approximate nearest
label, clear current input and temporary distances. Arbitrarily close numerical
ties are handled by additive metric error, not an exact-real comparison oracle.
