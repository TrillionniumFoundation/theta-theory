# Resource ledger — Revision 79

The new `revision_79_interior` entry in `RESOURCE_LEDGER.json` is controlling for Section 61. In particular, worst-record device calls, maximum fresh-block length, trusted tomography operations, exact dictionary enumeration, classical workspace, deterministic index length and randomized expected prefix length are different resources. Public randomness must be independent of the target. The default finite exact codec has no failure or public-randomness requirement. Runtime interruption produces no partial codebook. The learned-word theorem is in the ideal trusted-operation query model, not an efficient synthesis theorem.

The complete predecessor resource ledger is retained below; its version-specific implementation statements refer to v78.

---

# Resources and interfaces — Revision 78

Sections 53–60 distinguish finite-use comparison, unknown-device learning, independent training-block resources, finite trusted controls and deterministic public coding. This ledger keeps their physical and computational costs separate. `RESOURCE_LEDGER.json` is its machine-readable counterpart.

## 1. Measurement, access and representation

An effect `0<=E<=I_d` specifies the ordered binary memoryless measurement `(E,I_d-E)` on the complex Hilbert space `C^d`. A call consumes its input and returns a classical outcome. No residual device quantum output or measurement-environment access is provided. External references and retained tester memory are separately specified resources.

The future distance `d_N` is the supremum of the **unhalved** final joint-state trace norm over common experiments with at most `N` calls, allowing entangled inputs, retained references, coherent controls, feedback and bounded public stopping. Its maximum is two, its one-use value is `2 opnorm(E-F)`, and classical total variation is half the corresponding trace norm. A nonadaptive tester can still use entangled inputs and references.

In the matrix theorems, `matrix_metric.py` and `matrix_codec.py`, `d` is the complex Hilbert input dimension. In retained `biased_codec.py` and `coupled_codec.py`, `dimension=2` or `3` counts real Bloch coordinates of a qubit; the latter is not a qutrit.

| Task | Supplied information | Returned object | Device calls and access |
| --- | --- | --- | --- |
| Pair comparison | Exact legal Gaussian-rational `E,F`; public `d,N` | Exact comparison modulus and proved distance bounds | Zero; does not learn an unknown matrix |
| Common matrix learning | Public `d,N,delta,eta`; one unknown device | Legal Gaussian-rational estimate in the public input basis | Every-record bounded calls; fresh blocks up to `N` in the construction |
| Cap-`b` full-body learning | Same parameters plus public `1<=b<=N` | Legal common estimate | Fresh testers conditionally separated from old memory and isolated during their queries; collective processing at boundaries permitted |
| Fixed-interior learning | Public promise `I/4<=E<=3I/4` and parameters | Legal estimate with future-loss guarantee | Existing independent Choi acquisition and collective processing; fixed failure `1/8` |
| Matrix encoding | Supplied legal rational estimate and public code parameters | One fixed-length index | Zero |
| Matrix decoding | Index and public code parameters | Legal rational effect | Zero; dictionary reconstructed publicly |
| Learned public word | A common learner followed by deterministic encoding | Legal decoded effect meeting the future-loss risk | Only the learning calls |

Pair-dependent hard witnesses receive a supplied pair and serve a converse or comparison. They do not constitute a common estimator. Exact supplied-matrix coding does not implicitly acquire that matrix from a device. Nonpublic parameter headers must be charged separately.

## 2. Current learning laws and resource conventions

### 2.1 Full-body, fresh-block and fixed-interior laws

| Family and training class | Upper calls on every record | Lower calls | Range and sharpness |
| --- | --- | --- | --- |
| Complete body, common matrix construction | `C d^4 N delta^-2 log(d/eta)` | In the common small-error range, `c delta^-2[d^2N+N log(1/eta)]` even for arbitrary coherent adaptive training | `d,N>=1`, `eta<=1/8`; fixed-`d` optimal in horizon, accuracy and confidence; full-body `d^4` unmatched |
| Complete body, cap-`b` fresh blocks | `C d^4(N^2/b) delta^-2 log(d/eta)` | `c delta^-2[d^2N+(N^2/b)log(1/eta)]` in the common range | `d>=2`, `1<=b<=N`; fixed-`d` optimal in `N,b,delta,eta` |
| Scalar effects `d=1`, any cap `b` | `C N delta^-2 log(1/eta)` | Same order | Independent one-call Bernoulli acquisition suffices; block cap has no effect |
| Fixed interior `I/4<=E<=3I/4` | `C d^2N delta^-2` using existing Mele–Bittel estimator and new loss analysis | `c d^2N delta^-2`, even with arbitrary coherent adaptive training | `d,N>=1`, `delta<=2^-13`, fixed failure `1/8`; joint dimension/horizon/accuracy optimum |
| One-use binary operator loss `epsilon` | `C d^2 epsilon^-2` using the cited estimator | `c d^2 epsilon^-2`, coherent adaptive training allowed | `d>=1`, `epsilon<=2^-14`, fixed failure `1/8` |

The common matrix learner retains its absolute cap `delta_0` and confidence `eta<=1/8`. The block theorem uses `delta_*<=min(delta_0,1/4)`. The dimension-dependent lower uses `delta<=2^-13`. A displayed sum of lower bounds uses their intersection, because `max(u,v)>=(u+v)/2`. The sharp fixed-interior law does not assert a new arbitrary-confidence optimum or global rank-boundary extension.

In particular, existing one-call tomography admits a stronger linear-horizon future-loss analysis on a fixed interior. The full body's projective boundary instead forces quadratic horizon cost for the same one-call acquisition class, even with arbitrary collective processing. These are different target families. The new `d^2N` lower does not close the full-body dimension gap.

### 2.2 What is charged and what is public

| Resource | Accounting |
| --- | --- |
| Future horizon | `N` specifies subsequent evaluation loss, not the number of training calls. |
| Training calls | `M` counts unknown-device queries and is capped on every record, including failures and stopping. An expected-time bound is a different resource. |
| Fresh-block cap | `b` bounds the number of calls in each predeclared fresh tester. Internal early exit is padded and its declared length charged in full. |
| Classical feedback | Complete observed history may choose later tester states, lengths, frames, random signs and stopping at block boundaries. |
| Quantum memory in the lower bound | Arbitrary retained output systems and joint boundary processing are permitted. No old retained quantum register can couple into a fresh tester before its final query. |
| Quantum memory in the constructive upper | Blocks execute one at a time. At most `b` physical `d`-level probe registers suffice, each compressed block lying in tensor products of two-dimensional subspaces. No quantum system need pass between blocks. Preparation workspace is separate; no optimal memory bound is claimed. |
| Trusted preparation | The ideal reference construction uses specified product and embedded GHZ states. Section 59 gives finite trusted approximations with certified norm errors at the same loss and risk. Hardware and gate count are separate costs. |
| Public parameters | Hilbert dimension, input basis, horizon, block cap where imposed, loss, confidence, code convention and fixed algorithm. Their representation is excluded from payload only if shared publicly. |
| Unknown target | Matrix entries, spectrum, rank, eigenbasis, gaps, bias, contrast and direction are not supplied to the common learner. |
| Classical output | Legal Gaussian-rational effect in the original public basis, or a public codeword after exact postprocessing. Expanded matrix representation is not the optimal payload. |
| Arithmetic | Spectral algebra, guards, sample-count decisions and finite legal-grid selection have finite specifications. No polynomial-time or optimal bit-arithmetic guarantee follows. |
| Workspace | Records, counters, algebraic values, rational grids and dictionary tables are separate resources. |
| Evidence | Written statistical algorithms and proofs establish risk. Finite reference checks do not execute a physical learner, certify continuum risk, or imply a complete large matrix dictionary. |

Calibration scales may exceed the public horizon by a factor less than two, but use one-input product calls. They control precision, not coherent block length.

Sections 3–7 retain the predecessor's detailed qubit, matrix, codec and certificate ledgers. For the cap-`b` upper construction, their local future horizon is `H=b` and their requested accuracy is `epsilon=delta/ceil(N/b)`. For finite-control transfer, the ideal confidence parameter is `eta/2`. These substitutions apply inside the stated ledgers; they do not replace the external future loss `d_N`.

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
| Simultaneous endpoint calibration | `eta/2` | At most `C d^4 N log(d/eta)` | Legal `A`; on success both regularized support endpoints are comparable and `opnorm(E-A) <= N^-1/2` |
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

## 8. Fresh-block training and coding ledger

Definition `def:freshblocks78` and Theorem `thm:blocklearning78` specify the cap as a property of query access. Conditional on the complete classical history, every fresh input/reference tester is parameter-independent and tensor-separated from old retained outputs. All registers of the active tester remain isolated from old memory until its last query. At the next boundary, arbitrary collective processing is allowed. Merely declaring successive one-query steps “blocks” does not place an unrestricted coherent network in this class.

| Item | Exact accounting |
| --- | --- |
| Predeclared block | Integer `1<=t(h)<=b` fixed before its first call; all `t(h)` calls charged |
| Public stopping | Permitted between blocks using full history; total declared calls at most `M` on every record |
| Within-block operations | Arbitrary references, entangled inputs and adaptive controls using fresh tester registers |
| Boundary operations | Arbitrary common instrument on old and newly completed outputs; arbitrary classical feedback |
| Forbidden coupling for this theorem | Old retained quantum memory into any register of a tester that still has queries to make |
| Local learner parameters | `H=b`; `q=ceil(N/b)`; local accuracy `epsilon=delta/q` |
| Calibration calls | `O(d^4 b log(d/eta))` at local horizon `b` |
| Pair-learning calls | `O(d^4 b q^2 delta^-2 log(d/eta))` |
| Total upper | `C d^4(N^2/b)delta^-2 log(d/eta)`, all records |
| Projective lower | `N^2/(24b delta^2) log(1/eta)` under the stated small-error/confidence range |
| Scalar case | `Theta(N delta^-2 log(1/eta))` for `d=1`, with one-call probes |
| State storage | Unlimited in the lower-bound class; a one-block-at-a-time implementation suffices for the upper |
| Additional code calls | Zero |
| Learned-code error | Learner at `delta/2` plus codec at `delta/2` gives `27delta/32` on success |
| Payload lower | Fixed public deterministic decoder into legal binary effects; positive success for every target forces an actual `d_N` cover |

The fixed-dimensional payload is the same as Section 5 and depends on the future horizon `N`, not on the cap `b`. The cap changes the acquisition cost, not the required accuracy of the decoded reusable effect. The theorem claims simultaneous optimal orders in these separately defined resources, not an optimal combined time/memory/payload objective.

## 9. Finite trusted-control precision

The finite-control theorem applies to the explicit common matrix and block-constrained constructions and their deterministic word outputs. It assumes finite descriptions of trusted preparations/controls and certified bounds on their realized trace/diamond error. It does not assume exact physical preparation, prove a hardware architecture or optimize preparation time.

| Quantity | Budget and meaning |
| --- | --- |
| Ideal statistical target | Original loss `delta`; risk `eta/2` |
| Total known-operation error | Sum of unhalved trace/diamond charges at most `eta` on **every** complete record |
| Final output-law discrepancy | Unhalved trace norm at most `eta`; classical total variation at most `eta/2` |
| Actual target | Same original loss `delta`; failure at most `eta` |
| Preparation count | At most one fresh preparation per block, hence at most a computable public every-record bound `M_*` |
| Per-preparation total error | At most `eta/M_*` when no additional trusted events are charged |
| Rational/algebraic target allowance | Half the per-preparation error; a normalized Gaussian-rational vector describes the target |
| Trusted realization allowance | The remaining half, separately certified for actual preparation |
| Other known controls | If there are at most `S` further events, allocate errors with total at most `eta`; uniform precision order `eta/(M_*+S)` suffices |
| Instruments | Charge the full outcome-flagged CPTP map; sum separate CP-branch bounds before charging |
| State dimension | `D=d^m` for an `m<=b` probe block, or `m<=N` in the original construction |
| Direct coordinate description | `O(D log(D(M_*+S)/eta))` bits |
| State normalization | Algebraic normalization of a nonzero Gaussian-rational vector; exact rational unit amplitudes are unnecessary |
| Channel legality | Rational approximation followed by polar isometry restoration; separately charged trusted realization |
| Sample counts | Integer upper bounds `ell(x)=min{k:2^k>=x}` replace natural logarithms, preserving call order |
| Exact postprocessing | Same algebraic guard and legal output rule on every actual record |
| Additional loss rounding | None: whole-output-law comparison retains the original error event |
| Block boundary | Approximate preparation uses the same fresh input registers, resets/discards workspace and introduces no coherent old-memory coupling |

The description bound is exponential in block width under direct coordinate storage. The logarithmic precision dependence does not make preparation or control synthesis efficient. An error model stated in certified trace/diamond norm is a mathematical control assumption. No physical calibration experiment is represented as performed.

For requested real-valued tolerances, supplied rational tolerances between one half and the requested values preserve orders and the requested guarantees. This is not an arbitrary-real-input oracle. Matrix-code real inputs separately require their own certified representation as in Section 5.

## 10. Joint dimension/accuracy and fixed-interior resources

The information lower bound applies to arbitrary coherent adaptive training with every-record stopping caps, without the fresh-block restriction. Conditional input states may already depend on the unknown packing label. On the weak binary family `E_x=I/2+H_x` with `opnorm(H_x)<=r`, each call adds at most `4r^2` mutual information. The `d^2`-dimensional operator-norm packing and Bernoulli future-loss separation give `M>=c d^2N delta^-2`.

The lower bound already holds on `I/4<=E<=3I/4` and allows an arbitrary legal output effect. A fixed-confidence upper for this family uses the existing Mele–Bittel binary estimator at operator accuracy `delta/(8sqrt(N))`. Its fresh Choi acquisition and collective processing belong to `b=1`; the new interior comparison supplies the loss conversion without a dimension factor. The resulting joint order is `Theta(d^2N delta^-2)` at failure `1/8`, for every `d,N>=1` and `delta<=2^-13`.

| Distinction | Consequence |
| --- | --- |
| Full-body versus interior | Interior excludes the projective boundary that creates the cap-dependent horizon penalty; it remains full-dimensional in matrix coordinates. |
| Fixed confidence versus arbitrary confidence | The sharp joint interior upper/lower law is stated at failure `1/8`. No extra optimized `log(1/eta)` factor is silently appended. |
| Upper provenance | The one-use estimator is Mele–Bittel's; this revision proves the binary joint converse and its interior future-loss reanalysis. |
| Coherent lower versus fresh upper | The interior lower permits all coherent adaptive training, while its upper uses fresh one-call probes. |
| Payload | No new sharp growing-dimensional entropy or efficient public dictionary follows from the interior training law. |
| Finite controls | Section 9 proves the transfer for the explicit common matrix/block constructions; no efficient physical implementation of the imported collective estimator is inferred. |

## 11. Inherited resources and execution evidence

Earlier stochastic label-width, numerical streaming-space, state precision, rational compilation, instrument description, preparation and conditional-state results retain their original resources. The structural companion's fresh nondisturbing classical probes are a separate interface. None of these finite-dimensional results changes aggregate A/B/C/D analytic obligations.

The reviewed v77 run recorded 135,994 common-learning exact checks with 96 negative controls, and 1,038 matrix-codec assertions. Those are historical counts for the predecessor. Complete theorem dictionaries in those checks were scalar; finite matrix grids audited kernels, and a two-dimensional theorem-grid audit was an explicitly incomplete prefix. New finite block, control and information checks have the exact scope stated in their current output and audit files.

Current executed suite counts, ordinary/optimized equality, source/PDF identities, theorem maps, page counts, visual checks and final-head reconstruction belong to the matching generated v78 receipts. This ledger neither anticipates them nor reuses the predecessor's successful workflow as successor verification. It introduces no physical-device execution claim.

Written proofs establish the continuum geometry, entropy and risk bounds. Finite tests check their declared arithmetic and implementation examples. Build and rendered evidence establish reproducibility and layout. Independent human priority assessment remains R02/P01; a review brief, internal agent check, successful build and unsigned commit do not provide human authorship or journal acceptance.
