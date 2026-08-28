# CM2 Gate 1: common-plaque transport and IFT frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen input: the determinant-one biprojective half-density reduction  
Strict verdict: **the coupled all-pair equations are reduced exactly to a
common `2x2` linear transport on every nondegenerate stable or unstable
plaque.  Small amplitude alone does not certify the required bounded inverse
or critical decay.  No physical coupled frame, uniform big-cell bound, or
same-representative twisting is promoted; Gate 1 remains open.**

## 1. Determinant-one frame form

Write

```text
a(x)=q(x)^(-1/2)(1,u(x))^T,
b(x)=q(x)^(-1/2)(v(x),1)^T,
q(x)=1-u(x)v(x).
```

Then `det(a,b)=1`, while the critical half-density coordinates are wedges:

```text
c_s(x,y)=det(a(x),a(y)),
c_u(x,y)=det(b(y),b(x)).
```

The certificate replays these identities exactly over the rationals.

## 2. Common-plaque transport lemma

On a local stable plaque the coupled stable equation is equivalent to

```text
det(a(sigma x),a(sigma y))
 = r(x) det(a(x),a(y))
```

for every pair.  If two columns on the plaque are noncollinear, their images
define a unique matrix `M_s`.  The pair identities force

```text
a(sigma z)=M_s a(z) for every z on the plaque,
det(M_s)=r.
```

Indeed, the coordinates of every third column in the two-anchor basis are
ratios of wedges; the common factor `r` cancels.  The time-reversed statement
holds for `b` on unstable plaques.  A four-vector rational replay verifies
the lemma and rejects a perturbed image that cannot arise from one common
transport.

This exposes the true remaining object: compatible future-plaque transports
`M_s`, past-plaque transports `M_u`, and one shared determinant-one frame
`[a,b]` that also preserves `q>=q_*>0` and twisting.

## 3. Why amplitude is not yet an IFT proof

For `u=epsilon u_0`, `v=epsilon v_0`, the scalar half-density multiplier has
zero first derivative at `epsilon=0`, but is generically nontrivial at order
`epsilon^2`.  The exact sample gives

```text
q_shift_product-q_source_product
 = -5 epsilon^2+13 epsilon^4
 = -487/10000 at epsilon=1/10.
```

After multiplication by `du`, the critical residual is generically cubic.
That is not enough by itself: a model residual

```text
epsilon^3 theta^n
```

becomes `epsilon^3(theta/r)^n` after critical diagonal normalization.  The
exact sample `r=1/16`, `theta=1/2` has ratio `8`, so every nonzero amplitude
eventually grows.  This is a fail-closed exponent warning, not a proof that
all physical gauges are impossible.

Consequently, a valid implicit-function argument still needs both:

1. a right inverse whose range preserves the common-plaque transport
   constraints;
2. a bound in the actual Hölder or anisotropic norm that beats critical
   diagonal amplification.

Neither bound is currently installed.

## 4. Technology audit

- Butler--Park `arXiv:1909.11548` assumes that canonical holonomies converge
  and are Hölder; it does not construct the present combined gauge.
- Kalinin--Sadovskaya `arXiv:2604.13401`, Theorem 1.3, requires conjugate
  periodic data, Hölder control of the periodic conjugacy at one periodic
  point, and sufficiently narrow periodic spectrum.  Those hypotheses are
  not the current half-density problem.
- An arXiv API search on 2026-07-17 found no theorem directly solving this
  non-fibre-bunched common-frame compatibility problem.

## 5. Strict boundary

```text
COMMON-PLAQUE TRANSPORT REDUCTION:          CERTIFIED
PLAIN SMALL-AMPLITUDE IFT PROMOTION:        REJECTED
BOUNDED ANISOTROPIC GREEN RIGHT INVERSE:    NOT CERTIFIED
COUPLED HALF-DENSITY FRAME:                 NOT CERTIFIED
UNIFORM q LOWER BOUND:                      NOT CERTIFIED
SAME REPRESENTATIVE CLASS H + TWISTING:     NOT CERTIFIED
GATE 1:                                     NOT CERTIFIED
```

The shortest constructive continuation is to solve directly for the common
plaque transports and their shared determinant-one frame, rather than to
iterate unrelated scalar pair residuals.
