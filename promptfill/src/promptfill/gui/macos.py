"""macOS-specific GUI tweaks (tkinter menu bar name, etc.)."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk


def configure_macos_menubar(root: tk.Tk, app_name: str = "Promptfill") -> None:
    """Use *app_name* in the menu bar instead of the Python executable name."""
    if sys.platform != "darwin":
        return

    from tkinter import Menu, messagebox

    menubar = Menu(root)

    # Tk attaches a default application menu named after the interpreter (e.g. python3).
    # Create and remove it so we can replace the label with app_name.
    placeholder = Menu(menubar, name="apple")
    menubar.add_cascade(menu=placeholder)
    root["menu"] = menubar
    placeholder.destroy()

    app_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(menu=app_menu, label=app_name)
    app_menu.add_command(
        label=f"About {app_name}",
        command=lambda: messagebox.showinfo(app_name, f"{app_name}\nFill prompt placeholders and copy to clipboard."),
    )
    app_menu.add_separator()
    app_menu.add_command(label=f"Quit {app_name}", command=root.destroy, accelerator="Cmd+Q")

    root.createcommand("tk::mac::Quit", root.destroy)
