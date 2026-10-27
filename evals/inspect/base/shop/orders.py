from shop.dates import format_iso_date


def order_summary(order: dict) -> str:
    return f"Order {order['id']} on {format_iso_date(order['created_at'])}"
