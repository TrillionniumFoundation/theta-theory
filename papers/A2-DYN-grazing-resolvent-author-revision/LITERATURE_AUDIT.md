# Literature and applicability audit -- 16 October 2026

The new proofs 290--291 are elementary native derivations from the actual circular reflection equations. They do not invoke a new mixing, pressure, Markov approximation, local limit, or transfer-operator theorem. The positive matrix inverse, its exact weighted estimate, complex-log tensors and the set-partition induction are proved in the manuscript. The ordinary finite-dimensional implicit function theorem is applied to a smooth fixed-word reflection system with explicitly invertible Jacobian and nonzero flights, allowing radius as a parameter. It is not used to continue the physical itinerary through a forbidden obstacle.

## Demers--Zhang: what was checked

M. F. Demers and H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Communications in Mathematical Physics 324 (2013), 767--830; DOI 10.1007/s00220-013-1820-0. The author's 53-page PDF was inspected, including the hypotheses and stable-curve norms/preliminaries:

https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf

The relevant framework has H1--H5, an invariant homogeneous C2 curve class, adapted-norm one-step expansion, distortion and Jacobian hypotheses, with geometric bounds held uniformly across the declared perturbation class. Its arclength/direction coordinates are not automatically the radius-dependent alpha,p coordinates of this manuscript. Stable inverse-curve Jacobian root sums (including Lemma 3.2) require the stated curve class, cuts and norms. These hypotheses must be verified before transfer to the exact A2-DYN family. The reference alone does not prove a same-roof, exact-label m^-2 essential-height estimate or the remaining positive-source limit.

## Baladi--Demers: what was checked

V. Baladi and M. F. Demers, *Thermodynamic formalism for dispersing billiards*, Journal of Modern Dynamics 18 (2022), 415--493; DOI 10.3934/jmd.2022013. The author's 62-page proof PDF was inspected, including Theorem 1.1 and Lemma 3.1:

https://faculty.fairfield.edu/mdemers/research/2022.09.19.thermo.postultimate.proofed.pdf

The pressure concerns the geometric potential -t log J^u T on the specified finite-horizon dispersing billiard, for t in the stated pressure interval (0,t*). Lemma 3.1 fixes t1 in (1,t*) and theta in (Lambda^-1,Lambda^-1/2) satisfying theta^t1 < exp P(t1), then t0 in (0,1) and q>=2/t0; homogeneity and short-curve scales must be chosen accordingly. The resulting adapted stable-Jacobian root estimate is not an unrestricted four-label twisted spectral theorem. It neither makes all radius-dependent constants uniform automatically nor controls arbitrary Borel section/roof selectors in the topology required here.

## Consequences for this revision

These references support the identified frameworks, not a missing deduction. Their transfer to the manuscript's retained pressure/growth inputs remains explicitly conditional where the full coordinate/function-space/quantifier verification has not been supplied. The fourth-variation and endpoint-jet results require neither reference. We do not cite a scalar pressure result as the original raw joint local limit theorem, or a curve-growth bound as a roofwise essential supremum estimate.

Historical bibliography and earlier audits are retained rather than silently replaced. This is a focused fresh applicability check of the external inputs relevant to the present geometric step, not a claim that every historical bibliography entry or all old spectral proofs have been independently rederived in this round. Repository-internal source citations identify inherited assumptions and proof provenance; they are not independent peer review.
