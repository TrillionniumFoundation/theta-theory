# Proof dependencies — GTF I v3

## New principal chain

| Statement label | Inputs | Mathematical work performed |
|---|---|---|
| `thm:v3-orbit` | Borel regenerative experiment; independent acquisition/modes/coding tapes; bounded readout | Truncated Hilbert quantization; reset-time disjointness; finite-horizon summation; N then K limit. No invariant measure is assumed. |
| `lem:v3-tree` | Uniform binary digits; explicit union of all suffix states | Exact conditional cylinder variance and initial-acquisition age distribution; finite geometric risk sum. |
| `lem:v3-orbit-separation` | Fractional parts before dyadic separation | Global lower modulus despite jumps of the doubling map; all three q regimes. |
| `thm:v3-phase` | The preceding three results; scalar uniform quantization | Exact checkpoint risk, arbitrary-centre orbit small-ball lower bound, all-budget finite-machine upper bound, critical logarithm. |
| `thm:v3-quotient` | Positive definite joint Gaussian covariance; compact mean image; bounded loss; unrestricted nuisance | Difference/regression factorization; diffuse nuisance prior; independent replacement; TV control; M-label simulation. Equality is minimax for theta, not sufficiency for eta. |
| `thm:v3-contact` | Exact quotient; two-sided contact geometry in the actual noise metric | Borel minimum-distance estimator; power inverse bound; integer anisotropic codebook; Gaussian hypercube tests; arbitrary-label representation lower bound. |
| `ex:v3-coupled` | Explicit triangular shear and invertible Gaussian noise construction | A concrete nonseparable mean and genuinely correlated pair satisfying all contact assumptions. |

All new theorems and lemmas have full proofs in `regenerative.tex` or `calibration.tex`. The general orbit result is used only as a lower bound; matching realizability is constructed explicitly in the expanding example rather than assumed for arbitrary Hilbert codebooks.

## Preserved mathematical content

`retained-results.tex` is exactly the suffix of v2 `revision.tex` beginning with `\section{Acquired geometry and nonuniform causal resolution}`. It contains the entire previous quantitative theorem/proof development, including A1 transfer, nonuniform block stability, Hilbert projective contraction, positive/intermittent refresh laws, Cantor/discrete acquisition, measured calibration, unrestricted control, and finite-program accounting. No inherited theorem statement or proof is altered.

The eleven numbered foundational sections after the v1 introduction and both v1 appendices are loaded directly from the unchanged v2 `legacy/` tree. Every inherited mathematical label must be present in the compiled auxiliary file. The original introductions remain in the original v1/v2 files; v3 replaces exposition, not mathematical results.

## Boundaries explicitly checked in the new proofs

The reset at time zero is an actual acquisition; the uniform checkpoint lower law does not assume a deterministic known initial state. The decoder cannot reread the reset value after forming its label. A clock does not supply the last reset time. Random-tape positions are not free memory. The terminal probe is not feedback in the continuing process. The doubling map is not globally Euclidean Lipschitz. Off-image codebook centres and randomized machines are included in the converse. `sup_t E loss` and `E sup_t loss` are not conflated. The nuisance quotient preserves the label budget but makes no nuisance-estimation equivalence claim. The contact map and covariance are known; the additive calibration is unknown. Positive-definite correlated results do not remove the retained zero-noise theorem.

## Execution evidence

`verify.py` checks finite exact rational cylinder integrals and age sums, all charged transitions for budgets 1 through 512, finite orbit-separation cases, exact correlated Gaussian matrix identities, integer anisotropic covers, and contact-power identities. Mutants erasing the critical logarithm and omitting cross covariance must fail. Optimized Python must give the same results. Both inherited diagnostic suites are rerun. These are regression checks, not an automated proof of the infinite-time theorems.

`build.py` verifies source hashes, stable inherited Git trees when run in Actions, complete retained-body equality, all mathematical labels, stabilized TeX references, and absence of overfull boxes. It packages every actual mathematical input and its build recipe. Rendered-page inspection is recorded separately from compilation.
