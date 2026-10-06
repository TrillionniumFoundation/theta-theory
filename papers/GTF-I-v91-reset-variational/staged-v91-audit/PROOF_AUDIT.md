# Current proof audit — General Theta Foundations I, Revision 91

This is an author-side proof audit, not independent priority clearance. It responds to R60 and uses the exact reviewed v90 source as its baseline. Printed primary numbering is used first; source modules are secondary.

## Primary Section 15: general reset optimization (module 83)

The normal form purifies the first input and each receiver branch, retaining branch environments on the old side of the reset. The fresh complete input/reference is purified independently. Its common Gram constraints are `sum_h A_yh=rho` for every y and `tr b_yh=1`. Converse realization uses a support inverse of C0, so singular rho and zero branches are included. The input dimension is finite even when the original receiver is not.

Each leaf optimization is continuous on compact density/POVM domains and homogeneous in A. The upper concave envelope is over all density atoms; restricting to pure atoms would be unjustified. Its graph convex hull is compact. Caratheodory gives r^2+1 atoms on a rank-r face; a dependence-preserving zero-value weight direction removes one atom. The common barycenter is shared across y. This proves attainment with at most r^2 outcomes per label and finite quantum receivers, without an efficiency claim.

The homogeneous envelope hypographs are closed convex cones. At A=0, bounded normalized values give closure; positive definite A with sufficiently negative height gives interior. The shared point A_y=rho=I/d1, height -1 is strictly feasible. Finite-dimensional conic Slater duality applies to the finite-valued primal and gives an attained dual. Majorants must hold for every density matrix. Slack may be added positively to one multiplier to make their sum scalar. Contact and spectral conditions are exactly the nonnegative defects in weak duality.

The causal tester proposition derives T_j,yz from a positive congruence of the physical circuit state and partial trace. The physical input marginal is the transpose of the coefficient Gram convention. The sum over decisions equals Xi_y; its I2 marginal is the initial physical state. No normalized-Choi dimension factor is omitted.

## Primary Section 17: equal-prior hierarchy (module 84)

The second-moment substitution gives W_yy=a(I-dS), W_yz=-a(I-dS)/(d-1). The centered filtered-swap inequality uses `I-dS=2Pi_--(d-1)S`, the old exact norm `||K||_1=f^2`, and two explicitly proved trace/fidelity inequalities. Nonzero equality forces scalar factors, including the singular case.

The classical upper allows arbitrary second-call reference testers through T_z<=B, trB=1; contraction with the first effect A yields a bound by the operator norm of I-d A/trA. The reset upper maximizes positive and negative parts on the separately recorded second labels, sums to a trace norm and applies the centered bound branchwise. In both cases `sum_yh tr A_yh=d` is a normalization identity, not a hypothesis-dependent branch count.

The unrestricted upper sums the positive parts under the physical Xi_y normalization. Matching strategies are, respectively, two identical pure inputs; two independent normalized Bell pairs followed by label-dependent symmetric/antisymmetric reference readout; and a normalized antisymmetric two-input state. Their qubit probabilities are evaluated explicitly. Equal binary priors are not uniform weights on seven individual devices. The latent device is selected once, not redrawn.

## Retained mathematics

All v90 proof paragraphs and labels are preserved. The local chain retains its full channel remainder and binary signal error before amplification. A fixed tube has fixed-object constants; Q remains a worst-formal-path resource. The biased-prior hierarchy remains separately proved. Structural and wider analytic claims are not premises.

## Verification scope

`reset_variational_check.py` and `equal_prior_check.py` check finite exact Gram identities, support-inverse realizations, rectangular maps, complex transpose controls, qubit payoffs, event probabilities, diagonal equality cases and special primal/dual values. They do not test a continuum of dual constraints or prove the universal theorems. All 32 suites are scheduled by the production build in ordinary and optimized modes; only its actual receipt reports success.


## General classical-versus-quantum receiver criterion

Primary Section 15 additionally proves Theorem `classicalroof91`: complete classical readout is exactly the same common-barycenter problem with atoms restricted to rank-one density matrices. A complete first measurement can be spectrally refined without loss, and a rank-one Gram factor carries only a known receiver state; these give both operational directions. Compact graph convexification and the same strictly feasible hypograph dual give attained classical primal and dual optima. Corollary `gapcertificate91` then gives necessary and sufficient certificates of a strict retained-receiver advantage, and all-density dual contacts characterize equality. This extends the R60 breadth response to an exact general comparison criterion, not merely an evaluated example.

The finite receiver dimensions refer to retained registers at the recording cuts, not to all temporary workspaces of a selected implementation of an instrument. The dual majorizations remain universal requirements and are not checked by sampling.
