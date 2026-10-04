# Resources and interfaces — Revision 77

Sections 53–57 distinguish finite-use comparison of supplied effects, common learning from an unknown device, and deterministic coding of a supplied rational estimate. This ledger records their resource conventions; `RESOURCE_LEDGER.json` gives the machine-readable counterpart.

## 1. Measurement and access interfaces

An effect `0 <= E <= I_d` specifies the ordered binary measurement `(E,I_d-E)` on the complex Hilbert space `C^d`. Each memoryless call consumes its input and returns a classical outcome, with no residual quantum output or measurement-environment access. The finite-use distance `d_N` is the supremum of the **unhalved** final joint-state trace norm over common experiments with at most `N` calls, allowing input entanglement, retained references, feedback, and bounded public stopping. Its maximum is two and its one-use value is `2 ||E-F||_op`. Classical total variation is half the corresponding classical trace norm. The nonadaptive restriction retains block entanglement and references while excluding feedback.

In the matrix theorems, `matrix_metric.py`, and `matrix_codec.py`, `d` is the complex Hilbert input dimension. In inherited `biased_codec.py` and `coupled_codec.py`, `dimension=2` or `3` counts real Bloch coordinates of a qubit; the latter is not a qutrit.

| Task | Information supplied | Output | Unknown-device calls |
| --- | --- | --- | --- |
| Matrix comparison | Exact Gaussian-rational effects `E,F`; public `d,N` | Exact midpoint-resolvent modulus and its proved distance bounds | None |
| Common learning | Public `d,N,delta,eta`; access to one unknown measurement | Legal estimate; rational output available in the fixed public basis | Bounded on every training record |
| Matrix encoding | Supplied legal Gaussian-rational effect; public `d,N,delta` | One fixed-length dictionary index | None |
| Matrix decoding | Index and the same public `d,N,delta` | Legal Gaussian-rational effect | None |
| Learned matrix code | The common learner's rational estimate, followed by the supplied-matrix encoder | Reusable word meeting the future-loss guarantee | Only the preceding learning calls |

Pair-dependent metric witnesses receive a known pair. They are not the common unknown-device learner. An exact supplied-matrix encoder does not acquire its matrix from a physical device.

## 2. Learning resources and ranges

Theorem `thm:matrixlearning77` applies to every `d,N >= 1`, `0 < eta <= 1/8`, and sufficiently small `0 < delta <= delta_0`, with absolute `delta_0 <= 1/4096`. It proves

\[
 \sup_{E\in\mathfrak E_d}\mathbb P_E
 \{d_N(\mathcal M_E,\mathcal M_{\widehat E})>\delta\}\le\eta,
 \qquad M\le Cd^4N\delta^{-2}\log(d/\eta).
\]

Every common procedure with this risk and a deterministic cap on every training record obeys

\[
 M\ge cN\delta^{-2}\log(1/\eta).
\]

The minimax law is therefore `Theta_d(N delta^-2 log(1/eta))` for each fixed dimension. The `d^4` upper dependence is not asserted optimal; the scalar converse gives no matching growing-dimension factor. The complete qubit subroutine `thm:commonlearn76` has the same law with absolute constants.

| Resource | Common learner accounting |
| --- | --- |
| Future horizon | `N` specifies the subsequent loss `d_N`, independently of the training budget. |
| Training calls | `M` counts calls made to learn the device. Its bound holds on every record, including concentration failures, first rejection, and fallbacks. The converse uses this same convention, not expected stopping time. |
| Entangled block | At most `N` inputs. The qubit selector uses powers of two up to `2^floor(log2 N)`; the matrix learner embeds these blocks into learned two-dimensional subspaces. |
| Retained quantum memory | Blocks execute one at a time. The qubit construction prepares at most `N` input qubits, retains at most `N-1` unused qubits after the first call, and retains no quantum system between independent blocks. In dimension `d`, up to `N` physical `d`-level inputs suffice; each compressed block is supported on a tensor product of two-dimensional subspaces. These are sufficient constructions, not optimized memory bounds. |
| Trusted preparation | Ideal preparation of the specified product states, embedded GHZ blocks, and known-frame operations is allowed. Each GHZ block draws a fresh sign with conditional probabilities `1/2,1/2` given the entire preceding record. Hardware, gate count, and preparation precision are separate costs. |
| Public parameters | Dimension, fixed input-coordinate convention, future horizon, loss, confidence, and deterministic algorithm. If not public, the chosen header representation must be charged separately. |
| Unknown target | No exact matrix, spectrum, gap, multiplicity, eigenbasis, bias, contrast, direction, or candidate pair is supplied. All learned frames depend only on public parameters and observations. |
| Classical output | The qubit procedure gives a legal real effect with a finite algebraic description. Matrix postprocessing can give a legal Gaussian-rational effect in the public input basis. Expanded estimates are distinct from the optimal payload. |
| Classical time | Sample counts, algebraic spectral choices, and rational postprocessing are finite. No polynomial or optimal runtime follows from the device-call theorem. |
| Classical workspace | Records, counters, algebraic entries, rational approximation tables, and postprocessing grids are separate from the transmitted word. No optimal learning-workspace bound is claimed. |
| Implementation evidence | The complete learner is a written statistical algorithm. Finite exact checks cover its algebraic and control-flow ingredients; no full stochastic learner execution, physical training session, or executable continuum risk certificate is claimed. |

The calibration scale `2^ceil(log2 N)` can exceed `N`, but calibration uses only single-input product calls. That scale controls precision and sample counts, not entangled block length.

## 3. Complete qubit confidence and stopping ledger

The coarse Pauli test selects a product branch with six fresh Pauli groups or an entangled branch with data-dependent two-plane observations. Both end with two fresh endpoint groups after fixing the final direction.

| Batch | Failure allowance | Conditioning |
| --- | --- | --- |
| Coarse Pauli vector | `eta/8`, jointly over six groups | Unconditional |
| Product-branch Pauli vector | `eta/8`, jointly over six fresh groups | Given the coarse record; only when that branch is taken |
| Dyadic stage `m` | `eta m/(32N)`; all possible stages sum to at most `eta/16` | Given the record before the reached stage |
| Fine two-plane estimate | `eta/8` | Given the entire selection record, including its random length and frame |
| Fresh endpoint group on each signed axis | `eta/16` each; total `eta/8` | Given the final axis; fresh conditional Bernoulli samples in either branch |

The conservative total is `9eta/16 < eta`; inactive branches contribute no event. If `T_m` says that stage `m` is reached and `F_m` contains its preceding record, then

\[
 \mathbb P_E(T_m\cap G_m^c)
 =\mathbb E_E[\boldsymbol1_{T_m}
       \mathbb P_E(G_m^c\mid\mathcal F_m)]
 \le\epsilon_m\mathbb P_E(T_m)\le\epsilon_m.
\]

No independence between adaptive failure events is assumed. Fresh-block concentration holds on every reached record; cone localization is needed to turn the means into directional information.

`SelectBlock` returns at the **first** rejected amplitude or phase guard, carrying the preceding accepted length and its updated direction. It never retries or tests a larger scale after rejection. First-stage rejection returns `(1,w_0)`. Equality at amplitude `1/4` is accepted. Both complex estimates must satisfy `Re(z)>0` and `8|Im(z)|<=Re(z)` before a phase is used. This gives defined outcomes for zero estimates, the principal-argument branch cut, and out-of-cone phases. A final fine-phase failure retains the selected direction. A zero product-vector estimate uses the fixed third coordinate direction; public coordinate order resolves frame ties. Endpoint frequencies are sorted within `[0,1]`; ties give a scalar effect.

With

\[
 B(\zeta,\epsilon)=\lceil4\zeta^{-2}\log(8/\epsilon)\rceil,
 \quad L=\log(C_2/\eta),\quad n_0=\lceil C_0L\rceil,
 \quad n=\lceil C_1N\delta^{-2}L\rceil,
\]

the product branch uses exactly `6n_0+8n` calls. There are four settings in every two-plane batch. For `H=2^floor(log2 N)`, the entangled branch uses at most

\[
 6n_0+4\sum_{m=1,2,4,\ldots,H}mB(\kappa,\eta m/(32N))
 +4m_*B(c_*\delta\sqrt{m_*/N},\eta/8)+2n.
\]

This sum includes all possible later stages even if rejected earlier. Weighted dyadic logarithms give `O(N log(1/eta))`, using the convergent sums of `2^-k` and `k2^-k`. On every returned record,

\[
 m_*\zeta_*^{-2}=c_*^{-2}N\delta^{-2}.
\]

All ceilings and fallback lengths are included in these worst-record budgets.

## 4. Matrix calibration and compression ledger

For `d >= 2`, put `s=binom(d,2)`. Calibration uses `h_d=2d^2-d` product settings per stage and `K_d=(320d)^2`. Its clipping and rescaling return a legal algebraic estimate on every record; a fixed algebraic convention chooses eigenbases, including at multiplicities.

| Stage | Failure allowance | Calls on every record | Output |
| --- | --- | --- | --- |
| Simultaneous endpoint calibration | `eta/2` | At most `C d^4 N log(d/eta)` | Legal `A`; on success both regularized support endpoints are comparable and `||E-A||_op <= N^-1/2` |
| Each of `s` qubit learners | `eta/(2s)` | At most `C N(d/delta)^2 log(d/eta)` | Legal estimate in one pair of calibration eigenvectors, at requested loss `c_* delta/d` |
| Weighted legal rational selection | Zero | Zero | Legal Gaussian-rational effect in the public input basis |
| Subsequent matrix encoding | Zero | Zero | Reusable word when requested |

Pair guarantees are conditional on the calibration record and use fresh experiments. Their declared allowances sum to `eta/2`; calibration and pairs give total risk budget `eta`. Each pair uses its own internal qubit confidence ledger, without charging it twice. Dimension one uses Bernoulli endpoint estimation. At `N=1`, calibration may return `I/2` without observations.

Calibration simultaneously compares `E+N^-1 I` and `I-E+N^-1 I`, and bounds compression-induced extra variance by `N^-1`. The pair learners consequently attain the future-loss resolution in their learned basis. Fixed uncalibrated coordinate restrictions do not replace this step.

## 5. Deterministic rational matrix code

Theorem `thm:matrixcodec77` gives one finite exact encoder/decoder for every integer `d,N >= 1` and rational `0 < delta <= 1`. Its publicly reconstructed dictionary has radius at most `11delta/16` and cardinality at most

\[
 C_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]

For `0 < delta <= delta_d`, the fixed-length word has the matching optimal length

\[
 \frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1).
\]

Two-sided optimality uses the small-error covering theorem. The finite construction and its upper size bound have the separately stated range `0 < delta <= 1`.

| Resource | Matrix codec accounting |
| --- | --- |
| Encoder input | Supplied legal Gaussian-rational matrix in the public basis. A real input requires a supplied representation; certified coordinate approximations to `1/(8K)` suffice. Physical-device acquisition is not implicit. |
| Public reconstruction | `d,N,delta`, coordinate order, rounding ties, and the fixed algorithm determine the dictionary. No target-dependent advice or preassigned centre list is supplied. |
| Ambient grid | `K=ceil(32dN/delta)`; at most `(K+1)^d(2K+1)^(d(d-1))` bounded Hermitian coordinate tuples before legality filtering. |
| Greedy rule | Exact tests `Q_N(G,C)^2 > (delta/16)^2`; the encoder uses the first eligible retained centre after inward rounding. No triangle inequality for `Q_N` is used. |
| Fixed payload | `ceil(log2 L)` bits for one index, where `L` is the completed dictionary size. Both parties reconstruct the same list. All identifiable effect coordinates are charged through this index; no centre coordinates accompany it. |
| Decoder | Reconstructs the list and returns the indexed legal effect. Unused words of the fixed length map to `I/2`. |
| Device calls | Zero for dictionary construction, supplied-matrix encoding, decoding, and replay. |
| Field operations | Exact Schur legality tests; a conventional dense pairwise Sylvester solve takes `O(d^6)` field operations and `O(d^4)` stored field elements. Each candidate may be compared with the retained list. |
| Stored dictionary | The literal algorithm retains `O(Ld^2)` rational entries in addition to solver/traversal workspace; the decoder repeats construction. |
| Bit arithmetic | Rational numerator/denominator growth, input coefficient lengths, and interpreter overhead are additional. Field counts do not establish optimal bit complexity. |
| Efficiency | The finite grid gives termination. Enumeration can be enormous; polynomial runtime in payload length is not claimed. |
| Cutoff | `matrix_codec.py` reports incomplete construction if a resource cap prevents completion. It emits no purported completed codebook or payload. A prefix audit remains explicitly incomplete. |

Public parameters, expanded matrices, JSON envelopes, work tables, physical hardware, and training records are not the fixed-length index. A nonpublic parameter needs its own charged header representation. The retained exact joint qubit encoder keeps its separate rational Cartesian input, spectral-layer runtime, payload, and workspace conventions.

## 6. Learning followed by coding

Corollary `cor:matrixlearnedcode77` composes the interfaces. For rational requested `delta` in the intersection of the learning and small-error entropy ranges, run the matrix learner at loss `delta/2`, confidence `eta`, and encode its legal rational output with public coding accuracy `delta/2`. The coding error is at most `11delta/32`, so on the learning success event the decoded effect has future loss at most

\[
 \delta/2+11\delta/32=27\delta/32<\delta.
\]

Postprocessing introduces no additional failure event or device calls. It preserves the fixed-dimensional minimax training order and attains the full-matrix optimal payload above. Confidence is a public training parameter, not an extra target coordinate in the word; dictionary reconstruction remains a classical computation cost. The inherited qubit corollary `cor:learncode76` similarly uses rational rounding and the retained exact qubit code. Both start from observed estimates, not exact unknown-target descriptions.

## 7. Supplied-pair matrix certificate

`matrix_metric.py` solves

\[
 VX+XV+N^{-1}X=F-E,\qquad
 V=\frac{E+F}{2}\left(I-\frac{E+F}{2}\right)
\]

for supplied legal Gaussian-rational effects, returning `Q_N^2=N tr((F-E)X)`, the solution, and exact squared bounds `min(1,Q_N^2)/(8192d)^2` and `min(4,64Q_N^2)`. These encode

\[
 \frac1{8192d}\min\{1,Q_N\}
 \le d_N^{\rm na}\le d_N\le\min\{2,8Q_N\}.
\]

Legality uses exact Schur elimination, including zero-pivot rules. Replay recomputes the whole supplied pair and the horizon where pinned. The certificate evaluates the comparison modulus, not the exact adaptive optimum. Conventional unit-cost legality costs `O(d^3)` field operations; the dense `d^2`-variable Sylvester solve costs `O(d^6)` operations and `O(d^4)` stored field elements. `MATRIX_METRIC_SCHEMA.md` fixes the executable representation.

## 8. Inherited resources and evidence

Earlier stochastic label-width, numerical streaming-space, state-precision, rational-compilation, instrument-description, preparation, and conditional-state results retain their original hypotheses and resources. The structural companion's fresh nondisturbing classical probes remain separate from consuming quantum measurements. Finite-dimensional results do not change aggregate A/B/C/D analytic obligations.

The common-learning regression reports **135,994 exact checks and 96 negative controls**, including finite first-rejection transcripts. The matrix-codec regression reports **1,038 assertions**: complete theorem dictionaries are one-dimensional, small complete matrix grids audit kernels, and the two-dimensional theorem-grid audit is an explicitly incomplete prefix. These are finite computational examples and implementation contracts. They do not prove continuum metric, entropy, or risk theorems, execute the full stochastic learner, or demonstrate full higher-dimensional dictionary enumeration. Generated outputs and the final build receipt identify the evidence bound to the submitted sources.

Source hashes, theorem maps, proof-preservation checks, page counts, and final-head reconstruction establish their stated forms of provenance and reproducibility. They do not establish human authorship, independent priority clearance, or journal acceptance. Internal agent cross-review is identified as such. Current label and page counts come from generated evidence rather than estimates in this ledger.
