# v121 theorem dependencies

## New primary chain

`lem:coefficient-symbolic` (polynomial coefficient contraction) + `lem:minor-symbolic-order` (Schur complements; classical generic determinantal primeness/normality) -> `thm:weighted-primary` (all matrix sizes, primary exponents and irredundancy).

`thm:loewy-factorization` (retained full linear-plus-quadratic Fitting presentation) + exact module equality `[A,tB,t^2 c] = [A,tI]` on the first-order-spanning locus + weighted primary theorem -> `thm:universal-primary-flag`.

Intrinsic image-subspace incidence -> `thm:flag-resolution` (normal embedded supports, projective smooth resolutions, all fibres).

Direct cubic multiplication determinant + explicit smooth parameter open + direct local parameters `(t,f)` -> `thm:elliptic-boundary` (no arbitrary specialization of primary components). Classical Hesse Weierstrass coefficients only normalize j; the local ring and nilradical sequence are derived here. Smoothness of the elliptic family + the exact nilradical sequence -> `cor:elliptic-family` (flatness).

`prop:universal-conductor-flag` supplies the companion conductor kernel in arbitrary embedding dimension. Its `(1,3,3)` specialization has constant conductor rank one; the extra quadratic restriction data locate the varying embedded support.

## Descent and absence of circularity

`lem:frame-primary-descent` uses only a Zariski GL-frame trivialization, contraction, flat intersections and primary ideals. The affine portion of `thm:loewy-primary` proves all displayed algebraic ideal identities. `cor:loewy-primary-descent` uses those affine identities, defines global ideal sheaves, and verifies the Grassmannian associated points. The global conclusion of `thm:loewy-primary` then cites that corollary. No part of the corollary assumes the global statement it proves.

## Retained theorem chain

All v120 core inputs remain in `core.tex`. Coefficient-ring codimension stabilization, its sharpness family, codimension-two Fitting presentation, proper quotient-algebra incidence, the full `(1,2,2)` primary theorem, higher-contact embedded examples, relative cohomological conductor comparison, and global section realization retain their original hypotheses and conclusions. The complementary polar, residual, wall, orientation, and statistical proofs remain in `paper.tex` but are not needed by the primary chain.

## Scope and external interfaces

The universal primary theorem classifies the stated corank-one, first-order-spanning open only. It does not classify all higher projection coranks of an arbitrary cube-zero algebra. The whole `(1,2,2)` class is classified separately, without omitting its extreme-corank stratum. Primary decompositions are not asserted to commute with arbitrary nonflat specialization; raw Fitting equations do commute with substitution, and the elliptic family is proved independently.

No A1 input and no A3/downstream use is assumed. A2 is a repository identifier, not a theorem or a significance argument. Any downstream application must check the explicit algebra, generating and regularity assumptions. The unread Ballico 1993 article is a priority-comparison requirement, not an unstated mathematical lemma.
