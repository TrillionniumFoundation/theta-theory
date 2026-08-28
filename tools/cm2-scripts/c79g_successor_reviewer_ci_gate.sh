#!/usr/bin/env bash
set -u -o pipefail

# This gate deliberately preserves the reviewer's exit status.  ``jq -e``
# makes a PASS assertion false (and therefore non-zero) for every FAIL report;
# a plain ``jq`` would otherwise mask a failed reviewer with shell status 0.
root_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
reviewer="$root_dir/scripts/c79g_v16r2_successor_independent_reviewer.py"
suffix="${CM2_SUCCESSOR_SUFFIX:-v16r2r6}"
report_tmp="$(mktemp "${TMPDIR:-/tmp}/cm2-successor-review.XXXXXX.json")"
trap 'rm -f -- "$report_tmp"' EXIT

set +e
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -B "$reviewer" >"$report_tmp"
review_rc=$?
set -e

# jq -e returns 0 only for a genuine 34/34, zero-credit, runtime-disabled
# report.  It also rejects malformed/truncated JSON instead of treating it as
# a successful CI stream.
set +e
jq -e --arg suffix "$suffix" '
  (.successor_suffix == $suffix) and
  (.status == "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED") and
  (.check_count == 34) and (.failed_check_count == 0) and
  (.failed_checks == []) and (.formal_global_closure_credit == 0) and
  (.D02_unlock == false) and (.runtime_authorized == false)
' "$report_tmp"
jq_rc=$?
set -e

if [ "$review_rc" -ne 0 ] || [ "$jq_rc" -ne 0 ]; then
  # Preserve the full JSON for an auditable caller while returning failure.
  /usr/bin/python3 -I -B -c 'import pathlib,sys; sys.stdout.write(pathlib.Path(sys.argv[1]).read_text())' "$report_tmp"
  exit 1
fi

cat "$report_tmp"
exit 0
