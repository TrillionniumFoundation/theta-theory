# CM2 Gate 5 — Round-43 Eulerian/Duhamel charge frontier

Date: 2026-07-19  
Verdict: **the arbitrary-path transport-current insertion charge is now
physical, same-ID and summable.  The suffix-propagated two-trace operator
field and complete F16 flux cost remain open.**

## 1. One-step Eulerian generator

Use collision area coordinates `(r,p=sin phi)`.  On every regular branch

```text
X_s=(partial_s F_s) composed with F_s^-1,
div_mu X_s=0.
```

Same-colour branches have `X_s=0`.  For cross-colour branches the exact
Round-41/42 ray-circle bounds give

```text
|X^r|<=75/(4 c_target),
|X^p|<=25/4,
|X|_1<=25*2^B.
```

Thus the generator has rank exponent one, not the cubic exponent of the raw
mixed/second coordinate jets.  The physical collision-SRB moment gives

```text
integral |X|^(3/2) dmu_s
 <25^(3/2) * 134217735/64
 =16777216875/64.
```

## 2. Exact finite-path Duhamel split

For regular area-preserving branch operators `P_j,s`,

```text
partial_s(P_n...P_1)
 =sum_j P_n...P_(j+1) (partial_s P_j) P_(j-1)...P_1,

partial_s P_j h=-div_mu(X_j P_j h).
```

With moving branch domains, the product rule separates exactly into

```text
F10: moving-face delta(G_j) partial_s G_j seed,
F13: Eulerian divergence/current insertion,
F16: normal flux of that current.
```

No second parameter derivative of the complete pulled-back face is used.

## 3. Same-ID physical charge

On every finite regular `R_n` path define the insertion charge

```text
c_X,n(x)=25 sum_(i=1)^n 2^B_i(x).
```

Round 35 already certified on the same physical components and common
forward/reverse carrier

```text
c_D1,n(x)=151 sum_(i=1)^n 2^B_i(x).
```

Hence

```text
c_X,n=(25/151)c_D1,n<c_D1,n.
```

The new charge inherits the global physical `L^(6/5)` component moment and
the block-exponent `1/6` weighted tail.  The safe moment bound is

```text
sum_(n,k) mbar_n,k cbar_X,n,k^(6/5)
 <K_rank N_open^3,

K_rank=3055930500533353804145008325576782226562500/453789.
```

The rate is still nonnumerical because `N_open` is nonnumerical.

## 4. Exact nonpromotion

This charge measures each Duhamel insertion before the suffix operator.  A
complete F13 field still needs the two oriented traces propagated through
every suffix on the same physical homogeneous IDs and their `C1` trace
pullback norm.  A complete F16 field additionally needs all-five-face normal
trace/operator costs, not only the pointwise affine normal-speed envelope.

```text
arbitrary-R_n Duhamel insertion charge:     CERTIFIED
one-step physical L^(3/2) generator bound: CERTIFIED
affine r/p normal-speed envelope:           CERTIFIED
arbitrary-R_n F13 two-trace operator field: NOT CERTIFIED
complete all-face F16 operator cost:        NOT CERTIFIED
full F10 / F12 / F13 / F14--F18:           NOT CERTIFIED
Gate-5 maturity:                            7/18 UNCHANGED
Gate 5 / CM2:                               NOT CERTIFIED / NO-GO
```

## 5. Validation

Pinned dependency replay and exact arithmetic pass.  The fail-closed verifier
rejects `31/31` hostile mutations; default execution returns exit code `2`.
