from promptfill.gui.app import list_index_after_delta


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
