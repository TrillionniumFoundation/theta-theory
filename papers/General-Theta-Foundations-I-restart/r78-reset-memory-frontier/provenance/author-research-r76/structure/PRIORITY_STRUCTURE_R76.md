# R76 structural literature and contribution audit

This is an author-team research note. It is not an external referee report or an exhaustive priority clearance.

## Primary sources actually examined

- **Olivier Vu Thanh, Nicolas Gillis and Fabian Lecron**, *Bounded Simplex-Structured Matrix Factorization: Algorithms, Identifiability and Applications*, IEEE TSP **71** (2023), 2434–2447, [DOI](https://doi.org/10.1109/TSP.2023.3289704), [arXiv v2](https://arxiv.org/abs/2209.12638v2), [primary PDF](https://arxiv.org/pdf/2209.12638), [institutional metadata](https://orbi.umons.ac.be/handle/20.500.12907/45976). Read the model definition and Section IV-C, Theorem 3 and proof. Complementary slacks share a factor; sufficient identifiability uses a sufficiently scattered condition. That mechanism is prior work. The author PDF and institutional record were accessible; the publisher redirect failed. Our specific centered-family criterion does not replace their general sufficient condition.
- **Nicolas Gillis**, *Sparse and Unique Nonnegative Matrix Factorization Through Data Preprocessing*, JMLR **13** (2012), 3349–3386, [primary journal PDF](https://jmlr.org/papers/volume13/gillis12a/gillis12a.pdf). Read the geometric normalization in Section 1.1 and Section 4.3: Lemma 27, the nested-square Example 2, and Theorem 29. Threshold attainment and finite boundary factorizations already belong to this theory. The R76 result does not claim those general ideas as new; it provides its explicit all-n three-piece boundary and equality classification under different coefficient constraints.
- The inherited R75 representation, nonnegative-rank and nonnegative-factor support references remain controlling background. The rank-one zero-support argument used after the new extremum is elementary and standard; novelty is not assigned to that argument.

Both search systems were used for targeted queries about centered nonnegative singular matrices, shared stochastic factors and permutation-character realizations. These searches did not locate the same weighted common-null-vector inequality or the same three-piece formula, but this limited search is not proof of absence in the literature. The underlying field is broad; independent specialist assessment is still needed.

## Mathematical increment and precise quantifiers

The weighted inequality holds for every real triple v,c,d satisfying the displayed two-outcome inequalities, without assuming symmetry or a positive factorization. Its equality case forces one negative coordinate and equal other coordinates. The proof uses the inherited one-outcome estimate, an elementary range bound on the sum of squares, a strict concave endpoint comparison, and arithmetic–geometric mean. Those elementary ingredients are not claimed as novel separately.

The coefficient synthesis theorem quantifies over every n≥5 and every p in (0,1), a>0. It identifies the parameter pairs for which some bounded coefficient matrix and probability column have deficient joined rank; it proves that the same parameter pairs admit a nonnegative factorization of width n−1. It does not assert that every admissible pair away from the boundary has nonnegative rank n−1. On the middle transition curve, it proves uniqueness of the matrix pair and of the normalized factors up to relabeling. On the lower-mean transition it retains the explicit allowed weight family.

The S_n corollary covers all feasible means, both contrast signs and the constant endpoint. It reuses the established subgroup-index estimates and exact pure-start formula; these are not re-proved or repackaged as new. The mean p is a group-averaged terminal probability. It is not the unknown-parameter prior from the original decision problem. The general arbitrary-prior, arbitrary-M squared-sign risk frontier remains open.

## Additional proof challenge

A deterministic floating differential-evolution search over arbitrary signed normalized null vectors was used during development for n=5,6,7,10. It agreed with the analytical boundary in the sampled cases. This search did not establish the theorem, equality classification or priority. The final diagnostic suite instead records finite exact rational identities and examples; the universal proof is the written argument.
