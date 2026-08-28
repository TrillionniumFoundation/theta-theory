# CM2 Gate 5 Round-47 two-trace and F10-seed assault

Date: 2026-07-19  
Verdict: **the finite-regular-path two-trace boundary measure is embedded in
`(C1)*`, and affine C24 core edges gain a rank-zero F10 seed.  Neither result
contains the bulk Duhamel current or the all-face same-measure join, so Gate-5
maturity remains `10/18`.**

## 1. Two-trace `(C1)*` sublayer

At the Round-44 base parameter `s=0`, write the signed boundary measure as

```text
B=sigma*(tau_plus-tau_minus).
```

For every finite regular suffix `S`,

```text
||(S_*B)||_(C1)* <= TV(S_*B) <= TV(B),
```

because the `C1` norm dominates the supremum norm.  Constant-test
cancellation is preserved, and the existing same-ID charge remains

```text
c_F13,n <= (3816937/47112000)c_D1,n.
```

This is only the two-trace boundary sublayer.  The complete insertion current
is

```text
T=-div(K)+B,   K=X*(P_j h)*mu.
```

At source time,

```text
||T||_(C1)*
 <= (c_X+c_F13)||h||_infinity
 = (11616937/47112000)c_D1||h||_infinity
 < (1/4)c_D1||h||_infinity.
```

After a nonempty suffix the safe bulk bound still pays

```text
D_suffix*c_X+c_F13,
D_suffix=product_i(150*2^B_i).
```

Piola cancellation removes the normal-flux multiplier, not this bulk or
tangential test-pullback cost.  The exact family
`diag(L,L^-1)` preserves flux while multiplying a `C1` gradient by `L`, which
prevents a false promotion to complete strong F13.

## 2. Rank-zero affine C24 core-edge F10 seed

In collision area coordinates `(r=R*theta,p=sin(phi))`, a cross-colour
translation has Eulerian generator

```text
X^r=eta*(sin(theta)-(p/c)*cos(theta)),
X^p=(eta/R)*(c*sin(theta)-p*cos(theta)),
c=sqrt(1-p^2).
```

It is divergence-free.  On every C24 output edge,
`|p|<=1/50`, `c>19/20`, and `R>=4/25`, hence

```text
|X|_1 < 5621/760 < 8,
||DX||_(column l1) < 28105/608 < 47.
```

For an affine core edge with normal-flux density `a=X dot n`,

```text
|a|+|partial_tau a| < 163009/3040 < 55,
partial_s a = 0
```

in the pure-translation moving frame.  This closes the intermediate/terminal
affine C24 core-edge seed only.

If the missing same-measure arbitrary-`R_n` join were later proved, the
existing `35*2^B` reverse and `68*2^B` forward occurrence costs plus 192
oriented core traces would fit the target ledger

```text
103/151 + (192*55)/(151*2^14)
 = 26533/38656 < 1.
```

That target is not asserted as a current theorem.

## 3. Frozen Piola regression

The suite now freezes the previously transient exact audit:

- 180 integer matrices in `[-4,4]^4` with determinant one;
- two current vectors and two normal measures per matrix;
- 720 exact source/pushed flux equalities.

The case-row digest is independently recomputed by the verifier.  This is a
regression test for the symbolic identity `DS^T cof(DS)=I`, not a substitute
for it and not an extra Gate-5 field.

## 4. Exact frontier

Full all-face F10 still needs the occurrence/coarea-to-same-ID path-measure
join and corner/quotient-to-cemetery classification.  Complete strong F13
still needs an F17-type dynamic-test bound or a joint insertion/suffix rank
tail, followed by return-depth convergence and cemetery domination.  F14,
F15, F17, F18 and dynamic `MT_DQ` remain open.

Gate-5 maturity therefore stays `10/18`, with zero complete 18-field blocks.

