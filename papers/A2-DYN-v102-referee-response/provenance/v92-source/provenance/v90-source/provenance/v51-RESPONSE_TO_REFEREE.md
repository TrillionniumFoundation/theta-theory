# Response to the referees: A2-DYN revision 51

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Complete revised article:** `papers/A2-DYN-v51-referee-response/main.tex`.  
**Latest submission-status report:** revision 50, commit `e951b35077f020ae7e5ac711510e49be1faeb4ef`, blob `fa4b5109f7c38d8286f93cd723d6c751378df439`.  
**Controlling mathematical report:** revision 49, commit `11520f4876ca9033c0a0abfbdb0041e1f85c260e`, blob `cad56babdd60f941c0e554dc88c99e90c20335b4`.  
**Completed author baseline:** revision 49, commit `f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`, full paper tree `c583e9f175d668a427759812ac84dcca25259132`.

We thank the referees for separating submission completeness from mathematical closure. This revision supplies an actual complete manuscript and adds proofs on the original pointwise problem. It does not reclassify the v50 charter as a paper, does not rename local variation as uniform density convergence, and does not replace the actual record or arithmetic main term.

## I. The revision-50 submission-status report

The objection is accepted in its exact source meaning. The previous v50 object contains a charter and a provenance-freeze workflow, not a new article. It remains unchanged as history. Revision 51 descends from the report on that object and uses the latest complete article, v49, as the mathematical baseline.

The new directory contains a complete `main.tex`, every inherited core and script, two new mathematical modules, the bibliography, a precise manifest, response, proof ledger, specialist map, publication-status record, native build script, and a manuscript-qualification workflow. The new response and referee-copy branches are intended to identify the same final manuscript commit; their actual refs and runs are checked on publication, not predeclared successful here. The v50 freeze job is not cited as a successful manuscript build.

## II. Pointwise physical-boundary estimates (v49 requirements 1--2)

The new theorem is genuinely in essential supremum, but it is one-sided. Its proof uses additional information beyond the v49 local-variation limit.

For the original normalized coefficient write `P=m^2 p`, `G=L_{m,R}` and use the exact source partition `p=f+d+b`, where `b` is the nonnegative physical-only remainder and `f+d` contains the smoothly protected source and every physically protected section-decision source. The latter two corrections already have pointwise bounds.

Lemma `lem:v51-local-convolution-height` proves

`||K*f||_infinity <= (||K||_1/h + ||K'||_1) ||f||_(1,h,loc)`.

At a fixed reconstruction band, the physical remainder therefore has **smoothed** height `O(epsilon^(1/16)m^(-2))`, using the inherited all-depth local-variation bound. The proof never takes a count-dependent roof window through the collision limit. It makes no inference about the unconvolved physical height from small local mass.

The exact identity

`P-G-m^2 b = m^2[(f+d)-K_B*(f+d)] + (K_B*P-G) - m^2 K_B*b`

then gives, with `epsilon(B)=A_0 B^(-1/12)`,

`limsup_m sup ||P-G-m^2 b^(epsilon(B))||_infinity <= C B^(-1/192)`.

This is Theorem `thm:v51-positive-error`. Since `b>=0`, it proves the uniform arithmetic lower local law `sup ||(G-P)_+||_infinity -> 0`. Local `L1` convergence alone would not exclude thin holes; positivity of this specific source decomposition does.

The same estimate sharpens the still-unproved upper side. The two-sided pointwise law is equivalent to positive height smallness of `m^2 b^(epsilon(B))` in the ordered limit. Because the two first-physical-defect sources are nonnegative, it is also equivalent to the two separate positive-height conditions for incidence and clearance. Possible cancellation between their signed convolution corrections is no longer an alternative way around a remaining positive spike: both smoothed components are already small. This equivalence is proved in `cor:v51-positive-criterion`, not asserted from positivity alone.

We do not claim the final positive-height criterion is proved. Incidence and clearance spikes remain the outstanding upper-density mechanism. No orbit crosses a grazing or competing-hit seam in the new argument. The original two-sided raw endpoint and all its historical criteria remain in the article.

## III. Arithmetic (requirement 3 and technical comments 8--9, 12)

Every uniform formula retains the finite transition kernel `L_{m,R}`. The fixed-radius central specialization retains `c a_R g_{Omega_R}` and the equivalent original-return normalization. No section residue is set equal to one. No law is assigned to a zero transition class.

For the new denominator and minorization results the condition is explicitly **pointwise** positivity `G>=d>0` on the target roof set. This is stronger than merely assuming positive integrated mass. On a fixed radius and central compact set it follows on classes with an arithmetic coefficient bounded below. Uniformly through arithmetic transitions it remains a displayed assumption on the actual finite kernel.

## IV. Independent specialist audit (requirement 4)

No independent human specialist audit has been obtained in this author revision. The inherited thin-layer multiplication, complete occupation-torus spectrum, moving spectral projections, protected geometry, and all-depth source decompositions retain their specialist verification burden. The new elementary convolution and positivity argument is written separately, so it does not conceal a new billiard theorem inside an imported estimate.

The compiled appendix `app:v51-input-map` and `SPECIALIST_AUDIT_MAP.md` provide the requested citation-to-hypothesis map for the inherited piecewise multiplier, including strip complexity, stable transversality, coalescing boundaries, the horizontal grazing cuts, the common exponent choices and the physical meaning of the image-side clearance envelope. These maps identify the already stated proof locations; they are not a claim of independent certification of the cited continuum theorem.

## V. A reusable principle and its application (requirement 5)

Proposition `prop:v51-positive-principle` is stated for arbitrary families of densities, real reference functions, fixed reconstruction kernels and positive remainders. Its assumptions are separately testable: fixed-band reference convergence, a uniform correction for the controlled source, and a locally small positive remainder with a window-independent limiting constant. Its conclusion is a uniform positive-remainder representation of the error and a one-sided pointwise local law.

The billiard application checks each assumption against a named inherited theorem. This is a reusable real-analysis principle, not a claim that its dynamical assumptions have now been verified for arbitrary singular hyperbolic systems. The paper's full source and fixed exact return index remain unchanged.

## VI. Topology and conditioning (requirement 6; technical comments 6--7, 10--11)

The theorem hierarchy now states both the retained full-source local-variation law and the new one-sided essential-supremum law. It distinguishes them from the still-needed two-sided law. The main title and raw-return target are retained.

Corollary `cor:v51-lower-denominators` gives `p>=d/(2m^2)` almost everywhere on positive-reference target sets. Integrating it gives a lower probability for every measurable subset of those sets, even after the count is chosen and even if the set is very small. It does not provide an upper asymptotic on arbitrarily shrinking windows.

For a fixed interval with `G>=d`, let `delta_m=sup||(G-P)_+||_infinity` and `e_m(h)` be the inherited local-variation error. Theorem `thm:v51-conditional-minorization` proves that the true conditional roof law dominates

`alpha_m Q`, where `alpha_m=(1-delta_m/d)/(1+e_m(h)/d) -> 1`

and `Q` is the normalized arithmetic reference on that exact interval. Consequently `P_cond=alpha_m Q+(1-alpha_m)S_m` for a probability `S_m` on the same roof interval. The reverse likelihood divergence and reverse relative entropy tend to zero. These conclusions are stronger than total variation alone and do not change the conditioning event.

A single-roof equation has probability zero. The denominator assertion is a density lower bound, not a probability assigned to that equation and not a single-roof path bridge. A same-roof path numerator has not been supplied. The article includes an explicit positive-spike example showing that reverse likelihood convergence does not imply forward likelihood control or an upper density bound.

## VII. Short route, retention, and literature (requirements 7--8)

The introduction gives a direct route: local-convolution height lemma, positive source identity, original lower law, positive concentration criterion, then exact-window minorization. The mathematical dependencies are modules 93, 99, 103--107; the new argument does not require re-reading the full historical route to understand its logical step.

All 107 inherited core files and all 135 inherited Python files are byte-identical, as are the bibliography and compiled theorem appendices. The former main source, manifest, response, proof ledger, status and validation documents are archived under provenance. No previous theorem is removed or downgraded.

The literature comparison remains theorem-specific. DPZ treats cell-index mixing local limits with endpoint observables and deformed tables; Dolgopyat--Nandori gives an abstract suspension-flow local CLT including finite-horizon billiards. Neither is invoked here as a theorem giving the original exact-return density's new uniform lower inequality. The added inference uses this article's own positive raw source partition and all-depth physical local-variation bound. No claim of a historically first general local limit or of automatic top-four significance is made.

## VIII. Remaining technical comments and execution evidence

The reconstruction band `B`, auxiliary spectral band `B_*`, collision count `m`, and margin `epsilon(B)` are kept distinct. At every fixed band the collision limit precedes removal of the auxiliary regularization. The finite physical error remains `m^3 rho^(m/2)`; it is not replaced by the section-decision error. Clearance is still observed at collision `j+1`, and occupation still sums exactly times `0,...,m-1`. The source factor `1/c` is included once in the inherited physical remainder. The finite previous-disk contribution and homogeneity details are recorded in the input map.

The new read-only workflow verifies both frozen reports, the complete baseline tree, unchanged inherited mathematics, every TeX inclusion and reference, payload hashes, normal/optimized diagnostics, native compilation and label-based rendering. The dynamic receipt records the actual commit and run. The successful v49 manuscript runs and the successful v50 freeze run are preserved as different kinds of baseline evidence. Neither is substituted for a new v51 run.

This revision is offered for a substantive review of its new one-sided pointwise theorem, exact conditional minorization and positive-height reduction, with the original upper-density and same-roof path obligations retained.
