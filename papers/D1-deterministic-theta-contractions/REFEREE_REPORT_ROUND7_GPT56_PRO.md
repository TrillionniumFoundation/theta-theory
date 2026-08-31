# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — Deterministic Theta Contractions  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `751352215912c52f53aef6994eb9961c8500e98a`

## Executive assessment

The paper abandons the impossible requirements of one entire complex logarithm and gradient blow-up for bounded observables. It also retains phase coexistence and now centers every local likelihood at the exact finite-volume mean. These are correct repairs.

The replacement abstract theorem still does not follow from its hypotheses. A uniform zero-free complex tube is incompatible with genuine coexistence, the conjugate of a maximum of phase pressures is not the pointwise minimum of their conjugates, and local analytic charts do not yield boundary-face lower bounds or a full finite-dimensional LDP. The paper remains a synthesis of desired consequences rather than an independent theorem and should not survive as a standalone submission.

## Major mathematical objections

### 1. Uniform zero-free tubes are incompatible with phase coexistence

The paper assumes that every compact real source set, including coexistence points, is covered by complex tubes of fixed positive width on which the finite-volume moment generating function is nonzero and admits a logarithm converging locally uniformly.

At a first-order coexistence point the finite-volume partition function has the form, schematically,

\[
Z_\mu(\theta)
\approx e^{\mu Q_1(\theta)}+e^{\mu Q_2(\theta)}.
\]

Where \(Q_1=Q_2\) on the real axis, complex zeros occur when

\[
\mu(Q_1-Q_2)\approx (2k+1)\pi i,
\]

so the zeros approach the real coexistence set at distance \(O(\mu^{-1})\). This is the standard mechanism behind Lee–Yang pinching and is already visible in a two-term finite sum.

Therefore no \(arepsilon\)-independent zero-free tube can cover a genuine coexistence point while the limiting pressure is the nondifferentiable maximum of two phases. The local atlas assumption and the coexistence conclusion are mutually incompatible.

### 2. Phase pressures are not logarithm branches of one nonvanishing finite MGF

On an overlap, two branches of the logarithm of the same nonzero analytic function do differ by \(2\pi i k\). But the analytic functions \(Q_{m,j}\) used later are phase pressures whose maximum gives the physical pressure. They are not merely different logarithm branches of the same finite-volume moment generating function. A finite MGF has one real logarithm; phase decomposition requires spectral projectors, restricted partition functions, or metastable boundary conditions.

No microscopic phase-specific measures or analytic restricted partition functions are defined. Lemma r7-d1-atlas therefore conflates logarithm branches with competing phases.

### 3. The conjugate of a maximum is not the minimum of the conjugates

The theorem defines

\[
Q_m=\max_j Q_{m,j}
\]

and claims the finite-dimensional rate is

\[
I_m(x)=\min_j I_{m,j}(x),
\qquad I_{m,j}=Q_{m,j}^*.
\]

In general,

\[
(\max_j Q_{m,j})^*
e \min_j Q_{m,j}^*.
\]

The conjugate of the maximum is a closed convex object related to the convex hull/infimal mixing of the phase conjugates, whereas a pointwise minimum of convex functions can be nonconvex. A mixture of genuinely distinct microscopic phase families can have rate \(\min_j I_j\), but that requires an independently proved phase decomposition and phase-wise lower recovery. It is not a consequence of the pressure envelope.

The proof inserts exactly that missing result as “choose the phase-specific microscopic recovery supplied by the platform theorem.” The abstract D1 theorem has therefore assumed its main lower-bound input.

### 4. Local analytic charts do not prove boundary-face lower bounds

Sending a normal source \(rn_F\) to infinity is a second limiting problem. The zero-free atlas only controls compact real source sets; it gives no estimates uniform as \(r	o\infty\), no order of the limits \(r\) and \(\mu_arepsilon\), and no conditional LDP inside the exposed face.

Straszewicz's theorem approximates extreme points of a compact convex set by exposed points. It does not provide microscopic recovery probabilities, tangential pressure limits, or lower bounds at arbitrary points of a nonconvex phase rate. Iterating over a “flag of faces” is not a proof of a finite-dimensional LDP.

### 5. The finite-dimensional upper bound is not obtained from a finite cover of local charts

A large-deviation upper bound is a global statement about all exponential linear sources. A finite cover of each compact source set gives only local Laplace information. To identify the complete rate and control tails near the support boundary, one needs either the full real cumulant generating function, exponential tightness plus a separating exhaustion, or a direct compact-support argument. The theorem assumes these conclusions in its face stratification.

### 6. The topology-upgrade lower-bound argument is incomplete

Agreement of the projective and target topologies on compact rate sublevels can support an upper-bound upgrade. For the lower bound, one needs an exponentially good localization near the point and a projective neighborhood whose intersection with the compact set lies in the target-open set, while controlling probability outside the compact from below. Exponential tightness gives upper bounds on complements, not a lower bound preventing all mass from lying there under a tilted/recovery law. Additional recovery compactness is required.

### 7. Thin-shell conditioning still depends entirely on invalid upstream coefficients

The conditional theorem cites B1 for hard spheres and A2 for Sinai paths. Both coefficient theorems remain unproved. Moreover, the finite-source coefficient must be uniform across active phase charts and at coexistence; no such theorem is supplied by the abstract assumptions.

### 8. The independent mathematical contribution is insufficient

The exact finite-centred likelihood calculation is correct, but it is a standard exponential-family identity. The contraction, conditioning, and dynamic-programming statements are standard once full platform LDPs and coefficient theorems exist. D1 supplies no proof capable of closing those upstream results.

## Required reconstruction

Remove the coexistence points from any uniform zero-free atlas and formulate phase-specific finite-volume objects explicitly. Prove finite-dimensional LDPs platform by platform, including boundary and coexistence recovery, before projective passage. Do not infer a minimum-of-phase rate from a maximum pressure without a microscopic mixture theorem. The surviving exact-likelihood and commutation observations should be folded into the principal platform papers.

## Recommendation

**Reject; remove as a standalone submission.** The revised local likelihood is correct, but the advertised stratified projective LDP assumes phase-wise lower recovery and makes incompatible zero-free/coexistence assumptions. It remains a conditional synthesis, not an independent top-four theorem.
