"""
helpers/fs.py

Small filesystem helper to centralize resolution of the agent filesystem root.
- Respects AGENT_FS_ROOT env var
- Provides FOOTPATH alias for compatibility
- Falls back to ./usr then repo root
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from helpers import files

_ENV_VAR = "AGENT_FS_ROOT"
_FOOTPATH_ENV = "FOOTPATH"


def resolve_fs_root() -> str:
    # 1) explicit env var
    env = os.environ.get(_ENV_VAR)
    if env:
        return str(Path(env).expanduser().resolve())

    # 2) compatibility alias
    foot = os.environ.get(_FOOTPATH_ENV)
    if foot:
        return str(Path(foot).expanduser().resolve())

    # 3) prefer repo-local ./usr if it exists
    repo_usr = Path(files.get_base_dir()) / "usr"
    if repo_usr.exists():
        return str(repo_usr.resolve())

    # 4) fallback to repo root
    return str(Path(files.get_base_dir()).resolve())


def a0_path(*parts: str) -> str:
    """Return an absolute path under the resolved agent filesystem root.

    Example: a0_path('uploads', 'file.txt') -> /home/me/agent-zero/usr/uploads/file.txt
    """
    root = Path(resolve_fs_root())
    return str(root.joinpath(*parts))
