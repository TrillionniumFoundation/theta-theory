# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — *History, Memory, and Universal Pressure for Prepared Sinai Paths*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `f2ab3477daa06b082f07f20d143258c5b4e440f3`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/A4_HISTORY_DOOB_MEMORY_AREA.tex`, blob `0641c934761485a416f413108930321da27c21b8`

## Source-control verdict

The active A4 manuscript is unchanged from round four. Its exponential-memory theorem still assumes the decisive meromorphic decomposition, and its rough limit omits the generally nonzero antisymmetric area correction. The proposed round-five packet is not materialized because the branch workflow failed before copying any candidate into the paper.

The candidate makes two genuine corrections: it uses a true eigenfunction Doob transform for the nonlinear tower, and it includes an area anomaly in the rough limit. Those improvements do not close the history, memory-decay, or homogenization theorems.

## Audit of the proposed round-five replacement

### 1. The claimed orthogonality of the forcing is algebraically false

For `B in D(L)`, the candidate defines

\[
\eta_B(t)=x_B'(t)-Ax_B(t)-(K*x_B)(t),
\qquad x_B(t)=PU_tB,
\]

with `A=PLP` on the resolved range. At time zero,

\[
\eta_B(0)=PLB-PLPB=PLQB.
\]

This vector lies in the resolved space `V` because of the leading projection `P`; it is not generally orthogonal to `V`. The theorem explicitly states that the forcing is orthogonal to `V` at time zero, which is therefore false except under an additional condition `PLQB=0`.

The Volterra identity itself can be defined by this residual, but the claimed Mori–Zwanzig interpretation and orthogonality property must be corrected.

### 2. Positive asymptotic covariance does not exclude complex zeros of the compressed resolvent

The memory-decay proof asserts that a zero of

\[
\det \widehat C(z),\qquad
\widehat C(z)=P(z-L)^{-1}P,
\]

in a left half-strip would force zero spectral density and hence zero asymptotic variance. This implication is false. A matrix Laplace transform of correlations can have complex zeros away from the imaginary origin even when every nonzero resolved direction has strictly positive Green–Kubo variance.

Covariance positivity controls the quadratic behavior at frequency zero. It does not imply minimum-phase or zero-free transfer behavior throughout a complex strip. Without a separate coercivity/passivity theorem, `C-hat^{-1}` can have poles and the compressed memory transform need not be analytic in the claimed strip. The asserted exponential decay of `K` therefore does not follow.

### 3. The measured Ray construction does not establish the stated global semigroup

The candidate starts with regular conditional kernels defined only for `nu`-almost every history, completes one null set by a cemetery value, and then claims a positive semigroup on the entire Ray completion. A coherent version must verify Chapman–Kolmogorov identities on one common exceptional set for all rational times, extension to all times, and compatibility of the evaluation closure with those kernels.

The proof that resolvent functions become continuous by construction is not enough to show that every `P_t` preserves the uniform/strict closure or that the resulting process has the same completed sigma-field. These are substantive right-process/Ray compactification theorems and require precise hypotheses.

### 4. The history eigenfunction is not constructed from the displayed product

The infinite backward product defining `h_Psi` contains an undefined normalization `c_Psi` and conditional `g`-functions depending on finite histories. The paper does not prove that the product is independent of the chosen coding representatives at graph-completed singular histories, or that it intertwines the physical-time Feynman–Kac semigroup rather than only the discrete return operator.

Summable variations can control a normalized `g`-function product, but the exact formula, normalization, roof conversion, and two-sided bounds must be derived. The claimed history eigenfunction cannot be treated as automatic from the A2 transfer eigenvector.

### 5. The model-specific memory decay remains entirely dependent on A2

Even apart from the zero-free error, the proof imports meromorphic continuation and high-frequency bounds from A2 for every matrix element, plus enough differentiability to integrate by parts repeatedly. A2 has not established its all-depth bundle or Dolgopyat theorem. Thus A4 cannot serve as an independent closure of the memory interface.

### 6. The area-corrected rough theorem is still only a sketch

The candidate now includes the antisymmetric drift

\[
\Gamma=\frac12\int_0^\infty
\bigl[\operatorname{Cov}(G,G\circ\Theta_t)
-\operatorname{Cov}(G\circ\Theta_t,G)\bigr]dt,
\]

which is the correct phenomenon to retain. But a martingale–coboundary decomposition for a continuous-time billiard suspension does not automatically give convergence of the canonical second level in every `p`-variation topology. One needs explicit moment bounds, control of roof interpolation, identification of the area convention, and a proof that the limiting bracket drift has the displayed normalization.

### 7. The coupled slow-memory limit is not justified by pointwise kernel decay alone

Passing a rapidly rescaled convolution to its instantaneous mass in a stochastic rough system requires uniform control of the resolved process modulus, compatibility with the finite auxiliary realization, and joint convergence of forcing and memory coordinates. The candidate states these conclusions but gives no full stability theorem.

### 8. The nonlinear Doob tower is correct only on a proved eigenfunction domain

The algebraic identity

\[
\mathcal E_tF=\theta^{-1}\log\widetilde P_t(e^{\theta F})
\]

has the exact tower when `P-tilde` is a Markov semigroup. This is a real improvement over the active paper. Its application remains conditional on the unproved history eigenfunction and Feller construction above.

## Required reconstruction

The authors should separate the unconditional finite-dimensional Volterra theorem from model-specific decay. They must correct the forcing statement, prove a genuine Ray/right-process realization, construct the physical history eigenfunction, and replace the invalid zero-free argument by an actual transfer-function theorem or allow auxiliary modes for all zeros. The rough limit needs a standalone enhanced invariance principle with a fixed area convention.

## Recommendation

**Reject.** The active manuscript remains uncorrected. The candidate repairs the nonlinear normalization and acknowledges the area anomaly, but contains a false orthogonality assertion and an invalid inference from covariance positivity to a zero-free compressed resolvent. The model-specific history and memory theorems are not proved.