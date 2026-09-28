# Targeted literature comparison — Revision 56

This is a theorem-level author-side comparison, not an exhaustive or independent priority clearance. The retained v55/v54 bibliography and audits remain available. The following primary sources were inspected for the new arguments.

## Classical stochastic-semigroup structure

Peter Flor, *On groups of non-negative matrices*, Compositio Mathematica 21 (1969), 376–382. Primary full text: https://www.numdam.org/article/CM_1969__21_4_376_0.pdf . Theorem 2 describes nonnegative idempotents; Theorem 3 describes bounded nonnegative matrix groups via a permutation structure. These hypotheses match the finite stochastic idempotent and bounded corner group used in the paper. Flor explicitly cites Doob for the stochastic special case and the preceding work of T. C. Brown (*On clans of non-negative matrices*, Proc. Amer. Math. Soc. 15 (1964), 671–674) and Š. Schwarz (*On the structure of the semigroup of stochastic matrices*, Publ. Math. Inst. Hungar. Acad. Sci., Ser. A 9 (1964), 297–311). The classical ingredients are not claimed as new.

The application in the article forms the joint physical/stochastic closure so that every sandwiched limiting element remains subject to the original closed error inequalities for all seed/query pairs. The new physical-equivariant reduction averages the kernel above the physical identity and replaces labels by its orbits. This preserves width, legal decoder values and randomized initialization while ensuring that the action factors through the physical group. The article proves these steps explicitly rather than claiming a new general compact-semigroup structure theorem or a replacement for Rees theory.

## Neutral-letter advice and Ramsey extraction

Nathanaël Fijalkow and Charles Paperman, *Monadic second-order logic with arbitrary monadic predicates*, arXiv:1709.03117 (2017), https://arxiv.org/abs/1709.03117 . Their Theorem 10 proves the Crane Beach property for advice-regular languages: a neutral-letter language in the stated advice model is regular. Their proof uses common-length prefix/suffix tests and bounded deterministic state distinctions. This is a direct conceptual predecessor, not merely unrelated automata literature.

F. P. Ramsey, *On a problem of formal logic*, Proc. London Math. Soc. (2) 30 (1930), 264–286, DOI 10.1112/plms/s2-30.1.264, supplies the finite coloring theorem. Ramsey homogeneous-set extraction is classical. The stationarization statement here has a different quantitative object: one fixed stochastic label bound, a closed convex numerical error tolerance, arbitrarily large intermediate registers and eventual approximate returns in a topological monoid. The proof colors the actual tuple of endpoint kernels, keeps a legal stochastic representative, and folds the neutral representative into the terminal decoder without an idempotence assumption. Neither source by itself supplies those exact same-width/same-error conclusions. This comparison does not exclude equivalent results elsewhere in weighted or positive-realization formalisms.

## Nonabelian spectral gap

Jean Bourgain and Alex Gamburd, *A spectral gap theorem in SU(d)*, J. Eur. Math. Soc. 14 (2012), 1455–1511, DOI 10.4171/JEMS/337; primary article https://ems.press/journals/jems/articles/11408 and preprint https://arxiv.org/abs/1108.6264 . The algebraic dense-generator hypotheses were checked against the SU(2) lifts of the displayed rational SO(3) matrices. The 2012 theorem, not a free-generator hypothesis from an earlier special case, is the imported input. The width theorem additionally proves cap quantization, a uniform executable contraction estimate, an all-profile occupation bound and a common-row polytope upper construction. It does not claim an explicit numerical spectral-gap constant or remove the stated logarithmic lower loss.

## Nonnegative rank and existential-real complexity

Yaroslav Shitov, *A universality theorem for nonnegative matrix factorizations*, arXiv:1606.09068, revised 2018, https://arxiv.org/abs/1606.09068 . Theorem 2 states polynomial-time equivalence of the nonnegative matrix factorization decision problem and the existential theory of the reals. The article's hardness reduction uses rational input matrices but real nonnegative factors, deletes zero rows, normalizes rows and then normalizes factors into probability rows. It does not confuse rational-factor and real-factor questions or claim NP-completeness. The membership result is independently proved for the explicitly tabulated finite-group input. The broader compact matrix-input problem receives only this lower-complexity bound plus its retained termination theorem.

## Remaining priority and scope boundary

A conventional independent assessment should still compare the precise results with compact semigroup kernels, Markov representations, weighted series, approximate positive realization and numerical advice automata. Existing algorithms for rational matrix closures and real quantifier elimination remain credited as imported algorithms. A source-bound build, a repository revision number, and finite regression counts contribute no independent novelty evidence.
