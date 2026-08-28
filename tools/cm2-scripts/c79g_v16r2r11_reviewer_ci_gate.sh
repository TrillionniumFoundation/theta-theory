#!/usr/bin/env bash
# Fail-closed CI wrapper for the versioned r11 reviewer.
# jq -e output is redirected so a false predicate cannot leak a leading
# ``false`` line into the auditable JSON stream.
set -u -o pipefail

root_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)"
reviewer="$root_dir/scripts/c79g_v16r2r11_independent_reviewer.py"
suffix="${CM2_SUCCESSOR_SUFFIX:-v16r2r11}"
predecessor="${CM2_PREDECESSOR_SUFFIX:-v16r2r10}"
command -v jq >/dev/null 2>&1 || {
  echo 'FAIL_CLOSED_R11_REVIEW_CI: jq required' >&2
  exit 2
}
[[ -f "$reviewer" ]] || {
  echo 'FAIL_CLOSED_R11_REVIEW_CI: reviewer missing' >&2
  exit 2
}

report_tmp="$(mktemp "${TMPDIR:-/tmp}/cm2-r11-review.XXXXXX.json")"
trap 'rm -f -- "$report_tmp"' EXIT HUP INT TERM

set +e
CM2_SUCCESSOR_SUFFIX="$suffix" CM2_PREDECESSOR_SUFFIX="$predecessor" \
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$reviewer" >"$report_tmp"
review_rc=$?
set -e

set +e
jq -e --arg suffix "$suffix" --arg predecessor "$predecessor" '
  type == "object"
  and (.schema | type == "string" and startswith("cm2.c79g.successor.v16r2r11-independent-read-only-review.v1"))
  and .successor_suffix == $suffix
  and .predecessor_suffix == $predecessor
  and .status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"
  and .read_only == true
  and (.check_count == 34)
  and (.failed_check_count == 0)
  and ((.failed_checks | type) == "array")
  and ((.failed_checks | length) == 0)
  and ((.checks | type) == "array")
  and ((.checks | length) == 34)
  and (.checks | all(.[]; .passed == true))
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
  and .runtime_authorized == false
' "$report_tmp" >/dev/null
jq_rc=$?
set -e

if [[ "$review_rc" -ne 0 || "$jq_rc" -ne 0 ]]; then
  cat -- "$report_tmp"
  exit 1
fi
cat -- "$report_tmp"
exit 0
