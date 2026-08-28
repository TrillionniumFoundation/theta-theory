# CM2 Gate 5: finite-`s` physical prefix/suffix and Kac norm frontier

Date: 2026-07-16 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot  
Frozen inputs: v52, the ninth-pass Gate-3/4/5 manifests, the finite-`s`
common-mesh/recovery manifest, and the latest Gate-1/2 obstruction manifests
were read only

## Verdict

Gate 5 remains **`NOT_CERTIFIED`**, but its physical prefix/suffix frontier is
strictly advanced in three ways.

1. On the exact finite-signed-measure/bounded-Borel-test pair, every physical
   prefix and suffix now has the numeric operator constant **one**.  The
   endpoint return operator and its adjoint are contractions, while the Kac
   test sum and normalized phase lift have universal norm at most **nine**.
2. Binding these constants to the corrected 64-row current gives an explicit
   singular Kac output envelope:

   ```text
   global event-current TV                         <= 16128/5,
   two singular Kac coordinates in l1(TV)          <= 32256/5,
   worst height-nine phase lift of that pair       <= 290304/5.
   ```
3. The one-collision standard-family/recovery seed is now uniform on the
   complete parameter window `|s|<=1/400`: the geometric coefficient is
   `204`, the explicit initial boundary constant is
   `C_mesh=69986663973833932800`, and one-time controlled recovery holds for
   both orientations.

This is a genuine physical Borel norm lift, not merely a formal matrix
identity.  It is still weaker than all three CM2 lifts.  The complete
return-word operator registry, regular-density prefix/suffix bound,
return-wide standard-family/flux-face/dynamic-test CM2 intertwiners, full
four-term Kac output, and operator Wiener phase theorem remain open.  The
Growth Lemma constants are theorem-supplied but nonnumeric, and neither a
native stopping antichain nor hereditary repeated-cut recovery is claimed.

## 1. Exact physical Borel prefix/suffix constants

Let `(D_w)` be the disjoint Borel first-return partition and let `H_w` be the
physical endpoint map on `D_w`.  For a finite signed measure `nu`,

```text
L nu = sum_w (H_w)_*(nu|D_w).
```

Restriction is additive in total variation on a disjoint partition and a
deterministic pushforward contracts total variation.  Therefore

```text
||L nu||_TV
 <= sum_w ||nu|D_w||_TV
  = ||nu||_TV.                                      (1.1)
```

Dually, the partition selects exactly one return word at almost every point,
so

```text
||L^* phi||_infinity <= ||phi||_infinity.           (1.2)
```

The same argument applies to every individual physical prefix and suffix.
Thus a current inserted between them has multiplier at most one in TV, and
its test pullback has multiplier at most one in `L^infinity`.  No incidence,
inverse Jacobian, or distortion estimate is needed for (1.1)--(1.2); that is
special to this weak Borel pair.

The physical roof satisfies `1<=r_N<=9`.  Hence

```text
||S_XN h||_infinity <= 9 ||h||_infinity,
||E_NX nu||_TV      <= 9 ||nu||_TV.                 (1.3)
```

The second bound includes the Kac normalizer, since the mean roof is at least
one.  These are the first fully numeric global prefix/suffix constants on the
actual physical maps.

## 2. Corrected singular Kac output

The corrected maximal-row ledger has

```text
64  physical occurrences,
128 singular Kac coordinates,
(+1,-1) on the two coordinates of every occurrence,
global event-current TV <= 16128/5.
```

Using the direct-sum `l1(TV)` norm, the two singular coordinates therefore
cost at most

```text
2*(16128/5) = 32256/5.                              (2.1)
```

Applying the worst-case height-nine tower lift from (1.3) gives

```text
9*(32256/5) = 290304/5.                             (2.2)
```

Equations (2.1)--(2.2) coexist with the exact scalar identity
`mu(dot r)=0`; scalar cancellation is not used to reduce the arbitrary-test
TV envelope.  This prevents the familiar invalid promotion from a zero roof
mass to a zero signed current.

The other two terms in the four-term differentiated Kac identity are not
declared complete in the physical CM2 spaces.  Thus (2.2) is an explicit
singular Borel output, not the full physical CM2 Kac output.

## 3. Uniform finite-`s` one-collision and recovery seed

The finite-`s` common-mesh certificate upgrades all three one-collision
directions from the centred atom to every fixed `s` in `|s|<=1/400`:

- **dynamic test:** the bidirectional `C1` chart/test subcost is
  `151*2^B_s`, with a uniform first rank moment;
- **flux/face geometry:** both carrier `C2` bounds and both log-density
  costs are uniform, giving
  `C_fw^(geom)(s,a),C_rev^(geom)(s,a)<=204*2^B_s(a)`;
- **standard-family entry:** every controlled fixed-`s`, depth-`K`, one-time
  atom has both oriented standard-family representations, log-Hölder
  constant `52`, and

  ```text
  Z_s,fw(K,j), Z_s,rev(K,j)
      <= 69986663973833932800 * 2^K.
  ```

On the compact moving-table configuration class, the uniform Growth Lemma
supplies constants `C_p>1` and `0<vartheta_p<1`.  They are not numerically
evaluated.  With

```text
A0=ceil(log(C_mesh)/|log(vartheta_p)|)+1,
A1=ceil(log(2)/|log(vartheta_p)|),
```

the controlled one-time recovery clock obeys

```text
R_fw+R_rev <= 2A0+2A1 K,
```

and the product law `P(K)=(3/4)4^-K` gives

```text
E[2^K exp(gamma(R_fw+R_rev))] < infinity
for 0<gamma<log(2)/(2A1).
```

These facts live on the one-time occurrence/stopped-atom registry.  They do
not produce a native dynamical stopping antichain, do not recover
hereditarily after repeated indicator cuts, do not propagate through every
physical return prefix/suffix, and do not register every operator block.  The
precise missing composition layer is therefore

```text
complete return word
 -> every homogeneous prefix/suffix subbranch
 -> inverse Jacobian/distortion and cut growth
 -> face atlas and dynamic-test pullback
 -> completed three CM2 intertwiners.
```

The outer return depth is finite, but the inner homogeneity refinement is
countable near grazing and still needs a summable weighted ledger.

## 4. Exact reason the Borel constants do not close the three norms

Two exact countermodels remain decisive.

### 4.1 Fixed TV with unbounded curve boundary cost

Start with a unit curve of mass one and model cost `1+1/|W|=2`.  Split its
image into `n` components of mass and length `1/n`.  Total variation remains
one, while the positive-decomposition curve cost is

```text
sum_(j=1)^n (1/n)(1+n) = n+1.
```

At `n=64` the exact amplification is `65/2`.  Letting `n` increase shows
that the TV constant one cannot bound the standard-family `Z` term or the
flux-face cut/atlas norm.

### 4.2 Fixed TV with unbounded inverse test pullback

For the height-one branch `H(x)=x^2`, the pushed probability has density
`1/(2 sqrt(y))` and the inverse test pullback has derivative
`1/(2 sqrt(y))`.  At `y=1/n^2` both equal `n/2`.  Thus deterministic
pushforward is still a TV contraction while regular-density variation and
inverse `C1` test-pullback cost diverge.

The missing three-norm data are therefore logically independent of the new
Borel constants; they are not merely absent from the executable table.

## 5. Phase route

The actual standard-`N` component spanning graph already has weighted cycle
gcd one.  This removes the component period-two obstruction.  It does not
prove unit-circle invertibility of the operator polynomial because the
return-word operator blocks are not registered.

The preferred route remains `direct_standard_N`.  On that route no separate
phase tower is introduced, so component aperiodicity is not a new analytic
burden.  This route reduction is not labelled as Gate-5 completion: it still
needs Gates 1--4 and the direct-`N` three-space assembly.

## 6. Gates 1--2 bridge audit

No new cross-gate promotion is available.

- **Gate 1:** the exact QNL canonical stable limit fails with resonant
  coefficient `325/144`.  TV contraction of physical prefix/suffix maps acts
  on measures/tests and cannot change that cocycle-holonomy tail.  The
  cohomological/alternative-cocycle routes remain the only unrefuted routes.
- **Gate 2:** the Wasserstein/pair-energy theorem remains a valid weak-metric
  bridge, but the actual one-state full-mass quotient is absent.  The
  Gate-4 query-independent product-depth kernel is an auxiliary occurrence
  kernel, not a native physical inverse-branch quotient or stopping
  antichain.  It cannot be reused as `PPE_N`.

Thus neither Gate 1 nor Gate 2 changes status.

## 7. Latest technology audit

A live arXiv search on 2026-07-16 for moving scatterers, linear response for
Sinai/dispersing billiards, singular-measure Banach embeddings, cocycle
holonomies, and projective Frostman estimates found no newer applicable
bridge.  The closest sources remain:

1. Demers--Liverani, arXiv:2606.10155v1, whose Theorem 6.1 concerns the
   regular-density anisotropic space and whose Problem 8.7 records the
   characteristic-function restriction obstruction;
2. Stenlund--Young--Zhang, arXiv:1210.0011v4, whose uniform Growth Lemma and
   `Z` recovery supply the finite-`s` one-time recovery with theorem-level
   nonnumeric `C_p,vartheta_p`, not native repeated-cut recovery or
   return-wide prefix/suffix intertwiners;
3. Rush, arXiv:2601.14061, which concerns compactly supported i.i.d. matrix
   products and does not construct the physical billiard quotient;
4. Kalinin--Sadovskaya, arXiv:2604.13401, whose rigidity hypotheses do not
   provide the missing QNL cohomology.

No source found turns a Borel TV lift or a one-time standard-family seed into
the required return-wide three-space CM2 theorem.

## 8. Exact remaining Gate-5 boundary

```text
PHYSICAL BOREL TV/Linf PREFIX-SUFFIX CONSTANTS:       CERTIFIED
CORRECTED SINGULAR KAC BOREL OUTPUT ENVELOPE:         CERTIFIED
UNIFORM |s|<=1/400 ONE-COLLISION THREE-NORM SEEDS:   CERTIFIED
EXPLICIT INITIAL C_mesh=69986663973833932800:        CERTIFIED
UNIFORM ONE-TIME FINITE-s STOPPED-PARENT RECOVERY:   CERTIFIED
ACTUAL COMPONENT PHASE GCD ONE:                       CERTIFIED

COMPLETE RETURN-WORD OPERATOR REGISTRY:               NOT CERTIFIED
REGULAR-DENSITY PREFIX/SUFFIX INTERTWINER:             NOT CERTIFIED
NUMERIC THEOREM RECOVERY CONSTANTS C_p,vartheta_p:    NOT CERTIFIED
NATIVE DYNAMICAL STOPPING ANTICHAIN:                  NOT CERTIFIED
HEREDITARY REPEATED-INDICATOR-CUT RECOVERY:           NOT CERTIFIED
RETURN-WIDE STANDARD-FAMILY CM2 INTERTWINER:          NOT CERTIFIED
RETURN-WIDE FLUX-FACE CM2 INTERTWINER:                NOT CERTIFIED
RETURN-WIDE DYNAMIC-TEST CM2 INTERTWINER:             NOT CERTIFIED
FULL FOUR-TERM PHYSICAL KAC CM2 OUTPUT:                NOT CERTIFIED
OPERATOR WIENER PHASE TRANSFER:                        NOT CERTIFIED
GATE 5:                                               NOT CERTIFIED
```

## 9. Reproduction

```bash
python -m py_compile \
  deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_cert.py \
  deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_verifier.py

python deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_cert.py
python deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_verifier.py \
  --self-test
python deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_verifier.py \
  --replay --integrity-only

# Expected exit 2: stronger physical CM2 lifts remain fail-closed.
python deliverables/cm2_gate5_physical_prefix_kac_norm_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.sha256
```
