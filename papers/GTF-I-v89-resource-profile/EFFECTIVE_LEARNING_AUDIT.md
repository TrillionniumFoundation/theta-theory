# Revision 80 effective optimal learning audit

## 1. Object, outcome, and inherited boundary

This audit concerns `sections/63-effective-optimal-learning.tex`. The
theorem constructs a **new effective collective learner** at the existing
optimal interior query order. It does not claim to compute the operators
of Mele–Bittel's continuous estimator or to compile that estimator into
an efficient circuit.

The v79 Section 61 chain was read independently, including its entropy
packing, exact interior dictionary, prefix-description converse, and
learned-code argument. No blocking defect was found. In particular, that
section correctly states that a Borel finite partition of a tomography
outcome gives an abstract finite-outcome POVM. It also correctly retains
the ideal-control model: finite output range alone does not supply
computable measurement entries. Section 63 closes that latter resource
gap without modifying Section 61.

The new source and its mathematical mechanism have received an additional
independent proof read. No blocking defect was found. One literal
correction from that review was applied: the **real and imaginary parts**
of each Choi-record entry are rational-coefficient polynomials; individual
complex entries need not themselves have real rational coefficients.
Compilation and finite software checks, if any, are recorded separately
and are not treated as proofs of the continuum risk theorem.

| Object | Stable source label |
| --- | --- |
| Effective synthesis section | `sec:effectivelearning80` |
| Polynomial subnormalized Choi record | `eq:choirecord80` |
| Conditional readout probabilities and legality | `eq:readoutpolynomial80` |
| Decidable algebraic readout selection | `lem:algebraicreadout80` |
| Uniform success predicate | `eq:readoutfeasibility80` |
| Effective optimal learning theorem | `thm:effectiveinterior80` |
| Actual statistical guarantee | `eq:effectiverisk80` |
| Query order | `eq:effectivecalls80` |
| Description order | `eq:effectivepayload80` |
| Existence margin | `eq:effectiveexistence80` |
| Per-event physical-control allowance | `eq:effectivecontrolbudget80` |

## 2. Exact theorem range and claims

The executable public inputs are integers `d,N >= 1` and rationals

\[
0<\delta\le2^{-13},\qquad0<\eta\le1/8.
\]

The target family is the unchanged full-dimensional interior
`I/4 <= E <= 3I/4` of ordered binary effects. The channel consumes its
input, returns the ordered classical bit, and supplies no residual
quantum system or measurement environment. The future loss remains the
unrestricted adaptive unhalved distance `d_N`.

The new learner has

\[
\sup_{E\in\mathfrak I_d}\Pr_E\{d_N(E,C)>\delta\}\le\eta,
\]

\[
M=O\!\left(\frac N{\delta^2}
       \left[d^2+d\log(1/\eta)\right]\right),
\]

and a fixed deterministic public decoder with

\[
B=\frac{d^2}{2}\log_2N+d^2\log_2(1/\delta)+O(d^2).
\]

All constants are absolute. The actual number of queries is a fixed
integer found before acquisition begins. Only independent one-call
probe–reference pairs are prepared; collective processing occurs after
all queried probes have been consumed. The construction therefore
belongs to the fresh-block class with `b=1`, and hence to each allowed
larger cap.

The training optimality refers to `thm:interiorconfidence80` in Section
62. The fixed-decoder description optimality is the interior covering
converse in Section 61. Neither assertion extends the sharp dimension
factor to the complete effect body.

The completed Section 62 source was also checked directly. Its
dimension-dependent rational seed, Borel majority-neighbour selector,
and independent Choi acquisition provide exactly the existence input
used below, including when `d=1` and at arbitrarily small positive
confidence. Its separate lower-bound recurrence permits distinct
quantum inputs under the null and alternative hypotheses, retains the
same null experiment when summing coordinate counts, and accommodates
bounded stopping by ignored padding. No blocking defect or mismatch in
the Section 62 interface was found.

## 3. The polynomial quantum statistical model

One maximally entangled input/reference pair produces the normalized
Choi state

\[
\Gamma_1(E)=\frac1d
 \left(|1\rangle\langle1|\otimes E^{\mathsf T}
 +|0\rangle\langle0|\otimes(I-E)^{\mathsf T}\right).
\]

For `m` independent copies, condition on the recorded bit string `y`
without dividing by its probability:

\[
R_y(E)=d^{-m}\bigotimes_{\ell=1}^m E_{y_\ell}^{\mathsf T},
\qquad E_1=E,\quad E_0=I-E.
\]

These matrices are positive and their traces sum to one. Each real and
imaginary matrix coordinate is a rational-coefficient polynomial of
degree at most `m` in the real Hermitian coordinates of `E`. The
subnormalization is essential: normalized conditional states would
introduce target-dependent denominators and undefined zero-probability
branches.

The complete input to the final readout has dimension `(2d)^m`, but its
`2^m` outcome blocks are classical. The readout is parameterized directly
as a family `A_{j,y}` of POVMs on the `d^m`-dimensional retained references.
For every `y`, including strings of zero probability under a given
target, it satisfies

\[
A_{j,y}\succeq0,\qquad\sum_{j=1}^L A_{j,y}=I.
\]

The Born probabilities

\[
p_j(E;A)=\sum_y\operatorname{tr}(A_{j,y}R_y(E))
\]

are real polynomials with rational coefficients in `E` and the Hermitian
readout coordinates. If an existence proof initially gives a POVM on
the full classical–quantum register, dephasing its effects in `y`
preserves positivity, normalization, and every Born probability.
This verifies that synthesis does not require coherent access to a
classical device output.

## 4. The uniform success condition is exactly first-order

The dictionary `D(d,N,delta)` is the existing finite rational dictionary.
Let `k = ceil(sqrt(N))`, `a = delta/(8k)`, and `alpha = eta/2`.
For each center, define

\[
\mathsf{Good}_j(E)
\iff aI-(E-C_j)\succeq0\ \text{and}\ aI+(E-C_j)\succeq0.
\]

This is the exact condition `||E-C_j||_op <= a`. Its equality boundary
is included in success. Positive semidefiniteness is represented by all
principal minors, or by the equivalent real symmetric representation;
leading principal minors alone would be insufficient.

For each finite subset `S` of dictionary indices, the formula requires

\[
\left(\bigwedge_{j\in S}\mathsf{Good}_j(E)\right)
\wedge\left(\bigwedge_{j\notin S}\neg\mathsf{Good}_j(E)\right)
\implies\sum_{j\in S}p_j(E;A)\ge1-\alpha.
\]

Together with the universally quantified interior constraint, the
conjunction over all `S` is exactly the desired uniform success
condition. There is no approximation to the success indicator, no
unproved continuity assumption at a strict failure boundary, and no
finite-grid replacement for the quantifier over unknown effects.

The formula is very large, but finite. It uses rational coefficients
because the public tolerances and dictionary coordinates are rational.
Complex Hermitian variables are encoded by independent real coordinates.

## 5. Decidability, algebraic witnesses, and deterministic termination

Quantifier elimination first eliminates the effect variables while
leaving readout entries free. It produces a rational semialgebraic
feasible set in those entries. Exact positivity and normalization are
included in this set. Emptiness is decided before any witness search.

If the set is nonempty over the reals, real-closed-field transfer implies
that it has a point over the real algebraic numbers. A fully specified
selection can enumerate algebraic tuples through integer polynomials
and isolating rational intervals, using a fixed effective enumeration,
and test the quantifier-free formula by exact sign determination. This
enumeration terminates on the nonempty set.

The selected point satisfies the eliminated formula over the reals.
Consequently its risk guarantee holds for every real target effect,
including nonalgebraic targets. The proof does not merely check all
algebraic effects, nor assume that the unknown effect is supplied to
the constructor.

The outer algorithm tests `m = 1,2,...`. Each infeasible `m` is rejected
by a terminating decision, so it cannot stall at an impossible query
count. At the first feasible `m`, it extracts the algebraic family and
fixes `M=m`. This entire computation happens offline and uses no
unknown-device calls. No oracle for membership in a future adaptive
metric ball is used: the synthesized predicate is the sufficient
operator-norm ball explicitly displayed above.

There is no claim that the feasible set contains a rational optimizer.
It can have singular PSD boundary points or equality constraints with
only algebraic solutions. Exact algebraic sampling handles these cases.
The later physical approximation is paid in total variation and need
not itself satisfy the original semialgebraic feasibility conditions.

## 6. Why the first feasible query count has the sharp order

Section 62 supplies an independent-Choi operator estimator with failure
`eta/2`, legal output `F`, and target accuracy

\[
\epsilon=\delta/(64k).
\]

Its query count is at most an absolute constant times

\[
k^2\delta^{-2}\left[d^2+d\log(2/\eta)\right].
\]

This all-confidence result is used, rather than applying the simplified
Mele–Bittel corollary outside its confidence range. In particular, no
small-dimension exception arises when `eta/2 < 4 exp(-4d^2)`.

Clip the ideal estimator's output spectrally to `[I/4,3I/4]`, obtaining
`T`. On its good event, Weyl's inequality gives `||T-F||_op <= epsilon`
and hence `||T-E||_op <= 2 epsilon`. This argument does not require
clipping to be operator-Lipschitz for a noncommuting pair.

The existing dictionary rounding and predecessor rule give
`||T-C_j||_op <= 5 delta/(64k)`. Therefore

\[
\|E-C_j\|_{\rm op}\le7\delta/(64k)<\delta/(8k)=a.
\]

The conversion of the real-valued ideal outcome to this index is Borel,
including the prescribed rounding ties. Composing with the ideal
tomography measurement therefore gives a finite-outcome POVM satisfying
the synthesis predicate at its existing query count `m_0`. This is only
an **existence witness**. Its matrix entries, Haar integrals, continuous
randomness, and SDP output are never computed or provided as advice to
the algebraic constructor.

It follows that `M <= m_0`. The inequalities `k^2 <= 4N` and
`log(2/eta) = O(log(1/eta))` give the claimed query order. The search
need not know a numerical value for an absolute constant hidden in the
existence theorem in order to terminate.

Every ideal output counted as good satisfies

\[
d_N(E,C_j)\le4\sqrt N\,a\le\delta/2,
\]

because both effects lie in the extended interior of the
dimension-free metric comparison. This proves a sufficient event for
the original future loss; it does not change that loss.

## 7. Finite physical-control budget and exact decoding

For each recorded `y`, the algebraic readout admits the isometry

\[
V_y\psi=\sum_j|j\rangle_C|j\rangle_Z\sqrt{A_{j,y}}\,\psi.
\]

The positive matrix square roots have finite computable algebraic
descriptions, including on singular strata. Tracing out the copied
label and factor register gives the required classical channel.
A fixed final dephasing can be included when approximating its
Stinespring isometry. The finite target therefore preserves the
classical output type and exact CPTP constraints.

There are `M` fresh-pair preparations and one final readout event:

| Contribution | Unhalved error budget |
| --- | ---: |
| Each ideal instruction to its finite specified target | `eta/[2(M+1)]` |
| Each finite target to its actual trusted realization | `eta/[2(M+1)]` |
| Each complete trusted event | `eta/(M+1)` |
| Total over every executed record | `eta` |
| Total variation of ideal versus actual index laws | at most `eta/2` |
| Ideal statistical failure allowance | `eta/2` |
| Actual statistical failure | at most `eta` |

The preparation error concerns the complete fresh probe–reference pair,
tensor-separated from all stored references. A bound only on one
marginal would not suffice. The final readout bound is the complete
diamond norm, uniform over all classical strings `y` and all possible
retained reference inputs. Thus the guarantee includes unlikely,
zero-probability-in-the-ideal-model, and failed records.

If an implementation expands one trusted event into many elementary
known instructions, every instruction must be charged to the same
total budget. The query count is not asserted to bound the elementary
gate count. The source invokes the established normalized rational
state/isometry approximations from Section 59, with separate finite
specification and actual realization errors.

The output is a genuine finite index. The public decoder returns the
same exact rational effect in both ideal and actual experiments;
unused words retain their legal fallback. Therefore total variation
transfers the original failure event directly. No output legalization
error, decision-boundary stability, or additional `delta/N` control
precision is hidden in the argument.

## 8. Resource and scope ledger

The preparation and readout assumptions remain those of the finite
trusted-control model. They do not assert universal laboratory
implementability. All required target instructions and precision
requests are computable and finite; their availability at the certified
accuracy is the declared control assumption.

At the final selected query count, there are `2^M` conditional readouts,
each with `L` possible indices on a reference space of dimension `d^M`.
The quantum statistical register including the classical flags has
dimension `(2d)^M`. Describing the algebraic POVMs, performing quantifier
elimination, compiling isometries, and storing their coefficient tables
can be enormously more expensive than writing the final `B`-bit index.
No polynomial complexity claim is made for any of these tasks.

The full dictionary is unchanged and covers the interior, so its size
has both the upper and lower entropy orders. The same deterministic
decoder lower bound applies to any other finite-word learner with
positive success probability at every target. Shared-randomness prefix
codes remain governed by their separate Section 61 theorem.

## 9. Primary source boundary

The imported query-existence input originates in Mele–Bittel,
[arXiv:2512.10214v3](https://arxiv.org/html/2512.10214v3),
Section III.2 and Corollary III.9. Section 62 supplies its
all-confidence consequence used here. Section 63 does not assume
computability of the imported finite coarse-graining.

The real-algebraic tools are credited to Basu–Pollack–Roy,
*Algorithms in Real Algebraic Geometry*, second edition,
[DOI 10.1007/3-540-33099-2](https://doi.org/10.1007/3-540-33099-2),
Theorems 2.77 and 2.80 and Chapter 14. An author-authored accessible
account is Basu,
[arXiv:1409.1534v1](https://arxiv.org/html/1409.1534v1),
Sections 2.1, 2.2.2, and 2.5, covering effective quantifier elimination,
algebraic point representation, and sample selection. These supply
classical decidability and finite descriptions, not an efficiency claim
for the large readout problem constructed here.

The source's optimality and uniform risk remain mathematical theorems
with the stated proofs and imported inputs. This audit does not replace
an independent human specialist priority assessment or certify an
implemented theorem-scale tomography experiment.
