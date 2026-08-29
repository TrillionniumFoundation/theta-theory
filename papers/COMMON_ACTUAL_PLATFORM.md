# Common actual platform - deterministic path-ensemble v6

The load-bearing platform is `FB4-PE-v1`, an invertible area-preserving
four-branch baker collision map with natural Lebesgue measure.

A base preparation at current `a0=2/5` is conditioned on a mechanical signed
winding current.  For target current `a in (-1,1)`,

\[
\theta(a)=I'(a)=\frac12\log\frac{3(1+a)}{7(1-a)}.
\]

The canonical tilted path law is exactly the Lebesgue branch law of another
member of the same moving-seam family.  The branch impulse and roof are

\[
d_1=(2,0),\ d_2=(-1,0),\ d_3=(0,4),\ d_4=(0,-3),
\]

\[
\tau_1=\tau_2=2,\qquad \tau_3=\tau_4=1.
\]

Thus

\[
C(a)=\operatorname{diag}(1-a,6(1+a)),\qquad
\bar\tau(a)=\frac{3-a}{2}.
\]

Paper I derives the natural law, LDP, ensemble equivalence, theta, driven map,
and excess pressure.  Paper II derives the physical stochastic limit.  Paper
III derives the microscopic free-energy DPP and physical theta-HJB.  Paper IV
handles information and optimizer response.  Paper V proves axiomatic rigidity
and tangent representations.

`OB3-MG-v1`, `FB4-EXACT-v1`, and `SL-SIM-v1` are retained as physical or
benchmark branches but do not supply load-bearing coefficients to the v6
same-platform theorem.
