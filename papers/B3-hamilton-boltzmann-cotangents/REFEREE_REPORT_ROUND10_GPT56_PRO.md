# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** B3 — Hamilton–Boltzmann Cotangents  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `4fe0790e46710a9fc83c67cbbb1d1ee96f5737476ee76489fd9d38c98264548c`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The revision correctly abandons the false claim that the raw perspective Hessian is automatically positive and no longer attributes nonlinear curvature to the linear balance multiplier. It also starts from exact finite-volume covariance and uses exact finite-volume centering.

The new short-time coercivity and Gaussian geometry are nevertheless unsupported. A uniform spectral gap is assumed for a biased, generally non-equilibrium collision operator; the asserted nullspace identification omits possible dynamic coboundaries; and the infinite-dimensional covariance inverse is written on the wrong domain. Finite-dimensional cumulant convergence does not prove the Mosco limit or process tightness claimed here. The paper still depends entirely on B2's unproved marked expansion.

## Major mathematical objections

### 1. The biased collision spectral gap is an unproved main theorem

The proof assumes

\[
-\langle h,L_{f,q}^{\rm sym}h\rangle
\ge c\|h\|_\nu^2
\]

uniformly on a compact chart of exposed paths. For a Maxwellian equilibrium and the usual linearized Boltzmann operator, a coercive gap modulo the five collision invariants is classical in suitable weighted spaces. Here \(f=f(t,x,v)\) is an inhomogeneous, generally non-equilibrium path and \(q\) is a source-dependent collision-rate ratio. The weight \(u/f\) need not symmetrize the driven collision operator, and its symmetric part need not have the same kernel or sign.

The phrase “regular biased phase chart” does not prove detailed balance, uniform lower Maxwellian bounds, or a spectral gap. This is the principal analytic theorem required for the entire section.

### 2. The macroscopic component is not a finite-dimensional transport system

Integrating against \(1,v,|v|^2\) produces local mass, momentum, and energy fields depending on \((t,x)\). They solve an infinite-dimensional hyperbolic system coupled to higher moments, not a finite system of five scalar coefficients. The manuscript's micro–macro argument therefore does not close the spatial transport modes.

The norm includes only a negative Sobolev time integral for \(u\), while the claimed estimate controls a strong weighted \(L^2\) supremum. A genuine hypocoercive estimate with spatial Fourier modes, boundary traces, and source forcing is required.

### 3. The short-time coercivity conclusion depends on unverified boundedness assumptions

The absorption estimate

\[
\left|\int(1-q)D^2A_f[u,u]\right|
\le CT\|q-1\|_{\infty,w}\|u\|_{\mathsf X_T}^2
\]

requires \(q-1\) to be bounded in a weight compatible with the collision kernel and the exponential source class. No such bound is part of the theorem statement. For the Hamiltonian tilt \(q=e^{\Delta p+\psi}\), even moderate growth of \(p\) can make this norm infinite.

Moreover, the positive initial entropy cannot absorb the negative dynamic curvature unless the preceding well-posedness estimate is already valid with uniform constants. Thus the corollary is not an independent proof of positivity.

### 4. The exact gauge statement ignores endpoint and transport terms

The identity \(\ker\mathfrak D=\operatorname{Ran}\mathfrak G\) is algebraically tautological for \(\mathfrak D(p,\psi)=\Delta p+\psi\). It does not prove that every pair \((r,-\Delta r)\) annihilates the full balanced tangent pairing. Integration by parts in the weak balance produces initial, terminal, and transport terms unless \(r\) satisfies explicit endpoint/generator conditions.

“Endpoint normalization” is not a definition of the admissible gauge domain. The quotient can be larger or smaller than the annihilator actually seen by the path action.

### 5. Zero asymptotic variance is not identified by the balance gauge alone

A path observable can have zero asymptotic variance because it is a temporal coboundary for the driven dynamics. Such a coboundary need not be a collision-invariant direction or a representation gauge \((r,-\Delta r)\). The proof says that vanishing covariance against local tilts, together with a balance observability theorem, identifies the class. Balance observability is a deterministic constraint statement; it is not a Livšic/coboundary theorem for the stochastic or deterministic time evolution.

Therefore the claimed exact nullspace of \(\Sigma\) is not established.

### 6. The covariance inverse is written on the wrong infinite-dimensional domain

The manuscript states

\[
d_e^2I(z)=\langle z,\Sigma^\dagger z\rangle
\quad\text{for }z\in\overline{\operatorname{Ran}\Sigma}.
\]

For a positive covariance operator with eigenvalues tending to zero, the quadratic form domain of the inverse is \(\operatorname{Ran}\Sigma^{1/2}\), not the whole closure of \(\operatorname{Ran}\Sigma\). For example, on \(\ell^2\) let

\[
\Sigma e_n=n^{-2}e_n.
\]

Its range is dense, but the vector \(z=(1/n)_n\) lies in \(\ell^2=\overline{\operatorname{Ran}\Sigma}\) while

\[
\sum_n \frac{|z_n|^2}{n^{-2}}=\sum_n1=\infty.
\]

The Moore–Penrose inverse is not a bounded operator on the declared set. The second epi-derivative must be formulated as a closed extended quadratic form with its correct Cameron–Martin domain.

### 7. Finite projections do not automatically produce the claimed Mosco limit

Analytic convex duality on each finite projection gives a finite-dimensional Hessian relation. Passing to an infinite projective state requires tightness of the quadratic forms, consistency of the embeddings, control of the nullspaces, and recovery in the strong tangent topology. The statement that the projected forms are “monotone” is not proved and is not automatic for Schur complements under changing projections.

Identifying the resulting form with the closure of the raw action second variation is precisely the hard theorem; it is asserted after differentiating a formal action.

### 8. The process cumulant estimate is not supplied by a short-time cluster expansion

The localized tree-decay lemma requires a uniform connected-correlation density in deterministic time, including contact diagonals and all spatial/velocity tests. B2 proves no such theorem. Conservation and transport modes can produce long correlations; a short fixed time interval does not create an exponential temporal mixing estimate merely because graph genealogies are connected.

Without the fourth-moment estimate, Mitoma/Aldous tightness and the process-level Gaussian limit do not follow from finite-dimensional cumulants.

## Dependency and editorial assessment

B3 depends on B1 and especially B2, whose shell and first-surplus theorems remain open. It cannot serve as a certified covariance, cotangent, or Gaussian-process interface for B4, C1, C2, or D1.

A viable future paper should first prove a precise fluctuation theorem for the established microscopic model. Only then should it identify the closed inverse-covariance form and compare it with a rigorously derived second variation.

## Recommendation

**Reject.** The revision removes one false curvature argument but replaces it with an unproved non-equilibrium spectral gap and an incorrectly typed infinite-dimensional inverse. The Gaussian process theorem remains formal.
