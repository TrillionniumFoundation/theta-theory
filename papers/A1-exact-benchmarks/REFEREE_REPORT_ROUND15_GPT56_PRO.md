# Independent Referee Report — Round 15

**Manuscript:** A1 — *Exact Benchmarks*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

The branch is labelled and committed as a Round-Fifteen publication, but the manuscript in this folder still declares `ROUND14-REFEREE-POSITIVE-CLOSURE` and inputs `ROUND14_POSITIVE_CLOSURE.tex`. No `ROUND15_POSITIVE_CLOSURE.tex`, Round-Fifteen author response, or Round-Fifteen certificate is present in the submitted tree. The surviving `.round15` reconstruction archive is truncated and does not contain a recoverable A1 candidate source.

A referee can review only the controlling bytes actually submitted. The mathematical object before me is therefore the Round-Fourteen A1 manuscript, together with a failed claim that a later revision has been published. That provenance defect is independently disqualifying for external review.

## Executive assessment

The manuscript correctly separates the ordinary baker square from the zero-dimensional symbolic natural extension and tries to replace the earlier degenerating refinement norm by a mass-based current complex. Those are sensible repairs. The announced autonomous exact Hamiltonian realization nevertheless starts from an incorrect primitive identity, and the global impact quotient and all-order response space are not constructed with the stated smoothness and domain properties.

After removing those claims, the remaining Bernoulli/baker computations are useful benchmark material but do not meet the novelty threshold of a top-four mathematics journal.

## Decisive mathematical objections

### 1. The exact one-form identity is false

On branch \(i\), write

\[
Q=(q-s)/w,\qquad P=s+wp.
\]

For the canonical one-form \(p\,dq\),

\[
B_i^*(P\,dQ)-p\,dq
=(s+wp)\frac{dq}{w}-p\,dq
=\frac{s}{w}\,dq.
\]

A primitive is therefore

\[
G(q,p)=\frac{s}{w}(q-s)+\text{constant}.
\]

The manuscript instead inserts the additional term \(-sp\). Its differential contributes \(-s\,dp\), which is absent from the pullback difference. Thus the exact face-matching identity used to glue the channel primitive is wrong. The asserted exact symplectic cobordism, global primitive, and Hamiltonian impact network do not follow.

### 2. The proposed regular section is not an ordinary smooth section

The set obtained by deleting all forward and backward seam iterates is invariant and has full measure, but it is cut by a countable dense family of singular curves. The manuscript does not prove that this complement, with the intended return topology and graph completion, is a smooth two-dimensional manifold serving as a global Poincaré section of the quotient flow.

Keeping seams as “ideal impact faces” is not enough. One must construct compatible local charts near accumulating seam orbits, prove Hausdorffness of the quotient, and verify completeness or precisely state the maximal regular flow. None is supplied.

### 3. The flag-current space is defined circularly

The norm contains

\[
\mathbf M(D_a^jT_F)
\]

before the parameter derivative \(D_a\) has been constructed as a closed operator on the completed current space. The subsequent proposition then claims to construct exactly that operator using the norm already defined with it.

A valid scale must start from independently defined jet currents or graph norms on a fixed reference bundle, prove closability, and only then complete. The present definition cannot establish its own domain.

### 4. “All-order response” is only a proof schema

The response theorem says the derivative is a finite sum of “words” formed from one-sided resolvents, scores, present-symbol coupling, and flags. It does not specify the word set, combinatorial coefficients, transport identifications between the \(a\)-dependent spaces, or quantitative bounds uniform in word depth. The cancellation for a fixed physical observable is true at the level of the invariant Lebesgue integral, but it does not validate the undefined individual operator words.

### 5. The mechanical interpretation remains overextended

The work family is deliberately engineered by choosing

\[
p_i(\vartheta)\propto p_i^0e^{\vartheta c_i}.
\]

This proves closure of that chosen exponential family. It does not show that an independently given mechanical system selects the same scalar as a universal risk-preference coefficient. At most it realizes a canonical field conjugate to the chosen branch current.

### 6. Corrected content remains below the editorial threshold

After deleting the false exact gluing and undefined response claims, the core is an explicit Bernoulli baker coding, an additive branch current, and standard Poisson/resolvent identities. This is useful as a regression example, not as an independent top-four theorem.

## Required reconstruction

A viable benchmark paper should:

1. correct the primitive and give a complete hybrid symplectic-category construction;
2. work on a fixed physical current space with independently defined parameter jets;
3. state the response expansion explicitly, with domains and summability constants;
4. keep symbolic coding, mechanical realization, and risk calibration as separate claims; and
5. substantially reduce the editorial claims.

## Recommendation

**Reject.** The submitted branch does not contain a Round-Fifteen A1 manuscript, and the controlling Round-Fourteen theorem begins with a false exact one-form calculation. Even after repair, the surviving result is benchmark material rather than a top-four theorem.
