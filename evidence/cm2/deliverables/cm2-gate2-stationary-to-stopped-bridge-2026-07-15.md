# CM2 Gate 2: stationary-to-stopped projective Frostman bridge

Date: 2026-07-15 (Asia/Shanghai)  
Scope: a new Gate-2 bridge theorem; frozen v51/v52 are not edited  
Verdict: **the bridge is proved, but the physical pilot remains OPEN**

## 1. Result

The missing finite-depth, every-stopped-parent projective estimate does not
need to be assumed separately once two stronger objects have been built for
the **same physical future kernel**:

1. a spatial Frostman estimate for its stationary projective marginal; and
2. pointwise convergence from every initial base/projective state in a
   Holder test norm.

The precise loss in passing from stationary spatial regularity to a sharp
indicator of an interval is explicit.  If the stationary exponent is
`alpha`, the test exponent is `theta`, and the mixing rate is `tau`, then
the finite-depth remainder is

```text
rho_stop^N,        rho_stop = tau^(alpha/(alpha+theta)).
```

This supplies exactly the conditional law required by the projective
terminal criterion in frozen v52.  It does **not** construct the physical
quotient, prove stationary Frostman regularity for its countable
place-dependent cocycle, or identify the projective coordinate with the
physical endpoint tangent.

## 2. The bridge theorem

### Theorem 2.1 (stationary Frostman plus pointwise Holder mixing)

Let `K` be a Markov kernel on a compact state space `E` carrying a projective
coordinate `pi:E -> P^1`, and let `eta` be a `K`-stationary probability.
Work in one fixed compact affine projective chart.  Suppose there are

```text
0 < alpha <= 1,    0 < theta <= 1,    0 < tau < 1,
C_F < infinity,   C_mix < infinity
```

such that:

1. for every chart interval `I`,

   ```text
   eta{pi in I} <= C_F |I|^alpha;
   ```

2. for every `theta`-Holder function `f:E -> R`, every `x in E`, and every
   `n>=0`,

   ```text
   |K^n f(x) - eta(f)|
     <= C_mix tau^n (||f||_infinity + [f]_theta).
   ```

Then there is a constant `C`, depending only on the displayed data and the
fixed chart, such that, uniformly in `x`, `n`, and `I`,

```text
K^n(x,{pi in I})
  <= C ( |I|^alpha + tau^(alpha*n/(alpha+theta)) ).          (2.1)
```

The same estimate holds after conditioning on an arbitrary stopped past
whose future law is a mixture of initial states for this same kernel.
If a named cemetery has conditional mass at most `C_0 exp(-c_0 n)`, its mass
is added to the right side.

#### Proof

For `0<delta<=1`, choose a cutoff `f_delta` equal to one on `I`, zero outside
the `delta`-neighbourhood `I^delta`, and satisfying

```text
0 <= f_delta <= 1,       [f_delta]_theta <= C delta^(-theta).
```

The two assumptions give

```text
K^n(x,{pi in I})
 <= eta(f_delta) + C_mix tau^n(1+C delta^(-theta))
 <= C_F(|I|+2delta)^alpha
      + C_mix tau^n(1+C delta^(-theta)).                     (2.2)
```

Use `(a+b)^alpha <= a^alpha+b^alpha` up to a fixed chart constant and set

```text
delta_n = tau^(n/(alpha+theta)).
```

Then both `delta_n^alpha` and
`tau^n delta_n^(-theta)` equal
`tau^(alpha*n/(alpha+theta))`.  The harmless term `tau^n` is smaller.
This proves (2.1).  Integrating its pointwise bound against any conditional
law of the stopped initial state proves the arbitrary-parent assertion.
The cemetery contribution is a union bound.  QED.

### Corollary 2.2 (prescribed logarithmic depth and normalized amplitude)

Let

```text
N(r) = ceil(C_buf log(1/r)).
```

Then every exponent strictly below

```text
Theta_raw = min {
  alpha,
  C_buf |log tau| alpha/(alpha+theta),
  C_buf c_0
}
```

is a raw stopped-parent projective small-ball exponent.  If, on the same
stopped tree, a positive physical amplitude satisfies

```text
E[(A/E[A|parent])^p | parent] <= C_A,       p>1,
```

conditional Holder gives every weighted exponent below
`Theta_raw/p'`.  Thus Theorem 2.1 feeds the projective terminal criterion
and the nonlinear part of PPE1--PPE2 without transferring a marginal bound
by disintegration.

The normalized amplitude moment remains an independent physical input.

## 3. Exact applicability audit

| Required input | Current pilot | Consequence |
|---|---|---|
| One full-mass physical future kernel on every stopped parent | **absent** | The two pilot matrices are a negative-pressure subsystem, not the whole collision-SRB law. |
| Pointwise Holder mixing for that kernel | **absent** | No finite/countable product transfer operator has been instantiated on the pilot common vertex. |
| Stationary spatial Frostman for that kernel | **absent** | Rush 2026 is compactly supported i.i.d.; it is not the countable place-dependent billiard kernel. |
| Same carrier/projective endpoint identity | **absent** | Periodic-orbit trivializations have not been transported to the physical endpoint carrier. |
| Parentwise normalized amplitude moment | **absent** | Raw amplitude moments do not control `A/Z_A`. |

Therefore this result closes a genuine **logical bridge**, not Gate 2.

## 4. Exact literature route and latest-technology check

There is also an exact finite-depth theorem with the desired small-ball
shape in the independent-map setting.  Gorodetski--Kleptsyn--Monakov,
*Holder regularity of stationary measures*, Inventiones Mathematicae
(online 19 November 2025), arXiv:2209.12342v1, Theorem 2.6, proves that if a
probability law `mu` on bi-Lipschitz maps of a compact manifold has a
positive moment of the bi-Lipschitz constant and its support has no common
invariant measure, then for every initial probability `nu_0`,

```text
(mu^{*N} * nu_0)(B_r(x)) <= C (r^alpha + kappa^N).            (4.1)
```

Theorem 2.8 gives a uniform version for a predeclared sequence of
independent, non-identically distributed laws from a compact family, under
the stronger `no deterministic images` condition.  This is already the
finite-depth arbitrary-initial-law form needed by frozen v52; no stationary
limit or indicator smoothing is required.

For the exact two-matrix pilot Bernoulli model, finite support gives the
moment automatically and the existing noncoaxial proximal/SIP certificate
supplies the relevant nondegeneracy.  Thus (4.1) rigorously supports the
**artificial i.i.d. benchmark**.

It does not certify the physical collision-SRB kernel.  Its random maps are
chosen independently from a state-independent law (or from a predeclared
nonstationary sequence of such laws).  In the actual reverse quotient,
`p_a(x)=rho(h_a x)|h_a'(x)|/rho(x)` depends on the current base point and
the next base point depends on the chosen branch.  This adaptive
place-dependent Markov/Gibbs law is not Theorem 2.6 or 2.8.  Restricting it
to the two pilot branches again gives the forbidden negative-pressure
subsystem.

```text
arXiv:2209.12342v1
doi:10.1007/s00222-025-01389-y
sha256 18d248b5f955d39679f04e57b30d29434587471fe78ee2d97f7907f22332a8d0
```

The pointwise mixing input is available as a theorem for a substantial
Markov-cocycle class.  Cai--Duraes--Klein--Melo, *Holder continuity of the
Lyapunov exponent for Markov cocycles via Furstenberg's Formula*,
arXiv:2212.00174v1, Theorem 4.1, proves

```text
||Q^n f - eta(f)||_infinity <= C sigma^n ||f||_alpha
```

for the projective Markov operator on `Sigma x P(R^m)`.  Its hypotheses are:

- `Sigma` is compact;
- the base Markov kernel is continuous and uniformly ergodic;
- the matrix cocycle is Lipschitz;
- the cocycle is quasi-irreducible; and
- its top Lyapunov exponent is simple.

This is precisely the **mixing half** of Theorem 2.1, including uniformity
over the initial base and projective state.  It still does not prove spatial
Frostman regularity of the stationary projective marginal.  For the pilot it
also remains to certify that the collision-SRB reverse kernel is continuous
and uniformly ergodic on one compact quotient and that the billiard cocycle
is a bounded Lipschitz cocycle there; the current countable homogeneity
presentation does not make those facts automatic.

PDF audited in this assault:

```text
arXiv:2212.00174v1
sha256 e4a075ef0127b5860ac0533a4a16a6e7b78813320acbe69f07ceebb274819767
```

Abdoulaye Thiam, arXiv:2604.24057v2 (28 April 2026), Theorem 1.5 and
Proposition 8.5, concern a finite-state irreducible aperiodic Markov cocycle
and state a product-operator Holder spectral gap.  If that theorem is
instantiated together with a stationary **spatial** Frostman estimate, it
provides the mixing input of Theorem 2.1.

It does not itself provide the other input.  In particular Proposition 7.1
is Holder/Wasserstein continuity of the stationary measure as the matrix
law changes; it is not an estimate of the form `eta(I)<=C|I|^alpha` in the
projective variable.  The current billiard quotient is also neither a
certified finite-state Markov chain nor a certified locally constant
cocycle.

PDF audited in this assault:

```text
arXiv:2604.24057v2
sha256 7000a657f8aba517cd948dc82732539b48559e0ce788b81f0cc9314a6a6cec0f
```

Tom Rush, arXiv:2601.14061v1, supplies a stationary Furstenberg Frostman
theorem under compactly supported i.i.d. SIP assumptions.  It does not
supply a place-dependent/countable physical kernel or the same-carrier
endpoint typing.  Thus the two 2026 papers cannot simply be concatenated
for the pilot.

The newer Liu--Lu--Shi--Wang preprint, *Exponential mixing and
Freidlin--Wentzell large deviation principle for Markov cocycles*,
arXiv:2607.06242v2 (updated 13 July 2026), concerns Markov processes/SPDEs in
random environments and exponential attraction in a Wasserstein metric
under random Lyapunov and coupling hypotheses.  It is not a projective
linear-cocycle spatial-regularity theorem and supplies neither the pilot
matrix kernel nor a stationary Frostman estimate.

```text
arXiv:2607.06242v2
sha256 037d2789745ce9e085cb8d404d1be70d5a804675630ea1351f8a3f7672c2abe6
```

## 5. New minimal Gate-2 target

After this bridge, the projective part of Gate 2 can be attacked by one
falsifiable package on a declared physical common vertex:

1. construct its full-mass collision-SRB quotient and product kernel;
2. prove a uniform pointwise Holder spectral gap for that kernel;
3. prove stationary spatial Frostman regularity for its projective marginal;
4. certify that arbitrary stopped parents restart the same kernel (or a
   uniformly controlled family to which Theorem 2.1 applies);
5. transport the projective state to the actual endpoint tangent and prove
   the normalized amplitude moment on the identical tree.

The earliest hard stop remains item 1, which is coupled to the unresolved
actual common vertex in Gate 1.

Equivalently, one may try to extend the GKM energy-regularization theorem
from independent laws to the pilot's adaptive Markov kernel.  Theorem 2.8
does not already perform that extension.
