# Referee guide — Paper II, revision v4

## Central claims

The paper identifies the physical-time pressure root and diffusion tensor,
proves the oriented suspension renewal formula, and establishes actual
full-frequency moving-family resolvent response for both the explicit moving
collision model and a no-eclipse open-billiard family.

## Suggested audit order

1. **Common space:** check the quadratic partition, `R_aJ_a=I`, and the extra
   zero spectral block.
2. **Pressure calculus:** verify the order typing of differentiated Riesz and
   reduced-resolvent words imported from Paper I.
3. **Physical root:** check the sign of `P_s=-bar_tau`, the covariance
   normalization, and the mixed parameter derivative formula.
4. **Renewal orientation:** derive the entry and exit roof operators from a
   trajectory decomposition.
5. **Green--Kubo:** independently expand the pressure Hessian and partial-sum
   variance, and verify equality with the Gordin bracket.
6. **Explicit coefficients:** check the finite branch pressure and uniform
   spanning/ellipticity argument.
7. **Diophantine high frequency:** verify quotient contraction, the weighted
   phase identity, scalar phase separation, the right-strip two-case estimate,
   and the frequency powers in parameter derivatives.
8. **Open-billiard high frequency:** verify the concrete temporal-shear
   calculation for asymmetric disks and the match to the uniform Dolgopyat
   theorem on the fixed symbolic space.
9. **Triangular geometry:** check every primitive lattice direction and the
   quantitative deformation margin.
10. **Coefficient lift:** check the square-root modulus and global chain rule.

## High-risk proof locations

- the scalar phase lower bound under simultaneous Diophantine approximation;
- the extension from the imaginary axis to the right strip;
- uniformity of Dolgopyat constants over the moving open-billiard family;
- frequency loss in repeated parameter-resolvent identities;
- identification of the coboundary kernel of the covariance.

## Permanent scope

The full-frequency theorem is actual for the explicit Diophantine roof family
and for the open billiard under temporal shear.  It does not claim that
compactness alone supplies a common high-frequency graph domain for every
moving recurrent Sinai table.

A report should say separately whether the referee checked the low-frequency
physical coefficient theorem, the explicit Diophantine theorem, and the
open-billiard Dolgopyat branch.
