import requests

from fastapi import FastAPI, HTTPException, Depends
from .schemas import get_currency_headers

app = FastAPI()

url = 'https://api.exchangerate.host/'


@app.get("/api/rates")
def convert_currency(currency_headers: tuple = Depends(get_currency_headers)):
    """
        Convert currency based on provided parameters.

    :parameter:
        - `from_currency` (str): From currency code.
        - `to` (str): To currency code.
        - `value` (float): Value to convert.

    :return:
        - `result` (float): Converted value.
    """
    from_currency, to, value = currency_headers
    conversion_url = f'{url}convert?from={from_currency}&to={to}'
    response = requests.get(conversion_url).json()

    if 'result' not in response:
        raise HTTPException(
            status_code=400,
            detail="Invalid response from exchange rate service"
            )

    if response['result'] is None:
        raise HTTPException(status_code=400, detail="Invalid currency code")

    result = round(response['result'] * value, 2)
    return {"result": result}


@app.get("/api/symbols")
def get_symbols():
    """
        Get available symbols

    :return:
        list of symbols available for calculation
    """
    symbols_url = url + "symbols"
    response = requests.get(symbols_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch symbols")

    symbols_data = response.json()
    symbols = symbols_data.get("symbols", {})

    return symbols
