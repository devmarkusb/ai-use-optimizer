"""Desktop GUI entry points."""

__all__ = ["run_gui"]


def __getattr__(name: str):
    if name == "run_gui":
        from promptfill.gui.app import run_gui

        return run_gui
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
