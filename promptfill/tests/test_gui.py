from promptfill.gui.icon import icon_path
from promptfill.gui.navigation import list_index_after_delta


def test_bundled_icon_exists():
    path = icon_path()
    assert path is not None
    assert path.name == "icon.png"
    assert path.stat().st_size > 0


def test_list_index_after_delta_from_selection():
    assert list_index_after_delta(2, -1, 5) == 1
    assert list_index_after_delta(2, 1, 5) == 3
    assert list_index_after_delta(0, -1, 5) == 0
    assert list_index_after_delta(4, 1, 5) == 4


def test_list_index_after_delta_without_selection():
    assert list_index_after_delta(None, 1, 5) == 0
    assert list_index_after_delta(None, -1, 5) == 4


def test_list_index_after_delta_empty_list():
    assert list_index_after_delta(None, 1, 0) == 0
