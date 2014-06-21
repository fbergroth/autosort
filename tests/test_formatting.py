from autosort.formatting import _dynamic_wrap


def test_dynamic_wrapping():
    assert _dynamic_wrap([], 2) == []
    assert _dynamic_wrap([3, 2, 2, 4], 5) == [(0, 1), (1, 3), (3, 4)]
    assert _dynamic_wrap([1, 3, 1], 2) == [(0, 1), (1, 2), (2, 3)]
