# Finite-outcome proof audit — v82

This is an author-side dependency and error-accounting audit, not independent human priority clearance.

| Step | Written justification | Boundary checked |
| --- | --- | --- |
| Matrix horizontal lift | Solve `dot X=X A^-1 H/2`; uniqueness gives `X*X=A` | Noncommuting A,H; no chosen eigenbasis |
| Horizontal cancellation | `sum_j X_j*dot X_j=(sum_j H_j)/2=0` | Exact tuple normalization is essential |
| Adaptive path | Purify common controls, cancel cross-slot inner products | External reference allowed; dilation environment inaccessible |
| Stopping | Pad stopped branches with discarded dummy calls | At most N calls, same control rule |
| Inverse variance bound | `A_j^-1<=2k I` and congruence by H_j | No incorrect commuting product order |
| Lower geometry | Eigenvector for one component, repeat N times, coarse-grain | Arbitrary legal centres, including boundary centres |
| Entropy | Genuine p-dimensional affine norm ball, p=(k−1)d² | No d-dependent Euclidean conversion |
| Grid | Inward margin 2e; first k−1 rounded, last exact residual | Individual error<=d/K; residual<=e=(k−1)d/K |
| Effective real input | Grid approximation<=3t/4<t | Strict certified search terminates, no exact real comparisons |
| Greedy code | Strict r>s; closed assignment tests | Actual norm packing, not triangle inequality for Q_N |
| Common upper | Public bit probability 3/4 at j, 1/4 otherwise | Exact reference-preserving binary effect I/4+E_j/2 |
| Legal output | Finite net at epsilon/2 and distance<=2epsilon to every B_j | Deterministic uniform fallback on every exceptional record |
| Error | r<=3epsilon, D_N<=3delta/8; code adds<=delta/4 | Final good-event loss<=5delta/8 |
| Budget | k inherited learners, epsilon=delta/(16k ceil(sqrt N)) | C k³ N delta^-2[d²+d log(k/eta)], every record |
| Coherent converse | Label-splitting q=2 floor(k/2)/k>=2/3 | Odd-alphabet erasure correct on subnormalized references |
| Lower conversion | Coarse H, ||H−qF||<=128delta/sqrt N | Clipping uses Weyl plus triangle, not operator-Lipschitzness |
| Confidence | Binary interior converse at error<=384delta/sqrt N | delta<=2^-24 makes inherited cap valid, d=1 included |
| Learned word converse | Some successful word must exist at each target | Fixed decoder image covers entire family, independent of query bound |
| Risk certificate | Choi trace Lipschitz Mk r, index TV Mk r/2 | Both moving-radius buffer and fixed-event probability buffer |
| Finite controls | Inherited actual-control binary theorem for learning | Generic ideal certificate adds a separately certified implementation error |

## Executed finite scope

`finite_outcome_check.py` checks exact rational identities on noncommuting d=2,k=3 tuples, exact normalization after rounding, even and odd alphabet embeddings, full conditional readout completeness, singular PSD/equality behavior through the inherited kernel, and certificate mutation controls. It also reconstructs a complete scalar k=3 grid of denominator 192: 4225 candidates after exact diagonal pruning and 3169 legal points. All nine length-two classical strings are checked. The largest grid failure is exactly 8225/36864, below 1/4; the proved transfer gives radius 7/24 and failure at most 3/8 on the real scalar family.

There are 88 positive checks and 11 negative controls. Ordinary and optimized outputs must be identical. A candidate cutoff, omitted string, extra alleged grid, negative/incomplete readout, illegal centre, noncanonical rational and false risk allowance are rejected. General matrix-grid certificates and the general optimal quantum learner are not represented as executed. The exact scalar example instantiates the certificate theorem, not the tiny-accuracy minimax construction.

## Dependency credit

Binary finite-use Bernoulli geometry is `lem:bernoulliproduct75`. Joint binary interior confidence is `cor:operatorconfidence80`, whose proof restricts to the binary interior. The finite, actual-control common learner is `thm:rationallearner81`; its one-use upper primitive is explicitly credited to Mele–Bittel. No new theorem assumes that an arbitrary learning POVM is efficiently synthesizable. The horizontal construction uses a standard purification/cancellation method with the new normalized tuple lift. Affine volume packing and greedy nets are standard tools, not priority claims by themselves.
