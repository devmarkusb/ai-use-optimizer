"""List navigation helpers for the promptfill desktop GUI (no tkinter)."""


def list_index_after_delta(current: int | None, delta: int, count: int) -> int:
    """Return the list index after moving by delta, clamped to [0, count - 1]."""
    if count <= 0:
        return 0
    if current is None:
        index = 0 if delta > 0 else count - 1
    else:
        index = current + delta
    return max(0, min(count - 1, index))
