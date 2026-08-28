# CM2 Gates 3/4 — Round-43 `N_open` effectivity frontier

Date: 2026-07-19  
Verdict: **the exact reason `N_open` is still nonnumerical is now frozen.  The
published large-hole/projective chain contains theorem constants whose
dependence is explicitly left non-effective; the numerical C24 Growth and
standard-family recovery clocks do not replace the missing hit minorization.**

## 1. Published large-hole chain

For C24 the already certified inputs are

```text
P0=49,
Ct=1493,
mu(C24)<1/2500,
epsilon_hit=21/111718750.
```

Lemmas 8.6 and 8.8 and Proposition 8.7 of `arXiv:2104.06947v3`
enlarge the cone by

```text
c'=c P0,
A'=6A/(1-mu(H)),
L'=9L/(1-mu(H)).
```

They then use

```text
n_star=max(NF',nbar_delta),
NF'=Cstar' |log delta|+kstar n*,
N_return=J n_star.
```

The paper explicitly says that the worse dependence of `n_star` on `delta`
is not made explicit.  The current physical instance has no numerical values
for `C_delta,C_H,vartheta_H,nbar_delta,Cstar',kstar,n*,chi,J`, or the enlarged
cone's projective diameter and mixing constants.

## 2. Exact conditional schedule

If those constants were materialized, a safe mixing time is

```text
m_mix=max(0,1+ceil(log(2724 C_mix/epsilon_hit)/(-log vartheta_mix)))
```

and the frozen sparse-hit proof can take

```text
N_open=max(N_return,nbar_delta+m_mix).
```

This is an exact conditional formula, not a numerical value.  It explains
why the explicit hit gap does not yet yield a collision-time rate.

## 3. Why the local numerical clocks do not close it

The native artifacts now provide

```text
C24 killed Growth:        n_*=9148, gamma<1/2,
standard-family recovery: R(D)<=301500+1005D.
```

Both control boundary complexity/properness.  Neither gives a lower bound on
the mass of a recovered family inside the fixed 24-core target.  Therefore
using either clock as `N_open` would confuse Growth with mixing/minorization.

The shortest native replacement theorem is now explicit:

```text
find numerical H_SF>=1 and epsilon_SF>0 such that
mass(1_C24 T_s^H_SF G)>=epsilon_SF mass(G)
for every canonical proper family G, uniformly for |s|<=1/400,
and return the survivor to the same proper class numerically.
```

Together with the 9,148-step killed Growth block, this would bypass the
non-effective projective route.

## 4. Strict boundary

```text
N_open effectivity gap:                 CERTIFIED
conditional N_open formula:             CERTIFIED
numeric N_open:                         NOT CERTIFIED
native proper-family C24 minorization:  NOT CERTIFIED
collision-time q / C_fw / C_rev:        NOT CERTIFIED
strong cemetery:                        NOT CERTIFIED
Gate 3 / Gate 4:                        NOT CERTIFIED
CM2:                                    NO-GO_FOR_CLAIM
```

The result is an effectivity audit, not an impossibility theorem for future
independent proofs.

## 5. Validation

The certificate replays pinned dependencies and exact rational inputs.  Its
fail-closed verifier rejects `22/22` hostile mutations; default execution
returns exit code `2` while replay/integrity modes pass.
