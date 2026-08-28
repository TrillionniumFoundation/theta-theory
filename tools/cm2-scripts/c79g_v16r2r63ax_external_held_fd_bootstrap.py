#!/usr/bin/env python3
"""Externally pinned held-FD bootstrap for the append-only r63ax launcher."""
from __future__ import annotations

import ast
import builtins
import hashlib
import os
from pathlib import Path
import sys
from types import ModuleType

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/c79g_v16r2r63aw_external_held_fd_bootstrap.py"
BASE_SHA256 = "71d6d2035321bfbd12c02461fbe7a6831ecea2901403734d9ae987cffa238f18"
LAUNCHER_SHA256 = "216a5384dae041c0377c71360336886566e7c7ede0d8b219dd61cc08a204978c"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_impl() -> ModuleType:
    raw = BASE.read_bytes()
    if sha(raw) != BASE_SHA256:
        raise RuntimeError("immutable r63aw bootstrap recipe hash drift")
    text = raw.decode("utf-8").replace(
        "d67be1f66db7db0d7dc9bb2a5bd891baaea97fd7068d006a67755734ca16a4d2",
        LAUNCHER_SHA256)
    text = text.replace("r63aw", "r63ax").replace("R63AW", "R63AX")
    module = ModuleType("_c79g_v16r2r63ax_external_bootstrap_impl")
    module.__file__ = str(BASE)
    module.__package__ = None
    sys.modules[module.__name__] = module
    tree = ast.parse(text, str(BASE), mode="exec")
    exec(compile(tree, str(BASE), "exec"), module.__dict__, module.__dict__)
    return module


# The inherited r63aw repair lives under its own ``__main__`` guard.  This
# successor loads that bootstrap as a module, so install the same source
# projection at this outer boundary before entering the cold launcher.
_ROOT_REPLAY_OLD = (
    "            need(fingerprint(root_now) == fingerprint(self.root_identity.state) ==\n"
    "                 fingerprint(root_path_state) and\n"
    "                 directory_identity(root_label) == directory_identity(self.root_identity.state) and\n"
    "                 mount_id(self.root_fd) == mount_id(root_path_fd) == self.root_identity.mnt_id,\n"
    "                 \"root path/fd drift\")")
_ROOT_REPLAY_NEW = (
    "            need(directory_identity(root_now) == directory_identity(self.root_identity.state) ==\n"
    "                 directory_identity(root_path_state) and\n"
    "                 directory_identity(root_label) == directory_identity(self.root_identity.state) and\n"
    "                 mount_id(self.root_fd) == mount_id(root_path_fd) == self.root_identity.mnt_id,\n"
    "                 \"root path/fd drift\")")


def _compile_with_stable_root(real_compile):
    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        if "class HeldLauncher" in source_text and _ROOT_REPLAY_OLD in source_text:
            if source_text.count(_ROOT_REPLAY_OLD) != 1:
                raise RuntimeError("r63ax root replay anchor multiplicity drift")
            source_text = source_text.replace(_ROOT_REPLAY_OLD, _ROOT_REPLAY_NEW, 1)
            source = source_text.encode("utf-8") if source_is_bytes else source_text
        return real_compile(source, filename, mode, *args, **kwargs)
    return patched_compile


def main(argv: list[str] | None = None) -> int:
    return int(load_impl().main(argv))


if __name__ == "__main__":
    _real_compile = builtins.compile
    builtins.compile = _compile_with_stable_root(_real_compile)
    try:
        raise SystemExit(main())
    except Exception as exc:
        os.write(2, ("C79G_R63AX_EXTERNAL_BOOTSTRAP_REJECT: " +
                     str(exc) + "\n").encode("utf-8", "backslashreplace"))
        raise SystemExit(2)
    finally:
        builtins.compile = _real_compile
