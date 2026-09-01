# Independent Referee Report — Round Sixteen

**Paper:** `A3 — Full Empirical-Path LDP`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/A3-full-empirical-path-ldp`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/A3_EXACT_TERMINAL_EDGE_LDP.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate explicitly repairs the previous terminal-edge accounting error. It augments the stopped renewal path by a terminal branch label and profile and charges
\[
H(\nu^{\mathrm T}\mid w)
\]
for selecting that branch in full, rather than multiplying the branch-selection entropy by the fraction of the roof already traversed. It also retains predictable entropy controls and recession coordinates for clock defects.

This is the correct direction. Nevertheless, the main path-space LDP and its recovery theorem are not established.

## Major objections

### 1. The controlled-chain lemma uses spectral information that arbitrary predictable kernels do not possess

The candidate allows time-inhomogeneous predictable transition kernels \(\nu_i(\cdot\mid\mathcal F_{i-1})\) subject only to absolute continuity and a relative-entropy budget. It then invokes the A2 vector–return–roof local theorem as though the same Dolgopyat/nonlattice estimate held along the controlled chain.

It does not. Spectral estimates for one stationary transfer operator do not survive arbitrary predictable changes of the branch law. Finite relative entropy does not imply a uniform spectral gap, a uniform nonlattice condition, or the high-frequency cancellation needed for a local coefficient theorem. A controller may concentrate on branches with nearly arithmetic roofs or poor transversality while paying finite entropy.

A valid weak-convergence/entropy proof must either avoid such a controlled LLT entirely or establish a new uniform theorem for the exact admissible control class. The manuscript does neither. The “controlled-chain lemma” is the main lower-bound theorem in disguise.

### 2. The augmented terminal variable is not automatically the physical stopped path

Charging the complete terminal branch entropy is correct for an augmented random variable that actually records the full branch label/profile. The physical stopped trajectory, however, generally records only the prefix up to the observation horizon. Different completions of that prefix may correspond to different full branches.

The candidate alternates between an augmented marked graph and the physical empirical path without proving the contraction between them. If the theorem is for the augmented object, it must say so and then contract over all compatible terminal completions:
\[
I_{\rm phys}(\gamma)
 =\inf\{I_{\rm aug}(\gamma,a,\rho): (a,\rho)\text{ completes }\gamma\}.
\]
If the full terminal label is claimed observable, the microscopic definition must demonstrate that observability. Merely adding the label to the state space does not identify the LDP of the original path statistic.

Thus the old fractional-cost error is removed, but the relation between the repaired rate and the advertised observable remains incomplete.

### 3. Exponential tightness with recession clocks is not proved

The state space includes stopped paths, renewal measures, a terminal edge, singular clock components, and recession coordinates. The proof says that entropy and roof moments give compactness, but no compactness theorem is stated for this graph-completed topology.

In particular, the authors must control simultaneously:

* oscillation of the path between renewals;
* accumulation of short returns;
* escape through long terminal roofs;
* singular limits in which clock mass concentrates;
* compatibility of the terminal mark with the limiting prefix.

Moment bounds for the roof do not alone yield exponential tightness of all these coordinates. The lower-semicontinuity of the proposed recession functional and closure of the balance constraints are also not demonstrated.

### 4. The recovery sequence is asserted for a much larger class than is constructed

The candidate states a lower bound for arbitrary predictable finite-entropy controls, including singular/recession targets. The recovery argument consists of smoothing, truncating, and concatenating controlled branches. It does not prove that the resulting microscopic law has the required exact return count, homology, roof clock, and terminal mark simultaneously, nor that the entropy converges without an additional boundary cost.

The terminal edge is especially delicate: selecting a branch in full while stopping inside it requires a consistent change of measure on the entire branch and a contraction back to the observed prefix. No such construction is written.

### 5. The theorem depends on the unproved A2 raw LLT

The candidate repeatedly uses the Round-Sixteen A2 coefficient theorem for local normalization and exponential estimates. As explained in the A2 report, that theorem rests on an invalid trace-class compensation. Consequently the present LDP lacks its principal analytic input even before the controlled-kernel problem is addressed.

## Genuine progress

The candidate should be credited for eliminating a real inconsistency:
\[
\text{branch selection cost is paid once and in full.}
\]
That correction should be retained. It does not, however, supply the missing controlled path-space upper/lower bounds.

## Dependency and editorial significance

A3 feeds the history and memory constructions in A4 and later C2/D1. The downstream papers require a proved good rate function on the exact stopped-path topology, not a formal entropy formula. At present that interface is not closed.

## Minimum requirements for a new submission

A new version should:

1. define unambiguously the microscopic observable—physical prefix or augmented terminal mark;
2. derive the physical rate by a written contraction if an augmented process is used;
3. prove exponential tightness and compactness in one explicit graph-completed topology;
4. construct recovery sequences for regular, singular, and recession targets;
5. either restrict controls to a class with a proved uniform spectral theorem or remove the controlled LLT from the argument;
6. rebuild the normalization only after A2 has a valid raw coefficient theorem.

## Verdict

**Reject.** The terminal entropy is now counted correctly, but the path-space LDP still relies on an unjustified controlled spectral lemma, an unproved augmented-to-physical contraction, and a nonexistent recovery theorem at the claimed level of generality.
