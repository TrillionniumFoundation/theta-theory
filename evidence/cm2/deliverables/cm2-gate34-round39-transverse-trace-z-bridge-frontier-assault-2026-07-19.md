# CM2 Gates 3/4 round 39: transverse-trace to canonical-Z frontier

Date: 2026-07-19  
Status: **the missing interface between the scheduled projective strong tail
and canonical parent-`W` standard-family `Z` is now exactly typed and its
allowable rate loss is explicit; the interface itself remains unproved**

## 1. The two certified objects have different types

Round 38 controls the killed density in the Demers--Liverani projective
order norm:

```text
||K_s^k f||_* < K_cone r^k mass(f),
r=111718729/111718750.
```

Round 35 supplies canonical same-ID parent-`W` carriers

```text
phi(r)=4r+b,
p(r)=sin(4r+b).
```

Their slope `4` lies strictly in the certified global unstable cone

```text
25/9 < dphi/dr < 4108425/145348.
```

The projective object is a two-dimensional density tested by stable-curve
averages.  The canonical standard family is a one-dimensional unstable
disintegration carrying conditional density and boundary Growth `Z`.
Therefore the exact missing map is a bounded same-ID **transverse trace /
canonical disintegration operator**.  Neither the parent registry nor the
projective strong tail currently contains this operator.

## 2. Stable tests alone do not provide the trace

Straighten the stable leaves to horizontal segments and the canonical
transversal to `I={x=0}`.  On `(-1,1)^2`, put

```text
u_epsilon(x,y)=max(1-|x|/epsilon,0).
```

For every horizontal segment `J`,

```text
integral_J u_epsilon dx <= min(length(J),2 epsilon).
```

At the projective short-leaf exponent `q=1/4`, this gives

```text
sup_J length(J)^(-1/4) integral_J u_epsilon
 <= (2 epsilon)^(3/4) -> 0.
```

The stable-leaf transverse comparison is exactly zero because the density
is independent of `y`, and the two-dimensional mass is `2 epsilon -> 0`.
Yet

```text
u_epsilon restricted to I = 1
```

for every `epsilon`.  Thus the currently recorded stable-test controls alone
do not bound the required transverse trace.  This is a typed logical model,
not an impossibility theorem for an augmented cone: a new trace/boundary-`Z`
seminorm may still close the interface.

## 3. Exact rate budget for any future bridge

Suppose a same-ID canonical bridge satisfies

```text
Z_can(K_s^k f) <= A_k ||K_s^k f||_*,
limsup A_k^(1/k) <= gamma.
```

The unweighted `Z` tail requires

```text
gamma*r < 1,
gamma < 111718750/111718729
      = 1 + 21/111718729.
```

Round 38 uses

```text
w=223437479/223437458,
w*r=223437479/223437500.
```

Preserving its weighted Green sum requires the sharper condition

```text
gamma*w*r < 1,
gamma < 223437500/223437479
      = 1 + 21/223437479.
```

Fixed or polynomial bridge loss has asymptotic root growth `1` and is
compatible with both strict margins.  A generic doubling loss `A_k~2^k`
fails both.  The quantitative target is therefore extremely narrow but
fully explicit.

## 4. Strict installation boundary

```text
MISSING TRANSVERSE TRACE INTERFACE:     CERTIFIED EXACTLY LOCATED
CANONICAL SAME-ID PARENT-W REGISTRY:   CERTIFIED PREVIOUSLY
SCHEDULED PROJECTIVE STRONG TAIL:      CERTIFIED PREVIOUSLY
BOUNDED CANONICAL TRACE OPERATOR:      NOT CERTIFIED
CANONICAL STANDARD-FAMILY Z TAIL:      NOT CERTIFIED
NUMERIC C_fw / C_rev / q:              NOT CERTIFIED
GATE 3 / GATE 4 / CM2:                 NOT CERTIFIED / NO-GO
```

The shortest admissible construction is an augmented projective cone with
a canonical transverse trace/boundary-`Z` component whose block loss is
subexponential.  The independent fallback remains a direct full-`Q_N`
characteristic estimate `C_N a^N<1`.

## Evidence

- `deliverables/cm2_gate34_round39_transverse_trace_z_bridge_frontier_cert.py`
- `deliverables/cm2_gate34_round39_transverse_trace_z_bridge_frontier_verifier.py`
- `deliverables/cm2-gate34-round39-transverse-trace-z-bridge-frontier-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, exact dyadic arithmetic,
independent replay and live fail-close pass.  The verifier rejects `21/21`
hostile mutations.
