# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — Hamilton–Boltzmann Cotangents and Prepared Fluctuation Fields  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `438faf32ace9fc68e5375d4cf7b60fc4b570b65d`

## Executive assessment

The paper now separates local analytic sources from the global convex dual, centers fluctuation fields at exact finite-volume means, and writes the missing second derivative of the nonlinear reference measure \(A_f\). These are genuine improvements.

The new quadratic form is not generally coercive—and may be indefinite. The claimed closed-range observability estimate is simply asserted, so the Lax–Milgram covariance construction has no valid foundation. The process theorem also relies on cumulant bounds and the B2 measure–trace machinery that have not been proved.

## Major mathematical objections

### 1. The exact second variation is not a positive tangent action

For the perspective entropy

\[
\Phi(g,a)=g\log(g/a)-g+a
\]

at \(g=qa\), the manuscript correctly obtains, along affine \(\Gamma_s\) and nonlinear \(A_{f_s}\),

\[
\frac{(\dot\Gamma-qDA_f[\dot f])^2}{qA_f}
+(1-q)D^2A_f[\dot f,\dot f].
\]

The second term has no fixed sign. For \(q>1\), directions with small or zero contact residual can make it negative. In the scalar model \(A_f=f^2\), taking

\[
\dot\Gamma=q\,DA_f[\dot f]=2qf\dot f
\]

makes the square term vanish and leaves

\[
2(1-q)(\dot f)^2<0.
\]

The same local algebra is present in the hard-sphere bilinear reference \(A_f\). Linearized balance and an initial entropy term may control some directions on a sufficiently short interval, but they do not make the contact Hessian intrinsically positive on every regular biased phase and every fixed horizon. Splitting a horizon into blocks does not change the sign of the total second variation or recreate an initial entropy penalty at every block.

Therefore Lemma r7-b3-coercive is not a consequence of the displayed Hessian and is false without substantial restrictions on \(q\), the horizon, and the tangent class.

### 2. The advertised energy estimate is the missing theorem

The proof says that a “linearized balance energy estimate” controls the transport norm by the initial term and the square contact residual. No norm \(\mathsf X_T\), boundary condition, collision operator domain, or estimate is derived. For a biased time-dependent Boltzmann flow this is a nontrivial well-posedness and observability theorem.

The claimed absorption of the indefinite \(D^2A_f\) term depends entirely on that estimate. Naming it does not prove coercivity.

### 3. Closed range and gauge completeness are asserted rather than established

Theorem r7-b3-range is load bearing: it must identify the annihilator of all balanced tangents with the exact gauge and prove no additional zero-variance classes exist. Its proof consists of “solve the backward adjoint equation” and an observability inequality which is neither formulated with boundary data nor derived.

For transport with collision boundary measures, closed range depends on:

- the precise Hilbert and negative Sobolev spaces;
- endpoint and conservation constraints;
- trace regularity at grazing and velocity infinity;
- solvability and estimates for the backward kinetic equation; and
- compatibility with the nonlinear phase \(qA_f\).

None is supplied. The Hilbert closed-range theorem cannot be invoked until the model-specific observability estimate has actually been proved.

### 4. Lax–Milgram cannot be applied to an indefinite or undefined form

The covariance equation

\[
\mathfrak q_{f,q}(u_\xi,v)=\langle\xi,v\rangle
\]

requires a continuous coercive bilinear form on a completed balanced Hilbert space. Because the coercivity lemma is unsupported and the tangent completion is defined through that same lemma, the construction is circular.

Even if a positive quadratic action were available, identifying its inverse with the pressure Hessian requires twice differentiable local convex duality and a proved unique linearized minimizer. Those conclusions are not obtained by differentiating the formal B2 variational formula.

### 5. The two-interval cumulant estimate is not derived from one marked time

The statement that every connected block meeting adjacent intervals \(I,J\) carries a factor \(|I||J|\) ignores contact-time singularities and correlations crossing the common endpoint. A connected cumulant density may be integrable in one anchor time and depend on relative times; its integral over \(I\times J\) is not automatically a product bound. Endpoint atoms are not the only possible near-diagonal contribution.

The required \(L^1\) cumulant-density theorem is itself imported from the unproved B2 measure–trace renewal. The fractional Sobolev and Mitoma tightness conclusions therefore have no established estimate behind them.

### 6. The global dual theorem still lacks a complete pressure domain

Compactly supported bounded tests do detect Radon measures and singular currents. But the displayed equality with the full dynamic action also requires the limiting pressure on every such source, lower semicontinuity under increasing supports, and a proof that balance is closed in the chosen weighted topology. These are precisely the missing B2/B3 interfaces, not consequences of pointwise scalar conjugacy.

## Dependency assessment

B3 remains conditional on B2-GC and B1. It cannot supply a covariance kernel, Gaussian process, or cotangent rigidity theorem to B4, C1/C2, or D1. The exact-centering correction is valuable but does not repair the absent fluctuation theorem.

## Required reconstruction

Restrict first to a phase/horizon on which the exact second variation is demonstrably positive, or formulate the fluctuation covariance directly from finite-volume cumulants without interpreting an indefinite action Hessian as a metric. Prove the backward kinetic observability/closed-range theorem in explicit spaces, and establish localized cumulant estimates independently of point stopping states.

## Recommendation

**Reject.** The manuscript writes the correct nonlinear second-variation term but then assumes it is coercive. The closed-range and Gaussian-process results are unproved and remain dependent on an open B2 theorem.
