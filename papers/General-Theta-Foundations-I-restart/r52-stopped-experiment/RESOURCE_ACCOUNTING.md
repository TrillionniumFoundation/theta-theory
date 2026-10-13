# Resource accounting

| Resource | Core theorem | Gaussian / singular | Same-task error extension |
|---|---|---|---|
| Paid raw calls | every acquisition including rejection, E sum c_a<=N | E tau<=N, actual reveal counts beta E tau | n core calls in expectation plus preparation, early bit, audit: N=n+3 |
| Persistent labels | one live + m terminal, total M=m+1 | M=2 exact ROC; M=3 threshold upper | one early label + 3 live lanes + 3m terminals =4+3m |
| Label bits | ceil(log2 M) | same | same; not program storage |
| Program description | action probabilities, accept regions, m finite readouts | threshold constants/atom probabilities and readout | lane transitions plus core descriptions |
| Temporary workspace | current-call report/arithmetic W(p) | normal-tail or threshold evaluation / overflow detection | core workspace plus fixed lane operations |
| Precision | independent primitive, routing, calibration and readout certificates | rational feasible thresholds; no free exact real | invisible calibration alternative delta; finite numeric error separate |
| Physical time | primitive costs and E tau, no deterministic bound | reveal/measurement/channel actual calls | prep and protected audit explicitly paid |
| Simulator state | s labels multiplies observer to sM | clock/action/report/audit compatibility required | same |

No free external deadline marker is assumed. The interface is mean stopping, not the older exact-n protocol. The physical hidden chain or qubit belongs to the experiment and is not an accessible observer memory bank. A Borel existence theorem is not automatically an effective finite-bit synthesis theorem; Appendix B states additional computational certificates and a hazard margin.
