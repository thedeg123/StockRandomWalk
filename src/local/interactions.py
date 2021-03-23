import json
from random import choice


def getProfile() -> dict:
    with open("./static/profile.json") as f:
        profile = json.load(f)
    return profile


def getRandomTicker(crypto: bool = False, sAndPOnly: bool = True) -> str:
    if crypto:
        if getPositions()[0]["ticker"] == "BTC":
            return "ETH"
        return "BTC"
    fileString = "./static/s&p.json" if sAndPOnly else "./static/tickers.json"
    with open(fileString) as f:
        data = json.load(f)
        stock = choice(data)
    return stock


def getPositions() -> str:
    with open("./static/positions.json") as f:
        positions = json.load(f)
    return positions["positions"]


def getPurchasePower() -> float:
    if getHolding():
        return 0.0
    with open("./static/positions.json") as f:
        power = json.load(f)["purchase_power"]
    return float(power)


def getHolding() -> bool:
    with open("./static/positions.json") as f:
        positions = json.load(f)
    return bool(positions["holding"])


def setHolding(holding: bool) -> bool:
    purchasePower = getPurchasePower()
    positions = getPositions()
    with open("./static/positions.json", "w") as f:
        json.dump({"holding": holding,
                   "purchase_power": purchasePower,
                   "positions": positions
                   }, f)
    return True


def setPurchasePower(power: float) -> bool:
    holding = getHolding()
    positions = getPositions()
    with open("./static/positions.json", "w") as f:
        json.dump({"holding": holding,
                   "purchase_power": power,
                   "positions": positions
                   }, f)
    return True


def setPositions(ticker: str, price: float, quantity: float) -> bool:
    holding = getHolding()
    purchasePower = getPurchasePower()
    with open("./static/positions.json", "w") as f:
        json.dump({
            "holding": holding,
            "purchase_power": purchasePower,
            "positions": [
                {
                    "ticker": ticker,
                    "purchase_price": price,
                    "quantity": quantity
                }
            ]}, f)
    return True
