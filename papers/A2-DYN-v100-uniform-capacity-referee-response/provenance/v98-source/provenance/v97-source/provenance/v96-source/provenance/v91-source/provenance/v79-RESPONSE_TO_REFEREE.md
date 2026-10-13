# Response to the external rereview of A2-DYN revision 78

**Author:** Qian Qi. **Revision:** 79, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v78-external-top4-rereview-2026-10-11/REFEREE_REPORT.md`, commit `e3cd829a662db368b9dbc6db1fb9f0a1be5f60c3`, blob `cb19ddee147ba0978c638e4792d03a8d951272e7`. The new author branch descends from this rereview commit.

**Also considered:** the first v78 report at `44dc4675d03488b404c0d3269b3bac63f3fd1144`, report blob `ebc04c596d8e071dbd7abcb5715ab7fd77104a19`.

**Frozen author baseline:** `5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`, paper tree `0239ebffad6c3b6e75f070e29dd1bfc59c97491e`.

We thank the referee for insisting on separate estimates for true exits and physical volume loss. We retain the original title, triangular Lorentz family, complete actual-return record, exact event, original source normalization, original guard, all arithmetic peaks and zero classes, and the pointwise objective. The new revision proves a uniform reduced-roof third-derivative estimate and estimates the entire angular component of physical volume distortion. It also controls a quantitatively specified regular optical contribution and gives the initial-weight first-exit flux formula. These are estimates and identities on the original source; they are not a declaration that the two remaining pointwise heights have been proved small.

## 1. Optical/coarea volume loss — rereview §§11.2, 16.2; first report §14

The local third-derivative constants in v77 need not remain local. Lemma `lem:v79-stationary-cubic` proves the exact stationary-action identity

`D^3 F[u,v,w] = D^3 S[U_u,U_v,U_w]`.

Differentiating the stationary equations annihilates every term containing a second derivative of the internal contact map. The first contact derivatives already proved in module 177 decay as `q0^depth`. Each flight's cubic action derivative is uniformly bounded using the minimum flight and radius. The resulting cubic depth series is summable. Theorem `thm:v79-uniform-cubic` therefore proves `||D_q^3 F|| <= T_*` on every regular physical word, without any internal-incidence lower cutoff. It does not assume a uniform implicit-function neighborhood near grazing.

Along the canonical flow the momentum angle is constant. This turns the uniform cubic bound into `|chi(Phi_h x)-chi(x)| <= C sqrt(h)`. The physical Jacobian is exactly

`J_h = [omega(Phi_h x)/omega(x)] [chi(x)/chi(Phi_h x)]`,

where `omega=1/|B_m|`. Theorem `thm:v79-volume-factorization` proves that the complete averaged physical volume loss and the complete averaged inverse-twist loss differ, in the ordered `m^2` essential-height norm, by at most `C sqrt(r)`. The proof uses target-direction coarea covariance and the existing unweighted fixed-width bound. It does not multiply a per-word constant by word cardinality, assume a pointwise bound for `p`, or put the angle Jacobian into the residual unchanged.

Thus the angular coarea component is genuinely estimated. The remaining interior component is precisely inverse-twist loss, not an unspecified third derivative of the roof.

## 2. The remaining optical mechanism — rereview §§11.2, 16.2

Proposition `prop:v79-optical-sensitivity` uses the positive optical recursion to show that its denominator is separately affine in every flight length and internal potential. Its logarithmic sensitivities lie in `[0,1]`. The resulting exact differential of `log omega` retains the singular incidence factors explicitly, with uniform depth weights; it introduces no third derivative.

Theorem `thm:v79-regular-optical` proves a complete `C delta^{-1} sqrt(r)` bound for surviving trajectories whose internal incidences stay above `delta q0^(depth/2)`, at every fixed `r <= c delta^2`. The complement is not omitted: its initial source is pointwise dominated by the unchanged bad source `b^(C delta)`. This is a decomposition of the original source, not a replacement by a protected law. The latter density's pointwise height is still not controlled by its fixed-width average. We therefore do not promote the complete optical-loss flag.

## 3. True-exit height and the correct flux measure — rereview §§11.1, 16.1

Proposition `prop:v79-source-exit-flux` derives the exact first-exit formula on regular flow-box domains. The physical outgoing flux must be multiplied by the *initial* guard and by the inverse forward Jacobian. The backward lifetime selects the first exit rather than a later re-entry. An increasing regular exhaustion then recovers the full original exit mass by a decreasing source-level limit at fixed collision count.

This distinction is essential near grazing: the physical density at an exit can tend to zero while the inverse Jacobian diverges, leaving nonzero initial exit mass. The revision does not infer that grazing exits vanish from a zero boundary-density trace. Incidence, competing-hit and section exits are retained, with simultaneous first failures partitioned by a fixed ordering. Artificial exhaustion boundaries are not declared physical; their contributions disappear only through the proved limiting identity.

The formula supplies the oriented coarea/flux interface requested by the referee. A collision-uniform normalized roof-height estimate of that pulled-back flux is still required. Total exit probability is not offered in its place.

## 4. Separate budgets and legal scales — rereview §§16.3, 17.1–17.3

The opening defines the actual starting-fiber measure, killed mass, physical Jacobian and inverse-twist loss. The main endpoint estimate has separate `mathfrak X` and `mathfrak O` terms. It retains the now-controlled angular term `C sqrt(r)` and the previous guard term `C epsilon^{-1} sqrt(r)`.

Theorem `thm:v79-separated-endpoint` gives explicit independent exponents for a possible true-exit bound and optical bound. The width `r=c epsilon^gamma` is chosen with `gamma > max(2,q_X/beta_X,q_O/beta_O)`, before the collision limit. The auxiliary band is enlarged after that limit and the outer `B` last. Corollary `cor:v79-separated-criterion` proves the corresponding separated necessity and sufficiency under the inherited analytic input. The two remaining estimates are not claimed proved merely because this criterion is available.

## 5. Exact occupation and the original guard — rereview §§7, 10–11, 17.4–17.6

Three conventions are made explicit to avoid an unintended strengthening of v78's claims.

The original smooth guard has only incidence and third-disk clearance factors. Section-distance margins occur in exit localization, not in the guard. The opening table states this for every coordinate.

The incidence-normalized matrix is `A=D_A(I-P)`; the actual internal arclength Hessian is `D_c A D_c`. These are different diagonal normalizations, now displayed together with all endpoint conventions and the positive recursion.

The internal occupation identity is a signed current identity. It has not subtracted any positive mass from the original stopped exit term. Its Gaussian surface-amplitude premise and the nonzero occupation-peak leading factors remain unchanged in the complete supplement. No surface-current spectral theorem is imported from a bounded volume-multiplier result. Closing the direct geometric route would not require falsely declaring that alternative surface route solved.

## 6. Precise analytic dependencies — rereview §§9, 17.7–17.9

The opening pins `thm:v49-physical-remainder-local` and `eq:v49-local-limsup` in module 106, with `thm:v49-physical-marked-local` in module 105 as the marked-source input. The exact width and auxiliary-band quantifiers are stated adjacent to their use. The identity `W^1=1`, hence `b^1=p`, is shown from the initial-incidence factor, not assumed.

The geometric journal route retains modules 174 and 177 with their proofs and adds 180–182. The other inherited proofs remain in the complete supplement. The new stationary-action and Jacobian arguments are proved directly, rather than attributed to an external local-limit theorem. The scope of the DPZ literature input remains the retained bounded-multiplier framework; no new singular or surface insertion is attributed to it.

## 7. Scalar closure and downstream statements — rereview §§16.4–16.5

The organizing raw pointwise theorem is unchanged. Neither the true-exit height nor the complete inverse-twist height is yet proved small, so scalar closure and unconditional path, actual-return and likelihood conclusions are not promoted. The same-roof path numerator remains downstream of scalar closure; normalization is restricted to positive reference classes and no arithmetic zero class is divided by.

## 8. Independent review and submission architecture — rereview §§14–17

The new specialist map identifies the stationary cubic cancellation, optical normalization, target-direction covariance and inverse-Jacobian boundary weight as the principal new audit points. No independent human audit or formal proof certificate is claimed.

All 179 inherited cores, every inherited Python source, appendices, bibliographies and provenance are preserved byte-for-byte. Every v78 top-level file is also retained verbatim under `provenance/v78-*`. The complete v78 article is included in the supplement with a scoped reference namespace. The journal itself uses only the two indispensable inherited geometric modules and the three new modules; build receipts and referee correspondence remain outside its narrative.

The v79 qualification workflow checks the new author SHA, controlling review blob, frozen v78 tree, all preserved sources, ordinary/optimized fixture agreement, full journal and supplement builds, and actual recorder coverage of all 182 cores. Old passing runs are not presented as qualification of the new commit. Software checks remain source/build evidence, not continuum proof certification.
