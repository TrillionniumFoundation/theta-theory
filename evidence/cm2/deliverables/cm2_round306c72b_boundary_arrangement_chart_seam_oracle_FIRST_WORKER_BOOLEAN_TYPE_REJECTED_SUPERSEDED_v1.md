# Rejected / superseded C72b pre-result stage

The first `c72b-build-a.v1` attempt stopped before its first output row and
before any result object.  Its strict-normal predicate passed an integer sign
to the boolean-only fail-closed guard.  That isolated half-product is rejected
and must never be consumed, completed, renamed, or overwritten.  The successor
uses an explicit `!= 0` boolean predicate and a fresh output directory.
