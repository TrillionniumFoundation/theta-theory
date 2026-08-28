# Technical note: Brownian-bridge proof of the sharp fractional-Sobolev rough rate

Let `h=1/N`, let `P_NB` be Brownian polygonal interpolation, and write

\[
\beta_k(t)
=B_{kh+t}-B_{kh}-\frac{t}{h}(B_{(k+1)h}-B_{kh}),
\qquad 0\le t\le h.
\]

The processes `beta_k` are independent Brownian bridges and

\[
\beta_k(t)\overset{d}=h^{1/2}\beta(t/h).
\]

## 1. First level

For the local fractional seminorm,

\[
\int_0^h\int_0^h
\frac{|\beta_k(t)-\beta_k(s)|^p}{|t-s|^{1+\eta p}}dsdt
\overset{d}=
 h^{p/2+1-\eta p}Z_k,
\]

where `Z_k` are i.i.d. nonnegative variables with finite moments.  Summing the disjoint local terms gives

\[
\|B-P_NB\|_{W^{\eta,p}}
\le C N^{-(1/2-\eta)}
\]

in every finite `L^q`, after adding the cross-interval terms by the fact that each bridge vanishes at its interval endpoints.

## 2. Second level

Use Chen's identity interval by interval.  The difference between the Brownian lift and the polygonal lift is a sum of:

1. local bridge iterated integrals, which scale as `h`;
2. cross terms containing one bridge increment and one coarse increment.

The local `W^{2\eta,p/2}` contribution scales as `N^{-(1-2\eta)}` before the rough-metric square root.  The cross terms are bounded by the first-level bridge norm times a Brownian/coarse-path norm with finite moments.  Therefore

\[
\left\|\mathbb B-\mathbb {P_NB}\right\|_{W^{2\eta,p/2}}^{1/2}
\le C N^{-(1/2-\eta)}
\]

in finite moments.  This proves the upper rough-path estimate.

## 3. Lower bound

Let `A_N` be the set of paths affine on every mesh interval.  On each interval the quotient of `W^{\eta,p}` by affine functions has a strictly positive Brownian-bridge moment.  Restricting to the middle third removes endpoint interactions.  If `D_k` denotes the resulting local quotient seminorm, Brownian scaling gives

\[
D_k^p\overset{d}=h^{p/2+1-\eta p}D^p.
\]

The variables are independent and `P(D>c_0)>c_1`.  A binomial concentration bound implies that with probability bounded away from zero, at least a fixed fraction of the intervals satisfy `D_k>c_0h^{1/2+1/p-\eta}`.  Hence

\[
\operatorname{dist}_{W^{\eta,p}}(B,A_N)
\ge cN^{-(1/2-\eta)}
\]

with probability bounded away from zero, and therefore also in expectation.

The distance functional is 1-Lipschitz and vanishes on `P_NB`; Kantorovich duality proves the matching Wasserstein lower bound.
