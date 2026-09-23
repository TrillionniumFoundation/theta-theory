# Independent harsh top-four referee report — A2 revision 131

**Manuscript:** *Universal determinant completion, effective Pieri multiplication, and intrinsic primary boundary laws in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** `revision/a2-v131-relative-primary-filtrations-2026-09-23`  
**Reviewed head:** `1b3a82d09970ad6545c750733c80ff728a347cd4`  
**Principal referee-facing source:** `papers/A2-v17-boundary-information-coarsening/article/v131/geometry.tex`  
**Controlling previous report:** `reviews/a2-v130-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`  
**Previous review commit:** `57c70a882150cc6e44d85ad6f68043b7327d8a10`  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I read the complete v131 referee-facing source architecture, the response to the v130 report, the new relative-primary-filtration section, the new sharp-global-law section, the universal graded corollary, the inherited corank-two/corank-three/corank-four theorem chain, the exact-check scripts at the level recorded by the build receipt, the provenance files, and the final abstract/introduction. I also checked the precise logical role of the Stacks Project descent/relative-assassin statements invoked in the new family argument and the Bruns--Vasconcelos maximal-minor identity used in the quotient-induced family.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation should not obscure how much stronger revision 131 is than revision 130.

The two main local algebra objections in my previous report have been addressed in substance. The manuscript no longer tries to extract exact associated-point packets from open-containment constructibility. Instead it constructs actual primary quotients on a finite splitting cover, filters those quotients by modules that inject into free modules over the tracked prime quotient, and uses a diagonal injection to exclude untracked associated primes. Likewise, the embedded-multiplicity argument now introduces an actual coherent torsion module \(T\), passes to \(Q=M/T\), chooses a regular element \(h\in\mathfrak p\) on \(Q\), and uses preservation of the \(h\)-injection to exclude new \(\mathfrak p\)-power torsion after base change. These are the right mechanisms.

The graded universal corollary is also much cleaner. It now states the grading, names the finite family of multiplication maps, and separates the graded Hilbert-function conclusion from the ungraded flattening theorem. The corank-four Pieri nonvanishing is now audit-ready at the numerical level: the old coefficient-one straightening claim has been replaced by a Fischer projection with coefficient \(1/35\). The new global exponent-five theorem, the two global minimal supports, the incidence resolution, and the explicit \(2\to3\to4\) corank family are genuine mathematical additions. In particular, I no longer repeat the v130 criticism that the paper contains no actual cross-corank geometry.

However, the central relative theorem is still not fully proved in the form in which it is stated on the original base. The construction of primary quotients and exact associated-point exhaustion is carried out on a finite faithfully flat splitting cover. The subsequent passage back to closed packets on the original stratum is compressed into the sentence that “their finite images descend the packets.” That is not an fpqc descent proof. Effective fpqc descent requires an explicit descent datum (or an equivalent invariant-ideal construction), and scheme-theoretic image under a finite cover is not by itself a substitute for proving that the descended closed subscheme has exactly the asserted geometric fibre components and behaves correctly under the later flattening and incidence refinements.

This is a narrower and more sophisticated issue than E130.1, but it sits exactly under the abstract-level “finite-presentation families” theorem. Until the packet descent is written rigorously, I do not regard the universal primary-stratification theorem as proved at top-four archival standard.

Even after that repair, the significance question remains. Revision 131 now supplies a genuinely attractive global picture for the first two nilpotent layers, but it explicitly does not classify the embedded primary geometry of \(W_3\) and \(W_4\). The seven-component family is a decomposition of the pulled-back **incidence resolution**, not a transverse primary decomposition of the failure scheme. The quotient-induced symmetric-power family is useful and exact, but its main determinantal identity is classical and much of the resulting primary/colon algebra is a controlled regular-local consequence. The inverse theorem still reconstructs the polarized K3 but not the original web or the finite Torelli packet.

For a strong specialist journal, I now think the manuscript has a much clearer mathematical core. For a general top-four journal, I would require one more proof-closure step and one more genuinely decisive structural theorem.

# 1. What revision 131 genuinely fixes

A referee should not continue charging the manuscript with objections that have actually been repaired.

## 1.1 E130.1 is repaired on the splitting cover

Proposition `prop:relative-primary-models` is a real improvement over the v130 packet argument.

On the geometric generic fibre the manuscript chooses an irredundant primary decomposition
\[
0=\bigcap_i N_i,\qquad Q_i=M/N_i,\qquad \operatorname{Ass}Q_i=\{\mathfrak p_i\},
\]
together with associated-element injections
\[
A/\mathfrak p_i\hookrightarrow M
\]
and the diagonal injection
\[
M\hookrightarrow\bigoplus_iQ_i.
\]

The key point is that the assertion “\(Q_i\) is primary” is then spread by a finite exact diagram. The filtration
\[
F_{i,j}=(0:_{Q_i}\mathfrak p_i^j),\qquad
E_{i,j}=F_{i,j}/F_{i,j-1}
\]
has quotients killed by \(\mathfrak p_i\) and torsion-free over \(A/\mathfrak p_i\). After finite extension and shrinking, the \(E_{i,j}\) embed in finite free modules over the integral prime quotient on every geometric fibre.

This gives the two associated-point inclusions for a fibre:
\[
\operatorname{Ass}M_{\bar s}
\subset
\bigcup_i\operatorname{Ass}Q_{i,\bar s}
\subset
\{\mathfrak p_{i,\bar s}\},
\]
while the associated-element injections give the reverse inclusion.

That is the missing exhaustion mechanism from v130. An extra embedded point cannot hide inside an “adapted open”: it would contradict the diagonal injection into modules whose associated sets have already been controlled.

I therefore regard the old local reverse-inclusion objection as closed **after passage to the splitting cover**.

## 1.2 E130.2 is repaired in substance

Proposition `prop:no-new-packet-torsion` introduces the right relative object.

On the split generic fibre it chooses
\[
T=(0:_M\mathfrak p^n)=H^0_{\mathfrak p}(M),\qquad Q=M/T.
\]
Since \(Q\) has no \(\mathfrak p\)-power torsion, no associated prime of \(Q\) contains \(\mathfrak p\). Prime avoidance therefore gives
\[
h\in\mathfrak p
\]
outside all associated primes of \(Q\), so multiplication by \(h\) is injective on \(Q\).

The proof then spreads
\[
0\to T\to M\to Q\to0,
\qquad \mathfrak p^nT=0,
\qquad h:Q\to Q,
\]
and flattens the appropriate cokernels so that the injections survive arbitrary base change on the chosen stratum.

This is the decisive point. If a new \(\mathfrak p\)-power torsion element appeared in a fibre of \(M\), its image in \(Q\) would be killed by a power of \(h\), contradicting injectivity. Thus the spread-out \(T\) is not merely a generic torsion submodule; it equals the entire fibrewise \(\mathfrak p\)-power torsion.

The finite filtration
\[
T\supset\mathfrak pT\supset\cdots\supset\mathfrak p^nT=0
\]
then computes the local length from the ranks of the graded quotients at the packet generic point.

This is the construction I requested in E130.2. Subject to the descent issue in Section 2 below, I regard the local torsion argument as closed.

## 1.3 M130.1 is closed

The universal corollary now fixes the grading:
\[
A=\mathcal O_{\mathcal U}[t_{ij}],
\qquad \deg t_{ij}=1,\quad
\deg\mathcal O_{\mathcal U}=0,
\]
and defines
\[
M_q=A/(d,K_q),\qquad
L_j=M_{j-1}(-ej).
\]

It names the finite multiplication family
\[
\mu_{i,j}:L_i\otimes_A L_j\longrightarrow L_{i+j},
\qquad i+j\le N,
\]
rather than speaking about an unspecified collection of ranks.

The graded-flat lemma correctly separates the additional Hilbert-function conclusion from the ungraded theorem. This fixes the formulation problem from v130.

## 1.4 The Pieri coefficient is now properly normalized

The Fischer-form argument computes
\[
\operatorname{pr}_{(4,4,4,4)}
\left([123|123]^4x_{44}^4\right)
=\frac1{35}(\det X)^4.
\]

This is substantially better than the previous coefficient-one straightening sentence. The manuscript now distinguishes:

- nonzero isotypic projection;
- the normalization of that projection;
- right-\(GL(V)\) stability of the maximal-minor ideal;
- semisimple projection inside the ideal.

I regard the corank-four \(d^4\in J\) mechanism as closed.

## 1.5 The global exponent-five theorem is a real advance

Revision 131 uses the full-matrix identity to show that, for every \(R\in G_4^\circ\),
\[
d^4\in J
\]
on every Schur chart. Together with the inherited pointwise exclusions \(d^3\notin J\) at projection coranks three and four, this gives exact local nilpotency index five there.

I checked the quantifiers in the inherited corank-three/corank-four statements. The manuscript is not silently promoting a generic calculation to an everywhere statement on \(G_4^\circ\). The corank-three exclusion is formulated pointwise, and the corank-four argument uses the nonzero Jacobian covariant for every \(R\in G_4^\circ\).

The v130 five-or-six ambiguity on the smooth Jacobian open is therefore genuinely removed.

## 1.6 The paper now contains actual cross-corank geometry

The theorem identifying
\[
\sqrt{(d,J)}=I(Z_R),
\qquad
\sqrt{(d,J:d)}=I(D_2)
\]
is conceptually useful. The incidence space
\[
\widetilde Z_R=\operatorname{Tot}\operatorname{Hom}(V,\mathcal H)
\]
over the quartic K3 has the correct dimension, is smooth, and maps properly and birationally to its image.

The fibre description
\[
\pi^{-1}(T)
=
Y_R\cap\mathbf P((V/\operatorname{im}T)^*)
\]
gives four points, a genus-three plane quartic, and the K3 surface in successive ranks.

The explicit family
\[
M(u,v)=\operatorname{diag}(u,v,0,0)
\]
then produces
\[
V(u\alpha_1,v\alpha_2)
\]
with seven reduced components.

This directly addresses the v130 request for a concrete \(2\rightsquigarrow3\rightsquigarrow4\) geometric specialization. I no longer list “no cross-corank family” as an open objection.

# 2. Decisive proof-completeness issue E131.1 — the packet descent from the splitting cover is not proved

The main remaining correctness issue is now concentrated in a single passage of Lemma `lem:finite-geometric-assassin-stratification`.

The local primary model is constructed after a finite faithfully flat cover of a dense open. On that cover there are actual ideals \(\mathfrak p_i\), actual primary quotients \(Q_i\), the diagonal injection, and the associated-element injections. So far, the proof is concrete.

The lemma then says:

> Take the closures of the tracked generic points and group geometric conjugates into packets. A finite extension suffices to define all these closed subschemes and the finite diagrams. Their finite images descend the packets to the original base; after removing the images of the finitely many bad closed subsets, no further component of a packet fibre appears.

This is the point at which the proof again becomes too compressed.

## 2.1 Why “finite image” is not the same thing as fpqc descent

An effective fpqc descent theorem says that a quasi-coherent ideal/sheaf equipped with a compatible descent datum descends. One must provide, explicitly or implicitly, an isomorphism between the two pullbacks to the double overlap satisfying the cocycle condition.

The manuscript does not construct that datum for the labelled prime closures or for the Galois packet union.

Nor does it replace the missing datum with an explicit invariant ideal, for example by:

1. passing to a finite Galois splitting extension;
2. taking the reduced union of the full Galois orbit of a prime closure;
3. proving that this union carries the natural Galois descent datum;
4. descending its ideal by fpqc descent;
5. proving that the descended fibre, after geometric base change, is exactly the union of the intended conjugate components.

Instead the proof invokes “finite images.”

A scheme-theoretic image under a finite map is certainly closed, but the manuscript needs much more:

- exact control of its geometric irreducible components;
- compatibility with later base change;
- compatibility with the packet flatness refinement;
- compatibility with intersections used to define incidence;
- and preservation of the exact relationship between packet generic points and \(\operatorname{Ass}(M_{\bar s})\).

These conclusions do not follow merely from the existence of a finite image.

## 2.2 Tag 0GSJ does not fill this descent step

The alternative sentence invoking the flat relative-assassin closure lemma is useful but addresses a different issue.

The closure theorem guarantees that generic points of irreducible components of the fibre of a tracked relative-associated-point closure remain associated points under the flatness hypotheses. This is a persistence statement.

It does not:

- produce a descended closed packet from a prime closure defined only after a splitting extension;
- supply the missing descent datum;
- prove that a scheme-theoretic image of the split packet has no unintended geometric components;
- or prove that the full packet equality is compatible with arbitrary base change on the original stratum.

The manuscript has already solved exhaustion **upstairs** by the diagonal injection. The remaining task is to descend the geometric object that is supposed to encode that equality.

## 2.3 Why this is not cosmetic

The abstract states a theorem for finite-presentation families, not merely for families after an unspecified finite cover. The universal corollary similarly claims a finite stratification of the original surjection parameter space \(\mathcal U\).

Clause (2) of Theorem `thm:bounded-principal-colon-stratification` asserts closed relative support packets
\[
Z_{q,\nu}\subset\operatorname{Spec}A_{S_\alpha}
\]
on the original stratum.

Clause (3) attaches the canonical local torsion length to those packets.

The current proof establishes these statements in a labelled form on a splitting cover, then sketches the descent.

For a headline relative theorem, that sketch is not enough.

## 2.4 A clean repair

Because the applications in this paper are over \(\mathbf C\), the shortest repair is probably to work in characteristic zero and make the finite splitting extension Galois after replacing it by its Galois closure.

For each orbit of labelled generic primes:

1. take the reduced union \(Z'\) of the full Galois orbit of the corresponding closures upstairs;
2. show that the Galois action gives an actual descent datum on the ideal sheaf \(\mathcal I_{Z'}\);
3. descend \(\mathcal I_{Z'}\) by fpqc descent;
4. shrink so that the descended packet and its geometric pullback have exactly the required irreducible components;
5. perform the flatness and intersection refinements on these descended ideals;
6. then use faithful flatness to transport the associated-point equality from the splitting cover.

If the authors want the theorem over an arbitrary noetherian base, the same step should be written in fpqc language without relying on Galois terminology.

A second acceptable option is to weaken the theorem and state the primary-packet conclusion only after finite faithfully flat splitting covers. That would be mathematically clean but would reduce the strength of the universal headline.

Until one of these is done, I regard the family theorem as incomplete at the exact point where it returns from the split algebra to the original parameter space.

# 3. The local primary proof should be preserved — do not regress to constructibility

The repair to E131.1 should not discard the strongest part of v131.

The diagonal injection
\[
M\hookrightarrow\bigoplus_iQ_i
\]
is the right way to prove the **absence** of untracked associated primes.

The associated-element injections
\[
A/\mathfrak p_i\hookrightarrow M
\]
are the right way to prove the **presence** of every tracked prime.

The regular element
\[
h:M/T\to M/T
\]
is the right way to prove no new packet torsion appears.

A revision should keep these mechanisms and add the descent step after them. Replacing them again by a constructible-open argument would be a regression.

# 4. Structural issue S131.1 — the new incidence resolution is not a full higher-corank primary atlas

Revision 131 makes serious progress on the v130 higher-corank objection, but the distinction made in the manuscript itself remains decisive.

The new global theorem identifies the **minimal supports of the first two layers**:
\[
Z_R,\qquad D_2.
\]

The cross-corank family computes the primary decomposition of the pulled-back incidence scheme
\[
(u\alpha_1,v\alpha_2).
\]

The manuscript explicitly and correctly warns:

> the primary decomposition ... is the primary decomposition of the incidence-resolution family, not a claim that all transverse primary components of \(W_3\) and \(W_4\) have been classified.

That caveat is mathematically important.

The higher layers are exactly where the deeper nilpotent structure lives. Revision 131 still does not give, at generic corank-three and corank-four points:

- the complete associated-prime set of \(W_3\) and \(W_4\);
- the embedded primary components;
- their generic multiplicities;
- their geometric support varieties;
- or a representation-theoretic mechanism predicting them.

The residue-field algebra
\[
\kappa[\epsilon]/(\epsilon^5)
\]
records the local nilpotency length along the selected family. It does not encode the transverse support geometry of the higher residual layers.

Thus the paper now has:

- a detailed corank-two primary atlas;
- global first/second-layer minimal supports;
- exact higher-corank determinant depth;
- a cross-corank incidence resolution.

That is much stronger than v130. It is still not a full higher-corank primary boundary atlas.

For top-four significance, the most compelling next result would be to identify at least the generic \(W_3\) and \(W_4\) primary supports at coranks three and four and relate them to the incidence geometry already constructed.

# 5. Structural issue S131.2 — the quotient-induced family is exact but not the missing top-four theorem by itself

Theorem `thm:quotient-induced-primary-law` is a useful exact control family.

For
\[
\gamma=\operatorname{Sym}^r\rho,\qquad
\rho:V\twoheadrightarrow W,
\]
the manuscript obtains
\[
J=P^a,\qquad
(J:d^q)=P^{\max(a-q,0)},\qquad
dJ=(d)\cap P^{a+1},
\]
together with the exact nilpotency exponent and binomial local-length formulas.

I find the formulas internally coherent, and the manuscript correctly credits the maximal-minor identity
\[
I(\operatorname{Sym}^r\phi)=I(\phi)^a
\]
to Bruns--Vasconcelos.

This theorem is valuable as a benchmark because it shows that the universal determinant-completion framework can collapse to a completely explicit primary law on a nontrivial infinite family.

But its conceptual ingredients are substantially classical:

- the maximal-minor symmetric-power identity is classical;
- powers of the generic maximal-minor prime are a standard determinantal phenomenon;
- after localization at \(P\), the determinant is a regular parameter;
- the colon formula and binomial lengths are then regular-local calculations.

Accordingly I would not use this theorem, by itself, as the principal answer to the top-four significance question.

The strongest new content of the paper remains the interaction between the failure scheme, the K3 geometry, the intrinsic nilpotent filtration, and the boundary. The next revision should deepen that interaction rather than add more exactly solvable determinantal subfamilies unless those subfamilies reveal a genuinely new general pattern.

# 6. Structural issue S131.3 — the inverse theorem is still one step short of the natural endpoint

The polarized reconstruction theorem remains one of the strongest conceptual results in the manuscript:
\[
\widehat D_R
\quad\Longrightarrow\quad
(Y_R,\mathcal O_{Y_R}(1)).
\]

Revision 131 appropriately does not claim that the K3 recovers the original relation web.

The unresolved question remains:

- does the deeper nilpotent packet determine the original web?
- if not, what is the exact finite degree of the web-to-K3 map?
- do the new higher layers reduce the finite Torelli ambiguity?
- can one recover the Reye/Enriques datum from the full nonreduced failure scheme?

At present the answer is still not supplied.

This is not a correctness defect, because the manuscript is explicit about the limitation. It is a significance issue. A theorem showing that the new nilpotent layers actually distinguish some or all of the finite K3 ambiguity would connect the enormous boundary calculation directly to the inverse problem and would materially strengthen the case for a general top-four journal.

# 7. Major literature/priority issue M131.1 — the Ballico comparison is still open

The manuscript is commendably careful here.

The issue matrix and response explicitly say that a full-text theorem-by-theorem comparison with Ballico (1993) has not been completed, and the introduction avoids a theorem-level nonanticipation claim.

That is the right scholarly stance.

For an eventual top-four submission, however, this cannot remain a permanent documentary exception. A directly relevant historical paper has to be read in full and compared theorem by theorem against:

- the failure-locus/Fitting construction;
- the nilpotent structure;
- the residual boundary layers;
- and any reconstruction statement that might overlap with classical higher-order failure geometry.

I do not treat this as a mathematical correctness blocker. I do treat it as an unresolved novelty-boundary requirement.

# 8. Minor but real consistency issue M131.2 — stale v128/v130 language remains in the final source

The self-contained source is mechanically clean, but not every inherited sentence has been updated to the new theorem hierarchy.

For example, `parts/09a-rees-specialization.tex` still says that projection corank three has an “exact index-five/index-six dichotomy” from the corank-three theorem.

In v131 the theorem now says that on \(G_4^\circ\)
\[
d^3\notin J,\qquad d^4\in J,
\]
so the index is exactly five there; the binary alternative only survives for more general coefficient data outside the smooth-web open.

The same inherited section still speaks of “the point of Revision 128,” although the referee-facing article is Revision 131.

These are not serious mathematical errors, but a top-four submission should have a single current theorem hierarchy. The final pass should remove historical-version prose from the article proper and leave that history in response/provenance files.

# 9. The first two global supports are persuasive, but the proof should be stated with its exact scope

I find the main geometric argument for
\[
\sqrt{(d,J)}=I(Z_R)
\]
convincing at the stated set-theoretic/radical level.

At rank three, the failure condition is exactly the Jacobian-hyperplane condition. At rank at most two, the projective family of containing hyperplanes necessarily meets the quartic, so those matrices lie in the incidence image. Invertible matrices are excluded.

The local rank-three calculation
\[
J_{\mathrm{loc}}=(t,h)
\]
also explains the generic reducedness of the first layer.

Likewise, the degree argument showing that \(J:d\) is nonunit at every corank-at-least-two transverse origin gives the correct support \(D_2\), and the simple-contact calculation supplies generic length one on a dense open.

I therefore do not raise a correctness objection to the stated **minimal-support** theorem.

The paper should, however, continue to emphasize the word “minimal.” The theorem does not rule out higher embedded associated primes, and the later cross-corank family does not change that fact.

# 10. Computational evidence and source discipline are now strong

The v131 build receipt is one of the better parts of the package.

It records:

- a 63-page compiled PDF;
- no undefined references or citations;
- no LaTeX errors;
- local TeX inputs only;
- source hashes;
- no duplicate labels;
- exact execution of the inherited and new scripts;
- and a clear separation between finite symbolic checks and structural mathematics.

In particular, the receipt correctly lists as **not machine certified**:

- primary-quotient spreading and packet exhaustion;
- no-new-torsion/local-length arguments;
- global sharp depth/minimal-support arguments;
- incidence-resolution geometry;
- the general quotient-induced symbolic-power/colon theorem.

This is exactly the right epistemic boundary. A green build should never be presented as certification of the structural proofs.

I have no objection to the manuscript’s use of exact symbolic computation in its current form.

# 11. Status of the revision-130 issues after revision 131

## E130.1 — exact geometric-assassin packet exhaustion

**Substantially closed upstairs; narrowed to E131.1 downstairs.**

The diagonal-primary-quotient construction solves the old exhaustion problem on a finite splitting cover.

The remaining issue is rigorous descent of the packet subschemes and their fibre geometry to the original stratum.

## E130.2 — relative embedded multiplicity

**Closed in substance.**

The coherent torsion module and regular-element argument supply the missing relative mechanism.

Again, the final packet-labelled statement on the original base inherits the descent issue E131.1.

## M130.1 — graded universal corollary

**Closed.**

The grading and finite multiplication family are now stated explicitly.

## Pieri auditability

**Closed.**

The Fischer coefficient \(1/35\) is explicit and the ideal-stability/projection logic is clean.

## S130 global consequence

**Materially advanced.**

The sharp global exponent five, global first/second-layer minimal supports, incidence resolution, cross-corank family, and quotient-induced exact family are genuine additions.

I no longer characterize the global part as only formal flattening.

## S130 higher-corank primary atlas

**Partially closed, still open at the embedded level.**

The first two minimal supports and exact depth are known. The full \(W_3/W_4\) embedded primary geometry is explicitly not computed.

## S130 cross-corank specialization

**Substantially closed geometrically.**

The new two-parameter family is a real \(2\to3\to4\) transition.

What remains is to connect this geometry to the complete higher-layer transverse primary structure of the failure scheme.

## S130 inverse ambiguity

**Open.**

The K3 is recovered; the original web is not.

## M130.2 — primary terminology

**Closed.**

The manuscript now distinguishes an intrinsic “primary signature” from noncanonical actual primary decompositions on splitting covers.

## M130.3 — Ballico 1993

**Open, responsibly disclosed.**

# 12. What I would require before another top-four review

I would not request another general top-four-style review after only editorial changes. The next revision should close the following small set of decisive items.

## E131.1 — write the packet descent theorem, not a sentence about finite images

Give a complete fpqc/Galois descent argument for the closed support packets from the splitting cover to the original base.

The proof should explicitly show:

1. what object carries the descent datum;
2. why the datum satisfies the cocycle condition;
3. why the descended fibre has exactly the desired geometric irreducible components;
4. why no extra fibre component is introduced;
5. why the descended packet remains compatible with the later flatness/intersection refinements;
6. how the associated-point equality and local torsion lengths descend.

This is the only remaining proof-level blocker I regard as central.

## S131.1 — compute a genuinely higher residual layer

Determine at least the generic associated supports and embedded structure of \(W_3\) and/or \(W_4\) at corank three or four.

A theorem explaining these layers geometrically through the incidence resolution would be substantially stronger than another determinant-depth calculation.

## S131.2 — connect the cross-corank family to the actual transverse failure primary structure

The seven-component incidence family is useful. The next step is to prove a theorem describing how the actual residual layers of the failure scheme specialize along that family, not only the pulled-back incidence variety and the residue-field algebra.

Even one nontrivial embedded component tracked across \(2\to3\to4\) would materially strengthen the paper.

## S131.3 — resolve or sharpen the inverse ambiguity

A result showing that the full nilpotent signature reduces the finite web-to-K3 ambiguity would provide a compelling conceptual endpoint.

If the ambiguity genuinely cannot be removed, compute or characterize it.

## M131.1 — finish the historical comparison

Obtain and read the full Ballico paper and record a precise novelty table.

## M131.2 — perform a final theorem-hierarchy cleanup

Remove stale “Revision 128” language and update every inherited description of the corank-three depth theorem to match v131.

# 13. Editorial assessment at top-four level

The paper now has several features that are genuinely strong:

- an intrinsic nonreduced failure scheme rather than only a degeneracy locus;
- reconstruction of a polarized quartic K3 from that scheme;
- a finite residual-colon formalism;
- a detailed corank-two primary atlas with generic-field certification;
- an exact global nilpotency exponent on the smooth Jacobian open;
- a geometric incidence resolution for the first layer;
- a concrete cross-corank family;
- and unusually disciplined computational provenance.

The problem is no longer that the manuscript is built on an elementary homological mistake. It is not.

The problem is now one of final theorem closure and conceptual concentration.

A 63-page paper with this many layers must make its strongest theorem unmistakable. At present the relative universal theorem still has a descent gap; the higher-corank geometry stops before the deepest residual primary layers; and the inverse theorem stops at the K3 rather than the web.

If E131.1 is repaired but no deeper geometric theorem is added, I would view the paper as a serious and potentially strong specialist contribution. To cross the threshold to a general top-four journal, I would want one theorem that makes the long primary-boundary development feel inevitable rather than encyclopedic.

# 14. Final assessment

Revision 131 is the strongest A2 version I have reviewed.

The two principal v130 local-algebra objections have been addressed by mathematically appropriate constructions. The Pieri argument is normalized and auditable. The sharp exponent-five theorem is real. The first two global supports and the cross-corank incidence family are real geometric progress. The source package and evidence discipline are excellent.

I nevertheless do not recommend acceptance at a general top-four mathematics journal in the present form.

The main proof-level reason is precise: the primary decomposition is constructed on a finite faithfully flat splitting cover, but the closed packet theorem is stated on the original base, and the intervening descent is not actually proved. “Finite images descend the packets” is not a substitute for an fpqc descent datum plus a fibrewise component argument.

The main structural reason is also precise: the new global geometry controls the first two layers and the nilpotency length, while the genuinely higher embedded primary geometry remains uncomputed. The cross-corank family is an incidence-resolution theorem, not yet a full higher-corank failure-scheme primary theorem. The inverse ambiguity remains unresolved.

My recommendation is therefore:

**Reject in the present form at a general top-four mathematics journal.**

I would encourage another revision if it simultaneously (i) closes the packet descent rigorously and (ii) turns the new incidence/cross-corank picture into a theorem about the actual higher residual primary layers or the inverse ambiguity. That would be a materially different submission, not a cosmetic continuation of v131.
