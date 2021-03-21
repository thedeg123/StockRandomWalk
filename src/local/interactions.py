import json
from random import choice


def getAuth() -> dict:
    with open("./static/profile.json") as f:
        profile = json.load(f)
    return profile


def getRandomTicker() -> str:
    return "BTC"
    with open("./static/tickers.json") as f:
        data = json.load(f)
        stock = choice(data)
    return stock


def getPositions() -> str:
    with open("./static/positions.json") as f:
        positions = json.load(f)
    return positions


def setPositions(ticker: str, price: float, quantity: float) -> bool:
    with open("./static/positions.json", "w") as f:
        json.dump([
            {
                "ticker": ticker,
                "purchase_price": price,
                "quantity": quantity
            }
        ], f)
    return True
