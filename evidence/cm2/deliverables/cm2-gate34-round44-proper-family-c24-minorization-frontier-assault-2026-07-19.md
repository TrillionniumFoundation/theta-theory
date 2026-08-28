# CM2 Gates 3/4 Round 44: proper-family C24 minorization frontier

Date: 2026-07-19  
Status: **the direct numerical interfaces are now exact, but no numerical
proper-family C24 minorization is yet certified**

## Verdict

The numerical `9148`-collision C24 killed-Growth block and the numerical
standard-family recovery clock do not contain a fixed-target incidence
statement.  The first genuinely missing Gate-4 object is

```text
mass(1_C24*T_s^H G) >= epsilon_SF*mass(G)
```

uniformly over the canonical proper-family class and `|s|<=1/400`, together
with a numerical return of the survivor to the same family class.

This round freezes the two shortest valid constructions of that object and
audits their missing constants.  It does not substitute a Growth clock for a
hit clock.

## 1. Growth/properness is target-blind

An exact abstract countermodel has two disjoint unit unstable curves, the
identity map, target equal to one curve, and a normalized family on the other.
It satisfies

```text
Z/m=1<Cp=4,
Z_n/m <= Cp/2*(1+(1/2)^n*Z_0/m)
```

for every `n`, yet its target hit mass is always zero.  This is not a
counterexample to the billiard.  It proves only the required logical point:
the scalar properness/Growth inequalities cannot supply fixed-C24
minorization without an additional target-sensitive mixing or magnet input.

Consequently neither

```text
n_*=9148
R(D)<=301500+1005D
```

is a numerical C24 hit block.

## 2. Smooth-bump route

The frozen global bump satisfies

```text
0<=g<=1_C24,
mu_s(g)>21/55859375,
||g||_C1<2724.
```

If one proves on canonical proper families

```text
|G(g o T_s^H)/mass(G)-mu_s(g)|
 <= C_SF theta_SF^H ||g||_C1,
```

then the exact safe threshold

```text
H_SF=max(0,1+ceil(log(2724*C_SF/epsilon_hit)
                  /(-log(theta_SF)))),
epsilon_hit=21/111718750
```

gives the desired C24 hit.  The missing values are numerical `C_SF`,
`theta_SF`, `H_SF`, and the same-family post-restriction return.

## 3. Coupling-magnet route

The official `arXiv:1210.0011v4` chain is now aligned exactly:

```text
Lemma 16:             proper-family recovery,
Proposition 31 / Corollary 32: magnet crossing and coupling fraction zeta,
Lemma 30:             gap recovery r,C,lambda,
Lemma 33 / Corollary 34:
                      uncoupled tail (1-zeta/2)^(n/Delta-1).
```

If a magnet `S_C24 subset C24` and numerical `zeta,Delta` were supplied, the
collision-time rate would be

```text
q_magnet=(1-zeta/2)^(1/Delta)<1.
```

The paper's constants are uniform but existential.  More importantly, the
24 frozen collision rectangles have not been certified as a stable-saturated
SYZ magnet: local stable-leaf density, gap distribution, holonomy, mixing
time and the coupling fraction remain absent.  Rectangle geometry alone is
not a magnet theorem.

## 4. Strict boundary

```text
C24 killed Growth block n_*=9148:             CERTIFIED
C24 interior bump and desired hit gap:        CERTIFIED
direct proper-family sufficient interfaces:  CERTIFIED
numerical proper-family C24 minorization:     NOT CERTIFIED
numerical C24 coupling magnet:                NOT CERTIFIED
collision-time C_fw/C_rev/q:                  NOT CERTIFIED
strong cemetery / Gate 4 / CM2:               NOT CERTIFIED / NO-GO
```

The shortest native route is now a direct interval/covering proof on every
long canonical parent-`W` family which supplies both a positive C24 hit
fraction and a numerical post-cut proper-family return.  This bypasses the
nine non-effective large-hole constants without importing Gate-2 holonomy.

## Evidence

- `deliverables/cm2_gate34_round44_proper_family_c24_minorization_frontier_cert.py`
- `deliverables/cm2_gate34_round44_proper_family_c24_minorization_frontier_verifier.py`
- `deliverables/cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json`

