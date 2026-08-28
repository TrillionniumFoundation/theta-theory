# Referee guide — Paper IV, revision v4

## Central claims

The paper proves a noncompact filter contraction and a positive pure-strategy
Isaacs mechanism, then combines them with the exact moving-collision
innovations in one deterministic partially observed model.

## Suggested audit order

1. **Bayes expansion:** check the total-variation convention and constant.
2. **Refresh--AR kernel:** verify the common-component contraction and the
   exact quadratic Lyapunov identity.
3. **Posterior moment ball:** check the two independent strict gates and the
   affine moment recursion.
4. **Initial layer:** verify why geometric sensitivity alone is insufficient
   and how the prior-dependent reward disappears.
5. **Curvature compensation:** audit the saddle operator, exact mixed-Hessian
   cancellation, normal-cone variational inclusion, coercivity, and strong
   monotonicity.
6. **Pure selector:** check global saddle inequalities and the Lipschitz
   parameter estimate.
7. **Quadratic energy game:** verify the saddle, Hamiltonian, and nonconvex sign.
8. **Lower/upper schemes:** audit coercive localization, Taylor consistency,
   equality of the two limiting Hamiltonians, and comparison.
9. **Continuous-time verification:** check both Itô inequalities and the
   viscosity approximation/selector stability step.
10. **End-to-end product model:** verify that the filter, collision innovations,
    controls, and slow recursion are defined on one deterministic product
    system.

## High-risk proof locations

- uniform posterior contraction under control-dependent perturbations;
- maximal-monotone existence on noncompact constrained controls;
- uniform curvature domination on the doubled-variable jet range;
- passage from smooth feedback verification to bounded viscosity data;
- strategy-tree uniformity of the filter error convolution.

## Permanent scope

Pure Isaacs structure follows from curvature compensation, not from mixed
minimax.  Lower and upper discrete values need not coincide at each mesh; the
paper proves that they converge to one pure-strategy continuum value.

A report should separately assess the filter theorem, the curvature theorem,
the scheme convergence, and the full deterministic actualization.
