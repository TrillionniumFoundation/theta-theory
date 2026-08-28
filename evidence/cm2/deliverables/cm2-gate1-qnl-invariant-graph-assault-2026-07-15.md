# CM2 Gate 1 continuation: a validated QNL invariant graph

Date: 2026-07-15 (Asia/Shanghai)  
Scope: explicit Gate 1 invariant-manifold layer  
Frozen inputs: v51/v52 and their frozen certificates were read, not edited  
Final Gate 1 status: **OPEN / NO-GO FOR PHYSICAL COMMON VERTEX**

## 1. New certified result

The affine QNL eigentangent used in
`cm2_gate1_tangent_line_matching_cert.py` has now been upgraded, on the QNL
side only, to an actual local unstable manifold.

Let `(s,p)` be gray arclength--momentum coordinates at the exact gray--white
normal two-cycle and let

```text
k = sqrt(gamma/beta),
s = x+y,
p = k(x-y).
```

Thus `x` and `y` are respectively the unstable and stable eigen-coordinates
of the exact two-solid-collision return `F=(A,B)`.  The new 300-bit Arb
certificate proves that on

```text
|x| <= 2e-9,     |y| <= (2e-9)^2,
```

the physical word is exactly

```text
G(0,0) -> W(0,0) -> G(0,0),
```

and that there is a unique local unstable graph

```text
W^u_loc(QNL) = {(x,h(x)): |x| <= 2e-9}
```

in the declared graph-transform class, with

```text
|h(x)|  <= x^2,
|h'(x)| <= 1e-4.
```

This is an invariant-graph statement.  It is not interpolation of manifold
samples and it does not identify the eigentangent with the manifold.

## 2. Fail-closed graph-transform audit

The script implements two-variable second-order interval automatic
differentiation through both circle collisions.  It encloses the value,
Jacobian and Hessian of the exact return on the entire graph domain.  The
center derivative is

```text
diag(11.097701933801484225..., 0.0901087455731885047...),
```

up to Arb radii below `1e-84`.  On the full domain it proves

```text
m_A := inf(A_x-|A_y|L)       > 11.097,
Lip(Gh)                      < 4.07e-5 < L=1e-4,
graph-transform contraction < 0.0902 < 1,
quadratic image constant     < 1.08e-3 < C=1.
```

Here `G` is the forward graph transform reparameterized by the unstable
coordinate.  Since `m_A>1`, every target `x` in the declared interval has a
unique graph preimage whose unstable coordinate contracts by at least
`m_A`.  The displayed contraction gives the unique fixed graph.  Its
backward iterates converge to the QNL point, so the fixed graph is the local
unstable manifold.  The certified nonzero Jacobian and the strict physical
word make this a `C^2` local diffeomorphism; standard graph-transform
regularity upgrades the fixed Lipschitz graph to `C^1`, with the certified
derivative cone.

The quadratic tube follows from Taylor's theorem at the fixed point:

```text
B(x,y) = mu*y + (1/2) D^2B(xi)[(x,y),(x,y)],
```

using `B_x(0)=0`, the full interval Hessian, and the projection lower bound
`m_A`.  No unvalidated floating-point curvature estimate enters the
acceptance test.

The physical margins on the whole domain are

```text
minimum flight          > 0.187105,
minimum discriminant    > 0.02559999,
minimum incidence       > 0.99999,
minimum clearance       > 0.364982.
```

All endpoints are proved to remain in `(0,1)^2`.  The frozen `[-3,3]^2`
lift enumeration is exhaustive because an omitted gray or white lift has a
coordinate gap at least three, and `3-9/25>2`.

## 3. Ten-collision replay and the remaining numerical obstruction

At the certified affine shooting abscissa

```text
x = -1.396101069259116746830594312272814e-9,
```

the new theorem puts the unknown exact graph ordinate in

```text
|h(x)| <= 1.9491e-18.
```

The certificate propagates this entire ordinate tube through the immutable
ten-collision QNL word.  Every flight retains the declared first target and
strict flight/discriminant/incidence/clearance margins, so the physical
replay is certified for the true QNL manifold point.

However, ordinary interval propagation produces the terminal enclosure

```text
theta_terminal    = 0.8 +/- 0.0216,
momentum_terminal =       +/- 0.0371.
```

This is a dependency/wrapping bound, not the geometric size of the image.
It is vastly wider than the affine matching Krawczyk box.  Therefore this
run does not recycle the old tangent-line root into a true matching claim.
A Taylor-model/parameterization evaluation of the graph image is needed
before the true two-graph Krawczyk step can be attempted efficiently.

## 4. What remains open

The following are not certified:

1. a validated local `W^s(connector)` graph with a value and derivative
   enclosure at `u≈2.1861e-12`;
2. a correlation-preserving ten-plus-fourteen collision evaluation of both
   actual graphs;
3. a Krawczyk inclusion for the true matching map
   `T^10 gamma_A^u(t)-T^-14 gamma_B^s(u)`;
4. the reverse true intersection, explicit common vertex, four-face full
   crossing, and transported twisting.

The sharp next computational object is not a wider raw Arb state box.  It is
a polynomial/Taylor-model parameterization of the connector invariant graph
and of the two finite transition images, with a separately certified tail.

## 5. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_qnl_unstable_graph_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_qnl_unstable_graph_cert.py
sha256sum -c \
  deliverables/cm2-gate1-qnl-invariant-graph-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The script exits zero only after the invariant graph, its physical local
word, and the whole ten-collision graph-tube replay succeed.  It then prints
fail-closed labels for the connector graph, true heteroclinic matching and
full-cross common vertex.
