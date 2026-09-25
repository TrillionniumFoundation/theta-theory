# General Theta Foundations I — Revision 37

**Entropy Dissipation and Sharp Finite-Alphabet Memory**  
Qian Qi · 25 September 2026

Controlling r21 report: `d6b89112389b97a16a287fa32f3f75e4c2d72e0a`. Reviewed v36 publication: `1a08578710d55a2379cea56c43feb5eca56340a2`. Work branch: `revision/general-theta-foundations-i-v37-spectral-memory-2026-09-25`; a separate referee-ready branch is published only after a successful source-bound build.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r21](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Independent core sources](evidence/CORE_SOURCES.zip)

## Main result

A fixed finite orthogonal command alphabet with a norm gap on the full mean-zero spherical L2 space has

```
W_(N,epsilon) = Theta(N^((d-1)/2))
```

for every fixed positive signal and every fixed calibrated error `0 <= epsilon < rho/(2 sqrt(d))`. This removes the v36 logarithmic cardinality gap without changing the command alphabet or restricting hidden states. Exact common-row spherical synthesis supplies the matching upper bound; its final decoder depends on N. Isolated cut minima remain d+1 when the identity is present and d*rho<1.

The new proof smooths the law of conditional orbit centroids only as an analytic device. A spectral gap forces entropy production from angular Hellinger variance. Compression into a conditional mean costs at most a quadratic centroid loss divided by twice the Gaussian variance. Those quadratic losses telescope. Sparse smoothed centroid laws cannot be angularly uniform, so no fresh packet-mixing cost is needed at each epoch.

The general occupation statement allows different independent command laws and gaps at different epochs:

```
sum_(K_t<=k) (1-lambda_t^2) <= B_d kappa^(-3-2/(d-1)) k^(2/(d-1)).
```

Other epochs may have arbitrarily many labels. An actual-terminal-error corollary permits cancellation of intermediate errors.

For the five rational SO(3) commands, classical atomic labels are Theta(N), classical label bits are `log2 N+O(1)`, and quantum dimension two realizes the exact same wordwise numerical behavior. This is not a strict-cutpoint language or stationary-entropy separation. The external Bourgain–Gamburd gap is not numerically evaluated.

## Reproduction

Python 3.11+, SymPy, NumPy, SciPy, mpmath and PyMuPDF, plus LaTeX with AMS, Latin Modern, geometry, microtype, booktabs, mathtools, array, needspace and hyperref are sufficient.

```sh
python papers/GTF-I-v37-spectral-memory/verify.py
python -O papers/GTF-I-v37-spectral-memory/verify.py
python papers/GTF-I-v37-spectral-memory/build.py --core-only
python papers/GTF-I-v37-spectral-memory/build.py
```

After extracting the core ZIP, run `python GTF-I-v37-spectral-memory/build.py --core-only` from its parent. The full source ZIP also contains exact predecessor inputs for preservation and old regressions. Neither archive distributes standalone font files.

The build separates exact algebra from labelled numerical entropy quadrature. It runs v24–v37 ordinary/optimized regressions, new negative controls, three TeX passes, source hashes and predecessor preservation checks. The workflow publishes native sources before building them, then publishes the PDFs and receipts without force. Read the actual receipt rather than inferring execution from this description.

## Preservation and scope

[Unchanged v36 article](supporting-results.pdf) · [Cumulative mathematics](complete-manuscript.pdf) · [Cumulative development](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

The padded compiler in Appendix A has fixed update duration and a separately charged timer; it remains fixed-error, nonuniform, and leaves row tables free. Atomic width is not uniform computational space. Quantum labels, bits, entropy and language-recognition objectives are not interchanged. The independent historical A2/B4/C2 gates, noisy tags and adaptive collision scheduling are not claimed solved. All older files and proofs are preserved. Analytic proofs, priority and journal significance remain subject to independent scrutiny.
