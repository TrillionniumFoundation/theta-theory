# General Theta Foundations I — Revision 35

**Sharp Width of Hidden Rotation Experiments**  
Qian Qi · 25 September 2026

Controlling r19 report: `6016075083626f7c94cfb07912c49fa256fcf9e0`. Reviewed v34 publication: `47bc47e5995e4b1b99a18aaa472a1309f1668f40`; native source: `5d773fb7dddb007887119b35cc29e0b3bae7406f`. The new work branch is `revision/general-theta-foundations-i-v35-sharp-memory-2026-09-25`. The referee-ready branch is published after a successful source-bound build.

[Focused English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r19](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip)

## Main result

The hidden fifth-root/cube-root gap is closed for every badly approximable rotation angle and every fixed uniform row-TV error `0 <= epsilon < 1/20`:

```
W_(N,epsilon)(alpha) = Theta_(alpha,epsilon)(N^(1/3)).
```

The lower bound allows arbitrary hidden directions, arbitrary time-dependent stochastic rows and a new machine at each horizon. It matches the inherited exact resonant-polygon upper construction. Every separate cut still has positive minimum three. Exact hidden, vector-state and fixed-length common-command-row widths have the same order.

The new proof uses independent length-`2k-1` packets, each with a uniform count of active commands. Its k-state endpoint loses at least `s_(2k-1)(alpha)^2` of its incoming conditional phase amplitude. It does not assume independent commands within a packet, and it charges every command. Multiplication gives the sharp lower order, variable-profile occupation bounds and an obstruction to the actual minimum final simulation error. At the golden angle the exact lower bound is `W > (N/168)^(1/3)`, in addition to `W>=3`; the constants are not optimal.

A general compact-group representation theorem expresses this loss through orbit quantization. A separately declared model allowing all SO(d) matrices as atomic commands has matched width `Theta_(d,epsilon)(N^((d-1)/2))`, including noncommuting commands for d>=3. This is not the same command alphabet as the binary rotation experiment.

The model is explicitly a nonuniform probabilistic ordered read-once transducer with real terminal readouts. The article compares its quantities with the directly relevant branching-program and circle-walk literature. Classical positive realization, geometric quantization and Blackwell deficiency are credited. The old homogeneous angular estimate is sharpened to its optimal universal coefficient `l^2-1` in a proof appendix; the new lower bound bypasses its harmonic summation.

## Reproduction

Python 3.11+, SymPy 1.14.0, mpmath and PyMuPDF 1.26.7, and LaTeX providing AMS, Latin Modern, geometry, microtype, booktabs, mathtools, needspace and hyperref suffice.

```sh
python papers/GTF-I-v35-sharp-memory/verify.py
python -O papers/GTF-I-v35-sharp-memory/verify.py
python papers/GTF-I-v35-sharp-memory/build.py --core-only
python papers/GTF-I-v35-sharp-memory/build.py
```

The standalone core ZIP extracts to one package; run `python GTF-I-v35-sharp-memory/build.py --core-only` in its parent directory. The full source ZIP additionally contains the exact predecessor inputs for the archival build. No font files are distributed.

The workflow first publishes native source, builds that exact commit, checks the independent core source archive, then publishes artifacts and receipts to the new work and referee-ready branches without force. Trigger, native source and publication SHAs are different provenance fields. Actual executed counts and hashes belong to the receipt, not to an inferred success claim in this README.

## Preserved material and scope

[Unchanged v34 article](supporting-results.pdf) · [Complete mathematical archive](complete-manuscript.pdf) · [Complete development archive](complete-development.pdf) · [Full rebuilding archive](evidence/SUBMISSION_SOURCES.zip)

All predecessor sources and PDFs remain unchanged at their original repository paths. The full v34 article and its cumulative volumes are retained without alteration. Large archives are optional history, not the focused referee package.

The matched order is not an exact finite integer optimum, an optimized constant, an all-irrational theorem or a uniform signal-to-zero result. The compact-group extension has explicit input and error conventions. Exact atomic kernels are not finite-bit algorithms. Local deficiency sums may overestimate final error; the new actual-error lower bound does not assume otherwise. Fully adaptive collision scheduling, noisy-tag composition and the independent historical A2/B4/C2 analytic gates are not claimed solved. Checks and successful compilation are reproducibility evidence, not independent proof certification, exhaustive priority clearance or journal acceptance.
