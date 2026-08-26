from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from . import __version__


def is_immutable_code_version(revision: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{40}", revision)) or bool(
        os.getenv("THETA_CODE_VERSION")
    )


def code_version() -> str:
    """Resolve an immutable revision without requiring Git on a deployment host."""
    override = os.getenv("THETA_CODE_VERSION")
    if override:
        return override
    root = Path(__file__).resolve().parents[2]
    head_path = root / ".git" / "HEAD"
    try:
        head = head_path.read_text(encoding="utf-8").strip()
        if head.startswith("ref: "):
            revision = (root / ".git" / head[5:]).read_text(encoding="utf-8").strip()
        else:
            revision = head
        if revision:
            try:
                status = subprocess.run(
                    ["git", "status", "--porcelain", "--untracked-files=all"],
                    cwd=root,
                    capture_output=True,
                    check=False,
                    text=True,
                    timeout=5,
                )
                if status.returncode == 0 and status.stdout.strip():
                    return revision + "-dirty"
            except (OSError, subprocess.SubprocessError):
                pass
            return revision
    except OSError:
        pass
    return f"project-theta-{__version__}"
