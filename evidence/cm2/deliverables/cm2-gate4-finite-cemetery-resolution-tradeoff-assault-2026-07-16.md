# CM2 Gate 4 finite-cemetery resolution–cost assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

The finite-native-antichain escape left open by the previous Gate 4 assault
is now closed under the existing leafwise inverse-mass cost interface.  A
finite cemetery can make the charge finite at each fixed resolution, but it
cannot make that charge uniform while the retained mass tends to one and the
physical resolution tends to zero.

```text
FINITE-CEMETERY RESOLUTION–COST THEOREM:                 CERTIFIED
UNIFORM NATIVE LEAFWISE RECOVERY MOMENT:                NOT CERTIFIED
UNNORMALISED/REWEIGHTED FAMILY ESCAPE:                  NOT REFUTED
COMPLETE NUMERIC C_fw/C_rev/q:                          NOT CERTIFIED
GATE 4:                                                 NOT CERTIFIED
```

The unconditional CM2 verdict therefore remains `NO-GO`.

## 1. Exact theorem on the physical mass carrier

Work on any normalized cumulative physical-mass coordinate `u in [0,1]`.
Let a deterministic finite stopped partition retain mass at least
`1-epsilon`, and suppose every retained atom has diameter at most `delta`.
Here diameter means **diameter in the `u` coordinate**.  By the defining
cumulative-mass change of variables,

```text
(u_(e,s))_*(m_(e,s)/m_(e,s)(row_s)) = Lebesgue on [0,1].
```

Thus for every positive-mass measurable atom `A_a`,
`p_a=Leb(A_a)<=diam_u(A_a)<=delta`.  This implication would not be valid for
an unrelated physical coordinate or measure, and no such extension is used.
If there are `N` retained atoms, then

```text
N delta >= sum_a p_a >= 1-epsilon,
N >= ceil((1-epsilon)/delta).                         (1.1)
```

The present stopped-parent interface normalizes every atom separately and
therefore charges at least `p_a^-1`.  Its unconditional charge obeys the exact
counting identity

```text
sum_a p_a p_a^-1 = N
  >= ceil((1-epsilon)/delta).                         (1.2)
```

Let `P_ret=sum_a p_a` be the actual retained mass.  Conditioning on survival
gives

```text
E[cost | retained] >= N/P_ret >= 1/delta,             (1.3)
```

where the second inequality is exactly `N delta>=P_ret`.  One must not
replace `P_ret` by its lower bound `1-epsilon` in the denominator; that would
reverse the relevant comparison.

Multiplication by a recovery factor `exp(gamma R_a)>=1` cannot decrease any
of these bounds.  Hence, whenever `epsilon_j->0` and `delta_j->0`, the charged
moment diverges.  This obstruction is independent of the missing numerical
Growth-Lemma constants.

## 2. Dyadic audit

For `delta=2^-K` and `epsilon<=2^-K`, (1.1)–(1.2) give

```text
N >= 2^K-1,
E[cost] >= 2^K-1.                                    (2.1)
```

The certificate replays this exact identity for every `1<=K<=20`.  Thus a
sequence of finite native antichains with vanishing cemetery and arbitrarily
fine resolution cannot supply the uniform inverse-mass recovery moment that
Gate 4 requests.

## 3. Precise scope boundary

This result closes only the proposed **finite cemetery + leafwise
normalization** escape.  It does not prove that every conceivable recovery
construction fails.  In particular, the following remain legitimate but
uncertified routes:

- keep all stopped pieces in one unnormalised or reweighted standard family
  and prove recovery without a separate `p_a^-1` charge;
- change the functional interface so that component count is not charged
  leaf by leaf;
- use an external randomized depth mark, as in the already certified product
  extension, if the final theorem is permitted to carry that extension.

None of these supplies the native physical quotient demanded by v52.  The
global weighted Growth estimate, distortion constants, native charged
recovery, and propagated numerical `C_fw,C_rev,q` therefore remain open.

## 4. Replay and fail-close contract

The certificate binds by SHA-256 to the frozen native stopping/repeated-cut
frontier certificate and manifest, imports and replays that certificate, and
then recomputes all twenty dyadic rows using exact rational arithmetic.  The
verifier checks provenance, the theorem strings, every arithmetic row, the
internal digests, fail-closed scope flags, and the Gate 4 verdict.

Normal live execution deliberately exits `2`.  Replay/integrity and the
mutation suite must exit `0`; any altered hash, theorem field, row, summary,
or verdict fails closed.
