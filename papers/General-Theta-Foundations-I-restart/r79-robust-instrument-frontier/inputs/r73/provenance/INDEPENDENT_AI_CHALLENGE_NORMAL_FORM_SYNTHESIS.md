# R73 mathematical challenge note

## Status and role

This note records a separate automated author's proof challenge of mathematical files written by other members of the authoring session. It is not a commissioned referee report, human expert review, proof-assistant verification, or editorial judgment. The reviewer here is a collaborating AI agent. The finite computations described below are finite algebra checks with their actual scope, not a substitute for the proofs.

The review read the complete current contents of the following files:

| File | SHA-256 at review |
|---|---|
| `sections/33-reversible-normal-form.tex` | `676f2d450d75fbedc4607dc58b8bd7a2379a5d0e6c6bb86e026c344afb3c1344` |
| `sections/34-algebraic-synthesis.tex` | `fb8ea5a921694f880eb2333d120490c87c9d8108aa70dbef967d26b900440004` |
| `supplement-normal-form.tex` | `3c93c4981d02296ca9389a15ee871994716c55d3c4cdab6d962474736dc8c51e` (initial full read; see checked addendum below) |

The source root is `papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form`. A later change to one of these hashes requires an explicit addendum or a fresh check before attaching this note to that later file as its exact reviewed input.

**Checked addendum.** After the full read, the supplement explicitly added: when the transient set `H` is empty, the closed-class proof already gives convergence; otherwise the transient escape bound applies. The changed passage was read back and is consistent with the reviewed proof. Its updated SHA-256 is `fd336245f2e0dbd4bb24c4382a370721527181a1d502d53b080d46dc0dc1d2f1`. This addendum binds that clarified version; no theorem statement changed.

## 1. Reversible normal form

**Potential failure tested: hidden rows incorrectly identified with the observable quotient.** The proof uses the reachable linear span `R` and its valid quotient map, while the loop projection is constructed on the full stochastic simplex. It does not apply the quotient map to arbitrary hidden rows. The intertwining calculations use only rows in `R`, which remain in `R` under every command and the limiting projection. This avoids the previously dangerous shortcut.

**Potential failure tested: a loop semigroup need not itself be a group.** Identity words may have nonidentity and mutually different hidden stochastic matrices. The finite edge-cover average is legitimate because a finite hidden graph has at most `M^2` positive edges. Each closed class of the average is invariant under every identity-word matrix. The proof uses only `E Q_loop E = E`, not an unproved unsandwiched identity or a common stationary law for all loops. Convex combinations of products of identity words converge to `E` and remain observably the identity.

**Potential failure tested: the induced action may not factor through the observable group.** For an inverse word, inserting loop averages proves both inverse identities on the recurrent simplex. For two words representing the same group element, a common inverse then gives equality. Only after that step does the proof replace an inserted loop by the common quotient element to prove the product rule. This order avoids circularly assuming the quotient representation to prove its own well-definedness.

**Potential failure tested: lack of faithful action.** Identity on the entire recurrent simplex implies identity after projection on every reachable row. The quotient map is surjective, so the observable operator is the identity. It is not enough to preserve only the initial row; the written proof uses every row in `R`.

**Potential failure tested: a free initial mixture or lost first command.** If the original start lies in a closed class, its limiting row is that class's unique vertex. A mixed limiting row therefore requires a transient initial label and gives the extra count. Conversely the extra label has first-command row `lambda P_a`, not `lambda`, and decoder `lambda D`. The empty and every nonempty word are both realized. Unused orbits can be removed.

**Finding:** no mathematical gap identified in these steps at the recorded input hash. The conclusions concern a compactly reversible finite response, with an explicitly supplied pure initial-label convention; they do not claim arbitrary dissipative stochastic machines admit this form.

## 2. Exact size, group bounds, and rank rigidity

The first minimum follows from both directions of the normal form. Every point-start factorization is a deterministic-transition machine and so has at least the residual cardinality. Every mixed factorization pays at least `1+kappa`. Both upper alternatives exist. This proves `m=min(N,1+kappa)` including the case that a minimum-`kappa` factorization is itself pure.

Faithfulness gives `|G|<=M!`; if `M<N`, a pure core is impossible and gives the stronger `(M-1)!`. A finite-group invariant inner product justifies the subquotient-to-submodule passage in the permutation-module lower bound. The bounded probability decoder is kept as an additional condition, so the representation-theoretic lower bound is not falsely called sufficient.

At equality `M=d`, the reachable space is the full `d`-dimensional hidden row space and its observable quotient is an isomorphism. An inverse word consequently supplies an inverse stochastic matrix on that full space. This proves that the original transition matrices, not merely the replacement core, are permutations. No unproved full-row conclusion is used when `M>d`.

The symmetric-group family has full reachable rank because transposition differences span the zero-sum subspace and the initial row has mass one. The nonconstant nonnegative decoder has a nonzero mean and an orbit spanning the same full space, giving observability. Residual multiplicities and the pure/repeated/constant cases are consistent with the stated counts. The two generators work in every `k>=3`.

## 3. Bounded-decoder obstruction on S3

The new qubit example is a substantive positivity check beyond the module bound. Its coefficient response has the trivial representation plus the two-dimensional standard representation, six distinct residuals, and faithful `S_3` action. Any faithful action on at most five points must have one natural three-point orbit, with only a sign orbit or fixed points available for the remainder; the other transitive size is six.

The endpoint values at identity and the distinguished transposition force every positive-mass initial point to have decoder one and its transposed point decoder zero. In the natural orbit only one of the two moved points can carry mass, and fixed points carry none. The two equal rotation values force sign-orbit mass `1/4` and zero decoder on the third natural point. The remaining two transpositions would then have outputs `3/4` and zero, contradicting the two required `3/4` values. This excludes all probability factorizations of size at most five, including reducible actions and mixed starts. The six-residual upper completes `kappa=m=6`.

For the physical implementation the two real qubit unitaries induce reflections with angle difference `pi/3`; their product is a Bloch-plane rotation by `2 pi/3`. Relative to the x-axis preparation, the distinguished reflection has overlap `-1`, the other two reflections have overlap `1/2`, and the two nonidentity rotations have overlap `-1/2`. The Born probabilities are the claimed `0`, `3/4`, and `1/4`, with identity value one. The physical unitary group and observable group need not be identified before quotienting its scalar signs.

## 4. Algebraic synthesis

The reachable row closure and future-test column closure are finite linear computations over a common number field. Their annihilator intersection gives the observable quotient with the correct chronological matrix convention. Probability validity and compact reversibility are stated promises for the general input; the unitary corollary proves those promises for its physical class.

Restriction of scalars, the finite invariant lattice, and the torsion-free reduction-modulo-three kernel correctly yield the conservative group-order bound. In the prime-order kernel argument, division gives a contradiction modulo three for primes other than three; the separate cubic expansion gives `Z+3^s Z^2+3^(2s-1) Z^3=0`, again a contradiction for `s>=1`. Breadth-first enumeration therefore either closes or produces too many distinct products in finite time.

The finite residual orbit supplies a genuine upper bound. Enumerating group actions on every core that can beat that bound is finite; the bilinear probability constraints keep nonnegativity, row normalization, all terminal outcomes, and the initializer convention. Real-algebraic elimination supplies algebraic witnesses when the constraints are feasible. The proof credits classical matrix-group recognition and probabilistic-automaton minimization and does not claim a new polynomial-time decision result. The finite-word criterion is an alternative verification route, not a circular dependency of the normal-form proof.

## 5. Supplementary convergence and cyclic recovery

The closed-class convergence proof establishes a strictly positive finite power from paths and self-loops, proves contraction by splitting off a uniform row kernel, and obtains a stationary law by Cesaro compactness. The transient block decays geometrically, which justifies the displayed convergent convolution and its limiting simplex. The sandwich statement requires only class preservation. A minor clarity suggestion was sent to the author: explicitly dispose of an empty transient set before introducing its escape-time constants; this does not change the argument.

The cyclic module proof correctly permits repeated orders for different nonconjugate character pairs, counts an order-two real character once, and allows surplus trivial characters in a containing permutation module. Assignment of each required character to a containing cycle yields the sum-of-lcm lower; the specified positive-amplitude decoder proves attainment for the retained probability family. It does not turn a list of eigenvalue orders into a general bounded-decoder sufficiency theorem.

## 6. Finite certificate authoring and execution record

The author of this challenge note separately reconstructed `sections/35-finite-certificates.tex` and `diagnostics_r73_certificates.py`; therefore this note does **not** label those two files independently reviewed merely because it discusses them. Their final independent proof read belongs in the root proof audit.

The actual reconstructed diagnostic run completed 2,193 exact checks and zero floating probes. Ordinary and `python -O` output are byte-identical; explicit `check` calls remain active under optimization. The diagnostic file at execution has SHA-256 `5c9b9d98873a65ff3f55fbaa249a246c988c29f1e926a8dd18da03a895d33019`.

The declared checks include a six-variable exact polynomial identity, 64 rational stochastic matrices with 192 matrix/decoder pairs and their recurrences, 127 mixed words through length six for a four-label noncommuting background model, a finite invariant-span closure for an explicit period-four realization, and exact rational values for the sufficient damping interval. They do not execute general quantifier elimination, exhaust all stochastic controllers, or certify the continuum theorems by sampling.
