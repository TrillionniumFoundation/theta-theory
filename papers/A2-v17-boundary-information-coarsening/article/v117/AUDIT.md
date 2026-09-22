# Proof, literature and preservation audit — A2 v117

## Proof dependencies and adversarial checks

**Sharp conductor.** The evaluation kernel has rank n-c, negative summands, and total degree -n; hence a_max <= c+1. H^1 of its twist gives the exact multiplication obstruction. Fibrewise surjectivity is promoted to a vector-bundle surjection before arbitrary base change. The full-series exception k=d is stated only as a cokernel assertion for n=d-1; saturation requires n>=d. The boundary monomial verifies failure of the actual cokernel comparison, not just of an intermediate sufficient proof.

**Curves.** The normal-generation hypothesis fills W^2. A base-point-free pencil fills subsequent double-vanishing degrees; the first normal layer is filled by a unit on D. Each invoked H^1 is included explicitly. The numerical bound gives deg L(-D)>=2g+1 and deg L(-2D)>=2g-1. Positive-genus sharpness is not claimed.

**Universal hyperplane quotient.** The radical of beta(b,c)=phi(bc) is the kernel of a split map from the subalgebra to the base line, and associativity makes it an ideal. This proves rank and arbitrary base change on nonreduced bases. The converse uses the fact that no nonzero ideal of a rank-two algebra can lie in its scalar line. On unit frames, quadratic residual entries represent the subalgebra condition scheme-theoretically; insertion of the unit and closure modulo the residual ideal prove equality in every higher degree. Changing the chosen unit changes neither the subalgebra nor its conductor. No generic-flatness or reduced-point argument replaces these steps.

**All fixed multiplicities.** Idempotent quotient ranks are locally constant on every test scheme. They give open/closed Hilbert components, not just a point classification. A local length-two quotient has basis 1,z and relation z^2=uz+v. The recurrence proves its exact equations. The two-factor case is C[x,y]/(x^r,y^s). Generating lines give A^1 and G_m, respectively. Exact primary, length and nilpotency assertions follow from the displayed Artin complete intersections. The Grassmannian cohomology ring and Schur/Pieri calculation are classical, clearly attributed.

**Moving contacts.** Nested divisors on a smooth connected projective curve are Sym^2 C times Sym^(d-2) C, including families by monic division/Cartier divisor subtraction. The finite divisor-addition map is flat because its smooth source and target have the same dimension; the generic degree is binomial(d,2). The actual failure scheme, rather than merely its normalization, is an open projective-line bundle. Nonreduced fibres do not imply nonreducedness of the total scheme.

**Noncurvilinear test.** In C[x,y]/(x^2,y^2) the hyperplane residual row is (-2ab,-b^2,0). Its ideal is (ab,b^2)=(b) intersect (a,b)^2. Thus no absence-of-embedded-primes claim is extended from the curvilinear theorem to arbitrary finite algebras.

**Three-planes.** Polarized Cayley–Hamilton gives total-degree truncation over the coefficient ring. Haiman's theorem supplies the deep equality of the alternant ideal powers with the intersection of diagonal powers. It is not proved by pointwise interpolation, and it is not asserted for arbitrary embedding dimension or nonreduced contacts.

**Etale primary descent.** The orbit product has canonical descent data as an invertible ideal. Reducedness descends and the image of one prime divisor is irreducible. Only after this identification are powers and intersections descended. Regular-local factorization proves primary powers and no embedded primes, including braid intersections.

## Exact external comparisons

- Sarah Arpin, Sebastian Bozlee, Leo Herr and Hanson Smith, *The Scheme of Monogenic Generators I: Representability*, arXiv:2108.07185v2 (11 May 2022). Proposition 3.6, Definition 3.12 and Proposition 3.14: monogenerator/index-form and polygenerator-minor constructions. The generator functor and index form are not claimed new. Source: https://arxiv.org/pdf/2108.07185 .
- Mark Haiman, *Hilbert schemes, polygraphs, and the Macdonald positivity conjecture*, JAMS 14 (2001), 941–1006; arXiv:math/0010246v2. Corollary 3.8.3, printed preprint p.20: J^q equals the intersection of pair-diagonal qth powers. This is an essential input, not a result of the present paper. Source: https://arxiv.org/pdf/math/0010246 .
- Darij Grinberg, *A basis for a quotient of symmetric polynomials*, arXiv:1910.00207v2 (24 September 2021). Theorem 2.7 and following discussion: rectangular Schur basis and Grassmannian cohomology specialization. Source: https://arxiv.org/pdf/1910.00207 .
- Mark Green and Robert Lazarsfeld, *On the projective normality of complete linear series on an algebraic curve*, Invent. Math. 83 (1986), 73–90. The author-hosted scanned p.73 was read visually; it explicitly recalls normal generation in degree at least 2g+1. Source: https://www.math.stonybrook.edu/~roblaz/Reprints/Green.Laz.Proj.Norm.Alg.Curves.pdf .
- E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102. Publisher TOC/metadata and nominal PDF/ePDF paths did not deliver the complete theorem pages. **Full comparison unverified.** No theorem about anticipation or non-anticipation is asserted. The inherited accessible Ballico 1996 comparison is preserved with its precise theorem references.

The scholarly comparison is not exhaustive priority certification. Failed access is not positive novelty evidence. The AI-assisted revision does not represent any journal's editorial decision.

## Source and test evidence

All 28 v116 TeX sources are copied byte-for-byte to `history/v116_source` and hashed. The complete reading edition preserves every old part label. Independent earlier mathematics stays in that complete edition and the original historical tree; the primary reading edition is not a destructive replacement.

`verify_revision.py` checks exact residual/Groebner equivalence for r=3,...,9, Artin lengths, vanishing of all monomials in the claimed nilpotency degree, nonvanishing of the top power and its Catalan coefficient. It checks 112 modular conductor identities, 28 uniform-boundary examples, 268 multiplicity partitions and the noncurvilinear primary intersection. The v116 and inherited v115 diagnostics rerun in an isolated temporary directory.

These are finite regression checks. Universal statements rest on the manuscript proofs and on the explicitly cited classical theorems. The actual PDF receipt records real compilation, references, box warnings, source and output hashes; none of these is a proof certificate.
