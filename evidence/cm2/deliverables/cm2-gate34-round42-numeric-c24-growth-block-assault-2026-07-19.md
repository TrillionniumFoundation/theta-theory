# CM2 Gate 3/4 Round-42 numerical C24 Growth block assault

Date: 2026-07-19  
Verdict: **the hereditary C24 standard-family Growth block is now fully
numerical in exact symbolic form; the scheduled projective block and final
collision-time payload remain open**

## 1. What Round 41 left nonnumerical

Round 41 installed the correct all-mass extra-cut operator and hereditary
C24 killing, but retained theorem-supplied density, metric and chopping
prefactors.  The frozen closed-map standard family already supplied

```text
density ratio R=2000/1999,
theta=900337/901685,
delta_1=1/37724355673552103994.
```

The only missing numerical input was a uniform finite pullback scale keeping
all intermediate images inside the `delta_1` regime.

## 2. Explicit square-root image-length bound

On a smooth ray-circle branch write

```text
Delta=R_1^2-w^2=R_1^2 c_1^2,
a=u dot d=tau+sqrt(Delta).
```

Every constant-`w` level has stable slope

```text
-kappa_0-c_0/a<-25/9,
```

while an unstable graph has slope greater than `25/9`.  On
`Delta<=R_1^2/4`, this gives the exact lower derivative

```text
|dDelta/dr|>=(4/25)*(36337/800000)*(50/9)
             =36337/900000.
```

The frozen global upper derivative is `53748/625<100`.  Since `w` is
strictly monotone, the low-discriminant set has at most two components.
Splitting low and high discriminant regions yields

```text
integral dr/c_1
 <(13032674/36337)*sqrt(length_E(W)).
```

With `A=tau*(kappa_0+V)+c_0<427/4` and image slope `<29`, therefore

```text
length_E(T_s W)
 <C_len*sqrt(length_E(W)),
C_len=5962448355/5191.
```

This is uniform for every physical smooth branch and every fixed
`|s|<=1/400`.

## 3. Numerical pullback scale and block

Define

```text
delta_(j+1)=(delta_j/C_len)^2,
delta_open=(5/27)*delta_9148.
```

Equivalently,

```text
delta_n
=5191^(2^n-2)
 /(37724355673552103994^(2^(n-1))*5962448355^(2^n-2)).
```

No giant rational is materialized; its bases and integer exponents are
frozen exactly.  The metric comparison gives `length_E<=delta_9148` whenever
the adapted length is at most `delta_open`, so all first 9147 images remain
below `delta_1`.  Also `delta_open<10^-90`, hence the existing invariant
density cone and ratio `2000/1999` apply unchanged.

Including the density ratio once, the exact block coefficient is

```text
gamma
=(2000/1999)*(1+48*9148)*(900337/901685)^9148
<1/2.
```

Depth `9147` fails, so `9148` is minimal in this explicit half-contraction
scheme.  The resulting constants are

```text
n_*=9148,
Z0=2/delta_open=54/(5*delta_9148),
Z1=18367592526/360493663.
```

Thus every unnormalised C24-killed canonical family satisfies

```text
Z(O_s^9148 G)<=gamma Z(G)+Z0 mass(G),
Z(O_s G)<=Z1 Z(G).
```

## 4. Exact block-index aggregate resolvent

Let

```text
rho=(111718729/111718750)^9148,
w_Z=(1+rho^(-1))/2.
```

Then `w_Z>1`, `w_Z*rho<1` and `w_Z*gamma<3/4`.  With
`C=Z0/(1-gamma)`, the common scheduled-block recurrence has the explicit
bound

```text
sum_(p>=0) w_Z^p z_p
 <=z_0/(1-w_Z*gamma)
   +C*m_0*w_Z/((1-w_Z*gamma)*(1-w_Z*rho)).
```

This is an exact block-index result.  The collision block is
`9148*N_open`, and `N_open` remains theorem-supplied and nonnumerical.
Therefore no numerical collision-time `q`, full `C_fw/C_rev`, cemetery, or
Gate-4 closure is claimed.

## 5. Strict boundary

```text
numeric n_*,Z0,Z1:             CERTIFIED_EXACT_SYMBOLIC
hereditary C24 killed Growth:  CERTIFIED_NUMERICAL_BLOCK
block-index aggregate Z:       CERTIFIED_EXACT_SYMBOLIC
numeric N_open:                NOT CERTIFIED
collision-time q:              NOT CERTIFIED
Gate 4:                        NOT CERTIFIED
CM2:                           NO-GO_FOR_CLAIM
```

## 6. Validation

The suite passes syntax, pinned dependencies, strict JSON and independent
exact replay.  It rejects `24/24` hostile mutations.  Both certificate and
verifier default modes exit `2` and preserve the `NO-GO_FOR_CLAIM` boundary.
