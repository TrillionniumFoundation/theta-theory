# Platform `FB4-PE-v1`

## Deterministic phase space

An invertible area-preserving four-branch baker collision map on the unit square.
For macro current `a in (-1,1)` the branch weights are

\[
w_1=(1-a)/6,\quad w_2=(1-a)/3,\quad
w_3=3(1+a)/14,\quad w_4=2(1+a)/7.
\]

The reference preparation at `a0=2/5` has weights `(1/10,1/5,3/10,2/5)`.
Lebesgue area is the natural physical measure.

## Mechanical current and derived parameter

The branch winding is `(-1,-1,+1,+1)`.  Conditioning the base system on mean
current `a` yields

\[
\theta(a)=I'(a)=\frac12\log\frac{3(1+a)}{7(1-a)}.
\]

The canonical tilted branch law is exactly the Lebesgue branch law of the map
with weights `w(a)`.

## Mechanical slow port

\[
d_1=(2,0),\ d_2=(-1,0),\ d_3=(0,4),\ d_4=(0,-3),
\]

\[
\tau_1=\tau_2=2,\qquad \tau_3=\tau_4=1.
\]

Hence

\[
C(a)=\operatorname{diag}(1-a,6(1+a)),\qquad
\bar\tau(a)=(3-a)/2.
\]

## Role

This is the load-bearing deterministic-first-principles platform for the v6
series.  `OB3-MG-v1` remains a specular physical application, `FB4-EXACT-v1`
is subsumed as its response benchmark, and `SL-SIM-v1` remains a conjugacy
control.  Cross-platform conclusions require explicit bridge theorems.
