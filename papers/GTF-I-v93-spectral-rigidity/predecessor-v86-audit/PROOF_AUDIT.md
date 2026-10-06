# Author-side proof and resource audit — Revision 86

The written arguments below are mathematical proofs, not inferences from finite tests. This audit is not an independent specialist priority opinion or a proof-assistant certificate. It records the new finite-neighborhood proof and its exact relation to the preserved v85 development.

## 1. Channel norm without a state-optimization shortcut

For any Hermitian tuple R, the adjoint of the amplified classical-output map sends a block test to `sum R_j tensor Y_j`. The operator norm is at most `sum ||R_j||op`. Duality proves the diamond bound on arbitrary trace-class inputs, including nonpositive ones, and on every reference dimension. Channel differences and derivatives have zero tuple sum, so they are trace annihilating and Hermiticity preserving. No optimization-over-states assumption is required. The insertions in Sections 73–74 repeat the old curvature definition `L=sup_{|u|<=a0}sum_j||E_j''(u)||op` and refer to this explicit proof.

## 2. Exact one-sided tangent cone

Right positivity forces J_j=Q_jH_jQ_j>=0. Conversely `(E_j+sH_j+c s^2 I)/(1+kc s^2)` realizes every such zero-sum Hermitian direction for small s>=0. The support block remains above lambda_j/2; the Schur complement is bounded below by `sJ_j+s^2(c-2||H_j||^2/lambda_j)Q_j`. Choosing c larger than every displayed coefficient handles singular J and cross terms into its kernel. Zero effects require H_j>=0 and are handled directly. This is an exact analytic curve, not independent entry rounding or a formal tangent ansatz.

The intersection of this cone with its negative is exactly all J_j=0. Full covariance-range membership for an arbitrary zero-sum Hermitian direction requires both this vanishing and Gamma in W_E. The independent missing-support variables in the retained complete kernel force each J_j=0; after their elimination the exact remaining pairing is `-2tr(A Gamma)`. This checks the sign, factor two and real Hermitian spaces against the old unitary specialization.

## 3. A normalized factor with a finite remainder

For A* A=I and T_A B=H, zero tuple sum gives A*B+B*A=0. The inverse root of I+s^2 B*B is analytic. With b=||B||op, h=max||H_j||op, the ordered expansion gives `||G(s)-E-sH||Sigma<=k b^2(2+h)s^2` for s<=1. It never commutes E_j or H_j through the inverse root. For sb<=1 the stacked-factor displacement is at most 3bs/2. Duplicating the classical label into a discarded dilation environment is an isometric embedding of this stack and preserves its operator norm.

When B is horizontal, A*B=0 and the retained normalized derivative identities give W*W'=0. Distinct differentiated slots of every common adaptive tester are orthogonal, so the finite path upper is `2b sqrt(N)s`. Padding stopped branches with discarded dummy calls makes the original stopped output a common postprocessing. No environment is made accessible.

## 4. Uniformity over a fixed quadratic tangent neighborhood

The new hypothesis is finite: `||F-E-sH||Sigma<=Lambda s^2`, with E,H,Lambda fixed and H nonzero. There need not be a curve. It yields the channel hybrid `N(||H||Sigma s+Lambda s^2)` and a fixed-eigenvector Bernoulli gap at least hs/2 for sufficiently small s. The latter witness is the same throughout the neighborhood.

In the covariance range, the horizontal solution has a fixed finite b. Comparing F with its normalized factor surrogate gives `2b sqrt(N)s+(Lambda+K_b)Ns^2`. Put x=sqrt(N)s; for x<=1 its square is at most x, and for x>=1 cap at two. This proves a finite upper uniformly over all allowed remainders and N, rather than dropping the quadratic error.

No constants are asserted uniform over E,H,Lambda. Neighborhoods for a prescribed very small Lambda may be empty; the theorem is a universal statement for every legal pair satisfying its hypothesis. The cone realization itself supplies a nonempty neighborhood with a sufficiently large fixed remainder bound.

## 5. Two different linear lower mechanisms

If J_j>=0 is nonzero, choose v in Q_j with positive rate lambda. Label j is impossible under E and has probability at least lambda s/2 under every allowed F. The repeated-input event gives the exact lower `2[1-(1-lambda s/2)^N]`, hence a linear truncated scale. It requires no logical code, recovery or collective quantum readout. It proves the same product and adaptive order.

If all J_j=0 but Gamma is outside W_E, apply the complete actual-label/reference code to Gamma. The old normalized first-order realization proves algebraically that the corrected derivative D_H is `-i[Gamma_L,.]`. Its applicability here follows from the first jet, not differentiability of F or canonical roots. The finite pair remainder supplies the bound Lambda s^2 directly. Comparing with the logical exponential supplies `kappa=Lambda+2||Gamma||op^2` (not a curvature inferred from a first jet).

With Z=Gamma−Pi_W Gamma and Delta=||Z||HS^2/tr Z_+>0, the m-cycle lower is `2|sin(msDelta/2)|−m kappa s^2`. For `s<=min(1,1/(2Delta),Delta/(2pi kappa))`, take `m=min(N,floor(1/(sDelta)))`. The floor before the minimum is at least two; x=msDelta is at least half of min(1,NsDelta) and at most one. The sine lower and finite quadratic loss leave at least min(1,NsDelta)/(2pi). The recovery is a complete CPTP channel on the actual label and retained reference, with at most 2d reference dimension per call. It remains ideal, known-pair control, not a common learner.

## 6. Independent-product acquisition converse

The product model has arbitrary different probe–reference states, no entanglement between pairs and no feedback into future inputs. It permits arbitrary joint processing after all calls. This is not the class of all entangled parallel queries or every feedback protocol.

When every J_j=0, the canonical (not necessarily horizontal) first-order B exists. Its normalized-factor dilation gives a one-copy Bures displacement at most 3bs/2 uniformly in the input and reference. The finite F-to-surrogate error gives another Bures displacement at most sqrt(Lambda+K_b)s. Uhlmann purification gives the Bures triangle inequality, hence root fidelity at least 1−a^2s^2/2. Tensor multiplicativity and the unhalved fidelity–trace inequality give product trace separation at most 2a sqrt(N)s. A joint readout contracts trace norm; convexity allows public randomness with its retained record. The same repeated-label Bernoulli witness gives the lower. In the opening branch the impossible event and ordinary hybrid give both product bounds.

These standard fidelity facts are explicitly credited to Watrous, Proposition 3.16 and Theorems 3.22 and 3.33, not claimed as new. The adaptive column uses the finite-neighborhood theorem and therefore proves the three mechanisms with identical base/direction/remainder scope.

## 7. Higher-order and multiscale checks

The higher-order corollary assumes the actual bound `||F(t)-E-t^qH||Sigma<=Lambda t^(2q)` with H nonzero; positivity forces H into the one-sided cone. Direct substitution s=t^q is all that is used. This does not differentiate an inverse reparametrization. It applies to reparametrized C2 curves and suitable C^(2q) curves with absent intermediate coefficients, not arbitrary zero jets.

For the scalar family `((1-t^b)(1/2+t^a),(1-t^b)(1/2-t^a),t^b)`, the full product law is the maximal experiment even with adaptive controls and stopping, since the input has dimension one. The third-label event gives the Nt^b lower; sending that label to a fair bit gives the sqrt(N)t^a lower. Conditional on no third label the record is Bernoulli, giving the matching sum upper. The bounds are absolute for 1<=a<b<2a and t<=1/4. This example proves an additional mixed-rate law and explains why the O(t^(2q)) condition cannot be inferred merely from the leading coefficient.

## 8. Controls and exact represented input

The finite-neighborhood control corollary substitutes the finite pair kappa into the retained deterministic error ledger. It charges preparation and readout under both hypotheses, and every cycle's uniform diamond error twice. The sufficient budgets still tend to zero with sDelta; fixed nonzero control error is not claimed harmless as s tends to zero.

The exact cone program checks PSD of every missing block, real support-span rank and the Hilbert–Schmidt Gram projection. Supplied pair allowances are tested through `lambda_j s^2 I ± (F_j-E_j-sH_j)>=0` with sum lambda_j<=Lambda. A nonzero PSD J has a positive diagonal entry; Qe_r and its rational squared norm give the exact witness. No spectral floating tolerance is used. Positive support square roots used by the existence proof are not computed by the certificate.

A supplied pair certificate does not certify a whole curve or the small interval. A first jet does not compute curvature, recovery, a tester or distance. Zero input tangent remains `higher_order_undetermined`. Resource caps reject rather than return partial results. Replay compares canonical JSON so a Boolean replacing an integer is not accepted as numerically equal.

## 9. Executed finite scope and preservation

The new suite has 353 positive checks and 27 negative controls, including 56 complete finite classical laws and 8 comparisons with the full exact covariance range. It covers noncommuting directions, singular opening cross blocks, polynomial cone realization, old two-sided specialization, independent Choi fidelity identities, mixed scalar rates, pair allowances, normalization, malformed rationals, mismatched dimensions, caps and tampering. All 23 inherited suites execute anew alongside it in ordinary and optimized Python. These finite checks are not continuum proofs or physical execution.

All original proof bytes are preserved. Sections 73 and 74 have registered insertions for curvature and the channel norm; removing those exact strings restores the predecessor section SHA-256. Every other inherited section is byte-identical, and the old proof graphs remain active. The predecessor native inventory contains 565 files; the current graph retains 912 complete labels, 423 quantitative-package labels and 116 structural labels. The structural companion is not a premise. Native source, published artifacts and exact final review head require fresh separate receipts. The independent A/B/C/D flags remain false.
