# Notation audit

- theta is fixed and inaccessible. Fresh per-cycle B in the joint example is a physical random variable, not theta.
- i,j are retained boundary labels. q is a Q-state exploration label; the quantum Hilbert dimension is also denoted q locally in its separate subsection, never in the product-chain proof.
- P is the boundary transition; Pi_P its Cesaro projection; G_P the group inverse of I-P; h(P) its row absolute-sum norm.
- d_i is a conditional mean duration; v_i is a stored readout decision. These are distinct in the program specification and cycle formulas.
- The decision space is calligraphic D; D=diag(d_i) is the diagonal duration matrix. Neither is a random memory register.
- H is a recurrence bound, not a loss bound. The full squared-loss normalizer in the joint theorem is written out as diam(K)^2+5.
- mu-bar is a uniform conditional mean bound. a(T) is a conditional tail envelope. K is a 1+p moment bound; the bound from distinct entering-state laws pays MK.
- beta is a normalized discount. N counts physical calls; it is not the machine's stored clock. Source physical time after simulation is a different denominator.
- nu is an acquired occupation submeasure, not necessarily a probability. pi is a preparation law in holding examples or a stationary boundary law when subscripted by a closed class.
- delta is a state-metric numerical tolerance in the generic recursion, and an actually inaccessible calibration coordinate in the sharp example. Those error models are stated separately.
- epsilon is full conditional scored-cycle TV; deficiency is its infimum over the explicitly typed simulator class. The sharp example fixes an environment-owned audit wire.

All main labels and bibliography keys are checked mechanically. Local quantum dimension and control-fiber notation are confined to separate subsections. Label checks are not a semantic proof.
