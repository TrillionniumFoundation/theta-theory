#!/usr/bin/env bash
# jq -e fail-closed CI gate for the r16 34/34 reviewer.
set -u -o pipefail
root_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)"
reviewer="$root_dir/scripts/c79g_v16r2r16_independent_reviewer.py"
command -v jq >/dev/null 2>&1 || exit 2
[[ -f "$reviewer" ]] || exit 2
tmp="$(mktemp "${TMPDIR:-/tmp}/cm2-r16-review.XXXXXX.json")"
trap 'rm -f -- "$tmp"' EXIT HUP INT TERM
set +e
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$reviewer" >"$tmp"
review_rc=$?
set -e
set +e
jq -e '
  type == "object"
  and .schema == "cm2.c79g.successor.v16r2r16-independent-read-only-review.v1"
  and .successor_suffix == "v16r2r16"
  and .predecessor_suffix == "v16r2r15"
  and .status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"
  and .read_only == true
  and .check_count == 34
  and .failed_check_count == 0
  and (.failed_checks | length) == 0
  and (.checks | length) == 34
  and (.checks | all(.[]; .passed == true))
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
  and .runtime_authorized == false
' "$tmp" >/dev/null
jq_rc=$?
set -e
if [[ "$review_rc" -ne 0 || "$jq_rc" -ne 0 ]]; then
  cat "$tmp"
  exit 1
fi
cat "$tmp"
