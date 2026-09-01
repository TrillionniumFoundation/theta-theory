# Independent Referee Report — Round Sixteen

**Paper:** `B1 — Microcanonical Preparation`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/B1-microcanonical-preparation`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/B1_POSITIVE_CANONICAL_FOURIER_SHELL.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate responds directly to two fatal defects in the controlling manuscript. It removes the frequency-independent additive term from the proposed high-frequency majorant, and it no longer applies a Chernoff bound directly to signed Mayer activities. Instead it asserts an exact positive regenerative/compound-Poisson block law for connected hard-sphere components and derives one globally integrable Fourier estimate for the canonical coefficient.

The desired conclusion is exactly what the microcanonical argument needs. The positive block law, however, is not proved and is generally incompatible with the geometry of an interacting hard-sphere gas.

## Major objections

### 1. Connected components are not an independent compound-Poisson family

A deterministic configuration can certainly be decomposed into connected collision or exclusion components, and the measure of each configuration is positive. It does not follow that the component collection is a Poisson process or a sequence of independent regenerative blocks.

Distinct components remain coupled by the requirement that they do not overlap and by the finite-volume geometry. After integrating the internal coordinates of each component, there is still an inter-component exclusion constraint. The exact canonical coefficient therefore has the structure of an interacting polymer gas, not a product law of independent positive blocks.

The manuscript's “positive block law” drops precisely this residual interaction. No bijection or Jacobian is given that turns the canonical hard-sphere measure into the claimed compound-Poisson distribution. Positivity of the original phase-space measure is not a proof of independence.

### 2. The proposed replacement silently reintroduces cluster activities

If the inter-component exclusion is expanded away, one returns to connected cluster/polymer activities. Those activities carry alternating signs and cannot be used as probabilities. If the exclusion is not expanded, the block variables are dependent and the stated Chernoff/characteristic-function factorization fails.

The candidate does not resolve this dichotomy. It calls the weights “positive canonical component weights” while using the exponential formula appropriate to independent labelled components. The exponential formula is exactly the step that requires factorization and is absent.

### 3. The global Fourier majorant has no rigorous source

The manuscript states a single bound of the form
\[
|\widehat p_N(u)|\le G_N(u),\qquad
\int_{\mathbb R^d}G_N(u)\,du<\infty,
\]
covering central, intermediate, and large frequencies. The central Gaussian estimate is plausible in a low-density regular regime, but the intermediate and high-frequency decay is deduced from the unproved block law.

For the exact canonical density, one must control dependencies, hard-core singularities, and the fixed-number constraint. No smoothing component with a uniformly positive weight is identified in the actual canonical measure, and no integration-by-parts estimate is proved uniformly over all remaining particles. The earlier infinite-domain problem has been removed from the statement, not solved in the proof.

### 4. Exact coefficient positivity is not enough for a local limit theorem

The canonical coefficient itself is positive. A pointwise multivariate local limit theorem additionally requires a nondegenerate covariance, aperiodicity/nonlattice control, uniform derivative bounds, and a denominator lower bound at the chosen shell. The candidate treats these as consequences of the positive representation. They are not.

In particular, a mixture of positive component laws may still have near-lattice directions or a characteristic function close to one on large frequency sets. The paper provides no uniform spectral gap away from the origin.

### 5. The microcanonical transfer remains circular with B2

The collision-current microcanonical law is obtained by conditioning the grand-canonical dynamic LDP on exact number/energy/momentum shells. Its denominator estimate is B1, while several parameters in the B1 block construction are imported from the B2 collision genealogy expansion. B2 in turn invokes B1 for the microcanonical conclusion. The candidate does not separate the grand-canonical input from the exact-number coefficient theorem well enough to avoid circularity.

## Genuine progress

The authors are right that a proof must be based on a positive finite-volume object and one integrable Fourier majorant. The candidate also correctly avoids using signed Mayer weights as probabilities. These are necessary corrections. They are not sufficient because the asserted positive independent block law is the missing theorem itself.

## Dependency and editorial significance

B1 is the conditioning root for the hard-sphere microcanonical chain:
\[
B2_{\rm GC}\longrightarrow B1\longrightarrow B2_{\rm MC}
 \longrightarrow B3\longrightarrow B4.
\]
Without a valid exact-number coefficient theorem, none of the source-conditioned or microcanonical conclusions downstream has a controlled normalizing denominator.

## Minimum requirements for a new submission

A credible proof must do one of the following:

1. derive the exact coefficient directly from the positive canonical phase-space integral, with a genuine global Fourier estimate; or
2. prove a regenerative decomposition including the residual inter-block interaction and quantify why it is negligible at the required scale; or
3. use a positive probabilistic coupling/Stein method that does not factor the interacting components.

In all cases, the theorem must include uniform nonlattice and covariance estimates and a noncircular statement of its B2 inputs.

## Verdict

**Reject.** The candidate removes two explicit errors from the previous manuscript, but replaces them with an unproved exact compound-Poisson representation of an interacting hard-sphere gas. The canonical local limit theorem and the microcanonical denominator remain unavailable.
