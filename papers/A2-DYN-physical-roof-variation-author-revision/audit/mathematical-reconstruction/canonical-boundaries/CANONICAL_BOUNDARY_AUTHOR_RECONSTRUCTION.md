# Author reconstruction of the canonical collision-boundary proof

This is an author-side mathematical reconstruction and dependency audit, not a new referee report. It records the proof developed in native-ready modules 324–325 and the exact auxiliary checks accompanying it. It does not represent independent journal review or certification of the raw local limit theorem.

## Exact candidate source

| Source | Bytes | SHA-256 |
|---|---:|---|
| `324_canonical_collision_boundary_budgets.tex` | 27384 | `e366f8323739bf995309192cb183fa791ebb91766b0f49961fec65e4873ab5c0` |
| `325_exact_records_and_marked_roof_fourier.tex` | 15014 | `ebb0f60e0b5ca0d9d5233e1bc26c895ed59a00a51ae0d8285591228da57216c6` |
| `check_canonical_collision_boundaries.py` | 8808 | `fb53ba12e58ec788434b59844c0c8c55e775978bd02ecb3e7bd1b9f0154fde5e` |
| Preserved preliminary checker | 8884 | `b42cfc23414deafd465d0b2892ac3359325447f6622a56d4fd9830ceb974419b` |

The source-level mathematical inputs are the preserved physical differential and optical identities (260, 313, 317), the actual source, curvature, complexity and growth proofs (281–284), the countable interval overlay (319), the absolute logarithmic-variation and radial-turning lemmas (320), and the new complete cap-roof variation theorem (323). Module 324 does not depend on 323; module 325 does. The uncapped source part of 324 does not depend on its later endpoint-cap angular estimates.

## Unchanged physical scope and measure

The radius is always in `[9/20,47/100]`. Every trajectory is an actual regular collision record of the original triangular Lorentz gas. The speed is one, each true flight has length at least `t_*=3/50`, and the roof is the sum of those actual flight lengths. The collision probability remains `dα dp/(4π)`. The original initial-section probability remains `c_*=91/(10000π)` and the conditioned source is its original restriction divided by `c_*`.

A horizontal canonical source fixes the actual momentum `p_i=b∈(-1,1)` and uses source parameter `α_i`. A vertical source fixes the actual collision angle `α_i=a` and uses `φ_i=arcsin p_i`. Its reparametrization does not change the physical set. No exact grazing collision is included as a regular source, and the estimates remain uniform as a positive central incidence approaches zero. The actual visited-grazing endpoint trace is supplied separately by 323 and the preserved optical proof, rather than inferred from bulk measure zero.

For Gauss-angle charges, the original endpoint cap `|p_0|,|p_m|≤9/10` is imposed only as an upper-bound source already containing the original section. For the source branch-supremum theorem, that cap is absent. In 325 the smaller complete cap `5/6` of 323 also contains every original section state. This is verified from the actual section parameters, including the upper root bound `q_R<53/100`: the largest possible original section momentum is at most `10600/12809+1/200`, whose distance below `5/6` is the exact positive rational `6073/7685400`.

## 1. Source geometry and the qualified enlarged class

For a horizontal source, write `c=√(1-b²)` and `θ=α+arcsin b`. The actual current contact is

`q_0=−Rb v_θ^⊥+Rc v_θ`.

The next contact therefore has line representation `q_1=−Rb v_θ^⊥+a_1v_θ`, with `a_1=τ+Rc`. This is an optical decomposition. Its foot generally lies inside the current disk, so the proof explicitly begins the physical first-hit test at the actual exit `q_0`. There is no inserted physical flight and no change in the roof by `Rc`.

For a vertical source, `q_0` is fixed and `q_1=q_0+τv_θ`; thus `a_1=τ` and the line impact relative to this fixed source point is zero. Direct projection of the differentiated flight equation gives, in both cases,

`|ds_1/dθ|=a_1/c_1`, `V_1=κ+c_1/a_1`, and `ρ_1=c_1/[a_1√(1+V_1²)]`.

With `b_1=Rb` for the horizontal source or `b_1=0` for the vertical source,

`(a_1)_s=p_1+b_1 c_1/a_1`,

`(V_1)_s=−p_1κ/a_1−2p_1c_1/a_1²−b_1c_1²/a_1³`.

Both derivatives are uniformly bounded by the already proved `K_mom` of 284. The equality between this coarse bound and the proposed first-image allowance was checked exactly, not numerically. Hence both sources use the **already enlarged** class `Bhat_cv≥max(B_cv,K_mom,2C_*)`, with its own `k0hat, ellhat, Cghat`. Reusing the original smaller-class growth constant would be unjustified; the proof does not do so.

The horizontal first-hit decomposition is exactly 284. For a vertical fan, every other disk is viewed from an exterior point. Its angular shadow has width less than π and intersects the outgoing semicircle in at most one interval. At most two tangencies per candidate disk therefore produce at most `J_f=2N_f+1` genuine first-hit intervals. Different first-entry times cannot exchange order without two disjoint disks sharing the same physical point. The outgoing ray cannot reenter its own current convex disk. This establishes connected actual source intervals, not merely an image multiplicity count.

Each first image is an unstable graph with strictly monotone target `φ_1`, so it meets each homogeneous strip once. Its density retains the factor `c_1`, giving summable source suprema over the infinitely many grazing strips. The vertical weighted budget is

`A_fan=J_f J_len t_*^−1[1+2/(k0hat−1)]`.

The horizontal budget is `A_mom`, already proved in 284.

All collision-circle coordinates on a connected image use continuous unwrapped lifts. The horizontal initial source is cut once at a common seam before its preliminary arcs, already counted in `J_pre`; the vertical source is already an interval. Numerical image seams add no physical branches to `J_f`. If one also splits short images at a coordinate seam, the lifted horizontal span is at most `π/k_-<2πR_-`, so there is at most one such extra cut. It fits the exact retained `J_len=2+ceil(2L_0/ellhat)`. One-flight and terminal images are kept uncut and use their continuous lifts.

## 2. Optical derivative and branch supremum, without a false terminal cut

In `(s,φ)` coordinates, set `B(c)=[[c,0],[κ,1]]`, `P(τ)=[[1,τ],[0,1]]`, and `K(c')=[[1,0],[2κ/c',1]]`. The positive actual collision derivative satisfies

`B(c') D=K(c')P(τ)B(c)`.

The terminal momentum row satisfies `c_l(0,1)B(c_l)^−1K(c_l)=(κ_l,c_l)`. Multiplying these identities proves that the optical matrix used in 324 contains exactly `l` true flights and `l−1` intermediate kicks. There is neither a central kick nor a terminal kick left over. The horizontal initial vector is `(Rc,1)`, and the vertical one is `(0,1)`.

After the first actual flight their transverse displacements are `Rc+τ` and `τ`, both at least `t_*`. Each additional real kick and flight multiplies the positive displacement by at least `1+2t_*/R_+=59/47`. The terminal momentum derivative is at least `k_-` times this displacement. Therefore both source derivatives obey

`A_l^−1≤E_cs σ^(l−1)`, where `E_cs=47/6` and `σ=47/59`.

The exponent begins at `l−1`, because the first true flight supplies the nonzero source displacement. It does not begin at `l`, nor at the marked-foot indexing used elsewhere.

For `l=1`, the finite physical first-hit intervals give the whole branch-supremum sum directly. For `l≥2`, push each exact weighted first image through `l−2` actual iterates, apply the enlarged-class growth bound, and use the terminal cancellation `|dp_l/dell_{l−1}|≥k_-t_*`. The terminal step has at most `J_f` physical branches and is not divided into infinitely many terminal strips. This gives

`H_hor=max{J_pre J_f E_cs, A_mom Cghat J_f E_cs}`,

`H_ver=max{J_f E_cs, A_fan Cghat J_f E_cs}`.

These bound `Σ_I sup_I A_l^−1`, rather than a sum of roots at one target momentum. No pointwise kernel is promoted to a supremum bound. The entire countable source partition and its true weights are used before any exact-label selector. Time reversal is the actual collision involution and preserves the source parameter lengths. Invertibility of the physical map proves that translating the chosen collision disk to the origin produces no word, lattice or mark multiplicity.

## 3. Exact determinant and its essential incidence factor

At an interior collision `i`, let `(X_±,Y_±)` be the positive incoming endpoint rows for the `i` backward and `m−i` forward flights. In the central coordinates `(α_i,φ_i)`, the endpoint derivative matrix, up to an overall sign in each row, is

`[[Rc_i X_-+Y_-, −Y_-], [Rc_i X_++Y_+, Y_+]]`.

The two central `φ` columns have opposite signs because of physical time reversal. Its determinant is the positive sum `A_-Y_++Y_-A_+`. Collision-area invariance gives the exact root weight

`u_x=c_i/[A_- A_+(d_-+d_+)]`, `d_±=Y_±/(Rc_iX_±+Y_±)`.

The rightmost optical factor is the first true flight. Hence `X/Y≤1/τ_first≤1/t_*`, so `d_±≥t_* /(t_*+R_+)`. Therefore

`u_x≤(53/12)c_i/(A_- A_+)`.

The factor `c_i` is mandatory. It is retained throughout the horizontal source proof and gives summability over all original horizontal homogeneity levels. There is no marked-line factor `R^−1` in this canonical formula.

For a vertical source, putting `h_±=1+Rc_iX_±/Y_±≥1` gives

`u_x=c_i/[Y_-Y_+(h_-+h_+)]≤1/(2Y_-Y_+)`.

The countable interval-overlay lemma combines the two source-disjoint half partitions. Their maxima decay at exponents `i−1` and `m−i−1`; their full sums are bounded by the corresponding `H`. Equal endpoints are assigned once and finite exhaustion handles countably many intervals. This proves the all-word product-supremum bound with no component-count or comparison-capacity premise.

## 4. Absolute variation and regular turning

The total variation proof uses the **integral of the absolute one-step log-Jacobian derivative** from 282. It does not infer variation from a Hölder difference estimate. The derivative is at most `U/c+Dhat_B` per target arclength. A target homogeneous segment of length `r` contributes at most `Dhat_1 r^(1/3)`. Adapted backward contraction, with only its endpoint norm comparison, sums this to the fixed `Vhat_J`.

For a half-source of length at least two,

`A_l=[c_l V_l/√(1+V_l²)] J(T^(l−1))/ρ_C`.

The first density is the exact one above. Its grazing factor is retained until after the first-strip summation; its log variation is bounded by the explicit `V_rho,cs`. The terminal cap lies in the central homogeneous strip, and its restriction is an interval by strict momentum monotonicity. The terminal factor has explicit bounded log variation. For length one, direct differentiation gives `(κa_1+c_1)_s=c_1(κb_1−p_1)/a_1`, yielding the stated finite bound without an artificial homogeneous partition. This establishes `Var log A_l≤V_A,cs` on every capped source interval.

The endpoint momentum curve `P=(-p_0,p_m)` has tangent in one quadrant on each two-sided overlap. Its tangent turning is at most one half the sum of the two log variations. One component is strictly monotone, so it crosses the origin at most once. The preserved radial-turning lemma therefore gives the complete punctured regular bound `∫|d arg P|≤2π+V_A,cs`. Both punctured sides of a crossing are included; the separate critical incoming fan is not assigned zero.

Multiplication by the exact coefficient bound `A_coarea≤Λ_circle u_x/(4πc_*R_-²)` gives the desired interior source budget. Summing the two geometric age sequences yields a count-uniform total, and restricting both ages to at least `D` gives its explicit `σ^D` tail.

## 5. Endpoint sources

At `p_0=b≠0`, the exact angular differential is `|b|/(b²+v²)dv` with `v=p_m`; its integral over the endpoint cap is at most π. The actual pointwise physical momentum-root sum `C_mom` therefore bounds that entire horizontal endpoint charge. At `b=0` the regular polar angle is constant on each side of zero, so its regular charge is zero; critical incoming charge remains separate.

At `α_0=a`, parameterize by the true `φ_0`. The endpoint root weight is `u_x=1/(Rc_0X_m+Y_m)≤1/Y_m`. The complete fan branch-supremum sum is bounded by `H_ver`. The tangent of `P` is `(-c_0,±Y_m)` and `Var log c_0≤−2log c_circle` on the original endpoint cap. This proves its uniform angular turning and charge. Time reversal gives the two terminal counterparts. These arguments include `m=1` and retain the actual conditional factor.

## 6. Exact records and twists

The original section consists of exactly five disjoint rectangles. The twenty physical sides are bounded by 324 at each collision index. Source seams are glued. On a regular physical word the lattice displacement is constant and the original occupation count changes only when one of these original section tests changes.

An exact record indicator has jump at most one. A single occupation twist has jump modulus `2|sin(ζ/2)|`. At either endpoint the membership indicator gives jump at most one even for the twist. If several visit surfaces coincide, a telescoping assignment pays one visit change per included surface. The adjacent traces are combined into the actual jump before taking absolute values; they are not charged twice as artificial partition boundaries.

This yields the explicit constants in 325: exact variation `D_base+B_end+B_int`, and twist variation `D_base+B_end+2|sin(ζ/2)|B_int`. The original finite analytic section inequalities have incoming angular sector limits at critical points. Their traces are bounded in modulus by the complete positive critical charge of 323; visited-grazing traces remain zero. All physical boundary charges and exact interior derivatives are retained.

The signed/complex integration-by-parts identity is first established on finite compact regular chamber exhaustions and then passed to the absolutely summable interior and boundary measures. Positive height domination is used only for height, not to infer this variation. The original conditional initial factor gives the stronger actual mass bound `1`. The four nontrivial transform coordinates remain `(ξ_1,ξ_2,ζ,s)` at fixed collision count `m`; the extra constant phase `υm` only labels that fixed count and creates no fifth target dimension.

Finite variation gives the genuine uniform physical-roof Fourier estimate `min{1,D/|s|}`, its translation estimate, and squared tail `2D²/S`. It does not make `1/|s|` integrable, prove the normalized `m²` pointwise local limit, or grant BV/Fourier decay to an arbitrary Borel restriction. Those scope limitations are explicit in the native text.

## Auxiliary execution and what it verifies

`FINAL_EXACT_CHECK_NORMAL.json`, `FINAL_EXACT_CHECK_OPTIMIZED.json`, and their two `FINAL_COMMAND_*.json` receipts preserve the actual commands, return codes, runtime versions, source hashes and all34 exact checks. Both final runs passed; the mathematical JSON and stdout are byte-identical under normal and optimized Python, as independently recorded in `FINAL_NORMAL_OPTIMIZED_COMPARISON.json`. Runtime versions, command flags and timestamps live in the separate receipts, while the mathematical output remains deterministic. The preliminary executed reports and exact earlier checker are also retained unchanged under their original names and `check_canonical_collision_boundaries_preliminary.py`. Checks use explicit exceptions rather than disabled `assert` statements. They verify the physical-to-optical conjugacy, terminal row, determinant, inverse canonical endpoint derivative, positive algebraic inequality witnesses, exact optical constants, first-source derivatives, original section normalization/cap, geometric sums and phase/Fourier algebra.

`COMPILE_SNAPSHOT_CLOSURE.json` and `COMPILE_RECEIPT.json` bind the auxiliary native integration snapshot and actual LaTeX execution. This snapshot is separate from the root author's final build/publication evidence. Neither symbolic checks nor compilation prove the continuous first-hit coverage, the inherited curve-growth theorem, the physical endpoint exhaustion or the raw local limit; those remain mathematical proof obligations addressed in their explicit sources.
