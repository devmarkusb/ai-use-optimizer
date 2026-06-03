"""Capture the pre-launch window and paste back after fill (Espanso ;p flow)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Literal

ENV_KEY = "PROMPTFILL_RETURN_TARGET"
PASTE_DELAY_S = 0.15


class PasteUnavailableError(RuntimeError):
    """Raised by paste_back() when the required tool is not installed."""


@dataclass(frozen=True)
class ReturnTarget:
    kind: Literal["mac_bundle", "x11_window", "win_hwnd"]
    value: str

    def encode(self) -> str:
        return json.dumps({"kind": self.kind, "value": self.value})

    @staticmethod
    def decode(raw: str) -> ReturnTarget | None:
        try:
            data = json.loads(raw)
            kind = data["kind"]
            value = str(data["value"])
            if kind in ("mac_bundle", "x11_window", "win_hwnd") and value:
                return ReturnTarget(kind=kind, value=value)
        except (KeyError, TypeError, json.JSONDecodeError):
            return None
        return None


def capture_target() -> str | None:
    target = _capture_target()
    return target.encode() if target else None


def paste_back() -> bool:
    raw = os.environ.get(ENV_KEY)
    if not raw:
        return False
    target = ReturnTarget.decode(raw)
    if target is None:
        return False
    if target.kind == "mac_bundle":
        return _paste_macos(target.value)
    if target.kind == "x11_window":
        return _paste_x11(target.value)
    if target.kind == "win_hwnd":
        return _paste_windows(target.value)
    return False


def _capture_target() -> ReturnTarget | None:
    if sys.platform == "darwin":
        return _capture_macos()
    if sys.platform == "win32":
        return _capture_windows()
    if sys.platform.startswith("linux"):
        return _capture_linux()
    return None


def _capture_macos() -> ReturnTarget | None:
    script = (
        "tell application \"System Events\"\n"
        "  set p to first application process whose frontmost is true\n"
        "  return bundle identifier of p\n"
        "end tell"
    )
    proc = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=False,
    )
    bundle = proc.stdout.strip()
    if proc.returncode != 0 or not bundle:
        return None
    return ReturnTarget("mac_bundle", bundle)


def _paste_macos(bundle_id: str) -> bool:
    safe = bundle_id.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'tell application id "{safe}" to activate\n'
        f"delay {PASTE_DELAY_S}\n"
        'tell application "System Events" to keystroke "v" using command down'
    )
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, check=False)
    return proc.returncode == 0


def _capture_linux() -> ReturnTarget | None:
    if not _which("xdotool"):
        import warnings

        warnings.warn(
            "xdotool is not installed — paste-back is disabled on Linux/X11. "
            "Run: sudo apt install xdotool",
            stacklevel=3,
        )
        return None
    proc = subprocess.run(
        ["xdotool", "getactivewindow"],
        capture_output=True,
        text=True,
        check=False,
    )
    window_id = proc.stdout.strip()
    if proc.returncode != 0 or not window_id.isdigit():
        return None
    return ReturnTarget("x11_window", window_id)


def _paste_x11(window_id: str) -> bool:
    if not _which("xdotool"):
        return False
    activate = subprocess.run(["xdotool", "windowactivate", "--sync", window_id], check=False)
    if activate.returncode != 0:
        return False
    time.sleep(PASTE_DELAY_S)
    paste = subprocess.run(["xdotool", "key", "--clearmodifiers", "ctrl+v"], check=False)
    return paste.returncode == 0


def _capture_windows() -> ReturnTarget | None:
    try:
        import ctypes

        hwnd = ctypes.windll.user32.GetForegroundWindow()  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        return None
    if not hwnd:
        return None
    return ReturnTarget("win_hwnd", str(int(hwnd)))


def _paste_windows(hwnd_text: str) -> bool:
    if not hwnd_text.isdigit():
        return False
    hwnd = int(hwnd_text)
    script = (
        f"$sig = @'\n"
        "[DllImport(\"user32.dll\")] public static extern bool SetForegroundWindow(IntPtr hWnd);\n"
        "'@\n"
        "$type = Add-Type -MemberDefinition $sig -Name W -Namespace Promptfill -PassThru\n"
        f"[void]$type::SetForegroundWindow([IntPtr]{hwnd})\n"
        f"Start-Sleep -Milliseconds {int(PASTE_DELAY_S * 1000)}\n"
        "$wshell = New-Object -ComObject wscript.shell\n"
        "$wshell.SendKeys('^v')"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        check=False,
    )
    return proc.returncode == 0


def _which(name: str) -> bool:
    from shutil import which

    return which(name) is not None
