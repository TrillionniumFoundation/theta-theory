# Author mathematical verification of the physical tube source-height revision

This audit concerns the four new complete native bodies 310–313 and their integration with the unchanged physical model and inherited proofs 1–309. It records author-side derivation and cross-checking, including separately written reconstructions. It is not a new referee report, independent human specialist certification or a claim that the final unrestricted theorem is complete.

The complete current proof bodies are in main.tex and core/. The label-by-label dependency map is PROOF_LEDGER.md, with actual compiled locations generated in PROOF_INDEX.json. Full continuous derivations and independent author-side checks are additionally retained in audit/current-iteration/AUTHOR_MATHEMATICAL_CHECK_310_311.md, AUTHOR_MATHEMATICAL_CHECK_312_313.md and 313_OPTICAL_PROOF_AUDIT.md. This document explains the principal mathematical decisions and failure-sensitive checks.

## 1. Physical probability, events and coordinates remain fixed

Every theorem concerns the actual unit-speed triangular periodic disk gas, at radius R in [9/20,47/100]. A collision record has its actual first-hit word and all intermediate collisions. The full physical roof is L_m. The original section is the same union of five rectangles; its two endpoint tests and occupation at collision indices 0 through m−1 remain distinct. The joint event Pi retains the original displacement, return/occupation and collision labels.

The unconditioned collision probability is d alpha d p/(4 pi), and the original section probability has exactly one factor c_*^{-1}, with c_*=91/(10000 pi). Lower tube volumes are measured by the unconditioned probability on the whole physical collision space. They are not restricted by the initial section. Only the original source being bounded carries the section conditioning. This distinction is necessary for a valid volume lower bound and accounts for the single normalization factor in the final height constant.

The endpoint optical coordinate is (alpha,p), p=sin(phi). Stable arclength in 313 is the true Euclidean norm in (s,phi), s=R alpha. The change of physical coordinate, the collision area Jacobian, the momentum determinant and the roof radial Jacobian are all retained explicitly. Neither the stable norm nor the physical clock has been redefined to simplify a bound.

The original guard parameter q_0=47/53 is distinct from the inherited global-minimum contraction q_a=3263680/3263681. The positional resolvent decay is sigma=47/59. In 311 the guard root is named r_g=q_0^{1/4}, avoiding the inherited microscopic-window notation r_0.

## 2. What was already proved, and what is new

Native 281–283 already complete their stated physical curve-growth matching. Native 287/294 provide the uniform actual horizon and anchor geometry. Native 288–293 provide the physical endpoint resolvent, common actual tube and logarithmic optical distortion. Native 265 gives the global equal-momentum uniqueness on a physical word by a convex support argument. Native 297 identifies a regular critical point with the global disk-word minimum.

The latest complete predecessor, 304–309, gives a uniform contraction for every global disk-word minimum, including nonphysical/inactive comparison minima, and a small complete actual observable source outside which every central comparison is physical with all marks exact. Its unconditional measure estimate was a total-mass estimate. Its height estimates for comparison costs had an explicit pressure/optical input. None of those results is counted again as a new contribution.

The new mechanism pays each optical coefficient using the physical volume of a whole neighborhood on which it has two-sided distortion control. This turns complete sums into a geometric volume estimate before taking the roof supremum. Module 310 applies the mechanism to genuinely critical tubes. Module 311 extends it to every point of a full fixed guarded class by a finite-overlap atlas. Module 312 then proves the actual normalized source limit, singular volume and guarded pressure. Module 313 directly completes the two optical assertions, with explicit constants.

## 3. Critical tubes: disjointness, physical volume and witness transport

For 310 the actual critical inverse exists on the entire specified momentum disk. Distinct tubes cannot share a physical initial point: that point determines a unique lifted word, and 297 makes the critical center of that word unique. This establishes physical disjointness across the complete collection, without summing a number of words.

Both sides of the optical distortion estimate are used. With u=|partial_{alpha_0} p_m|^{-1}, a critical tube has lower unconditioned volume rho_epsilon^2 u(0)/(4 C_dist). The lower estimate pays the coefficient u(0); the upper estimate controls the common-roof source. A one-sided upper distortion bound alone would not prove this argument.

Every tube point follows an actual physical path in the already proved common endpoint neighborhood. The all-center closed-flight clearance is transported by the actual segment estimate, including both incident disks, every unvisited disk and changes of nearest center. Incidence and the original section-state collar include the incoming terminal state. A tube meeting an exceptional witness is entirely contained in its explicitly widened witness event. This is a geometric upper-bound device, not an alteration of the original event.

The source bound uses invariance and a union inequality. There is no independence between different collision times. At most two contacts or flights have any given depth. The widened incidence term is squared using (u+v)^2 <= 2u^2+2v^2, and all resulting coefficients are retained.

The conservative common depth D_cv=20,861,442,654 is established by exact rational inequalities, using q_a^{3263680} <= 1/2 and sigma^4 < 1/2. It places clearance, incidence and section widths within the strict ranges required by the native marginal formulas. This finite constant is not advertised as a useful simulation horizon.

## 4. Full guarded atlas: inverse existence, coverage and multiplicity

The class G_epsilon uses the original weighted incidence and clearance margins at every relevant contact/flight and the endpoint cap |p_0|,|p_m| <= 5/6. The cap contains the complete original initial/terminal section. No section-distance guard is added.

Let a_epsilon=delta_* epsilon/16, g=9/40 and rho=rho_epsilon^{at}=g a_epsilon/(8R_+). The already physical endpoint ball has radius a_epsilon. Endpoint momentum changes there are at most 1/64; 5/6+1/64=163/192<17/20 gives endpoint incidence greater than 1/2. The positive Schur matrix therefore has the required lower bound g Id throughout that whole physical ball.

Strong convexity is applied only inside this already physical ball. Minimizing the perturbed action on its closed boundary gives an interior point for every momentum in the stated disk of radius 4 rho. The radial outward derivative is strictly positive on the boundary; the inverse point lies inside the smaller half-ball. This proves an actual physical inverse, not a formal stationary continuation through an unvisited obstacle or grazing collision.

Each original point is assigned to a nearest square-grid point of mesh rho in the two endpoint momenta. A representative for every nonempty (word,grid) pair supplies a tube over the disk of radius 2 rho. Global momentum uniqueness identifies every assigned physical point with that inverse, even if the physical word domain has disconnected components. This proves coverage of the entire G_epsilon.

At a fixed physical initial point there is exactly one word. In each momentum coordinate at most five grid centers can lie within distance 2 rho. Hence at most 25 tubes can contain that point. The bound has no factor equal to the number of words, centers or collision cuts. The full finite word sum at fixed count is taken before the uniform estimate; unattained suprema are bounded pointwise and then approached, rather than assumed attained.

A tube's momentum area is 4 pi rho^2. Multiplication by the original source factor 1/(4 pi) and the lower distortion bound gives

    nu(T_w,z) >= rho^2 u(x_w,z)/C_dist.

Summing these lower bounds and using multiplicity 25 pays the complete positive coefficient sum. There is no section conditioning in this lower volume.

## 5. Roof coarea and normalization

For the endpoint momenta zeta=(p_0,p_m), the endpoint action gradient is R times the signed momentum vector. In the physical inverse coordinates, the radial derivative is r h, with 1/U <= h <= 2R_+, U=320/9. The gradient-angle coordinate differs from arg(zeta) by a reflection, whose absolute angular Jacobian is one.

Polar area contributes r; the roof derivative contributes r h; the original density contributes u/(4 pi c_*). Thus the roof-angle density is u/(4 pi c_* h). The radial cancellation is explicit. Global roof-angle uniqueness on one word handles disconnected physical components. The finite set of regular critical points is bulk-null; its limiting radial contribution is not deleted from coarea and is not confused with a paired trace.

The resulting complete positive-source constant is

    C_at = 25 U C_dist^2 / (2 c_* (rho_epsilon^{at})^2).

It is uniform in radius, collision count, all exact labels, the original roof and every Borel selector 0 <= h <= 1, at each fixed positive epsilon. It grows like epsilon^{-2}; this growth is an actual mathematical limitation on exchanging a guard exhaustion with a collision limsup.

## 6. Complete exceptional-source height and original ordered limits

The six-term V_epsilon(D) in eq:nh-budget retains the widened clearance, incidence and exact-section contributions. The incidence widening has coefficient 16. All original depth indices are included; short central ranges and the shared central contact are treated in the retained indexing conventions.

The actual multiplier is bounded by

    I_m <= H_epsilon = 1 + (4/epsilon) q_0^{3/4}/(1-q_0^{3/4}).

This is the half-guard estimate, valid throughout comparison tubes, and not a newly invented weight. The new full guarded exceptional-source densities obey ||b_D||_infinity <= C_at V_epsilon(D) and ||b_D^I||_infinity <= H_epsilon C_at V_epsilon(D).

For D_m=ceil(theta m), 0<theta<1/2, the complete source estimate was first proved at every finite m,D. Substitution gives V_epsilon(D_m)=O_epsilon(exp(-lambda_b m)), where lambda_b=theta min{|log q_a|/(4*94),|log sigma|}>0. Polynomial m^2 normalization therefore tends to zero after the full physical sums and uniformly over radius, exact labels and selectors. The finite initial segment below D_cv does not affect the limit.

This proves a real normalized limit on G_epsilon. It does not use a fixed-D asymptotic with D silently varying. At an original outer stage B, any auxiliary epsilon_B is fixed before the collision limsup. No guard complement is discarded and no original microscopic roof window is widened.

## 7. Exact central records and the endpoint-work sign

Every global minimum has the same active central physical states on the inherited good class. Its original section occupation and two separate endpoint tests, displacement and collision count are exact. The original end portions remain in the source event and full pushforward roof.

For integers d>=1 and 2d<m, the actual central clock satisfies

    L_d(Y)-L_d(Q) = W_d(Q,Y) + T_clock,d,
    0 <= T_clock,d <= 2R_+ q_a^{floor(d/94)}.

The compensated comparison phase is exp(-i s W_d) Phi_Y. The opposite sign would leave an erroneous 2sW_d. The checker explicitly compares these phases symbolically. The exceptional term has modulus at most one independently of every twist; only the clock term carries |s|. This distinction allows |s| <= exp(lambda m) for any fixed lambda < theta|log q_a|/94. No claim about integrating that estimate over all real frequencies is made.

A full-manuscript scope check found that the predecessor introduction had written d<=m-d for this clock formula. The new introduction now states d>=1 and 2d<m, agreeing with the unchanged complete proof 305. At d=m-d there is no central flight, while the displayed endpoint-work expression need not vanish. This correction is a genuine proof-scope improvement; the historical text remains preserved in its exact predecessor copy.

The new height mechanism removes the pressure dependence of the specified clock/phase/transverse cost densities on G_epsilon. The older conditional results remain readable and retain their unrestricted assumptions.

## 8. The actual inverse-gradient singular factor

The multiplier is precisely I_m/|gradient_q F|, and |gradient_q F|=R|zeta|. For |zeta|>=rho, the bounded source-height estimate pays its volume with factor H_epsilon/(R_- rho).

If a word has a selected point with |zeta|<rho, its actual inverse neighborhood contains the full disk B(0,2rho). Therefore it has a true regular critical center. Distinct selected words have disjoint critical tubes. Witness transport and lower tube volume give a bound on the complete sum of center coefficients by C_dist nu(E^+)/rho^2.

On a radial ray from such a center with roof a_w,

    0 < L(re_theta)-a_w <= R_+ r^2,
    1/(Rr) <= sqrt(R_+) / (R_- sqrt(t-a_w)).

The two-sided distortion estimate is applied before comparing different words at one roof. Integrating the angle gives the exact coefficient in the native proof. Layer cake gives integral_I (t-a_w)^{-1/2} 1_{t>a_w} dt <= 2 sqrt(|I|) for any Borel I of finite measure.

The resulting bound contains both |I| and sqrt(|I|), with exactly one section normalization and the actual physical radius factors. It is an absolutely continuous roof-volume theorem. It is not bounded pointwise at a critical roof. Truncation off finitely many bulk-null critical points defines the nonnegative integral, but does not declare any paired trace zero.

The full roof support has length at most 277m/50. The resulting O(m+sqrt(m)) loss is still paid by the exponential exceptional-source factor after m^2 normalization. A particular variation or pairing term may use this estimate only after a proved charging inequality identifies it with this source.

## 9. Explicit optical comparison and guarded pressure

Module 313 derives DT=-M in true (s,phi) coordinates. Its determinant is c_i/c_{i+1}; both signs and the incoming/outgoing normal convention are checked. The fractional-linear slope map preserves [100/47,170/9] and contracts with derivative at most 47/48. Nested past intervals and time reversal construct the actual invariant lines on M'_R, the full-collision-measure set regular in both infinite directions.

The stable and unstable slopes have opposite signs, and their Euclidean angle has an explicit uniform positive lower bound. The Euclidean area identity includes the ratio of endpoint angles and the collision Jacobian. Positive matrix columns compare the unstable norm to the off-diagonal entry with one uniform factor, rather than a factor raised to the collision count.

The physical optical conjugacy telescopes exactly, retaining the initial and terminal incidences and the conversion s=R alpha. Rational coefficient budgets imply

    (c_m j_m)/30000 <= omega <= 30000 c_m j_m,
    j_1/c_0 <= 6400.

These statements allow arbitrarily small positive incidences. The m=0 stable block is separate from the m>=1 optical statement. The full-measure extension to finite-record bulk integrals does not imply anything about singular traces. Historical 238 remains the qualitative antecedent; this iteration supplies explicit proof completion and constants.

For guarded pressure, the exact identity u=R^2 omega/det(G) and the Schur upper bound give omega <= R_+^2 U^2 u. The endpoint cap gives c_m>=1/2; hence j_m<=60000 R_+^2 U^2 u. The actual atlas coefficient sum has factor 25. Thus 60000*25=1,500,000, yielding the whole guarded word-supremum estimate. No c_* normalization occurs in that unconditioned pressure sum.

This proves the two optical assertions of the retained pressure input and a true guarded pressure theorem. It does not prove the unrestricted Q_* premise or erase the original complement.

## 10. Exact computations and their limits

Three new programs augment nineteen inherited ones. The critical-tube checker uses exact rational enclosures for the depth, margins and normalized source constants. The combined source-height checker independently checks the physical cap, inverse-ball constants, 25-overlap integer bounds, central indices, all partial 94-blocks, floor/ceiling schedules, coarea factors, endpoint-work sign, singular layer cake and pressure normalization. The optical checker symbolically derives the matrix/conjugacy identities and verifies rational coefficient budgets.

The author-side runs retain normal and Python -O commands, output and details hashes. The final complete suite executes all twenty-two programs in both modes. Failures use explicit runtime exceptions rather than removable assertions. Finite matrix examples are algebraic diagnostics, not a substitute ensemble of physical trajectories. Floating diagnostics inherited from earlier modules retain their original finite-sample status.

The native continuous proofs carry every universal quantifier. A passing finite program, a clean PDF or successful CI establishes only the recorded computational/build fact. Actual command evidence, final source fingerprints and visual inspections are described in VALIDATION.md.

## 11. Minimum remaining closure

The source identity still contains the guarded exceptional part, guarded good part and original guard complement. The first now has normalized height payment, including the actual I_m multiplier; the second has the exact central comparison and normalized specified costs. The original shallow portions, genuine same-roof comparison capacity and guard complement remain.

The original shortage is still measured by lim_{B->infinity} limsup_{m->infinity} sup_{R,n,k} m^2 esssup_t (U_low-B,m - K_B P_ng-rB,m)_+, on the original central roof range and in that order. A full closure needs a proved source or capacity mechanism there, the actual paired/singular charging and unrestricted pressure, followed by the full spectral/arithmetic, microscopic conditioning and long-time inverse-Jacobian estimates. The original scientific theorem is retained without an invented completion or a weakened replacement target.
