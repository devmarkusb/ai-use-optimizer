"""Window icon for the promptfill desktop GUI."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk


def icon_path() -> Path | None:
    """Return the bundled PNG icon path, or None if missing."""
    try:
        ref = resources.files("promptfill.assets").joinpath("icon.png")
    except (ModuleNotFoundError, TypeError):
        return None
    path = Path(ref)
    return path if path.is_file() else None


def apply_window_icon(root: tk.Misc) -> None:
    """Set the window (and child) icon from the bundled asset."""
    import tkinter as tk

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
