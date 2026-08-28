#!/usr/bin/env bash
# Fail-closed jq -e gate for the parameterized 34-check static reviewer.
# The reviewer is read-only; this wrapper only uses a temporary report in
# TMPDIR and never touches deliverables or runtime surfaces.
set -u -o pipefail

if (( $# != 0 )); then
  echo 'FAIL_CLOSED_C79G_REVIEW_CI: arguments are forbidden' >&2
  exit 2
fi

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
REVIEWER="$ROOT/scripts/c79g_v16r2r20_independent_reviewer.py"
SUFFIX="${CM2_SUCCESSOR_SUFFIX:-v16r2r20}"
PREV="${CM2_PREDECESSOR_SUFFIX:-v16r2r19}"

command -v jq >/dev/null 2>&1 || {
  echo 'FAIL_CLOSED_C79G_REVIEW_CI: jq required' >&2
  exit 2
}
[[ -f "$REVIEWER" ]] || {
  echo 'FAIL_CLOSED_C79G_REVIEW_CI: reviewer missing' >&2
  exit 2
}

REPORT="$(mktemp "${TMPDIR:-/tmp}/cm2-c79g-review.XXXXXX.json")"
cleanup() { rm -f -- "$REPORT"; }
trap cleanup EXIT HUP INT TERM

set +e
CM2_SUCCESSOR_SUFFIX="$SUFFIX" CM2_PREDECESSOR_SUFFIX="$PREV" \
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$REVIEWER" >"$REPORT"
REVIEW_RC=$?
set -e

set +e
jq -e --arg suffix "$SUFFIX" --arg predecessor "$PREV" '
  type == "object"
  and .schema == ("cm2.c79g.successor." + $suffix + "-independent-read-only-review.v1")
  and .successor_suffix == $suffix
  and .predecessor_suffix == $predecessor
  and .status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"
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
  and .runtime_authorized == false
' "$REPORT" >/dev/null
JQ_RC=$?
set -e

if (( REVIEW_RC != 0 || JQ_RC != 0 )); then
  echo "FAIL_CLOSED_C79G_REVIEW_CI: reviewer_rc=$REVIEW_RC jq_rc=$JQ_RC" >&2
  [[ -s "$REPORT" ]] && cat -- "$REPORT"
  exit 1
fi

cat -- "$REPORT"
exit 0
