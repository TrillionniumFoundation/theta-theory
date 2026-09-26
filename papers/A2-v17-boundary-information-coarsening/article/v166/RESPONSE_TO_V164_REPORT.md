# A2 v166 — Response to the v164 independent referee report

Controlling report: `reviews/a2-v164-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md`, commit `e795bc76e458260f0efcc8182c292f19d0610ca0`, report blob `9c1b6c09e6bddf67bdd97d3066638ea33bf4348b`.

New branch: `revision/a2-v166-universal-flattening-2026-09-26`. The first substantive source commit is `9cd08c938a2c4b2b6189c17a41b589cf2bd86711`. Compilation and materialization have their own later receipts; this document does not predict a future commit hash.

## Principal response

The report recognizes the complete first-contact fibre and the collision calculation as substantive advances, while asking for stronger modular reach and fuller scheme-theoretic foundations. We have not replaced the existing results by a weaker claim. All 358 predecessor mathematical environment blocks and all 539 labels of the preservation master are retained. Both complete companion papers and the complete master are regenerated; the new text is not a supplement offered in place of a manuscript.

The revision makes three additional structural steps. First, a projective relative-Hilbert construction represents the horizontal-flat lifting problem on schematically dense tests. Applied on integral coefficient strata, it supplies universal horizontal models for every discrete valuation ring specialization. This representability construction is classical and explicitly attributed; its application does not pretend to classify all higher-contact components. Second, five conic coordinate systems and two primitive division systems give exact presentations for **every arc in the six-dimensional double-contact base**, not only the symmetric collision. Saturation computes its horizontal scheme and all base torsion. Third, the square-zero extension is computed as an algebra extension: its local obstruction sheaf is the structure sheaf of the doubled-line curve, and the actual extension class is its nowhere vanishing section. The algebra is therefore locally nonsplit exactly along that curve.

Further results identify which coefficient directions realize the vertical conics and compute arbitrary ramification of the symmetric collision, including its cyclic-invariant normalization, parity-dependent component multiplicities, and the full torsion filtration. The technical appendix provides the requested patching category, completion/saturation statement, all-fibre exactness, quotient transitions, ramification indices, and descent arguments.

The precise new claims and their proofs are in the five new TeX sections. `THEOREM_INDEX_V166.json` supplies the compiled paper, theorem number, and page for each label cited below. The editorial adequacy of these results remains a question for independent review. Neither finite algebra checks nor a successful build are evidence of journal acceptance or an external audit of the sharp inverse.

## Detailed responses

### 1. Collision terminology rather than an unsupported wall crossing
The controlling paper consistently describes a discriminant collision and horizontal specialization. The new introduction explicitly excludes a variation of stability conditions. Historical filenames and theorem labels are retained for source continuity; they are not mathematical claims. See `sec:all-arcs-v166` and the new introduction's comparison subsection.

### 2. The v165 alias and unambiguous source control
The branch named v165 was not treated as a new manuscript: it pointed to the already materialized v164 work. This revision is in a separate v166 branch descended from the actual latest review commit. It contains new mathematical sources, a new assembler, and new complete manuscripts. The source lock, predecessor hashes, build source commit, and separate remote publication verification distinguish authored material from branch names.

### 3. Set-valued Artin functors and their morphisms
`sec:comparison-details-v166` defines objects `(A,beta)` with a specified map from the completed coefficient base, and morphisms commuting with that map. The embedded deformation functor is covariant on algebras and contravariant on test schemes. It is set-valued because embedded ideals, rather than abstract curves modulo automorphisms, are classified. Nilpotent tests are included.

### 4. One fixed target and an explicit undo diagram
Equation `eq:target-undo-v166` separates the incidence target, its normal-coordinate presentation, and the inverse change before mapping into the fixed complete-quadric target. Both coefficient and incidence projections remain in the diagram. A parameter-dependent congruence is never promoted to one constant target automorphism.

### 5. Formal patching hypotheses, including torsion
`prop:patching-algebraic-v166` specifies a Noetherian affine ring, a finitely generated contact ideal, the ring-theoretic completion, its open complement, and their actual overlap. Bhatt Proposition 5.6(4) and Example 5.8 are used in the flat Noetherian case. Coherent ideal quotients may have contact torsion. Algebra structure and the quotient map are patched, and base flatness is subsequently detected on the jointly surjective flat cover. The argument does not invoke a torsion-free-only gluing theorem.

### 6. Completion and saturation with a finite exponent
`lem:saturation-v166` proves the ideal-quotient identity by a finite-generator kernel calculation. Once the colon chain stabilizes at N, the same exponent works after flat change of rings, including completion. Faithful flatness detects the least exponent. The statement does not claim one uniform N for all arcs.

### 7. Why completion of the reduced graph is reduced
The paragraph following `prop:patching-algebraic-v166` uses excellent complex finite-type rings and geometrically reduced formal fibres, with Stacks Tag 0BJ0. An injection into the product of minimal-prime fraction fields stays injective after flat completion, and the resulting formal fibres are reduced. This is separate from normalization of a special fibre.

### 8. Frame cocycle on triple overlaps
Equation `eq:frame-cocycle-v166` defines the transition as `Theta_j Theta_i^{-1}` and writes its cocycle and undo identities. These hold on ambient targets and all their ideal quotients, including Artin base changes. This supplies the missing descent datum explicitly.

### 9. Algebraic construction before the completed criterion
The second part of `prop:patching-algebraic-v166` begins with an algebraic finite-presentation family and its Hilbert morphism. Recovery supplies a monomorphism. Only then are completed local isomorphisms used to prove etaleness and hence an open immersion. Agreement of reduced closed points is expressly insufficient.

### 10. The retained coefficient projection
Every new graph and arc presentation retains the map to its coefficient base. In the Hilbert--Burch recovery, the recovered polynomial f supplies c; the linear relations alone do not replace that coefficient datum. The five base equations in `eq:all-arc-HB-v166` include the constant r coefficient, which cannot be dropped on a general arc.

### 11. Height two for all Hilbert--Burch fibres
`lem:HB-details-v166` treats e=0, e nonzero on the affine parameter chart, and the point at infinity. At e=0 no codimension-one factor divides all three minors. At e nonzero elimination leaves a nonzero equation with monic z-squared coefficient after one independent linear equation. At infinity G=H=0. Thus no intermediate parameter value is omitted.

### 12. Fibrewise exactness and flatness of the cokernel
The same lemma applies the height-two Hilbert--Burch criterion on every geometric fibre, followed by the base-flat complex criterion in Stacks Lemma 10.99.5, Tag 00MI. It does not infer flatness solely from a constant list of closed-point Hilbert polynomials.

### 13. Ambient ranks and recovery minors
`lem:HB-details-v166` states the ranks five and four from six-dimensional ambient spaces. The corresponding nonzero 5-by-5 and 4-by-4 restriction minors, the selected conic coefficient, and the 2-by-2 bilinear pivot specify the recovery opens. The all-arc theorem uses those opens rather than claiming an unproved global affine chart outside them.

### 14. Doubled conics remain in the family
The restriction-map computation uses the exact sequence of a nonzero plane quadratic, which applies to a doubled line. The extension-class theorem is computed precisely along the doubled-line locus, and the realization theorem explicitly realizes doubled lines by arcs. No reduced-conic substitution occurs.

### 15. The Hirzebruch-surface convention
The technical appendix uses projectivization of lines in `O + O(2)`. The `[1:v]` chart is `Tot O(2)`; the infinity subline is `O(2)`, with normal bundle `Hom(O(2),O)=O(-2)`. This fixes the negative-section sign.

### 16. Connectedness of the proper birational fibre
`lem:exhaustion-v166` gives the Stein-factorization argument, under integral normal finite-type hypotheses, and cites the exact proper-birational connectedness statement. It separates connectedness of support from computation of scheme structure.

### 17. Scheme exhaustion after support exhaustion
The same lemma first obtains the full support from a nonempty proper open-and-closed union. The covering algebraic charts then compute the actual fibre ideals and nilpotents. In `thm:all-arcs-v166`, properness over a local discrete valuation ring upgrades coverage of the entire special fibre by seven coordinate systems to coverage of the full pullback.

### 18. Global associated subvarieties
`cor:associated-v166` glues the local primary decomposition. The associated subvarieties are the two reduced components and the embedded singular-conic plane S. There is no additional embedded subvariety hidden away from the conic charts. The nilradical support S is distinguished from the smaller nonsplitting locus D.

### 19. The square-zero extension class
This is now computed, rather than left as a module identification. `thm:extension-class-v166` represents the class by the map `eA -> 0`, `eB -> 0`, `eC -> eC` from the conormal module. Its local Ext group is `N/CN`, and the class is 1. The resulting obstruction sheaf is `i_*O_D`. Consequently the algebra extension is locally nonsplit at every doubled line.

### 20. The larger Smith exponent and k
`lem:larger-smith-v166` gives the invertible triangular matrix taking `(f,g,fk+r)` to `(f,g,r)`, with determinant one and an explicit inverse. Its use is confined to the relative graph target and undone before fixed-target patching. The independent coefficients of k are restored as smooth formal factors.

### 21. Representability of the product-family Hilbert map
`lem:exhaustion-v166` constructs the embedded family from disjoint contact-supported quotients before invoking Hilbert representability. This produces an algebraic finite-presentation morphism, not merely a product formula for closed points.

### 22. Completed isomorphisms on nonreduced Artin tests
Both `prop:patching-algebraic-v166` and the product argument require isomorphism on all Artin quotients, retaining nilpotents and the coefficient map. Their etale conclusion does not use an argument restricted to reduced fibres or tangent-space dimensions.

### 23. Unlabelled descent
On the finite etale cover ordering distinct supports, changes of order permute factors and their supported quotients. The permutation cocycle gives descent in `lem:exhaustion-v166`. No global ordering is imposed across a collision.

### 24. The explicit horizontal colon
The technical appendix gives `((eA,eB):e^2 C)=(A,B)` and its stabilization. `prop:dvr-horizontal-v166` gives the exact colon description on every arc. The new all-arc theorem uses the five full base equations before saturation, rather than extrapolating the symmetric-path colon.

### 25. Which local rings are discrete valuation rings
The flatness paragraph identifies the relevant nonfield localizations of the base `C[delta]`, not local rings of the threefold. The general argument is torsion-free implies flat over a discrete valuation ring; it does not mistake a higher-dimensional regular ring for a valuation ring.

### 26. Projectivity of the finite quotient
`lem:quotient-projective-v166` tensors a relatively ample line bundle with its translate and kills stabilizer characters by a further power. The descended ample bundle, or equivalently invariant projective charts, proves projectivity despite the fixed divisor. No freeness assumption is inserted.

### 27. All quotient-chart transition maps
Equations `eq:quotient-overlap-first-v166` and `eq:quotient-overlap-second-v166` give the transformations for an arbitrary fractional linear change of direction coordinate. The overlap between blow-up charts is also given. Composition before taking invariants proves the triple-overlap identities.

### 28. Fixed locus and regular invariant rings
The appendix computes the involution as sign change of h or t in the two ordered charts. Its fixed locus is the exceptional divisor, and the invariant rings are the displayed polynomial rings. Smoothness is checked at the fixed locus rather than assumed from a free quotient.

### 29. Strict-transform and exceptional multiplicities
`lem:quotient-projective-v166` distinguishes the ordered strict transform T_0 from the exceptional divisor F_0, and their images S and E. It gives `q^*S=T_0`, `q^*E=2F_0`, and `div(delta)=2S+E`. The factor two is attached to the correct ramification divisor.

### 30. The divisor class O_S(S)
Restricting the principal divisor E+2S to S gives `2 S|_S=-2H`, because E meets S in the doubled-line conic. The torsion-free Picard group of the plane gives `O_S(S)=O(-1)` in the same lemma.

### 31. The ideal of the singular-conic plane
`sec:all-arcs-v166` writes S as `V(q_FG,q_FR)` in the five-dimensional vector space of conic coefficients. These are the two nontrivial first derivatives at P. In the normalized Hilbert--Burch coordinates this is A=B=0. Thus the excess ideal has an explicit modular and coordinate definition.

### 32. Higher Tor sheaves
`prop:dvr-horizontal-v166` proves vanishing of all Tor_i for i at least two using the two-term residue-field resolution. `thm:ramified-v166` computes Tor_1 as the last layer of the full torsion ideal after ramification, not the whole torsion ideal when m is greater than one.

### 33. A cover of the full central fibre
The five evaluation functionals in `eq:five-vectors-v166` are independent, so every conic is covered. Two primitive directions cover every primitive jet. The complete-fibre theorem supplies exhaustion, including the doubled-line intersection. This is the central step in the proof of the all-arc theorem.

### 34. Common fraction field in normalization
`thm:ramified-v166` identifies the exponent lattice generated by `(m,0),(0,m),(2,1)` with the invariant character lattice. The invariant ring is finite, normal, and has the same fraction field, proving that it is the normalization. The appendix also identifies h=t/e inside the common fraction field in the quadratic case.

### 35. Three different normalizations
The introduction and technical appendix distinguish normalization of the total Hilbert graph, normalization after a ramified base change of the horizontal total space, and normalization of an individual fibre. Only the first two specified operations occur. The nonreduced fibre is not replaced by its own normalization.

### 36. Precise monodromy statement
The appendix chooses a positive real base point, a root there, and the explicit positive loop in the punctured analytic disc. It specifies the local system R^2 p_*Q and the two ruling classes. The loop exchanges them; the sum and difference are its invariant and anti-invariant lines.

### 37. Parameter-space semistability versus stable curves
The new introduction and ramification discussion repeatedly identify the space being normalized as a parameter space. In particular even ramification can give a reduced central divisor with singular total space. No statement converts all thick embedded Hilbert curves into stable maps.

### 38. Global interpretation of the extension class
In addition to the local computation requested in item 19, `thm:extension-class-v166` shows that the local generators glue because they are images of one global algebra extension. This canonically identifies its local obstruction sheaf with `i_*O_D` and its image with 1. It does not incorrectly identify the entire global hyperextension group with a one-dimensional vector space.

### 39. Functorial horizontal closure
`eq:horizontal-definition-v166` specifies the schematic closure by the kernel of restriction to the dense open. The functor is defined on schematically dense admissible tests. Flat pulled-back universal families are again the required closure. Arbitrary nonflat base change of an unsaturated family is not declared to commute with closure.

### 40. A universal flattening construction
`thm:horizontal-universal-v166` supplies the relative-Hilbert construction and its universal property. `thm:stratum-flattening-v166` applies it to coefficient strata and proves a finite stratumwise coverage of all discrete valuation ring arcs. This is a global modular construction, while its classical Hilbert representability is fully attributed. It is a universal horizontal modification, not the usual monomorphism representing flatness of the full pullback. No all-contact component classification is inferred solely from representability.

### 41. Modular meaning of the vertical four-space
`thm:conic-realization-v166` proves that every conic through P is reached by a generically nonincident coefficient arc. It separately proves that double-incidence arcs reach exactly S. Thus conics outside S are horizontal for other coefficient directions, explaining why they are vertical on the symmetric collision subbase.

### 42. Moving supports, not varying stability
The new introduction and the last paragraph of the conic-realization section state the distinction. The operation is saturation along a coefficient specialization. No stability parameter, chamber decomposition, or stability-wall equivalence is introduced without a definition and proof.

### 43. Broader comparison with degeneration constructions
The introduction now distinguishes the projective Hilbert construction, expanded relative stable-map degenerations, expanded Quot/coherent-system degenerations, and wonderful compactifications. The literature audit records the exact primary sources inspected and the depth of comparison. No equivalence with logarithmic, expanded, stable-quotient, or quasimap moduli is claimed on the basis of an analogy. The fixed target and the retained coefficient projection are stated explicitly.

### 44. Scope of collision arcs
This restriction has been substantively enlarged. `thm:all-arcs-v166` covers arbitrary six-coefficient arcs through the double-contact point, not just `f=x^2-delta,g=r=0`. Its proof gives exact ideals on seven coordinate systems and their saturated horizontal quotients. `thm:ramified-v166` additionally gives a closed-form normalized model for every ramification order of the symmetric path. The all-arc theorem is a presentation theorem, not a claim of a finite classification of all valuation patterns.

### 45. Independent versus interacting collisions
The old product formula remains a theorem about disjoint independent contacts. It is not used as evidence for interaction. The new miniversal equations allow both supports and residual directions to vary together in B_2; their exact saturation, rather than an independent-product ansatz, governs the interaction there.

### 46. The complete-fibre summary with smaller exponents one and two
The original complete formula, arbitrary larger exponents, component dimensions, intersections, and nilpotence orders remain in the introduction and theorem. `lem:larger-smith-v166` fills in the smooth-factor justification. Higher-contact universal models are added without erasing this stronger explicit classification on its original domain.

### 47. Higher-contact conjectures
All prior higher-contact statements and their conjectural labels are preserved. The new horizontal representability theorem is proved for arbitrary coefficient strata, but is not relabelled as a proof of those component conjectures. The distinction is made in the introduction and after `thm:stratum-flattening-v166`.

### 48. Singular-pencil invariants versus Hilbert classification
The sharp inverse and singular-pencil invariant theorems are retained in their all-pencil form. The new introduction explicitly states that these invariants do not alone give a complete higher-corank Hilbert-fibre classification. No singular-pencil content has been dropped to simplify the boundary story.

### 49. The effective failure image
`prop:effective-horizontal-v166` gives the equivariant horizontal modification and its descended universal property on the effective failure-family image. It identifies exactly where reconstruction is used and checks the property on source-frame torsors. It does not extend the claim to all finite algebras of the same length.

### 50. No internal operation before reconstruction
The same proposition and its concluding paragraph state the order: recover the source and pencil, form their geometric horizontal model, then descend. A closed multiplication table does not choose a specialization direction. This precision does not weaken the all-pencil reconstruction theorem or the new geometric assertions.

### 51. Reorganization without deletion
Paper II has a new introduction organized around universal horizontal models, all-arc equations, the extension class, and ramification. The older quadratic reciprocal-normalization-fibre section moves intact to the appendices. The technical consolidation has its own appendix. Paper I retains its main sharp-inverse route and adds only the effective consequence among the applications. Every predecessor mathematical environment block is checked byte for byte, and all previous front matter is archived. The complete master remains available as a preservation object, not a third submission.

### 52. External independent audit of Paper I
No new external independent audit has been obtained in this revision. We do not relabel an internal dependency review, symbolic verification, or an automated build as such an audit. The sharp-inverse statements and complete proofs are retained, its dependence on boundary results remains absent, and `PAPER_I_AUDIT_HANDOFF.md` records the proof obligations for a genuinely independent reader. This external request remains open and is disclosed in both manuscripts.

### 53. Ballico 1993 full-text comparison
The legitimate publisher record and the attempted publisher PDF retrieval are recorded in `LITERATURE_AUDIT_V166.md`. The PDF attempt did not supply the full text. The theorem/proof-level comparison therefore remains incomplete. The manuscript retains this precise limitation and makes no priority inference from an inaccessible source. The accessible later Ballico comparison already in the repository is not presented as a substitute for the 1993 text.

### 54. Scope of finite verification
The new checker verifies exact polynomial identities, target-coordinate coverage, primary and saturation calculations, selected ramified models, invariant-lattice indices, and quotient transitions. It reruns the inherited v164 chain. The preservation and compilation receipts are separate. All receipts explicitly state that finite computations do not certify the general proofs, global novelty, an independent audit, or journal acceptance. The universal arguments and arbitrary-order normalization proof are in the manuscript, not inferred by induction from a finite test range.

## Review boundary

The response is affirmative in the mathematical sense: it supplies new proofs and a broader specialization theorem while retaining the original scope. Two documentary obligations remain external: a genuinely independent full audit of the sharp inverse and the missing Ballico 1993 full text. The higher-contact component conjectures are not declared solved by the general relative-Hilbert construction. These distinctions are part of the stated claims, not a request to replace the paper by a weaker project.
