"""List navigation helpers for the promptfill desktop GUI (no tkinter)."""


def list_index_after_delta(current: int | None, delta: int, count: int) -> int:
    """Return the list index after moving by delta, wrapping at the list ends."""
    if count <= 0:
        return 0
    if current is None:
        return 0 if delta > 0 else count - 1
    return (current + delta) % count
