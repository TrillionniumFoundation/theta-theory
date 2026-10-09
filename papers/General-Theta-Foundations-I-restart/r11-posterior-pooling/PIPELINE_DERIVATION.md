# General derivation, not a realization rebranding

## 1. Start at the experiment

Given finite hidden preparation p0, controlled transition T and normalized positive report densities f, the actual report law is r(p,a,y)m(dy), r=sum_j(pT)_j f_j. The conditional Bayes map F is its normalized coordinate vector. All actions are chosen before the report. The scored future test is the terminal categorical state. Its expected loss is defined on the induced complete physical law.

## 2. Realize the predictive quotient

On the stated compact-history class, countable future-test evaluations have Borel image and a Borel section. Equality includes legal interface. For raw sensor kernels with an invertible legal transition, next-report means recover incoming belief; equal beliefs give all future controlled laws. Phase is appended. A smaller task chart is not thereby a full simulator.

## 3. Replace approximate filter trajectories by exact information loss

Let I be the old finite state, carrying the *true* conditional distribution p_i, and choose its action by the full Bellman value. After the actual report compute W=F(p_i,a_i,y), then retain only the global cell J. Offline pool every incoming edge:

alpha'_j=E 1{W in C_j}; b_j=E[W 1{W in C_j}]/alpha'_j.

Then b_j=P(X'=.|J=j). This induction uses exactly the information possessed by the finite machine. The full-history posterior is never retained or reconstructed in the upper.

## 4. A general error identity

With Q_t=P(X_t|Z_t), W_t=P(X_t|Z_{t-1},Y_t), Bellman minimization gives E V_t(W_t)=E V_{t-1}(Q_{t-1}). Hence

R_pool-B_n* = sum_t {E V_t(E[W_t|Z_t])-E V_t(W_t)}.

This is a sum of actual Jensen gaps. It survives policy switches because each V_t is concave, not because its optimizer is Lipschitz.

## 5. Integrate curvature rather than assume smoothness

For convex f=-V, subtract a tangent on each cube. Subharmonic averaging and convex radial growth bound the cube's oscillation by h^(2-d) times its local Laplacian mass. A density at most rho supplies h^d, and bounded overlap plus a Lipschitz cutoff bounds total curvature. Therefore the sum of cell gaps is O(rho h^2). Mollification proves the same statement for nonsmooth Bellman envelopes.

## 6. Lower geometry and matching

Every full-history terminal posterior law remains rho-bounded by conditioning before the last action/report. An M-ball union covers at most rho v_d M r^d mass. Projection thus gives excess >= c M^(-2/d) above the optimal full-history Bayes risk, uniformly in the acquisition policy. A checkpoint grid gives its matching upper. A phase-labelled pooling implementation gives C sum L_t^(-2/d) with exactly 1+sum L_t states. At fixed n this matches the exponent; its joint n bound is explicitly weaker and is not suppressed.

## 7. Derive raw acquired geometry

For f0=2^-d, fj=2^-d(1+lambda yj), q=pT and D=1+lambda sum qj yj, the posterior map has inverse and Jacobian lambda^d product(qj)/D^(d+1). T entries >=tau give a uniform compact interior carrier and actual-law density bound. In two states the information gain series I(q) is strictly increasing; asymmetric sensor choice changes with a noisy observed posterior. A two-call gap is bounded below by an explicit positive rational expression in alpha,lambda.

## 8. Singular and resource composition

A finite face mixture is pooled facewise; actual masses are preserved and atoms are encoded exactly. The physical validation channel gives repeated rank changes. Calibrated digital evaluation crosses a cell boundary only in an actual-mass slab. First-mismatch coupling combines numerical and physical errors, while typed causal simulation multiplies internal states. The early-channel experiment combines an attained deficiency with the same adaptive hidden-state task.

Each step is proved in the new native source. The old separated frontier, continuation, rank and block mechanisms remain fully available in integral supplements, with their original quantifiers.
