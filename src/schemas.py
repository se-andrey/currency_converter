from fastapi import Header


def get_currency_headers(
    from_currency: str = Header(..., description="From currency code"),
    to: str = Header(..., description="To currency code"),
    value: float = Header(..., description="Value to convert")
):
    return from_currency, to, value
