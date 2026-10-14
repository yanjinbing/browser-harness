"""browser-harness filesystem layout."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def home_dir() -> Path:
    raw = os.environ.get("BH_HOME") or os.environ.get("BROWSER_HARNESS_HOME")
    if raw:
        return Path(raw).expanduser().resolve()
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        return (Path(base).expanduser() / "browser-harness").resolve()
    return (Path.home() / ".config" / "browser-harness").resolve()


def ensure_private_dir(path: Path) -> Path:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True)
    if not existed and sys.platform != "win32":
        os.chmod(path, 0o700)
    return path


def config_dir() -> Path:
    raw = os.environ.get("BH_CONFIG_DIR")
    return ensure_private_dir(Path(raw).expanduser().resolve() if raw else home_dir())


def inspect_marker() -> Path:
    """Marker recording that the harness opened a chrome://inspect tab"""
    return config_dir() / "inspect-opened"


def runtime_dir() -> Path:
    raw = os.environ.get("BH_RUNTIME_DIR")
    return ensure_private_dir(Path(raw).expanduser().resolve() if raw else home_dir() / "runtime")


def tmp_dir() -> Path:
    raw = os.environ.get("BH_TMP_DIR")
    return ensure_private_dir(Path(raw).expanduser().resolve() if raw else home_dir() / "tmp")


def workspace_dir() -> Path:
    raw = os.environ.get("BH_AGENT_WORKSPACE")
    return ensure_private_dir(Path(raw).expanduser().resolve() if raw else home_dir() / "agent-workspace")


def automation_profile_dir() -> Path:
    """Dedicated user-data dir for the browser we auto-launch.

    Kept separate from the user's real browser profiles: an automation
    instance must never take over a profile the user is browsing in, and on
    recent Chrome builds a dedicated profile is the only one that reliably
    accepts ``--remote-debugging-port``.
    """
    raw = (os.environ.get("BH_AUTO_PROFILE_DIR") or "").strip()
    if raw:
        return ensure_private_dir(Path(raw).expanduser().resolve())
    return ensure_private_dir(home_dir() / "automation-profile")


def auto_debug_port() -> int:
    """Remote-debugging port used for browsers we launch ourselves."""
    raw = (os.environ.get("BH_AUTO_PORT") or "").strip()
    if raw.isdigit():
        try:
            port = int(raw)
        except ValueError:
            port = 0
        if 1 <= port <= 65535:
            return port
    return 9333
