# Independent Referee Report — Round Sixteen

**Paper:** `A1 — Exact Benchmarks`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/A1-exact-benchmarks`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/A1_HYBRID_EXACT_JET_RESPONSE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate tries to close three earlier defects at once: it corrects the canonical primitive for the branch map, gives two autonomous Hamiltonian-channel realizations, and replaces informal seam terms by a hierarchy of bulk, face, corner, and higher-flag currents equipped with a geometric mass norm. It then claims arbitrary fixed-order response jets and a functional central limit theorem for the full jet.

The algebraic correction is real. For
\[
Q=(q-s)/w,\qquad P=s+wp,
\]
the candidate now uses
\[
B_i^*(P\,dQ)-p\,dq=(s/w)\,dq
\]
and the primitive \(G=(s/w)q\); the spurious \(-s\,dp\) term from the controlling manuscript is gone. The transported-observable convention is also stated more honestly.

These repairs are useful, but the main response and fluctuation theorem is not proved.

## Major objections

### 1. The full jet is not a smooth cylinder observable

The probabilistic conclusion is justified by saying that each finite jet is a smooth cylinder observable of a mixing symbolic extension and therefore satisfies a CLT. That reduction is false without a substantial theorem. Differentiating a transfer operator across moving seams produces distributions supported on codimension-one faces; repeated differentiation produces traces on intersections of faces and derivatives of delta currents. These objects are not ordinary Hölder or smooth cylinder functions.

To invoke a scalar or Banach-valued CLT one must first construct a fixed topological vector space in which all shape derivatives live, prove that the transfer cocycle acts boundedly on it, and establish summable correlations or spectral perturbation estimates for the resulting current-valued observable. The candidate defines a formal flag space \(\mathfrak J_r\), but does not prove:

* continuity of all trace and restriction maps at corners;
* a closed chain rule for repeated moving-boundary differentiation;
* boundedness of the dynamics on the proposed mass norm;
* measurability and square integrability of the current-valued jet;
* tightness of the partial-sum process in the asserted path space.

Calling the resulting distributional jet a smooth cylinder observable simply renames the missing argument.

### 2. The arbitrary-order shape calculus is not closed

At second and higher order, products of boundary traces, normal derivatives, and moving incidence maps appear. A list of flags does not by itself make those products well-defined. The manuscript needs a recursive theorem showing that every derivative can be expressed as a finite compatible current, independent of the chosen local defining functions, with quantitative norm bounds uniform under refinement.

No such theorem is supplied. In particular, the claim that the geometric mass norm is nondegenerate under arbitrary refinement is much weaker than the estimate needed for response: refinement may proliferate strata, and the transfer of a current can increase both multiplicity and variation. There is no bound of the form
\[
\|\mathcal T_\eta^{(k)}J\|_{\mathfrak J_r}
   \le C_{r,k}\|J\|_{\mathfrak J_{r+k}}
\]
uniformly in the moving seam parameter. Without this, the stated Taylor expansion has no controlled remainder.

### 3. The functional CLT lacks a covariance and tightness theorem

Even if every scalar pairing of the jet satisfied a CLT, that would not yield a functional CLT for the full current-valued object. One needs a separable state space, a covariance operator defining a Radon Gaussian law, and a tightness criterion. The candidate merely writes the covariance series and asserts exponential tails. It does not prove nuclearity, trace-class covariance, a type-2 property, or a Mitoma-style reduction to a countable determining family with uniform estimates.

The asserted “uniform exponential tails” are also not derived from the symbolic mixing estimate. Seam currents can have parameter-dependent total variation near grazing or multiple-incidence configurations. The proof contains no quantitative exclusion or moment estimate that would make the covariance series converge in the claimed norm.

### 4. Local Hamiltonian channels are not a global autonomous realization

The two channel formulas verify local symplectic identities, but the theorem is stated for a single physical autonomous impact system. The candidate does not construct one globally smooth energy surface and Poincaré section on which all branches coexist with the advertised branch selection, no parasitic returns, and compatible gluing at seams. Local exactness of each branch is not enough. A global realization theorem must control the common section, return times, channel boundaries, and the higher-codimension encounters that are precisely where the current calculus is used.

This is not merely expository: the response theorem differentiates the global physical system, so the global family must exist before its jets can be defined.

## Dependency and editorial significance

A1 is comparatively independent of the long A2–A4 and B2–B4 chains, so the above defects cannot be excused as imported assumptions. The corrected primitive is a worthwhile repair, but the claimed arbitrary-order response and functional CLT are the paper's main new results. Both rest on unproved functional-analytic and probabilistic infrastructure.

## Minimum requirements for a new submission

A viable replacement would need, at minimum:

1. one explicit global autonomous Hamiltonian realization with a common section and a proof of exact return dynamics;
2. a fixed, complete current space carrying all flag traces and moving-boundary derivatives;
3. uniform operator and remainder estimates for the \(r\)-jet calculus;
4. a genuine scalar and current-valued correlation theorem, followed by a Radon Gaussian/tightness argument;
5. a clean separation between fixed physical observables and transported observables.

## Verdict

**Reject.** The candidate corrects the earlier one-line symplectic error, but the central arbitrary-order response and full-jet CLT are still theorem-sized assertions rather than consequences of the supplied analysis. Under a top-four standard this is not close to an acceptable proof.
