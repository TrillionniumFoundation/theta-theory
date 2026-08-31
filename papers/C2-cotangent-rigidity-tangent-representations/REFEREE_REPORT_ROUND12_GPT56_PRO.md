# Independent Referee Report — Round 12

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `3d008e9afbb96c4ad91113da352e52f5eb48a5bbf869a06693111e23b92a782c`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 correctly distinguishes scalar pressure equality from equality of the full perturbation functional, identifies the quotient dual as signed invariant measures rather than probabilities, separates source derivatives from state derivatives, and avoids infinite-path Radon–Nikodym trivializations.

The first theorem nevertheless contains an elementary logical error: if two potentials have equal integrals under every invariant probability, their difference must have zero invariant integral and hence belong to the coboundary closure \(\mathscr N_{\rm inv}\), not to \(\mathbb R1+\mathscr N_{\rm inv}\). The constant function one is an immediate counterexample to the stated equivalence. The common form-domain theorem is also assumed rather than derived: finite correlation Gram matrices cannot identify the full mutually singular \(L^2\) phase spaces or the graph domain of the Doob generator. The optional-projection and hard-sphere rigidity conclusions consequently remain conditional on unavailable upstream theorems.

## Decisive objections

### 1. The invariant-integral equivalence is false as written

The theorem states:

> Two potentials have equal integrals under every invariant probability iff their difference lies in \(\mathbb R1+\mathscr N_{\rm inv}\).

Take

\[
F=0,
\qquad G=1.
\]

Then

\[
F-G=-1\in\mathbb R1+\mathscr N_{\rm inv},
\]

but for every invariant probability \(\mu\),

\[
\int F\,d\mu=0,
\qquad
\int G\,d\mu=1.
\]

The integrals are not equal. The correct statements are:

- equality of all invariant integrals iff \(F-G\in\mathscr N_{\rm inv}\); and
- invariant integrals differ by one common constant iff \(F-G\in\mathbb R1+\mathscr N_{\rm inv}\).

The manuscript conflates these two quotients in the very theorem meant to separate them.

### 2. The proof's separation argument cannot produce the claimed constant quotient

A signed invariant separator annihilates \(\mathscr N_{\rm inv}\). It does not annihilate nonzero constants. Normalizing a positive Jordan component makes this explicit: every invariant probability evaluates \(c1\) as \(c\). Thus the proof supports the corrected zero-integral statement, not the theorem written.

### 3. The hard-sphere pressure-rigidity implication is not proved

Equality of the full perturbation functionals does imply equality of all first derivatives on a common analytic chart. The manuscript then says equality of the “complete mean and covariance functionals” and B3's local-noise representation identify the source difference with the balance/endpoint gauge.

This is insufficient. A covariance kernel is a local quadratic nullspace at one phase. Thermodynamic cohomology is an exact nonlinear identity of additive functionals. Zero local variance does not automatically produce an exact finite-time balance coboundary unless a closed-range representation theorem is proved on the full source space. Round 12 B3 does not prove such a theorem for the joint contact coordinate and, in fact, omits pure contact tests from its Gaussian bracket.

### 4. A finite correlation Gram operator cannot identify the full phase Hilbert spaces

The paper lets

\[
\mathcal H_\eta=L^2(\widehat\pi_\eta)
\]

and says the inner products are pulled to one reference Hilbert space by the positive square root of a correlation Gram operator. A finite Gram matrix for a selected resolved family identifies only that finite-dimensional span. It does not define a unitary or bounded isomorphism between the full \(L^2\) spaces.

Distinct ergodic Gibbs/path measures may be mutually singular. Without a common transfer representation or an explicitly constructed measurable Hilbert bundle, there is no canonical map on which the full Doob generator form can be pulled back.

### 5. The type-(B) common-domain theorem is an assumption, not a consequence

A2/A4 response bounds on fresh anisotropic strong levels do not imply that the closed sectorial forms of the continuous-time Doob generators share one common Gelfand domain \(\mathcal V\). Domain stability is precisely the hard operator-theoretic question. The proof simply says the correlation pullbacks “define bounded form derivatives,” without constructing the form, proving closability, or showing equivalence of norms across \(\eta\).

Kato's type-(B) theorem applies after a common closed form domain has been verified; it cannot be used to create that domain.

### 6. The generator derivative formula is only formal on a form scale

The displayed identity

\[
D(z-L_\eta)^{-1}
=(z-L_\eta)^{-1}(DL_\eta)(z-L_\eta)^{-1}
\]

requires a well-defined operator derivative \(DL_\eta\) between compatible spaces. For a type-(B) form family, the derivative is naturally a form \(\mathcal V\to\mathcal V^*\), and the resolvent identity must be written through the associated form operators. The manuscript uses ordinary operator notation without specifying those domains.

### 7. Optional projections do not follow from weak/stable path convergence alone

Convergence of martingales together with uniform \(L^{1+\delta}\) bounds does not generally imply convergence of their optional projections when filtrations change. One needs extended weak convergence of filtrations, convergence of conditional kernels on a determining class, and uniform approximation of the complete filtration.

A4's disputed complete-past spectral theorem and quenched kernel claim are the only supplied inputs. They do not establish the required filtration convergence.

### 8. The quadratic BSDE conclusion lacks a specified driver and solution class

“Exponential transformation of the bounded terminal value” can produce a standard entropic BSDE once the Brownian filtration, generator, sign convention, and integrability class are fixed. The theorem does not state these data. It presents a generic stochastic-calculus identity as a platform consequence without proving the deterministic-to-diffusion likelihood convergence.

### 9. All major platform dependencies remain open

The Sinai side depends on A2–A4, whose Fourier, controlled LDP, and complete-past spectral theorems fail. The hard-sphere side depends on B1–B4, whose shell, contact LDP, covariance, and comparison theorems remain unproved. C2 cannot close those gaps through quotient notation.

## Genuine improvements recognized

The following should be retained:

- signed invariant-measure duals;
- distinct invariant and pressure quotients;
- use of the full perturbed pressure functional rather than one scalar value;
- finite spectral frames rather than a regularity-losing Kato ODE;
- separate physical resolved projections; and
- explicit separation of source and state chain rules.

## Required reconstruction

Correct the quotient theorem first. Then construct all phase-dependent operator objects on a genuinely common transfer/form space, with domains and norm equivalences proved. The hard-sphere rigidity statement must be derived from an exact representation theorem for the full density/contact source, not from a local covariance slogan. Optional-projection convergence should be formulated as an independent filtration-convergence theorem.

## Recommendation

**Reject.** The leading quotient theorem has a one-line constant counterexample, and the common form bundle is assumed rather than constructed. The memory, likelihood, BSDE, and contraction synthesis remains conditional on invalid upstream interfaces.