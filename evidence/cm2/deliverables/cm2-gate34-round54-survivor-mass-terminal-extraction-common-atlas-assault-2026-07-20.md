# CM2 Round 54 Gate-4 survivor-mass / terminal-extraction / common-atlas assault

Date: 2026-07-20  
Strict status: **the Round-28 survivor tail is now joined to the unique
Round-36/37 killed-family mass.  A two-orientation coarse terminal-`Z`
inequality is explicit, but the same-ID natural-cell/image-recut refinement
to `J_pair` and the all-insertion-time C24-complement face forcing are both
open.  Physical `J_pair`, `I_D`, `q`, strong cemetery, Gate 4, and CM2 remain
not certified.**

## 1. Scope and frozen inputs

This append-only leaf reads eleven hash-pinned manifests.  In particular it
uses the exact Round-27 `R_n/Q_n` partition, the Round-28 normalized survivor
tail, the Round-36 aggregate recurrence together with its Round-37 typing
correction, the terminal core multiplier, the arbitrary-`R_n` common carrier,
and the Round-50--53 once-charged two-view/common-survivor stack.  No old
artifact is edited.

The new executable artifacts are:

- `cm2_gate34_round54_survivor_mass_terminal_extraction_common_atlas_cert.py`;
- `cm2_gate34_round54_survivor_mass_terminal_extraction_common_atlas_verifier.py`;
- `cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json`;
- `cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.sha256`.

## 2. The unique mass typing is the killed survivor family

Round 27 fixes, modulo the collision-null boundary,

```text
Q_0=C_s,
Q_(n-1)=R_n disjoint_union Q_n,
S_n=mu_s(Q_n)/mu_s(C_s).
```

Round 37 corrects the Round-36 base recurrence to the repeated
`C24`-complement restriction.  Its state is therefore uniquely instantiated
as

\[
 \mathcal F_n=(T_s^n)_\#(\mu_s|Q_n).
\]

Write `G_(n+1)=T_s#F_n` before killing.  The exact level split is

```text
E_(n+1)=1_C_s G_(n+1),       IDs R_(n+1),
F_(n+1)=1_(C_s^c)G_(n+1),   IDs Q_(n+1).
```

The half-open Round-27 prefix owner is preserved: a surviving prefix gains
one avoidance symbol, while a terminal child gains the corresponding
`R_(n+1)` path key.  Area preservation gives the exact unnormalised mass

\[
 \boxed{m_n=\|\mathcal F_n\|
       =\mu_s(Q_n)=\mu_s(C_s)S_n.}
\]

This resolves the former same-ID, layer-index, and normalization ambiguity.

The alternative `m_n=mu_s(R_n)` is not a second valid interpretation of this
recurrence.  Although `sum_n mu_s(R_n)=mu_s(C_s)`, one-step killed evolution
does not send the `R_n` return-level law to `R_(n+1)`.  Substituting return
mass into the survivor recurrence would mix two different state machines.

## 3. Exact summation of the collision mass

Put

```text
A=550000/147,
r=111718729/111718750,
1-r=21/111718750.
```

Round 28 gives, strictly,

\[
 m_n<\mu_s(C_s)A r^{\lfloor n/N_{\rm open}\rfloor}.
\]

Every block exponent occurs exactly `N_open` times, so

\[
 \sum_{n\ge0}m_n
 <\mu_s(C_s)\frac{A N_{\rm open}}{1-r}
 =\mu_s(C_s)\frac{61445312500000}{3087}N_{\rm open}.
\]

Using the frozen strict upper
`mu_s(C_s)<29021/75000000` also gives

\[
 \sum_{n\ge0}m_n
 <\frac{142656353125}{18522}N_{\rm open}<\infty.
\]

The sum is rigorously finite but not a numerical constant because
`N_open` is still theorem-supplied rather than materialized.

Thus the first of the three Round-53 aggregate joins is now genuinely
closed:

```text
Round28 Q_n -> Round36/37 m_n same-ID normalization: CERTIFIED
physical survivor-mass l1:                           CERTIFIED
```

## 4. Why this does not sum the face forcing

The remaining base recurrence in each orientation is

\[
 Z_{\sigma,n+1}
 \le aZ_{\sigma,n}+b m_n+\Phi_{\sigma,n},
 \qquad
 a=\frac{360134800}{360493663},\quad b=2\cdot10^{90},
\]

where `Phi_(sigma,n)` is the new boundary charge created while retaining the
`C24` complement.

An exact separator shows that the newly closed mass sum cannot provide this
charge.  Take a constant-density interval family

```text
W_n=(0,r^n).
```

At step `n`, remove `[r^(n+1),r^n)` and retain `W_(n+1)`.  Then

```text
m_n=r^n,       sum_n m_n=1/(1-r)<infinity,
Phi_n=1,       sum_n Phi_n=infinity.
```

Every fixed-level forcing is finite, but its all-time sum diverges.  This is
a logical standard-family restriction model, not a claim about the physical
billiard.  It proves that a trace-survivor contraction, hereditary open
Growth theorem, or an equivalent physical face cancellation is still an
independent input.

## 5. Coarse two-orientation terminal `Z` and the refinement gap

The frozen terminal core multiplier does give a useful but coarser typed
inequality.  The two orientation cores must be kept distinct:

```text
C_fw=C_s,
C_rev=I(C_s).
```

No literal equality `I(C_s)=C_s` is asserted.  The billiard involution `I`
preserves collision-SRB measure and carrier arclength.  Conjugating the
`C_s` characteristic operator by `I` therefore gives the same
`2000/1999` source norm on `I(C_s)`.

With the Round-35 identical physical return ID, define

```text
G_(fw,n+1)=T_s#F_(fw,n),   E_(fw,n+1)=1_C_s G_(fw,n+1),
G_(rev,n+1)=T_s#F_(rev,n), E_(rev,n+1)=1_(I(C_s))G_(rev,n+1).
```

The indexing is deliberate: `n=0` extracts the forward `R_1` layer and its
reverse `I(R_1)` layer.  The complement forcing `Phi_(sigma,n)` constructs
the next survivor and does **not** include that terminal layer.  Hence

\[
 Z(E_{\sigma,n+1})
 \le \frac{2000}{1999}\bigl(aZ_{\sigma,n}+bm_n\bigr).
\]

Let

```text
M=sum_n m_n,
Phi_pair=sum_n(Phi_fw,n+Phi_rev,n),
Z_pair,0=Z_fw,0+Z_rev,0.
```

For the coarse terminal family this yields

\[
 \boxed{
 Z_{\rm term,coarse,pair}
 \le\frac{2000/1999}{1-a}
       \left(aZ_{\rm pair,0}+2bM+a\Phi_{\rm pair}\right).
 }
\]

The common resolvent multiplier is

```text
(2000/1999)/(1-a)=720987326000/717367137=360674000/358863.
```

This is not yet the Round-53 `J_pair`.  That target is computed after the
natural-short-cell and image-recut refinement on exact same IDs.  A sharp
separator is a unit terminal interval:

```text
coarse mass=length=1, hence coarse Z=1;
split into N equal cells: each contributes (1/N)/(1/N)=1;
refined cell Z=N.
```

Thus no uniform coarse-`Z` domination of the refined `J_pair` follows from
the present fields.  Two independent interfaces remain:

```text
coarse terminal-Z inequality:                         CERTIFIED
terminal cell-refinement -> J_pair same-ID Z join:   NOT CERTIFIED
all-time complement forcing Phi_pair in l1:          NOT CERTIFIED
```

Even finite `Phi_pair` would currently close only the coarse terminal sum;
it would not close `J_pair` until the cell-refinement join is installed.

## 6. Physical Borel countable common-refinement atlas

There is also a new geometric existence layer on the Round-52 common
terminal survivor.  Work on the same raw once-charged parent restriction and
stratify by:

- integer stopped times;
- finite regular branch paths and incidence ranks;
- the existing half-open endpoint owners;
- a countable compact exhaustion staying a positive distance from all
  singular and predicate boundaries.

No compact containment is asserted for the original whole-family section.
On each compact regular substratum, both finite terminal schedules are finite
intersections of analytic inequalities.  A nonzero analytic boundary
function has finitely many zeros there; an identically signed row adds no
cut, while an identically zero strict row is empty or belongs to the removed
boundary stratum.  Hence each compact regular substratum has finitely many
components, but one original whole-family record may meet countably many
substrata.

Label a component by the least rational basis element it contains.  The
open-section component relation is Borel, and the countable union remains
standard-Borel.  The stopped view maps are finite analytic diffeomorphisms on
each compact regular substratum, so every positive component has positive
Borel lengths in both orientations.  The components partition the common raw
mass once, not once per orientation.

This establishes the atlas, not its boundary sum.  A separator within one
original record takes one component on each compact substratum and sets

```text
p_k=ell_fw,k=ell_rev,k=2^-k.
```

Then `sum_k p_k=1`, and every substratum has just one finite component, but
each orientation contributes `p_k/ell_k=1`.  Therefore the paired
`J_cap=sum_k 2` diverges.  Thus neither `J_cap(y)<infinity` nor `D_cap(y)` nor
recordwise properisation follows from the countable atlas.

The exact frontier is:

```text
physical Borel countable common atlas:          CERTIFIED
finite components per compact regular stratum: CERTIFIED
recordwise J_cap(y)<infinity:                   NOT CERTIFIED
recordwise D_cap / two-view properisation:      NOT CERTIFIED
integral J_cap(y) d lambda<infinity:            NOT CERTIFIED
integrated exp(D_cap/6) clock moment:           NOT CERTIFIED
```

The Round-52 interval-translation separator still applies: both marginal
views can be proper and the common mass can be `499/500`, while the common
inverse-length sum is infinite.  Large common mass and proper marginal views
do not repair either the within-record countable-stratum gap or the outer
integrability gap.

## 7. Strict typing boundary

Certified by this leaf:

1. the exact killed-survivor state and `m_n=mu_s(C_s)S_n`;
2. the strict finite collision-mass sum with coefficient
   `61445312500000/3087`;
3. the exact nonimplication from mass summability to face summability;
4. the two-orientation coarse terminal-`Z` inequality, including distinct
   `C_s/I(C_s)` cores, the `R_1/I(R_1)` off-by-one convention, and the
   `2000/1999` multiplier;
5. the exact coarse-`Z` to cell-refinement-`Z` nonimplication;
6. a physical Borel countable common-refinement atlas, with finite components
   only on each compact regular substratum;
7. the exact per-substratum-finite to recordwise-`J_cap` nonimplication.

Still not certified:

1. `sum_n Phi_(fw,n)+Phi_(rev,n)<infinity`;
2. the same-ID natural-cell/image-recut refinement from coarse terminal `Z`
   to `J_pair`;
3. the actual physical global `J_pair` and `I_D`;
4. recordwise and global `J_cap`, `D_cap`, and the integrated extra-clock moment;
5. one physical proper same-ID first-return kernel after the stopped
   two-view transports;
6. intermediate avoidance for the postproperisation terminal schedule;
7. later/repeated recovery-clock moments;
8. physical `C_fw,C_rev,q` and strong singular/current cemetery;
9. Gate 4 and CM2.

The countable atlas is not relabelled as a proper reference carrier, and the
ambient clock envelope is not relabelled as physical `q`.

## 8. Verification

The verifier independently reconstructs the strict block tail, both rational
sum coefficients, the survivor/return state rejection, the terminal
resolvent and its three coefficients, distinct forward/reverse core typing,
the face-forcing and cell-refinement separators, the countable-stratum atlas
separator, dependency hashes, and all nonpromotion fields.  It also checks
AST literal keys, strict JSON, replay determinism, and default fail-close.

Final targets:

```text
syntax:                          2/2 PASS
dependency hashes:              11/11 PASS
independent arithmetic/replay:  PASS
hostile mutations:              197/197 REJECTED
deterministic re-emission:       PASS
default cert/verifier:           both exit exactly 2
strict Gate 4 / CM2:             NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

## 9. Next shortest route

1. Put the terminal natural-short-cell/image-recut refinement on the exact
   coarse terminal IDs and prove a refinement-`Z` inequality.
2. Prove a physical all-time C24-complement trace contraction/cancellation
   for `Phi_pair`.  Together with item 1 and the now-closed mass join, this
   closes `J_pair` and then `I_D`.
3. Prove a within-record summable bound across the countable common-atlas
   strata, followed by an outer integrable `J_cap` majorant.  Only then apply
   the fractional-Z properisation-clock theorem.
4. On that same once-charged restriction, prove a physical same-class
   first-return/intermediate-avoidance theorem and every later recovery-clock
   moment before defining `q`.
5. Close the strong trace/current cemetery; only then assemble the remaining
   Gate-5 fields and induced coefficient.
