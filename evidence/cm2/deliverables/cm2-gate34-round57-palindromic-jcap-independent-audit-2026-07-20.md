# CM2 Round 57 Gate 4 palindromic `J_cap` independent audit

Date: 2026-07-20  
Audit verdict: **PASS — no remaining blocker for the claims actually made by
the frozen Round-57 Gate-4 leaf.**

The audited main manifest is frozen at

```text
cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8.
```

This audit is append-only and did not modify the audited certificate,
verifier, manifest, report, SHA ledger or any older dependency.

## 1. Exact reversible direction and the operator off-by-one

The terminal operator `O_s` performs one collision transfer and then deletes
the terminal `C24` descendants.  Consequently the first closed leg must be
`T_s^(K-1)`, not `T_s^K`:

```text
x
 -> T_s^(K-1)x
 ->[O_s] T_s^K x
 ->[I] I T_s^K x
 ->[T_s^K] I x
 ->[I] x.
```

The fourth arrow is exactly

```text
T_s^K I T_s^K=I,
```

equivalently `I T_s^K I T_s^K=id`.  The directions therefore agree with the
pinned Round-56 reverse path identity; there is no hidden inverse-expansion
step and no extra collision.

## 2. Borel/tag audit of the variable clock

On each immutable physical cell tag `c`,

```text
K(c)=696 Dbar(c)+H_joint>=1.
```

`Dbar` is integer-valued Borel and `H_joint` is one fixed finite integer.
Thus the stopped construction is the countable disjoint union of finite-`K`
strata.  The numerical value of `K` is retained across both applications of
`I`; it is not recomputed after conditioning on a survivor subfamily.

The Round-52 SYZ mass estimate lives at the whole-parent index `y`, not the
proof-cell index `c`:

```text
h_cap(y)>249 p(y)/250.
```

No corresponding lower bound is used or claimed for an individual thin
cell or survivor interval.

## 3. Closed Growth and the single terminal cut

With

```text
a  =360134800/360493663<1,
Z1 =18367592526/360493663,
```

each closed leg satisfies

```text
Z(T^r G)<=a^r Z(G)+(C_p/2)mass(G).
```

The hash-pinned Round-42 report states that every unnormalised controlled
canonical finite-`Z` family satisfies

```text
Z(O_s G)<=Z1 Z(G).
```

This universal one-step estimate, rather than the Round-47 proper-source
`P*mass` envelope, is the decisive scope.  It remains available when the
second palindrome starts from an arbitrarily thin nonproper positive
subfamily of `I(B)`.

The exact affine ledger is therefore

```text
first closed leg:  Z <= Z_in+(C_p/2)m_in,
one O_s cut:       Z <= Z1 Z_in+(Z1 C_p/2)m_in,
second closed leg:Z <= Z1 Z_in+((Z1+1)C_p/2)m_in.
```

There is exactly one `Z1` multiplier in each palindrome.  The SYZ small-hit
estimate is used separately, only on the two original proper marginal laws
to obtain the parent-level mass union bound.  It is never rerun conditionally
on the second, nonproper input.

## 4. Paired first-return replay and once charge

The two tagged directions are

```text
A -> B=T_s^n(A) -> I(B),
I(B) -> I(A) -> A,
```

with

```text
T_s^k(I(B))=I(T_s^(n-k)(A)),  0<=k<=n.
```

The original `n` and no-earlier-`C_s` path tag are retained.  Singularity,
homogeneity, Growth and deterministic recut operations only refine analytic
branch intervals.  No transverse redisintegration, same-measure shortcut,
normalization or duplicate mass charge is used.  Both terminal predicates
are therefore represented on the identical raw restriction
`S_fw intersect S_rev`.

## 5. Components, global `J_cap` and the `D_cap` join

The proof atoms form a countable half-open Borel connected-interval kernel.
For the physical maximal components, atoms are merged only if their actual
union is connected and the shared endpoint is owned and belongs to the
regular common set.  Closure-touching across an omitted singular, null or
cemetery puncture is never merged, and components are never merged across
different parent indices `y`.

Each physical component is a positive coarsening of proof intervals, so its
`p/ell` value is their length-weighted average.  Hence

```text
J_cap,physical<=Z_cap,proof.
```

The two uniform palindrome bounds and the two pinned hereditary terminal
resolvents act on the globally finite Round-56 `J_pair` source.  This gives
the required integrated result, not merely recordwise finiteness:

```text
J_cap,total=integral J_cap(y) dlambda(y)<infinity.
```

The Round-53 conditional interface is consequently discharged.  It gives a
Borel `D_cap(y)`, synchronized `696 D_cap` properisation, a finite
`exp(D_cap/6)` moment and the stronger dyadic first-moment bound

```text
integral h(y)2^D_cap(y) dlambda(y)
 <= H+(4/C_p)J_cap,total
 < infinity.
```

## 6. Strict nonpromotion

The audit accepts exactly these upgrades:

```text
physical J_cap,total:                    CERTIFIED_FINITE
single D_cap exponential moment:         CERTIFIED_FINITE
full dyadic D_cap first moment:          CERTIFIED_FINITE
proper common terminal two-view carrier: CERTIFIED
```

It does not reinterpret the inherited original `A->B` first-return graph as
the still-missing proper common landing kernel.  The later synchronized
properisations are two orientation-specific stopped pushforwards, not one
physical first-hit map.  Accordingly:

```text
physical proper same-ID first return:    NOT_CERTIFIED
intermediate C24 avoidance:              NOT_CERTIFIED
later/repeated clock moments:            NOT_CERTIFIED
physical q in L^(6/5):                   NOT_CERTIFIED
strong singular/current cemetery:        NOT_CERTIFIED
Gate 4:                                  NOT_CERTIFIED
complete composite gates:                0/5
CM2:                                     NO-GO_FOR_CLAIM
```

## 7. Executable validation

The independent verifier performs deterministic regeneration, pinned-file
integrity checks, independent direction and affine-coefficient replay,
strict JSON parsing, byte-identical re-emission and hostile semantic
mutations.

Validation result:

```text
syntax:                         PASS
frozen dependency hashes:       11/11 PASS
independent semantic replay:    PASS
hostile mutations:              66/66 rejected
byte-identical re-emission:      PASS
default certificate exit:       2
default verifier exit:          2
```

Artifacts:

- `cm2_gate34_round57_palindromic_jcap_independent_audit_cert.py`
- `cm2_gate34_round57_palindromic_jcap_independent_audit_verifier.py`
- `cm2-gate34-round57-palindromic-jcap-independent-audit-manifest-2026-07-20.json`
- `cm2-gate34-round57-palindromic-jcap-independent-audit-2026-07-20.md`
- `cm2-gate34-round57-palindromic-jcap-independent-audit-manifest-2026-07-20.sha256`
