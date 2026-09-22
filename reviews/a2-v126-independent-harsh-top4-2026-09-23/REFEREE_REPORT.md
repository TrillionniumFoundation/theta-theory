# Independent harsh top-four referee report — A2 revision 126

**Manuscript:** *Canonical nilpotent specialization, stratified contact algebra, and polarized reconstruction in multiplication failure*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision:** `revision/a2-v126-global-nilpotent-specialization-2026-09-23`  
**Parent mathematical revision:** `revision/a2-v125-stratified-nilpotent-contact-boundary-2026-09-23`  
**Controlling previous report:** `review/a2-v124-independent-harsh-top4-2026-09-23`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/article/v126/geometry.tex`  
**Referee PDF recorded by the revision:** `papers/A2-v17-boundary-information-coarsening/article/v126/geometry.pdf` (36 pages according to the branch build receipt)  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the revision-126 source itself, together with the inherited v123 and v125 proof blocks that form the actual article, the v126 response letter and issue matrix, the exact-computation receipts, and the controlling revision-124 referee report. I did not treat the issue matrix's labels such as “resolved” as evidence. In particular, I checked whether the new Rees construction proves the stronger geometric statement for which it is being used.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 126 contains real mathematical progress relative to revision 124, but the decisive advance predates the new revision: revision 125 gives a useful global residual-colon identity and materially strengthens the rank-two boundary analysis. It proves the fixed vertex primary component through mixed-regular contact collisions, treats the containment case (h_Hequiv0), and computes the first transverse decomposable-kernel wall. Those points should be credited and should not be recycled as unresolved objections.

The new mathematical centerpiece of revision 126 is different. It forms the extended Rees algebra of the nilradical
[
mathscr R_{mathcal N}
=
mathcal O_{widehat D}[t,mathcal N t^{-1}]
subset
mathcal O_{widehat D}[t,t^{-1}]
]
and observes that this gives a flat deformation whose general fibre is (widehat D) and whose special fibre is
[
operatorname{Spec}_{widehatDelta}
operatorname{gr}_{mathcal N}mathcal O_{widehat D}
=
C_{widehatDelta/widehat D}.
]

I agree with this construction and with the proof of flatness. The difficulty is not correctness.

The difficulty is that this is the standard deformation-to-the-normal-cone/Rees construction for a closed immersion, applied here to the intrinsic nilradical. It packages the filtration already described in v125, but it does not geometrically determine the unknown graded pieces on the higher-corank and rank-drop strata. The manuscript therefore converts an incompletely classified filtration into one canonical family and then treats the existence of that family as if it were the missing all-boundary structure theorem.

For this paper, and especially for a top-four submission, that distinction is decisive:

> **A deformation to the normal cone packages a filtration; it does not compute the filtration.**

The v124 report's Option C did not ask merely for the existence of a Rees algebra. It explicitly contemplated a Rees/normal-cone replacement whose graded pieces are identified on explicit Schubert/contact strata and whose specialization controls every boundary. Revision 126 supplies the universal formal mechanism but still does not identify the schemes (W_j) on the major exceptional loci that motivated the objection.

Accordingly, I do not accept the v126 issue matrix's status “resolved-by-global-rees-option-C” for E124.1 or “resolved-by-specialization” for E124.2 as a top-four-level mathematical closure.

# 1. What revision 126 inherits that is genuinely stronger

A fair report should separate the substantial revision-125 advances from the comparatively formal revision-126 addition.

## 1.1 The global residual-colon filtration is useful

Revision 125 proves on the whole Grassmannian that
[
mathcal I_{widehat D}
=
mathcal I_{widehatDelta},
mathcal J^{mathrm{res}},
qquad
mathcal J^{mathrm{res}}
=
(mathcal I_{widehat D}:mathcal I_{widehatDelta}),
]
and, for (jge1),
[
operatorname{Ann}_{mathcal O_{widehat D}}(mathcal N^j)
=
rac{
(mathcal J^{mathrm{res}}:
 mathcal I_{widehatDelta}^{,j-1})
}{
mathcal I_{widehat D}
}.
]
With
[
W_j=
V_{widehatDelta}!left(
(mathcal J^{mathrm{res}}:
 mathcal I_{widehatDelta}^{,j-1})
+mathcal I_{widehatDelta}
ight)
]
and
[
mathcal L=
mathcal I_{widehatDelta}/
mathcal I_{widehatDelta}^{,2},
]
this yields
[
mathcal N^j/mathcal N^{j+1}
simeq
mathcal L^{otimes j}otimesmathcal O_{W_j}.
]

Locally, if the Schubert equation is (d=det T) and
(mathcal I_{widehat D}=dJ), the formulas become
[
operatorname{Ann}(N^j)=(J:d^{j-1})/(dJ),
qquad
N^j/N^{j+1}
simeq
A/igl((d)+(J:d^{j-1})igr).
]

This is an exact and useful reduction of the nilpotent filtration to a tower of residual colons. It is genuinely better than the revision-124 presentation-only statement.

But the theorem itself also says what remains to be done: the schemes (W_j) must be identified geometrically on the successive rank strata. That sentence is the correct description of the current boundary of knowledge in the manuscript.

## 1.2 The repeated-contact and containment corrections are real

On the mixed-regular rank-two locus, v125 proves
[
J=I_Hcapmathfrak m^3
]
and
[
mathcal I_{widehat D}
=
delta I_Hcapmathfrak m^5.
]

Thus the v124 concern about merely gluing the ideal (mathfrak m^5), without proving it remains an actual primary component, is materially addressed on the claimed mixed-regular locus.

The collision law
[
(delta^2,delta q^e,q^{e+1})
]
also gives a meaningful scheme-theoretic refinement of a repeated contact, rather than merely a statement about the support of the quartic roots.

The separate containment formula
[
mathcal I_{widehat D}
=
delta^2mathfrak m
=
(delta^2)capmathfrak m^5
]
and the identification of the containment locus with the finite reduced line scheme of the smooth quartic are worthwhile additions.

I therefore withdraw the old E124.3 objection in its original form.

## 1.3 The first decomposable mixed-kernel wall is an actual new boundary calculation

The theorem
[
(J_{mathrm{dec}}:delta)
=
(c,d,a^2,ab,b^2)
]
shows that the second intrinsic depth support becomes a length-three nonreduced thickening at the transverse decomposable-kernel wall.

This is exactly the kind of calculation the earlier report requested: it does not merely rewrite the universal maximal-minor formula but extracts the scheme structure of one exceptional boundary.

The issue is that it is only the first such wall.

## 1.4 The manuscript now distinguishes presentation from structure

The v125 section explicitly says that the all-corank block formula is a presentation theorem, while primary decomposition, associated-prime calculations, and nilpotent filtration statements require separate hypotheses.

This is a substantial improvement in mathematical scope discipline over revision 124.

Revision 126 unfortunately weakens that discipline again in its abstract and response matrix by making the standard Rees family carry more structural meaning than has actually been computed.

# 2. Audit of the new canonical Rees theorem

## 2.1 I accept the algebraic construction

Let (A) be an affine coordinate ring of (widehat D), and let (N) be its nilradical. The extended Rees algebra
[
mathscr R_N=A[t,Nt^{-1}]
subset A[t,t^{-1}]
]
is well defined.

The nilradical and its powers commute with localization, so the local constructions glue.

Multiplication by (t) is injective on (mathscr R_N). More generally, a nonzero element of (mathbf C[t]) acts injectively, so (mathscr R_N) is torsion-free over the PID (mathbf C[t]). Hence it is flat over (mathbf C[t]).

After inverting (t),
[
mathscr R_N[t^{-1}]
=
A[t,t^{-1}],
]
and therefore the family is trivial over (mathbf G_m).

Modulo (t), one obtains the associated graded ring
[
mathscr R_N/(t)
simeq
igoplus_{jge0}N^j/N^{j+1}.
]

Since (N) is precisely the ideal of the reduction
(widehatDelta=(widehat D)_{mathrm{red}}) in (widehat D), the special fibre is the normal cone
[
C_{widehatDelta/widehat D}.
]

An abstract scheme isomorphism preserves the nilradical and hence the entire construction.

I do not see a correctness defect in this theorem.

## 2.2 But this is standard deformation to the normal cone

The article currently presents the result as the “principal new theorem” of revision 126. That is not an appropriate novelty description.

For a closed immersion defined by an ideal (I), the associated graded algebra
[
igoplus_{nge0}I^n/I^{n+1}
]
and its relative spectrum are the normal cone, and the extended Rees algebra gives the standard deformation to that normal cone.

This is classical intersection-theory technology; see, for example:

- William Fulton, *Intersection Theory*, Chapter 5, §5.1, “Deformation to the Normal Cone”;
- the Stacks Project discussion of the normal cone and the graded algebra (igoplus I^n/I^{n+1}) (Tag 062Z and surrounding material).

The manuscript should cite this directly.

What is specific to this paper is not the existence or flatness of the Rees deformation. It is whatever one can prove about the ideal (N), the colon schemes (W_j), their geometric supports, their multiplicative structure, and how those objects change across the multiplication-specific rank strata.

That is where the paper's theorem must live.

## 2.3 The construction adds no new information beyond (operatorname{gr}_{N}) unless the graded pieces are identified

A Rees family is highly useful because it retains all powers (N^j) in one object. But once the graded algebra
[
operatorname{gr}_Nmathcal O_{widehat D}
]
is already known abstractly, forming its standard deformation does not by itself determine any previously unknown support or primary structure.

Revision 125 writes
[
operatorname{gr}_Nmathcal O_{widehat D}
simeq
mathcal O_{widehatDelta}
oplus
igoplus_{jge1}
mathcal L^{otimes j}otimesmathcal O_{W_j}.
]

Revision 126 then says that this is the special fibre of one canonical flat family.

The missing geometry has simply moved into the unknown (W_j)'s.

This observation should govern the entire assessment of the revision.

# 3. Decisive blocker E126.1 — the v124 Option C has been met formally, not substantively

The v124 report proposed three routes for closing the higher-corank objection. Its Option C explicitly suggested an associated graded/Rees/normal-cone theorem, but not merely the universal existence theorem.

The requested substance was a canonical filtration whose graded pieces are identified on explicitly described Schubert/contact strata and whose specialization controls every boundary.

Revision 126 has only half of that package.

It has:

1. a canonical filtration;
2. a canonical associated graded algebra;
3. a canonical Rees deformation;
4. explicit calculations on corank one, mixed-regular corank two, the containment subcase, and one transverse decomposable-kernel wall.

It does not have an explicit geometric description of the graded pieces on the remaining higher-corank strata.

Thus the sentence in the v126 response

> “Every projection corank and rank-drop locus lies in this one global special fibre.”

is formally true but mathematically weak.

Every point of (widehat D), whatever its rank, necessarily appears somewhere in the special fibre of the deformation to the normal cone of its reduction. The statement does not tell us what happens there.

At a top-four level, “all boundary strata belong to the same canonical object” cannot substitute for “the object is determined on all boundary strata.”

### What would close E126.1

The next revision should prove a theorem that geometrically identifies the relevant (W_j) and their multiplicative maps on a canonical stratification.

A satisfactory theorem would state, for each allowed projection rank and each necessary secondary rank condition:

- which (W_j) are nonempty;
- their radicals;
- their scheme structures;
- their dimensions and multiplicities;
- the nilpotency index;
- the associated primes of the failure scheme;
- the multiplication maps
  [
  (N^i/N^{i+1})otimes(N^j/N^{j+1})
  longrightarrow
  N^{i+j}/N^{i+j+1};
  ]
- and how these data specialize when one crosses from one stratum to another.

That would turn the Rees object from a container into a structure theorem.

# 4. Decisive blocker E126.2 — the principal exceptional loci remain uncomputed

The manuscript still does not classify the loci on which the mixed-regular hypotheses fail, except for one transverse decomposable-kernel wall.

The following cases remain structurally open in the article.

## 4.1 Failure of injectivity of (A_H)

The current rank-two structure theorem begins by requiring
[
A_H:operatorname{Sym}^2H	o S_R
]
to be injective.

When this rank drops, the Gaussian elimination producing the (3	imes7) residual matrix changes.

The manuscript does not determine the resulting residual ideal, associated primes, or nilpotency filtration.

The Rees construction does not change that fact.

## 4.2 Failure of surjectivity of the mixed map

The mixed-regular theorem also requires the quotient mixed map
[
overline B_H:
Hotimes(V/H)	o S_R/operatorname{im}A_H
]
to be surjective with one-dimensional kernel.

The paper computes the transition from a rank-two generator of that one-dimensional kernel to a decomposable generator.

It does not classify the strata on which (overline B_H) drops rank further, or on which the kernel dimension increases.

Those are precisely the kinds of loci on which new embedded components or larger nilpotency indices can appear.

## 4.3 Projection corank three and four

The all-corank block identity is valid at these points, but no comparable structure theorem is given.

In particular, the paper does not state:

- the nonzero (W_j);
- the maximal nilpotency index;
- the associated primes;
- whether the special fibre develops new components;
- the local Hilbert functions;
- or the relation of those pieces to explicit Schubert strata.

Again, the Rees family exists automatically at these points. Its existence is not a classification.

## 4.4 Deeper nilpotent layers are not bounded or computed geometrically

The global colon formula gives the formal identity
[
	ext{nilpotency index}
=
1+min{k:d^kin J}
]
on a Schur chart.

That is useful.

But outside the computed rank-two loci the paper does not determine the minimum, so it does not determine the depth.

A top-four theorem advertised as “global nilpotent specialization” needs more than a formula reducing the answer to another ideal-membership problem on each missing stratum.

# 5. Decisive blocker E126.3 — the abstract and response letter overstate the computed scope

The abstract says:

> “Across the first singular Schubert boundary we compute that special fibre explicitly.”

This is too broad.

What is actually computed is:

- the mixed-regular rank-two locus, including repeated contact collisions;
- the mixed-regular containment case;
- the first transverse decomposable mixed-kernel wall.

That is a nontrivial and coherent package.

It is not the entire first singular Schubert boundary, because the boundary also contains the rank-drop loci for (A_H) and (overline B_H), higher-dimensional mixed kernels, and nontransverse versions of the decomposable wall.

The response letter similarly says that all coranks and rank-drop loci are realized in one global special fibre and uses this to mark the higher-corank objections resolved.

The correct wording is more modest:

> the Rees construction canonically places every rank stratum in one deformation; the paper determines its graded geometry completely on corank one and on specified portions of corank two, including the first tensor-rank wall.

That statement would be accurate.

At a very selective journal, the scope of the headline theorem must be readable from the theorem statement itself, not reconstructed from qualifiers scattered across later sections.

# 6. Decisive blocker E126.4 — the Ballico 1993 priority boundary remains open

The revision handles this limitation responsibly.

The bibliography identifies:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* **163** (1993), 5–13, DOI 10.1002/mana.19931630102.

The revision records that the available Wiley endpoint exposes bibliographic information and the first page but not the complete theorem text in the present environment. It does not infer non-anticipation from metadata. That is correct scholarly behavior.

Nevertheless, for a top-four publication claim, the priority boundary remains unresolved.

The article's title, object, and historical line are close enough to Ballico's earlier “failure locus” work that the nearest predecessor should be read at theorem level before the journal is asked to certify exceptional novelty.

This is not a claim that Ballico anticipates the present theorem. I have no basis for such a claim without the full paper.

It is the opposite point: the present evidence is insufficient to certify the comparison either way.

### Required action

Obtain the full 1993 article through a research library, interlibrary loan, author archive, or direct author contact, and add a theorem-by-theorem comparison covering at least:

- Ballico's definition of the failure locus;
- the relevant Grassmannian parameter;
- the multiplication/evaluation morphism;
- whether scheme structure is retained;
- whether Fitting ideals or embedded/nonreduced components appear;
- whether higher-order failure is organized by a nilpotent or normal-cone filtration;
- and whether any geometric reconstruction theorem is proved from the failure object.

Until this is done, I would not sign off on the historical-priority portion of a top-four report.

# 7. Major issue M126.1 — the Torelli “monodromy theorem” is largely formal

Revision 125 improves the inverse-problem discussion by replacing the vague phrase “finite ambiguity” with a finite étale cover after shrinking:
[
	au:mathcal W^circ	omathcal K^circ,
qquad
deg	au
=
[mathbf C(mathcal W):mathbf C(mathcal K)].
]

It also observes that the geometric monodromy action is transitive.

This is correct, but its mathematical content should not be overstated.

Once one already knows that a dominant morphism between irreducible varieties in characteristic zero is generically finite, it is standard to normalize the target in the function field and shrink away the branch and nonflat loci to obtain a finite étale cover.

Likewise, connectedness/irreducibility gives transitivity of the monodromy action on a generic fibre.

Thus the theorem gives an exact formal packaging of generic finiteness, but it does not classify the finite packet.

The still-open questions are the substantive ones:

- What is (d_{mathrm{Tor}})?
- Is (d_{mathrm{Tor}}=1)?
- If not, what is the monodromy group?
- Which compatible Enriques/Reye structures form the fibre?
- Do the deeper nilpotent strata separate points in that fibre?
- Where does the degree jump?

At top-four level, the inverse problem remains incomplete until at least one of these questions is answered in a genuinely new way.

# 8. Major issue M126.2 — after subtracting classical and standard geometry, the residue must carry the significance burden

The paper has become much better at distinguishing classical Reye geometry from its own contribution.

That is welcome.

But revision 126 adds another layer that must likewise be subtracted when assessing novelty: standard deformation-to-the-normal-cone technology.

After removing:

1. the classical Reye/nodal-Enriques geometry;
2. the classical nine-dimensional moduli framework;
3. the standard Rees/deformation-to-normal-cone mechanism;
4. the formal finite-étale shrinking of a generically finite map;

the genuinely manuscript-specific core is approximately:

- the intrinsic reconstruction of the polarized quartic K3 from the nilpotent structure of the multiplication-failure scheme;
- the global residual-colon formula for the nilpotent filtration;
- the explicit mixed-regular rank-two contact algebra, including collision primary laws and the containment case;
- and the first decomposable mixed-kernel wall.

This is a coherent and potentially publishable mathematical package.

For a general top-four journal, however, the paper must demonstrate that this package has significance beyond a highly specialized determinantal calculation attached to one Hilbert function ((1,4,6)).

At present the manuscript has not crossed that threshold.

The standard Rees family does not supply the missing breadth.

# 9. Major issue M126.3 — novelty hygiene for the Rees theorem must be fixed

The v126 index calls the Rees specialization the “Principal new theorem.”

The article should instead distinguish:

### Standard mechanism
For any closed immersion defined by (I), the extended Rees algebra gives a deformation to the normal cone with special fibre (operatorname{gr}_I).

### Manuscript-specific theorem
For this multiplication-failure scheme, identify the nilradical, its residual-colon filtration, the geometric meaning of the graded supports, and the multiplication structure in the special fibre.

The first item should be cited, stated efficiently, and treated as a tool.

The second item should be where the novelty claim is concentrated.

This revision currently reverses that emphasis.

# 10. Major issue M126.4 — the global residual-colon theorem is exact but still partly tautological

I regard the global residual-colon theorem as useful, but its strength should be calibrated carefully.

Starting from
[
mathcal I_{widehat D}
=
mathcal I_{widehatDelta}mathcal J^{mathrm{res}},
]
the formulas
[
operatorname{Ann}(N^j)
=
(mathcal J^{mathrm{res}}:
 mathcal I_{widehatDelta}^{j-1})/
mathcal I_{widehat D}
]
and
[
N^j/N^{j+1}
simeq
mathcal L^{otimes j}otimesmathcal O_{W_j}
]
are essentially colon/cancellation identities.

Their real geometric force arises only when the (W_j) are independently identified.

The manuscript succeeds at this on several rank-two pieces.

It should not describe the formal definition of (W_j) itself as an all-corank geometric classification.

This distinction should be made explicit in the main theorem statement.

# 11. The reconstruction theorem remains the strongest part of the paper

The strongest theorem in the current package is still the polarized reconstruction result inherited from v123.

On the corank-one open, the failure ideal has the exact normal form
[
I_D=I_Delta I_E=I_Deltacap I_E^2,
]
the nilradical is the intrinsic invertible line
[
Nsimeqmathcal O_E(-Delta),
]
and its annihilator recovers (E).

The line-bundle calculation
[
omega_Eotimes N^{-(p+e-1)}
simeq
ho^*mathcal O_Y(e)
]
together with
[
ho_*mathcal O_E=mathcal O_Y
]
recovers the section ring of (mathcal O_Y(e)). In the K3 case the torsion-free Picard argument then recovers the quartic polarization itself.

This is conceptually stronger than the new Rees theorem because it extracts unexpected geometric information from the nonreduced scheme.

If the authors want a top-four case, they should build outward from this reconstruction phenomenon and prove that the deeper nilpotent strata yield genuinely new global reconstruction/classification information, rather than making the universal Rees deformation the headline.

# 12. Computational evidence

The branch-scoped evidence is useful and, importantly, not oversold in the machine-readable files.

The v126 build receipt records:

- a generated PDF;
- no undefined references or citations;
- no LaTeX error;
- a 36-page principal article;
- and the presence of the Rees theorem.

The exact rank-two regressions record the expected identities for repeated contact, containment, and the decomposable-kernel wall.

The K3 certificate records exact finite witnesses and explicitly says
`general_proof_machine_certified: false`.

That last flag is the correct posture.

These computations are valuable regression checks. They are not independent evidence that the global higher-corank theorem has been proved.

I would retain them, but I would not respond to this report by adding more finite test cases. The remaining gaps are structural.

# 13. Specific theorem-level revisions required for top-four reconsideration

A credible next revision should make a mathematical advance beyond the universal Rees construction.

## E126.1 — determine the special fibre, not only construct it

Give a geometric classification of the (W_j) on a canonical stratification of the entire rank-two boundary.

At a minimum include:

- (A_H)-rank drop;
- failure of mixed surjectivity;
- higher-dimensional mixed kernels;
- decomposable and nontransverse kernel walls;
- collisions of these conditions with the quartic-contact discriminant;
- and the containment line locus.

For each stratum compute radical, associated primes, nilpotency index, and local Hilbert function.

## E126.2 — extend the classification to projection corank three and four, or prove an equally strong global theorem

If a direct primary classification becomes unwieldy, an acceptable replacement would be a theorem that identifies the entire graded algebra on these strata through intrinsic vector bundles/sheaves with explicitly determined supports.

What is not sufficient is a formula that leaves the answer as an unspecified colon ideal.

## E126.3 — prove actual specialization laws between strata

The Rees parameter (t) specializes the whole scheme to its normal cone, but it is not the parameter along which one crosses the rank stratification.

The manuscript should separately study one-parameter degenerations in the **moduli/rank variables** and show how the primary components, (W_j), and nilpotency indices specialize.

This is the boundary-control theorem that is currently missing.

## E126.4 — close the Ballico 1993 comparison

This is documentary rather than algebraic, but for the top-four novelty claim it remains necessary.

## E126.5 — advance the inverse problem beyond formal generic finiteness

Compute (d_{mathrm{Tor}}), prove generic injectivity, determine a nontrivial monodromy group, or show that a newly classified deeper nilpotent stratum canonically separates the finite Torelli packet.

## E126.6 — reframe the Rees theorem as standard background

Cite the classical deformation-to-the-normal-cone construction explicitly and state precisely which new geometric identifications are special to this manuscript.

# 14. Editorial and presentation corrections

Even before the larger structural work, I would make the following corrections.

1. Replace “Across the first singular Schubert boundary we compute that special fibre explicitly” by a statement naming the exact computed open loci and wall.

2. Replace the issue-matrix labels “resolved-by-global-rees-option-C” and “resolved-by-specialization” with a more accurate status unless the remaining (W_j) are actually classified.

3. In the introduction, separate three levels:
   - universal Fitting presentation;
   - universal nilradical/Rees formalism;
   - multiplication-specific geometric classification.

4. Add a classical reference for deformation to the normal cone and normal cones.

5. State prominently that the Rees family is intrinsic because the nilradical is intrinsic; do not present that formal functoriality as a substitute for explicit higher-corank geometry.

6. Retain the current careful wording around Ballico 1993. Do not infer novelty from the absence of accessible full text.

# 15. Final assessment

Revision 126 is not a failed revision. The project is substantially more coherent than it was at revision 124.

The strongest progress is real:

- the global residual-colon filtration is exact;
- the mixed-regular collision algebra is stronger;
- the vertex primary component is genuinely controlled through those collisions;
- the containment case is separated correctly;
- the first decomposable mixed-kernel wall is computed;
- and the paper is much more disciplined about what is classical Reye geometry.

The new Rees theorem is also correct.

But correctness of the Rees construction is not the same as closure of the higher-corank problem.

The family
[
mathfrak D_R	omathbb A^1
]
exists because deformation to the normal cone exists for every closed immersion. The hard manuscript-specific content is the geometry of its special fibre. That geometry is still explicitly known only on selected strata. The remaining rank-drop and higher-corank loci are carried into the special fibre without being classified.

Consequently the central top-four objection survives in a more precise form:

**revision 126 has produced a canonical container for the missing higher-corank structure, but it has not yet determined the missing structure.**

Together with the unresolved theorem-level Ballico 1993 comparison and the still-formal inverse-problem monodromy statement, this prevents me from recommending publication in a general top-four mathematics journal.

**Recommendation: reject in the present form at a general top-four journal. Reconsideration would require a genuinely new geometric classification of the graded special fibre across the remaining rank strata, not another formal repackaging of the same filtration.**
