# Second independent harsh referee report on A2, revision 65

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 18, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society  
**Round:** independent second examination of revision 65

This is an author-requested, AI-assisted external-referee-style assessment. It is not a commissioned journal report, an editorial decision issued on behalf of any journal, or a formal proof certificate. I separate mathematical correctness, novelty, exceptional significance, and presentation. A negative recommendation below is not converted into an invented technical error.

## 1. Recommendation

**Recommendation: reject at the requested top-four general-mathematics level.**

The reason for this recommendation is not that I have found a fatal sign error or a false theorem in the new Section 9. On a second independent reading, the central v65 chain remains mathematically coherent within the scope audited here:

1. the two-offset quotient separates the unequal future and past actions under the stated common-amplitude physical-law model;
2. the stationary boundary envelope counts the initial contact once and the later visits twice;
3. the signed cyclic response
   $$
   \mathcal C_n=(I+T_n)(I-T_n)^{-1}
   $$
   has the stated nonvanishing determinant, including odd contact cycles and odd jet orders;
4. the curvature block is genuinely part of the inverse rather than supplied data;
5. the analytic inverse is not deduced merely from diagonal Taylor blocks: the proof constructs a Banach-valued action map, inverts finitely many low degrees, and uses a contracted-evaluation tail inverse.

These are substantive achievements. They strengthen v64, and it is no longer correct to say that the general-period part of the paper is forward-only.

My adverse recommendation is instead based on the level of mathematical reach relative to the strength of the supplied observation. The v65 theorem fixes the collision polygon, contact points, signed tangent/normal frames, phase labels, flight geometry, closing translation, graph-coordinate sensors, and two full phase-resolved function-valued endpoint laws. Once these data are supplied, the two-offset algebra recovers the one-variable actions explicitly and the remaining local shape inversion is driven by a uniformly contracting scalar Jacobi tail. The result is a serious local coordinate theorem, but I do not find that the current manuscript demonstrates the kind of conceptual reach, intrinsic reconstruction, or new obstruction-resolution that would justify the requested exceptional general-journal placement.

The manuscript also has a structural problem at article level. The 143-page principal article places side by side several genuinely different observation models: the new fully marked general-period inverse; the weaker-data alternating-channel inverse; unknown-lattice/global registration results; and charged finite-preparation/statistical results. The text usually states the distinctions correctly, but the aggregate headline still invites the reader to attribute the strongest feature of one model to the others. For a top-four submission, the decisive theorem and its information content need to be much more sharply isolated.

I therefore recommend rejection rather than another nominal repair round. A further small lemma, build certificate, preservation audit, or additional finite diagnostic would not change this judgment.

## 2. Frozen object reviewed

| Object | Identity |
|---|---|
| Mathematical source commit | 06a197e4d11bc3d4193e9f0b7904105df35875fa |
| Reconstructed manuscript subtree | 469aba06035399f96f07417b172653228df36114 |
| Source branch | revision/a2-v65-referee-response-2026-09-16 |
| Native-products branch | revision/a2-v65-native-products-35059519641-1 |
| Native-products attestation head | 5425d9846069a0d23d454d20fe19ed0586d39270 |
| Manuscript directory | papers/A2-v17-boundary-information-coarsening/ |
| Previous v65 review branch | review/a2-v65-independent-harsh-top4-2026-09-16 |
| Previous v65 report | reviews/a2-v65-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md |

The products head attests source-matched native Git objects for source commit 06a197e4d11bc3d4193e9f0b7904105df35875fa. I review the mathematical source, not the fact that a PDF compiled successfully. Build reproducibility and mathematical validity are separate.

The present report is deliberately a second assessment. I read the previous v65 report but did not treat its conclusions as binding. Where the second examination agrees with it, I say so; where I sharpen the criticism, I identify the additional editorial issue.

## 3. Coverage

The central new source examined is:

- article/10b_periodic_contact_inverse_v65.tex, the complete Section 9 module;
- article/00f_periodic_contact_overview_v65.tex;
- the current abstract and principal introduction;
- RESPONSE_TO_REFEREE_V65.md;
- HISTORICAL_DERIVATION_AUDIT_V65.md;
- LITERATURE_CHECK_V65.md;
- journal/DEPENDENCY_LEDGER_V65.md;
- VALIDATION_V65.md;
- the preceding v64 report and the first independent v65 report.

I also traced the new Section 9 claims back to the retained periodic relative law and the earlier contracted-evaluation/real-to-disc mechanisms where they are used.

This is not a fresh proof certification of every inherited theorem in the 319-page technical manuscript. In particular, I do not reissue a new certification of every global matching, lattice, calibration, finite-experiment, and statistical argument merely because those files are retained byte-for-byte. Retention is provenance evidence, not proof evidence.

## 4. Mathematical findings that survive the second audit

### R65.2-M1. The marked graph coordinate is not circular

The local unknowns are written as
$$
R_i(x)=q_i+\nu_i^{-1}\{t_i x-n_iF_i(x)\},
\qquad F_i(0)=F_i'(0)=0.
$$
The measured coordinate is the scaled tangent projection, not the unknown normal graph height. Thus the theorem does not secretly observe the function it reconstructs. The marks nevertheless supply a great deal of geometry: the contact locations, normals, tangent orientations, flight directions, incidence cosines, phase registration, and closing translation.

The signed Hessian
$$
D^2h_i(0,0)=
\begin{pmatrix}
k_i+c_i&-\epsilon_i k_i\\
-\epsilon_i k_i&k_i+c_{i+1}
\end{pmatrix}
$$
is consistent with direct chord differentiation in these normalized graph coordinates. After sign conjugation, the positive mass is $2c_i$. The half-line one-step factors have modulus below one. I do not find a missing cosine or hidden curvature input here.

### R65.2-M2. The two-offset algebra is correct under its model

For
$$
f_d(u,v)=Z_d^{-1}B^-(u)B^+(v)\{d-A(u)-C(v)\}
$$
at two distinct positive offsets $d_1,d_2$, the ratio
$$
Q(u,v)=
\frac{f_{d_1}(u,v)f_{d_2}(0,0)}
     {f_{d_2}(u,v)f_{d_1}(0,0)}
$$
eliminates both normalizers and both common amplitude factors. Solving the resulting fractional-linear equation gives
$$
A(u)+C(v)
=
\frac{d_1d_2(1-Q(u,v))}
     {d_2-d_1Q(u,v)}.
$$
Axis restriction then separates $A$ and $C$. This is elementary once the physical-law factorization is available, but it is correct.

The important qualification is that this cancellation uses the same endpoint amplitude functions at both offsets. An offset-dependent recording efficiency or sensor distortion would generally not cancel. That is outside the theorem and is not a counterexample. It is, however, part of the information model and should remain prominent whenever the theorem is advertised.

### R65.2-M3. The signed cyclic block calculation is consistent, including odd cycles

The stationary envelope gives
$$
(D\mathcal S(F)\eta)_b(u)
=
\alpha_b(u)\eta_b(u)
+
\sum_{j\ge1}
v_{b,j}(u)\eta_{b+j}(x_{b,j}(u)).
$$
At the reference contact, the initial weight is one and the internal visit weight is two. For a fresh homogeneous degree $n$ this produces
$$
I+2\sum_{j\ge1}T_n^j
=
(I+T_n)(I-T_n)^{-1},
\qquad
(T_nz)_b=\sigma_b^n z_{b+1}.
$$

The determinant
$$
\det\mathcal C_n
=
\frac{1-(-1)^r\Lambda^n}{1-\Lambda^n},
\qquad
\Lambda=\prod_i\sigma_i,
$$
is nonzero for $|\Lambda|<1$. It equals one for even physical contact cycles but not in general for odd cycles. The source does not erase the signs by doubling the oriented period. That is the correct distinction.

The degree-two statement is local invertibility of the nonlinear curvature map, not an assertion that the curvature map itself is affine or globally injective. This distinction is correctly made in the proof.

### R65.2-M4. The smooth-jet argument is not merely formal

The finite stationary envelope retains the terminal term until its decay has been estimated. For two actual smooth profiles agreeing through order $M$, the interpolation argument yields an $O(|u|^{M+1})$ action difference. Therefore the action jet through order $M$ depends only on the boundary jet through order $M$.

That is the right way to justify the later triangular recursion. It avoids the common but invalid shortcut of identifying a formal Taylor calculation with a theorem about actual smooth representatives.

### R65.2-M5. The analytic inverse addresses the main infinite-dimensional objection

The v65 analytic argument works in anchored bounded-holomorphic graph spaces and allows curvature to vary. The protected-domain construction prevents the proof from treating differentiation at the boundary of an $H^\infty$ disc as a bounded operator.

For the base derivative $L=A+K$, the initial multiplier $A$ is invertible. On a sufficiently high vanishing tail, the contracted evaluations make $A^{-1}K$ a strict contraction. The finitely many lower Taylor degrees are solved by the invertible blocks $\mathcal C_2,\ldots,\mathcal C_{m-1}$. This supplies a bounded full inverse for $L$.

The nonlinear local inverse is then obtained by a standard contraction/inverse-function argument. I therefore do not regard “the author only inverted the diagonal blocks” as a valid objection to revision 65.

This conclusion should not be inflated. The result is a local biholomorphism on a sufficiently small fixed disc and a sufficiently small neighborhood of a base tuple. Its constants are base- and radius-dependent. It is not a global analytic parameterization of the full table class.

### R65.2-M6. The conditional real-data stability is honestly conditional

The real-law estimate uses an outer bounded analytic prior and loses radius before applying the analytic inverse. This is mathematically the right topology for a stable analytic-continuation statement. The manuscript does not claim same-disc stability from $C^0$ real data without a prior.

Likewise, the finite-flight estimate
$$
C_M(\tau^N+\epsilon)
$$
is a deterministic inversion bound conditional on an estimated density error. It is not a new sample-complexity theorem for the general-period experiment. The manuscript explicitly says so.

### R65.2-M7. The three-obstacle family is an actual geometric realization

The polar perturbation keeps the contact point and tangent fixed while changing the contact curvature independently. For sufficiently small parameters, strict convexity, clearance, and the selected polygon persist. This is materially better than presenting an arbitrary positive Jacobi sequence with no billiard realization.

I therefore find no basis for a harsh review that dismisses the v65 extension as “formal algebra only”.

## 5. Principal objection: the information model is too rich for the claimed level of significance

### R65.2-E1. The theorem begins after most first-order registration has already been supplied

The new theorem fixes a marked polygon containing:

- every collision point $q_i$;
- the phase labels;
- signed tangent and normal directions;
- the lifted closing translation;
- the flight lengths and incidence directions implied by those marks;
- a measured tangent coordinate at every phase.

It then receives two complete conditional density functions on a common two-dimensional square at every phase.

This is not a criticism of correctness. Rich data can lead to interesting inverse problems. The issue is the exceptional-significance claim. The supplied marks already solve the registration and first-order geometry problem that is often central in rigidity. The two-offset law then algebraically recovers the one-variable actions before the boundary inversion starts. The remaining geometric problem is a local inversion of a contractive periodic response.

The paper should therefore not sell “general-period rigidity” without simultaneously stating that the general-period theorem is a **fully registered, marked, phase-resolved local inverse**. The phrase “general period” describes the orbit length, not an unmarked or intrinsically observed table class.

### R65.2-E2. The general-period inverse is local in a stronger sense than the headline suggests

The curvature map is inverted by the finite-dimensional inverse function theorem. The full analytic action map is inverted on a small Banach neighborhood. Neither statement proves global injectivity of the general-period action map.

The whole-obstacle conclusion adds the assumptions that:

- the lattice is fixed;
- obstacle labels are fixed;
- every obstacle is visited by the marked polygon;
- the boundaries are connected closed embedded analytic curves;
- the recovered contact germs lie on the stated local inverse branch.

Under these hypotheses, equality of one open analytic boundary arc on each labelled obstacle propagates around that obstacle by analytic continuation. This is valid, but it should not be counted as a second independent global rigidity mechanism. The nontrivial dynamical inverse is local; the rest is an identity-theorem continuation under fixed registration.

That distinction matters greatly for placement.

### R65.2-E3. “Arbitrary periodic itinerary” is not period-uniform rigidity

The Section 9 argument treats an arbitrary **fixed finite** contact cycle in a compact nongrazing positive-curvature regime. The constants depend on the marked geometry. There is no theorem uniform as:

- the period tends to infinity;
- incidence approaches grazing;
- curvature degenerates;
- clearance collapses;
- the marked coordinates become unregistered.

None of these are missing hypotheses of the printed theorem. I do not require them for correctness. But they limit how much mathematical universality follows from the phrase “general-period inverse”.

The strongest accurate summary is that v65 gives a local inverse for each fixed marked nongrazing finite periodic polygon.

### R65.2-E4. The full Banach inverse is technically sound but conceptually close to a retained criterion once the geometry is contracted

The functional-analytic part is not trivial, but its architecture is now transparent:

1. the billiard geometry supplies a protected contracting half-line;
2. the stationary envelope gives an invertible initial multiplier plus contracted evaluations;
3. finitely many low Taylor blocks are nonresonant;
4. one tail Neumann series plus a finite quotient solves the full derivative;
5. a local inverse-function argument handles nonlinearity.

This is a good argument. It is also very close in structure to the retained contracted-evaluation criterion once the new geometric hypotheses have been verified. The novelty, therefore, lies mainly in proving that the periodic billiard contact map realizes that structure and in computing the signed cyclic blocks.

For a specialist journal this can be a strong contribution. For the very highest general journals, I would expect either a substantially more intrinsic observation theorem, a new obstruction that requires qualitatively new analysis, or a rigidity principle with broader consequences beyond the calibrated local setup.

## 6. Comparison with relevant rigidity literature

I do **not** claim that the v65 theorem is already contained in the marked-length-spectrum literature. The observation models are different, and the present endpoint laws are richer and function-valued.

The relevant comparison is instead one of information and reach.

Bálint, De Simoi, Kaloshin and Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Comm. Math. Phys. 374 (2020), study geometric information extracted from marked periodic-orbit lengths and related asymptotics in open dispersing billiards.

De Simoi, Kaloshin and Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, treat geometric determination in an analytic open-billiard setting under their symmetry/genericity hypotheses.

Finamore and Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983, use an enriched marked-length datum for finite-horizon Sinai billiards and obtain an isometric rigidity conclusion under that observation model.

These papers do not make the v65 theorem redundant. Conversely, merely using different probability-law data does not establish exceptional novelty. The current manuscript needs to explain why its much more highly registered, phase-resolved, function-valued data lead to a conceptual rigidity principle comparable in reach, rather than primarily to a local coordinate inversion after substantial geometry has been supplied.

The present targeted comparison does not establish priority, redundancy, or an exhaustive novelty verdict.

## 7. Article-level architecture is not yet at top-four standard

### R65.2-P1. The principal article aggregates incompatible strongest-case conclusions

The principal article now contains, in close proximity:

- a fully marked two-offset general-period local inverse;
- a weaker-data alternating-channel inverse;
- unknown-lattice and registration conclusions from other hypotheses;
- analytic whole-obstacle continuation;
- finite-observation and charged preparation results from still other experimental designs.

The manuscript often inserts sentences saying that one theorem does not inherit the assumptions or conclusions of another. Those caveats are necessary, but their frequency signals a structural problem: the reader must continuously reconstruct which observation model is active.

A top-four paper should make the information hierarchy visually and logically unavoidable. The current cumulative architecture instead rewards reading the abstract and introduction as a union of best-case features.

### R65.2-P2. Length is not itself the problem; theorem hierarchy is

A 143-page principal article can be justified when one theorem forces that length. Here the length is substantially driven by carrying a historical chain of related reconstructions and observation regimes inside one principal narrative, alongside a 319-page complete technical manuscript and a companion.

I would strongly separate:

1. the decisive new relative-law/contact-inverse theorem;
2. its exact observation model;
3. its direct rigidity consequences;
4. inherited statistical and registration consequences that require different data.

This need not mean deleting mathematics. It means making the top-level theorem structure reflect logical dependence rather than revision history.

### R65.2-P3. The paper should stop using theorem count as a proxy for significance

Revision 65 adds nine statements to Section 9, but several are natural stages of one proof:

- coordinate/Hessian normalization;
- two-offset action extraction;
- stationary envelope;
- graded blocks;
- analytic half-lines;
- analytic inverse;
- local law consequence;
- real-data stability;
- geometric example.

That is good proof organization, not nine independent reasons for exceptional placement.

The exceptional case should be made on one or two central theorems and on what they resolve that was previously inaccessible.

## 8. What would materially change this referee's assessment

The following are **not correctness requirements** and should not be misrepresented as missing hypotheses. They describe the kinds of mathematical development that would address the significance objection.

A substantially stronger case would result from at least one of the following:

1. **less marked data:** remove a meaningful part of the supplied contact registration, tangent-frame, phase-label, or fixed-polygon information while retaining reconstruction;
2. **intrinsic observation:** prove that an intrinsic dynamical/spectral record determines the phase-resolved endpoint laws used by the inverse, or otherwise connect the new coordinate theorem to a natural observation not already registered at every contact;
3. **global inverse geometry:** replace the local curvature/germ branch by a genuine global uniqueness or global stability result on a natural table class;
4. **unified general-period experiment:** extend the finite-preparation/statistical theory to the same general-period observation model without borrowing conclusions from the alternating experiment;
5. **new obstruction-resolution principle:** identify a phenomenon in general periodic billiards that cannot be handled by the positive-mass contraction plus finite-block inversion architecture, and solve it.

Again, I do not ask the author to bolt one of these onto v65 as another revision certificate. Without such a material advance, the more appropriate route is a focused paper at a strong specialist or field-leading venue.

## 9. Disposition of the main questions

**R65.2-D1 — Correctness.**  
No fatal counterexample or mandatory new core proof repair is established in this second examination of the new Section 9. The two-offset extraction, signed cyclic blocks, curvature inversion, smooth envelope, and analytic low/tail inverse remain coherent within the audited scope.

**R65.2-D2 — Novelty.**  
The targeted literature comparison does not establish redundancy. The observation model is different from ordinary or enriched marked-length spectra. I make no adverse priority finding.

**R65.2-D3 — Scope.**  
The strongest accurate description is: a local inverse for a fixed, fully registered, nongrazing marked periodic polygon from phase-resolved two-offset endpoint laws, with conditional analytic stability and fixed-lattice analytic continuation. The weaker-data alternating and acquisition theorems remain separate results.

**R65.2-D4 — Exceptional significance.**  
The current evidence is insufficient for the requested top-four general-journal level. The rich supplied geometry, local inverse branch, and contracted scalar structure materially weaken the claimed universality of “general-period rigidity”.

**R65.2-D5 — Presentation.**  
The principal article is over-aggregated. The strongest conclusions of different observation models should not be allowed to accumulate rhetorically into one apparent omnibus theorem.

**R65.2-D6 — Recommendation.**  
Reject at the requested level. Do not generate another nominal technical repair cycle merely to answer this report. Either materially strengthen the information-to-geometry theorem or recast the work around a sharply focused central contribution.

## 10. Evidence limits

The repository contains extensive native-build, preservation, exact-algebra, and finite numerical diagnostics. Those are useful for provenance and for catching implementation mistakes. They do not prove the infinite-dimensional theorem or exceptional significance.

I have therefore intentionally not treated:

- successful compilation;
- matching source hashes;
- normal/optimized checker parity;
- additional finite rational cases;
- page-render parity;

as independent mathematical reasons to accept the paper.

Conversely, I also do not use the absence of a new finite counterexample as proof of the entire 469-page corpus.

The harsh conclusion of this report is thus narrower and stronger: **the new core appears coherent, but the manuscript still does not make a convincing top-four case because the decisive general-period theorem is a highly marked local coordinate inverse and the article architecture blurs the boundaries among several stronger but incompatible observation regimes.**

## 11. Source map used in this review

- **S1:** papers/A2-v17-boundary-information-coarsening/article/10b_periodic_contact_inverse_v65.tex — complete v65 contact reconstruction module.
- **S2:** papers/A2-v17-boundary-information-coarsening/article/00f_periodic_contact_overview_v65.tex — shared headline theorem and observation model.
- **S3:** papers/A2-v17-boundary-information-coarsening/journal/00_principal_introduction_v61.tex and rigidity.tex — principal claim hierarchy.
- **S4:** papers/A2-v17-boundary-information-coarsening/article/10a_periodic_itinerary_relative_v64.tex — retained general-period forward law and physical normalization used by v65.
- **S5:** papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V65.md — dependency map.
- **S6:** papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V65.md — author response and claim distinctions.
- **S7:** papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V65.md and LITERATURE_CHECK_V65.md — provenance and targeted literature framing.
- **S8:** papers/A2-v17-boundary-information-coarsening/VALIDATION_V65.md — finite diagnostics and native-build scope.
- **R1:** reviews/a2-v64-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md — preceding v64 assessment.
- **R2:** reviews/a2-v65-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md — first independent v65 assessment, consulted but not adopted as authority.

### Literature cited for context

- P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Comm. Math. Phys. 374 (2020), 1531–1575; arXiv:1809.08947.
- J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890.
- D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983.
- S. Bolotin and D. Treschev, *Hill's formula*, Russian Math. Surveys 65 (2010), 191–257; arXiv:1006.1532.

These are contextual comparisons, not a claim that any one of them contains the v65 endpoint-law theorem.
