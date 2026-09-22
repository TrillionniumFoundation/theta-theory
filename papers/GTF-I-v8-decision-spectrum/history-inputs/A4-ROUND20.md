# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `d95d41a73c7a0e924474133362b2661691e33113`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

No new A4 mathematics appears on the declared revision branch. The active source is exactly the file reviewed in Round Eighteen. No variation-rate correction, Harris proof, fixed-space multiplier construction, renewal theorem, or transmission-zero analysis has been added. The previous report remains controlling.

## 2. Unresolved fatal defects

### 2.1. Summable variation is still incorrectly upgraded to exponential variation

The hypothesis remains `\sum_n \operatorname{var}_n(\log g)<\infty`, while `lem:r17-a4-coupling` concludes a total-variation bound `Ce^{-cN}`. Summability alone allows polynomial and other subexponential tails. The correct coupling rate must be derived from the actual variation modulus. Consequently the small-distance contraction in the exponentially weighted history metric has no proved foundation.

### 2.2. Drift, minorization, and operator spectral gap remain asserted

A uniform exponential moment for the next edge may yield a bounded expectation, but the stated Lyapunov drift and its compatibility with the full history weight are not proved. The small-set argument still confuses “finitely many cylinders carry most mass” with a common minorization valid for every state in a Lyapunov sublevel. Common word lengths, uniform Gibbs lower bounds, a common terminal measure, and continuous suspension coordinates are not treated.

Even a valid weak-Harris Wasserstein contraction does not automatically produce the announced bounded-operator spectral decomposition on the particular weighted Lipschitz space. Invariance, completeness, the dual norm, and a Doeblin–Fortet estimate are still missing.

### 2.3. The Feynman–Kac source class is still not a fixed multiplier algebra

The class permits logarithmic growth, so products may grow quadratically in `\log W`; it is not an algebra as stated. The estimate `e^{|V|}W^\theta\le C W^{\theta'}` maps to a heavier weight and does not show that `P(e^V\cdot)` is a bounded analytic family on one fixed `\mathcal B_\theta`. No return/smoothing estimate from `\theta'` to `\theta`, no uniform eigenfunction inverse bound, and no valid fixed-space perturbation theorem are supplied.

### 2.4. Scalar A2 bounds still do not imply the operator renewal theorem

The source continues to promote A2 matrix coefficients for a specific induced operator into meromorphic continuation and vertical-line integrability for a history-kernel suspension resolvent, uniformly over an infinite-dimensional source ball. No Fredholm family, compact perturbation, complement estimate, common graph domain, or relation between the two operator realizations is constructed. Analytic reduction on a leading finite-dimensional projector does not control the essential complement.

### 2.5. Transmission-zero promotion remains unproved

The paper still asserts that finitely many left-half-plane zeros can be adjoined to the resolved space and thereby removed. It does not prove finiteness, stable multiplicity, uniform Riesz ranges, preservation of the common domain, or termination of the iteration. Changing the resolved projection changes the compressed resolvent and may create new zeros. Meromorphicity alone does not yield the vertical decay needed for inverse Laplace contour shifting and exponential memory integrability.

## 3. Editorial consequence

A genuine revision must state the actual variation rate, prove a model-specific Harris theorem and the exact operator gap used later, construct a fixed analytic operator scale, and establish an operator-valued renewal/memory theorem with complete domain and contour bounds. None is present.

## 4. Recommendation

**Reject without reconsideration.** The paper remains a chain of unsupported upgrades rather than a completed theorem.