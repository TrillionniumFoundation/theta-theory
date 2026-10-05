# Literature audit for the external A2-DYN review

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Audit date:** 5 October 2026  
**Scope:** theorem-level positioning of the reviewed claims against primary sources; not an exhaustive priority search.

## 1. Classical Lorentz-process local limit theorem

D. Szász and T. Varjú, *Local limit theorem for the Lorentz process and its recurrence in the plane*, Ergodic Theory Dynam. Systems **24** (2004), 257–278, DOI `10.1017/S0143385703000439`.

This work proves a local central limit theorem for Young systems and applies it to the finite-horizon planar Lorentz process, with displacement as the principal lattice observable. It is the natural discrete-time benchmark for the present manuscript.

The reviewed A2-DYN paper studies a different and more detailed record: displacement, physical collision count, induced return count, and continuous flight time, together with raw density behavior. Its arithmetic and edge statements are not consequences of quoting the classical displacement LLT. Conversely, A2-DYN does not yet prove a new full Lorentz-process LLT that supersedes Szász–Varjú.

## 2. Suspension-flow local central limit theory

D. Dolgopyat and P. Nándori, *On mixing and the local central limit theorem for hyperbolic flows*, Ergodic Theory Dynam. Systems **40** (2020), 142–174, DOI `10.1017/etds.2018.29`; arXiv `1710.08568`.

The paper formulates abstract conditions for local central limit theorems of suspension flows and verifies them for several hyperbolic systems, including finite-horizon Sinai billiards. It is the closest general comparison for the induced-roof and physical-time aspects of A2-DYN.

The distinction emphasized by the reviewed manuscript is legitimate. An abstract mixing LCLT for test functions or smoothed suspension observables does not automatically provide an everywhere raw density for a mixed lattice–continuous record, nor does it remove the jump singularity found in the selected return-time component. A2-DYN's exact edge calculation and localized inversion criterion address this raw-data issue.

At the same time, the abstract suspension theory makes clear why the present periodic arithmetic is not the end of the proof. A2-DYN still needs a concrete operator/cohomology realization and quantitative frequency estimates on the spaces supporting its unbounded induced observables.

## 3. Transfer operators and parameter perturbations

M. F. Demers and H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Comm. Math. Phys. **324** (2013), 767–830, DOI `10.1007/s00220-013-1820-0`; arXiv `1210.1261`.

This work develops anisotropic Banach spaces for perturbations of the periodic Lorentz gas and proves continuity of spectra and spectral projections under broad classes of map perturbations. It is the most relevant primary source for the missing common-space and parameter-stability layer in A2-DYN.

The reviewed paper does not claim to import those perturbative results wholesale. Its inducing sets and induced observables vary with the radius, and the mixed record includes unbounded return quantities. The branchwise fixed-return continuity theorem is useful, but it is not yet a common twisted transfer-operator theorem or a uniform spectral perturbation result.

## 4. Flow spectral theory and exponential mixing

V. Baladi, M. Demers, and C. Liverani, *Exponential decay of correlations for finite horizon Sinai billiard flows*, Invent. Math. **211** (2018), 39–177, DOI `10.1007/s00222-017-0745-1`; arXiv `1506.02836`.

The paper proves exponential decay of correlations for finite-horizon Sinai billiard flows and describes the generator spectrum on anisotropic distribution spaces. This is relevant background for a future spectral realization of the A2-DYN physical-time problem.

A2-DYN correctly avoids claiming that exponential mixing alone yields its raw mixed-density LLT. The roof-frequency behavior, lattice arithmetic, unbounded induced observables, and explicit boundary contributions require additional arguments.

## 5. What is specific to A2-DYN

The reviewed manuscript's most distinctive contributions are:

1. an explicit physical periodic family with zero winding and controlled return/collision records;
2. positive excess-length increments with two-sided quantitative bounds;
3. a complete joint periodic annihilator and a negative-power periodic phase discrepancy at large roof frequency;
4. a physical critical-edge jump coefficient and exact raw-edge subtraction;
5. a local central-window criterion that permits nonvanishing extracted edge mass away from the window;
6. fixed-return raw-density continuity under radius variation;
7. a parameter-uniform first-order physical clock including the stationary length-biased law and unfinished returns.

These are not merely restatements of the cited LLT or mixing theorems.

## 6. Remaining comparison boundary

The manuscript still does not supply the theorem that would place its final result beyond the existing literature:

- a common anisotropic operator family for the radius-dependent induced system;
- regularity sufficient to turn spectral coboundaries into periodic equations;
- a quantitative high-frequency resolvent bound using the new periods;
- continuity and nondegeneracy of the full covariance;
- an all-branch raw residual estimate;
- a conditioned square-root physical-clock transfer;
- the resulting parameter-uniform raw mixed-density LLT.

For this reason, the current paper is best viewed as a collection of new enabling results and a precise obstruction analysis, not as a completed replacement for the classical map or suspension-flow LLT theories.

## 7. Audit limitation

The primary records and abstracts of the cited papers were checked. This audit did not conduct an exhaustive search for every periodic-orbit nonintegrability criterion, every anisotropic-space construction, or every raw-density result for billiards. It makes no definitive priority claim beyond the theorem-level distinctions stated above.
