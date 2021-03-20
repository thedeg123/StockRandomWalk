import json
from random import choice
with open("./static/tickers.json") as f:
    data = json.load(f)
    print(choice(data))
