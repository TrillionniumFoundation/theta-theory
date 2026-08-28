# CM2 Gate 5 Round-46 Piola F16 assault

Date: 2026-07-19  
Verdict: **area-preserving Piola naturality removes the nonempty-suffix
derivative product exactly.  The all-five-face arbitrary-suffix F16
`flux_face_operator_cost` is certified, advancing Gate 5 to `10/18`.**

## 1. Exact suffix cancellation

Let `S` be one regular homogeneous suffix branch in collision area
coordinates.  Then

```text
det(DS)=1.
```

For a source current `J` on a physical face `Gamma`, use

```text
J'(Sx)=DS(x)J(x),
n' dH1_on_SGamma=cof(DS)n dH1_on_Gamma.
```

The matrix identity

```text
DS^T cof(DS)=det(DS)I=I
```

gives the pointwise flux equality

```text
J' dot n' dH1_on_SGamma
  = J dot n dH1_on_Gamma.
```

Consequently, for every test `h`,

```text
|integral_SGamma h J' dot n' dH1|
 <= ||h||_infinity TV(source flux)
 <= ||h||_C1 TV(source flux).
```

The suffix derivative multiplier is exactly one.  Piecewise homogeneous
cuts do not change this upper bound; adjacent artificial traces are assembled
before absolute values.

## 2. All-face arbitrary-suffix F16

Round 44 already supplies the same-ID all-face two-trace flux charge at each
Duhamel insertion.  Piola pushforward transports that charge through every
finite regular suffix without `D_suffix`.  Therefore

```text
c_F16,n <= c_F13,n
          <= (3816937/7800000)c_X,n
          <= (3816937/47112000)c_D1,n.
```

The bound covers all five physical face grammars and inherits the physical
`L^(6/5)` moment and block tail exponent `1/6`.  This certifies the global
parameterized F16 `flux_face_operator_cost` and advances Gate-5 maturity

```text
9/18 -> 10/18.
```

Complete 18-field blocks remain zero.

## 3. Round-45 obstruction retyped

The Round-45 product

```text
TV(trace)*(1+D_suffix)
```

is a valid generic C1 pullback majorant, and its moment countermodel remains
correct for that route.  It is not the geometric F16 flux transformation.
Piola naturality bypasses the product rather than proving its moment finite.

## 4. Strict frontier

The following are not promoted:

1. the complete strong F13 current intertwiner;
2. cemetery-compatible F16;
3. full all-face F10;
4. F14, F15, F17, F18 and the induced common-space coefficient;
5. dynamic `MT_DQ` and the strong cemetery.

Gate 5 therefore remains open at `10/18`.

