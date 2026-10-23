# Literature hypothesis audit for the present A2-DYN author revision

Audit date: 2026-10-23. This document records a fresh reading of primary mathematical sources and the precise use made of them. It is an author-side reconstruction, not a new referee report, an external specialist certification, or a replacement for the retained native proofs. Page numbers below count the first PDF page as page 1.

## 1. Demers--Zhang: the exact multiplier and pairing interface

**Primary source:** Mark F. Demers and Hong-Kun Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, author version dated 10 October 2013, 53 pages. [Author PDF](https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf).

**Checked source statements:** Sections 3.2--3.3, pages 11--13; Lemma 3.4, page 17; Lemmas 5.2--5.3, page 32, proof pages 33--34.

- Representation: `h(psi)=integral h psi dmu`.
- Parameters: `0<q<p<=1/3`, `0<alpha<1-varsigma_0`, `0<beta<=min(alpha,p-q)`.
- Weak tests: `||psi||C^p<=1`; stable tests: `|W|^alpha ||psi||C^q<=1`; strong norm: stable plus a fixed positive multiple of unstable norm. The latter compares nearby curves in the same homogeneity strip, with matched tests and weight `epsilon^-beta`. Here `C^p` is the smooth-function closure in the Hölder norm.
- Lemma 3.4: `h in Bw`, `T in F`, `n>=0`, `psi in C^p(T^-n Ws)` imply `|h(psi)|<=C |h|w (||psi||infinity+H_n^p(psi))`.
- Lemma 5.2: a modulo-zero partition into open simply connected cells; uniformly bounded smooth boundary count and uniform stable-cone transversality; finitely many cells per homogeneity strip. Uniform piecewise `C^gamma`, `gamma>2beta`, implies membership in `B`.
- Lemma 5.3: additionally a uniform cell count `N_1` per strip; `gamma=max(p,2beta+epsilon)`, `epsilon>0`. Then `||fh||B<=C||h||B sup_P||f||C^gamma(P)`.

### Application to the original section in native 333

The reconstructed application is a finite geometric calculation on the original five section rectangles. It is located at `lem:sm-grid`, `thm:sm-multipliers`, `thm:sm-moving`, and `cor:sm-transfer`. Its common coordinates are `(alpha,varphi)`, with `p=sin(varphi)` and boundary arclength `s=R alpha`. The uniform containing cone has slope magnitudes between `45/47` and `799/90`. The section grid has at most 121 cells, four sides per cell, and at most 121 cells meeting any homogeneity strip. Its explicit sine-angle bound is

`vartheta_sec=(45/47)/sqrt(1+(799/90)^2)>0`.

On this partition the section indicator and its exponential are constant. Thus their piecewise regularity is available for every required finite Hölder exponent. The occupation exponential has the exact identity

`M_exp(z eta)=I+(exp(z)-1)M_eta`.

The bound and entire dependence follow from that identity and the bounded multiplier; they do not incur a power of the real occupation frequency. For the moving section, the proof estimates no more than 82 nonzero stable subarcs of length at most `11 |R-S|/vartheta_sec`. The defining strong stable inequality pays their weak pairing by a constant times `|R-S|^alpha`. This is a direct reconstruction of a multiplication estimate, not an estimate for changing the physical collision map.

The common cylinder carries the original reference probability

`dnu=cos(varphi) d alpha d varphi/(4pi)=d alpha dp/(4pi)`.

The intended density convention is **relative to nu**: the constant function `1` represents `nu`, and `eta_R` represents `eta_R nu`. It would be incorrect to insert the coordinate density `cos(varphi)/(4pi)` a second time into a space already representing `h nu`. Mass evaluation is the test against `1`; the section source is divided by `c_*` exactly once. This convention fixes the transfer identity and preserves the initial occupation count with a separate terminal membership test.

Containing all physical stable directions in a common cone does not prove invariance of the enlarged test family. A fixed norm construction, bounded coordinate scaling, multiplication, and weak motion of section sides do not by themselves establish the collision-family assumptions needed for spectral perturbation. The fixed common construction is used for the explicitly stated multiplication comparison. Any claim about a family of physical transfer operators must separately supply its common invariant curve geometry, bounded operator realization, compact embedding, distortion and expansion hypotheses, and parameter comparison. In the external source these are the roles of (H1)--(H5), (C1)--(C4), and the perturbative framework preceding Theorems 2.2--2.3. They are not automatically properties of a newly introduced joint twist.

### Historical priority and precise spectral status

The retained historical-v108 native 77 already contains `lem:v37-section-multiplier` and the entire section phase. Native 84 already proves the moving-section weak estimate in the proof of `thm:v40-polynomial-LY`. It also contains written full occupation-torus fixed-band inequalities and a peripheral-spectrum argument (`thm:v40-full-peripheral`). Native 85--87 retain their associated holonomy, arithmetic, local-law and resonance arguments. They are part of the preserved proof record; their existence must not be denied by saying that all joint spectral work is absent.

Native 333 is therefore a quantitative reconstruction and hypothesis audit of this interface. The explicit cutoff payment in 334 permits a bandwidth growing as `m^(P+2)/|I|`. A theorem whose roof band is fixed before the collision limit does not, merely by its statement, supply a strong-operator estimate throughout that growing band. However, the particular scalar interval expression can be evaluated by combining the retained native 87 fixed-window theorem with the new absolute tail; a new growing-band strong estimate is not required for that implication. `prop:ui-inherited-bridge` makes this consequence explicit, and `lem:ui-reference-modulus` proves the needed roof modulus of the same finite-peak reference. The normalized local derivative charge remains the sufficient condition not yet paid on this route. Retaining written spectral proofs is distinct from claiming their independent expert validation.

## 2. Baladi--Demers: physical table, finite horizon and pressure

**Primary source:** Viviane Baladi and Mark F. Demers, *Thermodynamic formalism for dispersing billiards*, arXiv:2009.10936, version 3 (31 August 2022), 62 pages; manuscript date 1 September 2022. [Primary PDF](https://arxiv.org/pdf/2009.10936).

Section 1.1, page 2, treats a two-torus with finitely many disjoint scatterers having `C^3` boundaries and positive curvature, unit-speed motion and specular reflection. Its stable slopes satisfy

`-K_max-tau_min^-1 <= dvarphi/dr <= -K_min`.

Its finite-horizon assumption excludes trajectories consisting entirely of tangential collisions. The text explicitly distinguishes this from merely `sup tau<infinity` and notes the stronger condition in connection with Proposition 5.2. The pressure and equilibrium-state statements concern the stated billiard, its geometric potential and its specified parameter interval. They are not a general theorem for arbitrary symbolic substitutes or arbitrary discontinuous joint observations.

**Use in this revision:** the cone geometry is compatible with the original circular family and is used with that family's proved curvature and free-flight constants. No new pressure theorem is imported to prove the selected endpoint kernel. If a pressure or equilibrium theorem is invoked elsewhere, its all-tangency exclusion, actual potential, spaces and uniformity over radius must be checked at that application. A free-flight cap alone is not that full verification. The native physical-word pressure proof and its original dependencies remain preserved; the present audit neither deletes it nor silently extends its scope.

## 3. Dolgopyat--Nandori: test topology, arithmetic and suspension measure

**Primary source:** Dmitry Dolgopyat and Peter Nandori, *On mixing and the local central limit theorem for hyperbolic flows*, arXiv:1710.08568, version 1, 24 October 2017, 35 pages. [Primary PDF](https://arxiv.org/pdf/1710.08568).

Definition 2.2, pages 3--4, assumes square-integrable `f=g-h+h o T`, with bounded, almost-everywhere continuous `h`, a closed subgroup `M`, a translate `r`, and positive-definite covariance. Its tests are fixed bounded continuous endpoint functions and a fixed compactly supported continuous additive-coordinate function. Centers satisfy `w_n in M+nr`, `|w_n-w sqrt(n)|<=K`; uniformity is for fixed `K` and compact `w`. Remark 2.5 permits the specified fixed continuity sets.

Definition 3.1, pages 7--8, uses a flow coboundary continuous almost everywhere and bounded on each bounded-height region, and analogous fixed tests. The suspension probability is `mu=nu tensor Leb/nu(tau)`. Theorem 3.7 requires (H1)--(H7), including the joint base MLCLT and the stated moderate-deviation bound. These are not conclusions deduced solely from a scalar roof limit.

**Use in this revision:** no new result is obtained by citing this flow theorem. Fixed-test convergence does not assert a supremum of raw density errors on shrinking microscopic windows, nor uniformity in radius and all exact labels. Such a conclusion requires additional estimates. The original conditional section source, the physical collision count, and the unit-speed clock cannot be replaced by the suspension probability or an induced time convention without an exact proved conversion. Coboundary endpoint terms and arithmetic subgroup effects remain observable information; they cannot be discarded to manufacture a product law.

## 4. New proofs and external-theorem dependence

Native 334 uses the inherited all-label BV statements (`thm:av-all-bv`, `thm:wo-bv`), elementary Fourier orthogonality, a justified approximate-identity limit, and explicit positive tail integration. Its first pointwise inequality is a sufficient conditional statement. The subsequent `prop:ui-inherited-bridge` invokes the written native 87 fixed-window law at its actual scope to pay the scalar comparison and reference-modulus terms, leaving the normalized local variation condition. No external raw density theorem is substituted for that remaining step. Earlier native 64, 66--67, 93 and 331 already contain exact inversion, cutoff or conditional-denominator results in their respective scopes; the precise added content of 334 is identified in the novelty audit rather than claimed as a first Fourier-inversion method.

Native 335 uses the inherited exact physical first-image density (`eq:mc-density`), complete renewal (`eq:lc-renewal`), last-collision cancellation (`eq:mc-last-cancellation`), area-preserving reversal, and physical-side critical-sector comparison (`eq:mc-sector-comparison`). It does not use a new pressure hypothesis or replace real trajectories by a Markov process.

The new mathematical check document records the derivations, normalizations and limit order. Finite verification scripts test algebra and transcription; they do not certify the continuous dynamical hypotheses of any cited source.

## 5. Exact downloaded author versions and duality background

The final primary-source check additionally downloaded the author-hosted Demers–Zhang (53 pages), Baladi–Demers (62 pages, URL dated 19 September 2022), and Dolgopyat–Nándori (35 pages, `llt_flow13.pdf`) files, together with the official Stanford duality slides (40 pages). URLs, byte counts, UTC retrieval times and SHA-256 values are in `audit/PRIMARY_SOURCE_DOWNLOAD_IDENTITIES.json`. These records pin the actual inspected files; an author-hosted file is not asserted byte-identical to a differently dated arXiv version. The author-hosted BD text explicitly states the no-all-tangential-trajectories requirement on page 2.

The Boyd–Vandenberghe citation is general background only. Its convex strong-duality discussion carries convexity and constraint qualification requirements; it is not invoked as an unchecked theorem for the billiard's disk-word problem. Native 297 supplies the specific primal/dual construction and its proof. The new continuation invokes no additional duality theorem. The PDFs were used for research inspection; the repository retains their content identities and locators, not redistributed copies of the external papers.
