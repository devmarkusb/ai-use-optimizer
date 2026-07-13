"""Desktop GUI for promptfill (tkinter, cross-platform)."""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from promptfill.clipboard import ClipboardError
from promptfill.focus import paste_back
from promptfill.gui.icon import apply_window_icon
from promptfill.gui.macos import configure_macos_menubar
from promptfill.gui.navigation import list_index_after_delta
from promptfill.schema import FieldSpec
from promptfill.workflow import (
    catalog_for,
    copy_rendered,
    fill_prompt,
    initial_values,
    resolve_prompts_dir,
    schema_for,
)

FIELD_LINES = 5
MULTILINE_FIELD_LINES = 8


def _xdotool_available() -> bool:
    from shutil import which

    return which("xdotool") is not None


class PromptfillApp:
    def __init__(self, root: tk.Tk, prompts_dir: Path) -> None:
        self.root = root
        self.prompts_dir = prompts_dir
        self.catalog = catalog_for(prompts_dir)
        self.filtered: list[tuple[Path, str]] = list(self.catalog)
        self.selected_path: Path | None = None
        self.field_widgets: dict[str, tk.Text] = {}
        self._skip_listbox_select = False

        root.title("Promptfill")
        root.minsize(720, 520)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self._build_layout()
        self._bind_submit_shortcuts()
        self._bind_list_navigation()
        self._refresh_list()
        if self.filtered:
            self.prompt_list.selection_set(0)
            self._load_selection(focus_fields=True)

    def _build_layout(self) -> None:
        paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        paned.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        left = ttk.Frame(paned, padding=4)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)
        paned.add(left, weight=1)

        ttk.Label(left, text="Prompts").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_list())
        self.search_entry = ttk.Entry(left, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        list_frame = ttk.Frame(left)
        list_frame.grid(row=2, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.prompt_list = tk.Listbox(list_frame, exportselection=False)
        self.prompt_list.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.prompt_list.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.prompt_list.configure(yscrollcommand=scroll.set)
        self.prompt_list.bind("<<ListboxSelect>>", self._on_listbox_select)
        self.prompt_list.bind("<Return>", self._on_return)

        right = ttk.Frame(paned, padding=4)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        paned.add(right, weight=2)

        header = ttk.Frame(right)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        header.columnconfigure(0, weight=1)
        self.header = header
        self.title_label = ttk.Label(header, text="Select a prompt", font=("", 13, "bold"))
        self.title_label.grid(row=0, column=0, sticky="ew")
        self.copy_btn = ttk.Button(
            header,
            text="Copy & paste (Enter)",
            command=self._submit_and_close,
            state=tk.DISABLED,
        )
        self.copy_btn.grid(row=1, column=0, sticky="e", pady=(6, 0))
        header.bind("<Configure>", self._on_header_configure)

        self.form_canvas = tk.Canvas(right, highlightthickness=0)
        self.form_frame = ttk.Frame(self.form_canvas)
        self.form_scroll = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.form_canvas.yview)
        self.form_canvas.configure(yscrollcommand=self.form_scroll.set)
        self.form_canvas.grid(row=1, column=0, sticky="nsew")
        self.form_scroll.grid(row=1, column=1, sticky="ns")
        self.form_window = self.form_canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.form_frame.bind("<Configure>", self._on_form_configure)
        self.form_canvas.bind("<Configure>", self._on_canvas_configure)

        self.status_var = tk.StringVar(
            value=f"Enter: copy, paste back, close · Shift+Enter: newline · {self.prompts_dir}"
        )
        ttk.Label(self.root, textvariable=self.status_var).grid(
            row=1, column=0, sticky="ew", padx=8, pady=(0, 6)
        )

    def _bind_submit_shortcuts(self) -> None:
        self.root.bind("<Return>", self._on_return)
        self.root.bind("<Escape>", lambda _e: self.root.destroy())

    def _bind_list_navigation(self) -> None:
        for sequence in ("<Up>", "<Down>"):
            self.search_entry.bind(sequence, self._on_arrow_nav)
            self.prompt_list.bind(sequence, self._on_arrow_nav)
        for widget in (self.search_entry, self.prompt_list):
            widget.bind("<Tab>", self._focus_first_field)
            widget.bind("<Shift-Tab>", self._focus_last_field)
            widget.bind("<ISO_Left_Tab>", self._focus_last_field)

    def _on_return(self, event: tk.Event) -> str | None:
        widget = event.widget
        if isinstance(widget, tk.Text) and self._shift_held(event):
            widget.insert(tk.INSERT, "\n")
            return "break"
        if isinstance(widget, tk.Listbox) and self.field_widgets:
            return None
        self._submit_and_close()
        return "break"

    def _on_arrow_nav(self, event: tk.Event) -> str:
        if not self.filtered:
            return "break"

        delta = -1 if event.keysym == "Up" else 1
        index = self._list_index_after_delta(delta)
        self._move_list_selection(index)
        return "break"

    def _list_index_after_delta(self, delta: int) -> int:
        selection = self.prompt_list.curselection()
        current = selection[0] if selection else None
        return list_index_after_delta(current, delta, len(self.filtered))

    def _move_list_selection(self, index: int) -> None:
        self._skip_listbox_select = True
        self.prompt_list.focus_set()
        self.prompt_list.selection_clear(0, tk.END)
        self.prompt_list.selection_set(index)
        self.prompt_list.activate(index)
        self.prompt_list.see(index)
        self._load_selection(focus_fields=False)
        self._skip_listbox_select = False

    def _on_listbox_select(self, _event: tk.Event | None = None) -> None:
        if self._skip_listbox_select:
            return
        self._load_selection(focus_fields=True)

    @staticmethod
    def _shift_held(event: tk.Event) -> bool:
        return bool(event.state & 0x0001)

    def _on_shift_return(self, event: tk.Event) -> str:
        if isinstance(event.widget, tk.Text):
            event.widget.insert(tk.INSERT, "\n")
        return "break"

    def _field_widgets_in_order(self) -> list[tk.Text]:
        return list(self.field_widgets.values())

    def _focus_field_at(self, index: int) -> str | None:
        widgets = self._field_widgets_in_order()
        if not widgets:
            return None
        widgets[index].focus_set()
        return "break"

    def _focus_first_field(self, _event: tk.Event) -> str | None:
        return self._focus_field_at(0)

    def _focus_last_field(self, _event: tk.Event) -> str | None:
        return self._focus_field_at(-1)

    def _focus_relative_field(self, widget: object, delta: int) -> str | None:
        widgets = self._field_widgets_in_order()
        if not widgets:
            return None
        try:
            current = widgets.index(widget)
        except ValueError:
            current = None
        index = list_index_after_delta(current, delta, len(widgets))
        widgets[index].focus_set()
        return "break"

    def _on_field_tab(self, event: tk.Event) -> str | None:
        return self._focus_relative_field(event.widget, 1)

    def _on_field_shift_tab(self, event: tk.Event) -> str | None:
        return self._focus_relative_field(event.widget, -1)

    def _bind_field_widget(self, widget: tk.Text) -> None:
        widget.bind("<Return>", self._on_return)
        widget.bind("<Shift-Return>", self._on_shift_return)
        widget.bind("<Tab>", self._on_field_tab)
        widget.bind("<Shift-Tab>", self._on_field_shift_tab)
        widget.bind("<ISO_Left_Tab>", self._on_field_shift_tab)

    def _on_header_configure(self, event: tk.Event) -> None:
        wrap = max(event.width - 8, 120)
        self.title_label.configure(wraplength=wrap)

    def _on_form_configure(self, _event: tk.Event) -> None:
        self.form_canvas.configure(scrollregion=self.form_canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.form_canvas.itemconfigure(self.form_window, width=event.width)

    def _refresh_list(self) -> None:
        query = self.search_var.get().strip().lower()
        if query:
            self.filtered = [
                item for item in self.catalog if query in item[1].lower() or query in item[0].name.lower()
            ]
        else:
            self.filtered = list(self.catalog)

        self.prompt_list.delete(0, tk.END)
        for _path, title in self.filtered:
            self.prompt_list.insert(tk.END, title)

    def _load_selection(self, *, focus_fields: bool) -> None:
        selection = self.prompt_list.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(self.filtered):
            return
        path, title = self.filtered[index]
        self.selected_path = path
        self.title_label.configure(text=title)
        self._build_form(path)
        self.copy_btn.configure(state=tk.NORMAL)
        self.status_var.set(f"{path.name} · Enter: copy & paste back · Shift+Enter: newline")

        if focus_fields and self.field_widgets:
            next(iter(self.field_widgets.values())).focus_set()
        else:
            self.prompt_list.focus_set()

    def _clear_form(self) -> None:
        for child in self.form_frame.winfo_children():
            child.destroy()
        self.field_widgets.clear()

    def _build_form(self, path: Path) -> None:
        self._clear_form()
        schema = schema_for(path)
        values = initial_values(schema)

        if not schema:
            ttk.Label(self.form_frame, text="No placeholders — press Enter to copy as-is.").grid(
                row=0, column=0, sticky="w", pady=4
            )
            return

        for index, field in enumerate(schema):
            self._add_field(index * 2, field, values.get(field.name, ""))

    def _add_field(self, base_row: int, field: FieldSpec, value: str) -> None:
        label = field.display_label + (" *" if field.required else "")
        ttk.Label(self.form_frame, text=label).grid(row=base_row, column=0, sticky="nw", pady=(8, 2))

        height = MULTILINE_FIELD_LINES if field.multiline else FIELD_LINES
        widget = scrolledtext.ScrolledText(
            self.form_frame,
            height=height,
            wrap=tk.WORD,
            undo=True,
        )
        widget.insert("1.0", value)
        widget.grid(row=base_row + 1, column=0, sticky="ew", pady=(0, 4))
        self.form_frame.columnconfigure(0, weight=1)
        self.field_widgets[field.name] = widget
        self._bind_field_widget(widget)

    def _collect_values(self) -> dict[str, str]:
        values: dict[str, str] = {}
        if self.selected_path is None:
            return values
        for name, widget in self.field_widgets.items():
            values[name] = widget.get("1.0", "end-1c")
        return values

    def _submit_and_close(self) -> None:
        if self.selected_path is None:
            return
        outcome = fill_prompt(self.selected_path, self._collect_values())
        if not outcome.ok:
            missing = ", ".join(f"<{name}>" for name in outcome.missing)
            messagebox.showerror("Missing required fields", f"Fill required placeholders: {missing}")
            return
        try:
            copy_rendered(outcome.rendered)
        except ClipboardError as exc:
            messagebox.showerror("Clipboard error", str(exc))
            return

        if sys.platform.startswith("linux") and not _xdotool_available():
            messagebox.showwarning(
                "Paste-back unavailable",
                "xdotool is not installed — the prompt was copied to your clipboard.\n\n"
                "To enable auto-paste on Linux, run:\n  sudo apt install xdotool",
            )
            self.root.destroy()
            return

        self.root.withdraw()
        self.root.update_idletasks()
        paste_back()
        self.root.destroy()

    def _fill(self):
        assert self.selected_path is not None
        return fill_prompt(self.selected_path, self._collect_values())


def run_gui(prompts_dir: Path | None = None) -> int:
    try:
        resolved = resolve_prompts_dir(prompts_dir)
    except FileNotFoundError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Promptfill", str(exc))
        root.destroy()
        return 1

    catalog = catalog_for(resolved)
    if not catalog:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Promptfill", f"No .md prompt files in {resolved}")
        root.destroy()
        return 1

    root = tk.Tk()
    configure_macos_menubar(root)
    apply_window_icon(root)
    PromptfillApp(root, resolved)
    root.mainloop()
    return 0
