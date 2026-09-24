# General Theta Foundations I — revision 26

**Causal Experiments, Finite-Memory Control, and Exact Minimax Laws**  
Qian Qi · 24 September 2026

The controlling report is the ninth external report on v25, frozen at `568301ff5d8991af9a99a478371c1c4993d0bcd1`. The reviewed manuscript is v25 at `818ca30bab506cfedaf6aee4c32bedff70c1e251`. This revision descends from the report and adds a new package without modifying any predecessor manuscript, report, A2 branch, or historical pipeline file.

The canonical English article is [paper.pdf](paper.pdf), with native source [main.tex](main.tex). Read [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md) for the mathematical response and the precise status of each request. The [theorem-location record](evidence/THEOREM_LOCATIONS.json) gives the numbers and pages of the actual compiled manuscript. [BUILD_RECEIPT.json](evidence/BUILD_RECEIPT.json) records executed results, native source commit and artifact hashes.

## Mathematical content

The restored opening develops A0–A5, prepared path laws, predictive quotients, posterior barycenters, entropy and normalized response, checkpoint resolution, an online matched small-ball/covering law, and causal simulation with simultaneous preparation, calibration, numerical/model error, and retained-memory accounting. These restore and extend the v1/blueprint route; their classical ingredients are not claimed as inventions.

The finite-memory controlled formulation uses parameterwise occupation bundles for **offline design only**. The executing controller reads only its declared finite register and current inputs. The resulting nonlinear dynamic/supersolution theorem does not interchange worst-case parameters with independently optimized post-report adversaries. A sharp family of incomparable sensing actions has exact value `1/(2*ceil(m/K))`; an uncharged ex ante controller mixture has value `K/(2*m)`. The gap is strict when K does not divide m. The selected action buffer and validation states are charged separately; K is a genuine cut constraint, not an incorrectly reported uniform peak. Full-support perturbations preserve the gap.

The collision marked model now has exact **U2**, not only U1:

```
2*r^3 + 25*r^2 - 3 = 0,      1/3 < r < 7/20,
U2 = (-r^3 + 6*r^2 - 3*r + 14)/32 = 0.4261127787966559...
```

A full-square polynomial lower certificate and a matching least-favorable two-point prior prove the equality against all full marked-word responses. The exact saddle extends to the continuous target-bias interval `6/25 <= gamma <= 13/50`, with its own cubic and exact value. The implementation still has five frozen events and peak twelve, including a newly exposed stochastic selection cut. A finite fair-bit approximation has separately counted precision and buffer costs.

The original physical two-preparation score is exact at ideal Q* for every W >= 12, and lies within beta of U2 for targets within TV distance beta. The strict-score preparation interval extends to `U1 + beta <= c < U2 - beta`. Existing deterministic results and their proofs remain intact.

For arbitrary integer m,K, the revelation model has an exact uniform-prior Bayes formula, an exact low-reveal minimax range, an exact perfect-reveal endpoint, and a complete two-label law for every N and m. Nondivisibility produces a real minimax/Bayes discrepancy; a random partition is not silently stored for free. A final confidence/simulation consumer theorem uses the new exact physical margin and the acquired causal transport theorem with explicit memory products.

## Reproduction

Use Python 3.11 or newer, SymPy 1.14.0, PyMuPDF 1.26.7 and an AMS-capable LaTeX installation with Latin Modern, geometry, microtype, booktabs, mathtools and hyperref. From the repository root:

```sh
python papers/GTF-I-v26-controlled-memory-foundations/verify.py
python -O papers/GTF-I-v26-controlled-memory-foundations/verify.py
python papers/GTF-I-v26-controlled-memory-foundations/build.py
```

`assemble.py` pins the v25 main source to Git blob `4b793be9f45326fab51d44b66877f5a8bf61667c`. It retains the entire substantive mathematical body, inserts new theorem modules, and explicitly updates the one obsolete statement that U2 is undetermined. Its reversible assembly manifest verifies the unchanged old body. All five v25 mathematical modules are byte-identical copies in the new package.

`build.py` executes v26, v25 and v24 regressions in ordinary and optimized Python, tests six new and six predecessor negative controls in both modes, compiles three times, rejects undefined references and overfull boxes, and appends the unaltered predecessor complete volumes. Every appended page is compared for text and raster identity. The source archive in `evidence/SUBMISSION_SOURCES.zip` contains the native source and exact predecessor files needed for rebuilding, with no standalone font files.

The workflow first materializes and publishes the native sources from a hash-checked bootstrap bundle, then builds the **native source commit**, and publishes the PDFs and receipts. The revision and referee-ready branches are updated without force. The workflow trigger SHA and native source SHA are separately recorded; they need not be equal.

## Scope retained for the next referee

The exact ideal score at N=2, W>=12 does not establish the least possible peak at N=2 or the complete widths-3-through-11 frontier. The continuous U2 family is not an all-N recurrence. General K>=3 high-reveal minimax values outside the stated exact regime remain distinct from the Bayes formula. The generic finite-memory recursion is an exact variational formulation, not an efficient algorithm or a linear prior saddle.

The later consumer is a proved local theorem dependency, not a fabricated claim that A2, B4, or C2 has become logically dependent on it. Those geometric and unbounded-operator routes and the full eleven-paper development are preserved. Norberg's original full-proof comparison is not claimed complete. Successful symbolic checks and publication establish reproducibility, not independent proof certification, novelty clearance, or journal acceptance.
