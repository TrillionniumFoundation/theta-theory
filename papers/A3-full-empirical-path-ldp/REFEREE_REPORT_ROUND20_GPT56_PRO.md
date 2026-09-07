# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** A3 — *Full Liouville Empirical-Path Large Deviations and Information Projections for Finite-Horizon Sinai Billiards*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `51e25b360f2dbfe25c4e57be8231657446b816c1`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

The declared Round-Nineteen branch contains no revised A3 source. The active module is exactly the previously reviewed Round-Seventeen file. There is no new symbolic-model theorem, stopped-state construction, compactness proof, recovery theorem, or rate formula. The prior detailed rejection is therefore incorporated without qualification.

## 2. Unresolved fatal defects

### 2.1. The reference process is still not shown to be the Sinai process

The paper continues to replace the deterministic induced billiard by a countable one-step Markov edge chain with kernel `p(e\mid v)`. No derivation shows that conditional probabilities depend only on the current vertex rather than the full past. This is especially serious because A4 in the same series explicitly uses a history-dependent `g(e\mid x)` with summable variations. The two descriptions cannot both be exact without a nontrivial Markov reduction theorem.

The marks `r(e)`, `\tau(e)`, `\kappa(e)`, `\mathfrak s(e)`, and `\gamma_e` are also treated as constants of a countable edge. In a genuine inducing branch, roof and excursion data generally vary with the continuous point inside the branch. The paper neither augments the state with that coordinate nor gives an exact conditional marked kernel. Thus the entropy identity, though standard for a specified discrete chain, is not connected to the billiard experiment claimed in the title.

### 2.2. The topology and coercive cost remain undefined

The singularity/excursion cost `\mathfrak s` is assumed to possess precisely the exponential integrability and coercivity needed later, but it is not constructed. The completion of normalized excursions, one-sided germs, recession profiles, source/target metric, weighted weak topology, terminal compatibility relation, and local Skorokhod coordinates are not specified sufficiently to prove Polishness. “Taking a closed balance-compatible hull” does not create compactness without a prior relative-compactness theorem and closed compatibility maps.

### 2.3. Entropy control still does not prove stopped compactness or recovery

The entropy inequality supplies expectation bounds only after a suitable exponential moment is proved. It does not by itself handle the random number of return edges before collision time, the control-induced distortion of long returns, or tightness of every path and terminal coordinate. The recovery theorem still assumes quantitative strong connectivity, negligible connector words, approximation of unbounded marks, and realization of abstract recession atoms by legal billiard branches. None is proved.

### 2.4. The terminal-prefix and rate formulae remain invalid or incomplete

For continuous excursion data, an exact path prefix generally has probability zero. The expression `-\log P(prefix)` is therefore not the contraction of a positive-probability discrete event without a reference prefix measure, conditional density, or neighborhood local LDP. The collision-clock rate is still defined only as a lower-semicontinuous envelope of informally named costs under unspecified compatibility equations. That is not a checkable good rate function. The physical-time contraction and the claimed conditional LDP additionally require local numerator estimates that an ordinary joint LDP does not provide.

## 3. Editorial consequence

A revised paper must first construct an exact history/marked representation of the Sinai law, then define a complete stopped/recession space, prove controlled compactness with random edge counts, give a legal-flow approximation theorem, and state an explicit rate. No such revision has been submitted.

## 4. Recommendation

**Reject without reconsideration.** The manuscript remains an abstract entropy-control outline for an unproved surrogate process.