# Independent agent challenge of the finite-certificate proof

This is an independent AI mathematical challenge within the author-revision
workflow. It is not an external referee report, a human expert endorsement,
a proof-assistant certificate, or an editorial assessment. The reviewing
agent authored section 33 and its supplement; it did not author section 35.

## Reviewed identity

- Source: `papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form/sections/35-finite-certificates.tex`
- SHA-256: `20bf2e7a32c6f8dcb9bde276f947dbc112604dc9e15c02c766111f6aacb03ee4`
- Scope: the entire source file, including all statements and proofs.
- Outcome: no substantive mathematical gap found in this challenge. This
  limited outcome does not certify correctness of the entire paper.

## Finite-word equivalence and positive separation

For the difference of a d-dimensional supplied response and an M-state
candidate, the nonzero initial row lies in a (d+M)-dimensional space. The
reachable spans of words up to length j stabilize as soon as two successive
spans agree. They therefore stabilize no later than j=d+M−1. Vanishing on
the indicated finite probes implies vanishing on the entire closed span.
This argument does not require the supplied representation to be minimal.

The parameter product of all candidate stochastic rows and decoder rows is
compact. The maximum finite-probe error is continuous, so the minimum is
attained. Infeasibility of exact all-word realization consequently gives a
strictly positive gap, rather than merely a nonzero error for each candidate.
The triangle-inequality perturbation bound correctly imposes no rank
hypothesis on the perturbed response.

For algebraic coefficients, the finite minimization is a semialgebraic
problem over the real algebraic numbers. The unique minimum value and a
sample minimizing parameter point are algebraic and effectively obtainable
by real quantifier elimination. A positive rational strict lower bound is
then computable. The article correctly distinguishes this algorithmic
existence statement from the finite diagnostics actually executed.

## Physical perturbations and common-background realization

The channel telescoping estimate gives trace-norm error at most
h_rho + |w| h_Phi. Both output states have unit trace. Subtracting I/2 from
the terminal effect gives operator norm at most 1/2, while the effect
perturbation contributes h_E. Thus the factor one half in the displayed
finite physical probe estimate is justified.

In the normal-form controller, averaging the initial core distribution over
the finite observable group produces a common stationary row pi. It has
zero mass on the initializer when one is present. Consequently both
Q_a J=J and J Q_a=J hold for J=1 pi, including the initializer row. The
command-specific product identity holds at every nonempty word and at the
empty word. The bound 1−product(alpha_a)≤|w| epsilon supplies the lower
threshold from delta_(m−1), and unreachable padding excludes all smaller
label counts. The nonconstant case has d,m≥2, so its denominator is positive.

The least Hilbert–Schmidt norm point of the compact convex hull of the
physical unitary orbit exists and is unique. Every physical conjugation
preserves the convex hull and the norm, so the point is invariant. Its
observable image is an invariant point in the convex hull of the finite
observable orbit. Applying finite group averaging identifies that image
with the group-averaged response. This proves the stated physical reset
background construction; it does not require a maximally mixed state.

## Period-four certificate

For any row-stochastic 3 by 3 matrix Q, its characteristic polynomial is
z^3−t z^2+(t+h−1)z−h, where t=tr(Q) and h=det(Q). Nonnegative rows with
unit sums give 0≤t≤3, |h|≤1 and |t+h−1|≤3. Applying its recurrence to
the first five target coefficients (1,1/2,0,1/2,1) yields
|t−h|≤16 eta and |2−t−h|≤16 eta, hence |t−1|,|h−1|≤16 eta.

Writing a_i=1−Q_ii and using the second characteristic coefficient gives
the exact nonnegative identity

    t^2−3t+3−3h = (1/2) sum_(i<j)(a_i−a_j)^2
                   +3 sum_(i<j)Q_ij Q_ji.

The recurrence constraints instead bound the left side by
−2+64 eta+256 eta^2, at most −2/81 when eta≤1/36. Thus error at most
1/36 is infeasible. Compactness makes the minimum on these five probes
strictly greater than 1/36; the six-probe delta_3 is at least this minimum.

The four-cycle decoder (1,1/2,0,1/2) attains the undamped response and its
stationary reset attains the damped response. On probes 0 through 5,
the perturbation is at most (5/2)(1−alpha), which is at most 1/36 for
alpha≥89/90. Because the gap is strictly larger, the inclusive stated
interval is valid. No claim of a sharp first transition point is needed.

## Limits

This challenge independently checks the written mathematical chain. It
does not claim to have executed a general real-algebraic minimizer, searched
all stochastic matrices numerically, or verified the manuscript in a
formal proof system. Earlier finite-check counts and hashes lost during
workspace maintenance are not treated as current execution identities.
