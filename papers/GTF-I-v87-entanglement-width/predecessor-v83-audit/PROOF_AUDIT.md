# Proof and resource audit — Revision 83

This author-side audit accompanies written proofs, not a formal proof-assistant certificate or an independent specialist opinion. Both controlling R52 reports and every inherited section remain unchanged.

## 1. Closed-body covariance

Work over the real Hilbert space of Hermitian tuples, with `sum_j H_j=0` and inner product `sum tr(H_j K_j)`. `S_E(K)=sum E_j K_j` is generally non-Hermitian. Its adjoint must not be omitted. The zero-sum identity is exact; no coordinatewise independent normalization is used.

Stack `A_j=sqrt(E_j)`, so `A*A=I`. Let `P=I-AA*` and `(T_A B)_j=A_j*B_j+B_j*A_j`. The real adjoint is `T_A* K=(2 A_j K_j)_j`. The identity `C_E=T_A P T_A*/4` proves self-adjointness and positivity. Expanding the squared norm proves the explicit covariance formula. Constants lie in the kernel and the image is zero sum, so restriction to the tangent space is legitimate.

The exact concavity remainder is `t(1-t)||S_F(K)-S_E(K)||HS²`. This is a positive operator-form comparison, not an entrywise inequality. The kernel formula includes singular effects. If the restricted operator is zero, constant-tuple invariance extends this to all Hermitian tuples; choosing a single identity component gives `tr(E_j-E_j²)=0`, hence every effect is a projection. Normalization then forces orthogonality. The converse uses orthogonal ranges. This does not assert that every nonprojective measurement has a positive definite covariance; nontrivial kernels remain possible.

## 2. Exact regularized energy

For `K=(C_E+tau Id)^(-1)H`, the minimizer is `B_j=A_j(K_j-S_E(K))/2`, `R=tau K`. It has `A*B=0`, `T_A B+R=H`, and minimizes `4||B||HS²+tau^-1||R||HS²`. Expanding at the minimizer cancels the linear term for every feasible perturbation. This proof is algebraic and applies at the boundary; it does not invert any effect.

## 3. Adaptive upper bound

Only the first differential argument assumes positive effects. The zero-sum horizontal tangent admits exact local factors via an anti-Hermitian gauge of the positive square root. Its Stinespring representation includes a duplicate label and factor system inaccessible to the tester. The state-independent identity `W* dot W=0` makes different differentiated slots orthogonal, even when the incoming reference-memory states differ. It gives `2 sqrt(N)||B||HS` in unhalved trace norm.

The residual is a channel derivative, not a proposed physical POVM. Duality bounds one reference block by `||R_j||op`; summing over outcomes and slots gives `N sqrt(k)||R||HS`. Cauchy–Schwarz with `tau=1/N` yields the factor `sqrt(k+1)`. Integrate for one fixed tester before taking the supremum. Public stopping is padded with discarded dummy calls; the original stopped record is a common postprocessing.

For singular paths, mix with a uniform tuple, use polynomial covariance continuity and the uniform bound `g<=N||H||HS`, then apply dominated convergence. The ordinary hybrid bound gives convergence of endpoint operational distances. Concavity on the straight segment gives the two integrable factors `(2t)^(-1/2)` and `(2(1-t))^(-1/2)`, whose integrals sum to two. Thus the midpoint upper has no rank, support, or positive-margin assumption.

## 4. Binary restriction and processing

On `(A,I-A)` with direction `(B,-B)`, the first covariance component is `A(I-A)B+BA(I-A)`. Both tuple components contribute equally, giving exactly `Qcal²=2 Q_binary²`; no norm-equivalence constant is substituted. This pins the normalization against the inherited closed binary theorem.

For a column-stochastic output map T, `S_(TE)(L)=S_E(T*L)`. The covariance difference is a weighted sum of matrix Jensen squares. The variational dual unregularized energy therefore contracts. The theorem does not claim that the fixed Euclidean ridge contracts under an arbitrary stochastic map.

## 5. Noise crossover

On the zero-sum tangent space `C_U=Id/k`. Concavity gives `C_(beta E+epsilon U)>=beta C_E+epsilon Id/k`. Inverse order yields the general noisy upper. The matching example is explicitly a rotating rank-one binary projective pair embedded with zero extra effects, then mixed with uniform k-outcome noise. Sending extra labels to a fair bit yields the binary effect `beta P+epsilon I/2`, as an equality on subnormalized reference states.

The binary midpoint variance is scalar and gives `Q_binary²=4N² beta² sin²(theta)/(2+N[1-beta² cos²(theta)])`. The written inequalities compare this with `z=beta N sin(theta)/sqrt(1+N epsilon)`, for `epsilon in [0,1/2]`. The absolute lower is `min(1,z)/16384`, and the upper is `4 sqrt(k(k+1))min(1,z)`. This is sharp at fixed k in noise, horizon and angle, not a growing-k optimality assertion.

## 6. Exact polynomial evaluation

Use a rational Hermitian basis and impose the last tuple component as minus the sum of the others. This is not an orthonormal basis. With Gram matrix G, covariance matrix L and right-hand side b, solve `(L+G/N)x=b`; then `Qcal²=N b^T x`. Omitting G changes the answer and has an explicit negative regression. Gaussian-rational legality, exact residuals and the squared bound are checked without a tolerance. Standard determinant bit bounds and fraction-free elimination give polynomial bit complexity. This computational claim concerns evaluation of a proved upper certificate, not optimization over all testers.

## 7. Guarded affine legalization

Correct the normalization defect by its arithmetic mean, then shift and scale by `(A_j+4a I)/(1+4ka)`. Component error at most a gives corrected error at most 2a. Both spectral inequalities follow exactly, and the target's balanced radius bounds the total repaired error by `4a/(1+4ka)`. Off the good event, full exact spectral tests either accept the legal tuple or return the public uniform tuple. There is no search whose stopping depends on a good event.

At `a=delta/(32k ceil(sqrt(N)))`, the inherited actual-control component procedures, with failure eta/k each, give future-use error delta/4. The existing public code adds delta/4. Every call remains charged and every record respects the old asymptotic budget. No polynomial dictionary or arbitrary quantum readout synthesis is inferred.

## 8. Execution and preservation

The new exact suite has 140 positive checks and 17 negative controls. Its d=2,k=3 case is noncommuting. It also tests projective degeneracy, a nonprojective singular family, all binary normalizations, outcome permutations, rational unitary conjugation, stochastic output processing, scalar product-law inequalities, balanced affine face cases and fallbacks. Certificate replay rejects malformed rationals, illegal effects, wrong dimensions, changed solutions/bounds, and insufficient resource caps.

The complete scalar ternary finite-risk replay from v82 is rerun unchanged. The 20 prior suites remain active and execute anew. No finite suite establishes the universal path theorem, minimax lower bound, asymptotic covering law, priority, or a general device implementation.

`V82_BASELINE.json` pins all 465 prior native files and all three active label graphs. All prior mathematical section files remain byte-identical and active. Only entry documents, audits, status/manifests and build wrappers change, with their exact originals retained. The quantitative article reorders its proof graph rather than deleting material. Exact-source and exact-final-head receipts separately govern publication and reproduction.
