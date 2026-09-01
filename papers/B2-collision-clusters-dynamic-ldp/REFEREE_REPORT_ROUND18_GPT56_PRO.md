# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`B2_GLOBAL_PRECONTACT_POSITIVE_RECOVERY.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The grand-canonical pressure and both joint LDPs are not proved.

## 1. Overall assessment

Round Seventeen contains two serious conceptual improvements. A surplus collision is now imposed through a pre-contact zero set before reflection is applied, which is the correct causal order, and the lower-bound discussion recognizes that an entropy penalty cannot manufacture feasibility outside the positive collision cone. These changes address genuine earlier defects.

The replacement proof still does not establish a convergent trajectory expansion or a full dynamic LDP. Most decisively, the genealogy estimate contains a factorial growth `k!`, while the proof of convergence later silently drops that factorial and invokes a geometric series. This is a direct contradiction in the active source. The pre-contact atlas, Green-trace closure, positive recovery, deterministic-contact change of measure, and projective LDP identification are also asserted rather than proved.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The closed Green-trace graph is not established in the declared weak topology

Theorem `thm:r17-b2-trace` claims that the free-transport generator with specular binary boundary relation has a closed graph in a space of transport currents and that the contact balance relation is closed under weighted weak convergence on entropy/moment sublevels.

The proof invokes the divergence theorem, “trace compactness for divergence-measure fields,” and entropy uniform integrability. It does not define the domain geometry, the normal trace space, or the topology in which incoming traces converge. For hard-sphere configuration domains the boundary has corners and multiple-contact strata; the normal field and specular map become singular at grazing and intersections. Although those strata have zero Liouville flux for a fixed smooth law, a sequence of flux measures can concentrate near them. Zero mass at each finite `\varepsilon` does not by itself exclude nonzero limiting concentration.

One needs a quantitative nonconcentration estimate near grazing, multiple collisions, and corners, uniform in the Boltzmann–Grad limit, together with a trace compactness theorem adapted to the growing-dimensional hard-sphere domains. No such theorem is given. The claimed closedness is therefore not available for the LDP upper bound or rate-domain identification.

### 2.2. [FATAL] The “global regular pre-contact atlas” does not follow from analyticity and one witness

For a fixed genealogy `G`, Lemma `lem:r17-b2-precontact` asserts a finite cover of the entire regular surplus-contact set by charts whose `3\times3` minors are bounded below, plus analytic sublevel estimates for the complement.

The zero set and parameter domain are not compact before truncation. A nonzero analytic minor at one constructed witness shows only that the minor is not identically zero on one connected analytic component. It does not show that every realized component contains a regular point of that minor, that a finite set of minors covers all components, or that the rank is three everywhere outside a controlled analytic stratum. Nor does it produce a uniform lower bound on a finite cover without compactness.

The proof later introduces compact truncation, but the lemma itself is global and its constants enter the genealogy estimate. Dependence of the Łojasiewicz exponent and constants on `G`, velocity cutoff, chronology separation, and truncation is not tracked. This is precisely the dependence that must be controlled before summing genealogies or taking the two limits.

### 2.3. [MAJOR] The coarea gain is not derived with the stated `\varepsilon` power and physical future

The proof of `lem:r17-b2-gain` says the contact tube has transverse volume `O(\varepsilon^2)` and then optimizes against an analytic sublevel estimate. But `\mathcal F_G=0` is a three-component condition involving `(t,\omega)` and trajectory parameters, while the collision cross section, normal-flux factor, and Boltzmann–Grad activity have their own powers of `\varepsilon`. The relative normalization to a creation tree is not written.

After imposing the zero set, a reflection can alter all later potential contacts and can move the trajectory into singular chronology strata. Smooth measure preservation of a single binary reflection does not prove that the complete post-collision genealogy map has the required bounded Jacobian and remains in the same admissible chart. The statement that the estimate “retains the true reflected future” is a goal, not a demonstrated consequence.

### 2.4. [FATAL, direct internal contradiction] The factorial genealogy bound is converted into a geometric series without justification

Immediately before `thm:r17-b2-majorant`, the manuscript states

\[
\sum_{|G|=k}W_G^\varepsilon(h,\psi)\le k!C^kT^{k-1}.
\]

The proof of the theorem then says that the discarded tail is bounded by the tail of the “absolutely convergent series”

\[
\sum_k C^kT^{k-1}.
\]

The factor `k!` has disappeared. As written, `\sum k! C^kT^{k-1}` diverges for every `T>0`. If the log-partition expansion contains an external `1/k!` symmetry factor, it must be included in the definition of `W_G` or in the displayed summation and proved not to be cancelled by label/genealogy counting. The active source explicitly calls `W_G` the “absolute connected trajectory weight” and gives no compensating factor.

This error destroys the tail estimate in `thm:r17-b2-majorant`, the normal convergence used in `thm:r17-b2-pressure`, all source-derivative claims, and the cumulant inputs later invoked by B1 and B3.

### 2.5. [FATAL] The two-limit argument does not supply a uniform all-genealogy result

Even after repairing the missing factorial normalization, the proof only says: truncate to finitely many genealogies, use the minimum of their positive exponents, let `\varepsilon\to0`, and then let the truncation grow. This requires a tail estimate uniform in `\varepsilon` and in the source, plus a truncation scheme controlling labels, contacts, velocities, chronology gaps, and all derivatives.

The constants `C_G` and exponents `\alpha_G` can deteriorate arbitrarily with `G`. The fixed-`K` vanishing of surplus contributions does not imply that the total surplus contribution is negligible after `K\to\infty` unless the untruncated tail is independently summable at the correct normalized-log scale. That summability is exactly what the erroneous factorial argument was supposed to provide.

The final sentence that time slicing permits every bounded source also lacks a concatenation theorem. The number of genealogies and possible recollisions across slices grows, and source derivatives need compatibility at slice boundaries.

### 2.6. [FATAL] A Lanford-type finite genealogy expansion is not a proof of the claimed analytic log-Laplace pressure

Theorem `thm:r17-b2-pressure` asserts local uniform convergence, with all fixed source derivatives, of a normalized log-Laplace functional for density and actual-contact measures to a unique analytic mild solution of a kinetic Hamiltonian equation.

This is a substantially stronger result than finite-time propagation of chaos or convergence of finitely many marginals. To prove it one needs exponential-scale control of the partition function and all connected cumulants, uniform over the source ball. The paper's genealogy outline does not establish:

1. the exact connected expansion of the logarithm in the deterministic hard-sphere ensemble;
2. absolute convergence at the `\mu_\varepsilon` scale;
3. treatment of overlapping clusters and initial correlations;
4. uniform control of arbitrary actual-contact markings;
5. uniqueness and analytic dependence of the nonlinear Hamiltonian flow in a specified Banach space.

“Selecting the last creation contact factorizes the two rooted subtrees” is not valid without a precise combinatorial factorization and proof that recollision/surplus histories are negligible uniformly in the connected expansion.

### 2.7. [FATAL] The positive balanced approximation theorem is not proved for the nonlinear collision reference `A_f`

The collision reference is nonlinear:

\[
dA_f=\tfrac12 ff_*B\,dt\,dx\,dv\,dv_*\,d\omega.
\]

Mixing two balanced pairs linearly preserves the weak balance equation, but the collision reference of the mixed density is not the corresponding linear mixture of `A_f` terms; it contains cross products. Convexity of the perspective entropy in a generic pair `(A,\Gamma)` does not immediately give the claimed action convergence when `A=A_f` is a nonlinear function of `f`.

Likewise, simultaneous smoothing of the density current and collision current may commute with the linear balance operator, but it does not imply

\[
\Gamma_n\ll A_{f_n}
\]

with a Radon–Nikodym derivative bounded above and below. Strict positivity of `f_n` on a compact velocity set gives `A_{f_n}>0` pointwise only where the collision kernel is positive, but a smoothed `\Gamma_n` can have concentrations or zeros at incompatible rates. Pointwise lower/upper bounds on `q_n` require quantitative comparability, not merely positivity.

The velocity truncation is also claimed to replace a tail by a Maxwellian “with the same mass, momentum, and energy” while retaining exact balance and action convergence. The required conservative correction and its collision cost are not constructed.

### 2.8. [FATAL] The “microscopic contact tilt” formula is not an exact Radon–Nikodym formula for deterministic contacts

The proof of `thm:r17-b2-exposure` writes the likelihood cost as

\[
\int\log q_n\,d\Gamma_n-\int(q_n-1)dA_{f_n}.
\]

That is the familiar compensator formula for changing the intensity of a Poisson random measure. In the microscopic hard-sphere model, the contact process is a deterministic function of the random initial configuration. Tilting the initial law by an exponential of contact marks gives an exact likelihood equal to the source functional minus the finite-volume log normalizer. It does not have a Poisson compensator representation unless that representation is proved as a limiting theorem.

The manuscript appears to infer the limiting action from the formal Hamiltonian and then use it as an exact microscopic change of measure. That is circular. Concentration under a source tilt also requires strict differentiability/exposedness and an exponential tightness theorem, not merely a second derivative bound.

### 2.9. [FATAL] Finite-dimensional pressure limits plus tightness do not identify the full good LDP in one paragraph

The proof of `thm:r17-b2-gc` invokes finite collections of tests, Dawson–Gärtner, exponential tightness, positive recovery, and compact action sublevels. None of the required topological objects is defined precisely. The projective limit theorem gives a rate as a supremum of finite-dimensional duals; identifying it with the displayed density-contact action requires a rigorous duality theorem and proof that all balance/contact constraints are detected by the test class.

Exponential tightness of the contact measure, velocity tails, and time modulus at speed `\mu_\varepsilon` is simply asserted. Goodness of the action is also nontrivial because `A_f` depends quadratically on a weakly convergent density. Lower semicontinuity and compactness do not follow from the scalar perspective integrand alone.

The microcanonical theorem then depends on the unproved B1 source-dependent shell coefficient and cannot be credited independently.

## 3. Dependency consequences

B2-GC is the root of the hard-sphere dependency chain. Its failure invalidates the stated upstream input to B1, and therefore also B2-MC, B3, B4, C1, C2, and D1. The factorial error is especially consequential because those later papers repeatedly cite the “B2 factorial majorant” for cumulants and correctors.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a complete hard-sphere trace theorem with quantitative exclusion of singular-boundary concentration;
2. compactly formulated pre-contact charts and uniform genealogy-dependent estimates;
3. a correct, fully normalized connected expansion with a genuinely summable tail;
4. exponential-scale control of the marked log-Laplace functional and source derivatives;
5. a rigorous positivity-preserving density theorem accounting for the nonlinear map `f\mapsto A_f`;
6. an exact finite-volume tilt argument, followed separately by derivation of the limiting entropy action;
7. full projective-topology exponential tightness, rate identification, and goodness proofs;
8. only after those steps, a source-uniform microcanonical transfer theorem.

## 5. Recommendation

**Reject.** The causal pre-contact reformulation is promising, but the active proof contains a fatal factorial inconsistency and does not establish the pressure, recovery, microscopic tilt, or full LDP. Since B2 is the foundation of the hard-sphere chain, no downstream theorem may treat its outputs as proved.