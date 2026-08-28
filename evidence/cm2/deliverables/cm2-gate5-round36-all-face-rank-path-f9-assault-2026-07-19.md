# CM2 Gate 5 round 36: all-face finite-rank-path F9

Date: 2026-07-19  
Status: **parameterized F9 is now certified on all five physical face grammars; Gate 5 remains open**

## Verdict

The missing owner/singularity and moving-occurrence face geometries have now
been joined to the arbitrary finite rank-path recurrence.  Every regular
face instance in the five frozen physical grammars therefore has a finite
parameterized F9 `C2` value.  This raises global Gate-5 field maturity from
`6/18` to `7/18`, while complete operator blocks remain zero.

```text
source core clipping F9:                         CERTIFIED
intermediate core-preimage F9:                   CERTIFIED
terminal core-preimage F9:                       CERTIFIED
owner/singularity F9:                            CERTIFIED
moving-occurrence F9:                            CERTIFIED
global physical Lp sum of F9 costs:              NOT CERTIFIED
complete F10:                                    NOT CERTIFIED
Gate 5:                                          NOT CERTIFIED
CM2:                                             NO-GO FOR CLAIM
```

## Base physical geometry

For two distinct disk boundaries the global boundary gap is

```text
ell > 36337/800000.
```

On a circle-tangency face, written as `G(r,phi)=phi-h(r)`, the circular
caustic identities give

```text
|h'| < 29,                 |h''| < 4949,
1 <= ||dG||_1 < 30.
```

The 64 selected moving-occurrence seeds retain the sharper bounds

```text
flight > 1/10,             |h'| < 17,
|h''| < 623,               ||dG||_1 < 18.
```

Forward integer-corner rays are treated as point-caustic graphs.  The same
gray-center ray is excluded because its outgoing cosine is negative.  The
remaining gray/white integer-corner rays satisfy

```text
ray length > 1/2,          |h'| < 9,
|h''| < 21,                ||dG||_1 < 10.
```

The remaining endpoint, chart, homogeneity and fixed-angle faces are affine
coordinate levels or regular pullbacks of them.  No recovery-carrier
curvature is retyped as physical-face curvature.

## Arbitrary finite rank path

For incidence rank `B>=14`, use the frozen envelopes

```text
L(B)=150*2^B,              M(B)=42672*2^(3B).
```

For a rank path `(B_1,...,B_j)`, define

```text
D_0=E_0=1, H_0=0,
D_i=L(B_i)D_(i-1),
E_i=L(B_i)E_(i-1),
H_i=M(B_i)D_(i-1)^2+L(B_i)H_(i-1).
```

If the base level satisfies

```text
1<=||dG||_1<=G0,           ||D2G||<=K0,
```

then its pullback has

```text
||d(G o T^j)||_1 > 1/E_j,
||D2(G o T^j)|| < K0*D_j^2+G0*H_j,
F9 < (3/2)*E_j*(K0*D_j^2+G0*H_j).
```

The certificate independently replays five sample paths through depth four
and covers all seven frozen one-step collision-boundary types.

## Strict boundary

The value is finite for each fixed finite rank path, but it is not uniform in
depth or rank.  No collision-SRB `L^p` sum of these values is proved.  F10,
F14--F18 and every complete 18-field block remain open.

## Evidence

- `deliverables/cm2_gate5_round36_all_face_rank_path_f9_cert.py`
- `deliverables/cm2_gate5_round36_all_face_rank_path_f9_verifier.py`
- `deliverables/cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json`

Validation passes syntax, dependency integrity, replay and live fail-close;
the suite rejects `16/16` hostile mutations.
