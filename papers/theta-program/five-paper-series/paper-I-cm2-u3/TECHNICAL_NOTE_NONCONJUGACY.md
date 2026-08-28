# Technical note: nonconjugacy of the radial Sinai family

Choose the base table so that the normal period-two orbit between the radially moved scatterer and a fixed scatterer is the unique shortest regular period-two orbit, with a positive gap to every other period-two flight length.  This is an open geometric condition.

Let the centre distance be `D`.  Its one-way free flight is

\[
d(a)=D-(R_1+a)-R_2=d_0-a,
\]

so the continuous-time billiard orbit has period

\[
\mathcal T(a)=2d(a)=2d_0-2a.
\]

For small `a`, the isolation gap prevents a permutation with another period-two orbit.  A time-preserving flow conjugacy preserves the marked periodic-period multiset, while `mathcal T(a)` changes strictly.  Hence the radial flow family is nonconjugate.

For the collision-map statement, the same orbit has Jacobi return trace

\[
\operatorname{tr}M(a)
=2+4d(a)(\kappa_1(a)+\kappa_2)
 +4d(a)^2\kappa_1(a)\kappa_2,
\]

whose derivative is strictly negative.  The isolated trace therefore also rules out a local `C^1` conjugacy of the collision maps.

This isolation hypothesis is part of the actual witness.  A calculation on one unnamed periodic orbit, without isolation or marking, would not by itself exclude a conjugacy which permutes periodic orbits.
