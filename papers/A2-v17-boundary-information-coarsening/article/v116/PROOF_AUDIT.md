# Proof audit — A2 revision 116

This is a dependency and assumption audit, not a certificate of correctness.

## New proof chain

1. **Pencil multiplication (`lem:conductor-pencil`).** A base-point-free subspace U of V_n contains two coprime binary forms. The exact syzygy kernel proves U V_t = V_(n+t) for t >= n-1. The endpoint t=n-1 is handled separately.
2. **Conductor reduction (`thm:conductor-reduction`).** Hypotheses: length d, n >= 2d-1, generating A, m >= 2. Products with two conductor factors fill I_D^2(mn), since 2n-2d >= n-1. Vanishing H^1(O(n-2d)) and a unit in A fill I_D/I_D^2. The resulting surjection is between vector bundles and survives arbitrary base change. A locally split symmetric-power quotient identifies coherent cokernels. No flatness of the cokernel is assumed.
3. **Power-basis presentation (`lem:contact-power-basis`).** On the open frame bundle A=<a,av>, a is a unit. Target multiplication by a^(-m) is invertible. Cayley–Hamilton holds over the entire coefficient ring, giving ideal stabilization for m >= d-1; the earlier-degree maximal-minor ideal is zero. Equality of ideals is not inferred from pointwise ranks.
4. **Primary formula (`thm:contact-factorization`).** Taylor expansion gives diagonal jet weights 1,c_i1,...,c_i1^(d_i-1). Divided differences prove the confluent Vandermonde with exact normalization. The formula is a polynomial identity even when first jets or value differences vanish. Each labelled factor is a smooth rank-one Schubert divisor; rank zero is excluded by generation. Distinct prime-factor exponents give the complete primary decomposition, with no embedded primes.
5. **All coranks.** The local minimal polynomial has exponent ceil(d_i/e_i), using e_i=d_i in the constant case. Repeated eigenvalues require an lcm, hence the maximum local exponent, not their sum. The global rank is min(m+1, degree of that lcm).
6. **Nilradical layers (`thm:contact-layers`).** These follow from an explicit colon-ideal calculation. The local index is the maximum exponent of the factors actually vanishing at the point. The quotient formula is local, with a specified generator; no untwisted global splitting is asserted. Braid intersections are not called normal crossings.
7. **Multiplicity-stratum descent (`cor:contact-multiplicity-strata`).** The labelled support cover is finite etale with deck group product S_(r_e). Component orbits are indexed by one multiplicity or an unordered pair of multiplicities. Descended components can have intersecting local branches; their smoothness is not asserted.
8. **Moving normalization (`thm:moving-normalization`).** Marking a length-two subdivisor is finite over the divisor parameter. On frame charts the marked incidence is exactly g=hq, v=lambda+hw and is smooth. Its image is the complete nonprimitive-element locus. A generic unique equal pair gives multiplicity one and birationality. The Cartier total scheme is therefore integral, even though its fixed-contact fibres can be nonreduced.
9. **Singular support (`prop:moving-singular-test`).** A unique preimage and injective normalization differential imply equality of the finite local rings by two applications of Nakayama. The differential kernel is calculated explicitly from q*dot h+h*dot q=0 and dot lambda+w*dot h+h*dot w=0. This yields h|q r and constancy of w r mod h. Multiple preimages are separately singular. The Jacobian ideal gives the full singular scheme on each frame chart.

The new proof chain does not invoke any statistical appendix, the old quadratic excess classification, or a claim about the old hyperplane primary ideal.

## Expanded inherited arguments

The new hyperplane diagonal matrix, residual interval computation, confluent Hankel-radical lemma, and equivariant associated-point lemma expand the exact points requested by R115. All original theorem and proof blocks remain present. Classical matrix normal forms retain their explicit attribution.

## Assertions intentionally not made

The contact-containing subseries family is not identified with the unrestricted ambient Grassmannian. The old quadratic excess theorem is not an all-associated-prime theorem. The original hyperplane nilpotency lower bound is not claimed exact. Finite algebra tests do not establish the universal theorems. An inaccessible historical source does not establish originality.

## Finite evidence

`verify_revision.py` uses modular Gaussian elimination at prime 1009 and exact SymPy polynomial arithmetic. It checks 272 global lifted-series ranks and conductor ranks, seven symbolic determinant formulas, three normalization examples, the transverse derivative of the smooth-total/triple-fibre example, and 1,287 colon-exponent cases. `build.sh` separately reruns the inherited v115 suite in a temporary copy, leaving the reviewed source directory unchanged.
