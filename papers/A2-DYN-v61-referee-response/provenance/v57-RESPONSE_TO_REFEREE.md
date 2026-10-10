# Response to the external referee: A2-DYN revision 57

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v56-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `f3d5a8a6238497950ecde6c6f276e3c80624fc4a` / `01e36e830daee2b04036320b562990f9daf47485`.  
**Reviewed author SHA:** `4292877a5100c4c22975d9d563a1c54793139db4`.  
**Frozen complete v56 paper tree:** `c3210ca54af8edb21aa048796172a13832d1335f`.  
**New source:** `papers/A2-DYN-v57-referee-response/main.tex`.

We thank the referee for the detailed audit of the common positive physical envelope and its all-resolution consequences. This revision keeps the same four-coordinate actual-return record, all exact labels, the complete unprotected source and the pointwise arithmetic target. It adds a dynamical spectral estimate rather than another application of the interval maximal inequality. No statement below identifies total-variation convergence with uniform density-height convergence.

## 1. Response to 28.1--28.3: the positive-height target and the new spectral advance

The incidence and clearance essential-height estimates requested in 28.1 and 28.2 are not proved by this revision. The referee is correct that weak integrability, small exceptional length and small source mass allow narrow positive spikes. The two-sided unrestricted pointwise theorem in 28.3 therefore remains an explicit target of the retained positive-error representation. No physical seam is crossed, no exact label is averaged and no bad set is deleted from the final source.

The new theorem addresses another genuine analytic obstruction in the same raw law: local central variation does not imply convergence of the full mixed measure unless the arithmetic reference is uniformly tight. The existing scalar branches have moving drifts. Continuity at a resonance alone does not control the displacement `sqrt(m)(mu_j-mu_R)` when damping tends to zero with the radius.

Module `121_pressure_controlled_transition_tails.tex` proves the missing estimate directly:

`|mu_j(R)-mu_R|^2 <= C kappa_j(R)`.

Its proof is not a continuity argument. Near an actual resonance, choose bounded smooth physical initial and terminal tests with nonzero projection amplitude. These are full collision tests, not the section pairing, whose amplitude can vanish. The modulus of their complex-frequency pairing is dominated by the positive exponential moment of the centered occupation observable. Taking m-th roots bounds the real part of the centered branch logarithm at an imaginary tilt by centered pressure. The latter is `O(|t|^2)`. Taylor expansion and the optimizing tilt give the displayed squared-drift estimate. A finite cover of the zero-damping locus and a positive minimum on its complement make the constant uniform for the existing peak partition.

Completion of the square for the compact complex covariance family then yields

`|L_{m,R}(y)| <= C exp(-a |y-m mu_R|^2/m)`.

This controls the whole transition kernel about the physical mean, including weakly damped nonresonant branches and arithmetic changes. It introduces no estimate at a growing Fourier band and no nonzero section-residue assumption.

Theorem `thm:v57-global-raw-TV` combines this reference tail with the inherited actual fourth moment and complete-source local variation. It proves

`sum_{m>=n,k} integral_{u>0} |p_{n,R}(k,m,u)-m^(-2)L_{m,R}(k_1,k_2,u,n)| du -> 0`

uniformly in the radius, at each fixed actual return index n. Neither the positive roof nor any discrete label is truncated in this result. The normalized positive part of the evaluated arithmetic transition density is consequently a probability approximation in total variation. This is a whole-law conclusion for the same raw record; it is not claimed to settle its pointwise height.

## 2. Response to 28.4: the actual joint bridge, without an independence error

Module `122_coupled_global_record_bridges.tex` first proves a local joint numerator estimate using the actual collision-to-return clock coupling from module 111. It does not infer a joint law from two marginal bridge statements. The Gaussian pair is the graph law

`Law(B_{Omega_R}, A_R B_{Omega_R})`, with `A_R=c^(-1/2)L_R^(-1)`.

The covariance identity gives `A_R Omega_R A_R^T=D_R`. The two limiting paths are thus coupled and are not independent samples. The same physical fourth-moment and arithmetic Gaussian tails extend this pair estimate to the entire record space in the norm that is variation in the observation and bounded-Lipschitz dual in the two paths.

The result includes convergence of the conditional pair-bridge in mean under its own complete record distribution, with no pointwise arithmetic floor. It is stronger in its global joint observation content than a statement for a prescribed mother interval. It remains a mean statement, not an unrestricted essential-supremum theorem at every positive-reference roof. The latter still requires the height estimates named by the referee.

## 3. Exact selection events and the warning in section 18 of the report

Theorem `thm:v57-selection` treats an arbitrary record-only Markov observation kernel, with independent randomization, applied identically under the true and reference laws. The output can include the chosen interval, the acceptance decision and the random seed. The output--path mixed norm contracts.

If a full output event has reference probability at least `r_n>Delta_n`, its true probability is at least `r_n-Delta_n`; the conditional output total-variation error is at most `Delta_n/(r_n-Delta_n)` and its joint path-dual error is at most `2 Delta_n/(r_n-Delta_n)`. The same second bound controls the conditional mean pair-bridge error. Thus the conclusion is uniform over selections satisfying `Delta_n/r_n -> 0`.

The theorem retains all information in the selection event. It does not identify conditioning on a reported adaptive interval with conditioning on membership in that interval. A selector reading the path is not a record-only kernel, and an arbitrary path-dependent Gaussian amplitude is not asserted. No prescribed microscopic event whose mass is smaller than the qualitative approximation error is covered by this mass budget.

## 4. Response to 28.5: arithmetic is permanent

The uniform theorem uses the complete finite transition kernel. Only its positive part is normalized to define a probability reference; the signed kernel remains in raw inversion. Its negative total mass is proved to tend to zero rather than assumed absent at finite count.

At a fixed radius, Corollary `cor:v57-fixed-radius-raw` identifies the corresponding entire-space reference as the normalization of `n^(-2) a_R(k,n,m) g_{D_R}(V_{n,R})`. The determinant computation is explicit: `Omega_R=c L_R D_R L_R^T`, `det L_R=c`, so `det Omega_R=c^6 det D_R`. The arithmetic factor, including zero classes, is retained. No concrete uniform-residue theorem is supplied or presumed.

## 5. Response to 28.6: independent specialist audit

No independent human specialist review has been obtained. The new source does not present its finite checks, source hashes or PDF build as such a review. `SPECIALIST_AUDIT_MAP.md` adds precise audit questions for complex physical pairings, nonzero test amplitudes, scalar-continuity localization, the pressure comparison, reference-tail summation, the joint clock coupling and common disintegration. The inherited continuum audit requests remain in force.

## 6. Response to 28.7: scope and generality of the new argument

The pressure comparison supplies a reusable spectral inequality wherever a visible analytic branch admits physical complex pairings dominated by the centered positive exponential moment. The complete proof is given for the existing occupation peaks, so no additional broad system class is claimed without verification. The finite observation-kernel principle is proved for arbitrary standard Borel outputs, but its generality is not advertised as a second singular-hyperbolic application.

A second independent dynamical realization has not been supplied. The revision instead strengthens the actual original record theorem through a new bound on moving spectral data. We do not describe the inherited classical maximal lemma or Markov-kernel contraction as a new spectral theorem, nor claim an unverified historical priority for positive-pressure domination.

## 7. Response to 28.8: a short route without deleting mathematics

The journal front matter now contains one leading theorem. New Part I gives the spectral-damping estimate, reference tails, global exact-record law and joint observation/bridge consequence. Each proof identifies the exact inherited theorem it uses. The previous three leading statements, proofs and full post-title front matter are compiled verbatim in `appendices/v56_frontmatter.tex`. All 120 inherited core modules, 159 inherited Python files, old appendices and the bibliography remain byte-identical; every inherited mathematical label remains compiled. The former full main file and twelve provenance/status objects are archived.

This ordering reduces the immediate proof-navigation burden while retaining the entire raw pointwise programme and its earlier statements. It does not re-title the paper or move the original target to another project.

## 8. Response to 28.9: theorem-level comparison

The inherited comparison with Lorentz-process, endpoint mixing and suspension local-limit theory remains compiled. The new main route distinguishes the object now controlled: the entire untruncated mixed law at an exact actual return index, its finite arithmetic transition reference, and a joint pair of collision/return bridges tested by arbitrary measurable record-dependent path tests.

The passage is not obtained by differentiating a fixed-window LLT or simply using tightness of the true process. Uniform tightness of the moving arithmetic reference is a separate step, supplied by the squared-drift/damping inequality. The path result uses an actual joint clock coupling, not just two known Gaussian marginals. Positive-pressure domination, complex Gaussian integration, conditional normalization and observation-kernel contraction are standard techniques; the manuscript states their full use on this exact source rather than claiming those techniques as inventions.

## 9. Technical comments and exact conventions

All 28 technical comments are retained in scope. In particular, the old mother interval, anchored interval, band, width, threshold and collision count remain distinct in the unchanged modules. Their target-dependent exceptional sets remain nonempty in general and their pointwise statements remain almost everywhere on the good set. The signed kernel and its positive probability part are distinguished. Probability TV has the factor one half; conditional output and path constants differ by two. No polynomial count rate, inherited collision-band rate for the return clock, path-space TV, strong critical `L^{145/144}` endpoint or forward essential likelihood is asserted.

The common disintegration is adjacent to the new measurable observation/path norm. Exact source normalization is by `nu_R^*=nu|Y_R^*/c`, once only. Occupation is at times `0,...,m-1`; clearance is read at collision `j+1` in the inherited physical source. The joint local proof includes the central enlargement over a roof window. The fixed-radius arithmetic factor and zero-denominator restriction remain. Global convergence removes cutoffs from the final measures, not from an unsupported spectral estimate. Source qualification and finite diagnostics are explicitly separate from continuum proof certification.

## 10. Reproducibility

The immediate baseline has response run `37903942132` and copy run `37903952642`. Its response artifact is `11603393547`, ZIP digest `cee773031360083bce502a8a91d3564053ac0fc5ad844eb592684606b9b6a368`. This evidence is for v56 only.

The new v57 read-only workflow checks the exact event SHA, ordinary source Merkle tree, frozen v56 paper and review, every inherited module/script/appendix, all compiled labels, normal/optimized finite diagnostics, native TeX, and theorem-label-based renders. Dynamic receipts carry the actual run ID and PDF hash. Successful execution is never predeclared in this response.

This packet is submitted for review of the new pressure-controlled spectral tails and the entire-record coupled law together with the unchanged pointwise target. The incidence/clearance height questions and independent specialist verification are not marked closed.
