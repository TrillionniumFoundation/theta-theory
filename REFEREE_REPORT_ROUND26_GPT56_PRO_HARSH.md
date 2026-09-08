# External Referee Report on the Purported Round-Twenty-Five Revision

## Recommendation: **Return without re-review and reject all eleven manuscripts; the Round-Twenty-Four report remains dispositive**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Purported revision branch:** `revision/round25-referee-positive-closure-11paper-2026-09-02`  
**Purported revision head:** `e56c2ed5775a072d8dfb38546775f17889094e43`  
**Review branch:** `review/round26-gpt56-pro-harsh-11paper-2026-09-02`  
**Review date:** 2 September 2026  
**Prior external report:** `REFEREE_REPORT_ROUND24_GPT56_PRO_HARSH.md`

This report applies the submission-integrity, correctness, self-containedness, novelty, and presentation threshold expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*.

The principal finding is preliminary but decisive:

> **There is no Round-Twenty-Five mathematical revision in the branch submitted for review.**

The branch called `revision/round25-referee-positive-closure-11paper-2026-09-02` is source-identical to `revision/round23-referee-positive-closure-11paper-2026-09-02`. Both refs point to the same commit, namely the commit that added the preceding external referee report. The comparison contains zero commits and zero changed files. The repository tree contains no active `ROUND25` source, no Round-Twenty-Four author response, no revised wrapper, no new theorem statement, no changed proof, no new bibliography interface, and no mathematical diff responding to the Round-Twenty-Four objections.

The eleven active wrappers still identify `ROUND23-REFEREE-POSITIVE-CLOSURE` as the controlling revision and still import `ROUND23_POSITIVE_CLOSURE.tex`. Thus the object presented under the Round-Twenty-Five branch name is exactly the object already reviewed in Round Twenty Four, augmented only by the referee's own report.

A new branch label is not a mathematical revision. There is consequently no basis for a new substantive referee round. The previous rejection stands in full.

---

## 1. Confidential recommendation to the editor

I recommend that the editor **return this purported revision without re-review and reject the eleven-paper dossier**.

This is not a case in which the authors made an inadequate response. No response or mathematical revision has been supplied at all. Sending the unchanged dossier back to specialist referees would consume substantial expert time without a reviewable delta.

The editorial record should state four facts clearly.

1. The purported Round-Twenty-Five branch and the already reviewed Round-Twenty-Three branch are identical at the commit level.
2. The head commit is the referee-report commit, not an author-revision commit.
3. The active manuscripts remain Round-Twenty-Three manuscripts.
4. Every mathematical blocker in the Round-Twenty-Four report is therefore unresolved.

I would not classify this as “major revision required.” A major-revision decision presupposes a coherent manuscript and a finite set of correctable gaps. The previous report identified direct contradictions, ill-typed expressions, invalid compactness and closed-range arguments, and missing root theorems. The present branch changes none of them.

The appropriate disposition is:

> **Administrative return without re-review, with the prior rejection maintained.**

---

## 2. Source-identity audit

### 2.1 Exact branch comparison

The exact Git comparison between

- `revision/round23-referee-positive-closure-11paper-2026-09-02`, and
- `revision/round25-referee-positive-closure-11paper-2026-09-02`

reports:

```text
status: identical
ahead_by: 0
behind_by: 0
total_commits: 0
files: []
```

Both branch refs resolve to

```text
e56c2ed5775a072d8dfb38546775f17889094e43
```

whose commit message is

```text
Add Round Twenty-Four external harsh referee report
```

This is conclusive. The purported revision branch contains no author-side commit after the preceding external review.

### 2.2 No Round-Twenty-Five active source exists

A recursive tree inspection finds no path containing `ROUND25`. In particular, there is no:

```text
ROUND25_POSITIVE_CLOSURE.tex
ROUND25_REVISION_STATUS.md
ROUND25_PROOF_DEPENDENCY_LEDGER.md
REFEREE_ROUND24_RESPONSE.md
AUTHOR_RESPONSE_ROUND24.md
```

and no per-paper Round-Twenty-Five replacement source.

The absence of a particular naming convention would not itself be fatal if the active sources had changed. They have not changed. The no-`ROUND25` result is therefore corroborating evidence, not the primary evidence.

### 2.3 The wrappers still activate Round Twenty Three

For example, the active A4 wrapper on the purported Round-Twenty-Five branch states:

```text
Controlling revision: ROUND23-REFEREE-POSITIVE-CLOSURE
Registered proof source: ROUND23_POSITIVE_CLOSURE.tex
Round-Twenty-Two referee response: AUTHOR_RESPONSE_ROUND22.md
```

and executes

```tex
\input{ROUND23_POSITIVE_CLOSURE.tex}
```

The same Round-Twenty-Three source architecture is retained across the dossier. There is no wrapper-level switch to a new mathematical manuscript.

### 2.4 The only new material relative to the pre-report source is the referee's own report

The current head is the commit that added `REFEREE_REPORT_ROUND24_GPT56_PRO_HARSH.md`. A referee report is not an author response, proof repair, or replacement theorem. Renaming a ref that points to this commit cannot transform that report into a mathematical revision.

### 2.5 Consequence for this referee round

There is no new theorem package to compare, no response matrix to test, and no revised proof whose correctness can be reassessed. The correct comparison baseline is therefore not “Round Twenty Five versus Round Twenty Four”; it is “the unchanged Round-Twenty-Three source versus the already issued Round-Twenty-Four report.”

That comparison was completed in the preceding round. Its result remains rejection.

---

## 3. Unresolved decisive blockers carried forward verbatim in substance

For completeness, I restate the most decisive mathematical failures. These are not newly discovered defects in a new source. They are unresolved defects in the unchanged active source.

### 3.1 A4: finite-step minorization is impossible on the exact complete-past state

A3 defines the state as a complete left-infinite history, and A4 updates that history by appending a new mark and shifting. After any finite number `n` of updates, the old remote tail has not been forgotten as a state coordinate; it has merely moved `n` places farther into the past.

For each initial history `h`, let `A_h^n` be the cylinder of histories whose coordinates beyond the newest `n` positions agree with the shifted initial tail of `h`. Then

```text
P^n(h,A_h^n)=1.
```

Choose two histories `h` and `h'` with different remote tails. Their sets `A_h^n` and `A_{h'}^n` are disjoint. A common minorization

```text
P^{n_L}(h,.) >= epsilon_L nu_L(.)
```

for every `h` in a Lyapunov sublevel would force `nu_L` to be supported simultaneously on disjoint exact-tail cylinders. Hence `nu_L=0`, contradicting that it is a probability measure.

This is not a missing estimate. It is a direct contradiction between the state definition and the claimed small-set theorem.

The correct tool for a complete-past representation, if one exists, would be a contraction in a quotient or Wasserstein-type distance that discounts remote coordinates—not a Doeblin minorization on exact histories.

### 3.2 A4: the displayed “weighted Lipschitz” seminorm does not impose continuity

The active source uses a denominator of the form

```text
(1+d_sigma(h,h'))(V(h)+V(h')).
```

Because this denominator does not vanish when `d_sigma(h,h') -> 0`, any function satisfying `|f(h)| <= C V(h)` automatically has bounded quotient:

```text
|f(h)-f(h')| / [(1+d_sigma(h,h'))(V(h)+V(h'))] <= C.
```

Thus the claimed seminorm does not control local oscillation. Discontinuous functions with weighted growth can belong to the space. A Feller or analytic perturbation theorem cannot be based on calling this quantity a Lipschitz norm.

The denominator would need a genuine distance factor, together with a proof that the kernel contracts or regularizes in that metric.

### 3.3 A4: the renewal formula is ill typed

The active source declares maps with types schematically equivalent to

```text
E(z): X -> Y
X(z): Y -> X
T(z): Y -> Y.
```

It then writes

```text
E(z)(I-T(z))^{-1}X(z).
```

Read from right to left, `X(z)` produces an element of `X`, while `(I-T(z))^{-1}` expects an element of `Y`. The composition is therefore undefined with the displayed types.

In addition, the formula defining `E(z)f(h)` integrates over a flight associated with a mark `m` that is not bound or selected by `h` in the displayed expression. The entry operator is not a well-defined map as written.

No source-identical branch can repair this typing failure.

### 3.4 A2: scalar coarea integration does not prove an anisotropic operator estimate

The active A2 source derives a scalar oscillatory-integral estimate on one collision chart and promotes it to a uniform norm estimate

```text
||L_{u,b}^n||_{B -> B_w}
```

for a singular countable-branch transfer operator. The manuscript does not prove the required stable-curve decomposition, distortion after repeated vector-field integration, compatibility with the strong/weak anisotropic norms, or cancellation of boundary and fold terms at operator level.

The treatment of words with too few good UNI blocks is also not valid as written. One cannot obtain a factor for the present `n`-iterate by “delaying the integration until a future good block” unless the time decomposition, exceptional mass, and resulting operator norm are proved uniformly. The scalar paragraph does not establish the global Fourier theorem imported by A3 and A4.

### 3.5 A3: the promised corrected projective state is not in the active source

The repository's later audit documents acknowledge that the earlier path scaling and recession notation were not complete measurable objects and promise a projective family of thresholded ordered lists with compatibility maps. That construction is not present in the active Round-Twenty-Three source.

The active source still moves rapidly from an ordered marked point measure and an informal recession compactification to a good stopped-path Laplace principle. It does not construct the full Polish projective state, prove measurability of every threshold component, establish consistency across thresholds, or prove exponential tightness of the actual time-reparametrized path coordinate.

The conditional-reference entropy quantization idea is useful, but it is only one component of the required LDP proof.

### 3.6 B2: the loop-opening estimate lacks a rank/nonvanishing theorem

The active B2 argument introduces an analytic determinant ideal and invokes a Łojasiewicz sublevel estimate. Such an estimate is useful only after proving that the relevant determinant is not identically zero on each component under consideration.

The manuscript does not prove:

- that every graph-theoretic surplus edge supplies an independent geometric loop constraint;
- that the maximal-minor ideal is nonzero after all previous contact equations have been imposed;
- that chronology, conservation, label symmetries, and recollision degeneracies do not force a component into the zero ideal;
- or that the claimed number of transverse coordinates equals the cyclomatic number.

An analytic function may vanish identically on a component. Łojasiewicz theory does not create rank. Therefore the additional factor `epsilon^{alpha s(G)}` is not established.

The later factorial hierarchy and finite-time propagation depend on precisely this missing root estimate.

### 3.7 B1: the global Fourier majorant is not uniform

The active B1 source contains a term of the form

```text
C_N (1+|v|)^{-s theta N}.
```

No usable bound on `C_N` is supplied. If `C_N` grows faster than the damping compensates, the displayed expression yields no uniform integrable characteristic-function majorant.

The deterministic label-block idea avoids one measurability problem, but the proof still needs:

- a uniform positive fraction of usable blocks on every relevant conditional configuration;
- controlled exceptional configurations;
- uniform boundary-flat chart constants;
- and a product estimate whose constants remain subexponential in `N`.

None is proved at the strength required for the exact-number coefficient theorem.

The third-pass audit promises a different high-frequency theorem and an exact-fibre coarea disintegration, but those repairs were not committed to the active source.

### 3.8 B3: the displayed graph theorem has an uncontrolled infinite-dimensional kernel

The active balance operator has the form

```text
B(u,h) = (partial_t u + v.grad_x u - DQ_f[u] - C h, u(0)).
```

The collision-to-density map `C` has a large kernel: there are many nonzero signed collision defects `h` whose gain-minus-loss velocity marginal vanishes. For every such `h`,

```text
B(0,h)=(0,0).
```

Hence the full graph operator has an infinite-dimensional kernel in the collision-defect coordinate unless that kernel is explicitly quotiented or penalized by the image norm. The manuscript's description of the null directions and the inference of a bounded right inverse do not address this.

A coercive estimate for `u` alone does not provide a right inverse controlling `h`, and it does not justify the nonlinear balance correction later required by B3 and B4.

### 3.9 B3: deterministic microscopic restart does not supply stopping-time cumulants

Conditioning on the complete hard-sphere phase point at a stopping time makes the future deterministic. It does not regenerate an independent prepared ensemble to which the original connected-cumulant expansion can simply be reapplied with the same uniform constants.

A stopping-time estimate would require a theorem about the conditional law of the remaining random initial configuration or a history hierarchy stable under the stopping sigma-field. The active proof contains neither. Thus the stated conditional increment estimate and the process CLT are not established.

### 3.10 B4: the original action does not propagate the asserted superquadratic moment

The state assumes a polynomial `p=2+delta` velocity moment. The proof invokes the entropy Young inequality with a test comparable to `|v|^p`. The dual term is of exponential type:

```text
A_f (exp(c|v|^p)-1).
```

A polynomial `p`-moment does not control that term. Therefore the written argument cannot propagate the superquadratic containment required for compactness in `W_2`.

One needs a genuine Povzner-type estimate, an upstream exponential collision-source bound with the exact admissible constants, or a different containment functional. The third-pass audit acknowledges this issue and promises such a repair, but the active source contains only the invalid one-line argument.

Without compact action sublevels, the Nisio optimizer, comparison argument, and nonlinear semigroup limit have no established state space.

### 3.11 C1: deterministic hidden dynamics and smooth conditional observations are inconsistently typed

The active C1 source sets

```text
M_theta^a(x,dx') = delta_{Phi_theta^a(x)}(dx')
```

while also claiming that, conditional on the hidden state, the physical observation block has an `L^1` density produced by A2 or B1.

For the noiseless deterministic billiard and hard-sphere systems described in the dossier, there are two possibilities.

1. `x` is a complete microscopic/history state. Then the next state and every deterministic aggregate of that trajectory are fixed; the conditional observation is a Dirac mass, not a smooth density.
2. `x` omits unresolved coordinates so that a conditional observation density may exist. Then the next hidden state is governed by a nontrivial conditional kernel, not by a deterministic Dirac map.

The manuscript does not add an independent observation-noise kernel that would reconcile these statements. Consequently the filtering model from which Feller continuity, LAN, and BvM are derived is not the model supplied by the mechanical papers.

### 3.12 C2: the adjoint and optional-projection theorems remain incomplete

B3's graph operator includes the initial value as an output. C2 drops that output when writing the operator whose adjoint it computes. The annihilator must contain the corresponding boundary source; the displayed adjoint formula is incomplete even before importing B3's invalid closed-range theorem.

The rigidity argument also extrapolates a local analytic pressure identity along unbounded exposing rays, although the active A4 pressure theorem is stated only on a small source ball. The complete-ray hypothesis promised by a later audit is absent.

Finally, a current-state prediction process

```text
Pi_t = Law(X_t | Y_{<=t})
```

determines conditional expectations of functions of `X_t`, not arbitrary functionals of the entire hidden path. The optional-projection theorem is false at the advertised path-functional level unless the hidden state is augmented by the required path information.

### 3.13 D1: the leading max-plus limit cannot remember a shared policy

For finitely many real functions `G_j(alpha)`, one has the exact algebraic identity

```text
sup_alpha max_j G_j(alpha) = max_j sup_alpha G_j(alpha).
```

Therefore a scalar leading-order log-sum-exp/max-plus limit cannot distinguish “one common policy” from phasewise pre-optimization. The shared-policy constraint can survive only in finite-scale values, phase-resolved outputs, near-optimal policy sets, or subleading asymptotics.

The repository's second-pass audit explicitly acknowledges this and promises a subleading theorem. The active D1 source still ends with the leading formula and claims that it retains the shared-policy content. It does not.

The same paper additionally assumes a joint local normal form in an arbitrary path variable that no upstream theorem provides.

---

## 4. Paper-by-paper disposition

| Paper | Disposition on the purported Round-Twenty-Five branch | Reason |
|---|---|---|
| **A1** | Reject / unchanged | No Round-Twenty-Five source or response. The prior concern that a short typed-domain construction does not establish the advertised all-order geometric current theory remains unaddressed. |
| **A2** | Reject / unchanged | No operator-level proof of the global anisotropic Fourier estimate or concrete certified family. |
| **A3** | Reject / unchanged | No committed projective ordered/recession state or complete path-level exponential-tightness proof. |
| **A4** | Reject / directly false | Exact complete-past minorization is impossible; the norm is not Lipschitz; the renewal product is ill typed. |
| **B1** | Reject / unchanged | The conditional block theorem and uniform full-frequency majorant are not proved; `C_N` is uncontrolled. |
| **B2** | Reject / root theorem absent | The determinant ideal may vanish identically; loop smallness and finite-time history propagation are not proved. |
| **B3** | Reject / directly false or incomplete | Infinite-dimensional collision-defect kernel and invalid stopping-time restart defeat the range and process theorems. |
| **B4** | Reject / unchanged | The original action does not provide the asserted moment containment; the microscopic semigroup realization remains formal. |
| **C1** | Reject / mistyped model | Deterministic Dirac hidden transitions and smooth noiseless conditional observations cannot simultaneously describe the claimed state. |
| **C2** | Reject / unchanged | Boundary adjoint terms, pressure-ray hypotheses, and path-valued prediction are missing; failed upstream results are imported. |
| **D1** | Reject / algebraic contradiction | The leading max-plus value loses the shared-policy constraint, and the promised subleading repair is absent. |

There is no mathematically honest basis for changing any disposition from the preceding external report.

---

## 5. Why repository checks cannot convert this into a revision

The repository contains build workflows, theorem-label checks, dependency ledgers, hash manifests, and regression tokens. These may be useful for provenance. They do not answer the source-identity problem and cannot validate the missing mathematics.

In particular, a script can verify that a file contains strings such as

```text
A2-QUANTITATIVE-DIOPHANTINE
B4-ACTION-COERCIVE-CONTAINMENT
C2-EXPOSING-RAYS
D1-SHARED-POLICY-SUBLEADING
```

only if those strings and their proofs are in the active source. A workflow or payload that could generate a future file is not the manuscript under review. Referees review committed active mathematics, not latent patch programs or audit claims.

Nor can a regression script establish:

- a nonvanishing determinant ideal on every singular graph component;
- a uniform anisotropic transfer-operator estimate;
- a stopped conditional cumulant theorem;
- exponential tightness in a projective path space;
- a nonlinear kinetic compactness theorem;
- or a policy-uniform Bernstein--von Mises theorem.

The present submission fails before those distinctions become subtle: the purported new branch contains no new source at all.

---

## 6. Minimum admissibility requirements for any future resubmission

Before another external referee round is requested, the repository should satisfy all of the following.

### 6.1 A real source diff

The new revision ref must be ahead of the reviewed ref by author-side commits that modify the active manuscript source. A comparison returning `identical` should automatically block submission.

### 6.2 One active source of truth

Every wrapper must identify and import the actual revised source. Audit documents, responses, manifests, and workflows must refer to the same source hash. A branch called Round Twenty Five must not continue to advertise Round Twenty Three as its controlling revision unless the authors explicitly state that no new manuscript is being submitted.

### 6.3 A point-by-point author response

There must be a Round-Twenty-Four response that maps each decisive objection to:

- the corrected definition or theorem;
- the exact active file and label;
- the mathematical argument replacing the refuted step;
- and the downstream interfaces affected by that correction.

### 6.4 No audit-only repairs

A repair described in a self-audit is not complete until the exact theorem and proof appear in the file imported by `main.tex`. Generated payloads and future patch scripts are irrelevant to the current review state.

### 6.5 Narrow the submission

The next scientifically meaningful submission should contain one root paper, preferably A2 or B2, rather than eleven mutually dependent manuscripts. Downstream memory, filtering, BvM, semigroup, and phase-synthesis papers should not be reviewed until their root theorem has survived specialist scrutiny.

### 6.6 Concrete proof objects

For A2, provide a concrete billiard family and an operator-level Fourier theorem. For B2, provide a complete collision-history hierarchy, graphwise nonvanishing/rank theorem, cutting estimate, and finite-time propagation. These are not replaceable by status declarations.

### 6.7 Independent specialist review

The billiard and hard-sphere roots require different specialist referees. Only after those roots are accepted as mathematically sound should operator-memory, filtering, asymptotic-statistics, and control synthesis be considered.

---

## 7. Final verdict

The branch submitted as the latest revision is exactly identical to the already reviewed Round-Twenty-Three branch and points to the commit that added the Round-Twenty-Four referee report. It contains no Round-Twenty-Five manuscript, no author response, and no mathematical modification.

Accordingly:

- there is no new revision to review;
- the Round-Twenty-Four mathematical objections remain unanswered;
- the direct contradictions and typing failures remain in the active sources;
- and the eleven-paper dependency chain remains invalid at multiple root nodes.

A top-four mathematics journal should not initiate a new referee cycle for a source-identical branch alias.

**Recommendation to the editor: return the purported Round-Twenty-Five revision without re-review and maintain rejection of all eleven manuscripts. Any future submission must contain a genuine, source-visible, self-contained mathematical revision rather than a renamed branch pointing to the previous referee-report commit.**
