# Response to the independent A2 v80 referee report

**Revision:** A2 v82, *Action rigidity with selective detection*  
**Mathematical source:** `80133d376cc28cc8f2555f58324a3285f9dcfb67`  
**New branch:** `revision/a2-v82-selective-detector-rigidity-2026-09-18`  
**Controlling report:** `2edd50e3f97228432ab3c7a1e1f11618f8f45a09`, `reviews/a2-v80-calibrated-records-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`  
**Inherited v81 head:** `8315577eeb8dcc711c4c1c89fc804d132be2e52e`

The latest review found in the repository assesses v80, not v81. Revision 81 already supplied blind clock pencils, projective de-normalization, unpaired regular sheets, a common-clock delayed protocol, and a fixed-source lower bound. We retain those developments and distinguish them from the new results below. This response is not presented as an independent referee endorsement or an editorial decision.

The principal change is a rigidity theorem for **unknown branch-selective detectors**, rather than another estimate around the calibrated affine inverse. In the new model the retained component weight is

\[
a_b(z)\exp(\kappa_b(z)T)(T-W_b(z)).
\]

Only the projective joint matrix of two uncalibrated readings is observed. Five deadlines determine the absolute actions, visible count, channels, relative weights and relative detector rates. The remaining continuous gauge changes only a common weight and exponential factor. Distinct actions are no longer required pairwise: a selective rate separates equal-action components when another unequal-action pair supplies an observable anchor. A finite-degree polynomial log-detector theorem and a nonconvex physical example accompany this result.

The proof of the scalar five-value lemma is complete and elementary: Rolle's theorem gives four derivative zeros, whereas the resulting quartic would have a sum of roots below the first deadline. We neither describe this lemma as a new general tensor-identifiability theorem nor claim that five is the minimal global clock count. Four clocks provide local invertibility; three have an explicit action-changing ambiguity.

## Major comments

### R80-M1 — Scientific misclassification versus unmarked recovery

The new principal theorem does not receive true-component column identities. The visible count is the rank of the observed matrix. Joint spectral projectors recover unnamed components, and clock ratios recover their absolute actions. This goes beyond supervised calibrated scientific labels. It does **not** rename those latent components as reflection words or lattice lifts. The marked billiard companion keeps its semantic marks. See `thm:v82-main`, `lem:v82-components`, and the closing scope section.

### R80-M2 — Ground-truth audit as an auxiliary oracle

The principal theorem and its error-transfer corollary use no audit sample. The acquisition instead supplies two conditionally independent, deadline-invariant readings. This is a declared additional measurement mechanism, not a cost-free replacement of one classifier. Proposition `prop:v82-shear` realizes it with two independent, unknown response curves; every reported value has positive probability on every sheet. The retained audited companion is not misrepresented as audit-free.

### R80-M3 — Endpoint-dependent channels

Both channels U(z) and V(z) may vary smoothly with the endpoint in the headline model. Their invariance across deadlines, conditional independence, full rank and finite capacity are explicit hypotheses. Independently varying channels at each deadline are not included. This separates the new blind experiment from the endpoint-independent calibrated-vector experiment retained from v80.

### R80-M4 — Unknown or omitted components

B is not an input in the blind model, and uniqueness holds against alternatives with another full-rank visible count. Stable counting requires a positive singular-value margin. An additional component above that margin can be learned when both enlarged channels remain full rank. Invisible duplicates and arbitrary rank-deficient/open-world decompositions are not identified. A small extra contribution is covered only as a small perturbation in the stated observation norm. This is a positive unknown-visible-count theorem, not a claim of unconstrained hidden-cause discovery.

### R80-M5 — Simultaneous clock windows

Proposition `prop:v82-physical` gives one fixed-source delayed experiment with D=H+6h and T_j=H+jh, j=1,...,5, simultaneously for every component with 0<=W_b<=H. It does not group trajectories by an audited word. For J polynomial-detector settings replace D by H+(J+1)h. The original adjacent-flight apparatus remains a different experiment and still requires its simultaneous-window condition, stated explicitly in inherited `article/v81/02_geometry_and_experiments.tex`.

### R80-M6 — Elementary raw affine inversion

The leading theorem is no longer the subtraction of two raw subdensities. It discards all joint matrix masses and allows an unknown branch-specific exponential response at every endpoint. Its decisive inverse is the scalar logarithmic-ratio theorem after joint spectral recovery. The old raw inverse remains a useful companion and is not advertised as the new conceptual result.

### R80-M7 — Unknown exposure and missing success/failure masses

The observed projective class permits arbitrary positive endpoint- and deadline-dependent branch-blind rescaling. Success masses, failure counts and scalar exposures may all be absent. More strongly, the new theorem allows branch-selective log-affine attenuation. The gauges are classified exactly in `eq:v82-gauge`. The equal-action obstruction shows precisely when the common action remains hidden despite distinct rates; the three-clock level-set construction shows why the extra detector parameter changes the information requirement.

### R80-M8 — Full powers given as group elements

Corollary `cor:v82-return` starts from projective endpoint matrices, unknown component counts and unpaired regular sheets. It reconstructs the absolute functions and their phase graphs before invoking Bezout. The finite word and its inverse domains are specified. The group identity itself is explicitly elementary. The phase-cover assumption remains; the result is weaker-data recovery of the inputs to the identity, not discovery of an unobserved phase domain.

### R80-M9 — Global section and regular coverage

The return corollary states both regularity and coverage, and the Reeb paragraph assumes an actual smooth global section. Neither is inferred from a matrix rank calculation. The strengthening concerns selective detection, unknown sheets and action coincidences inside covered regular domains. These geometric hypotheses are not counted as removed.

### R80-M10 — A natural contact inverse

The manuscript distinguishes the interpretation of an existing Reeb return action from construction of a suspension. The new three-sheet example is an actual positive-roof exact return system with a fixed source and survival detector; it is not evidence that every contact flow admits the required observations. A universal intrinsic contact invariant without a section/cover is not proved. The positive contribution here is the structured-detector rigidity theorem and its stated contact-return consequence.

### R80-M11 — Strongly marked billiard inverse

The full article preserves the marked billiard theorem, with its obstacle, lift, word, scalar-label and registration data. It does not call this canonical unmarked billiard rigidity. The new action inverse learns unnamed components; the return application can use the union of their canonical graphs without semantic word labels. This is a precise improvement in a different data layer, not a rhetorical removal of marks from the old theorem.

### R80-M12 — Local reference-atlas construction

The old billiard construction remains local in model space. The delayed common-clock construction is class-wide once the elapsed-action bound is given, but it does not construct a universal identifying geometric atlas. These statements are separated in the article and in the dependency ledger.

### R80-M13 — Attack the marks rather than add estimates

The inherited v81 blind theorem removed the supplied component count, audit and cross-gate sheet pairing in its regular return model. Revision 82 extends that recovery to branch-selective detectors and to equal-action sheets distinguished by detector rates. No further semantic billiard marks are claimed to be recovered. The new paper is driven by this information theorem, not by declaring old assumptions closed through an additional error estimate.

### R80-M14 — Fix the non-efficiency source

The full entry retains v81's fixed-source noncongruent-billiard lower bound, which keeps normalized scalar-phase source densities fixed between parameter points. Revision 82 also keeps one fixed normalized source across its positive five-clock protocol and crossed-action example. The larger compensation model and the selective finite-dimensional model therefore differ in detector structure, not by an unnoticed source adjustment.

### R80-M15 — Structured physical detector families

This is the principal new response. Theorem `thm:v82-main` treats unknown branchwise log-affine detectors and identifies the exact continuous gauge. Theorem `thm:v82-polynomial` extends to a fixed degree bound q: q+5 clocks suffice globally, q+3 give local anchor coordinates, and q+2 admit action-changing two-component ambiguity. For q=1 the sharper five-clock proof improves the general sufficient count of six. Proposition `prop:v82-shear` uses a positive phase-dependent survival rate r(p)=r_0+r_1p, not arbitrary endpoint retention. General clockwise compensation is retained only in the larger apparatus class where it belongs.

### R80-M16 — Sharp geometric sampling theory

The new result removes a calibration-sample term rather than claiming a new geometric minimax exponent. Corollary `cor:v82-error` propagates observed joint-density error through normalization and the locally Lipschitz inverse. The prior finite-record and conditional action-risk developments remain in the full article under their own hypotheses. Matching geometric sampling lower bounds are not asserted; the three-clock ambiguity is an exact identifiability statement, not a minimax sampling theorem.

### R80-M17 — Audit sampling design

The inherited v81 text imposes independence of scientific and calibration trials and conditional independence of the audit indicator from the reported label given the retained true component, with positive raw audit probability. This is active in the full v82 manuscript before the calibrated companion is read. Label-selected biased audits without correction are excluded. The new principal theorem has no audit estimator at all.

### R80-M18 — Classical ingredients and new implications

Section 1.1 distinguishes classical latent-class identification, observable operators and joint diagonalization from the new prescribed-deadline scalar inverse. The bibliography adds Bonhomme, Jochmans and Robin, *Estimating multivariate latent-structure models*, Annals of Statistics 44 (2016), 540–563, DOI 10.1214/15-AOS1376. This is a direct methodological predecessor, not a deep-learning-only analogy. Generating-function calculus, the Reeb primitive and Bezout are separately attributed. The comparison is an explicit structural positioning, not an exhaustive priority certificate.

### R80-M19 — Information comparison for billiards

The inherited v81 comparison remains active: regular endpoint generating functions contain local canonical-relation information; a finite atlas is not automatically a global scattering relation, and Euclidean scattering coordinates supply information absent from scalar labels. No unproved global information ordering against marked length/lens/scattering data is asserted. The new clock theorem solves for the action functions under structured detection; the downstream marked geometric certificate is not attributed to the clock algebra alone.

### R80-M20 — One paper rather than a toolkit

The principal article has one theorem chain: normalized matrices -> joint spectral components -> logarithmic clock ratios -> absolute actions modulo detector gauge -> regular return dynamics. Stability, finite-degree detectors, clock obstructions and the physical example all test this same principle. A self-contained core reading edition contains every new proof. The complete entry retains all earlier mathematical inputs as companion regimes; breadth is not reduced by deleting proofs, and the core is not falsely described as the entire inherited manuscript.

## Technical comments

| Comment | Revision and exact location |
|---|---|
| R80-T1 | The principal model explicitly permits endpoint-dependent U,V but requires deadline invariance and conditional independence. The calibrated companion explicitly keeps endpoint-independent C_j. |
| R80-T2 | The unbiased audit design remains active in v81's retained geometric/experimental section; the principal theorem does not use an audit. |
| R80-T3 | `prop:v82-physical` constructs simultaneous delayed windows. The original flow-box simultaneous-window condition remains an additional hypothesis, not inferred from branchwise admissibility. |
| R80-T4 | The principal theorem learns the full-rank visible count; the calibrated companion uses a known finite exhaustive semantic catalogue. Their different scope is stated, including the signal-margin restriction. |
| R80-T5 | The v81 fixed-source physical lower bound is retained. The new positive theorem and example also fix their source across clocks. |
| R80-T6 | The retained calibrated rank obstruction remains scoped to unrestricted action pencils. The new clock obstructions are also stated in their declared observation class, not asserted to realize every billiard deformation. |
| R80-T7 | The full entry keeps the clarified section heading: “Convex twist suspensions: six conditional laws and four raw laws.” The old proof file is unchanged. |
| R80-T8 | The introduction leads with Theorem 1.1 and its single proof chain; companions follow in the integrated manuscript. |
| R80-T9 | The dependency diagram in `PROOF_LEDGER.md` distinguishes the selective projective, common-detector, calibrated, conditional, geometric and finite-observation layers. The inherited one-page data table remains active. |
| R80-T10 | The contact/variational references and the explicit classical attribution are retained. The new statement remains conditional on an actual section and regular cover rather than asserting new general contact topology. |
| R80-T11 | Direct latent-structure/repeated-measurement and nonclassical measurement-error sources supplement the retained calibrated-noise references. Joint diagonalization is specifically attributed to its statistical predecessor. |
| R80-T12 | `prop:v82-stable` displays the rank/minor, joint spectral, residual, weight, anchor, norm, cover and clock margins. The geometric corollary adds mixed-Jacobian, inverse-map and domain collars; density normalization adds a marginal-density floor. |
| R80-T13 | Every listed honest nonclaim remains. The old “catalogue not learned” applies to the calibrated billiard catalogue, not to the new full-rank visible count. Neither statement is allowed to erase the other. |
| R80-T14 | The root README and `A2_REVISION_V82_REVIEW_READY.md` pin the exact mathematical source, controlling review, complete entry, response and build scope. The previous README is archived byte-exactly. |
| R80-T15 | `scripts/build_a2_v82.sh` and the native workflow actually compile both entries and reject unresolved references. Local verification establishes the core build only; the complete native build is not represented as passed before execution. |

## Preserved conclusions and remaining hypotheses

This revision retains the intended general-mathematics presentation and strengthens the positive result under weaker calibration and richer detector uncertainty. It does not replace the manuscript by a no-go discussion. The obstruction propositions identify necessary boundaries of the same positive theorem. All historical mathematical sources remain unchanged, and the full entry keeps every substantive input from v81.

A new independent referee should examine, in order, the joint spectral separation lemma, the five-value root-sum argument, the local inverse and detector-degree extension, and the nonconvex crossed-action realization. The retained marked/reference-atlas and phase-coverage hypotheses remain explicit. This response does not certify acceptance at any journal, formal proof verification, or completion of every broader direction suggested by the referee.
