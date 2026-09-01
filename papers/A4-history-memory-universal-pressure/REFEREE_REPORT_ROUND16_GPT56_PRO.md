# Independent Referee Report — Round Sixteen

**Paper:** `A4 — History, Memory, and Universal Pressure`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/A4-history-memory-universal-pressure`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/A4_PATCHED_HARRIS_FORCED_MEMORY.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate tries to replace the earlier global-contraction assumption by a finite cover of regular charts, local Doob kernels and couplings, and a partition-of-unity “patched” kernel. On top of the claimed weak-Harris contraction it builds a weighted Riesz domain, a Schur multiplier algebra, a renewal resolvent, and a forced generalized Langevin equation.

This is a plausible research program, but the first patching step is not valid as written. Everything after it is therefore conditional.

## Major objections

### 1. The partition-of-unity kernel is either unnecessary or changes the dynamics

The candidate defines, schematically,
\[
\Pi(z,\cdot)=\sum_j\chi_j(z)\Pi_j(z,\cdot).
\]
There are only two possibilities.

* If all \(\Pi_j\) are restrictions of the same globally defined Doob kernel and agree on overlaps, then the sum equals that kernel and the partition of unity contributes nothing; the authors must prove the global kernel already exists and is regular.
* If the local kernels do not agree exactly, the formula defines a new state-dependent mixture, not the original deterministic/Doob dynamics.

The manuscript moves between these alternatives. “Uniqueness on overlaps” is asserted but no common construction or compatibility cocycle is supplied. A local chart representation does not automatically glue as a Markov kernel, especially across singular itinerary changes.

### 2. Local contraction does not convex-combine into global contraction

Even if the patched kernel is well-defined, the coupling estimate ignores that the mixture weights depend on the starting state. For nearby \(z,z'\),
\[
\Pi(z)=\sum_j\chi_j(z)\Pi_j(z),\qquad
\Pi(z')=\sum_j\chi_j(z')\Pi_j(z').
\]
A coupling must first match the component indices. It incurs a term controlled by
\[
\sum_j |\chi_j(z)-\chi_j(z')|,
\]
and, when different charts are selected, it requires cross-chart couplings between \(\Pi_j(z)\) and \(\Pi_k(z')\). The candidate simply averages the local same-chart contraction constants and omits these terms.

Near chart boundaries those omitted terms are the whole problem. No global weak-Harris estimate follows from the displayed calculation.

### 3. Drift and minorization are postulated rather than derived

The weak-Harris theorem needs a Lyapunov drift, a genuinely small set, and a contracting distance with uniform constants. The manuscript declares local drift/minorization packets and says compactness of the cover makes them uniform. It does not derive them from the broken-ray or induced dynamics, control the singularity set, or show that the small measures are compatible across charts.

A finite cover cannot turn chart-dependent minorization measures into one common minorization without a quantitative overlap argument. Nor does it control trajectories that repeatedly cross singular chart boundaries.

### 4. The multiplier algebra and renewal resolvent depend on the missing global estimates

The weighted Riesz representation and Schur multiplier claims require a closed common domain and quantitative bounds on multiplication, conditional expectation, and renewal convolution. Those bounds are deduced from the patched Harris estimate. Since that estimate is unavailable, the claimed sectoriality and inverse bounds are unsupported.

More specifically, the paper does not prove that the history-dependent multipliers preserve the form domain or that the renewal operator is bounded in the weighted norm. The statement “local estimates patch” is not a substitute for a graph-norm calculation.

### 5. The forced generalized Langevin equation is not obtained on a common domain

A formal Schur-complement/Mori–Zwanzig identity can be written for bounded matrices. Here the generator, projection, memory operator, and forcing term are unbounded and history dependent. The candidate does not establish:

* invariance of the common domain under the projected evolution;
* differentiability of the projected semigroup;
* convergence of the memory convolution;
* identification of the forcing term as an adapted object;
* equality of the formal resolvent expression with the claimed time-domain equation.

The result is therefore a formal identity, not a proved forced GLE.

### 6. Upstream inputs are not closed

The renewal normalization uses A2's raw coefficient theorem and A3's stopped-path LDP. Both remain unproved in the recovered Round-Sixteen modules. A4 cannot treat them as black-box theorems merely because the files appear in the same payload.

## Dependency and editorial significance

A4 is the intended bridge from the Sinai pressure/LDP theory to the common memory and cotangent constructions in C2 and D1. A bridge theorem must be more, not less, explicit about global topology, domains, and constants. The candidate instead hides the global construction in the word “patched.”

## Minimum requirements for a new submission

The authors must provide:

1. one globally defined Doob/history kernel, or a rigorous cocycle/gluing theorem proving that the local kernels agree;
2. an explicit coupling of the state-dependent mixtures, including the variation of partition weights and cross-chart terms;
3. derived drift and minorization estimates uniform through chart changes;
4. complete graph-norm estimates for the multiplier and renewal algebra;
5. a common-domain theorem for the projected resolvent and time-domain memory equation;
6. a proof that the A2 and A3 inputs used here are actually available.

## Verdict

**Reject.** The candidate replaces the earlier unproved global contraction by an invalid partition-of-unity argument. The multiplier, resolvent, and forced-memory conclusions all rest on that first missing theorem.
