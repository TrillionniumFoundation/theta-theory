# Notation audit

- D: compact convex **test-coordinate** mixture domain; in the quantum section D_q denotes physical Hilbert-space dimension. K is the buffered update range; neither equals the actual acquired support by assertion.
- d: intrinsic affine predictive coordinate dimension; d_j is current affine-stratum dimension.
- u: an incoming predictive state/barycenter. X_t: exact full-history predictive vector under the actual selected policy. Q_t: conditional barycenter given the actual retained label. W_t: unpooled report-updated barycenter.
- ell: scalar report likelihood. c_{t,a}(y): row linear functional in raw likelihood. c(u) in the task is an affine second-moment function; the arguments distinguish these uses.
- U_{t,a}: affine unnormalized test numerator, not the independent bit U in the joint subsection. c(y)v is scalar; the Hessian numerator is A(y)v-(c(y)v)F(y,u).
- mu_{t,a,u}: actual row law; nu_t^pi: actual full-history policy law. lambda_{t,a}: report reference measure, not an acquisition law. Quantum lambda is a channel contraction parameter and is local to that section.
- V_t: full-history Bellman value of the declared terminal task, not a policy-conditional filter error. V_0 is not a universal monotone static-parameter learning curve.
- epsilon_*: acquired common mass. vartheta=1-epsilon_*: Bellman decay. rho is reserved for quantum density operators, avoiding an ambiguous stability rho.
- epsilon: attained causal deficiency in the post-control bit experiment; not epsilon_*.
- delta: actual unobservable calibration offset in the joint task. delta_out and gamma: numerical readout error and action slack; not the same lower-bound mechanism.
- n: core reports; N=n+2 core physical calls, or N=n+3 in the joint experiment. m: terminal checkpoint labels. M: total autonomous configurations, not bits.
- Xi_w(m): actual-weight singular profile; no normalization to surviving strata.

Label, citation, environment and active-source checks are automated by `verify.py`; their successful result is not a semantic proof audit. The build records actual displayed theorem numbers from the final aux file.
