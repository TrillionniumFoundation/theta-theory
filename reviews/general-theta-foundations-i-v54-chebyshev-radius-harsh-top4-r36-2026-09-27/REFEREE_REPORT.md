# Referee Report — General Theta Foundations I, Revision 54

**Manuscript:** *Sharp Noise Thresholds and Width Laws for Stochastic Realizations of Compact Group Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v54-chebyshev-radius-2026-09-27`
- `revision/general-theta-foundations-i-v54-referee-ready-2026-09-27`

**Reviewed publication head:** `1eb16a3f857d17a91dc1c82906ef16a5965a47d2`  
**Validated native-source commit:** `8b0e5fb6068962c22605d8222fee6cf96dfd2fad`  
**Source predecessor:** Revision 53 publication `825d1d302cfca6c6b5abe8497bddb4df8680d810`  
**Controlling prior report:** r35, `ea6d8b71653ec4aa6084b4faf63fe7d702505a26`  
**Qualification workflow:** `36308068660`  
**Review branch:** `review/general-theta-foundations-i-v54-chebyshev-radius-harsh-top4-r36-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 54 is the strongest, broadest, and most coherent manuscript in the recent General Theta Foundations I sequence. It is a substantial advance over Revision 53 rather than a repackaging of the scalar theorem. I did not find a fatal counterexample to the constrained-radius classification, the vector-valued localization argument, the arbitrary-width occupation theorem under cofinite executable returns, the categorical examples, the full-subcritical Diophantine width law, the exact polygon construction, the comparable-denominator lemma, or the effective rational specialization.

The two principal mathematical conclusions are genuinely nontrivial.

First, for a finite continuous interface from a compact group with finitely many connected components into compact convex finite-dimensional output sets, bounded nonuniform clocked stochastic width is possible exactly at and above the largest constrained Chebyshev radius of a component image. Equality is attained by one stationary finite component-permutation machine. Below the radius, the number of cuts having any fixed width is bounded independently of the horizon, even if all intervening registers are unrestricted.

Second, for a specified planar alphabet of `s` rotations whose angle vector is dual badly approximable, with signal amplitude `0<rho<1`, the paper proves

```text
W_{N,epsilon} = Theta(N^{s/(2s+1)})
```

for every fixed `0<=epsilon<rho/2`. The lower bound now covers the whole subcritical interval, and an exact common-row polygon realization gives the matching upper bound.

These results are considerably more substantial than the finite candidate certificates, rank-tight boundary theorems, and small-noise implications appearing in earlier revisions.

The top-four rejection is therefore **not** a correctness dismissal. It is based on the remaining gap between a strong focused specialist theorem and a leading general-mathematics-journal theorem.

1. The sharp radius classification remains a theorem for compact **group** dynamics with finitely many connected components and a strong synchronization hypothesis: exact identity-product words exist at every sufficiently large length. General compact semigroups, irreversible controlled systems, alphabets with more complicated return languages, and compact groups with infinitely many components are outside the theorem.
2. The resource model remains exceptionally permissive. Horizon, epoch, horizon-dependent arbitrary real row tables, their construction and lookup, exact arithmetic, and exact atomic sampling are free. The result is mathematically stronger for surviving this advice model, but its relationship to standard automaton size, workspace, random-bit complexity, and implementable positive systems remains indirect.
3. The matching quantitative theory is restricted to a planar rotation family with a dual badly approximable angle vector, strict amplitude slack `rho<1`, and an exact upper alphabet. There is no matched growth law for a general compact connected group, for broad noncommuting representations, at `rho=1`, or for generic algebraic rotations.
4. The effective theorem proves termination through group-closure algorithms and real quantifier elimination, not a usable complexity classification. No meaningful upper complexity bound is supplied for the complete stochastic-realization decision process.
5. The finite quotient theorem minimizes only deterministic component-quotient machines. The unrestricted stationary stochastic minimum at the threshold, and its relationship with the nonuniform minimum, remain open.
6. Much of the proof technology—Peter–Weyl approximation, Haar projection, Chebyshev centers, simultaneous Diophantine approximation, regular-polygon enclosure, Zariski closure, and real quantifier elimination—is classical. The combination is elegant and useful, but the present applications do not yet establish the breadth normally required by the four leading general journals.
7. The priority comparison is now serious and conventional, but it remains targeted rather than exhaustive. In particular, the surrounding real-valued probabilistic-automata, quantitative weighted-automata, almost-periodic-function, compact-semigroup, approximate-realization, and controlled hidden-Markov literatures still require independent expert comparison.
8. The theorem remains logically independent of the repository’s A/B/C/D analytic dependency graph. The repository pipeline and revision count add no general-journal significance to the standalone result.

**Disposition outside the four leading general journals:** this is now a credible, focused, potentially publishable paper for a strong specialist venue in probabilistic or weighted automata, positive realization, compact-group dynamics, control, or theoretical computer science. It should undergo a conventional external priority audit and a final tightening of the theorem’s intrinsic scope. Unlike earlier revisions, I do not regard major architectural rewriting as a prerequisite for specialist submission.

---

## 1. Scope, genealogy, and materials reviewed

At the final branch survey used for this report, Revision 54 was the latest referee-ready General Theta Foundations I revision. Both reviewed revision branches pointed to

```text
1eb16a3f857d17a91dc1c82906ef16a5965a47d2.
```

No Revision 55 branch and no pre-existing Revision 54 review branch were present at that survey.

I reviewed the complete active main article and the repository records needed to assess correctness, provenance, reproducibility, literature positioning, and relation to the wider pipeline. In particular, I examined:

- `papers/GTF-I-v54-chebyshev-radius/main.tex`;
- `sections/01-classification.tex`;
- `sections/02-localization.tex`;
- `sections/03-consequences.tex`;
- `sections/04-width-laws.tex`;
- `sections/05-algebraic-circle.tex`;
- `sections/06-effective.tex`;
- `sections/07-comparison.tex`;
- `sections/08-bibliography.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `HISTORY_AND_PIPELINE_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `FROZEN_R35_REPORT.md`;
- `PRESERVATION_MANIFEST.json`;
- the new and inherited exact-check programs;
- `evidence/BUILD_RECEIPT.json` and source identity records;
- the isolated rebuild records and referee package;
- the branch-specific qualification workflow;
- the complete r35 report;
- the Revision 53 source relevant to the scalar threshold and algebraic-circle argument;
- and the frozen repository-level Round-Seventeen dependency ledger retained through the predecessor package.

The twenty-page main article is independently complete. The scalar predecessor, four-page companion notes, and sixty-eight-page cumulative supplement are separately buildable background rather than hidden forward dependencies of the principal proofs. This is a genuine editorial improvement.

The genealogy is clean. Revision 54 descends from the Revision 53 publication, pins the controlling r35 report independently, commits readable theorem source before qualification, and adds generated publication evidence without changing that native source. Earlier revision, review, and unrelated manuscript branches remain untouched.

A successful source-bound build is useful evidence of reproducible delivery. It is not independent mathematical proof, priority clearance, or editorial acceptance. Conversely, my recommendation is not based on a packaging defect.

---

## 2. Executive assessment of the new mathematics

Revision 54 materially answers almost every central strengthening request in r35.

### 2.1 The scalar oscillation is replaced by the correct constrained output radius

Let `H` be a compact Hausdorff group with finitely many connected components, `K=H^0`, and `C=H/K`. For each seed-query pair the target is now a continuous map

```text
F_{s,j}: H -> Y_j,
```

where `Y_j` is a compact convex subset of a finite-dimensional normed space. The output may be a complete categorical law, a finite joint law, or another compact-convex numerical object.

The critical error is

```text
epsilon_c = max_{s,j,c} rad_{Y_j}(F_{s,j}(c)),
```

where the center is required to lie in the legal output set `Y_j`.

Theorem `radius54` proves, including equality, that

```text
sup_N W_{N,epsilon} < infinity
        iff
one stationary finite permutation realization works at every horizon
        iff
epsilon >= epsilon_c.
```

Below the radius, every fixed width has a horizon-independent occupation bound with unrestricted intervening widths.

This is the right vector-valued extension. It is not obtained by applying the binary theorem coordinate by coordinate, because separately chosen coordinate centers need not form a legal categorical distribution.

### 2.2 The lower bound is intrinsic to compact groups

The new proof no longer depends on a faithful finite-dimensional matrix embedding of the whole compact group. Real representative functions and Peter–Weyl density produce only the finite-dimensional feature space needed by the selected interface and localization functions.

This permits connected compact groups that are not finite-dimensional Lie groups or faithfully represented in the original physical dimension. The moving representation is finite because the test family is finite, not because the ambient group is assumed linear.

### 2.3 The synchronization hypothesis is weakened correctly

An identity letter is no longer required. It is enough that every sufficiently large length admit some executable identity-product word. Finite return words with relatively prime lengths imply this condition.

The occupation proof explicitly accounts for the bounded initial, intermediate, and final return gaps. It does not assume that the stochastic rows along a physical return word are identity rows.

This is a meaningful extension. It is also only a sufficient synchronization condition, not a classification of all possible return languages.

### 2.4 Whole categorical and joint laws are handled

The three-outcome example has constrained total-variation radius `2/3`, whereas each separately requested binary event has threshold `1/2`. This demonstrates that the vector theorem contains information absent from marginal-by-marginal analysis.

The measure-once unitary corollary treats one entire selected POVM law. It does not invent a joint law for incompatible measurements.

### 2.5 The subcritical width law is now matched

For a dual badly approximable `s`-tuple of rotation angles, the paper proves the same polynomial width exponent throughout the full fixed subcritical interval:

```text
W_{N,epsilon} = Theta(N^{s/(2s+1)}),
0 <= epsilon < rho/2,
0 < rho < 1.
```

The lower argument uses high-harmonic positive localization to retain a terminal moving moment even near the critical noise. A finite arithmetic grid of executable words then contracts that moment at every narrow endpoint.

The upper argument is a genuine common-row stochastic realization. A regular polygon is enlarged just enough to absorb each rotation, stochastic rows realize the contracted rotated vertices, and the terminal decoder rescales exactly. The simultaneous denominator lemma gives a denominator of the correct order.

The exponent and polygon idea have historical predecessors in the repository line; the new result is the full-subcritical matching theorem and its complete proof.

### 2.6 A finite input class is effectively classified

For rational orthogonal generators containing the identity and rational polynomial categorical outputs, Revision 54 proves computability of:

- the real connected components and finite component group;
- the exact algebraic radius;
- an attaining component-permutation machine;
- a subcritical occupation constant for every algebraic error and fixed width;
- and the unrestricted minimum width at every fixed finite horizon.

The proof clearly imports established Zariski-closure and real-algebraic algorithms. It does not claim a new closure algorithm or practical implementation.

### 2.7 The deterministic component quotient is minimized exactly

Within the natural class whose state is a deterministic quotient of the seed-component pair, the least boundary width is characterized by equivariant partitions whose block output unions have radius at most the error tolerance.

The manuscript correctly avoids identifying this finite partition minimum with the unrestricted stochastic stationary minimum.

---

## 3. Detailed correctness audit

### 3.1 The model and the constrained radius

The machine definition is coherent. A decoder map takes every terminal hidden label to a point of the legal compact convex output set. Averaging by the terminal hidden-state distribution remains in that set by convexity.

For categorical output, the half-`l1` norm is exactly total variation. For a binary mean, identifying the law with its mean gives the norm `|x-y|/2`, so the radius of an interval is one quarter of its length. The scalar predecessor is recovered with the correct factor.

Requiring the radius center to lie in `Y_j` is essential. An unconstrained center in the ambient vector space would not define a legal decoder.

### 3.2 The upper construction

The stationary upper machine stores `(s,c)`, where `s` is the seed and `c` is the current component in `H/K`. A command updates the component by left multiplication, consistent with the manuscript’s execution-order convention.

For each seed, query, and component, compactness gives a legal minimizing center of the component image. Using this center as the decoder gives the stated radius error. Command updates are permutations of a finite state set and are independent of the horizon.

Thus equality at the critical radius is attained by an actual machine, not merely by an infimum.

### 3.3 Positive-word density and common lengths

The positive semigroup generated by the command letters is dense in the compact group closure. Near returns of positive powers recover inverses in the closure.

Because the identity component is open under the finite-component hypothesis, positive executable products lying in it are dense there.

The cofinite return condition then pads finitely many executable products to one common length without changing their physical products. The argument does not confuse physical return with identity hidden-state processing.

### 3.4 The finite executable gap

For a fixed-point-free finite-dimensional orthogonal representation of the connected component, the Haar-averaged quantization defect over one moving unit vector and `k` unit centers has a positive compact minimum.

If the minimum were zero, continuity and full Haar support would put a connected orbit inside a finite set, forcing a fixed vector. This contradiction is valid.

Discretizing Haar measure by nearby executable products preserves a uniform positive defect because the maximum inner product is uniformly Lipschitz in operator norm. Zero-mass partition cells are irrelevant and are correctly discarded.

### 3.5 Conditional-centroid contraction

The block word is external and independent of the machine’s private randomness. Conditional on the incoming state and the selected word, the machine’s actual composite row produces the endpoint state.

Pairing each terminal conditional centroid with its unit direction and using stochasticity reduces the endpoint norm sum to the maximum over at most `k` centers. The finite executable gap then gives the contraction.

No lower bound on a hidden-state probability is used. Zero-probability labels contribute zero. Internal block widths may be arbitrary.

A fixed physical return word cannot increase the conditional centroid norm: the physical feature is unchanged at the endpoints, while the endpoint state is a stochastic coarsening of the previous state. Conditional Jensen is sufficient.

### 3.6 Representative functions and calibration

A finite family of real representative functions can be placed in one finite orthogonal representation. Haar averaging splits the feature into fixed and moving parts.

The displayed scalar, vector, and decoder calibration inequalities follow from this decomposition and Cauchy–Schwarz. They are moment statements and do not assert total-variation convergence of a hidden group variable.

The coefficient representations need not be unique; fixing any choices before defining the constants is enough.

### 3.7 Finite localization of the constrained radius

If the component image has radius above the target error, finitely many image points retain a strict radius margin. Compactness of `Y` upgrades the pointwise strict cover to a uniform strict minimum.

Representative functions uniformly approximate the vector target. Squared representative approximations to continuous bumps produce nonnegative mean-one localizers concentrated near the selected points.

The resulting weighted vector means preserve a strict constrained-radius margin. This is the correct vector replacement for the two scalar extreme-value weights in Revision 53.

### 3.8 The residual moment inequality

For a nonnegative localizer, wordwise correctness may be averaged under the externally selected word law before any feature estimate is used.

The unconditional expected decoder lies in `Y` by convexity. Calibration bounds compare it with every localized vector mean. If all moving conditional moments were too small, this one legal center would approximate all localized means inside a radius smaller than their certified constrained radius.

The contradiction gives the stated positive residual. The proof correctly uses conditional mean error of the decoder, not a pointwise error for each hidden label.

### 3.9 Occupation under cofinite returns

After a fixed component prefix, independent contraction blocks are placed immediately before greedily selected narrow cuts. Initial, intermediate, and final gaps are chosen long enough to be filled by executable identity-product words.

Each selected endpoint contracts the moving conditional moment by a fixed factor, while the terminal residual theorem supplies a fixed positive lower bound. Therefore the number of selected narrow endpoints is bounded.

The spacing count correctly converts this to a bound on all narrow cuts, including bounded losses at the beginning and end. Registers inside blocks and return gaps remain unrestricted.

When the whole profile has width at most `k`, the occupation bound directly bounds the horizon, so monotonicity under identity padding is unnecessary.

### 3.10 The three-outcome example

The displayed trigonometric law is a probability vector by discrete character orthogonality. Its image contains all three vertices of the probability simplex.

For any center `q`, the maximum total-variation distance to those vertices is `1-min_j q_j`, at least `2/3`. The uniform center is within `2/3` of every point of the simplex, so the constrained radius is exactly `2/3`.

Each individual coordinate ranges from zero to one, giving binary-event threshold `1/2`. The example genuinely separates joint-law preservation from marginal preservation.

### 3.11 The observable quotient and compact similarity

For linear outputs, componentwise constancy implies that every element of the identity component acts trivially on the reachable space modulo the invisible subspace. Normality is used correctly to propagate the statement through every future query.

Conversely, trivial identity-component action on the observable quotient makes every output componentwise constant. The generated group’s observable image then factors through the finite component group.

For a uniformly bounded group in `GL(D,R)`, Haar averaging produces an invariant positive-definite inner product. Conjugation to an orthogonal group preserves the numerical interface and exact return words. The proposition does not overreach to a merely bounded positive semigroup.

### 3.12 Harmonic localization near the critical error

For every fixed `epsilon<rho/2`, the localization degree `r` can be chosen so that the two weighted cosine means remain separated by more than the allowed mean error.

The Fourier coefficient estimates are deliberately crude but valid. The moving harmonic feature therefore has a positive terminal residual depending on the fixed subcritical parameters, not on the horizon or machine.

The localization degree increases as the error approaches the threshold, as it must. No uniform-in-error constant is claimed.

### 3.13 The arithmetic contraction law

The block construction produces at least `2k` distinct count vectors. The dual Diophantine inequality separates every nonzero harmonic frequency up to the required order.

For any unit feature vector, all orbit points are separated by the same positive distance. Any `k` unit centers can cover fewer than half the points by open balls of half that separation. Averaging the Euclidean squared-distance identity yields the stated inner-product defect.

Combining this defect with harmonic residual calibration gives the finite-horizon and occupation inequalities. Since the block length is of order `k^{1/s}`, inversion gives the exponent `s/(2tau+1)`; at `tau=s` this is `s/(2s+1)`.

### 3.14 The exact polygon realization

For a regular `q`-gon, rotating a vertex by an angle whose nearest rational `q`-multiple error is `h` enlarges the required facet support by

```text
cos(t-h)/cos(t).
```

The logarithmic dilation estimate is valid for the declared range. Scaling each rotated vertex by the reciprocal dilation places it inside the common polygon, so barycentric coordinates give legal stochastic command rows.

The initialization uses amplitude `a=(1+rho)/2`, made possible by the strict slack `rho<1`. Repeated row contractions produce a known scalar loss. The terminal decoder rescales by the reciprocal accumulated loss and remains bounded because of the enclosure inequality.

The resulting machine exactly realizes every length-`N` word. It is horizon-dependent but uses common legal rows within that horizon.

### 3.15 Comparable simultaneous denominators

Dirichlet’s pigeonhole argument gives a denominator `q<=Q^s` with simultaneous error at most `1/Q`.

A second pigeonhole argument among short integer vectors modulo `q`, combined with the dual Diophantine lower bound, prevents `q` from being too small. For `tau=s`, the lower and upper denominator orders match.

Choosing `Q` at the scale `N^{1/(2s+1)}` satisfies the polygon enclosure condition and yields `q=O(N^{s/(2s+1)})`. Together with the lower bound this proves the matching theorem.

### 3.16 The algebraic-circle bound

The resultant is a nonzero integer because the algebraic eigenvalue and all its conjugates are not roots of unity. Standard root bounds control the other conjugates and give an explicit exponential lower bound on `|lambda^n-1|`.

This produces a logarithmic width lower bound over the full subcritical interval. The paper correctly does not describe it as sharp or infer a badly approximable angle condition from algebraicity of matrix entries.

### 3.17 Effective rational classification

The effectivity theorem has a credible termination proof in its declared input model.

Established algorithms compute a finite algebraic description of the rational matrix group’s Zariski closure. In the compact orthogonal setting, real connected-component algorithms then describe the Euclidean compact group and its real components. Quantifier elimination computes constrained categorical radii and algebraic centers.

For the occupation constant, the paper does more than compute the threshold. It enumerates positive polynomial localizers and executable finite word laws, and uses decidable strict semialgebraic inequalities to detect successful witnesses. Density and the analytic proof guarantee termination.

For a fixed horizon and width, all machine variables range over compact simplexes and every word-output constraint is semialgebraic. Increasing the width eventually reaches a finite exact prefix-storing realization. Thus the least finite-horizon width is computable.

These are computability statements, not practical or polynomial-time algorithms. The manuscript maintains that distinction.

### 3.18 The component-quotient minimum

An equivariant partition of seed-component pairs induces well-defined command permutations. A radius center for each block-query output union gives the corresponding decoder.

Conversely, the fibers of any deterministic component-quotient encoding are equivariant, and density plus continuity forces its decoder to cover the entire block output union.

The finite partition formula is therefore exact in the stated class. The manuscript explicitly disclaims unrestricted stochastic minimality, so I find no correctness overclaim here.

---

## 4. Main limitations at the top-four level

### 4.1 The synchronization condition remains a major structural boundary

The cofinite exact-return condition is a useful and correctly proved replacement for an identity letter. It is not intrinsic to the compact group alone; it is a property of the chosen generating alphabet together with word length.

There are intermediate return languages—periodic length classes, multiple phases, or sparse but structured returns—for which one expects a phase-refined classification rather than either the present theorem or the one-letter counterexample.

A leading general-journal result would ideally characterize the exact synchronization hypothesis, perhaps through the finite automaton or semigroup of return lengths, rather than assume cofiniteness.

### 4.2 Infinite component groups remain untreated

The upper construction stores the finite component class. For a compact group with infinitely many connected components, a finite interface may still factor through a finite observable quotient or admit bounded approximation without storing the whole component space.

The correct obstruction in that setting may involve the constrained radius over fibers of a finite observable quotient rather than individual connected components. This potentially broad extension is absent.

### 4.3 The irreversible case is outside the theory

The scalar contraction example correctly shows that compact-group reasoning cannot simply be copied to an irreversible semigroup. Nevertheless, general stochastic and positive systems are predominantly irreversible.

A classification that distinguishes reversible compact directions from stable or nilpotent directions would have much broader realization-theoretic impact. The current theorem deliberately does not attempt it.

### 4.4 The quantitative theorem is still a special arithmetic model

The full-subcritical matching theorem is a real advance, but it is confined to planar rotations with a dual badly approximable vector and a precise upper alphabet.

There is no analogous sharp growth theorem for:

- higher-dimensional compact tori with general representations;
- compact nonabelian Lie groups;
- broad noncommuting matrix alphabets;
- generic algebraic rotations;
- the endpoint `rho=1`;
- or general categorical output maps.

Thus the paper does not yet provide a general quantitative theory below the radius threshold.

### 4.5 The effective result has no useful complexity classification

The proof imports algorithms with potentially extreme complexity and then adds nested searches over polynomial localizers, word laws, quantifier elimination, and width.

Termination is mathematically meaningful. It does not tell the reader whether any nontrivial input beyond the hand-worked examples is computationally accessible, nor does it identify the natural decision complexity of the problem.

### 4.6 Boundary-state minimality remains only partially resolved

The component-permutation construction is canonical and finite, but the least unrestricted stationary stochastic width at the threshold is not characterized. Randomized encodings can merge component behaviors in ways not captured by deterministic equivariant partitions.

This is not a flaw in the stated quotient theorem. It is an important unresolved structural question immediately adjacent to the principal result.

### 4.7 The primary resource has limited computational interpretation

The lower theorem survives a very permissive model, which is mathematically impressive. But the same model makes direct claims about memory or implementable automata hazardous.

A horizon-specific family may use arbitrarily complicated real tables and exact samplers for free. The effective rational section does not retroactively price the general theorem. The article should continue using “nonuniform stochastic label width” rather than unqualified “memory.”

### 4.8 External priority remains uncertain

The revised comparison section is much stronger than earlier repository audits. It now distinguishes fixed-machine equivalence, language recognition, positive realization, topological recognition, bisimulation metrics, and the manuscript’s horizon-dependent minimization.

Nevertheless, a final publication decision requires experts in probabilistic automata, weighted series, compact dynamical recognition, almost-periodic functions, positive systems, and approximate realization to assess whether an equivalent minimax statement or occupation principle is already implicit in a different formalism.

The repository’s own audit appropriately does not certify exhaustive novelty.

---

## 5. Novelty and significance

The genuinely new-looking package is the following combination:

1. a constrained component-image Chebyshev radius for a full compact-convex output law;
2. equality attained by a finite component-permutation machine;
3. a converse against a separately redesigned stochastic machine at every horizon;
4. an occupation bound for arbitrarily separated cuts of fixed width;
5. an intrinsic representative-function proof on compact Hausdorff groups;
6. a matching full-subcritical polynomial width law for a nontrivial Diophantine family; and
7. a terminating rational-algebraic specialization.

I regard this as a serious specialist-level contribution, subject to priority review.

The reason I do not recommend a top-four journal is not that any individual hypothesis is fatal. It is that the broad classification is qualitative and tied to reversible synchronized group actions, while the sharp quantitative theorem is narrow and arithmetic. The manuscript has not yet converted its elegant mechanism into a result with broad consequences across a major established area.

Possible routes to a qualitatively stronger paper include:

- a classification for compact groups with arbitrary return-length phases;
- an observable finite-quotient theorem for infinitely many connected components;
- a reversible-plus-contracting decomposition covering noninvertible compact or bounded semigroups;
- matched subcritical growth for a broad class of compact Lie-group representations;
- a structural characterization of the unrestricted stochastic boundary minimum;
- or a meaningful complexity classification for the rational input problem.

Any one of these would move the work materially closer to a general-journal standard.

---

## 6. Relation to the repository-wide pipeline

The local mathematical dependency chain used by Revision 54 is coherent:

```text
common stochastic-row compatibility
  -> moving conditional feature contraction
  -> representative-function localization
  -> constrained component-image radius
  -> boundary component-permutation realization
  -> subcritical narrow-cut occupation.
```

The quantitative chain is also coherent:

```text
positive harmonic localization
  + dual Diophantine separation
  -> finite executable orbit packing
  -> full-subcritical endpoint contraction
  + regular-polygon common-row realization
  + comparable simultaneous denominators
  -> matching polynomial width.
```

The effective chain imports external algebraic algorithms and then adds radius, localizer, word-law, occupation, and fixed-horizon machine searches.

These are real local advances.

They do **not** discharge any of the model-specific analytic gates in the frozen Round-Seventeen graph:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1,
```

with A1 separate.

Those chains require raw Fourier/density local limits, stopped entropy/LDP, a global past kernel, canonical coefficients and shell conditioning, process CLT/Mosco recovery, nonlinear Nisio resolvents and graph cores, filtering/QMD/LAN, strict/form response, changing-filtration projection, and labelled posterior contraction.

The compact-group stochastic-realization theorem neither uses nor proves those obligations. Revision 54 correctly claims no closure of:

- historical A2 replacement;
- B4 aggregate closure;
- C2 aggregate closure;
- the eleven-paper aggregate;
- or the wider Theta analytic program.

This separation is a strength of the repository records. It also means that “Foundations” provenance and cumulative pipeline volume cannot be used as evidence of top-four significance for the present standalone article.

---

## 7. Resource-model assessment

The manuscript now states its accounting clearly.

Charged:

- every available persistent label at every command cut;
- retained private randomness or selectors;
- zero-mass padding if declared available.

Free:

- the horizon and external epoch;
- redesign at every horizon;
- arbitrary real transition and decoder tables;
- table construction and lookup;
- exact real arithmetic;
- atomic sampling from prescribed real rows;
- and, in the main lower model, coefficient-description size.

The final output alphabet can be charged separately without changing boundedness or the principal growth laws for fixed finite outputs.

This is a coherent positive-realization invariant. It is not ordinary memory, uniform state complexity, program length, running time, random-bit complexity, or finite-precision implementation cost.

The rational finite-group compiler retained in the supplement and the rational-algebraic effectivity theorem answer different questions. They should not be used to market every arbitrary-real width theorem as implementable.

---

## 8. Reproducibility and publication audit

The exact reviewed publication head is one commit beyond the validated source commit. The derived publication commit does not silently change theorem source.

Workflow `36308068660` completed successfully. Its qualification job:

- materialized readable native source;
- installed fixed dependencies;
- ran new and inherited exact checks in normal and optimized Python;
- compiled the main article and retained documents;
- verified source identities;
- rebuilt the native archive in isolation;
- compared all text and raster pages;
- and published the referee-ready branch without changing native theorem source.

The build receipt records:

```text
main article:                 20 pages
scalar predecessor:           14 pages
companion notes:               4 pages
complete supplement:          68 pages
native source files:          91
new exact finite assertions:  81,594
named new negative controls:  21
negative-control executions:  42
normal/optimized agreement:   true
isolated text equality:       true
isolated raster equality:     true
```

No undefined references, malformed bookmarks, or overfull boxes are reported for the built documents.

This is unusually strong delivery and regression evidence. It does not establish the universal theorems, exhaustive priority, or editorial suitability. I assign it exactly the former credit and none of the latter.

---

## 9. Required revision before specialist submission

### 9.1 Freeze the central claim and remove residual series rhetoric

The standalone title is appropriate. The submission should consistently present itself as a paper on stochastic realization of compact-group numerical interfaces, not as evidence for a broader unnamed Foundations program.

Repository provenance may remain in metadata, but the journal-facing paper should stand entirely on the displayed theorems.

### 9.2 Obtain a conventional independent priority audit

The author should solicit or perform theorem-level comparison with experts in:

- numerical probabilistic automata;
- weighted and rational series;
- approximate positive realization;
- almost-periodic functions and Bohr compactifications;
- compact and profinite automata;
- quantitative group languages;
- controlled hidden Markov realization;
- and minimization under additive output error.

A novelty table written by the author is useful, but it is not a substitute for external assessment.

### 9.3 Clarify the exact role of synchronization

State prominently that the radius formula is not a theorem for an arbitrary dense alphabet in the compact group. It also needs the cofinite exact-return condition.

The introduction should explain what is known when identity returns have a nontrivial period or lie in finitely many residue classes. Even a phase-lift proposition would substantially improve the conceptual completeness.

### 9.4 Separate classification from quantitative consequences

The radius theorem and the Diophantine width theorem have distinct assumptions and proof mechanisms. The article mostly handles this correctly, but the abstract and conclusion should make the separation unmistakable.

In particular:

- rational matrix entries do not imply dual bad approximability;
- the exact upper law requires `rho<1`;
- extra letters are allowed for the lower bound but not silently for the upper bound;
- and the algebraic-circle logarithmic theorem is a different class from the matched badly approximable theorem.

### 9.5 State the open boundary-minimization problem explicitly

The finite quotient theorem solves deterministic component quotients only. The paper should formulate the unrestricted stationary stochastic minimum at `epsilon_c` as an open problem and explain whether randomization can strictly reduce the deterministic quotient width.

### 9.6 Give a realistic effectivity discussion

The current theorem correctly claims computability, not efficiency. Add a short roadmap of the nested algorithmic costs:

- closure construction;
- real-component decomposition;
- radius quantifier elimination;
- localizer enumeration;
- word-law enumeration;
- gap certification;
- and finite-horizon width search.

Even coarse upper complexity classes or explicit acknowledgment that no primitive-recursive-quality bound is extracted would help readers interpret the result.

### 9.7 Preserve the resource distinction

Use “nonuniform stochastic label width” consistently. Avoid unqualified computational-memory terminology in the abstract, introduction, and publicity.

### 9.8 Add one nonbinary worked example beyond the simplex vertices

The three-outcome example is excellent but maximally symmetric. A second categorical example with a proper curved image, nonuniform optimal center, and nontrivial component quotient would demonstrate the radius theorem’s actual geometric content rather than only the simplex extremal case.

### 9.9 Do not assign pipeline closure credit

Keep all A/B/C/D aggregate flags fail-closed. The compact-group theorem is independently valuable and does not need unsupported claims of global pipeline completion.

---

## 10. Local comments

1. In the model definition, state explicitly whether command width counts unused padding labels. The surrounding resource prose implies yes.
2. When discussing a categorical terminal register, distinguish the decoder’s output dimension from an actual sampled answer register.
3. In the radius definition, say once that the component image is compact by continuity.
4. In the upper construction, state that labels for unreachable seed-component pairs remain counted if included in the advertised state set.
5. In the positive-word lemma, spell out the step from a near identity power `u^r` with `r>=2` to the near inverse `u^{r-1}`.
6. The finite-component hypothesis should be repeated at the point where openness of `K` is used.
7. In the executable-gap lemma, specify that repeated centers are allowed, as the response already notes.
8. In the calibration section, keep the coefficient choices fixed before defining every norm-dependent constant.
9. In the radius-localization lemma, add one sentence that compactness turns the finite pointwise strict cover into a uniform strict margin.
10. In the residual proposition, display the bound on `E p_i` that contributes the `delta ||a_{p_i}|| Q` term.
11. State the dependencies of `B`, `d`, `chi`, and `L_k` immediately after the occupation theorem.
12. The count in `L_k` deliberately excludes cut zero; retain that convention in every corollary.
13. In the three-outcome example, say explicitly that the total-variation diameter of the simplex is one, so half its diameter is one half.
14. In the unitary corollary, `U(d)` is connected; saying so removes any possible ambiguity about components.
15. For the toral formula, keep the surjectivity onto the full product torus in the theorem statement, not only in commentary.
16. In the Diophantine condition, state that `b<=1/2` follows by testing a coordinate unit vector; this is used in the block-separation estimate.
17. Distinguish the localization order `r` from the command count `s` every time both appear in a displayed bound.
18. In the arithmetic block theorem, note explicitly that `B>=1` for all `k>=1`.
19. In the open-ball packing argument, retain the open-ball convention so equality at the separation radius causes no double counting.
20. In the polygon proof, one line with the facet-support function would make the inclusion transparent.
21. State that the standard reflection preserves the chosen orientation of the regular polygon.
22. In the comparable-denominator lemma, clarify that the residue computation is modulo `q` even when nearest integers `p_i` are negative.
23. In the algebraic-angle example, emphasize that `1,xi,...,xi^s` are linearly independent over the rationals by the degree assumption.
24. In the effective theorem, cite the precise compact-orthogonal fact ensuring that the real points of the computed algebraic closure equal the Euclidean group closure.
25. Explain how algebraic Haar moments are represented and compared in the enumerated localizer search.
26. In fixed-horizon feasibility, note that every rational command word gives a rational target vector under rational polynomial readouts.
27. In the quotient theorem, keep left-versus-right component multiplication consistent with the global word convention.
28. State separately that generator equivariance implies full finite-group equivariance because the generator images generate `C`.
29. The matched theorem excludes `rho=1`; list the endpoint as an open quantitative case.
30. The build receipt should continue to distinguish assertions executed by finite regression from universal statements proved only in prose.

---

## 11. Final disposition

Revision 54 is not a cosmetic response to r35. It advances the mathematics in three independent directions:

- scalar outputs to constrained categorical and joint outputs;
- identity-letter synchronization to cofinite exact returns;
- and qualitative subcritical divergence to a matched polynomial law on a substantial Diophantine family.

The proofs appear sound in their declared scope, and the manuscript is now a coherent standalone article.

My recommendation nevertheless remains:

```text
Reject at the Annals / Inventiones / JAMS / Acta level.
```

The decisive issue is no longer absence of a theorem, lack of focus, or a fatal correctness problem. It is that the broad theorem is qualitative and confined to synchronized reversible compact-group dynamics, while the sharp quantitative theorem is specialized to planar Diophantine rotations. The effective result is computability without tractable complexity, and the priority boundary remains incompletely settled.

For a strong specialist venue, however, the paper is now viable in principle. I would encourage submission after a conventional external priority review, a final clarification of synchronization and resource scope, and modest strengthening of the categorical examples and open-problem discussion.
