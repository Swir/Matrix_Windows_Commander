from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path


def is_windows() -> bool:
    return sys.platform == "win32"


def is_admin() -> bool:
    if not is_windows():
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative


def relaunch_as_admin() -> bool:
    if not is_windows():
        return False
    if getattr(sys, "frozen", False):
        executable = sys.executable
        params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    else:
        executable = sys.executable
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{script}"', *(f'"{arg}"' for arg in sys.argv[1:])])
    try:
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
        return int(result) > 32
    except Exception:
        return False
