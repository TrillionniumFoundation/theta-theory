# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `74660ef907fa0e9c4c0b8644a096f7bbca3b3f69`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

The Round-Nineteen branch contains no revised B1 source. The controlling file is unchanged from the prior review, including the direct regularity contradiction in the Fourier argument. No corrected scaling regime, canonical cluster estimate, mixed position/velocity Fourier proof, or shell theorem has been supplied.

## 2. Unresolved fatal defects

### 2.1. The canonical scaling and source-dependent comparison remain unspecified

The proof still uses `N\varepsilon^3=O(\varepsilon)` without stating the joint limit, physical volume, density, or activity scaling that makes this true. It also treats the path/contact source as though it were a uniformly bounded perturbation of sequential one-particle kernels. Future collision histories depend discontinuously on initial data when contacts are created, removed, or reordered. A source-differentiated fixed-`N` canonical cluster estimate is required; appeal to a grand-canonical connected remainder does not prove the displayed Hessian comparison.

### 2.2. The saddle theorem still overreaches

A local inverse-function theorem does not prove a unique saddle for every target in a compact subset of the full interior mean image. Global strict convexity, properness, and containment of the target set in the interacting mean image are missing. The cell coordinates may obey affine relations, in which case a positive-definite covariance on all of `\mathbb R^d` is impossible unless redundant coordinates are quotiented out. Analytic dependence on an infinite-dimensional path source is likewise not established.

### 2.3. The `C^4` versus `O(N)` integration-by-parts contradiction remains verbatim

`lem:r17-b1-cell` controls only four derivatives of the logarithmic interaction factor, and the upstream source input is also limited to low order. The high-frequency proof then performs `s+cN` integrations by parts. Those integrations generate derivatives, including mixed derivatives, of the interacting conditional amplitude of order growing with `N`. A `C^4` bound cannot justify this. Distributing integrations among particles does not remove the mixed-derivative requirement. This single contradiction invalidates the claimed global Fourier majorant.

### 2.4. Position-type Fourier directions remain uncontrolled

The constraint vector includes position observables `\chi_j`, while the proof detects every Fourier direction by differentiating in a velocity coordinate. A Fourier vector supported in the `\chi` directions has zero velocity derivative. Position integration would create hard-core boundary and moving-cell boundary terms, none of which is analysed. Thus the compact-annulus damping and high-frequency decay do not cover the declared dual space.

### 2.5. The fallback and shell claims remain too strong

`W^{d+3,1}` regularity does not provide arbitrary decay with an exponent `s>d+4`, and the exceptional event is not supplied with the derivatives used in the proof. The shell theorem claims relative Gaussian asymptotics for broad geometric families without lower bounds on Gaussian mass or a restriction to the central regime. “Point boxes” in continuous coordinates have zero probability and zero inradius. The pressure `Q^N` is then introduced as already obtained by the coefficient extraction B1 is meant to prove.

## 3. Editorial consequence

A revised manuscript must provide a precise scaling, a canonical source-dependent cluster theorem, a rank-correct global saddle, and a Fourier method whose regularity assumptions match its integrations and which handles position boundaries. No such revision exists.

## 4. Recommendation

**Reject without reconsideration.** The central coefficient theorem remains unsupported by a proof containing a direct internal contradiction.