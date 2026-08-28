# CM2 moving-billiard nonvacuity research note

Date: 2026-07-14

Target manuscript: cm2-bridge-note-v47.tex

## Bottom line

No paper found through 2026-07-14 verifies, on one actual moving collision–SRB descendant class, all of:

1. moving face to a regular standard family with product-time recovery;
2. prescribed-depth PPE2–PPE4;
3. exact physical/source occurrence-current matching;
4. normalized shallow and stopped-deep moments;
5. the final pathwise/quenched upgrade.

The literature shortens individual gates but cannot be cited as a black box for nonvacuity. The most economical pilot is Stenlund's fixed-section two-disk random moving-scatterer cocycle, not a general continuously moving billiard flow.

## Frozen pilot

Use

\[
\bar R=0.36=9/25,\qquad R=0.16=4/25,\qquad
\varepsilon=0.005=1/200.
\]

The exact certificate in cm2_fixed_section_geometry_cert.py proves:

| window | certified margin |
|---|---:|
| boundary | 0.14 |
| diagonal/non-overlap | 0.1821067811… |
| finite-horizon lower window | 0.0064466094… |
| blocking | 0.015 |
| free-zone | 0.1696486423… |

The fixed-section construction supplies a common collision section, a common invariant probability

\[
d\mu=M^{-1}\cos\varphi\,dr\,d\varphi,
\]

reversibility, bijective return maps, and at most one collision with the moving white disk per return. Therefore the physical tree/carrier Radon–Nikodym factors are exactly one.

## What the closest literature supplies

| source | usable ingredient | missing for CM2 |
|---|---|---|
| [Stenlund–Young–Zhang 2013](https://arxiv.org/abs/1210.0011) | uniform hyperbolicity, recovery, time-dependent magnet coupling, memory loss | exact coarea current, PPE, exact matching |
| [Stenlund 2014](https://arxiv.org/abs/1210.0902) | common fixed section and common invariant law for the two-disk pilot | moving-face derivative source, PPE, normalized rare-cell moments |
| [Demers–Zhang 2013](https://arxiv.org/abs/1210.1261) | common anisotropic spaces and perturbative stability | moving-face source and prescribed-depth escape |
| [Demers–Liverani 2023](https://arxiv.org/abs/2104.06947) | sequential projective cones, contraction, holes | coarea source, jet, exact current matching |
| [Canestrari 2026, small holes](https://arxiv.org/abs/2604.19671) | boundary-source standard families, Z-complexity, short curves, recovery and coupling | arbitrary moving coarea face, PPE, matching |
| [Canestrari 2026, discontinuous perturbations](https://arxiv.org/abs/2411.16628) | source-first foliation and long/small-bad decomposition | billiard collision singularities and all-depth PPE |
| [Demers–Liverani 2025](https://arxiv.org/abs/2502.07765) | sequential CLT-scale characteristic estimates | high-frequency prescribed-depth PPE |
| [Demers–Pène–Zhang 2020](https://arxiv.org/abs/1902.06850) | annealed LLT for randomly deforming billiards | moving descendants and environment-quenched CM2 |
| [Ni 2025](https://arxiv.org/abs/2410.10138) | foliation-aligned likelihood language | singular deterministic billiard coarea construction |
| [Dragičević et al.](https://arxiv.org/abs/1812.07340) | quenched operator-cocycle template | PPE and source matching |
| [Demers–Liverani 2026 review](https://arxiv.org/abs/2606.10155) | current frontier and open small-set/memory-loss problems | confirms rare-set concentration is not automatic |

The 2026 qualitative homoclinic results for analytic convex interior billiards do not supply a quantitative native-coordinate jet lower bound for dispersing moving tables.

## New bridge obtained in v47

PAIR_TENERGY need not remain primitive. Under the exact unselected product/source law, slope–endpoint identification, and a PPE estimate uniform in the frozen opposite endpoint and admissible polynomial context:

1. freeze the second endpoint;
2. apply PPE to the first endpoint with the frozen context polynomial;
3. include the SS/NST bad sets for both endpoints;
4. sum the stopped antichain;
5. integrate the frozen endpoint and parent by Tonelli.

This derives the exact pair small-ball bound. A common random environment alone would not suffice because it can correlate the two endpoints.

## FS_CERT(d_Z): remaining proof obligations

The v47 manuscript packages the honest concrete target as:

1. exact moving-face impact/coarea occurrence measure and signed current;
2. oriented flux standard-family entry plus deep failure tail;
3. hereditary cellwise weighted Z estimate;
4. recordwise diagonal physical/source matching;
5. an all-depth invariant terminal native-z jet cone;
6. precise weighted PPE2 and PPE3–PPE4;
7. one pre-query canonical depth linking word depth and recovery rank;
8. the remaining global response bundle;
9. a rational strict-rate feasibility certificate.

The hereditary estimate is the correct way to obtain the three laws:

\[
\int_C W Z^{\chi_Z}\,dq\le K_Z\int_C W\,dq.
\]

For the whole space and every shallow/deep record cell, dividing by the cell mass gives the normalized moment. A global average alone cannot do this.

## Shortest constructive route

1. On every clean finite cylinder, solve the white-disk impact equation
   \[
   |q+t v-c(z)|^2=R^2
   \]
   and interval-certify the non-grazing root, coarea Jacobian, distortion, orientation, and entry time.
2. Use Canestrari's small-hole machinery only after that face has been proved to be a regular flux family.
3. Restart the stopped renewal at
   \[
   j_-=\lceil(1-\theta_1)N\rceil
   \]
   and prove an invariant terminal jet cone for every depth. Finite-depth sampling is evidence, not proof.
4. Define source q as the push-forward of the same unselected physical occurrence law and prove exact current identities on every restriction.
5. Prove the hereditary Z estimate cellwise and the word-depth/recovery-rank inclusions.
6. Obtain the annealed statement by conditioning on all but one refreshed center coordinate. Upgrade with weighted Borel–Cantelli on total descendant q-mass, not a union bound over exponentially many words.

## Strict boundary

The explicit geometry and common-law portion of the pilot is now certified. The v47 theorem is a fully typed certification implication. It is not yet an unconditional CM2 theorem for the pilot because the all-depth terminal jet, exact moving-face coarea/current construction, hereditary rare-cell Z estimate, and remaining response bundle have not been proved.
