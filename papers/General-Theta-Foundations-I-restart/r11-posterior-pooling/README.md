# General Theta Foundations I — restart R11: posterior pooling

The new native article is `main.tex`. It keeps the General Theta mother problem and title. The latest external assessment used is the R10 report at review commit `6f3ca64beec4b054dba8cb5def1a6c69fbc46d52`, not the old R7 report.

## Mathematical result

The central theorem (source label `thm:pooling`; generated numbering is authoritative) is an adaptive completion theorem for positive finite-hidden-state experiments with overlapping continuous reports. Every finite retained state carries its true posterior under the implemented machine. Pooling incoming posterior laws at their actual barycenters gives an exact Bellman–Jensen loss identity. An integrated convex-curvature bound yields second-order error without smooth value functions or policy margins. For every fixed observation horizon n, checkpoint and autonomous excess risks have matching M^(-2/d) exponents. The explicit autonomous upper is C n floor((M-1)/n)^(-2/d), not a uniform joint n,M law.

Raw continuously noisy sensors have genuinely observation-dependent optimal last actions. A validation extension alternates atomic and continuous acquired strata. Common-task calibration, numerical error and attained early-channel deficiency are separately proved with complete controller, phase and simulator counts.

## Submission components and preservation

* Article: new posterior-pooling proof and raw realizations, page count in final build receipt.
* Integral Supplement T: the complete unchanged R10 mathematical source rebuilt and given an identifying cover. No old theorem is deleted or silently strengthened.
* Integral Supplement S: the complete unchanged earlier technical companion, rebuilt through the original pinned scripts.

R4–R10 sibling trees and old review inputs are inherited unchanged. Original reviews, realization branches, archive and canonical branch are not modified. The R10 external report is connected by its exact original blob in the inherited review commit. No v97 numbering or v96 copying is used.

## Rebuild

Python 3, TeX Live (amsart/lmodern/esint/microtype), pdflatex, poppler, and pypdf are required. From this directory:

```
python verify.py
python regression.py
python -O regression.py
python build.py --source-sha <40-character-source-commit> --expected-tree <native-source-tree>
```

The build runs new ordinary/optimized exact finite tests, the retained regression chain, and ten isolated PDF builds: six mathematical bodies and four identifying covers, each with three LaTeX passes. It checks complete sources, references, labels, recorder inputs, output identity within an environment and absence of overfull boxes. It does not certify continuous proofs, priority, or top-four acceptance.

Publication evidence distinguishes the mathematical-source commit, artifact child and final verification head. See `evidence/REFEREE_PACKET.md` once finalized. Audits are repository evidence, not claims of a mathematical breakthrough.
