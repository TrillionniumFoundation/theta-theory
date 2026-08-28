# CM2 Gates 1/3/4 round-33 2026 small-hole interface audit

Date: 2026-07-19  
Verdict: **new theorem identified; C24 shape and mass-loss interfaces still do not match**

The audit checks three exact sources against the frozen C24 open system:

- Canestrari, arXiv `2604.19671`, *Linear response for Sinai billiards with
  small holes*;
- Demers--Liverani, arXiv `2606.10155`, *Recent Progress in the Application
  of Transfer Operators to Dispersing Billiards*;
- Demers--Liverani, arXiv `2104.06947`, *Projective cones for sequential
  dispersing billiards*.

The 2026 Canestrari theorem treats one hole centered at one boundary
arclength and spanning the full angle interval.  Its normalized conditional
loss-of-memory theorem is therefore not directly a theorem for the frozen
union of 24 disjoint two-dimensional C24 rectangles.  The projective-cone
route does match the already certified finite-horizon, `O1/O1'`, `O2` and
mass-below-`1/2500` inputs, but still supplies only existential normalized
cone recovery.

The exact remaining scalar is unchanged: certify a uniform positive C24 hit
for every normalized recovered-cone density, or equivalently a stationary
killed-operator radius strictly below one.  Neither normalized loss of memory
nor Kac's first moment gives this unnormalized inequality.  Gate 2 also still
lacks the physical stable quotient, inverse branches, reverse weights and PPE.

No theorem is retyped across the hole-shape mismatch.  Gates 1--4 and CM2
remain `NOT_CERTIFIED` / `NO-GO_FOR_CLAIM`.

