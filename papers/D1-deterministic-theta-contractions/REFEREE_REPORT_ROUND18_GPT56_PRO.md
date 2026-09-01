# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`D1_LATENT_PHASE_SEMIGROUP.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The abstract finite-mixture lemmas are partly correct, but no model-specific phase theorem or posterior semigroup is proved.

## 1. Overall assessment

The revision corrects two earlier conceptual errors. A phase is now posited as a genuine positive latent label rather than a smooth partition weight relabeled as a discrete event, and the manuscript no longer calls the physical-state marginal log-sum operator a semigroup. The exact sign identity

\[
Q_{\varepsilon,j}^{\rm un}(F)
=-\alpha_{\varepsilon,j}+\widetilde Q_{\varepsilon,j}(F)
\]

is correct. The finite-mixture LDP in `thm:r17-d1-joint` is also correct **conditional on** the existence of finitely many genuine conditional laws with good component LDPs and the stated weight asymptotics.

Those conditional abstract facts do not establish the advertised Sinai/hard-sphere theory. The positive latent phase experiments are not constructed from the microscopic models, the proposed augmented state is insufficient for hidden components with different dynamics, the risk-sensitive log-sum formula illegally combines separately optimized component values, the zero-free theorem assumes its conclusion in a dominant-term expansion, and the Gaussian-mixture theorem contains a direct scaling error. The main result is therefore not proved.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The genuine phase decomposition is assumed, not constructed

The manuscript begins with a random label `J` and conditional path laws `P_{\varepsilon,j}` on a common path space. It then says that in the Sinai platform these arise from “positive recurrent components of the inducing graph plus a boundary component,” and in the hard-sphere platform from “positive source/preparation phases” constructed by B1–B4.

No measurable partition, latent-variable extension, or disintegration of the original microscopic law is given. In particular:

1. recurrent communicating components of an inducing graph need not correspond to a finite partition of the physical Sinai measure;
2. a “boundary component” may have zero mass or overlap with closures of recurrent components;
3. hard-sphere source tilts/preparations are alternative probability laws, not automatically mutually exclusive events of one common experiment;
4. choosing a source parameter at time zero is a control/preparation decision, not a latent random phase unless an explicit prior mixture experiment is defined;
5. the component weights and conditional laws may depend on the observed horizon or source, defeating a fixed latent decomposition.

The equality

\[
P_\varepsilon=\sum_jw_{\varepsilon,j}P_{\varepsilon,j}
\]

is therefore a new assumption, not a theorem about the original model. The finite-mixture LDP proves only an abstract proposition under that assumption.

### 2.2. [MAJOR] The component LDP hypotheses are not supplied by the upstream papers

Theorem `thm:r17-d1-joint` assumes each `P_{\varepsilon,j}` has a good path LDP at one common speed. Neither A3 nor B2 proves the required model LDP in this review, and neither manuscript establishes phase-conditioned LDPs with uniform exponential tightness and component-dependent normalizations.

Even abstractly, if some component weight is superexponentially small or if component speeds differ, the stated finite rate formula needs modification. The normalization by `\min_k\alpha_k` is correct only when all `\alpha_j` are finite at the common speed and the weights sum to one with compatible subexponential factors. These conditions should be part of the theorem.

### 2.3. [FATAL] The state `(x,\rho)` is generally not sufficient for posterior phase dynamics

The posterior weight

\[
\rho_t(j)=P(J=j\mid\mathcal F_t)
\]

is only one part of the information state. When different phases have different hidden transition kernels or filters, future likelihoods depend on the **phase-conditioned posterior state** for each component. A common physical state `x` together with scalar weights `\rho(j)` is insufficient unless the component state is fully observed and shared, or a lumpability theorem is proved.

For a hidden-state model the correct information state typically has the form

\[
(\rho(j),\pi^j_t)_{j=0}^m,
\]

where `\pi^j_t` is the conditional hidden-state belief under phase `j`, possibly together with unnormalized likelihood variables. The manuscript says that `S_t^j` includes its own physical/filter state, but then evaluates every component as `S_t^jh(x)` at the same `x`. It does not define a common state space or the coupling of component filters under one observed history.

Consequently, Bayes multiplication of scalar likelihood increments does not prove that the announced augmented process is Markov or that `\mathbf S_t` is a semigroup.

### 2.4. [FATAL] Common domination and likelihood increments are missing

The Bayes update

\[
\rho_t(j)=\frac{\rho_s(j)L_{s,t}^j}
{\sum_k\rho_s(k)L_{s,t}^k}
\]

requires the component observation laws over `[s,t]` to be dominated by one common reference conditional law, with `L_{s,t}^j` measurable as a function of the observed increment and current component information state. The manuscript does not specify this reference law or prove multiplicativity when the control is adaptive.

If component laws are mutually singular—as phase laws often are in asymptotic decompositions—finite-volume likelihood ratios may exist only on restricted sigma-fields or fail altogether. C1's dominated regular chart is unproved and does not supply a global common likelihood for the D1 phases.

### 2.5. [FATAL] The log-sum of separately optimized component semigroups is not the controlled mixture value

Theorem `thm:r17-d1-semigroup` states

\[
\mathcal V_t(x,\rho;h)
=\frac1\theta\log\sum_j\rho(j)
\exp\{\theta S_t^jh(x)\}.
\]

If `S_t^j` is a risk-sensitive **controlled** semigroup, each component value normally contains a supremum or infimum over controls. The controller in the mixture experiment does not know `J`; it must choose one admissible observation-based control shared across all components. In general,

\[
\sup_u\log\sum_j\rho_j E_j^u[e^{\theta h}]
\ne
\log\sum_j\rho_j\exp\{\theta\sup_u V_j^u\}.
\]

The right-hand side permits a different optimizing control for every hidden phase and therefore gives the value of a controller who observes `J`, not the posterior-control problem advertised. The operations “optimize” and “sum over latent phases” do not commute.

A correct DPP must optimize on the full phase-conditioned belief state with one nonanticipative control. The exact finite conditional-expectation identity only gives a log-sum **for a fixed common policy**, after which the common policy is optimized. This distinction is fatal to the stated semigroup and value formula.

### 2.6. [MAJOR] The zero-free chart theorem is conditional on an unproved dominant-term estimate

The Rouché argument in `thm:r17-d1-charts` is correct if one already has

\[
Z_{\varepsilon,j}(F)
=c_{\varepsilon,j}(F)e^{a_\varepsilon q_j(F)}+R_{\varepsilon,j}(F),
\quad |c|\ge c_0,
\quad |R|\le\tfrac12 c_0e^{a_\varepsilon\Re q_j}
\]

uniformly on a complex neighborhood. But this is essentially the desired spectral/coefficient dominance theorem. The manuscript does not derive it from A2/A3 or B1/B2; those papers do not prove the needed uniform complex estimates in this review.

Real positivity gives no zero-free complex neighborhood, and a simple leading eigenvalue of a transfer operator does not automatically control a finite-volume restricted partition function uniformly when component leakage, boundary terms, or conditioning are present. Thus the theorem is a correct elementary lemma under a powerful assumption, not a model-specific result.

### 2.7. [FATAL, direct scaling error] The Gaussian-mixture limit is written for the wrong random variable

The assumptions say that under component `j`,

\[
\sqrt{a_\varepsilon}\bigl(TX_\varepsilon-m_j\bigr)
\Rightarrow N(0,\Sigma_j).
\]

This implies `TX_\varepsilon\to m_j` in probability. Therefore:

- the unscaled labelled variable `(J,TX_\varepsilon)` can converge to a mixture of point masses `\delta_{m_j}`;
- the componentwise centered and scaled variable can converge to `N(0,\Sigma_j)`;
- there is no single variable specified by the assumptions that converges to `N(m_j,\Sigma_j)`.

The theorem nevertheless states a mixture

\[
\sum_{j\in J_*}\omega_j\,\delta_j\otimes N(m_j,\Sigma_j).
\]

This is dimensionally and asymptotically inconsistent. To obtain a normal with mean `m_j`, one would need to define a scaled variable such as `m_j+\sqrt{a_\varepsilon}(TX_\varepsilon-m_j)`, which depends on the latent label in its centering. The active theorem does not do so.

This direct error invalidates the central second-order coexistence claim.

### 2.8. [MAJOR] The tie-weight formula is incomplete and `\gamma_*` is undefined

The weights use an indicator `\mathbf1_{\{\gamma_j=\gamma_*\}}`, but `\gamma_*` is not defined. Presumably it is the smallest polynomial exponent among exponentially minimizing phases. This must be stated.

Moreover, the expansion of the prior/component weights alone need not determine posterior or conditioned tie weights. Component partition functions, saddle determinants, local likelihood normalizations, and the event on which the mixture is conditioned can contribute additional subexponential factors. The coefficient `c_j` in `w_{\varepsilon,j}` is sufficient only for the unconditional label prior under the exact assumptions, not for every “conditioning sequence” claimed in the theorem.

### 2.9. [FATAL] The phase-aware contraction theorem merely assumes all difficult commutations

The rate contraction formula follows from the abstract joint finite-mixture LDP. The rest of `thm:r17-d1-contraction` says that conditioning, pressure differentiation, Gaussian tangent formation, and posterior aggregation commute whenever upstream interfaces hold. This is not a theorem without precise hypotheses:

- conditioning on shrinking events requires local estimates, not ordinary contraction;
- differentiation through a limit requires locally uniform analytic control;
- Gaussian tangent push-forward requires a well-defined scaled variable and continuous linear map;
- posterior aggregation under control requires a shared-policy DPP;
- C2's purported typed contraction theorem is itself unproved.

The final caveat separating mechanical and valuation coefficients is correct, but it does not establish the preceding universality claim.

## 3. What remains valid

Two abstract statements can be retained after proper hypotheses are added:

1. a finite mixture of genuine component LDPs has the joint and marginal rate given in `thm:r17-d1-joint`;
2. the exact sign/log-sum identity in `lem:r17-d1-sign` holds for a fixed finite mixture.

These facts are elementary and useful, but they do not constitute the advertised phase theory for Sinai billiards or deterministic hard spheres.

## 4. Dependency consequences

D1 sits at the end of both dependency chains and assumes inputs from A2–A4, B1–B4, C1, and C2. Those inputs fail independent review. D1 also fails internally at the latent construction, shared-control posterior DPP, and Gaussian scaling stages. It cannot serve as a synthesis theorem for the series.

## 5. Minimum requirements for reconsideration

A future submission would need:

1. an explicit finite-volume latent-phase experiment whose marginal is exactly the original microscopic law;
2. component conditional laws and good LDPs at a common speed, with proved weight asymptotics;
3. a sufficient information state containing phase-conditioned beliefs/states, not only `(x,\rho)`;
4. common domination and measurable likelihood increments;
5. a DPP with one shared observation-based control and the correct order of optimization and mixture aggregation;
6. model-specific complex dominance estimates before invoking Rouché;
7. a corrected definition of the scaled Gaussian variable and complete tie-weight asymptotics;
8. separate the elementary finite-mixture lemmas from any universality or commutation claims.

## 6. Recommendation

**Reject.** The revision fixes the sign and abandons the false marginal-semigroup assertion, but it still assumes the existence of the phase experiment it claims to derive. The proposed posterior state and controlled log-sum value are incorrect in general, and the Gaussian coexistence theorem has a direct scaling inconsistency. Only the elementary conditional finite-mixture lemmas are presently valid.