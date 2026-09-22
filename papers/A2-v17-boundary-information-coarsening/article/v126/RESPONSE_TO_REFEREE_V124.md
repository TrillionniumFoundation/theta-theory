# Response to the independent A2 revision-124 referee report — Revision 126

**Manuscript:** *Canonical nilpotent specialization, stratified contact algebra, and polarized reconstruction in multiplication failure*  
**Revision:** 126  
**Controlling report:** reviews/a2-v124-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Revision branch:** revision/a2-v126-global-nilpotent-specialization-2026-09-23  
**Parent mathematical revision:** revision/a2-v125-stratified-nilpotent-contact-boundary-2026-09-23  
**Date:** 23 September 2026

We thank the referee for insisting that the higher-corank response be a structural theorem rather than another rewriting of the Fitting matrix. Revision 125 supplied the global residual-colon formula and the first explicit singular-boundary calculations. Revision 126 adds the missing specialization mechanism: the entire nilpotent filtration is now the special fibre of one canonical flat extended-Rees degeneration.

Let \(\widehat{\mathcal N}_R\) be the nilradical of \(\mathcal O_{\widehat D_R}\). The new theorem forms
\[
\mathscr R_R=
\mathcal O_{\widehat D_R}[t,\widehat{\mathcal N}_R t^{-1}]
\subset
\mathcal O_{\widehat D_R}[t,t^{-1}]
\]
and proves that it defines a flat family over \(\mathbb A^1\) whose generic fibre is \(\widehat D_R\) and whose special fibre is
\[
C_{\widehat\Delta_R/\widehat D_R}
=
\operatorname{Spec}_{\widehat\Delta_R}
\operatorname{gr}_{\widehat{\mathcal N}_R}\mathcal O_{\widehat D_R}.
\]
The construction is intrinsic under abstract scheme isomorphism. Combined with the residual-colon theorem, the special fibre is
\[
\mathcal O_{\widehat\Delta_R}
\oplus
\bigoplus_{j\ge1}\mathcal L^{\otimes j}\otimes\mathcal O_{W_j},
\]
with multiplication induced by the colon tower. This is the Rees/normal-cone specialization proposed in the referee's Option C.

## E124.1 — actual higher-corank structure

**Addressed by Option C, now with an explicit specialization theorem.**

The all-corank block formula remains a presentation theorem. The all-corank structure is the intrinsic normal cone obtained as the special fibre of the canonical Rees family. Every projection corank and rank-drop locus lies in this one global special fibre. On the first singular boundary the colon schemes are computed explicitly: the whole mixed-regular collision boundary, the zero-quartic containment locus, and the first decomposable mixed-kernel wall.

## E124.2 — nilpotent depth across strata

**Addressed globally, with specialization rather than juxtaposition.**

Corank one, mixed-regular corank two, and the decomposable-kernel wall are restrictions of the same canonical special fibre. On mixed-regular rank two,
\[
\operatorname{gr}_{N}\mathcal O_{\widehat D_R}
=
\mathcal O_{\widehat\Delta_R}
\oplus
(\mathcal L\otimes\mathcal O_{\mathcal C_H})
\oplus
(\mathcal L^{\otimes2}\otimes\mathcal O_{\Sigma_R}),
\]
while at the decomposable wall the degree-two support is
\[
V(c,d,a^2,ab,b^2).
\]

## E124.3 — contact cover and primary structure

The v125 correction is retained. The global discriminant, the branch divisor on the finite-flat locus, and the primary interpretation on the mixed-regular simple-contact locus are distinct. The identity
\[
\mathcal I_{\widehat D_R}=\delta I_H\cap\mathfrak m^5
\]
proves that the vertex factor is genuinely primary through mixed-regular collisions. Repeated contacts have primary type
\[
(\delta^2,\delta q^e,q^{e+1}),
\]
and the containment case is separately
\[
\delta^2\mathfrak m=(\delta^2)\cap\mathfrak m^5.
\]

## E124.4 — Ballico 1993 priority boundary

The official Wiley volume record, DOI record, PDF action, and first-page scan were rechecked on 23 September 2026. The available endpoint still exposes metadata, references, and the first page, but not the complete theorem text. Revision 126 therefore does not manufacture a theorem-level comparison from metadata. No mathematical theorem in the revision uses a claim of non-anticipation by Ballico 1993 as a premise. The inspected 1996 continuation remains compared at theorem level.

This documentary access boundary is recorded explicitly rather than converted into a mathematical weakening of the paper.

## E124.5 — inverse problem

The v125 finite-etale theorem is retained. On dense opens the regular-web quotient maps to the polarized-K3 image as a finite etale cover of constant function-field degree
\[
d_{\mathrm{Tor}}=[\C(\mathcal W):\C(\mathcal K)]
\]
with transitive geometric monodromy. No unsupported degree-one assertion is introduced.

## E124.6 — theorem after subtracting classical Reye geometry

The nonclassical theorem can now be stated without the classical dimension count:

> The abstract multiplication-failure scheme reconstructs the polarized quartic K3 and canonically determines a flat extended-Rees degeneration to its nilpotent normal cone. The special fibre is controlled at every projection corank by residual colons; across the first singular Schubert boundary its contact cone, collision primary laws, vertex component, containment algebra, and first decomposable mixed-kernel wall are computed scheme-theoretically.

The classical Reye/nodal-Enriques geometry remains credited as classical context.

## Additional referee hardening

Revision 126 fixes the malformed TeX escape block in the v125 abstract. The historical v124 and v125 branches remain untouched. The v126 principal driver imports the v123/v125 proof architecture and uses a v126-local copy of the depth section whose sole inherited-source repair is the missing display-math delimiters exposed by CI; the mathematical statements and proofs are otherwise preserved. The new mathematical addition is the Rees-specialization theorem and its proof, together with revised front matter, response material, and branch-scoped verification.
