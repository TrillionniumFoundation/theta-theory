# Referee Report — General Theta Foundations I, Revision 32

**Manuscript:** *General Theta Foundations I: Causal Width Beyond Cutwise Positive Rank*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v32-referee-ready-2026-09-25`  
**Reviewed head:** `d38fca741135d147dfdbdbd99cfd9a1a716a88a5`  
**Native mathematical source recorded by the manuscript:** `4ccfe985f0507154969b4405e94b99a2c8a451f3`  
**Controlling previous report:** `0e69fdcfc11067a7de9a6122fc603f6a5e2253d8`  
**Previous reviewed manuscript:** `90dc2c8f0c75e2cfbb95cc61b247ce4d5e216eb9`  
**Review branch:** `review/general-theta-foundations-i-v32-causal-width-pipeline-harsh-top4-r17-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 32 is a real mathematical advance over Revision 31. It replaces the earlier constant-size two-cut incompatibility example by a fixed-alphabet, uniformly full-support family in which every cut separately has positive minimum three while the minimum compatible clocked width is unbounded. It also gives a lower-bound mechanism that is valid for nonminimal hidden realizations, an exact finite upper construction, and an exact profile-set direct-sum theorem.

I did not find a short fatal counterexample to the principal displayed theorems. In the finite, wordwise, clocked, atomic stochastic-row model actually defined, the reachable-section lift, the volume budget, the rotation obstruction, the explicit polygon machine, and the retained-tag decomposition appear internally coherent. The negative recommendation is therefore **not** based on an allegation that the main theorem is false.

The four-journal case nevertheless fails for decisive reasons of originality, depth, quantitative strength, and relation to the advertised program.

1. The paper omits the most direct classical positive-realization precedent to its headline theme. Benvenuti and Farina constructed a family of transfer functions of fixed McMillan degree three whose minimum positive-realization dimension is arbitrarily large. Their stationary quantifiers differ from the present clocked finite-horizon quantifiers, so this does not subsume the new theorem; but it means that “rank three versus unbounded positive state dimension” is a classical phenomenon, not a new conceptual landscape. The manuscript cites a tutorial rotation example but not this fixed-degree large-dimension result or the associated minimality literature.
2. The key object `Q_t = aff{reachable distributions} ∩ Delta_(K_t)` projected to `P_t` is an extended formulation—a section of a simplex followed by a linear projection. The bound `|ext P_t| <= 2^(K_t)` is the standard face-count mechanism behind extension complexity. The paper does not cite Yannakakis or the extensive polygon extension-complexity literature. This omission is mathematically consequential, because regular polygons with many vertices have logarithmic-size extensions. The manuscript's direct `O(sqrt N)` vertex-state construction is therefore not remotely a convincing upper bound on the best lifted hidden-state width.
3. The quantitative theorem leaves an enormous unresolved gap: a logarithmic lower bound against a square-root upper bound. With the displayed constants, the lower bound exceeds the trivial value three only after `N > 6,291,456,000,000`. The rational rotation has no explicit growth rate at all. The proof establishes divergence, but it does not determine the scale of the phenomenon.
4. The resource model remains highly permissive: the epoch is free, rows may depend on the cut, stochastic rows are sampled atomically, transition tables and arithmetic are uncharged, the machine is horizon-specific, and only one terminal query is asked. This is a legitimate positive-realization model, but not ordinary streaming complexity and not an autonomous finite-state theorem.
5. The tagged profile theorem is neat, but its lower mechanism is exact output-support separation. It uses structural wrong-tag zeros and growing input/output alphabets, and its scalar ancestor is classical nonnegative direct-sum additivity. It is not a substitute for a general theory of untagged profile composition.
6. The repository-wide Foundations pipeline is still untouched at every difficult analytic gate. The manuscript's own status file leaves A2, B4, C2, the eleven-paper aggregate, and fully adaptive collision scheduling open. The new theorem is a local positive-realization result, not a bridge in the main A/B/C/D dependency DAG.

The correct editorial conclusion is that Revision 32 may be a serious specialist-paper candidate after a substantial literature repair and a complete removal of the “Foundations” framing. It is not close to the level of the four leading general mathematics journals.

---

## 1. Scope of this review

I reviewed the focused Revision 32 article and the records needed to place it in the repository pipeline. In particular, I examined:

- `papers/GTF-I-v32-causal-width/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `reachable-volume.tex`;
- `rotation-width.tex`;
- `quantitative-rotation.tex`;
- `profile-composition.tex`;
- `literature-and-scope.tex`;
- `primitive-proof.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the finite exact-check records;
- the publication and native-source commits;
- the complete sixteenth referee report;
- the Revision 31 source arguments retained or reused here;
- the repository-level Round-Seventeen proof-dependency ledger.

I also made a targeted external comparison with classical positive-realization minimality and polyhedral lift/extension-complexity results. This was not an exhaustive priority certification. It was sufficient to identify two direct literatures that the current audit does not cover and that materially alter the novelty assessment.

The publication genealogy is clean: the Revision 32 work descends from the controlling r16 report, the previous manuscript is retained, and the focused package is additive rather than destructive. That is good repository practice. It is not evidence of theorem correctness, priority, or editorial significance.

The 15-page article is self-contained enough to audit its new claims. The 406-page mathematical archive and 959-page development archive are therefore optional provenance records, not proof supplements that add weight to the journal case. I did not treat scripts, hashes, negative controls, page comparisons, or successful compilation as mathematical certification.

---

## 2. What Revision 32 genuinely accomplishes

### 2.1 It answers the strongest mathematical demand in r16

The preceding report asked for an unbounded incompatibility gap, an arbitrary-horizon obstruction, or a natural composition theory. Revision 32 supplies all three in some form.

The rotation family has fixed seed, command, query, and output alphabets. Every response probability remains uniformly separated from zero and one, independently of the horizon. Every cut separately has positive minimum three, yet the compatible width tends to infinity. This is a substantial improvement over repeating or summing the Revision 31 constant-size example.

### 2.2 The lower bound does not cheat by assigning observable vectors to arbitrary hidden states

The most technically important correction is the use of reachable state distributions. Given a `K_t`-label realization, the manuscript forms

```text
H_t = aff{E_h},
Q_t = H_t intersect Delta_(K_t),
P_t = pi_t(Q_t).
```

The intertwining relation is extended only across `H_t`, where it is justified by affine equality on actual reachable distributions. It is not asserted on arbitrary basis vectors of the hidden simplex. This is the right way to accommodate unobservable directions and nonminimal hidden realizations.

The conservative vertex bound `|ext P_t| <= 2^(K_t)` is also logically valid. A section of a simplex can have more vertices than the ambient simplex has vertices, so the tempting replacement by `K_t` would be false.

### 2.3 The paper gives an actual cumulative obstruction

The quantity

```text
delta_M = min_P [vol(conv union_L L P) - vol(P)]
```

over observable polytopes between a seed body and a bounded domain is independent of a proposed hidden transition table. Under the determinant-one and no-invariant-polytope hypotheses, compactness gives `delta_M > 0`, and every machine pays these increments along the horizon.

This is more than a restatement of compatible factorization. It is a usable necessary inequality for arbitrary time-dependent hidden realizations.

### 2.4 The upper construction is exact and explicit in the declared model

The nested regular polygons give a concrete horizon-dependent machine. The inradius/circumradius bookkeeping is explicit, the transition row is written down, and only a polygon vertex label survives. The rational counter construction supplies a separate fully rational finite realization for the rational rotation.

The paper is careful not to call the computable-real polygon rows a finite-denominator fair-bit implementation. That distinction is appropriate.

### 2.5 The tagged profile identity is an exact set-valued statement

The retained tag makes branch-reachable state sets disjoint at every cut. Restriction gives genuine component machines, while disjoint union gives the converse. Thus the entire feasible profile set, not merely one rank, adds by Minkowski sum.

Applied to the Revision 31 primitive, this correctly yields the complete region

```text
K_1 >= 3m,
K_2 >= 3m,
K_1 + K_2 >= 7m.
```

### 2.6 The focused package and model definition are better

Revision 32 centralizes the clocked transducer definition, specifies available-label counting, distinguishes clocked and autonomous models, and provides a compact referee package that excludes the cumulative archives. These are meaningful editorial improvements.

These advances make the paper worth taking seriously. They do not settle the top-four question in its favor.

---

## 3. Technical audit of the main arguments

### 3.1 The machine model is now sufficiently explicit

The product formula specifies initialization, command-dependent stochastic rows, and a terminal query decoder. Equality is required wordwise on the complete Cartesian input set. The current symbol is consumed atomically, and earlier data cannot be reread unless retained in the register.

The model also makes its free resources explicit: the time index, row tables, arithmetic, and atomic sampling are not counted. This clarity removes an ambiguity, though it also narrows the significance of the theorem.

The definition of separate minimum is coherent. A factorization at one selected cut can be embedded into a complete finite machine by storing the full prefix before the cut and sufficient suffix information after it, at potentially enormous costs at all other cuts.

### 3.2 The separate minimum in the rotation family is indeed three

At every cut, the residual family is affine in a two-dimensional predictive vector. The four idle-command seed rows span that affine plane, and the two terminal coordinate queries distinguish both directions, so normalized row rank is three.

The fixed triangle with vertices

```text
(1/2,0), (-1/2,1/2), (-1/2,-1/2)
```

contains the disk carrying all reachable predictive vectors. Each triangle vertex produces a legal continuation under all future rotations because its Euclidean norm is below one. Barycentric decomposition therefore gives a normalized three-generator continuation factorization. Together with the rank lower bound, this proves the separate minimum.

I see no hidden residual-state restriction in this step.

### 3.3 The reachable-section lift is valid

For an actual prefix distribution `E_h`, the observable map `pi_t` obtained by idling the remaining commands returns the current predictive vector. The realizing stochastic row maps actual prefix distributions at cut `t` to actual prefix distributions at cut `t+1`. Hence it maps their affine span into the next affine span.

The equality

```text
pi_(t+1)(E_h T_(t,L)) = L pi_t(E_h)
```

holds for every actual prefix and extends affinely over `H_t`. Intersecting with the hidden simplex restores nonnegativity. This gives

```text
P_t subset P_(t+1),
L P_t subset P_(t+1).
```

The active-zero-set proof of `|ext Q_t| <= 2^(K_t)` is correct: two distinct vertices with the same zero coordinates would leave a two-sided feasible direction inside the affine section. A linear image cannot have more vertices than are needed in the image of the source vertices.

This lemma is the strongest new local argument in the paper.

### 3.4 The abstract volume budget is sound

The feasible family of at-most-`M`-vertex polytopes can be parametrized by `M` points in the compact observation domain, with repetitions allowed. Containment of the seed body is closed, and volume is continuous under Hausdorff convergence for compact convex bodies. Thus the minimum is attained.

If the volume increment vanishes, the old polytope equals the convex hull of all its images. Each determinant-one image is contained in it and has the same volume, forcing equality. This contradicts the assumed absence of a common invariant polytope.

The telescoping inequality then follows from the nested inclusions. I do not see a missing compactness or full-dimensionality hypothesis in the stated setting.

### 3.5 The qualitative rotation obstruction is correct

An invariant full-dimensional polygon containing the seed square has a nonzero vertex. An infinite-order rotation preserving the polygon permutes its finite vertex set, which would give that vertex a finite nonzero orbit. This is impossible.

The rational matrix

```text
(1/5) [[3,-4],[4,3]]
```

is an infinite-order rotation. The manuscript's algebraic-integer argument is valid. Hence the qualitative divergence and the real-algebraic finite exclusion procedure follow from the abstract volume theorem.

### 3.6 The displayed quantitative estimate appears internally consistent

The Fibonacci approximation gives a finite orbit net of length between `32M` and `64M`. Iterating the one-step Hausdorff error along this orbit forces a polygon with at most `M` vertices to differ from its rotation by at least order `M^(-3)`.

The triangular cap argument converts Hausdorff displacement into an area increase of order the square of that displacement. With `a=1/10`, the constants yield

```text
delta_M >= 1/(6000000 M^6)
```

and hence

```text
sum_(t<N) 2^(-6 K_t) <= 24000000.
```

The estimates are crude, but I do not find an evident sign reversal or missing containment in the proof.

### 3.7 The polygon upper construction checks out

For `M=4 ceil(sqrt(N+1))`, the chosen radius sequence makes the inradius of `P_(t+1)` equal the circumradius of `P_t`. Thus both the idle and rotated copies of `P_t` lie in `P_(t+1)`. The Bernoulli estimate keeps the terminal polygon inside the square.

The adjacent-vertex coefficients plus uniform residual mass are nonnegative and normalized, and their mean is the required rotated vertex. Induction recovers the exact conditional predictive vector.

This proves the claimed `O(sqrt N)` label upper bound in the atomic-row model. It does not show that this growth is near optimal.

### 3.8 The profile direct-sum proof is correct under its explicit tag hypothesis

If a hidden state were reachable with positive probability in two branches, exact terminal recovery would force the same future continuation to output two distinct tags with probability one. Nonnegativity makes this impossible. Transition closure of branch-reachable state sets then gives restricted component machines.

The common full suffix alphabet and retained terminal tag are essential. The theorem should not be generalized rhetorically to untagged mixtures or branch-dependent interfaces.

### 3.9 The verification suite is appropriately secondary

The scripts check rational examples, symbolic row identities, selected constants, and deliberately invalid controls. They do not compute the geometric minima `delta_M`, prove the uniform optimization statements, or establish novelty. The manuscript generally says this correctly.

---

## 4. The most direct positive-realization precedent is missing

The literature audit treats stationary irrational-rotation nonrealizability as the closest classical ancestor. That is not enough.

L. Benvenuti and L. Farina, *An example of how positivity may force realizations of “large” dimension*, Systems & Control Letters 36 (1999), 261–266, construct a family of transfer functions, each of McMillan degree three, such that for every integer `N >= 3` a member has minimum positive-realization dimension at least `N`.

This is directly relevant to the paper's central slogan:

```text
fixed linear/cutwise rank three
versus
unbounded positive state dimension.
```

The models are not identical. Benvenuti–Farina study stationary linear positive realizations of transfer functions. Revision 32 studies exact finite-horizon wordwise transducers, permits unrelated transition rows at different epochs, and compares the minima at each cut with the peak of one compatible realization. Their theorem therefore does not imply the current volume budget or its profile statement.

But the distinction must be explained theorem by theorem. Without that comparison, the paper invites readers to treat the unbounded rank-versus-positive-dimension phenomenon itself as new. It is not.

The omission is especially serious because the same authors' later surveys explicitly frame minimal positive dimension as potentially much larger than McMillan degree and relate minimality to positive factorizations of Hankel matrices. A paper submitted under MSC 93B15 cannot regard this as peripheral background.

At minimum, the article must answer:

1. Can the Benvenuti–Farina family be encoded as finite terminal arrays whose cutwise positive minima remain bounded?
2. What part of Revision 32 fails if one truncates a classical large-positive-order impulse response?
3. Is the essential novelty the nonstationary clocked quantifier, the wordwise command interface, the cumulative profile inequality, or all three?
4. Does the volume budget produce any new lower bound for a classical stationary positive realization beyond known cone/Hankel arguments?
5. Which old lower-bound techniques for minimum positive order can be adapted to sharpen the present `log N` bound?

Until these questions are addressed, the priority boundary of the headline theorem is incomplete.

---

## 5. The paper is written in the language of extension complexity without citing it

The hidden-state lift has a standard polyhedral interpretation.

`Q_t` is a polytope cut out inside the `K_t`-label simplex by an affine subspace. It is described by at most `K_t` coordinate inequalities. The observable polytope `P_t` is its linear image. Thus `Q_t -> P_t` is an extended formulation, specifically a simplex-section lift.

The estimate

```text
|ext P_t| <= 2^(K_t)
```

is the elementary face-count consequence that a polytope described by `K_t` facets has at most `2^(K_t)` faces. This is not a novel combinatorial principle. It belongs to the theory initiated by Yannakakis, where extension size is related to nonnegative rank of slack matrices.

The omission matters twice.

### 5.1 It changes the conceptual interpretation of the lower bound

The theorem is naturally a lower bound on a **dynamic sequence of compatible lifts**, not merely a state-count argument. The machine supplies, at each time, a small simplex-section extension plus stochastic maps between successive extensions. The current paper discards most of that lift structure and retains only the worst-case vertex bound.

That loss is exactly why the final quantitative lower bound is logarithmic.

### 5.2 It exposes the weakness of the upper construction

Fiorini, Rothvoß and Tiwary proved that regular `m`-gons have extension complexity `O(log m)`, with the result tracing to Ben-Tal and Nemirovski. Later work sharpened the constants. Revision 32 instead represents its regular polygons by their `m` vertices and therefore spends `m = O(sqrt N)` labels.

A small static extension of each polygon does not automatically give compatible stochastic maps between epochs, so this literature does **not** by itself improve the machine upper bound. That missing compatibility is precisely an interesting problem. But the manuscript must formulate it, rather than presenting a direct-vertex construction as if it were the natural scale of hidden width.

The correct next object is something like a dynamic or equivariant extension complexity:

- a sequence of extensions of `P_t`;
- stochastic maps between the extensions lifting the idle and rotation maps;
- a common bound on the number of simplex coordinates;
- a terminal observable projection.

The paper currently has the ingredients for this definition but does not make it. Without the extension-complexity comparison, its strongest lemma is not placed in its natural mathematical setting.

Required references include at least:

- M. Yannakakis, *Expressing combinatorial optimization problems by linear programs*, J. Comput. System Sci. 43 (1991), 441–466;
- S. Fiorini, T. Rothvoß and H. R. Tiwary, *Extended formulations for polygons*, Discrete Comput. Geom. 48 (2012), 658–668;
- appropriate subsequent work on the linear extension complexity of regular polygons and on nonnegative factorizations of slack matrices.

This is not a cosmetic bibliography request. It may materially change both the lower-bound strategy and the plausible true order of `W_N`.

---

## 6. The quantitative theorem is far from a classification

The headline bounds are

```text
(1/6) log_2(N/24000000) <= W_N <= 4 ceil(sqrt(N+1)),
```

apart from the trivial lower bound three and the linear counter construction.

This gap is enormous. The lower bound becomes larger than three only when

```text
N > 24000000 * 2^18 = 6,291,456,000,000.
```

At that horizon, the displayed polygon upper bound is still on the order of ten million states. The theorem therefore establishes qualitative divergence but gives almost no information about the actual compatible width at any moderate horizon.

The proof method itself seems locked to a logarithmic conclusion:

1. a `K`-label simplex section is replaced by a polygon with at most `2^K` vertices;
2. the polygon's invariance defect is polynomial in the inverse vertex count;
3. the time budget then yields `K >= c log N`.

To exceed logarithmic growth, one must exploit more than the number of projected vertices. Extension-complexity, symmetry, stochastic-map compatibility, or algebraic constraints on the lift would have to enter.

Conversely, the regular-polygon upper bound ignores lifting entirely and is unlikely to be the last word. The true growth could plausibly be logarithmic, polylogarithmic, or something intermediate. Revision 32 does not distinguish these possibilities.

The rational rotation is weaker still: it proves unboundedness through existence and real quantifier elimination but gives no explicit lower function of `N`. Calling the thresholds “effective” is logically correct, but not a quantitative theorem in the usual analytic sense.

For a four-journal contribution, one would expect at least one of:

- a matching order of growth;
- a polynomial lower bound;
- a lift-aware logarithmic upper bound matching the present lower bound;
- an explicit quantitative rational-angle lower bound;
- an exact width formula for a natural subsequence;
- a robust structural invariant controlling arbitrary compatible lifts;
- a reduction from or solution of a recognized open problem in positive realization or extension complexity.

None is present.

---

## 7. The resource model sharply limits the significance

The theorem counts persistent labels in a horizon-specific clocked stochastic transducer. The following are free:

- the current epoch;
- a different state set at every cut;
- different stochastic rows at every cut;
- an arbitrarily large read-only transition table;
- exact arithmetic on algebraic or computable-real constants;
- atomic sampling from an exact stochastic row;
- construction time for the machine;
- one terminal query supplied only after all commands.

The polygon decoder depends on the horizon. Thus the upper construction is not one fixed finite device that works for all lengths. The rational counter construction stores the count of rotation commands but still relies on the free external epoch for its phase-dependent state availability.

These conventions are defensible in positive realization. They make the lower result stronger in one sense—the width diverges even when the clock and time-dependent rows are free. They also make the algorithmic interpretation much weaker.

The word “memory” should therefore be qualified throughout as **clocked positive-realization width**. The paper does not provide:

- an autonomous state-complexity theorem;
- a succinct streaming algorithm;
- a bit-space bound including tables and arithmetic;
- a finite fair-bit implementation for the golden-angle rows;
- a uniform approximation theorem with one fixed finite device;
- an adaptive experimental-policy result.

This distinction is central to editorial placement.

---

## 8. The tagged profile theorem is useful but not deep enough to carry the paper

The set-valued Minkowski identity is clean. It correctly preserves cross-cut tradeoffs that scalar rank additivity would erase.

Its mechanism, however, is exact support separation. The terminal output includes the branch tag, wrong tags have probability zero, and every branch shares the same full future interface. Positivity then forces branch-reachable state supports to be disjoint.

This is the sequential analogue of a familiar direct-sum argument. The theorem does not address:

- untagged mixtures;
- approximately recoverable tags;
- overlapping output supports;
- branch-dependent suffix alphabets;
- noisy tags;
- subadditivity or superadditivity without an explicit disjointness witness;
- profile composition under products, tensoring, or shared submachines.

The exact growing frontier is obtained by summing a previously known primitive. Its initial and final alphabets grow with `m`, and it contains structural zeros. The manuscript correctly separates it from the fixed-alphabet full-support rotation theorem. It should also reduce the novelty rhetoric accordingly.

---

## 9. The real-algebraic effectiveness statement is generic

For fixed `M`, the minimum area expansion over algebraic polygons can be encoded as a first-order formula over a real closed field. Quantifier elimination and root isolation then compute the algebraic minimum and a positive rational lower bound.

This is correct. It is also a generic consequence of semialgebraic optimization. The manuscript gives:

- no useful complexity estimate;
- no executable bound as a function of `M`;
- no numerical value of `delta_M` for the rational rotation;
- no asymptotic lower estimate;
- no evidence that the procedure is feasible beyond tiny `M`.

Accordingly, this corollary should be presented as a formal decidability observation, not a major constructive theorem.

The same applies to fixed-profile robustness: compactness gives positive distance from a target outside a compact realization image, and semialgebraic optimization makes the rational case effective. This is useful bookkeeping, not top-four mathematics.

---

## 10. Pipeline assessment

The repository's Round-Seventeen ledger contains two principal analytic chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Their unresolved gates include branchwise Fourier and local-limit theory, stopped large deviations, a common global kernel, nonlinear semigroup and resolvent arguments, graph-core convergence, filtering regularity, optional projection, and typed contraction.

Revision 32 proves none of these. Its own `PIPELINE_STATUS.json` correctly records as false:

- `historical_A2_replaced`;
- `B4_aggregate_closed`;
- `C2_aggregate_closed`;
- `eleven_paper_aggregate_closed`;
- `fully_adaptive_collision_solved`.

The new proof edges are internal to the positive-realization article:

```text
reachable affine sections -> projected polytopes -> volume budget
Fibonacci orbit covering -> quantitative area expansion
nested polygons -> exact finite upper bound
retained tag -> profile Minkowski sum
```

This is a coherent local DAG. It is not a dependency edge into the repository's hard analytic program.

The preservation of earlier arguments is valuable for provenance. It does not make this paper foundational for A2, B4, C2, or D1. The title “General Theta Foundations I” remains unsupported by the mathematical role of the article.

---

## 11. Editorial assessment and branding

The focused paper has a visible theorem spine:

1. a complete clocked transducer model;
2. reachable simplex sections and observable lifts;
3. a cumulative volume budget;
4. a rotation family with fixed separate minimum;
5. an explicit finite upper construction;
6. a tagged profile composition theorem.

This is the strongest and cleanest organization in the sequence so far.

The title still damages the paper. “General Theta Foundations I” does not identify a recognized mathematical object, theorem, or program outside the repository. It suggests a foundational role in a much larger theory that the paper neither explains nor supports.

A suitable specialist title would be something like:

- *Causal Width versus Cutwise Positive Rank*;
- *Compatible Positive Realizations of Finite Stochastic Transducers*;
- *Dynamic Polyhedral Lifts and Causal Positive Width*.

The 406-page and 959-page archives should not accompany a normal journal submission. The small referee package is the correct model. Repository provenance can be cited separately.

The author should also stop framing successive revisions as movement toward a top-four decision. Revision 32 deserves a fresh specialist evaluation only after its literature boundary has been repaired.

---

## 12. Required changes before a credible specialist submission

These changes are not a path to acceptance in a top-four general journal. They are the minimum for a fair specialist review.

### 12.1 Repair the positive-realization literature boundary

Add the Benvenuti–Farina 1999 large-dimension example and the subsequent minimal-positive-realization surveys and lower-bound literature. Explain precisely why the finite clocked theorem is not a corollary of those stationary results.

The comparison must address fixed degree/rank, positive Hankel factorization, stationary versus time-varying rows, finite truncations, and horizon-dependent machines.

### 12.2 Recast the lift theorem in extension-complexity language

Cite Yannakakis and the polygon extension-complexity literature. Define the special simplex-section extension supplied by a hidden state register. Explain which static lifts can or cannot be equipped with compatible stochastic inter-epoch maps.

A genuinely strong revision would formulate and study dynamic/equivariant extension complexity rather than discarding the lift structure after counting projected vertices.

### 12.3 Sharpen the growth theorem

Close a substantial part of the `log N` versus `sqrt N` gap. A matching logarithmic construction, a polynomial lower bound, or an exact result for a natural subsequence would materially change the paper.

At minimum, derive an explicit rate for the rational rotation rather than relying only on quantifier elimination.

### 12.4 Separate qualitative and quantitative claims

The present explicit constant gives a nontrivial lower bound only at astronomically large horizons. State this fact. Do not market the displayed inequality as a practically informative finite bound.

### 12.5 Investigate autonomous and succinct variants

Determine what survives when the external clock, horizon-dependent decoder, and uncharged table are removed. Even a nontrivial lower or upper comparison between clocked width and autonomous total-state count would broaden the significance.

### 12.6 Generalize profile composition beyond exact tags

Approximate tags, overlapping supports, or shared submachines would produce a more substantive composition theory. The current exact-zero direct sum should be presented as the base case.

### 12.7 Retitle and remove pipeline branding

Submit the focused article as a self-contained paper in positive systems, stochastic automata, or polyhedral lifts. Remove “General Theta Foundations I,” internal A/B/C/D labels, and cumulative archive claims from the editorial presentation.

### 12.8 Obtain an independent priority review

The current literature audit is improved but still misses two central bodies of work. An expert in positive realization and an expert in extension complexity should review the novelty claims before resubmission.

---

## 13. Specific major and minor points

1. **Cite the 1999 Benvenuti–Farina large-dimension construction.** It is indispensable for the headline comparison.
2. **Cite Yannakakis and polygon extension complexity.** The lift lemma is naturally an extended-formulation statement.
3. **Do not call the `2^K` vertex estimate a specifically hidden-state phenomenon.** It is a standard face-count bound for a `K`-inequality extension.
4. **Explain whether every relevant small extension can be normalized as a simplex section.** If not, state the restriction precisely.
5. **Define a dynamic lift parameter.** The current state count combines extension size and compatibility but never names that object.
6. **State the astronomical onset of the nontrivial explicit lower bound.** The constants should not be hidden behind asymptotic notation.
7. **Clarify that the rational-angle effectiveness result gives no explicit asymptotic rate.** “Computable” is not “quantitatively controlled.”
8. **Avoid calling the polygon upper bound structurally sharp.** Regular polygons admit much smaller static lifts.
9. **Distinguish available labels from reachable labels at every theorem.** The profile set is upward closed by available-label padding.
10. **Keep the terminal query convention prominent.** There is one query after acquisition, not repeated online access.
11. **Do not use “streaming” without “clocked atomic-row positive realization.”** The standard computational interpretation is different.
12. **State that the golden-angle upper machine uses computable-real row data.** It is not a finite rational transducer implementation.
13. **Keep the horizon dependence of the decoder explicit.** The construction is not one machine for all `N`.
14. **Clarify the state availability in the `3(t+1)` rational construction.** A conventional autonomous machine would need phase/count handling in one state set.
15. **Do not treat generic real quantifier elimination as an algorithmic contribution.** No complexity or usable bound is supplied.
16. **Separate the qualitative unboundedness theorem from the crude quantitative constants.** Their evidentiary strength is different.
17. **Keep the full-support claim restricted to the rotation family.** The tagged sum has wrong-tag zeros.
18. **Do not generalize tagged additivity to unlabelled mixtures.** The proof fundamentally uses exact terminal support separation.
19. **Add a comparison with finite Hankel truncations.** The paper should explain how its cutwise positive minima relate to classical positive Hankel factorizations.
20. **Discuss whether the volume method extends beyond determinant-one maps.** If contraction or expansion is allowed, the current telescoping argument changes.
21. **Discuss higher dimension.** The current quantitative argument is planar and uses area plus circular orbit covering.
22. **State whether the seed square can be replaced by a general full-dimensional body without changing separate positive minimum.** The abstract volume theorem is broader than the concrete rank-three construction.
23. **Do not imply that the fixed rank-three boundary is universal.** It is the chosen family and normalization, not a classification of all low-rank transducers.
24. **Reduce the role of the inherited two-cut appendix.** It is useful for the tagged corollary but not part of the new main theorem.
25. **Keep scripts out of the proof narrative.** Their current role is mostly appropriate; preserve that discipline.
26. **Remove cumulative archive page counts from the contribution summary.** They are not evidence of mathematical scope.
27. **Shorten the repository-pipeline discussion in the article.** The focused theorem does not require internal project labels.
28. **Use a neutral contribution table.** Separate new, inherited, classical, and formal-decidability statements.
29. **Do not claim exhaustive priority clearance.** The current audit correctly avoids this, but the omission of central literature demonstrates why.
30. **Seek a specialist venue.** Positive systems, stochastic automata, control, or polyhedral combinatorics are the natural editorial homes.

---

## 14. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Main arguments appear coherent; no short fatal counterexample found |
| Advance over Revision 31 | Substantial: fixed alphabets, full support, unbounded gap, arbitrary horizon |
| Originality boundary | Not established; direct positive-realization and extension-complexity precedents are omitted |
| Mathematical depth | Serious specialist level, below top-four general-journal level |
| Quantitative strength | Very weak: logarithmic lower versus square-root upper; rational case qualitative |
| Generality | Planar rotation family, one terminal query, clocked horizon-specific machines |
| Algorithmic content | Minimal; atomic rows and tables are free, real QE is formal rather than efficient |
| Profile composition | Exact but driven by retained tags and structural zeros |
| Pipeline impact | None on the decisive A2/B4/C2/D1 analytic gates |
| Presentation | Focused and substantially improved; branding remains misleading |
| Reproducibility engineering | Strong, but irrelevant to proof, originality, and journal level |
| Editorial recommendation | Reject at top-four level; consider only after specialist repositioning |

---

## 15. Final assessment

Revision 32 is the first version in this sequence that turns the compatibility issue into an arbitrary-horizon theorem with an unbounded gap. The authors deserve credit for directly answering the previous report rather than merely renaming the Revision 31 example. The all-hidden-state lift is carefully formulated, the volume budget is a genuine lower-bound device, and the finite constructions are explicit.

That is the positive assessment.

The negative assessment is equally clear. The paper does not yet know its closest classical relatives. Fixed degree three with arbitrarily large positive-realization dimension was already exhibited in 1999. The hidden section-and-projection argument belongs to extension-complexity theory, where regular polygons have logarithmic-size lifts. Once those facts are taken seriously, the central open question becomes the complexity of **compatible dynamic lifts**, and Revision 32 has only begun to formulate that problem.

Its quantitative result is far from sharp, its computational model is permissive, its tagged composition theorem is support-driven, and its repository pipeline remains open at all major analytic gates. The “Foundations” title and thousand-page archival history cannot convert a promising specialist theorem into a top-four contribution.

My recommendation is therefore firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A retitled, literature-complete paper centered on dynamic polyhedral lifts and clocked positive-realization width could merit serious review in a specialist venue. That would be a new editorial submission, not another round under the claim that this manuscript is approaching the four-journal threshold.
