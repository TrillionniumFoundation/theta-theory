# Independent Referee Report — Round 12

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `5a7c62fe0f336224ce17efb37ec913d891b70053506d49d5d74842cf8b739282`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 correctly places the Cameron–Martin form on \(\operatorname{Ran}\Sigma^{1/2}\), restores the microscopic diagonal term in fourth moments, avoids fictitious KKT curvature, and restricts the collision gap to a perturbative Maxwellian chart. These are real improvements.

The new covariance theorem is nevertheless not a theorem for the joint density/contact field it advertises. The displayed martingale problem and bracket contain only density tests through \(\Delta\phi\). A pure contact test then has zero variance, whereas B2's Poisson contact mechanism gives a strictly positive contact-contact covariance. The correct local noise coefficient for a dual pair \((p,\psi)\) is \(\Delta p+\psi\). This typing error invalidates the claimed kernel, quotient, second epi-derivative, and process limit. The stopping-time tightness and hypocoercive/domain interfaces also remain unproved.

## Decisive objections

### 1. The displayed Gaussian noise omits the contact coordinate

The microscopic object is the joint pair

\[
X^\varepsilon=(\pi^\varepsilon,\Gamma^\varepsilon).
\]

A dual source is therefore a pair \((p,\psi)\), where \(p\) tests the density balance and \(\psi\) tests the actual-contact measure directly. One collision contributes the combined source increment

\[
\Delta p+\psi.
\]

Consequently the local Gaussian bracket must have the form

\[
d\langle M(p,\psi),M(p',\psi')\rangle_t
=
\int q\,(\Delta p+\psi)(\Delta p'+\psi')\,dA_f\,dt.
\]

The manuscript instead writes

\[
d\langle M(\phi),M(\psi)\rangle_t
=
\int q\,\Delta\phi\,\Delta\psi\,dA_f\,dt,
\]

which contains no independent contact test.

Take a pure contact observable with density component \(p=0\) and nonzero contact test \(\psi\). The displayed martingale problem assigns it zero noise and zero variance. The microscopic contact count has Poisson-scale diagonal variance

\[
\int q\psi^2\,dA_f\,dt>0.
\]

This is a direct contradiction.

### 2. The “exact covariance kernel” is therefore the wrong kernel

The theorem identifies zero variance with vanishing projected initial source and vanishing “local collision-noise coefficient.” Because the coefficient has omitted \(\psi\), every pure contact source appears to lie in the kernel. That would quotient out precisely the contact fluctuations the paper is supposed to represent.

The claimed balance/endpoint gauge, the dual quotient, and the statement that the kernel is exact all fail at this first typing step.

### 3. The density martingale problem cannot determine the joint process

The state equation

\[
d\langle u_t,\phi\rangle
=\langle u_t,\mathcal A_{f,q}^*\phi\rangle dt+dM_t(\phi)
\]

describes a density fluctuation. It does not include a contact-fluctuation process or the algebraic relation between contact noise and the density jump. The later assertion that “all density/contact cross-brackets and contact diagonals are included” has no displayed process realizing those coordinates.

A correct theorem needs either an explicit joint Gaussian random measure on collision space or a contact martingale \(N(dt,d\omega)\) from which both density and contact components are obtained.

### 4. The second epi-derivative argument assumes the noise representation it is meant to identify

The proof realizes all finite projections on “the same initial-plus-collision Gaussian noise space,” then uses conditional expectations to obtain Mosco convergence. That common noise realization is exactly the conclusion of Theorem 3.1 and is incorrectly specified there.

Finite-dimensional convergence of Hessians does not by itself produce a common infinite-dimensional Gaussian space, identify its Cameron–Martin range, or prove that the path-action second epi-derivative equals the projective inverse form. Tightness and a closed-range theorem are required before that construction can be used.

### 5. Deterministic interval cumulants do not prove the stated stopping-time estimate

Lemma 5.1 is asserted for every bounded stopping time \(\tau\). The proof invokes localized connected diagrams on deterministic time intervals. An unconditional bound for deterministic intervals does not automatically pass to an interval selected adaptively from the path. Aldous tightness requires a uniform conditional increment estimate or a predictable compensator bound.

The hard-sphere dynamics is deterministic conditional on the microscopic state; the contact count does not come with a pre-existing Poisson compensator. This interface must be proved from the actual trajectory expansion.

### 6. The perturbative hypocoercive chart is not shown to contain all exposed paths used downstream

The chart requires

\[
cM\le f\le CM,
\qquad
\|f-M\|_{W^{2,\infty}(M^{-1})}
+\|q-1\|_{W^{1,\infty}_w}\le\delta.
\]

B2's small bounded source chart does not automatically imply these pointwise weighted derivative bounds for an exposed nonlinear path. The paper simply states that every regular exposed phase lies in the chart. This is another load-bearing theorem, especially in inhomogeneous space.

### 7. The contact trace is not continuous in the displayed energy norm

The energy estimate controls the microscopic component in a collision norm and the macroscopic fields in \(L^2_tH^{-1}_x\). Boundary traces on hard-sphere collision faces are not continuous under such a bulk norm without an additional transport graph estimate. Referring to B2's measure-valued Green graph does not identify it with this Hilbert tangent space.

The forward and adjoint endpoint/contact pairings used in the kernel proof therefore remain untyped.

### 8. Upstream inputs remain open

B2 has not proved the source-uniform actual-contact LDP or block sewing, and B1's shell coefficient is false as stated. B3 cannot use their normal pressure convergence, prepared covariance, or lower-recovery interfaces as completed inputs.

## Genuine improvements recognized

The following Round 12 changes should be retained:

- perturbative, rather than global, collision-gap claims;
- spatially dependent macroscopic fields;
- exact finite centering;
- the microscopic \(h/\mu_\varepsilon\) fourth-moment term;
- the Cameron–Martin domain \(\operatorname{Ran}\Sigma^{1/2}\); and
- explicit separation of primal form domain and dual covariance kernel.

## Required reconstruction

The paper must start from a correctly typed joint collision-space Gaussian random measure. It should derive density, contact, and cross components from the single coefficient \(\Delta p+\psi\), prove conditional stopping-time estimates from the microscopic expansion, and only then identify the covariance kernel and second epi-derivative. The perturbative chart and trace-domain embeddings also require independent proofs.

## Recommendation

**Reject.** The paper's main Gaussian object omits one of its two advertised coordinates. Pure contact fluctuations are assigned zero variance, so the covariance kernel, cotangent quotient, Cameron–Martin form identification, and process CLT are not established.