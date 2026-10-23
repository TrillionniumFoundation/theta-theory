# Fresh primary-source hypothesis check for the A2-DYN continuation

Author-revision verification, 23 October 2026. This note supplements the preserved literature audit. It checks the actual cited scopes; it is not a new referee report or independent human reconstruction.

## Retrieval and version identity

Fresh downloads at 12:52 UTC are recorded in `PRIMARY_RETRIEVAL.json`. The three successful PDF hashes match the latest inherited `audit/FRESH_PRIMARY_SOURCE_IDENTITIES.json` exactly. Different arXiv versions are not assumed byte-identical. The PDFs and extracted text remain scratch verification material; they are not proposed for repository redistribution.

| Primary text | Inspected version | Bytes | SHA-256 |
|---|---|---:|---|
| Demers–Zhang, *A functional analytic approach to perturbations of the Lorentz gas* | Author PDF dated 10 October 2013; 53 pages | 662784 | `1fa90861a949196bbb1c903e48a53217fbbd76ba24656c5aa1faeccac42fc66f` |
| Baladi–Demers, *Thermodynamic formalism for dispersing billiards* | Author PDF dated 19 September 2022; 62 pages | 907905 | `ee369f41e0a82d7d5f176338a2b925f0ae30d89275dda2177fcbd41a7524311d` |
| Dolgopyat–Nándori, *On mixing and the local central limit theorem for hyperbolic flows* | Author-hosted `llt_flow13.pdf`; 35 pages; server modification 24 October 2017 | 467506 | `1a0252ad6ed11e36e5b61a22689028f977ff545b3c29f15af93172432a528ad5` |
| Coste, *An Introduction to O-minimal Geometry* | November 1999 text, author-uploaded full text; theorem pages 19 and 71 inspected | Not downloaded | No new PDF hash claimed |

## Coste: fixed-formula geometric decomposition

The university PDF returned HTTP 503 and the HAL copy displayed an access-denied challenge. Public full text explicitly attributed to the author was readable at [the author-content page](https://www.researchgate.net/publication/228392940_An_introduction_to_O-minimal_geometry); the displayed PDF-download link returned 404. Thus this is direct theorem-text checking, not full-PDF identity verification.

Theorems 2.9–2.10, page 19, concern uniform finite fibers of one definable set and finite cylindrical decompositions adapted to finitely many definable sets. Theorems 6.6–6.7, page 71, give the finite smooth decomposition and piecewise smoothness of a definable scalar function.

Application inference: native 336 uses a semialgebraic physical graph at fixed collision count and same-radius fiberwise boundaries. These are appropriate inputs; smooth arbitrary weights are inserted afterward and need not be definable. The reference does not bound formula growth with collision count, guarantee uniform roof gaps, control Jacobian size, or pay normalized source concentration. Existing native 164 supplies the physical graph; the new audit does not rebrand that construction.

## Demers–Zhang: admissible multipliers and growth

Primary: [dated author PDF](https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf).

Section 3.3, pages 12–13, uses arclength stable-curve tests, matched curves in the same homogeneity strip, and little Hölder spaces; the function embedding represents density relative to the invariant collision measure. Lemmas 5.2–5.3, page 32, require a modulo-zero partition into simply connected open cells, uniformly bounded transverse smooth boundary pieces, and uniformly bounded cells per homogeneity strip for multiplication. The multiplier exponent is `gamma=max(p,2 beta+epsilon)`. H2–H4, pages 10–11, require an invariant curvature-controlled homogeneous curve family, adapted one-step contraction and uniform distortion. Lemma 5.5, pages 35–36, retains the actual last-long-ancestor genealogy.

Application inference: native 333's finite original-section partition verifies a multiplier interface, not all dynamical or perturbative hypotheses. Native 327 proves its own length-sensitive renewal and includes the terminal-long generation. Radius uniformity for the actual enlarged curve family and any joint marked operator remains a native proof obligation; neither lemma automatically pays a roofwise exact-record density.

## Baladi–Demers: potential, pressure and function space

Primary: [dated author PDF](https://faculty.fairfield.edu/mdemers/research/2022.09.19.thermo.postultimate.proofed.pdf).

Section 1.1, page 2, assumes finitely many disjoint positively curved C3 scatterers and excludes trajectories with only tangential collisions. Lemma 3.6, page 16, controls a long-cell fraction for its actual homogeneous partition and potential on the stated parameter interval. Proposition 3.14, page 25, requires a sufficiently long stable curve, bounded C1 perturbing potential and its inequalities (3.6), (3.30). Theorem 4.1, page 31, builds its own anisotropic space for a compact potential-parameter interval inside `(0,t_*)`. Remark 4.4, page 32, explicitly corrects an older inadequate citation concerning piecewise Hölder regularity of the stable Jacobian.

Application inference: native 282's original triangular geometry excludes straight half-lines avoiding disk interiors, hence the all-tangential possibility. Native 326's claimed full-word pressure has its own proof obligations; the external theorem does not automatically provide radius-uniform pressure, arbitrary section twists or the original comparison-pool abundance. No new result is inferred merely from replacing its partition or potential notation.

## Dolgopyat–Nándori: tests, arithmetic and normalization

Primary: [author PDF](https://www.math.umd.edu/~dolgop/llt_flow13.pdf).

Definition 2.2 and Remark 2.5, pages 3–4, retain square-integrability, a bounded almost-everywhere-continuous coboundary, positive covariance, translated subgroup, fixed endpoint/observation tests and compact scaled centers with a fixed center-error bound. Boundary-null fixed sets are allowed; a nonminimal observable can have an endpoint-dependent limit. The suspension measure is the collision measure times physical roof Lebesgue measure divided by mean roof. Proposition 6.3, page 32, assumes minimality and its arithmetic cases A–C; its displayed continuous formula additionally assumes nonarithmeticity.

Application inference: these tested limits cannot be substituted for A2-DYN's raw roof essential supremum, shrinking microscopic windows, full exact-label arithmetic factor or actual conditioned denominator. Native 334's sufficient bridge uses its explicitly identified inherited fixed-window result; it does not require an invented extra growing-band theorem. Native 337's fixed-parameter frequency mean square also does not replace the original raw target.

## Result of the check

The citations remain scope-qualified. Fresh primary reading confirms the distinctions already present in native 333–337. The newly obtained Coste author-content reading strengthens the earlier indexed-snippet evidence, while the failed byte download remains recorded. No listed external source supplies the missing normalized endpoint shortage, full local derivative-charge decay, or the final four-coordinate raw inversion theorem.

Web locators for reproducibility: Demers–Zhang and Baladi–Demers were opened directly as primary PDFs, as was Dolgopyat–Nándori. Coste theorem statements were located directly within the author-content full text. The repository note uses stable URLs, not transient search-result identifiers.

