# Exact TeX diagnostics in revision 107

The first exact-SHA run, `38512560347` at commit `2fad9446935a3c3efe6682715c8989ef66f1726d`, completed the source checks and both manuscript compilations but stopped at the strict log gate on one amsmath advisory. Its source is the byte-preserved inherited `core/253_uniform_positive_residence_persistence.tex`, line 21, which uses the valid plain-TeX fraction command `\over`. The advisory recommends `\frac` or `\genfrac`; it is not an undefined reference, missing glyph or layout overflow.

`tools/audit_v107_texlog.py` records exactly that advisory, verifies the document, exact multiline message, source context and line number, and rejects every other diagnostic previously rejected by the gate. The full unfiltered log remains in the build artifact. No mathematical source or inherited file was changed to silence the advisory. No blanket warning filter, continuation after a TeX error or preview bypass is introduced.

The current qualification must be read from its actual final-commit run. The source checker, optimized/non-optimized comparison, stabilized reference requirement, recorder coverage and clean tracked-tree check remain active. Successful source and typesetting checks are not mathematical proof certification.
