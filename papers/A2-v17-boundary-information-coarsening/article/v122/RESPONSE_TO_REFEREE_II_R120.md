# A2 revision 122 — response to Referee II on revision 120

**Manuscript:** *Ramification and intrinsic primary boundaries in multiplication failure*.

**Controlling report:** `review/a2-v120-referee-ii-harsh-top4-2026-09-22`, commit `489009deff528b896d2daee3fcf18a2ebdc2ab39`, report `reviews/a2-v120-referee-ii-harsh-top4-2026-09-22/REFEREE_REPORT.md`.

**Base used:** v121, commit `44f6b0bf3bb4f1f8c2a87d84beb61d82194fd5e7`. The second report postdates the v121 build and reviews v120, so this revision distinguishes retained v121 answers from further v122 mathematics. The first v120 report, commit `b20eafa006fd3abe650ad7478542d637327b1094`, is also addressed. Both reports are repository referee-style assessments, not journal-issued decisions.

The principal reading object is `geometry.pdf`. The complete `paper.pdf` and `applications.pdf` remain companion editions. Every v121 mathematical part is retained byte for byte and every old theorem/equation label remains; `evidence/PRESERVATION.json` gives the check. The new arguments are in Sections 1–4 and the additional literature section. Source labels below are stable across reading editions; `evidence/THEOREM_MAP.json` supplies compiled numbers and pages.

## RII-120.1 — nearest-source comparison

**Status: not completed.** We again attempted the publisher's complete-PDF route for Ballico 1993 and searched the available Library for the exact title and DOI. The publisher route did not deliver the full article. The Library results were earlier A2 papers, patches and audits containing the citation, not a complete copy of the source. They are not treated as substitutes for its theorem pages. We therefore do not claim either anticipation or non-anticipation.

`LITERATURE_AUDIT.md` retains the earlier source-check history and gives a comparison matrix with all requested axes: scheme structure, incomplete/complete series, moving contacts, multiplication versus embedding/jet properties, quotient/Hilbert constructions, conductor mechanisms, embedded primary structure and global regularity. The columns requiring the unseen theorem statements remain explicitly unverified. The main article states this boundary in `sec:v122-literature` rather than using missing access as evidence of originality.

We did inspect the author-hosted Huybrechts K3 text at the actual statements used in the new proof (Chapter 1, Example 1.3(i); Chapter 9, proof of Corollary 4.4), including rendered pages. The classical quartic and differential-form arguments are credited. No copyrighted third-party book or article is redistributed with the revision.

## RII-120.2 — a structural class with genuine moduli

**Response: a new fixed-tensor class theorem, not another isolated algebra.** v121 already contains the universal weighted-determinantal primary flag and the explicitly non-isotrivial elliptic family. The new revision treats every relation space in a proved nonempty invariant open

\[
G_e^\circ\subset\operatorname{Gr}(e,\operatorname{Sym}^2V),\qquad e=3,4,
\]

with Hilbert function `(1,e,binom(e,2))`. These include `(1,4,6)` algebras, not just the length-five class. The open is defined intrinsically by a basepoint-free relation system and a smooth ramification determinant. Its nonemptiness follows from a codimension-four corank incidence, a separate first-order-spanning incidence, and proper generic smoothness. All hypotheses are verified before using any primary statement (`prop:admissible-ramification`). The quotient orbit-dimension deficits are at least one and nine, respectively. We state this as an orbit estimate, not as the construction of a fine moduli space or a dominance theorem for K3 moduli.

The key step is the exact restriction–contraction cokernel identity (`lem:restriction-contraction`). It identifies the quadratic restriction determinant with the ramification scheme of the finite morphism defined by the relation quadrics (`prop:quadratic-ramification`). Thus the embedded prime is predicted directly from intrinsic data of `ker(gamma)`.

For every fixed admissible algebra, and on its entire projection-corank-at-most-one open, the full Fitting ideal is

\[
I_D=I_\Delta I_E=I_\Delta\cap I_E^2.
\]

There are exactly two associated supports, with `E` the graph bundle over the ramification curve or K3 surface times projective space (`thm:ramification-primary`). The proof computes local ideals over the actual fixed tensor, not by specializing a universal primary decomposition. For all ordinary powers,

\[
I_D^n=I_\Delta^n\cap I_E^{2n},
\]

with exact nilradical index `2n` along `E`, generic divisor multiplicity `n`, and embedded torsion length `n(n+1)/2` (`thm:primary-powers-intrinsic`). These powers are ideal-power thickenings, not new symmetric multiplication degrees. The specified families and all these thickenings are flat (`prop:ramification-flat-family`).

**Exact scope:** this theorem does not classify the omitted projection-corank-at-least-two locus for `(1,3,3)` or `(1,4,6)`, nor assert that arbitrary relation tensors lie in the open. The retained universal flag theorem and complete `(1,2,2)` theorem have their own, unchanged scopes.

## RII-120.3 — descent, associated points and canonical data

**Response: direct global calculation plus the retained formal descent.** v121's `lem:frame-primary-descent` and `cor:loewy-primary-descent` are retained unchanged, including the global definitions of the factor-surface, extreme-point, colon and embedded-primary ideals in `(1,2,2)`.

For the new class, `lem:global-two-stratum` proves the intersection on the smooth Grassmannian open itself: locally `I_D=t(t,f)` with `t,f` relative regular parameters, and `(t,f)^{2n}:t^n=(t,f)^n`. The proof supplies primarity, explicit witnesses to irredundancy, and the exact associated-point set. The graph-bundle functor specifies the global supports, while every ideal displayed is an intrinsic coherent ideal sheaf. This is a named proof on the global scheme, not an abbreviated appeal to regular fibres of a torsor.

The important distinction is made explicit. Associated supports are canonical. The particular ideal powers used in our formula are intrinsic choices of primary representatives; a general embedded primary representative is not declared unique. The module obtained by killing the generic localization is canonical, and its annihilator recovers the full ordinary-power neighbourhood `E^[n]`. For `n=1`, this is simply the nilradical and its annihilator. The geometry used later is recovered from that module, not from a noncanonical primary component.

## RII-120.4 — a genuinely global consequence

**Response: intrinsic reconstruction of a ramification curve or K3 surface.** Theorem `thm:intrinsic-ramification-recovery` proves

\[
D_R\simeq D_{R'}\quad\Longrightarrow\quad Y_R\simeq Y_{R'}
\]

for abstract complex-scheme isomorphisms. No Grassmannian embedding, input-algebra map, marked hyperplane parameter or frame is required of the isomorphism. The proof first recovers `E` as the annihilator subscheme of the nilradical, then identifies its stable birational base, and finally cancels projective-space factors over the non-uniruled genus-one or K3 base. The cancellation argument and the needed birational K3 conclusion are included in `lem:nonuniruled-cancellation`.

This distinguishes genuinely global geometry invisible to the fixed rational reduction: a smooth projective compactification of `E` has `h^1=1` in the cubic case and `h^1=0, h^2=1` in the quartic case, whereas the corresponding compactification of the reduced divisor has no higher coherent cohomology. In the explicit Hesse subfamily, different `j` values now distinguish the abstract full failure schemes (`cor:intrinsic-elliptic-distinction`), strengthening v121's distinction of the input algebras.

This result uses the embedded module essentially. If the nilradical is discarded, its annihilator cannot recover `E`; the remaining determinant divisor is the same rational object for all members. This is not the reproduction of a finite Fitting scheme by global section multiplication.

**What is not inferred:** recovery of a polarization, reconstruction of the finite map or algebra, realization of every quartic K3, or a computed image dimension in K3 moduli. None is needed for the proved reconstruction theorem.

## RII-120.5 — complete claims and unital planes

**Response: maintained precise terminology, with the new class stated explicitly.** The complete classification retained from v120/v121 is named for Hilbert function `(1,2,2)`, including its extreme-corank point. The new abstract gives the two new Hilbert functions and the exact projection-corank open. It does not call this a classification of all length-five, length-seven or length-eleven algebras. The parameters are unital subspaces `C + K`, not ordered generating tuples, and these subspaces need not generate the entire algebra at a failure point. The original clarification in `sec:v121-introduction` remains verbatim.

## RII-120.6 — journal architecture without deleting mathematics

**Response: focused principal article, preserved companions.** `geometry.tex` remains the primary journal manuscript in `amsart` form, led by a single chain: quadratic relation system → ramification cokernel → primary scheme and its powers → intrinsic geometric recovery. The universal flag, low-Loewy classification, conductor and relative/global-section theorems are retained in the principal mathematical development. The long `paper.tex` adds all historical complementary geometry and statistical appendices, while `applications.tex` remains a separately cross-referenced companion.

No historical mathematical part is silently removed or replaced by a summary. Original v121 files and branches remain untouched; within v122 all old parts are byte-identical and all old core inputs are still active. Updated front matter and new sections explain the dependence rather than asking the reader to infer it from the archive. Successful compilation, source hashes and preservation tests are delivery evidence, not journal acceptance or proof certification.

## RII-120.7 — the A2 pipeline role

**Response: a standalone theorem chain, with no invented dependency.** `DEPENDENCY_MAP.md` gives the exact internal arrows. No A1 theorem is assumed, and no particular A3–D1 manuscript is represented as a verified consumer of the new theorem. A2 remains the repository identifier, not part of the mathematical significance argument. This does not weaken or remove a theorem: it makes the logical inputs accurate.

## Crosswalk to the first v120 report and earlier closed items

The first report's E120.1 is the same unfinished Ballico comparison. Its scale and global-consequence objections are answered by the new fixed-tensor and reconstruction theorems above, in addition to the v121 universal flags and elliptic family. Its formal-descent request is answered by the retained frame lemma and the new direct global lemma. Scope, architecture and dependency objections have the corresponding responses RII-120.5–7. The original `RESPONSE_TO_R120.md` is retained as the v121 response rather than retroactively edited to claim these new arguments.

We do not reopen the old defects which both v120 reports explicitly regarded as answered: the `(1,2,2)` primary classification, conductor kernel, sharp `r+1` stabilization, detailed relative incidence/base change, and the source-bound build. Their statements and exact regressions remain in the revision. The new exact tests verify the power-intersection identities for `n=1,...,8`, symbolic restriction/Jacobian identities, and explicit cubic and quartic examples on every projective chart over `QQ`. They supplement, rather than replace, the proofs for the full parameter class.

The requested mathematical and expository responses are now submitted for renewed review. RII-120.1 remains a specifically identified documentary item; this response does not certify absolute priority or a journal outcome.
