# Nearest-source audit — A2 v116

Audit date: September 22, 2026. This record distinguishes inspected material from inaccessible theorem text. URLs identify primary sources; unsuccessful retrieval is not evidence of novelty.

## Ballico (1993): inspected first page, incomplete theorem comparison

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13. DOI: `10.1002/mana.19931630102`.

Publisher record: https://onlinelibrary.wiley.com/doi/10.1002/mana.19931630102

The publisher's first-page image was inspected directly:
https://onlinelibrary.wiley.com/cms/asset/121e4fb0-1492-43f2-8717-4513c267ae1f/mana.19931630102.fp.png

The page defines higher-order embedding properties using the restriction of a chosen series to finite schemes, with versions for curvilinear schemes and for all schemes, and generic/almost-everywhere variants. It is not a theorem-by-theorem account of pages 6–13. The full theorem pages were not obtained from the publisher routes checked. No theorem number, theorem hypothesis, or non-overlap assertion is invented for those pages.

| Source/result | Parameter space and variation | Map / degree | Scheme structure, coranks and primary layers |
|---|---|---|---|
| Ballico 1993, inspected definitions on p.5 | A variety, a line bundle and a series; finite schemes vary in the definition | Restriction to a length-controlled finite scheme; order of an embedding property, not by definition a symmetric multiplication degree | The inspected page is insufficient to determine the content of the later failure-locus theorems. Full comparison remains pending. |
| Present Theorem 11.1 | All hyperplanes in `V_4`, parameter space `P(V_4*)` | `Sym^m U -> V_{4m}`, every `m>=2` | Actual primary ideal, completed germ, exact nilpotency, all layers and normal cone |
| Present Theorem 12.1 | Open `Gr(s,H^0(O_Z(n)))`, `n>=2d-1`; relative flat divisors allowed | Original multiplication identified with multiplication in the finite residue algebra | Canonical cokernel isomorphism; all Fitting ideals; base change |
| Present Theorem 12.2 | Open residue-pencil Grassmannian, arbitrary multiplicity divisor, subseries codimension `d-2` | Every `m>=2`, explicit wall at `m=d-1` | Complete primary decomposition, all coranks, no embedded primes, full weighted local equations |

The difference between these displayed maps is a verified definitional distinction. It does **not** establish that Ballico's later theorems do not imply any of the present statements. A responsible theorem-level priority comparison still requires the complete source. The article states this limitation explicitly.

## Hankel/secant input

A. Conca, M. Mostafazadehfard, A. K. Singh and M. Varbaro, *Hankel determinantal rings have rational singularities*, primary manuscript:
https://arxiv.org/pdf/1709.05685

Inspected locations: §1, p.2, on Hankel determinantal ideals and reduction between catalecticant shapes; §2, p.3, especially (2.0.1), on the rational-normal-curve secant parametrization. These are the input used by the expanded length-two lemma. The rational-singularity theorem itself is not cited as if it were the radical computation. The manuscript supplies the length-two quotient and double-point pairing argument.

This source supplies classical reduced secant/Hankel geometry. It is not cited as a proof of the present degree-dependent maximal-minor primary ideal or the nilradical layers.

## Associated points and Fitting ideals

Stacks Project, precise algebraic statements used in the proofs:

- Tag 02M3, Lemma 10.63.3: associated primes under a short exact sequence, including the submodule inclusion. https://stacks.math.columbia.edu/tag/02M3
- Tag 00LC, Lemma 10.63.5: finiteness of associated primes of a finite module over a Noetherian ring. https://stacks.math.columbia.edu/tag/00LC
- Tag 02CE, Proposition 10.63.6: minimal support points and associated primes. https://stacks.math.columbia.edu/tag/02CE
- Tags 07Z8 and 07ZA: Fitting ideals, presentations and base change. https://stacks.math.columbia.edu/tag/07Z8 and https://stacks.math.columbia.edu/tag/07ZA

These are standard commutative-algebra inputs, not novelty claims. The equivariance step and the explicit multiplication applications are written in the article.

## Determinantal normal forms and confluent determinants

The v115 references to classical determinantal deformation/normal-form literature remain. The revision explicitly separates those normal forms from the new multiplication-specific ideal-spanning proof. The confluent power-basis formula in Lemma 12.3 is proved directly by a monic Newton basis and triangular substitution. Its elementary determinant factors are not presented as a newly discovered Vandermonde identity; the classification uses them after an exact reduction of the original multiplication cokernel and a global descent argument.
