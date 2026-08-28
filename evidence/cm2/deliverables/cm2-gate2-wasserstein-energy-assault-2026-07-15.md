# CM2 Gate 2: Wasserstein and Markov-energy positive route

Date: 2026-07-15 (Asia/Shanghai)  
Scope: direct Gate-2 continuation; frozen v51/v52 and the shared research log are not edited  
Verdict: **two weak-metric bridges and an adaptive pilot energy certificate are proved; physical Gate 2 remains OPEN / NO-GO**

## 1. Executive result

The previous audit proved that the exact inverse-branch SRB kernel cannot mix
from points in total variation: its finite-time laws are countably atomic,
whereas its physical stationary density is non-atomic.  This does **not**
block a weak-metric route.

This assault proves three positive statements.

1. **Wasserstein-to-stopped bridge.**  Exponential convergence in the
   Wasserstein metric for the snowflaked cost `d^theta`, together with a
   stationary spatial Frostman bound, gives the same finite-depth,
   arbitrary-initial-state small-ball estimate as Holder-test mixing.  The
   full-mass dyadic reverse kernel is the exact sanity check: its finite-time
   TV distance from Lebesgue is maximal, but its Wasserstein error is
   `O(2^-n)`.

2. **Direct Markov-energy bridge.**  A uniform two-copy truncated Riesz
   energy drift gives finite-depth Frostman bounds from every point without
   constructing a stationary projective law and without any TV or iid
   hypothesis.  It is therefore the shortest positive target for the
   place-dependent physical kernel.

3. **Adaptive pilot certificate.**  On the certified projective interval
   `K=[5,7]`, the exact pilot maps `Phi_g,Phi_w` satisfy the energy drift for
   arbitrary place/history-dependent weights in `[1/5,4/5]`.  With

   ```text
   alpha = 1/20,
   kappa = (17/25) 169^(1/20) = 0.878826710130965... < 1,
   ```

   one obtains

   ```text
   nu_N(I)
     <= (1-kappa)^(-1/2) |I|^(1/40) + kappa^(N/2).
   ```

   The strict inequality is certified exactly by

   ```text
   169 * 17^20 < 25^20.
   ```

   This removes independence from the algebraic two-map benchmark.  It does
   not turn the two maps into a full-mass physical return kernel.

The assault also proves a scale-normalized Holder lemma which converts a
relative amplitude regularity bound into the parentwise normalized moment of
`A/Z_A`.  This closes the normalization algebra on a clean component, but an
exhaustive physical amplitude registry and its global conditional moments
remain absent.

## 2. Wasserstein-to-stopped theorem

### Theorem 2.1 (weak-metric stationary bridge)

Let `K` be a Markov kernel on a compact metric state space `(E,d)`, let
`pi:E -> R` be a projective coordinate in one fixed compact affine chart,
and let `eta` be stationary.  Fix `0<alpha,theta<=1`.  Suppose

```text
eta{pi in I} <= C_F |I|^alpha
```

for every chart interval `I`, and suppose that for every initial state `x`

```text
W_{d^theta}(K^n(x,.),eta) <= C_W tau^n,       0<tau<1.       (2.1)
```

Here `W_{d^theta}` is the Kantorovich distance for the snowflaked cost
`d(x,y)^theta`; equivalently it controls tests that are Holder-`theta` in
the original metric.  Then, uniformly in `x,n,I`,

```text
K^n(x,{pi in I})
  <= C ( |I|^alpha + tau^(alpha*n/(alpha+theta)) ).          (2.2)
```

The same estimate holds after an arbitrary stopped past whose physical
future is a mixture of initial states for this same kernel.  A named
cemetery of conditional mass `epsilon_n` is added to the right side.

#### Proof

Let `f_delta` be one on `I`, zero outside the `delta`-neighbourhood, and
Holder-`theta` with seminorm at most `C delta^-theta`.  Kantorovich duality,
stationary Frostman regularity, and (2.1) give

```text
K^n f_delta(x)
 <= C_F(|I|+2 delta)^alpha
       + C C_W tau^n delta^-theta.
```

Set `delta=tau^(n/(alpha+theta))`.  Both error terms become
`tau^(alpha*n/(alpha+theta))`.  Integrating the pointwise bound against an
arbitrary stopped initial distribution proves the stopped-parent assertion.

### Exact reason this route survives the TV obstruction

For the full-mass dyadic reverse kernel

```text
h_0(x)=x/2,       h_1(x)=(x+1)/2,       p_0=p_1=1/2,
```

the depth-`n` law from `x` is uniform on

```text
{(x+k)/2^n : 0<=k<2^n}.
```

It has TV distance one from Lebesgue at every finite depth.  Nevertheless,
same-label coupling gives

```text
W_1(K^n_x,K^n_y) <= 2^-n |x-y|.
```

Couple the point `(x+k)/2^n` with a uniform point in the `k`-th dyadic cell
to obtain

```text
W_1(K^n_x,Leb) <= 2^-n.
```

Thus atomic finite-time laws are fully compatible with exponentially small
Wasserstein error.  The CDKM/Doeblin no-go was topological, not a no-go for
weak metrics.

## 3. Direct pair-energy theorem

The preceding theorem still needs a stationary projective Frostman law.  The
following criterion bypasses that input.

### Theorem 3.1 (uniform truncated Riesz drift)

Let `P` be a Markov kernel on `E` and let `pi:E -> K` take values in a compact
real interval.  For `0<alpha<=1` and `0<r<=1` put

```text
V_r(u,v) = max(r, |pi(u)-pi(v)|)^(-alpha).
```

Suppose there are `0<kappa<1` and `C_0<infinity` such that, for every
`u,v` and every `r`,

```text
(P tensor P)V_r(u,v) <= kappa V_r(u,v) + C_0.               (3.1)
```

The two copies choose their next branches conditionally independently; the
branch probabilities may depend arbitrarily on the current states.  Then for
the projective marginal `nu_{n,u}` of `P^n(u,.)` and every interval `I` of
length `r`,

```text
nu_{n,u}(I)
 <= sqrt(C_0/(1-kappa)) r^(alpha/2) + kappa^(n/2).           (3.2)
```

The estimate is uniform in the initial state and hence in every stopped-parent
mixture.  A named cemetery of mass `epsilon_n` adds `epsilon_n`.

#### Proof

Start two copies at the same state `u`.  Iterating (3.1) gives

```text
E V_r(U_n,V_n)
 <= kappa^n r^-alpha + C_0/(1-kappa).                       (3.3)
```

If both projective coordinates lie in `I`, their distance is at most `r`, so
`V_r=r^-alpha`.  Therefore

```text
nu_{n,u}(I)^2
 <= r^alpha E V_r(U_n,V_n)
 <= kappa^n + C_0 r^alpha/(1-kappa).
```

Taking square roots proves (3.2).  No stationary limit, independence in time,
or disintegration of a marginal Frostman law is used.

### Corollary 3.2 (two separated maps with adaptive weights)

Let `phi_0,phi_1:K->K` satisfy

```text
|phi_i(z)-phi_i(w)| >= ell |z-w|,
dist(phi_0(K),phi_1(K)) >= g,
```

and let the current weight `p` of `phi_0` lie in `[eta,1-eta]`; it may depend
on the entire current state/history.  For `r<=min(1,g)`, the same-map terms
in the pair kernel are at most

```text
{eta^2+(1-eta)^2} ell^-alpha V_r,
```

while the cross-map terms are at most `g^-alpha`.  Thus (3.1) holds with

```text
kappa={eta^2+(1-eta)^2} ell^-alpha,
C_0=g^-alpha,
```

whenever `kappa<1`.

### Certified pilot constants

The frozen exact projective certificate gives

```text
Phi_g([5,7]) subset (5,11/2),
Phi_w([5,7]) subset (13/2,7),
dist(Phi_g(K),Phi_w(K)) > 1,
Phi_i'(z) > 1/169.
```

Take `eta=1/5` and `alpha=1/20`.  The maximum same-map pair coefficient for
two possibly different current weights `p,q in [1/5,4/5]` is

```text
max {pq+(1-p)(1-q)} = 17/25.
```

The exact integer inequality displayed in Section 1 proves `kappa<1`.
Hence Corollary 3.2 applies to arbitrary adaptive weights, not merely a
Bernoulli chain.  Numerically,

```text
kappa = 0.878826710130965...,
sqrt(kappa) = 0.937457577776704....
```

This is a true place-dependent projective Frostman benchmark.  It remains an
algebraic benchmark because the physical quotient has not been shown to have
exactly these two children carrying all mass at every stopped parent.

## 4. Parentwise normalized amplitude from relative Holder control

### Lemma 4.1 (scale-normalized amplitude lemma)

Let `J` be an interval, let `lambda_J` be normalized Lebesgue measure on it,
and let a probability `mu` satisfy

```text
dmu/dlambda_J >= m > 0.
```

Let `A>=0` be nonzero and Holder-`theta`, put `M=||A||_infinity`, and assume

```text
|J|^theta [A]_theta <= L M.                                 (4.1)
```

Set

```text
delta = min{1,(2L)^(-1/theta)},
```

with `delta=1` when `L=0`.  Then

```text
Z_A=int A dmu >= (m delta/2) M,
||A/Z_A||_infinity <= 2/(m delta),                           (4.2)
int (A/Z_A)^p dmu <= {2/(m delta)}^(p-1).                   (4.3)
```

#### Proof

At a maximum point `x_0`, (4.1) implies `A>=M/2` on the intersection of `J`
with the radius-`delta |J|` interval around `x_0`.  This intersection has
`lambda_J`-mass at least `delta`.  The density floor gives (4.2).  Since
`int(A/Z_A)dmu=1`, (4.3) follows from
`W^p<=||W||_infinity^(p-1)W`.

Thus a uniform density floor and a uniform **relative** scaled Holder ratio
close the normalized moment on every clean parent.  If `L` is a random
parent mark, (4.3) reduces the required moment to a conditional moment of
`1+L^((p-1)/theta)`.

This lemma does not apply to an unstructured indicator `A=1_E`; its relative
Holder ratio diverges at the cut.  It therefore respects the exact
normalization counterexample from the previous assault.

For the current billiard proof this gives a concrete positive target:
positive compact-core coarea/chart amplitudes already have scaled
log-Holder bounds, so each predeclared clean component has the desired
normalized moment after its density floor is recorded.  What is still absent
is one exhaustive registry covering all stopped descendants, high-rank
homogeneity pieces, recovery marks, and endpoint handlers with a uniform
conditional moment of the resulting `L`.

## 5. Exact physical audit

The direct energy theorem identifies a strictly weaker and more appropriate
physical target than TV mixing.  It has not yet been instantiated.

| Required physical object | Current status |
|---|---|
| One-state full-mass quotient on the actual common magnet | **OPEN**: no explicit base interval, full return partition, stable quotient, or full-mass branch registry has been constructed. |
| Actual reverse weights `p_a(x)=rho(h_a x)|h_a'(x)|/rho(x)` | **conditional formula proved**, but `rho,h_a` are not instantiated on the pilot. |
| Common projective chart and every transported branch map | **OPEN**: the two periodic maps are certified and the local invariant graphs now exist, but the true common vertex/full-cross transport is still missing. |
| Full countable pair-energy inequality (3.1) | **OPEN**: only the adaptive two-map algebraic core is certified. |
| Countable tail in the same pair-energy norm | **OPEN**: needs a joint moment of branch co-Lipschitz losses and cross-image near-collisions, not merely a marginal return tail. |
| Actual stopped antichain and every-parent restart | **OPEN**: `NST_phys` remains an interface. |
| Same-carrier endpoint identity | **OPEN**: the Mobius/wedge algebra is exact, but the transported projective variable has not been pointwise identified with the actual endpoint tangent on the PPE carrier. |
| Exhaustive amplitude registry and normalized moment | **OPEN globally**: Lemma 4.1 closes clean components under a relative scaled Holder mark, but the complete registry and its conditional mark moment are missing. |

Consequently no physical Gate-2 promotion is made.

## 6. Minimal next certificate

The shortest positive continuation is now finite and falsifiable.

1. Finish Gate 1's two-graph common vertex and record one actual common
   projective chart.
2. Build the full return alphabet `a`, the exact inverse branches `h_a`, and
   the normalized physical weights `p_a`; do not truncate and renormalize.
3. For a growing compact branch-pair atlas, interval-certify the left side of
   (3.1).  Charge the omitted branch pairs with one joint
   co-Lipschitz/near-collision moment until the total coefficient is strictly
   below one.
4. Freeze the endpoint carrier record and certify the nonzero endpoint wedge
   on the same accepted continuations.
5. Generate the amplitude registry before the query and verify the density
   floor plus the relative scaled Holder mark in Lemma 4.1 on every retained
   parent; charge all failures to named cemeteries.

This route needs neither total-variation Doeblin nor an iid Markovization of
GKM.  Failure of the strict pair coefficient `kappa<1` would be a genuine
falsification of this particular route, rather than an ambiguity about which
mixing topology is intended.

## 7. Literature boundary

The exact literature boundary from the preceding audits is unchanged.

- Gorodetski--Kleptsyn--Monakov Theorems 2.6/2.8 give finite-depth Frostman
  estimates for independent map laws, not state-adaptive physical weights.
- Cai--Duraes--Klein--Melo Theorem 4.1 assumes base uniform ergodicity in TV,
  which is impossible for a non-atomic inverse-branch quotient from points.
- Rush 2026 gives stationary Furstenberg regularity in an iid compact setting.
- Thiam 2026 gives parameter regularity/product-operator mixing for a
  finite-state Markov class, not spatial Frostman regularity for this
  countable billiard kernel.

The Wasserstein and pair-energy theorems above are proved directly, so no
unsupported extension of any of these sources is used.  A targeted arXiv
query through 2026-07-15 found no newer theorem which supplies the missing
full-mass place-dependent billiard pair-energy or endpoint typing.

## 8. Reproduction

Run

```bash
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_wasserstein_energy_cert.py
```

Expected positive lines include

```text
DYADIC_W1_DEPTHS=0..16: EXACT_CONTRACTION_2^-n
KAPPA^20=169*(17/25)^20<1: EXACT
RAW_INTERVAL_EXPONENT=1/40
WEAK_METRIC_AND_ENERGY_BRIDGES: POSITIVE_CERTIFICATE
```

The script deliberately ends with

```text
PHYSICAL_FULL_MASS_PROJECTIVE_KERNEL: NOT_CERTIFIED
PHYSICAL_STOPPED_PARENT_PPE: NOT_CERTIFIED
```

so the positive bridge cannot be mistaken for physical Gate-2 closure.
