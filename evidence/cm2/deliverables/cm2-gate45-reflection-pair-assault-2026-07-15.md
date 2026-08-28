# CM2 Gates 4--5 continuation: a reflection-paired incidence orbit

Date: 2026-07-15  
Model: centred rational two-disk torus pilot on the standard solid-boundary
section; horizontal white-centre parameter s  
Verdict: **a two-row symmetry orbit and its local roof cancellation are
certified; Gates 4 and 5 remain globally open**

## 1. What is new

The previously certified positive-width grouped incidence

~~~text
A: G[0,0] -- tangent W[0,0] -- G[1,1]
~~~

has now been completed to its parameter-reflection partner

~~~text
Jx(A): G[1,0] -- tangent W[0,0] -- G[0,1].
~~~

The two rows:

1. are physical on the full certified theta band;
2. have one common absolute coarea law by Euclidean isometry;
3. use the same local Kac vector mark (+1,-1);
4. are isometric in the local source/test norms;
5. have opposite parameter-current polarities; and
6. therefore have exactly cancelling scalar roof-current masses.

This is the first rowwise cancellation certificate for the singular roof
term.  It covers one complete two-row symmetry orbit, not the global event
registry.

## 2. Exact conjugacies

Write the white centres as

~~~text
W(i,j;s)=(i+1/2+s,j+1/2).
~~~

At the centred table define

~~~text
Jx(x,y)=(1-x,y),       Jy(x,y)=(x,1-y).
~~~

Their lift-label actions are

~~~text
Jx G(i,j)=G(1-i,j),    Jx W(i,j;s)=W(-i,j;-s),
Jy G(i,j)=G(i,1-j),    Jy W(i,j;s)=W(i,-j;s).
~~~

Thus Jx conjugates the billiard at s to the billiard at -s and sends the
original row to

~~~text
G[1,0] -- tangent W[0,0] -- G[0,1].
~~~

The y-reflection sends the endpoint labels of A to the endpoint-swapped
labels of Jx(A).  Together with collision time reversal, it identifies the
two non-grazing endpoint descriptions as alternative representations of one
row; they are not added as two coefficient occurrences.

All these identities are exact isometries of the circular table.  They
preserve flight lengths, discriminants, incidence cosines, first-hit order,
the collision flux form and the stable/unstable cone typing.  Hence the
200-bit Arb proof for A transports without a new numerical loss to Jx(A).

## 3. Coarea polarity and the roof-current cancellation

Choose compatible event functions.  The branch conjugacy gives

~~~text
H_{Jx(A),s}(Jx z)=H_{A,-s}(z).
~~~

Differentiating at s=0 yields

~~~text
partial_s H_{Jx(A),0}(Jx z)
  = - partial_s H_{A,0}(z).
~~~

The collision flux and the absolute coarea Jacobian are invariant under Jx.
Consequently, after pulling both rows to the same occurrence coordinate,
their positive coefficient measures agree:

~~~text
m_{Jx(A)}=m_A=:m_orbit,
~~~

while their signed polarities are +1 and -1.  For the scalar roof test 1,

~~~text
<dot r_A,1> + <dot r_{Jx(A)},1>
 = integral 1 dm_orbit - integral 1 dm_orbit
 = 0.
~~~

This is an exact cancellation of two distinct additive roof rows.  It does
not add the forward and reverse descriptions within either row.

The result is local in event space.  It does not imply the global identity
by itself: all other symmetry orbits and any non-symmetric incidence rows
must first be present in the immutable Gate-3 registry.

## 4. Kac vector mark and local single charging

Both rows use the already proved vector occurrence

~~~text
coordinates = (moving-level dot(S), roof dot(r)*phase-mean),
Kac mark   = (+1,-1).
~~~

The reflection changes the row polarity, not this structural Kac mark.  Each
row therefore uses the same local pre-recovery constant and the reflected
copy of

~~~text
q_0=max(C_backward,C_forward,2)m_orbit.
~~~

There is one q charge per distinct occurrence row; the two endpoint views of
one row are still charged only once.  The two different reflection rows are
additive physical occurrences and are not collapsed into one q atom.

No stopped-parent recovery mark is hidden here.  The fat-Cantor restriction
obstruction from the preceding report still applies, so global admissibility
requires a controlled cylinder restriction algebra or the actual Gate-2 PPE
with parentwise normalization cost.

### 4.1 Local source/test norm isometry

Choose the finite physical chart atlas together with its images under Jx and
Jy.  The reflections preserve curve length, endpoint count, C2 chart marks,
coarea density regularity, homogeneity rank and dynamic separation time.
They therefore biject positive decompositions in both the standard-family
and flux norms without changing any summand cost.  Pullback likewise
preserves the local test sup norm, dynamic Holder seminorm and face-chart C1
norm.  Hence Jx is an isometry on this two-row local source/test pair.

This closes the reflection transport of the already typed local row; it is
not the global phase CM2 norm lift, which also requires every event row,
return prefix/suffix block and recovery envelope.

## 5. Certified and open layers

Certified:

~~~text
ORIGINAL_GROUPED_INCIDENCE: CERTIFIED
REFLECTED_GROUPED_INCIDENCE: CERTIFIED
COMMON_ABSOLUTE_COAREA_BY_ISOMETRY: CERTIFIED
ENDPOINT_VIEWS_NONADDITIVE: CERTIFIED
SAME_LOCAL_KAC_MARK: CERTIFIED
LOCAL_REFLECTION_SOURCE_TEST_NORM_ISOMETRY: CERTIFIED
TWO_ROW_ROOF_CURRENT_MASS_CANCELLATION: CERTIFIED
~~~

Open:

~~~text
COMPLETE_GLOBAL_EVENT_REGISTRY: NOT CERTIFIED
ALL_REFLECTION_ORBITS_AND_NONSYMMETRIC_ROWS: NOT CERTIFIED
GLOBAL_SINGLE_CHARGE_LEDGER: NOT CERTIFIED
GLOBAL_STOPPED_PARENT_RECOVERY: NOT CERTIFIED
GLOBAL_ROOF_CURRENT_ROW_CANCELLATION: NOT CERTIFIED
FOUR_TERM_KAC_TYPING: NOT CERTIFIED
PHASE_CM2_NORM_LIFTS: NOT CERTIFIED
GATE_4: NOT CERTIFIED
GATE_5: NOT CERTIFIED
~~~

## 6. Latest-technology check

The arXiv API was queried on 2026-07-15 for dispersing/Sinai billiard linear
response, anisotropic billiard Banach spaces and moving-scatterer response.
The newest directly relevant item returned was still Canestrari,
arXiv:2604.19671v2, on a fixed Sinai billiard with small holes.  Its
standard-family relaxation is useful after an entry family is built, but it
does not construct this moving-scatterer event registry, its reflected
boundary currents or the stopped restriction ledger.

## 7. Reproduction

~~~bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate45_reflection_pair_cert.py \
  deliverables/cm2_gate45_reflection_pair_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_reflection_pair_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_reflection_pair_verifier.py --self-test

# Expected exit 2 until every global field is present.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_reflection_pair_verifier.py
~~~

The certificate and self-test exit zero.  The live fail-closed verifier exits
two because the global registry, recovery, Kac and norm-lift fields remain
null.
