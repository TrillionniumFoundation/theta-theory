#!/usr/bin/env bash
# Fail-closed CI entry point for the read-only v14 source reviewer.
#
# The reviewer emits the complete JSON diagnostic on stdout.  Its process
# status is useful, but is intentionally not the sole gate: this wrapper also
# evaluates the JSON with jq -e so a malformed, truncated, or contradictory
# report cannot be accepted by a shell pipeline.  The report is kept in a
# private temporary file only; no workspace artifact, runtime surface, or
# Python bytecode is written.

set -euo pipefail

if (($# != 0)); then
    echo "FAIL_CLOSED_V14_REVIEW_CI: arguments are forbidden" >&2
    exit 2
fi

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
REVIEWER="$ROOT/scripts/c79g_v14_independent_static_review.py"

if [[ ! -f "$REVIEWER" ]]; then
    echo "FAIL_CLOSED_V14_REVIEW_CI: reviewer is missing" >&2
    exit 2
fi
if ! command -v jq >/dev/null 2>&1; then
    echo "FAIL_CLOSED_V14_REVIEW_CI: jq is required" >&2
    exit 2
fi

REPORT_FILE="$(mktemp -t c79g-v14-independent-review.XXXXXX)"
cleanup() {
    rm -f -- "$REPORT_FILE"
}
trap cleanup EXIT HUP INT TERM

set +e
/usr/bin/python3 -I -B "$REVIEWER" >"$REPORT_FILE"
REVIEW_RC=$?
set -e

# Always expose the diagnostic, including on a rejected review.
cat -- "$REPORT_FILE"

# This is the normative CI gate.  Keep the exact 34/34 hard gate here rather
# than relying on Python's exit convention or on a caller's pipe semantics.
if ! jq -e '
    type == "object"
    and .schema ==
      "cm2.c79g.v14.independent-read-only-static-review.v1"
    and .status == "PASS_STATIC_BYTES__RUNTIME_NOT_AUTHORIZED"
    and .read_only == true
    and .protocol_python_imported_or_executed == false
    and .protocol_or_runtime_files_written == false
    and (.check_count | type == "number" and . == 34)
    and (.failed_check_count | type == "number" and . == 0)
    and ((.failed_checks | type) == "array"
         and (.failed_checks | length) == 0)
    and ((.checks | type) == "array"
         and (.checks | length) == 34
         and all(.checks[]; .passed == true))
    and .sections.target_v14_pyc_incident.pyc_or___pycache___created == false
    and .sections.target_v14_pyc_incident.target_pyc_count == 0
    and .sections.target_v14_pyc_incident.terminal_target_pyc_count == 0
    and .sections.terminal_snapshot.changed_file_count == 0
    and (has("fatal_error") | not)
  ' "$REPORT_FILE" >/dev/null; then
    echo "FAIL_CLOSED_V14_REVIEW_CI: jq -e 34/34 status gate failed" >&2
    exit 1
fi

# A successful JSON report must also have a successful reviewer process.  This
# catches a future implementation that accidentally prints PASS and exits
# non-zero, or one that changes its output convention without updating CI.
if ((REVIEW_RC != 0)); then
    echo "FAIL_CLOSED_V14_REVIEW_CI: reviewer exited $REVIEW_RC" >&2
    exit "$REVIEW_RC"
fi

exit 0
