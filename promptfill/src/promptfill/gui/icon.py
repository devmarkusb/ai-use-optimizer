"""Window icon for the promptfill desktop GUI."""

from __future__ import annotations

import tkinter as tk
from importlib import resources
from pathlib import Path


def icon_path() -> Path | None:
    """Return the bundled PNG icon path, or None if missing."""
    try:
        ref = resources.files("promptfill.assets").joinpath("icon.png")
    except (ModuleNotFoundError, TypeError):
        return None
    path = Path(ref)
    return path if path.is_file() else None


def apply_window_icon(root: tk.Tk) -> None:
    """Set the window (and child) icon from the bundled asset."""
    path = icon_path()
    if path is None:
        return
    try:
        photo = tk.PhotoImage(file=str(path))
    except tk.TclError:
        return
    root.iconphoto(True, photo)
    # Prevent garbage collection of the image while the window exists.
    root._promptfill_icon = photo  # type: ignore[attr-defined]
