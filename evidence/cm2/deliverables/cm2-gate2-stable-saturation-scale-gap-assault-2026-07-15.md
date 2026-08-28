# CM2 Gate 2: stable-saturation scale and full-mass complement audit

Date: 2026-07-15 (Asia/Shanghai)  
Model: frozen centered rational fixed-section pilot  
Precision: 900-bit Arb through `python-flint==0.9.0`  
Verdict: **the actual single stable leaf and two local physical crossings
remain certified, but the present 96-word tube is smaller than the relevant
stable endpoint separation by a factor greater than `8.29e65`, and the two
enumerated raw source strips occupy less than `9.7%` of the common
rectangle's collision-SRB mass.  Stable saturation, a full-mass physical
quotient, and Gate 2 remain OPEN / NO-GO.**

## 1. What this audit corrects

The predecessor did more than find a numerical near-hit.  At 2400 bits it
proved that the **actual** stable leaf of the 96-collision point meets the
common-chart face `v=0`, and it proved a positive-width physical 96-word
rectangle around that crossing.  Therefore the remaining statement must
not be described as “the single stable leaf has not been continued”.  That
leaf-level continuation is certified.

The missing geometric object is stronger:

```text
an interval-indexed family of actual stable plaques,
uniformly physical on a common source/target product,
invariant under the declared return branches,
with a physical stable-holonomy Jacobian.
```

The new certificate quantifies exactly how far the existing *uniform tube*
falls short of the already known leaf segment, and then measures how much
physical mass is absent from the current finite branch registry.

## 2. Exact stable-scale gap

In either Perron chart the reversible 96-word fixed point has zero physical
momentum, hence transverse coordinate

```text
v(z_*)=a_*,
a_*=-8.293762194329601963437427046452104...e-15.
```

The certified actual stable-leaf crossing lies on `v=0`.  Thus the
transverse separation between the two certified endpoints is exactly
`|a_*|`.  The physical 96-word rectangle about the crossing has transverse
half-height

```text
r_v=1e-80.
```

The 900-bit calculation gives

```text
|a_*|/r_v > 8.29e65,                                      (2.1)
|a_*|-r_v > 8.29e-15.                                    (2.2)
```

The common rectangle has half-height `r=4.2e-15`, so

```text
r/r_v = 4.2e65,                                           (2.3)
r_v/r < 2.39e-66.                                         (2.4)
```

Equations (2.1)--(2.4) do **not** say that the actual stable leaf is absent;
it is present.  They say that the current uniform first-hit/cone certificate
only controls a microscopic endpoint tube.  It does not control a tube
along the whole leaf segment or a plaque through each point of a positive
unstable interval.  Reusing this raw rectangle as a full-height common
product is therefore rigorously impossible without a new continuation.

For completeness, the predecessor's crossing-location uncertainty is less
than `8.53e-172`, while the unstable half-width of the new strip is
`8e-68`; their ratio is

```text
< 1.07e-104.                                               (2.5)
```

So the problem is not localization of the one crossing.  It is uniform
two-dimensional continuation and leaf consistency.

## 3. A physical mass obstruction to promoting the two raw strips

The normalized collision-SRB density is constant in arclength--momentum
coordinates `(s,p)`.  In a Perron chart

```text
delta s=u+v,      delta p=k(u-v),
```

the absolute Jacobian is `2k`.

The common QNL rectangle has half-width `r=4.2e-15`.  Its certified QNL
source is full-height and has unstable width

```text
10^-17-(-8e-16)=8.1e-16.
```

Consequently its exact collision-SRB mass fraction inside the common
rectangle is

```text
(8.1e-16)/(2r)=27/280
 =0.0964285714285714....                                  (3.1)
```

The complete second raw rectangle has half-widths
`(r_u,r_v)=(8e-68,1e-80)`.  Reconstructing the loop and QNL Perron slopes
from the frozen orbit gives

```text
0.999999999999999999999999
 < k_loop/k_QNL
 < 1.000000000000000000000001.
```

Even charging the **entire** loop rectangle against the common base (rather
than only its intersection) yields

```text
(k_loop/k_QNL) r_u r_v / r^2 < 4.54e-119.                (3.2)
```

The two strips are already certified disjoint.  Combining (3.1)--(3.2),

```text
enumerated physical fraction < 0.097,
unregistered complement       > 0.903.                   (3.3)
```

Thus the two currently certified raw branches cannot themselves be a
full-mass first-return partition of the common rectangle.  At least the
`>90.3%` complement needs a genuine return/singularity/component registry.
This is a strict measure statement, not an appeal to lack of computation.

Equation (3.3) does not rule out completing the partition with countably
many additional branches.  It proves that those branches, their domains,
and their weights cannot be omitted.

## 4. Exact implication boundary

The current certified chain is

```text
actual single W^s(z_*) endpoint continuation          CERTIFIED
positive-width 96-word physical crossing              CERTIFIED
second local crossing in the common rectangle         CERTIFIED
uniform tube along the full stable endpoint segment   NOT CERTIFIED
interval-indexed invariant plaque family              NOT CERTIFIED
common physical stable holonomy/Jacobian              NOT CERTIFIED
two onto quotient inverse branches                    NOT CERTIFIED
full-mass countable return partition                   NOT CERTIFIED
stable-quotient density rho and physical p_a           NOT INSTANTIATED
countable pair-energy tail and stopped-parent PPE      NOT CERTIFIED
same-carrier endpoint/amplitude registry               NOT CERTIFIED
physical Gate 2                                        NOT CERTIFIED
```

The local stable-manifold/graph-transform theorem at one hyperbolic orbit
does not supply the missing interval-indexed family unless its iterated
domains and invariant plaque family are also constructed.  Likewise,
Poincare recurrence gives an almost-everywhere two-dimensional first return,
but its reverse kernel is deterministic before quotienting actual stable
leaves.  Neither theorem converts (2.1) or (3.3) into the required physical
random inverse kernel.

## 5. Minimal constructive continuation

The smallest honest next certificate is now:

1. cover the actual stable segment from `v=0` to `v=a_*` by correlated
   first-hit boxes, uniformly over a positive unstable parameter interval;
2. prove overlap compatibility and graph-transform invariance, thereby
   producing an interval-indexed physical stable plaque family;
3. certify source/target stable holonomy and its conditional-SRB Jacobian;
4. enumerate the `>90.3%` complement into a full-mass first-return alphabet,
   including all singular/homogeneity/context cuts;
5. instantiate `rho`, `h_a`, `p_a`, off-diagonal projective collision bounds,
   the native stopping antichain, endpoint typing, and normalized amplitudes.

The present report closes none of those layers by fiat.  It converts the
remaining Gate-2 gap into two exact, independently checkable quantities.

## 6. Reproduction

```bash
python3 -m py_compile \
  deliverables/cm2_gate2_stable_saturation_scale_gap_cert.py \
  deliverables/cm2_gate2_stable_saturation_scale_gap_manifest_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_stable_saturation_scale_gap_cert.py

python3 \
  deliverables/cm2_gate2_stable_saturation_scale_gap_manifest_verifier.py \
  --self-test

python3 \
  deliverables/cm2_gate2_stable_saturation_scale_gap_manifest_verifier.py
# expected exit 2: the physical snapshot is intentionally fail-closed

sha256sum -c \
  deliverables/cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.sha256
```

No v51/v52 file or shared research log is modified by this audit.
