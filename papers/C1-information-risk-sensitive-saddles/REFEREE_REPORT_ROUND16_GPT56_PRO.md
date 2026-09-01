# Independent Referee Report — Round Sixteen

**Paper:** `C1 — Information and Risk-Sensitive Saddles`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/C1-information-risk-sensitive-saddles`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/C1_DOMINATED_INFORMATION_TOPOLOGY.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate responds to the previous disintegration counterexample by restricting to a dominated observation class. Joint laws are written
\[
J(dx,dy)=p(x)\,m(dx)\,\kappa(dy\mid x),
\]
with a common reference measure, two-sided bounds and Lipschitz control on \(\kappa\). It then strengthens the topology by including \(L^1\) convergence of \(p\), integrated total-variation convergence of posteriors, and countably many moments. In that topology posterior disintegration is continuous essentially by definition. The paper claims a good LDP, filter stability, a posterior-state DPP, and LAN/saddle results.

Restricting the observation class is a legitimate way to avoid the weak-topology counterexample. The price is a much stronger topology. The candidate does not prove exponential tightness or goodness in that topology; in fact its compactness theorem is false.

## Major objections

### 1. Entropy sublevels are not compact in the proposed information topology

Take
\[
K=Y=[0,1],\qquad m=\ell=\text{Lebesgue},\qquad
\kappa(y\mid x)\equiv1,
\]
and for fixed \(0<a<1\) set
\[
p_n(x)=1+a\sin(2\pi n x).
\]
Then \(p_n\) are positive probability densities with a uniform two-sided bound. Their relative entropies
\[
\int_0^1 p_n\log p_n\,dx
\]
are uniformly bounded (indeed independent of \(n\)). All ordinary moment/tightness conditions on the compact state space hold. The joint laws converge weakly—and in \(W_1\)—to \(m\otimes\ell\), and integrals against every fixed continuous determining function converge by oscillation.

But
\[
\|p_n-1\|_{L^1}
 =a\int_0^1|\sin(2\pi x)|\,dx
 =\frac{2a}{\pi}
\]
for every \(n\). No subsequence converges in the \(L^1\) component of the proposed metric. Since \(\kappa\equiv1\), the posterior is \(p_n(x)m(dx)\), independent of \(y\), so the integrated posterior total-variation term also stays a fixed positive distance from the limit.

Thus the entropy/moment sublevel used in the candidate is not precompact in \(d_{\rm dit}\). This directly contradicts the compactness/good-rate theorem.

### 2. Weak LDP plus local LLT does not give a strong-topology LDP

The proof says that density convergence follows from the A2 or B1 local limit theorem and that the same expansion upgrades the weak LDP to the dominated information topology. Even a valid pointwise LLT would not yield exponential tightness in \(L^1\) or integrated posterior TV. One needs exponentially good approximation estimates uniform over the entire state space.

The oscillatory example above shows what must be excluded: arbitrarily fine density oscillations cost bounded entropy and disappear in weak topology while remaining separated in \(L^1\). No Sobolev/BV regularity or exponential modulus-of-continuity estimate for \(p\) is imposed. Consequently the proposed rate cannot be good in the stated topology.

### 3. The topology makes filter continuity tautological but may exclude the microscopic laws

Once integrated posterior TV is part of the metric, continuity of the posterior map on the dominated class is nearly built into the definition. The nontrivial task is to show that the finite-particle empirical/observation laws actually take values in this class with uniform two-sided and Lipschitz constants.

Empirical laws are typically atomic, not densities of the form required by \(\mathfrak D_{\rm dit}\). If the candidate instead uses smoothed or annealed laws, it must define that microscopic observable and prove exponential equivalence to the claimed one. The paper does not do so.

Moreover, conditioning and nonlinear evolution can cause the lower domination constant to deteriorate with time. A fixed compact-horizon bound is asserted, not derived.

### 4. The posterior DPP lacks a proved Markov state and measurable selection theorem

The candidate treats the posterior/joint law as a strong Markov state and writes a risk-sensitive DPP. It does not prove that the controlled observation process is closed in the dominated topology, that regular conditional probabilities can be chosen measurably as a function of the state and control, or that concatenation preserves the uniform domination constants.

These issues are not cosmetic. The admissible control set depends on the hidden kinetic/dynamical state, and the posterior transition kernel must be specified before a Nisio or saddle operator is defined.

### 5. LAN is stated without quadratic-mean differentiability of the exact experiment

An \(L^2\) score expansion for a limiting density does not establish LAN for the finite microscopic experiments. The authors need a uniform square-root likelihood expansion, a Lindeberg condition, and convergence of the information matrices under the exact observation law. The transfer/cluster expansions are cited but no remainder estimate at \(N^{-1/2}\) scale is given.

The claimed minimax/saddle conclusion also requires contiguity and uniformity over local alternatives. Those do not follow from the strong-topology LDP.

### 6. Upstream normalizations are unavailable

The density upgrade is attributed to A2 in the Sinai sector and B1/B2 in the hard-sphere sector. The recovered A2 and B1 modules do not prove their raw coefficient theorems, and B2 does not prove positive recovery. C1 therefore lacks even its stated input assumptions.

## Genuine progress

The paper correctly accepts that disintegration is not weakly continuous and introduces domination/TV structure rather than repeating the false Feller claim. This is a substantive conceptual correction. A viable theorem may exist on a sufficiently regular dominated class.

The current topology is too strong for the compactness proof supplied, and the counterexample above is decisive.

## Minimum requirements for a new submission

The authors must:

1. impose and derive compact regularity of the densities \(p\), such as uniform BV/Sobolev control with a compact embedding into \(L^1\);
2. prove exponential tightness and exponentially good approximation in the strong topology;
3. define a microscopic observable that actually lies in the dominated class;
4. prove closure of domination under filtering, control, and concatenation;
5. establish the posterior-state Markov kernel and measurable selection;
6. prove LAN by a finite-experiment quadratic-mean argument;
7. remove dependence on the invalid A2/B1 inputs.

## Verdict

**Reject.** The candidate fixes the logical category of the old posterior theorem, but its new good-LDP theorem is directly false: bounded entropy and moments do not give compactness in the \(L^1\)+posterior-TV topology. The downstream DPP and LAN conclusions therefore have no foundation.
