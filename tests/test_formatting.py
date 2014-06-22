from autosort.formatting import dynamic_wrap


def test_dynamic_wrapping():
    assert dynamic_wrap([], 2) == []
    assert dynamic_wrap([3, 2, 2, 4], 5) == [(0, 1), (1, 3), (3, 4)]
    assert dynamic_wrap([1, 3, 1], 2) == [(0, 1), (1, 2), (2, 3)]
