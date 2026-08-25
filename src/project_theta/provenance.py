from __future__ import annotations

import os
from pathlib import Path

from . import __version__


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
            return revision
    except OSError:
        pass
    return f"project-theta-{__version__}"
