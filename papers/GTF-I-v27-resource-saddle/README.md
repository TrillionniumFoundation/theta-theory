# General Theta Foundations I — revision 27

**Saddle Geometry and the Memory of Causal Experiments**  
Qian Qi · 24 September 2026

This revision responds to the tenth external report, frozen at `6018ed8f31d758b35eacc48079104e5895fc9591`, on v26 at `466bfcdcb8b7d594d3924dbfa82b4c6e29368858`. It is an additive descendant of that report. No predecessor manuscript, report, A2 file or historical pipeline path is overwritten.

[Canonical English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r10](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Complete mathematical manuscript](complete-manuscript.pdf) · [Complete preserved development](complete-development.pdf) · [Reproducible source archive](evidence/SUBMISSION_SOURCES.zip)

## New theorem chain

A least-favorable prior exposes a Bayes face. Uniform minimax optimality additionally forces contact and stationarity at its supporting parameters. Normalized positive continuation generators, compatible at all charged cuts, characterize which members of that saddle set are implementable. Independent cut ranks and a Bayes tie rule alone are not sufficient.

For the continuous two-preparation marked family, contact fixes the two previously indifferent response coordinates. Positive face packing then proves **minimum decision width exactly five**, allowing arbitrary stochastic encoders, adaptive training gates, stopping and independent calibration. The same argument on future output channels proves **minimum whole-schedule peak exactly twelve for candidate-first serial validation**. This ordered peak is not identified with the minimum over every validation order. A strict four-state loss is proved by compactness and persists for sufficiently small positive physical noise; its numerical size is not claimed.

For every preparation number N, unrestricted values tend to the closest-experiment distance, and every least-favorable prior localizes on the closest-experiment set. For the marked family:

```
s = sqrt((1+gamma)/2)
U_N -> 2*s - 1 - gamma/2
closest parameters = (s,s), (1-s,1-s)
TV(Q_gamma,b(p,q)) - min TV >= (7/2300)*dist((p,q),closest)^2.
```

The error in value is at most `sqrt(3/N)`. Every symmetric least-favorable prior converges in W2 to the equal two-point law, with bound `sqrt(2300/7)*(3/N)^(1/4)`. Finite-N two-point optimality and sharpness of these rates are not inferred.

## Reproduction

Use Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7 and a TeX distribution providing AMS, Latin Modern, geometry, microtype, booktabs, mathtools and hyperref. From the repository root:

```sh
python papers/GTF-I-v27-resource-saddle/verify.py
python -O papers/GTF-I-v27-resource-saddle/verify.py
python papers/GTF-I-v27-resource-saddle/build.py
```

The assembly pins the v26 main source by Git blob `c6dcd5f60dfbd34c679961e6afeded933cda3ba4`, verifies the eleven unchanged mathematical modules, and checks recovery of the complete predecessor body. The new introduction does not erase the earlier introduction: it remains at its unchanged repository path and in the preserved volumes.

The build runs new and predecessor regressions in ordinary and optimized Python, executes deliberately invalid controls, compiles three times, rejects unresolved references or overfull boxes, and checks every appended predecessor page for text identity and representative pages for raster identity. The source ZIP contains the exact rebuilding inputs and no font files. The workflow publishes native source first, builds that exact source commit, and then publishes PDFs and receipts to the revision and referee-ready branches without force.

See the actual receipt and workflow status for executed results. Tests and successful publication are reproducibility evidence, not independent mathematical verification, novelty clearance or journal acceptance.
