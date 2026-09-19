# A2 v88: closest predecessors and the scope of the new assertions

This audit accompanies the response to the v87 report at commit `976d23ef269126e68dd90c4c9d3184ee67ff0b54`. It distinguishes inherited tools from the assertions proved in the new paper. It is a targeted audit of the referee's closest comparisons, not a claim that a finite search establishes universal priority.

## Rational interpolation and normalization

**Van Barel and Bultheel (1990),** *A new approach to the rational interpolation problem: the vector case*, Journal of Computational and Applied Mathematics 33, 331--346. Publisher record: DOI `10.1016/0377-0427(90)90056-6`.

Vector rational interpolation and its linear solution spaces precede this paper. The equation N_P a=b_P is not claimed as a new linearization of interpolation. Theorem 1.1 and Lemmas 2.1--2.2 identify the residual kernel with the common factor of a simultaneously diagonalized stochastic polynomial model, realize its nonzero directions as positive fixed-channel fibres, and retain the diagonal normalization error in a one-sided observation modulus. Proposition 2.3 gives a worst-case count, not a claim that every vector rational curve requires that many nodes. Bibliographic data and subject scope were checked against the publisher record.

## Generalized eigenvalue and matrix-polynomial perturbation

**Chu (1987),** *Exclusion theorems and the perturbation analysis of the generalized eigenvalue problem*, SIAM Journal on Numerical Analysis 24, 1114--1125, DOI `10.1137/0724073`.

**Chu (2003),** *Perturbation of eigenvalues for matrix polynomials via the Bauer--Fike theorems*, SIAM Journal on Matrix Analysis and Applications 25, 551--573, DOI `10.1137/S0895479802217928`.

The publisher descriptions explicitly concern generalized-eigenvalue exclusion/conditioning and matrix-polynomial extensions including multiple eigenvalues. Therefore a cluster argument through repeated eigenvalues cannot by itself support a novelty claim here. Lemma 2.4 gives the particular elementary resolvent proof needed by this article, with algebraic multiplicity bookkeeping. The additional theorem concerns an unknown normalizing polynomial recovered from probability matrices, arbitrary closed-model competitors, and the additive conversion `delta(kappa^{-1}+tau^{-1})`. The comparison of broad scope is based on the publisher abstracts and bibliographic records; it is not a claim to have audited every proof in both Chu papers.

**Higham, Mackey and Tisseur (2006),** *The conditioning of linearizations of matrix polynomials*, SIAM Journal on Matrix Analysis and Applications 28, 1005--1028, DOI `10.1137/050628283`.

The author-hosted manuscript, including its simple-eigenvalue conditioning formula in Theorem 2.1, was inspected. That formula depends on the polynomial derivative and compares a specified polynomial problem with its linearizations. The present paper neither overturns nor replaces that theory. It first reconstructs the missing projective normalization and then proves the required structured coefficient estimate. A separate resolvent/cluster proof, rather than a simple-root derivative denominator, gives the stated cross-component-collision result. Author copy: `https://eprints.maths.manchester.ac.uk/71/1/paper8.pdf`.

## Structured and rational eigenvalue problems

**Tisseur and Higham (2001),** *Structured pseudospectra for polynomial eigenvalue problems, with applications*, SIAM Journal on Matrix Analysis and Applications 23, 187--208, DOI `10.1137/S0895479800371451`.

**Su and Bai (2011),** *Solving rational eigenvalue problems via linearization*, SIAM Journal on Matrix Analysis and Applications 32, 201--216, DOI `10.1137/090777542`.

These are direct predecessors for structured coefficient perturbations and rational eigenvalue computation, respectively; bibliographic data and stated scope were verified from the publisher records. The v88 residue construction uses the classical inverse-pencil resolvent. Theorem 3.2 additionally uses the exact projective two-clock shift before comparing pencils, proves an observable zero set and semicontinuity, and establishes an inverse bound in categorical observation norm. No claim is made that residues, structured pseudospectra or rational linearization themselves are new.

## Robust latent decomposition

**Bhaskara, Charikar and Vijayaraghavan (2014),** *Uniqueness of tensor decompositions with applications to polynomial identifiability*, Proceedings of Machine Learning Research 35, **742--778**. Primary proceedings page: `https://proceedings.mlr.press/v35/bhaskara14.html`.

The proceedings abstract and record were checked for robust tensor uniqueness and quantitative Kruskal-type identifiability. The present target is an unordered aggregate root multiset, not individually stable rank-one factors. Cross-component collisions can preserve this multiset inverse while destroying individual factor uniqueness. The paper now makes that comparison explicitly, alongside Allman--Matias--Rhodes and Bonhomme--Jochmans--Robin; it does not claim a stronger general tensor-decomposition theorem.

## Singular inference

The retained references to Donoho, Cai--Low, Dufour and Ho--Nguyen acknowledge the classical modulus/inference connection, weak identification and mixture singularities. Lemma 5.1 and the testing reductions are not novelty claims. The asserted contribution is the model-specific inverse modulus, its explicit constructive estimator, and exact least-favourable paths which prove the same sharp order on the new observable eta classes. These paths do not classify every local singular stratum of a general finite mixture.

## Assertion ledger

| Assertion in v88 | Status relative to the cited tools |
| --- | --- |
| Linear rational-interpolation equations | Classical mechanism, credited |
| Gcd/nullity formula for this stochastic projective model and its positive exact fibres | Proved in Lemmas 2.1--2.2 |
| Worst-case 2d+1 design count for every fixed capacity | Proved in Proposition 2.3; not a universal minimum |
| Resolvent exclusion, homotopy and multiplicity matching | Classical mechanism, fully specialized in Lemma 2.4 |
| Additive normalization/channel observation modulus | Proved in Theorem 1.1 |
| Canonical residue condition, zero set, semicontinuity and exact-shift inverse | Proved in Theorem 3.2 |
| Direct reconstruction with the observable affine modulus | Proved in Theorem 4.1 |
| Minimax and honest-diameter order on eta signal classes | Proved in Theorems 5.2 and 5.4 using Lemma 5.3 |

The accompanying response submits these assertions and their proofs for adversarial mathematical review. Verification of citations is not a proof of novelty, and numerical diagnostics are not a substitute for the written proofs.
