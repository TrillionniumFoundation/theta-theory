#!/usr/bin/env python3
"""Run the r62 positive cold-launch through a real blocking held FD.

This runner intentionally keeps the launcher's fd 1 attached to an anonymous
blocking pipe.  It drains that pipe while the child is alive, so a large
virtual root cannot deadlock the launcher at its semantic commit write.  The
runner itself does not create or modify deliverables; it only reports the
child's terminal JSON line and stderr for independent post-run validation.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts/c79g_v16r2r62_external_held_fd_bootstrap.py"
LAUNCHER_SHA256 = "d82461275e83ce720b1c18751b54de5611781db9992eae63e57091a4bf9230f0"
TIMEOUT_SECONDS = 1800


def _drain(proc: subprocess.Popen[bytes], read_fd: int) -> tuple[bytes, bytes, bool]:
    """Drain child stdout and stderr without allowing either pipe to block."""
    selector = selectors.DefaultSelector()
    selector.register(read_fd, selectors.EVENT_READ, "stdout")
    assert proc.stderr is not None
    selector.register(proc.stderr.fileno(), selectors.EVENT_READ, "stderr")
    out = bytearray()
    err = bytearray()
    deadline = time.monotonic() + TIMEOUT_SECONDS
    timed_out = False
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                proc.kill()
                break
            events = selector.select(min(remaining, 1.0))
            for key, _ in events:
                fd = int(key.fd)
                try:
                    block = os.read(fd, 1 << 16)
                except InterruptedError:
                    continue
                if block:
                    (out if key.data == "stdout" else err).extend(block)
                else:
                    selector.unregister(fd)
                    os.close(fd) if key.data == "stdout" else None
            if proc.poll() is not None and not selector.get_map():
                break
    finally:
        selector.close()
    return bytes(out), bytes(err), timed_out


def main() -> int:
    read_fd, write_fd = os.pipe()
    # Keep the write end inheritable only for the child's fd 1.  The external
    # bootstrap itself passes this descriptor through unchanged.
    env = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "CM2_R62_AUTHORIZE_APPROVED": "1",
    }
    proc = subprocess.Popen(
        [
            "/usr/bin/python3", "-I", "-B", "-S", str(BOOTSTRAP),
            "--workspace-root", str(ROOT),
            "--expected-launcher-sha256", LAUNCHER_SHA256,
            "authorize",
        ],
        cwd=str(ROOT),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=write_fd,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    os.close(write_fd)
    raw, err, timed_out = _drain(proc, read_fd)
    rc = proc.wait()
    report: dict[str, object] = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16r2r62-positive-wrapper-run-report.v1",
        "command": "authorize",
        "returncode": rc,
        "timed_out": timed_out,
        "stdout_byte_count": len(raw),
        "stderr_byte_count": len(err),
        "stdout_newline_count": raw.count(b"\n"),
        "stderr_utf8": err.decode("utf-8", "backslashreplace"),
    }
    if raw:
        try:
            lines = raw.splitlines(keepends=True)
            if len(lines) == 1 and lines[0].endswith(b"\n"):
                value = json.loads(lines[0].decode("utf-8"))
                report["stdout_json"] = value
                report["stdout_json_canonical"] = (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n" == lines[0])
        except Exception as exc:
            report["stdout_parse_error"] = repr(exc)
    print(json.dumps(report, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
    return 0 if rc == 0 and not timed_out else (rc if rc else 124)


if __name__ == "__main__":
    raise SystemExit(main())
