# Revision 81 resource ledger

## Finite rational interior learner

The parameters are integers `d,N>=1`, rational `0<delta<=2^-13`, rational `0<eta<=1/8`. The public dictionary and deterministic decoder are those of `thm:interiorcodec79`. The device remains a memoryless ordered consuming binary measurement with classical output.

| Resource | Bound or convention |
| --- | --- |
| Unknown-device calls | `M <= C N delta^-2[d^2+d log(1/eta)]`, fixed before acquisition, every record |
| Fresh-query block cap | One call; separate input-reference pair per call |
| Retained reference space | Dimension `d^M`; completed outputs may be measured collectively |
| Classical conditioning | All `2^M` ordered binary strings have complete specified readouts |
| Reusable transmitted word | `B=(d^2/2)log2 N+d^2 log2(1/delta)+O(d^2)`; no confidence term in the fixed dictionary |
| Risk grid at stage m | `r_m=min(delta/(32k),eta/(16m))`, `k=ceil(sqrt(N))`; `K_m=ceil(4d/r_m)`; at most `(2K_m+1)^(d^2)` coordinate tuples |
| Readout denominator | Coordinates in `Q_m^{-1} Z`, `Q_m=ceil(64 L^2 d^m/eta)` |
| Readout search at stage m | At most `(2Q_m+1)^((L-1)2^m d^(2m))` tuples; exact positivity and risk tests |
| Raw readout storage | At most `(L-1)2^m d^(2m) ceil(log2(2Q_m+1))` bits, in fixed coordinate order, plus public parameters |
| Termination | Stages `m=1,2,4,...`; each exhausts a finite list; first accepted `M<=2m0` for the proof's statistical existence count |
| Trusted control error | Total unhalved allowance `eta/(M+1)` per fresh preparation or complete final readout; target approximation and actual realization both charged |
| Actual risk | At most `13eta/16` for the original event `d_N(E,C)>delta` under the stated trusted model |
| Computation and gates | Finite, with explicit search/storage dimensions; no polynomial-time, optimized workspace or gate bound |

A receiver's public dictionary is not transmitted as a free private object: both sides reconstruct the same dictionary from agreed parameters. Any nonpublic parameter/header must be charged. Acquisition, offline synthesis, certificate replay, finite trusted-control specification, and dictionary decoding are separate operations. An incomplete search or verification cutoff is not a successful construction.

## Inherited laws and implementation scope

The complete v80 ledger is preserved in `predecessor-v80-audit/RESOURCE_LEDGER.md` and the JSON historical resource strata. All full-body, scalar, qubit, fresh-block, interior, prefix, streaming and instrument conventions remain unchanged. The full-body growing-dimensional bounds are still unmatched in their joint variables; the new theorem preserves the sharp promised-interior law.

The finite replay executable accepts a supplied rational readout, checks complete POVM legality and a fully regenerated parameter net, and reports the theorem's uniform transfer. Its completed scalar certificate is an executed mathematical example. Larger-dimensional local checks are reported as local checks. No theorem-scale optimal acquisition or physical readout is claimed executed. Full synthesis complexity and trusted device control performance are not inferred from a small certificate.
