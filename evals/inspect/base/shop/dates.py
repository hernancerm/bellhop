from datetime import datetime


def format_iso_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%d")
