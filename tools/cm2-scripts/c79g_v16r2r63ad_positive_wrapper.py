#!/usr/bin/env python3
"""Run the r63ad positive authorize through a blocking held stdout pipe."""
from __future__ import annotations

import json
import os
from pathlib import Path
import selectors
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts/c79g_v16r2r63ad_external_held_fd_bootstrap.py"
LAUNCHER_SHA256 = "854fecc76955f47b91123e8c3b5d6acb959a92dfeb2964052838390925732b87"
TIMEOUT_SECONDS = 1800


def drain(proc: subprocess.Popen[bytes], read_fd: int) -> tuple[bytes, bytes, bool]:
    selector = selectors.DefaultSelector()
    selector.register(read_fd, selectors.EVENT_READ, "stdout")
    assert proc.stderr is not None
    selector.register(proc.stderr.fileno(), selectors.EVENT_READ, "stderr")
    out = bytearray(); err = bytearray()
    deadline = time.monotonic() + TIMEOUT_SECONDS
    timed_out = False
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                proc.kill()
                break
            for key, _ in selector.select(min(remaining, 1.0)):
                fd = int(key.fd)
                try:
                    block = os.read(fd, 1 << 16)
                except InterruptedError:
                    continue
                if block:
                    (out if key.data == "stdout" else err).extend(block)
                else:
                    selector.unregister(fd)
                    if key.data == "stdout":
                        os.close(fd)
            if proc.poll() is not None and not selector.get_map():
                break
    finally:
        selector.close()
    return bytes(out), bytes(err), timed_out


def main() -> int:
    read_fd, write_fd = os.pipe()
    env = {
        "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSITE": "1", "PYTHONNOUSERSITE": "1",
        "CM2_R63AD_AUTHORIZE_APPROVED": "1",
    }
    proc = subprocess.Popen(
        ["/usr/bin/python3", "-I", "-B", "-S", str(BOOTSTRAP),
         "--workspace-root", str(ROOT),
         "--expected-launcher-sha256", LAUNCHER_SHA256, "authorize"],
        cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL,
        stdout=write_fd, stderr=subprocess.PIPE, close_fds=True)
    os.close(write_fd)
    raw, err, timed_out = drain(proc, read_fd)
    rc = proc.wait()
    report: dict[str, object] = {
        "schema": "cm2.c79g.v16r2r63ad-positive-wrapper-run-report.v1",
        "command": "authorize", "returncode": rc, "timed_out": timed_out,
        "stdout_byte_count": len(raw), "stderr_byte_count": len(err),
        "stdout_newline_count": raw.count(b"\n"),
        "stderr_utf8": err.decode("utf-8", "backslashreplace"),
    }
    if raw:
        try:
            lines = raw.splitlines(keepends=True)
            if len(lines) == 1 and lines[0].endswith(b"\n"):
                value = json.loads(lines[0].decode("utf-8"))
                report["stdout_json"] = value
                report["stdout_json_canonical"] = (
                    json.dumps(value, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False).encode("utf-8") + b"\n" == lines[0])
        except Exception as exc:
            report["stdout_parse_error"] = repr(exc)
    print(json.dumps(report, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":")))
    return 0 if rc == 0 and not timed_out else (rc if rc else 124)


if __name__ == "__main__":
    raise SystemExit(main())
