# Revision 12 validation record

Revision 12 is based on the substantive v11 review commit `fd84da57359a3ad2fefed532b0b5094ab8c6e436`. It intentionally creates a new source SHA rather than rewriting the failed revision-11 packet.

The active verifier checks exact v10 restoration of `core/06_downstream.tex`, byte identity of all other unrepaired v11 core files, absence of the malformed `\\nef` reference and marked-event fragment, complete one-time inclusion of all core sections, references/citations/environments, and all inherited finite marked-return/exponent diagnostics.

The exact remote workflow is `.github/workflows/a2-dyn-v12-qualification.yml`. This static file does not predeclare a successful remote run. The actual run conclusion and artifact digest are checked after the final push.

A successful build does not certify covariance nondegeneracy, complementary-frequency resolvent estimates, the global critical/singular branch decomposition, or weighted exact-event local limits.
