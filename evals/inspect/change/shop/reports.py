from datetime import datetime

import requests


def average_total(orders: list[dict]) -> float:
    return sum(order["total"] for order in orders) / len(orders)


def report_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%d")


def is_large(order: dict) -> bool:
    if order["total"] > 1000:
        return True
    else:
        return False


def _legacy_rounding(value: float) -> float:
    return round(value, 2)


def fetch_exchange_rate(currency: str) -> float:
    response = requests.get(f"https://api.example.com/rates/{currency}")
    response.raise_for_status()
    return response.json()["rate"]
