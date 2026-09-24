# A2 revision 146 — response to the two v144 reports

Date: 24 September 2026.

Controlling report: `reviews/a2-v144-independent-harsh-top4-r2-2026-09-24/REFEREE_REPORT.md`, commit `d8376b5dbb47422d93a474add8362d39cf2a68c1`.
Additional report: first independent v144 report, commit `e392e7ba5f04a94444831140b22638ae42aa2972`.
Reviewed v144 publication: `542bcd5027e96ca41568f3eb9c3481dc0f296fed`.
Immediate predecessor actually revised: v145 publication `89edc80cce6fd1801b356313544419d30f377636` (mathematical source `594c308f78e7b25bb970324589967afec3eff185`).
New branch: `revision/a2-v146-referee-proof-completion-2026-09-24`.

The latest report found no new fatal error in the audited reconstruction argument but requested a stronger intrinsic consequence, exact literature anchoring, a coherent publication object, and careful separation of family statements. The v145 revision had already added the constant-pencil curve theorem, separated the manuscripts, pinned Ohta, and supplied the two requested local proof expansions. We preserve those improvements and do not present them as new v146 work.

## 1. Reconstruction and the significance question — report §§1–5, 11, 16

The new principal section `parts/31-moving-pencils-v146.tex` proves an intrinsic theorem for a genuinely nonconstant pencil subbundle over a smooth connected projective base. It does not just pull a constant pencil back to a curve.

For admissible `(B_i,U_i,V_i,R_i)`, with an arbitrary rank-n source bundle and a locally direct-summand rank-two bundle `R_i` in `Sym^2 V_i`, the order-d finite schemes are isomorphic as abstract complex schemes exactly when there are a base isomorphism sigma, one constant linear map g, and an actual bundle isomorphism h with `sigma^* R_2=(Sym^2 g)R_1`. Here `d=n^2+2n-4` as before. The base, its projection, the normal ambient bundle and the two tensor factors are not supplied to the isomorphism.

The new proof has two steps beyond the constant-pencil statement. Lemma `lem:moving-coefficients-v146` recovers a varying coefficient line as a subbundle by contraction with the full right factor, followed by the Pluecker closed immersion. Theorem `thm:moving-reconstruction-v146` shows that, after choosing the one constant left lift, the right bundle maps are unique locally and glue to an actual source-bundle isomorphism, not merely a projective-bundle isomorphism with an unspecified line twist.

This is not justified by invoking the earlier constant-coefficient criterion outside its hypotheses: the required subbundle lemma and its constant-rank argument are proved explicitly. The exterior representation is denoted `F(H)=wedge^p Sym^2 H`; irreducibility is the existing pencil lemma. No incorrect uniform partition label is assigned to this representation.

Example `ex:nonconstant-pencil-v146` is a regular four-variable pencil bundle over P1 with nonconstant unordered cross-ratio and six spectral collision points. Its unmarked finite scheme retains the whole moving pencil, including collision fibres, up to a single global left transformation and base isomorphism. The cross-ratio and discriminant are classical calculations, not themselves novelty claims. The consequence uses the unmarked global inverse rather than merely the fixed-coordinate Grassmannian embedding. Whether this strengthening meets a general-journal significance threshold remains an editorial mathematical assessment, not something certified by a build log.

## 2. What is and is not reconstructed about automorphisms — §§3–4, 14, 15.4

Theorem `thm:automorphism-kernel-v146` gives a split exact sequence of abstract complex automorphism groups. The quotient consists of the recovered triples modulo their common scalar; the kernel is the identity on the associated graded scheme. Its filtration satisfies `[G_i,G_j] subset G_(i+j)`, terminates at `G_(d+1)=1`, and its successive quotients inject into the additive groups of global positive-degree C-derivations of the graded algebra. Derivations of degree zero coefficients are included; they need not be O_B-linear. Surjectivity onto all derivations is not claimed.

The homogeneous presentation supplies a splitting, not an intrinsic preferred splitting of every unmarked presentation. Example `ex:invisible-shear-v146` constructs the genuine nonidentity automorphism `x -> x+y^2` of the order-d scheme, fixing the reconstructed pencil. This prevents an overstatement that the whole finite-scheme automorphism group equals the pencil stabilizer. The result classifies geometric isomorphisms and their residual kernel; it does not claim a moduli-stack equivalence or a description of all deformations over nonreduced bases.

## 3. Sharpness and domains — §§2, 15.4–15.7

The original all-pencil theorem, including singular pencils, remains unchanged. The new family theorem also permits singular fibres. The order is the smallest uniform reconstruction order; it is not asserted to be the least order for each particular pair. The lower-bound proof includes inequivalent constant pencils over every fixed admissible base.

The family inverse has smooth connected projective reduced base. The coefficient-support theorem removes the nontrivial-right-projective-bundle assumption and allows a point. Arbitrary complex base change remains the separately proved relative theorem with its specified relative socle. Absolute nilradicals are not substituted over a nonreduced base. Regularity is needed for spectral descriptions, not for the inverse. Split semisimplicity and simple disjoint poles remain hypotheses of the separate critical-divisor application; definiteness and separated real data remain hypotheses of the real likelihood theorem. Higher Fitting incidence schemes are not replaced by reduced rank strata.

## 4. Orthogonal input — §§6, 15.3

Retain the v145 principal proof `parts/30-orthogonal-input-v145.tex`: Ohta's full-isometry-group setup in §1.1, Proposition 1 and Remark 1 at p.444, dominance Theorem 1 at p.447 with §1.4, and §2.4 Remark 8(i) at p.456. Retain the independent dimension calculation and the explicit distinction between O and SO components. This revision preserves the predecessor's primary-text audit; it does not claim a fresh successful full-PDF retrieval. These results are credited as classical and are not added to the novelty claim.

## 5. Critical schemes and the two local proof requests — §§7–9, 15.1–15.2

The separate applications manuscript retains every mathematical part. In particular `parts/28-projective-critical-divisor-v145.tex` already contains the characteristic-zero rational-point/monic-chart argument and the Hessian coordinate-change formula in the nonreduced critical quotient. Their v145 regression is executed again. No score discriminant is inverted to remove critical collisions. These are inherited resolutions, not a newly claimed v146 solution of the report.

## 6. Publication object and independent contraction results — §§9, 12–13

`geometry.pdf` is the principal submission: the finite inverse, the curve theorem, the new moving-family theorem and automorphism description, and the spectral readout. All proofs on which it depends are internal. `applications.pdf` remains a separate manuscript, not an unrelated supplement required to establish the principal theorem. `archive-v144.pdf` remains a non-submitted research archive preserving the independent operator, web, K3, polarized and boundary developments. No inherited mathematical part is silently dropped or represented as disproved. The operator priority audit remains a separate research obligation and is not used as an additional significance claim for this paper.

All v145 mathematical part files are retained byte-for-byte. Modified root entry documents have explicit v145 copies under `history/v145-root`. The source-bound nondeletion manifest checks both those bytes and inclusion of the predecessor's principal mathematical blocks and labels. Preservation is not an endorsement of every archived theorem.

## 7. Ballico 1993 — §10 and the historical-comparison condition in §16

The six-axis theorem-level comparison with E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI `10.1002/mana.19931630102`, is still documentary-open. Publisher full/PDF routes and exact-title/DOI searches did not supply the complete article, and the available Library search did not contain it. We do not infer theorems from the title or metadata, and we do not substitute the different 1996 article.

The present-paper sides of all six axes are explicit in `LITERATURE_AUDIT_V146.md`: parameter space, exact multiplication map, nonreduced/Fitting scheme, retained infinitesimal structure, families/base change, and inverse conclusion. The 1993 sides remain unverified, without invented theorem numbers or a declaration of either anticipation or nonanticipation. The new moving-family theorem does not itself discharge this documentary obligation. No historical-priority clearance is asserted.

## 8. Evidence and review object — §14

The build executes all twenty-one v145 exact-regression scripts plus the two new v146 scripts, then independently compiles the principal article, the applications manuscript and the complete archive using native LaTeX. The new script checks the nonconstant cross-ratio and its six symmetries, the exact discriminant and six collision points, a nonzero Pluecker tangent and full-right-factor contraction, homogeneous top-degree shear invariance, a filtered commutator, and dimension/rank numerics.

Only a completed source-bound `evidence/BUILD_RECEIPT_V146.json` with `all_checks_pass=true` establishes execution success. The receipt records the mathematical source commit, per-script hashes and statuses, native PDF hashes, inherited-byte checks, label resolution and absence of overfull boxes. Finite regressions are not formal proofs, an exhaustive historical audit, or a journal acceptance certificate. The next referee should independently inspect the new subbundle recovery, normal-bundle gluing and automorphism-kernel proofs as well as the preserved principal theorem.

## Principal strengthening: a single unmarked Artin local algebra

The final v146 theorem `thm:artin-local-inverse-v146` reconstructs every complex pencil from `C[t_ij]/((det T) I_p(gamma_R Sym^2 T)+(t_ij)^(d+1))`, without grading, generators, tangent coordinates, tensor factors or a positive-dimensional support. The order `d=n^2+2n-4` is still smallest uniform. This is not inferred from a reduced determinant cone. The first relation kernel reconstructs the homogeneous cone; its determinant quotient supplies the coefficient module.

The new conceptual ingredient is `lem:coefficient-orientation-v146`: in a multiplicity-one Cauchy summand, a proper nonzero left coefficient space tensored with the full right factor has unequal factor-support ranks. A transposed matrix map exchanges those ranks and cannot identify two ideals of that type. For every pencil the ranks are `(1, binomial(N,2))`, so transposition is excluded even at one point. This is a local intrinsic orientation criterion and applies beyond the particular projective-bundle obstruction used in the earlier proof.

Theorem `thm:unrestricted-moving-v146` consequently removes the source-projectivization restriction from the whole moving-family theorem. The earlier restricted theorem and its proof remain valid special cases and are preserved. Proposition `prop:local-automorphisms-v146` gives the full local tangent-identity kernel: every generator may receive an arbitrary element of the squared maximal ideal. The kernel is a unipotent algebraic group, with affine-space underlying variety of dimension `n^2(length-1-n^2)`, and generally nonadditive group law. This replaces the earlier limitation to curve-supported reconstruction by a proved stronger inverse, not by a weakened claim.

A second new script checks support ranks, three concrete genuine three-variable pencil coefficient spaces against their transposes by exact finite-field evaluation, and general higher-order corrections in a first-relation algebra. All 23 scripts are executed. Sampling does not prove the universal orientation theorem; the representation-theoretic support argument supplies that proof. The Ballico 1993 full-text priority comparison remains documentary-open and is not discharged by this strengthening.
