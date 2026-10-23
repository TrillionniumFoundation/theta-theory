# Independent author check of proposed module 333

Checked source: revision-prep/333_original_section_multipliers.tex,
as read on 23 October 2026. This is an internal proof check, not an
external referee report or independent expert certification.

## Mathematical conclusion

The finite partition, section motion, multiplication estimate, weak
motion estimate and actual finite-time occupation identity are valid
in the stated common stable-curve norm-construction scope. These
claims do not establish transfer invariance of an enlarged common
curve class or any joint twisted spectral theorem.

## Primary theorem check

The 10 October 2013 author PDF of Demers--Zhang was opened directly:
https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf

Section 3.3, printed pages 12--13, defines the weak test norm,
the strong stable norm with the positive short-arc exponent alpha,
and the completion of C1 densities. Lemmas 5.2 and 5.3, printed
pages 32--33, allow the finite transverse piecewise-constant
partition used here. The multiplier argument needs that norm
construction and those geometric partition hypotheses, not the
spectral conclusions elsewhere in the paper.

The complete exponent conditions in the cited construction are
0<q<p<=1/3, 0<alpha<1-varsigma0, and
0<beta<=min(alpha,p-q). It is preferable to spell these out in
the manuscript, while retaining the qualification that the full
dynamical hypotheses are separate.

## Constant and counting check

Exact rational arithmetic gives the stated upper bound
F_q <= -6710711/2500000 = -2.6842844.
The chosen F_R bound is 678877/125000 = 5.431016 < 6.
Hence q'_R<3 and theta'_R<6 are safe.

The upper section momentum bound is
2132809/2561800 = 0.8325431337340932, and its gap to 5/6 is
6073/7685400 > 0. Thus the stated horizontal speed
36/sqrt(11)<11 is valid.

The common cone endpoints are exactly 45/47 and 799/90.
The lower angle-sine estimate is conservative for both vertical
and horizontal sides because 45/47<1.

Ten side values per coordinate, plus one angular seam, give at
most 11 by 11 cells. The count 121 is safe. For the two radius
grids, forty side crossings on each monotone chart piece give
at most 41 intervals; allowing a single seam split gives the safe
bound 82. Refinement at the swept-strip endpoints introduces no
new side values.

A common angular seam can be fixed at alpha=pi for every radius.
The actual section rectangles all lie away from it. This avoids
any ambiguity between radius-specific coordinate seams.

## Functional-space and normalization check

The weak estimate uses only the strong stable norm on short
subarcs, restriction closure, uniform monotonicity of both
coordinates and the finite number of section changes. It
extends from smooth densities by the bounded strong multipliers
and the continuous weak embedding. There is no assertion about
the distributional product before that extension.

For clarity, define the common reference measure as
dnu=cos(phi) d(alpha) d(phi)/(4 pi), identify a density h with
h dnu, and use this same identification for eta_R nu in the
transfer formula. This makes the one factor c_*^-1 explicit.

The enlarged common cone contains each physical stable cone.
Its invariance under every collision map is not proved here.
The opening wording should therefore describe the common
homogeneous test-curve family rather than assert that every
curve in the enlarged cone is an actual dynamical stable curve.
The multiplier and weak-motion estimates remain valid with
that qualification.

In the finite-time formula multiplication occurs before each
physical transfer step. It counts eta at times 0,...,m-1.
The last section multiplier tests time m separately. Thus no
extra occupation count occurs, and the initial eta_R nu divided
by c_* is precisely the original entrance measure.

## Corrections sent to the author

1. Replace the undefined reference sec:lc-transport with sec:lc-length.
2. Remove the literal plus sign in the phrase constants,+but.
3. Replace the operator exponent ^{,m} with ^{m}.
4. State the common seam, full norm exponents and density/measure
   convention explicitly.
5. Qualify the common enlarged cone as a test-curve construction;
   its dynamical invariance is a separate input.

No change to the original section, probability event, occupation
count, physical clock or final raw theorem is needed.
