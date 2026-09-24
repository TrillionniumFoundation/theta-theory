# Theorem-level literature and access record — revision 30

Access date: 24 September 2026. The entries distinguish original full text from abstract/metadata access. No unseen theorem number or universal non-overlap claim is supplied.

## 1. Esposito–Lemay–Denis–Dupont (2002)

*Learning Probabilistic Residual Finite State Automata*, ICGI 2002, LNCS 2484, pp. 77–91, DOI 10.1007/3-540-45790-9_7.

Publisher record and abstract: https://link.springer.com/chapter/10.1007/3-540-45790-9_7 . The record announces finite generation by residual stochastic languages and canonical minimal forms. The original full chapter was not obtained: publisher access is subscription-limited and the located institutional copy is restricted. Therefore this revision does not claim a proof-level audit of that chapter's exact minimality theorem.

The object is a stochastic language on finite words. The residual representation restriction is checked in the full later source below. The new article includes the 2002 paper as essential prior work and proves an explicit distinction in a finite language: at least 2^n residual states but a polynomial-size arbitrary positive realization. This is not an assertion that exponential representation gaps themselves have no predecessors.

## 2. Denis–Esposito (2006)

Inspected full arXiv:cs/0602093v1, https://arxiv.org/pdf/cs/0602093 . Relevant locations: Section 2, PDF p.9 (PRA definition); Proposition 16, PDF pp.22–23; Proposition 19 and its ensuing minimality remark, PDF pp.29–30.

The state language in a PRA must be an actual normalized residual. Proposition 16 identifies a unique inclusion-minimal residual generating set; Proposition 19 equates finite residual generation with existence of a residual probabilistic automaton. Stable shifts are part of the stochastic-language realization and support zeros are allowed. Its canonical residual minimum must not be equated with all-positive-state size.

`thm:prfa-gap` works in this precise generative setting, not merely an analogy: complete length-(n+2) word laws are prescribed and phase/query storage is charged. It proves that an all-positive realization can use non-residual state languages and be much smaller than every PRA for the same finite law.

## 3. Heller (1965) / Vidyasagar (2011)

Heller, *On stochastic processes derived from Markov chains*, Ann. Math. Statist. 36, 1286–1291, DOI 10.1214/aoms/1177700000. Vidyasagar, *The complete realization problem for hidden Markov models: a survey and some new results*, MCSS 23, 1–65, DOI 10.1007/s00498-011-0066-7.

The Vidyasagar publisher abstract was inspected: https://link.springer.com/article/10.1007/s00498-011-0066-7 . It explicitly situates stationary HMM realization in stable polyhedral-set theory and notes that finite Hankel rank is not sufficient. No claim is made to have completed the original Heller or full Vidyasagar proof audit during this revision.

Arbitrary positive state generators, rather than only actual residuals, belong to this classical realization tradition. Shift stability is not claimed new. The current theorem addresses equality with a known finite support-component rank profile on a fully specified clocked controlled array, through explicit affine enclosures and common normalized shifts. Its operational results include streamed exact query laws. This records a model distinction, not a blanket claim that no classical realization theorem implies a special case.

## 4. Gillis–Glineur (2010 preprint / 2012 publication)

Inspected full arXiv:1009.0880v1, https://arxiv.org/pdf/1009.0880 . Definition 1 specifies restricted nonnegative rank by equality of column spaces; Theorem 1 gives the nested-polytope relation. Published in Linear Algebra Appl. 437 (2012), 2685–2712.

The object is a static nonnegative matrix; arbitrary nonnegative factors are allowed in unrestricted rank, while restricted rank imposes a span condition. Time-compatible transitions are not a condition in this static factorization theorem. `prop:ranks` proves the normalized single-output equality K=rank_+, identifies the transposed affine-restricted convention, and separately requires all queried blocks to normalize. `thm:coherence` adds simultaneous positive-shift constraints. The reservoir gives actual nonsimplicial residual hulls with a coherent rank-saturating realization.

## 5. Incomplete sequential machines and filtered experiments

Reusch–Merzenich, *Minimal coverings for incompletely specified sequential machines*, Acta Informatica 22 (1986), 663–678, DOI 10.1007/BF00263650; Norberg, *Comparison of statistical experiments with filtered probability spaces*, Statistics & Risk Modeling 20 (2002), 1–28, DOI 10.1524/strm.2002.20.14.1.

These retained references are relevant to incomplete prescriptions and filtered comparison, respectively. Their original full-proof comparisons have not been completed here. Accordingly the article makes no detailed claim about an unseen unrestricted-minimality theorem in either source. The present core takes complete conditional laws as input; a partial almost-sure specification requires a chosen or optimized completion. It does not claim to replace general filtered-experiment theory.

## 6. Classical random-access exponent: Ambainis–Nayak–Ta-Shma–Vazirani

Inspected full arXiv:quant-ph/9804043v2 (25 November 1998), https://arxiv.org/pdf/quant-ph/9804043 , especially Theorems 2.1–2.2 and their complete proofs on PDF pp.3–4. The published paper is *Dense quantum coding and quantum finite automata*, J. ACM 49 (2002), 496–511, DOI 10.1145/581771.581773; theorem numbering in our text refers to the inspected preprint.

The classical task minimizes message length under recovery success at least p for every input and coordinate. Private encoding randomness and decoding functions are included. Their lower bound is n(1-h2(p)); their upper construction with covering codes and a finite family of masks/permutations has O(log n) message overhead. The entropy exponent and this communication scale are therefore classical, not new v30 claims.

The present exact-synthesis upper bound instead proves convex-hull containment of every prescribed mean vector, hence equality at every conditional probability. The block implementation charges the full one-pass raw buffer and all previous codeword labels. The exact and fixed-tolerance full-streaming exponent is the paper's operational conclusion. No assertion is made that arbitrary message encoders can be computed at their final message space without additional memory.

## 7. Algebraic decision procedure

Collins (1975), *Quantifier elimination for real closed fields by cylindrical algebraic decomposition*, LNCS 33, 134–183, DOI 10.1007/3-540-07407-4_17 (publisher record inspected). Davenport–Tonks–Uncu, arXiv:2302.06814v2 (2023), provides a modern primary discussion of real quantifier elimination. `cor:algebraic` invokes a finite existential semialgebraic decision with rational/algebraic coefficients represented by defining polynomials and isolating intervals. It does not claim polynomial complexity.

## Overall interpretation

The new proofs are self-contained. Literature comparison does not amount to exhaustive priority clearance. The 2002 omission has been fixed; the residual/all-machine difference is demonstrated in an explicit language; the classical communication exponent is positively credited; original-source access gaps remain visible rather than filled with unsupported claims.
