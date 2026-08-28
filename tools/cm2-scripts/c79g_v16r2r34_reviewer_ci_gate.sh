#!/usr/bin/env bash
# Fail-closed, read-only r34 reviewer gate.
#
# A and B are independent static checkers.  Every acceptance assertion is
# evaluated with jq -e so a FAIL JSON cannot be masked by shell status 0.  The
# semantic audit is included as a third zero-credit witness; this wrapper never
# invokes a launcher, freeze, manifest, outer, runtime, or publication path.
set -u -o pipefail

if (( $# != 0 )); then
  echo 'FAIL_CLOSED_R34_REVIEW_CI: arguments are forbidden' >&2
  exit 2
fi

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
SUFFIX="${CM2_SUCCESSOR_SUFFIX:-v16r2r34}"
PREV="${CM2_PREDECESSOR_SUFFIX:-v16r2r33}"
REVIEWER="$ROOT/scripts/c79g_v16r2r20_independent_reviewer.py"
CHECKER_B="$ROOT/scripts/c79g_v16r2r23_structure_checker_b.py"
SEMANTIC="$ROOT/scripts/c79g_v16r2r34_runtime_semantic_audit.py"

command -v jq >/dev/null 2>&1 || {
  echo 'FAIL_CLOSED_R34_REVIEW_CI: jq required' >&2
  exit 2
}
for required in "$REVIEWER" "$CHECKER_B" "$SEMANTIC"; do
  [[ -f "$required" ]] || {
    echo "FAIL_CLOSED_R34_REVIEW_CI: missing $required" >&2
    exit 2
  }
done

WORK="$(mktemp -d "${TMPDIR:-/tmp}/cm2-r34-review.XXXXXX")"
cleanup() { rm -f -- "$WORK"/*.json; rmdir -- "$WORK" 2>/dev/null || :; }
trap cleanup EXIT HUP INT TERM

set +e
CM2_SUCCESSOR_SUFFIX="$SUFFIX" CM2_PREDECESSOR_SUFFIX="$PREV" \
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$REVIEWER" >"$WORK/a.json"
A_RC=$?
CM2_SUCCESSOR_SUFFIX="$SUFFIX" CM2_PREDECESSOR_SUFFIX="$PREV" \
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$CHECKER_B" >"$WORK/b.json"
B_RC=$?
CM2_SUCCESSOR_SUFFIX="$SUFFIX" CM2_PREDECESSOR_SUFFIX="$PREV" \
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$SEMANTIC" >"$WORK/semantic.json"
SEMANTIC_RC=$?
set -e

set +e
jq -e --arg suffix "$SUFFIX" --arg predecessor "$PREV" '
  type == "object"
  and .schema == ("cm2.c79g.successor." + $suffix + "-independent-read-only-review.v1")
  and .successor_suffix == $suffix
  and .predecessor_suffix == $predecessor
  and .status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"
  and .read_only == true
  and (.check_count | type == "number" and . == 34)
  and (.failed_check_count | type == "number" and . == 0)
  and ((.checks | type) == "array" and (.checks | length) == 34)
  and (.checks | all(.[]; .passed == true))
  and ((.failed_checks | type) == "array" and (.failed_checks | length) == 0)
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
  and .runtime_authorized == false
' "$WORK/a.json" >/dev/null
A_JQ=$?

jq -e --arg suffix "$SUFFIX" --arg predecessor "$PREV" '
  type == "object"
  and .schema == ("cm2.c79g." + $suffix + ".independent-checker-b.v1")
  and .successor_suffix == $suffix
  and .predecessor_suffix == $predecessor
  and .status == "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT"
  and .read_only == true
  and (.check_count | type == "number" and . == 16)
  and (.failed_check_count | type == "number" and . == 0)
  and ((.checks | type) == "array" and (.checks | length) == 16)
  and (.checks | all(.[]; .passed == true))
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
  and .runtime_authorized == false
' "$WORK/b.json" >/dev/null
B_JQ=$?

jq -e --arg suffix "$SUFFIX" --arg predecessor "$PREV" '
  type == "object"
  and .schema == ("cm2.c79g." + $suffix + ".runtime-semantic-audit.v1")
  and .successor_suffix == $suffix
  and .predecessor_suffix == $predecessor
  and .status == "PASS_R34_CURRENT_PATH_CHECKPOINT_AND_TRUST_AUDIT__ZERO_CREDIT"
  and .read_only == true
  and (.check_count | type == "number" and . == 8)
  and (.failed_check_count | type == "number" and . == 0)
  and ((.checks | type) == "array" and (.checks | length) == 8)
  and (.checks | all(.[]; .passed == true))
  and (.focused_report.status == "PASS_R34_PATCH_SPEC_CHECK__ZERO_CREDIT")
  and .formal_global_closure_credit == 0
  and .D02_unlock == false
  and .runtime_authorized == false
' "$WORK/semantic.json" >/dev/null
SEMANTIC_JQ=$?
set -e

if (( A_RC != 0 || B_RC != 0 || SEMANTIC_RC != 0 ||
      A_JQ != 0 || B_JQ != 0 || SEMANTIC_JQ != 0 )); then
  echo "FAIL_CLOSED_R34_REVIEW_CI: A=${A_RC}/${A_JQ} B=${B_RC}/${B_JQ} semantic=${SEMANTIC_RC}/${SEMANTIC_JQ}" >&2
  cat -- "$WORK/a.json" "$WORK/b.json" "$WORK/semantic.json"
  exit 1
fi

# Emit one valid composite JSON object for downstream guards.
jq -n --slurpfile reviewer_a "$WORK/a.json" \
      --slurpfile checker_b "$WORK/b.json" \
      --slurpfile semantic "$WORK/semantic.json" \
  --arg suffix "$SUFFIX" --arg predecessor "$PREV" '
  {
    schema: ("cm2.c79g." + $suffix + ".reviewer-ci.v1"),
    status: "PASS_R34_REVIEW_CI__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
    successor_suffix: $suffix, predecessor_suffix: $predecessor,
    reviewer_a: $reviewer_a[0], checker_b: $checker_b[0], semantic_audit: $semantic[0],
    formal_global_closure_credit: 0, D02_unlock: false,
    runtime_authorized: false, read_only: true
  }
'
exit 0
