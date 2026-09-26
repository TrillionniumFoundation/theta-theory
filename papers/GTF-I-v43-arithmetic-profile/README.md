# General Theta Foundations I — Revision 43

**Word Profiles and Arithmetic Fluctuations of Numerical Memory**  
Qian Qi · 26 September 2026

Controlling r28: `d5fdba334f7a031413bba08c29af30a555936905`. Reviewed v42 publication: `b5f9874903a429f9c1a9cb080547d50c891d050a`; native v42 source: `bc4e304693eb13b979154f5ad30c937390925352`.

Work branch: `revision/general-theta-foundations-i-v43-arithmetic-profile-2026-09-26`. The referee-ready branch is published only after the native-source build and isolated core rebuild succeed. All earlier paths and branches remain unchanged.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r28](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## Mathematical statements

The finite alphabet has an optimized word-packet distortion `Gamma_A(k,B)` and a separate compatible-polytope dilation `lambda_A(k,a)`. The former yields an all-hidden-state nonuniform interval budget and a lower bound on actual optimized final error. The latter supplies exact common stochastic rows. Neither assumes a spectral gap or commutation. Their values are finite algebraic optimization problems at fixed fully listed algebraic data; no efficient general minimizer or equality with optimal hidden width is claimed.

For planar word sets the optimal distortion is a finite second-order cone program over cyclic partitions. The complete four-phase example has an exact optimal law and values. This differs from certifying an infinite supremum over harmonic degrees.

For every rationally independent r-angle vector of minimal ordinary dual type `omega*=r`, with r fixed, fixed signal `0<rho<=1/10` and fixed row-TV error `epsilon<rho/(2 sqrt(2))`,

```
log W_(N,epsilon) / log N -> r/(2r+1).
```

This is a logarithmic exponent, not a constant-factor Theta claim throughout that larger class. Almost every vector belongs to it. For every fixed delta>0, almost everywhere,

```
c N^(r/(2r+1)) / log(N+2)^(2r(1+delta)/(2r+1))
 <= W_(N,epsilon)
 <= C N^(r/(2r+1)) log(N+2)^(2r^2(1+delta)/(2r+1)).
```

The upper bounds synthesize every prescribed conditional probability exactly. Finite rational extensions have the exponent of their actual independent basis, with rational phase labels charged. Reflection preserves these conclusions.

For every irrational single angle, convergent denominators give horizons `M_n=C_kappa*q_n^3+O(1)` on which width is Theta(M_n^(1/3)). For every Liouville angle,

```
liminf log W / log N = 0,
1/3 <= limsup log W / log N <= 1/2,
W_(N,epsilon) -> infinity.
```

Thus one fixed alphabet need not possess a single power-law exponent. The precise Liouville upper limit is not determined. The explicit number `sum_(j>=1) 10^(-j!)` gives exact subpower-horizon realizations.

## Provenance and classical boundary

The endpoint centroid contraction is inherited from v35/v42 and is reproduced with attribution. Nearest-center geometry, Dirichlet approximation, continued fractions, the summable metric Diophantine argument and the old algebraic vector are not claimed new. The direct DGLPS arXiv:2502.06202v2 comparison covers Theorem 3.9, Lemma 3.11 and their identical algebraic vector. New statements concern optimized finite word certificates and the dynamic metric/Liouville consequences, not new arithmetic or a general classification of positive realization.

[Unchanged v42 article](supporting-results.pdf) · [Complete mathematical archive](complete-manuscript.pdf) · [Complete development archive](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

The entire v42 article and cumulative volumes are retained without alteration. Its expansion, calibration and representation results are not withdrawn. The large archives are optional and excluded from the compact referee package.

## Reproduction

Use Python 3.12, SymPy 1.14.0, mpmath, PyMuPDF 1.26.7, and LaTeX supplying AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools and hyperref. The full inherited build additionally uses NumPy 2.3.5 and SciPy 1.17.0. Run from the repository root:

```sh
python papers/GTF-I-v43-arithmetic-profile/verify.py
python -O papers/GTF-I-v43-arithmetic-profile/verify.py
python papers/GTF-I-v43-arithmetic-profile/build.py --core-only
python papers/GTF-I-v43-arithmetic-profile/build.py
```

The core archive extracts to one directory; run `python GTF-I-v43-arithmetic-profile/build.py --core-only` from its parent. The full source archive also includes the pinned previous PDFs and verification inputs. Standalone font files are not included.

Available labels, label bits, total table size, construction cost, finite-bit sampling and anytime autonomous memory are separate resources. Epoch, horizon, tables and exact atomic rows are free here. No all-alphabet hidden-width optimum, optimized finite constants, independent expert verification, original-page LPS audit or unrelated analytic pipeline closure is inferred. Executed checks support reproducibility, not universal proof or priority certification.
