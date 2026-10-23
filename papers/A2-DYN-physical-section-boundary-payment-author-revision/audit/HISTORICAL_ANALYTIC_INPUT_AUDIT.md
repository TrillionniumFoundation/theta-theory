# Historical analytic inputs behind the current A2-DYN manuscript

## Scope and evidence standard

This is an author-revision dependency audit, not a new referee report and not a claim of independent expert certification. It reads the actual native proof bodies behind the current `inputs.tex`, identifies their precise logical status, and records the remaining closure conditions without deleting previously proved results. It does not infer mathematical validity from CI, branch names, theorem titles, or an author's proof ledger.

The frozen retrieval commit is `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`. Unless an origin is specified separately, paths below are relative to the **short direct archive**:

`papers/A2-DYN-v108-referee-response/`

This direct article tree is `e66a1dec484f419d88c05f12a7e2ec5310430448`; its core tree is `abc9ef989a20f32f7611d4060d65d51d3afd7732`, and its main entry is blob `1250c9acfa01d6eaf5d16e6b4fc03c2d947345e7`. Those objects are **identical** at the actual historical v108 author commit `2144665f89362ca80116f1999d99c80875833dcf`, repository tree `01859d5234f0ddc6807ffa36c378a6a468667446`. Thus the short path is an exact retained native source, not a reconstructed synopsis or an arbitrary higher-numbered branch.

The accompanying `historical-analytic-source-bodies.json` retains 40 retrieved native texts. Every text's canonical Git blob hash was recomputed from its UTF-8 bytes and agrees with the frozen repository blob. `historical-analytic-source-manifest.json` supplies full paths, Git blob IDs, SHA-256 checksums and byte counts. These checks establish source identity, not theorem truth. Historical full builds were not rerun by this audit; the root revision has a separate actual-build record.

The latest author source remains the localized-clearance article at source commit `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` and evidence carrier `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`. The latest controlling substantive external-report artifact remains v115 at `f01482035a0b945b50f1f9c30f30ef35077558dc`, explicitly reviewing author `31792379408c5ace2c09284c2eb22d2331023433`. It does not independently review later native modules 277–332. See `referee-baseline-audit.md` for the complete review and CI identities.

## 1. Frozen historical author identities

| Native historical role | Author commit | Repository root tree | Direct article and article tree |
|---|---|---|---|
| Full occupation-torus spectrum and exact arithmetic intervals, v40 | `d07c73f9db6a27c216fcfb2f32f844d63858c90b` | `1e6d177b2619ade59986124e359758829bc731fa` | `papers/A2-DYN-v40-referee-response`; `647d3d842655bf71e1d64afdc3321b016c190229` |
| Uniform arithmetic transition, v41 | `e8bb719f3100f16cb945ab57c2b3408d19f678dc` | `d3eb59923ab0a59b6dc6f83a9bd94bd9f9d83578` | `papers/A2-DYN-v41-referee-response`; `20e17443eac838e4b1af93dcfb057276540e1340` |
| Complete raw correction criterion, v43 | `f3fb2858b2c10aa2f4f857d56132491a5ea25861` | `94e973a4a4b13f213003869141d0e96cee51cc98` | `papers/A2-DYN-v43-referee-response`; `7e40f2a45fcb0658a938ae93d6473fb108f9ae28` |
| Common Gaussian/arithmetic law in its stated norm, v58 | `b9c8e1f15b65e4843d1321f23ed5b816378b855c` | `8eeccb222c31bce3ca328f0b3f7118840fb922eb` | `papers/A2-DYN-v58-referee-response`; `e7be5ba545bfc80e08c86e3c596e36b483bbedf7` |
| Joint endpoint/incidence localization, v81 | `49957346c784071bf6f2e18a7ae6f2d724254f20` | `0919c3785e33a6a1c7b169f43db23ba88d6df511` | `papers/A2-DYN-v81-referee-response`; `1d68fef5bbd1abc573d8e517e845cf889fe6431c` |
| Historical conditional capacity reduction, v98 | `3727d8bdcf7751f4aaec9b92cf9fa85be1ea0ce2` | `a08ac4da94bea08a23d9150f53a02d43ac71e459` | `papers/A2-DYN-v98-referee-response`; `8f84ba8e9b48373d1acbeac7a3c2d93cb3403bfb` |
| Uniform geometric pressure and uncut source, actual v100 uniform-capacity branch | `7b2d9c999e987f61a38e9fcadd7fd7605192f35a` | `6f3136dc8dddbc9c16b2a14d6114b94dd4ede958` | `papers/A2-DYN-v100-uniform-capacity-referee-response`; `7b8524304ab2eebc935e4c25f74b30d39f80c995` |
| Paired coarea and transverse comparison, v102 | `0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9` | `318f81a76c47dd69b7429bd205223ea5130bede9` | `papers/A2-DYN-v102-referee-response`; `2ac230d86ffc9c4907e57f0e425b80d97971a6c9` |
| Positive interval comparison, actual v104 positive-interval branch | `32e839acc2e190b7c93365aafee96f8e2c32f5e3` | `241833641783b0802ad8e56da69d10a15ca16258` | `papers/A2-DYN-v104-referee-response`; `a40ca28399c3aa4b2a0d76191b2816e47ef79b3a` |
| Fixed positive residence and exact microscopic partition, v105 | `4b7914462a1f34cdfabe959464d20a4bf836d247` | `0ff6be06c99a38b8d8200cef7c11a6bff42b5f16` | `papers/A2-DYN-v105-referee-response`; `5777abf932263abbb7887d19e45be47cc2bf3bf3` |
| Canonical comparison capacity, v108 | `2144665f89362ca80116f1999d99c80875833dcf` | `01859d5234f0ddc6807ffa36c378a6a468667446` | `papers/A2-DYN-v108-referee-response`; `e66a1dec484f419d88c05f12a7e2ec5310430448` |

A numerical version label does not select a source. In particular the separate refs `revision/a2-dyn-v100-referee-response-2026-10-13` at `7f6418223933b49f7ae38563f5a72ca8d1103733` and `revision/a2-dyn-v104-referee-response-2026-10-13` at `7949b93131806711109c8f126d2a56fe37da7b59` do not have their correspondingly numbered direct native article trees. They are not substitutes for the genuine uniform-capacity and positive-interval source commits above. The v113 clearance-geometry branch at `3d91709d12db4a292f212d07304ff036f594d892` likewise does not become a complete native v113 manuscript by its name.

## 2. Direct map from current inputs to native proof bodies

The current `papers/A2-DYN-localized-clearance-records-author-revision/inputs.tex` inherits the following chain.

| Current inherited statement | Actual native proof source | Logical status and limitation |
|---|---|---|
| One-copy physical pairing sheets, common kernels, original coarea density \(A=\omega/(4\pi c_*\chi)\) | `core/196_measurable_segments_and_cutoff_audit.tex`, `thm:v85-segment-map`; `core/244_barycentric_positive_trace_coarea.tex`, `thm:v102-pair-coarea` | Complete written finite-count Borel/coarea proofs, conditional on the already specified smooth endpoint field, optical density and contact-motion geometry. No uniform word-count estimate is inferred. |
| Regular optical variation \(|\partial_u f^\varepsilon|\le C(1+\varepsilon^{-1})AI_m/z\) | Earlier optical chain; explicitly used and justified in `core/211_two_sided_end_layers_and_source_oscillation.tex` and restated in `journal-inputs-v94.tex` | Actual derivative calculation includes both angular-density factors, original smooth guard and \(I_m=1+\sum q_0^{d_i}/c_i\). Later native endpoint proofs retain, rather than replace, its assumptions. |
| Complete uncut source average \(\limsup_m\sup m^2\|A_\rho v^0\|_\infty\le C\) | `core/241_uniform_geometric_pressure_by_finite_tests.tex`, `core/242_uniform_capacity_and_uncut_gradient_moments.tex`, especially `thm:v100-uncut` | Written proof discharges the older separate spectral-capacity premise using uniform geometric pressure and a two-cap layer-cake argument. It still depends on the native fixed-band joint localization theorem and its actual operator/geometric hypotheses. |
| Paired-source average \(\limsup_m\sup m^2\|A_r\mathsf T_\Delta^\varepsilon\|_\infty\le C[\varepsilon^{1/16}+(1+\varepsilon^{-1})\Delta]\) | `core/237_paired_physical_traces_and_scalar_reduction.tex` finite trace comparison; `core/243_uniform_source_recovery_and_positive_trace.tex`; actual short derivation in `core/245_transverse_clock_and_pointwise_trace_height.tex`, `eq:v102-paired-average` | Proved implication from original bad-source averages plus the now uncut \(v^0\) average; it is an averaged estimate. It is not an assumed height bound of the trace itself. |
| Fixed-positive-residence height | `core/253_uniform_positive_residence_persistence.tex`, `thm:v105-persistence` | Complete elementary finite-count inequality, then an inherited analytic consequence at each fixed positive residence. No \(m\)-dependent cutoff or zero-residence conclusion. |
| Original microscopic scalar equivalence | `core/255_exact_microscopic_and_failure_partition.tex`, `thm:v105-original`; exact older scalar is `provenance/v104-main.tex`, `eq:v104-old-remainder` | Complete exact positive partition and conditional equivalence under physical hypotheses and outer costs for the selected paid families. It explicitly does not prove that the remaining microscopic source vanishes. |
| Comparison-pool residual | `core/259_maximal_capacity_and_original_microscopic_residual.tex` | Roofwise maximality is proved within the specified one-sided-window certificate class; abundance of the actual comparison pool is not proved by maximality or finite-count exhaustion. |

The current scalar input states that the retained paid families already have the required outer costs. This is a retained premise of that application, not a theorem that all physical pairs belong to a paid family. The complement is explicitly retained in \(\widetilde H_B\). Empty selected families are permissible in the partition, but cannot improve its unresolved source.

## 3. Module 253: what its proof actually gives

Exact blob: `3e378881e18baaeb511d20bffe4e37d3b1796e77`.

For a fixed physical pairing sheet, let \(a<t<b\), \(\ell=b-a\), \(d_-=t-a\), \(d_+=b-t\). If \(\ell\ge h>0\), then
\[
 \int_{t-h}^{t+h}\mathbf1_{\{a<u<b\}}\,du
 =\min(h,d_-)+\min(h,d_+)\ge h.
\]
The proof multiplies this **finite-count scalar inequality** by the positive physical endpoint minimum \(c^\varepsilon(\xi)\) and the original target selector \(H(\xi,t)\), then uses the one-copy Borel sum and Tonelli. The selector is held at \(t\). Thus
\[
 T_{H,[h,\Delta)}^\varepsilon(t)
 \le h^{-1}\int_{t-h}^{t+h}\mathsf T_\Delta^\varepsilon(u)\,du
 =2A_h\mathsf T_\Delta^\varepsilon(t).
\]
No comparison corridor, angular derivative, independent process, moved label or changed event enters this proof.

The inherited paired-average estimate gives the normalized height at every **previously fixed** \(h,\Delta,\varepsilon>0\). The leading constant does not depend on that fixed \(h\); the finite-count spectral remainder need not have this uniformity. In the original schedule \(\Delta=O(\varepsilon^4)\), \(\varepsilon=A_0B^{-1/12}\), the leading cost is \(B^{-1/192}\). Taking \(h=h_B\) fixed at the outer \(B\)-stage is legal. Taking \(h=h_m\) after choosing the collision count is not a consequence. The complete microscopic contribution remains positive.

This is a real already-existing proof. Repeating the interval-length argument is not a new mathematical contribution.

## 4. Module 255: exact equivalence and its explicit open insertion

Exact blob: `03311bbb2b6a55b8d26f9e9374202ae9b354b83a`.

At finite count the original remainder is disjointly split into:

1. the selected, already paid critical-arm source \(\mathscr C_B\);
2. the selected adaptive source \(\mathscr D_B\), after removing \(\mathscr C_B\);
3. their complement with residence at least \(h_B\);
4. their complement with \(0<\ell<h_B\), the exact original \(\mathsf U_B^{\rm micro}\).

The theorem **assumes** the selected old/adaptive families meet their actual physical reach, overlap and balance hypotheses, with uniform outer costs at most \(C\varepsilon(B)^{-1/32}\). The first two pieces are paid by their named earlier theorems, the third by module 253. Combining the exact split with the older scalar error yields
\[
 \mathcal E_M\le
 \mathcal H_M(\mathsf U_B^{\rm micro})+C_MB^{-1/384}.
\]
The reverse implication uses the inherited necessity and positivity \(0\le\mathsf U_B^{\rm micro}\le\mathsf U_B^{\rm rem}\). It is not a spectral proof of the limit.

The same file's `prop:v105-insertion` explicitly labels the following a sufficient **additional, not presently verified** premise:
\[
 \sup_{B\ge B_0}\limsup_m\sup_{R,n,k}m^2
 \operatorname*{ess\,sup}_{t\in\mathcal C(M)}
 \int c^{\varepsilon(B)}H_B\,\ell^{-\sigma}
 \mathbf1_{\{0<\ell\le\delta(B),\,a<t<b\}}\,d\theta<\infty
 \quad(\sigma>0).
\]
Its implication is sound and elementary: on \(\ell<h_B\), \(1\le h_B^\sigma\ell^{-\sigma}\), so the remaining height is at most \(C_Mh_B^\sigma\). But the proposition does not prove the uniform insertion for the Lorentz source. The current revision must not cite this sufficient criterion as a solved physical residence theorem.

## 5. The paired average is supported by full native arguments, with two different capacities

### 5.1 Physical trace comparison

The finite comparison in `core/237_paired_physical_traces_and_scalar_reduction.tex` (blob `1b675d4bc8ef2b827f20d4d44c2f4688934dcfdc`) is
\[
 |R_H^\varepsilon(t)-T_H^\varepsilon(t)|
 \le C(1+\varepsilon^{-1})
       \int_{t-\delta}^{t+\delta}v^0(u)\,du.
\]
It follows by integrating the derivative of the physical density along the same actual segment, using the positive minimum of its two endpoint traces, and summing through the Borel bijection. The earlier asymptotic theorem in that file retained condition (SC); the finite identity itself did not prove (SC).

Module 245 (blob `d754f0c0f0c401a041ec35b31259aa7aa7cd1d00`) gives the actual paired-average derivation:
\[
 \mathsf T_\Delta^\varepsilon
 \le b^\varepsilon+
 C(1+\varepsilon^{-1})\int_{t-\Delta}^{t+\Delta}v^0(u)\,du.
\]
Average at a fixed \(r\). Translation invariance of the supremum of \(A_rv^0\) pays the convolution with \(2\Delta\). This is not a pointwise bound on \(v^0\) and uses no boundary spectral insertion.

### 5.2 Weighted momentum capacity and pressure

Modules 235, 238–243 give a genuinely different capacity from comparison-pool abundance.

The physical momentum-fiber quantity sums \(I_m\omega/\det K\). The marked stable-Jacobian comparison in module 239 (blob `fc76d61faeb70c0eeca6217c2c09daea4c3b2bde`) bounds it by
\[
 1+C\!\left(P_m+D\sum_i q_0^{d_i}P_iP_{m-i-1}\right).
\]
Here \(P_j\) is an actual physical-itinerary weighted sum; \(D\) counts one omitted physical step. The homogeneous geometric partition sum \(Q_j\) dominates \(P_j\), without forgetting all physical words.

Module 241 (blob `fa0f71468d1f304da492687d949ad00c953402e7`) contains a full author proof of
\[
 \sup_{R\in I,m\ge0}Q_m(R)\le Q_*.
\]
The proof names common geometric growth, whole-cell distortion and a positive pressure fraction carried by long backward cells. It constructs finitely many transverse stable test curves meeting every such long cell, uses an injective branch assignment and a bounded final **physical** one-step subdivision, and concludes
\[
 c_{\rm long}Q_m
 \le C_1D_*C_dN_*C_g.
\]
This is an actual proof body, not a favorable-review assertion. The specialized inputs needing faithful external theorem/application verification are: uniform long-cell constants; distortion between different stable curves in the same cell; stable-convexity/connected test intersections; and the claimed bound on final physical cuts. The proof cites DZUniform and BDPressure at specified lemmas; this audit does not claim an independent reconstruction of those entire source papers. Later native modules, especially 326, must be read in their actual stated scope when deciding which of these interfaces have been strengthened.

Module 242 (blob `5f9109de99f96b533c4d77979e827bb012137784`) then proves
\[
 \mathcal K_m\le
 1+C\left(Q_*+DQ_*^2\frac{2q_0}{1-q_0}\right)=K_*,
 \qquad
 m^6\mathcal K_m\theta_{B_*}^{2m}\to0
\]
for each fixed \(B_*\). Consequently the older separate condition (SC) is **not an additional premise of the later theorem**. Its proof still inherits the genuine joint spectral localization needed for the other cap.

### 5.3 The exact two-cap repair of the uncut source

The two finite-count estimates for the same positive source are
\[
 m^2\int_Ju_v\le Cv^\alpha(L+B_*^{-1})+Ev^{1/2},
 \qquad m^2\int_Ju_v\le Hv^2,
\]
where \(\alpha=129/128\), \(E=C_{B_*}(1+B_*L)m^2\theta_{B_*}^m\), and \(H=m^2K_*\). Positivity gives a valid capped remainder \(\min(Ev^{1/2},Hv^2)\). For \(1/2<p<2\), splitting at \(v_0=(E/H)^{2/3}\) yields
\[
 b^{-p}\min(Eb^{1/2},Hb^2)+
 p\int_0^bv^{-p-1}\min(Ev^{1/2},Hv^2)\,dv
 \le C_p\min\{Hb^{2-p},
 E^{(4-2p)/3}H^{(2p-1)/3}\}.
\]
The displayed exponents sum to one, so the product contains \(m^2\), not an extra uncontrolled polynomial factor. With \(1\le p<129/128\), layer cake is integrable also for the leading cap. The complete source \(I_mz^{-p}\) is finite at each count. It is **not** the power \((I_m/z)^p\). Collision limit precedes enlargement of \(B_*\); the resulting uncut first moment pays the current \(v^0\) average.

Module 243 (blob `9d2fe82694f7b587123653a3c1996c4aad0e854d`) explicitly distinguishes this discharged weighted-capacity premise from the still positive paired short-source height. It states that small difference of endpoint traces does not control their positive minimum.

### 5.4 Actual comparison capacity remains a different problem

Module 250 gives an exact positive comparison for actual angular intervals, with an explicit reach containment, physical overlap \(N\), source trace \(C\), comparison trace \(D\), and accepted fraction \(\min(1,\kappa D/C)\). A physical shortage \((C-\kappa D)_+\) remains. Its hypotheses do not assert that comparison trajectories exist in sufficient quantity.

Module 259 (blob `0b0e3edfc7ffa04160c727a3dc502e0c391af791`) proves the canonical roofwise allocation is maximal **within its one-sided fixed-window certificates** and that the old fixed-family certificates are dominated. It does not establish positive comparison-pool abundance for every original trajectory. Finite-count exhaustion as the comparison window shrinks is explicitly not exchanged with \(\limsup_m\) in the original order.

Calling both quantities “capacity” does not allow a bound for \(\mathcal K_m\) to pay \((U-KP)_+\).

## 6. The true joint spectral dependency behind the critical cap

The critical volume input is not an unsupported blank in current metadata. Its actual native route is:

- `core/183_homogeneous_incidence_localization.tex` (blob `5160d1dc476a2bd3e5746b1f50d2e48b7d2182b0`) specifies the density-relative-to-\(\nu\) anisotropic norms and the real four-coordinate operator \(Q=\mathscr T_{R,(u_1,u_2,b,v)}\). It explicitly imports the full-occupation fixed-band Doeblin–Fortet inequality, power boundedness, moving peaks, Gaussian integrals and multiplier bounds.
- `core/186_joint_endpoint_incidence_localization.tex` (blob `2b858f7a21b41a055a0150ee303513b343b185cd`) proves a two-endpoint/one-incidence insertion using the exact characteristic pairing \(\ell(P_bQ^{m-j}M_sQ^jP_b\mathbf1)\). It uses the physical modulus-one realization, a small **particular vector** \(P_b\mathbf1\), and bounded multipliers; it never assumes the multiplier itself has that small strong norm.
- `core/187_mixed_critical_volume_insertions.tex` (blob `a176583c4af087d4e83669abcd5d6dec87284a66`) integrates the capped inverse-incidence layer cake and sums the true depth weights before the collision limit.

The finite bound in module 186 is
\[
 m^2\nu\{K_m^{\rm c}=k,A_m=l,L_m\in J,
 |p_0|,|p_m|<b,c_j<s\}
 \le Cb^{129/128}s^{17/16}(|J|+B_*^{-1})
 +C_{B_*}(1+B_*|J|)m^2
     \min\{b\rho_{B_*}^{m/2},s^2\}.
\]
Its proof distinguishes the two chronological long-block cases. The actual rational exponent checks are:
\[
 63/64+(7/8)/32=259/256>129/128,
\]
\[
 (7/8)/32+31/32=255/256,\qquad
 255/256+1/32=263/256>129/128,
\]
\[
 (47/32)(31/32)(3/4)=4371/4096>17/16.
\]
These margins are small but positive; all were recomputed exactly. The cap is on the bound for the full characteristic pairing, rather than a falsely isolated signed spectral error.

Module 187 obtains
\[
 m^2\int_Ju^b
 \le Cb^{129/128}(|J|+B_*^{-1})
   +C_{B_*}(1+B_*|J|)m^2b^{1/2}\rho_{B_*}^{m/4}.
\]
Its historical fractional insertion is valid uncut only for \(0<\eta<1/2\), because the finite-count error integrates \(q^{1/2-\eta}\). The historical truncated first inverse-gradient estimate has error \(a^{-1/2}\rho^{m/4}\), so it cannot remove \(a\) before \(m\). Module 242's later quadratic cap is exactly the additional mechanism permitting the uncut first moment. The older limitation should be preserved historically without being falsely advertised as still unresolved after that later theorem.

The chain includes full written dynamical arguments, but remains dependent on the named anisotropic-space geometric and multiplier assumptions. An independent proof audit must test those hypotheses on the same physical map and same exact occupation event. A weak \(C^1\to(C^1)^*\) one-step estimate from module 332 cannot replace this strong, iterable four-record framework without an explicit compatible domain/norm theorem.

## 7. Early joint spectrum, arithmetic and inversion: preserve the achieved scope

### 7.1 Actual fixed-band spectral theorem

`core/84_occupation_cut_power_bounds.tex`, blob `676e74a9d3327046157a6b36b57d3b841894d7a8`, contains full written proofs of:

- at most \(1+Km\) occupation cuts on each already regular inverse curve;
- refinement of unstable matching and explicit extra unmatched costs;
- full real occupation-torus Lasota–Yorke estimates on each fixed roof band;
- a \(B\)-dependent equivalent strong norm with an essential spectral radius strictly below one;
- physical peripheral eigenvectors, exclusion of peripheral Jordan blocks, simple peripheral eigenvalues and uniform decay on compact subsets of the **joint** nonresonant parameter-frequency locus.

Its strong stable estimate subtracts a mean on the **old** inverse piece, preserves its old long ancestor and charges the refined descendants with their polynomial multiplicity. Newly short occupation pieces are not treated as an old never-long family. Its unstable estimate explicitly handles mismatched section cuts. These proof bodies must not be erased by summarizing the whole joint spectrum as “not proved.”

The dependence remains precise: inherited local common spaces, unweighted geometric sums, faithful completion, compact embedding, action/matching and the real preceding-flight/section multipliers. Constants may depend on the fixed band \(B\). The theorem does not claim any estimate at \(B=B_m\to\infty\).

`core/76_finite_cover_inputs.tex`, blob `85f17f4fc89d01f99ce7624a730a9d05e2923b40`, separates the genuine literature interfaces: fixed-cover collision mixing; local spaces; preceding-flight multiplier partitions; connector matching; parameter continuity; and observation geometry. It does not infer mixing from connectedness or use an affine nonisometric change of the reflection law. No mixing rate uniform in finite-cover index is required for the qualitative exclusion in that route.

The more general action-family theorem in module 74 is conditional on its explicitly listed geometric/dynamical hypotheses; its ellipse application is part of the preserved historical mathematical architecture, not authorization to change the current circular physical model.

### 7.2 Exact arithmetic is retained, rather than set to one

`core/85_occupation_holonomy_and_residues.tex`, blob `4980b094be913892f48aecbc5897c2be8c8dc20d`, gives a written no-roof-resonance proof by measurable stable/unstable holonomy, finite almost-sure occupation differences, countability of integer phases and nonatomic symplectic rectangle areas. It does not assume independence of collisions. It identifies the actual endpoint residue
\[
 A_\gamma=|\nu(\eta_Rq_\gamma)|^2
\]
and the common physical covariance curvature at every resonance. Pure-occupation cancellation is not asserted for a mixed displacement or scalar collision phase.

`core/86_fixed_count_arithmetic_local_law.tex`, blob `10bf384eb2b4c5ebb8fa1f584c7d641565affc55`, has a full proof of a fixed-radius exact-label local law for a **fixed positive roof interval**, with finite cyclic residue factor
\[
 \mathfrak a_R(k,n,m)
 =d\,c^{-2}\sum_\ell w_\ell w_{\ell+r},
 \qquad r=a\cdot k+n+hm\pmod d.
\]
The exact zero classes remain zero. A positive denominator is only obtained on allowed classes and within the specified fixed-radius, fixed-interval, central regime. The theorem is not a raw density-value theorem.

`core/87_uniform_resonance_transition.tex`, blob `4d8d66fe6734a8e54d9dca1af673ab8b7cbcdc31`, evaluates the finite moving Gaussian peaks and proves a radius-uniform fixed-interval transition formula. Continued branches with \(|\lambda|<1\) are retained when their damping may be on the inverse-count scale. The roof phase is retained. The interval proof takes \(m\to\infty\) with a fixed Fourier band before enlarging the band. Its diagonal slowly shrinking interval corollary gives no prescribed polynomial microscopic scale and no density value.

Module 124 retains a common physical Gaussian with the finite arithmetic/damping factor and has a global \(L^1\)/total-variation law in its stated source topology. It expressly supplies no polynomial modulus simply from compactness. These are real inherited results at different topologies; neither replacing the raw target by them nor calling them absent is accurate.

### 7.3 Physical arithmetic geometry is not an operator norm theorem

`core/08_joint_arithmetic.tex`, blob `4c0fed9a31b76b24a31280767a147d3785a9e4c6`, builds actual regular periodic excursions with explicit convex-action, clearance, collision-count and section-visit checks. It identifies the relevant periodic annihilator. Its historical section \(Y_R^*\) is explicitly distinguished from the earlier smaller \(Y_R\); the current revision must use the already fixed \(Y_R^*\), not silently transfer statements between them.

The periodic calculations alone do not establish covariance existence, continuity or a transfer-operator norm contraction. Later native covariance/phase and operator theorems supply the appropriate additional arguments. Conversely the early conditional Green–Kubo criteria in module 19 do not mean that every covariance claim remains open: the actual collision covariance, stopped return covariance and nondegeneracy have their separate subsequent native proofs.

### 7.4 Raw inversion interfaces do not prove their own hypotheses

`core/05_residual_inversion.tex`, blob `f568c751a5f4c5dacc5c225d2407277ba3d4a0e2`, is a fully written conditional Fourier inversion theorem. Its hypotheses require the appropriate small-frequency expansion, residual integrable tail at \(o(n^{-2})\), and normalized central edge control. It correctly keeps the splice inequalities involving actual derivative growth; taking the integration-by-parts order large is not by itself a valid choice of compatible exponents.

`core/09_localized_inversion.tex`, blob `f425488bdf151b8113416e3a63595969592d0a99`, proves a conditional localized-edge version with central edge-density and convolution bounds. Remote edge mass separated by a macroscopic scaled distance is paid there. That does not bound all central singular/critical components.

`core/17_operator_bridge.tex`, blob `4d6ce356eca5323e59a9d538722a37c7a7a04da7`, has an explicit quantitative phase-reconstruction/defect estimate and Fredholm index-zero hypothesis in its resolvent criterion. For an unbounded induced twist those are additional inputs, not consequences of merely having a smooth bounded collision observable near zero. This is an older alternative route; it must not be confused with the later fixed-band collision proof already present.

`core/19_raw_closure_contracts.tex`, blob `ff3bb2c0fa578c29bafc44c3a36d14b03b472559`, proves that actual sums of residual \(L^1\) norms and second-derivative total variations give an integrable transform/tail. It does not assert the all-word budgets merely because each finite component has them.

The explicit normal-orbit jump in `core/04_raw_edges.tex`, blob `5255764d8c689ba808469a88352628e95dcfb441`, proves that the full original raw characteristic transform is not globally \(L^1(\mathbb T^3\times\mathbb R)\). This is an obstruction to that particular proof route, not a no-go theorem for the requested raw central LLT. A revision must use justified edge extraction/component inversion or another valid local route, rather than impose a false integrability target on the unchanged full transform.

## 8. The complete raw correction criterion remains an equivalence

`core/93_complete_raw_inversion.tex`, blob `4b82fee9113b149bd3d3ecb6cf1d7a85110d6bdc`, preserves the full exact law and all singular germ components. Its exact correction at every fixed band satisfies
\[
 \mathscr D_{B,n,R}=p_{n,R}-K_B*p_{n,R}.
\]
Using the already evaluated fixed-band arithmetic transition,
\[
 m^2p_{n,R}(k,m,t)
 =\mathcal L_{m,R}(k_1,k_2,t,n)
    +m^2\mathscr D_{B,n,R}(k,m,t)+o(1)
\]
uniformly in the stated central targets. Hence the raw law is equivalent to normalized central essential-height decay of the full correction. This implication has a full native proof; the smallness of the correction is not proved by defining it.

The same file has a finite inverse reconstruction certificate whose bandwidth is allowed to depend on the actual germ derivative budget. It controls the prescribed reconstruction error after the label is fixed. It supplies no uniform polynomial or exponential long-time bound for that budget. Small correction/edge mass does not imply small height. A finite integral certificate is not an asymptotic evaluation of its finite inverse.

These historical residual criteria feed into the later positive source reductions. They should be preserved as exact equivalent routes, not repeatedly renamed and advertised as completion.

## 9. Minimal closure conditions that remain relevant to the new revision

The latest native chain has genuinely paid classes absent in early reports; those contributions must be inherited. In particular, the later guarded critical tube, guard-margin height, all-flight deep clearance, roof-profile and record-norm results cannot be rebranded as new. The following are the smallest still-relevant interfaces, stated without pretending all historical issues remain unchanged.

1. **Remaining positive source in the original order.** Prove a bound for the complete endpoint/shallow or otherwise retained same-pool shortage in the original \(\sup_{R,n,k}\), central roof essential supremum, \(m^2\) normalization and collision \(\limsup\), with outer \(B\) last. A new exact split is useful only if it supplies a new quantitative mechanism for the previously unpaid mass. An actual uniform residence insertion such as the one in module 255 is one sufficient route, not an already established fact.

2. **Faithful spectral/geometric dependencies.** The full fixed-band four-record theorem has native proof bodies and should remain available with their assumptions. To use it in a new stronger bound, verify the precise norms, section-cut matching, singularity budgets, physical source insertion and radius-uniform constants. A different weak test norm or one-step decay cannot simply be iterated, squared or exchanged for the original strong operator theorem.

3. **Raw topology and normalization.** Any full theorem must control the complete raw height error, including singular boundary/critical components, before division by an actual microscopic conditional probability. The fixed-positive-interval arithmetic LLT, global total variation and an absolute smoothing error are insufficient alone. Zero arithmetic classes stay zero, and no conditional law is normalized there.

4. **Quantifiers and error schedules.** Fixed-width constants uniform over previously fixed widths do not give finite-count uniformity when widths move with \(m\). Fixed-band spectral constants do not give a growing-band estimate. Finite-count monotone exhaustion does not commute with a normalized \(\limsup\). Every proposed closure must explicitly pay the relevant finite-count remainder or justify the exchange.

These are constraints on a positive proof of the original objective. They are not authorization to weaken it.

## 10. All-ref direct-source census and preservation

`all435-direct-source-role-census.json` records every A2-DYN-named remote head in the frozen 1304-ref snapshot:

- 435 refs and 219 distinct commits;
- 120 distinct direct `papers` trees;
- 122 distinct direct A2-DYN article trees;
- 93 distinct direct `reviews` trees;
- 91 distinct direct report-directory trees;
- 645 deduplicated Git tree objects read nonrecursively, using 864 Git object/tree commands.

Ref roles are explicitly **hints from names**: 248 revision, 178 review, 4 referee-copy, 4 referee-response, 1 research. Source roles are backed separately by tree/blob entries. Of 122 article trees, 120 have a direct `main.tex` entry; this is not a claim that 120 entry closures have been built or scientifically validated. The two lacking a direct main entry are `papers/A2-DYN-v50-referee-response` (tree `58818bc4835ad9d7d689017174e1d8d6bb51809a`) and `papers/A2-DYN-clearance-jacobi-2026-10-15` (tree `4d30e4984ba0eda27927ee622a22a5cb18a44c55`). Branches whose named version has no corresponding direct source remain distinguishable from those with complete manuscript entries.

The census resolves each ref to its commit/root tree, then direct paper/review trees, then each article's main/core/supplement/model/inputs/response/manifest/build/history pointers and each report directory's direct report blobs. It deliberately avoids recursively expanding enormous duplicated nested histories. The reproducible script is `census_direct_source_roles.py`.

This audit changed no old repository file, branch or review artifact. All working products are in revision preparation for selective integration into the new isolated author revision. The exact old text, failed attempts, conditional statements and counterexamples are retained.

## 11. Novelty check for a proposed new section-multiplier module

A proposed new module asserting the rectangular-section multiplier, its entire occupation phase, or width-controlled strong-to-weak motion would substantially overlap actual native proofs.

- `core/77_section_occupation_local_limit.tex`, blob `de1e1cb30e72b2e744e2ee5190e7f8179fd24b93`, **Lemma `lem:v37-section-multiplier`** already proves the five-rectangle grid qualification: a common nongrazing compact region; a uniformly finite simply connected rectangular partition; connected stable-curve intersections; at most one crossing per horizontal/vertical side; and a uniform \(C\epsilon\) boundary-neighborhood length. It explicitly checks DPZ Lemma 3.3 conditions (1)–(2) and invokes part (b). Equation `eq:v37-occupation-exponential` proves the exact entire strong-space family
  \[
  M_{e^{iv(\eta_R-c)}}=e^{-ivc}[I+(e^{iv}-1)M_{\eta_R}].
  \]
  Equations `eq:v37-joint-operator` and `eq:v37-exact-joint-pairing` already specify source-side occupation and the exact physical marked pairing.

- `core/72_action_norm_details.tex`, blob `4e49f3f18ca5adad32e1d9a1e4fa5af0ccc1b15c`, **Equation `eq:v35-exponent-choice`** already supplies \(p=1/12\), \(q=1/24\), \(\varsigma=1/8\), \(\zeta=1/4\), \(0<\gamma\le1/100\) and the strict multiplier inequality \(\max\{p,\gamma/(1-\gamma)\}<\zeta<1/2\). Lemma `lem:v35-multiplier-detail` proves the piecewise multiplier and its analytic derivatives under the exact partition conditions.

- `core/84_occupation_cut_power_bounds.tex`, blob `676e74a9d3327046157a6b36b57d3b841894d7a8`, **Theorem `thm:v40-polynomial-LY`, final proof paragraph**, already bounds the moving-section symmetric difference by finitely many strips of width \(\delta\), intersects each stable curve in a bounded number of intervals of length \(O(\delta)\), and explicitly concludes
  \[
    \|M_{\eta_R}-M_{\eta_{R_0}}\|_{\mathcal B\to\mathcal B_w}
       \le C\delta^\varsigma.
  \]
  The same file's Lemmas `lem:v40-linear-cuts` and `lem:v40-occupation-matching` already handle the entire occupation itinerary, polynomial subdivision, and unmatched unstable costs. The theorem is stronger than a one-step section multiplier.

An explicit bound on the derivative of the **actual moving section root**, a quantitatively certified relation \(\delta\le C|R-S|\) with the true coordinate changes, or an identified correction of an external-hypothesis gap can add proof completeness. Their contribution must be named as that quantitative/qualification addition. The rectangle-grid proof, entire phase identity and weak width estimate themselves are inherited results and cannot be presented as a new solution of a formerly open obstruction.

The source manifest now includes the complete native modules 72 and 77 as well as 84; all 40 retrieved source texts passed canonical Git blob checks. The reproducible exact-arithmetic script `check_historical_analytic_arithmetic.py` ran successfully with 25 assertions; `historical-analytic-arithmetic-results.json` records their scope as scalar checks only.


## 12. Final integration clarification: native 87, 93, 331 and 322

The final author continuation must inherit more than the existence of a fixed-band proof. Native 87, `thm:v41-uniform-transition` and `eq:v41-uniform-interval`, already gives the radius-uniform exact-label fixed-positive-window law with the full moving-peak reference, uniformly over real roof centers. With the positive analysis width fixed before the collision limit, this theorem evaluates the scalar interval comparison in new module 334. The exact-interval tail controls the sharp cutoff error. The retained finite peak data, including compact parameter supports and the implication that unit modulus forces zero roof frequency, also imply vanishing of the reference roof modulus; moving nonunit peaks must remain included. Thus the comparison and reference terms of that specific bridge are not new open hypotheses. The complete normalized local derivative charge remains its sufficient new physical closing condition. This does not assert the charge is necessary or prove the original raw theorem.

The distinction is implemented by new `lem:ui-reference-modulus`, `prop:ui-inherited-bridge` and `eq:ui-local-charge-suffices`. It uses each finite analysis width before the collision limit and the outer limit last. It supplies neither a collision-dependent shrinking-window law nor a new strong spectral theorem on a growing roof band. Such a strong theorem is an optional alternative route, not an additional prerequisite for this scalar implication.

Novelty must also credit native 93 `thm:v43-labelwise-inversion` and `cor:v43-finite-remainder-certificate`: they already prove exact labelwise inversion after explicit singular-germ subtraction and a finite remainder certificate. Native 331 `thm:av-likelihood`, `cor:av-exact-fourier` and `cor:av-denominator` already provide positive-likelihood reconstruction, its exact finite-band expression and an actual-event denominator certificate. New 334's distinct addition is direct absolutely convergent inversion of the unchanged interval indicator with its explicit label-summed variation tail and specified smooth observation class; it is not the first exact inversion or first conditional certificate.

Native 322 `pc:fan` already proves a zero-clearance leading critical-fan bound with exponent `max(j,m-1-j)`. Its `pc:all-marks` already pays the complete sum over every flight, including shallow ones, after multiplication by `m^2`, with bound `C_pc m^3 (47/59)^((m-1)/2)` tending to zero. New 335's critical contribution is the positive-width `O(delta)+O(theta_r^max(j,m-1-j))` extension. The zero-level longer-side exponential and normalized shallow-fan payment are inherited results, not newly solved obstructions. Neither theorem by itself estimates every nonleading roof remainder.

These clarifications supplement the initial source audit and are reflected in the final author response and historical dependency ledger. They do not alter any archived native proof or report.

## Verification boundary

Performed here: actual native-source reading; exact Git identity comparison for the retained v108 article; independent canonical blob verification for 40 source texts; exact rational checks of key localization and outer-budget exponents; direct all-ref/source-tree census; previous real GitHub run/job/artifact API audit reported separately.

Not performed here: a new full reconstruction of every external dynamical theorem; an independent proof of the original raw pointwise LLT; a historical build of each of the 120 main entries; inference that any CI proves a continuous-geometry or infinite-time assertion. Those exclusions identify the evidence boundary, not a negative recommendation about the original scientific goal.

