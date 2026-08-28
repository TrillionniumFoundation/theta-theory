# CM2 Gate 5 Round 44: all-face suffix two-trace F13

Date: 2026-07-19  
Status: **the global regular-density Borel F13 payload is certified on every
finite regular `R_n` path; Gate-5 maturity advances to `8/18`**

## Verdict

Round 43 bounded each Eulerian insertion but stopped before suffix
propagation.  The missing propagation is now closed at the measure level:
for every local positive trace `tau` and regular suffix `S`,

```text
tau_suffix=S_*tau,
mass(tau_suffix)=mass(tau).
```

Thus suffix derivatives never enter Borel total variation.  Prefix regular
branches preserve the `L^infinity` norm in collision area coordinates.

## 1. Exact C24 boundary flux

The 24 C24 rectangles have 96 physical edges and 192 oriented
inside/outside traces.  Using

```text
R_G=9/25, R_W=4/25,
Delta t=1/100,
Delta p_axis=1/250,
Delta p_diagonal=1/25,
|dtheta/dt|<1001/1000 or 1401/1000,
Z_N>156/25,
```

their total normalized `l1` boundary measure is

```text
<469439/1950000.
```

Since `|X|_1<=25*2^B`, one positive core-boundary trace has flux

```text
<(469439/78000)*2^B ||h||_infinity,
```

and the two oriented traces together have TV

```text
<(469439/39000)*2^B ||h||_infinity
 =(469439/975000)c_X,j ||h||_infinity.
```

This controls every intermediate and terminal C24 preimage face after
Eulerian change of variables; the suffix merely pushes the two positive
measures forward.

## 2. Physical occurrence traces

The complete depth-one DQ atlas already supplies

```text
64 physical current rows,
128 hit/miss traces,
one-sign positive mass <=8064/5,
signed current TV <=16128/5.
```

For the rank convention `B>=14`, one insertion has

```text
c_X,j=25*2^B>=409600,
(16128/5)/409600=63/8000.
```

Hence the whole occurrence current obeys

```text
TV(J_occ,j)<=(63/8000)c_X,j ||h||_infinity.
```

For every suffix the immutable two-trace formula is

```text
tau_(n,j,e,sign)=(S_(n,j))_*tau_(e,sign)(P_(j-1)h),
J_(n,j,e)=sigma_e(tau_hit-tau_miss).
```

Constant-test cancellation is preserved exactly.

## 3. All-five-face join

The five physical grammars are covered as follows:

1. source-core clipping: zero parameter current in the fixed common source
   coordinates;
2. intermediate core preimage: C24 edge flux plus suffix pushforward;
3. terminal core preimage: the same edge-flux construction;
4. collision singularity/owner change: complete corrected depth-one face
   current plus Duhamel suffix;
5. moving occurrence: the 64-row/128-trace occurrence current plus suffix.

Internal chart and homogeneity cuts cancel by quotient trace before absolute
values.  They are not retyped as physical F13 faces.

The 3,286,976 symbolic roof-level factors induce a lazy envelope of
210,366,464 trace-pair slots and 420,732,928 oriented slots.  Empty slots are
allowed; these counts are not claimed as nonempty physical components.

## 4. Same-ID physical tail

Adding core and occurrence sectors gives the exact pointwise factor

```text
c_F13,n<=(3816937/7800000)c_X,n
       <(1/2)c_X,n
       =(25/302)c_D1,n.
```

Therefore the suffix-pushed two-trace charge inherits, on the same physical
`R_n` IDs,

```text
global L^(6/5) moment: CERTIFIED,
weighted block exponent: 1/6.
```

The collision-time rate remains nonnumerical because the Gate-4 hit block is
still nonnumerical.

## 5. Strict boundary

```text
arbitrary-R_n suffix two-trace TV ledger:      CERTIFIED
all-five-face regular-density Borel F13:       CERTIFIED
physical F13 L^(6/5) moment and block tail:    CERTIFIED
complete strong F13 intertwiner:               NOT CERTIFIED
F12 C1 trace pullback:                         NOT CERTIFIED
all-face standard-family F16 cost:             NOT CERTIFIED
full F10 / strong cemetery / F14--F18:         NOT CERTIFIED
dynamic MT_DQ:                                 NOT CERTIFIED
Gate-5 maturity / complete blocks:             8/18 / 0
Gate 5 / CM2:                                  NOT CERTIFIED / NO-GO
```

F16 gains a certified regular-density boundary-flux input, but not its
standard-family/strong operator cost.  Dynamic `MT_DQ` still needs the common
moving branch-record atlas, quotient convergence and cemetery domination.

## Evidence

- `deliverables/cm2_gate5_round44_all_face_suffix_two_trace_f13_cert.py`
- `deliverables/cm2_gate5_round44_all_face_suffix_two_trace_f13_verifier.py`
- `deliverables/cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json`

