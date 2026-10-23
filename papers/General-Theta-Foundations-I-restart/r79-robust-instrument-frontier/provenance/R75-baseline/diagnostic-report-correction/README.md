# Preserved report-schema failure and correction

The strict execution of `c09682b410148263268a4e7ca3e9a6fed54ed9b9` completed
the ordinary and optimized commands of all 20 diagnostic programs, but stopped
while reading the final conditional suite's report. It did not reach native
compilation or issue PASS. The unchanged actual failure receipt is retained
here, and the completed outputs are preserved with the publication validation
archive.

The conditional script reported its actual 2,078 checks as `checks` and used
named `groups`, whereas the common verifier requires `total_checks` plus
explicit exact/floating counts. The current script adds those three fields
using its actual accumulated counter and keeps the existing fields. No check,
computation, mathematical TeX or inherited diagnostic changes. The original
script and its original development reports remain byte-identical under
`provenance/author-research-r75/conditional/`. The current top-level script and
new real-SHA strict execution control the final validation result.
