# CM2 Gate 3: independent resolution of the 320 owner/Voronoi endpoint descriptors

Date: 2026-07-15  
Scope: rational two-disk torus pilot, standard solid-boundary section
`N=G disjoint-union W`, `|s|<=1/400`, certified physical horizon
`tau_max<3`.

## Decision

**All 320 descriptors in the original owner/Voronoi full-window unresolved
set are physically empty as endpoint descriptors.  The strict residual set
is zero.**

The exact final accounting is

| resolver class | count |
|---|---:|
| empty | **320** |
| physical boundary | 0 |
| physical duplicate | 0 |
| physical earlier endpoint | 0 |
| physical later endpoint | 0 |
| physical joint vertex | 0 |
| unresolved | **0** |

The labels `earlier=220` and `later=100` survive only as exact common-line
contact-order metadata.  They are not physical endpoint counts.

Evidence:

- `deliverables/cm2_gate3_endpoint_descriptor_resolver_cert.py`;
- `deliverables/cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.json`;
- `deliverables/cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.sha256`.

The corrected owner/Voronoi artifacts are pinned read-only.  No v51/v52
file, shared log, or other agent's source was edited.

## 1. The missing forward-time condition

For a signed common tangent to target `T` and partner `B`, let `ell_T` and
`ell_B` be the oriented contact times from the outgoing source point.  On
the earlier branch,

\[
  \ell_B<\ell_T.
\]

That inequality does **not** say that `B` is a forward collision.  A physical
earlier visibility boundary additionally requires

\[
  \boxed{0<\ell_B<\ell_T.}
  \tag{1.1}
\]

The pre-correction classifier's comment required that “B is itself first,”
but its earlier branch called the clearance test without first checking
`ell_B>0`.  Consequently a backward tangency could be labelled
`physical_earlier_occlusion_boundary`.

The independent resolver regenerates the exact original 320-row set, with
digest

```
c04fc55676bcb0341c24f8ae5f50116913bb9b70b18ca901873c7e1ff15238a2
```

and inserts (1.1) before any earlier-boundary verdict.  The owner/Voronoi
certificate and manifest now explicitly retract the former 16-vertex claim
and preserve this digest as provenance.

## 2. Exact common-tangent geometry

Put

\[
 d=b-a,
 \qquad h=\epsilon_B R_B-\epsilon_T R_T,
 \qquad D=|d|^2,
 \qquad \rho=\sqrt{D-h^2}.
\]

For branch `lambda in {-1,+1}`, the oriented line normal and tangent are

\[
 n=\frac{h d+\lambda\rho d^\perp}{D},
 \qquad u=(n_y,-n_x),
 \qquad u\cdot d=\lambda\rho.
\]

The source point is the outgoing intersection of

\[
 n\cdot(q-a)=-\epsilon_T R_T
\]

with the source circle.  Every square root is evaluated by 256-bit Arb on a
closed rational `s` box.  The W/W/W common-translation families are reduced
exactly before interval evaluation: source, `T`, and `B` share the same
horizontal shift, so `u`, `n`, `ell_T`, `ell_B`, and the source normal are
independent of `s`; only `q_x` receives the common shift.  This removes the
dependency-only `source_grazing_transition` ambiguity without sampling.

## 3. Closed-cover classification of all 320 rows

Adaptive bisection produces 448 closed rational leaves, covers the complete
window with matching endpoints, and needs maximum depth only 3.  Every leaf
has one of five strict neighbourhood-stable empty witnesses:

| strict descriptor-level witness | descriptors |
|---|---:|
| a third target intersects strictly before `T` | 164 |
| target tangency is behind the source | 60 |
| earlier partner tangency is behind the source | 52 |
| common line has no outgoing source intersection | 32 |
| later partner is not the next target | 12 |
| **total** | **320** |

The leaf counts are respectively `188, 64, 52, 128, 16`; a descriptor can
need several boxes, but every box belonging to one descriptor has the same
physical empty type.

The six original unresolved classes resolve as follows:

| original class | strict resolution |
|---|---|
| `earlier_tangent_visibility` (16) | 16 strict third blockers |
| `later_miss_order` (4) | 4 later partners not next |
| `source_grazing_transition` (176) | 32 no source intersections; 60 target-behind; 60 third blockers; 20 earlier-partner-behind; 4 later-not-next |
| `target_after_earlier_tangent` (40) | 32 earlier-partner-behind; 8 third blockers |
| `target_time_endpoint` (76) | 76 third blockers |
| `target_visibility` (8) | 4 third blockers; 4 later-not-next |

The strict blocker criterion uses the certified disjoint-disk projection
order: if `0<ell_C<ell_T` and `Delta_C>0`, the positive incoming root of `C`
is before the tangent point of `T`.  Likewise, on a later branch an
intervening `C` with `ell_T<ell_C<ell_B` and `Delta_C>0` proves that `B`
cannot be the miss owner.

## 4. The 20 former transition collars

The resolver does not merely discard the old collars.  It gives each an
exact algebraic root equation, a rational isolating `s` interval, a rigorous
true-cell `(t,p)` box, and an exact Sturm root count of one.

### 4.1 Sixteen third-target roots

For a third target `C`, set

\[
 e=a-c,
 \quad
 g=\epsilon_T R_T-\epsilon_C R_C.
\]

The common line is also tangent to `C` only if

\[
 F(s)=
 (h e_y-g d_y)^2+(g d_x-h e_x)^2-\det(d,e)^2=0.
 \tag{4.1}
\]

All coefficients are exact rationals and `deg F<=2`.  Exact Sturm sequences
prove one labelled-branch root in each of the 16 rational boxes, while the
fixed signed gap changes sign across the box.

However, all 16 boxes satisfy the stronger full-window witness

\[
 \ell_B<0.
\]

Thus (4.1) locates a real triple common-line tangency but **not** a forward
physical joint vertex.  The former count 16 is retracted; the corrected
physical joint count is zero.

### 4.2 Four `tau=3` roots

For flight `L=3`, substituting

\[
 q=a-Lu-\epsilon_T R_T n
\]

into the source-circle equation gives `A(s)+B(s)rho(s)=0`.  The certificate
forms the exact rational elimination polynomial

\[
 P_3(s)=A(s)^2-B(s)^2\{D(s)-h^2\}
 \tag{4.2}
\]

and proves by Sturm that every isolating box contains one root.  Arb signs
on both endpoints select the intended radical branch, so no conjugate root
is accepted.  Each complete parameter window also has a fixed strict third
target before `T`.  Hence both sides and the equality `ell_T=3` are
nonphysical; the latter is additionally excluded by the strict certified
horizon `tau_max<3`.

The ordered digest of all 20 `(s,t,p)` root rows is

```
ca6e3ae0d5f63606a482fc2aa91059fa5aa128644dc14650209efb8e4f2b67e0
```

## 5. True dominant-cell audit

For source normal `nu=(nu_x,nu_y)`, the certificate selects the unique
strict dominant chart by

\[
\begin{aligned}
 E &: \nu_x>|\nu_y|, & W &: -\nu_x>|\nu_y|,\\
 N &: \nu_y>|\nu_x|, & S &: -\nu_y>|\nu_x|.
\end{aligned}
\]

It then records

\[
 t=\nu_y\quad(E,W),
 \qquad t=\nu_x\quad(N,S),
 \qquad p=-u_x\nu_y+u_y\nu_x.
\]

There are 1,480 regular strict-cell phase boxes and 128 no-source leaves.
Eight descriptors cross a dominant-cell seam.  At a seam

\[
 \nu=(\sigma_x,\sigma_y)/\sqrt2,
 \qquad \sigma_x,\sigma_y\in\{-1,1\}.
\]

Substitution into the common-line equations gives
`A(s)+sqrt(2)B(s)=0`; the resolver uses the exact rational elimination
`A^2-2B^2` and a Sturm count of one in each of the eight seam boxes.  These
are chart-coordinate duplicates only.  Every seam box retains an independent
strict empty witness, so the physical duplicate count remains zero.

The regular and seam registries have digests

```
regular: 6f57b2a8d0afbd695c3f919ffa09707a2dd761cd8e141318cf20bde084d60af7
seams:   8a767f36b7f2d745640007674745b2093bc7039b93daef590a48a4f3dbfbb663
```

## 6. Fail-closed boundary

This certificate closes precisely the original 320-row descriptor set.  It
does not independently re-audit the other 81,728 old first-pass rows and
does not construct connected immutable event rows.  Therefore global `DQ`
and scalar-current matching remain `NOT_CERTIFIED`.

Reproduction:

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_endpoint_descriptor_resolver_cert.py
sha256sum -c \
  deliverables/cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.sha256
```

Expected terminal lines:

```text
GATE3_320_ENDPOINT_DESCRIPTORS: CERTIFIED_PHYSICALLY_EMPTY
GATE3_320_ENDPOINT_UNRESOLVED: 0
GATE3_CONNECTED_IMMUTABLE_EVENT_ROWS: NOT_CERTIFIED
```
