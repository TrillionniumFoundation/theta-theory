# General Theta Foundations I — Revision 38

**Orbit Geometry and Entropy Budgets for Finite Memory**  
Qian Qi · 25 September 2026

Controlling r22 report: `c630ea23b8a27c959466a389da5d3de49a020bd6`. Reviewed v37 publication: `c5b8015887f83833832e393db69380afeb5a9a3b`; native v37 source: `946db04e25c075427a3f6c09054b61fef14adea9`.

Work branch: `revision/general-theta-foundations-i-v38-orbit-entropy-2026-09-25`. The separate referee-ready branch is published only after the source-bound build succeeds.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r22](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## The theorem chain

Group-invariant entropy production and a uniform orbital small-ball estimate give an occupation bound for arbitrary hidden stochastic states. The estimate must hold for all conditional-centroid directions, not just the seed orbit. For SU(q) conjugation on traceless Hermitian matrices, a spectral-projector argument gives the uniform exponent `2(q-1)` for every spectrum, including mixed and repeated-eigenvalue spectra. A quadratic projective-net enclosure then gives a matching exact upper machine:

```
W_(N,epsilon) = Theta_(q,rho,epsilon,mu)(N^(q-1))
```

for a full group norm gap, fixed signal and `epsilon < rho/(2 sqrt(q^2-1))`. Finite algebraic alphabets exist for every q through an external spectral-gap theorem. The same behavior has a fixed q-dimensional quantum realization. The classical quantity is `(q-1) log2 N+O(1)` label bits; neither quantity includes nonuniform program advice.

A **separate six-command** rational SO(3) example uses the standard V-gates, cosine `-3/5` and sine `4/5`, about all three axes and their inverses. The external LPS theorem supplies full mean-zero norm at most `sqrt(5)/3`, hence squared gap `4/9`. For all N>=1,

```
[(1/(10 sqrt(3))-2 epsilon)^4 / 221184] N <= W_(N,epsilon) < 150 N.
```

The upper construction is exact; at zero error the lower constant is `1/19,906,560,000`. The old five-gate numerical gap has not been evaluated or silently replaced. The new arithmetic certificate is an application of a classical infinite-dimensional theorem, not a finite harmonic computation.

## Reproduction

Python 3.11+, SymPy 1.14, NumPy, SciPy, mpmath, PyMuPDF 1.26.7 and a TeX distribution supplying AMS, Latin Modern, geometry, microtype, booktabs, mathtools and needspace suffice.

```sh
python papers/GTF-I-v38-orbit-entropy/verify.py
python -O papers/GTF-I-v38-orbit-entropy/verify.py
python papers/GTF-I-v38-orbit-entropy/build.py --core-only
python papers/GTF-I-v38-orbit-entropy/build.py
```

The core ZIP is self-contained: after extraction run `python GTF-I-v38-orbit-entropy/build.py --core-only`. The full source archive additionally includes frozen predecessor inputs for archival reproduction. No standalone font files are distributed.

Native source is committed before the full remote build. The full build runs v24–v38 checks, deliberately invalid controls, three LaTeX passes and preservation checks. The separate core build verifies the independently extractable source package. Check the actual receipt and workflow result rather than inferring successful execution from this description.

## Preservation and scope

[Unchanged v37 supporting article](supporting-results.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full source archive](evidence/SUBMISSION_SOURCES.zip)

The compact package excludes cumulative archives. The old article and all original repository paths remain unchanged. The new article compares causal coding, nonanticipative rate-distortion, Markov lumping, conditional-expectation entropy and probabilistic branching programs at the level of objectives and stated results.

Theorems concern nonuniform clocked atomic-row width. Full group gap is not merely dense generation or a gap in one finite representation. Fixed signal is not a uniform vanishing-signal theorem. The general-q gap is qualitative; only the separately named six-gate alphabet has the numerical certificate used here. Exact finite integer optima, optimized constants, uniform computational space, fully adaptive collision and independent historical analytic gates are not declared solved. Proofs and priority remain subject to independent review.
