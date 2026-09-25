# General Theta Foundations I — Revision 39

**Minimal Orbits and the Width of Numerical Experiments**  
Qian Qi · 25 September 2026

Controlling r23 report: `5439c0ea2540e3caddbab600cc7a4f8699421439`. Reviewed v38 publication: `8ec190c921656b9869f3520ec9bf7bf754622e97`; native v38 source `e52157d8a7df50e2ca962029e29412e7f62f0ed1`.
The work branch `revision/general-theta-foundations-i-v39-orbit-response-2026-09-25` was created remotely from the controlling report. Publication creates `revision/general-theta-foundations-i-v39-referee-ready-2026-09-25` only after the full and independent-core builds pass.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r23](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Independent core sources](evidence/CORE_SOURCES.zip)

## The representation invariant

Let a compact connected Lie group act orthogonally on a fixed finite-dimensional real space. On a nontrivial irreducible constituent V_i, put `s_i=min_unit_v dim(Gv)`. Under a full mean-zero group norm gap on a fixed finite command alphabet, the numerical experiment has width

```
W_(N,epsilon) = Theta(N^(s_i/2))                  (irreducible),
W_(N,epsilon) = Theta(N^(max_i s_i/2))            (spanning reducible seeds).
```

Signal and error are fixed in the explicit calibrated range in Theorem 1.1; the general small-signal upper bound is `rho<=min(1/10,1/(8D))`. For seeds on a minimal irreducible orbit, the original `rho<=1/10` range is retained. A purely invariant representation has constant width. Constants are not uniform in the representation, dimension, signal or gap.

The proof derives a uniform small-ball power across **all** stabilizer types from differential rank and compact charts. The inherited entropy occupation theorem therefore applies to every hidden conditional-centroid direction. The matching compiler uses a minimum-dimensional orbit and quadratic support approximation. In a reducible representation it randomizes over constituents, charges the branch inside the state, and uses amplified conditional signal with exactly the correct weights. It has common command rows and an N-dependent decoder. The theorem is not a statement about jointly independent answers to all coordinates.

For symmetric basis seeds every cut separately has positive minimum D+1, although simultaneous width grows. Conjugation over the real, complex and quaternionic self-adjoint spaces gives exponents `(q-1)/2`, `q-1`, `2(q-1)` under the respective full gap. Every fixed nontrivial real spherical-harmonic representation of SO(3) has exponent one. Minimum orbit dimension, generic dimension, dimension of the original seed orbit, and dimension of a product output law are distinguished.

An explicit D+1-label common-row simulator preserves cutpoint signs at every length by attenuating its numerical coefficient as `(2D)^(-N-1)`. It cannot preserve fixed numerical accuracy. The comparison includes the August revision of Chen–Wu's April paper and Chen's September symmetry paper, not only outdated abstracts. The embedding mechanism and static quantization exponents are credited as classical.

## Preserved results and the arithmetic source boundary

The v38 entropy proof, quantitative all-spectra proof, projective construction and effective six-gate bounds remain in the current article. The old projective signal range is unchanged. A normalization appendix proves the quaternion parity/inverse conventions, division of the Hecke sum by six, and the spherical-to-full-SO(3) spectral transfer. Its arithmetic input remains the external LPS inequality. The original 1986/1987 full page images were not obtained: the original theorem number is **not** claimed verified. The numbered inspected restatement is Pisier, Theorem 3(ii), together with the coauthor quaternionic account. This limitation does not affect the main theorem's explicitly conditional full-gap hypothesis.

[Unchanged v38 article](supporting-results.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full rebuilding inputs](evidence/SUBMISSION_SOURCES.zip)

No predecessor path is overwritten. Large archives are optional provenance, excluded from the compact submission. Independent analytic A2/B4/C2 and related gates are not claimed closed.

## Reproduction

Python 3.11+, SymPy 1.14.0, NumPy/SciPy (for inherited verifiers), mpmath, PyMuPDF 1.26.7 and a TeX installation with AMS, Latin Modern, mathrsfs, geometry, microtype, booktabs, mathtools, needspace and hyperref are sufficient.

```sh
python papers/GTF-I-v39-orbit-response/verify.py
python -O papers/GTF-I-v39-orbit-response/verify.py
python papers/GTF-I-v39-orbit-response/build.py --core-only
python papers/GTF-I-v39-orbit-response/build.py
```

The core ZIP is self-contained and rebuilds with `python GTF-I-v39-orbit-response/build.py --core-only` after extraction. The full archive contains exact predecessor inputs for preservation. No font files are included. Read the actual build receipt for executed results. Finite tests, source hashes and compilation are not independent proof or priority certification.
