# Primary-source comparison — General Theta Foundations I, Revision 65

Checked: 29 September 2026. This is an author-side theorem comparison, not an independent priority opinion. The unmodified v64 comparison is retained in `predecessor-v64-audit/LITERATURE_AUDIT.md`; the earlier comparison remains in `predecessor-audit/LITERATURE_AUDIT.md`. The cited versions below, rather than remembered titles, govern the current discussion.

## The current Chen–Wu comparisons

**Z. Chen and J. Wu, The State Cost of Classical Simulation of One-Way General Quantum Finite Automata, arXiv:2604.07058v2, 27 August 2026.**
Primary text: https://arxiv.org/html/2604.07058v2.

Definition 2.1 asks for equality of strict-cutpoint languages, permitting a different simulator cutpoint. Theorem 3.2 supplies an `n^2+1` upper bound; Theorem 4.4 and Corollary 4.5 give the matching worst-case value for `n>=2` (the one-state exception is separate). Proposition 3.1 explicitly multiplies the represented zero-cutpoint output by a positive length-dependent factor. The current title differs from the earlier title quoted in r41.

This result settles its state-cost question and is not presented as an open problem solved by our revision. Its correctness criterion is sign preservation. Theorem `matrixspace65` instead requires calibrated mean approximation of every numerical matrix target, with legal output on each run and complete private configurations charged. Neither the exact cutpoint theorem nor its attenuation step supplies that calibration. Conversely, our mean-output obstruction is not a lower bound for unrestricted cutpoint-language equivalence.

**Z. Chen and J. Wu, On the Simulation Cost of Quantum Finite Automata, arXiv:2605.10682v1, 11 May 2026.**
Primary text: https://arxiv.org/html/2605.10682v1.

Theorem 11 treats one-way hybrid automata with `c` classical states and quantum dimension `q`, for `c,q>=2`, obtaining order `cq^2` (displayed bounds `cq^2-1` and `2cq^2+6`). Theorem 14 and Corollary 15 give order `n^2` for the measure-once model. These are strict-cutpoint simulation costs, not whole adaptive transcript error bounds. Their prepare–test and sign-pattern lower-bound techniques are relevant antecedents, but preserved signs alone do not control the amplitudes needed in the centroid lower proof.

Section `35-cutpoint-comparison.tex` gives a complete elementary attenuation construction and the reverse, margin-sensitive implication from trace-norm approximation to a threshold decision. This is a clarification of the noninterchangeable resources, not a claim that attenuation or sign-preserving stochasticization is new.

## Positive realization, weighted automata, and precision

**L. Benvenuti and L. Farina, A tutorial on the positive realization problem, IEEE Transactions on Automatic Control 49 (2004), 651–664, DOI 10.1109/TAC.2004.826715.**
The inherited author-manuscript comparison identifies Theorem 2 and equation (2), concerning invariant polyhedral cones and exact stationary positive realization. It explains why low real linear dimension does not imply small positive state count. It is not a finite-bit, horizon/accuracy-dependent one-pass theorem. The duplicate `BF64` bibliography entry is removed in the new revision only; all active citations use `BF04`.

The earlier Ambainis–Watrous comparison concerns two-way quantum/classical language recognition (arXiv:cs/9911009), and the Panduranga Rao–Vinay comparison concerns complex-weighted automata (arXiv:quant-ph/0701144). Their input access, weights and output criteria are kept distinct from a one-pass nonnegative finite register with a legal numerical decoder. We retain these comparisons without treating them as an exhaustive current QFA survey.

## Standard quantum-information input and the constructive theorem

**J. Watrous, The Theory of Quantum Information, Cambridge University Press, 2018.**
Primary author text: https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf; Corollary 3.40, printed page 168.

Trace-norm contractivity of a positive trace-preserving map is classical. Applied to the direct-sum instrument channel, it yields the summed branch estimate used in `lem:instrumentcontraction65`. The manuscript includes the elementary Jordan-decomposition proof, so its zero-outcome convention and unhalved trace norm are explicit.

Density-matrix propagation, the hybrid argument for sequential errors, integer rejection sampling, and adding a scalar diagonal buffer after approximate matrix rounding are not claimed as new general principles. The construction in Sections 32–33 specifies a common-denominator positive update with a proved uniform error, exact rational branch sampling, bounded private bit-space, and a complete proof for adaptive classical control without an outcome-probability floor. It is a finite-horizon numerical simulation theorem, not an extension of the finite-response-quotient classification to disturbing quantum instruments. It does not simulate arbitrary external entangled memory and does not assert total variation between binary encodings of approximate and exact matrices.

The class is a fixed finite Gaussian-rational Kraus description and a fixed rational initial state. It is not every rational superoperator by an unproved rational-factorization inference. The code accepts this explicit description and validates completeness exactly. The classical trace-norm input alone gives no lower bound for an arbitrary noisy channel family; the sharp corollary requires an expanding unitary subsystem and the legal numerical matrix interface.

## Spectral inputs: precise uses and constants

**M. E. Pinochet Lobos and C. Pittet, The exact convergence rate in the ergodic theorem of Lubotzky–Phillips–Sarnak, arXiv:1805.05261v2, 8 March 2019.**
Primary version: https://arxiv.org/html/1805.05261v2.
Theorem 1.1 restates the original LPS freeness and one-step spherical norm; Theorem 1.2 gives exact radial sphere/ball averages. The bibliography now makes that distinction explicit. The six norm-five Bloch rotations have imported norm `sqrt(5)/3`; no numerical finite-harmonic test certifies it.

**Y. Benoist and N. de Saxcé, A spectral gap theorem in simple Lie groups, arXiv:1405.1808, Theorem 1.2.**
Primary version: https://arxiv.org/pdf/1405.1808.
The adapted algebraic-support theorem, or the retained Bourgain–Gamburd `SU(d)` theorem, supplies the full group gap for the explicit rational adjacent-coordinate unitary family in each fixed dimension. Symmetrization and laziness use actual commands, including the supplied identity. Peter–Weyl transfers the group estimate to the action off all invariant functions. The least-orbit cap theorem is an inherited manuscript result.

The new high-dimensional examples use rational unitary matrices. They are not the six rational LPS Bloch matrices: the unitary lifts of the latter are algebraic and need not be Gaussian rational. No dimension-uniform or numerical Benoist–de Saxcé/Bourgain–Gamburd constant is asserted. The upper algorithm does not need a spectral constant.

## Retained analytic comparisons and limits of this audit

The Polyanskiy–Wu entropy/Wasserstein comparison, the van Erven–Harremoës Rényi-affinity inequality, classical free-tree radial recurrences, Parzanchevski–Sarnak arithmetic gate covering, and Blackwell/Cohn/Grabchak–Sonin nonhomogeneous-tail theory retain their prior credits. The exact versioned manuscript references and predecessor comparisons remain available.

This audit is targeted. It does not exclude every equivalent formulation in finite-precision quantum trajectories, numerical filtering, automata, positive realization, quantization, or streaming complexity. No independent human priority opinion was commissioned or received in this revision. The claimed package is the written and implemented theorem chain with these precise interfaces, not an external novelty clearance or a guaranteed journal decision.
