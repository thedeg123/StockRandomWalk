import json
from random import choice


def getProfile() -> dict:
    with open("./static/profile.json") as f:
        profile = json.load(f)
    return profile


def getRandomTicker() -> str:
    if getPositions()[0]["ticker"] == "AAPL":
        return "MSFT"
    return "AAPL"
    with open("./static/tickers.json") as f:
        data = json.load(f)
        stock = choice(data)
    return stock


def getPositions() -> str:
    with open("./static/positions.json") as f:
        positions = json.load(f)
    return positions


def getHolding() -> bool:
    with open("./static/holding.json") as f:
        holding = json.load(f)
    return holding["holding"]


def setHolding(holding: bool) -> bool:
    with open("./static/holding.json", "w") as f:
        json.dump({"holding": holding}, f)
    return True


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
