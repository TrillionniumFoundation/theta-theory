# Derivation of the spectral and rank-rigidity extension

## 1. From branch ranks to a spectral cap

For each first label y the refined old Grams satisfy sum_h A_yh=rho and sum_h tr(A_yh)=1. Put w=tr(A), a=A/w. The centered-swap branch score is bounded by w(d-1/r). Exact total reward forces equality branchwise. Outside (d,r)=(2,1), the equality factors are a=b=P/r. Hence rho is a convex combination of normalized rank-r projections, and rho<=I/r.

Conversely diagonalize rho and put x_i=r lambda_i. Unit-interval translations of the integer lattice select r coordinates with inclusion probability x_i. Their at-most-d constant intervals give a finite projection decomposition. Set C_yh=sqrt(w_h/r)J_h^*, D_yh=J_h^*/sqrt(r), and use V_yh=C_yh C_0^+ on the initial Schmidt support. The Gram sum proves instrument completeness; final symmetric/antisymmetric effects attain each centered leaf value.

## 2. Three separate cuts

A pure state in I_1 tensor C^q has initial coefficient rank<=q. Classical resolution of a mixed state respects q. Each k-dimensional old Kraus output therefore has Gram rank<=min(q,k), while the independently prepared second reference has Gram rank<=ell. Existing swap bounds apply with s=min(q,k,ell). Two fixed-subspace pure preparations of rank s attain both formulas without feedback or compression.

## 3. Deficit to common-support distance

Let f=||sqrt(a)sqrt(b)||_1, eta=1-f^2 and e=tr(ab)-f^2/r. The unsaturated rank inequality gives Delta>=c*eta+e, c=d-1-1/r. Choose a right polar unitary so Z=sqrt(a)sqrt(b)U is positive. Its support has dimension<=r, trace f and squared norm tr(ab). For P containing its range, the distance to fP/r is at most sqrt(r e). Purification and Schatten-product bounds give distance from a to P/r at most (1+sqrt(2))sqrt(eta)+sqrt(r e), and distance from b at most (3+sqrt(2))sqrt(eta)+sqrt(r e). Squaring with weighted Cauchy–Schwarz proves K*Delta with K=r+(3+sqrt(2))^2/c.

## 4. Operational loss and initial spectrum

The gain normalization is alpha=t^2/[2d^2(d+1)] and sum_yh w_yh=d. Thus a loss epsilon bounds E_mu Delta by 2d(d+1)epsilon/t^2, where mu=w/d. Jensen gives a nearby rank-r projection decomposition for rho at each y. The exact unhalved trace distance from rho to the spectral cap is twice e_r(rho)=tr(rho-I/r)_+. Combining yields the quadratic initial spectral loss in Proposition 19.5.

## 5. The exceptional face

For d=2 and a pure factor a, the other factor b is tested by I-2a. The two-by-two trace/determinant identity gives centered norm sqrt(1-4|z|^2). The off-diagonal pinching error is 2|z|, so its square is 2Delta-Delta^2. Equality means commutation, even for mixed b. This is not a common-pure-state condition.

All five derivations are written in the active manuscript. The finite scripts are independent checks of examples and exact construction bookkeeping, not replacements for any quantified proof.
