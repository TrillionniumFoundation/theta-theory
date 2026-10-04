# Proof audit — Revision 79

This is an author-side proof check, not an independent external referee opinion. Current new claims are in active Section 61; earlier proof audits remain byte-preserved.

| Obligation | Argument and scope |
|---|---|
| Joint parameter dimension | Hermitian matrices form a real `d^2`-dimensional normed space. Lebesgue volumes scale as radius to `d^2`; the unknown unit-ball volume cancels in both directions. |
| Arbitrary legal covering centres | Interior packing points are pairwise at least `4delta` apart in actual `d_N`; the metric triangle prevents any radius-`delta` ball, including one centred outside the interior, from holding two. |
| Absolute range | With `s=512delta/sqrt(N)` and `delta<=2^-13`, the nonsaturated term of the dimension-free lower comparison gives `4delta`. The packing has at least `4^(d^2)` points. |
| Constructive radius and rounding | `k=ceil(sqrt(N))`, `K=ceil(128dk/delta)` and threshold `t=delta/(16k)`. Certified approximate-input error plus row-sum rounding is at most `2d/K<=delta/(64k)`. Both resulting matrices lie in the expanded fixed interior. |
| Strict selection/equality | Reject when both `tI-H` and `tI+H` are PSD, including zero eigenvalues. Accept only strict norm separation. No floating tolerance or missing singular-pivot branch is used. |
| Cardinality, without coordinate logarithm | Disjoint radius-`t/2` operator balls lie in radius-`3/8+t/2`; size at most `(1+12k/delta)^(d^2)`. Coordinate enumeration affects computation but is not transmitted. |
| Total legal decoder | Reconstruct entire dictionary; use first covering predecessor. All fixed-length indices outside list decode to `I/2`. Malformed length/schema is an input error, not a purported theorem word. |
| Randomized converse | Packing label independent of public seed. Classify from decoded effect, apply conditional Fano, data processing through private decoder randomness, then conditional Kraft bound. Worst-target expected length dominates packing-average length. |
| Randomized upper | Public seed selects empty-only code with probability eta and fixed-length index set otherwise. No target-dependent stopping or uncharged abort bit. Expected length is `(1-eta)B`. |
| Unknown-device common learner | Imported parameter-independent binary estimator returns one legal F. Spectral clipping satisfies distance to true interior E at most twice operator error by Weyl plus triangle; no noncommutative Lipschitz premise. |
| Finite classical readout | Continuous clipping, coordinate rounding with specified ties and finite dictionary selection define a Borel finite partition of the final POVM. Trusted implementation/gate synthesis is not inferred. |
| Two converses not conflated | Query lower from `dimensionlower78`; fixed-decoder payload lower from actual cover. General randomized expected-length lower separately uses Fano–Kraft. |
| Historical results | Every old section and active label retained; global endpoint logarithms and unoptimized full-body dimension factors are untouched. |

`interior_codec_check.py` tests finite exact arithmetic, equality rejection, malformed input, abort-on-incomplete behavior, small matrix grids, two complete scalar dictionaries, replay and all fixed-length words. These tests do not establish the continuum covering, statistical minimax or Fano claims, which are written proofs. No high-dimensional theorem-scale dictionary or physical learner was run.
