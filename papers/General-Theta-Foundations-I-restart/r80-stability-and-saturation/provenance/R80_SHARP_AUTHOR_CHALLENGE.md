# Author-side mathematical challenge: sharp primitive stability

## Scope and status

This is an internal author-side derivation and adversarial check of the new
sharpness section. It is not an independent referee report, human expert
assessment, formal proof-assistant verification, or editorial decision.

The controlling predecessor is the complete R79 instrument-frontier source.
Its general square-root primitive modulus is inherited. The new section
proves a matching obstruction with an explicit leading constant in a scalar
two-model, two-command, two-live-label family. The family is a member of the
general instrument class, so its local asymptotic proves sharpness of the
general exponent. Its special-model formulas are not promoted to formulas
for arbitrary instruments.

## Exploratory candidates and corrections retained

1. The first possible construction used the R79 symmetric perfect-command
   example: one command certainly succeeds in each model. That does not
   force the intended repair cost. An update following a previously
   impossible failure can be changed without affecting the other model's
   baseline cost. This candidate was rejected before any theorem claim.

2. The useful family makes command b succeed with probability beta strictly
   between zero and one in model 1. At zero perturbation, model 0 has a
   perfect command a and a dark command b. This makes escape from the
   pure-b continuation label costly in model 1 and necessary after a
   positive perturbation in model 0.

3. An initial first-call hazard bound suggested `1/beta + r` as a possible
   model-1 expression. It is only a lower bound and is not the cost of the
   proposed two-label program: a failed initial b call repeats the initial
   mixed row. Exact Bellman conditioning gives

   `C1 = (beta + r) / (beta * (beta + (1-beta)*r))`

   when the second row is pure b, a failures from the initial row enter it,
   and b failures keep their labels. This corrected expression was used
   throughout the final polynomial identity, baseline classification,
   asymptotic analysis and diagnostics. The discarded expression is not
   present in the manuscript as a claimed cost formula.

4. Finite differential-evolution probes performed in the parallel
   author-side challenge suggested the square-root scale for beta=1/4.
   Such probes can miss a singular boundary optimizer. They were not used
   as evidence of global optimality, and no optimizer output is required
   by the delivered diagnostics. The final proof covers all six controller
   probabilities, both row orientations, inaccessible dark labels, and
   arbitrary stochastic routing.

5. A proposed simple lower comparison for the opposite row orientation
   was too strong when the continuing command row and transition are both
   mixed. Direct symbolic expansion exposed a negative coefficient. It was
   discarded. The final proof instead imposes the exact model-0 cost
   constraint, substitutes its necessary transition bound, and uses three
   explicitly verified derivative signs. This gives the attained opposite
   orientation value `2*(sqrt(19)-2)`, strictly above the actual baseline.

## Load-bearing proof checks

- Every two-label controller is represented by six independent
  probabilities `(r,s,alpha,gamma,xi,delta)`. The initial label is fixed.
- Routing all a failures to the better model-1 label is used only as a
  lower-bound improvement. It changes nothing in model 0 at epsilon=0.
  It is not asserted as a normal form at positive epsilon.
- The baseline positive-polynomial identity gives a global lower bound
  in the orientation containing the optimum. Its strict positive terms
  identify the effective optimal program, not only its value.
- The opposite orientation is ruled out by a separately proved attained
  lower bound, rather than by numerical search.
- The inaccessible second label is handled by its reachable one-label
  cost, not by an invalid inverse of a singular full transition matrix.
- Near-optimizer coercivity gives `s+delta=O(Delta)`,
  `gamma=O(Delta*(s+delta))`, and `r-r0=O(Delta)`.
- Perturbed model-0 costs dominate the baseline costs term by term in
  their nonnegative finite-prefix series.
- Compactness and lower semicontinuity place every small-perturbation
  optimizer near the classified baseline optimizer. The proof does not
  presume convergence of all controller parameters without this argument.
- The exact activated-trap identity gives the lower contribution
  `epsilon/(s+delta)`; coercivity excludes a smaller escape scale.
- In the limiting model-1 cost, mixing command a into the second row is
  strictly more expensive than an equal first-order b-failure escape.
- The final lower bound minimizes over all scaled row shifts and escape
  allocations. The matching controller realizes its unique scale balance.

## Source and execution binding

Mathematical source:

- Repository-relative destination: `sections/57-sharp-stability.tex`.
- SHA-256 after the explicit endpoint clarification:
  `d7566b473142d8e87797a5929f17186b48d790754583d233799be1a8080d43ce`.

Independent diagnostic source:

- `diagnostics_r80_sharp.py`.
- SHA-256:
  `4f1bbafeda22ab5935bea50349e67f5b614b96959ac8e89cdb8e02a3a64b3878`.

Executed locally with the installed R79 dependency environment:

```
PYTHONPATH=/tmp/theta-r79-deps python -B diagnostics_r80_sharp.py
PYTHONPATH=/tmp/theta-r79-deps python -O -B diagnostics_r80_sharp.py
```

Both executions completed and emitted byte-identical JSON, including the
mathematical source hash. They recorded 5,372 exact checks and ten
high-precision finite checks. The exact checks include eleven symbolic
identities, an independently evaluated rational controller grid of 2,025
controllers, 27 rational repaired programs, exact quadratic-field
constant identities and a common fixed fallback.

The ten 70-digit comparisons evaluate only the explicit constructive
upper family at five positive perturbations. They do not compute the
globally optimized value at those perturbations and do not prove the
asymptotic. The manuscript's quantified argument proves the theorem.
Native LaTeX integration, publication identity and any hosted CI remain
the responsibility of the root revision workflow and are not claimed by
this local challenge record.
