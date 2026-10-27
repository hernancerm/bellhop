from datetime import datetime

from shop.orders import order_summary


def test_order_summary():
    order = {"id": 7, "customer": "Ada", "created_at": datetime(2026, 1, 2)}
    assert order_summary(order) == "Order 7 for Ada on 2026-01-02"
