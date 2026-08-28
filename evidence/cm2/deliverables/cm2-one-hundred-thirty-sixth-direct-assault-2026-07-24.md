# CM2 one hundred thirty-sixth direct assault

Date: 2026-07-24

Strict verdict: **one actual positive-area local rank-1056 return cylinder is
now frozen with a complete first-return replay. This removes the prior
point-only/nonreturn diagnostic obstruction, but it does not yet supply the
canonical component rank or the owner/`q_j` chain. Gate5 and CM2 do not
move.**

## Main advance

Round116 supplied a corrected transverse HIT collar, but its three official
keys were collision prefixes rather than a return path. Round136 chooses a
rational box strictly inside the selected corrected strip:

```text
source half-width in t and p: 2^-3815
exact source area:            2^-7628
fixed s:                      0
```

The box is located by an exact 1500-step rational bisection at the
third-collision cosine scale `2^-64`. After the box is frozen, the
construction target is discarded.

Every later collision is obtained from a fresh complete retained-candidate
search over the whole box.

## Actual first-return path

The complete path census is:

```text
collision rows:                    1056
strict nonreturns before return:   1055
strict terminal returns:              1
official-word occurrences:         1056
unique official-word IDs:           125
```

Collision 1056 lands strictly in

```text
core:d6e30c5e3160559018e3ed757ec6d3fc12eb97cbd9d9673c7907621b2fe97ee8.
```

Every official word is rebuilt after exact lattice-translation
normalization. Every collision has a whole-box C24 classification,
homogeneity label, incidence rank, chart decision, owner decision, and strict
margin closure.

The exceptional third collision lies in `H4294967295` and has target
incidence rank 65. All other homogeneity labels are central. The inherited
source endpoint makes collision 4 the second rank-65 incidence row.

## What remains blocked

The object is frozen as

```text
round136-local-return-cylinder:
51fca5b65a5bfef1067ea3bf60e464db5fe9d4fd192db0696160184c2781026e
```

because the old Round27/35 contracts do not provide an executable global
least-dyadic-basis component enumeration. A positive local box proves a
nonempty component witness, but it does not identify the least global basis
rank or exclude every earlier basis box.

Accordingly Round136 does not mint:

```text
c24-component
Round35 rn-restriction
Round50 owner key
Round54 t54 token
Round67 q_j output
```

The unique typed Round132 occurrence candidate is retained as a crosswalk
target, but there is still no proof that its D=0 face is in the closure of
this R1056 cylinder and no complete same-event primitive fibre.

## Independent verification

The independent verifier never imports or executes the producer. It
reconstructs the complete 1056-row certificate from byte-pinned upstreams.
The 8192-bit result matches the frozen certificate exactly; a second
12288-bit replay matches the complete discrete collision and strict-margin
semantic projections.

```text
formal verification:                   PASS
re-signed semantic mutations:         70/70 rejected
strict-JSON attacks:                  19/19 rejected
path-safety self-tests:               13/13 rejected
dual hash-seed artifacts:             byte-identical
process-level hostile I/O cases:      12/12 fail-closed
```

## Frozen global state

```text
positive-width local R1056 cylinder:      1
canonical global c24-components:          0
materialized owner records:               0
materialized q_j outputs:                 0
global complete 18-field blocks:          0
Gate5 global maturity:                10/18
Gate5:                         NOT_CERTIFIED
CM2:                        NO-GO_FOR_CLAIM
```

The next honest step is to freeze an executable canonical component
enumeration and prove the selected D=0 occurrence face belongs to the
appropriate return-component closure. Only then can the Round35 restriction,
primitive-free same-event fibre, owner key, and `q_j` projection be
materialized.
