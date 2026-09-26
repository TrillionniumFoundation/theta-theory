# General Theta Foundations I — Revision 44

**Hankel Compatibility, Distortion Rates, and Finite-Bit Memory**  
Qian Qi · 26 September 2026

Controlling r29: `6e8a9504a1a0820e6195317df885d99aed06c878`. Reviewed v43 publication: `153830f5dc8d13358f9103c307c619076c5ec80c`; native v43 source: `92722c0c14d1897740344a53e3e017258bec040e`. The new work branch is `revision/general-theta-foundations-i-v44-hankel-resonance-2026-09-26`. The existing `v44-resonance-width` branch is not modified. The new referee-ready branch is created only after the build and separate core rebuild succeed.

[English article](paper.pdf) · [Native source](main.tex) · [Response to r29](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core sources](evidence/CORE_SOURCES.zip) · [Integer-interval compiler](finite_bit.py)

## Mathematical changes

For every finite orthogonal alphabet the optimized per-command distortion rate is bounded by the logarithm of every feasible common polytope dilation:

```
sup_(B>=1) [-log(1-Gamma_A(k,B))]/B <= log lambda_A(k,a).
```

Repeating an optimizing packet arbitrarily many times removes the initial inradius loss. No commutativity, gap or Diophantine assumption is required. This is a one-sided comparison, not an equality or characterization of arbitrary hidden width. A cut-dependent enclosure chain satisfies the corresponding cumulative interval bound.

The finite-horizon probability Hankel array has an exact normalized positive-realization formulation through compatible future-response polytopes. Its per-row compatibility defect has an explicit finite convex dual. For the planar experiment every cut has ordinary, nonnegative and normalized stochastic factor rank exactly three, while the compatible whole-run width grows. These are a normalization and application of classical realization ideas, already related to the v33 lift framework, not priority claims for positive cones or Hankel rank.

A separate uniform finite-bit model charges the horizon, current label, arithmetic, parameter storage, random words and counters. A table-free compiler achieves prescribed positive wordwise error with O(log N+log(1/epsilon)) work bits and exactly (N+2)b fair bits, where b=ceil(log2(16(N+2)/epsilon)). Integer interval arithmetic constructs stochastic dyadic rows; no floating-point library is trusted to certify a row. The clean stochastic register has q+1 labels and inherits the arithmetic upper exponents at a changed constant. Scratch configurations are not included in that clean-label count and are charged separately.

For the fixed explicit algebraic-angle alphabets the work-space order is Theta(log N), with lower bound r/(2r+1) log2 N-O(log log N). The O(log N) upper order alone is elementary by retaining all command counts and is not advertised as a new streaming-space discovery. The compiler additionally gives a positive stochastic realization with a small clean register, no per-label table, fixed finite draws and explicit cumulative-error accounting. Exact arbitrary-real atomic simulation remains a different model.

The complete v43 packet, interval, circle optimization, metric and irrational-fluctuation arguments remain in the present article. The minimal-type proof now retains the sharper minimum. The old weaker inequality was already logically implied by that minimum; the response records this rather than asserting a false counterexample.

## Reproduction

Python 3.12, SymPy 1.14.0, PyMuPDF 1.26.7 and an AMS-compatible TeX installation suffice for the core. The full historical regression build additionally uses mpmath, NumPy 2.3.5 and SciPy 1.17.0.

```sh
python papers/GTF-I-v44-hankel-resonance/verify.py
python -O papers/GTF-I-v44-hankel-resonance/verify.py
python papers/GTF-I-v44-hankel-resonance/finite_bit.py --horizon 16 --angles 2
python papers/GTF-I-v44-hankel-resonance/build.py --core-only
python papers/GTF-I-v44-hankel-resonance/build.py
```

The core archive extracts to one package. Run `python GTF-I-v44-hankel-resonance/build.py --core-only` from its parent. The full archive contains the exact predecessor files required for archival reproduction. No font files are distributed. The publication workflow pushes native sources before running the build, then publishes the article and evidence without force.

## Preservation and boundaries

[Unchanged v43 article](supporting-results.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

All older paths and branches remain unchanged. The complete v43 article is byte-identical as the supporting PDF; its cumulative volumes are appended without alteration. Large archives are excluded from the small referee package. The earlier calibration and expansion theorems remain at their original paths and hypotheses.

No general profile duality, exact finite hidden-width optimum, all-irrational classification, precise Liouville limsup, independent priority certification, original-page LPS audit or unrelated analytic pipeline closure is claimed. Published proof arguments, not finite tests or archive volume, establish the stated mathematical claims and remain subject to independent scrutiny.
