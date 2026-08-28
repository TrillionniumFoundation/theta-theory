# CM2 Gate 5: finite prefix/suffix algebra versus physical norm transfer

Date: 2026-07-15 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot, common refinement
`X=M*=M sqcup W`, standard solid-boundary section `N=G sqcup W`  
Frozen inputs: v50/v52 and their manifests were read only

## Verdict

Gate 5 remains **`NOT_CERTIFIED`**.  This audit closes the finite algebraic
part of the section lift and isolates the last norm/phase obstruction more
sharply:

- `K_N<=9` and the finite Borel return-word partition make every formal
  prefix, suffix and Kac sum finite;
- the corresponding source pushforward and test pullback are exact adjoints,
  and the normalized tower lift obeys the exact Kac pairing;
- the already certified two-row reflection orbit is locally isometric in the
  standard-family/flux test coordinates;
- none of these facts supplies a uniform operator bound on the physical
  regular-density, standard-family, flux/face or physical-test spaces;
- bounded height does not imply return-phase gcd one.

The minimal missing input is no longer an abstract ``section transfer
theorem''.  It is one quantitative, branchwise prefix/suffix ledger on the
actual return partition: homogeneity subdivision, inverse-Jacobian and
distortion bounds, one-step cut/fragmentation bounds, face transversality and
chart bounds, dynamic-test pullback bounds, plus the actual weighted phase
graph and its cycle gcd.  Those data have not been certified globally.

## 1. What finite height proves exactly

Let `W_N` be the finite Borel collection of return records.  A record `w`
has length `r(w)<=9`, domain `D_w subset X`, endpoint branch

```text
H_w = T^(r(w)) | D_w : D_w -> N.
```

Up to the null overlap convention fixed by the event ledger, the `D_w` form
a partition.  Therefore the endpoint source map and its test adjoint are the
finite algebraic expressions

```text
L_XN nu = sum_w (H_w)_*(nu | D_w),
L_XN^* phi = sum_w 1_Dw (phi o H_w).
```

For every finite signed measure `nu` and bounded Borel test `phi`, ordinary
change of variables gives the exact identity

```text
<L_XN nu,phi>_N = <nu,L_XN^* phi>_X.              (1.1)
```

If `r_N:N->{1,...,9}` is the physical tower roof, the normalized phase lift
and Kac test sum are

```text
E_NX nu = (1/mu_N(r_N)) sum_w sum_{0<=j<r(w)}
              (T^j)_*(nu | D_w),
S_XN h(x) = sum_{0<=j<r_N(x)} h(T^j x).
```

They obey

```text
<E_NX nu,h>_X = <nu,S_XN h>_N / mu_N(r_N).        (1.2)
```

For a current inserted at level `j` of word `w`, its physical contribution
has an equally exact prefix/suffix factorization

```text
< U_suffix J_(w,j) U_prefix nu, phi >
 = < J_(w,j) U_prefix nu, U_suffix^* phi >.        (1.3)
```

The companion certificate replays (1.1)--(1.3) over exact rational finite
matrices.  These are algebra and measurability conclusions; no smoothness or
Banach bound occurs in their proof.

## 2. The two CM2 Banach pairs and the sufficient ledger

The v52 current interface uses two concrete oriented source/test pairs:

1. the measured standard-family pair
   `(S_sf^epsilon,T_sf^epsilon)`, whose source norm charges mass, density
   regularity and the inverse-length boundary functional `Z`;
2. the coarea/face pair `(S_flux^epsilon,T_flux^epsilon)`, which additionally
   charges oriented endpoints, homogeneous cuts, a `C2` atlas/coarea mark and
   a `C1` face-test trace.

The regular two-dimensional density space is a third input space feeding
these currents.  Demers--Liverani 2026, Theorem 6.1, identifies its cone and
anisotropic norms on the standard collision section `N`; it does not bound
the maps from the transparent-wall coordinates in `M` through every return
prefix/suffix.

For each physical homogeneous subbranch `b` of every prefix and suffix, a
sufficient quantitative ledger must freeze finite constants

```text
C_reg(b)   : regular-density pushforward / pullback,
C_sf(b)    : mass + Reg_alpha + Z after canonical subdivision,
C_flux(b)  : mass + Reg_alpha + Z_partial + Atl_2,
C_test(b)  : dynamic-Holder and C1 face-test pullback,
C_ov(b)    : overlap/multiplicity and endpoint assembly.
```

The needed global constants are finite positive sums/maxima over all words,
levels and canonical homogeneous subbranches, for example

```text
C_src = sum_(w,j,b) max(C_reg(b),C_sf(b),C_flux(b)) C_ov(b),
C_test = sum_(w,j,b) C_test(b) C_ov(b).             (2.1)
```

Then (1.3) would extend by density to the two completed Banach pairs, and
the source-side and test-side Wiener/CM2 norms would be intertwined with
constants `C_src` and `C_test`.  The finite word count and `r(w)<=9` make the
outer `(w,j)` sum finite.  They do **not** prove that the inner homogeneous
subbranch sums in (2.1) converge.

For a dispersing billiard the missing quantities are physical and familiar:

- a lower incidence/transversality scale or a summable homogeneity-strip
  replacement;
- inverse collision Jacobian and logarithmic-distortion sums;
- the one-step expansion/cutting sum controlling `Z` after all singular
  cuts;
- `C2` carrier curvature and coarea-density regularity through prefix and
  suffix maps;
- exact assembly of coincident artificial faces before the flux norm;
- separation-time compatibility and `C1` trace bounds for the pulled-back
  physical tests.

The existing grouped/reflection certificate supplies these bounds on one
positive-width two-row orbit by exact Euclidean isometry.  It is not a cover
of the return partition, and the unresolved grazing collars in Gate 3 are
precisely where the global constants can diverge.

## 3. Exact countermodels: finite height is not a norm bound

These countermodels are deliberately elementary.  They do not assert a
failure of the pilot; they prove that the already certified combinatorial
facts cannot logically imply the required analytic bounds.

### 3.1 One Borel branch can destroy the regular and test norms

Take the single height-one branch

```text
H:[0,1]->[0,1],      H(x)=x^2.
```

The pushforward of Lebesgue density has

```text
rho(y)=1/(2 sqrt(y)).
```

At `y=1/n^2`, both `rho(y)` and the derivative of the inverse test pullback
`H^{-1}(y)=sqrt(y)` equal `n/2`.  Thus the pushed density has infinite BV
variation at zero and the inverse `C1` test-pullback norm is unbounded.  The
same `n/2` is the inverse tangent-speed/coarea factor for a one-dimensional
face.  Return height is one, the branch collection is finite, and its domain
is Borel.  What fails is quantitative transversality/distortion.

### 3.2 Finite cutting can have an arbitrarily large curve norm

A unit curve of mass one has the model source cost

```text
1 + 1/|W| = 2.
```

Split it into `n` disjoint image components, each of mass `1/n` and length
`1/n`.  Their positive-decomposition cost is exactly

```text
sum_(j=1)^n (1/n)(1+n) = n+1.
```

For every `n` this is a finite Borel height-one partition, yet no bound can
depend only on the return height.  In the physical proof the missing
replacement is the canonical homogeneity subdivision plus a uniform
one-step expansion/boundary-growth estimate, including the face atlas mark.

### 3.3 Bounded roof does not imply phase aperiodicity

The two-state graph

```text
0 --1--> 1 --1--> 0
```

is finite, strongly connected and has height two, but every cycle has even
weight.  Its cycle gcd is two and its phase transfer matrix has the exact
eigenvector `(1,-1)` with eigenvalue `-1`.  The corresponding centered phase
correlation does not decay.  Thus `K_N<=9` cannot replace the actual cycle
gcd-one check.  This is the finite-graph version of the constant-roof-two
counterexample already recorded in v52.

## 4. Exact remaining Gate-5 frontier

The present status by layer is:

```text
FINITE_BOREL_PREFIX_SUFFIX_ALGEBRA:          CERTIFIED
EXACT_SOURCE_TEST_ADJOINT_PAIRING:           CERTIFIED
EXACT_NORMALIZED_KAC_TOWER_PAIRING:          CERTIFIED
LOCAL_REFLECTION_SOURCE_TEST_ISOMETRY:       CERTIFIED (one orbit)

GLOBAL_REGULAR_PREFIX_SUFFIX_BOUND:          NOT CERTIFIED
GLOBAL_STANDARD_FAMILY_NORM_INTERTWINER:     NOT CERTIFIED
GLOBAL_FLUX_FACE_NORM_INTERTWINER:           NOT CERTIFIED
GLOBAL_PHYSICAL_TEST_NORM_INTERTWINER:       NOT CERTIFIED
ACTUAL_RETURN_PHASE_GRAPH_CYCLE_GCD_ONE:     NOT CERTIFIED
GATE_5:                                      NOT CERTIFIED
```

This separates the combinatorial finite-height conclusion from the genuine
analytic problem.  Completing Gate 3's grazing-collar normal forms is not
merely bookkeeping for Gate 5: those normal forms must export the precise
distortion, cutting, coarea and test-pullback constants entering (2.1).
After that, a finite weighted return graph and a cycle-gcd-one replay would
close the remaining phase layer.

## 5. Reproduction

```bash
python -m py_compile \
  deliverables/cm2_gate5_prefix_suffix_norm_cert.py \
  deliverables/cm2_gate5_prefix_suffix_norm_verifier.py

python deliverables/cm2_gate5_prefix_suffix_norm_cert.py
python deliverables/cm2_gate5_prefix_suffix_norm_verifier.py --self-test

# Expected exit 2 until the physical constants and phase graph are present.
python deliverables/cm2_gate5_prefix_suffix_norm_verifier.py
sha256sum -c \
  deliverables/cm2-gate5-prefix-suffix-norm-manifest-2026-07-15.sha256
```

The positive certificate and verifier self-test exit zero.  The live
fail-closed verifier exits two by design.
