# Referee Report — General Theta Foundations I, Revision 94 (r61)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current linked supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed complete branch:** `revision/general-theta-foundations-i-v94-r60-spectral-value-2026-10-06`  
**Reviewed exact final head:** `db6739da3487be8787a67fc175b9086bd62f0e80`  
**Mathematical publication object:** `0919ff61895716ea3de1d6a0f2a6a291935764d0`  
**Qualified native source:** `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`  
**Completed predecessor publication:** Revision 93, `3b660839818d6ef676da72fb6e9969501be4e59a`  
**Predecessor native source:** `2595ee56f70138c58b1924591d32e09cbad31381`  
**Controlling external report:** r60, `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`  
**Controlling proof/pipeline audit:** r60, `e4e72a512bf747e7bd190196cd8dc3db35689e3c`  
**Exact-final-head read-only run:** `37436686847`, conclusion `success`  
**Exact-final-head job:** `112092683893`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v94-spectral-value-external-referee-r61-2026-10-06`  
**Date:** 6 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 94 is a genuine and mathematically substantial advance over the object reviewed in r60. The earlier exact operational hierarchy established that, for a specially designed two-use shared-device ensemble, classical measure-and-reprepare adaptation, unit-reset strategies, and unrestricted adaptive strategies have different exact Bayes values. Revisions 91–93 then introduced the common-barycenter normal form, rank-resolved cuts, fixed initial spectra, equality sets and rigidity. Revision 94 now solves the biased fixed-initial-spectrum optimization itself.

For a fixed pure first acquisition with Gram state `rho`, old and fresh retained dimensions `k,l`, active rank

```text
r = min(k,l),
```

the paper defines a rank-at-most-`r` least majorant `q^(r)(lambda(rho))` and the secular spectral functional

```text
H_r(rho) = chi(q^(r)(lambda(rho))),
```

where, on nonzero coordinates `u_i`, `chi(u)` is the nonnegative solution of

```text
sum_i u_i/(u_i+chi) = 1.
```

With

```text
L_0 = 2(d+1)-t^2,
p_E = (d+1)/L_0,
```

the exact biased value is

```text
P^b_{k,l}(rho)
  = p_E + [t^2/(2L_0)] H_r(rho).
```

The upper is attained by an instrument with at most `d` outcomes, by commuting Gram atoms of a common spectrum, without modifying the prescribed initial acquisition. The fresh state after the receiver outcome uses reference dimension at most `r`; the old retained register also has dimension `r`. The manuscript additionally computes the exact no-message comparison

```text
P^nm_{d,r}(rho)
  = p_E + [t^2/(2L_0)] chi(lambda_1,...,lambda_r)
```

and proves, for `t>0`,

```text
P^b_{d,r}(rho) > P^nm_{d,r}(rho)
  iff 2 <= r < rank(rho).
```

This is a clean, sharp operational statement. It identifies exactly when communicating a receiver outcome to the next fresh preparation has positive value while the initial acquisition is held fixed. It also identifies the initial-rank saturation threshold and treats singular spectra and the endpoints of the deformation.

I have not found a fatal mathematical gap in the new spectral-value section or in the v91–v93 machinery on which it depends. The load-bearing steps are coherent:

1. the fixed initial acquisition is represented by a single pure Gram matrix and is not silently replaced by a classically resolved mixture;
2. the common-barycenter weights are Gram decomposition weights, not hypothesis-dependent branch probabilities;
3. the leaf optimization is reduced to a rank-capped filtered-swap problem and solved by a secular equation;
4. singular support is handled by compression and a pseudoinverse/support restriction rather than by an illegal inverse;
5. the leaf optimizer can be chosen commuting on the leading eigenspaces;
6. the rank-capped concave roof is identified by the least majorizing rank-`r` spectrum;
7. the converse uses Ky Fan inequalities, concavity and majorization in the correct direction;
8. the commuting finite decomposition is supplied by Schur–Horn/Birkhoff-type finite convexity;
9. the same receiver instrument may be used after every first device label;
10. the no-message class is distinguished from complete measure-and-reprepare adaptation;
11. the strict message-gain criterion follows from the strict spectral comparison in the only nontrivial range; and
12. the exact rational executable is correctly limited to supplied spectra and certified bisection intervals.

The four-leading-general-journal conclusion nevertheless remains negative. The exact theorem is proved for a deliberately engineered, finite, two-call shared-basis experiment with a fixed prior, a once-selected latent basis reused at both calls, a fixed pure initial Gram state, and two finite rank cuts. It does not solve arbitrary-pair quantum channel or measurement discrimination, classify finite-memory strategies in general, produce a global metric geometry of the ordered-POVM body, or establish a general law for the value of classical communication in quantum decision problems. The proof's spectral core is an elegant application and synthesis of established majorization, concave-roof, filtered-swap and finite-dimensional convexity methods. In my judgment, the theorem is strong specialist mathematics but does not yet cause the breadth or conceptual displacement expected at the four leading general mathematics journals.

**Disposition outside the four leading general journals:** the focused v90–v94 finite-game development should be seriously considered by a leading specialist journal in mathematical quantum information, quantum statistics, operator theory or mathematical physics after substantial editorial extraction and the priority revisions below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Reviewable object and branch chronology

A complete branch survey finds a numerically later branch,

```text
revision/general-theta-foundations-i-v95-r60-spectral-decision-2026-10-06,
```

but its current head contains only four base64 transport payloads. The concatenated compressed stream is incomplete, the branch has no materialized paper directory, no complete native source, no PDFs, no build receipt, and no GitHub Actions run. The transport metadata itself says that remote assembly is still required and identifies v94 as the latest actual complete publication. I therefore do **not** treat v95 as a submitted manuscript.

The latest complete reviewable object is v94 at exact final head

```text
db6739da3487be8787a67fc175b9086bd62f0e80.
```

The mathematical publication contained in this chain is

```text
0919ff61895716ea3de1d6a0f2a6a291935764d0,
```

whose direct parent is the qualified native source

```text
24f48c90d6bcc1eae1d4c38ac5195405ac21da7d.
```

The publication child adds rendered manuscripts and evidence; it does not alter theorem source. Subsequent commits add the review entry and exact-head verification record. The exact final head was reconstructed read-only by run `37436686847`, job `112092683893`, with credentials persistence disabled and an explicit assertion that the verified head equals the triggering SHA.

The package contains:

```text
focused primary article:       78 pages,
linked binary supplement:      87 pages,
independent structural paper:  41 pages,
complete preservation edition:289 pages.
```

The primary is the journal-facing object. The complete edition is an archive and must not be counted as an additional submission or as evidence of significance.

The build receipt records 870 current source files, 841 predecessor native files, 1088 complete-edition labels, 256 quantitative-package labels, 116 structural labels and 36 regression suites. Inherited mathematical sections are reported byte-identical. This is strong preservation evidence, but it is not a formal proof certificate.

---

## 2. Exact operational interface

The exact theorem is meaningful only with its complete interface visible.

### 2.1 Shared finite family

The unknown device belongs to the finite once-selected basis family introduced in the operational hierarchy. One latent basis index is sampled once and the same device is used at both calls. Redrawing the basis independently at each use would destroy the second-moment signal and would be a different experiment.

The deformation parameter satisfies `0<=t<=1`, the dimension is fixed at `d>=2`, and the prior is the biased prior built into the experiment. The theorem does not optimize the prior.

### 2.2 Fixed pure initial acquisition

The first acquisition is fixed by a pure probe–reference state whose Gram matrix is

```text
rho = C_0^* C_0 in D_d.
```

This is stronger than fixing only the reduced density operator after a classical resolution. The first acquisition may not be replaced by an ensemble of distinct acquisitions selected by a public seed. Such a replacement would change the feasible common-barycenter problem and can change the value.

### 2.3 Two rank cuts

The old receiver memory has effective dimension at most `k`, the fresh reference has effective dimension at most `l`, and only

```text
r=min(k,l)
```

enters the spectral value. The theorem is therefore a two-cut result, not a classification of every memory architecture with dimensions `k,l`.

### 2.4 Receiver message

The biased value permits a receiver outcome to be communicated to the fresh source. The no-message comparator still permits dependence on the first device label and an independent public seed, arbitrary old receiver processing, and a final joint readout. It forbids only the receiver-to-source message. It is not the complete measure-and-reprepare class from v90.

The exact gain theorem is consequently a theorem about one precise communication edge in one finite causal experiment. This precision is a strength and must remain visible in every summary.

---

## 3. Mathematical assessment

### 3.1 The secular functional

For a nonnegative vector `u`, let `v_i=sqrt(u_i)` and consider

```text
v v^* - diag(u).
```

Its largest eigenvalue is `chi(u)`. When at least two coordinates are nonzero, the positive eigenvalue is the unique solution of

```text
sum_i u_i/(u_i+chi)=1.
```

For support size at most one the value is zero. The manuscript proves continuity, symmetry, positive homogeneity, coordinate monotonicity and concavity. On a fixed-trace simplex it establishes the strict Schur-concavity needed for the strict message criterion.

The secular description is exact and numerically stable for the stated finite-dimensional problem. The manuscript should make the support-one convention and the boundary form of strictness especially prominent, because several corollaries use zero padding and rank-deficient spectra.

### 3.2 Leaf optimization

For a positive old Gram operator `A`, the rank-`l` fresh optimization has value

```text
(1/2) chi(a_1,...,a_l),
```

where the selected coordinates are the leading eigenvalues of `A` under the stated convention. The proof compresses to the support, rewrites the rank-capped filtered-swap term, uses a trace/inverse-trace inequality and rearrangement, and rescales to obtain a commuting optimizer.

This avoids a common error: simply pinching an arbitrary optimizer in the eigenbasis of `A` need not preserve the nonlinear objective. The submitted proof does not rely on that invalid step. The singular case is also not obtained by pretending that `A` is invertible; it is treated on its support and by a limiting/pseudoinverse formulation.

I regard this lemma as correct in the submitted finite-dimensional setting. A future version should nonetheless isolate the equality conditions and the zero-eigenvalue approximation in a separate proposition, because those details are load-bearing for the global attainment statement.

### 3.3 Rank-capped least majorant

For the decreasing eigenvalue vector `lambda`, the paper constructs the least rank-at-most-`r` majorant

```text
q^(r)(lambda)
```

by retaining the large coordinates and water-filling the remaining mass over the remaining active positions. The construction allows rank strictly below `r` through zero tails.

The majorization direction is the correct one for the concave spectral roof. Every rank-`r` barycentric decomposition is bounded by the spectral value at this least majorant, while a commuting finite ensemble with common spectrum `q^(r)` attains the bound. The finite converse is obtained from Schur–Horn and finite doubly stochastic decompositions rather than from an unproved measurable-selection assertion.

This is standard majorization technology used effectively. The application-specific content is the identification of this roof as the exact operational value and the simultaneous realization within the reset normal form.

### 3.4 Concave roof

For a continuous symmetric concave homogeneous spectral function `f`, the rank-capped concave envelope over positive Gram atoms is

```text
f(q^(r)(lambda(rho))).
```

The upper uses Ky Fan inequalities and Jensen. The lower uses commuting atoms of common spectrum and a finite convex decomposition of `rho`. Taking `f=chi` yields `H_r`.

The proof correctly distinguishes trace weights in a Gram decomposition from probabilities of histories under either hypothesis. This distinction should be repeated immediately before the main theorem; otherwise readers may incorrectly normalize branch operators using hypothesis-dependent record probabilities.

### 3.5 Exact prescribed-spectrum value

The upper applies the dimension-preserving normal form from the earlier rank hierarchy. For each first device label, the receiver branches decompose the same fixed Gram state:

```text
sum_h A_{y,h}=rho.
```

Applying the leaf bound branchwise and then the spectral roof gives the exact upper. The commuting roof decomposition supplies an instrument with at most `d` outcomes. The fresh leaf optimizer supplies the matching preparation and final positive-part decision. The construction preserves the initial acquisition and requires no extra retained environment.

This is a real theorem, not a numerical conjecture or a comparison of two exhibited protocols. It solves the complete stated class `R_{k,l}`.

### 3.6 Exact message value

Without a receiver message, old processing can be postponed to the final readout and every first-label branch retains the Gram state `rho`. The leaf lemma therefore gives

```text
P^nm_{d,r}(rho)
 = p_E + [t^2/(2L_0)] chi(lambda_1,...,lambda_r).
```

The message-enabled value replaces the truncated spectrum by the rank-capped majorant roof. At `r=1`, both secular values vanish. At `r>=rank(rho)`, no tail is moved and the values agree. In the intermediate range `2<=r<rank(rho)`, strict Schur-concavity yields strict gain for `t>0`.

The iff statement is sharp and is one of the strongest parts of the revision. It should be stated next to the main value theorem in the introduction rather than being separated by several layers of historical material.

### 3.7 Example and boundary checks

The three-dimensional example with

```text
lambda=(1/2,1/4,1/4), r=2
```

gives

```text
q^(2)=(3/4,1/4,0),
chi(q^(2))=sqrt(3)/4,
chi(lambda_1,lambda_2)=sqrt(6)/8,
```

and hence a strictly positive exact communication gain for `t>0`. This example should move into the main exposition. It makes clear that the gain is neither an artifact of rank deficiency nor a statement about globally optimizing the initial Gram.

### 3.8 Countable outcomes and finite attainment

The theorem permits the general receiver class inherited from the normal form, while the optimizer has at most `d` outcomes. The upper only needs positive trace-class sums and finite-dimensional compactness. The final paper should state in one place how countable instruments are reduced by monotone finite truncation/upper semicontinuity or directly covered by the normal-form lemma. I see no fatal gap, but the current presentation makes this reduction more implicit than is desirable for a top-level submission.

---

## 4. Relation to the v90–v94 proof pipeline

The exact finite-game line now has a coherent progression:

```text
v90: exact three-class two-call operational hierarchy;
  -> v91: common-barycenter variational principle and attained dual;
  -> v92: rank-preserving normal form and two independent cuts;
  -> v93: fixed initial spectra, three-cut equality and rigidity;
  -> v94: exact biased value for every prescribed pure initial spectrum,
          exact message gain, and rank saturation.
```

Revision 94 positively answers the central mathematical request left by r60: it moves beyond an equality set and rigidity estimate to the exact value function on the entire prescribed-spectrum domain.

This finite-game line is logically distinct from the older local tangent-tube line:

```text
coupled covariance
 -> support kernel
 -> finite orbit and smooth-curve laws
 -> one-sided tangent tubes
 -> entanglement/reset width
 -> allocation profiles and hard quadratic budgets.
```

The latter remains active and correctly preserved, but it is not needed to prove the spectral roof theorem. The primary manuscript currently combines both lines in seventy-eight pages and then links a large supplement and a complete archival edition. That architecture obscures the new theorem. For specialist publication, the v90–v94 finite-game chain should be extracted as a standalone paper, with the local geometry summarized only as contextual work.

The wider repository A/B/C/D programme remains logically independent. Raw local limits, stopped-path recovery, grand-canonical/microcanonical transfer, Mosco recovery, nonlinear resolvent/core results, filtering/QMD/LAN, changing-filtration response and labelled posterior contraction are not consequences of the finite spectral value theorem. All five aggregate closure flags correctly remain false.

---

## 5. Novelty and literature position

The current literature audit is materially better than the one available at r60. It recognizes the following distinct antecedent layers:

1. pure-state majorization and finite ensemble transformations, including Nielsen and Jonathan–Plenio;
2. Schur–Horn, doubly stochastic decompositions and concave spectral roofs;
3. entanglement-of-assistance and related assisted convex/concave roofs;
4. filtered-swap and antisymmetric tests;
5. constrained-memory quantum channel discrimination, including Ohst–Zhang–Nguyen–Plávala–Quintino;
6. recent bounded coherent-memory and multi-time process discrimination, including Zonnios–Binder; and
7. the earlier Bures, reset-width and channel-metrology antecedents already discussed in the manuscript.

I do not see in these sources the exact submitted formula for the once-selected finite measurement family, its least-majorant secular roof, or the sharp message criterion at fixed initial Gram. But the underlying mathematical mechanism is close to classical majorization/assistance technology, and the memory-resource question has an active recent literature. An author-side audit cannot settle priority. A written assessment by an independent specialist familiar with both quantum combs and majorization roofs is still required before any strong firstness claim.

The paper should avoid claiming that it classifies the value of communication or quantum memory in general. Its defensible novelty is narrower and still significant:

- an exact rank-resolved operational value for the specific finite shared-device game;
- a singular-safe leaf optimization;
- an explicit rank-capped spectral roof;
- a finite attained normal form preserving a prescribed pure acquisition; and
- an iff criterion for receiver-to-source communication gain within that interface.

---

## 6. Computation and finite evidence

`spectral_value.py` accepts a supplied rational spectrum, dimensions `k,l`, deformation `t` and a bisection bit count. It:

- rejects floats, booleans, illegal spectra and illegal dimensions;
- constructs the rational water-filled majorant exactly;
- brackets the secular root by rational bisection;
- returns score and gain intervals;
- implements the same strict-gain criterion as the theorem; and
- explicitly states that the spectrum is supplied rather than measured.

It does not reconstruct an unknown device, find an eigenbasis, certify physical reset independence, synthesize the receiver instrument, prove the continuum theorem, or establish priority. These limitations are correctly machine-readable.

The executable is useful reproducibility evidence. The manuscript should state arithmetic-operation and bit-length growth separately. A bisection count of `B` gives an interval width controlled by `2^{-B}` only after the normalization and initial bracket are fixed; the size of rational numerators and denominators grows with `B`. Calling the procedure “efficient” without this qualification would be misleading.

The build receipt reports 36 regression suites, ordinary/optimized identity, isolated native rebuild, standalone journal reconstruction and no unresolved references or citations. This supports source integrity and catches implementation regressions. It does not prove the majorization theorem or the physical operational model.

---

## 7. Provenance assessment

The release chain is substantially cleaner than the v88 object reviewed previously.

- `24f48c...` is the qualified native source.
- `0919ff...` is the artifact publication.
- `db6739...` is the current exact final head containing review metadata and the exact-head receipt.
- Run `37436686847` checked out `db6739...` without persisted write credentials and reconstructed the published package read-only.

The paper must keep these identities distinct. The successful exact-final-head run is attached to the final branch head, not directly to the artifact publication SHA. It verifies the final head and the publication object referenced from it; it should not be described as a workflow whose triggering SHA was `0919ff...`.

The native and publication commits are unsigned. Git object identity, checksums, read-only reconstruction and Actions logs establish reproducibility and provenance of bytes, not verified human authorship or independent mathematical certification.

The numerically later v95 transport branch must not be listed as a completed revision until its payload has been fully materialized, source-qualified, built and exact-head verified. A branch number is not a publication state.

---

## 8. Required revisions before specialist submission

### R1 — Extract the finite-game paper

Create a standalone journal object centered on v90–v94: the shared finite family, operational hierarchy, common-barycenter normal form, rank cuts, fixed spectra, exact value and communication gain. Do not require a reader to traverse the full historical geometry corpus.

### R2 — Put the complete interface on page one

State the fixed prior, once-selected latent basis, two calls, fixed pure initial Gram, rank cuts, permitted receiver message, final joint readout and no-message comparator before displaying the theorem.

### R3 — State the two exact values together

Place `P^b_{k,l}(rho)` and `P^nm_{d,r}(rho)` together, followed immediately by the iff gain criterion and saturation cases.

### R4 — Explain why the initial Gram cannot be classically resolved

Give an explicit one-paragraph warning that an ensemble decomposition of `rho` used to select distinct first acquisitions changes the experiment and is not allowed.

### R5 — Expand the singular leaf proof

Isolate support compression, pseudoinverse convention, commuting optimizer and equality conditions. Avoid relying on a reader to reconstruct these from several inherited lemmas.

### R6 — Expand the roof proof

State the majorization direction, least-majorant property, Ky Fan/Jensen upper and finite commuting Schur–Horn/Birkhoff attainment in one self-contained theorem.

### R7 — Close the countable-outcome presentation

State explicitly why the general instrument class is covered and why finite `d`-outcome attainment loses no value.

### R8 — Sharpen strictness at the boundary

Separate `r=1`, `2<=r<rank(rho)`, `r>=rank(rho)`, support-one spectra, zero padding and `t=0`. State the exact boundary version of strict Schur-concavity used.

### R9 — Move the `d=3` gain example into the main text

Use it to distinguish fixed-initial-Gram message gain from global optimization over the initial acquisition.

### R10 — Add theorem-level literature comparison

Compare exact assumptions and conclusions with majorization transformations, assisted roofs, constrained-memory channel discrimination and recent bounded-memory process discrimination. Do not rely on broad thematic citations.

### R11 — Obtain independent specialist priority review

Repository chronology, targeted search and successful finite tests are not a priority opinion.

### R12 — State computational complexity honestly

Separate exact rational correctness, arithmetic-operation count, bit-length growth, physical design synthesis and unknown-spectrum estimation.

### R13 — Keep provenance identities distinct

Identify native source, publication object and exact final head separately in every release document.

### R14 — Resolve or retire the incomplete v95 transport branch

Materialize and qualify it, or mark it unambiguously as an incomplete transport. It must not displace v94 in “latest completed manuscript” statements.

### R15 — Separate the wider Theta programme

Do not use the complete edition, structural companion or unrelated A/B/C/D programme as a significance multiplier for the spectral theorem.

---

## 9. Detailed comments

### D1 — Meaning of `rank-r`

Use “rank at most `r`” consistently. The water-filled majorant may have smaller rank when zero tails occur.

### D2 — Ordering of eigenvalues

State once that `lambda_1>=...>=lambda_d>=0` and keep that convention in the executable documentation and examples.

### D3 — Definition of `chi`

Give both the matrix definition and the secular equation, including the support-size-one convention.

### D4 — Homogeneity

Specify whether homogeneity is used on subnormalized positive Gram operators before the trace-one spectral roof.

### D5 — Strict Schur-concavity

State precisely the domain on which strictness holds modulo permutations and zero padding.

### D6 — Water-filling index

Give the unique stopping-index characterization and explain the equality case at a plateau.

### D7 — Gram weights

Do not call `tr A_{y,h}` branch probabilities without qualification. They are common Gram weights in the barycenter identity.

### D8 — Null branches

State that zero-weight atoms are omitted and that all formulas extend continuously to singular endpoints.

### D9 — Same instrument after every label

Highlight this stronger attainment feature in the theorem statement, not only in the proof audit.

### D10 — Fresh-state dependence

The message-gain construction does not require first-device-label dependence of the fresh state. This is conceptually useful and deserves a sentence in the introduction.

### D11 — No-message class

Repeat that the no-message class still permits dependence on the first device label and public randomness. Otherwise readers may confuse it with v90 classical adaptation.

### D12 — Globally optimized acquisition

Explain why the no-feedback global attainments from v93 are compatible with positive fixed-Gram message gain in v94.

### D13 — Endpoints in `t`

State separately what remains at `t=0` and how the formulas extend to `t=1`.

### D14 — Dimension cuts

The value depends on `min(k,l)`, but the physical interpretations of old and fresh cuts differ. Do not describe them as interchangeable resources beyond this game.

### D15 — Attainment cardinality

Give the precise finite-convexity reason for the `d`-outcome bound and whether `d` is sharp.

### D16 — Eigenbasis knowledge

The mathematical optimizer may use an eigenbasis of a supplied `rho`. This does not imply an efficient unknown-state or unknown-device procedure.

### D17 — Exact bisection

The executable brackets the value; except for special algebraic inputs it does not return a closed-form root. Use “certified interval” rather than “exact decimal value.”

### D18 — Build evidence

Keep regression counts out of mathematical theorem statements. They belong in reproducibility material.

### D19 — Historical labels

The active source sequence is long. A focused paper should renumber its theorems rather than exposing historical section numbers 82–87.

### D20 — Editorial claim

“General Theta Foundations” is much broader than the submitted finite-game theorem. The specialist article title should describe the exact operational and spectral content.

---

## 10. Final disposition

The new theorem is mathematically serious. It gives an exact prescribed-spectrum value, a finite attained optimizer, a sharp rank threshold and a precise operational value for a receiver-to-source message. It closes the main mathematical question left by the v90–v93 sequence, and I found no fatal gap in the proof architecture inspected.

It does not, however, classify general memory-constrained quantum discrimination, establish global ordered-measurement geometry, or replace the standard majorization and concave-roof frameworks on which its spectral argument rests. The manuscript is also burdened by a very large historical package whose breadth is not the same as conceptual breadth of the new theorem.

My recommendation at the four leading general mathematics journals is therefore **reject**, explicitly on significance, scope and editorial-focus grounds rather than on correctness. A substantially extracted v90–v94 article would be a strong specialist-journal submission after the revisions above.

This report is an author-requested, repository-pinned external assessment. It is not a commissioned journal decision, a formal proof-assistant certificate, a verified human-priority opinion or an endorsement of the wider Theta programme.
