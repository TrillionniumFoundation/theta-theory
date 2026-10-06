# Revision 75 resource accounting

The theorem concerns supplied descriptions of ordered binary qubit measurements. The target is the effect matrix `E+=((1+b)I+x.sigma)/2`, with `|b|+|x|<=1`; the other outcome is `I-E+`. An encoder receives exact rational target data. A decoder returns legal rational effects in the specified Choi convention.

| Quantity | Convention and result |
|---|---|
| Reusable payload | One index in the full union alphabet, with capacity `L` and length `ceil(log2 L)`. Both spectral coordinates and every observable directional coordinate are included. |
| Bias and contrast | Charged through the two ordered spectral indices. They are not public headers. |
| Direction | Charged through the signed-axis chart and digits when the decoded spectrum is nonconstant. A scalar spectral pair has exactly one word. |
| Public data | Fixed qubit interface, horizon `N`, requested rational error `delta`, and dimension two or three for the implementation's Cartesian vector. The full effect-body theorem uses dimension three. |
| Accuracy | Final joint-state unhalved trace norm under every common adaptive tester, including entangled reference, feedback and public stopping bounded by `N`. |
| Construction certificate | Spectral error at most `delta/4` and angular error at most `delta/4`; the recorded `delta/2` is a proved budget. It is not an exact operational-distance evaluation. |
| Encoder input length | Exact rational numerators and denominators; may affect arithmetic bit complexity independently of the reusable output length. |
| Spectral layout | `B=ceil(8 sqrt(N)/delta)`. The reference implementation uses `O(B^2)` exact-arithmetic operations and retains `O(B)` probability and row-count entries. Each stored integer has its own bit length. |
| Angular layout | Angular words are ranked analytically; the complete set of angular matrices is not enumerated or stored. |
| Mutable workspace | Separate from payload. The theorem does not identify the row-count workspace with a minimal streaming-space requirement. |
| Expanded output | Exact rational Choi matrices. Expansion and their denominator lengths are not the fixed-length index payload. |
| Syntax and metadata | JSON is a transparent container for the index and replay certificate, rather than the optimized binary representation counted by the theorem. |
| Unknown-device queries | Not consumed by this encoder, which receives a supplied description. No sample or query complexity theorem is inferred from the covering law. |
| Physical hardware | The decoded object remains a quantum measurement. The result does not equate a mathematical codeword with a physical classical simulator of entangled inputs. |

For the full ordered binary qubit body, at every integer `N>=1` and an absolute sufficiently small error,

    log2 L_opt = 2 log2 N + log2 log(N+2) + 4 log2(1/delta) + O(1).

The construction applies for rational `0<delta<=1/4`; asymptotic optimality is asserted on the theorem's smaller fixed-error cap. Runtime is finite and pseudo-polynomial in numerical grid size, not polynomial in the binary lengths of all public parameters.

The inherited numerical-streaming bit-space theorems, classical label-width theorems, and public-visibility circle theorem retain their separate hypotheses and resources. Earlier ledgers and their v74 versions remain in the source tree and predecessor audit. No analytic-pipeline completion follows from a change in this supplied-description payload.
