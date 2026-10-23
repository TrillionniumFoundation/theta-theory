# R74 author-team mathematical development: contracting and observed instruments

This is an author-team research record, not an independent referee report or
an editorial recommendation. The native draft is `draftnoisy.tex` and the
executable diagnostic is `diagnostics_r74_noisy.py` in this directory. No
existing manuscript, report, historical branch, or remote ref was edited by
this research subtask.

## Main mathematical result developed

For every nonreal phase `z=exp(i theta)`, use the qubit instrument

\[
\Psi_0(X)=\tfrac18 U_\theta XU_\theta^*,\quad
\Psi_1(X)=\tfrac14\operatorname{tr}(EX)|0\rangle\langle0|,\quad
\Psi_2(X)=\operatorname{tr}(X)I/2-\Psi_0(X)-\Psi_1(X),
\quad E=\operatorname{diag}(3/4,1/4).
\]

The residual Choi matrix is at least `I_4/16`, uniformly in the phase.
The stationary start is `I/2`; the output process is one-dependent, has
word-Hankel rank exactly three, and every one-step conditional output
probability lies in the fixed intervals `{1/8}`, `[1/16,3/16]`, and
`[11/16,13/16]`. Its unconditioned channel is completely depolarizing in
one step.

Nevertheless its exact classical memory is:

| Phase | Free mixed start | Prescribed pure start |
|---|---:|---:|
| Primitive root of order `q>=3` | `q` | `q+1` |
| Not a root of unity | Infinite | Infinite |

The lower proof starts from **any** nonnegative outcome-matrix model. The
word probabilities

\[
p(1\,0^n\,1)=\frac{8^{-n}}{64}\bigl(1+\tfrac12\cos(n\theta)\bigr)
\]

force a relative peripheral eigenvalue of the zero-outcome matrix. An active
core path inequality bounds its spectral radius by `1/8`; Perron scaling and
the unit-circle equality case force every required cycle length to be a
multiple of `q`. This proves the lower and the infinite alternative.

At equality with `q` hidden labels, the entire zero-outcome matrix is a
weighted `q`-cycle. Under a pure start, `p(0^n)=8^{-n}` forces all weights
to equal `1/8`; `p(0^n1)=8^{-n}/8` forces the outcome-one terminal column
to be constant. The latter contradicts the displayed oscillation. Thus the
initializer costs exactly one extra label in this family.

For the upper, a regular `q`-gon of physical pure states is invariant under
normalized branch zero and contains the reset state. Every normalized branch
two output has Bloch radius at most `5/11`, smaller than the polygon's
inradius `cos(pi/q)>=1/2`. Barycentric decomposition gives exact nonnegative
outcome matrices and every word identity. A stationary hidden row can be
obtained by Cesaro averaging without changing the physical barycenter.

The fixed algebraic phase `(3+4i)/5`, with
`U=5^(-1/2) [[2,-1],[1,2]]`, gives rational superoperators and no finite
classical realization. Finite-order phases give algebraic primitives and
arbitrarily large exact memory in the same physical dimension and under the
same uniform positivity and dependence bounds. The theorem does not claim
that mixing, predictive rank, or output positivity have never been separated
from finite hidden-state realizability before.

## Additional common-contraction theorem

A finite command response `b(w,c)=p_c+ell_c(x_w)` with
`x_wa=F_a x_w`, a supplied common norm contraction `||F_a||<=rho<1`,
and a ball `rB` on which every decoder is legal has one exact stochastic
realization on all mixed words. The proved live-label upper is

\[
\sum_{j=0}^{T-1}|A|^j+
\left\lceil\left(1+\frac2{1-\rho}\right)^n\right\rceil,
\qquad \rho^{T-1}\|x_0\|\le r.
\]

A maximal norm-net gives a common invariant polytope; transient prefix
labels enter it at a certified depth. The full proof retains a pure initial
label and bounded probability decoders. This is a quantified application of
classical invariant-polytope positive realization, not a claim to originate
that principle or decide joint spectral radius. A supplied common quadratic
norm gives finitely checkable matrix inequalities; a supplied uniform product
bound also implies the hypothesis through an explicitly defined norm.

## Inherited closure corrected

The four-period response already has its sharp transition as a consequence of
R69 Theorem `thm:r69-sector-phase` at `M=3`, `theta=pi/2`:

\[
m=2\text{ at }\alpha=0;\qquad
m=3\text{ on }0<\alpha\le1/\sqrt3;\qquad
m=4\text{ on }1/\sqrt3<\alpha\le1.
\]

R73's finite-gap interval `[89/90,1]` remains a valid different statement.
The new draft marks this sharp law as an inherited corollary, correcting any
impression that this specific first transition remained open. It is not
counted as a new independent spectral discovery.

## Primary literature actually inspected

- Cihan Okay, *Polyhedral classical simulators for quantum computation*,
  Research in the Mathematical Sciences 13 (2026), article 55,
  DOI [10.1007/s40687-026-00626-x](https://doi.org/10.1007/s40687-026-00626-x).
  Publisher full text was opened. Theorem 16 gives instrument updates from
  preservation; Lemma 17 proves adaptive composition; Corollary 19 gives exact
  sampling of the resulting adaptive output law. These are direct antecedents
  for the simulation mechanism. The proposed work's quantitative posterior
  condition and exact conditional-cycle memory law must be distinguished from
  that framework. Full-text searches for `noise` and `strict` returned no
  matches; this bounded check is not a proof of worldwide priority.
- Alexander E. Holroyd and Thomas M. Liggett, *Finitely dependent coloring*,
  DOI [10.1017/fmp.2016.7](https://doi.org/10.1017/fmp.2016.7).
  The [author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/4col.pdf)
  was opened; its introduction, Theorem 1 and Proposition 3 establish prior
  one-dependent processes without finite-state hidden Markov representations.
  Therefore the qubit construction must not be advertised as the first
  one-dependent non-HMM. Its additional uniform positivity, rank-three,
  physical instrument and exact finite-order counts are the specific claims.
- Alex Monras and Andreas Winter, *Quantum learning of classical stochastic
  processes: The completely-positive realization problem*,
  [TQC 2014 primary proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99)
  and [arXiv 1412.3634](https://arxiv.org/abs/1412.3634).
  These were retrieved as the established quantum positive-realization
  antecedent, already cited in the inherited manuscript. This subtask did not
  claim a new polyhedral-cone characterization.
- M. Vidyasagar's *The complete realization problem for hidden Markov models*
  was located as a relevant mixing/ultra-mixing antecedent. The apparent
  author-hosted PDF at
  `https://personal.utdallas.edu/~mxv091000/Research/hmm-full.pdf` redirected to
  a university webpage-responsibility notice. This subtask therefore did not
  claim to have checked that full paper's technical hypotheses. The public
  author publication list identifies its 2011 journal version and DOI
  `10.1007/s00498-011-0066-7`.

## Executed diagnostics

`diagnostics_r74_noisy.py` completed under ordinary Python and `python -O`.
The output JSON files are byte-identical. The completed suite has **9,012 exact
checks**, no floating probes, and no assert-based checks.

The suite checks all principal minors of the explicit qubit Choi matrices
(including the residual lower bound), stationary and one-dependent cylinder
identities, 49 oscillatory cylinder values and a rank-three Hankel minor,
uniform conditional probability bounds on a finite ternary tree, and concrete
`q=3,4,6` classical instrument constructions in both phase directions. The
finite-order constructions use rational coordinates and exact row-state
intertwining. A separate 19-label machine for two noncommuting contractions
has exact coordinate intertwining and finite mixed-word comparisons. The
period-four checks implement the inherited threshold construction.

These finite computations do not prove the universal statements, minimality,
infinite-memory obstruction, priority, or editorial suitability. Those
mathematical claims require the written proofs and appropriate assessment.

### Current file identities

- `draftnoisy.tex`: SHA-256
  `66d30f83d0a230b9c4eac380098b914505114b6ed9e8a466af5016bbd6d4038f`.
- `diagnostics_r74_noisy.py`: SHA-256
  `a29e32bcef2d9dd7caaa9551f5e87f3c2cf6c73933609f1e513660148dfa198a`.
- Both completed diagnostic JSON outputs: SHA-256
  `c89b6411e9d5201d6b569c3443c6695a5ce61ffe25d5b23f8dec2da7b9ffd20b`.

The manuscript draft was not compiled separately by this subtask; integration
and the source-bound native build belong to the main revision workflow.

## Controlling historical attribution correction

The completed historical audit found that the proposed posterior-positivity
Section 39 had already been proved, in a stronger form, in retained R68
`sections/27-interior-instruments.tex`. I directly reread that source at
SHA-256 `a332eeddf728e01cc907b3e19cbff526539e65a1ff823aa1b366fa87b75aebe8`.
It already has the projective-net bound, adaptive and stopped-law transfer,
algebraic construction, sparse branch rows, several preparations, counted
finite blocks, and the stronger universal physical-dictionary lower
`s^(-(d-1))`. Earlier wording in these notes distinguishing a proposed
quantitative posterior condition from external frameworks must therefore
not be interpreted as an R74 novelty claim: that condition and its theory
are inherited R68 content.

The duplicate draft and weaker dictionary supplement are now preserved in
`provenance/author-research/superseded/`; active Section 39 is an unnumbered
bridge to the retained theorem. Its existing proof challenge remains a
correctness assessment of the specifically hashed draft, not a priority
clearance. The separate **873-check** `diagnostics_r74_instruments.py`
ordinary/optimized run is fresh finite validation of **retained R68**,
not validation of a new R74 general theorem. Nothing about the executed
diagnostic counts or hashes is retracted or silently rewritten.

The current contribution centers are Sections 37--38's group contrast and
quotient laws and Section 41's exact unrestricted-memory classification.
Section 40 supplies an explicit common-contraction certificate and counted
construction as an application of established positive-realization geometry.
The latter is not advertised as originating invariant polytopes.

## Additional bounded primary-source priority comparison

I opened the [Fanizza--Lumbreras--Winter publisher full text](https://link.springer.com/article/10.1007/s00220-023-04913-4)
and examined Section 2.3, Theorems 1--2, and Section 4.2, also comparing the
[author arXiv PDF](https://arxiv.org/pdf/2209.11225). The paper constructs
binary qubit/qutrit conjugation-and-reset processes, credits older FRDN
commensurate-phase exact classical minima, explains the peripheral-phase
obstruction for irrational phases, and proves a noisy worst-phase memory
lower. Thus neither phase-order memory dependence nor the irrational
finite-HMM obstruction is a new general mechanism here. The current
three-outcome family's simultaneous exact depolarization, one-dependence,
uniform outcome floors, rank three, and separately sharp pure-initializer
charge were not identified in those inspected statements and constructions.
This is a bounded comparison, not an exhaustive novelty clearance; no
unchanged transfer of their phase-denominator convention is made.

I also reread Theorem 1 and the Section 5 proof of Proposition 3 in the
[Holroyd--Liggett author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/4col.pdf).
Their one-dependent proper coloring and finite-HMM obstruction establish
the earlier general phenomenon. Proper coloring forbids repeated adjacent
symbols, whereas this qubit family's positive conditional lower bounds make
every finite word positive. Their coloring parameter is not the phase-order
memory parameter of this family. The earlier phenomenon is fully credited;
the present claim concerns the stated simultaneous properties and exact
initialization-sensitive law, not first existence of a one-dependent non-HMM.
