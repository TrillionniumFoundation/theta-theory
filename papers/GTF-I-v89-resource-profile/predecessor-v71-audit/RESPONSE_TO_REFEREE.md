# Response to the controlling v68/r45 reports — Revision 71

**Quantitative manuscript:** Input-Dependent Boundary Coding and the Full Error Range.
**Structural companion:** Finite Physical Actions and a Strong Converse for Repeatable Observations.
**Base:** completed v70 final head `a5cd3bb0ea9c29f680381230c603e54354866376`.
**External report:** `e862e5c963ef36b9caa3b1b814b495ae4428a088`.
**Pipeline audit:** `a3fd5b80549a855c46151fd7183b3fc7139abac7`.

The latest located reports review v68. V70 was already completed and independently rebuilt on the remote before this revision began; its coherent-boundary theorem and the CMW literature correction are inherited, not new v71 claims. No v70-specific external report was located in the opening survey. We retain the general-journal mathematical objective and every prior active proof, and respond with two additional theorem packages.

## Principal mathematical response

The earlier boundary results included preparation-only and coherent-tensor models, whose outcome probabilities did not depend on the input. The new family measures one fixed input basis and sends input row x to a tuple sigma_xy of conditional output states. Its outcomes genuinely depend on the input, and it destroys input coherences. Conditional states may have singular and varying supports. With V=sum_x(sum_y r_xy(2n-r_xy)-1), the joint description length is

    (V/2) log2 N + V log2(1/delta) + O(1),
    N>=1, 0<delta<=delta_*<2.

A common row-state programme supplies the upper adaptive modulus, and independent exact factor encoders supply legal rational centres with rank nonincrease and zero preservation. A product maximal-rank patch supplies the converse. A separate CPTP idempotent-input retraction proves that arbitrary legal memoryless covering centres do not improve the optimum over fixed-readout centres. This operation can increase rank and is not confused with the rank-aware encoder.

The full positive-error range is obtained by a new lower argument. The local binary separation bound alone cannot reach delta>=1, because it would need pairwise distances greater than 2delta in a metric of diameter two. Instead one common finite-dimensional estimator yields disjoint success events; a centre can be assigned at most 1/(1-eta-delta/2) such events. This gives the N^(dimension/2) lower term at every fixed error below two. Combining it with the inherited small-error precision term proves the full-range interior and preparation laws, as well as the new conditional law. No uniformity as delta_* approaches two is asserted; at error two one centre suffices. This argument does not extend the coherent N-scale theorem.

These are fixed-dimensional supplied-description theorems. The encoder is not learning an unknown instrument, and the decoder still specifies a quantum operation. The readout basis is fixed. Neither the classical programme idea, informationally complete estimation, rank-stratum dimensions nor rowwise quantization is claimed as an individually new principle. The focused comparison identifies the direct cq/common-measurement and process-estimation antecedents.

## Fourteen required revisions

### R45 required 01 — Direct replacer-channel antecedent

The CMW comparison introduced in v70 is retained in the focused comparison and bibliography. Its two-replacer discussion and asymptotic binary exponents are not claimed to prove finite-family covering or the conditional row-programme bound.

### R45 required 02 — Supplied-data interface

Page one and the conditional-code theorem specify that the encoder receives target matrix data. The common tomography experiment is only a converse witness; no optimal learning theorem is inferred.

### R45 required 03 — Physical implementation

The theorem and resource ledger state that the decoded object is a quantum instrument, not a finite-classical-message processor for unknown entangled inputs. The dN row-state programme is a proof device.

### R45 required 04 — Dimensions and public ranks

The new theorem fixes d,n,m, all conditional output-rank bounds and delta_*<2. The remainder can depend on those data. Conditional Choi ranks are the sums of the row ranks.

### R45 required 05 — Interior versus boundary

The positive-margin general instrument law remains separate from the rank-boundary preparation and conditional laws. The latter have no positive eigenvalue floor; the measured input basis is fixed.

### R45 required 06 — Qualify boundary uniformity

The title and abstract identify the input-dependent fixed-readout family. No claim of boundary uniformity over the whole instrument body is made.

### R45 required 07 — Metric convention

Every new covering theorem uses the unhalved final-state trace norm over the same adaptive quantum tester, with references, quantum memory, feedback and bounded public stopping. Event probabilities therefore incur delta/2, not delta.

### R45 required 08 — Pair-dependent tests

The inherited small-error local Choi proof remains pair dependent. At larger errors a new common estimator produces simultaneous disjoint events. These are two distinct witnesses, not an accidental substitution of a universal test into the old proof.

### R45 required 09 — Rank variables

The r_xy are ranks of conditional output blocks sigma_xy. Choi outcome rank is sum_x rank(sigma_xy). Preparation-only output ranks retain their earlier factor d in Choi rank. Arbitrary Choi-rank strata are not parameterized by V.

### R45 required 10 — Payload and workspace

The new codec counts the sum of row masks and fixed-length integer bodies. JSON length, source-data size, rational intermediate workspace and expanded Choi matrices are separate. Each row is normalized independently.

### R45 required 11 — Accuracy range

Sections 45 and 46 prove an extension, rather than retaining delta<=1/32 by default. Interior, preparation and fixed-readout conditional laws now hold uniformly on 0<delta<=delta_*<2. A common-estimator multiplicity bound handles delta>=1, where one-centre-per-point separation is unavailable. Constants depend on the fixed cap. The coherent tensor law is not extended.

### R45 required 12 — Separate v63 width crossover

All hidden-label width results and their remaining multiplicative crossover gap are retained under the original resource definition. The new description theorem changes none of those assertions.

### R45 required 13 — Independent priority review

The direct SHW fixed-common-measurement antecedent and tomography comparison are added. The inherited CMW correction remains credited to v70. No independent reviewer has been commissioned through a tool in this revision, and no author-side file is represented as an external opinion. The external priority request remains explicitly outstanding.

### R45 required 14 — Focused versus complete submission object

The focused quantitative manuscript carries the new full-range and conditional boundary proofs alongside the complete prior focused results. The structural article is independent. The combined edition retains all active mathematics and remains archival; no arbitrary mathematical deletion or submission-target change is used to shorten it.

## Twenty-four detailed comments

### R45 detailed 01 — Binary constants

The inherited 3/32 lower bound is for halved classical TV; d_N is unhalved trace. The new common-event coefficient is 1-eta-delta/2.

### R45 detailed 02 — Choi projection

The local positive spectral projection still depends on the pair. The coordinate binary POVMs in the new estimator are instead fixed before selecting the packing.

### R45 detailed 03 — Covering centres

All legal memoryless centres are allowed in the lower bounds. The input-dephasing retraction exactly reduces the centre class, but need not preserve the target rank bounds.

### R45 detailed 04 — Affine space

The interior patch remains in the joint marginal affine space. The new conditional patch has one normalization per input row, hence V=sum_x v_x rather than one normalization for all rows.

### R45 detailed 05 — Saturation

Small-error packing keeps its delta<=1/32 constants. The larger range is proved separately by bounding centre multiplicity. No comparison 2delta<diameter is asserted at delta>=1.

### R45 detailed 06 — Input erasure

The exact preparation product identity remains preparation-only. The conditional family gets a row-programme sandwich, not that equality.

### R45 detailed 07 — Quantum processor

The row-selection processor preserves the conditional reference operator after the fixed input measurement. It is quantum, not a physical classical simulation protocol.

### R45 detailed 08 — Zero pivots

The existing proof that a zero PSD diagonal forces a zero row/column remains intact in the active factor-code section and implementation.

### R45 detailed 09 — Pivot positions

Each row code includes its inherited pivot-position mask, not just a rank count. Public input row order is fixed.

### R45 detailed 10 — Rank decrease

The codec claims only nonincrease of conditional output ranks. Retraction of arbitrary centres may increase rank, and is separated from the upper encoding guarantee.

### R45 detailed 11 — Discarded factor columns

Directed rounding can eliminate a factor column. That is permitted and does not break positivity or the advertised rank bound.

### R45 detailed 12 — Squared rational factors

The executable encoder uses rational squared coordinates and integer-square-root comparisons. It never outputs a rational Cholesky factor of the original target.

### R45 detailed 13 — Denominators

Each decoded row has normalizer T_x<=h_x B^2. Expanded joining uses lcm(T_x), at most B^(2d) product_x h_x. This size is not hidden inside the compressed body count.

### R45 detailed 14 — Local charts

The lower proof uses a product of sufficiently small maximal-rank row charts, each with a leading-block inverse. No global support chart is claimed.

### R45 detailed 15 — Singleton

V=0 is explicitly separate. Every row is then a fixed one-dimensional unit block at the public permitted outcome; no payload is required.

### R45 detailed 16 — Classical case

The main text keeps the preparation m-1 example and adds the conditional d(m-1) stochastic-matrix case.

### R45 detailed 17 — Standard dimensions

n^2-1 and 2n-2, and their conditional sums, are credited as standard rank-stratum dimensions. The new theorem determines the declared adaptive coding scale, not a new manifold dimension.

### R45 detailed 18 — Legal codebook

Only valid decoded row words count as centres. Off-diagonal input blocks are rejected by encode; they are altered only by the separately named retraction command.

### R45 detailed 19 — Decode versus verify

Bare decode certifies syntax, positivity, marginal and formal budget. Target-bound verification replays the supplied target encoder and checks the complete canonical certificate.

### R45 detailed 20 — Binary regression

All prior exact binary tests execute, but the continuum derivative proof is the premise of the small-error theorem.

### R45 detailed 21 — Rank regression

Independent Gaussian-rational elimination checks finite ranks. The written row-chart proof, not finite tests, proves the full stratum exponent.

### R45 detailed 22 — Authorship

Git hashes and the read-only final-head build establish source/artifact identity. No cryptographic author signature or independently signed referee report is claimed.

### R45 detailed 23 — V69 anchor

The base is completed v70. The unfinished v69 anchor supplies no theorem premise and is not advertised as a completed revision.

### R45 detailed 24 — Global pipeline

The frozen analytic history and all A/B/C/D aggregate flags are preserved. Common finite-dimensional estimation supplies no LLT, stopped LDP, filtering/LAN, Mosco/Nisio or response gate.

## Proof, history and execution evidence

The new proofs are in `sections/45-full-error-coverings.tex` and `sections/46-input-dependent-boundary.tex`. `conditional_codec.py` implements exact encode/decode/retract/replay, and `check_conditional.py` includes input-dependent classical feedback policies, pure programme trace comparisons, zeros, extreme eigenvalue ratios, independent rank checks, a rank-increasing retraction example, and a large-error centre covering multiple mutually singular targets.

The manifest pins every native v70 source at its original inherited path; all prior active mathematical labels remain in their quantitative, structural and complete proof graphs. The frozen pipeline history and ledgers are consulted as dependencies, not as evidence of significance. Source qualification, isolated reconstruction, final-head read-only verification and finite regressions report only actual executed evidence. They do not certify universal proofs, independent priority, authorship, acceptance or the unrelated analytic programme.
