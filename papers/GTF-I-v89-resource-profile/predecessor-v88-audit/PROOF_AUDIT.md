# Proof and resource audit — Revision 88

This is an author-side audit of written proofs. It is not a formal proof-assistant verification or an independent specialist priority opinion. Both R57 reports and every predecessor mathematical section are retained verbatim.

## 1. The new resource class

At classical history h, the complete fresh probe-reference state sigma_h is identical under the two hypotheses and factorizes from the old receiver state. The old conditional receiver states may differ, be subnormalized, and have arbitrary quantum dimension. Within the new block, arbitrary coherent adaptive control is allowed. After acquisition, one common quantum instrument acts jointly on the new output and all receiver memory, retaining both quantum memory and a classical outcome. Only the classical outcome determines the next fresh preparation. No old quantum system is imported coherently.

This is not the same as independent blocks or separable probe marginals. It contains the former and is contained in the unrestricted adaptive class. A single block of reserved size N gives exactly the unrestricted adaptive class. The b=1 class includes classical input feedback and quantum receiver memory, so no equality with the independent-product distance is asserted.

Each node reserves a positive integer n<=b, internal unused slots are padded and charged, and every terminal path has total at most N. The finite depth is at most N. This is a worst-record resource bound, not an expected sample-size assumption. Receiver-only processing is absorbed into the preceding instrument or terminal channel. Public randomization is a retained classical outcome with the same rule under both hypotheses.

## 2. Conditional fidelity rather than false tensorization

For arbitrary positive receiver operators R0,R1, fresh acquisition appends R0 tensor omega0 and R1 tensor omega1. Root fidelity is multiplicative at this one conditional append step. Applying the common receiver instrument and retaining its classical record makes the sum of conditional root fidelities no smaller. The instrument may entangle old and new memory, so no product decomposition is asserted afterward.

The induction statement holds for every incoming positive pair, not just equal or normalized states. If every continuation from node h costs at most A_h<1 in fidelity deficits and the current node costs a, every child costs at most A_h-a. The lower factor is

`(1-A_h+a)(1-a) = 1-A_h+a(A_h-a) >= 1-A_h`.

All child sums are nonnegative; countably many outcomes are allowed. A zero-probability history requires no division. If A>=1 the claimed positive-part lower is zero and is immediate. Finite depth closes backward induction. This proves the generic lemma even with quantum receiver memory, history-dependent measurements/preparations, variable block budgets and stopping.

The lemma uses standard fidelity multiplicativity, direct-sum additivity and channel monotonicity. Its application to this reset-width model and the pathwise quadratic cost is the asserted resource result; the underlying fidelity identities are not priority claims.

## 3. A fresh adaptive block

For a lineality tangent all Q_j H_j Q_j vanish. The inherited canonical, generally nonhorizontal, factor and its normalized surrogate give isometries W0,Ws with `||Ws-W0||<=alpha*s`, alpha=3||B||/2, and device diamond remainder at most r*s², r=Lambda+K. Here `K=k||B||²(2+max_j||H_j||op)`.

Purify an arbitrary fresh n-call adaptive tester. Successively replacing W0 by Ws in the n slots costs at most n*alpha*s in purified vector norm, since all surrounding common factors are isometries. The proof is valid when internal controls depend coherently on earlier labels and reference memory. Dilation environments are inaccessible and never offered to the tester. Bounded internal stopping is padded within the reserved n slots.

Replacing the surrogate by the actual tube member costs at most n*r*s² in unhalved trace norm by adaptive channel telescoping. With root fidelity f and Bures `d_B²=2(1-f)`, the inequalities are `d_B²<=||rho-sigma||1<=2sqrt(1-f²)<=2d_B`. Thus the actual block Bures bound is

`s(alpha*n+sqrt(r*n))`.

Only after retaining the full quadratic channel error is its square root taken. Since n>=1, the fidelity deficit is at most gamma*n²*s² with `gamma=(alpha+sqrt(r))²/2`. The upper is uniform over the input, reference and internal controls. It is not the sharper horizontal regular-direction estimate; the two factors have distinct roles.

## 4. Policy-sensitive upper and sharp orders

Let `Q=max_paths sum n(h)²`. Conditional fidelity accumulation gives `f_out>=(1-gamma*Q*s²)_+`. If gamma*Q*s²<=1, `1-(1-x)²<=2x` converts to unhalved trace bound `2sqrt(2gamma*Q)*s`; if it is larger, cap by two. This is exactly `min(2,2(alpha+sqrt(r))*s*sqrt(Q))`. The every-record constraints imply `Q<=bN`.

This proves the coherent upper for the larger reset class. Its matching lower is already in v87: independent pre-encoded parallel GHZ blocks are a permitted reset policy. The lower pays the full m*kappa*s² error before the finite Bernoulli amplification and keeps both integer allocation cases. Nothing depends on the unknown remainder. Regular directions use the retained product lower and unrestricted adaptive horizontal upper including `(Lambda+K_h)Ns²`. Support opening uses a classically impossible-output event and the adaptive hybrid upper. Thus the three-row theorem is uniform in N,b,F on one fixed E,H,Lambda interval.

No claim is made that the displayed constants remain bounded through vanishing support eigenvalues, collapsing correction gaps or varying remainder allowances. The sufficient nonempty s_* and Lambda_* from v87 are not the discrimination interval s0 or a minimal allowance. A zero tangent remains a higher-order question. A power substitution requires the entire inherited O(t^(2q)) remainder condition.

## 5. Feedback versus coherent memory

At b=1, the coherent tangential scale remains sqrt(N)s despite arbitrary classical feedback and quantum receiver memory. The larger parallel and adaptive classes achieve Ns locally. The distinction is the ability to maintain coherence between different unknown-device inputs, not a ban on quantum receiver storage. This is not a global theorem that feedback is useless or that exact distances/error exponents coincide.

A shared quantum reference correlating later fresh inputs violates the reset condition even when probe marginals are separable. It is therefore not silently covered by the conditional append step. The exact b=N reset/adaptive class identity has a different status from the inherited parallel/adaptive local-order comparison.

## 6. Exact finite policy certificates

`feedback_budget.py` verifies a finite public policy graph, its complete reachable successors, acyclicity, reserved integer widths and hard pathwise call maximum. A DAG is an optional finite representation of repeated subtrees. The recurrence uses maxima, not averages. An unreachable, missing, repeated or cyclic successor is rejected. A node cap produces refusal, not a partial certificate.

With rational gamma and s supplied, the executable computes both the additive budget lower and a stronger backward product lower from `(1-gamma*n²*s²)_+`. These are conditional on the user-supplied gamma dominating every node's fidelity deficit coefficient and on the actual physical reset condition. The code does not establish either premise. The trace-square upper is an upper certificate, not the exact operational distance.

## 7. Executed finite quantum tests

The suite contains 8430 positive checks, 18 rejection controls, and 180 complete receiver-memory experiments on 45 policies with N<=5. Fresh rational qubit states have root fidelity `1-2x²/(1+x²)`, x=n*s. The receiver performs a rational joint rotation, controlled-NOT and a complete binary instrument, retaining a qubit memory. Later reserved widths depend on the classical history. Every branch and terminal state is enumerated exactly.

The replays cover equal, unequal nonorthogonal, subnormalized and zero incoming receiver states. CPTP instrument completeness, local conditional monotonicity, leaf normalization, policy-budget bounds and final fidelity are checked. These examples genuinely include quantum receiver processing and feedback; they are finite state experiments, not execution of a general unknown-POVM learning or correction protocol.

Negative controls include malformed rational fields, wrong integer types, width and total-budget violations, omitted successors, unreachable nodes, cycles, duplicated children/JSON keys, cap refusal and certificate mutation. Ordinary and optimized Python results must agree. All 25 inherited suites execute anew. None of these finite checks proves a continuum theorem or independently establishes novelty.

## 8. Literature and preservation

The main comparison now spells out the HMNW Theorems 17 and 19 bounds, credits the Yuan–Fung antecedent for the parallel bound, and retains the separate tube remainder. GHPS is compared at the fixed-block composite Stein task and its optimization order, not treated as the present finite local theorem. Salek–Hayashi–Winter is retained for classical-feedback antecedents; their fixed-pair exponent result is not conflated with this shrinking tube and hard call budget.

All 632 predecessor native files are represented. Every old section is byte-identical and active, and old introduction labels remain in the current introduction. The new section is active in both primary and complete edition. The structural graph is unchanged. New native-source, publication and final-head receipts are required. Independent human priority, signatures, physical execution and the separate analytic A/B/C/D flags are not manufactured by the revision.
