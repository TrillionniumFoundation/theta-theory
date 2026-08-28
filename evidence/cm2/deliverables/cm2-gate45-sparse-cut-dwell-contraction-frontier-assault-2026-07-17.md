# CM2 Gates 4/5: sparse-cut dwell-contraction frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the one-cut same-interval shell factor, the 24-core open
operator coefficient, and the all-`441280`-key field-7 characteristic factor  
Strict verdict: **arbitrarily many registered cuts now admit two deterministic
scheduled scalar Green ledgers.  The shell route contracts after each
`2018`-step core dwell; the raw all-key field-7 route contracts after each
`12108`-step dwell.  This removes an external cut-count tail from those
scheduled ledgers, but the physical incidence, no-hidden-recut schedule,
common strong-space typing, cemetery payload, and the other 17 fields remain
uncertified.  Gates 4 and 5 remain open.**

## 1. Sharpened fixed-core block

The frozen 24-core coefficient is

```text
b_core=720269600000/720626832337.
```

The previous certificate used `b_core^2018<1/2`.  Exact integer arithmetic
gives the stronger bound

```text
b_core^2018<3/8<1/2.
```

The certificate replays the full rational power comparison; its huge
numerator and denominator are represented in the manifest by a deterministic
witness digest rather than decimal rounding.

## 2. General scheduled ledger

For registered cut cycles let

```text
E_(h+1)<=lambda E_h+J_(h+1),  h>=0.
```

If `lambda<Lambda<1`, then

```text
E_h<=lambda^h E_0+sum_{j=1}^h lambda^(h-j)J_j.
```

Thus bounded injections give a pointwise ledger uniform in the arbitrary
registered cut count `h`.  More strongly, for `w>1` and `w Lambda<1`,

```text
sum_{h>=0} w^h E_h
 <=[E_0+sum_{h>=1}w^h J_h]/(1-w Lambda).
```

This is a deterministic dwell theorem.  It does not assume a probabilistic
geometric tail for the number of cuts.  Weighted summability of transported
injections is still required for the weighted `l1` conclusion.

## 3. Same-interval shell route

One registered same-interval cut in both orientation views costs strictly
less than `15/8`.  Following it by at least one `2018`-step fixed-core block
gives

```text
lambda_shell<(15/8)(3/8)=45/64<1,
1/(1-lambda_shell)<64/19.
```

The rational exponential cut weight `w=4/3` still contracts:

```text
w lambda_shell<15/16,
1/(1-w lambda_shell)<16.
```

Hence every history obeying this one-cut/one-dwell schedule has an
arbitrary-cut-count scalar Green ledger without a cut-count-tail hypothesis.

## 4. Raw all-key field-7 route

The uniform characteristic multiplier for all `441280` candidate keys and
every maximal return-word component is

```text
C_7=580000/1999.
```

Five coarse `3/8` blocks do not beat this loss; six are the first contracting
count for that certified coarse bound.  With `6*2018=12108` core steps,

```text
lambda_7
 <(580000/1999)(3/8)^6
 =13213125/16375808
 <1,

1/(1-lambda_7)<16375808/3162683.
```

The rational exponential cut weight `w=6/5` gives

```text
w lambda_7<7927875/8187904<1,
1/(1-w lambda_7)<8187904/260029<32.
```

This is an abstract contraction for a raw field-7 loss followed by six valid
core blocks.  It does not assert that the physical field-7 range lies in the
24-core strong space.

## 5. Physical installation still missing

The two scalar products become native operator statements only after all of
the following interfaces are supplied:

```text
OCCURRENCE -> FROZEN 24-CORE TRANSPORTED INCIDENCE: NOT CERTIFIED
ONE COMMON POST-CUT/CORE STRONG NORM:               NOT CERTIFIED
NO HIDDEN RECUT DURING 2018 OR 12108 STEPS:         NOT CERTIFIED
STRONG COMPLEMENT AND CEMETERY PAYLOAD:             NOT CERTIFIED
WEIGHTED TRANSPORTED-INJECTION SUMMABILITY:         NOT CERTIFIED
COMMON DQ / MT_DQ / FACE TYPING:                    NOT CERTIFIED
COMPLETE 18-FIELD OPERATOR BLOCKS:                  NOT CERTIFIED
STABLE QUOTIENT / PPE / THREE-NORM KAC CLOSURE:     NOT CERTIFIED
GATE 4:                                             NOT CERTIFIED
GATE 5:                                             NOT CERTIFIED
```

The shell route additionally requires the cut to remain the same physical
interval in both orientation views.  The field-7 route additionally requires
every admitted key to be materialized as a physical homogeneous subbranch.

## 6. Technology check

Demers--Liverani `arXiv:2606.10155`, section 5.6.1, explicitly distinguishes
large holes from sparse holes and notes that sufficient intervening mixing
can recover cone contraction for sparse holes.  That supports the dwell-block
strategy, but it does not furnish the CM2 occurrence-to-core incidence or
common Banach-space interfaces.  No literature promotion is made.

## 7. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate45_sparse_cut_dwell_contraction_frontier_cert.py \
  deliverables/cm2_gate45_sparse_cut_dwell_contraction_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate45_sparse_cut_dwell_contraction_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate45_sparse_cut_dwell_contraction_frontier_verifier.py \
  --self-test

# Expected exit 2: physical installation and Gates 4/5 remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate45_sparse_cut_dwell_contraction_frontier_verifier.py
```
