from shop.reports import is_large


def test_is_large_above_limit():
    assert is_large({"total": 1500}) is True


def test_is_large_below_limit():
    assert is_large({"total": 10}) is False


def test_is_large_at_limit():
    assert is_large({"total": 1000}) is False
