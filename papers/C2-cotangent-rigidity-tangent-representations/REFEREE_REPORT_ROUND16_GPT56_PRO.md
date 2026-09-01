# Independent Referee Report — Round Sixteen

**Paper:** `C2 — Cotangent Rigidity and Tangent Representations`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/C2-cotangent-rigidity-tangent-representations`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/C2_CONNECTED_PLATFORM_RESPONSE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate tries to repair the two principal defects of the controlling manuscript. It works with a weighted strict topology and Radon duals instead of an underspecified Banach dual, and it introduces a metric connection for a parameter-dependent Hilbert realization so that the derivative of the resolvent includes the varying metric. In the form setting it replaces the undefined expression \(PLP\) by a resolved form matrix. It then states a connected memory formula, pressure/cotangent rigidity, optional-projection convergence, and a platform-labelled functor theorem.

Including the metric connection is a genuine correction. The connected-memory formula is still not defined under the stated hypotheses, and the rigidity/filtration results are largely delegated to unavailable upstream theorems.

## Major objections

### 1. A compressed resolvent need not be invertible

The candidate defines
\[
C(z)=P(z-L)^{-1}P
\]
on the resolved range and then writes \(C(z)^{-1}\) in the memory kernel, assuming that \(z\) lies in a common resolvent half-plane. This is not sufficient.

A finite-dimensional counterexample already defeats the statement. On \(H=\mathbb R^2\), let
\[
L=\begin{pmatrix}0&-3\\1&0\end{pmatrix},\qquad z=1,
\]
and let \(P\) be the orthogonal projection onto
\[
e=\frac1{\sqrt2}(1,1).
\]
The eigenvalues of \(L\) are \(\pm i\sqrt3\); \(L\) generates a bounded finite-dimensional group, and \(z=1\) lies strictly to the right of its growth bound. Yet
\[
(zI-L)^{-1}
 =\frac14\begin{pmatrix}1&-3\\1&1\end{pmatrix}
\]
and
\[
\langle e,(zI-L)^{-1}e\rangle=0.
\]
Hence
\[
P(zI-L)^{-1}P=0
\]
on the one-dimensional resolved range, so the inverse used by the theorem does not exist.

The paper needs an explicit Feshbach/nondegeneracy or accretivity hypothesis and a proof that it holds for every platform considered. Membership of \(z\) in the resolvent set is not enough.

### 2. The covariant derivative formula requires a fully specified transported realization

Writing
\[
\nabla_\eta=\partial_\eta+\tfrac12G_\eta^{-1}G_\eta'
\]
addresses the missing metric term, but the theorem also varies the Riesz projection, form domain, null space, and complement. The candidate says that the Kato transport extends by the identity on a fixed complement. A fixed complement need not remain complementary to \(\operatorname{Ran}P_\eta\), and the extension need not intertwine the projections or preserve the form domain.

To differentiate
\[
R_\eta(z)=(z-L_\eta)^{-1}
\]
covariantly, the authors must specify one fixed ambient space, transport both domain and range, and define the induced connection on endomorphisms. The displayed commutator formula is formal until those maps are shown bounded and differentiable in the relevant graph/form norms.

### 3. The strict-dual theorem is not proved for the stated weighted topology

The dual of a weighted strict topology can indeed be a weighted Radon measure space, but only for a precisely defined locally convex topology and weight system. The candidate describes convergence on compact weight sublevels plus bounded-set control and then asserts a Riesz representation.

It does not verify completeness, barrelledness, the exact bounded sets, or continuity of the proposed functionals. The passage from compact restrictions to a countably additive global measure requires a uniform variation/tightness argument that is only stated. The later annihilator and quotient assertions therefore rest on an incompletely defined dual pair.

### 4. Pressure equality does not yield the asserted rigidity by the supplied argument

In the Sinai sector, the candidate differentiates equality of local pressure functionals and then invokes periodic-orbit separation and Livšic theory on an induced singular/countable system. It does not prove that the perturbation class separates every relevant periodic orbit, that the roof/unbounded observables satisfy the Livšic hypotheses, or that the coboundary transfer belongs to the weighted strict space.

In the hard-sphere sector, the annihilator identification is imported from B3's closed-range/observability theorem. The B3 report shows that theorem is not proved. Thus the cotangent rigidity result is conditional in both platform sectors.

### 5. Optional projections do not converge from the stated inputs

The optional-projection theorem uses convergence of filtrations, likelihoods, and underlying paths and concludes convergence of projected observables. Under changing filtrations this is delicate: weak convergence plus uniform integrability does not generally imply convergence of conditional expectations. One needs an extended-weak/stable convergence theorem with a verified immersion or conditional-independence structure.

The manuscript cites A4 history-kernel convergence and B3 likelihood estimates, neither of which is available. It also does not prove that the chosen versions of conditional expectation are compatible with the platform transport.

### 6. The form-domain repair is only local

Replacing \(PLP\) by a resolved form matrix avoids an undefined operator product at one displayed formula. It does not prove that the compressed form is closed, that its resolvent agrees with the operator compression, or that the memory inverse exists. These are Schur-complement theorems, not notation changes.

### 7. The “platform functor” is a bookkeeping declaration

The final functor theorem says that identities commute when all arrows obey the typing rules. No universal property, faithfulness, naturality proof, or nontrivial equivalence is established. At present it summarizes desired compatibility rather than proving a new mathematical result.

## Genuine progress

The varying-metric derivative is no longer silently omitted, and the candidate recognizes that form-domain and operator-domain compressions must be distinguished. Those are necessary corrections and should remain in any rewrite.

They do not close the compressed-resolvent, rigidity, or filtration gaps.

## Dependency and editorial significance

C2 is presented as the common dual/memory interface for A4, B3, B4, and D1. A common interface must state hypotheses strong enough to make every compression and inverse defined. The finite-dimensional counterexample shows that the current abstract theorem is false even before the model-specific inputs are considered.

## Minimum requirements for a new submission

A viable theorem needs:

1. a precise weighted strict topology and a full Radon-dual proof;
2. a fixed transported ambient/form realization with graph-norm differentiability;
3. a proved nondegeneracy/accretivity condition guaranteeing invertibility of \(P(z-L)^{-1}P\);
4. a rigorous Feshbach/Schur-complement formula in the form setting;
5. platform-specific Livšic/closed-range theorems with verified hypotheses;
6. a genuine extended-weak theorem for optional projections under changing filtrations;
7. removal or precise categorical formulation of the platform-functor claim.

## Verdict

**Reject.** The metric-connection correction is real, but the central connected-memory formula takes the inverse of an object that may be zero under the stated hypotheses. The rigidity and filtration results then depend on unproved upstream inputs. The paper is not mathematically closed.
