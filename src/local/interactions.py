import json
from random import choice


def getAuth() -> dict:
    with open("./static/profile.json") as f:
        profile = json.load(f)
    return profile


def getRandomTicker() -> str:
    with open("./static/tickers.json") as f:
        data = json.load(f)
        stock = choice(data)
    return stock


def getPositions() -> str:
    with open("./static/positions.json") as f:
        positions = json.load(f)
    return positions
