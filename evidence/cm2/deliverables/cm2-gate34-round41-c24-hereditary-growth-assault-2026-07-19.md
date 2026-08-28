# CM2 Gate 3/4 Round-41 C24 hereditary Growth assault

Date: 2026-07-19  
Status: **the C24 hereditary unnormalised standard-family Growth bridge is
certified qualitatively and uniformly; numerical block constants and final
Gate-4 charges remain open**

## Result

Round 40 left C24 Growth open because it typed `hat F` as a conditional
survivor operator and treated the 2026 boundary-strip geometry as essential.
Both points are now corrected.

In Demers' general-hole formulation, an admissible hole needs only:

```text
(H1) a short stable curve is cut into at most B0 pieces by boundary(H),
(H2) m_W(N_epsilon(boundary(H))) <= C0*epsilon^(1/2).
```

The frozen C24 certificate already proves the stronger facts

```text
B0=49,
m_W(N_epsilon(boundary(C24))) <=1493*epsilon,
```

uniformly for every fixed `|s|<=1/400`.  Since `epsilon<=sqrt(epsilon)` on
`(0,1]`, C24 satisfies Demers' `H1/H2` class with `C0=1493`.  The identical
positive-slope calculation supplies the unstable version used by the
standard-family proof.

## Correct operator

Canestrari's `hat F_t` is the closed billiard map with the hole boundary
added as an artificial singularity set.  It retains every descendant and all
mass.  The conditional survivor operator is `L_t`, not `hat F_t`.

Thus the Growth proof first applies to the all-mass extra-cut family.  The
unnormalised killed family is obtained by deleting components lying in C24.
For

```text
Z(G)=sum_j p_j/|W_j|,
```

deleting positive components can only decrease both `mass` and `Z`.
No survival normalization is needed.

## Expansion versus fragmentation

The closed-map one-step expansion certificate gives

```text
theta = 900337/901685 < 1.
```

Demers' artificial-cut argument therefore gives the short-curve kernel

```text
sum_j |J F^(-n)|_* <= (1+48n)*theta^n.
```

The exact first integer for which this bare kernel is below `1/2` is

```text
n=9148,
(1+48*9148)*theta^9148<1/2,
(1+48*9147)*theta^9147>=1/2.
```

This is not promoted to the final `n_*`: density ratio, cone-metric and
chopping prefactors are finite and uniform but not yet numerical.

For any prescribed `gamma in (0,1)`, in particular `gamma=1/2`, there are
uniform finite `n_*,Z0,Z1` such that

```text
Z(hat F_C24^((p+1)n_*)G)
 <= gamma Z(hat F_C24^(p n_*)G)+Z0 mass(G).
```

Positive-subfamily monotonicity gives the same recurrence for the
unnormalised every-collision killed family.  This closes the hereditary C24
Growth interface qualitatively.

## Aggregate Z resolvent

The every-collision survivor at scheduled times is a subset of the Round-38
scheduled survivor, whose mass factor is

```text
r=111718729/111718750<1.
```

On the common block `L=N_open*n_*`, write

```text
z_(p+1)<=g z_p+C m_p,
g=gamma^N_open<1,
m_p<=rho^p m_base,
rho=r^n_*<1.
```

Then

```text
z_p<=g^p z_0+C m_base sum_(j=0)^(p-1)g^(p-1-j)rho^j.
```

Hence some `w_Z>1` satisfies

```text
sum_p w_Z^p z_p<infinity.
```

This is a qualitative aggregate canonical-`Z` tail for controlled finite-`Z`
physical initial families dominated as positive measures by the base-cone
source.  It uses neither a cellwise `2^D` moment nor a projective-norm-to-`Z`
trace comparison.

## Strict boundary

The following are not numerical or complete:

```text
n_*, Z0, Z1, w_Z and the resolvent constant,
C_fw, C_rev and final same-ID q,
strong cemetery,
Gate 3, Gate 4 and unconditional CM2.
```

Gate 4 therefore remains open, but its hereditary C24 Growth and qualitative
aggregate-`Z` base obstruction are removed.

## Sources checked

- Mark F. Demers, *Dispersing Billiards with Small Holes* (2014),
  DOI `10.1007/978-1-4939-0419-8_8`, especially `H1/H2` and the artificial-cut
  complexity lemma.
- Canestrari, arXiv `2604.19671v2`, Lemmas 6.13--6.14 and the distinction
  between `hat F_t` and `L_t`.

## Validation

The certificate replays all frozen dependency hashes, exact rational
threshold arithmetic, strict JSON and the nonpromotion boundary.  Its
verifier rejects `27/27` hostile mutations and exits fail-closed by default.

Artifacts:

- `deliverables/cm2_gate34_round41_c24_hereditary_growth_cert.py`;
- `deliverables/cm2_gate34_round41_c24_hereditary_growth_verifier.py`;
- `deliverables/cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json`.
