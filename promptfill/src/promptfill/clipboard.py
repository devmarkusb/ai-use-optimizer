"""Copy text to the system clipboard."""

from __future__ import annotations

import subprocess
import sys


class ClipboardError(RuntimeError):
    pass


def copy_to_clipboard(text: str) -> None:
    platform = sys.platform
    encoded = text.encode("utf-8")

    if platform == "darwin":
        subprocess.run(["pbcopy"], input=encoded, check=True)
        return

    if platform == "win32":
        subprocess.run(["clip"], input=encoded, check=True, shell=True)
        return

    if platform.startswith("linux"):
        for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"]):
            try:
                subprocess.run(cmd, input=encoded, check=True)
                return
            except FileNotFoundError:
                continue
        raise ClipboardError(
            "No clipboard tool found. Install wl-clipboard (wl-copy) or xclip."
        )

    raise ClipboardError(f"Clipboard copy is not supported on platform: {platform}")
