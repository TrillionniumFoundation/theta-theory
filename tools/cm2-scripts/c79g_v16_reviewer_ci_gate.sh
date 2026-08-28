#!/usr/bin/env bash
# Fail-closed v16 source reviewer gate.  The Python reviewer is read-only;
# jq -e is the normative status gate so a reviewer that prints PASS while
# returning shell status 0/incorrect JSON cannot slip through CI.
set -euo pipefail

if (($# != 0)); then
  echo 'FAIL_CLOSED_V16_REVIEW_CI: arguments are forbidden' >&2
  exit 2
fi

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
REVIEWER="$ROOT/scripts/c79g_v16_independent_reviewer.py"
command -v jq >/dev/null 2>&1 || { echo 'FAIL_CLOSED_V16_REVIEW_CI: jq required' >&2; exit 2; }
[[ -f "$REVIEWER" ]] || { echo 'FAIL_CLOSED_V16_REVIEW_CI: reviewer missing' >&2; exit 2; }

REPORT_FILE="$(mktemp -t c79g-v16-independent-review.XXXXXX)"
cleanup() { rm -f -- "$REPORT_FILE"; }
trap cleanup EXIT HUP INT TERM

set +e
/usr/bin/python3 -I -B "$REVIEWER" >"$REPORT_FILE"
REVIEW_RC=$?
set -e
cat -- "$REPORT_FILE"

if ! jq -e '
  type == "object"
  and .schema == "cm2.c79g.v16.independent-read-only-static-review.v1"
  and .status == "PASS_V16_STATIC_34_OF_34__PINS_REBUILT__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
  and .read_only == true
  and .protocol_python_imported_or_executed == false
  and .protocol_or_runtime_files_written == false
  and (.check_count | type == "number" and . == 34)
  and (.failed_check_count | type == "number" and . == 0)
  and ((.failed_checks | type) == "array")
  and ((.failed_checks | length) == 0)
  and ((.checks | type) == "array")
  and ((.checks | length) == 34)
  and ((.checks | all(.[]; .passed == true)))
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
' "$REPORT_FILE" >/dev/null; then
  echo 'FAIL_CLOSED_V16_REVIEW_CI: jq -e 34/34 gate failed' >&2
  exit 1
fi
if ((REVIEW_RC != 0)); then
  echo "FAIL_CLOSED_V16_REVIEW_CI: reviewer exited $REVIEW_RC" >&2
  exit "$REVIEW_RC"
fi
exit 0
