# External top-four referee report on A2-DYN revision 39

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v39-referee-response-2026-10-08`, `revision/a2-dyn-v39-referee-copy-2026-10-08`  
**Reviewed commit:** `75eda04842b69319ae81c97ce1502129d55ee5fc`  
**Reviewed repository tree:** `57ca1b85a1c5d0c4077fbefa676e0209ef1709b8`  
**Ordinary source payload tree:** `42bf99511d4d6dcf01c945b0207649a3b40d87da`  
**Active manuscript directory:** `papers/A2-DYN-v39-referee-response`  
**Active mathematical source:** eighty-three numbered core modules; revision 39 adds modules 82--83  
**Frozen revision-38 author baseline:** `00f8b9baa95a2fa9d29b1e2e7164dc0f5cb2938e`  
**Frozen revision-38 paper tree:** `8b2b1d651e059c69827d10be0882c333a8901be1`  
**Controlling report:** `reviews/a2-dyn-v38-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `44a673d7d0dd2662e679b99f344709ce6f832107` / `dadc2fc8896e471c2686e02389df82f075b9051f`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 39 is a genuine mathematical advance over revision 38. It addresses the precise arithmetic and endpoint questions left open by the previous report rather than relabeling a mesoscopic theorem as a singleton theorem.

The revision adds two proof modules:

- `core/82_occupation_resonance_group.tex`;
- `core/83_section_source_cancellation.tex`.

The first module studies the full measurable phase equation

\[
q\circ T_R=
 e^{i(u\cdot\kappa_R+b\tau_R+v\eta_R+s)}q,
\qquad |q|=1,
\]

where \(\eta_R=\mathbf 1_{Y_R^*}\) is the true section occupation. It proves uniform isolation of nontrivial measurable phases near the joint origin, finite-on-bands structure, injectivity of the occupation-coordinate projection, a finite cyclic zero-roof subgroup, and an exact all-frequency correspondence with the genuinely induced return equation.

The second module works on the physical \(L^2\) space with the actual section source. It derives an exact source identity, spectral-window, resolvent and Cesaro estimates, a quadratic spectral-measure factor at zero physical frequency, an exact second-difference identity for the section-to-section characteristic function, bounded collision-clock partial sums, and an explicit Abel limit on the whole occupation torus away from zero.

I audited these two modules, their front-matter use, the response to the previous report, the proof ledger, the source manifest, and the exact-source qualification records. I found no decisive counterexample, sign error, endpoint-count error, missing section-mass factor, or false inference from an Abel average to a fixed coefficient in the new text.

In particular, the manuscript correctly distinguishes all of the following:

1. existence of a measurable peripheral phase;
2. the residue of that phase in the specific \(\eta_R\)--\(\eta_R\) endpoint pairing;
3. bounded collision-clock partial sums;
4. an Abel limit as the clock-generating parameter tends to one;
5. decay of a fixed collision-count coefficient;
6. cancellation of the full exact-index occupation-torus remainder; and
7. pointwise inversion in the roof variable.

This distinction is essential, and revision 39 handles it more carefully than many arguments in this area.

The negative recommendation is nevertheless forced by the exact scope of the new results. The resonance group is classified but not shown trivial. The source cancellation is exact only for a special endpoint vector and, at zero physical frequency, only annihilates the unit-eigenvalue residue. The Abel and partial-sum estimates average over the collision clock. They do not establish decay of the fixed-\(m\) coefficient appearing in the exact-index inverse, and they do not control the nonzero displacement--roof frequencies in that remainder.

Consequently, revision 39 still does not prove

\[
 m^2\mathcal R^q_{n,m,R}(k,t)\longrightarrow0
\]

for the remainder isolated in revision 38. It also does not prove the common pointwise raw correction, the full roof-frequency complement, or a pointwise roof-density local limit. The advertised four-coordinate singleton raw mixed-density theorem therefore remains incomplete.

The new results are conceptually useful and may be important ingredients in a future closure. They are not, at present, a substitute for the missing main endpoint or a general theorem of independent breadth sufficient for the requested venue standard.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`75eda04842b69319ae81c97ce1502129d55ee5fc`.

The repository tree at that commit is

`57ca1b85a1c5d0c4077fbefa676e0209ef1709b8`.

The active manuscript is

`papers/A2-DYN-v39-referee-response`.

The source manifest identifies revision 38 as the exact author baseline. All eighty-one inherited core modules and all ninety-one inherited Python files are retained byte-for-byte. The bibliography, inherited mathematical labels, and compiled A--X synopsis are retained. Revision 39 adds modules 82 and 83 and updates the explanatory front matter and source records while preserving previous versions under provenance.

The branch chronology is correct. The revision begins from the controlling revision-38 review commit and then adds a new author manuscript tree. It is not a review commit relabeled as an author source.

The present review branch begins directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v39-external-top4-review-2026-10-08/`.

No author manuscript source, prior review, workflow, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully on both reviewed branches:

- response branch run `37703491265`;
- referee-copy branch run `37703502179`.

The verifier checks, among other things:

- the frozen revision-38 paper identity;
- all eighty-three core inclusions;
- byte identity of the eighty-one inherited cores and ninety-one inherited scripts;
- preservation of inherited labels, bibliography, and A--X statements;
- the exact controlling-report blob and workflow hash;
- the ordinary-source Merkle identity;
- normal/optimized diagnostic agreement;
- native TeX compilation and theorem-label-based page rendering.

The new finite diagnostics test the second-difference identity, the `[0,m)` endpoint convention, finite unitary resolvents, the source spectral factor, the nonzero-frequency source identity, and the norm estimates. The negative controls reject a missing initial factor \(z\), insertion of the terminal visit, and the invalid inference of coefficient decay from bounded partial sums.

These are meaningful source, algebra, and regression checks. They do not establish the inherited continuum collision-space estimates, the small-occupation perturbation theorem, the full measurable phase theorem, a full-torus anisotropic power bound, the exact-index cancellation, or the pointwise roof-density theorem. The validation packet states this limitation accurately.

## 4. Scope of this review

I concentrated on the claims which could materially change the revision-38 assessment:

1. exclusion of measurable phases near the joint origin;
2. passage from smooth endpoint spectral decay to arbitrary measurable transfer functions;
3. group closure, uniform separation, and finite-on-bands counting;
4. injectivity of the occupation projection and the two possible group structures;
5. the exact all-frequency induced phase equation;
6. the physical unitary convention and source identity;
7. spectral-window, resolvent, and Cesaro estimates for the section source;
8. the spectral-measure identity at zero physical frequency;
9. invisibility of a pure occupation unit eigenphase in the actual endpoint pairing;
10. the exact second-difference identity and its endpoint convention;
11. the collision-clock partial-sum and Abel estimates;
12. the relationship of these results to the fixed-count exact-index inverse;
13. the remaining pointwise roof inversion; and
14. source identity and qualification evidence.

The inherited revision-38 chain is treated as the source-pinned baseline. This report does not independently re-certify every one of its eighty-one modules.

## 5. Local exclusion of measurable phases

The first new lemma uses the joint near-origin spectral expansion from revision 37. In centered coordinates

\[
X_R=(\kappa_{R,1},\kappa_{R,2},
      \tau_R-\bar\tau_R,\eta_R-c),
\]

the principal eigenvalue satisfies, on a uniform punctured neighborhood,

\[
|\lambda_R(\Theta)|\le e^{-a|\Theta|^2}<1.
\]

Thus twisted pairings of fixed smooth endpoint functions tend to zero at every nonzero frequency in that neighborhood.

The transfer function in the measurable phase equation is only assumed measurable and circle-valued. The manuscript approximates it in \(L^1\) by smooth bounded functions. Replacing the initial and terminal occurrences changes the pairing by at most twice the \(L^1\) error, uniformly in the iterate, because the dynamics preserves the collision probability and all phase factors have modulus one.

The order of limits is correct: the approximation is fixed first, the collision count tends to infinity next, and only then is the approximation error removed. No uniform smooth norm of the approximants is needed.

The exact iterated phase equation gives a right-hand side of modulus one. The smooth approximation gives a left-hand side tending to zero. This contradiction excludes every nontrivial measurable phase in a common punctured neighborhood.

At the origin, collision mixing excludes nontrivial scalar eigenphases and ergodicity makes invariant circle-valued functions constant.

I found this argument coherent, subject to the inherited joint spectral expansion.

## 6. The resonance group

Products and quotients of measurable phase solutions give a group. Uniqueness of the scalar phase over a fixed frequency triple follows because the quotient of two solutions is a collision eigenfunction with a constant eigenvalue. Mixing leaves only the trivial scalar phase, and ergodicity makes the quotient constant.

The difference of two distinct resonance triples is a nonzero resonance. The local exclusion lemma therefore gives a uniform positive separation between all distinct elements. This yields closedness without requiring compactness of the transfer functions.

Packing separated points in

\[
\mathbb T^3\times[-B,B]
\]

gives the linear band count

\[
\#\{(u,b,v)\in\mathcal G_R:|b|\le B\}
   \le C(1+B),
\]

uniformly in the radius.

When the occupation coordinate is zero, the phase equation reduces to the already proved complete physical displacement--roof phase equation. That theorem forces every remaining coordinate to be trivial. Therefore projection to the occupation coordinate is injective.

The subgroup with roof coordinate zero is finite, injects into the occupation circle, and is consequently cyclic. If the roof projection is nonzero, its finite-on-bands property makes it a discrete additive subgroup of \(\mathbb R\), hence a lattice \(\beta_R\mathbb Z\). Choosing one lift of the positive generator gives the asserted finite extension by the zero-roof cyclic subgroup.

The occupation coordinate of a roof generator must be irrational modulo \(2\pi\). Otherwise a positive multiple would have zero occupation coordinate but nonzero roof coordinate, contradicting injectivity.

The band-count estimate also supplies a radius-uniform lower bound for the positive roof spacing when that projection is nonzero.

I found no algebraic defect in this classification.

Two limitations should remain explicit.

First, the theorem classifies possibilities but proves neither that the group is trivial nor that a nonzero group occurs. Second, discrete measurable point spectrum does not by itself provide a spectral-radius estimate for the full anisotropic operator family on the occupation torus. Continuous or residual spectral effects and the quantitative behavior of long powers remain separate questions.

## 7. Exact induced arithmetic

The phase equation telescopes to the actual first return. Because the occupation sum on the half-open interval `[0,r_R^*)` is exactly one, restriction to the section gives

\[
 q_*\circ F_R^*
 =e^{i(u\cdot\kappa_R^*+b\tau_R^*
       +s r_R^*+v)}q_*.
\]

Conversely, the genuine return tower provides a measurable representation of almost every collision state as \(T_R^j y\), with \(0\le j<r_R^*(y)\). Extending the induced transfer function along the tower gives the one-step phase equation, including the case of return time one.

The placement of the occupation factor is correct: the initial section level contributes \(v\), while the terminal section is excluded from the half-open occupation count.

This equivalence clarifies the arithmetic roles of the parameters. The occupation phase \(v\) becomes the spectral phase of one induced return, while the scalar collision phase \(s\) multiplies the actual collision count \(r_R^*\). Ordinary finite lattice-cover mixing does not automatically eliminate a nonzero \(v\).

This is a useful clarification of the obstruction.

## 8. The physical unitary operator

The second new module introduces

\[
 U_{R,\omega,v}h
 =\bigl(e^{i(\omega\cdot f_R^{\rm c}+v\eta_R)}h\bigr)
       \circ T_R^{-1}.
\]

On physical \(L^2(\nu)\) this is unitary. Its inverse is

\[
 U^{-1}h
 =e^{-i(\omega\cdot f_R^{\rm c}+v\eta_R)}h\circ T_R.
\]

The elementary identity

\[
e^{-iv\eta_R}=1+(e^{-iv}-1)\eta_R
\]

leads to the exact source relation

\[
(e^{-iv}-1)\eta_R
 =(U^{-1}-I)1+h_{R,\omega,v},
\]

where

\[
h_{R,\omega,v}
 =(e^{i\omega\cdot f_R^{\rm c}}-1)U^{-1}1.
\]

The one-collision record is bounded, so

\[
\|h_{R,\omega,v}\|_2\le C|\omega|
\]

for \(|\omega|\le1\), uniformly in the radius and occupation phase.

I checked the signs in this identity. The two terms on the right combine to

\[
e^{-iv\eta_R}-1,
\]

as required. No occupation-itinerary derivative or long-word partition enters.

## 9. Spectral-window, resolvent, and Cesaro bounds

Applying the unitary spectral projection onto

\[
|\lambda-1|\le\epsilon
\]

to the source identity gives

\[
\|E(\epsilon)\eta_R\|_2
 \le \frac{\epsilon+C|\omega|}{|e^{iv}-1|}.
\]

On that spectral window,

\[
\|U^{-1}-I\|\le\epsilon,
\]

and the projection is a contraction. This argument is correct.

For the Abel resolvent, the scalar spectral multiplier satisfies

\[
\sup_{|\lambda|=1}
 \frac{|\lambda^{-1}-1|}{|1-r\lambda|}
 =\frac{2}{1+r},
\]

while

\[
\|(I-rU)^{-1}\|\le(1-r)^{-1}.
\]

These yield the stated source-vector estimate

\[
\|(I-rU)^{-1}\eta_R\|_2
 \le
 \frac{2/(1+r)+C|\omega|/(1-r)}{|e^{iv}-1|}.
\]

The factor \(|\omega|/(1-r)\) is retained. It is not silently treated as uniformly small in a joint limit.

The Cesaro estimate follows from the telescoping identity

\[
\sum_{j=0}^{M-1}U^j(U^{-1}-I)1
 =(U^{-1}-U^{M-1})1.
\]

The result is a bound for the actual section source \(\eta_R\), not a norm bound for the full resolvent or all vectors in \(L^2\). The manuscript states this distinction correctly.

## 10. The spectral-measure factor at zero physical frequency

At \(\omega=0\), the error vector \(h\) vanishes and the source identity is exact. Functional calculus gives

\[
 d\mu_{\eta_R,v}(\lambda)
 =\frac{|\lambda-1|^2}{|e^{iv}-1|^2}
    d\mu_{1,v}(\lambda).
\]

Thus the section source has zero projection onto the unit eigenvalue for every nonzero pure occupation phase.

If a circle-valued function satisfies

\[
q\circ T_R=e^{iv\eta_R}q,
\]

then invariance gives

\[
(e^{iv}-1)\int\eta_Rq\,d\nu=0.
\]

Hence both its collision-section coefficient and its induced mean vanish.

This establishes invisibility of a pure occupation phase at unit eigenvalue in the specific \(\eta_R\)--\(\eta_R\) pairing.

It does not establish the following stronger statements:

- vanishing for nonzero physical frequency \(\omega\);
- vanishing at an eigenvalue different from one;
- absence of all nonzero occupation resonances;
- decay of the continuous spectral contribution; or
- decay of a fixed collision-count coefficient.

Those distinctions are explicit in the manuscript and are mathematically important.

## 11. The exact second-difference identity

Let

\[
F_{m,R}(v)=\int e^{ivA_{m,R}}\,d\nu
\]

and

\[
C_{m,R}(v)=
 \int\eta_R(x)\eta_R(T_R^m x)
     e^{ivA_{m,R}(x)}\,d\nu(x).
\]

Writing \(z=e^{iv}\), stationarity gives

\[
F_{m+1}-F_m
 =(z-1)\int\eta_0 z^{\eta_1+\cdots+\eta_m}\,d\nu.
\]

Subtracting the analogous formula at \(m-1\) gives a second difference with both endpoint indicators. On the support of \(\eta_0\eta_m\), one additional factor \(z\) inserts the initial visit while still excluding the terminal visit. Therefore

\[
C_{m,R}(v)
 =\frac{z}{(z-1)^2}
  \bigl(F_{m+1,R}-2F_{m,R}+F_{m-1,R}\bigr).
\]

I checked the endpoint convention and the factor \(z\). They are correct. The formula also works at \(m=1\).

The exact return disintegration gives

\[
C_{m,R}(v)
 =c\sum_{n\ge1}e^{ivn}
   \nu_R^*\{N_{n,R}=m\},
\]

with only finitely many terms for fixed \(m\). This is the true return generating coefficient, not a surrogate count.

## 12. Collision-clock partial sums and the Abel limit

Summing the second difference from one to \(M\) leaves

\[
F_{M+1}-F_M-F_1+F_0.
\]

Since every \(F_m\) has modulus at most one,

\[
\left|\sum_{m=1}^M C_{m,R}(v)\right|
 \le \frac4{|e^{iv}-1|^2}.
\]

This is uniform in the radius and on every closed occupation-torus complement of zero.

For the Abel sum, direct summation of the second difference yields

\[
\sum_{m\ge1}r^mC_{m,R}(v)
 =\frac{z}{(z-1)^2}
 \left\{
   \frac{(1-r)^2}{r}F_R(r,v)
   -\frac{1-r}{r}-c(z-1)
 \right\}.
\]

The first two terms in braces have total modulus at most

\[
2(1-r)/r,
\]

which is bounded by \(4(1-r)\) for \(r\ge1/2\). The final term gives

\[
\frac{cz}{1-z}.
\]

The printed Abel estimate is therefore correct.

The manuscript also supplies a finite stationary example showing that bounded partial sums do not imply coefficient decay. This is an appropriate warning and prevents the new average estimate from being overinterpreted.

## 13. Why the exact-index blocker remains

The remainder in the revision-38 exact-index formula is a fixed collision-count coefficient. It contains an integral over the occupation torus outside the controlled central strip and, for a band-limited roof test, also integrates the displacement and roof frequencies.

Revision 39 supplies three kinds of information:

1. measurable resonances are uniformly separated and finite on bounded roof bands;
2. a pure occupation unit eigenphase has zero residue for the actual section endpoints at zero physical frequency;
3. the pure occupation section-source coefficients have bounded clock partial sums and an explicit Abel limit.

None of these statements alone yields the required fixed-\(m\) cancellation.

The reasons are structural.

First, resonance classification is not a full-torus power estimate. Even if point spectrum is finite, quantitative control of long powers away from those points is still needed.

Second, the exact zero-residue statement applies to \(\omega=0\) and unit eigenvalue. The exact-index remainder includes nonzero displacement--roof frequencies, and a general resonance may correspond to a scalar eigenvalue different from one.

Third, bounded partial sums and Abel convergence permit oscillatory coefficients that do not decay. The manuscript's two-cycle example illustrates precisely this distinction.

Fourth, a source-vector resolvent estimate does not automatically control every weighted endpoint insertion or the full operator norm needed for a uniform Fourier inverse.

Therefore the revision does not prove

\[
 m^2\mathcal R^q_{n,m,R}(k,t)\to0.
\]

The source manifest, proof ledger, and main text all correctly leave this claim false.

## 14. The pointwise roof problem is unchanged

The current exact-index result for a roof interval remains the concentration bound

\[
P_{n,m,R}(k,t;J)
 \le C(1+|J|)m^{-2}.
\]

The additive constant prevents division by \(|J|\) as the interval shrinks. Revision 39 introduces no new coarea derivative estimate and no new uniform control of high roof frequencies.

The following therefore remain open:

- the common pointwise correction for the actual-return law;
- complete control of critical and singular edge contributions;
- the full roof-frequency complement;
- pointwise inversion in the continuous roof variable;
- the exact-index Gaussian asymptotic; and
- the unconditional four-coordinate raw mixed-density local limit theorem.

These are not editorial details. They are the main endpoint advertised by the title and the inherited raw-inversion architecture.

## 15. Mathematical value of the new results

The resonance-group theorem is a useful structural result. Its proof cleanly separates local probabilistic nondegeneracy from global measurable arithmetic. The exact induced correspondence also clarifies why finite-cover arguments for displacement do not automatically remove the return spectral phase.

The section-source identity is elementary in ingredients but effective. It reveals a cancellation specific to identical initial and terminal section indicators and explains why the existence of a phase need not imply a nonzero endpoint residue. The second-difference and Abel formulas are exact and may guide a future Tauberian or renewal analysis.

These results improve the mathematical understanding of the remaining obstruction. They are not merely status bookkeeping.

Their independent scope, however, is limited relative to the requested venue benchmark. The group classification depends on the already established local joint expansion and complete physical phase theorem. The source identity applies generally to invertible probability-preserving systems with an indicator section, but by itself is not a new local-limit theorem. In the submitted article it remains an auxiliary step toward an unfinished singleton raw-return endpoint.

## 16. Significance at the requested benchmark

The manuscript now contains several substantial completed packages:

1. a stationary microscopic local law;
2. a compact-family action principle with noncircular applications;
3. a mixed occupation local-central theorem;
4. diffusive and arbitrarily fine diverging return-index window laws;
5. an exact-index concentration upper bound;
6. resonance-group classification; and
7. section-source spectral and Abel cancellation.

This is a significant body of work.

Nevertheless, the paper's title, abstract, and long technical architecture continue to organize themselves around raw local inversion for the genuine four-coordinate return record. That endpoint is still not proved. The new structural results materially narrow the gap but do not close it.

At the *Annals* / *Acta* / *Inventiones* / *JAMS* level, a positive recommendation would require either:

- completion of the exact-index, pointwise-roof raw-return theorem; or
- a general theorem of sufficiently broad independent significance that the unfinished raw endpoint no longer governs the submission.

Revision 39 supplies neither yet.

## 17. Architecture and editorial burden

The manuscript is exceptionally large. It combines:

- stationary-flow local limits;
- a compact-family geometric action principle;
- anisotropic norm construction;
- measurable phase rigidity;
- occupation and return-index local laws;
- resonance classification;
- source spectral identities;
- raw edge extraction;
- incomplete pointwise return inversion; and
- extensive provenance and status material.

The front matter is honest about the topology of each theorem, which is a substantial improvement. The main proof path nevertheless remains difficult to evaluate because completed and incomplete programmes coexist in one article.

For a strong specialist submission before full raw closure, the completed stationary/action theorem and the return concentration/fine-window/resonance package could be presented as a focused article, with the pointwise raw programme separated as a sequel or technical companion.

If the unified article is retained for a top-four submission, the exact-index and pointwise-roof endpoint should be completed.

This is not a recommendation to delete valid mathematics. It is a recommendation to align the principal claim, title, abstract, and proof architecture with the strongest theorem actually proved.

## 18. Required changes before another top-four review

A subsequent revision should address the following matters.

1. **Convert the arithmetic classification into fixed-count control.**  
   Prove a full occupation-torus power estimate, or decompose the exact-index remainder into finitely many resonant contributions plus a quantitatively decaying complement.

2. **Treat every relevant resonance residue.**  
   The zero-frequency unit-eigenvalue cancellation is not enough. Establish the endpoint coefficient at nonzero displacement--roof frequency and at scalar eigenvalues different from one, or prove those resonances absent.

3. **Control the nonresonant full torus.**  
   Finite point spectrum on bounded bands does not exclude continuous near-unit spectrum. A uniform anisotropic, renewal, or Tauberian estimate is needed.

4. **Do not infer coefficients from Abel averages without a new theorem.**  
   Any passage from the collision-clock Abel estimate to fixed-\(m\) decay must state and prove the additional Tauberian, regularity, or cancellation hypotheses.

5. **Complete pointwise roof inversion.**  
   Prove the common correction and full roof-frequency complement in the local norm required by the raw density theorem.

6. **Keep all frequency and limit dependencies explicit.**  
   State which constants depend on the roof band, occupation distance from zero, radius, and endpoint class. Do not insert an \(m\)-dependent band into a fixed-band estimate without a new quantitative theorem.

7. **Obtain independent specialist review.**  
   The inherited collision-space chain and the new measurable-phase/source-cancellation arguments should be checked by experts in dispersing billiards and anisotropic transfer operators.

8. **Strengthen the generality and novelty case.**  
   Explain theorem by theorem what exceeds existing Lorentz-process, billiard mixing-LLT, suspension local-limit, and operator-renewal frameworks.

9. **Reduce the submission burden.**  
   Present one unmistakable principal theorem and move provenance, status ledgers, and unresolved companion programmes out of the main proof path where possible.

## 19. Technical and presentation comments

1. The term “zero-roof subgroup” should always be understood as the subgroup with roof coordinate \(b=0\), not as a statement about zero physical flight time.
2. The group metric used in the separation and packing argument should be fixed explicitly once, including the torus quotient convention.
3. The local phase-exclusion proof should retain the order: fix the \(L^1\) approximation, take the time limit, then remove the approximation.
4. The uniqueness of the scalar phase uses collision mixing; uniqueness of the transfer function up to a constant uses ergodicity. These roles should remain distinguished.
5. The occupation-coordinate injectivity uses only the previously proved \(v=0\) physical phase theorem. It must not be described as exclusion of nonzero occupation phases.
6. The possible lattice generator \(\gamma_R\) is not claimed parameter-continuous. No later argument should assume such continuity without proof.
7. The source spectral-window estimate degenerates as \(v\to0\). Uniformity is only on a closed complement unless the joint near-zero theory is inserted separately.
8. The source resolvent estimate contains \(|\omega|/(1-r)\). This term must remain visible in every joint limit.
9. The exact spectral-measure factor at \(\omega=0\) annihilates the atom at \(\lambda=1\), not all atoms and not the whole continuous spectrum.
10. The corollary on a pure occupation phase should continue to state the scalar phase being treated; a general \(s\ne0\) phase corresponds to a different unitary eigenvalue.
11. The factor \(z\) in the second-difference identity encodes inclusion of the initial visit and exclusion of the terminal visit. It should not be absorbed into notation.
12. The Abel estimate is uniform away from \(v=0\), not for an occupation phase approaching zero with \(m\) or \(r\).
13. The exact-index remainder includes nonzero displacement--roof frequencies. The pure occupation calculation is not a complete estimate of that remainder.
14. The single-index upper bound, diverging-window asymptotic, singleton asymptotic, and pointwise density theorem must remain separate claims.
15. Qualification runs and finite models should remain separated from proof certification, as they are in the current metadata.
16. A future response should identify the exact theorem-bearing author SHA and the exact controlling review blob.

## 20. Final assessment

Revision 39 is a serious and mathematically useful advance.

It replaces an unspecified occupation arithmetic obstruction by a uniformly discrete, finite-on-bands measurable resonance group and identifies the exact induced equation seen by true returns. It also proves an elegant section-source identity, spectral-window and resolvent bounds, a precise second-difference formula, bounded collision-clock partial sums, and a full-occupation-torus Abel limit. I found no decisive error in these new arguments.

The revision is also commendably honest about what these results do not prove. It does not infer fixed-count decay from Abel control, does not declare the resonance group trivial, and does not relabel source-vector cancellation as a full operator estimate.

The central raw-return endpoint nevertheless remains open. The fixed-\(m\) full occupation-torus remainder is uncontrolled, the exact-index Gaussian asymptotic is unproved, and pointwise roof inversion still lacks the common correction and complete frequency complement.

Subject to independent specialist verification, the completed stationary, fine-window, concentration, resonance, and source-cancellation results could support a strong dynamics/probability submission in a more focused architecture.

At the requested four-journal benchmark, however, the advertised singleton raw theorem is still incomplete and the present independent significance case does not compensate for that incompleteness.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
