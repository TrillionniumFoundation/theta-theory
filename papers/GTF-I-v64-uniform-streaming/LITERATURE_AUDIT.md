# Theorem-level literature comparison — Revision 64

Date checked: 28 September 2026. This is an author-side comparison of specified primary sources, not an independent priority opinion or an exhaustive novelty certificate. The inherited audit is preserved in `predecessor-audit/LITERATURE_AUDIT.md`.

## New computational comparison

### Benvenuti–Farina: positive realization

Primary source: L. Benvenuti and L. Farina, *A tutorial on the positive realization problem*, IEEE Transactions on Automatic Control 49 (2004), 651–664, DOI 10.1109/TAC.2004.826715. Theorem 2 in the inspected author manuscript is the invariant-polyhedral-cone characterization, and equation (2) builds a nonnegative realization from generators of such a cone.

Inspected text: https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf (printed page 3, theorem and displayed equations visually checked).

The theorem treats an exact stationary realization of a transfer function. Our all-word horizon-dependent approximation problem has common stochastic rows for each command and legal vector outputs. The new computational statement additionally charges precision and scratch bits. The classical cone theorem explains why real linear dimension and positive state count differ; we do not claim that distinction as new. It does not state the finite-horizon accuracy/bit-space law proved in Section 31.

### Ambainis–Watrous: two-way quantum/classical automata

Primary source: A. Ambainis and J. Watrous, *Two-way finite automata with quantum and classical states*, Theoretical Computer Science 287 (2002), 299–311; https://arxiv.org/abs/cs/9911009.

Inspected locations: Section 2, particularly the two-way head and the 9-tuple model on printed page 3; Theorem 1 on palindrome recognition and the repeated scans in its proof. The model definition was also visually inspected in the PDF.

This is a language-recognition model with a quantum register and two-way input access. The present theorem is about one-pass classical numerical approximation for every command word. Its output is a legal matrix description, not a physical qubit. We do not infer that the language-recognition result is contradicted or that it has an uncharged bit-space simulation. Precision, access and output criteria must not be identified across the two models.

### Panduranga Rao–Vinay: complex-weighted simulation

Primary source: M. V. Panduranga Rao and V. Vinay, *Quantum finite automata and weighted automata*, https://arxiv.org/abs/quant-ph/0701144 (2007).

Inspected locations: Section 2.2, Definition 2, Section 3 and Theorem 1; the complex-weighted definition was visually inspected on PDF page 4. Theorem 1 constructs a two-way weighted automaton for the specified one-sided language-recognition problem.

The weights are complex and output is tested through a weight criterion; they are not nonnegative transition probabilities paired with a legal density-matrix decoder. A constant-dimensional algebraic representation does not bound the number of complete classical configurations in a finite-bit implementation. The v64 theorem addresses that separate cost, and does not claim a new general quantum-to-weighted conversion.

## Retained comparisons and exact scope

The spherical entropy/Wasserstein lemma is compared in the manuscript with Polyanskiy–Wu, *Wasserstein continuity of entropy and outer bounds for interference channels*, IEEE TIT 62 (2016), 3992–4002, Proposition 1; https://arxiv.org/html/1504.04419v2. That proposition concerns regular Euclidean densities. The paper supplies its own compactly supported spherical mixture proof, including zeros. Entropy transport continuity is not claimed as a new general principle.

The v63 audit separately credits the Rényi-affinity inequality (van Erven–Harremoës, Theorem 3), classical nonbacktracking radial identities and the exact LPS norm (Pinochet Lobos–Pittet, Theorems 1.1–1.2), and compares arithmetic gate covering (Parzanchevski–Sarnak, Section 3). These classical statements are mathematical inputs, not results certified by finite word tests. The v62 audit credits nonhomogeneous-chain tail theory in Blackwell, Cohn and Grabchak–Sonin for the causal strong-converse line.

The new upper rounding construction is elementary finite-precision arithmetic and is proved directly. The new lower bound is an application of the already derived entropy occupation theorem, not an independent new spectral theorem. The claimed contribution is a sharp uniform, one-pass numerical space consequence, with an explicit algorithm and a fully specified interface, alongside the retained finer width results.

## Remaining external assessment

The above entries identify precise differences between specified theorems. They do not exclude an equivalent formulation in all automata, positive-realization, finite-memory filtering or quantization literature. No external expert has endorsed priority in this package. The referee's request for an independent expert comparison cannot be discharged by renaming an author-written document an independent review.
