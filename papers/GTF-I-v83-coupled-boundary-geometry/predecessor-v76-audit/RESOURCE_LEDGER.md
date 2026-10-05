# Resources and interfaces — Revision 76

The new results distinguish a supplied-pair distance comparison in every finite input dimension, optimal-order reusable descriptions, and a common experiment learning an unknown qubit effect. Their complete machine-readable ledger is `RESOURCE_LEDGER.json`.

## 1. Measurement interface and dimensions

An effect `0 <= E <= I_d` specifies the ordered binary measurement `(E,I_d-E)`. Each memoryless call consumes its input and returns a classical outcome without residual quantum output. The finite-use distance is the supremum of the **unhalved** final joint-state trace norm over common experiments with at most `N` calls, allowing retained references, input entanglement, feedback, and bounded public stopping. Its maximum is two and its one-use value is `2 ||E-F||_op`.

In the matrix theorems and `matrix_metric.py`, `d` is the complex Hilbert input dimension. In inherited `biased_codec.py` and `coupled_codec.py`, `dimension=2` or `3` counts real Bloch coordinates of a qubit. The latter value does not designate a qutrit. Each schema states its convention.

## 2. Reusable descriptions

For fixed `d`, `N >= 1`, and `0 < delta <= delta_d`, the optimal fixed-length payload is

\[
\frac{d^2}{2}\log_2N+\lfloor d/2\rfloor\log_2\log(N+2)
       +d^2\log_2(1/\delta)+O_d(1).
\]

All identifiable effect coordinates are charged. A decoder selects one legal memoryless measurement of the same ordered binary interface. The converse permits every legal centre; rational centres attain the upper order. The covering proof in arbitrary dimension establishes existence through actual operational-ball volumes and rational approximation. It does not deliver a computationally optimized arbitrary-dimensional codebook generator.

The implemented joint qubit encoder receives rational bias and Cartesian coordinates, handles irrational Bloch norm, and charges both spectral indices and the identifiable direction in one integer index. Its canonical decoder and target replay are retained. Finite enumeration time, work tables, coefficient lengths, interpreter memory, expanded matrices, and JSON envelopes are separate from the payload. Public dimension, horizon, and accuracy are declared as such.

## 3. Common unknown-device learning

Theorem `thm:commonlearn76` treats every biased qubit effect, with bias, contrast, and direction unknown. It proves a uniform risk at most `eta` for error `delta` in the future-`N` adaptive distance, with matching worst-case training calls of order

\[
N\delta^{-2}\log(1/\eta).
\]

Here `N` is the **future horizon in the loss**, not the training-call budget. The upper budget holds on every record. The range is sufficiently small `delta` and `0 < eta <= 1/8`.

The construction permits ideal trusted preparation of the specified finite states, memory for the unused inputs of a GHZ block, fair random signs, and classical feedback. Every entangled block has at most `N` calls. At large contrast, empirical amplitudes choose a length comparable to `min(N,1/(1-r))`. At small contrast, variance-sensitive product observations suffice. Fresh endpoint samples follow the estimated direction in both branches, with conditional confidence bounds for random frames and decisions.

Rational rounding and the retained exact qubit code turn the final estimate into one optimal-order reusable word with no further device calls. Classical arithmetic time, mutable workspace, state-preparation hardware, and quantum memory are not optimized by the call-count theorem. The manuscript gives the complete learner construction; finite checks verify its algebraic ingredients. No physical-device training session or full learner software implementation is represented as having run. Pair-dependent witnesses and a supplied-target encoder remain distinct from this common experiment.

## 4. Exact matrix-pair certificate

`matrix_metric.py` accepts Gaussian-rational Hermitian effects and solves

\[
VX+XV+N^{-1}X=F-E,\qquad
V=\tfrac12(E+F)\bigl(I-\tfrac12(E+F)\bigr).
\]

It returns `Q_N^2=N tr((F-E)X)`, the full solution, the exact squared bounds `min(1,Q_N^2)/(8192d)^2` and `min(4,64Q_N^2)`, and a canonical supplied-pair identity. Legality uses exact Schur elimination including zero pivots. Replay recomputes every field and checks the entire pair, including a pinned horizon when requested. This evaluates the proved modulus and does not optimize the adaptive distance.

Under conventional unit-cost field-operation accounting, PSD elimination takes `O(d^3)` operations. A dense `d^2`-variable Sylvester solve takes `O(d^6)` operations and `O(d^4)` stored field elements. Integer growth, input bit lengths, the size of `N`, and interpreter overhead are additional costs; these are not optimal bit-space guarantees. `MATRIX_METRIC_SCHEMA.md` specifies the executable representation.

## 5. Inherited resources and evidence

The complete edition retains all earlier stochastic label-width, numerical streaming-space, state-precision, rational-compilation, instrument-description, and conditional-state resources under their original hypotheses. The v75 ledger and older audits remain preserved. The learning theorem does not change those models.

Finite exact checks support implemented legality, linear algebra, GHZ identities, and budget calculations. The build checks ordinary/optimized agreement and reproduces pages from frozen sources. The continuum geometry, entropy, and minimax statements are established in the written proofs. Source reconstruction does not establish an independent priority judgment, human authorship signature, or closure of the separate A/B/C/D analytic programme.
