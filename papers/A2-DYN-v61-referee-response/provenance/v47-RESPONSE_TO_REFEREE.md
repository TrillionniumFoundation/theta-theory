# Response to the external referee: A2-DYN revision 47

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v46-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `ae02860fe7182078ed738d1b23213b3ce8f8afe3` / `b222d90012ac419cd0cfe3b09a21e680da672205`.  
**Reviewed author SHA:** `fb16f06fb2bd205322d4a15979aef5a9a83d4970`.  
**Frozen full v46 paper tree:** `9bea85c50917e3f3de1410cb140cdce9966d6f8d`.  
**New article:** `papers/A2-DYN-v47-referee-response/main.tex`.

We thank the referee for distinguishing the proved protected inverse from the unproved pointwise estimate on the collapsing-margin source. This revision treats an actual class of that boundary source. It retains the title, the original exact four-coordinate return record, the arithmetic transition kernel, all inherited mathematics and the requested raw pointwise target. The new estimate is in essential supremum at scale `m^(-2)`, not merely in mass.

## 22.1. The full collapsing-margin criterion

The full criterion is not yet proved. We do not report otherwise. The new Theorem `thm:v47-endpoint-boundary-smallness` pays the entire signed correction of the endpoint section-decision component. The remaining source is explicitly resolved into incidence, clearance and interior-decision first-defect components. Their signed sum remains to be estimated pointwise. Thus this is a new analytical estimate for part of the boundary, not a claim that an equivalent formulation alone closes the referee's principal objection.

For fixed endpoint depth `J`, protection `eta` on all physical and retained middle margins, and decision width `epsilon`, the new theorem proves

`limsup_m sup_{R,n,k,|a|<=M} m^2 ||d^{eta,epsilon,J,a}_{n,k,m,R}||_infinity <= C M (J+1) epsilon`.

The same upper bound holds for `d-K_B*d` uniformly over every `B>0`. There is no lower bound on the endpoint decision distances in this source: those distances genuinely collapse. Physical incidence and clearance remain protected, and that condition is explicit.

## 22.2. First bad margin and exact positive decomposition

The original guard is factored as `Xi=G E`, where `E` contains the section decisions within distance `J` of the two endpoints and `G` contains every other original factor. The exact identity

`1-Xi = G(1-E) + (1-G)`

is made before pushforward and without normalization. The new pointwise theorem controls `G(1-E)`. The source `1-G` is partitioned disjointly by the first factor strictly less than one, including its smooth transition region, ordered by endpoint distance, margin type and physical index. This gives three actual positive densities with unchanged integer labels.

The first incidence, clearance and middle-decision components have summed masses at most `C epsilon^2`, `C epsilon` and `C epsilon q^((J+1)/4)`, respectively. The proof uses only the already established one-flight bounds and collision invariance. These are recorded as mass bounds, not substitutes for their missing density estimates.

## 22.3. Boundary jumps

The endpoint-decision theorem bounds the density itself. It therefore bounds every finite trace jump of this component by twice the same essential bound and bounds its whole signed inverse at every bandwidth. The intrinsic right-trace convention is unchanged. We do not infer an absolute sum over all jumps, and do not claim that incidence or clearance jumps have been paid by this argument.

## 22.4. Boundary noncritical inverse

The new argument replaces the forbidden crossing of a protected decision boundary by an explicitly permitted finite crossing. It has four steps.

1. The full-occupation spectral local upper bound is extended to smooth initial and terminal functions without compulsory section factors. At a surviving resonance, the physical amplitude is bounded by the product of their masses. Positive finite-time endpoint envelopes yield a `C epsilon |I|` normalized upper bound for a fixed roof interval and a bad decision in a fixed endpoint block.
2. All incidence, clearance and middle decisions remain protected, so the existing endpoint continuation, Hessian and relative source distortion remain available. The omitted section cuts do not change the physical reduced action. Their weak distance derivatives are controlled by endpoint influence, including at corners.
3. On the high-gradient source, choose the fixed roof time `h=c_2 min(eta^3 delta^2, epsilon eta delta)`. The flow of `grad F/|grad F|^2` preserves the word, displacement, collision count and middle occupation. It can change at most `2J+2` occupation summands, and carries a bad endpoint into a slightly enlarged bad endpoint set. Injectivity is proved on the physical word across the section cuts. The source on the upper side is `nu/c`, so an endpoint leaving the initial section creates no normalization error.
4. Coarea compares the original density with at most `4J+5` exact collision-occupation probabilities in a fixed positive roof window. The small-endpoint local bound cancels the window length and gives `C(J+1)epsilon` at the normalized density scale. The index enlargement is only an upper comparison; no averaged-index local theorem is substituted for the original coefficient.

The low-gradient part is completed to normal critical centers while leaving the same endpoint decisions free. Those centers need not lie in the original endpoint section. Their physical collars use `nu/c`, two normal endpoint strips and the same finite occupation allowance. Each physical collar is counted once. The resulting cluster bound is `C(J+1)r`; the low-gradient density is `C(J+1)delta^2`. Letting `delta` tend to zero after the collision limsup completes the endpoint estimate.

This proof does not differentiate an arbitrary source selector, does not sum wordwise second-derivative norms, and does not cross a genuine grazing or competing-hit boundary.

## 22.5. Prescribed thresholds

We give the explicit bandwidth-dependent choice

`epsilon(B)=A B^(-1/12), J(B)=floor(B^(1/24))`.

Both are fixed before `m` tends to infinity. The inherited protected correction is `O(B^(-1/2))`; the new endpoint correction is `O((J(B)+1)epsilon(B))=O(B^(-1/24))`. Their sum is paid at the same common band, leaving only the signed correction of `1-G`.

This is not a prescribed count-dependent protection rate. No threshold in the fixed-window local theorem is claimed uniform in a window, endpoint depth or protection parameter varying with `m`. The unproved count-dependent-rate flag is retained.

## 22.6. Weighted boundary theory

For this endpoint component the source-density estimate holds uniformly for every measurable insertion with modulus at most `M`, including bounded path functions, because of positive Radon--Nikodym domination. This is stronger than an endpoint derivative restriction for this component. The inherited protected regular theorem still requires its stated weak endpoint-gradient budget. Neither statement proves a full weighted incidence/clearance correction or a pointwise roof-conditioned bridge, and neither supplies a Gaussian amplitude for an arbitrary path selector.

## 22.7. Arithmetic form

The full transition kernel `mathcal L_{m,R}` remains the radius-uniform target. At fixed radius the target remains `c mathfrak a_R g_{Omega_R}`, or the equivalent return normalization. Every positive upper comparison includes all surviving resonances. A zero residue is not assigned a conditional law. No unmodulated singleton theorem is asserted.

## 22.8. Specialist audit

No independent human specialist audit has been obtained in this revision. `SPECIALIST_AUDIT_MAP.md` separates the imported collision spectrum and physical continuation from the new finite decision allowance, endpoint envelopes, flow injectivity, occupation count and critical collars outside the section. The finite models check bookkeeping and include negative controls against literal label preservation during a crossing and against deriving height from mass. They are not continuum proofs.

## 22.9. Central route and preservation

The new article-level synopsis points to a three-step route: small endpoint local mass, finite-decision roof transport, and critical completion. Modules 100 and 101 are compiled in the raw-return part after the protected reduction. All 99 inherited core modules and all 123 inherited Python scripts remain byte-identical. The bibliography, every inherited mathematical label, and the compiled 24-statement A--X synopsis remain. The old front matter and response are archived under provenance rather than deleted.

## Technical comments 1--20

Collision count is consistently `m`, return index `n`, bandwidth `B`, protection `eta` or `epsilon`, endpoint depth `J`, and gradient cutoff `delta`. The source measure after free endpoint crossing is explicitly `nu/c`; its endpoint density remains `|F_uv|/(4 pi R c)`. The terminal decision at collision `m` is not a summand of the occupation over `0,...,m-1`.

Every spectral upper bound fixes its window and endpoint family first. `J(B)` is not substituted for `J(m)`. Distance derivatives are weak derivatives; no boundary integration-by-parts identity is invoked for the new arbitrary selector. The high-gradient flow crosses only the named section cuts, while all physical-word and retained middle-decision boundaries remain protected. Global injectivity is checked on the physical word, so the same flowed point is not charged repeatedly at a section cut.

The low-gradient comparison drops compulsory endpoint section indicators explicitly. The finite trace-jump consequence concerns the aggregate density of the paid component, not an uncontrolled absolute sum of intrinsic jumps. Residual mass, the exponential fixed-count height bound, and the qualitative protection diagonal are not combined into an unproved local-scale estimate. Arithmetic, positive-denominator restrictions, and the distinction between source qualification and mathematical verification remain unchanged.

## Reproducibility

The baseline has two successful exact-source runs, `37778372692` and `37778409609`, at `fb16f06fb2bd205322d4a15979aef5a9a83d4970`. Its response artifact is `11550413832`, with archive SHA-256 `1204986e48d22084fc4191c684f6701b18b619b5959ef82eed31644e59dd2ac9`. This is baseline evidence only.

The new workflow checks the v47 event SHA, full controlling report blob, complete ordinary-source tree, inherited preservation, normal/optimized finite-check agreement, native typesetting and proof-page rendering. Each successful build emits its own dynamic SHA/run/PDF receipt. A locally incomplete report checkout is allowed only by an explicit recovery option, is recorded as incomplete, and is forbidden in GitHub Actions. No future run is predeclared successful in this response.
