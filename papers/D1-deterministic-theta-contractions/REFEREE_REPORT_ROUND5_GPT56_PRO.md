# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `5f107627fd9b99bdc9b2e33c619ee8f2130cf49c`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/D1_EXHAUSTED_DOMAIN_COMMUTATION.tex`, blob `9dce1da261b12fc5899e36f44fa2707d4c06fd04`

## Source-control verdict

The active D1 paper is unchanged from round four. It still uses local pressure information as a global convex dual and packages the full LDP/exposed-density theorem as a hypothesis.

The round-five candidate introduces an exhausted source domain and is more honest about local versus global pressure. It is not materialized. Its “exact likelihood” contains the same finite-centering algebra error previously identified, and its exhaustion theorem assumes the decisive global lower-bound theorem through property P3. D1 remains a conditional summary rather than an independent contribution.

## Decisive algebraic error in the proposed likelihood theorem

The candidate defines

\[
m_\Theta=DQ(\Theta),
\qquad
Z_\varepsilon=\sqrt{\mu_\varepsilon}
(\mathcal X_\varepsilon-m_\Theta),
\]

but then writes

\[
L_\varepsilon(h)=\exp\left\{
\langle h,Z_\varepsilon\rangle
-
\mu_\varepsilon\left[
Q_\varepsilon(\Theta+h/\sqrt{\mu_\varepsilon})
-Q_\varepsilon(\Theta)
-\mu_\varepsilon^{-1/2}DQ_\varepsilon(\Theta)h
\right]
\right\}.
\]

The exact Radon–Nikodym density is

\[
R_\varepsilon(h)=\exp\left\{
\sqrt{\mu_\varepsilon}\langle h,\mathcal X_\varepsilon\rangle
-\mu_\varepsilon[Q_\varepsilon(\Theta+h/\sqrt{\mu_\varepsilon})
-Q_\varepsilon(\Theta)]
\right\}.
\]

A direct subtraction gives

\[
\log L_\varepsilon(h)-\log R_\varepsilon(h)
=\sqrt{\mu_\varepsilon}
\langle h,DQ_\varepsilon(\Theta)-DQ(\Theta)\rangle.
\]

No assumed convergence rate makes this term vanish. Thus `L_epsilon` is not the exact likelihood and need not have expectation one. The theorem explicitly claims exactness, so it is false as written. One must center `Z_epsilon` at `DQ_epsilon(Theta)`, or remove the compensating finite-mean term from the bracket and track the deterministic shift.

## Further major objections

### 1. Property P3 assumes the hard part of the full LDP

The exhaustion theorem assumes that every finite-rate point is approximated by regular tilted points with convergence of the action. This is precisely the rate-dense exposed-point lower-bound theorem that A3 and B2 have not proved. Under P3 the lower bound is nearly tautological: the proof gives it at a regular tilt and passes through the assumed approximants.

Calling P3 a “proved interface” does not make D1 an independent theorem. In the current series both cited interfaces are invalid.

### 2. Finite-dimensional local pressures do not alone identify one global rate

Projective upper bounds plus exponential tightness can produce an upper rate based on the chosen source algebra. Equality with a pre-existing model action requires that the algebra separates the state space and that the regular-tilt lower bounds are dense with the correct costs. Those are exactly the assumptions imported as P3.

The theorem therefore does not derive global duality from local charts; it restates the conditions under which a standard projective LDP argument works.

### 3. Convex duality may not identify the full nonlinear dynamic action

A Legendre–Fenchel conjugate is convex. The hard-sphere density–contact action contains the nonlinear reference intensity `A_f` and is not shown to be convex in the complete pair `(f,Gamma)` on the chosen path space. D1 simply declares the B2 rate equal to the exhausted conjugate. That equality must be proved in B2/B3, not inferred from pressure notation.

### 4. The no-duality-gap theorem lacks complete hypotheses

Fenchel–Rockafellar duality requires locally convex spaces, proper lower-semicontinuous convex functionals, continuous affine maps, and a constraint qualification. The candidate refers to a relative-interior regular mean point but does not state the topology of the state space or prove convexity and closedness of the feasible action. The result is not valid merely because a finite-dimensional constraint Hessian is positive.

### 5. The conditioning theorem remains dependent on unproved finite-volume input

Property P4 imports B1’s exact mixed shell coefficient. The proposed B1 theorem itself depends on the unproved B2 pressure and an incomplete characteristic-function argument. D1 contributes no independent verification.

### 6. Process likelihood conclusions are completely downstream

The final theorem says process convergence follows after invoking B3 and C2. B3 has no valid actual-contact compensator or process-tightness theorem; C2 has no proved conditional-kernel homogenization. D1 therefore supplies only a finite-dimensional analytic expansion, and even that expansion is incorrectly centered.

### 7. The rate–pressure–semigroup triangle is a diagram, not a new theorem

Once a good LDP, exact convex duality, additive action, and a constructed dynamic programming semigroup are assumed, the displayed relations are standard consequences. They do not close any microscopic interface. The paper’s independent novelty remains insufficient for a standalone top-four submission.

## Genuine improvement

The candidate correctly restricts the Legendre transform to an increasing proved source domain and retains the exact factor `mu_epsilon` in the pressure Hessian. It also keeps the constrained normalization constant and distinguishes finite-dimensional from process convergence. These corrections should be preserved in a future synthesis section.

## Required reconstruction

The likelihood must be centered at the exact finite-volume mean. The exhaustion theorem should be stated explicitly as an abstract conditional proposition, not as independent model closure, and its convexity/separation hypotheses must be complete. D1 should then be merged into the principal microscopic paper after A3/B2/B3/B4 are actually proved.

## Recommendation

**Reject; remove as a standalone submission.** The active paper is unchanged. The unmaterialized candidate contains a false exact-likelihood formula and assumes the global rate-density theorem it claims to organize. Its valid content is a collection of standard analytic and convex lemmas suitable for a later synthesis section, not an independent top-four paper.